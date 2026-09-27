"""Phase 24 round 1, designer D: "Notebook first".

One template, four specimens. Emits D-<slug>.dc.html and static/D-<slug>.html beside this file.

Run with the gridflow_models venv (pandas 3.0.2): every DataFrame and text output in the notebook is
formatted by pandas itself from the fact pack's rows, so what the page prints is what the cell prints.
Every chart cell was executed on synthetic frames of the same dtypes to confirm what it draws (legend
texts and order, labels, the NaN gap); the drawings below follow that structure in the site's style.
"""
from __future__ import annotations

import html
import json
import math
import re
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
PACK = json.loads((HERE.parent / "pack" / "specimens.json").read_text(encoding="utf-8"))
SPEC = {s["id"]: s for s in PACK["specimens"]}
HEIGHTS = json.loads((HERE / "heights.json").read_text()) if (HERE / "heights.json").exists() else {}

PETROL, HORIZON, CHART, OLIVE = "#155A6E", "#3E8C97", "#AFC64E", "#66793B"
INK, DAY, CLAY, KHAKI, MUTED, RULE = "#1C2B22", "#F6F4EC", "#C77E3C", "#A39A6A", "#5d6a55", "#DFDACA"
BRONZE, INK2 = "#A5713C", "#3F4A3B"
W = 1440
HERO_H = 424          # hero band, ground line near 404


def f(v: float) -> str:
    return f"{v:.1f}".rstrip("0").rstrip(".") if abs(v - round(v)) > 1e-9 else str(int(round(v)))


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def smooth(pts: list[tuple[float, float]]) -> str:
    """Catmull-Rom through pts, as cubic Beziers (from the homepage generator)."""
    d = f"M{f(pts[0][0])} {f(pts[0][1])}"
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i > 0 else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else pts[i + 1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}"
    return d


# ================================================================ hero strip (pieces from gen_a.py)
def g(x: float) -> float:
    """The ground surface of the compact hero."""
    return 404 + 3 * math.sin(x / 190 + .6) - 2 * math.sin(x / 83 + 1.3)


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


def frange(a: float, b: float, step: float) -> list[float]:
    out, v = [], a
    while v <= b + 1e-6:
        out.append(v)
        v += step
    return out


def sc(svg: str, x: float, base: float, s: float) -> str:
    return f'<g transform="translate({f(x)} {f(base)}) scale({s}) translate({f(-x)} {f(-base)})">{svg}</g>'


def ccgt(x: float, base: float) -> str:
    def r(rx: float, ry: float, w: float, h: float, fill: str) -> str:
        return (f'<rect x="{f(x + rx)}" y="{f(base - ry)}" width="{f(w)}" height="{f(h)}" fill="{fill}" '
                f'stroke="{INK}" stroke-width=".9"></rect>')
    return "".join([
        r(66, 104, 7, 60, DAY), r(86, 112, 7, 68, DAY),
        f'<path d="M{f(x + 66)} {f(base - 98)} h7 M{f(x + 86)} {f(base - 106)} h7" stroke="{CLAY}" stroke-width="3"></path>',
        r(62, 46, 15, 46, CLAY), r(82, 46, 15, 46, CLAY), r(0, 32, 62, 32, CLAY), r(-24, 16, 24, 16, DAY),
        f'<path d="M{f(x + 4)} {f(base - 22)} H{f(x + 58)} M{f(x + 4)} {f(base - 12)} H{f(x + 58)}" stroke="{DAY}" '
        f'stroke-width=".8" stroke-dasharray="3 3" opacity=".8"></path>',
        f'<path d="M{f(x)} {f(base - 32)} L{f(x + 31)} {f(base - 38)} L{f(x + 62)} {f(base - 32)}" fill="{CLAY}" '
        f'stroke="{INK}" stroke-width=".9" stroke-linejoin="round"></path>',
    ])


def substation(x: float, base: float) -> tuple[str, list[tuple[float, float]]]:
    gg = []
    for gx in (x, x + 48):
        gg.append(f"M{f(gx)} {f(base)} V{f(base - 50)} M{f(gx + 36)} {f(base)} V{f(base - 50)} "
                  f"M{f(gx - 3)} {f(base - 50)} H{f(gx + 39)} M{f(gx)} {f(base - 50)} L{f(gx + 36)} {f(base - 24)} "
                  f"M{f(gx + 36)} {f(base - 50)} L{f(gx)} {f(base - 24)} M{f(gx)} {f(base - 24)} H{f(gx + 36)}")
    ins = " ".join(f"M{f(xi)} {f(base - 50)} v6" for xi in (x + 8, x + 18, x + 28, x + 56, x + 66, x + 76))
    out = [f'<path d="{" ".join(gg)} {ins} M{f(x + 8)} {f(base - 44)} H{f(x + 76)}" stroke="{INK}" '
           f'stroke-width="1.2" fill="none"></path>']
    for tx in (x + 6, x + 56):
        out.append(f'<rect x="{f(tx)}" y="{f(base - 17)}" width="22" height="17" fill="{KHAKI}" stroke="{INK}" '
                   f'stroke-width=".9"></rect>')
        out.append(f'<path d="{" ".join(f"M{f(tx + 3 + 3 * k)} {f(base - 14)} V{f(base - 3)}" for k in range(6))} '
                   f'M{f(tx + 5)} {f(base - 17)} v-6 M{f(tx + 11)} {f(base - 17)} v-7 M{f(tx + 17)} {f(base - 17)} v-6" '
                   f'stroke="{INK}" stroke-width=".7"></path>')
    posts = " ".join(f"M{f(xp)} {f(base)} v-12" for xp in frange(x - 10, x + 96, 12))
    out.append(f'<path d="{posts} M{f(x - 10)} {f(base - 11)} H{f(x + 96)}" stroke="{INK}" stroke-width=".6" '
               f'opacity=".65"></path>')
    return "".join(out), [(x - 3, base - 50), (x + 8, base - 44), (x + 18, base - 44)]


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


def gasterminal(x: float, base: float) -> str:
    def tank(tx: float, w: float, h: float) -> str:
        return (f'<path d="M{f(tx)} {f(base)} V{f(base - h)} Q{f(tx + w / 2)} {f(base - h - w * .2)} {f(tx + w)} '
                f'{f(base - h)} V{f(base)} Z" fill="{CLAY}" stroke="{INK}" stroke-width="1"></path>'
                f'<path d="M{f(tx + 4)} {f(base)} L{f(tx + w * .45)} {f(base - h + 1)} M{f(tx)} {f(base - h + 6)} '
                f'H{f(tx + w)}" stroke="{INK}" stroke-width=".7" opacity=".6" fill="none"></path>')
    rack = (f'<path d="M{f(x + 100)} {f(base - 10)} H{f(x + 126)} M{f(x + 100)} {f(base - 14)} H{f(x + 126)} '
            f'M{f(x + 104)} {f(base)} V{f(base - 16)} M{f(x + 124)} {f(base)} V{f(base - 16)}" stroke="{INK}" '
            f'stroke-width="1.1" fill="none"></path>')
    return tank(x, 52, 34) + tank(x + 60, 40, 27) + rack


def battery(x: float, base: float) -> str:
    out = []
    for dy, h, off in [(19, 9, 5), (10, 10, 0)]:
        for k in range(4):
            cx = x + off + k * 23
            out.append(f'<rect x="{f(cx)}" y="{f(base - dy)}" width="20" height="{h}" fill="{KHAKI}" stroke="{INK}" '
                       f'stroke-width=".8"></rect>')
    posts = " ".join(f"M{f(xp)} {f(base)} v-13" for xp in frange(x - 8, x + 104, 12))
    out.append(f'<path d="{posts} M{f(x - 8)} {f(base - 12)} H{f(x + 104)}" stroke="{INK}" stroke-width=".6" '
               f'opacity=".65"></path>')
    return "".join(out)


