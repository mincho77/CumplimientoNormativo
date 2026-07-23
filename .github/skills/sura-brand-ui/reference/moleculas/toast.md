# Mensaje emergente (Toast) — molécula

Fuente: `Toast.pdf` (2 páginas). Verificado contra imágenes renderizadas y muestreo
de píxeles. **Tipografía: Sura Sans. No aparece Barlow.**

## 1. Qué es

Los mensajes emergentes (toast) son elementos de retroalimentación que permiten a
los usuarios entender si una tarea o acción se ejecutó, o se modificó. También pueden
ser generados automáticamente por el sistema, para informar o advertir sobre una
acción determinada.

> **Reemplaza al `alert()` nativo informativo (efímero).** Todo mensaje de la app que
> solo **informa** un resultado o estado **efímero y de bajo peso** (guardado
> automático, "Copiado", info/advertencia/error que el usuario únicamente lee, **sin**
> pedir una decisión ni acusar un hito) debe mostrarse como **toast** de marca,
> **nunca** con el diálogo por defecto del navegador (`alert()`/`window.alert`).
>
> **Dos excepciones que NO son toast** (ver `moleculas/modales.md` §4.2):
> 1. Si el mensaje **pide una decisión o confirmación** → **modal base** (dos botones).
> 2. Si el mensaje **acusa el éxito de una acción ya completada que el usuario quiere
>    ver destacada** —**envío de formulario** o **solicitud generada exitosamente**—
>    → **modal de confirmación de éxito con un solo botón**
>    (`Cerrar`/`Aceptar`/`Continuar`/`Listo`), no un toast. El toast queda para las
>    micro-confirmaciones de fondo (autosave, "Copiado al portapapeles").

## 2. Anatomía

1. **Contenedor.**
2. **Ícono.**
3. **Título.**
4. **Subtítulo** (opcional).
5. **Descripción** (opcional).
6. **Botón de cierre** (`×`, opcional).

## 3. Construcción (medidas)

### Toast con descripción
- Padding de **16 px** en los cuatro lados (superior, inferior, izquierda, derecha).
- Espaciado entre **título y descripción**: 16 px.

### Toast simple
- Padding de **16 px** en los cuatro lados.
- El **ancho y alto** del contenedor son **automáticos** según el dispositivo.
- El texto descriptivo **no debe superar las 2 líneas**.

## 4. Colocación

- Aparecen **después de una acción** del usuario o se generan automáticamente por el
  sistema. Deben informar de forma **clara y concisa**.
- **Escritorio:** parte **inferior** de la pantalla.
- **Móvil:** parte **superior**.

### 4.1 Implementación — debe flotar sobre el viewport (no en el flujo del documento)

El toast tiene que verse **siempre, sin que el usuario tenga que desplazarse**
para encontrarlo. Por eso su contenedor va **`position: fixed`** anclado al borde
de la **ventana** (no del documento), con `z-index` por encima del header/sticky,
y entra animado (ver §4.2).

- **Nunca** lo insertes en el flujo normal del documento (p. ej. un `<div>` al
  inicio de un `<main>` con scroll): si el usuario está al final de la página, el
  toast aparece arriba fuera de vista y lo obliga a subir. **Esto es un bug de
  colocación, no un detalle.**
- Patrón correcto: un único `#alert-container` con
  `position: fixed; z-index: 200;` anclado abajo-centro (escritorio) o
  arriba-centro (móvil), `width: min(92%, 480px)`, y `pointer-events: none` en el
  contenedor + `pointer-events: auto` en cada toast (para no bloquear clics del
  fondo). El toast lleva su propia elevación (`dp`) para despegarse del contenido.

### 4.2 Animación de entrada/salida (obligatoria, ver `auditoria.md` §4.1)

El toast es un componente básico: **debe animar** su aparición y desaparición, no
parpadear de golpe. Anima `transform` + `opacity` (deslizamiento corto desde el
borde por el que entra) en ≈0.2–0.3 s con easing suave; al cerrarse, revierte.
Contempla `@media (prefers-reduced-motion: reduce)` para anular el movimiento.

## 5. Clasificación (estados / colores)

