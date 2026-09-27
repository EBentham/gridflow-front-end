"""Designer B, "The keyed atlas": the shared shell for the four top pages.

Colours, type and every drawing primitive here are copied from the locked homepage generator
(.planning/v4/design-loop/r3-7/gen_a.py); nothing is imported from it (its module level reads a file that
is not beside it). Text is laid out in flow with fixed section heights, so every stratum contact and every
keyed part lands at a y this module can compute; only drawings and strata are absolutely placed SVG.
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

HERE = Path(__file__).parent
PACK = json.loads((HERE.parent / "pack" / "toppages.json").read_text(encoding="utf-8"))

PETROL, HORIZON, CHART, OLIVE = "#155A6E", "#3E8C97", "#AFC64E", "#66793B"
INK, DAY, CLAY, KHAKI, MUTED, RULE = "#1C2B22", "#F6F4EC", "#C77E3C", "#A39A6A", "#5d6a55", "#DFDACA"
BRONZE, SILVER, GOLD = "#A5713C", "#9FADAB", "#C2A14A"
T_GOLD, T_SILVER, T_BRONZE, T_TOP = "#E9DDAF", "#DCE2DF", "#E2CDB3", "#ECE8DA"
GOLD_DEEP, CLAY_DEEP, SILVER_DEEP = "#8A6F1E", "#7C5530", "#5E6E6B"
INK2 = "#3F4A3B"
ONP, ONP2, ONP3 = "#F6F4EC", "#CFE0DC", "#B4D0CD"
LAB_P = "#E4EFEC"   # drawing labels on petrol (the homepage's land-label colour)

W = 1440
MX = 80                 # side margin
DW, GAP, IW = 888, 56, 336
IX = MX + DW + GAP      # index column left, 1024; it ends at 1360


def f(v: float) -> str:
    return f"{v:.1f}".rstrip("0").rstrip(".") if abs(v - round(v)) > 1e-9 else str(int(round(v)))


def smooth(pts: list[tuple[float, float]]) -> str:
    """Catmull-Rom through pts, as cubic Beziers."""
    d = f"M{f(pts[0][0])} {f(pts[0][1])}"
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i > 0 else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else pts[i + 1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}"
    return d


def frange(a: float, b: float, step: float) -> list[float]:
    out, v = [], a
    while v <= b + 1e-6:
        out.append(v)
        v += step
    return out


def wave(y0: float, amp: float, seed: float, step: int = 120) -> list[tuple[float, float]]:
    return [(x, y0 + amp * math.sin(x / 210 + seed) + amp * 0.45 * math.sin(x / 73 + seed * 2.3))
            for x in range(-40, W + step + 41, step)]


def surf(S: float):
    """The ground-surface profile for a page whose surface sits at S."""
    return lambda x: S + 4 * math.sin(x / 190 + 0.6) - 2.5 * math.sin(x / 83 + 1.3)


def sc(svg: str, x: float, base: float, s: float) -> str:
    return f'<g transform="translate({f(x)} {f(base)}) scale({s}) translate({f(-x)} {f(-base)})">{svg}</g>'


# ================================================================ drawing primitives (from the homepage)
def turbine(x: float, base: float, h: float, blade: float, spin: str, ang: float, col: str = DAY) -> str:
    s = h / 80
    t0, t1 = 2.3 * s, 1.05 * s
    hy = base - h
    tower = (f'<path d="M{f(x - t0)} {f(base)} L{f(x - t1)} {f(hy)} L{f(x + t1)} {f(hy)} L{f(x + t0)} {f(base)} Z" '
             f'fill="{col}"></path>')
    nac = (f'<rect x="{f(x - 1.6 * s)}" y="{f(hy - 2 * s)}" width="{f(7.4 * s)}" height="{f(3.8 * s)}" '
           f'rx="{f(1.5 * s)}" fill="{col}"></rect>')
    bw = max(blade * 0.075, 1.1)
    L = blade
    bd = (f"M{f(-bw * .55)} 0 C{f(-bw * 1.15)} {f(-L * .3)} {f(-bw * .45)} {f(-L * .76)} 0 {f(-L)} "
          f"C{f(bw * .3)} {f(-L * .72)} {f(bw * 1.25)} {f(-L * .3)} {f(bw * .55)} 0 Z")
    blades = "".join(f'<path d="{bd}" transform="rotate({f(ang + k * 120)})" fill="{col}"></path>' for k in range(3))
    rotor = (f'<g transform="translate({f(x - 1.9 * s)},{f(hy - .1 * s)})"><g class="rot {spin}">'
             f'<circle r="{f(L)}" fill="none"></circle>{blades}<circle r="{f(2.1 * s)}" fill="{col}"></circle></g></g>')
    return tower + nac + rotor


def hub_y(base: float, h: float) -> float:
    return base - h - .1 * h / 80


PYL = ("M-18 0 L-5 -96 M18 0 L5 -96 M-5 -96 L-5 -118 M5 -96 L5 -118 M-5 -118 H5 M-14 -28 H14 M-11 -56 H11 "
       "M-8 -80 H8 M-16 -14 L14 -28 M16 -14 L-14 -28 M-13 -42 L11 -56 M13 -42 L-11 -56 M-10 -68 L8 -80 M10 -68 L-8 -80 "
       "M-30 -66 H30 M-24 -92 H24 M-14 -112 H14 M-30 -66 L-5 -60 M30 -66 L5 -60 M-24 -92 L-5 -86 M24 -92 L5 -86")


def pylon(x: float, base: float, s: float) -> str:
    return (f'<g transform="translate({f(x)},{f(base)}) scale({s})"><path vector-effect="non-scaling-stroke" '
            f'd="{PYL}"></path></g>')


def tips(x: float, base: float, s: float, side: int) -> list[tuple[float, float]]:
    return [(x + side * 30 * s, base - 66 * s), (x + side * 24 * s, base - 92 * s), (x + side * 14 * s, base - 112 * s)]


def spans(a: list[tuple[float, float]], b: list[tuple[float, float]], sag: float) -> str:
    out = []
    for (ax, ay), (bx, by) in zip(a, b):
        mx, my = (ax + bx) / 2, max(ay, by) + sag
        out.append(f"M{f(ax)} {f(ay)} Q{f(mx)} {f(my)} {f(bx)} {f(by)}")
    return " ".join(out)


def ccgt(x: float, base: float, s: float) -> str:
    def r(rx: float, ry: float, w: float, h: float, fill: str) -> str:
        return (f'<rect x="{f(x + rx * s)}" y="{f(base - ry * s)}" width="{f(w * s)}" height="{f(h * s)}" '
                f'fill="{fill}" stroke="{INK}" stroke-width=".9"></rect>')
    return "".join([
        r(66, 104, 7, 60, DAY), r(86, 112, 7, 68, DAY),
        f'<path d="M{f(x + 66 * s)} {f(base - 98 * s)} h{f(7 * s)} M{f(x + 86 * s)} {f(base - 106 * s)} h{f(7 * s)}" '
        f'stroke="{CLAY}" stroke-width="{f(3 * s)}"></path>',
        r(62, 46, 15, 46, CLAY), r(82, 46, 15, 46, CLAY),
        r(0, 32, 62, 32, CLAY),
        r(-24, 16, 24, 16, DAY),
        f'<path d="M{f(x + 4 * s)} {f(base - 22 * s)} H{f(x + 58 * s)} M{f(x + 4 * s)} {f(base - 12 * s)} H{f(x + 58 * s)}" '
        f'stroke="{DAY}" stroke-width=".8" stroke-dasharray="3 3" opacity=".8"></path>',
        f'<path d="M{f(x)} {f(base - 32 * s)} L{f(x + 31 * s)} {f(base - 38 * s)} L{f(x + 62 * s)} {f(base - 32 * s)}" '
        f'fill="{CLAY}" stroke="{INK}" stroke-width=".9" stroke-linejoin="round"></path>',
    ])


def substation(x: float, base: float) -> str:
    g = []
    for gx in (x, x + 48):
        g.append(f"M{f(gx)} {f(base)} V{f(base - 50)} M{f(gx + 36)} {f(base)} V{f(base - 50)} "
                 f"M{f(gx - 3)} {f(base - 50)} H{f(gx + 39)} M{f(gx)} {f(base - 50)} L{f(gx + 36)} {f(base - 24)} "
                 f"M{f(gx + 36)} {f(base - 50)} L{f(gx)} {f(base - 24)} M{f(gx)} {f(base - 24)} H{f(gx + 36)}")
    ins = " ".join(f"M{f(xi)} {f(base - 50)} v6" for xi in (x + 8, x + 18, x + 28, x + 56, x + 66, x + 76))
    out = [f'<path d="{" ".join(g)} {ins} M{f(x + 8)} {f(base - 44)} H{f(x + 76)}" stroke="{INK}" stroke-width="1.2" '
           f'fill="none"></path>']
    for tx in (x + 6, x + 56):
        out.append(f'<rect x="{f(tx)}" y="{f(base - 17)}" width="22" height="17" fill="{KHAKI}" stroke="{INK}" '
                   f'stroke-width=".9"></rect>')
        out.append(f'<path d="{" ".join(f"M{f(tx + 3 + 3 * k)} {f(base - 14)} V{f(base - 3)}" for k in range(6))} '
                   f'M{f(tx + 5)} {f(base - 17)} v-6 M{f(tx + 11)} {f(base - 17)} v-7 M{f(tx + 17)} {f(base - 17)} v-6" '
                   f'stroke="{INK}" stroke-width=".7"></path>')
    posts = " ".join(f"M{f(xp)} {f(base)} v-12" for xp in frange(x - 10, x + 96, 12))
    out.append(f'<path d="{posts} M{f(x - 10)} {f(base - 11)} H{f(x + 96)}" stroke="{INK}" stroke-width=".6" '
               f'opacity=".65"></path>')
    return "".join(out)


def metmast(x: float, base: float, h: float, ground=None) -> str:
    g = ground or (lambda _x: base)
    zz = " ".join(f"L{f(x + (2.4 if k % 2 else -2.4) * (1 - k * 9 / h * .6))} {f(base - k * 9)}"
                  for k in range(1, int(h / 9) + 1))
    top = base - h
    booms = []
    for frac in (0.58, 0.8, 1.0):
        by = base - h * frac
        booms.append(f"M{f(x)} {f(by)} H{f(x + 16)} M{f(x)} {f(by)} H{f(x - 12)}")
    cups = "".join(f'<circle cx="{f(x + 16 + dx)}" cy="{f(base - h * fr - 2)}" r="1.5" fill="{INK}"></circle>'
                   for fr in (0.58, 0.8, 1.0) for dx in (-2.2, 2.2))
    guys = (f"M{f(x)} {f(base - h * .62)} L{f(x - 30)} {f(g(x - 30))} M{f(x)} {f(base - h * .62)} L{f(x + 28)} "
            f"{f(g(x + 28))} M{f(x)} {f(base - h * .92)} L{f(x - 44)} {f(g(x - 44))}")
    return "".join([
        f'<path d="{guys}" stroke="{INK}" stroke-width=".6" opacity=".55"></path>',
        f'<path d="M{f(x - 3.6)} {f(base)} L{f(x - 1.2)} {f(top)} M{f(x + 3.6)} {f(base)} L{f(x + 1.2)} {f(top)} '
        f'M{f(x - 3.6)} {f(base)} {zz}" stroke="{INK}" stroke-width=".9" fill="none"></path>',
        f'<path d="{" ".join(booms)} M{f(x)} {f(top)} V{f(top - 10)} M{f(x)} {f(top - 8)} L{f(x - 9)} {f(top - 6)}" '
        f'stroke="{INK}" stroke-width="1.1"></path>',
        cups,
    ])


def converter(x: float, base: float) -> str:
    seams = " ".join(f"M{f(xi)} {f(base - 60)} V{f(base)}" for xi in frange(x + 10, x + 60, 10))
    return "".join([
        f'<rect x="{f(x)}" y="{f(base - 62)}" width="66" height="62" fill="{OLIVE}" stroke="{INK}" stroke-width="1.1"></rect>',
        f'<path d="{seams}" stroke="{DAY}" stroke-width=".7" opacity=".3"></path>',
        f'<rect x="{f(x + 66)}" y="{f(base - 40)}" width="42" height="40" fill="{OLIVE}" stroke="{INK}" stroke-width="1.1"></rect>',
        f'<rect x="{f(x + 66)}" y="{f(base - 40)}" width="42" height="40" fill="{DAY}" opacity=".2"></rect>',
        f'<path d="M{f(x - 1)} {f(base - 62)} H{f(x + 67)}" stroke="{DAY}" stroke-width="1.4" opacity=".7"></path>',
        f'<rect x="{f(x + 76)}" y="{f(base - 16)}" width="10" height="16" fill="{INK}" opacity=".75"></rect>',
    ])


def tank(tx: float, base: float, w: float, h: float) -> str:
    return (f'<path d="M{f(tx)} {f(base)} V{f(base - h)} Q{f(tx + w / 2)} {f(base - h - w * .2)} {f(tx + w)} '
            f'{f(base - h)} V{f(base)} Z" fill="{CLAY}" stroke="{INK}" stroke-width="1"></path>'
            f'<path d="M{f(tx + 4)} {f(base)} L{f(tx + w * .45)} {f(base - h + 1)} M{f(tx)} {f(base - h + 6)} '
            f'H{f(tx + w)}" stroke="{INK}" stroke-width=".7" opacity=".6" fill="none"></path>')


def gasterminal(x: float, base: float) -> str:
    rack = (f'<path d="M{f(x + 100)} {f(base - 10)} H{f(x + 126)} M{f(x + 100)} {f(base - 14)} H{f(x + 126)} '
            f'M{f(x + 104)} {f(base)} V{f(base - 16)} M{f(x + 124)} {f(base)} V{f(base - 16)}" stroke="{INK}" '
            f'stroke-width="1.1" fill="none"></path>')
    return tank(x, base, 52, 34) + tank(x + 60, base, 40, 27) + rack


def solar_rows(x0: float, x1: float, base, rows=((0.6, 30), (0.78, 17), (1.0, 4))) -> str:
    """Tilted panel rows standing on a ground function base(x)."""
    parts = []
    for s, up in rows:
        a, b = x0 + (1 - s) * 18, x1 - (1 - s) * 12
        gy = base((a + b) / 2) - up
        h, lean, fh = 10 * s, 6 * s, 4.2 * s
        yf, yb = gy - fh, gy - fh - h
        legs = " ".join(f"M{f(xl)} {f(gy)} V{f(yf)}" for xl in frange(a + 6, b, 26 * s))
        parts.append(f'<path d="{legs}" stroke="{INK}" stroke-width=".9"></path>')
        parts.append(f'<path d="M{f(a)} {f(yf)} L{f(b)} {f(yf)} L{f(b - lean)} {f(yb)} L{f(a - lean)} {f(yb)} Z" '
                     f'fill="{CHART}" stroke="{INK}" stroke-width=".9" stroke-linejoin="round"></path>')
        cells = " ".join(f"M{f(xc)} {f(yf)} L{f(xc - lean)} {f(yb)}" for xc in frange(a + 9 * s, b - 2, 9 * s))
        parts.append(f'<path d="{cells}" stroke="{INK}" stroke-width=".55" opacity=".4"></path>')
    return "".join(parts)


# ================================================================ strata
PATTERNS = f"""<pattern id="p-stip" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="2" cy="3" r="1" fill="{GOLD_DEEP}"></circle><circle cx="6.5" cy="7.5" r=".8" fill="{GOLD_DEEP}"></circle></pattern>
<pattern id="p-diag" width="8" height="8" patternUnits="userSpaceOnUse"><path d="M0 8 L8 0" stroke="{SILVER_DEEP}" stroke-width=".8"></path></pattern>
<pattern id="p-brick" width="24" height="12" patternUnits="userSpaceOnUse"><path d="M0 11.5 H24 M12 0 V6 M0 6 H24 M0 6 V12" stroke="{CLAY_DEEP}" stroke-width=".8" fill="none"></path></pattern>
<pattern id="p-soil" width="23" height="17" patternUnits="userSpaceOnUse"><circle cx="4" cy="5" r=".9" fill="{KHAKI}"></circle><circle cx="15" cy="12" r="1.1" fill="{KHAKI}"></circle><path d="M17 3 h3" stroke="{KHAKI}" stroke-width=".9"></path></pattern>
<pattern id="p-granite" width="46" height="40" patternUnits="userSpaceOnUse"><path d="M8 8 h8 M12 4 v8 M30 26 h8 M34 22 v8 M20 34 h6 M23 31 v6 M40 6 h5 M42.5 3.5 v5" stroke="{HORIZON}" stroke-width="1.1"></path></pattern>"""

TINT = {"topsoil": (T_TOP, "p-soil", ".5"), "bronze": (T_BRONZE, "p-brick", ".15"),
        "silver": (T_SILVER, "p-diag", ".22"), "gold": (T_GOLD, "p-stip", ".26")}


def strata(H: int, S: float, contacts: list[tuple[float, str]], land: bool = True, names: bool = True) -> str:
    """Petrol sky to the surface S, topsoil below it, then each (y, stratum) in order; 'deep' is the
    unconformity into petrol granite. Returns the inner SVG of a full-page background layer."""
    prof = surf(S)
    pts = [(x, prof(x)) for x in range(-40, W + 41, 20)]
    sd = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts)
    out = [f'<rect x="0" y="0" width="{W}" height="{f(S + 20)}" fill="{PETROL}"></rect>',
           f'<path d="{sd} L{W + 40} {H + 10} L-40 {H + 10} Z" fill="{T_TOP}"></path>',
           f'<path d="{sd} L{W + 40} {H + 10} L-40 {H + 10} Z" fill="url(#p-soil)" opacity=".5"></path>']
    lines, labels = [], []
    for i, (y, kind) in enumerate(contacts):
        if kind == "deep":
            c = [(x, y + 9 * math.sin(x / 140 + 1) + 6 * math.sin(x / 53 + 2) + 4 * math.sin(x / 19))
                 for x in range(-40, W + 41, 20)]
            d = smooth(c)
            out.append(f'<path d="{d} L{W + 40} {H + 10} L-40 {H + 10} Z" fill="{PETROL}"></path>')
            out.append(f'<path d="{d} L{W + 40} {H + 10} L-40 {H + 10} Z" fill="url(#p-granite)" opacity=".5"></path>')
            lines.append(f'<path d="{d}" stroke="{INK}" stroke-width="2" fill="none" stroke-linejoin="round"></path>')
        else:
            fill, pat, op = TINT[kind]
            d = smooth(wave(y, 7, 0.4 + 1.7 * i))
            out.append(f'<path d="{d} L{W + 40} {H + 10} L-40 {H + 10} Z" fill="{fill}"></path>')
            out.append(f'<path d="{d} L{W + 40} {H + 10} L-40 {H + 10} Z" fill="url(#{pat})" opacity="{op}"></path>')
            lines.append(f'<path d="{d}" stroke="{INK}" stroke-width="1.5" fill="none"></path>')
            if names:
                labels.append(f'<text x="1360" y="{f(y + 30)}" text-anchor="end">{kind}</text>')
    if land:
        root = sd + " " + " ".join(f"L{f(x)} {f(y + 9)}" for x, y in reversed(pts)) + " Z"
        out.append(f'<path d="{root}" fill="{OLIVE}"></path>')
    out.append(f'<path d="{sd}" stroke="{INK}" stroke-width="1.5" fill="none"></path>')
    out += lines
    if labels:
        out.append(f'<g font-family="Hanken Grotesk" font-style="italic" font-size="14" fill="{INK}">{"".join(labels)}</g>')
    return "\n".join(out)


def bg_layer(H: int, inner: str) -> str:
    return (f'<svg class="layer" width="{W}" height="{H}" viewBox="0 0 {W} {H}" aria-hidden="true">'
            f'<defs>{PATTERNS}</defs>\n{inner}\n</svg>')


# ================================================================ the keyed index
def mark_svg(body: str, w: int = 30, h: int = 20) -> str:
    return f'<svg class="mk" width="{w}" height="{h}" viewBox="0 0 {w} {h}" aria-hidden="true">{body}</svg>'


MK_MID = 13   # the mark's vertical centre below the entry top (3 px margin + half of 20)


def index_list(entries: list[dict], label: str, top_pad: float = 0, cls: str = "") -> str:
    """entries: dicts with y (the drawing part's y, relative to the list's top edge), mark, name, and
    optional id, d, f, href, sky (on petrol), quiet (not a named thing). Rows are sized from the ys so
    each mark's centre sits level with its part."""
    ys = [e["y"] - MK_MID for e in entries]
    rows = [f"{f(b - a)}px" for a, b in zip(ys, ys[1:])] + ["auto"]
    items = []
    for e in entries:
        c = " ".join(k for k in ("sky" if e.get("sky") else "", "q" if e.get("quiet") else "") if k)
        name = e["name"]
        if e.get("href"):
            name = f'<a href="{e["href"]}">{name}</a>'
        head = f'<h3>{name}</h3>' if not e.get("quiet") else f'<p class="qn">{name}</p>'
        body = head
        if e.get("id"):
            body += f'<p class="id">{e["id"]}</p>'
        if e.get("d"):
            body += f'<p class="d">{e["d"]}</p>'
        if e.get("f"):
            body += f'<p class="fa">{e["f"]}</p>'
        items.append(f'<li data-lv="{f(e["y"])}"{f" class={chr(34)}{c}{chr(34)}" if c else ""}>{e["mark"]}'
                     f'<div>{body}</div></li>')
    return (f'<ol class="ix {cls}" aria-label="{label}" '
            f'style="padding-top: {f(ys[0])}px; grid-template-rows: {" ".join(rows)}">' + "".join(items) + "</ol>")


