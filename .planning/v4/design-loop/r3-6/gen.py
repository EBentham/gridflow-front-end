"""Round 3 v3: "Above ground, below ground". Emits R3-v3-{A,B,C}.dc.html (identical but for the workbench section) + static copies."""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

HERE = Path(__file__).parent
REPO = Path(r"C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end")
SERIES = json.loads((REPO / "site/hifi/data/chart-series.json").read_text(encoding="utf-8"))["series"]

PETROL, HORIZON, CHART, OLIVE = "#155A6E", "#3E8C97", "#AFC64E", "#66793B"
INK, DAY, CLAY, KHAKI, MUTED, RULE = "#1C2B22", "#F6F4EC", "#C77E3C", "#A39A6A", "#5d6a55", "#DFDACA"
BRONZE, SILVER, GOLD = "#A5713C", "#9FADAB", "#C2A14A"
T_GOLD, T_SILVER, T_BRONZE, T_TOP = "#E9DDAF", "#DCE2DF", "#E2CDB3", "#ECE8DA"
SOFT = "#3F4A3B"  # secondary text on light strata (contrast >= 7:1 on every tint)

W = 1440

# ---------------------------------------------------------------- the y table
Y: dict[str, int] = {}
Y["surf"] = 940            # ground surface (the cut)
Y["core"] = 984            # FUELHH block top
# v2: the research section sits in the topsoil, one layer above the warehouse, under the core sample
Y["bedP"] = 1352           # bedding line between the core sample and the research section
Y["p_head"] = Y["bedP"] + 62
P_HEAD_H = 276             # heading row height (measured, see report)
Y["tree"] = Y["p_head"] + P_HEAD_H
TREE_H = 640               # model entries (measured)
Y["tray"] = Y["tree"] + TREE_H + 20   # the cables' first horizontal run under the tree
Y["c_tb"] = Y["tray"] + 45 + 70       # topsoil / bronze contact
Y["b_head"] = Y["c_tb"] + 50
Y["lane"] = Y["c_tb"] + 244  # where the substation cable turns into its lane
Y["r1"] = Y["lane"] + 70
ENTRY_H = 262
Y["r2"] = Y["r1"] + ENTRY_H + 40
Y["c_bs"] = Y["r2"] + ENTRY_H + 34   # bronze / silver
Y["s_head"] = Y["c_bs"] + 58
Y["c_sg"] = Y["c_bs"] + 420          # silver / gold
Y["splice"] = Y["c_sg"] + 78
Y["views"] = Y["c_sg"] + 170
Y["bed1"] = Y["c_sg"] + 262
Y["q_head"] = Y["bed1"] + 58
# v3: the workbench section (the one part that differs between A, B and C) gets one shared band
# height, so every file is byte-identical outside that section
WB_H = 1046   # v4: +216 for the df.head() cell (keeps the 100 px gap above the gold/base contact)
Y["c_gr"] = Y["q_head"] + WB_H       # gold / base unconformity
Y["about"] = Y["c_gr"] + 96
H = Y["about"] + 660


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


def prof(x: float) -> float:
    """The ground surface (topographic profile of the cut)."""
    return Y["surf"] + 4 * math.sin(x / 190 + 0.6) - 2.5 * math.sin(x / 83 + 1.3)


def wave(y0: float, amp: float, seed: float, step: int = 120) -> list[tuple[float, float]]:
    return [(x, y0 + amp * math.sin(x / 210 + seed) + amp * 0.45 * math.sin(x / 73 + seed * 2.3))
            for x in range(-40, W + step + 41, step)]  # v2: run past the right edge (bands stopped at x 1400)


# ================================================================ landscape
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


def solar_farm() -> str:
    parts = []
    # the plot: a fenced patch of deep land
    plot = [(64, prof(64) - 60), (398, prof(398) - 64), (414, prof(414)), (52, prof(52))]
    parts.append(f'<path d="M{f(plot[0][0])} {f(plot[0][1])} L{f(plot[1][0])} {f(plot[1][1])} '
                 f'L{f(plot[2][0])} {f(plot[2][1])} L{f(plot[3][0])} {f(plot[3][1])} Z" fill="{OLIVE}"></path>')
    rows = [(0.46, 58), (0.58, 45), (0.71, 32), (0.85, 18), (1.0, 4)]
    for s, up in rows:
        x0, x1 = 78 + (1 - s) * 30, 392 - (1 - s) * 20
        base = prof((x0 + x1) / 2) - up
        h, lean, fh = 10 * s, 6 * s, 4.2 * s
        yf, yb = base - fh, base - fh - h
        legs = " ".join(f"M{f(xl)} {f(base)} V{f(yf)}" for xl in _frange(x0 + 6, x1, 30 * s))
        parts.append(f'<path d="{legs}" stroke="{INK}" stroke-width=".9"></path>')
        parts.append(f'<path d="M{f(x0)} {f(yf)} L{f(x1)} {f(yf)} L{f(x1 - lean)} {f(yb)} L{f(x0 - lean)} {f(yb)} Z" '
                     f'fill="{CHART}" stroke="{INK}" stroke-width=".9" stroke-linejoin="round"></path>')
        cells = " ".join(f"M{f(xc)} {f(yf)} L{f(xc - lean)} {f(yb)}" for xc in _frange(x0 + 9 * s, x1 - 2, 9 * s))
        parts.append(f'<path d="{cells} M{f(x0 - lean / 2)} {f((yf + yb) / 2)} H{f(x1 - lean / 2)}" '
                     f'stroke="{INK}" stroke-width=".55" opacity=".4"></path>')
    fence = " ".join(f"M{f(xp)} {f(prof(xp) + 0.5)} v-9" for xp in _frange(58, 412, 16))
    parts.append(f'<path d="{fence} M52 {f(prof(52) - 6)} L414 {f(prof(414) - 6)}" stroke="{INK}" '
                 f'stroke-width=".7" opacity=".7"></path>')
    return "\n".join(parts)


def _frange(a: float, b: float, step: float) -> list[float]:
    out, v = [], a
    while v <= b + 1e-6:
        out.append(v)
        v += step
    return out


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


def datacentre(x: float, base: float) -> str:
    fins = " ".join(f"M{f(xi)} {f(base - 34)} V{f(base - 5)}" for xi in _frange(x + 34, x + 166, 6))
    units = "".join(
        f'<rect x="{f(x + 12 + 22 * k)}" y="{f(base - 48)}" width="16" height="8" fill="{MUTED}"></rect>'
        f'<circle cx="{f(x + 16 + 22 * k)}" cy="{f(base - 44)}" r="2.2" fill="{INK}" opacity=".55"></circle>'
        f'<circle cx="{f(x + 24 + 22 * k)}" cy="{f(base - 44)}" r="2.2" fill="{INK}" opacity=".55"></circle>'
        for k in range(7))
    gens = "".join(
        f'<rect x="{f(x + 180 + 13 * k)}" y="{f(base - 12)}" width="11" height="12" fill="{KHAKI}" stroke="{INK}" '
        f'stroke-width=".7"></rect><path d="M{f(x + 188 + 13 * k)} {f(base - 12)} v-6" stroke="{INK}" stroke-width="1"></path>'
        for k in range(2))
    return "\n".join([
        f'<rect x="{f(x + 30)}" y="{f(base - 56)}" width="146" height="20" fill="{RULE}" stroke="{INK}" stroke-width=".9"></rect>',
        f'<path d="{" ".join(f"M{f(xi)} {f(base - 53)} V{f(base - 41)}" for xi in _frange(x + 36, x + 172, 6))}" '
        f'stroke="{INK}" stroke-width=".6" opacity=".3"></path>',
        units,
        f'<rect x="{f(x)}" y="{f(base - 40)}" width="172" height="40" fill="{DAY}" stroke="{INK}" stroke-width="1.1"></rect>',
        f'<path d="{fins}" stroke="{INK}" stroke-width=".7" opacity=".28"></path>',
        f'<rect x="{f(x + 8)}" y="{f(base - 20)}" width="18" height="20" fill="{INK}" opacity=".82"></rect>',
        f'<path d="M{f(x)} {f(base - 40)} H{f(x + 172)}" stroke="{INK}" stroke-width="2.2"></path>',
        gens,
    ])


def battery(x: float, base: float) -> str:
    out = []
    for row, (dy, h, off) in enumerate([(19, 9, 5), (10, 10, 0)]):
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


def metmast(x: float, base: float, h: float = 156) -> str:
    zig = [(x - 3.6 + 2.4 * (k * 9 / h), base - k * 9) for k in range(int(h / 9) + 1)]
    zz = " ".join(f"L{f(x + (2.4 if k % 2 else -2.4) * (1 - k * 9 / h * .6))} {f(base - k * 9)}" for k in range(1, int(h / 9) + 1))
    top = base - h
    booms = []
    for frac in (0.58, 0.8, 1.0):
        by = base - h * frac
        booms.append(f"M{f(x)} {f(by)} H{f(x + 16)} M{f(x)} {f(by)} H{f(x - 12)}")
    cups = "".join(f'<circle cx="{f(x + 16 + dx)}" cy="{f(base - h * fr - 2)}" r="1.5" fill="{INK}"></circle>'
                   for fr in (0.58, 0.8, 1.0) for dx in (-2.2, 2.2))
    guys = (f"M{f(x)} {f(base - h * .62)} L{f(x - 30)} {f(prof(x - 30))} M{f(x)} {f(base - h * .62)} L{f(x + 28)} "
            f"{f(prof(x + 28))} M{f(x)} {f(base - h * .92)} L{f(x - 44)} {f(prof(x - 44))}")
    return "\n".join([
        f'<path d="{guys}" stroke="{INK}" stroke-width=".6" opacity=".55"></path>',
        f'<path d="M{f(x - 3.6)} {f(base)} L{f(x - 1.2)} {f(top)} M{f(x + 3.6)} {f(base)} L{f(x + 1.2)} {f(top)} '
        f'M{f(zig[0][0])} {f(base)} {zz}" stroke="{INK}" stroke-width=".9" fill="none"></path>',
        f'<path d="{" ".join(booms)} M{f(x)} {f(top)} V{f(top - 10)} M{f(x)} {f(top - 8)} L{f(x - 9)} {f(top - 6)}" '
        f'stroke="{INK}" stroke-width="1.1"></path>',
        cups,
    ])


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


def landscape() -> str:
    S = Y["surf"]
    parts: list[str] = []
    # distant sea (lighter than the ridges), offshore wind on it
    parts.append(f'<rect x="820" y="786" width="620" height="80" fill="{HORIZON}"></rect>')
    parts.append(f'<rect x="820" y="786" width="620" height="80" fill="{DAY}" opacity=".13"></rect>')
    waves = " ".join(f"M{f(x0)} {f(y0)} h{f(ln)}" for x0, y0, ln in
                     [(960, 796, 40), (1060, 800, 26), (1200, 794, 34), (1330, 799, 44), (1010, 808, 22),
                      (1150, 812, 30), (1270, 806, 18), (1390, 812, 28)])
    parts.append(f'<path d="{waves}" stroke="{DAY}" stroke-width="1" opacity=".35"></path>')
    # the far coast: the other end of the interconnector
    parts.append(f'<path d="M1150 786 C1210 781 1250 778 1300 778 S1390 775 1440 776 V786 Z" fill="{HORIZON}" '
                 f'opacity=".6"></path>')
    for i, (ox, oh) in enumerate([(1090, 30), (1160, 34), (1238, 31), (1312, 36), (1392, 32)]):
        parts.append(turbine(ox, 804 + (i % 2) * 3, oh, oh * .5, ["sp1", "sp2", "sp3"][i % 3], 17 * i))
    # far ridge, then the near ridge with onshore wind
    far = [(-20, 716), (120, 688), (300, 700), (470, 668), (640, 686), (790, 712), (880, 760), (940, 800)]
    parts.append(f'<path d="{smooth(far)} L940 880 L-20 880 Z" fill="{HORIZON}" opacity=".5"></path>')
    near = [(-20, 748), (90, 716), (210, 704), (330, 722), (452, 698), (590, 710), (720, 732), (820, 770), (900, 806)]
    parts.append(f'<path d="{smooth(near)} L900 880 L-20 880 Z" fill="{HORIZON}"></path>')
    for i, (tx, ty) in enumerate(near[1:7]):
        hgt = [76, 84, 72, 88, 80, 70][i]
        parts.append(turbine(tx, ty + 3, hgt, hgt * .5, ["sp2", "sp1", "sp3"][i % 3], 40 * i + 10))
    # the energised land
    field = [(-20, 802), (160, 792), (340, 804), (520, 796), (700, 808), (880, 818), (1060, 834), (1240, 840), (1460, 846)]
    bottom = " ".join(f"L{f(x)} {f(prof(x))}" for x in range(1460, -21, -20))
    parts.append(f'<path d="{smooth(field)} {bottom} Z" fill="{CHART}"></path>')
    bounds = [smooth([(-20, 822), (300, 818), (700, 830), (1100, 850), (1460, 858)]),
              smooth([(-20, 852), (400, 848), (820, 862), (1200, 876), (1460, 880)]),
              smooth([(420, 890), (800, 896), (1180, 904), (1460, 906)])]
    parts.append(f'<path d="{" ".join(bounds)}" stroke="{OLIVE}" stroke-width="1" fill="none" opacity=".45"></path>')
    # mid-distance: gas-fired station and the pylon line
    parts.append(ccgt(262, 842, 0.82))
    p1, p2, p3 = (150, 836, 0.5), (430, 848, 0.58), (700, 862, 0.66)
    sub_x, sub_s = 866, 1.28
    sub_base = prof(sub_x + 50)
    sub_svg, sub_ends = substation(sub_x, sub_base)
    sub_svg = sc(sub_svg, sub_x, sub_base, sub_s)
    sub_ends = [(sub_x + (ex - sub_x) * sub_s, sub_base + (ey - sub_base) * sub_s) for ex, ey in sub_ends]
    wires = [
        spans([(-20, 788), (-20, 774), (-20, 764)], tips(*p1, -1), 6),
        spans(tips(*p1, 1), tips(*p2, -1), 12), spans(tips(*p2, 1), tips(*p3, -1), 13),
        spans(tips(*p3, 1), sub_ends, 10),
    ]
    parts.append(f'<g stroke="{INK}" fill="none" stroke-linecap="round" stroke-width="1.35">'
                 f'{pylon(*p1)}{pylon(*p2)}{pylon(*p3)}</g>')
    parts.append(f'<path d="{" ".join(wires)}" stroke="{INK}" stroke-width=".8" fill="none" opacity=".85"></path>')
    # foreground, on the cut
    parts.append(solar_farm())
    parts.append(sc(datacentre(434, prof(560)), 434, prof(560), 1.22))
    parts.append(sc(battery(706, prof(770)), 706, prof(770), 1.22))
    parts.append(sub_svg)
    parts.append(metmast(1018, prof(1018), 170))
    parts.append(sc(converter(1082, prof(1150)), 1082, prof(1150), 1.26))
    parts.append(sc(gasterminal(1240, prof(1310)), 1240, prof(1310), 1.32))
    return "\n".join(parts)


