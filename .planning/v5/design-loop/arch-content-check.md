claude-opus-5-5

# Architecture page content check (site/hifi/architecture.html vs gridflow code)

Checked 2026-09-27 against gridflow `src/gridflow`, `config/sources.yaml`, `README.md`, gridflow_models `pyproject.toml` + `src`, and the TOPPAGES pack section (b). Paths below are relative to the gridflow repo unless prefixed `models:`. Local row counts and windows were not used as proposed copy.

Page-wide site-rule breaks (apply to every section, listed once): em dashes throughout the prose and code comments; tracked all-caps eyebrows and middle-dot meta strings ("01 · SOURCES", "INVARIANTS", "elexon · system_prices"); "→" on the TOC links and "Read the full source on GitHub →"; italic single word in two headlines ("query.", "build."). No planning words (planned/shipped/trained/live) and no local-machine paths or local counts were found.

## 1. Header, "How Gridflow is built"
Says: a medallion pipeline (bronze raw, silver cleaned, gold joins) queryable from one embedded DuckDB catalogue; stat strip "3 pipeline layers / 7 async connectors / 67 silver transformers / Polars, DuckDB, httpx".

Wrong or stale:
- "67 silver transformers": 164 are registered (elexon 33, entsoe 48, entsog 33, neso 33, gie_agsi 7, open_meteo 6, neso_data_portal 3, gie_alsi 1). Evidence: `silver/registry.py` `_REGISTRY` after `runner.import_transformers()`, counted live.
- "7 async connectors": 7 connector modules (`pipeline/runner.py:113-121`) but 8 registered source names (gie splits into gie_agsi + gie_alsi, `connectors/gie/client.py:443-444`). Defensible only as "modules".

Fine: medallion framing; single embedded DuckDB file (`storage/duckdb.py:92`); Polars/DuckDB/httpx stack.

Site rules: big-number stat strip is on the DESIGN.md do-not-use list, and TOPPAGES rule 1 forbids hard-coded counts.

Verdict: KEEP WITH FIXES. The one-sentence lede is accurate; drop the stat strip entirely rather than correct its numbers.

## 2. "From vendor API to query" (system diagram)
Says: six vendors flow through bronze, silver, gold into four consumers (CLI, gridflow_models, Jupyter, MLflow), with a cross-cutting registry/CLI band.

Wrong or stale:
- Bronze box ".parquet / Raw Parquet Lake": bronze is raw response bytes with the extension chosen by content type (.json/.xml/.csv/.bin) plus `.meta.json` (`bronze/writer.py:34, 56, 85`).
- Bronze "Hive-partitioned layout, vendor/dataset/as_of=…" and "→ bronze/{vendor}/{dataset}/as_of=…": bronze dirs are plain `{source}/{dataset}/{YYYY}/{MM}/{DD}` (`bronze/writer.py:40-47`). Hive `year=/month=` is silver only (`storage/paths.py:50-73`).
- "Pydantic-validated payloads" in bronze: nothing is validated at bronze; `RawResponse` is a frozen dataclass (`connectors/base.py:32`). Validation is a silver step (`silver/base.py:2020`).
- "SHA-256 filename → idempotent re-fetch": the filename also carries `fetched_at` (`bronze/writer.py:32-33, 56`), so re-fetching an identical body writes a new file. Duplicates are detectable, not skipped.
- "@register_connector(vendor, dataset)": a plain call keyed by source only, `register_connector("elexon", ElexonConnector)` (`connectors/registry.py:15`, `connectors/elexon/client.py:377`).
- Gold "Point-in-time correctness, as_of @ SQL": the client says `available_at <= as_of` is a fail-closed cutoff, not historical PIT, and PIT is consumer-side, "not built here" (`serving/client.py:161-172`).
- Gold "Materialised views, CREATE VIEW": the views are plain, unmaterialised `CREATE OR REPLACE VIEW ... read_parquet(...)` (`storage/duckdb.py:445-447`).
- CLI "ingest, transform, build, query": there is no `query` verb; real verbs are init, ingest, transform, build, pipeline, backfill, export-csv, status, quality, reset, prune (`cli.py:185-1209`).
- gridflow_models "PuLP LP dispatch": `MeritOrderDispatchLP.solve` raises NotImplementedError (models: `src/gridflow_models/optim/dispatch.py:1-25`); pulp is declared (models: `pyproject.toml:19`) but never imported. Merit-order clearing is `SupplyCurve.clear_at_demand`.
- "MLflow tracking, local file-mode": no MLflow dependency or import in either repo (grep of both `src` trees and both `pyproject.toml`).
- Sources band omits NESO Data Portal, a configured and registered source (`config/sources.yaml:755`, `connectors/neso_data_portal/client.py:1492`).

