"""Models page, round 1 of the polish, designer 3: "One model in focus".

Round-1 A's sky and landscape stay as they were. The four cables drop through a short topsoil and nest into lanes
down the left gutter (the architecture page's arrangement); beside them the five models sit in chain order, one row
each. The demand row alone opens: its headline score and its one chart from the pack.

Chain topology follows the pack's drawing rule: the SMP's residual-demand cable forks off the demand, wind and solar
cables BEFORE their models (the recorded outturns, not the forecasts), so each forecast model is a dead end. Forks
are staggered: each one happens after the previous model's lane has ended, so no cable crosses another.

Usage: gen.py [desktop|phone ...]   (needs the design-loop folder served on 127.0.0.1:9733)
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
sys.path.insert(0, str(A_DIR))

import frame  # noqa: E402
import hp  # noqa: E402
import p_models as pa  # noqa: E402
import scenery as sn  # noqa: E402
from hp import f, smooth  # noqa: E402

PORT = 9733
PROBE_URL = f"http://127.0.0.1:{PORT}/models-r1/3/static/_probe.html"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
W, PW = 1440, 390
S = 750                                   # desktop ground line (A's sky height)

PETROL, HORIZON, CHART, OLIVE = "#155A6E", "#3E8C97", "#AFC64E", "#66793B"
INK, DAY, CLAY, KHAKI = "#1C2B22", "#F6F4EC", "#C77E3C", "#A39A6A"
BRONZE, SILVER, GOLD = "#A5713C", "#9FADAB", "#C2A14A"
T_GOLD, T_TOP = "#E9DDAF", "#ECE8DA"
FAR = "#297382"
OLIVE_D = "#4E5E2B"

PACK = json.loads((DL / "models-pack" / "pack.json").read_text(encoding="utf-8"))
MOD = {m["id"]: m for m in PACK["models"]}
SERIES = frame.PACK["series"]["models_landing_demand"]["points"]
CARD = {k: next(e["url"] for e in m["evidence"] if "MODEL_CARDS" in e["path"]) for k, m in MOD.items()}
CARDS_DIR = "https://github.com/EBentham/gridflow-models/tree/main/docs/MODEL_CARDS"

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


# =============================================================== content
# (id, mark, name, what it does, fed by [(code, role)])
ROWS = [
    ("demand", "demand", MOD["demand"]["name"], MOD["demand"]["job"],
     [("elexon/indo", "target"), ("open_meteo/historical_demand", "weather, version 2")]),
    ("wind", "wind", MOD["wind"]["name"], MOD["wind"]["job"],
     [("elexon/fuelhh", "target"), ("open_meteo/historical_wind", "weather")]),
    ("solar", "solar", MOD["solar"]["name"], MOD["solar"]["job"],
     [("neso_data_portal/historic_generation_mix", "target"), ("open_meteo/historical_solar", "weather")]),
    ("stack", "stack", MOD["stack"]["name"], MOD["stack"]["job"] + " " + MOD["stack"]["status_line"],
     [("elexon/bmunits_reference", "units"), ("elexon/remit", "availability"), ("elexon/fou2t14d", "derating")]),
    ("smp", "smp", MOD["smp"]["name"], MOD["smp"]["job"] + " " + MOD["smp"]["status_line"],
     [("elexon/indo", "recorded demand"), ("elexon/fuelhh", "recorded wind"),
      ("neso_data_portal/historic_generation_mix", "recorded solar"), ("stack.gb.v1", "supply curve per half-hour"),
      ("elexon/mid", "scored against")]),
]
ROLE_NEW = {"weather", "weather, version 2", "recorded wind"}   # shortened pack edge labels, listed as new


def masthead() -> str:
    cur = ' aria-current="page"'
    li = "".join(f'<li><a href="{h}"{cur if n == "Models" else ""}>{n}</a></li>' for n, h in NAV)
    return (f'<header class="mast"><a class="brand" href="index.html">gridflow</a>'
            f'<nav aria-label="Primary"><ul>{li}</ul></nav></header>')


def footer() -> str:
    links = "".join(f'<li><a href="{h}">{n}</a></li>' for n, h in NAV[1:] + [("GitHub", GH_REPO)])
    return (f'<footer class="st st-deep" data-st="deep" data-section="foot"><div class="foot"><a class="brand" '
            f'href="index.html">gridflow</a><ul>{links}</ul><p>This site is MIT-licensed. gridflow is Apache-2.0.</p>'
            f'</div></footer>')


def code(s: str, ph: bool) -> str:
    inner = esc(s)
    if ph or len(s) > 30:
        inner = re.sub(r"([_/.])", r"\1<wbr>", inner)
    return f"<code>{inner}</code>"


# =============================================================== the one chart
def demand_chart(ph: bool) -> str:
    pts = SERIES
    w, h = (270, 196) if ph else (764, 286)
    L, R, Tp, B = (40, 54, 18, 28) if ph else (52, 70, 18, 30)
    pw, ph_ = w - L - R, h - Tp - B
    n = len(pts)
    lo_v, hi_v = 16000, 32500
    X = lambda i: L + i * pw / (n - 1)  # noqa: E731
    Y = lambda v: Tp + (hi_v - v) * ph_ / (hi_v - lo_v)  # noqa: E731
    up = " L".join(f"{f(X(i))} {f(Y(p[4]))}" for i, p in enumerate(pts))
    dn = " L".join(f"{f(X(i))} {f(Y(p[2]))}" for i, p in reversed(list(enumerate(pts))))
    med = "M" + " L".join(f"{f(X(i))} {f(Y(p[3]))}" for i, p in enumerate(pts))
    act = "M" + " L".join(f"{f(X(i))} {f(Y(p[1]))}" for i, p in enumerate(pts))
    g = [f'<path d="M{up} L{dn} Z" fill="{OLIVE}" opacity=".3"></path>',
         f'<path d="{med}" fill="none" stroke="{OLIVE_D}" stroke-width="1.7"></path>',
         f'<path d="{act}" fill="none" stroke="{INK}" stroke-width="1.5"></path>']
    for v in (20000, 25000, 30000):
        lab = f"{v // 1000:,}k" if ph else f"{v:,}"
        g.append(f'<path d="M{L - 5} {f(Y(v))} H{L}" stroke="{INK}" stroke-width="1"></path>'
                 f'<text x="{L - 9}" y="{f(Y(v) + 4)}" text-anchor="end">{lab}</text>')
    ticks = ((0, "20 Aug"), (48, "21 Aug")) if ph else ((0, "20 Aug"), (24, "12:00"), (48, "21 Aug"), (72, "12:00"))
    for i, lab in ticks:
        g.append(f'<path d="M{f(X(i))} {Tp + ph_} v6" stroke="{INK}" stroke-width="1"></path>'
                 f'<text x="{f(X(i))}" y="{Tp + ph_ + 21}" text-anchor="{"start" if i == 0 else "middle"}">{lab}</text>')
    g.append(f'<path d="M{L} {Tp - 4} V{Tp + ph_} H{L + pw}" stroke="{INK}" stroke-width="1.2" fill="none"></path>')
    g.append(f'<text x="{L + 6}" y="{Tp + 2}" class="u">{"MW" if ph else "MW, UTC"}</text>')
    i0 = 60
    g.append(f'<text class="dl" x="{f(X(i0))}" y="{f(Y(pts[i0][4]) - 8)}" text-anchor="middle">5 to 95%</text>')
    ya, ym = Y(pts[-1][1]), Y(pts[-1][3])
    if abs(ya - ym) < 15:                      # keep the two end labels apart
        mid = (ya + ym) / 2
        ya, ym = (mid - 7.5, mid + 7.5) if ya < ym else (mid + 7.5, mid - 7.5)
    xe = X(n - 1) + 7
    g.append(f'<text class="dl" x="{f(xe)}" y="{f(ya + 4)}">{N("outturn")}</text>'
             f'<text class="dl" x="{f(xe)}" y="{f(ym + 4)}">{N("median")}</text>')
    lo = min(min(p[1:]) for p in pts)
    hi = max(max(p[1:]) for p in pts)
    aria = N(f"Line chart of GB national demand for 20 and 21 August 2026, in MW: the version 1 forecast median inside "
             f"its 5 to 95% band, with the outturn from elexon/indo. Values run from {lo:,.0f} to {hi:,.0f} MW.")
    return (f'<svg class="chart" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{aria}">'
            + "".join(g) + "</svg>")


def focus(ph: bool) -> str:
    """The one showcase: the demand model's headline score and its band chart, inside its own row."""
    sc = MOD["demand"]["scores"][0]
    rs = PACK["reading_scores"]["copy"].split(". ")
    defs = f"{rs[1]}. {rs[2]}."            # the two definitions only; no pass thresholds
    ch = PACK["charts"][0]
    score = (f'<div class="score"><p class="sv">{N("Version 1, from stored walk-forward backtests, 1 September 2024 to 22 August 2026.")}</p>'
             f'<dl><div><dt>{N("median pinball")}</dt><dd>{sc["pinball_q0_5_mw"]:.2f} MW</dd></div>'
             f'<div><dt>{N("90% coverage")}</dt><dd>{sc["coverage_90"]:.3f}</dd></div></dl>'
             f'<p class="sd">{esc(defs)}</p></div>')
    fig = (f'<figure class="fig"><h4>{esc(ch["title_copy"])}</h4>{demand_chart(ph)}'
           f'<figcaption>{esc(ch["caption_copy"])}</figcaption></figure>')
    return f'<div class="focus" data-t="focus">{score}{fig}</div>'


