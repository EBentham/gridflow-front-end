"""Render ARCH-PACK.md and pack.json from one content source, with copy checks."""

from __future__ import annotations

import json
import re
from pathlib import Path

OUT = Path(
    "C:/Users/Bobbo/OneDrive/Desktop/Python/gridflow-front-end/.planning/v5/design-loop/arch-pack"
)
GF_SHA = "2822d38952937ebb7ebad3d0f92abda644514408"
GM_SHA = "a17805b8466dc5d5bbf70073ff458693831ab9ba"
GF = "https://github.com/EBentham/gridflow"
GM = "https://github.com/EBentham/gridflow-models"


def gf(path: str, lines: str | None = None, tree: bool = False) -> dict[str, str]:
    kind = "tree" if tree else "blob"
    d = {"url": f"{GF}/{kind}/master/{path}", "file": path, "repo": "gridflow"}
    if lines:
        a, _, b = lines.partition("-")
        anchor = f"#L{a}" + (f"-L{b}" if b else "")
        d["permalink"] = f"{GF}/blob/{GF_SHA}/{path}{anchor}"
    return d


def gm(path: str, lines: str | None = None) -> dict[str, str]:
    d = {"url": f"{GM}/blob/main/{path}", "file": path, "repo": "gridflow-models"}
    if lines:
        a, _, b = lines.partition("-")
        anchor = f"#L{a}" + (f"-L{b}" if b else "")
        d["permalink"] = f"{GM}/blob/{GM_SHA}/{path}{anchor}"
    return d


# ---------------------------------------------------------------- 1. opening
OPENING = {
    "lede": (
        "Raw API responses land in bronze, cleaned and typed tables settle in silver, and "
        "cross-source joins and derived columns sit in gold; one embedded DuckDB file reads silver and gold."
    ),
    "lede_note": (
        "Changed from the old lede on purpose: 'live' is a banned word even as a verb, gold also holds a "
        "derived-column builder, and DuckDB registers views for silver and gold only, not bronze "
        "(storage/duckdb.py:161-209)."
    ),
    "scope": (
        "gridflow has no scheduler, no server, no cloud and no live feed: every run is a "
        "gridflow command someone starts, and vendor data arrives only when one runs."
    ),
    "evidence": [
        "pyproject.toml:7-21 (dependencies: httpx, tenacity, pydantic, polars, pyarrow, duckdb, lxml, "
        "typer and helpers; no web framework, server, cloud SDK or scheduler)",
        "pyproject.toml:33-34 (gridflow = gridflow.cli:app is the only entry point)",
        "src/gridflow/config/settings.py:60 (schedule field is parsed from sources.yaml; grep of src finds "
        "no reader of it)",
        "src/gridflow/storage/duckdb.py:54-72 (duckdb.connect on a local file path; no server)",
        "src/gridflow/cli.py:185-1209 (every stage is a Typer command)",
    ],
    "links": [gf("pyproject.toml", "7-34"), gf("src/gridflow/cli.py")],
}

# ---------------------------------------------------------------- 2. drawing
SOURCES = [
    ("elexon", "Elexon", "Elexon Insights API (BMRS)",
     "GB system prices, generation by fuel, demand, market index prices and REMIT notices.",
     "src/gridflow/connectors/elexon/client.py", "377", "config/sources.yaml:2-9"),
    ("entsoe", "ENTSO-E", "ENTSO-E Transparency Platform",
     "European day-ahead prices, load, generation, cross-border flows, outages and balancing.",
     "src/gridflow/connectors/entsoe/client.py", "585", "config/sources.yaml:188-195"),
    ("entsog", "ENTSO-G", "ENTSO-G Transparency Platform",
     "European gas flows, nominations, capacity, tariffs and gas quality.",
     "src/gridflow/connectors/entsog/client.py", "174", "config/sources.yaml:461-468"),
    ("neso", "NESO carbon intensity", "NESO Carbon Intensity API",
     "GB carbon intensity, national and regional, and the generation mix.",
     "src/gridflow/connectors/neso/carbon_intensity.py", "180", "config/sources.yaml:602-609"),
    ("neso_data_portal", "NESO Data Portal", "NESO Data Portal (CKAN API)",
     "Daily wind availability, historic generation mix, embedded wind and solar forecasts.",
     "src/gridflow/connectors/neso_data_portal/client.py", "1492", "config/sources.yaml:755-775"),
    ("gie_agsi", "GIE AGSI", "GIE AGSI+ gas storage",
     "European gas storage levels, plus storage unavailability and news.",
     "src/gridflow/connectors/gie/client.py", "443", "config/sources.yaml:411-446"),
    ("gie_alsi", "GIE ALSI", "GIE ALSI LNG",
     "European LNG terminal data at country level.",
     "src/gridflow/connectors/gie/client.py", "444", "config/sources.yaml:448-459"),
    ("open_meteo", "Open-Meteo", "Open-Meteo weather API",
     "Historical and forecast weather for demand, wind and solar: temperature, wind speed, radiation.",
     "src/gridflow/connectors/openmeteo/client.py", "152", "config/sources.yaml:146-187"),
]

source_parts = []
for reg, label, human, provides, cfile, reg_line, cfg in SOURCES:
    source_parts.append({
        "id": f"source-{reg}",
        "layer": "above ground",
        "registered_name": reg,
        "label": label,
        "human_name": human,
        "index": f"{reg}: {provides}",
        "links": [gf(cfile, reg_line)],
        "evidence": [cfg, f"{cfile}:{reg_line} (register_connector(\"{reg}\", ...))",
                     "src/gridflow/pipeline/runner.py:113-121 (_CONNECTOR_MODULES imports each connector module)"],
    })

