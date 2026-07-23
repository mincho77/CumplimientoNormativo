# Organismo · Presentación interactiva (MODO PRESENTAR)

Deck de diapositivas **HTML autónomo, navegable e interactivo** con marca SURA:
una sola página, sin dependencias externas, con navegación por teclado/clic,
modo claro/oscuro, animaciones de entrada y slides interactivas (mapas
anatómicos, comparadores antes/después, galerías con lightbox, tarjetas con
hover). **No** es un `.pptx` (para eso usar el skill `pptx`) ni un mockup PNG
estático (para eso, MODO GENERAR). Es un artefacto vivo que se abre en el
navegador y se recorre como una presentación.

> Toda la marca aplica igual que en GENERAR: Sura Sans, paleta de
> `reference/generales/colores.md`, íconos SOLO del catálogo, modo oscuro con la
> receta de `modo-oscuro.md`, animación obligatoria, toggle de tema obligatorio.
> Este documento añade lo **específico de un deck navegable**.

---

## 0. Filosofía: dinámica, interactiva y centrada en mantener la atención

Un deck SURA **no es un PDF con viñetas**. El objetivo de cada slide es que la
audiencia **entienda rápido y no despegue la vista**. Por eso, por defecto:

1. **Cada elemento y cada slide se anima.** Toda slide entra con una transición
   y sus piezas internas aparecen en cascada (stagger, §1.4). Nada aparece de
   golpe. Esto NO es adorno: el movimiento guía la mirada en el orden correcto
   de lectura. (Siempre con `prefers-reduced-motion`, §1.4.)
2. **Prefiere mostrar antes que contar.** Si un concepto se puede volver un
   **diagrama, una analogía visual, un comparador, una línea de tiempo, una
   tarjeta de dato o una pieza que se toca**, hazlo en vez de un párrafo. Una
   slide con una lista de 5 viñetas casi siempre se puede convertir en algo más
   vivo (mapa de nodos, pasos animados, grilla de tarjetas con íconos).
3. **Una idea protagonista por slide.** Si la slide tiene dos ideas grandes,
   son dos slides. La atención se sostiene cuando cada pantalla tiene un foco.
4. **Interacción real donde aporta.** Al menos las slides clave deben permitir
   **tocar/pasar/arrastrar** (un nodo que revela texto, un comparador
   antes/después, una tarjeta que se levanta en hover). El deck se "recorre",
   no solo se "pasa".
5. **El espacio se usa con intención.** Centrado o asimétrico, ambos valen: lo
   que importa es que cada posición tenga una razón y la slide se vea muy bien.
   Evita solo el vacío *accidental* que deja el contenido perdido (§5b).

> **Regla de oro del modo:** antes de escribir una slide, pregúntate "¿esto
> mantendría despierta a la sala?". Si la respuesta es "es una lista que leería
> en voz alta", rediséñala como una pieza visual o interactiva de §6–§9.

### 0.1 Analiza el contenido ANTES de maquetar (paso obligatorio)

No conviertas el guion en slides una a una de forma mecánica. Primero **lee todo
el contenido** que se va a presentar y decide, por bloque, **qué formato visual
lo hace más fácil de entender**. Mapa de decisión:

| Si el contenido es… | Conviértelo en… | Patrón |
|---|---|---|
| Un sistema de partes que se relacionan (una analogía "X es como Y") | **Mapa de nodos / diagrama anatómico** interactivo | §6 |
| Una comparación A vs B (antes/después, malo/bueno, opción 1/2) | **Comparador** o **dos tarjetas enfrentadas** (✗ rojo suave / ✓ éxito suave) | §7.3, §7b.4 |
| Evidencia, métricas, cifras | **Tarjetas de dato** con fuente citada | §9 |
| Un proceso o ciclo (paso 1 → 2 → 3, o un bucle) | **Pasos animados** con flechas/loop | §7b.5 |
| Una evolución en el tiempo | **Línea de tiempo** horizontal animada | §7b.6 |
| Una estructura jerárquica (carpetas, anatomía de un archivo) | **Árbol / bloque de código anotado** con tarjetas laterales | §7b.7 |
| Capturas de pantalla de un producto real | **Galería + lightbox** (con comparador si hay antes/después) | §7 |
| Una definición + 3–4 facetas | **Grilla de tarjetas con ícono** (2×2 o 1×4) | §7b.3 |
| Una idea-bisagra / cambio de tema | **Slide-respiro** `big-center` con una sola frase grande | §1.5 |
| Una lista de verdad (objetivos, agenda, preguntas) | **Lista con badges**; alineada a un lado con aire, o en columnas — lo que se vea mejor | §5b |

**Entrega del análisis:** antes de construir, comparte con el usuario el **guion
propuesto** (lista de slides con el formato elegido para cada una y cuáles son
interactivas) y confírmalo. Reporta los supuestos.

### 0.2 Tono SURA aplicado a una presentación

El tono de marca (`reference/generales/redaccion.md`) es para el *chrome* de UI;
en un **deck** el tono se ajusta al **propósito de la pieza** (explicar, enseñar,
mostrar resultados, abrir debate), pero conserva el **alma SURA**: cercano,
claro, humano, tranquilo y confiable. Reglas para los textos del deck:

- **Tutea y habla de tú a tú.** "Al terminar, vas a poder…", "lo que tiene
  presente", no "el usuario podrá" ni "se presentará a continuación".
- **Una idea por frase. Frases cortas.** Si una palabra sobra, quítala.
- **Aterriza el tecnicismo con una analogía cotidiana** la primera vez que
  aparece: "Tokens — habla por sílabas", "MCP — el enchufe universal". El
  término técnico va, pero acompañado de su equivalente humano.
