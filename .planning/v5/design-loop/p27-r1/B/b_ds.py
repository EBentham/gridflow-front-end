"""B-data-sources: the data-sources landing. One drawing, a section through the system from the Atlantic to the
Continent, with the seven vendors keyed by altitude: weather in the sky, then wind, carbon, the GB grid and the
continental grid, then (below ground) the gas pipeline in the seabed and the storage caverns in the salt."""
from __future__ import annotations

import math

from b_base import (CHART, CLAY, DAY, HORIZON, INK, INK2, KHAKI, LAB_P, OLIVE, ONP3, PACK, PETROL, W, bg_layer, ccgt,
                    converter, emit, f, footer, frange, index_list, mark_svg, masthead, page, pylon, sc, smooth,
                    solar_rows, spans, strata, surf, tank, tips, turbine, wbr)

# ---------------------------------------------------------------- page geometry (page y)
HERO_TOP, HERO_H = 100, 250
P = HERO_TOP + HERO_H          # plate band top
TITLE_H = 58                   # the plate heading row

SP = 128                       # keyed-part spacing: the tallest index entry (about 104 px) plus a gap
LV = {}                        # keyed part levels, plate-local y
LV["om"] = 124
LV["dp"] = LV["om"] + SP
LV["ci"] = LV["dp"] + SP
LV["el"] = LV["ci"] + SP
LV["ee"] = LV["el"] + SP
S_L = LV["ee"] + 124           # the cut, plate-local
LV["eg"] = S_L + 56            # the pipeline, trenched into the North Sea bed
LV["gie"] = LV["eg"] + SP + 20  # the storage caverns in the salt
PLATE_H = LV["gie"] + 136
S = P + S_L                    # the cut, page y
C_BRONZE = P + PLATE_H + 24    # topsoil / bronze contact
CAT_H = 930
C_DEEP = C_BRONZE + CAT_H
FOOT_H = 250
H = C_DEEP + FOOT_H

prof_page = surf(S)


def prof(x: float) -> float:
    return prof_page(x) - P


def interp(pts: list[tuple[float, float]], x: float) -> float:
    """Smoothstep interpolation through control points (a gentle, round-shouldered profile)."""
    if x <= pts[0][0]:
        return pts[0][1]
    for (a, ya), (b, yb) in zip(pts, pts[1:]):
        if a <= x <= b:
            t = (x - a) / (b - a)
            t = t * t * (3 - 2 * t)
            return ya + (yb - ya) * t
    return pts[-1][1]


# ---------------------------------------------------------------- land shapes (plate-local)
SEAS = [(178, 222), (646, 796)]                   # Irish Sea, North Sea: x ranges of open water
SEA_Y = S_L - 3                                   # the water line
NS_DEPTH = LV["eg"] - 8 - S_L                     # the North Sea is drawn deep enough to key the pipeline

FAR = [(-10, LV["dp"] + 84), (90, LV["dp"] + 58), (190, LV["dp"] + 76), (290, LV["dp"] + 52), (376, LV["dp"] + 48),
       (432, LV["dp"] + 44), (488, LV["dp"] + 50), (544, LV["dp"] + 58), (630, LV["dp"] + 104), (720, LV["dp"] + 168),
       (820, LV["dp"] + 246), (900, LV["dp"] + 318), (970, S_L - 40), (1030, S_L)]
MID = [(-10, LV["ci"] + 70), (80, LV["ci"] + 104), (170, LV["ci"] + 74), (250, LV["ci"] + 106), (330, LV["ci"] + 90),
       (420, LV["ci"] + 96), (500, LV["ci"] + 132), (600, LV["ci"] + 176), (700, LV["ci"] + 214), (800, LV["ci"] + 252),
       (900, LV["ci"] + 300), (970, S_L - 30), (1010, S_L)]
NEAR_GB = [(222, S_L - 6), (262, S_L - 54), (330, LV["el"] + 132), (402, LV["el"] + 90), (470, LV["el"] + 92),
           (526, LV["el"] + 110), (580, S_L - 60), (626, S_L - 26), (646, S_L - 6)]
NEAR_IE = [(-10, S_L - 64), (56, S_L - 84), (124, S_L - 56), (160, S_L - 30), (178, S_L - 6)]
NEAR_EU = [(796, S_L - 6), (812, LV["ee"] + 92), (970, LV["ee"] + 92), (1030, S_L - 13), (W + 20, S_L - 13)]


