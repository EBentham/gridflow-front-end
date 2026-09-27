"""Page 4: the models landing. The sky draws what each model forecasts (demand at the substation, a wind farm, a
solar farm, the plant fleet named by the stack's tranches). Four cables drop through a compressed descent, tap
the silver datasets each model reads, and end at the entries in gold. The SMP model has no cable: its published
headline clears the stack against realised inputs, not against the other models' forecasts, and its text says so."""
from __future__ import annotations

import math

import hp
import scenery as sn
from frame import (BRONZE, CHART, CLAY, DAY, GOLD, HORIZON, INK, KHAKI, OLIVE, PACK, PETROL, SILVER, T, T_GOLD,
                   T_SILVER, cable, contact_y, f, footer, joint, masthead, sleeve, smooth, strata_svg, terminal)

NAME = "A-models"
TITLE = "Models"
PG = "models"
S = 750
FAR = "#297382"
MD = {m["name"]: m for m in PACK["models"]["models"]}
OLIVE_D = "#4E5E2B"            # a darker olive for the median line only
WIDTHS = [440, 250, 250, 250]
GAP = 30



def mn(v: float, d: int = 2) -> str:
    """Format a number with a true minus sign."""
    return f"{v:.{d}f}".replace("-", "−")

def lanes() -> list[float]:
    xs, x = [], 80.0
    for w in WIDTHS:
        xs.append(x + 16)
        x += w + GAP
    return xs


# ---------------------------------------------------------------- marks (30 x 18, copied from the drawing)
def mark(kind: str) -> str:
    if kind == "demand":      # a lattice pylon
        body = (f'<path d="M9 17 L13 3 M21 17 L17 3 M13 3 H17 M6 7 H24 M8 11 H22 M11 17 L19 9 M19 17 L11 9" '
                f'stroke="{INK}" stroke-width="1.2" fill="none"></path>')
    elif kind == "wind":
        body = (f'<path d="M14 17 L15 7 L16 17 Z" fill="{DAY}" stroke="{INK}" stroke-width=".8"></path>'
                f'<path d="M15 7 L15 0.5 M15 7 L9.5 10 M15 7 L20.5 10" stroke="{HORIZON}" stroke-width="2.2" '
                f'stroke-linecap="round"></path><circle cx="15" cy="7" r="1.6" fill="{INK}"></circle>')
    elif kind == "solar":
        body = (f'<path d="M3 13 L27 13 L24 5 L0.5 5 Z" fill="{CHART}" stroke="{INK}" stroke-width=".9"></path>'
                f'<path d="M9 13 L6.5 5 M15 13 L12.5 5 M21 13 L18.5 5 M2 9 H25.5" stroke="{INK}" stroke-width=".6" '
                f'opacity=".5"></path><path d="M7 13 V17 M23 13 V17" stroke="{INK}" stroke-width="1"></path>')
    elif kind == "stack":
        body = (f'<rect x="1" y="12" width="6" height="5" fill="{BRONZE}"></rect>'
                f'<rect x="7" y="10" width="7" height="7" fill="{PETROL}"></rect>'
                f'<rect x="14" y="6" width="9" height="11" fill="{CLAY}"></rect>'
                f'<rect x="23" y="2" width="6" height="15" fill="{CLAY}" opacity=".7"></rect>'
                f'<path d="M1 12 H7 V10 H14 V6 H23 V2 H29" fill="none" stroke="{INK}" stroke-width="1.4"></path>')
    else:                     # smp: the stack crossed by a demand line, the price read off
        body = (f'<rect x="1" y="12" width="7" height="5" fill="{PETROL}"></rect>'
                f'<rect x="8" y="8" width="12" height="9" fill="{CLAY}"></rect>'
                f'<rect x="20" y="3" width="9" height="14" fill="{CLAY}" opacity=".7"></rect>'
                f'<path d="M1 12 H8 V8 H20 V3 H29" fill="none" stroke="{INK}" stroke-width="1.3"></path>'
                f'<path d="M15 1 V17" stroke="{OLIVE}" stroke-width="1.8"></path>'
                f'<path d="M1 8 H15" stroke="{GOLD}" stroke-width="1.8"></path>')
    return f'<svg class="mk" width="30" height="18" viewBox="0 0 30 18" aria-hidden="true">{body}</svg>'


