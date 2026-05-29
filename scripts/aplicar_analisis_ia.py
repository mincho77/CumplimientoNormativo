
import csv
import os
import json
from datetime import datetime, timezone, timedelta

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CASES_FILE = os.path.join(ROOT, 'data', 'casos_detectados.csv')
COLOMBIA_TZ = timezone(timedelta(hours=-5))

def apply_analysis(results):
    """
    results: list of dicts with {case_id, tema, incidencia, obligaciones, status_ia}
    """
    temp_file = CASES_FILE + '.tmp'
    updated_count = 0
    
    with open(CASES_FILE, 'r', encoding='utf-8', newline='') as f_in, \
         open(temp_file, 'w', encoding='utf-8', newline='') as f_out:
        
        reader = csv.DictReader(f_in)
        fieldnames = list(reader.fieldnames)
        if 'tokens_ia' not in fieldnames:
            fieldnames.append('tokens_ia')
            
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            res = next((r for r in results if r['case_id'] == row['case_id']), None)
            if res:
                row['Tema'] = res.get('tema', row['Tema'])
                
                # Manejo inteligente de la entidad
                entidad_real = res.get('entidad_real', '')
                if entidad_real and entidad_real.lower() != 'desconocida':
                    # Guardamos de dónde lo sacamos en 'Emisor', pero actualizamos la 'entidad' para los reportes
                    row['Emisor'] = row['entidad'] # El sitio web de origen
                    row['entidad'] = entidad_real # El verdadero autor de la norma
                
                # Manejo de la fecha de publicación vs detección
                fecha_pub = res.get('fecha_publicacion', '')
                if fecha_pub and fecha_pub.lower() != 'no especificada':
                    row['Fecha de publicación'] = fecha_pub
                else:
                    # Si no hay fecha en el documento, se asume la fecha en que lo vimos por primera vez
                    if not row.get('Fecha de publicación'):
                        row['Fecha de publicación'] = row.get('detected_at', '')[:10]
                        
                row['Incidencia SURA'] = res.get('incidencia', row['Incidencia SURA'])
                row['Obligaciones'] = res.get('obligaciones', row['Obligaciones'])
                row['tokens_ia'] = res.get('tokens_ia', row.get('tokens_ia', '0'))
                row['analisis_ia_status'] = 'procesado'
                row['analisis_ia_fecha'] = datetime.now(COLOMBIA_TZ).strftime('%Y-%m-%d %H:%M')
                row['Resultado análisis'] = "IA: " + res.get('obligaciones', '')[:50] + "..."
                updated_count += 1
            writer.writerow(row)
            
    import shutil
    shutil.move(temp_file, CASES_FILE)
    
    # Regenerar otros archivos
    import subprocess
    subprocess.run(['python3', 'scripts/generar_tablero_semaforo.py'])
    subprocess.run(['python3', 'scripts/generar_wiki_obsidian.py'])
    
    print(f"Análisis IA aplicado a {updated_count} documentos.")

if __name__ == '__main__':
    # Estos resultados los genero yo (la IA) basado en el texto leído
    demo_results = [
        {
            'case_id': '682492897c62c4e9',
            'tema': 'Hacienda Pública',
            'incidencia': 'parcial',
            'obligaciones': 'Informe detallado de la gestión presupuestal 2023-2024. Menciona entes de control como SFC y DIAN. Relevancia informativa para SURA.'
        },
        {
            'case_id': '4a289fceffda17b8',
            'tema': 'Presupuesto Público',
            'incidencia': 'NO',
            'obligaciones': 'Rendición de cuentas del periodo de José Antonio Ocampo. No genera obligaciones técnicas inmediatas para aseguradoras.'
        }
    ]
    apply_analysis(demo_results)
