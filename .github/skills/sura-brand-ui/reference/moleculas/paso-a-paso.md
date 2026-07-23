# Paso a paso (Stepper) — molécula

Fuente: `Paso a paso.pdf` (varias láminas). Verificado contra imágenes renderizadas
y muestreo de píxeles. **Tipografía: Sura Sans. No aparece Barlow.**

## 1. Qué es

El paso a paso (steppers) transmite el progreso a través de **pasos numerados**.
Guía a los usuarios por procesos complejos para hacerlos simples e intuitivos,
reduce la frustración y ayuda a completar tareas correctamente.

## 2. Anatomía

### Tarjeta base modular
1. **Cabecera** (la fila de pasos numerados).
2. **Área de contenido.**
3. **Pie de página** (opcional).
4. **Paso check** (completado).
5. **Separador** (línea entre pasos).
6. **Paso activo.**
7. **Paso inactivo.**
8. **Botón siguiente** (opcional).
9. **Botón atrás** (opcional).

### Anatomía de cada step
1. **Círculo contenedor.**
2. **Número del paso.**
3. **Etiqueta del paso.**

## 3. Construcción (medidas)

### Step (paso individual)
| Elemento | Medida |
|---|---|
| Número del paso | 24 px |
| Padding superior / inferior del círculo | 4 px |
| Espaciado círculo ↔ etiqueta | 10 px |
| Separación horizontal entre pasos | 8 px |

### Cabecera
| Elemento | Medida |
|---|---|
| Padding horizontal mínimo | 16 px |
| Padding vertical | 16 px |
| Ancho del separador entre pasos | 100 px |
| Gap del separador | 8 px |

### Pie de página
- Aplica **solo para escritorio** y es **opcional**, según el framework.
- Botón **"Atrás"** = botón **secundario mediano**.
- Botón **"Siguiente"** = botón **primario mediano**.
- Ambos siguen lo documentado en `atomos/botones.md`.
- Área de contenido: padding **24 px** a los lados, **16 px** vertical, altura **auto**.

### Anchos del componente
| Versión | Ancho |
|---|---|
| **Máximo** | 1366 px |
| **Mínimo** | 640 px |

## 4. Estados del step

| Estado | Círculo | Contenido | Color |
|---|---|---|---|
| **Inactivo** | sin relleno (outline) | número del paso | neutro/gris |
| **Activo** | relleno | número en blanco | **Azul SURA `#0033A0`** (muestreo `(0,51,160)`) |
| **Completado** | relleno con ícono **check** | check en blanco | **Teal `#00AEC6`** (muestreo `(0,174,198)`) |

- **Paso inactivo:** pasos que le faltan al usuario por completar. Muestra el número
  y el contenedor **no** lleva relleno.
- **Paso activo:** el paso actual del usuario. Muestra el número y usa el color
  **Azul SURA**.
- **Paso completado:** pasos visitados y completados antes. Muestra el ícono
  **check** sobre relleno teal.

## 5. Uso

- Ideal cuando el contenido de un paso **depende de haber completado** el anterior.
- Mostrar los pasos en orden **de izquierda a derecha**, indicando dónde se
  encuentra el usuario actualmente.
- **Máximo de pasos sugerido para escritorio**: respetar el límite del manual (no
  saturar la cabecera).
- **No puede haber dos pasos activos** a la vez (incorrecto — confunde al usuario).
- Los estados deben ser **coherentes con el progreso** real del usuario.
- **Etiquetas:** concisas, claras, que expliquen el propósito del paso. Máximo
  **2 líneas**; si exceden, truncar con puntos suspensivos (`…`).
- **No modificar las dimensiones** de las etiquetas ni sobrepasar las 2 líneas
  (ambos son incorrectos).

## 5.bis Mobile / Responsivo (Stepper Mobile)

Fuente: *Paso a paso mobile.pdf*. En móvil el stepper **no muestra los círculos
numerados**: se simplifica a una **barra de progreso lineal** con la etiqueta del
paso actual y la del siguiente. Solo se documentan aquí las diferencias mobile.

