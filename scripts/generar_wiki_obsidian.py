
import csv
import os
import re
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
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
        f.write(header + body)

def main():
    if not os.path.exists(CASES_FILE):
        return

    with open(CASES_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
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
            
            # Prioridad de nombres para el archivo: "TIPO - Entidad - Fecha - ID"
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

            # Definir etiquetas para colores en Obsidian
            status_tag = row.get('status', 'detectado').lower()
            tipo_tag = tipo.lower().replace(' ', '_')
            sox_tag = "sox" if row.get('Control SOX') == 'SÍ' else "no_sox"
            
            tags_list = ["normativa", status_tag, tipo_tag, sox_tag]
            if "proyecto" in tipo_tag:
                tags_list.append("en_tramite")
            else:
                tags_list.append("firmada")

            case_id = row.get('case_id')
            fecha_pub = row.get('Fecha de publicación') or 'No especificada'
            content = f"""## Detalles del Hallazgo
- **Entidad Emisora:** [[{entidad}]]
- **Tipo de Norma:** {tipo}
- **Fecha de Expedición:** {fecha_pub}
- **Fecha de Detección:** {fecha}
- **URL:** {row.get('document_url')}
- **Incidencia SURA:** {row.get('Incidencia SURA')}
- **Control SOX:** {row.get('Control SOX')}

## Análisis
{row.get('notes') or 'Pendiente de análisis detallado.'}
"""
            create_note('casos', titulo, content, {
                'case_id': case_id,
                'type': 'source',
                'status': status_tag,
                'entidad': f"[[{entidad}]]",
                'created': fecha,
                'published': fecha_pub,
                'tags': f"[{', '.join(tags_list)}]"
            })

            # 3. Nota de Tema
            tema = row.get('Tema')
            if tema:
                create_note('temas', tema, f"## Normativa Relacionada\nConceptos y normas sobre [[{tema}]].\n", {
                    'type': 'concept',
                    'tags': '[tema]'
                })

if __name__ == '__main__':
    main()
