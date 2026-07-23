#!/usr/bin/env python3
import csv
import hashlib
import html
import json
import os
import queue as queue_module
import re
import signal
import subprocess
import sys
import threading
import time
import multiprocessing
from datetime import datetime, timezone, timedelta
from urllib.parse import urljoin, urlparse

# --- CONFIGURACIÓN Y RUTAS ---
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DEFAULT_SOURCES = os.path.join(ROOT, 'data', 'Fuentes Normativas - limpio utf8 v2.csv')
CASES_FILE = os.environ.get('MONITOR_CASES_FILE', os.path.join(ROOT, 'data', 'casos_detectados.csv'))
INBOX_DIR = os.environ.get('MONITOR_INBOX_DIR', os.path.join(ROOT, 'raw', 'inbox'))
SITE_TREE_DIR = os.path.join(ROOT, 'wiki', 'operations', 'site_trees')
FINAL_LOG_FILE = os.environ.get('MONITOR_LOG_FILE', os.path.join(ROOT, 'wiki', 'operations', 'diagnostico_final.log'))
CURL_BIN = os.environ.get('MONITOR_CURL_BIN', 'curl')

# --- CONFIGURACIÓN DE RASTREO ---
# Subimos el nivel por defecto de profundidad de 1 a 2 para capturar
# documentos enlazados en una capa adicional del sitio fuente.
MAX_DEPTH = max(0, int(os.environ.get('MONITOR_MAX_DEPTH', '2')))
MAX_DOCS_PER_ENTITY = int(os.environ.get('MONITOR_MAX_DOCS_PER_ENTITY', '30'))
MAX_TIME_PER_ENTITY = int(os.environ.get('MONITOR_MAX_TIME_PER_ENTITY', '60'))
PDF_EXTRACTION_TIMEOUT = int(os.environ.get('MONITOR_PDF_TIMEOUT', '40'))

CANONICAL_HEADER = [
    'case_id', 'Resultado análisis', 'Fecha registro', 'Tipo', 'Título', 'URL',
    'Anexos', 'Fecha de publicación', 'Emisor', 'Norma', 'Fecha de divulgación',
    'Tipo de Norma', 'Tema', 'Sector Económico', 'Incidencia SURA',
    'Obligaciones SURA', 'Norma Importante', 'Control SOX', 'Divulgación SOX',
    'Compañía Impactada', 'Obligaciones', 'Persona que analizó',
    'Justificación de no divulgación SOX', 'detected_at', 'entidad', 'fuente_url',
    'document_url', 'publication_date', 'status', 'priority', 'aplica_sura',
    'link_status', 'link_error', 'notes', 'analisis_ia_status',
    'analisis_ia_fecha', 'tokens_ia', 'sincronizado_excel',
    'linea_negocio', 'impacto_ti', 'riesgo_sancionatorio', 
    'plazo_implementacion', 'control_sox_sugerido'
]
DOCUMENT_EXTENSIONS = {'pdf', 'doc', 'docx', 'xls', 'xlsx'}

# --- IN-MEMORY LOG ---
DIAGNOSTIC_LOG = []

shutdown_flag = threading.Event()

def signal_handler(sig, frame):
    if not shutdown_flag.is_set():
        print("\n🛑 INTERRUPCIÓN SOLICITADA (Ctrl+C). El reporte final se generará...")
        shutdown_flag.set()

signal.signal(signal.SIGINT, signal_handler)

try:
    import pdfplumber
    from docx import Document as DocxReader
except ImportError:
    pdfplumber = DocxReader = None

# --- HELPERS ---
def now_iso():
    return datetime.now(timezone(timedelta(hours=-5))).strftime('%Y-%m-%d %H:%M:%S%z')

def get_time():
    return datetime.now().strftime('%H:%M:%S')

def log_diagnostico(msg):
    DIAGNOSTIC_LOG.append(f"[{get_time()}] {msg}")

