"""E-vendor-elexon: the vendor-hub sheet, rendered for Elexon. Plate: the Elexon feed drawn as one cable, cut back
to its cores, one core per dataset, bundled by theme. A vendor with three datasets draws as a three-core cable in
one bundle with one key entry (see the notes)."""
from __future__ import annotations

from sheet import (PLATE_TOP, BRONZE, DAY, G, HORIZON, INK, KHAKI, ONP2, PACK, RULE, band, block, cable, deep, esc, f, height_for,
                   land_top, line_chart, page, pylon, a_substation, catenary, sky, sky_svg, sub_contact, write)

THEMES = [
    ("Prices and balancing", "Imbalance prices, market index, acceptances",
     ["system_prices", "market_depth", "mid", "boal", "pn", "disbsad", "netbsad", "soso"]),
    ("Generation and availability", "Outturn by fuel, wind forecast, availability",
     ["fuelhh", "fuelinst", "agpt", "agws", "windfor", "fou2t14d", "uou2t14d", "nonbm"]),
    ("Demand", "Outturn and forecasts, national and transmission",
     ["indo", "itsdo", "indod", "atl", "ndf", "ndfd", "tsdf", "tsdfd", "inddem"]),
    ("System indicators", "Margin, imbalance, loss of load, frequency",
     ["indgen", "imbalngc", "melngc", "lolpdrm", "freq", "temp"]),
    ("Reference and messages", "BM units and REMIT messages", ["bmunits_reference", "remit"]),
]
DESC = {
    "system_prices": "System sell price and system buy price per settlement period",
    "market_depth": "Settlement market depth per settlement period",
    "pn": "Physical notifications",
    "boal": "Bid-offer acceptance levels, final (replaces the deprecated BOAL)",
    "disbsad": "Disaggregated balancing services adjustment data",
    "mid": "Market index data",
    "netbsad": "Net balancing services adjustment data",
    "soso": "SO-SO prices (cross-border interconnector trading)",
    "fuelhh": "Half-hourly generation outturn by fuel type",
    "fuelinst": "Instantaneous generation outturn by fuel type",
    "agpt": "Actual aggregated generation per type (B1620)",
    "agws": "Actual or estimated wind and solar power generation (B1630)",
    "windfor": "Wind generation forecast",
    "fou2t14d": "2 to 14 day-ahead generation availability by fuel type",
    "uou2t14d": "2 to 14 day-ahead generation availability by BM unit",
    "nonbm": "Non-BM STOR generation",
    "indo": "Initial national demand outturn",
    "itsdo": "Initial transmission system demand outturn",
    "indod": "Initial national demand outturn (daily total)",
    "atl": "Actual total load per bidding zone (B0610)",
    "ndf": "National demand forecast (day-ahead)",
    "ndfd": "National demand forecast (2 to 14 days ahead)",
    "tsdf": "Transmission system demand forecast",
    "tsdfd": "2 to 14 day-ahead transmission system demand forecast",
    "inddem": "Day and day-ahead indicated demand",
    "indgen": "Day and day-ahead indicated generation",
    "imbalngc": "Indicated imbalance",
    "melngc": "Indicated margin",
    "lolpdrm": "Loss of load probability and de-rated margin",
    "freq": "System frequency",
    "temp": "Temperature data",
    "bmunits_reference": "All BM unit reference data",
    "remit": "REMIT outage and unavailability messages",
}
_DS = {d["key"]: d for d in PACK["data_sources"]["elexon_hub"]["datasets"]}
assert sorted(_DS) == sorted(k for _, _, ks in THEMES for k in ks) == sorted(DESC)
for _n, _g, _ks in THEMES:
    assert all(_DS[k]["proposed_theme"] == _n for k in _ks), _n


def code_of(k: str) -> str:
    d = _DS[k]
    if d.get("bmrs_code"):
        return d["bmrs_code"]
    return {"system_prices": "/balancing/settlement/system-prices/{date}",
            "market_depth": "/balancing/settlement/market-depth/{date}"}.get(k, d["api_path"])


# ---------------------------------------------------------------- the plate
PITCH, ROW0, W = 100, 8, 840
PY = PLATE_TOP
X_SS = 1300                     # substation (page x); its cable drops at its centre
XC = X_SS + 58 - 80 - 360 - 80  # the same x in the drawing's own coordinates
CP = 5.4                        # core pitch inside a bundle


