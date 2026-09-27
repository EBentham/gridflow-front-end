"""Drawings for designer C, "The field guide": the sky's horizon, the vendor marks, one plate per page, the footing edges.

Asset drawings (turbine, substation, met mast, converter, gas terminal) are copied from the locked homepage generator
(.planning/v4/design-loop/r3-7/gen_a.py) so the marks match the reference page's landscape exactly. Every plotted value
comes from ../pack/toppages.json.
"""
from __future__ import annotations

import datetime as dt
import json
import math
from pathlib import Path

HERE = Path(__file__).parent
PACK = json.loads((HERE.parent / "pack" / "toppages.json").read_text(encoding="utf-8"))
SERIES = PACK["series"]

PETROL, HORIZON, CHART, OLIVE = "#155A6E", "#3E8C97", "#AFC64E", "#66793B"
INK, INK2, MUTED, DAY, CLAY, KHAKI, RULE = "#1C2B22", "#3F4A3B", "#5d6a55", "#F6F4EC", "#C77E3C", "#A39A6A", "#DFDACA"
BRONZE, SILVER, GOLD = "#A5713C", "#9FADAB", "#C2A14A"
T_TOP, T_BRONZE, T_SILVER, T_GOLD = "#ECE8DA", "#E2CDB3", "#DCE2DF", "#E9DDAF"
W = 1440
LAB = 'font-style="italic" font-size="14"'
TICK = 'font-size="13"'


def f(v: float) -> str:
    return f"{v:.1f}".rstrip("0").rstrip(".") if abs(v - round(v)) > 1e-9 else str(int(round(v)))


def smooth(pts: list[tuple[float, float]]) -> str:
    """Catmull-Rom through pts, as cubic Beziers (as on the reference page)."""
    d = f"M{f(pts[0][0])} {f(pts[0][1])}"
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i > 0 else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else pts[i + 1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}"
    return d


def wave(y0: float, amp: float, seed: float, step: int = 120) -> list[tuple[float, float]]:
    return [(x, y0 + amp * math.sin(x / 210 + seed) + amp * 0.45 * math.sin(x / 73 + seed * 2.3))
            for x in range(-40, W + step + 41, step)]


def fnum(v: float, dp: int = 0) -> str:
    return f"{v:,.{dp}f}".replace("-", "−")


# ================================================================ patterns (per-svg prefix keeps every svg self-contained)
def patterns(p: str) -> str:
    return (
        f'<pattern id="{p}-brick" width="24" height="12" patternUnits="userSpaceOnUse"><path d="M0 11.5 H24 M12 0 V6 M0 6 H24 M0 6 V12" stroke="#7C5530" stroke-width=".8" fill="none"></path></pattern>'
        f'<pattern id="{p}-diag" width="8" height="8" patternUnits="userSpaceOnUse"><path d="M0 8 L8 0" stroke="#5E6E6B" stroke-width=".8"></path></pattern>'
        f'<pattern id="{p}-stip" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="2" cy="3" r="1" fill="#8A6F1E"></circle><circle cx="6.5" cy="7.5" r=".8" fill="#8A6F1E"></circle></pattern>'
        f'<pattern id="{p}-granite" width="46" height="40" patternUnits="userSpaceOnUse"><path d="M8 8 h8 M12 4 v8 M30 26 h8 M34 22 v8 M20 34 h6 M23 31 v6 M40 6 h5 M42.5 3.5 v5" stroke="{HORIZON}" stroke-width="1.1"></path></pattern>'
    )


# ================================================================ landscape pieces (copied from the reference generator)
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


def _frange(a: float, b: float, step: float) -> list[float]:
    out, v = [], a
    while v <= b + 1e-6:
        out.append(v)
        v += step
    return out


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
    return "".join(out)


