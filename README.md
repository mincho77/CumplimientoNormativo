# 📋 Compliance Monitoring Dashboard - Colombia

Sistema híbrido de monitoreo normativo y análisis de obligaciones regulatorias para Colombia.

**Stack:** Flask + Obsidian + Python + DataTables + Chart.js

---

## 🎯 Qué es

LLM Wiki + Dashboard interactivo para:
- Monitorear fuentes normativas oficiales (Superintendencias, DIAN, etc)
- Detectar documentos nuevos (PDFs, decretos, resoluciones)
- Validar si aplican a SURA (manual)
- Consolidar en matriz de obligaciones
- Analizar cambios regulatorios

## 🚀 Quick Start

### 1. Instala Python 3.9+
```bash
python3 --version
```

### 2. Crea venv
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Ejecuta el sistema

El flujo está dividido en dos partes:

**A) Monitor (Ingesta de datos):**
Ejecuta esto para buscar nuevos documentos en las fuentes oficiales o generar datos de prueba.
```bash
./run_monitor.sh
```

**B) Dashboard & Visuals (Servidor):**
Ejecuta esto para levantar la interfaz web y actualizar automáticamente el gráfico y el tablero Kanban en Obsidian.
```bash
./run_server.sh
```

### 4. Abre dashboard
```
http://localhost:5001
```

---

## 📊 Dashboard Features

### Tabla Interactiva
- Agrupa por semáforo (ROJO/AMARILLO/VERDE/CONSOLIDADO)
- Expandir/contraer grupos
- Filtros: entidad, prioridad, link_status
- Búsqueda por texto
- Columna con link a documento PDF

### Gráficos
- **Distribución por Semáforo** (doughnut con números visibles)
- **Top 10 Entidades** (bar chart horizontal)

### Semáforos
| Color | Significado | Qué hacer |
|-------|-------------|-----------|
| 🔴 ROJO | Alta prioridad | Revisar jurídicamente |
| 🟡 AMARILLO | Pendiente | Validar y consolidar |
| 🟢 VERDE | Cerrado/No aplica | Nada (monitorear cambios) |
| 🔵 CONSOLIDADO | En matriz | Monitorear actualizaciones |

---

## 🔧 Arquitectura

```
CumplimientoNormativo/
├── app.py                      # Flask app
├── scripts/
│   ├── monitor_fuentes.py      # Detecta PDFs en URLs fuente
│   ├── generar_tablero_semaforo.py  # Asigna semáforos
│   └── casos_update.py         # Actualiza casos manualmente
├── templates/index.html        # Dashboard UI
├── static/style.css            # Estilos
├── data/
│   ├── Fuentes Normativas - limpio utf8 v2.csv  # URLs a monitorear
│   ├── casos_detectados.csv    # Casos descubiertos
│   └── tablero_semaforo.csv    # Casos clasificados
├── wiki/                       # Obsidian vault (análisis manual)
└── start.sh                    # Script startup todo-en-uno
```

### Flujo de Datos

```
monitor_fuentes.py
  ↓ (visita URLs, busca .pdf)
casos_detectados.csv (link_status, link_error)
  ↓
generar_tablero_semaforo.py (asigna ROJO/AMARILLO/VERDE/CONSOLIDADO)
  ↓
tablero_semaforo.csv
  ↓
Flask API → Dashboard
```

---

## 📡 API Endpoints

### `GET /`
Dashboard UI.

### `GET /api/casos`
Retorna casos filtrados.

**Query params:**
- `semaforo`: ROJO, AMARILLO, VERDE, CONSOLIDADO
- `entidad`: Nombre regulador
- `priority`: alta, media, baja
- `link_status`: ok, timeout, http_404, http_403, conexion_error
- `search`: Búsqueda free-text

**Response:**
```json
[
  {
    "case_id": "abc123",
    "detected_at": "2026-05-26 09:41:44",
    "entidad": "Superintendencia de Sociedades",
    "document_url": "https://..../doc.pdf",
    "status": "detectado",
    "priority": "alta",
    "aplica_sura": "",
    "link_status": "ok",
    "link_error": "",
    "semaforo": "ROJO"
  }
]
```

