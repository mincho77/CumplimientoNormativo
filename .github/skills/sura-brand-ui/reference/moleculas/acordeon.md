# Acordeón (Accordion) — molécula

Fuente: `Acordeón.pdf` (varias láminas). Verificado contra imágenes renderizadas y
muestreo de píxeles. **Tipografía: Sura Sans. No aparece Barlow.**

## 1. Qué es

El acordeón agrupa contenido en secciones que el usuario expande o contrae. Hay
**dos tipos**:

- **Acordeón simple** — para secciones informativas (preguntas frecuentes,
  información sobre un tema). Cada panel tiene título, subtítulo opcional y un
  párrafo de contenido.
- **Acordeón múltiple (múltiples ítems)** — lista contenido puntual con un
  encabezado, una lista de ítems y una bajada o footer. Útil para mostrar
  opciones de segundo nivel en un menú lateral, o construir filtros / mostrar
  propiedades del sistema.

## 2. Anatomía

### Acordeón simple
1. **Contenedor.**
2. **Ícono.**
3. **Título.**
4. **Subtítulo.**
5. **Flecha de despliegue** (chevron).

### Acordeón múltiple
1. **Encabezado** del acordeón cerrado.
2. **Item central** (puede llevar ícono — radio / casilla / otro).
3. **Bajada o footer.**
4. **Acordeón desplegado.**

## 3. Construcción (medidas)

### Acordeón simple
| Elemento | Medida |
|---|---|
| Espaciado interno (padding) | 16 px |
| Espaciado entre ícono y contenido | 12 px |
| Espaciado entre título y subtítulo | 4 px |
| Altura cerrado | 72 px (mín. 52 px si no lleva subtítulo) |
| **Altura mínima abierto** | 142 px (a partir de ahí varía según el texto del panel) |
| Ancho mínimo (móvil) | **294 px** |
| Bordes redondeados | 12 px |
| Borde lineal | 1 px, color `#CCDAFF` |
| Marcadores (despliegue) | 24 px |

### Acordeón múltiple
| Elemento | Medida |
|---|---|
| Padding interno (encabezado / item / footer) | 16 px |
| Espaciado entre texto e ícono | 12 px |
| Altura del acordeón cerrado | 56 px |
| Ancho mínimo (móvil) | 342 px |
| Bordes redondeados | 12 px |
| Borde lineal | 1 px, color `#CCDAFF` |

> Aplica a las tres zonas (Encabezado, Item central, Bajada o footer): mismo
> padding 16 px y mismo tratamiento de borde/redondeo.

### 3.bis Mobile / Responsivo

Fuente: *Acordeón - mobile.pdf*. La construcción del acordeón es prácticamente
**idéntica** entre web y móvil (mismo padding 16 px, gap ícono↔contenido 12 px,
título↔subtítulo 4 px, alturas cerrado 72/52 px simple y 56 px múltiple, borde
12 px / 1 px `#CCDAFF`) — **no se repite**. La única diferencia móvil real es el
**ancho mínimo distinto por tipo**:

| Tipo | Ancho mínimo móvil |
|---|---|
| **Acordeón simple** | **294 px** |
| **Acordeón múltiple** | **342 px** |

> El acordeón simple admite un contenedor más angosto (294 px) porque solo apila
> título + subtítulo + chevron; el múltiple necesita 342 px para alojar el
> encabezado con *texto de apoyo* a la derecha y la lista de ítems con casilla. En
> el resto, móvil y web comparten exactamente la misma construcción.

## 4. Tipografía

| Texto | Tamaño | Estilo |
|---|---|---|
| Título / Encabezado | 16 px | Semibold |
| Texto de apoyo / Subtítulo | 14 px | Regular |
| Item central (múltiple) | 14 px | Regular |
| Párrafo (simple) | 14 px | Regular |

- El título ocupa **máximo 1 línea**, sin importar el ancho del acordeón. Si el
  texto excede, se trunca con puntos suspensivos (`…`) — solo para prototipado en
  Figma; en la implementación real el componente **no debe superar** ese límite.
- El título / texto se alinea **siempre a la izquierda**.

## 5. Estados y colores

- **Encabezado / título activo:** azul `#0033A0` (muestreo `(0,51,160)`).
- **Borde del contenedor:** `#CCDAFF` (lila claro), 1 px.
- **Estado contraído / Estado abierto (desplegado):** la flecha chevron rota para
  indicar el estado; el contenido aparece debajo al expandir.

## 6. Item central — ícono

- El ícono del item central es **opcional**.
- Se usa cuando el usuario debe **seleccionar una opción** (botón de radio) o
  **varias** (casillas de verificación). También puede ser cualquier otro ícono
  según la información adicional que se quiera dar al usuario.

## 7. Uso

- **Componentes en grupo:** usar **mínimo 3 y máximo 6** acordeones en grupo.
  **No debe utilizarse uno solo** (incorrecto).
- Diseñar para móvil (1 columna) y escritorio (multi-columna), colocando el grupo
  de acordeones al final del contenido.
- Acordeón simple: altura mínima abierta 142 px; respetar título/subtítulo/párrafo.

## 8. Tokens CSS

```css
:root {
  /* Común */
  --accordion-radius: 12px;
  --accordion-border: 1px solid #CCDAFF;   /* lila claro */
  --accordion-pad: 16px;
  --accordion-icon-gap: 12px;              /* ícono ↔ contenido/texto */
  --accordion-active: #0033A0;             /* encabezado/título activo */
  --accordion-simple-min-w-mobile: 294px;  /* simple: contenedor más angosto */
  --accordion-multi-min-w-mobile: 342px;   /* múltiple: aloja apoyo + lista */

  /* Simple */
  --accordion-simple-h-closed: 72px;
  --accordion-simple-h-closed-min: 52px;   /* sin subtítulo */
  --accordion-simple-h-open-min: 142px;
  --accordion-simple-title-gap: 4px;       /* título ↔ subtítulo */
  --accordion-marker: 24px;

  /* Múltiple */
  --accordion-multi-h-closed: 56px;

  /* Tipografía */
  --accordion-title-size: 16px;            /* semibold */
  --accordion-text-size: 14px;             /* regular */

  --font-accordion: 'Sura Sans', 'Helvetica Neue', Arial, sans-serif;
}
```

## 9. Reglas operativas para el skill

- Dos tipos: **simple** (informativo) y **múltiple** (encabezado + ítems + footer).
- Contenedor: `border-radius: 12px`, borde `1px solid #CCDAFF`, padding 16 px,
  gap ícono↔contenido 12 px.
- Altura cerrada: simple 72 px (mín 52 px sin subtítulo) / múltiple 56 px.
  Abierto simple: mínimo 142 px.
- Título 16 px semibold, apoyo/párrafo/ítem 14 px regular; **siempre 1 línea** con
  truncado `…`; alineado a la izquierda.
- Encabezado/título activo en `#0033A0`; nunca Barlow.
- Agrupar **3–6** acordeones; nunca uno solo. Ancho mínimo móvil: simple **294 px**,
  múltiple **342 px**.
- Ítem central con ícono solo cuando hay selección (radio/casilla) u otra ayuda.

## 10. Pendiente

- [ ] Confirmar color del texto/ícono por defecto (no activo) y del subtítulo
      (probable `--gray-900` / neutro; no impreso en hex).
- [ ] Confirmar el hex de fondo del ítem resaltado en el estado desplegado
      (gris azulado suave; no impreso — muestrear si se requiere fidelidad alta).
- [ ] Confirmar grosor/color exacto del chevron de despliegue.
