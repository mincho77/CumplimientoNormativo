# Redacción y tono — Sistema de Diseño SURA

Filosofía de microcopy para que **toda interfaz sea lo más entendible posible
para el usuario final**. Aplica a textos de UI: etiquetas, placeholders,
botones, mensajes (toast/alert), estados vacíos, modales, errores y éxitos.

> **Alcance:** esto es para el *chrome* de la interfaz (lo que el sistema le
> dice al usuario). **No** reescribe contenido de dominio: títulos de sección,
> preguntas de un formulario/encuesta, textos legales o nombres propios se
> dejan como están salvo que el usuario lo pida.

---

## 1. Idioma y persona

- **Español, tuteo** ("tú" / "tu"). Nunca "usted" ni "vos".
- Voz cercana y profesional, no acartonada.
- Hablamos **desde la marca** ("guardamos tus respuestas"), no en impersonal
  frío ("se ha guardado el registro").

## 2. Sin emojis ni caracteres decorativos

- **Prohibido** `✓`, `❌`, `✔`, `⚠`, `💾`, `📤`, `📋` y similares en el texto.
- Si necesitas señalizar estado, usa **palabras**: "Listo", "Atención",
  "No pudimos…". El ícono visual (si lo hay) lo pone el componente, no el texto.

## 3. Principios de estilo

| Principio | Qué significa |
|---|---|
| **Claro** | Una idea por frase. Sin tecnicismos ("local", "SharePoint", "endpoint", "payload"). |
| **Simple** | Palabras cotidianas. Si una palabra se puede quitar, se quita. |
| **Conversacional** | Como se lo dirías a una persona, no a una máquina. |
| **Directo pero amable** | Vamos al grano sin sonar cortantes. |
| **Accionable** | Verbo claro de qué hacer ("Escribe tu nombre", "Revisa tu conexión"). |
| **No culpar al usuario** | El sistema asume la responsabilidad, no acusa. |

### No culpar — el patrón clave

| ❌ Culpa al usuario | ✅ El sistema responde |
|---|---|
| "Usted ingresó mal el dato" | "No encontramos ese dato" |
| "Error: campo obligatorio vacío" | "Escribe tu nombre para continuar" |
| "Formato inválido" | "Revisa el formato e inténtalo de nuevo" |

## 4. Adaptación por canal

| Canal | Fórmula | Ejemplo |
|---|---|---|
| **Éxito** (toast/alert) | Empieza con **"Listo"** o **"Hecho"** + qué pasó | "Listo, guardamos tus respuestas." |
| **Error** (toast/alert) | **Qué pasó** + **qué hacer** (sin culpar, sin código técnico) | "No pudimos enviar tus respuestas. Revisa tu conexión e inténtalo de nuevo." |
| **Etiqueta de campo** | Sustantivo corto o instrucción breve | "Tu nombre" |
| **Placeholder** | Acción accionable, no solo el dato esperado | "Escribe tu nombre completo" |
| **Botón** | Verbo + objeto en lenguaje del usuario (sin jerga del sistema) | "Enviar respuestas" (no "Enviar a SharePoint") |
| **Estado vacío** | Qué falta + qué esperar cuando haya datos | "Aún no has guardado respuestas. Cuando lo hagas, las verás aquí." |
| **Modal de confirmación** | Pregunta directa + consecuencia clara | "¿Eliminar esta respuesta? No se puede deshacer." |

## 5. Qué hacer / qué evitar

**Hacer:**
- Verbos de acción en placeholders y botones.
- Mensajes de error que digan el siguiente paso.
- Personalizar con variables del contexto cuando aporten ("tus respuestas",
  "este equipo").
- Mantener consistencia: si en un lado dices "Enviar respuestas", no digas
  "Mandar el formulario" en otro.

**Evitar:**
- Jerga técnica o de plataforma ("SharePoint", "flow", "local", "JSON").
- Mensajes que solo describen el error sin salida ("Error inesperado").
- Mayúsculas sostenidas para enfatizar.
- Signos `!` apilados o tono alarmista.
- Echarle la culpa al usuario.

## 6. Mini guía de frases

| Situación | Frase modelo |
|---|---|
| Guardado correcto | "Listo, guardamos tus respuestas en este equipo." |
| Envío correcto | "Listo, recibimos tus respuestas." |
| Falta el nombre | "Escribe tu nombre para continuar." |
| Falta responder | "Responde al menos una sección antes de continuar." |
| Falla de envío | "No pudimos enviar tus respuestas. Revisa tu conexión e inténtalo de nuevo." |
| Sin datos todavía | "Aún no has guardado respuestas. Cuando lo hagas, las verás aquí." |
| Cargando | "Enviando…" (gerundio breve, sin "Por favor espere") |

## 7. Reglas operativas para el skill

- En **MODO AUDITAR**, revisa el microcopy junto con tipografía/color: detecta
  emojis (`✓`/`❌`/etc.), jerga de plataforma, mensajes que culpan al usuario y
  errores sin acción. Corrígelos con los patrones de §3–§6.
- En **MODO GENERAR**, redacta todos los textos de UI con esta filosofía desde
  el inicio (placeholders accionables, éxitos con "Listo", errores con salida).
- **No toques contenido de dominio** (títulos, preguntas, legales, nombres)
  salvo petición explícita del usuario.
- En el reporte de cambios, incluye una línea por ajuste: *antes → después → por
  qué*, igual que el resto de la auditoría.

## 8. Pendiente

- [ ] Validar el set de frases modelo con el equipo de marca/contenido.
- [ ] Definir tono para confirmaciones destructivas (eliminar/cancelar) con
      ejemplos aprobados.