def row(i: int, ph: bool) -> str:
    mid, kind, name, job, fed = ROWS[i]
    fl = "".join(f'<li>{code(c, ph)} <span>{N(r) if r in ROLE_NEW else r}</span></li>' for c, r in fed)
    extra = focus(ph) if mid == "demand" else ""
    return (f'<li class="m m-{mid}" data-t="r{i}"><h3 data-t="n{i}">{pa.mark(kind)}<a href="{CARD[mid]}">{esc(name)}</a></h3>'
            f'<p class="job">{esc(job)}</p><ul class="fed" aria-label="{N("Fed by")}">{fl}</ul>{extra}</li>')


def body(ph: bool) -> str:
    NEW.clear()
    op = PACK["opening"]
    lede = (f'<p class="lead">{esc(op["lede"])}</p><p>{esc(op["scope"])}</p>'
            f'<p><a class="alt" href="{CARDS_DIR}">{N("Read the model cards")}</a></p>')
    land = '<div class="landsp" data-t="land" aria-hidden="true"></div>' if ph else ""
    hs = "" if ph else f' style="height: {S}px"'
    sky = (f'<section class="sky" data-st="sky" data-section="opening"{hs} '
           f'aria-labelledby="h1">{masthead()}<div class="hero"><h1 id="h1">{esc(op["headline"]).replace("day-ahead", '<span class="nw">day-ahead</span>')}</h1>'
           f'<div class="lede">{lede}</div></div>{land}</section>')
    top = f'<div class="st st-top" data-st="topsoil" style="height: {TOP_PH if ph else TOP}px" aria-hidden="true"></div>'
    silver = (f'<div class="st st-silver" data-st="silver"><div class="intro"><h2 class="big" id="h-chain">'
              f'{N("How the models connect")}</h2><p>{esc(op["chain_line"])}</p></div></div>')
    head = ('<div class="lh" aria-hidden="true"><span>Model</span><span>What it does</span><span>Fed by</span></div>'
            if not ph else "")
    for s in ("Model", "What it does", "Fed by"):
        if not ph:
            N(s)
    gold = (f'<div class="st st-gold" data-st="gold" data-section="models">{head}<ol class="chain" aria-label="{N("The models, in chain order")}">'
            + "".join(row(i, ph) for i in range(5)) + "</ol></div>")
    chain = (f'<section class="chain-s" aria-labelledby="h-chain"><div data-section="chain">{top}{silver}</div>'
             f'{gold}</section>')
    out = sky + chain + footer()
    return out