BOUNDARY_PARTS = [
    {
        "id": "boundary-vendor-connector",
        "layer": "cable: vendor to connector",
        "label": "Async requests, capped and retried",
        "index": "One async httpx client per source; a semaphore caps requests in flight; tenacity retries with jittered backoff.",
        "links": [gf("src/gridflow/connectors/base.py", "110-146"), gf("src/gridflow/utils/retry.py", "19-54")],
        "evidence": [
            "src/gridflow/connectors/base.py:133-141 (asyncio.Semaphore(config.rate_limit_per_second) and httpx.AsyncClient in __aenter__)",
            "config/sources.yaml:757-759 (the code's own note: the semaphore is a concurrency cap despite its name)",
            "src/gridflow/utils/retry.py:19-54 (RETRY_POLICY: 5 attempts, wait_random_exponential, retry on TimeoutException, NetworkError, HTTPStatusError)",
            "src/gridflow/connectors/elexon/client.py:346-357 (@RETRY_POLICY on _request; async with self._semaphore; raise_for_status)",
        ],
    },
    {
        "id": "boundary-connector-bronze",
        "layer": "cable: connector to bronze",
        "label": "Raw bytes plus a sidecar",
        "index": "Each response is stored byte for byte with a .meta.json sidecar; both land by temp file and atomic rename.",
        "links": [gf("src/gridflow/bronze/writer.py", "28-119")],
        "evidence": [
            "src/gridflow/bronze/writer.py:33-34 (sha256 of body, first 8 hex chars; extension from content type)",
            "src/gridflow/bronze/writer.py:37-47 (partition by data_date when known, else fetch date: {source}/{dataset}/{YYYY}/{MM}/{DD})",
            "src/gridflow/bronze/writer.py:57 (raw_{fetched_at:%Y%m%dT%H%M%SZ}_{hash8}.{ext})",
            "src/gridflow/bronze/writer.py:67-86 (sidecar fields)",
            "src/gridflow/bronze/writer.py:94-105 (temp file then os.replace)",
            "src/gridflow/bronze/writer.py:108-119 (json, xml, csv, else bin)",
        ],
    },
    {
        "id": "stratum-bronze",
        "layer": "stratum",
        "label": "Bronze: raw responses by date",
        "index": "bronze/{source}/{dataset}/{YYYY}/{MM}/{DD}/raw_{fetched_at}_{hash8}.json, one file per response page.",
        "links": [gf("src/gridflow/bronze/writer.py", "37-57")],
        "evidence": ["src/gridflow/bronze/writer.py:37-57", "src/gridflow/storage/paths.py:26-38"],
    },
    {
        "id": "boundary-bronze-silver",
        "layer": "cable: bronze to silver",
        "label": "Typed transformers stamp every row",
        "index": "One Polars transformer per dataset: strict types, UTC, Pydantic checks counted not raised, then available_at, source_run_id, dataset_version.",
        "links": [gf("src/gridflow/silver/base.py", "936-1000"), gf("src/gridflow/silver/elexon/system_prices.py")],
        "evidence": [
            "src/gridflow/silver/base.py:403 (BaseSilverTransformer)",
            "src/gridflow/silver/base.py:1574-1680 (_process_frame: transform, validate, _add_bitemporal_columns at 1671)",
            "src/gridflow/silver/base.py:2021-2082 (_validate_against_schema: never raises, never drops a row, returns a failure count)",
            "src/gridflow/silver/base.py:2135-2156 (available_at = coalesce(published_at, ingest stamp), row by row)",
            "src/gridflow/silver/base.py:2180-2182, 2196-2199 (source_run_id, dataset_version)",
            "src/gridflow/pipeline/runner.py:1142, 1197-1199 (transform run id passed as run_id)",
        ],
    },
    {
        "id": "stratum-silver",
        "layer": "stratum",
        "label": "Silver: typed Parquet, Hive-partitioned",
        "index": "silver/{source}/{dataset}/year=YYYY/month=MM/; append-only datasets keep one file per capture, suffixed _run{capture time}.",
        "links": [gf("src/gridflow/storage/paths.py", "50-80"), gf("src/gridflow/silver/base.py", "2610-2637")],
        "evidence": [
            "src/gridflow/storage/paths.py:50-80 (year=/month= partition dir; {dataset}_{YYYYMMDD}.parquet)",
            "src/gridflow/silver/base.py:2618-2636 (APPEND_ONLY writes {dataset}_{YYYYMMDD}_run{stamp}.parquet; others overwrite one file per date)",
            "src/gridflow/storage/parquet.py:35-54 (temp file, then os.replace)",
        ],
    },
    {
        "id": "boundary-silver-views",
        "layer": "cable: silver to views",
        "label": "DuckDB views over Parquet",
        "index": "One view per dataset over read_parquet with Hive partitioning; append-only datasets also get a _latest view.",
        "links": [gf("src/gridflow/storage/duckdb.py", "161-209"), gf("src/gridflow/silver/latest_views.py", "94-134")],
        "evidence": [
            "src/gridflow/storage/duckdb.py:179 (silver_{source}_{dataset})",
            "src/gridflow/storage/duckdb.py:183-199 (_latest view built from LATEST_VIEW_SPECS, or dropped if it cannot be built)",
            "src/gridflow/storage/duckdb.py:434-447 (CREATE OR REPLACE VIEW ... read_parquet(..., hive_partitioning=true, union_by_name=true); plain views, not materialised)",
            "src/gridflow/cli.py:293, 335 (transform and build refresh the views when they finish)",
        ],
    },
    {
        "id": "catalogue",
        "layer": "stratum",
        "label": "One file: gridflow.duckdb",
        "index": "Views over the Parquet, plus the pipeline_runs, pipeline_watermarks and quality_reports tables. No server.",
        "links": [gf("src/gridflow/storage/duckdb.py", "92-158")],
        "evidence": [
            "src/gridflow/storage/duckdb.py:92-158 (init_catalogue: three tables, then views)",
            "src/gridflow/config/settings.py:97-99 (default data/gridflow.duckdb, configurable)",
        ],
    },
    {
        "id": "stratum-gold",
        "layer": "stratum",
        "label": "Gold: a builder and SQL views",
        "index": "Polars builder system_marginal_price; SQL views gold_uk_imbalance_context, gold_gb_day_ahead_benchmark, gold_eu_gas_storage.",
        "links": [gf("src/gridflow/gold/system_marginal_price.py", "24-71"), gf("src/gridflow/gold/views", tree=True)],
        "evidence": [
            "src/gridflow/gold/system_marginal_price.py:71 (register_builder, the one registered builder)",
            "src/gridflow/gold/views/uk_imbalance_context.sql:14-31 (latest system prices joined to NESO carbon intensity)",
            "src/gridflow/gold/views/gb_day_ahead_benchmark.sql:13-33 (Elexon MID APXMIDP)",
            "src/gridflow/gold/views/eu_gas_storage.sql:4-18 (GIE AGSI storage)",
            "src/gridflow/storage/duckdb.py:465-492 (SQL files executed at catalogue registration)",
            "src/gridflow/gold/base.py:23 (gold is rebuilt from silver, not incrementally updated)",
        ],
        "note": ("Not copy: gridflow_models also writes its outputs (forecasts, metrics, stack results) under the same "
                 "gold/ folder (gridflow_models src/gridflow_models/forecast_store/writer.py:220), and gridflow's catalogue "
                 "registers every gold folder as a gold_* view (src/gridflow/storage/duckdb.py:203-209). If the drawing "
                 "shows gridflow_models output in gold, it is a gridflow_models write, not a gridflow build."),
    },
]

