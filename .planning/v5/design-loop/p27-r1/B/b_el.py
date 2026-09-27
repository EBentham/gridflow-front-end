"""B-vendor-elexon: the vendor-hub pattern, rendered for Elexon. One drawing of the GB balancing and settlement
world, a panorama whose depth planes put each group of datasets at its own height (pumped storage on the far
mountain, the wind farm, the transmission line, the town, the notice board at a station gate), then every
dataset as a table list grouped the same way. Groups are the fact pack's PROPOSED thematic grouping."""
from __future__ import annotations

import math

from b_base import (CHART, CLAY, DAY, HORIZON, INK, INK2, KHAKI, LAB_P, MUTED, OLIVE, PACK, PETROL, RULE, W,
                    bg_layer, emit, f, footer, frange, index_list, mark_svg, masthead, page, pylon, smooth, spans,
                    strata, substation, surf, sc, tips, turbine)

# ---------------------------------------------------------------- page geometry
HERO_TOP, HERO_H = 100, 330
P = HERO_TOP + HERO_H
TITLE_H = 58
SP = 128
LV = {"pb": 124}
LV["ga"] = LV["pb"] + SP
LV["si"] = LV["ga"] + SP
LV["de"] = LV["si"] + SP
LV["rm"] = LV["de"] + SP
S_L = LV["rm"] + 124
PLATE_H = S_L + 40
S = P + S_L
CHART_TOP = P + PLATE_H
CHART_H = 470
C_BRONZE = CHART_TOP + CHART_H
DS = PACK["data_sources"]["elexon_hub"]["datasets"]
GROUPS = ["Prices and balancing", "Generation and availability", "System indicators", "Demand",
          "Reference and messages"]
N_ROWS = len(DS)
TABLE_H = 160 + 50 + N_ROWS * 45 + len(GROUPS) * 63 + 96
C_DEEP = C_BRONZE + TABLE_H
FOOT_H = 250
H = C_DEEP + FOOT_H

prof_page = surf(S)


def prof(x: float) -> float:
    return prof_page(x) - P


def interp(pts: list[tuple[float, float]], x: float) -> float:
    if x <= pts[0][0]:
        return pts[0][1]
    for (a, ya), (b, yb) in zip(pts, pts[1:]):
        if a <= x <= b:
            t = (x - a) / (b - a)
            t = t * t * (3 - 2 * t)
            return ya + (yb - ya) * t
    return pts[-1][1]


def lin(pts: list[tuple[float, float]], x: float) -> float:
    for (a, ya), (b, yb) in zip(pts, pts[1:]):
        if a <= x <= b:
            t = (x - a) / (b - a)
            return ya + (yb - ya) * (t + .12 * math.sin(math.pi * t))
    return pts[-1][1]


def band(pts: list[tuple[float, float]], a: float, b: float, fill: str, op: str = "1", wob: float = 3,
         jag: bool = False) -> str:
    xs = frange(a, b, 4)
    fn = lin if jag else interp
    top = " ".join(f"L{f(x)} {f(fn(pts, x) + wob * math.sin(x / 37 + len(pts)) + wob * .4 * math.sin(x / 11))}"
                   for x in xs)
    return f'<path d="M{f(a)} {f(S_L + 2)} {top} L{f(b)} {f(S_L + 2)} Z" fill="{fill}" opacity="{op}"></path>'


# depth planes (plate-local), far to near
MTN = [(-10, LV["pb"] + 8), (40, LV["pb"] - 30), (92, LV["pb"] - 12), (150, LV["pb"] - 58), (196, LV["pb"] - 4),
       (214, LV["pb"] + 2), (236, LV["pb"] + 2), (254, LV["pb"] - 6), (300, LV["pb"] - 50), (356, LV["pb"] - 22),
       (412, LV["pb"] - 44), (480, LV["pb"] + 4), (560, LV["pb"] + 30), (640, LV["pb"] + 84), (740, LV["pb"] + 150),
       (850, LV["pb"] + 232), (930, LV["pb"] + 330), (990, S_L - 30), (1016, S_L - 14)]
