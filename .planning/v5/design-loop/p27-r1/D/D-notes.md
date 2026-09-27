claude-opus-5-5

# D, "From the workbench": Phase 27 round 1 notes

## Boards (root height = `$preview`, 1440 wide)

- `p27\D\D-data-sources.dc.html`: 2154 px
- `p27\D\D-vendor-elexon.dc.html`: 2805 px
- `p27\D\D-architecture.dc.html`: 3394 px
- `p27\D\D-models.dc.html`: 2658 px

The generator is `gen_d.py`, run with the gridflow_models venv. It exec's the locked homepage generator `r3-7/gen_a.py` read-only for its pieces, patterns and CSS. `heights.json` holds the measured heights and `static\` holds the detector copies.

## The one idea

Each page opens the gridflow-models notebook at the cell a practitioner would run first on that subject, and sets the plain-English account beside it. The handle names are shared: the mono petrol `data.elexon` in a card row is the same mark as the one under the vendor's entry, so the prose column works on its own for a non-coder.

## Content model (top to bottom)

- **Data sources:**
  1. Sky: nav, h1, lede with `[N datasets]`, and a strip with the four fed assets (substation, met mast, interconnector, gas terminal).
  2. Thin topsoil.
  3. Bronze. Left: h2, intro, then seven vendor entries (h3, handle, description, fact line with `[n]`). Right: notebook with `[1]` setup and `[2]` `data`, which renders the real 17-row card; below it, "Finding a dataset".
  4. Deep footer.
- **Elexon hub:**
  1. Sky: breadcrumb, h1, lede with `[n]`, and a strip with the gas-fired power station, pylons, substation and battery storage.
  2. Thin topsoil.
  3. Bronze. Left: h2, a key note, and the 33 datasets in five themed table lists. Right: notebook with `[2]` the `data.elexon` card, `[3]` a FUELHH query and `[4]` a monthly wind plot; then the caption and "The feed" facts.
  4. Deep footer.
- **Architecture:**
  1. Sky: h1, a two-paragraph lede, and a strip whose substation carries a cable down.
  2. Topsoil: "Follow one dataset down" beside `[1]` setup.
  3. Bronze: prose, the path plate and the sidecar fields beside `[2]` `backfill`.
  4. Silver: prose and the path plate beside `[3]` `data.sql` over `silver_elexon_system_prices_latest`, whose DataFrame shows the pack's daily means for 19 to 22 Sep.
  5. Gold: prose and the three SQL views beside `[4]` `data.imbalance_context`, whose output is its help card.
  6. Deep: the eleven CLI verbs, then quality checks, gates and "Not in gridflow". A joined footer follows.
  7. One cable descends from the substation through every stratum, with a splice at each contact and a tap at each cell.
- **Models:**
  1. Sky: h1, lede, and a strip with the solar farm, onshore and offshore wind and the gas-fired station.
  2. Topsoil. Left: h2 and five model entries (h3, model_id, what it is, a fact line, and a caveat line where one is needed). Right: notebook with `[2]` `print(models)`, `[3]` a `data.sql` over `gold_forecasts` for run a55a829bc51c40b2, and `[4]` a pandas plot of the pack's 96-point band; then the caption.
  3. Gold: the five model-output views beside "How a forecast is scored".
  4. Deep footer.

**How the vendor hub holds for a 3-dataset vendor:** themes appear only when a vendor has enough datasets to need them (about 12 or more). NESO Data Portal would show one ungrouped table list of three rows. The notebook still shows `data.neso_data_portal`, whose card has the same seven verbs. The plot cell appears only when the pack supplies a series for that vendor (`historic_generation_mix` could); otherwise the card stands alone and "The feed" moves up under it.

## New copy, verbatim

### Data sources

