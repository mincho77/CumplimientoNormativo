import os
import csv
import json
from pathlib import Path
from openai import AzureOpenAI
from dotenv import load_dotenv
from pypdf import PdfReader
from datetime import datetime

# Cargar variables de entorno
load_dotenv()

# Configuración específica para Azure
client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    azure_endpoint=os.getenv("OPENAI_BASE_URL").split("/openai/")[0],
    api_version="2024-02-15-preview" # Versión común, ajustable
)

# En Azure, 'model' debe ser el nombre del despliegue (deployment name)
MODELO = os.getenv("OPENAI_MODEL_NAME")

ROOT = Path(__file__).parent.parent
INBOX_DIR = ROOT / "raw" / "inbox"
CASES_FILE = ROOT / "data" / "casos_detectados.csv"

PROMPT_SISTEMA = """
Eres un experto en cumplimiento normativo legal y financiero en Colombia, especializado en SURA.
Tu tarea es analizar extractos de documentos oficiales (leyes, decretos, resoluciones, circulares).

Debes determinar:
1. **Tema**: De qué trata el documento en 3-5 palabras.
2. **Entidad Real Emisora**: ¿Quién emitió originalmente la norma? (Ej. Si el Ministerio de Salud publica una Ley del Congreso, la entidad emisora es el Congreso de la República, no el Ministerio). Si no estás seguro, pon "Desconocida".
3. **Fecha de Publicación**: ¿En qué fecha (AAAA-MM-DD) se expidió o firmó el documento según su texto? Si no hay fecha clara, pon "No especificada".
4. **Incidencia**: ¿Tiene impacto directo en SURA? (Opciones: ALTA, MEDIA, BAJA, NO).
5. **Obligaciones**: Resume las obligaciones principales o acciones requeridas.
6. **Resumen**: Un resumen ejecutivo de 2 frases.

Responde ÚNICAMENTE en formato JSON con las siguientes llaves:
{
  "tema": "...",
  "entidad_real": "...",
  "fecha_publicacion": "...",
  "incidencia": "...",
  "obligaciones": "...",
  "resumen": "..."
}
"""

def extraer_texto_pdf(pdf_path, max_pages=5):
    try:
        reader = PdfReader(pdf_path)
        texto = ""
        # Leer solo las primeras páginas para no saturar el contexto y ahorrar tokens
        for i in range(min(len(reader.pages), max_pages)):
            texto += reader.pages[i].extract_text() + "\n"
        return texto[:10000] # Limitar a 10k caracteres
    except Exception as e:
        print(f"Error extrayendo texto de {pdf_path.name}: {e}")
        return None

def analizar_con_ia(texto):
    try:
        response = client.chat.completions.create(
            model=MODELO,
            messages=[
                {"role": "system", "content": PROMPT_SISTEMA},
                {"role": "user", "content": f"Analiza el siguiente texto normativo:\n\n{texto}"}
            ],
            response_format={ "type": "json_object" }
        )
        data = json.loads(response.choices[0].message.content)
        # Capturar tokens
        data['tokens_ia'] = response.usage.total_tokens
        return data
    except Exception as e:
        print(f"Error en la API de OpenAI: {e}")
        return None

def procesar_inbox():
    if not INBOX_DIR.exists():
        print(f"La carpeta {INBOX_DIR} no existe.")
        return

    # Obtener archivos en el inbox
    files = list(INBOX_DIR.glob("*.pdf"))
    if not files:
        print("No hay archivos PDF en el inbox.")
        return

    # Leer casos existentes para saber cuáles ya fueron procesados
    casos_procesados = set()
    if CASES_FILE.exists():
        with open(CASES_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('analisis_ia_status') == 'procesado':
                    casos_procesados.add(row.get('case_id'))
                    
    # Filtrar solo archivos pendientes
    archivos_pendientes = [p for p in files if p.stem not in casos_procesados]
    
    print(f"Encontrados {len(files)} archivos totales | {len(archivos_pendientes)} pendientes de análisis IA.")
    
    if not archivos_pendientes:
        print("Todo está al día. No hay archivos nuevos para la IA.")
        return

    from aplicar_analisis_ia import apply_analysis
    casos_para_actualizar = []
    
    # Procesar en lotes de 10 para guardar progreso periódicamente
    for i, pdf_path in enumerate(archivos_pendientes, start=1):
        case_id = pdf_path.stem 
        print(f"[{i}/{len(archivos_pendientes)}] Procesando: {pdf_path.name}...")
        
        texto = extraer_texto_pdf(pdf_path)
        if not texto or len(texto.strip()) < 50:
            print(f"Texto insuficiente en {pdf_path.name}, marcando como procesado vacío.")
            # Para que no lo vuelva a intentar
            casos_para_actualizar.append({
                'case_id': case_id, 'tema': 'Sin texto', 'incidencia': 'NO', 
                'obligaciones': 'No se pudo extraer texto', 'tokens_ia': 0
            })
        else:
            analisis = analizar_con_ia(texto)
            if analisis:
                analisis['case_id'] = case_id
                casos_para_actualizar.append(analisis)
                print(f"  -> Éxito: {analisis.get('tema', '')[:30]}... | Tokens: {analisis.get('tokens_ia', 0)}")
            else:
                print(f"  -> Falló la API para {pdf_path.name}")
                
        # Guardar cada 10 documentos o al final
        if len(casos_para_actualizar) >= 10 or i == len(archivos_pendientes):
            print(f"Guardando lote de {len(casos_para_actualizar)} documentos en CSV...")
            apply_analysis(casos_para_actualizar)
            casos_para_actualizar = []

if __name__ == "__main__":
    procesar_inbox()
