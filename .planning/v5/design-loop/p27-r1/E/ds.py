"""E-data-sources: the landing sheet. Plate: one day, cut at each vendor's publication grain."""
from __future__ import annotations

from sheet import (DAY, G, INK, INK2, ONP2, PACK, a_converter, a_gas_terminal, a_met_mast, a_substation, band, block,
                   cable, deep, esc, f, height_for, line_chart, page, sky, sky_svg, sub_contact, write)

# ---------------------------------------------------------------- the plate
PITCH, ROW0, W = 64, 34, 840
# (vendor, main grain, main label, sub grain, sub label, key description, key fact). Labels: (text, is_code)
ROWS = [
    ("Elexon BMRS", 48, [("settlement periods, 46 or 50 on clock-change days", 0)],
     288, [("fuelinst", 1), (", every 5 minutes", 0)],
     "GB system prices, generation, demand, BM units", "33 datasets, GB electricity, no key"),
    ("ENTSO-E", 96, [("day_ahead_prices", 1), (": 15-minute for DE-LU, BE, FR and NL", 0)],
     24, [("hourly for IE-SEM", 0)],
     "EU prices, load, generation, flows and outages", "[n] datasets, EU electricity, API key"),
    ("NESO Carbon Intensity", 48, [("half-hourly, national and regional", 0)], None, None,
     "GB carbon intensity, actual and forecast", "[n] datasets, GB carbon, no key"),
    ("NESO Data Portal", 48, [("half-hourly: ", 0), ("historic_generation_mix", 1), (", the embedded forecast", 0)],
     1, [("daily, per BM unit: ", 0), ("daily_wind_availability", 1)],
     "NESO open data: the GB mix since 2009", "3 datasets, GB electricity, no key"),
    ("Open-Meteo", 24, [("hourly, at 7 demand cities, 12 wind sites and 6 solar sites", 0)], None, None,
     "Weather for demand, wind and solar modelling", "6 datasets, weather, no key"),
    ("ENTSO-G", 1, [("the gas day", 0)], None, None,
     "EU gas flows, nominations, capacity, tariffs", "[n] datasets, EU gas, no key"),
    ("GIE AGSI+ and ALSI", 1, [("the gas day", 0)], None, None,
     "EU gas storage levels and LNG terminals", "[n] datasets, EU gas storage and LNG, API key"),
]


def scalebar(x: float, y: float, w: float, h: float, n: int) -> str:
    seg = w / n
    fills = "".join(f'<rect x="{f(x + k * seg)}" y="{f(y)}" width="{f(seg)}" height="{f(h)}"></rect>'
                    for k in range(1, n, 2))
    return (f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="{DAY}"></rect>'
            f'<g fill="{INK}">{fills}</g>'
            f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="none" stroke="{INK}" stroke-width="1">'
            f'</rect>')


def label(x: float, y: float, parts: list[tuple[str, int]]) -> str:
    spans = "".join(f'<tspan font-family="Red Hat Mono" font-style="normal" font-size="13">{esc(t)}</tspan>' if c
                    else f"<tspan>{esc(t)}</tspan>" for t, c in parts)
    return f'<text x="{f(x)}" y="{f(y)}">{spans}</text>'


def drawing() -> str:
    g, t = [], []
    # the bracket: one day
    g.append(f'<path d="M0.5 20 V12 H370 M470 12 H839.5 V20" stroke="{INK}" stroke-width="1.2" fill="none"></path>')
    t.append('<text x="420" y="16.5" text-anchor="middle">one day</text>')
    for i, (_, n, lab, n2, lab2, *_rest) in enumerate(ROWS):
        y = ROW0 + i * PITCH
        t.append(label(0, y + 12, lab))
        g.append(scalebar(0, y + 18, W, 14, n))
        if n2:
            t.append(label(0, y + 47, lab2))
            g.append(scalebar(0, y + 52, W, 6, n2))
    h = ROW0 + len(ROWS) * PITCH - 4
    aria = ("Seven bars, one per vendor, each one day long and divided at the grain the vendor publishes. Elexon: 48 "
            "settlement periods, with fuelinst every 5 minutes beneath. ENTSO-E: day-ahead prices in 15-minute periods "
            "for DE-LU, BE, FR and NL, hourly for IE-SEM beneath. NESO Carbon Intensity: half-hourly. NESO Data "
            "Portal: half-hourly, with daily wind availability beneath. Open-Meteo: hourly. ENTSO-G and GIE: one gas "
            "day each.")
    return (f'<svg width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" aria-label="{esc(aria)}">'
            + "".join(g) + f'<g font-family="Hanken Grotesk" font-style="italic" font-size="13.5" fill="{INK}">'
            + "".join(t) + "</g></svg>")


