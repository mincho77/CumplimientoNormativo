---
name: sura-brand-ui
description: 'Aplica el sistema de diseño SURA en tres modos: GENERAR (mockups UI web/móvil con PNG + specs), AUDITAR (ajuste de código HTML/CSS/SCSS/JSX/TSX/Vue/Angular/Tailwind/styled-components a marca) y PRESENTAR (presentaciones HTML interactivas y navegables: deck de slides dinámico con modo claro/oscuro, fondo difuminado según temática, animaciones y transiciones por elemento, barra de progreso, slides interactivas como mapas anatómicos, comparadores antes/después, pasos/ciclos, líneas de tiempo, galerías con lightbox y tarjetas de datos, en tono SURA). Use when: diseña interfaz SURA, crea mockup, ajusta UI a marca, audita brand compliance, crea presentación/deck/slides interactivo SURA. Do NOT use for archivos PowerPoint .pptx (usar pptx), documentos Word (usar docx) o edición de Figma.'
---

## Overview

Este skill aplica el sistema de diseño corporativo de Seguros SURA, derivado de
los manuales de marca y organizado con **Atomic Design** (Generales → Átomos →
Moléculas → Organismos) en `reference/`. Funciona en tres modos:

- **MODO GENERAR** — Diseña una interfaz nueva a partir de una descripción
  (ej. "pantalla de login del portal de clientes") y produce un **mockup PNG** +
  **especificaciones de marca** en texto.
- **MODO AUDITAR** — Toma **código existente** y lo corrige in situ para que
  cumpla la marca (tipografía, color, radio, elevación, espaciado, estados,
  accesibilidad), entregando un **reporte de cambios**. El flujo detallado vive
  en `reference/auditoria.md`.
- **MODO PRESENTAR** — Crea una **presentación HTML interactiva y navegable**
  (deck de slides autónomo) pensada para **mantener la atención**: dinámica e
  interactiva por defecto (animaciones y transiciones por elemento y slide),
  fondo difuminado elegido según la temática, header minimalista con barra de
  progreso, modo claro/oscuro, y slides que **muestran en vez de contar** (mapas
  anatómicos, comparadores antes/después, pasos/ciclos, líneas de tiempo,
  galerías con lightbox, tarjetas de datos). No es un `.pptx`. El patrón completo
  vive en `reference/organismos/presentacion-interactiva.md`.

## When to Use

**MODO GENERAR:**
- Diseño de pantallas web, móviles, dashboards, formularios o flujos.
- Wireframes o mockups de baja/media fidelidad respetando la marca.
- Especificaciones técnicas para que un desarrollador implemente la UI.

**MODO AUDITAR:**
- Ajustar HTML/CSS/SCSS/JSX/TSX/Vue/Angular/Tailwind/styled-components ya escrito
  para que cumpla el sistema de diseño SURA.
- Detectar y corregir Barlow, colores fuera de paleta, radios/elevaciones/
  espaciados fuera de escala, estados faltantes, contraste insuficiente.
- Validar cumplimiento de marca en código existente con reporte de cambios.

**MODO PRESENTAR:**
- Crear una presentación/deck de slides **HTML interactivo y navegable** con marca
  SURA (formación, sesiones de equipo, demos), no un archivo PowerPoint.
- Slides con animaciones de entrada, navegación por teclado/clic, modo claro/
  oscuro, y piezas interactivas: mapas/diagramas con nodos, comparadores antes/
  después, galerías con lightbox, tarjetas de datos con fuentes.
- Iterar y refinar un deck existente (reordenar nodos, corregir layout, añadir
  slides).

## When NOT to Use

- Crear archivos editables de Figma — el skill produce imágenes, no .fig.
- Presentaciones en **PowerPoint (.pptx)** — usar el skill `pptx`. (Para
  presentaciones **HTML interactivas/navegables**, usar **MODO PRESENTAR**.)
- Documentos largos tipo manual — usar `docx`.
- Generación de logos o assets de marca nuevos — el skill respeta marca,
  no inventa identidad.

## Cómo elegir el modo

1. ¿El usuario **pega o señala código** (archivo, fragmento, `input/…`) y pide
   ajustarlo/revisarlo/corregirlo a la marca? → **MODO AUDITAR**
   (sigue `reference/auditoria.md`).
2. ¿El usuario pide una **presentación, deck o slides interactivos/navegables**
   (no un `.pptx`)? → **MODO PRESENTAR** (sigue
   `reference/organismos/presentacion-interactiva.md`).
3. ¿El usuario pide **crear/diseñar/mockear** una pantalla desde cero? →
   **MODO GENERAR** (Paso 1-5 abajo).
