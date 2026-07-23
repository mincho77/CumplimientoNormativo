#!/bin/bash

# Script para ejecutar solo el servidor Dashboard y regenerar vistas de Obsidian

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$(cd "$ROOT/.." && pwd)/.venv"

cd "$ROOT"

echo "=================================="
echo "🌐 Dashboard Server & Visuals"
echo "=================================="

# 1. Activate venv
if [ -d "$VENV" ]; then
    source "$VENV/bin/activate"
else
    echo "❌ Error: Virtualenv no encontrado. Ejecuta start.sh primero para configurar el entorno."
    exit 1
fi

# 2. Limpiar puerto 5050
echo "[server] limpiando puerto 5050..."
lsof -ti:5050 | xargs kill -9 2>/dev/null || true
sleep 1

# 3. Regenerar visuales antes de iniciar (para asegurar consistencia)
echo "[visuals] actualizando semáforo y kanban..."
python3 "$ROOT/scripts/generar_tablero_semaforo.py" > /dev/null
python3 "$ROOT/scripts/generar_kanban.py"

echo ""
echo "=================================="
echo "✅ Dashboard listo"
echo "🌐 URL: http://localhost:5050"
echo "=================================="
echo ""

# 4. Iniciar Flask
python3 "$ROOT/app.py"