def metmast(x: float, base: float, h: float) -> str:
    zz = " ".join(f"L{f(x + (2.4 if k % 2 else -2.4) * (1 - k * 9 / h * .6))} {f(base - k * 9)}" for k in range(1, int(h / 9) + 1))
    top = base - h
    booms = " ".join(f"M{f(x)} {f(base - h * fr)} H{f(x + 16)} M{f(x)} {f(base - h * fr)} H{f(x - 12)}" for fr in (.58, .8, 1.0))
    cups = "".join(f'<circle cx="{f(x + 16 + dx)}" cy="{f(base - h * fr - 2)}" r="1.5" fill="{INK}"></circle>'
                   for fr in (.58, .8, 1.0) for dx in (-2.2, 2.2))
    guys = (f"M{f(x)} {f(base - h * .62)} L{f(x - 30)} {f(base)} M{f(x)} {f(base - h * .62)} L{f(x + 28)} {f(base)} "
            f"M{f(x)} {f(base - h * .92)} L{f(x - 44)} {f(base)}")
    return (f'<path d="{guys}" stroke="{INK}" stroke-width=".6" opacity=".55"></path>'
            f'<path d="M{f(x - 3.6)} {f(base)} L{f(x - 1.2)} {f(top)} M{f(x + 3.6)} {f(base)} L{f(x + 1.2)} {f(top)} '
            f'M{f(x - 3.6)} {f(base)} {zz}" stroke="{INK}" stroke-width=".9" fill="none"></path>'
            f'<path d="{booms} M{f(x)} {f(top)} V{f(top - 10)} M{f(x)} {f(top - 8)} L{f(x - 9)} {f(top - 6)}" '
            f'stroke="{INK}" stroke-width="1.1"></path>{cups}')


def converter(x: float, base: float) -> str:
    seams = " ".join(f"M{f(xi)} {f(base - 60)} V{f(base)}" for xi in _frange(x + 10, x + 60, 10))
    return (
        f'<path d="M{f(x - 34)} {f(base)} V{f(base - 30)} M{f(x - 10)} {f(base)} V{f(base - 30)} M{f(x - 36)} {f(base - 30)} '
        f'H{f(x - 8)} M{f(x - 34)} {f(base - 30)} L{f(x - 10)} {f(base - 12)} M{f(x - 10)} {f(base - 30)} L{f(x - 34)} '
        f'{f(base - 12)} M{f(x - 26)} {f(base - 30)} v5 M{f(x - 18)} {f(base - 30)} v5" stroke="{INK}" stroke-width="1.1" '
        f'fill="none"></path>'
        f'<rect x="{f(x)}" y="{f(base - 62)}" width="66" height="62" fill="{OLIVE}" stroke="{INK}" stroke-width="1.1"></rect>'
        f'<path d="{seams}" stroke="{DAY}" stroke-width=".7" opacity=".3"></path>'
        f'<rect x="{f(x + 66)}" y="{f(base - 40)}" width="42" height="40" fill="{OLIVE}" stroke="{INK}" stroke-width="1.1"></rect>'
        f'<rect x="{f(x + 66)}" y="{f(base - 40)}" width="42" height="40" fill="{DAY}" opacity=".2"></rect>'
        f'<path d="M{f(x - 1)} {f(base - 62)} H{f(x + 67)}" stroke="{DAY}" stroke-width="1.4" opacity=".7"></path>'
        f'<rect x="{f(x + 76)}" y="{f(base - 16)}" width="10" height="16" fill="{INK}" opacity=".75"></rect>')


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


def ccgt(x: float, base: float, s: float) -> str:
    def r(rx: float, ry: float, w: float, h: float, fill: str) -> str:
        return (f'<rect x="{f(x + rx * s)}" y="{f(base - ry * s)}" width="{f(w * s)}" height="{f(h * s)}" '
                f'fill="{fill}" stroke="{INK}" stroke-width=".9"></rect>')
    return "".join([
        r(66, 104, 7, 60, DAY), r(86, 112, 7, 68, DAY),
        f'<path d="M{f(x + 66 * s)} {f(base - 98 * s)} h{f(7 * s)} M{f(x + 86 * s)} {f(base - 106 * s)} h{f(7 * s)}" '
        f'stroke="{CLAY}" stroke-width="{f(3 * s)}"></path>',
        r(62, 46, 15, 46, CLAY), r(82, 46, 15, 46, CLAY), r(0, 32, 62, 32, CLAY), r(-24, 16, 24, 16, DAY),
        f'<path d="M{f(x)} {f(base - 32 * s)} L{f(x + 31 * s)} {f(base - 38 * s)} L{f(x + 62 * s)} {f(base - 32 * s)}" '
        f'fill="{CLAY}" stroke="{INK}" stroke-width=".9" stroke-linejoin="round"></path>',
    ])


