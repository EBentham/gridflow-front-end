"""Page 1: the data-sources landing. A west-to-east section: GB, the North Sea in profile, the continent. Seven
assets carry cables that drop through a shallow topsoil to the vendor entries in bronze; the silver band shows one
dataset under all its names, with the one series the pack computed for this page."""
from __future__ import annotations

import math

import hp
import scenery as sn
from frame import (BRONZE, CHART, CLAY, DAY, GOLD, HORIZON, INK, OLIVE, PACK, PETROL, SILVER, SOFT, T, T_BRONZE,
                   T_SILVER, cable, drop, f, footer, joint, masthead, sleeve, smooth, strata_svg, terminal)

NAME = "A-data-sources"
TITLE = "Data sources"
PG = "data-sources"
S = 780                     # the cut (sky height)
XA, XB = 772, 1012          # the coasts
SEA = S + 5                 # sea level in the cut
TOP_H = 150                 # topsoil depth
FAR, MIDR = "#297382", "#378390"   # horizon at .5 and .82 over petrol, made opaque so the sea cannot show through


def prof(x: float) -> float:
    return hp.prof(x)


def cut(x: float) -> float:
    """The ground surface in the cut, with the seabed between the coasts."""
    y = hp.prof(x)
    if XA < x < XB:
        t = (x - XA) / (XB - XA)
        ramp = min(1.0, t / .18, (1 - t) / .18)
        ramp = ramp * ramp * (3 - 2 * ramp)
        y += ramp * (30 + 3 * math.sin(x / 23))
    return y


# ---------------------------------------------------------------- vendors, in x order (the cable order)
V = {v["hub_slug"]: v for v in PACK["data_sources"]["vendors"]}
VENDORS = [
    # slug, name, bronze dirs, description, fact line, representative (key, gloss), grid col, row
    ("elexon", "Elexon BMRS", "bronze/elexon/",
     "GB balancing mechanism: prices, generation, demand, BM units and forecasts",
     "[n] datasets, half-hourly, no API key",
     [("system_prices", "one imbalance price per period"), ("fuelhh", "outturn by fuel type, no solar"),
      ("indo", "initial national demand outturn"), ("mid", "market index, the GB day-ahead benchmark")], 1, 1),
    ("neso", "NESO Carbon Intensity", "bronze/neso/",
     "GB carbon intensity, national and regional, actual and forecast",
     "[n] datasets, half-hourly, no API key",
     [("carbon_intensity", "national, over a date range"), ("regional_intensity", "every region, over a date range"),
      ("generation", "national generation mix"), ("intensity_fw48h", "48-hour forecast")], 2, 2),
    ("neso_data_portal", "NESO Data Portal", "bronze/neso_data_portal/",
     "System operator files: the GB generation mix since 2009, embedded forecasts",
     "[n] datasets, current file only, no API key",
     [("historic_generation_mix", "GB mix by fuel since 2009, with solar"),
      ("embedded_wind_solar_forecast", "embedded wind and solar forecast"),
      ("daily_wind_availability", "daily MW per BM unit")], 2, 1),
    ("openmeteo", "Open-Meteo", "bronze/open_meteo/",
     "Weather archive and forecasts at GB demand cities, wind and solar sites",
     "[n] datasets, hourly, no API key",
     [("historical_demand", "ERA5 at 7 demand cities"), ("historical_wind", "ERA5 at 12 wind sites, 10 m and 100 m"),
      ("historical_solar", "ERA5 at 6 solar sites"), ("forecast_wind", "forecast at the same wind sites")], 3, 2),
    ("gie", "GIE AGSI+ and ALSI", "bronze/gie_agsi/, gie_alsi/",
     "EU gas storage levels and flows, and LNG terminal send-out",
     "[n] datasets, daily gas days, API key",
     [("storage", "storage level by country and day"), ("storage_reports", "by country, company or facility"),
      ("unavailability", "storage unavailability reports"), ("lng", "LNG terminal data")], 3, 1),
    ("entsog", "ENTSO-G", "bronze/entsog/",
     "EU gas: flows, nominations and capacity at interconnection points",
     "[n] datasets, daily gas days, no API key",
     [("physical_flows", "flow at interconnection points"), ("nominations", "nominations per point"),
      ("firm_technical", "firm technical capacity"), ("gcv", "gross calorific value")], 4, 2),
    ("entsoe", "ENTSO-E", "bronze/entsoe/",
     "EU electricity: day-ahead prices, load, generation, flows and outages",
     "[n] datasets, XML, API key",
     [("day_ahead_prices", "EUR/MWh per bidding zone"), ("actual_generation", "output per production type"),
      ("cross_border_flows", "physical flows between zones"), ("wind_solar_forecast", "day-ahead wind and solar")], 4, 1),
]

