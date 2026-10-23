# Held Demand pages, part 2: checker review (2026-10-24)

Scope: `long-term-2-52-weeks-ahead-national-demand-forecast` and `school-holiday-percentages` only (transmission losses is another agent's).

Checked against the batch file, standing instructions, the writer's report, both canonical note diffs against `origin/master` (vault worktree `C:\gridflow-wt\vault-neso-dem`), the mirrors, the built pages, the ledger rows (lines 24 and 135), both registry records and their hold questions, the catalogue snapshot `20261006T195819Z` (package notes, resource descriptions, extras), the saved field info for both tables, gridflow `client.py` (`iter_members` upload branch), every bronze sidecar and body for the two keys (read only, Python csv) and silver (read only, Polars).

Gates, all rerun by me: `cmp` note against mirror clean on both; build `--only` for each key completes with no error (only the repo-wide "Known issues" warning); detector `[]` on both pages; no series, sample or notebook artefact exists for either key; viewport meta and `<main>` present; rendered `<main>` text has no em or en dashes, arrows or middle dots and none of live, now, real-time, soon, pending, planned, shipped, locally, ruling, ledger, TODO, E-SEM, RULINGS, held, yet, coming, "our " (the only "capture" hit is the command comment "the capture's date to silver", the wording the approved pages use); titles and meta descriptions are clean; hold lines are 16 and 15 words. Screenshots at 1440 and 768 (both pages) and 390 through a 390 px iframe (school holidays) on my port 9858 in `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\dem-h2-checker\shots\`; I read school 1440 and 390: nothing clipped or overlapping, long request URLs wrap. Dark mode not checked. Server stopped by its own listener PID (34576, command line matched); 9670 untouched.

## Verdicts

| Page | Verdict | blocker | major | nit |
|---|---|---|---|---|
| `long-term-2-52-weeks-ahead-national-demand-forecast` | REVISE | 0 | 1 | 4 |
| `school-holiday-percentages` | REVISE | 0 | 1 | 2 |

## Reproduced

| Claim | Result |
|---|---|
| Long-term: one bronze capture (`raw_20261008T100602Z_...79991bf0.csv`), 65 data rows, header equals the registry epoch, no recapture; silver one file, one capture | Reproduced. The "one capture" statements hold. |
| `(calendar_year, ESIWK)`: 64 distinct pairs in 65 rows; the only repeat is (2027, 29), peak dates 2027-07-21 and 2027-07-22 | Reproduced. Both rows carry identical values in all four MW columns (28,673 / 15,375 / 15,375 / 17,299); the note does not say so (nit 3). |
| `financial_year` differs from `calendar_year` on exactly 13 rows, all with peak dates 2027-01-05 to 2027-03-31 (financial year 2026); the label changes between 2027-03-31 (week 13, 2026) and 2027-04-05 (week 14, 2027); every 2026 row (October to December) carries 2026 | Reproduced from bronze. The note states it as a measurement, not a definition, which is the right register. It fits an April financial year, as written. |
| Long-term numbering: 2026 runs weeks 42 to 53, 2027 runs 1 to 52 | Reproduced (not in the note, nit 3). Week numbers 42 to 52 therefore appear under both years (finding 1). |
| Long-term span: peak dates 2026-10-15 to 2027-12-29 against a capture on 2026-10-08, about 1 to 64 weeks ahead | Reproduced (finding 2). |
| Long-term text: "ad hoc", "2-52 weeks ahead", National Demand definition, "assist the industry ... balancing their supply and demand positions", "Update Frequency: Ad hoc"; dictionary titles, descriptions and MW units; no issue column; registry `issue.kind: none`, temporal none | Reproduced against the snapshot, field info and registry. |
| Long-term requests: `package_show` form and the CSV URL equal the sidecar `request_url` (resource `903302b4`) | Matches. |
| School: six bronze captures (2026-10-08, one per resource), silver 434,933 rows (2,108 `Total`, 432,825 local-authority); date ranges per file as the note says (2021-06-19 to 2027-06-07); 205, 206, 206, 207, 207, 207 labels | Reproduced. |
| School: local-authority `School_Holiday` is only 0.0 or 1.0; `Total` runs 0.0 to 1.0 with multiplier 1.0 on every `Total` row; `Total` equals the sum of multiplier times flag within 0.0005 on all 2,108 dates | Reproduced. The page shows none of this, correctly. |
| School requests (2021/22, 2024/25, 2026/27) equal the sidecar `request_url`; 2024/25 writes dates day first (registry `formats_by_filename`) | Matches. |
| School text: "population weighted percentage of Public schools on holiday across GB and for each Local Authority", multipliers, local-authority websites, private schools and City of London excluded, "input into our demand models", "Update frequency: Yearly"; dictionary comment "currently either 1 or 0" | Reproduced against the snapshot and field info. |
| Raw-feed note "downloaded whole unless its `last_modified` is unchanged" | Matches `client.py` `iter_members` (upload branch, `capture.ckan_last_modified == live_modified`). |
| Commands: both keys exist in `config/sources.yaml` and the registry | Valid. |

## Focus 1: the "Rows not shown" lines

- **Long-term** ("NESO never defines its ESI weeks, and one week number appears twice with two peak dates."): covers the whole table (it is the only table) and both parts of the registry question. Accurate in substance, no codes, no local-data references, no planning words, but "one week number appears twice" is not what the data shows (finding 1).
- **School holidays** ("NESO calls the `Total` rows percentages but never states their scale: out of 1 or 100."): the scale of `Total` is the ledger's and registry's question and the line states it accurately and plainly. But the whole table is withheld, 432,825 local-authority rows included, and the line gives no reason for those. The note itself says "The local-authority rows are clear" (Holds), so a reader is told only about the rows that are not the problem (school finding 1). Same gap as the Historic Demand Data finding in part 1 and the Super SEL finding in Trading.

## 1. `long-term-2-52-weeks-ahead-national-demand-forecast` (lead `demand_forecast_2_52w`) - REVISE

1. **major** `page.held`: "one week number appears twice" is wrong as worded. Week numbers 42 to 52 each appear twice, once under 2026 and once under 2027; what repeats is the pair 2027 and week 29 (64 distinct year and week pairs in 65 rows). The registry names it "2027 week 29". A reader who knows the file has two years of weeks would find the claim false. Fix (16 words): "NESO never defines its ESI weeks, and 2027's week 29 appears twice, with two peak dates." Copy the same wording to the note's `page.held`.
2. **nit** `page.how_used[0]` and `[1]`: "from two weeks to a year ahead" and "weeks to a year ahead" state in the page's own voice a horizon the file does not have (peak dates run from 1 week to about 64 weeks after the 2026-10-08 capture; the note's own open item says the 65 rows exceed 52 and NESO does not explain). The summary attributes "2 to 52 weeks ahead" to NESO, which is fine. Say "NESO labels it 2 to 52 weeks ahead" in the first bullet, or drop the range. Check budgets.
3. **nit** note, "ESI week and year labels" and "Key and coverage": two measured facts the hold rests on are missing. 2026 runs to ESI week 53 (peak 2026-12-30) while 2027 runs 1 to 52 and starts week 1 on 2027-01-05; and the two 2027 week 29 rows are identical in all four MW columns, differing only by one day in the peak date, which points at a repeated row but does not prove it. Add both (dated, from bronze or silver).
4. **nit** `page.related[0]` (`2-14-days-ahead-national-demand-forecast`): "the next two weeks" is gridflow's paraphrase of "2-14 days ahead"; say "2 to 14 days ahead". The two forecast pages linked here (2-14 days, 7-day) are not built in this worktree yet; seat item, the links resolve once they land.
5. **nit** note, financial-year paragraph: it still lists "which month the financial year starts in" as a `TODO: verify` immediately before the measurement. Say "the data suggest April" in the TODO itself so the two do not read as in tension. No page change.

Checked and fine: `summary` (attributed), `facts` (one CSV; ad hoc, NESO says; grain), `what_it_is` (calendar and financial year labels, peak date, four MW columns, National Demand definition as NESO words it, no issue time), `raw_feed.note`, both requests, both commands, `related[1]` (7-day) and `related[2]` (historic demand outturn), the financial-year note addition (reproduced), capture counts (one), both missing items in Holds (week calendar, issue clock) match the registry.

## 2. `school-holiday-percentages` (lead `school_holiday_percentages`) - REVISE

1. **major** `page.held`: the line explains only the `Total` rows, but every row of the table is withheld. The 432,825 local-authority rows (NESO's own 1 or 0 flags) stay out because they share one table with the `Total` rows, and the note says as much. Without that, the page reads as if the local-authority rows could have been shown. Fix (16 words, no "held"): "All rows stay out: NESO never states whether Total rows are out of 1 or 100." If the seat wants to keep "NESO calls the Total rows percentages", the line needs a bigger budget.
2. **nit** `page.facts.grain`: "one local authority on one date, plus a `Total` row" can read as one `Total` row in the whole file. It is one per date (2,108 in all, one per distinct date in each file). Say "plus one `Total` row per date". Check budget.
3. **nit** `page.what_it_is`: "its population multiplier" reads as one weight per authority; four authorities carry two multiplier values within a year (note, Identity). No page change needed; the note covers it.

Checked and fine: `summary` ("daily calendar" is fair; each year omits NESO's gap between school years, as NESO's package notes say), `facts` (six yearly CSVs, Yearly NESO says, 2021/22 to 2026/27 NESO lists), `what_it_is` ("1 or 0" is NESO's dictionary comment; `Total` row "NESO calls" the percentage; sources and exclusions as NESO words them), `how_used`, `raw_feed.note` ("Three are shown" matches the three requests; day-first dates in 2024/25 reproduced), all three requests, both commands, `related` (all three exist in the page set; "partly by calendar activities" matches NESO's "recurring calendar activity" in the profile dates note), note body (row counts per year, 2,108 `Total` rows, Cadence "one capture of each", Holds paragraph, `Total` check within 0.0005; nothing stale).

## Cross-batch consistency

- Both lines follow the "what NESO says, then what it does not say" form of the approved lines. The school line is the only one in this pair that scopes the reason to part of the table (the same gap that was a major on Historic Demand Data in part 1).
- No page names a value the table withholds: the long-term page gives no MW or dates; the school page gives no `Total` values.

## Defects to carry (writer's, confirmed, plus two)

- NESO, Long Term 2-52 Weeks Ahead Demand Forecast: 2027 week 29 appears twice (2027-07-21 and 2027-07-22), with identical MW values on both rows. Confirmed; the identical values are new.
- NESO, same package: 2026 has an ESI week 53 and 2027 stops at 52, and the file spans about 64 weeks from capture against a 2-52 weeks name. New (the span is already an open item in the note).
- NESO, same package: `financial_year` switches from 2026 to 2027 between peak dates 2027-03-31 and 2027-04-05 (an April financial year, not stated by NESO). Reproduced.
- NESO, School Holiday Percentages: `Total` scale unstated (measured 0 to 1, equal to the weighted sum of local flags within 0.0005). Confirmed.
- No gridflow code defect found.