def sc(svg: str, x: float, base: float, s: float) -> str:
    return f'<g transform="translate({f(x)} {f(base)}) scale({s}) translate({f(-x)} {f(-base)})">{svg}</g>'


LAND_LABELS = [
    # text, x, y, fill, anchor
    ("onshore wind", 150, 752, "#E4EFEC", "middle"),
    ("offshore wind", 1330, 740, "#E4EFEC", "middle"),
    ("gas-fired power station", 300, 718, "#E4EFEC", "middle"),
    ("solar farm", 232, 864, INK, "middle"),
    ("data centre", 560, 858, INK, "middle"),
    ("battery storage", 776, 900, INK, "middle"),
    ("substation", 930, 858, INK, "middle"),
    ("met mast", 1004, 774, "#E4EFEC", "end"),
    ("interconnector", 1156, 836, INK, "middle"),
    ("converter station", 1156, 851, INK, "middle"),
    ("gas terminal", 1318, 872, INK, "middle"),
]


def land_labels() -> str:
    return "\n".join(f'<text x="{x}" y="{y}" fill="{c}" text-anchor="{a}">{t}</text>' for t, x, y, c, a in LAND_LABELS)


# ================================================================ core sample
FUELS = [("Wind", 6408.2, 29, HORIZON), ("CCGT", 5639.3, 26, CLAY), ("Nuclear", 3589.4, 16, PETROL),
         ("Imports", 3174.4, 14, OLIVE), ("Biomass", 2350.2, 11, CHART), ("Other", 929.2, 4, KHAKI)]
CORE_LEN = 660
TOTAL = sum(v for _, v, _, _ in FUELS)


def core_svg() -> str:
    k = CORE_LEN / (TOTAL / 1000)  # px per GW
    x0, top, hgt = 16, 104, 76
    bot = top + hgt
    xs = []
    acc = x0
    for name, mw, pct, col in FUELS:
        w = mw / 1000 * k
        xs.append((name, mw, pct, col, acc, w))
        acc += w
    end = acc
    tier = {"Wind": 1, "CCGT": 2, "Nuclear": 1, "Imports": 2, "Biomass": 1}
    out = ['<defs>',
           '<clipPath id="coreclip"><path d="' + core_outline(x0, end, top, bot) + '"></path></clipPath>',
           f'<pattern id="c-wind" width="14" height="6" patternUnits="userSpaceOnUse"><path d="M0 3 h8" stroke="{DAY}" '
           f'stroke-width=".8"></path></pattern>',
           f'<pattern id="c-gas" width="7" height="7" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r=".9" '
           f'fill="{INK}"></circle><circle cx="5.5" cy="5.5" r=".7" fill="{INK}"></circle></pattern>',
           f'<pattern id="c-imp" width="7" height="7" patternUnits="userSpaceOnUse"><path d="M0 7 L7 0" stroke="{DAY}" '
           f'stroke-width=".8"></path></pattern>',
           f'<pattern id="c-bio" width="10" height="8" patternUnits="userSpaceOnUse"><path d="M1 2 l3 1 M6 6 l3 -1" '
           f'stroke="{INK}" stroke-width=".8"></path></pattern>',
           '</defs>', '<g clip-path="url(#coreclip)">']
    pat = {"Wind": ("c-wind", ".45"), "CCGT": ("c-gas", ".22"), "Imports": ("c-imp", ".3"), "Biomass": ("c-bio", ".3")}
    for name, mw, pct, col, sx, w in xs:
        out.append(f'<rect x="{f(sx)}" y="{top}" width="{f(w + .5)}" height="{hgt}" fill="{col}"></rect>')
        if name in pat:
            out.append(f'<rect x="{f(sx)}" y="{top}" width="{f(w + .5)}" height="{hgt}" fill="url(#{pat[name][0]})" '
                       f'opacity="{pat[name][1]}"></rect>')
    out.append(f'<rect x="0" y="{top + 7}" width="{f(end + 20)}" height="7" fill="#FFFFFF" opacity=".2"></rect>')
    out.append(f'<rect x="0" y="{bot - 15}" width="{f(end + 20)}" height="15" fill="#000000" opacity=".13"></rect>')
    out.append('</g>')
    # fracture lines at each contact
    fr = []
    for i, (_, _, _, _, sx, _) in enumerate(xs[1:]):
        j = [5, -6, 6, -5, 4, -6] if i % 2 else [-6, 5, -5, 6, -4, 5]
        pts = [(sx, top)] + [(sx + j[n], top + 11 + n * 11) for n in range(6)] + [(sx, bot)]
        fr.append("M" + " L".join(f"{f(a)} {f(b)}" for a, b in pts))
    out.append(f'<path d="{" ".join(fr)}" stroke="{T_TOP}" stroke-width="2.4" fill="none" stroke-linejoin="round"></path>')
    out.append(f'<path d="{core_outline(x0, end, top, bot)}" fill="none" stroke="{INK}" stroke-width="1.2"></path>')
    # the drilled face at the left end
    out.append(f'<ellipse cx="{x0}" cy="{(top + bot) / 2}" rx="11" ry="{hgt / 2}" fill="#8FC0C6" stroke="{INK}" '
               f'stroke-width="1.2"></ellipse>')
    out.append(f'<ellipse cx="{x0}" cy="{(top + bot) / 2}" rx="6" ry="{hgt / 2 - 12}" fill="none" stroke="{INK}" '
               f'stroke-width=".7" opacity=".45"></ellipse>')
    # labels, two tiers, leaders
    lab = ['<g font-family="Hanken Grotesk" font-size="14.5" fill="#1C2B22">']
    leaders = []
    for name, mw, pct, col, sx, w in xs:
        if name == "Other":
            lx, ly = end + 16, (top + bot) / 2 - 4
            lab.append(f'<text x="{f(lx)}" y="{f(ly)}" font-weight="600">Other</text>'
                       f'<text x="{f(lx)}" y="{f(ly + 19)}">{mw / 1000:.1f} GW, {pct}%</text>')
            continue
        t = tier[name]
        ny = 20 if t == 1 else 64
        lx = sx + 4
        lab.append(f'<text x="{f(lx)}" y="{ny}" font-weight="600">{name}</text>'
                   f'<text x="{f(lx)}" y="{ny + 19}">{mw / 1000:.1f} GW, {pct}%</text>')
        leaders.append(f"M{f(sx + 1)} {ny + 26} V{top - 2}")
    lab.append('</g>')
    out.append(f'<path d="{" ".join(leaders)}" stroke="{INK}" stroke-width="1" opacity=".55"></path>')
    out += lab
    # scale in GW
    ay = bot + 20
    ticks = " ".join(f"M{f(x0 + g * k)} {ay - 4} V{ay + 4}" for g in range(0, 25, 5) if x0 + g * k <= end + .5)
    small = " ".join(f"M{f(x0 + g * k)} {ay - 2} V{ay + 2}" for g in range(0, 23) if g % 5)
    out.append(f'<path d="M{x0} {ay} H{f(end)} {ticks} {small}" stroke="{INK}" stroke-width="1"></path>')
    tl = ""
    for g in range(0, 25, 5):
        if x0 + g * k <= end + .5:
            lbl = "20 GW" if g == 20 else str(g)
            anc = 'text-anchor="start" dx="-5"' if g == 20 else 'text-anchor="middle"'
            tl += f'<text x="{f(x0 + g * k)}" y="{ay + 20}" {anc}>{lbl}</text>'
    out.append(f'<g font-family="Hanken Grotesk" font-size="13" fill="{SOFT}">{tl}</g>')
    width = int(end + 120)
    height = ay + 28
    aria = ("Core sample of Great Britain's mean generation by fuel, 1 to 5 August 2026, drawn to a gigawatt scale: "
            "wind 6.4 GW (29%), CCGT 5.6 GW (26%), nuclear 3.6 GW (16%), imports 3.2 GW (14%), biomass 2.4 GW (11%), "
            "other 0.9 GW (4%); 22.1 GW in all.")
    return (f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{aria}">'
            + "\n".join(out) + "</svg>")


def core_outline(x0: float, end: float, top: float, bot: float) -> str:
    # left end: half of the drilled ellipse; right end: a broken, irregular face
    brk = [(end, top), (end + 7, top + 12), (end + 1, top + 26), (end + 9, top + 40), (end + 3, top + 55),
           (end + 8, top + 66), (end + 2, bot)]
    return (f"M{x0} {top} " + " ".join(f"L{f(a)} {f(b)}" for a, b in brk) +
            f" L{x0} {bot} A11 {f((bot - top) / 2)} 0 0 1 {x0} {top} Z")


# ================================================================ sparklines
def spark(key: str, w: int = 280, h: int = 52, zero: bool = False) -> str:
    vals = SERIES[key]["values"]
    mn, mx = min(vals), max(vals)
    if zero:
        mn = min(mn, 0)
    pad = 4
    n = len(vals)

    def px(i: int) -> float:
        return pad + i * (w - 2 * pad) / (n - 1)

    def py(v: float) -> float:
        return pad + (mx - v) * (h - 2 * pad) / (mx - mn)

    pts = [(px(i), py(v)) for i, v in enumerate(vals)]
    d = "M" + " L".join(f"{p[0]:.1f} {p[1]:.1f}" for p in pts)
    out = []
    if zero and min(vals) < 0:
        zy = py(0)
        # shade the stretches below zero in clay
        neg = []
        run: list[tuple[float, float]] = []
        for (x, y), v in zip(pts, vals):
            if v < 0:
                run.append((x, y))
            elif run:
                neg.append(run)
                run = []
        if run:
            neg.append(run)
        for r in neg:
            xa, xb = r[0][0] - 1.2, r[-1][0] + 1.2
            poly = f"M{xa:.1f} {zy:.1f} " + " ".join(f"L{x:.1f} {y:.1f}" for x, y in r) + f" L{xb:.1f} {zy:.1f} Z"
            out.append(f'<path d="{poly}" fill="{CLAY}"></path>')
        out.append(f'<path d="M0 {zy:.1f} H{w}" stroke="{INK}" stroke-width=".8" stroke-dasharray="3 3" opacity=".6"></path>')
    out.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"></path>')
    if n <= 6:
        out.append("".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="{INK}"></circle>' for x, y in pts))
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" aria-hidden="true">' + "".join(out) + "</svg>"


# ================================================================ vendors
ROW1_X = [80, 400, 720, 1040]
ROW2_X = [364, 684, 1004]
VENDORS = {
    # key: (name, desc, meta, series, code, caption, row, slot, file, zero)
    "elexon": ("Elexon BMRS", "GB electricity: prices, generation, demand, balancing", "33 datasets, every 5 minutes",
               "elexon/system_prices", "system_prices", "system sell price, £/MWh, −39 to 179", 1, 0,
               "elexon/fuelhh.json", True),
    "neso": ("NESO", "GB grid carbon intensity", "33 datasets, every 30 minutes",
             "neso/carbon_intensity", "carbon_intensity", "forecast intensity, gCO₂/kWh, 35 to 179", 2, 0, None, False),
    "nesodp": ("NESO Data Portal", "CKAN file catalogue: wind availability, embedded forecasts, generation mix from 2009",
               "3 datasets, every 30 minutes", "neso_data_portal/historic_generation_mix", "historic_generation_mix",
               "gas share, %, Jan 2009 to Aug 2026", 1, 1, None, False),
    "openmeteo": ("Open-Meteo", "Weather: temperature, wind, radiation", "6 datasets, hourly",
                  "openmeteo/historical_wind", "historical_wind", "wind speed at 10 m, m/s, 2.9 to 8.9", 2, 1,
                  "openmeteo/weather.json", False),
    "entsoe": ("ENTSO-E", "European electricity transparency platform", "49 datasets, every 15 minutes",
               "entsoe/day_ahead_prices", "day_ahead_prices", "day-ahead price, €/MWh, 0 to 198", 1, 2,
               "entsoe/da_prices.xml", False),
    "entsog": ("ENTSO-G", "European gas transmission flows at interconnection points", "33 datasets, daily",
               "entsog/physical_flows", "physical_flows", "physical flow, GWh a day, 36.9 to 39.7", 2, 2, None, False),
    "gie": ("GIE AGSI and ALSI", "EU gas storage levels and LNG terminal send-out", "8 datasets, daily",
            "gie/storage", "storage", "gas in storage, GWh, 64.4 to 65.5", 1, 3, "gie/agsi.json", False),
}
DOM_ORDER = ["elexon", "entsoe", "entsog", "gie", "openmeteo", "neso", "nesodp"]


def vendor_pos(key: str) -> tuple[int, int, float]:
    v = VENDORS[key]
    row, slot = v[6], v[7]
    if row == 1:
        x = ROW1_X[slot]
        return x, Y["r1"], x + 16
    x = ROW2_X[slot]
    return x, Y["r2"], x + 16


def vendor_block(key: str) -> str:
    name, desc, meta, series, code, cap, row, slot, file, zero = VENDORS[key]
    x, top, land = vendor_pos(key)
    pad = land - x + 14
    fl = (f'<p class="land" style="padding-left: {f(pad)}px"><code>{file}</code></p>' if file
          else '<p class="land" aria-hidden="true"></p>')
    return (f'<article class="blk vend" style="top: {top}px; left: {x}px; width: 280px">{fl}'
            f'<h3><a href="#">{name}</a></h3><p class="vd">{desc}</p><p class="vm">{meta}</p>'
            f'{spark(series, zero=zero)}<p class="sc"><code>{code}</code><br>{cap}</p></article>')


# ================================================================ cables
def cable(d: str, core: str = BRONZE, sheath: float = 4.4, corew: float = 1.5) -> str:
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{sheath}" stroke-linecap="round" '
            f'stroke-linejoin="round"></path>'
            f'<path d="{d}" fill="none" stroke="{core}" stroke-width="{corew}" stroke-linecap="round" '
            f'stroke-linejoin="round"></path>')


