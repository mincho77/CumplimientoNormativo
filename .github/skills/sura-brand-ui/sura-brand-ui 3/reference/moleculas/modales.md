# Modales (Modal / Dialog) — molécula

Fuente: `Modales.pdf` (2 páginas). Verificado contra imágenes renderizadas y
muestreo de píxeles. **Tipografía: Sura Sans. No aparece Barlow.**

## 1. Qué es

Un cuadro de diálogo o modal es una ventana que aparece frente al contenido de la
aplicación para proporcionar información crítica o solicitar una decisión. Los
modales deben tener un **moderador** (acción que solicite). Una alternativa menos
disruptiva es usar un **menú**, que brinda opciones sin interrumpir la experiencia
del usuario.

## 2. Anatomía

### Modal tipo básico
1. **Contenedor.**
2. **Pictograma/ícono** (opcional).
3. **Título** (opcional).
4. **Texto de apoyo.**
5. **Acciones.**

### Modal tipo lista
1. **Contenedor.**
2. **Ícono** (opcional).
3. **Título** (opcional).
4. **Texto de apoyo.**
5. **Lista con casilla de verificación.**
6. **Acciones** (puede llevar **barra de desplazamiento** opcional).

## 3. Variantes

| Variante | Uso |
|---|---|
| **Diálogo con pictograma** | El pictograma cumple función decorativa o representa algo (no es indicación). Refuerza el mensaje del modal. |
| **Diálogo base** | Modal sin pictograma; el más usado para confirmar una elección antes de comprometer una acción. |
| **Modal de confirmación de éxito (un solo botón)** | Acusa el **éxito de una acción ya completada** que el usuario quiere ver de forma destacada — p. ej. **envío de formulario** o **solicitud generada exitosamente**. Lleva **una sola acción** de cierre (`Cerrar` / `Aceptar` / `Continuar` / `Listo`), no el par confirmar/descartar. Ver §4.2. |
| **Modal tipo lista** | Brinda una lista de opciones (selectores tipo casilla) para ejecutar una acción; permite seleccionar más de una opción. |
| **Modal tipo lista con barra de desplazamiento** | Cuando la lista supera el área de lectura; la barra facilita la navegación y debe activarse al desbordar. |

## 4. Construcción (medidas)

| Elemento | Medida |
|---|---|
| Padding **vertical** | 16 px → 8 px |
| Padding **horizontal** (extremos y entre botones) | 24 px |
| Ancho **mínimo** de la tarjeta | 348 px |
| Ancho **máximo** de la tarjeta | 604 px (con dos botones con íconos) |
| Cuerpo de texto | 16 px Regular |
| Bajada de texto | 14 px Regular |
| Borde redondeado | 12 px |
| Botones de acción | tamaño **mediano** (ver `atomos/botones.md`) |

- El **tamaño horizontal** lo delimita el tamaño de los botones.
- El **título** no debe pasar de ~20 caracteres.

### Contenedor y malla
- Las superficies detrás del contenedor se **cubren/atenúan temporalmente** (overlay)
  para que se noten menos y el usuario se centre en el diálogo.
- Sombras en el modal (drop shadow) según el modelo.

### 4.1 Superposición a pantalla completa, sin scroll — OBLIGATORIO

El modal **siempre se superpone sobre la ventana completa** y queda visible sin que
el usuario tenga que desplazarse. Nunca se inserta dentro del flujo del documento
(eso lo empuja fuera de la vista y obliga a hacer scroll para verlo).

- **Overlay/velo:** capa de cobertura con `position: fixed; inset: 0;` que cubre
  **todo el viewport** (`100vw × 100vh`), por encima de todo el contenido.
  Color del velo: en claro `#0033A0 @ 0.10` (token `OVERLAY`), en oscuro
  `#000000 @ 0.45` (ver `generales/modo-oscuro.md` §4).
- **Tarjeta del modal:** **centrada** en el viewport (vertical y horizontalmente),
  también `position: fixed`. Si el contenido excede el alto disponible, el **scroll
  ocurre dentro de la tarjeta** (`max-height: 90vh; overflow-y: auto`), nunca en la
  página.
  > ⚠ **Cuidado con desplegables propios dentro del modal.** El `overflow-y: auto`
  > de la tarjeta **recorta los menús de los desplegables propios** (que son
  > `position: absolute` dentro del control) y de cualquier popover. En formularios
  > con desplegables, prefiere un modal **que quepa sin scroll interno** (baja la
  > densidad con un grid de 2 columnas) o renderiza el menú en un **portal**
  > `position: fixed` fuera del contenedor con scroll. No dejes que el menú se corte.