def seabed(x: float) -> float:
    for a, b in SEAS:
        if a <= x <= b:
            t = (x - a) / (b - a)
            depth = 20 if a == 178 else NS_DEPTH
            return S_L + 4 + depth * math.sin(math.pi * t) ** .28 + 1.5 * math.sin(x / 13)
    return prof(x)


def field_top(x: float) -> float:
    for pts in (NEAR_IE, NEAR_GB, NEAR_EU):
        if pts[0][0] <= x <= pts[-1][0]:
            return interp(pts, x) + 2.5 * math.sin(x / 29)
    return S_L


def poly(pts: list[tuple[float, float]], a: float, b: float, fill: str, op: str = "1", step: float = 5) -> str:
    xs = frange(a, b, step)
    top = " ".join(f"L{f(x)} {f(interp(pts, x) + 4 * math.sin(x / 41 + len(pts)) + 1.5 * math.sin(x / 13))}" for x in xs)
    return f'<path d="M{f(a)} {f(S_L + 2)} {top} L{f(b)} {f(S_L + 2)} Z" fill="{fill}" opacity="{op}"></path>'


def land_path(pts: list[tuple[float, float]]) -> str:
    xs = frange(pts[0][0], pts[-1][0], 4)
    top = " ".join(f"L{f(x)} {f(field_top(x))}" for x in xs)
    bottom = " ".join(f"L{f(x)} {f(prof(x))}" for x in reversed(xs))
    return f"M{f(xs[0])} {f(prof(xs[0]))} {top} {bottom} Z"


# ---------------------------------------------------------------- the drawing
def plume(x: float, y: float) -> str:
    """A flat vapour plume: it rises from the stack at (x, y) and bends east along the carbon level."""
    c = LV["ci"]
    top = smooth([(x - 3, y), (x - 1, y - 12), (x + 12, c - 6), (x + 60, c - 9), (x + 130, c - 7), (x + 214, c - 3)])
    bot = smooth([(x + 214, c + 3), (x + 132, c + 6), (x + 64, c + 8), (x + 22, c + 9), (x + 6, y - 10), (x + 3, y)])
    return (f'<path d="{top} L{f(x + 214)} {f(c + 3)} {bot[bot.index("C"):]} Z" fill="{DAY}" opacity=".3"></path>'
            f'<path d="{smooth([(x + 2, y - 14), (x + 30, c + 2), (x + 110, c), (x + 196, c + 1)])}" stroke="{DAY}" '
            f'stroke-width=".9" fill="none" opacity=".55"></path>')


def streamlines() -> str:
    out = []
    for k, (dy, amp, ph, op, x0, x1) in enumerate([(-26, 7, .3, .38, 70, 900), (0, 9, 1.5, .62, 30, 960),
                                                    (24, 7, 2.7, .38, 120, 930)]):
        pts = [(x, LV["om"] + dy + amp * math.sin(x / 160 + ph) + 3 * math.sin(x / 53 + ph * 2))
               for x in range(x0, x1 + 1, 30)]
        out.append(f'<path d="{smooth(pts)}" stroke="{ONP3}" stroke-width="{1.6 if k == 1 else 1.1}" fill="none" '
                   f'opacity="{op}" stroke-linecap="round"></path>')
    return "".join(out)


def cavern(cx: float, cy: float, w: float, h: float) -> str:
    """A leached salt cavern: a tall bulb, narrow at the neck."""
    t, b = cy - h / 2, cy + h / 2
    d = (f"M{f(cx - w * .16)} {f(t)} C{f(cx - w * .16)} {f(t + h * .2)} {f(cx - w * .62)} {f(t + h * .3)} "
         f"{f(cx - w * .5)} {f(cy + h * .2)} C{f(cx - w * .42)} {f(b)} {f(cx + w * .42)} {f(b)} {f(cx + w * .5)} "
         f"{f(cy + h * .2)} C{f(cx + w * .62)} {f(t + h * .3)} {f(cx + w * .16)} {f(t + h * .2)} {f(cx + w * .16)} {f(t)} Z")
    return f'<path d="{d}" fill="{CLAY}" fill-opacity=".55" stroke="{INK}" stroke-width="1.2" stroke-linejoin="round"></path>'