### Anatomía mobile
1. **Paso actual** — título del paso en curso (negrita, izquierda).
2. **Paso siguiente** — texto "Paso : Siguiente" (atenuado, derecha).
3. **Barra de progreso** — barra lineal bajo las etiquetas que indica el avance.
4. **Área de contenido.**
5. **Pie de página (opcional)** — botones **Atrás** (secundario) + **Siguiente**
   (primario).

### Construcción mobile (medidas de la lámina)
| Elemento | Medida |
|---|---|
| Padding superior fila de etiquetas | **8 px** |
| Separación etiqueta ↔ barra | **4 px** |
| Padding inferior antes del contenido | **8 px** |
| Margen lateral del bloque | **12 px** |
| Barra de progreso (alto) | **5 px** |
| Padding vertical alrededor de la barra | **12 px** |

### Anchos mobile
| Versión | Ancho |
|---|---|
| **Mínimo** | **360 px** (smartphones) |
| **Máximo** | **744 px** (tablet) |

> Diferencia clave web↔mobile: el desktop usa la cabecera de **pasos numerados**
> (círculos + separadores, §2–§3); el móvil la reemplaza por **una barra de
> progreso + etiquetas actual/siguiente**. El área de contenido y el pie
> (Atrás/Siguiente) se conservan igual. En móvil el pie **sí se usa** (a diferencia
> del desktop, donde es opcional) porque es el único control de navegación entre
> pasos.

---

## 6. Tokens CSS

```css
:root {
  /* Step */
  --stepper-number-size: 24px;
  --stepper-circle-pad-y: 4px;
  --stepper-label-gap: 10px;          /* círculo ↔ etiqueta */
  --stepper-step-gap: 8px;            /* entre pasos */

  /* Cabecera */
  --stepper-header-pad-x: 16px;
  --stepper-header-pad-y: 16px;
  --stepper-separator-w: 100px;

  /* Contenido / pie */
  --stepper-content-pad-x: 24px;
  --stepper-content-pad-y: 16px;

  /* Anchos */
  --stepper-max-w: 1366px;
  --stepper-min-w: 640px;

  /* Mobile (Stepper Mobile) — barra de progreso lineal */
  --stepper-mobile-min-w: 360px;
  --stepper-mobile-max-w: 744px;
  --stepper-mobile-bar-h: 5px;
  --stepper-mobile-margin-x: 12px;
  --stepper-mobile-bar-pad-y: 12px;

  /* Estados */
  --stepper-active: #0033A0;          /* paso activo (relleno, número blanco) */
  --stepper-complete: #00AEC6;        /* paso completado (relleno + check) */
  --stepper-active-text: #FFFFFF;

  --font-stepper: 'Sura Sans', 'Helvetica Neue', Arial, sans-serif;
}
```

## 7. Reglas operativas para el skill

- Tres estados de paso: **inactivo** (outline, número, neutro), **activo**
  (relleno `#0033A0`, número blanco), **completado** (relleno `#00AEC6`, ícono
  check blanco). Separador entre pasos.
- Cabecera con padding 16/16; separador 100 px; gap entre pasos 8 px;
  número 24 px; etiqueta a 10 px del círculo.
- Pie de página solo escritorio/opcional: Atrás = secundario mediano, Siguiente =
  primario mediano (ver `botones.md`). Contenido padding 24 px lados / 16 px
  vertical, alto auto.
- Ancho del componente 640–1366 px.
- Orden izquierda→derecha; **nunca dos pasos activos**; etiquetas ≤2 líneas con
  truncado `…`; tipografía Sura Sans, nunca Barlow.

## 8. Pendiente

- [ ] Confirmar el neutro exacto del círculo/número/etiqueta del paso inactivo
      (no impreso en hex; probable `--gray-900` / borde neutro).
- [ ] Confirmar el color del separador en cada tramo (completado→teal/azul vs.
      inactivo→gris) y su grosor en px.
- [ ] Confirmar el número máximo de pasos sugerido para escritorio (texto de la
      lámina parcialmente recortado).
