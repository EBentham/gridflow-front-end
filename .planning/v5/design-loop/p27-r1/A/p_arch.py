"""Page 3: architecture. The full descent under the homepage's landscape. Four feeds come down through the
connectors (topsoil) and splice into one cable at the bronze contact; the cable's core changes colour at each
contact, and each contact is labelled with the command that moves data across it. Each stratum holds its real
path, drawn as a keyed path, with its formats and views; the build and the gates sit in the deep."""
from __future__ import annotations

import math

import hp
from frame import (BRONZE, DAY, GOLD, INK, OLIVE, PACK, SILVER, SOFT, T, T_BRONZE, T_GOLD, T_SILVER, cable,
                   contact_y, f, footer, masthead, sleeve, smooth, strata_svg, terminal)

NAME = "A-architecture"
TITLE = "Architecture"
PG = "architecture"
S = 780
DY = S - 940                    # the homepage landscape, lifted onto this page's cut
LANE = [1344, 1358, 1372, 1386]  # the four feeds in the right margin
TRUNK = 1365
A = PACK["architecture"]


def prof(x: float) -> float:
    return hp.prof(x) + DY          # hp.Y["surf"] stays 940 on this page


# ---------------------------------------------------------------- keyed paths
CW = .6                             # Red Hat Mono advance, measured


def keyed(parts: list[tuple[str, str | None, int]], fs: float = 17, y0: float = 20, x0: float = 0,
          label_w: float = 1240) -> tuple[str, float]:
    """A path template in mono with a dimension bracket under each placeholder and an italic label on one of two
    tiers. Returns (svg body, height)."""
    cw = CW * fs
    out_t, out_b, out_l = [], [], []
    x = x0
    yb = y0 + 9
    for text, label, tier in parts:
        w = len(text) * cw
        cls = "ph" if label else "lit"
        out_t.append(f'<tspan class="{cls}">{text}</tspan>')
        if label:
            a, b = x + 1.5, x + w - 1.5
            ly = yb + (22 if tier == 1 else 46)
            out_b.append(f"M{f(a)} {f(yb - 3)} V{f(yb)} H{f(b)} V{f(yb - 3)} M{f(a + 6)} {f(yb)} V{f(ly - 13)}")
            out_l.append(f'<text x="{f(a + 1)}" y="{f(ly)}">{label}</text>')
        x += w
    body = (f'<text x="{f(x0)}" y="{f(y0)}" class="kp" font-size="{fs}">{"".join(out_t)}</text>'
            f'<path d="{" ".join(out_b)}" stroke="{INK}" stroke-width="1" fill="none"></path>'
            f'<g class="kl">{"".join(out_l)}</g>')
    return body, yb + 54            # the bottom, absolute


def keyed_svg(rows: list[tuple[list[tuple[str, str | None, int]], float]], aria: str, w: int = 1220) -> str:
    g, y = [], 0.0
    for parts, x0 in rows:
        body, bottom = keyed(parts, y0=y + 20, x0=x0)
        g.append(body)
        y = bottom + 6
    return (f'<svg class="kpath" width="{w}" height="{f(y)}" viewBox="0 0 {w} {f(y)}" role="img" '
            f'aria-label="{aria}">{"".join(g)}</svg>')


BRONZE_PATH = [("bronze/", None, 0), ("{source}", "source key", 1), ("/", None, 0), ("{dataset}", "dataset", 2),
               ("/", None, 0), ("{YYYY}/{MM}/{DD}", "data date, else the fetch date", 1), ("/raw_", None, 0),
               ("{fetched_at:%Y%m%dT%H%M%SZ}", "when it was fetched, UTC", 2), ("_", None, 0),
               ("{sha256[:8]}", "first 8 characters of the body’s SHA-256", 2), (".", None, 0),
               ("{ext}", "json, xml, csv or bin, by content type", 1)]
