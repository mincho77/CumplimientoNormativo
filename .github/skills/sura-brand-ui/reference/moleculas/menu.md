# Menú (Menu / Dropdown) — molécula

Fuente: `Menú.pdf` (1 lámina). Verificado contra imágenes renderizadas y muestreo
de píxeles. **Tipografía: Sura Sans. No aparece Barlow.**

> ⚠ **Nota de color (aplica «confía en la muestra renderizada»):** la lámina
> imprime `#3F3F41` junto a "PANTONE 432 C", pero la **muestra renderizada real**
> es `#333F48` (confirmado por muestreo `(51,63,72)`, que coincide con el valor
> real de PANTONE 432 C). Usa **`#333F48`**; el `#3F3F41` impreso es un export
> poco fiable.

## 1. Qué es

El menú muestra una lista de opciones en una superficie temporal. Las opciones
aparecen cuando el usuario interactúa con un botón u otro control. Puede contener
íconos, botones o campos de texto.

## 2. Anatomía

1. **Menú dango** — el disparador (los 3 puntos / kebab que abre el menú).
2. **Contenedor** — la caja del menú desplegado.
3. **Elemento de la lista** — cada opción.
4. **Elemento activo** — la opción resaltada/seleccionada.
5. **Texto de etiqueta** del elemento de la lista.

## 3. Construcción (medidas)

### Menú dango (disparador)
| Elemento | Medida |
|---|---|
| Tamaño | 24 × 24 px |
| Espaciado de los puntos | 4 px |
| Color | `#333F48` (PANTONE 432 C; impreso `#3F3F41`) |

### Menú desplegado
| Elemento | Medida |
|---|---|
| Altura de cada elemento | 48 px |
| Tamaño de texto | 16 px (= 1 rem) |
| Tamaño del ícono | 24 × 24 px |
| Border-radius del contenedor | 12 px (`--radius-md`) |
| Ancho máximo | 188 px |
| Padding vertical interno del ítem | 8 px |
| Padding lateral externo (contenedor) | 4 px |
| **Margen con el contenedor** | 16 px |
| **Espaciado entre elementos** | 12 px |

- El margen interno **no lleva ícono al principio**: si no hay ícono, se ajusta y
  conserva la misma margen de 16 px.
- La margen interna depende del texto a colocar, **sin exceder** los 12 px entre
  elementos ni los 16 px con el contenedor.

## 4. Estados del elemento

| Estado | Apariencia |
|---|---|
| **Por defecto** | texto sobre fondo blanco |
| **Activo / seleccionado** | elemento resaltado (fondo suave azulado) |
| **Sobre (hover)** | resaltado al pasar el cursor |

## 5. Comportamiento / Uso

- En las etiquetas de la lista se recomienda **no más de tres palabras**; si se
  excede, activar puntos suspensivos (`…`). Cada etiqueta: **máximo 18 caracteres**.

### 5.1 Posicionamiento automático (flip) por espacio real

El menú se posiciona según el espacio **realmente disponible** frente al control
que lo genera — **no** por una regla de "mitad de pantalla".

- Por defecto abre **hacia abajo**.
- Antes de abrir, medir el rectángulo del disparador (`getBoundingClientRect()`)
  contra el alto de la ventana (`window.innerHeight`) y comparar:
  - espacio abajo = `vh − rect.bottom − margen`
  - espacio arriba = `rect.top − margen`
- Abrir **hacia arriba** solo si el menú **no cabe abajo** *y* arriba hay más
  espacio que abajo.
- **Recalcular en cada apertura** (no solo al cargar): el usuario pudo hacer
  scroll de la página entre aperturas.
- Al abrir hacia arriba, **invertir el origen de la animación**: el menú crece
  desde su borde inferior (`transform-origin: bottom`), no desde arriba. Sin esto
  la animación se siente al revés.

### 5.2 Scroll interno cuando la lista no cabe

- Si la altura del menú supera el espacio disponible, fijar `max-height`
  **dinámica** (= espacio disponible, con un piso mínimo p. ej. 120 px) y
  `overflow-y:auto`. Así el scroll vive **dentro de la lista**; el usuario nunca
  debe scrollear toda la pantalla para ver las opciones.