# ---------------------------------------------------------------- charts
def demand_chart() -> str:
    s = PACK["series"]["models_landing_demand"]
    pts = s["points"]
    w, h = 440, 190
    L, R, Tp, B = 50, 8, 12, 30
    pw, ph = w - L - R, h - Tp - B
    n = len(pts)
    lo_v, hi_v = 16000, 32000
    X = lambda i: L + i * pw / (n - 1)  # noqa: E731
    Y = lambda v: Tp + (hi_v - v) * ph / (hi_v - lo_v)  # noqa: E731
    up = " L".join(f"{f(X(i))} {f(Y(p[4]))}" for i, p in enumerate(pts))
    dn = " L".join(f"{f(X(i))} {f(Y(p[2]))}" for i, p in reversed(list(enumerate(pts))))
    med = "M" + " L".join(f"{f(X(i))} {f(Y(p[3]))}" for i, p in enumerate(pts))
    act = "M" + " L".join(f"{f(X(i))} {f(Y(p[1]))}" for i, p in enumerate(pts))
    g = [f'<path d="M{up} L{dn} Z" fill="{OLIVE}" opacity=".32"></path>',
         f'<path d="{med}" fill="none" stroke="{OLIVE_D}" stroke-width="1.6"></path>',
         f'<path d="{act}" fill="none" stroke="{INK}" stroke-width="1.4" stroke-dasharray="1 0"></path>']
    for v in (20000, 25000, 30000):
        g.append(f'<path d="M{L - 5} {f(Y(v))} H{L}" stroke="{INK}" stroke-width="1"></path>'
                 f'<text x="{L - 9}" y="{f(Y(v) + 4)}" text-anchor="end">{v:,}</text>')
    for i, lab in ((0, "20 Aug"), (24, "12:00"), (48, "21 Aug"), (72, "12:00")):
        g.append(f'<path d="M{f(X(i))} {Tp + ph} v6" stroke="{INK}" stroke-width="1"></path>'
                 f'<text x="{f(X(i))}" y="{Tp + ph + 21}" text-anchor="{"start" if i == 0 else "middle"}">{lab}</text>')
    g.append(f'<path d="M{L} {Tp} V{Tp + ph} H{w - R}" stroke="{INK}" stroke-width="1.2" fill="none"></path>')
    g.append(f'<text x="{L + 6}" y="{Tp + 4}" class="u">MW, UTC</text>')
    # direct labels, placed where the band is thin enough to read
    i0 = 60
    g.append(f'<text class="dl" x="{f(X(i0))}" y="{f(Y(pts[i0][4]) - 7)}" text-anchor="middle">5 to 95%</text>')
    aria = ("Day-ahead demand forecast for 20 and 21 August 2026, from gold forecasts run a55a829bc51c40b2, fold 12: "
            "the median forecast inside its 5 to 95 percent band, with the outturn line, in MW. Values run from "
            f"{min(min(p[1:]) for p in pts):,.0f} to {max(max(p[1:]) for p in pts):,.0f} MW.")
    return (f'<svg class="chart" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{aria}">'
            + "".join(g) + "</svg>")


