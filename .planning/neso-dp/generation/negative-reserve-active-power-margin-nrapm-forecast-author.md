# negative-reserve-active-power-margin-nrapm-forecast: writer's report

Writer, 2026-10-24. Page block on the canonical note in `C:\gridflow-wt\vault-neso-gen` (CRLF kept: 567 CRLF, 0 bare LF);
mirror `vault\neso_data_portal\negative-reserve-active-power-margin-nrapm-forecast.md` in `C:\gridflow-wt\fe-neso-gen`
`cmp` identical. Artefacts under the lead key `nrapm_forecast_national_daily_days` (series, sample, notebook JSON + PNG).
Build `--only neso_data_portal/nrapm_forecast_national_daily_days`: no errors (page written on the dataset template).
Detector `[]`. Page: 0 em dashes, 0 middle dots, 0 arrows; no "locally", "our copy", "yet", "live", "TODO".
Screenshots 1440, 1024, 768 and 390 (390 through a 390 px iframe), light mode: nothing clipped or overlapping. Dark mode
not checked (Chrome's dark flags did not switch the page). Server on 9803 started with PID 31532 recorded, stopped by
that PID, confirmed down. No git writes.

## The answers the launch prompt asked for

1. **What NRAPM is and what one row is.** NESO's package notes: an insufficient NRAPM warning "is a request to encourage
   more flexible parameters from generators, and inform participants of a risk of emergency instructions"; a system
   NRAPM may be issued when there is insufficient flexibility to make generation match demand in low demand periods.
   - Daily national and Scotland tables: one row per target `date` and cardinal point `cp` (`1B`, `3B`), with one value
     column, the forecast MW away from risk of a system-level (national) or Scotland-level NRAPM under forecast
     conditions. No settlement-period column, no demand or generation column, no load factor. Unit MW from NESO's field
     dictionary (`unit: MW`) and the resource descriptions ("Forecast Megawatt (MW) away from risk ...").
   - Weekly national and Scotland tables: one row per `week_number` (`<week>W<yy>`) and `date`, with a wind load factor
     column and a probability column, both with an empty `unit` in NESO's dictionary.
   - Scotland against national: separate files with the same layout, dates and points; NESO states no relation. In the
     16 October files national `1B` is below Scotland's `1B` on 24 October (3,363 against 4,369) and 26 October (4,185
     against 4,268), so Scotland is not simply a smaller share of the national figure on those days. The page says the
     link is unstated and never adds or subtracts them.
2. **Times.** `timestamp_utc` = `event_time` = start of settlement period 1 of `date` (recipe `date_sp1`, registry): 23:00
   UTC the evening before up to 25 October, 00:00 UTC from 26 October (every row checked in both captures, both daily
   tables). It is a date anchor, not a cardinal point's time; this package gives no clock window for `1B` or `3B`.
   `published_at` = `available_at` = CKAN `last_modified` read as UTC; rows carry no issue time. Weekly hold lines
   (one per table, covering the whole table, since these are its only value columns): "The load factor and probability
   columns have no NESO unit or scale, and their labels disagree." From the ledger/registry question "the load-factor and
   probability columns have no vendor unit or scale, and the dictionary titles and descriptions contradict each other".
3. **Captures.** Two per table, no 16 October recapture beyond the second capture:

   | Table | Capture (bronze) | Vintage (`published_at`) | Bytes | Rows | Targets |
   |---|---|---|---|---|---|
   | national daily | 2026-10-08T11:14:24Z | 2026-10-08 11:04:46.768036 | 660 | 26 | 10 to 22 Oct |
   | national daily | 2026-10-16T20:42:08Z | 2026-10-16 08:00:44.528954 | 664 | 26 | 18 to 30 Oct |
   | Scotland daily | 2026-10-08T11:14:28Z | 2026-10-08 10:55:55.308683 | 649 | 26 | 10 to 22 Oct |
   | Scotland daily | 2026-10-16T20:42:12Z | 2026-10-16 08:00:47.844483 | 649 | 26 | 18 to 30 Oct |
   | national weekly | 2026-10-08T11:14:31Z | 2026-10-08 10:46:06.065398 | 1,745 | 55 | 2026-10-25 to 2027-11-07 |
   | national weekly | 2026-10-16T20:42:15Z | 2026-10-15 08:00:50.650020 | 1,742 | 55 | 2026-11-01 to 2027-11-14 |
   | Scotland weekly | 2026-10-08T11:14:35Z | 2026-10-08 10:35:06.056281 | 1,747 | 55 | 2026-10-25 to 2027-11-07 |
   | Scotland weekly | 2026-10-16T20:42:19Z | 2026-10-15 08:00:53.901030 | 1,747 | 55 | 2026-11-01 to 2027-11-14 |

   Every header equals the epoch 1 header. Daily: 52 silver rows, 42 distinct `(date, cp)`; the 10 rows for 18 to 22
   October are in both captures and all 10 differ in value (national and Scotland alike). Weekly: 110 rows, 57 distinct
   `(date, week_number)`, 53 in both. Chart `dedup: {on: [date, cp], order_by: published_at}` (a guard; the
   `published_at >= 2026-10-16` filter does the work, distil reports 0 dropped of 52 read). Frame `dedup` on
   `[date, cp, published_at]` (a guard against a re-transform of one capture; it keeps both files' 22 October rows on
   purpose). Out-of-date "one capture" statements corrected (below).