def pipeline(x: float, base: float) -> str:
    """Two pipes on trestles with a valve and a flanged riser: an interconnection point."""
    sup = " ".join(f"M{f(xx)} {f(base)} V{f(base - 16)} M{f(xx - 5)} {f(base - 16)} H{f(xx + 5)}" for xx in (x + 8, x + 34, x + 70))
    return (f'<path d="{sup}" stroke="{INK}" stroke-width="1.1" fill="none"></path>'
            f'<rect x="{f(x - 2)}" y="{f(base - 24)}" width="84" height="7" fill="{CLAY}" stroke="{INK}" stroke-width=".9"></rect>'
            f'<rect x="{f(x - 2)}" y="{f(base - 33)}" width="84" height="6" fill="{CLAY}" stroke="{INK}" stroke-width=".9" opacity=".85"></rect>'
            f'<path d="M{f(x + 40)} {f(base - 33)} V{f(base - 40)}" stroke="{INK}" stroke-width="2.2"></path>'
            f'<circle cx="{f(x + 40)}" cy="{f(base - 44)}" r="5.5" fill="none" stroke="{INK}" stroke-width="1.4"></circle>'
            f'<path d="M{f(x + 34.5)} {f(base - 44)} h11 M{f(x + 40)} {f(base - 49.5)} v11" stroke="{INK}" stroke-width=".9"></path>'
            f'<path d="M{f(x + 20)} {f(base - 34)} v12 M{f(x + 60)} {f(base - 34)} v12" stroke="{INK}" stroke-width="1.6"></path>')


def tanks(x: float, base: float) -> str:
    def tank(tx: float, w: float, h: float) -> str:
        return (f'<path d="M{f(tx)} {f(base)} V{f(base - h)} Q{f(tx + w / 2)} {f(base - h - w * .2)} {f(tx + w)} '
                f'{f(base - h)} V{f(base)} Z" fill="{CLAY}" stroke="{INK}" stroke-width="1"></path>'
                f'<path d="M{f(tx + 4)} {f(base)} L{f(tx + w * .45)} {f(base - h + 1)} M{f(tx)} {f(base - h + 6)} '
                f'H{f(tx + w)}" stroke="{INK}" stroke-width=".7" opacity=".6" fill="none"></path>')
    return tank(x, 44, 30) + tank(x + 50, 30, 22)


def sc(svg: str, x: float, base: float, s: float) -> str:
    return f'<g transform="translate({f(x)} {f(base)}) scale({s}) translate({f(-x)} {f(-base)})">{svg}</g>'


# ================================================================ vendor marks: the asset each vendor's cable leaves on the homepage
MARK_W, MARK_H = 96, 50


def mark(kind: str) -> str:
    """A small plate of the landscape asset that feeds the vendor on the homepage, standing on a ground line."""
    base = MARK_H - 5
    if kind == "substation":
        body = sc(substation(8, base), 8, base, .88)
    elif kind == "metmast":
        body = metmast(48, base, 42)
    elif kind == "converter":
        body = sc(converter(40, base), 40, base, .62)
    elif kind == "pylon":
        body = (f'<g stroke="{INK}" fill="none" stroke-linecap="round" stroke-width="1.2">{pylon(48, base, .36)}</g>'
                f'<path d="M0 {f(base - 22)} Q24 {f(base - 16)} {f(48 - 10.8)} {f(base - 23.8)} M{f(48 + 10.8)} {f(base - 23.8)} '
                f'Q72 {f(base - 16)} 96 {f(base - 22)} M0 {f(base - 31)} Q24 {f(base - 26)} {f(48 - 8.6)} {f(base - 33)} '
                f'M{f(48 + 8.6)} {f(base - 33)} Q72 {f(base - 26)} 96 {f(base - 31)}" stroke="{INK}" stroke-width=".7" '
                f'fill="none"></path>')
    elif kind == "ccgt":
        body = ccgt(36, base, .38)
    elif kind == "pipeline":
        body = pipeline(8, base)
    else:
        body = tanks(10, base)
    ground = (f'<path d="M0 {base} H{MARK_W}" stroke="{INK}" stroke-width="1.5"></path>'
              f'<path d="M0 {base + .75} H{MARK_W} V{base + 5} H0 Z" fill="{OLIVE}"></path>')
    return (f'<svg class="mk" width="{MARK_W}" height="{MARK_H}" viewBox="0 0 {MARK_W} {MARK_H}" aria-hidden="true">'
            f'{body}{ground}</svg>')


