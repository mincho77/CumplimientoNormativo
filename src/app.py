#!/usr/bin/env python3
"""
Compliance Monitoring Dashboard - Flask App
Reads casos_detectados.csv and tablero_semaforo.csv
"""
import os
import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from urllib.parse import unquote
from flask import Flask, render_template, jsonify, request, send_from_directory, redirect
from flask_cors import CORS
from werkzeug.utils import secure_filename
import subprocess
import hashlib
import re
from urllib.parse import quote

SRC_ROOT = os.path.abspath(os.path.dirname(__file__))
CNORM_ROOT = os.path.abspath(os.path.join(SRC_ROOT, '..'))          # CumplimientoNormativo/
ROOT = CNORM_ROOT                                                   # CumplimientoNormativo/ ← donde escribe el monitor

app = Flask(__name__, 
            template_folder=os.path.join(SRC_ROOT, 'templates'),
            static_folder=os.path.join(SRC_ROOT, 'static'))
app.config['TEMPLATES_AUTO_RELOAD'] = True
CORS(app) # Habilitar CORS para túneles externos
COLOMBIA_TZ = timezone(timedelta(hours=-5))
CASOS_FILE = os.path.join(ROOT, 'data', 'casos_detectados.csv')
SEMAFORO_FILE = os.path.join(ROOT, 'data', 'tablero_semaforo.csv')
SKILLS_ROOT = os.path.join(CNORM_ROOT, '.github', 'skills')
EXTERNAL_SKILLS_ROOTS = [os.path.expanduser('/Users/cmotalvaro/Code/Skills')]
SKILLS_CONFIG_FILE = os.path.join(ROOT, 'data', 'state', 'skills_library_config.json')


def _read_skill_config_state():
    if not os.path.exists(SKILLS_CONFIG_FILE):
        return {}
    try:
        with open(SKILLS_CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def _write_skill_config_state(state):
    os.makedirs(os.path.dirname(SKILLS_CONFIG_FILE), exist_ok=True)
    tmp = SKILLS_CONFIG_FILE + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp, SKILLS_CONFIG_FILE)


def _find_skill_dirs():
    skills = []
    seen = set()
    for root in [*EXTERNAL_SKILLS_ROOTS, SKILLS_ROOT]:
        if not os.path.isdir(root):
            continue
        for dirpath, _, filenames in os.walk(root):
            if 'SKILL.md' in filenames:
                rel = os.path.relpath(dirpath, root).replace(os.sep, '/')
                if rel in seen:
                    continue
                seen.add(rel)
                skills.append((rel, dirpath))
    return sorted(skills, key=lambda x: x[0].lower())


def _parse_skill_markdown(skill_md_path):
    out = {
        'name': '',
        'description': '',
        'overview': '',
        'when_to_use': '',
        'when_not_to_use': '',
        'quick_start': '',
        'raw_markdown': '',
    }
    try:
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        out['raw_markdown'] = content

        frontmatter = ''
        body = content
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                body = parts[2]

        for line in frontmatter.splitlines():
            if ':' not in line:
                continue
            k, v = line.split(':', 1)
            k = k.strip().lower()
            v = v.strip().strip('"').strip("'")
            if k == 'name':
                out['name'] = v
            elif k == 'description':
                out['description'] = v

        sections = {}
        current = None
        acc = []
        for line in body.splitlines():
            if line.startswith('## '):
                if current is not None:
                    sections[current] = '\n'.join(acc).strip()
                current = line[3:].strip().lower()
                acc = []
            else:
                acc.append(line)
        if current is not None:
            sections[current] = '\n'.join(acc).strip()

        out['overview'] = sections.get('overview', '')
        out['when_to_use'] = sections.get('when to use', '')
        out['when_not_to_use'] = sections.get('when not to use', '')
        out['quick_start'] = sections.get('quick start', '')
    except Exception:
        pass
    return out


def _detect_skill_assets(skill_dir, max_items=200):
    assets_dir = os.path.join(skill_dir, 'assets')
    detected = []
    total = 0
    if not os.path.isdir(assets_dir):
        return {'total': 0, 'items': []}

    for dirpath, _, filenames in os.walk(assets_dir):
        for fn in filenames:
            total += 1
            if len(detected) >= max_items:
                continue
            full_path = os.path.join(dirpath, fn)
            rel_path = os.path.relpath(full_path, skill_dir).replace(os.sep, '/')
            ext = os.path.splitext(fn)[1].lower().lstrip('.')
            item_type = 'other'
            if ext in {'svg', 'png', 'jpg', 'jpeg', 'webp', 'gif'}:
                item_type = 'image'
            elif ext in {'woff', 'woff2', 'ttf', 'otf'}:
                item_type = 'font'
            elif ext in {'md', 'txt', 'json', 'yml', 'yaml'}:
                item_type = 'doc'
            detected.append({
                'path': rel_path,
                'type': item_type,
            })

    return {'total': total, 'items': detected}


def _default_skill_config(skill_id, assets_detected):
    return {
        'category': 'general',
        'owner': '',
        'status': 'active',
        'tags': [],
        'priority': 3,
        'entries': [
            {
                'name': 'request',
                'type': 'text',
                'required': True,
                'description': 'Peticion inicial del usuario.'
            }
        ],
        'outputs': [
            {
                'name': 'resultado',
                'format': 'markdown',
                'description': 'Respuesta final del skill.'
            }
        ],
        'assets': [
            {
                'path': it.get('path', ''),
                'type': it.get('type', 'other'),
                'role': '',
                'enabled': True,
            }
            for it in assets_detected[:25]
        ],
        'notes': '',
        'organization': {
            'folder': skill_id,
            'display_order': 0,
        }
    }


def _get_skill_by_id(skill_id):
    if not skill_id:
        return None
    for root in [*EXTERNAL_SKILLS_ROOTS, SKILLS_ROOT]:
        target = os.path.normpath(os.path.join(root, skill_id))
        if not target.startswith(os.path.normpath(root)):
            continue
        md = os.path.join(target, 'SKILL.md')
        if os.path.isfile(md):
            return target
    return None

def clean_filename(url, entidad):
    """Decodes URL, removes extension, and removes redundant entity name."""
    if not url:
        return ""
    filename = unquote(url.split('/')[-1])
    
    # Remove extension
    if '.' in filename:
        filename = '.'.join(filename.split('.')[:-1])
        
    # Remove entity name from filename if it's there (case insensitive)
    if entidad:
        ent_clean = entidad.lower().replace('ministerio de ', '').replace('superintendencia de ', '').strip()
        filename = filename.replace(entidad, '').replace(ent_clean, '')
    
    # Clean up multiple spaces, dashes or underscores
    filename = filename.replace('_', ' ').replace('-', ' ').strip()
    return filename

def get_extension(url):
    """Extracts extension from URL and returns it in uppercase."""
    if not url or '.' not in url:
        return "FILE"
    ext = url.split('.')[-1].split('?')[0].upper()
    return ext

@app.context_processor
def utility_processor():
    return dict(unquote=unquote, clean_filename=clean_filename, get_extension=get_extension)

def read_csv(filepath):
    """Read CSV and return list of dicts."""
    if not os.path.exists(filepath):
        return []
    rows = []
    with open(filepath, 'r', encoding='utf-8', newline='') as f:
        # Pre-procesar para eliminar caracteres NUL que corrompen el lector
        clean_lines = (line.replace('\0', '') for line in f)
        reader = csv.DictReader(clean_lines)
        for row in reader:
            rows.append(row)
    return rows


def get_summary():
    """Get count summary by semaforo, total tokens, and new cases today."""
    casos = read_csv(SEMAFORO_FILE)
    summary = {'ROJO': 0, 'AMARILLO': 0, 'VERDE': 0, 'CONSOLIDADO': 0, 'NUEVOS_HOY': 0, 'TOTAL_TOKENS': 0}
    
    today_str = datetime.now(COLOMBIA_TZ).strftime('%Y-%m-%d')
    
    for caso in casos:
        semaforo = caso.get('semaforo', '').upper()
        if semaforo in summary:
            summary[semaforo] += 1
            
        detected_at = caso.get('detected_at', '')
        if detected_at.startswith(today_str):
            summary['NUEVOS_HOY'] += 1
        
        # Sumar tokens (asumiendo que están en casos_detectados pero cargamos tablero_semaforo)
        # Para mayor precisión, leemos casos_detectados para los tokens
    
    casos_raw = read_csv(CASOS_FILE)
    def parse_tokens(val):
        try:
            return int(float(val or 0))
        except (ValueError, TypeError):
            return 0
            
    total_tokens = sum(parse_tokens(c.get('tokens_ia')) for c in casos_raw)
    summary['TOTAL_TOKENS'] = total_tokens
    
    return summary


def get_casos_by_filter(semaforo=None, entidad=None, priority=None, link_status=None, search=None, date=None):
    """Filter casos by criteria."""
    casos = read_csv(SEMAFORO_FILE)
    filtered = []

    for caso in casos:
        if semaforo and caso.get('semaforo', '').upper() != semaforo.upper():
            continue
        if entidad and caso.get('entidad') != entidad:
            continue
        if priority and caso.get('priority') != priority:
            continue
        if link_status and caso.get('link_status') != link_status:
            continue
        if date:
            val = caso.get('detected_at') or ''
            if val[:10] != date:
                continue
        if search:
            search_lower = search.lower()
            searchable = f"{caso.get('entidad', '')} {caso.get('motivo', '')} {caso.get('notes', '')}".lower()
            if search_lower not in searchable:
                continue
        filtered.append(caso)

    return filtered


def get_entities():
    """Get unique entities."""
    casos = read_csv(SEMAFORO_FILE)
    entities = sorted(set(c.get('entidad', '') for c in casos if c.get('entidad')))
    return entities


def get_priorities():
    """Get unique priorities."""
    casos = read_csv(SEMAFORO_FILE)
    priorities = sorted(set(c.get('priority', '') for c in casos if c.get('priority')))
    return [p for p in priorities if p]


def get_link_statuses():
    """Get unique link statuses."""
    casos = read_csv(SEMAFORO_FILE)
    statuses = sorted(set(c.get('link_status', '') for c in casos if c.get('link_status')))
    return [s for s in statuses if s]


import re

@app.route('/status')
def system_status():
    """Route to view the uptime/status of all monitored sources."""
    log_file = os.path.join(ROOT, 'wiki', 'operations', 'diagnostico_final.log')
    fuentes_file = os.path.join(ROOT, 'data', 'Fuentes Normativas - limpio utf8 v2.csv')
    
    # 1. Cargar todas las fuentes como base
    sites = {}
    if os.path.exists(fuentes_file):
        with open(fuentes_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                entidad = row.get('Entidad', '').strip()
                enlace = row.get('Enlace', '').strip()
                if entidad:
                    sites[entidad] = {
                        'url': enlace,
                        'status': 'UNKNOWN',
                        'last_check': '-',
                        'message': 'No se ha monitoreado aún.'
                    }

    # 2. Parsear el log para actualizar el estado
    if os.path.exists(log_file):
        last_check_date = datetime.fromtimestamp(os.path.getmtime(log_file)).strftime('%Y-%m-%d %H:%M')
        with open(log_file, 'r', encoding='utf-8') as f:
            log_content = f.read()
            
            # Buscar inicios de scrapeo
            starts = re.findall(r'\[START\] \[\d+\] (.*?) ->', log_content)
            for s in starts:
                if s in sites:
                    sites[s]['status'] = 'UP'
                    sites[s]['last_check'] = last_check_date
                    sites[s]['message'] = 'Operando correctamente.'
            
            # Buscar fallos principales (errores al intentar acceder a la fuente raíz)
            # El log dice: [08:13:49] [11] ❌ FETCH FAIL en http://www.urf.gov.co...
            fails = re.findall(r'\[\d+\] ❌ FETCH FAIL en (.*?):', log_content)
            for fail_url in fails:
                fail_url_clean = fail_url.strip()
                for ent, data in sites.items():
                    # Solo marcar DOWN si el fallo es exactamente en la URL semilla
                    if fail_url_clean == data['url'].strip():
                        data['status'] = 'DOWN'
                        data['message'] = 'Servidor inalcanzable (Error 50x/40x o Bloqueo al intentar conectar a la fuente principal).'
                        
    sorted_sites = sorted(sites.items(), key=lambda x: (x[1]['status'] != 'DOWN', x[0]))
    down_count = sum(1 for s in sites.values() if s['status'] == 'DOWN')
    
    return render_template('status.html', sites=sorted_sites, total=len(sites), down=down_count)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'sura-logo.svg', mimetype='image/svg+xml')

@app.route('/')
def index():
    summary = get_summary()
    entities = get_entities()
    priorities = get_priorities()
    link_statuses = get_link_statuses()
    return render_template('index.html',
                         summary=summary,
                         entities=entities,
                         priorities=priorities,
                         link_statuses=link_statuses)


