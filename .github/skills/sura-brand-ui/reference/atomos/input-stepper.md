# Input stepper (Paso a paso numérico) — átomo

Fuente: `Input stepper.pdf` (1 lámina). Verificado contra imágenes renderizadas
y muestreo de píxeles. **Tipografía: Sura Sans. No aparece Barlow.**

## 1. Qué es

Componente que se utiliza para **aumentar o disminuir un valor**, permitiéndole
al usuario cambiar el número de ítems. Se recomienda usarlo cuando se necesiten
ajustar **valores pequeños** que se aumentan o disminuyen en **pasos pequeños**.

## 2. Anatomía

1. **Etiqueta** (Opcional) — encabezado del control.
2. **Botón izquierdo** — decrementa el valor (signo menos).
3. **Campo de texto** — muestra el valor; editable manualmente.
4. **Botón derecho** — incrementa el valor (signo más).
5. **Texto de ayuda** (Opcional) — apoyo bajo el control, en una sola línea.

## 3. Construcción (medidas)

| Elemento | Medida |
|---|---|
| **Botones +/−** (círculo) | 40 × 40 px |
| **Espaciado horizontal mínimo** | 8 px |
| **Espaciado vertical** | 4 px |
| **Espaciado entre elementos** (botón ↔ campo) | 16 px |
| **Margen exterior** (área segura, extremos) | 24 px |
| **Espaciado vertical** etiqueta / texto de ayuda | 8 px |
| **Tamaño de texto** | 16 px (= 1 rem) |

> Los botones son **círculos** de 40 px. El campo de texto es un rectángulo con
> borde azul; el valor va **centrado**. En la variante con etiqueta y texto de
> ayuda, la etiqueta se sitúa arriba y el texto de ayuda abajo, separados 8 px.

## 4. Colores

| Parte | Color | Hex |
|---|---|---|
| **Botones +/−** (relleno, activo) | Azul Profundo | `#0033A0` |
| **Iconos +/−** | Blanco Puro | `#FFFFFF` |
| **Borde del campo de texto** | Azul Profundo | `#0033A0` |
| **Botón deshabilitado** (relleno) | Gris inactivo | `#B3B3B5` |
| **Icono de botón deshabilitado** | Blanco Puro | `#FFFFFF` |
| **Valor / texto** | Gris 500 | `#3F3F41` |

> ⚠ **Nota:** los botones del stepper usan **Azul Profundo `#0033A0`** como
> relleno por defecto (no Azul Cielo Latino). El borde del campo también es
> `#0033A0`. Confirmado por muestreo de píxeles `(0,51,160)`.

## 5. Estados de los botones

| Estado | Relleno | Icono |
|---|---|---|
| **Activo** | Azul Profundo `#0033A0` | Blanco `#FFFFFF` |
| **Deshabilitado** | Gris `#B3B3B5` | Blanco `#FFFFFF` |

- **Botón menos deshabilitado** cuando se alcanza el **valor mínimo**.
- **Botón más deshabilitado** cuando se alcanza el **valor máximo**.

## 6. Comportamiento

- El **botón derecho** aumenta el valor; el **botón izquierdo** lo disminuye.
- Con el **campo de texto** se puede añadir la cifra **manualmente**.
- El botón menos se desactiva al llegar al **mínimo**; el botón más se desactiva
  al llegar al **máximo**.

## 7. Uso

**Úsalo cuando:**
- El incremento o decremento sea una **cifra pequeña**.
- Se ajusten valores pequeños en pasos pequeños.

**Recomendaciones:**
- Por defecto, **debe existir un valor predeterminado** que la mayoría de los
  usuarios probablemente seleccionen.
- Etiquetas **breves y descriptivas**, con **mayúscula inicial** y sin
  puntuación final.
- El **texto de ayuda** va en una sola línea y es opcional.
- Ajusta el espaciado para garantizar un **área táctil** cómoda; no coloques los
  inputs demasiado juntos.
- Establece **valores seleccionables** definidos (rango y paso).

**No lo uses cuando:**
- El **rango de selección sea amplio** (ej. saltar hasta 48) — usa otro control.
- Se requieran **decimales** (ej. `3.6` es incorrecto).
- Dejarías el **campo en blanco** — siempre debe haber un valor.

**Correcto:** valor predeterminado (`2`), pasos pequeños, área táctil holgada.
**Incorrecto:** valor alto/rango amplio (`48`), decimales (`3.6`), campo vacío.

## 8. Tokens para implementación

```css
:root {
  /* Tamaños */
  --stepper-button-size: 40px;        /* botón +/− circular */
  --stepper-gap-min: 8px;             /* espaciado horizontal mínimo */
  --stepper-gap-vertical: 4px;        /* espaciado vertical */
  --stepper-gap-elements: 16px;       /* botón ↔ campo */
  --stepper-safe-margin: 24px;        /* margen exterior área segura */
  --stepper-gap-label: 8px;           /* etiqueta / texto de ayuda */
  --stepper-text-size: 16px;          /* 1rem */

  /* Colores */
  --stepper-button-fill: #0033A0;     /* Azul Profundo (activo) */
  --stepper-button-icon: #FFFFFF;     /* iconos +/− */
  --stepper-field-border: #0033A0;    /* borde del campo de texto */
  --stepper-button-disabled: #B3B3B5; /* gris inactivo */
  --stepper-value-color: #3F3F41;     /* Gris 500 (valor) */

  /* Forma */
  --stepper-button-radius: 9999px;    /* botón = círculo (altura/2) */
}
```

## 9. Reglas operativas para el skill

1. Botones +/− = **círculos de 40 px**, relleno `#0033A0`, icono blanco. En
   deshabilitado, relleno `#B3B3B5` con icono blanco.
2. Campo de texto rectangular con **borde `#0033A0`**, valor centrado, texto
   16 px Sura Sans, color `#3F3F41`.
3. Separa botón y campo **16 px**; margen exterior **24 px**; nunca comprimas
   por debajo de **8 px** horizontal (área táctil).
4. Deshabilita el botón menos en el **mínimo** y el botón más en el **máximo**.
5. Siempre arranca con un **valor predeterminado** — no dejes el campo vacío.
6. **No** uses el stepper para rangos amplios ni valores con **decimales**;
   para rangos amplios usa selector/input numérico, y para valor único en un
   continuo usa el `selector-rango.md`.
7. Etiqueta y texto de ayuda son **opcionales**: etiqueta con mayúscula inicial,
   sin puntuación; texto de ayuda en una sola línea, separados **8 px**.

## 10. Pendiente

- [ ] Confirmar el **paso (step) por defecto** y si el manual define mínimo y
      máximo recomendados.
- [ ] Confirmar el **radio exacto del campo de texto** (se ve rectangular con
      esquinas suaves; ¿`--radius-md` 12 px?).
- [ ] Confirmar estados **hover / focus / pressed** de los botones (la lámina
      solo documenta activo y deshabilitado).
