"""Models page, round 1 of the polish, designer 1: "Quiet sections".

Round-1 A's sky, landscape and four cables, almost unchanged. Below ground the page goes quiet: silver shows only the
dataset codes each cable taps; gold holds one calm entry per model in the order of the chain (heading, one line, one
fact line, everything else behind a closed disclosure). Fundamentals SMP sits alone under the row, where two short
lines meet it: residual demand, drawn from the three recorded datasets (never from the forecast models), and the
supply curve from the stack.

Every fact comes from ``models-pack`` (MODELS-PACK.md / pack.json). Lines that are not pack wording go through ``N()``
and are written to ``copy-new.json``.

Usage: gen.py [desktop] [phone]     probe (headless Chrome on 127.0.0.1:9787, serving ./static), then write boards
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
DL = HERE.parent.parent
A_DIR = DL / "p27-r1" / "A"
sys.dont_write_bytecode = True           # never write caches into round-1 A's folder
sys.path.insert(0, str(A_DIR))

import frame  # noqa: E402
import hp  # noqa: E402
import p_models as pa  # noqa: E402
import scenery as sn  # noqa: E402
from hp import _frange, f, smooth  # noqa: E402

PACK = json.loads((DL / "models-pack" / "pack.json").read_text(encoding="utf-8"))
M = {m["id"]: m for m in PACK["models"]}

PORT = 9787
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
W, PW = 1440, 390
S = 750                                   # desktop ground surface (A's sky height)

PETROL, HORIZON, CHART, OLIVE = frame.PETROL, frame.HORIZON, frame.CHART, frame.OLIVE
INK, DAY, CLAY, KHAKI = frame.INK, frame.DAY, frame.CLAY, frame.KHAKI
BRONZE, SILVER, GOLD = frame.BRONZE, frame.SILVER, frame.GOLD
T_GOLD, T_SILVER, T_BRONZE, T_TOP = frame.T_GOLD, frame.T_SILVER, frame.T_BRONZE, frame.T_TOP
FAR = "#297382"

GM = "https://github.com/EBentham/gridflow-models/blob/main/"
GMT = "https://github.com/EBentham/gridflow-models/tree/main/"
NAV = [("Home", "index.html"), ("Data sources", "data-sources.html"), ("Architecture", "architecture.html"),
       ("Models", "models.html"), ("About", "index.html#about")]
GH_REPO = "https://github.com/EBentham/gridflow"

NEW: list[str] = []


def N(s: str) -> str:
    """Register a line of copy that is not pack wording (for the notes)."""
    NEW.append(s)
    return s


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def mn(s: str) -> str:
    """True minus signs in visible numbers."""
    return re.sub(r"(?<![\w/])-(?=\d)", "\u2212", s)


# =============================================================== content
CARDS = {
    "day_ahead.lgbm_demand.v1": "docs/MODEL_CARDS/day_ahead_lgbm_demand_v1.md",
    "day_ahead.lgbm_demand.v2": "docs/MODEL_CARDS/day_ahead_lgbm_demand_v2.md",
    "wind.lgbm_quantile.v1": "docs/MODEL_CARDS/wind_lgbm_quantile_v1.md",
    "solar.lgbm_quantile.v1": "docs/MODEL_CARDS/solar_lgbm_quantile_v1.md",
    "stack.gb.v1": "docs/MODEL_CARDS/stack_gb_v1.md",
    "fundamentals_smp.gb.v1": "docs/MODEL_CARDS/fundamentals_smp_gb_v1.md",
}
# the datasets each cable taps in silver: pack inputs with cable true, in pack order
TAPS = {k: [i["dataset"] for i in M[k]["inputs"] if i["cable"]] for k in ("demand", "wind", "solar", "stack")}
ORDER = ["demand", "wind", "solar", "stack"]
KIND = {"demand": "demand", "wind": "wind", "solar": "solar", "stack": "stack"}
# residual demand: the three recorded datasets the published SMP run cleared (pack edges into Residual demand)
RESID = [e["from"] for e in PACK["chain"]["edges"] if e["to"] == "step_residual" and e["exercised_in_published_run"]]
NODE = {n["id"]: n["label"] for n in PACK["chain"]["nodes"]}
RESID = [NODE[r] for r in RESID]
EDGE = {(e["from"], e["to"]): e["label"] for e in PACK["chain"]["edges"]}
L_RESID = EDGE[("step_residual", "m_smp")]           # "residual demand"
L_CURVE = EDGE[("m_stack", "m_smp")]                 # "supply curve per half-hour"


def code(s: str, brk: bool = False) -> str:
    t = esc(s)
    if brk:
        t = t.replace("/", "/<wbr>")
    return f"<code>{t}</code>"


def idlink(mid: str) -> str:
    return f'<a href="{GM}{CARDS[mid]}">{code(mid)}</a>'


PLUS = ('<svg class="pl" width="10" height="10" viewBox="0 0 10 10" aria-hidden="true"><path d="M5 0.5 V9.5 M0.5 5 H9.5" '
        f'stroke="{INK}" stroke-width="1.6"></path></svg>')


def more(inner: str) -> str:
    return (f'<details class="more"><summary>{PLUS}<span>{N("How it works")}</span></summary>'
            f'<div class="dd">{inner}</div></details>')


def handles(hs: list[str]) -> str:
    return f'<p class="nb">{N("In a notebook:")} ' + ", ".join(code(h) for h in hs) + "</p>"


def entry_parts(k: str) -> tuple[str, str, str, str]:
    """(ids line, job line, fact line, disclosure) for one model."""
    m = M[k]
    ids = m["model_ids"]
    if k == "demand":
        land = idlink(ids[0]) + " " + f'<a href="{GM}{CARDS[ids[1]]}">{code("v2")}</a>'
    else:
        land = idlink(ids[0])
    job = m["job"]
    if k == "demand":
        s1, s2 = m["scores"]
        p1, p2 = s1["pinball_q0_5_mw"], s2["pinball_q0_5_mw"]
        fact = N(f"Version 1: median pinball {p1:.2f} MW in walk-forward backtests.")
        line = N(f"Median pinball, 1 September 2024 to 22 August 2026: version 1 {p1:.2f} MW, "
                 f"version 2 {p2:.2f} MW.")
        inner = (f'<p>{esc(m["method"])}</p>'
                 f'<p>{line} {esc(s2["caveat_copy"])}</p>'
                 f'<p>{esc(PACK["reading_scores"]["copy"].split(". ")[1])}.</p>'
                 + handles(m["handles"]))
    elif k in ("wind", "solar"):
        fact = m["output"]["copy"]
        inner = f'<p>{esc(m["method"])}</p>' + handles(m["handles"])
    elif k == "stack":
        fact = m["status_line"]
        inner = (f'<p>{esc(m["method"])}</p><p>{esc(m["output"]["copy"])}</p>' + handles(["models.stack.build(as_of)"]))
    else:  # smp
        fact = m["status_line"].split(". ", 1)[1]
        sc = m["scores"][0]
        cav = sc["caveat_copy"]
        run = N(f"Published run, 18 August to 3 September 2026: mean bias {sc['mean_bias_gbp_mwh']:.2f} GBP/MWh "
                f"and MAE {sc['mae_gbp_mwh']:.2f} GBP/MWh against elexon/mid (APXMIDP).")
        inner = (f'<p>{esc(m["method"])} {esc(PACK["opening"]["optional_capability_line"])}</p>'
                 f'<p>{esc(mn(run))} {esc(sc["note_copy"])}</p>'
                 f'<p>{" ".join(esc(mn(c)) for c in cav)}</p>'
                 + handles(m["handles"]))
    return land, esc(job), esc(mn(fact)), more(inner)


def article(i: int, k: str, cls: str = "") -> str:
    land, job, fact, dis = entry_parts(k)
    name = M[k]["name"]
    kind = "smp" if k == "smp" else KIND[k]
    return (f'<article class="model {cls}" data-t="m{i}" aria-labelledby="m{i}-h">'
            f'<p class="land">{land}</p>'
            f'<h2 id="m{i}-h">{pa.mark(kind)}<span>{esc(name)}</span></h2>'
            f'<p class="md">{job}</p><p class="fx">{fact}</p>{dis}</article>')


# =============================================================== page chrome
def masthead() -> str:
    li = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if n == "Models" else ""}>{n}</a></li>' for n, h in NAV)
    return (f'<header class="mast"><a class="brand" href="index.html">gridflow</a>'
            f'<nav aria-label="Primary"><ul>{li}</ul></nav></header>')


def footer() -> str:
    links = "".join(f'<li><a href="{h}">{n}</a></li>' for n, h in NAV[1:] + [("GitHub", GH_REPO)])
    return (f'<footer class="st st-deep" data-st="deep" data-section="foot"><div class="foot">'
            f'<a class="brand" href="index.html">gridflow</a><ul>{links}</ul>'
            f'<p>This site is MIT-licensed. gridflow is Apache-2.0.</p></div></footer>')


def hero() -> str:
    o = PACK["opening"]
    return (f'<div class="hero"><h1 id="h1">{esc(o["headline"]).replace("day-ahead", "<span class=\"nw\">day-ahead</span>")}</h1><div class="lede">'
            f'<p class="lead">{esc(o["lede"])}</p>'
            f'<p>{esc(o["chain_line"])}</p>'
            f'<p>{esc(o["scope"])}</p>'
            f'<p><a class="alt" href="{GMT}docs/MODEL_CARDS">{N("Read the model cards")}</a></p></div></div>')


def taps_desktop() -> str:
    cols = []
    for i, k in enumerate(ORDER):
        li = "".join(f'<li data-t="in{i}-{j}">{code(d, True)}</li>' for j, d in enumerate(TAPS[k]))
        cols.append(f"<ul>{li}</ul>")
    return (f'<div class="inputs" role="group" aria-label="{N("The datasets each model reads from silver")}">'
            + "".join(cols) + "</div>")


def taps_phone() -> str:
    li = ""
    for i, k in enumerate(ORDER):
        li += "".join(f'<li data-t="in{i}-{j}">{code(d, True)}</li>' for j, d in enumerate(TAPS[k]))
    return (f'<ul class="ptaps" role="group" aria-label="{N("The datasets each model reads from silver")}">'
            + li + "</ul>")


def resid_codes() -> str:
    return (f'<ul class="rc" aria-label="{N("Residual demand, from the recorded datasets")}">'
            + "".join(f'<li data-t="r{j}">{code(d, True)}</li>' for j, d in enumerate(RESID)) + "</ul>")


def body(m: dict, ph: bool) -> str:
    NEW.clear()
    sky_h = S if not ph else int(m.get("hero_b", 560)) + P_LAND
    rows = "".join(article(i, k) for i, k in enumerate(ORDER))
    sky = (f'<section class="sky" data-st="sky" data-section="opening" style="height: {sky_h}px" '
           f'aria-labelledby="h1">{masthead()}{hero()}</section>')
    inputs = (f'<div data-section="inputs"><div class="st st-top" data-st="topsoil" aria-hidden="true"></div>'
              f'<div class="st st-bronze" data-st="bronze" aria-hidden="true"></div>'
              f'<div class="st st-silver" data-st="silver">{taps_phone() if ph else taps_desktop()}</div></div>')
    gold = (f'<section class="st st-gold" data-st="gold" data-section="models" aria-label="{N("The models, in the order of the chain")}">'
            f'<div class="mgrid">{rows}<div class="conf" data-t="conf">{resid_codes()}</div>'
            f'{article(4, "smp", "smp")}</div></section>')
    out = "\n".join([sky, inputs, gold, footer()])
    if ph:
        def brk(mm: re.Match[str]) -> str:
            inner = mm.group(1)
            if len(inner.replace("<wbr>", "")) < 16:
                return mm.group(0)
            return "<code>" + re.sub(r"([_/.])(?!<wbr>)", r"\1<wbr>", inner) + "</code>"
        out = re.sub(r"<code>((?:[^<]|<wbr>)+)</code>", brk, out)
    return out


# =============================================================== drawing, shared
def strata(H: int, w: int, sky: float, surf: list[tuple[float, float]], contacts: list[tuple[str, float]],
           labels_x: float | None) -> str:
    """frame.strata_svg at any width (the petrol sky, the cut, each named band, the deep)."""
    surf_d = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in surf)
    root = surf_d + " " + " ".join(f"L{f(x)} {f(y + 9)}" for x, y in reversed(surf)) + " Z"
    tail = f" L{w + 40} {H + 10} L-40 {H + 10} Z"
    out = [f'<rect x="0" y="0" width="{w}" height="{f(sky + 60)}" fill="{PETROL}"></rect>',
           f'<path d="{surf_d}{tail}" fill="{T_TOP}"></path>',
           f'<path d="{surf_d}{tail}" fill="url(#p-soil)" opacity=".5"></path>']
    lines, deep = [], None
    for name, y in contacts:
        if name == "deep":
            deep = frame.rough(y)
            continue
        amp, seed = frame.SEEDS[name]
        d = smooth(frame.contact(y, amp, seed))
        pid, op = frame.PAT[name]
        out.append(f'<path d="{d}{tail}" fill="{frame.TINT[name]}"></path><path d="{d}{tail}" fill="url(#{pid})" '
                   f'opacity="{op}"></path>')
        lines.append(d)
    if deep:
        gd = smooth(deep)
        out.append(f'<path d="{gd}{tail}" fill="{PETROL}"></path><path d="{gd}{tail}" fill="url(#p-granite)" '
                   f'opacity=".5"></path>')
    out.append(f'<path d="{root}" fill="{OLIVE}"></path>')
    out.append(f'<path d="{surf_d}" stroke="{INK}" stroke-width="1.5" fill="none"></path>')
    out.append(f'<path d="{" ".join(lines)}" stroke="{INK}" stroke-width="1.5" fill="none"></path>')
    if deep:
        out.append(f'<path d="{smooth(deep)}" stroke="{INK}" stroke-width="2" fill="none" stroke-linejoin="round"></path>')
    if labels_x is not None:
        lab = "".join(f'<text x="{f(labels_x)}" y="{f(y + 30)}" text-anchor="end">{n}</text>'
                      for n, y in contacts if n != "deep")
        out.append(f'<g font-family="Hanken Grotesk" font-style="italic" font-size="14" fill="{INK}">{lab}</g>')
    return (f'<svg class="layer" width="{w}" height="{H}" viewBox="0 0 {w} {H}" aria-hidden="true">'
            f'<defs>{hp.PATTERNS}</defs>' + "\n".join(out) + "</svg>")


def cab(d: str, core: str) -> str:
    return frame.cable(d, core)


def seg_color(y0: float, y1: float, ys: float, yg: float, x: float) -> list[tuple[float, float, str]]:
    """Split a vertical run into bronze / silver / gold cores at the contacts."""
    c_bs, c_sg = frame.contact_y("silver", ys, x), frame.contact_y("gold", yg, x)
    out = []
    for a, b, col in ((y0, c_bs, BRONZE), (c_bs, c_sg, SILVER), (c_sg, y1, GOLD)):
        lo, hi = max(a, y0), min(b, y1)
        if hi > lo:
            out.append((lo, hi, col))
    return out


def label(x: float, y: float, s: str, anchor: str = "start", fill: str = INK) -> str:
    return f'<text x="{f(x)}" y="{f(y)}" text-anchor="{anchor}" fill="{fill}">{esc(s)}</text>'


def meet_lines(m: dict, lane_stack: float, t_smp: tuple[float, float], r: float, xr0: float,
               phone: bool) -> tuple[list[str], list[str], list[str]]:
    """The two short lines into Fundamentals SMP: residual demand from the recorded datasets, the stack's curve."""
    c, ends, labs = [], [], []
    tx, ty = t_smp
    # the stack's supply curve: from under the stack entry, down, then along to the SMP terminal
    sb = m["t"]["m3"][3]
    y0 = sb + 14
    d = (f"M{f(lane_stack)} {f(y0)} V{f(ty - r)} Q{f(lane_stack)} {f(ty)} {f(lane_stack - r)} {f(ty)} "
         f"H{f(tx)}")
    c.append(cab(d, GOLD))
    ends.append(frame.joint(lane_stack, y0))
    # residual demand: taps on the three recorded datasets, then along to the terminal
    rj = [m["t"][f"r{j}"] for j in range(len(RESID))]
    if phone:
        xs = xr0
        ya = rj[0][1] + 10
        d = f"M{f(xs)} {f(ya)} V{f(ty - r)} Q{f(xs)} {f(ty)} {f(xs + r)} {f(ty)} H{f(tx)}"
        c.append(cab(d, GOLD))
        for l, t, rr, b in rj:
            ends.append(frame.joint(xs, (t + b) / 2))
        labs.append(label(xs + 14, ty - 9, L_RESID))
        labs.append(label(lane_stack - 12, ty - 9, L_CURVE, "end"))
    else:
        x0 = rj[0][0] + 8
        c.append(cab(f"M{f(x0)} {f(ty)} H{f(tx)}", GOLD))
        for l, t, rr, b in rj:
            ends.append(frame.joint(l + 8, ty))
        labs.append(label(tx - 30, ty + 24, L_RESID, "end"))
        labs.append(label(lane_stack - 16, ty - 11, L_CURVE, "end"))
    ends.append(frame.terminal(tx, ty, T_GOLD))
    return c, ends, labs


