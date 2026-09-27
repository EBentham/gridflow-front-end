"""Models page, round 2: design 2, "Converging cables", with the round 1 pick's three changes (models-decisions.md):
no orders, positions or P&L line, the notebook section replaced by one in-development line, no licence line in the foot.

The drawing carries the chain. Cables drop from the sky images (substation, wind farm, solar farm, the plant fleet)
through topsoil to the silver datasets they read. In gold, the demand, wind and solar cables split at the tap: a
gold-cored spur ends at the forecast model, and the recorded branch runs on in chartreuse, the three converging on
residual demand. The fleet cable feeds the merit-order stack. Residual demand and the supply curve meet at
fundamentals SMP. Each model's short text sits level beside its part as a keyed index; below the drawing there is
only one line saying the modelling is still in development.

Drawing rule (models-pack section 2): only edges exercised in a stored run are drawn. The price run's
residual-demand cables branch off the recorded datasets, never off the forecast models.

Every line comes from ``models-pack/pack.json`` (verbatim or shortened); lines that are not pack wording are
registered through ``N()`` and listed in ``copy-new.json``.

Usage: gen.py [desktop] [phone]   probe on 127.0.0.1:9733 (the design-loop root), then write the boards.
"""
from __future__ import annotations

import html
import json
import math
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
DL = HERE.parent
A_DIR = DL / "p27-r1" / "A"
sys.path.insert(0, str(A_DIR))

import frame  # noqa: E402
import hp  # noqa: E402
import scenery as sn  # noqa: E402
from hp import f, smooth  # noqa: E402

PACK = json.loads((DL / "models-pack" / "pack.json").read_text(encoding="utf-8"))
MD = {m["id"]: m for m in PACK["models"]}
OP = PACK["opening"]
# the pack's scope line minus its second sentence (orders, positions and P&L), cut in the round 1 pick
SCOPE = OP["scope"].split(". ")[0] + "."
assert SCOPE == "It produces forecasts and prices for research.", SCOPE

NAME = "models-r2"
PORT = 9733
URL = f"http://127.0.0.1:{PORT}/models-r2/static/"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
W, PW = 1440, 390
PH = False

PETROL, HORIZON, CHART, OLIVE = "#155A6E", "#3E8C97", "#AFC64E", "#66793B"
INK, DAY, CLAY, KHAKI = "#1C2B22", "#F6F4EC", "#C77E3C", "#A39A6A"
BRONZE, SILVER, GOLD = "#A5713C", "#9FADAB", "#C2A14A"
T_GOLD, T_SILVER, T_TOP = "#E9DDAF", "#DCE2DF", "#ECE8DA"
FAR, MIDR = "#297382", "#378390"

GM = "https://github.com/EBentham/gridflow-models/blob/main/"
CARD = {
    "day_ahead.lgbm_demand.v1": "docs/MODEL_CARDS/day_ahead_lgbm_demand_v1.md",
    "day_ahead.lgbm_demand.v2": "docs/MODEL_CARDS/day_ahead_lgbm_demand_v2.md",
    "wind.lgbm_quantile.v1": "docs/MODEL_CARDS/wind_lgbm_quantile_v1.md",
    "solar.lgbm_quantile.v1": "docs/MODEL_CARDS/solar_lgbm_quantile_v1.md",
    "stack.gb.v1": "docs/MODEL_CARDS/stack_gb_v1.md",
    "fundamentals_smp.gb.v1": "docs/MODEL_CARDS/fundamentals_smp_gb_v1.md",
}

NEW: list[str] = []
ALL: list[str] = []


def N(s: str) -> str:
    """Register a line of copy that is not pack wording (for the notes)."""
    NEW.append(s)
    return s


def esc(s: str) -> str:
    return html.escape(s, quote=False)


# =============================================================== chrome (as the locked architecture page)
NAV = [("Home", "index.html"), ("Data sources", "data-sources.html"), ("Architecture", "architecture.html"),
       ("Models", "models.html"), ("About", "index.html#about")]
GH_REPO = "https://github.com/EBentham/gridflow"


def masthead() -> str:
    cur = ' aria-current="page"'
    li = "".join(f'<li><a href="{h}"{cur if n == "Models" else ""}>{n}</a></li>' for n, h in NAV)
    return (f'<header class="mast"><a class="brand" href="index.html">gridflow</a>'
            f'<nav aria-label="Primary"><ul>{li}</ul></nav></header>')


def footer() -> str:
    links = "".join(f'<li><a href="{h}">{n}</a></li>' for n, h in NAV[1:] + [("GitHub", GH_REPO)])
    return (f'<footer class="st st-deep"><div class="foot"><a class="brand" href="index.html">'
            f'gridflow</a><ul>{links}</ul></div></footer>')


# =============================================================== drawn parts
def cab(d: str, core: str, s: float = 1.0) -> str:
    if core == CHART:
        return hp.cable(d, core, 5.2 * s, 2.3 * s)
    return hp.cable(d, core, 4.4 * s, 1.5 * s)


def terminal(x: float, y: float, tint: str = T_GOLD, r: float = 5.5) -> str:
    return (f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{tint}" stroke="{INK}" stroke-width="1.8"></circle>'
            f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r / 3)}" fill="{INK}"></circle>')


def joint(x: float, y: float, r: float = 4.6) -> str:
    return f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{INK}"></circle>'


def run(x0: float, y0: float, d: float, lane: float, y1: float, r: float = 12) -> str:
    """Down from (x0, y0) to depth d, across to lane, down to y1, with rounded corners."""
    if abs(x0 - lane) < .5:
        return f"M{f(x0)} {f(y0)} V{f(y1)}"
    r = min(r, abs(x0 - lane) / 2, (d - y0) / 2, (y1 - d) / 2 if y1 > d else r)
    s = -1 if lane < x0 else 1
    return (f"M{f(x0)} {f(y0)} V{f(d - r)} Q{f(x0)} {f(d)} {f(x0 + s * r)} {f(d)} H{f(lane - s * r)} "
            f"Q{f(lane)} {f(d)} {f(lane)} {f(d + r)} V{f(y1)}")


def plate(x: float, y: float, w: float, h: float, sw: float = 1.5) -> str:
    return (f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="3" fill="{DAY}" stroke="{INK}" '
            f'stroke-width="{sw}"></rect>')


FAN = {"demand": (OLIVE, ".42"), "wind": (HORIZON, ".45"), "solar": (CHART, ".75")}