def strip() -> str:
    """The petrol sky's ground: a low version of the homepage landscape, the same pieces and palette."""
    p: list[str] = []
    far = [(560, 420), (660, 352), (790, 322), (930, 334), (1080, 300), (1230, 316), (1380, 302), (1470, 308)]
    p.append(f'<path d="{smooth(far)} L1470 430 L560 430 Z" fill="{HORIZON}" opacity=".5"></path>')
    near = [(680, 420), (780, 372), (890, 356), (1005, 366), (1125, 346), (1245, 360), (1360, 350), (1470, 356)]
    p.append(f'<path d="{smooth(near)} L1470 430 L680 430 Z" fill="{HORIZON}"></path>')
    for i, (tx, ty, h) in enumerate([(890, 356, 58), (1005, 366, 52), (1125, 346, 64), (1245, 360, 56), (1360, 350, 60)]):
        p.append(turbine(tx, ty + 3, h, h * .5, ["sp2", "sp1", "sp3"][i % 3], 40 * i + 10))
    field = [(-20, 374), (240, 368), (520, 377), (820, 384), (1120, 390), (1470, 386)]
    bottom = " ".join(f"L{f(x)} {f(g(x))}" for x in range(1470, -21, -20))
    p.append(f'<path d="{smooth(field)} {bottom} Z" fill="{CHART}"></path>')
    p.append(f'<path d="{smooth([(-20, 388), (400, 385), (820, 394), (1200, 399), (1470, 397)])}" stroke="{OLIVE}" '
             f'stroke-width="1" fill="none" opacity=".45"></path>')
    p.append(sc(ccgt(150, g(180)), 150, g(180), .74))
    p1, p2, p3 = (330, g(330), .46), (500, g(500), .5), (670, g(670), .54)
    sub_x = 760
    sub_svg, sub_ends = substation(sub_x, g(sub_x + 40))
    wires = [spans(tips(*p1, 1), tips(*p2, -1), 9), spans(tips(*p2, 1), tips(*p3, -1), 10),
             spans(tips(*p3, 1), sub_ends, 8)]
    p.append(f'<g stroke="{INK}" fill="none" stroke-linecap="round" stroke-width="1.3">'
             f'{pylon(*p1)}{pylon(*p2)}{pylon(*p3)}</g>')
    p.append(f'<path d="{" ".join(wires)}" stroke="{INK}" stroke-width=".8" fill="none" opacity=".85"></path>')
    p.append(sub_svg)
    p.append(battery(930, g(980)))
    p.append(sc(converter(1060, g(1110)), 1060, g(1110), 1.0))
    p.append(sc(gasterminal(1236, g(1300)), 1236, g(1300), 1.1))
    surf = "M" + " L".join(f"{f(x)} {f(g(x))}" for x in range(-20, 1461, 20))
    root = surf + " " + " ".join(f"L{f(x)} {f(g(x) + 9)}" for x in range(1460, -21, -20)) + " Z"
    p.append(f'<path d="{surf} L1460 {HERO_H + 2} L-20 {HERO_H + 2} Z" fill="{DAY}"></path>')
    p.append(f'<path d="{root}" fill="{OLIVE}"></path>')
    p.append(f'<path d="{surf}" stroke="{INK}" stroke-width="1.5" fill="none"></path>')
    return (f'<svg class="strip" width="{W}" height="{HERO_H}" viewBox="0 0 {W} {HERO_H}" aria-hidden="true">'
            + "".join(p) + "</svg>")


# ================================================================ notebook pieces
KW = r"\b(from|import|def|if|return|for|in|else)\b"


def hl(code: str) -> str:
    """Escape and tint a block of Python: string literals clay-deep, keywords petrol, comments muted."""
    out, pos = [], 0
    for m in re.finditer(r'(f?"[^"\n]*")|(#[^\n]*)|' + KW, code):
        out.append(esc(code[pos:m.start()]))
        if m.group(1):
            out.append(f'<span class="s">{esc(m.group(1))}</span>')
        elif m.group(2):
            out.append(f'<span class="c">{esc(m.group(2))}</span>')
        else:
            out.append(f'<span class="k">{m.group(0)}</span>')
        pos = m.end()
    out.append(esc(code[pos:]))
    return "".join(out)


SETUP = "from gridflow_models import setup_notebook\ndata, models, common = setup_notebook()\n"


def df_html(frame: pd.DataFrame) -> str:
    """pandas' own HTML for the frame, restyled only by class (index rows, rowspans and cell text untouched)."""
    s = frame.to_html()
    s = s.replace('<table border="1" class="dataframe">', '<table class="df">')
    s = s.replace('<tr style="text-align: right;">', "<tr>")
    s = s.replace(' valign="top"', "")
    return re.sub(r">\s+<", "><", s).strip()


def cell_in(n: str, code: str) -> str:
    return f'<div class="cell"><span class="pr">[{n}]:</span><pre class="in">{hl(code)}</pre></div>'


def cell_out(n: str, body: str) -> str:
    return f'<div class="cell out"><span class="pr">{f"[{n}]:" if n else ""}</span>{body}</div>'


def txt(s: str) -> str:
    return f'<pre class="txt">{esc(s)}</pre>'


# ================================================================ plots (matplotlib-style, drawn in site style)
FONT = 'font-family="Hanken Grotesk" fill="#1C2B22"'


def nice_ticks(lo: float, hi: float, target: int = 6) -> list[float]:
    span = hi - lo
    raw = span / target
    mag = 10 ** math.floor(math.log10(raw))
    step = min((m * mag for m in (1, 2, 2.5, 5, 10) if m * mag >= raw), default=10 * mag)
    first = math.ceil(lo / step) * step
    out, v = [], first
    while v <= hi + 1e-9:
        out.append(round(v, 6))
        v += step
    return out


def fmt_tick(v: float) -> str:
    """matplotlib's ScalarFormatter look: no thousands separator, a real minus sign."""
    s = f"{v:.0f}" if abs(v - round(v)) < 1e-9 else f"{v:g}"
    return s.replace("-", "−")


def frame_svg(ax0: float, ay0: float, aw: float, ah: float, ylo: float, yhi: float, xticks: list[tuple[float, str]],
              xlabel: str, ylabel: str, yticks: list[float] | None = None) -> tuple[list[str], callable]:
    Y = lambda v: ay0 + ah - (v - ylo) / (yhi - ylo) * ah  # noqa: E731
    yt = yticks if yticks is not None else nice_ticks(ylo, yhi)
    yt = [v for v in yt if ylo <= v <= yhi]
    o = [f'<rect x="{f(ax0)}" y="{f(ay0)}" width="{f(aw)}" height="{f(ah)}" fill="none" stroke="{INK}" stroke-width="1"></rect>']
    ticks = " ".join(f"M{f(ax0 - 4)} {f(Y(v))} H{f(ax0)}" for v in yt)
    ticks += " " + " ".join(f"M{f(x)} {f(ay0 + ah)} V{f(ay0 + ah + 4)}" for x, _ in xticks)
    o.append(f'<path d="{ticks}" stroke="{INK}" stroke-width="1"></path>')
    lab = "".join(f'<text x="{f(ax0 - 8)}" y="{f(Y(v) + 4.5)}" text-anchor="end">{fmt_tick(v)}</text>' for v in yt)
    lab += "".join(f'<text x="{f(x)}" y="{f(ay0 + ah + 19)}" text-anchor="middle">{t}</text>' for x, t in xticks)
    lab += (f'<text x="{f(ax0 + aw / 2)}" y="{f(ay0 + ah + 42)}" text-anchor="middle" font-size="13.5">{xlabel}</text>'
            f'<text transform="translate({f(ax0 - 52)} {f(ay0 + ah / 2)}) rotate(-90)" text-anchor="middle" '
            f'font-size="13.5">{ylabel}</text>')
    o.append(f'<g {FONT} font-size="12.5">{lab}</g>')
    return o, Y


def legend_box(x: float, y: float, rows: list[tuple[str, str]], title: str | None = None) -> str:
    """rows: (swatch svg at 0,0 within 24x12, label)."""
    lh = 20
    th = 20 if title else 0
    w = 34 + max(len(t) for _, t in rows) * 6.6 + 14
    if title:
        w = max(w, len(title) * 6.7 + 20)
    h = th + len(rows) * lh + 10
    o = [f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="3" fill="{DAY}" stroke="{INK}" '
         f'stroke-opacity=".3"></rect>']
    if title:
        o.append(f'<text x="{f(x + w / 2)}" y="{f(y + 17)}" text-anchor="middle" {FONT} font-size="12.5">{esc(title)}</text>')
    for i, (sw, t) in enumerate(rows):
        yy = y + th + 8 + i * lh
        o.append(f'<g transform="translate({f(x + 9)} {f(yy)})">{sw}</g>'
                 f'<text x="{f(x + 42)}" y="{f(yy + 10)}" {FONT} font-size="12.5">{esc(t)}</text>')
    return "".join(o)


def plot_svg(w: int, h: int, aria: str, parts: list[str], defs: str = "") -> str:
    return (f'<svg class="plot" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(aria)}">'
            + (f"<defs>{defs}</defs>" if defs else "") + "".join(parts) + "</svg>")


HATCH = (f'<pattern id="h-ps" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
         f'<path d="M0 0 V6" stroke="{INK}" stroke-width="1" opacity=".55"></path></pattern>')


def day_ticks(t0: pd.Timestamp, n: int, step_h: float, days: list[str], x0: float, aw: float) -> list[tuple[float, str]]:
    out = []
    for d in days:
        t = pd.Timestamp(d + " 00:00Z")
        i = (t - t0) / pd.Timedelta(hours=step_h)
        out.append((x0 + i / (n - 1) * aw, t.strftime("%b %d")))
    return out


