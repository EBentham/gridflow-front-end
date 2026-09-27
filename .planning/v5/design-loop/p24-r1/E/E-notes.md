claude-opus-5-5

# Designer E, "The datasheet": round 1 notes

Boards (1440 wide): E-fuelhh.dc.html 3095 px; E-system-prices.dc.html 3112; E-physical-flows.dc.html 3164; E-bmunits-reference.dc.html 3010. Generator: work/gen_e.py (heights measured in a browser, fed back via work/heights.json).

**Idea.** Every dataset gets the same sheet: a first screen that is one plate (real figure left, key-facts table right, how-to-get-it across the foot, all ending by ~890 px), then the detail in a fixed order down one side-head rail, descending the strata (topsoil, then silver for the table itself, then the deep for related links).

## CONTENT MODEL (order, budget)
1. Breadcrumb (vendor back-link) + H1 human name (<= 6 words) + dataset key at right (mono) + one-liner (pack identity, <= 20 words)
2. Figure: title (<= 10 words), real chart in a fixed 800x272 frame (plot box + direct-label column), caption with dataset, unit, window, aggregation (<= 40 words)
3. Key facts: always the same 7 rows (Vendor dataset, Grain, Cadence, History, Publication lag, Units, Volume), each value <= 8 words; "not established" stays in place
4. How to get it: Workbench call (gold swatch), silver relation (silver), vendor endpoint (bronze); note <= 16 words each
5. What it is (<= 60 words)
6. How it's used: 3 uses, title <= 4 words + line <= 16 words
7. Schema: source line + column/type/meaning (<= 14 words), lineage group marked
8. Sample rows: slice line + DataFrame (<= 8 rows, <= 7 columns)
9. Caveats: <= 3, bold lead + <= 32 words
10. Related: <= 4, key + <= 12 words
Changes: CLI cut (belongs on the vendor page); "facts" fixed to 7 rows for the series; related entries the pack marks unchecked dropped.

## Decisions
- Uncovered codes: no new colours. Unsigned codes with no slot (NPSHYD, COAL, OIL) take khaki and the khaki band is always named by its codes ("OTHER, NPSHYD, COAL, OIL"), never "other", which dissolves the OTHER clash. PS (signed, meaning undocumented) is khaki under an ink cross-hatch. INTELE has no rows in the window; it appears only in a caveat.
- Signed stacking: the zero line is the ground (1.6 px ink). Positives stack up, negatives down; the two signed series (INT* net, PS) are outermost so they fall below the line when negative. No abs, no clipping.
- BM Units: one figure, two scales: all 3,014 units in one bar to scale (499 typed in fuel colours, 2,515 null hatched), then the 499 enlarged as count bars by code. Counts only.
- ENTSOG: time-true axis 1 Aug to 21 Sep; the 38 empty days are a hatched span labelled "no rows in local silver"; dots per gas day, lines only within blocks; Bacton's zeros sit on the ground line.

## No-time-axis / sparse
The figure slot never changes size. A reference table fills it with a composition chart of the snapshot; a sparse series keeps a true time axis so the emptiness is visible.

## Verification
detect.mjs: [] on all four. Browser at 1440 (port 9583, stopped): root height = content height; 0 elements past the 80 px margins; 0 clipped elements; 0 overlapping SVG text boxes; get-it rows end at 846 / 865 / 889 / 826 px.

## Also
- Title-band scenery varies by vendor, keyed to the homepage cable map: substation for Elexon (and NESO), gas terminal for ENTSO-G and GIE (converter station for ENTSO-E, met mast for Open-Meteo). The only non-data variation.
- Removed accessories: the vendor-to-endpoint cable and an in-chart below-zero annotation.
- Optional one-word edits: the system-prices one-liner (pack text) says GBP/MWh while the page uses £/MWh.

## Could not do
Canvas render (support.js) not available; static copies used. 390 px reflow not built (layout is flow + grid, no absolute text).

## NEW COPY (verbatim)

