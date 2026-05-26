# ✅ CONSOLIDADOS - Matriz Obligaciones

> [!success]- **Integrados en matriz**
> **Acción**: Monitorear actualizaciones de fuente o cambios regulatorios.  
> _Casos validados y consolidados en matriz de obligaciones_

## Casos Consolidados

```csvtable
source: data/tablero_semaforo.csv
columns:
- entidad
- aplica_sura
- priority
- link_status
- detected_at
- document_url
filter:
- status == "consolidado"
sortBy:
- expression: detected_at
  reversed: true
maxRows: 1000
```

> [!quote]- 📋 Leyenda
> - **Entidad**: Regulador  
> - **Aplica SURA**: Si/No/Parcial  
> - **Priority**: Alta/Media/Baja  
> - **Link Status**: ok | timeout | http_404 | http_403 | conexion_error  
> - **Detected**: Fecha detección
