"""B-models: the residual-demand-to-price chain as one landscape. Far to near: the city (demand), the wind
ridge, the solar hill; in front, the merit order as a terraced hillside, cheapest terrace lowest. Residual
demand is the water let into the terraces from the bottom up; the price is the terrace where it stops.
Every model id, target and score sits in the keyed index and the tables below, from the pack."""
from __future__ import annotations

import math
import random

from b_base import (CHART, pylon, spans, tips, CLAY, DAY, GOLD, HORIZON, INK, INK2, KHAKI, OLIVE, PACK, PETROL, T_TOP, W, bg_layer, ccgt,
                    emit, f, footer, frange, index_list, mark_svg, masthead, page, smooth, solar_rows, strata, turbine)

# ---------------------------------------------------------------- geometry (plate-local unless noted)
HERO_TOP, HERO_H = 100, 250
P = HERO_TOP + HERO_H
TITLE_TOP, TITLE_H = 24, 58
L: dict[str, float] = {}
L["de"] = 150                    # city rooftops: day-ahead demand
L["wi"] = L["de"] + 192          # turbine hubs: wind (spacing = measured entry height + 26)
L["so"] = L["wi"] + 191          # panel rows: solar
L["st"] = L["so"] + 214          # the top terrace wall: the stack (the plateau edge runs between)
L["rd"] = L["st"] + 214          # the fill's span: residual demand
L["sm"] = L["rd"] + 112          # the water level on the marginal terrace: SMP
TOP_Y = L["st"] - 26             # the plateau, which runs on under the index
S = L["sm"] + 96                 # the lowest ground; the page's surface for the strata
PLATE_H = L["sm"] + 196
GOLD_H = 1990
DEEP_H = 820                     # deep band incl. the 250 px footer
H = P + PLATE_H + GOLD_H + DEEP_H

SM = L["sm"]
# terraces (x0, x1, tread y): the merit order, cheapest lowest. The wet ones run up to the marginal terrace,
# whose water sits at SM; the dry tail steepens to the plateau, which runs on under the index.
_XS = [-20, 110, 196, 272, 340, 404, 466, 528, 594, 650, 704, 756, 806]
_YS = [SM + 92, SM + 80, SM + 68, SM + 56, SM + 44, SM + 30, SM + 15, SM, SM - 28, SM - 66, SM - 122, SM - 206]
TER = [(a, b, y) for a, b, y in zip(_XS, _XS[1:], _YS)] + [(806, 1460, TOP_Y)]
WET = 8
TREAD = 18                       # the tread's visible depth
PYL0: list[tuple[float, float, float]] = []


def ridge(pts: list[tuple[float, float]], floor: float) -> str:
    return f"{smooth(pts)} L{f(pts[-1][0])} {f(floor)} L{f(pts[0][0])} {f(floor)} Z"


# ---------------------------------------------------------------- drawing
def city(x0: float, ground) -> str:
    """Terraces, flats and a few towers along the far ridge."""
    rng = random.Random(3)
    out, x = [], x0
    plan = [("t", 30), ("t", 26), ("f", 18, 44), ("t", 30), ("k", 14, 70), ("f", 22, 52), ("t", 28), ("t", 24),
            ("f", 16, 38), ("k", 12, 58), ("t", 30), ("f", 20, 46), ("t", 26), ("t", 22)]
    for item in plan:
        kind, w = item[0], item[1]
        g = ground(x + w / 2) + 2
        if kind == "t":
            h = 16
            out.append(f'<path d="M{f(x)} {f(g)} V{f(g - h)} L{f(x + w / 2)} {f(g - h - 10)} L{f(x + w)} {f(g - h)} '
                       f'V{f(g)} Z" fill="{DAY}" stroke="{INK}" stroke-width=".9" stroke-linejoin="round"></path>'
                       f'<path d="M{f(x)} {f(g - h)} L{f(x + w / 2)} {f(g - h - 10)} L{f(x + w)} {f(g - h)}" '
                       f'fill="{CLAY}" opacity=".8"></path>')
            out.append(f'<rect x="{f(x + w * .3)}" y="{f(g - 10)}" width="4" height="5" fill="{INK}" opacity=".55"></rect>')
        else:
            h = item[2]
            fill = "#A39A6A" if kind == "f" else "#D8D3BF"
            out.append(f'<rect x="{f(x)}" y="{f(g - h)}" width="{w}" height="{h}" fill="{fill}" stroke="{INK}" '
                       f'stroke-width=".9"></rect>')
            rows = " ".join(f"M{f(x + 3)} {f(yy)} H{f(x + w - 3)}" for yy in frange(g - h + 7, g - 4, 7))
            out.append(f'<path d="{rows}" stroke="{INK}" stroke-width="1.6" stroke-dasharray="2.5 2.5" '
                       f'opacity=".4"></path>')
        x += w + rng.choice([2, 3, 4])
    return "".join(out)


