claude-opus-5-5

# Designer B, "The reference manual": round 1 notes

## Boards (1440 wide; root height = $preview = measured footer bottom)
- B-fuelhh.dc.html: 3808
- B-system-prices.dc.html: 3572
- B-physical-flows.dc.html: 3757
- B-bmunits-reference.dc.html: 3587
Generator: gen_B.py (one template function, one copy dict per specimen; reads ../pack/specimens.json). Static copies in static/.

## The idea
A reference manual on one grid: a 280 px fact rail that stays level while you read, and a 944 px reading column. The grid is set in the petrol band, and the chart's keyed index names every code the drawing uses.

## CONTENT MODEL (ordered; word budgets)
1. Band: breadcrumb (Data sources / vendor); mono key `vendor/dataset` on the h1 baseline; vendor code and name (pack) | h1, 2 to 5 words; lede, 20 words max.
2. Fact rail (sticky in build, 280 px; each value 20 words max): Grain, Cadence, History + coverage strip drawn to scale, Publication lag, Units, Rows, Silver table, Workbench call (the pack call, broken at argument commas: whitespace only).
3. Chart: heading "<what>, <window>" (10 words max); plot + keyed index naming every code; caption 60 words max: dataset, layer, unit, window, aggregation.
4. What it is: 60 words max.
5. How it's used: 3 uses, 16 words each max.
6. Caveats: 3, each a bold lead clause + 30 words max.
7. Schema (side-head row): note, 20 words max (class, file, transformer version); table column / type / meaning (18 words max); lineage folded into one row.
8. Sample rows: note, 30 words max (slice, constant columns); DataFrame, values as stored.
9. How to get it: workbench cells (setup + exact call) + note, 45 words max; vendor endpoint, one query parameter per line; CLI from the pack.
10. Related datasets: 2 to 4, mono link + 12 words max each.
11. Footer: one wavy contact line into the granite deep; brand, the homepage About sentence, nav, the four About links.

Changes to the proposal, one line each:
- Auth dropped: the pack does not establish it.
- Vendor code and name moved to the band: identity, not a fact to scan.
- Rows and Silver table added: where to query and how big.
- Coverage strip added under History: sparse, gapped or snapshot history shows at a glance.
- Workbench call shown twice (rail for copying, full cells in How to get it): cut one if it reads as repetition.
- Caveats moved above the schema: they are the fastest proof of domain knowledge.
- Lineage columns folded into one row: every page shares them and query() drops them.

## Decisions the pack left open
- Uncovered codes: kept in the khaki family, told apart by ink texture and never merged into vendor OTHER. OTHER is flat khaki, keyed "other (vendor code)". NPSHYD + COAL + OIL share khaki with a diagonal hatch ("hydro, coal, oil"). PS is khaki with + marks. INTELE (9 zero rows, 2021) has no data in the window, so it is not drawn. The BMUNITS bars use the same mapping.
- Signed series: the stack holds only the nine codes that are never negative in silver (share_negative 0 for all nine). Net interconnectors (the 10 INT codes) and PS each get their own panel below, at the same 0.009 px/MW, filled to their own zero, with the sign rule in the key. Nothing is clipped or abs()'d.
- BMUNITS (no time axis): one bar of all 3,014 units, with the 2,515 null as hatched blank ground and the 499 typed as palette segments. A fan opens the 499 into count bars per code (the INT codes folded into one row and listed in the key). Counts only; capacity is never summed. The chart slot keeps its shape (heading, plot, key, caption) with "snapshot of <date>" in place of a window, and the rail strip is a single dot.
- ENTSOG (sparse): a broken time axis with break marks and a quiet "no rows, 6 Aug to 12 Sep" stretch; lines never cross the gap and each gas day is a dot. The rail's coverage strip draws the same 14 days to true scale.