def smoothstep(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


RISER = [1340, 1355, 1370, 1385]   # the four feeds pass the research section down the right margin
TRAY_DY = 15


def feed_cables() -> str:
    S = Y["surf"]
    y1 = Y["lane"]
    srcs = [890, 1018, 1124, 1314]
    ends = [664, 700, 736, 1020]
    out = []
    joints = []
    # 1. gather: from the assets, swaying down beside the core sample towards the right margin
    g0, g1 = S + 50, Y["bedP"] + 10
    # 2. riser: buried, not ducted, so it keeps a slow low-amplitude sway (never a straight column)
    r_end = Y["tray"] - 30
    paths = []
    for i, (xs, xr) in enumerate(zip(srcs, RISER)):
        pts = [(xs, prof(xs) - 3)]
        for y in range(int(S + 30), int(r_end) + 1, 22):
            if y <= g1:
                t = smoothstep((y - g0) / (g1 - g0))
                env = math.sin(math.pi * min(1, max(0, (y - S - 20) / (g1 - S - 20))))
                sway = 16 * math.sin((y - S) / 70) * env
                pts.append((xs + (xr - xs) * t + sway, y))
            else:
                env = math.sin(math.pi * min(1, (y - g1) / (r_end - g1)))
                sway = 9 * math.sin((y - g1) / 95 + 0.4) * env
                pts.append((xr + sway, y))
        pts[-1] = (xr, r_end)
        paths.append(pts)
    R = 16
    lane_y = y1 + R
    # 3. tray: each feed turns left under the models, the innermost first, and drops at its old x
    runs = []
    for i, (pts, xr, xe) in enumerate(zip(paths, RISER, ends)):
        ty = Y["tray"] + TRAY_DY * i
        rr = 18 + (xr - RISER[0])        # concentric corners
        runs.append(smooth(pts) + f" V{ty - rr} Q{xr} {ty} {xr - rr} {ty} H{xe + R} Q{xe} {ty} {xe} {ty + R}")
    # substation: turns into the lane and branches to Elexon, NESO Data Portal, NESO
    d1 = runs[0] + f" V{y1} Q{ends[0]} {lane_y} {ends[0] - R} {lane_y} H{96 + R} Q96 {lane_y} 96 {lane_y + R} V{Y['r1']}"
    out.append(cable(d1))
    for bx, to in ((416, Y["r1"]), (380, Y["r2"])):
        out.append(cable(f"M{bx + R} {lane_y} Q{bx} {lane_y} {bx} {lane_y + R} V{to}"))
        joints.append((bx + R, lane_y))
    # met mast: straight down the gutter to Open-Meteo (row 2)
    out.append(cable(runs[1] + f" V{Y['r2']}"))
    # converter station: ENTSO-E (row 1)
    out.append(cable(runs[2] + f" V{Y['r1']}"))
    # gas terminal: ENTSO-G (row 2, via the gutter), with a branch to GIE (row 1)
    out.append(cable(runs[3] + f" V{Y['r2']}"))
    jy = Y["r1"] - 44
    out.append(cable(f"M1020 {jy} Q1020 {jy + 14} 1034 {jy + 16} Q1056 {jy + 19} 1056 {jy + 34} V{Y['r1']}"))
    joints.append((1020, jy))
    for jx, jyy in joints:
        out.append(f'<circle cx="{f(jx)}" cy="{f(jyy)}" r="4.6" fill="{INK}"></circle>')
    for key in VENDORS:
        _, top, land = vendor_pos(key)
        out.append(f'<circle cx="{f(land)}" cy="{top}" r="6.5" fill="{T_BRONZE}" stroke="{INK}" stroke-width="2"></circle>'
                   f'<circle cx="{f(land)}" cy="{top}" r="2.2" fill="{INK}"></circle>')
    return "\n".join(out)


SILVER_T = ["silver.fuelhh", "silver.da_prices", "silver.gas_storage", "silver.weather_grid"]
GOLD_T = ["gold.gb_dispatch", "gold.eu_prices", "gold.fundamentals", "gold.daily_brief"]
ST_X = 948           # silver table list left
ST_Y0 = Y["s_head"] + 8
ST_DY = 44
GV_X = [80, 258, 436, 614]


def join_cables() -> str:
    out = []
    sx, sy = 690, Y["splice"]  # splice centre
    # four silver cables leave the table rows, turn down, sweep left into the splice's right end
    for i in range(4):
        ry = ST_Y0 + 20 + i * ST_DY
        xt = ST_X - 34 - (3 - i) * 12  # top row turns furthest left, so nothing crosses
        yin = sy - 9 + i * 6
        pts = [(ST_X - 12, ry), (xt + 14, ry)]
        d = (f"M{ST_X - 12} {ry} H{xt + 14} Q{xt} {ry} {xt} {ry + 14} V{ry + 60 + (3 - i) * 4}")
        c1y = Y["c_sg"] - 40
        d += (f" C{xt} {c1y} {sx + 70 + i * 6} {yin} {sx + 34} {yin}")
        out.append(cable(d, SILVER, 4, 1.4))
        out.append(f'<circle cx="{ST_X - 12}" cy="{ry}" r="4.2" fill="{T_SILVER}" stroke="{INK}" stroke-width="1.6"></circle>')
    # four gold cables leave the splice's left end and fan down to the gold views
    for i, gx in enumerate(GV_X):
        yout = sy - 9 + i * 6
        tx, ty = gx + 10, Y["views"] - 8
        d = f"M{sx - 34} {yout} C{sx - 90 - i * 4} {yout} {tx} {ty - 70 + i * 10} {tx} {ty}"
        out.append(cable(d, GOLD, 4, 1.4))
        out.append(f'<circle cx="{tx}" cy="{ty}" r="4.2" fill="{T_GOLD}" stroke="{INK}" stroke-width="1.6"></circle>')
    # the splice itself
    out.append(f'<rect x="{sx - 36}" y="{sy - 16}" width="72" height="32" rx="16" fill="{GOLD}" stroke="{INK}" '
               f'stroke-width="1.6"></rect>')
    out.append(f'<path d="M{sx - 20} {sy - 16} V{sy + 16} M{sx + 20} {sy - 16} V{sy + 16}" stroke="{INK}" '
               f'stroke-width="1" opacity=".5"></path>')
    return "\n".join(out)


# ================================================================ models tree
# v3: no status anywhere (no Shipped / Planned / F-codes, no solid-vs-dashed taps); every model is simply part
# of the work. The one real link left is the day-ahead case study.
MODELS = [
    ("Day-ahead demand, GB",
     "LightGBM quantile regression on national demand. Calendar and lag-feature pipeline; one model per quantile; "
     'six-fold expanding window. The worked example: <a class="more" href="#">see the case study</a>.',
     "7 quantiles, p05 to p95"),
    ("Wind generation, GB",
     "Same probabilistic estimator family applied to NESO wind output, with Open-Meteo wind-speed grid features. "
     "Output ties into the fundamentals SMP residual.", "7 quantiles, p05 to p95"),
    ("Solar generation, GB",
     "As wind, plus a night-time hard-zero post-processor and irradiance features from Open-Meteo. Different "
     "quantile-crossing risk; same orchestrator.", "7 quantiles, p05 to p95"),
    ("Merit-order supply curve",
     "Vectorised merit-order clearing across the GB plant universe. Fuel costs normalised to £/MWh; CCGT, OCGT, coal, "
     "biomass and pumped storage as separate tranches.", "Point estimate"),
]
SMP = ("Fundamentals SMP forecaster",
       "Monte Carlo sampler over residual demand × supply curve. The headline model, backtested against "
       "ENTSO-E day-ahead prices.", "Joint quantiles")
MT = [0, 160, 320, 500]      # model entry tops, relative to Y["tree"] (checked against measured heights)
E_X, M_W = 300, 470          # entries sit right of the vendor-data busbar
EX = E_X + M_W + 14          # entry output dots
BUS_X = 240                  # the busbar the vendor data arrives on
NODE_X = 872
NODE_RD, NODE_SC = 196, 516  # residual demand / supply curve nodes, relative
SMP_TOP, SMP_X, SMP_W = 318, 976, 332
ORIG_MID = 266               # vendor-data label, relative (vertical middle of the busbar)


def model_blocks() -> str:
    T = Y["tree"]
    out = [f'<div class="blk orig" style="top: {T + ORIG_MID - 15}px; left: 80px; width: 138px">'
           f'<p class="orig-t">Vendor data</p><p class="orig-d">Seven vendors, 165&nbsp;datasets</p></div>']
    for (title, desc, q), dy in zip(MODELS, MT):
        out.append(f'<article class="blk model" style="top: {T + dy}px; left: {E_X}px; width: {M_W}px">'
                   f'<h3>{title}</h3><p>{desc}</p><p class="mq">{q}</p></article>')
    t, d, q = SMP
    out.append(f'<article class="blk model smp" style="top: {T + SMP_TOP}px; left: {SMP_X}px; width: {SMP_W}px">'
               f'<h3>{t}</h3><p>{d}</p><p class="mq">{q}</p></article>')
    return "\n".join(out)


def tree_lines() -> str:
    T = Y["tree"]
    rx, ry = NODE_X, T + NODE_RD
    cx, cy = NODE_X, T + NODE_SC
    smp_x, smp_y = SMP_X - 18, T + SMP_TOP + 19
    lines = []  # v3: one stroke style for every tap and output (no solid-vs-dashed status encoding)

    # vendor data arrives on a busbar and is tapped by every model
    oy = T + ORIG_MID
    b0, b1 = T + MT[0] + 16, T + MT[3] + 16
    g = [f'<path d="M{BUS_X} {b0} V{b1}" stroke="{INK}" stroke-width="5" stroke-linecap="round"></path>',
         f'<path d="M224 {oy} H{BUS_X}" stroke="{INK}" stroke-width="1.5"></path>']
    for dy in MT:
        y = T + dy + 16
        lines.append(f"M{BUS_X} {y} H{E_X - 22}")
    # model outputs: forecasts into residual demand, the supply curve into its node, both into the SMP forecaster
    for dy in MT[:3]:
        y = T + dy + 16
        lines.append(f"M{EX} {y} C{EX + 52} {y} {rx - 52} {ry} {rx - 8} {ry}")
    y = T + MT[3] + 16
    lines.append(f"M{EX} {y} C{EX + 52} {y} {cx - 52} {cy} {cx - 8} {cy}")
    lines.append(f"M{rx + 8} {ry} C{rx + 52} {ry} {smp_x - 56} {smp_y - 8} {smp_x - 10} {smp_y - 3}")
    lines.append(f"M{cx + 8} {cy} C{cx + 52} {cy} {smp_x - 56} {smp_y + 8} {smp_x - 10} {smp_y + 3}")
    g.append(f'<path d="{" ".join(lines)}" fill="none" stroke="{INK}" stroke-width="1.5"></path>')
    for dy in MT:
        y = T + dy + 16
        for x in (E_X - 16, EX):
            g.append(f'<circle cx="{x}" cy="{y}" r="3.6" fill="{INK}" stroke="{INK}" stroke-width="1.5"></circle>')
    for x, y in [(rx, ry), (cx, cy)]:
        g.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{T_TOP}" stroke="{INK}" stroke-width="1.5"></circle>')
    # the destination
    g.append(f'<circle cx="{smp_x}" cy="{smp_y}" r="9" fill="{GOLD}" stroke="{INK}" stroke-width="1.5"></circle>'
             f'<circle cx="{smp_x}" cy="{smp_y}" r="3" fill="{INK}"></circle>')
    g.append(f'<g font-family="Hanken Grotesk" font-style="italic" font-size="14.5" fill="{INK}">'
             f'<text x="{rx + 12}" y="{ry - 14}">residual demand</text>'
             f'<text x="{cx}" y="{cy + 28}" text-anchor="middle">supply curve</text></g>')
    return "\n".join(g)


# ================================================================ strata (background)
def strata() -> str:
    top_c = wave(Y["c_tb"], 7, 0.4)
    bs_c = wave(Y["c_bs"], 8, 2.1)
    sg_c = wave(Y["c_sg"], 7, 4.0)
    gr_c = [(x, Y["c_gr"] + 9 * math.sin(x / 140 + 1) + 6 * math.sin(x / 53 + 2) + 4 * math.sin(x / 19))
            for x in range(-40, W + 41, 20)]

    def band(pts: list[tuple[float, float]], fill: str, pat: str | None, op: str) -> str:
        d = smooth(pts) + f" L{W + 40} {H + 10} L-40 {H + 10} Z"
        s = f'<path d="{d}" fill="{fill}"></path>'
        if pat:
            s += f'<path d="{d}" fill="url(#{pat})" opacity="{op}"></path>'
        return s

    surf = [(x, prof(x)) for x in range(-40, W + 41, 20)]
    surf_d = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in surf)
    root = surf_d + " " + " ".join(f"L{f(x)} {f(y + 9)}" for x, y in reversed(surf)) + " Z"
    gr_d = smooth(gr_c)
    beds = (f'<path d="{smooth(wave(Y["bed1"], 5, 1.2, 160))}" stroke="{INK}" stroke-width="1" stroke-dasharray="2 6" '
            f'fill="none" opacity=".55"></path>'
            f'<path d="{smooth(wave(Y["bedP"], 5, 3.3, 160))}" stroke="{INK}" stroke-width="1" stroke-dasharray="2 6" '
            f'fill="none" opacity=".55"></path>')
    unit = []
    for yy, name in [(Y["c_tb"], "bronze"), (Y["c_bs"], "silver"), (Y["c_sg"], "gold")]:
        unit.append(f'<text x="1360" y="{yy + 30}" text-anchor="end">{name}</text>')
    return "\n".join([
        f'<rect x="0" y="0" width="{W}" height="{Y["surf"] + 20}" fill="{PETROL}"></rect>',
        f'<path d="{surf_d} L{W + 40} {H + 10} L-40 {H + 10} Z" fill="{T_TOP}"></path>',
        f'<path d="{surf_d} L{W + 40} {H + 10} L-40 {H + 10} Z" fill="url(#p-soil)" opacity=".5"></path>',
        band(top_c, T_BRONZE, "p-brick", ".15"),
        band(bs_c, T_SILVER, "p-diag", ".22"),
        band(sg_c, T_GOLD, "p-stip", ".26"),
        f'<path d="{gr_d} L{W + 40} {H + 10} L-40 {H + 10} Z" fill="{PETROL}"></path>',
        f'<path d="{gr_d} L{W + 40} {H + 10} L-40 {H + 10} Z" fill="url(#p-granite)" opacity=".5"></path>',
        f'<path d="{root}" fill="{OLIVE}"></path>',
        f'<path d="{surf_d}" stroke="{INK}" stroke-width="1.5" fill="none"></path>',
        f'<path d="{smooth(top_c)} {smooth(bs_c)} {smooth(sg_c)}" stroke="{INK}" stroke-width="1.5" fill="none"></path>',
        f'<path d="{gr_d}" stroke="{INK}" stroke-width="2" fill="none" stroke-linejoin="round"></path>',
        beds,
        f'<g font-family="Hanken Grotesk" font-style="italic" font-size="14" fill="{INK}">{"".join(unit)}</g>',
    ])


