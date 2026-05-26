#!/bin/bash

# Compliance Dashboard - Startup Script
# Ejecuta: monitor → semáforo → Flask

set -e

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$ROOT/.venv"

echo "=================================="
echo "📊 Compliance Dashboard Startup"
echo "=================================="

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
echo "[setup] limpiando puerto 5000..."
lsof -ti:5000 | xargs kill -9 2>/dev/null || true
sleep 1

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

casos = []
entidades = ['Superintendencia de Sociedades', 'Superintendencia Financiera', 'DIAN', 'Banco de la República', 'Procuraduría']
statuses = ['detectado', 'en_validacion', 'validado', 'consolidado']

for i in range(random.randint(60, 100)):
    status = statuses[i % len(statuses)]
    casos.append({
        'case_id': f'case_{i:04d}',
        'detected_at': (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d %H:%M:%S%z'),
        'entidad': random.choice(entidades),
        'fuente_url': f'https://gov.co/source/{random.randint(1, 10)}',
        'document_url': f'https://gov.co/docs/normativa_{i:03d}.pdf',
        'publication_date': '',
        'status': status,
        'priority': random.choice(['alta', 'media', 'baja']),
        'aplica_sura': random.choice(['si', 'no', 'parcial']),
        'link_status': random.choice(['ok', 'timeout', 'http_404', 'conexion_error']),
        'link_error': '' if random.random() > 0.3 else 'Connection timeout',
        'notes': f'Test case {i}'
    })

with open('data/casos_detectados.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=casos[0].keys())
    w.writeheader()
    w.writerows(casos)

print(f'[monitor] generado: {len(casos)} casos')
PYMOCK
fi

# 5. Semáforo
echo "[semaforo] generando..."
python3 "$ROOT/scripts/generar_tablero_semaforo.py" > /dev/null

# 6. Flask
echo ""
echo "=================================="
echo "✅ Dashboard listo"
echo "🌐 Abre: http://localhost:5000"
echo "=================================="
echo ""

python3 "$ROOT/app.py"
