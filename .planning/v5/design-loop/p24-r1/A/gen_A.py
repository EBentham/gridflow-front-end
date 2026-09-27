"""Designer A, "The section": one geological section through a dataset. Emits A-<name>.dc.html + static copies.

Drawing pieces (turbine, pylon, ccgt, substation, converter, gas terminal, battery, cable, strata patterns) are
copied from the locked homepage generator (.planning/v4/design-loop/r3-7/gen_a.py) and re-parameterised on this
page's surface line. Every number drawn comes from pack/specimens.json.
"""
from __future__ import annotations

import html
import json
import math
import re
import sys
from datetime import date
from pathlib import Path

from content import SPECIMENS

HERE = Path(__file__).parent
PACK = json.loads((HERE.parent / "pack" / "specimens.json").read_text(encoding="utf-8"))
DATA = {s["id"]: s for s in PACK["specimens"]}
DFH = json.loads((HERE / "df_html.json").read_text(encoding="utf-8"))
HEIGHTS_F = HERE / "heights.json"
HEIGHTS = json.loads(HEIGHTS_F.read_text(encoding="utf-8")) if HEIGHTS_F.exists() else {}

PETROL, HORIZON, CHART, OLIVE = "#155A6E", "#3E8C97", "#AFC64E", "#66793B"
INK, DAY, CLAY, KHAKI, MUTED, RULE = "#1C2B22", "#F6F4EC", "#C77E3C", "#A39A6A", "#5d6a55", "#DFDACA"
BRONZE, SILVER, GOLD = "#A5713C", "#9FADAB", "#C2A14A"
T_GOLD, T_SILVER, T_BRONZE, T_TOP = "#E9DDAF", "#DCE2DF", "#E2CDB3", "#ECE8DA"
SOFT = "#3F4A3B"
ON2 = "#CFE0DC"
W = 1440
SURF = 640     # the ground surface under the sky; set per page


def f(v: float) -> str:
    return f"{v:.1f}".rstrip("0").rstrip(".") if abs(v - round(v)) > 1e-9 else str(int(round(v)))


def smooth(pts: list[tuple[float, float]]) -> str:
    d = f"M{f(pts[0][0])} {f(pts[0][1])}"
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i > 0 else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else pts[i + 1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}"
    return d


def prof(x: float) -> float:
    return SURF + 4 * math.sin(x / 190 + 0.6) - 2.5 * math.sin(x / 83 + 1.3)


def wave(y0: float, amp: float, seed: float, step: int = 120) -> list[tuple[float, float]]:
    return [(x, y0 + amp * math.sin(x / 210 + seed) + amp * 0.45 * math.sin(x / 73 + seed * 2.3))
            for x in range(-40, W + step + 41, step)]


def _frange(a: float, b: float, step: float) -> list[float]:
    out, v = [], a
    while v <= b + 1e-6:
        out.append(v)
        v += step
    return out


def sc(svg: str, x: float, base: float, s: float) -> str:
    return f'<g transform="translate({f(x)} {f(base)}) scale({s}) translate({f(-x)} {f(-base)})">{svg}</g>'


# ================================================================ landscape pieces (from the homepage)
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


