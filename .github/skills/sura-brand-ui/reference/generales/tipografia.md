# Tipografía — Sistema de Diseño SURA

Fuente: Manual de marca, sección "Tipografía".

**Familia tipográfica:** `Sura` (corporativa).
**Estilos web autorizados:** Regular, Seminegrita, Negrita.
**Estilos NO permitidos en web:** Fina, Ligera — no pasan contraste WCAG.

---

## 1. Tipografía Desktop (≥ 768 px)

| Escala | Estilo | Tamaño | Altura de línea | Uso |
|---|---|---|---|---|
| `h1` | Sura Negrita | 62 px / 3.875 rem | 62 px | Encabezado principal en desktop |
| `h2` | Sura Negrita | 48 px / 3 rem | 48 px | Encabezado principal en desktop |
| `h3` | Sura Negrita | 32 px / 2 rem | 32 px | Encabezado principal en Tablet/Desktop |
| `h4` | Sura Negrita | 26 px / 2.25 rem | 26 px | Encabezado principal en Tablet/Desktop |
| `h5` | Sura Seminegrita | 22 px / 1.375 rem | 22 px | Subtítulos grandes |
| `h6` | Sura Seminegrita | 18 px / 1.125 rem | 18 px | Subtítulos |
| Body Banner L | Sura Regular | 32 px / 2 rem | 38 px | Bloques de texto en banners |
| Body Banner M | Sura Regular | 24 px / 1.5 rem | 38 px | Bloques de texto en banners |
| Body | Sura Seminegrita | 16 px / 1 rem | Auto | Párrafos con palabras en negrita |
| Body | Sura Regular | 16 px / 1 rem | Auto | Párrafos en regular |
| Caption | Sura Negrita | 14 px / 0.875 rem | Auto | Pie de foto, comentarios RRSS, notas legales (negrita) |
| Caption | Sura Regular | 14 px / 0.875 rem | Auto | Pie de foto, comentarios RRSS, notas legales (regular) |

---

## 2. Tipografía Mobile (< 768 px)

| Escala | Estilo | Tamaño | Altura de línea | Uso |
|---|---|---|---|---|
| `h1` | Sura Negrita | 42 px / 3 rem | 42 px | Encabezado principal en mobile |
| `h2` | Sura Negrita | 36 px / 2.25 rem | 36 px | Encabezado principal en mobile |
| `h3` | Sura Negrita | 28 px / 1.75 rem | 28 px | Subtítulos grandes |
| `h4` | Sura Negrita | 24 px / 1.714 rem | 26 px | Subtítulos grandes |
| `h5` | Sura Negrita | 20 px / 1.429 rem | 22 px | Subtítulos |
| Body | Sura Negrita | 16 px / 1 rem | Auto | Párrafos con palabras en negrita |
| Body | Sura Regular | 16 px / 1 rem | Auto | Párrafos en regular |
| Caption | Sura Seminegrita | 14 px / 0.875 rem | Auto | Pie de foto, comentarios RRSS, notas legales (negrita) |
| Caption | Sura Regular | 14 px / 0.875 rem | Auto | Pie de foto, comentarios RRSS, notas legales (regular) |
| Small | Sura Regular | 12 px / 0.75 rem | Auto | **Solo aplicaciones nativas iOS y Android** |

---

## 3. Notas críticas

- Los **interlineados** para headings equivalen al valor en pixeles de la letra
  (h1 62px → line-height 62px). Esto compensa el espaciado por defecto amplio
  de la fuente en tamaños grandes.
- Para **bodys y captions** el interlineado es automático (`line-height: normal`).
- **Web solo permite** estilos Regular, Seminegrita y Negrita. **Fina y Ligera
  no pasan contraste** y están prohibidas.
- El estilo **Small (12 px)** se usa **únicamente** en pie de fotos y notas
  legales, y solo en apps nativas iOS/Android — no en web.