MIDH = [(-10, LV["ga"] + 110), (120, LV["ga"] + 86), (240, LV["ga"] + 74), (330, LV["ga"] + 66), (470, LV["ga"] + 64),
        (620, LV["ga"] + 70), (720, LV["ga"] + 112), (820, LV["ga"] + 200), (910, LV["ga"] + 300), (975, S_L - 30),
        (1004, S_L - 14)]
NEAR = [(-10, LV["si"] + 100), (90, LV["si"] + 92), (240, LV["si"] + 90), (380, LV["si"] + 94), (470, LV["si"] + 130),
        (560, LV["de"] + 64), (700, LV["de"] + 58), (840, LV["de"] + 64), (926, LV["de"] + 84), (958, LV["de"] + 150),
        (984, S_L - 20), (996, S_L - 12)]
FORE = [(300, S_L), (360, LV["rm"] + 44), (460, LV["rm"] + 36), (640, LV["rm"] + 38), (760, LV["rm"] + 52),
        (840, S_L - 26), (900, S_L)]


def fore_top(x: float) -> float:
    return interp(FORE, x) + 2 * math.sin(x / 29)


def near_top(x: float) -> float:
    return interp(NEAR, x) + 3 * math.sin(x / 37 + len(NEAR)) + 1.2 * math.sin(x / 11)


# ---------------------------------------------------------------- drawing pieces
def reservoir() -> str:
    """Pumped storage: a dam across the saddle between two shoulders, its reservoir level just under the crest,
    and a penstock down the mountain face to the power house."""
    y = LV["pb"]
    water = (f'<path d="M190 {f(y - 5)} L262 {f(y - 5)} L258 {f(y - 1)} L194 {f(y - 1)} Z" fill="{HORIZON}"></path>'
             f'<path d="M198 {f(y - 3)} h14 M222 {f(y - 3)} h20" stroke="{DAY}" stroke-width=".8" opacity=".5"></path>')
    dam = (f'<path d="M206 {f(y - 1)} L250 {f(y - 1)} L258 {f(y + 20)} L198 {f(y + 20)} Z" fill="{DAY}" '
           f'stroke="{INK}" stroke-width="1"></path>'
           f'<path d="M204 {f(y + 6)} H252 M202 {f(y + 13)} H255" stroke="{INK}" stroke-width=".6" opacity=".45"></path>'
           f'<path d="M204 {f(y - 1)} H252" stroke="{INK}" stroke-width="1.6"></path>')
    ph_x, ph_y = 300, LV["ga"] + 46
    pen = (f'<path d="M232 {f(y + 20)} C244 {f(y + 70)} 272 {f(ph_y - 80)} {ph_x} {f(ph_y - 14)} '
           f'M236 {f(y + 20)} C248 {f(y + 70)} 276 {f(ph_y - 80)} {ph_x + 4} {f(ph_y - 14)}" stroke="{DAY}" '
           f'stroke-width="1.1" fill="none" opacity=".85"></path>')
    house = (f'<rect x="{ph_x - 10}" y="{f(ph_y - 14)}" width="28" height="14" fill="{DAY}" stroke="{INK}" '
             f'stroke-width=".9"></rect><path d="M{ph_x - 12} {f(ph_y - 14)} H{ph_x + 20}" stroke="{INK}" '
             f'stroke-width="1.6"></path>')
    return water + pen + dam + house


def nuclear(x: float, base: float, s: float) -> str:
    def r(rx: float, ry: float, w: float, h: float, fill: str) -> str:
        return (f'<rect x="{f(x + rx * s)}" y="{f(base - ry * s)}" width="{f(w * s)}" height="{f(h * s)}" '
                f'fill="{fill}" stroke="{INK}" stroke-width=".9"></rect>')
    dome = (f'<path d="M{f(x)} {f(base)} V{f(base - 34 * s)} A{f(20 * s)} {f(20 * s)} 0 0 1 {f(x + 40 * s)} '
            f'{f(base - 34 * s)} V{f(base)} Z" fill="{DAY}" stroke="{INK}" stroke-width="1"></path>')
    return (r(36, 30, 70, 30, PETROL) + r(106, 22, 26, 22, DAY) + dome +
            f'<path d="M{f(x + 44 * s)} {f(base - 20 * s)} H{f(x + 102 * s)}" stroke="{DAY}" stroke-width=".8" '
            f'stroke-dasharray="3 3" opacity=".6"></path>' + r(118, 40, 5, 18, DAY))