def drawing() -> str:
    g: list[str] = []
    g.append('<defs><pattern id="ds-salt" width="14" height="12" patternUnits="userSpaceOnUse">'
             f'<path d="M2 3 l3 3 M5 3 l-3 3 M9 8 l3 3 M12 8 l-3 3" stroke="{KHAKI}" stroke-width=".8"></path></pattern>'
             '</defs>')
    g.append(streamlines())

    # far ridge, across the whole section; GB's far hills carry the wind the NESO Data Portal reports
    g.append(poly(FAR, -10, 1030, HORIZON, ".5"))
    for x, h, sp, a in [(376, 50, "sp1", 20), (430, 52, "sp2", 70), (486, 50, "sp3", 5), (540, 46, "sp1", 44)]:
        base = interp(FAR, x) + 2 * math.sin(x / 31) + 2
        g.append(turbine(x, base, h, h * .5, sp, a))
    for x, h, sp in [(86, 30, "sp2"), (128, 28, "sp3"), (170, 30, "sp1")]:
        g.append(turbine(x, interp(FAR, x) + 2 * math.sin(x / 31) + 2, h, h * .5, sp, x % 90))

    # mid ridge with the gas-fired station; its plume bends east at the carbon level
    cc_x, cc_s = 318, .8
    cc_base = interp(MID, cc_x + 30) + 3
    g.append(poly(MID, -10, 1010, HORIZON))
    g.append(plume(cc_x + 89.5 * cc_s, cc_base - 112 * cc_s))
    g.append(ccgt(cc_x, cc_base, cc_s))

    # the near land
    for pts in (NEAR_IE, NEAR_GB, NEAR_EU):
        g.append(f'<path d="{land_path(pts)}" fill="{CHART}"></path>')
    bounds = []
    for a, b in ((250, 620), (820, W)):
        bounds.append(smooth([(x, field_top(x) + (prof(x) - field_top(x)) * .42) for x in frange(a, b, 22)]))
    g.append(f'<path d="{" ".join(bounds)}" stroke="{OLIVE}" stroke-width="1" fill="none" opacity=".45"></path>')

    # GB: the transmission line (Elexon), the gas terminal and the interconnector's converter
    p1 = (406, LV["el"] + 92, 1.0)
    p2 = (500, field_top(500) + 3, .96)
    tb_x, tb_base = 534, field_top(560) + 3
    cv_x, cv_s = 590, .46
    cv_base = field_top(608) + 4
    g.append(tank(tb_x, tb_base, 28, 20) + tank(tb_x + 32, tb_base, 22, 16))
    g.append(f'<g stroke="{INK}" fill="none" stroke-linecap="round" stroke-width="1.35">{pylon(*p1)}{pylon(*p2)}</g>')
    g.append(sc(converter(cv_x, cv_base), cv_x, cv_base, cv_s))
    wires = [spans([(cc_x + 62 * cc_s, cc_base - 32 * cc_s)] * 3, tips(*p1, -1), 16),
             spans(tips(*p1, 1), tips(*p2, -1), 12),
             spans(tips(*p2, 1), [(cv_x + 6, cv_base - 62 * cv_s)] * 3, 8)]

    # the Continent: converter at the coast, a gas terminal, the continental grid receding east (ENTSO-E)
    ce_x, ce_s = 802, .46
    ce_base = field_top(820) + 3
    g.append(sc(converter(ce_x, ce_base), ce_x, ce_base, ce_s))
    et_x, et_base = 866, field_top(880) + 3
    g.append(tank(et_x, et_base, 24, 17) + tank(et_x + 27, et_base, 20, 14))
    q1 = (918, LV["ee"] + 92, 1.0)
    q2 = (962, field_top(962) - 16, .62)
    g.append(f'<g stroke="{INK}" fill="none" stroke-linecap="round" stroke-width="1.35">{pylon(*q1)}{pylon(*q2)}</g>')
    wires += [spans([(ce_x + 34 * ce_s + 20, ce_base - 62 * ce_s)] * 3, tips(*q1, -1), 10),
              spans(tips(*q1, 1), tips(*q2, -1), 5)]
    g.append(f'<path d="{" ".join(wires)}" stroke="{INK}" stroke-width=".8" fill="none" opacity=".85"></path>')

    # the seas, with offshore wind in the North Sea
    for a, b in SEAS:
        xs = frange(a, b, 3)
        d = f"M{f(a)} {f(SEA_Y)} L{f(b)} {f(SEA_Y)} " + " ".join(f"L{f(x)} {f(seabed(x))}" for x in reversed(xs)) + " Z"
        g.append(f'<path d="{d}" fill="{HORIZON}"></path><path d="{d}" fill="{DAY}" opacity=".13"></path>')
        g.append(f'<path d="M{f(a)} {f(seabed(a))} ' + " ".join(f"L{f(x)} {f(seabed(x))}" for x in xs) +
                 f'" stroke="{INK}" stroke-width="1.2" fill="none"></path>')
        rip = " ".join(f"M{f(x)} {f(SEA_Y + 8 + (i % 3) * 5)} h{10 + (i % 2) * 9}"
                       for i, x in enumerate(frange(a + 8, b - 22, 30)))
        g.append(f'<path d="{rip}" stroke="{DAY}" stroke-width="1" opacity=".35"></path>')
    for i, ox in enumerate([676, 710, 744, 776]):
        g.append(turbine(ox, SEA_Y, 42 - (i % 2) * 4, 20, ["sp3", "sp1", "sp2"][i % 3], 25 * i + 10))

    # below ground: the salt with its caverns (GIE), the pipeline (ENTSO-G) and the interconnector cable
    gy = LV["gie"]
    top = [(x, gy - 40 - 14 * math.exp(-((x - 548) / 70) ** 2) - 18 * math.exp(-((x - 876) / 80) ** 2)
            + 4 * math.sin(x / 57)) for x in range(-40, W + 41, 24)]
    bot = [(x, gy + 108 + 6 * math.sin(x / 90 + 1) + 3 * math.sin(x / 31)) for x in range(W + 40, -41, -24)]
    sd = smooth(top) + " L" + smooth(bot)[1:] + " Z"
    g.append(f'<path d="{sd}" fill="{DAY}"></path><path d="{sd}" fill="url(#ds-salt)"></path>'
             f'<path d="{sd}" stroke="{INK}" stroke-width="1.2" fill="none"></path>')
    for cx, w, h in [(530, 22, 70), (568, 18, 60), (840, 24, 76), (882, 20, 66), (922, 17, 56)]:
        g.append(cavern(cx, gy + 2, w, h))

    pipe = ([(tb_x + 14, tb_base - 2), (tb_x + 44, S_L + 8), (612, S_L + 24), (640, S_L + 40)] +
            [(x, seabed(x) + 8) for x in frange(664, 780, 12)] +
            [(802, S_L + 36), (834, S_L + 24), (858, S_L + 10), (et_x + 12, et_base - 2)])
    pd = smooth(pipe)
    g.append(f'<path d="{pd}" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"></path>'
             f'<path d="{pd}" stroke="{CLAY}" stroke-width="4.6" fill="none" stroke-linecap="round"></path>')
    cable = ([(cv_x + 30, cv_base - 2), (cv_x + 44, S_L + 8), (632, S_L + 16), (650, seabed(650) - 2)] +
             [(x, seabed(x) - 3) for x in frange(664, 780, 12)] + [(794, seabed(794) - 2), (806, S_L + 12),
                                                                  (ce_x + 24, ce_base - 2)])
    g.append(f'<path d="{smooth(cable)}" stroke="{PETROL}" stroke-width="2.6" fill="none"></path>')

    # labels, lower-case like an annotated plate
    L = []

    def lab(t: str, x: float, y: float, c: str, a: str = "middle") -> None:
        L.append(f'<text x="{f(x)}" y="{f(y)}" fill="{c}" text-anchor="{a}">{t}</text>')
    lab("weather", 520, LV["om"] - 38, LAB_P)
    lab("gas-fired power station", cc_x + 34, cc_base + 20, LAB_P)
    lab("Ireland", 100, S_L - 9, INK)
    lab("Great Britain", 436, S_L - 8, INK)
    lab("the Continent", 1000, S_L - 1, INK)
    lab("North Sea", 721, SEA_Y + 17, LAB_P)
    lab("interconnector", 721, seabed(721) - 8, LAB_P)
    lab("gas pipeline", 721, LV["eg"] + 24, INK)
    lab("salt, with gas storage caverns", 720, gy + 5, INK)
    g.append(f'<g font-family="Hanken Grotesk" font-style="italic" font-size="13.5">{"".join(L)}</g>')

    aria = ("A section through the energy system from Ireland, across the Irish Sea, Great Britain and the "
            "North Sea, to the Continent, with each vendor keyed by height. Wind and sunlight cross the sky; wind "
            "turbines stand on the far hills of Great Britain; a gas-fired power station on the middle hills sends its "
            "plume east; the GB transmission line crosses the near hills to a converter station on the coast. On the "
            "Continent a second converter station feeds the continental grid. Below ground, an interconnector cable and "
            "a gas pipeline cross the bed of the North Sea, and deeper, gas storage caverns sit in a layer of salt.")
    return (f'<svg class="draw ds-draw" width="{W}" height="{PLATE_H}" viewBox="0 0 {W} {PLATE_H}" role="img" '
            f'aria-label="{aria}"><g font-family="Hanken Grotesk">{"".join(g)}</g></svg>')