# =============================================================== desktop drawing
LANES = [96, 416, 736, 1056]
ORIG = [184, 560, 796, 1180]


def draw_desktop(m: dict) -> tuple[str, int]:
    hp.Y["surf"] = S
    H = int(math.ceil(m["H"]))
    sec = m["secs"]
    yb, ys, yg, yd = sec["bronze"][0], sec["silver"][0], sec["gold"][0], sec["deep"][0]
    surf = [(x, hp.prof(x)) for x in range(-40, W + 41, 10)]
    bg = strata(H, W, S, surf, [("bronze", yb), ("silver", ys), ("gold", yg), ("deep", yd)], 1360)
    land, lab, aria = pa.landscape()
    land_svg = (f'<svg class="layer land-svg" width="{W}" height="{S + 16}" viewBox="0 0 {W} {S + 16}" role="img" '
                f'aria-label="{esc(aria)}">{land}<g class="lab">{lab}</g></svg>')
    c, ends = [], []
    for i, (x0, lx) in enumerate(zip(ORIG, LANES)):
        l, t, r, b = m["t"][f"m{i}"]
        tx, ty = lx, t
        pts = [(x0, hp.prof(x0) - 3), (x0, S + 10)]
        for k in range(1, 12):
            tt = k / 12
            s2 = tt * tt * (3 - 2 * tt)
            pts.append((x0 + (tx - x0) * s2, S + 10 + 66 * tt))
        pts.append((tx, S + 76))
        c_bs, c_sg = frame.contact_y("silver", ys, tx), frame.contact_y("gold", yg, tx)
        c.append(cab(smooth(pts) + f" V{f(c_bs)}", BRONZE))
        c.append(cab(f"M{f(tx)} {f(c_bs)} V{f(c_sg)}", SILVER))
        c.append(cab(f"M{f(tx)} {f(c_sg)} V{f(ty)}", GOLD))
        ends += [frame.sleeve(tx, c_bs, SILVER), frame.sleeve(tx, c_sg, GOLD)]
        k = 0
        while f"in{i}-{k}" in m["t"]:
            ends.append(frame.joint(tx, m["t"][f"in{i}-{k}"][1] + 11))
            k += 1
        ends.append(frame.terminal(tx, ty, T_GOLD))
    sl, st, sr, sbm = m["t"]["m4"]
    mc, me, ml = meet_lines(m, LANES[3], (LANES[2], st), 14, 0, False)
    c += mc
    ends += me
    lines = (f'<svg class="layer cab" width="{W}" height="{H}" viewBox="0 0 {W} {H}" aria-hidden="true">'
             + "".join(c) + "".join(ends) + f'<g class="lab">{"".join(ml)}</g></svg>')
    return bg + "\n" + land_svg + "\n" + lines, H