def town(x0: float, base) -> tuple[str, float]:
    """Terraces, a block of flats and a shed, standing on a ground function; returns the drawing and the
    height of the highest roof."""
    out = []
    xs = x0
    highest = 1e9
    spec = [("terr", 64), ("flats", 30), ("terr", 52), ("shed", 58), ("terr", 46), ("flats", 26), ("terr", 40)]
    for kind, w in spec:
        gy = base(xs + w / 2) + 2
        if kind == "terr":
            h = 18
            ridge = gy - h - 12
            out.append(f'<path d="M{f(xs)} {f(gy)} V{f(gy - h)} L{f(xs + w / 2)} {f(ridge)} L{f(xs + w)} {f(gy - h)} '
                       f'V{f(gy)} Z" fill="{DAY}" stroke="{INK}" stroke-width=".9" stroke-linejoin="round"></path>')
            out.append(f'<path d="M{f(xs)} {f(gy - h)} L{f(xs + w / 2)} {f(ridge)} L{f(xs + w)} {f(gy - h)}" '
                       f'fill="{CLAY}" opacity=".75"></path>')
            doors = " ".join(f"M{f(xd)} {f(gy)} v-7" for xd in frange(xs + 6, xs + w - 4, 11))
            out.append(f'<path d="{doors}" stroke="{INK}" stroke-width="2" opacity=".55"></path>')
            highest = min(highest, ridge)
        elif kind == "flats":
            h = 58 if w == 30 else 44
            out.append(f'<rect x="{f(xs)}" y="{f(gy - h)}" width="{w}" height="{h}" fill="{KHAKI}" stroke="{INK}" '
                       f'stroke-width=".9"></rect>')
            win = " ".join(f"M{f(xs + 5)} {f(yy)} H{f(xs + w - 5)}" for yy in frange(gy - h + 7, gy - 6, 7))
            out.append(f'<path d="{win}" stroke="{INK}" stroke-width="1.6" stroke-dasharray="3 2.5" opacity=".5"></path>')
            highest = min(highest, gy - h)
        else:
            h = 22
            teeth = " ".join(f"L{f(xt + 7)} {f(gy - h - 7)} L{f(xt + 14)} {f(gy - h)}" for xt in frange(xs, xs + w - 14, 14))
            out.append(f'<path d="M{f(xs)} {f(gy)} V{f(gy - h)} {teeth} V{f(gy)} Z" fill="{RULE}" stroke="{INK}" '
                       f'stroke-width=".9" stroke-linejoin="round"></path>')
        xs += w + 4
    return "".join(out), highest


def noticeboard(x: float, ground: float, y: float) -> str:
    """A notice board at a station gate, centred on y: the unit's name plate and pinned notices."""
    return (f'<path d="M{f(x + 4)} {f(ground)} V{f(y)} M{f(x + 40)} {f(ground)} V{f(y)}" stroke="{INK}" '
            f'stroke-width="1.6"></path>'
            f'<rect x="{f(x)}" y="{f(y - 12)}" width="44" height="24" fill="{DAY}" stroke="{INK}" stroke-width="1.1"></rect>'
            f'<rect x="{f(x + 4)}" y="{f(y - 9)}" width="36" height="5" fill="{PETROL}"></rect>'
            f'<rect x="{f(x + 5)}" y="{f(y - 1)}" width="9" height="10" fill="{RULE}" stroke="{INK}" stroke-width=".5"></rect>'
            f'<rect x="{f(x + 17)}" y="{f(y - 1)}" width="9" height="10" fill="{CHART}" stroke="{INK}" stroke-width=".5"></rect>'
            f'<rect x="{f(x + 29)}" y="{f(y - 1)}" width="9" height="10" fill="{RULE}" stroke="{INK}" stroke-width=".5"></rect>')


