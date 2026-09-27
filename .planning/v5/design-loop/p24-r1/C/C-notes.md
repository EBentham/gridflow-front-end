claude-opus-5-5

# Designer C, "The plate": round 1 notes

## Boards (all in this folder; generator build_c.py + gen_c.py + c.css; static copies in static\)
- C-fuelhh.dc.html, 1440 x 4413
- C-system-prices.dc.html, 1440 x 4246
- C-physical-flows.dc.html, 1440 x 4354
- C-bmunits-reference.dc.html, 1440 x 4295

## The idea
The real series is drawn as a full-width, hand-labelled plate on the topsoil straight under a short petrol sky; the text then descends the pipeline in the order the data travels: raw call in bronze, schema and rows in silver, workbench call in gold, related in the deep.

## CONTENT MODEL (order, word budget)
1. Sky: vendor back-link; h1 dataset name (<=6 words); id line (gridflow key, vendor code/name); one-liner (<=25).
2. Plate (topsoil): title with window (<=9); plate note stating dataset, unit, window, aggregation (<=55); drawing 1280 wide, direct lower-case italic labels, at most 2 value callouts.
3. What it is (<=60).
4. How it's used: 3 uses (<=18 each).
5. Facts: 6 pairs, grain / cadence / unit / local history / publication lag / rows (<=15 each). "Not established" is printed, not dropped.
6. Caveats: <=3, bold lead + <=40.
7. From the vendor (bronze): endpoint well, CLI well, optional note (<=12).
8. Silver schema (silver): column / dtype / meaning (<=15 per row) + one lineage line (<=35).
9. Sample rows (silver): DataFrame-styled, <=8 rows, caption (<=30).
10. In the workbench (gold): setup cell + the exact call(s) from the pack; note (<=40). Slot is not hard-wired to query(): BMUNITS shows tail() and sql().
11. Related (deep): 3-4 dataset keys, one line each (<=12); footer.
Changes vs the proposal: caveats moved up beside facts (they qualify the plate the reader just saw); "how to get it" split into bronze (raw endpoint + CLI) and gold (workbench) so the page descends in data order; related moved into the deep stratum as navigation.

## Decisions the pack left open
- Uncovered fuel codes: the khaki family, told apart by hatch. Plain khaki = the vendor code OTHER only (labelled "other (vendor code OTHER)", which resolves the name clash). NPSHYD = khaki + daylight ripple ("hydro, NPSHYD"); PS = khaki + ink diagonal; COAL and OIL = khaki + stipple, drawn and stated on the plate ("coal, at most 66 MW, and oil, 0 MW"); INTELE joins the olive INT group (no rows in the window; named in caveat 3). The same glyphs mark the BMUNITS census.
- Signed series in FUELHH: every code split by sign. Positives stack up from zero (nuclear, biomass, hydro, coal/oil, gas, OTHER, PS+, interconnector imports, wind on top); negatives stack down (interconnector exports, then PS where negative). Nothing netted or clipped; the stack top is never labelled a total; PS negatives carry no cause word; the plate note states "positive means import to GB".
- BMUNITS: a census plate, one square per row (3,014). 499 typed units in fuel_type rows, 2,515 nulls as a hollow-square field, bracketed "2,515 units, 83%, with none". Capacity is not drawn.
- ENTSOG sparse window: all 14 gas days as paired daily bars (St. Fergus entry clay; Bacton (IUK) exit clay with daylight hatch); the 38-day hole is drawn as a geological unconformity through the axis, labelled "no rows in local silver, 6 Aug to 12 Sep (38 gas days)"; reported zeros are ink dashes labelled 0, visibly distinct from the break; every bar carries its value, so the plate is dense without invention.
- Line plates are shorter (380 px plot vs 470 for the stack) so the price plate is not empty; the 594.00 spike keeps a true linear scale.
- h1 steps down to the 52 px set-piece token so the plate starts 499-543 px down (above a 900 px fold).
- Accessory removed: the bronze rail's sub-line.

## No-time-axis and sparse cases
Reference tables get a census plate (one mark per row, nulls kept); sparse series get an unconformity break and per-bar values. Captions state the gap or the snapshot, never a cause.

## Verification
- Detector (static copies, run from the repo root): [] on all four.
- Browser (Python http.server on port 9533, own tab), measured at a true 1440 width in an iframe: content bottom == root height == $preview on all four; 0 collisions among plate labels (29/21/61/29 labels); 0 overlapping text blocks; no text past the 80 px margins; no plate text outside its SVG.
- 390 px plausibility: root overridden to 390, the media block reflows to one column, scrollWidth 390, nothing crosses the edge (wells, DataFrame and notebook scroll internally; the schema table stacks).

## Could not do
- A phone plate: at 358 px the 1280 plate scales to about 28% and its labels become unreadable. The build phase should render a separate phone plate (last 72 hours; label column becomes a keyed list under the drawing).
- Screenshots stall after scrolling at 1440; used 800 px 1:1 crops plus the numeric checks above.
- The Browser pane is shared: another designer's board loaded in my first tab once; I moved to my own tab and used nothing from it.