def smp_chart() -> str:
    s = PACK["series"]["models_landing_smp"]
    pts = s["points"]
    w, h = 810, 260
    L, R, Tp, B = 50, 118, 14, 30
    pw, ph = w - L - R, h - Tp - B
    n = len(pts)
    lo_v, hi_v = -150, 200
    X = lambda i: L + 10 + i * (pw - 20) / (n - 1)  # noqa: E731
    Y = lambda v: Tp + (hi_v - v) * ph / (hi_v - lo_v)  # noqa: E731
    mdl = "M" + " L".join(f"{f(X(i))} {f(Y(p[1]))}" for i, p in enumerate(pts))
    ref = "M" + " L".join(f"{f(X(i))} {f(Y(p[2]))}" for i, p in enumerate(pts))
    g = [f'<path d="M{L} {f(Y(0))} H{L + pw}" stroke="{INK}" stroke-width=".9" stroke-dasharray="3 3" opacity=".6">'
         f'</path>']
    for v in (-100, 0, 100, 200):
        g.append(f'<path d="M{L - 5} {f(Y(v))} H{L}" stroke="{INK}" stroke-width="1"></path>'
                 f'<text x="{L - 9}" y="{f(Y(v) + 4)}" text-anchor="end">{mn(v, 0)}</text>')
    for i in (0, 7, 14):
        d = pts[i][0]
        g.append(f'<path d="M{f(X(i))} {Tp + ph} v6" stroke="{INK}" stroke-width="1"></path>'
                 f'<text x="{f(X(i))}" y="{Tp + ph + 21}" text-anchor="middle">{int(d[8:])} '
                 f'{"Aug" if d[5:7] == "08" else "Sep"}</text>')
    g.append(f'<path d="M{L} {Tp} V{Tp + ph} H{L + pw}" stroke="{INK}" stroke-width="1.2" fill="none"></path>')
    g.append(f'<text x="{L + 6}" y="{Tp + 4}" class="u">GBP/MWh</text>')
    g.append(f'<path d="{ref}" fill="none" stroke="{INK}" stroke-width="1.5"></path>')
    g.append(f'<path d="{mdl}" fill="none" stroke="{GOLD}" stroke-width="2.4"></path>')
    g.append(f'<g fill="{INK}">' + "".join(f'<circle cx="{f(X(i))}" cy="{f(Y(p[2]))}" r="2.2"></circle>'
                                          for i, p in enumerate(pts)) + "</g>")
    g.append(f'<g fill="{GOLD}" stroke="{INK}" stroke-width=".8">' + "".join(
        f'<circle cx="{f(X(i))}" cy="{f(Y(p[1]))}" r="2.8"></circle>' for i, p in enumerate(pts)) + "</g>")
    xe = X(n - 1) + 10
    g.append(f'<text class="dl" x="{f(xe)}" y="{f(Y(pts[-1][2]) + 4)}">APXMIDP</text>'
             f'<text class="dl" x="{f(xe)}" y="{f(Y(pts[-1][1]) + 4)}">model clearing</text>')
    aria = ("Daily mean GB price, 18 August to 3 September 2026, GBP/MWh: the Elexon MID APXMIDP benchmark stays "
            "between about 90 and 167, while the fundamentals SMP model's clearing price sits below it every day, "
            f"from {mn(min(p[1] for p in pts), 1)} to {mn(max(p[1] for p in pts), 1)}.")
    return (f'<svg class="chart" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{aria}">'
            + "".join(g) + "</svg>")


# ---------------------------------------------------------------- content
def entry(i: int, kind: str, name: str, ids: list[str], parts: str, cls: str = "") -> str:
    idl = "".join(f"<code>{x}</code>" for x in ids)
    return (f'<article class="model {cls}" data-t="m{i}" aria-labelledby="m{i}-h">'
            f'<p class="land">{idl}</p>'
            f'<h2 id="m{i}-h">{mark(kind)}<span>{name}</span></h2>{parts}</article>')


INPUTS = [
    [("elexon/indo", "target"), ("open_meteo/historical_demand", "weather, version 2")],
    [("elexon/fuelhh", "WIND, the target"), ("open_meteo/historical_wind", "12 sites"), ("elexon/windfor", "benchmark")],
    [("elexon/fuelhh", "SOLAR, the target"), ("open_meteo/historical_solar", "6 sites")],
    [("elexon/bmunits_reference", "units"), ("elexon/remit", "availability"), ("elexon/fou2t14d", "derating")],
]


