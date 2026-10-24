# SSEP publication and economic zones (held): writer report (2026-10-24)

Package `ssep-onshore-publication-zone-shapefile`, one table `ssep_publication_zones_files` (registry `kind: files`,
`transformer: null`; ledger row 128 "GIS only (3 ZIPs: onshore, offshore, economic zones), catalogue + download").
It ships held only because it has no silver table (batch file, seat PROXY-SOURCED); the registry marks it eligible.

The `page:` block is on the canonical note
`C:\gridflow-wt\vault-neso-sep\30-vendors\neso-data-portal\datasets\ssep-onshore-publication-zone-shapefile.md`
and is copied byte for byte to `C:\gridflow-wt\fe-neso-sep\vault\neso_data_portal\` (`cmp` clean after the last edit).
The note was CRLF on every line before (192/192) and still is (241/241); the Edit tool kept CRLF. The vault diff is
59 insertions and 10 deletions, with no whole-file rewrite. `updated:` is now 2026-10-24.

## Gates

| Gate | Result |
|---|---|
| `parse_page_fields` / `anatomy_errors` | `[]` / `[]` (what_it_is 60, held 16, summary 21, title 5, facts 8/14/13, uses 11/13, raw note 25, related 10 to 12) |
| `gridflow-build --only neso_data_portal/ssep_publication_zones_files` | wrote `data-sources/neso_data_portal/ssep-onshore-publication-zone-shapefile.html`, no errors |
| Detector | `[]` |
| Rendered text | 0 em or en dashes, arrows or middle dots; none of live, now, yet, soon, planned, shipped, locally, ruling, ledger, TODO, held, hold, our; no Crown Estate, EPSG or 27700; viewport meta and `<main>` present; one "Rows not shown" block |
| Screenshots | 1440, 1024, 768 (window) and 390 (390 px iframe), light mode: nothing clipped or overlapping; URLs and keys wrap. In `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\ssep-held-writer\shots\` |
| Server | Bash `python -m http.server 9962 ... & echo $!`, PID 66710, stopped by that PID and confirmed down. 9670 not touched. Dark mode not checked (headless flags do not switch the palette). |

The build's repo-wide warning now counts 37 dropped "Known issues" lines (earlier batches reported 35). This note
contributes none: `_extract_caveats` on its Known issues section gives 0 dropped lines before and after my edits.

## What the page says

- **Held line (16 words):** "Three zipped shapefiles, kept whole; gridflow reads no rows from them and builds no silver
  table." This follows ETYS ("One zipped shapefile, kept whole; ...") and charging zones ("Two map files, kept whole; ...").
- **Title:** SSEP publication and economic zones. **Summary:** NESO's zone boundaries for the SSEP (spelled out): land
  and marine publication zones and land economic zones, as shapefiles.
- **Facts:** the package and its three ZIP files; ad hoc, last modified 11 February and 3 March 2026; one shapefile
  layer per ZIP: 19 onshore, 19 offshore and 17 economic features.
- **What it is (60 words), three sentences:**
  - NESO's file descriptions, as read in October 2026, give its counts: 19 land and 19 marine publication zones for the
    draft and final SSEP, and 17 land economic zones for economic modelling.
  - The files, last modified February and March 2026, contain 19, 19 and 17 features and state British National Grid
    coordinates in metres.
  - The package title names only the onshore file.
- **How it's used:** draw the land and marine publication zones on a map; group land data by SSEP economic zone.
- **Raw feed:** `package_show` plus the three sidecar `request_url`s (4 of 4 allowed); one `ingest` command, with no
  transform command.
- **Related:** grid supply points (NESO's `20260209` version associates GSPs with SSEP economic zones); generation
  charging zones; ETYS boundaries; DNO licence areas.

## Evidence

| Claim | Evidence |
|---|---|
| 19 land / 19 marine publication zones "for the publication of the draft and final" SSEP; 17 land economic zones "used for ... SSEP economic modelling" | resource descriptions, catalogue snapshot `20261006T195819Z` (gridflow `.planning/research/neso-snapshots/`), dated "as read in October 2026" as on the charging-zones page |
| "draft and final" | only as NESO's description says it. The page does not say which edition any file is. |
| Package notes: "Onshore and Offshore economic and publication zones related to the draft and final ..." | snapshot `notes`; package title names only the onshore file |
| Ad hoc | snapshot extras "Update frequency: Ad-hoc" |
| Last modified 11 Feb 2026 (economic) and 3 Mar 2026 (onshore 16:32:10, offshore 16:30:55) | sidecar `ckan_last_modified`, equal to the snapshot |
| 19, 19, 17 features; one layer per ZIP; all polygons | measured on the 2026-10-08 bronze (2026-10-24): `.shx` records 19/19/17; `.dbf` records 19/19/17; every `.shp` record is shape type 5; `testzip` clean. Matches `gis-facts.json`. |
| British National Grid coordinates in metres, **stated by the files** | each `.prj` is `PROJCS["British_National_Grid", GEOGCS["GCS_OSGB_1936" ...] ... UNIT["Meter",1.0]]`. The batch rule cuts CRS wording unless a file states it; all three do. Same pattern as charging zones ("state WGS 84 coordinates in degrees"). |
| Download rule: one `package_show`, each upload whole unless its `last_modified` is unchanged | gridflow `connectors/neso_data_portal/client.py` `iter_members` docstring, lines 1663-1670 |
| Request URLs | each sidecar's `request_url` (three captures, 2026-10-08; no later captures) |
| ZIP sizes (not on page) | 253,690 / 433,761 / 830,975 bytes; SHA-256 matches sidecars |
| GSP related note | GSP note changelog row `20260209` "GSPs associated with SSEP economic zones" (vendor text) |
| Related targets exist | all four are in the page set; the build resolved them |

**No equivalence.** NESO's counts (19, 19, 17) and the files' feature counts (19, 19, 17) sit in separate sentences,
with different dates ("as read in October 2026" against "last modified February and March 2026"). The page never says
a feature is a zone. File fact, not on the page: the zone attribute is distinct per feature in every file (onshore
`ssep_pubzn` 1 to 19, offshore `PUB_ZN_ID` 19 distinct codes, economic `SSEP_Zone` 1 to 17).

## Body corrections (measured on the 2026-10-08 bronze, 2026-10-24)

1. **Units.** The note said "No unit is stated for the coordinates". The `.prj` states it (`Meter`). Rewritten to say so.
   It also records Esri's `Shape_Area` definition in the `.shp.xml` ("Area of feature in internal units squared") and
   the economic file's history, which computes `Zone_Area_Ha` (DBF `Zn_Area_Ha`) as `!Shape_Area! / 10000`. The
   attribute-unit TODO stays.
2. **`.shp.xml`.** It was "not read; TODO". Now read:
   - The onshore and economic files' metadata hold only processing history and Esri default field definitions. The
     onshore history starts from a layer named `resp_boundaries_lad23_buc_4326`.
   - The offshore file's metadata keeps a Crown Estate source layer's title, abstract, contact and use limitation
     ("United Kingdom Continental Shelf (WGS84) - Juristictions", published 2023-05-25, "Internal use only").
   - The note says the site page does not mention any of this.
3. **Third-party origin bullet.** It now adds the offshore metadata fact. The stale "(DNO ... has no page)" now reads
   "its site page publishes no data".

## Unverified

- What edition of the SSEP each file is. NESO says only "draft and final", and the page claims neither.
- What `v4`, `v5` and `MASTER` mean. They are not on the page.
- The units of `Shape_Leng`, `CENTROID_X`, `CENTROID_Y` and `Zn_Area_Ha`. Not on the page.
- Whether the offshore "Internal use only" limitation is live or stale metadata. NESO's text does not address it.

## Open questions for the seat

1. **Crown Estate use limitation (offshore file).** The DNO package was held for a third-party origin cited in NESO's
   notes. Here the citation is only in a file's embedded metadata, and the package `url` field names ONS under OGL v3.
   This page republishes nothing: it prints NESO's own URLs, as the DNO page does under the same ruling. My
   recommendation: no change to the page; log it with NESO.
2. **Adjacent counts.** NESO's 19/19/17 and the files' 19/19/17 sit in consecutive sentences. A reader may infer one
   feature per zone, which happens to fit the distinct zone ids. The charging-zones ruling kept the analogous pair
   (27 and 28). If the seat wants it stricter, cut the counts from the files sentence and leave them in `grain` only.

## Template problems

None. The held mode rendered as on the other GIS pages.

## Defects

- **NESO, SSEP offshore publication zones file (last modified 2026-03-03):** the `.shp.xml` inside the ZIP carries
  metadata inherited from a Crown Estate layer. That includes the title "United Kingdom Continental Shelf (WGS84) -
  Juristictions" (sic), an abstract about UK Continental Shelf jurisdictions, a named Crown Estate staff contact, and
  the use limitation "Internal use only". The package `url` field cites ONS under OGL v3 instead, and no NESO text
  addresses the Crown Estate origin.
- **NESO, same package:** the package title "... Onshore Publication Zone Shapefile" names one of the three files, and
  the offshore ZIP's layer inside is named `marine_...` while the ZIP is `offshore_...` (cosmetic).
- **NESO, same package:** no data dictionary. Attribute units (`Shape_Leng`, `CENTROID_X/Y`, `Zn_Area_Ha`) are stated
  nowhere by NESO.
- **gridflow:** none. The registry, sidecars, bronze and committed `gis-facts.json` agree (feature counts, bbox, CRS,
  SHA-256).
- **Manifest:** right. `package_tables` maps the package to `ssep_publication_zones_files`, and the slug is in group 0
  of the page set.

## What the checker should look at hardest

1. The `what_it_is` count sentences: dated, separate, with no feature-to-zone claim (open question 2).
2. "state British National Grid coordinates in metres": confirm against the three `.prj` files, not NESO's text.
3. "draft and final SSEP": attributed only to NESO's file descriptions.
4. The note-body `.shp.xml` and third-party additions: measured, and kept off the page.

## Round 2 (2026-10-24, seat ruling on the review nits)

The feature counts are dropped from the `what_it_is` files sentence ("The files, last modified February and March 2026, state British National Grid coordinates in metres."), which leaves only NESO's dated zone counts (60 words down to 53). `how_used` now reads "Draw NESO's land and marine publication zone files on a map" and "Group land data with the economic zones file NESO describes for SSEP modelling". Nothing else changed, and `grain` keeps its feature counts. Checks: CRLF 240/240, `cmp` clean, `parse_page_fields` and `anatomy_errors` `[]`, build wrote with no errors, detector `[]`, no em or en dashes. No new screenshots: the changes only shorten prose.
