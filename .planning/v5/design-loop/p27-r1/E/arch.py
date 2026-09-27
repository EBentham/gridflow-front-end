"""E-architecture: the pipeline sheet. Plate: a section through bronze, silver and gold; every feed lands in bronze and
one dataset (Elexon system_prices) is followed down, with its real paths inscribed in each bed and the command that
carries it across each contact written on the contact."""
from __future__ import annotations

from sheet import (PLATE_TOP, pat, BRONZE, BRONZE_T, G, GOLD, GOLD_T, INK, ONP2, SILVER, SILVER_T, a_converter, a_gas_terminal,
                   a_met_mast, a_substation, band, block, cable, cable_end, deep, esc, f, height_for, land_top, page,
                   sky, sky_svg, smooth, sub_contact, swatch, wave_pts, write)

W = 840
PY = PLATE_TOP
BEDS = [("bronze", 44, 174), ("silver", 174, 304), ("gold", 304, 434)]
TINT = {"bronze": (BRONZE_T, "p-brick", .3), "silver": (SILVER_T, "p-diag", .4), "gold": (GOLD_T, "p-stip", .45)}
X_GT, X_CV, X_MM, X_SS = 776, 956, 1182, 1226
CX = {"gas terminal": X_GT + 83, "converter": X_CV + 91, "met mast": X_MM, "substation": X_SS + 58}
LOCAL = {k: v - 520 for k, v in CX.items()}
MONO = 8.1   # Red Hat Mono advance at 13.5 px


def contact(y: float, seed: int) -> list[tuple[float, float]]:
    return wave_pts(y, seed, amp=3, step=140, x0=0, x1=W)


def y_at(pts: list[tuple[float, float]], x: float) -> float:
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        if x1 <= x <= x2:
            return y1 + (y2 - y1) * (x - x1) / (x2 - x1)
    return pts[-1][1]


def mono(x: float, y: float, s: str) -> str:
    return f'<text x="{f(x)}" y="{f(y)}" font-family="Red Hat Mono" font-size="13.5">{esc(s)}</text>'


def ital(x: float, y: float, s: str) -> str:
    return (f'<text x="{f(x)}" y="{f(y)}" font-family="Hanken Grotesk" font-style="italic" font-size="13.5">'
            f'{esc(s)}</text>')


def glyph_files(x: float, y: float) -> str:
    """Two files: the body and its sidecar."""
    doc = lambda dx, dy, fill: (f'<path d="M{f(x + dx)} {f(y + dy)} h18 l7 7 v24 h-25 Z" fill="{fill}" stroke="{INK}" '  # noqa: E731
                                f'stroke-width="1.2" stroke-linejoin="round"></path><path d="M{f(x + dx + 18)} '
                                f'{f(y + dy)} v7 h7" fill="none" stroke="{INK}" stroke-width="1.2"></path>')
    lines = "".join(f'<path d="M{f(x + 13)} {f(y + 18 + 5 * k)} h14" stroke="{INK}" stroke-width=".8"></path>'
                    for k in range(3))
    return doc(0, 0, "#F6F4EC") + doc(10, 8, "#F6F4EC") + lines


def glyph_parquet(x: float, y: float) -> str:
    """A columnar file: column chunks side by side, two row groups."""
    g = [f'<rect x="{f(x)}" y="{f(y)}" width="34" height="34" fill="#F6F4EC" stroke="{INK}" stroke-width="1.2"></rect>']
    for k in range(1, 5):
        g.append(f'<path d="M{f(x + k * 6.8)} {f(y)} V{f(y + 34)}" stroke="{INK}" stroke-width=".8"></path>')
    g.append(f'<path d="M{f(x)} {f(y + 17)} H{f(x + 34)}" stroke="{INK}" stroke-width="1.2"></path>')
    g.append(f'<rect x="{f(x)}" y="{f(y)}" width="6.8" height="34" fill="{SILVER}" opacity=".7"></rect>')
    return "".join(g)


def glyph_view(x: float, y: float) -> str:
    """A view: a table outline with a header row."""
    g = [f'<rect x="{f(x)}" y="{f(y)}" width="34" height="30" fill="#F6F4EC" stroke="{INK}" stroke-width="1.2"></rect>',
         f'<rect x="{f(x)}" y="{f(y)}" width="34" height="8" fill="{GOLD}" stroke="{INK}" stroke-width="1.2"></rect>']
    for k in (15, 22):
        g.append(f'<path d="M{f(x)} {f(y + k)} H{f(x + 34)}" stroke="{INK}" stroke-width=".7"></path>')
    g.append(f'<path d="M{f(x + 13)} {f(y + 8)} V{f(y + 30)}" stroke="{INK}" stroke-width=".7"></path>')
    return "".join(g)