# asset x for each cable origin, same order
ORIG = {"elexon": 236, "neso": 356, "neso_data_portal": 596, "openmeteo": 748, "gie": 1104, "entsog": 1252,
        "entsoe": 1354}


def entries() -> str:
    out = []
    for slug, name, bdir, desc, fact, reps, col, row in VENDORS:
        li = "".join(f'<li><a href="#"><code>{k}</code></a><span>{T(PG, g)}</span></li>' for k, g in reps)
        out.append(f'<li class="vend r{row}" style="grid-column: {col}; grid-row: {row}" data-t="v-{slug}">'
                   f'<p class="land"><code>{bdir}</code></p>'
                   f'<h2 class="vn"><a href="#">{name}</a></h2><p class="vd">{T(PG, desc)}</p><p class="vm">{T(PG, fact)}</p>'
                   f'<ul class="reps" aria-label="{name}: datasets to start with">{li}</ul></li>')
    return "".join(out)


# ---------------------------------------------------------------- the names of one dataset
NAMES = [
    ("vendor endpoint", "/balancing/settlement/system-prices/{date}"),
    ("raw responses", "bronze/elexon/system_prices/"),
    ("typed Parquet", "silver/elexon/system_prices/"),
    ("DuckDB view", "silver_elexon_system_prices_latest"),
    ("notebook", 'data.elexon.query("system_prices", start, end)'),
]


DATES: dict[str, str] = {}
MONTHS = "January February March April May June July August September October November December".split()


def day(iso: str) -> str:
    return f"{int(iso[8:10])} {MONTHS[int(iso[5:7]) - 1]}"


def price_chart() -> tuple[str, str]:
    s = PACK["series"]["data_sources_landing"]
    pts = s["points"]
    w, h = 700, 250
    L, R, Tp, B = 46, 12, 12, 34
    pw, ph = w - L - R, h - Tp - B
    n = len(pts)
    X = lambda i: L + i * pw / (n - 1)  # noqa: E731
    Y = lambda v: Tp + (220 - v) * ph / 220  # noqa: E731
    d = "M" + " L".join(f"{f(X(i))} {f(Y(v))}" for i, (_, v) in enumerate(pts))
    g = []
    for v in (0, 50, 100, 150, 200):
        g.append(f'<path d="M{L - 5} {f(Y(v))} H{L}" stroke="{INK}" stroke-width="1"></path>')
        g.append(f'<text x="{L - 9}" y="{f(Y(v) + 4)}" text-anchor="end">{v}</text>')
    months = [("Jun", "2026-06-01"), ("Jul", "2026-07-01"), ("Aug", "2026-08-01"), ("Sep", "2026-09-01")]
    idx = {p[0]: i for i, p in enumerate(pts)}
    for lab, day in months:
        i = idx[day]
        g.append(f'<path d="M{f(X(i))} {Tp + ph} v6" stroke="{INK}" stroke-width="1"></path>'
                 f'<text x="{f(X(i))}" y="{Tp + ph + 22}" text-anchor="middle">{lab} 2026</text>')
    g.append(f'<path d="M{L} {Tp} V{Tp + ph} H{w - R}" stroke="{INK}" stroke-width="1.2" fill="none"></path>')
    g.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"></path>')
    g.append(f'<text x="{L + 8}" y="{Tp + 4}" class="u">GBP/MWh</text>')
    vals = [v for _, v in pts]
    lo, hi = vals.index(min(vals)), vals.index(max(vals))
    g.append(f'<circle cx="{f(X(hi))}" cy="{f(Y(vals[hi]))}" r="3.2" fill="{INK}"></circle>'
             f'<text class="dl" x="{f(X(hi) - 8)}" y="{f(Y(vals[hi]) + 5)}" text-anchor="end">{vals[hi]:.1f}</text>')
    g.append(f'<circle cx="{f(X(lo))}" cy="{f(Y(vals[lo]))}" r="3.2" fill="{INK}"></circle>'
             f'<text class="dl" x="{f(X(lo) + 9)}" y="{f(Y(vals[lo]) + 5)}">{vals[lo]:.1f}</text>')
    DATES["hi"], DATES["lo"] = pts[hi][0], pts[lo][0]
    aria = (f"Line chart of the GB system price, daily mean of the 48 settlement periods, 26 May to 22 September 2026, "
            f"in GBP/MWh. It ranges from {min(vals):.1f} to {max(vals):.1f}.")
    svg = (f'<svg class="chart" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{aria}">'
           + "".join(g) + "</svg>")
    return svg, aria