- **Sin mayúsculas sostenidas para enfatizar.** Para resaltar usa **negrita** o
  el color de acento, nunca `NO DEBE` ni `IMPORTANTE`. (Un acrónimo es
  diferente: "LLM", "MCP", "RAG" se quedan.)
- **Sin tono alarmista ni signos apilados.** Para una advertencia honesta, un
  pie tranquilo ("La ganancia no es uniforme: …"), no "¡CUIDADO!".
- **Kickers (el tag superior de cada slide) en minúscula con mayúscula inicial
  por palabra clave**, cortos y orientadores: "Qué te llevas hoy", "Los números
  · qué dice la evidencia". El CSS puede ponerlos en versalitas; el **texto
  fuente no va en mayúsculas sostenidas**.
- **Títulos con un acento de color en la palabra clave** (un `<span>` en
  `--accent`), no el título entero en color.
- **No culpes a la audiencia** ni la trates de novata. Acompañas, no señalas.
- **Cifras siempre con su fuente** y con el matiz honesto si lo tiene (§9). Gana
  confianza, que es puro tono SURA.

> En AUDITAR de un deck, los textos que rompan esto (mayúsculas sostenidas,
> frase larga y técnica sin aterrizar, tono frío/impersonal) son desviaciones a
> corregir, igual que un color fuera de paleta. No reescribas nombres propios ni
> citas textuales (un "prompt pobre" de ejemplo puede sonar pobre a propósito).

---

## 1. Arquitectura base del deck

### 1.1 Estructura del documento

Un único archivo `.html` autónomo (todo inline: `<style>`, SVG embebidos,
`@font-face` en base64 o ruta, `<script>` al final). Esqueleto:

```html
<!doctype html>
<html lang="es" data-theme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>/* tokens + fondo + componentes + slides */</style>
</head>
<body>
  <!-- Fondo difuminado animado (blobs) — ELIGE el preset según la temática (§3b) -->
  <div class="bg"><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div></div>

  <!-- Barra de progreso superior (avance del deck) -->
  <div class="progress" id="progress"></div>

  <!-- Barra superior fija minimalista: toggle de tema + nombre de la presentación -->
  <div class="topbar">
    …toggle de tema (§2)…
    <span class="tag">SURA · IA &amp; Skills</span>
  </div>

  <!-- Pista de slides -->
  <main class="deck" id="deck">
    <section class="slide big-center">…portada…</section>
    <section class="slide">…contenido…</section>
    <!-- una <section class="slide"> por diapositiva -->
  </main>

  <!-- Indicadores de progreso (dots) -->
  <nav class="dots" id="dots"></nav>

  <!-- Controles prev/next -->
  <div class="nav-arrows"><button id="prev">‹</button><button id="next">›</button></div>

  <script>/* navegación + progreso + interacciones */</script>
</body>
</html>
```

**Header minimalista (validado).** La barra superior va **sin color de fondo**
(transparente sobre el difuminado): solo el **toggle de tema** a la izquierda y
el **nombre de la presentación** a la derecha (`.tag`). El "avance" se comunica
con la **barra de progreso** superior (§1.6) y los **dots** inferiores, no con
una topbar azul. (Esto difiere del app-shell de GENERAR, que sí lleva topbar
azul: en un deck, el cromo se reduce para que la slide sea la protagonista.)

### 1.2 CSS de la slide (clave)

```css
.slide{
  position:absolute; inset:0;
  display:flex; flex-direction:column; justify-content:safe center;
  padding:64px clamp(40px,7vw,120px) 104px;   /* 104px abajo: respeta la nav */
  opacity:0; transform:translateX(40px) scale(.98); pointer-events:none;
  overflow-y:auto; overscroll-behavior:contain;            /* scroll por slide */
  transition:opacity .5s ease, transform .55s cubic-bezier(.2,.8,.25,1);
}
.slide.active{ opacity:1; transform:none; pointer-events:auto; }
```

- **`position:absolute; inset:0`**: todas las slides se apilan; solo `.active`
  es visible. La transición de salida/entrada se hace con `opacity` + `transform`.
- **`overflow-y:auto` por slide**: cada diapositiva puede desplazarse de forma
  independiente si su contenido excede el alto. **No** pongas el scroll en el
  `<body>`; va en la slide.
- **`padding-bottom` ≥ 104px**: deja sitio para la barra de navegación/dots para
  que no tape el contenido del fondo de la slide.

### 1.3 Navegación (JS mínimo)

```js
const slides=[...document.querySelectorAll('.slide')];
let cur=0;
function go(i){
  cur=Math.max(0,Math.min(slides.length-1,i));
  slides.forEach((s,k)=>s.classList.toggle('active',k===cur));
  syncDots(); syncProgress();
}
window.go=go;                                  // exponer para pruebas
addEventListener('keydown',e=>{
  if(e.key==='ArrowRight'||e.key==='PageDown') go(cur+1);
  if(e.key==='ArrowLeft' ||e.key==='PageUp')   go(cur-1);
});
prev.onclick=()=>go(cur-1); next.onclick=()=>go(cur+1);
go(0);
```

- **Expón `window.go(i)`**: imprescindible para la verificación con navegador
  headless (recorrer todas las slides) y para deep-links.
- Navegación por **teclado** (flechas/PageUp/PageDown) además de clic.

### 1.4 Animación de entrada escalonada (stagger) — patrón refinado

Marca **cada** pieza que deba aparecer con `data-r` y un índice `--i`; el CSS las
revela en cascada cuando la slide entra. Numera `--i` en el **orden de lectura**
(kicker → título → lead → tarjeta 1 → tarjeta 2 → pie), para que el movimiento
guíe la mirada:

```html
<div class="kicker" data-r style="--i:0">…</div>
<h2 data-r style="--i:1">…</h2>
<p class="lead" data-r style="--i:2">…</p>
<div class="card" data-r style="--i:3">…</div>
<div class="card" data-r style="--i:4">…</div>
```

```css
[data-r]{
  opacity:0; transform:translateY(20px);
  transition:opacity .5s ease, transform .6s cubic-bezier(.2,.8,.25,1);
}
.slide.active [data-r]{
  opacity:1; transform:none;
  transition-delay:calc(var(--i,0)*90ms + 180ms);   /* offset base + cascada */
}
@media (prefers-reduced-motion:reduce){
  [data-r], .slide.active [data-r]{transition:none; transform:none; opacity:1}
}
```

- El `+ 180ms` de offset base deja que la slide termine de entrar antes de que
  sus piezas empiecen a revelarse (se siente más intencional que arrancar en 0).
- `translateY(20px)` + curva `cubic-bezier(.2,.8,.25,1)`: entrada suave que sube,
  no un simple fade.
- Siempre contempla `prefers-reduced-motion` (regla de marca: animación con
  respeto a la accesibilidad). En ese modo todo aparece de una, sin transición.

> **Anima también las piezas interactivas**, no solo el texto: una tarjeta se
> **levanta** en hover (`transform:translateY(-4px)` + sombra), un nodo
> **pulsa** sutil, el comparador desliza con su `transition`. El movimiento de
> estado es obligatorio (regla de marca, `auditoria.md` §4.1).

### 1.5 Slide-respiro (`big-center`) entre secciones

Entre bloques temáticos, intercala una slide de **una sola frase grande**
centrada (clase `big-center`): da aire, marca el cambio de tema y sostiene el
ritmo. Úsala para la portada, las bisagras ("Cambiamos el foco", "Foco: Skills")
y el cierre ("¡Gracias!"). Es el contrapunto de las slides densas.

```css
.slide.big-center{justify-content:safe center; align-items:center; text-align:center}
.slide.big-center h1{font-size:clamp(40px,6vw,76px); line-height:1.04; font-weight:900}
```

### 1.6 Barra de progreso superior (avance del deck)

Una barra fina arriba que crece con el avance — comunica "cuánto falta" sin
ocupar espacio. Es parte del header minimalista (el nombre del deck a la derecha,
el progreso aquí):

```css
.progress{position:fixed; top:0; left:0; height:4px; width:0;
  background:var(--accent); z-index:5; transition:width .4s ease}
```

```js
function syncProgress(){
  document.getElementById('progress').style.width =
    ((cur)/(slides.length-1)*100) + '%';
}
// llama syncProgress() dentro de go(i)
```

---

## 2. Toggle de tema sol–pista–luna (patrón validado)

El control de tema es el átomo **Interruptor**, pero en un deck conviene la
variante con **sol a la izquierda, pista en medio, luna a la derecha**, con
**ambos íconos siempre visibles** y el activo resaltado. Evita la variante donde
un ícono desaparece (causa confusión sobre el estado actual).

```css
.theme-toggle{all:unset;cursor:pointer;display:flex;align-items:center;gap:6px}
.tt-track{position:relative;width:48px;height:26px;border-radius:999px;
  background:var(--prim);padding:3px;box-sizing:border-box;flex:none;transition:background .25s ease}
.tt-ic{width:16px;height:16px;flex:none;color:var(--prim);
  opacity:.35;transform:scale(.85);transition:opacity .25s ease,transform .25s ease}
.tt-ic.tt-active{opacity:1;transform:scale(1)}          /* el del tema vigente */
.tt-knob{position:absolute;top:3px;left:3px;width:20px;height:20px;border-radius:50%;
  background:#fff;box-shadow:0 1px 4px rgba(0,0,0,.22);transition:transform .25s cubic-bezier(.34,1.4,.64,1)}
[data-theme=dark] .tt-knob{transform:translateX(22px)}
[data-theme=dark] .tt-track{background:#26307a;border:1px solid #3d4a9a}
```

```html
<button class="theme-toggle" id="tt" role="switch" aria-checked="false"
        aria-label="Cambiar entre modo claro y oscuro">
  <svg class="tt-ic tt-sun tt-active" viewBox="0 0 1000 1000" aria-hidden="true">
    <path transform="translate(0,850) scale(1,-1)" fill="currentColor" d="{SOL}"/></svg>
  <span class="tt-track"><span class="tt-knob"></span></span>
  <svg class="tt-ic tt-moon" viewBox="0 0 1000 1000" aria-hidden="true">
    <path transform="translate(0,850) scale(1,-1)" fill="currentColor" d="{LUNA}"/></svg>
</button>
```

```js
const tt=document.getElementById('tt');
const ttSun=tt.querySelector('.tt-sun'), ttMoon=tt.querySelector('.tt-moon');
function syncThemeIcon(){
  const dark=document.documentElement.getAttribute('data-theme')==='dark';
  ttSun.classList.toggle('tt-active',!dark);
  ttMoon.classList.toggle('tt-active',dark);
  tt.setAttribute('aria-checked',String(dark));
}
tt.onclick=()=>{
  const dark=document.documentElement.getAttribute('data-theme')==='dark';
  document.documentElement.setAttribute('data-theme',dark?'light':'dark');
  syncThemeIcon();
};
syncThemeIcon();
```

Íconos: sol = `brillo-alto`, luna = `modo-oscuro` (del catálogo). Como van
embebidos, **llevan el transform de inversión** (ver §4).

---

## 3. Tokens del deck y modo oscuro

