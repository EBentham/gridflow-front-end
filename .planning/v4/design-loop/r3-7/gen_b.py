"""Round 7, variant B: "Clearing a distribution". Emits R3-v5-B.dc.html + static/R3-v5-B.html.

Everything outside the purpose section is rendered by gen.page(), so it is inherited byte for byte from
R3-v4-P1. Every shape in the drawing is schematic: widths, heights, costs and draws are drawn, not data.
"""
from __future__ import annotations

import math
import random
from statistics import NormalDist

import gen
from gen import (AIM, BUILD, CASE, CHART, CLAY, DAY, GOLD, HORIZON, INK, INTRO, MID, OLIVE, PETROL, RD, SW3,
                 T_TOP, TRANCHES, UNITS, WHY_H2, Y, cost_at, f, pat_defs, stack_draw)

# ---------------------------------------------------------------- geometry (page px unless noted)
T = Y["p_head"]                 # 1414, the h2 top
D_TOP, D_LEFT = T + 176, 80     # the drawing block
D_W = 948
PX, SW = 150, 764               # price axis x and stack width (svg px); stack ends at 914, page 994
BY, PH = 440, 432               # capacity axis y and the drawn cost height (svg px)
HIST_D = 58                     # depth of the residual-demand histogram under the capacity axis
ROWS = {"r": BY + 2, "s": BY + 112, "w": BY + 162, "d": BY + 212}   # svg y: histogram top, then each input row
D_H = ROWS["d"] + 24
BAR = 16                        # input bar height
IX = 1044                       # the index column (page x); it ends at 1310, left of the feed cables
IW = 266

X = lambda q: PX + q * SW       # noqa: E731
Q_LO, Q_HI = .2, .93            # the drawn residual-demand window, capacity units
# drawn spreads (capacity units) and the residual demand they imply, treating the three as independent
SD_D, SD_W, SD_S = .04, .075, .03
MU_R, WIND_M, SOLAR_M = .62, .24, .10
RDB = NormalDist(MU_R, math.sqrt(SD_D ** 2 + SD_W ** 2 + SD_S ** 2))
N_DRAW = 84


def sampled_draws(n: int, seed: int = 7) -> list[float]:
    """Deterministic but irregular: stratified quantiles, each jittered inside its own stratum."""
    rng = random.Random(seed)
    out = [RDB.inv_cdf((k + rng.random()) / n) for k in range(n)]
    return [min(max(q, Q_LO + .01), Q_HI - .01) for q in out]


def price_density(nb: int) -> list[float]:
    """A smoothed count of cleared prices per price bin (bins over the full drawn cost height, 0..1)."""
    counts = [0.0] * nb
    bw = .019
    for k in range(4000):
        c = cost_at(RDB.inv_cdf((k + .5) / 4000))
        for b in range(nb):
            mid = (b + .5) / nb
            counts[b] += math.exp(-.5 * ((mid - c) / bw) ** 2)
    return counts


def fan(cx: float, sd: float, y: float, fill: str) -> str:
    """A forecast's spread straddling a bar: p05 to p95 light, p25 to p75 dark, the median as a tick."""
    o, i, h = 1.645 * sd * SW, .674 * sd * SW, BAR + 10
    return (f'<rect x="{f(cx - o)}" y="{f(y - h / 2)}" width="{f(2 * o)}" height="{h}" fill="{fill}" opacity=".38" '
            f'stroke="{INK}" stroke-width=".6"></rect>'
            f'<rect x="{f(cx - i)}" y="{f(y - h / 2)}" width="{f(2 * i)}" height="{h}" fill="{fill}" opacity=".8"></rect>'
            f'<path d="M{f(cx)} {f(y - h / 2 - 3)} V{f(y + h / 2 + 3)}" stroke="{INK}" stroke-width="1.8"></path>')


def bar_row(y: float, segs: list[tuple[float, float, str, str]]) -> str:
    return "".join(f'<rect x="{f(a)}" y="{f(y - BAR / 2)}" width="{f(b - a)}" height="{BAR}" fill="{c}" opacity="{op}">'
                   f'</rect>' for a, b, c, op in segs)


