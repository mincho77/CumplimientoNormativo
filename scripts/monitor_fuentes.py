#!/usr/bin/env python3
import csv
import hashlib
import json
import os
import re
import socket
import sys
from datetime import datetime, timezone
from urllib.parse import urljoin
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DEFAULT_SOURCES = os.path.join(ROOT, 'data', 'Fuentes Normativas - limpio utf8 v2.csv')
STATE_DIR = os.path.join(ROOT, 'data', 'state')
STATE_FILE = os.path.join(STATE_DIR, 'monitor_state.json')
CASES_FILE = os.path.join(ROOT, 'data', 'casos_detectados.csv')
LOG_FILE = os.path.join(ROOT, 'wiki', 'operations', 'log.md')

URL_RE = re.compile(r'https?://[^\s"\'<>]+', re.I)
PDF_RE = re.compile(r'https?://[^\s"\'<>]+\.pdf(?:\?[^\s"\'<>]*)?', re.I)


def now_iso():
    return datetime.now(timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S%z')


def ensure_dirs():
    os.makedirs(STATE_DIR, exist_ok=True)
    os.makedirs(os.path.join(ROOT, 'raw', 'inbox'), exist_ok=True)


def load_state():
    if not os.path.exists(STATE_FILE):
        return {'seen': {}}
    with open(STATE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def read_sources(path):
    with open(path, 'r', encoding='utf-8', newline='') as f:
        sample = f.read(4096)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=',;\t|')
        except Exception:
            dialect = csv.get_dialect('excel')
        reader = csv.DictReader(f, dialect=dialect)
        return list(reader)


def fetch(url, timeout=20):
    """Fetch URL. Returns (data, ctype, status, error)."""
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (CumplimientoBot/0.1)'})
        with urlopen(req, timeout=timeout) as resp:
            ctype = resp.headers.get('Content-Type', '')
            data = resp.read()
        return data, ctype, 'ok', None
    except HTTPError as e:
        status = f'http_{e.code}'
        return None, None, status, f'{e.code} {e.reason}'
    except socket.timeout:
        return None, None, 'timeout', 'Socket timeout'
    except URLError as e:
        reason = str(e.reason) if hasattr(e, 'reason') else str(e)
        return None, None, 'conexion_error', reason
    except Exception as e:
        return None, None, 'error', str(e)


def extract_candidates(base_url, body_bytes, ctype):
    txt = body_bytes.decode('utf-8', errors='ignore')
    links = set(PDF_RE.findall(txt))
    if 'pdf' in ctype.lower() and base_url.lower().endswith('.pdf'):
        links.add(base_url)
    # also parse generic urls and keep .pdf ones after normalization
    for u in URL_RE.findall(txt):
        abs_u = urljoin(base_url, u)
        if '.pdf' in abs_u.lower():
            links.add(abs_u)
    return sorted(links)


def stable_id(entidad, source_url, doc_url):
    raw = f'{entidad}|{source_url}|{doc_url}'
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()[:16]


def append_cases(rows):
    exists = os.path.exists(CASES_FILE)
    with open(CASES_FILE, 'a', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=[
            'case_id', 'detected_at', 'entidad', 'fuente_url', 'document_url',
            'publication_date', 'status', 'priority', 'aplica_sura', 'link_status',
            'link_error', 'notes'
        ])
        if not exists:
            w.writeheader()
        for r in rows:
            w.writerow(r)


def append_log(summary):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"\n## [{datetime.now().strftime('%Y-%m-%d')}] monitor | corrida diaria\n")
        for line in summary:
            f.write(f"- {line}\n")


def main():
    sources_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SOURCES
    ensure_dirs()
    state = load_state()
    seen = state.setdefault('seen', {})
    sources = read_sources(sources_path)

    new_cases = []
    scanned = 0
    errors = 0

    total = len(sources)
    print(f'[monitor] inicio | fuentes_en_csv={total}')

    for idx, row in enumerate(sources, start=1):
        entidad = (row.get('Entidad') or '').strip()
        fuente_url = (row.get('Enlace') or '').strip()
        if not entidad or not fuente_url:
            print(f'[monitor] {idx}/{total} omitida | entidad/enlace vacio')
            continue
        scanned += 1
        print(f'[monitor] {idx}/{total} consultando | entidad="{entidad}" url="{fuente_url}"')

        body, ctype, status, error_msg = fetch(fuente_url)

        if status != 'ok':
            errors += 1
            print(f'[monitor] {idx}/{total} error | entidad="{entidad}" status={status} detalle="{error_msg}"')
            # Registrar error de fuente como caso con estado error
            cid = stable_id(entidad, fuente_url, fuente_url)
            if cid not in seen:
                seen[cid] = {'first_seen': now_iso(), 'entidad': entidad, 'fuente_url': fuente_url, 'document_url': fuente_url}
                new_cases.append({
                    'case_id': cid,
                    'detected_at': now_iso(),
                    'entidad': entidad,
                    'fuente_url': fuente_url,
                    'document_url': fuente_url,
                    'publication_date': '',
                    'status': 'error_fuente',
                    'priority': '',
                    'aplica_sura': '',
                    'link_status': status,
                    'link_error': error_msg,
                    'notes': f'Error accediendo fuente: {status}'
                })
            continue

        docs = extract_candidates(fuente_url, body, ctype)
        if not docs and fuente_url.lower().endswith('.pdf'):
            docs = [fuente_url]

        nuevos_entidad = 0
        for d in docs:
            cid = stable_id(entidad, fuente_url, d)
            if cid in seen:
                continue
            seen[cid] = {'first_seen': now_iso(), 'entidad': entidad, 'fuente_url': fuente_url, 'document_url': d}
            new_cases.append({
                'case_id': cid,
                'detected_at': now_iso(),
                'entidad': entidad,
                'fuente_url': fuente_url,
                'document_url': d,
                'publication_date': '',
                'status': 'detectado',
                'priority': '',
                'aplica_sura': '',
                'link_status': 'ok',
                'link_error': '',
                'notes': 'pendiente extracción/validación revisión manual'
            })
            nuevos_entidad += 1
        print(f'[monitor] {idx}/{total} ok | candidatos={len(docs)} nuevos={nuevos_entidad}')

    if new_cases:
        append_cases(new_cases)
    save_state(state)
    append_log([
        f'Fuentes escaneadas: {scanned}',
        f'Casos nuevos detectados: {len(new_cases)}',
        f'Fuentes con error: {errors}',
        f'Archivo de salida: data/casos_detectados.csv'
    ])

    print(f'[monitor] fin | scanned={scanned} new_cases={len(new_cases)} errors={errors}')


if __name__ == '__main__':
    main()
