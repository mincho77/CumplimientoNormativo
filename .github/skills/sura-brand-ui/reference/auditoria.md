# Modo AUDITAR — Ajustar código existente a la marca SURA

Flujo para tomar código **ya escrito** (HTML, CSS/SCSS, JSX/TSX, Vue, Angular,
styled-components, Tailwind, etc.) y ajustarlo para que cumpla el sistema de
diseño de Seguros SURA. No reescribe la app: detecta lo que se sale de la marca,
lo corrige in situ y entrega un reporte de cambios.

> **Tipografía: Sura Sans es la única oficial. Barlow está prohibida** — sin
> excepciones. Cualquier `Barlow` en el código es un error a corregir.
> **El hex manda, no el nombre:** los valores canónicos están en
> `reference/generales/colores.md`.

---

## 1. Flujo de auditoría (orden fijo)

1. **Recibir el código.** Si el usuario pega un fragmento, trabájalo tal cual. Si
   señala un archivo (`input/…`, ruta del workspace, adjunto), léelo con `Read`.
   Si son varios archivos, audítalos todos pero reporta por archivo.
2. **Inventariar los componentes** (paso obligatorio, ver §3.0). Antes de mirar
   tokens sueltos, enumera **cada componente** con el que se construyó la UI
   (switch, botón, input, tarjeta, toast, tabla, pestañas, modal, etc.) y mapea
   cada uno a su spec en `reference/atomos|moleculas|organismos/`. Un patrón
   funcional (p. ej. un alternador de tema) **es** un componente de marca (el
   átomo Interruptor), no un elemento ad-hoc: hay que reconstruirlo según su
   spec, no aproximarlo con CSS genérico.
3. **Inventariar desviaciones.** Recorre el código buscando las 5 categorías de
   §3 (tipografía, color, radio, elevación, espaciado) más estados/accesibilidad
   (§4). Para cada componente del paso 2, contrasta su anatomía, medidas, estados
   y tokens contra su archivo de spec. Anota cada hallazgo con su ubicación
   (línea/selector/propiedad).
4. **Mapear** cada desviación al token de marca correcto usando §2 y las
   referencias de `reference/`. Si un valor no tiene equivalente claro, **no lo
   inventes** — márcalo como pendiente (§7).
5. **Corregir** editando el código con `Edit` (cambios quirúrgicos, no reescritura
   total). Preserva estructura, nombres, lógica y funcionalidad. Solo cambia lo
   que afecta el cumplimiento de marca.
6. **Reportar** con el formato de §6: tabla de cambios (antes → después → porqué)
   + pendientes + cómo verificar. Incluye la tabla de cobertura por componente
   (§3.0).
7. **Verificar** ratios de contraste con Python cuando cambies un par
   texto/fondo (§4). No calcules a mano.

**Regla de oro:** ante la duda entre dos tokens, elige por *rol* (¿es primario?
¿secundario? ¿fondo? ¿alerta?) antes que por cercanía de hue. Si el rol no es
claro, deja pendiente y pregunta.

---

## 2. Tabla de mapeo — valor fuera de marca → token correcto

Los hex de destino son canónicos (`colores.md`). La columna "se reconoce por" da
patrones típicos que verás en código ajeno. **No es una lista cerrada:** cualquier
color que no esté en la paleta SURA es candidato a mapeo por rol/hue.

### 2.1 Tipografía

| Se reconoce por | Acción | Destino |
|---|---|---|
| `font-family: Barlow`, `'Barlow'`, `Barlow, …` | **Reemplazar siempre** | `'Sura Sans', 'Helvetica Neue', Arial, sans-serif` |
| `Roboto`, `Arial`, `Helvetica`, `Open Sans`, `Inter`, `system-ui`, `-apple-system`, `sans-serif` suelto como familia principal | Reemplazar | `'Sura Sans', 'Helvetica Neue', Arial, sans-serif` |
| No hay `@font-face` de Sura Sans pero se usa la familia | Añadir `@font-face` desde `assets/fonts/` (ver `reference/generales/tipografia.md`) | family name: `Sura Sans` |
| Pesos/tamaños arbitrarios | Validar contra la escala de `tipografia.md` | tokens `--font-*` |

