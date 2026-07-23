# Menú navegador (Navbar) — organismo

Fuente: `Menú navegador.pdf` (varias páginas). Verificado contra imágenes renderizadas
y muestreo de píxeles. **Tipografía: Sura Sans. No aparece Barlow.**

## 1. Qué es

El menú navegador (también conocido como **barra de navegación** o **menú de
navegación**) es la sección de una página web que contiene los **enlaces a otras
secciones del sitio**. Suele ubicarse en la **parte superior** de la página y
proporciona una forma clara y organizada de acceder a las diferentes páginas o
secciones. Al hacer clic en un enlace, el usuario es redirigido a la página
correspondiente.

## 2. Anatomía

1. **Barra de herramientas de accesibilidad y línea de negocio** (barra superior
   delgada: *Ley de transparencia · Accesibilidad* + ícono de accesibilidad).
2. **Barra primaria de navegación** (logo SURA, pastilla *Productos ▲*, enlaces
   EPS / ARL / IPS / Ayudas Diagnósticas, ícono de búsqueda, Pago Express, botón
   amarillo *Iniciar sesión*).
3. **Despliegue de contenido** (mega-menú: *¿Qué quieres proteger?* → Muévete,
   Habita, Conéctate, Se saludable, Se relevante, Decide).
4. **Descriptor de entorno corporativo** (franja azul oscuro *SEGUROS*; también
   EPS / ARL).

## 3. Construcción por dispositivo

### Menú desplegado escritorio
| Elemento | Medida |
|---|---|
| Ancho de canvas | **1440 px** |
| Barra de accesibilidad (alto) | **48 px** |
| Barra primaria de navegación (alto) | **96 px** |
| Descriptor *SEGUROS* (alto) | **48 px** |
| Márgenes del mega-menú | **156 px** |
| Columnas del mega-menú | **350 px** |
| Gutters (espaciado entre columnas) | **36 px** |
| Tamaño **máximo** de la imagen | **360 × 360 px** |
| Ancho de contenido (texto) | **300 px** |

### Menú desplegado tablet
| Elemento | Medida |
|---|---|
| Ancho | **768 px** |
| Márgenes | **24 px** |
| Barra de accesibilidad (alto) | **40 px** |
| Barra primaria de navegación (alto) | **96 px** |
| Descriptor *SEGUROS* (alto) | **40 px** |
| Separación entre barras | **24 px** |

- El menú se **colapsa en acordeones** (Productos → Muévete → *Plan muévete libre /
  Plan utilitarios y pesados / Seguro de autos / Seguro de bicis y patinetas /
  Seguro SOAT*, etc.). Aparece el botón **hamburguesa** junto a *Iniciar sesión*.

### Menú desplegado móvil
| Elemento | Medida |
|---|---|
| Ancho | **390 px** |
| Márgenes | **24 px** |
| Barra de accesibilidad (alto) | **40 px** |
| Descriptor *SEGUROS* (alto) | **40 px** |
| Separación entre barras | **16 px** |

- Acordeones apilados; barra primaria con logo SURA + avatar + **hamburguesa**.

### Botón *Iniciar sesión*
| Contexto | Tamaño de botón | Jerarquía | Color |
|---|---|---|---|
| Escritorio / tablet | **Mediano** | Primario | Amarillo alegría `#E3E829` |
| Móvil | **Icónico_pq** | Primario | Amarillo alegría `#E3E829` |

- Menú hamburguesa (móvil): espaciados **24 / 6 px**, caja **32 px**.

## 4. Panel navegador lateral (Logueado)

La navegación lateral permite a los usuarios navegar por **todo el contenido de un
producto o sección**. Se puede usar para navegación de **un solo nivel o de varios
niveles**. Se despliega a la derecha al **iniciar sesión**.

**Anatomía:** avatar + *Nombre Apellido* + *Bajada de texto* + botón de cierre `×`;
lista de **Elementos** con íconos; al pie, **iconos sociales** (Facebook, LinkedIn,
Twitter) + **Cerrar sesión**.

**Niveles:**
- **Primer nivel:** lista de elementos de primer nivel (chevron `▾` para los que
  despliegan hijos).