# =============================================================== phone drawing
P_LAND = 180                     # sky below the hero: the drawn strip, down to the surface
PLANES = [316, 332, 348, 364]
PORIG = [44, 115, 197, 318]
PTURN = [68, 52, 36, 20]         # depth below the surface where each cable turns into its lane (nested, no crossings)


def p_landscape(SP: float) -> tuple[str, str, str]:
    hp.Y["surf"] = SP
    p = []
    p.append(sn.ridge([(-20, SP - 126), (70, SP - 136), (160, SP - 126), (250, SP - 140), (330, SP - 130),
                       (410, SP - 134)], SP - 30, FAR))
    near = [(-20, SP - 104), (60, SP - 114), (140, SP - 108), (220, SP - 118), (300, SP - 106), (410, SP - 112)]
    p.append(sn.ridge(near, SP - 30, HORIZON))
    for i, (tx, hh) in enumerate([(60, 24), (220, 27), (300, 22)]):
        ty = {60: SP - 114, 220: SP - 118, 300: SP - 106}[tx]
        p.append(hp.turbine(tx, ty + 3, hh, hh * .5, ["sp2", "sp3", "sp1"][i], 29 * i + 5))
    top = [(-20, SP - 66), (100, SP - 72), (200, SP - 64), (300, SP - 70), (410, SP - 64)]
    p.append(sn.field(top, hp.prof, -20, 410, [[(-20, SP - 54), (200, SP - 58), (410, SP - 52)],
                                                [(-20, SP - 30), (200, SP - 34), (410, SP - 28)]]))
    # demand: a pylon into the substation
    pl = (8, hp.prof(8) - 1, .42)
    sub_x, sub_s = 22, .56
    sb = hp.prof(sub_x + 26)
    sub_svg, ends = hp.substation(sub_x, sb)
    ends = [(sub_x + (ex - sub_x) * sub_s, sb + (ey - sb) * sub_s) for ex, ey in ends]
    p.append(f'<g stroke="{INK}" fill="none" stroke-linecap="round" stroke-width="1.2">{hp.pylon(*pl)}</g>')
    p.append(hp.sc(sub_svg, sub_x, sb, sub_s))
    p.append(f'<path d="{hp.spans(hp.tips(*pl, 1), ends, 5)}" stroke="{INK}" stroke-width=".7" fill="none" '
             f'opacity=".85"></path>')
    # wind farm
    for i, (tx, hh) in enumerate([(100, 78), (132, 66)]):
        p.append(hp.turbine(tx, hp.prof(tx), hh, hh * .5, ["sp1", "sp2"][i], 25 + 40 * i))
    # solar farm, drawn at desktop scale and scaled down in place
    x0 = 158
    base = hp.prof(x0)
    p.append(hp.sc(sn.solar_farm_at(x0, x0 + 190, lambda x: base), x0, base, .44))
    # the plant fleet in merit order: biomass, nuclear, CCGT
    bx, bb = 252, hp.prof(262)
    p.append(f'<path d="M{f(bx)} {f(bb)} A10 10 0 0 1 {f(bx + 20)} {f(bb)} Z" fill="{BRONZE}" stroke="{INK}" '
             f'stroke-width="1"></path>')
    nb = hp.prof(300)
    p.append(hp.sc(sn.nuclear(276, nb), 276, nb, .42))
    p.append(hp.ccgt(348, hp.prof(360), .4))
    labs = [("substation", 44), ("wind farm", 115), ("solar farm", 197), ("power stations", 318)]
    lab = "".join(label(x, SP - 146, t, "middle", DAY) for t, x in labs)
    aria = pa.landscape()[2]
    return "\n".join(p), lab, aria