> El family name real del asset es **`Sura Sans`**. Mantén siempre el fallback
> `'Helvetica Neue', Arial, sans-serif` por si el entorno no resuelve la fuente.

### 2.2 Color — por rol

| Rol detectado (se reconoce por) | Token destino | Hex |
|---|---|---|
| Azul de marca / CTA primario (`#1976d2`, `#007bff`, `#2196f3`, azules genéricos de botón/enlace) | `--color-primary` | `#2D6DF6` |
| Azul oscuro / secundario / hover del botón azul | `--color-secondary` (`--btn-primary-hover`) | `#0033A0` |
| Amarillo de acento / CTA amarillo | `--color-accent-yellow` | `#E3E829` |
| Hover del botón amarillo/CTA | `--btn-cta-hover` | `#C5CB15` |
| Aqua / turquesa de acento | `--color-accent-aqua` | `#00AEC7` |
| Gris de texto secundario / neutro | `--color-neutral` | `#888B8D` |
| Texto principal / cuerpo (negros o grises muy oscuros: `#000`, `#212121`, `#222`) | `--gray-900` o `--color-secondary` para texto azul corporativo | `#0D0D0D` / `#0033A0` |
| Fondos de pantalla/sección claros (`#fafafa`, `#f5f5f5`, `#eee`) | uno de `--bg-1…5` | `#E5E9EA` `#F9FAE1` `#E6FAEF` `#DFEAFF` `#F8F8F8` |
| Bordes/divisores gris claro | `--gray-200` / `--gray-100` | `#E7E7E7` / `#F4F4F4` |
| Modo oscuro (fondo) | `--dark-mode-bg` | `#00003F` |

### 2.3 Color — alertas (uso exclusivo Toast / Tags / error)

| Estado (se reconoce por) | Principal | Fondo suave |
|---|---|---|
| Éxito / success / verde (`#4caf50`, `#28a745`) | `--alert-success` `#067014` | `--alert-success-bg` `#DEF6DE` |
| Advertencia / warning / naranja (`#ff9800`, `#ffc107`) | `--alert-warning` `#ED8B00` | `--alert-warning-bg` `#FFF5EC` |
| Error / danger / rojo (`#f44336`, `#dc3545`) | `--alert-error` `#D12D35` | `--alert-error-bg` `#FFF4F3` |
| Información / info (azul de aviso) | `--alert-info` `#0033A0` | `--alert-info-bg` `#E0EAFF` |

> ⚠ Estos 8 colores **solo** valen en Toast, Tags y variantes de error. Si los ves
> usados como fondo decorativo o color de marca general, eso también es una
> desviación: reubícalos al token de rol correcto de §2.2.

### 2.4 Borde redondeado (ver `reference/generales/borde-redondeado.md`)

Escala permitida: **8 / 12 / 16 / 24 px**. Nunca valores intermedios (no 10, 14,
20). Botones = píldora (`height / 2`). Tope de 24 px para contenedores.

| Se reconoce por | Acción | Destino |
|---|---|---|
| `border-radius: 4px / 6px / 10px` | Subir/bajar al escalón válido más cercano | `--radius-sm` 8px |
| `border-radius: 14px / 20px` | Ajustar al escalón | `--radius-md` 12px / `--radius-lg` 16px |
| `border-radius: 32px+` en contenedor | Capar a 24 px | `--radius-xl` 24px |
| Botón con radio fijo que no es altura/2 | Recalcular | `calc(height / 2)` |

### 2.5 Elevación / sombra (ver `reference/generales/elevaciones.md`)