TOP, TOP_PH = 150, 118

# =============================================================== CSS
CSS = """.sky{padding:0 80px}
.hero{display:grid;grid-template-columns:780px 440px;column-gap:60px;margin-top:64px;align-items:start}
.lede{padding-top:12px}
.nw{white-space:nowrap}
.intro{margin-left:250px;padding:40px 0 44px}
.intro h2.big{margin:0 0 14px}
.intro p{margin:0;font-size:17px;line-height:1.6;color:#3F4A3B;max-width:58ch}
.st-gold{padding-top:34px;padding-bottom:104px}
.lh{margin-left:250px;display:grid;grid-template-columns:236px 414px 320px;column-gap:30px;padding:0 0 10px;font-size:13.5px;font-style:italic;color:#3F4A3B}
.chain{list-style:none;margin:0;padding:0}
.m{margin-left:250px;display:grid;grid-template-columns:236px 414px 320px;column-gap:30px;align-items:start;padding:20px 0 22px;border-top:1px solid rgba(28,43,34,.3)}
.m:last-child{border-bottom:1px solid rgba(28,43,34,.3)}
.m h3{display:flex;align-items:center;gap:11px;font-size:20px;font-weight:700;font-stretch:90%;line-height:1.2;letter-spacing:-.006em;margin:0}
.m h3 a{text-decoration-color:#66793B}
.job{margin:1px 0 0;font-size:15px;line-height:1.5;color:#3F4A3B}
.fed{list-style:none;margin:2px 0 0;padding:0}
.fed li{font-size:12.5px;line-height:1.4;padding:0 0 5px;color:#3F4A3B}
.fed code{font-size:12.5px;color:#1C2B22}
.fed span{font-style:italic}
.focus{grid-column:1 / -1;display:grid;grid-template-columns:236px minmax(0,1fr);column-gap:30px;margin:30px 0 8px;align-items:start}
.score{padding-top:4px}
.sv{margin:0 0 14px;font-size:14px;line-height:1.5;color:#3F4A3B}
.score dl{margin:0 0 16px}
.score dl div{padding:8px 0 9px;border-top:1px solid rgba(28,43,34,.3)}
.score dl div:last-child{border-bottom:1px solid rgba(28,43,34,.3)}
.score dt{font-size:14px;line-height:1.3;color:#3F4A3B}
.score dd{margin:2px 0 0;font-size:24px;line-height:1.2;font-weight:600;color:#1C2B22}
.sd{margin:0;font-size:13.5px;line-height:1.5;color:#3F4A3B}
.fig{margin:0}
.fig h4{font-family:"Bricolage Grotesque",sans-serif;font-optical-sizing:auto;font-size:18px;font-weight:700;font-stretch:92%;line-height:1.25;margin:0 0 12px;color:#1C2B22}
.fig figcaption{margin:8px 0 0;font-size:13.5px;line-height:1.5;color:#3F4A3B;max-width:66ch}
.chart text.u{font-size:12.5px}
"""

