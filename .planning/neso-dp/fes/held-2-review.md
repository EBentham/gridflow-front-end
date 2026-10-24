# Held FES pages, part 2: checker review (2026-10-24)

Packages: fes-natural-gas-residential-and-non-domestic-i-c-heat-demand-summary-data-table-ed3 (ED3), fes-road-transport-summary-data-table-ed5 (ED5), fes-whole-system-gas-supply-data-table-ws1 (WS1), fes-whole-system-gas-supply-emissions-data-table-ws2 (WS2), local-authority-level-spatial-heat-model-outputs-fes (LA), levelised-cost-of-green-hydrogen (hydrogen).

## Verdicts

| Page | Verdict |
|---|---|
| ED3 | APPROVE with nits |
| ED5 | APPROVE |
| WS1 | APPROVE with nits |
| WS2 | REVISE (one major, a one-line fix) |
| LA | APPROVE with nits |
| Hydrogen | APPROVE with nits |

1 major, 11 nits, no blockers.

## Gates run

- `cmp` vault note vs front-end mirror: identical on all six.
- Build `--only neso_data_portal/<lead>` for all six leads: no errors, dataset template. The only warning is the repo-wide "Known issues" one.
- Detector `[]` on all six built pages.
- No artefact exists for any of the six keys (no series, samples, notebooks); the three `lcoh_*.html` files are redirect stubs to the package page.
- Rendered `<main>` text read in full for all six, scripted audit: no em or en dashes, arrows, middle dots, planning words, local-data words, bare codes beyond NESO's own table names (ED3, ED4, ED5, ED6, ED7, WS1, WS2, FLX1) or ADR/ruling references. Viewport meta present on all six.
- Screenshots 1440, 1024, 768 and 390 (390 px iframe) for all six; I read ED3 and the hydrogen page at 390 in full. Nothing clips or overlaps, long keys and URLs wrap. Light mode only.
- Server on 9957 started from Bash with a recorded PID and stopped by that PID; port confirmed down. Port 9670 untouched.
- Request URLs on every page equal the bronze sidecar `request_url` (resource ids and file names), for all 11 keys. The 20 LA CSVs are 7 domestic and 13 residential; the page's first and last picks are right. Package ids match the sidecars.
- Package facts checked against the catalogue snapshot `20261006T195819Z` (`.planning/research/neso-snapshots/`): created dates (7 July 2023 for ED3, ED5, WS1, WS2; 9 March 2022 for LA; 20 March 2025 for hydrogen), "Ad hoc", resource counts, resource last-modified dates, the 2026 "Ten-Year Outlook" wording. All correct.
- Related links: all 12 keys exist in the page set JSON and the mirror, and the three hrefs I resolved on ED5 point at the right pages.
- Not checked: dark mode; the WS2 2023 and 2024 dictionaries and the WS1 dictionary text (only the latest resource's field info is held locally, so "dictionary gives N/A" for WS2 2023 and 2024 rests on the note's earlier research pass).

## 1. Shared hold wording: true per table

| Table | Line | Verdict |
|---|---|---|
| ED5 | no period, blanks | True. All four ED6 notes time peak items at the winter system peak (5-6pm) and say vehicle counts are for "that year" or "a given year"; none says which twelve months or which winter a label names. No period word in any label column of the four CSVs. |
| WS2 | no period, blanks; units for 2025 only | Period and blank parts true. Units part: see finding 1. |
| WS1 | no period, blanks, `N/A` in 2024 | True (finding 2 on wording). `N/A` is only in the 2024 file; 2,166 blank year cells in that file. |
| ED3 combined and gas summary | "except peak gas" | True and scoped to the right tables (section 2). |
| ED3 ED7 | plain clause plus `uptake` | True; ED7 has no ED4 item. |
| LA domestic and residential | no count date | True. Field info for both: `Year` is "Year within the FES Scenarios" and "Year within the FES pathway"; no date or start or end. |

Consistent with batch 1 (ES2, FLX1): same opening clause, same "; extra" pattern. ED1's departure stays justified (NESO calls annual data fiscal there; nothing like it for these tables). No label column in any of the eight silver tables' bronze CSVs names a period (swept for fiscal, calendar, financial, gas year, winter, snapshot and month words).

## 2. "except peak gas" (ED3): verified in ED4 silver

- ED4 silver (42 rows): item 10, "Total GB Peak 1-in-20 Demand", says "Data is in gas years, i.e. 2022 is GY 2022/23 which is 01/10/2022 - 30/09/2023" in 2023 and 2024, and the same with 2023 / GY 2023/24 in 2025 and 2026. No other item in any edition (annual items 1 to 9, the 2025 and 2026 item 11 total) states a period. So the exception is exactly one item.
- It applies to the right tables. The combined 2023 and 2024 table carries that item (155 rows each edition: 2023 `Peak 1-in-20`, unit `GWh`; 2024 `Peak 1in20`, unit `GWh/day`, fuel gas, "Total GB demand"). The gas summary carries it (140 rows 2025, 28 rows 2026, `GWh/day`). ED7 (`fes_ed3_heat_demand_sum_ed`) has only heat peaks (`Peak 1-in-20`, `Peak 1in20`, `Peak ACS`, savings), no gas item, so its plain clause is right.
- The page text is carefully attributed: "NESO's ED4 package ... puts the 1-in-20 peak in gas years starting in October". It does not claim the ED3 file itself says so.
- Nit 1 below: "peak gas" is loose.