| Uso (se reconoce por) | Token | Valor |
|---|---|---|
| Card en reposo | `--elevation-dp1` | `0 1px 2px rgba(0,0,0,0.06)` |
| Botón / input | `--elevation-dp2` | `0 2px 4px rgba(0,0,0,0.08)` |
| Hover de card/botón | `--elevation-dp3` | `0 4px 8px rgba(0,0,0,0.10)` |
| Dropdown / tooltip / popover | `--elevation-dp4` | `0 8px 16px rgba(0,0,0,0.12)` |
| Modal / drawer / diálogo | `--elevation-dp5` | `0 16px 32px rgba(0,0,0,0.16)` |

Sombras arbitrarias (`box-shadow: 0 0 10px gray`, etc.) → mapear al `dp` del rol.

### 2.6 Espaciado (ver `reference/generales/grillas.md`)

Valida paddings/margins/gaps contra la grilla del manual. Valores fuera de la
escala se redondean al múltiplo válido más cercano. Si `grillas.md` no fija un
valor exacto para el caso, deja pendiente en lugar de inventar.

---

## 3.0 Auditoría por componente (paso obligatorio)

Antes del checklist transversal de §3, **enumera cada componente** con el que se
construyó la UI y audítalo contra **su propia spec** en `reference/`. El checklist
de tokens (§3) atrapa desviaciones sueltas; este paso atrapa el error más caro:
un componente reinventado a mano que *parece* funcionar pero no es el átomo/molécula
de marca (anatomía, medidas, estados o comportamiento equivocados).

**Método:**

1. **Detecta el rol funcional** de cada bloque de UI, no su markup. Un `<button>`
   con un círculo que se desliza **es** el átomo Interruptor, aunque el código lo
   llame `theme-toggle`. Una caja que aparece y desaparece con un mensaje **es** el
   Toast. Un `<div class="pill">` clickeable que cambia de color **es** un Botón.
2. **Mapea cada componente a su archivo de spec** (tabla abajo) y léelo.
3. **Compara contra la spec completa**, no solo color/tipografía: anatomía y
   medidas (tamaños, radios, separaciones), **todos los estados** (reposo, hover,
   foco, activo, deshabilitado, on/off), comportamiento (animación, etiqueta,
   accesibilidad/ARIA) y los tokens nombrados de esa spec. **"Todos los estados"
   incluye la animación de la transición entre ellos** (§4.1): un componente
   básico que cambia de estado sin animarlo está incompleto, aunque sus colores y
   medidas sean correctos. Anótalo como desviación con su fila en la cobertura.
4. **Si un componente no existe en `reference/`**, no lo inventes: déjalo como
   pendiente (§7) y audítalo solo con las reglas transversales (§2–§4).
5. **Reporta una fila por componente** en la tabla de cobertura (§6).

**Mapa rol → spec (no exhaustivo; el rol manda sobre el nombre de la clase):**

| Rol funcional en la UI | Spec a consultar |
|---|---|
| Alternador on/off, switch, theme-toggle | `atomos/interruptores.md` |
| Botón / CTA / pill clickeable | `atomos/botones.md` |
| Radio, opción única, escala Likert | `atomos/radios.md` |
| Casilla / checkbox | `atomos/casilla-de-verificacion.md` |
| Slider / selector de rango | `atomos/selector-de-rango.md` |
| Stepper numérico | `atomos/input-stepper.md` |
| Spinner / cargador | `atomos/cargador.md` |
| Avatar | `atomos/avatar.md` |
| Migas de pan / breadcrumb | `atomos/miga-de-pan.md` |
| Ícono | `atomos/iconos.md` (+ catálogo) |
| Input / textarea / campo de texto | `moleculas/campos.md` |
| Tarjeta / card | `moleculas/tarjetas.md` |
| Toast / alerta flotante | `moleculas/toast.md` |
| `alert()`/`confirm()`/`prompt()` nativos | → reemplazar según contenido: info efímera → `moleculas/toast.md`; **éxito de acción completada (formulario enviado / solicitud generada)** → modal de éxito de un botón `moleculas/modales.md` §4.2; decisión → modal base `moleculas/modales.md` §4.2 |
| Etiqueta / tag / chip | `moleculas/etiqueta.md` |
| Pestañas / tabs | `moleculas/pestanas.md` |
| Acordeón | `moleculas/acordeon.md` |
| Tooltip | `moleculas/tooltip.md` |
| Buscador | `moleculas/buscador.md` |
| Paginador | `moleculas/paginador.md` |
| Menú | `moleculas/menu.md` |
| Lista | `moleculas/lista.md` |
| Paso a paso / stepper de flujo | `moleculas/paso-a-paso.md` |
| Modal / diálogo / drawer | `moleculas/modales.md` |
| Carrusel | `moleculas/carrusel.md` |
| Tabla | `organismos/tablas.md` |
| Footer | `organismos/footer.md` |
| Barra/menú de navegación, header | `organismos/menu-navegador.md` |
| Banner | `organismos/banners.md` |