SILVER_PATH = [("silver/", None, 0), ("{source}", "source key", 1), ("/", None, 0), ("{dataset}", "dataset", 2),
               ("/year=", None, 0), ("{YYYY}", "year", 1), ("/month=", None, 0), ("{MM}", "month", 2),
               ("/", None, 0), ("{dataset}_{YYYYMMDD}", "one file per date", 1), (".parquet", None, 0)]
SILVER_RUN = [("{dataset}_{YYYYMMDD}", None, 0), ("_run{available_at}", "append-only: one file per capture", 1),
              (".parquet", None, 0)]


# ---------------------------------------------------------------- content
def html() -> tuple[str, str]:
    facts = [("Data root", "<code>GRIDFLOW_DATA_DIR</code>"), ("Catalogue", "<code>{data_root}/gridflow.duckdb</code>"),
             ("Entry point", "<code>gridflow = gridflow.cli:app</code>"), ("Licence", "Apache-2.0")]
    dl = "".join(f'<div><dt>{T(PG, a)}</dt><dd>{b}</dd></div>' for a, b in facts)
    lede = (f'<p class="lead">{T(PG, "gridflow is a local-first Python pipeline built on Polars, DuckDB, Pydantic v2, httpx and Typer.")}</p>'
            f'<p>{T(PG, "It has no server and no scheduler. Every run is a command, and everything it keeps is a file under one data root.")}</p>'
            f'<dl class="facts">{dl}</dl>')
    sky = (f'<section class="sky" data-st="sky" style="height: {S}px" aria-labelledby="h1">{masthead("Architecture")}'
           f'<div class="hero"><div><h1 id="h1">{T(PG, "From a vendor’s response to a DuckDB view")}</h1></div>'
           f'<div class="lede">{lede}</div></div></section>')

    keys = ["elexon", "entsoe", "entsog", "gie_agsi", "gie_alsi", "neso", "neso_data_portal", "open_meteo"]
    top = (f'<section class="st st-top" data-st="topsoil" aria-labelledby="c-h"><div class="lay">'
           f'<div><h2 class="fig-h" id="c-h">{T(PG, "One connector per source key")}</h2>'
           f'<p class="body">{T(PG, "Each source has an async client,")} <code>connectors/&lt;source&gt;/client.py</code>'
           f'{T(PG, ", with the rate limit and retries set for it in")} <code>config/sources.yaml</code> '
           f'{T(PG, "(Elexon 2 requests a second, ENTSO-E 1). GIE has two keys, one per API.")}</p></div>'
           f'<ul class="keys" aria-label="{T(PG, "Source keys")}">' + "".join(f"<li>{k}</li>" for k in keys)
           + '</ul></div></section>')

    side = A["layers"][0]["sidecar_fields"]
    side_li = "".join(f"<li>{s.replace(' (credentials masked)', '').replace(' (masked)', '')}</li>" for s in side)
    b_aria = T(PG, "The bronze path template: bronze, source key, dataset, the data date (else the fetch date) as year, "
                   "month and day, then raw_, the fetch time in UTC, the first 8 characters of the body's SHA-256 and "
                   "an extension set by content type.")
    bronze = (f'<section class="st st-bronze" data-st="bronze" aria-labelledby="b-h"><div class="lay">'
              f'<div><h2 class="big" id="b-h">{T(PG, "Bronze keeps every response as it arrived")}</h2>'
              f'<p class="body">{T(PG, "The body is written first, then a JSON sidecar with the same stem, each through a temporary file and")} '
              f'<code>os.replace</code>{T(PG, ". Nothing in bronze is rewritten.")}</p></div>'
              f'<div class="side"><p class="mini">{T(PG, "The sidecar,")} <code>.meta.json</code></p>'
              f'<ul class="fields">{side_li}</ul>'
              f'<p class="note">{T(PG, "The request URL and parameters are stored with credentials masked.")}</p></div></div>'
              f'<figure class="kfig">{keyed_svg([(BRONZE_PATH, 0)], b_aria)}</figure></section>')

    steps = [T(PG, "reads that date’s bronze and parses it"),
             T(PG, "validates every row against the dataset’s Pydantic schema"),
             T(PG, "normalises every timestamp to UTC"),
             T(PG, "deduplicates on the dataset’s key"),
             T(PG, "writes zstd Parquet, atomically")]
    cols = ["event_time", "available_at", "published_at", "ingested_at", "source_run_id", "dataset_version"]
    ao = ["elexon system_prices", "remit", "fou2t14d", "and the NESO Data Portal’s three"]
    fname_x = len("silver/{source}/{dataset}/year={YYYY}/month={MM}/") * CW * 17
    s_aria = T(PG, "The silver path template: silver, source key, dataset, year= and month= partitions, then one file "
                   "per date named after the dataset. Append-only datasets add _run and the capture's available_at "
                   "before .parquet, one file per capture.")
    silver = (f'<section class="st st-silver" data-st="silver" aria-labelledby="s-h"><div class="lay">'
              f'<div><h2 class="big" id="s-h">{T(PG, "Silver holds typed, validated, deduplicated tables")}</h2>'
              f'<p class="body">{T(PG, "One transformer per source and dataset. For each date it:")}</p>'
              f'<ol class="steps">' + "".join(f"<li>{x}</li>" for x in steps) + '</ol></div>'
              f'<div class="side"><p class="mini">{T(PG, "Columns every table carries")}</p>'
              f'<p class="note"><code>event_time</code> {T(PG, "is on every silver table. The tables checked also carry")} '
              + ", ".join(f"<code>{c}</code>" for c in cols[1:]) + f'{T(PG, ", which is what makes as-of reads possible downstream.")}</p>'
              f'<p class="mini">{T(PG, "Append-only datasets")}</p>'
              f'<p class="note">{T(PG, "Six keep every capture instead of overwriting:")} {", ".join(ao[:3])} {ao[3]}. '
              f'{T(PG, "A")} <code>_latest</code> {T(PG, "view returns the newest capture for each key.")}</p></div></div>'
              f'<figure class="kfig">{keyed_svg([(SILVER_PATH, 0), (SILVER_RUN, fname_x)], s_aria)}</figure></section>')

    views = [("silver_{source}_{dataset}", T(PG, "one view per silver dataset")),
             ("silver_{source}_{dataset}_latest", T(PG, "the newest capture, for append-only datasets")),
             ("gold_{name}", T(PG, "one view per gold directory")),
             ("gold_uk_imbalance_context", T(PG, "Elexon system prices with NESO carbon intensity, half-hourly")),
             ("gold_gb_day_ahead_benchmark", T(PG, "Elexon MID APXMIDP, GBP/MWh: the GB day-ahead benchmark")),
             ("gold_eu_gas_storage", T(PG, "GIE AGSI+ storage by country and day"))]
    vrows = "".join(f"<tr><th scope=\"row\"><code>{a}</code></th><td>{b}</td></tr>" for a, b in views)
    paths = [(T(PG, "gridflow’s builder"), "gold/{name}/year={YYYY}/{name}_{YYYYMMDD}.parquet"),
             (T(PG, "gridflow-models"), "gold/{table}/model_slug={slug}/{prefix}_{YYYYMMDDTHHMMSSZ}_{run_id}.parquet")]
    prow = "".join(f"<div><dt>{a}</dt><dd><code>{b}</code></dd></div>" for a, b in paths)
    gold = (f'<section class="st st-gold" data-st="gold" aria-labelledby="g-h"><div class="lay">'
            f'<div><h2 class="big" id="g-h">{T(PG, "Gold is what DuckDB serves")}</h2>'
            f'<p class="body"><code>gridflow init</code> {T(PG, "registers a view for every silver and gold directory, and the SQL views, in")} '
            f'<code>gridflow.duckdb</code>. <code>gridflow build</code> {T(PG, "runs the registered gold builder,")} '
            f'<code>system_marginal_price</code>{T(PG, ". gridflow-models writes its forecasts and backtests into the same gold root.")}</p>'
            f'<dl class="gpaths">{prow}</dl></div>'
            f'<div><table class="views"><caption data-t="views">{T(PG, "Views in gridflow.duckdb")}</caption><tbody>{vrows}</tbody></table>'
            f'<p class="note">{T(PG, "Beside them, three tables:")} <code>pipeline_runs</code>, <code>pipeline_watermarks</code>, '
            f'<code>quality_reports</code>. {T(PG, "Python reads it all through")} <code>GridflowClient</code>{T(PG, ", which is read-only.")}</p>'
            f'</div></div></section>')

    verbs = A["cli"]["verbs"]
    vd = {k: v.split(" - ", 1)[1] for k, v in verbs.items()}
    VERB_TXT = {
        "init": "create the catalogue and register views", "ingest": "API to bronze", "transform": "bronze to silver",
        "build": "silver to gold", "pipeline": "ingest then transform, then build with <code>--gold</code>",
        "backfill": "history, in chunks", "export-csv": "silver Parquet to CSV", "status": "run history and quality",
        "quality": "run the data checks, write a report", "reset": "delete layers and reset the catalogue",
        "prune": "delete partitions older than a cutoff"}
    cli = "".join(f"<div><dt><code>{k}</code></dt><dd>{T(PG, VERB_TXT[k])}</dd></div>" for k in verbs)
    _ = vd
    checks = ", ".join(f"<code>{c}</code>" for c in A["quality_checks"]["names"])
    code_ci = ["uv lock --check", "ruff check", "ruff format --check", "mypy", 'pytest -m "not live"']
    nots = [T(PG, "No scheduler: the schedule field in sources.yaml is read nowhere."),
            T(PG, "No server, public API or hosted database."),
            T(PG, "No cloud, object store, streaming or cluster."),
            T(PG, "No live feed: data lands when someone runs ingest."),
            T(PG, "No models: those live in gridflow-models.")]
    deep = (f'<section class="st st-deep" data-st="deep" aria-labelledby="d-h"><div class="gates">'
            f'<h2 class="big" id="d-h">{T(PG, "The build and the gates")}</h2>'
            f'<div class="g-grid">'
            f'<div class="g-cli"><h3>{T(PG, "Every command")}</h3><dl class="cli">{cli}</dl></div>'
            f'<div class="g-col"><h3>{T(PG, "Checks on the data")}</h3><p><code>gridflow quality</code> {T(PG, "runs")} {checks}'
            f'{T(PG, ", and writes each result to")} <code>quality_reports</code>.</p>'
            f'<h3>{T(PG, "Checks on the code")}</h3><p>{T(PG, "On every push and pull request:")} '
            + ", ".join(f"<code>{c}</code>" for c in code_ci) + '.</p>'
            f'<h3>{T(PG, "This site")}</h3><p><code>gridflow-build</code> {T(PG, "renders the vault notes into the dataset pages;")} '
            f'<code>--check</code> {T(PG, "proves the output unchanged on every pull request. Publishing adds htmlhint and a link check before GitHub Pages.")}</p></div>'
            f'<div class="g-col"><h3>{T(PG, "Not in gridflow")}</h3><ul class="nots">'
            + "".join(f"<li>{n}</li>" for n in nots) + '</ul></div>'
            f'</div></div></section>')
    body = "\n".join([sky, top, bronze, silver, gold, deep, footer(PG).replace(' data-st="deep"', ' data-st="foot"')])
    return body, CSS