def fan(kind: str, x: float, y: float, w: float, h: float, sw: float = 1.5) -> str:
    """A forecast, drawn: the median inside its spread of quantiles, on a plate. Schematic: no numbers."""
    ax, ay, aw, ah = x + .14 * w, y + .16 * h, .78 * w, .66 * h
    n = 40
    ts = [i / (n - 1) for i in range(n)]
    if kind == "demand":
        mid = [.62 - .34 * (.5 - .5 * math.cos(4 * math.pi * t + .5)) for t in ts]
        wid = [.07 + .03 * t for t in ts]
    elif kind == "wind":
        mid = [.52 - .2 * math.sin(2.1 * math.pi * t + .4) + .05 * math.sin(11 * t) for t in ts]
        wid = [.05 + .2 * t for t in ts]
    else:
        mid = [.9 - .72 * math.exp(-((t - .5) / .17) ** 2) for t in ts]
        wid = [.01 + .13 * math.exp(-((t - .5) / .2) ** 2) for t in ts]
    X = lambda t: ax + t * aw  # noqa: E731
    Y = lambda v: ay + v * ah  # noqa: E731
    up = [(X(t), Y(max(.02, m - wd))) for t, m, wd in zip(ts, mid, wid)]
    dn = [(X(t), Y(min(.98, m + wd))) for t, m, wd in zip(ts, mid, wid)]
    band = "M" + " L".join(f"{f(a)} {f(b)}" for a, b in up + dn[::-1]) + " Z"
    line = "M" + " L".join(f"{f(X(t))} {f(Y(m))}" for t, m in zip(ts, mid))
    col, op = FAN[kind]
    return (plate(x, y, w, h, sw) + f'<path d="{band}" fill="{col}" opacity="{op}"></path>'
            f'<path d="{line}" stroke="{INK}" stroke-width="{f(1.3 * sw / 1.5)}" fill="none"></path>'
            f'<path d="M{f(ax - .06 * w)} {f(ay - .04 * h)} V{f(ay + ah + .06 * h)} H{f(x + .96 * w)}" stroke="{INK}" '
            f'stroke-width="{f(max(.8, sw * .66))}" fill="none"></path>')


# the plant fleet in merit order, as in the sky: biomass, nuclear, CCGT, OCGT
STEPS = [(.18, .12, BRONZE, "1"), (.22, .24, PETROL, "1"), (.34, .52, CLAY, "1"), (.2, .86, CLAY, ".7")]


def stack(x: float, y: float, w: float, h: float, sw: float = 1.5, smp: bool = False) -> tuple[str, float, float]:
    """The merit-order stack, schematic (no numbers, no scales). With smp, residual demand crosses it and the price
    is read off at the crossing. Returns the svg, the crossing x and the price y."""
    ax, ay, aw, ah = x + .12 * w, y + .12 * h, .82 * w, .74 * h
    base = ay + ah
    out = [plate(x, y, w, h, sw)]
    cx = ax
    edge = f"M{f(ax)} {f(base)}"
    tops = []
    for fw, fh, col, op in STEPS:
        sw_ = fw * aw
        top = base - fh * ah
        out.append(f'<rect x="{f(cx)}" y="{f(top)}" width="{f(sw_)}" height="{f(fh * ah)}" fill="{col}" '
                   f'opacity="{op}"></rect>')
        edge += f" V{f(top)} H{f(cx + sw_)}"
        tops.append((cx, cx + sw_, top))
        cx += sw_
    out.append(f'<path d="{edge}" stroke="{INK}" stroke-width="{f(1.3 * sw / 1.5)}" fill="none" '
               f'stroke-linejoin="round"></path>')
    xc = yp = 0.0
    if smp:
        a, b, top = tops[2]
        xc = a + .55 * (b - a)
        yp = top
        out.append(f'<path d="M{f(xc)} {f(yp)} H{f(ax)}" stroke="{GOLD}" stroke-width="{f(2.2 * sw / 1.5)}"></path>'
                   f'<circle cx="{f(ax)}" cy="{f(yp)}" r="{f(2.6 * sw / 1.5)}" fill="{GOLD}" stroke="{INK}" '
                   f'stroke-width=".8"></circle>')
    out.append(f'<path d="M{f(ax - .05 * w)} {f(ay - .06 * h)} V{f(base)} H{f(x + .97 * w)}" stroke="{INK}" '
               f'stroke-width="{f(max(.8, sw * .66))}" fill="none"></path>')
    return "".join(out), xc, yp


def splice(cx: float, y: float, w: float, h: float, sw: float = 1.6) -> str:
    """The residual-demand splice: a sleeve that takes three cables in and lets one out."""
    return (f'<rect x="{f(cx - w / 2)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(h / 2)}" fill="{T_TOP}" '
            f'stroke="{INK}" stroke-width="{sw}"></rect>'
            f'<path d="M{f(cx - w / 4)} {f(y + 3)} V{f(y + h - 3)} M{f(cx + w / 4)} {f(y + 3)} V{f(y + h - 3)}" '
            f'stroke="{INK}" stroke-width=".9" opacity=".5"></path>')


def mk(kind: str) -> str:
    """A small mark copied from the drawing part an index entry names."""
    w, h = 48, 30
    if kind in FAN:
        inner = fan(kind, 1, 1, 46, 28, 1.2)
    elif kind == "stack":
        inner = stack(1, 1, 46, 28, 1.2)[0]
    elif kind == "smp":
        s, xc, yp = stack(1, 1, 46, 28, 1.2, smp=True)
        inner = s + f'<path d="M{f(xc)} 1 V{f(1 + .86 * 28)}" stroke="{INK}" stroke-width="3.2"></path>' \
                    f'<path d="M{f(xc)} 1 V{f(1 + .86 * 28)}" stroke="{CHART}" stroke-width="1.5"></path>'
    elif kind == "res":
        inner = (cab("M8 1 C8 9 18 8 18 15", CHART, .7) + cab("M24 1 V15", CHART, .7)
                 + cab("M40 1 C40 9 30 8 30 15", CHART, .7) + cab("M24 22 V29", CHART, .7)
                 + splice(24, 13, 34, 11, 1.3))
    else:  # a silver tap: a joint on a cable (phone index)
        inner = cab("M7 1 V29", SILVER, .8) + joint(7, 15, 3.6)
        w = 14
    return f'<svg class="mk" width="{w}" height="{h}" viewBox="0 0 {w} {h}" aria-hidden="true">{inner}</svg>'


# =============================================================== the keyed index
def links(ids: list[str]) -> str:
    return " ".join(f'<a href="{GM}{CARD[i]}"><code>{i}</code></a>' for i in ids)


