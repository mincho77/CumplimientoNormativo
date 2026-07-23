# Buscador (Search) — molécula

Fuente: `Buscador.pdf` (1 lámina). Verificado contra imágenes renderizadas y
muestreo de píxeles. **Tipografía: Sura Sans. No aparece Barlow.**

## 1. Qué es

Componente que permite a los usuarios buscar o filtrar contenidos relevantes de
forma rápida, a través de una palabra o grupo de palabras, acelerando la
navegación en el sitio.

## 2. Anatomía

1. **Contenedor** — el campo/caja del buscador.
2. **Campo de búsqueda** — el área editable (placeholder + texto ingresado).
3. **Ícono** — lupa de búsqueda (y `×` para limpiar/cerrar en estado desplegado).

## 3. Construcción (medidas)

### Buscador mediano
| Elemento | Medida |
|---|---|
| Altura | 48 px |
| Padding horizontal (lados) | 20 px |
| Padding vertical (top/bottom) | 12 px |
| Ancho mínimo | 240 px |

### Buscador grande
| Elemento | Medida |
|---|---|
| Altura | 56 px |
| Padding horizontal (lados) | 20 px |
| Padding vertical (top/bottom) | 12 px |
| Ancho mínimo | 240 px |

### Buscador desplegado (con resultados)
| Elemento | Medida |
|---|---|
| Padding interno del campo | 12 px |
| Padding lateral de la lista | 4 px |
| Padding inferior de la lista | 8 px |
| Cada ítem de resultado — vertical | 14 px (top/bottom) |
| Cada ítem de resultado — horizontal | 16 px (lados) |

### Versión responsive / fullscreen
| Elemento | Medida |
|---|---|
| Padding lateral | 12 px |
| Tamaño mínimo | 390 px |
| Tamaño máximo | 600 px |

- **Regla de tamaño:** usar mediano o grande cuando el buscador no ocupe más del
  **50 %** de la pantalla. Si lo supera, usar la versión fullscreen / responsive.

## 4. Placeholder

- Claro y conciso; palabras o frases breves que describan qué se debe ingresar.
- Evitar texto demasiado largo o complicado.
- **Mínimo 3 palabras cortas, máximo 8.**

## 5. Estados

| Estado | Borde | Texto / ícono | Notas |
|---|---|---|---|
| **Por defecto** | gris | texto/ícono gris (placeholder) | — |
| **Activo** | azul `#0033A0` (muestreo `(0,51,160)`) | azul `#0033A0` | + sombra de disponibilidad |
| **Deshabilitado** | gris claro atenuado | gris atenuado | fondo gris muy claro |
| **Sobre (hover)** | azul `#0033A0` | azul `#0033A0` | + sombra |
| **Enfocado (focus)** | azul `#0033A0` | — | anillo/sombra de foco |
| **Activo y sobre** | azul `#0033A0` | azul `#0033A0` | + sombra |

## 6. Sombra

La sombra en los estados **Activo** y **Sobre** indica que el buscador está
disponible para interactuar.

| Estado | X | Y | Blur | Spread | Color | Opacidad |
|---|---|---|---|---|---|---|
| **Activo** | 0 | 4 | 8 | 0 | `#006EFF` | 20 % |
| **Sobre** | 0 | 4 | 8 | 0 | `#535990` | 20 % |

## 7. Uso

- El buscador no debe medir menos de lo indicado en Construcción; si se reduce,
  los elementos pueden agruparse y afectar la experiencia.
- La versión responsive debe ser fácil de usar e intuitiva; el tamaño se ajusta
  al tamaño de pantalla del dispositivo.

## 8. Tokens CSS

```css
:root {
  /* Tamaños */
  --search-h-md: 48px;
  --search-h-lg: 56px;
  --search-pad-x: 20px;
  --search-pad-y: 12px;
  --search-min-w: 240px;

  /* Desplegado / resultados */
  --search-item-pad-y: 14px;
  --search-item-pad-x: 16px;
  --search-list-pad-x: 4px;
  --search-list-pad-b: 8px;

  /* Responsive */
  --search-responsive-pad-x: 12px;
  --search-responsive-min: 390px;
  --search-responsive-max: 600px;

  /* Estado activo/hover */
  --search-active: #0033A0;
  --search-shadow-active: 0 4px 8px rgba(0,110,255,0.20);   /* #006EFF 20% */
  --search-shadow-hover:  0 4px 8px rgba(83,89,144,0.20);   /* #535990 20% */

  --font-search: 'Sura Sans', 'Helvetica Neue', Arial, sans-serif;
}
```

## 9. Reglas operativas para el skill

- Default = borde gris + placeholder gris; al activar/hover/focus → borde y
  texto/ícono en `#0033A0` + la sombra correspondiente de §6.
- Mediano (48 px) o grande (56 px) solo si el buscador ocupa ≤50 % del ancho;
  si no, fullscreen/responsive (390–600 px).
- Placeholder Sura Sans, 3–8 palabras cortas; nunca Barlow.
- Las dos sombras (`#006EFF` activo, `#535990` sobre) son específicas del
  buscador — no reutilizar como elevación general (eso vive en `elevaciones.md`).

## 10. Pendiente

- [ ] Confirmar el gris exacto del borde por defecto y del estado deshabilitado
      (no impreso en la lámina; muestrear si se requiere fidelidad alta).
- [ ] Confirmar radio de borde del campo (la lámina no lo imprime en px;
      por defecto usar la escala `borde-redondeado.md`).
