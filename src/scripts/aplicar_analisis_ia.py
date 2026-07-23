
import csv
import os
import json
from datetime import datetime, timezone, timedelta

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
CASES_FILE = os.path.join(ROOT, 'data', 'casos_detectados.csv')
COLOMBIA_TZ = timezone(timedelta(hours=-5))

def apply_analysis(results):
    """
    results: list of dicts with {case_id, tema, incidencia, obligaciones, linea_negocio, impacto_ti, etc}
    """
    temp_file = CASES_FILE + '.tmp'
    updated_count = 0
    
    with open(CASES_FILE, 'r', encoding='utf-8', newline='') as f_in, \
         open(temp_file, 'w', encoding='utf-8', newline='') as f_out:
        
        reader = csv.DictReader(f_in)
        fieldnames = list(reader.fieldnames)
        
        # Nuevas columnas para el modelo SURA avanzado
        nuevas_columnas = [
            'tokens_ia', 'linea_negocio', 'impacto_ti', 
            'riesgo_sancionatorio', 'plazo_implementacion', 'control_sox_sugerido'
        ]
        for col in nuevas_columnas:
            if col not in fieldnames:
                fieldnames.append(col)
            
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            res = next((r for r in results if r['case_id'] == row['case_id']), None)
            if res:
                row['Tema'] = res.get('tema', row['Tema'])
                
                # Manejo inteligente de la entidad
                entidad_real = res.get('entidad_real', '')
                if entidad_real and entidad_real.lower() != 'desconocida':
                    row['Emisor'] = row['entidad']
                    row['entidad'] = entidad_real
                
                fecha_pub = res.get('fecha_publicacion', '')
                if fecha_pub and fecha_pub.lower() != 'no especificada':
                    row['Fecha de publicación'] = fecha_pub
                elif not row.get('Fecha de publicación'):
                    row['Fecha de publicación'] = row.get('detected_at', '')[:10]
                        
                row['Incidencia SURA'] = res.get('incidencia', row['Incidencia SURA'])
                row['Obligaciones'] = res.get('obligaciones', row['Obligaciones'])
                row['tokens_ia'] = res.get('tokens_ia', row.get('tokens_ia', '0'))
                
                # Guardar nuevas variables SURA
                row['linea_negocio'] = res.get('linea_negocio', row.get('linea_negocio', ''))
                row['impacto_ti'] = res.get('impacto_ti', row.get('impacto_ti', ''))
                row['riesgo_sancionatorio'] = res.get('riesgo_sancionatorio', row.get('riesgo_sancionatorio', ''))
                row['plazo_implementacion'] = res.get('plazo_implementacion', row.get('plazo_implementacion', ''))
                row['control_sox_sugerido'] = res.get('control_sox_sugerido', row.get('control_sox_sugerido', ''))

                row['analisis_ia_status'] = 'procesado'
                row['analisis_ia_fecha'] = datetime.now(COLOMBIA_TZ).strftime('%Y-%m-%d %H:%M')
                row['Resultado análisis'] = f"IA [{row['riesgo_sancionatorio']}]: " + res.get('resumen', '')[:100]
                updated_count += 1
            writer.writerow(row)
            
    import shutil
    shutil.move(temp_file, CASES_FILE)
    
    # Regenerar otros archivos
    import subprocess
    subprocess.run(['python3', os.path.join(ROOT, 'src', 'scripts', 'generar_tablero_semaforo.py')])
    subprocess.run(['python3', os.path.join(ROOT, 'src', 'scripts', 'generar_wiki_obsidian.py')])
    
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