- **Capas (z-index):** el velo y la tarjeta van por encima de cualquier barra,
  header o sticky (`z-index` ≥ 300; por encima del `#alert-container` de toasts).
- **Bloqueo de fondo:** al abrir, bloquea el scroll del `body`
  (`overflow: hidden`) para que la atención quede en el diálogo; se restaura al
  cerrar.
- **Foco y accesibilidad:** mover el foco al modal al abrir, atrapar el foco
  mientras está abierto, cerrar con `Esc` y devolver el foco al disparador.
- **Animación de entrada/salida** (obligatoria, ver `auditoria.md` §4.1): el velo
  hace fade y la tarjeta entra con un leve `scale`/`translateY` + `opacity`,
  ≈0.15–0.25 s con easing suave; respeta `@media (prefers-reduced-motion: reduce)`.

### 4.2 Prohibido usar diálogos nativos del navegador — modal vs toast

**Nunca jamás** se dejan los diálogos por defecto del navegador
(`alert()`, `confirm()`, `prompt()`, `window.alert/confirm/prompt`) ni los
`Notification` del sistema operativo para comunicar mensajes de la aplicación.
Rompen la marca por completo (muestran `localhost:5173 dice…`, tipografía del SO,
sin colores ni íconos SURA) y, además, bloquean el hilo de la página.

- **En GENERAR:** desde el primer render, todo mensaje de la app se construye con un
  **toast** o un **modal** de marca; jamás se emite un `alert()`/`confirm()`.
- **En AUDITAR:** todo `alert()`/`confirm()`/`prompt()`/`window.*` en el código **es
  una desviación a corregir** — se reemplaza por el componente de marca que
  corresponda según la tabla siguiente, preservando la lógica (p. ej. la rama
  Aceptar/Cancelar de un `confirm` se cablea a los botones del modal).

**Regla de decisión (según el mensaje y su contenido):**

| El mensaje… | Componente de marca | Por qué |
|---|---|---|
| **Informa** un estado o resultado **efímero y de bajo peso** que el usuario solo lee (guardado automático, "Copiado", "Cambios guardados", info/advertencia/error sin decisión ni hito) | **Toast** (`moleculas/toast.md`) | No disruptivo; aparece superpuesto, se anima y se autodescarta. Usa la clase semántica (Éxito/Info/Advertencia/Error). |
| **Confirma el ÉXITO de una acción ya completada** que merece destacarse — **envío de un formulario** o **solicitud/petición generada exitosamente** (y casos análogos: registro creado, trámite radicado) | **Modal de confirmación de éxito (un solo botón)** (§3) | El usuario espera un acuse claro del hito; el modal lo detiene un instante con **una sola acción** de cierre (`Cerrar` / `Aceptar` / `Continuar` / `Listo`) — **no** el par confirmar/descartar, porque no hay decisión. |
| **Pide una decisión o confirmación** antes de comprometer una acción (continuar/cancelar, borrar, sobrescribir) | **Modal base** (este archivo) | Requiere moderador: dos botones, confirmar (derecha) / descartar (izquierda). Bloquea hasta que el usuario elige. |
| Pide **un dato** de entrada (lo que haría un `prompt`) | **Modal tipo lista / con campo** | Mismo patrón de modal con un campo SURA, no el `prompt` nativo. |

- Un `confirm()` nativo (dos botones, decisión) → **modal base** con dos acciones.
- Un `alert()` nativo informativo (un botón "OK"):
  - Si solo informa algo **efímero/menor** (guardado, copiado, aviso sin hito) →
    **toast** de la clase semántica adecuada.
  - Si acusa el **éxito de una acción completada que el usuario quiere ver
    destacada** (formulario enviado, solicitud generada) → **modal de confirmación
    de éxito con un solo botón** (`Cerrar`/`Aceptar`/`Continuar`/`Listo`).
  - Si el mensaje es **crítico** y debe bloquear el flujo hasta acuse de recibo →
    **modal** (un botón si solo informa; dos si pide decidir).
