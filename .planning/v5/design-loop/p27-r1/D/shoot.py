"""Headless Edge screenshots of a board, in slices (Edge dies on very tall windows)."""
from __future__ import annotations
import subprocess, sys, json
from pathlib import Path
HERE = Path(__file__).parent
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
H = json.loads((HERE / "heights.json").read_text())
def shot(slug: str, y: int, h: int = 1400, name: str | None = None) -> None:
    src = (HERE / "static" / f"D-{slug}.html").read_text(encoding="utf-8")
    crop = src.replace("<style>", f"<style>.root{{margin-top:-{y}px}}", 1)
    (HERE / "static" / "_crop.html").write_text(crop, encoding="utf-8")
    out = HERE / "shots" / (name or f"{slug}_{y}.png")
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={HERE / '.edge'}",
                    f"--window-size=1440,{h}", f"--screenshot={out}", f"http://localhost:9644/_crop.html?y={y}"],
                   capture_output=True, timeout=90)
    print(out.name, out.exists())
if __name__ == "__main__":
    slug = sys.argv[1]
    ys = [int(a) for a in sys.argv[2:]] or list(range(0, H[slug], 1300))
    for y in ys:
        shot(slug, y)
