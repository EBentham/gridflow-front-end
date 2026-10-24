# Held FES pages, second batch: writer report (2026-10-24)

Six held pages, written in the author brief's held mode (ruling 6). None has a chart, frame or notebook, and no artefacts were made (there are no series, sample, notebook, staged spec or authored override for any key). Each `page:` block is on the canonical note in `C:\gridflow-wt\vault-neso-fes\30-vendors\neso-data-portal\datasets\`, copied byte for byte to `C:\gridflow-wt\fe-neso-fes\vault\neso_data_portal\`. `cmp` is clean on all six after the last edit. `updated:` is now 2026-10-24 on all six. Nothing is staged or committed.

**Line endings.** All six notes are LF in this worktree (0 CR before and after). The Edit tool kept LF. `git diff --stat` on the six: 268 insertions, 7 deletions, with no whole-file rewrite.

## Gates

| Page (lead key) | Kind | Build `--only` | Detector |
|---|---|---|---|
| `fes-natural-gas-residential-and-non-domestic-i-c-heat-demand-summary-data-table-ed3` (`fes_ed3_heat_demand_natural_gas`) | family of 3, `held: true` | wrote, no errors | `[]` |
| `fes-road-transport-summary-data-table-ed5` (`fes_ed5_road_transport`) | one table | wrote, no errors | `[]` |
| `fes-whole-system-gas-supply-data-table-ws1` (`fes_ws1_gas_supply`) | one table | wrote, no errors | `[]` |
| `fes-whole-system-gas-supply-emissions-data-table-ws2` (`fes_ws2_gas_emissions`) | one table | wrote, no errors | `[]` |
| `local-authority-level-spatial-heat-model-outputs-fes` (`fes_la_heat_model_domestic`) | family of 2, `held: true` | wrote, no errors | `[]` |
| `levelised-cost-of-green-hydrogen` (`lcoh_capex_opex_input_assumptions_pem`) | family of 3, `held: true`, no silver | wrote, no errors | `[]` |

- **Build history:** the first builds failed on two budgets, the ED3 summary (24 of 22 words) and the WS1 `what_it_is` (61 of 60). Both are fixed. After the fix, the "errors on pages not rendered by --only" line no longer appears, so none of those errors was ever another agent's. The only remaining warning is the repo-wide "Known issues" one.
- **Rendered `<main>` text, checked by script:**
  - No em or en dashes, arrows or middle dots.
  - None of these words: live, now, real-time, yet, soon, pending, planned, shipped, coming, locally, ruling, ledger, TODO, held, hold, our, E-SEM, "unit N".
  - No "since 20xx", and no digits followed by "rows" or "days".
  - The viewport meta is present.
  - Each page has one "Rows not shown" block listing every table.