4. Si es ambiguo, pregunta una vez con `AskUserQuestion`: "¿Quieres que diseñe
   una pantalla nueva, que ajuste un código existente a la marca, o que arme una
   presentación interactiva?".

## Quick Start

**GENERAR:**
```
User: "Diseña la pantalla de login del portal de clientes"
1. Identificar tipo de interfaz (web/móvil) y componentes necesarios.
2. Consultar reference/generales/* para tokens base (colores, tipografía).
3. Consultar reference/atomos/* y reference/moleculas/* para componentes.
4. Generar HTML/CSS aplicando tokens y componentes.
5. Renderizar a PNG con scripts/render_mockup.py.
6. Entregar mockup + especificaciones técnicas.
```

**AUDITAR:**
```
User: "Ajusta este componente a la marca SURA" (+ código)
1. Leer reference/auditoria.md (flujo de auditoría completo).
2. Inventariar desviaciones (tipografía, color, radio, elevación, espaciado).
3. Mapear cada una al token de marca correcto.
4. Corregir con Edit (cambios quirúrgicos, sin reescribir la app).
5. Verificar contraste con Python al cambiar pares texto/fondo.
6. Entregar código corregido + reporte de cambios.
```

**PRESENTAR:**
```
User: "Crea una presentación interactiva sobre X para mi equipo"
1. Leer reference/organismos/presentacion-interactiva.md (filosofía, fondos, patrones, gotchas).
2. ANALIZAR el contenido y proponer el guion: por cada bloque, el formato visual
   que lo hace más fácil de entender (mapa de nodos, comparador, tarjetas, pasos,
   línea de tiempo, datos…) y cuáles slides son interactivas. Confirmar con el usuario.
3. Elegir el FONDO según la temática (catálogo de presets §3b) y reportar la elección.
4. Construir el deck HTML autónomo: tokens de marca, fondo difuminado animado,
   header minimalista (toggle de tema + nombre + barra de progreso), slides con
   animación de entrada escalonada por elemento, modo claro/oscuro, contenido
   centrado (§5b), íconos SOLO del catálogo (transform §4), textos en tono SURA (§0.2).
5. Piezas interactivas (mapa de nodos, comparador, galería+lightbox, grilla,
   pasos, línea de tiempo) según §6–§7b y sus gotchas.
6. Verificar con navegador headless: recorrer TODAS las slides con window.go(i),
   ESPERANDO a que el stagger asiente antes de capturar, consola sin errores ([]),
   claro + oscuro, viewports 1440×810 y 1680×1050, composición con criterio.
7. Entregar el .html y ofrecer iteración por slide/componente.
```

## Core Instructions — MODO GENERAR

### Paso 1: Capturar contexto

Antes de diseñar, asegúrate de tener claro:

- **Tipo de interfaz**: web desktop, web móvil, app nativa, dashboard, formulario.
- **Propósito**: qué tarea va a realizar el usuario en esa pantalla.
- **Componentes esperados** (si el usuario los menciona): formulario, tabla,
  navegación, modales, etc.
- **Estado** a representar: vacío, con datos, error, éxito.

Si falta información crítica, pregunta una sola vez con `AskUserQuestion`
ofreciendo opciones concretas. Si es razonable asumir defaults, hazlo
y reporta el supuesto en la entrega.

### Paso 2: Consultar el sistema de diseño

Lee los archivos relevantes en `reference/` antes de generar el diseño.
La estructura sigue Atomic Design:

- `reference/generales/` — Colores, tipografía, grillas, elevaciones, logo,
  borde redondeado, formas/destacados, fotografía, ilustración, catálogo de
  ilustraciones, pictogramas, cobranding.
- `reference/atomos/` — Íconos, catálogo de íconos, avatar, botones, radios,
  interruptores, casilla de verificación, selector de rango, input stepper,
  miga de pan, cargador.
- `reference/moleculas/` — Menú, paginador, buscador, etiqueta, pestañas,
  acordeón, paso a paso, tooltip, lista, campos, modales, tarjetas,
  carrusel, toast.
- `reference/organismos/` — App-shell de navegación (PATRÓN POR DEFECTO),
  tablas, footer, menú navegador, banners.

**Regla:** nunca inventes valores de marca (colores, tipografías, medidas)
que no estén en `reference/`. Si una sección aún no existe, dilo
explícitamente y usa un placeholder marcado (ej. `/* TODO: validar color */`).

### Paso 2.5: Arranca con el App-shell por defecto

Para **cualquier interfaz nueva de pantalla completa** (portales, dashboards,
herramientas internas, catálogos, flujos admin), **el andamiaje por defecto es
el App-shell de navegación web** — ver `reference/organismos/app-shell.md`.
Salvo que el usuario pida algo distinto, toda UI nueva arranca con:

1. **Topbar azul sticky** (`#2D6DF6`, **azul en claro Y oscuro**): logo + nombre
   de la app · spacer · toggle de tema · bloque usuario (nombre + rol) · avatar
   con iniciales.
2. **Breadcrumbs** (`.crumbs`) con el contexto de navegación.
3. **Page-head**: `h1` + acciones a la derecha, luego el contenido.

Esto da la sensación "tipo navegación web" que SURA prefiere por defecto.
Excepciones (login/onboarding, modales embebidos, móvil compacto) en la §6 del
doc del organismo. El toggle de tema y el modo oscuro son **obligatorios**
(coherente con las memorias de marca).

### Usa los assets que VIENEN en el skill (no pidas cargarlos)

Este skill es **deliberadamente pesado** porque **empaqueta** todos los activos
de marca para que el agente los consuma directamente. **Nunca** le pidas al
usuario final que cargue íconos, fuentes, logos, ilustraciones o formas a su
proyecto: ya están aquí. Cárgalos desde la carpeta `assets/` del propio skill,
tanto en GENERAR como en AUDITAR.

| Activo | Ruta en el skill | Cómo usarlo |
|---|---|---|
| **Íconos** | `assets/icons/{nombre}.svg` | Inserta el SVG del catálogo; sustituye `currentColor` por el token. Nombre exacto según `iconos-catalogo.md`. |
| **Fuente Sura Sans** | `assets/fonts/SuraSans-Variable.{ttf,woff,woff2}` | Declara `@font-face` apuntando a este archivo. **Es la única tipografía oficial**; nunca pidas al usuario instalarla ni la sustituyas por una web-safe. |
| **Logos** | `assets/logo/logo-sura-{full,symbol}-{azul,blanco}.svg` | Elige la variante por fondo (claro→azul, oscuro→blanco) según `logo.md`. |
| **Ilustraciones** | `assets/illustrations/*.svg` | Catálogo en `ilustraciones-catalogo.md`. |
| **Formas / destacados** | `assets/shapes/*.svg` | Catálogo en `formas-destacados.md`. |

- En **GENERAR**: embebe los SVG y el `@font-face` desde `assets/` en el mockup;
  no dejes glifos de placeholder ni fuentes del sistema "provisionales".
- En **AUDITAR**: si al código le falta la fuente de marca o usa íconos ajenos,
  **corrige apuntando a los `assets/` del skill** (p. ej. inyecta el `@font-face`
  de `assets/fonts/SuraSans-Variable.woff2`), no dejes una nota pidiéndole al
  usuario que "agregue la fuente". El skill provee el activo; tu trabajo es
  cablearlo.

### Paso 3: Generar el HTML/CSS

Construye el mockup como un archivo HTML autónomo en `working/mockup.html`:

- Usa CSS variables para los tokens (`--color-primary`, `--font-titulo`, etc.).
- Estructura semántica (header, main, nav, form, button).
- Aplica el componente más simple que cumpla la necesidad — no agregues
  elementos decorativos que no estén en el sistema.
- Diseña en el ancho/alto correspondiente:
  - Web desktop: 1440×900
  - Móvil: 390×844
  - Tablet: 1024×768
- **Modo oscuro**: toda pieza de UI debe contemplarlo. Antes de derivar la
  paleta oscura, lee **`reference/generales/modo-oscuro.md`** — fija el único
  token de marca para oscuro (`#00003F`) y cómo derivar el resto de tokens ya
  existentes, verificándolos AA con Python. Usa **una sola maquetación**
  parametrizada por un flag (`data-theme="dark"` o un argumento `dark` en el
  generador): misma geometría, solo cambian los tokens, así un arreglo de layout
  sirve para ambos temas.
- **Estados interactivos (pestañas, paso a paso, acordeón, modal)**: un mockup
  estático representa **UN estado coherente por frame**. Si la UI tiene pestañas,
  muestra **solo el panel de la pestaña activa** — nunca apiles todas las
  secciones nombradas por las pestañas a la vez (eso contradice la promesa "una
  sección a la vez" del componente). Entrega **un PNG por estado** (una vista por
  pestaña/paso), parametrizando la misma maquetación con un **flag de estado**
  —igual que el flag de tema, y ortogonal a él: el generador produce el producto
  cartesiano estado × tema desde una sola plantilla. La cromática compartida
  (hero, barra lateral, cabecera) permanece **fija** entre estados; solo cambia
  el panel activo y el indicador de la pestaña.
