"""E-models: the models landing sheet. Plate: how the five fit together (demand, less wind, less solar, cleared against
the merit-order stack, gives a price), drawn without scales; the keyed index states what exists for each, neutrally."""
from __future__ import annotations

from sheet import (BRONZE, CHART, CLAY, DAY, G, GOLD, HORIZON, INK, KHAKI, OLIVE, ONP2, PACK, PETROL, a_gas_station,
                   a_solar, band, block, deep, esc, f, height_for, land_top, line_chart, page, sky, sky_svg,
                   sub_contact, turbine, write)

W = 840
PX, BY, SW, PH = 150, 240, 640, 196
ROWS = {"s": 300, "w": 370, "d": 440}
BAR = 14
MU_R, SOLAR_M, WIND_M = .56, .08, .20
SD = {"d": .035, "w": .07, "s": .025}
TRANCHES = [("biomass", .08, [.13], BRONZE), ("nuclear", .16, [.17], PETROL),
            ("CCGT", .48, [.30 + .028 * k for k in range(8)], CLAY), ("coal", .10, [.62], KHAKI),
            ("OCGT", .12, [.80, .93], CLAY)]
X = lambda q: PX + q * SW  # noqa: E731


def units() -> list[tuple[float, float, float, str, str]]:
    out, acc = [], 0.0
    for name, share, costs, fill in TRANCHES:
        w = share / len(costs)
        for c in costs:
            out.append((acc, acc + w, c, fill, name))
            acc += w
    return out


def cost_at(q: float) -> float:
    for a, b, c, _, _ in units():
        if a <= q < b:
            return c
    return 1.0


def fan(cx: float, sd: float, y: float, fill: str) -> str:
    o, i, h = 1.645 * sd * SW, .674 * sd * SW, BAR + 10
    return (f'<rect x="{f(cx - o)}" y="{f(y - h / 2)}" width="{f(2 * o)}" height="{h}" fill="{fill}" opacity=".38" '
            f'stroke="{INK}" stroke-width=".6"></rect>'
            f'<rect x="{f(cx - i)}" y="{f(y - h / 2)}" width="{f(2 * i)}" height="{h}" fill="{fill}" opacity=".8"></rect>'
            f'<path d="M{f(cx)} {f(y - h / 2 - 3)} V{f(y + h / 2 + 3)}" stroke="{INK}" stroke-width="1.8"></path>')


def bar_row(y: float, segs: list[tuple[float, float, str, str]]) -> str:
    return "".join(f'<rect x="{f(a)}" y="{f(y - BAR / 2)}" width="{f(b - a)}" height="{BAR}" fill="{c}" opacity="{op}">'
                   f'</rect>' for a, b, c, op in segs)


