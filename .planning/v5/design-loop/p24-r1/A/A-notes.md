claude-opus-5-5

# Designer A, “The section”: notes

Boards (1440 wide): A-fuelhh.dc.html 3718 px, A-system-prices.dc.html 3712 px, A-physical-flows.dc.html 3582 px, A-bmunits-reference.dc.html 3578 px. Generator: gen_A.py + content.py + a.css; static copies in static/.

## Idea
The page is one geological section through the dataset, and one drawn feed cable follows that dataset down it: from the asset in the sky strip through topsoil, tapping bronze (the request), splicing to a silver core (the schema), splicing to gold (the notebook).

## CONTENT MODEL (ordered; word budgets)
Sky (petrol)
1. Breadcrumb: Data sources / vendor. ADDED: the vendor back-link the brief allows.
2. h1 dataset name, 5 words or fewer.
3. Identity line: gridflow key chip + vendor code and the vendor's own name, 16 words or fewer.
4. One-liner, 18 words or fewer.
5. Facts: grain, cadence, units, history, publication lag; 14 words or fewer each. MOVED up from mid-page: readers judge in seconds, and identity belongs in the sky.
6. Landscape strip of the source asset: drawing only, at most 5 labels of 3 words or fewer.
Topsoil
7. Chart heading naming the window (10 or fewer) + caption: dataset, unit, aggregation, sign rule (40 or fewer).
8. Chart + keyed index in stack order (9 entries or fewer; notes of 18 words or fewer).
9. What it is, 60 words or fewer.
10. How it's used: 2 to 3 uses of 14 words or fewer.
Bronze
11. The raw feed: note (30 or fewer) + vendor request + gridflow command(s), each with a comment of 6 words or fewer.
Silver
12. Schema: relation, schema class, transformer version (25 or fewer); table with a meaning of 14 words or fewer per column, key columns marked, lineage columns in one row.
13. Sample rows: caption (16 or fewer) + DataFrame, 8 rows, 6 columns or fewer, formatted as pandas prints them. KEPT in silver (they are silver rows); gold shows only the call.
Gold
14. Workbench: note (35 or fewer) + notebook with the setup cell and the exact call.
Deep (petrol)
15. Caveats: up to 3, bold lead phrase + 25 words or fewer.
16. Related datasets: up to 4, key + basis of 12 words or fewer.
17. Footer.
Margin glosses at each contact, 6 words or fewer. ADDED: they make the descent teach the medallion.

## Decisions
- Uncovered fuel codes are drawn unpainted: daylight fill with their own ink hatch (NPSHYD horizontal lines, PS cross-hatch, COAL and OIL dots), named by code in the key. They never fold into khaki, so khaki means only the vendor code OTHER, keyed as the vendor's own code with undocumented contents. INTELE (9 zero rows in 2021) is outside the window and not drawn.
- Signed series: unsigned codes stack up from zero (nuclear, biomass, NPSHYD, COAL/OIL, OTHER, gas, wind); the positive parts of net interconnectors (ten INT codes summed per half-hour) and PS stack on top; the negative parts hang below zero. Nothing is clipped. The PS sign is stated as undocumented, never called pumping.
- BMUNITS (no time axis): the topsoil figure becomes the snapshot's composition: one bar of all 3,014 units (2,515 plain daylight with no fuel type, 499 painted), with the 499 enlarged eight times below, by code. Counts only, no capacity. The heading names the snapshot date as the window; gold uses tail() and data.sql() and says why query() returns 0 rows.
- ENTSOG (sparse): a true time axis over every local gas day; the 38-day hole is a hatched band labelled "no rows held locally", and the lines are not joined across it. Bacton (IUK), an interconnector point, is olive; St. Fergus, a terminal, is clay.

## NEW COPY (verbatim)
Template (every page):

- The raw feed
- Schema and sample rows
- Query it from a notebook
- What it is
- How it’s used
- What to watch for
- Related datasets
- A square marks the columns that identify a row.
- bronze, the response as fetched
- silver, typed and validated
- gold, served to the notebook
- Added to every row by the silver base transformer
- MIT licence
- settlement date; each starts at 23:00 UTC
- gas day, drawn to scale
- Relation <relation>, typed by <Class> in <file>; transformer version <v>.

