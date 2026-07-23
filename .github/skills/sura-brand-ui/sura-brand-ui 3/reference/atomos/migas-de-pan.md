# Migas de pan (Breadcrumb) — átomo

Fuente: `Migas de pan_Merged.pdf` (2 láminas). Verificado contra imágenes
renderizadas y muestreo de píxeles. **Tipografía: Sura Sans. No aparece Barlow.**

> ⚠ **Nota de color (aplica «el hex manda»):** la lámina de Colores **imprime**
> el hex `#26328C` junto al rótulo "Azul Profundo", pero la **muestra renderizada
> real** es `#0033A0` (confirmado por muestreo `(0,51,160)`). El hex canónico de
> Azul Profundo (`generales/colores.md`) es `#0033A0`. Usa **`#0033A0`** e ignora
> el `#26328C` impreso (es uno de los exports de código poco fiables del PDF).

## 1. Qué es

Elemento de navegación que ayuda a los usuarios a **comprender dónde se
encuentran** dentro del sitio o aplicación y cómo se conecta con la jerarquía de
páginas. Muestra la ruta desde la raíz hasta la ubicación actual.

## 2. Anatomía

### Variante completa

1. **Raíz** — normalmente la página de inicio.
2. **Delimitador** — los elementos están separados por un ícono (chevron `>`).
3. **Nivel** — muestra el orden jerárquico de navegación en la ruta.
4. **Ubicación** — la página actual en la que se encuentra el usuario.

### Variante colapsada (Elipsis)

1. **Raíz en forma de elipsis** (`...`) — agrupa los niveles ocultos.
2. **Ubicación** — la página actual.
3. **Lista** — menú desplegable que se abre desde la elipsis con todas las
   opciones de la ruta.

## 3. Construcción (medidas)

| Elemento | Medida |
|---|---|
| **Espaciado horizontal** entre elementos (label ↔ chevron) | 8 px |
| **Espaciado vertical** | 8 px |
| **Lista desplegable — radio de borde** | 12 px (`--radius-md`) |
| **Lista desplegable — espaciado interno** | 4 px |

> El separador es un **chevron `>`**, no una barra ni una diagonal. La lista
> desplegable (al abrir la elipsis) es una tarjeta blanca con `border-radius`
> 12 px y sombra.

## 4. Colores (según fondo)

El color del texto **se adapta al fondo** sobre el que se coloca la miga de pan.
La página actual se diferencia siempre (peso **negrita** o color destacado).

| Fondo | Enlaces (niveles) | Delimitador `>` | Página actual |
|---|---|---|---|
| **Claro / blanco** | Azul Profundo `#0033A0` | Azul Profundo `#0033A0` | `#0033A0` en **negrita** |
| **Azul Cielo Latino** `#2D6DF6` | Blanco `#FFFFFF` | Blanco `#FFFFFF` | Blanco `#FFFFFF` **negrita** |
| **Azul oscuro / Profundo** | Blanco `#FFFFFF` | Blanco `#FFFFFF` | **Amarillo Primario** `#E3E829` |

| Parte | Color | Hex |
|---|---|---|
| **Enlaces y delimitador** (sobre fondo claro) | Azul Profundo | `#0033A0` |
| **Texto sobre fondo azul** | Blanco Puro | `#FFFFFF` |
| **Página actual destacada** (sobre fondo oscuro) | Amarillo Primario | `#E3E829` |
| **Lista desplegable** (fondo) | Blanco Puro | `#FFFFFF` |
| **Ítem de lista — texto** | Azul Profundo | `#0033A0` |
| **Ítem de lista — hover (fondo)** | Gris muy claro | `~#F4F6FA` |

> En **fondo claro**, enlaces y página actual comparten `#0033A0`; la página
> actual se distingue por el **peso negrita**, no por el color. El color
> destacado (Amarillo Primario) solo aparece para la página actual sobre fondos
> oscuros.

## 5. Comportamiento

- Las rutas se **acortan** cuando no hay suficiente espacio para mostrar todos
  los niveles, o cuando existen **5 o más** rutas de navegación.
- La ruta acortada usa la **elipsis** (`...`); al activarla, despliega una
  **lista** con todas las opciones de la ruta.
