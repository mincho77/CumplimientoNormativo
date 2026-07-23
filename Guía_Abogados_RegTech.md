# ⚖️ Guía del Usuario: Cerebro Jurídico Estratégico

Esta herramienta transforma el monitoreo normativo de una lista de archivos en un **Grafo de Inteligencia Legal**. A continuación, se explica cómo el equipo jurídico debe utilizar este sistema para maximizar el control y la trazabilidad.

---

## 🚦 1. El Tablero de Control (Semáforo)
El tablero no es cronológico, es **estratégico**. Las normas se priorizan según su **impacto legal**:

*   **🔴 ROJO (Atención Inmediata):** 
    *   Normas con **Riesgo Crítico o Alto**.
    *   Normas con **Impacto SOX** (Controles financieros).
    *   Normas con impacto confirmado por la IA que requieren divulgación.
*   **🟡 AMARILLO (En Revisión):** 
    *   Normas nuevas pendientes de análisis manual.
    *   Validaciones técnicas en proceso.
*   **🟢 VERDE (Informativo/Descartado):** 
    *   Normas que no aplican a SURA o son repetitivas.

---

## 🕸️ 2. Navegación en Obsidian (El Grafo)
El mayor valor reside en las conexiones automáticas. Cada nota de norma en Obsidian ahora incluye enlaces bi-direccionales:

### ¿Cómo investigar en el Grafo?
1.  **Por Nivel de Riesgo:** Abre la nota `[[Riesgo Crítico]]`. En la vista de "Backlinks" o en el Grafo visual, verás todas las normas que actualmente estresan la operación.
2.  **Por Línea de Negocio:** Haz clic en `[[Seguros de Vida]]` o `[[Transversal]]` para ver el ecosistema normativo de un área específica.
3.  **Por Concepto Jurídico:** Las normas están vinculadas a `[[Temas]]` (ej: #Sarlaft, #Ciberseguridad). Esto permite ver la evolución de un concepto a través de diferentes emisores (SFC, BanRep, etc.).

---

## 📝 3. Anatomía de una Nota de Norma
Cada archivo generado en la carpeta `wiki/casos/` contiene:

*   **Metadata (Frontmatter):** Datos técnicos para filtros avanzados.
*   **Análisis Jurídico:** Un resumen generado por IA enfocado en la incidencia y obligaciones.
*   **Acciones de Cumplimiento:** Una lista de tareas (Checklist) para el abogado responsable:
    - [ ] Analizar impacto en procesos.
    - [ ] Verificar actualización de controles SOX.
*   **Responsables Sugeridos:** Enlaces a los roles encargados de la ejecución.

---

## 🛠️ 4. Flujo de Trabajo Recomendado
1.  **Mañana:** Revisar el Tablero en `http://localhost:5001` y filtrar por color **Rojo**.
2.  **Análisis:** Abrir la norma en Obsidian para leer el resumen de IA y seguir los enlaces de `[[Tema]]` para ver antecedentes.
3.  **Acción:** Marcar las tareas en el checklist de la nota de Obsidian.
4.  **Cierre:** Actualizar el estado a `consolidado` cuando la norma ya esté integrada en la matriz de obligaciones.

---

## 🚀 5. Mantenimiento (Comandos)
Para actualizar el cerebro con las últimas detecciones:
1.  Ejecutar búsqueda: `./src/run.sh`
2.  Sincronizar Wiki: `python3 src/scripts/generar_wiki_obsidian.py`

---
*Documentación generada por el Asistente RegTech - Junio 2026*
