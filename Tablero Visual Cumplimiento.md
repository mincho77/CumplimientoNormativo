# Tablero Visual Cumplimiento

_Actualizado: 2026-05-26_

```dataviewjs
// 1. Leer el archivo CSV
const data = await dv.io.csv("data/tablero_semaforo.csv");

// 2. Inicializar contadores
let counts = { "ROJO": 0, "AMARILLO": 0, "VERDE": 0, "CONSOLIDADO": 0 };

// 3. Contar los registros según la columna 'semaforo'
for (let row of data) {
    if (counts[row.semaforo] !== undefined) {
        counts[row.semaforo]++;
    }
}

// 4. Configurar Obsidian Charts (Chart.js)
const chartData = {
    type: 'doughnut',
    data: {
        labels: ['🔴 ROJO', '🟡 AMARILLO', '🟢 VERDE', '🔵 CONSOLIDADO'],
        datasets: [{
            data: [counts.ROJO, counts.AMARILLO, counts.VERDE, counts.CONSOLIDADO],
            backgroundColor: ['#ef4444', '#f59e0b', '#22c55e', '#3b82f6'],
            borderWidth: 0,
            hoverOffset: 4
        }]
    },
    options: {
        plugins: {
            legend: { position: 'bottom' },
            title: { display: true, text: 'Distribución de Obligaciones Normativas' }
        }
    }
};

// 5. Renderizar el gráfico
window.renderChart(chartData, this.container);
```

> [!danger]- 🔴 ROJO (revisar primero)
> [[Tablero Detalle - ROJO]]

> [!warning]- 🟡 AMARILLO (pendientes)
> [[Tablero Detalle - AMARILLO]]

> [!success]- 🟢 VERDE (cerrados / no aplica)
> [[Tablero Detalle - VERDE]]

> [!tip]- ✅ SOLO CONSOLIDADOS
> [[Tablero Detalle - CONSOLIDADO]]

## Últimos casos

```csvtable
source: data/tablero_semaforo.csv
columns:
- semaforo
- entidad
- status
- priority
- detected_at
sortBy:
- expression: detected_at
  reversed: true
maxRows: 20
```
