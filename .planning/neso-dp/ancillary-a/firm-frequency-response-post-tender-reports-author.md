# FFR post-tender reports (`firm-frequency-response-post-tender-reports`): writer report

Writer, 2026-10-18. Lead `ffr_post_tender_reports_csv_ext`; members `_workbook` (held), `_csv`, `_ext`. Port 9950 (stopped).

## Status

- `gridflow-build --only neso_data_portal/ffr_post_tender_reports_csv_ext`: succeeds (only the global "3 line(s) in Known issues" warning).
- Detector `[]`; 0 em dashes in the page; mirror `cmp` equal; note CRLF 728 of 728 lines.
- Artefacts: `site/hifi/data/series/neso_data_portal/ffr_post_tender_reports_csv_ext.json` (spec_origin vault, 26 bars),
  `samples/.../ffr_post_tender_reports_csv_ext.json` (gridflow-sample, 8 rows, 52 columns),
  `notebooks/.../ffr_post_tender_reports_csv_ext.json` + `-5.png` (run_notebooks.py, 5 cells, no errors).
- No staged chart spec or authored override existed for this dataset.
- Screenshots (headless Chrome, full page) at 1440, 1024, 768, and 390 through a 390 px iframe: hero, chips, scenery, chart and labels,
  raw-feed wells, frame and guide, notebook, related all visible. Built-in pane: frame unfolded and notebook open, document scroll
  width equals the viewport, no element outside a scroll box. The 390 notebook tab label clips (known template item).

## Chart

Bar, count of rows with `status` in [`Accepted`, `Accepted `] per report file (`group: resource_id`, mapped to "TR139 Jul 2021" and so on
from the registry resource names), dedup on `(resource_id, tender_ref)`, sorted by label. No time window: the table has no parsed date
(`temporal: none`; `start_date` and `end_date` are raw strings). Values: 70, 70, 70, 140, 155, 162, 132, 131, 157, 169, 164, 165, 171, 167,
161, 155, 125, 103, 36, 35, 47, 36, 37, 18, 23, 17 (sum 2,716 = provenance rows_used; 0 duplicates dropped). Reproduced independently in
Polars (trimmed status grouped by tender prefix: identical, since tender 162.198, the only cross-file repeat, is Rejected).

## Evidence

| Claim | Evidence |
|---|---|
| 89 files in the package | registry `firm-frequency-response-post-tender-reports.json` resources = 89; catalogue snapshot 20261006T195819Z lists 89 |
| `csv` and `ext` have no table of their own; their files feed `csv_ext` | registry: TR144 (family `_csv`) and TR142, TR143 (family `_ext`) dispositioned `SILVER` key `ffr_post_tender_reports_csv_ext`; `csv_ext` record `siblings: [_csv, _ext]`; `silver/neso_data_portal/generic.py:298` scans `(self.dataset, *record.siblings)` bronze dirs; `_csv` and `_ext` carry no `record`; gridflow_models has no relation for `_csv`; silver `bronze_capture_id` of TR144 rows is under `bronze/neso_data_portal/ffr_post_tender_reports_csv/` |
| Commands: ingest `_csv`, ingest `_ext`, then `pipeline _csv_ext` | each family owns its resources and bronze dir; CLI takes one dataset per call (`cli.py:186`); the build allows at most 3 commands; the window must end recently (`_assert_window_admissible`, 48 h) |
| Files downloaded again only when `last_modified` changes | `client.py` `iter_members`: an upload member is `unchanged` when its newest capture carries the live `last_modified` |
| Request URLs | bronze sidecar `request_url` of each listed resource (TR139, TR166, TR144, TR142, TR143 CSVs; TR108, both TR127 editions, TR166 workbooks) |
| "A report after each monthly tender"; reason codes in FFR market information reports | NESO package notes, catalogue snapshot 20261006T195819Z |
| "Not Active" | catalogue extras `Update Frequency: Not Active` |
| History TR108 (December 2018) to TR166 (October 2023) | resource names `Post Tender Report - TR108 Dec-18` to `Post Tender Report TR166 October 2023 ...` |
| Key `(resource_id, tender_ref)` | record `entity_key`; 0 duplicate keys in silver |
| Round = first three digits of `tender_ref` | NESO field info, `Tender Ref` description |
| `timestamp_utc` is capture time | record `temporal: none`; silver `timestamp_utc == capture_written_at` and `event_time == timestamp_utc` on all 5,457 rows |
| `published_at` = NESO last-modified | record `vintage: ckan_last_modified`; `available_at == published_at` on every row |
| `query()` filters on capture time, hence `data.sql` | gridflow_models `_DATE_COLUMN_BY_DATASET["ffr_post_tender_reports_csv_ext"] == "timestamp_utc"`; relation `silver_neso_data_portal_ffr_post_tender_reports_csv_ext_latest` |
| Units (£/h, £/window, MW, hours; Saturday unit blank; Sunday unit `£`, text hours) | field info `20261008T114228Z/ffr_post_tender_reports_csv_ext.json` |
| Window labels: no zone stated; EFA block times asked | field info comment "Has to be a time consistent with EFA blocks"; no zone given |
| `44562` = 1 January 2022, `44592` = 31 January 2022 | spreadsheet 1900 serial arithmetic; matches `tendered_period` `01.01.22 - 31.01.22` on the same rows |
| One TR165 row has `Accepted ` | silver: `165.012` status length 9; counts 2,715 `Accepted`, 1 `Accepted `, 2,741 `Rejected` |
| `post_code` null for TR139 | record epoch 2 (TR139) has no `Post code` column |
| TR147: a fee with a thousands comma; TR154: ten rows without a tender number | registry HOLD reasons (`1,366.61`; 10 nonblank rows with no Tender Ref) |
| Workbook held line: TR127 and TR136 have two editions, no precedence from NESO | ledger AS-5c row; workbook silver: TR127 175 refs and TR136 132 refs in both editions, 9 rows differ in `status` or `rejection_codes` in each pair; published 2020-07-16 and 2020-07-30, 2021-04-20 and 2021-05-07 |
| Workbooks cover the CSV rounds again from TR139 | silver: all 26 CSV rounds are in the workbook table; workbook has 57 rounds TR108 to TR166 over 59 files |
| Tender 162.198 in three reports | silver: 3 rows in the TR162, TR163, TR164 files, identical business columns; notebook cell 3 output |
| Plot alt numbers | notebook cell 4 data: totals 90 to 97 (TR139 to TR141), peak 310 (TR158), 149 to 209 from TR159; rejected above accepted from TR157 on and not before; accepted 17 in TR166 |
| Truncated-capture risk | not applicable: one capture per resource (2026-10-08) for all 26 resources |

