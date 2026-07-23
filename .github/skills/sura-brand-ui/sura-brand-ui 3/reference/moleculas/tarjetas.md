# Tarjetas (Cards) — molécula

Fuente: `Tarjetas.pdf` (3 páginas). Verificado contra imágenes renderizadas y
muestreo de píxeles. **Tipografía: Sura Sans. No aparece Barlow.**

## 1. Qué es

Las tarjetas agrupan información y acciones relacionadas en un contenedor. Sirven
como punto de entrada a más detalle, presentan contenido escaneable (imagen +
texto + acciones) y se adaptan a distintos contextos de uso.

## 2. Anatomía

Tarjeta tipo modular:
1. **Contenedor.**
2. **Imagen / foto** (opcional).
3. **Cabecera** — avatar + título + bajada de texto + **menú dango** (3 puntos,
   opcional).
4. **Título.**
5. **Subtítulo / bajada de texto.**
6. **Cuerpo de texto.**
7. **Acciones** (Acción 1 primario, Acción 2 secundario).

## 3. Construcción (medidas)

| Elemento | Medida |
|---|---|
| Bordes redondeados | 12 px |
| Trazo / borde | 1 px, borde **externo** |
| Cuerpo de texto | 16 px Regular |
| Bajada de texto | 14 px Regular |
| Ancho **máximo** tarjeta compacta (con imagen, sin botón) | 358 px |
| Botones de acción | tamaño **mediano** (ver `atomos/botones.md`) |

El ancho/alto **máximo** depende de los ítems usados y del contenedor.

### Variantes de relleno
| Variante | Fondo | Trazo | Sombra |
|---|---|---|---|
| **Relleno blanco (compacta)** | Blanco Puro `#FFFFFF` | 1 px, borde externo | **Sin sombra** |
| **Relleno blanco con sombra** | `#FFFFFF` | 1 px Azul Vivo | `X:0 Y:12 blur:16`, Azul secundario, **opacidad 20%** |
| **Relleno borde lineal** | Blanco Puro `#FFFFFF` | 1 px **Pantone 284** (azul), borde externo | Sin sombra (estado *sobre* genera sombra) |

- El borde lineal se usa sobre **blanco** y colores sólidos en colección.

## 4. Estilos de tarjeta sobre color

Cinco fondos de tinte claro detrás de la tarjeta. Los rótulos impresos de FONDO 4 y
5 eran poco fiables (repetían `#E5E9EA`); **se usa la muestra renderizada real**:

| Fondo | Hex render real | Impreso | Tinte |
|---|---|---|---|
| **FONDO 1** | `#E4E8E9` (muestreo `(228,232,233)`) | `#E5E9EA` ✓ | gris azulado |
| **FONDO 2** | `#F9F9E1` (muestreo `(249,249,225)`) | `#F9FAE1` ✓ | amarillo muy claro |
| **FONDO 3** | `#E6F9EF` (muestreo `(230,249,239)`) | `#E6FAEF` ✓ | verde menta |
| **FONDO 4** | `#DFE9FF` (muestreo `(223,233,255)`) | `#E5E9EA` ✗ | azul lila claro |
| **FONDO 5** | `#F8F8F8` (muestreo `(248,248,248)`) | `#E5E9EA` ✗ | gris casi blanco |

## 5. Estados y colores

| Rol | Hex |
|---|---|
| Título activo | Azul SURA `#0033A0` |
| Botón Acción 1 (primario) | `#2D6DF6` (Azul Vivo SURA) |
| Subtítulo / cuerpo | neutro/gris (ver Pendiente) |

## 6. Uso

- **Texto del título:** puede ser **demasiado largo o corto**; si excede, se trunca
  con puntos suspensivos (`…`). El **subtítulo** también puede truncarse.
- Existe variante **horizontal** (imagen a la derecha, texto a la izquierda) además
  de la vertical (imagen arriba).
- Sobre fondos de color, mantener **contraste y legibilidad** suficientes
  (correcto). No usar combinaciones que reduzcan el contraste (incorrecto).
- **Ajustes en instancia:** para este tipo de card se cambia en la instancia el
  color de fondo (uno de los 5 fondos) sin modificar la estructura.

## 7. Tokens CSS

