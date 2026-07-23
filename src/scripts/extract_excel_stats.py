import pandas as pd
import os
import json

def main():
    excel_path = "/Users/cmotalvaro/Downloads/Seguimiento Regulatorio - 2026 1.xlsm"
    output_dir = "data/stats"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Extrayendo metadatos y estadísticas de: {excel_path}...")
    
    try:
        xl = pd.ExcelFile(excel_path)
        
        # 1. Extraer Listas Desplegables
        df_listas = pd.read_excel(xl, 'Listas Desplegables')
        metadata = {
            "responsables": df_listas['Responsables'].dropna().tolist(),
            "ambitos": df_listas['Ámbito'].dropna().tolist(),
            "regionales": df_listas['Regionales'].dropna().tolist(),
            "reguladores_regionales": df_listas['Reguladores regionales'].dropna().tolist()
        }
        
        # Guardar metadatos
        with open(os.path.join(output_dir, 'excel_metadata.json'), 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=4, ensure_ascii=False)
            
        # 2. Extraer Estadísticas (Parsing manual de la hoja 'Estadísticas')
        df_stats = pd.read_excel(xl, 'Estadísticas')
        
        # La hoja tiene varias tablas dinámicas una al lado de la otra
        # Vamos a extraer las 3 principales que se ven en el primer vistazo
        
        # Tabla 1: Cuenta de Tipo (Filas 2-4 aprox)
        # Buscar "Etiquetas de fila" y "Cuenta de Tipo"
        tablas = {}
        
        # Tipo de Norma (Boletín, Resolución, etc)
        # En el dump vimos columnas como "Fecha registro.6" y "(Varios elementos).6"
        # Pero es mejor buscar por contenido
        
        def extract_table(df, start_col_name, val_col_name):
            try:
                # Buscar la fila donde están los encabezados "Etiquetas de fila"
                for col in df.columns:
                    if start_col_name in str(col):
                        idx = df[df[col] == 'Etiquetas de fila'].index
                        if not idx.empty:
                            start_row = idx[0] + 1
                            data_col = col
                            # La columna de valor suele ser la siguiente
                            val_col_idx = df.columns.get_loc(col) + 1
                            val_col = df.columns[val_col_idx]
                            
                            sub_df = df.iloc[start_row:, [val_col_idx - df.columns.get_loc(col), val_col_idx]] # relative
                            # Mejor usar nombres de columnas reales
                            res = []
                            for r in range(start_row, len(df)):
                                label = df.iloc[r, df.columns.get_loc(col)]
                                value = df.iloc[r, val_col_idx]
                                if pd.isna(label) or str(label).lower() == 'total general':
                                    break
                                res.append({"label": str(label), "value": int(value) if pd.notna(value) else 0})
                            return res
            except:
                pass
            return []

        # Intentar extraer tablas clave
        stats_data = {
            "por_tipo": extract_table(df_stats, "Fecha registro", "Cuenta de Tipo"), # Primera tabla
            "por_emisor": extract_table(df_stats, "Fecha registro.1", "Cuenta de Tipo"), # Segunda tabla
            "por_norma": extract_table(df_stats, "Fecha registro.6", "Cuenta de Tipo") # Sexta tabla aprox
        }
        
        # Si falló la extracción automática por nombres de columnas (que cambian al leer), 
        # usar posiciones fijas detectadas en el dump previo
        if not stats_data["por_tipo"]:
            # Primera tabla: col 0 y 1
            stats_data["por_tipo"] = []
            for r in range(2, 5):
                label = df_stats.iloc[r, 0]
                val = df_stats.iloc[r, 1]
                if pd.notna(label) and 'Total' not in str(label):
                    stats_data["por_tipo"].append({"label": str(label), "value": int(val)})

        if not stats_data["por_norma"]:
            # Tabla de normas (al final)
            stats_data["por_norma"] = []
            # Según el dump, está en las últimas columnas
            col_idx = len(df_stats.columns) - 2
            for r in range(2, 20):
                label = df_stats.iloc[r, col_idx]
                val = df_stats.iloc[r, col_idx + 1]
                if pd.notna(label) and 'Total' not in str(label):
                    stats_data["por_norma"].append({"label": str(label), "value": int(val)})

        # Guardar estadísticas
        with open(os.path.join(output_dir, 'excel_stats.json'), 'w', encoding='utf-8') as f:
            json.dump(stats_data, f, indent=4, ensure_ascii=False)

        print("Extracción completada con éxito.")

    except Exception as e:
        print(f"Error durante la extracción: {e}")

if __name__ == "__main__":
    main()
