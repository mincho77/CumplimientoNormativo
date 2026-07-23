# Información sobre herramientas (Tooltip) — molécula

Fuente: `Tooltip.pdf` (varias láminas). Verificado contra imágenes renderizadas y
muestreo de píxeles. **Tipografía: Sura Sans. No aparece Barlow.**

> ⚠ **Nota de color (aplica «confía en la muestra renderizada»):** el fondo del
> tooltip se rotula "Azul SURA `#26328C`", pero la **muestra renderizada real** es
> `#0033A0` (muestreo `(0,51,160)`). Usa **`#0033A0`** — mismo precedente de Migas
> de pan y Campos. El `#26328C` impreso es un export poco fiable.

## 1. Qué es

La información sobre herramientas o "Tooltip" se usa normalmente para brindar
información adicional sobre un tema cuando el usuario **pasa el cursor** sobre un
elemento. El tooltip **desaparece** al quitar el cursor. Por ello, instrucciones y
otra información práctica como **requisitos de campo no** deben incluirse en un
tooltip: para esos casos se usa una **ventana de notificación** (popover) en su
lugar (ver §5).

## 2. Anatomía (Tooltip)

1. **Contenedor.**
2. **Puntero** (la flecha/triángulo que apunta al elemento).
3. **Texto.**
4. **Ícono / elemento con mouse sobre** (el disparador).

## 3. Construcción (medidas) — Tooltip

| Elemento | Medida |
|---|---|
| Padding **horizontal** (ambos bordes) | 16 px |
| Padding **vertical** (ambos bordes) | 8 px |
| Altura **mínima** | 44 px |
| Altura **máxima** | 80 px (límite de **3 líneas** de texto) |
| Ancho ajustable al texto lineal, **máximo** | 256 px |
| Borde redondeado | 4 px |

## 4. Orientación (Tooltip)

La orientación del elemento sobre el que se despliega depende de su posición en la
pantalla. El **puntero** apunta al elemento. Cuatro posiciones:

- **Tooltip arriba**, **Tooltip abajo**, **Tooltip izquierda**, **Tooltip derecha**.

## 5. Ventana de notificación (popover) — variante relacionada

Un cuadro emergente **similar al tooltip**, pero aparece cuando el usuario hace
**clic** en un elemento. La diferencia es que el popover puede desplegar una **mayor
cantidad de información**.

### Anatomía
1. **Contenedor.** 2. **Puntero.** 3. **Texto.** 4. **Íconos / elemento clickeado.**

### Construcción (medidas)
| Elemento | Medida |
|---|---|
| Padding **horizontal** (ambos bordes) | 14 px |
| Padding **vertical** | 12 px |
| Altura **mínima** del popover | 52 px |
| Ancho ajustable al contenido, **máximo** | 256 px |
| Borde redondeado | 4 px |
| Texto | **máximo 3 líneas** |

### Orientación (12 posiciones)
Según la posición en pantalla y la dirección que se muestre, el puntero aparece en
distintas direcciones alrededor de este cuadro de texto: **Arriba_izquierda, Arriba,
Arriba_derecha, Derecha_arriba, Derecha, Derecha_abajo, Abajo_izquierda, Abajo,
Abajo_derecha, Izquierda_arriba, Izquierda_centro, Izquierda_abajo.**

## 6. Colores

| Rol | Nombre | Hex |
|---|---|---|
| Texto del tooltip | Blanco Puro | `#FFFFFF` |
| Fondo del **tooltip** | Azul SURA | **`#0033A0`** (impreso `#26328C`; render real `(0,51,160)`) |
| Fondo de la **ventana de notificación** (popover) | Pantone 432 C | **`#333F48`** (impreso `#3F3F41`; render real `(51,63,72)`) |

## 7. Modo oscuro

El tooltip / popover tiene variante en **modo oscuro**:

| Rol | Hex |
|---|---|
| Fondo de la superficie | Azul muy oscuro `#00003F` (muestreo `(0,0,63)`) |
| Acento (barras) | Amarillo de marca `#E2E828` (ver Pendiente) |
| Tooltip sobre fondo oscuro | tooltip **blanco** con texto **azul** |

- Mismo fondo `#00003F` que el modo oscuro de Modales.

## 8. Uso

- Se usa **principalmente** en la pantalla de **escritorio**.
- **No** lo utilices para información **crítica** de la tarea.
- Los usuarios **no** deberían necesitar exactamente este componente para completar
  una tarea específica. Si requieres que el usuario complete o digite información de
  campos (p. ej. una solicitud de formulario), usa el **formulario**, no el tooltip.
- Debe ofrecer contenido **breve y útil**.
- Las sugerencias con texto sobre o subrayado de la palabra para usuarios. Si no
  puedes, piensa en ningún contexto contenido **particularmente** útil; no lo
  utilices solo para enlaces.

## 9. Tokens CSS

```css
:root {
  /* Tooltip — construcción */
  --tooltip-pad-x: 16px;            /* ambos bordes horizontales */
  --tooltip-pad-y: 8px;             /* ambos bordes verticales */
  --tooltip-min-h: 44px;
  --tooltip-max-h: 80px;            /* 3 líneas */
  --tooltip-max-w: 256px;
  --tooltip-radius: 4px;

  /* Popover (ventana de notificación) — construcción */
  --popover-pad-x: 14px;
  --popover-pad-y: 12px;
  --popover-min-h: 52px;
  --popover-max-w: 256px;
  --popover-radius: 4px;            /* texto máx 3 líneas */

  /* Colores */
  --tooltip-text: #FFFFFF;          /* Blanco Puro */
  --tooltip-bg: #0033A0;            /* Azul SURA (impreso #26328C) */
  --popover-bg: #333F48;            /* Pantone 432 C (impreso #3F3F41) */

  /* Modo oscuro */
  --tooltip-dark-bg: #00003F;
  --tooltip-dark-accent: #E2E828;   /* amarillo de marca */

  --font-tooltip: 'Sura Sans', 'Helvetica Neue', Arial, sans-serif;
}
```

## 10. Reglas operativas para el skill

- **Tooltip** = contenedor + puntero + texto; aparece al **pasar el cursor** y
  desaparece al quitarlo. Padding 16 px horizontal / 8 px vertical; altura 44–80 px
  (máx 3 líneas); ancho máx 256 px; radio **4 px**. Fondo `#0033A0`, texto blanco.
- Orientación del tooltip: arriba/abajo/izquierda/derecha; el puntero apunta al
  elemento disparador.
- **Ventana de notificación (popover)** = variante que aparece al **clic** y admite
  más información: padding 14 px horizontal / 12 px vertical; altura mín 52 px; ancho
  máx 256 px; radio 4 px; texto máx 3 líneas; fondo `#333F48` (Pantone 432 C); 12
  posiciones de puntero.
- **No** usar tooltip para información crítica ni para requisitos de campo/formulario;
  contenido breve y útil; principalmente en escritorio.
- Modo oscuro: superficie `#00003F` con acento amarillo `#E2E828`; tooltip blanco con
  texto azul.
- El azul **manda por render** (`#0033A0`), no por el nombre impreso (`#26328C`).
- Tipografía Sura Sans; **nunca Barlow**.

## 11. Pendiente

- [ ] Confirmar el hex exacto del amarillo de acento en modo oscuro (probable
      `#E2E828`, mismo de Modales) — no muestreado en esta lámina.
- [ ] Confirmar el grosor del puntero/flecha y el tamaño del texto del tooltip en px
      (no impreso; cuerpo probable 14 px).
- [ ] Confirmar el color del texto del popover sobre `#333F48` (¿blanco?) y si el
      borde redondeado de 4 px aplica también al puntero.
