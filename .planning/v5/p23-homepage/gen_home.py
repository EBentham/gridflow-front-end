"""Phase 23: build site/hifi/index.html and the generated tail of site/hifi/assets/theme.css.

The drawings come from the design-loop generators that produced the locked board R3-final
(.planning/v4/design-loop/r3-6/gen.py and r3-7/gen_b.py; checked byte-identical against R3-final).
This script re-frames them for a reflowing page: a landscape that extends past 1440 and crops on
phones, phone variants of the core sample and the merit-order drawing, and the strata contacts as CSS.
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path
from statistics import NormalDist

WT = Path(r"C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.claude\worktrees\agent-af17b8660dd5506f2")
D = WT / ".planning" / "v4" / "design-loop"
sys.path[:0] = [str(D / "r3-7"), str(D / "r3-6")]
import gen  # noqa: E402
import gen_b  # noqa: E402
from gen import (BRONZE, CHART, CLAY, DAY, GOLD, HORIZON, INK, KHAKI, OLIVE, PETROL, T_TOP,  # noqa: E402
                 f, prof, smooth)

HERE = Path(__file__).parent
REF = (D / "r3-7" / "R3-final.dc.html").read_text(encoding="utf-8")
OUT_HTML = WT / "site" / "hifi" / "index.html"
OUT_CSS = WT / "site" / "hifi" / "assets" / "theme.css"
SOFT = "#3F4A3B"


# ================================================================ landscape, extended to 2240 wide
LX0, LX1 = -420, 1860          # drawn extent; the viewBox is -400..1840 so a 1440 view is centred on x 720
VB_Y0, VB_Y1 = 560, 954


def landscape_wide() -> str:
    """gen.landscape(), with the scenery carried past both edges of the 1440 board."""
    S = gen.Y["surf"]
    parts: list[str] = []
    surf = [(x, prof(x)) for x in range(LX0, LX1 + 1, 20)]
    surf_d = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in surf)
    # the ground below the cut: topsoil, then the olive root band, then the surface line (as the board's
    # background layer did, so the field and fences paint over them in the same order)
    parts.append(f'<path d="{surf_d} L{LX1} {VB_Y1 + 6} L{LX0} {VB_Y1 + 6} Z" fill="{T_TOP}"></path>')
    parts.append(f'<path d="{surf_d} L{LX1} {VB_Y1 + 6} L{LX0} {VB_Y1 + 6} Z" fill="url(#ls-soil)" opacity=".5"></path>')
    root = surf_d + " " + " ".join(f"L{f(x)} {f(y + 9)}" for x, y in reversed(surf)) + " Z"
    parts.append(f'<path d="{root}" fill="{OLIVE}"></path>')
    parts.append(f'<path d="{surf_d}" stroke="{INK}" stroke-width="1.5" fill="none"></path>')
    # sea and offshore wind
    parts.append(f'<rect x="820" y="786" width="{LX1 - 820}" height="80" fill="{HORIZON}"></rect>')
    parts.append(f'<rect x="820" y="786" width="{LX1 - 820}" height="80" fill="{DAY}" opacity=".13"></rect>')
    waves = " ".join(f"M{f(x0)} {f(y0)} h{f(ln)}" for x0, y0, ln in
                     [(960, 796, 40), (1060, 800, 26), (1200, 794, 34), (1330, 799, 44), (1010, 808, 22),
                      (1150, 812, 30), (1270, 806, 18), (1390, 812, 28), (1490, 797, 30), (1600, 803, 38),
                      (1720, 795, 26), (1800, 809, 32), (1540, 811, 20), (1660, 813, 24)])
    parts.append(f'<path d="{waves}" stroke="{DAY}" stroke-width="1" opacity=".35"></path>')
    parts.append(f'<path d="M1150 786 C1210 781 1250 778 1300 778 S1390 775 1440 776 S1640 771 1760 774 '
                 f'S1840 777 {LX1} 776 V786 Z" fill="{HORIZON}" opacity=".6"></path>')
    offshore = [(1090, 30), (1160, 34), (1238, 31), (1312, 36), (1392, 32), (1476, 30), (1556, 33), (1642, 31),
                (1726, 35), (1808, 30)]
    for i, (ox, oh) in enumerate(offshore):
        parts.append(gen.turbine(ox, 804 + (i % 2) * 3, oh, oh * .5, ["sp1", "sp2", "sp3"][i % 3], 17 * i))
    far = [(LX0, 694), (-300, 676), (-160, 702), (-20, 716), (120, 688), (300, 700), (470, 668), (640, 686),
           (790, 712), (880, 760), (940, 800)]
    parts.append(f'<path d="{smooth(far)} L940 880 L{LX0} 880 Z" fill="{HORIZON}" opacity=".5"></path>')
    near = [(LX0, 736), (-300, 716), (-160, 738), (-20, 748), (90, 716), (210, 704), (330, 722), (452, 698),
            (590, 710), (720, 732), (820, 770), (900, 806)]
    parts.append(f'<path d="{smooth(near)} L900 880 L{LX0} 880 Z" fill="{HORIZON}"></path>')
    for i, (tx, ty) in enumerate([(-300, 716), (-160, 738)]):
        hgt = [80, 74][i]
        parts.append(gen.turbine(tx, ty + 3, hgt, hgt * .5, ["sp3", "sp1"][i], 25 * i + 70))
    for i, (tx, ty) in enumerate(near[4:10]):
        hgt = [76, 84, 72, 88, 80, 70][i]
        parts.append(gen.turbine(tx, ty + 3, hgt, hgt * .5, ["sp2", "sp1", "sp3"][i % 3], 40 * i + 10))
    field = [(LX0, 806), (-200, 798), (-20, 802), (160, 792), (340, 804), (520, 796), (700, 808), (880, 818),
             (1060, 834), (1240, 840), (1460, 846), (1660, 850), (LX1, 852)]
    bottom = " ".join(f"L{f(x)} {f(prof(x))}" for x in range(LX1, LX0 - 1, -20))
    parts.append(f'<path d="{smooth(field)} {bottom} Z" fill="{CHART}"></path>')
    bounds = [smooth([(LX0, 824), (-20, 822), (300, 818), (700, 830), (1100, 850), (1460, 858), (LX1, 862)]),
              smooth([(LX0, 854), (-20, 852), (400, 848), (820, 862), (1200, 876), (1460, 880), (LX1, 884)]),
              smooth([(420, 890), (800, 896), (1180, 904), (1460, 906), (LX1, 908)])]
    parts.append(f'<path d="{" ".join(bounds)}" stroke="{OLIVE}" stroke-width="1" fill="none" opacity=".45"></path>')
    parts.append(gen.ccgt(262, 842, 0.82))
    p0, p1, p2, p3 = (-150, 830, 0.46), (150, 836, 0.5), (430, 848, 0.58), (700, 862, 0.66)
    sub_x, sub_s = 866, 1.28
    sub_base = prof(sub_x + 50)
    sub_svg, sub_ends = gen.substation(sub_x, sub_base)
    sub_svg = gen.sc(sub_svg, sub_x, sub_base, sub_s)
    sub_ends = [(sub_x + (ex - sub_x) * sub_s, sub_base + (ey - sub_base) * sub_s) for ex, ey in sub_ends]
    wires = [
        gen.spans([(LX0, 778), (LX0, 764), (LX0, 754)], gen.tips(*p0, -1), 8),
        gen.spans(gen.tips(*p0, 1), gen.tips(*p1, -1), 10),
        gen.spans(gen.tips(*p1, 1), gen.tips(*p2, -1), 12), gen.spans(gen.tips(*p2, 1), gen.tips(*p3, -1), 13),
        gen.spans(gen.tips(*p3, 1), sub_ends, 10),
    ]
    parts.append(f'<g stroke="{INK}" fill="none" stroke-linecap="round" stroke-width="1.35">'
                 f'{gen.pylon(*p0)}{gen.pylon(*p1)}{gen.pylon(*p2)}{gen.pylon(*p3)}</g>')
    parts.append(f'<path d="{" ".join(wires)}" stroke="{INK}" stroke-width=".8" fill="none" opacity=".85"></path>')
    parts.append(gen.solar_farm())
    parts.append(gen.sc(gen.datacentre(434, prof(560)), 434, prof(560), 1.22))
    parts.append(gen.sc(gen.battery(706, prof(770)), 706, prof(770), 1.22))
    parts.append(sub_svg)
    parts.append(gen.metmast(1018, prof(1018), 170))
    parts.append(gen.sc(gen.converter(1082, prof(1150)), 1082, prof(1150), 1.26))
    parts.append(gen.sc(gen.gasterminal(1240, prof(1310)), 1240, prof(1310), 1.32))
    _ = S
    return "\n".join(parts)


# Labels: (text, x, y, colour, anchor, class). Light labels carry a petrol halo so they hold AA contrast
# where they cross a ridge (DESIGN: on petrol, text is --on-petrol). lbl-edge hides below 1100 px and
# lbl-far below 700 px, where the drawing is cropped or scaled.
LIGHT = "#F6F4EC"
LABELS = [
    ("onshore wind", 150, 704, LIGHT, "middle", "lbl-edge"),
    ("offshore wind", 1330, 740, LIGHT, "middle", "lbl-edge"),
    ("gas-fired power station", 300, 718, LIGHT, "middle", "lbl-far"),
    ("solar farm", 232, 864, INK, "middle", "lbl-far"),
    ("data centre", 560, 858, INK, "middle", ""),
    ("battery storage", 776, 900, INK, "middle", ""),
    ("substation", 930, 858, INK, "middle", ""),
    ("met mast", 1004, 774, LIGHT, "end", ""),
    ("gas terminal", 1318, 872, INK, "middle", "lbl-edge"),
]


def land_labels() -> str:
    out = []
    for t, x, y, c, a, cls in LABELS:
        halo = (f' stroke="{PETROL}" stroke-width="3.2" stroke-linejoin="round" paint-order="stroke"'
                if c == LIGHT else "")
        k = f' class="{cls}"' if cls else ""
        out.append(f'<text{k} x="{x}" y="{y}" fill="{c}" text-anchor="{a}"{halo}>{t}</text>')
    # the two-line label: the second line is set in em so it follows the label size at every breakpoint
    out.append(f'<text class="lbl-far" x="1156" y="836" fill="{INK}" text-anchor="middle">interconnector'
               f'<tspan x="1156" dy="1.1em">converter station</tspan></text>')
    return "\n".join(out)


def landscape_svg() -> str:
    soil = ('<pattern id="ls-soil" width="23" height="17" patternUnits="userSpaceOnUse">'
            f'<circle cx="4" cy="5" r=".9" fill="{KHAKI}"></circle><circle cx="15" cy="12" r="1.1" fill="{KHAKI}">'
            f'</circle><path d="M17 3 h3" stroke="{KHAKI}" stroke-width=".9"></path></pattern>')
    aria = ("Drawing of the physical grid: onshore and offshore wind, a solar farm, a gas-fired power station and "
            "pylons, a data centre, battery storage, a substation, a met mast, an interconnector converter station "
            "and a gas terminal.")
    return (f'<svg viewBox="-400 {VB_Y0} 2240 {VB_Y1 - VB_Y0}" preserveAspectRatio="xMidYMax slice" role="img" '
            f'aria-label="{aria}"><defs>{soil}</defs>\n{landscape_wide()}\n{land_labels()}\n</svg>')


# ================================================================ core sample: desktop and phone
def core_desktop() -> str:
    return gen.core_svg().replace("<svg ", '<svg class="core-d" ', 1)


def core_phone() -> str:
    """The same core stood upright, labels beside each fuel; drawn to the same gigawatt scale."""
    L = 430
    k = L / (gen.TOTAL / 1000)
    x0, cw, top = 70, 72, 26
    x1 = x0 + cw
    segs, acc = [], float(top)
    for name, mw, pct, col in gen.FUELS:
        h = mw / 1000 * k
        segs.append((name, mw, pct, col, acc, h))
        acc += h
    end = acc
    brk = [(x1, end), (x1 - 12, end + 7), (x1 - 26, end + 1), (x1 - 40, end + 9), (x1 - 55, end + 3),
           (x1 - 66, end + 8), (x0, end + 2)]
    outline = (f"M{x0} {top} A{cw / 2} 10 0 0 1 {x1} {top} "
               + " ".join(f"L{f(a)} {f(b)}" for a, b in brk) + " Z")
    out = ['<defs>',
           f'<clipPath id="cm-clip"><path d="{outline}"></path></clipPath>',
           f'<pattern id="cm-wind" width="14" height="6" patternUnits="userSpaceOnUse"><path d="M0 3 h8" stroke="{DAY}" '
           f'stroke-width=".8"></path></pattern>',
           f'<pattern id="cm-gas" width="7" height="7" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r=".9" '
           f'fill="{INK}"></circle><circle cx="5.5" cy="5.5" r=".7" fill="{INK}"></circle></pattern>',
           f'<pattern id="cm-imp" width="7" height="7" patternUnits="userSpaceOnUse"><path d="M0 7 L7 0" stroke="{DAY}" '
           f'stroke-width=".8"></path></pattern>',
           f'<pattern id="cm-bio" width="10" height="8" patternUnits="userSpaceOnUse"><path d="M1 2 l3 1 M6 6 l3 -1" '
           f'stroke="{INK}" stroke-width=".8"></path></pattern>',
           '</defs>', '<g clip-path="url(#cm-clip)">']
    pat = {"Wind": ("cm-wind", ".45"), "CCGT": ("cm-gas", ".22"), "Imports": ("cm-imp", ".3"), "Biomass": ("cm-bio", ".3")}
    for name, mw, pct, col, sy, h in segs:
        y = top - 12 if name == "Wind" else sy
        hh = h + (sy - y) + (12 if name == "Other" else .5)
        out.append(f'<rect x="{x0}" y="{f(y)}" width="{cw}" height="{f(hh)}" fill="{col}"></rect>')
        if name in pat:
            out.append(f'<rect x="{x0}" y="{f(y)}" width="{cw}" height="{f(hh)}" fill="url(#{pat[name][0]})" '
                       f'opacity="{pat[name][1]}"></rect>')
    out.append(f'<rect x="{x0 + 7}" y="{top - 12}" width="7" height="{f(end - top + 24)}" fill="#FFFFFF" opacity=".2"></rect>')
    out.append(f'<rect x="{x1 - 15}" y="{top - 12}" width="15" height="{f(end - top + 24)}" fill="#000000" opacity=".13"></rect>')
    out.append('</g>')
    fr = []
    for i, (_, _, _, _, sy, _) in enumerate(segs[1:]):
        j = [5, -6, 6, -5, 4, -6] if i % 2 else [-6, 5, -5, 6, -4, 5]
        pts = [(x0, sy)] + [(x0 + 11 + n * 10, sy + j[n]) for n in range(6)] + [(x1, sy)]
        fr.append("M" + " L".join(f"{f(a)} {f(b)}" for a, b in pts))
    out.append(f'<path d="{" ".join(fr)}" stroke="{T_TOP}" stroke-width="2.4" fill="none" stroke-linejoin="round"></path>')
    out.append(f'<path d="{outline}" fill="none" stroke="{INK}" stroke-width="1.2"></path>')
    out.append(f'<ellipse cx="{x0 + cw / 2}" cy="{top}" rx="{cw / 2}" ry="10" fill="#8FC0C6" stroke="{INK}" '
               f'stroke-width="1.2"></ellipse>')
    out.append(f'<ellipse cx="{x0 + cw / 2}" cy="{top}" rx="{cw / 2 - 12}" ry="5" fill="none" stroke="{INK}" '
               f'stroke-width=".7" opacity=".45"></ellipse>')
    lab, ticks = [f'<g font-family="Hanken Grotesk" font-size="14.5" fill="{INK}">'], []
    for name, mw, pct, col, sy, h in segs:
        my = sy + h / 2
        ticks.append(f"M{x1 + 3} {f(my)} h8")
        lab.append(f'<text x="{x1 + 16}" y="{f(my + 5)}"><tspan font-weight="600">{name}</tspan> '
                   f'{mw / 1000:.1f} GW, {pct}%</text>')
    lab.append('</g>')
    out.append(f'<path d="{" ".join(ticks)}" stroke="{INK}" stroke-width="1" opacity=".55"></path>')
    out += lab
    ax = x0 - 16
    major = " ".join(f"M{ax - 4} {f(top + g * k)} H{ax + 4}" for g in range(0, 25, 5) if top + g * k <= end + .5)
    minor = " ".join(f"M{ax - 2} {f(top + g * k)} H{ax + 2}" for g in range(0, 23) if g % 5)
    out.append(f'<path d="M{ax} {top} V{f(end)} {major} {minor}" stroke="{INK}" stroke-width="1"></path>')
    tl = "".join(f'<text x="{ax - 8}" y="{f(top + g * k + 4.5)}" text-anchor="end">{"20 GW" if g == 20 else g}</text>'
                 for g in range(0, 25, 5) if top + g * k <= end + .5)
    out.append(f'<g font-family="Hanken Grotesk" font-size="13" fill="{SOFT}">{tl}</g>')
    w, h = 320, int(end + 26)
    aria = ("Core sample of Great Britain's mean generation by fuel, 1 to 5 August 2026, drawn to a gigawatt scale: "
            "wind 6.4 GW (29%), CCGT 5.6 GW (26%), nuclear 3.6 GW (16%), imports 3.2 GW (14%), biomass 2.4 GW (11%), "
            "other 0.9 GW (4%); 22.1 GW in all.")
    return (f'<svg class="core-m" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{aria}">'
            + "\n".join(out) + "</svg>")


# ================================================================ the merit-order drawing: desktop and phone
class Geo:
    def __init__(self, p: str, W: float, PX: float, SW: float, BY: float, PH: float, HIST_D: float, HW: float,
                 rows: dict[str, float], H: float, fs: float, phone: bool) -> None:
        self.p, self.W, self.PX, self.SW, self.BY, self.PH = p, W, PX, SW, BY, PH
        self.HIST_D, self.HW, self.rows, self.H, self.fs, self.phone = HIST_D, HW, rows, H, fs, phone

    def X(self, q: float) -> float:
        return self.PX + q * self.SW


DESK = Geo("pb", gen_b.D_W, gen_b.PX, gen_b.SW, gen_b.BY, gen_b.PH, gen_b.HIST_D, 122, gen_b.ROWS, gen_b.D_H, 14,
           False)
_BY = 330
PHONE = Geo("pm", 480, 84, 382, _BY, 292, 50, 72,
            {"r": _BY + 2, "s": _BY + 120, "w": _BY + 176, "d": _BY + 232}, _BY + 232 + 26, 16.5, True)
BAR = gen_b.BAR


def _fan(g: Geo, cx: float, sd: float, y: float, fill: str) -> str:
    o, i, h = 1.645 * sd * g.SW, .674 * sd * g.SW, BAR + 10
    return (f'<rect x="{f(cx - o)}" y="{f(y - h / 2)}" width="{f(2 * o)}" height="{h}" fill="{fill}" opacity=".38" '
            f'stroke="{INK}" stroke-width=".6"></rect>'
            f'<rect x="{f(cx - i)}" y="{f(y - h / 2)}" width="{f(2 * i)}" height="{h}" fill="{fill}" opacity=".8"></rect>'
            f'<path d="M{f(cx)} {f(y - h / 2 - 3)} V{f(y + h / 2 + 3)}" stroke="{INK}" stroke-width="1.8"></path>')


def _knock(x: float, y: float, text: str, fs: float, fill: str, anchor: str = "start") -> str:
    """A patch of the block's own colour behind an ink label, so neither the hatch nor the draws cross it."""
    w = sum(.66 if c.isupper() else .5 for c in text) * fs + 6
    x0 = x - 3 if anchor == "start" else x - w + 3
    return f'<rect x="{f(x0)}" y="{f(y - fs * .82)}" width="{f(w)}" height="{f(fs * 1.08)}" fill="{fill}"></rect>'