# ================================================================ page shell
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,200..800'
         '&amp;family=Hanken+Grotesk:ital,wght@0,400..700;1,400..600&amp;family=Red+Hat+Mono:wght@400;500'
         '&amp;display=swap" rel="stylesheet">')

CSS = """body{margin:0}
.root{background:#155A6E;color:#1C2B22;font:400 16px/1.6 "Hanken Grotesk",sans-serif;font-variant-numeric:tabular-nums;-webkit-font-smoothing:antialiased}
.root a{color:inherit;text-decoration-thickness:1.5px;text-underline-offset:4px;text-decoration-color:#66793B}
.root a:focus-visible{outline:2px solid #AFC64E;outline-offset:3px;border-radius:2px}
.root h1,.root h2,.root h3{font-family:"Bricolage Grotesque",sans-serif;margin:0;font-optical-sizing:auto}
.root code{font-family:"Red Hat Mono",monospace;font-size:.9em}
.layer{position:absolute;left:0;top:0}
.flow{position:relative}
.band{position:relative;box-sizing:border-box;padding:0 80px}
.draw{position:absolute;left:0;top:0;display:block}
.mast{box-sizing:border-box;height:100px;padding:26px 80px 0;display:flex;justify-content:space-between;align-items:baseline;color:#F6F4EC}
.brand{font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:24px;letter-spacing:-.01em;text-decoration:none}
.mast ul{display:flex;gap:30px;list-style:none;margin:0;padding:0;font-size:15px}
.mast ul a{text-decoration:none;color:#CFE0DC}
.mast ul a:hover{color:#F6F4EC}
.mast ul a[aria-current="page"]{color:#F6F4EC;box-shadow:inset 0 -2px 0 #AFC64E}
.hero{display:grid;grid-template-columns:860px 374px;column-gap:46px;align-items:start;padding-top:28px}
.hero h1{color:#F6F4EC;font-weight:760;font-stretch:84%;font-size:86px;line-height:.94;letter-spacing:-.022em}
.crumb{margin:0 0 14px;font-size:15px;color:#CFE0DC}
.crumb a{color:#CFE0DC;text-decoration-color:#AFC64E}
.lede{margin-top:14px}
.lede p{margin:0 0 14px;font-size:17.5px;line-height:1.6;color:#CFE0DC}
.lede p:last-child{margin-bottom:0}
.lede code{color:#F6F4EC;font-size:.84em}
.plate-h{font-size:30px;font-weight:700;font-stretch:90%;letter-spacing:-.012em;line-height:1.1}
.sky .plate-h,.plate-h.sky{color:#F6F4EC}
.plate{display:grid;grid-template-columns:888px 336px;column-gap:56px}
.plate > .ix{grid-column:2}
.ix{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:minmax(0,1fr)}
.ix li{display:grid;grid-template-columns:30px minmax(0,1fr);column-gap:14px;align-items:start;align-self:start}
.ix li.spacer{display:block}
.ix .mk{display:block;margin-top:3px}
.ix h3{font-size:23px;font-weight:720;font-stretch:90%;line-height:1.1;letter-spacing:-.01em;color:#1C2B22}
.ix h3 a{text-decoration-color:rgba(102,121,59,0)}
.ix h3 a:hover{text-decoration-color:#66793B}
.ix .qn{margin:0;font-size:17px;line-height:1.35;font-style:italic;font-weight:500;color:#1C2B22}
.ix .id{margin:4px 0 0;font:400 13px/1.45 "Red Hat Mono",monospace;color:#155A6E;overflow-wrap:anywhere}
.ix .d{margin:5px 0 0;font-size:14.5px;line-height:1.5;color:#3F4A3B}
.ix .d code{font-size:13px;color:#1C2B22}
.ix .fa{margin:5px 0 0;font-size:14.5px;line-height:1.45;font-weight:600;color:#1C2B22}
.ix .fa code{font-size:13px;font-weight:500}
.ix li.sky h3{color:#F6F4EC}
.ix li.sky h3 a:hover{text-decoration-color:#AFC64E}
.ix li.sky .id{color:#CFE0DC}
.ix li.sky .d{color:#CFE0DC}
.ix li.sky .d code{color:#F6F4EC}
.ix li.sky .fa{color:#F6F4EC}
.sec h2{font-size:42px;font-weight:720;font-stretch:88%;line-height:1.02;letter-spacing:-.018em;margin:0 0 16px}
.sec p{margin:0 0 14px;font-size:16px;line-height:1.62;color:#3F4A3B;max-width:58ch}
.sec p code{font-size:.86em;color:#1C2B22}
.fig-h{font-size:30px;font-weight:700;font-stretch:90%;letter-spacing:-.012em;line-height:1.1;margin:0 0 8px}
.cap{margin:10px 0 0;font-size:14.5px;line-height:1.55;color:#3F4A3B;max-width:66ch}
.cap code{font-size:13px;color:#1C2B22}
.more{font-weight:600;color:#1C2B22}
.tl{width:100%;border-collapse:collapse;font-size:15px;color:#1C2B22}
.tl th{text-align:left;font-weight:600;font-size:14px;color:#3F4A3B;padding:0 16px 10px 0;border-bottom:1px solid #1C2B22;vertical-align:bottom}
.tl td{height:44px;padding:0 16px 0 0;border-bottom:1px solid rgba(28,43,34,.22);vertical-align:middle}
.tl td.k{font:400 16px "Red Hat Mono",monospace;white-space:nowrap}
.tl td.c{font:400 14px "Red Hat Mono",monospace;color:#155A6E;white-space:nowrap}
.tl td.n{text-align:right;padding-right:0;white-space:nowrap}
.tl th.n{text-align:right;padding-right:0}
.tl td.m{color:#3F4A3B}
.tl .gh td{height:62px;vertical-align:bottom;padding-bottom:9px;border-bottom:1px solid #1C2B22}
.gh-in{display:flex;align-items:center;gap:12px}
.gh-in h3{font-size:23px;font-weight:720;font-stretch:90%;line-height:1.1;letter-spacing:-.01em}
.gh-in span{font-size:14.5px;color:#3F4A3B}
.deep{color:#F6F4EC}
.deep .brand{color:#F6F4EC}
.foot{display:grid;grid-template-columns:minmax(0,1fr) auto;column-gap:64px;align-items:start}
.foot p{margin:10px 0 0;font-size:15px;line-height:1.6;color:#CFE0DC;max-width:62ch}
.foot ul{display:flex;gap:28px;list-style:none;margin:6px 0 0;padding:0;font-size:15px}
.foot ul a{color:#CFE0DC;text-decoration:none}
.foot ul a:hover{color:#F6F4EC}
.rot{transform-box:fill-box;transform-origin:center;animation:spin 17s linear infinite}
.sp2{animation-duration:13s}
.sp3{animation-duration:21s}
@keyframes spin{to{transform:rotate(360deg)} }
@media (prefers-reduced-motion: reduce){.rot{animation:none} }
"""

