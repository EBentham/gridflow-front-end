"""Page 2: the vendor hub, rendered for Elexon. The GB system Elexon reports on is drawn above; one Elexon cable
comes down from the substation, and its dataset groups are laid as beds in bronze, each tapped off the cable. The
same cable crosses into silver (the vintage views) and gold (the notebook call)."""
from __future__ import annotations

import json
import math

import hp
import scenery as sn
from frame import (BRONZE, DAY, GOLD, HERE, HORIZON, INK, PACK, SILVER, T, T_BRONZE, T_GOLD, T_SILVER, cable,
                   contact_y, f, footer, joint, masthead, sleeve, smooth, strata_svg, terminal)

NAME = "A-vendor-elexon"
TITLE = "Elexon hub"
PG = "vendor-elexon"
S = 780
XA = 1118                      # the coast; sea to the east
SEA = S + 5
FAR = "#297382"
TX = 40                        # the Elexon cable's lane, in the left margin
ONE = json.loads((HERE / "elexon_oneliners.json").read_text(encoding="utf-8"))
DS = {d["key"]: d for d in PACK["data_sources"]["elexon_hub"]["datasets"]}

GROUPS = [  # the pack's PROPOSED themes (pack-assigned, owner OK pending), in the pack's order
    ("Prices and balancing", "What the system paid to balance, and the actions behind it.",
     ["system_prices", "market_depth", "mid", "boal", "pn", "disbsad", "netbsad", "soso"]),
    ("Generation and availability", "What ran, by fuel and by unit, and what is declared available.",
     ["fuelhh", "fuelinst", "agpt", "agws", "windfor", "fou2t14d", "uou2t14d", "nonbm"]),
    ("Demand", "Outturn and forecasts, national and transmission, from the day ahead to 14 days out.",
     ["indo", "itsdo", "indod", "atl", "ndf", "ndfd", "tsdf", "tsdfd", "inddem"]),
    ("System indicators", "Margin, imbalance, loss-of-load probability, frequency and temperature.",
     ["indgen", "imbalngc", "melngc", "lolpdrm", "freq", "temp"]),
    ("Reference and messages", "The register of BM units, and outage and unavailability notices.",
     ["bmunits_reference", "remit"]),
]


def cut(x: float) -> float:
    y = hp.prof(x)
    if x > XA:
        t = min(1.0, (x - XA) / 60)
        y += t * t * (3 - 2 * t) * (30 + 3 * math.sin(x / 23))
    return y


def path_of(k: str) -> str:
    d = DS[k]
    p = d["api_path"]
    if d["param_style"] == "date_path":
        p += "/{date}"
    return p


def beds() -> str:
    out = []
    for i, (name, desc, keys) in enumerate(GROUPS):
        rows = "".join(f'<li><a href="#"><code>{k}</code></a><div><span class="d">{ONE[k]}</span>'
                       f'<code class="p">{path_of(k)}</code></div></li>' for k in keys)
        out.append(f'<section class="bed" aria-labelledby="g{i}" data-t="bed{i}">'
                   f'<div class="bed-h"><h3 id="g{i}">{T(PG, name)}</h3><p>{T(PG, desc)}</p></div>'
                   f'<ul class="rows">{rows}</ul></section>')
    return "".join(out)


