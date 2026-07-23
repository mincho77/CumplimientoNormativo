# Casilla de verificación (Checkbox) — átomo

Fuente: `Casilla de verificación.pdf` (1 lámina). Verificado contra imágenes
renderizadas y muestreo de píxeles. **Tipografía: Sura Sans. No aparece Barlow.**

## 1. Qué es

Permite seleccionar **una o más** opciones de un conjunto (a diferencia del
radio, que es selección única). Cada casilla es independiente: activarla no
desactiva las demás. Soporta un estado **Indeterminado** para relaciones
padre-hijo. Útil para listas con subselecciones y para activar/desactivar un
elemento (ej. términos y condiciones).

## 2. Anatomía

1. **Casilla de verificación** seleccionada (caja con check relleno).
2. **Texto de la etiqueta** cercano.
3. **Casilla de verificación** no seleccionada (caja vacía).

## 3. Construcción (medidas)

Dos tamaños: **M** (por defecto) y **S**.

| Elemento | Tamaño M | Tamaño S |
|---|---|---|
| **Caja visible** | 24 × 24 px | 20 × 20 px |
| **Área segura / táctil** | 48 × 48 px | 24 × 24 px |
| **Margen de área segura** | 12 px por lado | 2 px por lado |
| **Altura mínima** | 40 px | 24 px |
| **Check interno** (palomita) | 12 px | 12 px |
| **Ancho mínimo** | depende del contenedor | depende del contenedor |

> El área segura añade espacio táctil alrededor de la caja para mejor toque en
> móvil. En M el margen es **12 px por lado** (24 + 12·2 = 48); en S es **2 px
> por lado** (20 + 2·2 = 24).
> ⚠ Tensión menor del manual: en M la "altura mínima" se rotula 40 px aunque el
> área segura mide 48 px. Tomamos **48 px como área táctil** y 40 px como alto
> mínimo de fila para layout.

### Con etiqueta

| Espaciado | Valor |
|---|---|
| **Caja ↔ etiqueta** | 12 px |
| **Espaciado horizontal mínimo** | 8 px |
| **Espaciado vertical** | 8 px |
| **Tamaño de texto de la etiqueta** | 16 px (= 1 rem), Sura Sans regular |

### Forma de la caja

Esquinas **suavemente redondeadas** (no es círculo como el radio). El radio es
pequeño; usa `--radius-sm` (8 px) o el inmediatamente inferior según el tamaño
de caja (ver `generales/borde-redondeado.md`).

### 3.bis Palomita por CSS: escala con el tamaño de la caja (no la fijes)

Cuando la palomita se dibuja por CSS (`appearance:none` + `::after` rotado 45°),
**sus medidas (posición, ancho y alto) deben escalar con el lado de la caja.**
Reutilizar una palomita calibrada para una caja grande en una caja más pequeña
hace que el check **se desborde por arriba y pise las esquinas redondeadas** — se
ve "roto" (incidente real con un chip de casilla de 16 px que heredó la palomita
de la matriz de 20 px).

- Define la palomita por **proporción del lado `L`**, no copiando valores
  absolutos de otro tamaño. Regla práctica verificada (caja con borde 2 px):
  `left ≈ 0.30·L`, `top ≈ 0.10·L`, `width ≈ 0.25·L`, `height ≈ 0.50·L`,
  `border-width: 0 2px 2px 0`, `transform: rotate(45deg)`.
- Al reducir la caja **recalcula esos cuatro valores**; no basta con cambiar el
  `width/height` de la caja. Si solo achicas la caja, la palomita queda grande y
  rompe el redondeo.
- Verifica que la palomita quede **dentro** del borde redondeado en el tamaño más
  pequeño que vayas a usar.

## 4. Estados

Cada estado existe en **Tamaño S / M**, **Desactivado (vacío) / Activado
(marcado)** y **Sin etiqueta / Con etiqueta**.

| Estado | Activado (relleno) | Desactivado (vacío) |
|---|---|---|
| **Por defecto** | caja `#2D6DF6` (Azul SURA) + check blanco `#FFFFFF` | caja vacía con borde |
| **Sobre** (hover) | `#2D6DF6` | caja con **relleno azul claro** `~#80B1FF` |
| **Enfocado** | `#2D6DF6` + halo de foco `#80B1FF` | borde de foco más marcado |
| **Presionado** | `#0033A0` (Azul Profundo) | caja con relleno azul claro |
| **Inactivo** (deshabilitado) | atenuado gris `~#B3B3B5`, check gris | caja gris muy tenue |
| **Indeterminado** | caja `#2D6DF6` con **guion horizontal** (–) blanco en lugar de palomita | guion atenuado |

> El **Indeterminado** se usa en relaciones padre-hijo (ver §5): cuando algunas
> —pero no todas— las casillas hijas están marcadas, el padre muestra el guion.
> La palomita es blanca sobre el azul; en Inactivo todo se atenúa a gris.

## 5. Relación padre-hijo

- Casilla **padre marcada** → todas las hijas se marcan.
- Casilla **padre no marcada** → todas las hijas se desmarcan.
- **Algunas** hijas marcadas (no todas) → el padre pasa a **Indeterminado**.

## 6. Comportamiento y uso

- Al seleccionar, comunica clara e instantáneamente el estado elegido.
- Se pueden seleccionar **varias** casillas en una lista.

