# Colores — Sistema de Diseño SURA

Fuente: Manual de marca, secciones "Primarios", "Ilustraciones" y "Accesibilidad".

El esquema de color facilita el uso significativo en interfaces de usuario.
Las variaciones oscuras y brillantes de cada color se aplican de varias maneras.

---

## 1. Paleta Principal

Uso predominante en cualquier pieza de comunicación digital. Es la base.

| Nombre | HEX | Token sugerido |
|---|---|---|
| Azul cielo latino | `#2D6DF6` | `--color-primary` |
| Blanco todo puede pasar | `#FFFFFF` | `--color-on-primary` |

> ⚠ **Nomenclatura de los azules — el manual se contradice entre secciones.**
> El **mismo hex** recibe nombres distintos según el documento. **El hex manda,
> no el nombre.** Tabla de equivalencias para no confundirse:
>
> | Hex | "Primarios"/este doc | Botones.pdf | Interruptores.pdf |
> |---|---|---|---|
> | `#2D6DF6` | Azul cielo latino | **Azul SURA** | **Azul Vivo** |
> | `#0033A0` | Azul profundo | Azul Profundo | **Azul SURA** |
>
> Nomenclatura **canónica del skill = la de este documento** (Azul cielo latino
> / Azul profundo). Cuando un componente diga "Azul SURA", confirma el hex.

---

## 2. Paleta Complementaria

Combina con la principal para jerarquía y lectura.

| Nombre | HEX | Token sugerido |
|---|---|---|
| Azul profundo | `#0033A0` | `--color-secondary` |
| Amarillo sol | `#E3E829` | `--color-accent-yellow` |
| Aqua inesperado | `#00AEC7` | `--color-accent-aqua` |
| Azul cielo latino | `#2D6DF6` | `--color-primary` |
| Gris | `#888B8D` | `--color-neutral` |

### 2.1. Tonos neutros (Pantone)

| Nombre | HEX | Token sugerido |
|---|---|---|
| Pantone 2114 C | `#838DC8` | `--color-neutral-lavender` |
| Pantone 461 C | `#ECF0A1` | `--color-neutral-yellow` |
| Pantone 304 C | `#9BE1E9` | `--color-neutral-aqua` |
| Pantone 284 C | `#81B1FF` | `--color-neutral-blue` |
| Pantone 429 C | `#B4B4B5` | `--color-neutral-gray` |

---

## 3. Colores para fondos digitales

Uso exclusivo como **fondo de pantalla o sección** en piezas digitales.

| Nombre | HEX | Token sugerido |
|---|---|---|
| Fondo 1 | `#E5E9EA` | `--bg-1` |
| Fondo 2 | `#F9FAE1` | `--bg-2` |
| Fondo 3 | `#E6FAEF` | `--bg-3` |
| Fondo 4 | `#DFEAFF` | `--bg-4` |
| Fondo 5 | `#F8F8F8` | `--bg-5` |

---

## 4. Paleta para uso en componentes

### 4.1. Colores de alerta (uso exclusivo en Toast, Tags y variantes de error)

> ⚠️ **Restricción:** estos colores son de uso exclusivo para los componentes
> Toast, Tags y variantes de error. No está permitido usarlos en otro contexto.

| Estado | Color principal | Color de fondo (suave) |
|---|---|---|
| Éxito | `#067014` (Éxito 1) | `#DEF6DE` (Éxito 2) |
| Advertencia | `#ED8B00` (Advertencia 1) | `#FFF5EC` (Advertencia 2) |
| Error | `#D12D35` (Error 1) | `#FFF4F3` (Error 2) |
| Información | `#0033A0` (Información 1) | `#E0EAFF` (Información 2) |

Tokens sugeridos: `--alert-success`, `--alert-success-bg`, `--alert-warning`,
`--alert-warning-bg`, `--alert-error`, `--alert-error-bg`, `--alert-info`,
`--alert-info-bg`.

> 🔴 **Rojo de alerta/error — valor canónico único: `#D12D35`.** La matriz de
> paleta impresa de los manuales muestra en algunas láminas un rojo `#E4002B`,
> pero el valor **renderizado y en uso** en todos los componentes (Toast, Tags,
> Campos en error, Botón de error) es `#D12D35` (Error 1), con fondo suave
> `#FFF4F3` (Error 2) y hover `#B04B60` (§4.3). Por la regla de marca «el hex
> manda sobre el nombre impreso / confía en la muestra renderizada», **`#E4002B`
> queda superado por `#D12D35`**. No usar `#E4002B`: cualquier aparición de ese
> hex en código es una desviación a corregir hacia `#D12D35`.