- **Cómo elegir entre toast de éxito y modal de éxito:** el **toast** es para
  micro-confirmaciones de fondo que no interrumpen (autosave, "Copiado al
  portapapeles"); el **modal de un botón** es para **hitos** que el usuario acaba
  de provocar y quiere ver acusados (un formulario que envió, una solicitud que
  generó). Ante la duda en un envío de formulario o una solicitud generada, usa el
  **modal de un botón** (preferencia explícita de marca).
- El modal de confirmación de éxito usa la **misma anatomía y medidas** del modal
  base (§4 y §8); solo cambia que lleva **una única acción** alineada a la derecha,
  con la etiqueta accionable que corresponda (`Cerrar`/`Aceptar`/`Continuar`/
  `Listo`). Puede incluir pictograma/ícono de éxito (decorativo, §3) y mantiene la
  superposición a pantalla completa y la animación de §4.1.
- Ambos —toast y modal— **se superponen a pantalla completa y son visibles sin
  scroll** (§4.1 para modal; `toast.md` §4.1 para toast).

## 4.bis Mobile / Responsivo

Fuente: *Modales - mobile.pdf*. La anatomía (tipos básico y lista), las variantes
(§3), la superposición a pantalla completa (§4.1) y la prohibición de diálogos
nativos (§4.2) son **idénticas** a la versión web — **no se repiten**. Lo nuevo de
la lámina móvil son las **medidas de construcción de la tarjeta** y un **borde
redondeado distinto**.

### Construcción móvil — dos variantes
| Elemento | Modal básico | Modal lista (con barra de desplazamiento) |
|---|---|---|
| Padding **vertical** | 16 px → 8 px | 16 px → 8 px |
| Padding **horizontal** | **16 px** (extremos y entre botones) | **24 px** |
| Ancho **mínimo** tarjeta | 348 px | 348 px |
| Ancho **máximo** tarjeta | 604 px (dos botones con ícono) | 604 px |
| **Alto** de la tarjeta | **348 px** | **418 px** |
| Título | **20 px Bold** (≤20 caracteres) | **20 px Bold** |
| Cuerpo de texto | **14 px Regular** | **14 px Regular** |
| Bajada de texto | 14 px Regular | 14 px Regular |
| Borde redondeado | **24 px solo esquinas superiores** | **24 px solo esquinas superiores** |
| Botones de acción | tamaño **pequeño** | tamaño **pequeño** |

> **Diferencias clave web↔móvil** (lo único que cambia):
> - **Cuerpo de texto: 14 px** en móvil (web 16 px).
> - **Borde redondeado: 24 px y solo en las esquinas superiores** (web 12 px en las
>   cuatro). El móvil ancla la tarjeta abajo/centrada y redondea arriba como una
>   *bottom-sheet*; las esquinas inferiores quedan rectas.
> - **Botones Acción tamaño pequeño** (web mediano), ver `atomos/botones.md`.
> - **Padding horizontal 16 px** en el básico (web 24 px); el tipo lista conserva
>   **24 px**.
> - Altura explícita de la tarjeta: **348 px** (básico) / **418 px** (lista).
>
> El resto (overlay a pantalla completa, scroll dentro de la tarjeta, foco,
> animación de entrada/salida, confirmar a la derecha) es igual a §4.1.

## 5. Colores

| Rol | Hex |
|---|---|
| Botón de acción primario (Acción 1) / título activo | `#2D6DF6` (muestreo `(45,109,246)`) |
| Borde lila claro de contenedores de campo/lista | `#CCDAFF` |

> El azul de acción es el **Azul Vivo SURA `#2D6DF6`**, el mismo precedente de Campos
> y Pestañas. El botón secundario (Acción 2) va en estilo outline.

## 6. Modo oscuro activado

El modal tiene variante en **modo oscuro**:

| Rol | Hex |
|---|---|
| Fondo del modal | Azul muy oscuro `#00003F` (muestreo `(0,0,63)`) |
| Botón de acción (acento) | Amarillo `#E2E828` (muestreo `(226,232,40)`) |

- Título **22 px Bold**; cuerpo **16 px Regular**.
- Ancho mínimo **348 px** (mismo que claro).
- Aplica a las tres variantes (con ícono, base, tipo lista).

## 7. Uso

- El propósito de un modal debe ser **comunicado** con su título y botones, con
  elementos procesables. Los **titulares** deben:
  - Contener una declaración o pregunta breve y clara.
  - Evitar disculparte (no pedir perdón por la interrupción).
  - Evitar la alarma adicional (p. ej. `¡Advertencia!`).
  - Evitar ambigüedades (p. ej. `¿Está seguro de querer ejecutar esta acción?`).
- **Botones / acciones:**
  - Se representan con **mayor frecuencia** como botones; la acción de confirmar,
    descartar o responder.
  - La acción de **confirmación** se alinea al **lado final** de la pantalla (lado
    derecho), y la de **descartar/rechazo** a su **izquierda**.
  - **Correcto:** desbloquear las acciones de confirmación hasta que se ejecute una
    acción. **Incorrecto:** dejar habilitadas las acciones de confirmación cuando no
    corresponde, o invertir la ubicación (confirmación a la izquierda).
- El ancho del modal **no** debe definirse por los botones de forma manual; se define
  por el componente.

## 8. Tokens CSS

```css
:root {
  /* Construcción */
  --modal-pad-y: 16px;              /* hasta 8px */
  --modal-pad-x: 24px;              /* extremos y entre botones */
  --modal-min-w: 348px;
  --modal-max-w: 604px;
  --modal-radius: 12px;
  --modal-body-size: 16px;          /* cuerpo, regular */
  --modal-caption-size: 14px;       /* bajada, regular */

  /* Construcción móvil (Modales - mobile) */
  --modal-mobile-pad-x-basic: 16px; /* básico: extremos y entre botones */
  --modal-mobile-pad-x-list: 24px;  /* tipo lista */
  --modal-mobile-h-basic: 348px;    /* alto tarjeta básico */
  --modal-mobile-h-list: 418px;     /* alto tarjeta lista */
  --modal-mobile-body-size: 14px;   /* cuerpo en móvil (web 16) */
  --modal-mobile-title-size: 20px;  /* título bold */
  --modal-mobile-radius-top: 24px;  /* solo esquinas superiores */
  /* Botones de acción en móvil = tamaño pequeño (atomos/botones.md) */

  /* Colores claro */
  --modal-action: #2D6DF6;          /* botón Acción 1 / título activo */
  --modal-field-border: #CCDAFF;    /* lila claro */

  /* Modo oscuro */
  --modal-dark-bg: #00003F;
  --modal-dark-action: #E2E828;     /* botón de acento amarillo */
  --modal-dark-title-size: 22px;    /* bold */

  --font-modal: 'Sura Sans', 'Helvetica Neue', Arial, sans-serif;
}
```

## 9. Reglas operativas para el skill

- Modal con overlay que atenúa el fondo; tarjeta `border-radius: 12px`, padding
  24 px lados / 16→8 px vertical; ancho 348–604 px; cuerpo 16 px, bajada 14 px.
- Dos tipos: **básico** (ícono opcional + título + apoyo + acciones) y **lista**
  (con casillas de verificación y barra de desplazamiento al desbordar).
- Variantes: diálogo con pictograma (decorativo), diálogo base (el más usado) y
  **modal de confirmación de éxito (un solo botón)** para acusar acciones
  completadas (envío de formulario, solicitud generada) — ver §3 y §4.2.
- Acciones = botones **medianos**; **confirmar a la derecha**, descartar a la
  izquierda; nunca invertir. El **modal de confirmación de éxito lleva una sola
  acción** alineada a la derecha (`Cerrar`/`Aceptar`/`Continuar`/`Listo`), sin par
  confirmar/descartar (no hay decisión).
- Botón primario `#2D6DF6` (outline para el secundario).
- Modo oscuro: fondo `#00003F`, botón de acento amarillo `#E2E828`, título 22 px Bold.
- Titulares concisos: sin disculpas, sin alarmas, sin ambigüedad; ≤~20 caracteres.
- Tipografía Sura Sans; **nunca Barlow**.
- **Superposición a pantalla completa, sin scroll** (§4.1): velo `position: fixed;
  inset: 0` sobre todo el viewport + tarjeta **centrada** (también `fixed`); el
  scroll, si lo hay, ocurre dentro de la tarjeta (`max-height: 90vh; overflow-y:
  auto`), nunca en la página; bloquea el scroll del `body` al abrir; `z-index` por
  encima de todo (≥300). Animación de entrada/salida obligatoria.
- **Prohibido `alert`/`confirm`/`prompt`/`window.*` nativos** (§4.2): se reemplazan
  según el contenido — **toast** (info efímera sin decisión), **modal de
  confirmación de éxito de un botón** (acción completada destacada: formulario
  enviado, solicitud generada) o **modal base de dos botones** (pide
  decisión/confirmación). En AUDITAR, todo diálogo nativo es desviación a corregir
  conservando la lógica.

- **Editar registros → modal.** En módulos de administración, abre la creación/
  edición de un registro en un **modal**, no en otra navegación/subvista: da
  consistencia y mantiene la lista visible detrás. Cancelar / `Esc` / clic en el
  velo cierran; Guardar valida y cierra.
- **Desplegables dentro de modal:** evita `overflow:auto` en la tarjeta si contiene
  desplegables propios (recorta el menú); prefiere un modal que quepa sin scroll
  interno o un menú en portal `fixed` (ver §4.1).

## 10. Pendiente

- [ ] Confirmar el ancho/alto exacto del modelo tipo lista y el grosor de la barra
      de desplazamiento.
- [ ] Confirmar el redondeo del botón de acento en modo oscuro y el contraste del
      texto sobre amarillo.

> Resuelto: el color del velo/overlay se toma del token `OVERLAY` de
> `generales/modo-oscuro.md` §4 — claro `#0033A0 @ 0.10`, oscuro `#000000 @ 0.45`.