@app.route('/detalle')
def detalle():
    fuente = request.args.get('fuente')
    entidad = request.args.get('entidad')
    casos = read_csv(SEMAFORO_FILE)
    
    # Filtrar documentos
    if fuente and fuente != "Sin Fuente" and fuente != "nan":
        documentos = [c for c in casos if c.get('fuente_url') == fuente]
    else:
        # Fallback para casos de Excel importados que no tienen fuente_url
        documentos = [c for c in casos if c.get('entidad') == entidad]
        fuente = "Reporte Manual (Excel)"

    # Escanear análisis en wiki para asociarlos por archivo/fuente original
    wiki_dir = os.path.join(ROOT, "wiki", "analyses")
    analysis_files = {}
    if os.path.exists(wiki_dir):
        for f in os.listdir(wiki_dir):
            if f.endswith('.md') and not f.startswith('.'):
                try:
                    fpath = os.path.join(wiki_dir, f)
                    with open(fpath, 'r', encoding='utf-8') as wf:
                        content = wf.read()
                        # Parsear metadatos frontmatter rudimentario
                        if content.startswith('---'):
                            parts = content.split('---', 2)
                            if len(parts) >= 3:
                                frontmatter = parts[1]
                                # Extraer source_files: ["..."]
                                sf_match = re.search(r'source_files:\s*\["(.*?)"\]', frontmatter)
                                if sf_match:
                                    sf = sf_match.group(1)
                                    # Guardar mapeo de fuente -> nombre de archivo wiki
                                    if sf:
                                        analysis_files[sf] = f
                except Exception:
                    pass

    for d in documentos:
        doc_url = d.get('document_url', '')
        fuente_url = d.get('fuente_url', '')
        # Asignar archivo wiki si coincide con la URL del documento o con la fuente
        match_wiki = None
        for k, v in analysis_files.items():
            if k == doc_url or k == fuente_url or (doc_url and doc_url.endswith(k)) or (fuente_url and fuente_url.endswith(k)):
                match_wiki = v
                break
        d['wiki_analysis_file'] = match_wiki

    return render_template('detalle.html', 
                         fuente=fuente, 
                         entidad=entidad, 
                         documentos=documentos)

@app.route('/analytics')
def analytics():
    """Route for the analytics and charts page."""
    return render_template('analytics.html')

@app.route('/analytics_tokens')
def analytics_tokens():
    """Route for the dedicated tokens analytics page."""
    return render_template('analytics_tokens.html')


@app.route('/analytics_excel')
def analytics_excel():
    """Route to view statistics from the manual tracking Excel file."""
    stats_file = os.path.join(ROOT, 'data', 'stats', 'excel_stats.json')
    stats = {}
    if os.path.exists(stats_file):
        with open(stats_file, 'r', encoding='utf-8') as f:
            stats = json.load(f)
    
    metadata_file = os.path.join(ROOT, 'data', 'stats', 'excel_metadata.json')
    metadata = {}
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
            
    return render_template('analytics_excel.html', stats=stats, metadata=metadata)

def is_case_error(c):
    """Define si un caso es un error de conexión o de descarga."""
    return (c.get('link_status') and c.get('link_status') != 'ok') or c.get('priority') == 'error'

def categorize_error(c):
    """Categoriza de forma humana un error basado en status y notas."""
    status = (c.get('link_status') or '').lower()
    notes = (c.get('notes') or '').lower()
    
    if '404' in status or '404' in notes: return '404 Not Found'
    if 'timeout' in status or 'timeout' in notes: return 'Timeout / Servidor Lento'
    if '403' in status or '403' in notes: return 'Acceso Denegado (403)'
    if 'ssl' in status or 'ssl' in notes or 'tlsv1' in notes: return 'SSL / Seguridad'
    if 'nodename' in notes or 'name not known' in notes: return 'DNS / Red Inexistente'
    if 'errno 2' in notes or 'directory' in notes: return 'Sistema (Ruta no encontrada)'
    if 'error_fuente' in c.get('status', ''): return 'Semilla No Carga'
    
    return 'Otros Errores'

@app.route('/errores')
def errores():
    """Route to view link errors with granular advanced filtering."""
    casos = read_csv(CASOS_FILE)
    
    f_date = request.args.get('date')
    f_entidad = request.args.get('entidad')
    f_tipo = request.args.get('tipo')
    f_estado = request.args.get('estado', 'pendientes')

    errores_raw = []
    all_error_types = set()

    for c in casos:
        if not is_case_error(c): continue
        
        cat = categorize_error(c)
        all_error_types.add(cat)
        
        # Filtro de Estado
        status = c.get('status')
        if f_estado == 'pendientes' and status == 'error_gestionado': continue
        if f_estado == 'gestionados' and status != 'error_gestionado': continue
        
        # Filtro de Fecha
        if f_date and f_date not in c.get('detected_at', ''): continue
        
        # Filtro de Entidad (Flexible)
        if f_entidad:
            target = f_entidad.strip().lower()
            current = (c.get('entidad') or '').strip().lower()
            if target != current: continue
        
        # Filtro de Tipo
        if f_tipo and f_tipo != cat: continue
            
        c['error_category'] = cat
        errores_raw.append(c)
    
    entities = sorted(list(set(c.get('entidad') for c in casos if (c.get('link_status') and c.get('link_status') != 'ok') or c.get('priority') == 'error')))
    error_types_list = sorted(list(all_error_types))

    from collections import defaultdict
    errores_grouped = defaultdict(list)
    for err in errores_raw:
        errores_grouped[err['entidad']].append(err)
    
    errores_grouped = dict(sorted(errores_grouped.items()))
    
    propuestas = {
        '404 Not Found': 'La URL del documento es inválida o fue eliminada.',
        'Timeout / Servidor Lento': 'El sitio está saturado o es muy lento. Reintentar luego.',
        'Acceso Denegado (403)': 'El sitio bloquea al bot (WAF). Requiere revisión manual.',
        'SSL / Seguridad': 'Problema de certificados. Se requiere bypass manual en script.',
        'DNS / Red Inexistente': 'La entidad cambió su dominio o no tiene internet.',
        'Sistema (Ruta no encontrada)': 'Error local del bot al crear carpetas.',
        'Semilla No Carga': 'La página principal del regulador no responde.',
        'Otros Errores': 'Error no clasificado. Revisar detalle técnico.'
    }
    
    return render_template('errores.html', 
                         errores_grouped=errores_grouped, 
                         propuestas=propuestas,
                         entities=entities,
                         error_types=error_types_list,
                         filters={
                             'date': f_date,
                             'entidad': f_entidad,
                             'tipo': f_tipo,
                             'estado': f_estado
                         })


def classify_legal_risk(caso):
    """Categorize a compliance case and assess its legal risk as a legal specialist."""
    entidad = (caso.get('entidad') or '').upper()
    notes = (caso.get('notes') or '').lower()
    motivo = (caso.get('motivo') or '').lower()
    
    # default classification
    category = "OPERATIVO"
    label = "Riesgo Operativo y de Datos"
    icon = "alertaCirculo"
    color = "#888B8D"  # Grey Sura
    bg_color = "#F8F8F8"  # digital bg
    border_color = "#888B8D20"
    
    if "DIAN" in entidad or "TRIBUT" in notes or "IMPUEST" in notes or "ADUANA" in notes:
        category = "TRIBUTARIO"
        label = "Riesgo Tributario y Fiscal"
        icon = "moneda"
        color = "#067014"  # Green Sura success alert style
        bg_color = "#DEF6DE"
        border_color = "#06701420"
    elif "FINANCIERA" in entidad or "SFC" in entidad or "SUPERINTENDENCIA FINANCIERA" in entidad or "BANCO DE LA" in entidad or "CAMBIAR" in notes or "SARLAFT" in notes or "MONEDA" in notes:
        category = "FINANCIERO"
        label = "Riesgo Financiero y SARLAFT"
        icon = "brujula"
        color = "#0033A0"  # Sura Secondary Blue
        bg_color = "#DFEAFF"
        border_color = "#0033A020"
    elif "SOCIEDADES" in entidad or "SUPERSOCIEDADES" in entidad or "ASAMBLEA" in notes or "CORPORATIV" in notes or "ESTATUT" in notes or "SOCIO" in notes:
        category = "CORPORATIVO"
        label = "Riesgo Corporativo y Societario"
        icon = "avantDerecha"
        color = "#2D6DF6"  # Sura Primary Blue
        bg_color = "#E5E9EA"
        border_color = "#2D6DF620"
    elif "PROCURADUR" in entidad or "CONTRALOR" in entidad or "AUDITOR" in entidad or "FISCAL" in notes or "DISCIPLIN" in notes or "SANCIO" in notes:
        category = "ADMINISTRATIVO"
        label = "Riesgo Administrativo y Control"
        icon = "senal"
        color = "#D12D35"  # Red Sura alert style
        bg_color = "#FFF4F3"
        border_color = "#D12D3520"
    elif "AMV" in entidad or "VALOR" in notes or "MERCAD" in notes or "ACCION" in notes or "BOLSA" in notes:
        category = "MERCADO"
        label = "Riesgo de Mercado e Inversión"
        icon = "bandera"
        color = "#ED8B00"  # Orange Sura warning style
        bg_color = "#FFF5EC"
        border_color = "#ED8B0020"
        
    return category, label, icon, color, bg_color, border_color

def get_risk_meta(category):
    meta = {
        "TRIBUTARIO": {
            "relation": "Vínculo directo entre reformas fiscales, plazos de declaración y obligaciones de reporte ante la DIAN.",
            "risk": "Afecta el flujo de caja y genera riesgo de sanciones e intereses de mora para Seguros SURA y sus filiales por reporte extemporáneo."
        },
        "FINANCIERO": {
            "relation": "Interconexión de directrices del Banco de la República sobre régimen cambiario y circulares de la Superfinanciera sobre solvencia y lavado de activos.",
            "risk": "Riesgo de descalce cambiario, penalizaciones por infracciones cambiarias y requerimientos adicionales de capital para Seguros SURA y SURA Asset Management."
        },
        "CORPORATIVO": {
            "relation": "Disposiciones de la Supersociedades sobre informes de gestión, actas de asamblea y registro de libros.",
            "risk": "Riesgo de inoponibilidad de decisiones societarias, multas a administradores y fallas en el cumplimiento del gobierno corporativo."
        },
        "ADMINISTRATIVO": {
            "relation": "Normativa disciplinaria y de control fiscal aplicable a contratos con entidades del Estado y licitaciones públicas.",
            "risk": "Pérdida de capacidad para contratar con el Estado (EPS SURA y Seguros SURA) y sanciones administrativas por incumplimientos en la gestión de recursos públicos."
        },
        "MERCADO": {
            "relation": "Directrices de la AMV y Superfinanciera sobre conducta en el mercado de valores y negociación de portafolios.",
            "risk": "Riesgo reputacional y de suspensión de licencias para operadores de fondos e inversiones en SURA Asset Management."
        },
        "OPERATIVO": {
            "relation": "Disposiciones sobre tratamiento de datos personales, seguridad de la información y archivo documental.",
            "risk": "Sanciones de la SIC por vulneración de la Ley 1581 de 2012 y fallas operativas en la custodia de datos de clientes."
        }
    }
    return meta.get(category, meta["OPERATIVO"])

@app.route('/mapa-riesgos')
def mapa_riesgos():
    """Render the mind map page."""
    return render_template('mapa_riesgos.html')


@app.route('/mapa-riesgos-termico')
def mapa_riesgos_termico():
    return render_template('mapa_riesgos_termico.html')


@app.route('/mapa_riesgos')
def mapa_riesgos_legacy():
    return redirect('/mapa-riesgos-termico', code=302)


def _yes(value):
    return (value or '').strip().upper() in {'SI', 'SÍ', 'YES', 'TRUE', '1'}


def _parse_date(value):
    value = (value or '').strip()
    if not value:
        return None
    for fmt in ('%Y-%m-%d', '%Y-%m-%d %H:%M:%S%z', '%d/%m/%Y'):
        try:
            return datetime.strptime(value[:10] if fmt == '%Y-%m-%d' else value, fmt).date()
        except ValueError:
            continue
    return None


def _risk_impact(caso):
    semaforo = (caso.get('semaforo') or '').strip().upper()
    resultado = (caso.get('Resultado análisis') or '').strip().lower()
    motivo = (caso.get('motivo') or '').strip().lower()
    impact = {'ROJO': 5, 'AMARILLO': 3, 'CONSOLIDADO': 2, 'VERDE': 1}.get(semaforo, 2)

    if 'divulgar' in resultado and 'no divulgar' not in resultado:
        impact = max(impact, 4)
    if _yes(caso.get('Incidencia SURA')) or _yes(caso.get('Obligaciones SURA')):
        impact = min(5, impact + 1)
    if _yes(caso.get('Control SOX')) or 'sox' in motivo:
        impact = 5
    if 'riesgo alto' in motivo or 'riesgo crítico' in motivo or 'riesgo critico' in motivo:
        impact = 5
    return max(1, min(5, impact))