def html() -> tuple[str, str]:
    lede = (f'<p class="lead">{T(PG, "gridflow reads seven vendors across GB and EU electricity, EU gas, carbon intensity and weather.")} '
            f'{T(PG, "The catalogue holds")} <span class="n">[N datasets]</span>{T(PG, ", organised by vendor.")}</p>'
            f'<p>{T(PG, "Each cable in the drawing runs from the part of the system a vendor reports on down to the directory where gridflow keeps that vendor’s raw responses.")}</p>'
            f'<p><a class="alt" href="#">{T(PG, "How the layers work")}</a></p>')
    h1 = T(PG, "Every dataset, traced to the vendor that publishes it")
    sky = (f'<section class="sky" data-st="sky" style="height: {S}px" aria-labelledby="h1">{masthead("Data sources")}'
           f'<div class="hero"><div><h1 id="h1">{h1}</h1></div><div class="lede">{lede}</div></div></section>')
    top = f'<div class="st st-top" data-st="topsoil" style="height: {TOP_H}px" aria-hidden="true"></div>'
    bronze = (f'<section class="st st-bronze" data-st="bronze" aria-label="{T(PG, "The seven vendors")}">'
              f'<ul class="vgrid">{entries()}<li class="vnote"><p>{T(PG, "The path beside each terminal is where gridflow keeps that vendor’s raw responses. The linked datasets are places to start: each vendor’s hub lists all of them, in groups.")}</p></li></ul></section>')
    chart, _ = price_chart()
    names = "".join(f'<div><dt>{T(PG, a)}</dt><dd><code>{b}</code></dd></div>' for a, b in NAMES)
    s = PACK["series"]["data_sources_landing"]
    silver = (f'<section class="st st-silver" data-st="silver" aria-labelledby="find-h"><div class="find">'
              f'<div class="find-l" data-t="find"><h2 class="big" id="find-h">{T(PG, "Find a dataset")}</h2>'
              f'<p class="body">{T(PG, "Search a vendor’s hub, or use the dataset’s gridflow key: it names the dataset in every layer, from the raw files to the notebook. Here is")} '
              f'<code>system_prices</code> {T(PG, "under each of its names.")}</p>'
              f'<dl class="names">{names}</dl></div>'
              f'<figure class="find-r"><h3 class="fig-h">{T(PG, "GB system price, daily mean, 26 May to 22 September 2026")}</h3>'
              f'{chart}<figcaption class="cap">{T(PG, "elexon/system_prices in silver: the latest vintage of each settlement period, averaged over the 48 periods of each settlement date, GBP/MWh. The dots mark the highest day, " + day(DATES["hi"]) + ", and the lowest, " + day(DATES["lo"]) + ". System sell and buy prices are equal on every row, so one line shows both.")}'
              f'</figcaption></figure></div></section>')
    _ = s
    body = "\n".join([sky, top, bronze, silver, footer(PG)])
    return body, CSS


