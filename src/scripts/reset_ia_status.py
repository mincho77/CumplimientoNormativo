import csv
import os
import shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
CASES_FILE = os.path.join(ROOT, 'data', 'casos_detectados.csv')

def reset_ia_analysis():
    if not os.path.exists(CASES_FILE):
        print("❌ Error: No se encontró el archivo de casos.")
        return

    temp_file = CASES_FILE + '.tmp'
    count = 0

    with open(CASES_FILE, 'r', encoding='utf-8', errors='ignore', newline='') as f_in, \
         open(temp_file, 'w', encoding='utf-8', newline='') as f_out:
        
        # Limpiar bytes nulos que rompen el lector de CSV
        clean_lines = (line.replace('\0', '') for line in f_in)
        reader = csv.DictReader(clean_lines)
        writer = csv.DictWriter(f_out, fieldnames=reader.fieldnames)
        writer.writeheader()
        
        for row in reader:
            # Solo reseteamos los que tienen un archivo PDF en inbox
            pdf_path = os.path.join(ROOT, 'raw', 'inbox', f"{row['case_id']}.pdf")
            if os.path.exists(pdf_path):
                row['analisis_ia_status'] = 'pendiente'
                row['analisis_ia_fecha'] = ''
                count += 1
            writer.writerow(row)
            
    shutil.move(temp_file, CASES_FILE)
    print(f"✅ Se han reseteado {count} casos para re-análisis con el nuevo modelo experto.")

if __name__ == '__main__':
    reset_ia_analysis()