def entries() -> list[tuple[str, str, str, list[str], list[str]]]:
    """(key, mark, name, lines [(cls, html)], model ids), in drawing order, top to bottom."""
    dm = MD["demand"]
    v1 = dm["scores"][0]
    cut_status = MD["stack"]["status_line"]
    return [
        ("dem", "demand", dm["name"],
         [("kl", dm["job"]),
          ("kf", N(f"Validated: median pinball {v1['pinball_q0_5_mw']:.2f} MW, 90% coverage {v1['coverage_90']:.3f} "
                   "(version 1, 1 September 2024 to 22 August 2026).")),
          ("kl", N("Version 2 adds weather from <code>open_meteo/historical_demand</code>."))],
         dm["model_ids"]),
        ("wind", "wind", MD["wind"]["name"],
         [("kl", MD["wind"]["job"]),
          ("kl", N("Weather from <code>open_meteo/historical_wind</code>."))],
         MD["wind"]["model_ids"]),
        ("solar", "solar", MD["solar"]["name"],
         [("kl", MD["solar"]["job"]),
          ("kl", N("Weather from <code>open_meteo/historical_solar</code>."))],
         MD["solar"]["model_ids"]),
        ("res", "res", N("Residual demand"),
         [("kl", N("Demand less wind and solar is residual demand.")),
          ("kf", OP["published_run_line"])],
         []),
        ("stack", "stack", MD["stack"]["name"],
         [("kl", MD["stack"]["job"]),
          ("kf", cut_status),
          ("kl", N("Fuel and carbon prices are synthetic."))],
         MD["stack"]["model_ids"]),
        ("smp", "smp", MD["smp"]["name"],
         [("kl", MD["smp"]["job"]),
          ("kf", N("It has nothing to fit."))],
         MD["smp"]["model_ids"]),
    ]


def entry_html(key: str, mark: str, name: str, lines: list[tuple[str, str]], ids: list[str], top: float) -> str:
    body = "".join(f'<p class="{c}">{t}</p>' for c, t in lines)
    lk = f'<p class="kk">{links(ids)}</p>' if ids else ""
    return (f'<li class="ke" data-h="{key}" style="top: {f(top)}px">{mk(mark)}<div><h2 class="kn">{name}</h2>'
            f'{body}{lk}</div></li>')


TAPS = [("t0", "elexon/indo"), ("t1", "elexon/fuelhh"), ("t2", "neso_data_portal/historic_generation_mix"),
        ("t3", "elexon/bmunits_reference"), ("t4", "elexon/remit"), ("t5", "elexon/fou2t14d")]


def tap_html(key: str, code: str, top: float) -> str:
    c = code.replace("/", "/<wbr>").replace("_generation", "_<wbr>generation")
    return (f'<li class="ke tap" data-h="{key}" style="top: {f(top)}px">{mk("tap")}<p class="kt"><code>{c}</code></p>'
            f'</li>')


def dev_line(top: float) -> str:
    """The one quiet line below the drawing, in the notebook section's old slot (Bobbo's wording choice)."""
    return (f'<p class="dev" data-h="dev" style="top: {f(top)}px">'
            f'{N("The modelling is still in development; this page will grow with it.")}</p>')


# =============================================================== layout: node levels from the measured index
def layout(h: dict, ph: bool) -> dict:
    g = lambda k, d: h.get(k, d)  # noqa: E731
    Y: dict = {}
    if not ph:
        GAP = 34
        Y["S"] = S = 300
        Y["CS"] = S + 112
        Y["T0"] = Y["CS"] + 46
        Y["CG"] = Y["T0"] + 106
        Y["D"] = Y["CG"] + 86
        Y["W"] = max(Y["D"] + 96, Y["D"] + g("dem", 180) + GAP)
        Y["Sl"] = max(Y["W"] + 96, Y["W"] + g("wind", 120) + GAP)
        Y["R"] = max(Y["Sl"] + 206, Y["Sl"] + g("solar", 120) + GAP)
        Y["K"] = max(Y["R"] + 96, Y["R"] + g("res", 120) + GAP)
        Y["M"] = max(Y["K"] + 150, Y["K"] + g("stack", 150) + GAP)
        Y["NB"] = max(Y["M"] + 180, Y["M"] + g("smp", 110) + 70)
        Y["Hd"] = Y["NB"] + g("dev", 24) + 76
    else:
        GAP = 26
        Y["S"] = S = 176
        Y["CS"] = S + 76
        t = Y["CS"] + 34
        for i in range(6):
            Y[f"t{i}"] = t
            t += max(26, g(f"t{i}", 20) + 10)
        Y["CG"] = t + 18
        Y["D"] = Y["CG"] + 56
        Y["W"] = max(Y["D"] + 50, Y["D"] + g("dem", 300) + GAP)
        Y["Sl"] = max(Y["W"] + 50, Y["W"] + g("wind", 220) + GAP)
        Y["R"] = max(Y["Sl"] + 96, Y["Sl"] + g("solar", 220) + GAP)
        Y["K"] = max(Y["R"] + 60, Y["R"] + g("res", 200) + GAP)
        Y["M"] = max(Y["K"] + 80, Y["K"] + g("stack", 260) + GAP)
        Y["NB"] = max(Y["M"] + 100, Y["M"] + g("smp", 200) + 44)
        Y["Hd"] = Y["NB"] + g("dev", 44) + 56
    return Y


# =============================================================== the ground, shared
def wave_d(y0: float, amp: float, seed: float, w: int) -> str:
    step = 120 if w > 500 else 60
    pts = [(x, y0 + amp * math.sin(x / (210 if w > 500 else 90) + seed)
            + amp * .45 * math.sin(x / (73 if w > 500 else 37) + seed * 2.3)) for x in range(-40, w + step + 41, step)]
    return smooth(pts)


def wave_y(y0: float, amp: float, seed: float, x: float, w: int) -> float:
    return (y0 + amp * math.sin(x / (210 if w > 500 else 90) + seed)
            + amp * .45 * math.sin(x / (73 if w > 500 else 37) + seed * 2.3))


def ground(Y: dict, w: int, prof, amp: tuple[float, float]) -> tuple[str, str]:
    """Topsoil from the cut, silver and gold from their contacts. Returns (fills, contact lines)."""
    S, Hd = Y["S"], Y["Hd"]
    surf = [(x, prof(x)) for x in range(-40, w + 41, 8 if w > 500 else 4)]
    surf_d = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in surf)
    tail = f" L{w + 40} {f(Hd + 10)} L-40 {f(Hd + 10)} Z"
    o = [f'<rect x="0" y="0" width="{w}" height="{f(S + 60)}" fill="{PETROL}"></rect>']
    fills = [f'<path d="{surf_d}{tail}" fill="{T_TOP}"></path><path d="{surf_d}{tail}" fill="url(#p-soil)" '
             f'opacity=".5"></path>']
    lines = []
    for y0, a, seed, fill, pid, op in ((Y["CS"], amp[0], 2.1, T_SILVER, "p-diag", ".22"),
                                       (Y["CG"], amp[1], 4.0, T_GOLD, "p-stip", ".26")):
        d = wave_d(y0, a, seed, w)
        fills.append(f'<path d="{d}{tail}" fill="{fill}"></path><path d="{d}{tail}" fill="url(#{pid})" '
                     f'opacity="{op}"></path>')
        lines.append(d)
    root = surf_d + " " + " ".join(f"L{f(x)} {f(y + (8 if w > 500 else 6))}" for x, y in reversed(surf)) + " Z"
    fills.append(f'<path d="{root}" fill="{OLIVE}"></path>')
    top = "".join(o + fills)
    ink = (f'<path d="{surf_d}" stroke="{INK}" stroke-width="1.5" fill="none"></path>'
           f'<path d="{" ".join(lines)}" stroke="{INK}" stroke-width="1.5" fill="none"></path>')
    return top, ink