# ---------------------------------------------------------------- the topsoil figure: wind by month
def wind_chart() -> tuple[str, dict]:
    s = PACK["series"]["elexon_hub"]
    pts = s["points"]
    w, h = 1280, 210
    L, R, Tp, B = 58, 6, 18, 34
    pw, ph = w - L - R, h - Tp - B
    n = len(pts)
    step = pw / n
    Y = lambda v: Tp + (12000 - v) * ph / 12000  # noqa: E731
    g = []
    bars = "".join(f'<rect x="{f(L + i * step + 3)}" y="{f(Y(v))}" width="{f(step - 6)}" height="{f(Y(0) - Y(v))}">'
                   f'</rect>' for i, (_, v) in enumerate(pts))
    g.append(f'<g fill="{HORIZON}">{bars}</g>')
    for v in (0, 4000, 8000, 12000):
        g.append(f'<path d="M{L - 5} {f(Y(v))} H{L}" stroke="{INK}" stroke-width="1"></path>'
                 f'<text x="{L - 9}" y="{f(Y(v) + 4)}" text-anchor="end">{v:,}</text>')
    for i, (m, _) in enumerate(pts):
        if m.endswith("-01") or i == 0:
            x = L + i * step
            lab = m[:4] if m.endswith("-01") else "Sep 2021"
            g.append(f'<path d="M{f(x)} {Tp + ph} v7" stroke="{INK}" stroke-width="1"></path>'
                     f'<text x="{f(x + 4)}" y="{Tp + ph + 22}">{lab}</text>')
    g.append(f'<path d="M{L} {Tp - 6} V{Tp + ph} H{w - R}" stroke="{INK}" stroke-width="1.2" fill="none"></path>')
    g.append(f'<text x="{L + 8}" y="{Tp}" class="u">MW</text>')
    vals = [v for _, v in pts]
    hi, lo = vals.index(max(vals)), vals.index(min(vals))
    for i, anchor in ((hi, "middle"),):
        x = L + i * step + step / 2
        g.append(f'<text class="dl" x="{f(x)}" y="{f(Y(vals[i]) - 7)}" text-anchor="{anchor}">{vals[i]:,.0f}</text>')
    aria = (f"Column chart of GB transmission-metered wind generation from elexon/fuelhh, mean half-hourly output per "
            f"calendar month, September 2021 to August 2026, in MW. Monthly means run from {min(vals):,.0f} MW to "
            f"{max(vals):,.0f} MW.")
    svg = (f'<svg class="chart" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{aria}">'
           + "".join(g) + "</svg>")
    return svg, {"hi": pts[hi][0], "lo": pts[lo][0], "vhi": vals[hi], "vlo": vals[lo]}


MONTHS = "January February March April May June July August September October November December".split()


def month(ym: str) -> str:
    return f"{MONTHS[int(ym[5:7]) - 1]} {ym[:4]}"


def html() -> tuple[str, str]:
    facts = [
        ("Market", "GB electricity"),
        ("Access", "No API key"),
        ("Base URL", "<code>data.elexon.co.uk/bmrs/api/v1</code>"),
        ("Grain", "Half-hourly settlement periods, 1 to 50 a day (46 or 50 when the clocks change); FUELINST every "
                  "5 minutes"),
        ("Connector", "<code>connectors/elexon/client.py</code>"),
        ("Datasets", "[n]"),
    ]
    dl = "".join(f'<div><dt>{T(PG, a)}</dt><dd>{T(PG, b)}</dd></div>' for a, b in facts)
    sky = (f'<section class="sky" data-st="sky" style="height: {S}px" aria-labelledby="h1">{masthead("Data sources")}'
           f'<div class="hero"><div><nav class="crumb" aria-label="Breadcrumb"><a href="#">Data sources</a></nav>'
           f'<h1 id="h1">Elexon BMRS</h1>'
           f'<p class="intro">{T(PG, "Great Britain’s balancing mechanism, from Elexon’s Insights API: system prices, generation outturn, BM-unit data, and demand and wind forecasts.")}</p></div>'
           f'<dl class="facts">{dl}</dl></div></section>')
    chart, ex = wind_chart()
    top = (f'<section class="st st-top" data-st="topsoil" aria-labelledby="w-h"><div class="wind">'
           f'<h2 class="fig-h" id="w-h">{T(PG, "GB wind generation, monthly mean, September 2021 to August 2026")}</h2>'
           f'{chart}<p class="cap">{T(PG, "elexon/fuelhh, fuel type WIND: mean half-hourly generation_mw per calendar month, MW, one row per settlement date, period and fuel type. The highest month is " + month(ex["hi"]) + ", the lowest " + month(ex["lo"]) + ". FUELHH is transmission-metered and carries no solar; GB solar outturn is in the NESO Data Portal’s historic_generation_mix.")}</p>'
           f'</div></section>')
    intro = (f'<div class="b-head"><h2 class="big" id="b-h">{T(PG, "The datasets, in five groups")}</h2>'
             f'<p class="body">{T(PG, "The groups are this site’s way in. In gridflow’s code they differ by how each is requested: most take a from/to publish-time window; system_prices and market_depth take a settlement date in the path, pn a settlement date and period, and bmunits_reference nothing at all.")}</p></div>')
    bronze = (f'<section class="st st-bronze" data-st="bronze" aria-labelledby="b-h">{intro}{beds()}</section>')
    views = ["silver_elexon_system_prices_latest", "silver_elexon_remit_latest", "silver_elexon_fou2t14d_latest"]
    silver = (f'<section class="st st-silver" data-st="silver" aria-labelledby="s-h"><div class="pair">'
              f'<div><h2 class="fig-h" id="s-h" data-t="silver">{T(PG, "In silver, every capture is kept")}</h2>'
              f'<p class="body">{T(PG, "Each dataset is one DuckDB view,")} <code>silver_elexon_{{dataset}}</code>. '
              f'{T(PG, "Three are append-only: a later publication never overwrites an earlier one, each capture is its own")} '
              f'<code>_run{{available_at}}</code> {T(PG, "file, and a")} <code>_latest</code> '
              f'{T(PG, "view returns the newest capture for each key.")}</p></div>'
              f'<ul class="tables" aria-label="{T(PG, "Latest-vintage views")}">'
              + "".join(f"<li>{v}</li>" for v in views) + '</ul></div></section>')
    code = ('data.elexon.list_datasets()\n'
            'df = data.elexon.query(<span class="s">"fuelhh"</span>, start, end)')
    gold = (f'<section class="st st-gold" data-st="gold" aria-labelledby="g-h"><div class="pair">'
            f'<div><h2 class="fig-h" id="g-h" data-t="gold">{T(PG, "From a notebook")}</h2>'
            f'<p class="body">{T(PG, "The workbench in gridflow-models reads the same silver. Every source answers the same verbs.")}</p></div>'
            f'<pre class="well">{code}</pre></div></section>')
    body = "\n".join([sky, top, bronze, silver, gold, footer(PG)])
    return body, CSS


