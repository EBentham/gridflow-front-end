claude-opus-5-5

# Designer A, Phase 27 round 1: "Sections"

## Boards (1440 wide, root height equals $preview)

- `p27/A/A-data-sources.dc.html`: 2589 px
- `p27/A/A-vendor-elexon.dc.html`: 3736 px
- `p27/A/A-architecture.dc.html`: 3800 px
- `p27/A/A-models.dc.html`: 2699 px

The static copies used for the detector and the layout checks are in `p27/A/static/`. The generator is `build.py` plus `p_*.py`, `frame.py` and `scenery.py`.

## The one idea

Each top page is its own geological section under the homepage's sky. A cable runs from each drawn asset down through the strata to the entry on the page that it feeds.

## Blocks per page, in order

- **Data sources:** sky (h1, lede with `[N datasets]`, landscape cut west to east through GB, the North Sea in profile and the continent); topsoil (the cables drop); bronze (seven vendor entries staggered along their cables, plus one note); silver ("Find a dataset": `system_prices` under five names, with the daily system-price chart); footer in the deep.
- **Elexon hub:** sky (breadcrumb, h1, intro, facts dl with `[n]`, GB assets with offshore wind in section); topsoil (monthly wind output chart); bronze (the head, then five dataset beds, with one trunk cable and a joint at each bed); silver (the three `_latest` views); gold (notebook well); footer.
- **Architecture:** sky (h1, lede, facts, the homepage landscape); topsoil (connectors and the 8 source keys); bronze (text, 14 sidecar fields, keyed path); silver (5 ordered steps, standard columns, append-only datasets, keyed paths); gold (views, paths, tables); deep ("The build and the gates": CLI verbs, data checks, code checks, this site, not in gridflow); footer. There is no flowchart: four feeds splice into one trunk, with verbs on the contacts.
- **Models:** sky (h1, lede, landscape: demand pylon, wind farm, solar farm, plant fleet in merit order); thin topsoil and bronze; silver (input taps per model); gold (demand with v1 and v2 scores and band chart; wind; solar; stack; SMP with table and chart carrying all four caveats; reading the scores, plus a notebook well); footer.

## Pattern for a 3-dataset vendor (for example the NESO Data Portal)

- The landscape shows one asset and one cable.
- Bronze holds a single bed with no grouping and three rows.
- The topsoil chart appears only where a long pack series exists (for example `historic_generation_mix`). Otherwise the topsoil is left empty.
- The silver and gold bands are kept.

## Decisions to flag

- The five Elexon beds use the pack's PROPOSED grouping, pending the owner's OK.
- The hub's split of datasets by parameter style is attributed to gridflow's code, not to Elexon.

## Verification

- **Detector:** `[]` on all four static pages (`node .claude/skills/impeccable/scripts/detect.mjs --json`).
- **Headless probe:** headless Chrome, served on port 9617, measured every section and terminal. The overflow list is empty on all four.
- **Browser-tab check:** in my own tab at 1440 wide, there are no overlapping text leaves, no text outside x 80 to 1360, and the document is 1440 wide.
- **Glyph scan:** none of the banned glyphs appear.
- **After the final tweak:** the browser-tab check ran before the last models rebuild (stack copy and true minus signs). The probe rects are unchanged (gold 1480, H 2699) and the overflow list is still empty.
- **Cleanup:** the server was stopped afterwards.

## Not done

- There are no 390 px media queries. Every block is a CSS grid in normal flow, so each page can collapse to one column, but the collapse is not written or tested.
- The `.dc.html` files were not rendered in the canvas itself (there is no local `support.js`). Only the static copies were rendered.


## Every copy line on the boards, verbatim

Extracted from the final static pages. Dataset keys, paths, model ids, numbers and the pack's own one-liners (vendor code descriptions, CLI lines) are facts from the pack; everything else is NEW COPY for approval.


### A-data-sources