# --- ROBUST NETWORKING with cURL ---
def fetch_with_curl(url, max_seconds=20):
    max_seconds = max(1, min(20, int(max_seconds)))
    try:
        result = subprocess.run(
            [CURL_BIN, '-L', '--max-time', str(max_seconds), '-A', 'Mozilla/5.0 SURA-Compliance-Bot/3.0', url],
            capture_output=True, check=False, timeout=max_seconds + 5
        )
        if result.returncode == 0:
            return result.stdout, 'ok', None
        else:
            error_msg = result.stderr.decode('utf-8', 'ignore') if result.stderr else f"cURL exit code {result.returncode}"
            return None, 'error_curl', error_msg[:150]
    except subprocess.TimeoutExpired:
        return None, 'timeout_subprocess', 'cURL se congeló y fue terminado.'
    except Exception as e:
        return None, 'error_subprocess', str(e)

def download_with_curl(url, local_path, max_seconds=45):
    max_seconds = max(1, min(45, int(max_seconds)))
    partial_path = f"{local_path}.part"
    try:
        result = subprocess.run(
            [CURL_BIN, '-L', '-o', partial_path, '--max-time', str(max_seconds), '-A', 'SURA-Bot/3.0', url],
            capture_output=True, check=False, timeout=max_seconds + 5
        )
        if result.returncode == 0:
            os.replace(partial_path, local_path)
            return True, None
        return False, result.stderr.decode('utf-8', 'ignore') if result.stderr else "cURL download failed"
    except Exception as e:
        return False, str(e)
    finally:
        if os.path.exists(partial_path):
            os.remove(partial_path)

# --- PDF EXTRACTION SENTINEL ---
def _extract_pdf_worker(pdf_path, result_queue):
    try:
        import pdfplumber
        text_parts = []
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            # Estrategia Jurídica: Leer el inicio (contexto) y el final (sanciones/vigencia)
            if total_pages <= 15:
                # Si es corto, leer todo
                pages_to_read = pdf.pages
            else:
                # Si es largo, leer primeras 10 y últimas 5
                pages_to_read = pdf.pages[:10] + pdf.pages[-5:]
            
            for page in pages_to_read:
                text_parts.append(page.extract_text() or "")
        
        full_text = "\n".join(text_parts)
        # Limitar a ~60,000 caracteres para no romper el buffer de la IA pero ser exhaustivos
        result_queue.put(full_text[:60000])
    except Exception as e:
        result_queue.put(f"Error en subproceso: {e}")

def extract_text_sentinel(local_path, ext):
    if ext != 'pdf' or not pdfplumber:
        if ext in ['doc', 'docx'] and DocxReader:
            try:
                doc = DocxReader(local_path)
                return "\n".join([p.text for p in doc.paragraphs[:20]])
            except:
                return "Error extrayendo DOCX"
        return "No extraíble"

    result_queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=_extract_pdf_worker, args=(local_path, result_queue))
    p.start()
    try:
        result = result_queue.get(timeout=PDF_EXTRACTION_TIMEOUT)
    except queue_module.Empty:
        p.terminate()
        p.join()
        return f"Error de extracción: PDF bloqueado (Timeout {PDF_EXTRACTION_TIMEOUT}s)."
    finally:
        result_queue.close()
    p.join(timeout=1)
    if p.is_alive():
        p.terminate()
        p.join()
    return result


def seconds_remaining(deadline):
    return max(0, int(deadline - time.monotonic()))


def document_extension(url):
    path = urlparse(url).path
    match = re.search(r'\.(pdf|docx?|xlsx?)(?:/|$)', path, re.I)
    return match.group(1).lower() if match else 'dat'