CSS = """.hero .intro{margin:26px 0 0;font-size:21px;line-height:1.5;color:#F6F4EC;max-width:36ch}
.hero .facts{margin-top:18px}
.hero .facts dt{font-size:14px}
.wind{padding:92px 0 70px}
.wind .fig-h{margin-bottom:18px}
.wind .cap{margin-top:10px}
.b-head{padding:70px 0 22px}
.bed{padding:24px 0 26px}
.bed-h{display:grid;grid-template-columns:330px minmax(0,1fr);column-gap:40px;align-items:baseline;margin:0 0 16px}
.bed-h h3{font-size:23px;font-weight:720;font-stretch:90%;line-height:1.1;letter-spacing:-.01em}
.bed-h p{margin:0;font-size:14.5px;line-height:1.5;color:#3F4A3B;max-width:58ch}
.rows{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:60px;border-top:1px solid rgba(28,43,34,.22)}
.rows li{display:grid;grid-template-columns:190px minmax(0,1fr);column-gap:14px;padding:7px 0 8px;border-bottom:1px solid rgba(28,43,34,.22)}
.rows a{align-self:start;text-decoration-color:rgba(102,121,59,.9)}
.rows a code{font-size:15px;color:#1C2B22}
.rows .d{display:block;font-size:14.5px;line-height:1.4;color:#1C2B22}
.rows .p{display:block;margin-top:2px;font-size:12.5px;line-height:1.4;color:#3F4A3B}
.pair{display:grid;grid-template-columns:620px minmax(0,1fr);column-gap:100px;align-items:start;padding:64px 0 64px}
.tables{list-style:none;margin:4px 0 0;padding:0;border-top:1px solid rgba(28,43,34,.22)}
.tables li{font-family:"Red Hat Mono",monospace;font-size:16px;height:44px;line-height:44px;border-bottom:1px solid rgba(28,43,34,.22);color:#1C2B22}
.st-gold .well{margin-top:4px}
.chart text.u{font-size:12.5px}
"""