> **Lección fija (no la olvides):** un alternador de tema claro/oscuro NO es un
> control ad-hoc. Es el átomo Interruptor: pista 40×24 (radio 12), pulgar 16px
> blanco, etiqueta a la izquierda (16px de separación), on `#2D6DF6` / hover
> `#0033A0`, foco halo `#DFEAFF`, off track `#E5E9EA` con borde. Si lo ves
> construido como pill traslúcido o con colores genéricos, recompónlo según
> `atomos/interruptores.md`.

> **Lección fija — el azul de enlace es una promesa de clic.** El color primario/
> enlace (`#2D6DF6` claro, `#81B1FF` oscuro) solo va en texto que **navega o
> acciona**. Texto descriptivo no accionable (cargo, rol, estado, bajada bajo un
> nombre, metadato) pintado de azul de enlace es **falsa afordancia**: prometes una
> interacción inexistente. Mándalo a texto secundario (`#3F3F41` / `#DFEAFF`). Esto
> aplica en cualquier componente, no solo en la cabecera.

> **Lección fija — nunca un diálogo nativo del navegador.** Un `alert()`/`confirm()`/
> `prompt()` (o `window.*`) muestra `localhost dice…`, tipografía del SO y cero
> marca: **siempre** es desviación a corregir. Reemplázalo según el contenido del
> mensaje: (a) si solo **informa** algo **efímero/menor** (autosave, "Copiado") →
> **toast**; (b) si acusa el **éxito de una acción completada** que el usuario quiere
> ver destacada (**formulario enviado**, **solicitud generada**) → **modal de
> confirmación de éxito con un solo botón** (`Cerrar`/`Aceptar`/`Continuar`/`Listo`);
> (c) si pide una **decisión/confirmación** → **modal base** (botones confirmar
> derecha / descartar izquierda), cableando la lógica del `confirm`. Los tres se
> superponen a pantalla completa y se ven **sin scroll** (`modales.md` §4.1,
> `toast.md` §4.1).

> **Lección fija — SOLO íconos de marca, jamás emojis ni iconografía externa.**
> El único origen válido de íconos es `assets/icons/` (catálogo
> `iconos-catalogo.md`). Cualquier **emoji o dingbat Unicode** (`✓ ❌ ⚠ 📤 🔔 ✅
> ℹ️ ▶ ●`…) —en markup, en `content:` de un pseudo-elemento, en texto, botones,
> tags, toasts o títulos— y cualquier **librería de íconos de terceros** (Font
> Awesome, Material Icons/Symbols, Bootstrap Icons, Feather, Heroicons, Lucide,
> Ionicons, Tabler, Remix, Phosphor, fuentes de íconos por CDN) **es una
> desviación a corregir**: se reemplaza por el SVG de marca equivalente del
> catálogo. Si no hay equivalente, se deja **pendiente** (`/* TODO: ícono de
> marca */`) — **nunca** se conserva el emoji ni el ícono ajeno. Sin excepciones.
> Ver `atomos/iconos.md` (recuadro inicial, §7, §8).

---

## 3. Qué buscar al inventariar (checklist)

