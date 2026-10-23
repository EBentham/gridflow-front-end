# GIS Boundaries for GB Grid Supply Points (`gis-boundaries-for-gb-grid-supply-points`): writer's report

One-table package page, lead key `gis_grid_supply_points`. The manifest is right: one table (the lookup CSV); the
boundary files and changelog are the `gis_grid_supply_points_files` family, which is files only and has no silver.
Nothing is held on the ledger (`v0.22-FE-LEDGER.md` line 130: eligible, the embedded 2018 CSV copy held as a duplicate,
which is not a table).

Files written:
- Canonical note `C:\gridflow-wt\vault-neso-sys\30-vendors\neso-data-portal\datasets\gis-boundaries-for-gb-grid-supply-points.md`
  (page block added, one body edit; 532 lines, all CRLF).
- Mirror `C:\gridflow-wt\fe-neso-sys\vault\neso_data_portal\gis-boundaries-for-gb-grid-supply-points.md` (`cmp` clean).
- Artefacts: `site\hifi\data\series\neso_data_portal\gis_grid_supply_points.json`,
  `samples\neso_data_portal\gis_grid_supply_points.json`, `notebooks\neso_data_portal\gis_grid_supply_points.json` and
  `gis_grid_supply_points-6.png`. No staged chart spec or authored override existed.

## Status

- `gridflow-build --only neso_data_portal/gis_grid_supply_points`: passes (only the unrelated global warning about 35
  dropped "Known issues" lines).
- Detector `detect.mjs --json`: `[]`.
- Rendered page text: 0 em or en dashes, arrows, middle dots; no "locally", "held", "our", "since 20", "now",
  "real-time" or planning words. The one "live" hit is the product name "PV_Live" (University of Sheffield), in a
  how-used line; not live framing.
- Screenshots at 1440, 1024, 768 and 390 (390 in a 390 px iframe), my server on 9885 started with the batch method
  (PID 598) and stopped by that PID. The site has no dark theme (no `prefers-color-scheme` rule in `theme.css`,
  `tokens.css` or `site.js`), so the forced-dark run renders the same as light. Nothing clipped or overlapping: hero
  and scenery, facts, chart and key, raw-feed wells, folded frame and guide, notebook panel, related list. At 390 the
  longest bar label ("Merseyside, N Wales") starts about 5 px from the frame edge, fully visible; the notebook tab
  name is truncated with an ellipsis (known template item). Unfolded frame not opened (headless, no click).

## 1. What one row is

| Claim | Evidence |
|---|---|
| A GSP, in NESO's words, is "points of connection between the Transmission System and a Distribution System" | Package notes, catalogue snapshot `20261006T195819Z` |
| The package: approximate GSP boundaries in GIS files (six versions, `20181031` to `20260209`) plus one lookup CSV and a changelog; only the lookup is a table | Registry `registry/gis-boundaries-for-gb-grid-supply-points.json`: family `gis_grid_supply_points` (tabular, REG, SILVER) and `gis_grid_supply_points_files` (kind `files`); resource names |
| One row = one lookup entry, key `ggd_id`. NESO: "Unique ID representing a fundamental entity in the lookup between GSP, Gnode and DNO License Area"; "Facilitates a MANY:MANY relationship between GSP and Gnode" | Registry `entity_key: [ggd_id]`; field info `field-info\20261008T114228Z\gis_grid_supply_points.json` |
| It is not a region with geometry: silver holds ids, names and WGS 1984 points only; geometry stays in the untabled GIS files | Registry columns (19, no geometry); silver schema |
| Row kinds: 356 rows with a GSP and a Gnode; 4 with a GSP and no Gnode; 19 with a Gnode and a Direct Connect (no GSP, region or group); 1 Gnode only (`DEESDM`) | Silver `group_by` on nulls; the notebook's second cell prints these counts |
| 338 distinct GSPs; 19 GSPs sit on 2 or 3 rows (one GSP, several Gnodes); 11 Gnodes sit on 2 to 6 rows | Silver |
| Every GSP sits in exactly one GSP group (`pes_name`) | Silver: 0 `gsp_id` with more than one `pes_name`; `gsp_id` and `gsp_name` one to one |
| Gnode, Direct Connect, `has_pv`, `pes_id`, `pes_name`, ids "arbitrary ... not consistent between versions", coordinates WGS 1984 | Field info file, quoted per column in the guide |

## 2. Time fields

No event time. Registry `temporal: none`, `vintage: ckan_last_modified`.

| Column | What it is | Evidence |
|---|---|---|
| `timestamp_utc` = `event_time` = `capture_written_at` | gridflow's capture time, 2026-10-08 11:04:07.596378 UTC, one value on every row | Silver unique values; bronze sidecar `written_at` |
| `published_at` = `available_at` | CKAN `last_modified` of the CSV, 2020-05-05 07:54:07.800829, read as UTC | Silver; sidecar `ckan_last_modified` |

The page never draws a clock: the chart is a bar, the frame's caption picks rows by entry, and the guide says
`timestamp_utc` is the capture time and the table has no event time. The workbench `query()` filters on
`timestamp_utc` (`_DATE_COLUMN_BY_DATASET['gis_grid_supply_points']` = `timestamp_utc`, checked in the
gridflow_models venv), which here is the capture day, so the notebook uses `data.sql()` on
`silver_neso_data_portal_gis_grid_supply_points_latest` (the relation `_relation_name_for_dataset` returns).

## 3. Captures and repeats

| Capture | Bronze rows | Silver rows | Body = declared length | Distinct `ggd_id` |
|---|---:|---:|---|---:|
| 2026-10-08 11:04:07 UTC (`raw_20261008T110407Z_bbe2cc72..._e6048a53.csv`) | 380 (+ header) | 380 | 34,324 = 34,324 | 380 |

