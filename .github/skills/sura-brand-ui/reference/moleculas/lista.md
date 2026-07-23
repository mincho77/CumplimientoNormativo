# Lista (List) — molécula

Fuente: `Lista.pdf` (varias láminas). Verificado contra imágenes renderizadas y
muestreo de píxeles. **Tipografía: Sura Sans. No aparece Barlow.**

## 1. Qué es

Las listas son disposiciones **verticales** que organizan y presentan información
de manera clara, mediante texto, íconos o componentes específicos.

Cada elemento o ítem de la lista se divide en **3 partes: A, B y C**. Cada lista
tiene un *núcleo* formado por una sección **A** y una sección **B**; la sección
**C** queda reservada para requisitos en distintas partes del producto.

## 2. Anatomía

### Sectores del ítem
- **A. Sector inicial** — soporta imagen, avatar, íconos y controles (casillas de
  verificación, radios, interruptores).
- **B. Sector contenido** — soporta contenido textual: título, subtítulo, bajada
  de texto, etiqueta.
- **C. Sector principio** — reservado para los **íconos de acción** (chevron `>`).

### Elementos
1. **Contenedor.**
2. **Avatar.**
3. **Título.**
4. **Ícono de acción.**

## 3. Construcción (medidas)

### Tamaño del ítem
| Versión | Altura del ítem | Ancho mínimo |
|---|---|---|
| **Escritorio** | **64 px** (fija) | 179 px |
| **Móvil** | **48 px** (fija) | 179 px |

- La altura fija permite incluir avatar e ícono en el sector A y **máximo 2 líneas
  de texto**.
- El ancho **máximo** depende de los ítems usados y del tamaño del contenedor.

### Espaciado del ítem
| Elemento | Medida |
|---|---|
| Espaciado vertical interno (top/bottom) | 8 px |
| Espaciado horizontal (borde) | 16 px |
| Espaciado entre elementos internos sector A ↔ sector B | 12 px |
| Espaciado entre controles del sector A | 8 px |
| Sector C | justificado a la derecha (16 px) |

## 4. Configuración del ítem

Usa distintas configuraciones de ítem según la necesidad:

- **Controles en sector A:** avatar + chevron, **radio**, **casilla de
  verificación**, **interruptor**.
- **Controles en sector C:** chevron de acción (`>`).

## 5. Contenedor de una lista

La construcción de una lista se forma de **tres partes**:
1. **Contenedor** — con márgenes superior e inferior de **16 px**.
2. **Cabecera** — componente base en tarjetas (título + bajada de texto + menú
   dango de 3 puntos).
3. **Ítems** — los elementos del listado descritos arriba.

| Versión | Ancho mínimo | Ancho máximo |
|---|---|---|
| **Móvil** | 220 px | 392 px |
| **Escritorio** | 288 px | 800 px |

## 5.bis Mobile / Responsivo — ítem increase/decrease

Fuente: *Lista - mobile.pdf*. La construcción base del ítem móvil (alto fijo 48 px,
ancho mín 179 px, contenedor 220–392 px) ya está documentada arriba — **no se
repite**. Lo nuevo de la lámina móvil es una **variante de ítem con stepper**:

### Ítem lista *increase / decrease*
Ítem con **kicker + título + texto descriptivo** en el sector B y un **input
stepper** (`− 0 +`, ver `atomos/input-stepper.md`) en el sector C. Sirve para
listas donde cada fila ajusta una cantidad (carrito, selección de coberturas,
unidades).

| Elemento | Medida |
|---|---|
| Altura **mínima** (solo kicker) | **98 px** |
| Altura con **kicker + dos líneas** activas | **118 px** |
| Ancho mínimo | **100 px** |
| Ancho máximo | el del contenedor |
| Espaciado vertical interno | 8 px |
| Espaciado horizontal | 16 px |
| Espaciado sector A ↔ sector B | **12 px** |
| Sector C (stepper) | justificado a la derecha |

> Diferencia clave con el ítem base: el *increase/decrease* es **más alto**
> (98–118 px vs 48 px) porque apila kicker, título y descripción, y reserva el
> sector C para el stepper en lugar del chevron. El resto de reglas (sectores A/B/C,
> tipografía, contenedor 220–392 px) son idénticas a la versión documentada arriba.

## 6. Estados y colores

- **Texto del elemento / título activo:** azul `#0033A0` (muestreo `(0,51,160)`).
- **Controles seleccionados** (casilla marcada, radio activo, interruptor on):
  relleno azul `#0033A0` (ver átomos `casilla-de-verificacion.md`,
  `boton-de-radio.md`, `interruptores.md`).
- **Ícono de acción:** chevron `>` a la derecha.

## 7. Uso

- En las listas es importante mantener **un** elemento en el sector A que apoye la
  acción requerida.
- **Evita incluir más de dos elementos en el mismo ítem** del sector A: tener dos o
  más controles juntos (p. ej. avatar + radio + casilla) genera mala experiencia y
  confunde al usuario (**incorrecto**).
- Ejemplos válidos: listado con avatar e ícono de acción, listado con casillas de
  verificación, listado con interruptores, listado con radios.

## 8. Tokens CSS

```css
:root {
  /* Ítem */
  --list-item-h-desktop: 64px;
  --list-item-h-mobile: 48px;
  --list-item-min-w: 179px;
  --list-item-pad-y: 8px;          /* vertical interno */
  --list-item-pad-x: 16px;         /* horizontal */
  --list-item-gap-ab: 12px;        /* sector A ↔ sector B */
  --list-item-gap-a: 8px;          /* entre controles del sector A */

  /* Contenedor */
  --list-container-margin-y: 16px;
  --list-container-min-w-mobile: 220px;
  --list-container-max-w-mobile: 392px;
  --list-container-min-w-desktop: 288px;
  --list-container-max-w-desktop: 800px;

  --list-active: #0033A0;          /* texto/título y controles activos */

  --font-list: 'Sura Sans', 'Helvetica Neue', Arial, sans-serif;
}
```

## 9. Reglas operativas para el skill

- Ítem en 3 sectores: **A** inicial (avatar/ícono/control), **B** contenido
  (texto), **C** acción (chevron a la derecha).
- Altura fija: escritorio 64 px / móvil 48 px; máx 2 líneas de texto; ancho ítem
  ≥179 px.
- Espaciado: vertical 8 px, horizontal 16 px, A↔B 12 px, sector C justificado
  derecha.
- Contenedor con márgenes 16 px; ancho móvil 220–392 px, escritorio 288–800 px.
- **Un solo control** por sector A; nunca apilar dos o más (mala práctica).
- Texto/controles activos en `#0033A0`; tipografía Sura Sans; nunca Barlow.

## 10. Pendiente

- [ ] Confirmar color del texto/ícono por defecto (no activo) y del subtítulo /
      bajada de texto (probable neutro `--gray-900`; no impreso en hex).
- [ ] Confirmar radio de borde del contenedor y de las tarjetas (usar
      `borde-redondeado.md` por defecto; la lámina no lo imprime en px).
