# Carrusel (Carousel) — molécula

Fuente: `Carrusel.pdf` (varias láminas). Verificado contra imágenes renderizadas y
muestreo de píxeles. **Tipografía: Sura Sans. No aparece Barlow.**

## 1. Qué es

Los carruseles permiten agrupar varios elementos en un espacio reducido con la ayuda
de un **scroll horizontal**. El usuario entra a uno y los contenidos se distribuyen
en su interior de forma horizontal. Se recomienda no usar más de **5** páginas dentro
de un carrusel. Los contenidos pueden referenciar el componente **Tarjetas**.

## 2. Anatomía

Tarjeta base modular:
1. **Imagen.**
2. **Encabezado.**
3. **Bajada / contenido** (texto, subtítulo).
4. **Llamada a la acción** (botones).
5. **Dots** de navegación.
6. **Flechas** de navegación.

## 3. Construcción (medidas)

### Tarjeta con llamada a la acción
| Elemento | Medida |
|---|---|
| Padding **horizontal** | 16 px |
| Padding **vertical** (extremos y entre botones) | 16 px |
| Espaciado **entre tarjetas** (slides) | 32 px |
| Ancho **mínimo** de la tarjeta | 358 px (estilo heading **h3**) |
| Título | 24 px Regular |
| Bajada de texto | 14 px Regular |
| Borde redondeado | 12 px |
| Botones de acción | tamaño **mediano** |

### Carrusel de imágenes de ancho completo
| Elemento | Medida |
|---|---|
| Padding horizontal **mínimo** | 16 px |
| Padding vertical (dots → borde inferior de la imagen) | 32 px |
| Ancho / alto | dependen del **formato** |
| Borde redondeado | 12 px |

## 4. Flechas de navegación

| Elemento | Escritorio / Móvil |
|---|---|
| Tamaño del ícono (chevron) | 24 px |
| Diámetro del círculo | 40 px |
| Espaciado | 16 px |

Estados: **Activo** (relleno azul `#2D6DF6`, chevron blanco), **Inactivo** (gris
atenuado), **Sobre (hover)**, **Enfocado (focus)**. Chevron derecha / izquierda.

## 5. Dots de navegación

| Elemento | Medida |
|---|---|
| Dot activo (pill alargado) | 20 px de ancho |
| Dot inactivo / separación | 10 px |

- **Dot activo:** `#2D6DF6` (muestreo `(45,109,246)`); inactivos en gris/azul claro.
- Variantes de color del estado activo (azul / amarillo / verde) según el fondo del
  carrusel (combinación **Flechas con dots**).

## 6. Uso (variantes)

| Variante | Comportamiento |
|---|---|
| **Tarjeta ajustada al inicio** | Fuerza a los elementos contenidos a aparecer al **inicio** (izquierda). |
| **Carrusel centrado** | Fuerza a los elementos a aparecer **centrados**. |
| **Carrusel versión mobile** | Solo tiene **flechas** (omite los dots) cuando son demasiadas páginas. |
| **Carrusel de imágenes de ancho completo** | Imágenes sin tarjeta; dots sobre la imagen. |
| **Tarjeta con llamado a la acción** | Tarjeta con imagen + texto + botones (la base). |

## 7. Tokens CSS

```css
:root {
  /* Tarjeta CTA */
  --carousel-card-pad-x: 16px;
  --carousel-card-pad-y: 16px;
  --carousel-slide-gap: 32px;       /* entre tarjetas */
  --carousel-card-min-w: 358px;
  --carousel-title-size: 24px;      /* h3 */
  --carousel-caption-size: 14px;
  --carousel-radius: 12px;

  /* Imagen ancho completo */
  --carousel-img-pad-x: 16px;
  --carousel-img-pad-y: 32px;       /* dots ↔ borde inferior */

  /* Flechas */
  --carousel-arrow-circle: 40px;
  --carousel-arrow-icon: 24px;
  --carousel-arrow-gap: 16px;

  /* Dots */
  --carousel-dot-active-w: 20px;    /* pill */
  --carousel-dot-gap: 10px;

  /* Color */
  --carousel-active: #2D6DF6;       /* dot/flecha activos */

  --font-carousel: 'Sura Sans', 'Helvetica Neue', Arial, sans-serif;
}
```

## 8. Reglas operativas para el skill

- Carrusel con scroll horizontal; **máximo 5 páginas**; contenidos basados en
  Tarjetas (`tarjetas.md`).
- Tarjeta CTA: padding 16/16, gap entre slides 32 px, ancho mín 358 px, título
  24 px (h3), bajada 14 px, radio 12 px, botones medianos.
- Imágenes de ancho completo: padding 16 px lados / 32 px dots↔borde inferior,
  radio 12 px, dimensiones según formato.
- Flechas: círculo 40 px, ícono 24 px, gap 16 px; activo relleno `#2D6DF6` con
  chevron blanco, inactivo gris.
- Dots: activo pill 20 px `#2D6DF6`, inactivos 10 px en gris/azul claro.
- Variantes: ajustada al inicio, centrado, mobile (solo flechas), ancho completo,
  con CTA.
- Tipografía Sura Sans; **nunca Barlow**.

## 9. Pendiente

- [ ] Confirmar los hex de las variantes amarilla/verde del dot activo (sobre
      fondos de color) — no muestreados.
- [ ] Confirmar el gris exacto de flechas/dots inactivos y el alto del círculo de
      flecha en escritorio vs. móvil (parecen iguales: 40 px).
- [ ] Confirmar el ancho del dot inactivo (¿8/10 px?) y el alto de la pill activa.