- [ ] **Cada componente** mapeado a su spec (§3.0) y auditado contra ella —
      anatomía, medidas y **todos** sus estados, no solo color/tipografía.
- [ ] **Emojis / dingbats Unicode o íconos de librería externa** usados como
      íconos (`✓ ❌ ⚠ 📤 🔔 ✅ ℹ️ ▶ ●`…; `<i class="fa…">`, `material-icons`,
      Bootstrap Icons, Feather, Heroicons, Lucide…): **siempre** desviación a
      corregir → reemplazar por el SVG de marca equivalente de `assets/icons/`
      (`atomos/iconos.md`, recuadro inicial). Si no hay equivalente, dejar
      pendiente con placeholder marcado, nunca conservar el emoji/ícono ajeno.
- [ ] `font-family` ≠ Sura Sans en cualquier selector o prop (prioridad máxima: Barlow).
- [ ] Colores **hardcodeados** (hex, `rgb()`, `hsl()`, nombres CSS como `blue`)
      que deberían ser un token de marca.
- [ ] Colores de marca correctos pero **escritos como literal** en vez de variable
      CSS — conviene tokenizarlos (`var(--…)`) si el proyecto ya usa variables.
- [ ] `border-radius` fuera de la escala 8/12/16/24.
- [ ] `box-shadow` que no corresponde a un `dp` del manual.
- [ ] Paddings/margins fuera de la grilla.
- [ ] Estados faltantes o fuera de marca: `:hover`, `:focus`, `:disabled`
      (cada color de botón oscurece hacia **su propio** hover — §2.2).
- [ ] **Transiciones de estado SIN animar** (§4.1). Todo componente básico al que
      se le pueda poner animación **debe** animar sus cambios de estado
      (hover, foco, activo/pressed, on↔off, selección, carga). Un componente sin
      `transition`/`@keyframes` en sus estados interactivos **es una desviación a
      corregir**, no un detalle opcional.
- [ ] **Cabecera app-shell logueada** (logo + título + usuario): logo recoloreado
      por fondo (`#2D6DF6` claro / `#FFFFFF` oscuro, **no** `#0033A0`), avatar combo
      Inicial (círculo `#2D6DF6` + iniciales `#E3E829`), nombre = primer nombre +
      primer apellido (truncar >20), y **la bajada/cargo bajo el nombre en texto
      secundario, nunca en azul de enlace** (falsa afordancia). Ver
      `organismos/menu-navegador.md` §4.1.
- [ ] **Etiqueta de estado con "bolita" de color** en vez de píldora rellena: el
      estado (info/advertencia/éxito/error) debe ir en el **fondo** del tag (par de
      `moleculas/etiqueta.md` §6: fondo suave + texto principal), nunca como un
      punto/círculo de color junto al texto. Un dot de estado es desviación a
      corregir → reconstruir como tag relleno.
- [ ] **Campo de lista desplegable (select)** que no hereda las medidas base del
      campo: alto Mediano 48 / Grande 56 px y **ancho mín 240 px** (no cajas cortas/
      bajas), redondeo 12 px, valor `#0033A0`, borde activo/foco `#2D6DF6` (no el
      fondo), chevron como glifo. Ver `moleculas/campos.md` §6/§9.
- [ ] **Tabla aproximada con un grid de chips a mano** en vez de su estructura real:
      filas 56 px, celdas 48 px/mín 180 px con su tipo (uno de los 5), columna de
      estatus con **tag relleno** (no dot), selección de fila tinte `#E4E8E9` (no
      cebra azul), casillas a la izquierda, ordenar (`↓`) por columna, acciones a la
      derecha, cabecera de grilla 64 px. Ver `organismos/tablas.md` §3/§8.
