# GIS Boundaries for GB Grid Supply Points (`gis-boundaries-for-gb-grid-supply-points`): checker's review

Checker: round 1. Table `gis_grid_supply_points`. Port 9895 (server PID recorded, stopped by that PID; port confirmed
closed afterwards).

## Verdict: REVISE

1 major, 4 nits. No blocker. Every number, quote and time claim I tried to break held. The one major is a vendor data
defect that sits in the page's own frame and that the writer's report says does not exist.

## What I checked and found sound

- **Build and detector.** `uv run --system-certs --extra build gridflow-build --only neso_data_portal/gis_grid_supply_points`
  passes (the only noise is the global 35-line "Known issues" warning and another agent's page, "left for the full
  build"). `detect.mjs --json` returns `[]`. `cmp` of the canonical note and the mirror is clean. The vault diff against
  `origin/master` is the `page:` block plus the one body edit the report describes.
- **What one row is.** Silver (380 rows, one parquet file): `ggd_id` 380 distinct, no nulls. Row kinds by nulls: 356 with
  a GSP and a Gnode, 4 with a GSP and no Gnode, 19 with a Gnode and a Direct Connect, 1 Gnode only (`DEESDM`, `ggd_id`
  289). 360 rows name a GSP, 19 are Direct Connects, 1 is Gnode only: 380. 338 distinct `gsp_id`, equal to 338 distinct
  `gsp_name`, one to one (the struct of both is also 338). 19 GSPs sit on repeat rows (16 on two, 3 on three). The page
  never says "region with geometry": the grain line, the summary and the guide all describe a lookup entry, and geometry
  is said to live in the GIS files.
- **NESO's GSP definition.** The catalogue snapshot `20261006T195819Z` (package notes) says GSPs "are points of connection
  between the Transmission System and a Distribution System". The page paraphrases that accurately (see nit 2 on the
  "In NESO's words" framing). The Gnode, Direct Connect, `has_pv`, `pes_id`, `pes_name`, `gsp_name` and id wording all
  match `field-info/20261008T114228Z/gis_grid_supply_points.json` (read in the gridflow repo's
  `.planning/research/neso-snapshots`). `pes_id` "10 to 23: the Distributor ID in an MPAN" is the vendor's own comment.
- **The chart.** I recomputed distinct `gsp_id` per `pes_name`: `_N` 80, `_P` 63, `_M` 21, `_H` 21, `_A` 20, `_F` 20,
  `_G` 19, `_C` 18, `_E` 16, `_B` 14, `_D` 13, `_J` 12, `_K` 11, `_L` 10; sum 338. This is identical to the committed
  series `site/hifi/data/series/neso_data_portal/gis_grid_supply_points.json` (14 categories, values in the same order).
  Series provenance: 380 read, 360 matched, 22 duplicates dropped, 338 used; 380 - 20 null-GSP rows - 22 repeats = 338.
  The alt text and the title numbers match the series exactly (80, 63, "the other twelve have 10 to 21", every value in
  the list). `spec_origin: vault`, `generated_by: gridflow-distil`, caption in the JSON empty (the note's caption is
  used), no staged spec.
