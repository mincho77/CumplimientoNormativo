#!/usr/bin/env python3
"""
analizar_norma.py
Extrae obligaciones regulatorias de un PDF usando Azure OpenAI.
Usa el prompt especializado de análisis de cumplimiento normativo SURA.
"""
import os
import io
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple
from urllib.request import Request, urlopen
from urllib.error import URLError

try:
    from scripts.self_heal import SelfHealConfig, generate_with_self_heal
except ImportError:
    from self_heal import SelfHealConfig, generate_with_self_heal

try:
    from openai import AzureOpenAI
    from dotenv import load_dotenv
    from pypdf import PdfReader
    DEPS_OK = True
except ImportError:
    DEPS_OK = False

ROOT = Path(__file__).parent.parent.parent  # Cumplimiento_Normativo raíz
SRC_ROOT = Path(__file__).parent.parent      # src/
LISTAS_FILE = ROOT / "data" / "listas_clasificacion.json"
REPAIR_HISTORY_FILE = ROOT / "data" / "state" / "ia_repair_history.jsonl"


def _get_max_repair_attempts() -> int:
    raw = os.getenv("MAX_REPAIR_ATTEMPTS", "2") or "2"
    try:
        return max(1, min(3, int(raw)))
    except Exception:
        return 2

# ─── Cargar configuración ────────────────────────────────────────────────────

def _load_env():
    env_path = ROOT / "CumplimientoNormativo" / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    else:
        load_dotenv()

def _load_listas():
    if LISTAS_FILE.exists():
        with open(LISTAS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def _get_client():
    _load_env()
    base_url = os.getenv("OPENAI_BASE_URL", "")
    endpoint = base_url.split("/openai/")[0] if "/openai/" in base_url else base_url
    return AzureOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        azure_endpoint=endpoint,
        api_version="2024-02-15-preview",
    )


def _strip_markdown_fences(raw: str) -> str:
    text = (raw or "").strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text


def _build_fallback_analysis(reason: str) -> dict:
    return {
        "datos_generales": {
            "titulo": "Extracción automática no concluyente",
            "anexos": "No especificado",
            "fecha_publicacion": "No especificado",
            "emisor": "No especificado",
            "norma": "No especificado",
            "tipo_norma": "No especificado",
            "jurisdiccion": "Colombia",
            "temas": [],
            "sectores_economicos": [],
            "incidencia_sura": "Evaluación Externa (requiere conocimiento de la operación de Sura)",
            "obligaciones_sura": "Evaluación Externa (requiere conocimiento de la operación de Sura)",
            "control_sox": "Evaluación Externa (requiere conocimiento de la operación de Sura)",
            "divulgacion_sox": "Evaluación Externa (requiere conocimiento de la operación de Sura)",
            "companias_impactadas": [],
        },
        "obligaciones": [
            {
                "numeral_articulo": "No especificado",
                "texto_obligacion": f"No fue posible extraer obligaciones válidas automáticamente. Motivo: {reason}",
                "tipo_obligacion": "General",
                "frecuencia": "Permanente",
                "vigencia_desde": "No especificado",
                "normas_relacionadas": "No especificado",
                "entregable": "Revisión manual requerida",
                "macroproceso": "No especificado",
                "proceso": "No especificado",
                "lider_proceso": "No especificado",
            }
        ],
    }


def _validate_analysis_output(candidate: dict) -> Tuple[bool, str]:
    if not isinstance(candidate, dict):
        return False, "salida no es objeto JSON"
    if "content" not in candidate:
        return False, "falta campo content"
    content = (candidate.get("content") or "").strip()
    if len(content) < 20:
        return False, "contenido vacío o demasiado corto"

    content = _strip_markdown_fences(content)
    try:
        parsed = json.loads(content)
    except Exception:
        return False, "json inválido"

    if not isinstance(parsed, dict):
        return False, "json raíz debe ser objeto"
    if "datos_generales" not in parsed or not isinstance(parsed.get("datos_generales"), dict):
        return False, "falta datos_generales"
    if "obligaciones" not in parsed or not isinstance(parsed.get("obligaciones"), list):
        return False, "falta obligaciones como lista"

    datos = parsed["datos_generales"]
    required_data_keys = ["norma", "tipo_norma", "jurisdiccion"]
    for key in required_data_keys:
        if str(datos.get(key, "")).strip() == "":
            return False, f"campo obligatorio vacío en datos_generales: {key}"

    parsed["obligaciones"] = [o for o in parsed["obligaciones"] if isinstance(o, dict)]
    if not parsed["obligaciones"]:
        return False, "sin obligaciones válidas"

    return True, ""


