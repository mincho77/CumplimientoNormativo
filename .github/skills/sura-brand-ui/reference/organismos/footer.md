# Footer (Pie de página) — organismo

Fuente: `Footer.pdf` (1 página larga). Verificado contra imágenes renderizadas y
muestreo de píxeles. **Tipografía: Sura Sans. No aparece Barlow.**

## 1. Qué es

El footer (también conocido como **pie de página**) es la sección que se encuentra al
**final** de una página web. Por lo general, contiene **información adicional** que
complementa el contenido principal de la página.

## 2. Anatomía

1. **Línea superior** (separador horizontal sobre el footer).
2. **Contenido** (columnas de enlaces).
3. **Logo SURA.**
4. **Grupo SURA afiliados** (barra azul de enlaces a las filiales).
5. **Iconos de redes sociales.**
6. **Números de contacto** (líneas de atención).
7. **Selector de columnas** (encabezados de cada columna; colapsables en tablet/móvil).

En escritorio el contenido se organiza en **4 columnas**: *Sobre Nosotros*,
*Encuéntranos*, *Servicios al usuario*, *Líneas de atención*.

## 3. Construcción por dispositivo

### Escritorio
| Elemento | Medida |
|---|---|
| Ancho de pantalla | **1440 px** |
| Altura **máxima** | **718 px** |
| Padding | **120 px** |
| Espaciado **entre columnas** | **24 px** |
| Ancho **máximo** del texto de contenido | **282 px** (no debe superponerse al espaciado entre columnas) |

### Tablet
| Elemento | Medida |
|---|---|
| Ancho | **768 px** |
| Altura | **450 px** |
| Padding | **4 px** |
| Espaciado **entre secciones** | **16 px** |

- Las columnas se **colapsan en acordeones** ("Encabezado" desplegable).

### Mobile
| Elemento | Medida |
|---|---|
| Ancho (pantalla completa) | **416 px** |
| Padding | **12 px** |
| Padding **vertical** | **16 px** |
| Espaciado **entre secciones** | **8 px** |

- Acordeones apilados; barra de afiliados con enlaces **en vertical**.

### Estado Abierto
El **largo** de las secciones de contenido en tablet y móvil **depende de la cantidad
de texto** que se coloque (los acordeones se expanden según se requiera).

## 4. Colores

| Rol | Hex |
|---|---|
| Enlaces, encabezados y números de contacto | Azul Vivo SURA `#2D6DF6` (muestreo `(45,109,246)`) |
| Barra **Grupo SURA afiliados** (fondo) | `#2D6DF6`; texto **blanco** `#FFFFFF` |
| Logo SURA | Azul SURA |
| Fondo del footer | Blanco `#FFFFFF` |
| Línea superior / copyright | gris claro (ver Pendiente) |

- `© Copyright SURA 2022` en gris, alineado a la izquierda bajo la barra de afiliados;
  iconos de redes sociales a la derecha.

## 5. Uso

- Ubicar **al final** de la página con información complementaria (no crítica).
- Mantener el **ancho de texto ≤282 px** por columna en escritorio para no invadir el
  espaciado entre columnas.
- En tablet/móvil, **colapsar** las columnas en acordeones; expandir según contenido.

## 6. Tokens CSS

```css
:root {
  /* Escritorio */
  --footer-w: 1440px;
  --footer-max-h: 718px;
  --footer-pad: 120px;
  --footer-col-gap: 24px;
  --footer-text-max-w: 282px;

  /* Tablet */
  --footer-tablet-w: 768px;
  --footer-tablet-h: 450px;
  --footer-tablet-pad: 4px;
  --footer-tablet-section-gap: 16px;

  /* Mobile */
  --footer-mobile-w: 416px;
  --footer-mobile-pad: 12px;
  --footer-mobile-pad-y: 16px;
  --footer-mobile-section-gap: 8px;

  /* Colores */
  --footer-link: #2D6DF6;           /* enlaces / encabezados / números */
  --footer-affiliate-bg: #2D6DF6;   /* barra Grupo SURA afiliados */
  --footer-affiliate-text: #FFFFFF;
  --footer-bg: #FFFFFF;

  --font-footer: 'Sura Sans', 'Helvetica Neue', Arial, sans-serif;
}
```

## 7. Reglas operativas para el skill

- Footer = línea superior + 4 columnas de enlaces + logo SURA + barra azul de
  afiliados + iconos sociales + números de contacto + copyright.
- Enlaces, encabezados y números en **azul vivo `#2D6DF6`**; barra de afiliados
  `#2D6DF6` con texto **blanco**; fondo blanco.
- Escritorio: 1440 px, padding 120, gutter 24, texto ≤282 px, alto máx 718.
  Tablet: 768×450, padding 4, secciones 16; **acordeones**. Mobile: 416 px, padding
  12 / vertical 16, secciones 8; acordeones apilados + afiliados en vertical.
- Estado Abierto: largo de secciones según contenido.
- Tipografía Sura Sans; **nunca Barlow**.

## 8. Pendiente

- [ ] Confirmar el gris exacto del copyright, de los iconos sociales y de la línea
      superior (no impreso en hex).
- [ ] Confirmar si los **encabezados/números** usan un azul más profundo (`#0033A0`)
      o el mismo `#2D6DF6` (el muestreo de los textos pequeños tiende a `#2D6DF6`).
- [ ] Confirmar el tamaño de fuente de enlaces, encabezados y números (px no impreso).
