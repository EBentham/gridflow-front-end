# Top pages fact pack — data sources, architecture, models (v5 Phase 27)

Built 2026-09-27 ~00:20 UTC by reading code and data directly. Machine-readable twin: `toppages.json`
(full dataset lists, per-dataset silver windows, chart arrays). Every fact below comes from gridflow code,
local data, the canonical vault, or gridflow_models code, cards or gold, never from the current site.

**Snapshot warning.** Another agent was writing local silver while this was built (for example,
`elexon/agws` gained 2021–2026 history between two of my scans). Silver counts and windows are a
snapshot. `DATA-MATRIX.json` and `PROPOSALS.md` did not exist in `.planning/v5/` when checked
(00:15 UTC), so counts here are my own and Phase 22's will supersede them.

## Rules for designers (apply to all three pages)

1. **Never hard-code a dataset count.** The headline number will change after the page-set ruling
   (D4 drops non-ingested stubs, D5 folds near-duplicate variants into families). Use a slot such
   as `{n} datasets`.
2. **Nothing "planned", "coming soon", "trained", "shipped" or "live".** Describe what exists.
   Charts must name dataset, unit and window.
3. **gridflow is Apache-2.0** (its `LICENSE`). The site's MIT licence is the site's own. Do not print
   MIT on the pipeline page.
4. **Omit version numbers** for gridflow. `pyproject.toml` says 0.16.0 while the vault cites v0.18 to
   v0.21 work, so no version is safe to print.
5. **No GB prices from ENTSO-E.** Local ENTSO-E day-ahead silver has no GB rows. The GB day-ahead
   benchmark is Elexon MID (APXMIDP).
6. **FUELHH has no solar.** Zero SOLAR rows from 2021-08-31 to 2026-09-26 (fuel types present:
   BIOMASS, CCGT, COAL, NPSHYD, NUCLEAR, OCGT, OIL, OTHER, PS, WIND, 11 interconnector codes INT*).
   GB solar outturn is in NESO Data Portal `historic_generation_mix`.

---

## (a) Data sources: landing and vendor hubs

gridflow registers **8 source keys** for **7 vendors** (GIE has two keys). The README's "7 public
APIs" table omits `neso_data_portal`.
Registry: `src/gridflow/connectors/registry.py`. Each connector self-registers (lines below).
Config: `config/sources.yaml`.

### Counts as documented now (all will change after the page-set ruling)

| Vendor (hub slug) | Configured in gridflow | Vault notes | Pages on current site | Local silver |
|---|---:|---:|---:|---:|
| Elexon (`elexon`) | 33 | 33 | 33 | 33 |
| ENTSO-E (`entsoe`) | 47 | 49 | 49 | 31 |
| ENTSO-G (`entsog`) | 33 | 33 | 33 | 25 |
| GIE (`gie`: `gie_agsi` 7 + `gie_alsi` 1) | 8 | 8 | 8 | 4 |
| NESO Carbon Intensity (`neso`) | 33 | 33 | 33 | 24 |
| NESO Data Portal (`neso_data_portal`) | 3 | 3 | **32** | 3 |
| Open-Meteo (`openmeteo`) | 6 | 6 | 6 | 6 |
| **Total** | **163** | **165** | **194** | **126** |

The current headline "165 datasets" counts vault notes. MILESTONE.md measured 125 with local silver.
I measure 126 (NESO 24): one more than MILESTONE, which dataset differs is unverified.

### Vendor cards

**Elexon BMRS (Insights API)**
- Publishes: GB balancing-mechanism data, including system prices, generation outturn, BM-unit data,
  and demand and wind forecasts (vault README).
- Market: GB electricity. Auth: **no**. `api_key_env ''`; vault: HTTP 200 with no key, verified 2026-05-08.
- Base URL `https://data.elexon.co.uk/bmrs/api/v1`. Connector `src/gridflow/connectors/elexon/client.py:377`,
  registry `endpoints.py:56` (`ENDPOINTS`).
- Grain: half-hourly settlement periods, 1..50 per day (46 or 50 on clock-change days). FUELINST is
  5-minute. Some datasets are daily publications or 2–14-day-ahead forecasts.
- History evidenced locally: `fuelhh`, `indo`, `mid`, `system_prices`, `windfor` and `agws` run from
  2021-08-31/09-01 to 2026-09. The other 27 hold data from about 2026-08-01 (`nonbm` has 5 rows;
  `bmunits_reference` is one snapshot). The vault does not state vendor-side depth.
