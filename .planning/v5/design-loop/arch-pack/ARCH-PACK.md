# Architecture page content pack

Built 2026-09-27 by claude-opus-5-5 from gridflow `master` at `2822d38` and gridflow-models `main` at `a17805b`. Every snippet ran against the real code and data, read-only (`RUN-LOG.md`, `_verify.py`). Machine-readable twin: `pack.json` (same content, plus permalinks with line anchors).

**Copy rules applied and checked by `_build_pack.py`** (the content source: edit it and re-run it to regenerate this file and pack.json): no em or en dashes, no arrows, no middle dots, no planning words, no local-data references, no counts of datasets or transformers; labels up to 6 words, index lines up to 20, stop headings up to 6, stop bodies up to 45, rules up to 18. Red Hat Mono for everything in backticks. Links point at the default branch (`master` for gridflow, `main` for gridflow-models); `pack.json` also carries commit permalinks. File:line evidence is at those commits. Paths are relative to the gridflow repo unless marked gridflow_models.

The example row throughout: **Elexon `system_prices`, settlement date 2026-09-08, period 37.** Two captures of the same day hold two versions: first published at 9.56, then 110.00 a day later.

## 1. Opening

**Lede.** Raw API responses land in bronze, cleaned and typed tables settle in silver, and cross-source joins and derived columns sit in gold; one embedded DuckDB file reads silver and gold.

Designer note (not copy): Changed from the old lede on purpose: 'live' is a banned word even as a verb, gold also holds a derived-column builder, and DuckDB registers views for silver and gold only, not bronze (storage/duckdb.py:161-209).

**Scope line.** gridflow has no scheduler, no server, no cloud and no live feed: every run is a gridflow command someone starts, and vendor data arrives only when one runs.

Evidence:
- pyproject.toml:7-21 (dependencies: httpx, tenacity, pydantic, polars, pyarrow, duckdb, lxml, typer and helpers; no web framework, server, cloud SDK or scheduler)
- pyproject.toml:33-34 (gridflow = gridflow.cli:app is the only entry point)
- src/gridflow/config/settings.py:60 (schedule field is parsed from sources.yaml; grep of src finds no reader of it)
- src/gridflow/storage/duckdb.py:54-72 (duckdb.connect on a local file path; no server)
- src/gridflow/cli.py:185-1209 (every stage is a Typer command)

## 2. The system drawing

Each part: label (drawing), keyed-index line (beside it), link, evidence. Order runs top to bottom: sources above ground, cables and strata below, readers at the bottom.

### Above ground: the sources

| Registered name | Label | Human name | Keyed index | Link | Evidence |
|---|---|---|---|---|---|
| `elexon` | Elexon | Elexon Insights API (BMRS) | elexon: GB system prices, generation by fuel, demand, market index prices and REMIT notices. | [`src/gridflow/connectors/elexon/client.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/connectors/elexon/client.py) | config/sources.yaml:2-9; src/gridflow/connectors/elexon/client.py:377 (register_connector("elexon", ...)) |
| `entsoe` | ENTSO-E | ENTSO-E Transparency Platform | entsoe: European day-ahead prices, load, generation, cross-border flows, outages and balancing. | [`src/gridflow/connectors/entsoe/client.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/connectors/entsoe/client.py) | config/sources.yaml:188-195; src/gridflow/connectors/entsoe/client.py:585 (register_connector("entsoe", ...)) |
| `entsog` | ENTSO-G | ENTSO-G Transparency Platform | entsog: European gas flows, nominations, capacity, tariffs and gas quality. | [`src/gridflow/connectors/entsog/client.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/connectors/entsog/client.py) | config/sources.yaml:461-468; src/gridflow/connectors/entsog/client.py:174 (register_connector("entsog", ...)) |
| `neso` | NESO carbon intensity | NESO Carbon Intensity API | neso: GB carbon intensity, national and regional, and the generation mix. | [`src/gridflow/connectors/neso/carbon_intensity.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/connectors/neso/carbon_intensity.py) | config/sources.yaml:602-609; src/gridflow/connectors/neso/carbon_intensity.py:180 (register_connector("neso", ...)) |
| `neso_data_portal` | NESO Data Portal | NESO Data Portal (CKAN API) | neso_data_portal: Daily wind availability, historic generation mix, embedded wind and solar forecasts. | [`src/gridflow/connectors/neso_data_portal/client.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/connectors/neso_data_portal/client.py) | config/sources.yaml:755-775; src/gridflow/connectors/neso_data_portal/client.py:1492 (register_connector("neso_data_portal", ...)) |
| `gie_agsi` | GIE AGSI | GIE AGSI+ gas storage | gie_agsi: European gas storage levels, plus storage unavailability and news. | [`src/gridflow/connectors/gie/client.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/connectors/gie/client.py) | config/sources.yaml:411-446; src/gridflow/connectors/gie/client.py:443 (register_connector("gie_agsi", ...)) |
| `gie_alsi` | GIE ALSI | GIE ALSI LNG | gie_alsi: European LNG terminal data at country level. | [`src/gridflow/connectors/gie/client.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/connectors/gie/client.py) | config/sources.yaml:448-459; src/gridflow/connectors/gie/client.py:444 (register_connector("gie_alsi", ...)) |
| `open_meteo` | Open-Meteo | Open-Meteo weather API | open_meteo: Historical and forecast weather for demand, wind and solar: temperature, wind speed, radiation. | [`src/gridflow/connectors/openmeteo/client.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/connectors/openmeteo/client.py) | config/sources.yaml:146-187; src/gridflow/connectors/openmeteo/client.py:152 (register_connector("open_meteo", ...)) |

