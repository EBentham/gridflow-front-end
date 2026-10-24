# FES natural gas demand definitions (ED4): writer's report (round 1)

Page `neso_data_portal/fes-natural-gas-demand-definitions-ed4`, a one-table page. Its lead and only member is
`fes_ed4_gas_demand_defs`. Build `--only neso_data_portal/fes_ed4_gas_demand_defs`: no errors (the one warning, 37
gotcha lines, is global). Detector `[]`. 0 em dashes in the built page. The mirror is identical (`cmp`). The note keeps
CRLF on all 419 lines. The vault diff is the `page:` block, `updated:` and one body sentence (85 lines added, 2
removed).

## Chart choice: `type: none`

- Reason on the spec: "Ten or eleven text definitions per edition and no measure; a count of items would only restate
  the rows."
- The only number in the table is `item_no`, an identifier. NESO's dictionary calls it "Unique Key".
- The honest summary would be a count bar: 10, 10, 11, 11 items per edition. Four near-equal bars restate what the
  frame, the facts line ("items 1 to 10, plus 11 from 2025") and notebook cell 1 already show.
- The chart spec has no distinct-count aggregation, so "wordings per item" cannot be charted either. Even if it could,
  it would count full stops as changes.
- Precedents: tRESP and national demand BM units both use `type: none` on text-only reference lists. The building-block
  page kept a count bar because its 49 to 64 step carries the reason to join on edition. Here the one step (item 11
  from 2025) is better shown as rows.
- With `type: none` the page has no chart section; there is no `chart_view`.
- If the seat prefers a bar, the spec is `type: bar, group: edition, aggregation: count, sort: label`. Add `dedup` on
  `[resource_id, item_no]` as a guard.

## Captures and editions (every capture checked)

| Edition | Resource | File | Bronze capture (2026-10-08 UTC) | Rows | `published_at` (CKAN `last_modified`) |
|---|---|---|---|---:|---|
| 2023 | `60a8299f-...` | `fes2023_ed4_v001.csv` | 10:54:18, 1,515 bytes | 10 | 2023-07-10 03:31:27 |
| 2024 | `a014dfba-...` | `fes2024_ed4_v001.csv` (UTF-8 BOM) | 10:54:21, 1,570 bytes | 10 | 2024-07-15 06:40:17 |
| 2025 | `74485527-...` | `fes2025_ed4_v006.csv` | 10:54:24, 2,062 bytes | 11 | 2025-12-10 16:56:34 |
| 2026 | `b5ae9932-...` | `10yo2026_ed4_v001.csv` | 10:54:27, 2,488 bytes | 11 | 2026-09-16 14:59:52 |

- There is one bronze capture per resource, all under `2026/10/08`. No other bronze folder holds these resource ids
  (grep of every NESO sidecar). There are four silver files, one per run.
- `bronze_capture_id` has 4 distinct values across 42 rows. There are 0 duplicate `(resource_id, edition, item_no)`
  tuples and 0 nulls in any column.
- `event_time` equals `timestamp_utc`, and `available_at` equals `published_at`, on every row. `dataset_version` is
  `1+e1` on every row.
- **`dedup`:** `{"on": [resource_id, item_no], order_by: capture_written_at}` on the frame. This is a guard only:
  there is one capture per resource, so nothing is dropped.
- **Dating:** each edition is dated to NESO's file through `published_at`, shown in the frame and the column guide. The
  2025 resource was created 2025-07-14 and last modified 2025-12-10. It is at `v006`, so NESO re-uploaded it; the note
  body already says so.

## What one row is

- One numbered item of NESO's natural gas demand codebook in one edition's file. It has three vendor columns:
  - `item_no` (NESO: "Unique Key");
  - `description` (NESO: "Description of data item in ED3");
  - `definition` (NESO: "More in-depth breakdown of description").
- The dictionary is from the field info on the 2026 resource, captured 8 October 2026.
- Edition comes from the file name (`edition_by_filename`).
- Key: `resource_id, edition, item_no`.
- The row has no event time: `timestamp_utc` is the capture time.

## The frame: items 2, 3, 5 and 11, 2025 and 2026