def drawing() -> str:
    g: list[str] = []
    # far mountains with the pumped-storage reservoir (prices and balancing)
    g.append(band(MTN, -10, 1016, HORIZON, ".5", wob=1.2, jag=True))
    g.append(reservoir())
    # middle hills with the wind farm (generation and availability)
    g.append(band(MIDH, -10, 1004, HORIZON))
    for i, x in enumerate([372, 432, 492, 552, 612, 672]):
        base = interp(MIDH, x) + 3 * math.sin(x / 37 + len(MIDH)) + 1.2 * math.sin(x / 11) + 3
        h = (base - LV["ga"]) / (1 + .1 / 80)
        g.append(turbine(x, base, h, 31, ["sp1", "sp2", "sp3"][i % 3], 22 * i + 5))
    # near hills (chartreuse): the transmission line and the town, down to the coast
    xs = frange(-10, 996, 4)
    top = " ".join(f"L{f(x)} {f(near_top(x))}" for x in xs)
    bot = " ".join(f"L{f(x)} {f(prof(x))}" for x in reversed(xs))
    g.append(f'<path d="M-10 {f(prof(-10))} {top} {bot} Z" fill="{CHART}"></path>')
    sea_y = S_L - 14
    sea = f"M986 {f(sea_y)} H{W + 20} V{f(S_L + 12)} H986 Z"
    g.append(f'<path d="{sea}" fill="{HORIZON}"></path><path d="{sea}" fill="{DAY}" opacity=".13"></path>')
    rip = " ".join(f"M{f(x)} {f(sea_y + 5 + (i % 2) * 4)} h{12 + (i % 3) * 8}" for i, x in enumerate(frange(1004, W, 38)))
    g.append(f'<path d="{rip}" stroke="{DAY}" stroke-width="1" opacity=".35"></path>')
    g.append(f'<path d="M{f(xs[-1])} {f(near_top(xs[-1]))} L{f(xs[-1] + 2)} {f(S_L + 12)}" stroke="none"></path>')
    tl, highest = town(560, near_top)
    g.append(tl)
    bounds = [smooth([(x, near_top(x) + (prof(x) - near_top(x)) * k) for x in frange(-10, 1000, 26)])
              for k in (.38, .7)]
    g.append(f'<path d="{" ".join(bounds)}" stroke="{OLIVE}" stroke-width="1" fill="none" opacity=".42"></path>')
    gsp_x = 520
    gsp_base = LV["rm"] + 52
    g.append(sc(substation(gsp_x, gsp_base), gsp_x, gsp_base, 1.0))
    g.append(noticeboard(438, LV["rm"] + 50, LV["rm"]))
    # pylons: across the near hills from the west, down to the grid supply point
    pyl = [(90, LV["si"] + 92, 1.0), (230, LV["si"] + 92, 1.0), (366, LV["si"] + 92, 1.0)]
    g.append(f'<g stroke="{INK}" fill="none" stroke-linecap="round" stroke-width="1.35">'
             + "".join(pylon(*p) for p in pyl) + '</g>')
    wires = [spans([(-12, LV["si"] + 14), (-12, LV["si"] - 12), (-12, LV["si"] - 32)], tips(*pyl[0], -1), 10)]
    wires += [spans(tips(*a, 1), tips(*b, -1), 14) for a, b in zip(pyl, pyl[1:])]
    wires.append(spans(tips(*pyl[2], 1), [(gsp_x - 3, gsp_base - 50), (gsp_x + 8, gsp_base - 44),
                                          (gsp_x + 18, gsp_base - 44)], 12))
    g.append(f'<path d="{" ".join(wires)}" stroke="{INK}" stroke-width=".8" fill="none" opacity=".85"></path>')

    L = []

    def lab(t: str, x: float, y: float, c: str, a: str = "middle") -> None:
        L.append(f'<text x="{f(x)}" y="{f(y)}" fill="{c}" text-anchor="{a}">{t}</text>')
    lab("pumped storage", 312, LV["pb"] + 40, LAB_P, "start")
    lab("wind farm", 700, LV["ga"] + 34, LAB_P, "start")
    lab("transmission line", 230, LV["si"] + 118, INK)
    lab("a town", 760, LV["de"] + 84, INK)
    lab("grid supply point", 562, gsp_base + 18, INK)
    lab("notice board", 460, LV["rm"] + 68, INK)
    g.append(f'<g font-family="Hanken Grotesk" font-style="italic" font-size="13.5">{"".join(L)}</g>')
    aria = ("A panorama of the GB electricity system, drawn in depth so each group of Elexon datasets sits at its own "
            "height. On the far mountains, a pumped-storage reservoir behind a dam, with its penstock down to the power "
            "house. On the middle hills, a wind farm. On the near hills, a transmission line on lattice pylons, running "
            "down to a grid supply point. Beyond it, a town of terraces, flats and sheds, down to "
            "the coast. In the foreground, a notice board at the gate of the grid supply point.")
    return (f'<svg class="draw el-draw" width="{W}" height="{PLATE_H}" viewBox="0 0 {W} {PLATE_H}" role="img" '
            f'aria-label="{aria}"><g font-family="Hanken Grotesk">{"".join(g)}</g></svg>')