def drawing() -> str:
    g = [f'<defs>{pat_defs("pb")}</defs>']
    ds = sampled_draws(N_DRAW)

    # the stack, large
    g.append(stack_draw("pb", PX, BY, SW, PH, joints_on=False))
    t, acc = [], 0.0
    for name, share, costs, fill, _ in TRANCHES:
        col = DAY if fill == PETROL else INK
        y = BY - costs[-1] * PH - 7 if name == "Biomass" else BY - 9
        t.append(f'<text x="{f(PX + acc * SW + (2 if name == "Biomass" else 7))}" y="{f(y)}" fill="{col}">{name}</text>')
        acc += share
    g.append(f'<g font-family="Hanken Grotesk" font-style="italic" font-size="14">{"".join(t)}</g>')

    # distribution in: residual demand as a histogram hanging under the capacity axis
    nb_in = round((Q_HI - Q_LO) * SW / (PH / 60))   # the same bin thickness as the price histogram
    step = (Q_HI - Q_LO) / nb_in
    pdf = [RDB.pdf(Q_LO + (b + .5) * step) for b in range(nb_in)]
    pm = max(pdf)
    bars_in = "".join(
        f'<rect x="{f(X(Q_LO + b * step) + .4)}" y="{BY + 2}" width="{f(step * SW - .8)}" '
        f'height="{f(p / pm * HIST_D)}"></rect>' for b, p in enumerate(pdf) if p / pm * HIST_D > 2)
    g.append(f'<g fill="{OLIVE}" opacity=".72">{bars_in}</g>')

    # the draws: each one rises from the axis through the stack to the curve, clears, and runs to the price axis
    ups = " ".join(f"M{f(X(q))} {BY} V{f(BY - cost_at(q) * PH)}" for q in ds)
    outs = " ".join(f"M{f(X(q))} {f(BY - cost_at(q) * PH)} H{PX}" for q in ds[::3])
    g.append(f'<path d="{ups}" stroke="{DAY}" stroke-width="1" opacity=".7"></path>')
    g.append(f'<path d="{outs}" stroke="{INK}" stroke-width=".8" opacity=".22"></path>')
    g.append(f'<g fill="{INK}">' + "".join(
        f'<circle cx="{f(X(q))}" cy="{f(BY - cost_at(q) * PH)}" r="1.7"></circle>' for q in ds) + '</g>')

    # distribution out: the cleared prices pile up against the price axis
    nb = 60
    dens = price_density(nb)
    dm = max(dens)
    bh = PH / nb
    bars = "".join(
        f'<rect x="{f(PX - 3 - n / dm * 122)}" y="{f(BY - (b + 1) * bh + .4)}" width="{f(n / dm * 122)}" '
        f'height="{f(bh - .8)}"></rect>' for b, n in enumerate(dens) if n / dm * 122 > .8)
    g.append(f'<g fill="{GOLD}">{bars}</g>')

    # axes, words only
    g.append(f'<path d="M{PX} {BY} V22 M{PX} {BY} H{PX + SW + 16}" stroke="{INK}" stroke-width="1.5" fill="none"></path>')
    g.append(f'<g font-family="Hanken Grotesk" font-style="italic" font-size="14" fill="{INK}">'
             f'<text x="{PX + 10}" y="30">price</text>'
             f'<text x="{PX + SW + 16}" y="{BY + 22}" text-anchor="end">capacity, cheapest first</text></g>')

    # the inputs, read from the bottom up and measured along the same capacity axis from zero: demand, then
    # wind carved off its end, then solar; what is left is residual demand, whose draws hang under the axis
    xr = X(MU_R)
    xw = X(MU_R + SOLAR_M)
    xd = X(MU_R + SOLAR_M + WIND_M)
    rs, rw, rd = ROWS["s"], ROWS["w"], ROWS["d"]
    g.append(bar_row(rd, [(PX, xd, OLIVE, ".4")]) + fan(xd, SD_D, rd, OLIVE))
    g.append(bar_row(rw, [(PX, xw, OLIVE, ".4"), (xw, xd, HORIZON, "1")]) + fan(xw, SD_W, rw, HORIZON))
    g.append(bar_row(rs, [(PX, xr, OLIVE, ".4"), (xr, xw, CHART, "1"), (xw, xd, HORIZON, ".3")])
             + fan(xr, SD_S, rs, CHART))
    hb = BAR / 2 + 8
    g.append(f'<path d="M{f(xd)} {rd - hb} V{rw + BAR / 2} M{f(xw)} {rw - hb} V{rs + BAR / 2} '
             f'M{f(xr)} {rs - hb} V{f(BY + 2 + HIST_D)}" stroke="{INK}" stroke-width="1" stroke-dasharray="1.5 3">'
             f'</path>')
    g.append(f'<g font-family="Hanken Grotesk" font-style="italic" font-size="14" fill="{INK}" text-anchor="end">'
             f'<text x="{PX - 12}" y="{BY + 24}">residual demand</text>'
             f'<text x="{PX - 12}" y="{rs + 5}">less solar</text>'
             f'<text x="{PX - 12}" y="{rw + 5}">less wind</text>'
             f'<text x="{PX - 12}" y="{rd + 5}">demand</text></g>')

    aria = ("How the price forecast is built, drawn without scales. Read from the bottom: a demand forecast is a bar "
            "along the capacity axis with its spread at the end; the wind forecast is carved off that end, then the "
            "solar forecast, each with its own spread. What is left is residual demand, drawn as a histogram of draws "
            "hanging under the capacity axis. Above it, a merit-order supply curve rises in steps: biomass, nuclear, "
            "a long run of CCGT units, coal, then OCGT. Many faint draws rise from the residual-demand histogram "
            "through the stack; each meets the curve and reads off a price, and the prices pile up as a second "
            "histogram along the price axis: a distribution in, a distribution out.")
    return (f'<svg width="{D_W}" height="{D_H}" viewBox="0 0 {D_W} {D_H}" role="img" aria-label="{aria}">'
            + "".join(g) + "</svg>")


