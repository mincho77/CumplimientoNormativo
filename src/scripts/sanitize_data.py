import csv
import os
import shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
CASES_FILE = os.path.join(ROOT, 'data', 'casos_detectados.csv')

def sanitize():
    temp_file = CASES_FILE + '.tmp'
    fixed_sox = 0
    fixed_consolidado = 0

    with open(CASES_FILE, 'r', encoding='utf-8', errors='ignore', newline='') as f_in, \
         open(temp_file, 'w', encoding='utf-8', newline='') as f_out:
        
        clean_lines = (line.replace('\0', '') for line in f_in)
        reader = csv.DictReader(clean_lines)
        writer = csv.DictWriter(f_out, fieldnames=reader.fieldnames)
        writer.writeheader()
        
        for row in reader:
            incidencia = str(row.get('Incidencia SURA')).strip().upper()
            status = str(row.get('status')).strip().lower()
            sox = str(row.get('Control SOX')).strip().upper()
            
            # Regla 1: SOX incoherente
            if sox == 'SÍ' and incidencia == 'NO':
                row['Incidencia SURA'] = 'SÍ' # Lo pasamos a SÍ genérico, para que la alerta se levante
                fixed_sox += 1
                
            # Regla 2: Consolidados contradictorios
            if status == 'consolidado' and row.get('Incidencia SURA', '').strip().upper() == 'NO':
                row['status'] = 'verde' # Lo mandamos al archivo de "sin acción requerida"
                fixed_consolidado += 1
                
            writer.writerow(row)
            
    shutil.move(temp_file, CASES_FILE)
    print(f"✅ Saneamiento completado.")
    print(f"   - Casos SOX corregidos (Incidencia forzada a SÍ): {fixed_sox}")
    print(f"   - Casos Consolidados sin incidencia degradados a 'Verde': {fixed_consolidado}")

if __name__ == '__main__':
    sanitize()