def merit(g: Geo) -> str:
    X, PX, SW, BY, PH = g.X, g.PX, g.SW, g.BY, g.PH
    parts = [f'<defs>{gen.pat_defs(g.p)}</defs>']
    ds = gen_b.sampled_draws(gen_b.N_DRAW)
    parts.append(gen.stack_draw(g.p, PX, BY, SW, PH, joints_on=False))
    RDB, Q_LO, Q_HI = gen_b.RDB, gen_b.Q_LO, gen_b.Q_HI
    nb_in = round((Q_HI - Q_LO) * SW / (PH / 60))
    step = (Q_HI - Q_LO) / nb_in
    pdf = [RDB.pdf(Q_LO + (b + .5) * step) for b in range(nb_in)]
    pm = max(pdf)
    bars_in = "".join(
        f'<rect x="{f(X(Q_LO + b * step) + .4)}" y="{BY + 2}" width="{f(step * SW - .8)}" '
        f'height="{f(p / pm * g.HIST_D)}"></rect>' for b, p in enumerate(pdf) if p / pm * g.HIST_D > 2)
    parts.append(f'<g fill="{OLIVE}" opacity=".72">{bars_in}</g>')
    ups = " ".join(f"M{f(X(q))} {BY} V{f(BY - gen.cost_at(q) * PH)}" for q in ds)
    outs = " ".join(f"M{f(X(q))} {f(BY - gen.cost_at(q) * PH)} H{PX}" for q in ds[::3])
    parts.append(f'<path d="{ups}" stroke="{DAY}" stroke-width="1" opacity=".7"></path>')
    parts.append(f'<path d="{outs}" stroke="{INK}" stroke-width=".8" opacity=".22"></path>')
    parts.append(f'<g fill="{INK}">' + "".join(
        f'<circle cx="{f(X(q))}" cy="{f(BY - gen.cost_at(q) * PH)}" r="1.7"></circle>' for q in ds) + '</g>')
    nb = 60
    dens = gen_b.price_density(nb)
    dm = max(dens)
    bh = PH / nb
    bars = "".join(
        f'<rect x="{f(PX - 3 - n / dm * g.HW)}" y="{f(BY - (b + 1) * bh + .4)}" width="{f(n / dm * g.HW)}" '
        f'height="{f(bh - .8)}"></rect>' for b, n in enumerate(dens) if n / dm * g.HW > .8)
    parts.append(f'<g fill="{GOLD}">{bars}</g>')
    parts.append(f'<path d="M{PX} {BY} V22 M{PX} {BY} H{PX + SW + 16}" stroke="{INK}" stroke-width="1.5" fill="none"></path>')

    # tranche labels last, so the draws never cross them; ink labels on clay sit on a knocked-out patch
    fs = g.fs
    t, knock, acc = [], [], 0.0
    for name, share, costs, fill, _ in gen.TRANCHES:
        col = DAY if fill == PETROL else INK
        x, y, anchor = PX + acc * SW + 7, BY - 9, "start"
        if name == "Biomass":
            x, y = PX + acc * SW + 2, BY - costs[-1] * PH - 7
            if g.phone:
                x, y = PX + 4, BY - .10 * PH - 28
        elif g.phone and name == "Nuclear":
            # the two cheapest tranches are too narrow to hold their names on a phone: stack the names above
            x, y, col = PX + 4, BY - costs[-1] * PH - 8, INK
        elif g.phone and name == "OCGT":
            x, y, anchor = PX + SW, BY - costs[-1] * PH - 8, "end"
        elif fill == CLAY:
            knock.append(_knock(x, y, name, fs, CLAY))
        a = ' text-anchor="end"' if anchor == "end" else ""
        t.append(f'<text x="{f(x)}" y="{f(y)}" fill="{col}"{a}>{name}</text>')
        acc += share
    parts.append("".join(knock))
    parts.append(f'<g font-family="Hanken Grotesk" font-style="italic" font-size="{fs}">{"".join(t)}</g>')

    rows = g.rows
    if g.phone:
        axis_words = (f'<text x="{PX + 10}" y="30">price</text>'
                      f'<text x="{PX + SW}" y="{BY + g.HIST_D + 26}" text-anchor="end">capacity, cheapest first</text>')
    else:
        axis_words = (f'<text x="{PX + 10}" y="30">price</text>'
                      f'<text x="{PX + SW + 16}" y="{BY + 22}" text-anchor="end">capacity, cheapest first</text>')
    parts.append(f'<g font-family="Hanken Grotesk" font-style="italic" font-size="{fs}" fill="{INK}">{axis_words}</g>')

    xr = X(gen_b.MU_R)
    xw = X(gen_b.MU_R + gen_b.SOLAR_M)
    xd = X(gen_b.MU_R + gen_b.SOLAR_M + gen_b.WIND_M)
    rs, rw, rd = rows["s"], rows["w"], rows["d"]
    parts.append(gen_b.bar_row(rd, [(PX, xd, OLIVE, ".4")]) + _fan(g, xd, gen_b.SD_D, rd, OLIVE))
    parts.append(gen_b.bar_row(rw, [(PX, xw, OLIVE, ".4"), (xw, xd, HORIZON, "1")]) + _fan(g, xw, gen_b.SD_W, rw, HORIZON))
    parts.append(gen_b.bar_row(rs, [(PX, xr, OLIVE, ".4"), (xr, xw, CHART, "1"), (xw, xd, HORIZON, ".3")])
                 + _fan(g, xr, gen_b.SD_S, rs, CHART))
    hb = BAR / 2 + 8
    parts.append(f'<path d="M{f(xd)} {rd - hb} V{rw + BAR / 2} M{f(xw)} {rw - hb} V{rs + BAR / 2} '
                 f'M{f(xr)} {rs - hb} V{f(BY + 2 + g.HIST_D)}" stroke="{INK}" stroke-width="1" '
                 f'stroke-dasharray="1.5 3"></path>')
    if g.phone:
        row_words = (f'<text x="{PX}" y="{BY + 22}">residual demand</text>'
                     f'<text x="{PX}" y="{rs - 17}">less solar</text>'
                     f'<text x="{PX}" y="{rw - 17}">less wind</text>'
                     f'<text x="{PX}" y="{rd - 17}">demand</text>')
        anchor = ""
    else:
        row_words = (f'<text x="{PX - 12}" y="{BY + 24}">residual demand</text>'
                     f'<text x="{PX - 12}" y="{rs + 5}">less solar</text>'
                     f'<text x="{PX - 12}" y="{rw + 5}">less wind</text>'
                     f'<text x="{PX - 12}" y="{rd + 5}">demand</text>')
        anchor = ' text-anchor="end"'
    parts.append(f'<g font-family="Hanken Grotesk" font-style="italic" font-size="{fs}" fill="{INK}"{anchor}>'
                 f'{row_words}</g>')
    aria = ("How the price forecast is built, drawn without scales. Read from the bottom: a demand forecast is a bar "
            "along the capacity axis with its spread at the end; the wind forecast is carved off that end, then the "
            "solar forecast, each with its own spread. What is left is residual demand, drawn as a histogram of draws "
            "hanging under the capacity axis. Above it, a merit-order supply curve rises in steps: biomass, nuclear, "
            "a long run of CCGT units, coal, then OCGT. Many faint draws rise from the residual-demand histogram "
            "through the stack; each meets the curve and reads off a price, and the prices pile up as a second "
            "histogram along the price axis: a distribution in, a distribution out.")
    cls = "draw-m" if g.phone else "draw-d"
    return (f'<svg class="{cls}" width="{f(g.W)}" height="{f(g.H)}" viewBox="0 0 {f(g.W)} {f(g.H)}" role="img" '
            f'aria-label="{aria}">' + "".join(parts) + "</svg>")