def centres() -> list[float]:
    return [ROW0 + i * PITCH + 34 for i in range(len(THEMES))]


def drawing() -> str:
    ys = centres()
    total = sum(len(k) for _, _, k in THEMES)
    gy = (ys[0] + ys[-1]) / 2 + 6
    g, t = [], []
    # the sheath: down from the ground line, then left to the gland
    top = G - PY - 1
    sheath = f"M{f(XC)} {f(top)} V{f(gy - 34)} Q{f(XC)} {f(gy)} {f(XC - 34)} {f(gy)} H632"
    g.append(cable(sheath, BRONZE, 13, 8.5))
    g.append(f'<rect x="616" y="{f(gy - 11)}" width="16" height="22" rx="2" fill="{INK}"></rect>')
    g.append(f'<path d="M620 {f(gy - 11)} V{f(gy + 11)} M628 {f(gy - 11)} V{f(gy + 11)}" stroke="{DAY}" '
             f'stroke-width=".8" opacity=".6"></path>')
    # the cores: out of the gland mouth, fanned into the five bundles, straight on to the terminal strips
    cores, j = [], 0
    for (_, _, keys), yc in zip(THEMES, ys):
        n = len(keys)
        for k in range(n):
            y1 = yc + (k - (n - 1) / 2) * CP
            y0 = gy - 7 + 14 * j / (total - 1)
            cores.append(f"M614 {f(y0)} C470 {f(y0)} 450 {f(y1)} 336 {f(y1)} H46")
            j += 1
    d = " ".join(cores)
    g.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"></path>')
    g.append(f'<path d="{d}" fill="none" stroke="{BRONZE}" stroke-width="1" stroke-linecap="round"></path>')
    for (_, _, keys), yc in zip(THEMES, ys):
        n = len(keys)
        hh = (n - 1) * CP / 2 + 5
        g.append(f'<rect x="296" y="{f(yc - hh)}" width="9" height="{f(2 * hh)}" rx="1.5" fill="{KHAKI}" '
                 f'stroke="{INK}" stroke-width="1.1"></rect>')
        g.append(f'<rect x="22" y="{f(yc - hh - 2)}" width="26" height="{f(2 * hh + 4)}" rx="2" fill="{RULE}" '
                 f'stroke="{INK}" stroke-width="1.1"></rect>')
        g.append("".join(f'<circle cx="35" cy="{f(yc + (k - (n - 1) / 2) * CP)}" r="1.9" fill="{INK}"></circle>'
                         for k in range(n)))
    t.append(f'<text x="624" y="{f(gy - 22)}" text-anchor="middle">sheath cut back</text>')
    t.append(f'<text x="336" y="{f(ys[-1] + 36)}" text-anchor="end">one core for each dataset</text>')
    h = ROW0 + len(THEMES) * PITCH - 20
    aria = ("The Elexon feed drawn as one cable coming down from the substation. Its sheath is cut back and 33 cores "
            "fan out into five bundles, each tied and wired to a terminal strip: prices and balancing, 8 cores; "
            "generation and availability, 8; demand, 9; system indicators, 6; reference and messages, 2.")
    return (f'<svg width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" aria-label="{esc(aria)}">'
            + "".join(g) + f'<g font-family="Hanken Grotesk" font-style="italic" font-size="13.5" fill="{INK}">'
            + "".join(t) + "</g></svg>")


def mark(n: int) -> str:
    m = min(n, 6)
    ys = [9 + (k - (m - 1) / 2) * 2.6 for k in range(m)]
    lines = " ".join(f"M3 {f(y)} H28" for y in ys)
    return (f'<svg class="mk" width="30" height="18" viewBox="0 0 30 18" aria-hidden="true">'
            f'<path d="{lines}" stroke="{INK}" stroke-width="1.6"></path>'
            f'<path d="{lines}" stroke="{BRONZE}" stroke-width=".6"></path>'
            f'<rect x="17" y="{f(ys[0] - 2.6)}" width="4" height="{f(ys[-1] - ys[0] + 5.2)}" rx="1" fill="{KHAKI}" '
            f'stroke="{INK}" stroke-width=".9"></rect></svg>')