# ---------------------------------------------------------------- the marks (copied from the drawing parts)
def marks() -> dict[str, str]:
    m = {}
    m["om"] = mark_svg(f'<path d="M1 8 C8 4 14 12 22 7 S29 6 29 6" stroke="{ONP3}" stroke-width="1.6" fill="none"></path>'
                       f'<path d="M1 15 C9 11 15 18 23 14 S29 13 29 13" stroke="{ONP3}" stroke-width="1.1" fill="none" '
                       f'opacity=".65"></path>')
    m["dp"] = mark_svg(f'<path d="M0 20 C8 15 20 15 30 18 V20 Z" fill="{HORIZON}"></path>' +
                       turbine(15, 18, 12, 7.5, "", 18).replace('class="rot "', ''))
    m["ci"] = mark_svg(f'<path d="M6 16 C6 11 9 8 15 8 C20 8 25 8 30 9 V13 C25 13 20 13 16 13 C12 13 10 14 9 16 Z" '
                       f'fill="{DAY}" opacity=".45"></path>'
                       f'<rect x="4" y="12" width="4" height="8" fill="{DAY}" stroke="{INK}" stroke-width=".7"></rect>'
                       f'<path d="M4 13.5 h4" stroke="{CLAY}" stroke-width="1.6"></path>')
    m["el"] = mark_svg(f'<g stroke="{DAY}" fill="none" stroke-width="1.3" stroke-linecap="round">'
                       f'<path d="M9 20 L13 2 M21 20 L17 2 M13 2 H17 M2 8 H28 M5 13.5 H25 M10.5 17 H19.5"></path></g>')
    m["ee"] = mark_svg(f'<g stroke="{DAY}" fill="none" stroke-width="1.2" stroke-linecap="round">'
                       f'<path d="M5 20 L8.5 3 M15 20 L11.5 3 M8.5 3 H11.5 M1 8 H19 M3 13 H17"></path>'
                       f'<path d="M23 20 L25 10 M29 20 L27 10 M21 13 H31 M22 16 H30" stroke-width="1"></path>'
                       f'<path d="M19 8 Q21 11 22 13 M17 13 Q19.5 15 21.5 16" stroke-width=".7"></path></g>')
    m["eg"] = mark_svg(f'<rect x="0" y="0" width="30" height="9" fill="{HORIZON}"></rect>'
                       f'<path d="M0 9 C9 10 20 10 30 9" stroke="{INK}" stroke-width="1.2" fill="none"></path>'
                       f'<path d="M3 14 H27" stroke="{INK}" stroke-width="7.6" stroke-linecap="round"></path>'
                       f'<path d="M3 14 H27" stroke="{CLAY}" stroke-width="5" stroke-linecap="round"></path>')
    m["gie"] = mark_svg(f'<rect x="0" y="1" width="30" height="18" fill="{DAY}"></rect>'
                        f'<path d="M3 5 l3 3 M6 5 l-3 3 M22 12 l3 3 M25 12 l-3 3" stroke="{KHAKI}" stroke-width=".8"></path>'
                        f'<path d="M13 2 C13 5 9 6 10 12 C11 18 19 18 20 12 C21 6 17 5 17 2 Z" fill="{CLAY}" '
                        f'fill-opacity=".55" stroke="{INK}" stroke-width="1.1"></path>'
                        f'<path d="M0 1 H30 M0 19 H30" stroke="{INK}" stroke-width=".9"></path>')
    return m