- [ ] **Diálogos nativos del navegador** (`alert()`, `confirm()`, `prompt()`,
      `window.alert/confirm/prompt`, `Notification` del SO) usados para mensajes de
      la app: **siempre** son desviación a corregir → reemplazar por componente de
      marca según el contenido. Mensaje que solo **informa** algo **efímero/menor**
      (autosave, "Copiado", aviso sin hito) → **toast** (`moleculas/toast.md`).
      Mensaje que acusa el **éxito de una acción completada** que el usuario quiere
      ver destacada (**formulario enviado**, **solicitud generada**) → **modal de
      confirmación de éxito con un solo botón** `Cerrar`/`Aceptar`/`Continuar`/
      `Listo` (`moleculas/modales.md` §4.2). Mensaje que pide
      **decisión/confirmación** → **modal base** de dos botones
      (`moleculas/modales.md` §4.2). Conserva la lógica: la rama Aceptar/Cancelar de
      un `confirm` se cablea a los botones del modal (confirmar derecha / descartar
      izquierda); el callback de cierre de un `alert` de éxito se cablea al único
      botón del modal de éxito. Nunca dejar el diálogo nativo.
- [ ] **Toast o modal insertados en el flujo del documento** (no superpuestos): ambos
      deben flotar sobre el viewport con `position: fixed` y verse **sin scroll** —
      modal con velo a pantalla completa + tarjeta centrada (`modales.md` §4.1),
      toast en `#alert-container` fijo (`toast.md` §4.1). Un mensaje que obliga al
      usuario a desplazarse para verlo es desviación a corregir.
- [ ] Pares texto/fondo con contraste insuficiente (§4).

---

## 4. Accesibilidad (ver `reference/generales/colores.md` §7)

Al cambiar un color de texto o de fondo, **verifica el contraste con Python**
(no a ojo):

- Cuerpo de texto: mínimo **4.5:1** (AA); recomendado 7:1 (AAA).
- Componentes activos (íconos, bordes de UI): mínimo **3:1**.

Si el cambio de marca empeora un contraste que antes pasaba, prioriza la
legibilidad: elige el token de marca del mismo rol que sí cumpla (p. ej. texto
`#0033A0` sobre fondos claros pasa AA en todos los Fondos 1–5) y anótalo en el
reporte. Nunca dejes un par que falle AA en cuerpo de texto.

```python
def contrast_ratio(hex1, hex2):
    def lum(h):
        h = h.lstrip('#'); r,g,b = (int(h[i:i+2],16)/255 for i in (0,2,4))
        f = lambda c: c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4
        return 0.2126*f(r) + 0.7152*f(g) + 0.0722*f(b)
    L1, L2 = sorted([lum(hex1), lum(hex2)], reverse=True)
    return round((L1 + 0.05) / (L2 + 0.05), 2)
```

---

## 4.1 Animación en cambios de estado (obligatoria, no opcional)

**Regla:** todo componente básico al que se le pueda poner animación **debe**
animar sus transiciones de estado. Un componente básico (switch, botón, radio,
casilla, input, pestaña, acordeón, toast, cargador) **no tiene sentido sin
animación** en sus cambios de estado: hover, foco, activo/pressed, on↔off,
selección, carga. Esto aplica en **ambos modos**.

- **En GENERAR:** incluye `transition`/`@keyframes` en cada estado interactivo
  **desde el primer render** — no como pulido posterior. La animación forma parte
  de la anatomía del componente, igual que su color o su radio.
- **En AUDITAR:** un componente que cambia de estado **sin** transición animada
  **es una desviación a corregir**, no un detalle menor. Repórtalo en la tabla de
  cobertura por componente (§3.0) y aplícale la corrección con `Edit`.

**Cómo animar (sin inventar):**

- **Respeta la spec del componente en `reference/`** si define duración o curva
  (p. ej. el pulgar del Interruptor). Si la spec no la fija, usa transiciones
  cortas y coherentes (**≈0.15–0.25 s, easing suave**). Rebote leve **solo** donde
  aporta (p. ej. `cubic-bezier(0.34, 1.4, 0.64, 1)` en el pulgar del switch al
  asentar); el resto, easing limpio.
