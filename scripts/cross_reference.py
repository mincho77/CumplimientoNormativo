import pandas as pd
import os
import re
from urllib.parse import urlparse

def normalize_url(url):
    if pd.isna(url) or not isinstance(url, str):
        return ""
    # Remove fragments, trailing slashes, and normalize scheme/host
    url = url.strip().lower()
    parsed = urlparse(url)
    # Reconstruct without fragment and trailing slash in path
    path = parsed.path.rstrip('/')
    normalized = f"{parsed.scheme}://{parsed.netloc}{path}"
    if parsed.query:
        normalized += f"?{parsed.query}"
    return normalized

def clean_string(s):
    if pd.isna(s) or not isinstance(s, str):
        return s
    # Remove illegal characters for Excel (control characters)
    return "".join(c for c in s if c.isprintable())

def main():
    excel_path = "/Users/cmotalvaro/Downloads/Seguimiento Regulatorio - 2026 1.xlsm"
    csv_cases_path = "data/casos_detectados.csv"
    csv_tablero_path = "data/tablero_semaforo.csv"
    output_path = "data/cruce_seguimiento.xlsx"

    print(f"Leyendo Excel: {excel_path}...")
    try:
        df_excel = pd.read_excel(excel_path, sheet_name='Seguimiento')
    except Exception as e:
        print(f"Error al leer Excel: {e}")
        return

    print(f"Leyendo CSVs del sistema...")
    df_csv = pd.read_csv(csv_cases_path)
    if os.path.exists(csv_tablero_path):
        df_tablero = pd.read_csv(csv_tablero_path)
        # Combine unique documents from both CSVs based on URL
        df_system = pd.concat([df_csv, df_tablero]).drop_duplicates(subset=['URL'])
    else:
        df_system = df_csv

    # Normalize URLs
    df_excel['url_norm'] = df_excel['URL'].apply(normalize_url)
    df_system['url_norm'] = df_system['URL'].apply(normalize_url)

    # Clean strings for Excel
    for col in df_system.columns:
        df_system[col] = df_system[col].apply(clean_string)
    for col in df_excel.columns:
        df_excel[col] = df_excel[col].apply(clean_string)

    # 1. Match by URL
    excel_urls = set(df_excel[df_excel['url_norm'] != '']['url_norm'])
    system_urls = set(df_system[df_system['url_norm'] != '']['url_norm'])

    ok_urls = excel_urls.intersection(system_urls)
    
    # 2. Match by Norma (fallback)
    # Extract non-empty Normas from both
    excel_normas = df_excel[df_excel['Norma'].notna() & (df_excel['Norma'] != '')].copy()
    system_normas = df_system[df_system['Norma'].notna() & (df_system['Norma'] != '')].copy()
    
    # Normalize Normas (strip, upper)
    excel_normas['norma_norm'] = excel_normas['Norma'].astype(str).str.strip().str.upper()
    system_normas['norma_norm'] = system_normas['Norma'].astype(str).str.strip().str.upper()
    
    ok_normas = set(excel_normas['norma_norm']).intersection(set(system_normas['norma_norm']))
    
    # Identify OKs by Norma that were not OKs by URL
    urls_by_norma = set(system_normas[system_normas['norma_norm'].isin(ok_normas)]['url_norm'])
    ok_urls.update(urls_by_norma)

    # Final categories
    only_excel_urls = excel_urls - ok_urls
    only_system_urls = system_urls - ok_urls

    print(f"\n--- RESULTADOS DEL CRUCE ---")
    print(f"✅ Coincidentes (OK): {len(ok_urls)}")
    print(f"🆕 Pendientes en Excel (Están en Sistema pero no en el seguimiento manual): {len(only_system_urls)}")
    print(f"❌ No detectados por Sistema (Están en Excel pero no el monitor): {len(only_excel_urls)}")

    # Reports
    df_pendientes = df_system[df_system['url_norm'].isin(only_system_urls)].copy()
    df_no_detectados = df_excel[df_excel['url_norm'].isin(only_excel_urls)].copy()
    df_coincidentes = df_system[df_system['url_norm'].isin(ok_urls)].copy()

    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df_pendientes.drop(columns=['url_norm']).to_excel(writer, sheet_name='Pendientes_en_Excel', index=False)
        df_no_detectados.drop(columns=['url_norm']).to_excel(writer, sheet_name='No_detectados_por_Monitor', index=False)
        df_coincidentes.drop(columns=['url_norm']).to_excel(writer, sheet_name='Coincidentes_OK', index=False)
        
        resumen = pd.DataFrame({
            'Categoría': ['Coincidentes (OK)', 'Pendientes en Excel', 'No detectados por Monitor'],
            'Cantidad': [len(ok_urls), len(only_system_urls), len(only_excel_urls)]
        })
        resumen.to_excel(writer, sheet_name='Resumen', index=False)

    print(f"\nReporte detallado guardado en: {output_path}")

if __name__ == "__main__":
    main()
