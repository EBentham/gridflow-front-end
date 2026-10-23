# National Demand Balancing Mechanism Units (`national-demand-balancing-mechanism-units`): writer's report

One-table package page, lead key `national_demand_bmus`. The manifest is right: one package, one CSV resource, one
family (registry `national-demand-balancing-mechanism-units.json`); the page set lists the slug with lead
`national_demand_bmus` (`neso_data_portal.json` line 623). Ledger line 23: eligible, nothing held.

Files written:
- Canonical note `C:\gridflow-wt\vault-neso-dem\30-vendors\neso-data-portal\datasets\national-demand-balancing-mechanism-units.md`
  (page block added, three body edits, `updated` bumped to 2026-10-23; 272 lines, all CRLF).
- Mirror `C:\gridflow-wt\fe-neso-dem\vault\neso_data_portal\national-demand-balancing-mechanism-units.md` (`cmp` clean).
- Artefacts: `site\hifi\data\samples\neso_data_portal\national_demand_bmus.json`,
  `site\hifi\data\notebooks\neso_data_portal\national_demand_bmus.json` and `national_demand_bmus-6.png`. No series file
  (chart `type: none`). No staged chart spec or authored override existed.

## Status

- `gridflow-build --only neso_data_portal/national_demand_bmus`: passes (only the unrelated global warning about 37
  dropped "Known issues" lines).
- Detector `detect.mjs --json`: `[]`.
- Rendered text: 0 em or en dashes, arrows or middle dots. No "locally", "held", "our", "since 20", "live", "now",
  "real-time" or planning words; the "rows" hits are template text (frame heading, help card).
- Screenshots: headless Chrome at 1440, 1024, 768 and 390 (390 in a 390 px iframe) from my server on 9845 (PID 17285,
  started with the batch method, stopped by that PID). Headless with a 5200 px window drew the petrol "Related datasets"
  stratum as blank cream below the notebook (a capture artefact: the window was taller than the page). So I re-checked
  every width in the browser pane (1440x900, 1024, 768x1024, 390x844): hero and scenery, facts, prose, raw-feed wells,
  folded frame and guide, notebook panel and related list are all fully visible, nothing clipped or overlapping; at 390
  `scrollWidth` = 390 (no sideways scroll), SQL in the notebook wraps inside its cell. No dark theme exists to check
  (as the GIS writer found). Unfolded frame not opened; it adds only the four pipeline columns.

## 1. What one row is, and what "National Demand" means

| Claim | Evidence |
|---|---|
| NESO: "a preliminary list of Balancing Mechanism units that make up National Demand"; related to Historic Demand Data | Package `notes`, catalogue snapshot `20261006T195819Z` (resource description: "preliminary list of BM (Balancing Mechanism) Units that make up National Demand") |
| National Demand, NESO: "is the sum of metered generation, but excludes generation required to meet station load, pump storage pumping and interconnector exports" (also "calculated as a sum of generation based on the operational generation metering from the Transmission Network Operators"; "equivalent to the Initial National Demand Outturn (INDO)") | Field info `20261008T114228Z\historic_demand.json`, field `ND` (quoted verbatim in `what_it_is`) |
| One row = one BM unit name, the file's only column `BM_Name` ("Name of BM Unit", example `AG-ADL03E`, unit blank) | Registry record (one column `BM_Name` → `bm_name`, string); field info `national_demand_bmus.json` |
| Entity key `bm_name`; `latest: whole_capture` (newest capture replaces the list) | Registry `entity_key`, `latest` |
| 1,001 names in the file of 29 September 2026 (stated in `facts.grain`) | NESO's CKAN datastore `total: 1001` (field info request 2026-10-08); silver 1,001 rows, 1,001 distinct |
| No capacity, fuel or dates in the file | One-column header; registry |
| NESO does not say what "preliminary" means | Package notes, resource description and dictionary say nothing more |
| The names are in Elexon's `national_grid_bm_unit` form, not `bm_unit_id` | Notebook cell 4: 859 found, 142 not, joining on `national_grid_bm_unit`; 0 on `bm_unit_id` (note body table) |