# ---------------------------------------------------------------- the marks
def marks(on: str = "sky") -> dict[str, str]:
    """Marks copied from the drawing. The plate's copies sit on petrol; the table's copies on bronze."""
    line = DAY if on == "sky" else INK
    m = {}
    m["pb"] = mark_svg(f'<path d="M0 20 L6 8 L11 12 L16 4 L30 16 V20 Z" fill="{HORIZON}" opacity="{".7" if on == "sky" else "1"}"></path>'
                       f'<path d="M5 12 C10 10 16 10 20 11 L21 14 C16 15 10 15 6 14 Z" fill="{DAY}" opacity=".6"></path>'
                       f'<path d="M19 10 L23 10 L25 18 L18 18 Z" fill="{DAY}" stroke="{INK}" stroke-width=".8"></path>')
    tb = turbine(15, 19, 13, 8, "", 40).replace('class="rot "', '')
    m["ga"] = mark_svg((tb if on == "sky" else tb.replace(f'fill="{DAY}"', f'fill="{HORIZON}"')))
    m["si"] = mark_svg(f'<g stroke="{line}" fill="none" stroke-width="1.3" stroke-linecap="round">'
                       f'<path d="M9 20 L13 2 M21 20 L17 2 M13 2 H17 M2 8 H28 M5 13.5 H25 M10.5 17 H19.5"></path></g>')
    m["de"] = mark_svg(f'<path d="M1 20 V12 L6 7 L11 12 V20 Z" fill="{DAY}" stroke="{INK}" stroke-width=".8"></path>'
                       f'<path d="M1 12 L6 7 L11 12" fill="{CLAY}"></path>'
                       f'<rect x="13" y="3" width="8" height="17" fill="{KHAKI}" stroke="{INK}" stroke-width=".8"></rect>'
                       f'<path d="M23 20 V13 L27 10 L29 13 V20 Z" fill="{DAY}" stroke="{INK}" stroke-width=".8"></path>')
    m["rm"] = mark_svg(f'<rect x="3" y="3" width="24" height="14" fill="{DAY}" stroke="{INK}" stroke-width="1"></rect>'
                       f'<rect x="5" y="5" width="20" height="3" fill="{PETROL}"></rect>'
                       f'<rect x="6" y="10" width="5" height="5" fill="{RULE}"></rect><rect x="13" y="10" width="5" height="5" '
                       f'fill="{CHART}"></rect><rect x="20" y="10" width="5" height="5" fill="{RULE}"></rect>'
                       f'<path d="M5 17 V20 M25 17 V20" stroke="{line}" stroke-width="1.4"></path>')
    return m