- **Anima la propiedad que comunica el cambio**, no "todo": `background`/
  `border-color` en hover/on-off, `box-shadow` en foco, `left`/`transform` en el
  pulgar del switch, `opacity`/`transform` en la entrada del toast, `transform`
  en el spinner. Evita `transition: all` cuando puedas nombrar la propiedad.
- **Accesibilidad:** contempla siempre
  `@media (prefers-reduced-motion: reduce)` para anular o reducir el movimiento
  en usuarios que lo piden. La animación nunca debe ser la única señal de un
  estado (acompáñala de color/posición/ARIA).
- **No animes por adornar:** la animación comunica el cambio de estado, no decora.
  Movimientos largos, parpadeos o rebotes gratuitos también son una desviación.

---

## 5. Chequeos extendidos (opcionales)

Pasadas adicionales que **no corrigen marca** (eso ya lo hacen §1–§4), sino que
verifican robustez, responsive, pulido, redacción y modo oscuro. Aplícalas cuando
el usuario quiera dejar el código listo para producción o lo pida explícitamente.
**Regla heredada:** lo que requiera un valor que no esté en `reference/` se deja
como pendiente (§7) — no se inventa. Los hallazgos se reportan en la misma tabla
de §6 (antes → después → porqué).

### 5.1 Robustez (casos extremos)

- Contenido que crece (nombres largos, números grandes) no desborda: usa
  `overflow`/`text-overflow`/`min-width:0` en celdas y contenedores flex.
- Estados presentes y con marca: **vacío**, **cargando**, **error**, **éxito**.
- Foco siempre visible: halo `#81B1FF` (`box-shadow: 0 0 0 3px`), nunca
  `outline:none` sin reemplazo.
- `:hover`, `:focus` y `:disabled` definidos en inputs y botones.

### 5.2 Responsive

- Revisa en 3 anchos: **móvil 390**, **tablet 1024**, **desktop 1440**.
- Sin scroll horizontal en móvil. Las **tablas anchas** se envuelven en un
  contenedor con `overflow-x:auto` en lugar de romper el layout.
- Áreas táctiles ≥ **44×44 px** en móvil (botones, radios, checkboxes).
- `<meta name="viewport">` presente.
- Los ajustes se hacen con **media queries**, sin cambiar los tokens de marca.

### 5.3 Pixel-perfect (pulido final)

- Alineaciones contra la escala de 8 px.
- Mismo radio entre componentes hermanos (no 12 px en una card y 10 en otra).
- Misma elevación por rol (todas las cards en reposo = dp1).
- Transiciones uniformes, sin parpadeos.

### 5.4 Copy / microcopy (ver `reference/generales/redaccion.md`)

- Sin emojis ni caracteres decorativos (`✓`/`❌`/`📤`).
- Tuteo; éxitos empiezan con "Listo"/"Hecho"; errores = qué pasó + qué hacer,
  sin culpar al usuario ni jerga de plataforma.
- Botones y placeholders accionables (verbo + objeto).
- **No toca contenido de dominio** (títulos, preguntas, legales, nombres).

### 5.5 Modo oscuro

Considera el modo oscuro **siempre** que audites o generes una interfaz, aunque
el código original no lo tenga.

- El único token de marca para modo oscuro es **`--dark-mode-bg: #00003F`**
  (Azul oscuro, "exclusivamente componentes en modo oscuro", `colores.md` §4.3).
  **No existe una paleta oscura completa en `reference/`: no la inventes.**
- Implementa con `@media (prefers-color-scheme: dark)` reasignando variables
  CSS, no duplicando reglas.
- Construye superficies y texto **solo** a partir de tokens existentes: fondo
  `#00003F`, texto claro (blanco / `#F8F8F8`), acentos azules que pasen AA sobre
  oscuro (`#81B1FF`, `#2D6DF6`). Cualquier par sin token de marca que cumpla AA
  se deja como **pendiente**, no se inventa un color nuevo.
- **Verifica cada par texto/fondo del modo oscuro con Python** (§4): cuerpo
  ≥ 4.5:1, componentes ≥ 3:1.