- Representative: `system_prices` (single imbalance price per period: SSP = SBP on all 88,694 latest-vintage rows, 2021-09-01 to 2026-09-22) ·
  `fuelhh` (half-hourly outturn by fuel, no solar) · `indo` (initial national demand outturn; the demand
  model's target) · `mid` (market index; its APXMIDP provider is the GB day-ahead benchmark) ·
  `remit` (outage and unavailability messages).

**ENTSO-E Transparency Platform**
- Publishes: EU electricity day-ahead prices, load, generation per type, cross-border flows, outages,
  capacity, transmission allocation and balancing (vault README).
- Market: EU electricity. Configured zones `GB, FR, NL, BE, DE-LU, IE-SEM`; control area `GB`
  (`endpoints.py` `DEFAULT_ZONES`, `DEFAULT_CONTROL_AREAS`).
- Auth: **yes**. `ENTSOE_API_KEY`, sent as the `securityToken` query parameter.
- Base URL `https://web-api.tp.entsoe.eu`. Connector `connectors/entsoe/client.py:585`, registry
  `endpoints.py` `DOC_TYPES`. Responses are XML.
- Grain: local `day_ahead_prices` has 15-minute rows for DE-LU, BE, FR and NL and hourly rows for
  IE-SEM, with **no GB rows**. The vault README says "most operational EU data items no longer publish
  for the GB control area".
- History: vault README gives vendor depth as "about 5 years on most datasets". Local silver mostly
  starts 2026-08-01. Outage datasets carry event times from 2015 to 2077 because they describe
  planned windows, so do not read those as history.
- Representative: `day_ahead_prices` (EUR/MWh by bidding zone) · `actual_generation` (per production
  type) · `actual_load` · `cross_border_flows` (physical) · `wind_solar_forecast` (day-ahead).

**ENTSO-G Transparency Platform**
- Publishes: EU gas physical flows, nominations, allocations, capacities, gas quality, CMP outcomes,
  interruptions, tariffs, urgent market messages and reference inventory (vault README).
- Market: EU gas. Default point directions are UK TSO interconnection points
  (e.g. `UK-TSO-0001ITP-00005exit`). Auth: **no**.
- Base URL `https://transparency.entsog.eu/api/v1`. Connector `connectors/entsog/client.py:174`,
  `endpoints.py` `ENDPOINTS`.
- Grain: daily (`periodType: day`, gas day). Tariff and CMP data are periodic.
- History: local silver from 2026-07-31 (tariffs from 2025-10-01). The vault does not state vendor
  depth.
- Representative: `physical_flows` · `nominations` · `firm_technical` (capacity) · `gcv` (gross
  calorific value) · `tariffs` (country UK).

**GIE: AGSI+ (storage) and ALSI (LNG)**
- Publishes: EU underground gas storage levels and flows (AGSI+) and LNG terminal data (ALSI).
- Market: EU gas storage (AT BE DE ES FR GB IT NL PL) and LNG (BE ES FR GB IT NL PL PT).
- Auth: **yes**. `GIE_API_KEY` in the lowercase `x-key` header; one key serves both APIs.
- Base URLs `https://agsi.gie.eu`, `https://alsi.gie.eu`. Connector `connectors/gie/client.py:443-444`.
- Grain: daily (gas day). Local silver from 2026-08-01.
- Representative: `storage` (country-day levels; feeds `gold_eu_gas_storage`) · `storage_reports` ·
  `unavailability` · `lng` (ALSI).

**NESO Carbon Intensity API**
- Publishes: GB national and regional carbon intensity (actual and forecast), statistics, fuel
  emission factors and generation mix (vault README).
- Market: GB electricity carbon intensity. Auth: **no**. Base URL `https://api.carbonintensity.org.uk`.
- Connector `connectors/neso/carbon_intensity.py:180`, `endpoints.py` `ENDPOINTS`.
- Grain: half-hourly. Local windows are short, at most 2026-07-30 to 2026-09-21; many variants hold
  1–5 days.
- The vault groups the 33 route variants into 5 families: intensity (national), factors, stats,
  generation, regional. (the vault README table carries a Family column with these five values).
- Representative: `carbon_intensity` (national, date range) · `regional_intensity` (all regions) ·
  `generation` (national mix) · `intensity_factors` (fuel emission factors) · `intensity_fw48h`
  (48-hour forecast).

**NESO Open Data Portal (CKAN)**
- Publishes: NESO's open-data catalogue. It is a file-download API (CKAN metadata plus CSV resources),
  not a query API. gridflow implements **3** of its packages.
- Market: GB electricity (system operator data). Auth: **no**. Base URL `https://api.neso.energy`.
- Connector `connectors/neso_data_portal/client.py:1492`, `endpoints.py` `DATASETS`.
- History: `historic_generation_mix` silver spans **2009-01-01 to 2026-09-26** (verified). The portal
  serves only its current file, so backfill and historical windows are refused by design.
- Datasets: `historic_generation_mix` (half-hourly GB mix by fuel since 2009, including SOLAR and
  embedded wind) · `embedded_wind_solar_forecast` (embedded wind and solar forecast per settlement
  period) · `daily_wind_availability` (daily MW per BM unit).

**Open-Meteo**
- Publishes: weather, as ERA5 archive (`historical_*`) and NWP forecast (`forecast_*`), for three
  role-keyed location lists (vault README).
- Market: weather inputs for GB power modelling. Auth: **no** (free tier).
- Base URLs `https://archive-api.open-meteo.com/v1` and `https://api.open-meteo.com/v1`.
  Connector `connectors/openmeteo/client.py:152`.
- Locations (code): demand has 7 cities (london, birmingham, manchester, leeds, glasgow, cardiff,
  belfast). Wind has 12 sites (dogger_bank, hornsea, east_anglia, triton_knoll, walney, gwynt_y_mor,
  beatrice, seagreen, highland_central, borders_crystalrig, whitelee, pen_y_cymoedd). Solar has
  6 sites (east_anglia_norfolk, wiltshire_somerset, kent, cornwall, sussex, oxfordshire).
- Grain: hourly. History: `historical_*` silver runs from 2021-09-01 to 2026-09-22/26.
- Datasets: `historical_demand` · `historical_wind` (10 m and 100 m wind) · `historical_solar`
  (GHI/DNI/DHI/GTI) · `forecast_demand` · `forecast_wind` · `forecast_solar`.

**Cadence.** `schedule:` values in `sources.yaml` (hourly, daily and so on) are declared at
`config/settings.py:60` and read nowhere else in `src/`. No scheduler exists. Describe cadence as the
vendor's publication grain (above), never as "updated hourly".

### Must NOT appear in any design

- **29 NESO Data Portal stub pages** that `build_dataset_stubs_from_landings` manufactures (no
  connector, no silver): aahedc_tariffs, bsuos_fixed_tariffs, constraint_cost_forecast_24_months_ahead,
  contract_transfer_of_obligation, country_carbon_intensity_forecast, daily_opmr,
  day_ahead_half_hourly_demand_forecast_performance, demand_profile_dates,
  dynamic_moderation_requirements, dynamic_regulation_requirements, embedded_register,
  gb_system_inertia_bid_and_offer_costs, interconnector_register,
  long_term_2_52_weeks_ahead_national_demand_forecast, long_term_forecasts_for_dc_dm_dr_requirements,
  obp_non_bm_physical_notifications, obp_non_bm_reserve_instructions,
  obp_reserve_availability_utilisation_price, operational_transparency_forum_network_congestion_data,
  quick_reserve_auction_requirement_forecast,
  short_term_operating_reserve_stor_day_ahead_auction_results, slow_reserve_requirement_forecast,
  stability_midterm_y_1_utilisation_report, static_firm_frequency_response_requirement, stor_windows,
  transmission_entry_capacity_tec_register, upcoming_trades, weekly_opmr, weekly_wind_availability.
  The current NDP hub marks them `planned-card`.
- **ENTSO-E `activated_balancing_qty`**: a silver transformer only, not in `DOC_TYPES` or
  `sources.yaml`, so the CLI never fetches it. **ENTSO-E `commercial_schedules_net_positions`**: deprecated,
  removed in gridflow V2 (ADR-019). Both are rendered pages today.
- **GIE `news`, `news_item`**: `implementation_phase='deferred'` in `gie/endpoints.py`, with no silver.
- **Elexon endpoints excluded in code** (`EXCLUDED_ENDPOINTS`): `bod` (unstable),
  `generation_by_fuel` (duplicate of fuelhh), `indicative_imbalance_volumes` (removed by Elexon).

### Configured, connector-wired, but no local silver (Phase 22 decides; not classified here)

ENTSO-E 16: outages_offshore_grid, redispatching_cross_border, countertrading,
congestion_management_costs, offered_transfer_capacity_{continuous,implicit,explicit},
transfer_capacity_use, congestion_income, imbalance_prices, imbalance_volume,
activated_balancing_prices, contracted_reserves, aggregated_balancing_energy_bids,
cross_zonal_balancing_capacity, balancing_financial_expenses_income.
ENTSO-G 8: interruptions, urgent_market_messages, connection_points, operators, balancing_zones,
operator_point_directions, interconnections, aggregate_interconnections.
NESO 9: intensity_current, intensity_today, generation_current, regional_current,
regional_{england,scotland,wales}, regional_postcode, regional_regionid.
GIE 2: about_summary, about_listing.
Designs should use a generic dataset-row component and never feature these by name.

### Elexon hub: full list (33), grouped as the vault groups them

The vault's only grouping is `30-vendors/elexon/endpoints.md`, which groups by **API parameter style**.
Dataset notes have no category field. The current site's Generation / Prices & Balancing / Demand &
Forecasts / System & Reference grouping is site-authored. A **PROPOSED** thematic grouping (mine, not
canonical) follows the list. One-liners are the code's `ElexonEndpoint.description`. "2021→" means local
silver from 2021-08-31/09-01; otherwise local silver starts about 2026-08.

*Settlement-date style (7)*
| Key | API path | One line | Local |
|---|---|---|---|
| system_prices | /balancing/settlement/system-prices/{date} | System Sell Price and System Buy Price per settlement period | 2021→ |
| market_depth | /balancing/settlement/market-depth/{date} | Settlement market depth per settlement period | 2026-08→ |
| pn | /datasets/PN | Physical Notifications (per BM unit, per period) | 2026-08→ |
| boal | /datasets/BOALF | Bid/Offer Acceptance Levels (BOALF; replaces deprecated BOAL) | 2026-08→ |
| disbsad | /datasets/DISBSAD | Disaggregated Balancing Services Adjustment Data | 2026-08→ |
| mid | /datasets/MID | Market Index Data | 2021→ |
| netbsad | /datasets/NETBSAD | Net Balancing Services Adjustment Data | 2026-08→ |

The vault lists boal, disbsad, mid and netbsad here, but their code `ParamStyle` is `PUBLISH_DATETIME`
with `from`/`to` params. The vault's own table says so.

*Publish-datetime style (25)*
| Key | Code | One line | Local |
|---|---|---|---|
| freq | FREQ | System frequency | 2026-08→ |
| fuelhh | FUELHH | Half-hourly generation outturn by fuel type (no solar) | 2021→ |
| fuelinst | FUELINST | Instantaneous generation outturn by fuel type | 2026-08→ |
| imbalngc | IMBALNGC | Indicated imbalance | 2026-08→ |
| ndf | NDF | National Demand Forecast (day-ahead) | 2026-08→ |
| ndfd | NDFD | National Demand Forecast (2–14 days ahead) | 2026-08→ |
| melngc | MELNGC | Indicated margin | 2026-08→ |
| fou2t14d | FOU2T14D | 2–14 day-ahead generation availability by fuel type | 2026-08→ |
| uou2t14d | UOU2T14D | 2–14 day-ahead generation availability by BM unit | 2026-08→ |
| windfor | WINDFOR | Wind generation forecast | 2021→ |
| temp | TEMP | Temperature data | 2026-08→ |
| agpt | AGPT | Actual aggregated generation per type (B1620) | 2026-08→ |
| agws | AGWS | Actual or estimated wind and solar generation (B1630) | 2021→ |
| atl | ATL | Actual total load per bidding zone (B0610) | 2026-08→ |
| indo | INDO | Initial National Demand Outturn | 2021→ |
| itsdo | ITSDO | Initial Transmission System Demand Outturn | 2026-08→ |
| indod | INDOD | Initial National Demand Outturn (daily total) | 2026-08→ |
| nonbm | NONBM | Non-BM STOR generation | 5 rows |
| inddem | INDDEM | Day and day-ahead indicated demand | 2026-08→ |
| indgen | INDGEN | Day and day-ahead indicated generation | 2026-08→ |
| tsdf | TSDF | Transmission System Demand Forecast | 2026-08→ |
| tsdfd | TSDFD | 2–14 day-ahead Transmission System Demand Forecast | 2026-08→ |
| lolpdrm | LOLPDRM | Loss of Load Probability and De-rated Margin | 2026-08→ |
| remit | REMIT | REMIT outage and unavailability messages | 2026-08→ |
| soso | SOSO | SO-SO prices (cross-border interconnector trading) | 2026-08→ |

*No params (reference data) (1)*
| bmunits_reference | /reference/bmunits/all | All BM unit reference data | snapshot |
|---|---|---|---|

PROPOSED themes (pack-assigned, needs owner OK): **Prices and balancing** (system_prices,
market_depth, mid, boal, pn, disbsad, netbsad, soso) · **Generation and availability** (fuelhh,
fuelinst, agpt, agws, windfor, fou2t14d, uou2t14d, nonbm) · **Demand** (indo, itsdo, indod, atl, ndf,
ndfd, tsdf, tsdfd, inddem) · **System indicators** (indgen, imbalngc, melngc, lolpdrm, freq, temp) ·
**Reference and messages** (bmunits_reference, remit).

---

## (b) Architecture

gridflow is a local-first Python pipeline: Polars, DuckDB, Pydantic v2, httpx and Typer. It has no
server. The data root is configurable (`GRIDFLOW_DATA_DIR`, `GRIDFLOW_DUCKDB_PATH`); this machine uses
`C:\gridflow-data`. Paths come from `src/gridflow/storage/paths.py` (`PathBuilder`).

### Layers

| Layer | Stored as | Path and naming (exact) | Refs |
|---|---|---|---|
| **Bronze** | Raw response bytes, `.json` / `.xml` / `.csv` / `.bin` by content type, plus a `.meta.json` sidecar. Written once, never rewritten. | `bronze/{source}/{dataset}/{YYYY}/{MM}/{DD}/raw_{fetched_at:%Y%m%dT%H%M%SZ}_{sha256[:8]}.{ext}`. Partition = data date when known, else fetch date. | `bronze/writer.py:38-48, 57, 85`; `paths.py:23-38` |
| **Silver** | Parquet, zstd by default. Typed, Pydantic-validated per row, deduplicated, UTC. | `silver/{source}/{dataset}/year={YYYY}/month={MM}/{dataset}_{YYYYMMDD}.parquet` | `paths.py:50-73`; `storage/parquet.py:38` |
| Silver, append-only | Same, plus a vintage suffix so every capture is kept | `{dataset}_{YYYYMMDD}_run{available_at ISO}.parquet`, only for elexon `system_prices`, `remit`, `fou2t14d` and NDP's 3 datasets | `silver/base.py:2635`; each transformer's `APPEND_ONLY = True` |
| **Gold (gridflow)** | Parquet from one Python builder, `system_marginal_price` (latest-vintage system prices plus spread, absolute imbalance, calendar features); plus 3 SQL views | `gold/{name}/year={YYYY}/{name}_{YYYYMMDD}.parquet` | `gold/system_marginal_price.py:26`; `paths.py:96-101` |
| **Gold (gridflow_models outputs)** | Parquet written by the models repo into the same root: `forecasts`, `forecast_metrics`, `stack_clearing`, `stack_residual_demand`, `stack_supply_curve_points` | `gold/{table}/model_slug={slug}/{prefix}_{YYYYMMDDTHHMMSSZ}_{run_id}.parquet` | on disk |

Two facts the old README gets wrong. First, **no gridflow-built gold exists locally**: the only gold on
disk is gridflow_models output, and `system_marginal_price` has never been built here. Second, the
README's silver filename omits the `_run…` suffix used by append-only datasets.

Bronze sidecar fields (`writer.py:67-84`): source, dataset, fetched_at, written_at, data_date,
request_url and request_params (credentials masked), api_version, http_status, content_type,
body_sha256, body_size_bytes, page, total_pages.

Silver columns: `event_time` is present on all 126 local silver datasets (checked); `available_at`, `published_at`,
`ingested_at`, `source_run_id`, `dataset_version` appear on the datasets sampled (fuelhh, system_prices, entsoe day_ahead_prices). `available_at` supports point-in-time
("as-of") reads downstream.

### Transforms between layers

- **API → bronze** (`gridflow ingest`): async per-source connectors (`connectors/<source>/client.py`)
  with rate limits and retries per `sources.yaml` (for example Elexon 2 req/s, ENTSO-E 1 req/s).
  `BronzeWriter.write` stores body then sidecar, each via temp file and `os.replace`.
- **Bronze → silver** (`gridflow transform`): one `BaseSilverTransformer` per (source, dataset), 164
  registered (`silver/registry.py`; entsoe 48, elexon 33, entsog 33, neso 33, gie_agsi 7,
  open_meteo 6, neso_data_portal 3, gie_alsi 1). `run()` (`silver/base.py:936`) reads that date's
  bronze, parses, validates each row against the Pydantic schema (`schemas/*.py`; `base.py:2046`),
  normalises time to UTC, deduplicates on the dataset key (`base.py:1337`) and writes Parquet
  atomically.
- **Silver → gold** (`gridflow build`): registered builders (`gold/registry.py`; only
  `system_marginal_price`). The three SQL views register on `init`.
- **Latest vintage**: for append-only datasets, `silver/latest_views.py:94` (`LATEST_VIEW_SPECS`)
  defines the business key and precedence. It is rendered as a `_latest` DuckDB view and, for Python,
  as `select_latest_vintage`.

### DuckDB catalogue (`{data_root}/gridflow.duckdb`)

- Tables: `pipeline_runs`, `pipeline_watermarks`, `quality_reports` (`storage/duckdb.py:106, 124, 134`).
- Views (`storage/duckdb.py:161-209`, re-registered by `gridflow init`):
  - `silver_{source}_{dataset}` for each silver directory (line 179).
  - `silver_{source}_{dataset}_latest` for the 6 append-only datasets (line 186).
  - `silver_{dataset}`: a deprecated alias, skipped when two sources share a name (line 265).
  - `gold_{dir}` for each gold directory (line 207).
  - SQL views from `gold/views/*.sql` (line 465): `gold_uk_imbalance_context` (Elexon system prices +
    NESO carbon intensity, half-hourly), `gold_gb_day_ahead_benchmark` (Elexon MID APXMIDP, GBP/MWh)
    and `gold_eu_gas_storage` (GIE AGSI+ by country and day).
- Observed 2026-09-27: 269 relations. That is 258 `silver_*` views, 8 `gold_*` views and 3 tables.

### CLI verbs (`gridflow = gridflow.cli:app`, `pyproject.toml:34`)

`init` (cli.py:1209) · `ingest` (186) · `transform` (261) · `build` (306) · `pipeline` (485: ingest →
transform, → build with `--gold`) · `backfill` (346, chunked) · `export-csv` (438) · `status` (584) ·
`quality` (677) · `reset` (796) · `prune` (972). Quality checks (`quality/checks.py`): null_rate,
time_series_gaps, range_check, row_count, duplicates. Read-only query client:
`gridflow.serving.client.GridflowClient`.

### What gridflow does NOT do (do not imply it)

- No scheduler or orchestrator. Every run is a CLI invocation; `schedule:` in config is unused.
- No cloud, object store, warehouse, streaming, cluster or multi-tenancy (vault architecture "Out of
  scope"). No server, no public API, no hosted database.
- No live feed. Data lands when someone runs `ingest`, so there are no freshness badges.
- No ENTSO-E GB day-ahead prices. No NESO Data Portal backfill. Only 3 NESO Data Portal packages.
- No models, forecasts or trading. Those live in gridflow_models, which "does not produce orders"
  (vault gridflow-models README).

### This site's build and gates (if the page covers them)

- `gridflow-build` renders the vault mirror `.md` to `site/hifi/data-sources/` (Jinja2).
  `gridflow-build --check` checks idempotence. `gridflow-staleness-check` checks authored pages.
  `gridflow-drift-check` calls live vendor APIs and runs only on the owner's yes.
- `.github/workflows/ci.yml` runs on **pull_request** and push to main: staleness check, baseline
  ratchet, `gridflow-build --check`.
- `deploy.yml` runs on push to main (and manual dispatch): build, `--check`, htmlhint, lychee, then
  GitHub Pages.
- gridflow's own CI runs on push and pull_request: `uv lock --check`, ruff check and format, mypy,
  `pytest -m "not live"`.
- v5 adds: impeccable detector `[]`, AA contrast, no horizontal overflow at 390 px (MILESTONE.md).

---

## (c) Models landing: five models

Repo `gridflow_models`, a separate library that reads gridflow's DuckDB and Parquet. Status source
per MILESTONE is `notebooks/README.md`. **That README (last edited 2026-05-31) says wind and solar are
"trained", but the manifest, gold store and 2026-09-01 model cards show they have never been trained.**
Render the "What exists" column. The README wording is quoted only for provenance. See `toppages.json` → `report`.

| Model | model_id | Target (exact) | Method | Horizon | README says (verbatim) | What exists (neutral) |
|---|---|---|---|---|---|---|
| Day-ahead demand | `day_ahead.lgbm_demand.v1` (+ `.v2`) | GB national demand outturn, half-hourly, MW (`elexon/indo`, `initial_demand_outturn_mw`) | LightGBM quantile regression, one model per quantile (0.05 … 0.95); monotone sorted output; conformal (CQR) outer band. v2 adds weather + calendar | 24h ahead | "trained; full lifecycle: backfill → build gold → train/load → inspect" | 21 v1 and 1 v2 manifest versions (`validated`); walk-forward backtests in gold; one live issued v2 forecast (2026-09-04/06) |
| Wind | `wind.lgbm_quantile.v1` | GB wind outturn, half-hourly, MW (`elexon/fuelhh` WIND) | LightGBM quantile, 12-site weather; benchmark WINDFOR | 24h ahead | "trained; parallel sections" | Configured, with model card and training dataset file; no manifest entry, forecasts or metrics |
| Solar | `solar.lgbm_quantile.v1` | Configured as `elexon/fuelhh` SOLAR, which is empty; successor target `neso_data_portal/historic_generation_mix.solar` authorised, not yet configured | LightGBM quantile, 6-site weather; benchmark persistence | 24h ahead | "trained; parallel sections" | Configured, with model card; no manifest entry, forecasts or metrics; configured target has no rows |
| GB merit-order stack | `stack.gb.v1` | GB supply curve at a settlement period (units by short-run marginal cost, cumulative MW, GBP/MWh, floor −500) | Constructive: bmunits_reference inventory, REMIT availability (FOU2T14D derating), manual commodity prices, plant-technology config | Point in time (`as_of`, target period) | "constructive; … No gold or training sections." | Builds on demand; supply-curve points published in gold as part of SMP runs |
| Fundamentals SMP | `fundamentals_smp.gb.v1` | GB day-ahead system marginal price, half-hourly, GBP/MWh; scored against `elexon/mid` APXMIDP | Hybrid composite: stack cleared against realised residual demand (INDO − wind − solar − signed netting), perfect-prognosis policy | Day-ahead, half-hourly | "hybrid; loads four component models from the manifest …" | Published headline and diagnostic backtests in `gold_stack_*` |

Demand is one model with two registered versions. That keeps "five models" honest. Workbench handles
include `models.demand_forecast_v2`.

### Metrics that exist (only these may be shown)

Definitions from code (`gridflow_models/validation/metrics.py`):
- **Pinball q0.5** is the mean quantile loss at 0.5. It equals half the MAE of the median forecast.
  Unit: MW. Do not label it "MAE".
- **coverage_90** is the share of actuals inside [q0.05, q0.95], inclusive.
- **Gates**: pinball q0.5 ≤ 1500; coverage within 0.90 ± 0.05; zero quantile crossings.

| Model | Run | Window | Metric | Source |
|---|---|---|---|---|
| Demand v1 | `a55a829bc51c40b2` | 12 × 30-day walk-forward folds, 2024-09-01 → 2026-08-22, 17,279 half-hours; 1095-day rolling training window | pinball q0.5 **711.04 MW**, coverage_90 **0.893**, 0 crossings, all gates pass | gold `forecast_metrics` (scope=run) = card v1 "headline" |
| Demand v2 | `b367a742aa544f8f` | same folds | pinball q0.5 **599.72 MW**, coverage_90 **0.883**, gates pass | gold + card v2. **Perfect-prognosis**: actual ERA5 weather used as if forecast, so the score is optimistic. The card calls the 15.7% gain an upper bound, from one run with no significance claim. |
| Fundamentals SMP | `41de423cfc0b421e` (policy `smp_headline_perfect_prog_v2`) | 2026-08-18 → 2026-09-03, 816 periods | mean bias **−151.80 GBP/MWh**, MAE **151.80** (every period under-predicts) | card "v2.0 published headline", reproduced from gold |
| Fundamentals SMP diagnostic | 13 monthly runs | 2025-05-05 → 2026-05-04, 17,520 periods | mean bias −69.81, MAE 72.84 GBP/MWh | card |
| Wind, solar, stack | none | none | No metric exists. Show none. | none |

SMP captions must say: perfect-prognosis; **fuel and carbon prices synthetic** (card: "synthetic
(35e4d8d, seed 20240507)"); APXMIDP mixes day-ahead and intraday trades; the −500 GBP/MWh floor
(vault: ~46% of the v1.9 bias came from the 12% of periods where clearing hit the floor).
Older demand runs in gold (808.04, 669.25, 714.15) are superseded or retired. Do not quote them.

### Workbench calls (from code, `src/gridflow_models/research/handles/`)

```python
from gridflow_models import setup_notebook
data, models, common = setup_notebook()

data.elexon.system_prices(start, end)        # per-source client; 8 sources from gridflow config
data.list_data_sources(); data.list_tables(); data.list_freshness(); data.sql("…")
data.gb_day_ahead_benchmark(start, end)      # cross-source reader (Elexon MID APXMIDP)
models.list()                                # model_id, family, version, status, last_trained
models.demand_forecast.predict(...)          # also train / validate / show_folds / predictions / model_card
models.stack.build(as_of); models.stack.clear(as_of, demand_mw)
models.fundamentals_smp.backtest(...)        # also assemble / components / predictions
common.datetime(2026, 8, 1, tzinfo=common.utc); common.pl
```

References: `data.py:94` (Data; top-level verbs `list_data_sources`, `list_tables`, `list_freshness`,
`sql`, `refresh_all`, `training_set` at 55-62). `source.py:188-491` (list_datasets, refresh,
describe, backfill, query, tail, coverage). `models.py` (one client per `configs/models/**/*.yaml` by
`workbench_nature`: predictive, stack or smp). `model.py:300-1647` (client verbs). `common.py:37`.
Attribute names: `demand_forecast`, `demand_forecast_v2`, `wind_forecast`, `solar_forecast`, `stack`,
`fundamentals_smp`. Notebooks are call sites only: "no model logic in notebooks" (README).

---

## Chart series (arrays in `toppages.json` → `series`)

| Page | Series | Dataset · unit · window | Points |
|---|---|---|---:|
| Data-sources landing | GB system price, daily mean | `elexon/system_prices` silver, latest vintage per period (run_type is null on every row, so selection falls to available_at DESC), mean of 48 periods · GBP/MWh · 2026-05-26 → 2026-09-22 | 120 |
| Elexon hub | GB transmission-metered wind, monthly mean | `elexon/fuelhh` WIND `generation_mw`, deduped on (date, period, fuel) · MW · 2021-09 → 2026-08 | 60 |
| Architecture | **None recommended.** Schematics carry no numbers. If a figure is wanted, use the counts above as a table. | none | 0 |
| Models landing | Demand v1 forecast band vs outturn | gold `forecasts` run `a55a829bc51c40b2` (fold 12): actual, q0.05, q0.5, q0.95 · MW · 2026-08-20T00:00Z → 2026-08-21T23:30Z | 96 |
| Models landing (alt) | Demand v1 pinball q0.5 per fold | gold `forecast_metrics` scope=fold · MW · 12 folds, 2024-09 → 2026-08 | 12 |
| Models landing (SMP) | SMP clearing vs APXMIDP, daily mean | `gold_stack_clearing` run `41de423cfc0b421e` ⋈ `gold_gb_day_ahead_benchmark` · GBP/MWh · 2026-08-18 → 09-03 (caption the perfect-prog and synthetic-fuel caveats) | 17 |

Other vendor hubs: no series computed. Local silver for ENTSO-E, ENTSO-G, GIE and NESO is ≤ 8 weeks
deep. Open-Meteo `historical_*` (2021 →) and NESO Data Portal `historic_generation_mix` (2009 →)
could support hub charts if wanted.