# ================================================================ the sky's lower edge
def horizon() -> str:
    """A shallow landscape strip: far and near ridges, onshore wind on the near ridge, a pylon line, the energised land."""
    h = 124
    far = [(-20, 64), (150, 50), (330, 60), (520, 44), (700, 56), (900, 46), (1080, 58), (1260, 48), (1460, 60)]
    near = [(-20, 82), (130, 72), (300, 80), (470, 68), (640, 78), (820, 70), (990, 62), (1160, 72), (1320, 64), (1460, 74)]
    land = [(-20, 98), (220, 94), (520, 100), (840, 95), (1140, 101), (1460, 97)]
    surf = 112
    out = [f'<path d="{smooth(far)} L1460 {h} L-20 {h} Z" fill="{HORIZON}" opacity=".5"></path>',
           f'<path d="{smooth(near)} L1460 {h} L-20 {h} Z" fill="{HORIZON}"></path>']
    for i, (tx, ty, th) in enumerate([(990, 63, 44), (1076, 66, 38), (1160, 73, 41), (1244, 68, 36), (1320, 65, 42)]):
        out.append(turbine(tx, ty, th, th * .5, ["sp2", "sp1", "sp3"][i % 3], 23 * i + 8))
    out.append(f'<path d="{smooth(land)} L1460 {surf} L-20 {surf} Z" fill="{CHART}"></path>')
    out.append(f'<path d="{smooth([(-20, 104), (400, 102), (900, 106), (1460, 104)])}" stroke="{OLIVE}" stroke-width="1" '
               f'fill="none" opacity=".45"></path>')
    p = [(110, 100, .3), (330, 101, .33), (560, 100, .36)]
    wires = [spans([(-20, 84), (-20, 76), (-20, 70)], tips(*p[0], -1), 3), spans(tips(*p[0], 1), tips(*p[1], -1), 6),
             spans(tips(*p[1], 1), tips(*p[2], -1), 6),
             spans(tips(*p[2], 1), [(770 - 1.5, 106 - 25), (770 + 4, 106 - 22), (770 + 9, 106 - 22)], 5)]
    out.append(f'<g stroke="{INK}" fill="none" stroke-linecap="round" stroke-width="1.2">'
               + "".join(pylon(*q) for q in p) + '</g>')
    out.append(f'<path d="{" ".join(wires)}" stroke="{INK}" stroke-width=".7" fill="none" opacity=".8"></path>')
    out.append(sc(substation(770, 106), 770, 106, .5))
    out.append(f'<path d="M-20 {surf} H1460 V{h} H-20 Z" fill="{OLIVE}"></path>')
    out.append(f'<path d="M-20 {surf} H1460" stroke="{INK}" stroke-width="1.5"></path>')
    return (f'<svg class="horizon" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" '
            f'aria-label="A strip of landscape: ridges with onshore wind turbines and a line of pylons.">'
            + "".join(out) + '</svg>')


# ================================================================ footing edges
def band_bg(kind: str, seed: float) -> str:
    p = f"f{kind[:2]}"
    fills = {"bronze": (T_BRONZE, "brick", ".15"), "silver": (T_SILVER, "diag", ".22"), "gold": (T_GOLD, "stip", ".26"),
             "deep": (PETROL, "granite", ".5")}
    fill, pat, op = fills[kind]
    if kind == "deep":
        pts = [(x, 15 + 5 * math.sin(x / 140 + 1) + 3.5 * math.sin(x / 53 + 2) + 2.2 * math.sin(x / 19))
               for x in range(-40, W + 41, 20)]
        top = smooth(pts)
    else:
        top = smooth(wave(14, 6, seed))
    body = f"{top} L{W + 40} 3000 L-40 3000 Z"
    return (f'<svg class="band-bg" width="{W}" aria-hidden="true"><defs>{patterns(p)}</defs>'
            f'<path d="{body}" fill="{fill}"></path><path d="{body}" fill="url(#{p}-{pat})" opacity="{op}"></path>'
            f'<path d="{top}" stroke="{INK}" stroke-width="{2 if kind == "deep" else 1.5}" fill="none" '
            f'stroke-linejoin="round"></path></svg>')


