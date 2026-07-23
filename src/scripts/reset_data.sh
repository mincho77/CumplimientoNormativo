#!/bin/bash
echo "⚠️ ATENCIÓN: Esto borrará todos los casos detectados y el progreso del monitor."
read -p "¿Estás seguro de continuar? (s/n): " confirm
if [ "$confirm" = "s" ]; then
    rm -f data/casos_detectados.csv
    rm -f data/tablero_semaforo.csv
    rm -f data/state/monitor_state.json
    rm -f data/state/sox_trace.json
    rm -rf raw/inbox/*
    echo "✅ Datos limpiados exitosamente. El sistema está como nuevo."
else
    echo "Operación cancelada."
fi
