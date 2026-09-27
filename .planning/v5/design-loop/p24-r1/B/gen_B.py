"""Phase 24 round 1, designer B: "The reference manual". Emits four dataset-page boards from ONE template.

    python gen_B.py            # writes B-<slug>.dc.html + static/B-<slug>.html
    python gen_B.py H=a,b,c,d  # (optional) root heights measured in the browser, in board order

Every number, code and column name comes from ../pack/specimens.json (read at run time) or is quoted from
../pack/SPECIMENS.md. Prose that is not in the pack is marked NEW COPY in the COPY dicts below.
"""
from __future__ import annotations

import html
import json
import math
import re
import sys
from datetime import date, datetime
from pathlib import Path

HERE = Path(__file__).parent
PACK = json.loads((HERE.parent / "pack" / "specimens.json").read_text(encoding="utf-8"))
SPEC = {s["id"]: s for s in PACK["specimens"]}

W = 1440
PETROL, HORIZON, CHART, OLIVE = "#155A6E", "#3E8C97", "#AFC64E", "#66793B"
INK, INK2, DAY, CLAY, KHAKI, MUTED = "#1C2B22", "#3F4A3B", "#F6F4EC", "#C77E3C", "#A39A6A", "#5d6a55"
BRONZE, TOP = "#A5713C", "#ECE8DA"
FONT_STACK = "Hanken Grotesk"


def f(v: float) -> str:
    return f"{v:.1f}".rstrip("0").rstrip(".") if abs(v - round(v)) > 1e-9 else str(int(round(v)))


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def num(v: float, dp: int = 0) -> str:
    s = f"{abs(v):,.{dp}f}"
    return ("−" if v < 0 else "") + s


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


# ================================================================ patterns (the homepage core-sample textures, plus two)
def pat_defs(p: str) -> str:
    """Fuel textures, as on the homepage core sample, plus the two for codes the palette does not name."""
    return (
        f'<pattern id="{p}-wind" width="14" height="6" patternUnits="userSpaceOnUse"><path d="M0 3 h8" stroke="{DAY}" '
        f'stroke-width=".8"></path></pattern>'
        f'<pattern id="{p}-gas" width="7" height="7" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r=".9" '
        f'fill="{INK}"></circle><circle cx="5.5" cy="5.5" r=".7" fill="{INK}"></circle></pattern>'
        f'<pattern id="{p}-imp" width="7" height="7" patternUnits="userSpaceOnUse"><path d="M0 7 L7 0" stroke="{DAY}" '
        f'stroke-width=".8"></path></pattern>'
        f'<pattern id="{p}-bio" width="10" height="8" patternUnits="userSpaceOnUse"><path d="M1 2 l3 1 M6 6 l3 -1" '
        f'stroke="{INK}" stroke-width=".8"></path></pattern>'
        # uncovered codes: khaki, told apart from the vendor's OTHER (flat khaki) by an ink texture
        f'<pattern id="{p}-hyd" width="6" height="6" patternUnits="userSpaceOnUse"><path d="M0 6 L6 0 M-1 1 L1 -1 M5 7 L7 5" '
        f'stroke="{INK}" stroke-width=".7"></path></pattern>'
        f'<pattern id="{p}-ps" width="8" height="8" patternUnits="userSpaceOnUse"><path d="M4 2 V6 M2 4 H6" stroke="{INK}" '
        f'stroke-width=".8"></path></pattern>'
        f'<pattern id="{p}-null" width="7" height="7" patternUnits="userSpaceOnUse"><path d="M0 7 L7 0 M-1 1 L1 -1 M6 8 L8 6" '
        f'stroke="{INK}" stroke-width=".6"></path></pattern>'
    )


# (fill, pattern suffix or None, pattern opacity)
GROUP_STYLE = {
    "wind": (HORIZON, "wind", ".45"), "gas": (CLAY, "gas", ".22"), "nuclear": (PETROL, None, ""),
    "imports": (OLIVE, "imp", ".3"), "biomass": (BRONZE, "bio", ".3"), "other": (KHAKI, None, ""),
    "hyd": (KHAKI, "hyd", ".38"), "ps": (KHAKI, "ps", ".42"),
}


def fill_rect(p: str, g: str, x: float, y: float, w: float, h: float, outline: bool = False) -> str:
    col, pat, op = GROUP_STYLE[g]
    s = f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="{col}"></rect>'
    if pat:
        s += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="url(#{p}-{pat})" opacity="{op}"></rect>'
    if outline:
        s += (f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="none" stroke="{INK}" '
              f'stroke-width=".9"></rect>')
    return s


def fill_path(p: str, g: str, d: str) -> str:
    col, pat, op = GROUP_STYLE[g]
    s = f'<path d="{d}" fill="{col}"></path>'
    if pat:
        s += f'<path d="{d}" fill="url(#{p}-{pat})" opacity="{op}"></path>'
    return s


def swatch(p: str, g: str, x: float, y: float) -> str:
    return fill_rect(p, g, x, y, 20, 13, outline=True)


def relax(ideal: list[float], gap: float, lo: float, hi: float) -> list[float]:
    """Spread label centres (sorted top to bottom) so neighbours are at least gap apart, inside [lo, hi]."""
    ys = [min(max(v, lo), hi) for v in ideal]
    for _ in range(60):
        prev = ys[:]
        for i in range(1, len(ys)):          # push down
            ys[i] = max(ys[i], ys[i - 1] + gap)
        ys[-1] = min(ys[-1], hi)
        for i in range(len(ys) - 2, -1, -1):  # push up
            ys[i] = min(ys[i], ys[i + 1] - gap)
        ys[0] = max(ys[0], lo)
        # pull each label back toward its ideal where there is room
        for i in range(len(ys)):
            a = ys[i - 1] + gap if i else lo
            b = ys[i + 1] - gap if i < len(ys) - 1 else hi
            if a <= b:
                ys[i] = min(max(ideal[i], a), b)
        if max(abs(p - q) for p, q in zip(prev, ys)) < .05:
            break
    return ys


def key_entry(p: str, g: str | None, x: float, y: float, name: str, lines: list[str], mono: bool = True) -> str:
    """One keyed-index entry drawn in the chart's own SVG: swatch, name, then code lines. y = name baseline."""
    out = []
    tx = x
    if g:
        out.append(swatch(p, g, x, y - 11))
        tx = x + 30
    out.append(f'<text x="{f(tx)}" y="{f(y)}" class="kn">{name}</text>')
    for i, ln in enumerate(lines):
        cls = "kc" if mono else "kd"
        out.append(f'<text x="{f(tx)}" y="{f(y + 18 + i * 16)}" class="{cls}">{ln}</text>')
    return "".join(out)


# ================================================================ chart geometry shared by all four
SVG_W = 944
PX0, PW = 64, 624           # plot area x and width; the keyed index starts at KX
KX = 718
PX1 = PX0 + PW


def ts(s: str) -> datetime:
    return datetime.fromisoformat(s)