def drawing() -> str:
    g, t = [], []
    tops = [contact(44, 3), contact(174, 4), contact(304, 5)]
    bottom = contact(434, 6)
    for (kind, _, _), top, bot in zip(BEDS, tops, tops[1:] + [bottom]):
        fill, pat_name, op = TINT[kind]
        body = smooth(top) + " L" + " L".join(f"{f(x)} {f(y)}" for x, y in reversed(bot)) + " Z"
        defs, url = pat(pat_name)
        g.append(f'{defs}<path d="{body}" fill="{fill}"></path><path d="{body}" fill="{url}" opacity="{op}"></path>')
    g.append(f'<path d="M0 {f(tops[0][0][1])} V{f(bottom[0][1])} M{W} {f(tops[0][-1][1])} V{f(bottom[-1][1])}" '
             f'stroke="{INK}" stroke-width="1.2"></path>')
    g.append(f'<path d="{smooth(bottom)}" stroke="{INK}" stroke-width="1.2" fill="none"></path>')
    # contacts, each broken where its command is written on it
    verbs = [[("gridflow ingest", 22)], [("gridflow transform", 22)], [("gridflow build", 22), ("gridflow init", 250)]]
    for top, vs in zip(tops, verbs):
        segs, x = [], 0.0
        for s, x0 in vs:
            segs.append((x, x0 - 7))
            x = x0 + len(s) * MONO + 7
        segs.append((x, W))
        for a, b in segs:
            pts = [(a, y_at(top, a))] + [p for p in top if a < p[0] < b] + [(b, y_at(top, b))]
            g.append(f'<path d="{smooth(pts)}" stroke="{INK}" stroke-width="1.4" fill="none"></path>')
        for s, x0 in vs:
            t.append(mono(x0, y_at(top, x0 + 40) + 4.5, s))
    # inscriptions: the real paths of system_prices in each bed
    g.append(glyph_files(24, 74))
    t += [mono(80, 86, "bronze/elexon/system_prices/{YYYY}/{MM}/{DD}/"),
          mono(80, 106, "raw_{fetched_at}_{sha256[:8]}.json"),
          mono(80, 126, "raw_{fetched_at}_{sha256[:8]}.meta.json"),
          ital(80, 150, "the response as sent, written once, and its sidecar")]
    g.append(glyph_parquet(24, 200))
    t += [mono(80, 206, "silver/elexon/system_prices/year={YYYY}/month={MM}/"),
          mono(80, 225, "system_prices_{YYYYMMDD}_run{available_at}.parquet"),
          ital(80, 245, "one file per day and per capture"),
          mono(80, 268, "silver_elexon_system_prices_latest"),
          ital(80, 287, "a view: the newest capture of each settlement period")]
    g.append(glyph_view(24, 334))
    t += [mono(80, 350, "gold_uk_imbalance_context"),
          ital(80, 372, "a DuckDB view: system prices joined with NESO carbon intensity, half-hourly")]
    # the feeds: every cable lands in bronze; the substation's carries system_prices on down to the gold view
    top_y = G - PY - 1
    for name in ("gas terminal", "converter", "met mast"):
        x = LOCAL[name]
        g.append(cable(f"M{f(x)} {f(top_y)} V{f(y_at(tops[0], x) + 16)}"))
        g.append(cable_end(x, y_at(tops[0], x) + 16))
    xs = LOCAL["substation"]
    g.append(cable(f"M{f(xs)} {f(top_y)} V{f(360)}"))
    for y in (109, 239):
        g.append(f'<circle cx="{f(xs)}" cy="{y}" r="4.6" fill="{INK}"></circle>')
    g.append(f'<rect x="{f(xs - 16)}" y="352" width="32" height="30" rx="15" fill="{GOLD}" stroke="{INK}" '
             f'stroke-width="1.6"></rect><path d="M{f(xs - 16)} 367 H{f(xs - 40)}" stroke="{INK}" stroke-width="1.6">'
             f'</path>')
    h = 446
    aria = ("A section through three beds, bronze, silver and gold. Cables from a gas terminal, a converter station and "
            "a met mast end in bronze. The substation's cable, carrying Elexon system_prices, runs on through all three. "
            "gridflow ingest is written on the ground contact, gridflow transform on the bronze to silver contact, and "
            "gridflow build and gridflow init on the silver to gold contact. In bronze: the raw JSON response and its "
            "meta.json sidecar under bronze/elexon/system_prices by date. In silver: a daily Parquet file with a run "
            "suffix per capture, and the silver_elexon_system_prices_latest view. In gold: the gold_uk_imbalance_context "
            "view, joined with NESO carbon intensity.")
    return (f'<svg width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" aria-label="{esc(aria)}">'
            + "".join(g) + f'<g fill="{INK}">' + "".join(t) + "</g></svg>")