- Cuando un **nombre de página es muy extenso**, usa la variante elipsis para
  truncarlo (ej. `Previa > Serv... > Actual`).

## 6. Uso

**Úsalo cuando:**
- Necesites ayudar a los usuarios a comprender y navegar entre varias páginas
  del sitio.

**Considera:**
- Debe aparecer en **todas las páginas excepto la página de inicio**.
- **No** lo uses en sitios con navegación de **un solo nivel**.
- Todos los elementos de la ruta deben ser **enlaces en los que se pueda hacer
  clic**, salvo la **página actual**, que se muestra como **texto sin formato**
  (no clicable).
- Es solo una **ayuda a la navegación**: **no** lo uses para mostrar los pasos
  de un proceso (para eso va el **stepper / paginador**).

## 7. Contexto de uso

La mayoría de las veces, las migas de pan se colocan **antes del contenido
principal y después del encabezado**. Comienzan en el **primer nivel** (página
de inicio) y terminan en el **último nivel** para dejar claro dónde se encuentra
el usuario.

Ejemplos reales: `Inicio > Productos > Motos` · `Canales de venta > ... > Sufi`
(con desplegable: Entidades financieras / Grupo Bancolombia / Servicios en línea).

## 8. Tokens para implementación

```css
:root {
  /* Espaciado */
  --breadcrumb-gap-h: 8px;            /* entre elemento y chevron */
  --breadcrumb-gap-v: 8px;            /* vertical */
  --breadcrumb-dropdown-radius: 12px; /* tarjeta de lista (radius-md) */
  --breadcrumb-dropdown-gap: 4px;     /* espaciado interno de la lista */

  /* Colores — fondo claro (por defecto) */
  --breadcrumb-link: #0033A0;         /* Azul Profundo (enlaces + chevron) */
  --breadcrumb-current: #0033A0;      /* página actual (negrita) */
  --breadcrumb-current-weight: 700;   /* negrita */

  /* Colores — fondo azul (#2D6DF6) */
  --breadcrumb-on-blue: #FFFFFF;      /* texto blanco */

  /* Colores — fondo oscuro */
  --breadcrumb-on-dark: #FFFFFF;      /* enlaces blancos */
  --breadcrumb-current-dark: #E3E829; /* Amarillo Primario (página actual) */

  /* Lista desplegable */
  --breadcrumb-dropdown-bg: #FFFFFF;
  --breadcrumb-dropdown-item: #0033A0;
  --breadcrumb-dropdown-hover-bg: #F4F6FA;
}
```

## 9. Reglas operativas para el skill

1. Separador = **chevron `>`** en el mismo color que los enlaces. Nunca uses
   `/`, `|` ni `»`.
2. Sobre fondo claro: todo el texto en `#0033A0`; la **página actual en
   negrita** y **sin enlace** (texto plano). Los demás niveles son enlaces.
3. Sobre fondo `#2D6DF6`: todo el texto en **blanco**. Sobre fondo oscuro:
   enlaces en blanco y **página actual en `#E3E829`** (Amarillo Primario).
4. Si hay **≥ 5 niveles** o falta espacio, colapsa con **elipsis `...`** que
   abre una **lista desplegable** (tarjeta blanca, `radius` 12 px, ítems en
   `#0033A0`, hover `~#F4F6FA`).
5. Trunca con elipsis los **nombres muy largos**.
6. **No** muestres migas de pan en la **página de inicio** ni en sitios de un
   solo nivel; **no** las uses como indicador de pasos de un proceso.
7. Coloca el breadcrumb **antes del contenido principal**, tras el encabezado.

## 10. Pendiente

- [ ] Confirmar el **tamaño de tipografía** exacto del breadcrumb (la escala de
      texto no quedó legible en la lámina de construcción).
- [ ] Confirmar el **peso tipográfico** de los enlaces vs. página actual
      (¿regular vs. semibold/bold?).
- [ ] Confirmar el **hover de la lista** (`~#F4F6FA` por muestreo escaso) y si
      el ítem activo lleva color/peso distinto.
- [ ] Confirmar el **límite de caracteres** que dispara el truncado (la lámina
      sugiere ~20 caracteres / "4 caracteres del nombre").
