# Held FES pages, part 1: checker review (2026-10-24)

Packages: building-heat-model, fes-electricity-demand-summary-data-table-ed1, future-energy-scenario-electricity-supply-data-table-es1, fes-european-electricity-supply-data-table-es2, fes-flexibility-data-table-data-table-flx1.

## Verdicts

| Page | Verdict |
|---|---|
| ED1 | APPROVE with nits |
| ES1 | APPROVE with nits |
| ES2 | APPROVE with nits |
| FLX1 | APPROVE |
| Building heat model | APPROVE with nits |

No blockers, no majors. Nine nits, all optional.

## Gates run

- Build with `--only neso_data_portal/<lead>` for all five leads: no errors, pages written with the dataset template. Another writer's files did not interfere.
- Detector `[]` on all five built pages.
- Mirror `cmp` of vault note vs front-end mirror: identical on all five.
- Rendered `<main>` text read in full for all five: no em dashes, no codes beyond the dataset keys and NESO's own table names (ED1, ES1, ES2, FLX1, ED2), no local-data references, no planning words.
- Screenshots at 1440, 1024, 768, and 390 (390 px iframe) for all five; I looked at ES2 and the heat model at 390 in full. Nothing clips or overlaps; long URLs and keys wrap. Light mode only.
- Server on 9956 started with a recorded PID and stopped by that PID. Port 9670 untouched.
- Related keys: all resolve to pages in the page set (interconnector-register is a package page that an `--only` build simply does not build).
- Request URLs on all five pages equal the bronze sidecar `request_url` (resource ids and file names); package ids for ES1 and FLX1 match the sidecars.

## 1. ED1 hold line: true, and it still says why rows are held

Line: "NESO says annual data is usually a fiscal year, but not which year a label names."

- Sources checked myself. All four bronze CSVs: 2023, 2024 and 2025 label annual rows `Annual [Fiscal]` (150, 145 and 125 rows); the 2026 file says `Annual Demand` and has no ED2. `pdftotext` of the three ED2 PDFs: 2023, 2024 and 2025 all say "Annual Data, usually Fiscal Year". Peak is "Winter Peak, 5pm-6pm" (2023, 2024) and "Traditionally in the winter at 5-6pm" (2025). None says whether a header integer is the start or end of the fiscal year or winter.
- Ledger row 46 and `eligibility.md` line 161: the question asks what period a year header denotes and whether its integer is a start or end label; the registry says "NESO states none of these in the CSVs". The shared clause "NESO states no period for the year labels" would be false for ED1 (the CSV label and the PDF both name a fiscal period), so the departure is justified. The registry text is too strong for the annual measure, as the writer records under Defects.
- The line still says why rows are held (the meaning of the year label is open) and covers peak and minimum through "which year a label names". The blank question and the missing 2026 ED2 sit in `what_it_is`.
- Nit 1 (ED1 `held`): the line reads as covering the whole table, but NESO's wording is only in the 2023 to 2025 ED2 PDFs and `[Fiscal]` labels; the 2026 file has neither. Not wrong; tighter if it said "NESO's 2023 to 2025 files say ..." and the word budget allows.
- Nit 2 (ED1 note body, Holds part 1): the new dated paragraph reports the PDFs as checked, but the sentence above it still says `TODO: verify` in the ED2 PDFs. Reword to what remains open (start or end).

## 2. ES2 replacement: dated, correct, does not over-claim

- Bronze 2026-10-08 capture: `ckan_last_modified` 2026-09-16, header `Notes, Description`, 11 data rows. Bronze 2026-10-16 capture (`fetched_at` 20:33 UTC): same resource id and file name, `ckan_last_modified` 2026-10-09T09:33:06, 32,362 bytes, 199 data rows, header `Country, EU Scenario, FES Scenario Alignment, Variable, Category, Type, SubType, 2024..2050`. Body counts match: 17 countries, one `EU Central` label, alignment blank on all rows, `Capacity (MW)` 182 and `Demand (TWh)` 17, values only under 2025 to 2036, 2,388 numbers and 2,985 blanks, no BOM, CRLF.
- Repeated tuples confirmed: `France` and `Italy`, `EU Central`, blank alignment, `Capacity (MW)` / `Other` / `Other` / `Other` appear twice each with different values.
- Epoch claim in the body checked against the registry: the three recorded epoch headers have 37 columns (`SubSubType`), 35 and 34 columns (`FES Pathway Alignment`); none matches.
- The public sentence "On 9 October 2026 NESO replaced its 2026 notes file with a supply table" is a dated fact tied to NESO's `last_modified`. It says nothing about the values being usable and does not mention the repeated tuples. Good. The hold line still holds because the replacement carries no period statement and has 2,985 blank cells.
- Consideration, not a finding: the removed notes file (bronze 2026-10-08) did say "calendar years" and "snapshots taken on 1st January". The body already records this and says it does not establish the convention for the 2023 to 2025 tables, and as at the 16 October capture NESO publishes it nowhere. "NESO states no period for the year labels" is therefore fair for ES2, and equally for ES1 and FLX1 as a statement about the files NESO currently publishes.
- Nit 3 (ES2 `raw_feed.note`): the other three pages end with a "Shown: ..." sentence; ES2 lists the 2023, 2025 and 2026 requests with no "Shown: 2023, 2025, 2026."
- Nit 4 (ES2 `facts.cadence`): "editions 2023 to 2026, as at 6 October 2026" sits beside a sentence about a 9 October change; harmless, and the raw-feed sentence answers it.
- Nit 5 (ES2 note body, Holds part 3): "NESO answered the upload half on 2026-10-09" implies a reply to gridflow's question. Nothing shows the question was sent. Say "NESO replaced the notes with a supply table on 2026-10-09".
- Nit 6 (ES2 note body): the HOLD table and the "Why 2026 is held" bullet still say, in the present tense, that the 2026 body is an 11-row notes table. The new dated bullet follows them, so it is recoverable; "as captured 2026-10-08" would remove the contradiction.