KEY = [("bronze", "Bronze", "The raw response, as sent, and a JSON sidecar. Written once, never rewritten.",
        "json, xml, csv or bin, by content type"),
       ("silver", "Silver", "Typed tables: every row validated, times in UTC, duplicates removed.",
        "Parquet, zstd"),
       ("gold", "Gold", "Ready to query: DuckDB views over silver, some joined across sources.",
        "views in gridflow.duckdb")]


def plate() -> str:
    items = "".join(f'<li style="height: 130px">{swatch(k, 30, 18).replace("<svg", "<svg class=\"mk\"", 1)}'
                    f'<div><h3>{n}</h3><p class="d">{d}</p><p class="f">{fa}</p></div></li>' for k, n, d, fa in KEY)
    cap = ("Elexon <code>system_prices</code> on its way down. Every feed lands in bronze; the command that carries data "
           "across each contact is written on it.")
    inner = (f'<h2 class="ph" id="p-h">One dataset, followed down</h2><div class="pgrid">'
             f'<ul class="ix" style="margin-top: 50px" aria-label="The three layers, keyed to the beds">{items}</ul>'
             f'<figure class="pfig">{drawing()}<figcaption>{cap}</figcaption></figure></div>')
    return band("topsoil", 13, inner, "plate", "p-h")


# ---------------------------------------------------------------- register (bronze)
REG = [
    ("bronze", "Bronze", "<code>gridflow ingest</code>",
     "Raw response bytes, exactly as the API sent them, with a JSON sidecar beside each body. Written once, never "
     "rewritten. Partitioned by the data date when known, otherwise the fetch date.",
     [("Format", "json, xml, csv or bin, by content type, plus <code>.meta.json</code>"),
      ("Path", "<code>bronze/{source}/{dataset}/{YYYY}/{MM}/{DD}/&#8203;raw_{fetched_at}_{sha256[:8]}.{ext}</code>"),
      ("Code", "<code>bronze/writer.py</code>, <code>storage/paths.py</code>")]),
    ("silver", "Silver", "<code>gridflow transform</code>",
     "One transformer per source and dataset reads the day’s bronze, validates every row against its Pydantic "
     "schema, normalises time to UTC, deduplicates on the dataset key and writes Parquet atomically.",
     [("Format", "Parquet, zstd"),
      ("Path", "<code>silver/{source}/{dataset}/year={YYYY}/month={MM}/&#8203;{dataset}_{YYYYMMDD}.parquet</code>"),
      ("Captures", "<code>{dataset}_{YYYYMMDD}_run{available_at}.parquet</code> for Elexon "
                        "<code>system_prices</code>, <code>remit</code> and <code>fou2t14d</code> and the three NESO "
                        "Data Portal datasets; <code>_latest</code> views pick the newest"),
      ("Code", "<code>silver/base.py</code>, <code>silver/registry.py</code>, <code>silver/latest_views.py</code>")]),
    ("gold", "Gold", "<code>gridflow build</code>, <code>gridflow init</code>",
     "Built from silver: one Python builder, <code>system_marginal_price</code>, and three SQL views that register "
     "when the catalogue is initialised.",
     [("Path", "<code>gold/{name}/year={YYYY}/{name}_{YYYYMMDD}.parquet</code>"),
      ("Views", "<code>gold_uk_imbalance_context</code>: Elexon system prices with NESO carbon intensity. "
                "<code>gold_gb_day_ahead_benchmark</code>: Elexon MID APXMIDP, GBP/MWh. "
                "<code>gold_eu_gas_storage</code>: GIE AGSI+ by country and day."),
      ("Code", "<code>gold/registry.py</code>, <code>gold/views/*.sql</code>")]),
    ("gold", "Model outputs", "written by gridflow-models",
     "gridflow-models writes its forecasts, metrics and stack tables into the same gold root, partitioned by model.",
     [("Tables", "<code>forecasts</code>, <code>forecast_metrics</code>, <code>stack_clearing</code>, "
                 "<code>stack_residual_demand</code>, <code>stack_supply_curve_points</code>"),
      ("Path", "<code>gold/{table}/model_slug={slug}/&#8203;{prefix}_{timestamp}_{run_id}.parquet</code>")]),
    (None, "Catalogue", "<code>gridflow init</code>",
     "One DuckDB file, <code>{data_root}/gridflow.duckdb</code>, holding run metadata and a view over every silver and "
     "gold directory.",
     [("Tables", "<code>pipeline_runs</code>, <code>pipeline_watermarks</code>, <code>quality_reports</code>"),
      ("Views", "<code>silver_{source}_{dataset}</code>, <code>silver_{source}_{dataset}_latest</code>, "
                "<code>gold_{name}</code>"),
      ("Code", "<code>storage/duckdb.py</code>")]),
]