- Home
- Data sources
- Architecture
- Models
- About
- Every dataset, traced to the vendor that publishes it
- gridflow reads seven vendors across GB and EU electricity, EU gas, carbon intensity and weather. The catalogue holds [N datasets], organised by vendor.
- Each cable in the drawing runs from the part of the system a vendor reports on down to the directory where gridflow keeps that vendor’s raw responses.
- How the layers work
- bronze/elexon/
- Elexon BMRS
- GB balancing mechanism: prices, generation, demand, BM units and forecasts
- [n] datasets, half-hourly, no API key
- system_prices | one imbalance price per period
- fuelhh | outturn by fuel type, no solar
- indo | initial national demand outturn
- mid | market index, the GB day-ahead benchmark
- bronze/neso/
- NESO Carbon Intensity
- GB carbon intensity, national and regional, actual and forecast
- [n] datasets, half-hourly, no API key
- carbon_intensity | national, over a date range
- regional_intensity | every region, over a date range
- generation | national generation mix
- intensity_fw48h | 48-hour forecast
- bronze/neso_data_portal/
- NESO Data Portal
- System operator files: the GB generation mix since 2009, embedded forecasts
- [n] datasets, current file only, no API key
- historic_generation_mix | GB mix by fuel since 2009, with solar
- embedded_wind_solar_forecast | embedded wind and solar forecast
- daily_wind_availability | daily MW per BM unit
- bronze/open_meteo/
- Open-Meteo
- Weather archive and forecasts at GB demand cities, wind and solar sites
- [n] datasets, hourly, no API key
- historical_demand | ERA5 at 7 demand cities
- historical_wind | ERA5 at 12 wind sites, 10 m and 100 m
- historical_solar | ERA5 at 6 solar sites
- forecast_wind | forecast at the same wind sites
- bronze/gie_agsi/, gie_alsi/
- GIE AGSI+ and ALSI
- EU gas storage levels and flows, and LNG terminal send-out
- [n] datasets, daily gas days, API key
- storage | storage level by country and day
- storage_reports | by country, company or facility
- unavailability | storage unavailability reports
- lng | LNG terminal data
- bronze/entsog/
- ENTSO-G
- EU gas: flows, nominations and capacity at interconnection points
- [n] datasets, daily gas days, no API key
- physical_flows | flow at interconnection points
- nominations | nominations per point
- firm_technical | firm technical capacity
- gcv | gross calorific value
- bronze/entsoe/
- ENTSO-E
- EU electricity: day-ahead prices, load, generation, flows and outages
- [n] datasets, XML, API key
- day_ahead_prices | EUR/MWh per bidding zone
- actual_generation | output per production type
- cross_border_flows | physical flows between zones
- wind_solar_forecast | day-ahead wind and solar
- The path beside each terminal is where gridflow keeps that vendor’s raw responses. The linked datasets are places to start: each vendor’s hub lists all of them, in groups.
- Find a dataset
- Search a vendor’s hub, or use the dataset’s gridflow key: it names the dataset in every layer, from the raw files to the notebook. Here is system_prices under each of its names.
- vendor endpoint
- /balancing/settlement/system-prices/{date}
- raw responses
- bronze/elexon/system_prices/
- typed Parquet
- silver/elexon/system_prices/
- DuckDB view
- silver_elexon_system_prices_latest
- notebook
- data.elexon.query("system_prices", start, end)
- GB system price, daily mean, 26 May to 22 September 2026
- elexon/system_prices in silver: the latest vintage of each settlement period, averaged over the 48 periods of each settlement date, GBP/MWh. The dots mark the highest day, 13 September, and the lowest, 13 June. System sell and buy prices are equal on every row, so one line shows both.
- Data sources
- Architecture
- Models
- About
- GitHub
- This site is MIT-licensed. gridflow is Apache-2.0.

Drawing and chart labels: bronze; silver; onshore wind; offshore wind; substation; gas-fired power station; solar farm; met mast; LNG carrier; LNG terminal; gas terminal; interconnector; converter station; Jun 2026; Jul 2026; Aug 2026; Sep 2026

Alt text (aria-label) of drawings and charts:

- A section from Great Britain across the North Sea to the continent. On the British side: pylons into a substation, a gas-fired power station, a solar farm and a met mast on the coast, with onshore wind on the ridge. The sea is cut in section, with offshore turbines on monopiles and an LNG carrier at a jetty. On the far shore: an LNG terminal, a gas terminal and an interconnector converter station. One cable runs down from each of these seven assets to the vendor that publishes data on it.
- Line chart of the GB system price, daily mean of the 48 settlement periods, 26 May to 22 September 2026, in GBP/MWh. It ranges from 20.9 to 211.2.

