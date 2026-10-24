# Checker review: ssep-onshore-publication-zone-shapefile (held, bronze only)

Checked 2026-10-24 on worktrees `C:\gridflow-wt\fe-neso-sep` and `C:\gridflow-wt\vault-neso-sep`, port 9972 (server started with a recorded PID, stopped by that PID; 9670 untouched).

## Verdict: APPROVE with nits

0 blockers, 0 majors, 2 nits. Every factual claim on the page reproduces.

## What was checked and how

- **Build and gates.** `gridflow-build --only neso_data_portal/ssep_publication_zones_files` wrote the page with no errors (the repo-wide 37 dropped-caveat warning is the same count the writer reported; this note adds none). Detector `[]`. Mirror `cmp` clean. Rendered page has the viewport meta and `<main>`, no em or en dashes, arrows or middle dots, and none of Crown, Internal use, EPSG, 27700 or "Juristictions". One "Rows not shown" block.
- **Screenshots** at 1440, 1024, 768 and 390 (a 390 px iframe): nothing clipped or overlapping; the long request URLs wrap inside their boxes; the facts, raw feed, held block and related list all render.
- **Feature counts (finding 1 evidence).** Read from the three bronze ZIPs (`ssep_publication_zones_files/2026/10/08`, `testzip` clean): `.shx` records 19 / 19 / 17, `.dbf` records 19 / 19 / 17, shape type 5 (polygon) in each `.shp` header. Sizes 253,690 / 433,761 / 830,975 bytes and SHA-256 prefixes `7d5fd8e6` / `51abd72e` / `2e978527` match the sidecars and the note.
- **NESO's counts.** Catalogue snapshot `20261006T195819Z` (read 6 October 2026): onshore "The 19 land publication zones for the publication of the draft and final Strategic Spatial Energy Plan (SSEP)", offshore "The 19 marine publication zones for the publication of the draft and final ...", economic "The 17 land economic zones used for Strategic Spatial Energy Plan (SSEP) economic modelling". "As read in October 2026" is accurate.
- **Coordinates.** All three `.prj` files are the identical string `PROJCS["British_National_Grid",GEOGCS["GCS_OSGB_1936",...],PROJECTION["Transverse_Mercator"],...UNIT["Meter",1.0]]`. "State British National Grid coordinates in metres" rests on the files, not on NESO's text (NESO's text says nothing about a coordinate system).
- **Draft and final.** Appears once on the page, in the sentence attributed to NESO's file descriptions, and matches the onshore and offshore descriptions and the package notes. The page does not say which edition any file is; the note body keeps that as `TODO: verify`.
- **Held line.** Registry `ssep-onshore-publication-zone-shapefile.json`: one family `ssep_publication_zones_files`, `kind: files`, `transformer: null`, eligibility `eligible`; ledger row 128 "GIS only (3 ZIPs ...) catalogue + download", no silver rows, no held question. "Three zipped shapefiles, kept whole; gridflow reads no rows from them and builds no silver table" is true and parallels the ETYS and charging-zones held lines. The batch file's ruling (ships held because no silver table) is the seat's, not a finding.
- **Raw feed.** The three request URLs equal each sidecar's `request_url` (file names, resource ids, package id). Download rule ("each ZIP whole unless its `last_modified` is unchanged") matches `client.py` `iter_members`. Ingest command family key matches `config/sources.yaml`. `last_modified` 2026-02-11 (economic) and 2026-03-03 (onshore 16:32:10, offshore 16:30:55) match sidecars and snapshot; facts "11 February and 3 March 2026" correct. Ad hoc is the snapshot's "Update frequency: Ad-hoc".
- **Facts and related.** Vendor, cadence and grain lines are all supported. Related: the GSP note changelog row `20260209` reads "GSPs associated with SSEP economic zones"; charging zones, ETYS and DNO pages are in the page set and the links in the built page are relative and well formed. Stub `ssep_publication_zones_files.html` redirects to the package page as on other packages.
- **Note-body corrections** (diff vs `origin/master`, CRLF kept, 59 insertions / 10 deletions): the units correction is right (`.prj` states Meter; the old "no unit stated for the coordinates" was wrong). `.shp.xml` facts verified by reading all three: "Area of feature in internal units squared" is in each; the economic file's history has `!Shape_Area! / 10000` and `Zone_Area_Ha`; the onshore history starts from `resp_boundaries_lad23_buc_4326`; the offshore file carries a Crown Estate source layer titled "United Kingdom Continental Shelf (WGS84) - Juristictions" (sic), published 2023-05-25, use limitation "Internal use only". The DNO line ("its site page publishes no data") is accurate for the held DNO page. `updated:` bumped.
- **Crown Estate metadata** stays off the page and is only in the note's body and Known issues. The seat accepts that.

## Findings

1. **nit** | `page.what_it_is` sentences 1 and 2, `page.facts.grain`, `page.how_used` | No equivalence is stated: NESO's counts and the files' feature counts are in separate sentences with separate dates, and no sentence says a feature is a zone, so the rule is met. But the two triples are identical (19, 19, 17) and adjacent, so a reader will infer one feature per zone; unlike charging zones (27 against 28) nothing on the page signals that the two counts are separate facts. Evidence: counts above (the note body itself says "numeric agreement only"). Optional tightening, the writer's own option: drop the counts from the files sentence (keep them in `grain`), or keep as is under the charging-zones precedent. Not a blocker.
2. **nit** | `page.how_used` | "Draw NESO's SSEP land and marine publication zones on a map" and "Group land data by SSEP economic zone" read as the files being the zones. They use NESO's words and are the natural use, so this is the same point as finding 1 and needs no change unless finding 1 is acted on.

## Unverified (not on the page)

Which SSEP edition each file is; meaning of `v4`, `v5`, `MASTER`; units of `Shape_Leng`, `CENTROID_X/Y`, `Zn_Area_Ha`; whether the offshore "Internal use only" limitation is live. All stay out of the page text.

Dark mode not checked (headless flags do not switch the palette).