- **Segundo nivel:** *Elemento Padre* resaltado (`▴`) → *Elemento hijo* ×N.
- **Tercer nivel:** cabecera *← Elemento Hijo desplegado*; los elementos pueden
  llevar controles (radio, casilla, interruptor, chevron `›`).

## 4.1 Cabecera de aplicación (app-shell) con sesión iniciada

Variante interna válida del navbar para **aplicaciones de negocio** (no marketing):
barra superior blanca fija con logo a la izquierda, título de la app y, a la
derecha, el **bloque de usuario logueado** (nombre + bajada + avatar). Es el patrón
del SIA y de cualquier herramienta interna con sesión. No reemplaza el navbar de
3 barras (§2) del sitio público; es su contraparte de producto.

**Reglas verificadas (no las repitas mal al generar):**

1. **Color del logo por fondo (logo.md §7).** El logo se recolorea según el fondo,
   **no** se deja en Azul profundo:
   - Fondo claro (barra blanca) → variante **full-azul `#2D6DF6`** (Azul Cielo
     Latino). No uses `#0033A0`.
   - Fondo oscuro (modo oscuro `#00003F`) → variante **negativo `#FFFFFF`**.
   - Contraste verificado: `#2D6DF6` sobre blanco = 4.54:1; `#FFFFFF` sobre
     `#00003F` = 19.59:1.
2. **Avatar = combo Inicial (avatar.md §4).** Solo hay dos combos válidos; en la
   cabecera usa **círculo `#2D6DF6` (PRIM) + iniciales `#E3E829` (CTA)**. Nunca
   fondo `#DFEAFF` + texto `#0033A0` ni otras mezclas. Tamaños por avatar.md §5
   (56px→texto 22, 40px→18, 24–32px→14). Iniciales en Seminegrita/Bold.
   Contraste CTA sobre PRIM = 3.42:1 (cumple 3:1 de componente UI).
3. **Nombre = primer nombre + primer apellido (avatar.md §7).** No el nombre
   completo. Truncar con elipsis si supera ~20 caracteres
   ("Alejandro Jimenez Zapata" → "Alejandro Jimenez").
4. **La bajada bajo el nombre NUNCA usa el color de enlace/primario.** El rol,
   cargo o estado (p. ej. "Administrador") debe ir en **texto secundario**
   (`#3F3F41` claro / `#DFEAFF` oscuro), no en el azul de enlace `#2D6DF6`/`#81B1FF`.
   Razón: el azul de enlace comunica *afordancia de clic*; un texto descriptivo
   que no es accionable pintado de azul promete una interacción que no existe
   (falsa afordancia). Solo va en azul de enlace lo que de verdad navega o acciona.
5. **Tamaños tipográficos a la escala (tipografia.md).** Nombre y bajada al
   escalón de **subtítulo/caption (14px)**; no uses tamaños sueltos como 15/13.
   El título de la app puede subir (p. ej. 18px/700) respetando la jerarquía.

**Anatomía (izquierda → derecha):** logo (recoloreado por fondo) · título de la
app · *(flexible)* · nombre (primer nombre + primer apellido) sobre bajada
secundaria · avatar Inicial (PRIM + CTA). El bloque de usuario se alinea a la
derecha; el avatar abre el panel lateral logueado (§4).

## 5. Colores

| Rol | Nombre | Hex |
|---|---|---|
| Barra de accesibilidad (fondo) | Lavanda claro | `#DFE9FF` (muestreo `(223,233,255)`) |
| Barra primaria de navegación (fondo) | Azul Vivo SURA | `#2D6DF6` (muestreo `(45,109,246)`) |
| Pastilla *Productos* (fondo) | Azul SURA | `#0033A0` (muestreo `(0,51,160)`) |
| Descriptor *SEGUROS* (fondo) | Azul SURA | `#0033A0` (muestreo `(0,51,160)`) |
| Botón *Iniciar sesión* | Amarillo alegría | `#E3E829` (render `(226,232,40)` ≈ `#E2E828`) |
| Texto sobre barra azul / descriptor | Blanco Puro | `#FFFFFF` |
| Texto de enlaces del mega-menú / panel lateral | Azul Vivo / Azul SURA | `#2D6DF6` / `#0033A0` |

