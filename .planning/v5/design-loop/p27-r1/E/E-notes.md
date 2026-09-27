claude-opus-5-5

# Designer E, "Survey sheets": Phase 27 round 1 notes

## Boards (1440 wide, root height = `$preview`, measured)

- `E\E-data-sources.dc.html`: 5265 px
- `E\E-vendor-elexon.dc.html`: 5551 px
- `E\E-architecture.dc.html`: 5043 px
- `E\E-models.dc.html`: 5485 px

Generator: `E\work\sheet.py` (the shared grammar) plus `ds.py`, `elexon.py`, `arch.py` and `models.py`. Heights are fed back through `work\heights.json`. The static copies are in `E\static\`, and exact sed-recipe copies are in `E\work\sedcopy\`.

## The idea

Every top page is one survey sheet, built the same way. The same grounds hold the same kinds of thing on every page:
- **sky**: title, answer line, horizon
- **topsoil**: the plate, with words on the left and a drawing on the right, keyed level
- **bronze**: the register
- **silver**: the specimen
- **gold**: reach it from code, then how it is checked
- **deep**: limits, sources, other pages

## Content model (the same order on all four; only the plate drawing changes)

1. **Sky** (0 to 290): masthead; h1 of 6 words or fewer (64 px, one line); answer line of 3 lines or fewer; the page's own assets standing on the horizon.
2. **Plate** (topsoil, ends 876 to 930): plate heading; keyed index on the left (mark, name, one line, one fact), each entry level with its part of the drawing; drawing on the right; caption.
3. **Register** (bronze): rail head "Every ..." plus a gloss; every item, one row each.
4. **Specimen** (silver): one real thing, read closely: a pack series, or real field lists where the pack has none.
5. **Reach it from code** (gold): three or four rows, each with a label, one line and a code well.
6. **How it is checked** (gold, below a dotted sub-contact): a definition list of checks, gates and measured facts.
7. **Deep**: What it does not do; Where these facts come from; Other pages; footer.

Per page:
- **Data sources**:
  - Plate: one day, cut at each vendor's grain (7 scale bars, dense to sparse) + key of 7 vendors.
  - Register: 7 vendors (publishes, grain, access, start with).
  - Specimen: GB system price, daily mean, 120 days.
  - Reach: site path / notebook / DuckDB.
  - Checks: silver validation, `gridflow quality`, `--check`.
- **Elexon hub**:
  - Plate: the Elexon cable dropping from the substation, sheath cut back, 33 cores fanned into 5 tied bundles on terminal strips + key of 5 themes with their keys.
  - Register: all 33 by theme (key, BMRS code or path, connector description).
  - Specimen: fuelhh WIND, monthly mean, 60 months.
  - Reach: site / notebook / DuckDB.
  - Checks: no key, SSP = SBP, no solar, quality.
- **Architecture**:
  - Plate: a section through bronze, silver and gold. Cables from four feed assets land in bronze; the substation's cable follows `system_prices` down. Real paths are inscribed per bed, with `gridflow ingest` / `transform` / `build` / `init` written on the contacts.
  - Register: bronze, silver, gold, model outputs, catalogue.
  - Specimen: the bronze sidecar fields and the silver lineage columns (help cards).
  - Reach: the 11 CLI verbs with `cli.py` lines.
  - Checks: row validation, quality, gridflow CI, site gates.
- **Models**:
  - Plate: demand, less wind, less solar, cleared against the stack, gives a price (schematic, no scales) + key of 5 models with neutral standing.
  - Register: target, method, horizon and what exists, for each model.
  - Specimen: demand v1 fold 12 band vs outturn.
  - Reach: workbench calls.
  - Checks: gate definitions + demand metrics table + SMP metrics table + all SMP caveats.

## Decisions

- **Counts.** `[N datasets]` headline. Per vendor `[n]` for ENTSO-E, ENTSO-G, GIE and NESO. Elexon 33, NESO Data Portal 3 and Open-Meteo 6 print as numbers, because configured, vault and local silver agree and nothing in the pack marks them as changing.
- **Elexon themes** are the pack's PROPOSED thematic grouping (the vault groups by API parameter style). They need your OK.
- **A 3-dataset vendor** (NESO Data Portal) uses the same hub. The plate becomes a three-core cable in one bundle, with one key entry listing the three keys, and the register is one group of three rows. ENTSO-E (47 configured) keeps the pattern with more bundles.
- **Grounds are zones, not data layers.** The models register sits on bronze and its specimen (a gold forecast) sits on silver. The rule is by position, so the set reads as one survey.
- **Removed accessories:**
  - The SMP clearing-vs-APXMIDP chart. Its numbers and every required caveat stay under the SMP table.
  - The hub back link. The nav carries `aria-current="true"` on Data sources.
  - Any architecture chart (schematics carry no numbers).
- **Honesty:**
  - Wind and solar are described from "what exists" only.
  - The SMP headline figures always carry the perfect-prognosis caveat, the synthetic fuel prices, the APXMIDP mix and the floor.
  - Gold is shown as the view `gold_uk_imbalance_context`. The `system_marginal_price` builder is described as code only.
  - gridflow is Apache-2.0 in the footer; MIT is the site's own licence.
- **Motion:** only the turbine rotors (models sky), stopped under reduced motion.
- **Inferred wording, needs confirming:**
  - The architecture specimen's one-line meanings for the sidecar fields and lineage columns (`written_at`, `api_version`, `published_at`, `dataset_version`, `total_pages` and so on) are readings of the field names; the pack lists only the names.
  - The Elexon register descriptions are sentence-cased from `ElexonEndpoint.description`, with "2-14" written as "2 to 14" and "Bid/Offer" as "Bid-offer".
  - The Elexon theme glosses on the plate are mine.
- **Canvas safety:** every SVG carries its own pattern definitions under scoped ids (no cross-SVG `url(#...)`, no duplicate ids). Long paths break with zero-width spaces, not `<wbr>`.

## Verification

- Detector `[]` on all four: static copies and exact sed-recipe copies.
- Layout was measured in a browser at 1440 (port 9647, server stopped). Root height equals content bottom on all four. There are no text blocks past the 80 px margins, no clipped boxes, no overlapping SVG text, no SVG text spilling its drawing, no sky label touching the h1 or answer line, and no horizontal overflow. Plates end at 930 / 918 / 876 / 918 px.
- Text is flow and grid; only decorative strata and the sky drawing are absolutely placed.

## Could not do

- Canvas render (no `support.js` here); the static copies were used instead.
- The 390 px reflow is not built. Everything is grid, so the plate would stack the drawing above its keyed index, and the marks would keep the key legible.
- The tab cap was reached, so I reused round 24 designer E's stale tab rather than opening a new one.

## NEW COPY (verbatim; every line on the boards is new)

### E-data-sources

- gas terminal
- converter station
- met mast
- substation
- Where the data comes from
- gridflow ingests [N datasets] from seven vendors, covering GB and EU electricity, EU gas and storage, GB carbon intensity and weather. The catalogue is filed by vendor, then by dataset.
- One day, cut at each vendor’s grain
- Elexon BMRS GB system prices, generation, demand, BM units 33 datasets, GB electricity, no key
- ENTSO-E EU prices, load, generation, flows and outages [n] datasets, EU electricity, API key
- NESO Carbon Intensity GB carbon intensity, actual and forecast [n] datasets, GB carbon, no key
- NESO Data Portal NESO open data: the GB mix since 2009 3 datasets, GB electricity, no key
- Open-Meteo Weather for demand, wind and solar modelling 6 datasets, weather, no key
- ENTSO-G EU gas flows, nominations, capacity, tariffs [n] datasets, EU gas, no key
- GIE AGSI+ and ALSI EU gas storage levels and LNG terminals [n] datasets, EU gas storage and LNG, API key
- one day
- settlement periods, 46 or 50 on clock-change days
- fuelinst, every 5 minutes
- day_ahead_prices: 15-minute for DE-LU, BE, FR and NL
- hourly for IE-SEM
- half-hourly, national and regional
- half-hourly: historic_generation_mix, the embedded forecast
- daily, per BM unit: daily_wind_availability
- hourly, at 7 demand cities, 12 wind sites and 6 solar sites
- the gas day
- Each bar is one day, divided at the grain its vendor publishes; a thin bar beneath is a second grain. Elexon also publishes some datasets once a day, and some as forecasts 2 to 14 days ahead.
- Every vendor, in full
- Seven vendors behind eight source keys: GIE’s two APIs share one key.
- Elexon BMRS elexon 33 datasets The Insights API. GB balancing-mechanism data: system prices, generation outturn, BM-unit data, and demand and wind forecasts. Grain Settlement periods; fuelinst is 5-minute; some daily and 2 to 14-day-ahead sets. Access No key. https://data.elexon.co.uk/bmrs/api/v1 Start with system_prices, fuelhh, indo, mid, remit
- ENTSO-E entsoe [n] datasets The Transparency Platform. EU electricity: day-ahead prices, load, generation per type, cross-border flows, outages, capacity and balancing. Grain XML time series. Zones GB, FR, NL, BE, DE-LU and IE-SEM. Access Key ENTSOE_API_KEY as securityToken, https://web-api.tp.entsoe.eu Start with day_ahead_prices, actual_generation, actual_load, cross_border_flows, wind_solar_forecast
- NESO Carbon Intensity neso [n] datasets GB national and regional carbon intensity, actual and forecast, with statistics, fuel emission factors and the generation mix. Grain Half-hourly. Five families: intensity, factors, stats, generation, regional. Access No key. https://api.carbonintensity.org.uk Start with carbon_intensity, regional_intensity, generation, intensity_factors, intensity_fw48h
- NESO Data Portal neso_data_portal 3 datasets NESO’s open-data catalogue, a file-download API. gridflow reads three of its packages. Grain Half-hourly; daily_wind_availability is daily, per BM unit. Current file only. Access No key. https://api.neso.energy Datasets historic_generation_mix, embedded_wind_solar_forecast, daily_wind_availability
- Open-Meteo open_meteo 6 datasets Weather: the ERA5 archive and NWP forecasts, where GB demand, wind and solar are modelled. Grain Hourly, at 7 demand cities, 12 wind sites and 6 solar sites. Access No key. archive-api.open-meteo.com/v1, api.open-meteo.com/v1 Datasets historical_demand, historical_wind, historical_solar, forecast_demand, forecast_wind, forecast_solar
- ENTSO-G entsog [n] datasets The Transparency Platform. EU gas: physical flows, nominations, allocations, capacities, gas quality and tariffs, by default at UK TSO interconnection points. Grain Daily, by gas day; tariffs and CMP data are periodic. Access No key. https://transparency.entsog.eu/api/v1 Start with physical_flows, nominations, firm_technical, gcv, tariffs
- GIE AGSI+ and ALSI gie_agsi, gie_alsi [n] datasets EU underground gas storage levels and flows (AGSI+) and LNG terminal data (ALSI). Grain Daily, by gas day. AGSI+ nine countries, ALSI eight, GB in both. Access Key GIE_API_KEY in x-key, one for both. agsi.gie.eu, alsi.gie.eu Start with storage, storage_reports, unavailability, lng
- The GB system price, day by day
- Elexon publishes one imbalance price per settlement period: the system sell and buy prices are equal on every latest-vintage row from September 2021 to September 2026.
- 0
- 50
- 100
- 150
- 200
- 1 Jun
- 1 Jul
- 1 Aug
- 1 Sep
- GBP/MWh
- daily mean
- elexon/system_prices silver, system_sell_price: the latest vintage for each settlement period, then the mean of the 48 periods in each settlement date. GBP/MWh, 26 May to 22 September 2026.
- Reach it from code
- Three ways to the same rows.
- On this site Every dataset page sits under its vendor, by key. data-sources/elexon/system_prices.html data-sources/entsoe/day_ahead_prices.html
- In a notebook The gridflow-models workbench has one client per source. from gridflow_models import setup_notebook data, models, common = setup_notebook() data.list_data_sources() data.elexon.list_datasets() data.elexon.system_prices(start, end)
- In DuckDB One view per silver dataset, named source then dataset. Datasets that keep every capture add a _latest view. select * from silver_elexon_system_prices_latest select * from silver_entsoe_day_ahead_prices
- How it is checked
- What a row passes before it reaches a page.
- On the way to silver
- Every row is validated against its Pydantic schema, times are normalised to UTC, and rows are deduplicated on the dataset key.
- gridflow quality
- Five checks per dataset: null_rate, time_series_gaps, range_check, row_count and duplicates.
- Dataset pages
- Rendered from the vault notes by gridflow-build. gridflow-build --check checks the render is idempotent, on every pull request.
- What it does not do
- No scheduler. Data lands when someone runs gridflow ingest; the schedule field in the source config is not read.
- No GB day-ahead prices from ENTSO-E: its GB rows are empty, so the GB benchmark is Elexon MID (APXMIDP).
- No solar in Elexon fuelhh. GB solar outturn is in the NESO Data Portal’s historic_generation_mix.
- No NESO Data Portal backfill, and three of its packages rather than the whole portal.
- Where these facts come from
- Vendors and source keyssrc/gridflow/connectors/registry.py, config/sources.yaml
- Datasets per vendorconnectors/<source>/endpoints.py
- What each vendor publishesthe vault’s 30-vendors/<vendor> notes
- Grain and historylocal silver, read directly
- Other pages
- Architecture How a response becomes a table: bronze, silver, gold and the commands between them.
- Models Five forecasting models built on the warehouse, and the evidence for each.

Drawing and chart descriptions (aria-label):

- Drawing of the grid on the horizon: a gas terminal, an interconnector converter station, a met mast and a substation, standing on the land.
- Seven bars, one per vendor, each one day long and divided at the grain the vendor publishes. Elexon: 48 settlement periods, with fuelinst every 5 minutes beneath. ENTSO-E: day-ahead prices in 15-minute periods for DE-LU, BE, FR and NL, hourly for IE-SEM beneath. NESO Carbon Intensity: half-hourly. NESO Data Portal: half-hourly, with daily wind availability beneath. Open-Meteo: hourly. ENTSO-G and GIE: one gas day each.
- Line chart of the GB system price, daily mean, 26 May to 22 September 2026, in GBP/MWh. It moves between 21 and 211.

### E-vendor-elexon

- pylons
- substation
- Elexon BMRS
- Elexon’s Insights API: GB system prices, generation outturn, BM-unit data, and demand and wind forecasts, with no key needed. 33 datasets, filed here in five themes.
- The datasets, bundled by theme
- Prices and balancing Imbalance prices, market index, acceptances system_prices, market_depth, mid, boal, pn, disbsad, netbsad, soso
- Generation and availability Outturn by fuel, wind forecast, availability fuelhh, fuelinst, agpt, agws, windfor, fou2t14d, uou2t14d, nonbm
- Demand Outturn and forecasts, national and transmission indo, itsdo, indod, atl, ndf, ndfd, tsdf, tsdfd, inddem
- System indicators Margin, imbalance, loss of load, frequency indgen, imbalngc, melngc, lolpdrm, freq, temp
- Reference and messages BM units and REMIT messages bmunits_reference, remit
- sheath cut back
- one core for each dataset
- Elexon drawn as one cable, cut back to its cores: one core for each dataset gridflow ingests, bundled in the five themes this page files them under.
- Every Elexon dataset
- One line each, from the connector’s own description. The middle column is the BMRS code, or the API path where there is none.
- Prices and balancing
- system_prices/​balancing/​settlement/​system-prices/​{date}System sell price and system buy price per settlement period
- market_depth/​balancing/​settlement/​market-depth/​{date}Settlement market depth per settlement period
- midMIDMarket index data
- boalBOALFBid-offer acceptance levels, final (replaces the deprecated BOAL)
- pnPNPhysical notifications
- disbsadDISBSADDisaggregated balancing services adjustment data
- netbsadNETBSADNet balancing services adjustment data
- sosoSOSOSO-SO prices (cross-border interconnector trading)
- Generation and availability
- fuelhhFUELHHHalf-hourly generation outturn by fuel type
- fuelinstFUELINSTInstantaneous generation outturn by fuel type
- agptAGPTActual aggregated generation per type (B1620)
- agwsAGWSActual or estimated wind and solar power generation (B1630)
- windforWINDFORWind generation forecast
- fou2t14dFOU2T14D2 to 14 day-ahead generation availability by fuel type
- uou2t14dUOU2T14D2 to 14 day-ahead generation availability by BM unit
- nonbmNONBMNon-BM STOR generation
- Demand
- indoINDOInitial national demand outturn
- itsdoITSDOInitial transmission system demand outturn
- indodINDODInitial national demand outturn (daily total)
- atlATLActual total load per bidding zone (B0610)
- ndfNDFNational demand forecast (day-ahead)
- ndfdNDFDNational demand forecast (2 to 14 days ahead)
- tsdfTSDFTransmission system demand forecast
- tsdfdTSDFD2 to 14 day-ahead transmission system demand forecast
- inddemINDDEMDay and day-ahead indicated demand
- System indicators
- indgenINDGENDay and day-ahead indicated generation
- imbalngcIMBALNGCIndicated imbalance
- melngcMELNGCIndicated margin
- lolpdrmLOLPDRMLoss of load probability and de-rated margin
- freqFREQSystem frequency
- tempTEMPTemperature data
- Reference and messages
- bmunits_reference/​reference/​bmunits/​allAll BM unit reference data
- remitREMITREMIT outage and unavailability messages
- GB wind generation, month by month
- fuelhh records transmission-metered outturn by fuel type every settlement period. It has no solar fuel type, so GB solar comes from the NESO Data Portal.
- 0
- 4,000
- 8,000
- 12,000
- 2022
- 2023
- 2024
- 2025
- 2026
- MW
- monthly mean
- elexon/fuelhh silver, fuel_type WIND, generation_mw, deduplicated on settlement date, period and fuel type, then the mean for each calendar month. MW, September 2021 to August 2026.
- Reach it from code
- Three ways to the same rows.
- On this site Each dataset page sits under the vendor, by key. data-sources/elexon/fuelhh.html data-sources/elexon/system_prices.html
- In a notebook The Elexon client, and the cross-source day-ahead benchmark built on mid. data.elexon.list_datasets() df = data.elexon.query("fuelhh", "2026-08-01", "2026-08-05") data.elexon.system_prices(start, end) data.gb_day_ahead_benchmark(start, end)
- In DuckDB system_prices, remit and fou2t14d keep every capture; their _latest views keep the newest. select * from silver_elexon_fuelhh select * from silver_elexon_system_prices_latest select * from gold_gb_day_ahead_benchmark
- How it is checked
- Facts about this feed that were measured, not assumed.
- No key
- Every Elexon dataset answered HTTP 200 without a key when the vault checked them on 8 May 2026.
- One imbalance price
- system_sell_price equals system_buy_price on all 88,694 latest-vintage rows from 1 September 2021 to 22 September 2026.
- No solar in fuelhh
- Zero SOLAR rows from 31 August 2021 to 26 September 2026.
- gridflow quality
- Five checks per dataset: null_rate, time_series_gaps, range_check, row_count and duplicates.
- What it does not do
- Three Elexon endpoints are left out on purpose: bod (its availability is unstable), generation_by_fuel (a duplicate of fuelhh) and indicative_imbalance_volumes (removed by Elexon).
- No solar in fuelhh. GB solar outturn is in the NESO Data Portal’s historic_generation_mix.
- No scheduler. Data lands when someone runs gridflow ingest.
- Where these facts come from
- Datasets and descriptionssrc/gridflow/connectors/elexon/endpoints.py (ENDPOINTS)
- Connectorsrc/gridflow/connectors/elexon/client.py
- API parameter stylesthe vault’s 30-vendors/elexon/endpoints.md
- Checks abovelocal silver, read directly
- Other pages
- Data sources Seven vendors and every dataset gridflow ingests, filed by vendor.
- Architecture How a response becomes a table: bronze, silver, gold and the commands between them.
- Models Five forecasting models built on the warehouse, and the evidence for each.

Drawing and chart descriptions (aria-label):

- Drawing of lattice pylons carrying lines into a substation on the horizon. A cable runs from the substation down into the ground.
- The Elexon feed drawn as one cable coming down from the substation. Its sheath is cut back and 33 cores fan out into five bundles, each tied and wired to a terminal strip: prices and balancing, 8 cores; generation and availability, 8; demand, 9; system indicators, 6; reference and messages, 2.
- Line chart of GB transmission-metered wind generation, monthly mean, September 2021 to August 2026, in MW. It moves between 3,661 and 11,581 MW, higher in winter months.

### E-architecture

- gas terminal
- converter station
- met mast
- substation
- How data moves, bronze to gold
- A local Python pipeline with no server. Each API response lands untouched in bronze, becomes typed Parquet in silver, and is served as DuckDB views in gold.
- One dataset, followed down
- Bronze The raw response, as sent, and a JSON sidecar. Written once, never rewritten. json, xml, csv or bin, by content type
- Silver Typed tables: every row validated, times in UTC, duplicates removed. Parquet, zstd
- Gold Ready to query: DuckDB views over silver, some joined across sources. views in gridflow.duckdb
- gridflow ingest
- gridflow transform
- gridflow build
- gridflow init
- bronze/elexon/system_prices/{YYYY}/{MM}/{DD}/
- raw_{fetched_at}_{sha256[:8]}.json
- raw_{fetched_at}_{sha256[:8]}.meta.json
- the response as sent, written once, and its sidecar
- silver/elexon/system_prices/year={YYYY}/month={MM}/
- system_prices_{YYYYMMDD}_run{available_at}.parquet
- one file per day and per capture
- silver_elexon_system_prices_latest
- a view: the newest capture of each settlement period
- gold_uk_imbalance_context
- a DuckDB view: system prices joined with NESO carbon intensity, half-hourly
- Elexon system_prices on its way down. Every feed lands in bronze; the command that carries data across each contact is written on it.
- Every layer, as stored
- Paths are relative to the data root, set by GRIDFLOW_DATA_DIR.
- Bronze gridflow ingest Raw response bytes, exactly as the API sent them, with a JSON sidecar beside each body. Written once, never rewritten. Partitioned by the data date when known, otherwise the fetch date. Format json, xml, csv or bin, by content type, plus .meta.json Path bronze/{source}/{dataset}/{YYYY}/{MM}/{DD}/​raw_{fetched_at}_{sha256[:8]}.{ext} Code bronze/writer.py, storage/paths.py
- Silver gridflow transform One transformer per source and dataset reads the day’s bronze, validates every row against its Pydantic schema, normalises time to UTC, deduplicates on the dataset key and writes Parquet atomically. Format Parquet, zstd Path silver/{source}/{dataset}/year={YYYY}/month={MM}/​{dataset}_{YYYYMMDD}.parquet Captures {dataset}_{YYYYMMDD}_run{available_at}.parquet for Elexon system_prices, remit and fou2t14d and the three NESO Data Portal datasets; _latest views pick the newest Code silver/base.py, silver/registry.py, silver/latest_views.py
- Gold gridflow build, gridflow init Built from silver: one Python builder, system_marginal_price, and three SQL views that register when the catalogue is initialised. Path gold/{name}/year={YYYY}/{name}_{YYYYMMDD}.parquet Views gold_uk_imbalance_context: Elexon system prices with NESO carbon intensity. gold_gb_day_ahead_benchmark: Elexon MID APXMIDP, GBP/MWh. gold_eu_gas_storage: GIE AGSI+ by country and day. Code gold/registry.py, gold/views/*.sql
- Model outputs written by gridflow-models gridflow-models writes its forecasts, metrics and stack tables into the same gold root, partitioned by model. Tables forecasts, forecast_metrics, stack_clearing, stack_residual_demand, stack_supply_curve_points Path gold/{table}/model_slug={slug}/​{prefix}_{timestamp}_{run_id}.parquet
- Catalogue gridflow init One DuckDB file, {data_root}/gridflow.duckdb, holding run metadata and a view over every silver and gold directory. Tables pipeline_runs, pipeline_watermarks, quality_reports Views silver_{source}_{dataset}, silver_{source}_{dataset}_latest, gold_{name} Code storage/duckdb.py
- What a file and a row carry
- The metadata kept with every body and row, so a number can be traced back to the request that fetched it.
- raw_….meta.json
- source
- the source key, such as elexon
- dataset
- the dataset key
- fetched_at
- when the request was made
- written_at
- when the body was written
- data_date
- the date the data is for, when known
- request_url
- with credentials masked
- request_params
- api_version
- the vendor API version
- http_status
- the response status
- content_type
- sets the body’s extension
- body_sha256
- its first 8 characters are in the file name
- body_size_bytes
- the body’s size
- page
- position in a paged response
- total_pages
- pages in the response
- Beside every bronze body.
- silver lineage columns
- event_time
- the time the value describes, in UTC
- available_at
- when the value became available, for as-of reads
- published_at
- when the vendor published it
- ingested_at
- when gridflow ingested it
- source_run_id
- the run that wrote the row
- dataset_version
- the dataset’s version
- event_time is on every silver dataset; the others were on every dataset sampled.
- Reach it from code
- Every run is one of these commands; gridflow = gridflow.cli:app. Read-only queries go through gridflow.serving.client.GridflowClient.
- gridflow initCreate the DuckDB catalogue and register its viewscli.py:1209
- gridflow ingestAPI to bronzecli.py:186
- gridflow transformBronze to silver: normalised, validated, deduplicatedcli.py:261
- gridflow buildSilver to goldcli.py:306
- gridflow pipelineIngest then transform; with --gold, build as wellcli.py:485
- gridflow backfillHistorical data, in chunkscli.py:346
- gridflow export-csvSilver Parquet to CSVcli.py:438
- gridflow statusRun history and a quality summarycli.py:584
- gridflow qualityRun the quality checks and write a reportcli.py:677
- gridflow resetDelete bronze, silver and gold data and reset the cataloguecli.py:796
- gridflow pruneDelete partitions older than a retention cutoffcli.py:972
- How it is checked
- What runs before a row, or a page, is trusted.
- Each row
- Validated against its Pydantic schema during gridflow transform.
- gridflow quality
- null_rate, time_series_gaps, range_check, row_count and duplicates, written to quality_reports.
- gridflow’s CI
- On every push and pull request: uv lock --check, ruff check and format, mypy, and pytest, excluding the tests that call vendor APIs.
- This site
- On pull requests: a staleness check, a baseline ratchet and gridflow-build --check. Before deploy: htmlhint and lychee.
- What it does not do
- No scheduler or orchestrator: every run is a command. The schedule field in the source config is not read.
- No cloud, object store, warehouse, streaming or cluster: local files and one embedded DuckDB file.
- No server, public API or hosted database.
- No models or forecasts. Those live in gridflow-models, which reads this store.
- Where these facts come from
- Pathssrc/gridflow/storage/paths.py (PathBuilder)
- Bronze and silverbronze/writer.py, silver/base.py, silver/latest_views.py
- Gold and the cataloguegold/registry.py, gold/views/*.sql, storage/duckdb.py
- Commands and checkscli.py, quality/checks.py, the CI workflows
- Other pages
- Data sources Seven vendors and every dataset gridflow ingests, filed by vendor.
- Models Five forecasting models built on the warehouse, and the evidence for each.

Drawing and chart descriptions (aria-label):

- Drawing of a gas terminal, an interconnector converter station, a met mast and a substation on the horizon, each with a cable running down into the ground.
- A section through three beds, bronze, silver and gold. Cables from a gas terminal, a converter station and a met mast end in bronze. The substation's cable, carrying Elexon system_prices, runs on through all three. gridflow ingest is written on the ground contact, gridflow transform on the bronze to silver contact, and gridflow build and gridflow init on the silver to gold contact. In bronze: the raw JSON response and its meta.json sidecar under bronze/elexon/system_prices by date. In silver: a daily Parquet file with a run suffix per capture, and the silver_elexon_system_prices_latest view. In gold: the gold_uk_imbalance_context view, joined with NESO carbon intensity.

### E-models

- onshore wind
- gas-fired power station
- solar farm
- What the models forecast
- A separate library that reads gridflow’s DuckDB and Parquet. Five models: day-ahead demand, wind, solar, a GB merit-order stack, and a price model built from the other four.
- How the five fit together
- GB merit-order stack stack.gb.v1 Built on demand; no standalone metric
- Fundamentals SMP fundamentals_smp.gb.v1 Backtests published, scored against APXMIDP
- Solar generation solar.lgbm_quantile.v1 Config and model card; its target has no rows
- Wind generation wind.lgbm_quantile.v1 Config, model card, training file; no forecasts
- Day-ahead demand day_ahead.lgbm_demand.v1, .v2 v1 backtest: pinball q0.5 711.04 MW
- biomass
- nuclear
- CCGT
- coal
- OCGT
- price
- capacity, cheapest first
- clearing price
- residual demand
- less solar
- less wind
- demand
- Read from the bottom: demand, less wind and less solar, leaves residual demand; cleared against the merit-order stack, it gives a price. The published price backtests use realised inputs in place of the three forecasts.
- Every model, in full
- Five models, one of them in two versions, as configured in gridflow-models.
- Day-ahead demand day_ahead.lgbm_demand.v1day_ahead.lgbm_demand.v2 Target GB national demand outturn, half-hourly, MW: elexon/indo, initial_demand_outturn_mw Method LightGBM quantile regression, one model per quantile from 0.05 to 0.95, sorted to be monotone, with a conformal (CQR) outer band. v2 adds weather and calendar features. Horizon 24 hours ahead What exists 21 v1 versions and one v2 version in the manifest, all with status validated; walk-forward backtests in gold; one issued v2 forecast, 4 to 6 September 2026.
- Wind generation wind.lgbm_quantile.v1 Target GB wind outturn, half-hourly, MW: elexon/fuelhh WIND Method LightGBM quantile regression on weather at 12 wind sites; benchmark WINDFOR. Horizon 24 hours ahead What exists A config, a model card and a training dataset file, with no manifest entry, forecasts or metrics.
- Solar generation solar.lgbm_quantile.v1 Target Configured as elexon/fuelhh SOLAR, which has no rows Method LightGBM quantile regression on weather at 6 solar sites; benchmark persistence. Horizon 24 hours ahead What exists A config and a model card, with no manifest entry, forecasts or metrics.
- GB merit-order stack stack.gb.v1 Target The GB supply curve at one settlement period: units by short-run marginal cost, cumulative MW, GBP/MWh, floor −500 Method Constructive, no training: BM-unit inventory from bmunits_reference, availability from remit, commodity prices from a manual file, per-technology parameters from config. Horizon A point in time: a decision time and a target period What exists Builds on demand; its supply-curve points are published in gold with each SMP run.
- Fundamentals SMP fundamentals_smp.gb.v1 Target GB day-ahead system marginal price, half-hourly, GBP/MWh, scored against elexon/mid APXMIDP Method The stack cleared against residual demand (demand less wind, solar and signed netting), with realised inputs in place of forecasts. Horizon Day-ahead, half-hourly What exists A published headline backtest and 13 monthly diagnostic runs in gold.
- Demand forecast against outturn
- Two days from the last fold of the v1 backtest: the 90% band, the median, and what happened.
- 18,000
- 22,000
- 26,000
- 30,000
- 20 Aug
- 12:00
- 21 Aug
- MW
- outturn
- median forecast
- 5% to 95%
- gold forecasts, run a55a829bc51c40b2, day_ahead.lgbm_demand.v1, walk-forward fold 12, issued vintage: outturn, q0.05, q0.5 and q0.95. MW, 20 to 21 August 2026, half-hourly, UTC.
- Reach it from code
- Notebooks are call sites only; the model logic lives in the library.
- Set up One handle per configured model; list() lists them. from gridflow_models import setup_notebook data, models, common = setup_notebook() models.list()
- Demand Also train, validate, show_folds, predictions and model_card; v2 is models.demand_forecast_v2. models.demand_forecast.predict(...)
- Stack Build the supply curve for a decision time, then clear it against a demand. models.stack.build(as_of) models.stack.clear(as_of, demand_mw)
- Fundamentals SMP Also assemble, components and predictions. models.fundamentals_smp.backtest(...)
- How it is checked
- The gates a probabilistic model must pass, and the scores that exist; wind, solar and the stack have none.
- Pinball q0.5
- The mean quantile loss at 0.5: half the mean absolute error of the median forecast, in MW. Gate: at most 1,500.
- coverage_90
- The share of outturns inside q0.05 to q0.95, bounds included. Gate: within 0.90 ± 0.05.
- Crossings
- Quantiles that cross each other. Gate: none.
- day_ahead.lgbm_demand, walk-forward backtests
- run
- pinball q0.5, MW
- crossings
- gates
- v1
- a55a829bc51c40b2
- 711.04
- 0.893
- 0
- pass
- v2
- b367a742aa544f8f
- 599.72
- 0.883
- Both over the same 12 folds of 30 days, 1 September 2024 to 22 August 2026, 17,279 half-hours. v2 used actual ERA5 weather as if it were a forecast, so its score is optimistic; its model card calls the 15.7% gain an upper bound, from one run.
- fundamentals_smp.gb.v1, against APXMIDP
- window
- periods
- mean bias, GBP/MWh
- MAE, GBP/MWh
- headline
- 18 Aug to 3 Sep 2026
- 816
- −151.80
- 151.80
- 13 monthly runs
- 5 May 2025 to 4 May 2026
- 17,520
- −69.81
- 72.84
- Both are perfect-prognosis backtests: realised demand, wind and solar stand in for the forecasts, and fuel and carbon prices are synthetic. APXMIDP mixes day-ahead and intraday trades, so it is not one auction. The −500 GBP/MWh floor weighs on the bias: in an earlier version, about 46% of it came from the 12% of periods where clearing hit the floor.
- What it does not do
- gridflow-models does not produce orders.
- No forecasts or metrics exist for the wind and solar models.
- The stack has no accuracy metric of its own; it is scored through the fundamentals SMP model.
- The published SMP backtests use realised inputs and synthetic fuel and carbon prices.
- Where these facts come from
- What existsthe manifest in data/gridflow_models.duckdb, gold forecasts and forecast_metrics, and docs/MODEL_CARDS/
- Metrics and gatesgridflow_models/validation/metrics.py
- Models and targetsconfigs/models/
- Workbench callssrc/gridflow_models/research/handles/
- Other pages
- Data sources Seven vendors and every dataset gridflow ingests, filed by vendor.
- Architecture How a response becomes a table: bronze, silver, gold and the commands between them.

Drawing and chart descriptions (aria-label):

- Drawing of onshore wind turbines, a gas-fired power station and a solar farm on the horizon: the output and the price the models forecast.
- How the five models fit together, drawn without scales. Read from the bottom: a demand forecast is a bar along the capacity axis with its spread at the end; the wind forecast is carved off that end, then the solar forecast. What is left is residual demand. Above, the merit-order stack rises in steps: biomass, nuclear, a long run of CCGT units, coal, then OCGT. Where residual demand meets the stack, a clearing price is read off the price axis.
- Chart of the day-ahead demand forecast against outturn, 20 to 21 August 2026, half-hourly, in MW: a band from the 5% to the 95% quantile, the median forecast, and the outturn, which stays inside the band for most of the two days.
