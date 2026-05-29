import pandas as pd
import sys

excel_path = "/Users/cmotalvaro/Downloads/Seguimiento Regulatorio - 2026 1.xlsm"
csv_path = "data/casos_detectados.csv"

try:
    # Read excel headers
    xl = pd.ExcelFile(excel_path)
    print(f"Sheets in Excel: {xl.sheet_names}")
    
    # Try to read the first sheet or one that looks like 'Seguimiento'
    sheet_name = xl.sheet_names[0]
    df_excel = pd.read_excel(excel_path, sheet_name=sheet_name, nrows=5)
    print(f"\nColumns in Excel ({sheet_name}):")
    print(df_excel.columns.tolist())
    print("\nSample Excel data:")
    print(df_excel.head())

    # Read CSV headers
    df_csv = pd.read_csv(csv_path, nrows=5)
    print(f"\nColumns in CSV ({csv_path}):")
    print(df_csv.columns.tolist())
    print("\nSample CSV data:")
    print(df_csv.head())

except Exception as e:
    print(f"Error: {e}")
