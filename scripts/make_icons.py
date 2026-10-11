#!/usr/bin/env python3
"""Renders favicon.ico and apple-touch-icon.png from favicon.svg.

Chrome draws the SVG, so the PNGs match what browsers show for the SVG. Run it
after changing favicon.svg and commit all three files.

Usage: python3 -I scripts/make_icons.py
"""
import os
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SVG = ROOT / "favicon.svg"
CHROME = os.environ.get(
    "CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
)
ICO_SIZES = (16, 32, 48)
# iOS rounds the corners itself and fills transparency with black, so the
# touch icon is a full square in the tile colour.
TOUCH_SIZE = 180
TILE = "#15181a"


def render(size, background, tmp):
    page = tmp / f"icon-{size}.html"
    out = tmp / f"icon-{size}.png"
    page.write_text(
        "<style>html,body{margin:0;overflow:hidden;background:%s}img{display:block}</style>"
        '<img src="%s" width="%d" height="%d">'
        % (background, SVG.as_uri(), size, size),
        encoding="utf-8",
    )
    subprocess.run(
        [
            CHROME,
            "--headless",
            "--disable-gpu",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            "--default-background-color=00000000",
            f"--user-data-dir={tmp / 'profile'}",
            f"--window-size={size},{size}",
            f"--screenshot={out}",
            page.as_uri(),
        ],
        check=True,
        capture_output=True,
    )
    data = out.read_bytes()
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (size, size):
        sys.exit(f"Chrome rendered {width}x{height} instead of {size}x{size}")
    return data


def ico(pngs):
    """An ICO file holding PNG images, which every current browser reads."""
    header = struct.pack("<HHH", 0, 1, len(pngs))
    offset = len(header) + 16 * len(pngs)
    entries = b""
    for size, data in pngs:
        entries += struct.pack("<BBBBHHII", size, size, 0, 0, 1, 32, len(data), offset)
        offset += len(data)
    return header + entries + b"".join(data for _, data in pngs)


with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    pngs = [(size, render(size, "transparent", tmp)) for size in ICO_SIZES]
    (ROOT / "favicon.ico").write_bytes(ico(pngs))
    (ROOT / "apple-touch-icon.png").write_bytes(render(TOUCH_SIZE, TILE, tmp))

print("Wrote favicon.ico and apple-touch-icon.png")