PATTERNS = f"""<pattern id="p-stip" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="2" cy="3" r="1" fill="#8A6F1E"></circle><circle cx="6.5" cy="7.5" r=".8" fill="#8A6F1E"></circle></pattern>
<pattern id="p-diag" width="8" height="8" patternUnits="userSpaceOnUse"><path d="M0 8 L8 0" stroke="#5E6E6B" stroke-width=".8"></path></pattern>
<pattern id="p-brick" width="24" height="12" patternUnits="userSpaceOnUse"><path d="M0 11.5 H24 M12 0 V6 M0 6 H24 M0 6 V12" stroke="#7C5530" stroke-width=".8" fill="none"></path></pattern>
<pattern id="p-soil" width="23" height="17" patternUnits="userSpaceOnUse"><circle cx="4" cy="5" r=".9" fill="{KHAKI}"></circle><circle cx="15" cy="12" r="1.1" fill="{KHAKI}"></circle><path d="M17 3 h3" stroke="{KHAKI}" stroke-width=".9"></path></pattern>
<pattern id="p-granite" width="46" height="40" patternUnits="userSpaceOnUse"><path d="M8 8 h8 M12 4 v8 M30 26 h8 M34 22 v8 M20 34 h6 M23 31 v6 M40 6 h5 M42.5 3.5 v5" stroke="{HORIZON}" stroke-width="1.1"></path></pattern>"""


# ================================================================ html
def swatch(fill: str, pid: str, pat_path: str, w: int = 46, h: int = 30) -> str:
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" aria-hidden="true"><defs>{pat_path}</defs>'
            f'<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" fill="{fill}"></rect>'
            f'<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" fill="url(#{pid})" opacity=".45"></rect>'
            f'<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" fill="none" stroke="{INK}" stroke-width="1.5"></rect></svg>')


def key_block() -> str:
    sw_b = swatch(T_BRONZE, "k-b", '<pattern id="k-b" width="24" height="12" patternUnits="userSpaceOnUse"><path d="M0 11.5 H24 M12 0 V6 M0 6 H24 M0 6 V12" stroke="#7C5530" stroke-width=".8" fill="none"></path></pattern>')
    sw_s = swatch(T_SILVER, "k-s", '<pattern id="k-s" width="8" height="8" patternUnits="userSpaceOnUse"><path d="M0 8 L8 0" stroke="#5E6E6B" stroke-width=".8"></path></pattern>')
    sw_g = swatch(T_GOLD, "k-g", '<pattern id="k-g" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="2" cy="3" r="1" fill="#8A6F1E"></circle><circle cx="6.5" cy="7.5" r=".8" fill="#8A6F1E"></circle></pattern>')
    items = [
        (sw_b, "Vendors", "Seven vendors across UK and EU power, gas, carbon and weather: 165 datasets, each with schema, "
                          "sample queries, and the caveats that bite."),
        (sw_s, "Pipeline", "Bronze, silver and gold layers. End-to-end data flow, design decisions, and the full repo map."),
        (sw_g, "Forecasts", "Quantitative work built on the warehouse: probabilistic demand, wind, solar, and a "
                            "fundamentals SMP forecaster."),
    ]
    li = "".join(f'<li><a href="#">{sw}<h3>{t}</h3><p>{d}</p></a></li>' for sw, t, d in items)
    return (f'<section class="blk key" aria-labelledby="key-h" style="top: 348px; left: 80px; width: 820px">'
            f'<h2 id="key-h">Three things to explore</h2><ul>{li}</ul></section>')


# ================================================================ the workbench section (the one variable)
# Every handle, verb and docstring line here was read from gridflow-models (research/handles/source.py,
# data.py, models.py, model.py, _help_card.py; notebooks/data_layer/01_elexon.py, 00_overview.py;
# notebooks/models/01_demand_forecast.py) or introspected from Data() / Models(). No output data is shown.
SRC_VERBS = [  # SourceClient._VERBS, in card order, with the first line of each docstring
    ("list_datasets", "List every dataset this source provides."),
    ("refresh", "Fetch the latest rows for this source, topping up what you have."),
    ("describe", "Show a dataset's columns, sample values, and freshness."),
    ("backfill", "Download history for a dataset and store it locally."),
    ("query", "Read stored rows for a dataset over a date range."),
    ("tail", "Read the most recent rows of a dataset."),
    ("coverage", "Show how up to date each dataset on this source is."),
]
SOURCES = ["elexon", "entsoe", "entsog", "gie_agsi", "gie_alsi", "neso", "neso_data_portal", "open_meteo"]
PRED_HANDLES = ["demand_forecast", "demand_forecast_v2", "wind_forecast", "solar_forecast"]
PRED_VERBS = ["train", "validate", "show_folds", "gold_dataset", "feature_matrix", "predict", "predict_raw",
              "predict_range", "predictions", "backtest_predictions", "features_at", "check_data_freshness",
              "register"]
OTHER_MODELS = [("stack", ["build", "clear"]), ("fundamentals_smp", ["assemble", "backtest", "components"])]

WB_H2 = "Run it all from a notebook"
WB_P1 = ('The workbench lives in <code>gridflow-models</code>. One call returns three handles: <code>data</code> for '
         'the warehouse, <code>models</code> for the modelling stack and <code>common</code> for shared helpers.')
WB_P2 = ('Run a source, or any of its verbs, on its own and it renders a help card. Tab, shift+tab and '
         '<code>?</code> work as usual.')
SETUP = ('<span class="k">from</span> gridflow_models <span class="k">import</span> setup_notebook\n'
         'data, models, common = setup_notebook()')
Q_FUEL = 'data.elexon.query("fuelhh", "2026-08-01", "2026-08-05")'


def hl(code: str) -> str:
    """Tint the string literals in a line of Python."""
    return re.sub(r'"[^"]*"', lambda m: f'<span class="s">{m.group(0)}</span>', code)


def wb_open(extra: str = "") -> str:
    return (f'<section class="blk wb{extra}" aria-labelledby="wb-h" style="top: {Y["q_head"]}px; left: 80px; '
            f'width: 1280px">')


def wb_copy() -> str:
    return f'<div class="sec"><h2 id="wb-h">{WB_H2}</h2><p>{WB_P1}</p><p>{WB_P2}</p></div>'


# v4: the query comes back. Real rows from silver elexon fuelhh, settlement date 2026-08-01, period 1, the first
# five fuel types in sort order (read from C:\gridflow-data\silver\elexon\fuelhh on 2026-09-26).
HEAD_COLS = ["settlement_date", "settlement_period", "fuel_type", "generation_mw"]
HEAD_ROWS = [("2026-08-01", "1", "BIOMASS", "2367.0"), ("2026-08-01", "1", "CCGT", "9789.0"),
             ("2026-08-01", "1", "COAL", "0.0"), ("2026-08-01", "1", "INTELEC", "402.0"),
             ("2026-08-01", "1", "INTEW", "-532.0")]
Q_HEAD = 'df[[' + ", ".join(f'"{c}"' for c in HEAD_COLS) + ']].head()'


def df_html() -> str:
    """The frame as pandas renders it in JupyterLab: index column, right-aligned cells, banded rows."""
    head = "<tr><th></th>" + "".join(f"<th>{c}</th>" for c in HEAD_COLS) + "</tr>"
    body = "".join(f"<tr><th>{i}</th>" + "".join(f"<td>{v}</td>" for v in r) + "</tr>"
                   for i, r in enumerate(HEAD_ROWS))
    return f'<table class="df"><thead>{head}</thead><tbody>{body}</tbody></table>'


def wb_notebook() -> str:
    """A: a JupyterLab session drawn in the site's own materials."""
    rows = "".join(f"<div><dt>{n}</dt><dd>{d}</dd></div>" for n, d in SRC_VERBS)
    comp = "".join(f'<li class="sel">{n}</li>' if i == 0 else f"<li>{n}</li>"
                   for i, n in enumerate(sorted(n for n, _ in SRC_VERBS)))
    cell = '<div class="cell{c}"><span class="pr">{p}</span>{body}</div>'
    body = "".join([
        cell.format(c="", p="[1]:", body=f'<pre class="in">{SETUP}</pre>'),
        cell.format(c="", p="[2]:", body='<pre class="in">data.elexon</pre>'),
        cell.format(c=" out", p="[2]:", body=(
            f'<div class="card"><p class="card-h">data.elexon</p><dl>{rows}</dl>'
            f'<p class="card-f">Discover datasets: <code>data.elexon.list_datasets()</code></p></div>')),
        cell.format(c="", p="[3]:", body=f'<pre class="in">df = {hl(Q_FUEL)}</pre>'),
        cell.format(c="", p="[4]:", body=f'<pre class="in">{hl(Q_HEAD)}</pre>'),
        cell.format(c=" out", p="[4]:", body=df_html()),
        cell.format(c=" act", p="[ ]:", body=(
            '<pre class="in">data.entsoe.<span class="caret"></span></pre>'
            f'<ul class="cmp" aria-label="Tab completions for data.entsoe">{comp}</ul>')),
    ])
    aria = ("A JupyterLab notebook, fuelhh_analysis.ipynb, on the gridflow_models kernel: the setup cell, the help "
            "card for data.elexon listing its seven verbs, a query for fuelhh into df, the first five rows of df "
            "(settlement date 2026-08-01, period 1: biomass 2367 MW, CCGT 9789, coal 0, INTELEC 402, INTEW -532), "
            "and tab completion on data.entsoe showing the same seven verbs.")
    return (wb_open() + f'<div class="wb-grid">{wb_copy()}'
            f'<figure class="nb" aria-label="{aria}"><div class="nb-bar"><span class="nb-tab">fuelhh_analysis.ipynb</span>'
            f'<span class="nb-kern">gridflow_models</span></div><div class="nb-body">{body}</div></figure>'
            f'</div></section>')


TREE_TOP = 196   # the tree drawing, relative to the section top
WBT_H = 482


def wb_tree() -> str:
    """B: the tab-completable surface drawn as buried cable: handles branch, shared verbs splice."""
    t0, P, VP = 20, 30, 24
    mono = 'font-family="Red Hat Mono"'
    g: list[str] = []
    txt: list[str] = []
    ends: list[str] = []

    def term(x: float, y: float, fill: str) -> None:
        ends.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="4.2" fill="{fill}" stroke="{INK}" stroke-width="1.6"></circle>')

    def splice(cx: float, cy: float, w: float, fill: str) -> None:
        ends.append(f'<rect x="{f(cx - w / 2)}" y="{f(cy - 15)}" width="{f(w)}" height="30" rx="15" fill="{fill}" '
                    f'stroke="{INK}" stroke-width="1.6"></rect>'
                    f'<path d="M{f(cx - w / 2 + 16)} {f(cy - 15)} V{f(cy + 15)} M{f(cx + w / 2 - 16)} {f(cy - 15)} '
                    f'V{f(cy + 15)}" stroke="{INK}" stroke-width="1" opacity=".5"></path>')

    def label(x: float, y: float, s: str, size: float = 14, extra: str = "") -> None:
        txt.append(f'<text x="{f(x)}" y="{f(y + 5)}" {mono} font-size="{size}" {extra}>{s}</text>')

    def tag(x: float, y: float, s: str) -> None:
        # a handle's name rides on its cable, like a cable marker
        txt.append(f'<text x="{f(x)}" y="{f(y - 8)}" {mono} font-size="14">{s}</text>')

    # ---- data: root, eight sources (one cable each), one splice, the seven shared verbs
    ys = [t0 + 4 + i * P for i in range(len(SOURCES))]
    yc = (ys[0] + ys[-1]) / 2
    label(0, yc, "data", 17, 'font-weight="500"')
    run, sp_x, sp_w = 272, 384, 72
    for i, (s, y) in enumerate(zip(SOURCES, ys)):
        yin = yc - 10.5 + i * 3
        g.append(cable(f"M50 {f(yc)} C82 {f(yc)} 78 {f(y)} 110 {f(y)} H{run} C{run + 42} {f(y)} "
                       f"{f(sp_x - sp_w / 2 - 42)} {f(yin)} {f(sp_x - sp_w / 2)} {f(yin)}", SILVER, 4, 1.4))
        term(110, y, T_SILVER)
        tag(124, y, s)
    for j, (v, _) in enumerate(SRC_VERBS):
        yv = yc + (j - 3) * P
        yo = yc - 9 + j * 3
        g.append(cable(f"M{f(sp_x + sp_w / 2)} {f(yo)} C{f(sp_x + sp_w / 2 + 38)} {f(yo)} 456 {f(yv)} 490 {f(yv)}",
                       SILVER, 4, 1.4))
        term(494, yv, T_SILVER)
        label(506, yv, v)
    splice(sp_x, yc, sp_w, SILVER)
    txt.append(f'<text x="{sp_x}" y="{f(ys[-1] + 40)}" text-anchor="middle" font-family="Hanken Grotesk" '
               f'font-style="italic" font-size="14.5">the same seven verbs on every source</text>')

    # ---- one worked lifecycle, down a short cable under the data tree
    life = [("discover", "data.elexon.list_datasets()"), ("refresh", 'data.elexon.refresh("fuelhh", yes=True)'),
            ("query", Q_FUEL), ("inspect", 'data.elexon.describe("fuelhh")')]
    l0 = t0 + 318
    g.append(cable(f"M6 {l0 - 16} V{l0 + 3 * 36 + 16}", SILVER, 4, 1.4))
    for r, (stage, call) in enumerate(life):
        y = l0 + r * 36
        term(6, y, T_SILVER)
        txt.append(f'<text x="24" y="{y + 5}" font-family="Hanken Grotesk" font-style="italic" '
                   f'font-size="14.5">{stage}</text>')
        tinted = re.sub(r'"[^"]*"', lambda m: f'<tspan fill="#7C5530">{m.group(0)}</tspan>', call)
        label(104, y, tinted)

    # ---- models: root, six model handles; the four forecast models splice into their shared verbs
    vr = [t0 + j * VP for j in range(len(PRED_VERBS))]
    groups = []
    y = vr[-1] + VP + 18
    for name, verbs in OTHER_MODELS:
        rows = [y + k * VP for k in range(len(verbs))]
        groups.append((name, verbs, rows))
        y = rows[-1] + VP + 18
    pc = (vr[0] + vr[-1]) / 2
    hy = [pc + d for d in (-42, -14, 14, 42)] + [(r[0] + r[-1]) / 2 + 4 for _, _, r in groups]
    yr = (hy[0] + hy[-1]) / 2
    label(660, yr, "models", 17, 'font-weight="500"')
    RX, TX, MRUN, VX = 728, 776, 952, 1080
    msp_x, msp_w = 1004, 52
    for i, (h, y) in enumerate(zip(PRED_HANDLES, hy)):
        yin = pc - 4.5 + i * 3
        g.append(cable(f"M{RX} {f(yr)} C{RX + 34} {f(yr)} {TX - 34} {f(y)} {TX} {f(y)} H{MRUN} "
                       f"C{MRUN + 26} {f(y)} {f(msp_x - msp_w / 2 - 26)} {f(yin)} {f(msp_x - msp_w / 2)} {f(yin)}",
                       GOLD, 4, 1.4))
    for (name, verbs, rows), y in zip(groups, hy[4:]):
        g.append(cable(f"M{RX} {f(yr)} C{RX + 34} {f(yr)} {TX - 34} {f(y)} {TX} {f(y)} H{MRUN}", GOLD, 4, 1.4))
        for v, ry in zip(verbs, rows):
            g.append(cable(f"M{MRUN} {f(y)} C{MRUN + 60} {f(y)} {VX - 64} {f(ry)} {VX - 4} {f(ry)}", GOLD, 4, 1.4))
            term(VX, ry, T_GOLD)
            label(VX + 12, ry, v)
    for h, y in zip(PRED_HANDLES + [n for n, _, _ in groups], hy):
        term(TX, y, T_GOLD)
        tag(TX + 14, y, h)
    for j, (v, y) in enumerate(zip(PRED_VERBS, vr)):
        yo = pc - 9 + j * 1.5
        g.append(cable(f"M{f(msp_x + msp_w / 2)} {f(yo)} C{f(msp_x + msp_w / 2 + 24)} {f(yo)} {VX - 28} {f(y)} "
                       f"{VX - 4} {f(y)}", GOLD, 4, 1.4))
        term(VX, y, T_GOLD)
        label(VX + 12, y, v)
    splice(msp_x, pc, msp_w, GOLD)

    aria = ("The workbench as a tree of tab-completable handles. data splits into eight sources: "
            + ", ".join(SOURCES) + "; all eight share the same seven verbs: "
            + ", ".join(v for v, _ in SRC_VERBS) + ". models splits into six model handles. demand_forecast, "
            "demand_forecast_v2, wind_forecast and solar_forecast share thirteen verbs: " + ", ".join(PRED_VERBS)
            + "; stack has build and clear; fundamentals_smp has assemble, backtest and components. A worked "
            "lifecycle: discover with data.elexon.list_datasets(), refresh with data.elexon.refresh(‘fuelhh’, "
            "yes=True), query with data.elexon.query for 1 to 5 August 2026, inspect with data.elexon.describe.")
    svg = (f'<svg width="1280" height="{WBT_H}" viewBox="0 0 1280 {WBT_H}" role="img" aria-label="{aria}" '
           f'style="position: absolute; top: {TREE_TOP}px; left: 0">'
           f'<g>{"".join(g)}</g><g>{"".join(ends)}</g><g fill="{INK}">{"".join(txt)}</g></svg>')
    return (wb_open() + f'<div class="wbB-head"><div class="sec"><h2 id="wb-h">{WB_H2}</h2></div>'
            f'<div class="sec"><p>{WB_P1}</p><p>{WB_P2}</p></div></div>{svg}</section>')