### 4.2. Escala de grises

| Nombre | HEX | Token sugerido |
|---|---|---|
| Gris 100 | `#F4F4F4` | `--gray-100` |
| Gris 200 | `#E7E7E7` | `--gray-200` |
| Gris 500 | `#3F3F41` | `--gray-500` |
| Negro | `#0D0D0D` | `--gray-900` |

### 4.3. Otros colores (uso restringido)

| Nombre | HEX | Uso |
|---|---|---|
| Amarillo oscuro | `#C5CB15` | Estado *sobre* (hover) del botón **amarillo** — CTA en claro y **acción primaria en oscuro** |
| Rojo oscuro | `#B04B60` | **Exclusivamente** estado *sobre* (hover) del botón de error |
| Azul oscuro | `#00003F` | **Exclusivamente** componentes en modo oscuro (fondo/superficie) |

> ⚠ **Corrección de nomenclatura:** el manual rotula esta fila como "hover del
> botón primario", pero el botón **Primario es el azul** y su hover es Azul
> profundo `#0033A0` (ver `botones.md` §7). El `#C5CB15` es el hover del botón
> **amarillo** (`#E3E829` → oscurece hacia `#C5CB15`; el muestreo de la lámina
> dio `~#C0C810`, mismo tono).

> 🟡 **El amarillo manda en modo oscuro.** El mockup "Diálogo base" de la lámina
> sobre `#00003F` y la lámina de botones (`Botones.pdf`: "Botón Primario -
> Amarillo", "Botón Secundario - Amarillo (Dark mode)") muestran que en oscuro
> el **Amarillo alegría `#E3E829` es el acento de resaltado**: relleno del botón
> primario (texto navy `#00003F`), contorno del secundario, **avatares**,
> **casillas de verificación**, selección activa y estrellas. Es decir, el
> amarillo deja de ser exclusivo del CTA **en oscuro** y pasa a ser la acción
> primaria general. El azul foco `#81B1FF` se reserva para texto/enlaces/bordes
> de lectura. Detalle completo en `generales/modo-oscuro.md` §1 y §5.

Tokens sugeridos: `--btn-cta-hover` (≡ `--btn-primary-hover`), `--btn-error-hover`,
`--dark-mode-bg`.

---

## 5. Paleta de colores para ilustraciones

> ⚠️ **Restricción:** esta paleta es de **uso exclusivo en ilustraciones y
> pictogramas**. No está permitido utilizarla en un contexto diferente.

### Naranjas y marrones
`#FFAA5C` · `#FF7768` · `#765238` · `#A47A59` · `#CB9A6E`

### Aquas y azules profundos
`#00AEC7` · `#D5F5F8` · `#00003F` · `#001263` · `#26328C`

### Beiges y amarillos
`#E7BE92` · `#F8CFA9` · `#8F8C00` · `#E3E829` · `#ECF0A1`

### Azules y lila
`#838DC8` · `#001F91` · `#0033CC` · `#2D6DF6` · `#81B1FF`

### Verdes
`#F9FAE1` · `#006947` · `#006276`

### Neutros oscuros
`#060618` · `#333F48` · `#888B8D` · `#B4B4B5` · `#E7E7E7`

---

## 6. Proporción de color (regla 60 / 30 / 10)

La correcta aplicación de proporción garantiza homogeneidad en todos los
materiales de comunicación.

### 6.1. Proporción con paleta principal predominante

Ideal para la mayor cantidad de piezas. Garantiza consistencia y diferenciación
de marca.

- **60%** — paleta principal (Azul cielo latino + Blanco)
- **30%** — paleta complementaria (Azul profundo / Amarillo sol / Aqua / Gris)
- **10%** — acentos de complementaria para jerarquía

### 6.2. Proporción con paleta secundaria predominante

Para piezas digitales que requieren **mayor facilidad de lectura y contraste**.

- **60%** — paleta digital de fondos (Fondo 1–5)
- **30%** — paleta complementaria
- **10%** — acentos de la principal

**Regla práctica:** Si la pantalla es de contenido denso (formularios, tablas,
dashboards), prefiere proporción 6.2. Si es una landing o banner promocional,
prefiere proporción 6.1.

---

## 7. Accesibilidad — Contraste WCAG 2.1

El contraste entre fondo y contenido (texto) debe ser suficiente para garantizar
legibilidad. Beneficia especialmente a personas con baja sensibilidad al
contraste.

### Relaciones mínimas exigidas

| Tipo de contenido | Mínimo AA | Recomendado AAA |
|---|---|---|
| Cuerpo de texto | 4.5 : 1 | 7 : 1 |
| Componentes activos (íconos, gráficos, UI) | 3 : 1 | No definido |

### Criterios WCAG nombrados (de la lámina "3. Accesibilidad")

La lámina de marca evalúa cada par fondo/texto contra **dos criterios de éxito
WCAG 2.1 explícitos**, con un veredicto Pass/Fail por separado para cada uno.
Úsalos como rúbrica al validar (no basta con "≥4.5:1"):

| Criterio | Aplica a | Umbral | Sub-veredictos de la lámina |
|---|---|---|---|
| **1.4.3 Contraste (Mínimo) (AA)** | Texto | 4.5:1 (regular) · 3:1 (large) | `Pass/Fail (regular text)` **y** `Pass/Fail (large text)` por separado |
| **1.4.11 Contraste sin texto (AA)** | Componentes UI y objetos gráficos | 3:1 | `Pass/Fail (UI components and graphical objects)` |

> **Large text** = ≥18pt, o ≥14pt en negrita. Un par puede **fallar** 1.4.3 en
> regular pero **pasar** en large (ej. `#838DC8`+blanco = 3.2:1 → Fail regular /
> Pass large). Por eso un color que falla para cuerpo puede usarse en titulares
> grandes. Documenta SIEMPRE qué tamaño asumiste.

> ⚠ **Sin ejemplo en modo oscuro:** la lámina de Accesibilidad es **100 % modo
> claro** — cada tarjeta usa un fondo claro (Fondo 1–5, azul `#2D6DF6`/`#0033A0`)
> con texto `#0033A0` o blanco. **No existe ninguna tarjeta de contraste sobre
> `#00003F`.** El contraste de modo oscuro NO viene de una imagen de ejemplo: se
> **deriva y verifica con Python** sobre `#00003F` (ver `modo-oscuro.md` §6). El
> único mockup oscuro de marca es el "Diálogo base" de `Colores.pdf`, del que
> proviene la regla del acento amarillo — no es una tabla de contrastes.

### 7.1. Combinaciones recomendadas (PASS AA)

Todas estas combinaciones usan **texto Azul profundo `#0033A0`** sobre fondos
claros y pasan AA. Son la base segura para tipografía corporativa.

| Fondo | Texto | Ratio | Resultado |
|---|---|---|---|
| `#E5E9EA` (Fondo 1) | `#0033A0` | 8.7:1 | ✅ Pass AA |
| `#F9FAE1` (Fondo 2) | `#0033A0` | 10:1 | ✅ Pass AA + AAA |
| `#E6FAEF` (Fondo 3) | `#0033A0` | 9.7:1 | ✅ Pass AA + AAA |
| `#DFEAFF` (Fondo 4) | `#0033A0` | 8.8:1 | ✅ Pass AA + AAA |
| `#F8F8F8` (Fondo 5) | `#0033A0` | 10:1 | ✅ Pass AA + AAA |
| `#ECF0A1` (Pantone 461 C) | `#0033A0` | 8.8:1 | ✅ Pass AA + AAA |
| `#9BE1E9` (Pantone 304 C) | `#0033A0` | 7.2:1 | ✅ Pass AA + AAA |
| `#81B1FF` (Pantone 284 C) | `#0033A0` | 4.9:1 | ✅ Pass AA |
| `#E3E829` (Amarillo sol) | `#0033A0` | 8:1 | ✅ Pass AA + AAA |
| `#0033A0` | `#FFFFFF` | 10.6:1 | ✅ Pass AA + AAA |
| `#2D6DF6` | `#FFFFFF` | 4.5:1 | ✅ Pass AA |

### 7.2. Combinaciones NO recomendadas (FAIL AA)

Evitar estas combinaciones para cuerpo de texto. Solo válidas si texto es
"large text" (≥18pt o ≥14pt bold).

| Fondo | Texto | Ratio | Resultado |
|---|---|---|---|
| `#FFFFFF` | `#888B8D` (Gris) | 3.4:1 | ❌ Fail texto regular |
| `#FFFFFF` | `#838DC8` (Pantone 2114 C) | 3.2:1 | ❌ Fail texto regular |
| `#FFFFFF` | `#B4B4B5` (Pantone 429 C) | 2.1:1 / 2.7:1 | ❌ Fail todo |

---

## 8. Reglas operativas para el skill

Al generar un mockup, aplica estas reglas en orden:

1. **Fondo de pantalla**: usa uno de los Fondos 1–5 (`#E5E9EA`, `#F9FAE1`,
   `#E6FAEF`, `#DFEAFF`, `#F8F8F8`) o blanco `#FFFFFF`.
2. **Texto principal (cuerpo)**: usa Azul profundo `#0033A0` o Negro `#0D0D0D`
   para máxima legibilidad sobre cualquier fondo claro.
3. **CTAs primarios** (botón azul): fondo Azul cielo latino `#2D6DF6` con texto
   blanco `#FFFFFF`. Hover → fondo Azul profundo `#0033A0` (ver `botones.md`).
   > ⚠ El `#C5CB15` (Amarillo oscuro) **NO** es el hover del botón azul. Es el
   > hover **exclusivo del botón amarillo** (`--btn-primary-hover` en §4.3).
   > No confundir: cada color de botón oscurece hacia su propio tono.
4. **CTAs secundarios**: fondo Blanco con borde y texto Azul cielo latino
   `#2D6DF6`.
5. **Alertas**: usa los colores 4.1 únicamente en Toast, Tags y variantes de
   error. Nunca como fondo decorativo.
6. **Ilustraciones / pictogramas**: usa la paleta sección 5. Nunca uses esa
   paleta para texto, botones u otros componentes.
7. **Proporción 60/30/10**: respeta una de las dos proporciones (6.1 ó 6.2)
   según el tipo de pieza.
8. **Contraste**: antes de aprobar una combinación texto/fondo, valida que la
   relación supere 4.5:1 (cuerpo) o 3:1 (componentes UI). Si está en la sección
   7.2, NO la uses para texto regular.

---

## 9. CSS Variables — copiar tal cual

```css
:root {
  /* Paleta principal */
  --color-primary: #2D6DF6;
  --color-on-primary: #FFFFFF;

  /* Paleta complementaria */
  --color-secondary: #0033A0;
  --color-accent-yellow: #E3E829;
  --color-accent-aqua: #00AEC7;
  --color-neutral: #888B8D;

  /* Tonos neutros */
  --color-neutral-lavender: #838DC8;
  --color-neutral-yellow: #ECF0A1;
  --color-neutral-aqua: #9BE1E9;
  --color-neutral-blue: #81B1FF;
  --color-neutral-gray: #B4B4B5;

  /* Fondos digitales */
  --bg-1: #E5E9EA;
  --bg-2: #F9FAE1;
  --bg-3: #E6FAEF;
  --bg-4: #DFEAFF;
  --bg-5: #F8F8F8;

  /* Alertas (uso exclusivo Toast/Tag/Error) */
  --alert-success: #067014;
  --alert-success-bg: #DEF6DE;
  --alert-warning: #ED8B00;
  --alert-warning-bg: #FFF5EC;
  --alert-error: #D12D35;
  --alert-error-bg: #FFF4F3;
  --alert-info: #0033A0;
  --alert-info-bg: #E0EAFF;

  /* Escala de grises */
  --gray-100: #F4F4F4;
  --gray-200: #E7E7E7;
  --gray-500: #3F3F41;
  --gray-900: #0D0D0D;

  /* Estados de hover (uso restringido) */
  --btn-primary-hover: #0033A0;     /* botón azul (Primario) → Azul profundo */
  --btn-cta-hover: #C5CB15;         /* botón amarillo (CTA) → Amarillo oscuro */
  --btn-error-hover: #B04B60;

  /* Modo oscuro */
  --dark-mode-bg: #00003F;
}
```
