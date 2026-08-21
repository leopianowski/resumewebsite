#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera os assets de favicon a partir de static/icons/favicon.svg.

    python make_favicon.py

O SVG é a fonte de verdade — para mudar o ícone, edite ele e rode isto.
Produz, ao lado dele:

    static/icons/favicon.ico          16 + 32 + 48 px (payloads PNG)
    static/icons/apple-touch-icon.png 180 px, fundo quadrado e opaco

Os rasterizados são versionados de propósito: rasterizar exige um browser, e
depender disso no CI seria frágil. Rode local e commite o resultado.

Rasteriza com o Chrome/Edge que já está instalado (headless), e monta o .ico
com struct + zlib da stdlib. Nenhuma dependência a instalar.

Roda raramente — o build normal (`python build.py`) não depende disto.
"""

from __future__ import annotations

import struct
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent
ICONS = ROOT / "static" / "icons"
SVG = ICONS / "favicon.svg"
ICO = ICONS / "favicon.ico"
APPLE = ICONS / "apple-touch-icon.png"

ICO_SIZES = (16, 32, 48)
APPLE_SIZE = 180

BROWSERS = (
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
)


def find_browser() -> str:
    for path in BROWSERS:
        if Path(path).exists():
            return path
    sys.exit("[erro] Chrome ou Edge não encontrado — necessário para rasterizar.")


def rasterize(browser: str, svg_markup: str, size: int, out: Path) -> None:
    """Renderiza `svg_markup` num PNG de size x size com fundo transparente."""
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "icon.html"
        page.write_text(
            "<!DOCTYPE html><html><head><meta charset='utf-8'><style>"
            "html,body{margin:0;padding:0;background:transparent}"
            f"svg{{display:block;width:{size}px;height:{size}px}}"
            f"</style></head><body>{svg_markup}</body></html>",
            encoding="utf-8",
        )
        subprocess.run(
            [
                browser,
                "--headless=new",
                "--disable-gpu",
                "--hide-scrollbars",
                "--force-device-scale-factor=1",
                "--default-background-color=00000000",  # fundo transparente
                f"--window-size={size},{size}",
                f"--screenshot={out}",
                page.as_uri(),
            ],
            check=True,
            capture_output=True,
        )


def write_ico(pngs: list[tuple[int, bytes]], out: Path) -> None:
    """
    Monta um .ico com payloads PNG.

    ICONDIR:   reserved(2)=0 | type(2)=1 | count(2)
    ICONDIRENTRY: w(1) h(1) colors(1)=0 reserved(1)=0 planes(2)=1
                  bpp(2)=32 bytes(4) offset(4)
    Tamanho 256 é gravado como 0, por definição do formato.
    """
    header = struct.pack("<HHH", 0, 1, len(pngs))
    offset = len(header) + 16 * len(pngs)
    entries, blobs = [], []
    for size, blob in pngs:
        dim = 0 if size >= 256 else size
        entries.append(
            struct.pack("<BBBBHHII", dim, dim, 0, 0, 1, 32, len(blob), offset)
        )
        offset += len(blob)
        blobs.append(blob)
    out.write_bytes(header + b"".join(entries) + b"".join(blobs))


def main() -> int:
    if not SVG.exists():
        sys.exit(f"[erro] {SVG} não encontrado.")

    browser = find_browser()
    svg = SVG.read_text(encoding="utf-8")
    print(f"[ok] rasterizando com {Path(browser).name}")

    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)

        # .ico — mantém os cantos arredondados e a transparência
        pngs = []
        for size in ICO_SIZES:
            png = tmpdir / f"{size}.png"
            rasterize(browser, svg, size, png)
            pngs.append((size, png.read_bytes()))
            print(f"     {size}x{size} -> {len(pngs[-1][1]):,} bytes")
        write_ico(pngs, ICO)
        print(f"[ok] {ICO.relative_to(ROOT).as_posix()} — "
              f"{', '.join(str(s) for s in ICO_SIZES)} px, {ICO.stat().st_size:,} bytes")

        # apple-touch-icon — o iOS aplica a própria máscara e ignora alpha,
        # então aqui o fundo vai quadrado e opaco.
        square = svg.replace('rx="14"', 'rx="0"').replace('rx="13"', 'rx="0"')
        png = tmpdir / "apple.png"
        rasterize(browser, square, APPLE_SIZE, png)
        APPLE.write_bytes(png.read_bytes())
        print(f"[ok] {APPLE.relative_to(ROOT).as_posix()} — "
              f"{APPLE_SIZE} px, {APPLE.stat().st_size:,} bytes")

    return 0


if __name__ == "__main__":
    sys.exit(main())