def plot_fuelhh(sp: dict) -> str:
    ch = sp["chart"]
    per = ch["per_fuel_mw"]
    n = len(ch["hours_utc"])

    def band(code: str) -> str:
        if code.startswith("INT"):
            return "INT* (net)"
        if code in ("CCGT", "OCGT"):
            return "CCGT, OCGT"
        if code in ("OTHER", "NPSHYD", "COAL", "OIL"):
            return "OTHER, NPSHYD, COAL, OIL"
        return code
    order = ["INT* (net)", "PS", "NUCLEAR", "BIOMASS", "OTHER, NPSHYD, COAL, OIL", "CCGT, OCGT", "WIND"]
    fill = {"INT* (net)": OLIVE, "PS": KHAKI, "NUCLEAR": PETROL, "BIOMASS": BRONZE,
            "OTHER, NPSHYD, COAL, OIL": KHAKI, "CCGT, OCGT": CLAY, "WIND": HORIZON}
    mix = {b: [0.0] * n for b in order}
    for code, vals in per.items():
        for i, v in enumerate(vals):
            mix[band(code)][i] += v
    pos = {b: [max(v, 0.0) for v in mix[b]] for b in order}
    neg = {b: [min(v, 0.0) for v in mix[b]] for b in order[:2]}
    top = [sum(pos[b][i] for b in order) for i in range(n)]
    bot = [sum(neg[b][i] for b in order[:2]) for i in range(n)]
    lo, hi = min(bot), max(top)
    pad = (hi - lo) * .05
    ylo, yhi = lo - pad, hi + pad
    PW, PH = 752, 330
    ax0, ay0, aw, ah = 62, 10, 474, 262
    t0 = pd.Timestamp(ch["hours_utc"][0])
    xt = day_ticks(t0, n, 1, [f"2026-09-{d}" for d in range(20, 27)], ax0, aw)
    o, Y = frame_svg(ax0, ay0, aw, ah, ylo, yhi, xt, "timestamp_utc", "MW", nice_ticks(ylo, yhi, 6))
    X = lambda i: ax0 + i / (n - 1) * aw  # noqa: E731
    areas = []
    cum = [0.0] * n
    for b in order:
        up = [cum[i] + pos[b][i] for i in range(n)]
        d = "M" + " L".join(f"{f(X(i))} {f(Y(up[i]))}" for i in range(n))
        d += " L" + " L".join(f"{f(X(i))} {f(Y(cum[i]))}" for i in range(n - 1, -1, -1)) + " Z"
        areas.append(f'<path d="{d}" fill="{fill[b]}"></path>')
        if b == "PS":
            areas.append(f'<path d="{d}" fill="url(#h-ps)"></path>')
        cum = up
    cum = [0.0] * n
    for b in order[:2]:
        dn = [cum[i] + neg[b][i] for i in range(n)]
        d = "M" + " L".join(f"{f(X(i))} {f(Y(dn[i]))}" for i in range(n))
        d += " L" + " L".join(f"{f(X(i))} {f(Y(cum[i]))}" for i in range(n - 1, -1, -1)) + " Z"
        areas.append(f'<path d="{d}" fill="{fill[b]}"></path>')
        if b == "PS":
            areas.append(f'<path d="{d}" fill="url(#h-ps)"></path>')
        cum = dn
    zero = f'<path d="M{f(ax0)} {f(Y(0))} H{f(ax0 + aw)}" stroke="{INK}" stroke-width=".9"></path>'
    note = (f'<text x="{f(ax0 + .99 * aw)}" y="{f(ay0 + ah - .03 * ah)}" text-anchor="end" {FONT} font-size="12.5">'
            f'below zero: INT* net export and PS</text>')

    def sw(b: str) -> str:
        r = f'<rect x="0" y="1" width="24" height="10" fill="{fill[b]}"></rect>'
        return r + (f'<rect x="0" y="1" width="24" height="10" fill="url(#h-ps)"></rect>' if b == "PS" else "")
    leg = legend_box(ax0 + aw + 8, ay0, [(sw(b), b) for b in reversed(order)])
    mx = max(range(n), key=lambda i: mix["WIND"][i])
    aria = (f"Stacked area chart of elexon/fuelhh, MW, hourly means of the half-hour values, {n} hours from 23:00 UTC "
            f"on 19 September to 22:00 UTC on 26 September 2026 (settlement dates 20 to 26 September). Bands from the "
            f"zero line up: INT* net, PS, NUCLEAR, BIOMASS, OTHER with NPSHYD, COAL and OIL, CCGT with OCGT, WIND. "
            f"Below zero, the negative parts of INT* net (down to {f(round(min(mix['INT* (net)'])))} MW) "
            f"and PS. The stack tops out at {f(round(hi))} MW; WIND peaks at {f(round(mix['WIND'][mx]))} MW.")
    return plot_svg(PW, PH, aria, [*areas[:], zero, *o, note, leg], HATCH)


def plot_prices(sp: dict) -> str:
    ch = sp["chart"]
    v = ch["ssp_gbp_per_mwh"]
    n = len(v)
    lo, hi = min(v), max(v)
    pad = (hi - lo) * .05
    ylo, yhi = lo - pad, hi + pad
    PW, PH = 752, 318
    ax0, ay0, aw, ah = 62, 10, 668, 250
    t0 = pd.Timestamp(ch["t_utc"][0])
    xt = day_ticks(t0, n, .5, [f"2026-09-{d}" for d in range(19, 23)], ax0, aw)
    o, Y = frame_svg(ax0, ay0, aw, ah, ylo, yhi, xt, "timestamp_utc", "£/MWh", nice_ticks(ylo, yhi, 7))
    X = lambda i: ax0 + i / (n - 1) * aw  # noqa: E731
    line = "M" + " L".join(f"{f(X(i))} {f(Y(y))}" for i, y in enumerate(v))
    zero = f'<path d="M{f(ax0)} {f(Y(0))} H{f(ax0 + aw)}" stroke="{INK}" stroke-width=".9"></path>'
    body = f'<path d="{line}" fill="none" stroke="{PETROL}" stroke-width="1.5" stroke-linejoin="round"></path>'
    aria = (f"Line chart of the system sell price from elexon/system_prices, £/MWh, {n} half-hourly settlement periods "
            f"from 23:00 UTC on 18 September to 22:30 UTC on 22 September 2026, with a line at zero. "
            f"{ch['negatives']['count']} periods are below zero; the low is −50.00 at 13:30 UTC on 20 September and the "
            f"high 594.00 at 20:00 UTC on 22 September.")
    return plot_svg(PW, PH, aria, [zero, body, *o])


def plot_flows(sp: dict) -> str:
    ch = sp["chart"]
    days = pd.date_range("2026-08-01 04:00Z", "2026-09-21 04:00Z", freq="D")
    n = len(days)
    ser = []
    for s, col in zip(ch["series"], [OLIVE, CLAY]):
        m = {pd.Timestamp(p["timestamp_utc"]): p["flow_gwh_per_day"] for p in s["points"]}
        ser.append(([m.get(d) for d in days], col))
    vals = [y for ys, _ in ser for y in ys if y is not None]
    lo, hi = min(vals), max(vals)
    pad = (hi - lo) * .05
    ylo, yhi = lo - pad, hi + pad
    PW, PH = 752, 318
    ax0, ay0, aw, ah = 62, 10, 668, 250
    xt = [(ax0 + i / (n - 1) * aw, days[i].strftime("%b %d")) for i in (0, 14, 31, 45)]
    o, Y = frame_svg(ax0, ay0, aw, ah, ylo, yhi, xt, "timestamp_utc", "GWh/d", nice_ticks(ylo, yhi, 7))
    X = lambda i: ax0 + i / (n - 1) * aw  # noqa: E731
    body = []
    for ys, col in ser:
        segs, cur = [], []
        for i, y in enumerate(ys):
            if y is None:
                if cur:
                    segs.append(cur)
                cur = []
            else:
                cur.append((X(i), Y(y)))
        if cur:
            segs.append(cur)
        d = " ".join("M" + " L".join(f"{f(x)} {f(y)}" for x, y in sg) for sg in segs)
        body.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.6" stroke-linejoin="round"></path>')
        body.append("".join(f'<circle cx="{f(x)}" cy="{f(y)}" r="3.3" fill="{col}"></circle>' for sg in segs for x, y in sg))

    def sw(col: str) -> str:
        return (f'<path d="M0 6 H24" stroke="{col}" stroke-width="1.6"></path>'
                f'<circle cx="12" cy="6" r="3.3" fill="{col}"></circle>')
    leg = legend_box(ax0 + aw / 2 - 92, ay0 + 8, [(sw(OLIVE), "(Bacton (IUK), exit)"), (sw(CLAY), "(St. Fergus, entry)")],
                     "point_label,direction_key")
    aria = ("Line chart with markers from entsog/physical_flows, GWh/d, one native value per gas day at two National Gas "
            "TSO points, 1 August to 21 September 2026. The lines break between 5 August and 13 September, where "
            "nothing is stored. Bacton (IUK) exit runs 381.9 to 406.9 in early August, is 0.0 from 13 to 20 September "
            "and 175.166 on 21 September. St. Fergus entry runs 350.3 to 594.6.")
    return plot_svg(PW, PH, aria, [*body, *o, leg])


