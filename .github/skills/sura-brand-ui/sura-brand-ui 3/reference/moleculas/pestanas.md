# Pestañas (Tabs) — molécula

Fuente: `Pestañas.pdf` (1 lámina). Verificado contra imágenes renderizadas y
muestreo de píxeles. **Tipografía: Sura Sans. No aparece Barlow.**

## 1. Qué es

Las pestañas permiten cambiar entre vistas de grupos de información distintos
pero relacionados. Sirven para organizar contenido en diferentes pantallas,
conjuntos de datos y otras interacciones.

## 2. Anatomía

1. **Contenedor.**
2. **Indicador** — la línea/subrayado que marca la pestaña activa.
3. **Ícono** (opcional).
4. **Etiqueta** — el texto de la pestaña.

## 3. Construcción (medidas)

### Solo ícono
| Elemento | Medida |
|---|---|
| Padding | 18 px |
| Espaciado entre pestañas | 4 px |
| Espaciado indicador ↔ tab | 11 px |
| Tamaño del ícono | 24 × 24 px |

### Texto e ícono
| Elemento | Medida |
|---|---|
| Padding | 16 px |
| Espaciado ícono ↔ etiqueta | 8 px |
| Espaciado indicador ↔ tab | 11 px |

### Flotante
| Elemento | Medida |
|---|---|
| Padding | 5 px |
| Espaciado entre pestañas | 4 px |

## 4. Estados de la pestaña base

Variantes a las que aplican: **Ícono**, **Flotante**, **Fijo con ícono**.

| Estado | Apariencia |
|---|---|
| **Por defecto** | texto/ícono neutro, sin indicador |
| **Activo** | texto/ícono azul `#0033A0` (muestreo `(0,51,160)`) + indicador (subrayado azul) |
| **Sobre (hover)** | texto/ícono azul `#0033A0` + indicador |
| **Enfocado (focus)** | recuadro/anillo de foco azul |
| **Inactivo (disabled)** | gris atenuado |

> 🔑 **Texto e indicador van como una unidad del mismo color.** En el estado
> Activo, la etiqueta y el subrayado comparten color (`#0033A0` en claro); no se
> parten en dos colores distintos.

### 4.bis Modo oscuro — la pestaña activa es SELECCIÓN, no lectura

La pestaña activa es un **indicador de selección**, así que en oscuro se reasigna
al **acento amarillo `#E3E829`** (no al azul de lectura) — coherente con
`generales/modo-oscuro.md` §2/§5/§8 ("selección/pestaña activa → amarillo").
Manteniendo la regla §4 de que texto e indicador van unidos:

| Estado | Claro | Oscuro |
|---|---|---|
| **Activo** (etiqueta **+** indicador, unificados) | `#0033A0` | **`#E3E829`** (Amarillo alegría) |
| **Inactivo / por defecto** | neutro | `#81B1FF` (azul foco, texto de lectura) |

> ⚠ **No dejar la letra activa en azul con solo el subrayado amarillo.** En oscuro
> `#81B1FF` es a la vez el color de lectura y el de las inactivas, así que una
> etiqueta activa azul **no se distingue** de las inactivas: solo cambiaría el
> peso. El amarillo en etiqueta + indicador es lo que marca la selección.
> Verificado AA: `#E3E829` sobre `#00003F` = **14.78:1** ✅.

## 5. Estados del conjunto

Dos tratamientos del grupo de pestañas:
- **Sin relleno** — pestañas sobre fondo transparente.
- **Relleno blanco** — pestañas sobre una barra/fondo blanco.

## 6. Uso

- **Mínimo 3 tabs (obligatorio), máximo 6 tabs** por componente.
- **Tamaño mínimo de cada tab: 215 px**; el máximo depende del número de tabs y
  del texto que contengan.
- No usar más de **2 componentes de pestañas por pantalla**.
- No usar etiquetas muy largas ni variar el uso de íconos.
- Preferir "Ícono y Etiqueta de texto" para el contenido más relevante.
- Pestañas **solo con íconos**: únicamente en **contexto móvil**.

## 7. Tokens CSS

```css
:root {
  /* Solo ícono */
  --tab-icon-pad: 18px;
  --tab-icon-gap: 4px;
  --tab-icon-size: 24px;
  /* Texto e ícono */
  --tab-pad: 16px;
  --tab-icon-label-gap: 8px;
  /* Flotante */
  --tab-float-pad: 5px;
  --tab-float-gap: 4px;
  /* Común */
  --tab-indicator-gap: 11px;     /* indicador ↔ tab */
  --tab-min-w: 215px;
  --tab-active: #0033A0;         /* texto, ícono e indicador activos (claro) */
  --tab-active-dark: #E3E829;    /* oscuro: selección = acento amarillo */
  --tab-inactive-dark: #81B1FF;  /* oscuro: inactivas en azul de lectura */

  --font-tab: 'Sura Sans', 'Helvetica Neue', Arial, sans-serif;
}
```

## 8. Reglas operativas para el skill

- Pestaña activa = texto/ícono `#0033A0` + indicador (subrayado) `#0033A0`;
  las inactivas en neutro. **Texto e indicador siempre del mismo color** (unidad).
- **Modo oscuro:** la pestaña activa es selección → texto **+** indicador en
  amarillo `#E3E829`; las inactivas en azul de lectura `#81B1FF`. Nunca dejar la
  etiqueta activa azul con solo el subrayado amarillo (no se distinguiría de las
  inactivas). Ver §4.bis y `generales/modo-oscuro.md` §5.
- Generar siempre entre 3 y 6 tabs; cada tab ≥215 px de ancho.
- Texto Sura Sans; nunca Barlow.
- Variante solo-ícono solo en layouts móviles.
- Máximo 2 grupos de pestañas por pantalla.

## 9. Pendiente

- [ ] Confirmar el neutro exacto del texto/ícono por defecto e inactivo
      (no impreso en hex; muestrear si se requiere fidelidad alta).
- [ ] Confirmar grosor del indicador (subrayado) en px (no impreso).