Define los tokens de marca en `:root` y derívalos para `[data-theme=dark]` con la
receta de `reference/generales/modo-oscuro.md` (único token nuevo `#00003F`):

```css
:root{
  --prim:#2D6DF6; --prof:#0033A0; --accent:#2D6DF6;
  --bg:#f4f7ff; --surf:#ffffff; --head:#0a1f44; --ink2:#33415c;
  --muted:#6b7a99; --stroke:#e2e8f5; --foco:#2D6DF6;
}
[data-theme=dark]{
  --bg:#00003F; --surf:#0a1452; --head:#eaf0ff; --ink2:#c5d2f0;
  --muted:#8fa0c8; --stroke:#23306b;
}
```

- **El header del deck es minimalista y transparente** (no topbar azul): toggle
  + nombre del deck sobre el fondo difuminado (§1.1). El azul de marca se reserva
  para acentos, títulos y la barra de progreso.
- Verifica contraste AA con Python al fijar pares texto/fondo (regla de marca).
- Para superficies derivadas, usa **opacidad de un token** existente, no hex
  inventados.

---

## 3b. Fondos según la temática (catálogo de presets) — ELIGE, no inventes

El fondo **fija la emoción** de la presentación antes de leer una palabra. SURA
usa fondos difuminados suaves (no planos, no fotos de stock): un lienzo claro con
**blobs de color desenfocados** que flotan despacio. **Analiza la temática del
deck y elige el preset** cuya emoción encaje; deriva los blobs de **tokens de
marca** (paleta principal + fondos digitales `colores.md` §3 + paleta de
ilustración `colores.md` §5). **Nunca inventes hex**: todos los colores de abajo
salen del manual.

### 3b.1 El lienzo base (siempre difuminado, salvo petición)

```css
.bg{position:fixed; inset:0; z-index:0; overflow:hidden; background:var(--bg)}
.blob{position:absolute; border-radius:50%; filter:blur(60px); opacity:.5;
  animation:float 16s ease-in-out infinite}
.blob.b1{width:520px;height:520px; top:-160px; right:-120px; background:var(--blob-1)}
.blob.b2{width:460px;height:460px; bottom:-180px; left:-120px; background:var(--blob-2); animation-delay:-6s}
.blob.b3{width:380px;height:380px; top:38%; left:42%;    background:var(--blob-3); animation-delay:-11s}
@keyframes float{0%,100%{transform:translate(0,0) scale(1)} 50%{transform:translate(30px,-26px) scale(1.08)}}
@media (prefers-reduced-motion:reduce){.blob{animation:none}}
```

En **oscuro**, baja la opacidad de los blobs (`opacity:.32`) y derívalos hacia
azules profundos para que no compitan con el contenido sobre `#00003F`.

### 3b.2 Presets por emoción/temática

Define `--blob-1/2/3` y `--bg` por preset. La columna "Emoción" es la guía para
elegir; todos los hex son de marca.

| Preset | Cuándo usarlo (temática) | Emoción | `--bg` (claro) | Blobs (de marca) |
|---|---|---|---|---|
| **Tecnología / IA** *(difuminado azul, por defecto para tech)* | IA, datos, plataformas, transformación digital, automatización | Innovación, futuro, confianza | `#F4F7FF` (blanco azulado) | `#81B1FF` foco · `#DFEAFF` fondo-4 · `#2D6DF6` primario |
| **Aqua / claridad** | Salud, bienestar, simplicidad, "lo claro y simple" | Frescura, calma, transparencia | `#E6FAEF` fondo-3 | `#9BE1E9` neutro-aqua · `#00AEC7` aqua · `#81B1FF` foco |
| **Energía / logros** | Resultados, metas, celebración, cierre motivador | Optimismo, impulso, éxito | `#F9FAE1` fondo-2 | `#ECF0A1` neutro-amarillo · `#E3E829` amarillo · `#9BE1E9` aqua |
| **Confianza institucional** | Gobierno, juntas, cumplimiento, estrategia corporativa | Solidez, seriedad, respaldo | `#E5E9EA` fondo-1 | `#838DC8` lavanda · `#2D6DF6` primario · `#0033A0` profundo |
| **Cálido / humano** | Personas, cultura, equipo, experiencias, cercanía | Calidez, comunidad, empatía | `#F8F8F8` fondo-5 | `#FFAA5C` · `#F8CFA9` · `#81B1FF` *(naranjas: paleta de ilustración §5, uso decorativo en blob, no en texto)* |
| **Sobrio / foco total** | Contenido muy denso, técnico, donde el fondo debe desaparecer | Neutralidad, concentración | `#F8F8F8` fondo-5 | un solo blob `#DFEAFF` muy tenue (`opacity:.3`) |

```css
/* Ejemplo: preset Tecnología / IA (el del deck de referencia) */
:root{
  --bg:#F4F7FF;
  --blob-1:#81B1FF;  --blob-2:#DFEAFF;  --blob-3:#2D6DF6;
}
[data-theme=dark]{
  --bg:#00003F;
  --blob-1:#26328C; --blob-2:#001263; --blob-3:#0033A0;   /* azules profundos, tenues */
}
```

### 3b.3 Otras texturas de fondo (cuando el difuminado no encaja)

El difuminado es el **default** y cubre la mayoría de casos. Alternativas de
marca si la temática lo pide (todas con tokens del manual, nunca imágenes):

- **Malla de puntos / grid sutil** (`radial-gradient` de puntos `--stroke` muy
  espaciados): temática de datos, ingeniería, "sistema". Discreto, no distrae.
- **Bandas de formas SURA** (`assets/shapes/*.svg` del catálogo
  `formas-destacados.md`) ancladas a una esquina, muy tenues: para portadas y
  slides-respiro con sello de marca.