CSS = """.vgrid{list-style:none;margin:0;padding:66px 0 72px;display:grid;grid-template-columns:repeat(4,280px);column-gap:53.33px;row-gap:46px;align-items:start}
.vend{min-width:0;width:280px;box-sizing:border-box}
.vnote{grid-column:1;grid-row:2;width:236px;padding-top:34px}
.vnote p{margin:0;font-size:14px;line-height:1.55;color:#3F4A3B;font-style:italic}
.vend.r2{margin-left:-43.33px}
.vend .land{margin:0 0 10px;height:18px;padding-left:30px;font-size:13px;line-height:18px;transform:translateY(-9px);color:#1C2B22}
.vend .land code{font-size:13px}
.vend .vn{font-size:23px;font-weight:720;font-stretch:90%;line-height:1.1;letter-spacing:-.01em;margin:0 0 6px}
.vend .vn a{text-decoration-color:rgba(28,43,34,0)}
.vend .vn a:hover{text-decoration-color:#66793B}
.vend .vd{margin:0;font-size:14.5px;line-height:1.45;color:#3F4A3B}
.vend .vm{margin:8px 0 12px;font-size:14.5px;font-weight:600;color:#1C2B22}
.reps{list-style:none;margin:0;padding:0;border-top:1px solid rgba(28,43,34,.22)}
.reps li{padding:6px 0 7px;border-bottom:1px solid rgba(28,43,34,.22);line-height:1.35}
.reps a{display:block;text-decoration-color:rgba(102,121,59,.9)}
.reps code{font-size:14px;color:#1C2B22}
.reps span{display:block;font-size:13.5px;color:#3F4A3B}
.find{display:grid;grid-template-columns:520px 700px;column-gap:60px;padding:76px 0 90px;align-items:start}
.find-l{padding-top:22px}
.names{margin:22px 0 0}
.names div{display:grid;grid-template-columns:118px minmax(0,1fr);column-gap:14px;padding:8px 0;border-top:1px solid rgba(28,43,34,.22)}
.names div:last-child{border-bottom:1px solid rgba(28,43,34,.22)}
.names dt{font-size:14px;line-height:1.5;color:#3F4A3B;font-style:italic}
.names dd{margin:0;font-size:14px;line-height:1.5;overflow-wrap:anywhere}
.names code{font-size:13.5px}
.find-r{margin:0}
.find-r .fig-h{font-size:23px;font-weight:720;font-stretch:90%;line-height:1.15;letter-spacing:-.01em;margin:0 0 16px}
.chart text.u{font-size:12.5px}
"""