elexon/fuelhh:
- h1: Generation by fuel type
- identity: Elexon dataset FUELHH, “Half-hourly Generation Outturn by Fuel Type”
- one-liner: Great Britain’s generation outturn for every half-hour settlement period, one MW value per Elexon fuel-type code.
- fact Grain: One row per settlement period and fuel-type code
- fact Cadence: Every 30 minutes
- fact Units: MW
- fact History: 1 Sep 2021 to 26 Sep 2026 held locally; 7 to 9 Sep 2026 missing
- fact Publication lag: Published at the period end on 99.82% of rows
- chart heading: Generation by fuel, 20 to 26 September 2026
- caption: Silver elexon/fuelhh, MW, hourly: each point is the mean of an hour’s two half-hours, with a group’s codes summed first. Values stack above zero when positive and below it when negative; nothing is clipped.
- what it is: Elexon’s outturn by fuel type for each GB settlement period: one MW figure per code, from CCGT and wind to each interconnector. Recent half-hours carry 20 codes. The ten interconnector codes are signed, positive for imports to GB, and pumped storage (PS) is signed too, with the sign’s meaning undocumented. There is no solar code.
- use: Fuel-mix and residual-demand features for a GB power price model.
- use: Net interconnector flows by link, from ten signed codes.
- use: Checking a wind generation forecast against outturn.
- bronze note: From the Elexon Insights API. gridflow ingest writes the raw response to bronze; gridflow pipeline carries it on to silver.
- command comment: # bronze only
- command comment: # bronze to silver
- schema settlement_date: GB settlement date, taken from the vendor start time
- schema settlement_period: Half-hour of the day, 1 to 50 (46 or 50 on clock-change days)
- schema timestamp_utc: Start of the half-hour
- schema fuel_type: Elexon fuel-type code, uppercase as sent
- schema generation_mw: MW for the period. Interconnectors signed, positive is import; PS signed, meaning undocumented
- schema published_at: Vendor publish time
- schema data_provider: Always elexon
- schema ingested_at: When the silver transform ran
- sample caption: Silver rows for settlement date 2026-09-26, period 25: 8 of its 20 codes.
- gold note: Returns a pandas DataFrame from the DuckDB relation silver_elexon_fuelhh, filtered on settlement_date with both ends included: 6,720 rows for this week. Lineage columns are dropped.
- caveat: No solar. FUELHH has no solar code, so solar outturn has to come from another dataset.
- caveat: Eleven codes are signed: ten interconnectors (positive is import to GB) and PS. Negatives are routine: INTIRL is negative in 70.3% of half-hours.
- caveat: The code set changes. INTELEC arrives in 2021, INTVKL in 2023 and INTGRNL in 2024, so a half-hour holds 17 to 20 rows.
- related elexon/fuelinst: Instantaneous outturn by fuel type, from the same connector
- related neso_data_portal/historic_generation_mix: Where solar outturn lives
- related elexon/bmunits_reference: Shares the fuel-type codes
- related elexon/indo: Demand, used to check the interconnector sign

elexon/system_prices:
- h1: System sell and buy prices
- identity: Elexon dataset DISEBSP, “System Sell Price and System Buy Price per settlement period”
- one-liner: The GB imbalance price for each half-hour settlement period, with the net imbalance volume, in GBP/MWh.
- fact Grain: One row per settlement period per published version (append-only)
- fact Cadence: Every 30 minutes
- fact Units: GBP/MWh; net imbalance volume in MWh
- fact History: 1 Sep 2021 to 22 Sep 2026 held locally, no missing dates
- fact Publication lag: Median 52 min in 2021 to 2023, about 24.7 h in 2024 to 2026
- chart heading: System sell price, 19 to 22 September 2026
- caption: Silver elexon/system_prices, latest version of each period, GBP/MWh: 192 native half-hours, no aggregation. The buy price is identical in this window, so one line carries both.
- what it is: Elexon’s system sell price (SSP) and system buy price (SBP) are the cash-out prices that settle imbalances in each GB settlement period, in GBP/MWh. In every row held locally, from September 2021, the two are equal. Each row also carries the net imbalance volume in MWh and a price derivation code (N, P or K).
- use: The target for an imbalance price forecast.
- use: Pricing the cash-out exposure of a position left out of balance.
- use: Studying negative prices: 4,052 half-hours below zero since September 2021.
- bronze note: From the Elexon Insights API, one settlement date per request. gridflow ingest writes the raw response to bronze; gridflow pipeline carries it on to silver.
- command comment: # bronze only
- command comment: # bronze to silver
- schema settlement_date: GB settlement date
- schema settlement_period: Half-hour of the day, 1 to 50
- schema timestamp_utc: Start of the period
- schema system_sell_price: SSP, GBP/MWh
- schema system_buy_price: SBP, GBP/MWh; equal to SSP on every row
- schema net_imbalance_volume: NIV, MWh; sign convention undocumented
- schema run_type: Null on every row: this endpoint has no such field
- schema price_derivation_code: Vendor code: N, P or K
- schema published_at: Vendor created time; a new version adds a row
- schema data_provider: Always elexon
- schema ingested_at: When the silver transform ran
- sample caption: Silver rows for settlement date 2026-09-20, periods 22 to 29: one version each.
- gold note: Reads silver_elexon_system_prices_latest, so each period comes back once; the raw parquet keeps every version. Filtered on settlement_date, both ends included.
- caveat: Silver is append-only: 96,793 rows cover 88,694 periods. Read the _latest view, as the workbench does, or dedupe on available_at.
- caveat: SSP equals SBP on every row since September 2021, so one line carries both.
- caveat: Negative prices are routine: 4,052 periods since September 2021, and 34 of the 192 in the chart.
- related neso/carbon_intensity: Joined in the workbench by data.imbalance_context()
- related elexon/mid: Read by the workbench’s day-ahead benchmark
- related system_marginal_price: A gold view built over this table