def html() -> tuple[str, str]:
    lede = (f'<p class="lead">{T(PG, "gridflow-models is a separate library that reads gridflow’s DuckDB catalogue and Parquet.")}</p>'
            f'<p>{T(PG, "It holds models for demand, wind and solar, a GB merit-order stack, and a model that clears the stack into a day-ahead price. It does not produce orders.")}</p>'
            f'<p><a class="alt" href="#">{T(PG, "Read the model cards")}</a></p>')
    sky = (f'<section class="sky" data-st="sky" style="height: {S}px" aria-labelledby="h1">{masthead("Models")}'
           f'<div class="hero"><div><h1 id="h1">{T(PG, "Five models, from demand to the day-ahead price")}</h1></div>'
           f'<div class="lede">{lede}</div></div></section>')
    top = '<div class="st st-top" data-st="topsoil" style="height: 92px" aria-hidden="true"></div>'
    bronze = '<div class="st st-bronze" data-st="bronze" style="height: 58px" aria-hidden="true"></div>'
    cols = []
    for i, ins in enumerate(INPUTS):
        li = "".join(f'<li data-t="in{i}-{k}"><code>{a}</code> <span>{T(PG, b)}</span></li>' for k, (a, b) in enumerate(ins))
        cols.append(f'<ul style="width: {WIDTHS[i]}px">{li}</ul>')
    silver = (f'<div class="st st-silver" data-st="silver"><div class="inputs" role="group" '
              f'aria-label="{T(PG, "What each model reads from silver")}">{"".join(cols)}</div></div>')

    d = MD["Day-ahead demand"]["metrics"]
    dem = (f'<p class="md">{T(PG, "GB national demand outturn, half-hourly in MW, forecast a day ahead. LightGBM quantile regression, one model per quantile from 0.05 to 0.95, sorted so they never cross, with a conformal outer band. Version 2 adds weather and calendar features.")}</p>'
           f'<table class="sc"><caption>{T(PG, "Walk-forward backtest, 12 folds of 30 days, 1 September 2024 to 22 August 2026")}</caption>'
           f'<thead><tr><th scope="col"></th><th scope="col">{T(PG, "pinball, q0.5")}</th><th scope="col">{T(PG, "coverage, 5 to 95%")}</th></tr></thead>'
           f'<tbody><tr><th scope="row">v1</th><td>{d[0]["pinball_q0.5_mw"]:.2f} MW</td><td>{d[0]["coverage_90"]:.3f}</td></tr>'
           f'<tr><th scope="row">v2</th><td>{d[1]["pinball_q0.5_mw"]:.2f} MW</td><td>{d[1]["coverage_90"]:.3f}</td></tr></tbody></table>'
           f'<p class="mn">{T(PG, "v2 is scored with actual weather standing in for the forecast, so its score is optimistic.")}</p>'
           f'<figure class="fig">{demand_chart()}<figcaption>{T(PG, "v1, fold 12, 20 and 21 August 2026: the median (olive) inside its 5 to 95% band, and the outturn from elexon/indo (ink). Run a55a829bc51c40b2, forecast issued at noon the day before.")}</figcaption></figure>'
           f'<p class="hd"><code>models.demand_forecast</code>, <code>models.demand_forecast_v2</code></p>')
    wind = (f'<p class="md">{T(PG, "GB wind outturn, half-hourly in MW, a day ahead. LightGBM quantile regression on weather at 12 sites, benchmarked against WINDFOR.")}</p>'
            f'<p class="ex">{T(PG, "A configuration, a model card and a training dataset exist. There are no forecasts or scores in gold.")}</p>'
            f'<p class="hd"><code>models.wind_forecast</code></p>')
    solar = (f'<p class="md">{T(PG, "GB solar, half-hourly, a day ahead. LightGBM quantile regression on weather at 6 sites, benchmarked against persistence.")}</p>'
             f'<p class="ex">{T(PG, "Its configured target, elexon/fuelhh SOLAR, holds no rows. A configuration and a model card exist; there are no forecasts or scores in gold.")}</p>'
             f'<p class="hd"><code>models.solar_forecast</code></p>')
    stack = (f'<p class="md">{T(PG, "The GB supply curve for one settlement period: units ranked by short-run marginal cost, cumulative MW against GBP/MWh, floored at −500.")}</p>'
             f'<p class="ex">{T(PG, "It is built when called, with nothing to train. It is scored through the SMP model, and its curves are kept in gold with each SMP run.")}</p>'
             f'<p class="hd"><code>models.stack.build(as_of)</code></p>')
    sm = MD["Fundamentals SMP"]["metrics"]
    smp = (f'<div class="smp-l"><p class="md">{T(PG, "Clears the stack against realised residual demand (demand less wind, solar and signed netting) for every half-hour, and scores the price against Elexon MID APXMIDP, the GB day-ahead benchmark.")}</p>'
           f'<table class="sc"><thead><tr><th scope="col"></th><th scope="col">{T(PG, "mean bias")}</th><th scope="col">MAE</th></tr></thead><tbody>'
           f'<tr><th scope="row">{T(PG, "Headline, 18 August to 3 September 2026, 816 periods")}</th><td>{mn(sm[0]["mean_bias_gbp_mwh"])}</td><td>{sm[0]["mae_gbp_mwh"]:.2f}</td></tr>'
           f'<tr><th scope="row">{T(PG, "13 monthly runs, 5 May 2025 to 4 May 2026, 17,520 periods")}</th><td>{mn(sm[1]["mean_bias_gbp_mwh"])}</td><td>{sm[1]["mae_gbp_mwh"]:.2f}</td></tr>'
           f'</tbody></table><p class="mn">{T(PG, "GBP/MWh. In the headline run every period is under-predicted.")}</p>'
           f'<p class="hd"><code>models.fundamentals_smp.backtest(...)</code></p></div>'
           f'<figure class="fig smp-r"><h3>{T(PG, "Daily mean price, 18 August to 3 September 2026")}</h3>{smp_chart()}'
           f'<figcaption>{T(PG, "Model clearing (gold) against APXMIDP (ink), daily means of the 816 half-hours in run 41de423cfc0b421e. A perfect-prognosis backtest: realised demand, wind and solar stand in for forecasts. Fuel and carbon prices are synthetic. APXMIDP mixes day-ahead and intraday trades. Clearing is floored at −500 GBP/MWh, which pulls some daily means below zero.")}</figcaption></figure>')
    ents = (entry(0, "demand", T(PG, "Day-ahead demand"), ["day_ahead.lgbm_demand.v1", "v2"], dem, "w-dem")
            + entry(1, "wind", T(PG, "Wind generation"), ["wind.lgbm_quantile.v1"], wind)
            + entry(2, "solar", T(PG, "Solar generation"), ["solar.lgbm_quantile.v1"], solar)
            + entry(3, "stack", T(PG, "GB merit-order stack"), ["stack.gb.v1"], stack))
    reading = (f'<div class="read"><div><h2 class="fig-h" id="r-h">{T(PG, "Reading the scores")}</h2>'
               f'<p class="body">{T(PG, "Every score here is a backtest held in gold. Pinball loss at q0.5 is half the mean absolute error of the median forecast, in MW; coverage is the share of outturns inside the 5 to 95% band. A demand model passes when pinball is at most 1,500 MW, coverage is within 0.90 ± 0.05 and no quantiles cross.")}</p></div>'
               f'<div><p class="mini">{T(PG, "In a notebook")}</p><pre class="well"><span class="k">from</span> gridflow_models <span class="k">import</span> setup_notebook\n'
               f'data, models, common = setup_notebook()\nmodels.list()</pre></div></div>')
    gold = (f'<section class="st st-gold" data-st="gold" aria-label="{T(PG, "The five models")}">'
            f'<div class="mgrid">{ents}'
            f'<article class="model smp" data-t="m4" aria-labelledby="m4-h"><p class="land"><code>fundamentals_smp.gb.v1</code></p>'
            f'<h2 id="m4-h">{mark("smp")}<span>{T(PG, "Fundamentals SMP")}</span></h2><div class="smp-g">{smp}</div></article>'
            f'</div>{reading}</section>')
    body = "\n".join([sky, top, bronze, silver, gold, footer(PG)])
    return body, CSS