# ================================================================ chart helpers
def pts_path(xs: list[float], ys: list[float]) -> str:
    return "M" + " L".join(f"{f(x)} {f(y)}" for x, y in zip(xs, ys))


def plate_svg(w: int, h: int, aria: str, body: str) -> str:
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{aria}">{body}</svg>')


# ---------------------------------------------------------------- landing: GB system price, daily mean (120 days)
def plate_system_price() -> str:
    s = SERIES["data_sources_landing"]
    pts = s["points"]
    w, h = 560, 262
    x0, x1, y0, y1 = 46, 546, 30, 222
    vmax = 240.0
    X = lambda i: x0 + (x1 - x0) * i / (len(pts) - 1)  # noqa: E731
    Y = lambda v: y1 - (y1 - y0) * v / vmax  # noqa: E731
    o = []
    for t in (0, 100, 200):
        o.append(f'<path d="M{x0} {f(Y(t))} H{x1}" stroke="{INK}" stroke-width="{1.5 if t == 0 else .6}" '
                 f'opacity="{1 if t == 0 else .25}"></path>')
        o.append(f'<text x="{x0 - 8}" y="{f(Y(t) + 4.5)}" text-anchor="end" {TICK} fill="{INK2}">{t}</text>')
    o.append(f'<text x="3" y="15" {LAB} fill="{INK}">£/MWh</text>')
    dates = [dt.date.fromisoformat(p[0]) for p in pts]
    for i, d in enumerate(dates):
        if d.day == 1:
            o.append(f'<path d="M{f(X(i))} {y1} v5" stroke="{INK}" stroke-width="1"></path>')
            o.append(f'<text x="{f(X(i) + 4)}" y="{y1 + 20}" {TICK} fill="{INK2}">{d.strftime("%B")}</text>')
    xs = [X(i) for i in range(len(pts))]
    ys = [Y(p[1]) for p in pts]
    o.append(f'<path d="{pts_path(xs, ys)} L{f(xs[-1])} {y1} L{f(xs[0])} {y1} Z" fill="{T_TOP}"></path>')
    o.append(f'<path d="{pts_path(xs, ys)}" fill="none" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"></path>')
    vals = [p[1] for p in pts]
    hi, lo = vals.index(max(vals)), vals.index(min(vals))
    for i, anchor, dx, dy in ((hi, "end", -9, 4), (lo, "start", 9, 14)):
        d = dates[i]
        o.append(f'<circle cx="{f(xs[i])}" cy="{f(ys[i])}" r="3" fill="{INK}"></circle>')
        o.append(f'<text x="{f(xs[i] + dx)}" y="{f(ys[i] + dy)}" text-anchor="{anchor}" {LAB} fill="{INK}">'
                 f'{d.day} {d.strftime("%B")}, {vals[i]:.2f}</text>')
    aria = (f"Line chart of the GB system price, daily mean, in pounds per megawatt hour, 26 May to 22 September 2026. "
            f"It ranges from {min(vals):.2f} on 13 June to {max(vals):.2f} on 13 September.")
    return plate_svg(w, h, aria, "".join(o))