def plate() -> str:
    items = "".join(
        f'<li style="height: {PITCH}px">{mark(len(keys))}<div><h3>{name}</h3><p class="d">{gl}</p>'
        f'<p class="keys">{", ".join(f"<a href=\"#\">{k}</a>" for k in keys)}</p></div></li>'
        for name, gl, keys in THEMES)
    cap = ("Elexon drawn as one cable, cut back to its cores: one core for each dataset gridflow ingests, bundled in "
           "the five themes this page files them under.")
    inner = (f'<h2 class="ph" id="p-h">The datasets, bundled by theme</h2><div class="pgrid">'
             f'<ul class="ix" style="margin-top: {ROW0}px" aria-label="The five themes, keyed to the bundles">'
             f'{items}</ul><figure class="pfig">{drawing()}<figcaption>{cap}</figcaption></figure></div>')
    return band("topsoil", 12, inner, "plate", "p-h")


# ---------------------------------------------------------------- register (bronze)
def register() -> str:
    groups = []
    for name, _, keys in THEMES:
        rows = "".join(f'<li><span class="k"><a href="#">{k}</a></span><span class="c">{esc(code_of(k)).replace("/", "/&#8203;")}</span>'
                       f'<span class="t">{DESC[k]}</span></li>' for k in keys)
        groups.append(f'<div class="tg"><h3>{name}</h3><ul class="tl">{rows}</ul></div>')
    gloss = ("One line each, from the connector’s own description. The middle column is the BMRS code, or the "
             "API path where there is none.")
    return band("bronze", 24, block("reg-h", "Every Elexon dataset", gloss, "".join(groups)), "det", "reg-h")


# ---------------------------------------------------------------- specimen (silver)
def specimen() -> str:
    s = PACK["series"]["elexon_hub"]
    pts = s["points"]
    v = [p[1] for p in pts]
    idx = {p[0]: i for i, p in enumerate(pts)}
    xt = [(idx[f"{y}-01"], str(y)) for y in range(2022, 2027)]
    aria = (f"Line chart of GB transmission-metered wind generation, monthly mean, September 2021 to August 2026, in "
            f"MW. It moves between {min(v):,.0f} and {max(v):,.0f} MW, higher in winter months.")
    svg = line_chart(840, 320, len(v), 0, 12000,
                     [(0, "0"), (4000, "4,000"), (8000, "8,000"), (12000, "12,000")], xt,
                     [{"v": v, "c": HORIZON, "w": 2, "label": "monthly mean"}], aria, ylab="MW", mr=110)
    cap = ("<code>elexon/fuelhh</code> silver, <code>fuel_type</code> WIND, <code>generation_mw</code>, deduplicated on "
           "settlement date, period and fuel type, then the mean for each calendar month. MW, September 2021 to "
           "August 2026.")
    gloss = ("<code>fuelhh</code> records transmission-metered outturn by fuel type every settlement period. It has no "
             "solar fuel type, so GB solar comes from the NESO Data Portal.")
    return band("silver", 38, block("spec-h", "GB wind generation, month by month", gloss,
                                    f'<figure class="fig">{svg}<figcaption>{cap}</figcaption></figure>'),
                "det", "spec-h")