CSS = """.inputs{display:flex;column-gap:30px;padding:26px 0 22px}
.inputs ul{list-style:none;margin:0;padding:0 0 0 30px;box-sizing:border-box}
.inputs li{font-size:13px;line-height:1.35;padding:3px 0 5px;color:#3F4A3B}
.inputs code{font-size:13px;color:#1C2B22}
.inputs span{font-style:italic}
.mgrid{display:grid;grid-template-columns:440px 250px 250px 250px;column-gap:30px;padding:70px 0 0;align-items:start}
.model .land{margin:0 0 10px;height:18px;padding-left:30px;font-size:13px;line-height:18px;transform:translateY(-9px);color:#1C2B22;display:flex;gap:10px;white-space:nowrap}
.model .land code{font-size:13px}
.model h2{display:flex;align-items:center;gap:12px;font-size:23px;font-weight:720;font-stretch:90%;line-height:1.1;letter-spacing:-.01em;margin:0 0 10px}
.mk{display:block;flex:none}
.model .md{margin:0 0 12px;font-size:14.5px;line-height:1.5;color:#3F4A3B}
.model .ex{margin:0 0 12px;font-size:14.5px;line-height:1.5;color:#1C2B22;font-weight:600}
.model .hd{margin:12px 0 0;font-size:13px;line-height:1.5;color:#1C2B22}
.model .hd code{font-size:13px;color:#155A6E}
.model .mn{margin:6px 0 0;font-size:13.5px;line-height:1.45;color:#3F4A3B}
.sc{border-collapse:collapse;width:100%;font-size:14px;color:#1C2B22;margin:4px 0 0}
.sc caption{text-align:left;font-size:13.5px;line-height:1.45;color:#3F4A3B;padding:0 0 6px}
.sc th,.sc td{padding:6px 0;border-bottom:1px solid rgba(28,43,34,.22);text-align:right;font-weight:400}
.sc thead th{font-size:13px;color:#3F4A3B;font-style:italic;border-bottom:1px solid #1C2B22;vertical-align:bottom;white-space:nowrap}
.sc tbody th{text-align:left;font-weight:600;padding-right:14px}
.sc td{font-weight:600;padding-left:12px;white-space:nowrap}
.fig{margin:18px 0 0}
.fig figcaption{margin:6px 0 0;font-size:13.5px;line-height:1.5;color:#3F4A3B}
.w-dem{grid-row:1 / span 2}
.model.smp{grid-column:2 / span 3;grid-row:2;padding:64px 0 0}
.model.smp .land{padding-left:0}
.model.smp h2{font-size:32px;font-stretch:86%;line-height:1.02}
.smp-g{display:grid;grid-template-columns:minmax(0,1fr);row-gap:26px;align-items:start}
.smp-l{display:grid;grid-template-columns:330px minmax(0,1fr);column-gap:40px;align-items:start}
.smp-l .md{grid-row:1 / span 3}
.smp-l .sc tbody th{font-weight:500;font-size:13.5px;line-height:1.4}
.smp-r{margin:0}
.smp-r h3{font-size:18px;font-weight:700;font-stretch:92%;margin:0 0 10px}
.smp-r figcaption{max-width:66ch}
.read{display:grid;grid-template-columns:620px minmax(0,1fr);column-gap:100px;padding:74px 0 86px;align-items:start}
.mini{margin:0 0 8px;font-size:14.5px;font-weight:600;color:#1C2B22}
.chart text.u{font-size:12.5px}
"""