- **H1:** Where the data comes from
- **Lede:** gridflow ingests [N datasets] from seven vendors: GB and European electricity, gas, weather and carbon intensity. Five need no API key; ENTSO-E and GIE each need one.
- **H2:** One handle per source
- **Intro:** The catalogue is organised by vendor, and in the gridflow-models notebook each vendor is a handle on data. GIE has two, one for storage and one for LNG, so seven vendors give eight handles. Every handle answers the same seven verbs.
- **Vendor entries** (name / description / fact line):
  - Elexon BMRS / GB balancing-mechanism data: system prices, generation outturn, BM-unit data, and demand and wind forecasts. / [n] datasets, mostly half-hourly settlement periods, no API key
  - ENTSO-E / European electricity: day-ahead prices, load, generation by type, cross-border flows, outages and balancing. / [n] datasets, XML responses, API key required
  - ENTSO-G / European gas: physical flows, nominations, capacities, gas quality and tariffs at interconnection points. / [n] datasets, daily by gas day, no API key
  - GIE AGSI+ and ALSI / EU gas storage levels and flows (AGSI+), and LNG terminal inventory and send-out (ALSI). / [n] datasets, daily by gas day, one API key for both
  - NESO Carbon Intensity / GB national and regional carbon intensity, actual and forecast, with fuel emission factors and the generation mix. / [n] datasets, half-hourly, no API key
  - NESO Data Portal / Files from NESO's open-data catalogue, including the GB generation mix by fuel since 2009, solar included. / [n] datasets, the portal's current file only, no API key
  - Open-Meteo / Weather for GB power modelling: ERA5 archive and forecasts at 7 demand cities, 12 wind sites and 6 solar sites. / [n] datasets, hourly, no API key
- **H3:** Finding a dataset
  - Each vendor page lists its datasets by theme. Each dataset has its own page: what it measures, its grain and units, the silver schema, sample rows and the caveats.
  - A dataset keeps one name throughout. system_prices is the gridflow key, silver_elexon_system_prices is its DuckDB view, and data.elexon.query("system_prices", start, end) reads it in a notebook.
- **Footer (all pages):** An open-source pipeline for UK and European power, gas, weather and carbon data, under the Apache-2.0 licence. The models live in gridflow-models.

### Elexon hub

- **Lede:** GB balancing-mechanism data from Elexon's Insights API: system prices, generation outturn, BM-unit data, and demand and wind forecasts. [n] datasets, and no API key is needed.
- **H2:** Datasets by theme
- **Key note:** Each name is the gridflow key: the page, the silver view silver_elexon_<key> and the notebook call all use it.
- **Themes:** the pack's PROPOSED grouping, which needs owner OK: Prices and balancing, Generation and availability, Demand, System indicators, Reference and messages. The row lines are the pack's one-liners in sentence case. Two carry a small addition: mid ("its APXMIDP provider is the GB day-ahead benchmark") and fuelhh ("(no solar)").
- **Plot caption:** The plot in [4]: monthly mean of the half-hourly wind rows in elexon/fuelhh (generation_mw, MW), September 2021 to August 2026. It is a mean per row, not total output.
- **The feed:**
  - API: https://data.elexon.co.uk/bmrs/api/v1, no key
  - Market: GB electricity
  - Grain: Half-hourly settlement periods, 1 to 50 a day (46 or 50 when the clocks change). FUELINST is instantaneous, every 5 minutes; some datasets are daily publications or 2 to 14-day forecasts.
  - Prices: system_prices carries a single imbalance price: SSP equals SBP on every latest-vintage row from 1 September 2021 to 22 September 2026.
  - Benchmark: The APXMIDP provider in mid is the GB day-ahead benchmark, read through gold_gb_day_ahead_benchmark.
  - Solar: FUELHH has no solar rows. GB solar outturn is in the NESO Data Portal's historic_generation_mix.

### Architecture

- **H1:** Three layers on one machine
- **Lede:**
  - gridflow is a local-first Python pipeline built on Polars, DuckDB, Pydantic and httpx, run from a Typer command line. There is no server, scheduler or cloud: data lands when someone runs a command.
  - This page follows one dataset, Elexon system_prices, from the API response to the view a notebook reads.
- **H2:** Follow one dataset down
  - Each layer below shows where system_prices is stored and the notebook cell that reads it. The cells are one gridflow-models session, run from top to bottom.
- **H2:** Bronze keeps the response as it arrived
  - The Elexon connector fetches the API response and writes its bytes once, never rewritten, as .json, .xml, .csv or .bin by content type. A sidecar beside it records the request. Files are partitioned by the data's date, or by the fetch date when that is unknown.
  - Sidecar fields: source, dataset, fetched_at, written_at, data_date, request_url, request_params (credentials masked), api_version, http_status, content_type, body_sha256, body_size_bytes, page, total_pages.
  - For each chunk of days, backfill runs gridflow ingest and then gridflow transform, so this one cell fills bronze and silver. Nothing is fetched without yes=True; Elexon is called at most twice a second.
