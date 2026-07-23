# Grillas y disposición (layout) — Sistema de Diseño SURA

Fuente: Manual de marca, sección "Disposición (layout)".

---

## 1. Sistema de espaciado (Frame System)

Se usan **seis valores** de espaciado para que la interfaz se sienta
consistente y armoniosa. Aplican tanto horizontal como verticalmente.

| Token | Valor | Uso típico |
|---|---|---|
| `--space-0` | **0 px** | Sin espacio |
| `--space-1` | **8 px** | Espaciado mínimo entre elementos relacionados |
| `--space-2` | **16 px** | Espaciado base / entre componentes hermanos |
| `--space-3` | **24 px** | Espaciado entre grupos pequeños |
| `--space-4` | **32 px** | Separación entre secciones cortas |
| `--space-5` | **48 px** | Separación entre secciones medianas |
| `--space-6` | **64 px** | Separación entre secciones grandes |
| `--space-7` | **96 px** | Separación entre secciones de página completa |

> Nota: el manual lista la escala como **0, 8, 16, 32, 48, 64 y 96 px** y
> ejemplifica también 24 px en la tabla — incluimos 24 en los tokens por
> coherencia con las grillas (canal = 24 px).

### Reglas

1. Nunca uses espaciados intermedios fuera de la escala (no 10, 14, 20, 36 px).
2. Si necesitas un valor no contemplado, usa el inmediatamente inferior.
3. Aplica los mismos tokens horizontal y verticalmente.

---

## 2. Grilla Escritorio (Desktop)

Para estructurar el contenido horizontalmente. Suele usarse un número par de
columnas entre 2 y 12.

| Parámetro | Valor |
|---|---|
| Ancho de pantalla | **1440 px** |
| Alto de pantalla | **1024 px** |
| Margen lateral | **156 px** |
| Ancho de contenedor | **1128 px** |
| Columnas | **12** |
| Ancho de columna | **72 px** |
| Ancho de canal (gutter) | **24 px** |

```
| 156 |[72|24|72|24|72|24|72|24|72|24|72|24|72|24|72|24|72|24|72|24|72|24|72]| 156 |
   ←─ margen ─→  ←──────────── contenedor 1128 px ────────────→  ←─ margen ─→
```

### Reglas escritorio

- Las columnas tienen **ancho fluido** (`fill container`).
- El margen lateral se mantiene fijo en 156 px hasta el viewport de 1440 px.
- Los canales (gutters) son de 24 px y **no** son fluidos.

---

## 3. Grilla Tablet

| Parámetro | Valor |
|---|---|
| Ancho de pantalla (vertical) | **792 px** |
| Margen lateral | **24 px** |
| Ancho de contenedor | **744 px** |
| Columnas | **8** |
| Ancho de columna | **72 px** |
| Ancho de canal | **24 px** |

---

## 4. Grilla Móvil

| Parámetro | Valor |
|---|---|
| Ancho de pantalla (vertical) | **416 px** |
| Margen lateral | **28 px** |
| Ancho de contenedor | **360 px** |
| Columnas | **4** |
| Ancho de columna | **72 px** |
| Ancho de canal | **24 px** |

```
| 28 |[72|24|72|24|72|24|72]| 28 |
  ←margen→ ←─ contenedor 360 px ─→ ←margen→
```

> ✅ **Verificado contra la lámina *Grillas Mobile*:** 28 + (4×72) + (3×24) + 28
> = 28 + 288 + 72 + 28 = **416 px**. La **columna móvil es 72 px** (igual que
> tablet y desktop): el ancho de columna es constante en toda la marca; lo que
> cambia entre breakpoints es el **número de columnas** y el **margen**, no el
> ancho de columna.

---

## 5. Resumen comparativo

| Breakpoint | Pantalla | Columnas | Margen | Columna | Canal |
|---|---|---|---|---|---|
| Desktop | 1440 px | 12 | 156 px | 72 px | 24 px |
| Tablet | 792 px | 8 | 24 px | 72 px | 24 px |
| Móvil | 416 px | 4 | 28 px | 72 px | 24 px |

---

## 6. Reglas operativas para el skill

1. Para mockups web, usa el ancho de **1440 px** y la grilla de 12 columnas.
2. Para mockups tablet, usa **792 px** y 8 columnas.
3. Para mockups móviles, usa **416 px** y 4 columnas.
4. Los **canales son siempre 24 px** en los tres breakpoints.
5. **Nunca** uses una grilla con número impar de columnas.
6. El contenido no debe invadir los márgenes laterales.
7. Para componentes que ocupen "media columna" en móvil, usa `calc((100% - 24px) / 2)` —
   no inventes anchos fijos.

---

## 7. CSS tokens

```css
:root {
  /* Escala de espaciado */
  --space-0: 0;
  --space-1: 8px;
  --space-2: 16px;
  --space-3: 24px;
  --space-4: 32px;
  --space-5: 48px;
  --space-6: 64px;
  --space-7: 96px;

  /* Grilla Desktop (≥ 1024px) */
  --grid-desktop-width: 1440px;
  --grid-desktop-margin: 156px;
  --grid-desktop-container: 1128px;
  --grid-desktop-cols: 12;
  --grid-desktop-col-width: 72px;
  --grid-desktop-gutter: 24px;

  /* Grilla Tablet (768 - 1023px) */
  --grid-tablet-width: 792px;
  --grid-tablet-margin: 24px;
  --grid-tablet-container: 744px;
  --grid-tablet-cols: 8;
  --grid-tablet-col-width: 72px;
  --grid-tablet-gutter: 24px;

  /* Grilla Móvil (< 768px) */
  --grid-mobile-width: 416px;
  --grid-mobile-margin: 28px;
  --grid-mobile-container: 360px;
  --grid-mobile-cols: 4;
  --grid-mobile-col-width: 72px;
  --grid-mobile-gutter: 24px;
}

.container {
  width: var(--grid-desktop-container);
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(var(--grid-desktop-cols), 1fr);
  gap: var(--grid-desktop-gutter);
}

@media (max-width: 1023px) {
  .container {
    width: var(--grid-tablet-container);
    grid-template-columns: repeat(var(--grid-tablet-cols), 1fr);
  }
}

@media (max-width: 767px) {
  .container {
    width: var(--grid-mobile-container);
    grid-template-columns: repeat(var(--grid-mobile-cols), 1fr);
    padding: 0 var(--grid-mobile-margin);
  }
}
```