```css
:root {
  /* Construcción */
  --card-radius: 12px;
  --card-border-w: 1px;
  --card-body-size: 16px;          /* cuerpo, regular */
  --card-caption-size: 14px;       /* bajada, regular */
  --card-compact-max-w: 358px;
  --card-shadow: 0 12px 16px rgba(45,109,246,.20); /* azul secundario 20% */

  /* Colores */
  --card-title: #0033A0;           /* título activo */
  --card-action: #2D6DF6;          /* botón Acción 1 */

  /* Fondos sobre color (render real) */
  --card-bg-1: #E4E8E9;
  --card-bg-2: #F9F9E1;
  --card-bg-3: #E6F9EF;
  --card-bg-4: #DFE9FF;
  --card-bg-5: #F8F8F8;

  /* KPI semántico (fondo suave + acento pleno) */
  --kpi-ok-bg: #DEF6DE;        --kpi-ok-accent: #067014;
  --kpi-warn-bg: #FFF5EC;      --kpi-warn-accent: #ED8B00;
  --kpi-error-bg: #FFF4F3;     --kpi-error-accent: #D12D35;
  --kpi-info-bg: #DFEAFF;      --kpi-info-accent: #0033A0;

  /* Tarjeta modular */
  --card-modular-min-w: 188px;
  --card-modular-max-w: 358px;
  --card-modular-max-h: 640px;
  --card-pad-x: 16px;
  --card-pad-y: 8px;
  --card-hover-shadow: -8px -8px 16px rgba(45,109,246,.20);

  --font-card: 'Sura Sans', 'Helvetica Neue', Arial, sans-serif;
}
```

## 7b. Tarjetas KPI / indicadores (tonos suaves) — OBLIGATORIO

Cuando una tarjeta comunica un **indicador o KPI con significado semántico**
(advertencia, éxito, fallo, información), **no se usa el color de marca saturado
como fondo**. Se usa el **tono claro/suave** de marca como fondo de la tarjeta y
el color semántico pleno **solo** para el número, el ícono o un acento fino
(borde-izquierdo / barra superior de 4 px). Esto evita los tableros "demasiado
fuertes" y mantiene el dato legible.

### Mapa semántico KPI (fondo suave + acento pleno)

| Estado KPI | Fondo de tarjeta (suave) | Acento / número / ícono | Notas |
|---|---|---|---|
| **Éxito / OK** | `#DEF6DE` (Éxito suave) o `#E6FAEF` (FONDO 3) | `#067014` | Verde de éxito de marca. |
| **Advertencia** | `#FFF5EC` (Advertencia suave) o `#F9FAE1` (FONDO 2) | `#ED8B00` | Naranja de advertencia de marca. |
| **Error / Fallo** | `#FFF4F3` (Error suave) | `#D12D35` | No hay rojo entre los 5 fondos sobre color; usar el fondo suave de la etiqueta de Error (`etiqueta.md` §6). |
| **Información / neutro** | `#DFEAFF` (FONDO 4) | `#0033A0` | Azul SURA como acento; chip autocontenido (no voltear en oscuro). |

- **Regla de uso del color:** el fondo es el tono suave; el color pleno se reserva
  para **número grande**, **ícono de estado** y, si se quiere, **una línea de
  acento de 4 px** (superior o izquierda). Nunca pintar toda la tarjeta del color
  pleno semántico.
- **Pares verificados AA** (texto pleno sobre su fondo suave): todos superan 4.5:1
  para el número/etiqueta. Verificar con Python si se cambia un par.
- **Modo oscuro:** estos fondos suaves son **chips autocontenidos** — mantienen su
  fondo claro y su acento pleno en ambos temas (ver `generales/modo-oscuro.md`
  §3). No se voltean a `#81B1FF`.

### Tarjeta modular (estilo tablero KPI)

El formato preferido para KPIs es la **tarjeta modular**: módulos compactos,
iguales en geometría, alineados en grilla, cada uno con un solo dato dominante.

| Elemento | Medida |
|---|---|
| Ancho **mínimo** módulo compacto | 188 px |
| Ancho **máximo** módulo compacto | 358 px |
| Alto **máximo** (móvil) | 640 px |
| Padding horizontal | mín. 16 px |
| Padding vertical | 8 px |
| Bordes redondeados | 12 px |
| Título / rótulo del KPI | 18 px Bold (heading h6) |
| Bajada / unidad | 14 px Regular |
| Texto de botón (si aplica) | máx. **8 caracteres** |
| Sombra estado *sobre* (hover) | `X:-8 Y:-8 blur:16`, Azul primario, opacidad 20% |