- Los colores de alerta (§2.3) mantienen su rol; si su fondo suave no contrasta
  sobre `#00003F`, usa el principal de la alerta como texto y déjalo anotado.

---

## 6. Formato del reporte de cambios

Entrega **el código corregido** (vía `Edit` sobre el archivo, o como bloque si fue
un fragmento pegado) + este reporte en el chat:

```
## Auditoría de marca — <archivo o fragmento>

### Cobertura por componente (§3.0)
| Componente (rol funcional) | Spec consultada | Estado | Notas |
|---|---|---|---|
| Interruptor (theme-toggle) | atomos/interruptores.md | Corregido | Reconstruido como átomo: pista 40×24, pulgar 16px, on #2D6DF6 |
| Botón / CTA | atomos/botones.md | OK | Píldora, hover por color de rol |
| Toast | moleculas/toast.md | Corregido | Barra de acento + título azul-profundo |
| Tabla | organismos/tablas.md | OK | — |
| … | … | … | … |

### Cambios aplicados (N)
| # | Ubicación | Antes | Después | Por qué |
|---|-----------|-------|---------|---------|
| 1 | .btn-primary, L42 | font-family: Barlow | 'Sura Sans', … | Barlow está prohibida; Sura Sans es la única oficial |
| 2 | :root --azul, L8 | #1976d2 | #2D6DF6 (--color-primary) | Azul de marca canónico |
| … |

### Pendientes (no resueltos sin más contexto)
- <qué, dónde, y qué decisión falta>

### Verificación
- Contraste de los pares modificados (ratio + AA/AAA).
- Cómo probarlo (render del componente / abrir en navegador).
```

Reglas del reporte:
- La tabla de cobertura lleva **una fila por componente** detectado en la UI
  (§3.0), con su estado (Corregido / OK / Pendiente). Ningún componente queda
  fuera de la tabla, aunque ya cumpla la marca.
- Una fila por cambio; agrupa repeticiones idénticas ("12 ocurrencias de `#1976d2`").
- El "por qué" cita la regla o la sección del manual, no solo "es la marca".
- Sé honesto con lo que **no** tocaste y por qué.

---

## 7. Reglas operativas (qué hacer y qué no)

1. **No reescribas la app.** Edición quirúrgica: cambia valores, no arquitectura.
   No renombres clases ni muevas lógica salvo que sea imprescindible para la marca.
2. **No cambies funcionalidad.** Nada de tocar handlers, estado, rutas, data.
3. **No inventes valores.** Si un caso no tiene token claro en `reference/`,
   déjalo como pendiente y pregunta una vez con `AskUserQuestion`.
4. **Respeta el estilo del proyecto.** Si ya usa variables CSS / tokens / Tailwind
   config, integra los valores de marca en ese mecanismo (p. ej. extiende el
   `theme` de Tailwind) en vez de hardcodear.
5. **Tokeniza cuando convenga.** Si hay un color de marca repetido como literal,
   ofrécelo como variable `:root` y referencia con `var(--…)`.
6. **Prioridad de hallazgos:** (1) Barlow / tipografía, (2) colores fuera de
   paleta, (3) contraste que falla AA, (4) radio/elevación/espaciado.
7. **El hex manda.** Si el código comenta un color con un nombre ("Azul SURA"),
   ignora el nombre y corrige por el hex canónico del rol.
8. **Verifica el resultado.** Tras editar, relee el bloque cambiado para confirmar
   que el código sigue siendo válido (sintaxis, comas, llaves).

---

## 8. Pendiente

- [ ] Calibrar la tabla de mapeo §2 con **código real del usuario** (caso de
      prueba que entregará tras cargar moléculas/organismos).
- [ ] Confirmar escala de espaciado exacta contra `grillas.md` para volver
      determinista §2.6.
- [ ] Definir manejo de **Tailwind**: ¿editar `tailwind.config` (tokens) o las
      clases utilitarias en el markup? (depende del proyecto del usuario).
