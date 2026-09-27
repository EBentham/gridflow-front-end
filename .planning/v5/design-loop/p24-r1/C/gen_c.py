"""Phase 24 round 1, designer C, "The plate". Emits C-<slug>.dc.html + static/C-<slug>.html for four specimens.

Every number drawn or printed comes from ../pack/specimens.json or ../pack/SPECIMENS.md. Text blocks flow (CSS grid);
only the SVG plates and the strata edges are drawn. Root height per board is measured in a browser and written to
HEIGHTS below (the root and $preview must match).
"""
from __future__ import annotations

import datetime as dt
import html
import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
PACK = json.loads((HERE.parent / "pack" / "specimens.json").read_text(encoding="utf-8"))
SPEC = {s["id"]: s for s in PACK["specimens"]}

PETROL, HORIZON, CHART, OLIVE = "#155A6E", "#3E8C97", "#AFC64E", "#66793B"
INK, INK2, MUTED, DAY = "#1C2B22", "#3F4A3B", "#5d6a55", "#F6F4EC"
CLAY, KHAKI, BRONZE = "#C77E3C", "#A39A6A", "#A5713C"
T_TOP, T_BRONZE, T_SILVER, T_GOLD = "#ECE8DA", "#E2CDB3", "#DCE2DF", "#E9DDAF"
W = 1440

HEIGHTS = {"fuelhh": 3900, "system-prices": 3900, "physical-flows": 3900, "bmunits-reference": 3900}
if (HERE / "heights.json").exists():
    HEIGHTS.update(json.loads((HERE / "heights.json").read_text(encoding="utf-8")))


def f(v: float) -> str:
    return f"{v:.1f}".rstrip("0").rstrip(".") if abs(v - round(v)) > 1e-9 else str(int(round(v)))


def esc(s: str) -> str:
    return html.escape(s, quote=False)


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


def wave(y0: float, amp: float, seed: float, step: int = 120) -> list[tuple[float, float]]:
    return [(x, y0 + amp * math.sin(x / 210 + seed) + amp * 0.45 * math.sin(x / 73 + seed * 2.3))
            for x in range(-40, W + step + 41, step)]


# ================================================================ patterns (the site's hatches + the plate's)
def patterns(p: str) -> str:
    """Pattern defs with a per-svg prefix, so every inline svg is self-contained."""
    return (
        f'<pattern id="{p}-soil" width="23" height="17" patternUnits="userSpaceOnUse"><circle cx="4" cy="5" r=".9" fill="{KHAKI}"></circle><circle cx="15" cy="12" r="1.1" fill="{KHAKI}"></circle><path d="M17 3 h3" stroke="{KHAKI}" stroke-width=".9"></path></pattern>'
        f'<pattern id="{p}-brick" width="24" height="12" patternUnits="userSpaceOnUse"><path d="M0 11.5 H24 M12 0 V6 M0 6 H24 M0 6 V12" stroke="#7C5530" stroke-width=".8" fill="none"></path></pattern>'
        f'<pattern id="{p}-diag" width="8" height="8" patternUnits="userSpaceOnUse"><path d="M0 8 L8 0" stroke="#5E6E6B" stroke-width=".8"></path></pattern>'
        f'<pattern id="{p}-stip" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="2" cy="3" r="1" fill="#8A6F1E"></circle><circle cx="6.5" cy="7.5" r=".8" fill="#8A6F1E"></circle></pattern>'
        f'<pattern id="{p}-granite" width="46" height="40" patternUnits="userSpaceOnUse"><path d="M8 8 h8 M12 4 v8 M30 26 h8 M34 22 v8 M20 34 h6 M23 31 v6 M40 6 h5 M42.5 3.5 v5" stroke="{HORIZON}" stroke-width="1.1"></path></pattern>'
    )


def plate_patterns(p: str) -> str:
    """Textures for the plate bands. The homepage core-sample textures for the named fuels, plus one hatch per
    code the palette does not name (all on khaki): ripple = hydro, diagonal = pumped storage, stipple = coal/oil."""
    return (
        f'<pattern id="{p}-wind" width="14" height="6" patternUnits="userSpaceOnUse"><path d="M0 3 h8" stroke="{DAY}" stroke-width=".8"></path></pattern>'
        f'<pattern id="{p}-gas" width="7" height="7" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r=".9" fill="{INK}"></circle><circle cx="5.5" cy="5.5" r=".7" fill="{INK}"></circle></pattern>'
        f'<pattern id="{p}-imp" width="7" height="7" patternUnits="userSpaceOnUse"><path d="M0 7 L7 0" stroke="{DAY}" stroke-width=".8"></path></pattern>'
        f'<pattern id="{p}-bio" width="10" height="8" patternUnits="userSpaceOnUse"><path d="M1 2 l3 1 M6 6 l3 -1" stroke="{INK}" stroke-width=".8"></path></pattern>'
        f'<pattern id="{p}-hyd" width="12" height="5" patternUnits="userSpaceOnUse"><path d="M0 2.5 q3 -2 6 0 t6 0" stroke="{DAY}" stroke-width=".9" fill="none"></path></pattern>'
        f'<pattern id="{p}-ps" width="6" height="6" patternUnits="userSpaceOnUse"><path d="M0 6 L6 0 M-1 1 L1 -1 M5 7 L7 5" stroke="{INK}" stroke-width=".9"></path></pattern>'
        f'<pattern id="{p}-coal" width="5" height="5" patternUnits="userSpaceOnUse"><circle cx="2.5" cy="2.5" r=".9" fill="{INK}"></circle></pattern>'
        f'<pattern id="{p}-exit" width="7" height="7" patternUnits="userSpaceOnUse"><path d="M0 7 L7 0 M-1 1 L1 -1 M6 8 L8 6" stroke="{DAY}" stroke-width="1.3"></path></pattern>'
        f'<pattern id="{p}-null" width="10" height="10" patternUnits="userSpaceOnUse"><rect x="1" y="1" width="7" height="7" fill="none" stroke="{INK}" stroke-width=".9" opacity=".42"></rect></pattern>'
    )