entsog/physical_flows:
- h1: Physical gas flows
- identity: ENTSOG Transparency Platform, operationalData indicator “Physical Flow”
- one-liner: Daily gas flow at each European transmission point, per operator and direction, in GWh/d.
- fact Grain: One row per gas day, point, operator and direction
- fact Cadence: Daily; each operator’s gas day starts at its own hour
- fact Units: GWh/d
- fact History: 14 gas days held locally: 1 to 5 Aug and 13 to 21 Sep 2026
- fact Publication lag: Not established; available_at is the ingest time
- chart heading: Daily flow at two GB points, August and September 2026
- caption: Silver entsog/physical_flows, National Gas TSO, GWh/d: one native value per gas day, nothing averaged. These are all the gas days held locally; the gap has no rows and is not interpolated.
- what it is: ENTSOG’s Physical Flow indicator: for each gas day, the flow that each transmission operator reports at each point, marked entry or exit. gridflow normalises every value to GWh/d. Both sides of a cross-border point report, so one physical flow can appear twice. About 983 rows arrive per gas day.
- use: GB supply features for a gas price model: terminal and LNG entries.
- use: Tracking pipeline flows between GB and the continent, such as Bacton to Zeebrugge.
- bronze note: From the ENTSOG Transparency Platform, the whole system in one fetch. gridflow ingest writes the raw response to bronze; gridflow pipeline carries it on to silver.
- command comment: # bronze only
- command comment: # bronze to silver
- schema timestamp_utc: Start of the operator’s gas day
- schema point_key: ENTSOG point id, e.g. ITP-00005
- schema point_label: Point name, e.g. Bacton (IUK)
- schema operator_key: Reporting operator id, e.g. UK-TSO-0001
- schema operator_label: Operator name, e.g. National Gas TSO
- schema direction_key: entry or exit
- schema flow_gwh_per_day: Flow in GWh/d, normalised from the vendor unit; nullable
- schema unit: Always GWh/d
- schema data_provider: Always entsog
- schema ingested_at: When the silver transform ran; added by the transformer, not in the schema class
- sample caption: Silver rows for gas day 2026-09-21 at GB points (04:00 UTC).
- gold note: Filters timestamp_utc from 00:00 UTC on the start date to 00:00 UTC after the end date. Operators whose gas day starts at 21:00 to 23:00 UTC the day before miss the first day.
- caveat: Local history is 14 gas days in two blocks: 1 to 5 August and 13 to 21 September 2026.
- caveat: Both sides of a point report, so summing every row double counts: at Bacton (IUK) on 21 September, both sides read 175.165952 GWh/d.
- caveat: Flows can be null: 2,499 rows, and every day for 176 series such as Avonmouth LNG. Do not zero-fill.
- related entsog/aggregated_physical_flows: The same indicator at zone level
- related entsog/nominations: Same endpoint, Nomination indicator
- related entsog/allocations: Same endpoint, Allocation indicator

