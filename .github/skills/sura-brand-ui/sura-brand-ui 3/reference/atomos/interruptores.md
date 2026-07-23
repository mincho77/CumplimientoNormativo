# Interruptor / Switch — átomo

Fuente: `Interruptores.pdf` (3 láminas). Verificado contra imágenes renderizadas
y muestreo de la lámina de Colores. **Tipografía: Sura Sans. No aparece Barlow.**

## 1. Qué es

Alterna entre **dos estados** (encendido/apagado) con efecto inmediato. Para
configuraciones tipo activar/desactivar opciones. Siempre emparejado con una
**etiqueta en línea** que describe la opción y su estado.

## 2. Anatomía

1. **Pista** (track).
2. **Pulgar** (thumb).
3. **Texto de etiqueta**.

## 3. Construcción (medidas)

| Elemento | Medida |
|---|---|
| **Pista** (track) | 40 × 24 px, forma píldora (radio 12) |
| **Pulgar** (thumb) | 16 px (círculo) |
| **Caja táctil del switch** (con padding) | 46 × 32 px |
| Padding del switch | 3 px horizontal · 4 px vertical |
| Desplazamiento del pulgar (off→on) | ~20 px |
| **Contenedor de la fila** (con etiqueta) | alto 44–48 px |
| Padding del contenedor | 8 px horizontal · 8 px vertical |
| Gap etiqueta ↔ switch | 16 px |
| Tamaño de texto de etiqueta | 16 px, **Regular** |
| Ancho en móvil | ocupa el total (390 px) |

> ⚠ **Inconsistencia de etiquetas en el PDF:** el texto de la lámina dice
> "Ancho de pulgar 40 px / Ancho de pista 20 px", lo cual es físicamente
> imposible (el pulgar no puede ser más ancho que la pista). La geometría real
> de los diagramas es **pista 40 px / pulgar 16 px**; el "20 px" corresponde al
> desplazamiento del pulgar. Se documenta la geometría correcta, no las
> etiquetas cruzadas.

## 4. Estados (lámina "Estados": Apagado / Encendido)

Columnas: **Activo · Sobre · Enfocado · Presionado · Inactivo**.

| Estado | Pista ENCENDIDO | Notas |
|---|---|---|
| **Activo** | `#2D6DF6` (Azul Vivo) | estado por defecto encendido |
| **Sobre** (hover) | `#0033A0` (azul oscuro) | |
| **Enfocado** | `#2D6DF6` + halo de foco `#DFEAFF` | anillo/relleno de foco |
| **Presionado** | `#0033A0` | azul oscuro al pulsar |
| **Inactivo** (deshabilitado) | `#888B8D` (gris) / atenuado | sin interacción |

**Apagado (off):** pista `#E5E9EA` (Background 1), borde `#B4B4B5` (Pantone
429 C), pulgar blanco/gris. Inactivo apagado = todo en grises atenuados.

## 5. Paleta oficial del componente (lámina "Colores")

| Nombre en el PDF | Hex | Uso |
|---|---|---|
| **AZUL SURA** | `#0033A0` | pista on en hover/presionado |
| **AZUL VIVO** | `#2D6DF6` | pista on activo/enfocado |
| **BACKGROUND 4** | `#DFEAFF` | halo de enfoque / azul claro |
| **GRIS** | `#888B8D` | pulgar off / inactivo |
| **PANTONE 429 C** | `#B4B4B5` | borde de pista off |
| **BACKGROUND 1** | `#E5E9EA` | relleno de pista off |

> ⚠⚠ **Contradicción de nomenclatura entre documentos del manual:** este PDF
> llama **"AZUL SURA" a `#0033A0`** y **"AZUL VIVO" a `#2D6DF6`**. En `Botones.pdf`
> es al revés: `#2D6DF6` se llama "Azul SURA" y `#0033A0` "Azul Profundo".
> **Los hex son los que mandan**, no los nombres. Ver `colores.md` para la
> nomenclatura canónica adoptada por el skill. (Mismo patrón de descuido que
> Barlow vs Sura Sans.)

## 6. Etiqueta y colocación

- La etiqueta **siempre** acompaña al switch, a la **izquierda** por defecto
  (también admite a la derecha).
