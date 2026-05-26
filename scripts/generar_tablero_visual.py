#!/usr/bin/env python3
import csv
import os
from collections import Counter
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "data", "tablero_semaforo.csv")
OUT = os.path.join(ROOT, "Tablero Visual Cumplimiento.md")


def load_rows():
    if not os.path.exists(SRC):
        return []
    with open(SRC, "r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def to_row_md(r):
    return (
        f"| {r.get('detected_at','')} | {r.get('entidad','')} | {r.get('status','')} | "
        f"{r.get('priority','')} | {r.get('aplica_sura','')} | {r.get('motivo','')} | {r.get('document_url','')} |"
    )


def section(title, rows):
    lines = [
        f"<details>",
        f"<summary><b>{title} ({len(rows)})</b> — click para ver detalle</summary>",
        "",
        "| detected_at | entidad | status | priority | aplica_sura | motivo | document_url |",
        "|---|---|---|---|---|---|---|",
    ]
    lines.extend(to_row_md(r) for r in rows[:500])
    lines.append("")
    lines.append("</details>")
    return "\n".join(lines)


def main():
    rows = load_rows()
    c = Counter((r.get("semaforo", "") for r in rows))
    rojos = [r for r in rows if r.get("semaforo") == "ROJO"]
    amarillos = [r for r in rows if r.get("semaforo") == "AMARILLO"]
    verdes = [r for r in rows if r.get("semaforo") == "VERDE"]
    consolidados = [r for r in rows if (r.get("status", "").lower() == "consolidado")]

    md = f"""# Tablero Visual Cumplimiento

_Actualizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_

## Resumen Semáforo

| 🔴 ROJO | 🟡 AMARILLO | 🟢 VERDE | TOTAL |
|---:|---:|---:|---:|
| **{c.get('ROJO',0)}** | **{c.get('AMARILLO',0)}** | **{c.get('VERDE',0)}** | **{len(rows)}** |

## Consolidado
Casos en estado `consolidado`: **{len(consolidados)}**

{section('🔴 ROJO (revisar primero)', rojos)}

{section('🟡 AMARILLO (pendientes)', amarillos)}

{section('🟢 VERDE (cerrados/no aplica)', verdes)}

{section('✅ SOLO CONSOLIDADOS', consolidados)}
"""
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Generado: {OUT}")


if __name__ == "__main__":
    main()