# band styles: fill, texture id suffix, texture opacity, label colour when a label sits inside the band
BAND = {
    "nuclear": (PETROL, None, "", DAY),
    "biomass": (BRONZE, None, "", INK),
    "hydro": (KHAKI, "hyd", ".9", INK),
    "coaloil": (KHAKI, "coal", ".55", INK),
    "gas": (CLAY, None, "", INK),
    "other": (KHAKI, None, "", INK),
    "ps": (KHAKI, "ps", ".42", INK),
    "imports": (OLIVE, None, "", DAY),
    "wind": (HORIZON, None, "", INK),
    "exports": (OLIVE, None, "", DAY),
    "psneg": (KHAKI, "ps", ".42", INK),
}

LAB = 'font-family="Hanken Grotesk" font-style="italic" font-size="14"'
NUM = 'font-family="Hanken Grotesk" font-size="13"'
SVG_W = 1280
X0, PW = 64, 1000          # plot left and width inside the plate svg; x 1064..1280 is the label column
LX = 1086                  # label column text x


def band_fill(p: str, key: str, d: str) -> str:
    fill, tex, op, _ = BAND[key]
    s = f'<path d="{d}" fill="{fill}"></path>'
    if tex:
        s += f'<path d="{d}" fill="url(#{p}-{tex})" opacity="{op}"></path>'
    return s


def area(xs: list[float], lo: list[float], hi: list[float]) -> str:
    top = " L".join(f"{f(x)} {f(y)}" for x, y in zip(xs, hi))
    bot = " L".join(f"{f(x)} {f(y)}" for x, y in zip(reversed(xs), reversed(lo)))
    return f"M{top} L{bot} Z"


def polyline(xs: list[float], ys: list[float]) -> str:
    return "M" + " L".join(f"{f(x)} {f(y)}" for x, y in zip(xs, ys))


def spread(items: list[list], lo: float, hi: float, gap: float = 17) -> None:
    """Push label y positions (item[0]) apart so no two are closer than gap, inside [lo, hi]."""
    items.sort(key=lambda it: it[0])
    for _ in range(60):
        moved = False
        for a, b in zip(items, items[1:]):
            if b[0] - a[0] < gap:
                m = (b[0] - a[0] - gap) / 2
                a[0] += m
                b[0] -= m
                moved = True
        for it in items:
            it[0] = min(max(it[0], lo), hi)
        if not moved:
            break


def leader(x1: float, y1: float, y2: float) -> str:
    """From a point on a band at the plot's right edge, out to a label in the column."""
    return f"M{f(x1)} {f(y1)} H{f(X0 + PW + 6)} L{f(LX - 6)} {f(y2)}"


def dtp(s: str) -> dt.datetime:
    return dt.datetime.fromisoformat(s)


def day_axis(ts: list[dt.datetime], xat, y: float, label_days: bool = True) -> list[str]:
    """Ticks at 00:00 UTC, the day's name centred in its span."""
    out = []
    t0, t1 = ts[0], ts[-1] + (ts[1] - ts[0])
    d = dt.datetime(t0.year, t0.month, t0.day, tzinfo=t0.tzinfo)
    ticks = []
    while d <= t1:
        if d >= t0:
            ticks.append(d)
        d += dt.timedelta(days=1)
    tick = " ".join(f"M{f(xat(t))} {f(y)} v7" for t in ticks)
    out.append(f'<path d="{tick}" stroke="{INK}" stroke-width="1.2"></path>')
    if label_days:
        spans = [(max(t0, a), min(t1, a + dt.timedelta(days=1))) for a in [ticks[0] - dt.timedelta(days=1)] + ticks]
        labs = []
        for a, b in spans:
            if (b - a).total_seconds() < 12 * 3600:
                continue
            day = a if a.hour == 0 else b - dt.timedelta(hours=1)
            labs.append(f'<text x="{f((xat(a) + xat(b)) / 2)}" y="{f(y + 24)}" text-anchor="middle">'
                        f'{day.strftime("%a")} {day.day} {day.strftime("%b")}</text>')
        out.append(f'<g {NUM} font-size="13.5" fill="{INK2}">{"".join(labs)}</g>')
    return out


