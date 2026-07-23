# Formas / Destacados — Sistema de Diseño SURA

Fuente: Manual de marca, sección "Formas".

---

## 1. Concepto

Los **destacados** son una familia de formas redondeadas y orgánicas
inspiradas en las **burbujas de conversación**. Se usan para resaltar textos,
enmarcar imágenes y complementar piezas gráficas.

> **Regla crítica:** los destacados son un set **cerrado**. No se pueden
> alterar ni crear nuevas versiones.

---

## 2. Estilos autorizados

| Estilo | Descripción |
|---|---|
| **Cuadrados y rectangulares** | Forma básica con esquinas redondeadas |
| **Cuadrados/rectangulares — speech bubble izquierda** | Con "cola" apuntando a la izquierda |
| **Cuadrados/rectangulares — speech bubble derecha** | Con "cola" apuntando a la derecha |
| **Triangulares** | Formas con vértices redondeados |
| **Romboides** | Formas tipo diamante con curvas |
| **Dobles** | Composición de dos formas superpuestas |

---

## 3. Anatomía de un destacado

1. **Silueta visible**: la forma no debe cubrir completamente el elemento
   que contiene — debe permitir apreciar la silueta de la imagen o
   ilustración.
2. **Color de paleta**: usa colores de la paleta SURA (ver `colores.md`),
   sobre fondos **contrastantes**.
3. **Sobresale hasta 25 %**: la ilustración o silueta puede sobresalir
   hasta un **25 % del contenedor** — esto refuerza la dinámica visual.

---

## 4. Usos correctos

| Uso | Detalle |
|---|---|
| Forma contenedora de **imágenes** | La imagen no debe llenarla completamente; deja silueta visible |
| Resaltar **textos** (titulares, cifras) | Deja siempre espacio para que el texto "respire" |
| **Flotante** detrás de ilustraciones | Para complementar, contrastar y romper simetrías |
| Forma contenedora de **ilustraciones** | Con colores de paleta que contrasten fondo y figura |

---

## 5. Usos incorrectos

**Nunca:**

1. Editar fotografías aplicando cortes bruscos o radicales con la forma.
2. Mezclar más de un contenido en el contenedor (no combinar foto + ilustración
   + texto). **Un propósito a la vez.**
3. Contener una fotografía totalmente sin usar silueta visible.
4. Alterar las formas o crear nuevas variantes.

---

## 6. Assets vectoriales disponibles

Ubicación: `assets/shapes/`. **432 formas** (solo paths + fills, sin fuentes
ni referencias externas — renderizan con cairosvg). Lienzo `1080×1080`.

### Convención de nombres

```
{paleta}_{color}_forma-{NN}.svg
```

- `{NN}` va de `00` a `35` → **36 formas** por grupo de color.
- 3 paletas × 4 colores × 36 formas = **432** assets.

| Paleta | Colores disponibles |
|---|---|
| `complementaria` | `amarillo-alegre`, `aqua`, `azul-sura`, `azul-vivo` |
| `digital` | `amarillo`, `aqua`, `azul-vivo`, `gris` |
| `neutro` | `amarillo`, `aqua`, `azul`, `azul-vivo` |

Ejemplos: `complementaria_azul-sura_forma-00.svg`,
`digital_gris_forma-12.svg`, `neutro_amarillo_forma-35.svg`.

> Las formas son orgánicas (blobs / burbujas redondeadas). Cada índice
> `forma-NN` es la **misma silueta** repetida en los 12 grupos de color —
> elige el grupo según la paleta del bloque y el color de contraste deseado.

### Selección de color en mockup

- Bloque con sistema SURA puro → paleta `digital` o `neutro`.
- Acentos vivos / destacados de campaña → paleta `complementaria`.
- Respeta el contraste figura-fondo (ver `colores.md`); nunca color fuera de paleta.

---

## 7. Reglas operativas para el skill

1. Referencia los destacados **por nombre exacto** del asset
   (`{paleta}_{color}_forma-NN.svg`) y renderízalos con cairosvg al tamaño
   del contenedor.
2. Cuando uses un destacado como contenedor de imagen, deja al menos
   **el 15 %** del contenedor sin cubrir para preservar la silueta.
3. Aplica color de la paleta principal o complementaria al destacado;
   nunca colores fuera de paleta. El color ya viene fijado en cada SVG —
   elige el grupo correcto en lugar de recolorear.
4. **Un destacado por elemento** — no superpongas dos destacados
   excepto en el estilo "Dobles" predefinido.
5. Los destacados son **decorativos** — no los uses para botones,
   inputs ni elementos interactivos.

---

## 8. Pendiente

- [ ] Confirmar el **mapa silueta→estilo**: qué índices `forma-NN`
      corresponden a cuadrado, speech-bubble izq/der, triangular, romboide,
      doble (§2). Hoy se conocen por nombre numérico, no por estilo.
- [ ] Documentar las **proporciones exactas** de cada estilo (ratio
      ancho/alto) — todas se entregan en lienzo cuadrado 1080×1080.