I did not state the composition rule (whether these are the units whose metering is summed into ND): NESO's two
sentences together suggest it, but NESO does not say it, and the note's `TODO: verify` stays.

## 2. Time fields

No event time. Registry `temporal: none`, `issue: none`, `vintage: ckan_last_modified`.

| Column | Value (every row) | What it is | Evidence |
|---|---|---|---|
| `timestamp_utc` = `event_time` = `capture_written_at` | 2026-10-08 11:12:57.464036 UTC | gridflow's capture write time | `casting.py` 605 to 607 (`temporal.kind == "none"` → `ctx.capture_written_at`); sidecar `written_at` |
| `published_at` = `available_at` | 2026-09-29 13:45:22.344455, read as UTC | CKAN `last_modified` of the CSV | Sidecar `ckan_last_modified`; ADR-030 |

The page draws no clock: the chart is `type: none`, the frame caption picks rows by name, the guide says
`timestamp_utc` is the capture time and the list has no event time. `query()` filters on `timestamp_utc`
(`_DATE_COLUMN_BY_DATASET['national_demand_bmus']` = `timestamp_utc`, checked in the gridflow_models venv), so the
notebook uses `data.sql()` on `silver_neso_data_portal_national_demand_bmus_latest` (the relation
`_relation_name_for_dataset` returns).

## 3. Captures and repeats

| Capture | Bronze | Silver rows | Distinct `bm_name` | Header |
|---|---|---:|---:|---|
| 2026-10-08 11:12:57 UTC | `raw_20261008T111257Z_7e1e84cf-..._46cdc2ce.csv`, 9,462 bytes = declared length | 1,001 | 1,001 | `BM_Name` |

One capture only. **No 16 October recapture**: bronze `national_demand_bmus/2026/10/08/` is the only date; silver has one
parquet. That is expected behaviour: for an upload resource the connector yields `unchanged` and downloads nothing while
CKAN's `last_modified` equals the newest capture's (`client.py` `iter_members`, around line 1753). With one capture there
is no change in the unit list to report. `dedup: {on: [bm_name], order_by: capture_written_at}` is set on the frame as a
guard (sample.py keeps the last row after the sort, so the newest capture wins). No chart, so no chart dedup.

The note's "one capture" statements are still true on 2026-10-23; I dated the Cadence one and gave the skip rule (body
edit 2) instead of rewriting them.

## 4. Visual

`type: none`, reason: "A list of unit names with no other column: nothing NESO publishes here to count or plot by."
A bar of name prefixes (`AG-` 299 names, and so on) would rest on an undocumented naming convention, and a chart spec
reads one silver table, so it cannot join Elexon's register.

The honest category count is in the notebook instead, dated: the list joined to Elexon's BM unit register (bronze
fetched 2026-09-26 19:08:05 UTC; silver `ingested_at` is the transform stamp, `bmunits.py` line 194), three days before
NESO's file was last modified.
- Cell 3 `sql()` join and `.head()`.
- Cell 4: 859 in the register, 142 not.
- Cell 5: the register's fuel types against list membership: none of its 16 `PS` units or 11 interconnector units (ten
  `INT*` codes, `INTELEC` has two) is on the list; WIND 222 of 234, CCGT 47 of 61, NUCLEAR 14 of 16, and so on.
- Cell 6: horizontal bars of the 1,001 names by Elexon fuel type: no fuel type 445, WIND 222, not in register 142, OTHER
  89, CCGT 47, NPSHYD 16, NUCLEAR 14, BIOMASS 12, OCGT 12, COAL 2 (sum 1,001). `plot_alt` matches.
- 6 cells, 8.4 s, no errors, all read-only.

`needs`: "NESO's national demand BM unit list and Elexon's BM unit register". A reader's register will be newer, so
their counts will differ; the lead dates the one the outputs use.