def y_axis(ticks: list[float], ymap, label, unit: str,
           fmt=lambda v: f"{v:,.0f}".replace("-", "−")) -> list[str]:
    out = [f'<path d="{" ".join(f"M{X0 - 6} {f(ymap(v))} H{X0}" for v in ticks)}" stroke="{INK}" stroke-width="1.2"></path>',
           f'<path d="{" ".join(f"M{X0} {f(ymap(v))} H{X0 + PW}" for v in ticks if v != 0)}" stroke="{INK}" '
           f'stroke-width=".8" stroke-dasharray="1 5" opacity=".45"></path>']
    labs = "".join(f'<text x="{X0 - 10}" y="{f(ymap(v) + 4.5)}" text-anchor="end">{label(v) if label else fmt(v)}</text>'
                   for v in ticks)
    out.append(f'<g {NUM} font-size="13" fill="{INK2}">{labs}</g>')
    out.append(f'<text x="{X0 - 10}" y="{f(ymap(ticks[-1]) - 16)}" text-anchor="end" {NUM} font-size="13" '
               f'font-weight="600" fill="{INK}">{unit}</text>')
    return out


# ================================================================ plate 1: FUELHH, diverging stack
INT_CODES = ["INTELEC", "INTEW", "INTFR", "INTGRNL", "INTIFA2", "INTIRL", "INTNED", "INTNEM", "INTNSL", "INTVKL"]
POS = [("nuclear", ["NUCLEAR"]), ("biomass", ["BIOMASS"]), ("hydro", ["NPSHYD"]), ("coaloil", ["COAL", "OIL"]),
       ("gas", ["CCGT", "OCGT"]), ("other", ["OTHER"]), ("ps", ["PS"]), ("imports", INT_CODES), ("wind", ["WIND"])]
NEG = [("exports", INT_CODES), ("psneg", ["PS"])]


