# Quick Reserve requirement forecast: author report

One-table page `quick-reserve-auction-requirement-forecast` (table `qr_auction_requirement_fc`). Writer, 2026-10-18.

## Status

- `gridflow-build --only neso_data_portal/qr_auction_requirement_fc`: success. The stderr warning about 3 dropped
  "Known issues and gotchas" lines is the known one; this note has no such section.
- Detector on `site/hifi/data-sources/neso_data_portal/quick-reserve-auction-requirement-forecast.html`: `[]`.
- Built page: 0 em dashes, en dashes, middle dots, arrows; no "locally", "live", "now", planning words (the 10 "our"
  hits are all inside "hour").
- Canonical note edited with the Edit tool; working file CRLF throughout (406 lines, 406 CRLF; the repository blob is
  LF, so checkout converts). Vault diff against `origin/master`: +128 / -1 (the `page:` block, `updated`, two
  inserted body sentences). Mirror copied and `cmp` equal.
- Artefacts (worktree `C:\gridflow-wt\fe-neso-as-a`):
  `site/hifi/data/series/neso_data_portal/qr_auction_requirement_fc.json` (spec_origin vault, 2 series x 48 points,
  96 rows used, 48 matched),
  `site/hifi/data/samples/neso_data_portal/qr_auction_requirement_fc.json` (gridflow-sample, 8 rows),
  `site/hifi/data/notebooks/neso_data_portal/qr_auction_requirement_fc.json` and `-6.png` (run_notebooks.py, 6 cells,
  no errors). No staged chart spec or authored override existed.