CLI_VERBS = ["init", "ingest", "transform", "build", "pipeline", "backfill", "export-csv",
             "status", "quality", "reset", "prune"]
CLIENT_METHODS = ["query", "get_system_prices", "get_gb_day_ahead_benchmark", "get_generation_by_fuel",
                  "get_fuel_generation", "get_gas_storage", "get_imbalance_context", "get_tables"]

READER_PARTS = [
    {
        "id": "reader-cli",
        "layer": "readers",
        "label": "The gridflow command",
        "index": "init, ingest, transform, build, pipeline, backfill, export-csv, status, quality, reset, prune.",
        "verbs": CLI_VERBS,
        "links": [gf("src/gridflow/cli.py", "185-1233")],
        "evidence": [
            "src/gridflow/cli.py:185 ingest, 260 transform, 305 build, 345 backfill, 437 export-csv, 484 pipeline, "
            "583 status, 676 quality, 795 reset, 971 prune, 1208 init (@app.command)",
            "gridflow --help, run 2026-09-27, lists exactly these eleven commands (RUN-LOG.md)",
        ],
    },
    {
        "id": "reader-client",
        "layer": "readers",
        "label": "GridflowClient, read-only, returns Polars",
        "index": "from gridflow.serving.client import GridflowClient: query, get_system_prices, get_imbalance_context, get_gas_storage and more.",
        "methods": CLIENT_METHODS,
        "links": [gf("src/gridflow/serving/client.py", "61-405")],
        "evidence": [
            "src/gridflow/serving/client.py:75-89 (duckdb.connect(..., read_only=True))",
            "src/gridflow/serving/client.py:102-104 (query returns .pl(), a Polars DataFrame)",
            "src/gridflow/serving/client.py:152, 192, 219, 251, 270, 327, 363 (get_* methods)",
            "src/gridflow/serving/client.py:401-405 (context manager)",
            "src/gridflow/__init__.py is empty: import from gridflow.serving.client",
        ],
    },
    {
        "id": "reader-notebooks",
        "layer": "readers",
        "label": "Notebooks",
        "index": "Any notebook can open a GridflowClient; the gridflow_models workbench notebooks do, through their setup helper.",
        "links": [gm("src/gridflow_models/research/notebook_setup.py", "425-441")],
        "evidence": [
            "gridflow_models src/gridflow_models/research/notebook_setup.py:435 (GridflowClient(db_path=...))",
            "gridflow_models src/gridflow_models/research/_pandas_client.py:1-6 (the workbench wraps it and hands pandas to the notebook)",
            "gridflow repo has no notebooks/ folder",
        ],
    },
    {
        "id": "reader-gridflow-models",
        "layer": "readers",
        "label": "gridflow_models, reading as of a time",
        "index": "Training and backtests read silver Parquet directly, keeping only rows whose available_at is at or before the as-of time.",
        "links": [gm("src/gridflow_models/data/gridflow_source.py", "320-366"), {"url": "models.html", "file": "site page", "repo": "site"}],
        "site_link": "models.html",
        "evidence": [
            "gridflow_models src/gridflow_models/data/gridflow_source.py:45-46 (GridflowDataSource reads gridflow silver files without importing gridflow modules)",
            "gridflow_models src/gridflow_models/data/gridflow_source.py:340-366 (WHERE available_at <= ?; optional QUALIFY ROW_NUMBER() ... ORDER BY available_at DESC)",
            "gridflow_models src/gridflow_models/data/gridflow_source.py:96-105 (fetch(dataset, event_time_start, event_time_end, as_of, latest_only, ...))",
            "gridflow_models pyproject.toml:32, 101 (gridflow is a local path dependency)",
            "gridflow src/gridflow/serving/client.py:161-172 (point-in-time selection is consumer-side, in gridflow_models)",
        ],
    },
]