# ================================================================ html pieces
def keys() -> str:
    b = gen.swatch(gen.T_BRONZE, "k-b", '<pattern id="k-b" width="24" height="12" patternUnits="userSpaceOnUse"><path d="M0 11.5 H24 M12 0 V6 M0 6 H24 M0 6 V12" stroke="#7C5530" stroke-width=".8" fill="none"></path></pattern>')
    s = gen.swatch(gen.T_SILVER, "k-s", '<pattern id="k-s" width="8" height="8" patternUnits="userSpaceOnUse"><path d="M0 8 L8 0" stroke="#5E6E6B" stroke-width=".8"></path></pattern>')
    g = gen.swatch(gen.T_GOLD, "k-g", '<pattern id="k-g" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="2" cy="3" r="1" fill="#8A6F1E"></circle><circle cx="6.5" cy="7.5" r=".8" fill="#8A6F1E"></circle></pattern>')
    items = [
        (b, "data-sources.html", "Vendors", "Seven vendors across UK and EU power, gas, carbon and weather: 165 datasets, "
                                            "each with schema, sample queries, and the caveats that bite."),
        (s, "architecture.html", "Pipeline", "Bronze, silver and gold layers. End-to-end data flow, design decisions, and "
                                             "the full repo map."),
        (g, "models/demand-forecast.html", "Forecasts", "Quantitative work built on the warehouse: probabilistic demand, "
                                                        "wind, solar, and a fundamentals SMP forecaster."),
    ]
    li = "\n".join(f'          <li><a href="{h}">{sw}<h3>{t}</h3><p>{d}</p></a></li>' for sw, h, t, d in items)
    return li