PH_CSS = """.ph .sky{padding:0 16px}
.ph .mast{flex-wrap:wrap;row-gap:10px;padding-top:18px}
.ph .mast nav{flex:1 1 100%}
.ph .mast ul{flex-wrap:wrap;column-gap:18px;row-gap:2px}
.ph .hero{grid-template-columns:minmax(0,1fr);row-gap:18px;margin-top:34px}
.ph .hero h1{font-size:44px;line-height:.98}
.ph .lede{padding-top:0}
.ph .lede p{font-size:16.5px}
.ph .landsp{height:176px}
.ph .st{padding:0 16px}
.ph .intro{margin-left:88px;padding:30px 0 34px}
.ph .intro h2.big{font-size:30px;line-height:1.08}
.ph .intro p{font-size:15.5px}
.ph .st-gold{padding-top:26px;padding-bottom:84px}
.ph .m{margin-left:88px;grid-template-columns:minmax(0,1fr);row-gap:8px;padding:16px 0 18px}
.ph .m h3{font-size:19px;gap:9px}
.ph .job{font-size:14.5px}
.ph .fed{margin-top:2px}
.ph .fed li,.ph .fed code{font-size:12.5px}
.ph .focus{grid-column:1;grid-template-columns:minmax(0,1fr);row-gap:22px;margin:18px 0 6px}
.ph .score dl{display:grid;grid-template-columns:1fr 1fr;column-gap:16px}
.ph .score dl div:last-child{border-bottom:0}
.ph .score dl{border-bottom:1px solid rgba(28,43,34,.3)}
.ph .score dd{font-size:21px}
.ph .fig h4{font-size:17px}
.ph .fig figcaption{font-size:13px}
.ph .foot{grid-template-columns:minmax(0,1fr);row-gap:14px;padding:36px 0 44px}
.ph .foot ul{flex-wrap:wrap;column-gap:18px;row-gap:6px}
.ph .foot p{margin-top:4px}
"""


# =============================================================== drawing
def geom(ph: bool) -> dict:
    if ph:
        return {"R": 22, "lanes": [38, 54, 70, 86], "smp": 54, "runs": [22, 42, 62, 82], "r": 8, "lab": 30}
    return {"R": 92, "lanes": [150, 196, 242, 288], "smp": 190, "runs": [28, 56, 84, 112], "r": 12, "lab": 102}