- **`dedup` on `gsp_id` is safe.** 0 of the 338 GSPs have more than one `pes_name` or any null `pes_name`, so which
  repeat row survives does not change a count. (The 22 dropped rows are the 19 GSPs' extra Gnode rows.)
- **The group-name join is honest.** The 14 names come from silver `fes_building_blocks_block_licence_area`
  (`elexon_gsp_group` to `elexon_gsp_group_name`, edition 2024): every one of the 14 letters maps to the name in
  `group_map`; `_D` is "Merseyside and North Wales" (shortened on the bar, spelled out in the key note). A second,
  independent check agrees: `pes_id` to `pes_name` in the lookup itself gives 17 = `_P` (North Scotland) and
  18 = `_N` (South Scotland), as MPAN Distributor IDs do, and the scatter in the notebook puts the 63-GSP group in the
  far north and the 80-GSP group across the central belt.
- **Time fields.** `timestamp_utc` = `event_time` = `capture_written_at` = 2026-10-08 11:04:07.596378 UTC on every row
  (one unique value); `published_at` = `available_at` = 2020-05-05 07:54:07.800829 (sidecar `ckan_last_modified`
  `2020-05-05T07:54:07.800829`, a naive CKAN stamp, so "read as UTC" is the right hedge). The page calls `timestamp_utc`
  the capture time with "no event time", calls `published_at` NESO's last-modified time, draws no clock and never
  presents either as a data time. The facts line, the caption and the intro say "last modified", not "published".
- **Notebook and `query()`.** In the `gridflow_models` venv `_DATE_COLUMN_BY_DATASET['gis_grid_supply_points']` is
  `timestamp_utc` and `_RELATION_NAME_BY_DATASET` gives `silver_neso_data_portal_gis_grid_supply_points_latest`, so the
  lead text and `data.sql()` are right. The notebook JSON is `generated_by: scripts/run_notebooks.py`, six cells,
  no error output (0 "error"/"Traceback" in the file). Cell 3 prints `ggd_id` 1 to 5; cell 4 prints 356 / 19 / 4 / 1
  (matches my group-by); cell 5 prints the 14 counts (matches); cell 6 is the scatter. I read the PNG: 338 points,
  Great Britain's outline, the London cluster dense, the two Scottish groups far apart. `plot_alt` (50.4 to 58.6 N,
  6.6 W to 1.3 E) matches my min and max (50.394, 58.576, -6.645, 1.346).
- **Captures.** One bronze capture of the lookup: `gis_grid_supply_points/2026/10/08/raw_20261008T110407Z_bbe2cc72...csv`,
  body 34,324 bytes = declared length, 380 data rows. `gis_grid_supply_points_files/2026/10/08/` holds nine files
  (eight GIS and the changelog), all 8 October. No 16 October capture of anything in the package.
- **Raw feed.** The lookup URL equals the bronze sidecar's `request_url`; the third URL is the `5dfab3dd` resource of the
  note's download table; `_package_show` sends `id=<package>`; the unchanged-skip on `last_modified` is real
  (`client.py` around lines 1666 to 1765); `window must end recently` matches the D-34 guard (`client.py` around 1545);
  `gis_grid_supply_points_files` is a registry family. Leakage grep of the `page:` block and the rendered text: no em or
  en dashes, arrows, middle dots, "locally", "held", "our ", "since 20", "now", "real-time". "rows" appears only for
  lookup rows, "live" only inside "PV_Live".
- **Related notes** are all 12 words or fewer. `bmunits_reference.gsp_group_id` holds `_A` to `_P` (checked in silver).
  `neso/regional_intensity` regions 1 to 14 are DNO areas (its vault note); `pes_id` is "a.k.a. DNO Licence Area".
