#!/usr/bin/env python3
import csv
import os
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CASES_FILE = os.path.join(ROOT, "data", "casos_detectados.csv")
OUT_FILE = os.path.join(ROOT, "data", "tablero_semaforo.csv")


def semaforo(status: str, priority: str, aplica: str):
    s = (status or "").strip().lower()
    p = (priority or "").strip().lower()
    a = (aplica or "").strip().lower()

    if s == "consolidado":
        return "CONSOLIDADO", "Integrado en matriz de obligaciones"
    if s in {"detectado", "extraido_ia", "en_validacion"}:
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
        with open(OUT_FILE, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(
                [
                    "semaforo",
                    "motivo",
                    "detected_at",
                    "entidad",
                    "fuente_url",
                    "document_url",
                    "status",
                    "priority",
                    "aplica_sura",
                    "link_status",
                    "link_error",
                    "notes",
                ]
            )
        print("No existe casos_detectados.csv; se creó tablero vacío.")
        return

    with open(CASES_FILE, "r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    out_rows = []
    for r in rows:
        color, motivo = semaforo(r.get("status", ""), r.get("priority", ""), r.get("aplica_sura", ""))
        out_rows.append(
            {
                "semaforo": color,
                "motivo": motivo,
                "detected_at": r.get("detected_at", ""),
                "entidad": r.get("entidad", ""),
                "fuente_url": r.get("fuente_url", ""),
                "document_url": r.get("document_url", ""),
                "status": r.get("status", ""),
                "priority": r.get("priority", ""),
                "aplica_sura": r.get("aplica_sura", ""),
                "link_status": r.get("link_status", ""),
                "link_error": r.get("link_error", ""),
                "notes": r.get("notes", ""),
            }
        )

    order = {"ROJO": 0, "AMARILLO": 1, "VERDE": 2}
    out_rows.sort(key=lambda x: (order.get(x["semaforo"], 9), x["detected_at"]), reverse=False)

    with open(OUT_FILE, "w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "semaforo",
            "motivo",
            "detected_at",
            "entidad",
            "fuente_url",
            "document_url",
            "status",
            "priority",
            "aplica_sura",
            "link_status",
            "link_error",
            "notes",
        ]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(out_rows)

    print(f"Generado: {OUT_FILE} | filas={len(out_rows)} | {datetime.now().isoformat(timespec='seconds')}")


if __name__ == "__main__":
    main()