# ---------------------------------------------------------------- drawing
def landscape() -> tuple[str, str, str]:
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
    # demand: the pylon line into the substation
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
    # wind: a wind farm standing on the cut
    for i, (tx, hh) in enumerate([(468, 150), (560, 136), (640, 124)]):
        p.append(hp.turbine(tx, hp.prof(tx), hh, hh * .5, ["sp1", "sp2", "sp3"][i], 25 + 40 * i))
    # solar
    p.append(sn.solar_farm_at(690, 900, hp.prof))
    # the plant fleet, in merit order: biomass, nuclear, CCGT, OCGT
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
    labels = [
        ("substation", 184, S - 72, INK, "middle"),
        ("onshore wind", 330, S - 262, "#E4EFEC", "middle"),
        ("wind farm", 700, S - 176, INK, "middle"),
        ("solar farm", 796, S - 72, INK, "middle"),
        ("biomass", 990, S - 50, INK, "middle"),
        ("nuclear", 1100, S - 88, INK, "middle"),
        ("CCGT", 1250, S - 120, INK, "middle"),
        ("OCGT", 1384, S - 58, INK, "middle"),
    ]
    lab = "".join(f'<text x="{x}" y="{y}" fill="{c}" text-anchor="{a}">{T(PG, t)}</text>' for t, x, y, c, a in labels)
    aria = T(PG, "What the models forecast, drawn: pylons into a substation for national demand, a wind farm, a solar "
                 "farm, and the plant fleet in merit order (biomass, nuclear, CCGT and OCGT). A cable runs down from "
                 "each to its model, tapping the datasets it reads on the way.")
    return "\n".join(p), lab, aria


