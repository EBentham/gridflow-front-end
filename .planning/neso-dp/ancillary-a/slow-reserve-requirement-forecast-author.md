# Slow Reserve requirement forecast: author report

One-table page `slow-reserve-requirement-forecast` (table `slow_reserve_requirement_fc`). Writer, 2026-10-18.

## Status

- `gridflow-build --only neso_data_portal/slow_reserve_requirement_fc`: success. The only stderr line is the known
  warning about 3 dropped "Known issues and gotchas" lines; this note has no such section.
- Detector on `site/hifi/data-sources/neso_data_portal/slow-reserve-requirement-forecast.html`: `[]`.
- Built page: 0 em dashes, en dashes, middle dots, arrows; no "locally", "our", "live", "now", planning words
  (the only "our" hits are inside "hour").
- Canonical note edited with the Edit tool; CRLF kept in the working copy (`autocrlf` on, repo stores LF). Vault diff
  against `origin/master`: +124 / -4 (the `page:` block, `updated`, one body span). Mirror copied and `cmp` equal.
- Artefacts (worktree `C:\gridflow-wt\fe-neso-as-a`):
  `site/hifi/data/series/neso_data_portal/slow_reserve_requirement_fc.json` (spec_origin vault, 2 series over 39
  service days, 8 + 31 points, 1,874 rows used), `site/hifi/data/samples/neso_data_portal/slow_reserve_requirement_fc.json`
  (gridflow-sample, 8 rows), `site/hifi/data/notebooks/neso_data_portal/slow_reserve_requirement_fc.json` and
  `slow_reserve_requirement_fc-5.png` (run_notebooks.py, 5 cells, no errors). No staged chart spec or authored
  override existed.