def terraces() -> tuple[str, str]:
    """The stepped hillside: returns (ground body, details on top)."""
    prof = []
    for i, (x0, x1, y) in enumerate(TER):
        prof += [(x0, y), (x1, y)]
    d = "M-20 " + f(TER[0][2]) + " " + " ".join(f"L{f(x)} {f(y)}" for x, y in prof) + f" L1460 {f(S + 40)} L-20 {f(S + 40)} Z"
    # the body in page coordinates so its soil pattern meets the strata's without a seam
    body = (f'<g transform="translate(0 {-P})"><path d="{d}" transform="translate(0 {P})" fill="{T_TOP}"></path></g>')
    shift = (f'<g transform="translate(0 {-P})"><path d="' +
             d.replace("M-20 ", "M-20 ").strip() + '" fill="none"></path></g>')
    _ = shift
    pat = []
    # paths shifted into page space for the pattern fill
    pd = "M-20 " + f(TER[0][2] + P) + " " + " ".join(f"L{f(x)} {f(y + P)}" for x, y in prof) + \
         f" L1460 {f(S + 40 + P)} L-20 {f(S + 40 + P)} Z"
    pat.append(f'<g transform="translate(0 {-P})"><path d="{pd}" fill="url(#p-soil)" opacity=".5"></path></g>')
    body = f'<path d="{d}" fill="{T_TOP}"></path>' + "".join(pat)

    det = []
    rng = random.Random(11)
    for i, (x0, x1, y) in enumerate(TER):
        a, b = max(x0, -20), x1
        wet = i < WET
        # the tread, seen a little from above
        tread = f"M{f(a)} {f(y)} L{f(a + 5)} {f(y - TREAD)} L{f(b)} {f(y - TREAD)} L{f(b)} {f(y)} Z"
        if wet:
            det.append(f'<path d="{tread}" fill="#86BCC2"></path>')
            ripples = " ".join(f"M{f(xx)} {f(y - TREAD * rr)} h{f(rng.uniform(8, 18))}"
                               for xx, rr in ((rng.uniform(a + 10, b - 24), rng.choice([.3, .5, .7]))
                                              for _ in range(int((b - a) / 26))))
            det.append(f'<path d="{ripples}" stroke="{DAY}" stroke-width="1" opacity=".85"></path>')
            det.append(f'<path d="M{f(a + 5)} {f(y - TREAD)} H{f(b)}" stroke="{PETROL}" stroke-width="1" opacity=".6"></path>')
            # the bund on the downhill edge that holds the water
            det.append(f'<path d="M{f(a - 1)} {f(y + .5)} Q{f(a + 3)} {f(y - 5)} {f(a + 7)} {f(y - TREAD - 1)}" '
                       f'stroke="{OLIVE}" stroke-width="3" fill="none" stroke-linecap="round"></path>')
        else:
            det.append(f'<path d="{tread}" fill="{CHART}"></path>')
            det.append(f'<path d="M{f(a + 5)} {f(y - TREAD)} H{f(b)}" stroke="{OLIVE}" stroke-width="1" opacity=".8"></path>')
        det.append(f'<path d="M{f(a)} {f(y)} H{f(b)}" stroke="{INK}" stroke-width="1.4"></path>')
        # stakes: one plot per unit, of uneven widths
        if i < len(TER) - 1:
            xs, xx = [], a + rng.uniform(20, 40)
            while xx < b - 14:
                xs.append(xx)
                xx += rng.uniform(22, 52)
            det.append("".join(f'<path d="M{f(s)} {f(y + 1)} L{f(s + 2)} {f(y - TREAD - 5)}" stroke="{INK}" '
                               f'stroke-width="1.3" stroke-linecap="round"></path>' for s in xs))
        # the retaining wall up to the next terrace
        if i < len(TER) - 1:
            ny = TER[i + 1][2]
            wall = f"M{f(b)} {f(y)} V{f(ny - TREAD)} L{f(b + 5)} {f(ny - TREAD)} L{f(b + 5)} {f(ny)} L{f(b)} {f(y)} Z"
            det.append(f'<path d="M{f(b)} {f(y)} V{f(ny)}" stroke="{INK}" stroke-width="1.4"></path>')
            courses = " ".join(f"M{f(b - 9)} {f(yy)} h9" for yy in frange(ny + 7, y - 2, 7))
            joints = " ".join(f"M{f(b - (4 if k % 2 else 7))} {f(yy)} v7"
                              for k, yy in enumerate(frange(ny + 7, y - 9, 7)))
            det.append(f'<path d="M{f(b - 10)} {f(ny)} H{f(b)} V{f(y)} H{f(b - 10)} Z" fill="#D8D1B6"></path>')
            det.append(f'<path d="{courses} {joints}" stroke="{INK}" stroke-width=".6" opacity=".55"></path>')
            _ = wall
    return body, "".join(det)