GROUP_KEY = dict(zip(GROUPS, ["pb", "ga", "si", "de", "rm"]))
GROUP_TEXT = {
    "pb": ("What balancing the system cost each half-hour: the system price, market index prices, bid and offer "
           "acceptances, physical notifications and balancing services adjustments.",
           "The sell and buy prices are equal on every period in the store."),
    "ga": ("Outturn by fuel type, half-hourly and every five minutes, wind and solar actuals, the wind forecast, and "
           "availability 2 to 14 days ahead.", "fuelhh carries no solar rows."),
    "si": ("The state of the whole system: frequency, indicated margin and imbalance, loss-of-load probability, "
           "indicated generation and temperature.", ""),
    "de": ("National and transmission demand, as outturn and as forecasts from a day to 14 days ahead.",
           "indo is the demand model’s target."),
    "rm": ("The register of every BM unit, and REMIT messages on outages and unavailability.", ""),
}
INDEX_D = {
    "pb": "What balancing cost each half-hour: prices, and the bids and offers accepted.",
    "ga": "Outturn by fuel type, wind and solar actuals, and availability days ahead.",
    "si": "Frequency, margin, imbalance and loss-of-load probability, system-wide.",
    "de": "National and transmission demand: outturn, and forecasts to 14 days out.",
    "rm": "The register of every BM unit, and REMIT messages on outages.",
}
INDEX_F = {"pb": "[n] datasets, among them <code>system_prices</code>", "ga": "[n] datasets, among them <code>fuelhh</code>",
           "si": "[n] datasets, among them <code>freq</code>", "de": "[n] datasets, among them <code>indo</code>",
           "rm": "[n] datasets: <code>bmunits_reference</code>, <code>remit</code>"}


def entries() -> list[dict]:
    m = marks()
    return [dict(y=LV[k], mark=m[k], sky=True, name=g, href=f"#g-{k}", d=INDEX_D[k], f=INDEX_F[k])
            for g, k in GROUP_KEY.items()]


# ---------------------------------------------------------------- the wind chart (topsoil)
def wind_chart() -> str:
    s = PACK["series"]["elexon_hub"]
    pts = s["points"]
    w, h = 1280, 260
    x0, x1, y0, y1 = 64, w - 8, 12, h - 34
    lo, hi = 0, 12000
    X = lambda i: x0 + (i + .5) * (x1 - x0) / len(pts)  # noqa: E731
    Y = lambda v: y1 - (v - lo) / (hi - lo) * (y1 - y0)  # noqa: E731
    bw = (x1 - x0) / len(pts) - 3
    bars = "".join(f'<rect x="{f(X(i) - bw / 2)}" y="{f(Y(v))}" width="{f(bw)}" height="{f(y1 - Y(v))}"></rect>'
                   for i, (_, v) in enumerate(pts))
    ticks = ""
    for v in (0, 4000, 8000, 12000):
        ticks += (f'<path d="M{x0 - 5} {f(Y(v))} H{x0}" stroke="{INK}" stroke-width="1"></path>'
                  f'<text x="{x0 - 9}" y="{f(Y(v) + 4.5)}" text-anchor="end">{v:,}</text>')
    for i, (m, _) in enumerate(pts):
        if m.endswith("-01"):
            xx = x0 + i * (x1 - x0) / len(pts)
            ticks += (f'<path d="M{f(xx)} {y1} v6" stroke="{INK}" stroke-width="1"></path>'
                      f'<text x="{f(xx + 4)}" y="{y1 + 21}">{m[:4]}</text>')
    aria = ("Bar chart of GB transmission-metered wind generation, monthly mean, September 2021 to August 2026, in "
            "megawatts: 60 bars between about 3,700 and 11,600 MW, higher every winter than in the summers either side.")
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{aria}">'
            f'<g fill="{HORIZON}">{bars}</g>'
            f'<g font-family="Hanken Grotesk" font-size="13.5" fill="{INK2}">{ticks}</g>'
            f'<path d="M{x0} {y0 - 4} V{y1} H{x1}" stroke="{INK}" stroke-width="1.5" fill="none"></path>'
            f'<text x="{x0 + 8}" y="{y0 + 4}" font-family="Hanken Grotesk" font-style="italic" font-size="13.5" '
            f'fill="{INK}">MW</text></svg>')


