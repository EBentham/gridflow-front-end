"""Phase 27 round 1, designer C, "The field guide". Emits C-<page>.dc.html + static/C-<page>.html for the four top pages.

Type and table lists carry the identity. The drawing is held to three places: a shallow horizon strip under the sky, one
small plate per page, and the strata as the page footing (where they carry the site's three sections). Text flows in CSS
grid; only the SVGs are drawn. Root heights are measured in a browser and written to heights.json (root == $preview).
Every fact comes from ../pack/TOPPAGES.md or ../pack/toppages.json.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

import draw_c as D

HERE = Path(__file__).parent
PACK = D.PACK
W = 1440
HEIGHTS = {"data-sources": 6000, "vendor-elexon": 6000, "architecture": 6000, "models": 6000}
if (HERE / "heights.json").exists():
    HEIGHTS.update(json.loads((HERE / "heights.json").read_text(encoding="utf-8")))

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,200..800'
         '&amp;family=Hanken+Grotesk:ital,wght@0,400..700;1,400..600&amp;family=Red+Hat+Mono:wght@400;500'
         '&amp;display=swap" rel="stylesheet">')
CSS = (HERE / "c.css").read_text(encoding="utf-8")


def esc(s: str) -> str:
    return html.escape(s, quote=False)


# ================================================================ shared chrome
NAV = ["Home", "Data sources", "Architecture", "Models", "About"]


def mast(current: str) -> str:
    li = "".join(f'<li><a href="#"{" aria-current=" + chr(34) + "page" + chr(34) if t == current else ""}>{t}</a></li>'
                 for t in NAV)
    return f'<header class="mast"><a class="brand" href="#">gridflow</a><nav aria-label="Primary"><ul>{li}</ul></nav></header>'


LENS = ('<svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><circle cx="7.5" cy="7.5" r="5.6" fill="none" '
        'stroke="#1C2B22" stroke-width="1.6"></circle><path d="M11.6 11.6 L16.5 16.5" stroke="#1C2B22" stroke-width="1.8" '
        'stroke-linecap="round"></path></svg>')


def find(label: str, placeholder: str, fid: str) -> str:
    return (f'<div class="find"><label for="{fid}">{label}</label><div class="find-well">{LENS}'
            f'<input id="{fid}" type="search" placeholder="{placeholder}"></div></div>')


def toc(items: list[tuple[str, str]]) -> str:
    li = "".join(f'<li><a href="#{a}">{t}</a></li>' for a, t in items)
    return f'<nav class="toc" aria-label="On this page"><p>On this page</p><ol>{li}</ol></nav>'


def sky(current: str, h1: str, lede: str, right_extra: str = "", crumbs: str = "", marks: str = "") -> str:
    cr = f'<nav class="crumbs" aria-label="Breadcrumb">{crumbs}</nav>' if crumbs else ""
    return (f'<div class="sky">{mast(current)}<div class="head"><div>{cr}<h1>{h1}</h1>{marks}</div>'
            f'<div><p class="lede">{lede}</p>{right_extra}</div></div>{D.horizon()}</div>')


def sky_toc(current: str, h1: str, lede: str, items: list[tuple[str, str]], right_extra: str = "") -> str:
    li = "".join(f'<li><a href="#{a}">{t}</a></li>' for a, t in items)
    nav = f'<nav class="toc-l" aria-label="On this page"><ol>{li}</ol></nav>'
    return (f'<div class="sky">{mast(current)}<div class="head"><div><h1>{h1}</h1>{nav}</div>'
            f'<div><p class="lede">{lede}</p>{right_extra}</div></div>{D.horizon()}</div>')


FOOTING = [
    ("bronze", 0.4, "Data sources", "Every vendor gridflow ingests and every dataset it takes, found by vendor or by what "
                                    "it measures."),
    ("silver", 2.1, "Architecture", "Bronze, silver and gold on disk, the DuckDB catalogue, the commands, the build and "
                                    "its checks."),
    ("gold", 4.0, "Models", "Five models that read the warehouse: demand, wind, solar, the merit-order stack and a "
                            "fundamentals price."),
]


def footing(current: str) -> str:
    bands = []
    for kind, seed, title, line in FOOTING:
        t = (f'<span class="t" aria-current="page">{title}</span>' if title == current
             else f'<a class="t" href="#">{title}</a>')
        bands.append(f'<div class="band">{D.band_bg(kind, seed)}<div class="band-in">{t}<p>{line}</p>'
                     f'<span class="layer" aria-hidden="true">{kind}</span></div></div>')
    deep = (f'<footer class="deep">{D.band_bg("deep", 1.0)}<div class="deep-in"><a class="brand" href="#">gridflow</a>'
            f'<ul><li><a href="#">Home</a></li><li><a href="#">About</a></li><li><a href="#">Code on GitHub</a></li>'
            f'</ul></div></footer>')
    return f'<nav class="footing" aria-label="Sections of the site">{"".join(bands)}</nav>{deep}'


def part(pid: str, h2: str, aside: str, body: str, first: bool = False) -> str:
    a = f"<p>{aside}</p>" if aside else ""
    return (f'<section class="part{" first" if first else ""}" id="{pid}" aria-labelledby="{pid}-h">'
            f'<div class="part-head"><h2 id="{pid}-h">{h2}</h2>{a}</div>{body}</section>')


def facts(pairs: list[tuple[str, str]], cls: str = "") -> str:
    out = []
    for k, v in pairs:
        wide = k.startswith("!")
        out.append(f'<div{" class=" + chr(34) + "wide" + chr(34) if wide else ""}><dt>{k.lstrip("!")}</dt><dd>{v}</dd></div>')
    return f'<dl class="facts{(" " + cls) if cls else ""}">{"".join(out)}</dl>'


def plate(title: str, svg: str, caption: str) -> str:
    return f'<figure class="plate"><p class="pt">{title}</p>{svg}<figcaption>{caption}</figcaption></figure>'


# ================================================================ page 1: data sources
VENDORS = [
    # mark, name, keys, count, publishes, four facts, where to reach it
    ("pylon", "Elexon BMRS", ["elexon"], "33 datasets",
     "Great Britain’s balancing-mechanism data: system prices, generation outturn, BM-unit data, and demand and wind "
     "forecasts.",
     [("Market", "GB electricity"), ("Access", "Public, no key"),
      ("Grain", "Half-hourly settlement periods; FUELINST is 5-minute"),
      ("History held", "From September 2021 for six datasets, August 2026 for the rest")],
     "<code>data.elexon.co.uk/bmrs/api/v1</code>, through <code>connectors/elexon/client.py</code>"),
    ("converter", "ENTSO-E Transparency Platform", ["entsoe"], "[n] datasets",
     "European electricity: day-ahead prices, load, generation by type, cross-border flows, outages, capacity, "
     "transmission allocation and balancing. Its GB day-ahead rows are empty; the GB benchmark comes from Elexon MID.",
     [("Market", "EU electricity: GB, FR, NL, BE, DE-LU and IE-SEM"),
      ("Access", "Key <code>ENTSOE_API_KEY</code>, as <code>securityToken</code>"),
      ("Grain", "15-minute or hourly by zone, as XML"),
      ("History held", "From August 2026; the vendor keeps about five years")],
     "<code>web-api.tp.entsoe.eu</code>, through <code>connectors/entsoe/client.py</code>"),
    ("substation", "NESO Data Portal", ["neso_data_portal"], "[n] datasets",
     "The system operator’s open-data catalogue, served as files through CKAN rather than as a query API. gridflow "
     "reads three of its packages.",
     [("Market", "GB electricity, from the system operator"), ("Access", "Public, no key"),
      ("Grain", "Half-hourly; wind availability daily, per BM unit"),
      ("History held", "Generation mix from January 2009; current file only, no backfill")],
     "<code>api.neso.energy</code>, through <code>connectors/neso_data_portal/client.py</code>"),
    ("ccgt", "NESO Carbon Intensity", ["neso"], "[n] datasets, in five families",
     "GB carbon intensity, national and regional, actual and forecast, with statistics, fuel emission factors and the "
     "generation mix.",
     [("Market", "GB electricity carbon intensity"), ("Access", "Public, no key"), ("Grain", "Half-hourly"),
      ("History held", "Short windows, the longest 30 July to 21 September 2026")],
     "<code>api.carbonintensity.org.uk</code>, through <code>connectors/neso/carbon_intensity.py</code>"),
    ("pipeline", "ENTSO-G Transparency Platform", ["entsog"], "[n] datasets",
     "European gas: physical flows, nominations, allocations, capacities, gas quality, congestion outcomes, "
     "interruptions, tariffs, urgent market messages and the reference inventory.",
     [("Market", "EU gas; the UK’s interconnection points by default"), ("Access", "Public, no key"),
      ("Grain", "Daily, by gas day; tariffs and congestion data periodic"),
      ("History held", "From August 2026; tariffs from October 2025")],
     "<code>transparency.entsog.eu/api/v1</code>, through <code>connectors/entsog/client.py</code>"),
    ("tanks", "GIE AGSI+ and ALSI", ["gie_agsi", "gie_alsi"], "[n] datasets",
     "Underground gas storage across Europe, levels and flows (AGSI+), and LNG terminal data (ALSI).",
     [("Market", "Storage in 9 countries, LNG in 8; GB in both"),
      ("Access", "Key <code>GIE_API_KEY</code> in the <code>x-key</code> header, for both"),
      ("Grain", "Daily, by gas day"), ("History held", "From August 2026")],
     "<code>agsi.gie.eu</code> and <code>alsi.gie.eu</code>, through <code>connectors/gie/client.py</code>"),
    ("metmast", "Open-Meteo", ["open_meteo"], "[n] datasets",
     "Weather for GB power modelling: the ERA5 archive and forecasts, at 7 demand cities, 12 wind sites and 6 solar "
     "sites.",
     [("Market", "Weather inputs for GB power"), ("Access", "Public, free tier"), ("Grain", "Hourly"),
      ("History held", "Archive from September 2021; forecasts from August 2026")],
     "<code>archive-api.open-meteo.com/v1</code> and <code>api.open-meteo.com/v1</code>, through "
     "<code>connectors/openmeteo/client.py</code>"),
]

# measure key: group, scope line, rows of (sub-label or "", key, what it holds, vendor)
KEY = [
    ("Power", "GB and European electricity: prices, generation, demand, flows, forecasts and outages.", [
        ("prices", "system_prices", "Imbalance price per settlement period; sell and buy are equal", "Elexon"),
        ("", "mid", "Market index; its APXMIDP provider is the GB day-ahead benchmark", "Elexon"),
        ("", "day_ahead_prices", "Day-ahead prices by bidding zone, EUR/MWh; no GB rows", "ENTSO-E"),
        ("generation", "fuelhh", "Half-hourly generation by fuel type; no solar", "Elexon"),
        ("", "historic_generation_mix", "GB generation mix by fuel since 2009, solar included", "NESO Data Portal"),
        ("", "actual_generation", "Actual generation per production type", "ENTSO-E"),
        ("demand", "indo", "Initial national demand outturn, half-hourly", "Elexon"),
        ("", "actual_load", "Actual total load", "ENTSO-E"),
        ("flows", "cross_border_flows", "Physical flows across borders", "ENTSO-E"),
        ("forecasts", "windfor", "Wind generation forecast", "Elexon"),
        ("", "wind_solar_forecast", "Day-ahead wind and solar forecast", "ENTSO-E"),
        ("", "embedded_wind_solar_forecast", "Embedded wind and solar, per settlement period", "NESO Data Portal"),
        ("outages", "remit", "REMIT outage and unavailability messages", "Elexon"),
    ]),
    ("Gas", "European transmission, storage and LNG, by gas day.", [
        ("flows", "physical_flows", "Physical flow at interconnection points", "ENTSO-G"),
        ("", "nominations", "Nominations at interconnection points", "ENTSO-G"),
        ("capacity", "firm_technical", "Firm technical capacity", "ENTSO-G"),
        ("quality", "gcv", "Gross calorific value", "ENTSO-G"),
        ("tariffs", "tariffs", "Tariff types and components, UK", "ENTSO-G"),
        ("storage", "storage", "Storage levels by country and gas day", "GIE AGSI+"),
        ("", "unavailability", "Storage unavailability reports", "GIE AGSI+"),
        ("LNG", "lng", "LNG terminal data", "GIE ALSI"),
    ]),
    ("Weather", "Hourly, at the locations each model needs.", [
        ("archive", "historical_demand", "ERA5 archive at 7 demand cities", "Open-Meteo"),
        ("", "historical_wind", "ERA5 archive at 12 wind sites, 10 m and 100 m wind", "Open-Meteo"),
        ("", "historical_solar", "ERA5 archive at 6 solar sites: GHI, DNI, DHI and GTI", "Open-Meteo"),
        ("forecast", "forecast_demand", "Forecast weather at the 7 demand cities", "Open-Meteo"),
        ("", "forecast_wind", "Forecast weather at the 12 wind sites", "Open-Meteo"),
        ("", "forecast_solar", "Forecast weather at the 6 solar sites", "Open-Meteo"),
    ]),
    ("Carbon", "GB carbon intensity, half-hourly.", [
        ("national", "carbon_intensity", "National carbon intensity over a date range", "NESO"),
        ("", "intensity_fw48h", "National intensity forecast, 48 hours forward", "NESO"),
        ("regional", "regional_intensity", "Intensity for every region", "NESO"),
        ("mix", "generation", "National generation mix", "NESO"),
        ("factors", "intensity_factors", "Emission factor for each fuel", "NESO"),
    ]),
]


def vendor_entry(v: tuple) -> str:
    kind, name, keys, count, pub, fx, reach = v
    ids = " ".join(f"<code>{k}</code>" for k in keys)
    cnt = count.replace("[n]", '<span class="slot">[n]</span>')
    return (f'<li class="ent v-ent" id="v-{keys[0]}"><div>{D.mark(kind)}<h3><a href="#">{name}</a></h3><p class="id">{ids}</p>'
            f'<p class="n"><a href="#">{cnt}</a></p></div>'
            f'<div><p class="acc">{pub}</p>{facts(fx, "four")}<p class="reach">Reached at {reach}.</p></div></li>')


def key_group(g: tuple) -> str:
    name, scope, rows = g
    li = "".join(f'<li><span class="s">{s}</span><span class="k"><a href="#">{k}</a></span><span class="d">{d}</span>'
                 f'<span class="v">{v}</span></li>' for s, k, d, v in rows)
    return (f'<div class="grp"><div class="g-head"><h3>{name}</h3><p>{scope}</p></div>'
            f'<ul class="tl" aria-label="{name} datasets">{li}</ul></div>')


def page_data_sources() -> tuple[str, str, str]:
    lede = ('gridflow ingests <span class="slot">[N datasets]</span> from seven vendors: GB and European power, gas, '
            'weather and carbon. Each vendor’s page lists all it supplies, and each dataset has a page of its own.')
    head = sky_toc("Data sources", "Data sources", lede,
                   [(f"v-{v[2][0]}", v[1].replace(" Transparency Platform", "")) for v in VENDORS]
                   + [("measure", "By what it measures")],
                   find("Find a dataset", "A key, a code or a word: fuelhh, INDO, storage", "q-all"))
    vendors = part("vendors", "The seven vendors",
                   "Grain is the vendor’s own publication grain. gridflow has no scheduler: data lands when "
                   "<code>gridflow ingest</code> runs.",
                   f'<ul class="ents" aria-label="Vendors">{"".join(vendor_entry(v) for v in VENDORS)}</ul>', first=True)
    key = part("measure", "By what it measures",
               "A selection from every vendor, sorted into power, gas, weather and carbon. Each vendor’s page lists all "
               "of its datasets.",
               f'<div class="key4">{"".join(key_group(g) for g in KEY)}</div>')
    org_dl = facts([
        ("!Vendor, then dataset", "Every dataset has a source key and a dataset key, such as <code>elexon</code> and "
                                  "<code>fuelhh</code>. Most Elexon keys are the BMRS code in lower case."),
        ("!A page for each dataset", "What it is, its facts and caveats, the vendor endpoint, the silver schema, sample "
                                     "rows and the call that reads it, with a chart of its own data where the data "
                                     "allows."),
        ("!A view for each dataset", "In DuckDB every dataset is a view named <code>silver_{source}_{dataset}</code>. "
                                     "Datasets that keep every vintage also get a <code>_latest</code> view."),
    ], "two")
    sp = plate("From the <code>system_prices</code> page: GB system price, daily mean", D.plate_system_price(),
               "Source <code>elexon/system_prices</code>, silver, the latest vintage of each settlement period; the mean "
               "of the 48 periods in each settlement day, £/MWh, 26 May to 22 September 2026. The sell and buy prices "
               "are equal on every row, so one line carries both.")
    org = part("organised", "How the catalogue is organised", "",
               f'<div class="org"><div>{org_dl}</div>{sp}</div>')
    body = "<main>" + vendors + key + org + "</main>"
    return "Data sources", head, body


# ================================================================ page 2: the Elexon hub
def hub_rows() -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = {}
    for x in PACK["data_sources"]["elexon_hub"]["datasets"]:
        groups.setdefault(x["proposed_theme"], []).append(x)
    return groups


ONE_LINE = {  # the code's ElexonEndpoint.description, as the pack table gives it; en dashes set as "to"
    "system_prices": "System sell price and system buy price per settlement period",
    "market_depth": "Settlement market depth per settlement period",
    "pn": "Physical notifications, per BM unit and period",
    "boal": "Bid/offer acceptance levels (BOALF; replaces the deprecated BOAL)",
    "disbsad": "Disaggregated balancing services adjustment data",
    "mid": "Market index data; APXMIDP is the GB day-ahead benchmark",
    "netbsad": "Net balancing services adjustment data",
    "soso": "SO-SO prices: cross-border interconnector trading",
    "freq": "System frequency",
    "fuelhh": "Half-hourly generation outturn by fuel type (no solar)",
    "fuelinst": "Instantaneous generation outturn by fuel type",
    "imbalngc": "Indicated imbalance",
    "ndf": "National demand forecast, day-ahead",
    "ndfd": "National demand forecast, 2 to 14 days ahead",
    "melngc": "Indicated margin",
    "fou2t14d": "Generation availability by fuel type, 2 to 14 days ahead",
    "uou2t14d": "Generation availability by BM unit, 2 to 14 days ahead",
    "windfor": "Wind generation forecast",
    "temp": "Temperature data",
    "agpt": "Actual aggregated generation per type (B1620)",
    "agws": "Actual or estimated wind and solar generation (B1630)",
    "atl": "Actual total load per bidding zone (B0610)",
    "indo": "Initial national demand outturn",
    "itsdo": "Initial transmission system demand outturn",
    "indod": "Initial national demand outturn, daily total",
    "nonbm": "Non-BM STOR generation",
    "inddem": "Day and day-ahead indicated demand",
    "indgen": "Day and day-ahead indicated generation",
    "tsdf": "Transmission system demand forecast",
    "tsdfd": "Transmission system demand forecast, 2 to 14 days ahead",
    "lolpdrm": "Loss of load probability and de-rated margin",
    "remit": "REMIT outage and unavailability messages",
    "bmunits_reference": "All BM unit reference data",
}
THEME_ORDER = [
    ("Prices and balancing", "Imbalance prices and the market index, BM unit notifications and acceptances, and "
                             "balancing adjustments.",
     ["system_prices", "mid", "market_depth", "boal", "pn", "disbsad", "netbsad", "soso"]),
    ("Generation and availability", "Outturn by fuel and by type, the wind forecast, and availability 2 to 14 days "
                                    "ahead.",
     ["fuelhh", "fuelinst", "agpt", "agws", "windfor", "fou2t14d", "uou2t14d", "nonbm"]),
    ("Demand", "National and transmission demand: outturn and forecasts.",
     ["indo", "itsdo", "indod", "atl", "ndf", "ndfd", "tsdf", "tsdfd", "inddem"]),
    ("System indicators", "Frequency, temperature, margin, imbalance and the loss-of-load probability.",
     ["freq", "temp", "melngc", "imbalngc", "indgen", "lolpdrm"]),
    ("Reference and messages", "The BM unit register and REMIT messages.", ["bmunits_reference", "remit"]),
]


def held_from(x: dict) -> str:
    if x["key"] == "bmunits_reference":
        return "snapshot"
    t = x["event_time_min"][:7]
    return {"2021-08": "Sep 2021", "2021-09": "Sep 2021", "2026-07": "Aug 2026", "2026-08": "Aug 2026",
            "2026-04": "Apr 2026"}[t]


def page_elexon() -> tuple[str, str, str]:
    by_key = {x["key"]: x for x in PACK["data_sources"]["elexon_hub"]["datasets"]}
    assert sorted(by_key) == sorted(k for _, _, ks in THEME_ORDER for k in ks) == sorted(ONE_LINE), "33 rows, once each"
    crumbs = '<a href="#">Data sources</a><span aria-hidden="true">/</span>Elexon BMRS'
    marks = ('<dl class="marks"><div><dt>Source key</dt><dd><code>elexon</code></dd></div>'
             '<div><dt>Access</dt><dd>Public, no key</dd></div>'
             '<div><dt>Grain</dt><dd>Half-hourly settlement periods</dd></div></dl>')
    lede = ("Great Britain’s balancing-mechanism data, from Elexon’s Insights API: system prices, generation outturn, "
            "BM-unit data, and demand and wind forecasts. gridflow takes 33 datasets from it.")
    head = sky("Data sources", "Elexon BMRS", lede,
               find("Find an Elexon dataset", "A key or a BMRS code: fuelhh, INDO, BOALF", "q-elexon"), crumbs, marks)
    groups = []
    for name, scope, keys in THEME_ORDER:
        li = "".join(
            f'<li><span class="k"><a href="#">{k}</a></span><span class="d">{ONE_LINE[k]}</span>'
            f'<span class="p">{by_key[k]["api_path"] + ("/{date}" if by_key[k]["param_style"] == "date_path" else "")}</span>'
            f'<span class="v r">{held_from(by_key[k])}</span></li>' for k in keys)
        groups.append(f'<div class="grp"><div class="g-head"><h3>{name}</h3><p>{scope}</p></div>'
                      f'<ul class="tl" aria-label="{name}">{li}</ul></div>')
    colhead = ""
    arrange = ('<div class="tl-h"><p class="arrange">Arranged by <a href="#" aria-current="true">what it '
               'measures</a><a href="#">request style</a></p><span aria-hidden="true">Endpoint</span>'
               '<span class="r" aria-hidden="true">Held from</span></div>')
    lst = part("datasets", "Every Elexon dataset gridflow takes",
               "Each row is one dataset: its key, what it holds, the endpoint gridflow calls, and how far back the "
               "local store reaches.",
               f'<div class="hub">{arrange}{colhead}{"".join(groups)}</div>', first=True)
    fx = facts([("Base URL", "<code>https://data.elexon.co.uk/bmrs/api/v1</code>"),
                ("Connector", "<code>connectors/elexon/client.py</code>; endpoints in <code>endpoints.py</code>"),
                ("Rate limit", "2 requests a second, retried, as set in <code>config/sources.yaml</code>"),
                ("History held", "From September 2021 for <code>system_prices</code>, <code>mid</code>, "
                                 "<code>fuelhh</code>, <code>indo</code>, <code>windfor</code> and <code>agws</code>; "
                                 "from August 2026 for the rest")], "two")
    wp = plate("GB wind generation, monthly mean, September 2021 to August 2026", D.plate_wind(),
               "Source <code>elexon/fuelhh</code>, fuel type WIND, <code>generation_mw</code>: the mean half-hourly output "
               "of each calendar month, MW. Transmission-metered output only.")
    cav = ('<dl class="cav">'
           '<div><dt>FUELHH has no solar</dt><dd>No solar fuel type, from 2021 on. GB solar outturn is in the NESO Data '
           'Portal’s <code>historic_generation_mix</code>.</dd></div>'
           '<div><dt>One imbalance price</dt><dd>The system sell and buy prices are equal on every latest-vintage row '
           'since September 2021.</dd></div>'
           '<div><dt>The GB day-ahead benchmark</dt><dd>MID’s APXMIDP provider. ENTSO-E has no GB day-ahead rows, so '
           'gridflow and the price model both use MID.</dd></div>'
           '<div><dt>Some datasets keep every vintage</dt><dd><code>system_prices</code>, <code>remit</code> and '
           '<code>fou2t14d</code> keep each capture; read their <code>_latest</code> views.</dd></div></dl>')
    about = part("feed", "About the feed", "",
                 f'<div class="lay"><div>{fx}<h3 class="sub-h" id="cav-h">Read before using</h3>{cav}</div>{wp}</div>')
    body = "<main>" + lst + about + "</main>"
    return "Elexon BMRS", head, body


# ================================================================ page 3: architecture
CLI = [("init", "Create the catalogue and register its views"),
       ("ingest", "API to bronze"),
       ("transform", "Bronze to silver, validated and deduplicated"),
       ("build", "Silver to gold"),
       ("pipeline", "Ingest, then transform; build too with <code>--gold</code>"),
       ("backfill", "Fetch history in chunks"),
       ("export-csv", "Silver Parquet to CSV"),
       ("status", "Run history and a quality summary"),
       ("quality", "Run the quality checks and write a report"),
       ("reset", "Delete every layer and reset the catalogue"),
       ("prune", "Delete partitions past a retention cutoff")]


def tl(rows: list[tuple[str, str]], label: str, cols: str = "184px minmax(0,1fr)") -> str:
    li = "".join(f'<li style="grid-template-columns: {cols}"><span class="k">{k}</span><span class="d">{d}</span></li>'
                 for k, d in rows)
    return f'<ul class="tl" aria-label="{label}">{li}</ul>'


def layer(pid: str, kind: str, name: str, sub: str, verb: str, prose: str, extra: str) -> str:
    return (f'<section class="part" id="{pid}" aria-labelledby="{pid}-h"><div class="split"><div class="m-head">'
            f'<div class="sw">{D.swatch(kind)}</div><h2 id="{pid}-h" class="lh">{name}</h2><p>{sub}</p></div>'
            f'<div><p class="cmd">Written by <code>{verb}</code></p><div class="prose">{prose}</div>{extra}</div>'
            f'</div></section>')


def page_architecture() -> tuple[str, str, str]:
    lede = ("gridflow is a local-first Python pipeline. Every run is a command on one machine: raw responses land in "
            "bronze, typed tables in silver, and views in gold, all read through one DuckDB file. There is no server "
            "and no scheduler.")
    head = sky_toc("Architecture", "Architecture", lede,
                   [("brief", "In brief"), ("bronze", "Bronze"), ("silver", "Silver"), ("gold", "Gold"),
                    ("catalogue", "The catalogue"), ("commands", "Commands"), ("gates", "The build and the gates"),
                    ("not", "What it does not do")])
    brief = part("brief", "In brief", "",
                 '<div class="split"><div class="m-head"><p>The data root is set by <code>GRIDFLOW_DATA_DIR</code>; '
                 'every path below is relative to it and built by <code>PathBuilder</code> in '
                 '<code>storage/paths.py</code>.</p></div><div>'
                 + facts([("Language", "Python 3.11 or later"),
                          ("Libraries", "Polars, DuckDB, Pydantic v2, httpx and Typer"),
                          ("Command", "<code>gridflow</code>, from <code>gridflow.cli:app</code>"),
                          ("Catalogue", "<code>{data_root}/gridflow.duckdb</code>, or <code>GRIDFLOW_DUCKDB_PATH</code>"),
                          ("Sources", "8 source keys for 7 vendors, in <code>connectors/registry.py</code>"),
                          ("Licence", "Apache-2.0")])
                 + '<div class="disk">'
                 + plate("What lands on disk", D.plate_disk(),
                         "A bronze body with its sidecar; a silver Parquet file, one of a set partitioned by year and "
                         "month; and <code>gridflow.duckdb</code>, whose views read the Parquet files where they lie.")
                 + '</div></div></div>', first=True)
    sidecar = ["source", "dataset", "fetched_at", "written_at", "data_date", "request_url", "request_params",
               "api_version", "http_status", "content_type", "body_sha256", "body_size_bytes", "page", "total_pages"]
    bronze = layer(
        "bronze", "bronze", "Bronze", "The response as it arrived: written once, never rewritten.", "gridflow ingest",
        "<p>Each source has an async connector, <code>connectors/&lt;source&gt;/client.py</code>, with the rate limits "
        "and retries set in <code>config/sources.yaml</code>: Elexon at 2 requests a second, ENTSO-E at 1. "
        "<code>BronzeWriter.write</code> stores the body, then a sidecar, each through a temporary file and "
        "<code>os.replace</code>. The body keeps its content type: <code>.json</code>, <code>.xml</code>, "
        "<code>.csv</code> or <code>.bin</code>. The partition is the data date when it is known, else the fetch date.</p>",
        '<pre class="well">bronze/{source}/{dataset}/{YYYY}/{MM}/{DD}/\n'
        '  raw_{fetched_at:%Y%m%dT%H%M%SZ}_{sha256[:8]}.{ext}\n'
        '  raw_{fetched_at:%Y%m%dT%H%M%SZ}_{sha256[:8]}.meta.json</pre>'
        '<p class="note">The sidecar’s fields, with credentials masked in the request URL and parameters:</p>'
        '<p class="fields">' + ", ".join(f"<code>{x}</code>" for x in sidecar) + '.</p>'
        '<p class="ref">In the code: <code>bronze/writer.py:38-48</code> (partitions), <code>:57</code> (the body), '
        '<code>:67-85</code> (the sidecar), and <code>storage/paths.py:23-38</code>.</p>')
    silver = layer(
        "silver", "silver", "Silver", "Typed, validated, deduplicated tables, in UTC.", "gridflow transform",
        "<p>One <code>BaseSilverTransformer</code> for each source and dataset, 164 of them in "
        "<code>silver/registry.py</code>. Its <code>run()</code> reads one date’s bronze, parses it, validates every row "
        "against the Pydantic schema in <code>schemas/</code>, normalises time to UTC, deduplicates on the dataset’s key "
        "and writes Parquet, zstd-compressed, atomically.</p>"
        "<p>Six datasets keep every capture instead: <code>system_prices</code>, <code>remit</code> and "
        "<code>fou2t14d</code> from Elexon, and the three from the NESO Data Portal. Their files carry the vintage in the "
        "name, and <code>LATEST_VIEW_SPECS</code> in <code>silver/latest_views.py</code> sets the business key and "
        "precedence that picks the latest.</p>",
        '<pre class="well">silver/{source}/{dataset}/year={YYYY}/month={MM}/{dataset}_{YYYYMMDD}.parquet\n'
        '<span class="c">keeps every capture:</span>  {dataset}_{YYYYMMDD}_run{available_at}.parquet</pre>'
        + tl([("event_time", "The time the value is for; on every silver table"),
              ("available_at", "When the value could first be known: the basis for as-of reads"),
              ("published_at", "When the vendor published it"),
              ("ingested_at", "When gridflow fetched it"),
              ("source_run_id", "The run that wrote the row"),
              ("dataset_version", "The transformer’s schema version")], "Silver columns")
        + '<p class="ref">In the code: <code>silver/base.py:936</code> (the run), <code>:2046</code> (validation), '
          '<code>:1337</code> (deduplication) and <code>:2635</code> (the vintage suffix).</p>')
    gold = layer(
        "gold", "gold", "Gold", "Joined and derived tables, read as DuckDB views.", "gridflow build",
        "<p>gridflow registers one gold builder, <code>system_marginal_price</code>, in <code>gold/registry.py</code>: "
        "latest-vintage system prices with the spread, the absolute imbalance and calendar features. Three SQL views in "
        "<code>gold/views/</code> register with the catalogue.</p>"
        "<p>gridflow-models writes its outputs into the same root, partitioned by model rather than by year: "
        "<code>forecasts</code>, <code>forecast_metrics</code>, <code>stack_clearing</code>, "
        "<code>stack_residual_demand</code> and <code>stack_supply_curve_points</code>.</p>",
        '<pre class="well">gold/{name}/year={YYYY}/{name}_{YYYYMMDD}.parquet\n'
        '<span class="c">from gridflow-models:</span>  gold/{table}/model_slug={slug}/{prefix}_{YYYYMMDDTHHMMSSZ}_{run_id}.parquet</pre>'
        + tl([("gold_uk_imbalance_context", "Elexon system prices with NESO carbon intensity, half-hourly"),
              ("gold_gb_day_ahead_benchmark", "Elexon MID APXMIDP, one row per settlement period, GBP/MWh"),
              ("gold_eu_gas_storage", "GIE AGSI+ storage by country and day")], "Gold SQL views", "252px minmax(0,1fr)"))
    cat = part("catalogue", "The catalogue",
               "One DuckDB file, <code>{data_root}/gridflow.duckdb</code>. <code>gridflow init</code> registers a view "
               "for every directory it finds, so a new dataset is queryable as soon as it has silver.",
               '<div class="split"><div class="m-head"><h3>Tables</h3><p><code>pipeline_runs</code>, '
               '<code>pipeline_watermarks</code> and <code>quality_reports</code>.</p><p class="ref">'
               '<code>storage/duckdb.py:106-209, 465</code></p></div><div>'
               + tl([("silver_{source}_{dataset}", "One for each silver dataset"),
                     ("silver_{source}_{dataset}_latest", "The latest vintage, for the six datasets that keep every capture"),
                     ("gold_{name}", "One for each gold directory, and the three SQL views"),
                     ("silver_{dataset}", "An older short alias, skipped when two sources share a dataset name")],
                    "View names", "328px minmax(0,1fr)")
               + '<p class="note">Read it from DuckDB, or from Python with the read-only '
                 '<code>gridflow.serving.client.GridflowClient</code>.</p></div></div>')
    cmds = part("commands", "Commands",
                "Each is a Typer command, run as <code>gridflow &lt;verb&gt;</code>. Nothing runs on a timer.",
                '<div class="split"><div class="m-head"><h3>Quality checks</h3><p><code>null_rate</code>, '
                '<code>time_series_gaps</code>, <code>range_check</code>, <code>row_count</code> and '
                '<code>duplicates</code>, run by <code>gridflow quality</code>.</p><p class="ref">'
                '<code>quality/checks.py</code></p></div><div>'
                + '<div class="two-tl">' + tl([(k, d) for k, d in CLI[:6]], "Commands, first half", "112px minmax(0,1fr)")
                + tl([(k, d) for k, d in CLI[6:]], "Commands, second half", "112px minmax(0,1fr)") + '</div>'
                + '</div></div>')
    gates = part("gates", "The build and the gates",
                 "Two repositories, each with its own checks in GitHub Actions.",
                 '<div class="split"><div class="m-head"><h3>gridflow</h3><p>The pipeline’s own CI, on every push and '
                 'pull request.</p></div><div>'
                 + tl([("uv lock --check", "The lockfile matches the project"),
                       ("ruff check", "Lint"), ("ruff format --check", "Formatting"), ("mypy", "Types"),
                       ("pytest -m \"not live\"", "The test suite, without calls to vendor APIs")], "gridflow CI",
                      "220px minmax(0,1fr)")
                 + '</div></div><div class="split grp"><div class="m-head"><h3>This site</h3><p><code>gridflow-build</code> '
                   'renders each vault note into a dataset page with Jinja2.</p></div><div>'
                 + tl([("ci.yml", "On pull requests and pushes to main: the staleness check, a baseline ratchet "
                                  "and the build check"),
                       ("deploy.yml", "On pushes to main: build, <code>--check</code>, htmlhint, lychee link checks, then "
                                      "GitHub Pages"),
                       ("gridflow-build --check", "A second build changes nothing: the build is idempotent"),
                       ("gridflow-drift-check", "Checks pages against the vendors’ live APIs, so it runs only by hand")],
                      "Site gates", "220px minmax(0,1fr)")
                 + '</div></div>')
    notdo = part("not", "What it does not do", "",
                 '<div class="split"><div></div><dl class="cav">'
                 '<div><dt>No scheduler</dt><dd>Every run is a command. The <code>schedule</code> field in '
                 '<code>sources.yaml</code> is declared and read nowhere else.</dd></div>'
                 '<div><dt>No live feed</dt><dd>Data lands when someone runs <code>gridflow ingest</code>.</dd></div>'
                 '<div><dt>No server</dt><dd>No web service, public API or hosted database: local files and one '
                 'embedded DuckDB file.</dd></div>'
                 '<div><dt>No cloud</dt><dd>No object store, warehouse, streaming, cluster or multi-tenancy.</dd></div>'
                 '<div><dt>No models</dt><dd>Forecasts live in gridflow-models, a separate repository, which does not '
                 'produce orders.</dd></div>'
                 '<div><dt>Not every package</dt><dd>Three NESO Data Portal packages, current file only, and no GB '
                 'day-ahead prices from ENTSO-E.</dd></div></dl></div>')
    body = "<main>" + brief + bronze + silver + gold + cat + cmds + gates + notdo + "</main>"
    return "Architecture", head, body


# ================================================================ page 4: models
def hl(code: str) -> str:
    code = esc(code)
    code = re.sub(r"\b(from|import)\b", r'<span class="k">\1</span>', code)
    return code


def page_models() -> tuple[str, str, str]:
    lede = ("gridflow-models is a separate library that reads gridflow’s catalogue and Parquet. It holds five models: "
            "forecasters for demand, wind and solar, a merit-order supply stack, and a fundamentals model that prices "
            "each half-hour from the stack. It does not produce orders.")
    head = sky_toc("Models", "Models", lede,
                   [("scores", "Reading the scores"), ("demand", "Day-ahead demand"), ("wind", "Wind generation"),
                    ("solar", "Solar generation"), ("stack", "GB merit-order stack"), ("smp", "Fundamentals SMP"),
                    ("workbench", "In the workbench")])
    scores = part("scores", "Reading the scores",
                  "Scores appear only where a run has produced them. Every figure below is read from the gold "
                  "<code>forecast_metrics</code> and stack tables, or the model card that publishes it.",
                  '<div class="split"><div class="m-head"><h3>Definitions</h3><p>From '
                  '<code>validation/metrics.py</code> and the model cards.</p></div><div>'
                  + tl([("pinball q0.5", "The mean quantile loss at 0.5, in MW: half the mean absolute error of the "
                                         "median forecast"),
                        ("coverage_90", "The share of outturns inside the band from q0.05 to q0.95, bounds included"),
                        ("crossings", "Rows where a higher quantile falls below a lower one"),
                        ("gates", "Pinball q0.5 at most 1,500 MW; coverage within 0.90 ± 0.05; no crossings"),
                        ("mean bias", "The mean of the modelled price less APXMIDP, GBP/MWh")], "Score definitions",
                       "184px minmax(0,1fr)")
                  + '</div></div>', first=True)

    def model(mid: str, name: str, ids: list[str], handle: str, rows: list[tuple[str, str]], extra: str = "") -> str:
        idl = "".join(f'<code>{i}</code><br>' for i in ids)[:-4]
        return (f'<li class="ent" id="{mid}"><div><h3>{name}</h3><p class="id">{idl}</p>'
                f'<p class="n">In the workbench, {handle}</p></div>'
                f'<div>{facts(rows, "two")}{extra}</div></li>')

    dem = D.SERIES["models_landing_demand_folds"]["points"]
    folds = ('<table class="folds"><caption>Pinball q0.5 by fold, version 1, MW</caption><thead><tr><th scope="col">Fold</th>'
             + "".join(f'<th scope="col">{p[0]}</th>' for p in dem) + '</tr></thead><tbody><tr><th scope="row">Pinball</th>'
             + "".join(f"<td>{p[2]:.0f}</td>" for p in dem) + '</tr></tbody></table>')
    dem_scores = (
        '<table class="sc"><thead><tr><th>Version</th><th>Run</th><th class="num">Pinball q0.5</th>'
        '<th class="num">coverage_90</th><th class="num">Crossings</th><th>Read it as</th></tr></thead><tbody>'
        '<tr><td>1</td><td><code>a55a829bc51c40b2</code></td><td class="num">711.04 MW</td><td class="num">0.893</td>'
        '<td class="num">0</td><td>Issued forecasts, as they would have been made. Passes every gate.</td></tr>'
        '<tr><td>2</td><td><code>b367a742aa544f8f</code></td><td class="num">599.72 MW</td><td class="num">0.883</td>'
        '<td class="num">0</td><td>Perfect prognosis: actual ERA5 weather used as if forecast, so optimistic. The card '
        'calls its 15.7% gain an upper bound, from one run. Passes every gate.</td></tr></tbody></table>'
        '<p class="note">Both runs: 12 walk-forward folds of 30 days, 1 September 2024 to 22 August 2026, 17,279 scored '
        'half-hours; each fold fits on a rolling 1,095-day window.</p>')
    dem_plate = plate("Version 1 against outturn, 20 and 21 August 2026", D.plate_demand(),
                      "Source gold <code>forecasts</code>, run <code>a55a829bc51c40b2</code>, walk-forward fold 12, issued "
                      "vintage: the median and the band from q0.05 to q0.95 against the outturn, MW, 96 half-hours in UTC.")
    smp_scores = (
        '<table class="sc"><thead><tr><th>Backtest</th><th>Window</th><th class="num">Mean bias</th>'
        '<th class="num">MAE</th></tr></thead><tbody>'
        '<tr><td>Headline, run <code>41de423cfc0b421e</code></td><td>18 August to 3 September 2026, 816 periods</td>'
        '<td class="num">−151.80</td><td class="num">151.80</td></tr>'
        '<tr><td>Diagnostic, 13 monthly runs</td><td>5 May 2025 to 4 May 2026, 17,520 periods</td>'
        '<td class="num">−69.81</td><td class="num">72.84</td></tr></tbody></table>'
        '<p class="note">GBP/MWh, against APXMIDP. In the headline run every period is below the benchmark.</p>'
        '<dl class="cav smp-cav">'
        '<div><dt>Perfect prognosis</dt><dd>Realised demand, wind and solar go in, not forecasts.</dd></div>'
        '<div><dt>Synthetic fuel and carbon prices</dt><dd>Provenance <code>synthetic 35e4d8d</code>, seed 20240507.</dd></div>'
        '<div><dt>A mixed benchmark</dt><dd>APXMIDP is volume-weighted across day-ahead and intraday trades, not one '
        'auction.</dd></div>'
        '<div><dt>A −500 GBP/MWh floor</dt><dd>In an earlier version about 46% of the bias came from the 12% of periods '
        'where clearing hit the floor.</dd></div>'
        '<div><dt>No calibration read</dt><dd>The realised inputs have degenerate quantiles, so coverage says nothing '
        'here.</dd></div></dl>')
    entries = [
        model("demand", "Day-ahead demand", ["day_ahead.lgbm_demand.v1", "day_ahead.lgbm_demand.v2"],
              "<code>models.demand_forecast</code> and <code>models.demand_forecast_v2</code>",
              [("Target", "GB national demand outturn, half-hourly, MW: <code>elexon/indo</code>, "
                          "<code>initial_demand_outturn_mw</code>"),
               ("Method", "LightGBM quantile regression, one model per quantile from 0.05 to 0.95, sorted to stay "
                          "monotone, with a conformal outer band. Version 2 adds weather and calendar features"),
               ("Horizon", "24 hours ahead"),
               ("As it stands", "21 version-1 entries and one version-2 entry in the manifest; walk-forward backtests "
                                "in gold; one issued version-2 forecast, 4 to 6 September 2026")],
              dem_plate + dem_scores + folds),
        model("wind", "Wind generation", ["wind.lgbm_quantile.v1"], "<code>models.wind_forecast</code>",
              [("Target", "GB wind outturn, half-hourly, MW: <code>elexon/fuelhh</code> where the fuel type is WIND"),
               ("Method", "LightGBM quantile regression, seven quantiles, on weather at 12 wind sites; WINDFOR is the "
                          "benchmark"),
               ("Horizon", "24 hours ahead"),
               ("As it stands", "A configuration, a model card and a training dataset. No registered versions, forecasts "
                                "or scores")]),
        model("solar", "Solar generation", ["solar.lgbm_quantile.v1"], "<code>models.solar_forecast</code>",
              [("Target", "Configured as <code>elexon/fuelhh</code> SOLAR, which holds no rows. The model card names "
                          "the solar column of <code>neso_data_portal/historic_generation_mix</code> as its successor"),
               ("Method", "LightGBM quantile regression, seven quantiles, on weather at 6 solar sites; persistence is "
                          "the benchmark"),
               ("Horizon", "24 hours ahead"),
               ("As it stands", "A configuration and a model card. No registered versions, forecasts or scores")]),
        model("stack", "GB merit-order stack", ["stack.gb.v1"], "<code>models.stack</code>",
              [("Target", "The GB supply curve for a settlement period: units ranked by short-run marginal cost, "
                          "cumulative MW against GBP/MWh, floored at −500"),
               ("Method", "Constructed, nothing fitted: plant from <code>elexon/bmunits_reference</code>, availability from "
                          "<code>elexon/remit</code>, fuel and carbon prices from <code>data/manual/commodities.csv</code>, "
                          "technology from <code>plant_technology.yaml</code>"),
               ("Horizon", "A point in time: a decision time <code>as_of</code> and a target period"),
               ("As it stands", "Supply-curve points published in gold with each fundamentals run, 87,678 in the "
                                "headline run. It has no score of its own; it is scored through the fundamentals model")]),
        model("smp", "Fundamentals SMP", ["fundamentals_smp.gb.v1"], "<code>models.fundamentals_smp</code>",
              [("Target", "GB day-ahead system marginal price, half-hourly, GBP/MWh, scored against "
                          "<code>elexon/mid</code> APXMIDP"),
               ("Method", "The stack cleared against residual demand: INDO less wind, less solar, less signed netting. "
                          "Nothing is fitted"),
               ("Horizon", "Day-ahead, half-hourly"),
               ("As it stands", "A headline backtest and 13 monthly diagnostic runs, published in "
                                "<code>gold_stack_clearing</code>, <code>gold_stack_residual_demand</code> and "
                                "<code>gold_stack_supply_curve_points</code>")],
              smp_scores),
    ]
    ents = part("five", "The five models", "Demand, wind and solar forecast the inputs; the stack turns plant into a "
                                           "supply curve; the fundamentals model clears one against the other.",
                f'<ul class="ents" aria-label="Models">{"".join(entries)}</ul>')
    cells = [("from gridflow_models import setup_notebook\ndata, models, common = setup_notebook()"),
             "models.list()",
             "models.demand_forecast.model_card()",
             "as_of = common.datetime(2026, 8, 1, tzinfo=common.utc)\ncurve = models.stack.build(as_of)"]
    nb = ('<div class="nb"><div class="nb-bar"><span class="nb-tab">models.ipynb</span><span class="nb-kern">'
          'Python 3</span></div><div class="nb-body">'
          + "".join(f'<div class="cell"><span class="pr">In [{i}]:</span><pre class="in">{hl(c)}</pre></div>'
                    for i, c in enumerate(cells, 1)) + '</div></div>')
    wb = part("workbench", "In the workbench",
              "Notebooks are call sites only; the model logic lives in the library. <code>models.list()</code> returns "
              "each model’s id, family, version, status and last training time.",
              f'<div class="split"><div class="m-head"><h3>Handles</h3><p><code>demand_forecast</code>, '
              f'<code>demand_forecast_v2</code>, <code>wind_forecast</code>, <code>solar_forecast</code>, '
              f'<code>stack</code> and <code>fundamentals_smp</code>.</p></div><div>{nb}</div></div>')
    body = "<main>" + scores + ents + wb + "</main>"
    return "Models", head, body


# ================================================================ assemble
PAGES = {"data-sources": (page_data_sources, "Data sources"), "vendor-elexon": (page_elexon, "Data sources"),
         "architecture": (page_architecture, "Architecture"), "models": (page_models, "Models")}

EXTRA_CSS = """.toc-l ol{list-style:none;margin:24px 0 0;padding:0;display:flex;flex-wrap:wrap;column-gap:22px;row-gap:6px;max-width:640px;font-size:15px}
.toc-l a{color:#CFE0DC;text-decoration-color:rgba(175,198,78,.55)}
.toc-l a:hover{color:#F6F4EC;text-decoration-color:#AFC64E}
.hub .tl-h{align-items:baseline;margin:0 0 22px}
.hub .tl-h .arrange{grid-column:1/3;margin:0}
.two-tl{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:40px}
.plate + .sc{margin-top:26px}
.folds tbody th{border-bottom:0}
.cell{grid-template-columns:66px minmax(0,1fr)}
.part{margin-top:92px}
.plate text.mono{font-family:"Red Hat Mono",monospace}
.g-head{display:grid;grid-template-columns:272px minmax(0,1fr);column-gap:72px;align-items:baseline;margin:0 0 12px}
.g-head h3{font-size:23px;font-weight:720;font-stretch:90%;line-height:1.1;letter-spacing:-.01em}
.g-head p{margin:0;font-size:14.5px;line-height:1.5;color:#3F4A3B}
.key4 .tl li{grid-template-columns:110px 280px 560px minmax(0,1fr)}
.v-ent{padding:24px 0 26px}
.v-ent .mk{margin:0 0 10px}
.v-ent .acc{margin:0 0 14px}
.facts.four{grid-template-columns:repeat(4,minmax(0,1fr));column-gap:28px}
.reach{margin:10px 0 0;font-size:14px;line-height:1.5;color:#3F4A3B}
.reach code{color:#1C2B22;font-size:13.5px}
.ent .n a{text-decoration-color:#66793B}
.ent .slot,.part .slot{color:#1C2B22;font-weight:600}
.band-in .t{justify-self:start}
.hub .tl li,.hub .tl-h{grid-template-columns:170px minmax(0,1fr) 350px 90px}
@media (max-width: 760px){.two-tl{grid-template-columns:minmax(0,1fr)}.tl li{grid-template-columns:minmax(0,1fr) !important;row-gap:2px;padding:8px 0}.g-head{grid-template-columns:minmax(0,1fr);row-gap:4px}.tl .r{text-align:left} }
.sub-h{margin:34px 0 12px;font-size:23px;font-weight:720;font-stretch:90%;line-height:1.1;letter-spacing:-.01em}
.lh{font-size:42px;font-weight:720;font-stretch:88%;line-height:1.02;letter-spacing:-.018em}
.disk{margin-top:40px}
.fields{margin:0;font-size:14.5px;line-height:1.75;color:#3F4A3B;max-width:78ch}
.fields code{color:#1C2B22;font-size:13.5px}
.prose + .well,.prose + pre{margin-top:18px}
.smp-cav{margin-top:18px}
.ent .id br + code{margin-top:2px}
"""


def page(slug: str) -> str:
    fn, current = PAGES[slug]
    title, head, body = fn()
    height = HEIGHTS[slug]
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{FONTS}
<style>
{CSS}{EXTRA_CSS}</style>
</helmet>
<div class="root" style="width: {W}px; height: {height}px; overflow: hidden; position: relative">
<div class="flow">
{head}
{body}
{footing(current)}
</div>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{W},"height":{height}}}}}'>
class Component extends DCLogic {{
renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
"""


def static(dc: str) -> str:
    s = dc.replace('<script src="./support.js"></script>', "")
    s = re.sub(r"</?x-dc>", "", s)
    s = re.sub(r"</?helmet>", "", s)
    s = re.sub(r"<script type=\"text/x-dc\".*?</script>\n", "", s, flags=re.S)
    s = s.replace("<head>", '<head>\n<meta name="viewport" content="width=device-width, initial-scale=1">', 1)
    return s


if __name__ == "__main__":
    (HERE / "static").mkdir(exist_ok=True)
    for slug in PAGES:
        out = page(slug)
        body_only = out.split('<script type="text/x-dc"')[0]
        assert "{{" not in body_only and "}}" not in body_only, f"{slug}: template-hole syntax in markup"
        assert "/>" not in re.sub(r"<(meta|link|br|input)[^>]*>", "", body_only), f"{slug}: self-closing tag"
        assert "—" not in body_only, f"{slug}: em dash"
        (HERE / f"C-{slug}.dc.html").write_text(out, encoding="utf-8")
        (HERE / "static" / f"C-{slug}.html").write_text(static(out), encoding="utf-8")
        print(slug, HEIGHTS[slug], len(out))
