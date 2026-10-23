# Demand Flexibility Service 2022/23 test events: writer's report

Page `demand-flexibility-service-test-events` (family; lead `dfs_test_events_utilisation_report_sum`, then
`dfs_test_events_utilisation_report`, `dfs_test_events_service_update_industry`, `dfs_test_events_service_requirement`).
Writer, 2026-10-23.

## Status

- Build `uv run --system-certs --extra build gridflow-build --only neso_data_portal/dfs_test_events_utilisation_report_sum`:
  passes, no errors (the 37-line "Known issues" caveat-grammar warning is global, not this page).
- Detector on `site/hifi/data-sources/neso_data_portal/demand-flexibility-service-test-events.html`: `[]`. Real em dashes: 0.
  Banned-word grep: only "live" in "live events are a separate package" and the related note on the live-events page
  (NESO's event type, not live framing).
- Mirror: `cp` + `cmp` clean. The note is CRLF on all 559 lines; the vault diff is 134 insertions, 0 deletions (page
  block only; body unchanged).
- Screenshots at 1440, 1024, 768 and 390 (390 through a 390 px iframe), light only: nothing clipped or overlapping
  beyond the known template items below. Server on 9873 started with a recorded PID (9458) and stopped by that PID.
- Files (mine only): canonical note `C:\gridflow-wt\vault-neso-dfs\30-vendors\neso-data-portal\datasets\demand-flexibility-service-test-events.md`,
  its mirror `vault\neso_data_portal\demand-flexibility-service-test-events.md`, and
  `site\hifi\data\{series,samples,notebooks}\neso_data_portal\dfs_test_events_utilisation_report_sum*` (series JSON,
  sample JSON, notebook JSON + `-5.png`). No staged spec or authored override existed for this lead.
- Manifest lead and members match `site/hifi/data/neso_data_portal.json` (family 23, lead first). Nothing to report.

## The answers the launch prompt asked for

1. **What one row is.**
   - Summary (`dfs_test_events_utilisation_report_sum`): one half-hour test window (key `date`, `window_from`), with
     the MW NESO required, D-1 accepted MW and cost, the D0 update of both, then settled volume and cost.
   - Report (`dfs_test_events_utilisation_report`): one bid of one DFS unit in one window (key adds `unit`),
     `Accepted` or `Rejected`, with price, D-1 volume and the D-1 and D0 split by region.
   - Notifications (`dfs_test_events_service_update_industry`): one notice NESO posted to industry, keyed by posting
     `date`, `time_label`, `type`: Anticipated Requirement Notice, Requirement Published, or Test DFS Requirement not
     issued.
   - Requirement (`dfs_test_events_service_requirement`): one window's published MW requirement (held).
   - Units, NESO's dictionary: MW for every volume and regional column, £ for the three cost columns, £/MWh for
     `price`; window and notice times are `HH:MM` labels marked GMT.
   - Test against live, only where NESO says so: the package notes say the dataset covers "the test service (not
     live events)" and point to the separate live-events dataset. The page says only that live events are a separate
     package and never adds or compares them.
2. **Clock.** NESO's dictionary marks `From`/`To` (summary, report) and `From GMT`/`To GMT` (requirement) with comment
   `GMT`; the catalogue gives notice times "around 10:00 GMT" and "around 14:30 GMT". The season **does cross a clock
   change**: 38 of the 40 windows (18 dates, 15 November 2022 to 23 March 2023) are in GMT, where GMT, UK time and UTC
   agree; the two windows of 28 March 2023 (18:00 and 18:30 labels) fall after the clocks went forward on 26 March,
   as do the 27 March notices (10:00 and 14:30 labels, the same labels as every winter notice). The rows cannot tell
   whether those labels are GMT or UK local time. The page keeps labels as text ("GMT in its dictionary"), says in the
   frame caption that 28 March is in British Summer Time, and the `timestamp_utc` guide line says it is 23:00 the day
   before for 28 March (visible in the frame and notebook). The chart uses `time: date`, not `timestamp_utc`, so 28
   March plots on 28 March. The notebook converts `timestamp_utc` and `published_at` from the session zone to UTC.
3. **Captures.** One capture per table, all on 2026-10-08; **no 16 October recaptures** exist in bronze or silver.
   Summary 40 rows, report 739, notifications 40, requirement 40; each bronze CSV has exactly rows + 1 header line
   (41, 740, 41, 41), so nothing is truncated. One `bronze_capture_id` and one `published_at` per table. Keys are
   distinct on every row (summary 40/40, report 739/739). Nothing repeats; `dedup: {"on": [date, window_from],
   order_by: published_at}` is set on the chart and the frame as a guard (distil: 0 duplicates dropped).
