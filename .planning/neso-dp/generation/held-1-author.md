# Held Generation pages, part 1: writer's report (2026-10-24)

Packages: `14-days-ahead-wind-forecasts` (lead `wind_forecast_14d_days_ahead`, member `wind_forecast_14d_day_ahead_bmu`), `daily-opmr` (`daily_opmr`), `weekly-opmr` (`weekly_opmr`). Every table held; held mode (no chart, frame, notebook; no artefacts committed).

## Gates

- Canonical notes edited with the Edit tool in `C:\gridflow-wt\vault-neso-gen\30-vendors\neso-data-portal\datasets\` (CRLF kept: `file` reports CRLF; diffs 104, 82 and 74 lines, not whole-file rewrites). Mirrored to `C:\gridflow-wt\fe-neso-gen\vault\neso_data_portal\`; `cmp` clean on all three.
- `gridflow-build --only neso_data_portal/<lead>` for `wind_forecast_14d_days_ahead`, `daily_opmr`, `weekly_opmr`: each wrote its page, no errors (only the repo-wide "Known issues" warning).
- Detector `[]` on all three built pages.
- No series, sample or notebook artefact exists for any of the four keys.
- Rendered `<main>` scanned: no em or en dashes, arrows or middle dots; none of live, now, real-time, soon, pending, planned, shipped, locally, ruling, ledger, TODO, held, yet, E-SEM. The only "capture" hit is the approved command comment "the capture's date to silver". "coming seasons" was reworded to "the seasons ahead". Viewport meta and `<main>` present.
- Hold lines: 16 (national), 16 (BMU), 16 (daily), 15 (weekly) words.
- Screenshots at 1440, 1024, 768 and 390 (390 through a 390 px iframe) for all three pages, port 9806, in `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\gen-h1-writer\shots\`. I looked at wind 1440 and 390, daily 768 and weekly 390: nothing clipped or overlapping; long URLs, keys and slugs wrap. Dark mode not checked. Server started with its PID recorded (36270) and stopped by that PID only.

## Recaptures (all four tables)

Every table has a second capture on 2026-10-16. The notes said "one capture"; corrected in all three. Headers are identical across captures (one epoch each).

| Table | 2026-10-08 | 2026-10-16 |
|---|---|---|
| `wind_forecast_14d_days_ahead` | 672 rows, stamp 11:30:47.254827 | 672 rows, 46,176 bytes, stamp `2026-10-16T20:30:51.163278` |
| `wind_forecast_14d_day_ahead_bmu` | 155,232 rows, stamp 11:30:44.268960 | 155,232 rows, 12,212,455 bytes, stamp `2026-10-16T20:30:47.916675` |
| `daily_opmr` | 26,827 silver rows, stamp 09:20:23.077566 | 26,937 silver rows (26,938 raw, one blank), 2,170,323 bytes, stamp `2026-10-16T19:20:20.671046` |
| `weekly_opmr` | 314,711 rows, stamp 11:20:53.625059 | 315,952 rows (315,953 raw, one blank), 24,786,014 bytes, stamp `2026-10-16T20:20:44.102738` |

## 1. `14-days-ahead-wind-forecasts` (family, `held: true`)

### Hold lines

- National: "All rows stay out: NESO's October 2026 files include half-hours before their stated forecast time, unexplained." The ledger's question is past targets. Both files (8 and 16 October) open with three half-hours at or before the file's stamp, two of them strictly before NESO's own `ForecastDateTime` and one equal to it. NESO does not say whether those are forecasts or past values, so neither the stated time nor the stamp dates every row. That is why the whole file stays out, not only the three rows. "All rows stay out" follows the approved pattern.
- BMU: "All rows stay out: NESO's October 2026 files include half-hours before publication, and no forecast time." In both files 693 rows (3 half-hours × 231 units) sit at or before the stamp, and the file has no issue column at all.

### Evidence

| Claim (page) | Evidence |
|---|---|
| 2 CSV files; `package_show` and both download URLs | Snapshot `20261006T195819Z` resources; each URL equals the sidecar `request_url` of both captures |
| "8 times a day, NESO says, at no stated times" | Snapshot extras "Update Frequency: 8 times/day"; no time in any NESO text |
| Grain | Both captures: one row per `datetime` (national), per `datetime` + `generator_name` (BMU), 231 per target |
| Feeds the day-ahead incentive forecast; excludes licence-exempt farms | Package notes and both resource descriptions (snapshot) |
| Capacity "on the transmission network" | Dictionary `Capacity`: "total operational wind capacity that is connected to the National Grid Transmission Network" |
| National file states when produced | Dictionary `ForecastDateTime`: "Date and time of when the forecast is produced" |
| BMU file "splits it", with region and capacity | Both captures: unit `wind_forecast` and `capacity` sum exactly (max difference 0.0) to the national values at all 672 targets |
| Each file holds one 14-day window and replaces the last | 8 Oct file: targets 2026-10-08 10:30 to 2026-10-22 10:00 UTC; 16 Oct file: 2026-10-16 19:30 to 2026-10-30 19:00 UTC; fixed filenames; upload rule in `client.py` `iter_members` (as confirmed in earlier held reviews) |
| Past targets in both October files; 2 before, 1 at the stated time | Silver both captures: 3 national / 693 BMU rows at or before `published_at`; national `forecast_datetime` 11:30:00Z and 20:30:00Z, split 2 strictly before + 1 equal in both |
| Commands | `wind_forecast_14d_days_ahead`, `wind_forecast_14d_day_ahead_bmu` in `config/sources.yaml` (lines 1103-1104); `pipeline` form as on the approved NRAPM page |
| Related | All four targets in the page sets; "issued several times a day" is the approved day-ahead page's WINDFOR note; the metered sibling's notes say SCADA-metered farms, "Update frequency: Daily" |

### Note body corrections

- Both resource bullets: second capture file, bytes, rows, same header; filenames matched in both captures.
- BOM present in both captures.
- BMU hold question and shape: the 16 October capture repeats the 693 past-target rows (19:30, 20:00, 20:30 UTC); "the capture spans no clock change" scoped to 8 October; the 16 October window crosses 25 October 2026 (periods 1 to 50) and the start-of-period mapping holds on every row; same 231 generators; units sum exactly to national in both.
- National issue time: second capture's single issue `2026-10-16T20:30:00Z`, 51 s before its stamp; the 2 + 1 split holds in both; shape scoped per capture with the clock change.
- Cadence: 16 October stamps and `ForecastDateTime`; the new file keeps none of the earlier window.
- Holds: "Later captures may or may not include past targets" replaced: the 16 October capture includes them too.

## 2. `daily-opmr` (one table)

### Hold line

"Publications carry a date but no time or zone, and most rows forecast days long past." Covers the whole table: every row's only issue clue is a day-only `Publish Date` (dictionary: "Date the ... OPMR was published"), and the file is history-bearing (26,821 of 26,937 rows in the 16 October file target a day at or before the file's stamp). Both parts of the ledger's question.

### Evidence

| Claim (page) | Evidence |
|---|---|
| OPMR in plain words | Package notes: "the amount of generation exceeding the demand forecast needed to meet our reserve requirement" |
| One CSV; requests | Snapshot; URL equals both sidecars |
| "Daily (weekdays), NESO lists; its October 2026 files include weekend publications" | Extras "Daily (Weekdays)"; publication dates spread over all seven days (289 to 292 each, 16 October file) |
| History from 12 March 2021 | 16 October file: `Publish Date` 2021-03-12 to 2026-10-16 |
| Columns in MW; national surplus after demand and OPMR | Dictionary units MW; `National Surplus` "The total generation – demand - OPMR" |
| "for each day 2 to 14 days ahead, NESO says" | Resource description "2-14 days ahead" (package notes say 2-13; the file measures 2 to 15: in the note's TODO) |
| "The 8 October 2026 publication differs between NESO's files of 8 and 16 October" | All 13 shared rows of publication 2026-10-08 changed (most columns), and a 14th target added; the 8 October file's rows match neither the 7 nor the 9 October publication; no other publication changed |
| Commands, related | `daily_opmr` key in sources.yaml; all four related targets in the page sets; `uou2t14d` summary "2 to 14 days ahead" by BM unit |

### Note body corrections

- Second capture listed; both stamps in the vintage clock.
- New paragraph "Second capture": 26,937 rows, 2,038 publication dates, 2,057 target dates, keys unique, same nulls and off-grid rows; seven missing publication dates; the 8 October revision (13 rows changed, column by column; one row added; 110 new rows; 26,814 identical); partial answer to the revision TODO.
- Cadence: three NESO stamps (6, 8, 16 October); weekday spread in both; "One capture exists" changed to two.
- Holds: 26,821 of 26,937 at or before the vintage in the second capture.
- Implementation delta: the "no pre-rename body in bronze" TODO resolved (both bodies carry the new names).

## 3. `weekly-opmr` (one table)

### Hold line

"Rows name engineering weeks NESO never maps to dates, and give only a publication date." Covers the whole table (every row is keyed by an engineering week) and both parts of the ledger's question (calendar undocumented; publication date only).

### Evidence

| Claim (page) | Evidence |
|---|---|
| OPMR in plain words; "2 to 52 weeks ahead, it says" | Package notes and resource description |
| "Weekly, NESO lists; its October 2026 files carry a publication almost every day" | Extras "Weekly"; 2,038 publication dates over 2,045 days (2021-03-12 to 2026-10-16), the same seven gaps as the daily file |
| History from 12 March 2021 | 16 October file `Publish Date` minimum |
| Columns in MW; national surplus undefined beyond its name | Dictionary units; `National Surplus` description "National Surplus" |
| "newest publication reaches 2029" | 16 October file, publication 2026-10-16: 155 weeks, 2026 week 44 to 2029 week 41 |
| 8 October publication differs | All 155 rows of publication 2026-10-08 changed (`generator_availability`, `generation_availability_margin`, `national_surplus` on all; `opmr_total`, `constrained_plant` on 111); no other publication changed; 1,241 rows added |
| Commands, related | `weekly_opmr` key; three related targets in the page set; NRAPM package has daily and weekly tables |

### Note body corrections

- Second capture listed; header history covers both captures; both stamps in the vintage clock; the second capture's `timestamp_utc`.
- Hold question: measured horizon of the newest publication in each capture (155 weeks, to 2029); engineering year 2026 the only one with a week 53, consistent with ISO weeks (2026 is the only 53-week ISO year in 2021 to 2029) but not proof.
- Identity: second capture unique, no nulls.
- Cadence: 16 October stamp; daily publication dates despite the "Weekly" label; append and revise behaviour (the old "mid-week re-uploads" TODO partly answered; a narrower TODO left).

## Unverified

- Whether NESO's 8 October publications (daily and weekly) changed because the 09:20 and 11:20 UTC files held a provisional version, or for another reason: NESO says nothing.
- That the BMU `Generator_Name` values still all match Elexon `national_grid_bm_unit` in the 16 October file (the note's claim rests on the 8 October file; the page does not repeat it).
- The 14-day wind cadence ("8 times a day"): two captures cannot test it.

## Open questions

- Daily OPMR horizon: NESO says 2-13 and 2-14 days; both October files run to 15 days on about a fifth of publications. The page says "2 to 14 days ahead, NESO says". Fine as attributed, I think.
- The page set names only these members; lead and member order match the manifest (`families[36]`, `package_tables`). No manifest problem.

## Template problems

None found. (As on earlier held pages, the silver band title "silver, typed and validated" sits above a section that shows no rows; it reads correctly with the "Rows not shown" label.)

## Defects

- NESO, Daily OPMR: the 8 October 2026 publication in NESO's file stamped 09:20 UTC that day differs from the same publication in the 16 October file on all 13 rows (generator availability, margin, OPMR, surplus, minimum demand, response and negative reserve on every row), and gained a 14th target (2026-10-23). A publication can be replaced under the same `Publish Date`. New.
- NESO, Weekly OPMR: the same for the 8 October 2026 publication, file stamped 11:20 UTC: all 155 rows changed (availability, margin, surplus; OPMR and constrained plant on 111). New.
- NESO, Weekly OPMR: labelled "Weekly" and "2-52 weeks ahead", but the file has a publication for all but seven days since 12 March 2021 (the same dates as the daily file), and each newest publication runs 155 weeks, to 2029. New (the horizon part was in FACTS).
- NESO, Daily OPMR: labelled "Daily (Weekdays)", with publications on every day of the week; horizon text 2-13 / 2-14 against a measured 2 to 15. Confirmed in the 16 October file.
- NESO, 14 Days Ahead Wind Forecasts: the 16 October 2026 files again open with three half-hours at or before the file stamp (two before the stated `ForecastDateTime`), so the past targets are a pattern, not a one-off. Confirms the hold evidence.
- Both OPMR files miss the same seven publication dates: 2022-04-24, 2024-02-23 to 25, 2024-03-09, 2024-07-30, 2026-08-23. New, minor.
- No gridflow code defect found.