# =============================================================== desktop drawing
LD, LW, LS, LF = 150, 300, 450, 800         # the four lanes below ground
ORIG = [184, 560, 760, 1200]                # where each cable leaves its image


def dprof(x: float) -> float:
    return hp.prof(x)


def landscape_desk(S: float) -> tuple[str, str]:
    """The sky of round-1 A, kept: pylons into a substation, a wind farm, a solar farm and the plant fleet."""
    hp.Y["surf"] = S
    p = []
    p.append(sn.ridge([(-20, S - 250), (160, S - 280), (360, S - 262), (560, S - 286), (760, S - 258), (960, S - 276),
                       (1160, S - 250), (1320, S - 270), (1460, S - 256)], S - 60, FAR))
    near = [(-20, S - 214), (110, S - 238), (250, S - 246), (400, S - 226), (560, S - 250), (720, S - 232),
            (880, S - 214), (1040, S - 228), (1220, S - 208), (1460, S - 220)]
    p.append(sn.ridge(near, S - 60, HORIZON))
    for i, (tx, ty) in enumerate(near[2:6]):
        hgt = [56, 62, 54, 60][i]
        p.append(hp.turbine(tx, ty + 3, hgt, hgt * .5, ["sp2", "sp3", "sp1"][i % 3], 29 * i + 5))
    top = [(-20, S - 142), (200, S - 150), (420, S - 138), (640, S - 148), (860, S - 136), (1080, S - 146),
           (1280, S - 134), (1460, S - 140)]
    p.append(sn.field(top, hp.prof, -20, 1460,
                      [[(-20, S - 116), (400, S - 120), (900, S - 110), (1460, S - 114)],
                       [(-20, S - 84), (500, S - 90), (1000, S - 80), (1460, S - 86)],
                       [(-20, S - 48), (600, S - 52), (1200, S - 44), (1460, S - 48)]]))
    pl1 = (58, hp.prof(58) - 2, .62)
    sub_x, sub_s = 128, 1.1
    sb = hp.prof(sub_x + 50)
    sub_svg, ends = hp.substation(sub_x, sb)
    ends = [(sub_x + (ex - sub_x) * sub_s, sb + (ey - sb) * sub_s) for ex, ey in ends]
    p.append(f'<g stroke="{INK}" fill="none" stroke-linecap="round" stroke-width="1.35">{hp.pylon(*pl1)}</g>')
    p.append(hp.sc(sub_svg, sub_x, sb, sub_s))
    wires = [hp.spans([(-20, S - 146), (-20, S - 160), (-20, S - 172)], hp.tips(*pl1, -1), 6),
             hp.spans(hp.tips(*pl1, 1), ends, 9)]
    p.append(f'<path d="{" ".join(wires)}" stroke="{INK}" stroke-width=".8" fill="none" opacity=".85"></path>')
    for i, (tx, hh) in enumerate([(468, 150), (560, 136), (640, 124)]):
        p.append(hp.turbine(tx, hp.prof(tx), hh, hh * .5, ["sp1", "sp2", "sp3"][i], 25 + 40 * i))
    p.append(sn.solar_farm_at(690, 900, hp.prof))
    bx, bb = 944, hp.prof(980)
    for dx, r in ((0, 22), (50, 22)):
        p.append(f'<path d="M{f(bx + dx)} {f(bb)} A{r} {r} 0 0 1 {f(bx + dx + 2 * r)} {f(bb)} Z" fill="{BRONZE}" '
                 f'stroke="{INK}" stroke-width="1"></path>'
                 f'<path d="M{f(bx + dx + 6)} {f(bb - 8)} A{r - 6} {r - 8} 0 0 1 {f(bx + dx + 2 * r - 6)} {f(bb - 8)}" '
                 f'stroke="{DAY}" stroke-width=".8" opacity=".35" fill="none"></path>')
    p.append(sn.nuclear(1052, hp.prof(1110)))
    p.append(hp.ccgt(1222, hp.prof(1260), .92))
    ox, ob = 1360, hp.prof(1380)
    p.append(f'<rect x="{ox}" y="{f(ob - 18)}" width="44" height="18" fill="{CLAY}" stroke="{INK}" stroke-width=".9"></rect>'
             f'<rect x="{ox + 30}" y="{f(ob - 40)}" width="8" height="22" fill="{DAY}" stroke="{INK}" stroke-width=".9"></rect>'
             f'<path d="M{ox + 4} {f(ob - 11)} H{ox + 26}" stroke="{DAY}" stroke-width=".8" stroke-dasharray="3 3"></path>')
    labels = [("substation", 184, S - 72, "middle"), ("wind farm", 384, S - 98, "end"),
              ("solar farm", 796, S - 74, "middle"), ("biomass", 990, S - 50, "middle"),
              ("nuclear", 1100, S - 88, "middle"), ("CCGT", 1250, S - 120, "middle"), ("OCGT", 1360, S - 58, "end")]
    lab = "".join(f'<text x="{x}" y="{f(y)}" text-anchor="{a}">{t}</text>' for t, x, y, a in labels)
    return "\n".join(p), lab


def draw_aria() -> str:
    return N("Section drawing of the models. Above ground: pylons into a substation for national demand, a wind farm, "
             "a solar farm, and the plant fleet in merit order (biomass, nuclear, CCGT and OCGT). A cable drops from "
             "each to the silver datasets it reads: elexon/indo, elexon/fuelhh and "
             "neso_data_portal/historic_generation_mix, and for the fleet elexon/bmunits_reference, elexon/remit and "
             "elexon/fou2t14d. In gold, the demand, wind and solar cables each split: one branch ends at its forecast "
             "model, the other carries the recorded values on, and the three meet as residual demand. The fleet cable "
             "ends at the GB merit-order stack. Residual demand and the stack's supply curve meet at fundamentals SMP, "
             "where the price is read off.")