def _risk_probability(caso):
    status = (caso.get('status') or '').strip().lower()
    semaforo = (caso.get('semaforo') or '').strip().upper()
    probability = {
        'detectado': 4,
        'extraido_ia': 4,
        'en_validacion': 4,
        'importado_excel': 3,
        'validado': 3,
        'consolidado': 2,
        'rechazado': 1,
    }.get(status, 3 if semaforo in {'ROJO', 'AMARILLO'} else 2)

    if semaforo == 'ROJO':
        probability = max(probability, 4)
    elif semaforo == 'AMARILLO':
        probability = max(probability, 3)

    today = datetime.now(COLOMBIA_TZ).date()
    detected = _parse_date(caso.get('detected_at'))
    disclosure = _parse_date(caso.get('Fecha de divulgación'))
    if detected and (today - detected).days <= 7:
        probability = min(5, probability + 1)
    if disclosure:
        days_to_disclosure = (disclosure - today).days
        if days_to_disclosure < 0:
            probability = 5
        elif days_to_disclosure <= 7:
            probability = max(probability, 4)

    return max(1, min(5, probability))


def _normalize_rel_text(value):
    text = (value or '').lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def _extract_norma_key(norma_value):
    norma_txt = _normalize_rel_text(norma_value)
    if not norma_txt:
        return ''
    match = re.search(r'(decreto|resolucion|resolucion externa|circular|ley|acuerdo)\s+([a-z0-9-]{2,})', norma_txt)
    if match:
        return f"{match.group(1)} {match.group(2)}"
    return ''


def _extract_keywords(caso, max_keywords=8):
    txt = ' '.join([
        caso.get('Titulo') or caso.get('Título') or '',
        caso.get('Norma') or '',
        caso.get('Tema') or '',
        caso.get('Obligaciones') or '',
        caso.get('motivo') or '',
    ])
    norm = _normalize_rel_text(txt)
    if not norm:
        return []

    stop_words = {
        'para', 'como', 'sobre', 'entre', 'desde', 'hasta', 'esta', 'este', 'estas', 'estos',
        'norma', 'normativo', 'normativa', 'documento', 'cumplimiento', 'obligacion', 'obligaciones',
        'decreto', 'resolucion', 'circular', 'ley', 'acuerdo', 'articulo', 'capitulo', 'titulo',
        'sura', 'colombia', 'analisis', 'integrado', 'matriz', 'riesgo', 'riesgos', 'control',
    }

    counts = Counter()
    for token in norm.split(' '):
        if len(token) < 5:
            continue
        if token.isdigit():
            continue
        if token in stop_words:
            continue
        counts[token] += 1

    return [tok for tok, _ in counts.most_common(max_keywords)]


def _doc_id(caso, index):
    base = '|'.join([
        caso.get('case_id') or '',
        caso.get('document_url') or caso.get('fuente_url') or '',
        caso.get('Titulo') or caso.get('Título') or caso.get('Norma') or '',
        caso.get('entidad') or caso.get('Emisor') or '',
        caso.get('detected_at') or '',
        str(index),
    ])
    return hashlib.sha1(base.encode('utf-8')).hexdigest()[:12]


def _build_doc_entry(caso, index):
    semaforo = (caso.get('semaforo') or 'SIN').strip().upper()
    entidad = (caso.get('entidad') or caso.get('Emisor') or 'Sin entidad').strip()
    title = (caso.get('Titulo') or caso.get('Título') or caso.get('Norma') or caso.get('motivo') or 'Sin titulo').strip()
    tema = (caso.get('Tema') or '').strip()
    tipo = (caso.get('Tipo de Norma') or caso.get('Tipo') or '').strip()
    detected_at = (caso.get('detected_at') or '')[:10]

    sem_weight = {'ROJO': 5, 'AMARILLO': 4, 'CONSOLIDADO': 3, 'VERDE': 2}.get(semaforo, 1)
    urgency = sem_weight
    if _yes(caso.get('Incidencia SURA')) or _yes(caso.get('Obligaciones SURA')):
        urgency += 1

    return {
        'id': _doc_id(caso, index),
        'title': title,
        'entidad': entidad,
        'entidad_key': _normalize_rel_text(entidad),
        'tema': tema,
        'tema_key': _normalize_rel_text(tema),
        'tipo_norma': tipo,
        'tipo_key': _normalize_rel_text(tipo),
        'norma_key': _extract_norma_key(caso.get('Norma') or ''),
        'keywords': _extract_keywords(caso),
        'semaforo': semaforo,
        'detected_at': detected_at,
        'document_url': (caso.get('document_url') or caso.get('fuente_url') or '#').strip(),
        'urgency': urgency,
    }


def _pairwise(group):
    for i in range(len(group)):
        for j in range(i + 1, len(group)):
            yield group[i], group[j]


def _edge_key(a_id, b_id):
    return (a_id, b_id) if a_id < b_id else (b_id, a_id)


REL_WEIGHTS = {
    'same_entity': 30,
    'same_tema': 22,
    'same_tipo': 14,
    'same_norma_ref': 35,
    'shared_keyword': 8,
}

REL_REASON_LABELS = {
    'same_entity': 'Misma entidad emisora',
    'same_tema': 'Mismo tema regulatorio',
    'same_tipo': 'Mismo tipo de norma',
    'same_norma_ref': 'Referencia normativa muy similar',
    'shared_keyword': 'Coincidencia de palabras clave',
}


def _score_doc_relation(doc_a, doc_b):
    score = 0
    reasons = []

    if doc_a.get('entidad_key') and doc_a.get('entidad_key') == doc_b.get('entidad_key'):
        score += REL_WEIGHTS['same_entity']
        reasons.append(REL_REASON_LABELS['same_entity'])

    if doc_a.get('tema_key') and doc_a.get('tema_key') == doc_b.get('tema_key'):
        score += REL_WEIGHTS['same_tema']
        reasons.append(REL_REASON_LABELS['same_tema'])

    if doc_a.get('tipo_key') and doc_a.get('tipo_key') == doc_b.get('tipo_key'):
        score += REL_WEIGHTS['same_tipo']
        reasons.append(REL_REASON_LABELS['same_tipo'])

    if doc_a.get('norma_key') and doc_a.get('norma_key') == doc_b.get('norma_key'):
        score += REL_WEIGHTS['same_norma_ref']
        reasons.append(REL_REASON_LABELS['same_norma_ref'])

    shared_keywords = sorted(set(doc_a.get('keywords') or []).intersection(set(doc_b.get('keywords') or [])))
    if shared_keywords:
        score += REL_WEIGHTS['shared_keyword']
        reasons.append(REL_REASON_LABELS['shared_keyword'])
        reasons.append('Keywords: ' + ', '.join(shared_keywords[:5]))

    return {
        'score': score,
        'reasons': reasons,
        'cross_entity': (doc_a.get('entidad') or '') != (doc_b.get('entidad') or ''),
    }


@app.route('/grafo-relaciones')
def grafo_relaciones_page():
    return render_template('grafo_relaciones.html')


@app.route('/api/mapa-riesgos-termico')
def api_mapa_riesgos_termico():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    category = request.args.get('category')

    cells = {
        f'{impact}-{probability}': {
            'impact': impact,
            'probability': probability,
            'count': 0,
            'score': impact * probability,
            'cases': []
        }
        for impact in range(1, 6)
        for probability in range(1, 6)
    }

    total_cases = 0
    critical_cases = 0
    categories = Counter()

    for caso in read_csv(SEMAFORO_FILE):
        det_date = (caso.get('detected_at') or '')[:10]
        if (start_date or end_date) and not det_date:
            continue
        if start_date and det_date < start_date:
            continue
        if end_date and det_date > end_date:
            continue

        cat_key, cat_label, _, _, _, _ = classify_legal_risk(caso)
        if category and cat_key != category:
            continue

        impact = _risk_impact(caso)
        probability = _risk_probability(caso)
        score = impact * probability
        cell = cells[f'{impact}-{probability}']
        cell['count'] += 1
        total_cases += 1
        categories[cat_label] += 1
        if score >= 16:
            critical_cases += 1

        if len(cell['cases']) < 8:
            cell['cases'].append({
                'score': score,
                'entidad': caso.get('entidad') or caso.get('Emisor') or 'Sin entidad',
                'title': caso.get('Título') or caso.get('Norma') or caso.get('motivo') or 'Sin título',
                'semaforo': caso.get('semaforo') or '',
                'detected_at': det_date,
                'document_url': caso.get('document_url') or caso.get('URL') or '#',
                'category': cat_label
            })

    hottest = sorted(cells.values(), key=lambda cell: (cell['count'] > 0, cell['score'], cell['count']), reverse=True)[:5]
    return jsonify({
        'start_date': start_date or 'Mínima',
        'end_date': end_date or 'Máxima',
        'total_cases': total_cases,
        'critical_cases': critical_cases,
        'cells': list(cells.values()),
        'hottest': hottest,
        'categories': [{'name': name, 'count': count} for name, count in categories.most_common()]
    })


@app.route('/api/grafo-relaciones')
def api_grafo_relaciones():
    start_date = (request.args.get('start_date') or '').strip()
    end_date = (request.args.get('end_date') or '').strip()
    semaforo_filter = (request.args.get('semaforo') or '').strip().upper()
    entidad_filter = _normalize_rel_text(request.args.get('entidad') or '')

    try:
        max_nodes = int(request.args.get('max_nodes', 120))
    except ValueError:
        max_nodes = 120
    max_nodes = max(30, min(250, max_nodes))

    try:
        min_score = int(request.args.get('min_score', 35))
    except ValueError:
        min_score = 35
    min_score = max(10, min(100, min_score))

    docs = []
    for idx, caso in enumerate(read_csv(SEMAFORO_FILE)):
        det_date = (caso.get('detected_at') or '')[:10]
        if (start_date or end_date) and not det_date:
            continue
        if start_date and det_date < start_date:
            continue
        if end_date and det_date > end_date:
            continue
        if semaforo_filter and (caso.get('semaforo') or '').strip().upper() != semaforo_filter:
            continue

        entidad_raw = (caso.get('entidad') or caso.get('Emisor') or '').strip()
        if entidad_filter and entidad_filter not in _normalize_rel_text(entidad_raw):
            continue

        docs.append(_build_doc_entry(caso, idx))

    docs.sort(key=lambda d: (d['urgency'], d['detected_at']), reverse=True)
    docs = docs[:max_nodes]

    nodes = {
        doc['id']: {
            'id': doc['id'],
            'label': doc['title'][:92],
            'title': doc['title'],
            'entidad': doc['entidad'],
            'tema': doc['tema'],
            'tipo_norma': doc['tipo_norma'],
            'semaforo': doc['semaforo'],
            'detected_at': doc['detected_at'],
            'document_url': doc['document_url'],
            'urgency': doc['urgency'],
            'degree': 0,
        }
        for doc in docs
    }

    buckets = {
        'same_entity': defaultdict(list),
        'same_tema': defaultdict(list),
        'same_tipo': defaultdict(list),
        'same_norma_ref': defaultdict(list),
        'shared_keyword': defaultdict(list),
    }

    for doc in docs:
        if doc['entidad_key']:
            buckets['same_entity'][doc['entidad_key']].append(doc['id'])
        if doc['tema_key']:
            buckets['same_tema'][doc['tema_key']].append(doc['id'])
        if doc['tipo_key']:
            buckets['same_tipo'][doc['tipo_key']].append(doc['id'])
        if doc['norma_key']:
            buckets['same_norma_ref'][doc['norma_key']].append(doc['id'])
        for kw in doc['keywords']:
            buckets['shared_keyword'][kw].append(doc['id'])

    weights = REL_WEIGHTS

    max_bucket = {
        'same_entity': 45,
        'same_tema': 35,
        'same_tipo': 35,
        'same_norma_ref': 35,
        'shared_keyword': 25,
    }

    reasons_label = REL_REASON_LABELS

    edges = {}
    for relation_type, bucket_map in buckets.items():
        for shared_value, ids in bucket_map.items():
            unique_ids = list(dict.fromkeys(ids))
            if len(unique_ids) < 2:
                continue
            if len(unique_ids) > max_bucket[relation_type]:
                continue

            for left, right in _pairwise(unique_ids):
                key = _edge_key(left, right)
                edge = edges.setdefault(key, {
                    'source': key[0],
                    'target': key[1],
                    'score': 0,
                    'reason_types': set(),
                    'shared_keywords': set(),
                })
                edge['score'] += weights[relation_type]
                edge['reason_types'].add(reasons_label[relation_type])
                if relation_type == 'shared_keyword' and len(edge['shared_keywords']) < 5:
                    edge['shared_keywords'].add(shared_value)

    edge_list = []
    for _, edge in edges.items():
        if edge['score'] < min_score:
            continue
        source_entity = nodes[edge['source']]['entidad']
        target_entity = nodes[edge['target']]['entidad']
        cross_entity = source_entity != target_entity
        nodes[edge['source']]['degree'] += 1
        nodes[edge['target']]['degree'] += 1
        reasons = sorted(edge['reason_types'])
        if edge['shared_keywords']:
            reasons.append('Keywords: ' + ', '.join(sorted(edge['shared_keywords'])))
        edge_list.append({
            'source': edge['source'],
            'target': edge['target'],
            'score': edge['score'],
            'width': max(1.5, min(8.0, edge['score'] / 14.0)),
            'reasons': reasons,
            'cross_entity': cross_entity,
            'source_entity': source_entity,
            'target_entity': target_entity,
        })

    node_list = sorted(nodes.values(), key=lambda n: (n['degree'], n['urgency']), reverse=True)
    if edge_list:
        connected_ids = {e['source'] for e in edge_list} | {e['target'] for e in edge_list}
        node_list = [n for n in node_list if n['id'] in connected_ids]

    edge_list.sort(key=lambda e: e['score'], reverse=True)

    entity_edges = {}
    for edge in edge_list:
        if not edge['cross_entity']:
            continue
        pair = _edge_key(edge['source_entity'], edge['target_entity'])
        entity_edge = entity_edges.setdefault(pair, {
            'source_entity': pair[0],
            'target_entity': pair[1],
            'score': 0,
            'count': 0,
            'reasons': Counter(),
        })
        entity_edge['score'] += edge['score']
        entity_edge['count'] += 1
        for reason in edge['reasons']:
            entity_edge['reasons'][reason] += 1

    entity_edge_list = []
    for entity_edge in entity_edges.values():
        reason_items = [name for name, _ in entity_edge['reasons'].most_common(3)]
        entity_edge_list.append({
            'source_entity': entity_edge['source_entity'],
            'target_entity': entity_edge['target_entity'],
            'score': entity_edge['score'],
            'count': entity_edge['count'],
            'reasons': reason_items,
        })
    entity_edge_list.sort(key=lambda e: (e['score'], e['count']), reverse=True)

    return jsonify({
        'start_date': start_date or 'Minima',
        'end_date': end_date or 'Maxima',
        'total_filtered_docs': len(docs),
        'total_nodes': len(node_list),
        'total_edges': len(edge_list),
        'total_entity_edges': len(entity_edge_list),
        'min_score': min_score,
        'nodes': node_list,
        'edges': edge_list,
        'entity_edges': entity_edge_list,
        'top_edges': edge_list[:12],
        'top_entity_edges': entity_edge_list[:12],
    })