- **H2:** Silver is typed, checked and deduplicated
  - One transformer per dataset reads a day of bronze, validates every row against a Pydantic schema, converts time to UTC, drops duplicates on the dataset's key and writes Parquet compressed with zstd.
  - system_prices is append-only: each capture is kept under its own _run suffix, and the _latest view picks the newest vintage for each settlement period.
  - Every silver table checked carries event_time. The tables sampled also carry available_at, published_at, ingested_at, source_run_id and dataset_version, so a read can be made as of a point in time.
  - Daily means of the system sell price in £/MWh, over the latest vintage of each of the 48 settlement periods.
- **H2:** Gold is ready to query
  - gridflow init registers every silver and gold directory as a view in gridflow.duckdb, beside three tables that log runs, watermarks and quality reports. Three SQL views ship with gridflow:
  - Views: gold_uk_imbalance_context (Elexon system prices with NESO carbon intensity, half-hourly), gold_gb_day_ahead_benchmark (Elexon MID APXMIDP in £/MWh, per settlement period), gold_eu_gas_storage (GIE AGSI+ storage by country and day).
  - gridflow build runs gridflow's own gold builder, system_marginal_price. gridflow-models writes its forecasts and scores into the same gold root, and they register as views too.
  - A bare verb renders its help card; called with a start and an end, it returns gold_uk_imbalance_context as a DataFrame.
- **H2:** Commands and checks
  - Every run is a gridflow command.
  - CLI rows:
    - init: Create the DuckDB catalogue and register the views
    - ingest: Fetch from a vendor API into bronze
    - transform: Bronze to silver: parse, validate, deduplicate
    - build: Silver to gold
    - pipeline: Ingest then transform, and build with --gold
    - backfill: Fetch history in chunks
    - export-csv: Write silver Parquet out as CSV
    - status: Run history and a quality summary
    - quality: Run the quality checks and write a report
    - reset: Delete bronze, silver and gold data and reset the catalogue
    - prune: Delete partitions older than a retention cutoff
  - **H3 Quality checks:** gridflow quality runs five checks on a dataset (null rate, time-series gaps, value ranges, row counts and duplicates) and writes the results to quality_reports.
  - **H3 Gates:**
    - gridflow's CI runs on every push and pull request: uv lock --check, ruff check, ruff format --check, mypy and pytest -m "not live".
    - This site is rendered from the dataset notes by gridflow-build; gridflow-build --check, htmlhint and lychee run before GitHub Pages publishes it.
  - **H3 Not in gridflow:** No scheduler: every run is a command. No server, cloud or hosted database: local files and one DuckDB file. No models or trading: forecasts live in gridflow-models.

### Models

- **H1:** Models that read the warehouse
- **Lede:**
  - gridflow-models is a separate library. It reads gridflow's DuckDB views and Parquet files, and writes its forecasts and scores back into gold.
  - It holds five models, from half-hourly demand to a fundamentals price, and it places no orders.
- **H2:** Five models, six handles
  - In a notebook each model is a handle on models. Demand has two versions, so five models give six handles.
- **Day-ahead demand**
  - GB national demand outturn (Elexon INDO), half-hourly in MW, 24 hours ahead. LightGBM quantile regression, one model per quantile, with a conformal outer band; v2 adds weather and calendar inputs.
  - v1: pinball loss 711.04 MW at the median; 89.3% of outturns inside the 90% band.
  - Scored over 12 walk-forward folds, September 2024 to August 2026. v2 scores 599.72 MW on the same folds with actual weather standing in for forecasts, so its score is optimistic.
- **Wind generation**
  - GB wind outturn (Elexon FUELHH wind), half-hourly in MW, 24 hours ahead. LightGBM quantile regression on weather at 12 wind sites, benchmarked against WINDFOR.
  - It has a model card and a training dataset. No forecasts or scores are stored.
- **Solar generation**
  - Configured on Elexon FUELHH solar, 24 hours ahead, with weather at 6 solar sites and a persistence benchmark.
  - FUELHH has no solar rows, so the configured target is empty and no forecasts or scores exist.
- **GB merit-order stack**
  - The GB supply curve for a settlement period as known at a decision time: BM units ranked by short-run marginal cost, built from the BM unit register, REMIT availability, fuel and carbon prices and plant parameters. It is built, not fitted.
  - It has no score of its own; it is scored through the fundamentals SMP model.
- **Fundamentals SMP**
  - Clears the stack against realised residual demand (national demand less wind, solar and netting) to give a half-hourly day-ahead price, scored against Elexon MID APXMIDP.
  - Headline backtest, 18 August to 3 September 2026 (816 periods): mean bias −151.80 £/MWh, and every period under-predicts.
  - Realised inputs stand in for forecasts, fuel and carbon prices are synthetic, the clearing price has a −500 £/MWh floor, and APXMIDP mixes day-ahead and intraday trades.