def drawing_desk(Y: dict) -> str:
    S, CS, T0, CG, Hd = Y["S"], Y["CS"], Y["T0"], Y["CG"], Y["Hd"]
    hp.Y["surf"] = S
    land, sky_lab = landscape_desk(S)
    top, ink = ground(Y, W, dprof, (8, 7))
    o = [top, land, ink]
    lab: list[str] = []
    lanes = [LD, LW, LS, LF]
    # ---- topsoil: each cable down from its image, across to its lane (nested, none cross)
    for i, (x0, lane) in enumerate(zip(ORIG, lanes)):
        o.append(cab(run(x0, dprof(x0) + 12, S + 36 + 13 * i, lane, wave_y(CS, 8, 2.1, lane, W)), BRONZE))
    # ---- silver: the datasets each cable taps
    for lane in lanes:
        o.append(cab(f"M{lane} {f(wave_y(CS, 8, 2.1, lane, W))} V{f(wave_y(CG, 7, 4.0, lane, W))}", SILVER))
    taps = [(LD, T0, "elexon/indo"), (LW, T0, "elexon/fuelhh"), (LS, T0, "neso_data_portal/"),
            (LF, T0, "elexon/bmunits_reference"), (LF, T0 + 27, "elexon/remit"), (LF, T0 + 54, "elexon/fou2t14d")]
    for x, y, code in taps:
        o.append(joint(x, y))
        lab.append(f'<text x="{x + 14}" y="{f(y + 4.5)}" class="m">{code}</text>')
    lab.append(f'<text x="{LS + 14}" y="{f(T0 + 21)}" class="m">historic_generation_mix</text>')
    # ---- gold: spurs to the forecasts; the recorded branches converge on residual demand
    yR, yK, yM = Y["R"], Y["K"], Y["M"]
    sp_w, sp_h = 88, 54
    parts = []
    for lane, key, kind in ((LD, "D", "demand"), (LW, "W", "wind"), (LS, "Sl", "solar")):
        yp = Y[key]
        ys = yp - 42
        o.append(cab(f"M{lane} {f(wave_y(CG, 7, 4.0, lane, W))} V{f(ys)}", CHART))
        o.append(cab(run(lane, ys, ys + 16, lane + 50, yp, 10), GOLD))
        parts.append(fan(kind, lane + 24, yp, sp_w, sp_h))
        parts.append(terminal(lane + 50, yp))
        parts.append(joint(lane, ys))
    # the recorded branches, down past the forecasts and into the splice
    SW, SH = 76, 22
    yc = yR + 4
    o.append(cab(f"M{LD} {f(Y['D'] - 42)} V{f(yc - 92)} C{LD} {f(yc - 40)} {LW - 20} {f(yc - 52)} {LW - 20} {f(yc + 2)}",
                 CHART))
    o.append(cab(f"M{LW} {f(Y['W'] - 42)} V{f(yc + 2)}", CHART))
    o.append(cab(f"M{LS} {f(Y['Sl'] - 42)} V{f(yc - 92)} C{LS} {f(yc - 40)} {LW + 20} {f(yc - 52)} {LW + 20} "
                 f"{f(yc + 2)}", CHART))
    ly = yc - 104
    lab += [f'<text x="{LD + 12}" y="{f(ly)}">recorded demand</text>',
            f'<text x="{LW + 12}" y="{f(ly)}">recorded wind</text>',
            f'<text x="{LS + 12}" y="{f(ly)}">recorded solar</text>']
    # SMP plate, the residual cable into it, the stack and its supply curve
    mx, mw, mh = 476, 204, 112
    smp_svg, xc, yprice = stack(mx, yM, mw, mh, smp=True)
    base = yM + .12 * mh + .74 * mh
    o.append(cab(run(LW, yc + SH - 2, yM - 36, xc, base, 12), CHART))
    lab.append(f'<text x="{LW + 12}" y="{f(yc + SH + 32)}">residual demand</text>')
    kx, kw, kh = LF - 78, 156, 76
    o.append(cab(f"M{LF} {f(wave_y(CG, 7, 4.0, LF, W))} V{f(yK)}", CHART))
    sx = mx + mw - 30
    o.append(cab(run(LF, yK + kh, yM - 36, sx, yM, 12), CHART))
    lab.append(f'<text x="{LF - 12}" y="{f((yK + kh + yM - 36) / 2 + 4)}" text-anchor="end">'
               f'supply curve per half-hour</text>')
    lab.append(f'<text x="{mx - 10}" y="{f(yprice + 4)}" text-anchor="end">{N("price")}</text>')
    parts.append(splice(LW, yc, SW, SH))
    parts.append(stack(kx, yK, kw, kh)[0])
    parts.append(terminal(LF, yK))
    parts.append(smp_svg)
    # the residual cable runs on into the plate as the demand line; the supply curve lands on its terminal
    parts.append(cab(f"M{f(xc)} {f(yM - 2)} V{f(base)}", CHART))
    parts.append(terminal(sx, yM))
    parts.append(terminal(xc, base, T_TOP, 4.6))
    # sleeves where the cables cross a contact
    for lane in lanes:
        parts.append(frame.sleeve(lane, wave_y(CS, 8, 2.1, lane, W), T_SILVER))
        parts.append(frame.sleeve(lane, wave_y(CG, 7, 4.0, lane, W), T_GOLD))
    for i, x0 in enumerate(ORIG):
        parts.append(terminal(x0, dprof(x0) + 12, "#E2CDB3"))
    return (f'<svg class="dr" width="{W}" height="{f(Hd)}" viewBox="0 0 {W} {f(Hd)}" role="img" '
            f'aria-label="{draw_aria()}"><defs>{hp.PATTERNS}</defs>\n' + "\n".join(o + parts)
            + f'\n<g class="lab sky">{sky_lab}</g><g class="lab">' + "".join(lab) + "</g></svg>")


# =============================================================== phone drawing (redrawn, not scaled)
PL = [24, 66, 108, 152]
PORIG = [40, 104, 190, 300]


def pprof_for(S: float):
    return lambda x: S + 2 * math.sin(x / 60 + .6) - 1.2 * math.sin(x / 27 + 1.3)


