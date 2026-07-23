# Paginador (Pagination) — molécula

Fuente: `Paginador.pdf` (1 lámina). Verificado contra imágenes renderizadas y
muestreo de píxeles. **Tipografía: Sura Sans. No aparece Barlow.**

## 1. Qué es

El paginador permite dividir el contenido de una página web en varias secciones
o páginas, dando al usuario la oportunidad de avanzar entre ellas mediante una
serie de enlaces o botones. Útil para contenido de una página muy extensa.

## 2. Anatomía

1. **Contenedor.**
2. **Controles de cambio de página** — chevrons anterior `<` / siguiente `>`.
3. **Página activa** — la página actual seleccionada.
4. **Páginas siguientes** — el resto de números (con elipsis `…` cuando son muchas).
5. **Selector desplegable** de filas por página ("Mostrar [10 ▾]").

## 3. Construcción (medidas)

### Versión escritorio
| Elemento | Medida |
|---|---|
| Ancho máximo | 1400 px |
| Ancho mínimo | 636 px |
| Altura del componente | 56 px |
| Padding vertical (contenedor) | 10 px |
| Espaciado entre elementos | 8 px |
| Margen externo (lados) | 24 px |
| Filas por página | múltiplos de **10 / 20 / 30** |

### Versión responsive — tablet
| Elemento | Medida |
|---|---|
| Ancho mínimo | 636 px |
| Padding vertical | 10 px |
| Disposición | elementos **justificados al centro** |

### Versión responsive — móvil
| Elemento | Medida |
|---|---|
| Botones prev/next | 40 × 40 px |
| Espaciado de botones | 8 px |
| Padding vertical | 6 px |
| Ancho mínimo | 227 px |
| Contenido | solo "Página X de Y" + botones prev/next + selector de filas |

> En móvil **no se listan los números**: solo se marca la página actual
> ("Página 1 de 10") y se navega con los botones anterior/siguiente.

## 4. Página activa

- Círculo relleno **`#0033A0`** (Azul Profundo, confirmado por muestreo
  `(0,51,160)`) con número en **blanco**.
- Las demás páginas se muestran como texto plano (sin relleno).

## 5. Uso

- El paginador debe ir **dentro de un contenedor** y **justificado a la derecha**.
- Se ubica en la **parte inferior** del contenido (tabla de datos o página de
  información archivada).

## 6. Tokens CSS

```css
:root {
  /* Escritorio */
  --pager-max-w: 1400px;
  --pager-min-w: 636px;
  --pager-h: 56px;
  --pager-pad-y: 10px;
  --pager-gap: 8px;
  --pager-margin-x: 24px;

  /* Móvil */
  --pager-btn-size: 40px;
  --pager-btn-gap: 8px;
  --pager-mobile-pad-y: 6px;
  --pager-mobile-min-w: 227px;

  /* Página activa */
  --pager-active-bg: #0033A0;
  --pager-active-text: #FFFFFF;

  --font-pager: 'Sura Sans', 'Helvetica Neue', Arial, sans-serif;
}
```

## 7. Reglas operativas para el skill

- Página activa = círculo relleno `#0033A0` con texto blanco; resto en texto plano.
- Escritorio: ancho 636–1400 px, alto 56 px, gap 8 px, márgenes 24 px,
  justificado a la derecha dentro de un contenedor, en la parte inferior.
- Tablet: mismos elementos centrados, mín 636 px.
- Móvil: colapsar a "Página X de Y" + prev/next 40×40 px; mín 227 px.
- Selector "Mostrar" siempre con opciones 10/20/30.
- Texto Sura Sans; nunca Barlow.

## 8. Pendiente

- [ ] Confirmar color de los números no activos y de los chevrons (probable
      `--gray-900` / `--color-secondary`; no impreso, muestrear si se requiere).
- [ ] Confirmar radio/elevación del selector desplegable "Mostrar"
      (usar `borde-redondeado.md` / `elevaciones.md` por defecto).
