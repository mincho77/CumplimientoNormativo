# 🔴 ROJO - Revisar Primero

> [!danger]- **Requiere revisión inmediata**
> **Acción**: Validar, clasificar y consolidar.  
> _Casos pendientes de validación manual + alta prioridad_

## Casos

```csvtable
source: data/tablero_semaforo.csv
columns:
- entidad
- motivo
- priority
- aplica_sura
- status
- link_status
- detected_at
- document_url
filter:
- semaforo == "ROJO"
sortBy:
- expression: priority
  reversed: true
- expression: detected_at
  reversed: true
maxRows: 1000
```

> [!tip]- 📋 Leyenda
> - **Entidad**: Regulador  
> - **Motivo**: Razón pendencia  
> - **Priority**: Alta/Media/Baja  
> - **Aplica SURA**: Si/No/Parcial  
> - **Status**: Estado validación  
> - **Link Status**: ok | timeout | http_404 | http_403 | conexion_error
