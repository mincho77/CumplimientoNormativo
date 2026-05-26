# 🟡 AMARILLO - Pendientes

> [!warning]- **Requiere seguimiento**
> **Acción**: Revisar, validar y consolidar cuando sea posible.  
> _Casos detectados sin validación manual o con estado pendiente_

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
- semaforo == "AMARILLO"
sortBy:
- expression: priority
  reversed: true
- expression: detected_at
  reversed: true
maxRows: 1000
```

> [!note]- 📋 Leyenda
> - **Entidad**: Regulador  
> - **Motivo**: Razón pendencia  
> - **Priority**: Alta/Media/Baja  
> - **Aplica SURA**: Si/No/Parcial  
> - **Status**: Estado validación  
> - **Link Status**: ok | timeout | http_404 | http_403 | conexion_error