def drawing() -> str:
    g: list[str] = []
    # far ridge: the city on its crest, falling away east behind the plateau
    de = L["de"]
    far = [(-20, de + 50), (80, de + 38), (240, de + 32), (420, de + 34), (560, de + 50), (660, de + 130),
           (770, de + 360), (880, TOP_Y + 6)]
    g.append(f'<path d="{ridge(far, S)}" fill="#2E7682"></path>')
    cg = lambda x: de + 36 + 3 * math.sin(x / 90)  # noqa: E731
    g.append(city(92, cg))

    # the wind ridge; its eastern shoulder is a bench of solar rows
    wi, so = L["wi"], L["so"]
    bench = [(600, so + 16), (660, so + 20), (720, so + 22), (770, so + 26)]
    mid = [(-20, wi + 170), (110, wi + 112), (240, wi + 78), (380, wi + 70), (500, wi + 86), (556, so - 6)] + bench + \
        [(830, so + 70), (900, TOP_Y + 6)]
    g.append(f'<path d="{ridge(mid, S)}" fill="{HORIZON}"></path>')
    crest = lambda x: wi + 72 + 9 * ((x - 380) / 130) ** 2  # noqa: E731
    for i, tx in enumerate([232, 296, 360, 424, 488]):
        base = crest(tx) + 3
        h = base - wi
        g.append(turbine(tx, base, h, h * .5, ["sp1", "sp2", "sp3"][i % 3], 25 * i + 10))
    # the energised field on the bench, and the panel rows standing in it
    top = smooth(mid[5:10])
    under = smooth([(x, y + 20) for x, y in reversed(mid[5:10])])
    g.append(f'<path d="{top} L{under[1:]} Z" fill="{CHART}"></path>')
    g.append(f'<path d="{top}" stroke="{OLIVE}" stroke-width="1" fill="none"></path>')
    g.append(solar_rows(616, 772, lambda x: so + 18, rows=((0.84, 22), (0.92, 11), (1.0, 0))))

    # a transmission line from the gas plant, up the flank and over towards the city
    pyl = [(628, SM - 104, .46), (500, SM - 200, .38), (400, SM - 290, .31), (318, SM - 370, .25),
           (250, SM - 436, .2), (196, SM - 490, .16)]
    wires = []
    for (xa, ya, sa), (xb, yb, sb) in zip(pyl, pyl[1:]):
        wires.append(spans(tips(xa, ya, sa, -1), tips(xb, yb, sb, 1), 6 * sa))
    g.append(f'<g stroke="{INK}" fill="none" stroke-linecap="round" stroke-width="1.2">'
             + "".join(pylon(x, y, sc_) for x, y, sc_ in pyl) + "</g>")
    g.append(f'<path d="{" ".join(wires)}" stroke="{INK}" stroke-width=".7" fill="none" opacity=".8"></path>')
    PYL0[:] = [pyl[0]]

    # the terraced hillside in front
    body, det = terraces()
    g.append(body)
    g.append(det)
    # the first dry terrace carries a gas station, wired to the line of pylons
    t = TER[WET]
    cx, cy = t[0] + 16, t[2] - TREAD + 3
    g.append(f'<g transform="translate({f(cx)} {f(cy)}) scale(.5) translate({f(-cx)} {f(-cy)})">{ccgt(cx, cy, 1.0)}</g>')
    px, py, ps = PYL0[0]
    g.append(f'<path d="{spans([(cx + 62 * .5, cy - 18)] * 3, tips(px, py, ps, 1), 4)}" stroke="{INK}" '
             f'stroke-width=".7" fill="none" opacity=".8"></path>')

    # residual demand: the span of the fill, measured from the bottom of the stack to where it stops
    x0, x1 = 36, TER[WET - 1][1]
    y = L["rd"]
    g.append(f'<path d="M{x0} {f(TER[0][2] - TREAD - 4)} V{f(y + 9)} M{f(x1)} {f(SM - TREAD - 4)} V{f(y + 9)}" '
             f'stroke="{DAY}" stroke-width="1" stroke-dasharray="2 3"></path>')
    g.append(f'<path d="M{x0} {f(y)} H{f(x1)} M{x0} {f(y - 7)} V{f(y + 7)} M{f(x1)} {f(y - 7)} V{f(y + 7)}" '
             f'stroke="{DAY}" stroke-width="1.6"></path>')
    g.append(f'<path d="M{x0 + 10} {f(y - 4)} L{x0 + 1} {f(y)} L{x0 + 10} {f(y + 4)} M{f(x1 - 10)} {f(y - 4)} '
             f'L{f(x1 - 1)} {f(y)} L{f(x1 - 10)} {f(y + 4)}" stroke="{DAY}" stroke-width="1.6" fill="none"></path>')
    # SMP: a gauge post standing in the marginal terrace's water
    gx = TER[WET - 1][1] - 30
    g.append(f'<rect x="{f(gx)}" y="{f(SM - 58)}" width="7" height="{f(58 - 2)}" fill="{DAY}" stroke="{INK}" '
             f'stroke-width="1"></rect>' +
             "".join(f'<path d="M{f(gx)} {f(yy)} h{4 if k % 2 else 7}" stroke="{INK}" stroke-width="1"></path>'
                     for k, yy in enumerate(frange(SM - 52, SM - 6, 6))) +
             f'<path d="M{f(gx - 8)} {f(SM - TREAD * .5)} H{f(gx + 15)}" stroke="{DAY}" stroke-width="1.4"></path>')

    aria = ("A landscape read from far to near. On the farthest ridge, a city. On the next ridge, a row of wind "
            "turbines, and on its shoulder rows of solar panels. In front, a hillside cut into terraces that climb "
            "from left to right, the cheapest lowest, each terrace divided by stakes into plots, with a gas station on "
            "the first dry terrace and a line of pylons climbing towards the city. Water has been let into the "
            "lowest terraces, from the bottom up; a "
            "dimension line above measures how far along the hillside it reaches, and a gauge post stands in the "
            "highest wet terrace, where the water stops.")
    return (f'<svg class="draw mo-draw" width="{W}" height="{PLATE_H}" viewBox="0 0 {W} {PLATE_H}" role="img" '
            f'aria-label="{aria}">{"".join(g)}</svg>')