def plot_units(sp: dict) -> str:
    bars = [b for b in sp["chart"]["bars"] if b["fuel_type"] != "(null)"]
    bars.sort(key=lambda b: (b["units"], [-ord(c) for c in b["fuel_type"]]))
    n = len(bars)
    total = sum(b["units"] for b in bars)
    hi = max(b["units"] for b in bars) * 1.05
    PW, PH = 752, 398
    ax0, ay0, aw, ah = 92, 34, 560, 318
    X = lambda v: ax0 + v / hi * aw  # noqa: E731
    step = ah / n
    xt = [(X(v), fmt_tick(v)) for v in (0, 50, 100, 150, 200)]
    o = [f'<rect x="{f(ax0)}" y="{f(ay0)}" width="{f(aw)}" height="{f(ah)}" fill="none" stroke="{INK}" stroke-width="1"></rect>']
    ticks = " ".join(f"M{f(x)} {f(ay0 + ah)} V{f(ay0 + ah + 4)}" for x, _ in xt)
    ticks += " " + " ".join(f"M{f(ax0 - 4)} {f(ay0 + ah - (i + .5) * step)} H{f(ax0)}" for i in range(n))
    o.append(f'<path d="{ticks}" stroke="{INK}" stroke-width="1"></path>')
    rects, labs = [], []
    for i, b in enumerate(bars):
        cy = ay0 + ah - (i + .5) * step
        bh = step * .5
        rects.append(f'<rect x="{f(ax0)}" y="{f(cy - bh / 2)}" width="{f(max(X(b["units"]) - ax0, .6))}" '
                     f'height="{f(bh)}" fill="{PETROL}"></rect>')
        labs.append(f'<text x="{f(ax0 - 8)}" y="{f(cy + 4.2)}" text-anchor="end">{b["fuel_type"]}</text>')
        labs.append(f'<text x="{f(X(b["units"]) + 4)}" y="{f(cy + 4.2)}">{b["units"]}</text>')
    labs += [f'<text x="{f(x)}" y="{f(ay0 + ah + 19)}" text-anchor="middle">{t}</text>' for x, t in xt]
    labs.append(f'<text transform="translate({f(ax0 - 76)} {f(ay0 + ah / 2)}) rotate(-90)" text-anchor="middle" '
                f'font-size="13.5">fuel_type</text>')
    labs.append(f'<text x="{f(ax0 + aw / 2)}" y="{f(ay0 - 12)}" text-anchor="middle" font-size="15">'
                f'fuel_type is set on {total} of 3,014 units</text>')
    aria = (f"Horizontal bar chart from elexon/bmunits_reference, count of BM units per fuel_type in the 26 September "
            f"2026 snapshot, {n} codes, {total} units. The chart title reads: fuel_type is set on {total} of 3,014 units. "
            + ", ".join(f"{b['fuel_type']} {b['units']}" for b in reversed(bars)) + ".")
    return plot_svg(PW, PH, aria, [*rects, *o, f'<g {FONT} font-size="12.5">{"".join(labs)}</g>'])


# ================================================================ the specimens
def rows(sid: str) -> pd.DataFrame:
    return pd.DataFrame(SPEC[sid]["sample_rows"]["rows"])


def nb_fuelhh() -> list[tuple[str, str]]:
    r = rows("elexon/fuelhh")
    r["settlement_date"] = pd.to_datetime(r["settlement_date"]).astype("datetime64[us]")
    r["settlement_period"] = r["settlement_period"].astype("int32")
    codes = ["BIOMASS", "CCGT", "INTFR", "NPSHYD", "NUCLEAR", "OTHER", "PS", "WIND"]
    out2 = r.set_index("fuel_type").loc[codes, ["settlement_date", "settlement_period", "generation_mw"]]
    return [
        (SETUP + 'df = data.elexon.query("fuelhh", "2026-09-20", "2026-09-26")\nlen(df)', txt("6720")),
        ('codes = ["BIOMASS", "CCGT", "INTFR", "NPSHYD", "NUCLEAR", "OTHER", "PS", "WIND"]\n'
         'sp25 = df[df.timestamp_utc == "2026-09-26 11:00Z"].set_index("fuel_type")\n'
         'sp25.loc[codes, ["settlement_date", "settlement_period", "generation_mw"]]', df_html(out2)),
        ('def band(code):\n'
         '    if code.startswith("INT"): return "INT* (net)"\n'
         '    if code in ("CCGT", "OCGT"): return "CCGT, OCGT"\n'
         '    if code in ("OTHER", "NPSHYD", "COAL", "OIL"): return "OTHER, NPSHYD, COAL, OIL"\n'
         '    return code\n\n'
         'colour = {"INT* (net)": "#66793B", "PS": "#A39A6A", "NUCLEAR": "#155A6E",\n'
         '          "BIOMASS": "#A5713C", "OTHER, NPSHYD, COAL, OIL": "#A39A6A",\n'
         '          "CCGT, OCGT": "#C77E3C", "WIND": "#3E8C97"}\n'
         'order = list(colour)\n'
         'hourly = df.pivot_table("generation_mw", "timestamp_utc", "fuel_type")\n'
         'mix = hourly.tz_convert("UTC").resample("1h").mean().T.groupby(band).sum().T[order]', ""),
        ('ax = (common.pd.concat([mix.clip(lower=0), mix[order[:2]].clip(upper=0)], axis=1)\n'
         '        .plot.area(lw=0, color=colour, ylabel="MW", legend=False))\n'
         'for c in ax.collections:\n'
         '    if c.get_label() == "PS": c.set(hatch="////", edgecolor="#1C2B22")\n'
         'ax.axhline(0, color="k", lw=0.8)\n'
         'ax.text(0.99, 0.03, "below zero: INT* net export and PS", ha="right",\n'
         '        transform=ax.transAxes)\n'
         'h, l = ax.get_legend_handles_labels()\n'
         'ax.legend(h[6::-1], l[6::-1], loc="upper left", bbox_to_anchor=(1, 1));', "PLOT"),
    ]


def nb_prices() -> list[tuple[str, str]]:
    r = rows("elexon/system_prices")
    r["settlement_period"] = r["settlement_period"].astype("int32")
    r["price_derivation_code"] = r["price_derivation_code"].astype("str")
    cols = ["system_sell_price", "system_buy_price", "net_imbalance_volume", "price_derivation_code"]
    out2 = r.set_index("settlement_period").sort_index().loc[22:29, cols]
    return [
        (SETUP + 'df = data.elexon.query("system_prices", "2026-09-19", "2026-09-22")\nlen(df)', txt("192")),
        ('day = df[df.settlement_date == "2026-09-20"]\n'
         'day = day.set_index("settlement_period").sort_index()\n'
         'cols = ["system_sell_price", "system_buy_price", "net_imbalance_volume",\n'
         '        "price_derivation_code"]\n'
         'day.loc[22:29, cols]', df_html(out2)),
        ('ssp = df.set_index("timestamp_utc").tz_convert("UTC")["system_sell_price"]\n'
         'ax = ssp.plot(color="#155A6E", ylabel="£/MWh")\n'
         'ax.axhline(0, color="k", lw=0.8);', "PLOT"),
    ]


def nb_flows() -> list[tuple[str, str]]:
    r = rows("entsog/physical_flows")
    r["flow_gwh_per_day"] = r["flow_gwh_per_day"].astype("float64")
    keys = [("ITP-00005", "UK-TSO-0001", "exit"), ("ITP-00005", "UK-TSO-0003", "entry"),
            ("ITP-00061", "UK-TSO-0003", "exit"), ("ITP-00207", "UK-TSO-0001", "exit"),
            ("ITP-00207", "UK-TSO-0004", "entry"), ("ITP-00022", "UK-TSO-0001", "entry"),
            ("LNG-00007", "UK-TSO-0001", "entry"), ("LNG-00053", "UK-TSO-0001", "entry")]
    cols = ["point_label", "operator_label", "flow_gwh_per_day"]
    out2 = r.set_index(["point_key", "operator_key", "direction_key"]).loc[keys, cols]
    uniq = repr(pd.Series(["GWh/d"] * 3, dtype="str").unique())
    kl = ",\n        ".join(", ".join(f'("{a}", "{b}", "{c}")' for a, b, c in keys[i:i + 2]) for i in range(0, 8, 2))
    return [
        (SETUP + 'df = data.entsog.query("physical_flows", "2026-09-13", "2026-09-21")\ndf.unit.unique()', txt(uniq)),
        (f"keys = [{kl}]\n"
         'cols = ["point_label", "operator_label", "flow_gwh_per_day"]\n'
         'day = df[df.timestamp_utc == "2026-09-21 04:00Z"]\n'
         'day.set_index(["point_key", "operator_key", "direction_key"]).loc[keys, cols]', df_html(out2)),
        ('flows = data.entsog.query("physical_flows", "2026-08-01", "2026-09-21")\n'
         'nts = flows[flows.operator_key.eq("UK-TSO-0001")\n'
         '            & flows.point_key.isin(["ITP-00005", "ITP-00022"])]\n'
         'daily = nts.pivot_table("flow_gwh_per_day", "timestamp_utc",\n'
         '                        ["point_label", "direction_key"]).tz_convert("UTC")\n'
         'pair = daily[[("Bacton (IUK)", "exit"), ("St. Fergus", "entry")]]\n'
         'pair.asfreq("D").plot(marker="o", color=["#66793B", "#C77E3C"], ylabel="GWh/d");', "PLOT"),
    ]