def _persist_repair_history(input_payload: dict, output_payload: dict) -> None:
    try:
        REPAIR_HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": input_payload.get("source", "desconocido"),
            "input_size": len(input_payload.get("texto_norma", "") or ""),
            "repair_info": output_payload.get("repair_info", {}),
            "meta": output_payload.get("meta", {}),
        }
        with open(REPAIR_HISTORY_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:
        # No bloquear el flujo principal por fallas de logging.
        pass


def _call_azure_json(client, model_name: str, messages: list) -> tuple[str, int]:
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0.1,
    )
    raw = (response.choices[0].message.content or "").strip()
    tokens = response.usage.total_tokens if response.usage else 0
    return raw, tokens

# ─── Extracción de texto ─────────────────────────────────────────────────────

def extraer_texto_de_bytes(pdf_bytes: bytes, max_pages: int = 20) -> str:
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        texto = ""
        for i in range(min(len(reader.pages), max_pages)):
            texto += (reader.pages[i].extract_text() or "") + "\n"
        texto = " ".join(texto.split())
        return texto[:40000]  # ~40k chars es aprox 10k tokens
    except Exception as e:
        return ""


def descargar_pdf(url: str, timeout: int = 25) -> Optional[bytes]:
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0 (CumplimientoBot/1.0)"})
        with urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except Exception:
        return None


def extraer_texto_de_url(url: str) -> str:
    pdf_bytes = descargar_pdf(url)
    if not pdf_bytes:
        return ""
    return extraer_texto_de_bytes(pdf_bytes)

# ─── Construcción del prompt ─────────────────────────────────────────────────

