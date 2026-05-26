# Tablero de Control de Cumplimiento

## 1) Casos por Revisar (pendientes revisión manual)
```csvtable
source: data/casos_detectados.csv
columns:
- case_id
- detected_at
- entidad
- document_url
- status
- priority
- aplica_sura
- notes
filter:
- status == "detectado" or status == "extraido_ia" or status == "en_validacion"
sortBy:
- expression: detected_at
  reversed: true
maxRows: 500
```

## 2) Casos Consolidados (ya cerrados)
```csvtable
source: data/casos_detectados.csv
columns:
- case_id
- detected_at
- entidad
- status
- priority
- aplica_sura
- notes
filter:
- status == "consolidado"
sortBy:
- expression: detected_at
  reversed: true
maxRows: 500
```

## 3) Casos Rechazados (no aplican o descartados)
```csvtable
source: data/casos_detectados.csv
columns:
- case_id
- detected_at
- entidad
- status
- aplica_sura
- notes
filter:
- status == "rechazado" or aplica_sura == "no"
sortBy:
- expression: detected_at
  reversed: true
maxRows: 500
```

## 4) Cambios Detectados (nuevos casos)
```csvtable
source: data/casos_detectados.csv
columns:
- detected_at
- entidad
- document_url
- status
- priority
- aplica_sura
sortBy:
- expression: detected_at
  reversed: true
maxRows: 200
```

## 5) Alta Prioridad
```csvtable
source: data/casos_detectados.csv
columns:
- case_id
- detected_at
- entidad
- status
- priority
- aplica_sura
- notes
filter:
- priority == "alta"
sortBy:
- expression: detected_at
  reversed: true
maxRows: 500
```

## Estados sugeridos
- `detectado` -> `extraido_ia` -> `en_validacion` -> `validado`/`rechazado` -> `consolidado`
