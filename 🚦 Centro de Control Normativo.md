# 🚦 Centro de Control Normativo - SURA

Este tablero permite filtrar la normativa de forma rápida utilizando las propiedades inteligentes extraídas por la IA. 

> [!TIP] Instrucción de Uso
> Haz clic en la lupa de cada sección para ver los documentos filtrados. Los resultados se actualizan automáticamente con cada nueva corrida del sistema.

---

## 🚨 Alarmas de Riesgo Sancionatorio
Documentos que mencionan multas, plazos cortos o medidas cautelares.

### 🔴 Riesgo Crítico / Alto
```query
[riesgo:Crítico] OR [riesgo:Alto]
```

### 🟠 Riesgo Medio
```query
[riesgo:Medio]
```

---

## 💻 Impacto Tecnológico (TI)
Normativa que requiere cambios en sistemas, bases de datos o reportes digitales.

### 🔵 Requiere Ajustes TI
```query
[impacto_ti:SÍ]
```

---

## 🏢 Filtro por Línea de Negocio
Visualiza el impacto específico por filial o sector.

### 🏥 Salud (EPS / IPS)
```query
[linea_negocio:Salud]
```

### 🛡️ Seguros (Vida / Generales / ARL)
```query
[linea_negocio:Vida] OR [linea_negocio:Generales] OR [linea_negocio:ARL]
```

### 💰 Pensiones y Asset Management
```query
[linea_negocio:Pensiones]
```

### 🌐 Transversal (Holding)
```query
[linea_negocio:Transversal]
```

---

## ✅ Ejecución y Publicación
Seguimiento de normas que ya han sido gestionadas o comunicadas.

### 📢 Ya Publicados / Ejecutados
```query
[ejecutado:SÍ] OR tag:#publicado
```

### ⏳ Pendientes de Ejecución
```query
[ejecutado:NO] [estado:consolidado]
```

---

## 📅 Gestión de la Última Corrida
Documentos detectados recientemente que aún no han sido procesados formalmente.

### 🆕 Pendientes de Validación Humana
```query
[estado:detectado]
```

### ✅ Validados / Consolidados
```query
[estado:validado] OR [estado:consolidado]
```

---

## 🛠️ Herramientas de Análisis
- [[Tablero Kanban Cumplimiento|📋 Ver Kanban de Trabajo]]
- [[Tablero Visual Cumplimiento|📊 Ver Reporte Visual]]