VEND_ORDER = ["elexon", "nesodp", "entsoe", "gie", "neso", "openmeteo", "entsog"]   # row by row, as drawn
VEND_HREF = {"elexon": "elexon", "nesodp": "neso_data_portal", "entsoe": "entsoe", "gie": "gie", "neso": "neso",
             "openmeteo": "openmeteo", "entsog": "entsog"}
FEED = {"elexon": "substation", "nesodp": "substation", "neso": "substation", "openmeteo": "metmast",
        "entsoe": "converter", "entsog": "gasterminal", "gie": "gasterminal"}


def vendors() -> str:
    out = []
    for key in VEND_ORDER:
        name, desc, meta, series, code, cap, _row, _slot, file, zero = gen.VENDORS[key]
        land = (f'<p class="vend__land"><code>{file}</code></p>' if file
                else '<p class="vend__land" aria-hidden="true"></p>')
        spark = gen.spark(series, zero=zero)
        out.append(
            f'        <article class="vend vend--{key}" data-feed="{FEED[key]}">\n'
            f'          {land}\n'
            f'          <h3 class="h-entry"><a href="data-sources/{VEND_HREF[key]}.html">{name}</a></h3>\n'
            f'          <p class="vend__d">{desc}</p>\n'
            f'          <p class="vend__m">{meta}</p>\n'
            f'          {spark}\n'
            f'          <p class="vend__cap"><code>{code}</code><br>{cap}</p>\n'
            f'        </article>')
    return "\n".join(out)