# ---------------------------------------------------------------- marks and entries
def marks() -> dict[str, str]:
    m = {}
    m["de"] = mark_svg(f'<path d="M1 19 V10 L6 5 L11 10 V19 Z" fill="{DAY}"></path><path d="M1 10 L6 5 L11 10" '
                       f'fill="{CLAY}"></path><rect x="13" y="2" width="7" height="17" fill="#D8D3BF"></rect>'
                       f'<path d="M22 19 V11 L26 7 L30 11 V19 Z" fill="{DAY}"></path>'
                       f'<path d="M1 19 V10 L6 5 L11 10 V19 M13 19 V2 H20 V19 M22 19 V11 L26 7 L30 11 V19" '
                       f'stroke="{INK}" stroke-width=".8" fill="none"></path>')
    m["wi"] = mark_svg(turbine(15, 30, 20, 9.5, "", 12)
                       .replace('class="rot "', 'class=""'), 30, 20).replace('viewBox="0 0 30 20"', 'viewBox="0 0 30 20"')
    m["so"] = mark_svg(solar_rows(2, 30, lambda x: 19, rows=((1.0, 0),)).replace(f'fill="{CHART}"', f'fill="{CHART}"'))
    m["st"] = mark_svg(f'<path d="M0 20 V15 H11 V8 H20 V2 H30 V20 Z" fill="{T_TOP}"></path>'
                       f'<path d="M0 15 H11 M11 8 H20 M20 2 H30" stroke="{CHART}" stroke-width="3"></path>'
                       f'<path d="M0 15 H11 V8 H20 V2 H30" stroke="{INK}" stroke-width="1.3" fill="none"></path>'
                       f'<path d="M7 11 h4 M16 4 h4 M16 6.5 h4" stroke="{INK}" stroke-width=".6"></path>')
    m["rd"] = mark_svg(f'<path d="M1 10 H29 M1 4 V16 M29 4 V16" stroke="{INK}" stroke-width="1.6"></path>'
                       f'<path d="M8 6.5 L2 10 L8 13.5 M22 6.5 L28 10 L22 13.5" stroke="{INK}" stroke-width="1.4" '
                       f'fill="none"></path>')
    m["sm"] = mark_svg(f'<path d="M0 20 V14 H30 V20 Z" fill="{T_TOP}"></path>'
                       f'<path d="M1 14 L3 8 H30 V14 Z" fill="#8FC0C4"></path>'
                       f'<path d="M6 11 h7 M17 10 h6" stroke="{DAY}" stroke-width="1"></path>'
                       f'<path d="M0 14 H30" stroke="{INK}" stroke-width="1.4"></path>'
                       f'<rect x="21" y="0" width="5" height="13" fill="{DAY}" stroke="{INK}" stroke-width=".9"></rect>'
                       f'<path d="M21 3 h3 M21 6 h2 M21 9 h3" stroke="{INK}" stroke-width=".8"></path>')
    return m