# ---------------------------------------------------------------- the index marks (shape-distinct, 30 x 18)
def mark(kind: str) -> str:
    w, h = 30, 18
    if kind == "smp":         # a rotated histogram against an axis
        rows = [3, 7, 12, 9, 4]
        body = (f'<g fill="{GOLD}">' + "".join(
            f'<rect x="{25 - v * 1.7:.1f}" y="{2 + i * 3}" width="{v * 1.7:.1f}" height="2.4"></rect>'
            for i, v in enumerate(rows)) + '</g>'
            f'<path d="M26 1 V17" stroke="{INK}" stroke-width="1.4"></path>')
    elif kind == "stack":     # three steps
        body = (f'<rect x="1" y="12" width="7" height="5" fill="{PETROL}"></rect>'
                f'<rect x="8" y="8" width="13" height="9" fill="{CLAY}"></rect>'
                f'<rect x="21" y="3" width="8" height="14" fill="{CLAY}"></rect>'
                f'<path d="M1 12 H8 V8 H21 V3 H29" fill="none" stroke="{INK}" stroke-width="1.4"></path>')
    elif kind == "resid":     # a histogram hanging from an axis
        rows = [2, 5, 9, 11, 8, 4, 2]
        body = (f'<g fill="{OLIVE}" opacity=".7">' + "".join(
            f'<rect x="{1.5 + i * 4}" y="3" width="3.2" height="{v * 1.2:.1f}"></rect>' for i, v in enumerate(rows))
            + f'</g><path d="M0 2.5 H30" stroke="{INK}" stroke-width="1.4"></path>')
    elif kind == "solar":     # the solar row: olive, carved chartreuse, the wind already gone
        body = (f'<rect x="1" y="6" width="10" height="6" fill="{OLIVE}" opacity=".5"></rect>'
                f'<rect x="11" y="6" width="10" height="6" fill="{CHART}"></rect>'
                f'<rect x="21" y="6" width="8" height="6" fill="{HORIZON}" opacity=".3"></rect>'
                f'<rect x="7" y="3" width="8" height="12" fill="{CHART}" opacity=".38" stroke="{INK}" '
                f'stroke-width=".6"></rect><path d="M11 1 V17" stroke="{INK}" stroke-width="1.6"></path>')
    elif kind == "wind":      # the wind row: olive, carved horizon, a wide spread at the cut
        body = (f'<rect x="1" y="6" width="13" height="6" fill="{OLIVE}" opacity=".5"></rect>'
                f'<rect x="14" y="6" width="15" height="6" fill="{HORIZON}"></rect>'
                f'<rect x="7" y="3" width="14" height="12" fill="{HORIZON}" opacity=".38" stroke="{INK}" '
                f'stroke-width=".6"></rect><path d="M14 1 V17" stroke="{INK}" stroke-width="1.6"></path>')
    else:                     # the demand row: an olive bar with its spread at the end
        body = (f'<rect x="1" y="6" width="22" height="6" fill="{OLIVE}" opacity=".5"></rect>'
                f'<rect x="17" y="3" width="12" height="12" fill="{OLIVE}" opacity=".38" stroke="{INK}" '
                f'stroke-width=".6"></rect><rect x="20" y="3" width="6" height="12" fill="{OLIVE}" opacity=".8"></rect>'
                f'<path d="M23 1 V17" stroke="{INK}" stroke-width="1.6"></path>')
    return f'<svg class="b-mk" width="{w}" height="{h}" viewBox="0 0 {w} {h}" aria-hidden="true">{body}</svg>'


