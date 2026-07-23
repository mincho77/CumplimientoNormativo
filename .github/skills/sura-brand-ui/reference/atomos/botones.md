# Botones — Sistema de Diseño SURA (Átomo)

Fuente: Manual de marca, sección "Botones" (Botones.pdf).

> **Nota de método:** los valores de este documento se extrajeron de las
> **imágenes** del PDF (página de Construcción), no del texto. La página de
> *showcase* (matriz de estados) no contiene ningún número — solo "Botones" de
> relleno. Los specs reales están en las anotaciones de la lámina de
> Construcción. Verificado renderizando el botón y comparándolo con el PDF.

---

## 1. Concepto

Elemento interactivo que ejecuta una acción. Es lo más importante a nivel de
decisión por parte del usuario; sus variantes se usan según la jerarquía de la
acción en la interfaz.

---

## 2. Anatomía

1. **Etiqueta** (texto de la acción).
2. **Ícono** (opcional) — puede ir a la izquierda, derecha o ambos lados.
3. **Contenedor** — forma tipo **píldora** (capsule).

---

## 3. Forma — píldora

El contenedor es **siempre una píldora**: el radio de esquina = **altura ÷ 2**.
Nunca esquinas suavemente redondeadas; las puntas son semicírculos completos.

---

## 4. Tamaños (verificado)

| Tamaño | Altura | Radio (alto÷2) | Pad. horizontal | Ancho mín | Texto |
|---|---|---|---|---|---|
| **Grande** | 56 px | **28 px** | 48 px | 150 px | 16 px (1 rem) |
| **Mediano** | 48 px | **24 px** ⚠ | 48 px | 150 px | 16 px |
| **Pequeño** | 40 px | **20 px** | 16 px | 100 px | 16 px |

> ⚠ **Inconsistencia del PDF:** el bloque del botón Mediano reusa el widget del
> Grande (muestra "56 ÷ 2 = 28 px", H 56, radio 28) — es un copy-paste. La
> altura base escrita del Mediano es **48 px**, por lo que el radio correcto es
> **24 px**. Usamos el valor derivado de la regla píldora (alto÷2), no el 28 px
> heredado por error.

### Espaciado vertical (padding)
- Grande: **16 px** · Mediano: **12 px** · Pequeño: ~8 px (confirmar).

### Anchos máximos (Grande)
- Sin íconos: **258 px** · con 1 ícono: **298 px** · con 2 íconos: **338 px**.
- Límite de **20 caracteres** de etiqueta. Botón de 150 px sin ícono → límite
  de **4 caracteres**.

---

## 5. Íconos en el botón

- Tamaño de ícono: **24 px** según la anotación de la lámina (los íconos del
  botón van a 24px para mantener simetría). ⚠ El CSS del PDF exporta los íconos
  a **16 px** (`.iconos-figurativos { height:16px }`); ante la duda, manda la
  lámina (24 px). Si el ícono debe alinearse al texto de 16 px, 16 px también es
  válido — documentar la elección.
- Separación **ícono ↔ etiqueta**: **16 px**.
- Con ícono, el **ancho mínimo** del botón sube a **180 px** (Grande/Base).
- Disposición: ícono-izquierda, ícono-derecha o ambos lados.
- Los íconos salen del banco oficial (`assets/icons/`, estilo outline) — ver
  `iconos.md`.

---

## 6. Estados (6)

| Estado | Comportamiento visual |
|---|---|
| **Por defecto** | Color base de la variante. |
| **Cursor sobre** (hover) | Tono más oscuro de la variante. |
| **Presionado** | Tono aún más oscuro. |
| **Cargando** | Spinner dentro del botón. |
| **Enfocado** | Anillo de foco exterior alrededor de la píldora. |
| **Inactivo** | Gris claro deshabilitado, texto gris (sin interacción). |

---

## 7. Variantes y colores

Colores **verificados por muestreo de píxeles** en la lámina (coinciden con la
paleta de marca):

> **Nomenclatura del manual:** la jerarquía en el panel de Figma se llama
> **Primario** y **CTA** (no "Primario Amarillo"). El "amarillo" es la jerarquía
> **CTA**; el azul es **Primario**.

| Variante | Fondo por defecto | Hover | Texto |
|---|---|---|---|
| **Primario (Azul)** | `#2D6DF6` (Azul SURA) | `#0033A0` (Azul Profundo) | Blanco `#FFFFFF` |
| **CTA (Amarillo)** | `#E3E829` (Amarillo alegría) | tono más oscuro (`~#C0C810`) | Azul Profundo |
| **Secundario (Azul)** | Blanco, borde 1 px + texto azul (outline) | borde/texto más oscuro | azul (ver nota) |
| **Secundario Amarillo (dark mode)** | Outline sobre fondo oscuro | — | amarillo/claro |
| **Peligro** | Blanco, borde 1 px + texto rojo (outline); existe también versión sólida (relleno rojo, texto blanco) | tono más oscuro | `#D12D35` |
| **Inactivo (deshabilitado)** | `#E7E7E7` (gris platinum) | — | `#818181` (gris) |
| **Icónico** | solo ícono, contenedor circular (píldora cuadrada) | — | — |