# ---------------------------------------------------------------- hub: GB wind (FUELHH WIND), monthly mean (60 months)
def plate_wind() -> str:
    s = SERIES["elexon_hub"]
    pts = s["points"]
    w, h = 600, 262
    x0, x1, y0, y1 = 56, 588, 30, 222
    vmax = 12000.0
    X = lambda i: x0 + (x1 - x0) * i / (len(pts) - 1)  # noqa: E731
    Y = lambda v: y1 - (y1 - y0) * v / vmax  # noqa: E731
    o = []
    for t in (0, 4000, 8000, 12000):
        o.append(f'<path d="M{x0} {f(Y(t))} H{x1}" stroke="{INK}" stroke-width="{1.5 if t == 0 else .6}" '
                 f'opacity="{1 if t == 0 else .25}"></path>')
        o.append(f'<text x="{x0 - 8}" y="{f(Y(t) + 4.5)}" text-anchor="end" {TICK} fill="{INK2}">{fnum(t)}</text>')
    o.append(f'<text x="3" y="15" {LAB} fill="{INK}">MW</text>')
    xs = [X(i) for i in range(len(pts))]
    ys = [Y(p[1]) for p in pts]
    o.append(f'<path d="{pts_path(xs, ys)} L{f(xs[-1])} {y1} L{f(xs[0])} {y1} Z" fill="{HORIZON}" opacity=".85"></path>')
    o.append(f'<path d="{pts_path(xs, ys)}" fill="none" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"></path>')
    for i, p in enumerate(pts):
        if p[0].endswith("-01"):
            o.append(f'<path d="M{f(xs[i])} {y1} v5" stroke="{INK}" stroke-width="1"></path>')
            o.append(f'<text x="{f(xs[i])}" y="{y1 + 20}" text-anchor="middle" {TICK} fill="{INK2}">{p[0][:4]}</text>')
    vals = [p[1] for p in pts]
    hi, lo = vals.index(max(vals)), vals.index(min(vals))
    months = {p[0]: dt.date.fromisoformat(p[0] + "-01").strftime("%B %Y") for p in pts}
    o.append(f'<circle cx="{f(xs[hi])}" cy="{f(ys[hi])}" r="3" fill="{INK}"></circle>'
             f'<text x="{f(xs[hi] - 9)}" y="{f(ys[hi] + 4)}" text-anchor="end" {LAB} fill="{INK}">'
             f'{months[pts[hi][0]]}, {fnum(vals[hi])}</text>')
    o.append(f'<circle cx="{f(xs[lo])}" cy="{f(ys[lo])}" r="3" fill="{INK}"></circle>'
             f'<text x="{f(xs[lo])}" y="{f(ys[lo] + 22)}" text-anchor="middle" {LAB} fill="{INK}">'
             f'{months[pts[lo][0]]}, {fnum(vals[lo])}</text>')
    aria = ("Area chart of GB transmission-metered wind generation, the mean half-hourly output of each month, in megawatts, "
            f"September 2021 to August 2026. Winters run high and summers low; the highest month is January 2026 at "
            f"{fnum(vals[hi])} MW and the lowest August 2022 at {fnum(vals[lo])} MW.")
    return plate_svg(w, h, aria, "".join(o))


# ---------------------------------------------------------------- models: demand v1 band vs outturn (96 half-hours)
def plate_demand() -> str:
    s = SERIES["models_landing_demand"]
    pts = s["points"]  # delivery_time_utc, actual, q05, q50, q95
    w, h = 936, 272
    x0, x1, y0, y1 = 58, 780, 28, 232
    vmin, vmax = 16000.0, 32000.0
    X = lambda i: x0 + (x1 - x0) * i / (len(pts) - 1)  # noqa: E731
    Y = lambda v: y1 - (y1 - y0) * (v - vmin) / (vmax - vmin)  # noqa: E731
    o = []
    for t in (18000, 22000, 26000, 30000):
        o.append(f'<path d="M{x0} {f(Y(t))} H{x1}" stroke="{INK}" stroke-width=".6" opacity=".25"></path>')
        o.append(f'<text x="{x0 - 8}" y="{f(Y(t) + 4.5)}" text-anchor="end" {TICK} fill="{INK2}">{fnum(t)}</text>')
    o.append(f'<path d="M{x0} {y1} H{x1}" stroke="{INK}" stroke-width="1.5"></path>')
    o.append(f'<text x="3" y="15" {LAB} fill="{INK}">MW</text>')
    xs = [X(i) for i in range(len(pts))]
    lo = [Y(p[2]) for p in pts]
    md = [Y(p[3]) for p in pts]
    hi = [Y(p[4]) for p in pts]
    ac = [Y(p[1]) for p in pts]
    band = pts_path(xs, hi) + " L" + " L".join(f"{f(x)} {f(y)}" for x, y in zip(reversed(xs), reversed(lo))) + " Z"
    o.append(f'<path d="{band}" fill="{OLIVE}" opacity=".3"></path>')
    o.append(f'<path d="{pts_path(xs, md)}" fill="none" stroke="{OLIVE}" stroke-width="1.8" stroke-linejoin="round"></path>')
    o.append(f'<path d="{pts_path(xs, ac)}" fill="none" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"></path>')
    for i, p in enumerate(pts):
        hh = p[0][11:16]
        if hh in ("00:00", "12:00"):
            o.append(f'<path d="M{f(xs[i])} {y1} v5" stroke="{INK}" stroke-width="1"></path>')
            day = dt.date.fromisoformat(p[0][:10])
            lab = f"{day.day} August, {hh}" if hh == "00:00" else hh
            o.append(f'<text x="{f(xs[i] + 4)}" y="{y1 + 21}" {TICK} fill="{INK2}">{lab}</text>')
    # direct labels at the right end, spread so none collide
    ends = sorted([(ac[-1], "outturn", INK), (md[-1], "median forecast, q0.5", "#4E5E2C"),
                   (hi[-1], "q0.95", INK2), (lo[-1], "q0.05", INK2)])
    last = -99.0
    for y, t, c in ends:
        y = max(y, last + 17)
        last = y
        o.append(f'<text x="{x1 + 12}" y="{f(y + 4.5)}" {LAB} fill="{c}">{t}</text>')
    aria = ("Line chart of GB national demand in megawatts over 96 half-hours, 20 and 21 August 2026: the day-ahead "
            "demand model's median forecast and its band from the 0.05 to the 0.95 quantile, against the outturn. Demand "
            "runs from about 17,500 MW overnight to about 31,600 MW; the outturn stays close to the median and inside the "
            "band for most of the two days.")
    return plate_svg(w, h, aria, "".join(o))