def plate_fuelhh() -> tuple[str, str]:
    c = SPEC["elexon/fuelhh"]["chart"]
    pf, hrs = c["per_fuel_mw"], [dtp(h) for h in c["hours_utc"]]
    n = len(hrs)
    PT, PH, VMAX, VMIN = 46, 470, 36000, -11000
    ym = lambda v: PT + (VMAX - v) * PH / (VMAX - VMIN)  # noqa: E731
    xs = [X0 + i * PW / (n - 1) for i in range(n)]
    xat = lambda t: X0 + (t - hrs[0]).total_seconds() / 3600 * PW / (n - 1)  # noqa: E731
    p = "pf"
    lows: dict[str, list[float]] = {}
    highs: dict[str, list[float]] = {}
    base = [0.0] * n
    for key, codes in POS:
        v = [sum(max(pf[cd][i], 0) for cd in codes) for i in range(n)]
        lows[key] = base[:]
        base = [b + x for b, x in zip(base, v)]
        highs[key] = base[:]
    top = base[:]
    nb = [0.0] * n
    for key, codes in NEG:
        v = [sum(min(pf[cd][i], 0) for cd in codes) for i in range(n)]
        highs[key] = nb[:]
        nb = [b + x for b, x in zip(nb, v)]
        lows[key] = nb[:]
    bottom = nb[:]

    g = [f'<defs>{plate_patterns(p)}</defs>']
    g += y_axis([-5000, 0, 10000, 20000, 30000], ym, None, "MW")
    for key, _ in POS + NEG:
        lo = [ym(v) for v in lows[key]]
        hi = [ym(v) for v in highs[key]]
        g.append(band_fill(p, key, area(xs, lo, hi)))
    # internal contacts, then the outline of the whole stack and the zero line
    seams = (" ".join(polyline(xs, [ym(v) for v in highs[k]]) for k, _ in POS[:-1]) + " "
             + polyline(xs, [ym(v) for v in highs["psneg"]]))
    g.append(f'<path d="{seams}" stroke="{INK}" stroke-width=".6" fill="none" opacity=".5" stroke-linejoin="round"></path>')
    g.append(f'<path d="{polyline(xs, [ym(v) for v in top])} {polyline(xs, [ym(v) for v in bottom])}" stroke="{INK}" '
             f'stroke-width="1.5" fill="none" stroke-linejoin="round"></path>')
    g.append(f'<path d="M{X0} {f(ym(0))} H{X0 + PW}" stroke="{INK}" stroke-width="1.5"></path>')
    g.append(f'<path d="M{X0} {PT - 6} V{PT + PH}" stroke="{INK}" stroke-width="1.5"></path>')
    ab = PT + PH
    g.append(f'<path d="M{X0} {ab} H{X0 + PW}" stroke="{INK}" stroke-width="1.2"></path>')
    g += day_axis(hrs, xat, ab)

    # in-band labels only where the fill carries 14 px text at >= 4.5:1 (petrol with daylight, clay with ink)
    def best(key: str, lo_i: int, hi_i: int, half: int = 5) -> int:
        bi, bt = lo_i, -1.0
        for i in range(lo_i + half, hi_i - half):
            th = min((highs[key][j] - lows[key][j]) for j in range(i - half, i + half + 1))
            if th > bt:
                bi, bt = i, th
        return bi

    labs = []
    for key, text, rng in [("nuclear", "nuclear", (14, 60)), ("gas", "gas, CCGT and OCGT", (60, 130))]:
        i = best(key, *rng, half=7)
        yy = ym((lows[key][i] + highs[key][i]) / 2) + 5
        labs.append(f'<text x="{f(xs[i])}" y="{f(yy)}" text-anchor="middle" fill="{BAND[key][3]}">{text}</text>')
    # wind is the top band, so its label sits on the topsoil just above its upper edge
    wi, wbest = 0, 1e9
    for i in range(20, n - 60):
        win = range(i - 4, i + 5)
        if min(highs["wind"][j] - lows["wind"][j] for j in win) < 3500:
            continue
        t = max(top[j] for j in win)
        if t < wbest:
            wi, wbest = i, t
    labs.append(f'<text x="{f(xs[wi])}" y="{f(ym(wbest) - 9)}" text-anchor="middle">wind</text>')
    # the two bands below zero are labelled on the topsoil under the stack
    ei = min(range(n), key=lambda i: bottom[i])
    labs.append(f'<text x="{f(xs[ei] + 8)}" y="{f(ym(bottom[ei]) + 21)}">interconnector exports</text>')
    far = [i for i in range(8, n - 8) if abs(xs[i] - xs[ei]) > 420]
    pi = max(far, key=lambda i: highs["psneg"][i] - lows["psneg"][i])
    pmid = ym((highs["psneg"][pi] + lows["psneg"][pi]) / 2)
    labs.append(f'<text x="{f(xs[pi])}" y="{f(ym(bottom[pi]) + 26)}" text-anchor="middle">'
                f'pumped storage, where negative</text>')
    g.append(f'<path d="M{f(xs[pi])} {f(pmid)} V{f(ym(bottom[pi]) + 11)}" stroke="{INK}" stroke-width="1"></path>'
             f'<circle cx="{f(xs[pi])}" cy="{f(pmid)}" r="2.2" fill="{INK}"></circle>')
    g.append(f'<g {LAB} fill="{INK}">{"".join(labs)}</g>')

    # wind's highest and lowest hours, called out on one line above the plate
    wv = c["palette_groups_mw"]["wind"]
    imax, imin = wv.index(max(wv)), wv.index(min(wv))
    ann, dots = [], []
    for idx, words, yfrom in [(imax, "wind at its week high", ym(top[imax])),
                              (imin, "at its week low", ym((lows["wind"][imin] + highs["wind"][imin]) / 2))]:
        x = xs[idx]
        dots.append(f'<circle cx="{f(x + (3 if idx == 0 else 0))}" cy="{f(yfrom + (4 if idx == 0 else 0))}" r="2.4" '
                    f'fill="{INK}"></circle>')
        lead = (f"M{f(x + 3)} {f(yfrom + 4)} L{f(x + 24)} {PT - 22} H{f(x + 32)}" if idx == 0
                else f"M{f(x)} {f(yfrom)} V{PT - 22} H{f(x + 8)}")
        tx = x + (36 if idx == 0 else 12)
        ann.append((lead, f'<text x="{f(tx)}" y="{PT - 18}">{words}, {wv[idx]:,.0f} MW '
                          f'({hrs[idx].day} Sep {hrs[idx].strftime("%H:%M")} UTC)</text>'))
    g.append(f'<path d="{" ".join(a for a, _ in ann)}" stroke="{INK}" stroke-width="1" fill="none"></path>')
    g.append("".join(dots))
    g.append(f'<g {LAB} fill="{INK}">{"".join(t for _, t in ann)}</g>')

    # the label column: bands too thin, or too dark for 14 px text, keyed by leaders from the last hour
    col = []
    for key, texts in [("imports", ["interconnector imports"]), ("ps", ["pumped storage, PS"]),
                       ("other", ["other (vendor code", "OTHER)"]), ("coaloil", ["coal, at most 66 MW,", "and oil, 0 MW"]),
                       ("hydro", ["hydro, NPSHYD"]), ("biomass", ["biomass"])]:
        yb = ym((lows[key][-1] + highs[key][-1]) / 2)
        col.append([yb, key, texts, yb])
    col.sort(key=lambda it: it[0])
    for _ in range(80):
        for a, b in zip(col, col[1:]):
            need = 26 + 18 * (len(a[2]) - 1)
            if b[0] - a[0] < need:
                m = (need - (b[0] - a[0])) / 2
                a[0] -= m
                b[0] += m
    lines, texts = [], []
    xe = xs[-1]
    for y2, key, words, yb in col:
        lines.append(f"M{f(xe)} {f(yb)} H{f(xe + 6)} L{f(LX - 6)} {f(y2 - 6)}")
        sw = (f'<rect x="{LX}" y="{f(y2 - 13)}" width="12" height="12" fill="{BAND[key][0]}" stroke="{INK}" '
              f'stroke-width=".8"></rect>')
        if BAND[key][1]:
            sw += (f'<rect x="{LX}" y="{f(y2 - 13)}" width="12" height="12" fill="url(#{p}-{BAND[key][1]})" '
                   f'opacity="{BAND[key][2]}"></rect>')
        tl = "".join(f'<text x="{LX + 18}" y="{f(y2 - 2 + 18 * k)}" {LAB}>{w}</text>' for k, w in enumerate(words))
        texts.append(sw + tl)
    g.append(f'<path d="{" ".join(lines)}" stroke="{INK}" stroke-width=".9" fill="none" opacity=".75"></path>')
    g.append(f'<g fill="{INK}">{"".join(texts)}</g>')
    g.append(f'<text x="{X0 + PW}" y="{ab + 48}" text-anchor="end" {NUM} fill="{INK2}">hours in UTC</text>')

    H = ab + 56
    aria = ("Stacked area chart of GB generation by fuel code from elexon/fuelhh silver, hourly means in MW, settlement "
            "dates 20 to 26 September 2026. Above zero, from the bottom: nuclear, steady near 3,300 to 4,000 MW; "
            "biomass; hydro; coal and oil, near zero; gas, which swings between about 2,100 and 15,900 MW; the "
            "vendor's OTHER; pumped storage where positive; interconnector imports; and wind on top, from 16,011 MW "
            "in the first hour down to 1,326 MW on 22 September. Below zero: interconnector exports and pumped "
            "storage where negative, down to about 7,100 MW in all.")
    svg = (f'<svg class="plate-svg" width="{SVG_W}" height="{H}" viewBox="0 0 {SVG_W} {H}" role="img" '
           f'aria-label="{aria}">' + "".join(g) + "</svg>")
    return svg, aria