def nb_units() -> list[tuple[str, str]]:
    r = rows("elexon/bmunits_reference")
    r["fuel_type"] = r["fuel_type"].astype("str")
    ids = ["E_ABERDARE", "T_ABRBO-1", "T_DRAXX-1", "T_HEYM27", "T_PEHE-1", "I_IEG-FRAN1", "2__AANGE001", "V__AENEL001"]
    cols = ["bm_unit_name", "fuel_type", "registered_capacity_mw", "company_name"]
    out2 = r.set_index("bm_unit_id").loc[ids, cols]
    vc = repr(pd.Series([None] * 2515 + ["WIND"] * 499, dtype="str", name="fuel_type").isna().value_counts())
    return [
        (SETUP + 'df = data.elexon.tail("bmunits_reference", n=3014)\ndf.fuel_type.isna().value_counts()', txt(vc)),
        ('ids = ["E_ABERDARE", "T_ABRBO-1", "T_DRAXX-1", "T_HEYM27", "T_PEHE-1",\n'
         '       "I_IEG-FRAN1", "2__AANGE001", "V__AENEL001"]\n'
         'cols = ["bm_unit_name", "fuel_type", "registered_capacity_mw", "company_name"]\n'
         'df.set_index("bm_unit_id").loc[ids, cols]', df_html(out2)),
        ('counts = df.fuel_type.value_counts(ascending=True)\n'
         'title = f"fuel_type is set on {counts.sum()} of {len(df):,} units"\n'
         'ax = counts.plot.barh(color="#155A6E", title=title)\n'
         'ax.bar_label(ax.containers[0]);', "PLOT"),
    ]


def code(s: str) -> str:
    return f"<code>{s}</code>"