# ---------------------------------------------------------------- architecture: what lands on disk (drawn, no numbers)
def _sheet(x: float, y: float, w: float, h: float, fill: str, fold: float = 14) -> str:
    return (f'<path d="M{f(x)} {f(y)} H{f(x + w - fold)} L{f(x + w)} {f(y + fold)} V{f(y + h)} H{f(x)} Z" fill="{fill}" '
            f'stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"></path>'
            f'<path d="M{f(x + w - fold)} {f(y)} V{f(y + fold)} H{f(x + w)}" fill="none" stroke="{INK}" stroke-width="1.1"></path>')


def plate_disk() -> str:
    w, h = 936, 318
    p = "dk"
    o = [f'<defs>{patterns(p)}</defs>']
    # bronze: the body as sent, and its sidecar
    bx, by = 2, 40
    o.append(_sheet(bx + 118, by + 26, 118, 150, DAY))
    rows = []
    for k in range(9):
        yy = by + 58 + k * 13
        rows.append(f"M{bx + 130} {yy} h{16 + (k * 7) % 20} M{bx + 158 + (k * 7) % 20} {yy} h{24 + (k * 11) % 30}")
    o.append(f'<path d="{" ".join(rows)}" stroke="{INK}" stroke-width="2.2" opacity=".55"></path>')
    o.append(_sheet(bx, by, 150, 190, T_BRONZE))
    o.append(f'<path d="M{bx} {by} H{bx + 136} L{bx + 150} {by + 14} V{by + 190} H{bx} Z" fill="url(#{p}-brick)" opacity=".18"></path>')
    body = []
    ind = [0, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 0]
    for k, lv in enumerate(ind):
        yy = by + 22 + k * 12
        body.append(f"M{bx + 14 + lv * 12} {yy} h{34 + (k * 13) % 44 - lv * 6}")
    o.append(f'<path d="{" ".join(body)}" stroke="{INK}" stroke-width="2.2" opacity=".7" stroke-linecap="round"></path>')
    o.append(f'<g {LAB} fill="{INK}"><text x="{bx}" y="{by + 216}">the body, bytes as the vendor sent them</text>'
             f'<text x="{bx + 160}" y="{by + 14}">its sidecar: request and hash</text></g>')
    # silver: a Parquet file, typed columns in row groups, a set of them behind it
    sx, sy, sw, sh = 372, 86, 236, 150
    for k in (2, 1):
        o.append(f'<rect x="{sx + 14 * k}" y="{sy - 12 * k}" width="{sw}" height="{sh}" fill="{T_SILVER}" stroke="{INK}" '
                 f'stroke-width="1.1" opacity="{1 - .25 * k}"></rect>')
    o.append(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" fill="{T_SILVER}" stroke="{INK}" stroke-width="1.5"></rect>')
    o.append(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" fill="url(#{p}-diag)" opacity=".22"></rect>')
    cols = 6
    cw = sw / cols
    grid = " ".join(f"M{f(sx + cw * c)} {sy} V{sy + sh - 22}" for c in range(1, cols))
    grid += " " + " ".join(f"M{sx} {f(sy + 16 + (sh - 38) * r / 3)} H{sx + sw}" for r in (1, 2))
    o.append(f'<path d="{grid}" stroke="{INK}" stroke-width=".9"></path>')
    o.append(f'<path d="M{sx} {sy + 16} H{sx + sw} M{sx} {sy + sh - 22} H{sx + sw}" stroke="{INK}" stroke-width="1.2"></path>')
    o.append(f'<rect x="{sx}" y="{sy + sh - 22}" width="{sw}" height="22" fill="{SILVER}" opacity=".55"></rect>')
    heads = "".join(f'<rect x="{f(sx + cw * c + 7)}" y="{sy + 6}" width="{f(cw - 14)}" height="4" fill="{INK}" opacity=".6"></rect>'
                    for c in range(cols))
    o.append(heads)
    o.append(f'<g {LAB} fill="{INK}">'
             f'<text x="{sx}" y="{sy + sh + 26}">typed columns, stored in row groups</text>'
             f'<text x="{sx}" y="{sy + sh + 44}">the schema in the footer</text>'
             f'<text x="{sx}" y="{sy + sh + 62}">one file per data date, by year and month</text></g>')
    # gold: the catalogue file; its views read the Parquet where it lies
    gx, gy = 700, 34
    o.append(_sheet(gx + 40, gy, 150, 62, T_GOLD, 12))
    o.append(f'<path d="M{gx + 40} {gy} H{gx + 178} L{gx + 190} {gy + 12} V{gy + 62} H{gx + 40} Z" fill="url(#{p}-stip)" opacity=".3"></path>')
    o.append(f'<text class="mono" x="{gx + 54}" y="{gy + 38}" font-size="13.5" fill="{INK}">gridflow.duckdb</text>')
    files = [(gx + 0, T_SILVER), (gx + 62, T_SILVER), (gx + 124, T_SILVER), (gx + 186, T_GOLD)]
    fy = gy + 176
    rays = []
    for fx, fill in files:
        o.append(f'<rect x="{fx}" y="{fy}" width="46" height="34" fill="{fill}" stroke="{INK}" stroke-width="1.2"></rect>')
        o.append(f'<path d="M{fx + 12} {fy} V{fy + 34} M{fx + 24} {fy} V{fy + 34} M{fx + 36} {fy} V{fy + 34}" stroke="{INK}" '
                 f'stroke-width=".6" opacity=".5"></path>')
        rays.append(f"M{gx + 115} {gy + 62} L{fx + 23} {fy}")
    o.append(f'<path d="{" ".join(rays)}" stroke="{INK}" stroke-width=".9" stroke-dasharray="2 4" fill="none"></path>')
    o.append(f'<g {LAB} fill="{INK}">'
             f'<text x="{gx}" y="{fy + 60}">views read the Parquet in place;</text>'
             f'<text x="{gx}" y="{fy + 78}">the catalogue holds no copies</text></g>')
    aria = ("Drawing of what lands on disk. Left, bronze: a sheet of raw response text with a smaller sidecar sheet behind it, "
            "holding the request and a hash. Centre, silver: a Parquet file drawn as typed columns in row groups with the "
            "schema in its footer, and more files stacked behind it, one per data date. Right, gold: the gridflow.duckdb "
            "catalogue file, with dotted sight lines to four Parquet files below it, because its views read the files "
            "where they lie.")
    return plate_svg(w, h, aria, "".join(o))


# ---------------------------------------------------------------- layer swatches for the architecture walk (as on the homepage key)
def swatch(kind: str) -> str:
    p = f"sw{kind[:2]}"
    fill, pat, op = {"bronze": (T_BRONZE, "brick", ".45"), "silver": (T_SILVER, "diag", ".45"),
                     "gold": (T_GOLD, "stip", ".45"), "deep": (PETROL, "granite", ".6")}[kind]
    return (f'<svg class="sw" width="46" height="30" viewBox="0 0 46 30" aria-hidden="true"><defs>{patterns(p)}</defs>'
            f'<rect x=".75" y=".75" width="44.5" height="28.5" fill="{fill}"></rect>'
            f'<rect x=".75" y=".75" width="44.5" height="28.5" fill="url(#{p}-{pat})" opacity="{op}"></rect>'
            f'<rect x=".75" y=".75" width="44.5" height="28.5" fill="none" stroke="{INK}" stroke-width="1.5"></rect></svg>')
