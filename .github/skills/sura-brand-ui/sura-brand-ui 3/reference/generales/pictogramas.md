# Pictogramas — Sistema de Diseño SURA

Fuente: Manual de marca, sección "Pictogramas".

---

## 1. Concepto

Los pictogramas SURA se destacan por su **evidencia, literalidad y carácter
lúdico**. Tienen un alto grado de simplificación y un nivel de detalle mínimo.
Logran ser igual de ricos en contenido que una ilustración, pero con la
**concisión y simplicidad de un ícono**.

> **Regla crítica de jerarquía:** los pictogramas ilustran información de
> **segundo y tercer nivel de lectura**. **Nunca** se usan como portadas o
> aperturas de contenido — para eso se usan ilustraciones.

---

## 2. Anatomía

| # | Regla | Detalle |
|---|---|---|
| 1 | **Colores** | No más de **5 colores**, no menos de **3** |
| 2 | **Elementos** | Pocos elementos por pictograma |
| 3 | **Tono** | Situaciones lúdicas, divertidas y obvias |
| 4 | **Identificador** | Imagen que comunica el concepto de forma inmediata |
| 5 | **Construcción** | **100 % vectoriales**, sin efectos ni gradientes |

---

## 3. Tamaños autorizados

Existen **tres versiones** de tamaño:

| Versión | Tamaño |
|---|---|
| Grande | **150 px** |
| Medio | **100 px** |
| Pequeño | **60 px** |

> Los tres tamaños son cuadrados (lado × lado). Para tamaños intermedios,
> reduce al inmediatamente inferior — no inventes valores.

---

## 4. Contexto de uso

Los pictogramas son **soporte** para piezas digitales o web que **refuerzan
el concepto del Call to Action**.

### Ejemplos de uso correcto

- Como ícono identificador de un producto en una grilla de servicios
  (ej. EPS, ARL, IPS, Diagnósticas, Pago Express).
- Acompañando bloques de "Conoce tus beneficios", "Nuestros accionistas",
  etc.
- En cards de servicios o secciones de navegación de segundo nivel.

### Ubicación típica en pantalla

- Grids de servicios (4 columnas con pictograma + título + descripción).
- Sidebar / quick actions.
- Headers de sección secundaria.

**Nunca** en:
- Heroes / banners principales.
- Aperturas de página o portadas.
- Como única forma de identificar una acción crítica (siempre acompañar
  con texto).

---

## 5. Usos incorrectos

**Nunca:**

1. Utilizar pictogramas con una **línea de estilo o trazo diferentes** a los
   suministrados oficialmente.
2. Modificar o utilizar **colores diferentes** a la paleta establecida para
   ilustración y pictogramas (ver `colores.md`, §5 «Paleta para ilustraciones»).
3. Hacer composiciones con **2 o más pictogramas** combinados para ilustrar
   situaciones — un pictograma representa un concepto.
4. **Enmascarar o cortar** pictogramas dentro de contenedores geométricos
   o destacados.
5. Aplicar **efectos, gradientes o sombras** sobre el pictograma.
6. Cambiar la proporción / escalar de forma no uniforme.

---

## 6. Reglas operativas para el skill

1. Los pictogramas son **assets vectoriales suministrados aparte**. En
   mockups, referencia por nombre (`pictogram-eps.svg`, etc.) y marca como
   pendiente si el SVG no está disponible.
2. Usa los tres tamaños oficiales (60, 100, 150 px) — para tamaños
   intermedios, usa el inmediatamente inferior.
3. **Siempre acompaña** el pictograma con un texto de apoyo (título o label).
4. En grids de servicios, alinea el pictograma **centrado horizontalmente**
   respecto al texto debajo.
5. Color de fondo del contenedor donde va el pictograma: prefiere blanco
   (`#FFFFFF`) o `--bg-1` (gris claro de la paleta).
6. **Espaciado mínimo** entre pictograma y el texto debajo: `--space-2`
   (16 px). Entre pictogramas adyacentes: `--space-4` (32 px).
7. No combines pictogramas con ilustraciones en el mismo bloque — son
   niveles jerárquicos distintos.

---

## 7. Pendiente

- [ ] Ingerir el **set de SVG oficiales** de pictogramas a `assets/pictograms/`
      cuando estén disponibles.
- [ ] Documentar la **lista nominal** de pictogramas existentes (productos,
      acciones, conceptos) para validar nombres exactos.
- [ ] Confirmar la **paleta exacta** permitida para pictogramas (¿toda la
      paleta principal? ¿solo paleta ilustraciones?).
