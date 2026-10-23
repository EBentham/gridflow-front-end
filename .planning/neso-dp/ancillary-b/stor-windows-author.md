# Writer report: STOR committed windows

Package `stor-windows`, one table `stor_windows` (lead and only member; `package_tables` maps the slug to it, so the
manifest is right). One-table page, nothing held.

**Status:** `gridflow-build --only neso_data_portal/stor_windows` exit 0 (only the template-wide caveat-grammar
warning); detector `[]`; 0 em dashes, middle dots or arrows on the page. Mirror `cmp` identical; note CRLF throughout
(394/394); vault diff 134 insertions, 2 deletions.

Files (mine only):
- vault: `C:\gridflow-wt\vault-neso-as-b\30-vendors\neso-data-portal\datasets\stor-windows.md` (`page:` block + 1 body correction)
- mirror: `C:\gridflow-wt\fe-neso-as-b\vault\neso_data_portal\stor-windows.md`
- artefacts: `site\hifi\data\{series,samples}\neso_data_portal\stor_windows.json`,
  `site\hifi\data\notebooks\neso_data_portal\stor_windows.json` and `stor_windows-5.png`
- page: `site\hifi\data-sources\neso_data_portal\stor-windows.html`
- screenshots: `.planning\neso-dp\ancillary-b\stor-windows-shots\` (1440, 1024, 768 full page; 390 through a 390 px iframe)

## The four questions

1. **What one row is.** One delivery date (`Date`, NESO: "Delivery date"; `date` is unique, 1,826 of 1,826) with
   NESO's season label, the `WD`/`NWD` flag and two committed windows, each an `HH:MM` start and end. NESO's package
   notes (catalogue snapshot `20261006T195819Z`): "committed windows from Season 15 to Season 19 applicable from 1 April
   2021 to 1 April 2026. These seasons define the committed windows for each STOR Service Day where STOR is required to
   be provided in accordance with the STOR Day Ahead Service Terms." Resource description: "Tabular view of ... STOR
   committed windows across Season 15 to Season 19."
   **Relation to the day-ahead auction (NESO's text only):** the auction dictionary gives `Tendered MW` "for the
   availability windows" and `Contracted MW` "for the availabilty windows accepted by us". The page says only that
   (related note: "Daily tenders of MW for each service day's availability windows") and "Reading the day-ahead auction
   results beside the windows set for each service day". It does not claim the auction's "availability windows" are
   these committed windows, and gridflow joins neither table to the other. Measured, report only: both files span
   delivery days 1 April 2021 to 31 March 2026.
   **Structure, measured:** seasons are contiguous blocks, six parts (`.1` to `.6`) per season, 30 labels `15.1` to
   `19.6`. Each (season, day type) has exactly one window pair, and each part has the same pair in all five seasons:
   12 window templates in the whole file (notebook cell 4: `seasons` = 5 on all 12). Committed hours 10 to 13.5 on
   working days, 6 to 8.5 on non-working days. 26 of 30 season parts start on a Monday; the other four are the `.1`
   parts starting 1 April.
2. **Times and dates.**
   - `Date` is written `dd/mm/yyyy` in the raw CSV (`01/04/2021`); registry format `%d/%m/%Y`; silver `date` is a Date.
   - The four window columns are `HH:MM` strings (all 1,826 rows match `^\d\d:\d\d$`), no zone marker, kept as text;
     NESO's dictionary gives no zone or unit. The gridflow research (K-AS-2-FACTS 611) calls a UK-local reading a
     "contextual inference" from NESO's STOR guidance. The rows cannot settle it: within one season part the labels do
     not move at a clock change (part `.6` spans late March, part `.5` late October) under either reading. The page
     claims neither UTC nor UK time ("`HH:MM` text with no zone stated"; plot axis "window labels as NESO writes them;
     no zone stated").
   - No window crosses midnight (end later than start in every row, both windows); the guide says "in this file".
   - `timestamp_utc` = `event_time` = `settlement_period_to_utc(date, 1)`, UK midnight of `date` as UTC
     (`silver/neso_data_portal/casting.py` 618-625): 2025-03-30 gives 2025-03-30 00:00Z, 2025-03-31 gives
     2025-03-30 23:00Z. The eight rows straddle the 30 March 2025 clock change to show it.
   - `published_at` = `available_at` = CKAN `last_modified` 2026-07-27 14:25:54.738965 on every row (vintage
     `ckan_last_modified`).
   - Workbench: `query()` designated column `date` (DATE), `BETWEEN` both ends inclusive, relation
     `silver_neso_data_portal_stor_windows_latest`, excludes `event_time`, `available_at`, `vintage_policy`,
     `source_run_id`, `dataset_version`, `month`, `year` (checked by calling `_get_method_registry` in the
     gridflow_models venv). The notebook converts `timestamp_utc`, `published_at`, `capture_written_at` from the session
     zone to UTC, and its output shows `uk_time` 00:00 on each row across the clock change.
3. **Captures.** One silver file (`stor_windows_20261008_run2026-10-08T11-27-43...parquet`, 1,826 rows) and one bronze
   capture (`raw_20261008T112743Z_..._6e5c1515.csv`: 1,827 lines = header + 1,826, 80,748 bytes = sidecar
   `declared_content_length` and `body_size_bytes`, CRLF, BOM, no tab, no padded comma). Not truncated. One capture
   cannot repeat rows: no `dedup:` on the chart or frame.
4. **Chart: no hold.** The table has no numeric measure and the spec cannot turn `HH:MM` text into times, so a time
   chart of the windows is not possible. I chose a bar: delivery dates counted by `season` for Season 19, 1 April 2025
   to 31 March 2026 (filters on `date`, inclusive): 19.1 27, 19.2 112, 19.3 35, 19.4 28, 19.5 91, 19.6 72 (365). Each
   key note carries that part's dates and its working and non-working windows, so the chart is how NESO divides the
   last season and the key is what each part commits. The notebook plot draws the windows themselves (12 bars on a
   06:00 to 22:00 axis of labels). If Bobbo finds a count chart too thin, the fallback is `chart: {type: none,
   reason: ...}` (the template supports it: the topsoil then shows no chart), not a page hold: the rows are complete,
   correct and unambiguous apart from the undocumented clock.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Key `date`, one row per delivery date | registry `entity_key: [date]`; Polars `n_unique` 1,826 = rows |
| `Date` "Delivery date"; window columns "Start/End time for delivery window 1/2"; no unit | field-info snapshot `20261008T114228Z/stor_windows.json` |
| Windows on each STOR service day where STOR must be provided, Day Ahead Service Terms | catalogue snapshot `20261006T195819Z`, package `notes` |
| History "Seasons 15 to 19, applicable 1 April 2021 to 1 April 2026 (NESO)" | same `notes` |
| Cadence "Ad hoc (NESO)"; last modified 27 July 2026 | package `extras` "Update frequency: Ad hoc"; resource `last_modified` 2026-07-27T14:25:54.738965; visible as `published_at` in the eight rows |
| `HH:MM` text, no zone stated | registry dtype `string`; dictionary unit and description carry no zone |
| Same windows in each part across all five seasons | Polars group by (part, day type): 1 form each, 5 seasons each; notebook cell 4 |
| 10 to 13.5 committed hours on working days | notebook cell 4 `hours` column (10.0, 11.0, 11.5, 12.0, 12.5, 13.5) |
| `timestamp_utc` UK midnight as UTC, 23:00 the evening before in summer | `casting.py` 618-625 (`settlement_period_to_utc(date, 1)`); eight rows; notebook cell 3 |
| `wd_nwd` kept as NESO flags it | registry: string column, no transformer; no derivation in `generic.py` |
| No window crosses midnight in this file | Polars: end <= start, 0 rows for each window |
| Chart values and alt | committed series `x` 19.1..19.6, `values` [27, 112, 35, 28, 91, 72]; season spans from Polars min/max `date` per label |
| Key note windows | Polars group by (season, `wd_nwd`) for Season 19 |
| Raw request URLs | bronze sidecar `request_url`; `package_show?id=stor-windows` per the sibling approved pages |
| Downloaded whole unless `last_modified` unchanged | `connectors/neso_data_portal/client.py` 1751-1767 |
| `--last 24h` commands | same rules as the approved STOR auction, OBP and SFFR pages (48 h tolerance, 7 d cap) |
| `query()` relation, column, bounds, drops | `_get_method_registry` called live in the gridflow_models venv: `date`, DATE, `BETWEEN`, relation `_latest` |
| Plot alt | the committed PNG (looked at): working days 06:00/06:30 to 13:00/14:00, then 16:00 to 19:00 starts to 20:30/22:00; non-working days start 10:00/10:30 |
| Related notes | auction dictionary ("for the availability windows"); buy-curve package notes ("used in the daily assessment process"); notices family reviewed in the sibling (delays, failures, one requirement change); EAC note reused from the approved sibling |

## Body corrections (vault note)

1. Opening paragraph: the `TODO: verify` on how a committed window relates to payments and to the auction results now
   quotes NESO's package notes ("define the committed windows for each STOR Service Day where STOR is required to be
   provided ...") and the auction dictionary ("for the availability windows"); the payments part stays a TODO, and it
   says gridflow joins neither table to the other. Smallest span, 2 lines to 6.

## Unverified

- The clock of the window labels (UK local or UTC). Not claimed on the page.
- Whether the auction's "availability windows" are exactly these committed windows (likely, not stated by NESO).
- What the decimal part of a season label means beyond "a part of Season N"; NESO's dictionary gives only "time frame
  for which the committed STOR windows apply".

## Open questions

- Is a count-by-season bar acceptable, or does Bobbo prefer `type: none` for a calendar with no measure (see question 4)?

## Template notes (not page findings)

- The chart spec has no derived columns, so clock-label tables (start and end `HH:MM` text) cannot be drawn as
  time-of-day bands. A band or Gantt chart type would suit this table and similar window registers.
- Key notes wrap time ranges at the hyphen (`10:30-` / `13:00`) at 1024, 768 and 390; readable, not clipped.
- The notebook panel tab truncates and the caveat-grammar warning (22 lines) are template-wide, as on the sibling.

## Defects

- **NESO data observation (not gridflow):** NESO's STOR windows file flags 19 September 2022 (the bank holiday for the
  Queen's state funeral) as `WD`, while every other weekday bank holiday in its span from 2021 to 2026 is `NWD`
  (42 weekday `NWD` dates, including 3 June 2022 and 8 May 2023). NESO's flag is authoritative and its working-day
  rule is unpublished in the package, so this may be intended. Vault note only; no gridflow fix; the page shows the flag
  as written and claims no rule.
- No gridflow defect found.
