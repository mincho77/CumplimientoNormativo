#!/bin/bash

# Script para ejecutar el monitor de fuentes (Ingesta de datos)

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$(cd "$ROOT/.." && pwd)/.venv"
SOURCES_FILE="${1:-$(cd "$ROOT/.." && pwd)/data/Fuentes Normativas - limpio utf8 v2.csv}"

cd "$ROOT"

echo "=================================="
echo "🔍 Monitor de Fuentes Normativas"
echo "=================================="

# Profundidad por defecto: un nivel más que antes (2).
export MONITOR_MAX_DEPTH="${MONITOR_MAX_DEPTH:-2}"
echo "[monitor] profundidad activa MONITOR_MAX_DEPTH=$MONITOR_MAX_DEPTH"

# 1. Activate venv
if [ -d "$VENV" ]; then
    source "$VENV/bin/activate"
else
    echo "❌ Error: Virtualenv no encontrado. Ejecuta start.sh primero para configurar el entorno."
    exit 1
fi

# 2. Monitoreo real
echo "[monitor] ejecutando barrido real..."
python3 "$ROOT/scripts/monitor_fuentes.py" "$SOURCES_FILE"

# 3. Procesar resultados (sin IA)
if [ "${MONITOR_SKIP_POSTPROCESS:-0}" != "1" ]; then
    echo "[process] actualizando semáforo y kanban..."
    python3 "$ROOT/scripts/generar_tablero_semaforo.py"
    python3 "$ROOT/scripts/generar_kanban.py"
fi

echo "✅ Proceso completado. Ahora puedes ejecutar el script de IA o el servidor."