- **Ocultar los botones de flecha de la barra de desplazamiento nativa.** El
  navegador (WebKit) los dibuja con **fondo blanco cuadrado** en los extremos de
  la barra, y esos cuadrados **pisan las esquinas redondeadas** del contenedor.
  Usar `::-webkit-scrollbar-button{display:none}`.
- Dejar la barra **fina y redondeada**, con color de marca, y **separada de los
  bordes** (borde transparente + `background-clip:padding-box` + margen en el
  track) para que no toque las esquinas y el redondeo se vea limpio.

## 6. Tokens CSS

```css
:root {
  /* Disparador (dango) */
  --menu-trigger-size: 24px;
  --menu-trigger-dot-gap: 4px;
  --menu-trigger-color: #333F48;   /* PANTONE 432 C */

  /* Menú desplegado */
  --menu-item-h: 48px;
  --menu-text-size: 16px;          /* 1rem */
  --menu-icon-size: 24px;
  --menu-radius: 12px;
  --menu-max-w: 188px;
  --menu-item-pad-y: 8px;
  --menu-pad-x: 4px;
  --menu-margin-container: 16px;
  --menu-gap-items: 12px;

  --font-menu: 'Sura Sans', 'Helvetica Neue', Arial, sans-serif;
}
```

### Barra de desplazamiento interna (oculta los botones de flecha)

```css
/* Apertura hacia arriba: el menú crece desde su borde inferior */
.menu.dd-up .menu-panel{
  top:auto; bottom:calc(100% + 6px);
  transform-origin:bottom;        /* origen invertido */
}

/* Barra fina, sin botones de flecha y separada de los bordes */
.menu-panel{ scrollbar-width:thin; scrollbar-color:var(--field-stroke) transparent; }
.menu-panel::-webkit-scrollbar{ width:8px; height:8px; }
.menu-panel::-webkit-scrollbar-button{ display:none; width:0; height:0; } /* mata las flechitas con fondo blanco */
.menu-panel::-webkit-scrollbar-track{ background:transparent; margin:6px 0; }
.menu-panel::-webkit-scrollbar-thumb{
  background:var(--field-stroke); border-radius:8px;
  border:2px solid transparent; background-clip:padding-box;   /* separa el pulsador del borde */
}
.menu-panel::-webkit-scrollbar-thumb:hover{ background:var(--menu-trigger-color); background-clip:padding-box; }
```

## 7. Reglas operativas para el skill

- Disparador = 3 puntos 24×24 px, color `#333F48`.
- Contenedor: `border-radius: 12px`, `max-width: 188px`, margen interno 16 px,
  gap entre ítems 12 px, ítems de 48 px de alto.
- Texto Sura Sans 16 px; nunca Barlow.
- Truncar etiquetas largas con `…`; máx 3 palabras / 18 caracteres.
- Sin ícono al inicio → mantener la margen de 16 px (no comprimir).
- Elevación del contenedor: usar el `dp` de dropdown de `elevaciones.md`
  (`--elevation-dp4`), salvo que se indique otra.
- **Posicionamiento (flip):** abrir hacia abajo por defecto; hacia arriba solo si
  no cabe abajo y arriba hay más espacio. Medir con `getBoundingClientRect()` vs
  `window.innerHeight`, **recalcular en cada apertura**, e **invertir el origen de
  la animación** al abrir hacia arriba. No usar la regla de "mitad de pantalla".
- **Scroll interno:** cuando la lista excede el espacio, `max-height` dinámica +
  `overflow-y:auto` dentro del menú (nunca obligar a scrollear la pantalla).
- **Barra de desplazamiento:** ocultar siempre los botones de flecha nativos con
  `::-webkit-scrollbar-button{display:none}` — su fondo blanco cuadrado rompe el
  redondeo. Barra fina (8 px), pulsador redondeado en color de marca y separado de
  los bordes (`background-clip:padding-box` + margen en el track).

## 8. Pendiente

- [ ] Confirmar el hex exacto del fondo del elemento activo/hover (no impreso;
      muestrear si se requiere fidelidad alta).
- [ ] Confirmar color del texto de etiqueta por defecto (probable `--gray-900`).
