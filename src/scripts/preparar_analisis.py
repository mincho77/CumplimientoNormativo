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

ROOT = Path(__file__).parent.parent.parent
INBOX_DIR = ROOT / "raw" / "inbox"
CASES_FILE = ROOT / "data" / "casos_detectados.csv"

PROMPT_SISTEMA = """
Eres un Analista Senior de Cumplimiento Normativo Legal y Estratégico para el Grupo SURA en Colombia. 
Tu propósito es realizar un análisis TÉCNICO y de RIESGO de extractos de documentos oficiales.

INSTRUCCIONES DE ANÁLISIS CORPORATIVO:
1. **Línea de Negocio**: Identifica a qué filial de SURA afecta más (Salud/EPS, Seguros Vida, Seguros Generales, ARL, Pensiones/Asset Management, o Transversal si afecta a todas).
2. **Impacto TI**: Determina si la norma implica cambios en sistemas de información, reportes digitales, bases de datos o facturación electrónica.
3. **Riesgo Sancionatorio**: Evalúa si la norma menciona multas, cierres, o medidas cautelares. Clasifica como (Crítico, Alto, Medio, Bajo).
4. **Plazo**: Identifica el tiempo límite para implementar los cambios (ej: 30 días, Inmediato, 6 meses).

TAREA:
Responde ÚNICAMENTE en formato JSON con las siguientes llaves:
{
  "tema": "Título corto (max 5 palabras)",
  "entidad_real": "Nombre de la entidad que emite",
  "fecha_publicacion": "AAAA-MM-DD",
  "incidencia": "Impacto en SURA (ALTA, MEDIA, BAJA, NO)",
  "linea_negocio": "Salud, Vida, Generales, ARL, Pensiones, Transversal",
  "impacto_ti": "SÍ/NO",
  "riesgo_sancionatorio": "Crítico/Alto/Medio/Bajo",
  "plazo_implementacion": "Ej: 30 días",
  "obligaciones": "Resumen de las 3 obligaciones principales",
  "resumen": "Resumen ejecutivo de 2 frases",
  "control_sox_sugerido": "SÍ/NO (¿Afecta reporte financiero?)"
}
"""

def extraer_texto_pdf(pdf_path, max_pages=5):
    try:
        reader = PdfReader(pdf_path)
        texto = ""
        # Leer solo las primeras páginas para no saturar el contexto y ahorrar tokens
        for i in range(min(len(reader.pages), max_pages)):
            texto += reader.pages[i].extract_text() + "\n"
        # Limpieza básica para evitar disparadores de filtros por ruido
        texto = texto.replace('  ', ' ').strip()
        return texto[:10000] # Limitar a 10k caracteres
    except Exception as e:
        print(f"Error extrayendo texto de {pdf_path.name}: {e}")
        return None

def get_timestamp():
    return datetime.now().strftime('%H:%M:%S')

def clean_text_for_ia(texto):
    """Limpia el texto de palabras que suelen disparar falsos positivos en los filtros de Azure."""
    # Reemplazar palabras 'violentas' o 'peligrosas' por versiones neutrales si es necesario
    # Por ahora solo limpieza de ruido y caracteres extraños
    texto = texto.replace('\x00', '') # Null bytes
    texto = ' '.join(texto.split()) # Colapsar espacios
    return texto[:8000] # Un poco más corto para ser más seguro

def analizar_con_ia(texto, retry_safe=True):
    try:
        # Envolver el texto en delimitadores claros para separar DATA de INSTRUCCIONES
        user_content = f"### DATA NORMATIVA PARA ANÁLISIS CORPORATIVO ###\n{texto}\n### FIN DE DATA ###"
        
        response = client.chat.completions.create(
            model=MODELO,
            messages=[
                {"role": "system", "content": PROMPT_SISTEMA},
                {"role": "user", "content": user_content}
            ],
            response_format={ "type": "json_object" }
        )
        data = json.loads(response.choices[0].message.content)
        data['tokens_ia'] = response.usage.total_tokens
        return data

    except Exception as e:
        error_str = str(e).lower()
        is_filter = any(x in error_str for x in ['content_filter', 'filtered', 'policy', 'responsibleai'])
        
        if is_filter:
            if retry_safe:
                print(f"[{get_timestamp()}] ⚠️ Filtro detectado. Reintentando en 'MODO SEGURO' (limpieza de texto)...")
                # Reintentar con texto más corto y limpio
                safe_text = texto[:4000] # Mucho más corto
                return analizar_con_ia(safe_text, retry_safe=False)
            
            print(f"[{get_timestamp()}] ❌ BLOQUEO DEFINITIVO por política de seguridad de Azure.")
            return {
                "tema": "Bloqueado por Seguridad Azure",
                "entidad_real": "Desconocida",
                "fecha_publicacion": "No especificada",
                "incidencia": "BAJA",
                "obligaciones": "El documento disparó los filtros de contenido de Azure (Jailbreak/Violence). Posible mención de sanciones o delitos en la norma. Revisar manualmente.",
                "resumen": "Análisis IA no disponible por políticas de Azure OpenAI.",
                "tokens_ia": 0
            }
        
        print(f"[{get_timestamp()}] Error en la API: {e}")
        return None

def procesar_inbox():
    if not INBOX_DIR.exists():
        print(f"[{get_timestamp()}] La carpeta {INBOX_DIR} no existe.")
        return

    files = list(INBOX_DIR.glob("*.pdf"))
    if not files:
        print(f"[{get_timestamp()}] No hay archivos PDF en el inbox.")
        return

    casos_procesados = set()
    if CASES_FILE.exists():
        with open(CASES_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('analisis_ia_status') == 'procesado':
                    casos_procesados.add(row.get('case_id'))
                    
    archivos_pendientes = [p for p in files if p.stem not in casos_procesados]
    
    print(f"[{get_timestamp()}] 🤖 INICIO ANÁLISIS IA | Pendientes: {len(archivos_pendientes)} / {len(files)}")
    
    if not archivos_pendientes:
        print(f"[{get_timestamp()}] ✅ Todo al día.")
        return

    from aplicar_analisis_ia import apply_analysis
    casos_para_actualizar = []
    
    for i, pdf_path in enumerate(archivos_pendientes, start=1):
        case_id = pdf_path.stem 
        print(f"[{get_timestamp()}] [{i}/{len(archivos_pendientes)}] Procesando: {pdf_path.name}...")
        
        texto = extraer_texto_pdf(pdf_path)
        if not texto or len(texto.strip()) < 50:
            print(f"  -> ⚠️ Texto insuficiente.")
            casos_para_actualizar.append({
                'case_id': case_id, 'tema': 'Sin texto', 'incidencia': 'NO', 
                'obligaciones': 'No se pudo extraer texto legible del PDF.', 'tokens_ia': 0
            })
        else:
            texto_limpio = clean_text_for_ia(texto)
            analisis = analizar_con_ia(texto_limpio)
            
            if analisis:
                analisis['case_id'] = case_id
                casos_para_actualizar.append(analisis)
                print(f"  -> ✅ Éxito: {analisis.get('tema', '')[:30]}... | Tokens: {analisis.get('tokens_ia', 0)}")
            else:
                print(f"  -> ❌ Fallo crítico en API para {pdf_path.name}")
                
        if len(casos_para_actualizar) >= 10 or i == len(archivos_pendientes):
            if casos_para_actualizar:
                print(f"[{get_timestamp()}] 💾 Guardando lote de {len(casos_para_actualizar)}...")
                apply_analysis(casos_para_actualizar)
                casos_para_actualizar = []

if __name__ == "__main__":
    procesar_inbox()
