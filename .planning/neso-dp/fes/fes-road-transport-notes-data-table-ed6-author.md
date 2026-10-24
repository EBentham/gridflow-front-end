# FES road transport notes (ED6): writer's report (round 1)

Page `neso_data_portal/fes-road-transport-notes-data-table-ed6`. This is a one-table page with key
`fes_ed6_road_transport_notes`.

- **Build:** `--only neso_data_portal/fes_ed6_road_transport_notes` ran with no errors. The one warning (37 gotcha lines dropped) is global.
- **Detector:** `[]`. The built page has 0 em dashes.
- **Mirror:** identical to the canonical note (`cmp`).
- **Line endings:** the note is LF throughout (0 CRLF before and after), and I kept LF.
- **Vault diff:** the `page:` block, `updated:` and two body additions (99 lines added, 2 removed).

## Chart choice: `type: none`

Reason on the page: "The notes are text with no measure; the rows below show how NESO's wording changes between editions."

- **Why not a count of notes per edition:** it would draw four near-equal bars (27, 27, 26, 26). The one structural change is in 2025, where `Peak/Annual/Minimum` goes from 3 notes to 2. A count shows that as 3 to 2, which hides what actually happened: `# Vehicles` and `Reference data` go, and `Annual` arrives. The frame shows this in NESO's own words, and notebook cell 2 lists which values appear in which editions.
- **No series file:** none is committed, and the build reports 0 template charts for this page.
- **Precedent:** this follows tRESP (`type: none` for its reference lists). The building-block page kept a count bar because its 49 to 64 to 66 step means something.
- **Consistency with ED4:** the ED4 note had no `page:` block when I wrote this, so I could not align with it. If ED4 uses a count bar, the seat should pick one rule for both codebooks. ED4's counts (10, 10, 11, 11) are just as flat.

## Captures and editions (every capture checked)

| Edition | Resource | File | Captures | Silver rows | `published_at` (CKAN `last_modified`) | Captured (UTC) |
|---|---|---|---|---:|---|---|
| 2023 | `30012023-…` | `fes2023_ed6_v001.csv` | 1 | 27 | 2023-07-10 03:26:39 | 2026-10-08 10:54:43 |
| 2024 | `7fe93ddc-…` | `fes2024_ed6_v001.csv` | 1 | 27 | 2024-07-15 06:41:16 | 2026-10-08 10:54:46 |
| 2025 | `43add83b-…` | `fes2025_ed6_v006.csv` | 1 | 26 | 2025-12-10 17:02:44 | 2026-10-08 10:54:48 |
| 2026 | `06601add-…` | `10yo2026_ed6_v001.csv` | 1 | 26 | 2026-09-16 15:01:14 | 2026-10-08 10:54:51 |

- **Bronze:** only `2026/10/08` exists, with one CSV and one sidecar per resource. Each `bronze_capture_id` is unique within its edition.
- **Silver:** 4 parquet files, 106 rows, zero nulls in any column, and zero duplicate entity keys.
- **`dedup`:** on the frame, `{"on": [resource_id, edition, column_name, category], order_by: capture_written_at}`. It is a guard only and drops nothing today.
- **2026 edition:** NESO's resource description says "One of the Ten-Year Outlook outputs" (catalogue snapshot `20261006T195819Z`). The page calls that file "the 2026 Ten-Year Outlook".

## What one row is

One row is one NESO note on one value of one ED5 column, in one edition's file.

- `column_name` is the ED5 column: `Data Item`, `Fuel` or `Peak/Annual/Minimum`.
- `category` is a value in that column, such as `V2G Maximum Capacity`.
- `description` is NESO's note on it. 21 notes per edition contain a formula in square brackets.
- Key: `resource_id, edition, column_name, category`.
- There is no measure, unit or year. `timestamp_utc` is the capture time.

## Page content

- **Frame:** eight rows, the two V2G notes plus `Peak`, `# Vehicles` and `Annual`, in FES 2024 and 2025.
  - The caption reads "V2G and period notes, FES 2024 and 2025: 2025 adds `Annual`, drops `# Vehicles`."
  - `description` folds at every width, because its cells run to about 300 characters. I moved it after `published_at` and `resource_id` so that the dating columns stay visible at 1440.
  - The `description` guide line carries the V2G change: "the 2025 V2G notes add HGVs and buses parked at the depot".
- **Notebook:** `data.sql()` on `_latest`, which keeps the newest capture per resource, so all four editions (`latest_partition: resource_id`). It runs 5 cells with 0 errors and 0 images.
  - Cell 1: notes per edition by column (22/2/3, 22/2/3, 22/2/2, 22/2/2).
  - Cell 2: the values that appear in only some editions: `# Vehicles` and `Reference data` in 2023 and 2024, `Annual` in 2025 and 2026.
  - Cell 3: the hydrogen TWh note by edition. 2026 adds "Report in the higher heating value of hydrogen".
- **Quotes:** NESO is quoted once in `what_it_is` ("a file supporting", from the resource descriptions). Every other NESO text appears as silver rows, each dated by edition and `published_at`.
- **ED5:** it is linked as related ("The road transport table whose columns and values these notes explain"). None of its rows or values is described anywhere on the page.
- **Related:** ED5, ED1 (the 2023 and 2024 `Reference data` note says that data "is not used in the calculation of Peak/Annual/Minimum in ED1"), ED4, and building blocks. All four slugs are in the page set.

## Evidence table

