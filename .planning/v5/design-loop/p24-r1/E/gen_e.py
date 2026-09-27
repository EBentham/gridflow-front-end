"""Phase 24 round 1, designer E: "The datasheet". Emits E-<slug>.dc.html (+ static copies) for four specimens.

One template: a petrol title band, then a single plate on the topsoil (figure left, key facts right, how to
get it across the foot), then the detail in a fixed order down a side-head rail: what it is, how it's used
(topsoil), schema, sample rows, caveats (the silver stratum), related datasets (the deep).

Every fact, number, code and column comes from pack/specimens.json or pack/SPECIMENS.md. The page is laid
out in normal flow and CSS grid (no absolutely positioned text), so the site build can reflow it; the root
height is measured in a browser and fed back through heights.json.
"""
from __future__ import annotations

import html
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE.parent
sys.path.insert(0, str(HERE))
from helpers import g  # noqa: E402  (the homepage generator's drawing helpers)

PACK = json.loads((OUT.parent / "pack" / "specimens.json").read_text(encoding="utf-8"))
SPEC = {s["id"]: s for s in PACK["specimens"]}
HEIGHTS_F = HERE / "heights.json"
HEIGHTS = json.loads(HEIGHTS_F.read_text(encoding="utf-8")) if HEIGHTS_F.exists() else {}

f, smooth = g.f, g.smooth
PETROL, HORIZON, CHART, OLIVE = g.PETROL, g.HORIZON, g.CHART, g.OLIVE
INK, DAY, CLAY, KHAKI, MUTED = g.INK, g.DAY, g.CLAY, g.KHAKI, g.MUTED
T_TOP, T_SILVER = g.T_TOP, g.T_SILVER
SOFT = g.SOFT
BIOMASS = "#A5713C"  # tokens.css --fuel-biomass (the homepage core sample's chartreuse is superseded)
MINUS = "−"
W = 1440


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def num(v: float, dp: int = 0) -> str:
    s = f"{abs(v):,.{dp}f}"
    return (MINUS if v < 0 else "") + s


# ============================================================ drawn pieces: the title band's land
def surface(x: float) -> float:
    return 104 + 3 * math.sin(x / 190 + .6) - 2 * math.sin(x / 83 + 1.3)


LAND_H = 114


def land(asset: str) -> str:
    """A low strip of the homepage landscape: ridge, three turbines, energised land, and the vendor's asset."""
    p = []
    far = [(640, 104), (760, 80), (880, 58), (1000, 44), (1120, 50), (1240, 34), (1360, 42), (1470, 36)]
    p.append(f'<path d="{smooth(far)} L1470 110 L640 110 Z" fill="{HORIZON}" opacity=".5"></path>')
    near = [(780, 104), (880, 84), (980, 70), (1070, 76), (1170, 64), (1280, 72), (1380, 60), (1470, 66)]
    p.append(f'<path d="{smooth(near)} L1470 110 L780 110 Z" fill="{HORIZON}"></path>')
    for i, (tx, ty, h) in enumerate([(880, 86, 40), (980, 72, 48), (1070, 78, 40)]):
        p.append(g.turbine(tx, ty, h, h * .5, ["sp2", "sp1", "sp3"][i], 40 * i + 10))
    field = [(-20, 92), (300, 88), (620, 94), (900, 92), (1200, 86), (1470, 88)]
    back = " ".join(f"L{f(x)} {f(surface(x))}" for x in range(1470, -21, -10))
    p.append(f'<path d="{smooth(field)} {back} Z" fill="{CHART}"></path>')
    if asset == "substation":
        px, ps = 1150, .42
        pb = surface(px)
        sx = 1236
        sb = surface(sx + 50)
        sub, ends = g.substation(sx, sb)
        p.append(f'<g stroke="{INK}" fill="none" stroke-linecap="round" stroke-width="1.3">{g.pylon(px, pb, ps)}</g>')
        wires = g.spans(g.tips(px, pb, ps, 1), ends, 5) + " " + g.spans(
            [(1040, pb - 26), (1040, pb - 37), (1040, pb - 45)], g.tips(px, pb, ps, -1), 4)
        p.append(f'<path d="{wires}" stroke="{INK}" stroke-width=".8" fill="none" opacity=".85"></path>')
        p.append(sub)
    else:  # gas terminal, for the gas vendors
        gx = 1200
        gb = surface(gx + 60)
        p.append(g.sc(g.gasterminal(gx, gb), gx, gb, 1.3))
    surf = [(x, surface(x)) for x in range(-20, 1471, 10)]
    sd = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in surf)
    root = sd + " " + " ".join(f"L{f(x)} {f(y + 8)}" for x, y in reversed(surf)) + " Z"
    p.append(f'<path d="{sd} L1470 {LAND_H + 2} L-20 {LAND_H + 2} Z" fill="{T_TOP}"></path>')
    p.append(f'<path d="{sd} L1470 {LAND_H + 2} L-20 {LAND_H + 2} Z" fill="url(#p-soil-l)" opacity=".5"></path>')
    p.append(f'<path d="{root}" fill="{OLIVE}"></path>')
    p.append(f'<path d="{sd}" stroke="{INK}" stroke-width="1.5" fill="none"></path>')
    defs = ('<defs><pattern id="p-soil-l" width="23" height="17" patternUnits="userSpaceOnUse">'
            f'<circle cx="4" cy="5" r=".9" fill="{KHAKI}"></circle><circle cx="15" cy="12" r="1.1" fill="{KHAKI}"></circle>'
            f'<path d="M17 3 h3" stroke="{KHAKI}" stroke-width=".9"></path></pattern></defs>')
    return (f'<svg class="land" width="{W}" height="{LAND_H}" viewBox="0 0 {W} {LAND_H}" aria-hidden="true">'
            f'{defs}{"".join(p)}</svg>')


# ============================================================ drawn pieces: strata
PAT = {
    "soil": ('<pattern id="{id}" width="23" height="17" patternUnits="userSpaceOnUse"><circle cx="4" cy="5" r=".9" '
             f'fill="{KHAKI}"></circle><circle cx="15" cy="12" r="1.1" fill="{KHAKI}"></circle><path d="M17 3 h3" '
             f'stroke="{KHAKI}" stroke-width=".9"></path></pattern>', ".5"),
    "diag": ('<pattern id="{id}" width="8" height="8" patternUnits="userSpaceOnUse"><path d="M0 8 L8 0" '
             'stroke="#5E6E6B" stroke-width=".8"></path></pattern>', ".22"),
    "granite": ('<pattern id="{id}" width="46" height="40" patternUnits="userSpaceOnUse"><path d="M8 8 h8 M12 4 v8 '
                f'M30 26 h8 M34 22 v8 M20 34 h6 M23 31 v6 M40 6 h5 M42.5 3.5 v5" stroke="{HORIZON}" '
                'stroke-width="1.1"></path></pattern>', ".5"),
}


def texture(kind: str, pid: str) -> str:
    pat, op = PAT[kind]
    return (f'<svg class="tex" aria-hidden="true"><defs>{pat.format(id=pid)}</defs>'
            f'<rect width="100%" height="100%" fill="url(#{pid})" opacity="{op}"></rect></svg>')


def edge(fill: str, kind: str, pid: str, seed: float, sw: float = 1.5, label: str = "") -> str:
    """The wavy contact at a stratum's top: the lower ground painted up over a flat join, then the ink line."""
    h = 30
    pts = [(x, 15 + 5 * math.sin(x / 210 + seed) + 2.4 * math.sin(x / 73 + seed * 2.3)) for x in range(-40, W + 81, 60)]
    d = smooth(pts)
    pat, op = PAT[kind]
    lab = (f'<text x="1360" y="{f(pts[24][1] + 26)}" text-anchor="end" font-family="Hanken Grotesk" font-style="italic" '
           f'font-size="14" fill="{INK}">{label}</text>' if label else "")
    return (f'<svg class="edge" width="{W}" height="{h + 24}" viewBox="0 0 {W} {h + 24}" aria-hidden="true">'
            f'<defs>{pat.format(id=pid)}</defs>'
            f'<path d="{d} L{W + 80} {h + 24} L-40 {h + 24} Z" fill="{fill}"></path>'
            f'<path d="{d} L{W + 80} {h + 24} L-40 {h + 24} Z" fill="url(#{pid})" opacity="{op}"></path>'
            f'<path d="{d}" stroke="{INK}" stroke-width="{sw}" fill="none" stroke-linejoin="round"></path>{lab}</svg>')


def bedding(seed: float) -> str:
    pts = [(x, 8 + 3 * math.sin(x / 160 + seed) + 1.5 * math.sin(x / 61 + seed * 2)) for x in range(-40, W + 81, 80)]
    return (f'<svg class="bed" width="{W}" height="16" viewBox="0 0 {W} 16" aria-hidden="true"><path d="{smooth(pts)}" '
            f'stroke="{INK}" stroke-width="1" stroke-dasharray="2 6" fill="none" opacity=".55"></path></svg>')