# ---------------------------------------------------------------- FUELHH: stack of never-negative codes + signed panels
def chart_fuelhh(p: str = "fh") -> tuple[str, int]:
    c = SPEC["elexon/fuelhh"]["chart"]
    g = c["palette_groups_mw"]
    n = len(c["hours_utc"])
    groups = {
        "nuclear": g["nuclear"], "biomass": g["biomass"],
        "hyd": [g["uncovered:NPSHYD"][i] + g["uncovered:COAL"][i] + g["uncovered:OIL"][i] for i in range(n)],
        "other": g["other"], "gas": g["gas"], "wind": g["wind"],
    }
    order = ["nuclear", "biomass", "hyd", "other", "gas", "wind"]   # bottom to top
    k = 0.009                       # px per MW, the same in all three panels
    A_TOP, A_MAX = 34, 32000
    A_BASE = A_TOP + A_MAX * k      # 322
    B_ZERO = A_BASE + 58 + 7000 * k
    C_ZERO = B_ZERO + 7000 * k + 50 + 1600 * k
    AX_Y = C_ZERO + 1600 * k + 16
    H = int(AX_Y + 34)
    xs = [PX0 + (i + .5) * PW / n for i in range(n)]

    o = [f'<defs>{pat_defs(p)}</defs>']
    # stack
    acc = [0.0] * n
    tops = {}
    for name in order:
        lo = acc[:]
        hi = [acc[i] + groups[name][i] for i in range(n)]
        dn = " ".join(f"L{f(xs[i])} {f(A_BASE - lo[i] * k)}" for i in range(n - 1, -1, -1))
        d = (f"M{f(xs[0])} {f(A_BASE - hi[0] * k)} "
             + " ".join(f"L{f(xs[i])} {f(A_BASE - hi[i] * k)}" for i in range(1, n)) + " " + dn + " Z")
        o.append(fill_path(p, name, d))
        tops[name] = (lo, hi)
        acc = hi
    # daylight partings between bands, then the ink silhouette on top
    for name in order[:-1]:
        hi = tops[name][1]
        o.append(f'<path d="M' + " L".join(f"{f(xs[i])} {f(A_BASE - hi[i] * k)}" for i in range(n)) +
                 f'" fill="none" stroke="{DAY}" stroke-width=".8" opacity=".9"></path>')
    top = tops["wind"][1]
    o.append(f'<path d="M' + " L".join(f"{f(xs[i])} {f(A_BASE - top[i] * k)}" for i in range(n)) +
             f'" fill="none" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"></path>')

    # signed panels: area between the series and its own zero, same scale
    def signed(series: list[float], zero: float, grp: str) -> str:
        pts = " ".join(f"L{f(xs[i])} {f(zero - series[i] * k)}" for i in range(n))
        d = f"M{f(xs[0])} {f(zero)} {pts} L{f(xs[-1])} {f(zero)} Z"
        line = "M" + " L".join(f"{f(xs[i])} {f(zero - series[i] * k)}" for i in range(n))
        return (fill_path(p, grp, d) +
                f'<path d="{line}" fill="none" stroke="{INK}" stroke-width="1.1" stroke-linejoin="round"></path>')

    o.append(signed(g["imports"], B_ZERO, "imports"))
    o.append(signed(g["uncovered:PS"], C_ZERO, "ps"))

    # axes: one vertical ink axis per panel, zero rules, a few ticks
    ax = [f"M{PX0} {A_TOP - 8} V{f(A_BASE)} H{PX1}",
          f"M{PX0} {f(B_ZERO - 7000 * k)} V{f(B_ZERO + 7000 * k)}", f"M{PX0} {f(B_ZERO)} H{PX1}",
          f"M{PX0} {f(C_ZERO - 1600 * k)} V{f(C_ZERO + 1600 * k)}", f"M{PX0} {f(C_ZERO)} H{PX1}"]
    ticks, labels = [], []
    for v in (10000, 20000, 30000):
        y = A_BASE - v * k
        ticks.append(f"M{PX0 - 5} {f(y)} H{PX0}")
        labels.append(f'<text x="{PX0 - 9}" y="{f(y + 4.5)}" text-anchor="end">{num(v)}</text>')
    labels.append(f'<text x="{PX0 - 9}" y="{f(A_BASE + 4.5)}" text-anchor="end">0</text>')
    for v in (5000, -5000):
        y = B_ZERO - v * k
        ticks.append(f"M{PX0 - 5} {f(y)} H{PX0}")
        labels.append(f'<text x="{PX0 - 9}" y="{f(y + 4.5)}" text-anchor="end">{num(v)}</text>')
    labels.append(f'<text x="{PX0 - 9}" y="{f(B_ZERO + 4.5)}" text-anchor="end">0</text>')
    for v in (1500, -1500):
        y = C_ZERO - v * k
        ticks.append(f"M{PX0 - 5} {f(y)} H{PX0}")
        labels.append(f'<text x="{PX0 - 9}" y="{f(y + 4.5)}" text-anchor="end">{num(v)}</text>')
    labels.append(f'<text x="0" y="{f(A_TOP - 14)}" class="ax-u">MW</text>')
    o.append(f'<path d="{" ".join(ax)} {" ".join(ticks)}" stroke="{INK}" stroke-width="1.2" fill="none"></path>')
    # days: settlement dates start at 23:00 UTC in September (BST)
    t0 = ts(c["hours_utc"][0])
    day_ticks, day_lab = [], []
    for dd in range(8):
        x = PX0 + dd * 24 * PW / n
        day_ticks.append(f"M{f(x)} {f(AX_Y - 5)} V{f(AX_Y + 1)}")
        if dd < 7:
            day_lab.append(f'<text x="{f(x + 12 * PW / n)}" y="{f(AX_Y + 17)}" text-anchor="middle">'
                           f'{20 + dd} Sep</text>')
    o.append(f'<path d="M{PX0} {f(AX_Y)} H{PX1} {" ".join(day_ticks)}" stroke="{INK}" stroke-width="1" '
             f'fill="none"></path>')
    o.append(f'<g class="ax">{"".join(labels)}{"".join(day_lab)}</g>')
    _ = t0

    # plate labels inside the panels (Hanken italic, lower case)
    o.append(f'<g class="pl">'
             f'<text x="{PX0 + 12}" y="{A_TOP + 4}">the nine codes never negative in silver, stacked</text>'
             f'<text x="{PX0 + 12}" y="{f(B_ZERO - 7000 * k + 2)}">interconnectors, net</text>'
             f'<text x="{PX0 + 12}" y="{f(C_ZERO - 1600 * k - 8)}">pumped storage</text></g>')

    # the keyed index: one entry per band, level with the band's right end
    names = {"wind": ("wind", ["WIND"]), "gas": ("gas", ["CCGT, OCGT"]),
             "other": ("other (vendor code)", ["OTHER"]),
             "hyd": ("hydro, coal, oil", ["NPSHYD, COAL, OIL"]),
             "biomass": ("biomass", ["BIOMASS"]), "nuclear": ("nuclear", ["NUCLEAR"])}
    top_down = list(reversed(order))
    ideal = [A_BASE - (tops[nm][0][-1] + tops[nm][1][-1]) / 2 * k for nm in top_down]
    ys = relax(ideal, 40, A_TOP + 6, A_BASE - 8)
    lead = []
    for nm, yi, yk in zip(top_down, ideal, ys):
        lab, codes = names[nm]
        o.append(key_entry(p, nm, KX, yk + 4, lab, codes))
        lead.append(f"M{f(PX1 + 3)} {f(yi)} L{f(PX1 + 12)} {f(yi)} L{f(KX - 6)} {f(yk)}")
    o.append(f'<path d="{" ".join(lead)}" stroke="{INK}" stroke-width=".8" fill="none" opacity=".6"></path>')
    o.append(key_entry(p, "imports", KX, B_ZERO - 44, "interconnectors, net",
                       ["INTELEC INTEW INTFR INTGRNL", "INTIFA2 INTIRL INTNED INTNEM", "INTNSL INTVKL"]))
    o.append(f'<text x="{KX + 30}" y="{f(B_ZERO + 30)}" class="kd">above zero is import to GB,</text>'
             f'<text x="{KX + 30}" y="{f(B_ZERO + 46)}" class="kd">below zero is export</text>')
    o.append(key_entry(p, "ps", KX, C_ZERO - 6, "pumped storage", ["PS"]))
    o.append(f'<text x="{KX + 30}" y="{f(C_ZERO + 29)}" class="kd">signed, sign undocumented</text>')

    aria = ("Chart of elexon/fuelhh, 20 to 26 September 2026, hourly means in MW. Top panel: the nine fuel codes that "
            "are never negative, stacked: nuclear about 3,300 to 4,000 at the base, biomass, non-pumped hydro with "
            "coal and oil, OTHER, gas (CCGT and OCGT) and wind on top, wind ranging from about 16,000 MW at the start "
            "of 20 September down to about 1,300. Middle panel, same scale: net "
            "interconnector flow, from about 6,300 MW export to 6,600 MW import. Bottom panel: pumped storage, "
            "signed, within 1,500 MW of zero.")
    svg = (f'<svg width="{SVG_W}" height="{H}" viewBox="0 0 {SVG_W} {H}" role="img" aria-label="{esc(aria)}">'
           + "".join(o) + "</svg>")
    return svg, H


# ---------------------------------------------------------------- system prices: one step line, negatives hatched
def chart_prices(p: str = "sp") -> tuple[str, int]:
    c = SPEC["elexon/system_prices"]["chart"]
    v = c["ssp_gbp_per_mwh"]
    n = len(v)
    k = 0.5
    TOP, VMAX, VMIN = 34, 600, -100
    ZERO = TOP + VMAX * k
    BOT = ZERO - VMIN * k
    AX_Y = BOT + 14
    H = int(AX_Y + 34)
    dx = PW / n
    y = lambda val: ZERO - val * k  # noqa: E731
    o = [f'<defs>{pat_defs(p)}<pattern id="{p}-neg" width="5" height="5" patternUnits="userSpaceOnUse">'
         f'<path d="M0 5 L5 0 M-1 1 L1 -1 M4 6 L6 4" stroke="{INK}" stroke-width=".8"></path></pattern></defs>']
    # below-zero periods: hatched between the step and zero
    negs = []
    for i, val in enumerate(v):
        if val < 0:
            negs.append(f'<rect x="{f(PX0 + i * dx)}" y="{f(ZERO)}" width="{f(dx)}" height="{f(-val * k)}"></rect>')
    o.append(f'<g fill="{TOP}">{"".join(negs)}</g>')
    o.append(f'<g fill="url(#{p}-neg)">{"".join(negs)}</g>')
    # axes
    ticks, labels = [], []
    for tv in (200, 400, 600, -100):
        ticks.append(f"M{PX0 - 5} {f(y(tv))} H{PX0}")
        labels.append(f'<text x="{PX0 - 9}" y="{f(y(tv) + 4.5)}" text-anchor="end">{num(tv)}</text>')
    labels.append(f'<text x="{PX0 - 9}" y="{f(ZERO + 4.5)}" text-anchor="end">0</text>')
    labels.append(f'<text x="0" y="{f(TOP - 14)}" class="ax-u">GBP/MWh</text>')
    o.append(f'<path d="M{PX0} {TOP - 8} V{f(BOT)} {" ".join(ticks)}" stroke="{INK}" stroke-width="1.2" '
             f'fill="none"></path>')
    o.append(f'<path d="M{PX0} {f(ZERO)} H{PX1}" stroke="{INK}" stroke-width="1.2"></path>')
    # the step line: one level per settlement period
    d = f"M{f(PX0)} {f(y(v[0]))}"
    for i in range(n):
        if i:
            d += f" V{f(y(v[i]))}"
        d += f" H{f(PX0 + (i + 1) * dx)}"
    o.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"></path>')
    # days
    day_ticks, day_lab = [], []
    for dd in range(5):
        x = PX0 + dd * 48 * dx
        day_ticks.append(f"M{f(x)} {f(AX_Y - 5)} V{f(AX_Y + 1)}")
        if dd < 4:
            day_lab.append(f'<text x="{f(x + 24 * dx)}" y="{f(AX_Y + 17)}" text-anchor="middle">{19 + dd} Sep</text>')
    o.append(f'<path d="M{PX0} {f(AX_Y)} H{PX1} {" ".join(day_ticks)}" stroke="{INK}" stroke-width="1" '
             f'fill="none"></path>')
    o.append(f'<g class="ax">{"".join(labels)}{"".join(day_lab)}</g>')
    # annotate the extremes where they sit
    t_all = [ts(t) for t in c["t_utc"]]
    imax = t_all.index(ts(c["max"]["at_utc"]))
    imin = t_all.index(ts(c["negatives"]["min_at_utc"]))
    xm, xn = PX0 + (imax + .5) * dx, PX0 + (imin + .5) * dx
    o.append(f'<path d="M{f(xm - 4)} {f(y(v[imax]))} H{f(xm - 26)} M{f(xn)} {f(y(v[imin]) + 3)} V{f(y(v[imin]) + 18)}" '
             f'stroke="{INK}" stroke-width=".8" opacity=".7"></path>')
    o.append(f'<g class="pl"><text x="{f(xm - 30)}" y="{f(y(v[imax]) + 4.5)}" text-anchor="end">high: 594.00 at 20:00 UTC,'
             f' 22 Sep</text>'
             f'<text x="{f(xn)}" y="{f(y(v[imin]) + 32)}" text-anchor="middle">low: {num(v[imin], 2)} at 13:30 UTC,'
             f' 20 Sep</text></g>')
    # keyed index
    last_y = y(v[-1])
    o.append(key_entry(p, None, KX, last_y + 4, "system sell price", ["SSP, one step per period"], mono=False))
    o.append(f'<path d="M{f(PX1 + 3)} {f(last_y)} H{f(KX - 6)}" stroke="{INK}" stroke-width=".8" opacity=".6"></path>')
    o.append(f'<text x="{KX}" y="{f(last_y + 38)}" class="kd">SBP is identical in every period</text>')
    ky = ZERO + 16
    o.append(f'<rect x="{KX}" y="{f(ky - 11)}" width="20" height="13" fill="{TOP}"></rect>'
             f'<rect x="{KX}" y="{f(ky - 11)}" width="20" height="13" fill="url(#{p}-neg)"></rect>'
             f'<rect x="{KX}" y="{f(ky - 11)}" width="20" height="13" fill="none" stroke="{INK}" stroke-width=".9"></rect>')
    o.append(f'<text x="{KX + 30}" y="{f(ky)}" class="kn">below zero</text>'
             f'<text x="{KX + 30}" y="{f(ky + 18)}" class="kd">34 of the 192 periods</text>')
    aria = ("Step chart of the system sell price, elexon/system_prices, settlement dates 19 to 22 September 2026, "
            "GBP/MWh, one step per half-hour settlement period. The price is below zero "
            "in 34 of 192 periods, with a low of minus 50.00 at 13:30 UTC on 20 September, and spike to 594.00 at "
            "20:00 UTC on 22 September.")
    return (f'<svg width="{SVG_W}" height="{H}" viewBox="0 0 {SVG_W} {H}" role="img" aria-label="{esc(aria)}">'
            + "".join(o) + "</svg>"), H