- Screenshots at 1440, 1024, 768 and a 390 px iframe, every section looked at: nothing clipped or overlapping. The
  site has no dark scheme (as the earlier pages in this batch found). Shots in the scratchpad `qr-writer\`
  (`f-<width>.png` full, `s-<width>-<n>.png` slices).
- Server on 9945 stopped. 9670 not touched. No git.

## Data truth

- One capture only (bronze 2026-10-08T11:16:53Z, CKAN `last_modified` 2026-09-22T14:48:27.491459), so the truncated
  capture risk does not apply: there is no newer capture to compare.
- 1,874 rows, 1,874 distinct `(auction_date, service_window)`. One row is one auction date and half-hour service
  window. 39 service days, 23 September to 31 October 2026; 38 days of 48 windows and 25 October with 50 (`5x`, `6x`).
  `service_delivery_date` is `auction_date` + 1 day on every row (measured; not stated on the page as a rule).
- Units: MW for both requirement columns (vendor dictionary `unit: MW`, registry header "... Requirement MW").
- Issue time versus delivery window: the file has no issue instant. `forecast_produced_on` is a date (registry dtype
  `date`, `issue: {kind: none}`); `published_at` is the file's CKAN last-modified read as UTC (`vintage:
  ckan_last_modified`). Windows run on the UK local clock from 23:00 the evening before the service day.
- Earlier editions: no window appears twice, so the file shows one forecast per window. It mixes two production
  dates: 31 August 2026 for service days 23 to 30 September (384 rows), 22 September 2026 for 1 to 31 October
  (1,490 rows). Whether NESO replaces or appends at its monthly update is unknown from one capture; the page says
  only "NESO updates it monthly" and shows the two production dates in the frame and notebook.
- Values: one profile on every day, under both production dates: positive 500 MW in window 1 (23:00), 300 MW in
  windows 2 to 13 (23:30 to 05:30; 14 windows with `5x`, `6x` on 25 October), 500 MW in windows 14 to 48; negative
  300 MW on all 1,874 rows.
- Slow Reserve sibling: the registry (`slow-reserve-requirement-forecast.json`) has the same eight-column layout
  (MW column names differ; it spells `Service Window Start Time` with a capital W), the same entity key, `latest`,
  `vintage` and temporal recipe. That is the only basis for the related line and the body sentence. I touched no
  Slow Reserve file.

## The page in one paragraph

Chart: line, `values` = positive and negative MW, filtered to service day 1 October 2026 (auction 30 September,
produced 22 September), x = `service_window_start_time` read with `time_text` `%d/%m/%Y %H:%M` (the local label drawn
on its own clock, as on the Balancing Reserve page), `y_min: 0`. Positive 500, 300 from 23:30, 500 from 05:30;
negative flat 300; the lines meet from 23:30 to 05:00. Frame: windows 1, 2, 13, 14 of service days 30 September
(produced 31 August) and 1 October (produced 22 September), file order; columns put both MW columns and
`forecast_produced_on` in view at 1440. Notebook: `data.sql` on `_latest`, a summary per production date (first,
last, day count, file time), value counts of the MW pair, the low-run windows per day (38 days 2 to 13, one day 14
windows), and a step plot of 1 October.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Key `auction_date`, `service_window`; `_latest` whole capture (facts Key, record.key) | registry `quick-reserve-auction-requirement-forecast.json` (`entity_key`, `latest: whole_capture`); silver 1,874 distinct of 1,874 |
| One row per auction date and window, 48 on an ordinary day (grain) | silver: 38 days x 48 + 25 Oct x 50 |
| Positive and negative Quick Reserve, pre-fault disturbances, frequency near 50.0 Hz, daily auction, delivery 23:00 to 23:00 (what_it_is) | catalogue snapshot `20261006T195819Z` package `notes` and resource description |
| Updated monthly (facts, what_it_is, notebook lead) | same snapshot: extras `Update frequency: Monthly`; notes "The data set is updated monthly." |
| One CSV file, no archive (facts) | snapshot `num_resources: 1`; registry one resource |
| MW, NESO's unit (fields) | field info `field-info/20261008T114228Z/qr_auction_requirement_fc.json` (`unit: MW` on both) |
| Windows on the UK clock, window 1 23:00 the day before (what_it_is, fields, caption, x label) | same field info: "Time given in local time"; "service window 1 starts at 23:00 D-1"; silver labels |
| UK-local reading fits EAC results better (how_used join bullet) | joined requirement to `eac_results_summary` `PQR`/`NQR` on `delivery_start`: label read as UK local, 1,200 windows over 25 days, mean absolute gap 44.0 MW (positive); read as UTC, 59.3 MW. Report only |
| `PQR`, `NQR` in EAC results, half-hour (how_used, related) | silver `eac_results_summary`: products PQR and NQR, 18,768 rows each, delivery 30 min, 2026-03-31 22:00 to 2026-10-17 21:30 UTC |
| Autumn adds `5x`, `6x`, unlike NESO's dictionary (service_window field) | silver 25 Oct rows `5x`, `6x` repeating `5`, `6` start labels; dictionary comment says 7x/8x at GMT to BST and no 5 or 6 at BST to GMT |
| End label `:29`/`:59` (field) | silver rows |
| Negative given as a positive figure (field) | silver: 300.0 on every row |
| `forecast_produced_on` a date, not a publication time (field) | registry dtype `date`, `issue: {kind: none}` |
| `timestamp_utc` = UK midnight of the service date in UTC; window 1 an hour earlier (field) | registry `temporal: date_sp1(service_delivery_date)`; silver 1 Oct -> 2026-09-30 23:00 UTC; 25 Oct -> 24 Oct 23:00 UTC; 26 Oct -> 26 Oct 00:00 UTC; one value per day |
| `published_at` = file last-modified read as UTC (field) | registry `vintage: ckan_last_modified`; sidecar `ckan_last_modified` 2026-09-22T14:48:27.491459 = silver |
| Chart values, alt, key notes | committed series: 48 x, 2026-09-30T23:00 to 2026-10-01T22:30; positive changes 500 -> 300 at 23:30, 300 -> 500 at 05:30; negative {300} |
| "the same on every day in this file" (key notes) | notebook cell 5 (38 days windows 2 to 13, one day 14 windows), cell 4 (only 500/300 and 300/300 pairs); silver profile scan |
| Sample caption: service days 30 Sep and 1 Oct, produced on different dates | sample rows: produced 2026-08-31 and 2026-09-22 |
| Raw requests | sidecar `request_url`; `package_show?id=<slug>` as on the DM and BR pages (`endpoints.py`) |
| `--last 24h`; dates select nothing; skip when `last_modified` unchanged (raw note, commands) | `client.py:1474-1545` (window admissibility), `client.py:1750-1765` (unchanged skip); same as the approved DM and BR pages |
| `query()` reads `silver_neso_data_portal_qr_auction_requirement_fc_latest` on `service_delivery_date` (notebook lead) | resolved in the models interpreter: `_DATE_COLUMN_BY_DATASET['qr_auction_requirement_fc'] = service_delivery_date`, `_relation_name_for_dataset` -> `..._latest`; `silver/date_columns.py:57` (DATE) |
| Related: Slow Reserve same layout and key | registry comparison above |
| Related: Balancing Reserve on the same windows | BR approved page (window 1 23:00, 48 windows, same EAC explainer) |
| Related: `elexon/freq` | vendor "return the frequency close to 50.0 Hz"; `vault/elexon/freq.md` |

## Body corrections (canonical note)

1. "Row counts and shape": added one sentence after "These are single-capture observations ...": every service day
   carries the same positive profile (window 1 500, windows 2 to 13 and `5x`, `6x` 300, windows 14 to 48 500) under
   both production dates (silver, 2026-10-18).
2. "Related": added that Slow Reserve has the same eight-column layout, key, clocks and temporal recipe, citing the
   gridflow registry file, with a link to its note.
3. Front matter `updated` 2026-10-13 to 2026-10-18.

No existing sentence was changed. The body's capture facts (one capture, 2026-10-08; two production dates; 9 to 39 day
leads) re-checked and true.

## Unverified

- The time zone of NESO's "daily auction at 14:00" (no zone given). Not on the page.
- Whether NESO replaces the file or appends at each monthly update, and whether values are amended in place: one
  capture. The page claims neither.
- What positive and negative denote (direction): the vendor text does not say; the page states neither.
- Whether the requirement is what NESO buys: cleared `PQR` sits at 295 to 350 MW where the requirement is 300 and
  66 to 547 MW (median 495) where it is 500, over 23 September to 17 October. Not on the page.

## Open questions

1. A second capture after NESO's next monthly update would show whether past days are dropped and whether the 31 August
   rows are replaced. Worth keeping the package on the periodic capture.
2. The line renderer joins window points with slopes, so a half-hour step reads as a diagonal between two windows (as
   on the Balancing Reserve page). The notebook carries a true step plot.

## Template problems (report only)

- At 1024 and 768 the folded frame shows only `auction_date`, `service_window` and the positive MW column; the
  negative column and `forecast_produced_on` need unfolding (known item).
- Notebook preview breaks long names mid-word at 768 and 390, and the tab label clips at 390 (known items).
- The notebook's first output carries the stray grouped-table column (known item).
- The series file stamps the local labels with `Z` (known item).

## Checker: look hardest at

- The key notes' "the same on every day in this file": scoped to the file, backed by notebook cells 4 and 5.
- The `service_window` field line ("autumn clock change adds `5x`, `6x`, unlike NESO's dictionary") against the
  dictionary comment and the 25 October rows.
- The `time_text` x axis: the local labels drawn on their own clock; caption and x label say so.
- The related Slow Reserve line ("same file layout and key"): code-only basis, the registry.

## Defects

- No new gridflow or data defect on this package. The table has a single complete capture.
- Vendor documentation (already in the note's Known issues): NESO's column dictionary for `qr_auction_requirement_fc`
  says the GMT to BST change repeats windows `7x`, `8x` and the BST to GMT day has no windows 5 or 6; the served file's
  autumn day (2026-10-25) has `5`, `6`, `5x` and `6x`, matching NESO's EAC explainer. The dictionary also gives ISO
  examples while the file serves day-first dates.

## Nits fixed (after the checker's APPROVE with 2 nits)

1. `record.fields.service_window`: now "`1` to `48`; autumn change day adds `5x`, `6x`; NESO's dictionary omits `5`, `6`"
   (14 words). It says what the dictionary claims for that day ("no service window 5 or 6" at the BST to GMT change)
   against the file's 25 October rows `5`, `6`, `5x`, `6x`.
2. `chart_view.key[0].note`: now "300 MW for windows starting 23:30 to 05:00, else 500 MW; the same every day in this
   file." (18 words). Matches the series (300 MW for the windows starting 23:30 to 05:00, 500 MW from the 05:30 window)
   and the alt text.

Re-checked: canonical note CRLF kept (406 lines, 406 CRLF), mirror `cmp` equal; `gridflow-build --only
neso_data_portal/qr_auction_requirement_fc` wrote the page (only the known dropped-caveat warning; the build's "2
error(s) on pages not rendered by --only" are on other agents' pages: it sets aside only errors that do not name
this page); detector `[]`; 0 em dashes; both new lines present in the built page. Artefacts unchanged (no chart,
sample or notebook field touched). No server started; 9670 untouched; no git.