Fine: httpx async connectors with `asyncio.Semaphore(rate_limit_per_second)` (`connectors/base.py:135`); tenacity retries on HTTP status, timeout and network errors (`utils/retry.py:20-51`); `os.replace` atomic writes (`bronze/writer.py:95-99`); silver UTC, dedup, settlement period 1 to 50 (`schemas/elexon.py:43`); `hive_partitioning=true` (`storage/duckdb.py:447`); LightGBM quantile (models: `estimators/day_ahead/lgbm_quantile.py`) and MAPIE (models: `estimators/fundamentals_smp/model.py`); ENTSO-G flows and nominations, Open-Meteo temperature/wind/solar (`config/sources.yaml`); Jupyter reading through GridflowClient (`serving/client.py:61`).

Site rules: the SVG's embedded CSS names Inter, Fraunces and JetBrains Mono (DESIGN.md do-not-use, and off the locked type stack); node-and-arrow flowchart is itself on the do-not-use list; "01 · SOURCES" eyebrows.

Verdict: CUT. Nine wrong labels, two banned fonts and a banned diagram form; the medallion section below carries the same story with fewer errors.

## 3. "Bronze, Silver, Gold"
Says: bronze is raw, immutable, append-only, one file per response with a SHA-256 name; silver is typed, deduplicated, one Parquet per dataset per date, Hive year/month; gold is cross-source joins and derived features from DuckDB SQL or Polars builders.

Wrong or stale:
- Bronze "Every write appends; nothing is ever overwritten or deleted": `reset` (`cli.py:796`) and `prune` (`cli.py:972`) delete bronze on operator request. True for the pipeline, false as an absolute.
- Silver "One Parquet file per dataset per calendar date": the 6 append-only datasets write one file per vintage, `{dataset}_{YYYYMMDD}_run{available_at}.parquet` (`silver/base.py:2633-2636`). The example path `system_prices_20260429.parquet` is exactly one of those datasets, so its filename is wrong.
- Silver "deduplicated by primary key": append-only datasets keep every vintage; latest is chosen in the `_latest` view (`silver/latest_views.py:94-99`).
- Gold "weather-adjusted demand": no such builder; the only registered builder is `system_marginal_price` (`gold/registry.py`), which adds spread, abs_imbalance, hour_of_day, day_of_week (`gold/system_marginal_price.py:48-64`).
- Gold "documented derivation for every column": unsupported; no per-column derivation record found.
- "silver → BaseGoldBuilder.build()": correct name, but the entry point the CLI calls is `run()` (`gold/base.py:33, 40`). Minor.

Fine: bronze example path shape `raw_{ts}_{hash8}.json` + `.meta.json` (`bronze/writer.py:56, 85`); silver snake_case, strict types, Hive year/month, atomic `os.replace` (`storage/parquet.py`); silver example directory shape; gold path shape `gold/{name}/year=YYYY/{name}_{YYYYMMDD}.parquet` (`storage/paths.py:96-101`); gold as SQL views or Polars builders (`gold/views/*.sql`); `BronzeWriter.write`, `BaseSilverTransformer.run` names.

Site rules: headline "Bronze · Silver · Gold." uses a middle-dot string; "INVARIANTS" eyebrows.

Verdict: KEEP WITH FIXES. Best compact statement of the layer contract; fix the absolutes and the append-only exception.

## 4. "One dataset, six steps" (system_prices trace)
Says: follows Elexon system_prices from CLI call to SQL, through connector, bronze write, silver transform with run-type precedence, DuckDB view registration and query.

