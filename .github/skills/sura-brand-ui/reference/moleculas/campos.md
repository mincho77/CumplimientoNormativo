# Campos de texto (Text fields / Inputs) — molécula

Fuente: `Campos.pdf` (1 página larga). Verificado contra imágenes renderizadas y
muestreo de píxeles. **Tipografía: Sura Sans. No aparece Barlow.**

> ⚠ **Nota de color (aplica «confía en la muestra renderizada»):** el valor de
> relleno digitado se rotula "Azul PROFUNDO `#26328C`", pero la **muestra
> renderizada real** es `#0033A0` (muestreo `(0,51,160)`). Usa **`#0033A0`** — es
> el mismo precedente de Migas de pan. El `#26328C` impreso es un export poco
> fiable.

## 1. Qué es

Los campos de texto se utilizan cuando el usuario necesita ingresar texto en una
interfaz (p. ej. completar información de contacto o de pago en un formulario).

## 2. Anatomía

1. **Etiqueta.**
2. **Ícono** (opcional, izquierda / derecha / ambos lados).
3. **Texto de ayuda** (descripción, opcional).
4. **Contenedor** (trazo + relleno).
5. **Texto de relleno** (el valor digitado).

## 3. Construcción (medidas)

### Tamaños base
| Tamaño | Altura | Ancho mín. | Redondeo | Texto |
|---|---|---|---|---|
| **Grande** | 56 px | 240 px | 12 px | 16 px (1 rem) |
| **Mediano** | 48 px | 240 px | 12 px | 16 px (1 rem) |

- Ancho **flexible** en móvil: ocupa el ancho completo del dispositivo.
- **Etiqueta** y **texto de ayuda**: 14 px Regular, alineados a la izquierda, una
  sola línea (no se ondulan, totalmente visibles).
- **Espaciado entre campos de texto: 24 px** (contando todos los elementos del
  campo). Aunque se oculte el texto de ayuda, este valor **no cambia**.

### Trazo y relleno
El contenedor tiene relleno y un trazo alrededor. El **color y grosor del trazo
cambian** para indicar cuándo el campo está activo.

### 3.bis Mobile / Responsivo

Fuente: *Campos - mobile.pdf*. Los tamaños base (48/56 px), redondeo 12 px, valor
16 px, etiqueta/ayuda 14 px y la separación de 24 px entre campos son **iguales** a
la versión web — **no se repiten**. Deltas móviles reales:

- **En la App se usa siempre el tamaño _Mediano_ (48 px)** del componente — el
  Grande (56 px) queda para escritorio. (Texto literal de la lámina: «Para su
  aplicación en la App, se debe hacer uso del tamaño mediano del componente».)
- **Ancho flexible = ancho completo del dispositivo** (ya documentado arriba); el
  ancho estándar mínimo sigue siendo 240 px.
- **Paddings internos (resuelven el pendiente §10)** medidos en la lámina móvil:
  - Padding superior del bloque (antes de la etiqueta): **8 px**.
  - Etiqueta ↔ contenedor del campo: **4 px**.
  - Padding **vertical interno** del contenedor (texto de relleno): **12 px**.
  - Margen lateral interno del campo: **12 px**.
  - Campo ↔ texto de ayuda / condición: **4 px**.

#### Selector de fecha (móvil)
| Elemento | Medida |
|---|---|
| Ancho del campo de fecha | **280 px** |
| Alto del campo (etiqueta + campo + condición) | **88 px** |
| Calendario desplegado | **280 × 506 px** |
| Margen lateral del calendario | **16 px** |
| Separación entre celdas de día | **4 px** |
| Variante **con botones** (pie «Seleccionar fecha») | ancho **360 px**, separación al pie **24 px** |

> El calendario móvil mantiene la cabecera `Mes Año` con chevrons y la grilla
> `Do Lu Ma Mi Ju Vi Sa`; el día seleccionado se resalta. Formato de campo
> `12/01/2023` con `×` para limpiar (igual que web).

## 4. Estados del campo

| Estado | Trazo / contenido |
|---|---|
| **Inactivo** | borde gris, placeholder gris |
| **Activo** | borde azul vivo `#2D6DF6`; valor en `#0033A0` |
| **Sobre (hover)** | borde azul |
| **Enfocado (focus)** | borde azul + anillo de foco |
| **Activo y sobre** | borde azul |
| **Deshabilitado** | gris atenuado, fondo gris muy claro |
| **Error** | borde, texto e ícono en rojo `#D12D35` |