- **Screenshots:** light mode at 1440, 1024 and 768, and at 390 through a 390 px iframe, for all six pages. They are in `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\fes-held2-writer\shots\` (`<ed3|ed5|ws1|ws2|la|lcoh>_<width>.png`).
  - I read ED3 at 1440, and the local authority and hydrogen pages at 390.
  - Nothing is clipped or overlapping. Long keys, URLs and commands wrap.
  - I did not check dark mode, because headless flags do not switch the palette.
- **Server:** started from Bash as `python -m http.server 9947 ... & echo $!` (PID 65438), stopped by that PID and confirmed down. Port 9670 was not touched.
- **My own slip, already undone:** my first screenshot pass wrote five iframe wrapper files (`_h2w390_*.html`) into `C:\gridflow-wt\fe-neso-fes\site\hifi\`. I deleted them by exact name straight away, and the worktree status shows only my six mirror notes. The wrappers now live in my scratch folder.

## Held lines (16 words or fewer each)

The shared clause is H1's ES2 line, word for word: "NESO states no period for the year labels, or what blanks mean." (12 words.) FLX1 extends it with "; ...", and I followed that pattern. `fes\held-1-author.md` did not exist yet, so I read H1's in-progress `page:` blocks in the vault worktree (ED1, ES1, ES2, FLX1, building heat model).

| Table | Held line | Words |
|---|---|---|
| `fes_ed5_road_transport` | NESO states no period for the year labels, or what blanks mean. | 12 |
| `fes_ws2_gas_emissions` | NESO states no period for the year labels, or what blanks mean; units for 2025 only. | 16 |
| `fes_ws1_gas_supply` | NESO states no period for the year labels, or what blanks mean, or `N/A` in 2024. | 16 |
| `fes_ed3_heat_demand_natural_gas` | NESO states no period for the year labels except peak gas, or what blanks mean. | 15 |
| `fes_ed3_heat_demand_natural_gas_sum_ed` | the same line as the row above | 15 |
| `fes_ed3_heat_demand_sum_ed` (ED7) | NESO states no period for the year labels, or what blanks mean; `uptake` is undefined. | 15 |
| `fes_la_heat_model_domestic` | NESO states no count date for each year's stock; oil boiler and hydrogen cells are unclear. | 16 |
| `fes_la_heat_model_residential` | NESO states no count date for each year's stock. | 9 |
| all three `lcoh_*` | The package cites third-party sources; NESO does not say it is authorised to license them. | 15 |

Why the lines differ from the shared clause:

- **ED3, "except peak gas":** the same-edition ED4 gives a gas year for item 10, the total GB peak 1-in-20 demand, in every edition, 2023 to 2026. The silver text reads "Data is in gas years, i.e. 2022 is GY 2022/23 which is 01/10/2022 - 30/09/2023". Without "except peak gas", the plain clause would be false for the tables that hold that item, which are the 2023 and 2024 combined table and the 2025 and 2026 gas summary. ED7 has no ED4 item, so it keeps the plain clause.
- **ED5 keeps the plain clause, and it is true.** ED6 (silver, all editions) times peak items at "winter system peak (5-6pm)". From 2025 it defines `Annual` as "annual demand, number of vehicles on the road for a given year". Neither gives the period, or which winter a year label names.
- **Local authority tables:** these are stock counts, so the question is a date, not a period. The registry asks for the "stock assessment date" and whether it falls at the start or end of the year. Both lines share the first clause.
- **Hydrogen package:** the second clause matches the approved DNO licence-area line ("NESO does not say it is authorised to license them").

## What each page says (sources)

All six pages:
- **Package facts, from the catalogue snapshot `20261006T195819Z`:** notes, resource descriptions, created date, `last_modified` and "Update frequency: Ad hoc".
- **Requests:** equal to the bronze sidecar `request_url` of the 2026-10-08 captures. There is one capture per resource and no later ones. `package_show` is in the connector's form.
- **Upload rule:** "one `package_show`, then each file downloaded whole unless its `last_modified` is unchanged". Source: `client.py` `iter_members`, lines 1658 to 1688.
- **Cadence and history:** "Ad hoc (NESO); ... as at 6 October 2026" and "NESO created the package on ...", in the approved ED4 page's format.

**ED5.**
- Units `TWh`, `GW` and `# Cars` come from the note and silver.
- ED6 timing of peak items: from ED6 silver.
- "NESO calls the 2026 file a Ten-Year Outlook output": the 2026 resource description, "One of the Ten-Year Outlok outputs" (NESO's spelling).
- Related: ED6, ED1 and FLX1. The FLX1 link rests on the 2023 and 2024 ED6 text: "V2G data is used in supply and flexibility modelling".

**WS1.**
- Dimensions and the three units: registry columns, plus the silver and bronze unit sets.
- **2024 file:** `N/A` appears in 7,128 cells, all in year columns 2023 to 2049, reproduced on bronze `fa5697c5`. The page says "many 2023 to 2049 cells". The file was last modified on 2024-07-15.
- **2025 file:** four pairs of rows share all eight label columns but not their values, reproduced on bronze `ebf4f503` (group-by over every non-year column). The file was last modified on 2025-12-10.
- The transform comment reads "2023 and 2026 files to silver": the 2024 resource is held and the 2025 capture fails its key check, so only those two editions reach silver.
- `how_used` says "hydrogen capacity and storage". I removed an earlier claim that both are in `GW`: silver shows storage is `TWh`.
- Nothing is summed across units.

**WS2.**
- There is no unit column. The dictionary units (`N/A` for 2023 and 2024, `MTCO2e` for 2025, none for 2026) come from the approved note. The field-info probe confirms that the 2026 fields carry no units.
- 2026 adds a `Category` column: registry epoch 3.

**ED3.**
- **Three tables:** six resources in three families, mapped by the registry and the resource names.
- **Member descriptions:**
  - gas summary: `Annuals` = `GWh` and `Peak 1in20` = `GWh/day`, checked in silver (2025: 1,400 and 140 rows; 2026: 280 and 28);
  - ED7 units: `TWh`, `GW`, `stock` and `uptake`, from silver.
- The ED7 dictionary gives column types only, so "`uptake` is undefined" holds.

**Local authority.**
- The two tables are kept separate, never stacked or joined.
- Domestic dictionary: "number of buildings with ...", plus "Proportion of Buildings with ...".
- `stock Oil boiler` is described as "Proportion of Buildingswith oil boilers" (field info).
- Residential: "dwellings or buildings".
- Columns renamed between FES 2024 and FES 2025, from silver non-null counts:
  - `biofuel` became `biolpg`;
  - `community` and `dh` became `fossil_fuel_communal_heating` and `low_carbon_district_heating`.
  - The page says only that names change between the editions; no equivalence is claimed.
- Hydrogen blanks: domestic null counts grow from 2030 (all null in 2020 and 2025; 1,111 of 1,482 in 2030; 741 from 2035). Neither count is on the page.

**Hydrogen package: catalogue only.**
- The page uses only NESO's package notes and resource descriptions:
  - the NPV method;
  - "not a forecast";
  - the cited sources (Bloomberg NEF, Aurora Energy Research, the International Energy Agency);
  - the resource titles and descriptions, used for the member descriptions.
- The page shows the file URLs and one ingest command, and says "Ingest only: gridflow builds no silver table" and "this page shows nothing from the files".
- **Nothing is read from the files.** I did not open the bronze CSVs, and the field-info JSON that exists for the three keys was not used.

## Body corrections

- **ED5 (the only one):** the note body said only the batch spec treats 2026 as the Ten-Year Outlook. It now adds that NESO's own 2026 resource description says so, quoted with "(sic)" and the snapshot id.
- I made no other body edits. I re-checked the notes' WS1 `N/A` count and repeated rows, the ED3 units and timeframe counts, the local authority oil-boiler dictionary text and the ED5 null counts against bronze or silver. All of them hold.

## Unverified

- The WS2 dictionary units for 2023 to 2025. They come from the approved note's research pass; the local field info covers 2026 only.
- Whether "1-in-20 peak in `GWh/day`" also holds for the 2023 combined table, which labels that item `GWh` (a registry question). The member description covers 2025 and 2026 only.

## Look hardest at

1. **The ED3 lines' "except peak gas".** It is true for item 10 via ED4. Check that the 2023 and 2024 combined line, which shares the gas-summary wording, does not need the `uptake` and `number` question more. That question is in the registry text, but it does not fit the 16-word budget alongside the shared clause.
2. **The hydrogen page as a catalogue-only page under ruling 477.** It uses the package notes, including the method sentence and the source list, and the file URLs, and nothing from the files. "The silver tables" heading appears over three tables that have no silver (see Template problems).
3. **The WS1 `what_it_is` file facts.** The 2024 `N/A` and the 2025 repeated pairs, each dated by `last_modified`, are NESO-file facts rather than local counts. Confirm that this reading of the no-local-data rule is acceptable.
4. **Related-link claims:** the ED5 to FLX1 link (the vehicle-to-grid sentence exists only in the 2023 and 2024 ED6 notes), and the hydrogen package to WS1 link (the hydrogen rows are WS1 labels).

## Template problems

- **A package with no silver table still gets "The silver tables" heading and "Rows not shown" with each key.** This affects the hydrogen page, as it did the ETYS, DNO and charging-zones pages. The raw-feed note states plainly that there is no silver table, but the heading implies there is. A held variant such as "The tables" would fix it. This is a seat item; I did not work around it.
- **Family pages do not print each member's held reason under its raw-feed entry,** only in the silver list. This matches the approved TNUoS page.

## Defects (pasteable)

- **NESO, WS1 2024 (`fes2024_ws1_v001.csv`, last modified 2024-07-15):** 7,128 projection cells hold the literal `N/A`, 264 in each year column from 2023 to 2049. NESO does not define it. This is already in the note and the registry; it still stands in the 2026-10-08 capture.
- **NESO, WS1 2025 (`fes2025_ws1_v006.csv`, last modified 2025-12-10):** for each of four pathways, two rows share Fuel Type Bioenergy, `TWh`, Supply, Waste, Waste, `MSW, C&I (biogenic)` and a blank Category Lookup, with conflicting values. This is already logged as a failed entry under the reconcile-adjudication decision (ADR-040), and it still stands.
- **NESO, local authority domestic dictionary:** `stock Oil boiler` is described as "Proportion of Buildingswith oil boilers" (missing space, and a proportion under a stock heading). Already in the note; still present in the 6 October 2026 field info.
- **NESO, local authority package notes:** they describe 2021 thought-piece data, but no 2021 resource is in the package (20 resources: FES 2022, 2024 and 2025). The page does not mention 2021.
- **NESO, ED5 2026 resource description:** "Ten-Year Outlok" (typo).
- **gridflow:** none found. The registry, sidecars, silver and ledger agree.
- **Manifest:** the leads and members are right: ED3 in page-set order, local authority led by domestic, the hydrogen package led by the capex and opex file, and ED5, WS1 and WS2 as one-table pages in `package_tables`.