Frame: eight names `ABERU-1`, `ABRTW-1`, `AG-ADL03E` (NESO's dictionary example), `AG-PEPG01`, `DIDCB6`, `DNGB21`,
`HAB02G`, `ZEN02A`, ordered by name; columns `bm_name`, `published_at`, `timestamp_utc`, `capture_written_at`,
`bronze_capture_id` first.

## Body corrections

1. Two clocks, item 2: `casting.py` "line 484" → "lines 605 to 607" (line 484 is the `sp_pair` branch; the
   `temporal.kind == "none"` assignment is at 605 to 607).
2. Cadence: "One capture (2026-10-08) exists to date." → it is still the only one on 2026-10-23, and an ingest skips an
   upload resource while its CKAN `last_modified` equals the newest capture's (`client.py` `iter_members`).
3. Elexon cross-check: added one sentence after the existing match table: the 859 matched names by Elexon `fuel_type`
   (222 WIND, 89 OTHER, 47 CCGT, 16 NPSHYD, 14 NUCLEAR, 12 BIOMASS, 12 OCGT, 2 COAL, 445 none), and that none of the
   register's 16 `PS` or 11 interconnector units is on the list, "NESO states no rule that explains this". Same
   snapshot as the existing table; checked by Polars and by notebook cells 5 and 6. This is an addition next to the
   composition `TODO`, not a correction; the checker may rule it out of scope.

Other body facts re-checked and still true: 1,001 rows and distinct names; `"EEND01 "` with its trailing space (silver
length 7, data row 989, CSV line 990); CKAN size 6,175 against body 9,462; 859 / 142 / 17 match counts; package created
2024-04-15.

## Unverified

- The meaning of "preliminary", and the composition rule (left as the note's `TODO: verify`).
- Why 142 names are not in Elexon's register (for example `CLUN-1`, `RANN-1`, `DIDC1`, `AG-PEPG01`); the register
  predates NESO's file by three days, but that does not explain any one name.
- `neso_data_portal/daily-demand-update` related note ("Recent `ND` outturn with a short forecast tail") leans on that
  note's own description (about ten days' lag, a 7-day forecast tail); not re-researched.
- `elexon/indo` related note: NESO's dictionary says ND "is equivalent to" INDO; the vault records that measured
  equality was not established, so the note says "which NESO calls equivalent", not "the same".

## Open questions and template problems

- First note on the new template with `chart: {type: none}`. It builds, renders no chart figure and no reason text.
  Fine here; the seat may want the reason shown, or a line in the author brief that `chart_view` is omitted for `none`.
- `gridflow-distil` prints "wrote 1 series file(s)" for a `type: none` spec although it writes none (it reports "no
  chart (spec type none)" on the line above). Cosmetic.
- Headless Chrome with a window taller than the page leaves the last petrol stratum unpainted in the capture; checking
  in the browser pane at fixed viewport heights avoids it. Worth a line in AGENT-PROMPTS for writers and checkers.

## Defects

- **gridflow_models: `query()` on a reference table filters on the capture time** (already logged from the GIS page).
  For `national_demand_bmus` (temporal `none`) `_DATE_COLUMN_BY_DATASET` is `timestamp_utc`, the capture instant
  (2026-10-08 11:12:57 UTC), so `data.neso_data_portal.query("national_demand_bmus", start, end)` returns rows only for
  a window holding a capture day, with no warning. Same as `gis_grid_supply_points` and Elexon `bmunits_reference`.
- **front-end `gridflow-distil`: misleading count for a `type: none` spec.** It prints "wrote 1 series file(s)" when it
  writes none (`--dataset neso_data_portal/national_demand_bmus`, 2026-10-23).
- **NESO data (open question, not a confirmed defect): 142 of 1,001 names have no match** in Elexon's BM unit register
  (`national_grid_bm_unit` or `bm_unit_id`), register fetched 2026-09-26; examples `CLUN-1`, `RANN-1`, `DIDC1`,
  `AG-PEPG01`, `"EEND01 "` (trailing space). Already a `TODO: verify` in the note; a newer Elexon register would settle
  how many are timing.
- **NESO metadata: CKAN `size` 6,175 bytes against a 9,462-byte delivered body** for resource `7e1e84cf` (same
  `last_modified`). Already in the note's implementation delta.