NAV = [("Home", "#"), ("Data sources", "#"), ("Architecture", "#"), ("Models", "#"), ("About", "#")]


def masthead(current: str) -> str:
    li = "".join(f'<li><a href="{h}"{" aria-current=" + chr(34) + "page" + chr(34) if n == current else ""}>{n}</a></li>'
                 for n, h in NAV)
    return (f'<header class="mast"><a class="brand" href="#">gridflow</a>'
            f'<nav aria-label="Primary"><ul>{li}</ul></nav></header>')


FOOT_LINE = ("Gridflow is a personal research platform for UK and European power markets: a medallion data pipeline, "
             "vendor catalogue and probabilistic modelling stack.")


def footer(h: int, pad_top: int) -> str:
    li = "".join(f'<li><a href="{hh}">{n}</a></li>' for n, hh in NAV)
    return (f'<footer class="band deep" style="height: {h}px; padding-top: {pad_top}px"><div class="foot">'
            f'<div><a class="brand" href="#">gridflow</a><p>{FOOT_LINE}</p></div>'
            f'<nav aria-label="Footer"><ul>{li}</ul></nav></div></footer>')


def page(title: str, H: int, layers: str, flow: str, extra_css: str = "") -> str:
    out = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{FONTS}
<style>
{CSS}{extra_css}</style>
</helmet>
<div class="root" style="width: {W}px; height: {H}px; overflow: hidden; position: relative">
{layers}
<div class="flow">
{flow}
</div>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{W},"height":{H}}}}}'>
class Component extends DCLogic {{
renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
"""
    body_only = out.split('<script type="text/x-dc"')[0]
    assert "{{" not in body_only and "}}" not in body_only, "template-hole syntax in markup"
    stripped = re.sub(r"<(meta|link|br|wbr)[^>]*>", "", body_only)
    assert "/>" not in stripped, "self-closing tag"
    assert "—" not in out, "em dash"
    return out


def static(dc: str) -> str:
    s = dc.replace('<script src="./support.js"></script>', "")
    s = re.sub(r"</?x-dc>", "", s)
    s = re.sub(r"</?helmet>", "", s)
    s = re.sub(r"<script type=\"text/x-dc\".*?</script>\n", "", s, flags=re.S)
    return s


def emit(name: str, dc: str) -> None:
    (HERE / f"{name}.dc.html").write_text(dc, encoding="utf-8")
    (HERE / "static").mkdir(exist_ok=True)
    (HERE / "static" / f"{name}.html").write_text(static(dc), encoding="utf-8")


def wbr(path: str) -> str:
    """Allow a long mono path to break after each slash or underscore run."""
    return path.replace("/", "/<wbr>")