# ---------------------------------------------------------------- the table list (bronze)
ONE_LINE = {
    "system_prices": "System sell price and system buy price per settlement period",
    "market_depth": "Settlement market depth per settlement period",
    "pn": "Physical notifications, per BM unit and period",
    "boal": "Bid and offer acceptance levels (BOALF, which replaces BOAL)",
    "disbsad": "Disaggregated balancing services adjustment data",
    "mid": "Market index data; its APXMIDP provider is the GB day-ahead benchmark",
    "netbsad": "Net balancing services adjustment data",
    "soso": "SO-SO prices for cross-border interconnector trading",
    "freq": "System frequency",
    "fuelhh": "Half-hourly generation outturn by fuel type (no solar)",
    "fuelinst": "Instantaneous generation outturn by fuel type, every five minutes",
    "imbalngc": "Indicated imbalance",
    "ndf": "National demand forecast, day-ahead",
    "ndfd": "National demand forecast, 2 to 14 days ahead",
    "melngc": "Indicated margin",
    "fou2t14d": "Generation availability by fuel type, 2 to 14 days ahead",
    "uou2t14d": "Generation availability by BM unit, 2 to 14 days ahead",
    "windfor": "Wind generation forecast",
    "temp": "Temperature data",
    "agpt": "Actual aggregated generation per type (B1620)",
    "agws": "Actual or estimated wind and solar generation (B1630)",
    "atl": "Actual total load per bidding zone (B0610)",
    "indo": "Initial national demand outturn, the demand model’s target",
    "itsdo": "Initial transmission system demand outturn",
    "indod": "Initial national demand outturn, daily total",
    "nonbm": "Non-BM STOR generation",
    "inddem": "Day and day-ahead indicated demand",
    "indgen": "Day and day-ahead indicated generation",
    "tsdf": "Transmission system demand forecast",
    "tsdfd": "Transmission system demand forecast, 2 to 14 days ahead",
    "lolpdrm": "Loss of load probability and de-rated margin",
    "remit": "REMIT outage and unavailability messages",
    "bmunits_reference": "All BM unit reference data",
}
QUERY = {"publish_datetime": "publish time", "date_path": "settlement date",
         "settlement_date_period": "settlement date and period", "no_params": "no parameters"}
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
ORDER = {  # within a group: the order the index names them, then the rest by key
    "Prices and balancing": ["system_prices", "mid", "market_depth", "boal", "pn", "disbsad", "netbsad", "soso"],
    "Generation and availability": ["fuelhh", "fuelinst", "agpt", "agws", "windfor", "fou2t14d", "uou2t14d", "nonbm"],
    "System indicators": ["freq", "melngc", "imbalngc", "lolpdrm", "indgen", "temp"],
    "Demand": ["indo", "itsdo", "indod", "atl", "ndf", "ndfd", "tsdf", "tsdfd", "inddem"],
    "Reference and messages": ["bmunits_reference", "remit"],
}


def held_from(d: dict) -> str:
    if d["key"] == "bmunits_reference":
        return "one snapshot"
    if d["key"] == "nonbm":
        return "5 rows"
    y, m, dd = d["event_time_min"][:10].split("-")
    y, m = int(y), int(m)
    if int(dd) >= 30 and d["event_time_min"][11:13] >= "22":   # a UTC evening that is the next settlement date
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return f"{MONTHS[m - 1]} {y}"


def table() -> str:
    by = {d["key"]: d for d in DS}
    mk = marks("ground")
    rows = []
    for grp in GROUPS:
        k = GROUP_KEY[grp]
        rows.append(f'<tr class="gh" id="g-{k}"><td colspan="4"><div class="gh-in">{mk[k]}<h3>{grp}</h3>'
                    f'<span>[n] datasets</span></div></td></tr>')
        for key in ORDER[grp]:
            d = by[key]
            code = d["bmrs_code"] or d["api_path"]
            rows.append(f'<tr><td class="k"><a href="#">{key}</a></td><td class="c">{code}</td>'
                        f'<td class="m">{ONE_LINE[key]}</td><td class="n">{held_from(d)}</td></tr>')
    assert sum(len(v) for v in ORDER.values()) == len(DS) == len({k for v in ORDER.values() for k in v})
    return (f'<table class="tl el-tl" aria-labelledby="tl-h"><thead><tr><th scope="col">Dataset</th>'
            f'<th scope="col">BMRS code or path</th><th scope="col">What it holds</th>'
            f'<th scope="col" class="n">In the store from</th></tr></thead><tbody>{"".join(rows)}</tbody></table>')