def keyed() -> str:
    MID, BUILD = gen.MID, gen.BUILD
    D_H = gen_b.D_H
    rows = gen_b.ROWS
    PH, BY = gen_b.PH, gen_b.BY

    def at(px: float) -> str:
        return f"{px / D_H * 100:.2f}%"

    def row(y: float) -> float:
        return y - 11
    entries = [
        (at(34), "stack", "Merit-order supply curve", f'<p class="keyed__id">{MID["stack"]}</p>'
         f'<p class="keyed__d">{BUILD}: GB plant in merit order, cheapest first.</p>', ""),
        (at(BY - .66 * PH), "smp", "Fundamentals SMP forecaster", f'<p class="keyed__id">{MID["smp"]}</p>'
         '<p class="keyed__d">Monte Carlo draws of residual demand, each cleared against the curve, build a price '
         'distribution. Backtested against ENTSO-E day-ahead prices.</p>', ""),
        (at(rows["r"] + 1), "resid", "Residual demand",
         '<p class="keyed__d">Demand less wind and solar: 1,000 draws, each a demand draw less a wind draw and a '
         'solar draw.</p>', "is-q"),
        (at(row(rows["s"])), "solar", "Solar generation", f'<p class="keyed__id">{MID["solar"]}</p>', ""),
        (at(row(rows["w"])), "wind", "Wind generation", f'<p class="keyed__id">{MID["wind"]}</p>', ""),
        (at(row(rows["d"])), "demand", "Day-ahead demand", f'<p class="keyed__id">{MID["demand"]}</p>'
         '<p class="keyed__d"><a class="more" href="models/demand-forecast.html">See the case study</a></p>', ""),
    ]
    out = []
    for top, kind, name, rest, cls in entries:
        mark = gen_b.mark(kind).replace(' class="b-mk"', "")
        c = f' class="{cls}"' if cls else ""
        out.append(f'          <li{c} style="--at: {top}">{mark}<div><p class="keyed__n">{name}</p>{rest}</div></li>')
    return "\n".join(out)