Wrong or stale:
- Step 01 "Each source is a registered module, no central wiring file": `_CONNECTOR_MODULES` in `pipeline/runner.py:113` is that central list.
- Step 02 `RawResponse` listing omits `request_params`, `api_version`, `total_pages` and shows `page` as a "pagination cursor" (it is a page number, `connectors/base.py:36-49`). Minor.
- Step 03 hard-codes `.json`; extension follows content type (`bronze/writer.py:34`). "idempotent re-fetch is a no-op": false, see section 2.
- Step 04 is invented. `silver/elexon/system_prices.py` has no `RUN_PRECEDENCE` or `_resolve_runs`; the transformer is `APPEND_ONLY` + `VINTAGE_PER_BRONZE_FILE` (lines 65-66) and keeps every vintage. The II..DF rank exists, but in `silver/latest_views.py:84-99`, as the secondary tie-break after `available_at` in the `_latest` view; the live feed carries no run label (`latest_views.py:32-36`).
- Step 05 view name `silver_system_prices` is the deprecated alias (`storage/duckdb.py:255-277`); canonical is `silver_elexon_system_prices`, plus `silver_elexon_system_prices_latest` (`storage/duckdb.py:179-186`). Glob `data/silver/...` is fine. Views are refreshed by the CLI after transform/build (`cli.py:293, 335`), not by the transformer.
- Step 06 SQL `FROM silver_system_prices ... AND run_type = 'DF'`: returns every stacked vintage, and live rows have null run_type, so the filter drops them. Use `silver_elexon_system_prices_latest` with no run_type filter.
- Step 06 `from gridflow import GridflowClient`: `src/gridflow/__init__.py` is empty; the import is `from gridflow.serving.client import GridflowClient` (models: `control/discover.py:361` uses exactly that).
- Step 06 spread = sell minus buy in both examples; gridflow's gold defines spread = buy minus sell (`gold/system_marginal_price.py:48`).
- "pandas, DuckDB WASM, Tableau" as query tools: unverified and off-brand for a Polars-only project; drop.

Fine: dataset description (SBP/SSP half-hourly imbalance settlement prices); semaphore rate limit 2/s for Elexon (`config/sources.yaml:6`); bronze filename code and date partitioning (`bronze/writer.py:32-47`); `get_system_prices(start, end)` returns Polars, read-only connection (`serving/client.py:86-88, 152-191`); single DuckDB file, no server.

Site rules: step numbering 01 to 06 is a real sequence, fine; em dashes in code comments.

Verdict: KEEP WITH FIXES. The strongest idea on the page, but steps 04 to 06 must be rewritten around append-only vintages and the `_latest` view.

## 5. "How we build" (principles)
Says: six principles: idempotency, immutable bronze, schema as contract, provenance, partition by event time, boring stack.

Wrong or stale:
- "Schema as contract: upstream changes raise ValidationError at parse time, never a silent NaN column": inverted. `_validate_against_schema` is fail-soft, "Never raises and never drops a row"; invalid rows are written and the count is surfaced as a run warning; `extra="ignore"` tolerates new fields (`silver/base.py:2020-2035`). "Every silver dataset has a Pydantic v2 model" is also false: `schema_cls` defaults to None (`silver/base.py:419`) and the GIE AGSI transformer sets it to None (`silver/gie/agsi.py:301`).
- Idempotency "converges to the same state on disk": bronze gains a new file per fetch and append-only silver gains a new vintage file per run (`bronze/writer.py:56`, `silver/base.py:2633-2636`). Re-runs are safe, not byte-convergent. "Backfill is not a special code path": true in substance (it loops `run_ingest`/`run_transform`, `cli.py:346-420`), though a `backfill` verb and `assert_backfillable` exist.
- "Bronze is forever": `reset`/`prune` can delete it (`cli.py:796, 972`).
- "Every gold value is one SQL query away from the raw bytes": silver carries `source_run_id`/`ingested_at`, not a bronze file reference; lineage to bytes is not a single query. Soften.
- "runs identically in CI, same files, same results": gridflow CI runs lock check, ruff, mypy and `pytest -m "not live"`, not the pipeline (`.github/workflows/ci.yml:19-42`).

Fine: replay from bronze without re-hitting APIs; `.meta.json` sidecar fields (`bronze/writer.py:67-84`); partition by data date when known, else fetch date (`bronze/writer.py:37-39`); Polars/DuckDB/httpx/Pydantic/Typer stack.

Site rules: "How we build" uses "we" for a single-author project (tone, not a rule); italic "build."