# ---------------------------------------------------------------- ENTSOG: fourteen daily points, a broken time axis
def chart_flows(p: str = "pf") -> tuple[str, int]:
    c = SPEC["entsog/physical_flows"]["chart"]
    ser = {s["point_label"]: s for s in c["series"]}
    fergus = [pt["flow_gwh_per_day"] for pt in ser["St. Fergus"]["points"]]
    bacton = [pt["flow_gwh_per_day"] for pt in ser["Bacton (IUK)"]["points"]]
    days = [ts(pt["timestamp_utc"]).date() for pt in ser["St. Fergus"]["points"]]
    k = 0.5
    TOP, VMAX = 34, 600
    ZERO = TOP + VMAX * k
    AX_Y = ZERO + 16
    H = int(AX_Y + 52)
    D = 34                                  # px per gas day inside a block
    b1 = [i for i, d in enumerate(days) if d.month == 8]
    b2 = [i for i, d in enumerate(days) if d.month == 9]
    x1s = PX0 + D / 2
    GAP_L = PX0 + len(b1) * D
    GAP_R = PX1 - len(b2) * D
    xs = {}
    for j, i in enumerate(b1):
        xs[i] = x1s + j * D
    for j, i in enumerate(b2):
        xs[i] = GAP_R + D / 2 + j * D
    y = lambda val: ZERO - val * k  # noqa: E731
    o = []
    # the gap: no rows, drawn as an empty, labelled stretch
    o.append(f'<rect x="{f(GAP_L)}" y="{TOP - 8}" width="{f(GAP_R - GAP_L)}" height="{f(ZERO - TOP + 8)}" '
             f'fill="{TOP_FILL}"></rect>')
    o.append(f'<path d="M{f(GAP_L)} {TOP - 8} V{f(ZERO)} M{f(GAP_R)} {TOP - 8} V{f(ZERO)}" stroke="{INK}" '
             f'stroke-width=".7" opacity=".35"></path>')
    gx = (GAP_L + GAP_R) / 2
    o.append(f'<g class="pl" text-anchor="middle"><text x="{f(gx)}" y="{f(TOP + 118)}">no rows</text>'
             f'<text x="{f(gx)}" y="{f(TOP + 136)}">6 Aug to 12 Sep</text></g>')
    # axes
    ticks, labels = [], []
    for tv in (200, 400, 600):
        ticks.append(f"M{PX0 - 5} {f(y(tv))} H{PX0}")
        labels.append(f'<text x="{PX0 - 9}" y="{f(y(tv) + 4.5)}" text-anchor="end">{tv}</text>')
    labels.append(f'<text x="{PX0 - 9}" y="{f(ZERO + 4.5)}" text-anchor="end">0</text>')
    labels.append(f'<text x="0" y="{f(TOP - 14)}" class="ax-u">GWh/d</text>')
    o.append(f'<path d="M{PX0} {TOP - 8} V{f(ZERO)} {" ".join(ticks)}" stroke="{INK}" stroke-width="1.2" '
             f'fill="none"></path>')
    # zero rule broken at the gap, with break marks
    o.append(f'<path d="M{PX0} {f(ZERO)} H{f(GAP_L + 6)} M{f(GAP_R - 6)} {f(ZERO)} H{PX1}" stroke="{INK}" '
             f'stroke-width="1.2"></path>')
    o.append(f'<path d="M{f(GAP_L + 1)} {f(ZERO + 6)} l10 -12 M{f(GAP_L + 7)} {f(ZERO + 6)} l10 -12 '
             f'M{f(GAP_R - 17)} {f(ZERO + 6)} l10 -12 M{f(GAP_R - 11)} {f(ZERO + 6)} l10 -12" stroke="{INK}" '
             f'stroke-width="1.2"></path>')
    # the two series, lines only within a block
    def line(vals: list[float], col: str, wdt: str) -> str:
        segs = []
        for blk in (b1, b2):
            segs.append("M" + " L".join(f"{f(xs[i])} {f(y(vals[i]))}" for i in blk))
        return f'<path d="{" ".join(segs)}" fill="none" stroke="{col}" stroke-width="{wdt}" stroke-linejoin="round"></path>'
    o.append(line(fergus, CLAY, "2"))
    o.append(line(bacton, INK, "1.5"))
    o.append("".join(f'<circle cx="{f(xs[i])}" cy="{f(y(fergus[i]))}" r="3.6" fill="{CLAY}" stroke="{INK}" '
                     f'stroke-width="1"></circle>' for i in xs))
    o.append("".join(f'<circle cx="{f(xs[i])}" cy="{f(y(bacton[i]))}" r="3.4" fill="{DAY}" stroke="{INK}" '
                     f'stroke-width="1.3"></circle>' for i in xs))
    o.append(f'<g class="pl"><text x="{f(xs[b2[0]] - 4)}" y="{f(ZERO - 12)}">0.0 on 13 to 20 Sep, as reported</text></g>')
    # day labels under each point, month under each block
    dl = "".join(f'<text x="{f(xs[i])}" y="{f(AX_Y + 4)}" text-anchor="middle">{days[i].day}</text>' for i in xs)
    o.append(f'<g class="ax">{"".join(labels)}{dl}'
             f'<text x="{f((xs[b1[0]] + xs[b1[-1]]) / 2)}" y="{f(AX_Y + 24)}" text-anchor="middle" class="ax-m">August 2026</text>'
             f'<text x="{f((xs[b2[0]] + xs[b2[-1]]) / 2)}" y="{f(AX_Y + 24)}" text-anchor="middle" class="ax-m">September 2026</text></g>')
    # keyed index, level with each series' last point
    yf, yb = y(fergus[-1]), y(bacton[-1])
    o.append(f'<circle cx="{KX + 10}" cy="{f(yf - 5)}" r="3.6" fill="{CLAY}" stroke="{INK}" stroke-width="1"></circle>'
             f'<path d="M{KX} {f(yf - 5)} H{KX + 20}" stroke="{CLAY}" stroke-width="2"></path>')
    o.append(f'<text x="{KX + 30}" y="{f(yf)}" class="kn">St. Fergus, entry</text>'
             f'<text x="{KX + 30}" y="{f(yf + 18)}" class="kc">ITP-00022</text>'
             f'<text x="{KX + 30}" y="{f(yf + 35)}" class="kd">559.186 on 21 Sep</text>')
    o.append(f'<path d="M{KX} {f(yb - 5)} H{KX + 20}" stroke="{INK}" stroke-width="1.5"></path>'
             f'<circle cx="{KX + 10}" cy="{f(yb - 5)}" r="3.4" fill="{DAY}" stroke="{INK}" stroke-width="1.3"></circle>')
    o.append(f'<text x="{KX + 30}" y="{f(yb)}" class="kn">Bacton (IUK), exit</text>'
             f'<text x="{KX + 30}" y="{f(yb + 18)}" class="kc">ITP-00005</text>'
             f'<text x="{KX + 30}" y="{f(yb + 35)}" class="kd">175.166 on 21 Sep</text>')
    o.append(f'<path d="M{f(PX1 - D / 2 + 5)} {f(yf)} H{KX - 6} M{f(PX1 - D / 2 + 5)} {f(yb)} H{KX - 6}" stroke="{INK}" '
             f'stroke-width=".8" opacity=".6"></path>')
    o.append(f'<text x="{KX}" y="{f(ZERO - 20)}" class="kd">both reported by</text>'
             f'<text x="{KX}" y="{f(ZERO - 4)}" class="kd">National Gas TSO</text>')
    aria = ("Chart of entsog/physical_flows in GWh/d for two points reported by National Gas TSO, one value per gas "
            "day, 1 to 5 August and 13 to 21 September 2026, with the axis broken over 6 August to 12 September, "
            "where there are no rows. St. Fergus entry runs from 433.651 down to 350.288 in August and from 473.217 "
            "up to 594.565 in September, ending at 559.186. Bacton (IUK) exit is about 382 to 407 in August, 0.0 from "
            "13 to 20 September and 175.166 on 21 September.")
    return (f'<svg width="{SVG_W}" height="{H}" viewBox="0 0 {SVG_W} {H}" role="img" aria-label="{esc(aria)}">'
            + "".join(o) + "</svg>"), H


TOP_FILL = "#EFEBDF"   # --zebra: the gap's quiet ground


