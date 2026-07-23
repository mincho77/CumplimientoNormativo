#!/usr/bin/env python3
import csv
import os
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CASES_FILE = os.path.join(ROOT, "data", "casos_detectados.csv")
OUT_FILE = os.path.join(ROOT, "data", "tablero_semaforo.csv")


def semaforo(row: dict):
    s = (row.get("status", "") or "").strip().lower()
    p = (row.get("priority", "") or "").strip().lower()
    a = (row.get("aplica_sura", "") or "").strip().lower()
    r = (row.get("Resultado análisis", "") or "").strip().lower()
    riesgo = (row.get("riesgo_sancionatorio", "") or "").strip().lower()
    sox = (row.get("Control SOX", "") or "").strip().upper()
    sox_sug = (row.get("control_sox_sugerido", "") or "").strip().upper()

    if s == "consolidado":
        return "CONSOLIDADO", "Integrado en matriz de obligaciones"
    
    # REGLA JURÍDICA: Riesgo Crítico o Alto es prioridad máxima
    if riesgo in ["crítico", "critico", "alto"]:
        return "ROJO", f"RIESGO {riesgo.upper()}: Requiere atención legal inmediata"
    
    # REGLA JURÍDICA: Impacto SOX detectado o sugerido
    if sox == "SÍ" or sox_sug == "SÍ":
        return "ROJO", "IMPACTO SOX: Afecta controles financieros"

    # REGLA DE NEGOCIO: Si es "No divulgar" o "Repetida", va a verde
    if "no divulgar" in r or "repetida" in r:
        return "VERDE", "Descartado / no aplica (según análisis)"
        
    # REGLA DE NEGOCIO: Si es "Divulgar", es impacto confirmado
    if "divulgar" in r:
        return "ROJO", "IMPACTO CONFIRMADO: Requiere divulgación"

    if s in {"detectado", "extraido_ia", "en_validacion", "importado_excel"}:
        if p == "alta":
            return "ROJO", "Pendiente de revisión prioritaria (alta)"
        return "AMARILLO", "Pendiente de revisión manual"
    
    if s == "validado":
        return "AMARILLO", "Validado, falta consolidar"
    
    if s == "rechazado" or a == "no":
        return "VERDE", "Descartado / no aplica"
    
    return "AMARILLO", "Estado incompleto o no clasificado"


def main():
    if not os.path.exists(CASES_FILE):
        print("No existe casos_detectados.csv")
        return

    with open(CASES_FILE, "r", encoding="utf-8", newline="") as f:
        clean_lines = (line.replace('\0', '') for line in f)
        rows = list(csv.DictReader(clean_lines))

    out_rows = []
    for r in rows:
        color, motivo = semaforo(r)
        # Diccionario base con campos de sistema
        d_at = r.get("detected_at", "")
        if not d_at or d_at == "":
            d_at = r.get("Fecha registro", "")
            if d_at and len(d_at) == 10: # YYYY-MM-DD
                d_at = f"{d_at} 00:00:00-0500"

        row_data = {
            "semaforo": color,
            "motivo": motivo,
            "detected_at": d_at,
            "entidad": r.get("entidad", ""),
            "fuente_url": r.get("fuente_url", ""),
            "document_url": r.get("document_url", ""),
            "status": r.get("status", ""),
            "notes": r.get("notes", ""),
            "Título": r.get("Título", ""),
            "sincronizado_excel": r.get("sincronizado_excel", "False")
        }
        
        # Agregar TODOS los campos que vienen del Excel para que estén disponibles en el dashboard
        campos_excel = [
            'Resultado análisis', 'Fecha registro', 'Tipo', 'Anexos', 
            'Fecha de publicación', 'Emisor', 'Norma', 'Fecha de divulgación', 
            'Tipo de Norma', 'Tema', 'Sector Económico', 'Incidencia SURA', 
            'Obligaciones SURA', 'Norma Importante', 'Control SOX', 'Divulgación SOX', 
            'Compañía Impactada', 'Obligaciones', 'Persona que analizó', 
            'Justificación de no divulgación SOX'
        ]
        for field in campos_excel:
            row_data[field] = r.get(field, "")

        out_rows.append(row_data)

    order = {"ROJO": 0, "AMARILLO": 1, "VERDE": 2, "CONSOLIDADO": 3}
    out_rows.sort(key=lambda x: (order.get(x["semaforo"], 9), x["detected_at"]), reverse=True)

    with open(OUT_FILE, "w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "semaforo", "motivo", "detected_at", "entidad", "Título", "Norma", 
            "Resultado análisis", "status", "Incidencia SURA", "Control SOX",
            "Fecha de divulgación", "Compañía Impactada", "Persona que analizó",
            "fuente_url", "document_url", "notes", "sincronizado_excel"
        ]
        # Asegurar que todos los campos del Excel estén en los fieldnames si no están ya
        for fkey in out_rows[0].keys():
            if fkey not in fieldnames:
                fieldnames.append(fkey)
                
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(out_rows)

    print(f"Generado: {OUT_FILE} | filas={len(out_rows)} | {datetime.now().isoformat(timespec='seconds')}")


if __name__ == "__main__":
    main()