def mark(n: int, n2: int | None) -> str:
    m = {48: 6, 96: 10, 24: 4, 1: 1, 288: 16}
    body = scalebar(.5, 3, 29, 7, m[n]) + (scalebar(.5, 13, 29, 3.5, m[n2]) if n2 else "")
    return f'<svg class="mk" width="30" height="18" viewBox="0 0 30 18" aria-hidden="true">{body}</svg>'


def plate() -> str:
    items = "".join(
        f'<li style="height: {PITCH}px">{mark(n, n2)}<div><h3><a href="#">{name}</a></h3><p class="d">{d}</p>'
        f'<p class="f">{fact}</p></div></li>' for name, n, _, n2, _, d, fact in ROWS)
    cap = ("Each bar is one day, divided at the grain its vendor publishes; a thin bar beneath is a second grain. "
           "Elexon also publishes some datasets once a day, and some as forecasts 2 to 14 days ahead.")
    inner = (f'<h2 class="ph" id="p-h">One day, cut at each vendor’s grain</h2><div class="pgrid">'
             f'<ul class="ix" style="margin-top: {ROW0}px" aria-label="The seven vendors, keyed to the bars">{items}</ul>'
             f'<figure class="pfig">{drawing()}<figcaption>{cap}</figcaption></figure></div>')
    return band("topsoil", 11, inner, "plate", "p-h")


# ---------------------------------------------------------------- register (bronze)
V = [
    ("Elexon BMRS", "elexon", "33 datasets",
     "The Insights API. GB balancing-mechanism data: system prices, generation outturn, BM-unit data, and demand and wind forecasts.",
     [("Grain", "Settlement periods; <code>fuelinst</code> is 5-minute; some daily and 2 to 14-day-ahead sets."),
      ("Access", "No key. <code>https://data.elexon.co.uk/bmrs/api/v1</code>"),
      ("Start with", "<code>system_prices</code>, <code>fuelhh</code>, <code>indo</code>, <code>mid</code>, "
                     "<code>remit</code>")]),
    ("ENTSO-E", "entsoe", "[n] datasets",
     "The Transparency Platform. EU electricity: day-ahead prices, load, generation per type, cross-border flows, outages, capacity and balancing.",
     [("Grain", "XML time series. Zones GB, FR, NL, BE, DE-LU and IE-SEM."),
      ("Access", "Key <code>ENTSOE_API_KEY</code> as <code>securityToken</code>, <code>https://web-api.tp.entsoe.eu</code>"),
      ("Start with", "<code>day_ahead_prices</code>, <code>actual_generation</code>, <code>actual_load</code>, "
                     "<code>cross_border_flows</code>, <code>wind_solar_forecast</code>")]),
    ("NESO Carbon Intensity", "neso", "[n] datasets",
     "GB national and regional carbon intensity, actual and forecast, with statistics, fuel emission factors and the "
     "generation mix.",
     [("Grain", "Half-hourly. Five families: intensity, factors, stats, generation, regional."),
      ("Access", "No key. <code>https://api.carbonintensity.org.uk</code>"),
      ("Start with", "<code>carbon_intensity</code>, <code>regional_intensity</code>, <code>generation</code>, "
                     "<code>intensity_factors</code>, <code>intensity_fw48h</code>")]),
    ("NESO Data Portal", "neso_data_portal", "3 datasets",
     "NESO’s open-data catalogue, a file-download API. gridflow reads three of its packages.",
     [("Grain", "Half-hourly; <code>daily_wind_availability</code> is daily, per BM unit. Current file only."),
      ("Access", "No key. <code>https://api.neso.energy</code>"),
      ("Datasets", "<code>historic_generation_mix</code>, <code>embedded_wind_solar_forecast</code>, "
                   "<code>daily_wind_availability</code>")]),
    ("Open-Meteo", "open_meteo", "6 datasets",
     "Weather: the ERA5 archive and NWP forecasts, where GB demand, wind and solar are modelled.",
     [("Grain", "Hourly, at 7 demand cities, 12 wind sites and 6 solar sites."),
      ("Access", "No key. <code>archive-api.open-meteo.com/v1</code>, <code>api.open-meteo.com/v1</code>"),
      ("Datasets", "<code>historical_demand</code>, <code>historical_wind</code>, <code>historical_solar</code>, "
                   "<code>forecast_demand</code>, <code>forecast_wind</code>, <code>forecast_solar</code>")]),
    ("ENTSO-G", "entsog", "[n] datasets",
     "The Transparency Platform. EU gas: physical flows, nominations, allocations, capacities, gas quality and tariffs, by default at UK TSO interconnection points.",
     [("Grain", "Daily, by gas day; tariffs and CMP data are periodic."),
      ("Access", "No key. <code>https://transparency.entsog.eu/api/v1</code>"),
      ("Start with", "<code>physical_flows</code>, <code>nominations</code>, <code>firm_technical</code>, "
                     "<code>gcv</code>, <code>tariffs</code>")]),
    ("GIE AGSI+ and ALSI", "gie_agsi, gie_alsi", "[n] datasets",
     "EU underground gas storage levels and flows (AGSI+) and LNG terminal data (ALSI).",
     [("Grain", "Daily, by gas day. AGSI+ nine countries, ALSI eight, GB in both."),
      ("Access", "Key <code>GIE_API_KEY</code> in <code>x-key</code>, one for both. <code>agsi.gie.eu</code>, <code>alsi.gie.eu</code>"),
      ("Start with", "<code>storage</code>, <code>storage_reports</code>, <code>unavailability</code>, "
                     "<code>lng</code>")]),
]


