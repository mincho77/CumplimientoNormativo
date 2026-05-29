#!/usr/bin/env python3
import csv
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSV_PATH = os.path.join(ROOT, "data", "tablero_semaforo.csv")
KANBAN_PATH = os.path.join(ROOT, "wiki", "Tablero Kanban Cumplimiento.md")

def sincronizar_kanban_obsidian():
    # Estructura del tablero
    tablero = {
        "ROJO": [],
        "AMARILLO": [],
        "VERDE": [],
        "CONSOLIDADO": []
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
                if semaforo in tablero:
                    # Crear la tarjeta Kanban
                    entidad = row.get('entidad', 'Sin Entidad')
                    titulo = row.get('Título', 'Sin Título')
                    notes = row.get('notes', 'Sin notas')
                    
                    # Formato de tarjeta más rico
                    tarjeta = f"- [ ] **{entidad}**<br>_{titulo}_<br>{notes}"
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