def drawing() -> str:
    g, t = [], []
    # the stack
    us = units()
    for a, b, c, fill, _ in us:
        g.append(f'<rect x="{f(X(a))}" y="{f(BY - c * PH)}" width="{f(X(b) - X(a))}" height="{f(c * PH)}" '
                 f'fill="{fill}" stroke="{INK}" stroke-width=".7"></rect>')
    step = f"M{PX} {BY}" + "".join(f" V{f(BY - c * PH)} H{f(X(b))}" for a, b, c, _, _ in us)
    g.append(f'<path d="{step}" fill="none" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"></path>')
    lab = {"biomass": (X(0) + 2, BY - .13 * PH - 8, INK, "start"), "nuclear": (X(.08) + 8, BY - 9, DAY, "start"),
           "CCGT": (X(.24) + 8, BY - 9, INK, "start"), "coal": (X(.72) + 6, BY - .62 * PH - 8, INK, "start"),
           "OCGT": (X(.82) + 6, BY - .93 * PH - 8, INK, "start")}
    for name, (x, y, col, anc) in lab.items():
        t.append(f'<text x="{f(x)}" y="{f(y)}" fill="{col}" text-anchor="{anc}">{name}</text>')
    # the inputs, measured along the capacity axis from zero
    xr, xw, xd = X(MU_R), X(MU_R + SOLAR_M), X(MU_R + SOLAR_M + WIND_M)
    rs, rw, rd = ROWS["s"], ROWS["w"], ROWS["d"]
    g.append(bar_row(rd, [(PX, xd, OLIVE, ".4")]) + fan(xd, SD["d"], rd, OLIVE))
    g.append(bar_row(rw, [(PX, xw, OLIVE, ".4"), (xw, xd, HORIZON, "1")]) + fan(xw, SD["w"], rw, HORIZON))
    g.append(bar_row(rs, [(PX, xr, OLIVE, ".4"), (xr, xw, CHART, "1"), (xw, xd, HORIZON, ".3")]) + fan(xr, SD["s"], rs, CHART))
    hb = BAR / 2 + 8
    yc = BY - cost_at(MU_R) * PH
    g.append(f'<path d="M{f(xd)} {rd - hb} V{rw + BAR / 2} M{f(xw)} {rw - hb} V{rs + BAR / 2} M{f(xr)} {rs - hb} V{f(yc)}" '
             f'stroke="{INK}" stroke-width="1" stroke-dasharray="1.5 3"></path>')
    g.append(f'<path d="M{f(xr)} {f(yc)} H{PX}" stroke="{INK}" stroke-width="1" stroke-dasharray="1.5 3"></path>')
    g.append(f'<circle cx="{f(xr)}" cy="{f(yc)}" r="3.6" fill="{INK}"></circle>')
    g.append(f'<rect x="{PX - 16}" y="{f(yc - 3.5)}" width="16" height="7" fill="{GOLD}" stroke="{INK}" '
             f'stroke-width="1"></rect>')
    # axes, words only
    g.append(f'<path d="M{PX} {BY} V14 M{PX} {BY} H{PX + SW + 16}" stroke="{INK}" stroke-width="1.5" fill="none"></path>')
    t += [f'<text x="{PX + 10}" y="22" fill="{INK}">price</text>',
          f'<text x="{PX + SW + 16}" y="{BY + 22}" fill="{INK}" text-anchor="end">capacity, cheapest first</text>',
          f'<text x="{PX - 22}" y="{f(yc + 5)}" fill="{INK}" text-anchor="end">clearing price</text>',
          f'<text x="{PX - 12}" y="{BY + 22}" fill="{INK}" text-anchor="end">residual demand</text>',
          f'<text x="{PX - 12}" y="{rs + 5}" fill="{INK}" text-anchor="end">less solar</text>',
          f'<text x="{PX - 12}" y="{rw + 5}" fill="{INK}" text-anchor="end">less wind</text>',
          f'<text x="{PX - 12}" y="{rd + 5}" fill="{INK}" text-anchor="end">demand</text>']
    g.append(f'<path d="M{f(xr)} {BY - 4} V{BY + 4}" stroke="{INK}" stroke-width="2"></path>')
    h = rd + 26
    aria = ("How the five models fit together, drawn without scales. Read from the bottom: a demand forecast is a bar "
            "along the capacity axis with its spread at the end; the wind forecast is carved off that end, then the "
            "solar forecast. What is left is residual demand. Above, the merit-order stack rises in steps: biomass, "
            "nuclear, a long run of CCGT units, coal, then OCGT. Where residual demand meets the stack, a clearing "
            "price is read off the price axis.")
    return (f'<svg width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" aria-label="{esc(aria)}">'
            + "".join(g) + '<g font-family="Hanken Grotesk" font-style="italic" font-size="14">' + "".join(t)
            + "</g></svg>")