def swatch(kind: str) -> str:
    """The homepage key swatches (bronze brick, silver diagonal, gold stipple), at index-mark size."""
    fill, pat = {
        "gold": ("#E9DDAF", '<circle cx="2" cy="3" r="1" fill="#8A6F1E"></circle><circle cx="6.5" cy="7.5" r=".8" '
                            'fill="#8A6F1E"></circle>', ),
        "silver": ("#DCE2DF", '<path d="M0 8 L8 0" stroke="#5E6E6B" stroke-width=".8"></path>'),
        "bronze": ("#E2CDB3", '<path d="M0 11.5 H24 M12 0 V6 M0 6 H24 M0 6 V12" stroke="#7C5530" stroke-width=".8" '
                              'fill="none"></path>'),
    }[kind]
    pw, ph = {"gold": (9, 9), "silver": (8, 8), "bronze": (24, 12)}[kind]
    pid = f"k-{kind}"
    return (f'<svg class="sw" width="30" height="20" viewBox="0 0 30 20" aria-hidden="true"><defs>'
            f'<pattern id="{pid}" width="{pw}" height="{ph}" patternUnits="userSpaceOnUse">{pat}</pattern></defs>'
            f'<rect x=".75" y=".75" width="28.5" height="18.5" fill="{fill}"></rect>'
            f'<rect x=".75" y=".75" width="28.5" height="18.5" fill="url(#{pid})" opacity=".5"></rect>'
            f'<rect x=".75" y=".75" width="28.5" height="18.5" fill="none" stroke="{INK}" stroke-width="1.5"></rect></svg>')


# ============================================================ figures (one frame for every page)
FW, FH = 800, 272          # figure svg
PL, PR = 52, 620           # plot box, x; the direct-label column runs from PR + 12 to FW
LX = PR + 14


def t_text(x: float, y: float, s: str, anchor: str = "start", cls: str = "tk") -> str:
    return f'<text class="{cls}" x="{f(x)}" y="{f(y)}" text-anchor="{anchor}">{s}</text>'


def spread(items: list[tuple[float, str]], lo: float, hi: float, line: float = 15, pad: float = 3
           ) -> list[tuple[float, float, str]]:
    """Place label centres near their wanted y, top to bottom, so no two overlap; a label's height is its lines."""
    items = sorted(items)
    hs = [line * (s.count("|") + 1) for _, s in items]
    ys = [y for y, _ in items]
    for i in range(1, len(ys)):
        ys[i] = max(ys[i], ys[i - 1] + (hs[i - 1] + hs[i]) / 2 + pad)
    over = ys[-1] + hs[-1] / 2 - hi if ys else 0
    if over > 0:
        ys[-1] -= over
        for i in range(len(ys) - 2, -1, -1):
            ys[i] = min(ys[i], ys[i + 1] - (hs[i] + hs[i + 1]) / 2 - pad)
    return [(want, y, s) for (want, s), y in zip(items, ys)]


def declash(items: list[tuple[float, str]], lo: float, hi: float, gap: float) -> list[tuple[float, float, str]]:
    """Spread label ys (sorted top to bottom) at least gap apart inside [lo, hi]; keep each one's wanted y."""
    items = sorted(items)
    ys = [y for y, _ in items]
    for i in range(1, len(ys)):
        ys[i] = max(ys[i], ys[i - 1] + gap)
    over = ys[-1] - hi if ys else 0
    if over > 0:
        ys[-1] -= over
        for i in range(len(ys) - 2, -1, -1):
            ys[i] = min(ys[i], ys[i + 1] - gap)
    ys = [max(lo, y) for y in ys]
    return [(want, y, s) for (want, s), y in zip(items, ys)]


FUEL_PATS = (
    f'<pattern id="c-wind" width="14" height="6" patternUnits="userSpaceOnUse"><path d="M0 3 h8" stroke="{DAY}" '
    f'stroke-width=".8"></path></pattern>'
    f'<pattern id="c-gas" width="7" height="7" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r=".9" fill="{INK}">'
    f'</circle><circle cx="5.5" cy="5.5" r=".7" fill="{INK}"></circle></pattern>'
    f'<pattern id="c-imp" width="7" height="7" patternUnits="userSpaceOnUse"><path d="M0 7 L7 0" stroke="{DAY}" '
    f'stroke-width=".8"></path></pattern>'
    f'<pattern id="c-bio" width="10" height="8" patternUnits="userSpaceOnUse"><path d="M1 2 l3 1 M6 6 l3 -1" '
    f'stroke="{INK}" stroke-width=".8"></path></pattern>'
    f'<pattern id="c-ps" width="6" height="6" patternUnits="userSpaceOnUse"><path d="M0 0 L6 6 M-1 5 L1 7 M5 -1 L7 1" '
    f'stroke="{INK}" stroke-width=".9"></path></pattern>'
    f'<pattern id="c-null" width="7" height="7" patternUnits="userSpaceOnUse"><path d="M0 7 L7 0" stroke="{INK}" '
    f'stroke-width=".7"></path></pattern>'
)

# fuel code -> (fill, pattern id or None, pattern opacity). Codes with no palette slot and no sign join khaki,
# and PS (signed, meaning undocumented) is khaki under an ink cross-hatch. The band is always named by its codes.
FUEL_STYLE = {
    "WIND": (HORIZON, "c-wind", ".45"), "CCGT": (CLAY, "c-gas", ".22"), "OCGT": (CLAY, "c-gas", ".22"),
    "NUCLEAR": (PETROL, None, ""), "INT": (OLIVE, "c-imp", ".3"), "BIOMASS": (BIOMASS, "c-bio", ".3"),
    "OTHER": (KHAKI, None, ""), "NPSHYD": (KHAKI, None, ""), "COAL": (KHAKI, None, ""), "OIL": (KHAKI, None, ""),
    "PS": (KHAKI, "c-ps", ".55"),
}


def fuel_fill(code: str) -> tuple[str, str | None, str]:
    return FUEL_STYLE["INT" if code.startswith("INT") else code]


def fig_fuelhh(ch: dict) -> str:
    pg = ch["palette_groups_mw"]
    n = len(ch["hours_utc"])
    khaki = [pg["other"][i] + pg["uncovered:NPSHYD"][i] + pg["uncovered:COAL"][i] + pg["uncovered:OIL"][i]
             for i in range(n)]
    # bottom to top; the two signed series are outermost so they fall below the ground line when negative
    bands = [
        ("BIOMASS", pg["biomass"], "BIOMASS"), ("NUCLEAR", pg["nuclear"], "NUCLEAR"),
        ("OTHER", khaki, "OTHER, NPSHYD,|COAL, OIL"), ("CCGT", pg["gas"], "CCGT, OCGT"),
        ("WIND", pg["wind"], "WIND"), ("INT", pg["imports"], "INT* (10 links, net)"), ("PS", pg["uncovered:PS"], "PS (signed)"),
    ]
    top_gw, bot_gw = 35.0, -7.5
    PT, PB = 14, 236
    ky = (PB - PT) / (top_gw - bot_gw)
    y0 = PT + top_gw * ky

    def X(i: float) -> float:
        return PL + i * (PR - PL) / (n - 1)

    def Y(mw: float) -> float:
        return y0 - mw / 1000 * ky

    up = [0.0] * n
    dn = [0.0] * n
    shapes, mids = [], []
    for code, vals, label in bands:
        lo_u, lo_d = up[:], dn[:]
        hi_u = [lo_u[i] + max(vals[i], 0) for i in range(n)]
        hi_d = [lo_d[i] + min(vals[i], 0) for i in range(n)]
        fill, pid, op = fuel_fill(code)
        for lo, hi in ((lo_u, hi_u), (lo_d, hi_d)):
            if all(abs(a - b) < 1e-9 for a, b in zip(lo, hi)):
                continue
            d = ("M" + " L".join(f"{f(X(i))} {f(Y(hi[i]))}" for i in range(n)) + " " +
                 " ".join(f"L{f(X(i))} {f(Y(lo[i]))}" for i in range(n - 1, -1, -1)) + " Z")
            shapes.append(f'<path d="{d}" fill="{fill}"></path>')
            if pid:
                shapes.append(f'<path d="{d}" fill="url(#{pid})" opacity="{op}"></path>')
            shapes.append(f'<path d="M{" L".join(f"{f(X(i))} {f(Y(hi[i]))}" for i in range(n))}" fill="none" '
                          f'stroke="{T_TOP}" stroke-width=".7"></path>')
        up, dn = hi_u, hi_d
        # label at the band's mean position over the last six hours, on whichever side it sits there
        k = range(n - 6, n)
        v_end = sum(vals[i] for i in k) / 6
        if v_end >= 0:
            mid = sum((lo_u[i] + hi_u[i]) / 2 for i in k) / 6
        else:
            mid = sum((lo_d[i] + hi_d[i]) / 2 for i in k) / 6
        mids.append((Y(mid), label))
    placed = spread(mids, PT, PB + 8)
    labs, leads = [], []
    for want, y, s in placed:
        main, _, rest = s.partition(" (")
        lines = main.split("|")
        t = "".join(f'<tspan class="cd" x="{LX + 12}" dy="{0 if j == 0 else 15}">{esc(ln)}</tspan>'
                    for j, ln in enumerate(lines))
        if rest:
            t += f'<tspan class="an" dx="5">{esc(rest[:-1])}</tspan>'
        yy = y + 4.5 - 7.5 * (len(lines) - 1)
        labs.append(f'<text x="{LX + 12}" y="{f(yy)}">{t}</text>')
        leads.append(f"M{PR + 2} {f(want)} L{LX + 2} {f(want)} L{LX + 8} {f(y)}")
    # axes: the zero line is the ground
    ticks = []
    for gw in (-5, 0, 10, 20, 30):
        yy = Y(gw * 1000)
        ticks.append(f"M{PL - 5} {f(yy)} H{PL}")
        lab = f"{MINUS}5" if gw < 0 else str(gw)
        ticks.append("")
        shapes_lab = t_text(PL - 9, yy + 4.5, lab + (" GW" if gw == 30 else ""), "end")
        labs.append(shapes_lab)
    days = [i for i, h in enumerate(ch["hours_utc"]) if h[11:13] == "00"]
    dticks = " ".join(f"M{f(X(i))} {PB + 4} V{PB + 10}" for i in days)
    for i in days:
        labs.append(t_text(X(min(i + 12, n - 1)), PB + 24, f"{int(ch['hours_utc'][i][8:10])} Sep", "middle"))
    ann = ""
    aria = ("Stacked area chart of GB generation by Elexon fuel code, hourly, 20 to 26 September 2026, in MW. "
            "Nuclear holds at about 3.3 to 4.0 GW; wind swings between 1.3 and 16.0 GW and CCGT with OCGT between "
            "2.1 and 15.9 GW. Net interconnector flow runs from 6.3 GW of export to 6.6 GW "
            "of import, and pumped storage between minus 1.5 and plus 1.5 GW; negative values are drawn below the "
            "zero line.")
    return (f'<svg width="{FW}" height="{FH}" viewBox="0 0 {FW} {FH}" role="img" aria-label="{aria}">'
            f'<defs>{FUEL_PATS}</defs>{"".join(shapes)}'
            f'<path d="M{PL} {PT - 4} V{PB + 2}" stroke="{INK}" stroke-width="1"></path>'
            f'<path d="{" ".join(t for t in ticks if t)} {dticks}" stroke="{INK}" stroke-width="1"></path>'
            f'<path d="M{PL} {f(y0)} H{PR + 2}" stroke="{INK}" stroke-width="1.6"></path>'
            f'<path d="{" ".join(leads)}" stroke="{INK}" stroke-width=".8" fill="none" opacity=".6"></path>'
            f'<g class="lb">{"".join(labs)}{ann}</g></svg>')