def register() -> str:
    rows = []
    for kind, name, by, pub, dl in REG:
        sw = swatch(kind, 46, 30) if kind else ""
        dls = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in dl)
        rows.append(f'<li><div>{sw}<h3>{name}</h3><p class="sk">{by}</p></div>'
                    f'<div><p class="pub">{pub}</p><dl>{dls}</dl></div></li>')
    gloss = "Paths are relative to the data root, set by <code>GRIDFLOW_DATA_DIR</code>."
    return band("bronze", 25, block("reg-h", "Every layer, as stored", gloss, f'<ul class="reg arch">{"".join(rows)}</ul>'),
                "det", "reg-h")


# ---------------------------------------------------------------- specimen (silver)
SIDECAR = [("source", "the source key, such as <code>elexon</code>"), ("dataset", "the dataset key"),
           ("fetched_at", "when the request was made"), ("written_at", "when the body was written"),
           ("data_date", "the date the data is for, when known"), ("request_url", "with credentials masked"),
           ("request_params", "with credentials masked"), ("api_version", "the vendor API version"),
           ("http_status", "the response status"), ("content_type", "sets the body’s extension"),
           ("body_sha256", "its first 8 characters are in the file name"), ("body_size_bytes", "the body’s size"),
           ("page", "position in a paged response"), ("total_pages", "pages in the response")]
LINEAGE = [("event_time", "the time the value describes, in UTC"),
           ("available_at", "when the value became available, for as-of reads"),
           ("published_at", "when the vendor published it"), ("ingested_at", "when gridflow ingested it"),
           ("source_run_id", "the run that wrote the row"), ("dataset_version", "the dataset’s version")]


def specimen() -> str:
    c1 = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in SIDECAR)
    c2 = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in LINEAGE)
    cards = (f'<div class="cards"><div class="card"><p class="card-h">raw_….meta.json</p><dl>{c1}</dl>'
             f'<p class="card-f">Beside every bronze body.</p></div>'
             f'<div class="card"><p class="card-h">silver lineage columns</p><dl>{c2}</dl>'
             f'<p class="card-f"><code>event_time</code> is on every silver dataset; the others were on every dataset '
             f'sampled.</p></div></div>')
    gloss = "The metadata kept with every body and row, so a number can be traced back to the request that fetched it."
    return band("silver", 39, block("spec-h", "What a file and a row carry", gloss, cards), "det", "spec-h")


# ---------------------------------------------------------------- reach + checks (gold)
VERBS = [("init", "Create the DuckDB catalogue and register its views", 1209),
         ("ingest", "API to bronze", 186), ("transform", "Bronze to silver: normalised, validated, deduplicated", 261),
         ("build", "Silver to gold", 306), ("pipeline", "Ingest then transform; with --gold, build as well", 485),
         ("backfill", "Historical data, in chunks", 346), ("export-csv", "Silver Parquet to CSV", 438),
         ("status", "Run history and a quality summary", 584), ("quality", "Run the quality checks and write a report", 677),
         ("reset", "Delete bronze, silver and gold data and reset the catalogue", 796),
         ("prune", "Delete partitions older than a retention cutoff", 972)]