## 3. Shared opening "NESO states no period for the year labels"

- ES1: true. I read all seven CSVs (2020 to 2026) and the catalogue text. The 2021 and 2022 preambles say only that one earlier year's values are "from estimates or backcasting" and name no period. The page avoids that wording completely and never calls ES1 outturn or projection. The "or what blanks mean" tail is correctly absent (the question has no blank part).
- ES2: true (see above).
- FLX1: true. I swept the first eight label columns of all four CSVs for winter, summer, year, annual, calendar, fiscal, financial, peak, snapshot, January and April: only the "peak" detail labels and the scenario name "Five Year Forecast" hit. The catalogue text names no period.
- Consistent across the three: ES1 "...labels; 2020 to 2022 numbers carry commas or spaces." ES2 "...labels, or what blanks mean." FLX1 "...labels, or what blanks mean; 2023 numbers carry spaces." Same clause, same tail where the question matches.
- Number formats confirmed: ES1 2020 has thousands commas and `N/A`; 2021 and 2022 have commas plus trailing spaces; FLX1 2023 has 1,152 padded cells, 2024, 2025 and 2026 none.
- Nit 7 (ES1 `what_it_is`): "NESO says the files cover capacity, generation and interconnector flows, by connection, scenario or pathway and technology." NESO's resource descriptions say capacity, generation and interconnector flows only; "by connection ... technology" is the writer's gloss from the columns. Let "NESO says" cover the first part only.

## 4. Building heat model: all confirmed

- Catalogue text (snapshot 20261006T195819Z): "average January day", run 1 gas combi-boiler, run 2 air-source heat pump (air-to-water), profiles "synthetic ... rather than measured household data", one-minute timestep over 24 hours aggregated half-hourly, built with the Centre for Sustainable Energy, all four files last modified 2026-07-30, package created 2026-07-30, update frequency Ad hoc.
- Bronze output: 96 rows, `run_1` and `run_2` 48 each, one archetype, month `jan`, clocks 00:00 to 23:30, no date column. `avg_COP_space_heat` is blank on 70 rows and `avg_COP_dhw` on 92; no unit anywhere in the CSV or catalogue. The COP line is accurate. The workbook (bronze) also labels the quantity "avg COP" with no unit.
- Input list: 269 rows under a three-column header. Exactly one fully identical pair (`DOMESTIC HOT WATER`, both blank, a section heading). One more label repeats with different values (`heat loss at design temperature`). No other column. So "no column tells them apart" is true. The list has no silver table: registry record is null, the resource is ingest-only, matching the page.
- Nit 8 (heat model `held` on the input list): "Identical rows repeat" is plural; the file has one identical pair. "An identical row repeats" would be exact. The wording matches the precedent pages, so the seat may keep it.
- Nit 9 (heat model `how_used`): "Run the workbook for other homes, heating systems and months" is an inference from the catalogue (heating system types, building characteristics, "1 month" in the input header), not NESO's stated use. Acceptable.

## 5. Held-page rules

- Facts are dated (as at 6 October 2026 for the catalogue; the dated 9 October replacement; file last-modified dates); no codes or local-data references on any page.
- Raw feed files: ED1 shows the 2023 and 2026 CSVs and the 2025 ED2 PDF; ES1 2020, 2023, 2026; FLX1 2023, 2024, 2026; ES2 2023, 2025, 2026; the heat model output and input list. All resource ids and file names match bronze and the registry. Edition counts match the catalogue (ED1 4 CSVs and 3 PDFs, ES1 7, ES2 4, FLX1 4).
- Facts tables checked against the catalogue: created dates (7 July 2023 for ED1, ES2 and FLX1; 3 December 2020 for ES1; 30 July 2026 for the heat model) and Ad hoc cadence are correct.
- Related links all resolve and their one-line notes are accurate. The ES2 note for the interconnector register, "many to countries listed here", reads awkwardly (wording only, not counted).
- ES2 `what_it_is` says "Countries are NESO's names, not codes": the 2024 and 2025 files also list `SEM` (the all-island market) in the Country column. Harmless; "countries and markets" would be exact.
- FLX1 `what_it_is`: units GW, GWh and TWh; interconnectors GW (5 rows) and TWh (15 to 20 rows); storage capacity and energy, dispatchable supply, demand side response, vehicle to grid, electrolysis, interconnectors; all confirmed in bronze.
- Note-body corrections: the ED1 and ES2 dated corrections are accurate (above). ES1, FLX1 and heat model bodies are page-block only; the body statements I spot-checked (ES1 `N/A` and padding, FLX1 padding, the heat model input-list reason) match bronze.
- Not checked: dark mode; the FES Data Workbook notes (the writer did not either).

## Nits summary (all optional)

1. ED1 line is general but NESO's wording covers the 2023 to 2025 files only.
2. ED1 body: stale `TODO: verify` beside the new check.
3. ES2 raw feed: no "Shown:" sentence.
4. ES2 cadence "as at 6 October" next to a 9 October change.
5. ES2 body: "NESO answered" overstates.
6. ES2 body: HOLD table and "Why 2026 is held" in the present tense.
7. ES1 `what_it_is`: "NESO says" over-covers "by connection ... technology".
8. Heat model input list: one identical row, wording plural.
9. Heat model `how_used`: "months" is an inference.