def fig_prices(ch: dict) -> str:
    vals = ch["ssp_gbp_per_mwh"]
    n = len(vals)
    top, bot = 650.0, -150.0
    PT, PB = 14, 236
    ky = (PB - PT) / (top - bot)
    y0 = PT + top * ky

    def X(i: float) -> float:
        return PL + i * (PR - PL) / (n - 1)

    def Y(v: float) -> float:
        return y0 - v * ky

    pts = [(X(i), Y(v)) for i, v in enumerate(vals)]
    neg, run = [], []
    for (x, y), v in zip(pts, vals):
        if v < 0:
            run.append((x, y))
        elif run:
            neg.append(run)
            run = []
    if run:
        neg.append(run)
    shades = []
    step = (PR - PL) / (n - 1)
    for r in neg:
        xa, xb = r[0][0] - step / 2, r[-1][0] + step / 2
        poly = (f"M{f(xa)} {f(y0)} L{f(r[0][0])} {f(r[0][1])} " + " ".join(f"L{f(x)} {f(y)}" for x, y in r) +
                f" L{f(xb)} {f(y0)} Z")
        shades.append(f'<path d="{poly}" fill="{CLAY}"></path>')
    line = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts)
    labs = []
    ticks = []
    for v in (0, 200, 400, 600):
        ticks.append(f"M{PL - 5} {f(Y(v))} H{PL}")
        labs.append(t_text(PL - 9, Y(v) + 4.5, str(v) if v < 600 else "600", "end"))
    ticks.append(f"M{PL - 5} {f(Y(-100))} H{PL}")
    labs.append(t_text(PL - 9, Y(-100) + 4.5, f"{MINUS}100", "end"))
    days = [i for i, t in enumerate(ch["t_utc"]) if t[11:16] == "00:00"]
    dticks = " ".join(f"M{f(X(i))} {PB + 4} V{PB + 10}" for i in days)
    for i in days:
        labs.append(t_text(X(min(i + 24, n - 1)), PB + 24, f"{int(ch['t_utc'][i][8:10])} Sep", "middle"))
    imax = vals.index(max(vals))
    imin = vals.index(min(vals))
    marks = (f'<circle cx="{f(X(imax))}" cy="{f(Y(vals[imax]))}" r="3" fill="{INK}"></circle>'
             f'<circle cx="{f(X(imin))}" cy="{f(Y(vals[imin]))}" r="3" fill="{INK}"></circle>')
    labs.append(t_text(X(imax) - 8, Y(vals[imax]) + 4, "594.00 at 20:00 UTC, 22 Sep", "end", "an"))
    labs.append(t_text(X(imin) + 9, Y(vals[imin]) + 5, f"{MINUS}50.00 at 13:30 UTC, 20 Sep", "start", "an"))
    labs.append(t_text(PL + 8, Y(-118), "34 of 192 periods below zero", "start", "an"))
    labs.append(f'<text x="{LX + 12}" y="{f(Y(vals[-1]) + 4.5)}"><tspan class="cd">SSP</tspan>'
                f'<tspan class="an" dx="5">= SBP</tspan></text>')
    labs.append(t_text(LX + 12, Y(vals[-1]) + 22, "£/MWh", "start", "tk"))
    aria = ("Line chart of the GB system sell price, half-hourly, settlement dates 19 to 22 September 2026, in pounds "
            "per MWh. The price dips below zero in 34 of 192 periods, to a low of minus 50.00 at 13:30 UTC on 20 "
            "September, and peaks at 594.00 at 20:00 UTC on 22 September.")
    return (f'<svg width="{FW}" height="{FH}" viewBox="0 0 {FW} {FH}" role="img" aria-label="{aria}">'
            f'{"".join(shades)}'
            f'<path d="M{PL} {PT - 4} V{PB + 2}" stroke="{INK}" stroke-width="1"></path>'
            f'<path d="{" ".join(ticks)} {dticks}" stroke="{INK}" stroke-width="1"></path>'
            f'<path d="M{PL} {f(y0)} H{PR + 2}" stroke="{INK}" stroke-width="1.6"></path>'
            f'<path d="{line}" fill="none" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"></path>'
            f'<path d="M{PR + 2} {f(Y(vals[-1]))} H{LX + 8}" stroke="{INK}" stroke-width=".8" opacity=".6"></path>'
            f'{marks}<g class="lb">{"".join(labs)}</g></svg>')