- **Screenshots** (Chrome headless at 1440, 1024, 768; 390 in a 390 px iframe; looked at 1440 whole and the 390 hero,
  intro, chart, raw feed and column guide). Nothing clipped or overlapping. At 390 the longest bar label ("Merseyside,
  N Wales") starts about 5 px from the frame edge and is fully visible. Unfolded frame opened in the preview browser:
  all 27 columns scroll inside the frame's own box, nothing clipped. Notebook panel opens and shows the six cells with
  outputs.

## Findings

1. **major** · `page.record.fields.gnode_lon`, `dc_lon` and the frame row `ggd_id` 290 (also a missing defect in the
   writer's report). The vendor file has Direct Connect and Gnode longitudes that cannot be right, and the page puts one
   of them on screen without a word. Silver, Direct Connects sorted by `dc_lon`:
   `T_CASKD-1` (Gnode `CASK`) 53.3421, **2.7297**; `T_THNJD-1` and `T_THNJD-2` (Gnode `MELK`) 51.4341, **2.1464**, while
   the same Gnode `MELK` has `gnode_lon` -2.150383 at 51.391815. Every other point in the table is west of 1.35 E (the
   largest `gsp_lon` is 1.3459) and the other 16 Direct Connects are all negative. A positive 2.73 E at 53.34 N, and
   2.15 E at 51.43 N, are in the sea, east of the English coast; the same latitudes with the sign flipped are
   Cheshire and Wiltshire. NESO's own field-info example for `dc_lon` is `2.7297`, so the error is in the vendor
   dictionary too. Frame row 290 prints `gnode_lon 2.7297` and `dc_lon 2.7297` under the guide line "Gnode longitude,
   decimal degrees, WGS 1984", so a reader sees a GB point in the North Sea and has no explanation. The writer's report
   ("No NESO data defect found beyond what the note already records") is therefore wrong, and batch practice is to log
   every data defect a package shows. Fix: (a) add the defect to the Defects list and to the vault remediation page
   (three Direct Connect rows, two distinct places, positive longitude where the sign looks dropped); (b) on the page,
   one short caveat on the `dc_lon` guide line, stated as what the rows show and not as a correction, for example
   "NESO's values for three Direct Connect rows are positive, which falls in the sea; kept as published". Keep
   it to the evidence above; do not repair the values.

2. **nit** · `page.what_it_is`. "In NESO's words a grid supply point (GSP) is a point of connection between the
   transmission system and a distribution system." NESO's sentence is "GSPs are points of connection between the
   Transmission System and a Distribution System." The meaning is right but the singular, the lower case and "a point"
   make it a paraphrase presented as NESO's words. Either drop "In NESO's words" or quote it as written.

3. **nit** · `page.chart_view.key[0].note`. "Group names from NESO's FES area lookup" does not name the dataset, so a
   reader cannot find it. The join is the page's own (letter code to name through `group_map`) and is correct against
   silver `fes_building_blocks_block_licence_area` (all 14, edition 2024). Name it ("NESO's FES building block
   licence-area lookup") or point to its vault page.

4. **nit** · `page.how_used[1]`. "Join a GSP's Elexon settlement name to its 2018 boundary through `region_id`." is
   right (NESO's resource description says the lookup says which region represents each entry), but the join is not one
   to one on the boundary side: the 2018 GeoJSON has 329 features and 325 distinct `RegionID` values, with 18, 41, 60 and
   64 each twice (read from the bronze GeoJSON `a3ed5711`). The note body already says so. A short parenthetical
   ("four `RegionID` values repeat in the GeoJSON") would stop a reader from assuming a clean join. Room exists in the
   how-used budget; check `BUDGET`.

5. **nit** · vault note body, the intro paragraph the writer edited. The replacement text is correct, but the edit left
   a hard line break after "2020-05-05. The **current**" so the paragraph now has one short orphan line before
   "GSP Regions version is `20260209`". Re-wrap that paragraph (CRLF, re-mirror, `cmp`).

## Template and seat items (not findings)

- The chart title cannot carry backticks (writer found it); the 9-entry key cap; the 390 px label column at about 19
  characters ("Merseyside, N Wales" has about 5 px to spare, so any longer group name would clip at 390).
- The notebook's first output card lists `refresh` among the source's methods; it is the template's standard card, no
  cell calls it.

## Defects (pasteable)

- **NESO data: positive longitudes on three Direct Connect rows of the GSP lookup.** `gsp_gnode_directconnect_region_lookup.csv`
  (`bbe2cc72`, last modified 2020-05-05): `ggd_id` 290 (`CASK` / `T_CASKD-1`, 53.3421, +2.7297) and `ggd_id` 373, 374
  (`T_THNJD-1`, `T_THNJD-2`, 51.4341, +2.1464; their Gnode `MELK` is at -2.150383). Every other coordinate in the file
  is west of 1.35 E. Kept as published; NESO's field-info example for `dc_lon` repeats `2.7297`. Remediation page entry
  needed; the 2018 shapefile and GeoJSON are untabled, so I did not check whether the same points are wrong there.
- **gridflow_models (writer's, confirmed):** `query()` on a temporal-`none` table filters on the capture time; confirmed
  `_DATE_COLUMN_BY_DATASET['gis_grid_supply_points']` is `timestamp_utc`.