### elexon/fuelhh
- H1: Generation outturn by fuel type
- Figure title: Generation by fuel code, 20 to 26 September 2026
- Caption: elexon/fuelhh silver, MW (axis in GW), settlement dates 20 to 26 September 2026. Hourly means, UTC; codes in one band are summed first. Positive values stack up from zero, negative ones down; the PS sign is not documented.
- Fact, Vendor dataset: FUELHH, Elexon Insights API
- Fact, Grain: settlement period × fuel_type
- Fact, Cadence: every 30 minutes
- Fact, History: 2021-09-01 to 2026-09-26, with gaps
- Fact, Publication lag: period end (30 min) on 99.82% of rows
- Fact, Units: MW; INT* and PS are signed
- Fact, Volume: 29,760 rows in August 2026
- Get-it note (Workbench): a pandas DataFrame; 6,720 rows for this range
- Get-it note (Silver relation): date column settlement_date
- What it is: Elexon’s half-hourly record of what GB generation produced, split by fuel-type code. Each settlement period carries one MW value per code: wind, gas, nuclear, biomass, hydro, pumped storage, coal, oil, other, and ten interconnectors, signed so that imports are positive. There is no solar code. gridflow keeps the codes as sent, one row each.
- Use: Fuel-mix features: Hourly wind, gas and nuclear outturn as inputs to a GB price model.
- Use: Net interconnector flow: Sum the INT* codes for GB net imports, or read each link on its own.
- Use: Scoring a wind forecast: WIND outturn is an observed series to score a wind forecast against.
- Caveat (adapted from pack): No solar. FUELHH has no solar code at all, so solar outturn has to come from another dataset.
- Caveat (adapted from pack): Eleven codes are signed: the ten INT* interconnectors (positive is import to GB) and PS. Negatives are routine: INTIRL is negative in 70.3% of all half-hours, PS in 54.7%.
- Caveat (adapted from pack): The code set changes over time: INTELEC starts 2021-09-14, INTVKL 2023-07-12 and INTGRNL 2024-03-19, and a stray INTELE has 9 zero rows on 2021-09-10. A half-hour holds 17 to 20 rows.
- Related, elexon/fuelinst: Instantaneous generation outturn by fuel type, from the same connector.
- Related, elexon/bmunits_reference: The BM Unit registry; it shares the fuel-type codes.
- Related, elexon/indo: Demand outturn, used to check the INT* sign convention.
- Related, neso_data_portal/historic_generation_mix: Where GB solar outturn is found.
- Sample caption: Silver rows for settlement date 2026-09-26, period 25 (11:00 UTC): 8 of that period’s 20 codes.

### elexon/system_prices
- H1: System sell and buy prices
- Figure title: System sell price, 19 to 22 September 2026
- Caption: elexon/system_prices silver, latest vintage per period, £/MWh, settlement dates 19 to 22 September 2026, times in UTC. Native half-hourly values, 192 of them, nothing averaged; SBP equals SSP in every period, so one line carries both.
- Fact, Vendor dataset: DISEBSP, Elexon Insights API
- Fact, Grain: settlement period × vendor publication
- Fact, Cadence: every 30 minutes
- Fact, History: 2021-09-01 to 2026-09-22, no dates missing
- Fact, Publication lag: median 52 min to 2023; about 24.7 h from 2024
- Fact, Units: £/MWh; net imbalance volume in MWh
- Fact, Volume: 3,770 rows in August 2026
- Get-it note (Workbench): reads the latest vintage: one row per period
- Get-it note (Silver relation): date column settlement_date; raw parquet keeps every vintage
- What it is: The GB imbalance (cash-out) prices Elexon publishes for each settlement period: the system sell price and system buy price in £/MWh, with the net imbalance volume in MWh. gridflow appends every publication the vendor makes, so a period can hold more than one row; the workbench reads only the latest.
- Use: Imbalance price modelling: The target series for a GB cash-out price forecast, negative prices included.
- Use: Pricing a forecast error: Value a generation or demand imbalance at the period’s system price.
- Use: Day-ahead spread: Set beside elexon/mid, which the workbench’s day-ahead benchmark reads.
- Caveat (adapted from pack): Silver is append-only: 96,793 rows cover 88,694 periods. Read the _latest view (the workbench does) or dedupe on available_at before plotting.
- Caveat (adapted from pack): SSP equals SBP on every row since 2021-09, so one line carries both.
- Caveat (adapted from pack): Negative prices are routine: 4,052 periods since 2021-09 (latest vintage), and 34 of the 192 in the figure.
- Related, neso/carbon_intensity: Joined to these prices by the workbench’s imbalance_context().
- Related, elexon/mid: Read by the workbench’s GB day-ahead benchmark.
- Sample caption: Silver rows for settlement date 2026-09-20, periods 22 to 29; one vintage each. system_buy_price equals system_sell_price on every row, so it is left out here.