### A-vendor-elexon

- Home
- Data sources
- Architecture
- Models
- About
- Elexon BMRS
- Great Britain’s balancing mechanism, from Elexon’s Insights API: system prices, generation outturn, BM-unit data, and demand and wind forecasts.
- Market
- GB electricity
- Access
- No API key
- Base URL
- data.elexon.co.uk/bmrs/api/v1
- Grain
- Half-hourly settlement periods, 1 to 50 a day (46 or 50 when the clocks change); FUELINST every 5 minutes
- Connector
- connectors/elexon/client.py
- Datasets
- [n]
- GB wind generation, monthly mean, September 2021 to August 2026
- elexon/fuelhh, fuel type WIND: mean half-hourly generation_mw per calendar month, MW, one row per settlement date, period and fuel type. The highest month is January 2026, the lowest August 2022. FUELHH is transmission-metered and carries no solar; GB solar outturn is in the NESO Data Portal’s historic_generation_mix.
- The datasets, in five groups
- The groups are this site’s way in. In gridflow’s code they differ by how each is requested: most take a from/to publish-time window; system_prices and market_depth take a settlement date in the path, pn a settlement date and period, and bmunits_reference nothing at all.
- Prices and balancing
- What the system paid to balance, and the actions behind it.
- system_prices | System Sell Price and System Buy Price per settlement period | /balancing/settlement/system-prices/{date}
- market_depth | Settlement market depth per settlement period | /balancing/settlement/market-depth/{date}
- mid | Market Index Data | /datasets/MID
- boal | Bid/Offer Acceptance Levels (BOALF; replaces deprecated BOAL) | /datasets/BOALF
- pn | Physical Notifications (per BM unit, per period) | /datasets/PN
- disbsad | Disaggregated Balancing Services Adjustment Data | /datasets/DISBSAD
- netbsad | Net Balancing Services Adjustment Data | /datasets/NETBSAD
- soso | SO-SO prices (cross-border interconnector trading) | /datasets/SOSO
- Generation and availability
- What ran, by fuel and by unit, and what is declared available.
- fuelhh | Half-hourly generation outturn by fuel type (no solar) | /datasets/FUELHH
- fuelinst | Instantaneous generation outturn by fuel type | /datasets/FUELINST
- agpt | Actual aggregated generation per type (B1620) | /datasets/AGPT
- agws | Actual or estimated wind and solar generation (B1630) | /datasets/AGWS
- windfor | Wind generation forecast | /datasets/WINDFOR
- fou2t14d | 2–14 day-ahead generation availability by fuel type | /datasets/FOU2T14D
- uou2t14d | 2–14 day-ahead generation availability by BM unit | /datasets/UOU2T14D
- nonbm | Non-BM STOR generation | /datasets/NONBM
- Demand
- Outturn and forecasts, national and transmission, from the day ahead to 14 days out.
- indo | Initial National Demand Outturn | /datasets/INDO
- itsdo | Initial Transmission System Demand Outturn | /datasets/ITSDO
- indod | Initial National Demand Outturn (daily total) | /datasets/INDOD
- atl | Actual total load per bidding zone (B0610) | /datasets/ATL
- ndf | National Demand Forecast (day-ahead) | /datasets/NDF
- ndfd | National Demand Forecast (2–14 days ahead) | /datasets/NDFD
- tsdf | Transmission System Demand Forecast | /datasets/TSDF
- tsdfd | 2–14 day-ahead Transmission System Demand Forecast | /datasets/TSDFD
- inddem | Day and day-ahead indicated demand | /datasets/INDDEM
- System indicators
- Margin, imbalance, loss-of-load probability, frequency and temperature.
- indgen | Day and day-ahead indicated generation | /datasets/INDGEN
- imbalngc | Indicated imbalance | /datasets/IMBALNGC
- melngc | Indicated margin | /datasets/MELNGC
- lolpdrm | Loss of Load Probability and De-rated Margin | /datasets/LOLPDRM
- freq | System frequency | /datasets/FREQ
- temp | Temperature data | /datasets/TEMP
- Reference and messages
- The register of BM units, and outage and unavailability notices.
- bmunits_reference | All BM unit reference data | /reference/bmunits/all
- remit | REMIT outage and unavailability messages | /datasets/REMIT
- In silver, every capture is kept
- Each dataset is one DuckDB view, silver_elexon_{dataset}. Three are append-only: a later publication never overwrites an earlier one, each capture is its own _run{available_at} file, and a _latest view returns the newest capture for each key.
- silver_elexon_system_prices_latest
- silver_elexon_remit_latest
- silver_elexon_fou2t14d_latest
- From a notebook
- The workbench in gridflow-models reads the same silver. Every source answers the same verbs.
- Data sources
- Architecture
- Models
- About
- GitHub
- This site is MIT-licensed. gridflow is Apache-2.0.