> El estado **Presionado** muestrea ~`#1840A8` (azul aún más oscuro). Rojo de
> **Peligro** = `#D12D35` (muestreado de la lámina, pág. 3). **Inactivo** =
> fondo `#E7E7E7` + texto `#818181` (de las variables `:root` del PDF).
> Pendientes: hex del spinner **Cargando** y del anillo **Enfocado** (en las
> láminas no aparecen como swatch con número — heredan el color de la variante:
> spinner = color del texto; anillo de foco = Azul SURA `#2D6DF6`).

> **⚠ Color del Secundario — conflicto de fuentes:** la lámina muestra el
> outline en Azul SURA `#2D6DF6`, pero el CSS del PDF lo pinta con la variable
> `--smalt` = `rgba(0,55,143)` = `#00378F` (azul más profundo). Igual pasa con
> el texto del CTA: lámina/paleta dice Azul Profundo `#0033A0`, el CSS usa
> `--primaryazul-profundo` = `rgba(38,50,140)` = `#26328C`. Son aproximaciones
> distintas del "azul profundo". **Se sigue la paleta de marca** (`colores.md`):
> Azul Profundo `#0033A0`.

---

## 7.4 Variante por tema: Azul (claro) ↔ Amarillo (oscuro) — CLAVE

La lámina de showcase (`Botones.pdf` pág. 1) ordena los botones en pares de
tema, no solo por jerarquía:

- **Botón Primario - Azul** y, justo debajo, **Botón Primario - Amarillo.**
- **Botón Secundario - Azul** y **Botón Secundario - Amarillo (Dark mode)**
  (la lámina **rotula literalmente "Dark mode"** en la fila amarilla).

Lectura correcta: **el "amarillo" no es una jerarquía aparte, es el render del
botón en modo oscuro.** En oscuro la jerarquía primaria se pinta amarilla y la
secundaria queda como contorno amarillo. Por tanto:

| Variante | Claro | Oscuro (`#00003F`) |
|---|---|---|
| **Primario** | relleno `#2D6DF6` + texto blanco | **relleno `#E3E829` + texto navy `#00003F`** (hover Amarillo oscuro `~#C9CE12`) |
| **Secundario** | contorno + texto azul `#2D6DF6` | **contorno + texto `#E3E829`** (hover: leve relleno amarillo translúcido) |
| **Peligro** | contorno/relleno rojo `#D12D35` | contorno rojo; **hover usa Rojo oscuro `#B04B60`** (`colores.md`) |
| **Terciario (ghost)** | texto azul, sin contorno | texto `#81B1FF`, sin contorno |

- En ambos temas el **anillo Enfocado** se mantiene en Azul SURA `#2D6DF6`
  (también legible sobre amarillo y sobre oscuro).
- Texto sobre relleno amarillo = navy `#00003F` (14.78:1 ✅), **no** blanco.
- Esto deja sin efecto, **solo para oscuro**, la antigua regla "amarillo =
  exclusivo del CTA": en oscuro el amarillo es la acción primaria general.

---

## 7.5 ⚠ El HTML/CSS del PDF NO es fuente de verdad

La página 6 ("Botones HTML - CSS") trae código que **contradice las láminas de
construcción y a sí mismo**. Es un export automático tipo Figma/Anima, no un
spec curado. Evidencia concreta:

| Aspecto | CSS del PDF (pág. 6) | Lámina / marca | Decisión del skill |
|---|---|---|---|
| **Radio** | Primario y CTA: `border-radius: 5px` (plano); Secundario: `border-radius: 50px` (píldora) — **incoherente entre variantes** | Todos píldora (alto÷2) | **Píldora** (radio = alto÷2) |
| **Fuente** | `--font-family-barlow: "Barlow"` (Google Font de relleno) | `Sura Sans` corporativa | **Sura Sans** |
| **Ícono** | `.iconos-figurativos { height: 16px }` | Lámina anota 24 px | Ver §5 (lámina manda; CSS exporta 16) |
| **Peso del texto** | `font-weight: 700` (Negrita) | — | **700 Negrita** (corregido; antes asumí 600) |

Lo que **sí coincide** entre CSS y lámina (y por tanto es confiable):
`height: 56px`, `padding: 16px 48px`, `gap: 16px`, `align/justify: center`,
fondo Primario = `--primaryazul-sura` `#2D6DF6`, CTA = `--primaryamarillo-alegra`
`#E3E829`, texto Primario = blanco.

**Regla:** usa el CSS solo para confirmar medidas de caja (alto/padding/gap).
Para forma, fuente, color y estados, manda la **lámina + paleta de marca**.
Esto confirma la sospecha del analista: las secciones de código se exportaron
"por encima", sin alinearlas con el diseño.

### Variables `:root` recuperadas del PDF (RGB → hex)