### entsog/physical_flows
- H1: Physical gas flows
- Figure title: Daily flow at two GB points, every gas day held
- Caption: entsog/physical_flows silver, GWh/d, every gas day held locally. One native value a gas day as National Gas TSO reports it; nothing averaged or interpolated, and the line breaks where there are no rows.
- Fact, Vendor dataset: operationalData, Physical Flow indicator
- Fact, Grain: gas day × point × operator × direction
- Fact, Cadence: daily, on each operator’s gas day
- Fact, History: 1 to 5 Aug and 13 to 21 Sep 2026
- Fact, Publication lag: not established
- Fact, Units: GWh/d; flow can be null
- Fact, Volume: about 983 rows a gas day
- Get-it note (Workbench): gas days that start before midnight UTC fall outside the first day
- Get-it note (Silver relation): date column timestamp_utc
- What it is: ENTSOG’s physical-flow indicator: the gas that moved each gas day at interconnection points, LNG terminals and other points on Europe’s transmission systems. Operators on both sides of a point report it, each as entry or exit, so one point can appear once per operator and direction. gridflow normalises every value to GWh/d.
- Use: Border flows: Follow one point day by day, such as Bacton (IUK) exit.
- Use: Supply features: Daily entry flow at terminals such as St. Fergus as inputs to a gas price model.
- Use: Checking both sides: Compare two operators’ values at one point, as at Bacton (IUK) on 21 September.
- Caveat (adapted from pack): Local history is 14 gas days in two blocks: 1 to 5 August and 13 to 21 September 2026.
- Caveat (adapted from pack): Both sides of a point are reported, so summing every row double counts. At Bacton (IUK) on 2026-09-21, National Gas TSO exit and Interconnector entry are both 175.165952 GWh/d.
- Caveat (adapted from pack): Flows can be null: 2,499 rows, including every day for 176 series such as Avonmouth LNG entry. Do not zero-fill.
- Related, entsog/aggregated_physical_flows: The same Physical Flow indicator, aggregated by zone.
- Related, entsog/nominations: The same endpoint, Nomination indicator.
- Related, entsog/allocations: The same endpoint, Allocation indicator.
- Sample caption: Silver rows for gas day 2026-09-21 (timestamp_utc 04:00 UTC) at GB points; Avonmouth LNG reports a null flow.

### elexon/bmunits_reference
- H1: BM Unit reference data
- Figure title: BM units by fuel type, one snapshot
- Caption: elexon/bmunits_reference silver, count of BM units, snapshot of 26 September 2026. No time axis: all 3,014 units to scale, then the 499 with a fuel type by code. Counts only; capacities are not additive.
- Fact, Vendor dataset: reference/bmunits/all, Elexon Insights API
- Fact, Grain: BM Unit (bm_unit_id)
- Fact, Cadence: weekly snapshot, overwritten
- Fact, History: current snapshot only (2026-09-26)
- Fact, Publication lag: not established
- Fact, Units: MW, per registration
- Fact, Volume: 3,014 rows
- Get-it note (Workbench): not query(): its date column is ingested_at, so a date range returns 0 rows
- Get-it note (Silver relation): one file, overwritten on each run
- Get-it note (Vendor endpoint): no parameters, no pagination
- What it is: Elexon’s registry of Balancing Mechanism Units: one row per unit, with its name, fuel type, registered capacity, lead party and GSP group. gridflow keeps it as a single snapshot, overwritten on each run, so it describes the registry as it stands, not its history. Most units carry no fuel type.
- Use: Naming unit-level data: Join on bm_unit_id to label rows in elexon/boal or elexon/pn.
- Use: Grouping units by fuel: Map units to the fuel codes of elexon/fuelhh; 499 of 3,014 have one.
- Use: A party’s units: Filter on company_name to list the units a lead party registers.
- Caveat (adapted from pack): 83% of units have no fuel type (2,515 of 3,014), so a fuel breakdown covers only 499 units.
- Caveat (adapted from pack): Capacity is not additive: registered_capacity_mw is per registration, and the null-fuel rows alone sum to 727,551 MW.
- Caveat (adapted from pack): One snapshot, overwritten each run, and keyless vendor rows are dropped, so counts drift between runs: 2,969 on 2026-09-09, 3,014 on 2026-09-26.
- Related, elexon/boal: Per-unit data joined on bm_unit_id.
- Related, elexon/pn: Per-unit data joined on bm_unit_id.
- Related, elexon/uou2t14d: Per-unit availability.
- Related, elexon/fuelhh: Shares the fuel-type codes; interconnector flow is found there.
- Sample caption: Eight units from the 26 September 2026 snapshot.

### shared
- Headings: Key facts; How to get it; What it is; How it’s used; Schema; Sample rows; Caveats; Related datasets
- Fact labels: Vendor dataset; Grain; Cadence; History; Publication lag; Units; Volume
- Get-it labels: Workbench; Silver relation; Vendor endpoint
- Schema group row: Lineage, added by the base silver transformer; query() and tail() drop these
- Footer (invented; R3-final has none): Source on GitHub; MIT license
- Chart labels: “34 of 192 periods below zero”, “594.00 at 20:00 UTC, 22 Sep”, “−50.00 at 13:30 UTC, 20 Sep”, “no rows in local silver / 6 Aug to 12 Sep”, “0.0 GWh/d on 13 to 20 Sep, as reported”, “499 with a fuel type”, “2,515 with no fuel type (null)”, “the 499, by code; INT* is ten codes”, band labels “OTHER, NPSHYD, COAL, OIL”, “INT* (10 links, net)”, “PS (signed)”
