# Etiqueta (Tag) — molécula

Fuente: `Etiquetas.pdf` (1 lámina). Verificado contra imágenes renderizadas y
muestreo de píxeles. **Tipografía: Sura Sans. No aparece Barlow.**

## 1. Qué es

Las etiquetas (Tags) son elementos compactos e interactivos que muestran
información relevante: categorías, nombres de usuario, ubicaciones, fechas o
estados. Pueden agrupar varios elementos en una misma área y pueden contener o
no íconos.

## 2. Anatomía

1. **Ícono** — opcional; puede ir a la izquierda o a la derecha.
2. **Etiqueta** — el texto del tag.
3. **Contenedor** — la píldora que envuelve ícono + texto.

## 3. Construcción (medidas)

### Tag con ícono
| Elemento | Medida |
|---|---|
| Padding izquierdo | 16 px |
| Espaciado ícono ↔ texto | 4 px |
| Padding superior / inferior | 4 px |
| Padding derecho | 12 px |
| Altura máxima | 24 px |
| Ancho mínimo | 93 px (palabras cortas en adelante) |

### Tag sin ícono
| Elemento | Medida |
|---|---|
| Padding izquierdo / derecho | 12 px |
| Padding superior / inferior | 4 px |
| Altura máxima | 24 px |
| Ancho mínimo | 78 px (palabras cortas en adelante) |

- **Borde redondeado:** píldora → `radius = altura / 2` = 12 px con altura 24 px.
- **Espaciado entre tags agrupados:** 16 px.

## 4. Variantes

- **Sin ícono.**
- **Con ícono a la izquierda** (chevron `<` antes del texto).
- **Con ícono a la derecha** (`×` u otro ícono después del texto).

## 5. Estados

| Estado | Fondo | Texto | Borde |
|---|---|---|---|
| **Por defecto** | `#FFFFFF` blanco | azul `#0033A0` | gris muy claro suave |
| **Activo** | `#0033A0` (relleno, confirmado por muestreo `(0,51,160)`) | blanco | — |
| **Sobre (hover)** | blanco | azul `#0033A0` | borde azul `#0033A0` 1 px |
| **Enfocado (focus)** | blanco | azul `#0033A0` | borde azul `#0033A0` reforzado (anillo de foco) |
| **Inactivo (disabled)** | gris claro atenuado | gris atenuado | — |

## 6. Colores de estado (Tags de alerta)

Estos 4 pares son de **uso exclusivo** para tags de estado (información,
advertencia, éxito, error). Coinciden con la paleta de alertas del manual.

| Estado | Principal | Fondo suave | Contraste impreso |
|---|---|---|---|
| **Información** | `#0033A0` | `#E0EAFF` | AAA (8.8) |
| **Advertencia** | `#ED8B00` | `#FFF5EC` | AA (2.8) |
| **Éxito** | `#067014` | `#DEF6DE` | AA (5.5) |
| **Error** | `#D12D35` | `#FFF4F3` | AA (4.7) |

> El manual rotula la fila como "INFORMACIÓN 1 / 2", "ADVERTENCIA 1 / 2", etc.
> El número 1 es el color **principal** (texto/borde) y el 2 es el **fondo suave**.

> ⚠ **El estado se comunica con el FONDO de color del tag, no con una "bolita".**
> El par de la fila se aplica como **píldora rellena**: fondo = color suave (col. 2),
> texto = color principal (col. 1). **Nunca** representes el estado con un punto/
> círculo de color junto a un texto sobre fondo blanco o neutro — eso es una
> desviación. El contenedor coloreado **es** la señal de estado; un dot decorativo
> al lado es redundante y rompe la anatomía del tag (§2: contenedor que envuelve
> ícono + texto, sin viñeta de color suelta). Si necesitas un ícono, va a la
> izquierda o derecha (§4), no un bullet de color como sustituto del fondo.

## 7. Uso

- Máximo **2 palabras** por tag, para mantener apariencia limpia y legible.
- Respetar **16 px** de espaciado entre tags para crear relación y estructura.
- Usar **mínimo 2 tags** en pantalla — no es correcto usar uno solo.
- No alargar un tag con demasiado texto (incorrecto).
- El espaciado entre tags debe ser uniforme (16 px, no mezclar 16 y 38).

> **Aclaración — columna de estado (un tag por fila):** la regla de "**mínimo
> 2 tags**" aplica a tags **agrupados horizontalmente** (una fila de tags
> relacionados: categorías, filtros, metadatos juntos). **No** aplica a una
> **columna de estado** en una tabla/lista, donde cada fila lleva **un solo**
> tag de estado (p. ej. "En funcionamiento" repetido fila a fila). Esa columna
> es un patrón válido y completo: el conjunto vertical de tags ya cumple el
> espíritu de la regla (no hay un tag huérfano y solo en pantalla). Al auditar,
> **no marques como desviación** una lista con un tag de estado por fila por
> "tener solo 1 tag" — la regla del ≥2 es para grupos horizontales, no para una
> columna repetida.

## 8. Tokens CSS

```css
:root {
  --tag-height: 24px;
  --tag-radius: 12px;              /* altura / 2 (píldora) */
  --tag-pad-y: 4px;
  --tag-pad-x-sin-icono: 12px;
  --tag-pad-left-con-icono: 16px;
  --tag-pad-right-con-icono: 12px;
  --tag-icon-gap: 4px;
  --tag-gap: 16px;                 /* entre tags agrupados */
  --tag-min-w-con-icono: 93px;
  --tag-min-w-sin-icono: 78px;

  /* Por defecto / hover / focus */
  --tag-default-bg: #FFFFFF;
  --tag-default-text: #0033A0;
  /* Activo */
  --tag-active-bg: #0033A0;
  --tag-active-text: #FFFFFF;

  /* Tags de alerta */
  --tag-info: #0033A0;     --tag-info-bg: #E0EAFF;
  --tag-warning: #ED8B00;  --tag-warning-bg: #FFF5EC;
  --tag-success: #067014;  --tag-success-bg: #DEF6DE;
  --tag-error: #D12D35;    --tag-error-bg: #FFF4F3;

  --font-tag: 'Sura Sans', 'Helvetica Neue', Arial, sans-serif;
}
```

## 9. Reglas operativas para el skill

- Tag = píldora con `border-radius: calc(height / 2)`; altura 24 px → radio 12 px.
- Texto siempre en Sura Sans; nunca Barlow.
- Estado activo = relleno `#0033A0` con texto blanco; los demás estados son sobre
  fondo blanco con texto/borde `#0033A0`.
- Para tags de estado, usar exclusivamente los 4 pares de §6 según el rol
  (info/advertencia/éxito/error). No reutilizarlos como color decorativo.
- **El estado va en el FONDO del tag, no en una "bolita" de color.** Píldora
  rellena: fondo = color suave (col. 2), texto = principal (col. 1). Prohibido
  marcar el estado con un dot/círculo de color junto al texto (§6).
- **Tags de estado = solo texto, SIN ícono.** El fondo de color ya comunica el
  estado; meter un ícono (sol, candado, check…) dentro del tag de estado es
  redundante y suele quedar inconsistente (unas filas con ícono y otras sin él).
  Reserva los íconos (§4) para tags de categoría/acción, nunca para la columna de
  estado Activo/Inactivo.
- Agrupar siempre ≥2 tags con gap de 16 px; máximo 2 palabras por etiqueta.

## 10. Pendiente

- [ ] Confirmar grosor exacto del borde en hover/focus (la lámina no imprime px).
- [ ] Confirmar el gris exacto del estado inactivo (no impreso; muestrear si se
      requiere fidelidad alta).