elexon/bmunits_reference:
- h1: Balancing Mechanism units
- identity: Elexon reference endpoint /reference/bmunits/all, “All BM Unit reference data”
- one-liner: The register of Balancing Mechanism units: id, name, fuel type, registered capacity, lead party and GSP group.
- fact Grain: One row per BM unit
- fact Cadence: Snapshot, scheduled weekly, overwritten each run
- fact Units: Registered capacity in MW, per registration
- fact History: Current snapshot only (26 Sep 2026)
- fact Publication lag: Not established
- chart heading: 3,014 BM units by fuel type, snapshot of 26 September 2026
- caption: Silver elexon/bmunits_reference, count of BM units in one snapshot; null is kept as its own group. Counts only: registered capacity is not additive, so it is not summed.
- what it is: Elexon’s reference list of registered BM units, fetched whole in one call and overwritten on every run. It is the lookup that turns a bm_unit_id in unit-level balancing data into a name, a lead party and, for 499 of 3,014 units, a fuel type. Registered capacity is per registration and does not add up.
- use: Joining BOAL or PN data to a unit’s lead party and fuel type.
- use: Grouping units by lead party or GSP group.
- bronze note: From the Elexon Insights API: no parameters and no pages. gridflow pipeline writes the raw response to bronze and carries it on to silver.
- command comment: # no dates: one fetch of the whole list
- schema bm_unit_id: Elexon BM unit id, e.g. T_DRAXX-1
- schema bm_unit_name: Vendor name; often repeats the id
- schema fuel_type: Vendor fuel type; null on 2,515 of 3,014 rows
- schema registered_capacity_mw: MW per registration; not additive across rows
- schema company_name: Lead party
- schema gsp_group_id: GSP group, e.g. _A; null on 1,822 rows
- schema national_grid_bm_unit: National Grid unit id, e.g. ABERU-1; not an ENTSO-E EIC
- schema data_provider: Always elexon
- schema ingested_at: When the silver transform ran
- sample caption: Silver rows from the snapshot of 2026-09-26, chosen across id prefixes.
- gold note: Use tail() or data.sql(). A query() date range filters this table on ingested_at, so it returns 0 rows.
- caveat: 83% of units have no fuel type (2,515 of 3,014), so any fuel breakdown covers 499 units.
- caveat: Capacity does not add up: it is per registration, and the null-fuel rows alone sum to 727,551 MW.
- caveat: One snapshot, overwritten each run, with keyless vendor rows dropped, so counts drift: 2,969 units on 9 September, 3,014 on 26 September.
- related elexon/boal: Bid-offer acceptances, joined on bm_unit_id
- related elexon/pn: Physical notifications, joined on bm_unit_id
- related elexon/uou2t14d: Availability per unit
- related elexon/fuelhh: Shares the fuel-type codes; interconnector flow lives there

Chart keys and drawing labels:
- fuelhh key: Pumped storage PS: Signed; the vendor does not say what the sign means. Drawn above or below zero as it falls. | Interconnectors, net INT*, 10 codes: Positive is import to GB; below zero, net export. | Wind WIND | Gas CCGT, OCGT | Other OTHER: The vendor’s own code; what it holds is undocumented. | Hydro, not pumped NPSHYD: 244 to 893 MW here. | Coal and oil COAL, OIL: Stacked, but 66.5 MW at most here: too thin to see. | Biomass BIOMASS | Nuclear NUCLEAR. Band labels: nuclear, biomass, other, gas, wind, net imports, net exports.
- system_prices key: System sell price system_sell_price: Equal to system_buy_price on every row. | Below zero: 34 of 192 half-hours. Lowest −50.00 at 13:30 UTC on 20 September; highest 594.00 at 20:00 UTC on 22 September. Labels: lowest, −50.00; highest, 594.00.
- physical_flows key: St. Fergus, entry ITP-00022: 350.3 to 594.6 GWh/d. | Bacton (IUK), exit ITP-00005: 0.0 on 13 to 20 September, 175.2 on the 21st, as reported. | No rows: Nothing held locally for these 38 gas days; the lines are not joined across the gap. Labels: no rows held locally / 6 August to 12 September; St. Fergus entry; Bacton (IUK) exit.
- bmunits key: No fuel type: 2,515 units, 83% of the register. | Palette colours: Wind, gas, nuclear, interconnectors, biomass and OTHER, as in every chart on this site. | Unpainted NPSHYD, PS, COAL: Codes the palette has no colour for, drawn in daylight with their own hatch. Labels: all 3,014; no fuel type, 2,515; with a fuel type, 499; the 499, at eight times the scale; ten codes, 1 unit each but INTELEC (2).
- Landscape labels: onshore wind, gas-fired power station, substation, interconnector, offshore wind, transmission lines, battery storage, gas terminal, offshore platform, landfall.

## Verification
- impeccable detect.mjs --json on each static copy: [] (all four).
- Layout measured in the browser at 1440 with fonts loaded: every section's content bottom is inside its section; no text blocks overlap; no clipped pre, table or p; nothing outside x 80..1360 except the full-bleed sections; root height equals the $preview height.
