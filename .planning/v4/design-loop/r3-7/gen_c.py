"""Round 7, variant C: "The forecast, assembled". Emits R3-v5-C.dc.html (+ a static copy).

Three steps read left to right on one shared baseline and one shared vertical MW scale:
1. a day of demand (real median line) with wind and solar carved out of it (drawn),
2. the evening-peak residual demand carried straight across onto a merit-order stack drawn on its side
   (capacity up the shared vertical axis, price along the baseline), where the draws meet the stack's edge,
3. the price read off each crossing by dropping to the baseline, where a narrow distribution collects.
"""
from __future__ import annotations

import math
import re
from statistics import NormalDist

import gen
from gen import (CASE, CHART, CLAY, DAY, FAN, GOLD, HERE, HORIZON, INK, INTRO, AIM, KHAKI, MID, OLIVE, PETROL,
                 SOFT, T_TOP, WHY_H2, Y, f, line, band, pat_defs, page, static)

# ---------------------------------------------------------------- geometry (page x; y local to the drawing)
DT = 1520                 # drawing top, page y
DH = 806                  # drawing height (ends at page y 2326, above the cable tray at 2350)
YB = 2152 - DT            # the shared baseline
K = 14.0                  # px per GW, shared by the demand panel and the stack's capacity axis
CAPG = 42.0               # drawn stack capacity in the same px scale (never labelled)
CAP = CAPG * K
X1, DX = 84, 10.0         # demand panel: 48 half-hours
X2 = X1 + 48 * DX
X0, PW = 620, 730         # stack: capacity axis x, price extent (0..1 drawn cost)
DAY_I = 3                 # 4 August 2026 (settlement periods 145..192 of the fold)

TR = [  # name, share of capacity, drawn costs (0..1), fill, pattern
    ("Biomass", .07, [.04, .055], CHART, "bio"),
    ("Nuclear", .12, [.08, .095], PETROL, None),
    ("CCGT", .60, [.27 + .23 * (k / 17) ** 1.25 for k in range(18)], CLAY, "gas"),
    ("Coal", .07, [.60, .65], KHAKI, "coal"),
    ("OCGT", .14, [.77, .85], CLAY, "ocgt"),
]
PAT_OP = {"gas": ".22", "ocgt": ".4", "bio": ".3", "coal": ".35"}


def _units() -> list[tuple[float, float, float, int]]:
    out, q = [], 0.0
    for i, (_, share, costs, _, _) in enumerate(TR):
        w = share / len(costs)
        for c in costs:
            out.append((q, q + w, c, i))
            q += w
    return out


UNITS = _units()


def unit_at(q: float) -> int:
    for k, (_, q1, _, _) in enumerate(UNITS):
        if q < q1:
            return k
    return len(UNITS) - 1


def yq(q: float) -> float:
    """Capacity fraction to local y."""
    return YB - q * CAP


def xc(c: float) -> float:
    return X0 + c * PW


# ---------------------------------------------------------------- the day: real demand median, drawn wind and solar
D = [v / 1000 for v in FAN["q_0.5"][DAY_I * 48:(DAY_I + 1) * 48]]
assert FAN["settlement_date"][DAY_I * 48] == "2026-08-04" and len(D) == 48
WIND = [6.3 + 1.0 * math.sin(2 * math.pi * i / 48 * .9 + .5) + .3 * math.sin(i / 3.1 + 1) for i in range(48)]


def _solar(i: int) -> float:
    h = (i + .5) / 2
    return 3.4 * math.sin(math.pi * (h - 5.5) / 15.4) ** 1.6 if 5.5 < h < 20.9 else 0.0


SOLAR = [_solar(i) for i in range(48)]
RES = [d - w - s for d, w, s in zip(D, WIND, SOLAR)]
TS = max(range(48), key=lambda i: D[i])          # the evening peak half-hour (index 40, 20:00)
RS = RES[TS]
SIG = 1.3                                         # drawn residual spread at that half-hour, GW
RDIST = NormalDist(RS, SIG)
N_DRAW = 9
DRAWS = [RDIST.inv_cdf((k + .5) / N_DRAW) for k in range(N_DRAW)]
XS = [X1 + (i + .5) * DX for i in range(48)]


def ygw(v: float) -> float:
    return YB - v * K


def _ext(vals: list[float]) -> tuple[list[float], list[float]]:
    """Hold the first and last half-hour flat to the panel edges."""
    return [X1] + XS + [X2], [vals[0]] + vals + [vals[-1]]


