#!/usr/bin/env python3
"""
Render a UI mockup to PNG.

Supports two input formats:
  - SVG (recommended for pixel-perfect modern UI mockups)
  - HTML (rendered via LibreOffice — limited CSS support)

Usage:
  python scripts/render_mockup.py --input working/mockup.svg --output output/mockup.png
  python scripts/render_mockup.py --input working/mockup.html --output output/mockup.png --width 1440 --height 900
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def render_svg(input_path: Path, output_path: Path, width: int | None, height: int | None) -> None:
    """Render SVG → PNG using cairosvg."""
    import cairosvg

    kwargs = {"url": str(input_path), "write_to": str(output_path)}
    if width:
        kwargs["output_width"] = width
    if height:
        kwargs["output_height"] = height
    cairosvg.svg2png(**kwargs)


def render_html(input_path: Path, output_path: Path, width: int, height: int) -> None:
    """Render HTML → PNG via soffice → pdftoppm.

    Note: LibreOffice has limited support for modern CSS (flexbox, grid,
    advanced shadows). For complex layouts prefer SVG.
    """
    if not shutil.which("soffice"):
        raise RuntimeError("soffice (LibreOffice) no está disponible.")
    if not shutil.which("pdftoppm"):
        raise RuntimeError("pdftoppm no está disponible.")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        # 1. HTML → PDF
        result = subprocess.run(
            ["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(tmp_path), str(input_path)],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode != 0:
            raise RuntimeError(f"soffice falló: {result.stderr}")

        pdf_files = list(tmp_path.glob("*.pdf"))
        if not pdf_files:
            raise RuntimeError("soffice no produjo PDF.")
        pdf_path = pdf_files[0]

        # 2. PDF → PNG. Resolution chosen so output approximates target width.
        # pdftoppm renders at DPI; we estimate DPI to hit the requested width.
        # Default A4 width is 8.27in; for a 1440px target → ~174 DPI.
        target_dpi = max(96, int(width / 8.27))
        out_prefix = tmp_path / "page"
        result = subprocess.run(
            ["pdftoppm", "-png", "-r", str(target_dpi), str(pdf_path), str(out_prefix)],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode != 0:
            raise RuntimeError(f"pdftoppm falló: {result.stderr}")

        png_files = sorted(tmp_path.glob("page-*.png"))
        if not png_files:
            raise RuntimeError("pdftoppm no produjo PNG.")

        # If multiple pages, take the first.
        from PIL import Image

        img = Image.open(png_files[0])
        # Resize to exact target dimensions if requested.
        if width and height:
            img = img.resize((width, height), Image.LANCZOS)
        img.save(output_path, "PNG")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True, help="Ruta al archivo .svg o .html")
    ap.add_argument("--output", required=True, help="Ruta del PNG de salida")
    ap.add_argument("--width", type=int, default=1440, help="Ancho del mockup (px). Default: 1440")
    ap.add_argument("--height", type=int, default=900, help="Alto del mockup (px). Default: 900")
    args = ap.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"ERROR: no existe el archivo de entrada: {input_path}", file=sys.stderr)
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)

    ext = input_path.suffix.lower()
    try:
        if ext == ".svg":
            render_svg(input_path, output_path, args.width, args.height)
        elif ext in (".html", ".htm"):
            render_html(input_path, output_path, args.width, args.height)
        else:
            print(f"ERROR: formato no soportado: {ext}. Use .svg o .html", file=sys.stderr)
            return 1
    except Exception as e:
        print(f"ERROR durante renderizado: {e}", file=sys.stderr)
        return 1

    size_kb = output_path.stat().st_size / 1024
    print(f"OK: {output_path} ({size_kb:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