- **Item 11** (total): the 2025 formula is `= 1+2+3+4+5+6+8`; the 2026 formula is `= 1+2+4+5+6+8`.
- **Item 3** (transport): the 2026 text adds that it "is not be added" (NESO's typo) to other components, because
  networked CNG sits in commercial.
- **Item 2** (commercial): the 2026 text adds that commercial "includes networked CNG used for transport".
- **Item 5** (NTS gas for generation): the 2026 text adds the network-constraint gas and says it is "not directly
  comparable".
- These are the definition changes silver shows between the two latest editions. Caption: "Items 2, 3, 5 and 11,
  2025 and 2026: the 2026 total omits item 3."
- **Known limit:** `definition` is up to about 490 characters. The frame never wraps (`white-space: nowrap`) and sizes
  columns from the full text, so `definition` and everything after it folds behind `…` at every width. Unfolded, it
  scrolls inside the frame.
- Notebook cell 3 therefore prints the 2026 items 3 and 5 whole (the text output wraps). Cell 2 flags which item texts
  differ from 2025 to 2026: items 2, 3, 5, 8, 10 and 11 do; items 1, 4, 6, 7 and 9 do not.

## Evidence table

| Claim | Evidence |
|---|---|
| 4 CSVs, editions 2023 to 2026, 42 rows (10/10/11/11) | silver `group_by(edition)`; bronze `csv.reader` counts; notebook cell 1 |
| Item 11 formulas `= 1+2+3+4+5+6+8` (2025), `= 1+2+4+5+6+8` (2026) | silver `definition`; sample rows |
| 2026 item 2 adds "includes networked CNG used for transport" | silver, 2026 item 2; the 2025 text lacks it |
| Items 7 and 8 descriptions end in a space | silver `description` repr, all editions |
| "Unique Key", "Description of data item in ED3", "More in-depth breakdown of description" | `gridflow/.planning/research/neso-snapshots/field-info/20261008T114228Z/fes_ed4_gas_demand_defs.json` |
| Package notes quote "an agreed set of data tables", natural gas and residential heat demand | catalogue snapshot `20261006T195819Z`, package `notes` |
| 2026 file is a Ten-Year Outlook output | the same snapshot, the 2026 resource description ("One of the Ten-Year Outlook outputs ...") |
| Package created 7 July 2023 | snapshot `metadata_created` 2023-07-07T15:14:21 |
| Ad hoc | snapshot extras "Update frequency: Ad hoc"; registry `refresh: adhoc` |
| Request URLs | each file URL equals its bronze sidecar `request_url`; `package_show?id=` from `client.py:981` |
| Downloads skipped when `last_modified` is unchanged | `client.py:1752-1767` |
| `--last 24h`; the window is not a selector | `client.py:1583-1589`; `config/sources.yaml:930` (`fes_ed4_gas_demand_defs` key) |
| Edition from the file name | registry `edition_by_filename` |
| `published_at` = CKAN `last_modified`, read as UTC | registry `vintage: ckan_last_modified`; sidecar `ckan_last_modified`; silver tz UTC |
| `query()` filters on the capture time, so `data.sql()` | batch "Checked facts" (remediation 20at) |
| Notebook ran clean | `run_notebooks.py`: 5 cells, 0 errors, 0 images |
| Note body bronze facts (bytes, BOM, commas 6/6/2/4, one newline in 2025 item 10) | `csv.reader` over the four bronze bodies: all match |

## Body corrections (canonical note)

- `updated:` changed from 2026-10-15 to 2026-10-24.
- **"What changed between editions", the item 3 bullet:** one sentence added. The 2026 item 2 definition says
  commercial demand "includes networked CNG used for transport"; the 2025 text does not. Evidence: silver `definition`
  for item 2 in 2025 and 2026.
- Every other body claim I re-checked is true: counts, bytes, BOM, embedded newline, commas, `published_at` values,
  capture times, the item 8 label change, the item 10 gas-year text, and the item 5 "FES 2026" against "FES25"
  inconsistency.

## Unverified

- Whether NESO revises an edition in place (the 2025 file is `v006`). The page does not claim either way.
- Which earlier forecast the 2026 item 5 text means ("FES 2026 10 Year Forecast" against "FES25"). This stays in the
  note body as a `TODO: verify` and is not on the page.

## Template problems (seat items)

- The frame cannot wrap long text cells. A definitions table's main column folds at every width, and unfolded it
  scrolls inside the frame. The notebook prints the texts whole as a workaround.
- `raw_feed.requests` allows at most four, but the page has `package_show` plus four files. Shown: `package_show`,
  2023, 2025 and 2026; the note says so. The 2024 file URL is in the note body's resource table.
- The site has no dark theme. Light screenshots only.

## Screenshots

- Static server on 9944, started with its PID recorded (61007) and stopped by that PID (the port then refused
  connections).
- Headless Chrome, `timeout 60`, with `--timeout=15000 --virtual-time-budget=5000`. Full page at 1440, 1024 and 768;
  390 through a 390 px iframe, cut into tiles.
- Nothing is clipped or overlapping:
  - hero chips and the key chip wrap;
  - the request wells break the long URLs;
  - the folded frame shows `item_no`, `edition` and `description` at 1440, and `item_no` and `edition` at 768 and 390;
  - related slugs wrap.
- Files are in
  `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\ed4-writer\`
  (`p1440.png`, `p1024.png`, `p768.png`, `c390.png`, `t390-0..3.png`).

## Files written

- Canonical note:
  `C:\gridflow-wt\vault-neso-fes\30-vendors\neso-data-portal\datasets\fes-natural-gas-demand-definitions-ed4.md`.
- Mirror: `C:\gridflow-wt\fe-neso-fes\vault\neso_data_portal\fes-natural-gas-demand-definitions-ed4.md`.
- Artefacts:
  - `C:\gridflow-wt\fe-neso-fes\site\hifi\data\samples\neso_data_portal\fes_ed4_gas_demand_defs.json`;
  - `C:\gridflow-wt\fe-neso-fes\site\hifi\data\notebooks\neso_data_portal\fes_ed4_gas_demand_defs.json`;
  - no series, since the chart is `type: none`.
- Built page: `C:\gridflow-wt\fe-neso-fes\site\hifi\data-sources\neso_data_portal\fes-natural-gas-demand-definitions-ed4.html`.

## What the checker should look at hardest

1. **The ED3 boundary.** Nothing on the page describes ED3's rows or values. The related note and `description` line
   only name ED3 as the table these items define, which is NESO's own dictionary wording. The note-body label match
   (measured on 2025 and 2026) is not on the page.
2. **`type: none` against a count bar.** Is the reason sound, or should the 10/10/11/11 bar stand (the building-block
   precedent)?
3. **The frame caption** "the 2026 total omits item 3", against the item 11 rows. Also whether "omits" could read as
   "transport is excluded". The 2026 item 2 text says networked transport sits in commercial; the frame shows it once
   unfolded.
4. **The `what_it_is` quote and its dating.** The package notes still say "natural gas and residential heat demand",
   while the 2025 and 2026 resource descriptions say natural gas only. The page quotes the package notes and says each
   edition defines gas items.
5. **The folded frame.** `definition` is never visible until unfolded. This is the template limit above. Check that
   notebook cell 3 is enough.

## Defects (pasteable)

- **Front-end template: the sample frame cannot show long text columns.**
  - Where: `build.py` `_frame_view` sizes each column from its longest cell; `dataset.css` `.pl td` is
    `white-space: nowrap`.
  - What: a definitions table's main column (`fes_ed4_gas_demand_defs.definition`, up to about 490 characters) folds
    behind `…` at every width.
  - Action: a front-end template follow-up (cap or wrap long string cells). There is no gridflow change.
- **NESO FES ED4 2026 item 5: the text names two different earlier forecasts.**
  - Where: resource `b5ae9932-2ce9-42f0-a820-15a13f0eedd0` (`10yo2026_ed4_v001.csv`, last modified 2026-09-16).
  - What: the item 5 definition calls the excluded forecast "FES 2026 10 Year Forecast" in one sentence and "FES25 10
    Year Forecast" in the next.
  - Effect: comparability is stated but its baseline is ambiguous.
  - Action: vendor quirk, already in the vault note as `TODO: verify`. There is no gridflow change.
- No gridflow code defect found.
