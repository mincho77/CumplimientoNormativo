#!/usr/bin/env python3
"""
Compliance Monitoring Dashboard - Flask App
Reads casos_detectados.csv and tablero_semaforo.csv
"""
import os
import csv
import json
from datetime import datetime, timezone, timedelta
from urllib.parse import unquote
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Habilitar CORS para túneles externos
COLOMBIA_TZ = timezone(timedelta(hours=-5))
ROOT = os.path.abspath(os.path.dirname(__file__))
CASOS_FILE = os.path.join(ROOT, 'data', 'casos_detectados.csv')
SEMAFORO_FILE = os.path.join(ROOT, 'data', 'tablero_semaforo.csv')

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
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def get_summary():
    """Get count summary by semaforo and total tokens."""
    casos = read_csv(SEMAFORO_FILE)
    summary = {'ROJO': 0, 'AMARILLO': 0, 'VERDE': 0, 'CONSOLIDADO': 0, 'TOTAL_TOKENS': 0}
    for caso in casos:
        semaforo = caso.get('semaforo', '').upper()
        if semaforo in summary:
            summary[semaforo] += 1
        
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
    
    # Filtrar todos los documentos de esa fuente específica
    documentos = [c for c in casos if c.get('fuente_url') == fuente]
    
    return render_template('detalle.html', 
                         fuente=fuente, 
                         entidad=entidad, 
                         documentos=documentos)

@app.route('/analytics')
def analytics():
    """Route for the analytics and charts page."""
    return render_template('analytics.html')


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
                tipo = "📄" if "DOC" in line else "🔗"
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
        mes_str = c.get('analisis_ia_fecha', '')[:7] # YYYY-MM
        
        if not fecha_str:
            fecha_str = c.get('detected_at', '')[:10]
            mes_str = c.get('detected_at', '')[:7]
            
        if not fecha_str:
            fecha_str = 'Desconocida'
            mes_str = 'Desconocido'
            
        stats['total'] += tokens
        
        stats['by_entity'][entidad] = stats['by_entity'].get(entidad, 0) + tokens
        stats['by_date'][fecha_str] = stats['by_date'].get(fecha_str, 0) + tokens
        stats['by_month'][mes_str] = stats['by_month'].get(mes_str, 0) + tokens
        
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
            
    return jsonify(casos)


@app.route('/api/summary')
def api_summary():
    """API endpoint for summary."""
    return jsonify(get_summary())


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
            subprocess.run(['python3', 'scripts/generar_tablero_semaforo.py'], check=True)
            subprocess.run(['python3', 'scripts/generar_wiki_obsidian.py'], check=True)
            subprocess.run(['python3', 'scripts/generar_kanban.py'], check=True)
        except Exception as e:
            print(f"Error regenerando: {e}")
        
        return jsonify({'status': 'success'})
    else:
        os.remove(temp_file)
        return jsonify({'error': 'Case not found'}), 404

if __name__ == '__main__':
    print(f"[app] iniciando | root={ROOT}")
    print(f"[app] casos={CASOS_FILE}")
    print(f"[app] semaforo={SEMAFORO_FILE}")
    print(f"[app] server en http://0.0.0.0:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)
