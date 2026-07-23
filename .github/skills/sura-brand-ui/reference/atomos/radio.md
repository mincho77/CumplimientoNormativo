# Botón de radio (Radio button) — átomo

Fuente: `Botón de Radio.pdf` (1 lámina). Verificado contra imágenes renderizadas
y muestreo de píxeles. **Tipografía: Sura Sans. No aparece Barlow.**

## 1. Qué es

Selecciona **una sola** opción de un conjunto. Al seleccionar, aparece un
círculo de relleno de menor radio dentro del círculo exterior. Seleccionar otro
anula el anterior. Siempre debe haber **una opción seleccionada** por defecto.

## 2. Anatomía

1. Ícono **seleccionado** (círculo exterior + punto interno relleno).
2. Etiqueta de texto cercana.
3. Ícono **no seleccionado** (círculo exterior vacío).

## 3. Construcción (medidas)

| Elemento | Medida |
|---|---|
| **Contenedor** (área táctil) | 40 × 40 px |
| **Círculo exterior** (anillo) | 20 × 20 px |
| **Círculo interno** (punto relleno al seleccionar) | 10 × 10 px |
| **Área segura** | 12 px de margen (48 × 48 px total) → mejor toque en móvil |
| **Altura mínima** | 40 px |
| **Ancho máximo** | depende del contenedor |
| **Gap radio ↔ etiqueta** | 12 px |
| **Espaciado horizontal mínimo** | 8 px |
| **Espaciado vertical** | 10 px |
| **Tamaño de texto de la etiqueta** | 16 px (= 1 rem) |

## 4. Estados × selección (de la lámina "Estados")

Cada estado existe en **Seleccionado / No seleccionado** y **Sin etiqueta / Con
etiqueta**.

| Estado | Color del anillo/punto (seleccionado) | Notas |
|---|---|---|
| **Activo** | `#2D6DF6` (Azul SURA) | estado por defecto |
| **Sobre** (hover) | `#2D6DF6` | igual al activo en la lámina |
| **Enfocado** | `#2D6DF6` + halo de foco `#81B1FF` (azul claro) | anillo de foco exterior |
| **Presionado** | `#0033A0` (Azul Profundo) | azul más oscuro al pulsar |
| **Inactivo** (deshabilitado) | gris `~#818181`, atenuado | sin interacción |

> No seleccionado en todos los estados = círculo exterior con borde, sin relleno.
> El gris de inactivo coincide con el token de Inactivo de botones
> (`#818181` texto / familia de grises del manual).

## 5. Colocación / buenas prácticas

- Listar **verticalmente**, con espaciado de 48 px entre filas (de la lámina de
  Colocación).
- Evitar distribución **horizontal**; si se requiere, mínimo **24 px** entre
  elementos.
- Siempre una opción seleccionada por defecto.
- No anidar radios ni usarlos para selección múltiple (eso es checkbox).
- No mezclar radios y checkboxes en el mismo grupo; sepáralos en conjuntos.
- Úsalo para elegir una sola opción de un conjunto (ej. diálogo de Color: Rojo /
  Azul / Verde).

## 6. Tokens para implementación

```css
:root {
  --radio-container: 40px;
  --radio-outer: 20px;
  --radio-inner: 10px;
  --radio-safe-margin: 12px;
  --radio-gap-label: 12px;
  --radio-min-height: 40px;
  --radio-label-size: 16px;          /* 1rem, Sura Sans regular */

  --radio-color-active: #2D6DF6;     /* Azul SURA */
  --radio-color-pressed: #0033A0;    /* Azul Profundo */
  --radio-focus-ring: #81B1FF;       /* halo de enfoque */
  --radio-color-disabled: #818181;   /* gris inactivo */
}
```

## 7. Reglas operativas para el skill

- Radio = elegir **una** opción de un conjunto; **siempre** una seleccionada por
  defecto. Para selección múltiple usa **casilla de verificación**, nunca radio.
- Medidas: contenedor 40×40, anillo 20, punto 10, área segura +12 (48×48 en
  móvil), gap radio↔etiqueta 12, etiqueta 16 px Sura Sans regular.
- Colores por estado: activo/hover/enfocado `#2D6DF6` (+ halo `#81B1FF` en
  foco); presionado `#0033A0`; inactivo gris `#818181`. **El hex manda.**
- Colocación: lista **vertical**, 48 px entre filas; horizontal solo si hace
  falta, mínimo 24 px. No anidar radios ni mezclarlos con checkboxes en un grupo.
- Tipografía Sura Sans; **nunca Barlow**.

## 8. Pendiente

- [ ] Confirmar hex exacto del estado **Inactivo** (muestreo dio `~#7A8287`;
      probablemente el gris de la escala del manual `#818181`).
- [ ] Confirmar si **Sobre** (hover) tiene un tono propio o es idéntico a Activo
      (en la lámina se ven iguales).
