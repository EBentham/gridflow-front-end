# v5 Phase 22: proposals for Bobbo to rule (families, page set)

Written 2026-09-27 by the Phase 22 data-truth agent (claude-opus-5-5). Every recommendation here is a
proposal; nothing is applied. Evidence: `DATA-MATRIX.md/.json` (one row per dataset), `ingest-receipts/`,
`DISCREPANCIES.md`.

Rule used: a family is proposed only when its members differ by a window, horizon, selector, boundary or
indicator parameter over the same kind of row. Datasets that differ in grain or use stay singletons even
when their names look alike (FUELHH vs FUELINST, NETBSAD vs DISBSAD, FOU2T14D vs UOU2T14D).

Evidence column: **S** = members share one gridflow schema class; **E** = same endpoint, different
parameter; **H** = same measure at another horizon or boundary. Families count only datasets that stay in
the page set (see D4 below).

## D5 families

### Elexon (33 datasets → 25 pages if all accepted)

| # | family (proposed page) | members | evidence | recommend |
|---|---|---|---|---|
| EL-A | Indicated day and day-ahead (NGC) | `indgen`, `inddem`, `imbalngc`, `melngc` | H: same NGC publication and settlement keys, one measure each (generation, demand, imbalance, margin) | **yes**: one row shape, four measures; one page with a measure switch |
| EL-B | Demand outturn | `indo`, `itsdo`, `indod` | H: one outturn at two boundaries plus its daily total | **yes**: the canonical note now stresses that ITSDO is higher than INDO; that relationship belongs on one page |
| EL-C | Demand forecasts | `ndf`, `ndfd`, `tsdf`, `tsdfd` | S (`ElexonDemandForecast` for ndf/ndfd) + H (day-ahead vs 2–14 day, national vs transmission) | **yes**: one forecast at two horizons and two boundaries |
| – | not proposed | `fou2t14d`/`uou2t14d`, `netbsad`/`disbsad`, `fuelhh`/`fuelinst`, `agpt`/`agws` | different grain (fuel vs BM unit, net vs disaggregated, 30-min vs 5-min) | **no, keep singletons**; FUELHH is also the Phase 24 specimen |

### ENTSO-E (36 with silver → 24 pages if all accepted)

| # | family | members | evidence | recommend |
|---|---|---|---|---|
| EE-A | Load forecast horizons | `load_forecast`, `load_forecast_weekly`, `load_forecast_monthly`, `load_forecast_yearly` | S (3 share `EntsoeLoadForecast`) + H (A65, processType A01/A31/A32/A33) | **yes**: textbook horizon variants; `actual_load` stays its own page |
| EE-B | Unavailability (outages) | `outages_generation`, `outages_production`, `outages_consumption`, `outages_transmission`, `outages_offshore_grid` | E: one unavailability document family (A76–A80) split by asset type | **yes**: one page with an asset-type switch; generation (A80) vs production (A77) units is a distinction a reader needs side by side |
| EE-C | Congestion management | `redispatching_internal`, `redispatching_cross_border`, `countertrading`, `congestion_management_costs` | S (`EntsoeTransmissionMarketQuantity` for the first three) + one topic (TSO remedial actions and their cost) | **yes (lean)**: they only make sense together; countertrading has 12 rows and redispatching_cross_border 288 (6–9 Jul only) |
| EE-D | Capacity allocated and nominated | `total_capacity_allocated`, `total_nominated_capacity` | S + E: A26 with businessType A29 / B08 | **yes (lean)**: two businessType slices of one document |
| EE-E | Balancing energy bids | `balancing_energy_bids`, `aggregated_balancing_energy_bids` | S (`EntsoeBalancingEnergyBid`) | **yes**: per-bid and aggregated views of the same bids |
| – | not proposed | `installed_capacity`/`installed_capacity_units`, `actual_generation`/`actual_generation_units`, `generation_forecast`/`wind_solar_forecast` | different documents and grain | **no**; `actual_generation` (generation by PSR type) is the locked cross-vendor proof and must stay its own page |

### NESO Carbon Intensity (33 → 5 pages if all accepted)

