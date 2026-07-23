# Ilustración — Sistema de Diseño SURA

Fuente: Manual de marca, sección "Ilustración".

---

## 1. Concepto

Las ilustraciones SURA son **exclusivas de la marca** y fueron creadas dentro
de un universo gráfico en el cual **las personas son el eje central**.
Personalidad **amigable** que resalta la humanidad a través de lo **hecho a
mano**.

| Característica | Detalle |
|---|---|
| **Trazos** | Orgánicos, fluidos y naturales — **nunca** trazos vectoriales rígidos o fríos |
| **Estilo** | Transmite el lado humano y cálido de SURA |
| **Lectura** | Representan **emociones** más que situaciones — la ilustración propicia que el observador complete la información |

---

## 2. Cuándo usar ilustración

Usa ilustración (en lugar de fotografía) cuando necesites:

1. Comunicar **emociones ambiguas** que pueden generar diferentes
   interpretaciones positivas.
2. Mostrar **situaciones complejas** que la audiencia puede completar.
3. Llegar a **diferentes audiencias y edades**.
4. Mostrar **situaciones de riesgo** que la fotografía explicaría de manera
   burda.
5. Comunicar conceptos **específicos** (procesos, productos, errores
   técnicos) que serían difíciles de fotografiar.

---

## 3. Anatomía

Latinoamérica tiene **rostros, pieles y rasgos latinos** muy expresivos
(ojos y labios). Las ilustraciones SURA:

- Reflejan **cuerpos diversos**.
- Cumplen **criterios anatómicos coherentes** con lo que SURA sabe de salud.
- **Evitan perpetuar estereotipos de belleza**.
- **Reconocen todas las poblaciones**.

---

## 4. Familias temáticas

### 4.1 Producto
Ilustra situaciones de productos SURA:
- Seguro **Salud**
- Seguro **Viajes**
- Seguro **Carro**
- Seguro **Moto**
- Seguro de **Arriendo**
- Seguro de **Empresa**
- Seguro de **Mascotas**

### 4.2 UX
Para situaciones digitales y temáticas virtuales:
- **Error 404**
- **Redirección**
- **Error genérico**
- **Error 500**

### 4.3 CCM (Customer Communication Management)
Comunicaciones transaccionales sobre productos:
- **Cancelación de producto**
- **Bienvenida**
- **Notificación**
- **Pago pendiente**

### 4.4 Temáticas específicas
- **Maternidad**
- **Educación financiera**
- **Odontología**
- **Vacunación**

### 4.5 Temática general
Historias latinas que dan vida a las comunicaciones. Momentos sencillos de
la vida cotidiana con personajes cercanos y felices que sienten ganas de
vivir.

Subcategorías:
- **Diversidad de edad**
- **Salud y cuidado**
- **Entornos**
- **Movilidad (vehículos)**
- **Conceptos con representación abstracta** (inclusión)
- **Caracterizaciones antropomorfas** (salud + mascotas)
- **Humanos y animales**

---

## 5. Recomendaciones generales

1. Elegir **situaciones positivas**.
2. **Sonrisas y calidez** en rostros.
3. **Situaciones seguras**, con elementos de protección: cinturón, casco,
   gafas, guantes, etc.
4. **Inclusión**: edad, género, prótesis, sillas de ruedas, tatuajes,
   limitaciones locomotoras, auditivas y visuales.
5. **Texturizar con halftone** solo objetos inertes — **nunca seres vivos**.
   Solo una superficie por composición y a tono contrastante.
6. **Texturizar con noise** hasta 2 superficies — sí permitido en seres
   vivos (humano, animal, planta). Usar tonos de contraste.

---

## 6. Usos incorrectos

**Nunca:**

1. Usar una **línea, proporción o trazo diferente** a la del banco oficial.
   Si necesitas una situación particular, **primero revisa el banco** y
   busca la más aproximada.
2. Modificar o utilizar **colores diferentes** a la paleta establecida para
   ilustración y pictogramas (ver `colores.md`).
3. Componer con **2 o más ilustraciones** para ilustrar una sola situación
   — una ilustración = una situación.
4. Usar **fondos sin contraste** con la ilustración.

---

## 7. Assets vectoriales disponibles

Ubicación: `assets/illustrations/` — **166 SVG** del banco oficial. Catálogo
completo con nombres exactos por familia en
[`ilustraciones-catalogo.md`](./ilustraciones-catalogo.md).

| Familia | Cantidad | Notas |
|---|---|---|
| Producto | 77 | Salud, Viajes, Carro/Movilidad, Moto, Arriendo, Empresa/ARL, Mascotas, Recompensas |
| UX | 5 | Error 404 / 500 / genérico, Redirección, Cookies |
| CCM | 13 | Bienvenida, Cancelación, Notificación, Pago aprobado/pendiente, Cotización, Descarga app |
| Específicas | 25 | Maternidad, Educación financiera, Odontología, Oftalmología, Vacunación, Bienestar |
| General | 46 | Cotidiano (adulto mayor, niño, deporte, alimentación, teletrabajo, etc.) |

- Sin fuentes embebidas ni referencias externas → renderizan con cairosvg.
- **84/166** incrustan imagen raster (base64); cairosvg también las soporta.
- Variantes de pose por sufijo (`_`, `__1`, `__2`); dimensión nativa en el
  nombre (`_1920x1080` = hero/banner). Ver convenciones en el catálogo.

---

## 8. Reglas operativas para el skill

1. Para elegir ilustración: busca el **tema** en `ilustraciones-catalogo.md`,
   toma el **nombre literal** del SVG (con tildes/espacios si los trae) y
   renderízalo con cairosvg al tamaño del bloque. Solo usa placeholder si el
   tema **no existe** en el catálogo.
2. **Placeholder convention** (solo si falta el tema): caja con borde
   discontinuo y texto "Ilustración SURA · [tema] · [familia]".
3. Usa **una ilustración por bloque** — nunca combines dos en el mismo
   contenedor.
4. La ilustración va siempre sobre un **fondo contrastante** (gris claro
   `--bg-1`, blanco, o color de paleta complementaria).
5. Para mockups de **error / estado vacío / éxito**, usa la familia UX.
6. Para **landings de producto**, usa la familia Producto.
7. Para **emails y notificaciones transaccionales**, usa la familia CCM.
8. **No mezcles** pictogramas e ilustraciones en el mismo bloque — son
   niveles jerárquicos distintos (ilustración = primer nivel /
   pictograma = segundo-tercer nivel).

---

## 9. Pendiente

- [x] ~~Ingerir el banco oficial de ilustraciones~~ — **166 SVG instalados**
      en `assets/illustrations/`.
- [x] ~~Lista nominal por familia~~ — ver `ilustraciones-catalogo.md`.
- [ ] Confirmar **tamaños mínimos / máximos** recomendados por contexto
      (hero, card, modal, email).
- [ ] Definir paleta exacta permitida para ilustración (si difiere de la
      paleta principal de UI).
- [ ] Validar el **mapa tema→archivo** heurístico del catálogo con el equipo
      de marca.