El tipo de toast se elige según el contexto o la acción. **Los colores no deben
modificarse**; cada uno representa una clase. Cada toast lleva una **barra de acento
izquierda** + ícono del color de la clase; el **título** va en azul.

| Clase | Acento / ícono | Fondo (tinte) |
|---|---|---|
| **Seguro** | Azul SURA `#0033A0` (muestreo `(10,59,164)`) | `#E1EBFF` (`(225,235,255)`) |
| **Advertencia** | Naranja `#EE8F0B` (muestreo `(238,143,11)`) | `#FFF4EB` (`(255,244,235)`) |
| **Error** | Rojo `#D12D35` (muestreo `(207,36,44)`) | `#FFF4F2` (`(255,244,242)`) |
| **Éxito** | Verde `#1A8736` (muestreo `(26,125,39)`) | `#DDF6DD` (`(221,246,221)`) |
| **Información** | Azul SURA `#0033A0` (muestreo `(10,59,164)`) | `#E1EBFF` (`(225,235,255)`) |

## 6. Uso

- **Seguro:** informa de la seguridad de la acción; generado automáticamente por el
  sistema en tratamiento de datos, políticas de privacidad, pagos, etc.
- **Éxito:** notifica que una tarea se completó con éxito (consecuencia de una acción
  del usuario).
- **Advertencia:** ambientes en los que el usuario debe terminar o reintentar una
  condición o estado de tarea ejecutada.
- **Información:** instrucciones o datos acerca de una acción ejecutada en un momento
  determinado; puede notificar al usuario sobre un cambio.
- **Titulares:** cortos y concisos, que den información suficiente. **Evitar títulos
  generales** como `Error`, `Información`, `Mensaje importante` (incorrecto).
- La **descripción** debe ser clara y puntual; **no más de 2 líneas** de texto.

## 7. Tokens CSS

```css
:root {
  /* Construcción */
  --toast-pad: 16px;                 /* 4 lados */
  --toast-title-desc-gap: 16px;
  /* ancho/alto automáticos; descripción ≤2 líneas */

  /* Clases — acento/ícono */
  --toast-secure: #0033A0;
  --toast-warning: #EE8F0B;
  --toast-error: #D12D35;
  --toast-success: #1A8736;
  --toast-info: #0033A0;

  /* Clases — fondo */
  --toast-secure-bg: #E1EBFF;
  --toast-warning-bg: #FFF4EB;
  --toast-error-bg: #FFF4F2;
  --toast-success-bg: #DDF6DD;
  --toast-info-bg: #E1EBFF;

  --font-toast: 'Sura Sans', 'Helvetica Neue', Arial, sans-serif;
}
```

## 8. Reglas operativas para el skill

- Toast = contenedor con **barra de acento izquierda** + ícono + título + descripción
  opcional + botón de cierre `×`; padding 16 px en los 4 lados; gap título↔descripción
  16 px; descripción ≤2 líneas; ancho/alto automáticos.
- **Cinco clases con color fijo** (no modificar): Seguro/Info azul `#0033A0`,
  Advertencia naranja `#EE8F0B`, Error rojo `#D12D35`, Éxito verde `#1A8736`; cada
  una con su fondo tinte correspondiente.
- Colocación: escritorio abajo, móvil arriba; aparecen tras una acción o por el
  sistema. **Debe flotar `position: fixed` sobre el viewport** (no en el flujo del
  documento), `z-index` por encima del header/sticky, visible **sin desplazarse**.
  Insertarlo dentro de un `<main>` con scroll es un bug de colocación (§4.1). Anima
  su entrada/salida (`transform`+`opacity`, ≈0.2–0.3 s) con `prefers-reduced-motion`
  (§4.2).
- Titulares concisos; **evitar** títulos genéricos (Error/Información/Mensaje
  importante).
- Tipografía Sura Sans; **nunca Barlow**.

## 9. Pendiente

- [ ] Confirmar el grosor exacto de la barra de acento (px) y el redondeo del
      contenedor (probable 12 px).
- [ ] Confirmar el verde de marca de "Éxito" contra la paleta oficial (muestreo
      `(26,125,39)` ≈ `#1A8736`).
- [ ] Confirmar tamaños de título y descripción en px (no impresos).
