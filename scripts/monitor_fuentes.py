#!/usr/bin/env python3
import csv
import hashlib
import json
import os
import re
import socket
import sys
import concurrent.futures
import threading
import ssl
import signal
import time
import requests
from datetime import datetime, timezone, timedelta
from urllib.parse import urljoin, urlparse
from urllib3.exceptions import InsecureRequestWarning

# Desactivar advertencias de SSL no verificado (necesario para sitios gov.co con TLS viejo)
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# --- CONFIGURACIÓN Y RUTAS ---
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DEFAULT_SOURCES = os.path.join(ROOT, 'data', 'Fuentes Normativas - limpio utf8 v2.csv')
STATE_DIR = os.path.join(ROOT, 'data', 'state')
STATE_FILE = os.path.join(STATE_DIR, 'monitor_state.json')
CASES_FILE = os.path.join(ROOT, 'data', 'casos_detectados.csv')
LOG_FILE = os.path.join(ROOT, 'wiki', 'operations', 'log.md')
SITE_TREE_DIR = os.path.join(ROOT, 'wiki', 'operations', 'site_trees')

# Configuración de Rastreo
MAX_DEPTH = 1  
MAX_DOCS_PER_ENTITY = 50
MAX_TIME_PER_ENTITY = 180 # 3 minutos

# Locks para concurrencia
csv_lock = threading.Lock()
state_lock = threading.Lock()
tree_lock = threading.Lock()

# Flag global para parada inmediata
shutdown_flag = threading.Event()

def signal_handler(sig, frame):
    if not shutdown_flag.is_set():
        print("\n🛑 INTERRUPCIÓN SOLICITADA (Ctrl+C). Cerrando de forma segura...")
        shutdown_flag.set()
    else:
        print("\n⚠️ Forzando cierre inmediato...")
        os._exit(1)

signal.signal(signal.SIGINT, signal_handler)

URL_RE = re.compile(r'https?://[^\s"\'<>]+', re.I)
DOCS_RE = re.compile(r'https?://[^\s"\'<>]+\.(?:pdf|docx?|xlsx?|zip|rar|7z|rtf|csv)(?:\?[^\s"\'<>]*)?', re.I)

try:
    import pdfplumber
    from docx import Document as DocxReader
except ImportError:
    pdfplumber = DocxReader = None

# --- FUNCIONES DE RED PROFESIONALES ---

def now_iso():
    tz = timezone(timedelta(hours=-5))
    return datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S%z')

def get_time():
    return datetime.now().strftime('%H:%M:%S')