# ---------------------------------------------------------------- drawing (pass 2)
def landscape() -> tuple[str, str]:
    p = []
    H0 = S - 152                                    # the horizon over the sea
    # far hills, then the sea between them (bounded by the horizon and the two coasts)
    p.append(sn.ridge([(-20, S - 262), (140, S - 292), (320, S - 276), (500, S - 300), (660, S - 270),
                       (780, S - 214), (846, S - 158), (870, S - 150)], S - 30, FAR))
    p.append(sn.ridge([(972, S - 150), (1000, S - 172), (1080, S - 206), (1210, S - 196), (1330, S - 222),
                       (1460, S - 204)], S - 30, FAR))
    sea = f"M680 {H0} H1110 V{S - 12} H{XB} V{SEA} H{XA} V{S - 12} H680 Z"
    p.append(f'<path d="{sea}" fill="{HORIZON}"></path><path d="{sea}" fill="{DAY}" opacity=".13"></path>')
    p.append(sn.wavelets([(876, H0 + 12, 30), (930, H0 + 22, 22), (952, H0 + 8, 20), (846, H0 + 44, 36),
                          (952, H0 + 56, 24), (812, H0 + 92, 28), (860, H0 + 122, 40), (790, H0 + 130, 22)]))
    # far offshore wind on the horizon
    for i, (ox, oh) in enumerate([(884, 22), (914, 25), (944, 22), (968, 24)]):
        p.append(hp.turbine(ox, H0 + 8 + (i % 2) * 2, oh, oh * .5, ["sp1", "sp2", "sp3"][i % 3], 23 * i))
    # near ridge (GB) with onshore wind, and the continent's low ridge
    near = [(-20, S - 226), (80, S - 258), (200, S - 268), (330, S - 246), (450, S - 272), (590, S - 256),
            (700, S - 222), (760, S - 180), (800, S - 156)]
    p.append(sn.ridge(near, S - 90, HORIZON))
    for i, (tx, ty) in enumerate(near[1:6]):
        hgt = [80, 88, 74, 90, 78][i]
        p.append(hp.turbine(tx, ty + 3, hgt, hgt * .5, ["sp2", "sp1", "sp3"][i % 3], 40 * i + 10))
    p.append(sn.ridge([(990, S - 152), (1040, S - 162), (1110, S - 172), (1240, S - 166), (1360, S - 182), (1460, S - 172)],
                      S - 60, MIDR))
    # energised land on both shores
    gb_top = [(-20, S - 142), (160, S - 150), (340, S - 138), (520, S - 146), (660, S - 148), (760, H0),
              (852, H0), (846, H0 + 16), (826, S - 112), (804, S - 80), (790, S - 44), (XA + 4, SEA)]
    p.append(sn.field(gb_top, prof, -20, XA + 4,
                      [[(-20, S - 118), (300, S - 122), (560, S - 114), (720, S - 92)],
                       [(-20, S - 88), (400, S - 92), (700, S - 70)], [(200, S - 50), (500, S - 54), (730, S - 40)]]))
    eu_top = [(XB - 4, SEA), (XB + 8, S - 46), (1000, S - 94), (984, S - 128), (988, H0), (1080, H0 + 2),
              (1160, S - 140), (1280, S - 132), (1460, S - 126)]
    p.append(sn.field(eu_top, prof, XB - 4, 1460,
                      [[(1010, S - 100), (1200, S - 104), (1460, S - 98)], [(1022, S - 56), (1250, S - 62), (1460, S - 58)]]))
    # the jetty and an LNG carrier alongside
    jy = S - 58
    p.append(f'<path d="M{XB + 6} {jy} H{XB - 44} M{XB - 36} {jy} v10 M{XB - 12} {jy} v12" '
             f'stroke="{INK}" stroke-width="1.1" fill="none"></path>')
    p.append(sn.lng_carrier(XB - 174, jy + 8, 124))
    # the sea in section: water down to the seabed, near turbines on monopiles
    xs = [x / 2 for x in range(2 * XA, 2 * XB + 1)]
    wet = [(x, cut(x)) for x in xs if cut(x) > SEA + .5]
    water = (f"M{f(wet[0][0])} {SEA} " + " ".join(f"L{f(x)} {f(y)}" for x, y in wet[::4] + [wet[-1]])
             + f" L{f(wet[-1][0])} {SEA} Z")
    p.append(f'<path d="{water}" fill="{HORIZON}"></path><path d="M{f(wet[0][0])} {SEA} H{f(wet[-1][0])}" '
             f'stroke="{DAY}" stroke-width="1.2" opacity=".6"></path>')
    p.append(sn.monopile_turbine(812, SEA, cut(812), 100, "sp1", 30))
    # the assets, west to east
    p.append(f'<g stroke="{INK}" fill="none" stroke-linecap="round" stroke-width="1.35">'
             f'{hp.pylon(92, prof(92) - 2, .6)}</g>')
    sub_x, sub_s = 176, 1.12
    sb = prof(sub_x + 50)
    sub_svg, ends = hp.substation(sub_x, sb)
    ends = [(sub_x + (ex - sub_x) * sub_s, sb + (ey - sb) * sub_s) for ex, ey in ends]
    p.append(hp.sc(sub_svg, sub_x, sb, sub_s))
    wires = [hp.spans([(-20, S - 150), (-20, S - 164), (-20, S - 176)], hp.tips(92, prof(92) - 2, .6, -1), 6),
             hp.spans(hp.tips(92, prof(92) - 2, .6, 1), ends, 9)]
    p.append(f'<path d="{" ".join(wires)}" stroke="{INK}" stroke-width=".8" fill="none" opacity=".85"></path>')
    p.append(hp.ccgt(324, prof(360), 1.0))
    p.append(sn.solar_farm_at(470, 716, prof))
    p.append(hp.metmast(748, prof(748), 150))
    p.append(sn.lng_terminal(1040, prof(1090)))
    p.append(hp.sc(hp.gasterminal(1206, prof(1260)), 1206, prof(1260), 1.18))
    p.append(hp.sc(hp.converter(1318, prof(1360)), 1318, prof(1360), 1.02))
    labels = [
        ("onshore wind", 250, S - 300, "#E4EFEC", "middle"),
        ("offshore wind", 846, H0 - 44, "#E4EFEC", "middle"),
        ("substation", 226, S - 72, INK, "middle"),
        ("gas-fired power station", 356, S - 128, INK, "middle"),
        ("solar farm", 596, S - 72, INK, "middle"),
        ("met mast", 736, S - 146, INK, "end"),
        ("LNG carrier", 900, S - 92, INK, "middle"),
        ("LNG terminal", 1104, S - 66, INK, "middle"),
        ("gas terminal", 1262, S - 64, INK, "middle"),
        ("interconnector", 1372, S - 104, INK, "middle"),
        ("converter station", 1372, S - 89, INK, "middle"),
    ]
    lab = "".join(f'<text x="{x}" y="{y}" fill="{c}" text-anchor="{a}">{T(PG, t)}</text>' for t, x, y, c, a in labels)
    aria = T(PG, "A section from Great Britain across the North Sea to the continent. On the British side: pylons into "
                 "a substation, a gas-fired power station, a solar farm and a met mast on the coast, with onshore wind "
                 "on the ridge. The sea is cut in section, with offshore turbines on monopiles and an LNG carrier at "
                 "a jetty. On the far shore: an LNG terminal, a gas terminal and an interconnector converter station. "
                 "One cable runs down from each of these seven assets to the vendor that publishes data on it.")
    return "\n".join(p), lab, aria


