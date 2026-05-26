#!/bin/bash

# Compliance Monitoring - Local Startup Script

set -e

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$ROOT/.venv"

echo "[run] iniciando | root=$ROOT"

# 1. Activate venv (or create if missing)
if [ ! -d "$VENV" ]; then
    echo "[run] creando virtualenv..."
    python3 -m venv "$VENV"
fi

source "$VENV/bin/activate"
echo "[run] venv activado"

# 2. Install dependencies
echo "[run] instalando dependencias..."
pip install -q -r "$ROOT/requirements.txt"

# 3. Run monitor
echo "[run] ejecutando monitor..."
python3 "$ROOT/scripts/monitor_fuentes.py" "$ROOT/data/Fuentes Normativas - limpio utf8 v2.csv"

# 4. Generate semaforo
echo "[run] generando semáforo..."
python3 "$ROOT/scripts/generar_tablero_semaforo.py"

# 5. Start Flask
echo "[run] iniciando Flask..."
echo ""
echo "=========================================="
echo "✅ Dashboard disponible en: http://localhost:5000"
echo "=========================================="
echo ""

python3 "$ROOT/app.py"
