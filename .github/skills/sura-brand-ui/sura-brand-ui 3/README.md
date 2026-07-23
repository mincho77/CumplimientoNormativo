# Instalacion y uso del skill

## Ubicacion canonica

Este skill vive en:

- `.github/skills/sura-brand-ui/`

El nombre del skill siempre debe ser `sura-brand-ui` en el frontmatter de `SKILL.md`.

## Como invocarlo

- En chat, usar `/sura-brand-ui`.

## Modos disponibles

- `GENERAR`: mockups UI web/movil con PNG + especificaciones.
- `AUDITAR`: ajuste de codigo existente a marca SURA.
- `PRESENTAR`: presentaciones HTML interactivas y navegables.

## Instalar en otros agentes/proyectos

Copiar la carpeta completa `sura-brand-ui` a cualquiera de estas rutas:

- Proyecto: `.github/skills/sura-brand-ui/`
- Proyecto: `.agents/skills/sura-brand-ui/`
- Proyecto: `.claude/skills/sura-brand-ui/`
- Personal (Windows): `%USERPROFILE%/.copilot/skills/sura-brand-ui/`
- Personal (Windows): `%USERPROFILE%/.agents/skills/sura-brand-ui/`
- Personal (Windows): `%USERPROFILE%/.claude/skills/sura-brand-ui/`

## Dependencias para render (cuando aplique)

Python:

```bash
pip install -r requirements.txt
```

- `cairosvg`: render SVG a PNG.
- `Pillow`: resize/procesamiento de imagen.

Dependencias del sistema (opcionales segun flujo):

- `fc-cache` (fontconfig): registrar fuentes.
- `soffice` (LibreOffice): render desde HTML.
- `pdftoppm` (poppler): conversion intermedia en flujo HTML.

## Build de distribucion (3 tipos)

Script de build:

- `scripts/build_portable_catalog_zip.ps1`

Comando recomendado para release:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\build_portable_catalog_zip.ps1 -Build all -Version 02.01.00
```

Salidas:

- `sura-brand-ui-v<Version>-portable.zip` (liviano, sin ilustraciones)
- `sura-brand-ui-v<Version>-full.zip` (con ilustraciones catalogadas)
- `sura-brand-ui-v<Version>-original.zip` (assets en formato original)

En todos los ZIP, la carpeta interna es `sura-brand-ui`.

## Compartir con el equipo

1. Editar solo `.github/skills/sura-brand-ui/`.
2. Ejecutar build con `-Build all`.
3. Publicar los 3 ZIP versionados.

---

© SURA. Material corporativo de marca para uso interno y equipos/proveedores autorizados.

No se concede redistribucion publica ni uso por terceros sin autorizacion expresa de SURA.

Desarrollado en la Direccion de Aceleracion de Capacidades por Alejandro Jimenez Zapata y Mauricio Otalvaro Ospina.

Ver `NOTICE` para los terminos de uso.