def ensure_cases_schema():
    os.makedirs(os.path.dirname(CASES_FILE), exist_ok=True)
    if not os.path.exists(CASES_FILE):
        with open(CASES_FILE, 'w', encoding='utf-8', newline='') as f:
            csv.DictWriter(f, fieldnames=CANONICAL_HEADER).writeheader()
        return
    with open(CASES_FILE, 'r', encoding='utf-8', newline='') as f:
        actual_header = next(csv.reader(f), [])
    if actual_header != CANONICAL_HEADER:
        raise RuntimeError(
            f"Esquema incompatible en {CASES_FILE}: se esperaban "
            f"{len(CANONICAL_HEADER)} columnas y se encontraron {len(actual_header)}. "
            "No se escribió ningún caso."
        )


def write_final_log():
    os.makedirs(os.path.dirname(FINAL_LOG_FILE), exist_ok=True)
    with open(FINAL_LOG_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(DIAGNOSTIC_LOG))

# --- CORE PROCESSING LOGIC ---
def process_source(idx, row, seen_urls):
    entidad = row.get('Entidad', '').strip()
    fuente_url = row.get('Enlace', '').strip()
    log_diagnostico(f"[START] [{idx}] {entidad} -> {fuente_url}")
    print(f'[{get_time()}] 🚀 [monitor] [{idx}] INICIO | "{entidad}"')

    deadline = time.monotonic() + MAX_TIME_PER_ENTITY
    queue, visited, found_docs, docs_to_save = [(fuente_url, 0)], set(), {}, []

    while queue:
        if shutdown_flag.is_set() or seconds_remaining(deadline) <= 0:
            if not shutdown_flag.is_set():
                log_diagnostico(f"[{idx}] ⚠️ TIEMPO LÍMITE ({MAX_TIME_PER_ENTITY}s) SUPERADO para {entidad}.")
            break

        curr_url, depth = queue.pop(0)
        if curr_url in visited: continue
        visited.add(curr_url)

        body, status, err = fetch_with_curl(curr_url, seconds_remaining(deadline))
        if status != 'ok':
            log_diagnostico(f"[{idx}] ❌ FETCH FAIL en {curr_url}: {err}")
            if depth == 0:
                cid = hashlib.sha256(f"FAIL|{entidad}|{curr_url}".encode()).hexdigest()[:16]
                docs_to_save.append({'case_id': cid, 'status': 'error_fuente', 'link_error': err, 'entidad': entidad, 'fuente_url': fuente_url})
            continue

        decoded_body = body.decode('utf-8', 'ignore')
        links = re.findall(r'https?://[^\s"\'<>]+', decoded_body)
        links.extend(re.findall(r'''href=["']([^"']+)["']''', decoded_body, re.I))
        for u in links:
            abs_u = urljoin(curr_url, html.unescape(u)).split('#')[0]
            if abs_u in found_docs: continue

            if document_extension(abs_u) in DOCUMENT_EXTENSIONS:
                found_docs[abs_u] = curr_url
                if len(found_docs) >= MAX_DOCS_PER_ENTITY:
                    break
            elif depth < MAX_DEPTH and urlparse(curr_url).netloc == urlparse(abs_u).netloc and abs_u not in visited:
                if any(k in abs_u for k in ['norma', 'resolu', 'decreto', 'circular']):
                    queue.append((abs_u, depth + 1))
        if len(found_docs) >= MAX_DOCS_PER_ENTITY:
            log_diagnostico(f"[{idx}] ⚠️ LÍMITE DE DOCUMENTOS ({MAX_DOCS_PER_ENTITY}) ALCANZADO para {entidad}.")
            break

    log_diagnostico(f"[{idx}] {entidad}: {len(found_docs)} documentos encontrados para descargar.")

    for doc_url, parent_url in found_docs.items():
        remaining = seconds_remaining(deadline)
        if shutdown_flag.is_set() or remaining <= 0:
            if not shutdown_flag.is_set():
                log_diagnostico(f"[{idx}] ⚠️ TIEMPO LÍMITE ALCANZADO antes de descargar {doc_url}.")
            break
        cid = hashlib.sha256(f"DOC|{entidad}|{doc_url}".encode()).hexdigest()[:16]
        if cid in seen_urls: continue

        ext = document_extension(doc_url)
        local_path = os.path.join(INBOX_DIR, f"{cid}.{ext}")

        if os.path.exists(local_path):
            log_diagnostico(f"[{idx}]   -> Reutilizando descarga existente {local_path}")
            success, error_msg = True, None
        else:
            log_diagnostico(f"[{idx}]   -> Descargando {doc_url}")
            success, error_msg = download_with_curl(doc_url, local_path, remaining)

        notes = ""
        if success:
            log_diagnostico(f"[{idx}]   -> Extrayendo {local_path}")
            notes = extract_text_sentinel(local_path, ext)
        else:
            notes = f"Error de descarga: {error_msg}"

        docs_to_save.append({
            'case_id': cid, 'detected_at': now_iso(), 'entidad': entidad,
            'fuente_url': fuente_url, 'document_url': doc_url, 'status': 'detectado',
            'link_status': 'ok' if success else 'error_descarga', 'notes': notes,
            'Emisor': entidad, 'URL': doc_url, 'Título': doc_url.split('/')[-1]
        })
        seen_urls.add(cid)

    if docs_to_save:
        with open(CASES_FILE, 'a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=CANONICAL_HEADER)
            writer.writerows({field: row.get(field, '') for field in CANONICAL_HEADER} for row in docs_to_save)

    log_diagnostico(f"[{idx}] FIN | {len(docs_to_save)} nuevos casos guardados.")
    print(f'[{get_time()}] ✅ [monitor] [{idx}] FIN | "{entidad}" | {len(docs_to_save)} nuevos.')
    return True

# --- MAIN ---
def main():
    sources_file = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SOURCES
    os.makedirs(INBOX_DIR, exist_ok=True)
    ensure_cases_schema()

    seen_urls = set()
    if os.path.exists(CASES_FILE):
        with open(CASES_FILE, 'r', encoding='utf-8') as f:
            try:
                seen_urls.update(row['case_id'] for row in csv.DictReader(f))
            except: pass

    with open(sources_file, 'r', encoding='utf-8', newline='') as f:
        sources = [
            row for row in csv.DictReader(f)
            if row.get('Entidad', '').strip() and row.get('Enlace', '').strip()
        ]
    print(f"🚀 INICIO MONITOR INQUEBRANTABLE | {len(sources)} fuentes para analizar.")

    failed_sources = []

    for i, row in enumerate(sources):
        idx = i + 1
        if shutdown_flag.is_set():
            print("\n🛑 Interrupción. Generando reporte final...")
            break

        try:
            if not process_source(idx, row, seen_urls):
                 failed_sources.append((idx, row.get('Entidad'), "Fallo reportado en log"))
        except Exception as e:
            failed_sources.append((idx, row.get('Entidad'), f"CRÍTICO: {e}"))

    # Reporte final
    log_diagnostico("--- REPORTE DE BARRIDO ---")
    if failed_sources:
        log_diagnostico(f"❌ {len(failed_sources)} reguladores fallaron:")
        for idx, ent, err in failed_sources:
            log_diagnostico(f"   - [{idx}] {ent}: {err}")
    else:
        log_diagnostico("🎉 ¡Todos los reguladores se procesaron sin fallos críticos!")

    print("\n" + "="*50)
    print(f"🏁 BARRIDO FINALIZADO A LAS {get_time()}")
    print(f"📄 Reporte completo guardado en: {FINAL_LOG_FILE}")
    print("="*50)

if __name__ == '__main__':
    # Esta línea es crucial para que el centinela de procesos funcione en macOS/Windows
    multiprocessing.freeze_support()
    exit_code = 0
    try:
        main()
    except Exception as e:
        exit_code = 1
        log_diagnostico(f"❌ ERROR CRÍTICO: {e}")
        print(f"❌ ERROR CRÍTICO: {e}", file=sys.stderr)
    finally:
        write_final_log()
    sys.exit(exit_code)