def panel_day() -> list[str]:
    o = []
    xs, dd = _ext(D)
    _, rr = _ext(RES)
    _, ww = _ext([r + w for r, w in zip(RES, WIND)])
    base = [0.0] * len(xs)
    o.append(f'<path d="{band(xs, [ygw(v) for v in base], [ygw(v) for v in rr])}" fill="{OLIVE}" opacity=".4"></path>')
    o.append(f'<path d="{band(xs, [ygw(v) for v in rr], [ygw(v) for v in ww])}" fill="{HORIZON}" opacity=".5"></path>')
    o.append(f'<path d="{band(xs, [ygw(v) for v in ww], [ygw(v) for v in dd])}" fill="{CHART}" opacity=".72"></path>')
    o.append(f'<path d="{line(xs, [ygw(v) for v in rr])}" fill="none" stroke="{OLIVE}" stroke-width="2.2" '
             f'stroke-linejoin="round"></path>')
    o.append(f'<path d="{line(xs, [ygw(v) for v in dd])}" fill="none" stroke="{INK}" stroke-width="2" '
             f'stroke-linejoin="round"></path>')
    # the half-hour that is carried across
    xt = XS[TS]
    o.append(f'<path d="M{f(xt)} {YB} V{f(ygw(D[TS]) - 10)}" stroke="{INK}" stroke-width="1" '
             f'stroke-dasharray="2 3"></path>')
    # time axis
    ticks = "".join(f"M{f(X1 + h * 2 * DX)} {YB} V{YB + 5}" for h in (0, 6, 12, 18, 24))
    o.append(f'<path d="{ticks}" stroke="{INK}" stroke-width="1.2"></path>')
    lab = "".join(f'<text x="{f(X1 + h * 2 * DX)}" y="{YB + 21}" text-anchor="{a}">{h:02d}:00</text>'
                  for h, a in ((0, "start"), (6, "middle"), (12, "middle"), (18, "middle"), (24, "end")))
    o.append(f'<g font-family="Hanken Grotesk" font-size="12.5" fill="{SOFT}">{lab}</g>')
    # names on the bands
    o.append(f'<g font-family="Hanken Grotesk" font-style="italic" font-size="14" fill="{INK}">'
             f'<text x="{X1 + 12}" y="{YB - 18}">residual demand</text>'
             f'<text x="{f(XS[5])}" y="{f(ygw(RES[5] + WIND[5] / 2) + 5)}" text-anchor="middle">wind</text>'
             f'<text x="{f(XS[25])}" y="{f(ygw(RES[25] + WIND[25] + SOLAR[25] / 2) + 5)}" text-anchor="middle">solar</text>'
             f'<text x="{f(XS[16])}" y="{f(ygw(D[16]) - 12)}" text-anchor="middle">demand</text></g>')
    o.append(f'<text x="{f(xt - 8)}" y="{f(ygw(D[TS]) - 14)}" text-anchor="end" font-family="Hanken Grotesk" '
             f'font-size="14" font-weight="600" fill="{INK}">28.1 GW</text>')
    return o


def panel_stack() -> list[str]:
    o, joints, contacts = [], [], []
    for k, (q0, q1, c, i) in enumerate(UNITS):
        _, _, _, fill, pat = TR[i]
        top, bot, w = yq(q1), yq(q0), c * PW
        o.append(f'<rect x="{X0}" y="{f(top)}" width="{f(w)}" height="{f(bot - top + .4)}" fill="{fill}"></rect>')
        if pat:
            o.append(f'<rect x="{X0}" y="{f(top)}" width="{f(w)}" height="{f(bot - top + .4)}" '
                     f'fill="url(#pc-{pat})" opacity="{PAT_OP[pat]}"></rect>')
        if k:
            (joints if UNITS[k - 1][3] == i else contacts).append(f"M{X0} {f(bot)} H{f(xc(UNITS[k - 1][2]))}")
    o.append(f'<path d="{" ".join(joints)}" stroke="{T_TOP}" stroke-width="1" opacity=".75"></path>')
    o.append(f'<path d="{" ".join(contacts)}" stroke="{INK}" stroke-width="1"></path>')
    d = f"M{f(xc(UNITS[0][2]))} {YB}"
    for k, (q0, q1, c, _) in enumerate(UNITS):
        d += f" H{f(xc(c))} V{f(yq(q1))}"
    d += f" H{X0}"
    o.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="2" stroke-linejoin="round"></path>')
    # tranche names
    t, acc = [], 0.0
    for name, share, costs, fill, _ in TR:
        mid = yq(acc + share / 2) + 5
        if name == "CCGT":
            mid = yq(acc) - 14
        inside = costs[0] * PW > 64
        x = X0 + 8 if inside else xc(costs[-1]) + 8
        col = DAY if (fill == PETROL and inside) else INK
        t.append(f'<text x="{f(x)}" y="{f(mid)}" fill="{col}">{name}</text>')
        acc += share
    o.append(f'<g font-family="Hanken Grotesk" font-style="italic" font-size="14">{"".join(t)}</g>')
    return o