## Verification
- detect.mjs --json on each static copy: [] x 4.
- Served on :9537, iframes at 1440: root scrollHeight = clientHeight = footer bottom on every board; 0 SVG text collisions, 0 text clipped past the chart edge, 0 elements past the 80 px margins; DataFrames end at x 1136 / 1291 / 1051 / 1351 (max 1360); rail 681 to 708 px tall, so it fits a 900 px viewport while sticky. Server stopped.
- Not done: the 390 px build. Plan: the grid becomes one column in DOM order (band, rail facts, chart, reading sections, side-heads above tables); the keyed index drops under the plot; charts redraw at phone width from data, not scaled down.

## NEW COPY (verbatim; schema meanings, rail values and caveats are condensed from pack facts)

### elexon/fuelhh
- Title: Generation by fuel type
- Lede: Half-hourly GB generation outturn in MW, one value per settlement period for each Elexon fuel-type code.
- Chart heading: Hourly outturn, 20 to 26 September 2026
- Caption: elexon/fuelhh, silver, MW. Settlement dates 20 to 26 September 2026: 336 half-hours drawn as 168 hourly points, each the mean of a code’s two half-hours, with a group’s codes summed first. The signed interconnectors and PS sit in their own panels on the same scale. Day ticks mark each settlement date’s start, 23:00 UTC.
- What it is: For every half-hour settlement period, Elexon publishes GB generation outturn by fuel type. Gridflow keeps one row per period and fuel-type code, upper case as sent: 20 codes in a recent half-hour, ten of them interconnectors. Interconnector and pumped-storage values are signed. There is no solar code.
- Use: Wind and gas outturn as features for residual-demand and price models.
- Use: Actuals to score a wind generation forecast against.
- Use: Tracking the fuel mix and interconnector flows over a week or a year.
- Caveat: There is no solar code. Solar outturn is not in this dataset; it has to come from another one.
- Caveat: Eleven codes are signed: the ten interconnector codes, where positive is import to GB, and PS. Negatives are routine: INTIRL is negative in 70.3% of all half-hours, PS in 54.7%.
- Caveat: The code set changes over time. INTELEC starts on 14 Sep 2021, INTVKL on 12 Jul 2023 and INTGRNL on 19 Mar 2024, so a half-hour holds 17 to 20 rows.
- Fact, Vendor dataset: FUELHH, Half-hourly Generation Outturn by Fuel Type
- Fact, Grain: One row per settlement period and fuel-type code
- Fact, Cadence: 30 minutes
- Fact, History: 1 Sep 2021 to 26 Sep 2026 in local silver; 7 to 9 Sep 2026 are missing
- Fact, Publication lag: At the period end, 30 min after its start, on 99.82% of rows; the longest is 271 min
- Fact, Units: MW; the interconnector codes and PS are signed
- Fact, Rows: 1,682,517; 17 to 20 per half-hour
- Fact, Silver table: silver_elexon_fuelhh
- Schema note: Pydantic class ElexonFuelHH in gridflow/schemas/elexon.py. Transformer version 2.0.0.
- Workbench note: Reads silver_elexon_fuelhh and filters settlement_date inclusively: 6,720 rows for this range. Returns a pandas DataFrame. query("fuel_generation", ...) is an alias of the same table.
- Related, elexon/fuelinst: Same connector: instantaneous outturn by fuel type.
- Related, elexon/bmunits_reference: Shares the fuel-type vocabulary.
- Related, elexon/indo: The demand series the interconnector sign is checked against.
- Related, neso_data_portal/historic_generation_mix: Carries the solar outturn this dataset lacks.
- Sample note: Settlement date 2026-09-26, period 25: 8 of the 20 codes. Every row also has data_provider elexon and dataset_version 2.0.0.
- Meaning, settlement_date: GB settlement date, derived from the vendor start time since v2.0.0
- Meaning, settlement_period: Half-hour within the date, 1 to 50 (46 or 50 on clock-change days)
- Meaning, timestamp_utc: Start of the half-hour, UTC (vendor startTime)
- Meaning, fuel_type: Elexon fuel-type code, upper case as sent
- Meaning, generation_mw: MW for the period. INT codes are signed, positive is import to GB; PS is signed, meaning undocumented
- Meaning, published_at: Vendor publication time
- Meaning, data_provider: Always elexon
- Meaning, ingested_at: When the silver transform ran, not the bronze fetch