# ---------------------------------------------------------------- BMUNITS: no time axis, so the registry's make-up
def chart_units(p: str = "bm") -> tuple[str, int]:
    c = SPEC["elexon/bmunits_reference"]["chart"]
    bars = {b["fuel_type"]: b["units"] for b in c["bars"]}
    total = sum(bars.values())                       # 3,014
    null = bars["(null)"]
    typed = total - null                             # 499
    grp_of = {"WIND": "wind", "OTHER": "other", "CCGT": "gas", "OCGT": "gas", "NPSHYD": "hyd", "COAL": "hyd",
              "NUCLEAR": "nuclear", "PS": "ps", "BIOMASS": "biomass"}
    ints = {kk: vv for kk, vv in bars.items() if kk.startswith("INT")}
    o = [f'<defs>{pat_defs(p)}</defs>']
    # the whole registry as one bar
    BY, BH = 44, 30
    sc = PW / total
    xn = PX0 + null * sc
    o.append(f'<rect x="{PX0}" y="{BY}" width="{f(null * sc)}" height="{BH}" fill="{DAY}"></rect>'
             f'<rect x="{PX0}" y="{BY}" width="{f(null * sc)}" height="{BH}" fill="url(#{p}-null)" opacity=".4"></rect>')
    seq = [("wind", bars["WIND"]), ("other", bars["OTHER"]), ("gas", bars["CCGT"] + bars["OCGT"]),
           ("hyd", bars["NPSHYD"] + bars["COAL"]), ("nuclear", bars["NUCLEAR"]), ("ps", bars["PS"]),
           ("biomass", bars["BIOMASS"]), ("imports", sum(ints.values()))]
    x = xn
    for g, cnt in seq:
        o.append(fill_rect(p, g, x, BY, cnt * sc, BH))
        x += cnt * sc
    o.append(f'<rect x="{PX0}" y="{BY}" width="{PW}" height="{BH}" fill="none" stroke="{INK}" stroke-width="1.3"></rect>'
             f'<path d="M{f(xn)} {BY - 6} V{BY + BH + 6}" stroke="{INK}" stroke-width="1.3"></path>')
    o.append(f'<g class="ax"><text x="{PX0}" y="{BY - 12}">no fuel type: 2,515 units (83%)</text>'
             f'<text x="{f(PX1)}" y="{BY - 12}" text-anchor="end">fuel type set: 499</text></g>')
    # the 499, opened out below
    RY0 = BY + BH + 58
    RH = 27
    rows = sorted([(kk, vv) for kk, vv in bars.items() if kk in grp_of], key=lambda t: -t[1])
    rows.insert(next(i for i, r in enumerate(rows) if r[1] < 11), ("INT", sum(ints.values())))
    LX = PX0 + 118            # bars start
    s2 = 1.9                  # px per unit
    o.append(f'<path d="M{f(xn)} {BY + BH} L{PX0} {RY0 - 16} M{PX1} {BY + BH} L{PX1} {RY0 - 16}" stroke="{INK}" '
             f'stroke-width=".8" opacity=".45"></path>')
    for j, (code, cnt) in enumerate(rows):
        yy = RY0 + j * RH
        g = "imports" if code == "INT" else grp_of[code]
        o.append(fill_rect(p, g, LX, yy, cnt * s2, 15, outline=True))
        lab = "INT (10 codes)" if code == "INT" else code
        o.append(f'<text x="{LX - 12}" y="{yy + 12}" text-anchor="end" class="kc kc-b">{lab}</text>'
                 f'<text x="{f(LX + cnt * s2 + 8)}" y="{yy + 12}" class="bn">{cnt}</text>')
    RY1 = RY0 + len(rows) * RH
    tk = " ".join(f"M{f(LX + t * s2)} {RY1 + 2} V{RY1 + 8}" for t in (0, 100, 200))
    o.append(f'<path d="M{LX} {RY0 - 8} V{RY1 + 2} H{f(LX + 250 * s2)} {tk}" stroke="{INK}" stroke-width="1.1" '
             f'fill="none"></path>')
    o.append('<g class="ax">' + "".join(
        f'<text x="{f(LX + t * s2)}" y="{RY1 + 24}" text-anchor="middle">{t}</text>' for t in (0, 100, 200))
        + f'<text x="{f(LX + 250 * s2)}" y="{RY1 + 24}" text-anchor="end" class="ax-u">units</text></g>')
    H = RY1 + 36
    # keyed index
    o.append(f'<rect x="{KX}" y="{BY + 4}" width="20" height="13" fill="{DAY}"></rect>'
             f'<rect x="{KX}" y="{BY + 4}" width="20" height="13" fill="url(#{p}-null)" opacity=".4"></rect>'
             f'<rect x="{KX}" y="{BY + 4}" width="20" height="13" fill="none" stroke="{INK}" stroke-width=".9"></rect>'
             f'<text x="{KX + 30}" y="{BY + 15}" class="kn">fuel_type is null</text>'
             f'<text x="{KX + 30}" y="{BY + 33}" class="kd">2,515 of 3,014 units</text>')
    ky = RY0 + 6
    o.append(f'<text x="{KX}" y="{ky}" class="kn">The ten INT codes</text>'
             f'<text x="{KX}" y="{ky + 20}" class="kc">INTELEC 2</text>'
             f'<text x="{KX}" y="{ky + 38}" class="kc">INTEW INTFR INTGRNL</text>'
             f'<text x="{KX}" y="{ky + 54}" class="kc">INTIFA2 INTIRL INTNED</text>'
             f'<text x="{KX}" y="{ky + 70}" class="kc">INTNEM INTNSL INTVKL</text>'
             f'<text x="{KX}" y="{ky + 88}" class="kd">one unit each</text>')
    aria = ("Chart of elexon/bmunits_reference, snapshot of 26 September 2026, counting BM units. A bar of all 3,014 "
            "units: 2,515 (83%) have no fuel type, 499 have one. Those 499 by code: WIND 234, OTHER 92, CCGT 61, "
            "OCGT 22, NPSHYD 22, NUCLEAR 16, PS 16, BIOMASS 15, the ten INT codes 11 (INTELEC 2, the rest 1 each), "
            "COAL 10.")
    return (f'<svg width="{SVG_W}" height="{H}" viewBox="0 0 {SVG_W} {H}" role="img" aria-label="{esc(aria)}">'
            + "".join(o) + "</svg>"), H


# ================================================================ the fact rail's coverage strip
RW = 280


def coverage(kind: str) -> str:
    """Local silver coverage drawn to scale along the rail. Ink where rows exist, nothing where they do not."""
    H = 44
    y0, bh = 8, 9
    o = []
    if kind in ("fuelhh", "system_prices"):
        a, b = date(2021, 9, 1), date(2026, 9, 26 if kind == "fuelhh" else 22)
        span = (date(2026, 12, 31) - a).days
        X = lambda d: 1 + (d - a).days / span * (RW - 2)  # noqa: E731
        o.append(f'<rect x="{f(X(a))}" y="{y0}" width="{f(X(b) - X(a))}" height="{bh}" fill="{INK}"></rect>')
        if kind == "fuelhh":
            xg = X(date(2026, 9, 8))
            o.append(f'<path d="M{f(xg)} {y0 - 3} V{y0 + bh + 3}" stroke="{DAY}" stroke-width="1.6"></path>'
                     f'<path d="M{f(xg)} {y0 + bh + 3} V{y0 + bh + 8}" stroke="{INK}" stroke-width="1"></path>')
        yrs = "".join(f'<text x="{f(X(date(yr, 1, 1)))}" y="{H - 4}" text-anchor="middle">{yr}</text>'
                      for yr in range(2022, 2027))
        tk = " ".join(f"M{f(X(date(yr, 1, 1)))} {y0 + bh + 1} V{y0 + bh + 5}" for yr in range(2022, 2027))
        o.append(f'<path d="M1 {y0 + bh + 1} H{RW - 1} {tk}" stroke="{INK}" stroke-width=".8" fill="none"></path>')
        o.append(f'<g class="cv">{yrs}</g>')
        aria = ("Coverage from 1 September 2021 to " + ("26" if kind == "fuelhh" else "22") + " September 2026"
                + (", with a mark at the missing days, 7 to 9 September 2026" if kind == "fuelhh" else ""))
    elif kind == "physical_flows":
        a, b = date(2026, 8, 1), date(2026, 9, 22)
        span = (b - a).days
        X = lambda d: 1 + (d - a).days / span * (RW - 2)  # noqa: E731
        for s, e in ((date(2026, 8, 1), date(2026, 8, 6)), (date(2026, 9, 13), date(2026, 9, 22))):
            o.append(f'<rect x="{f(X(s))}" y="{y0}" width="{f(X(e) - X(s) - .6)}" height="{bh}" fill="{INK}"></rect>')
        tk = " ".join(f"M{f(X(d))} {y0 + bh + 1} V{y0 + bh + 5}" for d in (date(2026, 9, 1),))
        o.append(f'<path d="M1 {y0 + bh + 1} H{RW - 1} {tk}" stroke="{INK}" stroke-width=".8" fill="none"></path>')
        o.append(f'<g class="cv"><text x="1" y="{H - 4}">1 Aug</text>'
                 f'<text x="{f(X(date(2026, 9, 1)))}" y="{H - 4}" text-anchor="middle">1 Sep</text>'
                 f'<text x="{RW - 1}" y="{H - 4}" text-anchor="end">21 Sep</text></g>')
        aria = "Coverage: 1 to 5 August and 13 to 21 September 2026, nothing between"
    else:
        o.append(f'<path d="M1 {y0 + bh + 1} H{RW - 1}" stroke="{INK}" stroke-width=".8" opacity=".4"></path>'
                 f'<circle cx="{RW - 6}" cy="{y0 + bh / 2 + 1}" r="5" fill="{INK}"></circle>')
        o.append(f'<g class="cv"><text x="{RW - 1}" y="{H - 4}" text-anchor="end">26 Sep 2026</text></g>')
        aria = "One snapshot, 26 September 2026"
    return (f'<svg class="cov" width="{RW}" height="{H}" viewBox="0 0 {RW} {H}" role="img" aria-label="{aria}">'
            + "".join(o) + "</svg>")


# ================================================================ the thin horizon under the title band
def turbine(x: float, base: float, h: float, blade: float, spin: str, ang: float, col: str = DAY) -> str:
    s = h / 80
    t0, t1 = 2.3 * s, 1.05 * s
    hy = base - h
    tower = (f'<path d="M{f(x - t0)} {f(base)} L{f(x - t1)} {f(hy)} L{f(x + t1)} {f(hy)} L{f(x + t0)} {f(base)} Z" '
             f'fill="{col}"></path>')
    bw = max(blade * 0.075, 1.1)
    L = blade
    bd = (f"M{f(-bw * .55)} 0 C{f(-bw * 1.15)} {f(-L * .3)} {f(-bw * .45)} {f(-L * .76)} 0 {f(-L)} "
          f"C{f(bw * .3)} {f(-L * .72)} {f(bw * 1.25)} {f(-L * .3)} {f(bw * .55)} 0 Z")
    blades = "".join(f'<path d="{bd}" transform="rotate({f(ang + kk * 120)})" fill="{col}"></path>' for kk in range(3))
    return (tower + f'<g transform="translate({f(x)},{f(hy)})"><g class="rot {spin}"><circle r="{f(L)}" fill="none">'
            f'</circle>{blades}<circle r="{f(2.1 * s)}" fill="{col}"></circle></g></g>')


PYL = ("M-18 0 L-5 -96 M18 0 L5 -96 M-5 -96 L-5 -118 M5 -96 L5 -118 M-5 -118 H5 M-14 -28 H14 M-11 -56 H11 "
       "M-8 -80 H8 M-16 -14 L14 -28 M16 -14 L-14 -28 M-13 -42 L11 -56 M13 -42 L-11 -56 M-10 -68 L8 -80 M10 -68 L-8 -80 "
       "M-30 -66 H30 M-24 -92 H24 M-14 -112 H14 M-30 -66 L-5 -60 M30 -66 L5 -60 M-24 -92 L-5 -86 M24 -92 L5 -86")

HZ_H = 92