## 3. Local authority: tables separate, count date true

- Never joined or stacked on the page: it says "Two separate tables" and gives each table its own raw-feed entry and held line. It never mixes them in a statement. Nit 7: it does not tell the reader not to stack or join, as the note body does.
- "No count date": confirmed above. The package notes mention 2021 thought-piece data but no 2021 resource exists (20 resources: FES 2022, 2024, 2025); the page does not mention 2021. Good.
- "NESO's dictionary calls the 2022 oil boiler stock a proportion": field info for the domestic table gives `stock Oil boiler` = "Proportion of Buildingswith oil boilers"; the residential dictionary says "Number of dwellings or buildings". Page keeps this to the 2022 table. Correct.
- "some technology columns change name between the editions": residential silver has `stock_biofuel_boiler` and `stock_community`, `stock_dh` in 2024 and `stock_biolpg_boiler`, `stock_fossil_fuel_communal_heating`, `stock_low_carbon_district_heating` in 2025. Correct, and no equivalence claimed.
- Hydrogen blanks: domestic hydrogen columns are null in all 2020 and 2025 rows and in 1,111 of 1,482 (2030) and 741 of 1,482 (2035 onwards); residential hydrogen columns are never null. The page's "hydrogen cells are unclear" sits on the domestic line only. Right table, vague wording (nit 8).

## 4. Hydrogen (licence carve-out): clean

- Nothing from the files appears. The built page has no number, unit, column name, row, chart, frame, sample or file size from any CSV (grepped for the byte sizes, £, kg, MWh, kW; none). No artefact exists under `site/hifi/data` or in the page set for these keys.
- Every description comes from the catalogue snapshot: the NPV method sentence, "not a forecast" (green resource description), the Bloomberg NEF, Aurora Energy Research and IEA list (the package also lists the Danish Energy Agency, TNO and the European Hydrogen Observatory; "among its sources" is right), "Power BI dashboard", "autothermal reforming with carbon capture and storage", "3 scenarios for PEM and Alkaline", the "discount rate, capacity factor and electricity price" parameters.
- File facts used: names, URLs and CKAN last-modified dates only (2026-06-17 green; 2026-09-24 capex and blue), "June and September 2026" is right.
- The page says plainly, in `what_it_is`: "NESO does not say it may license their data, so this page shows nothing from the files", and each table's held line matches the approved DNO licence-area wording. The raw-feed note says "Ingest only: gridflow builds no silver table".
- Remaining template wart (a seat item, not a finding): the "silver, typed and validated" band and "The silver tables" heading still sit over three tables with no silver.

## 5. WS1 dated file facts: reproduced

- 2024 file (`fes2024_ws1_v001.csv`, last modified 2024-07-15, bronze `fa5697c5`): 7,128 `N/A` cells, 264 in each of the 27 year columns 2023 to 2049, none in 2020 to 2022 or 2050, none in label columns, no other non-numeric text. No `N/A` in the 2023, 2025 or 2026 files.
- 2025 file (`fes2025_ws1_v006.csv`, last modified 2025-12-10, bronze `ebf4f503`): grouping on all eight label columns gives exactly four groups of two (Bioenergy, `TWh`, Supply, Waste, Waste, `MSW, C&I (biogenic)`, blank Category Lookup; one pair for each of Holistic Transition, Electric Engagement, Falling Behind, Hydrogen Evolution). Each pair differs in exactly one year column, so "share every label but not their values" is exact. No fully identical rows.
- Never summed across units: no sum, total or cross-unit statement anywhere on the page; the unit set (`GW` 35, `TWh`, `bcm/yr` 35 rows in the 2024 and 2025 files) is stated as "as its unit column says".
- These are NESO-file facts dated by `last_modified`, not local counts; the reading of the no-local-data rule is acceptable.

## 6. The rest

- Facts tables, raw-feed files, related links and note bodies are right (ED5 body correction checked: quote "One of the Ten-Year Outlok outputs" is verbatim from the 2026 resource description, snapshot id right; the other five note bodies are unchanged by this writer and the WS1, ED3 and LA spot-checks match bronze and silver).
- ED3 unit facts: `Annuals` `GWh` and `Peak 1in20` `GWh/day` in the gas summary (1,400 and 140 rows in 2025; 280 and 28 in 2026). ED7 units `TWh`, `GW`, `stock` and `uptake` per the writer; ED7 silver data types match.
- WS2: no unit column, 2021 to 2050 year columns in all four files, 2026 adds `Category` (33 columns vs 32): all true.

## Findings

### Major