# ---------------------------------------------------------------- 3. journey
STOPS = [
    {
        "id": "stop-1-cli",
        "heading": "One command starts the run",
        "body": ("Nothing runs on a timer. Someone runs ingest to fetch a day from Elexon into bronze, "
                 "then transform to turn that bronze into silver. Both take a source, a dataset and a date range."),
        "snippets": ["snippets/01-cli.sh"],
        "links": [gf("src/gridflow/cli.py", "185-303")],
        "evidence": [
            "src/gridflow/cli.py:185-258 (ingest source dataset --start --end --last --all --incremental)",
            "src/gridflow/cli.py:260-303 (transform; refreshes views at 293)",
            "src/gridflow/pipeline/runner.py:479-501 (a bare date is midnight UTC), 1134-1138 (inclusive date range)",
            "src/gridflow/connectors/elexon/client.py:360-374 (_date_range inclusive)",
        ],
    },
    {
        "id": "stop-2-connector",
        "heading": "The connector calls Elexon",
        "body": ("The Elexon connector puts the settlement date in the URL path and follows the pages. "
                 "A per-source semaphore caps requests in flight, and tenacity retries timeouts, network "
                 "errors and HTTP errors with jittered backoff."),
        "snippets": ["snippets/02-connector-request.txt", "snippets/02-connector-request.py"],
        "links": [gf("src/gridflow/connectors/elexon/client.py", "246-284"), gf("src/gridflow/connectors/elexon/endpoints.py", "58-62")],
        "evidence": [
            "src/gridflow/connectors/elexon/endpoints.py:58-62 (system_prices: /balancing/settlement/system-prices, DATE_PATH)",
            "config/sources.yaml:3 (base_url https://data.elexon.co.uk/bmrs/api/v1)",
            "src/gridflow/connectors/elexon/client.py:255 (path = f\"{endpoint.path}/{settlement_date.isoformat()}\")",
            "src/gridflow/connectors/elexon/client.py:257-282 (page loop until total_pages)",
            "the real request_url in both bronze sidecars for 2026-09-08",
        ],
    },
    {
        "id": "stop-3-bronze",
        "heading": "Bronze keeps the raw bytes",
        "body": ("The response is saved byte for byte, in a folder for the date it describes, beside a "
                 ".meta.json sidecar recording the request, status and body hash. Fetching the same day "
                 "again adds a second file next to the first."),
        "snippets": ["snippets/03-bronze-files.txt", "snippets/03-bronze-body-excerpt.json", "snippets/03-bronze-sidecar.json"],
        "snippet_note": "Body excerpt shows 8 of the record's 22 fields and 1 of its records; every value shown is real.",
        "links": [gf("src/gridflow/bronze/writer.py", "28-105")],
        "evidence": [
            "src/gridflow/bronze/writer.py:33-57 (hash, timestamp, date partition, filename)",
            "src/gridflow/bronze/writer.py:67-86 (sidecar)",
            "src/gridflow/bronze/writer.py:61-63 (written_at marks the durable write)",
        ],
    },
    {
        "id": "stop-4-silver",
        "heading": "Silver keeps every version",
        "body": ("Each bronze capture becomes its own typed Parquet file, named for when it was captured, and "
                 "both prices are kept. Every row is checked against a Pydantic schema and stamped with "
                 "available_at (Elexon's publication time), source_run_id and dataset_version."),
        "snippets": ["snippets/04-silver-files.txt", "snippets/04-silver-vintages.sql"],
        "snippet_note": ("File suffix = the bronze capture's written_at. Row available_at = Elexon's createdDateTime. "
                         "They are different instants; do not conflate them. source_run_id is the pipeline_runs.run_id "
                         "of the transform that wrote the row. dataset_version is the transformer's output version, not a gridflow version."),
        "links": [gf("src/gridflow/silver/elexon/system_prices.py", "39-71"), gf("src/gridflow/silver/base.py", "2084-2200")],
        "evidence": [
            "src/gridflow/silver/elexon/system_prices.py:65-66 (APPEND_ONLY, VINTAGE_PER_BRONZE_FILE)",
            "src/gridflow/silver/elexon/system_prices.py:129 (createdDateTime becomes published_at)",
            "src/gridflow/silver/elexon/system_prices.py:199-220 (casts; UTC timestamp from date and period)",
            "src/gridflow/silver/base.py:1364-1474 (one silver file per bronze body; stamp from the sidecar)",
            "src/gridflow/silver/base.py:2633-2636 (filename {dataset}_{YYYYMMDD}_run{stamp}.parquet)",
            "src/gridflow/silver/base.py:2155 (available_at = coalesce(published_at, ingest stamp))",
            "src/gridflow/silver/base.py:2021-2082 (Pydantic check, fail-soft, counted)",
        ],
    },
    {
        "id": "stop-5-latest",
        "highlight": True,
        "heading": "The latest view picks a winner",
        "body": ("silver_elexon_system_prices_latest keeps one row per settlement period: the latest "
                 "available_at wins, ties go to the later settlement run. The base view keeps both, so a "
                 "backtest can ask what was known at any moment: here, 9.56 until the revision."),
        "mechanism": ("When a vendor gives no publication time, a dated per-dataset rule estimates when each "
                      "value could first have been known, for history before a set cutover. On datasets that "
                      "declare one, each row records which applied: vendor, the rule's name, or ingest-clock."),
        "snippets": ["snippets/05-latest-view-ddl.sql", "snippets/05-latest-view.sql", "snippets/05-as-of.sql"],
        "snippet_note": ("05-as-of.sql is the as-of read gridflow_models applies (available_at at or before the as-of time, "
                         "then the latest survivor); gridflow's own _latest view is the current best value, not an as-of read. "
                         "This row's vintage_policy is vendor: Elexon supplied the time, so the lag rule did not apply. "
                         "Never print the rule's lag figure or cutover date."),
        "links": [gf("src/gridflow/silver/latest_views.py", "82-134"), gf("src/gridflow/silver/base.py", "36-67")],
        "evidence": [
            "src/gridflow/silver/latest_views.py:84-99 (II..DF rank; system_prices key settlement_date, settlement_period; rank on run_type)",
            "src/gridflow/silver/latest_views.py:260-269 (ORDER BY available_at DESC NULLS LAST, then rank DESC; ROW_NUMBER() = 1)",
            "src/gridflow/silver/latest_views.py:32-39 (available_at leads because the live feed has no run label)",
            "src/gridflow/storage/duckdb.py:183-199 (view registered from LATEST_VIEW_SPECS)",
            "src/gridflow/silver/base.py:36-67 (VintagePolicy: name, lag, dated, rule, applies_before)",
            "src/gridflow/silver/base.py:2159-2193 (policy replaces only the fallback, before the cutover; labels vendor / policy name / ingest-clock)",
            "src/gridflow/silver/elexon/system_prices.py:48-62 (system_prices declares a policy; its rule text calls itself an assumption)",
            "src/gridflow/serving/client.py:161-172 (as-of selection is consumer-side)",
            "gridflow_models src/gridflow_models/data/gridflow_source.py:340-366 (available_at <= as_of, latest survivor)",
        ],
    },
    {
        "id": "stop-6-gold",
        "heading": "Gold adds derived columns",
        "body": ("The system_marginal_price builder reads the latest version of each period and adds spread "
                 "(buy minus sell), absolute imbalance, hour of day and ISO day of week. Buy and sell are "
                 "equal in this period, so spread is 0.0."),
        "snippets": ["snippets/06-gold-build.sh", "snippets/06-gold-spread.py", "snippets/06-gold-build.py"],
        "snippet_note": ("The row was produced by the builder's build() method, which returns the frame; "
                         "gridflow build calls run(), which also writes gold/system_marginal_price/year=2026/"
                         "system_marginal_price_20260908.parquet. hour_of_day is the UTC hour."),
        "links": [gf("src/gridflow/gold/system_marginal_price.py", "29-68")],
        "evidence": [
            "src/gridflow/gold/system_marginal_price.py:36-40 (scan silver, select_latest_vintage)",
            "src/gridflow/gold/system_marginal_price.py:48 (system_buy_price - system_sell_price AS spread)",
            "src/gridflow/gold/system_marginal_price.py:50, 63-64 (abs_imbalance, hour_of_day, day_of_week ISO)",
            "src/gridflow/gold/base.py:40-68 (run writes gold/{name}/year=YYYY/{name}_{YYYYMMDD}.parquet)",
        ],
    },
    {
        "id": "stop-7-client",
        "heading": "Read it into Polars",
        "body": ("GridflowClient opens the DuckDB file read-only and returns Polars DataFrames. "
                 "get_system_prices reads the _latest view, so each settlement period comes back once, "
                 "with available_at kept so you know which version you hold."),
        "snippets": ["snippets/07-client.py"],
        "links": [gf("src/gridflow/serving/client.py", "152-190")],
        "evidence": [
            "src/gridflow/serving/client.py:53 (_REL_SYSTEM_PRICES = silver_elexon_system_prices_latest)",
            "src/gridflow/serving/client.py:44 (available_at and vintage_policy retained)",
            "src/gridflow/serving/client.py:182-190 (SELECT ... WHERE settlement_date BETWEEN ? AND ?, .pl())",
            "src/gridflow/serving/client.py:87-89 (read_only=True)",
        ],
    },
]