def carry_and_clear() -> tuple[list[str], list[float]]:
    """The residual draws leave the evening peak, run across into the stack and stop at its edge."""
    o = []
    xt = XS[TS]
    lo, hi = RDIST.inv_cdf(.05), RDIST.inv_cdf(.95)
    # the carried band: from the half-hour to the capacity axis
    o.append(f'<rect x="{f(xt)}" y="{f(ygw(hi))}" width="{f(X0 - xt)}" height="{f((hi - lo) * K)}" fill="{OLIVE}" '
             f'opacity=".4"></rect>')
    outside, inside, drops, dots = [], [], [], []
    xs_clear = []
    for r in DRAWS:
        y = ygw(r)
        c = UNITS[unit_at(r / CAPG)][2]
        x = xc(c)
        xs_clear.append(x)
        outside.append(f"M{f(xt)} {f(y)} H{X0}")
        inside.append(f"M{X0} {f(y)} H{f(x)}")
        dots.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="2.8"></circle>')
    o.append(f'<path d="{" ".join(outside)} {" ".join(inside)}" stroke="{INK}" stroke-width="1" opacity=".62"></path>')
    return o + [f'<g fill="{INK}">{"".join(dots)}</g>'], xs_clear


def panel_price(xs_clear: list[float]) -> tuple[list[str], float, float]:
    """Drop each crossing to the baseline; many more draws of the same half-hour pile up there."""
    o = []
    counts: dict[int, int] = {}
    n = 4000
    for k in range(n):
        u = unit_at(RDIST.inv_cdf((k + .5) / n) / CAPG)
        counts[u] = counts.get(u, 0) + 1
    mx = max(counts.values())
    hmax, bw = 104, 8.0
    tops = {}
    bars = []
    for u, cnt in sorted(counts.items()):
        x, h = xc(UNITS[u][2]), cnt / mx * hmax
        tops[round(x, 1)] = YB - h
        bars.append(f'<rect x="{f(x - bw / 2)}" y="{f(YB - h)}" width="{f(bw)}" height="{f(h)}"></rect>')
    drops = []
    for r, x in zip(DRAWS, xs_clear):
        drops.append(f"M{f(x)} {f(ygw(r) + 4)} V{f(tops[round(x, 1)] - 3)}")
    o.append(f'<path d="{" ".join(sorted(set(drops)))}" stroke="{INK}" stroke-width="1" stroke-dasharray="2 3" '
             f'opacity=".7"></path>')
    o.append(f'<g fill="{GOLD}" stroke="{INK}" stroke-width=".9">{"".join(bars)}</g>')
    xs = [xc(UNITS[u][2]) for u in counts]
    return o, min(xs) - bw / 2, max(xs) + bw / 2


def axes() -> list[str]:
    top = yq(1) - 22
    return [f'<path d="M{X1} {YB} H1312 M{X0} {YB} V{f(top)}" stroke="{INK}" stroke-width="1.5" fill="none"></path>',
            f'<g font-family="Hanken Grotesk" font-style="italic" font-size="14" fill="{INK}">'
            f'<text x="{X0 + 8}" y="{f(top + 6)}">capacity, cheapest first</text>'
            f'<text x="1312" y="{YB + 21}" text-anchor="end">price</text></g>']