1. **WS2 `held` (and `what_it_is`): "units for 2025 only" is contradicted by the 2026 file.** The 2026 CSV (`10yo2026_ws2_v001.csv`, bronze `3aba22fd`) has two `Category` values, `Emissions (MtCO2e)` (11 rows) and `Carbon Captured (MtCO2e)` (7 rows). The note body (lines 257 to 261) records this and reserves judgement ("not a dictionary unit declaration"), but the public line says NESO states units for 2025 only, and `what_it_is` says "it adds a category column" without saying the labels carry `MtCO2e`. A reader opening the file sees a unit the page says is absent. The dictionary part is right. Fix (within 16 words): "NESO states no period for the year labels, or what blanks mean; dictionary units for 2025 only." and add to `what_it_is`: "its two category labels read MtCO2e". Nothing else on the page changes.

### Nits

1. **ED3 `held` (both gas tables) "peak gas".** The exception covers one item, the total GB 1-in-20 peak (155 rows per edition in the combined table). The combined 2024 table also has 775 `Peak 1in20` rows with fuel `gas` in `GW` (and 2023 equivalents) that are heat-demand peaks ED4 does not define. "Except the GB gas peak" would not invite reading those as dated. Word budget: 15 now; "except the GB gas peak" is one word longer for the gas lines.
2. **ED3 combined table: line silent on `number` and `uptake`, and on the peak unit.** The 2023 and 2024 file carries `uptake` (4,960 and 6,448 rows) and `number` (4,960 and 6,758), and ED7's line says `uptake` is undefined while the combined line does not, which implies it is defined. The ledger also asks which unit the earlier peak item carries: silver has `GWh` in 2023 and `GWh/day` in 2024 for the same item. Not false, but a one-clause line in the combined table's `differs` (for example "peak item is `GWh` in 2023, `GWh/day` in 2024") would carry it without touching the shared clause. The writer flagged this; I agree it is optional.
3. **WS1 `held` grammar.** "...or what blanks mean, or `N/A` in 2024." reads as a second list item that NESO states nothing about; suggest "NESO states no period for the year labels, or what blanks and `N/A` mean." (11 words) and let `what_it_is` carry the 2024 file.
4. **WS1 `held` omits the 2025 repeated rows**, which is the second ledger question for this table (which omitted label separates the pairs, and a corrected file). `what_it_is` carries the fact, so the page is complete; the hold line alone is not. Optional: add "; four row pairs repeat in 2025" if budget allows after nit 3 frees words.
5. **WS1 `summary`: "natural gas, hydrogen and bioenergy".** The table also has an Oil fuel type (10 `TWh` Demand rows in the 2025 file). Say "GB energy supply and demand: natural gas, hydrogen, bioenergy and oil" or drop the list.
6. **WS1 `raw_feed.commands`: "2023 and 2026 files to silver".** It names which files are in local silver (a local-data reference) and names 2023, which is not in the "Shown" list. Use the shared "the capture's date to silver".
7. **LA `what_it_is`: nothing tells the reader not to stack or join the two tables.** "Two separate tables" is correct; one clause such as "Never stacked or joined" (the note body already says it) would carry the rule the batch asked for.
8. **LA domestic `held`: "oil boiler and hydrogen cells are unclear".** Say what is unclear: "oil boiler is a proportion or a count; hydrogen blanks are unexplained" (15 words with the clause cut).
9. **LA `how_used` second bullet: "Allocate GB heat electrification to local authorities in energy system models".** This is the note body's "candidate scenario input" (gridflow's inference, with "once the holds below lift"), not NESO's stated use. Batch 1 dropped the same kind of line. Optional: reword as NESO's summary does or drop.
10. **Hydrogen `family.members[0].differs`: "capital and operating cost benchmarks ... three scenarios".** NESO's text says the benchmark capex figures are presented for 3 scenarios; opex is not tied to the three scenarios. "Capital cost benchmarks in three scenarios, with operating costs, for ..." is exact.
11. **Hydrogen note body (not rendered):** the line "Vendor portal page (the only link this page gives to the files)" is now inaccurate because the page block lists the three download URLs. The batch brief allows the file links, so correct the body line rather than the page.

(ED5 has no findings. Consideration only: the 2023 and 2024 ED6 notes say vehicle counts are "in that year", which is as vague as the page's "no period" implies; same standard as ES2 in batch 1.)

## Defects (pasteable)

None new beyond the writer's list, which I reproduced:
- NESO WS1 2024 `N/A` (7,128 cells, 264 per year column 2023 to 2049): confirmed on bronze.
- NESO WS1 2025 repeated rows (four pairs, each differing in one year column): confirmed on bronze.
- NESO LA domestic dictionary `stock Oil boiler` "Proportion of Buildingswith oil boilers": confirmed in field info.
- NESO ED5 2026 "Ten-Year Outlok": confirmed in the catalogue snapshot.
- gridflow data: WS2 2026 `Category` labels carry `MtCO2e` while the 2026 dictionary has no unit (already in the WS2 note body; relevant to the major finding).