4. **Chart and frame.** Line chart of the lead table only: national MW away from NRAPM risk at `1B` and `3B`, target dates
   18 to 30 October 2026 (days 2 to 14 of the file NESO last modified 08:00 on 16 October, read as UTC), `y_min: 0` so
   the distance from zero reads. Held rows are not charted. Frame: both points on 10, 22 and 26 October: the only
   negative value (10 October `1B`, -2,862, 8 October file), 22 October from both files (11,509 then 11,041; 17,901 then
   15,723), and 26 October after the clock change (`timestamp_utc` 00:00). Notebook: `tail()` on both daily tables,
   `published_at`, `timestamp_utc`, `capture_written_at` converted to UTC, merged on `date, cp`; plot national solid,
   Scotland dashed. Output: 26 rows, all from the 16 October files, `+00:00` stamps.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Grain, key `(date, cp)` (facts.grain, record.key) | registry `negative-reserve-active-power-margin-nrapm-forecast.json` lines 62-65, 121-124 (`entity_key`); silver: unique within each capture, repeats across (52 rows, 42 keys) |
| `1B` overnight daily minimum, `3B` daily minimum (grain, key notes, cp field) | catalogue snapshot `20261006T195819Z`, resource descriptions: "for overnight daily minimum 1B and daily minimum 3B"; field-info `20261008T114228Z` value-column description repeats it |
| No clock window for `1B`/`3B` in this package (key note) | field-info CP description is generic (cardinal points explained, no codes or windows); resource text names the codes only |
| Unit MW | field-info `unit: "MW"` on both daily value columns; resource descriptions "Forecast Megawatt (MW)" |
| Sign undefined (caption, field) | no sign text in package notes, resource descriptions or dictionary; values: one negative in the 8 Oct national file |
| NRAPM definition, warning, emergency instructions (what_it_is) | package `notes` in catalogue snapshot `20261006T195819Z` |
| Cadence "Daily, as NESO lists the package; no publication time" | package extras `Update Frequency: Daily`; notes give no time |
| `published_at` = CKAN `last_modified` read as UTC; no issue time | registry `vintage: ckan_last_modified`, `issue: {kind: none}`; eligibility report rows 214-215; sidecar `ckan_last_modified` equals silver `published_at` |
| `timestamp_utc` = start of SP1 of `date` | registry `temporal: date_sp1`; silver: 23:00Z to 25 Oct, 00:00Z from 26 Oct, `event_time == timestamp_utc` on all 104 daily rows |
| Requests | 2026-10-16 sidecars' `request_url` for all four files |
| Commands `gridflow pipeline ... --last 24h` | `cli.py` 485-495 (`pipeline` takes one dataset and `--last`); same form on approved NESO pages (`current-balancing-services-use-of-system-bsuos-data`, `demand-flexibility-service-test-events`); 2-14 day demand page approved `--last 24h` for this connector |
| Raw-feed note (package_show, whole file unless `last_modified` unchanged) | wording approved on the 2-14 day demand page for the same connector; `captures.py` line 4 "unchanged-member skip" |
| Chart values, alt | committed series: daily 15,819 ... 20,104 (19 Oct) ... 7,914 (24 Oct) ... 19,204; overnight 11,670, 13,067 (19 Oct) ... 3,363 (24 Oct) ... 9,777; 3B above 1B on all 13 dates; 24 Oct 2026 is a Saturday |
| plot_alt numbers | notebook output: national 3B 20,104 to 7,914; national 1B 3,363 vs Scotland 4,369 on 24 Oct; Scotland min 4,032 (23 Oct 3B), max 6,827 (30 Oct 3B) |
| Notebook lead (`tail()` reads `_latest`, newest first) | `gridflow_models/research/handles/source.py` 453-489 (`ORDER BY <date col> DESC LIMIT n`, bitemporal columns excluded); output holds only the 16 Oct capture (26 rows), matching `whole_capture` |
| Weekly hold line | registry lines 193-197, 264-268 (question); field-info: both value columns `unit: ""`, titles and descriptions swapped (national title says Scotland; probability column described as load factor) |
| Related: 2-14 day demand `1B`/`3B` trough windows | `2-14-days-ahead-national-demand-forecast.md` body: `1B` T 430-730, `3B` T 1330-1630 |
| Related: SOP negative reserve per cardinal point | `system-operating-plan-sop.md`: `total_negative_reserve` etc. (MW), one row per cardinal point incl. `1B`, `3B` |
| Related: daily OPMR negative reserve in MW | `daily-opmr.md` line 79 (`Negative Reserve`, MW) |
| Related: wind | weekly resource descriptions: "Probability of seeing a load factor on Wind that would cause a National NRAPM" |