4. **Chart.** Line (drawn mostly as dots) of `values` `dfs_required` (requirement), `dfs_procured` (accepted at D-1),
   `settled_volume` (settled), MW, **mean** over each delivery date's windows (two per day; four on 12 December), 15
   November 2022 to 28 March 2023, 19 points per series. All three are MW per window; they are separate lines, never
   stacked or added. The requirement is constant within each day, so its mean is the requirement. Story: settled
   above accepted on the first five test days, below on 12 of the 14 later days, about 1 MW on the last two small
   tests. Held member: "NESO does not say when each window's requirement was first published."
5. **Related.** `neso_data_portal/demand-flexibility` (showcase), `-service` (2023/24), `-service-live-events` (2022/23
   live, "never add them"), plus `elexon/system_prices`.

## Evidence

| Claim on the page | Evidence |
|---|---|
| Four tables, one CSV file each; member request URLs | registry `gridflow/src/gridflow/connectors/neso_data_portal/registry/demand-flexibility-service-test-events.json` (four resources, one per family); bronze sidecars `request_url` (`.../2026/10/08/*.meta.json`) |
| `package_show` request URL | `config/sources.yaml:756` `base_url: "https://api.neso.energy"`; `endpoints.py:49` `CKAN_ACTION_PREFIX = "/api/3/action"`; `client.py:971` `_package_show(family.package)` |
| One `package_show`, whole-file download unless `last_modified` unchanged; dates select nothing | `client.py` `iter_members` docstring (1661-1672) |
| "the window must end within 48 hours" | `client.py` `_assert_window_admissible` (1474-1513): `NesoHistoricalWindowError` when `end` is more than 48 h stale; bronze partition is `end.date()` |
| Commands: `gridflow pipeline ... --last 24h`, one table per call | `cli.py:186,485`: `dataset` is a single argument; two `pipeline` lines (summary, report) fit the three-command limit; the window's end date is the capture's partition, so the transform has bronze |
| Cadence "Not Active"; files last modified March 2023 or July 2026 | catalogue snapshot `20261006T195819Z`, package extras `Update Frequency: Not Active`; resource `last_modified`: requirement 2023-03-27T13:29:56, notifications 2023-03-27T13:28:50, report 2026-07-27T13:58:49, summary 2026-07-27T13:46:55 |
| Test only; live events in a separate dataset | same package notes: "This dataset will contain updates regarding the use of the test service (not live events)", link to `demand-flexibility-service-live-events` |
| History "Test events on 19 days, 15 November 2022 to 28 March 2023" | NESO's whole frozen file (one capture, 40 rows = bronze lines); the chart's x axis shows the 19 dates |
| Key `date`, `window_from`; report adds `unit` | registry `entity_key`; silver distinct keys 40/40 and 739/739 |
| Units MW, £, £/MWh; D0 at 10:00 GMT, D-1 used where no D0 update | field-info `20261008T114228Z/dfs_test_events_utilisation_report_sum.json` (`D0 DFS Procured`: "Where an updated forecast has not been received on D0, the values for the unit submitted at D-1 will be used"); `..._utilisation_report.json` (`Price` `£/MWh`) |
| Window labels GMT in NESO's dictionary | field-info `comment: "GMT"` on `From`/`To` (summary, report) and `From GMT`/`To GMT` (requirement) |
| `timestamp_utc` = 00:00 UK time on `date`; 23:00 the day before for 28 March | registry `temporal: date_sp1` on `date`; silver: 38 rows at 00:00Z, the two 28 March rows at 2023-03-27 23:00Z (frame rows 7-8; notebook cell 3) |
| `published_at` = file last-modified, read as UTC | registry `vintage: ckan_last_modified`; silver summary `published_at` 2026-07-27 13:46:55.144778 UTC = catalogue `last_modified` 2026-07-27T13:46:55.144778 (no zone) |
| `dfs_procured` = report's Accepted bids summed | silver: max abs difference 0.0046 MW over 40 windows |
| Chart key: requirement 25 to 300 MW | committed series `required`: min 25.0 (28 Mar), max 300.0 (12 Dec, 23 Mar) |
| Accepted above requirement on 19 January and 15 March | series: 207.54 vs 150 and 268.33 vs 250; no other day |
| Settled above accepted on the first five days; 1.01 MW or less on 21 and 28 March | series: 15 Nov to 12 Dec settled > accepted (133.39/75.9 ... 199.335/152.445); 21 Dec onwards below except 13 and 21 Feb; 21 Mar 0.725, 28 Mar 1.01 |
| Chart alt peaks | series: accepted max 268.33 (15 Mar), settled max 269.0 (21 Feb) |
| Notebook lead | gridflow_models `research/handles/source.py:401` `query()`; `_get_method_registry`: relation `silver_neso_data_portal_dfs_test_events_utilisation_report_sum_latest`, date column `date`, SQL type DATE, `BETWEEN` both ends; bitemporal exclude `event_time, available_at, vintage_policy, source_run_id, dataset_version, month, year` |
| Notebook outputs | cell 3: first two and last two windows, 28 March `timestamp_utc` 2023-03-27 23:00:00+00:00; cell 4: Accepted 613 bids, 34 units, £3,000 to £3,000/MWh; Rejected 126 bids, 11 units, £3,000 to £6,000/MWh |
| Plot alt | silver: accepted 7.0 to 270.69 MW, settled 0.72 to 269.2; 17 of 40 windows settled > accepted; 15 Nov windows 74.31/125.36 and 77.49/141.42 (also in the frame) |