def draw_phone(m: dict) -> tuple[str, int]:
    H = int(math.ceil(m["H"]))
    sec = m["secs"]
    SP = sec["sky"][1]
    hp.Y["surf"] = SP
    yb, ys, yg, yd = sec["bronze"][0], sec["silver"][0], sec["gold"][0], sec["deep"][0]
    surf = [(x, hp.prof(x)) for x in range(-40, PW + 41, 10)]
    bg = strata(H, PW, SP, surf, [("bronze", yb), ("silver", ys), ("gold", yg), ("deep", yd)], None)
    land, lab, aria = p_landscape(SP)
    land_svg = (f'<svg class="layer land-svg" width="{PW}" height="{f(SP + 16)}" viewBox="0 0 {PW} {f(SP + 16)}" '
                f'role="img" aria-label="{esc(aria)}">{land}<g class="lab">{lab}</g></svg>')
    c, ends = [], []
    r = 8
    for i, (x0, lx, dy) in enumerate(zip(PORIG, PLANES, PTURN)):
        l, t, rr, b = m["t"][f"m{i}"]
        ty = t + 9
        yt = SP + dy
        d = (f"M{f(x0)} {f(hp.prof(x0) - 3)} V{f(yt - r)} Q{f(x0)} {f(yt)} {f(x0 + r)} {f(yt)} "
             f"H{f(lx - r)} Q{f(lx)} {f(yt)} {f(lx)} {f(yt + r)}")
        c_bs, c_sg = frame.contact_y("silver", ys, lx), frame.contact_y("gold", yg, lx)
        c.append(cab(d + f" V{f(c_bs)}", BRONZE))
        c.append(cab(f"M{f(lx)} {f(c_bs)} V{f(c_sg)}", SILVER))
        c.append(cab(f"M{f(lx)} {f(c_sg)} V{f(ty)}", GOLD))
        ends += [frame.sleeve(lx, c_bs, SILVER), frame.sleeve(lx, c_sg, GOLD)]
        k = 0
        while f"in{i}-{k}" in m["t"]:
            a = m["t"][f"in{i}-{k}"]
            ends.append(frame.joint(lx, (a[1] + a[3]) / 2))
            k += 1
        ends.append(frame.terminal(lx, ty, T_GOLD))
    sl, st, sr, sbm = m["t"]["m4"]
    mc, me, ml = meet_lines(m, PLANES[3], (176, st), 10, 24, True)
    c += mc
    ends += me
    lines = (f'<svg class="layer cab" width="{PW}" height="{H}" viewBox="0 0 {PW} {H}" aria-hidden="true">'
             + "".join(c) + "".join(ends) + f'<g class="lab">{"".join(ml)}</g></svg>')
    return bg + "\n" + land_svg + "\n" + lines, H


