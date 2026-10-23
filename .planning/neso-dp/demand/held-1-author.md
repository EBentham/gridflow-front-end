# Held Demand pages, part 1: writer report (2026-10-23)

Four one-table held pages (`page.held: <reason>`), each built with `--only neso_data_portal/<key>`, no errors; detector `[]` on all four; canonical note and mirror `cmp` clean on all four; notes stay pure CRLF (byte check: 0 LF-only lines); no series, sample or notebook artefact exists for any key, and no staged spec or authored override existed. `anatomy_errors` over every `vault/neso_data_portal/*.md` with a `page:` block returns nothing. The build's "1 error on pages not rendered by --only" line comes from another agent's page (not one of these four; it cleared on my last run).

Screenshots at 1440, 1024, 768 and 390 (390 through a 390 px iframe, also cut into 1400 px offsets) on port 9847, in `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\dem-h1-writer\shots\`. I looked at historic 1440, day-ahead 390 (all three strips), profile dates 390 (raw feed to related) and daily 768: nothing clipped or overlapping; long request URLs, keys and related slugs wrap. Dark mode not checked. Server started with `python -m http.server ... & echo $!` (PID 18549), stopped by that PID only; port 9847 free afterwards; 9670 untouched.

Rendered `<main>` text: no em or en dashes, arrows, middle dots; none of live, now, real-time, soon, pending, planned, shipped, locally, ruling, ledger, TODO, E-SEM, RULINGS, "held", "since 20". (A grep for "our " hits only "half hour"; "yet" and "coming" were reworded out.) Viewport meta present.

Every hold line comes from the registry question (`src/gridflow/connectors/neso_data_portal/registry/<package>.json`, `record.eligibility.question`), which the ledger rows (20, 21, 22, 136) point at. Each is within 16 words by the build's count.

## 1. `day-ahead-half-hourly-demand-forecast-performance` (`da_demand_fc_performance`)

Hold line: "NESO says times follow clock changes, but they carry `Z`; it never says start or end." Covers the first two parts of the registry question (zone against `Z`, period start or end); the repeated clock-change labels and the meaning of `Publish_Datetime` did not fit in 16 words and follow from the first two.

| Claim | Evidence |
|---|---|
| Forecast "as published via BMRS", outturn, TRIAD avoidance adjustments, APE, per half hour from April 2021; earlier data in the Ofgem 1B submissions | NESO package notes, catalogue snapshot `20261006T195819Z` |
| TRIAD estimates may be revised | Same notes ("may be revised after publication if required") |
| Absolute error in MW, APE in %, corrected outturn adds estimated TRIAD avoidance, `Publish_Datetime` = when the forecast was made, times follow clock changes | Vendor dictionary as quoted in the note's Units table (field info swept 2026-10-08) |
| Cadence "Monthly, NESO says" | Snapshot extras `Update frequency: Monthly`; resource description "updated on a monthly basis" |
| "also modified on 8 and 16 October 2026" | CKAN `last_modified` in the two capture sidecars: `2026-10-08T09:15:10.605360`, `2026-10-16T09:15:07.976027` (and `2026-10-06T09:15:08` in the snapshot) |
| Every time carries `Z` | Both bronze bodies: every `Datetime` and `Publish_Datetime` ends `Z` |
| Request lines | Sidecar `request_url` (both captures identical); `package_show` form as on the approved pages |
| Raw-feed note: whole file unless `last_modified` unchanged | `client.py` `iter_members` upload branch (lines 1751-1768) |
| "Each download is the whole history" | Both bodies run from 2021-04-01 |
| Related `elexon/ndf`: "NESO says it scores the day-ahead one published there" | NESO's "as published via BMRS" (attributed, not asserted as NDF identity) |

Body corrections (note): vintage paragraph now gives both captures' `last_modified` instead of "All 96,786 silver rows share this one vintage"; event-time sentence scoped to "a capture"; "The silver table has 2,017 outturn dates" scoped to the first capture; revision paragraph's "One capture exists so far" replaced with the measured result (all 96,786 rows of 8 October unchanged in the 16 October body, full-row multiset; 383 rows added, 2026-10-08 SP21 to 2026-10-16 SP19); `dataset_version` reading corrected to record version plus engine version (`generic.py`, as the Trading checker confirmed); new "Recapture (2026-10-16)" paragraph (97,169 rows, 2,025 dates, every structural pattern repeats, last label SP19 `09:30Z` against `last_modified` 09:15:07); Cadence "Captures to date: one" now two with the 16 October stamp; Activation "(first and only capture)" now "(the first capture)".

## 2. `daily-demand-update` (`daily_demand_update`)

Hold line: "Forecast rows carry zero national and transmission demand, and NESO does not say what zero means." Matches the registry question (zero ND/TSD on `F` rows: forecast of zero or no forecast).

| Claim | Evidence |
|---|---|
| Daily, usually by 08:30 UTC; about ten days' lag in settlement data; like Historic Demand Data but daily | Resource description and package notes (snapshot) |
| From the first day of the previous month, plus seven days ahead | Resource description |
| MW; each half hour starts at the UK time given | FAQ as quoted in the note (FACTS C5, T02) |
| Column list | Header of both captures (23 columns) |
| `A`/`F` grain | `FORECAST_ACTUAL_INDICATOR`, both captures |
| ND, TSD zero on every `F` row | 367 of 367 `F` rows in both captures (bronze, Python csv) |
| Request lines | Sidecar `request_url` for the CSV and the FAQ docx |
| Third command key | `daily_demand_update_files`, `kind: files` in the registry |
| Related `elexon/indo` "which NESO calls ND's equivalent" | Vendor dictionary "equivalent to the Initial National Demand Outturn (INDO)" (note body) |

Body corrections (note): vintage sentence ("For the one capture to date") now names both captures; the open item "whether a pair delivered as `F` returns as `A`... needs a second capture" answered (366 of the 367 first-capture `F` rows are `A` in the second, each with non-zero ND; the 367th is missing); Row composition rewritten for both captures, including two first-capture `A` rows (2026-10-08 SP16, SP17) with ND 0, TSD 500 and every flow 0, filled in later; the second body lacks 2026-10-15 SP48 and 2026-10-16 SP1; 24 `A` rows of 7 and 8 October changed embedded solar, the other 1,769 shared `A` rows unchanged; Cadence "One capture exists to date" and the revision TODO updated; Holds paragraph now says the zero pattern holds in both captures, covers every non-embedded column, and also appeared on two `A` rows.

## 3. `demand-profile-dates` (`demand_profile_dates`, bronze only)

Hold line: "NESO repeats some rows exactly and does not say why, so gridflow builds no table." The registry has no hold question for this family (no record); the line follows the ledger ("538: vendor repeats identical rows") and the note's open question (whether the repeats are intended).

| Claim | Evidence |
|---|---|
| Profile dates convert cardinal-point forecasts into half-hourly ones; closest match for weather, embedded generation, time of year, recurring calendar activities, special events; from the start of 2018 to 14 days ahead; can change closer to real time; daily | NESO package notes and extras (snapshot) |
| Cardinal points are peaks, troughs and fixed times | Matches the sibling 1-day-ahead page's wording and its note body |
| Rows repeat exactly | Both captures: 3,224 rows / 3,216 distinct (8 October), 3,234 / 3,225 (16 October); never two analogues for one date |
| No silver table; ingest only | No record (`registry.families[...].record` absent); no silver directory |
| Request lines | Sidecar `request_url` |

Body corrections (note): Identity bullet scoped to the activation capture and extended (the 16 October file repeats all seven and adds 2026-10-08); bronze table "1 (the only local capture of this resource)" now "1 at activation; a second on 2026-10-16"; Cadence "Only one capture exists so far" and its TODO replaced with the measured comparison: dates to 2026-10-07 unchanged, nine dates 2026-10-08 to 2026-10-18 changed analogue, seven of them already past or on the day when NESO republished, nine new dates to 2026-10-30. New TODO: whether a past date's profile date is the one finally used.

## 4. `historic-demand-data` (`historic_demand`)

Hold line: "The 2001 to 2008 files write `NA` in some columns, and NESO does not define it." Matches the registry question (literal NA in the 2001-2008 bodies: missing, not applicable or zero).

| Claim | Evidence |
|---|---|
| 26 yearly CSV files (2001 to 2026) and an FAQ | Snapshot resource list; registry (27 resources) |
| Populated 21 days in arrears; corrections to solar and demand can follow months later; NESO aware of data quality issues | Package notes (snapshot) |
| Half-hour averages, starting at the UK time given, MW | FAQ as quoted in the note (RESEARCH U5, FACTS C5) |
| Columns differ between years | The note's four header epochs |
| Request lines | Sidecar `request_url`: 2001, 2026 (`demanddataupdate_2026.csv`), FAQ |
| Related `elexon/indo` | The 2026 dictionary's "equivalent to INDO" (note body) |

Body corrections (note): "the one capture of each resource" now "the first capture"; the 2026 body's end date now notes the 16 October recapture (to 2026-09-25); Row composition adds the recapture (all 12,862 rows `A`); Cadence "One capture of each resource exists to date" replaced with the recapture facts (12,862 rows to 2026-09-25 SP48, 21 days before the capture as NESO says; all 12,478 earlier rows unchanged; 384 added; 27th silver file; the other 25 files and the FAQ not downloaded again); the Holds bullet quoted the old registry text "(2001-2008, 2023-2025)", now the registry's current "of 2001-2008", and the paragraph beneath it no longer calls the line generated from the whole header group.

## Unverified

- That the day-ahead forecast scored here is the one Elexon publishes as NDF: NESO says only "as published via BMRS"; the related note attributes it.
- Why NESO's 16 October demand update lacks two periods, and why profile dates change after the day: no NESO text found.
- Whether the 25 untouched historic yearly files were skipped by the `last_modified` rule or not requested: bronze shows only that they were not downloaded again; I did not read the run log.

## Open questions

- None blocking. The seat may prefer the day-ahead hold line to name the repeated clock-change labels instead of start or end; both are in the registry question, and 16 words fit one.

## Template problems

None.

## Defects

- NESO, Demand Data Update: the 2026-10-08 file carried two outturn (`A`) rows, 2026-10-08 SP16 and SP17, with ND 0, TSD 500 (the station-load estimate alone), England and Wales demand 0 and every flow 0; the 2026-10-16 file gives both full values. So zero demand is not confined to forecast rows. New, log for remediation (bears on the zero-demand hold).
- NESO, Demand Data Update: the 2026-10-16 file lacks 2026-10-15 SP48 and 2026-10-16 SP1 (47 rows on each date); NESO gives no reason. New.
- NESO, Demand Profile Dates: the identical-row repeats persist and grew (eight target dates in the 2026-10-16 file, adding 2026-10-08); the file changes a date's profile date after the date has passed (2026-10-08 to 2026-10-15 changed between 8 and 16 October), which NESO's notes do not describe. New observation.
- NESO, Day Ahead Demand Forecast Performance: described as monthly but modified on 6, 8 and 16 October 2026; the newest label again falls after `last_modified` if `Z` is read as UTC. Confirms the existing hold evidence.
- Vault: the historic note's Holds bullet quoted a stale registry question (fixed in this edit).
- No gridflow defect found.

## Round 2 (2026-10-24): fixes from `held-1-review.md`

All four rebuilt with `--only neso_data_portal/<key>` with no errors (the other agent's orphan-artefact stop the checker hit did not recur); canonical note and mirror `cmp` clean on all four; detector `[]` on all four; notes still pure CRLF; `anatomy_errors` empty on all four. The rendered text is free of the copy-rule words (the only grep hit for "our" is inside "half hour"). No git writes.

| Finding | Change |
|---|---|
| 4.1 major, historic `page.held` | "All years stay out: the 2001 to 2008 files write `NA`, which NESO does not define." (16 words). The coordinator's longer wording ("The whole table stays out: ...") is 17 words, over budget, so I used the checker's. |
| 1.1 performance `facts.cadence` | "Monthly, NESO says; its modified stamp moved on 6, 8 and 16 October 2026" |
| 1.2 performance `what_it_is` | "Each row also gives the time NESO says its forecast was made." (attributed) |
| 1.3 performance `related[2]` | "How NESO turns cardinal-point forecasts into half hours" (no claim about this file) |
| 1.x performance note body (Activation) | "As of the query on 2026-10-16T18:37Z, before the second capture, silver held one parquet file ..." |
| 2.1 daily `summary` | "...half-hourly GB demand and interconnector flows, with embedded wind and solar estimates and seven days of their forecasts." (22 words). The same idea is applied to historic `related[0]`: "The 2026 columns, updated daily, plus seven days of embedded forecasts". `what_it_is` was not touched (59 of 60 words). |
| 2.2 daily `facts.cadence` | "Daily, NESO says, with settlement data about ten days late; recent outturn can change" (13 words). Partly skipped: "usually by 08:30 UTC" no longer fits the 14-word fact or the 60-word `what_it_is` (59 now), so the publish time is dropped from the page; it stays in the note body. The revision clause rests on the dated change between the 8 and 16 October files. |
| 2.3 daily `related[0]` | "NESO's yearly demand files; the 2026 file has this file's columns" |
| 3.1 profile dates `facts.cadence` | "Daily; NESO changed some past days' profile dates between 8 and 16 October 2026". NESO's own "can change as the day nears" moved into `what_it_is` (trimmed elsewhere to fit 60: "peaks, troughs and fixed times. It makes them half-hourly using a profile date"). |
| 3.2 profile dates `related[3]` | "Half-hourly demand outturn of the past days chosen here, once filled" (12) |
| 4.2 historic note body | "because only one capture exists of 25 of the 26 files" |
| 4.3 historic `related[2]` | "Past days NESO picks as profiles; their demand appears here once filled" (12) |

Skipped as instructed: 1.4 and 2.4 (optional held lines), 3.3 (template item, the seat has it), 4.4 (no action). No new defects; the seat logged the round-1 defects as 20bh and 20bi.