CSS = """.lay{display:grid;grid-template-columns:600px 520px;column-gap:100px;align-items:start}
.st-top .lay{padding:78px 0 64px}
.st-bronze .lay,.st-silver .lay,.st-gold .lay{padding:78px 0 0}
.keys{list-style:none;margin:6px 0 0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:28px;border-top:1px solid rgba(28,43,34,.22)}
.keys li{font-family:"Red Hat Mono",monospace;font-size:16px;height:44px;line-height:44px;border-bottom:1px solid rgba(28,43,34,.22);color:#1C2B22}
.mini{margin:0 0 8px;font-size:14.5px;font-weight:600;color:#1C2B22}
.mini code{font-size:.92em}
.note{margin:0 0 20px;font-size:14.5px;line-height:1.55;color:#3F4A3B;max-width:58ch}
.fields{list-style:none;margin:0 0 14px;padding:0;columns:2;column-gap:28px;font:400 14.5px/1.9 "Red Hat Mono",monospace;color:#1C2B22}
.kfig{margin:34px 0 0;padding:0 0 70px}
.kpath{display:block;overflow:visible}
.kpath .kp{font-family:"Red Hat Mono",monospace;fill:#1C2B22}
.kpath .lit{fill:#3F4A3B}
.kpath .kl text{font-family:"Hanken Grotesk",sans-serif;font-style:italic;font-size:13.5px;fill:#1C2B22}
.steps{margin:0 0 0 22px;padding:0;font-size:16px;line-height:1.62;color:#3F4A3B;max-width:54ch}
.steps li{padding-left:4px}
.st-gold .lay{padding-bottom:84px}
.gpaths{margin:18px 0 0}
.gpaths div{padding:8px 0;border-top:1px solid rgba(28,43,34,.22)}
.gpaths div:last-child{border-bottom:1px solid rgba(28,43,34,.22)}
.gpaths dt{font-size:14px;font-style:italic;color:#3F4A3B}
.gpaths dd{margin:0;font-size:13.5px;overflow-wrap:anywhere}
.views{border-collapse:collapse;width:100%;margin:6px 0 16px}
.views caption{text-align:left;font-size:14.5px;font-weight:600;color:#1C2B22;padding:0 0 8px}
.views th,.views td{text-align:left;vertical-align:top;padding:9px 0;border-bottom:1px solid rgba(28,43,34,.22)}
.views tr:first-child th,.views tr:first-child td{border-top:1px solid rgba(28,43,34,.22)}
.views th{font-weight:400;padding-right:16px;white-space:nowrap}
.views th code{font-size:14px;color:#1C2B22}
.views td{font-size:14px;line-height:1.45;color:#3F4A3B}
.st-deep{color:#F6F4EC}
.gates{padding:96px 0 40px}
.gates h2{color:#F6F4EC}
.g-grid{display:grid;grid-template-columns:420px minmax(0,1fr) 330px;column-gap:64px;margin-top:10px;align-items:start}
.gates h3{font-size:20px;font-weight:700;font-stretch:90%;margin:0 0 10px;color:#F6F4EC}
.g-col h3+p{margin-top:0}
.g-col p{margin:0 0 24px;font-size:14.5px;line-height:1.6;color:#CFE0DC}
.st-deep .g-col p code,.st-deep .cli code{color:#F6F4EC;font-size:13.5px}
.cli{margin:0}
.cli div{display:grid;grid-template-columns:118px minmax(0,1fr);column-gap:14px;padding:7px 0;border-top:1px solid rgba(207,224,220,.22)}
.cli dd{margin:0;font-size:14.5px;line-height:1.45;color:#CFE0DC}
.nots{list-style:none;margin:0;padding:0}
.nots li{padding:8px 0;border-top:1px solid rgba(207,224,220,.22);font-size:14.5px;line-height:1.5;color:#CFE0DC}
"""