# =============================================================== CSS
CSS = """.hero{display:grid;grid-template-columns:700px 520px;column-gap:60px;margin-top:64px;align-items:start}
.lede p{max-width:56ch}
.nw{white-space:nowrap}
.st-top{height:92px}
.st-bronze{height:58px}
.inputs{display:grid;grid-template-columns:repeat(4,280px);column-gap:40px;padding:30px 0 30px}
.inputs ul{list-style:none;margin:0;padding:0 0 0 30px}
.inputs li{font-size:13px;line-height:1.35;padding:2px 0 6px;color:#1C2B22}
.inputs code,.rc code{font-size:13px;color:#1C2B22}
.mgrid{display:grid;grid-template-columns:repeat(4,280px);column-gap:40px;padding:76px 0 0;align-items:start}
.model .land{margin:0 0 12px;height:18px;padding-left:30px;font-size:13px;line-height:18px;transform:translateY(-9px);display:flex;gap:10px;white-space:nowrap}
.model .land code{font-size:13px}
.root .model .land a{color:#1C2B22}
.model h2{display:flex;align-items:center;gap:12px;font-size:23px;font-weight:720;font-stretch:90%;line-height:1.1;letter-spacing:-.01em;margin:0 0 10px}
.mk{display:block;flex:none}
.model .md{margin:0 0 12px;font-size:14.5px;line-height:1.55;color:#3F4A3B;max-width:58ch}
.model .fx{margin:0 0 14px;font-size:14.5px;line-height:1.5;color:#1C2B22;font-weight:600;max-width:58ch}
.more summary{display:inline-flex;align-items:center;gap:9px;cursor:pointer;list-style:none;font-size:14px;font-weight:600;color:#1C2B22;text-decoration:underline;text-decoration-color:#66793B;text-decoration-thickness:1.5px;text-underline-offset:4px}
.more summary::-webkit-details-marker{display:none}
.more summary:focus-visible{outline:2px solid #AFC64E;outline-offset:3px;border-radius:2px}
.more[open] .pl{transform:rotate(45deg)}
.more .dd{padding:10px 0 0}
.more .dd p{margin:0 0 10px;font-size:14px;line-height:1.55;color:#3F4A3B;max-width:58ch}
.more .dd code{font-size:12.5px;color:#1C2B22}
.conf{grid-column:1 / -1;height:96px;position:relative}
.rc{list-style:none;margin:0;padding:0;position:absolute;left:0;bottom:12px;display:flex;column-gap:48px;align-items:flex-end}
.rc li{padding:0 0 0 0;line-height:1.3}
.model.smp{grid-column:3 / span 2;padding-top:30px}
.model.smp h2{font-size:30px;font-stretch:88%;letter-spacing:-.015em}
.model.smp .land{transform:none;padding-left:0;margin:0 0 10px}
.model.smp .md,.model.smp .fx{font-size:15.5px}
.st-gold{padding-bottom:110px}
.cab .lab text{font-family:"Hanken Grotesk",sans-serif;font-style:italic;font-size:13.5px}
"""