Cada estado se documenta en 4 variantes de ícono: **sin ícono**, **ícono
derecho**, **ícono izquierdo**, **ícono ambos lados**, y con / sin etiqueta.

## 5. Colores

| Rol | Nombre | Hex |
|---|---|---|
| Etiqueta, ayuda e íconos (activo/foco) | Azul Vivo SURA | `#2D6DF6` (muestreo `(45,109,246)`) |
| Etiqueta, ayuda e íconos de **alerta** | Error 1 | `#D12D35` (muestreo `(209,45,52)`) |
| Texto / valor de **relleno** | Azul Profundo | **`#0033A0`** (impreso `#26328C`; render real `(0,51,160)`) |

## 6. Variantes del campo

### Campo con despliegue (select / dropdown)
- Permite elegir de una **lista** en un espacio limitado.
- Se sugiere usarlo a partir de **3 o más** elementos.
- Ítems de la lista: texto **16 px** (1 rem), una sola línea; ícono **opcional**.
- Estados: Inactivo, Sobre, Activo, Activo y sobre, Enfocado, **Desplegado**
  (lista de elementos), Error con etiqueta, Deshabilitado.
- **Correcto:** etiqueta brer que cabe completa. **Incorrecto:** etiqueta larga
  que se trunca con `…`.

> ⚠ **El `<select>` nativo NO es estilizable de marca al desplegarse.** El campo
> cerrado sí se puede maquetar (altura, borde, chevron), pero **la lista de
> opciones que pinta el navegador al hacer clic la dibuja el sistema operativo**
> (tipografía del SO, resaltado azul del SO, esquinas y sombra del SO) y **no
> respeta** los tokens de marca. Por eso el desplegado del `<select>` siempre se
> ve "fuera de marca", sin importar el CSS que se aplique al `<select>`.
>
> **Solución de marca — desplegable propio basado en la molécula Menú.** Sustituye
> el `<select>` nativo por un patrón compuesto que SÍ se controla por completo:
> 1. **Disparador** = un `<button>` con la apariencia del campo (`.field.select`):
>    ícono opcional + valor/placeholder + chevron triangular `avant-abajo` a la
>    derecha. Lleva `aria-haspopup="listbox"` y `aria-expanded`.
> 2. **Lista** = un `<ul role="listbox">` con la anatomía de **Menú**
>    (`reference/moleculas/menu.md`): ítems de 44–48 px, radio del contenedor
>    12 px, opción activa en **azul suave** (`--fondo`/sel-bg), elevación de
>    dropdown, apertura/cierre **animados**, variante de **modo oscuro**. Cada
>    opción es un `<li role="option">` con `data-value` y `aria-selected`.
> 3. **Valor real** = un `<input type="hidden">` que conserva el valor para la
>    lógica/formulario; al elegir una opción se actualiza y dispara un evento
>    `change` (burbujeante) para no romper los manejadores existentes.
> 4. **Cierre** por clic afuera y tecla **Esc**; foco gestionado.
>
> Así el componente cerrado y **el desplegado** quedan ambos en marca, accesibles
> y animados. Mantén las medidas base del campo (altura 48/56, redondeo 12 px,
> valor `#0033A0`, borde de foco `#2D6DF6`).

### Área de texto (textarea)
- Para entradas de **2 a 4 líneas**. Etiqueta y descripción no se ondulan y ocupan
  una sola línea. Estados: inactiva, activa, activo y sobre, enfocado, sobre, error.

### Campo OTP (contraseña de un solo uso)
- Mecanismo de inicio de sesión / validación de identidad (doble factor).
- Casillas de **dígito individual**; estados Reposo, Activo (1.º campo), Mitad
  relleno, Relleno completo, Error. Enlace **"Reenviar código"**.
- Etiqueta 14 px Regular, izquierda; texto de ayuda 14 px Regular, una línea.

### Selector de fecha (date picker)
- Permite seleccionar una fecha o un **rango** desde un calendario. Configurable
  con formato, validación y predeterminados.
- Formato de campo: `12/01/2023`; ícono de calendario; `×` para limpiar.
- Estados: Inactivo, Abierto (calendario), Seleccionado, Completado, Error.
- Variantes: **Selección de fecha**, **rango de fecha**, **selección de mes**,
  **rango de mes**, **selección de año**. Día/mes/año seleccionado resaltado.

## 7. Contenedor / accesibilidad

- Los contenedores mejoran la **visibilidad** de los campos: debe existir
  contraste suficiente entre el área del relleno y el fondo.

## 8. Tokens CSS

