# Avatar — Sistema de Diseño SURA (Átomo)

Fuente: Manual de marca, sección "Avatar" (Avatar.pdf).

> **Nota de método:** specs verificados leyendo las **imágenes** del PDF
> (láminas de Construcción), no solo el texto. La sección de texto de Avatar
> resultó completa y confiable; aun así se confirmó cada valor contra la lámina.

---

## 1. Concepto

Representación visual de un usuario. Identifica de forma rápida a la persona en
la interfaz (navbar, listas, comentarios). Tiene tres contenidos posibles según
disponibilidad: **imagen**, **iniciales** o **ícono** por defecto.

---

## 2. Forma

- Contenedor **circular** siempre (`border-radius: 50%`).
- Contenido centrado, recortado al círculo.

---

## 3. Tamaños

| Token | px | Uso |
|---|---|---|
| `--avatar-24` | 24 | Inline, listas densas (móvil) |
| `--avatar-32` | 32 | Listas, comentarios (móvil) |
| `--avatar-40` | 40 | Navbar móvil, tarjetas (móvil) |
| `--avatar-56` | 56 | Navbar/perfil desktop (tamaño base desktop) |

---

## 4. Tipos de contenido y color

| Tipo | Fondo | Contenido | Borde |
|---|---|---|---|
| **Inicial** | Azul SURA `#2D6DF6` | Iniciales en **Amarillo alegría** | — |
| **Ícono** | Azul SURA `#2D6DF6` | Ícono por defecto (blanco/claro) | — |
| **Imagen** | Imagen del usuario | — | 1 px Azul SURA `#2D6DF6` |
| **Color alternativo** | Blanco | Iniciales/contenido en Azul SURA `#2D6DF6` | 1 px Azul SURA `#2D6DF6` |

---

## 5. Iniciales — tamaño de texto

| Avatar | Iniciales (caracteres) | Tamaño texto |
|---|---|---|
| 56 px | 2 caracteres | 22 px |
| 40 px | 2 caracteres | 18 px |
| 24–32 px | **1 carácter** | 14 px |

> En 24 y 32 px solo cabe **una inicial** (primer nombre) por legibilidad.

---

## 6. Orden de respaldo (fallback)

Si falta el contenido preferido, baja por esta cadena:

1. **Imagen** del usuario (preferido).
2. **Iniciales** (si no hay imagen).
3. **Ícono por defecto** (si no hay imagen ni nombre).

Tamaño del ícono por defecto según avatar:
- Avatar **56 / 40 px** → ícono **24 px**.
- Avatar **24 / 32 px** → ícono **16 px** (variante simplificada, ver `iconos.md`).

---

## 7. Avatar con sesión iniciada (navbar)

Variante extendida que solo aparece en la **barra de navegación** — nunca en
listas ni comentarios.

- **Ancho del bloque:** 230–260 px.
- **Nombre mostrado:** primer nombre + primer apellido. Truncar con elipsis si
  supera **20 caracteres**.
- **Bajada de texto** opcional (rol/correo) bajo el nombre, ~20 caracteres máx.
- **Tamaño del avatar:** 56 px en desktop, **40 px** en móvil.
- **Paddings:** 8 px / 16 px alrededor del bloque.

---

## 7.bis Mobile / Responsivo — Avatar sesión iniciada

Fuente: *Avatar — mobile.pdf*. En móvil el avatar con sesión iniciada es un
**menú desplegable** con dos estados (no solo un bloque estático como en navbar
desktop). Solo se documentan aquí las diferencias mobile.

**Tamaño:** avatar **40 × 40 px** (constante en móvil).

### Estado por defecto (colapsado)
Solo el **contenedor circular** (40 px) con su elemento identificador (imagen,
inicial o ícono). Es el punto de toque que abre el menú.

### Estado desplegado
Al tocar, se despliega un **menú** anclado al avatar:

| Parte | Detalle |
|---|---|
| Cabecera | avatar 40 px + **Nombre Apellido** + **Bajada de texto** (rol/correo) + chevron `avant-abajo` a la derecha |
| Cuerpo | **Lista** de opciones (Mi perfil, Notificaciones, Tutorial, etc.) |
| Elemento de lista | alto **64 px**, **ícono de marca a la izquierda** + etiqueta; estado seleccionado con realce (tinte `#DFEAFF` claro / `#E3E829` 15 % en oscuro) |

**Espaciados (lámina de Construcción):**
- **16 px** entre avatar y bloque de texto.
- **8 px** entre Nombre y Bajada de texto, y como padding interno del bloque.
- Cada **Elemento de lista = 64 px** de alto.

### Patrones de uso mobile (lámina *Uso del avatar*)
1. **Card con avatar y tag** — perfil: avatar + nombre + documento + **etiqueta**
   (p. ej. "Tomador") + tira de métricas; debajo, lista con íconos de marca.
2. **Card con avatar** — formulario "Crear cuenta": avatar + código en cabecera
   de la tarjeta, seguido de campos.
3. **Avatar sesión iniciada por defecto** — drawer/menú: avatar + nombre + doc,
   con secciones ("Cuenta", "Configuración y privacidad") e ítems con ícono.

> Regla mobile: en pantallas pequeñas, la variante "sesión iniciada" **abre menú
> desplegable** (no abre página). El chevron es obligatorio para señalar que es
> expandible. Los ítems del menú siguen `lista.md` (alto 64 px, ícono líder).

---

## 8. Reglas operativas para el skill

1. Renderiza el contenedor **circular** (`rx=ry=tamaño/2`).
2. Elige el tipo según datos disponibles siguiendo el fallback §6
   (imagen → iniciales → ícono).
3. Para **Inicial**: fondo `#2D6DF6`, texto en Amarillo alegría, tamaño de
   texto según §5. Calcula nº de iniciales por tamaño (1 en 24–32, 2 en 40/56).
4. Para **Ícono**: toma SVG del banco (`assets/icons/`, p. ej. `persona.svg`),
   recolorea y renderiza a 24 px (avatar 56/40) o 16 px (avatar 24/32).
5. Para **Imagen**: recorta al círculo y añade borde 1 px `#2D6DF6`.
6. Variante **color alternativo** solo cuando el contexto exija avatar claro
   (fondo blanco, borde+texto azul).
7. La variante **sesión iniciada** únicamente en navbar, con las medidas §7.
8. Texto de iniciales en **Sura Sans Seminegrita (600)** (ver `tipografia.md`).

---

## 9. Tokens / referencias para implementación

```css
:root {
  --avatar-24: 24px;
  --avatar-32: 32px;
  --avatar-40: 40px;
  --avatar-56: 56px; /* base desktop */

  --avatar-bg: #2D6DF6;          /* Azul SURA */
  --avatar-text-on-blue: #E3E829; /* Amarillo alegría (confirmado vía styleguide) */
  --avatar-border: 1px solid #2D6DF6;

  /* Color alternativo */
  --avatar-alt-bg: #FFFFFF;
  --avatar-alt-text: #2D6DF6;
}
```

---

## 10. Pendiente

- [x] ~~Hex del "Amarillo alegría"~~ → `#E3E829` (variable `--primaryamarillo-alegra`
      = rgba(227,232,41) del styleguide de Botones.pdf). Confirmado.
- [ ] Confirmar el ícono **por defecto** exacto del banco (persona / usuario).
- [ ] Validar el line-height de las iniciales (centrado óptico vs geométrico).
- [ ] Confirmar paddings exactos del bloque navbar (8/16 px asumidos de la
      lámina).