Verdict: KEEP WITH FIXES. Recruiters read principles, but "Drift fails loudly" states the opposite of the code and must be rewritten as "drift is counted and surfaced, never dropped".

## 6. "Repo map"
Says: annotated `src/gridflow/` tree, four key abstractions, and the `data/` layout.

Wrong or stale:
- Dataset counts: entsoe "49 datasets" (47 configured, 48 transformers), silver entsoe "26 transformers" (48), gie "8 datasets" (8 = 7 + 1, fine). All counts violate TOPPAGES rule 1 anyway.
- `gold/demand_features.py` and `gold/merit_order.py` do not exist; `gold/` holds `base.py`, `registry.py`, `system_marginal_price.py`, `views/`.
- Missing real modules: `connectors/neso_data_portal/`, `schemas/neso.py`, `schemas/weather.py`, `pipeline/runner.py`, `silver/latest_views.py`, `utils/retry.py`, `gold/registry.py`, `config/`.
- `cli.py` "ingest · transform · build · init · run": no `run` verb (it is `pipeline`); missing backfill, export-csv, status, quality, reset, prune (`cli.py:185-1209`).
- `connectors/openmeteo/` is right as a folder, but the source name is `open_meteo` (`config/sources.yaml:146`); `neso/` is NESO carbon intensity only.
- BaseConnector "Manages the httpx client lifecycle and rate-limiting semaphore": correct (`connectors/base.py:110-146`).
- BaseSilverTransformer "run(date) calls read_bronze() → transform() → _write_silver()": correct names (`silver/base.py:837, 843, 936, 2610`), though run() also validates, adds bitemporal columns and dedups.
- GridflowClient methods `get_system_prices`, `get_fuel_generation`, `get_gas_storage` exist (`serving/client.py:152, 251, 270`); also `get_gb_day_ahead_benchmark`, `get_weather`, `get_imbalance_context`, `query`.

Fine: `connectors/base.py`, `registry.py`; `bronze/writer.py`; `storage/duckdb.py`, `parquet.py`, `paths.py`; `quality/checks.py` five checks (`quality/checks.py:23-171`) and `reporter.py` writing `quality_reports`; `observability.py` PipelineRunTracker and watermarks (`observability.py:63, 236`); `schemas/common.py` BaseSchema/TimestampMixin/SettlementPeriodMixin (`schemas/common.py:10-29`); `data/` default root (`config/settings.py:97-99`).

Site rules: hard-coded counts; "→" arrows.

Verdict: KEEP WITH FIXES. A recruiter-useful map; remove the two phantom files and all counts, add the missing modules.

## Missing (code-supported, what an energy-trading data-science reader expects)
1. Vintages and as-of reads: the base transformer stamps every silver row with `available_at`, `source_run_id` and `dataset_version` (`silver/base.py:2180-2200`), with `available_at = coalesce(published_at, ingest time)` where the vendor publishes a vintage (`silver/base.py:2092-2100`); append-only datasets keep every revision, and `_latest` views pick the winner (`silver/latest_views.py:94-107`, `storage/duckdb.py:186`). This is the revision-aware story traders care about, and the page misdescribes it.
2. Per-dataset publication-lag policies: `VintagePolicy` declares, with a dated rule and a named assumption, when a value could have been known if the vendor gives no publication time (`silver/elexon/system_prices.py:48-61`). Describe the mechanism only; do not print the lag figure, which the code itself labels an unverified assumption. Relevant to leakage-free backtests.
3. Run tracking and watermarks: `pipeline_runs`, `pipeline_watermarks`, `quality_reports` tables (`storage/duckdb.py:106, 124, 134`) and `PipelineRunTracker` (`observability.py:63`), plus the `quality` verb (`cli.py:677`).
4. The three real cross-source gold views: `gold_uk_imbalance_context` (system prices + carbon intensity), `gold_gb_day_ahead_benchmark` (Elexon MID APXMIDP), `gold_eu_gas_storage` (`gold/views/*.sql`, registered `storage/duckdb.py:465`).
5. What gridflow deliberately does not do: no scheduler, server, cloud or live feed; every run is a CLI call (TOPPAGES (b) "does NOT do"; `schedule:` keys in `config/sources.yaml` unused). One honest scope line reads as senior judgement.
