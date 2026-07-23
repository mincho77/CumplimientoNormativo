# Íconos — Sistema de Diseño SURA (Átomo)

Fuente: Manual de marca, sección "Iconos".

> ## ⛔ Regla dura — SOLO íconos de marca, JAMÁS emojis ni iconografía externa
>
> Los **únicos** íconos admitidos son los SVG de marca de `assets/icons/`
> (catálogo en `iconos-catalogo.md`). **Nunca, por ninguna razón**, se admite:
>
> - **Emojis ni dingbats Unicode** — `✓ ✔ ❌ ⚠ 📤 🔔 ✅ ⭐ 🚀 👍 ℹ️ 🔍 🗑 ▶ ●`,
>   etc. Ni en el markup, ni en pseudo-elementos (`content: "✓"`), ni en texto,
>   placeholders, botones, tags, toasts, modales o títulos.
> - **Librerías de íconos de terceros** — Font Awesome, Material Icons / Material
>   Symbols, Bootstrap Icons, Feather, Heroicons, Lucide, Ionicons, Tabler,
>   Remix Icon, Phosphor, fuentes de íconos por CDN (`<i class="fa…">`,
>   `<span class="material-icons">`), SVG/PNG de íconos ajenos a la marca.
> - **Glifos de sistema o del SO** como sustituto de un ícono.
>
> Esto aplica en **ambos modos**:
> - **GENERAR:** desde el primer render solo se incrustan SVG de `assets/icons/`.
>   Si el concepto no existe en el catálogo, se busca un sinónimo (`grep`) y, si
>   aún no hay, se deja un **placeholder marcado** (`/* TODO: ícono de marca */`)
>   — **nunca** se rellena el hueco con un emoji ni un ícono externo.
> - **AUDITAR:** **cada** emoji, dingbat Unicode o ícono de librería externa **es
>   una desviación a corregir** → se reemplaza por el SVG de marca equivalente del
>   catálogo (ver `auditoria.md` §3.0 y checklist §3). Si no hay equivalente, se
>   deja pendiente, no se conserva el emoji.
>
> **El hueco vacío marcado siempre es preferible a un emoji o un ícono ajeno.**

---

## 1. Concepto

Los íconos son imágenes que **invocan acciones** y actúan como llamados de
atención. Ayudan a comprender el contexto, **bajan la carga cognitiva** del
usuario y aumentan la recordación.

---

## 2. Anatomía

Para mantener consistencia, todo ícono debe cumplir:

| Característica | Regla |
|---|---|
| **Esquinas** | Curvas (no rectas) |
| **Terminaciones** | Redondeadas |
| **Trazo** | Línea delgada |
| **Líneas internas** | **NO** redondeadas |
| **Separaciones en el trazo** | Mínimo **2** |

Estilo resultante: **outline / line-icon** de trazo fino y uniforme — nunca
relleno sólido ni trazo grueso.

---

## 3. Tamaños

Tamaños autorizados para interfaz:

| Token | px | Uso típico |
|---|---|---|
| `--icon-16` | 16 | Inline en texto, campos, tags — **usar variante simplificada** |
| `--icon-24` | 24 | Botones, navegación, listas (tamaño base) |
| `--icon-32` | 32 | Encabezados de card, acciones destacadas |
| `--icon-40` | 40 | Features, estados |
| `--icon-64` | 64 | Ilustrativo / vacío / hero pequeño |

> **Iconos simplificados:** en **16 px** usa la versión simplificada del ícono
> (`-s` / `-linea` en el catálogo) cuando exista, para garantizar contraste,
> legibilidad y funcionalidad en móvil.

---

## 4. Estilos y versiones

Dos aplicaciones permitidas:

1. **Sobre fondo de color** — ícono en color contrastante sobre un fondo de
   paleta.
2. **En línea** — ícono del color del texto/acción, sin contenedor.

El **color del ícono puede variar** siempre que sea **totalmente legible**
(contraste suficiente con el fondo, ver `colores.md`).

---

## 5. Categorías del manual

Accesibilidad · Alertas · Flechas · Movilidad · Salud · Financieros ·
Personas · Manos · Animales · Navegación · Varios · Redes sociales ·
Toast y Tags.

El índice completo (503 íconos) por categoría está en
[`iconos-catalogo.md`](./iconos-catalogo.md).

---

## 6. Assets disponibles

Ubicación: `assets/icons/` — **503 SVG**, uno por ícono.

- Extraídos de la fuente oficial `sura-icons` (`units-per-em=1000`,
  `ascent=850`). Cada SVG trae un único `<path fill="currentColor">` con la
  corrección de eje-Y ya aplicada → `viewBox="0 0 1000 1000"`.
- Nombre de archivo = `glyph-name` original (kebab-case), p. ej.
  `corazon.svg`, `flecha-derecha.svg`, `silla-ruedas.svg`.
- Solo paths (sin imágenes ni fuentes embebidas) → renderizan con cairosvg.
- Insumos hermanos en `input/` (no usados por el render, solo referencia):
  fuente web `sura-icons.{eot,ttf,woff,woff2}` + `sura-icons.css` (mapeo
  `.si-{nombre}:before { content:'\eXXX' }`).

### Colorización

El SVG usa `fill="currentColor"`. Para pintar un ícono al renderizar,
**reemplaza `currentColor` por el hex del token** antes de pasar a cairosvg:

