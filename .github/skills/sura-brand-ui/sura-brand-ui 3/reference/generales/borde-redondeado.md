# Bordes redondeados — Sistema de Diseño SURA

Fuente: Manual de marca, sección "Bordes redondeados".

---

## 1. Valores autorizados

Solo se permiten **cuatro valores** de radio de borde. Le confieren a la
interfaz un aspecto más cercano y acogedor.

| Token | Valor | Uso típico |
|---|---|---|
| `--radius-sm` | **8 px** | Chips, etiquetas, inputs compactos |
| `--radius-md` | **12 px** | Campos de texto, cards pequeños |
| `--radius-lg` | **16 px** | Cards medianos, modales pequeños, contenedores |
| `--radius-xl` | **24 px** | Cards grandes, banners, contenedores destacados |

> ⚠ **Los botones NO usan esta escala.** El átomo Botón es **siempre píldora**
> (radio = altura ÷ 2, esquinas semicirculares completas — ver `botones.md` §3).
> Un botón de 56 px → radio 28 px, que supera el tope de 24 px de esta escala a
> propósito. Esta escala (8/12/16/24) y el tope de 24 px aplican a contenedores
> **rectangulares** (cards, inputs, modales), no a componentes píldora.

---

## 2. Regla del 50 % de altura

**Regla maestra:** el valor del radio debe ser **aproximadamente el 50 % de
la altura del elemento** al que se aplica.

| Altura del elemento | Radio recomendado |
|---|---|
| 16 px | 8 px |
| 24 px | 12 px |
| 32 px | 16 px |
| 48 px | 24 px |
| > 48 px | 24 px (tope máximo) |

Para elementos muy pequeños (chips, badges), aplicar 8 px aunque la regla del
50 % daría menos.

> **Relación con la píldora:** la "regla del 50 %" es la misma idea que el radio
> píldora (altura ÷ 2). La diferencia es el **tope de 24 px**: para contenedores
> rectangulares se respeta el tope; para componentes **píldora** (botones,
> switches, tags redondas) **no hay tope** — el radio sigue altura ÷ 2 aunque
> supere 24 px.

---

## 3. Reglas operativas para el skill

1. Nunca uses valores intermedios fuera de la escala (no 10 px, 14 px, 20 px).
2. Si la altura del elemento no encaja exactamente, **redondea al valor
   inferior**, no al superior.
3. Para **pildoras / botones tipo pill** (radio = altura/2 con esquinas
   completamente redondas) usa `border-radius: 9999px` solo cuando el manual
   lo permita explícitamente — en duda, usa 24 px.
4. **No uses borde redondeado en:**
   - Tablas de datos (esquinas internas).
   - Imágenes a sangrado.
   - Áreas grandes de contenido (más de la mitad del viewport).
5. Aplica el mismo radio en **todas las esquinas** salvo que el componente
   indique lo contrario (ej. dropdown que se conecta a un input).

---

## 4. CSS tokens

```css
:root {
  /* Radios autorizados */
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 24px;
}

/* Ejemplos de aplicación (contenedores rectangulares) */
.chip       { border-radius: var(--radius-sm); }   /* chips / etiquetas */
.input      { border-radius: var(--radius-md); }   /* alto 32-40px */
.card       { border-radius: var(--radius-lg); }   /* alto > 32px */
.card-hero  { border-radius: var(--radius-xl); }   /* hero / banner */

/* Botones: SIEMPRE píldora, no usar la escala de arriba (ver botones.md) */
.button     { border-radius: calc(var(--btn-height) / 2); } /* p. ej. 56px → 28px */
```
