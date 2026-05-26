This is your new *vault*.

Make a note of something, [[create a link]], or try [the Importer](https://help.obsidian.md/Plugins/Importer)!

When you're ready, delete this note and make the vault your own.
## Pendientes de Enlaces (Fuentes Normativas)

```csvtable
source: data/pendientes_enlaces.csv
columns:
- hoja
- fila
- entidad
- enlace_actual
filter:
- enlace_actual == "(vacío)" or enlace_actual == "Link" or enlace_actual == "link"
sortBy:
- hoja
- fila
maxRows: 1000
```