- **Plot caption:** The plot in [4]: day-ahead demand v1, walk-forward fold 12, GB national demand in MW, 20 to 21 August 2026 (UTC). The line pair is the outturn and the median forecast; the shading runs from the 5% to the 95% quantile. Source: gold forecasts, run a55a829bc51c40b2.
- **H2:** Where the outputs land
  - Forecasts and scores are written to gold as Parquet, partitioned by model, and read back through DuckDB views.
  - View rows:
    - gold_forecasts: Quantile forecasts beside the outturn, per delivery half-hour
    - gold_forecast_metrics: Scores per run and per walk-forward fold
    - gold_stack_clearing: Fundamentals SMP clearing prices per settlement period
    - gold_stack_residual_demand: The residual demand each SMP run clears against
    - gold_stack_supply_curve_points: The supply-curve points behind each cleared period
- **H3:** How a forecast is scored
  - Pinball loss: The mean quantile loss at the median (q 0.5), in MW for demand. It equals half the mean absolute error of the median forecast.
  - Coverage: The share of outturns inside the band from the 5% to the 95% quantile. A calibrated band covers 90%.
  - Gates: A model passes when its pinball loss at the median is at most 1,500 MW, its coverage is within 0.90 ± 0.05, and no quantiles cross.

## Where the notebook text comes from, and deviations

- **Card rows.** They were rendered on 2026-09-27 from `gridflow_models/research/handles` (`Data._repr_html_`, `SourceClient._repr_html_`, `HelpCard`) and copied verbatim into the site's card chrome, as the homepage did. `Models.__repr__` was rendered the same way.
- **Calls and signatures** (`backfill`, `query`, `sql`, `print(models)`) were checked against `source.py`, `data.py` and `models.py`.
- **Outputs are all pack values:**
  - the daily system-price means for 19 to 22 Sep;
  - the 60 FUELHH wind monthly means;
  - the 96-point band from run a55a829bc51c40b2.
- **The pack's `gold_forecasts` columns** come from its own extraction script (`p27/fc.py`).
- **Models page: no `models` help card** (a deviation). The card's live rows for `stack` and `fundamentals_smp` carry `D-WBA-05` and `ADR-038`, and the predictive verb docstrings carry more codes. `print(models)` (its `__repr__`) is the clean, real substitute.
  - **Finding:** strip the internal codes from the sub-client and verb docstrings in gridflow_models before any models card can appear on the site.
- **Card header count omitted**, as on the homepage. The live `data.elexon` card prints `· 35 datasets` (a middle-dot string and a count), and 35 disagrees with the pack's 33.
  - **Finding:** check what `_DATASET_SOURCE` counts.
- **Double backticks left verbatim.** The live one-liners print literal RST double backticks (``data.elexon``).
  - **Finding:** `_one_liner` should strip RST markup.
- **Architecture has no tab bar.** It is one session with continuous prompts, so it doesn't read as three screenshots.
  - `[2]` `backfill` writes both bronze and silver, and its caption says so. Its summary frame isn't in the pack, so only the input is shown.
  - The bronze and silver paths are the pack's patterns with real directory parts. Placeholders stay visible (tinted).
- **Elexon groups** are the pack's PROPOSED themes, which need owner OK.
- **Removed accessory:** the homepage's keyed marks beside the model entries. This page has no drawing for them to key to.

## Verification

- **Detector:** `[]` on all four boards (SHARED.md sed recipe, then `detect.mjs --json`).
- **Format checks:** root height equals `$preview`; no `{{`/`}}`; no self-closing tags; no `data:` URIs, iframes, em dashes, middle dots or arrows.
- **Layout:** served `static\` on port 9644 in my own tab. JS measured each footer bottom (the root height) and checked every code well, stream and path for horizontal overflow, every notebook child against the notebook's right edge, and every text box against the 80 and 1360 px margins. Zero issues on all four pages.
- **Screenshots:** the browser pane's screenshots wedged, so I viewed the pages as headless Edge shots in slices (`shots\`).
- **Mobile:** layout is flow (CSS grid, no absolutely positioned text), but I didn't check it at 390 px.

## Incident

To clear a stuck headless Edge I ran `taskkill /F /IM msedge.exe` filtered on an empty window title. That can also end the owner's own Edge background processes. Worth knowing if an Edge window closed overnight.
