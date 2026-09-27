"""Screenshot a page in headless Chrome (own profile) and cut it into slices: shoot.py url_path name height [band] [scale]."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
UD = r"C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\a0012501-ff9a-440a-b654-cec67ac10bcf\scratchpad\chrome-ud"
url, name, h = sys.argv[1], sys.argv[2], int(sys.argv[3])
band = int(sys.argv[4]) if len(sys.argv) > 4 else 1000
sc = float(sys.argv[5]) if len(sys.argv) > 5 else .7
out = HERE / "shots" / f"{name}.png"
subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={UD}",
                f"--window-size=1440,{h}", "--virtual-time-budget=9000", f"--screenshot={out}",
                f"http://127.0.0.1:9731/{url}"], capture_output=True, timeout=120)
im = Image.open(out)
w, H = im.size
i, a = 0, 0
while a < H:
    b = min(H, a + band)
    im.crop((0, a, w, b)).resize((int(w * sc), int((b - a) * sc))).save(HERE / "shots" / f"{name}_{i}.png")
    i += 1
    a = b
print(w, H, i)
