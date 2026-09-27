"""Build the four boards: pass 1 (probe) -> measure.json -> pass 2 (draw). Usage: build.py [page ...] [--reuse]."""
from __future__ import annotations

import importlib
import json
import sys

import frame
from frame import HERE, MEAS_F, check, measure, shell, static

PAGES = {"sources": "p_sources", "elexon": "p_elexon", "arch": "p_arch", "models": "p_models"}


def build(key: str, reuse: bool, meas: dict) -> None:
    mod = importlib.import_module(PAGES[key])
    frame.COPY.pop(mod.PG, None)
    body, css = mod.html()
    title = mod.TITLE if hasattr(mod, "TITLE") else mod.NAME
    if reuse and mod.NAME in meas:
        m = meas[mod.NAME]
    else:
        m = measure(mod.NAME, shell(title, css, "<main>" + body + "</main>", 6000, probe=True))
        meas[mod.NAME] = m
    layers, H = mod.draw(m)
    frame.COPY.pop(mod.PG, None)
    body, css = mod.html()
    out = shell(title, css, layers + "\n<main>\n" + body + "\n</main>", H)
    check(out)
    (HERE / f"{mod.NAME}.dc.html").write_text(out, encoding="utf-8")
    (HERE / "static" / f"{mod.NAME}.html").write_text(static(out), encoding="utf-8")
    print(mod.NAME, "H =", H, "secs", {k: [round(a), round(b)] for k, (a, b) in m["secs"].items()},
          "over", m.get("over"), "fonts", len(m.get("fonts", "").split("|")))
    (HERE / f"copy-{mod.PG}.json").write_text(json.dumps(frame.COPY.get(mod.PG, []), ensure_ascii=False, indent=1),
                                            encoding="utf-8")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    reuse = "--reuse" in sys.argv
    meas = json.loads(MEAS_F.read_text(encoding="utf-8")) if MEAS_F.exists() else {}
    for k in args or list(PAGES):
        build(k, reuse, meas)
    MEAS_F.write_text(json.dumps(meas, indent=1), encoding="utf-8")