- **Plano liso** (`--bg` sin blobs): solo si el usuario lo pide o el contenido es
  tan denso que cualquier fondo estorba (equivale al preset "Sobrio").

> **Regla:** ante la duda, **difuminado azul (preset Tecnología/IA)**. Es el que
> mejor envejece, el más neutro de marca y el validado en producción. Cambia de
> preset solo cuando la emoción de la temática lo justifique, y **díselo al
> usuario** ("elegí el preset Aqua porque el tema es bienestar"); ofrécele
> cambiarlo.

---

## 4. Íconos de marca embebidos — LA REGLA DEL TRANSFORM (gotcha crítico)

Los SVG del catálogo (`assets/icons/*.svg`, `icons.catalog.json`) están
trazados en un **sistema de coordenadas con el eje Y hacia arriba** y por eso el
catálogo los entrega con un `transform="translate(0,850) scale(1,-1)"` que los
voltea al sistema SVG estándar (Y hacia abajo). Ese transform vive normalmente
en el `<svg>`/`<use>` del catálogo.

**Cuando embebes el `<path>` directamente** (como decoración dentro de otro SVG,
o como ícono inline en una tarjeta del deck), **DEBES** replicar ese transform
**en el `<path>`**, o el ícono sale **boca abajo**:

```html
<!-- CORRECTO: ícono SURA embebido -->
<g transform="translate(X,Y) scale(S)" fill="var(--prim)">
  <path transform="translate(0,850) scale(1,-1)" d="{D_DEL_CATALOGO}"/>
</g>

<!-- Inline en tarjeta -->
<svg class="bic" viewBox="0 0 1000 1000" aria-hidden="true">
  <path transform="translate(0,850) scale(1,-1)" fill="currentColor" d="{D}"/>
</svg>
```

- El transform va en el **`<path>`**, no en el `<g>` exterior (el `<g>` exterior
  ya posiciona/escala; mezclar ambos descuadra la geometría).
- **Síntoma del bug**: casco, laptop, certificado, libro… aparecen invertidos
  verticalmente. Esta lección costó varias rondas; revísalo SIEMPRE que embebas
  un ícono del catálogo fuera de su `<svg>` original.
- **Logos de terceros NO llevan este transform** (ver §8): ya vienen en
  orientación SVG estándar.

### 4.1 viewBox correcto

Los íconos del catálogo usan `viewBox="0 0 1000 1000"`. Respeta ese viewBox al
inline-arlos; si copias un `d` del catálogo a un `viewBox` distinto, escala mal.

---

## 5. Patrón: scroll y centrado vertical por slide (gotcha de layout)

Por defecto la slide centra su contenido (`justify-content:safe center`). Pero
una slide **alta** (mapa anatómico, lista larga, comparador) **no debe**
centrarse: al centrar, el contenido del fondo (una caja de detalle, un pie) se
**solapa** con lo de arriba o queda recortado.

**Regla**: si el contenido de la slide puede exceder el alto del viewport, esa
slide **fluye desde arriba** y se hace **scrolleable**:

```css
.slide.tall{justify-content:flex-start}     /* no centra: fluye de arriba */
```

- El `.slide` ya tiene `overflow-y:auto`, así que el scroll aparece solo.
- **Lección real (mapa de la silueta)**: una caja de detalle bajo un diagrama se
  solapaba con las etiquetas. Se corrigió con `justify-content:flex-start` + un
  `min-height` en el contenedor del diagrama suficiente para alojar las etiquetas
  posicionadas en absoluto, de modo que la caja de detalle se empuja **debajo**
  de todo y aparece scroll natural.
- **"Cabe el texto" ≠ "cabe el elemento"**: verifica que las cajas del fondo no
  se solapen midiendo `getBoundingClientRect()` (ver §9).

---

## 5b. Uso del espacio y composición (cada posición se justifica y se ve muy bien)

El objetivo **no** es "centrar todo". Es que **cada slide use el espacio con
intención** y se vea muy bien. Una composición puede ser centrada o asimétrica
(alineada a un lado con aire al otro) — ambas son válidas. Lo que **no** vale es
una posición **accidental**: contenido pegado a un borde "porque sí", con el
resto del lienzo vacío sin que eso aporte nada.