def notebook() -> str:
    rows = "".join(f"<div><dt>{n}</dt><dd>{d}</dd></div>" for n, d in gen.SRC_VERBS)
    comp = "".join(f'<li class="sel">{n}</li>' if i == 0 else f"<li>{n}</li>"
                   for i, n in enumerate(sorted(n for n, _ in gen.SRC_VERBS)))
    plot = re.search(r'<svg class="plot".*?</svg>', REF, flags=re.S).group(0)
    plot = plot.replace('class="plot" width="600" height="300" ', 'class="plot" width="600" height="300" ')
    aria = re.search(r'<figure class="nb" aria-label="([^"]*)"', REF).group(1)
    q5 = ('df[df.fuel_type == <span class="s">"WIND"</span>].plot(x=<span class="s">"timestamp_utc"</span>, '
          'y=<span class="s">"generation_mw"</span>, ylabel=<span class="s">"MW"</span>)')

    def cell(c: str, p: str, body: str) -> str:
        return f'            <div class="cell{c}"><span class="pr">{p}</span>{body}</div>'
    cells = "\n".join([
        cell("", "[1]:", f'<pre class="in">{gen.SETUP}</pre>'),
        cell("", "[2]:", '<pre class="in">data.elexon</pre>'),
        cell(" out", "[2]:", f'<div class="card"><p class="card-h">data.elexon</p><dl>{rows}</dl>'
             f'<p class="card-f">Discover datasets: <code>data.elexon.list_datasets()</code></p></div>'),
        cell("", "[3]:", f'<pre class="in">df = {gen.hl(gen.Q_FUEL)}</pre>'),
        cell("", "[4]:", f'<pre class="in">{gen.hl(gen.Q_HEAD)}</pre>'),
        cell(" out", "[4]:", f'<div class="df-wrap">{gen.df_html()}</div>'),
        cell("", "[5]:", f'<pre class="in">{q5}</pre>'),
        cell(" out", "[5]:", '<div class="fig"><pre class="txt">&lt;Axes: xlabel=\'timestamp_utc\', '
             f'ylabel=\'MW\'&gt;</pre>{plot}</div>'),
        cell(" act", "[ ]:", '<pre class="in">data.entsoe.<span class="caret"></span></pre>'
             f'<ul class="cmp" aria-label="Tab completions for data.entsoe">{comp}</ul>'),
    ])
    return (f'        <figure class="nb" aria-label="{aria}">\n'
            f'          <div class="nb-bar"><span class="nb-tab">fuelhh_analysis.ipynb</span>'
            f'<span class="nb-kern">gridflow_models</span></div>\n'
            f'          <div class="nb-body">\n{cells}\n          </div>\n        </figure>')


def skills() -> str:
    return "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in gen.SKILLS)


FONTS = ("https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,200..800"
         "&amp;family=Hanken+Grotesk:ital,wght@0,400..700;1,400..600&amp;family=Red+Hat+Mono:wght@400;500"
         "&amp;display=swap")