@app.route('/api/grafo-relaciones-historico')
def api_grafo_relaciones_historico():
    doc_id = (request.args.get('doc_id') or '').strip()
    if not doc_id:
        return jsonify({'error': 'doc_id es requerido'}), 400

    before_only = (request.args.get('before_only') or '1').strip() not in ('0', 'false', 'False')

    try:
        max_related = int(request.args.get('max_related', 10))
    except ValueError:
        max_related = 10
    max_related = max(3, min(30, max_related))

    try:
        min_score = int(request.args.get('min_score', 28))
    except ValueError:
        min_score = 28
    min_score = max(10, min(100, min_score))

    all_docs = []
    for idx, caso in enumerate(read_csv(SEMAFORO_FILE)):
        all_docs.append(_build_doc_entry(caso, idx))

    docs_by_id = {d['id']: d for d in all_docs}
    seed = docs_by_id.get(doc_id)
    if not seed:
        return jsonify({'error': 'Documento no encontrado'}), 404

    related = []
    seed_date = seed.get('detected_at') or ''

    for candidate in all_docs:
        if candidate['id'] == seed['id']:
            continue

        cand_date = candidate.get('detected_at') or ''
        if before_only and seed_date and cand_date and cand_date >= seed_date:
            continue

        rel = _score_doc_relation(seed, candidate)
        if rel['score'] < min_score:
            continue

        days_diff = None
        if seed_date and cand_date:
            try:
                d_seed = datetime.strptime(seed_date, '%Y-%m-%d')
                d_cand = datetime.strptime(cand_date, '%Y-%m-%d')
                days_diff = (d_seed - d_cand).days
            except ValueError:
                days_diff = None

        related.append({
            'id': candidate['id'],
            'title': candidate['title'],
            'entidad': candidate['entidad'],
            'semaforo': candidate['semaforo'],
            'detected_at': candidate['detected_at'],
            'document_url': candidate['document_url'],
            'score': rel['score'],
            'cross_entity': rel['cross_entity'],
            'reasons': rel['reasons'],
            'days_older': days_diff,
        })

    related.sort(key=lambda r: (r['score'], -((r['days_older'] if isinstance(r['days_older'], int) else 999999))), reverse=True)

    return jsonify({
        'document': {
            'id': seed['id'],
            'title': seed['title'],
            'entidad': seed['entidad'],
            'semaforo': seed['semaforo'],
            'detected_at': seed['detected_at'],
            'document_url': seed['document_url'],
        },
        'before_only': before_only,
        'min_score': min_score,
        'total_related': len(related),
        'related': related[:max_related],
    })

@app.route('/api/mapa-riesgos')
def api_mapa_riesgos():
    """Retrieve risk map data categorized and analyzed."""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    casos = read_csv(SEMAFORO_FILE)
    
    # Filter by date range if provided
    filtered_casos = []
    for caso in casos:
        det_date = caso.get('detected_at', '')[:10]
        if start_date and det_date < start_date:
            continue
        if end_date and det_date > end_date:
            continue
        filtered_casos.append(caso)
        
    # Group and analyze
    groups = {}
    for caso in filtered_casos:
        cat_key, cat_label, cat_icon, cat_color, cat_bg, cat_border = classify_legal_risk(caso)
        if cat_key not in groups:
            meta = get_risk_meta(cat_key)
            groups[cat_key] = {
                "id": cat_key,
                "label": cat_label,
                "icon": cat_icon,
                "color": cat_color,
                "bgColor": cat_bg,
                "borderColor": cat_border,
                "relation": meta["relation"],
                "riskAssessment": meta["risk"],
                "children": []
            }
        
        # Child case particular legal risk assessment
        notes = (caso.get('notes') or '').lower()
        priority = (caso.get('Incidencia SURA') or caso.get('priority') or '').upper()
        entidad = caso.get('entidad', '')
        
        particular_risk = f"Obligación con {entidad} clasificada como prioridad {priority}."
        if priority == 'ALTA':
            particular_risk += " Exige revisión jurídica prioritaria por riesgo de incumplimiento legal."
        else:
            particular_risk += " Requiere monitoreo en el ciclo de cumplimiento rutinario."
            
        groups[cat_key]["children"].append({
            "id": caso.get('case_id') or f"case_{hash(caso.get('document_url', ''))}",
            "text": caso.get('motivo') or 'Cumplimiento normativo detectado',
            "document_url": caso.get('document_url', '#'),
            "detected_at": caso.get('detected_at', '')[:10],
            "priority": priority,
            "particular_risk": particular_risk,
            "entidad": entidad
        })
        
    # Return as list of nodes
    nodes_list = list(groups.values())
    
    # Define layout angles dynamically depending on the number of active nodes
    angles = [-90, -30, 30, 90, 150, 210, 270]
    for i, node in enumerate(nodes_list):
        node["angle"] = angles[i % len(angles)]
        
    response_data = {
        "start_date": start_date or "Mínima",
        "end_date": end_date or "Máxima",
        "total_cases": len(filtered_casos),
        "nodes": nodes_list
    }
    return jsonify(response_data)


@app.route('/site_tree')
def site_tree():
    """Route to visualize the site structure graphically."""
    entidad = request.args.get('entidad')
    if not entidad:
        return "Entidad no especificada", 400
        
    tree_dir = os.path.join(ROOT, 'wiki', 'operations', 'site_trees')
    if not os.path.exists(tree_dir):
        return "No hay árboles registrados aún", 404
        
    # Buscar el archivo más reciente para esa entidad
    safe_e = "".join([c if c.isalnum() else "_" for c in entidad])
    files = [f for f in os.listdir(tree_dir) if safe_e in f and f.endswith('.txt')]
    if not files:
        # Intentar con un match más parcial por si acaso
        files = [f for f in os.listdir(tree_dir) if f.endswith('.txt')]
        files = [f for f in files if entidad[:10] in f]
        
    if not files:
        return f"No se encontró un árbol de navegación reciente para '{entidad}'. Asegúrate de correr el monitor primero.", 404
        
    latest_file = sorted(files, reverse=True)[0]
    filepath = os.path.join(tree_dir, latest_file)
    
    # Estructura JSON para D3.js
    tree_data = {"name": entidad, "children": []}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        current_parent = None
        for line in f:
            line = line.strip()
            if line.startswith('📂'):
                url = line.replace('📂', '').strip()
                current_parent = {"name": url, "children": []}
                tree_data["children"].append(current_parent)
            elif line.startswith('└──') and current_parent:
                parts = line.split(': ')
                url = parts[-1].strip()
                tipo = "[DOC]" if "DOC" in line else "[LINK]"
                current_parent["children"].append({"name": f"{tipo} {url.split('/')[-1]}"})
                
    return render_template('site_tree.html', entidad=entidad, tree_json=json.dumps(tree_data))