# ================================================================ plate 2: system prices, a line through zero
def plate_prices() -> tuple[str, str]:
    c = SPEC["elexon/system_prices"]["chart"]
    ts = [dtp(t) for t in c["t_utc"]]
    v = c["ssp_gbp_per_mwh"]
    n = len(v)
    PT, PH, VMAX, VMIN = 46, 380, 625, -75
    ym = lambda y: PT + (VMAX - y) * PH / (VMAX - VMIN)  # noqa: E731
    xs = [X0 + i * PW / (n - 1) for i in range(n)]
    xat = lambda t: X0 + (t - ts[0]).total_seconds() / 1800 * PW / (n - 1)  # noqa: E731
    p = "sp"
    g = [f'<defs>{plate_patterns(p)}</defs>']
    g += y_axis([0, 100, 200, 300, 400, 500, 600], ym, None, "£/MWh")
    z = ym(0)
    # below-zero stretches, closed exactly at the zero crossings
    polys, run = [], []
    for i in range(n):
        if v[i] < 0:
            if not run:
                if i > 0:
                    xc = xs[i - 1] + (xs[i] - xs[i - 1]) * v[i - 1] / (v[i - 1] - v[i])
                    run.append((xc, z))
                else:
                    run.append((xs[0], z))
            run.append((xs[i], ym(v[i])))
            nxt = v[i + 1] if i + 1 < n else None
            if nxt is None or nxt >= 0:
                if nxt is not None:
                    xc = xs[i] + (xs[i + 1] - xs[i]) * v[i] / (v[i] - nxt)
                    run.append((xc, z))
                else:
                    run.append((xs[i], z))
                polys.append(run)
                run = []
    g.append(f'<path d="{" ".join("M" + " L".join(f"{f(a)} {f(b)}" for a, b in r) + " Z" for r in polys)}" '
             f'fill="{CLAY}"></path>')
    g.append(f'<path d="M{X0} {f(z)} H{X0 + PW}" stroke="{INK}" stroke-width="1.5"></path>')
    g.append(f'<path d="{polyline(xs, [ym(y) for y in v])}" stroke="{INK}" stroke-width="1.6" fill="none" '
             f'stroke-linejoin="round"></path>')
    g.append(f'<path d="M{X0} {PT - 6} V{PT + PH}" stroke="{INK}" stroke-width="1.5"></path>')
    ab = PT + PH
    g.append(f'<path d="M{X0} {ab} H{X0 + PW}" stroke="{INK}" stroke-width="1.2"></path>')
    g += day_axis(ts, xat, ab)
    # the -50 tick sits on the axis too, since the low is exactly there
    g.append(f'<path d="M{X0 - 6} {f(ym(-50))} H{X0}" stroke="{INK}" stroke-width="1.2"></path>'
             f'<text x="{X0 - 10}" y="{f(ym(-50) + 4.5)}" text-anchor="end" {NUM} fill="{INK2}">−50</text>')

    imx, imn = v.index(max(v)), v.index(min(v))
    ann = []
    xa, ya = xs[imx], ym(v[imx])
    ann.append((f"M{f(xa - 4)} {f(ya)} H{f(xa - 36)}",
                f'<text x="{f(xa - 42)}" y="{f(ya + 5)}" text-anchor="end">the window’s high, '
                f'{v[imx]:,.2f} £/MWh at {ts[imx].strftime("%H:%M")} UTC on {ts[imx].day} Sep</text>'))
    xb, yb = xs[imn], ym(v[imn])
    ann.append((f"M{f(xb)} {f(yb + 4)} V{f(ab - 30)}",
                f'<text x="{f(xb + 6)}" y="{f(ab - 16)}">its low, −{abs(v[imn]):.2f} £/MWh at '
                f'{ts[imn].strftime("%H:%M")} UTC on {ts[imn].day} Sep</text>'))
    g.append(f'<path d="{" ".join(a for a, _ in ann)}" stroke="{INK}" stroke-width="1" fill="none"></path>')
    g.append(f'<circle cx="{f(xa)}" cy="{f(ya)}" r="2.6" fill="{INK}"></circle>'
             f'<circle cx="{f(xb)}" cy="{f(yb)}" r="2.6" fill="{INK}"></circle>')
    g.append(f'<g {LAB} fill="{INK}">{"".join(t for _, t in ann)}</g>')
    # label column: the line itself, and the clay
    yl = ym(v[-1])
    neg = c["negatives"]["count"]
    g.append(f'<path d="M{f(xs[-1] + 3)} {f(yl)} L{LX - 6} {f(yl)} M{X0 + PW + 4} {f(z + 12)} L{LX - 6} {f(z + 26)}" '
             f'stroke="{INK}" stroke-width=".9" fill="none" opacity=".75"></path>')
    g.append(f'<g {LAB} fill="{INK}"><text x="{LX}" y="{f(yl - 3)}">system sell price</text>'
             f'<text x="{LX}" y="{f(yl + 15)}">(the buy price is</text><text x="{LX}" y="{f(yl + 33)}">identical)</text>'
             f'<text x="{LX + 18}" y="{f(z + 30)}">below zero in</text>'
             f'<text x="{LX}" y="{f(z + 48)}">{neg} of {n} half-hours</text></g>'
             f'<rect x="{LX}" y="{f(z + 19)}" width="12" height="12" fill="{CLAY}" stroke="{INK}" stroke-width=".8"></rect>')
    g.append(f'<text x="{X0 + PW}" y="{ab + 48}" text-anchor="end" {NUM} fill="{INK2}">half-hours in UTC</text>')
    H = ab + 56
    aria = ("Line chart of the GB system sell price from elexon/system_prices silver, latest vintage per period, "
            "in pounds per megawatt-hour, 192 half-hours over settlement dates 19 to 22 September 2026. The price "
            f"dips below zero in {neg} half-hours, shaded, reaching its low of minus 50.00 at 13:30 UTC on 20 "
            "September, and spikes to its high of 594.00 at 20:00 UTC on 22 September. The system buy price is "
            "identical in every period.")
    return (f'<svg class="plate-svg" width="{SVG_W}" height="{H}" viewBox="0 0 {SVG_W} {H}" role="img" '
            f'aria-label="{aria}">' + "".join(g) + "</svg>"), aria