def register() -> str:
    rows = []
    for name, keys, n, pub, dl in V:
        dls = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in dl)
        rows.append(f'<li><div><h3><a href="#">{name}</a></h3><p class="sk">{keys}</p><p class="n">{n}</p></div>'
                    f'<div><p class="pub">{pub}</p><dl>{dls}</dl></div></li>')
    return band("bronze", 23, block("reg-h", "Every vendor, in full",
                                    "Seven vendors behind eight source keys: GIE’s two APIs share one key.",
                                    f'<ul class="reg">{"".join(rows)}</ul>'), "det", "reg-h")


# ---------------------------------------------------------------- specimen (silver)
def specimen() -> str:
    s = PACK["series"]["data_sources_landing"]
    pts = s["points"]
    v = [p[1] for p in pts]
    idx = {p[0]: i for i, p in enumerate(pts)}
    xt = [(idx["2026-06-01"], "1 Jun"), (idx["2026-07-01"], "1 Jul"), (idx["2026-08-01"], "1 Aug"),
          (idx["2026-09-01"], "1 Sep")]
    aria = (f"Line chart of the GB system price, daily mean, 26 May to 22 September 2026, in GBP/MWh. It moves "
            f"between {min(v):.0f} and {max(v):.0f}.")
    svg = line_chart(840, 320, len(v), 0, 220, [(0, "0"), (50, "50"), (100, "100"), (150, "150"), (200, "200")], xt,
                     [{"v": v, "c": INK, "w": 1.6, "label": "daily mean"}], aria, ylab="GBP/MWh", mr=96)
    cap = ("<code>elexon/system_prices</code> silver, <code>system_sell_price</code>: the latest vintage for each "
           "settlement period, then the mean of the 48 periods in each settlement date. GBP/MWh, 26 May to 22 "
           "September 2026.")
    gloss = ("Elexon publishes one imbalance price per settlement period: the system sell and buy prices are equal on "
             "every latest-vintage row from September 2021 to September 2026.")
    return band("silver", 37, block("spec-h", "The GB system price, day by day", gloss,
                                    f'<figure class="fig">{svg}<figcaption>{cap}</figcaption></figure>'),
                "det", "spec-h")


