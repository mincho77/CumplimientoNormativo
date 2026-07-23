import csv
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
CASES_FILE = os.path.join(ROOT, 'data', 'casos_detectados.csv')

def audit_data():
    anomalies = {
        'riesgo_alto_sin_incidencia': [],
        'sox_incoherente': [],
        'consolidados_incompletos': [],
        'no_aplica_dudoso': []
    }

    with open(CASES_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        clean_lines = (line.replace('\0', '') for line in f)
        reader = csv.DictReader(clean_lines)
        
        for row in reader:
            cid = row.get('case_id')
            titulo = row.get('Título') or row.get('Tema') or 'Sin título'
            incidencia = str(row.get('Incidencia SURA')).strip().upper()
            status = str(row.get('status')).strip().lower()
            riesgo = str(row.get('riesgo_sancionatorio')).strip().upper()
            sox = str(row.get('Control SOX')).strip().upper()
            
            # 1. Riesgo Crítico/Alto pero clasificado como "NO aplica"
            if riesgo in ['CRÍTICO', 'ALTO'] and incidencia == 'NO':
                anomalies['riesgo_alto_sin_incidencia'].append(f"{cid} | {riesgo} | {titulo[:60]}")
                
            # 2. Control SOX marcado como SÍ, pero Incidencia es NO
            if sox == 'SÍ' and incidencia == 'NO':
                anomalies['sox_incoherente'].append(f"{cid} | {titulo[:60]}")
                
            # 3. Consolidados (Archivados/Publicados) que dicen que NO tienen incidencia
            if status == 'consolidado' and incidencia == 'NO':
                anomalies['consolidados_incompletos'].append(f"{cid} | {titulo[:60]}")
                
            # 4. Clasificado en VERDE (Cumplido/No aplica) pero tiene alto riesgo
            if status == 'verde' and riesgo in ['CRÍTICO', 'ALTO']:
                anomalies['no_aplica_dudoso'].append(f"{cid} | {riesgo} | {titulo[:60]}")

    print("=== REPORTE DE AUDITORÍA LEGAL ===")
    print(f"1. Falsos Negativos (Riesgo Alto/Crítico pero Incidencia 'NO'): {len(anomalies['riesgo_alto_sin_incidencia'])}")
    for a in anomalies['riesgo_alto_sin_incidencia'][:5]: print(f"   - {a}")
    
    print(f"\n2. Incoherencia SOX (Aplica SOX pero Incidencia 'NO'): {len(anomalies['sox_incoherente'])}")
    for a in anomalies['sox_incoherente'][:5]: print(f"   - {a}")
    
    print(f"\n3. Consolidados Contradictorios (Están en matriz final pero Incidencia 'NO'): {len(anomalies['consolidados_incompletos'])}")
    for a in anomalies['consolidados_incompletos'][:5]: print(f"   - {a}")
    
    print(f"\n4. Cumplidos ('Verdes') con Riesgo Sancionatorio detectado: {len(anomalies['no_aplica_dudoso'])}")
    for a in anomalies['no_aplica_dudoso'][:5]: print(f"   - {a}")

if __name__ == '__main__':
    audit_data()