def pc() -> str:
    carry, xs_clear = carry_and_clear()
    price, h0, h1 = panel_price(xs_clear)
    pats = pat_defs("pc") + (f'<pattern id="pc-res" width="7" height="7" patternUnits="userSpaceOnUse">'
                             f'<path d="M0 7 L7 0" stroke="{OLIVE}" stroke-width=".8"></path></pattern>')
    g = [f"<defs>{pats}</defs>"] + panel_day() + panel_stack() + carry + price + axes()
    aria = ("How the price forecast is assembled, in three steps on one baseline. Left: a day of demand, "
            "4 August 2026, the median day-ahead forecast peaking at 28.1 GW at 20:00, with wind and solar drawn as "
            "bands carved out of it; what is left is residual demand. Middle: the residual demand at the 20:00 "
            "peak, as a band of repeated draws, runs straight across onto a merit-order supply stack drawn on its "
            "side, capacity rising from biomass and nuclear through a long run of CCGT units to coal and OCGT, "
            "price running right. Each draw stops where it meets the edge of the stack. Right: each crossing drops "
            "to the price axis, where many draws build a narrow price distribution.")
    svg = (f'<svg width="1320" height="{DH}" viewBox="0 0 1320 {DH}" role="img" aria-label="{aria}">'
           + "".join(g) + "</svg>")
    LT = YB + 42

    def lab(left: float, width: float, html: str) -> str:
        return f'<div class="pc-l" style="left: {f(left)}px; top: {LT}px; width: {f(width)}px">{html}</div>'

    smp_x = round(h0) - 2
    labels = [
        lab(80, 252, f'<p class="pc-t">Day-ahead demand</p><p class="pc-id">{MID["demand"]}</p>'
                     '<p class="pc-d">Top line: the median forecast for 4 August 2026 in GW, issued at noon the '
                     f'day before (target: Elexon INDO). {CASE}</p>'),
        lab(356, 210, f'<p class="pc-t">Wind generation</p><p class="pc-id">{MID["wind"]}</p>'
                      f'<p class="pc-t pc-t2">Solar generation</p><p class="pc-id">{MID["solar"]}</p>'),
        lab(X0, smp_x - X0 - 28, f'<p class="pc-t">Merit-order supply curve</p><p class="pc-id">{MID["stack"]}</p>'
                                 f'<p class="pc-d">{gen.BUILD}: GB plant in merit order, cheapest first.</p>'),
        lab(smp_x, 1312 - smp_x, f'<p class="pc-t">Fundamentals SMP forecaster</p><p class="pc-id">{MID["smp"]}</p>'
                                 '<p class="pc-d">Monte Carlo draws of residual demand, each cleared against the '
                                 'curve, build a price distribution. Backtested against ENTSO-E day-ahead prices.</p>'),
    ]
    head = (f'<div class="blk why pc-head" style="top: {Y["p_head"]}px; left: 80px; width: 660px">'
            f'<h2 id="why-h">{WHY_H2}</h2><p class="intro">{INTRO}</p><p class="aim">{AIM}</p></div>')
    return (f'<section class="pc" aria-labelledby="why-h">{head}'
            f'<div class="blk pc-draw" style="top: {DT}px; left: 0px; width: 1320px; height: {DH}px">'
            f'{svg}{"".join(labels)}</div></section>')


PC_CSS = """.pc-head .intro{margin:0 0 14px;font-size:20px;line-height:1.5;color:#1C2B22;max-width:480px;text-wrap:pretty}
.pc-head .aim{margin:0;font-size:16px;line-height:1.6;font-weight:600;color:#1C2B22;max-width:440px;text-wrap:balance}
.pc-draw svg{display:block}
.pc-l{position:absolute}
.pc-t{margin:0;font-family:"Bricolage Grotesque",sans-serif;font-size:19px;font-weight:700;font-stretch:90%;line-height:1.15;letter-spacing:-.005em;color:#1C2B22}
.pc-t2{margin-top:12px}
.pc-id{margin:2px 0 0;font:400 13px/1.4 "Red Hat Mono",monospace;color:#155A6E}
.pc-d{margin:5px 0 0;font-size:14px;line-height:1.45;color:#3F4A3B}
.pc-d code{font-size:12.5px;color:#1C2B22}
.pc .more{font-weight:600;color:#1C2B22;text-decoration-color:#66793B}
"""

gen.PURPOSE["C"] = pc
gen.PCSS["C"] = PC_CSS

if __name__ == "__main__":
    (HERE / "static").mkdir(exist_ok=True)
    for name, v in (("R3-v5-C", "C"), ("_ref-P1", "P1")):
        out = page(v)
        body_only = out.split("<script type=\"text/x-dc\"")[0]
        assert "{{" not in body_only and "}}" not in body_only, "template-hole syntax in markup"
        assert "/>" not in re.sub(r"<(meta|link|br)[^>]*>", "", body_only), "self-closing tag"
        (HERE / f"{name}.dc.html").write_text(out, encoding="utf-8")
        (HERE / "static" / f"{name}.html").write_text(static(out), encoding="utf-8")
    print("H =", gen.H, "TS =", TS, "RS = %.2f" % RS, "D* = %.3f" % D[TS],
          "q* = %.3f" % (RS / CAPG), "stack top page y =", DT + yq(1))
