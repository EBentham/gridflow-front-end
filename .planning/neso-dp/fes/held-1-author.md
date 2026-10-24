# Held FES pages, part 1: writer report (2026-10-24)

Packages:
- `building-heat-model`: a family page. The lead is `building_heat_model_example_output_half`; `building_heat_model_list_input` has no silver table.
- One-table pages: `fes-electricity-demand-summary-data-table-ed1` (`fes_ed1_electricity_demand`), `future-energy-scenario-electricity-supply-data-table-es1` (`fes_es1_electricity_supply`), `fes-european-electricity-supply-data-table-es2` (`fes_es2_european_supply`) and `fes-flexibility-data-table-data-table-flx1` (`fes_flx1_flexibility`).

Worktrees: vault `C:\gridflow-wt\vault-neso-fes`, front end `C:\gridflow-wt\fe-neso-fes`. Nothing is staged or committed, and I touched no other package's files.

## Gates

| Gate | Result |
|---|---|
| CRLF | Notes edited with the Edit tool. Every line is CRLF: 395, 366, 396, 415 and 385 lines (heat model, ED1, ES1, ES2, FLX1) |
| Mirror | `cp` to `vault\neso_data_portal\<slug>.md`, then `cmp`: clean on all five. ES1 was re-mirrored after its last edit |
| Build | `gridflow-build --only neso_data_portal/<lead>` ran for all five leads. Each wrote its page with the dataset template and no errors. The only warning is the repo-wide "Known issues" one |
| Detector | `[]` on all five built pages |
| Artefacts | None written (held pages) |
| Rendered `<main>` | No em or en dashes, arrows or middle dots. None of: live, now, real-time, soon, pending, planned, shipped, coming, locally, ruling, ledger, TODO, held, yet, E-SEM, "since 20", outturn, projection, forecast, "% of", or a digit followed by "rows" or "days". The sweep's only "our " hits are inside "four". Viewport meta is present |
| Links | Some targets are not built in this worktree because I only ran `--only` builds: the hub, the landing page, `local-authority-...-fes`, `fes-natural-gas-...-ed3`, `interconnector-register` and `demand-flexibility`. All related keys passed the build's resolve check |
| Screenshots | 1440, 1024, 768, and 390 through a 390 px iframe, for all five pages, in `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\fes-h1-writer\shots\`. I looked at the heat model at 1440 and ES2 at 390: nothing is clipped or overlapping, and URLs and keys wrap. Light mode only. The server was started in Bash with its PID recorded (63236) and stopped by that PID. 9670 was not touched |

## The hold lines (16 words or fewer)

The shared clause comes from the approved building-blocks line: "NESO states no period for the year labels". The shared tail is "or what blanks mean", used where the question asks about blanks.

| Page / table | Line | Words |
|---|---|---|
| ES1 | NESO states no period for the year labels; 2020 to 2022 numbers carry commas or spaces. | 15 |
| ES2 | NESO states no period for the year labels, or what blanks mean. | 12 |
| FLX1 | NESO states no period for the year labels, or what blanks mean; 2023 numbers carry spaces. | 16 |
| ED1 | NESO says annual data is usually a fiscal year, but not which year a label names. | 16 |
| Heat model, example output | NESO states no unit or scale for the two COP columns, or what blanks mean. | 15 |
| Heat model, input list | Identical rows repeat and no column tells them apart, so there is no silver table. | 15 |

Why the lines differ:
- **ED1 does not use the shared clause because it would be false.** The 2023, 2024 and 2025 CSVs label their annual rows `Annual [Fiscal]`. All three ED2 PDFs (`pdftotext` of bronze) say "Annual Data, usually Fiscal Year" and define the peak as winter 5pm-6pm. None says whether a header integer is the start or the end of that fiscal year or winter. The line keeps that open question. The blank question moves to `what_it_is`, and the definitions question is covered by "each with a definitions PDF (ED2) ... 2026 ... with none".
- **ES1's question has no blank part,** so it has no blank tail. The `N/A` part sits in the raw-feed note.
- **ES2's question also asked whether the 2026 file was really a notes file.** NESO replaced that file on 9 October 2026 (see Defects), so the line drops that part. The raw-feed note states the replacement as a dated fact.
- **The input-list line uses the precedent wording** from contract transfer, disaggregated BSAD and ODFM.

## What each page says

All pages:
- Facts follow the sibling pattern: "Ad hoc (NESO); editions X to Y, as at 6 October 2026", and "NESO created the package on <metadata_created>".
- Landscape is `power`.
- No outturn, projection or forecast wording anywhere. ES1 is never called either.

**ED1 (FES electricity demand summary):**
- Demand by item and level, per scenario or pathway, as peak, minimum or annual (the CSV heading), in GW or GWh.
- 2023 to 2025 are FES editions, each with an ED2 PDF. 2026 is the Ten-Year Outlook, with no ED2.
- NESO does not say what a blank means.
- Requests: `package_show`, the 2023 and 2026 CSVs, and the 2025 ED2 PDF. Commands: ingest, transform, and `_files` ingest.
- Related: ES1, FLX1, building blocks, regional breakdown.

**ES1 (FES electricity supply):**
- Per NESO's descriptions: capacity, generation and interconnector flows, by connection, scenario or pathway, and technology.
- The unit sits in the `Variable` label, so a column mixes units.
- The 2021 and 2022 files open with notes above the table. The package has no definitions file.
- Raw note: "NESO's 2020 file writes `N/A` in some number cells". Shown: 2020, 2023 and 2026.
- Related: ED1, ES2, FLX1, resource adequacy.

**ES2 (FES European electricity supply):**
- European countries by EU scenario, with a FES alignment.
- Rows are `Capacity (MW)` or `Demand (TWh)`. Countries are NESO's names, not codes. ES1 is the GB table.
- Raw note: "On 9 October 2026 NESO replaced its 2026 notes file with a supply table."
- Related: ES1, interconnector register, ED1.

**FLX1 (FES flexibility data):**
- Supply-side and demand-side items. Each row names its unit (GW, GWh or TWh), and interconnectors use both GW and TWh.
- `Detail` splits items. The package has no definitions file.
- Shown: 2023 (the held resource), 2024 and 2026.
- Related: ES1, ED1, regional breakdown, demand flexibility.

**Building heat model (family):**
- NESO built the tool with the Centre for Sustainable Energy. It simulates minute by minute over 24 hours, then sums to half hours.
- The page states plainly: "NESO's example is one average January day, with no date: run 1 a gas combi boiler, run 2 an air-source heat pump (air to water)". NESO calls the profiles synthetic, not measured.
- Members: the output CSV (with `package_show`) and the input-list CSV.
- Commands:
  - `pipeline` for the example output;
  - `ingest` for the input list;
  - `ingest building_heat_model_files` for the workbook and guide (bronze only).
- Related: local authority heat model, ED3, ED1, building blocks.

## Evidence

| Claim | Evidence |
|---|---|
| Hold questions | Registry `record.eligibility` for each family. `eligibility.md` lines 57-59, 161-164, 178. Ledger rows 46, 49, 116, 117, 122 |
| Resource holds | Registry `disposition`: ES1 2020, 2021 and 2022 HOLD; ES2 2026 HOLD; FLX1 2023 HOLD. The ED1 and heat-model resources are SILVER or DOC |
| ES1 2020 | Bronze `40f40b39`: 5,456 non-plain number cells (2,645 with thousands commas, 2,811 `N/A`) |
| ES1 2021, 2022 | Physical line 10 is the header after a notes preamble. 12,184 and 15,545 non-blank cells are all edge-padded (2,899 and 3,189 of them also carry commas). The preamble states no period |
| FLX1 2023 | 1,152 edge-padded cells. 2024 has none |
| No trim or lexical mechanism | `record.py` `ValueSpec` fields: dtype, nullable, null_tokens, min, max |
| ED1 period text | Silver `peak_annual_minimum`: `Annual [Fiscal]` (2023-25); `ACS Peak Demand` / `Annual Demand` / `Capacity` (2026). The ED2 PDFs' "Annual Data, usually Fiscal Year" |
| No period words elsewhere | A regex sweep of every string column's labels in ES1, ES2 and FLX1 silver found only scenario names and "peak" detail labels |
| Silver counts | ED1 21,730 / 16,275 / 7,000 / 980. ES1 17,052 / 17,192 / 16,740 / 3,375. ES2 22,997 / 24,640 / 20,331. FLX1 5,550 / 4,860 / 972. Each edition has one capture. All match the notes. No figures are on the pages |
| Units | ED1 `unit` GW, GWh. FLX1 GW, GWh, TWh, with interconnectors in GW and TWh. ES2 has two `Variable` labels |
| Catalogue text | Snapshot `20261006T195819Z`: notes, extras, `metadata_created`, resource descriptions (Ten-Year Outlook for 2026; the heat model's "average January day", run 1 and run 2, "synthetic") |
| Heat model files | Bronze output: 96 rows, `run_1` and `run_2` at 48 each, month `jan`, clocks 00:00 to 23:30. Input list: 269 rows; one fully identical row pair (`DOMESTIC HOT WATER`, both blank); two labels repeat. All four `last_modified` on 2026-07-30 |
| Request URLs | Equal to each bronze sidecar's `request_url` or the snapshot resource `url` |
| Upload rule | `client.py` `iter_members` docstring (about line 1666) |
| Keys | `config/sources.yaml` lines 811-813, 925-926, 933-935. CLI `ingest`, `transform` and `pipeline` all take `--last` |

The scripts are in `...\scratchpad\fes-h1-writer\` (`silver.py`, `bronze.py`, `pad.py`, `labels.py`, `period.py`, `es2new.py`, `cat.py`), all read only.

## Body corrections (canonical notes; `updated: 2026-10-24` on all five)

- **ED1, Holds part 1:** a dated paragraph records the `Annual [Fiscal]` labels and the ED2 PDF wording. It says the registry's "NESO states none of these in the CSVs" is too strong for the annual measure, and that the hold stands.
- **ES2:**
  - Intro and lead paragraph: the 2026 file was replaced on 2026-10-09.
  - New "Second 2026 capture" bullet: the header, shape, no matching epoch, and two repeated tuples.
  - Holds part 3 and Cadence updated.
- **ES1, FLX1, heat model:** page block only. Their bodies checked out against bronze and silver.

## Not verified / open

- Whether the 16 October run re-checked the other FES resources. Only ES2 2026 has a second capture, and I read no run log.
- The FES Data Workbook notes, which might state the period. They were not inspected, as before.
- Dark mode was not checked.
- Whether ES2's old 2026 notes text was meant for ES1. It mentions GB imports and exports, says annual values are calendar years and gives 1 January capacity snapshots. NESO has removed it, so the page does not use it.

## Template problems

None. Both the family held mode and the one-table held mode render as the brief describes. The input-list member, which has no silver table, renders under "Rows not shown" like the precedents. The page set's leads and members are right.

## Defects

- **NESO, ES2 2026 (`e8ed65c6`):** On 2026-10-09T09:33:06 NESO replaced the 11-row notes body with a supply table (captured 2026-10-16, 32,362 bytes, 199 rows).
  - Two dimension tuples repeat with different values: `France` and `Italy`, `Capacity (MW)` / `Other` / `Other` / `Other`.
  - `FES Scenario Alignment` is blank on every row.
  - Values sit only under 2025 to 2036.
- **gridflow registry (`fes-european-electricity-supply-data-table-es2.json`):**
  - The 2026 `HOLD` reason still describes the notes body.
  - The replacement matches no recorded epoch (it has `SubSubType`-less 2023-style columns plus a 2024 start) and would fail the duplicate guard.
  - The hold question's upload part is answered. Re-disposition is needed at the next registry edit.
- **gridflow registry and eligibility (`fes-electricity-demand-summary-data-table-ed1`):** "NESO states none of these in the CSVs" is inaccurate for the annual measure. The CSVs say `Annual [Fiscal]` and the ED2 PDFs say "Annual Data, usually Fiscal Year". Start or end, and the peak's winter, remain open.
- **NESO, ED1 and ED2:** the measure labels change between editions (`Annual [Fiscal]` to `Annual Demand`; `Peak` to `ACS Peak Demand`). There is no ED2 for 2026.
- **Already known and reproduced:** ES1 2020, 2021 and 2022 lexical numbers and the preamble; FLX1 2023 padding; the input list's identical row pair.

## What the checker should look at hardest

1. **ED1's hold line.** It departs from the shared clause. Check the `Annual [Fiscal]` labels and the ED2 wording ("Annual Data, usually Fiscal Year") yourself. Then decide whether "but not which year a label names" is the fair reading, and whether dropping blanks from the line (they are in `what_it_is`) is acceptable.
2. **ES2's raw-feed sentence about the 9 October replacement.** Compare the two bronze captures' `ckan_last_modified` and bodies. Also check whether "NESO states no period for the year labels" is fair now that the removed notes did state calendar years and 1 January snapshots.
3. **ES1 wording.** Nothing may call it outturn or projection. I avoided the "estimates or backcasting" preamble note entirely.
4. **The building heat model's January-day wording** and the input-list "Identical rows repeat" line, against the bronze (only one fully identical pair).