def wb_lifecycle() -> str:
    """C: the lifecycle as four plain steps, the real calls beside each."""
    steps = [
        ("Set up", "One call builds the three handles, on the <code>gridflow_models</code> Jupyter kernel.", SETUP),
        ("Run the pipeline", "<code>backfill</code> and <code>refresh</code> run the gridflow pipeline from the "
         "notebook; nothing is fetched until you pass <code>yes=True</code>.",
         hl('data.elexon.backfill("fuelhh", "2026-08-01", "2026-08-05", yes=True)\n'
            'data.elexon.refresh("fuelhh", yes=True)\ndata.refresh_all(yes=True)')),
        ("Explore the data", "Every source answers the same seven verbs; <code>data.sql</code> takes read-only SQL "
         "across all of them.",
         hl(f'data.elexon.list_datasets()\ndata.elexon.describe("fuelhh")\ndf = {Q_FUEL}\n'
            'data.sql("SELECT * FROM silver_system_prices LIMIT 5")')),
        ("Work the models", "The demand, wind and solar models share one set of verbs, and the walk-forward folds "
         "are built for you.",
         "dm = models.demand_forecast\ndm.show_folds(start, end)\ndm.validate(start, end)\ndm.train()\n"
         "dm.backtest_predictions(start, end)"),
    ]
    li = "".join(f"<li><div><h3>{t}</h3><p>{s}</p></div><pre>{c}</pre></li>" for t, s, c in steps)
    return wb_open() + f'<div class="wb-grid">{wb_copy()}<ol class="lc">{li}</ol></div></section>'


WORKBENCH = {"A": wb_notebook, "B": wb_tree, "C": wb_lifecycle}

SKILLS = [
    ("Languages", "Python, SQL"),
    ("Data engineering", "Polars, DuckDB, Parquet, Pydantic, medallion architecture, event-driven design (Kafka)"),
    ("Quant and ML", "LightGBM, quantile regression, conformal prediction (MAPIE), linear programming (PuLP), "
                     "Monte Carlo, time-series analysis"),
    ("HPC", "Multithreading, multiprocessing, parallel batch compute, distributed computing (PySpark)"),
    ("Cloud and infra", "AWS, Azure, Docker, Git, CI/CD"),
    ("Visualisation", "Power BI, Plotly, matplotlib"),
    ("Markets", "UK and European power, gas, FX options, rates, credit, commodities, vol surfaces"),
]

CSS = """body{margin:0}
.root{background:#155A6E;color:#1C2B22;font:400 16px/1.6 "Hanken Grotesk",sans-serif;font-variant-numeric:tabular-nums;-webkit-font-smoothing:antialiased}
.root a{color:inherit;text-decoration-thickness:1.5px;text-underline-offset:4px}
.root a:focus-visible{outline:2px solid #AFC64E;outline-offset:3px;border-radius:2px}
.root h1,.root h2,.root h3{font-family:"Bricolage Grotesque",sans-serif;margin:0;font-optical-sizing:auto}
.root code{font-family:"Red Hat Mono",monospace;font-size:.9em}
.layer{position:absolute;left:0;top:0}
.blk{position:absolute}
.mast{position:absolute;top:26px;left:80px;right:80px;display:flex;justify-content:space-between;align-items:baseline;color:#F6F4EC}
.brand{font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:24px;letter-spacing:-.01em;text-decoration:none}
.mast ul{display:flex;gap:30px;list-style:none;margin:0;padding:0;font-size:15px}
.mast ul a{text-decoration:none;color:#CFE0DC}
.mast ul a:hover{color:#F6F4EC}
.mast ul a[aria-current="page"]{color:#F6F4EC;box-shadow:inset 0 -2px 0 #AFC64E}
.hero h1{color:#F6F4EC;font-weight:760;font-stretch:84%;font-size:86px;line-height:.94;letter-spacing:-.022em}
.lede{color:#F6F4EC}
.lede p{margin:0;font-size:17.5px;line-height:1.6;color:#CFE0DC}
.cta{display:flex;gap:26px;align-items:center;margin:26px 0 22px}
.go{background:#AFC64E;color:#1C2B22;font-weight:600;padding:12px 20px;border-radius:3px;text-decoration:none}
.root .go{color:#1C2B22;text-decoration:none}
.go:hover{background:#C3D86A}
.alt{font-weight:600;color:#F6F4EC;text-decoration-color:#AFC64E}
.lede .scope{font-size:15px;color:#A9C7C4}
.key h2{color:#F6F4EC;font-size:21px;font-weight:650;font-stretch:92%;letter-spacing:-.005em;margin:0 0 16px}
.key ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));column-gap:34px}
.key a{display:block;text-decoration:none;color:#F6F4EC}
.key svg{display:block;margin:0 0 12px}
.key h3{font-size:20px;font-weight:700;font-stretch:90%;margin:0 0 4px;text-decoration:underline;text-decoration-color:rgba(175,198,78,.0);text-underline-offset:4px}
.key a:hover h3{text-decoration-color:#AFC64E}
.key p{margin:0;font-size:14.5px;line-height:1.5;color:#CFE0DC}
.land-svg text{font-family:"Hanken Grotesk",sans-serif;font-style:italic;font-size:13.5px}
.coreblk h2{font-size:30px;font-weight:700;font-stretch:90%;letter-spacing:-.012em;margin:0 0 6px}
.coreblk svg{display:block}
.coreblk .cap{margin:8px 0 0;font-size:14.5px;line-height:1.55;color:#3F4A3B;max-width:66ch}
.sec h2{font-size:42px;font-weight:720;font-stretch:88%;line-height:1.02;letter-spacing:-.018em;margin:0 0 16px}
.sec p{margin:0 0 14px;font-size:16px;line-height:1.62;color:#3F4A3B;max-width:58ch}
.sec .more{font-weight:600;color:#1C2B22;text-decoration-color:#66793B}
.vend .land{margin:0 0 10px;height:18px;font-size:13px;line-height:18px;transform:translateY(-9px);color:#1C2B22}
.vend h3{font-size:23px;font-weight:720;font-stretch:90%;line-height:1.1;letter-spacing:-.01em;margin:0 0 6px}
.vend h3 a{text-decoration-color:rgba(28,43,34,.0)}
.vend h3 a:hover{text-decoration-color:#66793B}
.vend .vd{margin:0;font-size:14.5px;line-height:1.45;color:#3F4A3B;min-height:42px}
.vend .vm{margin:6px 0 12px;font-size:14.5px;font-weight:600;color:#1C2B22}
.vend svg{display:block}
.vend .sc{margin:8px 0 0;font-size:13px;line-height:1.45;color:#3F4A3B}
.vend .sc code{color:#1C2B22;font-size:13px}
.note{font-size:14px;line-height:1.55;color:#3F4A3B;margin:0}
.tables{list-style:none;margin:0;padding:0}
.tables li{font-family:"Red Hat Mono",monospace;font-size:16px;height:44px;line-height:44px;border-bottom:1px solid rgba(28,43,34,.22);color:#1C2B22}
.views{list-style:none;margin:0;padding:0;display:flex}
.views li{position:absolute;top:0;font-family:"Red Hat Mono",monospace;font-size:15.5px;color:#1C2B22}
.why h2{font-size:52px;font-weight:740;font-stretch:84%;line-height:1;letter-spacing:-.02em;margin:0 0 22px}
.why .intro{margin:0;font-size:21px;line-height:1.5;color:#1C2B22;max-width:36ch}
.why-body p{margin:0 0 14px;font-size:16px;line-height:1.62;color:#3F4A3B}
.why-body .aim{color:#1C2B22;font-weight:600}
.orig-t{margin:0 0 4px;font-family:"Bricolage Grotesque",sans-serif;font-size:20px;font-weight:700;font-stretch:90%;line-height:1.1;color:#1C2B22}
.orig-d{margin:0;font-size:14px;line-height:1.45;color:#3F4A3B}
.model h3{font-size:23px;font-weight:720;font-stretch:90%;line-height:1.1;letter-spacing:-.01em;margin:0 0 6px}
.model p{margin:0;font-size:14.5px;line-height:1.5;color:#3F4A3B}
.model .mq{margin:8px 0 0;font-size:14px;color:#1C2B22}
.model .more{font-weight:600;color:#1C2B22;text-decoration-color:#66793B}
.model.smp h3{font-size:32px;font-stretch:86%;line-height:1.02;margin:0 0 10px}
.model.smp p{font-size:15.5px}
.foot{font-size:14.5px;color:#3F4A3B;margin:0}
.wb h2{margin-bottom:18px}
.wb .sec p code{font-size:.86em;color:#1C2B22}
.wb-grid{display:grid;grid-template-columns:360px minmax(0,1fr);gap:64px;align-items:start}
.nb{margin:0;background:#F6F4EC;border:1.5px solid #1C2B22;border-radius:4px;overflow:hidden}
.nb-bar{display:flex;justify-content:space-between;align-items:flex-end;height:40px;background:#1C2B22;padding:0 18px 0 12px;font:500 13.5px/1 "Red Hat Mono",monospace}
.nb-tab{background:#F6F4EC;color:#1C2B22;padding:11px 18px 12px;border-radius:3px 3px 0 0}
.nb-kern{color:#CFE0DC;align-self:center}
.nb-body{position:relative;padding:16px 24px 176px 8px}
.cell{display:grid;grid-template-columns:52px minmax(0,1fr);column-gap:10px;margin:0 0 9px;position:relative}
.cell.out{margin:-3px 0 12px}
.pr{font:400 13px/1 "Red Hat Mono",monospace;color:#5d6a55;text-align:right;padding-top:12px}
.in{margin:0;background:#ECE8DA;border:1px solid rgba(28,43,34,.18);border-radius:3px;padding:8px 12px;font:400 14.5px/1.6 "Red Hat Mono",monospace;color:#1C2B22;white-space:pre;overflow:hidden}
.in .k,.lc .k{color:#155A6E;font-weight:500}
.in .s,.lc .s{color:#7C5530}
.act .in{background:#F6F4EC;border-color:#1C2B22}
.caret{display:inline-block;width:1.5px;height:1.2em;background:#1C2B22;vertical-align:-.25em}
.cmp{position:absolute;top:100%;left:167px;margin:-2px 0 0;padding:4px 0;list-style:none;width:176px;background:#F6F4EC;border:1px solid #1C2B22;border-radius:2px;font:400 14px/22px "Red Hat Mono",monospace;color:#1C2B22}
.cmp li{padding:0 12px}
.cmp .sel{background:#1C2B22;color:#F6F4EC}
.card{max-width:600px;border:1px solid rgba(28,43,34,.34);border-radius:3px;overflow:hidden;background:#F6F4EC}
.card-h{margin:0;padding:9px 14px;background:#ECE8DA;border-bottom:1px solid rgba(28,43,34,.2);font:500 15px/1.2 "Red Hat Mono",monospace;color:#155A6E}
.card dl{margin:0;padding:7px 8px 1px}
.card dl div{display:grid;grid-template-columns:136px minmax(0,1fr);gap:14px;padding:2px 8px;border-radius:2px}
.card dl div:nth-child(odd){background:#EFEBDF}
.card dt{font:400 13.5px/1.5 "Red Hat Mono",monospace;color:#155A6E}
.card dd{margin:0;font-size:14px;line-height:1.45;color:#1C2B22}
.card-f{margin:5px 14px 10px;padding-top:8px;border-top:1px solid rgba(28,43,34,.2);font-size:13.5px;color:#3F4A3B}
.card-f code{font-size:13px;color:#1C2B22;background:#ECE8DA;padding:1px 5px;border-radius:2px}
.df{justify-self:start;border-collapse:collapse;margin:3px 0 0;font:400 13.5px/1 "Hanken Grotesk",sans-serif;font-variant-numeric:tabular-nums;color:#1C2B22}
.df th,.df td{padding:6px 12px;text-align:right;white-space:nowrap}
.df thead th{font-weight:600;border-bottom:1px solid #1C2B22;vertical-align:bottom}
.df tbody th{font-weight:600}
.df tbody tr:nth-child(odd){background:#EFEBDF}
.wbB-head{display:grid;grid-template-columns:620px minmax(0,1fr);gap:92px;align-items:start}
.wbB-head p:last-child{margin-bottom:0}
.wb svg{display:block}
.lc{list-style:none;margin:0;padding:0;border-bottom:1px solid rgba(28,43,34,.25)}
.lc li{display:grid;grid-template-columns:240px minmax(0,1fr);gap:36px;padding:26px 0 28px;border-top:1px solid rgba(28,43,34,.25)}
.lc h3{font-size:23px;font-weight:720;font-stretch:90%;line-height:1.1;letter-spacing:-.01em;margin:0 0 7px}
.lc p{margin:0;font-size:14.5px;line-height:1.5;color:#3F4A3B}
.lc p code{font-size:13.5px;color:#1C2B22}
.lc pre{margin:2px 0 0;font:400 14px/1.85 "Red Hat Mono",monospace;color:#1C2B22;white-space:pre}
.about{color:#F6F4EC}
.about h2{font-size:56px;font-weight:760;font-stretch:84%;line-height:1;letter-spacing:-.02em;margin:0 0 10px}
.about .role{margin:0 0 26px;font-size:16px;color:#A9C7C4}
.about .intro{margin:0 0 18px;font-size:21px;line-height:1.5;color:#F6F4EC;max-width:34ch}
.about .body{margin:0 0 30px;font-size:15.5px;line-height:1.7;color:#CFE0DC;max-width:62ch}
.links{display:flex;flex-wrap:wrap;gap:12px}
.links a{font-weight:600;padding:10px 18px;border-radius:3px;text-decoration:none;border:1.5px solid rgba(207,224,220,.55);color:#F6F4EC}
.links a:hover{border-color:#F6F4EC}
.root .links a.primary{background:#AFC64E;border-color:#AFC64E;color:#1C2B22}
.skills h3{font-size:22px;font-weight:700;font-stretch:90%;margin:0 0 12px;color:#F6F4EC}
.skills dl{margin:0}
.skills div{display:grid;grid-template-columns:150px minmax(0,1fr);gap:18px;padding:11px 0;border-top:1px solid rgba(207,224,220,.22)}
.skills dt{font-weight:600;font-size:14.5px;color:#F6F4EC}
.skills dd{margin:0;font-size:14.5px;line-height:1.5;color:#CFE0DC}
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


def page(purpose: str) -> str:
    S = Y["surf"]
    bg = (f'<svg class="layer" width="{W}" height="{H}" viewBox="0 0 {W} {H}" aria-hidden="true">'
          f'<defs>{PATTERNS}</defs>\n{strata()}\n</svg>')
    land_h = S + 14
    land = (f'<svg class="layer land-svg" width="{W}" height="{land_h}" viewBox="0 0 {W} {land_h}" role="img" '
            f'aria-label="Drawing of the physical grid: onshore and offshore wind, a solar farm, a gas-fired power '
            f'station and pylons, a data centre, battery storage, a substation, a met mast, an interconnector '
            f'converter station and a gas terminal. Cables run from the substation, the met mast, the converter '
            f'station and the gas terminal down into the data layers below.">\n{landscape()}\n{land_labels()}\n</svg>')
    cables = (f'<svg class="layer" width="{W}" height="{H}" viewBox="0 0 {W} {H}" aria-hidden="true">\n'
              f'{feed_cables()}\n{join_cables()}\n{tree_lines() if purpose == "base" else ""}\n</svg>')

    nav = """<header class="mast">