def mark(kind: str) -> str:
    if kind == "stack":
        body = (f'<rect x="1" y="12" width="7" height="5" fill="{PETROL}"></rect>'
                f'<rect x="8" y="8" width="13" height="9" fill="{CLAY}"></rect>'
                f'<rect x="21" y="3" width="8" height="14" fill="{CLAY}"></rect>'
                f'<path d="M1 12 H8 V8 H21 V3 H29" fill="none" stroke="{INK}" stroke-width="1.4"></path>')
    elif kind == "smp":
        body = (f'<path d="M6 1 V17" stroke="{INK}" stroke-width="1.4"></path><path d="M6 9 H28" stroke="{INK}" '
                f'stroke-width="1" stroke-dasharray="1.5 2.5"></path><rect x="1" y="6.5" width="5" height="5" '
                f'fill="{GOLD}" stroke="{INK}" stroke-width=".9"></rect><circle cx="27" cy="9" r="2" fill="{INK}"></circle>')
    elif kind == "solar":
        body = (f'<rect x="1" y="6" width="10" height="6" fill="{OLIVE}" opacity=".5"></rect>'
                f'<rect x="11" y="6" width="10" height="6" fill="{CHART}"></rect>'
                f'<rect x="21" y="6" width="8" height="6" fill="{HORIZON}" opacity=".3"></rect>'
                f'<rect x="7" y="3" width="8" height="12" fill="{CHART}" opacity=".38" stroke="{INK}" '
                f'stroke-width=".6"></rect><path d="M11 1 V17" stroke="{INK}" stroke-width="1.6"></path>')
    elif kind == "wind":
        body = (f'<rect x="1" y="6" width="13" height="6" fill="{OLIVE}" opacity=".5"></rect>'
                f'<rect x="14" y="6" width="15" height="6" fill="{HORIZON}"></rect>'
                f'<rect x="7" y="3" width="14" height="12" fill="{HORIZON}" opacity=".38" stroke="{INK}" '
                f'stroke-width=".6"></rect><path d="M14 1 V17" stroke="{INK}" stroke-width="1.6"></path>')
    else:
        body = (f'<rect x="1" y="6" width="22" height="6" fill="{OLIVE}" opacity=".5"></rect>'
                f'<rect x="17" y="3" width="12" height="12" fill="{OLIVE}" opacity=".38" stroke="{INK}" '
                f'stroke-width=".6"></rect><rect x="20" y="3" width="6" height="12" fill="{OLIVE}" opacity=".8"></rect>'
                f'<path d="M23 1 V17" stroke="{INK}" stroke-width="1.6"></path>')
    return f'<svg class="mk" width="30" height="18" viewBox="0 0 30 18" aria-hidden="true">{body}</svg>'


KEY = [("stack", "GB merit-order stack", "stack.gb.v1", "Built on demand; no standalone metric"),
       ("smp", "Fundamentals SMP", "fundamentals_smp.gb.v1", "Backtests published, scored against APXMIDP"),
       ("solar", "Solar generation", "solar.lgbm_quantile.v1", "Config and model card; its target has no rows"),
       ("wind", "Wind generation", "wind.lgbm_quantile.v1", "Config, model card, training file; no forecasts"),
       ("demand", "Day-ahead demand", "day_ahead.lgbm_demand.v1, .v2", "v1 backtest: pinball q0.5 711.04 MW")]


def plate() -> str:
    yc = BY - cost_at(MU_R) * PH
    tops = [22, yc - 9, ROWS["s"] - 9, ROWS["w"] - 9, ROWS["d"] - 9]
    items = []
    for i, (kind, name, mid, st) in enumerate(KEY):
        h = (tops[i + 1] - tops[i]) if i + 1 < len(tops) else 70
        items.append(f'<li style="height: {f(h)}px">{mark(kind)}<div><h3><a href="#">{name}</a></h3>'
                     f'<p class="id">{mid}</p><p class="f">{st}</p></div></li>')
    cap = ("Read from the bottom: demand, less wind and less solar, leaves residual demand; cleared against the "
           "merit-order stack, it gives a price. The published price backtests use realised inputs in place of the "
           "three forecasts.")
    inner = (f'<h2 class="ph" id="p-h">How the five fit together</h2><div class="pgrid">'
             f'<ul class="ix" style="margin-top: {f(tops[0])}px" aria-label="The five models, keyed to the drawing">'
             f'{"".join(items)}</ul><figure class="pfig">{drawing()}<figcaption>{cap}</figcaption></figure></div>')
    return band("topsoil", 14, inner, "plate", "p-h")


