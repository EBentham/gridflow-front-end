"""crop.py name x0 y0 x1 y1 out [scale]"""
import sys
from PIL import Image
n, x0, y0, x1, y1, out = sys.argv[1], *map(int, sys.argv[2:6]), sys.argv[6]
sc = float(sys.argv[7]) if len(sys.argv) > 7 else 1
im = Image.open(f"shots/{n}.png").crop((x0, y0, x1, y1))
im.resize((int(im.width * sc), int(im.height * sc))).save(f"shots/{out}.png")