def landscape_phone(S: float) -> tuple[str, str]:
    pprof = pprof_for(S)
    p: list[str] = []
    p.append(sn.ridge([(-20, S - 96), (70, S - 108), (160, S - 98), (250, S - 110), (330, S - 100), (410, S - 106)],
                      S - 30, FAR))
    near = [(-20, S - 78), (60, S - 88), (140, S - 92), (220, S - 82), (300, S - 90), (410, S - 84)]
    p.append(sn.ridge(near, S - 30, HORIZON))
    for i, (tx, ty) in enumerate(near[1:5]):
        hgt = [26, 30, 24, 28][i]
        p.append(hp.turbine(tx, ty + 2, hgt, hgt * .5, ["sp2", "sp3", "sp1", "sp2"][i], 29 * i + 5))
    fld = [(-20, S - 56), (90, S - 60), (200, S - 54), (300, S - 60), (410, S - 56)]
    p.append(sn.field(fld, pprof, -20, 410, [[(-20, S - 40), (200, S - 42), (410, S - 38)],
                                             [(-20, S - 20), (220, S - 22), (410, S - 18)]]))
    hp.Y["surf"] = S
    sub_svg, _e = hp.substation(10, pprof(40))
    p.append(hp.sc(sub_svg, 10, pprof(40), .5))
    for i, (tx, hh) in enumerate([(84, 64), (106, 58), (126, 52)]):
        p.append(hp.turbine(tx, pprof(tx), hh, hh * .5, ["sp1", "sp2", "sp3"][i], 25 + 40 * i))
    farm = sn.solar_farm_at(0, 120, lambda _x: 0.0)
    p.append(f'<g transform="translate(152 {f(pprof(190))}) scale(.62)">{farm}</g>')
    bb = pprof(240)
    for bx in (228, 244):
        p.append(f'<path d="M{bx} {f(bb)} A8 8 0 0 1 {bx + 16} {f(bb)} Z" fill="{BRONZE}" stroke="{INK}" '
                 f'stroke-width=".8"></path>')
    p.append(hp.sc(sn.nuclear(266, pprof(290)), 266, pprof(290), .4))
    p.append(hp.sc(hp.ccgt(330, pprof(344), .92), 330, pprof(344), .4))
    ob = pprof(372)
    p.append(f'<rect x="362" y="{f(ob - 8)}" width="20" height="8" fill="{CLAY}" stroke="{INK}" stroke-width=".7"></rect>'
             f'<rect x="375" y="{f(ob - 18)}" width="4" height="10" fill="{DAY}" stroke="{INK}" stroke-width=".7"></rect>')
    labs = [("substation", 16, S - 124, "start", 32, S - 30), ("wind farm", 110, S - 140, "middle", 110, S - 60),
            ("solar farm", 190, S - 124, "middle", 190, S - 44), ("power stations", 306, S - 140, "middle", 306, S - 44)]
    lab = "".join(f'<text x="{x}" y="{f(y)}" text-anchor="{a}" class="v">{t}</text>' for t, x, y, a, _lx, _ly in labs)
    lead = " ".join(f"M{lx} {f(y + 6)} V{f(ly)}" for _t, _x, y, _a, lx, ly in labs)
    p.append(f'<path d="{lead}" stroke="{DAY}" stroke-width=".8" opacity=".75"></path>')
    return "\n".join(p), lab


def drawing_phone(Y: dict) -> str:
    S, CS, CG, Hd = Y["S"], Y["CS"], Y["CG"], Y["Hd"]
    pprof = pprof_for(S)
    land, sky_lab = landscape_phone(S)
    top, ink = ground(Y, PW, pprof, (5, 5))
    o = [top, land, ink]
    parts: list[str] = []
    k = .78
    for i, (x0, lane) in enumerate(zip(PORIG, PL)):
        o.append(cab(run(x0, pprof(x0) + 9, S + 18 + 9 * i, lane, wave_y(CS, 5, 2.1, lane, PW), 8), BRONZE, k))
    for lane in PL:
        o.append(cab(f"M{lane} {f(wave_y(CS, 5, 2.1, lane, PW))} V{f(wave_y(CG, 5, 4.0, lane, PW))}", SILVER, k))
    for i, lane in enumerate([PL[0], PL[1], PL[2], PL[3], PL[3], PL[3]]):
        parts.append(joint(lane, Y[f"t{i}"] + 9, 3.8))
    yR, yK, yM = Y["R"], Y["K"], Y["M"]
    fw, fh = 34, 22
    for lane, key, kind in ((PL[0], "D", "demand"), (PL[1], "W", "wind"), (PL[2], "Sl", "solar")):
        yp = Y[key] + 4
        ys = yp - 26
        o.append(cab(f"M{lane} {f(wave_y(CG, 5, 4.0, lane, PW))} V{f(ys)}", CHART, k))
        o.append(cab(run(lane, ys, ys + 10, lane + 16, yp, 6), GOLD, k))
        parts.append(fan(kind, lane + 5, yp, fw, fh, 1.2))
        parts.append(terminal(lane + 16, yp, T_GOLD, 3.8))
        parts.append(joint(lane, ys, 3.6))
    SW, SH = 46, 14
    yc = yR + 6
    o.append(cab(f"M{PL[0]} {f(Y['D'] - 22)} V{f(yc - 56)} C{PL[0]} {f(yc - 24)} {PL[1] - 12} {f(yc - 30)} "
                 f"{PL[1] - 12} {f(yc + 2)}", CHART, k))
    o.append(cab(f"M{PL[1]} {f(Y['W'] - 22)} V{f(yc + 2)}", CHART, k))
    o.append(cab(f"M{PL[2]} {f(Y['Sl'] - 22)} V{f(yc - 56)} C{PL[2]} {f(yc - 24)} {PL[1] + 12} {f(yc - 30)} "
                 f"{PL[1] + 12} {f(yc + 2)}", CHART, k))
    mx, mw, mh = 44, 104, 60
    smp_svg, xc, _yp = stack(mx, yM + 4, mw, mh, 1.3, smp=True)
    base = yM + 4 + .12 * mh + .74 * mh
    o.append(cab(run(PL[1], yc + SH - 2, yM - 16, xc, base, 7), CHART, k))
    kx, kw, kh = 88, 58, 34
    ky = yK + 4
    o.append(cab(run(PL[3], wave_y(CG, 5, 4.0, PL[3], PW), ky - 16, 130, ky, 6), CHART, k))
    sx = mx + mw - 14
    o.append(cab(run(130, ky + kh, yM - 16, sx, yM + 4, 6), CHART, k))
    parts.append(splice(PL[1], yc, SW, SH, 1.3))
    parts.append(stack(kx, ky, kw, kh, 1.3)[0])
    parts.append(terminal(130, ky, T_GOLD, 3.8))
    parts.append(smp_svg)
    parts.append(cab(f"M{f(xc)} {f(yM + 2)} V{f(base)}", CHART, k))
    parts.append(terminal(sx, yM + 4, T_GOLD, 3.8))
    parts.append(terminal(xc, base, T_TOP, 3.4))
    for lane in PL:
        cy = wave_y(CS, 5, 2.1, lane, PW)
        parts.append(hp.sc(frame.sleeve(lane, cy, T_SILVER), lane, cy, .6))
        cy = wave_y(CG, 5, 4.0, lane, PW)
        parts.append(hp.sc(frame.sleeve(lane, cy, T_GOLD), lane, cy, .6))
    for x0 in PORIG:
        parts.append(terminal(x0, pprof(x0) + 9, "#E2CDB3", 3.8))
    return (f'<svg class="dr drp" width="{PW}" height="{f(Hd)}" viewBox="0 0 {PW} {f(Hd)}" role="img" '
            f'aria-label="{draw_aria()}"><defs>{hp.PATTERNS}</defs>\n' + "\n".join(o + parts)
            + f'\n<g class="lab sky">{sky_lab}</g></svg>')