def horizon() -> str:
    """A thin, quiet horizon: far ridge, a few rotors, one pylon run, the energised land and the cut."""
    surf = lambda x: 80 + 1.6 * math.sin(x / 170 + .4) - 1.1 * math.sin(x / 71 + 1.2)  # noqa: E731
    o = []
    far = [(-20, 60), (140, 50), (330, 56), (520, 44), (700, 52), (880, 58), (1060, 48), (1250, 55), (1460, 50)]
    o.append(f'<path d="{smooth(far)} L1460 {HZ_H} L-20 {HZ_H} Z" fill="{HORIZON}" opacity=".45"></path>')
    near = [(-20, 70), (110, 62), (240, 58), (380, 64), (520, 70), (640, 76)]
    o.append(f'<path d="{smooth(near)} L640 {HZ_H} L-20 {HZ_H} Z" fill="{HORIZON}"></path>')
    for i, (tx, hh) in enumerate([(96, 34), (176, 40), (262, 36), (348, 31)]):
        yb = 62 + [2, -2, -1, 2][i] + 1
        o.append(turbine(tx, yb, hh, hh * .5, ["sp2", "sp1", "sp3", "sp1"][i], 23 * i + 12))
    land = [(-20, 74), (300, 72), (620, 75), (900, 73), (1200, 74), (1460, 72)]
    bottom = " ".join(f"L{f(x)} {f(surf(x))}" for x in range(1460, -21, -20))
    o.append(f'<path d="{smooth(land)} {bottom} Z" fill="{CHART}"></path>')
    # pylons on the land, catenary between them
    pxs = [760, 940, 1120, 1300]
    sc = .27
    wires = []
    for a, b in zip(pxs[:-1], pxs[1:]):
        for dy in (66, 92):
            ya = surf(a) - dy * sc
            yb = surf(b) - dy * sc
            for side in (-1, 1):
                ax_, bx_ = a + side * (30 if dy == 66 else 24) * sc, b + side * (30 if dy == 66 else 24) * sc
                wires.append(f"M{f(ax_)} {f(ya)} Q{f((ax_ + bx_) / 2)} {f(max(ya, yb) + 3.5)} {f(bx_)} {f(yb)}")
    o.append(f'<g stroke="{INK}" fill="none" stroke-linecap="round" stroke-width="1">' + "".join(
        f'<g transform="translate({x},{f(surf(x))}) scale({sc})"><path vector-effect="non-scaling-stroke" d="{PYL}">'
        f'</path></g>' for x in pxs) + '</g>')
    o.append(f'<path d="{" ".join(wires)}" stroke="{INK}" stroke-width=".6" fill="none" opacity=".75"></path>')
    # the cut: ink surface line, a thin olive root, then the reading ground
    sd = "M" + " L".join(f"{f(x)} {f(surf(x))}" for x in range(-20, 1461, 20))
    o.append(f'<path d="{sd} L1460 {HZ_H} L-20 {HZ_H} Z" fill="{DAY}"></path>')
    root = sd + " " + " ".join(f"L{f(x)} {f(surf(x) + 5)}" for x in range(1460, -21, -20)) + " Z"
    o.append(f'<path d="{root}" fill="{OLIVE}"></path>')
    o.append(f'<path d="{sd}" stroke="{INK}" stroke-width="1.5" fill="none"></path>')
    return (f'<svg class="hz" width="{W}" height="{HZ_H}" viewBox="0 0 {W} {HZ_H}" aria-hidden="true">'
            + "".join(o) + "</svg>")


def deep_edge(h: int) -> str:
    """The page's footing: one wavy contact line from the reading ground into the deep, granite below."""
    top = 26
    pts = [(x, top + 7 * math.sin(x / 150 + 1) + 4 * math.sin(x / 57 + 2) + 2.5 * math.sin(x / 21))
           for x in range(-40, W + 41, 20)]
    d = smooth(pts)
    body = f"{d} L{W + 40} {h + 10} L-40 {h + 10} Z"
    return (f'<svg class="deep-bg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" aria-hidden="true"><defs>'
            f'<pattern id="p-granite" width="46" height="40" patternUnits="userSpaceOnUse"><path d="M8 8 h8 M12 4 v8 '
            f'M30 26 h8 M34 22 v8 M20 34 h6 M23 31 v6 M40 6 h5 M42.5 3.5 v5" stroke="{HORIZON}" stroke-width="1.1">'
            f'</path></pattern></defs><path d="{body}" fill="{PETROL}"></path>'
            f'<path d="{body}" fill="url(#p-granite)" opacity=".5"></path>'
            f'<path d="{d}" stroke="{INK}" stroke-width="2" fill="none" stroke-linejoin="round"></path></svg>')


# ================================================================ content: one dict per specimen
def hl(code: str) -> str:
    """Tint the string literals in a line of Python (as on the homepage notebook)."""
    return re.sub(r'"[^"]*"', lambda m: f'<span class="s">{m.group(0)}</span>', code)


def wrap_call(call: str) -> str:
    """The workbench call, token for token, broken at its argument commas to fit the rail."""
    head, _, rest = call.partition("(")
    args = rest[:-1]
    parts = [a.strip() for a in args.split(",")]
    if len(parts) == 3:
        body = f'{head}(\n    {parts[0]},\n    {parts[1]}, {parts[2]})'
    else:
        body = f'{head}(\n    {", ".join(parts)})'
    return hl(esc(body).replace("&quot;", '"'))


def df_table(cols: list[str], rows: list[list[str]], num_cols: set[str]) -> str:
    head = "<tr>" + "".join(f"<th>{esc(c)}</th>" for c in cols) + "</tr>"
    body = ""
    for r in rows:
        body += "<tr>" + "".join(
            f'<td class="{"nul" if v == "null" else ("t" if c not in num_cols else "")}">{esc(v)}</td>'.replace(
                ' class=""', "") for c, v in zip(cols, r)) + "</tr>"
    return f'<table class="df"><thead>{head}</thead><tbody>{body}</tbody></table>'


def zfmt(s: str) -> str:
    return s.replace("+00:00", "Z")


def val(v: object) -> str:
    if v is None:
        return "null"
    if isinstance(v, float):
        return repr(v)
    return zfmt(str(v))


def schema_table(sid: str) -> str:
    cols = SPEC[sid]["schema"]["columns"]
    main = [c for c in cols if c["origin"] != "lineage"]
    lin = [c for c in cols if c["origin"] == "lineage"]
    MEAN = MEANINGS[sid]

    def row(c: dict) -> str:
        return (f'<tr><td class="c">{esc(c["column"])}</td><td class="ty">{esc(c["dtype"])}</td>'
                f'<td class="m">{MEAN[c["column"]]}</td></tr>')

    lin_names = ", ".join(f"<code>{c['column']}</code>" for c in lin)
    return (f'<table class="schema"><thead><tr><th>Column</th><th>Type</th><th>Meaning</th></tr></thead>'
            f'<tbody>{"".join(row(c) for c in main)}</tbody>'
            f'<tbody class="lin"><tr><td class="c">lineage</td><td class="ty">{len(lin)} columns</td>'
            f'<td class="m">{lin_names}. Added by the silver layer, not the Pydantic class; '
            f'<code>query()</code> and <code>tail()</code> drop them.</td></tr></tbody></table>')


# Column meanings: condensed from the pack's schema meanings (citations moved to the side note).
MEANINGS = {
    "elexon/fuelhh": {
        "settlement_date": "GB settlement date, derived from the vendor start time since v2.0.0",
        "settlement_period": "Half-hour within the date, 1 to 50 (46 or 50 on clock-change days)",
        "timestamp_utc": "Start of the half-hour, UTC (vendor startTime)",
        "fuel_type": "Elexon fuel-type code, upper case as sent",
        "generation_mw": "MW for the period. INT codes are signed, positive is import to GB; PS is signed, "
                         "meaning undocumented",
        "published_at": "Vendor publication time",
        "data_provider": "Always <code>elexon</code>",
        "ingested_at": "When the silver transform ran, not the bronze fetch",
    },
    "elexon/system_prices": {
        "settlement_date": "GB settlement date",
        "settlement_period": "Half-hour within the date, 1 to 50",
        "timestamp_utc": "Period start, UTC",
        "system_sell_price": "SSP, GBP/MWh; schema bound −500 to 10,000",
        "system_buy_price": "SBP, GBP/MWh; same bound",
        "net_imbalance_volume": "NIV, MWh. Sign convention not documented in code or vault",
        "run_type": "Null on every row: this endpoint has no such field",
        "price_derivation_code": "Vendor code: N 49,764 rows, P 47,019, K 10. The vault reads N as normal, "
                                 "P as provisional; K is unknown",
        "published_at": "Vendor createdDateTime",
        "data_provider": "Always <code>elexon</code>",
        "ingested_at": "When the silver transform ran",
    },
    "entsog/physical_flows": {
        "timestamp_utc": "Gas-day start (vendor periodFrom), UTC; the hour varies by operator",
        "point_key": "ENTSOG point id, e.g. ITP-00005",
        "point_label": "Point name, e.g. Bacton (IUK)",
        "operator_key": "Reporting operator id, e.g. UK-TSO-0001",
        "operator_label": "Operator name, e.g. National Gas TSO",
        "direction_key": "entry or exit, relative to the reporting operator’s system (inferred from paired "
                         "values, not documented)",
        "flow_gwh_per_day": "Flow normalised to GWh/d from the vendor value and unit. Nullable",
        "unit": "Always GWh/d after normalisation",
        "data_provider": "Always <code>entsog</code>",
        "ingested_at": "When the silver transform ran. In silver but not declared in the Pydantic class",
    },
    "elexon/bmunits_reference": {
        "bm_unit_id": "Elexon BM unit id (vendor elexonBmUnit); the key",
        "bm_unit_name": "Vendor bmUnitName; often repeats the id",
        "fuel_type": "Vendor fuelType; null on 2,515 of 3,014 rows",
        "registered_capacity_mw": "Vendor generationCapacity, MW; per registration, not additive across rows",
        "company_name": "Vendor leadPartyName",
        "gsp_group_id": "Vendor gspGroupId, e.g. _A; null on 1,822 rows",
        "national_grid_bm_unit": "Vendor nationalGridBmUnit, e.g. ABERU-1; not the ENTSO-E EIC",
        "data_provider": "Always <code>elexon</code>",
        "ingested_at": "When the silver transform ran",
    },
}


def sample_block(sid: str) -> tuple[str, str]:
    rows = SPEC[sid]["sample_rows"]["rows"]
    if sid == "elexon/fuelhh":
        cols = ["settlement_date", "settlement_period", "timestamp_utc", "fuel_type", "generation_mw", "published_at"]
        numc = {"settlement_period", "generation_mw"}
        note = ("Settlement date 2026-09-26, period 25: 8 of the 20 codes. Every row also has "
                "<code>data_provider</code> elexon and <code>dataset_version</code> 2.0.0.")
    elif sid == "elexon/system_prices":
        cols = ["settlement_period", "timestamp_utc", "system_sell_price", "system_buy_price", "net_imbalance_volume",
                "published_at"]
        numc = {"settlement_period", "system_sell_price", "system_buy_price", "net_imbalance_volume"}
        note = ("Settlement date 2026-09-20, periods 22 to 29, one vintage each, values as stored. "
                "<code>price_derivation_code</code> is N and <code>run_type</code> null on every row shown.")
    elif sid == "entsog/physical_flows":
        cols = ["point_key", "point_label", "operator_key", "operator_label", "direction_key", "flow_gwh_per_day"]
        numc = {"flow_gwh_per_day"}
        note = ("Gas day 2026-09-21, <code>timestamp_utc</code> 04:00Z and <code>unit</code> GWh/d on every row. "
                "Bacton (IUK) appears twice, once from each operator.")
    else:
        cols = ["bm_unit_id", "bm_unit_name", "fuel_type", "registered_capacity_mw", "company_name", "gsp_group_id",
                "national_grid_bm_unit"]
        numc = {"registered_capacity_mw"}
        note = "Eight units from the 2026-09-26 snapshot, <code>dataset_version</code> 1.1.0."
    data = [[val(r[c]) for c in cols] for r in rows]
    return df_table(cols, data, numc), note


