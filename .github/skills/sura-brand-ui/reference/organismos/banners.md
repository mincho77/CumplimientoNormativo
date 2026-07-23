# Tablero destacado (Banner) — organismo

Fuente: `Banners.pdf` (3 páginas). Verificado contra imágenes renderizadas y muestreo
de píxeles. **Tipografía: Sura Sans. No aparece Barlow.**

## 1. Qué es

El banner se utiliza para indicar mensajes **breves e importantes** para ciertas
funciones o servicios; algunos pueden proporcionar **CTAs** relacionados. Es una
manera de presentar una experiencia y proporcionar al usuario un **claro llamado a la
acción**. Solo si es necesario incluir **más de un banner** se deben activar las
**flechas** y los **dots** (siguiendo lo planteado en el componente **Carrusel**).

## 2. Anatomía

1. **Titular.**
2. **Subtítulo.**
3. **Call to action** (CTA).
4. **Dots.**
5. **Manejadores** (flechas de navegación).
6. **Imagen** (ilustración o fotografía).
7. **Contenedor.**

## 3. Construcción por dispositivo

### Banner principal (escritorio)
- Rejilla con **márgenes de 120 px** y **gutters de 24 px** entre columnas.
- Dots con flechas debajo del contenido cuando hay varios banners.

### Banner Tablet
- **Ancho 768 px**, **alto 374 px**.
- Márgenes **64 px**, gutters **12 px**.
- Dots: ancho de la fila **176 px**, separación **28 px**.

### Banner mobile
- **Ancho 360 px**; alto/ancho **se adaptan** al dispositivo.
- Espaciado interno **8 px** y **24 px** entre elementos.
- Dots: ancho de la fila **176 px**, separación **10 px**.

## 4. Variantes y recomendaciones de uso

| Variante | Botón | Título | Subtítulo / cuerpo | Espaciado |
|---|---|---|---|---|
| **Banner principal** (escritorio) | Primario **Grande** | **62 px bold** (h1) | ≤ 2 líneas, **26 px** | múltiplo de 8 |
| **Super banner / Interna** | (título de página + migas de pan) | **48 px bold** (h2) | — | **16 px** |
| **Banner anuncio** | Primario **Mediano** | **32 px bold** (h3) | cuerpo **16 px** regular (body 2) | **24 px** |
| **Banner flotante** | Primario **Grande** | **48 px bold** (h2) | cuerpo **22 px** | múltiplo de 8 |
| **Banner mobile** | Primario **Pequeño** | **36 px bold** (h2-mobile) | subtítulo **18 px bold** (h6) | múltiplo de 8 |

- **Super banner / Interna:** usa el **título de la página actual** + **migas de pan**;
  deben generar contraste con el fondo según **WCAG**.
- El botón se elige según el contexto: el tamaño del botón crece con la jerarquía del
  banner (Grande en principal/flotante, Mediano en anuncio, Pequeño en mobile).

## 5. Colores

| Rol | Nombre | Hex |
|---|---|---|
| Fondo del banner | Azul Vivo SURA | `#2D6DF6` (muestreo `(45,105,245)`) |
| Acento / blob / CTA | Amarillo de marca | `#E1E628` (muestreo `(225,230,40)`; marca `#E2E828`) |
| Titular sobre azul | Amarillo o **Blanco Puro** | `#E1E628` / `#FFFFFF` |
| Subtítulo sobre azul | Blanco Puro | `#FFFFFF` |
| Fondo de tinte alterno | Verde menta | `#E6F9EF` (muestreo `(230,249,239)`) |

- El **CTA** se ve como botón **amarillo** con texto azul oscuro; según contexto puede
  ser un botón primario azul. La imagen suele ir sobre un **blob amarillo**.

## 6. Uso

- Presenta mensajes breves e importantes con un claro llamado a la acción.
- **Un solo banner por pantalla** (correcto). Apilar dos banners en la misma vista es
  **incorrecto**.
- Cuando hay varios banners, **activar flechas + dots** (comportamiento de Carrusel).
- Mantener **contraste** suficiente del titular/migas sobre el fondo (WCAG).

## 7. Tokens CSS

```css
:root {
  /* Rejilla por dispositivo */
  --banner-desktop-margin: 120px;
  --banner-desktop-gutter: 24px;
  --banner-tablet-w: 768px;
  --banner-tablet-h: 374px;
  --banner-tablet-margin: 64px;
  --banner-tablet-gutter: 12px;
  --banner-mobile-w: 360px;
  --banner-mobile-pad: 8px;         /* + 24px entre elementos */

  /* Tipografía por variante (bold) */
  --banner-title-principal: 62px;   /* h1 */
  --banner-sub-principal: 26px;
  --banner-title-interna: 48px;     /* h2 */
  --banner-title-anuncio: 32px;     /* h3 */
  --banner-body-anuncio: 16px;      /* body 2 */
  --banner-title-flotante: 48px;    /* h2 */
  --banner-body-flotante: 22px;
  --banner-title-mobile: 36px;      /* h2-mobile */
  --banner-sub-mobile: 18px;        /* h6 */

  /* Colores */
  --banner-bg: #2D6DF6;             /* Azul Vivo SURA */
  --banner-accent: #E1E628;         /* amarillo (marca #E2E828) */
  --banner-text: #FFFFFF;
  --banner-tint-mint: #E6F9EF;

  --font-banner: 'Sura Sans', 'Helvetica Neue', Arial, sans-serif;
}
```

## 8. Reglas operativas para el skill

- Banner = contenedor con titular + subtítulo + CTA + imagen (ilustración/foto sobre
  blob amarillo); fondo **azul vivo `#2D6DF6`**, acento **amarillo `#E1E628`**.
- **Cinco variantes** con jerarquía de botón y tipografía propia (ver tabla §4):
  principal (Grande, 62/26), interna (48 + migas de pan), anuncio (Mediano, 32/16),
  flotante (Grande, 48/22), mobile (Pequeño, 36/18).
- Rejilla: escritorio márgenes 120/gutter 24; tablet 768×374 márgenes 64/gutter 12;
  mobile 360, padding 8/24.
- **Un banner por pantalla**; varios → activar flechas + dots (Carrusel).
- Espaciado regla de **múltiplo de 8**; contraste WCAG del titular/migas.
- Tipografía Sura Sans; **nunca Barlow**.

## 9. Pendiente

- [ ] Confirmar el alto exacto del banner principal en escritorio (solo se imprimió
      tablet 374 px) y el alto del banner mobile.
- [ ] Confirmar el ancho/alto del dot activo (pill) y del inactivo en banner (parecen
      heredar de Carrusel: activo 20 px, inactivo 10 px).
- [ ] Confirmar si existe variante de **modo oscuro** del banner (no apareció lámina
      dedicada; las últimas láminas son ejemplos de uso correcto/incorrecto).