- ⚠ **La columna `rem` del PDF no es confiable** (conversiones mal calculadas:
  p. ej. h4 dice "26 px / 2.25 rem" cuando 2.25 rem = 36 px; h4 mobile "24 px /
  1.714 rem" cuando 24 px = 1.5 rem). **Manda el valor en px**; los tokens de §5
  usan px exactos. Para convertir, base 16 px = 1 rem.

---

## 4. Reglas operativas para el skill

1. Para **viewports ≥ 768 px** (desktop, tablet) usa la escala de la sección 1.
2. Para **viewports < 768 px** (mobile) usa la escala de la sección 2.
3. Nunca uses tamaños intermedios fuera de la escala. Si necesitas un tamaño
   no contemplado, usa el inmediatamente inferior, no inventes.
4. Para títulos principales (`h1`/`h2`) usa **Sura Negrita**.
5. Para subtítulos (`h5`/`h6` desktop) usa **Sura Seminegrita**.
6. Para cuerpo de texto usa **16 px Regular**, con Seminegrita para énfasis
   inline.
7. Nunca uses estilos Fina o Ligera en web.
8. La familia **sí está disponible** en el skill como asset (ver §6). Antes de
   renderizar con cairosvg, instala la fuente en la ruta de fontconfig y úsala
   con `font-family="Sura Sans"`. Mantén siempre el fallback declarado por si
   el entorno no la resuelve: `font-family: 'Sura Sans', 'Helvetica Neue', Arial, sans-serif`.

---

## 5. CSS / SVG tokens

```css
:root {
  /* Familia tipográfica — family name real del asset: "Sura Sans" */
  --font-family: 'Sura Sans', 'Helvetica Neue', Arial, sans-serif;

  /* Pesos */
  --font-regular: 400;
  --font-seminegrita: 600;
  --font-negrita: 700;

  /* Escala desktop */
  --font-h1: 62px;        --lh-h1: 62px;
  --font-h2: 48px;        --lh-h2: 48px;
  --font-h3: 32px;        --lh-h3: 32px;
  --font-h4: 26px;        --lh-h4: 26px;
  --font-h5: 22px;        --lh-h5: 22px;
  --font-h6: 18px;        --lh-h6: 18px;
  --font-body-banner-l: 32px;  --lh-body-banner-l: 38px;
  --font-body-banner-m: 24px;  --lh-body-banner-m: 38px;
  --font-body: 16px;      --lh-body: 1.5;
  --font-caption: 14px;   --lh-caption: 1.4;

  /* Escala mobile (< 768px) */
  --font-h1-mobile: 42px;
  --font-h2-mobile: 36px;
  --font-h3-mobile: 28px;
  --font-h4-mobile: 24px;
  --font-h5-mobile: 20px;
}

@media (max-width: 767px) {
  :root {
    --font-h1: var(--font-h1-mobile);
    --font-h2: var(--font-h2-mobile);
    --font-h3: var(--font-h3-mobile);
    --font-h4: var(--font-h4-mobile);
    --font-h5: var(--font-h5-mobile);
  }
}
```

En SVG, los pesos se aplican con `font-weight`:
- Regular → `font-weight="400"`
- Seminegrita → `font-weight="600"`
- Negrita → `font-weight="700"`

---

## 6. Asset de fuente disponible

Ubicación: `assets/fonts/` — la fuente corporativa **Sura Sans** en 3 formatos.

| Archivo | Formato | Uso |
|---|---|---|
| `SuraSans-Variable.ttf` | TrueType | **Render con cairosvg** (instalar en fontconfig) |
| `SuraSans-Variable.woff2` | WOFF2 | Web (`@font-face`, el más liviano) |
| `SuraSans-Variable.woff` | WOFF | Web (fallback de compatibilidad) |

### Característica clave: es una **fuente variable**

- Family name: **`Sura Sans`** · 315 glifos · `units-per-em=1000`.
- **Cobertura completa de español**: A-Z, á é í ó ú ñ Ñ ü ¿ ¡ — sin glifos
  faltantes (verificado).
- Trae un eje `wght` (peso): **min 0 · default 450 · max 1000**. Un **solo
  archivo** produce todos los pesos de marca — no se necesitan ficheros
  estáticos separados por peso.
- Mapa peso de marca → valor del eje `wght`:
  - Regular → **400**
  - Seminegrita → **600**
  - Negrita → **700**
  (Fina/Ligera existen en el eje pero están **prohibidas en web** por contraste.)

### Render con cairosvg (workflow verificado)

cairosvg resuelve la fuente vía **fontconfig**, no por ruta directa. Instálala
una vez por sesión antes de renderizar:

```python
import shutil, subprocess, os
# 1) Instalar la fuente en la ruta de usuario de fontconfig
dst = os.path.expanduser('~/.fonts')
os.makedirs(dst, exist_ok=True)
shutil.copy('assets/fonts/SuraSans-Variable.ttf', f'{dst}/SuraSans-Variable.ttf')
subprocess.run(['fc-cache', '-f', dst], check=True)

# 2) En el SVG, declarar family + weight
#    <text font-family="Sura Sans" font-weight="700" font-size="62">Hola</text>
import cairosvg
cairosvg.svg2png(bytestring=svg.encode(), write_to='out.png')
```

> **Verificado:** cairosvg usa la fuente, respeta los pesos 400/600/700 como
> grosores progresivamente distintos (honra el eje variable `wght`) y renderiza
> las tildes/eñes del español correctamente.

> **Nota de entorno:** `fc-cache` está disponible; `fc-list` **no**. No dependas
> de `fc-list` para verificar la instalación — valida con un render de prueba.