> **Criterio rector:** antes de fijar la posición de un bloque, ten una **razón**
> ("alineo a la izquierda para dar dirección de lectura y dejo aire a la derecha
> que respira", "centro porque es una idea-ancla que quiero que domine"). Si la
> única razón es "quedó ahí", revísalo. El vacío **intencional** es buen diseño;
> el vacío **accidental** descompensa.

### 5b.1 Cuándo cada composición se ve bien

- **Centrado total** (`big-center`): ideas-ancla, portadas, cierres, bisagras —
  cuando quieres que **una sola cosa domine** la pantalla. §1.5.
- **Bloque centrado en ancho útil** (grilla de tarjetas/datos/pasos): cuando hay
  **varias piezas del mismo peso** que se reparten y llenan el ancho de forma
  natural. Se ve ordenado y equilibrado.
- **Asimétrico alineado a la izquierda con aire a la derecha**: **se ve muy bien**
  para listas, objetivos, agendas e intros, porque el borde izquierdo da un eje
  de lectura firme y el aire derecho **respira**. Es una elección legítima y a
  menudo la mejor. No la "arregles" por simetría.
- **Lista + pieza visual de apoyo** (lista a un lado, diagrama/ícono/cifra al
  otro): cuando tienes un elemento que **gana** al acompañar la lista, no para
  "rellenar". Si no hay un visual que aporte de verdad, **no lo inventes** solo
  para tapar el aire — la lista sola con aire se ve mejor que una lista junto a un
  adorno vacío.

```css
.slide-inner{width:100%; max-width:1180px}                 /* ancho útil */
.slide-inner.center{margin-inline:auto}                    /* opcional: centrado */
.slide-inner.left{max-width:880px}                         /* asimétrico izq. con aire a la derecha */
.grid-2{display:grid; grid-template-columns:1fr 1fr; gap:20px}
.grid-4{display:grid; grid-template-columns:repeat(4,1fr); gap:18px}
@media (max-width:1100px){.grid-4{grid-template-columns:repeat(2,1fr)} .grid-2{grid-template-columns:1fr}}
```

### 5b.2 La señal de alarma real (no "está a la izquierda")

Lo que delata una composición **accidental** no es la alineación, son estos
síntomas — y solo si aparecen, se corrige:

- El aire vacío es **tan grande** que el contenido se ve **perdido/encogido** en
  una esquina, no "respirando".
- Hay **desequilibrio incómodo**: peso visual fuerte amontonado a un lado y nada
  que lo balancee ni un margen que lo justifique.
- Romper la cuadrícula **sin razón**: una slide alineada distinto a sus vecinas
  sin motivo, que hace "saltar" el contenido entre slides.

Si una lista a la izquierda con aire a la derecha **se ve bien y respira** (caso
de "Al terminar, vas a poder…"), **déjala así**. No la repartas en dos columnas
ni le claves un visual de relleno solo por simetría: eso la empeora.

### 5b.3 Verifica con criterio, no con una métrica de simetría

Tras maquetar, revisa en headless **mirando** la slide: ¿se ve bien?, ¿el aire
parece intencional o el contenido quedó perdido? Usa `getBoundingClientRect()`
para **detectar** casos extremos (un bloque chico en una esquina con >60% del
lienzo vacío merece una segunda mirada), pero **no** como regla automática de
"si no está centrado, muévelo". La decisión final es de composición, no de una
fórmula. Si dudas, déjalo alineado y con aire antes que forzar simetría.

---

## 6. Slide interactiva: mapa anatómico / diagrama con nodos

Patrón de "analogía visual" (p. ej. *la IA como una persona*): una figura/silueta
SVG central con **nodos** anclados a partes, conectados por **líneas punteadas**
a **etiquetas** laterales; al pasar/tocar un nodo se resalta y se muestra una
descripción en una caja de detalle.

### 6.1 Estructura

```
.bmap-wrap (flex)
 ├─ .bmap-side.left   (etiquetas izquierda, posición absoluta por `top`)
 ├─ .bmap-center      (la silueta SVG + nodos + props + conectores)
 └─ .bmap-side.right  (etiquetas derecha)
.detail (#map-detail) (caja de texto que cambia al seleccionar un nodo)
```

- **Silueta acotada**: la columna central NO debe crecer sin límite en ventanas
  grandes. Acótala con `flex:0 0 20%` **y** `max-width` fijo **y** `max-height`:

  ```css
  .bmap-center{flex:0 0 20%; display:flex; align-items:center; justify-content:center}
  .bmap-center svg{width:100%; height:auto; max-width:240px; max-height:44vh; margin:0 auto}
  ```

  (Lección: con solo `flex:%` la silueta se agrandaba en monitores grandes y
  tapaba etiquetas. El `max-width` en px es el tope que faltaba.)

### 6.2 Nodos, anclas y conectores

- Cada parte del cuerpo es un `<g class="bpart" data-node="N" tabindex="0">` con
  un `<circle class="hot">` (área táctil) y un `<circle class="anchor">` (punto
  exacto de donde sale la línea).
- Las **etiquetas** son `<div class="mlabel" data-node="N" style="top:Npx">`.
- Un JS calcula la línea punteada entre el `anchor` del nodo y su etiqueta. La
  función `anchorPt(node)` prefiere `.bpart[data-node].anchor` y cae a
  `.prop[data-node].anchor` si la parte está representada por un "prop" externo.
- **Decoraciones fijas** (algo en la mano de la figura, p. ej. una llave que
  represente "Herramientas") van **dentro** del `<g>` del cuerpo con
  `pointer-events:none` y **sin** `data-node`, para que el JS no las reposicione.
  Si un ícono del catálogo se ve incompleto a escala pequeña, sustitúyelo por un
  **dibujo geométrico simple** (círculo + línea + rect) — se reconoce mejor.

### 6.3 Distribución de etiquetas (evitar líneas cruzadas)

Ordena las etiquetas de cada lado **según la posición vertical de su nodo en el
cuerpo**, no por importancia. Si un nodo conecta a la cabeza (parte alta), su
etiqueta va arriba; si conecta a las piernas, abajo. (Lección: "Contexto"
conectaba a la cabeza pero estaba al fondo → su línea cruzaba toda la figura.)

### 6.4 Inserción segura de nodos en el DOM

Al insertar/mover etiquetas o props con manipulación de strings, **cuenta la
profundidad de `<div>`** con un contador (regex sobre `<div`/`</div>`) hasta
`depth==0` para hallar el cierre correcto. Un `</div>` mal emparejado rompe toda
la jerarquía (el `.detail` y `.bmap-center` se salen de su contenedor). Verifica
después con el navegador que `slide.children`, `wrap.children` y `side.children`
tengan el conteo esperado.

---

## 7. Slide interactiva: galería + lightbox + comparador antes/después

Galería de capturas que abren un **modal (lightbox)** a pantalla completa; dentro,
un **comparador antes/después** con tirador deslizante, o un `iframe` con una
vista navegable.

### 7.1 Estructura del lightbox

```
.lightbox (#lb)            position:fixed; inset:0; display:grid; place-items:center
 └─ .lb-stage              flex-direction:column; width:fit-content; margin:0 auto
     ├─ .lb-bar            barra título + botón cerrar (width:100%)
     └─ .lb-body           contiene: <img>, #lb-ba (comparador), <iframe> (algunos ocultos)
```

### 7.2 GOTCHA crítico: el iframe oculto descentra el modal

Si el `.lb-body` contiene un `<iframe hidden>` (p. ej. una vista alterna), la
regla `.lb-body iframe{display:block}` **anula el atributo `hidden`** y el iframe
**sigue ocupando su ancho** (p. ej. 1366px), inflando el contenedor flex por
encima del viewport y **empujando la imagen visible a la izquierda** (se ve
descentrada y recortada).

**Fix** (imprescindible):

```css
.lb-body [hidden]{display:none!important}   /* respeta hidden sobre display:block */
.lb-stage{display:flex;flex-direction:column;align-items:center;width:fit-content;max-width:96vw;margin:0 auto}
.lb-body{display:flex;align-items:center;justify-content:center}
.lb-bar{width:100%;align-self:stretch}      /* barra ocupa el ancho del stage */
```

Verifica que el centro del `.lb-stage`, del comparador y del viewport coincidan
(midiendo `getBoundingClientRect`).

### 7.3 Comparador antes/después

`#lb-ba.ba` con `<img class=before>` y `<img class=after>` (la de después con
`clip-path` controlado por un `<input type=range>` o arrastre del `.handle`).
Etiqueta "Antes (app original)" / "Después (marca SURA)" en cada lado.

---

## 7b. Catálogo de slides de contenido (no-modal) para mostrar en vez de contar

Estos patrones cubren el mapa de decisión §0.1. Todos: tokens de marca, íconos
del catálogo (con transform §4), stagger por elemento, hover animado, modo
oscuro y centrado en `.slide-inner` (§5b).

### 7b.3 Grilla de tarjetas con ícono (definición + facetas)

Una idea y 3–4 facetas, cada una en su tarjeta con **ícono de marca** en badge de
acento suave, título y una línea. Reparte en `grid-2` (2×2) o `grid-4` (1×4) para
llenar el ancho. Cada tarjeta `data-r` con su `--i` para entrada en cascada;
hover que la **levanta** (`transform:translateY(-4px)` + sombra).

```css
.card{background:var(--surf); border:1px solid var(--stroke); border-radius:16px;
  padding:22px; transition:transform .2s ease, box-shadow .2s ease}
.card:hover{transform:translateY(-4px); box-shadow:0 12px 30px rgba(45,109,246,.14)}
.card .ic{width:40px;height:40px; border-radius:12px; display:grid; place-items:center;
  background:color-mix(in srgb, var(--prim) 12%, transparent)}   /* acento suave */
```

### 7b.4 Dos tarjetas enfrentadas (comparación A vs B sin modal)

Para "malo vs bueno", "antes vs después conceptual", "opción 1 vs 2". Dos
tarjetas lado a lado: la negativa con borde/acento **error suave** (`--err` en
borde, fondo `#FFF4F3`/su derivado), la positiva con **éxito suave** (`--ok`,
fondo `#DEF6DE`). Encabezado de cada una con ícono de marca (✗ → ícono "cerrar"
del catálogo; ✓ → ícono "verificado"), **nunca emojis**. Útil para "Prompt pobre
/ Prompt claro", "Fine-tuning / Skill".

> Recuerda: los colores de alerta (`colores.md` §4.1) son de uso exclusivo de
> estado; aquí encajan porque la tarjeta **comunica un veredicto** (esto está
> mal / esto está bien). Usa el tono **suave** de fondo y el pleno solo en
> borde/ícono (regla `tarjetas.md` §7b).

### 7b.5 Pasos animados / ciclo (proceso 1→2→3 o bucle)

Para un flujo: cajas conectadas por **flechas** (`→`) o un **bucle** (`↺`). Cada
paso es una tarjeta con número, verbo de acción y una línea ("Piensa · planea el
paso" → "Actúa · usa una herramienta" → "Observa · revisa el resultado" ↺).
Anima la aparición paso a paso con `--i` y, si aporta, un pulso sutil en la
flecha activa. Las flechas y el loop pueden ser **glifos de texto** (`→ ↺`) o un
trazo SVG; si usas ícono de concepto, que sea del catálogo.

### 7b.6 Línea de tiempo horizontal (evolución)

Eje horizontal con hitos: una línea base (`--stroke`), nodos (`--prim`) y
etiquetas alternadas arriba/abajo. Anima el **trazo de la línea** creciendo de
izquierda a derecha (`stroke-dashoffset` o `width` con transición) y los nodos
apareciendo en secuencia. Para "del modelo al Skill", "evolución de la IA".

### 7b.7 Árbol / bloque de código anotado (estructura jerárquica)

Para anatomía de un archivo o estructura de carpetas: un **bloque de código**
(`--code-bg` oscuro, fuente mono) a la izquierda con la estructura, y **tarjetas
laterales** a la derecha que explican cada parte (conectadas por línea o por
color). Resalta tokens (`name`, `description`, comentarios) con color. Si es
interactivo, al tocar una línea del árbol se resalta su tarjeta. Para "Cómo está
hecho un Skill por dentro", "El archivo SKILL.md a fondo".

```css
.code{background:var(--code-bg); color:#cfe0ff; border-radius:14px; padding:20px;
  font-family:'JetBrains Mono','SF Mono',ui-monospace,monospace; font-size:14px; line-height:1.7}
.code .k{color:#81B1FF} .code .s{color:#9be1e9} .code .c{color:#6f8fc9}  /* keyword/string/comment */
```

---

## 8. Logos de terceros (herramientas externas)

En decks que comparan o citan herramientas externas (GitHub, Microsoft, Google,
Anthropic/Claude…), **sí** se permiten sus logotipos oficiales, porque son marcas
ajenas que el usuario debe reconocer — no son "iconografía decorativa" sustituible
por un ícono SURA. **Pero**:

- Usa el **logotipo oficial** real (de su brand kit o de un set fiel como Simple
  Icons/Bootstrap Icons), no un ícono SURA genérico que "se parezca".
- **No** les apliques el transform de inversión §4: vienen en orientación SVG
  estándar (su `viewBox` propio, p. ej. `0 0 16 16` o `0 0 24 24`).
- Mantén el contenedor de marca (círculo/badge con tinte de acento) para que
  encajen visualmente con el resto del deck.
- Para **conceptos propios** de SURA o de IA (no marcas de producto) sigue
  rigiendo la regla: **solo íconos del catálogo**, nunca emojis ni librerías.

---

## 9. Slide de datos / cifras con fuente

Para comunicar evidencia (productividad, adopción), usa tarjetas de estadística:

```
.stat-grid (grid 4 col, 2 en <1100px)
 └─ .stat-card
     ├─ .stat-ic   (ícono de marca en badge de acento suave)
     ├─ .stat-num  (cifra grande, 46px, font-weight 900) + .stat-unit
     ├─ .stat-lbl  (qué mide)
     └─ .stat-src  (FUENTE citada — obligatorio)
.stat-foot (matiz honesto: límites del dato)
```

- **Cada cifra cita su fuente** (`.stat-src`). No inventes números; respáldalos
  con fuentes oficiales/primarias (estudios, papers, blogs de producto). Si la
  ganancia tiene matices (no aplica igual a todos los casos), dilo en un pie
  honesto — gana credibilidad.
- KPIs con estado (éxito/advertencia): tono suave de fondo, color pleno solo en
  número/ícono (regla de `tarjetas.md` §7b).

---

## 10. Verificación con navegador headless (obligatorio)

Antes de entregar, **recorre TODAS las slides** con un navegador headless
(Playwright) y comprueba:

1. **Cero errores de consola** en todo el recorrido (target: arreglo `[]`):

   ```python
   errors=[]
   pg.on('console', lambda m: errors.append(m.text) if m.type=='error' else None)
   total=pg.evaluate("()=>document.querySelectorAll('.slide').length")
   for i in range(total):
       pg.evaluate(f"()=>window.go({i})"); pg.wait_for_timeout(110)
   assert errors==[]
   ```

2. **Espera a que el stagger termine antes de capturar.** Las animaciones de
   entrada (§1.4) tardan ~`offset + n*90ms`. Si capturas a los 110 ms, sale el
   contenido **a medio aparecer** (translúcido, descentrado). Para revisar el
   estado final de una slide, espera **≥1200 ms** tras `go(i)`:

   ```python
   pg.evaluate(f"()=>window.go({i})"); pg.wait_for_timeout(1300); pg.screenshot(...)
   ```

   (Para el barrido de errores de consola basta 110 ms; para **capturas que vas a
   inspeccionar**, espera a que asiente.)

3. **Claro y oscuro**: captura ambos (clic en `#tt`) y revisa contraste y que
   los íconos no estén invertidos. Verifica también que **el fondo difuminado**
   sea el del preset elegido (§3b) y que en oscuro los blobs estén atenuados.

4. **Dos viewports**: `1440×810` (estándar) y `1680×1050` (regresión de ventanas
   grandes: aquí se detecta la silueta que crece o el modal que se descentra).

5. **Composición (§5b)**: mira cada slide y juzga si el espacio se ve bien. La
   asimetría con aire intencional es válida (una lista alineada a un lado con aire
   al otro puede verse muy bien). Marca para revisión solo el vacío *accidental*:
   un bloque chico perdido en una esquina con casi todo el lienzo vacío.

6. **Interacciones**: abre el lightbox, dispara un nodo del mapa
   (`el.dispatchEvent(new MouseEvent('click',{bubbles:true}))` si un hotspot
   intercepta el clic), pasa el hover por una tarjeta (que se levante), y mide
   solapamientos con `getBoundingClientRect()` (la caja de detalle debe quedar
   **por debajo** de la última etiqueta).

7. **Anti-desbordamiento**: ningún elemento del fondo de una slide debe quedar
   tapado por la barra de navegación (respeta el `padding-bottom`).

8. **Íconos del catálogo, no placeholders.** Revisa que ningún ícono salga como
   cuadrado/relleno vacío (síntoma de `d` mal copiado o ícono inexistente):
   verifica cada `<path>` contra el catálogo.

---

## 11. Flujo de trabajo de edición iterativa (recomendado)

El deck suele ser un archivo grande; edítalo de forma incremental y verificable:

1. Copia el entregable a un `work.html` de trabajo.
2. Edita con reemplazos quirúrgicos (string/regex) o `Edit`; para inserciones
   estructurales usa el contador de profundidad de `<div>` (§6.4).
3. Verifica con navegador headless a 1440×810 (y 1680×1050 para regresión).
4. Captura claro y oscuro; revisa el cambio puntual y que no se rompió lo demás.
5. Recorre las slides recolectando errores de consola (target `[]`).
6. Copia `work.html` al entregable final y preséntalo.

**Cierre iterativo obligatorio** (igual que GENERAR/AUDITAR): nunca des el deck
por terminado de forma unilateral. Pregunta qué slide o componente refinar
(portada, un diagrama, el comparador, una cifra) y ajústalo en rondas cortas
dirigidas por el usuario.