PAGES = {
    "fuelhh": dict(
        sid="elexon/fuelhh", nb=nb_fuelhh, plot=plot_fuelhh, file="fuelhh.ipynb",
        vendor="Elexon BMRS",
        h1="Generation by fuel type",
        ident=f"Dataset {code('FUELHH')}, read in gridflow as {code('elexon/fuelhh')}.",
        one="Half-hourly GB generation outturn in MW: one value per settlement period for each Elexon fuel-type code.",
        notes=[
            ("What it is", "<p>Elexon’s outturn by fuel type: each half-hour settlement period has one row per "
             "fuel-type code, in MW. The codes mix plant types (CCGT, NUCLEAR, WIND) with pumped storage (PS) and ten "
             "interconnectors (INT*). The week queried here is 336 half-hours of 20 codes: 6,720 rows.</p>"),
            ("Facts", [("Grain", "One row per settlement date, period and fuel code"),
                       ("Cadence", "Every 30 minutes: 48 periods a day, 46 or 50 on clock-change days"),
                       ("Stored", "1 Sep 2021 to 26 Sep 2026; 7 to 9 Sep 2026 missing"),
                       ("Published", "At the end of the half-hour on 99.82% of rows; longest wait 271 minutes"),
                       ("Units", "MW; the INT* codes and PS are signed")]),
            ("From codes to bands", "<p>The chart sums the codes into seven bands, each named by the codes it holds. "
             "INT* is the net of the ten interconnectors, positive when GB imports. OTHER, NPSHYD, COAL and OIL share "
             "khaki; COAL peaks at 133 MW this week. PS keeps its own hatched khaki band: it is signed, and what its "
             "sign means is not documented.</p>"),
            ("One week of the mix", "<p class=\"cap\">Hourly mean of each code’s two half-hours, summed into bands, for "
             "settlement dates 20 to 26 September 2026, on a UTC axis. Source: elexon/fuelhh silver, MW. Positive parts "
             "stack above zero; the negative parts of INT* and PS stack below it.</p>",
             [("No solar.", "FUELHH has no solar code, so solar outturn has to come from another dataset."),
              ("Signed codes.", "INT* codes are positive when GB imports; PS is signed with no documented meaning. "
               "Negatives are routine: INTIRL is below zero in 70.3% of half-hours, PS in 54.7%."),
              ("The code set changes.", "INTELEC starts on 14 Sep 2021, INTVKL on 12 Jul 2023 and INTGRNL on 19 Mar "
               "2024, so a half-hour holds 17 to 20 rows.")]),
        ],
        uses=[("Price-model features", "Wind, gas and net imports each half-hour, as inputs to residual-demand and "
               "merit-order models."),
              ("Interconnector flows", "Net import or export on each of the ten links, from the signed INT* codes."),
              ("Mix history", "Five years of half-hourly outturn for backtests, with its gaps and code changes to "
               "handle.")],
        table=("silver_elexon_fuelhh", "ElexonFuelHH",
               "<p>Typed by the Pydantic contract " + code("ElexonFuelHH") + " at parse time; dataset version 2.0.0. "
               "1,682,517 rows, with no duplicate keys.</p>",
               [("settlement_date", "Date", "GB settlement date, taken from the vendor start time"),
                ("settlement_period", "Int32", "Half-hour index, 1 to 50"),
                ("timestamp_utc", "Datetime(us, UTC)", "Start of the half-hour"),
                ("fuel_type", "String", "Elexon fuel-type code, as sent"),
                ("generation_mw", "Float64", "MW for the period; INT* and PS are signed"),
                ("published_at", "Datetime(us, UTC)", "Vendor publish time"),
                ("data_provider", "String", "Always “elexon”"),
                ("ingested_at", "Datetime(us, UTC)", "When the silver transform ran"),
                ("event_time, available_at, source_run_id, dataset_version", "lineage",
                 "Added by the pipeline; query() leaves them out")]),
        other=("<p>The workbench name " + code('"fuel_generation"') + " reads the same table.</p>",
               [("From Elexon", "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELHH\n"
                 "    ?publishDateTimeFrom=<UTC Z>&publishDateTimeTo=<UTC Z>&page=<n>"),
                ("With the gridflow CLI", "gridflow ingest elexon fuelhh --start 2026-09-20 --end 2026-09-26    # bronze only\n"
                 "gridflow pipeline elexon fuelhh --start 2026-09-20 --end 2026-09-26  # bronze to silver")]),
        related=[("elexon/fuelinst", "The same connector’s instantaneous outturn by fuel type."),
                 ("elexon/bmunits_reference", "Uses the same fuel-type codes, unit by unit."),
                 ("elexon/indo", "Demand, used to check the interconnector sign."),
                 ("neso_data_portal/historic_generation_mix", "Where solar outturn lives.")],
    ),
    "system-prices": dict(
        sid="elexon/system_prices", nb=nb_prices, plot=plot_prices, file="system_prices.ipynb",
        vendor="Elexon BMRS", h1="System sell and buy prices",
        ident=f"Dataset {code('DISEBSP')}, read in gridflow as {code('elexon/system_prices')}.",
        one=("GB imbalance (cash-out) prices for each half-hour settlement period, in £/MWh, published with the net "
             "imbalance volume."),
        notes=[
            ("What it is", "<p>The price at which imbalances are cashed out, per half-hour settlement period: a "
             "system sell price (SSP) and a system buy price (SBP), equal on every row since September 2021, with the "
             "net imbalance volume (NIV) in MWh. Four days come back as 192 rows, one per period.</p>"),
            ("Facts", [("Grain", "One row per settlement period per publication; silver keeps every vintage"),
                       ("Cadence", "Every 30 minutes"),
                       ("Stored", "1 Sep 2021 to 22 Sep 2026, with no missing dates"),
                       ("Published", "Median 52 minutes after the period starts in 2021 to 2023, about 24.7 hours in "
                        "2024 to 2026; the cause is not established"),
                       ("Units", "£/MWh for prices, MWh for NIV")]),
            ("Four days of prices", "<p class=\"cap\">System sell price for each half-hour, latest publication per "
             "period, settlement dates 19 to 22 September 2026, on a UTC axis. Source: elexon/system_prices silver, "
             "£/MWh, no aggregation.</p>",
             [("Append-only silver.", "96,793 rows cover 88,694 periods. Read the latest-publication view, as the "
               "workbench does, or dedupe on available_at before plotting."),
              ("One price.", "SSP equals SBP on every row, so one series carries both."),
              ("Negative prices are routine.", "4,052 periods since September 2021 went below zero, and 34 of the 192 "
               "here; the low is −50.00 at 13:30 UTC on 20 September.")]),
        ],
        uses=[("Imbalance-price forecasting", "The half-hourly target series for models of cash-out prices."),
              ("Imbalance exposure", "Pricing what a short or long position costs in each settlement period."),
              ("Negative-price studies", "When and how often cash-out went below zero, period by period.")],
        table=("silver_elexon_system_prices", "ElexonSystemPrice",
               "<p>Typed by " + code("ElexonSystemPrice") + "; dataset version 2.0.0, append-only. The workbench "
               "reads " + code("silver_elexon_system_prices_latest") + ", one row per period.</p>",
               [("settlement_date", "Date", "GB settlement date"),
                ("settlement_period", "Int32", "Half-hour index, 1 to 50"),
                ("timestamp_utc", "Datetime(us, UTC)", "Period start"),
                ("system_sell_price", "Float64", "SSP, £/MWh"),
                ("system_buy_price", "Float64", "SBP, £/MWh; equal to SSP"),
                ("net_imbalance_volume", "Float64", "NIV, MWh; the sign convention is not documented"),
                ("run_type", "String", "Null on every row: this endpoint has no such field"),
                ("price_derivation_code", "String", "N, P or K; K is undocumented"),
                ("published_at", "Datetime(us, UTC)", "Vendor createdDateTime"),
                ("data_provider, ingested_at", "String, Datetime", "“elexon”; when the silver transform ran"),
                ("event_time, available_at, source_run_id, dataset_version, vintage_policy", "lineage",
                 "Added by the pipeline; query() leaves them out")]),
        other=("<p>" + code("data.imbalance_context(start, end)") + " returns these prices joined to NESO carbon "
               "intensity.</p>",
               [("From Elexon", "GET https://data.elexon.co.uk/bmrs/api/v1/balancing/settlement/system-prices/{YYYY-MM-DD}\n"
                 "    ?page=<n>"),
                ("With the gridflow CLI", "gridflow ingest elexon system_prices --start 2026-09-19 --end 2026-09-22\n"
                 "gridflow pipeline elexon system_prices --start 2026-09-19 --end 2026-09-22")]),
        related=[("neso/carbon_intensity", "Joined to these prices in the imbalance-context view."),
                 ("elexon/mid", "The day-ahead benchmark the workbench compares against."),
                 ("system_marginal_price", "A gold view built on this table.")],
    ),
    "physical-flows": dict(
        sid="entsog/physical_flows", nb=nb_flows, plot=plot_flows, file="physical_flows.ipynb",
        vendor="ENTSO-G", h1="Physical gas flows",
        ident=(f"ENTSOG {code('operationalData')}, indicator Physical Flow, read in gridflow as "
               f"{code('entsog/physical_flows')}."),
        one="Daily physical gas flow at each European transmission point, by reporting operator and direction, in GWh/d.",
        notes=[
            ("What it is", "<p>Each row is one gas day’s flow at one point, as reported by one operator and marked "
             "entry or exit. The direction reads as relative to that operator’s system (inferred from paired values, "
             "not documented). gridflow normalises every value to GWh/d. A gas day holds about 983 rows across 620 "
             "points and 48 operators.</p>"),
            ("Facts", [("Grain", "One row per gas day, point, operator and direction"),
                       ("Cadence", "Daily; the timestamp is each operator’s gas-day start, mostly 04:00 UTC for GB"),
                       ("Stored", "14 gas days: 1 to 5 Aug and 13 to 21 Sep 2026"),
                       ("Published", "Not established; available_at is the ingest time"),
                       ("Units", "GWh/d; a flow can be null")]),
            ("Two GB points", "<p class=\"cap\">Daily flow at two National Gas TSO points, native values with no "
             "averaging, gas days 1 August to 21 September 2026, on a UTC axis. Source: entsog/physical_flows silver, "
             "GWh/d. Nothing is stored from 6 August to 12 September, so the lines break there. The zeros at Bacton "
             "(IUK) are as reported.</p>",
             [("Two blocks of history.", "Local silver holds 14 gas days: 1 to 5 August and 13 to 21 September "
               "2026."),
              ("Both sides report.", "At Bacton (IUK) on 21 September, National Gas TSO exit and Interconnector entry "
               "are both 175.165952 GWh/d, so summing every row double counts."),
              ("Nulls are real.", "2,499 rows have no flow, including every day for 176 series such as Avonmouth LNG. "
               "Do not zero-fill.")]),
        ],
        uses=[("GB supply picture", "Daily entry at terminals and LNG points and exit at interconnectors, as inputs to "
               "a gas balance."),
              ("Cross-border flows", "Which way gas moved at each interconnection point, and how much."),
              ("Point-level features", "Flow series for gas price and spread models, keyed by point and operator.")],
        table=("silver_entsog_physical_flows", "EntsogPhysicalFlow",
               "<p>Typed by " + code("EntsogPhysicalFlow") + "; dataset version 1.0.0. 13,764 rows, with no duplicate "
               "keys.</p>",
               [("timestamp_utc", "Datetime(us, UTC)", "Gas-day start, from the vendor periodFrom"),
                ("point_key, point_label", "String", "ENTSOG point id and name"),
                ("operator_key, operator_label", "String", "Reporting operator id and name"),
                ("direction_key", "String", "“entry” or “exit”"),
                ("flow_gwh_per_day", "Float64", "Flow in GWh/d; nullable"),
                ("unit", "String", "Always “GWh/d”"),
                ("data_provider", "String", "Always “entsog”"),
                ("ingested_at", "Datetime(us, UTC)", "When the silver transform ran; not declared in the class"),
                ("event_time, available_at, source_run_id, dataset_version", "lineage",
                 "Added by the pipeline; available_at is the ingest time")]),
        other=("<p>A range’s first day misses operators whose gas day starts the evening before (21:00 to 23:00 "
               "UTC).</p>",
               [("From ENTSOG", "GET https://transparency.entsog.eu/api/v1/operationalData\n"
                 "    ?limit=-1&timeZone=UCT&from=YYYY-MM-DD&to=YYYY-MM-DD\n"
                 "    &indicator=Physical%20Flow&periodType=day"),
                ("With the gridflow CLI", "gridflow ingest entsog physical_flows --start 2026-09-13 --end 2026-09-21\n"
                 "gridflow pipeline entsog physical_flows --start 2026-09-13 --end 2026-09-21")]),
        related=[("entsog/aggregated_physical_flows", "The same indicator at zone level."),
                 ("entsog/nominations", "The same endpoint, Nomination indicator."),
                 ("entsog/allocations", "The same endpoint, Allocation indicator.")],
    ),
    "bmunits-reference": dict(
        sid="elexon/bmunits_reference", nb=nb_units, plot=plot_units, file="bmunits_reference.ipynb",
        vendor="Elexon BMRS", h1="BM unit reference",
        ident=f"Endpoint {code('/reference/bmunits/all')}, read in gridflow as {code('elexon/bmunits_reference')}.",
        one=("The register of Balancing Mechanism units (id, name, fuel type, capacity, lead party, GSP group), held as "
             "one snapshot."),
        notes=[
            ("What it is", "<p>Elexon’s list of registered Balancing Mechanism units, one row per unit id. gridflow "
             "keeps one snapshot, overwritten on each weekly run; this one was ingested on 26 September 2026. Read it "
             "with " + code("tail()") + " or " + code("data.sql()") + ": " + code("query()") + " filters this table "
             "on ingest time, so an ordinary date range returns no rows.</p>"),
            ("Facts", [("Grain", "One row per bm_unit_id"),
                       ("Cadence", "A weekly snapshot, overwritten on each run"),
                       ("Stored", "The 26 Sep 2026 snapshot only; no history is kept"),
                       ("Published", "Not established"),
                       ("Units", "MW for registered_capacity_mw, per registration")]),
            ("Units by fuel type", "<p class=\"cap\">Count of BM units per fuel_type in the 26 September 2026 "
             "snapshot, 19 codes. The 2,515 units with no fuel type are counted in [1] and left out of the bars, and "
             "the title says so. Source: elexon/bmunits_reference silver. There is no time axis, so there is no "
             "line.</p>",
             [("Mostly untyped.", "83% of units (2,515 of 3,014) have no fuel type, so a fuel breakdown covers 499."),
              ("Capacity is not additive.", "registered_capacity_mw is per registration: the untyped rows alone sum to "
               "727,551 MW, and 1,315 ids start I_ (described as per-party interconnector registrations)."),
              ("Counts drift.", "Each run overwrites the file and drops keyless vendor rows: 2,969 units on 9 September "
               "2026, 3,014 on 26 September.")]),
        ],
        uses=[("Joining unit-level data", "Attach fuel type, lead party and capacity to BOAL or PN rows through "
               "bm_unit_id."),
              ("Fleet views", "Count or filter units by fuel type, lead party or GSP group."),
              ("Unit lookups", "Resolve an id such as T_DRAXX-1 to its name and lead party.")],
        table=("silver_elexon_bmunits_reference", "ElexonBMUnit",
               "<p>Typed by " + code("ElexonBMUnit") + "; dataset version 1.1.0. 3,014 rows in one file, with no "
               "duplicate ids.</p>",
               [("bm_unit_id", "String", "Elexon BM unit id; the entity key"),
                ("bm_unit_name", "String", "Vendor name; often repeats the id"),
                ("fuel_type", "String", "Vendor fuel type; null on 2,515 rows"),
                ("registered_capacity_mw", "Float64", "MW per registration; not additive"),
                ("company_name", "String", "Lead party"),
                ("gsp_group_id", "String", "GSP group, such as _A; null on 1,822 rows"),
                ("national_grid_bm_unit", "String", "National Grid unit name, such as ABERU-1; not an ENTSO-E EIC"),
                ("data_provider, ingested_at", "String, Datetime", "“elexon”; when the silver transform ran"),
                ("event_time, available_at, source_run_id, dataset_version", "lineage",
                 "Added by the pipeline; tail() leaves them out")]),
        other=("<p>" + code('data.sql("SELECT * FROM silver_elexon_bmunits_reference")') + " reads the same rows.</p>",
               [("From Elexon", "GET https://data.elexon.co.uk/bmrs/api/v1/reference/bmunits/all"),
                ("With the gridflow CLI", "gridflow pipeline elexon bmunits_reference   # dates are ignored")]),
        related=[("elexon/boal", "Per-unit bid-offer acceptances, joined on bm_unit_id."),
                 ("elexon/pn", "Per-unit physical notifications, joined on bm_unit_id."),
                 ("elexon/uou2t14d", "Per-unit availability."),
                 ("elexon/fuelhh", "The same fuel-type codes; interconnector flow lives there.")],
    ),
}