def entries() -> list[dict]:
    m = marks()
    return [
        dict(y=LV["om"], mark=m["om"], sky=True, name="Open-Meteo", href="#",
             d="Hourly weather, archive and forecast, for 7 cities, 12 wind sites and 6 solar sites.",
             f="[n] datasets. No key."),
        dict(y=LV["dp"], mark=m["dp"], sky=True, name="NESO Data Portal", href="#",
             d="Three packages from NESO’s file catalogue, among them the GB mix since 2009.",
             f="[n] datasets. No key."),
        dict(y=LV["ci"], mark=m["ci"], sky=True, name="NESO Carbon Intensity", href="#",
             d="Carbon intensity of GB electricity: national and regional, actual and forecast.",
             f="[n] datasets, half-hourly. No key."),
        dict(y=LV["el"], mark=m["el"], sky=True, name="Elexon BMRS", href="#",
             d="The GB balancing mechanism: prices, outturn, BM units and forecasts.",
             f="[n] datasets, half-hourly. No key."),
        dict(y=LV["ee"], mark=m["ee"], sky=True, name="ENTSO-E", href="#",
             d="European electricity for six zones. Its day-ahead prices hold no GB rows.",
             f="[n] datasets, 15-minute and hourly. API key."),
        dict(y=LV["eg"], mark=m["eg"], name="ENTSO-G", href="#",
             d="European gas transmission, by default at the UK’s interconnection points.",
             f="[n] datasets per gas day. No key."),
        dict(y=LV["gie"], mark=m["gie"], name="GIE AGSI+ and ALSI", href="#",
             d="Gas storage (AGSI+, nine countries) and LNG terminals (ALSI, eight countries).",
             f="[n] datasets per gas day. One API key."),
    ]


