# GIS Boundaries for GB Grid Supply Points: writer's report, round 2

All five review findings fixed in the canonical note
`C:\gridflow-wt\vault-neso-sys\30-vendors\neso-data-portal\datasets\gis-boundaries-for-gb-grid-supply-points.md`
(542 lines, all CRLF), mirrored to `C:\gridflow-wt\fe-neso-sys\vault\neso_data_portal\gis-boundaries-for-gb-grid-supply-points.md`
(`cmp` clean). `gridflow-build --only neso_data_portal/gis_grid_supply_points` passes; detector `[]`; rendered text
has 0 em or en dashes, arrows or middle dots. Chart spec, frame selection and notebook are unchanged, so the series,
sample and notebook artefacts were not regenerated (the build's digest checks pass). No server was started this round,
as instructed, so no new screenshots; the changes are text in the column guide, key note, how-used list and intro,
which wrap in place.

## Fixes

1. **Major: positive longitudes on three Direct Connect rows.** Reproduced in silver: `ggd_id` 290 (Gnode `CASK`,
   `T_CASKD-1`) has `gnode_lon` and `dc_lon` 2.7297 at 53.3421; `ggd_id` 373 and 374 (`T_THNJD-1`, `T_THNJD-2`) have
   `dc_lon` 2.1464 at 51.4341 while their Gnode `MELK` is at -2.150383. Every other `gsp_lon` is at most 1.3459 and
   every other `gnode_lon` at most 1.27176. The checker's finding also covers `gnode_lon` on row 290, which the frame
   shows, so both guide lines carry the caveat:
   - `record.fields.dc_lon`: "Direct Connect longitude, decimal degrees; three positive values fall at sea, kept as
     published"
   - `record.fields.gnode_lon`: "Gnode longitude, decimal degrees, WGS 1984; `CASK`'s positive value falls at sea"
   - Note body: new section "Known issues and gotchas" (the convention in the ETYS and inertia notes; this note had
     none) with one bullet giving the rows, values, the 1.3459 maximum elsewhere, NESO's `2.7297` dictionary example,
     "kept as published, not corrected" and a TODO to ask NESO about the sign. The build accepts it (no new caveat
     grammar warning beyond the global 35).
   - Added to Defects below.
2. **Nit: `what_it_is`.** Now quotes NESO verbatim: Grid supply points (GSPs), NESO says, "are points of connection
   between the Transmission System and a Distribution System" (catalogue snapshot `20261006T195819Z`, package notes).
   57 words.
3. **Nit: key note.** Now names the source: "Names from NESO's FES building block licence-area lookup; Merseyside, N
   Wales is Merseyside and North Wales." (silver `fes_building_blocks_block_licence_area`).
4. **Nit: `how_used[1]`.** Now "Join a GSP to its 2018 boundary by `region_id`; four GeoJSON `RegionID`s repeat."
   (note body "Pairing with the 2018 GIS files": `18`, `41`, `60`, `64` twice each in 329 features). 13 words.
5. **Nit: orphan line.** The intro paragraph is re-wrapped; "The **current** GSP Regions version is `20260209`" now
   runs on one line.

## Defects

- **NESO data: positive longitudes on three Direct Connect rows of the GSP lookup.**
  `gsp_gnode_directconnect_region_lookup.csv` (resource `bbe2cc72`, last modified 2020-05-05), silver
  `gis_grid_supply_points`: `ggd_id` 290 (`CASK` / `T_CASKD-1`, lat 53.3421, `gnode_lon` and `dc_lon` +2.7297) and
  `ggd_id` 373, 374 (`T_THNJD-1`, `T_THNJD-2`, lat 51.4341, `dc_lon` +2.1464; their Gnode `MELK` at -2.150383). Both
  points fall in the sea east of England; every other longitude in the file is at most 1.3459. NESO's field dictionary
  repeats `2.7297` as its `dc_lon` example. Kept as published (no range rule on the coordinate columns). Question for
  NESO: is the sign missing? The 2018 GIS files are untabled, so not checked there.
- **gridflow_models: `query()` on a reference table filters on the capture time** (from round 1, confirmed by the
  checker). For `gis_grid_supply_points` (temporal `none`) `_DATE_COLUMN_BY_DATASET` is `timestamp_utc`, the capture
  instant, so `query()` returns rows only for a window holding a capture day, with no warning. Same shape as Elexon
  `bmunits_reference`. Suggest returning the latest capture for temporal-`none` tables, or refusing with a pointer to
  `data.sql()`.
