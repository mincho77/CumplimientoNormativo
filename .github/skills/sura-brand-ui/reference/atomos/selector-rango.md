# Selector de rango / Deslizador (Slider) — átomo

Fuente: `Selector de rango.pdf` (1 lámina). Verificado contra imágenes
renderizadas y muestreo de píxeles. **Tipografía: Sura Sans. No aparece Barlow.**

> ⚠ **Nota de nombres (aplica «el hex manda»):** esta lámina rotula `#2D6DF6`
> como "Azul Vivo" y `#0033A0` como "Azul SURA". El nombre **canónico**
> (`generales/colores.md`) es `#2D6DF6` = **Azul Cielo Latino** y `#0033A0` =
> **Azul Profundo**. Los hex son los correctos; ignora la discrepancia de
> nombres del PDF.

## 1. Qué es

Control de formulario para seleccionar un valor dentro de un rango
preestablecido. Permite seleccionar **un solo valor** (fluido) o **un rango de
valores** (dos manipuladores). El usuario arrastra el manipulador a lo largo de
la pista.

## 2. Anatomía

1. **Elipse / manipulador** arrastrable (el círculo que se desliza).
2. **Indicador de rango** — barra azul de relleno (tramo seleccionado).
3. **Pista** — riel completo de fondo.
4. **Valor mínimo** (etiqueta extremo izquierdo).
5. **Valor máximo** (etiqueta extremo derecho).

## 3. Construcción (medidas)

| Elemento | Medida |
|---|---|
| **Altura total** del componente | 48 px |
| **Altura de la pista** (riel) | 4 px — *se anima para indicar el valor al arrastrar* |
| **Manipulador** (elipse) | 12 × 12 px |
| **Ancho mínimo** | 360 px |

## 4. Colores

| Parte | Color | Hex |
|---|---|---|
| **Pista** (fondo del riel) | Background 5 | `#F8F8F8` |
| **Indicador** (barra de relleno) | Azul Cielo Latino *(lámina: "Azul Vivo")* | `#2D6DF6` |
| **Etiquetas mín. y máx.** | Gris 500 | `#3F3F41` |
| **Etiqueta de valor activo** | Azul Profundo *(lámina: "Azul SURA")* | `#0033A0` |

## 5. Manipulador (handle) — por estado

| Estado | Borde | Relleno |
|---|---|---|
| **Default** | 2 px solid Azul Cielo Latino `#2D6DF6` | Blanco Puro `#FFFFFF` |
| **Presionado / en arrastre** | 2 px solid `#81B1FF` *(lámina: "Pantone 284 C")* | Azul Cielo Latino `#2D6DF6` |

### Indicador numérico del manipulador (tooltip de valor)

- Texto: **Sura Sans Semibold, 12 px**.
- Color: Azul Profundo `#0033A0`.

### Sombra del manipulador (elevación)

| Propiedad | Valor |
|---|---|
| X | 0 |
| Y | 3 |
| Blur | 8 |
| Spread | 0 |
| Color | `#006EFF` al 20 % |

## 6. Variantes / estados (de la lámina "Estados")

| Variante | Descripción |
|---|---|
| **Vacío** | Un manipulador en el mínimo, sin relleno. `$0 … $1000` |
| **Fluido** | Un manipulador; el indicador rellena de mín. hasta el valor (ej. `$500`) |
| **Rango** | **Dos** manipuladores; el indicador rellena el tramo entre ambos (ej. `$200–$600`) |
| **Segmentado** | Pista con marcas de paso (ticks); el valor salta en escalones |

## 7. Uso

- **No** lo uses para un **rango muy pequeño** (ej. 1–3): se mueve a saltos
  cuando el rango de valores es bajo.
- **No** lo uses si es importante seleccionar un **valor exacto** — el cursor no
  es preciso; usa un input o un select.
- Los deslizadores suelen ser **horizontales**, pero pueden ser **verticales**
  cuando sea necesario.

**Correcto:** ancho amplio con etiquetas legibles (`$0  $500  $1000`).
**Incorrecto:** comprimido en un campo angosto o con un rango diminuto (`$0…$3`).

## 8. Tokens para implementación

```css
:root {
  /* Tamaños */
  --slider-height-total: 48px;       /* alto del componente */
  --slider-track-height: 4px;        /* riel */
  --slider-handle-size: 12px;        /* elipse manipulador */
  --slider-min-width: 360px;

  /* Colores */
  --slider-track-bg: #F8F8F8;        /* Background 5 */
  --slider-indicator: #2D6DF6;       /* Azul Cielo Latino (relleno) */
  --slider-label: #3F3F41;           /* Gris 500 (mín/máx) */
  --slider-value-label: #0033A0;     /* Azul Profundo (valor activo) */

  /* Manipulador */
  --slider-handle-border: #2D6DF6;   /* 2px solid, default */
  --slider-handle-fill: #FFFFFF;     /* Blanco Puro, default */
  --slider-handle-border-drag: #81B1FF;  /* en arrastre */
  --slider-handle-fill-drag: #2D6DF6;    /* en arrastre */
  --slider-handle-border-width: 2px;

  /* Sombra del manipulador */
  --slider-handle-shadow: 0px 3px 8px 0px rgba(0,110,255,0.20); /* #006EFF 20% */

  /* Tipografía del valor */
  --slider-value-font-size: 12px;    /* Sura Sans Semibold */
  --slider-value-font-weight: 600;
}
```

## 9. Reglas operativas para el skill

1. Manipulador = círculo de **12 px**, borde **2 px** `#2D6DF6`, relleno blanco.
   En arrastre invierte: relleno `#2D6DF6`, borde `#81B1FF`.
2. La pista mide **4 px** de alto; el tramo seleccionado se pinta `#2D6DF6`.
3. Etiquetas mín./máx. en Gris 500 `#3F3F41`; el valor activo del manipulador en
   Azul Profundo `#0033A0`, Sura Sans Semibold 12 px.
4. Respeta el **ancho mínimo de 360 px** — no comprimas el slider en campos
   angostos (es el uso incorrecto de la lámina).
5. Usa **Fluido** para un valor único y **Rango** (dos manipuladores) para
   intervalos. **Segmentado** cuando los valores sean discretos.
6. Aplica la sombra `0 3 8 0` `#006EFF` al 20 % en el manipulador para darle
   elevación.
7. No uses slider cuando se requiera precisión exacta o el rango sea ≤ 3 pasos.

## 10. Pendiente

- [ ] Confirmar si el **ancho mínimo de 360 px** es solo para la pista o incluye
      las etiquetas mín./máx.
- [ ] Documentar el **paso (step)** por defecto del modo Segmentado y cuántas
      marcas dibuja según el rango.
- [ ] Confirmar tipografía/posición exacta del tooltip de valor en la variante
      **Rango** (¿uno por manipulador?).