# ================================================================ page
def notebook(p: dict) -> str:
    sp = SPEC[p["sid"]]
    cells = p["nb"]()
    notes = p["notes"]
    items: list[str] = []
    n_rows = len(cells) + 1
    items.append(f'<div class="nb-frame" style="grid-row: 1 / span {n_rows}" aria-hidden="true"></div>')
    items.append(f'<div class="nb-bar" style="grid-row: 1"><span class="nb-tab">{p["file"]}</span>'
                 f'<span class="nb-kern">gridflow_models</span></div>')
    # which note sits beside which cell group
    note_for = {0: 0, 1: 1, len(cells) - 1: len(notes) - 1}
    if len(cells) == 4:
        note_for[2] = 2
    for k, (src, out) in enumerate(cells):
        n = str(k + 1)
        body = cell_in(n, src)
        if out == "PLOT":
            body += cell_out("", f'<div class="fig">{p["plot"](sp)}</div>')
        elif out:
            body += cell_out(n, out)
        last = " last" if k == len(cells) - 1 else ""
        items.append(f'<div class="cg{last}" style="grid-row: {k + 2}">{body}</div>')
        if k in note_for:
            items.append(note_block(notes[note_for[k]], k + 2, k == 0))
    return (f'<section class="nbk" aria-label="Working with {esc(p["h1"].lower())} in a notebook">'
            + "".join(items) + "</section>")


def note_block(note: tuple, row: int, first: bool) -> str:
    head = note[0]
    hid = re.sub(r"[^a-z]+", "-", head.lower()).strip("-")
    span = f"grid-row: {row - 1} / span 2" if first else f"grid-row: {row}"
    cls = "note first" if first else "note"
    if isinstance(note[1], list):
        dl = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in note[1])
        inner = f'<dl class="facts">{dl}</dl>'
    else:
        inner = note[1]
    if len(note) > 2:
        cav = "".join(f"<p><strong>{a}</strong> {b}</p>" for a, b in note[2])
        inner += f'<h3>Caveats</h3><div class="cav">{cav}</div>'
    return (f'<section class="{cls}" style="{span}" aria-labelledby="{hid}">'
            f'<h2 id="{hid}">{head}</h2>{inner}</section>')


def lower(p: dict) -> str:
    uses = "".join(f"<li><h3>{a}</h3><p>{b}</p></li>" for a, b in p["uses"])
    rel, cls, txt_, cols = p["table"]
    dl = "".join(f'<div><dt>{a}</dt><dd class="ty">{b}</dd><dd>{c}</dd></div>' for a, b, c in cols)
    card = (f'<div class="card sch"><p class="card-h">{rel}</p><dl>{dl}</dl></div>')
    lead, wells = p["other"]
    wl = "".join(f'<div class="way"><p class="lbl">{a}</p><pre class="in">{hl(b)}</pre></div>' for a, b in wells)
    related = "".join(f'<li><a href="#"><code>{a}</code></a><p>{b}</p></li>' for a, b in p["related"])
    return ('<div class="low">'
            f'<section class="lrow" aria-labelledby="use-h"><div class="lh"><h2 id="use-h">How it’s used</h2></div>'
            f'<ul class="uses">{uses}</ul></section>'
            f'<section class="lrow" aria-labelledby="tab-h"><div class="lh"><h2 id="tab-h">The silver table</h2>{txt_}</div>'
            f'{card}</section>'
            f'<section class="lrow" aria-labelledby="way-h"><div class="lh"><h2 id="way-h">Other ways to get it</h2>{lead}</div>'
            f'<div class="ways">{wl}</div></section>'
            f'<section class="lrow" aria-labelledby="rel-h"><div class="lh"><h2 id="rel-h">Related datasets</h2></div>'
            f'<ul class="rel">{related}</ul></section>'
            '</div>')


FOOT_H = 212


def footer(H: int) -> str:
    edge = [(x, 26 + 9 * math.sin(x / 140 + 1) + 6 * math.sin(x / 53 + 2) + 4 * math.sin(x / 19))
            for x in range(-40, W + 41, 20)]
    d = smooth(edge) + f" L{W + 40} {FOOT_H + 4} L-40 {FOOT_H + 4} Z"
    gran = (f'<pattern id="p-granite" width="46" height="40" patternUnits="userSpaceOnUse"><path d="M8 8 h8 M12 4 v8 '
            f'M30 26 h8 M34 22 v8 M20 34 h6 M23 31 v6 M40 6 h5 M42.5 3.5 v5" stroke="{HORIZON}" stroke-width="1.1">'
            f'</path></pattern>')
    svg = (f'<svg class="edge" width="{W}" height="{FOOT_H}" viewBox="0 0 {W} {FOOT_H}" aria-hidden="true">'
           f'<defs>{gran}</defs><rect x="0" y="0" width="{W}" height="{FOOT_H}" fill="{DAY}"></rect>'
           f'<path d="{d}" fill="{PETROL}"></path><path d="{d}" fill="url(#p-granite)" opacity=".5"></path>'
           f'<path d="{smooth(edge)}" stroke="{INK}" stroke-width="2" fill="none" stroke-linejoin="round"></path></svg>')
    return (f'<footer class="deep">{svg}<div class="deep-in">'
            f'<div><p class="who">Elliot Bentham</p><p class="role">Quantitative Developer, London, UK</p></div>'
            f'<div class="links"><a class="primary" href="#">GitHub</a><a href="#">LinkedIn</a><a href="#">CV (PDF)</a>'
            f'<a href="#">Email</a></div></div></footer>')


