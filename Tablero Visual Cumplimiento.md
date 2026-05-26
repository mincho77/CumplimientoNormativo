# Tablero Visual Cumplimiento

_Actualizado: 2026-05-26_

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