- **Una sección vive en un solo lugar (IA sin duplicados)**: si una sección
  tiene su propia pestaña, no la repitas también como tarjeta en la barra
  lateral (ni viceversa). Decide un único hogar para cada bloque de información.
  La barra lateral es para metadato del activo siempre visible (acción,
  responsable, licenciamiento); las pestañas, para los cuerpos que se
  intercambian.

### Paso 4: Renderizar a imagen

Ejecuta el script de renderizado:

```bash
python scripts/render_mockup.py \
  --input working/mockup.html \
  --output output/mockup-{nombre}.png \
  --width {ancho} --height {alto}
```

El PNG queda en `output/` para que el usuario lo descargue.

#### Verificación de contención (anti-desbordamiento)

En mockups con coordenadas absolutas/calculadas (SVG, canvas), **el alto de cada
contenedor debe calcularse a partir del contenido real** (suma de los hijos +
relleno inferior), no a ojo. Antes de reportar éxito, verifica que **cada
elemento quepa dentro de su contenedor** por sus **cuatro** bordes:

- Presta atención especial a lo que vive **al fondo** de una tarjeta: botones de
  acción, chips, la última fila de una tabla, filas de "Ver más".
- **"Cabe el texto" ≠ "cabe el elemento".** Un botón puede ajustar bien su texto
  y aun así sobresalir ~10 px por debajo de una tarjeta de alto insuficiente.
  (Lección real: el botón "Registra tu opinión" quedaba desbordado porque la
  tarjeta cerraba 10 px antes de su borde inferior; se corrigió subiendo el alto
  de la tarjeta, no tocando el botón.)
- Comprueba borde **inferior** (`y + alto` del hijo ≤ `y + alto` del contenedor)
  y borde **derecho** (`x + ancho` del hijo ≤ `x + ancho` del contenedor).
- Si generas claro y oscuro con la misma maquetación, un arreglo de contención
  vale para ambos; re-renderiza y vuelve a verificar las dos versiones.

### Paso 5: Entregar especificaciones

Junto al mockup, entrega en el chat una sección de **Especificaciones**:

- **Tokens aplicados**: lista de colores, tipografías, espaciados usados.
- **Componentes**: listado de átomos/moléculas/organismos invocados,
  con referencia a la sección del manual.
- **Jerarquía visual**: cómo se organiza la información (qué es primario,
  secundario, terciario).
- **Justificación de marca**: 2-3 líneas explicando cómo el diseño
  refleja los lineamientos.
- **Pendientes** (si aplica): secciones del manual que aún no están en
  `reference/` y se usaron supuestos.

### Paso 6: Invitar a iterar (obligatorio)

Cierra **siempre** ofreciendo una iteración. No des el trabajo por terminado de
forma unilateral: pregúntale al usuario si quiere ajustar algo y pídele que
**indique qué componentes revisar** (p. ej. "el select", "el tag de estado",
"la fila expandida"). El diseño de marca se afina por componente, en rondas
cortas y dirigidas por el usuario. Ejemplo de cierre:

> "¿Quieres iterar sobre algún componente? Dime cuáles revisar (campos, tags,
> tabla, modal…) y los ajusto."

## Core Instructions — MODO AUDITAR

El flujo completo está en **`reference/auditoria.md`** — léelo al entrar a este
modo. Resumen del orden fijo:

1. **Recibir el código** (fragmento pegado o archivo señalado; léelo con `Read`).
2. **Inventariar los componentes** (paso obligatorio, `auditoria.md` §3.0):
   enumera **cada** componente con el que se construyó la UI (switch, botón,
   input, tarjeta, toast, tabla, pestañas, modal…), detecta su **rol funcional**
   (no su markup) y audítalo contra **su propia spec** en `reference/atomos|
   moleculas|organismos/` — anatomía, medidas y **todos** sus estados, no solo
   color/tipografía. Un patrón funcional (p. ej. un alternador de tema) **es** un
   componente de marca (el átomo Interruptor), no un elemento ad-hoc.
3. **Inventariar desviaciones** en 5 categorías: tipografía, color, radio,
   elevación, espaciado + estados/accesibilidad.
4. **Mapear** cada desviación al token de marca correcto (tablas de mapeo en
   `auditoria.md` §2). Si no hay equivalente claro, déjalo pendiente — no inventes.
5. **Corregir** con `Edit` (cambios quirúrgicos, sin reescribir la app ni tocar
   funcionalidad).
6. **Reportar** con tabla de cobertura por componente (§3.0) + tabla de cambios
   (antes → después → por qué) + pendientes + cómo verificar.