def page() -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>gridflow: a pipeline and catalogue for UK and European energy data</title>
  <meta name="description" content="gridflow ingests, normalises and serves time-series data from seven vendors (electricity, gas, weather and carbon) into one queryable warehouse, with models for demand, wind, solar and clearing prices one layer above.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="{FONTS}">
  <link rel="stylesheet" href="assets/theme.css">
</head>
<body data-page="home" data-root="" data-screen-label="01 Home">
  <main id="main">
    <section class="stratum stratum--sky" aria-labelledby="hero-h">
      <div class="wrap hero">
        <h1 class="hero__h h-hero" id="hero-h">A pipeline and catalogue for UK &amp; European energy data.</h1>
        <div class="hero__lede">
          <p>Gridflow ingests, normalises and serves time-series data from seven public and authenticated vendors (electricity, gas, weather and carbon) into a single queryable warehouse. Models for demand, wind, solar and clearing prices sit one layer above.</p>
          <div class="cta"><a class="btn" href="architecture.html">Explore the architecture</a><a class="link-alt" href="models/demand-forecast.html">See a model</a></div>
          <p class="hero__scope">Seven vendors, 165 datasets, four markets, seventeen years of history, three pipeline layers.</p>
        </div>
        <section class="keys" aria-labelledby="keys-h">
          <h2 id="keys-h">Three things to explore</h2>
          <ul>
{keys()}
          </ul>
        </section>
      </div>
      <figure class="landscape">
        {landscape_svg()}
      </figure>
    </section>

    <div class="stratum stratum--topsoil stratum--flush">
      <section class="wrap core" aria-labelledby="core-h">
        <h2 class="core__h h-fig" id="core-h">Great Britain’s generation by fuel, 1 to 5 August 2026</h2>
        <figure class="core__fig">
          {core_desktop()}
          {core_phone()}
        </figure>
        <p class="core__cap caption">Mean output per fuel type across 240 half-hourly settlement periods; the six fuels sum to 22.1 GW. Source: Elexon FUELHH. <a class="more" href="data-sources/elexon/fuelhh.html">Open the fuelhh page</a></p>
      </section>
      <hr class="bedding">
      <section class="wrap purpose" aria-labelledby="why-h">
        <div class="purpose__head">
          <h2 class="h-xl" id="why-h">{gen.WHY_H2}</h2>
          <p class="purpose__intro intro">{gen.INTRO}</p>
          <p class="purpose__aim">{gen.AIM}</p>
        </div>
        <div class="purpose__body">
          <figure class="purpose__draw">
            {merit(DESK)}
            {merit(PHONE)}
          </figure>
          <ul class="keyed" aria-label="The models and residual demand, keyed to the drawing">
{keyed()}
          </ul>
        </div>
      </section>
    </div>

    <section class="stratum stratum--bronze" aria-labelledby="cat-h">
      <span class="stratum__name" aria-hidden="true">bronze</span>
      <div class="wrap">
        <div class="cat__head prose">
          <h2 class="h-sec" id="cat-h">Seven feeds, one warehouse</h2>
          <p>Raw API responses land in bronze, append-only and SHA-256 hashed. Each cable below ends at the vendor that publishes data on that part of the system.</p>
          <p><a class="more" href="data-sources.html">Full catalogue</a></p>
        </div>
        <div class="vendors">
{vendors()}
        </div>
      </div>
    </section>

    <section class="stratum stratum--silver" aria-labelledby="silver-h">
      <span class="stratum__name" aria-hidden="true">silver</span>
      <div class="wrap silver">
        <div class="prose">
          <h2 class="h-sec" id="silver-h">Cleaned, typed, deduped tables live in silver</h2>
          <p>Everything is Hive-partitioned Parquet, queryable from DuckDB or the Python client. Backfills are idempotent. Schema changes are caught at parse time by Pydantic v2 contracts. Bitemporal: every row carries both event-time and ingestion-time, so point-in-time queries are trivial.</p>
          <p><a class="more" href="architecture.html">Read the design doc</a></p>
        </div>
        <div class="silver__tables">
          <ul class="tables" aria-label="Silver tables">{"".join(f"<li>{t}</li>" for t in gen.SILVER_T)}</ul>
        </div>
      </div>
    </section>

    <section class="stratum stratum--gold" aria-labelledby="gold-h">
      <span class="stratum__name" aria-hidden="true">gold</span>
      <div class="wrap gold">
        <div class="gold__text prose">
          <h2 class="h-sec" id="gold-h">Gold data is cleaned, joined and ready to use</h2>
          <p>Served as DuckDB views.</p>
        </div>
        <ul class="views" aria-label="Gold views">{"".join(f"<li>{t}</li>" for t in gen.GOLD_T)}</ul>
      </div>
      <hr class="bedding">
      <section class="wrap wb" aria-labelledby="wb-h">
        <div class="prose">
          <h2 class="h-sec" id="wb-h">{gen.WB_H2}</h2>
          <p>{gen.WB_P1}</p>
          <p>{gen.WB_P2}</p>
        </div>
{notebook()}
      </section>
    </section>

    <section class="stratum stratum--deep" id="about" aria-labelledby="about-h">
      <div class="wrap about">
        <div>
          <h2 class="about__name" id="about-h">Elliot Bentham</h2>
          <p class="about__role">Quantitative Developer, London, UK</p>
          <p class="about__intro">Gridflow is a personal research platform for UK and European power markets: a medallion data pipeline, vendor catalogue and probabilistic modelling stack.</p>
          <p class="about__body">I’m a quantitative developer at ICBCS working across FICC, with prior experience in European power and gas research at RISQ and FX options pricing at Bank of America Merrill Lynch. Gridflow integrates data from Elexon, ENTSO-E, ENTSO-G and weather sources, with a React + TypeScript front-end over the analytics layer. Developed to support my own research in energy markets, including power stack modelling, as well as to develop fluency in agentic AI development workflows.</p>
          <div class="links"><a class="btn" href="https://github.com/EBentham">GitHub</a><a href="https://linkedin.com/in/elliot-bentham">LinkedIn</a><a href="cv.pdf">CV (PDF)</a><a href="mailto:e.bentham31231@gmail.com">Email</a></div>
        </div>
        <div class="skills">
          <h3>Skills</h3>
          <dl>{skills()}</dl>
        </div>
      </div>
    </section>
  </main>
  <script src="assets/site.js"></script>
  <script src="assets/home.js"></script>