# the phone board: root carries class "ph" (a fixed 390 root, so no @media)
PH_CSS = """.ph .sky{padding:0 16px}
.ph .mast{flex-wrap:wrap;row-gap:10px;padding-top:18px}
.ph .mast nav{flex:1 1 100%}
.ph .mast ul{flex-wrap:wrap;column-gap:18px;row-gap:2px}
.ph .hero{grid-template-columns:minmax(0,1fr);row-gap:18px;margin-top:34px}
.ph .hero h1{font-size:44px;line-height:.98}
.ph .lede{padding-top:0}
.ph .lede p{font-size:16.5px}
.ph .land-svg .lab text,.ph .cab .lab text{font-size:12.5px}
.ph .st{padding:0 16px}
.ph .st-top{height:92px}
.ph .st-bronze{height:44px}
.ph .ptaps{list-style:none;margin:0;padding:26px 94px 26px 0;text-align:right}
.ph .ptaps li{font-size:12px;line-height:1.3;padding:3px 0}
.ph .ptaps code{font-size:12px;color:#1C2B22}
.ph .mgrid{grid-template-columns:minmax(0,1fr);row-gap:44px;padding:60px 78px 0 0}
.ph .model .land{transform:none;padding-left:0;height:auto;white-space:normal;flex-wrap:wrap;margin:0 0 10px}
.ph .model h2{font-size:21px}
.ph .model .md,.ph .model .fx{font-size:14.5px}
.ph .conf{grid-column:1;height:auto;margin:4px -78px 0 0;padding:0 0 42px 20px}
.ph .rc{position:static;display:block}
.ph .rc li{padding:2px 0}
.ph .rc code{font-size:12px}
.ph .model.smp{grid-column:1;margin:-44px -78px 0 0;padding-top:26px}
.ph .model.smp h2{font-size:26px}
.ph .model.smp .md,.ph .model.smp .fx{font-size:15px}
.ph .st-gold{padding-bottom:80px}
.ph .foot{grid-template-columns:minmax(0,1fr);row-gap:14px;padding:36px 0 44px}
.ph .foot ul{flex-wrap:wrap;column-gap:18px;row-gap:6px}
.ph .foot p{margin-top:4px}
"""