@app.route('/fuentes')
def fuentes():
    """Route to manage seed URLs (Fuentes Normativas)."""
    fuentes_file = os.path.join(ROOT, 'data', 'Fuentes Normativas - limpio utf8 v2.csv')
    fuentes = []
    if os.path.exists(fuentes_file):
        with open(fuentes_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            # Filtrar filas vacías
            fuentes = [row for row in reader if row.get('Entidad', '').strip() != '']
            
    # Ordenar alfabéticamente por Entidad
    fuentes = sorted(fuentes, key=lambda x: x.get('Entidad', '').lower())
    
    return render_template('fuentes.html', fuentes=fuentes)

@app.route('/api/update_fuente', methods=['POST'])
def update_fuente():
    """API to add/edit/delete sources."""
    data = request.json
    action = data.get('action') # 'add', 'edit', 'delete'
    fuentes_file = os.path.join(ROOT, 'data', 'Fuentes Normativas - limpio utf8 v2.csv')
    
    fuentes = []
    if os.path.exists(fuentes_file):
        with open(fuentes_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fuentes = list(reader)
    
    if action == 'add':
        fuentes.append({'Entidad': data['entidad'], 'Enlace': data['enlace'], 'Fuente control SOX': data.get('sox', '')})
    elif action == 'edit':
        for f in fuentes:
            if f['Entidad'] == data['old_entidad']:
                f['Entidad'] = data['entidad']
                f['Enlace'] = data['enlace']
                f['Fuente control SOX'] = data.get('sox', '')
    elif action == 'delete':
        fuentes = [f for f in fuentes if f['Entidad'] != data['entidad']]
    
    # Escribir de vuelta al CSV
    with open(fuentes_file, 'w', encoding='utf-8', newline='') as f:
        if fuentes:
            writer = csv.DictWriter(f, fieldnames=fuentes[0].keys())
            writer.writeheader()
            writer.writerows(fuentes)
            
    return jsonify({'status': 'success'})

@app.route('/api/tokens_stats')
def api_tokens_stats():
    """API endpoint to get token usage statistics."""
    casos = read_csv(CASOS_FILE)
    
    stats = {
        'total': 0,
        'by_entity': {},
        'by_date': {},
        'by_week': {},
        'by_month': {}
    }
    
    for c in casos:
        try:
            tokens = int(float(c.get('tokens_ia', 0) or 0))
        except (ValueError, TypeError):
            tokens = 0
            
        if tokens == 0: continue
        
        entidad = c.get('entidad', 'Desconocida')
        fecha_str = c.get('analisis_ia_fecha', '')[:10] # YYYY-MM-DD
        
        if not fecha_str:
            fecha_str = c.get('detected_at', '')[:10]
            
        if not fecha_str:
            fecha_str = 'Desconocida'
            mes_str = 'Desconocido'
            sem_str = 'Desconocida'
        else:
            mes_str = fecha_str[:7] # YYYY-MM
            try:
                dt = datetime.strptime(fecha_str, '%Y-%m-%d')
                # Obtener año y semana en formato YYYY-Www
                sem_str = dt.strftime('%Y-W%W')
            except ValueError:
                sem_str = 'Desconocida'
            
        stats['total'] += tokens
        
        stats['by_entity'][entidad] = stats['by_entity'].get(entidad, 0) + tokens
        stats['by_date'][fecha_str] = stats['by_date'].get(fecha_str, 0) + tokens
        stats['by_month'][mes_str] = stats['by_month'].get(mes_str, 0) + tokens
        stats['by_week'][sem_str] = stats['by_week'].get(sem_str, 0) + tokens
        
    return jsonify(stats)

@app.route('/api/casos')
def api_casos():
    """API endpoint to get filtered casos."""
    semaforo = request.args.get('semaforo')
    entidad = request.args.get('entidad')
    priority = request.args.get('priority')
    link_status = request.args.get('link_status')
    search = request.args.get('search')
    date = request.args.get('date')

    casos = get_casos_by_filter(semaforo, entidad, priority, link_status, search, date)
    
    # Cachear archivos de mapas existentes para optimizar
    tree_dir = os.path.join(ROOT, 'wiki', 'operations', 'site_trees')
    existing_trees = os.listdir(tree_dir) if os.path.exists(tree_dir) else []
    
    # Mapeo de slugs de archivos a booleanos
    # El archivo es YYYY-MM-DD_Nombre_Entidad.txt
    map_slugs = set()
    for f in existing_trees:
        if f.endswith('.txt'):
            # Quitamos la fecha inicial (11 chars: YYYY-MM-DD_) e ignoramos mayúsculas
            slug = f[11:].replace('.txt', '').lower()
            if slug: map_slugs.add(slug)

    for c in casos:
        # Probar con Emisor (fuente) y entidad (IA)
        found = False
        for field in ['Emisor', 'entidad']:
            val = c.get(field, '')
            if not val: continue
            # Normalizar para comparación fuzzy
            clean_val = "".join([x if x.isalnum() else "_" for x in val]).lower()
            
            # Match directo o contenido
            if clean_val in map_slugs:
                found = True
                break
            
            # Match inverso o por palabras clave
            for slug in map_slugs:
                # Si el slug del mapa está en el nombre o viceversa
                if slug in clean_val or clean_val in slug:
                    found = True
                    break
                # O si comparten palabras significativas (ej. Finagro)
                words_slug = set(s for s in slug.split('_') if len(s) > 3)
                words_val = set(v for v in clean_val.split('_') if len(v) > 3)
                if words_slug.intersection(words_val):
                    found = True
                    break
            if found: break
        
        c['has_map'] = found

    # Escanear análisis en wiki para asociarlos por archivo/fuente original
    wiki_dir = os.path.join(ROOT, "wiki", "analyses")
    analysis_files = {}
    if os.path.exists(wiki_dir):
        for f in os.listdir(wiki_dir):
            if f.endswith('.md') and not f.startswith('.'):
                try:
                    fpath = os.path.join(wiki_dir, f)
                    with open(fpath, 'r', encoding='utf-8') as wf:
                        content = wf.read()
                        if content.startswith('---'):
                            parts = content.split('---', 2)
                            if len(parts) >= 3:
                                frontmatter = parts[1]
                                sf_match = re.search(r'source_files:\s*\["(.*?)"\]', frontmatter)
                                if sf_match:
                                    sf = sf_match.group(1)
                                    if sf:
                                        analysis_files[sf] = f
                except Exception:
                    pass

    for c in casos:
        doc_url = c.get('document_url', '')
        fuente_url = c.get('fuente_url', '')
        match_wiki = None
        for k, v in analysis_files.items():
            if k == doc_url or k == fuente_url or (doc_url and doc_url.endswith(k)) or (fuente_url and fuente_url.endswith(k)):
                match_wiki = v
                break
        c['wiki_analysis_file'] = match_wiki
            
    return jsonify(casos)


@app.route('/api/summary')
def api_summary():
    """API endpoint for summary."""
    return jsonify(get_summary())


@app.route('/api/upload_manual', methods=['POST'])
def upload_manual():
    """Permite subir un archivo manualmente para una entidad cuando falla el bot."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    entidad = request.form.get('entidad')
    # Nuevos campos de trazabilidad
    titulo_manual = request.form.get('titulo')
    url_origen = request.form.get('url_origen')
    fecha_pub = request.form.get('fecha_pub')
    
    if file.filename == '' or not entidad:
        return jsonify({'error': 'Falta archivo o entidad'}), 400

    filename = secure_filename(file.filename)
    cid = hashlib.sha256(f"MANUAL|{entidad}|{filename}|{datetime.now().timestamp()}".encode()).hexdigest()[:16]
    
    # Guardar en raw/inbox
    inbox_dir = os.path.join(ROOT, 'raw', 'inbox')
    os.makedirs(inbox_dir, exist_ok=True)
    ext = filename.split('.')[-1].lower()
    local_path = os.path.join(inbox_dir, f"{cid}.{ext}")
    file.save(local_path)
    
    # Registrar en el CSV como 'detectado' pero marcado como manual
    now = datetime.now(COLOMBIA_TZ).strftime('%Y-%m-%d %H:%M:%S%z')
    new_row = {
        'case_id': cid,
        'detected_at': now,
        'entidad': entidad,
        'status': 'detectado',
        'priority': 'ALTA',
        'link_status': 'ok',
        'notes': f'Carga manual por usuario. Origen reportado: {url_origen or "No especificado"}',
        'Título': titulo_manual or filename,
        'URL': url_origen or 'manual_upload',
        'fuente_url': 'Carga Manual',
        'document_url': f'/{cid}.{ext}', # Ruta local virtual
        'Fecha de publicación': fecha_pub or now[:10],
        'Fecha registro': now[:10],
        'Emisor': entidad
    }
    
    # Escribir en CSV
    header_exists = os.path.exists(CASES_FILE)
    with open(CASES_FILE, 'a', encoding='utf-8', newline='') as f:
        fieldnames = ['case_id', 'Resultado análisis', 'Fecha registro', 'Tipo', 'Título', 'URL', 'Anexos', 'Fecha de publicación', 'Emisor', 'Norma', 'Fecha de divulgación', 'Tipo de Norma', 'Tema', 'Sector Económico', 'Incidencia SURA', 'Obligaciones SURA', 'Norma Importante', 'Control SOX', 'Divulgación SOX', 'Compañía Impactada', 'Obligaciones', 'Persona que analizó', 'Justificación de no divulgación SOX', 'detected_at', 'entidad', 'fuente_url', 'document_url', 'publication_date', 'status', 'priority', 'aplica_sura', 'link_status', 'link_error', 'notes', 'analisis_ia_status', 'analisis_ia_fecha', 'tokens_ia', 'sincronizado_excel']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not header_exists: writer.writeheader()
        writer.writerow({fn: new_row.get(fn, '') for fn in fieldnames})
        
    # Regenerar tablero para que aparezca
    subprocess.run(['python3', os.path.join(SRC_ROOT, 'scripts/generar_tablero_semaforo.py')])
    
    return jsonify({'success': True, 'case_id': cid})

TAGS_FILE = os.path.join(ROOT, 'data', 'tag_definitions.json')

def read_tags():
    if not os.path.exists(TAGS_FILE):
        return []
    try:
        with open(TAGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_tags(tags):
    with open(TAGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tags, f, indent=4, ensure_ascii=False)

SPECIALTIES_FILE = os.path.join(ROOT, 'data', 'specialties.json')

def read_specialties():
    if not os.path.exists(SPECIALTIES_FILE):
        return []
    try:
        with open(SPECIALTIES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_specialties(specs):
    with open(SPECIALTIES_FILE, 'w', encoding='utf-8') as f:
        json.dump(specs, f, indent=4, ensure_ascii=False)

@app.route('/tags')
def tags_page():
    tags = read_tags()
    specs = read_specialties()
    return render_template('tags.html', tags=tags, specialties=specs)

@app.route('/api/specialties/save', methods=['POST'])
def api_save_specialty():
    new_spec = request.json.get('specialty')
    specs = read_specialties()
    if new_spec and new_spec not in specs:
        specs.append(new_spec)
        save_specialties(specs)
    return jsonify({'status': 'success'})

@app.route('/api/specialties/delete', methods=['POST'])
def api_delete_specialty():
    spec_name = request.json.get('specialty')
    specs = read_specialties()
    specs = [s for s in specs if s != spec_name]
    save_specialties(specs)
    return jsonify({'status': 'success'})

@app.route('/api/tags/save', methods=['POST'])
def api_save_tag():
    new_tag = request.json
    tags = read_tags()
    # Update if exists, else append
    existing = next((t for t in tags if t['tag'] == new_tag['tag']), None)
    if existing:
        existing.update(new_tag)
    else:
        tags.append(new_tag)
    save_tags(tags)
    return jsonify({'status': 'success'})

@app.route('/api/tags/delete', methods=['POST'])
def api_delete_tag():
    tag_name = request.json.get('tag')
    tags = read_tags()
    tags = [t for t in tags if t['tag'] != tag_name]
    save_tags(tags)
    return jsonify({'status': 'success'})

@app.route('/api/update_case', methods=['POST'])
def update_case():
    """Update a specific case in the CSV and regenerate summary."""
    data = request.json
    case_id = data.get('case_id')
    if not case_id:
        return jsonify({'error': 'No case_id provided'}), 400

    # 1. Update cases_detectados.csv
    updated = False
    temp_file = CASOS_FILE + '.tmp'
    
    with open(CASOS_FILE, 'r', encoding='utf-8', newline='') as f_in, \
         open(temp_file, 'w', encoding='utf-8', newline='') as f_out:
        
        reader = csv.DictReader(f_in)
        writer = csv.DictWriter(f_out, fieldnames=reader.fieldnames)
        writer.writeheader()
        
        for row in reader:
            if row['case_id'] == case_id:
                # Update allowed fields
                for field in data:
                    if field in row:
                        row[field] = data[field]
                updated = True
            writer.writerow(row)
    
    if updated:
        os.replace(temp_file, CASOS_FILE)
        # 2. Regenerate dashboard and Obsidian Wiki
        try:
            import subprocess
            subprocess.run(['python3', os.path.join(SRC_ROOT, 'scripts/generar_tablero_semaforo.py')], check=True)
            subprocess.run(['python3', os.path.join(SRC_ROOT, 'scripts/generar_wiki_obsidian.py')], check=True)
            subprocess.run(['python3', os.path.join(SRC_ROOT, 'scripts/generar_kanban.py')], check=True)
        except Exception as e:
            print(f"Error regenerando: {e}")
        
        return jsonify({'status': 'success'})
    else:
        os.remove(temp_file)
        return jsonify({'error': 'Case not found'}), 404


# ─── Analizador de Obligaciones Regulatorias ─────────────────────────────────

@app.route('/gobierno')
def gobierno_page():
    """Página de Estructura de Gobierno y Enlaces de Cumplimiento."""
    return render_template('gobierno.html')


@app.route('/skills')
def skills_library_page():
    """Biblioteca de skills del repositorio."""
    return render_template('skills_library.html')


@app.route('/skills/detail')
def skill_detail_page():
    """Pantalla de detalle y configuracion editable de un skill."""
    return render_template('skill_detail.html')


@app.route('/api/skills')
def api_skills_library():
    """Lista de skills disponibles en .github/skills."""
    state = _read_skill_config_state()
    items = []
    for skill_id, skill_dir in _find_skill_dirs():
        md_path = os.path.join(skill_dir, 'SKILL.md')
        parsed = _parse_skill_markdown(md_path)
        assets = _detect_skill_assets(skill_dir, max_items=1)
        conf = state.get(skill_id, {})
        items.append({
            'id': skill_id,
            'name': parsed.get('name') or skill_id.split('/')[-1],
            'description': parsed.get('description', ''),
            'path': os.path.relpath(md_path, CNORM_ROOT).replace(os.sep, '/'),
            'updated_at': datetime.fromtimestamp(os.path.getmtime(md_path)).strftime('%Y-%m-%d %H:%M'),
            'asset_count': assets.get('total', 0),
            'status': conf.get('status', 'active'),
            'category': conf.get('category', 'general'),
            'priority': conf.get('priority', 3),
            'url': f"/skills/detail?skill={quote(skill_id)}",
        })
    return jsonify({'success': True, 'skills': items})


@app.route('/api/skills/detail')
def api_skill_detail():
    """Detalle completo de un skill con configuracion editable."""
    skill_id = request.args.get('skill', '')
    skill_dir = _get_skill_by_id(skill_id)
    if not skill_dir:
        return jsonify({'error': 'Skill no encontrado'}), 404

    md_path = os.path.join(skill_dir, 'SKILL.md')
    parsed = _parse_skill_markdown(md_path)
    assets_data = _detect_skill_assets(skill_dir, max_items=250)

    state = _read_skill_config_state()
    cfg = state.get(skill_id)
    if not cfg:
        cfg = _default_skill_config(skill_id, assets_data.get('items', []))

    return jsonify({
        'success': True,
        'skill': {
            'id': skill_id,
            'name': parsed.get('name') or skill_id.split('/')[-1],
            'description': parsed.get('description', ''),
            'overview': parsed.get('overview', ''),
            'when_to_use': parsed.get('when_to_use', ''),
            'when_not_to_use': parsed.get('when_not_to_use', ''),
            'quick_start': parsed.get('quick_start', ''),
            'path': os.path.relpath(md_path, CNORM_ROOT).replace(os.sep, '/'),
            'assets_detected': assets_data,
            'config': cfg,
        }
    })


@app.route('/api/skills/save', methods=['POST'])
def api_skill_save():
    """Guarda configuracion editable del skill sin modificar SKILL.md."""
    payload = request.get_json(silent=True) or {}
    skill_id = (payload.get('skill_id') or '').strip()
    config = payload.get('config') or {}

    skill_dir = _get_skill_by_id(skill_id)
    if not skill_dir:
        return jsonify({'error': 'Skill no encontrado'}), 404

    if not isinstance(config, dict):
        return jsonify({'error': 'Configuracion invalida'}), 400

    state = _read_skill_config_state()
    state[skill_id] = config
    _write_skill_config_state(state)
    return jsonify({'success': True})


@app.route('/analizar')
def analizar_page():
    """Página del analizador de obligaciones regulatorias con IA."""
    import urllib.parse
    casos = read_csv(CASOS_FILE)
    pdfs_monitor = []
    for c in casos:
        url = c.get('document_url', '') or c.get('URL', '')
        if (c.get('link_status', '').lower() == 'ok' or c.get('link_status', '') == '') and '.pdf' in url.lower():
            # Extraer un nombre descriptivo del archivo desde la URL
            filename = url.split('/')[-1] if '/' in url else ''
            filename = filename.split('?')[0]
            filename = urllib.parse.unquote(filename)
            
            titulo = c.get('Título') or c.get('titulo')
            if not titulo or titulo == 'nan' or titulo == '':
                titulo = filename if filename else (c.get('notes', '')[:60] or 'Documento sin título')
                
            pdfs_monitor.append({
                'case_id': c.get('case_id', ''),
                'entidad': c.get('entidad', ''),
                'url': url,
                'titulo': titulo,
                'detected_at': c.get('detected_at', '')
            })
    # Ordenar por fecha de detección descendente para mostrar los más nuevos primero
    pdfs_monitor.sort(key=lambda x: x.get('detected_at', ''), reverse=True)
    pdfs_monitor = pdfs_monitor[:500]

    # Cargar análisis existentes desde wiki/analyses
    wiki_dir = os.path.join(ROOT, "wiki", "analyses")
    analizados = []
    if os.path.exists(wiki_dir):
        import glob
        md_files = glob.glob(os.path.join(wiki_dir, "*.md"))
        for filepath in md_files:
            fname = os.path.basename(filepath)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                # Extraer título y fecha del frontmatter
                title = "Análisis sin título"
                date_created = "—"
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        frontmatter = parts[1]
                        for line in frontmatter.split('\n'):
                            if ':' in line:
                                k, v = line.split(':', 1)
                                k = k.strip()
                                v = v.strip().strip('"').strip("'")
                                if k == 'title':
                                    title = v.replace('Análisis: ', '')
                                elif k == 'created':
                                    date_created = v
                analizados.append({
                    'filename': fname,
                    'title': title,
                    'created': date_created
                })
            except Exception:
                pass
    # Ordenar por fecha descendente
    analizados.sort(key=lambda x: x.get('created', ''), reverse=True)

    return render_template('analizar.html', pdfs_monitor=pdfs_monitor, analizados=analizados)


@app.route('/api/analisis_existente')
def api_analisis_existente():
    """Retorna el resultado parseado de un análisis Markdown guardado en wiki/analyses/."""
    wiki_file = request.args.get('wiki_file')
    if not wiki_file:
        return jsonify({'error': 'Falta el parámetro wiki_file'}), 400
    
    wiki_dir = os.path.join(ROOT, "wiki", "analyses")
    filepath = os.path.join(wiki_dir, wiki_file)
    if not os.path.exists(filepath):
        return jsonify({'error': 'Archivo de análisis no encontrado'}), 404
        
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        resultado = {
            'datos_generales': {},
            'obligaciones': []
        }
        
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                for line in frontmatter.split('\n'):
                    if ':' in line:
                        k, v = line.split(':', 1)
                        k = k.strip()
                        v = v.strip().strip('"').strip("'")
                        if k == 'title':
                            resultado['datos_generales']['norma'] = v.replace('Análisis: ', '')
                        elif k == 'source_files':
                            sf_match = re.search(r'\["(.*?)"\]', v)
                            if sf_match:
                                resultado['datos_generales']['_fuente'] = sf_match.group(1)
                                resultado['_fuente'] = sf_match.group(1)
                
                body = parts[2]
                dg_section = re.search(r'## Datos Generales de la Norma\s*\n\n(.*?)(?=\n\n##|$)', body, re.DOTALL)
                if dg_section:
                    for row in dg_section.group(1).split('\n'):
                        if '| **' in row:
                            rparts = [p.strip() for p in row.split('|') if p.strip()]
                            if len(rparts) >= 2:
                                label = rparts[0].replace('**', '').strip()
                                value = rparts[1]
                                label_map = {
                                    'Título': 'titulo', 'Emisor': 'emisor', 'Tipo de Norma': 'tipo_norma',
                                    'Fecha de Publicación': 'fecha_publicacion', 'Jurisdicción': 'jurisdiccion',
                                    'Incidencia SURA': 'incidencia_sura', 'Control SOX': 'control_sox',
                                    'Divulgación SOX': 'divulgacion_sox', 'Anexos': 'anexos'
                                }
                                if label in label_map:
                                    resultado['datos_generales'][label_map[label]] = value
                
                obl_matches = re.finditer(r'### Obligación \d+ — (.*?)\n(.*?)(?=\n### Obligación \d+ — |\n## Caveats|\n##|$)', body, re.DOTALL)
                for m in obl_matches:
                    numeral = m.group(1).strip()
                    table_content = m.group(2).strip()
                    ob = {'numeral_articulo': numeral}
                    for row in table_content.split('\n'):
                        if '| **' in row:
                            rparts = [p.strip() for p in row.split('|') if p.strip()]
                            if len(rparts) >= 2:
                                label = rparts[0].replace('**', '').strip()
                                value = rparts[1]
                                label_map = {
                                    'Texto': 'texto_obligacion', 'Frecuencia': 'frecuencia',
                                    'Entregable': 'entregable', 'Normas relacionadas': 'normas_relacionadas',
                                    'Macroproceso': 'macroproceso', 'Proceso': 'proceso', 'Líder': 'lider_proceso'
                                }
                                if label in label_map:
                                    ob[label_map[label]] = value
                    
                    ob['tipo_obligacion'] = 'General'
                    txt_low = ob.get('texto_obligacion', '').lower()
                    verb_map = {
                        'Reportar': ['reportar', 'notificar', 'remitir', 'presentar', 'enviar', 'declarar'],
                        'Pagar': ['pagar', 'liquidar', 'desembolsar', 'transferir', 'financiar', 'costear'],
                        'Implementar': ['implementar', 'adoptar', 'crear', 'establecer', 'diseñar', 'desarrollar'],
                        'Controlar': ['controlar', 'monitorear', 'evaluar', 'auditar', 'supervisar', 'vigilar'],
                        'Documentar': ['documentar', 'registrar', 'archivar', 'conservar', 'guardar'],
                        'Autorizar': ['autorizar', 'aprobar', 'permitir', 'licenciar', 'validar'],
                        'Capacitar': ['capacitar', 'entrenar', 'formar', 'instruir', 'educar'],
                        'Prohibición': ['prohibir', 'prohibición', 'no permitir', 'sancionar'],
                        'Divulgar': ['divulgar', 'comunicar', 'publicar', 'difundir'],
                        'Garantizar': ['garantizar', 'asegurar', 'proteger'],
                        'Actualizar': ['actualizar', 'modificar', 'reformar', 'revisar']
                    }
                    for k, vlist in verb_map.items():
                        if any(v in txt_low for v in vlist):
                            ob['tipo_obligacion'] = k
                            break
                    resultado['obligaciones'].append(ob)
        
        return jsonify({'success': True, 'resultado': resultado})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/prompt')
def api_prompt():
    """Retorna el prompt completo utilizado para el análisis de IA."""
    try:
        from scripts.analizar_norma import _load_listas, _build_prompt
        listas = _load_listas()
        prompt = _build_prompt(listas)
        return jsonify({'success': True, 'prompt': prompt})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/repair_metrics')
def api_repair_metrics():
    """Retorna métricas de auto-reparación a partir del historial JSONL."""
    history_file = os.path.join(ROOT, 'data', 'state', 'ia_repair_history.jsonl')
    if not os.path.exists(history_file):
        return jsonify({
            'success': True,
            'metrics': {
                'total_runs': 0,
                'initial_invalid_rate': 0.0,
                'recovery_rate': 0.0,
                'fallback_rate_total': 0.0,
                'fallback_rate_invalid': 0.0,
                'avg_repair_attempts_invalid': 0.0,
                'top_repair_reasons': [],
                'last_event_at': None,
            }
        })

    rows = []
    with open(history_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception:
                continue

    total = len(rows)
    if total == 0:
        return jsonify({
            'success': True,
            'metrics': {
                'total_runs': 0,
                'initial_invalid_rate': 0.0,
                'recovery_rate': 0.0,
                'fallback_rate_total': 0.0,
                'fallback_rate_invalid': 0.0,
                'avg_repair_attempts_invalid': 0.0,
                'top_repair_reasons': [],
                'last_event_at': None,
            }
        })

    invalid_count = 0
    recovered_count = 0
    fallback_count = 0
    repair_attempts_invalid = []
    reasons = Counter()
    last_event_at = None

    for row in rows:
        repair = row.get('repair_info', {}) or {}
        meta = row.get('meta', {}) or {}
        auto_repaired = bool(repair.get('auto_repaired', False))
        attempts = int(repair.get('repair_attempts', 0) or 0)
        reason = str(repair.get('repair_reason', '') or '').strip()
        final_valid = bool(meta.get('valid', False))

        ts = row.get('timestamp')
        if ts and (last_event_at is None or ts > last_event_at):
            last_event_at = ts

        if auto_repaired:
            invalid_count += 1
            repair_attempts_invalid.append(attempts)
            if reason:
                reasons[reason] += 1
            if final_valid:
                recovered_count += 1
            else:
                fallback_count += 1

    initial_invalid_rate = round((invalid_count / total) * 100, 2)
    recovery_rate = round((recovered_count / invalid_count) * 100, 2) if invalid_count else 0.0
    fallback_rate_total = round((fallback_count / total) * 100, 2)
    fallback_rate_invalid = round((fallback_count / invalid_count) * 100, 2) if invalid_count else 0.0
    avg_repair_attempts_invalid = (
        round(sum(repair_attempts_invalid) / len(repair_attempts_invalid), 2)
        if repair_attempts_invalid else 0.0
    )

    return jsonify({
        'success': True,
        'metrics': {
            'total_runs': total,
            'initial_invalid_rate': initial_invalid_rate,
            'recovery_rate': recovery_rate,
            'fallback_rate_total': fallback_rate_total,
            'fallback_rate_invalid': fallback_rate_invalid,
            'avg_repair_attempts_invalid': avg_repair_attempts_invalid,
            'top_repair_reasons': [
                {'reason': reason, 'count': count}
                for reason, count in reasons.most_common(5)
            ],
            'last_event_at': last_event_at,
        }
    })



@app.route('/api/analizar', methods=['POST'])
def api_analizar():
    """
    Analiza un documento PDF con IA y retorna la extracción estructurada.
    Acepta:
      - JSON { "url": "https://..." }  (PDF del monitor)
      - multipart/form-data con campo 'file' (PDF subido manualmente)
    """
    try:
        from scripts.analizar_norma import analizar_desde_url, analizar_desde_bytes
    except ImportError as e:
        return jsonify({'error': f'Módulo de análisis no disponible: {e}'}), 500

    # Opción A: URL del monitor
    if request.is_json:
        data = request.get_json()
        url = data.get('url', '').strip()
        if not url:
            return jsonify({'error': 'Se debe proveer una URL'}), 400
        try:
            resultado = analizar_desde_url(url)
            return jsonify({'success': True, 'resultado': resultado})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Opción B: PDF subido manualmente
    if 'file' in request.files:
        f = request.files['file']
        if f.filename == '':
            return jsonify({'error': 'Archivo vacío'}), 400
        if not f.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Solo se aceptan archivos PDF'}), 400
        try:
            pdf_bytes = f.read()
            resultado = analizar_desde_bytes(pdf_bytes, nombre=f.filename)
            return jsonify({'success': True, 'resultado': resultado})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Petición inválida. Envía una URL (JSON) o un archivo PDF (multipart)'}), 400


@app.route('/api/guardar_analisis', methods=['POST'])
def api_guardar_analisis():
    """Guarda el resultado del análisis como página en wiki/analyses/."""
    data = request.get_json()
    resultado = data.get('resultado')
    if not resultado:
        return jsonify({'error': 'Sin resultado que guardar'}), 400

    dg = resultado.get('datos_generales', {})
    norma = dg.get('norma', 'Norma sin título').replace('/', '-').replace('\\', '-')[:60]
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')

    # Construir el contenido markdown
    obs = resultado.get('obligaciones', [])
    obs_md = ""
    for i, o in enumerate(obs, 1):
        obs_md += f"""
### Obligación {i} — {o.get('numeral_articulo', 'Sin artículo')}

| Campo | Valor |
|---|---|
| **Texto** | {o.get('texto_obligacion', '')} |
| **Frecuencia** | {o.get('frecuencia', '')} |
| **Entregable** | {o.get('entregable', '')} |
| **Normas relacionadas** | {o.get('normas_relacionadas', '')} |
| **Macroproceso** | {o.get('macroproceso', '')} |
| **Proceso** | {o.get('proceso', '')} |
| **Líder** | {o.get('lider_proceso', '')} |
"""

    contenido = f"""---
title: "Análisis: {norma}"
type: analysis
status: draft
created: {fecha_hoy}
updated: {fecha_hoy}
source_files: ["{dg.get('_fuente', '')}"]
confidence: medium
tags: [analisis-ia, obligaciones]
---

## Pregunta

Extracción estructurada de obligaciones de la norma: **{norma}**

## Datos Generales de la Norma

| Campo | Valor |
|---|---|
| **Título** | {dg.get('titulo', '')} |
| **Norma** | {dg.get('norma', '')} |
| **Emisor** | {dg.get('emisor', '')} |
| **Tipo de Norma** | {dg.get('tipo_norma', '')} |
| **Fecha de Publicación** | {dg.get('fecha_publicacion', '')} |
| **Jurisdicción** | {dg.get('jurisdiccion', '')} |
| **Temas** | {', '.join(dg.get('temas', []))} |
| **Sectores Económicos** | {', '.join(dg.get('sectores_economicos', []))} |
| **Compañías Impactadas** | {', '.join(dg.get('companias_impactadas', []))} |
| **Incidencia SURA** | {dg.get('incidencia_sura', '')} |
| **Control SOX** | {dg.get('control_sox', '')} |
| **Divulgación SOX** | {dg.get('divulgacion_sox', '')} |
| **Anexos** | {dg.get('anexos', '')} |

## Obligaciones Identificadas ({len(obs)})

{obs_md}

## Caveats

- Análisis generado automáticamente por IA. Verificar con experto jurídico.
- Los campos de incidencia, SOX y compañías requieren evaluación externa.
- Tokens utilizados: {resultado.get('_tokens', 'N/A')}

## Follow-up Actions

- [ ] Validar obligaciones con abogado responsable
- [ ] Clasificar incidencia SURA manualmente
- [ ] Asignar a proceso/área correspondiente
"""

    safe_name = re.sub(r'[^a-zA-Z0-9\- ]', '', norma).strip().replace(' ', '-').lower()[:40]
    filename = f"{fecha_hoy} - analisis-{safe_name}.md"
    wiki_dir = os.path.join(ROOT, "wiki", "analyses")
    os.makedirs(wiki_dir, exist_ok=True)
    filepath = os.path.join(wiki_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as wf:
        wf.write(contenido)

    # Buscar y actualizar el caso en casos_detectados.csv para persistir los tokens procesados
    fuente = dg.get('_fuente') or resultado.get('_fuente', '')
    tokens_usados = resultado.get('_tokens', 0)
    
    if fuente:
        try:
            casos = read_csv(CASOS_FILE)
            updated_any = False
            for c in casos:
                # Comparamos la fuente o URL original
                if c.get('document_url') == fuente or c.get('fuente_url') == fuente or c.get('URL') == fuente or c.get('fuente_url', '').endswith(fuente) or fuente.endswith(c.get('document_url', '---')):
                    c['tokens_ia'] = str(tokens_usados)
                    c['analisis_ia_status'] = 'completado'
                    c['analisis_ia_fecha'] = fecha_hoy
                    updated_any = True
            
            if updated_any and casos:
                with open(CASOS_FILE, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=casos[0].keys())
                    writer.writeheader()
                    writer.writerows(casos)
                    
                # Regenerar el tablero semáforo para sincronizar contadores
                subprocess.run(['python3', os.path.join(SRC_ROOT, 'scripts/generar_tablero_semaforo.py')], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            # Silenciosamente continuar para no romper la experiencia si falla la escritura del CSV
            pass

    return jsonify({'success': True, 'archivo': str(filepath)})


@app.route('/api/exportar_pdf', methods=['POST'])
def api_exportar_pdf():
    """Genera dinámicamente un archivo PDF de las obligaciones analizadas y lo retorna."""
    try:
        from xhtml2pdf import pisa
        import io
    except ImportError:
        return jsonify({'error': 'Librería xhtml2pdf no disponible.'}), 500

    data = request.get_json()
    resultado = data.get('resultado')
    if not resultado:
        return jsonify({'error': 'Sin resultado para exportar'}), 400

    dg = resultado.get('datos_generales', {})
    obs = resultado.get('obligaciones', [])

    # ── Helper: mini-tabla con cabecera azul SURA ────────────────────────────
    def _mini_table(headers, rows, accent="#0033A0"):
        th = "".join(
            f'<td style="background:{accent};color:#FFF;font-weight:bold;'
            f'padding:4px 6px;font-size:7pt;">{h}</td>'
            for h in headers
        )
        trs = ""
        for row in rows:
            tds = "".join(
                f'<td style="padding:4px 6px;font-size:7.5pt;vertical-align:top;'
                f'border-bottom:1px solid #E7E7E7;">{v}</td>'
                for v in row
            )
            trs += f"<tr>{tds}</tr>"
        return (
            f'<table style="border-collapse:collapse;width:100%;'
            f'border:1px solid #D0D8F0;">'
            f"<tr>{th}</tr>{trs}</table>"
        )

    # ── Helper: badge visual para la frecuencia/plazo ────────────────────────
    import re as _re
    from datetime import datetime as _dt, timedelta as _td

    _MESES = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5,
        "junio": 6, "julio": 7, "agosto": 8, "septiembre": 9,
        "octubre": 10, "noviembre": 11, "diciembre": 12,
    }

    def _badge_frecuencia(texto, fecha_pub="", vigencia_desde=""):
        """Devuelve HTML con etiqueta visual de urgencia para el plazo."""
        # Determinar el texto de inicio de vigencia que se mostrará
        inicio_str = vigencia_desde or fecha_pub or ""

        if not texto or texto.strip() == "":
            label = f"Vigente desde {inicio_str}" if inicio_str else "Sin plazo definido"
            return (
                f'<span style="display:inline-block;background:#888B8D;color:#FFF;'
                f'padding:2px 6px;border-radius:9999px;font-size:6.5pt;'
                f'font-weight:bold;margin-bottom:3px;">VIGENTE</span><br/>'
                f'<span style="font-size:7pt;color:#3F3F41;">{label}</span>'
            )

        t = texto.strip().lower()
        hoy = _dt.today()

        # ── Detectar fecha explícita tipo "14 de mayo de 2026" ─────────────
        m = _re.search(
            r"(\d{1,2})\s+de\s+([a-záéíóú]+)\s+de\s+(\d{4})", t
        )
        if m:
            try:
                dia = int(m.group(1))
                mes = _MESES.get(m.group(2), 0)
                anio = int(m.group(3))
                if mes:
                    fecha = _dt(anio, mes, dia)
                    delta = (fecha - hoy).days
                    if delta < 0:
                        color, bg, icono, etiq = "#FFF", "#D12D35", "", "VENCIDO"
                    elif delta <= 30:
                        color, bg, icono, etiq = "#FFF", "#E85D2B", "", f"{delta}d"
                    elif delta <= 90:
                        color, bg, icono, etiq = "#3F3F41", "#ED8B00", "", f"{delta}d"
                    elif delta <= 180:
                        color, bg, icono, etiq = "#3F3F41", "#E3E829", "", f"{delta}d"
                    else:
                        color, bg, icono, etiq = "#FFF", "#067014", "", f"{delta}d"
                    return (
                        f'<span style="display:inline-block;background:{bg};color:{color};'
                        f'padding:2px 6px;border-radius:9999px;font-size:6.5pt;'
                        f'font-weight:bold;margin-bottom:3px;">{etiq}</span><br/>'
                        f'<span style="font-size:7pt;color:#3F3F41;">{texto}</span>'
                    )
            except ValueError:
                pass

        # ── Palabras clave periódicas ──────────────────────────────────────
        periodicas = ["mensual", "trimestral", "semestral", "anual", "bimestral",
                      "quincenal", "semanal", "diaria", "cada año", "cada mes"]
        if any(p in t for p in periodicas):
            return (
                f'<span style="display:inline-block;background:#2D6DF6;color:#FFF;'
                f'padding:2px 6px;border-radius:9999px;font-size:6.5pt;'
                f'font-weight:bold;margin-bottom:3px;">PERIÓDICO</span><br/>'
                f'<span style="font-size:7pt;color:#3F3F41;">{texto}</span>'
            )

        # ── Permanente / continuo ──────────────────────────────────────────
        if any(p in t for p in ["permanente", "continuo", "continua", "siempre"]):
            label = f"Vigente desde {inicio_str}" if inicio_str else "Permanente"
            return (
                f'<span style="display:inline-block;background:#888B8D;color:#FFF;'
                f'padding:2px 6px;border-radius:9999px;font-size:6.5pt;'
                f'font-weight:bold;margin-bottom:3px;">PERMANENTE</span><br/>'
                f'<span style="font-size:7pt;color:#3F3F41;">{label}</span>'
            )

        # ── Default: texto tal cual con estilo neutro ──────────────────────
        return (
            f'<span style="display:inline-block;background:#F4F4F4;color:#3F3F41;'
            f'border:1px solid #E7E7E7;'
            f'padding:2px 6px;border-radius:9999px;font-size:6.5pt;'
            f'font-weight:bold;margin-bottom:3px;">PLAZO</span><br/>'
            f'<span style="font-size:7pt;color:#3F3F41;">{texto}</span>'
        )

    # ── Paleta de tipos de obligación ─────────────────────────────────────────
    _TIPO_COLORS = {
        "Reportar":    ("#0033A0", "#FFF", ""),
        "Pagar":       ("#067014", "#FFF", ""),
        "Implementar": ("#7B2D8B", "#FFF", ""),
        "Controlar":   ("#ED8B00", "#FFF", ""),
        "Documentar":  ("#795548", "#FFF", ""),
        "Autorizar":   ("#3F51B5", "#FFF", ""),
        "Capacitar":   ("#00838F", "#FFF", ""),
        "Prohibición": ("#D12D35", "#FFF", ""),
        "Divulgar":    ("#C47A00", "#FFF", ""),
        "Garantizar":  ("#2E7D32", "#FFF", ""),
        "Actualizar":  ("#546E7A", "#FFF", ""),
        "General":     ("#888B8D", "#FFF", ""),
    }

    def _badge_tipo(tipo):
        bg, fg, icono = _TIPO_COLORS.get(tipo, ("#888B8D", "#FFF", ""))
        return (
            f'<span style="display:inline-block;background:{bg};color:{fg};'
            f'padding:2px 7px;border-radius:9999px;font-size:6.5pt;'
            f'font-weight:bold;white-space:nowrap;">{tipo}</span>'
        )

    # ── Ordenar y agrupar obligaciones por tipo ───────────────────────────────
    _TIPO_ORDER = ["Reportar","Pagar","Implementar","Controlar","Documentar",
                   "Autorizar","Capacitar","Prohibición","Divulgar",
                   "Garantizar","Actualizar","General"]
    obs_sorted = sorted(obs, key=lambda x: _TIPO_ORDER.index(x.get("tipo_obligacion","General"))
                        if x.get("tipo_obligacion","General") in _TIPO_ORDER else 99)

    obs_rows_html = ""
    current_tipo = None
    for i, o in enumerate(obs_sorted, 1):
        tipo = o.get("tipo_obligacion", "General")
        bg_tipo, fg_tipo, icono_tipo = _TIPO_COLORS.get(tipo, ("#888B8D", "#FFF", ""))

        # ─ Fila de encabezado de grupo cuando cambia el tipo ─
        if tipo != current_tipo:
            current_tipo = tipo
            obs_rows_html += f"""
        <tr style="background:{bg_tipo}; page-break-before:auto;">
            <td colspan="8" style="padding:6px 10px;color:{fg_tipo};
                font-weight:bold;font-size:9pt;border:1px solid #CCC;
                letter-spacing:0.5px;">
                {tipo.upper()}
            </td>
        </tr>"""

        # Formatear proceso responsable de forma limpia sin usar tablas anidadas (causan bugs en xhtml2pdf)
        macro = o.get("macroproceso", "N/A")
        proc = o.get("proceso", "N/A")
        lider = o.get("lider_proceso", "N/A")
        proceso_html = f"""
        <div style="font-size:7pt; line-height:1.2;">
            <b>Macro:</b> {macro}<br/>
            <b>Proceso:</b> {proc}<br/>
            <b>Líder:</b> {lider}
        </div>
        """

        normas_raw = o.get("normas_relacionadas", "")
        normas_html = '<div style="font-size:7pt; line-height:1.2;">'
        if isinstance(normas_raw, list):
            for n in normas_raw:
                if isinstance(n, dict):
                    normas_html += f"• {n.get('norma','')} ({n.get('clasificacion','')})<br/>"
                else:
                    normas_html += f"• {str(n)}<br/>"
        elif normas_raw:
            normas_html += f"{str(normas_raw)}"
        else:
            normas_html += "No especificado"
        normas_html += "</div>"

        row_bg = "#F4F7FF" if i % 2 == 0 else "#FFFFFF"
        obs_rows_html += f"""
        <tr style="background:{row_bg}; page-break-inside:avoid;
                   border-left:4px solid {bg_tipo};">
            <td style="padding:7px 5px;border:1px solid #E7E7E7;vertical-align:top;
                       font-weight:bold;color:{bg_tipo};font-size:8pt;
                       text-align:center;width:25px;">{i}</td>
            <td style="padding:7px 5px;border:1px solid #E7E7E7;vertical-align:top;
                       font-size:7pt;width:60px;">{o.get('numeral_articulo','N/A')}</td>
            <td style="padding:7px 5px;border:1px solid #E7E7E7;vertical-align:top;
                       font-size:7pt;">{o.get('texto_obligacion','N/A')}</td>
            <td style="padding:7px 5px;border:1px solid #E7E7E7;vertical-align:top;
                       width:75px;">{_badge_tipo(tipo)}</td>
            <td style="padding:7px 5px;border:1px solid #E7E7E7;vertical-align:top;
                       font-size:7pt;width:90px;">{_badge_frecuencia(
                           o.get('frecuencia',''),
                           fecha_pub=dg.get('fecha_publicacion',''),
                           vigencia_desde=o.get('vigencia_desde',''))}</td>
            <td style="padding:7px 5px;border:1px solid #E7E7E7;vertical-align:top;
                       width:180px;">{proceso_html}</td>
            <td style="padding:7px 5px;border:1px solid #E7E7E7;vertical-align:top;
                       width:160px;">{normas_html}</td>
            <td style="padding:7px 5px;border:1px solid #E7E7E7;vertical-align:top;
                       font-size:7pt;width:100px;">{o.get('entregable','No especificado')}</td>
        </tr>"""

    temas_str = ", ".join(dg.get('temas', [])) if isinstance(dg.get('temas'), list) else str(dg.get('temas', ''))
    companias_str = ", ".join(dg.get('companias_impactadas', [])) if isinstance(dg.get('companias_impactadas'), list) else str(dg.get('companias_impactadas', ''))
    obs_html_blocks = obs_rows_html  # alias for backward compat

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            @font-face {{
                font-family: 'Sura Sans';
                src: url('file:///Users/cmotalvaro/.gemini/config/skills/sura-brand-ui/assets/fonts/SuraSans-Variable.ttf');
            }}
            @page {{
                size: A4 landscape;
                margin: 1.5cm 1.8cm;
                @frame footer_frame {{
                    -pdf-frame-content: footer_content;
                    left: 1.8cm; right: 1.8cm; bottom: 0.8cm; height: 0.8cm;
                }}
            }}
            body {{
                font-family: 'Sura Sans', Helvetica, Arial, sans-serif;
                color: #3F3F41;
                font-size: 8.5pt;
                line-height: 1.4;
            }}
            .header-bar {{
                width: 100%;
                border-collapse: collapse;
                border-bottom: 3px solid #0033A0;
                margin-bottom: 14px;
            }}
            .page-title {{
                color: #0033A0;
                font-size: 15pt;
                font-weight: bold;
            }}
            .page-subtitle {{ color: #888B8D; font-size: 9pt; }}
            .meta-table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 18px;
            }}
            .meta-table td {{
                padding: 5px 7px;
                border: 1px solid #E7E7E7;
                font-size: 8pt;
            }}
            .meta-label {{
                font-weight: bold;
                color: #FFFFFF;
                background-color: #0033A0;
                width: 130px;
                white-space: nowrap;
            }}
            h2 {{
                color: #0033A0;
                font-size: 10pt;
                border-bottom: 2px solid #0033A0;
                padding-bottom: 3px;
                margin-top: 16px;
                margin-bottom: 8px;
            }}
            .master-table {{
                width: 100%;
                border-collapse: collapse;
            }}
            .master-table thead th {{
                background-color: #0033A0;
                color: #FFFFFF;
                font-size: 7.5pt;
                font-weight: bold;
                padding: 6px 7px;
                border: 1px solid #002580;
                text-align: left;
            }}
            #footer_content {{
                text-align: right;
                font-size: 7pt;
                color: #888B8D;
                border-top: 1px solid #E7E7E7;
                padding-top: 3px;
            }}
        </style>
    </head>
    <body>
        <div id="footer_content">Página <pdf:pagenumber> de <pdf:pagecount> — {dg.get('norma', 'N/A')} · SURA Cumplimiento Normativo</div>

        <table class="header-bar">
            <tr>
                <td style="padding-bottom:8px;">
                    <img src="{SRC_ROOT}/static/sura-logo-azul.png" style="width:120px;margin-bottom:5px;" />
                    <div class="page-title">Análisis de Cumplimiento Normativo</div>
                    <div class="page-subtitle">Extracción de Obligaciones Regulatorias</div>
                </td>
            </tr>
        </table>

        <h2>Datos Generales del Documento</h2>
        <table class="meta-table">
            <tr>
                <td class="meta-label">Norma</td>
                <td>{dg.get('norma', 'N/A')}</td>
                <td class="meta-label">Emisor</td>
                <td>{dg.get('emisor', 'N/A')}</td>
            </tr>
            <tr>
                <td class="meta-label">Tipo</td>
                <td>{dg.get('tipo_norma', 'N/A')}</td>
                <td class="meta-label">Fecha</td>
                <td>{dg.get('fecha_publicacion', 'N/A')}</td>
            </tr>
            <tr>
                <td class="meta-label">Temas</td>
                <td colspan="3">{temas_str}</td>
            </tr>
            <tr>
                <td class="meta-label">Compañías Impactadas</td>
                <td colspan="3">{companias_str}</td>
            </tr>
            <tr>
                <td class="meta-label">Incidencia SURA</td>
                <td colspan="3">{dg.get('incidencia_sura', 'N/A')}</td>
            </tr>
            <tr>
                <td class="meta-label">Control SOX</td>
                <td>{dg.get('control_sox', 'N/A')}</td>
                <td class="meta-label">Divulgación SOX</td>
                <td>{dg.get('divulgacion_sox', 'N/A')}</td>
            </tr>
        </table>

        <h2>Obligaciones Identificadas ({len(obs)})</h2>
        <table class="master-table">
            <thead>
                <tr>
                    <th style="width:25px;">#</th>
                    <th style="width:60px;">Artículo</th>
                    <th>Texto de la Obligación</th>
                    <th style="width:75px;">Tipo</th>
                    <th style="width:90px;">Plazo / Vigencia</th>
                    <th style="width:190px;">Proceso Responsable</th>
                    <th style="width:155px;">Normas Relacionadas</th>
                    <th style="width:100px;">Entregable</th>
                </tr>
            </thead>
            <tbody>
                {obs_rows_html}
            </tbody>
        </table>

    </body>
    </html>
    """

    pdf_io = io.BytesIO()
    pisa_status = pisa.CreatePDF(html_content, dest=pdf_io)
    
    if pisa_status.err:
        return jsonify({'error': 'Error generating PDF'}), 500

    pdf_io.seek(0)
    return send_from_directory(
        os.path.dirname(SEMAFORO_FILE), # Solo para usar send_from_directory de manera segura, o usar flask.send_file
        'tablero_semaforo.csv', # fallback
        as_attachment=True,
        attachment_filename='analisis.pdf',
        mimetype='application/pdf'
    ) if False else flask_send_file_fallback(pdf_io)