def _build_prompt(listas: dict) -> str:
    emisores = "\n".join(f"  - {e}" for e in listas.get("emisores", []))
    tipos = "\n".join(f"  - {t}" for t in listas.get("tipos_norma", []))
    temas = "\n".join(f"  - {t}" for t in listas.get("temas", []))
    sectores_raw = listas.get("sectores_economicos", [])
    sectores = "\n".join(f"  - {s}" for s in sectores_raw) if sectores_raw and "PENDIENTE" not in str(sectores_raw[0]) else "  (pendiente de configurar)"
    companias_raw = listas.get("companias", [])
    companias = "\n".join(f"  - {c}" for c in companias_raw) if companias_raw and "PENDIENTE" not in str(companias_raw[0]) else "  (pendiente de configurar)"
    procesos_raw = listas.get("procesos_sura", [])
    procesos = "\n".join(f"  - {p}" for p in procesos_raw) if procesos_raw and "PENDIENTE" not in str(procesos_raw[0]) else "  (pendiente de configurar)"

    return f"""
Eres un experto analista regulatorio, meticuloso y preciso, especializado en la extracción estructurada de información de documentos legales y normativos. Tu tarea principal es identificar y extraer todos los campos definidos en las secciones "I. Datos generales de la norma" y "II. Identificación de obligaciones", a partir del texto de la norma.

# Instrucciones generales:
1. Procesamiento del documento: Analiza el documento normativo completo con gran atención, identificando cada sección, título y, fundamentalmente, cada artículo o numeral.
2. Enfoque en obligaciones: Tu objetivo principal es identificar y extraer obligaciones específicas. Presta especial atención a los verbos que denoten acción o mandato (por ejemplo: "deberá", "podrá", "garantizarán", "fijar", "establecer", "informar", "realizar", "reportar", "adoptar", "cumplir", entre otros).
3. Considerandos: Analiza los "considerandos" de la norma solo para contextualizar. Bajo ninguna circunstancia extraigas obligaciones de esta sección.
4. Extracción a nivel de artículo: Realiza el análisis y la extracción de obligaciones a nivel de artículo o numeral. Cada artículo puede contener una o varias obligaciones.
5. Filtro Estricto de Sujeto Obligado (Exclusión de Entes Públicos): Extrae **únicamente** las obligaciones que correspondan a entidades privadas, aseguradoras, administradoras de riesgos (ARL), entidades promotoras de salud (EPS), instituciones prestadoras de servicios de salud (IPS) o empresas del sector privado. 
   * **CRÍTICO:** Ignora por completo y bajo ninguna circunstancia extraigas obligaciones cuyo sujeto responsable sea un Ministerio (de Salud, Trabajo, Hacienda, etc.), el FONSAET, la Superintendencia, u otros organismos de control, fondos públicos o reguladores. Si el artículo dicta una acción para el Estado o el Gobierno, **no es una obligación para este alcance y debes omitirla.**
6. Si no encuentras información para un campo específico, indica "No especificado".

## I. Datos generales de la norma
Extrae los siguientes campos:
- titulo: Descripción de la finalidad o el contenido principal de la norma.
- anexos: Lista de anexos mencionados, o "No especificado".
- fecha_publicacion: Fecha de emisión de la norma (Ej: "6 de mayo de 2016").
- emisor: Autoridad reguladora que expide la norma. Clasifica en una de estas opciones:
{emisores}
- norma: Título o nombre oficial de la norma (Ej: "DECRETO 780 DE 2016").
- tipo_norma: Clasifica en una de estas opciones:
{tipos}
- jurisdiccion: País donde se emite la norma.
- temas: Categorías o áreas principales (puedes seleccionar múltiples):
{temas}
- sectores_economicos: Sectores económicos aplicables (puedes seleccionar múltiples):
{sectores}
- incidencia_sura: Indica "Evaluación Externa (requiere conocimiento de la operación de Sura)".
- obligaciones_sura: Indica "Evaluación Externa (requiere conocimiento de la operación de Sura)".
- control_sox: Indica "Evaluación Externa (requiere conocimiento de la operación de Sura)".
- divulgacion_sox: Indica "Evaluación Externa (requiere conocimiento de la operación de Sura)".
- companias_impactadas: Compañías de Sura que podrían verse impactadas (puedes seleccionar múltiples):
{companias}

## II. Identificación de obligaciones
Para CADA obligación encontrada, extrae:
- numeral_articulo: Número exacto del artículo o numeral (Ej: "Artículo 2.1.1.6").
- texto_obligacion: Texto literal o paráfrasis clara del artículo con el verbo de acción principal.
- tipo_obligacion: Clasifica la obligación según su naturaleza de acción principal. Usa **únicamente** una de estas opciones:
  - **Reportar**: reportar, informar, notificar, remitir, enviar, comunicar (hacia un ente regulador o tercero).
  - **Pagar**: pagar, cancelar, liquidar, desembolsar, transferir, reconocer económicamente.
  - **Implementar**: implementar, adoptar, establecer, crear, diseñar, estructurar, desarrollar (sistemas, procesos, políticas).
  - **Controlar**: verificar, monitorear, supervisar, vigilar, auditar, revisar (en calidad de seguimiento operativo).
  - **Documentar**: conservar, archivar, registrar, custodiar, documentar, guardar, llevar registro.
  - **Autorizar**: autorizar, aprobar, validar, certificar, habilitar, homologar.
  - **Capacitar**: capacitar, formar, entrenar, sensibilizar, instruir.
  - **Prohibición**: no podrá, se prohíbe, está prohibido, no está permitido, no debe.
  - **Divulgar**: divulgar, publicar, socializar, difundir, informar (al público o clientes).
  - **Garantizar**: garantizar, asegurar, velar, procurar, proteger.
  - **Actualizar**: actualizar, modificar, revisar, ajustar, renovar (información o documentos existentes).
  - **General**: cuando ningún otro tipo aplica claramente.
- frecuencia: Plazo, fecha límite o frecuencia de cumplimiento. Si no hay plazo explícito de vencimiento, indica "Permanente".
- vigencia_desde: Fecha o condición explícita desde la cual esta obligación específica **entra en vigor o debe comenzar a cumplirse**. Busca expresiones como "rige a partir de", "entrará en vigencia el", "a partir del", "desde la publicación", "dentro de los X días siguientes a", o referencias a otra norma que defina el inicio. Si el artículo no establece un inicio diferente al de la norma general, indica "No especificado".
- normas_relacionadas: Otras normas mencionadas como fundamento o complemento. Clasifica si es "Fundamento legal" o "Norma relacionada".
- entregable: Documento, informe u output tangible que genera la obligación. Si no hay uno, indica "No especificado".
- macroproceso: Macroproceso de Sura aplicable.
  * **REGLA DE ORO PARA LA ASIGNACIÓN DE PROCESOS:** Si la norma exige implementar un control operativo, validar datos, verificar condiciones de un cliente, procesar un pago o realizar seguimientos del día a día, esto es responsabilidad del **PROCESO DE NEGOCIO / OPERACIÓN COMPETENTE** (ej: *Diseño y desarrollo de portafolio*, *Distribución*, o *Prestación de servicios*).
  * **REGLA DE EXCLUSIÓN DE AUDITORÍA:** **NO** lo asignes a procesos de "Auditoría Integral" o "Auditoría Interna" solo porque el texto use palabras como "verificar" o "controlar". Reserva los procesos de **Auditoría** *únicamente* cuando el texto normativo exija explícitamente una evaluación independiente de la tercera línea de defensa, auditorías de la alta dirección o investigaciones de fraude/línea ética.
  * **REGLA DE EXCLUSIÓN DE GESTIÓN DE CASOS:** El proceso de "Gestión de casos" aplica **ÚNICAMENTE** si el artículo regula de forma directa el trámite, tiempos de respuesta, escalabilidad o radicación de **PQRS (Peticiones, Quejas, Reclamos o Sugerencias)** o requerimientos directos de entes de control sobre inconformidades. Si el artículo habla de la atención ordinaria de un caso médico, un caso de siniestro, un reclamo de póliza de autos/vida o la entrega general de un servicio, **NO** va en Gestión de Casos; debes asignarlo al proceso de prestación o siniestro correspondiente (ej. *Atención reclamaciones*, *Atención en salud*, *Acceso y asignación*).
  Selecciona el macroproceso según las siguientes opciones:

{procesos}
- proceso: Proceso de Sura aplicable.
- lider_proceso: Líder del proceso de Sura aplicable.


# FORMATO DE RESPUESTA (JSON estricto, sin texto adicional):
{{
  "datos_generales": {{
    "titulo": "...",
    "anexos": "...",
    "fecha_publicacion": "...",
    "emisor": "...",
    "norma": "...",
    "tipo_norma": "...",
    "jurisdiccion": "...",
    "temas": ["..."],
    "sectores_economicos": ["..."],
    "incidencia_sura": "Evaluación Externa (requiere conocimiento de la operación de Sura)",
    "obligaciones_sura": "Evaluación Externa (requiere conocimiento de la operación de Sura)",
    "control_sox": "Evaluación Externa (requiere conocimiento de la operación de Sura)",
    "divulgacion_sox": "Evaluación Externa (requiere conocimiento de la operación de Sura)",
    "companias_impactadas": ["..."]
  }},
  "obligaciones": [
    {{
      "numeral_articulo": "...",
      "texto_obligacion": "...",
      "tipo_obligacion": "...",
      "frecuencia": "...",
      "vigencia_desde": "...",
      "normas_relacionadas": "...",
      "entregable": "...",
      "macroproceso": "...",
      "proceso": "...",
      "lider_proceso": "..."
    }}
  ]
}}
"""