# ---------------------------------------------------------------- register (bronze)
REG = [
    ("Day-ahead demand", "<code>day_ahead.lgbm_demand.v1</code><br><code>day_ahead.lgbm_demand.v2</code>",
     [("Target", "GB national demand outturn, half-hourly, MW: <code>elexon/indo</code>, "
                 "<code>initial_demand_outturn_mw</code>"),
      ("Method", "LightGBM quantile regression, one model per quantile from 0.05 to 0.95, sorted to be monotone, "
                 "with a conformal (CQR) outer band. v2 adds weather and calendar features."),
      ("Horizon", "24 hours ahead"),
      ("What exists", "21 v1 versions and one v2 version in the manifest, all with status <code>validated</code>; walk-forward backtests in "
                      "gold; one issued v2 forecast, 4 to 6 September 2026.")]),
    ("Wind generation", "<code>wind.lgbm_quantile.v1</code>",
     [("Target", "GB wind outturn, half-hourly, MW: <code>elexon/fuelhh</code> WIND"),
      ("Method", "LightGBM quantile regression on weather at 12 wind sites; benchmark WINDFOR."),
      ("Horizon", "24 hours ahead"),
      ("What exists", "A config, a model card and a training dataset file, with no manifest entry, forecasts or metrics.")]),
    ("Solar generation", "<code>solar.lgbm_quantile.v1</code>",
     [("Target", "Configured as <code>elexon/fuelhh</code> SOLAR, which has no rows"),
      ("Method", "LightGBM quantile regression on weather at 6 solar sites; benchmark persistence."),
      ("Horizon", "24 hours ahead"),
      ("What exists", "A config and a model card, with no manifest entry, forecasts or metrics.")]),
    ("GB merit-order stack", "<code>stack.gb.v1</code>",
     [("Target", "The GB supply curve at one settlement period: units by short-run marginal cost, cumulative MW, "
                 "GBP/MWh, floor −500"),
      ("Method", "Constructive, no training: BM-unit inventory from <code>bmunits_reference</code>, availability from "
                 "<code>remit</code>, commodity prices from a manual file, per-technology parameters from config."),
      ("Horizon", "A point in time: a decision time and a target period"),
      ("What exists", "Builds on demand; its supply-curve points are published in gold with each SMP run.")]),
    ("Fundamentals SMP", "<code>fundamentals_smp.gb.v1</code>",
     [("Target", "GB day-ahead system marginal price, half-hourly, GBP/MWh, scored against <code>elexon/mid</code> "
                 "APXMIDP"),
      ("Method", "The stack cleared against residual demand (demand less wind, solar and signed netting), with "
                 "realised inputs in place of forecasts."),
      ("Horizon", "Day-ahead, half-hourly"),
      ("What exists", "A published headline backtest and 13 monthly diagnostic runs in gold.")]),
]


def register() -> str:
    rows = []
    for name, ids, dl in REG:
        dls = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in dl)
        rows.append(f'<li><div><h3><a href="#">{name}</a></h3><p class="sk">{ids}</p></div><div><dl>{dls}</dl></div></li>')
    return band("bronze", 26, block("reg-h", "Every model, in full",
                                    "Five models, one of them in two versions, as configured in gridflow-models.",
                                    f'<ul class="reg mdl">{"".join(rows)}</ul>'), "det", "reg-h")


