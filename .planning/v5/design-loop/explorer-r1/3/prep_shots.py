"""Crop and re-encode the pack's screenshots into explorer-shots/ (WebP).

Desktop: the top 1440 x 811 of each screen (the window body is 1101 x 620 css px), which also keeps the rail's
foot out of frame. Phone: one 440 x 520 crop per screen, the part of the screen that reads at phone width.

Usage: PYTHONPATH=_tools python prep_shots.py
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
SRC = HERE.parent.parent / "explorer-pack" / "shots"
OUT = HERE / "explorer-shots"

DESK_H = 811
# (left, top) of each phone crop, in screenshot pixels
PHONE = {
    "catalogue": (110, 330),
    "generation-mix": (122, 176),
    "market-index-price": (122, 380),
    "historic-mix": (122, 430),
}
PW, PH = 440, 520


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for stem, (x, y) in PHONE.items():
        for theme in ("light", "dark"):
            im = Image.open(SRC / f"{stem}-{theme}.png").convert("RGB")
            im.crop((0, 0, 1440, DESK_H)).save(OUT / f"{stem}-{theme}.webp", "WEBP", quality=82, method=6)
            im.crop((x, y, x + PW, y + PH)).save(OUT / f"{stem}-{theme}-crop.webp", "WEBP", quality=86, method=6)
    total = 0
    for p in sorted(OUT.iterdir()):
        total += p.stat().st_size
        print(f"{p.name:44} {p.stat().st_size:>8,}")
    print(f"total {total:,}")


if __name__ == "__main__":
    main()
