# Cargador / Indicador de progreso (Loader) — átomo

Fuente: `Cargador.pdf` (1 lámina). Verificado contra imágenes renderizadas y
muestreo de píxeles. **Tipografía: Sura Sans. No aparece Barlow.**

> ⚠ **Nota de nombres (aplica «el hex manda»):** esta lámina rotula `#2D6DF6`
> como "Azul Vivo" y `#0033A0` como "Azul SURA". El nombre **canónico**
> (`generales/colores.md`) es `#2D6DF6` = **Azul Cielo Latino** y `#0033A0` =
> **Azul Profundo**. Los hex son correctos; ignora la discrepancia de nombres
> del PDF (mismo patrón que `selector-rango.md`).

## 1. Qué es

Un cargador o indicador de progreso informa al usuario sobre el **estado de un
proceso activo** (cargar una aplicación, enviar un formulario, guardar una
actualización). Comunica el estado de la aplicación e indica acciones
disponibles, como si el usuario puede navegar fuera de la pantalla actual.

- El **indicador determinado** muestra cuánto durará la transacción (avanza de
  0 a 100 %).
- El **indicador indefinido** indica un tiempo de espera indefinido marcando un
  **loop** en la animación.
- Cuando se muestra el progreso de una **secuencia de procesos**, se muestra el
  **progreso general**, no el progreso de cada paso.

## 2. Anatomía (lineal)

1. **Indicador de progreso** — barra de relleno que avanza.
2. **Pista de progreso** — riel de fondo completo.
3. **Remate o borde** — terminación de la barra.

## 3. Construcción (medidas)

### Cargador lineal (barra)

| Elemento | Medida |
|---|---|
| **Altura del indicador** | 4 px — *se anima para indicar cuánto avanza el proceso* |
| **Altura de la pista** | 8 px |
| **Ancho mínimo** | 358 px |

### Cargador circular

| Elemento | Medida |
|---|---|
| **Diámetro** | 32 × 32 px |
| **Ancho de trazo** | 2 px |

> El cargador circular es un anillo de 32 px con trazo de 2 px que gira en loop
> (indefinido). La barra lineal puede ser determinada (avanza 0→100) o
> indeterminada (loop de la animación).

## 4. Colores

| Parte | Color | Hex |
|---|---|---|
| **Pista** (fondo del riel) | Pantone 429 C *(gris)* | `#B4B4B5` |
| **Indicador — variante amarilla** | Amarillo Alegre / Primario | `#E3E829` |
| **Indicador — variante azul vivo** | Azul Cielo Latino *(lámina: "Azul Vivo")* | `#2D6DF6` |
| **Indicador — variante azul profundo** | Azul Profundo *(lámina: "Azul SURA")* | `#0033A0` |

> El indicador admite **tres colores de marca**: Amarillo Alegre `#E3E829`,
> Azul Cielo Latino `#2D6DF6` y Azul Profundo `#0033A0`. La pista siempre es
> gris `#B4B4B5`. Confirmado por muestreo: pista `(179,179,181)` ≈ `#B4B4B5`,
> azul profundo `(0,51,160)`, azul cielo `(45,109,246)`, amarillo `(226,232,40)`.

## 5. Estados (lineal)

| Estado | Descripción |
|---|---|
| **Vacío** | Solo la pista gris, sin relleno (progreso 0 %) |
| **Lleno** | El indicador rellena la pista (progreso hasta 100 %) |

### Elevación (sombras del estado "Lleno")

| Sombra | X | Y | Blur | Spread | Color |
|---|---|---|---|---|---|
| **Drop shadow #1** | 4 | 8 | 24 | 0 | `#000000` al 15 % |
| **Drop shadow #2** | 0 | 4 | 10 | 0 | `#006EFF` al 25 % |

## 6. Animación

- La barra **se anima** para reflejar el avance del proceso.
- En modo **indeterminado**, la animación hace un **loop** continuo (no hay
  porcentaje conocido).
- El **cargador circular** gira en loop como indicador indefinido.

## 7. Uso

**Usa un indicador de progreso o carga (lineal) cuando:**
- Necesites cargar datos en **segundo plano**.
- Parte del contenido de la **carga inicial** no se pudo completar o no tuvo
  éxito.

**Usa un indicador de progreso circular para:**
- Proporcionar a los usuarios el estado sobre el **procesamiento de sus
  solicitudes**.
- Cuando se **desconozca el contenido** que se va a cargar (como una vista web
  de un tercero).
- **Cargar de forma parcial** por petición del usuario.
- En **respuesta a una acción** disparada por un botón.

## 8. Contenedor y malla

Las superficies detrás del cargador se **cubren temporalmente** para que se
noten menos y el usuario se centre en la animación.

- **Color del fondo:** Blanco (Blanco Puro) que cubre todo, al **80 %** de
  opacidad.

## 9. Tokens para implementación

```css
:root {
  /* Tamaños — barra lineal */
  --loader-indicator-height: 4px;     /* indicador (se anima) */
  --loader-track-height: 8px;         /* pista */
  --loader-min-width: 358px;

  /* Tamaños — circular */
  --loader-circular-size: 32px;       /* diámetro */
  --loader-circular-stroke: 2px;      /* ancho de trazo */

  /* Colores */
  --loader-track: #B4B4B5;            /* Pantone 429 C (gris pista) */
  --loader-indicator-yellow: #E3E829; /* Amarillo Alegre */
  --loader-indicator-blue: #2D6DF6;   /* Azul Cielo Latino */
  --loader-indicator-deep: #0033A0;   /* Azul Profundo */

  /* Elevación (estado lleno) */
  --loader-shadow-1: 4px 8px 24px 0 rgba(0,0,0,0.15);     /* #000000 15% */
  --loader-shadow-2: 0px 4px 10px 0 rgba(0,110,255,0.25); /* #006EFF 25% */

  /* Contenedor / malla */
  --loader-overlay-bg: rgba(255,255,255,0.80); /* Blanco al 80% */
}
```

## 10. Reglas operativas para el skill

1. **Lineal:** pista `#B4B4B5` de **8 px** de alto; indicador de **4 px**
   animado. Ancho mínimo **358 px** — no lo comprimas por debajo.
2. **Circular:** anillo de **32 px** con trazo de **2 px**, gira en loop como
   indicador indefinido.
3. El indicador usa **uno** de los tres colores de marca: `#E3E829`, `#2D6DF6`
   o `#0033A0`. Nunca mezcles colores en una misma barra.
4. Usa **determinado** (0→100) cuando conozcas la duración; usa **indeterminado**
   (loop) cuando no la conozcas.
5. En una **secuencia de procesos** muestra el **progreso general**, no el de
   cada paso.
6. Aplica el **overlay blanco al 80 %** sobre las superficies detrás del
   cargador para enfocar la atención en la animación.
7. En el estado **Lleno**, aplica las dos sombras de elevación
   (`#000000` 15 % y `#006EFF` 25 %).

## 11. Pendiente

- [ ] Confirmar el **radio del remate** de la barra (¿extremos redondeados a la
      mitad de la altura, o rectos?).
- [ ] Confirmar la **duración / curva (easing)** de la animación del loop
      indeterminado (la lámina no documenta tiempos).
- [ ] Confirmar si la barra lineal admite **etiqueta de porcentaje** numérica y
      su tipografía.
- [ ] Verificar si el **gris de pista** es exactamente `#B4B4B5` (impreso) o
      `#B3B3B5` (muestreo) — diferencia de 1 unidad, probable antialiasing.