# ---------------------------------------------------------------- 4. correctness
RULES = [
    {
        "rule": "Raw responses are kept, so any silver table can be rebuilt without calling the vendor again.",
        "links": [gf("src/gridflow/bronze/writer.py", "57-63")],
        "evidence": ["src/gridflow/bronze/writer.py:57-63", "src/gridflow/silver/base.py:837-846 (transformers read bronze)",
                     "src/gridflow/cli.py:268-272 (transform --reingest rebuilds with sidecar timestamps)"],
        "caveat": "True while bronze exists: gridflow reset and prune delete bronze on request (cli.py:795, 971).",
    },
    {
        "rule": "Re-runs are safe: every file lands by temp file and atomic rename, never half-written.",
        "links": [gf("src/gridflow/storage/parquet.py", "35-54")],
        "evidence": ["src/gridflow/bronze/writer.py:94-105", "src/gridflow/storage/parquet.py:35-54"],
        "caveat": ("Do not claim re-runs rewrite the same files. Re-ingesting adds a new bronze file (the name carries "
                   "fetch time). Append-only silver datasets can gain a new version file on a plain re-transform, because "
                   "the stamp is the transform time unless --reingest or the per-capture path supplies the sidecar time "
                   "(silver/base.py:1181-1183, 2618-2625). Non-append-only datasets overwrite one file per date."),
    },
    {
        "rule": "Rows that fail validation are still written, counted, and the run is marked completed with warnings.",
        "links": [gf("src/gridflow/silver/base.py", "2021-2082")],
        "evidence": ["src/gridflow/silver/base.py:2021-2035", "src/gridflow/pipeline/runner.py:1232, 1423",
                     "src/gridflow/observability.py:151-160 (status completed_with_warnings)"],
        "caveat": "Extra fields pass the Pydantic check (schemas/common.py:13, extra=\"ignore\"). Do not say drift fails loudly or raises.",
    },
    {
        "rule": "Each row gridflow writes carries available_at: vendor publication time if given, else a dated estimate or gridflow's clock.",
        "links": [gf("src/gridflow/silver/base.py", "2084-2200")],
        "evidence": ["src/gridflow/silver/base.py:2135-2156", "src/gridflow/silver/base.py:2159-2193",
                     "src/gridflow/silver/base.py:1181-1183 (fallback is the transform time, or the sidecar time with --reingest)"],
    },
    {
        "rule": "One embedded DuckDB file is the catalogue; GridflowClient opens it read-only, and there is no server.",
        "links": [gf("src/gridflow/storage/duckdb.py", "54-72")],
        "evidence": ["src/gridflow/storage/duckdb.py:54-72", "src/gridflow/serving/client.py:87-89"],
    },
]
RUN_TRACKING = {
    "text": ("Every ingest, transform and build writes a row to pipeline_runs with its status, row counts "
             "and any error, and each silver row's source_run_id points back to it. Incremental ingest "
             "resumes from pipeline_watermarks. gridflow quality runs row-count, null-rate, gap and "
             "duplicate checks and writes them to quality_reports."),
    "snippets": ["snippets/08-run-tracking.sql"],
    "links": [gf("src/gridflow/observability.py", "63-221"), gf("src/gridflow/quality/checks.py")],
    "evidence": [
        "src/gridflow/pipeline/runner.py:937, 1142, 1567 (PipelineRunTracker for ingest, transform, build)",
        "src/gridflow/observability.py:63-221 (running, success, completed_with_warnings, failed)",
        "src/gridflow/observability.py:236-300 (monotonic watermark upsert)",
        "src/gridflow/cli.py:195-206 (ingest --incremental resumes from the watermark)",
        "src/gridflow/cli.py:676-792 (quality runs check_row_count, check_null_rate, check_time_series_gaps, check_duplicates)",
        "src/gridflow/quality/reporter.py:47-123 (writes quality_reports)",
        "src/gridflow/storage/duckdb.py:106-145 (the three tables)",
    ],
    "caveat": "checks.py also defines check_range (line 120), but the quality verb does not run it. Name the four it runs.",
}
CI = {
    "text": ("On every push and pull request, gridflow's CI checks the lockfile, runs ruff lint and format "
             "checks, mypy over src/gridflow, and pytest with live-API tests excluded."),
    "links": [gf(".github/workflows/ci.yml", "1-42")],
    "evidence": [".github/workflows/ci.yml:2 (on: [push, pull_request])", ".github/workflows/ci.yml:19 (uv lock --check)",
                 ".github/workflows/ci.yml:28, 31 (ruff check, ruff format --check)", ".github/workflows/ci.yml:39 (mypy src/gridflow/)",
                 ".github/workflows/ci.yml:42 (pytest tests/ -m \"not live\")"],
    "caveat": "CI does not run the pipeline against real data. Do not say it runs identically in CI.",
}