Drawing and chart labels: bronze; silver; gold; onshore wind; offshore wind; substation; gas-fired power station; nuclear power station; battery storage; interconnector; converter station; Sep 2021

Alt text (aria-label) of drawings and charts:

- The GB system that Elexon reports on: pylons into a substation, a gas-fired power station, a nuclear power station, battery storage and an interconnector converter station on the coast, with onshore wind on the ridge and offshore wind cut in section at sea. One cable runs down from the substation and taps each group of datasets in turn.
- Column chart of GB transmission-metered wind generation from elexon/fuelhh, mean half-hourly output per calendar month, September 2021 to August 2026, in MW. Monthly means run from 3,661 MW to 11,581 MW.

### A-architecture

- Home
- Data sources
- Architecture
- Models
- About
- From a vendor’s response to a DuckDB view
- gridflow is a local-first Python pipeline built on Polars, DuckDB, Pydantic v2, httpx and Typer.
- It has no server and no scheduler. Every run is a command, and everything it keeps is a file under one data root.
- Data root
- GRIDFLOW_DATA_DIR
- Catalogue
- {data_root}/gridflow.duckdb
- Entry point
- gridflow = gridflow.cli:app
- Licence
- Apache-2.0
- One connector per source key
- Each source has an async client, connectors/<source>/client.py, with the rate limit and retries set for it in config/sources.yaml (Elexon 2 requests a second, ENTSO-E 1). GIE has two keys, one per API.
- elexon
- entsoe
- entsog
- gie_agsi
- gie_alsi
- neso
- neso_data_portal
- open_meteo
- Bronze keeps every response as it arrived
- The body is written first, then a JSON sidecar with the same stem, each through a temporary file and os.replace. Nothing in bronze is rewritten.
- The sidecar, .meta.json
- source
- dataset
- fetched_at
- written_at
- data_date
- request_url
- request_params
- api_version
- http_status
- content_type
- body_sha256
- body_size_bytes
- page
- total_pages
- The request URL and parameters are stored with credentials masked.
- Silver holds typed, validated, deduplicated tables
- One transformer per source and dataset. For each date it:
- reads that date’s bronze and parses it
- validates every row against the dataset’s Pydantic schema
- normalises every timestamp to UTC
- deduplicates on the dataset’s key
- writes zstd Parquet, atomically
- Columns every table carries
- event_time is on every silver table. The tables checked also carry available_at, published_at, ingested_at, source_run_id, dataset_version, which is what makes as-of reads possible downstream.
- Append-only datasets
- Six keep every capture instead of overwriting: elexon system_prices, remit, fou2t14d and the NESO Data Portal’s three. A _latest view returns the newest capture for each key.
- Gold is what DuckDB serves
- gridflow init registers a view for every silver and gold directory, and the SQL views, in gridflow.duckdb. gridflow build runs the registered gold builder, system_marginal_price. gridflow-models writes its forecasts and backtests into the same gold root.
- gridflow’s builder
- gold/{name}/year={YYYY}/{name}_{YYYYMMDD}.parquet
- gridflow-models
- gold/{table}/model_slug={slug}/{prefix}_{YYYYMMDDTHHMMSSZ}_{run_id}.parquet
- Views in gridflow.duckdb
- silver_{source}_{dataset}
- one view per silver dataset
- silver_{source}_{dataset}_latest
- the newest capture, for append-only datasets
- gold_{name}
- one view per gold directory
- gold_uk_imbalance_context
- Elexon system prices with NESO carbon intensity, half-hourly
- gold_gb_day_ahead_benchmark
- Elexon MID APXMIDP, GBP/MWh: the GB day-ahead benchmark
- gold_eu_gas_storage
- GIE AGSI+ storage by country and day
- Beside them, three tables: pipeline_runs, pipeline_watermarks, quality_reports. Python reads it all through GridflowClient, which is read-only.
- The build and the gates
- Every command
- init
- create the catalogue and register views
- ingest
- API to bronze
- transform
- bronze to silver
- build
- silver to gold
- pipeline
- ingest then transform, then build with --gold
- backfill
- history, in chunks
- export-csv
- silver Parquet to CSV
- status
- run history and quality
- quality
- run the data checks, write a report
- reset
- delete layers and reset the catalogue
- prune
- delete partitions older than a cutoff
- Checks on the data
- gridflow quality runs null_rate, time_series_gaps, range_check, row_count, duplicates, and writes each result to quality_reports.
- Checks on the code
- On every push and pull request: uv lock --check, ruff check, ruff format --check, mypy, pytest -m "not live".
- This site
- gridflow-build renders the vault notes into the dataset pages; --check proves the output unchanged on every pull request. Publishing adds htmlhint and a link check before GitHub Pages.
- Not in gridflow
- No scheduler: the schedule field in sources.yaml is read nowhere.
- No server, public API or hosted database.
- No cloud, object store, streaming or cluster.
- No live feed: data lands when someone runs ingest.
- No models: those live in gridflow-models.
- Data sources
- Architecture
- Models
- About
- GitHub
- This site is MIT-licensed. gridflow is Apache-2.0.