### elexon/system_prices
- Title: System sell and buy prices
- Lede: GB imbalance (cash-out) prices in GBP/MWh, with net imbalance volume, for every half-hour settlement period.
- Chart heading: System sell price, 19 to 22 September 2026
- Caption: elexon/system_prices, silver, latest vintage per period, GBP/MWh. Settlement dates 19 to 22 September 2026: 192 native half-hourly values, one step each, not averaged. Day ticks mark each settlement date’s start, 23:00 UTC.
- What it is: The system sell price (SSP) and system buy price (SBP) settle imbalances in GB: Elexon publishes one pair per half-hour settlement period, with the net imbalance volume in MWh. Silver keeps every vendor publication of a period, so a period can appear more than once. Since September 2021 the two prices have been equal on every row.
- Use: The target for an imbalance-price model.
- Use: Measuring how often, and how far, prices go negative.
- Use: The spread between day-ahead prices (elexon/mid) and cash-out.
- Caveat: Silver is append-only: 96,793 rows cover 88,694 periods. Read the _latest view, as the workbench does, or dedupe on available_at before plotting.
- Caveat: SSP equals SBP on every row since September 2021, so one line carries both.
- Caveat: Negative prices are routine: 4,052 periods since September 2021 (latest vintage), and 34 of the 192 in the chart.
- Fact, Vendor dataset: DISEBSP, System Sell Price and System Buy Price per settlement period
- Fact, Grain: One row per settlement period and vendor publication, so a period can repeat
- Fact, Cadence: 30 minutes
- Fact, History: 1 Sep 2021 to 22 Sep 2026 in local silver, no missing dates
- Fact, Publication lag: Median 52 min after the period start in 2021 to 2023, about 24.7 h in 2024 to 2026; the cause is not established
- Fact, Units: GBP/MWh; net imbalance volume in MWh
- Fact, Rows: 96,793 for 88,694 periods
- Fact, Silver table: silver_elexon_system_prices_latest, a view with one row per period
- Schema note: Pydantic class ElexonSystemPrice in gridflow/schemas/elexon.py. Transformer version 2.0.0, append-only.
- Workbench note: Reads silver_elexon_system_prices_latest, so vintages are already collapsed to one row per period; raw parquet is not. Returns a pandas DataFrame. data.imbalance_context(start, end) adds NESO carbon intensity.
- Related, neso/carbon_intensity: Joined with this in the workbench’s imbalance context.
- Related, elexon/mid: The day-ahead benchmark the workbench reads.
- Sample note: Settlement date 2026-09-20, periods 22 to 29, one vintage each, values as stored. price_derivation_code is N and run_type null on every row shown.
- Meaning, settlement_date: GB settlement date
- Meaning, settlement_period: Half-hour within the date, 1 to 50
- Meaning, timestamp_utc: Period start, UTC
- Meaning, system_sell_price: SSP, GBP/MWh; schema bound −500 to 10,000
- Meaning, system_buy_price: SBP, GBP/MWh; same bound
- Meaning, net_imbalance_volume: NIV, MWh. Sign convention not documented in code or vault
- Meaning, run_type: Null on every row: this endpoint has no such field
- Meaning, price_derivation_code: Vendor code: N 49,764 rows, P 47,019, K 10. The vault reads N as normal, P as provisional; K is unknown
- Meaning, published_at: Vendor createdDateTime
- Meaning, data_provider: Always elexon
- Meaning, ingested_at: When the silver transform ran