# ---------------------------------------------------------------- 5. where to look
WHERE = [
    ("which sources and endpoints are configured", [gf("config/sources.yaml")]),
    ("how a connector requests, limits and retries", [gf("src/gridflow/connectors/base.py"), gf("src/gridflow/utils/retry.py")]),
    ("how raw responses are stored", [gf("src/gridflow/bronze/writer.py")]),
    ("how bronze becomes silver: validation, timestamps, file names", [gf("src/gridflow/silver/base.py")]),
    ("a complete transformer, Elexon system prices", [gf("src/gridflow/silver/elexon/system_prices.py")]),
    ("how the latest version is chosen", [gf("src/gridflow/silver/latest_views.py")]),
    ("the catalogue, its views and run tables", [gf("src/gridflow/storage/duckdb.py")]),
    ("gold builders and SQL views", [gf("src/gridflow/gold/system_marginal_price.py"), gf("src/gridflow/gold/views", tree=True)]),
    ("reading data into Polars", [gf("src/gridflow/serving/client.py")]),
    ("every command", [gf("src/gridflow/cli.py")]),
    ("run tracking and quality checks", [gf("src/gridflow/observability.py"), gf("src/gridflow/quality/checks.py")]),
    ("what CI runs", [gf(".github/workflows/ci.yml")]),
    ("how gridflow_models reads gridflow as of a time", [gm("src/gridflow_models/data/gridflow_source.py")]),
]

CUT = [
    ("Bronze stored as Parquet, a 'Raw Parquet Lake', or Hive/as_of= folders in bronze",
     "bronze is raw bytes (.json/.xml/.csv/.bin) plus .meta.json in {source}/{dataset}/YYYY/MM/DD (bronze/writer.py:37-57, 108-119)"),
    ("Pydantic-validated bronze", "nothing is validated at bronze; validation is a silver step (silver/base.py:2021)"),
    ("The SHA-256 filename makes re-fetching a no-op", "the name also carries fetch time; a re-fetch writes a new file (bronze/writer.py:57)"),
    ("@register_connector decorator; 'no central wiring file'",
     "a plain register_connector(source, cls) call, and runner.py:113-121 lists the modules"),
    ("A rate limit of N requests per second", "the semaphore caps requests in flight (sources.yaml:757-759)"),
    ("Point-in-time or as-of reads in gridflow's gold or _latest views",
     "_latest is the current best value; as-of reads are consumer-side (serving/client.py:161-172)"),
    ("Materialised views", "plain CREATE OR REPLACE VIEW over read_parquet (storage/duckdb.py:445-447)"),
    ("A query or run verb", "verbs are init, ingest, transform, build, pipeline, backfill, export-csv, status, quality, reset, prune"),
    ("MLflow, PuLP dispatch", "neither is used (MeritOrderDispatchLP.solve raises NotImplementedError in gridflow_models)"),
    ("'Nothing is ever deleted', 'bronze is forever'", "reset and prune delete on request (cli.py:795, 971)"),
    ("system_prices_20260429.parquet, 'one Parquet per dataset per date' for system_prices, 'deduplicated by primary key'",
     "append-only datasets keep one file per capture: {dataset}_{YYYYMMDD}_run{stamp}.parquet"),
    ("A run-type precedence resolver inside the transformer (RUN_PRECEDENCE, _resolve_runs)",
     "the transformer keeps every version; the II..DF rank is only the tie-break in the _latest view"),
    ("Weather-adjusted demand; gold/demand_features.py; gold/merit_order.py", "not in gridflow; the only builder is system_marginal_price"),
    ("A documented derivation for every gold column", "no such record exists"),
    ("silver_system_prices as the view name; a run_type = 'DF' filter",
     "canonical names are silver_elexon_system_prices and silver_elexon_system_prices_latest; live rows have null run_type"),
    ("from gridflow import GridflowClient", "gridflow/__init__.py is empty; use from gridflow.serving.client import GridflowClient"),
    ("spread = sell minus buy", "gridflow defines spread = buy minus sell (gold/system_marginal_price.py:48)"),
    ("pandas, DuckDB WASM or Tableau as ways to query", "unverified and off-brand; drop"),
    ("'Schema drift fails loudly', 'raises ValidationError', 'every silver dataset has a Pydantic model'",
     "validation is fail-soft and counted; some transformers set schema_cls = None (silver/base.py:419, silver/gie/agsi.py:301)"),
    ("'Runs identically in CI', 'same files, same results'", "CI runs lock check, ruff, mypy and pytest without live tests"),
    ("'Every gold value is one SQL query from the raw bytes'", "silver carries source_run_id, not a bronze file reference"),
    ("Counts of sources, connectors, datasets, transformers or views", "counts change; name things instead"),
    ("gridflow_models reads everything through GridflowClient",
     "training and backtests read silver Parquet directly with an as-of filter; only the notebook workbench uses GridflowClient"),
    ("get_weather returns weather", "it returns Elexon ITSDO demand outturn; the name is a documented misnomer (serving/client.py:302-306); leave it off"),
    ("The quality verb runs five checks", "it runs four; check_range exists but is not wired into the verb"),
    ("The system_prices lag figure or cutover date", "the code labels them an assumption; describe the mechanism only"),
    ("A gridflow version number, or MIT for gridflow", "gridflow is Apache-2.0 and its version is not safe to print"),
    ("Scheduled, hourly or real-time runs", "the schedule key in sources.yaml is parsed but used by nothing; every run is a command"),
    ("Spread as a signal for this row", "buy equals sell in the example period, so spread is 0.0; do not caption a cause"),
    ("'Nothing skips a layer'", "GridflowClient reads silver views directly; the claim adds nothing"),
]

