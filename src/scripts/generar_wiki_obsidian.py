
import csv
import os
import re
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
CASES_FILE = os.path.join(ROOT, 'data', 'casos_detectados.csv')
WIKI_DIR = os.path.join(ROOT, 'wiki')

def safe_filename(name):
    # Quitar caracteres prohibidos y limitar longitud
    clean = re.sub(r'[\\/*?:"<>|]', '', str(name)).strip()
    return clean[:100] # Limitar para evitar errores de SO

def create_note(folder, title, content, properties):
    os.makedirs(os.path.join(WIKI_DIR, folder), exist_ok=True)
    path = os.path.join(WIKI_DIR, folder, f"{safe_filename(title)}.md")
    
    header = "---\n"
    for k, v in properties.items():
        header += f"{k}: {v}\n"
    header += "---\n\n"
    
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            try:
                # Buscar el final del frontmatter
                indices = [i for i, x in enumerate(lines) if x == "---\n"]
                if len(indices) >= 2:
                    body = "".join(lines[indices[1]+1:])
                else:
                    body = "".join(lines)
            except:
                body = "".join(lines)
    else:
        body = content

    with open(path, 'w', encoding='utf-8') as f:
        # Siempre escribimos el header nuevo (actualiza tags) + el cuerpo existente
        f.write(header + body)

def main():
    if not os.path.exists(CASES_FILE):
        return

    with open(CASES_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        # Usamos un generador para limpiar bytes nulos que rompen el lector de CSV
        clean_lines = (line.replace('\0', '') for line in f)
        reader = csv.DictReader(clean_lines)
        processed_titles = set()
        for row in reader:
            entidad = (row.get('entidad') or row.get('Emisor') or '').strip()
            if not entidad: continue

            # 1. Nota de Entidad
            create_note('entidades', entidad, f"## Descripción\nInformación sobre {entidad}.\n", {
                'type': 'entity',
                'tags': '[entidad]',
                'updated': datetime.now().strftime('%Y-%m-%d')
            })

            # 2. Nota de Caso/Norma
            entidad_clean = safe_filename(entidad)[:25]
            fecha = row.get('detected_at', '')[:10]
            tipo = row.get('Tipo de Norma') or "Norma"
            
            # Prioridad de nombres para el archivo
            if row.get('Título') and len(row.get('Título')) < 80:
                base_name = f"{tipo} - {row.get('Título')}"
            elif row.get('Norma'):
                base_name = f"{tipo} - {row.get('Norma')}"
            else:
                base_name = f"{tipo} - {entidad_clean} {fecha} {row.get('case_id')[:4]}"

            titulo = safe_filename(base_name)
            
            if titulo in processed_titles:
                titulo = f"{titulo}-{row.get('case_id')[:4]}"
            processed_titles.add(titulo)

            # --- LÓGICA DE TAGS Y PROPIEDADES OPTIMIZADA ---
            status_val = row.get('status', 'detectado').lower()
            tipo_val = tipo.lower().replace(' ', '_')
            riesgo = row.get('riesgo_sancionatorio', 'Bajo')
            divulgacion = row.get('Fecha de divulgación') or row.get('Divulgación SOX')
            
            # Tags: Solo para estados visuales importantes
            tags_list = []
            if status_val in ['validado', 'rechazado', 'consolidado']:
                tags_list.append(status_val)
            
            if row.get('Control SOX') == 'SÍ' or row.get('control_sox_sugerido') == 'SÍ':
                tags_list.append("sox")
            
            if riesgo in ['Crítico', 'Alto']:
                tags_list.append(f"riesgo_{riesgo.lower()}")
            
            if row.get('impacto_ti') == 'SÍ':
                tags_list.append("impacto_ti")
            
            # Marcado de PUBLICADO / EJECUTADO
            es_publicado = "SÍ" if (status_val == 'consolidado' or (divulgacion and divulgacion.strip())) else "NO"
            if es_publicado == "SÍ":
                tags_list.append("publicado")

            if "proyecto" in tipo_val or "agenda" in tipo_val:
                tags_list.append("en_tramite")
            elif tipo_val in ['ley', 'decreto', 'resolución', 'circular_externa']:
                tags_list.append("firmada")

            # Propiedades: Metadata rica para búsqueda [propiedad:valor]
            properties = {
                'case_id': row.get('case_id'),
                'tipo': tipo,
                'estado': status_val,
                'entidad': f"[[{entidad}]]",
                'linea_negocio': f"[[{row.get('linea_negocio') or 'Transversal'}]]",
                'riesgo': f"[[Riesgo {riesgo}]]",
                'impacto_ti': row.get('impacto_ti') or "NO",
                'ejecutado': es_publicado,
                'plazo': row.get('plazo_implementacion') or "No especificado",
                'tema': f"[[{row.get('Tema') or 'Sin clasificar'}]]",
                'sox': row.get('Control SOX') or "NO",
                'created': fecha,
                'published': row.get('Fecha de publicación') or 'No especificada',
                'tags': f"[{', '.join(tags_list)}]"
            }

            content = f"""## Detalles del Hallazgo
- **Entidad Emisora:** [[{entidad}]]
- **Línea de Negocio:** {properties['linea_negocio']}
- **Tipo de Norma:** {tipo}
- **Fecha de Expedición:** {properties['published']}
- **Riesgo Sancionatorio:** {properties['riesgo']}
- **Plazo de Implementación:** {properties['plazo']}
- **URL:** {row.get('document_url')}
- **Control SOX:** {properties['sox']}

## Análisis Jurídico
> **Tema Central:** [[{row.get('Tema') or 'Sin clasificar'}]]

{row.get('notes') or 'Pendiente de análisis detallado por el equipo legal.'}

## Acciones de Cumplimiento
- [ ] Analizar impacto en procesos de {properties['linea_negocio']}
- [ ] Verificar si requiere actualización de Control SOX: {properties['sox']}
- [ ] Fecha límite estimada: {properties['plazo']}

## Responsables Sugeridos
- [[Líder de Cumplimiento Normativo]]
- [[Responsable de {row.get('linea_negocio') or 'Transversal'}]]
"""
            create_note('casos', titulo, content, properties)

            # 3. Nota de Tema
            tema = row.get('Tema')
            if tema:
                create_note('temas', tema, f"## Normativa Relacionada\nConceptos y normas sobre [[{tema}]].\n", {
                    'type': 'concept',
                    'updated': datetime.now().strftime('%Y-%m-%d')
                })

if __name__ == '__main__':
    main()