7. **Verificar** contraste con Python al cambiar pares texto/fondo.
8. **Invitar a iterar** (obligatorio): cierra preguntando si quiere otra ronda y
   pídele que **indique qué componentes revisar** (p. ej. "el switch", "los
   inputs", "la tabla"). No cierres la auditoría como definitiva por tu cuenta;
   el ajuste de marca es iterativo y dirigido por el usuario, componente a
   componente.

**Prioridad de hallazgos:** (1) Barlow / tipografía, (2) colores fuera de paleta,
(3) contraste que falla AA, (4) radio/elevación/espaciado.

## Core Instructions — MODO PRESENTAR

El patrón completo, con todos los snippets y gotchas, vive en
**`reference/organismos/presentacion-interactiva.md`** — léelo al entrar a este
modo. La meta del modo: un deck **dinámico e interactivo** que mantiene la
atención (cada elemento y slide se anima; se **muestra** en vez de **contar**;
§0). Resumen del flujo:

### Paso 1: Analizar el contenido y proponer el guion

**No conviertas el guion en slides de forma mecánica.** Primero **lee todo el
contenido** y decide, por bloque, qué **formato visual** lo hace más fácil de
entender (mapa de decisión §0.1): mapa de nodos para un sistema de partes,
comparador o dos tarjetas enfrentadas para A vs B, tarjetas de dato para cifras,
pasos animados para un proceso, línea de tiempo para una evolución, árbol/código
anotado para una jerarquía, grilla de tarjetas para definición + facetas,
slide-respiro para las bisagras. Acuerda con el usuario el **guion propuesto**
(formato por slide + cuáles son interactivas). Si falta contexto crítico (tema,
audiencia, número aproximado de slides), pregunta una vez con `AskUserQuestion`.
Asume defaults razonables y repórtalos.

### Paso 2: Elegir el fondo según la temática

Elige el **preset de fondo** cuya emoción encaje con el tema (catálogo §3b:
Tecnología/IA, Aqua/claridad, Energía/logros, Confianza institucional,
Cálido/humano, Sobrio). Por defecto, **difuminado azul (Tecnología/IA)**. Deriva
los blobs de **tokens de marca** (nunca inventes hex). **Díselo al usuario** y
ofrece cambiarlo.

### Paso 3: Construir el deck HTML autónomo

Un solo `.html` con todo inline (estilos, SVG, fuente, script). Aplica:

- **Tokens de marca** en `:root` + derivación oscura con la receta de
  `reference/generales/modo-oscuro.md` (§3 del doc del organismo).
- **Fondo difuminado animado** (blobs `filter:blur` con `@keyframes float`) del
  preset elegido; atenuado en oscuro (§3b).
- **Header minimalista** (sin topbar azul): **toggle de tema sol–pista–luna**
  obligatorio (átomo Interruptor; §2) + **nombre del deck** + **barra de
  progreso** superior que comunica el avance (§1.1, §1.6).
- **Slides** como `<section class="slide">` apiladas en absoluto; navegación con
  `window.go(i)`, teclado y dots; **animación de entrada escalonada por
  elemento** con `data-r`/`--i` y `prefers-reduced-motion` (§1.4). Slides-respiro
  `big-center` en las bisagras (§1.5).
- **Espacio usado con intención** (§5b): bloque en `.slide-inner` con ancho útil;
  centrado o asimétrico según lo que se vea mejor. Una lista alineada a un lado
  con aire al otro es válida; corrige solo el vacío accidental que descompensa.
- **Textos en tono SURA para presentación** (§0.2): tuteo, frase corta, aterriza
  el tecnicismo con su analogía humana, **sin mayúsculas sostenidas**, cifras con
  fuente.
- **Íconos SOLO del catálogo** para conceptos propios, **con** el transform de
  inversión al embeberlos (`translate(0,850) scale(1,-1)` en el `<path>`; §4).
  Logos de terceros permitidos solo para herramientas externas y **sin** ese
  transform (§8).
- **Scroll por slide**: las slides altas fluyen desde arriba
  (`justify-content:flex-start`), no centradas, para no solapar cajas del fondo
  (§5).

### Paso 4: Piezas interactivas y de contenido

Sigue los patrones del doc del organismo y respeta sus gotchas:

- **Mapa anatómico / diagrama de nodos** (§6): silueta acotada con `max-width`
  fijo, nodos con `anchor`/`hot`, etiquetas ordenadas por la altura corporal de
  su nodo (evita líneas cruzadas), inserción segura por profundidad de `<div>`.
- **Galería + lightbox + comparador** (§7): **fix obligatorio del iframe oculto**
  (`.lb-body [hidden]{display:none!important}`) para que el modal quede centrado;
  `.lb-stage` con `width:fit-content; margin:0 auto`.
- **Slides de contenido (mostrar, no contar)** (§7b): grilla de tarjetas con
  ícono, dos tarjetas enfrentadas (✗/✓ con alerta suave), pasos/ciclo animados,
  línea de tiempo, árbol/código anotado. Todas con hover animado y stagger.
- **Tarjetas de datos** (§9): cada cifra **cita su fuente**; matiz honesto en el
  pie; no inventes números.

### Paso 5: Verificar con navegador headless (obligatorio)

Recorre **todas** las slides con `window.go(i)` y comprueba (§10):

1. **Consola sin errores** en todo el recorrido (target `[]`).
2. **Espera a que el stagger asiente** (~≥1200 ms) antes de capturar para
   inspeccionar, o saldrá el contenido a medio aparecer.
3. **Claro y oscuro** (clic en `#tt`): contraste, íconos no invertidos, fondo del
   preset correcto y blobs atenuados en oscuro.
4. **Viewports 1440×810 y 1680×1050** (regresión de ventanas grandes: silueta que
   crece, modal que se descentra).
5. **Composición** (§5b): el espacio se usa con intención; la asimetría
   intencional es válida, solo se corrige el vacío accidental que descompensa.
6. **Interacciones**: abre el lightbox, dispara un nodo, pasa hover por una
   tarjeta, mide solapamientos con `getBoundingClientRect()` (la caja de detalle
   debe quedar **bajo** la última etiqueta).
7. **Íconos del catálogo, no placeholders** (sin cuadrados vacíos).

### Paso 5: Entregar e iterar (obligatorio)

Entrega el `.html` y **cierra ofreciendo iteración**: pide al usuario qué slide o
componente refinar (portada, un diagrama, el comparador, una cifra). El deck se
afina en rondas cortas dirigidas por el usuario, igual que GENERAR/AUDITAR.

## Guardrails

- **Cierre iterativo obligatorio (los tres modos).** Nunca des el resultado por
  terminado de forma unilateral. Al final de GENERAR, AUDITAR y PRESENTAR,
  pregunta al usuario si quiere iterar y pídele que **escriba qué revisar**
  (componentes en GENERAR/AUDITAR; slides o piezas en PRESENTAR). El refinamiento
  de marca es por componente/slide y dirigido por el usuario, en rondas cortas.
- **Íconos del catálogo embebidos: aplica el transform de inversión (PRESENTAR y
  cualquier SVG inline).** Al embeber el `<path>` de un ícono del catálogo fuera
  de su `<svg>` original (decoración dentro de otro SVG, ícono inline en una
  tarjeta del deck), **DEBES** ponerle `transform="translate(0,850) scale(1,-1)"`
  **en el `<path>`** o el ícono saldrá **boca abajo**. Los **logos de terceros**
  (GitHub, Microsoft, Google, Claude…) **no** llevan ese transform: ya vienen en
  orientación SVG estándar. Detalle en
  `reference/organismos/presentacion-interactiva.md` §4 y §8.
- **PRESENTAR: verifica con navegador headless antes de entregar.** Recorre
  **todas** las slides con `window.go(i)` recolectando errores de consola (target
  `[]`), captura **claro y oscuro**, y prueba en **1440×810 y 1680×1050** (la
  regresión de ventanas grandes revela siluetas que crecen y modales que se
  descentran). Mide solapamientos con `getBoundingClientRect()`. Detalle en
  el doc del organismo §10.
- **Íconos: SOLO los de marca. Emojis e iconografía externa están prohibidos** —
  sin excepciones, en los tres modos. Los únicos íconos admitidos son los SVG de
  `assets/icons/` (catálogo `reference/atomos/iconos-catalogo.md`). **Nunca, por
  ninguna razón**, un emoji o dingbat Unicode (`✓ ❌ ⚠ 📤 🔔 ✅ ℹ️ ▶ ●`…) —en
  markup, en `content:` de pseudo-elementos, en texto, botones, tags, toasts,
  modales o títulos— ni una librería de íconos de terceros (Font Awesome,
  Material Icons/Symbols, Bootstrap Icons, Feather, Heroicons, Lucide, Ionicons,
  Tabler, Remix, Phosphor, fuentes de íconos por CDN). En GENERAR solo se
  incrustan SVG de `assets/icons/`; si el concepto no existe, se deja placeholder
  marcado (`/* TODO: ícono de marca */`), nunca un emoji. En AUDITAR cada emoji o
  ícono externo es una desviación a corregir → reemplazar por el SVG de marca
  equivalente; si no hay, dejar pendiente. Detalle en `reference/atomos/iconos.md`
  (recuadro inicial, §7, §8).
- **Tipografía: Sura Sans es la única oficial. Barlow está prohibida** — sin
  excepciones, en los tres modos.
- **El hex manda sobre el nombre impreso.** Los valores canónicos están en
  `reference/generales/colores.md`.
- **Animación obligatoria en cambios de estado (los tres modos, ver
  `reference/auditoria.md` §4.1).** Todo componente básico al que se le pueda
  poner animación (switch, botón, radio, casilla, input, pestaña, acordeón,
  toast, cargador) **debe** animar sus transiciones de estado (hover, foco,
  activo/pressed, on↔off, selección, carga). En GENERAR se incluye
  `transition`/`@keyframes` desde el primer render; en AUDITAR un componente sin
  transición animada **es una desviación a corregir**. Respeta la duración/curva
  de la spec si la define; si no, usa ≈0.15–0.25 s con easing suave. Contempla
  siempre `@media (prefers-reduced-motion: reduce)`. No animes por adornar.
- **PRESENTAR: el deck es dinámico e interactivo por defecto.** Cada elemento y
  cada slide se anima (entrada escalonada, §1.4); se **muestra** en vez de
  **contar** (mapa de decisión §0.1: convierte listas en diagramas, comparadores,
  tarjetas, pasos, líneas de tiempo); hay **interacción real** donde aporta
  (tocar/pasar/arrastrar). Una slide que es "una lista que leería en voz alta" es
  una desviación a rediseñar. **Analiza el contenido y propón el guion** (formato
  por slide) antes de maquetar, y confírmalo con el usuario.
- **PRESENTAR: header minimalista, fondo por temática.** El header va sin color
  (toggle de tema + nombre del deck + barra de progreso superior), no topbar
  azul. El **fondo** se elige según la emoción de la temática del catálogo de
  presets (§3b), por defecto el **difuminado azul** (Tecnología/IA); los blobs se
  derivan de tokens de marca (nunca hex inventado) y se atenúan en oscuro.
  Comunica al usuario qué preset elegiste y ofrécele cambiarlo.
- **PRESENTAR: espacio usado con intención (§5b).** Cada posición se justifica y
  la slide se ve muy bien. Centrado o asimétrico (alineado a un lado con aire al
  otro) son ambos válidos — una lista a la izquierda con aire a la derecha puede
  ser la mejor opción y no se "arregla" por simetría. Corrige solo el vacío
  *accidental* que deja el contenido perdido o desequilibrado, no toda asimetría.
- **PRESENTAR: tono SURA editorial (§0.2).** Tuteo, frase corta, aterriza cada
  tecnicismo con su analogía humana, **sin mayúsculas sostenidas** para enfatizar
  (usa negrita/acento), sin tono alarmista, cifras con su fuente. En AUDITAR de
  un deck, estos defectos de texto son desviaciones a corregir (no toques nombres
  propios ni citas-ejemplo).
- Nunca inventes valores de marca que no estén en `reference/`. Si el manual aún
  no tiene una sección necesaria, dilo y marca el supuesto/pendiente.
- **Consume los assets empaquetados; no pidas cargarlos.** Íconos, fuente Sura
  Sans, logos, ilustraciones y formas viven en `assets/` dentro del skill (por
  eso el skill es pesado). Cárgalos desde ahí en GENERAR y AUDITAR. **Prohibido**
  pedirle al usuario final que suba o instale esos activos en su proyecto, o
  dejar placeholders/fuentes del sistema "provisionales" cuando el activo de
  marca ya está disponible en `assets/`.
- **Modo oscuro**: deriva la paleta oscura SOLO con la receta de
  `reference/generales/modo-oscuro.md` — único token de marca nuevo `#00003F`,
  el resto derivado de tokens existentes y verificado AA con Python. No inventes
  hex intermedios; usa opacidad de un token de marca para superficies derivadas.
- **Botón de alternancia claro/oscuro (los tres modos, obligatorio).** Si la
  interfaz no trae un control para cambiar de tema, **siempre agrégalo** (en
  GENERAR desde el primer render; en AUDITAR es una desviación a corregir).
  Prioriza un **diseño simple con íconos de marca**: sol = `assets/icons/
  brillo-alto.svg`, luna = `assets/icons/modo-oscuro.svg`. Trátalo como el átomo
  Interruptor (anatomía, estados y animación on↔off). Receta completa en
  `reference/generales/modo-oscuro.md` §7.
- **KPI / indicadores con estado**: para tarjetas que signifiquen advertencia,
  éxito o fallo, usa los **tonos suaves** de marca como fondo y el color
  semántico pleno solo para número/ícono/acento — nunca el color saturado de
  fondo. Prefiere **tarjeta modular** para tableros. Mapa y medidas en
  `reference/moleculas/tarjetas.md` §7b.
- **Prohibido dejar diálogos nativos del navegador (los tres modos).** Nunca jamás
  dejes `alert()`/`confirm()`/`prompt()`/`window.*` (ni `Notification` del SO)
  para mensajes de la app: rompen la marca y bloquean la página. Reemplázalos
  según el **contenido del mensaje**: (a) si solo **informa** algo **efímero/menor**
  (autosave, "Copiado", aviso sin hito ni decisión) → **toast** de marca;
  (b) si acusa el **éxito de una acción completada** que el usuario quiere ver
  destacada —**envío de formulario** o **solicitud generada exitosamente**— →
  **modal de confirmación de éxito con un solo botón** (`Cerrar`/`Aceptar`/
  `Continuar`/`Listo`); (c) si pide una **decisión o confirmación** → **modal base**
  de marca (confirmar derecha / descartar izquierda, cableando la lógica del
  `confirm`). En GENERAR, jamás emitas un diálogo nativo; en AUDITAR, cada uno es
  desviación a corregir conservando la funcionalidad. Tabla de decisión en
  `reference/moleculas/modales.md` §4.2.
- **Prohibido el `<select>` nativo para listas de marca (los tres modos).** El campo
  cerrado se puede maquetar, pero **la lista de opciones que despliega el navegador
  la dibuja el sistema operativo** (tipografía, resaltado azul, esquinas y sombra
  del SO) y **no respeta** los tokens de marca, sin importar el CSS aplicado.
  Sustitúyelo **siempre** por el desplegable propio basado en la molécula **Menú**:
  disparador `<button>` con apariencia de campo (`aria-haspopup="listbox"` +
  `aria-expanded`) + `<ul role="listbox">` (ítems 44–48 px, radio 12 px, opción
  activa en azul suave, elevación, apertura/cierre animados, modo oscuro,
  `<li role="option">` con `data-value`/`aria-selected`) + `<input type="hidden">`
  que conserva el valor y dispara un evento `change` burbujeante; cierre por clic
  afuera y `Esc`. En GENERAR no emitas `<select>` para listas de marca; en AUDITAR
  cada `<select>` nativo es una **desviación a corregir**, conservando la lógica
  (mismo `value`, mismo evento `change`). Anatomía y detalle en
  `reference/moleculas/campos.md` §6 «Campo con despliegue» y §9.
- **Toast y modal se superponen a pantalla completa, sin scroll (los tres modos).**
  Ambos flotan sobre el viewport con `position: fixed` y deben verse **sin que el
  usuario se desplace**: el modal con velo a pantalla completa (`inset: 0`) +
  tarjeta centrada y scroll interno si desborda (`modales.md` §4.1); el toast en
  un `#alert-container` fijo anclado al borde de la ventana (`toast.md` §4.1).
  Insertarlos en el flujo del documento es un bug de colocación. No olvides la
  **animación** de entrada/salida del toast y del modal.
- **Estados interactivos en estático**: cuando la UI tenga pestañas/pasos/
  acordeón, no muestres todos los paneles a la vez en un mismo PNG; representa
  **un estado por frame** y entrega **un PNG por estado**, desde una sola
  maquetación parametrizada por un flag de estado (ortogonal al de modo oscuro).
  Mantén fija la cromática compartida entre estados. Ninguna sección debe
  aparecer **duplicada** (p. ej. como pestaña y como tarjeta lateral a la vez).
- **Contención antes de entregar**: en mockups con coordenadas calculadas,
  verifica que ningún elemento se desborde de su contenedor (bordes inferior y
  derecho), calculando el alto del contenedor desde el contenido real. "Cabe el
  texto" no implica "cabe el elemento".
- En GENERAR: el PNG final siempre va en `output/` — confirmar con
  `Glob output/**/*` antes de reportar éxito.
- En AUDITAR: edición quirúrgica, no reescritura; no cambies funcionalidad
  (handlers, estado, rutas, data).
- Para verificar tokens calculados (ratios de contraste, tamaños relativos),
  usa Python — no calcules a mano.
- No generes imágenes fotorrealistas; este skill produce mockups de UI.

## Créditos y derechos

© Seguros SURA. Los derechos de autor de este skill y de los activos de marca
pertenecen a Seguros SURA. Desarrollado en la Dirección de Aceleración de
Capacidades por Alejandro Jimenez Zapata y Mauricio Otalvaro Ospina. Uso
restringido al ámbito interno de Seguros SURA. Ver `NOTICE` y `README.md`.