# ---------------------------------------------------------------- specimen (silver)
def specimen() -> str:
    s = PACK["series"]["models_landing_demand"]
    pts = s["points"]
    act, lo, med, hi = ([p[i] for p in pts] for i in (1, 2, 3, 4))
    Yv = lambda v: 18 + (32000 - v) / (32000 - 16000) * (320 - 18 - 34)  # noqa: E731
    xt = [(0, "20 Aug"), (24, "12:00"), (48, "21 Aug"), (72, "12:00")]
    series = [{"v": act, "c": INK, "w": 1.6, "label": "outturn", "ly": Yv(act[-1]) - 9},
              {"v": med, "c": OLIVE, "w": 1.6, "label": "median forecast", "ly": Yv(med[-1]) + 9}]
    band_ = (lo, hi, OLIVE, ".26", "5% to 95%", Yv(hi[-1]) - 4)
    aria = ("Chart of the day-ahead demand forecast against outturn, 20 to 21 August 2026, half-hourly, in MW: a band "
            "from the 5% to the 95% quantile, the median forecast, and the outturn, which stays inside the band for "
            "most of the two days.")
    svg = line_chart(840, 320, len(act), 16000, 32000,
                     [(18000, "18,000"), (22000, "22,000"), (26000, "26,000"), (30000, "30,000")], xt, series, aria,
                     band=band_, ylab="MW", mr=130)
    cap = ("gold <code>forecasts</code>, run <code>a55a829bc51c40b2</code>, <code>day_ahead.lgbm_demand.v1</code>, "
           "walk-forward fold 12, issued vintage: outturn, q0.05, q0.5 and q0.95. MW, 20 to 21 August 2026, "
           "half-hourly, UTC.")
    gloss = "Two days from the last fold of the v1 backtest: the 90% band, the median, and what happened."
    return band("silver", 40, block("spec-h", "Demand forecast against outturn", gloss,
                                    f'<figure class="fig">{svg}<figcaption>{cap}</figcaption></figure>'), "det", "spec-h")


# ---------------------------------------------------------------- reach + checks (gold)
def reach_checks() -> str:
    lc = [
        ("Set up", "One handle per configured model; <code>list()</code> lists them.",
         '<span class="k">from</span> gridflow_models <span class="k">import</span> setup_notebook\n'
         "data, models, common = setup_notebook()\nmodels.list()"),
        ("Demand", "Also <code>train</code>, <code>validate</code>, <code>show_folds</code>, <code>predictions</code> "
                   "and <code>model_card</code>; v2 is <code>models.demand_forecast_v2</code>.",
         "models.demand_forecast.predict(...)"),
        ("Stack", "Build the supply curve for a decision time, then clear it against a demand.",
         "models.stack.build(as_of)\nmodels.stack.clear(as_of, demand_mw)"),
        ("Fundamentals SMP", "Also <code>assemble</code>, <code>components</code> and <code>predictions</code>.",
         "models.fundamentals_smp.backtest(...)"),
    ]
    rows = "".join(f'<li><div><h3>{a}</h3><p>{b}</p></div><pre class="well">{c}</pre></li>' for a, b, c in lc)
    reach = block("reach-h", "Reach it from code", "Notebooks are call sites only; the model logic lives in the library.",
                  f'<ul class="lc">{rows}</ul>')
    gates = [
        ("Pinball q0.5", "The mean quantile loss at 0.5: half the mean absolute error of the median forecast, in MW. "
                         "Gate: at most 1,500."),
        ("coverage_90", "The share of outturns inside q0.05 to q0.95, bounds included. Gate: within 0.90 ± 0.05."),
        ("Crossings", "Quantiles that cross each other. Gate: none."),
    ]
    dl = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in gates)
    t1 = ('<div class="dfw"><table class="df"><caption>day_ahead.lgbm_demand, walk-forward backtests</caption><thead><tr>'
          '<th></th><th>run</th><th>pinball q0.5, MW</th><th>coverage_90</th><th>crossings</th><th>gates</th></tr></thead>'
          '<tbody><tr><th>v1</th><td>a55a829bc51c40b2</td><td>711.04</td><td>0.893</td><td>0</td><td>pass</td></tr>'
          '<tr><th>v2</th><td>b367a742aa544f8f</td><td>599.72</td><td>0.883</td><td>0</td><td>pass</td></tr></tbody>'
          '</table></div>'
          '<p class="dnote">Both over the same 12 folds of 30 days, 1 September 2024 to 22 August 2026, 17,279 '
          'half-hours. v2 used actual ERA5 weather as if it were a forecast, so its score is optimistic; its model card '
          'calls the 15.7% gain an upper bound, from one run.</p>')
    t2 = ('<div class="dfw"><table class="df"><caption>fundamentals_smp.gb.v1, against APXMIDP</caption><thead><tr>'
          '<th></th><th>window</th><th>periods</th><th>mean bias, GBP/MWh</th><th>MAE, GBP/MWh</th></tr></thead><tbody>'
          '<tr><th>headline</th><td>18 Aug to 3 Sep 2026</td><td>816</td><td>−151.80</td><td>151.80</td></tr>'
          '<tr><th>13 monthly runs</th><td>5 May 2025 to 4 May 2026</td><td>17,520</td><td>−69.81</td><td>72.84</td>'
          '</tr></tbody></table></div>')
    fig = ('<p class="dnote">Both are perfect-prognosis backtests: realised demand, wind and solar stand in for the '
           'forecasts, and fuel and carbon prices are synthetic. APXMIDP mixes day-ahead and intraday trades, so it is '
           'not one auction. The −500 GBP/MWh floor weighs on the bias: in an earlier version, about 46% of it '
           'came from the 12% of periods where clearing hit the floor.</p>')
    checks = block("ck-h", "How it is checked", "The gates a probabilistic model must pass, and the scores that exist; "
                   "wind, solar and the stack have none.",
                   f'<dl class="ck">{dl}</dl>{t1}{t2}{fig}')
    return band("gold", 56, reach + sub_contact(8) + checks, "det", "reach-h")


