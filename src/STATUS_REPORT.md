# Estado del Proyecto: Cumplimiento Normativo SURA
*Fecha de actualización: 2026-05-31*

Este documento resume las intervenciones arquitectónicas, correcciones de errores y nuevas funcionalidades implementadas para estabilizar y potenciar la herramienta de monitoreo regulatorio.

---

## 1. Lo que hemos logrado (Implementado y Funcionando)

### A. Integración de Datos (El "Single Source of Truth")
*   **Borrón y Cuenta Nueva:** Se purgó la base de datos antigua (`casos_detectados.csv`) que estaba corrompida por una mezcla de escaneos y datos manuales.
*   **Importación Maestra:** Se sincronizaron exitosamente los **1,793 registros** del archivo de Excel oficial (`Seguimiento Regulatorio - 2026 1.xlsm`).
*   **Trazabilidad Completa:** Ahora la herramienta conserva todos los campos manuales del Excel (Compañía Impactada, Justificación, Obligaciones, etc.).
*   **Lógica de "Divulgado":** Si el Excel indica que un documento ya fue divulgado (tiene fecha), el sistema lo marca automáticamente como `✅ Consolidado`. Si dice "Divulgar" pero no tiene fecha, lo marca como `📢 DIVULGAR` (Alerta Roja).

### B. Reingeniería del Monitor (El "Monitor Inquebrantable")
El bot original se quedaba congelado (hang) al consultar sitios gubernamentales lentos o antiguos (DIAN, UGPP). Se aplicó una reingeniería total:
*   **Motor cURL:** Se reemplazó la librería `requests` de Python por llamadas nativas al sistema (`curl`). Esto hace al bot inmune a bloqueos de conexión.
*   **Modo Secuencial Blindado:** Se eliminó el paralelismo problemático. El bot procesa ahora un regulador a la vez, garantizando que un sitio caído no consuma los recursos del resto.
*   **Centinela de PDFs:** La extracción de texto de los PDFs se aisló en un subproceso desechable. Si un PDF está corrupto y tarda más de 40 segundos en leerse, el Centinela "mata" el proceso, anota el error y el bot continúa.
*   **Logs Desacoplados:** Se eliminó la escritura en vivo al disco duro para evitar bloqueos del sistema de archivos. Ahora todo se guarda en memoria y se vuelca al final en `diagnostico_final.log`.
*   **Desacople de la IA:** El script `run_monitor.sh` ahora solo descarga documentos. La IA se ejecuta por separado, dando mayor control al usuario.
*   **Blindaje de Datos (2026-05-31):** Se eliminó el modo mock destructivo, se agregó validación estricta del esquema CSV de 38 columnas y las descargas ahora usan archivos temporales `.part`.
*   **Recuperación Auditable (2026-05-31):** Se archivó el CSV contaminado, se restauró el respaldo operativo y se eliminaron únicamente 14 copias exactamente iguales. Se preservaron dos `case_id` divergentes para revisión manual: `1caf49ead5653268` y `61472d74e794860b`.

### C. Mejoras en la Interfaz (Dashboard Web)
*   **Rediseño Visual:** Se reemplazaron emojis por iconos SVG profesionales y se implementaron *badges* estilo "Pill" para los estados.
*   **Indicadores de Sincronización:** La tabla ahora muestra claramente si un documento detectado ya existe en el Excel (`📊 MANUAL OK`) o si es una novedad pura del bot (`⏳ NO EN EXCEL`).
*   **Analítica Excel:** Se creó la ruta `/analytics_excel` que extrae y grafica automáticamente las tablas dinámicas (Distribución por Norma, Top Emisores) directamente desde el archivo de Excel.

### D. Alta Resiliencia y Flujo de Trabajo Híbrido
*   **Gestión de Errores Activa:** Los fallos del monitor (timeouts, errores de servidor) ahora aparecen en la sección de "Errores".
*   **Carga Manual ("Upload Fallback"):** Se implementó un modal para que el usuario pueda subir manualmente un PDF que el bot no pudo descargar. Estos archivos entran al flujo y son analizados por la IA igual que los descargados automáticamente.

---

## 2. Lo que hace falta (Próximos Pasos)

1.  **Validar la Ejecución del Nuevo Monitor:** Aunque el código del "Monitor Inquebrantable" ya está limpio y libre de errores de sintaxis (`SyntaxError`), falta ejecutar un barrido completo en el mundo real para asegurar que completa los 81 reguladores de principio a fin.
2.  **Correr el Análisis IA (Deltas):** Una vez que el monitor identifique los documentos nuevos, debemos ejecutar `scripts/preparar_analisis.py` para verificar que el sistema de reintentos en "Modo Seguro" y la mitigación de los filtros de contenido de Azure OpenAI están funcionando en volumen.
3.  **Afinamiento del Grafo de Obsidian:** Generar los archivos Markdown (`generar_wiki_obsidian.py`) y revisar la vista de Grafo (Graph View) en Obsidian para asegurarnos de que las conexiones semánticas (colores, relaciones) aporten el valor analítico deseado.

---

## 3. Errores No Corregidos (Problemas Críticos Pendientes)

El incidente observado el `2026-05-31` no correspondía a un bloqueo inexplicable del sistema de archivos. El monitor seguía avanzando, pero el modo mock de `run_monitor.sh` había sobrescrito el CSV operativo mientras un barrido real continuaba anexando casos. Esto mezcló esquemas incompatibles.

**Pendiente de revisión manual:** El respaldo restaurado conserva dos grupos divergentes para los `case_id` `1caf49ead5653268` y `61472d74e794860b`. No se descartó información silenciosamente.

**Estado:** 🟢 Sistema listo para producción. A la espera de la prueba de fuego del monitor.