PROBE = """<pre id="m"></pre><script>
window.addEventListener('load',function(){Promise.all(['760 86px "Bricolage Grotesque"','720 23px "Bricolage Grotesque"','400 16px "Hanken Grotesk"','600 16px "Hanken Grotesk"','italic 400 14px "Hanken Grotesk"','400 14px "Red Hat Mono"'].map(function(q){return document.fonts.load(q)})).then(function(){return document.fonts.ready}).then(function(){setTimeout(function(){
var root=document.querySelector('.root').getBoundingClientRect(),o={secs:{},t:{},sections:{},H:0,over:[]};
document.querySelectorAll('[data-st]').forEach(function(s){var r=s.getBoundingClientRect();o.secs[s.dataset.st]=[r.top-root.top,r.height];});
document.querySelectorAll('[data-section]').forEach(function(s){var r=s.getBoundingClientRect();o.sections[s.dataset.section]=[Math.round(r.top-root.top),Math.round(r.height)];});
document.querySelectorAll('[data-t]').forEach(function(e){var r=e.getBoundingClientRect();o.t[e.dataset.t]=[r.left-root.left,r.top-root.top,r.right-root.left,r.bottom-root.top];});
o.hero_b=document.querySelector('.hero').getBoundingClientRect().bottom-root.top;
o.H=Math.ceil(document.querySelector('main').getBoundingClientRect().bottom-root.top);
var LIM=__LIM__,RW=__RW__;
document.querySelectorAll('main p,main li,main h1,main h2,main dd,main dt,main pre,main figcaption,main summary').forEach(function(e){if(e.scrollWidth>e.clientWidth+1&&getComputedStyle(e).overflow!=='visible')o.over.push((e.className||e.tagName)+':'+e.textContent.slice(0,30));var r=e.getBoundingClientRect();if(r.width>0&&r.right-root.left>LIM+1&&!e.closest('.mast'))o.over.push('WIDE '+(e.className||e.tagName)+':'+Math.round(r.right-root.left)+':'+e.textContent.slice(0,30));if(r.width>0&&r.left-root.left<(RW-LIM)-1&&!e.closest('.mast'))o.over.push('LEFT '+(e.className||e.tagName)+':'+Math.round(r.left-root.left)+':'+e.textContent.slice(0,30));});
var bad=[];document.querySelectorAll('main *').forEach(function(e){if(e.closest('svg')&&e.tagName.toLowerCase()!=='svg')return;if(e.matches('svg.layer'))return;var r=e.getBoundingClientRect();if(r.width>0&&(r.right-root.left>RW+.5||r.left-root.left<-.5))bad.push((e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className||e.tagName)+':'+Math.round(r.left-root.left)+'..'+Math.round(r.right-root.left));});
o.outside=bad.slice(0,20);o.docW=document.documentElement.scrollWidth;
document.getElementById('m').textContent=JSON.stringify(o);},500);});});
</script>"""