<a class="brand" href="#">gridflow</a>
<nav aria-label="Primary">
<ul>
<li><a href="#" aria-current="page">Home</a></li>
<li><a href="#">Data sources</a></li>
<li><a href="#">Architecture</a></li>
<li><a href="#">Models</a></li>
<li><a href="#">About</a></li>
</ul>
</nav>
</header>"""
    hero = (f'<div class="blk hero" style="top: 128px; left: 80px; width: 860px">'
            f'<h1>A pipeline and catalogue for UK &amp; European energy data.</h1></div>'
            f'<div class="blk lede" style="top: 142px; left: 986px; width: 374px">'
            f'<p>Gridflow ingests, normalises and serves time-series data from seven public and authenticated vendors '
            f'(electricity, gas, weather and carbon) into a single queryable warehouse. Models for demand, wind, solar '
            f'and clearing prices sit one layer above.</p>'
            f'<div class="cta"><a class="go" href="#">Explore the architecture</a><a class="alt" href="#">See a model</a></div>'
            f'<p class="scope">Seven vendors, 165 datasets, four markets, seventeen years of history, three pipeline layers.</p>'
            f'</div>')
    core = (f'<section class="blk coreblk" aria-labelledby="core-h" style="top: {Y["core"]}px; left: 64px; width: 800px">'
            f'<h2 id="core-h" style="margin-left: 16px">Great Britain’s generation by fuel, 1 to 5 August 2026</h2>'
            f'{core_svg()}'
            f'<p class="cap" style="margin-left: 16px">Mean output per fuel type across 240 half-hourly settlement periods; '
            f'the six fuels sum to 22.1 GW. Source: Elexon FUELHH. <a class="more" href="#">Open the fuelhh page</a></p>'
            f'</section>')
    bronze_head = (f'<div class="blk sec" style="top: {Y["b_head"]}px; left: 80px; width: 560px">'
                   f'<h2 id="cat-h">Seven feeds, one warehouse</h2>'
                   f'<p>Raw API responses land in bronze, append-only and SHA-256 hashed. Each cable below ends at the '
                   f'vendor that publishes data on that part of the system.</p>'
                   f'<p><a class="more" href="#">Full catalogue</a></p></div>')
    vendors = "\n".join(vendor_block(k) for k in DOM_ORDER)
    bronze_note = (f'<p class="blk note" style="top: {Y["r2"] + 4}px; left: 80px; width: 236px">Each line is one dataset: '
                   f'the mean across the rows it returns per timestamp, 1 to 5 August 2026 unless marked, downsampled.</p>')
    silver = (f'<div class="blk sec" style="top: {Y["s_head"]}px; left: 80px; width: 620px">'
              f'<h2>Cleaned, typed, deduped tables live in silver</h2>'
              f'<p>Everything is Hive-partitioned Parquet, queryable from DuckDB or the Python client. Backfills are '
              f'idempotent. Schema changes are caught at parse time by Pydantic v2 contracts. Bitemporal: every row '
              f'carries both event-time and ingestion-time, so point-in-time queries are trivial.</p>'
              f'<p><a class="more" href="#">Read the design doc</a></p></div>'
              f'<div class="blk" style="top: {ST_Y0}px; left: {ST_X}px; width: 412px">'
              f'<ul class="tables" aria-label="Silver tables">{"".join(f"<li>{t}</li>" for t in SILVER_T)}</ul></div>')
    gold = (f'<div class="blk sec" style="top: {Y["c_sg"] + 52}px; left: 836px; width: 524px">'
            f'<h2>Gold data is cleaned, joined and ready to use</h2>'
            f'<p>Served as DuckDB views.</p></div>'
            f'<div class="blk" style="top: {Y["views"] + 6}px; left: 0px; width: 800px; height: 60px">'
            f'<ul class="views" aria-label="Gold views">'
            + "".join(f'<li style="left: {gx}px">{t}</li>' for gx, t in zip(GV_X, GOLD_T)) +
            f'</ul></div>')
    research = PURPOSE[purpose]() if purpose != "base" else (f'<section aria-labelledby="why-h">'
                f'<div class="blk why" style="top: {Y["p_head"]}px; left: 80px; width: 640px">'
                f'<h2 id="why-h">A personal research platform for UK and European power markets</h2>'
                f'<p class="intro">The warehouse exists to support quantitative work. The pipeline and the catalogue are '
                f'the means; the models are the point.</p></div>'
                f'<div class="blk why-body" style="top: {Y["p_head"] + 10}px; left: 792px; width: 516px">'
                f'<p>Probabilistic estimators live in <code>gridflow-models</code>, a sibling repository: one LightGBM '
                f'model per quantile, walk-forward validated, artifact-pinned to the data fingerprint that trained them.</p>'
                f'<p class="aim">The aim is a price forecast: the input that trading research starts from.</p></div>'
                f'{model_blocks()}'
                f'<p class="blk foot" style="top: {Y["tree"] + SMP_TOP + 250}px; left: {SMP_X}px; width: {SMP_W}px">Every '
                f'model on this site is a function of the catalogue. Inputs are linked. Code is on GitHub. Caveats are '
                f'stated.</p></section>')
    query = wb_notebook()
    skills = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in SKILLS)
    about = (f'<section class="blk about" id="about" aria-labelledby="about-h" style="top: {Y["about"]}px; left: 80px; width: 1280px">'
             f'<div style="display: grid; grid-template-columns: minmax(0,1fr) 520px; gap: 96px; align-items: start">'
             f'<div><h2 id="about-h">Elliot Bentham</h2><p class="role">Quantitative Developer, London, UK</p>'
             f'<p class="intro">Gridflow is a personal research platform for UK and European power markets: a medallion '
             f'data pipeline, vendor catalogue and probabilistic modelling stack.</p>'
             f'<p class="body">I’m a quantitative developer at ICBCS working across FICC, with prior experience in European '
             f'power and gas research at RISQ and FX options pricing at Bank of America Merrill Lynch. Gridflow integrates '
             f'data from Elexon, ENTSO-E, ENTSO-G and weather sources, with a React + TypeScript front-end over the '
             f'analytics layer. Developed to support my own research in energy markets, including power stack modelling, '
             f'as well as to develop fluency in agentic AI development workflows.</p>'
             f'<div class="links"><a class="primary" href="#">GitHub</a><a href="#">LinkedIn</a><a href="#">CV (PDF)</a>'
             f'<a href="#">Email</a></div></div>'
             f'<div class="skills"><h3>Skills</h3><dl>{skills}</dl></div></div></section>')

    body = "\n".join([bg, land, cables, nav,
                      '<main>', hero, key_block(), core, research,
                      f'<section aria-labelledby="cat-h">{bronze_head}{vendors}{bronze_note}</section>',
                      silver, gold, query, about, '</main>'])
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Above ground, below ground</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{FONTS}
<style>
{CSS}{PCSS.get(purpose, "")}</style>
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


def static(dc: str) -> str:
    s = dc.replace('<script src="./support.js"></script>', "")
    s = re.sub(r"</?x-dc>", "", s)
    s = re.sub(r"</?helmet>", "", s)
    s = re.sub(r"<script type=\"text/x-dc\".*?</script>\n", "", s, flags=re.S)
    return s


# ================================================================ v4: the purpose-section variants
PURPOSE: dict = {}
PCSS: dict = {}
from statistics import NormalDist  # noqa: E402

# Real values: only the demand fan. gold/forecasts, model_slug=day_ahead_lgbm_demand_v1, run a55a829bc51c40b2
# (walk-forward fold 12, issued 12:00 UTC the day before), settlement dates 1 to 5 Aug 2026, extracted to
# demand_fan.json. Wind and solar have no stored predictions and the stack's costs are placeholder
# assumptions (cost_provenance: zero_fuel, synthetic carbon), so every other drawing is schematic, unscaled.
FAN = json.loads((HERE / "demand_fan.json").read_text(encoding="utf-8"))

WHY_H2 = "A personal research platform for UK and European power markets"
INTRO = ("The warehouse exists to support quantitative work. The pipeline and the catalogue are the means; "
         "the models are the point.")
AIM = "The aim is a price forecast: the input that trading research starts from."
CASE = '<a class="more" href="#">See the case study</a>'
MID = {"demand": "day_ahead.lgbm_demand.v1", "wind": "wind.lgbm_quantile.v1", "solar": "solar.lgbm_quantile.v1",
       "stack": "stack.gb.v1", "smp": "fundamentals_smp.gb.v1"}
BUILD = "<code>GBStackModel.build(as_of)</code> returns a <code>SupplyCurve</code>"
WIND_D, SOLAR_D = "#2B6B75", "#7E9230"   # darker shades of horizon and chartreuse, for median lines only

# The schematic merit order. Tranche order is the order stack.gb.v1 returns (biomass, nuclear, CCGT, coal,
# OCGT; pumped storage and interconnectors are netted out of demand, not stacked). Widths and heights are drawn.
TRANCHES = [  # name, share of capacity, unit costs on a 0..1 drawn scale, fill, pattern
    ("Biomass", .07, [.05, .07], CHART, "bio"),
    ("Nuclear", .15, [.08, .10], PETROL, None),
    ("CCGT", .56, [.28, .30, .32, .335, .35, .37, .39, .41, .43, .46, .49, .52], CLAY, "gas"),
    ("Coal", .12, [.61, .65], KHAKI, "coal"),
    ("OCGT", .10, [.80, .92], CLAY, "ocgt"),
]
PAT_OP = {"gas": ".22", "ocgt": ".4", "bio": ".3", "coal": ".35"}
RD = NormalDist(.62, .1)   # the drawn residual-demand distribution, in capacity units


def _units() -> list[tuple[float, float, float, int]]:
    out, x = [], 0.0
    for i, (_, share, costs, _, _) in enumerate(TRANCHES):
        w = share / len(costs)
        for c in costs:
            out.append((x, x + w, c, i))
            x += w
    return out


UNITS = _units()


def cost_at(q: float) -> float:
    for _, x1, c, _ in UNITS:
        if q < x1:
            return c
    return UNITS[-1][2]


def draws(n: int) -> list[float]:
    return [min(max(RD.inv_cdf((k + .5) / n), .23), .895) for k in range(n)]


def pat_defs(p: str) -> str:
    return (f'<pattern id="{p}-gas" width="7" height="7" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r=".9" '
            f'fill="{INK}"></circle><circle cx="5.5" cy="5.5" r=".7" fill="{INK}"></circle></pattern>'
            f'<pattern id="{p}-ocgt" width="6" height="6" patternUnits="userSpaceOnUse"><path d="M0 6 L6 0" '
            f'stroke="{INK}" stroke-width=".9"></path></pattern>'
            f'<pattern id="{p}-bio" width="10" height="8" patternUnits="userSpaceOnUse"><path d="M1 2 l3 1 M6 6 l3 -1" '
            f'stroke="{INK}" stroke-width=".8"></path></pattern>'
            f'<pattern id="{p}-coal" width="8" height="8" patternUnits="userSpaceOnUse"><rect x="1" y="1" width="2.2" '
            f'height="2.2" fill="{INK}"></rect><rect x="5" y="5" width="1.8" height="1.8" fill="{INK}"></rect></pattern>')


def stack_draw(p: str, x0: float, base: float, w: float, h: float, lab: float = 0, joints_on: bool = True) -> str:
    """Tranche blocks from the axis up to each unit's cost, unit joints, tranche contacts, the stepped curve."""
    out, joints, contacts = [], [], []
    for k, (ux0, ux1, c, i) in enumerate(UNITS):
        _, _, _, fill, pat = TRANCHES[i]
        a, b, top = x0 + ux0 * w, x0 + ux1 * w, base - c * h
        out.append(f'<rect x="{f(a)}" y="{f(top)}" width="{f(b - a + .4)}" height="{f(base - top)}" fill="{fill}"></rect>')
        if pat:
            out.append(f'<rect x="{f(a)}" y="{f(top)}" width="{f(b - a + .4)}" height="{f(base - top)}" '
                       f'fill="url(#{p}-{pat})" opacity="{PAT_OP[pat]}"></rect>')
        if k:
            (joints if UNITS[k - 1][3] == i else contacts).append(f"M{f(a)} {f(base)} V{f(base - UNITS[k - 1][2] * h)}")
    if joints_on:
        out.append(f'<path d="{" ".join(joints)}" stroke="{T_TOP}" stroke-width="1" opacity=".75"></path>')
    out.append(f'<path d="{" ".join(contacts)}" stroke="{INK}" stroke-width="1"></path>')
    d = f"M{f(x0)} {f(base - UNITS[0][2] * h)}"
    for ux0, ux1, c, _ in UNITS:
        d += f" V{f(base - c * h)} H{f(x0 + ux1 * w)}"
    out.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="2" stroke-linejoin="round"></path>')
    if lab:
        t, acc = [], 0.0
        for name, share, _, fill, _ in TRANCHES:
            col = DAY if fill == PETROL else INK
            t.append(f'<text x="{f(x0 + acc * w + 7)}" y="{f(base - 9)}" fill="{col}">{name}</text>')
            acc += share
        out.append(f'<g font-family="Hanken Grotesk" font-style="italic" font-size="{lab}">{"".join(t)}</g>')
    return "".join(out)