def entries() -> list[dict]:
    m = marks()
    return [
        dict(y=L["de"], mark=m["de"], name="Day-ahead demand", sky=True,
             id="day_ahead.lgbm_demand.v1, .v2",
             d="GB national demand outturn (<code>elexon/indo</code>), half-hourly, 24 hours ahead; v2 adds weather "
               "and calendar.",
             f="v1: median pinball loss 711.04 MW over 12 walk-forward folds."),
        dict(y=L["wi"], mark=m["wi"], name="Wind generation", sky=True, id="wind.lgbm_quantile.v1",
             d="GB wind outturn from <code>elexon/fuelhh</code>, 24 hours ahead, on weather at 12 sites; "
               "benchmark WINDFOR.",
             f="A model card and a training dataset; no forecasts or metrics in the store."),
        dict(y=L["so"], mark=m["so"], name="Solar generation", sky=True, id="solar.lgbm_quantile.v1",
             d="Weather at 6 sites; benchmark persistence. Its configured target, FUELHH solar, has no rows.",
             f="A model card; no forecasts or metrics in the store."),
        dict(y=L["st"], mark=m["st"], name="GB merit-order stack", id="stack.gb.v1",
             d="Constructive, with no training step: units from <code>bmunits_reference</code> ranked by short-run "
               "marginal cost, down to a floor of −500 £/MWh.",
             f="Its supply-curve points are stored with each SMP run."),
        dict(y=L["rd"], mark=m["rd"], name="Residual demand", quiet=True,
             d="Demand outturn less wind, less solar, less signed netting: what the stack has to meet."),
        dict(y=L["sm"], mark=m["sm"], name="Fundamentals SMP", id="fundamentals_smp.gb.v1",
             d="The stack cleared against realised residual demand, perfect-prognosis, half-hourly; scored against "
               "Elexon MID APXMIDP.",
             f="Mean bias −151.80 £/MWh over 816 periods, 18 August to 3 September 2026."),
    ]


# ---------------------------------------------------------------- the gold band: the five models, two charts
MODELS = [
    ("Day-ahead demand", "day_ahead.lgbm_demand.v1<br>day_ahead.lgbm_demand.v2",
     "GB national demand outturn, half-hourly, MW (<code>elexon/indo</code>). 24 hours ahead.",
     "LightGBM quantile regression, one model per quantile (0.05 to 0.95), conformal outer band. v2 adds weather "
     "and calendar.",
     "21 v1 and 1 v2 versions in the manifest; walk-forward backtests; one issued v2 forecast, 4 to 6 September 2026.",
     "v1: 711.04 MW, coverage 0.893, 12 folds. v2: 599.72 MW, 0.883, with actual weather used as if forecast."),
    ("Wind generation", "wind.lgbm_quantile.v1",
     "GB wind outturn, half-hourly, MW (<code>elexon/fuelhh</code>, WIND). 24 hours ahead.",
     "LightGBM quantile regression on weather at 12 sites; benchmark WINDFOR.",
     "A model card and a training dataset file; no manifest entry, forecasts or metrics.", "None"),
    ("Solar generation", "solar.lgbm_quantile.v1",
     "Configured as <code>elexon/fuelhh</code> SOLAR, which has no rows. 24 hours ahead.",
     "LightGBM quantile regression on weather at 6 sites; benchmark persistence.",
     "A model card; no manifest entry, forecasts or metrics.", "None"),
    ("GB merit-order stack", "stack.gb.v1",
     "The GB supply curve at a settlement period: units by short-run marginal cost, cumulative MW, £/MWh, floor −500.",
     "Constructive: <code>bmunits_reference</code> inventory, REMIT availability, manual fuel and carbon prices, "
     "plant-technology parameters.",
     "Supply-curve points in gold with each SMP run.", "Scored through the SMP"),
    ("Fundamentals SMP", "fundamentals_smp.gb.v1",
     "GB day-ahead system marginal price, half-hourly, £/MWh, scored against <code>elexon/mid</code> APXMIDP.",
     "The stack cleared against realised residual demand, perfect-prognosis.",
     "A headline backtest and 13 monthly diagnostic runs in gold.",
     "Mean bias −151.80 £/MWh over 816 periods; the 13 monthly runs, −69.81."),
]