COPY: dict[str, dict] = {
    "elexon/fuelhh": {
        "slug": "fuelhh", "vendor": "Elexon BMRS", "key": "elexon/fuelhh", "cov": "fuelhh",
        "title": "Generation by fuel type",                                             # NEW COPY
        "lede": "Half-hourly GB generation outturn in MW, one value per settlement period for each Elexon "
                "fuel-type code.",                                                        # pack what_it_is, reworded
        "facts": [
            ("Vendor dataset", "<code>FUELHH</code>, Half-hourly Generation Outturn by Fuel Type"),
            ("Grain", "One row per settlement period and fuel-type code"),
            ("Cadence", "30 minutes"),
            ("History", "1 Sep 2021 to 26 Sep 2026 in local silver; 7 to 9 Sep 2026 are missing"),
            ("Publication lag", "At the period end, 30 min after its start, on 99.82% of rows; the longest is "
                                "271 min"),
            ("Units", "MW; the interconnector codes and PS are signed"),
            ("Rows", "1,682,517; 17 to 20 per half-hour"),
            ("Silver table", "<code>silver_elexon_fuelhh</code>"),
        ],
        "fig_h": "Hourly outturn, 20 to 26 September 2026",                              # NEW COPY
        "chart": chart_fuelhh,
        "cap": "<code>elexon/fuelhh</code>, silver, MW. Settlement dates 20 to 26 September 2026: 336 half-hours "
               "drawn as 168 hourly points, each the mean of a code’s two half-hours, with a group’s codes summed "
               "first. The signed interconnectors and PS sit in their own panels on the same scale. Day ticks mark "
               "each settlement date’s start, 23:00 UTC.",                              # NEW COPY
        "what": "For every half-hour settlement period, Elexon publishes GB generation outturn by fuel type. "
                "Gridflow keeps one row per period and fuel-type code, upper case as sent: 20 codes in a recent "
                "half-hour, ten of them interconnectors. Interconnector and pumped-storage values are signed. There "
                "is no solar code.",                                                      # NEW COPY (46 words)
        "uses": ["Wind and gas outturn as features for residual-demand and price models.",
                 "Actuals to score a wind generation forecast against.",
                 "Tracking the fuel mix and interconnector flows over a week or a year."],  # NEW COPY
        "caveats": [
            ("There is no solar code.", "Solar outturn is not in this dataset; it has to come from another one."),
            ("Eleven codes are signed:", "the ten interconnector codes, where positive is import to GB, and PS. "
             "Negatives are routine: INTIRL is negative in 70.3% of all half-hours, PS in 54.7%."),
            ("The code set changes over time.", "INTELEC starts on 14 Sep 2021, INTVKL on 12 Jul 2023 and INTGRNL "
             "on 19 Mar 2024, so a half-hour holds 17 to 20 rows."),
        ],
        "schema_note": "Pydantic class <code>ElexonFuelHH</code> in <code>gridflow/schemas/elexon.py</code>. "
                       "Transformer version 2.0.0.",
        "call": 'data.elexon.query("fuelhh", "2026-09-20", "2026-09-26")',
        "call_extra": None,
        "wb_note": "Reads <code>silver_elexon_fuelhh</code> and filters <code>settlement_date</code> inclusively: "
                   "6,720 rows for this range. Returns a pandas DataFrame. <code>query(\"fuel_generation\", ...)</code> "
                   "is an alias of the same table.",
        "endpoint": "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELHH?publishDateTimeFrom=<UTC Z>"
                    "&publishDateTimeTo=<UTC Z>&page=<n>",
        "ep_note": None,
        "related": [("elexon/fuelinst", "Same connector: instantaneous outturn by fuel type."),
                    ("elexon/bmunits_reference", "Shares the fuel-type vocabulary."),
                    ("elexon/indo", "The demand series the interconnector sign is checked against."),
                    ("neso_data_portal/historic_generation_mix", "Carries the solar outturn this dataset lacks.")],
    },
    "elexon/system_prices": {
        "slug": "system-prices", "vendor": "Elexon BMRS", "key": "elexon/system_prices", "cov": "system_prices",
        "title": "System sell and buy prices",                                          # NEW COPY
        "lede": "GB imbalance (cash-out) prices in GBP/MWh, with net imbalance volume, for every half-hour "
                "settlement period.",
        "facts": [
            ("Vendor dataset", "<code>DISEBSP</code>, System Sell Price and System Buy Price per settlement period"),
            ("Grain", "One row per settlement period and vendor publication, so a period can repeat"),
            ("Cadence", "30 minutes"),
            ("History", "1 Sep 2021 to 22 Sep 2026 in local silver, no missing dates"),
            ("Publication lag", "Median 52 min after the period start in 2021 to 2023, about 24.7 h in 2024 to "
                                "2026; the cause is not established"),
            ("Units", "GBP/MWh; net imbalance volume in MWh"),
            ("Rows", "96,793 for 88,694 periods"),
            ("Silver table", "<code>silver_elexon_system_prices_latest</code>, a view with one row per period"),
        ],
        "fig_h": "System sell price, 19 to 22 September 2026",
        "chart": chart_prices,
        "cap": "<code>elexon/system_prices</code>, silver, latest vintage per period, GBP/MWh. Settlement dates 19 "
               "to 22 September 2026: 192 native half-hourly values, one step each, not averaged. Day ticks mark "
               "each settlement date’s start, 23:00 UTC.",
        "what": "The system sell price (SSP) and system buy price (SBP) settle imbalances in GB: Elexon publishes one "
                "pair per half-hour settlement period, with the net imbalance volume in MWh. Silver keeps every "
                "vendor publication of a period, so a period can appear more than once. Since September 2021 the two "
                "prices have been equal on every row.",                                  # NEW COPY (55 words)
        "uses": ["The target for an imbalance-price model.",
                 "Measuring how often, and how far, prices go negative.",
                 "The spread between day-ahead prices (elexon/mid) and cash-out."],
        "caveats": [
            ("Silver is append-only:", "96,793 rows cover 88,694 periods. Read the <code>_latest</code> view, as "
             "the workbench does, or dedupe on <code>available_at</code> before plotting."),
            ("SSP equals SBP", "on every row since September 2021, so one line carries both."),
            ("Negative prices are routine:", "4,052 periods since September 2021 (latest vintage), and 34 of the "
             "192 in the chart."),
        ],
        "schema_note": "Pydantic class <code>ElexonSystemPrice</code> in <code>gridflow/schemas/elexon.py</code>. "
                       "Transformer version 2.0.0, append-only.",
        "call": 'data.elexon.query("system_prices", "2026-09-19", "2026-09-22")',
        "call_extra": None,
        "wb_note": "Reads <code>silver_elexon_system_prices_latest</code>, so vintages are already collapsed to one "
                   "row per period; raw parquet is not. Returns a pandas DataFrame. "
                   "<code>data.imbalance_context(start, end)</code> adds NESO carbon intensity.",
        "endpoint": "GET https://data.elexon.co.uk/bmrs/api/v1/balancing/settlement/system-prices/{YYYY-MM-DD}"
                    "?page=<n>",
        "ep_note": None,
        "related": [("neso/carbon_intensity", "Joined with this in the workbench’s imbalance context."),
                    ("elexon/mid", "The day-ahead benchmark the workbench reads.")],
    },
    "entsog/physical_flows": {
        "slug": "physical-flows", "vendor": "ENTSO-G", "key": "entsog/physical_flows", "cov": "physical_flows",
        "title": "Physical gas flows",
        "lede": "Daily physical gas flow for each point, operator and direction on European transmission systems, "
                "in GWh/d.",
        "facts": [
            ("Vendor dataset", "<code>operationalData</code>, indicator Physical Flow"),
            ("Grain", "One row per gas day, point, operator and direction"),
            ("Cadence", "Daily, by gas day; the start hour varies by operator"),
            ("History", "14 gas days in local silver: 1 to 5 Aug and 13 to 21 Sep 2026"),
            ("Publication lag", "Not established: silver keeps the ingest time, not the vendor’s update time"),
            ("Units", "GWh/d on every row"),
            ("Rows", "13,764; about 983 per gas day"),
            ("Silver table", "<code>silver_entsog_physical_flows</code>"),
        ],
        "fig_h": "Flow at two GB points, every gas day held",
        "chart": chart_flows,
        "cap": "<code>entsog/physical_flows</code>, silver, GWh/d. One native value per gas day, 04:00 UTC, with "
               "nothing averaged across points. There are no rows from 6 August to 12 September, so the axis breaks "
               "there and nothing is interpolated.",
        "what": "The ENTSO-G Transparency Platform reports the physical gas flow at each point for every gas day, "
                "once for each reporting operator and direction. Gridflow normalises every value to GWh/d. Local "
                "silver holds 620 points and 48 operators, and each gas day starts at the operator’s own hour.",
        "uses": ["Tracking flows at GB entry and exit points such as St. Fergus and Bacton.",
                 "Supply-side features for gas demand or price models.",
                 "Comparing nominations (entsog/nominations) with physical flow."],
        "caveats": [
            ("Only 14 gas days are held,", "in two blocks: 1 to 5 August and 13 to 21 September 2026."),
            ("Both sides of a point report,", "so summing every row double counts. At Bacton (IUK) on 21 September "
             "the National Gas TSO exit and the Interconnector entry are both 175.165952 GWh/d."),
            ("Flows can be null:", "2,499 rows, including every day for 176 series such as Avonmouth LNG entry. "
             "Do not zero-fill."),
        ],
        "schema_note": "Pydantic class <code>EntsogPhysicalFlow</code> in <code>gridflow/schemas/entsog.py</code>. "
                       "Transformer version 1.0.0.",
        "call": 'data.entsog.query("physical_flows", "2026-09-13", "2026-09-21")',
        "call_extra": None,
        "wb_note": "Reads <code>silver_entsog_physical_flows</code> and filters <code>timestamp_utc</code> from "
                   "2026-09-13T00:00Z to before 2026-09-22T00:00Z. Returns a pandas DataFrame. Operators whose gas "
                   "day starts at 21:00 to 23:00Z on the previous date fall outside the first day.",
        "endpoint": "GET https://transparency.entsog.eu/api/v1/operationalData?limit=-1&timeZone=UCT"
                    "&from=YYYY-MM-DD&to=YYYY-MM-DD&indicator=Physical%20Flow&periodType=day",
        "ep_note": "No <code>pointDirection</code>: a full-system fetch.",
        "related": [("entsog/aggregated_physical_flows", "The same indicator at zone level."),
                    ("entsog/nominations", "Same endpoint, Nomination indicator."),
                    ("entsog/allocations", "Same endpoint, Allocation indicator.")],
    },
    "elexon/bmunits_reference": {
        "slug": "bmunits-reference", "vendor": "Elexon BMRS", "key": "elexon/bmunits_reference", "cov": "snapshot",
        "title": "Balancing Mechanism units",
        "lede": "A snapshot of every registered Balancing Mechanism unit: id, name, fuel type, capacity, lead party "
                "and GSP group.",
        "facts": [
            ("Vendor dataset", "<code>/reference/bmunits/all</code>, All BM Unit reference data"),
            ("Grain", "One row per BM unit"),
            ("Cadence", "A snapshot, on a weekly schedule"),
            ("History", "One snapshot, 26 Sep 2026, overwritten on each run: 3,014 units, where the vault "
                        "recorded 2,969 on 9 Sep"),
            ("Publication lag", "Not established"),
            ("Units", "MW, registered capacity"),
            ("Rows", "3,014; 499 with a fuel type"),
            ("Silver table", "<code>silver_elexon_bmunits_reference</code>"),
        ],
        "fig_h": "BM units by fuel type, snapshot of 26 September 2026",
        "chart": chart_units,
        "cap": "<code>elexon/bmunits_reference</code>, silver snapshot of 26 September 2026, count of BM units per "
               "<code>fuel_type</code> with nulls kept. There is no time axis. Capacity is not summed: it is per "
               "registration and not additive.",
        "what": "Elexon’s reference list of Balancing Mechanism units, fetched whole in one call. Gridflow keeps a "
                "single snapshot and overwrites it on each run, so there is no history. It names the units behind "
                "per-unit datasets such as elexon/boal and elexon/pn: name, lead party, registered capacity and, "
                "for 499 of 3,014, a fuel type.",
        "uses": ["Labelling per-unit data (elexon/boal, elexon/pn) with a name, lead party and fuel type.",
                 "Selecting the wind or CCGT units for a unit-level study.",
                 "Grouping units by lead party: 379 companies."],
        "caveats": [
            ("Most units have no fuel type:", "2,515 of 3,014 (83%), so a fuel breakdown covers 499 units."),
            ("Capacity is not additive.", "It is per registration: null-fuel rows alone sum to 727,551 MW, and "
             "1,315 ids start <code>I_</code>, which the vault describes as per-party interconnector registrations."),
            ("<code>query()</code> returns nothing here.", "The manifest’s date column is <code>ingested_at</code>, "
             "so a date range returns 0 rows. Use <code>tail()</code> or <code>sql()</code>."),
        ],
        "schema_note": "Pydantic class <code>ElexonBMUnit</code> in <code>gridflow/schemas/elexon.py</code>. "
                       "Transformer version 1.1.0.",
        "call": 'data.elexon.tail("bmunits_reference", n=3014)',
        "call_extra": 'data.sql("SELECT * FROM silver_elexon_bmunits_reference")',
        "wb_note": "<code>tail()</code> orders by <code>ingested_at</code>, newest first; <code>sql()</code> is "
                   "read-only. Both return a pandas DataFrame. Do not use <code>query()</code>: it filters on "
                   "<code>ingested_at</code> and returns 0 rows for a date range.",
        "endpoint": "GET https://data.elexon.co.uk/bmrs/api/v1/reference/bmunits/all",
        "ep_note": "No parameters and no pagination.",
        "related": [("elexon/boal", "Per-unit data, joined on <code>bm_unit_id</code>."),
                    ("elexon/pn", "Per-unit data, joined on <code>bm_unit_id</code>."),
                    ("elexon/uou2t14d", "Per-unit availability."),
                    ("elexon/fuelhh", "Shares the fuel-type vocabulary and carries interconnector flow.")],
    },
}

