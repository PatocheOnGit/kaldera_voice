# -*- coding: utf-8 -*-
"""
Kaldera Voice: recolors the Plasmo Voice icons to the Kaldera palette (warm inks, magma, ruby, topaz) and puts
the Kaldera logo where the Plasmo logo was. Reads the upstream icons from git (the 2.2.0-beta.3 commit), so it can
run again at any time. The recolored icons derive from Plasmo Voice's and stay under the LGPL-3.0.

    python kaldera/recolor_icons.py [output_dir]

Without output_dir, writes into client/src/main/resources/assets/plasmovoice/textures/icons.
"""
import colorsys
import io
import subprocess
import sys
from pathlib import Path

from PIL import Image

UPSTREAM = "198ad94af569492cd5151ecd67668628403edd10"
ICONS = "client/src/main/resources/assets/plasmovoice/textures/icons"
ROOT = Path(__file__).resolve().parent.parent
LOGO = ROOT / "kaldera" / "logo.png"

INK_DARK = (0x3A, 0x3A, 0x43)
INK_LIGHT = (0xF4, 0xED, 0xE6)
MAGMA_DARK = (0xA8, 0x32, 0x06)
MAGMA_LIGHT = (0xFF, 0x8A, 0x45)

# The plain microphone and speaker (shown when talking and hearing) take the magma tint.
MAGMA_ICONS = {"microphone.png", "speaker.png", "microphone_menu.png", "speaker_menu.png"}


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def recolor_pixel(r, g, b, magma):
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    if s < 0.22:
        # Greys and whites: warm ink gradient (magma gradient for the main icons), shading kept.
        return lerp(MAGMA_DARK, MAGMA_LIGHT, v) if magma else lerp(INK_DARK, INK_LIGHT, v)
    hue = h * 360
    if 70 <= hue <= 170 or 180 <= hue <= 260:
        target = 22  # greens and blues (groups, radio, activity): magma
    elif hue < 20 or hue > 330:
        target = 350  # reds (muted, disabled): ruby
    else:
        target = 37  # oranges and yellows (priority): topaz
    return tuple(round(c * 255) for c in colorsys.hsv_to_rgb(target / 360, min(1.0, s * 1.05), v))


def upstream(path):
    data = subprocess.run(["git", "show", f"{UPSTREAM}:{path}"], cwd=ROOT, capture_output=True, check=True).stdout
    return Image.open(io.BytesIO(data)).convert("RGBA")


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / ICONS
    names = subprocess.run(["git", "ls-tree", "-r", "--name-only", UPSTREAM, ICONS], cwd=ROOT, capture_output=True,
                           check=True, text=True).stdout.split()
    for path in names:
        relative = path[len(ICONS) + 1:]
        target = out / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if relative == "tabs/plasmo.png":
            Image.open(LOGO).convert("RGBA").resize((16, 16), Image.LANCZOS).save(target)
            continue
        image = upstream(path)
        magma = Path(relative).name in MAGMA_ICONS
        pixels = image.load()
        for y in range(image.height):
            for x in range(image.width):
                r, g, b, a = pixels[x, y]
                if a:
                    pixels[x, y] = (*recolor_pixel(r, g, b, magma), a)
        image.save(target)
    print(f"{len(names)} icons written to {out}")


if __name__ == "__main__":
    main()
