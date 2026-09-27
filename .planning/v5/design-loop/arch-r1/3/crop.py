"""Crop a tall board PNG into readable slices: crop.py name [band_px] [scale]."""
from __future__ import annotations
import sys
from PIL import Image
name = sys.argv[1]
band = int(sys.argv[2]) if len(sys.argv) > 2 else 1100
sc = float(sys.argv[3]) if len(sys.argv) > 3 else .75
im = Image.open(f"shots/{name}.png")
w, h = im.size
i, a = 0, 0
while a < h:
    b = min(h, a + band)
    im.crop((0, a, w, b)).resize((int(w * sc), int((b - a) * sc))).save(f"shots/{name}_{i}.png")
    i += 1
    a = b
print(w, h, i)