## NEW COPY (verbatim)
Shared template lines: "What it is", "How it’s used", "Facts", "Caveats", "From the vendor", "Silver schema", "Sample rows", "In the workbench", "From gridflow-models.", "Pydantic class <X>; transformer version <v>.", "Related", "Code on GitHub", "MIT licence", fact labels "Grain", "Cadence", "Unit(s)", "Local history", "Publication lag", "Rows", CLI comments "bronze only", "bronze to silver", "dates are ignored".

Plate labels:
- fuelhh: "wind", "nuclear", "gas, CCGT and OCGT", "interconnector imports", "interconnector exports", "pumped storage, PS", "pumped storage, where negative", "other (vendor code OTHER)", "coal, at most 66 MW, and oil, 0 MW", "hydro, NPSHYD", "biomass", "wind at its week high, 16,011 MW (19 Sep 23:00 UTC)", "at its week low, 1,326 MW (22 Sep 16:00 UTC)", "hours in UTC".
- system-prices: "the window’s high, 594.00 £/MWh at 20:00 UTC on 22 Sep", "its low, −50.00 £/MWh at 13:30 UTC on 20 Sep", "system sell price (the buy price is identical)", "below zero in 34 of 192 half-hours", "half-hours in UTC".
- physical-flows: "no rows in local silver, 6 Aug to 12 Sep (38 gas days)", "St. Fergus, entry", "Bacton (IUK), exit: reported as 0.0 on each gas day, 13 to 20 Sep", "gas days".
- bmunits-reference: "each square is one row: one BM unit registration, 3,014 in the snapshot", "499 units with a fuel type", "2,515 units, 83%, with none", "interconnectors, 10 codes".