Drawing and chart labels: onshore wind; offshore wind; gas-fired power station; solar farm; data centre; battery storage; substation; met mast; interconnector; converter station; gas terminal; gridflow ingest; into bronze; gridflow transform; bronze into silver; gridflow build; silver into gold; bronze/{source}/{dataset}/{YYYY}/{MM}/{DD}/raw_{fetched_at:%Y%m%dT%H%M%SZ}_{sha256[:8]}.{ext}; source key; dataset; data date, else the fetch date; when it was fetched, UTC; first 8 characters of the body’s SHA-256; json, xml, csv or bin, by content type; silver/{source}/{dataset}/year={YYYY}/month={MM}/{dataset}_{YYYYMMDD}.parquet; year; month; one file per date; {dataset}_{YYYYMMDD}_run{available_at}.parquet; append-only: one file per capture

Alt text (aria-label) of drawings and charts:

- The same landscape as the home page: wind, solar, a gas-fired power station, pylons, a data centre, battery storage, a substation, a met mast, an interconnector converter station and a gas terminal. Four cables run down from the substation, the met mast, the converter station and the gas terminal and join into one at the bronze contact.
- The bronze path template: bronze, source key, dataset, the data date (else the fetch date) as year, month and day, then raw_, the fetch time in UTC, the first 8 characters of the body's SHA-256 and an extension set by content type.
- The silver path template: silver, source key, dataset, year= and month= partitions, then one file per date named after the dataset. Append-only datasets add _run and the capture's available_at before .parquet, one file per capture.

### A-models