- Screenshots at 1440, 1024, 768 and a 390 px iframe, every section looked at: nothing clipped or overlapping. The
  site has no dark scheme. Shots in the session scratchpad `sr-writer\shots\` (f-<width>.png full, s-<width>-<n>.png).
- Server on 9946 stopped. 9670 not touched. No git writes.

## The page in one paragraph

Thin and flat. Silver holds one capture of NESO's one file (last modified 2026-09-22 14:48:32 UTC): 39 service days,
23 September to 31 October 2026, 48 windows each and 50 on 25 October, and both requirement columns read 1,800 MW in
every one of the 1,874 windows. What does vary is the production date: service days 23 to 30 September were
produced on 31 August, 1 to 31 October on 22 September. A two-column chart would draw one line exactly on top of
the other, so the chart is the positive requirement per service day (mean of the day's windows), split into two
series by `forecast_produced_on` (petrol for 31 August, clay for 22 September), `y_min: 0`. Both key notes say
positive and negative are both 1,800 MW in every window of those days. Frame: windows 5 and 6 on 30 September and
1 October (either side of the production-date change) and `5`, `5x`, `6`, `6x` on 25 October (the repeated hour,
with identical start labels); `forecast_produced_on` is third so it shows in the folded frame at 1440 and 1024.
Notebook: `data.sql` on `_latest`, a per-production-date summary (first and last service day, days, windows),
`value_counts` of the two MW columns (one pair, 1,800 and 1,800, 1,874 windows), and a plot of days between
production date and service day (23 to 30 for 31 August, 9 to 39 for 22 September).

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Key `auction_date`, `service_window`; `_latest` whole capture; vintage = CKAN `last_modified`; issue `none` | registry `src/gridflow/connectors/neso_data_portal/registry/slow-reserve-requirement-forecast.json` (`entity_key`, `latest: whole_capture`, `vintage: ckan_last_modified`, `issue: {kind: none}`) |
| One row per auction date and window, 48 on an ordinary day (grain) | silver: 1,874 rows, 1,874 distinct keys; 38 days x 48 + 25 October x 50 |
| `5x`, `6x` on 25 October (service_window field, record caption) | silver 25 October: `5`, `6`, `5x`, `6x`, start labels `01:00`, `01:30` twice. Scoped to 25 October, not stated as a clock-change rule (NESO's dictionary comment contradicts the file; note body Known issues) |
| MW, both columns (fields, chart unit) | registry header `... Requirement MW`; dictionary `field-info/20261008T114228Z/slow_reserve_requirement_fc.json` unit `MW` |
| Negative given as a positive figure | silver: `negative_slow_reserve_requirement_mw` = 1800.0 on every row |
| Window start and end UK local, kept as text | dictionary comment "Time given in local time"; registry dtype `string` |
| Window 1 starts 23:00 the day before | dictionary `Service Delivery Date` comment "service window 1 starts at 23:00 D-1"; silver 2026-09-23 window 1 `22/09/2026 23:00` |
| End `:29` / `:59` | silver: every end is start + 29 minutes (note body: 1,740 s on all rows) |
| `forecast_produced_on` a date, not a publication time | registry dtype `date`, issue `none`; dictionary "Date that the forecast was produce[d]" |
| `auction_date` meaning | dictionary "The date of the auction event that these requirements apply to." |
| `timestamp_utc` = UK midnight of the service day in UTC; window 1 an hour earlier | registry `temporal: date_sp1(service_delivery_date)`; silver 23 Sep -> 2026-09-22 23:00 UTC, 25 Oct -> 2026-10-24 23:00 UTC, 26 Oct -> 2026-10-26 00:00 UTC; window 1 = 23:00 local the day before, one local hour before local midnight on every day |
| `published_at` = file last-modified read as UTC | `vintage: ckan_last_modified`; sidecar `ckan_last_modified` 2026-09-22T14:48:32.823004 = silver |
| Reacts to loss of generation or demand, plus or minus 0.2 Hz within 15 minutes; daily auction; windows from 23:00 the evening before; "daily forecast"; "updated monthly" (what_it_is, summary, cadence) | catalogue snapshot `20261006T195819Z`, package `notes` and extras `Update frequency: Monthly` |
| One CSV file, no archive | catalogue `num_resources: 1`; registry one resource |
| Chart: 1,800 MW flat, 8 + 31 points, two production dates (alt, key notes) | committed series: `aug` 2026-09-23..30 {1800}, `sep` 2026-10-01..31 {1800}; silver by `forecast_produced_on`: 31 Aug 384 rows (23 to 30 Sep), 22 Sep 1,490 rows (1 to 31 Oct) |
| "positive and negative both 1,800 MW in every window" (key notes) | silver: unique positive {1800.0}, unique negative {1800.0}; notebook cell 4 output |
| `query()` reads `silver_neso_data_portal_slow_reserve_requirement_fc_latest`, filters `service_delivery_date` (DATE, BETWEEN) | resolved in the models interpreter: `_validate_dataset_for_source` -> `service_delivery_date`, `_RELATION_NAME_BY_DATASET` -> `..._fc_latest`; `_get_method_registry.py` `_date_range_predicate`; gridflow `silver/date_columns.py:57` |
| Raw requests | sidecar `request_url` of the only capture; `package_show` as on the approved DM and BR pages |
| `--last 24h` ingest and transform; dates select nothing; skip when `last_modified` unchanged | `client.py:1474` (`_assert_window_admissible`), `client.py:1752-1765` (unchanged skip); same as the approved DM page |
| How used, EAC join: convert the UK local start to UTC | `eac_results_summary` has `PSR` and `NSR` rows with UTC `delivery_start`, 30-minute windows; converting each start label from Europe/London (`5x`, `6x` as the second occurrence) matches 1,200 of 1,200 windows for each product over 23 Sep to 17 Oct. The flat requirement cannot tell local from UTC by value; the local-time fact rests on NESO's dictionary |
| Related: Quick Reserve has "the same columns and key" | registry `quick-reserve-auction-requirement-forecast.json`: same eight silver columns and dtypes bar the product word in the two MW names, same `entity_key`, `temporal`, `latest`, `vintage`, `issue`, refresh monthly, one upload resource. (Its vendor header spells `Service window Start Time`; silver names are the same.) |
| Related: Balancing Reserve "the same windows plus a forecast type" | registry `balancing-reserve-auction-requirement-forecast.json`: same window columns, key and recipe, plus `forecast_type` |
| Related: EAC results "Cleared `PSR` and `NSR` MW and price for each half-hour window" | silver `eac_results_summary`: products PSR, NSR, 30-minute delivery, `cleared_volume`, `clearing_price` |
| Related: `elexon/system_prices` | same note as the approved BR page |

## Body corrections (canonical note)

1. "It has the same layout ... and as @balancing-reserve" was wrong for Balancing Reserve: its records carry a ninth
   column, `forecast_type` (registry). Now "the same window columns as @balancing-reserve..., whose records add a
   `forecast_type` column (gridflow registry ...)". The Quick Reserve half of the sentence is right and kept.
2. Front matter `updated` 2026-10-13 to 2026-10-18.

Nothing else in the body changed. The capture facts (one capture, 2026-10-08, 1,874 rows, 1800 MW) are still true:
bronze and silver hold only that capture, so the truncated-capture risk does not arise for this table.

## Issue time versus delivery window, and earlier editions

- No row carries an issue instant. `forecast_produced_on` is a date; `published_at` is the whole file's last-modified
  time. The page says both plainly and never calls either an issue time.
- The file holds one forecast per auction and window (key distinct), produced on two dates. Whether NESO keeps,
  replaces or appends earlier editions at its monthly update cannot be measured from one capture, so the page says
  nothing about it beyond "updated monthly" (NESO) and the two production dates visible in the chart and rows.

## Unverified

- Spring clock-change layout: no spring service day in the file; the page states the `5x`/`6x` fact for 25 October
  only.
- The 14:00 auction time zone: NESO gives none; the page leaves 14:00 out.
- What "positive" and "negative" Slow Reserve denote: NESO does not say; the page does not interpret them.
- Cleared `NSR` in `eac_results_summary` is 0 MW in all 1,200 windows from 23 September to 17 October, against a
  1,800 MW negative requirement (cleared `PSR` 1,793 to 1,868 MW, mean 1,803). Not on the page.

## Open questions

1. Chart choice: positive only, split by production date, because the two MW columns are identical and would overlap.
   The key notes carry the negative value. If the seat prefers both columns as `values` (one hidden line), say so.
2. A later capture would show whether the monthly update replaces or extends the file and whether the 31 August
   forecasts were superseded; worth a periodic capture.

## Template problems (report only)

- Notebook runner adds a stray column to the grouped table (cell 3 shows `forecast_produced_on` as a trailing header
  with empty cells); already listed under the batch file's template follow-ups.
- Notebook preview wraps long identifiers mid-word at 390 and 768; already listed.
- At 390 the folded frame shows only `service_delivery_date` and `service_window`; already listed for 768.

## Checker: look hardest at

- The chart: positive only, split by `forecast_produced_on` through a `group_map` on the date text; confirm the
  caption and key notes make plain it is the positive requirement and that negative matches.
- The `service_window` field line scoped to 25 October against NESO's contradicting dictionary comment.
- The related note claiming Quick Reserve has "the same columns and key" (registry comparison above).
- The EAC join bullet: the flat requirement cannot prove the local-time reading by value; it rests on the dictionary.

## Defects

- No gridflow or data defect found on this package (one complete capture, no nulls, keys distinct, values as served).
- Vendor documentation: NESO's `Service Window` dictionary comment puts the repeated hour at `7x`/`8x` on the spring
  change and says the autumn change has no windows 5 or 6; the file's 25 October has `5`, `6`, `5x`, `6x`. Already in
  the note's Known issues; no new defect.
- Observation for the EAC owners (not a defect claim): cleared `NSR` volume is 0 MW in every `eac_results_summary`
  window from 23 September to 17 October 2026, while NESO's forecast negative Slow Reserve requirement is 1,800 MW.