## 6. Uso

- Ubicar **en la parte superior** de la página; jerarquía de tres barras
  (accesibilidad → primaria → descriptor).
- **Un solo menú navegador** por página, fijo arriba.
- En tablet/móvil, **colapsar** la navegación en acordeones + botón hamburguesa.
- El botón *Iniciar sesión* es **primario amarillo**; al loguearse se reemplaza por
  el avatar que abre el **panel lateral**.
- Mantener contraste suficiente del texto blanco sobre las barras azules (WCAG).

## 7. Tokens CSS

```css
:root {
  /* Escritorio */
  --nav-w: 1440px;
  --nav-access-h: 48px;       /* barra accesibilidad */
  --nav-primary-h: 96px;      /* barra primaria */
  --nav-descriptor-h: 48px;   /* franja SEGUROS */
  --nav-megamenu-margin: 156px;
  --nav-megamenu-col: 350px;
  --nav-megamenu-gutter: 36px;
  --nav-megamenu-img-max: 360px;   /* 360 × 360 */
  --nav-megamenu-content-w: 300px;

  /* Tablet */
  --nav-tablet-w: 768px;
  --nav-tablet-margin: 24px;
  --nav-tablet-access-h: 40px;
  --nav-tablet-primary-h: 96px;
  --nav-tablet-descriptor-h: 40px;
  --nav-tablet-gap: 24px;

  /* Móvil */
  --nav-mobile-w: 390px;
  --nav-mobile-margin: 24px;
  --nav-mobile-access-h: 40px;
  --nav-mobile-descriptor-h: 40px;
  --nav-mobile-gap: 16px;

  /* Colores */
  --nav-access-bg: #DFE9FF;   /* barra accesibilidad lavanda */
  --nav-primary-bg: #2D6DF6;  /* barra primaria Azul Vivo */
  --nav-pill-bg: #0033A0;     /* pastilla Productos */
  --nav-descriptor-bg: #0033A0; /* franja SEGUROS */
  --nav-login-btn: #E3E829;   /* Amarillo alegría (render #E2E828) */
  --nav-text-on-blue: #FFFFFF;

  --font-nav: 'Sura Sans', 'Helvetica Neue', Arial, sans-serif;
}
```

## 8. Reglas operativas para el skill

- Menú navegador = **3 barras** apiladas: accesibilidad (lavanda `#DFE9FF`) +
  primaria (Azul Vivo `#2D6DF6`, con logo, pastilla *Productos* `#0033A0`, enlaces,
  búsqueda, Pago Express y botón amarillo *Iniciar sesión*) + descriptor *SEGUROS*
  (Azul SURA `#0033A0`).
- Escritorio: canvas 1440; alturas 48 / 96 / 48; mega-menú márgenes 156, columnas
  350, gutter 36, imagen máx 360×360, contenido 300.
- Tablet: 768, márgenes 24, alturas 40 / 96 / 40, gap 24; **acordeones** +
  hamburguesa. Móvil: 390, márgenes 24, alturas 40 / — / 40, gap 16; acordeones
  apilados + hamburguesa.
- Botón *Iniciar sesión* = primario amarillo `#E3E829` (render `#E2E828`); Mediano en
  escritorio/tablet, Icónico_pq en móvil.
- **Panel navegador lateral (Logueado)**: panel derecho con avatar + Nombre Apellido
  + bajada + lista de elementos + iconos sociales + Cerrar sesión; **3 niveles**
  (primer nivel, segundo nivel con Elemento Padre, tercer nivel con controles).
- Un solo menú por página, fijo arriba; texto blanco sobre barras azules (WCAG).
- Tipografía Sura Sans; **nunca Barlow**.

## 9. Pendiente

- [ ] Confirmar el hex exacto del amarillo del botón: impreso `#E3E829` (Amarillo
      alegría) vs. render `(226,232,40)` ≈ `#E2E828` (diferencia mínima).
- [ ] Confirmar medidas internas del panel lateral logueado (ancho del panel, alto
      de fila de *Elemento*, padding) — no impresas en hex/px en las láminas.
- [ ] Confirmar tamaños de fuente de enlaces de la barra primaria y del mega-menú
      (px no impreso).