Per page:
### fuelhh
- title (h1): Generation by fuel type
- one-liner: GB generation outturn by fuel type: one MW value for every half-hour settlement period and every Elexon fuel code, interconnectors included.
- plate title: Generation by fuel, 20 to 26 September 2026
- plate note: Source elexon/fuelhh, silver, MW. Settlement dates 20 to 26 September 2026, by UTC hour: each code is the mean of its two half-hours, summed within a band, never averaged across fuels. Signed codes split by sign, positive stacking up from zero and negative down; for interconnectors, positive means import to GB.
- what it is: Elexon publishes GB generation outturn for every settlement period, split by fuel type. gridflow keeps one row per settlement date, period and fuel code: twenty codes today, from WIND, CCGT and NUCLEAR to pumped storage and ten interconnectors. The interconnector codes are signed, positive for imports to GB. There is no solar code.
- use: Wind and gas output by half-hour, as features for a GB price or imbalance model.
- use: Interconnector flows border by border, read from the signed INT codes.
- use: Outturn to score a wind generation forecast against, half-hour by half-hour.
- caveat: No solar. FUELHH has no solar code at all, so solar outturn has to come from another dataset.
- caveat: Eleven codes are signed. The ten INT codes (positive = import to GB) and PS, whose sign is undocumented. Negatives are routine: INTIRL is negative in 70.3% of half-hours, PS in 54.7%.
- caveat: The code set changes. INTELEC starts on 14 Sep 2021, INTVKL on 12 Jul 2023 and INTGRNL on 19 Mar 2024, so a half-hour holds 17 to 20 rows. A stray INTELE has nine zero rows on 10 Sep 2021.
- sample caption: Settlement date 2026-09-26, period 25: 8 of the 20 codes. Every row also carries data_provider elexon and dataset_version 2.0.0.
- workbench note: Returns a pandas DataFrame: 6,720 rows for that range, with event_time, available_at, source_run_id and dataset_version left out. "fuel_generation" names the same table.
- related (elexon/fuelinst): Same connector: instantaneous generation outturn by fuel type.
- related (elexon/bmunits_reference): The BM unit register, which uses the same fuel-type codes.
- related (elexon/indo): The demand series the interconnector sign is checked against.
- related (neso_data_portal/historic_generation_mix): Where solar outturn lives.
### system-prices
- title (h1): System sell and buy prices
- one-liner: GB imbalance (cash-out) prices for every half-hour settlement period: the system sell and buy price in £/MWh, with the net imbalance volume.
- plate title: System sell price, 19 to 22 September 2026
- plate note: Source elexon/system_prices, silver, latest vintage per period, £/MWh. Settlement dates 19 to 22 September 2026, in UTC. Native half-hourly values, no aggregation. The buy price is identical in every period, so one line carries both.
- what it is: For each settlement period Elexon publishes the system sell price (SSP) and system buy price (SBP), the prices imbalances are cashed out at, with the net imbalance volume (NIV) in MWh. The two prices are equal on every row gridflow holds. Silver keeps every vintage the vendor sends, so a period can appear more than once.
- use: The target series for an imbalance price forecast.
- use: Valuing a position’s imbalance exposure, half-hour by half-hour.
- use: Finding and counting negative-price periods, which are routine.
- caveat: Silver is append-only. 96,793 rows cover 88,694 periods. Read the latest view, as the workbench does, or dedupe on available_at before plotting.
- caveat: SSP equals SBP. On every row since September 2021, so one line carries both.
- caveat: Negative prices are routine. 4,052 periods since September 2021 and 34 of the 192 in the chart above.
- sample caption: Settlement date 2026-09-20, periods 22 to 29, one vintage each; run_type is null on every row.
- workbench note: Reads silver_elexon_system_prices_latest, so vintages are already collapsed to one row per period; the raw parquet is not. data.imbalance_context(start, end) adds NESO carbon intensity.
- related (neso/carbon_intensity): Joined to these prices in the workbench’s imbalance context.
- related (elexon/mid): The workbench’s GB day-ahead benchmark.
- related (system_marginal_price): A gold view built over this table.
### physical-flows
- title (h1): Physical gas flows
- one-liner: Daily physical gas flow in GWh/d for each operator, point and direction on Europe’s transmission systems.
- plate title: Daily flow at two GB points, all 14 gas days held
- plate note: Source entsog/physical_flows, silver, GWh/d, National Gas TSO rows. Every gas day in local silver: 1 to 5 August and 13 to 21 September 2026, one native value per day, nothing averaged. The axis breaks where there are no rows.
- what it is: Each transmission operator reports the gas that physically crossed each of its points, per gas day and direction. gridflow keeps one row per point, operator, direction and gas day, normalised to GWh/d: about 983 rows a day across 620 points and 48 operators. Both sides of a point report, and some flows are null.
- use: Supply by entry point, terminals and LNG included, for a gas balance model.
- use: Flows at the points joining GB to the continent.
- use: Checking physical flow against nominations and allocations at the same point.
- caveat: Fourteen gas days. Local history is 1 to 5 August and 13 to 21 September 2026, in two blocks.
- caveat: Both sides report. Summing every row double counts: at Bacton (IUK) on 2026-09-21, National Gas TSO exit and Interconnector entry are both 175.165952 GWh/d.
- caveat: Flows can be null. 2,499 rows, and every day for 176 series such as Avonmouth LNG entry. Do not zero-fill.
- sample caption: Gas day 2026-09-21, timestamp_utc 2026-09-21T04:00Z, GB-side points. Avonmouth LNG shows a null flow.
- workbench note: Filters timestamp_utc from 13 Sep 00:00 UTC to before 22 Sep 00:00 UTC, so operators whose gas day starts at 21:00 to 23:00 UTC the day before miss the first day.
- related (entsog/aggregated_physical_flows): The same indicator, aggregated to zone level.
- related (entsog/nominations): Same endpoint, the Nomination indicator.
- related (entsog/allocations): Same endpoint, the Allocation indicator.
### bmunits-reference
- title (h1): BM unit reference data
- one-liner: A snapshot of Balancing Mechanism unit registrations: id, name, fuel type, registered capacity, lead party and GSP group.
- plate title: Registered BM units by fuel type
- plate note: Source elexon/bmunits_reference, silver snapshot ingested 26 September 2026. No time axis: a count of units, one square per row, grouped by fuel_type with nulls kept. Capacity is not drawn: it is per registration and does not add up.
- what it is: Elexon’s register of Balancing Mechanism units, one row per unit id. gridflow fetches the whole list in one call and overwrites a single file each run, so silver holds the current snapshot only. Fuel type is filled for 499 of the 3,014 units, with the same codes as FUELHH.
- use: Mapping per-unit datasets such as boal and pn to a fuel type and lead party.
- use: Selecting every unit of one technology, such as all WIND units.
- use: Linking unit registrations to FUELHH’s fuel codes.
- caveat: Most units have no fuel type. 2,515 of 3,014 (83%), so a fuel breakdown covers only 499 units.
- caveat: Capacity does not add up. It is per registration: the untyped rows alone sum to 727,551 MW, and 1,315 ids start I_, which the docs describe as per-party interconnector registrations.
- caveat: Counts drift between runs. One snapshot, overwritten each run, with keyless vendor rows dropped: 2,969 units on 2026-09-09, 3,014 now.
- sample caption: Eight units from the 2026-09-26 snapshot, including one each of the I_, 2__ and V__ id patterns.
- workbench note: Not query(): this table’s date column is ingested_at, so a date range such as January 2026 returns 0 rows. tail() reads the newest rows; sql() is read-only.
- related (elexon/boal): A per-unit dataset joined on bm_unit_id; the transformer measures this join’s coverage.
- related (elexon/pn): A per-unit dataset joined on bm_unit_id.
- related (elexon/uou2t14d): Per-unit availability.
- related (elexon/fuelhh): Shares the fuel-type codes; interconnector flow lives there.