One capture only. **No 16 October recapture** of the lookup or of any boundary file (bronze
`gis_grid_supply_points*/2026/10/08/` only). No truncation, no repeats. Region count cannot change between captures
(one capture; 325 distinct `region_id`). `dedup` is set on the frame as a guard (`on: [ggd_id]`, `order_by:
capture_written_at`). On the chart, `dedup` does real work: `on: [gsp_id]`, `order_by: ggd_id` collapses a GSP on
several rows to one (`duplicates_dropped: 22` in the series provenance); since each GSP has one `pes_name`, which row
is kept does not change any count.

## 4. Chart

Bar, `neso_data_portal/gis_grid_supply_points`, filter `gsp_id` not null (360 rows), dedup per `gsp_id` (338), count
per `pes_name`, sorted by value. No map: `locations` is Open-Meteo only (`locations.py` reads gridflow's weather
endpoints) and the chart types are line, stacked area, bar or none. A count of distinct GSPs per GSP group is honest:
it is what the rows support, nothing is summed, no time.

Series (committed): South Scotland 80, North Scotland 63, Southern 21, Yorkshire 21, Eastern 20, Northern 20, North
Western 19, London 18, Midlands 16, East Midlands 14, Merseyside, N Wales 13, South Eastern 12, South Wales 11, South
Western 10 (sum 338). Matches my own Polars count and the notebook's third cell.

Bar labels are NESO's GSP group names, mapped in `group_map` from `_A` to `_P`. Source: NESO's FES building-block area
lookup, silver `fes_building_blocks_block_licence_area` (`elexon_gsp_group`, `elexon_gsp_group_name`; all 14 checked;
also tabled in the vault note `future-energy-scenario-fes-building-block-data.md`). "Merseyside and North Wales" is
shortened to "Merseyside, N Wales" on the bar (label width 150 px, 110 on phones); the key note gives the full name.
One key entry (series `count`), because the build allows at most 9 key entries and a bar chart needs none per
category.

Frame: eight entries `ggd_id` 1, 290, 301, 302, 303, 357, 358, 377: a one-to-one row (Cowley), a Direct Connect
(`T_CASKD-1`, `has_pv` 0, null GSP and group), one GSP on three Gnodes (`BRLE_1` on `BRL1` to `BRL3`), one Gnode on
two GSPs (`AMEM` on `AMEM_1` and `LOUD_H`, two groups), and a GSP with no Gnode (`KNAR`). Columns print names first so
the relations stay in view when the frame folds.

Notebook (6 cells, 5.8 s, no errors): the `sql()` read and `.head()`; row kinds; distinct GSPs per group (matches the
chart); a scatter of the 338 GSP points by latitude and longitude, coloured by `pes_id` (traces Great Britain, 50.39 to
58.58 N, 6.65 W to 1.35 E).

## Body corrections

1. Intro: "The files were published on 2020-05-05" now reads "last modified (CKAN `last_modified`) on 2020-05-05". The
   date is CKAN's `last_modified` (registry `vintage: ckan_last_modified`; catalogue snapshot), not a publish time.

All other body numbers re-checked against silver and hold: 380 rows; `ggd_id` 380 distinct; `gnode_id` 360,
`gsp_id` 338, `region_id` 325, `dc_id` 17 distinct; nulls 4 / 20 / 361; `has_pv` 356 and 24; `ng_id` differs from
`ggd_id` on one row (387 against 372, `MELK_1`); the `(gnode_id, gsp_id, dc_id)` triple unique; `Clyde’s Mill`
spelling in the lookup.

## Unverified

- The ETYS related note ("study boundaries across the transmission network") leans on that page's own summary in its
  vault note; I did not research ETYS further.
- `neso/regional_intensity` related note ("per DNO licence area, the level GSP groups form"): NESO's lookup equates the
  GSP group with the DNO licence area (`pes_id` description), and the Carbon Intensity regions 1 to 14 are DNO areas
  (vault `neso/README.md`); I did not check that the two sets of 14 areas are drawn identically.
- `gridflow ingest neso_data_portal gis_grid_supply_points_files --last 24h`: the family is in the connector's
  `FAMILIES` and bronze holds its captures, but I did not run it (never run ingest).

## Open questions and template problems

- A chart title prints backticks literally (first build showed "lookup \`20181031\`"); I removed them. Titles are plain
  text, unlike captions. Worth a line in the author brief.
- The 9-entry key cap means a bar chart with more than 9 categories cannot give each bar its code; the codes then
  show only in the frame and notebook. Fine here; seat may want it noted.
- At 390 the 110 px bar-label column holds about 19 characters; "Merseyside, N Wales" fits with 5 px to spare.

## Defects

- **gridflow_models: `query()` on a reference table filters on the capture time.** For `gis_grid_supply_points`
  (temporal `none`) the manifest date column is `timestamp_utc`, which silver sets to the capture instant
  (2026-10-08 11:04 UTC). `data.neso_data_portal.query("gis_grid_supply_points", start, end)` therefore returns rows
  only when the window contains a capture day, and nothing for any other window, with no warning. Same shape as
  Elexon `bmunits_reference` (`ingested_at`). Readers must use `data.sql()` on the `_latest` relation. Suggest: a
  `query()` on a temporal-`none` table returns the latest capture whatever the window, or refuses with a pointer to
  `sql()`.
- No NESO data defect found beyond what the note already records (the mis-decoded apostrophe in the 2018 GeoJSON's
  `Clyde’s Mill`, the four repeated `RegionID` values in that GeoJSON, ids not stable between versions).