| # | family | members | evidence | recommend |
|---|---|---|---|---|
| NE-A | National carbon intensity | `carbon_intensity`, `intensity_at`, `intensity_current`, `intensity_date`, `intensity_fw24h`, `intensity_fw48h`, `intensity_period`, `intensity_pt24h`, `intensity_today` | S (`CarbonIntensity`, all 9) + E (window variants of `/intensity`) | **yes**: nine windows onto one series; the page lists the endpoints |
| NE-B | Regional carbon intensity | 18: `regional_intensity` and its `_fw24h`/`_fw48h`/`_pt24h` windows, each also by `_postcode` and `_regionid`; plus `regional_current`, `regional_england`, `regional_scotland`, `regional_wales`, `regional_postcode`, `regional_regionid` | S (`RegionalIntensity`, all 18) + E (window × selector) | **yes**: the strongest case in the catalogue. Alternative if one page reads too long: split "all regions" from "one region" (2 pages) |
| NE-C | Generation mix | `generation`, `generation_current`, `generation_pt24h` | S (`GenerationMix`) + E | **yes** |
| NE-D | Intensity statistics | `intensity_stats`, `intensity_stats_block` | S (`CarbonIntensityStats`) | **yes** |
| – | singleton | `intensity_factors` | own schema (fuel emission factors, no time axis) | keep |

The "current" and "today" endpoints return one snapshot per call (1–162 rows after one ingest tonight). On
their own they can never carry a meaningful chart, which is a further reason to fold them into NE-A/B/C.

### ENTSO-G (32 with silver → 9 pages if all accepted)

| # | family | members | evidence | recommend |
|---|---|---|---|---|
| EG-A | Capacity by indicator | `firm_available`, `firm_booked`, `firm_technical`, `interruptible_available`, `interruptible_booked`, `interruptible_total`, `available_through_oversubscription`, `available_through_surrender`, `available_through_uioli_long_term`, `available_through_uioli_short_term` | E: `/operationalData?indicator=…`, one generic transformer each | **yes**: ten indicator values of one endpoint |
| EG-B | Gas quality | `gcv`, `wobbe_index`, `methane_content`, `hydrogen_content`, `oxygen_content` | E: same endpoint, quality indicators | **yes** |
| EG-C | Nominations and allocations | `nominations`, `renominations`, `allocations` | E: same endpoint, commercial-flow indicators | **yes**; `physical_flows` stays its own page (own curated schema `EntsogPhysicalFlow`; Phase 24 specimen) |
| EG-D | Congestion management procedures (CMP) | `cmp_auction_premiums`, `cmp_unavailable_firm_capacity`, `cmp_unsuccessful_requests` | one CMP topic, three endpoints | **yes** |
| EG-E | Reference data | `operators`, `balancing_zones`, `connection_points`, `interconnections`, `aggregate_interconnections`, `operator_point_directions` | no time axis; point and operator master data (27–1,225 rows each, ingested tonight) | **yes**: one "who and where" page that the flow pages link to |
| EG-F | Tariffs | `tariffs`, `tariff_simulations` | one topic, published vs simulated | **yes (lean)** |
| – | singletons | `physical_flows`, `aggregated_physical_flows`, `urgent_market_messages` | distinct endpoints and uses | keep |

### GIE (6 with silver → 4 pages if all accepted)

| # | family | members | evidence | recommend |
|---|---|---|---|---|
| GI-A | AGSI reference ("about") | `about_listing`, `about_summary` | E: both `/api/about` (flat vs hierarchical) | **yes** |
| GI-B | AGSI storage | `storage`, `storage_reports` | E: both AGSI `/api`, country vs aggregate/company/facility levels | **yes (lean)** |
| – | singletons | `lng`, `unavailability` | different endpoints (ALSI; `/api/unavailability`) | keep |

### Open-Meteo (6 → 3 pages if all accepted)

| # | family | members | evidence | recommend |
|---|---|---|---|---|
| OM-A | Demand weather | `forecast_demand`, `historical_demand` | S (`DemandWeather`) + H (forecast vs ERA5 archive) | **yes** |
| OM-B | Solar weather | `forecast_solar`, `historical_solar` | S (`SolarWeather`) + H | **yes** |
| OM-C | Wind weather | `forecast_wind`, `historical_wind` | S (`WindWeather`) + H | **yes** |

