#!/bin/bash

# Compliance Dashboard - Startup Script
# Ejecuta: monitor → semáforo → Flask

set -e

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$ROOT/.venv"

echo "=================================="
echo "📊 Compliance Dashboard Startup"
echo "=================================="

# 0. Opcional: Limpiar datos
echo "⚠️ ¿Deseas limpiar todos los datos existentes para empezar de cero?"
read -p "Escribe 'limpiar' para confirmar o cualquier otra tecla para continuar: " CLEAN_CONFIRM

if [ "$CLEAN_CONFIRM" = "limpiar" ]; then
    echo "[clean] reseteando archivos de datos..."
    # Nuevo header alineado con Seguimiento Regulatorio 2026
    echo "case_id,Resultado análisis,Fecha registro,Tipo,Título,URL,Anexos,Fecha de publicación,Emisor,Norma,Fecha de divulgación,Tipo de Norma,Tema,Sector Económico,Incidencia SURA,Obligaciones SURA,Norma Importante,Control SOX,Divulgación SOX,Compañía Impactada,Obligaciones,Persona que analizó,Justificación de no divulgación SOX,detected_at,entidad,fuente_url,document_url,publication_date,status,priority,aplica_sura,link_status,link_error,notes" > "$ROOT/data/casos_detectados.csv"
    echo "semaforo,motivo,detected_at,entidad,fuente_url,document_url,Control SOX,status,Incidencia SURA,notes,Título,Norma,Tipo de Norma" > "$ROOT/data/tablero_semaforo.csv"
    echo "entidad,enlace,error" > "$ROOT/data/pendientes_enlaces.csv"
    
    echo "[clean] eliminando historial y estados..."
    rm -f "$ROOT/data/state/monitor_state.json"
    rm -f "$ROOT/data/state/sox_trace.json"
    rm -f "$ROOT/data/state/notifications.json"
    
    echo "[clean] eliminando documentos descargados..."
    rm -rf "$ROOT/raw/inbox"/*
    
    echo "[clean] limpiando Wiki de Obsidian..."
    rm -rf "$ROOT/wiki/casos"/*
    rm -rf "$ROOT/wiki/entidades"/*
    rm -rf "$ROOT/wiki/temas"/*
    
    echo "# Log de Operaciones de Cumplimiento" > "$ROOT/wiki/operations/log.md"
    echo "[clean] ¡Limpieza TOTAL completada!"
else
    echo "[clean] manteniendo datos existentes."
fi

# 1. Ensure venv
if [ ! -d "$VENV" ]; then
    echo "[setup] creando virtualenv..."
    python3 -m venv "$VENV"
fi

source "$VENV/bin/activate"
echo "[setup] venv ok"

# 2. Install deps
pip install -q -r "$ROOT/requirements.txt" 2>/dev/null || true

# 3. Kill old Flask if running
echo "[setup] limpiando puerto 5001..."
lsof -ti:5001 | xargs kill -9 2>/dev/null || true
sleep 1

START_TIME=$(date +"%Y-%m-%d %H:%M:%S")
echo "🕒 Inicio de procesamiento: $START_TIME"

# 4. Monitor
echo ""
echo "[menu] opciones:"
echo "  A) Monitor real (tarda ~5 min, visita fuentes)"
echo "  B) Mock rápido (segundos, datos de prueba)"
echo "  C) Solo servidor (usa datos existentes, sin monitor)"
echo ""
read -p "Elige (A/B/C) [B]: " CHOICE
CHOICE=${CHOICE:-B}

if [ "$CHOICE" = "C" ] || [ "$CHOICE" = "c" ]; then
    echo "[menu] saltando monitor (datos existentes)..."
elif [ "$CHOICE" = "A" ] || [ "$CHOICE" = "a" ]; then
    echo "[monitor] ejecutando real..."
    python3 "$ROOT/scripts/monitor_fuentes.py" "$ROOT/data/Fuentes Normativas - limpio utf8 v2.csv"
else
    echo "[monitor] ejecutando mock..."
    python3 << 'PYMOCK'
import csv
from datetime import datetime, timedelta
import random

fieldnames = [
    'case_id', 'Resultado análisis', 'Fecha registro', 'Tipo', 'Título', 
    'URL', 'Anexos', 'Fecha de publicación', 'Emisor', 'Norma', 
    'Fecha de divulgación', 'Tipo de Norma', 'Tema', 'Sector Económico', 
    'Incidencia SURA', 'Obligaciones SURA', 'Norma Importante', 'Control SOX', 
    'Divulgación SOX', 'Compañía Impactada', 'Obligaciones', 'Persona que analizó', 
    'Justificación de no divulgación SOX', 'detected_at', 'entidad', 'fuente_url', 
    'document_url', 'publication_date', 'status', 'priority', 'aplica_sura', 
    'link_status', 'link_error', 'notes'
]

casos = []
entidades = ['Superintendencia de Sociedades', 'Superintendencia Financiera', 'DIAN', 'Banco de la República', 'Procuraduría']
statuses = ['detectado', 'en_validacion', 'validado', 'consolidado']

for i in range(random.randint(60, 100)):
    status = statuses[i % len(statuses)]
    entidad = random.choice(entidades)
    casos.append({
        'case_id': f'case_{i:04d}',
        'detected_at': (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d %H:%M:%S%z'),
        'entidad': entidad,
        'Emisor': entidad,
        'fuente_url': f'https://gov.co/source/{random.randint(1, 10)}',
        'document_url': f'https://gov.co/docs/normativa_{i:03d}.pdf',
        'URL': f'https://gov.co/docs/normativa_{i:03d}.pdf',
        'status': status,
        'Control SOX': 'SÍ' if entidad in ['DIAN', 'Superintendencia Financiera'] else 'NO',
        'Incidencia SURA': 'pendiente',
        'notes': f'Mock: Revisión pendiente para {entidad}'
    })

with open('data/casos_detectados.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for c in casos:
        row = {fn: c.get(fn, '') for fn in fieldnames}
        w.writerow(row)

print(f'[monitor] generado: {len(casos)} casos mock')
PYMOCK
fi

# 5. Semáforo
echo "[semaforo] generando..."
python3 "$ROOT/scripts/generar_tablero_semaforo.py" > /dev/null

# 5.1 Kanban (Obsidian)
echo "[kanban] sincronizando..."
python3 "$ROOT/scripts/generar_kanban.py"

END_TIME=$(date +"%Y-%m-%d %H:%M:%S")
echo "🏁 Fin de procesamiento: $END_TIME"
echo "⏱️ Ventana de ejecución: desde $START_TIME hasta $END_TIME"

# 6. Flask
echo ""
echo "=================================="
echo "✅ Dashboard listo"
echo "🌐 Abre: http://localhost:5001"
echo "=================================="
echo ""

python3 "$ROOT/app.py"