# ---------------------------------------------------------------- reach + checks (gold)
def reach_checks() -> str:
    lc = [
        ("On this site", "Each dataset page sits under the vendor, by key.",
         "data-sources/elexon/fuelhh.html\ndata-sources/elexon/system_prices.html"),
        ("In a notebook", "The Elexon client, and the cross-source day-ahead benchmark built on <code>mid</code>.",
         "data.elexon.list_datasets()\n"
         'df = data.elexon.query(<span class="s">"fuelhh"</span>, <span class="s">"2026-08-01"</span>, '
         '<span class="s">"2026-08-05"</span>)\n'
         "data.elexon.system_prices(start, end)\ndata.gb_day_ahead_benchmark(start, end)"),
        ("In DuckDB", "<code>system_prices</code>, <code>remit</code> and <code>fou2t14d</code> keep every capture; "
                      "their <code>_latest</code> views keep the newest.",
         '<span class="k">select</span> * <span class="k">from</span> silver_elexon_fuelhh\n'
         '<span class="k">select</span> * <span class="k">from</span> silver_elexon_system_prices_latest\n'
         '<span class="k">select</span> * <span class="k">from</span> gold_gb_day_ahead_benchmark'),
    ]
    rows = "".join(f'<li><div><h3>{a}</h3><p>{b}</p></div><pre class="well">{c}</pre></li>' for a, b, c in lc)
    reach = block("reach-h", "Reach it from code", "Three ways to the same rows.", f'<ul class="lc">{rows}</ul>')
    ck = [
        ("No key", "Every Elexon dataset answered HTTP 200 without a key when the vault checked them on 8 May 2026."),
        ("One imbalance price", "<code>system_sell_price</code> equals <code>system_buy_price</code> on all 88,694 "
                                "latest-vintage rows from 1 September 2021 to 22 September 2026."),
        ("No solar in <code>fuelhh</code>", "Zero SOLAR rows from 31 August 2021 to 26 September 2026."),
        ("<code>gridflow quality</code>", "Five checks per dataset: <code>null_rate</code>, "
                                          "<code>time_series_gaps</code>, <code>range_check</code>, "
                                          "<code>row_count</code> and <code>duplicates</code>."),
    ]
    dl = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in ck)
    checks = block("ck-h", "How it is checked", "Facts about this feed that were measured, not assumed.",
                   f'<dl class="ck">{dl}</dl>')
    return band("gold", 54, reach + sub_contact(6) + checks, "det", "reach-h")


def deep_elexon() -> str:
    limits = [
        "Three Elexon endpoints are left out on purpose: <code>bod</code> (its availability is unstable), "
        "<code>generation_by_fuel</code> (a duplicate of <code>fuelhh</code>) and "
        "<code>indicative_imbalance_volumes</code> (removed by Elexon).",
        "No solar in <code>fuelhh</code>. GB solar outturn is in the NESO Data Portal’s "
        "<code>historic_generation_mix</code>.",
        "No scheduler. Data lands when someone runs <code>gridflow ingest</code>.",
    ]
    sources = [
        ("Datasets and descriptions", "<code>src/gridflow/connectors/elexon/endpoints.py</code> (<code>ENDPOINTS</code>)"),
        ("Connector", "<code>src/gridflow/connectors/elexon/client.py</code>"),
        ("API parameter styles", "the vault’s <code>30-vendors/elexon/endpoints.md</code>"),
        ("Checks above", "local silver, read directly"),
    ]
    return deep("elexon", limits, sources)


def sky_art() -> str:
    sub, _ = a_substation(X_SS, 1.0)
    pyl = [(930, .5), (1060, .58), (1196, .66)]
    parts, att = [], []
    for x, s in pyl:
        y = land_top(x) + 1
        parts.append(pylon(x, y, s))
        att.append((x, y - 92 * s))
    att.append((X_SS + 12, land_top(X_SS + 12) - 58))
    g = (f'<g stroke="{INK}" fill="none" stroke-linecap="round" stroke-width="1.35">{"".join(parts)}</g>'
         + catenary(att, 10) + sub)
    # the stub of the Elexon cable, from the substation down to the ground line
    xc = X_SS + 58
    g += cable(f"M{xc} {f(land_top(xc) - 4)} V{G + 16}", BRONZE, 13, 8.5)
    labels = [(1060, 172, "pylons", ONP2), (X_SS + 58, 208, "substation", ONP2)]
    return sky_svg(g, labels, "Drawing of lattice pylons carrying lines into a substation on the horizon. A cable "
                              "runs from the substation down into the ground.")


def build() -> str:
    ans = ("Elexon’s Insights API: GB system prices, generation outturn, BM-unit data, and demand and wind "
           "forecasts, with no key needed. 33 datasets, filed here in five themes.")
    body = sky("Elexon BMRS", ans) + plate() + register() + specimen() + reach_checks() + deep_elexon()
    return page("Elexon BMRS", "ds", sky_art(), body, height_for("E-vendor-elexon", 5600), level="true")


if __name__ == "__main__":
    write("E-vendor-elexon", build())
    print("ok", "PY", PY, "XC", XC)