EL_CSS = """.el-draw text{font-size:13.5px}
.hero-l .lead{margin:20px 0 0;font-size:21px;line-height:1.5;color:#F6F4EC;max-width:40ch}
.vfacts{margin:14px 0 0}
.vfacts div{display:grid;grid-template-columns:92px minmax(0,1fr);column-gap:16px;padding:8px 0;border-top:1px solid rgba(207,224,220,.22)}
.vfacts div:last-child{border-bottom:1px solid rgba(207,224,220,.22)}
.vfacts dt{font-size:14.5px;font-weight:600;color:#F6F4EC}
.vfacts dd{margin:0;font-size:14.5px;line-height:1.5;color:#CFE0DC}
.vfacts dd code{font-size:13px;color:#F6F4EC}
.wfig svg{display:block;margin-top:16px}
.el-tl{margin-top:8px}
.el-tl td a{text-decoration-color:rgba(102,121,59,.55)}
.el-tl td.k{width:190px}
.el-tl td.c{width:330px}
.el-tl td.n{width:150px}
.tl-head p code{font-size:13px;color:#1C2B22}
.tl-head{display:grid;grid-template-columns:minmax(0,1fr) 520px;column-gap:96px;align-items:end}
.tl-head p{margin:0;font-size:14.5px;line-height:1.55;color:#3F4A3B}
"""


def build() -> str:
    facts = [("Market", "GB electricity"), ("Access", "Public; no API key"),
             ("Base URL", "<code>data.elexon.co.uk/bmrs/api/v1</code>"),
             ("Grain", "Half-hourly settlement periods, 1 to 50 a day (46 or 50 when the clocks change); FUELINST "
                       "every five minutes"),
             ("Source key", "<code>elexon</code>")]
    dl = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in facts)
    hero = (f'<section class="band hero" aria-labelledby="h1" style="height: {HERO_H}px">'
            f'<div class="hero-l"><p class="crumb"><a href="#">Data sources</a> / Elexon BMRS</p>'
            f'<h1 id="h1">Elexon BMRS</h1>'
            f'<p class="lead">The GB balancing mechanism through the BMRS Insights API: [n] datasets on prices, '
            f'generation, demand and the state of the system.</p></div>'
            f'<dl class="vfacts">{dl}</dl></section>')
    plate = (f'<section class="band" aria-labelledby="pl-h" style="height: {PLATE_H}px">{drawing()}'
             f'<div class="plate" style="position: relative"><h2 class="plate-h sky" id="pl-h" '
             f'style="grid-column: 1 / -1; height: {TITLE_H}px">Five groups of datasets, and where each sits in the '
             f'system</h2>'
             f'{index_list([dict(e, y=e["y"] - TITLE_H) for e in entries()], "The five groups, keyed to the drawing")}'
             f'</div></section>')
    wind = (f'<section class="band" aria-labelledby="w-h" style="height: {CHART_H}px; padding-top: 72px">'
            f'<figure class="wfig" style="margin: 0"><h2 class="fig-h" id="w-h">GB wind generation, monthly mean, '
            f'September 2021 to August 2026</h2>{wind_chart()}'
            f'<figcaption class="cap">Every winter runs higher than the summers either side of it. The mean of '
            f'half-hourly transmission-metered wind output per calendar month. Source: <code>elexon/fuelhh</code>, '
            f'silver, fuel type <code>WIND</code>, MW.</figcaption></figure></section>')
    tbl = (f'<section class="band" aria-labelledby="tl-h" style="height: {TABLE_H}px; padding-top: 72px">'
           f'<div class="tl-head sec"><h2 id="tl-h" style="margin: 0">Every Elexon dataset in gridflow</h2>'
           f'<p>Grouped as in the drawing above. Each is queried by publish time, except <code>system_prices</code> '
           f'and <code>market_depth</code> (by settlement date), <code>pn</code> (by settlement date and period) and '
           f'<code>bmunits_reference</code> (no parameters).</p></div>{table()}</section>')
    flow = "\n".join([masthead("Data sources"), "<main>", hero, plate, wind, tbl, "</main>", footer(FOOT_H, 92)])
    bg = bg_layer(H, strata(H, S, [(C_BRONZE, "bronze"), (C_DEEP, "deep")], land=True, names=False))
    return page("Elexon BMRS", H, bg, flow, EL_CSS)


if __name__ == "__main__":
    emit("B-vendor-elexon", build())
    print("H", H, "S", S, "levels", LV, "bronze", C_BRONZE, "deep", C_DEEP)
