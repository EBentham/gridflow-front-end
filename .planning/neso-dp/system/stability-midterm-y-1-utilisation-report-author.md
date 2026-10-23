# Stability midterm (Y-1) utilisation report: writer's report

Page `stability-midterm-y-1-utilisation-report`, one table `stability_midterm_y1` (lead and only member; the manifest
is right). Worktrees: front end `C:\gridflow-wt\fe-neso-sys`, vault `C:\gridflow-wt\vault-neso-sys`.

## Status

- `gridflow-build --only neso_data_portal/stability_midterm_y1`: passes. Detector `[]`. Real em dashes in the page: 0.
- Mirror `vault\neso_data_portal\stability-midterm-y-1-utilisation-report.md` is byte-identical to the canonical note
  (`cmp`); the note stays CRLF (301 lines, 301 CRLF).
- Artefacts (all from tools, none by hand): `site\hifi\data\series\neso_data_portal\stability_midterm_y1.json`
  (`spec_origin: vault`), `samples\neso_data_portal\stability_midterm_y1.json` (`gridflow-sample`),
  `notebooks\neso_data_portal\stability_midterm_y1.json` and `stability_midterm_y1-6.png` (`run_notebooks.py`).
  No staged spec or authored override existed.
- Screenshots at 1440, 1024, 768 and a 390 px iframe (server on 9887 started with a recorded PID, stopped by that
  PID). Scratchpad `...\scratchpad\midterm-writer\shots\`. The site has no dark scheme, so one set per width.
  Nothing clipped or overlapping. Two fixes came from looking: the title "Stability midterm (Y-1) utilisation"
  broke inside "(Y-1)" at 390, so the h1 is now NESO's tag "Stability Y-1 utilisation"; the notebook lead's long
  relation name broke mid-word, so it now says "the table's `_latest` view".

## The four things asked for

1. **What one row is.** One instruction from NESO's control room to a unit holding a Stability Y-1 contract: unit id,
   the unit's contracted inertia (MVA.s), NESO's month label, start and cease times, and NESO's duration text. NESO's
   words (package `notes`, catalogue snapshot `20261006T195819Z`): "an indicative overview of the monthly utilisation
   of BMU's with a Stability Y-1 contract", "based on instructions provided by NESO's Control Room"; "start and cease
   times of instructions and the total utilisation time for each instructed period". The market in NESO's words: the
   "Stability midterm (Y-1) 25/26 contracts covering the delivery period of Oct-25 to Sep-26". NESO does not define
   "Y-1" or "midterm" anywhere in the package; the page says so and does not guess. Units from NESO's dictionary
   (field-info `20261008T114228Z`): inertia "MVA.s", duration "Hours and Minutes", BMU ID unit "BMUID-1".
2. **Clock.** NESO states "Time values are all given in GMT" (package notes and both datetime fields). The registry
   types both columns `zone: UTC` (registry json, `utilisation_start_datetime` and `_end_`), so no daylight-saving
   shift is applied; `timestamp_utc` = the start (`casting.py:600`, checked equal on all rows). Scoped to the rows:
   five of the seven labelled months (April to August 2026) and 4 October 2025 fall in British Summer Time, so 13:00
   GMT is 14:00 in the UK (the workbench shows it as `14:00+01:00`). Nothing in the rows tests the GMT claim: no row
   touches a clock change, and Elexon's physical notifications for `T_HIRWN-1` stay at 0 MW through its August 2026
   instructions, so they cannot confirm a start. `query()` returns all datetimes in Europe/London (checked: dtype
   `datetime64[us, Europe/London]`); the notebook's first cell converts the start, cease and `timestamp_utc` to UTC.
3. **Captures, row counts, repeats.** One bronze capture, 8 October 2026: `raw_20261008T112705Z_..._998df585.csv`,
   3,950 bytes, CKAN `last_modified` 2026-09-28T16:54:21.377483, 61 data rows; NESO's datastore `total` is also 61
   (field-info snapshot), so no truncation. One header epoch. Silver: one parquet, 61 rows, one `published_at`, one
   `bronze_capture_id`. **No 16 October recapture:** the 16 October refresh logged "stability_midterm_y1: 0 responses
   ingested, 1 unchanged since newest capture" (gridflow `.planning/phases/v0.22-close/refresh-20261016/ingest.log:282`).
   No repeats: `casting.py` raises `DuplicateEntityKeyError` on a repeated entity key within a capture, and the key is
   unique (61 of 61). `dedup:` on the key, ordered by `capture_written_at`, is set on chart and frame as a guard
   (`duplicates_dropped: 0`), and both also pin `published_at` to the 28 September file.
4. **Chart.** Stacked area, instructions per month by unit, counted by NESO's month label, October 2025 to August
   2026, unit "instructions". True: counts of distinct rows, no overlapping measure added (each unit's own instructions
   never overlap, smallest gap 1 minute; different units' counts are distinct instructions). December to March has no
   rows and draws as a gap. The caption says it is a count, not hours (16 minutes to 304 hours, both in the frame).
   Hours could not be charted: `hours_utilised` is text and the chart spec cannot derive cease minus start, so the
   notebook computes hours per unit and month from the start and cease times (table and grouped bar plot).

## Evidence table

| Claim (page) | Evidence |
|---|---|
| One row per instruction; key `bmu_id`, start, end | registry `stability-midterm-y-1-utilisation-report.json` `entity_key`; NESO notes "start and cease times of instructions" |
| Contracted inertia in MVA.s | field-info `Inertia (in MVA.s)`: "Contracted Inertia of the utilised unit", unit "MVA.s" |
| Times in GMT, read as UTC with no clock change | field-info start/end descriptions; registry `"zone": "UTC"`; `casting.py:600-604` |
| Delivery October 2025 to September 2026 (history fact) | package notes: "covering the delivery period of Oct-25 to Sep-26" |
| Monthly, shortly after the month's service payments | catalogue extras "Update frequency: Monthly"; notes "updated shortly after payments for the relevant month have been made" |
| "NESO calls the report indicative" | notes "an indicative overview" |
| Month label read as the 1st | registry `"format": "%b-%y"`, dtype date |
| Month label = the month the instruction ends, in this file | silver: `month_and_year == trunc_month(end)` on 61 of 61; the 3 rows whose label differs from the start month all cross a month end |
| Chart counts: DEEPS-1 6, 8, 5, 6, 8; HIRWN-1 2, 5, 10, 6; CRUA-2 1, 1; CRUA-4 2, 1; July 16 | committed series file |
| Contracted inertia 3,052 / 496 / 483 / 483 | frame rows (all four units shown) |
| 16 minutes, 304 hours | frame rows `00:16:00` (CRUA-4, 10 Nov 2025) and `304:25:00` (HIRWN-1, 2 June 2026) |
| Four April rows 12 seconds off | notebook cell 2 output: four DEEPS-1 rows, `seconds_off` 12, 12, -12, 12 |
| `HH:MM:SS` or `HH:MM` | silver: 48 three-part, 13 two-part values |
| Elexon lists HIRWN-1 as OCGT, CRUA units as pumped storage | Elexon `bmunits_reference` silver: `T_HIRWN-1` national id `HIRWN-1`, fuel `OCGT`; `T_CRUA-2`/`T_CRUA-4` fuel `PS` |
| `query()` relation, column, inclusive ends, dropped columns | `_get_method_registry.py`: date column `timestamp_utc` (TIMESTAMPTZ), relation `silver_neso_data_portal_stability_midterm_y1_latest`, half-open UTC day bounds; run: `event_time`, `available_at`, `source_run_id`, `dataset_version` absent |
| Request URLs | bronze sidecar `request_url`; `client.py:971-981` `package_show` |
| Commands | as the approved single-file NESO pages (`system-inertia`, `constraint-breakdown`): whole file, `--last 24h` |
| Notebook plot alt values (514.5, 411.6 to 467.1, under 3 hours) | notebook cell 3 table output |
| 1 GVA.s is 1,000 MVA.s (related note) | SI prefixes; system-inertia page uses GVA.s |

## Body corrections (canonical note)

- Intro: "covering utilisation that was actually delivered" overclaimed; NESO calls it an indicative overview based on
  control-room instructions, updated after each month's payments. Replaced with NESO's words and the snapshot cited.
- "Y-1" TODO kept; added NESO's only statement (25/26 contracts cover delivery Oct-25 to Sep-26).
- "25/26 suggests a financial-year resource": wrong per NESO's notes (contract year Oct to Sep; the former 26/27 file
  consolidated into this one, 26/27 to be deleted). Corrected; the later-years TODO kept.
- `month_and_year`: added that the label equals the end instant's month on all 61 rows of this capture (not a NESO
  rule).
- `hours_utilised`: the four disagreements are each 12 seconds (three +12, one -12), all DEEPS-1 in April 2026.
- Cadence: the 16 October refresh found the file unchanged (log cited).

## Not verified

- Whether NESO's GMT statement is true of the rows (no independent instant to test against; see clock above).
- What "Y-1", "midterm" and the dictionary unit "BMUID-1" mean.
- What `DEEPS-1` is: it is not in Elexon's BM unit register as captured on 26 September 2026 (the other three ids
  match Elexon's National Grid BM unit ids). The page makes no claim about it.

## Open questions for the checker

- The month-label rule is phrased "in this file" (field) and "which here is the month each one ends" (caption). It is
  measured on the whole of NESO's 28 September file, which the chart counts in full; tell me if you want it scoped to
  "these rows" instead.
- The Elexon fuel-type notes in the key are cross-vendor facts from Elexon's register, not visible on this page;
  the related link to `elexon/bmunits_reference` points at their source.

## Template problems (seat items)

- The chart spec cannot plot a duration computed from two datetime columns (cease minus start), so an hours chart is
  impossible for this table; hours live in the notebook.
- A monthly time axis over 11 months ticks "1 Oct ... 1 Aug" with no year shown anywhere on the axis (the title
  carries the window).
- A monthly stacked area draws each segment's first and last month partly flat (the Oct to Nov piece reads as a step).
- At 768 the folded frame shows three columns (known follow-up); notebook preview breaks names mid-word (known).

## Defects (pasteable)

- **NESO data, stability midterm (Y-1) utilisation, `Hours Utilised`:** four `DEEPS-1` rows in April 2026 (starts
  2026-04-03 20:45, 04-09 21:06, 04-12 22:20, 04-23 23:50 GMT) give durations 12 seconds off cease minus start
  (+12, +12, -12, +12 s), and 13 of 61 values drop the seconds (`HH:MM`). gridflow keeps the text, correctly; vendor
  question MIDTERM-DURATION stands.
- **NESO docs, stability midterm (Y-1) utilisation, `Month & Year`:** the dictionary calls it "the month and year of
  the utilisation period", but in the 28 September 2026 file the label is the month the instruction ends (three
  instructions crossing a month end carry the later month). Vendor question: is the label the cease month or a
  payment month?
- **NESO data, BMU ids:** `DEEPS-1` appears in this file but not in Elexon's BM unit register (captured 26 September
  2026); the other three ids (`CRUA-2`, `CRUA-4`, `HIRWN-1`) match Elexon's National Grid BM unit ids. Vendor question
  whether `DEEPS-1` is a BM unit id at all.
- **Front-end template:** chart specs have no derived duration (end minus start), so utilisation hours cannot be
  charted from interval tables (this page, likely the Pathfinder utilisation report too).