# ================================================================ plate 3: ENTSOG, sparse daily bars with an unconformity
def plate_flows() -> tuple[str, str]:
    c = SPEC["entsog/physical_flows"]["chart"]
    bac = c["series"][0]
    fer = c["series"][1]
    assert bac["point_label"].startswith("Bacton") and fer["point_label"].startswith("St")
    days = [dtp(pt["timestamp_utc"]) for pt in fer["points"]]
    vb = [pt["flow_gwh_per_day"] for pt in bac["points"]]
    vf = [pt["flow_gwh_per_day"] for pt in fer["points"]]
    n = len(days)
    PT, PH, VMAX = 46, 440, 650
    ym = lambda y: PT + (VMAX - y) * PH / VMAX  # noqa: E731
    GAPW = 150
    k_break = next(i for i in range(1, n) if (days[i] - days[i - 1]).days > 1)
    slot = (PW - GAPW) / n
    def xslot(i: int) -> float:
        return X0 + i * slot + (GAPW if i >= k_break else 0)
    p = "ef"
    g = [f'<defs>{plate_patterns(p)}</defs>']
    g += y_axis([0, 100, 200, 300, 400, 500, 600], ym, None, "GWh/d")
    bw, gap = 22, 4
    ab = PT + PH
    bars, vals, zeros = [], [], []
    for i in range(n):
        cx = xslot(i) + slot / 2
        for val, dx, key in [(vf[i], -(bw + gap / 2), "fer"), (vb[i], gap / 2, "bac")]:
            x = cx + dx
            if val > 0:
                d = f"M{f(x)} {f(ab)} V{f(ym(val))} H{f(x + bw)} V{f(ab)} Z"
                bars.append(f'<path d="{d}" fill="{CLAY}" stroke="{INK}" stroke-width="1.2"></path>')
                if key == "bac":
                    bars.append(f'<path d="{d}" fill="url(#{p}-exit)" opacity=".75"></path>')
            else:
                zeros.append(f"M{f(x)} {f(ab - 1.5)} H{f(x + bw)}")
            vals.append(f'<text x="{f(x + bw / 2)}" y="{f(ym(val) - 7)}" text-anchor="middle">{val:,.0f}</text>')
    g += bars
    g.append(f'<path d="{" ".join(zeros)}" stroke="{INK}" stroke-width="3" stroke-linecap="butt"></path>')
    g.append(f'<g {NUM} font-size="12.5" fill="{INK}">{"".join(vals)}</g>')
    # axes: the baseline breaks at the gap, with an unconformity drawn through the plot's full height
    xa, xb = xslot(k_break - 1) + slot + 18, xslot(k_break) - 18
    g.append(f'<path d="M{X0} {ab} H{f(xa)} M{f(xb)} {ab} H{X0 + PW} M{X0} {PT - 6} V{ab}" stroke="{INK}" '
             f'stroke-width="1.5" fill="none"></path>')
    def unconf(x: float, seed: float) -> str:
        pts = [(x + 4 * math.sin(y / 23 + seed) + 2.2 * math.sin(y / 9 + seed * 3), y) for y in range(PT - 10, ab + 17, 6)]
        return smooth(pts)
    g.append(f'<path d="{unconf(xa, 0.4)} {unconf(xb, 2.2)}" stroke="{INK}" stroke-width="1.4" fill="none"></path>')
    mid = (xa + xb) / 2
    gap_days = (days[k_break] - days[k_break - 1]).days - 1
    first_gap = days[k_break - 1] + dt.timedelta(days=1)
    last_gap = days[k_break] - dt.timedelta(days=1)
    g.append(f'<g {LAB} fill="{INK}" text-anchor="middle"><text x="{f(mid)}" y="{f(PT + 150)}">no rows in</text>'
             f'<text x="{f(mid)}" y="{f(PT + 168)}">local silver,</text>'
             f'<text x="{f(mid)}" y="{f(PT + 186)}">{first_gap.day} {first_gap.strftime("%b")} to {last_gap.day} '
             f'{last_gap.strftime("%b")}</text><text x="{f(mid)}" y="{f(PT + 204)}">({gap_days} gas days)</text></g>')
    # day labels under each pair; month under the first day of each block
    dl = []
    for i, d in enumerate(days):
        cx = xslot(i) + slot / 2
        dl.append(f'<text x="{f(cx)}" y="{ab + 22}" text-anchor="middle">{d.day}</text>')
    ml = (f'<text x="{f(xslot(0) + slot / 2)}" y="{ab + 42}" text-anchor="middle" font-weight="600">August</text>'
          f'<text x="{f(xslot(k_break) + slot / 2)}" y="{ab + 42}" text-anchor="middle" font-weight="600">September</text>')
    g.append(f'<g {NUM} font-size="13.5" fill="{INK2}">{"".join(dl)}{ml}</g>')
    g.append(f'<text x="{X0 + PW}" y="{ab + 42}" text-anchor="end" {NUM} fill="{INK2}">gas days</text>')
    # label column, keyed to the last pair
    cx = xslot(n - 1) + slot / 2
    yf, yb2 = ym(vf[-1]), ym(vb[-1])
    ks = [[yf + 60, "fer", yf, cx - bw / 2 - gap / 2], [yb2 + 40, "bac", yb2 + 40, cx + gap / 2 + bw / 2]]
    zi = [i for i in range(n) if vb[i] == 0]
    lines = (f"M{f(cx - gap / 2)} {f(yf + 30)} L{f(cx + bw + 20)} {f(yf + 30)} L{LX - 6} {f(ks[0][0] - 5)} "
             f"M{f(ks[1][3] + bw / 2)} {f(yb2 + 40)} L{LX - 6} {f(ks[1][0] - 5)}")
    g.append(f'<path d="{lines}" stroke="{INK}" stroke-width=".9" fill="none" opacity=".75"></path>')
    g.append(f'<rect x="{LX}" y="{f(ks[0][0] - 13)}" width="12" height="12" fill="{CLAY}" stroke="{INK}" stroke-width=".8"></rect>'
             f'<rect x="{LX}" y="{f(ks[1][0] - 13)}" width="12" height="12" fill="{CLAY}" stroke="{INK}" stroke-width=".8"></rect>'
             f'<rect x="{LX}" y="{f(ks[1][0] - 13)}" width="12" height="12" fill="url(#{p}-exit)" opacity=".75"></rect>')
    g.append(f'<g {LAB} fill="{INK}"><text x="{LX + 18}" y="{f(ks[0][0] - 2)}">St. Fergus, entry</text>'
             f'<text x="{LX + 18}" y="{f(ks[1][0] - 2)}">Bacton (IUK), exit:</text>'
             f'<text x="{LX + 18}" y="{f(ks[1][0] + 16)}">reported as 0.0 on</text>'
             f'<text x="{LX + 18}" y="{f(ks[1][0] + 34)}">each gas day, {days[zi[0]].day} to {days[zi[-1]].day} Sep</text></g>')
    H = ab + 56
    aria = ("Bar chart of daily physical gas flow in GWh per day from entsog/physical_flows silver, National Gas TSO, "
            "at two points: St. Fergus entry and Bacton (IUK) exit, for every gas day in local silver. The time axis "
            "is broken between 5 August and 13 September 2026, where silver has no rows. 1 to 5 August: St. Fergus "
            "406 to 434 except 350 on the 5th, Bacton exit 382 to 407. 13 to 21 September: St. Fergus rises from 473 "
            "to 595 on the 19th and ends at 559; Bacton exit is reported as 0.0 on each day from the 13th to the "
            "20th and 175 on the 21st.")
    return (f'<svg class="plate-svg" width="{SVG_W}" height="{H}" viewBox="0 0 {SVG_W} {H}" role="img" '
            f'aria-label="{aria}">' + "".join(g) + "</svg>"), aria