def deep_models() -> str:
    limits = [
        "gridflow-models does not produce orders.",
        "No forecasts or metrics exist for the wind and solar models.",
        "The stack has no accuracy metric of its own; it is scored through the fundamentals SMP model.",
        "The published SMP backtests use realised inputs and synthetic fuel and carbon prices.",
    ]
    sources = [
        ("What exists", "the manifest in <code>data/gridflow_models.duckdb</code>, gold <code>forecasts</code> and "
                        "<code>forecast_metrics</code>, and <code>docs/MODEL_CARDS/</code>"),
        ("Metrics and gates", "<code>gridflow_models/validation/metrics.py</code>"),
        ("Models and targets", "<code>configs/models/</code>"),
        ("Workbench calls", "<code>src/gridflow_models/research/handles/</code>"),
    ]
    return deep("models", limits, sources)


def sky_art() -> str:
    parts = []
    for x, r, hh, rot, sp in ((846, 30, 92, 20, "sp2"), (926, 34, 104, 70, "sp1"), (1012, 28, 86, 110, "sp3")):
        parts.append(turbine(x, land_top(x) + 1, r, hh, rot, sp))
    parts.append(a_gas_station(1076, 1.0))
    parts.append(a_solar(1196, .5))
    labels = [(926, 146, "onshore wind", ONP2), (1126, 166, "gas-fired power station", ONP2),
              (1287, 206, "solar farm", ONP2)]
    return sky_svg("".join(parts), labels, "Drawing of onshore wind turbines, a gas-fired power station and a solar "
                                           "farm on the horizon: the output and the price the models forecast.")


def build() -> str:
    ans = ("A separate library that reads gridflow’s DuckDB and Parquet. Five models: day-ahead demand, wind, "
           "solar, a GB merit-order stack, and a price model built from the other four.")
    body = sky("What the models forecast", ans) + plate() + register() + specimen() + reach_checks() + deep_models()
    css = (".reg.mdl dl div{grid-template-columns:96px minmax(0,1fr)}\n"
           ".dfw+.dnote{margin-bottom:0}\n.dnote+.dfw{margin-top:34px}\n")
    return page("Models", "models", sky_art(), body, height_for("E-models", 5200), css)


if __name__ == "__main__":
    write("E-models", build())
    _ = (G, DAY)
    print("ok")