### NESO Data Portal (3 → 3): all singletons.

## D4 page set

**Rule:** a page exists only for a dataset that gridflow ingests AND that has local silver, so it can
carry a real chart and real sample rows. Coverage truth is gridflow's: a dataset that starts returning
data later (for example after a gridflow fix) re-enters through the matrix.

### Dropped or held (45 page slots on today's site)

| group | datasets | why | recommend |
|---|---|---|---|
| NESO Data Portal stubs (29) | the 29 `neso_data_portal/*` coming-soon pages (`aahedc_tariffs` … `weekly_wind_availability`) | no vault note, no gridflow connector; manufactured by `build_dataset_stubs_from_landings` from landing links | **drop** (already ratified in D4) |
| ENTSO-E, no data for gridflow's domains (10) | `activated_balancing_prices`, `congestion_income`, `contracted_reserves`, `cross_zonal_balancing_capacity`, `imbalance_prices`, `imbalance_volume`, `offered_transfer_capacity_continuous`, `offered_transfer_capacity_explicit`, `offered_transfer_capacity_implicit`, `transfer_capacity_use` | gridflow ingests them, but ENTSO-E answered every request for gridflow's domains (GB control area; GB and continental borders) with "No matching data" (Acknowledgement 999): 22–25 Sep, then again over a month-aligned 1 Jul – 31 Aug retry (62–496 requests each). The canonical notes already record the Brexit gap for 8 of the 10 and the acknowledgements for `transfer_capacity_use`; `cross_zonal_balancing_capacity` records neither. (`redispatching_cross_border` was in this group until the retry found 288 rows.) | **drop from the site**; keep the vault notes (they correctly document an empty feed) |
| ENTSO-E, monthly and still empty (1) | `balancing_financial_expenses_income` | GB control area, still empty over a month-aligned July–August retry | **drop** |
| ENTSO-E, not wired in gridflow (2) | `activated_balancing_qty` (a transformer exists but it is not in `sources.yaml`, so `gridflow ingest` rejects it); `commercial_schedules_net_positions` (no config, no transformer; the vault titles it "Deprecated" and the catalogue marks it a duplicate pointer) | not ingested by gridflow | **drop**; the `activated_balancing_qty` config gap is gridflow work, not this milestone |
| ENTSO-G, vendor empty (1) | `interruptions` | 268 daily requests, 2026-01-01 → 2026-09-26, every body `{"message":"No result found"}` | **drop** |
| GIE news (2) | `news`, `news_item` | 2.6 MB of real announcements in bronze, but the transform writes 0 rows (cause unconfirmed; candidate: its date-window filter drops announcements dated before the partition day); `news_item` depends on `news` | **hold** (unpublished) and open a gridflow unit for the news transform; low value for this audience either way |

### What remains

| vendor | datasets with silver (documented) | pages, families accepted | pages, no families |
|---|---:|---:|---:|
| Elexon | 33 | 25 | 33 |
| ENTSO-E | 36 | 24 | 36 |
| ENTSO-G | 32 | 9 | 32 |
| NESO Carbon Intensity | 33 | 5 | 33 |
| GIE | 6 | 4 | 6 |
| Open-Meteo | 6 | 3 | 6 |
| NESO Data Portal | 3 | 3 | 3 |
| **total** | **149** | **73** | **149** |

### Headline number (replaces "165 datasets" on `index.html` and `data-sources.html`)

**Recommend: "149 datasets".** That is the number of datasets the site documents, and each one has
checked local silver behind it. With families accepted, the data-sources landing can say "149 datasets on
73 pages"; the homepage keeps "149 datasets". Rejected alternatives: 165 (counts 16 datasets with no data,
including a deprecated pointer); 163 (gridflow's `sources.yaml`, which still counts 14 datasets that return no silver); 73 (the page count, which undersells the catalogue and hides the variants).

Phase 26 shrinks with it: 73 author/review units instead of 165, about 18–29M tokens at the milestone's
250–400k per page, before the pilot re-measures.
