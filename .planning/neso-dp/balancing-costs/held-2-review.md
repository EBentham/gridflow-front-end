# Held pages, Balancing costs part 2: checker review (2026-10-23)

Pages: `daily-balancing-volume-balancing-services-use-of-system`, `bsuos-monthly-forecast`, `skip-rates`.

Checked against: the batch file, the standing instructions, the writer's report `held-2-author.md`, the three canonical note
diffs against `origin/master` in `C:\gridflow-wt\vault-neso-bc` (front matter insertions only, no body edits), the mirrors in
`C:\gridflow-wt\fe-neso-bc\vault\neso_data_portal\`, the built pages, ledger rows 66, 69 and 70, the gridflow registry JSON
for all three packages, the NESO catalogue snapshot (20261006T195819Z) and field dictionaries (field-info 20261008T114228Z),
and the bronze sidecars and bodies under `C:\gridflow-data\bronze\neso_data_portal\` (read only; Polars lazy for row counts).

Gates (my own runs): `gridflow-build --only neso_data_portal/<lead>` ok on all three (only the known vault-wide "Known issues"
caveat warning); `cmp` canonical note against mirror clean on all three; detector `[]` on all three; rendered text has 0 em
dashes, 0 en dashes, 0 arrows, 0 middle dots, no mojibake and none of live, now, yet, soon, pending, coming, planned, shipped,
real-time, locally, ruling, ledger, TODO, RULINGS, E-SEM, "our copy", "since 20"; no capture date, size or row count on any
page. Layout: I measured at 390 px in the browser pane (page served by my own server on 9933): `scrollWidth` is 390 on all
three and no element in `main` extends past the viewport; I looked at the volume page header and facts block at 390. I did not
re-take the 1440, 1024 and 768 screenshots myself; the writer's set is in `held-2-shots\`. Server on 9933 was started with its
PID recorded (34404) and stopped by that PID; 9670 untouched.

Seat ruling applied: `skip-rates` ships held although the ledger lists a `skip_rates_summary` eligible pair; not a finding.
Its two hold lines are accurate (see ask 1).

## What I checked, per the three asks

**1. "Rows not shown" lines against the ledger question.**
- Volume (one table): "Rows are not labelled with a settlement run, so there is no silver table." Ledger row 66 says no record
  (the settlement-run ruling), registry family has no record, and the file has no run column (header: `SETT_DATE`,
  `SETT_PERIOD`, eight MWh columns). Accurate, plain, no codes. Same wording as the approved cost page.
- Monthly forecast, all 8 tables covered (8 `Rows not shown` entries). Forecast summary: "NESO does not say when each monthly
  edition was issued, only when its file last changed." This is the lead item of the registry question (issue instant and
  availability of each edition; the filename month is a label, not an issue time) and true to the data (the only clock NESO
  gives is the resource `last_modified`, and the vintage is `ckan_last_modified`). The registry question also lists forward
  targets, the target-month clock, units of two columns and the dash rule; one 16-word line cannot carry all of that, and
  the lead reason is the right one. The other seven: "The header's £ is not valid UTF-8, so gridflow keeps these files in
  bronze only." I scanned every capture: all 22, 12, 12, 18, 1, 1 files of actual summary, forecast pct, summary pct, summary,
  impact and including-new are invalid UTF-8, every high byte is `0xA3`, and it sits in the header row only (body decodes
  clean). The winter-contingency file's header mixes valid UTF-8 (`0xC2 0xA3`) with one bare `0xA3`, so "One header £ is not
  valid UTF-8" is exact. Singular and plural wording match the file counts. See finding 2.1 for one omission on the forecast
  summary.
- Skip rates, all 11 tables covered. Behind constraints (2): matches the registry question (dictionary says a share of in-merit
  volume, the methodology presentation uses accepted volume). Exclusion reasons, stage 6 acceptance, stage 6 PSA: five-minute
  stamp start or end, matches. All BM and PSA: the same plus coverage. Both DSF tables: "Identical rows repeat and no column
  tells them apart" re-derived on both captures of each file: psa DSF unit 431,215 rows / 423,385 distinct (8 Oct) and 435,526 /
  427,696 (16 Oct); stage 5 DSF technology 7,202 / 7,010 and 7,223 / 7,031; excess 7,830 and 192 in both captures, and every
  column is part of the comparison, so no column separates them. Summary and stage 5 PSA technology (seat ruling): "NESO has
  reissued past rows; the files never say when each row was first published." NESO's own resource descriptions say "We have
  reissued all published datasets" on 15/05/2025 (summary) and 18/11/2025 (summary and stage 5 PSA technology), and the summary
  also says the previous days' data were updated on 19/12/2024. Accurate.
- "some monthly files are partial" (All BM and PSA): true on the files, and from the files, not NESO (the sentence separates it
  with a semicolon; it is not attributed to NESO). Evidence: All BM September 2026 holds 30 September only (387,189 rows, 288
  distinct five-minute stamps against 8,640 for the month); PSA September 2026 the same (273,888 rows); PSA March 2026 stops at
  2026-03-24T15:45 on exactly 3,200,000 rows. The sidecars show `declared_content_length` equal to the body size on all four,
  so these are NESO's files, not a gridflow truncation. Keep the line.

**2. Raw feed and files against bronze.** Every request URL on all three pages equals a bronze sidecar `request_url` (volume 4
of 4 incl. `package_show`; monthly 12 files plus `package_show`; skip 14 files plus `package_show`), and every URL sits under the
member whose capture family it belongs to (checked each of the 8 monthly and 11 skip members). `package_show` is
`/api/3/action/package_show?id=<package>`. Volume: ten yearly resources 2017-18 to 2026-27 plus the workbook, first and newest
shown, as worded. Monthly: 144 resources = 142 CSV, one zipped workbook archive (served as `.zip` under an XLSX label), one PDF
(catalogue and registry agree); every CSV has exactly one capture (no recapture exists). Skip: 77 CSVs = three 23-resource
monthly families (69) plus eight single files; the writer's seven 16 October recaptures are confirmed (October 2026 files of
exclusion reasons, All BM and PSA, both DSF files, the summary, the stage 5 PSA technology file). Page wording says "(a few
shown)" on the two family pages, and nothing is labelled "newest" except the volume page's "newest file is the current
financial year" and "first and newest shown", both true whenever read. **No page states a capture date, size, row count or
"captured once"**, so the 16 October recaptures (volume 2026-27: 605,496 bytes then 639,451 bytes, 8,826 then 9,306 rows) cannot
make a page stale. The stale statements are in the note bodies only (Defects). The commands are right: volume ingests
`daily_balancing_volume` and `daily_balancing_volume_files` (workbook `5cb7f9f2`), monthly ingests and transforms
`bsuos_monthly_forecast_fc_summary` and ingests `bsuos_monthly_forecast_files`, skip ingests and transforms
`skip_rates_behind_constraints_bmu`; "swap in any key" is the approved ORPS wording.

**3. Facts and what-it-is against NESO's text and gridflow code.**
- Volume: cadence `Weekly` (extras); grain one settlement date and period; eight MWh columns named exactly as the header and
  dictionary (units MWh on every value column); `SETT_DATE` title "Settlement Date", description "The Payment Date in relation
  to an Initial Settlement Run" (dictionary); BSUoS sentence is NESO's package text; ten April-to-March files from 2017-18.
- Monthly: rolling 24-month forecast, monthly, the "may not bear relation to ... tariffs" disclaimer, `Update Frequency:
  Monthly` all NESO's; costs in £m and an estimated BSUoS volume (TWh) from the newest header; outturn summaries ("Outturn BSUoS
  for the previous twelve months"), COVID demand cuts of 5, 10 and 15 percent, the two COVID forecasts with and without the new
  commercial services, and the September 2022 file with a "Winter Contingency Cost (Central) £m" column all match resource
  names, descriptions and headers. Each member's `differs` matches the registry family and file counts (22, 75, 12, 1, 1, 1, 18,
  12); "March 2020 to December 2021" for the actual summary matches first and last resource names.
- Skip: skip definition, the LCP Delta method, "per 30 minutes of each day following each stage of exclusions" (NESO package
  text), cadence `Daily`, "uploaded monthly" (stage 6 PSA description), "will be published monthly" (behind constraints BMU),
  77 files, files from 12_2024 (first monthly resources), stage 5 DSF "per half hour and unit" (header has `bm_unit`), summary
  "under both measures" (BM and post-system-action columns), summary grain (entity key `settlement_period_start`, `stage`).
- Units are as NESO states them: MWh, £m, £; TWh is not stated on the page.
- Related links resolve and every note is true to its target: costs note ("six categories", cost page), current charges ("per
  settlement run"), constraint breakdown (daily costs by reason), fixed tariffs, the daily forecast ("to March 2023": last
  row 2023-03-31 in the newest file), `elexon/boal` (page exists; see 3.4).

## 1. `daily-balancing-volume-balancing-services-use-of-system` (lead `daily_balancing_volume`): APPROVE

1. **nit** `page.summary`: "in eight categories such as energy imbalance, reserve and constraints" counts columns as categories.
   The eight are columns across six categories (frequency control and constraints are each split into offers and bids), and the
   cost page for the same periods says six categories, so a reader comparing the two sees six against eight. `what_it_is` already
   says "eight MWh columns", which is exact. Suggest "in eight columns, such as energy imbalance, reserve and constraints." (the
   vendor note itself says "eight action categories", so this is wording, not an error).
2. **nit** `page.what_it_is`: "NESO's dictionary calls `SETT_DATE`, titled settlement date, a payment date." reads as a riddle.
   The dictionary (field-info `daily_balancing_volume.json`) says title "Settlement Date", description "The Payment Date in
   relation to an Initial Settlement Run." Suggest "NESO's dictionary describes `SETT_DATE`, titled settlement date, as a
   payment date." Same wording as the approved cost page, so low priority.

## 2. `bsuos-monthly-forecast` (lead `bsuos_monthly_forecast_actual_sum`, 8 members): APPROVE

1. **nit** `page.family.members[bsuos_monthly_forecast_fc_summary]` and `page.raw_feed.note`: the page implies the forecast
   summary has silver across its whole history. `differs` ("one file per monthly edition, from March 2020"), `facts.history`
   and the first example URL (`monthly-bsuos-forecast-summary-mar_20.csv`, resource `ef004890`) all point at March 2020, and the
   note says "Only the forecast summary has silver". In fact 22 of its 75 files (the 18 oldest, May 2022, and April to June
   2023) have the same `0xA3` header problem (checked: 22 invalid, 53 valid) and are bronze only; the Mar_20 file shown is one
   of them. Evidence: the note's "Where each family stands" and the registry record for the family. The hold line is true as
   written and full, so the room is in the raw feed note. Suggest "Only the forecast summary has silver, and its oldest editions
   share the £ problem and stay in bronze; the other seven tables, the archive and the PDF are bronze only." (check the 30-word
   budget; drop "From NESO's CKAN portal:" if needed). No dates or counts needed.
2. **nit** `page.raw_feed.note`: "the archive and PDF are bronze only" reads as if only those two are, when every file here is
   (the hold lines say so for the seven tables). Covered by the suggestion in 2.1.
3. **nit** `page.raw_feed.commands[1].comment`: "held silver, forecast summary only" uses "held" on its own, which no other line
   on the page uses or explains. Suggest "forecast summary only; its rows are not shown".

## 3. `skip-rates` (lead `skip_rates_behind_constraints_bmu`, 11 members): APPROVE

1. **nit** `page.family.members[skip_rates_in_merit_psa].differs`: "a narrower measure" is the writer's word. NESO says PSA is "a
   more targeted measure of avoidable skips not in context of all actions taken at the time". "Narrower" suggests fewer units or
   periods. Suggest "Post System Action (PSA) basis: a more targeted measure, same columns, monthly files".
2. **nit** `page.family.members[skip_rates_behind_constraints_*].held`: "NESO's dictionary and methodology presentation disagree
   ..." is accurate to the registry question, but "presentation" here means NESO's slide deck. Suggest "NESO's dictionary and
   methodology slides disagree on what the skip rate is a percentage of." (13 words, plainer).
3. **nit** `page.summary`: "per half hour and by unit, stage by stage" fits the summary table and the technology tables, but
   six of the tables are five-minute and two are monthly. Suggest dropping the grain: "NESO's measure of better-priced Balancing
   Mechanism volume it passed over, stage by stage, by unit and by technology." The facts block already gives the summary's grain.
4. **nit** `page.related[0].note` (`elexon/boal`): "The accepted bids and offers that skips are measured against" is an
   inference. NESO's skip files carry their own accepted volumes; the BOAL page is Elexon's record of acceptance levels. Suggest
   "Elexon's record of accepted bids and offers, the actions that skipped volume was passed over for" (check the 12-word budget:
   "Elexon's accepted bids and offers, the actions skipped volume was passed over for", 12 words).

## Defects (not page findings; for the seat to paste)

- **Vault, `daily-balancing-volume-balancing-services-use-of-system.md` (and its mirror), stale on captures.** Confirmed: bronze
  holds a second 2026-27 capture, `daily_balancing_volume/2026/10/16/raw_20261016T200136Z_e781da74-6c35-4296-81dd-250cee869c19_edf40a60.csv`,
  639,451 bytes, 9,306 data rows, against the note's table row (line 188) of 605,496 bytes and 8,826 rows for the 8 October
  capture; the note's "one capture per resource so far" statement (line 333) and "to the capture date" count are out of date.
  Not on the page.
- **Vault, `skip-rates.md`, stale on captures.** Line 132 ("gridflow captured every resource once, on 2026-10-08") and line 171
  ("gridflow holds a single capture of each file") are false for the seven files listed under ask 2; the DSF repeat counts are
  unchanged (7,830 and 192 excess rows). Not on the page.
- **Vault, `bsuos-monthly-forecast.md`:** "every resource captured once, on 2026-10-08" is still true (no recapture of any of the
  144 resources exists).
- **Coverage detail for the skip note (vendor behaviour, not page content):** besides the September 2026 and March 2026 files, the
  All BM and PSA August 2026 files carry 8,640 distinct five-minute stamps against 8,928 for the month (one day's worth short; I did
  not check which day), December 2024 starts on 15 December (the first published day), and October 2026 runs only to 15 October
  in the 16 October capture. The note's coverage section lists only September and March. Not on the page.
- **Package registry status reads `eligible`** on all three packages while every table is held or bronze only (known pattern).
- **Manifest lead and member lists are correct** for all three (8 and 11 members match the registry families, the monthly
  `_files` family aside); no change suggested. Template follow-ups already known: a held family page prints "Rows not shown"
  only under "The silver tables", and a family page cannot show the monthly archive and PDF (a non-member family).

## Verdicts

| Page | Verdict |
|---|---|
| `daily-balancing-volume-balancing-services-use-of-system` | APPROVE |
| `bsuos-monthly-forecast` | APPROVE |
| `skip-rates` | APPROVE |

0 blockers, 0 majors, 9 nits (2 + 3 + 4). Every hold line is accurate against the ledger and registry question (the monthly
forecast summary's is the lead of several reasons; 2.1 asks the raw feed note to say its oldest editions are bronze only). No
page states a capture date or a one-capture claim, so the 16 October recaptures cannot make any page stale. The writer's open
question is answered: keep "some monthly files are partial", which is true on the vendor's files and not attributed to NESO.