# ---------------------------------------------------------------- drawing
def draw(m: dict) -> tuple[str, int]:
    hp.Y["surf"] = 940
    secs = m["secs"]
    H = int(math.ceil(m["H"]))
    yb, ys, yg, yd = secs["bronze"][0], secs["silver"][0], secs["gold"][0], secs["deep"][0]
    surf = [(x, prof(x)) for x in range(-40, 1481, 10)]
    bg = strata_svg(H, S, surf, [("bronze", yb), ("silver", ys), ("gold", yg), ("deep", yd)], labels=False)
    aria = T(PG, "The same landscape as the home page: wind, solar, a gas-fired power station, pylons, a data centre, "
                 "battery storage, a substation, a met mast, an interconnector converter station and a gas terminal. "
                 "Four cables run down from the substation, the met mast, the converter station and the gas terminal "
                 "and join into one at the bronze contact.")
    land = (f'<svg class="layer land-svg" width="1440" height="{S + 16}" viewBox="0 0 1440 {S + 16}" role="img" '
            f'aria-label="{aria}"><g transform="translate(0 {DY})">{hp.landscape()}\n{hp.land_labels()}</g></svg>')
    # four feeds into the right margin, spliced into one at the bronze contact
    srcs = [890, 1018, 1124, 1314]
    c, ends = [], []
    c_tb = contact_y("bronze", yb, TRUNK)
    sp_y = c_tb
    for xs, xl in zip(srcs, LANE):
        pts = [(xs, prof(xs) - 3), (xs, S + 20)]
        for k in range(1, 14):
            tt = k / 14
            s2 = tt * tt * (3 - 2 * tt)
            pts.append((xs + (xl - xs) * s2, S + 20 + 110 * tt))
        pts.append((xl, S + 130))
        c.append(cable(smooth(pts) + f" V{f(sp_y - 10)}"))
    c_bs, c_sg = contact_y("silver", ys, TRUNK), contact_y("gold", yg, TRUNK)
    vl, vt, vr, vb = m["t"]["views"]
    end_y = vt + 11
    ex = 1318
    c.append(cable(f"M{TRUNK} {f(sp_y)} V{f(c_bs)}", BRONZE))
    c.append(cable(f"M{TRUNK} {f(c_bs)} V{f(c_sg)}", SILVER))
    c.append(cable(f"M{TRUNK} {f(c_sg)} V{f(end_y - 14)} Q{TRUNK} {f(end_y)} {TRUNK - 14} {f(end_y)} H{ex + 7}", GOLD))
    ends.append(f'<rect x="{LANE[0] - 12}" y="{f(sp_y - 14)}" width="{LANE[-1] - LANE[0] + 24}" height="28" rx="14" '
                f'fill="{BRONZE}" stroke="{INK}" stroke-width="1.6"></rect>'
                f'<path d="M{LANE[0] + 2} {f(sp_y - 14)} V{f(sp_y + 14)} M{LANE[-1] - 2} {f(sp_y - 14)} V{f(sp_y + 14)}" '
                f'stroke="{INK}" stroke-width="1" opacity=".5"></path>')
    ends.append(sleeve(TRUNK, c_bs, SILVER))
    ends.append(sleeve(TRUNK, c_sg, GOLD))
    ends.append(terminal(ex, end_y, T_GOLD))
    # the commands, written on the contacts they cross
    labs = [(sp_y, "gridflow ingest", T(PG, "into bronze")), (c_bs, "gridflow transform", T(PG, "bronze into silver")),
            (c_sg, "gridflow build", T(PG, "silver into gold"))]
    tx = []
    for y, verb, sub in labs:
        tx.append(f'<text x="1316" y="{f(y + 30)}" text-anchor="end" class="vb">{verb}</text>'
                  f'<text x="1316" y="{f(y + 49)}" text-anchor="end" class="vs">{sub}</text>')
    cab = (f'<svg class="layer" width="1440" height="{H}" viewBox="0 0 1440 {H}" aria-hidden="true">'
           + "".join(c) + "".join(ends) + f'<g class="verbs">{"".join(tx)}</g></svg>')
    return bg + "\n" + land + "\n" + cab, H


CSS += """.verbs .vb{font-family:"Red Hat Mono",monospace;font-weight:500;font-size:15px;fill:#1C2B22}
.verbs .vs{font-family:"Hanken Grotesk",sans-serif;font-style:italic;font-size:13.5px;fill:#1C2B22}
"""

_ = (DAY, OLIVE, SOFT, T_BRONZE, T_SILVER)