def run(x0: float, y0: float, d: float, lx: float, y1: float, r: float) -> str:
    """Down from a drawn asset, a rounded turn west at depth d, a rounded turn south onto lane lx, down to y1."""
    return (f"M{f(x0)} {f(y0)} V{f(d - r)} Q{f(x0)} {f(d)} {f(x0 - r)} {f(d)} H{f(lx + r)} "
            f"Q{f(lx)} {f(d)} {f(lx)} {f(d + r)} V{f(y1)}")


def phone_landscape(PS: float) -> tuple[str, str, list[float]]:
    """The four assets redrawn for 390: pylon and substation, a wind farm, a solar farm, the plant fleet."""
    p = []
    p.append(sn.ridge([(-10, PS - 118), (60, PS - 130), (140, PS - 122), (220, PS - 136), (300, PS - 120),
                       (400, PS - 130)], PS - 30, FAR))
    near = [(-10, PS - 98), (50, PS - 108), (120, PS - 112), (190, PS - 100), (260, PS - 110), (330, PS - 98),
            (400, PS - 104)]
    p.append(sn.ridge(near, PS - 30, HORIZON))
    top = [(-10, PS - 64), (100, PS - 68), (200, PS - 62), (300, PS - 67), (400, PS - 63)]
    p.append(sn.field(top, hp.prof, -10, 400,
                      [[(-10, PS - 50), (200, PS - 53), (400, PS - 49)], [(-10, PS - 30), (200, PS - 33), (400, PS - 29)]]))
    # demand: a pylon into the substation
    pl = (12, hp.prof(12) - 1, .4)
    sub_x, sub_s = 30, .62
    sb = hp.prof(sub_x + 30)
    sub_svg, ends = hp.substation(sub_x, sb)
    ends = [(sub_x + (ex - sub_x) * sub_s, sb + (ey - sb) * sub_s) for ex, ey in ends]
    p.append(f'<g stroke="{INK}" fill="none" stroke-linecap="round" stroke-width="1.2">{hp.pylon(*pl)}</g>')
    p.append(hp.sc(sub_svg, sub_x, sb, sub_s))
    p.append(f'<path d="{hp.spans(hp.tips(*pl, 1), ends, 5)}" stroke="{INK}" stroke-width=".7" fill="none" '
             f'opacity=".85"></path>')
    for i, (tx, hh) in enumerate([(116, 78), (146, 66)]):
        p.append(hp.turbine(tx, hp.prof(tx), hh, hh * .5, ["sp1", "sp2"][i], 25 + 50 * i))
    p.append(sn.solar_farm_at(172, 246, hp.prof))
    bb = hp.prof(262)
    p.append(f'<path d="M254 {f(bb)} A12 12 0 0 1 278 {f(bb)} Z" fill="{BRONZE}" stroke="{INK}" stroke-width="1"></path>')
    p.append(hp.sc(sn.nuclear(284, hp.prof(300)), 284, hp.prof(300), .46))
    p.append(hp.ccgt(348, hp.prof(360), .5))
    # labels sit in the petrol sky above the ridges, one row, each over its asset (on the ridge they fail AA)
    yl = PS - 146
    labels = [("substation", 58), ("wind farm", 133), ("solar farm", 209), ("power stations", 322)]
    lab = "".join(f'<text x="{x}" y="{f(yl)}" fill="{DAY}" text-anchor="middle">{N(t)}</text>' for t, x in labels)
    return "\n".join(p), lab, [60, 132, 209, 318]


