# App-shell de navegación web — organismo (PATRÓN POR DEFECTO)

Derivado del proyecto **Marketplace de Activos SURA** (validado en producción con
el usuario). Este es el **andamiaje por defecto** para cualquier interfaz nueva
de pantalla completa en MODO GENERAR: portales, dashboards, herramientas internas,
catálogos, flujos administrativos. Salvo que el usuario pida algo distinto,
**toda UI nueva arranca con este shell**.

**Tipografía: Sura Sans. Barlow prohibida.** Solo íconos de marca (`assets/icons/`).

## 1. Qué es

Una estructura de tres bandas que da sensación de "navegación web" corporativa:

```
┌──────────────────────────────────────────────────────────┐
│ TOPBAR (azul, sticky)  logo+marca · spacer · toggle · user · avatar │
├──────────────────────────────────────────────────────────┤
│ BREADCRUMBS  Inicio / Sección / Aquí                       │
├──────────────────────────────────────────────────────────┤
│ PAGE-HEAD   h1 título            [acciones]                 │
│ ────────────────────────────────────────────────────────  │
│ contenido de la página                                     │
└──────────────────────────────────────────────────────────┘
```

## 2. Anatomía

### Banda 1 — Topbar (azul, sticky, siempre azul en ambos temas)
1. **Logo SURA** (`#ic-logo`) + **nombre de la app** (`.brand`).
2. **Spacer** flexible que empuja el resto a la derecha.
3. **Toggle de tema claro/oscuro** — interruptor animado con sol
   (`#ic-brillo-alto`) y luna (`#ic-modo-oscuro`) + `.thumb` que se desliza.
   Obligatorio (memoria de marca: toggle + modo oscuro siempre).
4. **Bloque de usuario** (`.user`): nombre en negrita + etiqueta de rol debajo.
5. **Avatar** (`.avatar`): iniciales del usuario sobre fondo blanco, texto azul.

### Banda 2 — Breadcrumbs (`.crumbs`)
Contexto de navegación: `Inicio / Sección / <Aquí>`. El último segmento
(`.here`) no es enlace. Da orientación jerárquica en todo momento.

### Banda 3 — Page-head (`.page-head`)
Título de la página (`h1`) a la izquierda + acciones primarias a la derecha
(botones CTA / secundarios). Debajo arranca el contenido.

## 3. Tokens y construcción

| Elemento | Valor / token |
|---|---|
| Alto topbar | **64 px**, `position:sticky; top:0; z-index:50` |
| Fondo topbar | `--topbar:#2D6DF6` — **azul en claro Y oscuro** (no se invierte) |
| Texto topbar | `#fff` |
| Avatar | fondo `#fff`, texto `var(--prim)`, círculo con iniciales |
| Etiqueta rol | tamaño menor, opacidad reducida bajo el nombre |
| Toggle thumb (oscuro) | `[data-theme="dark"] .theme-toggle .thumb{transform:translateX(28px)}` |
| Breadcrumbs sep | `/` atenuado; `.here` sin enlace, color de texto normal |
| Persistencia tema | `localStorage` (ej. `sura-<app>-theme`), aplicar **antes del primer paint** |

## 4. Reglas de marca (no negociables)

- **La topbar y cualquier banner de noticias permanecen AZUL en modo oscuro.**
  No se invierten con el tema; son anclas de marca.
- **Modo oscuro obligatorio** con su toggle visible (sol/luna). Si la UI no lo
  trae, agrégalo como átomo Interruptor.
- **Solo los íconos de marca** del sprite; nunca emojis ni librerías externas.
- **Animar todo cambio de estado** (hover/foco/activo, deslizamiento del toggle,
  apertura de menús).
- **Sin diálogos nativos** del navegador: usar toast / modal de marca.
- **KPIs** (si la página los tiene) con tonos suaves de marca: fondo suave +
  acento pleno, estilo tarjeta modular.
- El avatar muestra **iniciales reales** del usuario; el rol se lee de contexto
  (no inventar nombres ni roles).

## 5. Rol y permisos (opcional, si la app los necesita)

El avatar/usuario puede alternar rol (`data-rol` en `<html>`), ocultando
secciones con `.admin-only`. Útil en herramientas con vistas final vs. admin.
Default: rol más restringido.

## 6. Cuándo NO usar el shell completo

- Pantallas de **login / onboarding** (sin sesión todavía → sin avatar/rol;
  conserva logo + toggle de tema).
- **Modales o flujos embebidos** dentro de otra app que ya trae su propio shell.
- Móvil muy compacto: el bloque `.user` puede colapsar a solo avatar; el toggle
  y breadcrumbs se mantienen.
