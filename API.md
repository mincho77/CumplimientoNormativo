# 📡 API Documentation

Dashboard API endpoints.

## Base URL
```
http://localhost:5001
```

---

## Endpoints

### `GET /`
**Dashboard UI**

Retorna página HTML con:
- Cards de resumen (ROJO/AMARILLO/VERDE/CONSOLIDADO)
- Filtros interactivos
- Tabla agrupable
- Gráficos

---

### `GET /api/casos`
**Obtener casos filtrados**

Retorna array de casos con opción de filtrar.

#### Query Parameters

| Param | Type | Description | Example |
|-------|------|-------------|---------|
| `semaforo` | string | Filtrar por semáforo | `ROJO`, `AMARILLO`, `VERDE`, `CONSOLIDADO` |
| `entidad` | string | Filtrar por regulador | `Superintendencia de Sociedades` |
| `priority` | string | Filtrar por prioridad | `alta`, `media`, `baja` |
| `link_status` | string | Filtrar por estado de link | `ok`, `timeout`, `http_404`, `http_403`, `conexion_error` |
| `search` | string | Búsqueda free-text | `seguros`, `decreto` |

#### Response (200 OK)
```json
[
  {
    "case_id": "a1b2c3d4e5f6g7h8",
    "detected_at": "2026-05-26 09:41:44+0000",
    "entidad": "Superintendencia de Sociedades",
    "fuente_url": "https://www.supersociedades.gov.co",
    "document_url": "https://www.supersociedades.gov.co/documents/doc.pdf",
    "publication_date": "2026-05-20",
    "status": "detectado",
    "priority": "alta",
    "aplica_sura": "si",
    "link_status": "ok",
    "link_error": "",
    "semaforo": "ROJO",
    "motivo": "Pendiente de revisión prioritaria (alta)",
    "notes": "Resolución de superintendencia"
  },
  ...
]
```

#### Examples

**Obtener todos los casos ROJO:**
```bash
curl "http://localhost:5001/api/casos?semaforo=ROJO"
```

**Filtrar AMARILLO de Superintendencia Financiera:**
```bash
curl "http://localhost:5001/api/casos?semaforo=AMARILLO&entidad=Superintendencia+Financiera"
```

**Buscar casos con error de conexión:**
```bash
curl "http://localhost:5001/api/casos?link_status=conexion_error"
```

**Búsqueda libre:**
```bash
curl "http://localhost:5001/api/casos?search=decreto"
```

#### Filtros combinados
```bash
curl "http://localhost:5001/api/casos?semaforo=ROJO&priority=alta&link_status=ok"
```

---

### `GET /api/summary`
**Obtener resumen de contadores**

Retorna cantidad de casos por semáforo.

#### Response (200 OK)
```json
{
  "ROJO": 5,
  "AMARILLO": 12,
  "VERDE": 8,
  "CONSOLIDADO": 23
}
```

#### Example
```bash
curl "http://localhost:5001/api/summary"
```

---

## Data Model

### Caso (Row en CSV)

| Field | Type | Description |
|-------|------|-------------|
| `case_id` | string | Hash único (SHA256[:16]) |
| `detected_at` | datetime | Fecha detección |
| `entidad` | string | Regulador/Ministerio |
| `fuente_url` | string | URL que se visitó |
| `document_url` | string | URL del PDF encontrado |
| `publication_date` | string | Fecha publicación (ISO 8601) |
| `status` | string | detectado, en_validacion, validado, consolidado, rechazado, error_fuente |
| `priority` | string | alta, media, baja (vacío = no asignada) |
| `aplica_sura` | string | si, no, parcial (vacío = no validado) |
| `link_status` | string | ok, timeout, http_404, http_403, conexion_error, error |
| `link_error` | string | Mensaje de error si link_status != ok |
| `notes` | string | Notas de revisión manual |

### Semáforo (Computed)

Asignado por `generar_tablero_semaforo.py`:

| Value | Condition | Motivo |
|-------|-----------|--------|
| ROJO | status IN (detectado, en_validacion) AND priority = alta | Pendiente de revisión prioritaria |
| AMARILLO | status IN (detectado, en_validacion) AND priority != alta | Pendiente de revisión manual |
| AMARILLO | status = validado | Validado, falta consolidar |
| VERDE | status = rechazado OR aplica_sura = no | Descartado / no aplica |
| CONSOLIDADO | status = consolidado | Integrado en matriz |

---

## Status Workflow

```
detectado
  ↓ (revisar documento)
en_validacion
  ↓ (validar si aplica)
validado  o  rechazado
  ↓ (si validado)
consolidado
```

---

## Link Status Reference

Capturado durante `fetch()` en `monitor_fuentes.py`:

| Status | HTTP Code | Meaning | Action |
|--------|-----------|---------|--------|
| `ok` | 200 | Descarga exitosa | Procesar |
| `http_404` | 404 | Documento no encontrado | URL rota, revisar |
| `http_403` | 403 | Acceso denegado | Solicitar permisos |
| `http_500` | 500 | Error servidor | Reintentar después |
| `timeout` | - | >20s esperando | Reintentar después |
| `conexion_error` | - | Red/DNS error | Verificar conectividad |
| `error` | - | Otro error | Ver `link_error` |
| `error_fuente` | - | Falla accediendo fuente completa | Revisar fuente |

---

## Rate Limiting

Sin límite actual. Producción: implementar si necesario.

---

## Authentication

Sin autenticación. Aplicar si acceso remoto.

---

## Error Handling

### 400 Bad Request
```json
{
  "error": "Invalid parameter"
}
```

### 500 Internal Server Error
```json
{
  "error": "CSV read error"
}
```

---

## Examples

### JavaScript/Fetch

```javascript
// Obtener casos ROJO
const response = await fetch('http://localhost:5001/api/casos?semaforo=ROJO');
const casos = await response.json();
console.log(casos);
```

### Python/Requests

```python
import requests

resp = requests.get('http://localhost:5001/api/casos', params={
    'semaforo': 'ROJO',
    'priority': 'alta'
})
casos = resp.json()
print(casos)
```

### cURL

```bash
# Resumen
curl http://localhost:5001/api/summary

# Casos ROJO alta prioridad con error de conexión
curl "http://localhost:5001/api/casos?semaforo=ROJO&priority=alta&link_status=conexion_error"
```

---

## CSV Files Reference

### `data/casos_detectados.csv`
Raw casos detectados por monitor. Incluye link_status y link_error.

### `data/tablero_semaforo.csv`
Casos con semáforo asignado por lógica automática. Input para API.

### `data/Fuentes Normativas - limpio utf8 v2.csv`
Listado de fuentes a monitorear:
- `Entidad`: nombre regulador
- `Enlace`: URL a visitar

---

## Deployment Notes

- Flask default: `localhost:5001`
- Para producción: usar Gunicorn + Nginx
- CSV location: `data/` (relativo a app.py)
- CORS: no configurado, agregar si acceso remoto
- HTTPS: configurar en reverse proxy

---

## Support

Issues: https://github.com/mincho77/CumplimientoNormativo/issues