**Úsalo cuando:**
- Selecciones más de una opción de una lista.
- La lista contenga subselecciones (padre-hijo).
- Actives/desactives un elemento en entorno de escritorio.

**Recomendaciones de etiqueta:**
- Mantener etiquetas **breves y descriptivas**.
- Empezar todas con **mayúscula inicial**.
- **No** incluir puntuación al final de la etiqueta.

## 7. Cuándo usar otro control (selección alternativa)

| Control | Para qué |
|---|---|
| **Casilla de verificación** | Selección **múltiple** o activar/desactivar un ítem |
| **Interruptor** | Encender/apagar un ajuste con efecto **inmediato** (ver `interruptores.md`) |
| **Botón de radio** | Selección **única** de un conjunto (ver `radio.md`) |

## 8. Contextos de uso (de la lámina)

- **Listas multi-selección** (ej. Programas de bienestar: Nutrición, Bienestar
  en el lugar de trabajo, Ejercicio físico) — permite elegir más de una opción.
- **Términos y condiciones**: casilla previa al botón **Enviar** en un
  formulario de cotización, para aceptar la política de privacidad.

## 9. Tokens para implementación

```css
:root {
  /* Tamaños */
  --checkbox-box-m: 24px;            /* caja visible, tamaño M (default) */
  --checkbox-box-s: 20px;            /* caja visible, tamaño S */
  --checkbox-touch-m: 48px;          /* área táctil M */
  --checkbox-touch-s: 24px;          /* área táctil S */
  --checkbox-safe-margin-m: 12px;    /* margen área segura M */
  --checkbox-safe-margin-s: 2px;     /* margen área segura S */
  --checkbox-min-height-m: 40px;
  --checkbox-min-height-s: 24px;
  --checkbox-check-inner: 12px;      /* palomita / guion interno */
  --checkbox-radius: 8px;            /* esquinas suaves (radius-sm) */

  /* Con etiqueta */
  --checkbox-gap-label: 12px;        /* caja ↔ etiqueta */
  --checkbox-spacing-h: 8px;
  --checkbox-spacing-v: 8px;
  --checkbox-label-size: 16px;       /* 1rem, Sura Sans regular */

  /* Colores */
  --checkbox-color-active: #2D6DF6;  /* Azul SURA — marcado */
  --checkbox-color-pressed: #0033A0; /* Azul Profundo — presionado */
  --checkbox-focus-ring: #80B1FF;    /* halo de enfoque */
  --checkbox-hover-fill: #80B1FF;    /* relleno azul claro en hover (caja vacía) */
  --checkbox-check-color: #FFFFFF;   /* palomita / guion */
  --checkbox-color-disabled: #B3B3B5;/* inactivo atenuado */
}
```

### Palomita por CSS proporcional (cajas de 20 / 16 px)

```css
/* Caja base 20px — palomita proporcional (left/top/width/height ≈ 0.30/0.10/0.25/0.50·L) */
.check{appearance:none;width:20px;height:20px;border:2px solid var(--field-stroke);
  border-radius:6px;position:relative;cursor:pointer}
.check:checked{background:var(--checkbox-color-active);border-color:var(--checkbox-color-active)}
.check:checked::after{content:"";position:absolute;left:6px;top:2px;width:5px;height:10px;
  border:solid var(--checkbox-check-color);border-width:0 2px 2px 0;transform:rotate(45deg)}

/* Variante pequeña 16px — palomita RE-ESCALADA (×0.8), nunca la de 20px */
.check.sm{width:16px;height:16px;border-radius:5px}
.check.sm:checked::after{left:5px;top:2px;width:4px;height:8px}
```

## 10. Reglas operativas para el skill

1. Por defecto usa **Tamaño M** (caja 24 px, área táctil 48 px). Usa S solo en
   listas densas de escritorio.
2. Marcado = relleno `#2D6DF6` + palomita blanca. Nunca uses otro color de
   relleno (cada control oscurece hacia su propio tono; el azul → `#0033A0` al
   presionar).
3. Para grupos jerárquicos implementa el estado **Indeterminado** en el padre.
4. Etiqueta siempre a la derecha de la caja, separada **12 px**, con mayúscula
   inicial y sin puntuación final.
5. No mezcles casillas y radios en el mismo grupo (radio = selección única).
6. No uses casilla para acciones de efecto inmediato tipo on/off de un ajuste:
   ahí va el **interruptor**.
7. **Palomita por CSS:** escálala con la caja. Si reduces el lado `L`, recalcula
   `left/top/width/height` del `::after` de forma proporcional (≈ 0.30/0.10/0.25/
   0.50·L); **no reutilices la palomita de un tamaño mayor** porque se desborda y
   rompe el redondeo. Ver §3.bis y la receta CSS de §9.

## 11. Pendiente

- [ ] Confirmar hex exacto del **borde de la casilla vacía** (muestreo dio un
      azul-gris desaturado `~#8593C9`, posible antialiasing del trazo).
- [ ] Confirmar el **radio de esquina** exacto de la caja (se ve ~6 px; se
      propone `--radius-sm` 8 px o inmediatamente inferior).
- [ ] Confirmar gris exacto de **Inactivo** (`~#B3B3B5`); verificar si es un
      token de la escala de grises del manual o una atenuación por opacidad.
