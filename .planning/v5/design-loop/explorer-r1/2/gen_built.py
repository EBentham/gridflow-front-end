"""Explorer page, "How it's built": three wording variations of the section, the request drawing kept.

A "Plain": a line each for front end and backend, headline technologies only.
B "What it does": three verb-led lines, each level with the part of the drawing it describes.
C "Let the drawing speak": no columns; the drawing's labels carry the technology, one short paragraph under it.

Section-only boards (topsoil into silver into gold). Reuses gen.py's drawing parts.
Usage: gen_built.py [a] [b] [c]   probes on 127.0.0.1:9772 (this folder).
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import html  # noqa: E402
import importlib.util  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).parent
_spec = importlib.util.spec_from_file_location("explorer_gen", HERE / "gen.py")
g = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(g)  # type: ignore[union-attr]

f, hp, frame, mg = g.f, g.hp, g.frame, g.mg
W, PW = g.W, g.PW
INK, DAY, T_TOP, T_SILVER, T_GOLD = g.INK, g.DAY, g.T_TOP, g.T_SILVER, g.T_GOLD
cab, terminal = g.cab, g.terminal

NEW: dict[str, list[str]] = {}
CUR = ""


def N(s: str) -> str:
    NEW.setdefault(CUR, []).append(s)
    return s


H2 = "How it’s built"

# ---------------------------------------------------------------- copy
A_FE = "React and TypeScript, drawing every dataset as charts and tables, in light and dark."
A_BE = "Python, with a FastAPI backend that reads gridflow’s silver and gold tables through DuckDB, read-only."
B_LINES = [
    ("Draws every dataset as charts and tables, in light and dark", "React and TypeScript"),
    ("Serves each dataset’s rows to the page", "a Python API built with FastAPI"),
    ("Reads gridflow’s silver and gold tables, read-only", "DuckDB, through gridflow’s own client"),
]
C_PARA = ("The front end is React and TypeScript; the backend is Python. Open a dataset and the page asks the FastAPI "
          "backend for it, which reads it from gridflow’s silver and gold tables through DuckDB, read-only.")
C_LABELS = ["the page: React and TypeScript", "the API: Python and FastAPI",
            '<tspan class="m">GridflowClient</tspan>, gridflow’s own client', "DuckDB over silver and gold, read-only"]
C_LABELS_PH = ["the page: React, TypeScript", "the API: Python, FastAPI",
               '<tspan class="m">GridflowClient</tspan>', "DuckDB, read-only"]


# ---------------------------------------------------------------- section bodies
def sec_a() -> str:
    return (f'<section class="built va" data-section="built" aria-labelledby="h-built"><h2 id="h-built" data-t="bh">'
            f'{H2}</h2><div class="bcol"><div class="fe" data-t="fe"><h3>Front end</h3><p>{N(A_FE)}</p></div>'
            f'<div class="be" data-t="be"><h3>Backend</h3><p>{N(A_BE)}</p></div></div>'
            f'<div class="bspace" data-t="bspace"></div></section>')


def sec_b() -> str:
    li = "".join(f'<li data-t="i{k}"><p>{N(w)}: <span class="tech">{N(t)}</span>.</p></li>'
                 for k, (w, t) in enumerate(B_LINES))
    return (f'<section class="built vb" data-section="built" aria-labelledby="h-built"><h2 id="h-built" data-t="bh">'
            f'{H2}</h2><ul class="does">{li}</ul><div class="bspace" data-t="bspace"></div></section>')


def sec_c() -> str:
    return (f'<section class="built vc" data-section="built" aria-labelledby="h-built"><h2 id="h-built" data-t="bh">'
            f'{H2}</h2><div class="dslot" data-t="dslot"></div><p class="cpara" data-t="cp">{N(C_PARA)}</p></section>')


SEC = {"a": lambda: nw(sec_a()), "b": lambda: nw(sec_b()), "c": lambda: nw(sec_c())}


def nw(h: str) -> str:
    """Keep "read-only" on one line in the HTML copy."""
    return h.replace("read-only", '<span class="nw">read-only</span>')


# ---------------------------------------------------------------- layout
def layout(v: str, m: dict, ph: bool) -> dict:
    t = m["t"]
    Y: dict = {}
    ah, ch = (44, 40) if ph else (64, 58)
    if v == "a":
        fe, be = t["fe"], t["be"]
        Y["fe"] = fe[1] + 4
        Y["CS"] = be[1] - (40 if ph else 60)
        Y["api"] = be[1] + 4
        Y["cli"] = Y["api"] + (92 if ph else 132)
        Y["CG"] = max(be[3] + (50 if ph else 70), Y["cli"] + ch + (74 if ph else 96))
    elif v == "b":
        i0, i1, i2 = t["i0"], t["i1"], t["i2"]
        Y["fe"] = i0[1] + 2
        Y["CS"] = i1[1] - (40 if ph else 56)
        Y["api"] = i1[1] + 2
        Y["cli"] = Y["api"] + ah + (30 if ph else 44)
        Y["CG"] = i2[1] - (18 if ph else 22)
    else:
        top = t["dslot"][1]
        Y["fe"] = top + (26 if ph else 30)
        Y["CS"] = Y["fe"] + (52 if ph else 86) + (46 if ph else 60)
        Y["api"] = Y["CS"] + (40 if ph else 56)
        Y["cli"] = Y["api"] + ah + (34 if ph else 48)
        Y["CG"] = Y["cli"] + ch + (74 if ph else 96)
    Y["dtop"] = Y["CG"] - (26 if ph else 40)
    Y["dbot"] = Y["CG"] + (34 if ph else 52)
    Y["need"] = Y["dbot"] + (60 if ph else 90)
    Y["Hd"] = m["G"]
    return Y


def flow(Y: dict, ph: bool, v: str) -> tuple[str, str]:
    """gen.flow's drawing, with each variation's labels."""
    o: list[str] = []
    if not ph:
        cx = 860 if v != "c" else 250
        bw, bh, aw, ah, cw, ch, rx, ry = 132, 86, 120, 64, 96, 58, 68, 13
    else:
        cx = 56
        bw, bh, aw, ah, cw, ch, rx, ry = 78, 52, 72, 44, 64, 40, 36, 8
    yb, ya, yc, dt, db = Y["fe"], Y["api"], Y["cli"], Y["dtop"], Y["dbot"]
    o.append(cab(f"M{cx} {f(yb + bh)} V{f(ya)}"))
    o.append(cab(f"M{cx} {f(ya + ah)} V{f(yc)}"))
    o.append(cab(f"M{cx} {f(yc + ch)} V{f(dt - ry)}"))
    sx = 190 if cx > 500 else 0
    if not ph:
        sides = (-1, 1) if sx else ()
        if v == "c":
            sx, sides = 150, (-1, 1)
        for side in sides:
            o.append(f'<path d="M{f(cx + side * rx * .8)} {f(dt + 6)} L{f(cx + side * sx)} {f(Y["CG"] - 44)} '
                     f'M{f(cx + side * rx * .8)} {f(db - 4)} L{f(cx + side * sx)} {f(Y["CG"] + 38)}" stroke="{INK}" '
                     f'stroke-width=".9" opacity=".6"></path>')
            o.append(g.slab(cx + side * sx, Y["CG"] - 56, T_SILVER))
            o.append(g.slab(cx + side * sx, Y["CG"] + 34, T_GOLD))
    r = 4 if ph else 5
    parts = [g.g_browser(cx - bw / 2, yb, bw, bh), g.g_api(cx - aw / 2, ya, aw, ah),
             g.g_client(cx - cw / 2, yc, cw, ch), g.g_drum(cx, dt, db, rx, ry),
             terminal(cx, yb + bh, T_TOP, r), terminal(cx, ya, T_SILVER, r), terminal(cx, ya + ah, T_SILVER, r),
             terminal(cx, yc, T_SILVER, r), terminal(cx, yc + ch, T_SILVER, r)]
    cy = mg.wave_y(Y["CS"], 5 if ph else 8, 2.1, cx, PW if ph else W)
    parts.append(hp.sc(frame.sleeve(cx, cy, T_SILVER), cx, cy, .6) if ph else frame.sleeve(cx, cy, T_SILVER))
    lab: list[str] = []
    if v == "c":
        L = C_LABELS_PH if ph else C_LABELS
        lx = cx + (48 if ph else 92)
        halo = ["ht", "hs", "hs", "hg"]
        ys = [yb + bh / 2, ya + ah / 2, yc + ch / 2, Y["CG"] + (18 if ph else 39)]
        if not ph:
            lx_d = cx + sx + 44
            lab += [f'<text x="{lx}" y="{f(y + 5)}" class="{h}">{N(s) if "tspan" not in s else s}</text>'
                    for s, y, h in zip(L[:3], ys[:3], halo[:3])]
            lab.append(f'<text x="{lx_d}" y="{f(ys[3] + 5)}" class="hg">{N(L[3])}</text>')
            lab += [f'<text x="{cx - sx}" y="{f(Y["CG"] - 66)}" text-anchor="middle">silver</text>',
                    f'<text x="{cx + sx}" y="{f(Y["CG"] + 74)}" text-anchor="middle">gold</text>']
        else:
            lab += [f'<text x="{lx}" y="{f(y + 5)}" class="{h}">{N(s) if "tspan" not in s else s}</text>'
                    for s, y, h in zip(L, ys, halo)]
        NEW.setdefault(CUR, []).append(L[2].replace('<tspan class="m">', "").replace("</tspan>", ""))
    elif not ph:
        lx = cx + 92
        lab += [f'<text x="{lx}" y="{f(yb + bh / 2 + 5)}">browser (React)</text>',
                f'<text x="{lx}" y="{f(ya + ah / 2 + 5)}">FastAPI</text>',
                f'<text x="{lx}" y="{f(yc + ch / 2 + 5)}" class="m">GridflowClient</text>',
                f'<text x="{cx}" y="{f(db + ry + 26)}" text-anchor="middle">DuckDB over silver and gold</text>',
                f'<text x="{cx - sx}" y="{f(Y["CG"] - 66)}" text-anchor="middle">silver</text>',
                f'<text x="{cx + sx}" y="{f(Y["CG"] + 74)}" text-anchor="middle">gold</text>']
    else:
        lab += [f'<text x="{cx}" y="{f(yb - 8)}" text-anchor="middle" class="ht">browser</text>',
                f'<text x="{cx}" y="{f(ya - 9)}" text-anchor="middle" class="hs">FastAPI</text>',
                f'<text x="{cx}" y="{f(yc - 9)}" text-anchor="middle" class="m hs">GridflowClient</text>',
                f'<text x="{cx}" y="{f(db + ry + 18)}" text-anchor="middle">DuckDB</text>']
    return "".join(o + parts), "".join(lab)


def ground(Y: dict, ph: bool) -> str:
    """Topsoil from the top of the board, silver and gold from their contacts."""
    w = PW if ph else W
    Hd = Y["Hd"]
    tail = f" L{w + 40} {f(Hd + 10)} L-40 {f(Hd + 10)} Z"
    o = [f'<rect x="0" y="0" width="{w}" height="{f(Hd)}" fill="{T_TOP}"></rect>',
         f'<rect x="0" y="0" width="{w}" height="{f(Hd)}" fill="url(#p-soil)" opacity=".5"></rect>']
    lines = []
    amp = (5, 5) if ph else (8, 7)
    for y0, a, seed, fill, pid, op in ((Y["CS"], amp[0], 2.1, T_SILVER, "p-diag", ".22"),
                                       (Y["CG"], amp[1], 4.0, T_GOLD, "p-stip", ".26")):
        d = mg.wave_d(y0, a, seed, w)
        o.append(f'<path d="{d}{tail}" fill="{fill}"></path><path d="{d}{tail}" fill="url(#{pid})" opacity="{op}">'
                 f'</path>')
        lines.append(d)
    o.append(f'<path d="{" ".join(lines)}" stroke="{INK}" stroke-width="1.5" fill="none"></path>')
    return "".join(o)


def body(v: str, m: dict | None, ph: bool) -> str:
    global CUR
    CUR = v + ("-390" if ph else "")
    NEW[CUR] = []
    sec = SEC[v]()
    bg = ""
    if m is not None:
        Y = layout(v, m, ph)
        w = PW if ph else W
        if "bspace" in m["t"]:
            bs = m["t"]["bspace"]
            base = bs[1]
            spacer = max(0, round(Y["need"] - base))
            sec = sec.replace('<div class="bspace" data-t="bspace"></div>',
                              f'<div class="bspace" data-t="bspace" style="height: {spacer}px"></div>')
        fl, lab = flow(Y, ph, v)
        bg = (f'<svg class="gnd" width="{w}" height="{f(Y["Hd"])}" viewBox="0 0 {w} {f(Y["Hd"])}" aria-hidden="true">'
              f'<defs>{hp.PATTERNS}</defs>{ground(Y, ph)}</svg>'
              f'<svg class="flow" width="{w}" height="{f(Y["Hd"])}" viewBox="0 0 {w} {f(Y["Hd"])}" role="img" '
              f'aria-label="{g.flow_aria()}">{fl}<g class="lab">{lab}</g></svg>')
        if v == "c":
            sec = sec.replace('<div class="dslot" data-t="dslot"></div>',
                              f'<div class="dslot" data-t="dslot" style="height: {round(Y["need"] - m["t"]["dslot"][1])}px">'
                              f'</div>')
    return f'<div class="ground" data-t="ground">{bg}<div class="gin">{sec}</div></div>'


CSS = """.gin{padding:70px 80px 96px}
.nw{white-space:nowrap}
.root .built{margin-top:0}
.built h2{margin:0 0 30px}
.flow .lab text.hg{paint-order:stroke;stroke:#E9DDAF;stroke-width:5px;stroke-linejoin:round}
.flow .lab tspan.m{font-family:"Red Hat Mono",monospace;font-style:normal;font-size:13px}
.va .bcol{width:520px}
.va .fe p,.va .be p{font-size:17.5px;line-height:1.55;color:#3F4A3B;max-width:40ch}
.va .be{margin-top:170px}
.does{list-style:none;margin:0;padding:0;width:560px}
.does li{margin:0}
.does li+li{margin-top:150px}
.does li:nth-child(3){margin-top:230px}
.does p{margin:0;font-size:19px;line-height:1.45;color:#1C2B22;max-width:38ch}
.does .tech{color:#3F4A3B}
.vc .dslot{height:0}
.vc h2{margin-bottom:0}
.cpara{margin:0;font-size:17.5px;line-height:1.6;color:#3F4A3B;max-width:58ch}
"""

PH_CSS = """.ph .gin{padding:44px 16px 64px}
.ph .va .bcol{width:auto;padding-left:116px}
.ph .va .fe p,.ph .va .be p{font-size:15.5px}
.ph .va .be{margin-top:96px}
.ph .does{width:auto;padding-left:116px}
.ph .does p{font-size:16px}
.ph .does li+li{margin-top:96px}
.ph .does li:nth-child(3){margin-top:140px}
.ph .cpara{font-size:15.5px}
.ph .flow .lab tspan.m{font-size:11.5px}
"""


def shell(inner: str, H: int, probe: bool, ph: bool, title: str) -> str:
    s = g.shell(inner, H, probe, ph)
    s = s.replace("<title>Explorer</title>", f"<title>{title}</title>")
    return s.replace("</style>", CSS + (PH_CSS if ph else "") + "</style>", 1)


PROBE_EXTRA = ""


def build(v: str, ph: bool) -> dict:
    w = PW if ph else W
    name = f"2-built-{v}" + ("-390" if ph else "")
    title = {"a": "Built, plain", "b": "Built, what it does", "c": "Built, drawing"}[v]
    m1 = g.measure(shell(body(v, None, ph), 20000, True, ph, title), w)
    m2 = g.measure(shell(body(v, m1, ph), 20000, True, ph, title), w)
    m3 = g.measure(shell(body(v, m2, ph), 20000, True, ph, title), w)
    H = m3["H"]
    out = shell(body(v, m2, ph), H, False, ph, title)
    frame.check(out)
    (HERE / f"{name}.dc.html").write_text(out, encoding="utf-8")
    (HERE / "static").mkdir(exist_ok=True)
    (HERE / "static" / f"{name}.html").write_text(frame.static(out), encoding="utf-8")
    print(name, "H", H, "G", m2["G"], m3["G"], "over", m3["over"], "outside", m3["outside"], "hit", m3["hit"])
    return {"H": H}


def main() -> None:
    which = sys.argv[1:] or ["a", "b", "c"]
    res = {}
    for v in which:
        for ph in (False, True):
            res[f"{v}{'-390' if ph else ''}"] = build(v, ph)
    (HERE / "built-measure.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    (HERE / "built-copy.json").write_text(json.dumps(NEW, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