# =============================================================== page
def rough_edge(w: int) -> str:
    pts = [p for p in frame.rough(22) if p[0] <= w + 40]
    d = smooth(pts)
    return (f'<svg class="redge" width="{w}" height="44" viewBox="0 0 {w} 44" aria-hidden="true">'
            f'<defs>{hp.PATTERNS}</defs><path d="{d} L{w + 40} -4 L-40 -4 Z" fill="{T_GOLD}"></path>'
            f'<path d="{d} L{w + 40} -4 L-40 -4 Z" fill="url(#p-stip)" opacity=".26"></path>'
            f'<path d="{d}" stroke="{INK}" stroke-width="2" fill="none" stroke-linejoin="round"></path></svg>')


def body(h: dict, ph: bool = False) -> str:
    global PH
    PH = ph
    NEW.clear()
    Y = layout(h, ph)
    lis = [entry_html(k, m, n, ls, ids, Y[{"dem": "D", "wind": "W", "solar": "Sl", "res": "R", "stack": "K",
                                          "smp": "M"}[k]] - 5)
           for k, m, n, ls, ids in entries()]
    if ph:
        lis = [tap_html(k, c, Y[k]) for k, c in TAPS] + lis
    ov = (f'<div class="dov"><ul class="kidx" aria-label="{N("The models, keyed to the drawing")}">{"".join(lis)}</ul>'
          f'{dev_line(Y["NB"])}</div>')
    opening = (f'<section class="sky" data-section="opening">{masthead()}'
               f'<div class="hero"><h1>{OP["headline"].replace("day-ahead price", '<span class="nw">day-ahead price</span>')}</h1><div class="lede">'
               f'<p class="lead">{esc(OP["lede"])}</p><p>{esc(SCOPE)}</p></div></div></section>')
    drawing = (f'<section class="drawing" data-section="chain" aria-label="{N("The chain, in section")}">'
               f'{drawing_phone(Y) if ph else drawing_desk(Y)}{ov}</section>')
    gran = ('<svg class="gran" width="100%" height="100%" aria-hidden="true"><defs><pattern id="p-gran-d" width="46" '
            'height="40" patternUnits="userSpaceOnUse"><path d="M8 8 h8 M12 4 v8 M30 26 h8 M34 22 v8 M20 34 h6 M23 31 '
            f'v6 M40 6 h5 M42.5 3.5 v5" stroke="{HORIZON}" stroke-width="1.1"></path></pattern></defs>'
            '<rect width="100%" height="100%" fill="url(#p-gran-d)" opacity=".5"></rect></svg>')
    deep = f'<div class="deep" data-section="foot">{gran}{rough_edge(PW if ph else W)}{footer()}</div>'
    out = opening + drawing + deep
    if ph:
        def brk(mm: re.Match[str]) -> str:
            inner = mm.group(1)
            if len(inner.replace("<wbr>", "")) < 16 or "<wbr>" in inner:
                return mm.group(0)
            return "<code>" + re.sub(r"([_/.])", r"\1<wbr>", inner) + "</code>"
        out = re.sub(r"<code>((?:[^<]|<wbr>)+)</code>", brk, out)
    return out


CSS = """.sky{position:relative;box-sizing:border-box;padding:0 80px 18px;background:#155A6E}
.hero{display:grid;grid-template-columns:780px 440px;column-gap:60px;margin-top:64px;align-items:start}
.hero h1 .nw{white-space:nowrap}
.lede{padding-top:10px}
.drawing{position:relative;background:#155A6E}
.dr{display:block;overflow:visible}
.dr .lab text{font-family:"Hanken Grotesk",sans-serif;font-style:italic;font-size:13.5px;fill:#1C2B22}
.dr .lab text.m{font-family:"Red Hat Mono",monospace;font-style:normal;font-size:12.5px}
.dr .lab.sky text{font-size:13.5px}
.dov{position:absolute;left:0;top:0;width:1440px;height:0}
.kidx{list-style:none;margin:0;padding:0}
.ke{position:absolute;left:900px;width:460px;display:grid;grid-template-columns:48px minmax(0,1fr);column-gap:16px;margin:0}
.ke .mk{display:block;margin-top:0}
.root .kn{font-family:"Bricolage Grotesque",sans-serif;font-size:23px;font-weight:720;font-stretch:90%;line-height:1.1;letter-spacing:-.005em;margin:0 0 7px}
.kl{margin:0;font-size:14.5px;line-height:1.5;color:#3F4A3B;max-width:58ch}
.kl+.kl,.kf+.kl{margin-top:5px}
.kf{margin:6px 0 0;font-size:14.5px;line-height:1.5;font-weight:600;color:#1C2B22;max-width:58ch}
.kk{margin:7px 0 0;font-size:13px;line-height:1.5;display:flex;flex-wrap:wrap;column-gap:16px;row-gap:2px}
.kk code,.kl code{font-size:12.5px;color:#1C2B22}
.kk a{text-decoration-color:#66793B}
.dev{position:absolute;left:80px;width:560px;margin:0;font-size:15px;line-height:1.5;color:#3F4A3B}
.deep{position:relative;background:#155A6E;color:#F6F4EC;margin-top:-2px}
.deep .gran{position:absolute;left:0;top:0;z-index:0}
.deep>*:not(.gran){position:relative;z-index:1}
.redge{display:block}
.deep .st{position:relative;z-index:1}
.foot{border-top:0}
"""

PH_CSS = """.ph .sky{padding:0 16px 22px}
.ph .mast{flex-wrap:wrap;row-gap:10px;padding-top:18px}
.ph .mast nav{flex:1 1 100%}
.ph .mast ul{flex-wrap:wrap;column-gap:18px;row-gap:2px}
.ph .hero{grid-template-columns:minmax(0,1fr);row-gap:18px;margin-top:34px}
.ph .hero h1{font-size:44px;line-height:.98}
.ph .lede{padding-top:0}
.ph .lede p{font-size:16.5px}
.ph .dov{width:390px}
.ph .drp .lab text.v{fill:#F6F4EC;font-size:13px;font-weight:500}
.ph .ke{left:172px;width:202px;grid-template-columns:34px minmax(0,1fr);column-gap:8px}
.ph .ke .mk{width:34px;height:21px;margin-top:1px}
.ph .ke.tap{grid-template-columns:10px minmax(0,1fr);column-gap:8px}
.ph .ke.tap .mk{width:10px;height:21px;margin-top:0}
.ph .kt{margin:0;font-size:12px;line-height:1.45}
.ph .kt code{font-size:12px;color:#1C2B22}
.ph .kn{font-size:18px;margin-bottom:5px}
.ph .kl,.ph .kf{font-size:13.5px;line-height:1.45}
.ph .kk{column-gap:10px;font-size:12.5px}
.ph .kk code,.ph .kl code{font-size:12px}
.ph .kl,.ph .kn,.ph .kf{overflow-wrap:anywhere}
.ph .dev{left:16px;width:358px;font-size:14px;line-height:1.45}
.ph .st{padding:0 16px}
.ph .foot{grid-template-columns:minmax(0,1fr);row-gap:14px;padding:36px 0 44px}
.ph .foot ul{flex-wrap:wrap;column-gap:18px;row-gap:6px}
"""

