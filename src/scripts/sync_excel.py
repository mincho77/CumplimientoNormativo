import pandas as pd
import os
import hashlib
from urllib.parse import urlparse

def normalize_url(url):
    if pd.isna(url) or not isinstance(url, str):
        return ""
    url = url.strip().lower()
    parsed = urlparse(url)
    path = parsed.path.rstrip('/')
    normalized = f"{parsed.scheme}://{parsed.netloc}{path}"
    if parsed.query:
        normalized += f"?{parsed.query}"
    return normalized

def clean_string(s):
    if pd.isna(s):
        return ""
    return str(s).strip()

def main():
    excel_path = "/Users/cmotalvaro/Downloads/Seguimiento Regulatorio - 2026 1.xlsm"
    csv_path = "data/casos_detectados.csv"
    
    print(f"Sincronizando datos extendidos desde Excel: {excel_path}...")
    
    try:
        df_excel = pd.read_excel(excel_path, sheet_name='Seguimiento')
    except Exception as e:
        print(f"Error al leer Excel: {e}")
        return

    if not os.path.exists(csv_path):
        print(f"Aviso: No se encuentra {csv_path}. Se creará uno nuevo.")
        df_csv = pd.DataFrame(columns=['case_id', 'URL', 'url_norm'])
    else:
        df_csv = pd.read_csv(csv_path)
        df_csv['url_norm'] = df_csv['URL'].apply(normalize_url)

    # Normalizar URLs del Excel
    df_excel['url_norm'] = df_excel['URL'].apply(normalize_url)

    # Todas las columnas del Excel que queremos en el CSV
    columnas_excel = [
        'Resultado análisis', 'Fecha registro', 'Tipo', 'Título', 'URL', 'Anexos', 
        'Fecha de publicación', 'Emisor', 'Norma', 'Fecha de divulgación', 
        'Tipo de Norma', 'Tema', 'Sector Económico', 'Incidencia SURA', 
        'Obligaciones SURA', 'Norma Importante', 'Control SOX', 'Divulgación SOX', 
        'Compañía Impactada', 'Obligaciones', 'Persona que analizó', 
        'Justificación de no divulgación SOX'
    ]

    # Asegurar que todas las columnas existan en el CSV
    for col in columnas_excel:
        if col not in df_csv.columns:
            df_csv[col] = ""
    if 'sincronizado_excel' not in df_csv.columns:
        df_csv['sincronizado_excel'] = False

    # Mapeo de datos del Excel (URL -> Datos)
    excel_data_map = df_excel.dropna(subset=['url_norm']).drop_duplicates('url_norm', keep='last').set_index('url_norm')

    count_sync = 0
    for idx, row in df_csv.iterrows():
        url = row['url_norm']
        if url in excel_data_map.index:
            excel_row = excel_data_map.loc[url]
            
            # 1. Sincronizar campos
            for col in columnas_excel:
                val = excel_row[col]
                if pd.notna(val):
                    # Convertir fechas a string para el CSV
                    if 'Fecha' in col and not isinstance(val, str):
                        try:
                            val = val.strftime('%Y-%m-%d')
                        except:
                            val = str(val)
                    df_csv.at[idx, col] = val
            
            # 2. Lógica de Status basada en Divulgación
            res_analisis = clean_string(excel_row['Resultado análisis']).lower()
            fecha_div = clean_string(excel_row['Fecha de divulgación'])
            
            # Si tiene fecha de divulgación o el resultado es "Divulgar" y NO está vacío (heurística para ya hecho)
            # Pero el usuario dice: "si dice divulgado no debería aparecer esa alerta porque ya está consolidado"
            # En el Excel vimos 'Divulgar' y 'No divulgar'. 
            # Si Fecha de divulgación tiene dato -> Consolidado
            if fecha_div != "" and fecha_div != "nan":
                df_csv.at[idx, 'status'] = 'consolidado'
            elif res_analisis == 'no divulgar' or 'repetida' in res_analisis:
                df_csv.at[idx, 'status'] = 'rechazado'
                df_csv.at[idx, 'aplica_sura'] = 'NO'
            elif res_analisis == 'divulgar':
                # Si dice Divulgar pero no tiene fecha, sigue siendo un impacto pendiente (ROJO)
                df_csv.at[idx, 'status'] = 'validado' 
                df_csv.at[idx, 'aplica_sura'] = 'SÍ'
            
            df_csv.at[idx, 'sincronizado_excel'] = True
            count_sync += 1

    # Importar registros nuevos del Excel
    excel_only = df_excel[~df_excel['url_norm'].isin(df_csv['url_norm'])]
    print(f"Registros en Excel no detectados por monitor: {len(excel_only)}")
    
    new_rows = []
    for _, xrow in excel_only.iterrows():
        if pd.isna(xrow['URL']): continue
        cid = hashlib.sha256(f"IMPORT|{xrow['URL']}".encode()).hexdigest()[:16]
        
        # Determinar status para importados
        fecha_div = clean_string(xrow['Fecha de divulgación'])
        res_analisis = clean_string(xrow['Resultado análisis']).lower()
        
        status = 'importado_excel'
        aplica = ""
        if fecha_div != "" and fecha_div != "nan":
            status = 'consolidado'
            aplica = "SÍ"
        elif res_analisis == 'no divulgar' or 'repetida' in res_analisis:
            status = 'rechazado'
            aplica = "NO"
        elif res_analisis == 'divulgar':
            status = 'validado'
            aplica = "SÍ"

        new_row = {
            'case_id': cid,
            'detected_at': '2026-05-29 00:00:00-0500',
            'status': status,
            'aplica_sura': aplica,
            'entidad': xrow['Emisor'], # Asegurar que entidad tenga valor para agrupar
            'url_norm': xrow['url_norm'],
            'sincronizado_excel': True
        }
        
        for col in columnas_excel:
            val = xrow[col]
            if pd.notna(val):
                if 'Fecha' in col and not isinstance(val, str):
                    try: val = val.strftime('%Y-%m-%d')
                    except: val = str(val)
                new_row[col] = val
            else:
                new_row[col] = ""

        # Llenar el resto con vacío
        for col in df_csv.columns:
            if col not in new_row:
                new_row[col] = ""
        new_rows.append(new_row)

    if new_rows:
        df_csv = pd.concat([df_csv, pd.DataFrame(new_rows)], ignore_index=True)
        print(f"Importados {len(new_rows)} registros nuevos.")

    df_csv.drop(columns=['url_norm']).to_csv(csv_path, index=False)
    print(f"Sincronización completada. {count_sync} registros actualizados.")

if __name__ == "__main__":
    main()