def demand_chart() -> str:
    s = PACK["series"]["models_landing_demand"]
    pts = s["points"]
    w, h = 1280, 300
    x0, x1, y0, y1 = 70, w - 10, 16, h - 40
    lo, hi = 16000, 32000
    X = lambda i: x0 + i * (x1 - x0) / (len(pts) - 1)  # noqa: E731
    Y = lambda v: y1 - (v - lo) / (hi - lo) * (y1 - y0)  # noqa: E731
    band = ("M" + " L".join(f"{f(X(i))} {f(Y(p[4]))}" for i, p in enumerate(pts)) + " L" +
            " L".join(f"{f(X(i))} {f(Y(p[2]))}" for i, p in reversed(list(enumerate(pts)))) + " Z")
    med = "M" + " L".join(f"{f(X(i))} {f(Y(p[3]))}" for i, p in enumerate(pts))
    act = "M" + " L".join(f"{f(X(i))} {f(Y(p[1]))}" for i, p in enumerate(pts))
    ticks = ""
    for v in (16000, 20000, 24000, 28000, 32000):
        ticks += (f'<path d="M{x0 - 5} {f(Y(v))} H{x0}" stroke="{INK}" stroke-width="1"></path>'
                  f'<text x="{x0 - 9}" y="{f(Y(v) + 4.5)}" text-anchor="end">{v:,}</text>')
    for i, lab in [(0, "20 Aug 00:00"), (12, "06:00"), (24, "12:00"), (36, "18:00"), (48, "21 Aug 00:00"),
                   (60, "06:00"), (72, "12:00"), (84, "18:00")]:
        anchor = "start" if i == 0 else "middle"
        ticks += (f'<path d="M{f(X(i))} {y1} v5" stroke="{INK}" stroke-width="1"></path>'
                  f'<text x="{f(X(i))}" y="{y1 + 21}" text-anchor="{anchor}">{lab}</text>')
    lab = (f'<text x="{f(X(30))}" y="{f(Y(pts[30][4]) - 12)}" font-style="italic">5 to 95% band</text>'
           f'<text x="{f(X(64))}" y="{f(Y(pts[64][1]) + 30)}" font-style="italic">outturn</text>')
    aria = ("Line chart of GB national demand, 20 to 21 August 2026, in megawatts: the day-ahead demand model's "
            "5 to 95% band and median, with the outturn. Demand runs between about 19,000 and 28,500 MW, peaking in "
            "the evening, and the outturn stays mostly inside the band.")
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{aria}">'
            f'<path d="{band}" fill="{HORIZON}" opacity=".28"></path>'
            f'<g font-family="Hanken Grotesk" font-size="13.5" fill="{INK2}">{ticks}{lab}</g>'
            f'<path d="M{x0} {y0 - 6} V{y1} H{x1}" stroke="{INK}" stroke-width="1.5" fill="none"></path>'
            f'<text x="{x0 + 8}" y="{y0 + 2}" font-family="Hanken Grotesk" font-style="italic" font-size="13.5" '
            f'fill="{INK}">MW</text>'
            f'<path d="{med}" stroke="{PETROL}" stroke-width="1.8" fill="none" stroke-linejoin="round"></path>'
            f'<path d="{act}" stroke="{INK}" stroke-width="1.4" fill="none" stroke-linejoin="round"></path></svg>')