| Claim | Evidence |
|---|---|
| Four CSVs, one per edition, editions from file names | registry `edition_by_filename`; sidecars `resource_filename` |
| `published_at` is CKAN `last_modified` | registry `vintage: ckan_last_modified`; sidecar `ckan_last_modified` equals silver |
| Package created 7 July 2023 | snapshot `metadata_created` 2023-07-07T15:50:38 |
| "a file supporting" | resource descriptions 2023 to 2026 (snapshot) |
| Requests | each URL equals a bronze sidecar `request_url` |
| `package_show`, then download whole unless `last_modified` unchanged; `--last 24h` | `client.py:1583-1589` (window is not a selector), `client.py:1752-1765` (skip) |
| `# Vehicles - Hydrogen` filed under `Fuel` | silver, all four editions; bronze line 8 (2023) and line 14 (2024 to 2026) start `Fuel,# Vehicles - Hydrogen` |
| 2025 V2G scope widened; `Peak` reworded; `Annual` new | silver `description` by edition (frame rows) |
| 2026 hydrogen higher heating value | silver; bronze 2026 line 26 |
| Peak is 5pm to 6pm | NESO `Peak` note text, every edition |
| Trailing space kept | `Electric Vehicle Unmanaged Peak Demand ` in every edition; the registry has no trim |

## Body corrections (canonical note)

- `updated:` changed from 2026-10-14 to 2026-10-24.
- **"What changed between editions":** added the wording revisions beyond line breaks, read from the captures and quoted:
  - 2024: the ICE note drops the mild-hybrid sentence, and the motorbikes note changes its e-bicycle wording.
  - 2025: the V2G scope widens, `Peak` is reworded, and `Annual` is new.
  - 2026: the hydrogen note adds the higher heating value, the EV peak note adds "does not consider any use of vehicle-to-grid", and the five `# ... - All` notes switch from the DfT PDF to a gov.uk link.
- **New bullet:** one `Fuel` row (`# Vehicles - Hydrogen`) is a vehicle count, as NESO labels it in every file. This probably explains the note's "1 of the 2 `Fuel` rows matches an ED5 fuel label", but I did not check it against ED5, which is held.
- Every other body count I re-checked is true:
  - rows per edition, and 9 blank rows dropped in 2023 (37 bronze lines including the header);
  - 19 newline cells in each of 2024 to 2026;
  - descriptions of 43 to 486 characters;
  - labels by column.

## Unverified

- Whether the 2025 `Annual` note replaces the earlier `# Vehicles` note. The page says only that 2025 adds one and drops the other. The note keeps its `TODO: verify`.
- Whether NESO edits a file in place without bumping `last_modified`.

## Template problems (seat items)

- **Long text cells:** frame width is computed from the full string (`build.py` `width()`), so a long text column folds at every width and pulls every later column with it. Unfolded, the frame scrolls sideways inside its own box, so nothing on the page overflows. Notes and definitions tables (this page, ED4) would need wrapping or truncation of long string cells to show the text folded.
- **At 390:** the folded frame shows only `column_name` (the known fold follow-up).

## Screenshots

- Server on 9945, started with PID 61000 recorded and stopped by that PID.
- Headless Chrome (`timeout 60`) at 1440, 1024 and 768; 390 through a 390 px iframe. The unfolded frame was checked in the browser pane.
- Nothing is clipped or overlapping.
- Files: `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\ed6-writer\` (`q1440.png`, `q1440-frame.png`, `q1024.png`, `q768.png`, `q390-a.png`, `q390-b.png`).

## Files written

- Canonical note: `C:\gridflow-wt\vault-neso-fes\30-vendors\neso-data-portal\datasets\fes-road-transport-notes-data-table-ed6.md`.
- Mirror: `C:\gridflow-wt\fe-neso-fes\vault\neso_data_portal\fes-road-transport-notes-data-table-ed6.md`.
- Artefacts: `C:\gridflow-wt\fe-neso-fes\site\hifi\data\samples\neso_data_portal\fes_ed6_road_transport_notes.json` and `...\notebooks\neso_data_portal\fes_ed6_road_transport_notes.json`. There is no series file (`type: none`).
- Built page: `C:\gridflow-wt\fe-neso-fes\site\hifi\data-sources\neso_data_portal\fes-road-transport-notes-data-table-ed6.html`.

## What the checker should look at hardest

1. **`type: none` against a count bar:** is the reason honest, and is it consistent with whatever ED4 chose?
2. **Frame caption and `description` guide line:** check them against the eight rows. The V2G text is behind the fold, so unfold the frame.
3. **ED5 boundary:** nothing on the page should describe ED5's rows (the related note, `how_used`, `column_name` guide line).
4. **Body additions:** check the revision quotes against silver by edition. The "beyond line breaks and full stops" filter is my reading; minor wording edits, such as "including" changing to "includes" in 2024, are left out.
5. **`how_used[1]`:** "peak (5pm to 6pm)" is NESO's note text. 2025 widens `Peak` to "demand or available capacity".

## Defects (pasteable)

- **NESO FES road transport notes (ED6): hydrogen vehicle count filed under `Fuel`.**
  - Where: all four files. The resources are 2023 `30012023-6c0b-4da5-bd77-4f2b244a950d`, 2024 `7fe93ddc-…`, 2025 `43add83b-…` and 2026 `06601add-…`.
  - What: the `# Vehicles - Hydrogen` row has `Column` = `Fuel`, but it is a vehicle-count item with a formula like the `Data Item` counts.
  - Effect: joining on `column_name` puts it against ED5's `fuel` column, where it will not match.
  - Action: vendor quirk, kept as received. The note body states it, and so does the page's column guide. No gridflow change.
- **Front-end template: long string cells always fold.** The frame width uses the full string length, so a notes column folds at every width (seat item).
- No gridflow code defect found.
