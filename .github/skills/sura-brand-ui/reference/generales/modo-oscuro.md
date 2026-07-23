# Modo oscuro — Sistema de Diseño SURA

Toda pieza de UI (GENERAR y AUDITAR) debe contemplar modo oscuro. Esta guía
fija **cómo** derivarlo sin inventar paleta. Receta validada en producción
(ficha técnica del Marketplace, autoevaluación Junta Directiva).

---

## 1. Regla de oro: dos tokens de marca para oscuro

El modo oscuro tiene **dos** colores de marca propios:

1. **Fondo `#00003F`** (Azul oscuro, `--dark-mode-bg`, `colores.md` §4.3) —
   superficie de todos los componentes en oscuro.
2. **Acento `#E3E829`** (Amarillo alegría) — **en oscuro el amarillo deja de
   estar reservado al CTA y pasa a ser el color para RESALTAR los elementos
   interactivos** (botón primario, contorno del secundario, avatares, casillas
   de verificación, selección activa, estrellas de calificación). Lo dicen
   explícitamente `Colores.pdf` (mockup "Diálogo base" en oscuro) y
   `Botones.pdf` ("Botón Primario - Amarillo" y "Botón Secundario - Amarillo
   (Dark mode)").

**El resto se deriva** de tokens que YA existen en la paleta clara (texto y
bordes en azul foco `#81B1FF`), y cada par texto/fondo se **verifica AA con
Python sobre `#00003F`** antes de aprobarlo. No se inventan hex nuevos.

> **Reparto claro:** el azul `#81B1FF` es para **leer** (texto, enlaces,
> bordes, íconos de navegación); el amarillo `#E3E829` es para **actuar y
> resaltar** (acción primaria, selección, avatares, casillas, estrellas). No se
> mezclan roles: un enlace de texto no se vuelve amarillo, un botón primario no
> se queda azul.

---

## 2. Mapa de derivación (claro → oscuro)

Valores verificados AA sobre `#00003F`:

| Rol | Claro | Oscuro | Ratio s/ #00003F |
|---|---|---|---|
| Fondo / superficie | `#F8F8F8` / `#FFFFFF` | `#00003F` | — |
| Texto cuerpo | `#0D0D0D` | `#F8F8F8` | 18.45:1 ✅ |
| Texto secundario | `#3F3F41` | `#DFEAFF` (Fondo 4) | 16.19:1 ✅ |
| Texto muted / encabezados-en-superficie / enlaces | `#0033A0` / `#2D6DF6` | `#81B1FF` (azul foco) | 9.02:1 ✅ |
| **Acento de acción / resaltado** (botón primario, selección, avatar, casilla, estrella) | `#2D6DF6` | **`#E3E829` (Amarillo alegría)** | 14.78:1 ✅ |
| Texto sobre acento amarillo (relleno) | `#FFFFFF` | `#00003F` (navy) | 14.78:1 ✅ |
| Hover del acento amarillo | — | `#C9CE12` (Amarillo oscuro/oliva) | 11.5:1 ✅ |
| Barra superior de identidad (no es contenido) | `#2D6DF6` | `#2D6DF6` (se mantiene) | — |
| Borde / divisor | `#E7E7E7` | `#81B1FF` @ ~0.30 op | — |

> El azul profundo `#0033A0` hardcodeado **falla** sobre oscuro (≈1.85:1). En
> oscuro, todo **texto/ícono de lectura o navegación** que en claro era
> `#0033A0` o `#2D6DF6` **sobre superficie** se reasigna a `#81B1FF`. En cambio,
> todo lo que sea **acción primaria, selección o resaltado** (no texto de
> lectura) se reasigna a **`#E3E829`** con texto navy `#00003F` encima.

---

## 3. Separar "encabezado-en-superficie" de "texto-en-chip-autocontenido"

El error clásico es voltear **todos** los azules a la vez. Hay que separarlos:

- **HEAD / LINK / NOTE** = texto, encabezados, enlaces e íconos que viven
  **directamente sobre la superficie**. En oscuro → `#81B1FF`.
- **Chips autocontenidos** = elementos con su **propio fondo claro** (chip
  FONDO `#DFEAFF`, chip éxito `#DEF6DE`, círculos de avatar con iniciales,
  encabezado de tabla sobre FONDO). Su texto azul profundo `#0033A0`
  **NO se cambia**: el fondo del chip sigue claro en ambos temas, así que el
  par texto/fondo del chip ya pasa AA por sí mismo.

Por eso el código debe tener **tokens distintos** para "azul sobre superficie"
(HEAD/LINK) y "azul sobre chip claro" (se queda PROF). Nunca un swap global.

---

## 4. Tokens de opacidad (en vez de hex nuevos)

Para superficies derivadas en oscuro, usa el token de marca con **opacidad** en
lugar de inventar un hex intermedio:

| Token | Claro | Oscuro |
|---|---|---|
| `CARDSTROKE` (borde tarjeta) | `#E7E7E7` opaco | `#81B1FF` @ 0.30 |
| `ZEBRA` (fila alterna) | `#F4F4F4` opaco | `#81B1FF` @ 0.08 |
| `CHIPBG` (chip tenue) | `#F4F4F4` opaco | `#81B1FF` @ 0.15 |
| `DIV` (divisor / hline) | `#E7E7E7` opaco | `#E7E7E7` @ 0.30 |
| `OVERLAY` (velo de modal) | `#0033A0` @ 0.10 | `#000000` @ 0.45 |
| `SHADOW` (sombra/elevación) | `#0033A0` @ 0.06 | `#000000` @ 0.40 |

El chip tenue (`CHIPBG`) en oscuro queda como azul foco al 15 % sobre `#00003F`
(≈`#131B5C`); su texto `#DFEAFF` da 12.96:1 ✅.

---

## 5. Qué se mantiene idéntico y qué cambia entre temas

**Se mantiene idéntico:**
- **Barra superior azul** (`#2D6DF6` con logo y texto blancos): igual en claro y
  oscuro. Es identidad, no superficie de contenido; su avatar va en círculo
  blanco con iniciales azules ("color alternativo").
- **Tags semánticos autocontenidos** (éxito verde `#DEF6DE`, advertencia
  `#FFF5EC`): conservan su color en ambos temas.

**Cambia en oscuro (clave de esta guía):**
- **Botón primario:** en claro es azul `#2D6DF6` + texto blanco; en **oscuro es
  Amarillo alegría `#E3E829` + texto navy `#00003F`** (hover Amarillo oscuro
  `#C9CE12`). Ya **no** se queda azul.
- **Botón secundario (contorno):** en claro es contorno azul; en **oscuro es
  contorno + texto amarillo `#E3E829`**.
- **Avatares sobre superficie, casillas de verificación, indicador de
  selección/pestaña activa y estrellas de calificación:** en oscuro usan el
  acento **amarillo** en lugar del azul. En la **pestaña activa** el amarillo va
  en **etiqueta + indicador unificados** (no solo el subrayado): si la letra se
  queda azul `#81B1FF` no se distingue de las inactivas, que ya son ese mismo
  azul. Spec del componente en `moleculas/pestanas.md` §4.bis.
- **El amarillo ya NO está reservado solo al CTA en oscuro** — es el color
  general de resaltado interactivo (ver §1).

### 5.bis Modales y diálogos en oscuro (homologación)

El **modal** en oscuro **no es una construcción aparte**: se deriva de los mismos
tokens de esta guía. La lámina *Modales* lo confirma (su panel "Modo oscuro
activado" muestra fondo navy + botón de acción amarillo). Para mantener un único
estilo de interfaz en oscuro:

- **Superficie de la tarjeta del modal** → `#00003F` (igual que cualquier
  superficie en oscuro, §1). El hex `#00003F`/`#00003F` muestreado en la lámina es
  el mismo token de fondo.
- **Botón de acción del modal** → **acento amarillo `#E3E829`** con texto navy
  `#00003F` (la lámina lo muestrea como `#E2E828`, misma Amarillo alegría con
  variación de muestreo; usar el canónico `#E3E829`). El secundario, contorno
  amarillo.
- **Velo / overlay** → token `OVERLAY` oscuro `#000000 @ 0.45` (§4), nunca el azul
  claro del tema claro.
- **Tipografía** del modal en oscuro: título 22 px Bold, cuerpo 16 px (web) —
  geometría idéntica al claro; solo cambian los tokens de color.

> Misma lógica para **toasts** y demás superficies emergentes: fondo `#00003F`,
> acento de acción amarillo, texto de lectura `#81B1FF`, chips semánticos
> autocontenidos intactos. Así toda capa superpuesta comparte el estilo oscuro.

---

## 6. Implementación

- **Una sola maquetación** parametrizada por un flag (`data-theme="dark"` en
  HTML/CSS; un argumento `dark` en un generador por script). Misma geometría,
  solo cambian los tokens. Así un arreglo de layout sirve para ambos temas.
- En HTML: tokens en `:root[data-theme="dark"]` + un script en `<head>` que fija
  el tema antes de pintar (preferencia guardada o `prefers-color-scheme`).
- **Verificación AA obligatoria con Python** de cada par texto/fondo sobre
  `#00003F` antes de entregar. Cuerpo/UI ≥4.5:1; gráficos/acentos ≥3:1.

---

## 7. Botón de alternancia claro/oscuro — OBLIGATORIO

Si la interfaz **no trae** un control para cambiar de tema, **siempre se agrega**
(en GENERAR desde el primer render; en AUDITAR es una desviación a corregir). Se
prioriza un **diseño simple con los íconos de marca**:

- **Íconos de marca** (no dibujar ni usar íconos ajenos):
  - Claro → ícono **`brillo-alto.svg`** (sol) en `assets/icons/`.
  - Oscuro → ícono **`modo-oscuro.svg`** (luna) en `assets/icons/`.
  - Inyecta el SVG y sustituye `currentColor` por el token de color del tema.
- **Patrón funcional = átomo Interruptor.** El alternador de tema **es** el átomo
  Interruptor (`atomos/interruptores.md`), no un botón ad-hoc: respeta su
  anatomía, sus estados y su **animación** de transición on↔off (ver
  `auditoria.md` §4.1; ≈0.15–0.25 s, con `prefers-reduced-motion`).
- **Diseño simple, no decorativo:** un solo control compacto que muestre el ícono
  del tema **destino** (o el actual, de forma consistente). Sin etiquetas largas;
  si hay texto, "Claro/Oscuro" ≤8 caracteres. Ubicación típica: barra superior
  derecha o el menú de usuario.
- **Color del control:** sigue los tokens del tema activo. Sobre la barra azul
  (`#2D6DF6`) el ícono va en blanco; sobre superficie clara, en `#0033A0`; sobre
  superficie oscura, en `#81B1FF`.
- **Comportamiento:** alterna `data-theme` y persiste la preferencia; el estado
  inicial respeta `prefers-color-scheme`. No cambies la geometría de la página al
  alternar — misma maquetación, solo cambian los tokens (§6).

## 8. Checklist de entrega (oscuro)

1. ¿Tokens de marca de oscuro = `#00003F` (fondo) + `#E3E829` (acento)? (lo demás derivado) ✅
2. ¿Azules de lectura/navegación sobre superficie → `#81B1FF`, chips autocontenidos intactos? ✅
3. ¿**Acción primaria, selección, avatar, casilla y estrella → amarillo `#E3E829`** con texto navy encima? ✅
4. ¿Superficies derivadas con opacidad de token, no hex inventados? ✅
5. ¿Barra de identidad azul igual en ambos temas, pero botón primario **amarillo** en oscuro (no azul)? ✅
6. ¿Todos los pares texto/fondo verificados AA con Python sobre `#00003F` (amarillo da 14.78:1)? ✅
7. ¿Hay botón de alternancia claro/oscuro con íconos de marca (sol/luna) si la
   interfaz no lo traía, animado y tratado como átomo Interruptor? ✅