### entsog/physical_flows
- Title: Physical gas flows
- Lede: Daily physical gas flow for each point, operator and direction on European transmission systems, in GWh/d.
- Chart heading: Flow at two GB points, every gas day held
- Caption: entsog/physical_flows, silver, GWh/d. One native value per gas day, 04:00 UTC, with nothing averaged across points. There are no rows from 6 August to 12 September, so the axis breaks there and nothing is interpolated.
- What it is: The ENTSO-G Transparency Platform reports the physical gas flow at each point for every gas day, once for each reporting operator and direction. Gridflow normalises every value to GWh/d. Local silver holds 620 points and 48 operators, and each gas day starts at the operator’s own hour.
- Use: Tracking flows at GB entry and exit points such as St. Fergus and Bacton.
- Use: Supply-side features for gas demand or price models.
- Use: Comparing nominations (entsog/nominations) with physical flow.
- Caveat: Only 14 gas days are held, in two blocks: 1 to 5 August and 13 to 21 September 2026.
- Caveat: Both sides of a point report, so summing every row double counts. At Bacton (IUK) on 21 September the National Gas TSO exit and the Interconnector entry are both 175.165952 GWh/d.
- Caveat: Flows can be null: 2,499 rows, including every day for 176 series such as Avonmouth LNG entry. Do not zero-fill.
- Fact, Vendor dataset: operationalData, indicator Physical Flow
- Fact, Grain: One row per gas day, point, operator and direction
- Fact, Cadence: Daily, by gas day; the start hour varies by operator
- Fact, History: 14 gas days in local silver: 1 to 5 Aug and 13 to 21 Sep 2026
- Fact, Publication lag: Not established: silver keeps the ingest time, not the vendor’s update time
- Fact, Units: GWh/d on every row
- Fact, Rows: 13,764; about 983 per gas day
- Fact, Silver table: silver_entsog_physical_flows
- Schema note: Pydantic class EntsogPhysicalFlow in gridflow/schemas/entsog.py. Transformer version 1.0.0.
- Workbench note: Reads silver_entsog_physical_flows and filters timestamp_utc from 2026-09-13T00:00Z to before 2026-09-22T00:00Z. Returns a pandas DataFrame. Operators whose gas day starts at 21:00 to 23:00Z on the previous date fall outside the first day.
- Endpoint note: No pointDirection: a full-system fetch.
- Related, entsog/aggregated_physical_flows: The same indicator at zone level.
- Related, entsog/nominations: Same endpoint, Nomination indicator.
- Related, entsog/allocations: Same endpoint, Allocation indicator.
- Sample note: Gas day 2026-09-21, timestamp_utc 04:00Z and unit GWh/d on every row. Bacton (IUK) appears twice, once from each operator.
- Meaning, timestamp_utc: Gas-day start (vendor periodFrom), UTC; the hour varies by operator
- Meaning, point_key: ENTSOG point id, e.g. ITP-00005
- Meaning, point_label: Point name, e.g. Bacton (IUK)
- Meaning, operator_key: Reporting operator id, e.g. UK-TSO-0001
- Meaning, operator_label: Operator name, e.g. National Gas TSO
- Meaning, direction_key: entry or exit, relative to the reporting operator’s system (inferred from paired values, not documented)
- Meaning, flow_gwh_per_day: Flow normalised to GWh/d from the vendor value and unit. Nullable
- Meaning, unit: Always GWh/d after normalisation
- Meaning, data_provider: Always entsog
- Meaning, ingested_at: When the silver transform ran. In silver but not declared in the Pydantic class