# ================================================================ plate 4: BM units, a census (one square per row)
def plate_units() -> tuple[str, str]:
    c = SPEC["elexon/bmunits_reference"]["chart"]
    cnt = {b["fuel_type"]: b["units"] for b in c["bars"]}
    ints = sum(v for k, v in cnt.items() if k.startswith("INT"))
    int_codes = sum(1 for k in cnt if k.startswith("INT"))
    rows = [("WIND", cnt["WIND"], "wind"), ("OTHER", cnt["OTHER"], "other"), ("CCGT", cnt["CCGT"], "gas"),
            ("OCGT", cnt["OCGT"], "gas"), ("NPSHYD", cnt["NPSHYD"], "hydro"), ("NUCLEAR", cnt["NUCLEAR"], "nuclear"),
            ("PS", cnt["PS"], "ps"), ("BIOMASS", cnt["BIOMASS"], "biomass"), ("COAL", cnt["COAL"], "coaloil"),
            (f"{int_codes} INT codes", ints, "imports")]
    typed = sum(r[1] for r in rows)
    null = cnt["(null)"]
    total = typed + null
    p = "bu"
    PER, PITCH, SQ = 88, 10, 8
    MX = 240                      # first mark x
    g = [f'<defs>{plate_patterns(p)}</defs>']
    y = 50
    marks, labels, counts = [], [], []
    for code, k, key in rows:
        fill = BAND[key][0]
        lines = math.ceil(k / PER)
        for m in range(k):
            x, yy = MX + (m % PER) * PITCH, y + (m // PER) * PITCH
            marks.append(f'<rect x="{x}" y="{yy}" width="{SQ}" height="{SQ}" fill="{fill}"></rect>')
        # the texture for codes the palette does not name, drawn once over the block
        if BAND[key][1] and key in ("hydro", "ps", "coaloil"):
            for ln in range(lines):
                w = min(PER, k - ln * PER) * PITCH - 2
                marks.append(f'<rect x="{MX}" y="{y + ln * PITCH}" width="{w}" height="{SQ}" '
                             f'fill="url(#{p}-{BAND[key][1]})" opacity="{BAND[key][2]}"></rect>')
        mono = 'font-family="Red Hat Mono" font-size="13.5"'
        labels.append(f'<text x="{MX - 72}" y="{y + 8}" text-anchor="end" {mono}>{code}</text>' if not code[0].isdigit()
                      else f'<text x="{MX - 72}" y="{y + 8}" text-anchor="end" {LAB} font-size="13.5">'
                           f'interconnectors, {code.split()[0]} codes</text>')
        counts.append(f'<text x="{MX - 14}" y="{y + 8}" text-anchor="end">{k:,}</text>')
        y += lines * PITCH + 8
    y_typed_end = y - 8
    y += 34
    y_null = y
    full = null // PER
    rest = null - full * PER
    marks.append(f'<rect x="{MX}" y="{y}" width="{PER * PITCH}" height="{full * PITCH}" fill="url(#{p}-null)"></rect>')
    marks.append(f'<rect x="{MX}" y="{y + full * PITCH}" width="{rest * PITCH}" height="{PITCH}" fill="url(#{p}-null)"></rect>')
    labels.append(f'<text x="{MX - 72}" y="{y + 8}" text-anchor="end" font-family="Red Hat Mono" font-size="13.5">null</text>')
    counts.append(f'<text x="{MX - 14}" y="{y + 8}" text-anchor="end">{null:,}</text>')
    y_end = y + (full + 1) * PITCH
    g += marks
    g.append(f'<g fill="{INK}">{"".join(labels)}</g>')
    g.append(f'<g {NUM} font-size="13.5" fill="{INK}">{"".join(counts)}</g>')
    # brackets: the typed rows and the untyped field, with hand notes
    bx = MX + PER * PITCH + 14
    g.append(f'<path d="M{bx} 50 h6 V{y_typed_end} h-6 M{bx} {y_null} h6 V{y_end - 2} h-6" stroke="{INK}" '
             f'stroke-width="1" fill="none"></path>')
    pct = round(100 * null / total)
    g.append(f'<g {LAB} fill="{INK}">'
             f'<text x="{bx + 14}" y="{f((50 + y_typed_end) / 2 - 4)}">{typed} units</text>'
             f'<text x="{bx + 14}" y="{f((50 + y_typed_end) / 2 + 14)}">with a fuel type</text>'
             f'<text x="{bx + 14}" y="{f((y_null + y_end) / 2 - 4)}">{null:,} units, {pct}%,</text>'
             f'<text x="{bx + 14}" y="{f((y_null + y_end) / 2 + 14)}">with none</text>'
             f'<text x="{MX}" y="30">each square is one row: one BM unit registration, {total:,} in the snapshot</text>'
             f'</g>')
    g.append(f'<g {NUM} font-size="13" font-weight="600" fill="{INK}"><text x="{MX - 72}" y="30" text-anchor="end">'
             f'fuel_type</text><text x="{MX - 14}" y="30" text-anchor="end">units</text></g>')
    g.append(f'<path d="M{MX - 234} 38 H{MX - 10}" stroke="{INK}" stroke-width="1.2"></path>')
    H = y_end + 18
    aria = (f"Census of the {total:,} rows in the elexon/bmunits_reference silver snapshot of 26 September 2026, one "
            f"square per BM unit, grouped by fuel_type. {typed} units have a fuel type: WIND 234, OTHER 92, CCGT 61, "
            f"OCGT 22, NPSHYD 22, NUCLEAR 16, PS 16, BIOMASS 15, COAL 10, and {ints} across {int_codes} interconnector "
            f"codes. The other {null:,}, drawn as a large field of hollow squares, have no fuel type.")
    return (f'<svg class="plate-svg" width="{SVG_W}" height="{H}" viewBox="0 0 {SVG_W} {H}" role="img" '
            f'aria-label="{aria}">' + "".join(g) + "</svg>"), aria