- Apilar interruptores verticalmente en listas de configuración.
- Máximo **2 líneas** de texto por opción; la 2ª línea es texto de apoyo en
  **color secundario** para diferenciarla del nombre de la opción.
- Nunca se activa automáticamente; requiere acción del usuario.

## 7. Tokens para implementación

```css
:root {
  --switch-track-w: 40px;
  --switch-track-h: 24px;
  --switch-thumb: 16px;
  --switch-pad-h: 3px;
  --switch-pad-v: 4px;
  --switch-row-h: 48px;
  --switch-gap-label: 16px;
  --switch-label-size: 16px;        /* Sura Sans regular */

  --switch-on: #2D6DF6;             /* Azul Vivo (activo) */
  --switch-on-hover: #0033A0;       /* hover/presionado */
  --switch-focus-ring: #DFEAFF;     /* Background 4 */
  --switch-off-track: #E5E9EA;      /* Background 1 */
  --switch-off-border: #B4B4B5;     /* Pantone 429 C */
  --switch-disabled: #888B8D;       /* Gris */

  /* Animación (obligatoria, ver auditoria.md §4.1) */
  --switch-thumb-move: left 0.24s cubic-bezier(0.34, 1.4, 0.64, 1); /* deslizamiento con leve rebote al asentar */
  --switch-track-anim: background 0.18s, border-color 0.18s;        /* cambio on↔off / hover */
}
```

> El pulgar **debe deslizarse animado** entre off y on (no saltar). Usa
> `transition: var(--switch-thumb-move)` en el pulgar y `var(--switch-track-anim)`
> en la pista. Contempla `@media (prefers-reduced-motion: reduce)` para anular el
> movimiento. La animación es parte de la anatomía del switch, no un adorno
> (ver `auditoria.md` §4.1).

## 8. Reglas operativas para el skill

- Switch = alternar **dos estados** (on/off) con efecto inmediato; **siempre**
  con etiqueta en línea. No lo uses para elegir entre opciones de un conjunto
  (eso es radio) ni para acciones que requieran confirmar.
- Geometría real: pista 40×24 (píldora radio 12), pulgar 16, desplazamiento ~20,
  fila 44–48 px, gap etiqueta↔switch 16, etiqueta 16 px regular. **Ignora las
  etiquetas cruzadas del PDF** (pulgar 40 / pista 20 es imposible).
- On: `#2D6DF6` activo, `#0033A0` hover/presionado, halo foco `#DFEAFF`.
  Off: pista `#E5E9EA`, borde `#B4B4B5`, pulgar blanco/gris. Inactivo `#888B8D`.
- **El hex manda, no el nombre:** este PDF invierte "Azul SURA"/"Azul Vivo"
  respecto a Botones. Usa la nomenclatura canónica de `colores.md`.
- Etiqueta a la izquierda por defecto; máx 2 líneas (la 2ª en color secundario).
  Apilar verticalmente en listas de configuración. Nunca se activa solo.
- **El pulgar se desliza animado** (off→on / on→off): `transition: left 0.24s
  cubic-bezier(0.34, 1.4, 0.64, 1)` + transición de `background`/`border-color` en
  la pista; con `prefers-reduced-motion: reduce`. Un switch que salta de estado sin
  animar es una desviación (ver `auditoria.md` §4.1).
- **Robustez del estado (lección fija):** el switch refleja **el estado real** desde
  una única fuente de verdad (p. ej. `data-theme` en `<html>`). Separa el render
  visual del switch de cualquier **efecto secundario de persistencia**: si guardas la
  preferencia (`localStorage.setItem`, cookie, fetch), **aíslalo en `try/catch`** y
  ejecútalo **después** de fijar el estado, de modo que la sincronización visual
  (`aria-checked`, posición del pulgar, etiqueta/ícono) **siempre** corra aunque la
  persistencia falle (file://, modo privado, almacenamiento bloqueado). Un switch que
  queda desincronizado del tema cuando `setItem` lanza es un bug, no un caso límite.
- Tipografía Sura Sans; **nunca Barlow**.

## 9. Pendiente

- [ ] Confirmar alto del contenedor (lámina muestra 44 px; el texto dice 48 px).
- [ ] Confirmar el color del pulgar en on (¿siempre blanco?).
