"""Build arch-3.dc.html: pass 1 (probe) -> measure.json -> pass 2 (draw). Usage: build3.py [--reuse]."""
from __future__ import annotations

import json
import sys

import p3
from frame import HERE, MEAS_F, check, measure, shell, static

if __name__ == "__main__":
    reuse = "--reuse" in sys.argv and MEAS_F.exists()
    if reuse:
        m = json.loads(MEAS_F.read_text(encoding="utf-8"))
    else:
        m = measure(p3.NAME, shell(p3.TITLE, p3.CSS, "<main>" + p3.html_body() + "</main>", 9000, probe=True))
        MEAS_F.write_text(json.dumps(m, indent=1), encoding="utf-8")
    bg, H, plate = p3.draw(m)
    out = shell(p3.TITLE, p3.CSS, bg + "\n<main>\n" + p3.html_body(plate) + "\n</main>", H)
    check(out)
    (HERE / f"{p3.NAME}.dc.html").write_text(out, encoding="utf-8")
    (HERE / "static" / f"{p3.NAME}.html").write_text(static(out), encoding="utf-8")
    print("H =", H, {k: [round(a), round(b)] for k, (a, b) in m["secs"].items()})
    print("over", m.get("over"))
    print("scroll", m.get("scroll"))