# ─── Llamada a la API ─────────────────────────────────────────────────────────

def _llamar_api(client, prompt_sistema: str, texto_norma: str) -> dict:
    model_name = os.getenv("OPENAI_MODEL_NAME")
    base_user_content = f"### TEXTO DE LA NORMA PARA ANÁLISIS ###\n\n{texto_norma}\n\n### FIN DEL TEXTO ###"
    token_counter = {"value": 0}

    def _generate(payload: dict) -> dict:
        user_content = payload.get("user_content", base_user_content)
        repair_reason = payload.get("repair_reason", "")
        attempt = payload.get("attempt", 0)

        system_content = prompt_sistema
        if repair_reason:
            system_content += (
                "\n\nINSTRUCCIONES DE REPARACION OBLIGATORIAS:\n"
                f"- Motivo de invalidación previo: {repair_reason}\n"
                f"- Intento actual: {attempt}\n"
                "- Responde SOLO con JSON válido, sin texto extra, sin markdown, sin fences.\n"
                "- Incluye obligatoriamente `datos_generales` (objeto) y `obligaciones` (lista).\n"
                "- No dejes campos clave vacíos."
            )

        try:
            raw, tokens = _call_azure_json(
                client,
                model_name,
                [
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": user_content},
                ],
            )
            token_counter["value"] += tokens
            return {"content": raw}
        except Exception as e:
            err = str(e).lower()
            is_filter = any(x in err for x in ["content_filter", "filtered", "policy", "responsibleai"])
            if is_filter:
                short_content = f"### TEXTO DE LA NORMA ###\n\n{texto_norma[:6000]}\n\n### FIN ###"
                try:
                    raw2, tokens2 = _call_azure_json(
                        client,
                        model_name,
                        [
                            {"role": "system", "content": system_content},
                            {"role": "user", "content": short_content},
                        ],
                    )
                    token_counter["value"] += tokens2
                    return {"content": raw2, "warning": "Texto recortado por política de seguridad de Azure."}
                except Exception as retry_err:
                    return {"content": "", "error": f"{retry_err}"}

            return {"content": "", "error": f"{e}"}

    def _enrich_for_repair(original_input: dict, reason: str, attempt: int) -> dict:
        # Reducimos longitud en reintentos para mejorar robustez sin perder demasiada señal.
        max_chars = max(6000, 40000 - (attempt * 10000))
        return {
            "texto_norma": original_input.get("texto_norma", "")[:max_chars],
            "user_content": (
                "### TEXTO DE LA NORMA PARA ANÁLISIS ###\n\n"
                f"{original_input.get('texto_norma', '')[:max_chars]}\n\n"
                "### FIN DEL TEXTO ###"
            ),
            "repair_reason": reason,
            "attempt": attempt,
            "source": original_input.get("source", "desconocido"),
        }

    def _build_fallback(input_payload: dict, reason: str) -> dict:
        fallback = _build_fallback_analysis(reason)
        return {"content": json.dumps(fallback, ensure_ascii=False)}

    def _normalize(payload: dict) -> dict:
        artifact = payload.get("artifact", {})
        content = _strip_markdown_fences(str(artifact.get("content", "")))
        try:
            parsed = json.loads(content)
        except Exception:
            parsed = _build_fallback_analysis("json inválido tras normalización")

        artifact["content"] = json.dumps(parsed, ensure_ascii=False)
        payload["artifact"] = artifact
        return payload

    contract = generate_with_self_heal(
        {
            "texto_norma": texto_norma,
            "user_content": base_user_content,
            "source": "analizar_norma",
            "attempt": 0,
        },
        _generate,
        _validate_analysis_output,
        _enrich_for_repair,
        _build_fallback,
        config=SelfHealConfig(
            max_repair_attempts=_get_max_repair_attempts(),
            artifact_type="json",
            filename="analisis_norma.json",
            encoding="plain",
            mime_type="application/json",
        ),
        normalize=_normalize,
        persist_history=_persist_repair_history,
    )

    parsed = json.loads(contract["artifact"]["content"])
    parsed["_tokens"] = token_counter["value"]
    parsed["_repair_info"] = contract.get("repair_info", {})
    return parsed