def band(xs: list[float], lo: list[float], hi: list[float]) -> str:
    up = " L".join(f"{f(x)} {f(y)}" for x, y in zip(xs, hi))
    dn = " L".join(f"{f(x)} {f(y)}" for x, y in zip(reversed(xs), reversed(lo)))
    return f"M{up} L{dn} Z"


def line(xs: list[float], ys: list[float]) -> str:
    return "M" + " L".join(f"{f(x)} {f(y)}" for x, y in zip(xs, ys))


def head_block(right: str, left_extra: str = "") -> str:
    T = Y["p_head"]
    return (f'<div class="blk why" style="top: {T}px; left: 80px; width: 640px">'
            f'<h2 id="why-h">{WHY_H2}</h2>{left_extra}</div>'
            f'<div class="blk why-r" style="top: {T + 12}px; left: 792px; width: 516px">{right}</div>')


# ---------------------------------------------------------------- P1: the stack
P1_TOP = Y["p_head"] + 170    # the drawing, page y
P1_W, P1_H = 1230, 734
PX, SW, BY, PH = 250, 940, 454, 400     # price axis x, stack width, capacity axis y, cost height
ROWS = {"r": BY + 58, "s": BY + 106, "w": BY + 154, "d": BY + 202}


def p1() -> str:
    x = lambda q: PX + q * SW  # noqa: E731
    g = [f'<defs>{pat_defs("p1")}</defs>']
    # the Monte Carlo: residual-demand draws rise through the stack and read off a price
    mc_in, mc_out, mc_low = [], [], []
    for q in draws(13):
        X, top = x(q), BY - cost_at(q) * PH
        mc_low.append(f"M{f(X)} {ROWS['r'] - 9} V{BY}")
        mc_in.append(f"M{f(X)} {BY} V{f(top)}")
        mc_out.append(f"M{f(X)} {f(top)} H{PX}")
    g.append(stack_draw("p1", PX, BY, SW, PH, lab=14))
    g.append(f'<path d="{" ".join(mc_in)}" stroke="{DAY}" stroke-width="1.4"></path>')
    g.append(f'<path d="{" ".join(mc_out)}" stroke="{INK}" stroke-width="1" stroke-dasharray="2 3" opacity=".6"></path>')
    g.append(f'<path d="{" ".join(mc_low)}" stroke="{INK}" stroke-width="1" opacity=".5"></path>')
    g.append(f'<g fill="{INK}">' + "".join(f'<circle cx="{f(x(q))}" cy="{f(BY - cost_at(q) * PH)}" r="2.6"></circle>'
                                           for q in draws(13)) + '</g>')
    # the price distribution, built on the price axis from many more draws of the same curve
    bins = [0] * 50
    for q in draws(4000):
        bins[min(int(cost_at(q) * 50), 49)] += 1
    mx = max(bins)
    bars = "".join(f'<rect x="{f(PX - 2 - n / mx * 118)}" y="{f(BY - (b + 1) * PH / 50 + .5)}" width="{f(n / mx * 118)}" '
                   f'height="{f(PH / 50 - 1)}"></rect>' for b, n in enumerate(bins) if n)
    g.append(f'<g fill="{GOLD}" stroke="{INK}" stroke-width=".8">{bars}</g>')
    # axes, no scales
    g.append(f'<path d="M{PX} {BY} V64 M{PX} {BY} H{PX + SW + 14}" stroke="{INK}" stroke-width="1.5" fill="none"></path>')
    g.append(f'<g font-family="Hanken Grotesk" font-style="italic" font-size="14" fill="{INK}">'
             f'<text x="{PX + 10}" y="72">price</text>'
             f'<text x="{PX + SW + 14}" y="{BY + 24}" text-anchor="end">capacity, cheapest first</text></g>')
    # the inputs, read from the bottom: demand, less wind, less solar, leaves residual demand
    xr = x(RD.mean)
    ws, ss, ds = .24 * SW, .10 * SW, .035 * SW
    xd = xr + ws + ss
    z = NormalDist().inv_cdf

    def fanrow(cx: float, sd: float, y: float, fill: str) -> str:
        o, i = 1.645 * sd, .674 * sd
        return (f'<rect x="{f(cx - o)}" y="{y - 7}" width="{f(2 * o)}" height="14" fill="{fill}" opacity=".35"></rect>'
                f'<rect x="{f(cx - i)}" y="{y - 7}" width="{f(2 * i)}" height="14" fill="{fill}" opacity=".75"></rect>'
                f'<path d="M{f(cx)} {y - 11} V{y + 11}" stroke="{INK}" stroke-width="2"></path>')

    def bar(a: float, b: float, y: float, fill: str, whisk: float) -> str:
        return (f'<path d="M{f(b - whisk)} {y} H{f(b + whisk)} M{f(b - whisk)} {y - 5} V{y + 5} M{f(b + whisk)} {y - 5} '
                f'V{y + 5}" stroke="{INK}" stroke-width="1.2"></path>'
                f'<rect x="{f(b)}" y="{y - 7}" width="{f(a - b)}" height="14" fill="{fill}" stroke="{INK}" '
                f'stroke-width="1.2"></rect>'
                f'<path d="M{f(b + 10)} {y - 7} L{f(b)} {y} L{f(b + 10)} {y + 7}" fill="none" stroke="{INK}" '
                f'stroke-width="1.2"></path>')

    g.append(fanrow(xr, RD.stdev * SW, ROWS["r"], OLIVE))
    g.append(bar(xr + ss, xr, ROWS["s"], CHART, 20))
    g.append(bar(xd, xr + ss, ROWS["w"], HORIZON, 44))
    g.append(fanrow(xd, ds, ROWS["d"], OLIVE))
    g.append(f'<path d="M{f(xd)} {ROWS["d"] - 12} V{ROWS["w"] + 8} M{f(xr + ss)} {ROWS["w"] - 8} V{ROWS["s"] + 8} '
             f'M{f(xr)} {ROWS["s"] - 8} V{ROWS["r"] + 12}" stroke="{INK}" stroke-width="1" stroke-dasharray="1.5 3"></path>')
    _ = z
    aria = ("How the price forecast is assembled, drawn without scales. A merit-order supply curve rises in steps "
            "from left to right: biomass, nuclear, a long run of CCGT units, coal, then OCGT. Below the capacity axis, "
            "the demand forecast band, less the wind forecast and the solar forecast, leaves a residual demand band. "
            "Thirteen Monte Carlo draws of residual demand rise through the stack; each meets the curve and reads "
            "off a price, and a histogram of prices builds up on the price axis.")
    svg = (f'<svg width="{P1_W}" height="{P1_H}" viewBox="0 0 {P1_W} {P1_H}" role="img" aria-label="{aria}">'
           + "".join(g) + "</svg>")

    def lab(left: float, top: float, width: float, html: str, right: bool = False) -> str:
        cls = "p1-l p1-r" if right else "p1-l"
        return f'<div class="{cls}" style="left: {f(left)}px; top: {f(top)}px; width: {f(width)}px">{html}</div>'

    L = [
        lab(0, 8, 226, f'<p class="p1-t">Fundamentals SMP forecaster</p><p class="p1-id">{MID["smp"]}</p>'
                       '<p class="p1-d">Monte Carlo draws of residual demand, each cleared against the curve, build a '
                       'price distribution. Backtested against ENTSO-E day-ahead prices.</p>'),
        lab(496, 44, 380, f'<p class="p1-t">Merit-order supply curve</p><p class="p1-id">{MID["stack"]}</p>'
                          f'<p class="p1-d">{BUILD}: GB plant in merit order, cheapest first.</p>'),
        lab(xr - 1.645 * RD.stdev * SW - 14 - 300, ROWS["r"] - 21, 300,
            '<p class="p1-n">Residual demand</p><p class="p1-d">Demand less wind and solar</p>', True),
        lab(xr - 20 - 12 - 300, ROWS["s"] - 20, 300,
            f'<p class="p1-n">Solar generation</p><p class="p1-id">{MID["solar"]}</p>', True),
        lab(xr + ss - 44 - 12 - 300, ROWS["w"] - 20, 300,
            f'<p class="p1-n">Wind generation</p><p class="p1-id">{MID["wind"]}</p>', True),
        lab(xd - 1.645 * ds - 12 - 300, ROWS["d"] - 20, 300,
            f'<p class="p1-n">Day-ahead demand</p><p class="p1-id">{MID["demand"]}</p><p class="p1-d">{CASE}</p>', True),
        lab(0, BY + 12, 226, '<p class="p1-cap">An illustration of the method, drawn without scales.</p>'),
    ]
    right = f'<p class="intro">{INTRO}</p><p class="aim">{AIM}</p>'
    return (f'<section class="p1" aria-labelledby="why-h">{head_block(right)}'
            f'<div class="blk p1-draw" style="top: {P1_TOP}px; left: 80px; width: {P1_W}px; height: {P1_H}px">'
            f'{svg}{"".join(L)}</div></section>')


P1_CSS = """.why-r .intro{margin:0 0 14px;font-size:21px;line-height:1.5;color:#1C2B22}
.why-r .aim{margin:0;font-size:16px;line-height:1.6;font-weight:600;color:#1C2B22}
.p1-draw svg{display:block}
.p1-l{position:absolute}
.p1-r{text-align:right}
.p1-t{margin:0 0 5px;font-family:"Bricolage Grotesque",sans-serif;font-size:21px;font-weight:700;font-stretch:90%;line-height:1.08;letter-spacing:-.005em;color:#1C2B22}
.p1-n{margin:0;font-weight:600;font-size:15.5px;line-height:1.3;color:#1C2B22}
.p1-id{margin:1px 0 0;font:400 13px/1.4 "Red Hat Mono",monospace;color:#155A6E}
.p1-d{margin:4px 0 0;font-size:14px;line-height:1.45;color:#3F4A3B}
.p1-d code{font-size:12.5px;color:#1C2B22}
.p1-cap{margin:0;font-size:14px;color:#3F4A3B}
.p1 .more{font-weight:600;color:#1C2B22;text-decoration-color:#66793B}
"""


# ---------------------------------------------------------------- P2: the questions
def glyph(kind: str) -> str:
    w, h, b = 104, 52, 46
    o = []
    if kind == "demand":
        xs = [4 + i * 3 for i in range(33)]
        m = [b - 20 - 10 * math.sin(i / 5.2) for i in range(33)]
        s = [5 + i * .18 for i in range(33)]
        o.append(f'<path d="{band(xs, [a + e for a, e in zip(m, s)], [a - e for a, e in zip(m, s)])}" fill="{OLIVE}" '
                 f'opacity=".35"></path><path d="{line(xs, m)}" fill="none" stroke="{OLIVE}" stroke-width="1.8"></path>')
    elif kind == "ws":
        xs = [4 + i * 3 for i in range(33)]
        m = [b - 26 - 7 * math.sin(i / 3.6 + .6) for i in range(33)]
        o.append(f'<path d="{band(xs, [a + 4 + i * .15 for i, a in enumerate(m)], [a - 4 - i * .15 for i, a in enumerate(m)])}" '
                 f'fill="{HORIZON}" opacity=".35"></path><path d="{line(xs, m)}" fill="none" stroke="{WIND_D}" '
                 f'stroke-width="1.8"></path>')
        sx = [4 + i * 3 for i in range(33)]
        sv = [max(0.0, math.sin((i - 6) / 21 * math.pi)) ** 1.4 * 20 if 6 <= i <= 27 else 0 for i in range(33)]
        o.append(f'<path d="{band(sx, [b - v * .75 for v in sv], [b - v * 1.2 for v in sv])}" fill="{CHART}" opacity=".7"></path>'
                 f'<path d="{line(sx, [b - v for v in sv])}" fill="none" stroke="{SOLAR_D}" stroke-width="1.8"></path>')
    elif kind == "stack":
        o.append(f'<defs>{pat_defs("g3")}</defs>' + stack_draw("g3", 4, b, 96, 40, joints_on=False))
    else:
        n = [2, 4, 7, 12, 17, 19, 16, 11, 7, 5, 3, 2, 4, 3, 1]
        o.append(f'<g fill="{GOLD}" stroke="{INK}" stroke-width=".8">' + "".join(
            f'<rect x="{6 + i * 6.2:.1f}" y="{b - v * 2}" width="5.4" height="{v * 2}"></rect>' for i, v in enumerate(n))
            + "</g>")
    o.append(f'<path d="M2 {b} H{w - 2}" stroke="{INK}" stroke-width="1.2"></path>')
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" aria-hidden="true">{"".join(o)}</svg>'