## Body corrections (canonical note)

- Files by disposition: "Captures are one per family, all on 2026-10-08" -> two per family (8 and 16 October), epoch 1
  headers, second-capture sizes and row counts.
- National clocks: "For the one capture to date ... All 26 silver rows share this vintage" -> both vintages; each
  capture's rows share its own.
- National contents: added the 16 October capture's targets (18 to 30 October) and that the ten shared rows for 18 to 22
  October all differ, so `(date, cp)` repeats across captures.
- National sign: "The capture holds one negative value" -> scoped to the 8 October capture; the 16 October capture has
  none.
- National and Scotland identity: "unique across the whole body" -> unique within each body, not across captures.
- Scotland clocks and contents: second vintage; both captures all positive; 18 to 22 October rows differ.
- Weekly national and Scotland clocks: second vintages (15 October, captured 16 October).
- Weekly national and Scotland structure: the second capture's span and the `35W27` date move (Saturday 2027-09-04 to
  Monday 2027-08-30); 53 keys in both captures.
- Cadence: "Captures to date: one per family (2026-10-08). No scheduled refresh has run yet." -> two per family, with the
  vintages seen (daily 6, 8, 16 October; weekly 1, 8, 15 October, a week apart).

## Not verified

- The national datastore `total: 52` against a 26-row upload (note's existing TODO) is unexplained; gridflow reads the
  upload. Not used on the page.
- The sign convention, the clock window of `1B` and `3B` in this package, and whether Scotland is part of the national
  calculation: NESO documents none. The page says so; it does not borrow the demand files' windows as NRAPM facts.
- That NESO publishes the daily files every day: two vintages eight days apart are all the captures show.

## Open questions for the seat

- The chart reads the lead only. A national-with-Scotland chart would need the chart spec to read a second silver table;
  the notebook carries the comparison instead.
- The title keeps "NRAPM" in brackets (5 words); the page-set title is "Negative reserve active power margin (NRAPM)
  forecast". Seat's call if the hero should spell it out.

## Template problems

- None blocking. `raw_feed.commands` allows 1 to 3 lines, so a two-table eligible family cannot show separate ingest and
  transform lines for both tables; I used one `gridflow pipeline ... --last 24h` line per table, as approved NESO pages do.
- At 390 px the frame folds the value column behind `…` because of its long name (template behaviour); the guide lists it.

## Defects

- **NESO weekly NRAPM files move a week's date between publications.** In `weeklynrapmresult.csv` and
  `scotweeklynrapmresult.csv`, week `35W27` is dated Saturday 2027-09-04 in the files last modified 2026-10-08 and
  Monday 2027-08-30 in the files last modified 2026-10-15 (bronze `raw_20261008T111431Z_42377a3d...`,
  `raw_20261016T204215Z_42377a3d...`, and the Scotland pair `88f3e766`). Every other date in both files is a Saturday or
  Sunday; the second file's steps include 2 and 13 days. gridflow's entity key `(date, week_number)` therefore does not
  follow one week across captures (110 rows, 57 keys, 53 shared). Add to the weekly hold's question for NESO (week
  commencing convention); no code change while the tables are held.
- **NESO national daily NRAPM datastore count disagrees with the upload (carried over, still open).** Datastore
  `total: 52` at 2026-10-08T13:20Z against a 26-row upload (field-info `20261008T114228Z`); Scotland's datastore and
  upload agree at 26. gridflow captures the upload only.
- **NESO NRAPM dictionary examples use day-first dates.** Field-info `Date` examples read `25/03/2020` and `29/03/2020`
  while every file sends `YYYY-MM-DD` (the registry's `%Y-%m-%d` parses all 324 rows). Harmless for gridflow; note for the
  NESO question packet.
