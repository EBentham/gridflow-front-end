# System frequency (`system-frequency-data`): writer's revision 2

Answers `system-frequency-data-review.md` (REVISE, 0 blockers, 2 majors, 7 nits). Page words only: the chart spec,
the row selection and the notebook cells are unchanged, so the series, sample and notebook artefacts stand
(digests pass; notebook not re-run). No server started; no screenshots this round.

## Status

- Note `C:\gridflow-wt\vault-neso-sys\30-vendors\neso-data-portal\datasets\system-frequency-data.md`: 893 lines, all
  CRLF; diff against the branch base is additions only (145 lines, the `page:` block).
- Mirror `C:\gridflow-wt\fe-neso-sys\vault\neso_data_portal\system-frequency-data.md`: `cmp` clean.
- `gridflow-build --only neso_data_portal/system_frequency`: passes (the 35-dropped-lines warning is the existing
  "Known issues" grammar warning, not this page).
- Detector: `[]`. Rendered page: 0 em dashes, 0 en dashes, 0 arrows, 0 middle dots.

## Findings and fixes

| # | Severity | Field | Fix |
|---|---|---|---|
| 1 | major | `family.members[0].differs`; `raw_feed.note` | Lead now reads "Bronze only, no table: every monthly file lands here for the five tables below". Raw note now opens "`system_frequency` holds the files, no table." and ends "The other four tables transform like the second line." (true of all four, the held 2014 table included: it is sibling-fed from the same bronze and has silver). |
| 2 | major | `record.caption` | "Silver `system_frequency_gmt_csv`, 26 March 2023: the hour UK clocks skip is present; labels are GMT." Names the frame's table; the bronze-only lead is stated in the member well and the raw note. |
| 3 | nit | `record.caption` | Same caption: says what the eight rows show (no skipped hour, so GMT labels). |
| 4 | nit | `raw_feed.commands` comments | Ingest: "about 9.4 GB, bronze only" (NESO's declared sizes in the 152 sidecars sum to 9,381,661,800 bytes). Transform: "the date's `_gmt_csv` captures to silver". |
| 5 | nit | `related[2].note` | "NESO's frequency response auctions before EAC". |
| 6 | nit | `related[0].note` | "Elexon's GB frequency, one sample every 15 seconds". |
| 7 | nit | `notebook.lead` | Adds "cell 5 counts a clock-change day per table" (cell numbers match the page's `[3]` and `[5]`); dropped "(equal to `dtm`)" for budget; the column guide still says it. |
| 8 | nit | `chart_view` x axis | **Template limit, for the seat:** a 30-minute intraday axis gets one tick label (`13:00`), because `chart_svg._time_axis` ticks only on whole hours for spans of two days or less. The x label gives the range and the key note gives the dip's times. Needs sub-hour ticks (for example every 5 or 10 minutes when the span is under two hours). |
| 9 | nit | members, chart caption | `_gmt_csv` differs now: "April 2022 on, plain CSV, GMT as UTC; August 2026 midnights are bare dates". Chart caption now says the rows come "from NESO's file last modified 17 April 2026" (December 2023's re-upload); "1,800 readings" moved out (it stays in the alt range and key). |

Held line (2014): "NESO's descriptions give no 2014 zone, and October repeats an hour, so it is not loaded." (16
words.) No note body change: the body already says October 2014 fails its key and is not served, with the 3,600
repeated labels and 7,200 rows in duplicate groups ("`system_frequency_dmy_csv`" section and "Holds").

## Defects

- **gridflow silver, held 2014 table (known, adjudicated):** `system_frequency_dmy_csv` serves 11 of 12 months; October
  2014 fails `(resource_id, dtm)` with `DuplicateEntityKeyError` on 7,200 rows (labels `26/10/2014 01:00:00` to
  `01:59:59` twice). Adjudicated `failed` under ADR-040 (ruling 861), and documented in the note body; the page's held
  line now says October is not loaded. Not a new defect, but the key cannot serve the whole year until NESO states
  which repeated row is the BST hour.
- **gridflow_models: the workbench serves the held 2014 table, filtered by capture time** (from revision 1).
  `query("system_frequency_dmy_csv", ...)` has no hold check and filters `timestamp_utc`, the capture time: a 2014
  window returns 0 rows, a window on 8 October 2026 returns all 28,857,600 held rows (DuckDB count).
- **gridflow_models: `list_datasets("neso_data_portal")` names `system_frequency`, which `query()` rejects** as unknown
  (the bronze home has no silver relation) (from revision 1).