def smp_chart() -> str:
    s = PACK["series"]["models_landing_smp"]
    pts = s["points"]
    w, h = 1280, 300
    x0, x1, y0, y1 = 70, w - 130, 16, h - 40
    lo, hi = -150, 200
    X = lambda i: x0 + 20 + i * (x1 - x0 - 40) / (len(pts) - 1)  # noqa: E731
    Y = lambda v: y1 - (v - lo) / (hi - lo) * (y1 - y0)  # noqa: E731
    clear = "M" + " L".join(f"{f(X(i))} {f(Y(p[1]))}" for i, p in enumerate(pts))
    apx = "M" + " L".join(f"{f(X(i))} {f(Y(p[2]))}" for i, p in enumerate(pts))
    dots = "".join(f'<circle cx="{f(X(i))}" cy="{f(Y(p[1]))}" r="2.6" fill="{PETROL}"></circle>'
                   f'<circle cx="{f(X(i))}" cy="{f(Y(p[2]))}" r="2.6" fill="{INK}"></circle>' for i, p in enumerate(pts))
    ticks = ""
    for v in (-150, -100, -50, 0, 50, 100, 150, 200):
        ticks += (f'<path d="M{x0 - 5} {f(Y(v))} H{x0}" stroke="{INK}" stroke-width="1"></path>'
                  f'<text x="{x0 - 9}" y="{f(Y(v) + 4.5)}" text-anchor="end">{v}</text>'.replace(">-", ">−"))
    for i, lab in [(0, "18 Aug"), (4, "22 Aug"), (8, "26 Aug"), (12, "30 Aug"), (16, "3 Sep")]:
        ticks += (f'<path d="M{f(X(i))} {y1} v5" stroke="{INK}" stroke-width="1"></path>'
                  f'<text x="{f(X(i))}" y="{y1 + 21}" text-anchor="middle">{lab}</text>')
    zero = f'<path d="M{x0} {f(Y(0))} H{x1}" stroke="{INK}" stroke-width=".8" opacity=".45"></path>'
    labs = (f'<text x="{f(X(16) + 12)}" y="{f(Y(pts[16][2]) + 5)}">APXMIDP</text>'
            f'<text x="{f(X(16) + 12)}" y="{f(Y(pts[16][1]) + 5)}">Clearing price</text>')
    aria = ("Line chart, 18 August to 3 September 2026, in pounds per megawatt-hour: the daily mean of the model's "
            "clearing price against the daily mean of APXMIDP. APXMIDP runs between about 90 and 167; the clearing "
            "price sits below it every day, between about minus 136 and 78.")
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{aria}">'
            f'<g font-family="Hanken Grotesk" font-size="13.5" fill="{INK2}">{ticks}</g>{zero}'
            f'<path d="M{x0} {y0 - 6} V{y1} H{x1}" stroke="{INK}" stroke-width="1.5" fill="none"></path>'
            f'<text x="{x0 + 8}" y="{y0 + 2}" font-family="Hanken Grotesk" font-style="italic" font-size="13.5" '
            f'fill="{INK}">£/MWh</text>'
            f'<path d="{apx}" stroke="{INK}" stroke-width="1.6" fill="none" stroke-linejoin="round"></path>'
            f'<path d="{clear}" stroke="{PETROL}" stroke-width="1.8" fill="none" stroke-linejoin="round"></path>{dots}'
            f'<g font-family="Hanken Grotesk" font-size="14" font-weight="600" fill="{INK}">{labs}</g></svg>')


def gold_band() -> str:
    rows = "".join(f'<tr><th scope="row"><span class="mn">{n}</span><span class="mid">{i}</span></th><td>{t}</td>'
                   f'<td>{me}</td><td>{ex}</td><td class="sc">{sc}</td></tr>' for n, i, t, me, ex, sc in MODELS)
    return (f'<section class="band mo-gold" aria-labelledby="fm-h" style="height: {GOLD_H}px; padding-top: 84px">'
            f'<div class="sec"><h2 id="fm-h">The five models</h2>'
            f'<p>gridflow-models is a separate library that reads gridflow’s DuckDB and Parquet and writes its '
            f'outputs back to gold. Demand is one model with two registered versions.</p></div>'
            f'<table class="mt" aria-labelledby="fm-h"><thead><tr><th scope="col">Model</th>'
            f'<th scope="col">Target and horizon</th><th scope="col">Method</th><th scope="col">What exists</th>'
            f'<th scope="col">Score in the store</th></tr></thead><tbody>{rows}</tbody></table>'
            f'<p class="cap">Median pinball loss is the quantile loss at q = 0.5: half the mean absolute error of the '
            f'median forecast, in MW. Coverage is the share of outturns inside the 5 to 95% band.</p>'
            f'<figure class="mf" aria-labelledby="dc-h"><h3 class="fig-h" id="dc-h">Day-ahead demand against outturn, '
            f'20 to 21 August 2026</h3>{demand_chart()}'
            f'<figcaption class="cap">The v1 model’s 5 to 95% band and median, issued a day ahead, against the INDO '
            f'outturn: walk-forward fold 12 of run <code>a55a829bc51c40b2</code>, 96 half-hours, MW. Source: gold '
            f'<code>forecasts</code>.</figcaption></figure>'
            f'<figure class="mf" aria-labelledby="sc-h"><h3 class="fig-h" id="sc-h">Clearing price against APXMIDP, '
            f'daily mean, 18 August to 3 September 2026</h3>{smp_chart()}'
            f'<figcaption class="cap">A perfect-prognosis backtest: realised demand, wind and solar stand in for '
            f'forecasts. Fuel and carbon prices are synthetic. APXMIDP, from Elexon MID, mixes day-ahead and intraday '
            f'trades, so it is not one auction. The −500 £/MWh floor pulls the daily means down. Run '
            f'<code>41de423cfc0b421e</code>, 816 periods, £/MWh. Source: gold <code>stack_clearing</code> joined to '
            f'<code>gold_gb_day_ahead_benchmark</code>.</figcaption></figure></section>')


NB = """<span class="c">from</span> gridflow_models <span class="c">import</span> setup_notebook
data, models, common = setup_notebook()

models.list()                        <span class="k"># id, family, version, status</span>
models.demand_forecast.predict(...)  <span class="k"># also train, validate</span>
models.stack.build(as_of)
models.stack.clear(as_of, demand_mw)
models.fundamentals_smp.backtest(...)
data.gb_day_ahead_benchmark(start, end)"""