### `GET /api/summary`
Contadores por semáforo.

---

## 🎮 Uso Manual

### Ejecutar monitor (fuentes reales)
```bash
python3 scripts/monitor_fuentes.py "data/Fuentes Normativas - limpio utf8 v2.csv"
```

Genera: `data/casos_detectados.csv` con campos:
- `case_id`: hash único
- `link_status`: ok | timeout | http_404 | http_403 | conexion_error
- `link_error`: mensaje de error

### Generar semáforo
```bash
python3 scripts/generar_tablero_semaforo.py
```

Genera: `data/tablero_semaforo.csv` con clasificación automática.

### Actualizar caso (validación manual)
```bash
python3 scripts/casos_update.py <case_id> <status> <priority> <aplica_sura> "<notes>"
```

**Ejemplo:**
```bash
python3 scripts/casos_update.py abc123 validado alta si "Aplica a operaciones de seguros"
```

---

## 🔍 Link Status

Errores capturados durante acceso a URLs:

| Status | Significado | Acción |
|--------|------------|--------|
| `ok` | Acceso exitoso | Procesar |
| `timeout` | URL lenta (>20s) | Reintentar |
| `http_404` | Documento perdido | Revisar URL |
| `http_403` | Acceso denegado | Solicitar acceso |
| `conexion_error` | Red/DNS | Revisar conectividad |
| `error_fuente` | Error accediendo fuente | Revisar fuente |

---

## 📚 Obsidian Vault

Análisis manual y documentación:
- `Tablero Visual Cumplimiento.md`: vista principal
- `Tablero Detalle - ROJO.md`: casos prioritarios
- `Tablero Detalle - AMARILLO.md`: casos pendientes
- `Tablero Detalle - VERDE.md`: casos cerrados
- `Tablero Detalle - CONSOLIDADO.md`: matriz de obligaciones

---

## ⚙️ Configuración

### `requirements.txt`
```
Flask==3.0.0
Werkzeug==3.0.1
```

### `start.sh`
Script completo que:
1. Limpia puerto 5001
2. Elige: Monitor real / Mock / Solo servidor
3. Genera semáforo
4. Levanta Flask

---

## 🚧 Limitaciones Actuales

- Detecta PDFs por regex, no valida contenido
- No extrae fecha de publicación automáticamente
- `aplica_sura` requiere validación manual
- Sin descarga de PDFs a `raw/`
- Sin extracción IA de obligaciones

## 📋 Próximas Mejoras

- [ ] Descargar PDFs a `raw/inbox/`
- [ ] Extraer `publication_date` de HTML
- [ ] IA para detectar si aplica a SURA
- [ ] Notificaciones (Teams/Email) en ROJO
- [ ] Extracción automática de obligaciones
- [ ] Versionado de cambios (auditoría)

---

## 🕒 Log de Sesiones

### [2026-05-27] Refactorización y Visualización en Obsidian
**Cambios:**
- **Separación de Concerns:** Se dividió `start.sh` en `./run_monitor.sh` (ingesta) y `./run_server.sh` (servidor y visuales) para mayor flexibilidad.
- **Tablero Kanban:** Se creó el script `scripts/generar_kanban.py` para sincronizar automáticamente el estado de los casos con una nota de Obsidian compatible con el plugin Kanban.
- **Gráficos Dinámicos:** Se integró un gráfico de dona en `Tablero Visual Cumplimiento.md` utilizando **DataviewJS**.
- **Automatización:** Los visuales se actualizan automáticamente al iniciar el servidor o al recibir cambios vía API.
- **Documentación:** Actualización de README con las nuevas instrucciones de ejecución.

---

## 🤝 Contribuir

1. Fork repo
2. Crea rama: `git checkout -b feature/mejora`
3. Commit: `git commit -m "Add: descripción"`
4. Push: `git push origin feature/mejora`
5. PR a `main`

---

## 📜 Licencia

Privado. Uso interno SURA.

---

## ✉️ Contacto

Mauricio Otálvaro  
Email: otalvaroospinamauricio@gmail.com