# ---------------------------------------------------------------- the catalogue section (bronze)
ADDR = [
    ("At the vendor", "data.elexon.co.uk/bmrs/api/v1/balancing/settlement/system-prices/{date}"),
    ("In bronze, as fetched", "bronze/elexon/system_prices/{YYYY}/{MM}/{DD}/"),
    ("In silver, typed", "silver/elexon/system_prices/year={YYYY}/month={MM}/"),
    ("In DuckDB", "silver_elexon_system_prices_latest"),
    ("In a notebook", "data.elexon.system_prices(start, end)"),
]


def price_chart() -> str:
    s = PACK["series"]["data_sources_landing"]
    pts = s["points"]
    w, h = 1280, 250
    x0, x1, y0, y1 = 64, w - 8, 14, h - 34
    lo, hi = 0, 225
    X = lambda i: x0 + i * (x1 - x0) / (len(pts) - 1)  # noqa: E731
    Y = lambda v: y1 - (v - lo) / (hi - lo) * (y1 - y0)  # noqa: E731
    line = "M" + " L".join(f"{f(X(i))} {f(Y(v))}" for i, (_, v) in enumerate(pts))
    ticks = ""
    for v in (0, 50, 100, 150, 200):
        ticks += (f'<path d="M{x0 - 5} {f(Y(v))} H{x0}" stroke="{INK}" stroke-width="1"></path>'
                  f'<text x="{x0 - 9}" y="{f(Y(v) + 4.5)}" text-anchor="end">{v}</text>')
    months = [("2026-06-01", "June"), ("2026-07-01", "July"), ("2026-08-01", "August"), ("2026-09-01", "September")]
    idx = {d: i for i, (d, _) in enumerate(pts)}
    for d, name in months:
        i = idx[d]
        ticks += (f'<path d="M{f(X(i))} {y1} v5" stroke="{INK}" stroke-width="1"></path>'
                  f'<text x="{f(X(i))}" y="{y1 + 21}" text-anchor="middle">{name}</text>')
    aria = ("Line chart of the GB system price, daily mean, 26 May to 22 September 2026, in pounds per megawatt-hour. "
            "The daily mean moves between about 21 and 211, mostly between 60 and 150.")
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{aria}">'
            f'<g font-family="Hanken Grotesk" font-size="13.5" fill="{INK2}">{ticks}</g>'
            f'<path d="M{x0} {y0 - 6} V{y1} H{x1}" stroke="{INK}" stroke-width="1.5" fill="none"></path>'
            f'<text x="{x0 + 8}" y="{y0 + 2}" font-family="Hanken Grotesk" font-style="italic" font-size="13.5" '
            f'fill="{INK}">£/MWh</text>'
            f'<path d="{line}" stroke="{PETROL}" stroke-width="1.8" fill="none" stroke-linejoin="round"></path></svg>')