def flask_send_file_fallback(pdf_io):
    from flask import send_file
    return send_file(pdf_io, mimetype='application/pdf', as_attachment=True, download_name='Analisis_Obligaciones.pdf')


# ─── Mapa Mental por Norma ────────────────────────────────────────────────────

@app.route('/mapa-norma', methods=['GET', 'POST'])
def mapa_norma():
    """Renderiza el mapa mental interactivo de una norma analizada."""
    if request.method == 'POST':
        data = request.get_json()
        resultado = data.get('resultado', {})
        app.config['_ultimo_mapa_norma'] = resultado
        return jsonify({'ok': True, 'redirect': '/mapa-norma'})

    wiki_file = request.args.get('wiki_file')
    if wiki_file:
        # Intentar cargar desde el archivo Markdown guardado
        wiki_dir = os.path.join(ROOT, "wiki", "analyses")
        filepath = os.path.join(wiki_dir, wiki_file)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parsear frontmatter e identificaciones
                resultado = {
                    'datos_generales': {},
                    'obligaciones': []
                }
                
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        frontmatter = parts[1]
                        # Título, emisor, etc
                        for line in frontmatter.split('\n'):
                            if ':' in line:
                                k, v = line.split(':', 1)
                                k = k.strip()
                                v = v.strip().strip('"').strip("'")
                                if k == 'title':
                                    resultado['datos_generales']['norma'] = v.replace('Análisis: ', '')
                                elif k == 'source_files':
                                    # Extraer la fuente
                                    sf_match = re.search(r'\["(.*?)"\]', v)
                                    if sf_match:
                                        resultado['datos_generales']['_fuente'] = sf_match.group(1)
                                        resultado['_fuente'] = sf_match.group(1)
                        
                        # Intentar parsear los datos generales de la tabla Markdown
                        body = parts[2]
                        dg_section = re.search(r'## Datos Generales de la Norma\s*\n\n(.*?)(?=\n\n##|$)', body, re.DOTALL)
                        if dg_section:
                            for row in dg_section.group(1).split('\n'):
                                if '| **' in row:
                                    # Formato: | **Título** | Valor |
                                    rparts = [p.strip() for p in row.split('|') if p.strip()]
                                    if len(rparts) >= 2:
                                        label = rparts[0].replace('**', '').strip()
                                        value = rparts[1]
                                        label_map = {
                                            'Título': 'titulo', 'Emisor': 'emisor', 'Tipo de Norma': 'tipo_norma',
                                            'Fecha de Publicación': 'fecha_publicacion', 'Jurisdicción': 'jurisdiccion',
                                            'Incidencia SURA': 'incidencia_sura', 'Control SOX': 'control_sox',
                                            'Divulgación SOX': 'divulgacion_sox', 'Anexos': 'anexos'
                                        }
                                        if label in label_map:
                                            resultado['datos_generales'][label_map[label]] = value
                        
                        # Parsear las obligaciones de los bloques markdown
                        # ### Obligación {i} — {numeral}
                        # Seguido de una tabla con sus campos
                        obl_matches = re.finditer(r'### Obligación \d+ — (.*?)\n(.*?)(?=\n### Obligación \d+ — |\n## Caveats|\n##|$)', body, re.DOTALL)
                        for m in obl_matches:
                            numeral = m.group(1).strip()
                            table_content = m.group(2).strip()
                            ob = {'numeral_articulo': numeral}
                            for row in table_content.split('\n'):
                                if '| **' in row:
                                    rparts = [p.strip() for p in row.split('|') if p.strip()]
                                    if len(rparts) >= 2:
                                        label = rparts[0].replace('**', '').strip()
                                        value = rparts[1]
                                        label_map = {
                                            'Texto': 'texto_obligacion', 'Frecuencia': 'frecuencia',
                                            'Entregable': 'entregable', 'Normas relacionadas': 'normas_relacionadas',
                                            'Macroproceso': 'macroproceso', 'Proceso': 'proceso', 'Líder': 'lider_proceso'
                                        }
                                        if label in label_map:
                                            ob[label_map[label]] = value
                            
                            # Obtener tipo_obligacion a partir de la lógica del backend basándose en el texto
                            # O usar un mapeo simple. Mapear verbos clave o dejar general
                            ob['tipo_obligacion'] = 'General'
                            txt_low = ob.get('texto_obligacion', '').lower()
                            verb_map = {
                                'Reportar': ['reportar', 'notificar', 'remitir', 'presentar', 'enviar', 'declarar'],
                                'Pagar': ['pagar', 'liquidar', 'desembolsar', 'transferir', 'financiar', 'costear'],
                                'Implementar': ['implementar', 'adoptar', 'crear', 'establecer', 'diseñar', 'desarrollar'],
                                'Controlar': ['controlar', 'monitorear', 'evaluar', 'auditar', 'supervisar', 'vigilar'],
                                'Documentar': ['documentar', 'registrar', 'archivar', 'conservar', 'guardar'],
                                'Autorizar': ['autorizar', 'aprobar', 'permitir', 'licenciar', 'validar'],
                                'Capacitar': ['capacitar', 'entrenar', 'formar', 'instruir', 'educar'],
                                'Prohibición': ['prohibir', 'prohíbe', 'prohibido', 'abstenerse', 'no podrá'],
                                'Divulgar': ['divulgar', 'publicar', 'comunicar', 'difundir', 'informar'],
                                'Garantizar': ['garantizar', 'asegurar', 'proteger', 'salvaguardar', 'mantener'],
                                'Actualizar': ['actualizar', 'modificar', 'ajustar', 'renovar', 'corregir']
                            }
                            found_tipo = False
                            for t, words in verb_map.items():
                                if any(w in txt_low for w in words):
                                    ob['tipo_obligacion'] = t
                                    found_tipo = True
                                    break
                            
                            resultado['obligaciones'].append(ob)
                
                return render_template('mapa_norma.html', resultado=resultado)
            except Exception:
                pass

    resultado = app.config.get('_ultimo_mapa_norma', {})
    return render_template('mapa_norma.html', resultado=resultado)


if __name__ == '__main__':
    print(f"[app] iniciando | root={ROOT}")
    print(f"[app] casos={CASOS_FILE}")
    print(f"[app] semaforo={SEMAFORO_FILE}")
    print(f"[app] server en http://localhost:5050")
    app.run(debug=False, host='localhost', port=5050)
