# Monthly operational metered wind output: writer's report (round 1)

Package page `monthly-operational-metered-wind-output`, one table `metered_wind_output_monthly` (eligible), nine
April-to-March resources. Writer port 9804.

**Status:** build `--only neso_data_portal/metered_wind_output_monthly` passes; detector `[]`; 0 em dashes in the
page. Screenshots at 1440, 1024, 768 and 390 (390 in a 390 px iframe), light only (the site has no dark rendering).
Nothing clipped or overlapping.

## Files (mine only)

- Canonical note: `C:\gridflow-wt\vault-neso-gen\30-vendors\neso-data-portal\datasets\monthly-operational-metered-wind-output.md`
  (CRLF kept: 481 CRLF of 481 lines). Mirror `C:\gridflow-wt\fe-neso-gen\vault\neso_data_portal\monthly-operational-metered-wind-output.md`, `cmp` identical.
- Artefacts in `C:\gridflow-wt\fe-neso-gen\site\hifi\data\`: `series\neso_data_portal\metered_wind_output_monthly.json`
  (spec_origin vault), `samples\neso_data_portal\metered_wind_output_monthly.json` (gridflow-sample),
  `notebooks\neso_data_portal\metered_wind_output_monthly.json` and `-5.png` (run_notebooks.py).
- Built page `site\hifi\data-sources\neso_data_portal\monthly-operational-metered-wind-output.html`.
- No staged chart spec or authored override existed for this table.

## The four questions from the launch prompt

1. **What one row is.** Neither a wind farm nor a BM unit: one settlement date and half-hour settlement period in one
   yearly file, with three numbers, Scottish wind output, England/Wales wind output and their total, all **MW** per
   NESO's dictionary ("Operational Metered MW"; Total = "Total of Scotland and England/Wales Operational Metered MW").
   Not MWh. The dictionary does not say whether a value is a half-hour average or a spot reading.
2. **Times and coverage.** `timestamp_utc` = `event_time` = start of the period: GB-local midnight of `sett_date`
   converted to UTC plus 30 min x (period - 1); 0 mismatches over all 149,234 silver rows. `published_at` =
   `available_at` = the file's CKAN `last_modified`, read as UTC (one per capture). `_latest` is `whole_capture`
   partitioned by `resource_id`, so each yearly file keeps its own newest capture. **The adjudicated overlap is not
   August and September.** "M08/M09" in the ledger are the note's codes for the 8th and 9th files (2025-2026 and
   2026-2027). ADR-040 and `_reconcile_adjudications.json` adjudicate the 193 settlement keys 2026-04-01 P1 to
   2026-04-05 P1 that both files publish with conflicting values; both rows are served (no dedup, ADR-039 P-5).
   Honest coverage on the page: yearly files from 2018-19 (NESO's catalogue), the page stopping at NESO's
   3 October 2026 file (data to 1 October P1) because the 16 October upload renamed a column.
3. **Row counts and repeats.** See the evidence table. Within any capture 0 repeated keys; across files, 193 shared
   keys (April 2026). Chart: `dedup` on `[sett_date, sett_period]` by `published_at` (drops the 193 rows of the
   2025-26 file; the 2026-27 file wins, which is also the "file whose year contains the date" policy). Frame: `dedup`
   on `[resource_id, sett_date, sett_period]` by `published_at` as a guard against future recaptures, so both files
   still show. One 16 October recapture (2026-2027 file), failed at transform: see Defects.
4. **Chart and frame.** Stacked area, daily mean of each settlement date's half-hourly MW, England and Wales below
   (`horizon`), Scotland above (`hatch-lines`, as AGWS does for its second wind series), top edge = NESO's total,
   1 April 2025 to 30 September 2026 (548 days). I first drew 1 April 2018 to 30 September 2026 (3,105 days): the
   hatched band became noise, so I shortened it. Frame: 1 April 2026 periods 1 to 4 in both files (eight rows,
   values differ). Notebook: `query()` over 1 to 5 April 2026, times converted to UTC, rows per file, the 2026-27
   minus 2025-26 total per shared period, and its plot.

## Evidence table

| Claim (page) | Evidence |
|---|---|
| Grain: one row per settlement period and yearly file | registry `monthly-operational-metered-wind-output.json` `entity_key: [resource_id, sett_date, sett_period]`; silver: 0 duplicate keys over 149,234 rows |
| Units MW for the three value columns | NESO CKAN field info quoted in the note ("Operational Metered MW"); registry dtypes float64, no unit transform |
| Total is NESO's total of the two regions | dictionary text; silver: 0 rows where `abs(total - (scottish + england_wales)) > 1e-6` |
| `timestamp_utc` = GB midnight of `sett_date` + 30 min per period, UTC | registry `temporal: sp_pair`; silver: 0 mismatches against the formula; `event_time == timestamp_utc` on all rows |
| `published_at` = CKAN `last_modified`, read as UTC, one per capture | registry `vintage: ckan_last_modified`; silver: one `published_at` per `resource_id`, equal to the sidecar `ckan_last_modified` |
| Nine yearly files, 2018-19 to 2026-27 | registry `resources` (9, names 2018-2019 ... 2026-2027) |
| Cadence monthly (NESO's catalogue) | note: snapshot extras "Update Frequency: Monthly"; registry `refresh: monthly` |
| Periods 46 / 50 on clock-change days | silver days per file: 3,093 days of 48, 8 of 46, 8 of 50, 2 of 1 (the two partial final days) |
| 2025-26 and 2026-27 both cover 1 to 5 April 2026 and disagree | silver: 193 keys with 2 rows, 2026-04-01 to 2026-04-05; 2025-26 file 193 rows to 2026-04-05 P1; only 3 totals equal |
| 16 October upload renamed a column | bronze `2026/10/16/raw_20261016T204037Z_c9bc94c4-..._64345ea9.csv` header `England Wales Wind Output`; failure record `HeaderEpochError` in `C:\gridflow-data\state\neso_data_portal\completion_failures\metered_wind_output_monthly\996658c4....json` |
| Page stops at the 3 October file | silver `published_at` of the 2026-2027 resource 2026-10-03 11:17:29 UTC; data to 2026-10-01 P1 |
| Chart series: 548 days, 881 (16 Aug 2026) to 16,868 (25 Mar 2026), E&W larger on 443 days, 84 of 103 days above 12,000 between Sep 2025 and Mar 2026 | committed series JSON (sums of the two series per day) |
| Request URLs | connector `client.py` `fetch`/`iter_members`: one `package_show?id=<package>` then the resource download URL; exact URLs from the bronze sidecars' `request_url` |
| Commands `--last 24h` | same connector and wording as the approved constraint-breakdown and transmission-losses pages |
| `query()` reads `_latest` on `sett_date`, both ends inclusive, lineage dropped | gridflow_models `research/handles/source.py` `query()`; `_validate_dataset_for_source` -> `sett_date`; `_relation_name_for_dataset` -> `silver_neso_data_portal_metered_wind_output_monthly_latest`; `_BITEMPORAL_EXCLUDE` = event_time, available_at, vintage_policy, source_run_id, dataset_version, month, year |
| Notebook outputs: 2025-26 193 rows, 2026-27 240 rows; gap mean 31.3, median 31.5, min 0.0, max 70.9 MW | notebook JSON outputs; silver cross-check: max 70.874 at 2026-04-03 P5 (01:00 UTC), min 0.0 at 2026-04-02 P11/P12 |
| Related slugs resolve | build passes; `daily_wind_availability` is a table key (live page), `14-days-ahead-...` a family slug, `wind-bmu-boa-volumes` a package slug (held page) |

Per-capture counts (silver, all captures 2026-10-08):

| File | `published_at` (UTC) | Rows | Dates |
|---|---|---:|---|
| 2018-2019 | 2021-05-12 10:42 | 17,520 | 2018-04-01 to 2019-03-31 |
| 2019-2020 | 2021-05-12 15:33 | 17,568 | 2019-04-01 to 2020-03-31 |
| 2020-2021 | 2021-05-12 15:37 | 17,520 | 2020-04-01 to 2021-03-31 |
| 2021-2022 | 2022-04-13 13:09 | 17,520 | 2021-04-01 to 2022-03-31 |
| 2022-2023 | 2023-04-21 15:26 | 17,520 | 2022-04-01 to 2023-03-31 |
| 2023-2024 | 2024-04-15 11:23 | 17,568 | 2023-04-01 to 2024-03-31 |
| 2024-2025 | 2025-04-29 13:43 | 17,520 | 2024-04-01 to 2025-03-31 |
| 2025-2026 | 2026-04-07 10:00 | 17,713 | 2025-04-01 to 2026-04-05 (P1) |
| 2026-2027 | 2026-10-03 11:17 | 8,785 | 2026-04-01 to 2026-10-01 (P1) |
| 2026-2027 recapture (bronze only) | CKAN 2026-10-16 06:38 | 9,409 | 2026-04-01 to 2026-10-14 (P1); not in silver |

## Body corrections (canonical note)

- Capture list: added the 2026-10-16 recapture of the 2026-2027 file (bytes, rows, dates, header rename, failure
  record, and that its 8,785 shared keys repeat the earlier values exactly). Evidence: bronze body and sidecar,
  failure record above; Polars comparison of all three value columns, 0 differences.
- Identity and `_latest`: "Each resource has exactly one capture today" now says one *silver* capture, with the failed
  recapture noted.
- Cadence: added the 2026-10-16 modification and that the upload repeats the year to date; the TODO on whole-file
  replacement now notes the 16 October upload did.
- Operational consequence (ADR-040 R-1): added that the first recapture failed the header check before silver, so the
  family needs a second header epoch first (gridflow BACKLOG section 19).
- Front matter `updated:` 2026-10-09 -> 2026-10-24.

## Not verified

- Whether each value is a half-hour average or a spot reading (NESO's dictionary does not say; the page says so).
- The regional boundary NESO uses (the key note says NESO does not define it).
- Which file NESO considers authoritative for 1 to 5 April 2026 (the page states the chart's choice as its own).
- Dark mode: the site renders light only (as earlier writers found).

## Open questions for the seat

- The launch prompt's "August and September overlap" reads the ledger's `M08/M09` as months; they are file codes.
  The page states the April 2026 overlap.
- Once gridflow adds the second header epoch and transforms the 16 October capture, the page's "stops at its 3 October
  file" line, the chart window and the notebook outputs will need a refresh (and per ADR-040 R-1 the overlap ledger
  entry goes stale at the same moment).

## Template problems

- Headless Chrome leaves everything below the chart unpainted unless `--force-prefers-reduced-motion` is passed (the
  scroll-reveal `IntersectionObserver` in `site.js`). Worth adding to the checker's screenshot recipe.
- At 390 px the sample frame folds after its first column when the second is a long id (`resource_id`, 38
  characters), so the column that tells paired rows apart is only visible from 768 up. Not a page bug; noting it.

## Defects

- **NESO metered wind output monthly: 2026-27 file header drift (extends BACKLOG section 19).** NESO's 2026-2027
  upload of 2026-10-16 (CKAN `last_modified` 2026-10-16T06:38:45.339694) renames `England/Wales Wind Output` to
  `England Wales Wind Output`; the record's single epoch rejects it (`HeaderEpochError`, capture
  `raw_20261016T204037Z_c9bc94c4-6d8c-49ff-afff-67c0030bec05_64345ea9.csv`). The body is otherwise compatible:
  9,409 rows, 2026-04-01 to 2026-10-14 P1, 0 duplicate keys, and its 8,785 keys shared with the 2026-10-08 capture
  carry identical values in all three columns. Fix: add a second epoch mapping the new header to
  `england_wales_wind_output` (no semantics change), re-transform, and in the same PR re-point the ADR-040 overlap
  ledger entry to the new 2026-2027 capture (R-1: it goes stale otherwise). A fresh install today loads eight files
  and no 2026-27 rows.
- **No new data defect in the loaded rows.** The 1 to 5 April 2026 overlap is already adjudicated (ADR-040, RULINGS
  547). New detail for the NESO question: on all 193 shared keys the 2026-27 file's total is greater than or equal to
  the 2025-26 file's (0 to 70.874 MW, mean 31.3 MW), so the later file reads as a systematic upward restatement, not
  noise.

## Round 2 (review APPROVE with 8 nits)

All eight nits applied. Build `--only neso_data_portal/metered_wind_output_monthly` passes, detector `[]`, 0 em
dashes, note CRLF kept (486 of 486), mirror `cmp` identical. Chart spec, frame select and notebook cells unchanged, so
no artefact was regenerated. Re-shot 1440 and 390 for the prose changes: they fit with nothing clipped. Server on 9804
was started with its PID recorded and stopped by that PID only.

1. First half-hour of 5 April: `what_it_is` now says the two files "cover 1 April to the first half-hour of 5 April
   2026 and differ". The chart caption now says "Shared April 2026 periods use the 2026-27 file" (true for every
   shared period).
2. Why the page stops: `what_it_is` now says "This page stops at the 3 October file: gridflow does not read the header
   NESO renamed on 16 October." I left out "yet" because the batch rules ban it as a planning word.
3. `sett_period`: "Half-hour of the day, 1 to 48; 46 or 50 on clock-change days".
4. `timestamp_utc`: "Period start, UTC: GB midnight, plus 30 minutes for each period after the first".
5. Average or spot: the chart caption now says "(averages or spot readings: NESO does not say)". The guide lines for
   `england_wales_wind_output` and `total` now carry "average or spot not stated", like `scottish_wind_output`.
6. BOA related note: "Balancing acceptances taken on wind BM units".
7. No precedence: `what_it_is` says "NESO does not say which wins". The frame caption says "values differ; NESO names
   no precedence". To stay within the 60-word budget, NESO's settlement-metering caveat moved to the third `how_used`
   line ("Not settlement-grade: NESO expects it to differ from its settlement-metered forecasting metrics").
8. Note body: replaced the scheduler TODO with the fact (first daily refresh ran 2026-10-16, BACKLOG section 19,
   RULINGS 888). Added a "Fresh install" paragraph: until 20bp is fixed, the page's notebook returns no 2026-2027 rows
   on a fresh install.

Not applied: none.
