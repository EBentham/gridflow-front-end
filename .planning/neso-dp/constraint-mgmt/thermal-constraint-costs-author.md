# Thermal constraint costs: writer report

Page `thermal-constraint-costs` (members `thermal_constraint_costs` lead, `thermal_constraint_costs_xlsx`). The manifest's
lead and members are right.

Files: canonical note `C:\gridflow-wt\vault-neso-cm\30-vendors\neso-data-portal\datasets\thermal-constraint-costs.md`
(CRLF kept, 532 CRLF lines before the later edits, no LF-only lines), mirrored to
`C:\gridflow-wt\fe-neso-cm\vault\neso_data_portal\thermal-constraint-costs.md` (`cmp` clean after every edit). Artefacts
`site\hifi\data\series\neso_data_portal\thermal_constraint_costs.json` (`spec_origin: vault`), `samples\...\thermal_constraint_costs.json`
(`gridflow-sample`), `notebooks\...\thermal_constraint_costs.json` and `thermal_constraint_costs-5.png` (run_notebooks.py).
No staged spec or authored override existed. Build `--only neso_data_portal/thermal_constraint_costs` clean; detector `[]`;
0 em dashes in the page. Screenshots in `.planning\neso-dp\constraint-mgmt\thermal-shots\` (1440, 1024, 768 full page;
390 through a 390 px iframe). The site has no dark theme (no `prefers-color-scheme` rule in `theme.css`, `tokens.css` or
`site.js`), so light only. Server on 9901 started from Bash with PID 11908 recorded, stopped by `kill 11908`; port 9670
not touched.

## What one row is

- **CSV member:** one row per `settlement_date`, `constraint_group` and yearly file; six groups every date present. Key
  `resource_id, settlement_date, constraint_group` (registry `thermal-constraint-costs.json`, `entity_key`). NESO:
  "The date the constraint costs belong to"; "The name of the constraint"; "The daily spend in GBP for the constraint.
  This is an integer (rounded)" (field-info snapshot `20261008T114228Z/thermal_constraint_costs.json`).
- **Workbook member:** the same three columns from the `Data` sheet of the 2019-20 and 2020-21 workbooks (registry
  `xlsx: {header_row: 1, columns: A:C}`), plus `child_id` and `child_crc32`.
- **Yearly resources:** five CSVs read (2022-23 2,190; 2023-24 2,196; 2024-25 2,190; 2025-26 2,184; 2026-27 1,104 =
  9,864) and two workbooks (1,464 + 2,190 = 3,654), matching the ledger row exactly.
- **Held 2021-22 resource (ledger: HOLD):** its costs are written with thousands separators (360 cells, for example
  `"2,150,551"`), which the strict whole-number reading refuses. Page line: the CSV member's `differs` says "2021-22 is
  not read: its costs carry thousands separators"; its file is listed in the member's requests because the connector
  still downloads it.
- **Overlap:** none. CSV years 2022-04-01 to 2026-10-01, workbooks 2019-08-01 to 2021-03-31; 0 shared
  `(settlement_date, constraint_group)` across all seven resources (measured). The notebook concatenates the two
  tables' different years and never adds them on the same date.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| £, whole pounds (`daily_cost_gbp` guide, chart unit) | NESO dictionary unit `£`, "integer (rounded)" (field-info snapshot); registry dtype `int64` |
| Negatives kept, unexplained by NESO | 21 negative cells in silver; no vendor definition in the dictionary or catalogue; registry casts nothing to null |
| Date, not instant; day boundary not stated (`settlement_date`, `x_label`) | NESO "The date the constraint costs belong to"; no boundary in any captured NESO text |
| `timestamp_utc` = start of period 1, GB local midnight, in UTC | `casting.py:619-627` (`settlement_period_to_utc(value, 1)` for `date_sp1`); silver 2025-06-26 gives 2025-06-25 23:00 UTC |
| `published_at` = file `last_modified`, read as UTC | registry `vintage: ckan_last_modified`; silver 2026-04-07 10:00:55.940094 UTC equals the sidecar `2026-04-07T10:00:55.940094` |
| "Six of what NESO calls significant constraint boundaries ... do not add up to its total thermal cost" (`what_it_is`) | Catalogue: "outturn system costs for thermal constraints across a number of significant constraint boundaries"; measured: six-group daily sum below `constraint_breakdown` thermal cost, median day 0.07 of it in 2025-26 (equal on 8 of 364 dates) |
| SCOTEX = B6, SSHARN = B7 (key notes) | NESO OTF boundary document 383631, cited in gridflow `K-CON-FACTS.md` section 8 |
| SSE-SP drawn on the Scotland diagram (key note) | NESO resource description: "This file shows the location of the SSE-SP constraint group" (Network Diagram Scotland) |
| Chart numbers (alt, key notes) | committed series: SCOTEX max 11,635,590 on 2025-08-31, 168 days above zero; SSE-SP max 8,841,754 on 2026-01-22, 261 days; SSHARN max 11,571,424 on 2025-06-27, 94 days; 364 points each, 8 April 2025 absent |
| "NESO's file has no 8 April 2025" (caption) | 2025-26 body 2,184 rows = 364 days x 6; bronze and silver agree; approved `constraint-breakdown` caption states the same of its file |
| Plot alt numbers | notebook year table: SSE-SP 389.6 (2022-23), 336.8 (2024-25); SSHARN 245.0 (2020-21); SCOTEX 73.9 to 153.3; 2021-22 NaN |
| `query()` lead | `source.py:401-445`: `_latest` view, `settlement_date` both ends included, ordered by it; lineage `event_time`, `available_at`, `source_run_id`, `dataset_version` dropped; times returned in Europe/London (run: `2025-04-01 00:00:00+01:00`) |
| Commands | `cli.py` ingest/transform/pipeline take `--last`; the workbooks belong to `thermal_constraint_costs_files` (registry `family`), so ingesting `_xlsx` would find no member (`client.py:2268-2272`); `_xlsx` transform reads the `_files` bronze through `siblings` (`generic.py:298`) |
| Requests | exact `request_url` strings from the 2026-10-08 bronze sidecars |
| History fact | catalogue resource names "Thermal Constraint Costs 19-20" to "Data 26-27" |

## Captures, truncation, repeats

| Table | Silver captures | Rows per capture | Repeats |
|---|---|---|---|
| `thermal_constraint_costs` | 5 (one per file, 2026-10-08) | 2,190 / 2,196 / 2,190 / 2,184 / 1,104 | 0 duplicate keys; 0 shared date and group across files |
| `thermal_constraint_costs_xlsx` | 2 (2026-10-08) | 1,464 / 2,190 | 0 |

No capture is truncated: every closed year has six rows per date for every day of its file (365 or 366; 2025-26 364 with
8 April absent in NESO's body; 2019-20 from 1 August as NESO's body starts); 2026-27 runs to 2026-10-01, two days before
its `last_modified`. Captures do not repeat rows today, but a weekly recapture of the open-year file would, so the chart
and frame carry `dedup: {on: [settlement_date, constraint_group], order_by: published_at}` as a guard (distil reported
0 duplicates dropped).

## Chart

Line, `thermal_constraint_costs`, `daily_cost_gbp` in £, one value per settlement date, SCOTEX, SSE-SP and SSHARN,
1 April 2025 to 31 March 2026 (the latest closed year, so no restated dates). Not stacked: NESO does not say the six
groups are additive, and they fall far short of the Constraint Breakdown total, so a stack top would read as a total it
is not. The three shown carry £353.5M of the year's £375.1M across the six (SWALEX is zero all year); the caption names
the three left out. `y_min: -500000` lifts the zero runs off the axis so the 8 April break reads as a gap.

## Body corrections (canonical note)

1. Item 4 of "Seven things": "only one capture per file exists (2026-10-08)" was stale; now says silver holds one per
   file and the 2026-10-16 recapture of the 2026-27 file failed transform (bronze
   `thermal_constraint_costs/2026/10/16/`, sidecar `ckan_last_modified` 2026-10-16T06:39:05.103084).
2. "Downloads and captures": "Every resource was captured once, on 2026-10-08" corrected the same way.
3. "Constraint group codes": the additivity TODO kept; added that the six are not NESO's whole thermal cost (catalogue
   wording plus the measured comparison above).
4. "The open year": resolved the TODO on whether NESO re-uploads the same resource id (it does), with the 2026-10-16
   facts: 1,164 rows to 2026-10-11, 14 cells dated 2026-09-03 to 2026-10-01 restated (for example SCOTEX 2026-09-04
   11,295,859 then 9,085,448), cost header renamed `Daily Cost GBP`, `HeaderEpochError`, citing gridflow
   `refresh-20261016/DRIFT.md`.
5. "Cadence": "captured every resource once" corrected.
6. Front matter `updated:` 2026-10-23.

## Not verified

- What a zero, or a negative, means for NESO; whether groups overlap; the day boundary of `settlement_date`. All stay as
  stated gaps; the page says NESO does not state or explain them.
- The B6 and B7 aliases come from NESO's OTF document as cited in K-CON-FACTS; I did not reopen the document (no live
  calls).

## Open questions for the seat

1. **The first command fails today for a reader.** `gridflow pipeline neso_data_portal thermal_constraint_costs --last 24h`
   downloads NESO's current 2026-27 file, whose header is now `Daily Cost GBP`, and the transform raises
   `HeaderEpochError`. The page does not say so (that would describe local state). If the seat wants a line, a vendor
   fact such as "NESO renamed the cost column in its October 2026 upload" could go in `raw_feed.note`; or hold until the
   new header epoch lands.
2. The CSV member can list four files of six: 2022-23, 2025-26 (chart and rows), 2026-27 (open year) and 2021-22 (held).
   2023-24 and 2024-25 are not printed; the raw feed note says each file is downloaded whole.

## Template problems (seen, not worked around)

- At 390 the folded frame shows only `settlement_date` and `constraint_group`; `daily_cost_gbp` appears on unfolding
  (known follow-up, frame fold).
- At 390 the notebook tab label clips (`thermal_constraint_co...`) (known follow-up).
- Family raw feed does not print `raw_feed.requests` (the `package_show` URL); only member files show. Same on the
  approved BSUoS page.
- Four requests per member (known follow-up).

## Defects

- **gridflow, open-year header drift (thermal_constraint_costs):** NESO's 2026-10-16 upload of resource
  `c730b788-4328-43dc-9f84-27fd3adeda59` (Thermal Constraint Costs Data 26-27, `last_modified`
  2026-10-16T06:39:05.103084) renames `Daily Cost (GBP)` to `Daily Cost GBP`; the frozen record has one header epoch, so
  the capture `raw_20261016T204709Z_c730b788..._0a2a78cf.csv` failed with `HeaderEpochError` and silver is stuck at the
  2026-10-03 vintage (to 2026-10-01). Already listed in `.planning/phases/v0.22-close/refresh-20261016/DRIFT.md`; fix is a
  second header epoch. Note for that unit: the same upload restates 14 earlier cells (2026-09-03 to 2026-10-01), so the
  open-year file is revised in place, not only appended.
- **data, NESO catalogue text:** the 2026-27 resource description reads "for 25-26 financial year" (copy error in NESO's
  catalogue; the file holds 2026-27 dates).
- **data, coverage of the six groups:** the six named groups' daily sum is well below NESO's Constraint Breakdown
  thermal cost (median day 0.94 of it in 2019-20, 0.07 in 2025-26), and above it on a few dates (7 in 2019-20, 3 in
  2020-21, 0 to 2 in later years). Nothing in NESO's text reconciles the two; worth a vendor question before any model
  treats the groups as a breakdown.