# ---------------------------------------------------------------- drawing
def landscape() -> tuple[str, str, str]:
    p = []
    H0 = S - 150
    p.append(sn.ridge([(-20, S - 236), (150, S - 258), (330, S - 246), (520, S - 262), (700, S - 244),
                       (880, S - 222), (1010, S - 192), (1090, S - 160), (1140, S - 150)], S - 30, FAR))
    sea = f"M1000 {H0} H1460 V{SEA} H{XA} V{S - 12} H1000 Z"
    p.append(f'<path d="{sea}" fill="{HORIZON}"></path><path d="{sea}" fill="{DAY}" opacity=".13"></path>')
    p.append(sn.wavelets([(1180, H0 + 12, 34), (1290, H0 + 18, 24), (1390, H0 + 10, 30), (1150, H0 + 50, 26),
                          (1260, H0 + 62, 40), (1380, H0 + 70, 22), (1200, H0 + 104, 30), (1330, H0 + 118, 36)]))
    for i, (ox, oh) in enumerate([(1170, 26), (1224, 30), (1282, 27), (1340, 31), (1398, 27)]):
        p.append(hp.turbine(ox, H0 + 10 + (i % 2) * 3, oh, oh * .5, ["sp1", "sp2", "sp3"][i % 3], 19 * i))
    near = [(-20, S - 204), (90, S - 226), (230, S - 234), (360, S - 216), (490, S - 238), (630, S - 226),
            (760, S - 210), (880, S - 184), (960, S - 162), (1010, S - 150)]
    p.append(sn.ridge(near, S - 90, HORIZON))
    for i, (tx, ty) in enumerate(near[1:7]):
        hgt = [72, 78, 68, 80, 72, 66][i]
        p.append(hp.turbine(tx, ty + 3, hgt, hgt * .5, ["sp2", "sp1", "sp3"][i % 3], 37 * i + 10))
    top = [(-20, S - 140), (180, S - 150), (380, S - 136), (580, S - 146), (780, S - 140), (960, S - 148),
           (1040, H0), (1110, H0), (1104, H0 + 18), (1082, S - 108), (1090, S - 70), (1102, S - 36), (XA + 4, SEA)]
    p.append(sn.field(top, hp.prof, -20, XA + 4,
                      [[(-20, S - 116), (400, S - 120), (800, S - 108), (1050, S - 84)],
                       [(-20, S - 86), (500, S - 92), (1000, S - 66)], [(300, S - 48), (700, S - 52), (1080, S - 38)]]))
    # the sea in section
    xs = [x / 2 for x in range(2 * XA, 2 * 1460 + 1)]
    wet = [(x, cut(x)) for x in xs if cut(x) > SEA + .5]
    water = (f"M{f(wet[0][0])} {SEA} " + " ".join(f"L{f(x)} {f(y)}" for x, y in wet[::4] + [wet[-1]])
             + f" L{f(wet[-1][0])} {SEA} Z")
    p.append(f'<path d="{water}" fill="{HORIZON}"></path><path d="M{f(wet[0][0])} {SEA} H1440" stroke="{DAY}" '
             f'stroke-width="1.2" opacity=".6"></path>')
    for i, ox in enumerate((1236, 1352)):
        p.append(sn.monopile_turbine(ox, SEA, cut(ox), 100 - 8 * i, ["sp1", "sp3"][i], 30 + 60 * i))
    # the grid: pylons into the substation (where the Elexon cable starts), then the plant
    pl = (72, hp.prof(72) - 2, .6)
    sub_x, sub_s = 160, 1.12
    sb = hp.prof(sub_x + 50)
    sub_svg, ends = hp.substation(sub_x, sb)
    ends = [(sub_x + (ex - sub_x) * sub_s, sb + (ey - sb) * sub_s) for ex, ey in ends]
    p.append(f'<g stroke="{INK}" fill="none" stroke-linecap="round" stroke-width="1.35">{hp.pylon(*pl)}</g>')
    p.append(hp.sc(sub_svg, sub_x, sb, sub_s))
    wires = [hp.spans([(-20, S - 150), (-20, S - 164), (-20, S - 176)], hp.tips(*pl, -1), 6),
             hp.spans(hp.tips(*pl, 1), ends, 9)]
    p.append(f'<path d="{" ".join(wires)}" stroke="{INK}" stroke-width=".8" fill="none" opacity=".85"></path>')
    p.append(hp.ccgt(330, hp.prof(370), 1.0))
    p.append(sn.nuclear(520, hp.prof(580)))
    p.append(hp.sc(hp.battery(740, hp.prof(790)), 740, hp.prof(790), 1.2))
    p.append(hp.sc(hp.converter(962, hp.prof(1020)), 962, hp.prof(1020), 1.1))
    labels = [
        ("onshore wind", 300, S - 262, "#E4EFEC", "middle"),
        ("offshore wind", 1290, H0 - 44, "#E4EFEC", "middle"),
        ("substation", 212, S - 72, INK, "middle"),
        ("gas-fired power station", 366, S - 128, INK, "middle"),
        ("nuclear power station", 586, S - 84, INK, "middle"),
        ("battery storage", 810, S - 44, INK, "middle"),
        ("interconnector", 1010, S - 100, INK, "middle"),
        ("converter station", 1010, S - 85, INK, "middle"),
    ]
    lab = "".join(f'<text x="{x}" y="{y}" fill="{c}" text-anchor="{a}">{T(PG, t)}</text>' for t, x, y, c, a in labels)
    aria = T(PG, "The GB system that Elexon reports on: pylons into a substation, a gas-fired power station, a nuclear "
                 "power station, battery storage and an interconnector converter station on the coast, with onshore "
                 "wind on the ridge and offshore wind cut in section at sea. One cable runs down from the "
                 "substation and taps each group of datasets in turn.")
    return "\n".join(p), lab, aria