- Home
- Data sources
- Architecture
- Models
- About
- Five models, from demand to the day-ahead price
- gridflow-models is a separate library that reads gridflow’s DuckDB catalogue and Parquet.
- It holds models for demand, wind and solar, a GB merit-order stack, and a model that clears the stack into a day-ahead price. It does not produce orders.
- Read the model cards
- elexon/indo | target
- open_meteo/historical_demand | weather, version 2
- elexon/fuelhh | WIND, the target
- open_meteo/historical_wind | 12 sites
- elexon/windfor | benchmark
- elexon/fuelhh | SOLAR, the target
- open_meteo/historical_solar | 6 sites
- elexon/bmunits_reference | units
- elexon/remit | availability
- elexon/fou2t14d | derating
- day_ahead.lgbm_demand.v1v2
- Day-ahead demand
- GB national demand outturn, half-hourly in MW, forecast a day ahead. LightGBM quantile regression, one model per quantile from 0.05 to 0.95, sorted so they never cross, with a conformal outer band. Version 2 adds weather and calendar features.
- Walk-forward backtest, 12 folds of 30 days, 1 September 2024 to 22 August 2026
- pinball, q0.5
- coverage, 5 to 95%
- v1
- 711.04 MW
- 0.893
- v2
- 599.72 MW
- 0.883
- v2 is scored with actual weather standing in for the forecast, so its score is optimistic.
- v1, fold 12, 20 and 21 August 2026: the median (olive) inside its 5 to 95% band, and the outturn from elexon/indo (ink). Run a55a829bc51c40b2, forecast issued at noon the day before.
- models.demand_forecast, models.demand_forecast_v2
- wind.lgbm_quantile.v1
- Wind generation
- GB wind outturn, half-hourly in MW, a day ahead. LightGBM quantile regression on weather at 12 sites, benchmarked against WINDFOR.
- A configuration, a model card and a training dataset exist. There are no forecasts or scores in gold.
- models.wind_forecast
- solar.lgbm_quantile.v1
- Solar generation
- GB solar, half-hourly, a day ahead. LightGBM quantile regression on weather at 6 sites, benchmarked against persistence.
- Its configured target, elexon/fuelhh SOLAR, holds no rows. A configuration and a model card exist; there are no forecasts or scores in gold.
- models.solar_forecast
- stack.gb.v1
- GB merit-order stack
- The GB supply curve for one settlement period: units ranked by short-run marginal cost, cumulative MW against GBP/MWh, floored at −500.
- It is built when called, with nothing to train. It is scored through the SMP model, and its curves are kept in gold with each SMP run.
- models.stack.build(as_of)
- fundamentals_smp.gb.v1
- Fundamentals SMP
- Clears the stack against realised residual demand (demand less wind, solar and signed netting) for every half-hour, and scores the price against Elexon MID APXMIDP, the GB day-ahead benchmark.
- mean bias
- MAE
- Headline, 18 August to 3 September 2026, 816 periods
- −151.80
- 151.80
- 13 monthly runs, 5 May 2025 to 4 May 2026, 17,520 periods
- −69.81
- 72.84
- GBP/MWh. In the headline run every period is under-predicted.
- models.fundamentals_smp.backtest(...)
- Daily mean price, 18 August to 3 September 2026
- Model clearing (gold) against APXMIDP (ink), daily means of the 816 half-hours in run 41de423cfc0b421e. A perfect-prognosis backtest: realised demand, wind and solar stand in for forecasts. Fuel and carbon prices are synthetic. APXMIDP mixes day-ahead and intraday trades. Clearing is floored at −500 GBP/MWh, which pulls some daily means below zero.
- Reading the scores
- Every score here is a backtest held in gold. Pinball loss at q0.5 is half the mean absolute error of the median forecast, in MW; coverage is the share of outturns inside the 5 to 95% band. A demand model passes when pinball is at most 1,500 MW, coverage is within 0.90 ± 0.05 and no quantiles cross.
- In a notebook
- Data sources
- Architecture
- Models
- About
- GitHub
- This site is MIT-licensed. gridflow is Apache-2.0.

Drawing and chart labels: bronze; silver; gold; substation; onshore wind; wind farm; solar farm; biomass; nuclear; CCGT; OCGT; 20 Aug; 12:00; 21 Aug; 5 to 95%; −100; 18 Aug; 25 Aug; 1 Sep; APXMIDP; model clearing

Alt text (aria-label) of drawings and charts:

- What the models forecast, drawn: pylons into a substation for national demand, a wind farm, a solar farm, and the plant fleet in merit order (biomass, nuclear, CCGT and OCGT). A cable runs down from each to its model, tapping the datasets it reads on the way.
- Day-ahead demand forecast for 20 and 21 August 2026, from gold forecasts run a55a829bc51c40b2, fold 12: the median forecast inside its 5 to 95 percent band, with the outturn line, in MW. Values run from 17,466 to 31,583 MW.
- Daily mean GB price, 18 August to 3 September 2026, GBP/MWh: the Elexon MID APXMIDP benchmark stays between about 90 and 167, while the fundamentals SMP model's clearing price sits below it every day, from −136.0 to 78.4.