- Mantén **misma geometría** entre módulos del tablero; solo cambian el dato y el
  estado semántico (fondo suave + acento).
- El **acento pleno** y el **fondo suave** salen del mapa semántico de arriba; no
  inventar nuevos hex.

### 7.bis Mobile / Responsivo

Fuente: *Tarjetas - mobile.pdf* (Tarjetas modulares + Tarjetas complementarias).
La anatomía (íconos/título/contenedor/botón), los estados (por defecto /
deshabilitado), las variaciones (pequeña/mediana/grande, con tag / imagen / kicker
/ avatar) y todas las medidas base (radio 12 px, cuerpo 16 px, bajada 14 px,
módulo compacto 188–358 px, padding 16/8 px, título 18 px Bold) son **idénticas**
a la versión web — **no se repiten**. Lo genuinamente móvil:

- **La tarjeta ocupa el ancho completo del dispositivo:** el módulo compacto se
  estira al **ancho del viewport** (≈358 px dentro de los 390 px del lienzo móvil,
  con los 16 px de margen lateral). El máximo de 358 px de web es aquí el ancho
  por defecto, no un tope estético.
- **Imagen / ilustración a ancho completo arriba:** en las variantes con imagen,
  la imagen se ancla al borde superior y ocupa todo el ancho de la tarjeta (sin
  márgenes laterales internos), con el contenido textual debajo.
- **Tarjetas complementarias** (prototipos de App): se construyen con los mismos
  parámetros del módulo mediano; la acción usa el **CTA amarillo `#E3E829`** con
  texto navy (cotizar/agendar) o el botón **secundario outline azul** (ver mapa).
  No introducen medidas nuevas.

> El PDF móvil de Tarjetas **no incluye panel de modo oscuro** — todos los ejemplos
> son tema claro. El comportamiento oscuro de la tarjeta se rige por
> `generales/modo-oscuro.md` (chips KPI autocontenidos, fondo navy del lienzo).

## 8. Reglas operativas para el skill

- Tarjeta = contenedor `border-radius: 12px`, borde 1 px externo; imagen opcional,
  cabecera (avatar/título/bajada/menú dango), cuerpo 16 px, bajada 14 px, acciones
  medianas.
- Tres rellenos: **blanco compacto** (sin sombra, ancho máx 358 px), **blanco con
  sombra** (`0 12px 16px` azul 20%), **borde lineal** (Pantone 284, sin sombra,
  sombra en *sobre*).
- Cinco fondos de color (usar hex render real, no el impreso): `#E4E8E9`, `#F9F9E1`,
  `#E6F9EF`, `#DFE9FF`, `#F8F8F8`.
- Título `#0033A0`; Acción 1 `#2D6DF6`. Truncar título/subtítulo largos con `…`.
- Variantes vertical y horizontal; ajustar solo el fondo en instancia.
- Tipografía Sura Sans; **nunca Barlow**.
- **KPI / indicadores con estado** (advertencia/éxito/fallo/info): usar el **tono
  suave** de marca como fondo y el color semántico pleno **solo** para número,
  ícono o acento de 4 px (§7b). Nunca pintar la tarjeta entera del color saturado.
  Mapa: Éxito `#DEF6DE`/`#067014`, Advertencia `#FFF5EC`/`#ED8B00`, Error
  `#FFF4F3`/`#D12D35`, Info `#DFEAFF`/`#0033A0`.
- **Tablero KPI = tarjeta modular**: módulos de geometría idéntica (188–358 px
  ancho, ≤640 px alto móvil, padding 16/8 px, radio 12 px), un dato dominante por
  módulo, sombra hover `-8 -8 16` azul 20%, texto de botón ≤8 caracteres.

## 9. Pendiente

- [ ] Confirmar el neutro exacto del subtítulo/cuerpo y del menú dango (no impreso
      en hex; probable `--gray-900`).
- [ ] Confirmar tamaño del título en px (no impreso) y el estilo de Acción 2
      (outline vs. relleno) por variante.
- [ ] Confirmar el equivalente RGB de "Pantone 284" usado en el borde lineal.