UNVERIFIED = [
    "GitHub links: built from the local remotes (gridflow master at 2822d38, gridflow-models main at a17805b). Not opened online, so whether they resolve publicly was not checked.",
    "Why Elexon published a different price for 2026-09-08 period 37 on 2026-09-09: not in the repo. Do not caption a cause.",
    "Why buy and sell prices are equal in the example period: a market-rule explanation is not in the repo. Show the value, not a reason.",
    "The system_prices publication-lag rule: the code itself marks its lag and cutover as an assumption with a TODO (system_prices.py:48-62).",
    "01-cli.sh and 06-gold-build.sh were not executed (they write). Their options were checked with --help, and 06's result was produced by build() in memory.",
    "Re-running 01-cli.sh today may fetch different bytes than the two captures shown, if Elexon has published again.",
    "SQL output shows UTC because the check session set TimeZone = 'UTC'; a DuckDB shell shows the machine's timezone.",
]


# ---------------------------------------------------------------- checks
BANNED = ["\u2014", "\u2013", "\u2192", "\u00b7", "->"]
PLANNING = re.compile(r"\b(planned|shipped|trained|live|in service|coming soon)\b", re.I)
LOCAL = re.compile(r"\b(locally|local data|on this machine|held locally|C:)\b", re.I)


def words(s: str) -> int:
    return len(s.split())


problems: list[str] = []


def check(text: str, where: str, limit: int | None = None, allow_live: bool = False) -> None:
    for b in BANNED:
        if b in text:
            problems.append(f"{where}: banned '{b}'")
    m = PLANNING.search(text)
    if m and not (allow_live and m.group(0).lower() == "live"):
        problems.append(f"{where}: planning word '{m.group(0)}'")
    if LOCAL.search(text):
        problems.append(f"{where}: local-data reference")
    if limit is not None and words(text) > limit:
        problems.append(f"{where}: {words(text)} words > {limit}")


check(OPENING["lede"], "lede")
check(OPENING["scope"], "scope", allow_live=True)
for p in source_parts + BOUNDARY_PARTS + READER_PARTS:
    check(p["label"], p["id"] + ".label", 6)
    check(p["index"], p["id"] + ".index", 20)
for s in STOPS:
    check(s["heading"], s["id"] + ".heading", 6)
    check(s["body"], s["id"] + ".body", 45)
    if "mechanism" in s:
        check(s["mechanism"], s["id"] + ".mechanism", 45)
for i, r in enumerate(RULES):
    check(r["rule"], f"rule{i + 1}", 18)
check(RUN_TRACKING["text"], "run_tracking")
check(CI["text"], "ci", allow_live=True)
for x, _ in WHERE:
    check(x, "where:" + x)
for snip in (OUT / "snippets").iterdir():
    for b in BANNED[:4]:
        if b in snip.read_text(encoding="utf-8"):
            problems.append(f"{snip.name}: banned '{b}'")

if problems:
    raise SystemExit("\n".join(problems))