ORIG = [184, 560, 796, 1180]


def draw(m: dict) -> tuple[str, int]:
    hp.Y["surf"] = S
    secs = m["secs"]
    H = int(math.ceil(m["H"]))
    yb, ys, yg, yd = secs["bronze"][0], secs["silver"][0], secs["gold"][0], secs["deep"][0]
    surf = [(x, hp.prof(x)) for x in range(-40, 1481, 10)]
    bg = strata_svg(H, S, surf, [("bronze", yb), ("silver", ys), ("gold", yg), ("deep", yd)])
    land, lab, aria = landscape()
    land_svg = (f'<svg class="layer land-svg" width="1440" height="{S + 16}" viewBox="0 0 1440 {S + 16}" role="img" '
                f'aria-label="{aria}">{land}<g class="lab">{lab}</g></svg>')
    c, ends = [], []
    for i, (x0, lx) in enumerate(zip(ORIG, lanes())):
        l, t, r, b = m["t"][f"m{i}"]
        tx, ty = l + 16, t
        c_bs, c_sg = contact_y("silver", ys, tx), contact_y("gold", yg, tx)
        pts = [(x0, hp.prof(x0) - 3), (x0, S + 10)]
        for k in range(1, 12):
            tt = k / 12
            s2 = tt * tt * (3 - 2 * tt)
            pts.append((x0 + (tx - x0) * s2, S + 10 + 66 * tt))
        pts.append((tx, S + 76))
        c.append(cable(smooth(pts) + f" V{f(c_bs)}", BRONZE))
        c.append(cable(f"M{f(tx)} {f(c_bs)} V{f(c_sg)}", SILVER))
        c.append(cable(f"M{f(tx)} {f(c_sg)} V{f(ty)}", GOLD))
        ends.append(sleeve(tx, c_bs, SILVER))
        ends.append(sleeve(tx, c_sg, GOLD))
        k = 0
        while f"in{i}-{k}" in m["t"]:
            il, it, ir, ib = m["t"][f"in{i}-{k}"]
            ends.append(joint(tx, it + 12))
            k += 1
        ends.append(terminal(tx, ty, T_GOLD))
    cab = (f'<svg class="layer" width="1440" height="{H}" viewBox="0 0 1440 {H}" aria-hidden="true">'
           + "".join(c) + "".join(ends) + "</svg>")
    return bg + "\n" + land_svg + "\n" + cab, H


_ = (KHAKI, T_SILVER, lanes)