CSS = """body{margin:0}
.root{background:#F6F4EC;color:#1C2B22;font:400 16px/1.6 "Hanken Grotesk",sans-serif;font-variant-numeric:tabular-nums;-webkit-font-smoothing:antialiased}
.root a{color:inherit;text-decoration-thickness:1.5px;text-underline-offset:4px}
.root a:focus-visible{outline:2px solid #AFC64E;outline-offset:3px;border-radius:2px}
.root h1,.root h2,.root h3{font-family:"Bricolage Grotesque",sans-serif;margin:0;font-optical-sizing:auto}
.root code{font-family:"Red Hat Mono",monospace;font-size:.9em}
.mast{position:absolute;top:26px;left:80px;right:80px;z-index:2;display:flex;justify-content:space-between;align-items:baseline;color:#F6F4EC}
.brand{font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:24px;letter-spacing:-.01em;text-decoration:none}
.mast ul{display:flex;gap:30px;list-style:none;margin:0;padding:0;font-size:15px}
.mast ul a{text-decoration:none;color:#CFE0DC}
.mast ul a:hover{color:#F6F4EC}
.mast ul a[aria-current="page"]{color:#F6F4EC;box-shadow:inset 0 -2px 0 #AFC64E}
.hero{position:relative;height:424px;background:#155A6E;color:#F6F4EC}
.strip{position:absolute;left:0;top:0;display:block}
.hero-in{position:relative;padding:104px 80px 0;width:760px}
.crumb ol{display:flex;list-style:none;margin:0;padding:0;font-size:15px;color:#CFE0DC}
.crumb li+li::before{content:"/";margin:0 10px;color:#B4D0CD}
.crumb a{text-decoration-color:rgba(207,224,220,.45)}
.crumb a:hover{text-decoration-color:#AFC64E}
.hero h1{margin:16px 0 0;font-size:52px;font-weight:740;font-stretch:84%;line-height:1;letter-spacing:-.02em;color:#F6F4EC}
.ident{margin:16px 0 0;font-size:16px;line-height:1.5;color:#CFE0DC}
.ident code{color:#F6F4EC;font-size:.92em}
.one{margin:8px 0 0;font-size:21px;line-height:1.45;color:#F6F4EC;max-width:31em}
.body{padding:60px 80px 104px}
.nbk{display:grid;grid-template-columns:356px 868px;column-gap:56px;align-items:start}
.nb-frame{grid-column:2;align-self:stretch;background:#F6F4EC;border:1.5px solid #1C2B22;border-radius:4px}
.nb-bar{grid-column:2;position:relative;display:flex;justify-content:space-between;align-items:flex-end;height:40px;margin:1.5px 1.5px 0;background:#1C2B22;border-radius:2.5px 2.5px 0 0;padding:0 18px 0 12px;font:500 13.5px/1 "Red Hat Mono",monospace}
.nb-tab{background:#F6F4EC;color:#1C2B22;padding:11px 18px 12px;border-radius:3px 3px 0 0}
.nb-kern{color:#CFE0DC;align-self:center}
.cg{grid-column:2;position:relative;padding:14px 20px 6px 9px}
.cg.last{padding-bottom:26px}
.cell{display:grid;grid-template-columns:52px minmax(0,1fr);column-gap:10px;margin:0 0 9px;position:relative}
.cell.out{margin:-2px 0 14px}
.pr{font:400 13px/1 "Red Hat Mono",monospace;color:#5d6a55;text-align:right;padding-top:11px}
.in{margin:0;background:#ECE8DA;border:1px solid rgba(28,43,34,.18);border-radius:3px;padding:7px 12px;font:400 14px/1.6 "Red Hat Mono",monospace;color:#1C2B22;white-space:pre;overflow:hidden}
.in .k{color:#155A6E;font-weight:500}
.in .s{color:#7C5530}
.in .c{color:#5d6a55}
.txt{margin:0;padding-top:9px;font:400 14px/1.6 "Red Hat Mono",monospace;color:#1C2B22;white-space:pre}
.fig{padding-top:4px}
.fig svg{display:block}
.df{justify-self:start;border-collapse:collapse;margin:4px 0 0;font:400 13.5px/1 "Hanken Grotesk",sans-serif;font-variant-numeric:tabular-nums;color:#1C2B22}
.df th,.df td{padding:6px 11px;text-align:right;white-space:nowrap}
.df thead th{font-weight:600;vertical-align:bottom}
.df thead tr:last-child th{border-bottom:1px solid #1C2B22}
.df tbody th{font-weight:600;vertical-align:top}
.df tbody tr:nth-child(odd){background:#EFEBDF}
.note{grid-column:1;padding-top:14px}
.note.first{padding-top:0}
.note h2,.lh h2{font-size:30px;font-weight:700;font-stretch:90%;line-height:1.1;letter-spacing:-.012em;margin:0 0 12px}
.note p,.lh p{margin:0 0 12px;font-size:16px;line-height:1.62;color:#3F4A3B}
.note p code,.lh p code{font-size:.86em;color:#1C2B22}
.note .cap{font-size:15px;line-height:1.55}
.note h3{font-size:20px;font-weight:700;font-stretch:90%;line-height:1.1;margin:22px 0 10px}
.cav p{font-size:15px;line-height:1.55;margin:0 0 10px}
.cav strong{font-weight:600;color:#1C2B22}
.facts{margin:0;border-bottom:1px solid rgba(28,43,34,.22)}
.facts div{display:grid;grid-template-columns:92px minmax(0,1fr);gap:14px;padding:9px 0 10px;border-top:1px solid rgba(28,43,34,.22)}
.facts dt{font-weight:600;font-size:15px;line-height:1.5;color:#1C2B22}
.facts dd{margin:0;font-size:15px;line-height:1.5;color:#3F4A3B}
.low{margin-top:100px}
.lrow{display:grid;grid-template-columns:356px 868px;column-gap:56px;align-items:start;margin:0 0 76px}
.lrow:last-child{margin-bottom:0}
.uses{list-style:none;margin:6px 0 0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));column-gap:36px}
.uses h3{font-size:23px;font-weight:720;font-stretch:90%;line-height:1.1;letter-spacing:-.01em;margin:0 0 8px}
.uses p{margin:0;font-size:15px;line-height:1.5;color:#3F4A3B}
.card{border:1px solid rgba(28,43,34,.34);border-radius:3px;overflow:hidden;background:#F6F4EC}
.card-h{margin:0;padding:10px 16px;background:#ECE8DA;border-bottom:1px solid rgba(28,43,34,.2);font:500 15px/1.2 "Red Hat Mono",monospace;color:#155A6E}
.card dl{margin:0;padding:8px 8px 8px}
.sch dl div{display:grid;grid-template-columns:236px 150px minmax(0,1fr);gap:16px;padding:5px 10px;border-radius:2px}
.sch dl div:nth-child(odd){background:#EFEBDF}
.sch dt{font:400 13.5px/1.5 "Red Hat Mono",monospace;color:#155A6E}
.sch dd{margin:0;font-size:14.5px;line-height:1.5;color:#1C2B22}
.sch dd.ty{font:400 13px/1.55 "Red Hat Mono",monospace;color:#3F4A3B}
.ways{display:grid;row-gap:22px}
.lbl{margin:0 0 7px;font-weight:600;font-size:15px;color:#1C2B22}
.rel{list-style:none;margin:6px 0 0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:36px;row-gap:20px}
.rel a{font-weight:500;color:#1C2B22;text-decoration-color:#66793B}
.rel code{font-size:15.5px}
.rel p{margin:4px 0 0;font-size:15px;line-height:1.5;color:#3F4A3B}
.deep{position:relative;height:212px;color:#F6F4EC}
.edge{position:absolute;left:0;top:0;display:block}
.deep-in{position:relative;display:flex;justify-content:space-between;align-items:center;padding:84px 80px 0}
.who{margin:0;font-family:"Bricolage Grotesque",sans-serif;font-size:30px;font-weight:720;font-stretch:88%;line-height:1.1;color:#F6F4EC}
.role{margin:6px 0 0;font-size:16px;color:#B4D0CD}
.links{display:flex;flex-wrap:wrap;gap:12px}
.links a{font-weight:600;padding:10px 18px;border-radius:3px;text-decoration:none;border:1.5px solid rgba(207,224,220,.55);color:#F6F4EC}
.links a:hover{border-color:#F6F4EC}
.root .links a.primary{background:#AFC64E;border-color:#AFC64E;color:#1C2B22}
.rot{transform-box:fill-box;transform-origin:center;animation:spin 17s linear infinite}
.sp2{animation-duration:13s}
.sp3{animation-duration:21s}
@keyframes spin{to{transform:rotate(360deg)} }
@media (prefers-reduced-motion: reduce){.rot{animation:none} }
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,200..800'
         '&amp;family=Hanken+Grotesk:ital,wght@0,400..700;1,400..600&amp;family=Red+Hat+Mono:wght@400;500'
         '&amp;display=swap" rel="stylesheet">')


def page(slug: str) -> str:
    p = PAGES[slug]
    H = HEIGHTS.get(slug, 5200)
    nav = ('<header class="mast"><a class="brand" href="#">gridflow</a><nav aria-label="Primary"><ul>'
           '<li><a href="#">Home</a></li><li><a href="#" aria-current="page">Data sources</a></li>'
           '<li><a href="#">Architecture</a></li><li><a href="#">Models</a></li><li><a href="#">About</a></li>'
           '</ul></nav></header>')
    hero = (f'<section class="hero" aria-labelledby="ds-h">{strip()}<div class="hero-in">'
            f'<nav class="crumb" aria-label="Breadcrumb"><ol><li><a href="#">Data sources</a></li>'
            f'<li><a href="#">{p["vendor"]}</a></li></ol></nav>'
            f'<h1 id="ds-h">{p["h1"]}</h1><p class="ident">{p["ident"]}</p><p class="one">{p["one"]}</p></div></section>')
    body = f'<div class="body">{notebook(p)}{lower(p)}</div>'
    title = p["h1"]
    return f"""<!doctype html>
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
{CSS}</style>
</helmet>
<div class="root" style="width: {W}px; height: {H}px; overflow: hidden; position: relative">
{nav}
<main>
{hero}
{body}
</main>
{footer(H)}
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


def static(dc: str) -> str:
    s = dc.replace('<script src="./support.js"></script>', "")
    s = re.sub(r"</?x-dc>", "", s)
    s = re.sub(r"</?helmet>", "", s)
    return re.sub(r"<script type=\"text/x-dc\".*?</script>\n", "", s, flags=re.S)


if __name__ == "__main__":
    (HERE / "static").mkdir(exist_ok=True)
    for slug in PAGES:
        out = page(slug)
        body_only = out.split('<script type="text/x-dc"')[0]
        assert "{{" not in body_only and "}}" not in body_only, f"{slug}: template-hole syntax in markup"
        assert "/>" not in re.sub(r"<(meta|link|br)[^>]*>", "", body_only), f"{slug}: self-closing tag"
        assert "—" not in re.sub(r"<title>.*?</title>", "", body_only), f"{slug}: em dash"
        (HERE / f"D-{slug}.dc.html").write_text(out, encoding="utf-8")
        (HERE / "static" / f"D-{slug}.html").write_text(static(out), encoding="utf-8")
        print(slug, "H =", HEIGHTS.get(slug, 5200), len(out))
    sys.exit(0)