def draw(m: dict, ph: bool) -> tuple[str, int]:
    g = geom(ph)
    w = PW if ph else W
    secs, t = m["secs"], m["t"]
    H = int(math.ceil(m["H"]))
    ys, yg, yd = secs["silver"][0], secs["gold"][0], secs["deep"][0]
    if ph:
        land_t = t["land"]
        Sg = land_t[3]
    else:
        Sg = S
    hp.Y["surf"] = Sg
    surf = [(x, hp.prof(x)) for x in range(-40, 1481, 10)]
    bg = frame.strata_svg(H, Sg, surf, [("silver", ys), ("gold", yg), ("deep", yd)], labels=not ph)
    if ph:
        land, lab, orig = phone_landscape(Sg)
        aria = N("The four things the models are about, drawn small: pylons into a substation, a wind farm, a solar "
                 "farm and power stations. A cable runs down from each to the model that reads its data.")
    else:
        land, lab, aria = pa.landscape()
        orig = pa.ORIG
    land_svg = (f'<svg class="layer land-svg" width="{w}" height="{f(Sg + 16)}" viewBox="0 0 {w} {f(Sg + 16)}" '
                f'role="img" aria-label="{esc(aria)}">{land}<g class="lab">{lab}</g></svg>')

    def mid(i: int) -> float:
        nl, nt, nr, nb = t[f"n{i}"]
        return (nt + nb) / 2

    rows = [t[f"r{i}"] for i in range(5)]
    r = g["r"]
    c, ends = [], []
    tops = [rw[1] for rw in rows]
    for i, (x0, lx) in enumerate(zip(orig, g["lanes"])):
        d = Sg + g["runs"][i]
        ym = mid(i)
        cs, cg = frame.contact_y("silver", ys, lx), frame.contact_y("gold", yg, lx)
        full = run(x0, hp.prof(x0) - 3, d, lx, cs, r)
        c.append(frame.cable(full, BRONZE))
        c.append(frame.cable(f"M{f(lx)} {f(cs)} V{f(cg)}", SILVER))
        c.append(frame.cable(f"M{f(lx)} {f(cg)} V{f(ym)}", GOLD))
        ends += [frame.sleeve(lx, cs, SILVER), frame.sleeve(lx, cg, GOLD)]
    # the recorded outturns fork off before each forecast model; the forecast models end there
    R = g["R"]
    y5 = mid(4)
    xs = g["smp"]
    forks = [tops[0] - 2, tops[1] - 2, tops[2] - 2]
    rpath = (f"M{f(g['lanes'][0])} {f(forks[0])} H{f(R + r)} Q{f(R)} {f(forks[0])} {f(R)} {f(forks[0] + r)} "
             f"V{f(y5 - 3.2 * r)} C{f(R)} {f(y5 - r)} {f(R + r)} {f(y5)} {f(xs - 7)} {f(y5)}")
    c.append(frame.cable(rpath, GOLD))
    for k in (1, 2):
        lx = g["lanes"][k]
        c.append(frame.cable(f"M{f(lx)} {f(forks[k])} H{f(R + r)} Q{f(R)} {f(forks[k])} {f(R)} {f(forks[k] + r)}",
                             GOLD))
        ends.append(frame.joint(R, forks[k] + r + 2))
    for k in range(3):
        ends.append(frame.joint(g["lanes"][k], forks[k]))
    # the stack's supply curve into the SMP
    sx = g["lanes"][3]
    y4 = mid(3)
    c.append(frame.cable(f"M{f(sx)} {f(y4)} V{f(y5 - 3.2 * r)} C{f(sx)} {f(y5 - r)} {f(sx - r)} {f(y5)} "
                         f"{f(xs + 7)} {f(y5)}", GOLD))
    for i in range(4):
        ends.append(frame.terminal(g["lanes"][i], mid(i), T_GOLD))
    ends.append(frame.terminal(xs, y5, T_GOLD, 7.5))
    # plate label on the residual-demand cable, between the stack's row and the SMP's row
    ly = tops[4] - (10 if ph else 12)
    N("residual demand")
    if ph:   # two lines, between the residual cable and the stack's cable
        labs = (f'<g class="plab"><text x="{f(R + 7)}" y="{f(ly - 16)}">residual</text>'
                f'<text x="{f(R + 7)}" y="{f(ly)}">demand</text></g>')
    else:
        labs = f'<g class="plab"><text x="{f(R + 12)}" y="{f(ly)}">residual demand</text></g>'

    cab = (f'<svg class="layer" width="{w}" height="{H}" viewBox="0 0 {w} {H}" aria-hidden="true">'
           + "".join(c) + "".join(ends) + labs + "</svg>")
    if ph:
        bg = bg.replace(f'width="{W}" height="{H}" viewBox="0 0 {W} {H}"', f'width="{PW}" height="{H}" '
                        f'viewBox="0 0 {PW} {H}"', 1)
    return bg + "\n" + land_svg + "\n" + cab, H