### elexon/bmunits_reference
- Title: Balancing Mechanism units
- Lede: A snapshot of every registered Balancing Mechanism unit: id, name, fuel type, capacity, lead party and GSP group.
- Chart heading: BM units by fuel type, snapshot of 26 September 2026
- Caption: elexon/bmunits_reference, silver snapshot of 26 September 2026, count of BM units per fuel_type with nulls kept. There is no time axis. Capacity is not summed: it is per registration and not additive.
- What it is: Elexon’s reference list of Balancing Mechanism units, fetched whole in one call. Gridflow keeps a single snapshot and overwrites it on each run, so there is no history. It names the units behind per-unit datasets such as elexon/boal and elexon/pn: name, lead party, registered capacity and, for 499 of 3,014, a fuel type.
- Use: Labelling per-unit data (elexon/boal, elexon/pn) with a name, lead party and fuel type.
- Use: Selecting the wind or CCGT units for a unit-level study.
- Use: Grouping units by lead party: 379 companies.
- Caveat: Most units have no fuel type: 2,515 of 3,014 (83%), so a fuel breakdown covers 499 units.
- Caveat: Capacity is not additive. It is per registration: null-fuel rows alone sum to 727,551 MW, and 1,315 ids start I_, which the vault describes as per-party interconnector registrations.
- Caveat: query() returns nothing here. The manifest’s date column is ingested_at, so a date range returns 0 rows. Use tail() or sql().
- Fact, Vendor dataset: /reference/bmunits/all, All BM Unit reference data
- Fact, Grain: One row per BM unit
- Fact, Cadence: A snapshot, on a weekly schedule
- Fact, History: One snapshot, 26 Sep 2026, overwritten on each run: 3,014 units, where the vault recorded 2,969 on 9 Sep
- Fact, Publication lag: Not established
- Fact, Units: MW, registered capacity
- Fact, Rows: 3,014; 499 with a fuel type
- Fact, Silver table: silver_elexon_bmunits_reference
- Schema note: Pydantic class ElexonBMUnit in gridflow/schemas/elexon.py. Transformer version 1.1.0.
- Workbench note: tail() orders by ingested_at, newest first; sql() is read-only. Both return a pandas DataFrame. Do not use query(): it filters on ingested_at and returns 0 rows for a date range.
- Endpoint note: No parameters and no pagination.
- Related, elexon/boal: Per-unit data, joined on bm_unit_id.
- Related, elexon/pn: Per-unit data, joined on bm_unit_id.
- Related, elexon/uou2t14d: Per-unit availability.
- Related, elexon/fuelhh: Shares the fuel-type vocabulary and carries interconnector flow.
- Sample note: Eight units from the 2026-09-26 snapshot, dataset_version 1.1.0.
- Meaning, bm_unit_id: Elexon BM unit id (vendor elexonBmUnit); the key
- Meaning, bm_unit_name: Vendor bmUnitName; often repeats the id
- Meaning, fuel_type: Vendor fuelType; null on 2,515 of 3,014 rows
- Meaning, registered_capacity_mw: Vendor generationCapacity, MW; per registration, not additive across rows
- Meaning, company_name: Vendor leadPartyName
- Meaning, gsp_group_id: Vendor gspGroupId, e.g. _A; null on 1,822 rows
- Meaning, national_grid_bm_unit: Vendor nationalGridBmUnit, e.g. ABERU-1; not the ENTSO-E EIC
- Meaning, data_provider: Always elexon
- Meaning, ingested_at: When the silver transform ran

### Chart labels and shared lines
- fuelhh plate labels: "the nine codes never negative in silver, stacked"; "interconnectors, net"; "pumped storage". Key: wind, gas, other (vendor code), hydro, coal, oil, biomass, nuclear, interconnectors, net; "above zero is import to GB," / "below zero is export"; "signed, sign undocumented".
- system_prices: "high: 594.00 at 20:00 UTC, 22 Sep"; "low: -50.00 at 13:30 UTC, 20 Sep"; key "system sell price", "SSP, one step per period", "SBP is identical in every period", "below zero", "34 of the 192 periods".
- physical_flows: "no rows" / "6 Aug to 12 Sep"; "0.0 on 13 to 20 Sep, as reported"; key "St. Fergus, entry", "559.186 on 21 Sep", "Bacton (IUK), exit", "175.166 on 21 Sep", "both reported by National Gas TSO".
- bmunits: "no fuel type: 2,515 units (83%)"; "fuel type set: 499"; "INT (10 codes)"; key "fuel_type is null", "2,515 of 3,014 units", "The ten INT codes", "one unit each".
- Shared: "Workbench call"; "or read-only SQL:"; lineage row "Added by the silver layer, not the Pydantic class; query() and tail() drop them."
- Footer sentence reused from the homepage About section (not new).