def deep() -> str:
    return (f'<section class="band deep mo-deep" aria-labelledby="nb-h" style="height: {DEEP_H - 250}px; '
            f'padding-top: 120px"><div class="nb-two"><div><h2 id="nb-h">From a notebook</h2>'
            f'<p>One call sets up a notebook: a data handle over every gridflow source, and one client per '
            f'configured model: <code>demand_forecast</code>, <code>demand_forecast_v2</code>, '
            f'<code>wind_forecast</code>, <code>solar_forecast</code>, <code>stack</code> and '
            f'<code>fundamentals_smp</code>.</p><p>Notebooks are call sites only. The model logic lives in the '
            f'library.</p></div><pre class="nb" aria-label="Workbench calls">{NB}</pre></div></section>')


MO_CSS = """.mt{width:100%;border-collapse:collapse;margin-top:28px;font-size:14.5px;line-height:1.5;color:#3F4A3B}
.mt th[scope=col]{text-align:left;font-weight:600;font-size:14px;color:#3F4A3B;padding:0 18px 10px 0;border-bottom:1px solid #1C2B22}
.mt th[scope=row]{text-align:left;font-weight:400;width:236px}
.mt td,.mt th[scope=row]{padding:14px 18px 14px 0;border-bottom:1px solid rgba(28,43,34,.22);vertical-align:top}
.mt td:nth-child(2){width:250px}
.mt td:nth-child(3){width:270px}
.mt td:nth-child(4){width:240px}
.mt td.sc{color:#1C2B22;font-weight:600;padding-right:0}
.mt code{font-size:13px;color:#1C2B22}
.mn{display:block;font-family:"Bricolage Grotesque",sans-serif;font-size:20px;font-weight:700;font-stretch:90%;line-height:1.15;color:#1C2B22}
.mid{display:block;margin-top:4px;font:400 13px/1.45 "Red Hat Mono",monospace;color:#155A6E}
.mf{margin:72px 0 0}
.mf .fig-h{margin-bottom:14px}
.mo-gold > .cap{margin-top:14px}
.nb-two{display:grid;grid-template-columns:440px minmax(0,1fr);column-gap:96px;align-items:start}
.mo-deep h2{font-size:42px;font-weight:720;font-stretch:88%;line-height:1.02;letter-spacing:-.018em;margin:0 0 18px;color:#F6F4EC}
.mo-deep p{margin:0 0 14px;font-size:16px;line-height:1.62;color:#CFE0DC}
.mo-deep p code{font-size:.86em;color:#F6F4EC}
.nb{margin:8px 0 0;padding:26px 28px;background:#0F4757;border:1px solid rgba(207,224,220,.25);border-radius:4px;font:400 14px/1.75 "Red Hat Mono",monospace;color:#F6F4EC;white-space:pre;overflow:hidden}
.nb .c{color:#AFC64E}
.nb .k{color:#B4D0CD}
"""


def build() -> str:
    hero = (f'<section class="band hero" aria-labelledby="h1" style="height: {HERO_H}px">'
            f'<h1 id="h1">From demand to a price</h1>'
            f'<div class="lede"><p>Five models, from GB demand to a day-ahead price.</p>'
            f'<p>The aim is a price forecast: the input that trading research starts from.</p></div></section>')
    ents = [dict(e, y=e["y"] - (TITLE_TOP + TITLE_H)) for e in entries()]
    plate = (f'<section class="band" aria-labelledby="pl-h" style="height: {PLATE_H}px">{drawing()}'
             f'<div class="plate" style="position: relative; padding-top: {TITLE_TOP}px">'
             f'<h2 class="plate-h sky" id="pl-h" style="grid-column: 1 / -1; height: {TITLE_H}px">'
             f'Residual demand meets the stack</h2>'
             f'{index_list(ents, "The five models, keyed to the drawing")}</div></section>')
    flow = "\n".join([masthead("Models"), "<main>", hero, plate, gold_band(), deep(), "</main>", footer(250, 40)])
    c_g = P + PLATE_H
    c_d = c_g + GOLD_H + 30
    bg = bg_layer(H, strata(H, P + S, [(c_g, "gold"), (c_d, "deep")], land=False, names=False))
    return page("Models", H, bg, flow, MO_CSS)


_ = (GOLD, KHAKI)

if __name__ == "__main__":
    emit("B-models", build())
    print("H", H, "levels", {k: round(v) for k, v in L.items()}, "TOP_Y", TOP_Y, "S", S, "PLATE_H", PLATE_H)