Note: `gie_agsi` and `gie_alsi` share one connector file; `open_meteo` lives in folder `connectors/openmeteo/`. Every connector module is imported from one list, `pipeline/runner.py:113-121`.

### Below ground: cables and strata

**Async requests, capped and retried** (cable: vendor to connector)

- Index: One async httpx client per source; a semaphore caps requests in flight; tenacity retries with jittered backoff.
- Link: [`src/gridflow/connectors/base.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/connectors/base.py), [`src/gridflow/utils/retry.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/utils/retry.py)
- Evidence: src/gridflow/connectors/base.py:133-141 (asyncio.Semaphore(config.rate_limit_per_second) and httpx.AsyncClient in __aenter__); config/sources.yaml:757-759 (the code's own note: the semaphore is a concurrency cap despite its name); src/gridflow/utils/retry.py:19-54 (RETRY_POLICY: 5 attempts, wait_random_exponential, retry on TimeoutException, NetworkError, HTTPStatusError); src/gridflow/connectors/elexon/client.py:346-357 (@RETRY_POLICY on _request; async with self._semaphore; raise_for_status)

**Raw bytes plus a sidecar** (cable: connector to bronze)

- Index: Each response is stored byte for byte with a .meta.json sidecar; both land by temp file and atomic rename.
- Link: [`src/gridflow/bronze/writer.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/bronze/writer.py)
- Evidence: src/gridflow/bronze/writer.py:33-34 (sha256 of body, first 8 hex chars; extension from content type); src/gridflow/bronze/writer.py:37-47 (partition by data_date when known, else fetch date: {source}/{dataset}/{YYYY}/{MM}/{DD}); src/gridflow/bronze/writer.py:57 (raw_{fetched_at:%Y%m%dT%H%M%SZ}_{hash8}.{ext}); src/gridflow/bronze/writer.py:67-86 (sidecar fields); src/gridflow/bronze/writer.py:94-105 (temp file then os.replace); src/gridflow/bronze/writer.py:108-119 (json, xml, csv, else bin)

**Bronze: raw responses by date** (stratum)

- Index: bronze/{source}/{dataset}/{YYYY}/{MM}/{DD}/raw_{fetched_at}_{hash8}.json, one file per response page.
- Link: [`src/gridflow/bronze/writer.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/bronze/writer.py)
- Evidence: src/gridflow/bronze/writer.py:37-57; src/gridflow/storage/paths.py:26-38

**Typed transformers stamp every row** (cable: bronze to silver)

- Index: One Polars transformer per dataset: strict types, UTC, Pydantic checks counted not raised, then available_at, source_run_id, dataset_version.
- Link: [`src/gridflow/silver/base.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/silver/base.py), [`src/gridflow/silver/elexon/system_prices.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/silver/elexon/system_prices.py)
- Evidence: src/gridflow/silver/base.py:403 (BaseSilverTransformer); src/gridflow/silver/base.py:1574-1680 (_process_frame: transform, validate, _add_bitemporal_columns at 1671); src/gridflow/silver/base.py:2021-2082 (_validate_against_schema: never raises, never drops a row, returns a failure count); src/gridflow/silver/base.py:2135-2156 (available_at = coalesce(published_at, ingest stamp), row by row); src/gridflow/silver/base.py:2180-2182, 2196-2199 (source_run_id, dataset_version); src/gridflow/pipeline/runner.py:1142, 1197-1199 (transform run id passed as run_id)

**Silver: typed Parquet, Hive-partitioned** (stratum)

- Index: silver/{source}/{dataset}/year=YYYY/month=MM/; append-only datasets keep one file per capture, suffixed _run{capture time}.
- Link: [`src/gridflow/storage/paths.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/storage/paths.py), [`src/gridflow/silver/base.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/silver/base.py)
- Evidence: src/gridflow/storage/paths.py:50-80 (year=/month= partition dir; {dataset}_{YYYYMMDD}.parquet); src/gridflow/silver/base.py:2618-2636 (APPEND_ONLY writes {dataset}_{YYYYMMDD}_run{stamp}.parquet; others overwrite one file per date); src/gridflow/storage/parquet.py:35-54 (temp file, then os.replace)

**DuckDB views over Parquet** (cable: silver to views)

- Index: One view per dataset over read_parquet with Hive partitioning; append-only datasets also get a _latest view.
- Link: [`src/gridflow/storage/duckdb.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/storage/duckdb.py), [`src/gridflow/silver/latest_views.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/silver/latest_views.py)
- Evidence: src/gridflow/storage/duckdb.py:179 (silver_{source}_{dataset}); src/gridflow/storage/duckdb.py:183-199 (_latest view built from LATEST_VIEW_SPECS, or dropped if it cannot be built); src/gridflow/storage/duckdb.py:434-447 (CREATE OR REPLACE VIEW ... read_parquet(..., hive_partitioning=true, union_by_name=true); plain views, not materialised); src/gridflow/cli.py:293, 335 (transform and build refresh the views when they finish)

**One file: gridflow.duckdb** (stratum)

- Index: Views over the Parquet, plus the pipeline_runs, pipeline_watermarks and quality_reports tables. No server.
- Link: [`src/gridflow/storage/duckdb.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/storage/duckdb.py)
- Evidence: src/gridflow/storage/duckdb.py:92-158 (init_catalogue: three tables, then views); src/gridflow/config/settings.py:97-99 (default data/gridflow.duckdb, configurable)

**Gold: a builder and SQL views** (stratum)

- Index: Polars builder system_marginal_price; SQL views gold_uk_imbalance_context, gold_gb_day_ahead_benchmark, gold_eu_gas_storage.
- Link: [`src/gridflow/gold/system_marginal_price.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/gold/system_marginal_price.py), [`src/gridflow/gold/views`](https://github.com/EBentham/gridflow/tree/master/src/gridflow/gold/views)
- Evidence: src/gridflow/gold/system_marginal_price.py:71 (register_builder, the one registered builder); src/gridflow/gold/views/uk_imbalance_context.sql:14-31 (latest system prices joined to NESO carbon intensity); src/gridflow/gold/views/gb_day_ahead_benchmark.sql:13-33 (Elexon MID APXMIDP); src/gridflow/gold/views/eu_gas_storage.sql:4-18 (GIE AGSI storage); src/gridflow/storage/duckdb.py:465-492 (SQL files executed at catalogue registration); src/gridflow/gold/base.py:23 (gold is rebuilt from silver, not incrementally updated)
- Designer note: Not copy: gridflow_models also writes its outputs (forecasts, metrics, stack results) under the same gold/ folder (gridflow_models src/gridflow_models/forecast_store/writer.py:220), and gridflow's catalogue registers every gold folder as a gold_* view (src/gridflow/storage/duckdb.py:203-209). If the drawing shows gridflow_models output in gold, it is a gridflow_models write, not a gridflow build.

### The readers

**The gridflow command**

- Index: init, ingest, transform, build, pipeline, backfill, export-csv, status, quality, reset, prune.
- Verbs: `init`, `ingest`, `transform`, `build`, `pipeline`, `backfill`, `export-csv`, `status`, `quality`, `reset`, `prune`
- Link: [`src/gridflow/cli.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/cli.py)
- Evidence: src/gridflow/cli.py:185 ingest, 260 transform, 305 build, 345 backfill, 437 export-csv, 484 pipeline, 583 status, 676 quality, 795 reset, 971 prune, 1208 init (@app.command); gridflow --help, run 2026-09-27, lists exactly these eleven commands (RUN-LOG.md)

**GridflowClient, read-only, returns Polars**

- Index: from gridflow.serving.client import GridflowClient: query, get_system_prices, get_imbalance_context, get_gas_storage and more.
- Methods: `query`, `get_system_prices`, `get_gb_day_ahead_benchmark`, `get_generation_by_fuel`, `get_fuel_generation`, `get_gas_storage`, `get_imbalance_context`, `get_tables` (`get_weather` also exists but reads demand, not weather; leave it off)
- Link: [`src/gridflow/serving/client.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/serving/client.py)
- Evidence: src/gridflow/serving/client.py:75-89 (duckdb.connect(..., read_only=True)); src/gridflow/serving/client.py:102-104 (query returns .pl(), a Polars DataFrame); src/gridflow/serving/client.py:152, 192, 219, 251, 270, 327, 363 (get_* methods); src/gridflow/serving/client.py:401-405 (context manager); src/gridflow/__init__.py is empty: import from gridflow.serving.client

**Notebooks**

- Index: Any notebook can open a GridflowClient; the gridflow_models workbench notebooks do, through their setup helper.
- Link: [`src/gridflow_models/research/notebook_setup.py`](https://github.com/EBentham/gridflow-models/blob/main/src/gridflow_models/research/notebook_setup.py)
- Evidence: gridflow_models src/gridflow_models/research/notebook_setup.py:435 (GridflowClient(db_path=...)); gridflow_models src/gridflow_models/research/_pandas_client.py:1-6 (the workbench wraps it and hands pandas to the notebook); gridflow repo has no notebooks/ folder

**gridflow_models, reading as of a time**

- Index: Training and backtests read silver Parquet directly, keeping only rows whose available_at is at or before the as-of time.
- Site link: this part links to the Models page, `models.html`.
- Link: [`src/gridflow_models/data/gridflow_source.py`](https://github.com/EBentham/gridflow-models/blob/main/src/gridflow_models/data/gridflow_source.py), [Models page](models.html)
- Evidence: gridflow_models src/gridflow_models/data/gridflow_source.py:45-46 (GridflowDataSource reads gridflow silver files without importing gridflow modules); gridflow_models src/gridflow_models/data/gridflow_source.py:340-366 (WHERE available_at <= ?; optional QUALIFY ROW_NUMBER() ... ORDER BY available_at DESC); gridflow_models src/gridflow_models/data/gridflow_source.py:96-105 (fetch(dataset, event_time_start, event_time_end, as_of, latest_only, ...)); gridflow_models pyproject.toml:32, 101 (gridflow is a local path dependency); gridflow src/gridflow/serving/client.py:161-172 (point-in-time selection is consumer-side, in gridflow_models)

## 3. The row's journey

Seven stops, one real row. Stop 5 is the highlighted stop.

### Stop 1: One command starts the run

Nothing runs on a timer. Someone runs ingest to fetch a day from Elexon into bronze, then transform to turn that bronze into silver. Both take a source, a dataset and a date range.

`snippets/01-cli.sh`

```bash
gridflow ingest elexon system_prices --start 2026-09-08 --end 2026-09-08
gridflow transform elexon system_prices --start 2026-09-08 --end 2026-09-08
```

Link: [`src/gridflow/cli.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/cli.py)

Evidence: src/gridflow/cli.py:185-258 (ingest source dataset --start --end --last --all --incremental); src/gridflow/cli.py:260-303 (transform; refreshes views at 293); src/gridflow/pipeline/runner.py:479-501 (a bare date is midnight UTC), 1134-1138 (inclusive date range); src/gridflow/connectors/elexon/client.py:360-374 (_date_range inclusive)

### Stop 2: The connector calls Elexon

The Elexon connector puts the settlement date in the URL path and follows the pages. A per-source semaphore caps requests in flight, and tenacity retries timeouts, network errors and HTTP errors with jittered backoff.

`snippets/02-connector-request.txt`

```text
GET https://data.elexon.co.uk/bmrs/api/v1/balancing/settlement/system-prices/2026-09-08?page=1
```

`snippets/02-connector-request.py`

```python
from datetime import date

from gridflow.connectors.elexon.endpoints import ENDPOINTS, build_params

endpoint = ENDPOINTS["system_prices"]
path = f"{endpoint.path}/{date(2026, 9, 8).isoformat()}"
print(path, build_params(endpoint, page=1))
```

Real output:

```text
/balancing/settlement/system-prices/2026-09-08 {'page': 1}
```

Link: [`src/gridflow/connectors/elexon/client.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/connectors/elexon/client.py), [`src/gridflow/connectors/elexon/endpoints.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/connectors/elexon/endpoints.py)

Evidence: src/gridflow/connectors/elexon/endpoints.py:58-62 (system_prices: /balancing/settlement/system-prices, DATE_PATH); config/sources.yaml:3 (base_url https://data.elexon.co.uk/bmrs/api/v1); src/gridflow/connectors/elexon/client.py:255 (path = f"{endpoint.path}/{settlement_date.isoformat()}"); src/gridflow/connectors/elexon/client.py:257-282 (page loop until total_pages); the real request_url in both bronze sidecars for 2026-09-08

### Stop 3: Bronze keeps the raw bytes

The response is saved byte for byte, in a folder for the date it describes, beside a .meta.json sidecar recording the request, status and body hash. Fetching the same day again adds a second file next to the first.

`snippets/03-bronze-files.txt`

```text
data/bronze/elexon/system_prices/2026/09/08/
  raw_20260908T214403Z_3a7fca58.json
  raw_20260908T214403Z_3a7fca58.meta.json
  raw_20260916T190532Z_4c2c01b2.json
  raw_20260916T190532Z_4c2c01b2.meta.json
```

`snippets/03-bronze-body-excerpt.json`

```json
{
  "metadata": { "datasets": ["DISEBSP"] },
  "data": [
    {
      "settlementDate": "2026-09-08",
      "settlementPeriod": 37,
      "startTime": "2026-09-08T17:00:00Z",
      "createdDateTime": "2026-09-08T17:48:45Z",
      "systemSellPrice": 9.56,
      "systemBuyPrice": 9.56,
      "priceDerivationCode": "N",
      "netImbalanceVolume": -1467.4127825220955
    }
  ]
}
```

`snippets/03-bronze-sidecar.json`

```json
{
  "source": "elexon",
  "dataset": "system_prices",
  "fetched_at": "2026-09-08T21:44:03.540996+00:00",
  "written_at": "2026-09-08T21:44:03.546999+00:00",
  "data_date": "2026-09-08",
  "request_url": "https://data.elexon.co.uk/bmrs/api/v1/balancing/settlement/system-prices/2026-09-08?page=1",
  "request_params": { "page": 1 },
  "api_version": "v1",
  "http_status": 200,
  "content_type": "application/json; charset=utf-8",
  "body_sha256": "3a7fca5829bdc6b15878ab19659625b6d52cdfcb6abec67094e828e44a18571f",
  "body_size_bytes": 39466,
  "page": 1,
  "total_pages": 1
}
```

Designer note (not copy): Body excerpt shows 8 of the record's 22 fields and 1 of its records; every value shown is real.

Link: [`src/gridflow/bronze/writer.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/bronze/writer.py)

Evidence: src/gridflow/bronze/writer.py:33-57 (hash, timestamp, date partition, filename); src/gridflow/bronze/writer.py:67-86 (sidecar); src/gridflow/bronze/writer.py:61-63 (written_at marks the durable write)

### Stop 4: Silver keeps every version

Each bronze capture becomes its own typed Parquet file, named for when it was captured, and both prices are kept. Every row is checked against a Pydantic schema and stamped with available_at (Elexon's publication time), source_run_id and dataset_version.

`snippets/04-silver-files.txt`

```text
data/silver/elexon/system_prices/year=2026/month=09/
  system_prices_20260908_run2026-09-08T21-44-03.546999-00-00.parquet
  system_prices_20260908_run2026-09-16T19-05-32.981753-00-00.parquet
```

`snippets/04-silver-vintages.sql`

```sql
SELECT settlement_date, settlement_period,
       system_sell_price, system_buy_price,
       available_at, vintage_policy, source_run_id, dataset_version
FROM silver_elexon_system_prices
WHERE settlement_date = DATE '2026-09-08' AND settlement_period = 37
ORDER BY available_at;
```

Real output:

```text
settlement_date  settlement_period  system_sell_price  system_buy_price  available_at             vintage_policy  source_run_id                         dataset_version
2026-09-08       37                 9.56               9.56              2026-09-08 17:48:45 UTC  vendor          494e780a-a127-4fa8-b371-25caf146c094  2.0.0
2026-09-08       37                 110.0              110.0             2026-09-09 17:44:29 UTC  vendor          494e780a-a127-4fa8-b371-25caf146c094  2.0.0
```

Designer note (not copy): File suffix = the bronze capture's written_at. Row available_at = Elexon's createdDateTime. They are different instants; do not conflate them. source_run_id is the pipeline_runs.run_id of the transform that wrote the row. dataset_version is the transformer's output version, not a gridflow version.

Link: [`src/gridflow/silver/elexon/system_prices.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/silver/elexon/system_prices.py), [`src/gridflow/silver/base.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/silver/base.py)

Evidence: src/gridflow/silver/elexon/system_prices.py:65-66 (APPEND_ONLY, VINTAGE_PER_BRONZE_FILE); src/gridflow/silver/elexon/system_prices.py:129 (createdDateTime becomes published_at); src/gridflow/silver/elexon/system_prices.py:199-220 (casts; UTC timestamp from date and period); src/gridflow/silver/base.py:1364-1474 (one silver file per bronze body; stamp from the sidecar); src/gridflow/silver/base.py:2633-2636 (filename {dataset}_{YYYYMMDD}_run{stamp}.parquet); src/gridflow/silver/base.py:2155 (available_at = coalesce(published_at, ingest stamp)); src/gridflow/silver/base.py:2021-2082 (Pydantic check, fail-soft, counted)

### Stop 5: The latest view picks a winner (highlighted)

silver_elexon_system_prices_latest keeps one row per settlement period: the latest available_at wins, ties go to the later settlement run. The base view keeps both, so a backtest can ask what was known at any moment: here, 9.56 until the revision.

**Publication-lag rule, as a mechanism:** When a vendor gives no publication time, a dated per-dataset rule estimates when each value could first have been known, for history before a set cutover. On datasets that declare one, each row records which applied: vendor, the rule's name, or ingest-clock.

`snippets/05-latest-view-ddl.sql`

```sql
CREATE OR REPLACE VIEW "silver_elexon_system_prices_latest" AS
SELECT * FROM "silver_elexon_system_prices"
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY "settlement_date", "settlement_period"
    ORDER BY "available_at" DESC NULLS LAST,
             CASE "run_type" WHEN 'II' THEN 1 WHEN 'SF' THEN 2 WHEN 'R1' THEN 3 WHEN 'R2' THEN 4 WHEN 'R3' THEN 5 WHEN 'RF' THEN 6 WHEN 'DF' THEN 7 ELSE 0 END DESC
) = 1
```

`snippets/05-latest-view.sql`

```sql
SELECT settlement_date, settlement_period,
       system_sell_price, system_buy_price, available_at
FROM silver_elexon_system_prices_latest
WHERE settlement_date = DATE '2026-09-08' AND settlement_period = 37;
```

Real output:

```text
settlement_date  settlement_period  system_sell_price  system_buy_price  available_at
2026-09-08       37                 110.0              110.0             2026-09-09 17:44:29 UTC
```

`snippets/05-as-of.sql`

```sql
SELECT settlement_date, settlement_period, system_sell_price, available_at
FROM silver_elexon_system_prices
WHERE settlement_date = DATE '2026-09-08' AND settlement_period = 37
  AND available_at <= TIMESTAMPTZ '2026-09-09 12:00:00+00'
QUALIFY row_number() OVER (
    PARTITION BY settlement_date, settlement_period
    ORDER BY available_at DESC
) = 1;
```

Real output:

```text
settlement_date  settlement_period  system_sell_price  available_at
2026-09-08       37                 9.56               2026-09-08 17:48:45 UTC
```

Designer note (not copy): 05-as-of.sql is the as-of read gridflow_models applies (available_at at or before the as-of time, then the latest survivor); gridflow's own _latest view is the current best value, not an as-of read. This row's vintage_policy is vendor: Elexon supplied the time, so the lag rule did not apply. Never print the rule's lag figure or cutover date.

Link: [`src/gridflow/silver/latest_views.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/silver/latest_views.py), [`src/gridflow/silver/base.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/silver/base.py)

Evidence: src/gridflow/silver/latest_views.py:84-99 (II..DF rank; system_prices key settlement_date, settlement_period; rank on run_type); src/gridflow/silver/latest_views.py:260-269 (ORDER BY available_at DESC NULLS LAST, then rank DESC; ROW_NUMBER() = 1); src/gridflow/silver/latest_views.py:32-39 (available_at leads because the live feed has no run label); src/gridflow/storage/duckdb.py:183-199 (view registered from LATEST_VIEW_SPECS); src/gridflow/silver/base.py:36-67 (VintagePolicy: name, lag, dated, rule, applies_before); src/gridflow/silver/base.py:2159-2193 (policy replaces only the fallback, before the cutover; labels vendor / policy name / ingest-clock); src/gridflow/silver/elexon/system_prices.py:48-62 (system_prices declares a policy; its rule text calls itself an assumption); src/gridflow/serving/client.py:161-172 (as-of selection is consumer-side); gridflow_models src/gridflow_models/data/gridflow_source.py:340-366 (available_at <= as_of, latest survivor)

### Stop 6: Gold adds derived columns

The system_marginal_price builder reads the latest version of each period and adds spread (buy minus sell), absolute imbalance, hour of day and ISO day of week. Buy and sell are equal in this period, so spread is 0.0.

`snippets/06-gold-build.sh`

```bash
gridflow build system_marginal_price --start 2026-09-08 --end 2026-09-08
```

`snippets/06-gold-spread.py`

```python
(pl.col("system_buy_price") - pl.col("system_sell_price")).alias("spread")
```

`snippets/06-gold-build.py`

```python
from datetime import date

import polars as pl

from gridflow.config.settings import load_settings
from gridflow.gold.system_marginal_price import SystemMarginalPriceBuilder

builder = SystemMarginalPriceBuilder(load_settings().pipeline.data_dir)
gold = builder.build(date(2026, 9, 8), date(2026, 9, 8))  # build() returns the frame; run() writes it
print(
    gold.filter(pl.col("settlement_period") == 37).select(
        "settlement_date", "settlement_period", "system_buy_price", "system_sell_price",
        "spread", "abs_imbalance", "hour_of_day", "day_of_week",
    )
)
```

Real output:

```text
settlement_date  settlement_period  system_buy_price  system_sell_price  spread  abs_imbalance  hour_of_day  day_of_week
2026-09-08       37                 110.0             110.0              0.0     346.717783     17           2
```

Designer note (not copy): The row was produced by the builder's build() method, which returns the frame; gridflow build calls run(), which also writes gold/system_marginal_price/year=2026/system_marginal_price_20260908.parquet. hour_of_day is the UTC hour.

Link: [`src/gridflow/gold/system_marginal_price.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/gold/system_marginal_price.py)

Evidence: src/gridflow/gold/system_marginal_price.py:36-40 (scan silver, select_latest_vintage); src/gridflow/gold/system_marginal_price.py:48 (system_buy_price - system_sell_price AS spread); src/gridflow/gold/system_marginal_price.py:50, 63-64 (abs_imbalance, hour_of_day, day_of_week ISO); src/gridflow/gold/base.py:40-68 (run writes gold/{name}/year=YYYY/{name}_{YYYYMMDD}.parquet)

### Stop 7: Read it into Polars

GridflowClient opens the DuckDB file read-only and returns Polars DataFrames. get_system_prices reads the _latest view, so each settlement period comes back once, with available_at kept so you know which version you hold.

`snippets/07-client.py`

```python
import polars as pl

from gridflow.serving.client import GridflowClient

with GridflowClient() as gf:
    prices = gf.get_system_prices("2026-09-08", "2026-09-08")

print(
    prices.filter(pl.col("settlement_period") == 37).select(
        "settlement_date", "settlement_period", "system_sell_price", "system_buy_price",
        pl.col("available_at").dt.convert_time_zone("UTC"),
    )
)
```

Real output:

```text
settlement_date  settlement_period  system_sell_price  system_buy_price  available_at
2026-09-08       37                 110.0              110.0             2026-09-09 17:44:29 UTC
```

Link: [`src/gridflow/serving/client.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/serving/client.py)

Evidence: src/gridflow/serving/client.py:53 (_REL_SYSTEM_PRICES = silver_elexon_system_prices_latest); src/gridflow/serving/client.py:44 (available_at and vintage_policy retained); src/gridflow/serving/client.py:182-190 (SELECT ... WHERE settlement_date BETWEEN ? AND ?, .pl()); src/gridflow/serving/client.py:87-89 (read_only=True)

## 4. How it stays correct

1. **Raw responses are kept, so any silver table can be rebuilt without calling the vendor again.** [`src/gridflow/bronze/writer.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/bronze/writer.py). Evidence: src/gridflow/bronze/writer.py:57-63; src/gridflow/silver/base.py:837-846 (transformers read bronze); src/gridflow/cli.py:268-272 (transform --reingest rebuilds with sidecar timestamps). Caveat (not copy): True while bronze exists: gridflow reset and prune delete bronze on request (cli.py:795, 971).
2. **Re-runs are safe: every file lands by temp file and atomic rename, never half-written.** [`src/gridflow/storage/parquet.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/storage/parquet.py). Evidence: src/gridflow/bronze/writer.py:94-105; src/gridflow/storage/parquet.py:35-54. Caveat (not copy): Do not claim re-runs rewrite the same files. Re-ingesting adds a new bronze file (the name carries fetch time). Append-only silver datasets can gain a new version file on a plain re-transform, because the stamp is the transform time unless --reingest or the per-capture path supplies the sidecar time (silver/base.py:1181-1183, 2618-2625). Non-append-only datasets overwrite one file per date.
3. **Rows that fail validation are still written, counted, and the run is marked completed with warnings.** [`src/gridflow/silver/base.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/silver/base.py). Evidence: src/gridflow/silver/base.py:2021-2035; src/gridflow/pipeline/runner.py:1232, 1423; src/gridflow/observability.py:151-160 (status completed_with_warnings). Caveat (not copy): Extra fields pass the Pydantic check (schemas/common.py:13, extra="ignore"). Do not say drift fails loudly or raises.
4. **Each row gridflow writes carries available_at: vendor publication time if given, else a dated estimate or gridflow's clock.** [`src/gridflow/silver/base.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/silver/base.py). Evidence: src/gridflow/silver/base.py:2135-2156; src/gridflow/silver/base.py:2159-2193; src/gridflow/silver/base.py:1181-1183 (fallback is the transform time, or the sidecar time with --reingest).
5. **One embedded DuckDB file is the catalogue; GridflowClient opens it read-only, and there is no server.** [`src/gridflow/storage/duckdb.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/storage/duckdb.py). Evidence: src/gridflow/storage/duckdb.py:54-72; src/gridflow/serving/client.py:87-89.

**Run tracking.** Every ingest, transform and build writes a row to pipeline_runs with its status, row counts and any error, and each silver row's source_run_id points back to it. Incremental ingest resumes from pipeline_watermarks. gridflow quality runs row-count, null-rate, gap and duplicate checks and writes them to quality_reports.

`snippets/08-run-tracking.sql`

```sql
CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id          VARCHAR PRIMARY KEY,
    source          VARCHAR NOT NULL,
    dataset         VARCHAR NOT NULL,
    operation       VARCHAR NOT NULL,
    started_at      TIMESTAMP WITH TIME ZONE NOT NULL,
    completed_at    TIMESTAMP WITH TIME ZONE,
    status          VARCHAR NOT NULL,
    rows_in         INTEGER DEFAULT 0,
    rows_out        INTEGER DEFAULT 0,
    rows_skipped    INTEGER DEFAULT 0,
    duration_seconds FLOAT,
    error_message   VARCHAR,
    parameters      VARCHAR
)
```

Link: [`src/gridflow/observability.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/observability.py), [`src/gridflow/quality/checks.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/quality/checks.py). Evidence: src/gridflow/pipeline/runner.py:937, 1142, 1567 (PipelineRunTracker for ingest, transform, build); src/gridflow/observability.py:63-221 (running, success, completed_with_warnings, failed); src/gridflow/observability.py:236-300 (monotonic watermark upsert); src/gridflow/cli.py:195-206 (ingest --incremental resumes from the watermark); src/gridflow/cli.py:676-792 (quality runs check_row_count, check_null_rate, check_time_series_gaps, check_duplicates); src/gridflow/quality/reporter.py:47-123 (writes quality_reports); src/gridflow/storage/duckdb.py:106-145 (the three tables). Caveat (not copy): checks.py also defines check_range (line 120), but the quality verb does not run it. Name the four it runs.

**CI.** On every push and pull request, gridflow's CI checks the lockfile, runs ruff lint and format checks, mypy over src/gridflow, and pytest with live-API tests excluded.

Link: [`.github/workflows/ci.yml`](https://github.com/EBentham/gridflow/blob/master/.github/workflows/ci.yml). Evidence: .github/workflows/ci.yml:2 (on: [push, pull_request]); .github/workflows/ci.yml:19 (uv lock --check); .github/workflows/ci.yml:28, 31 (ruff check, ruff format --check); .github/workflows/ci.yml:39 (mypy src/gridflow/); .github/workflows/ci.yml:42 (pytest tests/ -m "not live"). Caveat (not copy): CI does not run the pipeline against real data. Do not say it runs identically in CI.

## 5. Where to look

- For which sources and endpoints are configured, see [`config/sources.yaml`](https://github.com/EBentham/gridflow/blob/master/config/sources.yaml)
- For how a connector requests, limits and retries, see [`src/gridflow/connectors/base.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/connectors/base.py), [`src/gridflow/utils/retry.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/utils/retry.py)
- For how raw responses are stored, see [`src/gridflow/bronze/writer.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/bronze/writer.py)
- For how bronze becomes silver: validation, timestamps, file names, see [`src/gridflow/silver/base.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/silver/base.py)
- For a complete transformer, Elexon system prices, see [`src/gridflow/silver/elexon/system_prices.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/silver/elexon/system_prices.py)
- For how the latest version is chosen, see [`src/gridflow/silver/latest_views.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/silver/latest_views.py)
- For the catalogue, its views and run tables, see [`src/gridflow/storage/duckdb.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/storage/duckdb.py)
- For gold builders and SQL views, see [`src/gridflow/gold/system_marginal_price.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/gold/system_marginal_price.py), [`src/gridflow/gold/views`](https://github.com/EBentham/gridflow/tree/master/src/gridflow/gold/views)
- For reading data into Polars, see [`src/gridflow/serving/client.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/serving/client.py)
- For every command, see [`src/gridflow/cli.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/cli.py)
- For run tracking and quality checks, see [`src/gridflow/observability.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/observability.py), [`src/gridflow/quality/checks.py`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/quality/checks.py)
- For what CI runs, see [`.github/workflows/ci.yml`](https://github.com/EBentham/gridflow/blob/master/.github/workflows/ci.yml)
- For how gridflow_models reads gridflow as of a time, see [`src/gridflow_models/data/gridflow_source.py`](https://github.com/EBentham/gridflow-models/blob/main/src/gridflow_models/data/gridflow_source.py)

## Cut: do not say

| Do not say | Because |
|---|---|
| Bronze stored as Parquet, a 'Raw Parquet Lake', or Hive/as_of= folders in bronze | bronze is raw bytes (.json/.xml/.csv/.bin) plus .meta.json in {source}/{dataset}/YYYY/MM/DD (bronze/writer.py:37-57, 108-119) |
| Pydantic-validated bronze | nothing is validated at bronze; validation is a silver step (silver/base.py:2021) |
| The SHA-256 filename makes re-fetching a no-op | the name also carries fetch time; a re-fetch writes a new file (bronze/writer.py:57) |
| @register_connector decorator; 'no central wiring file' | a plain register_connector(source, cls) call, and runner.py:113-121 lists the modules |
| A rate limit of N requests per second | the semaphore caps requests in flight (sources.yaml:757-759) |
| Point-in-time or as-of reads in gridflow's gold or _latest views | _latest is the current best value; as-of reads are consumer-side (serving/client.py:161-172) |
| Materialised views | plain CREATE OR REPLACE VIEW over read_parquet (storage/duckdb.py:445-447) |
| A query or run verb | verbs are init, ingest, transform, build, pipeline, backfill, export-csv, status, quality, reset, prune |
| MLflow, PuLP dispatch | neither is used (MeritOrderDispatchLP.solve raises NotImplementedError in gridflow_models) |
| 'Nothing is ever deleted', 'bronze is forever' | reset and prune delete on request (cli.py:795, 971) |
| system_prices_20260429.parquet, 'one Parquet per dataset per date' for system_prices, 'deduplicated by primary key' | append-only datasets keep one file per capture: {dataset}_{YYYYMMDD}_run{stamp}.parquet |
| A run-type precedence resolver inside the transformer (RUN_PRECEDENCE, _resolve_runs) | the transformer keeps every version; the II..DF rank is only the tie-break in the _latest view |
| Weather-adjusted demand; gold/demand_features.py; gold/merit_order.py | not in gridflow; the only builder is system_marginal_price |
| A documented derivation for every gold column | no such record exists |
| silver_system_prices as the view name; a run_type = 'DF' filter | canonical names are silver_elexon_system_prices and silver_elexon_system_prices_latest; live rows have null run_type |
| from gridflow import GridflowClient | gridflow/__init__.py is empty; use from gridflow.serving.client import GridflowClient |
| spread = sell minus buy | gridflow defines spread = buy minus sell (gold/system_marginal_price.py:48) |
| pandas, DuckDB WASM or Tableau as ways to query | unverified and off-brand; drop |
| 'Schema drift fails loudly', 'raises ValidationError', 'every silver dataset has a Pydantic model' | validation is fail-soft and counted; some transformers set schema_cls = None (silver/base.py:419, silver/gie/agsi.py:301) |
| 'Runs identically in CI', 'same files, same results' | CI runs lock check, ruff, mypy and pytest without live tests |
| 'Every gold value is one SQL query from the raw bytes' | silver carries source_run_id, not a bronze file reference |
| Counts of sources, connectors, datasets, transformers or views | counts change; name things instead |
| gridflow_models reads everything through GridflowClient | training and backtests read silver Parquet directly with an as-of filter; only the notebook workbench uses GridflowClient |
| get_weather returns weather | it returns Elexon ITSDO demand outturn; the name is a documented misnomer (serving/client.py:302-306); leave it off |
| The quality verb runs five checks | it runs four; check_range exists but is not wired into the verb |
| The system_prices lag figure or cutover date | the code labels them an assumption; describe the mechanism only |
| A gridflow version number, or MIT for gridflow | gridflow is Apache-2.0 and its version is not safe to print |
| Scheduled, hourly or real-time runs | the schedule key in sources.yaml is parsed but used by nothing; every run is a command |
| Spread as a signal for this row | buy equals sell in the example period, so spread is 0.0; do not caption a cause |
| 'Nothing skips a layer' | GridflowClient reads silver views directly; the claim adds nothing |

## Unverified (kept out of the copy)

- GitHub links: built from the local remotes (gridflow master at 2822d38, gridflow-models main at a17805b). Not opened online, so whether they resolve publicly was not checked.
- Why Elexon published a different price for 2026-09-08 period 37 on 2026-09-09: not in the repo. Do not caption a cause.
- Why buy and sell prices are equal in the example period: a market-rule explanation is not in the repo. Show the value, not a reason.
- The system_prices publication-lag rule: the code itself marks its lag and cutover as an assumption with a TODO (system_prices.py:48-62).
- 01-cli.sh and 06-gold-build.sh were not executed (they write). Their options were checked with --help, and 06's result was produced by build() in memory.
- Re-running 01-cli.sh today may fetch different bytes than the two captures shown, if Elexon has published again.
- SQL output shows UTC because the check session set TimeZone = 'UTC'; a DuckDB shell shows the machine's timezone.