# ─── Funciones públicas ───────────────────────────────────────────────────────

def analizar_desde_url(url: str) -> dict:
    """Descarga un PDF desde una URL y ejecuta el análisis de obligaciones."""
    if not DEPS_OK:
        raise ImportError("Faltan dependencias: openai, pypdf, python-dotenv")
    
    texto = extraer_texto_de_url(url)
    if len(texto.strip()) < 100:
        raise ValueError(f"No se pudo extraer texto suficiente del PDF: {url}")
    
    listas = _load_listas()
    prompt = _build_prompt(listas)
    client = _get_client()
    resultado = _llamar_api(client, prompt, texto)
    resultado["_fuente"] = url
    return resultado


def analizar_desde_bytes(pdf_bytes: bytes, nombre: str = "documento.pdf") -> dict:
    """Analiza un PDF a partir de sus bytes (subido manualmente)."""
    if not DEPS_OK:
        raise ImportError("Faltan dependencias: openai, pypdf, python-dotenv")
    
    texto = extraer_texto_de_bytes(pdf_bytes)
    if len(texto.strip()) < 100:
        raise ValueError(f"No se pudo extraer texto suficiente del PDF: {nombre}")
    
    listas = _load_listas()
    prompt = _build_prompt(listas)
    client = _get_client()
    resultado = _llamar_api(client, prompt, texto)
    resultado["_fuente"] = nombre
    return resultado


if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else None
    if not url:
        print("Uso: python analizar_norma.py <url_pdf>")
        sys.exit(1)
    try:
        res = analizar_desde_url(url)
        print(json.dumps(res, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