PROBE = """<pre id="m"></pre><script>
window.addEventListener('load',function(){Promise.all(['760 86px "Bricolage Grotesque"','720 23px "Bricolage Grotesque"','400 16px "Hanken Grotesk"','600 16px "Hanken Grotesk"','italic 400 14px "Hanken Grotesk"','400 14px "Red Hat Mono"','500 14px "Red Hat Mono"'].map(function(q){return document.fonts.load(q)})).then(function(){return document.fonts.ready}).then(function(){setTimeout(function(){
var root=document.querySelector('.root').getBoundingClientRect(),o={h:{},secs:{},H:0,over:[],hit:[]};
document.querySelectorAll('[data-h]').forEach(function(e){o.h[e.dataset.h]=Math.ceil(e.getBoundingClientRect().height);});
document.querySelectorAll('[data-section]').forEach(function(s){var r=s.getBoundingClientRect();o.secs[s.dataset.section]=[Math.round(r.top-root.top),Math.round(r.height)];});
o.H=Math.ceil(document.querySelector('main').getBoundingClientRect().bottom-root.top);
var LIM=__LIM__,RW=__RW__;
document.querySelectorAll('main p,main li,main h1,main h2,main h3,main pre,main a').forEach(function(e){if(e.scrollWidth>e.clientWidth+1&&!e.matches('pre.well'))o.over.push((e.className||e.tagName)+':'+(e.scrollWidth-e.clientWidth)+':'+e.textContent.slice(0,40));var r=e.getBoundingClientRect();if(r.right-root.left>LIM+1&&!e.closest('.mast'))o.over.push('WIDE '+(e.className||e.tagName)+':'+Math.round(r.right-root.left)+':'+e.textContent.slice(0,30));if(r.left-root.left<(RW-LIM)-1)o.over.push('LEFT '+(e.className||e.tagName)+':'+Math.round(r.left-root.left)+':'+e.textContent.slice(0,30));});
var ks=[].slice.call(document.querySelectorAll('.ke,.dev'));for(var i=0;i<ks.length;i++)for(var j=i+1;j<ks.length;j++){var a=ks[i].getBoundingClientRect(),b=ks[j].getBoundingClientRect();if(a.left<b.right&&b.left<a.right&&a.top<b.bottom&&b.top<a.bottom)o.hit.push((ks[i].dataset.h)+'x'+(ks[j].dataset.h));}
var bad=[];document.querySelectorAll('.root *').forEach(function(e){if(e.closest('svg')&&e.tagName.toLowerCase()!=='svg')return;if(e.closest('pre.well')&&!e.matches('pre.well'))return;var r=e.getBoundingClientRect();if(r.width>0&&(r.right-root.left>RW+.5||r.left-root.left<-.5))bad.push((e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className||e.tagName)+':'+Math.round(r.left-root.left)+'..'+Math.round(r.right-root.left));});
o.outside=bad.slice(0,20);o.docW=document.documentElement.scrollWidth;
document.getElementById('m').textContent=JSON.stringify(o);},500);});});
</script>"""


def shell(inner: str, H: int, probe: bool, ph: bool = False) -> str:
    w = PW if ph else W
    css = CSS + PH_CSS if ph else CSS
    cls = "root ph" if ph else "root"
    pr = PROBE.replace("__LIM__", str(w - (16 if ph else 80))).replace("__RW__", str(w)) if probe else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Models</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{hp.FONTS}
<style>
{frame.BASE_CSS}{css}</style>
</helmet>
<div class="{cls}" style="width: {w}px; height: {H}px; overflow: hidden; position: relative">
<main>
{inner}
</main>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{H}}}}}'>
class Component extends DCLogic {{
renderVals() {{ return {{}}; }}
}}
</script>
{pr}</body>
</html>
"""


def measure(html_text: str, w: int) -> dict:
    (HERE / "static").mkdir(exist_ok=True)
    p = HERE / "static" / "_probe.html"
    p.write_text(frame.static(html_text), encoding="utf-8")
    for attempt in range(3):
        try:
            out = subprocess.run([CHROME, "--headless=new", "--disable-gpu", f"--window-size={w},4000",
                                  "--virtual-time-budget=9000", "--dump-dom", f"{URL}_probe.html?v={time.time_ns()}"],
                                 capture_output=True, text=True, encoding="utf-8", timeout=120)
            break
        except subprocess.TimeoutExpired:
            if attempt == 2:
                raise
    mm = re.search(r'<pre id="m">(.*?)</pre>', out.stdout, re.S)
    if not mm or not mm.group(1).strip():
        raise RuntimeError(f"probe failed: {out.stderr[-400:]}")
    p.unlink()
    return json.loads(html.unescape(mm.group(1)))


def build(ph: bool) -> dict:
    """Probe the index heights, lay the nodes out level with them, probe again, then write at the measured height."""
    w = PW if ph else W
    name = f"{NAME}-{PW}" if ph else NAME
    m1 = measure(shell(body({}, ph), 20000, True, ph), w)
    m2 = measure(shell(body(m1["h"], ph), 20000, True, ph), w)
    H = m2["H"]
    out = shell(body(m1["h"], ph), H, False, ph)
    frame.check(out)
    ALL.extend(NEW)
    (HERE / f"{name}.dc.html").write_text(out, encoding="utf-8")
    (HERE / "static" / f"{name}.html").write_text(frame.static(out), encoding="utf-8")
    print(name, "H", H, "h", m2["h"], "secs", m2["secs"])
    for k in ("over", "outside", "hit"):
        print(" ", k, m2.get(k))
    print("  docW", m2.get("docW"))
    if m1["h"] != m2["h"]:
        print("  WARNING index heights moved between passes", m1["h"], m2["h"])
    return {"h": m2["h"], "H": H, "Y": layout(m1["h"], ph)}


def main() -> None:
    which = sys.argv[1:] or ["desktop", "phone"]
    meas = {}
    for k in which:
        meas[k] = build(k == "phone")
    (HERE / "copy-new.json").write_text(json.dumps(list(dict.fromkeys(ALL)), ensure_ascii=False, indent=1),
                                        encoding="utf-8")
    (HERE / "measure.json").write_text(json.dumps(meas, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
