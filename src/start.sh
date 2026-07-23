#!/bin/bash

# Compliance Dashboard - Startup Script
# Ejecuta: monitor → semáforo → Flask

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$(cd "$ROOT/.." && pwd)/.venv"

cd "$ROOT"

echo "=================================="
echo "📊 Compliance Dashboard Startup"
echo "=================================="

# 0. Opcional: Limpiar datos
echo "⚠️ ¿Deseas limpiar todos los datos existentes para empezar de cero?"
read -p "Escribe 'limpiar' para confirmar o cualquier otra tecla para continuar: " CLEAN_CONFIRM

if [ "$CLEAN_CONFIRM" = "limpiar" ]; then
    echo "[clean] reseteando archivos de datos..."
    # Nuevo header alineado con Seguimiento Regulatorio 2026
    echo "case_id,Resultado análisis,Fecha registro,Tipo,Título,URL,Anexos,Fecha de publicación,Emisor,Norma,Fecha de divulgación,Tipo de Norma,Tema,Sector Económico,Incidencia SURA,Obligaciones SURA,Norma Importante,Control SOX,Divulgación SOX,Compañía Impactada,Obligaciones,Persona que analizó,Justificación de no divulgación SOX,detected_at,entidad,fuente_url,document_url,publication_date,status,priority,aplica_sura,link_status,link_error,notes,analisis_ia_status,analisis_ia_fecha,tokens_ia,sincronizado_excel" > "$ROOT/data/casos_detectados.csv"
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
echo "[setup] limpiando puerto 5500..."
lsof -ti:5050 | xargs kill -9 2>/dev/null || true
sleep 1

START_TIME=$(date +"%Y-%m-%d %H:%M:%S")
echo "🕒 Inicio de procesamiento: $START_TIME"

# 4. Monitor
echo ""
echo "[menu] opciones:"
echo "  A) Monitor real (tarda ~5 min, visita fuentes)"
echo "  C) Solo servidor (usa datos existentes, sin monitor)"
echo ""
read -p "Elige (A/C) [C]: " CHOICE
CHOICE=${CHOICE:-C}

if [ "$CHOICE" = "C" ] || [ "$CHOICE" = "c" ]; then
    echo "[menu] saltando monitor (datos existentes)..."
elif [ "$CHOICE" = "A" ] || [ "$CHOICE" = "a" ]; then
    echo "[monitor] ejecutando real..."
    python3 "$ROOT/scripts/monitor_fuentes.py" "$(cd "$ROOT/.." && pwd)/data/Fuentes Normativas - limpio utf8 v2.csv"
else
    echo "❌ Opción inválida. Usa A para monitor real o C para solo servidor."
    exit 1
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
echo "🌐 Abre: http://localhost:5050"
echo "=================================="
echo ""

python3 "$ROOT/app.py"