def draw(m: dict) -> tuple[str, int]:
    hp.Y["surf"] = S
    secs = m["secs"]
    H = int(math.ceil(m["H"]))
    yb, ys, yg, yd = secs["bronze"][0], secs["silver"][0], secs["gold"][0], secs["deep"][0]
    surf = [(x, cut(x)) for x in range(-40, 1481, 10)]
    bed_lines = [m["t"][f"bed{i}"][1] for i in range(1, len(GROUPS))]
    bg = strata_svg(H, S, surf, [("bronze", yb), ("silver", ys), ("gold", yg), ("deep", yd)], beds=bed_lines)
    land, lab, aria = landscape()
    land_svg = (f'<svg class="layer land-svg" width="1440" height="{S + 44}" viewBox="0 0 1440 {S + 44}" role="img" '
                f'aria-label="{aria}">{land}<g class="lab">{lab}</g></svg>')
    # one cable: substation -> the margin lane -> a joint and a terminal per bed -> silver -> gold
    x0 = 214
    taps = []
    for i in range(len(GROUPS)):
        l, t, r, b = m["t"][f"bed{i}"]
        taps.append(t + 24 + 13)          # level with the bed heading
    sl, st_, _, _ = m["t"]["silver"]
    gl, gt, _, _ = m["t"]["gold"]
    ys_end, yg_end = st_ + 17, gt + 17
    c_bs, c_sg = contact_y("silver", ys, TX), contact_y("gold", yg, TX)
    pts = [(x0, cut(x0) - 3), (x0, S + 12)]
    for k in range(1, 12):
        tt = k / 12
        s2 = tt * tt * (3 - 2 * tt)
        pts.append((x0 + (TX - x0) * s2, S + 12 + 58 * tt))
    pts.append((TX, S + 70))
    trunk_b = smooth(pts) + f" V{f(c_bs)}"
    c = [cable(trunk_b, BRONZE), cable(f"M{TX} {f(c_bs)} V{f(c_sg)}", SILVER),
         cable(f"M{TX} {f(c_sg)} V{f(yg_end - 14)} Q{TX} {f(yg_end)} {TX + 14} {f(yg_end)} H57", GOLD)]
    ends = []
    for y in taps:
        c.append(cable(f"M{TX} {f(y)} H{f(64 - 7)}", BRONZE))
        ends.append(joint(TX, y))
        ends.append(terminal(64, y))
    c.append(cable(f"M{TX} {f(ys_end)} H{f(64 - 7)}", SILVER))
    ends.append(joint(TX, ys_end))
    ends.append(terminal(64, ys_end, T_SILVER))
    ends.append(terminal(64, yg_end, T_GOLD))
    ends.append(sleeve(TX, c_bs, SILVER))
    ends.append(sleeve(TX, c_sg, GOLD))
    cab = (f'<svg class="layer" width="1440" height="{H}" viewBox="0 0 1440 {H}" aria-hidden="true">'
           + "".join(c) + "".join(ends) + "</svg>")
    return bg + "\n" + land_svg + "\n" + cab, H


_ = (T_BRONZE, T_SILVER)
