# 🟢 VERDE - Cerrados / No Aplica

> [!success]- **Validados y clasificados**
> **Acción**: Revisar si necesita consolidación a matriz de obligaciones.  
> _Casos rechazados, no aplicables o listos para consolidar_

## Casos

```csvtable
source: data/tablero_semaforo.csv
columns:
- entidad
- motivo
- aplica_sura
- status
- link_status
- detected_at
- priority
- document_url
filter:
- semaforo == "VERDE"
sortBy:
- expression: detected_at
  reversed: true
maxRows: 1000
```

> [!quote]- 📋 Leyenda
> - **Entidad**: Regulador  
> - **Motivo**: Razón clasificación  
> - **Aplica SURA**: Si/No/Parcial  
> - **Status**: Estado validación  
> - **Link Status**: ok | timeout | http_404 | http_403 | conexion_error  
> - **Priority**: Alta/Media/Baja