def draw(m: dict) -> tuple[str, str, int]:
    hp.Y["surf"] = S
    secs = m["secs"]
    H = int(math.ceil(m["H"]))
    yb, ys, yd = secs["bronze"][0], secs["silver"][0], secs["deep"][0]
    surf = [(x, cut(x)) for x in range(-40, 1441 + 40, 10)]
    bg = strata_svg(H, S, surf, [("bronze", yb), ("silver", ys), ("deep", yd)])
    land, lab, aria = landscape()
    land_svg = (f'<svg class="layer land-svg" width="1440" height="{S + 44}" viewBox="0 0 1440 {S + 44}" role="img" '
                f'aria-label="{aria}">{land}<g class="lab">{lab}</g></svg>')
    # cables: one per vendor, west to east; the S-bends share one band so none cross
    c, ends = [], []
    order = [v[0] for v in VENDORS]
    for i, slug in enumerate(order):
        x0 = ORIG[slug]
        l, t, r, b = m["t"][f"v-{slug}"]
        tx, ty = l + 16, t
        ya, yb2 = S + 22, S + TOP_H - 30
        c.append(cable(drop(x0, cut(x0) - 3, tx, ty, ya, yb2)))
        ends.append(terminal(tx, ty))
    # system_prices, followed on down: a branch leaves the Elexon cable before its terminal and runs to silver
    l, t, r, b = m["t"]["v-elexon"]
    fl, ft, fr, fb = m["t"]["find"]
    jx, jy = l + 16, t - 40
    gx = 64
    ey = ft
    csl = ys + 8 * math.sin(gx / 210 + 2.1) + 8 * .45 * math.sin(gx / 73 + 2.1 * 2.3)
    d1 = f"M{f(jx)} {f(jy)} H{gx + 14} Q{gx} {f(jy)} {gx} {f(jy + 14)} V{f(csl)}"
    d2 = f"M{gx} {f(csl)} V{f(ey - 14)} Q{gx} {f(ey)} {gx + 14} {f(ey)} H{f(fl + 16 - 7)}"
    c.append(cable(d1, BRONZE))
    c.append(cable(d2, SILVER))
    ends.append(joint(jx, jy))
    ends.append(sleeve(gx, csl, SILVER))
    ends.append(terminal(fl + 16, ey, T_SILVER))
    cab = (f'<svg class="layer" width="1440" height="{H}" viewBox="0 0 1440 {H}" aria-hidden="true">'
           + "".join(c) + "".join(ends) + "</svg>")
    return bg + "\n" + land_svg + "\n" + cab, H


_ = (CHART, CLAY, GOLD, OLIVE, PETROL, SOFT, T_BRONZE, DAY, smooth)