def ccgt(x: float, base: float, s: float) -> str:
    def r(rx: float, ry: float, w: float, h: float, fill: str, extra: str = "") -> str:
        return (f'<rect x="{f(x + rx * s)}" y="{f(base - ry * s)}" width="{f(w * s)}" height="{f(h * s)}" '
                f'fill="{fill}" stroke="{INK}" stroke-width=".9" {extra}></rect>')
    return "\n".join([
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


def battery(x: float, base: float) -> str:
    out = []
    for dy, h, off in [(19, 9, 5), (10, 10, 0)]:
        for k in range(4):
            cx = x + off + k * 23
            out.append(f'<rect x="{f(cx)}" y="{f(base - dy)}" width="20" height="{h}" fill="{KHAKI}" stroke="{INK}" '
                       f'stroke-width=".8"></rect>')
            out.append(f'<path d="M{f(cx + 7)} {f(base - dy + 1.5)} V{f(base - dy + h - 1.5)} M{f(cx + 12)} '
                       f'{f(base - dy + 2.5)} h5" stroke="{INK}" stroke-width=".6" opacity=".7"></path>')
    out.append(f'<rect x="{f(x + 98)}" y="{f(base - 14)}" width="12" height="14" fill="{DAY}" stroke="{INK}" '
               f'stroke-width=".8"></rect>')
    posts = " ".join(f"M{f(xp)} {f(base)} v-13" for xp in _frange(x - 8, x + 116, 12))
    out.append(f'<path d="{posts} M{f(x - 8)} {f(base - 12)} H{f(x + 116)}" stroke="{INK}" stroke-width=".6" '
               f'opacity=".65"></path>')
    return "\n".join(out)


def substation(x: float, base: float) -> tuple[str, list[tuple[float, float]]]:
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
    posts = " ".join(f"M{f(xp)} {f(base)} v-12" for xp in _frange(x - 10, x + 96, 12))
    out.append(f'<path d="{posts} M{f(x - 10)} {f(base - 11)} H{f(x + 96)}" stroke="{INK}" stroke-width=".6" '
               f'opacity=".65"></path>')
    ends = [(x - 3, base - 50), (x + 8, base - 44), (x + 18, base - 44)]
    return "\n".join(out), ends


def converter(x: float, base: float) -> str:
    seams = " ".join(f"M{f(xi)} {f(base - 60)} V{f(base)}" for xi in _frange(x + 10, x + 60, 10))
    return "\n".join([
        f'<path d="M{f(x - 34)} {f(base)} V{f(base - 30)} M{f(x - 10)} {f(base)} V{f(base - 30)} M{f(x - 36)} {f(base - 30)} '
        f'H{f(x - 8)} M{f(x - 34)} {f(base - 30)} L{f(x - 10)} {f(base - 12)} M{f(x - 10)} {f(base - 30)} L{f(x - 34)} '
        f'{f(base - 12)} M{f(x - 26)} {f(base - 30)} v5 M{f(x - 18)} {f(base - 30)} v5" stroke="{INK}" stroke-width="1.1" '
        f'fill="none"></path>',
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


def platform(x: float, sea: float) -> str:
    """An offshore gas platform: a jacket standing in the sea, a deck, a module, a derrick and a flare boom."""
    dk = sea - 26
    legs = (f"M{f(x - 16)} {f(sea + 4)} L{f(x - 11)} {f(dk)} M{f(x + 16)} {f(sea + 4)} L{f(x + 11)} {f(dk)} "
            f"M{f(x - 14)} {f(sea - 4)} L{f(x + 12)} {f(dk + 8)} M{f(x + 14)} {f(sea - 4)} L{f(x - 12)} {f(dk + 8)}")
    derrick = (f"M{f(x + 6)} {f(dk - 6)} L{f(x + 11)} {f(dk - 38)} L{f(x + 16)} {f(dk - 6)} "
               f"M{f(x + 7.5)} {f(dk - 16)} H{f(x + 14.5)} M{f(x + 9)} {f(dk - 26)} H{f(x + 13)} "
               f"M{f(x + 7.5)} {f(dk - 16)} L{f(x + 13)} {f(dk - 26)}")
    return "\n".join([
        f'<path d="{legs}" stroke="{INK}" stroke-width="1.1" fill="none"></path>',
        f'<path d="M{f(x - 22)} {f(dk - 2)} L{f(x - 44)} {f(dk - 24)}" stroke="{INK}" stroke-width="1.3"></path>',
        f'<rect x="{f(x - 24)}" y="{f(dk - 6)}" width="48" height="6" fill="{DAY}" stroke="{INK}" stroke-width="1"></rect>',
        f'<rect x="{f(x - 20)}" y="{f(dk - 20)}" width="24" height="14" fill="{KHAKI}" stroke="{INK}" stroke-width=".9"></rect>',
        f'<path d="{derrick}" stroke="{INK}" stroke-width="1" fill="none"></path>',
    ])


def cable(d: str, core: str = BRONZE, sheath: float = 4.4, corew: float = 1.5) -> str:
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{sheath}" stroke-linecap="round" '
            f'stroke-linejoin="round"></path>'
            f'<path d="{d}" fill="none" stroke="{core}" stroke-width="{corew}" stroke-linecap="round" '
            f'stroke-linejoin="round"></path>')


# ================================================================ the landscape strip, per dataset
def ground(sea: bool) -> list[str]:
    B = SURF
    p: list[str] = []
    if sea:
        p.append(f'<rect x="860" y="{B - 118}" width="600" height="70" fill="{HORIZON}"></rect>')
        p.append(f'<rect x="860" y="{B - 118}" width="600" height="70" fill="{DAY}" opacity=".13"></rect>')
        wv = " ".join(f"M{x0} {B - y0} h{ln}" for x0, y0, ln in
                      [(1000, 108, 40), (1090, 104, 26), (1210, 110, 34), (1330, 105, 44), (1040, 96, 22),
                       (1170, 92, 30), (1290, 98, 18), (1395, 92, 28)])
        p.append(f'<path d="{wv}" stroke="{DAY}" stroke-width="1" opacity=".35"></path>')
        p.append(f'<path d="M1180 {B - 118} C1230 {B - 122} 1270 {B - 125} 1320 {B - 125} S1400 {B - 127} 1460 '
                 f'{B - 126} V{B - 118} Z" fill="{HORIZON}" opacity=".6"></path>')
        far = [(-20, B - 150), (120, B - 172), (300, B - 160), (470, B - 184), (640, B - 166), (790, B - 146),
               (880, B - 120), (960, B - 100)]
        near = [(-20, B - 126), (90, B - 150), (210, B - 160), (330, B - 146), (452, B - 166), (590, B - 154),
                (720, B - 136), (820, B - 110), (900, B - 90)]
    else:
        far = [(-20, B - 150), (120, B - 172), (300, B - 160), (470, B - 184), (640, B - 166), (790, B - 150),
               (940, B - 138), (1090, B - 146), (1240, B - 132), (1350, B - 140), (1460, B - 128)]
        near = [(-20, B - 126), (90, B - 150), (210, B - 160), (330, B - 146), (452, B - 166), (590, B - 154),
                (720, B - 136), (840, B - 118), (980, B - 104), (1120, B - 110), (1280, B - 100), (1460, B - 96)]
    p.append(f'<path d="{smooth(far)} L{far[-1][0]} {B - 30} L-20 {B - 30} Z" fill="{HORIZON}" opacity=".5"></path>')
    p.append(f'<path d="{smooth(near)} L{near[-1][0]} {B - 30} L-20 {B - 30} Z" fill="{HORIZON}"></path>')
    field = [(-20, B - 86), (160, B - 94), (340, B - 84), (520, B - 92), (700, B - 80), (880, B - 72),
             (1060, B - 64), (1240, B - 60), (1460, B - 56)]
    bottom = " ".join(f"L{f(x)} {f(prof(x))}" for x in range(1460, -21, -20))
    p.append(f'<path d="{smooth(field)} {bottom} Z" fill="{CHART}"></path>')
    bounds = [smooth([(-20, B - 66), (300, B - 70), (700, B - 60), (1100, B - 44), (1460, B - 38)]),
              smooth([(-20, B - 40), (400, B - 44), (820, B - 32), (1200, B - 22), (1460, B - 18)])]
    p.append(f'<path d="{" ".join(bounds)}" stroke="{OLIVE}" stroke-width="1" fill="none" opacity=".45"></path>')
    return p


def ridge_turbines(xs: list[int], sea: bool) -> str:
    near = dict((x, y) for x, y in [(90, 150), (210, 160), (330, 146), (452, 166), (590, 154), (720, 136)])
    out = []
    for i, x in enumerate(xs):
        hgt = [64, 70, 60, 72, 66, 58][i % 6]
        out.append(turbine(x, SURF - near[x] + 3, hgt, hgt * .5, ["sp2", "sp1", "sp3"][i % 3], 40 * i + 10))
    return "".join(out)


def offshore(xs: list[int]) -> str:
    return "".join(turbine(x, SURF - 110 + (i % 2) * 3, 28 + (i % 3) * 3, (28 + (i % 3) * 3) * .5,
                           ["sp1", "sp2", "sp3"][i % 3], 17 * i) for i, x in enumerate(xs))


def pylon_line(pts: list[tuple[float, float, float]], ends: list[tuple[float, float]] | None,
               start_edge: bool = True) -> str:
    wires = []
    if start_edge:
        x0, b0, s0 = pts[0]
        wires.append(spans([(-20, b0 - 60 * s0), (-20, b0 - 86 * s0), (-20, b0 - 104 * s0)], tips(*pts[0], -1), 5))
    for a, b in zip(pts, pts[1:]):
        wires.append(spans(tips(*a, 1), tips(*b, -1), 11))
    if ends:
        wires.append(spans(tips(*pts[-1], 1), ends, 9))
    return (f'<g stroke="{INK}" fill="none" stroke-linecap="round" stroke-width="1.35">'
            + "".join(pylon(*p) for p in pts) + '</g>'
            f'<path d="{" ".join(wires)}" stroke="{INK}" stroke-width=".8" fill="none" opacity=".85"></path>')


def placed_substation(x: float, s: float = 1.12) -> tuple[str, list[tuple[float, float]], tuple[float, float]]:
    base = prof(x + 50)
    svg, ends = substation(x, base)
    svg = sc(svg, x, base, s)
    ends = [(x + (ex - x) * s, base + (ey - base) * s) for ex, ey in ends]
    return svg, ends, (x + 42 * s, base)


def scene(spec: dict) -> tuple[str, str, tuple[float, float]]:
    """Returns (svg body, labels, cable origin) for the strip. Only real infrastructure; no solar anywhere."""
    B = SURF
    slug = spec["slug"]
    lab: list[tuple[str, float, float, str, str]] = []
    on = "#E4EFEC"
    if slug == "fuelhh":
        p = ground(True)
        p.append(ridge_turbines([90, 210, 330, 452, 590], True))
        p.append(sc(ccgt(262, B - 70, .72), 262, B - 70, 1))
        sub, ends, org = placed_substation(760)
        p.append(pylon_line([(150, B - 74, .42), (420, B - 66, .48), (640, B - 56, .54)], ends))
        p.append(sub)
        p.append(sc(converter(1000, prof(1060)), 1000, prof(1060), 1.08))
        p.append(offshore([1150, 1230, 1310, 1390]))
        lab += [("onshore wind", 40, B - 112, on, "start"), ("gas-fired power station", 300, B - 164, on, "middle"),
                ("substation", 806, B - 76, INK, "middle"), ("interconnector", 1060, B - 86, INK, "middle"),
                ("offshore wind", 1270, B - 160, on, "middle")]
    elif slug == "system_prices":
        p = ground(False)
        p.append(ridge_turbines([90, 330, 590], False))
        sub, ends, org = placed_substation(900)
        p.append(pylon_line([(120, B - 78, .46), (390, B - 70, .52), (660, B - 58, .58)], ends))
        p.append(sub)
        p.append(sc(battery(1110, prof(1170)), 1110, prof(1170), 1.12))
        p.append(pylon_line([(1300, B - 46, .44)], None, start_edge=False))
        lab += [("transmission lines", 390, B - 150, on, "middle"), ("substation", 946, B - 76, INK, "middle"),
                ("battery storage", 1172, B - 40, INK, "middle")]
    elif slug == "physical_flows":
        p = ground(True)
        p.append(ridge_turbines([90, 330, 590], True))
        p.append(sc(ccgt(262, B - 70, .72), 262, B - 70, 1))
        p.append(sc(gasterminal(860, prof(930)), 860, prof(930), 1.5))
        p.append(platform(1260, B - 96))
        # the landfall: the pipeline comes ashore and runs to the terminal on low supports
        ly = prof(1060) - 6
        sup = " ".join(f"M{f(xx)} {f(prof(xx))} V{f(ly)}" for xx in _frange(1062, 1130, 17))
        p.append(f'<path d="{sup}" stroke="{INK}" stroke-width=".8"></path>'
                 f'<path d="M1054 {f(ly)} H1140 Q1150 {f(ly)} 1152 {f(ly - 6)}" stroke="{INK}" stroke-width="4" '
                 f'fill="none" stroke-linecap="round"></path><path d="M1054 {f(ly)} H1140 Q1150 {f(ly)} 1152 '
                 f'{f(ly - 6)}" stroke="{CLAY}" stroke-width="2" fill="none" stroke-linecap="round"></path>')
        org = (926, prof(926))
        lab += [("gas-fired power station", 300, B - 164, on, "middle"), ("gas terminal", 918, B - 88, INK, "middle"),
                ("offshore platform", 1260, B - 170, on, "middle"), ("landfall", 1100, B - 36, INK, "middle")]
    else:  # bmunits_reference: a row of registered units of different kinds
        p = ground(False)
        p.append(ridge_turbines([90, 210, 330, 452], False))
        p.append(sc(ccgt(262, B - 70, .72), 262, B - 70, 1))
        p.append(sc(battery(560, prof(620)), 560, prof(620), 1.1))
        sub, ends, org = placed_substation(820)
        p.append(pylon_line([(150, B - 74, .42), (440, B - 64, .48), (700, B - 54, .54)], ends))
        p.append(sub)
        p.append(sc(converter(1060, prof(1120)), 1060, prof(1120), 1.08))
        lab += [("onshore wind", 40, B - 112, on, "start"), ("gas-fired power station", 300, B - 164, on, "middle"),
                ("battery storage", 622, B - 36, INK, "middle"), ("substation", 866, B - 76, INK, "middle"),
                ("interconnector", 1120, B - 86, INK, "middle")]
    labels = "".join(f'<text x="{f(x)}" y="{f(y)}" fill="{c}" text-anchor="{a}">{t}</text>' for t, x, y, c, a in lab)
    return "\n".join(p), labels, org


# ================================================================ chart helpers
CW, CH = 900, 470          # chart svg size
PX0, PX1 = 70, 884         # plot x range
IXW = 320                  # keyed index column


def hatch_defs(p: str) -> str:
    """Hatches for the codes the palette has no colour for: drawn unpainted, daylight with an ink hatch."""
    return (f'<pattern id="{p}A" width="6" height="4" patternUnits="userSpaceOnUse"><path d="M0 2 H6" stroke="{INK}" '
            f'stroke-width=".7"></path></pattern>'
            f'<pattern id="{p}B" width="6" height="6" patternUnits="userSpaceOnUse"><path d="M0 6 L6 0 M0 0 L6 6" '
            f'stroke="{INK}" stroke-width=".55"></path></pattern>'
            f'<pattern id="{p}C" width="4" height="4" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r=".75" '
            f'fill="{INK}"></circle></pattern>'
            f'<pattern id="{p}G" width="8" height="8" patternUnits="userSpaceOnUse"><path d="M0 8 L8 0" '
            f'stroke="{INK}" stroke-width=".6" opacity=".35"></path></pattern>')


_MK = [0]


def mark(fill: str, kind: str = "block", hatch: str | None = None) -> str:
    """A 30 x 18 key mark copied from the chart part it names. hatch: A, B, C (unpainted codes) or G (gap)."""
    _MK[0] += 1
    p = f"mk{_MK[0]}"
    w, h = 30, 18
    defs = f'<defs>{hatch_defs(p)}</defs>' if hatch else ""
    if kind == "line":
        body = (f'<path d="M1 12 L8 7 L15 10 L22 4 L29 8" fill="none" stroke="{fill}" stroke-width="1.8" '
                f'stroke-linejoin="round"></path>')
    elif kind == "dots":
        body = (f'<path d="M3 12 L15 7 L27 9" fill="none" stroke="{fill}" stroke-width="1.8"></path>'
                + "".join(f'<circle cx="{cx}" cy="{cy}" r="3" fill="{fill}" stroke="{INK}" stroke-width="1"></circle>'
                          for cx, cy in [(3, 12), (15, 7), (27, 9)]))
    elif kind == "neg":
        body = (f'<path d="M1 7 L9 7 L13 13 L19 12 L22 7 L29 7" fill="{fill}" stroke="none"></path>'
                f'<path d="M0 7 H30" stroke="{INK}" stroke-width="1"></path>'
                f'<path d="M1 3 L9 7 L13 13 L19 12 L22 7 L29 2" fill="none" stroke="{PETROL}" stroke-width="1.6"></path>')
    elif kind == "gap":
        body = (f'<rect x=".5" y="1" width="29" height="16" fill="url(#{p}G)"></rect>'
                f'<path d="M.5 1 V17 M29.5 1 V17" stroke="{INK}" stroke-width=".8"></path>')
    elif kind == "blank":
        body = f'<rect x=".75" y="3.75" width="28.5" height="10.5" fill="{DAY}" stroke="{INK}" stroke-width="1.2"></rect>'
    else:
        under = f'<rect x=".75" y="3.75" width="28.5" height="10.5" fill="{DAY}"></rect>' if hatch else ""
        f2 = f"url(#{p}{hatch})" if hatch else fill
        body = (under + f'<rect x=".75" y="3.75" width="28.5" height="10.5" fill="{f2}" stroke="{INK}" '
                f'stroke-width="1.2"></rect>')
    return f'<svg class="mk" width="{w}" height="{h}" viewBox="0 0 {w} {h}" aria-hidden="true">{defs}{body}</svg>'


def ix_entry(mk: str, name: str, codes: str = "", note: str = "") -> str:
    c = f' <span class="ix-c">{codes}</span>' if codes else ""
    n = f'<p class="ix-d">{note}</p>' if note else ""
    return f'<li>{mk}<div><p class="ix-n">{name}{c}</p>{n}</div></li>'


def axis_text(x: float, y: float, s: str, anchor: str = "end", extra: str = "") -> str:
    return f'<text x="{f(x)}" y="{f(y)}" text-anchor="{anchor}"{extra}>{s}</text>'


def fmt_int(v: float) -> str:
    return f"{v:,.0f}".replace("-", "−")


# ---------------------------------------------------------------- FUELHH: signed stacked area
def chart_fuelhh() -> tuple[str, str]:
    c = DATA["elexon/fuelhh"]["chart"]
    g = c["palette_groups_mw"]
    n = len(c["hours_utc"])
    top_y, bot_y = 22, 420
    lo, hi = -8000, 34000
    Y = lambda v: bot_y - (v - lo) / (hi - lo) * (bot_y - top_y)  # noqa: E731
    X = lambda t: PX0 + t / n * (PX1 - PX0)  # noqa: E731
    pid = "fh"
    # (group key, fill, hatch letter or None, label, label colour)
    unsigned = [("nuclear", PETROL, None, "nuclear", DAY), ("biomass", BRONZE, None, "biomass", INK),
                ("uncovered:NPSHYD", None, "A", "", INK), ("uncovered:COAL", None, "C", "", INK),
                ("uncovered:OIL", None, "C", "", INK), ("other", KHAKI, None, "other", INK),
                ("gas", CLAY, None, "gas", INK), ("wind", HORIZON, None, "wind", INK)]
    acc = [0.0] * n
    layers = []
    for key, fill, hat, lab, lc in unsigned:
        lower = acc[:]
        acc = [a + v for a, v in zip(acc, g[key])]
        layers.append((key, fill, hat, lab, lc, lower, acc[:]))
    for key, fill, hat, lab, lc in [("imports", OLIVE, None, "net imports", DAY), ("uncovered:PS", None, "B", "", INK)]:
        lower = acc[:]
        acc = [a + max(0.0, v) for a, v in zip(acc, g[key])]
        layers.append((key + "+", fill, hat, lab, lc, lower, acc[:]))
    nacc = [0.0] * n
    for key, fill, hat, lab, lc in [("imports", OLIVE, None, "net exports", DAY), ("uncovered:PS", None, "B", "", INK)]:
        upper = nacc[:]
        nacc = [a + min(0.0, v) for a, v in zip(nacc, g[key])]
        layers.append((key + "-", fill, hat, lab, lc, nacc[:], upper))

    o = [f'<defs>{hatch_defs(pid)}</defs>']
    labels = []
    for key, fill, hat, lab, lc, lower, upper in layers:
        pts_u = [(X(i + .5), Y(upper[i])) for i in range(n)]
        pts_l = [(X(i + .5), Y(lower[i])) for i in range(n)]
        # extend to the plot edges so the stack meets the frame
        pts_u = [(PX0, pts_u[0][1])] + pts_u + [(PX1, pts_u[-1][1])]
        pts_l = [(PX0, pts_l[0][1])] + pts_l + [(PX1, pts_l[-1][1])]
        d = ("M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts_u) + " L"
             + " L".join(f"{f(x)} {f(y)}" for x, y in reversed(pts_l)) + " Z")
        if hat:
            o.append(f'<path d="{d}" fill="{DAY}"></path><path d="{d}" fill="url(#{pid}{hat})"></path>')
        else:
            o.append(f'<path d="{d}" fill="{fill}"></path>')
        edge = pts_u if not key.endswith("-") else pts_l
        o.append(f'<path d="M' + " L".join(f"{f(x)} {f(y)}" for x, y in edge) + f'" fill="none" stroke="{INK}" '
                 f'stroke-width=".6" opacity=".55"></path>')
        if key == "imports-":
            k = min(range(n), key=lambda i: lower[i])
            ax_, ay_ = X(k + 3.5), Y(lower[k] * .45)
            labels.append(f'<path d="M{f(ax_)} {f(ay_)} L{f(X(15))} {f(Y(-4600) - 5)}" stroke="{INK}" stroke-width=".8"></path>'
                          f'<text x="{f(X(15) + 4)}" y="{f(Y(-4600))}">net exports</text>')
            continue
        if lab:
            best, bi = 0.0, 0
            for i in range(4, n - 4):
                th = abs(Y(lower[i]) - Y(upper[i]))
                # prefer the middle of the week a little, so labels do not crowd the frame
                score = th - abs(i - n / 2) * .02
                if score > best:
                    best, bi = score, i
            th = abs(Y(lower[bi]) - Y(upper[bi]))
            if th >= 17:
                cls = ' class="on"' if lc == DAY else ""
                lx = max(PX0 + 46, min(PX1 - 46, X(bi + .5)))
                labels.append(f'<text{cls} x="{f(lx)}" y="{f((Y(lower[bi]) + Y(upper[bi])) / 2 + 4.5)}" '
                              f'text-anchor="middle">{lab}</text>')
    # frame: axis, zero line, ticks
    days = ["20 Sep", "21 Sep", "22 Sep", "23 Sep", "24 Sep", "25 Sep", "26 Sep"]
    ax = [f'<path d="M{PX0} {top_y - 6} V{bot_y} H{PX1}" fill="none" stroke="{INK}" stroke-width="1.5"></path>',
          f'<path d="M{PX0} {f(Y(0))} H{PX1}" stroke="{INK}" stroke-width="1.2"></path>']
    tk = " ".join(f"M{f(X(24 * k))} {bot_y} v6" for k in range(8))
    ytk = " ".join(f"M{PX0 - 6} {f(Y(v))} H{PX0}" for v in (-5000, 0, 10000, 20000, 30000))
    ax.append(f'<path d="{tk} {ytk}" stroke="{INK}" stroke-width="1.2"></path>')
    txt = [axis_text(PX0 - 10, Y(v) + 4.5, fmt_int(v)) for v in (-5000, 0, 10000, 20000, 30000)]
    txt.append(axis_text(PX0 - 10, top_y - 8 + 4.5, "MW"))
    txt += [axis_text(X(24 * k + 12), bot_y + 22, d, "middle") for k, d in enumerate(days)]
    txt.append(axis_text(PX1, bot_y + 44, "settlement date; each starts at 23:00 UTC", "end", ' class="ax-i"'))
    aria = ("Stacked area chart of GB generation by fuel from elexon/fuelhh, hourly means in MW, settlement dates 20 to "
            "26 September 2026. From zero upward: nuclear (about 3.3 to 4.0 GW), biomass, non-pumped hydro, other, gas "
            "(2.1 to 15.9 GW) and wind (1.3 to 16.0 GW), then net imports and pumped storage when positive. Net exports "
            "and pumped storage hang below zero when negative; net interconnector flow ranges from 6.3 GW of exports "
            "to 6.6 GW of imports. The stack peaks near 33 GW.")
    svg = (f'<svg class="chart" width="{CW}" height="{CH}" viewBox="0 0 {CW} {CH}" role="img" aria-label="{aria}">'
           + "".join(o) + "".join(ax)
           + f'<g class="ax">{"".join(txt)}</g><g class="dl">{"".join(labels)}</g></svg>')
    ix = "".join([
        ix_entry(mark("", hatch="B"), "Pumped storage", "PS",
                 "Signed; the vendor does not say what the sign means. Drawn above or below zero as it falls."),
        ix_entry(mark(OLIVE), "Interconnectors, net", "INT*, 10 codes",
                 "Positive is import to GB; below zero, net export."),
        ix_entry(mark(HORIZON), "Wind", "WIND"),
        ix_entry(mark(CLAY), "Gas", "CCGT, OCGT"),
        ix_entry(mark(KHAKI), "Other", "OTHER", "The vendor’s own code; what it holds is undocumented."),
        ix_entry(mark("", hatch="A"), "Hydro, not pumped", "NPSHYD", "244 to 893 MW here."),
        ix_entry(mark("", hatch="C"), "Coal and oil", "COAL, OIL", "Stacked, but 66.5 MW at most here: too thin "
                                                                    "to see."),
        ix_entry(mark(BRONZE), "Biomass", "BIOMASS"),
        ix_entry(mark(PETROL), "Nuclear", "NUCLEAR"),
    ])
    return svg, ix


# ---------------------------------------------------------------- system prices: one line, negatives filled
def chart_prices() -> tuple[str, str]:
    c = DATA["elexon/system_prices"]["chart"]
    v = c["ssp_gbp_per_mwh"]
    n = len(v)
    top_y, bot_y = 22, 420
    lo, hi = -100, 640
    Y = lambda p: bot_y - (p - lo) / (hi - lo) * (bot_y - top_y)  # noqa: E731
    X = lambda t: PX0 + t / n * (PX1 - PX0)  # noqa: E731
    pts = [(X(i + .5), Y(p)) for i, p in enumerate(v)]
    z = Y(0)
    # the below-zero area: walk the line, cut at zero crossings
    polys, cur = [], []
    for i, p in enumerate(v):
        x, y = pts[i]
        if p < 0:
            if not cur:
                if i > 0 and v[i - 1] >= 0:
                    t = v[i - 1] / (v[i - 1] - p)
                    cur.append((pts[i - 1][0] + t * (x - pts[i - 1][0]), z))
                else:
                    cur.append((x, z))
            cur.append((x, y))
        elif cur:
            t = v[i - 1] / (v[i - 1] - p)
            cur.append((pts[i - 1][0] + t * (x - pts[i - 1][0]), z))
            polys.append(cur)
            cur = []
    if cur:
        cur.append((cur[-1][0], z))
        polys.append(cur)
    o = ["".join(f'<path d="M{" L".join(f"{f(a)} {f(b)}" for a, b in pl)} Z" fill="{CHART}"></path>' for pl in polys)]
    o.append(f'<path d="M{PX0} {f(z)} H{PX1}" stroke="{INK}" stroke-width="1.2"></path>')
    o.append(f'<path d="M{" L".join(f"{f(a)} {f(b)}" for a, b in pts)}" fill="none" stroke="{PETROL}" '
             f'stroke-width="1.6" stroke-linejoin="round"></path>')
    imin = v.index(min(v))
    imax = v.index(max(v))
    for i in (imin, imax):
        o.append(f'<circle cx="{f(pts[i][0])}" cy="{f(pts[i][1])}" r="3.6" fill="{DAY}" stroke="{INK}" '
                 f'stroke-width="1.4"></circle>')
    lab = [f'<text x="{f(pts[imin][0] + 10)}" y="{f(pts[imin][1] + 16)}">lowest, −50.00</text>',
           f'<text x="{f(pts[imax][0] - 10)}" y="{f(pts[imax][1] + 5)}" text-anchor="end">highest, 594.00</text>']
    days = ["19 Sep", "20 Sep", "21 Sep", "22 Sep"]
    ax = [f'<path d="M{PX0} {top_y - 6} V{bot_y} H{PX1}" fill="none" stroke="{INK}" stroke-width="1.5"></path>']
    ticks = (0, 200, 400, 600)
    tk = " ".join(f"M{f(X(48 * k))} {bot_y} v6" for k in range(5))
    ytk = " ".join(f"M{PX0 - 6} {f(Y(t))} H{PX0}" for t in ticks)
    ytk2 = " ".join(f"M{PX0 - 3} {f(Y(t))} H{PX0}" for t in (-100, 100, 300, 500))
    ax.append(f'<path d="{tk} {ytk} {ytk2}" stroke="{INK}" stroke-width="1.2"></path>')
    txt = [axis_text(PX0 - 10, Y(t) + 4.5, fmt_int(t)) for t in ticks]
    txt.append(axis_text(PX0 - 10, top_y - 8 + 4.5, "GBP/MWh", "start", ' dx="16"'))
    txt += [axis_text(X(48 * k + 24), bot_y + 22, d, "middle") for k, d in enumerate(days)]
    txt.append(axis_text(PX1, bot_y + 44, "settlement date; each starts at 23:00 UTC", "end", ' class="ax-i"'))
    aria = ("Line chart of the GB system sell price from elexon/system_prices, GBP/MWh, 192 half-hours over settlement "
            "dates 19 to 22 September 2026. The price sits near zero for much of 19 and 20 September and is below zero "
            "in 34 half-hours, lowest at minus 50.00 at 13:30 UTC on 20 September. It rises in the evenings, highest "
            "at 594.00 at 20:00 UTC on 22 September.")
    svg = (f'<svg class="chart" width="{CW}" height="{CH}" viewBox="0 0 {CW} {CH}" role="img" aria-label="{aria}">'
           + "".join(o) + "".join(ax) + f'<g class="ax">{"".join(txt)}</g><g class="dl">{"".join(lab)}</g></svg>')
    ix = "".join([
        ix_entry(mark(PETROL, "line"), "System sell price", "system_sell_price",
                 "Equal to <code>system_buy_price</code> on every row."),
        ix_entry(mark(CHART, "neg"), "Below zero", "",
                 "34 of 192 half-hours. Lowest −50.00 at 13:30 UTC on 20 September; highest 594.00 at 20:00 UTC on "
                 "22 September."),
    ])
    return svg, ix


# ---------------------------------------------------------------- physical flows: two sparse daily series
def chart_flows() -> tuple[str, str]:
    c = DATA["entsog/physical_flows"]["chart"]
    series = c["series"]
    d0 = date(2026, 8, 1)
    ndays = (date(2026, 9, 21) - d0).days + 1
    top_y, bot_y = 22, 300
    lo, hi = 0, 650
    Y = lambda p: bot_y - (p - lo) / (hi - lo) * (bot_y - top_y)  # noqa: E731
    X = lambda d: PX0 + (d + .5) / ndays * (PX1 - PX0)  # noqa: E731
    pid = "pf"
    o = [f'<defs>{hatch_defs(pid)}</defs>']
    g0, g1 = X(4.5), X(42.5)
    o.append(f'<rect x="{f(g0)}" y="{top_y}" width="{f(g1 - g0)}" height="{bot_y - top_y}" fill="url(#{pid}G)"></rect>')
    o.append(f'<path d="M{f(g0)} {top_y} V{bot_y} M{f(g1)} {top_y} V{bot_y}" stroke="{INK}" stroke-width=".8"></path>')
    o.append(f'<rect x="{f((g0 + g1) / 2 - 150)}" y="{f((top_y + bot_y) / 2 - 28)}" width="300" height="54" '
             f'fill="{T_TOP}"></rect>')
    o.append(f'<text class="gap-t" x="{f((g0 + g1) / 2)}" y="{f((top_y + bot_y) / 2 - 5)}" text-anchor="middle">'
             f'no rows held locally</text><text class="gap-t" x="{f((g0 + g1) / 2)}" y="{f((top_y + bot_y) / 2 + 15)}"'
             f' text-anchor="middle">6 August to 12 September</text>')
    cols = {"ITP-00022": CLAY, "ITP-00005": OLIVE}
    dots = []
    for s in series:
        col = cols[s["point_key"]]
        pts = []
        for p in s["points"]:
            d = (date.fromisoformat(p["timestamp_utc"][:10]) - d0).days
            pts.append((X(d), Y(p["flow_gwh_per_day"])))
        for blk in (pts[:5], pts[5:]):
            o.append(f'<path d="M{" L".join(f"{f(a)} {f(b)}" for a, b in blk)}" fill="none" stroke="{col}" '
                     f'stroke-width="2" stroke-linejoin="round"></path>')
        dots += [f'<circle cx="{f(a)}" cy="{f(b)}" r="3.4" fill="{col}" stroke="{INK}" stroke-width="1.1"></circle>'
                 for a, b in pts]
    o.append(f'<path d="M{PX0} {bot_y} H{PX1}" stroke="{INK}" stroke-width="1.5"></path>')
    o += dots
    lab = [f'<text x="{f(X(47))}" y="{f(Y(430))}" text-anchor="middle">St. Fergus entry</text>',
           f'<text x="{f(X(47))}" y="{f(Y(0) - 12)}" text-anchor="middle">Bacton (IUK) exit</text>']
    ax = [f'<path d="M{PX0} {top_y - 6} V{bot_y}" fill="none" stroke="{INK}" stroke-width="1.5"></path>']
    ticks = (0, 200, 400, 600)
    datadays = list(range(0, 5)) + list(range(43, 52))
    tk = " ".join(f"M{f(X(d))} {bot_y} v{6 if d in (0, 4, 43, 47, 51) else 3}" for d in datadays)
    ytk = " ".join(f"M{PX0 - 6} {f(Y(t))} H{PX0}" for t in ticks)
    ax.append(f'<path d="{tk} {ytk}" stroke="{INK}" stroke-width="1.2"></path>')
    txt = [axis_text(PX0 - 10, Y(t) + 4.5, fmt_int(t)) for t in ticks]
    txt.append(axis_text(PX0 - 10, top_y - 8 + 4.5, "GWh/d", "start", ' dx="16"'))
    txt += [axis_text(X(d), bot_y + 22, s, "middle") for d, s in
            [(0, "1 Aug"), (4, "5 Aug"), (43, "13 Sep"), (47, "17 Sep"), (51, "21 Sep")]]
    txt.append(axis_text(PX1, bot_y + 44, "gas day, drawn to scale", "end", ' class="ax-i"'))
    h = bot_y + 56
    aria = ("Chart of daily physical gas flow in GWh/d from entsog/physical_flows, National Gas TSO, for every gas day held "
            "locally: 1 to 5 August and 13 to 21 September 2026, with no rows between them. St. Fergus entry runs from "
            "406 to 434 in early August (350 on the 5th) and from 473 to 595 in September. Bacton (IUK) exit is about 382 "
            "to 407 in August, 0.0 from 13 to 20 September and 175.2 on 21 September.")
    svg = (f'<svg class="chart" width="{CW}" height="{h}" viewBox="0 0 {CW} {h}" role="img" aria-label="{aria}">'
           + "".join(o) + "".join(ax) + f'<g class="ax">{"".join(txt)}</g><g class="dl">{"".join(lab)}</g></svg>')
    ix = "".join([
        ix_entry(mark(CLAY, "dots"), "St. Fergus, entry", "ITP-00022", "350.3 to 594.6 GWh/d."),
        ix_entry(mark(OLIVE, "dots"), "Bacton (IUK), exit", "ITP-00005",
                 "0.0 on 13 to 20 September, 175.2 on the 21st, as reported."),
        ix_entry(mark("", "gap", hatch="G"), "No rows", "", "Nothing held locally for these 38 gas days; the lines "
                                                             "are not joined across the gap."),
    ])
    return svg, ix


# ---------------------------------------------------------------- BM units: the register, then the typed units
def chart_bmunits() -> tuple[str, str]:
    bars = {b["fuel_type"]: b["units"] for b in DATA["elexon/bmunits_reference"]["chart"]["bars"]}
    total = sum(bars.values())
    ints = [k for k in bars if k.startswith("INT")]
    rows = [("WIND", HORIZON, None), ("OTHER", KHAKI, None), ("CCGT", CLAY, None), ("OCGT", CLAY, None),
            ("NPSHYD", None, "A"), ("NUCLEAR", PETROL, None), ("PS", None, "B"), ("BIOMASS", BRONZE, None),
            ("INT*", OLIVE, None), ("COAL", None, "C")]
    val = {k: (sum(bars[i] for i in ints) if k == "INT*" else bars[k]) for k, _, _ in rows}
    pid = "bm"
    RX0, RW = 150, 734            # registry bar
    k1 = RW / total
    k8 = k1 * 8
    o = [f'<defs>{hatch_defs(pid)}</defs>']
    ry, rh = 34, 36
    nul = bars["(null)"]
    o.append(f'<rect x="{RX0}" y="{ry}" width="{f(nul * k1)}" height="{rh}" fill="{DAY}"></rect>')
    x = RX0 + nul * k1
    segs = []
    for k, fill, hat in rows:
        w = val[k] * k1
        if hat:
            segs.append(f'<rect x="{f(x)}" y="{ry}" width="{f(w)}" height="{rh}" fill="{DAY}"></rect>'
                        f'<rect x="{f(x)}" y="{ry}" width="{f(w)}" height="{rh}" fill="url(#{pid}{hat})"></rect>')
        else:
            segs.append(f'<rect x="{f(x)}" y="{ry}" width="{f(w)}" height="{rh}" fill="{fill}"></rect>')
        x += w
    o += segs
    xt = RX0 + nul * k1
    o.append(f'<rect x="{RX0}" y="{ry}" width="{RW}" height="{rh}" fill="none" stroke="{INK}" stroke-width="1.4"></rect>'
             f'<path d="M{f(xt)} {ry - 8} V{ry + rh}" stroke="{INK}" stroke-width="1.4"></path>')
    lab = [f'<text x="{RX0 + 12}" y="{ry + rh / 2 + 5}">no fuel type, 2,515</text>',
           f'<text x="{f(xt + (RX0 + RW - xt) / 2)}" y="{ry - 12}" text-anchor="middle">with a fuel type, 499</text>']
    txt = [f'<text x="{RX0 - 14}" y="{ry + rh / 2 + 5}" text-anchor="end">all 3,014</text>']
    # the typed units enlarged: leaders from the typed segment to the rows below
    y0 = ry + rh + 46
    rowh, bh = 25, 15
    o.append(f'<path d="M{f(xt)} {ry + rh} L{RX0} {y0 - 12} M{RX0 + RW} {ry + rh} L{f(RX0 + val["WIND"] * k8 + 70)} '
             f'{y0 - 12}" stroke="{INK}" stroke-width=".8" opacity=".5"></path>')
    for j, (k, fill, hat) in enumerate(rows):
        y = y0 + j * rowh
        w = val[k] * k8
        if hat:
            o.append(f'<rect x="{RX0}" y="{y}" width="{f(w)}" height="{bh}" fill="{DAY}" stroke="{INK}" '
                     f'stroke-width="1"></rect><rect x="{RX0}" y="{y}" width="{f(w)}" height="{bh}" '
                     f'fill="url(#{pid}{hat})"></rect>')
        else:
            o.append(f'<rect x="{RX0}" y="{y}" width="{f(w)}" height="{bh}" fill="{fill}"></rect>')
        txt.append(f'<text x="{RX0 - 14}" y="{y + bh - 3}" text-anchor="end" class="code">{k}</text>')
        txt.append(f'<text x="{f(RX0 + w + 8)}" y="{y + bh - 3}">{val[k]}</text>')
    o.append(f'<path d="M{RX0} {y0 - 6} V{y0 + len(rows) * rowh - 6}" stroke="{INK}" stroke-width="1.4"></path>')
    lab.append(f'<text x="{f(RX0 + 140)}" y="{y0 + 8 * rowh + bh - 3}">ten codes, 1 unit each but INTELEC (2)</text>')
    lab.append(f'<text x="{PX1}" y="{y0 + 1 * rowh + bh - 3}" text-anchor="end">the 499, at eight times the scale</text>')
    h = y0 + len(rows) * rowh + 10
    aria = ("Bar chart of BM units by fuel type in the elexon/bmunits_reference snapshot of 26 September 2026. A bar of "
            "all 3,014 units: 2,515 have no fuel type and 499 have one. The 499 are enlarged below: WIND 234, OTHER 92, "
            "CCGT 61, OCGT 22, NPSHYD 22, NUCLEAR 16, PS 16, BIOMASS 15, ten interconnector codes 11, COAL 10.")
    svg = (f'<svg class="chart" width="{CW}" height="{h}" viewBox="0 0 {CW} {h}" role="img" aria-label="{aria}">'
           + "".join(o) + f'<g class="ax">{"".join(txt)}</g><g class="dl">{"".join(lab)}</g></svg>')
    ix = "".join([
        ix_entry(mark("", "blank"), "No fuel type", "", "2,515 units, 83% of the register."),
        ix_entry(mark(HORIZON), "Palette colours", "", "Wind, gas, nuclear, interconnectors, biomass and "
                                                       "<code>OTHER</code>, as in every chart on this site."),
        ix_entry(mark("", hatch="A"), "Unpainted", "NPSHYD, PS, COAL",
                 "Codes the palette has no colour for, drawn in daylight with their own hatch."),
    ])
    return svg, ix


CHARTS = {"fuelhh": chart_fuelhh, "system_prices": chart_prices, "physical_flows": chart_flows,
          "bmunits_reference": chart_bmunits}


# ================================================================ DataFrame, schema, notebook
def df_table(key: str) -> str:
    raw = DFH[key]
    head = re.findall(r"<th>(.*?)</th>", raw.split("</thead>")[0])[1:]
    body = raw.split("<tbody>")[1]
    rows = re.findall(r"<tr>(.*?)</tr>", body, flags=re.S)
    str_cols = {"fuel_type", "gsp_group_id", "bm_unit_name", "company_name", "point_label", "operator_label"}
    out_rows = []
    for r in rows:
        idx = re.findall(r"<th>(.*?)</th>", r)[0]
        cells = re.findall(r"<td>(.*?)</td>", r)
        cells = ["None" if (c == "NaN" and head[i] in str_cols) else c for i, c in enumerate(cells)]
        out_rows.append(f"<tr><th>{idx}</th>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
    thead = "<tr><th></th>" + "".join(f"<th>{h}</th>" for h in head) + "</tr>"
    return f'<table class="df"><thead>{thead}</thead><tbody>{"".join(out_rows)}</tbody></table>'


def schema_table(spec: dict) -> str:
    rows = []
    for col, dt, mean in spec["schema"]:
        k = ' class="key"' if col in spec["keys"] else ""
        rows.append(f"<tr{k}><td><code>{col}</code></td><td>{dt}</td><td>{mean}</td></tr>")
    lc, ln = spec["lineage"]
    names = ", ".join(f"<code>{c.strip()}</code>" for c in lc.split(","))
    rows.append(f'<tr class="lin"><td>{names}</td><td>lineage</td><td>{ln}</td></tr>')
    return ('<table class="schema"><thead><tr><th>Column</th><th>Type</th><th>Meaning</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table>')


def hl(code: str) -> str:
    return re.sub(r'"[^"]*"', lambda m: f'<span class="s">{m.group(0)}</span>', code)


SETUP = ('<span class="k">from</span> gridflow_models <span class="k">import</span> setup_notebook\n'
         'data, models, common = setup_notebook()')


def notebook(spec: dict) -> str:
    cells = [f'<div class="cell"><span class="pr">[1]:</span><pre class="in">{SETUP}</pre></div>']
    for i, c in enumerate(spec["nb_cells"]):
        cells.append(f'<div class="cell"><span class="pr">[{i + 2}]:</span><pre class="in">{hl(c)}</pre></div>')
    aria = f"A notebook on the gridflow_models kernel: the setup cell, then {' and '.join(spec['nb_cells'])}"
    return (f'<figure class="nb" aria-label="{html.escape(aria, quote=True)}"><div class="nb-bar"><span class="nb-tab">'
            f'{spec["slug"]}.ipynb</span><span class="nb-kern">gridflow_models</span></div>'
            f'<div class="nb-body">{"".join(cells)}</div></figure>')


# ================================================================ page
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,200..800'
         '&amp;family=Hanken+Grotesk:ital,wght@0,400..700;1,400..600&amp;family=Red+Hat+Mono:wght@400;500'
         '&amp;display=swap" rel="stylesheet">')

CSS = (HERE / "a.css").read_text(encoding="utf-8")

STRATA = [("top", None), ("bronze", "bronze, the response as fetched"), ("silver", "silver, typed and validated"),
          ("gold", "gold, served to the notebook"), ("deep", None)]

DEFAULT_H = {"sky": 668, "top": 980, "bronze": 400, "silver": 820, "gold": 380, "deep": 560}


PATTERNS = f"""<pattern id="p-stip" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="2" cy="3" r="1" fill="#8A6F1E"></circle><circle cx="6.5" cy="7.5" r=".8" fill="#8A6F1E"></circle></pattern>
<pattern id="p-diag" width="8" height="8" patternUnits="userSpaceOnUse"><path d="M0 8 L8 0" stroke="#5E6E6B" stroke-width=".8"></path></pattern>
<pattern id="p-brick" width="24" height="12" patternUnits="userSpaceOnUse"><path d="M0 11.5 H24 M12 0 V6 M0 6 H24 M0 6 V12" stroke="#7C5530" stroke-width=".8" fill="none"></path></pattern>
<pattern id="p-soil" width="23" height="17" patternUnits="userSpaceOnUse"><circle cx="4" cy="5" r=".9" fill="{KHAKI}"></circle><circle cx="15" cy="12" r="1.1" fill="{KHAKI}"></circle><path d="M17 3 h3" stroke="{KHAKI}" stroke-width=".9"></path></pattern>
<pattern id="p-granite" width="46" height="40" patternUnits="userSpaceOnUse"><path d="M8 8 h8 M12 4 v8 M30 26 h8 M34 22 v8 M20 34 h6 M23 31 v6 M40 6 h5 M42.5 3.5 v5" stroke="{HORIZON}" stroke-width="1.1"></path></pattern>"""


def strata_svg(ys: dict[str, float], H: int) -> str:
    def band(pts: list[tuple[float, float]], fill: str, pat: str | None, op: str) -> str:
        d = smooth(pts) + f" L{W + 40} {H + 10} L-40 {H + 10} Z"
        s = f'<path d="{d}" fill="{fill}"></path>'
        if pat:
            s += f'<path d="{d}" fill="url(#{pat})" opacity="{op}"></path>'
        return s
    tb, bs, sg = wave(ys["bronze"], 7, 0.4), wave(ys["silver"], 8, 2.1), wave(ys["gold"], 7, 4.0)
    gr = [(x, ys["deep"] + 9 * math.sin(x / 140 + 1) + 6 * math.sin(x / 53 + 2) + 4 * math.sin(x / 19))
          for x in range(-40, W + 41, 20)]
    surf = [(x, prof(x)) for x in range(-40, W + 41, 20)]
    surf_d = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in surf)
    root = surf_d + " " + " ".join(f"L{f(x)} {f(y + 9)}" for x, y in reversed(surf)) + " Z"
    gr_d = smooth(gr)
    unit = []
    for key, name in STRATA:
        if name:
            unit.append(f'<text x="1360" y="{f(ys[key] + 34)}" text-anchor="end">{name}</text>')
    return (f'<svg class="layer" width="{W}" height="{H}" viewBox="0 0 {W} {H}" aria-hidden="true"><defs>{PATTERNS}'
            '</defs>' + "\n".join([
                f'<rect x="0" y="0" width="{W}" height="{SURF + 20}" fill="{PETROL}"></rect>',
                f'<path d="{surf_d} L{W + 40} {H + 10} L-40 {H + 10} Z" fill="{T_TOP}"></path>',
                f'<path d="{surf_d} L{W + 40} {H + 10} L-40 {H + 10} Z" fill="url(#p-soil)" opacity=".5"></path>',
                band(tb, T_BRONZE, "p-brick", ".15"),
                band(bs, T_SILVER, "p-diag", ".22"),
                band(sg, T_GOLD, "p-stip", ".26"),
                f'<path d="{gr_d} L{W + 40} {H + 10} L-40 {H + 10} Z" fill="{PETROL}"></path>',
                f'<path d="{gr_d} L{W + 40} {H + 10} L-40 {H + 10} Z" fill="url(#p-granite)" opacity=".5"></path>',
                f'<path d="{root}" fill="{OLIVE}"></path>',
                f'<path d="{surf_d}" stroke="{INK}" stroke-width="1.5" fill="none"></path>',
                f'<path d="{smooth(tb)} {smooth(bs)} {smooth(sg)}" stroke="{INK}" stroke-width="1.5" fill="none"></path>',
                f'<path d="{gr_d}" stroke="{INK}" stroke-width="2" fill="none" stroke-linejoin="round"></path>',
                f'<g font-family="Hanken Grotesk" font-style="italic" font-size="14" fill="{INK}">{"".join(unit)}</g>',
            ]) + "</svg>")


def feed_cable(org: tuple[float, float], ys: dict[str, float], H: int) -> str:
    """One feed, followed down: from the asset it sways into the right margin and descends. Its core is bronze to
    the bronze/silver contact, silver to the silver/gold contact, then gold; a splice sleeve marks each change.
    Taps land on the request well (bronze), the schema (silver) and the notebook (gold, where the riser ends)."""
    xs, ys0 = org
    XR = 1404
    lands = {"bronze": (1330, ys["bronze"] + 66), "silver": (1348, ys["silver"] + 77), "gold": (1334, ys["gold"] + 66)}
    g0, g1 = SURF + 14, SURF + 150
    y_end = lands["gold"][1] - 22

    def rx(y: float) -> float:
        env = math.sin(math.pi * min(1, max(0.0, (y - g1) / (y_end - 40 - g1))))
        return XR + 9 * math.sin((y - g1) / 95 + .4) * env

    pts = [(xs, ys0 - 3)]
    for y in range(int(g0), int(y_end - 40) + 1, 16):
        if y <= g1:
            t = max(0.0, min(1.0, (y - g0) / (g1 - g0)))
            t = t * t * (3 - 2 * t)
            env = math.sin(math.pi * min(1, max(0, (y - SURF - 10) / (g1 - SURF - 10))))
            pts.append((xs + (XR - xs) * t + 14 * math.sin((y - SURF) / 70) * env, y))
        else:
            pts.append((rx(y), y))
    pts.append((XR, y_end - 40))

    def cy(key: str, seed: float, amp: float) -> float:
        y0 = ys[key]
        return y0 + amp * math.sin(XR / 210 + seed) + amp * 0.45 * math.sin(XR / 73 + seed * 2.3)
    c_bs, c_sg = cy("silver", 2.1, 8), cy("gold", 4.0, 7)
    segs = [[p for p in pts if p[1] <= c_bs], [p for p in pts if c_bs <= p[1] <= c_sg], [p for p in pts if p[1] >= c_sg]]
    segs[1].insert(0, segs[0][-1])
    segs[2].insert(0, segs[1][-1])
    R = 14
    lx, ly = lands["gold"]
    out = [cable(smooth(segs[0]), BRONZE), cable(smooth(segs[1]), SILVER),
           cable(smooth(segs[2]) + f" V{f(y_end - R)} Q{XR} {f(y_end)} {XR - R} {f(y_end)} H{f(lx + R)} "
                                   f"Q{f(lx)} {f(y_end)} {f(lx)} {f(y_end + R)} V{f(ly)}", GOLD)]
    joints = []
    for key, core in (("bronze", BRONZE), ("silver", SILVER)):
        tx, ty = lands[key]
        jy = ty - 22
        jx = rx(jy)
        out.append(cable(f"M{f(jx)} {f(jy)} H{f(tx + R)} Q{f(tx)} {f(jy)} {f(tx)} {f(jy + R)} V{f(ty)}", core))
        joints.append((jx, jy))
    for c, fill in ((c_bs, SILVER), (c_sg, GOLD)):
        x = rx(c)
        out.append(f'<rect x="{f(x - 7)}" y="{f(c - 17)}" width="14" height="34" rx="7" fill="{fill}" stroke="{INK}" '
                   f'stroke-width="1.6"></rect><path d="M{f(x - 7)} {f(c - 8)} H{f(x + 7)} M{f(x - 7)} {f(c + 8)} '
                   f'H{f(x + 7)}" stroke="{INK}" stroke-width="1" opacity=".5"></path>')
    for jx, jy in joints:
        out.append(f'<circle cx="{f(jx)}" cy="{f(jy)}" r="4.6" fill="{INK}"></circle>')
    for key, tint in (("bronze", T_BRONZE), ("silver", T_SILVER), ("gold", T_GOLD)):
        tx, ty = lands[key]
        out.append(f'<circle cx="{f(tx)}" cy="{f(ty)}" r="6.5" fill="{tint}" stroke="{INK}" stroke-width="2"></circle>'
                   f'<circle cx="{f(tx)}" cy="{f(ty)}" r="2.2" fill="{INK}"></circle>')
    return (f'<svg class="layer" width="{W}" height="{H}" viewBox="0 0 {W} {H}" aria-hidden="true">'
            + "".join(out) + '</svg>')


NAV = ["Home", "Data sources", "Architecture", "Models", "About"]


def page(spec: dict) -> tuple[str, int]:
    global SURF
    hs = dict(DEFAULT_H)
    hs.update(HEIGHTS.get(spec["file"], {}))
    SURF = hs["sky"]
    ys = {"top": SURF}
    acc = SURF
    for k in ("top", "bronze", "silver", "gold"):
        acc += hs[k]
        nxt = {"top": "bronze", "bronze": "silver", "silver": "gold", "gold": "deep"}[k]
        ys[nxt] = acc
    H = acc + hs["deep"]

    land_svg, land_lab, org = scene(spec)
    land = (f'<svg class="layer land" width="{W}" height="{SURF + 12}" viewBox="0 0 {W} {SURF + 12}" role="img" '
            f'aria-label="{html.escape(LAND_ARIA[spec["slug"]], quote=True)}">\n{land_svg}\n<g class="land-l">'
            f'{land_lab}</g>\n</svg>')
    cab = feed_cable(org, ys, H)

    cur = ' aria-current="page"'
    nav = "".join(f'<li><a href="#"{cur if n == "Data sources" else ""}>{n}</a></li>' for n in NAV)
    facts = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in spec["facts"])
    sky = (f'<section class="sky" aria-labelledby="ds-h" style="height: {hs["sky"]}px">'
           f'<header class="mast"><a class="brand" href="#">gridflow</a><nav aria-label="Primary"><ul>{nav}</ul></nav>'
           f'</header>'
           f'<div class="hero"><div class="hero-l">'
           f'<nav class="crumb" aria-label="Breadcrumb"><a href="#">Data sources</a> / <a href="#">{spec["vendor"]}</a>'
           f'</nav><h1 id="ds-h">{spec["title"]}</h1>'
           f'<p class="ident"><code class="chip">{spec["key"]}</code><span>{spec["code"]}</span></p></div>'
           f'<div class="hero-r"><p class="one">{spec["oneliner"]}</p><dl class="facts">{facts}</dl></div></div>'
           f'</section>')

    svg, ix = CHARTS[spec["slug"]]()
    uses = "".join(f"<li>{u}</li>" for u in spec["uses"])
    top = (f'<section class="st st-top" aria-labelledby="fig-h" style="height: {hs["top"]}px"><div class="inner">'
           f'<div class="fig-h"><h2 id="fig-h">{spec["chart_h2"]}</h2><p class="cap">{spec["chart_cap"]}</p></div>'
           f'<div class="fig"><div class="fig-l">{svg}</div>'
           f'<ul class="ix" aria-label="Key to the chart">{ix}</ul></div>'
           f'<div class="about"><div class="what"><h3>What it is</h3><p>{spec["what"]}</p></div>'
           f'<div class="how"><h3>How it’s used</h3><ul>{uses}</ul></div></div>'
           f'</div></section>')

    ep = "\n".join(spec["endpoint"])
    cli = "\n".join(f'{c}  <span class="cm"># {m}</span>' for c, m in spec["cli"])
    bronze = (f'<section class="st st-bronze" aria-labelledby="br-h" style="height: {hs["bronze"]}px"><div class="inner">'
              f'<div class="split"><div class="lead"><h2 id="br-h">The raw feed</h2><p>{spec["bronze_note"]}</p></div>'
              f'<div class="wells"><pre class="in-w">{ep}</pre>'
              f'<pre class="in-w">{cli}</pre></div></div></div></section>')

    silver = (f'<section class="st st-silver" aria-labelledby="sv-h" style="height: {hs["silver"]}px"><div class="inner">'
              f'<div class="split"><div class="lead"><h2 id="sv-h">Schema and sample rows</h2>'
              f'<p>Relation <code>{spec["relation"]}</code>, typed by <code>{spec["schema_cls"]}</code> in '
              f'<code>{spec["schema_src"]}</code>; transformer version {spec["version"]}.</p>'
              f'<p class="kn">A square marks the columns that identify a row.</p></div>'
              f'<div class="sch">{schema_table(spec)}</div></div>'
              f'<div class="sample"><p class="dfc">{spec["df_cap"]}</p><div class="dfw">{df_table(spec["df"])}</div></div>'
              f'</div></section>')

    gold = (f'<section class="st st-gold" aria-labelledby="gd-h" style="height: {hs["gold"]}px"><div class="inner">'
            f'<div class="split"><div class="lead"><h2 id="gd-h">Query it from a notebook</h2>'
            f'<p>{spec["gold_note"]}</p></div>{notebook(spec)}</div></div></section>')

    cav = "".join(f"<li><strong>{a}</strong> {b}</li>" for a, b in spec["caveats"])
    rel = "".join(f'<li><a href="#"><code>{k}</code></a><p>{b}</p></li>' for k, b in spec["related"])
    foot_nav = "".join(f'<li><a href="#">{n}</a></li>' for n in ["Data sources", "Architecture", "Models", "About",
                                                                    "GitHub"])
    deep = (f'<section class="st st-deep" aria-label="Caveats and related datasets" style="height: {hs["deep"]}px">'
            f'<div class="inner"><div class="deep-g"><div class="cav"><h2>What to watch for</h2><ul>{cav}</ul></div>'
            f'<div class="rel"><h2>Related datasets</h2><ul>{rel}</ul></div></div>'
            f'<footer class="foot"><a class="brand" href="#">gridflow</a><ul>{foot_nav}</ul>'
            f'<p>MIT licence</p></footer></div></section>')

    body = "\n".join([strata_svg(ys, H), land, cab, "<main>", sky, top, bronze, silver, gold, deep, "</main>"])
    out = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{spec["title"]}</title>
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
{body}
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
    return out, H


LAND_ARIA = {
    "fuelhh": ("Drawing of the generation this data comes from: onshore wind on a ridge, a gas-fired power station, "
               "pylons into a substation, an interconnector converter station on the coast and offshore wind at sea. A "
               "cable runs from the substation down to the vendor feed."),
    "system_prices": ("Drawing of the transmission system these prices balance: pylons running into a substation, with "
                      "battery storage beside it and wind turbines on the ridge. A cable runs from the substation down "
                      "to the vendor feed."),
    "physical_flows": ("Drawing of gas coming ashore: an offshore platform, a pipeline landfall, a gas terminal and a "
                       "gas-fired power station inland. A cable runs from the terminal down to the vendor feed."),
    "bmunits_reference": ("Drawing of registered units of different kinds side by side: onshore wind, a gas-fired power "
                          "station, battery storage, a substation and an interconnector converter station. A cable runs "
                          "from the substation down to the vendor feed."),
}


def static(dc: str) -> str:
    s = dc.replace('<script src="./support.js"></script>', "")
    s = re.sub(r"</?x-dc>", "", s)
    s = re.sub(r"</?helmet>", "", s)
    s = re.sub(r"<script type=\"text/x-dc\".*?</script>\n", "", s, flags=re.S)
    return s


if __name__ == "__main__":
    only = sys.argv[1:] or None
    (HERE / "static").mkdir(exist_ok=True)
    for spec in SPECIMENS:
        if only and spec["file"] not in only:
            continue
        out, H = page(spec)
        body_only = out.split('<script type="text/x-dc"')[0]
        assert "{{" not in body_only and "}}" not in body_only, "template-hole syntax in markup"
        assert "/>" not in re.sub(r"<(meta|link|br)[^>]*>", "", body_only), "self-closing tag"
        assert "#A9C7C4" not in out.upper(), "banned colour"
        (HERE / f"{spec['file']}.dc.html").write_text(out, encoding="utf-8")
        (HERE / "static" / f"{spec['file']}.html").write_text(static(out), encoding="utf-8")
        print(spec["file"], "H =", H)