def shell(inner: str, H: int, probe: bool, ph: bool) -> str:
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
    p = HERE / "static" / "_probe.html"
    p.write_text(frame.static(html_text), encoding="utf-8")
    out = None
    for attempt in range(3):
        try:
            out = subprocess.run([CHROME, "--headless=new", "--disable-gpu", f"--window-size={w},4000",
                                  "--virtual-time-budget=9000", "--dump-dom",
                                  f"http://127.0.0.1:{PORT}/_probe.html?v={time.time_ns()}"],
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
    w = PW if ph else W
    name = "1-models-390" if ph else "1-models"
    m1 = measure(shell(body({}, ph), 9000, True, ph), w)
    m2 = measure(shell(body(m1, ph), 9000, True, ph), w)
    layers, H = (draw_phone if ph else draw_desktop)(m2)
    out = shell(layers + "\n" + body(m1, ph), H, False, ph)
    frame.check(out)
    (HERE / f"{name}.dc.html").write_text(out, encoding="utf-8")
    (HERE / "static" / f"{name}.html").write_text(frame.static(out), encoding="utf-8")
    print(name, "H", H, "sections", m2["sections"])
    for k in ("over", "outside"):
        print(" ", k, m2.get(k))
    print("  docW", m2.get("docW"))
    return {"H": H, "sections": m2["sections"], "over": m2["over"], "outside": m2["outside"]}


def main() -> None:
    which = sys.argv[1:] or ["desktop", "phone"]
    meas = {}
    copy: list[str] = []
    for k in which:
        meas[k] = build(k == "phone")
        copy += NEW
    (HERE / "copy-new.json").write_text(json.dumps(list(dict.fromkeys(copy)), ensure_ascii=False, indent=1),
                                        encoding="utf-8")
    (HERE / "measure.json").write_text(json.dumps(meas, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