QUESTIONS = [
    ("How much power will Great Britain need tomorrow, and how sure can we be?", ["demand"],
     f"Seven quantiles, p05 to p95, for each half-hour of the next day, from one LightGBM model per quantile. {CASE}",
     "demand"),
    ("How much will the wind and the sun supply?", ["wind", "solar"],
     "The same quantile method on wind and solar output, with Open-Meteo weather features. Solar is held at zero "
     "overnight.", "ws"),
    ("Where does the supply stack clear?", ["stack"],
     f"{BUILD}: GB plant in merit order, cheapest first. Residual demand, which is demand less wind and solar, sets "
     "where it clears.", "stack"),
    ("What will the price be, and how wide is the range?", ["smp"],
     "A Monte Carlo over residual demand and the supply curve gives a price distribution, backtested against ENTSO-E "
     "day-ahead prices.", "hist"),
]


def p2() -> str:
    T = Y["p_head"]
    rows = "".join(
        f'<li><h3>{q}</h3><div class="p2-a">{glyph(gk)}<div><p class="p2-id">'
        + "".join(f"<code>{MID[k]}</code>" for k in ids) + f'</p><p class="p2-t">{a}</p></div></div></li>'
        for q, ids, a, gk in QUESTIONS)
    return (f'<section class="p2" aria-labelledby="why-h">'
            f'<div class="blk p2-side" style="top: {T}px; left: 80px; width: 404px">'
            f'<h2 id="why-h">{WHY_H2}</h2><p class="intro">{INTRO}</p><p class="aim">{AIM}</p></div>'
            f'<ul class="blk p2-q" aria-label="What the models answer" style="top: {T + 6}px; left: 560px; width: 750px">'
            f'{rows}</ul></section>')


P2_CSS = """.p2-side h2{font-size:46px;font-weight:740;font-stretch:84%;line-height:1.02;letter-spacing:-.02em;margin:0 0 24px}
.p2-side .intro{margin:0 0 16px;font-size:19px;line-height:1.5;color:#1C2B22}
.p2-side .aim{margin:0;font-size:16px;line-height:1.6;font-weight:600;color:#1C2B22}
.p2-q{list-style:none;margin:0;padding:0;border-bottom:1px solid rgba(28,43,34,.3)}
.p2-q li{padding:30px 0 34px;border-top:1px solid rgba(28,43,34,.3)}
.p2-q h3{margin:0 0 16px;font-size:32px;font-weight:680;font-stretch:88%;line-height:1.1;letter-spacing:-.012em;color:#1C2B22}
.p2-a{display:grid;grid-template-columns:104px minmax(0,1fr);column-gap:22px;align-items:start}
.p2-a svg{display:block;margin-top:2px}
.p2-id{margin:0 0 3px;display:flex;flex-wrap:wrap;gap:4px 18px}
.p2-id code{font-size:13.5px;color:#155A6E}
.p2-t{margin:0;font-size:16px;line-height:1.55;color:#3F4A3B;max-width:56ch}
.p2-t code{font-size:13.5px;color:#1C2B22}
.p2 .more{font-weight:600;color:#1C2B22;text-decoration-color:#66793B}
"""


# ---------------------------------------------------------------- P3: specimens
SW3, SH3 = 390, 176                  # specimen plot size
PL, PR, PT, PB = 38, 8, 12, 26      # plot insets
P3_TOP = Y["p_head"] + 214
P3_ROW = 340


def frame(xt: str, yt: str) -> tuple[list[str], float, float, float, float]:
    x0, x1, y0, y1 = PL, SW3 - PR, PT, SH3 - PB
    o = [f'<path d="M{x0} {y0 - 4} V{y1} H{x1}" fill="none" stroke="{INK}" stroke-width="1.2"></path>',
         f'<g font-family="Hanken Grotesk" font-style="italic" font-size="13" fill="{SOFT}">'
         f'<text x="{x0 + 8}" y="{y0 + 6}">{yt}</text>'
         f'<text x="{x1}" y="{y1 + 19}" text-anchor="end">{xt}</text></g>']
    return o, x0, x1, y0, y1


def spec_svg(o: list[str], aria: str) -> str:
    return (f'<svg width="{SW3}" height="{SH3}" viewBox="0 0 {SW3} {SH3}" role="img" aria-label="{aria}">'
            + "".join(o) + "</svg>")


def sp_demand() -> str:
    x0, x1, y0, y1 = PL, SW3 - PR, PT, SH3 - PB
    lo_gw, hi_gw = 12.0, 32.0
    n = len(FAN["actual"])
    xs = [x0 + 2 + i * (x1 - x0 - 4) / (n - 1) for i in range(n)]
    Yv = lambda mw: y1 - (mw / 1000 - lo_gw) / (hi_gw - lo_gw) * (y1 - y0)  # noqa: E731
    col = {k: [Yv(v) for v in FAN[k]] for k in ["q_0.05", "q_0.25", "q_0.5", "q_0.75", "q_0.95", "actual"]}
    o = [f'<path d="{band(xs, col["q_0.05"], col["q_0.95"])}" fill="{OLIVE}" opacity=".26"></path>',
         f'<path d="{band(xs, col["q_0.25"], col["q_0.75"])}" fill="{OLIVE}" opacity=".5"></path>',
         f'<path d="{line(xs, col["actual"])}" fill="none" stroke="{INK}" stroke-width="1.2" stroke-linejoin="round"></path>']
    ticks = "".join(f'<text x="{x0 - 7}" y="{f(Yv(g * 1000) + 4)}" text-anchor="end">{g}</text>' for g in (15, 20, 25, 30))
    tm = " ".join(f"M{x0 - 4} {f(Yv(g * 1000))} H{x0}" for g in (15, 20, 25, 30))
    per = (x1 - x0 - 4) / 5
    days = "".join(f'<text x="{f(x0 + 2 + per * (k + .5))}" y="{y1 + 17}" text-anchor="middle">{k + 1} Aug</text>'
                   for k in range(5))
    dm = " ".join(f"M{f(x0 + 2 + per * k)} {y1} V{y1 + 4}" for k in range(1, 5))
    o += [f'<path d="M{x0} {y0 - 4} V{y1} H{x1} {tm} {dm}" fill="none" stroke="{INK}" stroke-width="1.2"></path>',
          f'<g font-family="Hanken Grotesk" font-size="12.5" fill="{SOFT}">{ticks}{days}</g>',
          f'<text x="{x0 + 8}" y="{y0 + 6}" font-family="Hanken Grotesk" font-style="italic" font-size="13" '
          f'fill="{SOFT}">GW</text>']
    aria = ("Day-ahead demand forecast from a walk-forward backtest fold of day_ahead.lgbm_demand.v1, 1 to 5 August "
            "2026, 240 half-hours: a p05 to p95 band from about 14 to 31 GW with an inner p25 to p75 band, and the "
            "realised demand line, which leaves the outer band for part of 5 August.")
    return spec_svg(o, aria)


def _fan_ill(xs: list[float], m: list[float], s: list[float], fill: str, dark: str) -> list[str]:
    return [f'<path d="{band(xs, [a + e for a, e in zip(m, s)], [a - e for a, e in zip(m, s)])}" fill="{fill}" opacity=".3"></path>',
            f'<path d="{band(xs, [a + e * .45 for a, e in zip(m, s)], [a - e * .45 for a, e in zip(m, s)])}" fill="{fill}" '
            f'opacity=".55"></path>',
            f'<path d="{line(xs, m)}" fill="none" stroke="{dark}" stroke-width="1.6" stroke-linejoin="round"></path>']


def sp_wind() -> str:
    o, x0, x1, y0, y1 = frame("time ahead", "output")
    n = 97
    xs = [x0 + 2 + i * (x1 - x0 - 4) / (n - 1) for i in range(n)]
    hgt = y1 - y0
    m = [y1 - hgt * (.52 + .2 * math.sin(i / 11 + .3) + .08 * math.sin(i / 4.1 + 1.2) - .12 * (i / n)) for i in range(n)]
    s = [hgt * (.07 + .17 * i / n) for i in range(n)]
    s = [min(e, y1 - a - 1, a - y0 + 6) for a, e in zip(m, s)]
    return spec_svg(_fan_ill(xs, m, s, HORIZON, WIND_D) + o,
                    "Illustration of a probabilistic wind forecast: a median line inside quantile bands that widen "
                    "with time ahead. No scale.")


def sp_solar() -> str:
    o, x0, x1, y0, y1 = frame("three days", "output")
    n = 145
    xs = [x0 + 2 + i * (x1 - x0 - 4) / (n - 1) for i in range(n)]
    hgt = y1 - y0
    amp = [.86, .55, .74]
    m, s = [], []
    for i in range(n):
        d, p = divmod(i, 48)
        d = min(d, 2)
        v = math.sin((p - 11) / 29 * math.pi) ** 1.3 if 11 <= p <= 40 else 0.0
        m.append(y1 - hgt * amp[d] * v)
        s.append(hgt * .22 * v)
    zero = [(xs[i], xs[j]) for i, j in ((0, 10), (41, 58), (89, 106), (137, 144))]
    zl = " ".join(f"M{f(a)} {y1 - 1.5} H{f(b)}" for a, b in zero)
    o2 = _fan_ill(xs, m, s, CHART, SOLAR_D)
    o2.append(f'<path d="{zl}" stroke="{SOLAR_D}" stroke-width="3" stroke-linecap="round"></path>')
    return spec_svg(o2 + o, "Illustration of a probabilistic solar forecast over three days: daytime humps with "
                             "quantile bands that collapse to exactly zero overnight. No scale.")


def sp_stack() -> str:
    o, x0, x1, y0, y1 = frame("capacity", "cost")
    body = f'<defs>{pat_defs("p3")}</defs>' + stack_draw("p3", x0, y1, x1 - x0, y1 - y0 - 8)
    return spec_svg([body] + o, "Illustration of a merit-order supply curve: stepped tranches, cheapest first: "
                                "biomass, nuclear, a long run of CCGT units, coal, then OCGT. No scale.")


def sp_smp() -> str:
    o, x0, x1, y0, y1 = frame("price", "draws")
    nb = 20
    bins = [0] * nb
    ds = draws(4000)
    for q in ds:
        bins[min(int(cost_at(q) / .8 * nb), nb - 1)] += 1
    mx = max(bins)
    bw = (x1 - x0 - 8) / nb
    hgt = y1 - y0 - 18
    bars = "".join(f'<rect x="{f(x0 + 4 + b * bw)}" y="{f(y1 - n / mx * hgt)}" width="{f(bw - 1)}" height="{f(n / mx * hgt)}">'
                   f'</rect>' for b, n in enumerate(bins) if n)
    body = f'<g fill="{GOLD}" stroke="{INK}" stroke-width=".8">{bars}</g>'
    return spec_svg([body] + o, "Illustration of the SMP forecaster's output: a histogram of Monte Carlo price draws, "
                                "bunched where the supply curve is flat, with a small upper tail. No scale.")


SPECIMENS = [
    ("Day-ahead demand, GB", "demand", sp_demand,
     f"Walk-forward backtest fold, 1 to 5 August 2026, issued at noon the day before. Bands p05 to p95 and p25 "
     f"to p75; line: realised demand (Elexon INDO). {CASE}"),
    ("Wind generation, GB", "wind", sp_wind, "Quantile bands around the median, with Open-Meteo wind-speed features."),
    ("Solar generation, GB", "solar", sp_solar, "The same method with irradiance features, held at zero overnight."),
    ("Merit-order supply curve", "stack", sp_stack,
     f"{BUILD}. Biomass, nuclear, CCGT, coal and OCGT, cheapest first."),
    ("Fundamentals SMP forecaster", "smp", sp_smp,
     "Monte Carlo over residual demand and the supply curve, backtested against ENTSO-E day-ahead prices."),
]


def p3() -> str:
    cols = [80, 500, 920]
    cells = []
    order = [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2)]
    for (title, key, fn, cap), (r, c) in zip(SPECIMENS, order):
        cells.append(f'<figure class="blk p3-s" style="top: {P3_TOP + r * P3_ROW}px; left: {cols[c]}px; width: {SW3}px">'
                     f'<h3>{title}</h3><p class="p3-id">{MID[key]}</p>{fn()}<figcaption>{cap}</figcaption></figure>')
    cells.insert(3, f'<div class="blk p3-x" style="top: {P3_TOP + P3_ROW}px; left: 80px; width: {SW3 - 30}px">'
                    '<p>Residual demand is the demand forecast less the wind and solar forecasts. The SMP forecaster '
                    'samples it, clears each draw against the supply curve and collects the prices.</p></div>')
    right = (f'<p class="intro">{INTRO}</p><p class="key">The demand panel is real output. The other four '
             f'draw each method without a scale.</p>')
    return (f'<section class="p3" aria-labelledby="why-h">{head_block(right)}{"".join(cells)}</section>')


P3_CSS = """.why-r .intro{margin:0 0 14px;font-size:21px;line-height:1.5;color:#1C2B22}
.why-r .key{margin:0;font-size:15px;line-height:1.55;color:#3F4A3B}
.p3-s{margin:0}
.p3-s h3{margin:0;font-size:21px;font-weight:700;font-stretch:90%;line-height:1.15;letter-spacing:-.005em;color:#1C2B22}
.p3-id{margin:2px 0 12px;font:400 13px/1.4 "Red Hat Mono",monospace;color:#155A6E}
.p3-s svg{display:block}
.p3-s figcaption{margin:8px 0 0;font-size:13.5px;line-height:1.5;color:#3F4A3B}
.p3-s figcaption code{font-size:12.5px;color:#1C2B22}
.p3-x p{margin:0;padding-top:12px;border-top:1.5px solid #1C2B22;font-size:17px;line-height:1.55;color:#1C2B22}
.p3 .more{font-weight:600;color:#1C2B22;text-decoration-color:#66793B}
"""

PURPOSE.update({"P1": p1, "P2": p2, "P3": p3})
PCSS.update({"P1": P1_CSS, "P2": P2_CSS, "P3": P3_CSS})


if __name__ == "__main__":
    (HERE / "static").mkdir(exist_ok=True)
    for v in ["base"] + sorted(PURPOSE):
        out = page(v)
        body_only = out.split("<script type=\"text/x-dc\"")[0]
        assert "{{" not in body_only and "}}" not in body_only, "template-hole syntax in markup"
        assert "/>" not in re.sub(r"<(meta|link|br)[^>]*>", "", body_only), "self-closing tag"
        (HERE / f"R3-v4-{v}.dc.html").write_text(out, encoding="utf-8")
        (HERE / "static" / f"R3-v4-{v}.html").write_text(static(out), encoding="utf-8")
    print("H =", H, {k: v for k, v in Y.items()})