def reach_checks() -> str:
    rows = "".join(f'<li><span class="k">gridflow {v}</span><span class="t">{d}</span><span class="c">cli.py:{ln}</span>'
                   f'</li>' for v, d, ln in VERBS)
    reach = block("reach-h", "Reach it from code",
                  "Every run is one of these commands; <code>gridflow = gridflow.cli:app</code>. Read-only queries go "
                  "through <code>gridflow.serving.client.GridflowClient</code>.",
                  f'<ul class="tl verbs">{rows}</ul>')
    ck = [
        ("Each row", "Validated against its Pydantic schema during <code>gridflow transform</code>."),
        ("<code>gridflow quality</code>", "<code>null_rate</code>, <code>time_series_gaps</code>, "
                                          "<code>range_check</code>, <code>row_count</code> and "
                                          "<code>duplicates</code>, written to <code>quality_reports</code>."),
        ("gridflow’s CI", "On every push and pull request: <code>uv lock --check</code>, ruff check and format, "
                               "mypy, and pytest, excluding the tests that call vendor APIs."),
        ("This site", "On pull requests: a staleness check, a baseline ratchet and "
                      "<code>gridflow-build --check</code>. Before deploy: htmlhint and lychee."),
    ]
    dl = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in ck)
    checks = block("ck-h", "How it is checked", "What runs before a row, or a page, is trusted.", f'<dl class="ck">{dl}</dl>')
    return band("gold", 55, reach + sub_contact(7) + checks, "det", "reach-h")


def deep_arch() -> str:
    limits = [
        "No scheduler or orchestrator: every run is a command. The <code>schedule</code> field in the source config "
        "is not read.",
        "No cloud, object store, warehouse, streaming or cluster: local files and one embedded DuckDB file.",
        "No server, public API or hosted database.",
        "No models or forecasts. Those live in gridflow-models, which reads this store.",
    ]
    sources = [
        ("Paths", "<code>src/gridflow/storage/paths.py</code> (<code>PathBuilder</code>)"),
        ("Bronze and silver", "<code>bronze/writer.py</code>, <code>silver/base.py</code>, "
                              "<code>silver/latest_views.py</code>"),
        ("Gold and the catalogue", "<code>gold/registry.py</code>, <code>gold/views/*.sql</code>, "
                                   "<code>storage/duckdb.py</code>"),
        ("Commands and checks", "<code>cli.py</code>, <code>quality/checks.py</code>, the CI workflows"),
    ]
    return deep("arch", limits, sources)


def sky_art() -> str:
    sub, _ = a_substation(X_SS, 1.0)
    assets = a_gas_terminal(X_GT, 1.0) + a_converter(X_CV, 1.0) + a_met_mast(X_MM, .88) + sub
    for x in CX.values():
        assets += cable(f"M{f(x)} {f(land_top(x) - 3)} V{G + 16}")
    labels = [(CX["gas terminal"], 212, "gas terminal", ONP2), (CX["converter"], 181, "converter station", ONP2),
              (X_MM - 34, 150, "met mast", ONP2), (CX["substation"] + 4, 212, "substation", ONP2)]
    return sky_svg(assets, labels, "Drawing of a gas terminal, an interconnector converter station, a met mast and a "
                                   "substation on the horizon, each with a cable running down into the ground.")


def build() -> str:
    ans = ("A local Python pipeline with no server. Each API response lands untouched in bronze, becomes typed Parquet "
           "in silver, and is served as DuckDB views in gold.")
    body = sky("How data moves, bronze to gold", ans) + plate() + register() + specimen() + reach_checks() + deep_arch()
    css = (".reg.arch>li>div:first-child svg{display:block;margin:4px 0 12px}\n"
           ".verbs li{grid-template-columns:196px minmax(0,1fr) 110px}\n"
           ".verbs .k{font-size:15px}\n.verbs .c{text-align:right}\n"
           ".card-f{margin:4px 14px 10px;padding-top:8px;border-top:1px solid rgba(28,43,34,.2);font-size:13.5px;"
           "line-height:1.5;color:#3F4A3B}\n.card-f code{font-size:12.5px;color:#1C2B22}\n"
           ".card dl div{grid-template-columns:136px minmax(0,1fr)}\n")
    return page("Architecture", "arch", sky_art(), body, height_for("E-architecture", 5000), css)


if __name__ == "__main__":
    write("E-architecture", build())
    _ = (BRONZE,)
    print("ok")