SETUP = ('<span class="k">from</span> gridflow_models <span class="k">import</span> setup_notebook\n'
         'data, models, common = setup_notebook()')


# ================================================================ the template
CSS = """body{margin:0}
.root{background:#F6F4EC;color:#1C2B22;font:400 16px/1.6 "Hanken Grotesk",sans-serif;font-variant-numeric:tabular-nums;-webkit-font-smoothing:antialiased}
.root a{color:inherit;text-decoration-thickness:1.5px;text-underline-offset:4px;text-decoration-color:#66793B}
.root a:focus-visible{outline:2px solid #AFC64E;outline-offset:3px;border-radius:2px}
.root h1,.root h2,.root h3{font-family:"Bricolage Grotesque",sans-serif;margin:0;font-optical-sizing:auto}
.root code{font-family:"Red Hat Mono",monospace;font-size:.88em}
.mast{display:flex;justify-content:space-between;align-items:baseline;padding:26px 80px 0;background:#155A6E;color:#F6F4EC}
.brand{font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:24px;letter-spacing:-.01em;text-decoration:none}
.mast ul{display:flex;gap:30px;list-style:none;margin:0;padding:0;font-size:15px}
.mast ul a{text-decoration:none;color:#CFE0DC}
.mast ul a:hover{color:#F6F4EC}
.mast ul a[aria-current="page"]{color:#F6F4EC;box-shadow:inset 0 -2px 0 #AFC64E}
.band{background:#155A6E;color:#F6F4EC}
.grid{display:grid;grid-template-columns:280px minmax(0,1fr);column-gap:56px;padding:0 80px}
.dhead{padding-top:50px;align-items:baseline;row-gap:0}
.crumbs ol{list-style:none;margin:0 0 14px;padding:0;display:flex;flex-wrap:wrap;font-size:14.5px;line-height:1.4;color:#CFE0DC}
.crumbs li+li::before{content:"/";padding:0 8px;color:#B4D0CD}
.crumbs a{text-decoration-color:rgba(175,198,78,.8)}
.dkey{margin:0;font:500 18px/1.3 "Red Hat Mono",monospace;color:#F6F4EC}
.dhead h1{font-size:64px;font-weight:760;font-stretch:84%;line-height:.96;letter-spacing:-.022em;color:#F6F4EC}
.dvend{margin:14px 0 0;font-size:14.5px;line-height:1.5;color:#CFE0DC;align-self:start;padding-top:4px}
.dvend code{font-size:13.5px;color:#F6F4EC}
.lede{margin:14px 0 0;font-size:18px;line-height:1.55;color:#CFE0DC;max-width:56ch}
.hz{display:block;margin-top:18px}
.ov{padding-top:58px;align-items:start}
.rail{position:sticky;top:24px}
.facts{margin:0}
.facts div{padding:8px 0 9px;border-top:1px solid rgba(28,43,34,.22)}
.facts div:last-child{border-bottom:1px solid rgba(28,43,34,.22)}
.facts dt{font-size:13.5px;font-weight:600;line-height:1.3;color:#3F4A3B}
.facts dd{margin:2px 0 0;font-size:14.5px;line-height:1.45;color:#1C2B22}
.facts dd code{font-size:13.5px}
.cov{display:block;margin:9px 0 1px}
.cov text,.cv text{font:400 12px "Hanken Grotesk",sans-serif;fill:#3F4A3B}
.call{margin:18px 0 0}
.call p{margin:0 0 7px;font-size:13.5px;font-weight:600;color:#3F4A3B}
.well{margin:0;background:#ECE8DA;border:1px solid rgba(28,43,34,.18);border-radius:3px;padding:9px 12px;font:400 13.5px/1.6 "Red Hat Mono",monospace;color:#1C2B22;white-space:pre}
.well .s{color:#7C5530}
.well .k{color:#155A6E;font-weight:500}
.call .alt{margin:8px 0 0;font-size:13.5px;line-height:1.45;color:#3F4A3B}
.main h2{font-size:30px;font-weight:700;font-stretch:90%;line-height:1.08;letter-spacing:-.012em}
.fig{margin:0}
.fig h2{margin:0 0 20px}
.fig svg{display:block}
.fig figcaption{margin:14px 0 0;font-size:14.5px;line-height:1.55;color:#3F4A3B;max-width:66ch}
.fig figcaption code{font-size:13px;color:#1C2B22}
.fig text{font-family:"Hanken Grotesk",sans-serif}
.ax text,.ax{font-size:13px;fill:#3F4A3B}
.ax-u{font-weight:600}
.ax-m{font-weight:600;fill:#1C2B22}
.pl text,.pl{font-style:italic;font-size:13.5px;fill:#1C2B22}
.pl-s text{font-size:13px}
.kn{font-size:14.5px;font-weight:600;fill:#1C2B22}
.kc{font-family:"Red Hat Mono",monospace;font-size:12.5px;fill:#155A6E}
.kc-b{font-size:13.5px;fill:#1C2B22}
.kcode{font-family:"Red Hat Mono",monospace;font-size:12.5px}
.kd{font-size:13px;fill:#3F4A3B}
.bn{font-size:13px;font-weight:600;fill:#1C2B22}
.two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);column-gap:48px;margin-top:64px}
.two h2{margin:0 0 12px}
.two p{margin:0;font-size:16px;line-height:1.62;color:#3F4A3B;max-width:58ch}
.uses{list-style:none;margin:0;padding:0}
.uses li{padding:9px 0 10px;border-top:1px solid rgba(28,43,34,.22);font-size:16px;line-height:1.5;color:#1C2B22}
.uses li:first-child{border-top:0;padding-top:0}
.cav{margin-top:60px}
.cav h2{margin:0 0 14px}
.cav ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));column-gap:32px}
.cav li{padding-top:14px;border-top:1.5px solid #1C2B22;font-size:15px;line-height:1.55;color:#3F4A3B}
.cav strong{font-weight:650;color:#1C2B22}
.cav code{font-size:13.5px;color:#1C2B22}
.ref{margin-top:88px}
.row{padding-top:26px;padding-bottom:56px;border-top:1px solid rgba(28,43,34,.22);align-items:start}
.row:last-child{padding-bottom:88px}
.side h2{font-size:30px;font-weight:700;font-stretch:90%;line-height:1.08;letter-spacing:-.012em}
.side p{margin:10px 0 0;font-size:14.5px;line-height:1.5;color:#3F4A3B}
.side code{font-size:13px;color:#1C2B22}
.schema{width:100%;border-collapse:collapse}
.schema th{text-align:left;font-size:13.5px;font-weight:600;color:#1C2B22;padding:5px 18px 8px 0;border-bottom:1px solid #1C2B22}
.schema td{padding:9px 18px 9px 0;border-bottom:1px solid rgba(28,43,34,.22);vertical-align:baseline}
.schema .c{font:500 14px/1.4 "Red Hat Mono",monospace;color:#1C2B22;white-space:nowrap}
.schema .ty{font:400 13px/1.4 "Red Hat Mono",monospace;color:#155A6E;white-space:nowrap}
.schema .m{font-size:14.5px;line-height:1.5;color:#3F4A3B}
.schema .m code{font-size:13px;color:#1C2B22}
.schema .lin td{border-bottom:0;padding-top:14px}
.schema .lin .c{font:italic 400 14.5px/1.4 "Hanken Grotesk",sans-serif;color:#3F4A3B}
.df{border-collapse:collapse;font:400 13px/1 "Hanken Grotesk",sans-serif;font-variant-numeric:tabular-nums;color:#1C2B22}
.df th,.df td{padding:7px 9px;text-align:right;white-space:nowrap}
.df thead th{font-weight:600;border-bottom:1px solid #1C2B22;vertical-align:bottom}
.df tbody tr:nth-child(odd){background:#EFEBDF}
.df td.nul{color:#5d6a55;font-style:italic}
.get{display:grid;row-gap:26px}
.get h3{font-size:20px;font-weight:700;font-stretch:90%;line-height:1.15;margin:0 0 10px}
.get p{margin:10px 0 0;font-size:14.5px;line-height:1.55;color:#3F4A3B;max-width:78ch}
.get p code{font-size:13px;color:#1C2B22}
.cell{display:grid;grid-template-columns:40px minmax(0,1fr);column-gap:10px;margin:0 0 8px}
.pr{font:400 13px/1 "Red Hat Mono",monospace;color:#5d6a55;text-align:right;padding-top:12px}
.in{margin:0;background:#ECE8DA;border:1px solid rgba(28,43,34,.18);border-radius:3px;padding:8px 12px;font:400 14.5px/1.6 "Red Hat Mono",monospace;color:#1C2B22;white-space:pre}
.in .k{color:#155A6E;font-weight:500}
.in .s{color:#7C5530}
.ep{margin:0;background:#ECE8DA;border:1px solid rgba(28,43,34,.18);border-radius:3px;padding:9px 12px;font:400 14px/1.6 "Red Hat Mono",monospace;color:#1C2B22;white-space:pre-wrap}
.rel{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:48px}
.rel li{padding:11px 0 12px;border-bottom:1px solid rgba(28,43,34,.22)}
.rel a{font:500 15px/1.4 "Red Hat Mono",monospace;color:#1C2B22}
.rel p{margin:3px 0 0;font-size:14.5px;line-height:1.45;color:#3F4A3B}
.rel code{font-size:13px}
.deep{position:relative;color:#F6F4EC}
.deep-bg{position:absolute;left:0;top:0}
.fin{position:relative;display:grid;grid-template-columns:280px minmax(0,1fr) auto;column-gap:56px;padding:86px 80px 64px;align-items:start}
.fin .brand{display:inline-block;color:#F6F4EC}
.fin p{margin:0;font-size:15.5px;line-height:1.6;color:#CFE0DC;max-width:52ch}
.fin ul{list-style:none;margin:0;padding:0}
.fnav ul{display:flex;flex-wrap:wrap;gap:8px 26px;margin-top:18px;font-size:15px}
.fnav a{text-decoration:none;color:#CFE0DC}
.fnav a:hover{color:#F6F4EC}
.links{display:flex;flex-wrap:wrap;gap:12px}
.links a{font-weight:600;padding:10px 18px;border-radius:3px;text-decoration:none;border:1.5px solid rgba(207,224,220,.55);color:#F6F4EC}
.links a:hover{border-color:#F6F4EC}
.rot{transform-box:fill-box;transform-origin:center;animation:spin 17s linear infinite}
.sp2{animation-duration:13s}
.sp3{animation-duration:21s}
@keyframes spin{to{transform:rotate(360deg)} }
@media (prefers-reduced-motion: reduce){.rot{animation:none} }
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,'
         '200..800&amp;family=Hanken+Grotesk:ital,wght@0,400..700;1,400..600&amp;family=Red+Hat+Mono:wght@400;500'
         '&amp;display=swap" rel="stylesheet">')

FOOT_H = 250
ABOUT_LINE = ("Gridflow is a personal research platform for UK and European power markets: a medallion data "
              "pipeline, vendor catalogue and probabilistic modelling stack.")   # existing homepage copy


def endpoint_html(ep: str) -> str:
    """The endpoint as a reference manual sets it: base URL, then one query parameter per line (whitespace only)."""
    base, q, rest = ep.partition("?")
    if not q:
        return esc(ep)
    params = rest.split("&")
    return esc(base) + "\n    ?" + "\n    &amp;".join(esc(x) for x in params)


def page(sid: str, height: int) -> str:
    c = COPY[sid]
    svg, _ = c["chart"]()
    vend = next(v for k, v in c["facts"] if k == "Vendor dataset")
    facts = "".join(f"<div><dt>{k}</dt><dd>{v}{coverage(c['cov']) if k == 'History' else ''}</dd></div>"
                    for k, v in c["facts"] if k != "Vendor dataset")
    alt = ""
    if c["call_extra"]:
        alt = (f'<p class="alt">or read-only SQL:</p><pre class="well">{wrap_sql(c["call_extra"])}</pre>')
    rail = (f'<aside class="rail" aria-label="Facts about this dataset"><dl class="facts">{facts}</dl>'
            f'<div class="call"><p>Workbench call</p><pre class="well">{wrap_call(c["call"])}</pre>{alt}</div></aside>')
    uses = "".join(f"<li>{u}</li>" for u in c["uses"])
    cav = "".join(f"<li><strong>{a}</strong> {b}</li>" for a, b in c["caveats"])
    main = (f'<div class="main">'
            f'<figure class="fig" aria-labelledby="fig-h"><h2 id="fig-h">{c["fig_h"]}</h2>{svg}'
            f'<figcaption>{c["cap"]}</figcaption></figure>'
            f'<div class="two"><section aria-labelledby="what-h"><h2 id="what-h">What it is</h2><p>{c["what"]}</p>'
            f'</section><section aria-labelledby="use-h"><h2 id="use-h">How it’s used</h2><ul class="uses">{uses}</ul>'
            f'</section></div>'
            f'<section class="cav" aria-labelledby="cav-h"><h2 id="cav-h">Caveats</h2><ul>{cav}</ul></section></div>')
    df, snote = sample_block(sid)
    cells = (f'<div class="cell"><span class="pr">[1]:</span><pre class="in">{SETUP}</pre></div>'
             f'<div class="cell"><span class="pr">[2]:</span><pre class="in">{hl(esc(c["call"]).replace("&quot;", chr(34)))}'
             f'</pre></div>')
    if c["call_extra"]:
        cells += (f'<div class="cell"><span class="pr">[3]:</span><pre class="in">'
                  f'{hl(esc(c["call_extra"]).replace("&quot;", chr(34)))}</pre></div>')
    ep_note = f'<p>{c["ep_note"]}</p>' if c["ep_note"] else ""
    cli = "\n".join(esc(x) for x in SPEC[sid]["how_to_get_it"]["cli"])
    related = "".join(f'<li><a href="#">{esc(k)}</a><p>{v}</p></li>' for k, v in c["related"])
    ref = (
        f'<div class="ref">'
        f'<section class="grid row" aria-labelledby="sch-h"><div class="side"><h2 id="sch-h">Schema</h2>'
        f'<p>{c["schema_note"]}</p></div><div>{schema_table(sid)}</div></section>'
        f'<section class="grid row" aria-labelledby="smp-h"><div class="side"><h2 id="smp-h">Sample rows</h2>'
        f'<p>{snote}</p></div><div>{df}</div></section>'
        f'<section class="grid row" aria-labelledby="get-h"><div class="side"><h2 id="get-h">How to get it</h2></div>'
        f'<div class="get"><div><h3>Workbench</h3>{cells}<p>{c["wb_note"]}</p></div>'
        f'<div><h3>Vendor endpoint</h3><pre class="ep">{endpoint_html(c["endpoint"])}</pre>{ep_note}</div>'
        f'<div><h3>Command line</h3><pre class="ep">{cli}</pre></div></div></section>'
        f'<section class="grid row" aria-labelledby="rel-h"><div class="side"><h2 id="rel-h">Related datasets</h2>'
        f'</div><ul class="rel">{related}</ul></section>'
        f'</div>')
    nav = ('<header class="mast"><a class="brand" href="#">gridflow</a><nav aria-label="Primary"><ul>'
           '<li><a href="#">Home</a></li><li><a href="#" aria-current="page">Data sources</a></li>'
           '<li><a href="#">Architecture</a></li><li><a href="#">Models</a></li><li><a href="#">About</a></li>'
           '</ul></nav></header>')
    head = (f'<section class="band" aria-labelledby="title"><div class="grid dhead">'
            f'<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="#">Data sources</a></li>'
            f'<li><a href="#">{esc(c["vendor"])}</a></li></ol></nav><span></span>'
            f'<p class="dkey">{esc(c["key"])}</p><h1 id="title">{c["title"]}</h1>'
            f'<p class="dvend">{vend}</p><p class="lede">{c["lede"]}</p></div>{horizon()}</section>')
    foot = (f'<footer class="deep">{deep_edge(FOOT_H)}<div class="fin">'
            f'<div><a class="brand" href="#">gridflow</a></div>'
            f'<div><p>{ABOUT_LINE}</p><nav class="fnav" aria-label="Footer"><ul><li><a href="#">Home</a></li>'
            f'<li><a href="#">Data sources</a></li><li><a href="#">Architecture</a></li><li><a href="#">Models</a></li>'
            f'<li><a href="#">About</a></li></ul></nav></div>'
            f'<div class="links"><a href="#">GitHub</a><a href="#">LinkedIn</a><a href="#">CV (PDF)</a>'
            f'<a href="#">Email</a></div></div></footer>')
    body = "\n".join([nav, "<main>", head, f'<div class="grid ov">{rail}{main}</div>', ref, "</main>", foot])
    title = f"{c['key']} reference"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{FONTS}
<style>
{CSS}</style>
</helmet>
<div class="root" style="width: {W}px; height: {height}px; overflow: hidden; position: relative">
{body}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{W},"height":{height}}}}}'>
class Component extends DCLogic {{
renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
"""


