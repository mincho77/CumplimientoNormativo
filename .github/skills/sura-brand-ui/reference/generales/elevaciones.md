# Elevaciones — Sistema de Diseño SURA

Fuente: Manual de marca, sección "Elevaciones".

> **Nota:** la sección web del manual define cinco niveles (DP1–DP5) y su
> propósito, pero **no especifica los valores exactos de `box-shadow`** en el PDF
> web (son ejemplos visuales). Los valores DP1–DP5 listados abajo son
> **propuestos** (prácticas estándar adaptadas a la marca) y deben **validarse**.
>
> ✅ **El PDF *Elevaciones — mobile* SÍ trae valores exactos** para DP1–DP3 y, lo
> más importante, **confirma el color de sombra de marca: `#1D428A`** (azul, no
> negro). Esto resuelve el pendiente histórico sobre el color de sombra: úsalo
> como color canónico de sombra en toda la interfaz (web y mobile). Ver §4.bis.

---

## 1. Propósito

Las elevaciones diferencian visualmente los componentes en pantalla y comunican
**clicabilidad / jerarquía**: cuanto más alto el nivel, más cerca del usuario
está el elemento y más interactivo se percibe.

---

## 2. Niveles autorizados

Solo se permiten **cinco niveles**: `DP1`, `DP2`, `DP3`, `DP4`, `DP5`.

| Token | Nivel | Uso típico | Valor propuesto (TODO validar) |
|---|---|---|---|
| `--elevation-dp1` | DP1 | Cards en reposo, contenedores planos | `0 1px 2px rgba(0, 0, 0, 0.06)` |
| `--elevation-dp2` | DP2 | Botones en reposo, inputs activos | `0 2px 4px rgba(0, 0, 0, 0.08)` |
| `--elevation-dp3` | DP3 | Cards interactivas, hover de botones | `0 4px 8px rgba(0, 0, 0, 0.10)` |
| `--elevation-dp4` | DP4 | Dropdowns, tooltips, popovers | `0 8px 16px rgba(0, 0, 0, 0.12)` |
| `--elevation-dp5` | DP5 | Modales, drawers, diálogos | `0 16px 32px rgba(0, 0, 0, 0.16)` |

---

## 3. Reglas operativas para el skill

1. Cualquier componente clickeable o interactivo debe tener **al menos DP1**.
2. **No usar elevaciones intermedias** fuera de la escala (DP1.5, DP6, etc.).
3. Los **modales y diálogos** siempre van en DP5.
4. En **hover** de un componente, sube **un nivel** de elevación
   (DP2 → DP3, DP3 → DP4).
5. **No combines** sombras con bordes oscuros: usa una u otro para crear
   separación, no ambos.
6. Las elevaciones **no aplican sobre fondos oscuros** (el contraste se logra
   con tonos claros de la paleta complementaria — ver `colores.md`).

---

## 3.bis Mobile / Responsivo

El PDF *Elevaciones — mobile* define **solo 3 niveles** (DP1, DP2, DP3) con
**valores medidos exactos** y un **color de sombra azul `#1D428A`** (no negro).
Estos son los valores autoritativos de marca:

| Token | Offset Y | Blur | Color | Opacidad |
|---|---|---|---|---|
| `DP1` | `2px` | `4` | `#1D428A` | `16%` |
| `DP2` | `4px` | `8` | `#1D428A` | `32%` |
| `DP3` | `4px-2`* | `30` | `#1D428A` | `16%` |

\* *`4px-2`* es la notación literal de la lámina para DP3: una sombra más
**difusa y amplia** (blur 30) con desplazamiento pequeño — visualmente la más
suave de las tres pese a su mayor blur. Interprétalo como offset Y ≈ `2px` con
gran difuminado (sombra ambiental), frente a DP1/DP2 que son sombras de contacto
más marcadas. Confirmar con marca el desglose exacto si se requiere multicapa.

**Reglas mobile:**
- En mobile la escala práctica se reduce a **DP1–DP3** (no se usan DP4/DP5 con
  sombras pesadas; los modales mobile suben a pantalla completa, ver
  `moleculas/modales.md`).
- **Color de sombra siempre `#1D428A`** con la opacidad del nivel — nunca negro
  puro. Esto homologa web y mobile.
- DP1 = reposo (cards/contenedores); DP2 = énfasis/activo; DP3 = sombra
  ambiental amplia para elementos flotantes ligeros.

```css
:root {
  /* Valores de marca confirmados (Elevaciones — mobile). Sombra azul #1D428A */
  --shadow-color: 29, 66, 138;                 /* #1D428A en RGB */
  --elevation-dp1: 0 2px 4px  rgba(var(--shadow-color), 0.16);
  --elevation-dp2: 0 4px 8px  rgba(var(--shadow-color), 0.32);
  --elevation-dp3: 0 2px 30px rgba(var(--shadow-color), 0.16);
}
```

> ⚠ Cuando exista conflicto, **estos valores mobile mandan** sobre los DP1–DP3
> "propuestos" de la tabla §2 (que eran placeholders con sombra negra).

---

## 4. CSS tokens

```css
:root {
  /* Elevaciones — TODO: validar valores exactos con equipo de marca */
  --elevation-dp1: 0 1px 2px rgba(0, 0, 0, 0.06);
  --elevation-dp2: 0 2px 4px rgba(0, 0, 0, 0.08);
  --elevation-dp3: 0 4px 8px rgba(0, 0, 0, 0.10);
  --elevation-dp4: 0 8px 16px rgba(0, 0, 0, 0.12);
  --elevation-dp5: 0 16px 32px rgba(0, 0, 0, 0.16);
}

/* Aplicación */
.card        { box-shadow: var(--elevation-dp1); }
.button      { box-shadow: var(--elevation-dp2); }
.button:hover{ box-shadow: var(--elevation-dp3); }
.dropdown    { box-shadow: var(--elevation-dp4); }
.modal       { box-shadow: var(--elevation-dp5); }
```

---

## 5. Pendiente

- [x] ~~Valores exactos de blur/offset/opacidad~~ → **DP1–DP3 confirmados** en
      *Elevaciones — mobile* (ver §3.bis). Faltan solo DP4–DP5.
- [x] ~~¿Color de sombra distinto al negro?~~ → **Sí: `#1D428A`** (azul),
      confirmado por la lámina mobile. Aplicado como `--shadow-color`.
- [ ] Obtener valores exactos para **DP4 y DP5** (no aparecen en la lámina
      mobile, que solo cubre DP1–DP3).
- [ ] Definir comportamiento en **dark mode** (sobre `#00003F` la separación se
      logra con borde `#81B1FF` tenue, no con sombra azul — ver `modo-oscuro.md`).