# ---------------------------------------------------------------- reach + checks (gold)
def reach_checks() -> str:
    lc = [
        ("On this site", "Every dataset page sits under its vendor, by key.",
         "data-sources/elexon/system_prices.html\ndata-sources/entsoe/day_ahead_prices.html"),
        ("In a notebook", "The gridflow-models workbench has one client per source.",
         '<span class="k">from</span> gridflow_models <span class="k">import</span> setup_notebook\n'
         "data, models, common = setup_notebook()\n\n"
         "data.list_data_sources()\ndata.elexon.list_datasets()\ndata.elexon.system_prices(start, end)"),
        ("In DuckDB", "One view per silver dataset, named source then dataset. Datasets that keep every capture add a "
                      "<code>_latest</code> view.",
         '<span class="k">select</span> * <span class="k">from</span> silver_elexon_system_prices_latest\n'
         '<span class="k">select</span> * <span class="k">from</span> silver_entsoe_day_ahead_prices'),
    ]
    rows = "".join(f'<li><div><h3>{a}</h3><p>{b}</p></div><pre class="well">{c}</pre></li>' for a, b, c in lc)
    reach = block("reach-h", "Reach it from code", "Three ways to the same rows.", f'<ul class="lc">{rows}</ul>')
    ck = [
        ("On the way to silver", "Every row is validated against its Pydantic schema, times are normalised to UTC, and "
                                 "rows are deduplicated on the dataset key."),
        ("<code>gridflow quality</code>", "Five checks per dataset: <code>null_rate</code>, "
                                          "<code>time_series_gaps</code>, <code>range_check</code>, "
                                          "<code>row_count</code> and <code>duplicates</code>."),
        ("Dataset pages", "Rendered from the vault notes by <code>gridflow-build</code>. "
                          "<code>gridflow-build --check</code> checks the render is idempotent, on every pull request."),
    ]
    dl = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in ck)
    checks = block("ck-h", "How it is checked", "What a row passes before it reaches a page.", f'<dl class="ck">{dl}</dl>')
    return band("gold", 53, reach + sub_contact(5) + checks, "det", "reach-h")


def deep_ds() -> str:
    limits = [
        "No scheduler. Data lands when someone runs <code>gridflow ingest</code>; the <code>schedule</code> field in "
        "the source config is not read.",
        "No GB day-ahead prices from ENTSO-E: its GB rows are empty, so the GB benchmark is Elexon MID (APXMIDP).",
        "No solar in Elexon <code>fuelhh</code>. GB solar outturn is in the NESO Data Portal’s "
        "<code>historic_generation_mix</code>.",
        "No NESO Data Portal backfill, and three of its packages rather than the whole portal.",
    ]
    sources = [
        ("Vendors and source keys", "<code>src/gridflow/connectors/registry.py</code>, <code>config/sources.yaml</code>"),
        ("Datasets per vendor", "<code>connectors/&lt;source&gt;/endpoints.py</code>"),
        ("What each vendor publishes", "the vault’s <code>30-vendors/&lt;vendor&gt;</code> notes"),
        ("Grain and history", "local silver, read directly"),
    ]
    return deep("ds", limits, sources)


def sky_art() -> str:
    x_gt, x_cv, x_mm, x_ss = 846, 1034, 1262, 1300
    sub, _ = a_substation(x_ss, 1.0)
    assets = a_gas_terminal(x_gt, 1.0) + a_converter(x_cv, 1.0) + a_met_mast(x_mm, .88) + sub
    labels = [(x_gt + 83, 212, "gas terminal", ONP2), (x_cv + 91, 181, "converter station", ONP2),
              (x_mm - 34, 150, "met mast", ONP2), (x_ss + 58, 212, "substation", ONP2)]
    _ = cable
    return sky_svg(assets, labels, "Drawing of the grid on the horizon: a gas terminal, an interconnector converter "
                                   "station, a met mast and a substation, standing on the land.")


def build() -> str:
    title = "Where the data comes from"
    ans = ("gridflow ingests [N datasets] from seven vendors, covering GB and EU electricity, EU gas and storage, GB "
           "carbon intensity and weather. The catalogue is filed by vendor, then by dataset.")
    body = sky(title, ans) + plate() + register() + specimen() + reach_checks() + deep_ds()
    h = height_for("E-data-sources", 4600)
    return page("Data sources", "ds", sky_art(), body, h)


if __name__ == "__main__":
    write("E-data-sources", build())
    _ = (G, INK2)
    print("ok")