def fetch(url, timeout=20):
    """Fetch URL usando la librería requests con timeouts estrictos."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) SURA-Compliance-Bot/1.0'}
        # timeout=(connect, read)
        response = requests.get(url, headers=headers, timeout=(10, timeout), verify=False, stream=True)
        response.raise_for_status()
        
        content_type = response.headers.get('Content-Type', '')
        
        # Leer el contenido con un límite de tamaño para evitar bloqueos por archivos gigantes (10MB max para análisis)
        max_size = 10 * 1024 * 1024 
        content = b""
        for chunk in response.iter_content(chunk_size=8192):
            if shutdown_flag.is_set(): return None, None, 'abort', 'Cancelado por usuario'
            content += chunk
            if len(content) > max_size:
                break
        
        return content, content_type, 'ok', None
    except requests.exceptions.Timeout:
        return None, None, 'timeout', 'Servidor no respondió a tiempo'
    except requests.exceptions.SSLError as e:
        return None, None, 'ssl_error', f'Fallo de seguridad SSL: {str(e)[:50]}'
    except requests.exceptions.ConnectionError:
        return None, None, 'conexion_error', 'No se pudo establecer conexión'
    except Exception as e:
        return None, None, 'error', str(e)[:50]

def download_file(url, local_path):
    """Descarga un archivo físico usando streaming."""
    try:
        with requests.get(url, stream=True, timeout=20, verify=False) as r:
            r.raise_for_status()
            with open(local_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if shutdown_flag.is_set(): return False
                    f.write(chunk)
        return True
    except:
        return False

def download_and_extract(url, case_id):
    inbox_dir = os.path.join(ROOT, 'raw', 'inbox')
    os.makedirs(inbox_dir, exist_ok=True)
    ext = url.split('?')[0].split('.')[-1].lower() if '.' in url else 'dat'
    local_path = os.path.join(inbox_dir, f"{case_id}.{ext}")
    
    if not download_file(url, local_path):
        return "Error en descarga o servidor no disponible.", "error"
    
    text = ""
    try:
        if ext == 'pdf' and pdfplumber:
            with pdfplumber.open(local_path) as pdf:
                text = "\n".join([(p.extract_text() or "") for p in pdf.pages[:3]])
        elif ext in ['doc', 'docx'] and DocxReader:
            doc = DocxReader(local_path)
            text = "\n".join([p.text for p in doc.paragraphs[:20]])
    except Exception as e:
        text = f"Error extracción: {str(e)}"
    
    # Análisis de prioridad básico
    text_l = text.lower()
    priority = "ALTA" if any(k in text_l for k in ['sura', 'sanción', 'multa', 'penalidad']) else "baja"
    clean_text = " ".join(text.split())[:600]
    return clean_text or "Sin texto extraíble.", priority

# --- GESTIÓN DE ESTADO Y MEMORIA ---

def ensure_dirs():
    for d in [STATE_DIR, SITE_TREE_DIR, os.path.join(ROOT, 'raw', 'inbox')]:
        os.makedirs(d, exist_ok=True)

def load_state():
    state = {'seen': {}, 'last_index': 0}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            try:
                data = json.load(f)
                state.update(data)
            except: pass
    
    if not state['seen'] and os.path.exists(CASES_FILE):
        print(f"[{get_time()}] [monitor] Reconstruyendo memoria desde CSV...")
        with open(CASES_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('case_id'): state['seen'][row['case_id']] = {'e': row.get('entidad')}
    return state

def save_state(state):
    with state_lock:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)

# --- PROCESAMIENTO ---

def is_relevant_nav(url):
    u = url.lower()
    if any(x in u for x in ['facebook', 'twitter', 'youtube', 'instagram', 'linkedin', 'mailto:', '#', 'contacto', 'mapa-del-sitio', 'prensa', 'noticias']):
        return False
    keywords = ['norma', 'ley', 'resolu', 'decreto', 'circular', 'concepto', 'juridic', '2024', '2025', '2026', 'documento', 'archivo', 'publicacion']
    return any(k in u for k in keywords)

def process_source(idx, row, state, seen, dynamic_limit):
    start_t = datetime.now()
    entidad = row.get('Entidad', '').strip()
    fuente_url = row.get('Enlace', '').strip()
    if not entidad or not fuente_url: return None
    
    # LOG DE INICIO CON HORA
    print(f'[{get_time()}] 🚀 [monitor] [{idx}] INICIO analizando | "{entidad}"')
    
    site_tree = {}
    queue, visited, found_docs, new_cases = [(fuente_url, 0)], set(), dict(), []
    
    try:
        while queue and not shutdown_flag.is_set():
            # Timeouts de seguridad
            if (datetime.now() - start_t).total_seconds() > MAX_TIME_PER_ENTITY:
                print(f"[{get_time()}]     [{idx}] ⚠️ TIEMPO LÍMITE SUPERADO. Saltando {entidad}.")
                break
            if len(found_docs) >= MAX_DOCS_PER_ENTITY:
                break
            if len(visited) >= dynamic_limit:
                break

            curr_url, depth = queue.pop(0)
            if curr_url in visited: continue
            visited.add(curr_url)

            body, ctype, status, err = fetch(curr_url)
            if status != 'ok':
                if depth == 0:
                    cid = hashlib.sha256(f"{entidad}|{fuente_url}|{curr_url}".encode()).hexdigest()[:16]
                    if cid not in seen:
                        new_cases.append({'case_id': cid, 'detected_at': now_iso(), 'entidad': entidad, 'fuente_url': fuente_url, 'document_url': curr_url, 'status': 'error_fuente', 'link_status': status, 'link_error': err, 'Control SOX': 'NO', 'Emisor': entidad, 'URL': curr_url, 'Fecha registro': now_iso()[:10]})
                continue

            # Extraer links
            txt = body.decode('utf-8', errors='ignore')
            links = URL_RE.findall(txt)
            found_in_page = []
            for u in links:
                abs_u = urljoin(curr_url, u).split('#')[0]
                if DOCS_RE.search(abs_u):
                    if abs_u not in found_docs:
                        found_docs[abs_u] = curr_url
                        found_in_page.append(f"📄 {abs_u}")
                elif depth < MAX_DEPTH and urlparse(curr_url).netloc == urlparse(abs_u).netloc and is_relevant_nav(abs_u):
                    if abs_u not in visited:
                        queue.append((abs_u, depth + 1))
                        found_in_page.append(f"🔗 {abs_u}")
            
            site_tree[curr_url] = found_in_page

        # Procesar documentos encontrados
        docs_to_save = []
        for doc_url, parent_url in found_docs.items():
            if shutdown_flag.is_set(): break
            cid = hashlib.sha256(f"{entidad}|{fuente_url}|{doc_url}".encode()).hexdigest()[:16]
            
            with state_lock:
                if cid in seen: continue
                seen[cid] = {'e': entidad}
            
            # Heurística rápida
            fname = doc_url.split('/')[-1]
            tipo = "Resolución" if 'res' in fname.lower() else "Circular" if 'circ' in fname.lower() else "Documento"
            
            print(f"[{get_time()}]     [{idx}] [doc] bajando: {fname[:30]}...")
            notes, prio = download_and_extract(doc_url, cid)
            
            docs_to_save.append({
                'case_id': cid, 'detected_at': now_iso(), 'entidad': entidad,
                'fuente_url': fuente_url, 'document_url': doc_url, 'status': 'detectado',
                'priority': prio, 'link_status': 'ok', 'notes': notes, 'Emisor': entidad,
                'URL': doc_url, 'Fecha registro': now_iso()[:10], 'Título': fname, 'Tipo de Norma': tipo,
                'Anexos': f"Origen: {parent_url}" if parent_url != fuente_url else ""
            })
            
        if docs_to_save:
            with csv_lock:
                exists = os.path.exists(CASES_FILE)
                with open(CASES_FILE, 'a', encoding='utf-8', newline='') as f:
                    w = csv.DictWriter(f, fieldnames=['case_id', 'Resultado análisis', 'Fecha registro', 'Tipo', 'Título', 'URL', 'Anexos', 'Fecha de publicación', 'Emisor', 'Norma', 'Fecha de divulgación', 'Tipo de Norma', 'Tema', 'Sector Económico', 'Incidencia SURA', 'Obligaciones SURA', 'Norma Importante', 'Control SOX', 'Divulgación SOX', 'Compañía Impactada', 'Obligaciones', 'Persona que analizó', 'Justificación de no divulgación SOX', 'detected_at', 'entidad', 'fuente_url', 'document_url', 'publication_date', 'status', 'priority', 'aplica_sura', 'link_status', 'link_error', 'notes', 'analisis_ia_status', 'analisis_ia_fecha', 'tokens_ia'])
                    if not exists: w.writeheader()
                    for r in docs_to_save: w.writerow({fn: r.get(fn, '') for fn in w.fieldnames})

        # Guardar Site Tree
        if site_tree:
            safe_e = "".join([c if c.isalnum() else "_" for c in entidad])
            with open(os.path.join(SITE_TREE_DIR, f"{datetime.now().strftime('%Y-%m-%d')}_{safe_e}.txt"), 'w') as f:
                f.write(f"ÁRBOL DE NAVEGACIÓN - {entidad}\n\n")
                for p, children in site_tree.items():
                    f.write(f"📂 {p}\n")
                    for c in children: f.write(f"   └── {c}\n")
                    f.write("\n")

        # LOG DE FIN CON HORA
        print(f'[{get_time()}] ✅ [monitor] [{idx}] FIN analizando | "{entidad}" | {len(docs_to_save)} nuevos.')
        return idx
    except Exception as e:
        print(f"[{get_time()}] [error] [{idx}] Falló {entidad}: {e}")
        return None

def main():
    ensure_dirs()
    state = load_state()
    sources = []
    with open(DEFAULT_SOURCES, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        sources = list(reader)
    
    pending = [(i, s) for i, s in enumerate(sources, start=1) if i > state['last_index']]
    if not pending: 
        print("Todo procesado. ¿Reiniciar? (s/n)")
        if input().lower() == 's': pending, state['last_index'] = list(enumerate(sources, start=1)), 0
        else: return

    print(f"🚀 INICIO: {get_time()} | Pendientes: {len(pending)}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(process_source, idx, row, state, state['seen'], 50): idx for idx, row in pending}
        try:
            while futures and not shutdown_flag.is_set():
                done, _ = concurrent.futures.wait(futures, timeout=0.5, return_when=concurrent.futures.FIRST_COMPLETED)
                for f in done:
                    res_idx = f.result()
                    if res_idx:
                        with state_lock:
                            if res_idx > state['last_index']: state['last_index'] = res_idx
                            save_state(state)
                    del futures[f]
        except KeyboardInterrupt:
            shutdown_flag.set()

    print(f"🏁 FIN: {get_time()} | Checkpoint: {state['last_index']}")

if __name__ == '__main__':
    main()
