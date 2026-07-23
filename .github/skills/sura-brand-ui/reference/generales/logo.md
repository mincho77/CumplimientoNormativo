# Logo y descriptor — Sistema de Diseño SURA

Fuente: Manual de marca, sección "Logo y descriptor".

---

## 1. Logosímbolo

El logosímbolo combina:
1. **Tipografía** SURA (creada exclusivamente para la marca, inspirada en las
   plumas del cóndor).
2. **Símbolo** — abstracción del cóndor; sus segmentos representan las plumas
   y evocan movimiento. Los contornos dibujan la letra "S".

### Construcción — tamaños mínimos digitales

| Elemento | Ancho mínimo | Alto mínimo |
|---|---|---|
| Logo completo (tipografía + símbolo) | 65 px | 32 px |
| Símbolo / Isotipo independiente | 18.69 px | 23 px |

### Área de reserva

- El logo debe estar rodeado por un espacio vacío que ningún elemento gráfico,
  fotográfico o tipográfico puede invadir.
- **Área estándar:** equivalente al ancho del símbolo. Debe respetarse a cada
  lado y debe ser mayor siempre que sea posible.
- **Área reducida:** en materiales con espacios reducidos, se puede disminuir
  a la **mitad del ancho del símbolo**.

### Aplicaciones sobre fondos de color

Para fondos planos de color, se pueden utilizar los **tonos más claros de la
paleta complementaria extendida** (ver `colores.md`).

---

## 2. Usos incorrectos del logo

**Nunca:**

1. Cambiar la orientación original.
2. Modificar el orden de los elementos.
3. Alterar la proporción entre tipografía y símbolo.
4. Deformar o distorsionar.
5. Reemplazar la tipografía.
6. Sustituir la palabra "SURA" con otros nombres.
7. Aplicar en un color no permitido.
8. Reproducir en línea de contorno.
9. Emplear efectos o sombras.

---

## 3. Uso del símbolo (isotipo) independiente

El símbolo separado de la tipografía se usa **exclusivamente** en aplicaciones
y materiales digitales:

1. Favicon o thumbnail.
2. Avatar de app.
3. Avatar de redes sociales.
4. Publicaciones de redes sociales.

---

## 4. Descriptores de negocio

Los descriptores indican el negocio que emite el mensaje. Se componen de:

1. **Texto** — nombre del negocio.
2. **Contenedor** — forma rectangular que envuelve el texto.

### Construcción del descriptor

1. Escribir el nombre en **Sura Sans Semibold**, en **mayúsculas sostenidas**,
   en cualquier tamaño. ⚠ El PDF dice aquí "Barlow regular semibold" — es error
   de plantilla; la fuente oficial es **Sura Sans** (ver §6 y `tipografia.md`).
2. Crear un frame rectangular alrededor del texto.
3. **Espaciado vertical** del frame: ½ de la altura de la palabra (½ X).
4. **Espaciado lateral**: igual a la altura de la palabra (X).

### Ejemplos de descriptores aprobados

- `SEGUROS`
- `EPS`
- `SALUD`
- `MOVILIDAD`
- `MASCOTAS`

### Versiones

Cada descriptor existe en versión **positivo** y **negativo** según el fondo
sobre el que se aplique.

---

## 5. Aplicación en navbar / interfaces digitales

El logo aparece en la **navbar superior**, normalmente alineado a la izquierda,
respetando su área de reserva. Cuando hay descriptor de negocio, se ubica al
lado del logo principal con el espaciado lateral correspondiente.

---

## 6. Reglas operativas para el skill

1. En mockups web/desktop, usar el logo completo (no el símbolo aislado).
2. Para favicons, avatares y elementos compactos < 32 px de alto, usar
   el símbolo aislado.
3. Respetar el área de reserva mínima alrededor del logo (= ancho del símbolo).
   En espacios muy reducidos, usar área reducida (= ½ ancho del símbolo).
4. Nunca aplicar sombras, efectos, gradientes o contornos al logo.
5. Si el fondo es de color, usar tonos claros de la paleta complementaria
   o aplicar la versión en negativo (blanco).
6. Para descriptores, usar **Sura Sans Semibold en mayúsculas sostenidas**.
   ⚠ El PDF se contradice: la descripción (pág. "Descriptores") dice "escrito en
   **SURA Sans**", pero el paso de instrucción dice "**Barlow** regular semibold".
   Por directiva de marca, la fuente oficial es **Sura Sans** y nada usa Barlow;
   la mención a Barlow es un error de plantilla (mismo patrón que el CSS de
   Botones). **No usar Barlow en ningún caso.**

---

## 7. Assets vectoriales disponibles

Ubicación: `assets/logo/`. **4 variantes** (solo paths + fills, sin fuentes
embebidas ni referencias externas — renderizan con cairosvg sin dependencias).

| Archivo | Contenido | Color | Uso |
|---|---|---|---|
| `logo-sura-full-azul.svg` | Tipografía + símbolo (90×32) | Azul Cielo Latino | Navbar, header, fondos claros |
| `logo-sura-full-blanco.svg` | Tipografía + símbolo (90×32) | Blanco | Fondos de color / oscuros (negativo) |
| `logo-sura-symbol-azul.svg` | Solo cóndor (26×32) | Azul Cielo Latino | Favicon, avatar, compactos < 32 px |
| `logo-sura-symbol-blanco.svg` | Solo cóndor (26×32) | Blanco | Favicon/avatar sobre fondo de color |

> El símbolo (cóndor) mide **26 px de ancho** en el SVG real — usa este valor
> como referencia del "1 cóndor imaginario" para área de reserva y separación
> de cobranding (ver `cobranding.md`).

### Reglas de selección en mockup

- Fondo claro (`--bg-0` / `--bg-1` / blanco) → variante **azul**.
- Fondo de color o foto oscura → variante **blanco**.
- Ancho de contenedor ≥ 65 px → **full**; < 65 px o cuadrado → **symbol**.

---

## 8. Tokens / referencias para implementación

```css
:root {
  /* Logo principal */
  --logo-min-width: 65px;
  --logo-min-height: 32px;

  /* Símbolo aislado */
  --symbol-min-width: 18.69px;
  --symbol-min-height: 23px;

  /* Área de reserva */
  --logo-clearspace: var(--symbol-min-width);
  --logo-clearspace-reduced: calc(var(--symbol-min-width) / 2);

  /* Descriptor — tipografía (Sura Sans, NO Barlow) */
  --descriptor-font-family: 'Sura Sans', 'Sura', sans-serif;
  --descriptor-font-weight: 600; /* Semibold */
  --descriptor-text-transform: uppercase;
}
```

---

## 9. Pendiente

- [ ] **Descriptores de negocio** (`SEGUROS`, `EPS`, `SALUD`, `MOVILIDAD`,
      `MASCOTAS`) en positivo/negativo — **no entregados aún** como SVG. Por
      ahora el descriptor se compone en mockup con Sura Sans Semibold mayúsculas
      sobre frame rectangular (ver §4), no como asset.
- [ ] Confirmar si existe variante **monocromática gris/negra** del logo para
      casos de impresión o baja tinta.
