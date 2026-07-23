---
case_id: ed507b3d25f0bac0
tipo: Norma
estado: detectado
entidad: [[Agencia Nacional de Hidrocarburos (ANH)]]
linea_negocio: [[Transversal]]
riesgo: [[Riesgo Medio]]
impacto_ti: SÍ
ejecutado: NO
plazo: A partir de la publicación (inicio inmediato) y conforme a plazos del art. 4 de la Resolución 651 de 2025
tema: [[JSON IDP ANH v2.0]]
sox: NO
created: 2026-05-31
published: 2026-02-02
tags: [impacto_ti]
---







## Detalles del Hallazgo
- **Entidad Emisora:** [[Agencia Nacional de Hidrocarburos (ANH)]]
- **Tipo de Norma:** Norma
- **Fecha de Expedición:** No especificada
- **Fecha de Detección:** 2026-05-31
- **URL:** https://www.anh.gov.co/documents/33701/Circular_ANH_003_de_2026.pdf
- **Incidencia SURA:** 
- **Control SOX:** 

## Análisis
CIRCULAR No. 0003 DEL 02-02-2026
PARA: Compañías Operadoras de Contratos de Asociación, Contratos de Exploración
y Explotación (E&E), Contratos de Exploración y Producción (E&P), Convenios
de Explotación, Convenios de Exploración y Explotación.
DE: Vicepresidente de Operaciones, Regalías y Participaciones.
ASUNTO: Actualización del Anexo Técnico de Diseño de Archivo (JSON) Versión 2.0
para el intercambio de información de producción, en cumplimiento de la Resolución 651
de 2025 y sus modificaciones.
La presente Circular establece las orientaciones técnicas para la implementación,
diligenciamiento y envío del archivo JSON destinado a la generación del Informe Diario
de Producción (IDP), conforme a lo previsto en la Resolución 0651 de 2025 y sus
modificaciones, en el marco de las competencias de fiscalización de la Agencia Nacional
de Hidrocarburos – ANH, de acuerdo con la Ley 2056 de 2020, la Resolución 40236 de
2022 y la Resolución 40537 de 2024.
Las disposiciones contenidas en esta Circular aplican a todas las compañías operadoras
que administren campos productores ubicados en el territorio nacional y que en virtud del
artículo 2 y su parágrafo 1 de la Resolución 0651 de 2025 y sus modificaciones, deban
remitir información mediante el envío del archivo JSON para la generación del Informe
Diario de Producción, diferenciando su implementación de la siguiente manera:
1. CLASIFICACIÓN DEL ARCHIVO JSON PARA EL IDP (TIPO A / TIPO B).
Para efectos de implementación, el archivo JSON para la generación del informe diario
de producción (IDP) será clasificado como:
a. Tipo A: aplicable a los campos productores que se encuentren dentro del ámbito de
aplicación del artículo 2 de la Resolución 0651 de 2025 y sus modificaciones, en el cual
se reportará la información obtenida a partir de sistemas de telemetría (datos
automatizados) y cuando corresponda, información complementaria registrada de forma
manual.
b. Tipo B: aplicable a los campos productores que no se encuentren dentro del ámbito
de aplicación del artículo 2 de la Resolución 0651 de 2025 y sus modificaciones, en el
ANH-GDO-FR-16 Versión N° 3 Pág. 1 de 8
CIRCULAR No. 0003 DEL 02-02-2026
cual se reportará la información obtenida por medios no telemetrizados y registrada de
forma manual para la generación del IDP, conforme a las condiciones técnicas definidas
por la ANH.
En todo caso, el archivo JSON corresponde a un único formato estándar y la
diferenciación entre Tipo A y Tipo B obedece a la forma de obtención y registro de ciertos
datos, sin que ello implique la existencia de archivos o estructuras incompatibles entre sí.
2. CANALES DE ENTREGA Y RECEPCIÓN HABILITADOS PARA EL ARCHIVO
JSON.
La entrega del archivo JSON se realizará mediante los canales dispuestos por la ANH,
conforme al flujo de intercambio Operador–ANH descrito en la Figura 1 de la presente
Circular, así:
a. Canal de integración por API (API 1 – C1): Los operadores deberán remitir el archivo
JSON correspondiente (Tipo A o Tipo B) mediante el canal de integración por API
dispuesto por la ANH (API 1 – C1), conforme a las condiciones de seguridad,
autenticación, autorización, validación e ingesta definidas por la ANH.
En este canal:
i. el JSON Tipo A será generado a partir de la información consolidada en la Zona de
Entrega del operador (lago de datos), en coherencia con la arquitectura de telemetría
exigida para los campos dentro del artículo 2; y
ii. el JSON Tipo B podrá ser remitido por el mismo canal (API 1 – C1), aun cuando su
información provenga de procesos de captura y digitación manual (sin origen
telemetrizado), para campos por fuera del ámbito del artículo 2.
ANH-GDO-FR-16 Versión N° 3 Pág. 2 de 8
CIRCULAR No. 0003 DEL 02-02-2026
Figura 1. Arquitectura de intercambio de información (JSON Tipo A / JSON Tipo B)
Nota: El flujo API 1 (C1) admite el envío de JSON Tipo A y JSON Tipo B. Adicionalmente,
para continuidad operacional, el JSON Tipo B podrá ingresar por los canales E1 (manual)
y E2 (automatizado), según aplique.
b. Canales actualmente operativos del IDP (E1 y E2) – Aplicables al JSON Tipo B:
Sin perjuicio del canal de integración por API y con el propósito de asegurar continuidad
operativa en el reporte del IDP, se mantendrán los canales actualmente utilizados para
el ingreso del IDP, según se muestra en la Figura 1, así:
iii. E1 (Registro manual): cuando el operador no cuente con un sistema de medición
volumétrica compatible con el sistema de medición volumétrica de la ANH, o no
disponga de sistema de medición volumétrica, la información que actualmente se
entrega mediante plantillas en Excel será reemplazada por el archivo JSON Tipo B,
conforme a lo establecido en la presente Circular.
iv.E2 (Registro automatizado): cuando el operador cuente con un sistema de medición
volumétrica compatible con el sistema de medición volumétrica de la ANH, el
intercambio automático de información se realizará mediante archivo JSON Tipo B,
conforme a las disposiciones técnicas de interoperabilidad definidas por la ANH.
ANH-GDO-FR-16 Versión N° 3 Pág. 3 de 8