</body>
</html>
"""


# ================================================================ generated css: textures and contacts
def uri(svg: str) -> str:
    return ("url(\"data:image/svg+xml," + svg.replace("%", "%25").replace("#", "%23").replace("<", "%3C")
            .replace(">", "%3E").replace('"', "'") + "\")")


def bez_points(pts: list[tuple[float, float]], per: int = 10) -> list[tuple[float, float]]:
    """Sample the same Catmull-Rom curve gen.smooth() draws."""
    out = [pts[0]]
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i > 0 else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else pts[i + 1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        for k in range(1, per + 1):
            t = k / per
            u = 1 - t
            out.append((u ** 3 * p1[0] + 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t ** 3 * p2[0],
                        u ** 3 * p1[1] + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t ** 3 * p2[1]))
    return out


def contact(pts: list[tuple[float, float]], y0: float, band: float, stroke: float, per: int) -> tuple[str, str]:
    dense = [(x, y - y0 + band / 2) for x, y in bez_points(pts, per) if -30 <= x <= 1470]
    for x, y in dense:
        assert 0 < y < band, (x, y, band)
    poly = ", ".join(f"{x / 14.4:.3f}% {y:.2f}px" for x, y in dense) + ", 100% 100%, 0% 100%"
    d = "M" + " L".join(f"{x:.1f} {y:.2f}" for x, y in dense)
    line = uri(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1440 {band:g}' preserveAspectRatio='none'>"
               f"<path d='{d}' fill='none' stroke='#000' stroke-width='{stroke:g}'/></svg>")
    return f"polygon({poly})", line


def generated_css() -> str:
    tex = {
        "soil": ("<svg xmlns='http://www.w3.org/2000/svg' width='23' height='17'><circle cx='4' cy='5' r='.9'/>"
                 "<circle cx='15' cy='12' r='1.1'/><path d='M17 3 h3' stroke='#000' stroke-width='.9'/></svg>", "23px 17px"),
        "brick": ("<svg xmlns='http://www.w3.org/2000/svg' width='24' height='12'><path d='M0 11.5 H24 M12 0 V6 M0 6 H24 "
                  "M0 6 V12' stroke='#000' stroke-width='.8' fill='none'/></svg>", "24px 12px"),
        "diag": ("<svg xmlns='http://www.w3.org/2000/svg' width='8' height='8'><path d='M0 8 L8 0' stroke='#000' "
                 "stroke-width='.8'/></svg>", "8px 8px"),
        "stip": ("<svg xmlns='http://www.w3.org/2000/svg' width='9' height='9'><circle cx='2' cy='3' r='1'/>"
                 "<circle cx='6.5' cy='7.5' r='.8'/></svg>", "9px 9px"),
        "granite": ("<svg xmlns='http://www.w3.org/2000/svg' width='46' height='40'><path d='M8 8 h8 M12 4 v8 M30 26 h8 "
                    "M34 22 v8 M20 34 h6 M23 31 v6 M40 6 h5 M42.5 3.5 v5' stroke='#000' stroke-width='1.1'/></svg>",
                    "46px 40px"),
    }
    bed = "M" + " L".join(f"{x} {6 + 4 * math.sin(2 * math.pi * x / 480 + .8) :.2f}" for x in range(0, 481, 8))
    bed_svg = (f"<svg xmlns='http://www.w3.org/2000/svg' width='480' height='12'><path d='{bed}' fill='none' "
               f"stroke='#000' stroke-width='1' stroke-dasharray='2 6'/></svg>")
    lines = [":root {"]
    for k, (svg, size) in tex.items():
        lines.append(f"  --tex-{k}: {uri(svg)} 0 0 / {size} repeat;")
    lines.append(f"  --tex-bed: {uri(bed_svg)} 0 50% / 480px 12px repeat-x;")
    lines.append("}")
    W = gen.W
    waves = {
        "topsoil": (gen.wave(0, 6, 5.5), 0, 24, 3, 6),
        "bronze": (gen.wave(0, 7, 0.4), 0, 24, 3, 6),
        "silver": (gen.wave(0, 8, 2.1), 0, 24, 3, 6),
        "gold": (gen.wave(0, 7, 4.0), 0, 24, 3, 6),
        "deep": ([(x, 9 * math.sin(x / 140 + 1) + 6 * math.sin(x / 53 + 2) + 4 * math.sin(x / 19))
                  for x in range(-40, W + 41, 20)], 0, 44, 4, 2),
    }
    for name, (pts, y0, band, stroke, per) in waves.items():
        poly, line = contact(pts, y0, band, stroke, per)
        lines.append(f".stratum--{name}:not(.stratum--flush) {{ clip-path: {poly}; }}")
        lines.append(f".stratum--{name}:not(.stratum--flush)::after {{ -webkit-mask: {line} 0 0 / 100% 100% no-repeat; "
                     f"mask: {line} 0 0 / 100% 100% no-repeat; }}")
    return ("/* ---------------------------------------------------------------- GENERATED: textures and contacts\n"
            "   Written by the homepage generator from the reference board's wave functions. */\n" + "\n".join(lines) + "\n")


def main() -> None:
    html = page()
    ids = re.findall(r'\sid="([^"]+)"', html)
    dup = {i for i in ids if ids.count(i) > 1}
    assert not dup, dup
    assert "/>" not in re.sub(r"<(meta|link|br)[^>]*>", "", html), "self-closing tag"
    OUT_HTML.write_text(html, encoding="utf-8", newline="\n")
    css = (HERE / "theme.src.css").read_text(encoding="utf-8").replace("/*@GENERATED@*/\n", generated_css())
    OUT_CSS.write_text(css, encoding="utf-8", newline="\n")
    print("html", len(html), "css", len(css), "ids", len(ids))


if __name__ == "__main__":
    _ = (BRONZE, NormalDist)
    main()