def fig_flows(ch: dict) -> str:
    from datetime import date
    d0 = date(2026, 8, 1)
    d1 = date(2026, 9, 21)
    span = (d1 - d0).days
    top = 650.0
    PT, PB = 14, 236
    ky = (PB - PT) / top
    y0 = PB

    def X(d: str) -> float:
        dd = date(int(d[:4]), int(d[5:7]), int(d[8:10]))
        return PL + 10 + (dd - d0).days * (PR - PL - 20) / span

    def Y(v: float) -> float:
        return y0 - v * ky

    g_a, g_b = X("2026-08-05"), X("2026-09-13")
    step = (PR - PL - 20) / span
    gap = (f'<rect x="{f(g_a + step * .5)}" y="{PT}" width="{f(g_b - g_a - step)}" height="{PB - PT}" fill="url(#c-null)" '
           f'opacity=".16"></rect>')
    gap_lab = (t_text((g_a + g_b) / 2, PT + 26, "no rows in local silver", "middle", "an") +
               t_text((g_a + g_b) / 2, PT + 44, "6 Aug to 12 Sep", "middle", "an"))
    series = []
    labs = []
    styles = {"St. Fergus": (CLAY, CLAY, "1.8"), "Bacton (IUK)": (INK, DAY, "1.3")}
    ends = []
    for se in ch["series"]:
        stroke, fill, sw = styles[se["point_label"]]
        blocks = [[p for p in se["points"] if p["timestamp_utc"] < "2026-08-10"],
                  [p for p in se["points"] if p["timestamp_utc"] > "2026-09-01"]]
        for b in blocks:
            d = "M" + " L".join(f"{f(X(p['timestamp_utc']))} {f(Y(p['flow_gwh_per_day']))}" for p in b)
            series.append(f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"></path>')
            series.append("".join(f'<circle cx="{f(X(p["timestamp_utc"]))}" cy="{f(Y(p["flow_gwh_per_day"]))}" r="3.4" '
                                  f'fill="{fill}" stroke="{stroke}" stroke-width="1.4"></circle>' for p in b))
        last = se["points"][-1]
        ends.append((Y(last["flow_gwh_per_day"]), f'{se["point_label"]} ({se["direction_key"]})'))
    for want, y, s in declash(ends, PT + 6, PB, 18):
        main, _, rest = s.partition(" (")
        labs.append(f'<text x="{LX + 12}" y="{f(y + 4.5)}"><tspan class="nm">{esc(main)}</tspan>'
                    f'<tspan class="an" dx="5">{rest[:-1]}</tspan></text>')
        labs.append(f'<path d="M{PR - 4} {f(want)} L{LX + 2} {f(want)} L{LX + 8} {f(y)}" stroke="{INK}" '
                    f'stroke-width=".8" fill="none" opacity=".6"></path>')
    zx0, zx1 = X("2026-09-13"), X("2026-09-20")
    labs.append(t_text((zx0 + zx1) / 2, y0 - 12, "0.0 GWh/d on 13 to 20 Sep, as reported", "middle", "an"))
    ticks, tl = [], []
    for v in (0, 200, 400, 600):
        ticks.append(f"M{PL - 5} {f(Y(v))} H{PL}")
        tl.append(t_text(PL - 9, Y(v) + 4.5, str(v), "end"))
    for dstr, lab in (("2026-08-01", "1 Aug"), ("2026-08-05", "5 Aug"), ("2026-09-13", "13 Sep"), ("2026-09-21", "21 Sep")):
        ticks.append(f"M{f(X(dstr))} {PB + 4} V{PB + 10}")
        tl.append(t_text(X(dstr), PB + 24, lab, "middle"))
    tl.append(t_text(LX + 12, PB + 24, "GWh/d", "start"))
    aria = ("Line chart of daily physical gas flow in GWh per day at two GB points reported by National Gas TSO, for "
            "every gas day held locally: 1 to 5 August and 13 to 21 September 2026, with no rows between. St. Fergus "
            "entry runs from 350 to 595. Bacton (IUK) exit is 382 to 407 in August, 0.0 from 13 to 20 September, and "
            "175 on 21 September.")
    return (f'<svg width="{FW}" height="{FH}" viewBox="0 0 {FW} {FH}" role="img" aria-label="{aria}">'
            f'<defs>{FUEL_PATS}</defs>{gap}'
            f'<path d="M{PL} {PT - 4} V{PB + 2}" stroke="{INK}" stroke-width="1"></path>'
            f'<path d="{" ".join(ticks)}" stroke="{INK}" stroke-width="1"></path>'
            f'<path d="M{PL} {f(y0)} H{PR + 2}" stroke="{INK}" stroke-width="1.6"></path>'
            f'{"".join(series)}<g class="lb">{gap_lab}{"".join(tl)}{"".join(labs)}</g></svg>')


def fig_units(ch: dict) -> str:
    bars = {b["fuel_type"]: b["units"] for b in ch["bars"]}
    total = sum(bars.values())
    typed = total - bars["(null)"]
    rows = [("WIND", bars["WIND"]), ("OTHER", bars["OTHER"]), ("CCGT", bars["CCGT"]), ("OCGT", bars["OCGT"]),
            ("NPSHYD", bars["NPSHYD"]), ("NUCLEAR", bars["NUCLEAR"]), ("PS", bars["PS"]), ("BIOMASS", bars["BIOMASS"]),
            ("INT*", sum(v for k, v in bars.items() if k.startswith("INT"))), ("COAL", bars["COAL"])]
    assert sum(v for _, v in rows) == typed == 499 and total == 3014
    k = (PR - PL) / total
    by, bh = 26, 24
    out = []
    x = PL
    for code, v in rows:
        fill, pid, op = fuel_fill("INTFR" if code == "INT*" else code)
        out.append(f'<rect x="{f(x)}" y="{by}" width="{f(v * k)}" height="{bh}" fill="{fill}"></rect>')
        if pid:
            out.append(f'<rect x="{f(x)}" y="{by}" width="{f(v * k)}" height="{bh}" fill="url(#{pid})" opacity="{op}"></rect>')
        x += v * k
    xt = x
    out.append(f'<rect x="{f(xt)}" y="{by}" width="{f(PR - xt)}" height="{bh}" fill="{DAY}"></rect>'
               f'<rect x="{f(xt)}" y="{by}" width="{f(PR - xt)}" height="{bh}" fill="url(#c-null)" opacity=".28"></rect>')
    out.append(f'<rect x="{PL}" y="{by}" width="{PR - PL}" height="{bh}" fill="none" stroke="{INK}" stroke-width="1.3"></rect>'
               f'<path d="M{f(xt)} {by - 6} V{by + bh + 6}" stroke="{INK}" stroke-width="1.3"></path>')
    labs = [
        f'<text x="{PL}" y="{by - 10}"><tspan class="nm">499</tspan><tspan class="an" dx="5">with a fuel type</tspan></text>',
        f'<text x="{PR}" y="{by - 10}" text-anchor="end"><tspan class="nm">2,515</tspan><tspan class="an" dx="5">with '
        f'no fuel type (null)</tspan></text>',
        f'<text x="{LX + 12}" y="{by + 17}"><tspan class="nm">3,014</tspan><tspan class="an" dx="5">BM units</tspan></text>',
    ]
    # the enlargement: the 499 typed units, by code, on their own count scale
    top = 76
    pitch, h = 16.2, 11
    cx0 = PL + 92
    kc = (PR - 40 - cx0) / 250
    out.append(f'<path d="M{PL} {by + bh} L{PL} {top - 12} M{f(xt)} {by + bh} L{PR - 40} {top - 12}" stroke="{INK}" '
               f'stroke-width=".8" opacity=".55" fill="none"></path>'
               f'<path d="M{PL} {top - 12} H{PR - 40}" stroke="{INK}" stroke-width=".8" opacity=".55"></path>')
    for i, (code, v) in enumerate(rows):
        y = top + i * pitch
        fill, pid, op = fuel_fill("INTFR" if code == "INT*" else code)
        out.append(f'<rect x="{cx0}" y="{f(y)}" width="{f(v * kc)}" height="{h}" fill="{fill}"></rect>')
        if pid:
            out.append(f'<rect x="{cx0}" y="{f(y)}" width="{f(v * kc)}" height="{h}" fill="url(#{pid})" opacity="{op}"></rect>')
        labs.append(f'<text class="cd" x="{cx0 - 10}" y="{f(y + 9.5)}" text-anchor="end">{esc(code)}</text>')
        labs.append(t_text(cx0 + v * kc + 7, y + 9.5, str(v), "start"))
    ay = top + len(rows) * pitch + 4
    ticks = " ".join(f"M{f(cx0 + c * kc)} {f(ay)} V{f(ay + 5)}" for c in range(0, 251, 50))
    out.append(f'<path d="M{cx0} {f(ay)} H{f(cx0 + 250 * kc)} {ticks}" stroke="{INK}" stroke-width="1"></path>')
    for c in range(0, 251, 50):
        labs.append(t_text(cx0 + c * kc, ay + 19, str(c), "middle"))
    labs.append(t_text(cx0 + 250 * kc + 14, ay + 19, "units", "start"))
    labs.append(f'<text x="{LX + 12}" y="{top + 9}"><tspan class="an">the 499, by code;</tspan></text>')
    labs.append(f'<text x="{LX + 12}" y="{top + 26}"><tspan class="an">INT* is ten codes</tspan></text>')
    aria = ("Bar chart of the 26 September 2026 snapshot of 3,014 BM units. A bar drawn to scale splits them into 499 "
            "units with a fuel type and 2,515 with none. The 499 are then enlarged by fuel code: WIND 234, OTHER 92, "
            "CCGT 61, OCGT 22, NPSHYD 22, NUCLEAR 16, PS 16, BIOMASS 15, ten interconnector codes 11, COAL 10.")
    return (f'<svg width="{FW}" height="{FH}" viewBox="0 0 {FW} {FH}" role="img" aria-label="{aria}">'
            f'<defs>{FUEL_PATS}</defs>{"".join(out)}<g class="lb">{"".join(labs)}</g></svg>')


# ============================================================ content: the four specimens
def code(s: str) -> str:
    return f"<code>{esc(s)}</code>"


def ts(v: str) -> str:
    """Silver timestamps as a pandas DataFrame prints them."""
    return v.replace("T", " ")


def fmt(v: object) -> str:
    if v is None:
        return '<span class="nul">null</span>'
    if isinstance(v, float):
        s = repr(v)
        return s.replace("-", MINUS, 1) if s.startswith("-") else s
    if isinstance(v, str) and len(v) >= 19 and v[4] == "-" and v[10] == "T":
        return esc(ts(v))
    return esc(str(v))


def hl_call(s: str) -> str:
    """Syntax colour for a one-line workbench call: strings in clay-deep, as on the homepage notebook."""
    out, i = [], 0
    while i < len(s):
        if s[i] == '"':
            j = s.index('"', i + 1)
            out.append(f'<span class="s">{esc(s[i:j + 1])}</span>')
            i = j + 1
        else:
            out.append(esc(s[i]))
            i += 1
    return "".join(out)


LINEAGE = {"event_time", "available_at", "source_run_id", "dataset_version", "vintage_policy"}


def spec_fuelhh() -> dict:
    s = SPEC["elexon/fuelhh"]
    return dict(
        slug="fuelhh", key="elexon/fuelhh", vendor="Elexon BMRS", asset="substation",
        title="FUELHH datasheet", h1="Generation outturn by fuel type", one=s["identity"]["what_it_is"],
        fig_h="Generation by fuel code, 20 to 26 September 2026", fig=fig_fuelhh(s["chart"]),
        cap=(f'{code("elexon/fuelhh")} silver, MW (axis in GW), settlement dates 20 to 26 September 2026. Hourly means, '
             'UTC; codes in one band are summed first. Positive values stack up from zero, negative ones down; the PS '
             'sign is not documented.'),
        facts=[
            ("Vendor dataset", f'{code("FUELHH")}, Elexon Insights API'),
            ("Grain", f'settlement period × {code("fuel_type")}'),
            ("Cadence", "every 30 minutes"),
            ("History", "2021-09-01 to 2026-09-26, with gaps"),
            ("Publication lag", "period end (30 min) on 99.82% of rows"),
            ("Units", "MW; INT* and PS are signed"),
            ("Volume", "29,760 rows in August 2026"),
        ],
        get=[
            ("gold", "Workbench", s["how_to_get_it"]["workbench"], "a pandas DataFrame; 6,720 rows for this range"),
            ("silver", "Silver relation", "silver_elexon_fuelhh", f'date column {code("settlement_date")}'),
            ("bronze", "Vendor endpoint", "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELHH\n"
                                         "    ?publishDateTimeFrom=<UTC Z>&publishDateTimeTo=<UTC Z>&page=<n>", ""),
        ],
        what=("Elexon’s half-hourly record of what GB generation produced, split by fuel-type code. Each settlement "
              "period carries one MW value per code: wind, gas, nuclear, biomass, hydro, pumped storage, coal, oil, "
              "other, and ten interconnectors, signed so that imports are positive. There is no solar code. gridflow "
              "keeps the codes as sent, one row each."),
        uses=[
            ("Fuel-mix features", "Hourly wind, gas and nuclear outturn as inputs to a GB price model."),
            ("Net interconnector flow", "Sum the INT* codes for GB net imports, or read each link on its own."),
            ("Scoring a wind forecast", f'{code("WIND")} outturn is an observed series to score a wind forecast against.'),
        ],
        schema_src=f'Pydantic class {code("ElexonFuelHH")} in {code("gridflow/schemas/elexon.py")}; transformer version 2.0.0.',
        schema=[
            ("settlement_date", "Date", "GB settlement date, derived from the vendor start time"),
            ("settlement_period", "Int32", "half-hour index, 1 to 50 (46 or 50 on clock-change days)"),
            ("timestamp_utc", "Datetime(us, UTC)", "start of the half-hour, UTC"),
            ("fuel_type", "String", "Elexon fuel-type code, uppercase as sent"),
            ("generation_mw", "Float64", "MW for the period; INT* positive is import to GB; PS signed, meaning undocumented"),
            ("published_at", "Datetime(us, UTC)", "vendor publication time"),
            ("data_provider", "String", "always elexon"),
            ("ingested_at", "Datetime(us, UTC)", "when the silver transform ran, not the bronze fetch"),
            ("event_time", "Datetime(us, UTC)", "event instant for the bitemporal layer"),
            ("available_at", "Datetime(us, UTC)", f'when the row became knowable: {code("published_at")}, else ingest time'),
            ("source_run_id", "String", "the pipeline run that wrote the row"),
            ("dataset_version", "String", "transformer version stamped on the row"),
        ],
        sample_cap="Silver rows for settlement date 2026-09-26, period 25 (11:00 UTC): 8 of that period’s 20 codes.",
        sample_cols=["settlement_date", "settlement_period", "timestamp_utc", "fuel_type", "generation_mw"],
        sample=s["sample_rows"]["rows"],
        caveats=[
            ("No solar.", "FUELHH has no solar code at all, so solar outturn has to come from another dataset."),
            ("Eleven codes are signed:", "the ten INT* interconnectors (positive is import to GB) and PS. Negatives "
                                         "are routine: INTIRL is negative in 70.3% of all half-hours, PS in 54.7%."),
            ("The code set changes over time:", "INTELEC starts 2021-09-14, INTVKL 2023-07-12 and INTGRNL 2024-03-19, "
                                                "and a stray INTELE has 9 zero rows on 2021-09-10. A half-hour holds 17 "
                                                "to 20 rows."),
        ],
        related=[
            ("elexon/fuelinst", "Instantaneous generation outturn by fuel type, from the same connector."),
            ("elexon/bmunits_reference", "The BM Unit registry; it shares the fuel-type codes."),
            ("elexon/indo", "Demand outturn, used to check the INT* sign convention."),
            ("neso_data_portal/historic_generation_mix", "Where GB solar outturn is found."),
        ],
    )


def spec_prices() -> dict:
    s = SPEC["elexon/system_prices"]
    return dict(
        slug="system-prices", key="elexon/system_prices", vendor="Elexon BMRS", asset="substation",
        title="System prices datasheet", h1="System sell and buy prices", one=s["identity"]["what_it_is"],
        fig_h="System sell price, 19 to 22 September 2026", fig=fig_prices(s["chart"]),
        cap=(f'{code("elexon/system_prices")} silver, latest vintage per period, £/MWh, settlement dates 19 to 22 '
             'September 2026, times in UTC. Native half-hourly values, 192 of them, nothing averaged; SBP equals SSP in '
             'every period, so one line carries both.'),
        facts=[
            ("Vendor dataset", f'{code("DISEBSP")}, Elexon Insights API'),
            ("Grain", "settlement period × vendor publication"),
            ("Cadence", "every 30 minutes"),
            ("History", "2021-09-01 to 2026-09-22, no dates missing"),
            ("Publication lag", "median 52 min to 2023; about 24.7 h from 2024"),
            ("Units", "£/MWh; net imbalance volume in MWh"),
            ("Volume", "3,770 rows in August 2026"),
        ],
        get=[
            ("gold", "Workbench", s["how_to_get_it"]["workbench"], "reads the latest vintage: one row per period"),
            ("silver", "Silver relation", "silver_elexon_system_prices_latest",
             f'date column {code("settlement_date")}; raw parquet keeps every vintage'),
            ("bronze", "Vendor endpoint", "GET https://data.elexon.co.uk/bmrs/api/v1/balancing/settlement/system-prices/"
                                         "{YYYY-MM-DD}\n    ?page=<n>", ""),
        ],
        what=("The GB imbalance (cash-out) prices Elexon publishes for each settlement period: the system sell price "
              "and system buy price in £/MWh, with the net imbalance volume in MWh. gridflow appends every publication "
              "the vendor makes, so a period can hold more than one row; the workbench reads only the latest."),
        uses=[
            ("Imbalance price modelling", "The target series for a GB cash-out price forecast, negative prices included."),
            ("Pricing a forecast error", "Value a generation or demand imbalance at the period’s system price."),
            ("Day-ahead spread", f'Set beside {code("elexon/mid")}, which the workbench’s day-ahead benchmark reads.'),
        ],
        schema_src=(f'Pydantic class {code("ElexonSystemPrice")} in {code("gridflow/schemas/elexon.py")}; transformer '
                    'version 2.0.0, append-only.'),
        schema=[
            ("settlement_date", "Date", "GB settlement date"),
            ("settlement_period", "Int32", "half-hour index, 1 to 50"),
            ("timestamp_utc", "Datetime(us, UTC)", "period start, UTC"),
            ("system_sell_price", "Float64", f"SSP, GBP/MWh; schema bound {MINUS}500 to 10,000"),
            ("system_buy_price", "Float64", "SBP, GBP/MWh; equal to SSP on every row"),
            ("net_imbalance_volume", "Float64", "NIV, MWh; the sign convention is not documented"),
            ("run_type", "String", "null on every row; this endpoint has no such field"),
            ("price_derivation_code", "String", "vendor code: N, P or K"),
            ("published_at", "Datetime(us, UTC)", "vendor createdDateTime"),
            ("data_provider", "String", "always elexon"),
            ("ingested_at", "Datetime(us, UTC)", "when the silver transform ran"),
            ("event_time", "Datetime(us, UTC)", "event instant for the bitemporal layer"),
            ("available_at", "Datetime(us, UTC)", f'when the row became knowable: {code("published_at")}, else ingest time'),
            ("source_run_id", "String", "the pipeline run that wrote the row"),
            ("dataset_version", "String", "transformer version stamped on the row"),
            ("vintage_policy", "String", "the rule that set available_at; vendor on every row"),
        ],
        sample_cap=("Silver rows for settlement date 2026-09-20, periods 22 to 29; one vintage each. system_buy_price "
                    "equals system_sell_price on every row, so it is left out here."),
        sample_cols=["settlement_period", "timestamp_utc", "system_sell_price", "net_imbalance_volume",
                     "price_derivation_code", "published_at"],
        sample=s["sample_rows"]["rows"],
        caveats=[
            ("Silver is append-only:", "96,793 rows cover 88,694 periods. Read the _latest view (the workbench does) "
                                       "or dedupe on available_at before plotting."),
            ("SSP equals SBP", "on every row since 2021-09, so one line carries both."),
            ("Negative prices are routine:", "4,052 periods since 2021-09 (latest vintage), and 34 of the 192 in the "
                                             "figure."),
        ],
        related=[
            ("neso/carbon_intensity", f'Joined to these prices by the workbench’s {code("imbalance_context()")}.'),
            ("elexon/mid", "Read by the workbench’s GB day-ahead benchmark."),
        ],
    )


def spec_flows() -> dict:
    s = SPEC["entsog/physical_flows"]
    return dict(
        slug="physical-flows", key="entsog/physical_flows", vendor="ENTSO-G", asset="gas",
        title="Physical flows datasheet", h1="Physical gas flows", one=s["identity"]["what_it_is"],
        fig_h="Daily flow at two GB points, every gas day held", fig=fig_flows(s["chart"]),
        cap=(f'{code("entsog/physical_flows")} silver, GWh/d, every gas day held locally. One native value a gas day '
             'as National Gas TSO reports it; nothing averaged or interpolated, and the line breaks where there are no '
             'rows.'),
        facts=[
            ("Vendor dataset", f'{code("operationalData")}, Physical Flow indicator'),
            ("Grain", "gas day × point × operator × direction"),
            ("Cadence", "daily, on each operator’s gas day"),
            ("History", "1 to 5 Aug and 13 to 21 Sep 2026"),
            ("Publication lag", "not established"),
            ("Units", "GWh/d; flow can be null"),
            ("Volume", "about 983 rows a gas day"),
        ],
        get=[
            ("gold", "Workbench", s["how_to_get_it"]["workbench"],
             "gas days that start before midnight UTC fall outside the first day"),
            ("silver", "Silver relation", "silver_entsog_physical_flows", f'date column {code("timestamp_utc")}'),
            ("bronze", "Vendor endpoint", "GET https://transparency.entsog.eu/api/v1/operationalData\n    ?limit=-1&"
                                         "timeZone=UCT&from=YYYY-MM-DD&to=YYYY-MM-DD\n    &indicator=Physical%20Flow"
                                         "&periodType=day",
             ""),
        ],
        what=("ENTSOG’s physical-flow indicator: the gas that moved each gas day at interconnection points, LNG "
              "terminals and other points on Europe’s transmission systems. Operators on both sides of a point "
              "report it, each as entry or exit, so one point can appear once per operator and direction. gridflow "
              "normalises every value to GWh/d."),
        uses=[
            ("Border flows", "Follow one point day by day, such as Bacton (IUK) exit."),
            ("Supply features", "Daily entry flow at terminals such as St. Fergus as inputs to a gas price model."),
            ("Checking both sides", "Compare two operators’ values at one point, as at Bacton (IUK) on 21 September."),
        ],
        schema_src=(f'Pydantic class {code("EntsogPhysicalFlow")} in {code("gridflow/schemas/entsog.py")}; transformer '
                    'version 1.0.0.'),
        schema=[
            ("timestamp_utc", "Datetime(us, UTC)", "gas-day start (vendor periodFrom), UTC"),
            ("point_key", "String", "ENTSOG point id, such as ITP-00005"),
            ("point_label", "String", "point name, such as Bacton (IUK)"),
            ("operator_key", "String", "reporting operator id, such as UK-TSO-0001"),
            ("operator_label", "String", "operator name, such as National Gas TSO"),
            ("direction_key", "String", "entry or exit, relative to the reporting operator (inferred)"),
            ("flow_gwh_per_day", "Float64", "flow normalised to GWh/d; nullable"),
            ("unit", "String", "always GWh/d"),
            ("data_provider", "String", "always entsog"),
            ("ingested_at", "Datetime(us, UTC)", "when the silver transform ran; not in the Pydantic class"),
            ("event_time", "Datetime(us, UTC)", "event instant for the bitemporal layer"),
            ("available_at", "Datetime(us, UTC)", "when the row became knowable; here, the ingest time"),
            ("source_run_id", "String", "the pipeline run that wrote the row"),
            ("dataset_version", "String", "transformer version stamped on the row"),
        ],
        sample_cap="Silver rows for gas day 2026-09-21 (timestamp_utc 04:00 UTC) at GB points; Avonmouth LNG reports a null flow.",
        sample_cols=["point_key", "point_label", "operator_key", "operator_label", "direction_key", "flow_gwh_per_day"],
        sample=s["sample_rows"]["rows"],
        caveats=[
            ("Local history is 14 gas days", "in two blocks: 1 to 5 August and 13 to 21 September 2026."),
            ("Both sides of a point are reported,", "so summing every row double counts. At Bacton (IUK) on "
                                                    "2026-09-21, National Gas TSO exit and Interconnector entry are "
                                                    "both 175.165952 GWh/d."),
            ("Flows can be null:", "2,499 rows, including every day for 176 series such as Avonmouth LNG entry. Do "
                                   "not zero-fill."),
        ],
        related=[
            ("entsog/aggregated_physical_flows", "The same Physical Flow indicator, aggregated by zone."),
            ("entsog/nominations", "The same endpoint, Nomination indicator."),
            ("entsog/allocations", "The same endpoint, Allocation indicator."),
        ],
    )


def spec_units() -> dict:
    s = SPEC["elexon/bmunits_reference"]
    return dict(
        slug="bmunits-reference", key="elexon/bmunits_reference", vendor="Elexon BMRS", asset="substation",
        title="BM Units datasheet", h1="BM Unit reference data", one=s["identity"]["what_it_is"],
        fig_h="BM units by fuel type, one snapshot", fig=fig_units(s["chart"]),
        cap=(f'{code("elexon/bmunits_reference")} silver, count of BM units, snapshot of 26 September 2026. No time '
             'axis: all 3,014 units to scale, then the 499 with a fuel type by code. Counts only; capacities are not '
             'additive.'),
        facts=[
            ("Vendor dataset", f'{code("reference/bmunits/all")}, Elexon Insights API'),
            ("Grain", f'BM Unit ({code("bm_unit_id")})'),
            ("Cadence", "weekly snapshot, overwritten"),
            ("History", "current snapshot only (2026-09-26)"),
            ("Publication lag", "not established"),
            ("Units", "MW, per registration"),
            ("Volume", "3,014 rows"),
        ],
        get=[
            ("gold", "Workbench", s["how_to_get_it"]["workbench"],
             f'not {code("query()")}: its date column is ingested_at, so a date range returns 0 rows'),
            ("silver", "Silver relation", "silver_elexon_bmunits_reference", "one file, overwritten on each run"),
            ("bronze", "Vendor endpoint", "GET https://data.elexon.co.uk/bmrs/api/v1/reference/bmunits/all",
             "no parameters, no pagination"),
        ],
        what=("Elexon’s registry of Balancing Mechanism Units: one row per unit, with its name, fuel type, registered "
              "capacity, lead party and GSP group. gridflow keeps it as a single snapshot, overwritten on each run, so it "
              "describes the registry as it stands, not its history. Most units carry no fuel type."),
        uses=[
            ("Naming unit-level data", f'Join on {code("bm_unit_id")} to label rows in {code("elexon/boal")} or {code("elexon/pn")}.'),
            ("Grouping units by fuel", f'Map units to the fuel codes of {code("elexon/fuelhh")}; 499 of 3,014 have one.'),
            ("A party’s units", f'Filter on {code("company_name")} to list the units a lead party registers.'),
        ],
        schema_src=(f'Pydantic class {code("ElexonBMUnit")} in {code("gridflow/schemas/elexon.py")}; transformer '
                    'version 1.1.0.'),
        schema=[
            ("bm_unit_id", "String", "Elexon BM Unit id; the entity key"),
            ("bm_unit_name", "String", "vendor name; often repeats the id"),
            ("fuel_type", "String", "vendor fuel type; null on 2,515 of 3,014 rows"),
            ("registered_capacity_mw", "Float64", "registered capacity, MW; not additive across rows"),
            ("company_name", "String", "lead party name"),
            ("gsp_group_id", "String", "GSP group, such as _A; null on 1,822 rows"),
            ("national_grid_bm_unit", "String", "National Grid BM Unit, such as ABERU-1; not an ENTSO-E EIC"),
            ("data_provider", "String", "always elexon"),
            ("ingested_at", "Datetime(us, UTC)", "when the silver transform ran"),
            ("event_time", "Datetime(us, UTC)", "the target date, 2026-09-26 00:00 UTC"),
            ("available_at", "Datetime(us, UTC)", "when the row became knowable; here, the ingest time"),
            ("source_run_id", "String", "the pipeline run that wrote the row"),
            ("dataset_version", "String", "transformer version stamped on the row"),
        ],
        sample_cap="Eight units from the 26 September 2026 snapshot.",
        sample_cols=["bm_unit_id", "bm_unit_name", "fuel_type", "registered_capacity_mw", "company_name",
                     "gsp_group_id", "national_grid_bm_unit"],
        sample=s["sample_rows"]["rows"],
        caveats=[
            ("83% of units have no fuel type", "(2,515 of 3,014), so a fuel breakdown covers only 499 units."),
            ("Capacity is not additive:", f'{code("registered_capacity_mw")} is per registration, and the null-fuel '
                                          "rows alone sum to 727,551 MW."),
            ("One snapshot, overwritten each run,", "and keyless vendor rows are dropped, so counts drift between runs: "
                                                    "2,969 on 2026-09-09, 3,014 on 2026-09-26."),
        ],
        related=[
            ("elexon/boal", f'Per-unit data joined on {code("bm_unit_id")}.'),
            ("elexon/pn", f'Per-unit data joined on {code("bm_unit_id")}.'),
            ("elexon/uou2t14d", "Per-unit availability."),
            ("elexon/fuelhh", "Shares the fuel-type codes; interconnector flow is found there."),
        ],
    )


# ============================================================ page
CSS = """body{margin:0}
.root{--petrol:#155A6E;--daylight:#F6F4EC;--topsoil:#ECE8DA;--zebra:#EFEBDF;--ink:#1C2B22;--ink-2:#3F4A3B;--muted:#5d6a55;
--rule-ink:rgba(28,43,34,.22);--on-petrol:#F6F4EC;--on-petrol-2:#CFE0DC;--on-petrol-3:#B4D0CD;--rule-petrol:rgba(207,224,220,.22);
--chartreuse:#AFC64E;--olive:#66793B;--silver-tint:#DCE2DF;
background:var(--petrol);color:var(--ink);font:400 16px/1.6 "Hanken Grotesk",sans-serif;font-variant-numeric:tabular-nums;
-webkit-font-smoothing:antialiased}
.root a{color:inherit;text-decoration-thickness:1.5px;text-underline-offset:4px;text-decoration-color:var(--olive)}
.root a:focus-visible{outline:2px solid var(--chartreuse);outline-offset:3px;border-radius:2px}
.root h1,.root h2,.root h3{font-family:"Bricolage Grotesque",sans-serif;margin:0;font-optical-sizing:auto}
.root code{font-family:"Red Hat Mono",monospace;font-size:.9em}
.root svg{display:block}
.band{position:relative;padding:0 80px}
.band>*{position:relative}
.tex{position:absolute;inset:0;width:100%;height:100%}
.edge{position:absolute;left:0;top:-15px}
.bed{margin:0 -80px}

/* sky: masthead and title band */
.sky{background:var(--petrol);color:var(--on-petrol)}
.mast{display:flex;justify-content:space-between;align-items:baseline;padding:26px 80px 0}
.brand{font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:24px;letter-spacing:-.01em;text-decoration:none}
.mast ul{display:flex;gap:30px;list-style:none;margin:0;padding:0;font-size:15px}
.mast ul a{text-decoration:none;color:var(--on-petrol-2)}
.mast ul a:hover{color:var(--on-petrol)}
.mast ul a[aria-current="page"]{color:var(--on-petrol);box-shadow:inset 0 -2px 0 var(--chartreuse)}
.title{padding:30px 80px 0}
.crumbs ol{display:flex;list-style:none;margin:0;padding:0;font-size:15px;color:var(--on-petrol-2)}
.crumbs li+li::before{content:"/";margin:0 10px;color:var(--on-petrol-3)}
.crumbs a{text-decoration-color:rgba(175,198,78,.7)}
.head{display:grid;grid-template-columns:minmax(0,1fr) auto;column-gap:40px;align-items:baseline;margin:14px 0 0}
.head h1{font-size:60px;font-weight:760;font-stretch:84%;line-height:.98;letter-spacing:-.02em;color:var(--on-petrol)}
.pn{margin:0;font:500 19px/1 "Red Hat Mono",monospace;color:var(--on-petrol-2)}
.one{margin:14px 0 0;max-width:60ch;font-size:19px;line-height:1.5;color:var(--on-petrol-2)}
.land{margin:-78px 0 0}

/* the plate */
.soil{background:var(--topsoil)}
.plate{display:grid;grid-template-columns:800px minmax(0,1fr);column-gap:64px;padding-top:16px}
.plate h2{font-size:23px;font-weight:720;font-stretch:90%;line-height:1.1;letter-spacing:-.01em;margin:0 0 14px}
.fig{margin:0}
.fig figcaption{margin:8px 0 0;font-size:14.5px;line-height:1.5;color:var(--ink-2);max-width:98ch}
.fig figcaption code{font-size:13.5px;color:var(--ink)}
.fig .tk{font:400 12.5px "Hanken Grotesk",sans-serif;fill:var(--ink-2)}
.fig .an{font:italic 400 13.5px "Hanken Grotesk",sans-serif;fill:var(--ink)}
.fig .cd{font:500 12.5px "Red Hat Mono",monospace;fill:var(--ink)}
.fig .nm{font:600 13.5px "Hanken Grotesk",sans-serif;fill:var(--ink)}
.facts{margin:0;display:grid;grid-template-columns:128px minmax(0,1fr);border-bottom:1px solid var(--rule-ink)}
.facts dt,.facts dd{margin:0;padding:8px 0 9px;border-top:1px solid var(--rule-ink);line-height:1.42}
.facts dt{font-size:14.5px;font-weight:600;color:var(--ink)}
.facts dd{font-size:15px;color:var(--ink-2)}
.facts code{font-size:13.5px;color:var(--ink)}

/* the rail: every block below the figure hangs its heading here */
.row{display:grid;grid-template-columns:240px minmax(0,1fr);column-gap:40px}
.row>h2{font-size:30px;font-weight:700;font-stretch:90%;line-height:1.05;letter-spacing:-.012em}
.get{padding:26px 0 34px}
.get>h2{font-size:23px;font-weight:720;line-height:1.1;padding-top:4px}
.ways{margin:0;display:grid;grid-template-columns:30px 140px minmax(0,1fr);column-gap:16px;row-gap:12px;align-items:start}
.ways dt{display:contents}
.ways .sw{margin-top:4px}
.ways .lab{font-size:15px;font-weight:600;padding-top:3px}
.ways dd{margin:0;display:flex;align-items:flex-start;column-gap:24px}
.call{margin:0;display:inline-block;background:var(--daylight);border:1px solid var(--ink);border-radius:3px;padding:7px 14px;
font:400 15px/1.6 "Red Hat Mono",monospace;color:var(--ink);white-space:pre}
.call .s{color:#7C5530}
.ep{margin:0;padding-top:3px;font:400 14px/1.6 "Red Hat Mono",monospace;color:var(--ink);white-space:pre}
.note{margin:0;padding-top:4px;max-width:44ch;font-size:14px;line-height:1.45;color:var(--ink-2)}
.note code{font-size:13px;color:var(--ink)}
.detail{padding:34px 0 64px}
.lede{margin:0;max-width:58ch;font-size:17.5px;line-height:1.6;color:var(--ink)}
.uses{list-style:none;margin:0;padding:0}
.uses li{display:grid;grid-template-columns:250px minmax(0,1fr);column-gap:40px;padding:12px 0 13px;border-top:1px solid var(--rule-ink)}
.uses li:last-child{border-bottom:1px solid var(--rule-ink)}
.uses h3{font-family:"Hanken Grotesk",sans-serif;font-size:16px;font-weight:650;line-height:1.45}
.uses p{margin:0;font-size:15.5px;line-height:1.5;color:var(--ink-2)}
.uses code{font-size:14px;color:var(--ink)}
.gap{height:44px}

/* silver */
.silver{background:var(--silver-tint);padding-top:66px;padding-bottom:72px}
.src{margin:4px 0 16px;font-size:15px;color:var(--ink-2)}
.src code{font-size:14px;color:var(--ink)}
.schema{border-collapse:collapse;width:100%;font-size:14.5px}
.schema th,.schema td{text-align:left;padding:8px 16px 8px 0;border-top:1px solid var(--rule-ink);vertical-align:baseline;line-height:1.4}
.schema thead th{font-size:14px;font-weight:600;color:var(--ink);border-top:0;padding-top:0}
.schema tbody tr:last-child td{border-bottom:1px solid var(--rule-ink)}
.schema .cn{font:400 14.5px "Red Hat Mono",monospace;color:var(--ink);width:228px}
.schema .ty{font:400 13.5px "Red Hat Mono",monospace;color:var(--ink-2);width:170px}
.schema td{color:var(--ink-2)}
.schema td code{font-size:13.5px;color:var(--ink)}
.schema .grp th{padding:20px 0 8px;font:italic 400 14.5px "Hanken Grotesk",sans-serif;color:var(--ink);border-top:0}
.dfw{display:inline-block;max-width:100%;box-sizing:border-box;background:var(--daylight);border:1.5px solid var(--ink);border-radius:4px;padding:10px 10px 12px}
.df{border-collapse:collapse;font:400 13px/1 "Hanken Grotesk",sans-serif;font-variant-numeric:tabular-nums;color:var(--ink)}
.df th,.df td{padding:7px 9px;text-align:right;white-space:nowrap}
.df thead th{font-weight:600;border-bottom:1px solid var(--ink);vertical-align:bottom}
.df tbody th{font-weight:600}
.df tbody tr:nth-child(odd){background:var(--zebra)}
.df .nul{color:var(--muted)}
.cavs{list-style:none;margin:0;padding:0;max-width:66ch}
.cavs li{padding:12px 0 13px;border-top:1px solid var(--rule-ink);font-size:16px;line-height:1.6;color:var(--ink-2)}
.cavs li:last-child{border-bottom:1px solid var(--rule-ink)}
.cavs strong{font-weight:650;color:var(--ink)}
.cavs code{font-size:14.5px;color:var(--ink)}

/* the deep */
.deep{background:var(--petrol);color:var(--on-petrol);padding-top:70px;padding-bottom:0}
.dfoot{padding-top:64px;padding-bottom:30px}
.deep .row>h2{color:var(--on-petrol)}
.rel{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:48px;row-gap:22px}
.rel a{font:500 17px/1.3 "Red Hat Mono",monospace;color:var(--on-petrol);text-decoration-color:var(--chartreuse)}
.rel p{margin:5px 0 0;font-size:15px;line-height:1.5;color:var(--on-petrol-2)}
.rel code{font-size:13.5px;color:var(--on-petrol)}
.foot{display:flex;justify-content:space-between;align-items:baseline;padding:22px 0 0;border-top:1px solid var(--rule-petrol);
font-size:14.5px;color:var(--on-petrol-2)}
.foot .brand{font-size:20px;color:var(--on-petrol)}
.foot ul{display:flex;gap:26px;list-style:none;margin:0;padding:0}
.foot a{text-decoration:none}
.foot a:hover{color:var(--on-petrol)}
.rot{transform-box:fill-box;transform-origin:center;animation:spin 17s linear infinite}
.sp2{animation-duration:13s}
.sp3{animation-duration:21s}
@keyframes spin{to{transform:rotate(360deg)} }
@media (prefers-reduced-motion: reduce){.rot{animation:none} }
"""

NAV = ["Home", "Data sources", "Architecture", "Models", "About"]


def page(sp: dict) -> str:
    nav = "".join(f'<li><a href="#"{" aria-current=\"page\"" if n == "Data sources" else ""}>{n}</a></li>' for n in NAV)
    mast = (f'<header class="mast"><a class="brand" href="#">gridflow</a>'
            f'<nav aria-label="Primary"><ul>{nav}</ul></nav></header>')
    title = (f'<div class="title"><nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="#">Data sources</a></li>'
             f'<li><a href="#">{esc(sp["vendor"])}</a></li></ol></nav>'
             f'<div class="head"><h1>{esc(sp["h1"])}</h1><p class="pn">{esc(sp["key"])}</p></div>'
             f'<p class="one">{esc(sp["one"])}</p></div>{land(sp["asset"])}')
    facts = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in sp["facts"])
    ways = []
    for kind, lab, val, note in sp["get"]:
        if kind == "gold":
            body = f'<pre class="call">{hl_call(val)}</pre>'
        else:
            body = f'<pre class="ep">{esc(val)}</pre>'
        nt = f'<p class="note">{note}</p>' if note else ""
        ways.append(f'<dt>{swatch(kind)}<span class="lab">{lab}</span></dt><dd>{body}{nt}</dd>')
    plate = (f'<div class="plate">'
             f'<figure class="fig" aria-labelledby="fig-h"><h2 id="fig-h">{esc(sp["fig_h"])}</h2>{sp["fig"]}'
             f'<figcaption>{sp["cap"]}</figcaption></figure>'
             f'<section aria-labelledby="kf-h"><h2 id="kf-h">Key facts</h2><dl class="facts">{facts}</dl></section></div>'
             f'<section class="row get" aria-labelledby="get-h"><h2 id="get-h">How to get it</h2>'
             f'<dl class="ways">{"".join(ways)}</dl></section>')
    uses = "".join(f"<li><h3>{esc(t)}</h3><p>{d}</p></li>" for t, d in sp["uses"])
    detail = (f'<div class="detail"><section class="row" aria-labelledby="what-h"><h2 id="what-h">What it is</h2>'
              f'<p class="lede">{esc(sp["what"])}</p></section><div class="gap"></div>'
              f'<section class="row" aria-labelledby="use-h"><h2 id="use-h">How it’s used</h2>'
              f'<ul class="uses">{uses}</ul></section></div>')
    # schema
    main_rows = [r for r in sp["schema"] if r[0] not in LINEAGE]
    lin_rows = [r for r in sp["schema"] if r[0] in LINEAGE]

    def tr(r: tuple[str, str, str]) -> str:
        return f'<tr><td class="cn">{r[0]}</td><td class="ty">{r[1]}</td><td>{r[2]}</td></tr>'

    dropped = ", ".join(r[0] for r in lin_rows)
    schema = (f'<section class="row" aria-labelledby="sch-h"><h2 id="sch-h">Schema</h2><div>'
              f'<p class="src">{sp["schema_src"]}</p>'
              f'<table class="schema"><thead><tr><th>column</th><th>type</th><th>meaning</th></tr></thead>'
              f'<tbody>{"".join(tr(r) for r in main_rows)}</tbody>'
              f'<tbody><tr class="grp"><th colspan="3">Lineage, added by the base silver transformer; '
              f'<code>query()</code> and <code>tail()</code> drop these</th></tr>{"".join(tr(r) for r in lin_rows)}</tbody>'
              f'</table></div></section>')
    cols = sp["sample_cols"]
    head = "<tr><th></th>" + "".join(f"<th>{c}</th>" for c in cols) + "</tr>"
    body = "".join(f"<tr><th>{i}</th>" + "".join(f"<td>{fmt(r[c])}</td>" for c in cols) + "</tr>"
                   for i, r in enumerate(sp["sample"]))
    sample = (f'<section class="row" aria-labelledby="smp-h"><h2 id="smp-h">Sample rows</h2><div>'
              f'<p class="src">{esc(sp["sample_cap"])}</p>'
              f'<div class="dfw"><table class="df"><thead>{head}</thead><tbody>{body}</tbody></table></div></div></section>')
    cav = "".join(f"<li><strong>{esc(a)}</strong> {b}</li>" for a, b in sp["caveats"])
    caveats = (f'<section class="row" aria-labelledby="cav-h"><h2 id="cav-h">Caveats</h2>'
               f'<ul class="cavs">{cav}</ul></section>')
    rel = "".join(f'<li><a href="#">{esc(k)}</a><p>{d}</p></li>' for k, d in sp["related"])
    related = (f'<section class="row" aria-labelledby="rel-h"><h2 id="rel-h">Related datasets</h2>'
               f'<ul class="rel">{rel}</ul></section>')
    foot = (f'<footer class="foot"><a class="brand" href="#">gridflow</a>'
            f'<ul><li><a href="#">Source on GitHub</a></li><li>MIT license</li></ul></footer>')

    body = "\n".join([
        f'<div class="sky">{mast}</div>',
        '<main>',
        f'<div class="sky">{title}</div>',
        f'<div class="band soil">{texture("soil", "p-soil")}{plate}{bedding(1.4)}{detail}</div>',
        f'<div class="band silver">{texture("diag", "p-diag")}{edge(T_SILVER, "diag", "p-diag-e", 2.1, label="silver")}'
        f'{schema}<div class="gap"></div>{sample}<div class="gap"></div>{caveats}</div>',
        f'<div class="band deep">{texture("granite", "p-gran")}{edge(PETROL, "granite", "p-gran-e", 4.0, sw=2)}'
        f'{related}</div>',
        '</main>',
        f'<div class="band deep dfoot">{texture("granite", "p-gran-f")}{foot}</div>',
    ])
    H = HEIGHTS.get(sp["slug"], 4000)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{esc(sp["title"])}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{g.FONTS}
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


def check(out: str) -> None:
    import re
    body_only = out.split('<script type="text/x-dc"')[0]
    assert "{{" not in body_only and "}}" not in body_only, "template-hole syntax in markup"
    assert "/>" not in re.sub(r"<(meta|link|br)[^>]*>", "", body_only), "self-closing tag"
    assert "—" not in body_only, "em dash"
    assert "data:" not in body_only.replace("data: ", ""), "data URI"
    ids = re.findall(r'id="([^"]+)"', body_only)
    dup = {i for i in ids if ids.count(i) > 1}
    assert not dup, f"duplicate ids {dup}"


if __name__ == "__main__":
    (HERE / "static").mkdir(exist_ok=True)
    for build in (spec_fuelhh, spec_prices, spec_flows, spec_units):
        sp = build()
        out = page(sp)
        check(out)
        (OUT / f"E-{sp['slug']}.dc.html").write_text(out, encoding="utf-8")
        (HERE / "static" / f"E-{sp['slug']}.html").write_text(g.static(out), encoding="utf-8")
        print(sp["slug"], HEIGHTS.get(sp["slug"], 4000))