## Body corrections

- Front matter `updated` 2026-10-14 to 2026-10-18.
- Known issues: added "Status spelling" (one `Accepted ` with a trailing space, tender `165.012`, TR165), evidence above. No other body text changed.

## Unverified and open

- Rejection-code meanings: NESO says they are "below the table in the data files", but the TR144 and TR166 CSV tails carry no legend
  (blank rows only). The page says only that NESO points to its FFR market information reports.
- TR123 and TR125 (workbooks) are not named on the page: the whole workbook member is held and its 16-word line carries the
  two-edition reason. Their reasons stay in the vault body.
- Manifest: lead and members are right. Its family title is "FFR post-tender reports"; the page title uses the full name.

## Template problems

- `raw_feed.commands` allows 3 entries; this family needs two sibling ingests plus the owner, so the owner line is `pipeline`.
- `raw_feed.requests` (`package_show`) does not print on a family page (same on the SFFR page).
- Known items: stray header cells on the pivot table output (`["status","Accepted","Rejected","round","",""]`); notebook tab label clips at 390.

## Defects

- **Docs mismatch:** gridflow `docs/neso_data_portal/eligibility.md` and the note's body call `ffr_post_tender_reports_workbook` eligible,
  while the front-end ledger holds it for the page on the unsettled TR127/TR136 supersession. Not a data defect; no change made.
- **Vendor:** NESO's package text says rejection-code legends are "below the table in the data files"; the CSVs checked carry none.
- **Vendor:** tender `165.012` (TR165 CSV) has `status` `Accepted ` with a trailing space; a filter on `== "Accepted"` misses it.

## Nits fixed (review 1, APPROVE with 4 nits)

1. `record.fields.post_code`: now "Postcode's first four digits (NESO), assets 1 MW and over; none in TR139" (NESO field info: "1st 4 digits ... Only applies to assets 1MW or greater").
2. `family.members[1].differs` (workbook): now "Excel reports TR108 to TR166; from TR139 they repeat CSV rounds: never add both".
3. `family.members[0].differs`: now "One CSV per monthly round, TR139 to TR166 except TR147 and TR154"; `raw_feed.note` "one per tender" changed to "one per monthly round".
4. `record.fields.frame_duration_sun_bh`: now "Hours on Sundays and bank holidays (NESO's comment); its unit field says £".

All within budgets. Mirror `cmp` equal (CRLF 728 of 728); `gridflow-build --only neso_data_portal/ffr_post_tender_reports_csv_ext` succeeds; detector `[]`; 0 em dashes on the page. No artefact change needed (words only; series, sample and notebook digests unchanged).