```python
svg = open('assets/icons/corazon.svg').read().replace('currentColor', '#0033A0')
cairosvg.svg2png(bytestring=svg.encode(), write_to=out,
                 output_width=24, output_height=24)
```

---

## 7. Usos incorrectos

**Nunca:**

1. **Usar un emoji o dingbat Unicode** (`✓ ❌ ⚠ 📤 🔔 ✅ ⭐ ℹ️ ▶ ●`…) en lugar de
   un ícono de marca — en markup, `content:` de pseudo-elementos, texto, botones,
   tags, toasts o títulos. **Prohibición absoluta, sin excepciones.**
2. **Usar una librería de íconos de terceros** (Font Awesome, Material Icons/
   Symbols, Bootstrap Icons, Feather, Heroicons, Lucide, Ionicons, Tabler, Remix,
   Phosphor) o cualquier SVG/PNG/fuente de íconos ajeno a `assets/icons/`.
3. Engrosar el trazo o rellenar el ícono (rompe el estilo outline).
4. Redondear las **líneas internas** (solo esquinas y terminaciones van curvas).
5. Usar menos de **2 separaciones** en el trazo.
6. Usar un color sin contraste suficiente con el fondo.
7. Deformar la proporción o usar tamaños fuera de la escala (16/24/32/40/64).
8. Usar el ícono detallado en 16 px cuando existe variante simplificada.

---

## 8. Reglas operativas para el skill

1. **Solo íconos de marca.** Todo ícono sale de `assets/icons/` (catálogo
   `iconos-catalogo.md`). **Jamás** un emoji/dingbat Unicode ni un ícono de
   librería externa (Font Awesome, Material, Bootstrap Icons, Feather, Heroicons,
   Lucide…). Sin excepciones, en GENERAR y AUDITAR. En AUDITAR cada uno es
   desviación a corregir; si no hay equivalente, déjalo pendiente — no lo conserves.
2. Para colocar un ícono: busca el concepto en `iconos-catalogo.md`, toma el
   **nombre exacto** → `assets/icons/{nombre}.svg`, reemplaza `currentColor`
   por el token de color y renderiza al **tamaño de la escala** más cercano.
3. Si el concepto no existe, busca un sinónimo en el catálogo (`grep`); si aún no
   aparece, deja un **placeholder marcado** (`/* TODO: ícono de marca */`) — nunca
   lo sustituyas por un emoji ni un ícono ajeno.
3. Tamaño base de UI = **24 px**. Inline en texto = 16 px (variante
   simplificada). Acción destacada = 32 px.
4. Color del ícono = color del texto/acción del contexto (en línea) o
   contrastante (sobre fondo de color). Nunca fuera de paleta.
5. **No** mezcles ícono + ilustración + pictograma en el mismo rol jerárquico
   — el ícono es elemento de acción/UI, no decorativo.
6. En **stepper** los íconos/numerales marcan el paso actual (ver futuro
   `stepper.md` en moléculas/organismos).
7. **Íconos semánticos de acción — usa el del significado, no uno aproximado:**
   - **Eliminar / borrar → `papelera.svg`** (o `basurero.svg`). **Nunca** un pulgar
     abajo (`mano-abajo`), una `×`, ni el emoji `🗑` para "eliminar".
   - Editar → `editar`/`lapiz`. Ver detalle → `ojo-abierto`. Agregar/crear →
     `mas-linea`. Buscar → `buscar`. Actualizar/recargar → `flechas-circulando`.
   - `mano-arriba` / `mano-abajo` (pulgares) significan **aprobar/rechazar** o
     **útil/no útil**, NO acciones CRUD; no los uses para eliminar/inactivar.
   En AUDITAR, un ícono semánticamente incorrecto (p. ej. pulgar abajo para
   "eliminar") es una desviación a corregir por el ícono correcto del catálogo.
8. **En scripts Python de generación de mockups SVG: SIEMPRE usa el helper
   `icon(name, cx, cy, size, color)`** que carga el SVG de `assets/icons/`.
   **NUNCA dibujes íconos a mano** con `<path d="...">` o `<line>`/`<circle>`
   construidos inline — aunque parezcan correctos visualmente, no son los íconos
   de marca, se desactualizan y producen inconsistencias entre mockups.
   La regla es la misma que en GENERAR/AUDITAR: si el concepto no existe en el
   catálogo, deja un `# TODO: ícono de marca` y pon un rectángulo placeholder.

---

## 9. Tokens / referencias para implementación

```css
:root {
  --icon-16: 16px;
  --icon-24: 24px; /* base */
  --icon-32: 32px;
  --icon-40: 40px;
  --icon-64: 64px;

  --icon-stroke: 1.5px;      /* trazo delgado (aprox. — confirmar) */
  --icon-color-inline: currentColor;
}
```

---

## 10. Pendiente

- [ ] Confirmar el **grosor de trazo exacto** (px) por tamaño — el PDF dice
      "línea delgada" sin valor numérico.
- [ ] Mapear qué íconos tienen **variante simplificada** real para 16 px
      (más allá de los sufijos `-s` / `-linea`).
- [ ] Validar el **mapa heurístico ícono→categoría** del catálogo con marca.
- [ ] Documentar el componente **Stepper** (numerales 1·2) como molécula.