# =============================================================== shell, probe, build
PROBE = """<pre id="m"></pre><script>
window.addEventListener('load',function(){Promise.all(['760 86px "Bricolage Grotesque"','720 42px "Bricolage Grotesque"','400 16px "Hanken Grotesk"','600 16px "Hanken Grotesk"','italic 400 14px "Hanken Grotesk"','400 14px "Red Hat Mono"','500 14px "Red Hat Mono"'].map(function(q){return document.fonts.load(q)})).then(function(){return document.fonts.ready}).then(function(){setTimeout(function(){
var root=document.querySelector('.root').getBoundingClientRect(),o={secs:{},t:{},sec:{},H:0,over:[]};
document.querySelectorAll('[data-st]').forEach(function(s){var r=s.getBoundingClientRect();o.secs[s.dataset.st]=[r.top-root.top,r.height];});
document.querySelectorAll('[data-section]').forEach(function(s){var r=s.getBoundingClientRect();o.sec[s.dataset.section]=[Math.round(r.top-root.top),Math.round(r.height)];});
document.querySelectorAll('[data-t]').forEach(function(e){var r=e.getBoundingClientRect();o.t[e.dataset.t]=[r.left-root.left,r.top-root.top,r.right-root.left,r.bottom-root.top];});
o.H=Math.ceil(document.querySelector('main').getBoundingClientRect().bottom-root.top);
var LIM=__LIM__,RW=__RW__;
document.querySelectorAll('main p,main li,main h1,main h2,main h3,main h4,main dd,main dt,main figcaption,main code,main a').forEach(function(e){if(e.scrollWidth>e.clientWidth+1&&getComputedStyle(e).display!=='inline')o.over.push((e.className||e.tagName)+':'+(e.scrollWidth-e.clientWidth)+':'+e.textContent.slice(0,40));var r=e.getBoundingClientRect();if(r.width>0&&r.right-root.left>LIM+1&&!e.closest('.mast'))o.over.push('WIDE '+(e.className||e.tagName)+':'+Math.round(r.right-root.left)+':'+e.textContent.slice(0,30));});
var bad=[];document.querySelectorAll('.root *').forEach(function(e){if(e.closest('svg')&&e.tagName.toLowerCase()!=='svg')return;if(e.matches('svg.layer'))return;var r=e.getBoundingClientRect();if(r.width>0&&(r.right-root.left>RW+.5||r.left-root.left<-.5))bad.push((e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className||e.tagName)+':'+Math.round(r.left-root.left)+'..'+Math.round(r.right-root.left));});
o.outside=bad.slice(0,20);o.docW=document.documentElement.scrollWidth;
document.getElementById('m').textContent=JSON.stringify(o);},500);});});
</script>"""


def shell(layers: str, inner: str, H: int, probe: bool, ph: bool) -> str:
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
{frame.BASE_CSS}{css}.plab text{{font-family:"Hanken Grotesk",sans-serif;font-style:italic;font-size:{12.5 if ph else 13.5}px;fill:#1C2B22}}
</style>
</helmet>
<div class="{cls}" style="width: {w}px; height: {H}px; overflow: hidden; position: relative">
{layers}
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
                                  "--virtual-time-budget=9000", "--dump-dom", f"{PROBE_URL}?v={time.time_ns()}"],
                                 capture_output=True, text=True, encoding="utf-8", timeout=120)
            break
        except subprocess.TimeoutExpired:
            if attempt == 2:
                raise
    mm = re.search(r'<pre id="m">(.*?)</pre>', out.stdout if out else "", re.S)
    if not mm or not mm.group(1).strip():
        raise RuntimeError("probe failed")
    p.unlink()
    return json.loads(html.unescape(mm.group(1)))


def build(ph: bool) -> dict:
    w = PW if ph else W
    name = "3-models-390" if ph else "3-models"
    inner = body(ph)
    m1 = measure(shell("", inner, 16000, True, ph), w)
    layers, H = draw(m1, ph)
    m2 = measure(shell(layers, inner, H, True, ph), w)
    out = shell(layers, inner, H, False, ph)
    frame.check(out)
    (HERE / f"{name}.dc.html").write_text(out, encoding="utf-8")
    (HERE / "static" / f"{name}.html").write_text(frame.static(out), encoding="utf-8")
    print(name, "H", H, "H2", m2["H"], "sections", m2["sec"])
    for k in ("over", "outside"):
        print(" ", k, m2.get(k))
    print("  docW", m2.get("docW"))
    return {"H": H, "m": m2}


def main() -> None:
    which = sys.argv[1:] or ["desktop", "phone"]
    res, new = {}, []
    for k in which:
        res[k] = build(k == "phone")
        new += NEW
    (HERE / "copy-new.json").write_text(json.dumps(list(dict.fromkeys(new)), ensure_ascii=False, indent=1),
                                        encoding="utf-8")
    (HERE / "measure.json").write_text(json.dumps(res, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