def wrap_sql(call: str) -> str:
    head, _, rest = call.partition("(")
    return hl(esc(f'{head}(\n    {rest}').replace("&quot;", '"'))


def static(dc: str) -> str:
    s = dc.replace('<script src="./support.js"></script>', "")
    s = re.sub(r"</?x-dc>", "", s)
    s = re.sub(r"</?helmet>", "", s)
    s = re.sub(r"<script type=\"text/x-dc\".*?</script>\n", "", s, flags=re.S)
    return s


ORDER = ["elexon/fuelhh", "elexon/system_prices", "entsog/physical_flows", "elexon/bmunits_reference"]

if __name__ == "__main__":
    heights = [5200] * 4
    for a in sys.argv[1:]:
        if a.startswith("H="):
            heights = [int(x) for x in a[2:].split(",")]
    (HERE / "static").mkdir(exist_ok=True)
    for sid, h in zip(ORDER, heights):
        out = page(sid, h)
        body_only = out.split('<script type="text/x-dc"')[0]
        assert "{{" not in body_only and "}}" not in body_only, "template-hole syntax in markup"
        assert "/>" not in re.sub(r"<(meta|link|br|wbr)[^>]*>", "", body_only), "self-closing tag"
        name = f"B-{COPY[sid]['slug']}"
        (HERE / f"{name}.dc.html").write_text(out, encoding="utf-8")
        (HERE / "static" / f"{name}.html").write_text(static(out), encoding="utf-8")
        print(name, h)