# ---------------------------------------------------------------- render
pack = {
    "meta": {
        "built": "2026-09-27",
        "model": "claude-opus-5-5",
        "gridflow": {"repo": GF, "default_branch": "master", "commit": GF_SHA},
        "gridflow_models": {"repo": GM, "default_branch": "main", "commit": GM_SHA},
        "limits": {"label_words": 6, "index_words": 20, "stop_heading_words": 6, "stop_body_words": 45, "rule_words": 18},
        "example": {"dataset": "elexon/system_prices", "settlement_date": "2026-09-08", "settlement_period": 37,
                    "vintages": [{"price": 9.56, "available_at": "2026-09-08T17:48:45Z"},
                                 {"price": 110.0, "available_at": "2026-09-09T17:44:29Z"}]},
    },
    "sections": [
        {"id": "opening", **OPENING},
        {"id": "drawing", "parts": source_parts + BOUNDARY_PARTS + READER_PARTS},
        {"id": "journey", "stops": STOPS},
        {"id": "correctness", "rules": RULES, "run_tracking": RUN_TRACKING, "ci": CI},
        {"id": "where_to_look", "entries": [{"for": x, "links": links} for x, links in WHERE]},
    ],
    "cut": [{"do_not_say": a, "because": b} for a, b in CUT],
    "unverified": UNVERIFIED,
}
(OUT / "pack.json").write_text(json.dumps(pack, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def md_links(links: list[dict[str, str]]) -> str:
    out = []
    for link in links:
        if link["repo"] == "site":
            out.append(f"[Models page]({link['url']})")
        else:
            out.append(f"[`{link['file']}`]({link['url']})")
    return ", ".join(out)


def snippet_block(rel: str) -> str:
    p = OUT / rel
    lang = {".sh": "bash", ".py": "python", ".sql": "sql", ".json": "json", ".txt": "text"}[p.suffix]
    return f"`{rel}`\n\n```{lang}\n{p.read_text(encoding='utf-8').rstrip()}\n```\n"


RESULTS = {
    "snippets/04-silver-vintages.sql": (
        "settlement_date  settlement_period  system_sell_price  system_buy_price  available_at             vintage_policy  source_run_id                         dataset_version\n"
        "2026-09-08       37                 9.56               9.56              2026-09-08 17:48:45 UTC  vendor          494e780a-a127-4fa8-b371-25caf146c094  2.0.0\n"
        "2026-09-08       37                 110.0              110.0             2026-09-09 17:44:29 UTC  vendor          494e780a-a127-4fa8-b371-25caf146c094  2.0.0"
    ),
    "snippets/05-latest-view.sql": (
        "settlement_date  settlement_period  system_sell_price  system_buy_price  available_at\n"
        "2026-09-08       37                 110.0              110.0             2026-09-09 17:44:29 UTC"
    ),
    "snippets/05-as-of.sql": (
        "settlement_date  settlement_period  system_sell_price  available_at\n"
        "2026-09-08       37                 9.56               2026-09-08 17:48:45 UTC"
    ),
    "snippets/06-gold-build.py": (
        "settlement_date  settlement_period  system_buy_price  system_sell_price  spread  abs_imbalance  hour_of_day  day_of_week\n"
        "2026-09-08       37                 110.0             110.0              0.0     346.717783     17           2"
    ),
    "snippets/07-client.py": (
        "settlement_date  settlement_period  system_sell_price  system_buy_price  available_at\n"
        "2026-09-08       37                 110.0              110.0             2026-09-09 17:44:29 UTC"
    ),
    "snippets/02-connector-request.py": "/balancing/settlement/system-prices/2026-09-08 {'page': 1}",
}

L: list[str] = []
a = L.append
a("# Architecture page content pack")
a("")
a(f"Built 2026-09-27 by claude-opus-5-5 from gridflow `master` at `{GF_SHA[:7]}` and gridflow-models `main` at "
  f"`{GM_SHA[:7]}`. Every snippet ran against the real code and data, read-only (`RUN-LOG.md`, `_verify.py`). "
  "Machine-readable twin: `pack.json` (same content, plus permalinks with line anchors).")
a("")
a("**Copy rules applied and checked by `_build_pack.py`** (the content source: edit it and re-run it to regenerate this file and pack.json): no em or en dashes, no arrows, no middle dots, no planning words, "
  "no local-data references, no counts of datasets or transformers; labels up to 6 words, index lines up to 20, "
  "stop headings up to 6, stop bodies up to 45, rules up to 18. Red Hat Mono for everything in backticks. "
  "Links point at the default branch (`master` for gridflow, `main` for gridflow-models); `pack.json` also carries "
  "commit permalinks. File:line evidence is at those commits. Paths are relative to the gridflow repo unless marked gridflow_models.")
a("")
a("The example row throughout: **Elexon `system_prices`, settlement date 2026-09-08, period 37.** Two captures of the "
  "same day hold two versions: first published at 9.56, then 110.00 a day later.")
a("")
a("## 1. Opening")
a("")
a(f"**Lede.** {OPENING['lede']}")
a("")
a(f"Designer note (not copy): {OPENING['lede_note']}")
a("")
a(f"**Scope line.** {OPENING['scope']}")
a("")
a("Evidence:")
for e in OPENING["evidence"]:
    a(f"- {e}")
a("")
a("## 2. The system drawing")
a("")
a("Each part: label (drawing), keyed-index line (beside it), link, evidence. Order runs top to bottom: sources above "
  "ground, cables and strata below, readers at the bottom.")
a("")
a("### Above ground: the sources")
a("")
a("| Registered name | Label | Human name | Keyed index | Link | Evidence |")
a("|---|---|---|---|---|---|")
for p in source_parts:
    a(f"| `{p['registered_name']}` | {p['label']} | {p['human_name']} | {p['index']} | {md_links(p['links'])} | "
      f"{'; '.join(p['evidence'][:2])} |")
a("")
a("Note: `gie_agsi` and `gie_alsi` share one connector file; `open_meteo` lives in folder `connectors/openmeteo/`. "
  "Every connector module is imported from one list, `pipeline/runner.py:113-121`.")
a("")
a("### Below ground: cables and strata")
a("")
for p in BOUNDARY_PARTS:
    a(f"**{p['label']}** ({p['layer']})")
    a("")
    a(f"- Index: {p['index']}")
    a(f"- Link: {md_links(p['links'])}")
    a("- Evidence: " + "; ".join(p["evidence"]))
    if "note" in p:
        a(f"- Designer note: {p['note']}")
    a("")
a("### The readers")
a("")
for p in READER_PARTS:
    a(f"**{p['label']}**")
    a("")
    a(f"- Index: {p['index']}")
    if "verbs" in p:
        a("- Verbs: " + ", ".join(f"`{v}`" for v in p["verbs"]))
    if "methods" in p:
        a("- Methods: " + ", ".join(f"`{m}`" for m in p["methods"]) +
          " (`get_weather` also exists but reads demand, not weather; leave it off)")
    if "site_link" in p:
        a(f"- Site link: this part links to the Models page, `{p['site_link']}`.")
    a(f"- Link: {md_links(p['links'])}")
    a("- Evidence: " + "; ".join(p["evidence"]))
    a("")
a("## 3. The row's journey")
a("")
a("Seven stops, one real row. Stop 5 is the highlighted stop.")
a("")
for n, s in enumerate(STOPS, 1):
    star = " (highlighted)" if s.get("highlight") else ""
    a(f"### Stop {n}: {s['heading']}{star}")
    a("")
    a(s["body"])
    a("")
    if "mechanism" in s:
        a(f"**Publication-lag rule, as a mechanism:** {s['mechanism']}")
        a("")
    for rel in s["snippets"]:
        a(snippet_block(rel))
        if rel in RESULTS:
            a("Real output:")
            a("")
            a(f"```text\n{RESULTS[rel]}\n```")
            a("")
    if "snippet_note" in s:
        a(f"Designer note (not copy): {s['snippet_note']}")
        a("")
    a(f"Link: {md_links(s['links'])}")
    a("")
    a("Evidence: " + "; ".join(s["evidence"]))
    a("")
a("## 4. How it stays correct")
a("")
for i, r in enumerate(RULES, 1):
    a(f"{i}. **{r['rule']}** {md_links(r['links'])}. Evidence: {'; '.join(r['evidence'])}."
      + (f" Caveat (not copy): {r['caveat']}" if "caveat" in r else ""))
a("")
a(f"**Run tracking.** {RUN_TRACKING['text']}")
a("")
a(snippet_block(RUN_TRACKING["snippets"][0]))
a(f"Link: {md_links(RUN_TRACKING['links'])}. Evidence: {'; '.join(RUN_TRACKING['evidence'])}. "
  f"Caveat (not copy): {RUN_TRACKING['caveat']}")
a("")
a(f"**CI.** {CI['text']}")
a("")
a(f"Link: {md_links(CI['links'])}. Evidence: {'; '.join(CI['evidence'])}. Caveat (not copy): {CI['caveat']}")
a("")
a("## 5. Where to look")
a("")
for x, links in WHERE:
    a(f"- For {x}, see {md_links(links)}")
a("")
a("## Cut: do not say")
a("")
a("| Do not say | Because |")
a("|---|---|")
for x, why in CUT:
    a(f"| {x} | {why} |")
a("")
a("## Unverified (kept out of the copy)")
a("")
for u in UNVERIFIED:
    a(f"- {u}")
a("")
(OUT / "ARCH-PACK.md").write_text("\n".join(L), encoding="utf-8")
print("ok", {k: words(v) for k, v in {"lede": OPENING["lede"], "scope": OPENING["scope"]}.items()})
for s in STOPS:
    print(s["id"], words(s["heading"]), words(s["body"]), words(s.get("mechanism", "")))
for r in RULES:
    print(words(r["rule"]), r["rule"])
