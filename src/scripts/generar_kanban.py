#!/usr/bin/env python3
import csv
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CSV_PATH = os.path.join(ROOT, "data", "tablero_semaforo.csv")
KANBAN_PATH = os.path.join(ROOT, "wiki", "Tablero Kanban Cumplimiento.md")

def sincronizar_kanban_obsidian():
    # Estructura del tablero extendida
    tablero = {
        "ROJO": [],
        "AMARILLO": [],
        "VERDE": [],
        "CONSOLIDADO": [],
        "EJECUTADO": []
    }
    
    if not os.path.exists(CSV_PATH):
        print(f"Error: No se encontró el archivo {CSV_PATH}")
        return

    try:
        # Leer la información del CSV
        with open(CSV_PATH, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                semaforo = row.get("semaforo", "").upper()
                
                # Lógica para mover a la columna de EJECUTADO si ya tiene fecha o status específico
                divulgacion = row.get('Fecha de divulgación') or row.get('Divulgación SOX')
                if divulgacion and divulgacion.strip() and semaforo == "CONSOLIDADO":
                    semaforo = "EJECUTADO"

                if semaforo in tablero:
                    # Datos enriquecidos
                    entidad = row.get('entidad', 'Sin Entidad')
                    titulo = row.get('Título', 'Sin Título')
                    riesgo = row.get('riesgo_sancionatorio', 'Bajo')
                    linea = row.get('linea_negocio', 'Transversal')
                    
                    # Icono de riesgo
                    ic_riesgo = "⚪"
                    if riesgo == "Crítico": ic_riesgo = "🚨"
                    elif riesgo == "Alto": ic_riesgo = "🔥"
                    elif riesgo == "Medio": ic_riesgo = "⚠️"
                    
                    # Formato de tarjeta visualmente rico
                    tarjeta = f"- [ ] **{entidad}**<br>{ic_riesgo} *Riesgo {riesgo}* | 🏢 {linea}<br>_{titulo}_"
                    tablero[semaforo].append(tarjeta)
                    
    except Exception as e:
        print(f"Error procesando CSV: {e}")
        return

    # Generar el archivo Markdown para Obsidian Kanban
    try:
        with open(KANBAN_PATH, mode='w', encoding='utf-8') as f:
            # Frontmatter obligatorio para el plugin
            f.write("---\n\nkanban-plugin: basic\n\n---\n\n")
            
            # Escribir las columnas y sus tarjetas
            for columna, tarjetas in tablero.items():
                icono = ""
                if columna == "ROJO": icono = "🔴"
                elif columna == "AMARILLO": icono = "🟡"
                elif columna == "VERDE": icono = "🟢"
                elif columna == "CONSOLIDADO": icono = "🔵"
                
                f.write(f"## {icono} {columna}\n\n")
                for tarjeta in tarjetas:
                    f.write(f"{tarjeta}\n")
                f.write("\n")
                
            # Configuraciones finales del plugin
            f.write("%% kanban:settings\n")
            f.write("```\n")
            f.write('{"kanban-plugin":"basic"}\n')
            f.write("```\n")
            f.write("%%")
            
        print(f"Tablero Kanban generado exitosamente en {KANBAN_PATH}")
    except Exception as e:
        print(f"Error escribiendo archivo Kanban: {e}")

if __name__ == "__main__":
    sincronizar_kanban_obsidian()