```
--primaryazul-sura:      rgba(45,109,246)  → #2D6DF6  (Azul SURA)
--primaryazul-profundo:  rgba(38,50,140)   → #26328C  (≠ paleta #0033A0)
--smalt:                 rgba(0,55,143)    → #00378F  (azul profundo alterno)
--primaryamarillo-alegra:rgba(227,232,41)  → #E3E829  (Amarillo alegría)
--primaryblanco-lienzo:  rgba(255,255,255) → #FFFFFF
--scale-grayplatinum:    rgba(231,231,231) → #E7E7E7  (Inactivo fondo)
--scale-graygray:        rgba(129,129,129) → #818181  (Inactivo texto)
--scale-grayblack:       rgba(0,0,0)       → #000000
--font-size-m: 16px · --font-size-1: 22px
```

---

## 7.6 Mobile / Responsivo — módulos de botón

Fuente: *Botones mobile.pdf* ("Multiplataforma, módulos de botón" + "Buenas
prácticas de prototipado"). El **átomo botón no cambia** (forma píldora, tamaños,
colores, estados); lo que define el móvil es **cómo se agrupan** los botones.

### Construcción del módulo (regla de la derecha)
El módulo de botones **se arma desde la derecha**: el **primario va a la derecha**
y hacia la izquierda se agregan el **secundario** y luego el **terciario** (este
último solo si es estrictamente necesario). El tercer nivel se reserva para botón
terciario o **vínculo de texto**.

### Dos disposiciones en móvil
| Disposición | Cuándo | Detalle |
|---|---|---|
| **Horizontal** | 2 acciones (primario + secundario) | van lado a lado; **ancho máximo del módulo = 344 px**. Si el módulo lleva un solo botón, el **primario ocupa los 344 px completos** (ancho completo del dispositivo). |
| **Vertical** | 3 acciones (se necesita terciario / vínculo de texto) | botones **apilados a ancho completo**; orden de arriba abajo: **primario → secundario → terciario**. |

> Se reserva la **disposición vertical** para cuando hay que agregar la tercera
> acción. Importante: todos los botones del grupo tienen el **mismo tamaño**.

### Espaciados del módulo móvil
- **Margen lateral:** 12 px.
- **Separación entre botones:** 16 px (tanto horizontal como vertical apilado).

### Tablet horizontal / Escritorio
Módulo alineado a la **derecha**, en fila: `Botón terciario · Texto de acción 2 ·
Acción primaria`, con **gap 16 px** entre cada uno y margen derecho 16 px.

### Buenas prácticas de prototipado (aplican también a web)
- **Define primero el texto/CTA**, luego el botón; una vez asignado el texto, **no
  reduzcas el ancho** del botón.
- **No uses un botón de longitud pequeña para un texto de acción largo.**
- Ejemplos de la lámina (ancho ✓/✗ según nº de caracteres + ícono):
  - 150 px / 29 caracteres → ✗ incorrecto (muy angosto para texto largo).
  - 196 px / 7 caracteres ("Comprar") → ✓ correcto.
  - 350 px / 29 caracteres → ✗ incorrecto.
  - 289 px / 19 caracteres ("Continuar comprando") → ✓ correcto.

---

## 8. Reglas operativas para el skill

1. Renderiza el contenedor como **píldora** (`rx = altura/2`). Nunca un radio
   fijo en px que no sea la mitad de la altura.
2. Usa la tabla §4 para alto/radio/padding según tamaño. Texto **16 px**
   **Negrita (700)** en **Sura Sans** (ver `tipografia.md`). El CSS y el
   styleguide del PDF confirman `font-weight: 700`.
3. Para íconos, toma SVG del banco (`assets/icons/`), recolorea
   `currentColor`→hex del texto del botón y renderiza a **24 px**; separa **16
   px** de la etiqueta.
4. Color por variante y estado según §7. Primario azul por defecto `#2D6DF6`,
   hover `#0033A0`; amarillo `#E3E829` con texto `#0033A0`.
5. Respeta ancho mínimo (150 / 100 px) y los topes de caracteres.
6. No inventes el radio del Mediano desde el PDF (está mal) — usa **24 px**.

---

## 9. Pendiente

- [x] ~~Hex de Peligro~~ → `#D12D35` (pág. 3). ~~Inactivo~~ → fondo `#E7E7E7`,
      texto `#818181` (variables `:root`, pág. 6).
- [ ] Hex del spinner **Cargando** y del anillo **Enfocado**: no aparecen como
      swatch numerado; se asumen color-de-texto / Azul SURA. Confirmar con marca.
- [ ] Confirmar padding vertical del Pequeño (≈8 px sin confirmar).
- [ ] Confirmar si el padding horizontal del Mediano es realmente 48 px (igual
      al Grande) o un valor menor — la anotación lo da en 48, revisable.
- [ ] Estilo exacto de la variante Icónico (diámetro = altura del tamaño).
- [ ] Reportar a marca la inconsistencia del radio del Mediano (28→24).
- [ ] Reportar a marca que el HTML/CSS (pág. 6) no concuerda con las láminas:
      radio 5px vs píldora, Barlow vs Sura Sans, radios incoherentes entre
      variantes (5px Primario/CTA vs 50px Secundario). Pedir un CSS curado.