def entry(top: float, kind: str, name: str, rest: str, cls: str = "") -> str:
    return (f'<li class="b-e{(" " + cls) if cls else ""}" style="top: {f(top)}px">{mark(kind)}'
            f'<div><p class="b-n">{name}</p>{rest}</div></li>')


def b() -> str:
    idd = lambda k: f'<p class="b-id">{MID[k]}</p>'  # noqa: E731
    top = D_TOP + 10
    rows = lambda k: D_TOP + ROWS[k] - 11  # noqa: E731   # name line centred on the drawing row
    items = [
        entry(D_TOP + 34 - top, "stack", "Merit-order supply curve", idd("stack") +
              f'<p class="b-d">{BUILD}: GB plant in merit order, cheapest first.</p>'),
        entry(D_TOP + BY - .66 * PH - top, "smp", "Fundamentals SMP forecaster", idd("smp") +
              '<p class="b-d">Monte Carlo draws of residual demand, each cleared against the curve, build a price '
              'distribution. Backtested against ENTSO-E day-ahead prices.</p>'),
        entry(D_TOP + ROWS["r"] + 1 - top, "resid", "Residual demand",
              '<p class="b-d">Demand less wind and solar: 1,000 draws, each a demand draw less a wind draw and a '
              'solar draw.</p>', "b-q"),
        entry(rows("s") - top, "solar", "Solar generation", idd("solar")),
        entry(rows("w") - top, "wind", "Wind generation", idd("wind")),
        entry(rows("d") - top, "demand", "Day-ahead demand", idd("demand") + f'<p class="b-d">{CASE}</p>'),
    ]
    head = (f'<div class="blk b-h" style="top: {T}px; left: 80px; width: 1230px"><h2 id="why-h">{WHY_H2}</h2></div>'
            f'<p class="blk b-intro" style="top: {T + 80}px; left: 80px; width: 760px">{INTRO}</p>'
            f'<p class="blk b-aim" style="top: {T + 85}px; left: {IX}px; width: {IW}px">{AIM}</p>')
    draw = (f'<div class="blk b-draw" style="top: {D_TOP}px; left: {D_LEFT}px; width: {D_W}px; height: {D_H}px">'
            f'{drawing()}</div>')
    index = (f'<ul class="blk b-ix" aria-label="The models and residual demand, keyed to the drawing" '
             f'style="top: {top}px; left: {IX}px; width: {IW}px; height: {D_H}px">{"".join(items)}</ul>')
    return f'<section class="pb" aria-labelledby="why-h">{head}{draw}{index}</section>'


B_CSS = """.b-h h2{font-size:50px;font-weight:740;font-stretch:80%;line-height:1;letter-spacing:-.02em;white-space:nowrap}
.b-intro{margin:0;font-size:21px;line-height:1.5;color:#1C2B22}
.b-aim{margin:0;font-size:16px;line-height:1.55;font-weight:600;color:#1C2B22}
.b-draw svg{display:block}
.b-ix{list-style:none;margin:0;padding:0}
.b-e{position:absolute;left:0;right:0;display:grid;grid-template-columns:30px minmax(0,1fr);column-gap:14px;align-items:start}
.b-mk{display:block;margin-top:1px}
.b-n{margin:0;font-weight:600;font-size:15.5px;line-height:1.3;color:#1C2B22}
.b-id{margin:1px 0 0;font:400 13px/1.4 "Red Hat Mono",monospace;color:#155A6E}
.b-d{margin:4px 0 0;font-size:14px;line-height:1.45;color:#3F4A3B}
.b-d code{font-size:12.5px;color:#1C2B22}
.b-q .b-n{font-weight:500;font-style:italic}
.pb .more{font-weight:600;color:#1C2B22;text-decoration-color:#66793B}
"""

gen.PURPOSE["B"] = b
gen.PCSS["B"] = B_CSS

if __name__ == "__main__":
    _ = (SW3, T_TOP, TRANCHES, UNITS, NormalDist)
    out = gen.page("B")
    body_only = out.split('<script type="text/x-dc"')[0]
    assert "{{" not in body_only and "}}" not in body_only, "template-hole syntax in markup"
    assert "/>" not in gen.re.sub(r"<(meta|link|br)[^>]*>", "", body_only), "self-closing tag"
    (gen.HERE / "R3-v5-B.dc.html").write_text(out, encoding="utf-8")
    (gen.HERE / "static").mkdir(exist_ok=True)
    (gen.HERE / "static" / "R3-v5-B.html").write_text(gen.static(out), encoding="utf-8")
    print("H =", gen.H, "section", T, "to", D_TOP + D_H, "index ends", IX + IW)