def catalogue() -> str:
    rows = "".join(f'<tr><th scope="row">{k}</th><td><code>{wbr(v)}</code></td></tr>' for k, v in ADDR)
    keys = ", ".join(f"<code>{k}</code>" for k in
                     ["elexon", "entsoe", "entsog", "gie_agsi", "gie_alsi", "neso", "neso_data_portal"]) + \
        " and <code>open_meteo</code>"
    return (f'<section class="band cat" aria-labelledby="cat-h" style="height: {CAT_H}px; padding-top: 70px">'
            f'<div class="cat-top"><div class="sec"><h2 id="cat-h">How the catalogue is organised</h2>'
            f'<p>Each vendor has a hub that lists its datasets, and each dataset has one page: what it holds, its '
            f'schema, a sample, how to fetch it and the caveats that bite.</p>'
            f'<p>A dataset is named by its source key and its dataset key, and that pair addresses it everywhere in '
            f'gridflow. The source keys are {keys}.</p></div>'
            f'<div class="addr"><h3 class="fig-h" id="addr-h">Where <code>elexon/system_prices</code> lives</h3>'
            f'<table class="adt" aria-labelledby="addr-h"><tbody>{rows}</tbody></table></div></div>'
            f'<figure class="pc" aria-labelledby="pc-h"><h3 class="fig-h" id="pc-h">GB system price, daily mean, '
            f'26 May to 22 September 2026</h3>{price_chart()}'
            f'<figcaption class="cap">The mean of the 48 half-hourly system prices on each settlement date, taking the '
            f'latest vintage of each period. The sell and buy prices are equal on every period. Source: '
            f'<code>elexon/system_prices</code>, silver, £/MWh.</figcaption></figure></section>')


DS_CSS = """.ds-draw text{font-size:13.5px}
.cat-top{display:grid;grid-template-columns:520px minmax(0,1fr);column-gap:96px;align-items:start}
.cat .sec p code{font-size:.86em}
.addr .fig-h code{font-size:.8em;font-weight:500;color:#1C2B22}
.adt{width:100%;border-collapse:collapse;margin-top:14px}
.adt th{text-align:left;font-weight:600;font-size:14.5px;color:#1C2B22;width:190px;padding:0 16px 0 0;vertical-align:middle}
.adt td{font:400 15px/1.45 "Red Hat Mono",monospace;color:#1C2B22;padding:11px 0}
.adt td code{font-size:15px}
.adt tr{border-bottom:1px solid rgba(28,43,34,.22)}
.adt tr:first-child{border-top:1px solid #1C2B22}
.pc{margin:72px 0 0}
.pc svg{display:block;margin-top:14px}
"""


def build() -> str:
    hero = (f'<section class="band hero" aria-labelledby="h1" style="height: {HERO_H}px">'
            f'<h1 id="h1">Where the data comes from</h1>'
            f'<div class="lede"><p>gridflow ingests [N datasets] from seven vendors, across GB and European power, gas, '
            f'weather and carbon.</p><p>The drawing cuts across the system from Ireland to the Continent. Each vendor '
            f'is set level with the part of the system it reports on.</p></div></section>')
    plate = (f'<section class="band" aria-labelledby="pl-h" style="height: {PLATE_H + 24}px">'
             f'{drawing()}'
             f'<div class="plate" style="position: relative"><h2 class="plate-h sky" id="pl-h" '
             f'style="grid-column: 1 / -1; height: {TITLE_H}px">From the weather to the gas stores</h2>'
             f'{index_list([dict(e, y=e["y"] - TITLE_H) for e in entries()], "The seven vendors, keyed to the drawing")}'
             f'</div></section>')
    flow = "\n".join([masthead("Data sources"), "<main>", hero, plate, catalogue(), "</main>",
                      footer(FOOT_H, 92)])
    bg = bg_layer(H, strata(H, S, [(C_BRONZE, "bronze"), (C_DEEP, "deep")], land=True, names=False))
    return page("Data sources", H, bg, flow, DS_CSS)


if __name__ == "__main__":
    emit("B-data-sources", build())
    print("H", H, "S", S, "levels", LV, "bronze", C_BRONZE, "deep", C_DEEP)