## Body corrections

None. Re-derived and held: 739 report rows, 613 Accepted and 126 Rejected; 40 windows on 19 dates; D0 regional nulls
126 each (`d0_other` 136, `d0_total` 128); 18 zero `dfs_volume` and `total`; 4 negative `other` and `d0_other`; regions
sum to `total` on 714 rows, `total` = `dfs_volume` on 727; summary D-1 MW matches all 40 windows and D-1 cost 38 (17
January's two windows £4.50 off); 20 notice posting dates; 11 padded `status` cells and 1 padded `type`; 38 of 40
requirement windows on or before the file's stamp.

## Unverified

- Whether NESO's "GMT" labels on 28 March 2023 (and the 27 March notice times) are GMT or UK local time; no row can
  tell. The page states the date is in British Summer Time and keeps the labels as text.
- D0 summary reconciliation: I get D0 MW matching in 32 windows, the note says 31 (my fallback: report `d0_total`,
  else `dfs_volume`, tolerance 0.01 MW). A method difference, not corrected; the page states no D0 count.
- The note body's claim that NESO guidance describes tests as real deliveries (cites gridflow's K-DFS-FACTS, not a
  NESO text in the snapshot). The page does not repeat it; it only shows that test windows were settled.

## Open questions

- None blocking. The requirement table stays held per the ledger.

## For the checker

- The 28 March clock wording (frame caption, `timestamp_utc` line) and the chart's `time: date`.
- The chart uses `aggregation: mean` over each day's windows of MW columns (caption says so); the requirement is
  constant within a day.
- Consecutive test days are joined by steep segments (30 to 31 January, 14 to 15 March, 30 November to 1 December):
  the renderer joins consecutive dates; the values are true.

## Template problems (seat items)

- Known: family pages do not print `raw_feed.requests` (the `package_show` line is set, as on approved pages, and not
  shown).
- Known: the folded frame at 390 shows only the two key columns until unfolded; the notebook tab label truncates at 390.
- New, minor: a dot-style line chart joins any two consecutive dates, so a 250 MW day followed by a 100 MW day draws a
  steep segment that reads like an intra-day ramp. A per-series "points only" option would avoid it.
- Observation for the seat (not my file): the sibling live-events block writes `dedup: {on: [...]}` unquoted;
  PyYAML reads `on` as `True` (`yaml.safe_load('d: {on: [a], order_by: p}')` gives `{True: [...]}`), and
  `chart_spec.py:298` requires the key `"on"`. Their chart is a bar without `dedup` in the chart, so it may only
  affect the frame's `record.select`.

## Defects

- **NESO data, `demand-flexibility-service-test-events` clock labels:** the dictionary marks window starts and ends
  (`From`, `To`, `From GMT`, `To GMT`) and the catalogue marks notice times as GMT, but the 28 March 2023 windows and
  the 27 March 2023 notices fall in British Summer Time; NESO does not say whether those labels are GMT or UK local
  time. Two summary windows, their report bids and two notices affected. Non-holding; page keeps labels as text.
- **NESO data, `dfs_test_events_utilisation_report_sum` 17 January 2023:** D-1 `bids_accepted_total_cost` is £4.50
  below the report's Accepted bids x price x 0.5 h in both windows (83,835 vs 83,839.5; 85,335 vs 85,339.5). Already
  in the note as SUMMARY-RECONCILIATION; nothing new.
- No new gridflow defect found.