```css
:root {
  /* Tamaños */
  --field-h-lg: 56px;
  --field-h-md: 48px;
  --field-min-w: 240px;
  --field-radius: 12px;
  --field-text-size: 16px;          /* 1 rem (valor) */
  --field-label-size: 14px;         /* etiqueta y ayuda, regular */
  --field-gap: 24px;                /* entre campos */

  /* Despliegue */
  --field-option-size: 16px;        /* ítem de lista */

  /* Colores */
  --field-active: #2D6DF6;          /* Azul Vivo SURA — etiqueta/ayuda/íconos activos */
  --field-value: #0033A0;           /* valor de relleno (impreso #26328C) */
  --field-error: #D12D35;           /* estado de alerta */

  --font-field: 'Sura Sans', 'Helvetica Neue', Arial, sans-serif;
}
```

## 9. Reglas operativas para el skill

- Dos alturas base: Grande 56 px / Mediano 48 px; ancho mín 240 px; redondeo
  12 px; valor 16 px; etiqueta y ayuda 14 px Regular alineadas a la izquierda.
- **Separación entre campos: 24 px**, invariable aunque se oculte la ayuda.
- Activo/foco → borde e íconos `#2D6DF6`; valor digitado `#0033A0`; error
  (borde+texto+ícono) `#D12D35`. Inactivo/deshabilitado en gris.
- Select solo a partir de 3 opciones; ítems 16 px, una línea, ícono opcional;
  truncar etiquetas largas con `…` (no romper el contenedor).
- **El select hereda las medidas base del campo, no las inventa:** altura Mediano
  48 / Grande 56 px y **ancho mín 240 px** (no campos cortos/bajos tipo 38×150);
  redondeo 12 px; placeholder/etiqueta gris, valor `#0033A0`. El chevron de
  despliegue es un glifo (sin caja de relleno) y no altera la altura del campo.
  En activo/foco el **borde** pasa a `#2D6DF6` (más anillo de foco), no el fondo.
- **Excepción de ancho en barra de filtros densa:** el ancho mín **240 px** es
  regla de **campo de formulario** (un campo por fila o pocos campos anchos). En
  una **barra de filtros densa** (varios selects en una sola fila de toolbar —
  p. ej. la cabecera de una tabla con Carril/Etapa/Subetapa) el ancho **puede
  ceder por debajo de 240 px** para que todos quepan sin desbordar el contenedor.
  Lo que **no** cede: altura base (48/56), redondeo 12 px, valor `#0033A0`, borde
  de foco `#2D6DF6` y el chevron triangular. Es un compromiso válido, no una
  desviación: al auditar, no marques como error un select de filtro angosto si
  conserva lo demás. La altura sí es obligatoria (no bajar a 38).
- **El chevron oficial del select es el glifo TRIANGULAR** (▾, ícono de catálogo
  `avant-abajo`), **no** la flecha lineal (`flecha-abajo-linea`). Va a la derecha,
  como glifo sin caja de relleno, sin alterar la altura del campo.
- **Prohibido el `<select>` nativo para listas de marca (generar y auditar).** El
  navegador dibuja la **lista de opciones desplegada** con estilo del sistema
  operativo, imposible de alinear a la marca. Sustitúyelo **siempre** por el
  desplegable propio (disparador `<button>` + `<ul role="listbox">` con anatomía
  de **Menú** + `<input type="hidden">` que dispara `change`), con opción activa
  en azul suave, elevación, apertura/cierre animados, modo oscuro, cierre por clic
  afuera/Esc y `aria-haspopup`/`aria-expanded`/`role="option"`. En GENERAR no
  emitas `<select>` para listas de marca; en AUDITAR cada `<select>` nativo (cuyo
  desplegado se ve con estilo del SO) es una **desviación a corregir**,
  conservando la lógica (mismo `value`, mismo evento `change`). Detalle y
  anatomía en §6 «Campo con despliegue».
- Textarea para 2–4 líneas; OTP en casillas de dígito con "Reenviar código";
  date picker formato `12/01/2023` con calendario (fecha/rango/mes/año).
- Tipografía Sura Sans; **nunca Barlow**.

## 10. Pendiente

- [ ] Confirmar el gris exacto del borde por defecto, placeholder y estado
      deshabilitado (no impreso en hex; muestrear si se requiere fidelidad alta).
- [ ] Confirmar grosor del trazo en cada estado (px no impreso) y el color/relleno
      del día/mes/año seleccionado en el calendario (azul claro de selección).
- [ ] Confirmar medidas internas (padding horizontal/vertical) del campo base y de
      las casillas OTP (parcialmente recortadas en la lámina).
