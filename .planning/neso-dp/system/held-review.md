# Held System pages: checker review (2026-10-23)

Checked against the batch file, standing instructions, the writer's report, the three canonical note diffs against `origin/master` (vault worktree `C:\gridflow-wt\vault-neso-sys`), the mirrors, the built pages, the ledger rows (43, 58, 142), the registry hold questions, the N-licence research and seat addendum (ruling 477), gridflow `client.py` (`iter_members`, `_dump_member`), the catalogue snapshot `20261006T195819Z`, bronze sidecars and bronze bodies, and silver (read only, Polars).

Gates, all rerun by me: `gridflow-build --only neso_data_portal/<lead>` wrote all three, no errors (only the repo-wide "Known issues" warning); `cmp` canonical note against mirror clean on all three; detector `[]` on all three; rendered text has no em or en dashes, arrows or middle dots and none of live, now, real-time, yet, soon, pending, planned, shipped, coming, locally, ruling, ledger, TODO, RULINGS, E-SEM, held; viewport meta and `<main>` present; the three held reasons are 16 words each. Screenshots at 1440, 1024, 768 and 390 (390 through a 390 px iframe) on my own port 9898, in `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\held-checker-sys\`; I read 1440 for all three and 390 for Pathfinder: nothing clipped or overlapping, long request URLs wrap. Server stopped by its own PID (found on port 9898 and matched to my command line); 9670 untouched. Dark mode not checked (headless flags do not switch the palette).

## Reproduced from bronze and silver

| Claim | Result |
|---|---|
| DNO: six captures on 2026-10-08, none on 16 October; `ckan_last_modified` 8 May 2024 for five files, 24 May 2024 for the PNG | Reproduced (bronze listing, sidecars). |
| DNO: the three 2024 request lines | Each equals the sidecar `request_url` of its capture exactly. The `package_show` form is the connector's. |
| Pathfinder 2026-27 files: availability 137,322 rows, utilisation 129,027 rows; same headers as 8 October | Reproduced. |
| Pathfinder: only a week of rows added, earlier rows unchanged | Reproduced as a multiset: rows up to the old last start (`2026-09-27T23:30:00+00:00`) number 132,011 and 123,987, equal to the old captures, and 0 row-count differences by group-by on all columns. 0 distinct old rows missing. 5,311 and 5,040 rows follow, over 336 starts, to `2026-10-04T23:30:00+00:00`. |
| Pathfinder: every time cell ends `+00:00`, in all eight 8 October files and both 16 October files | Reproduced on every time column (start, end, issue time, actual start or cease). Starts run from 1 April 2026, all inside British Summer Time. |
| Pathfinder: duplicate excess 7,943 and 9,650 (availability), 0 and 3 (utilisation, on `(UNIT, start)`) | Reproduced. Per-file repeats: availability in every file; utilisation 0, 1, 3,964, 0 across the four files, so "some rows repeat" is true of the table. |
| Pathfinder: no availability silver; third utilisation silver file of 129,027 rows | Reproduced (no directory; three parquet files, 16 columns). A completion-failure record for availability exists from 16 October, so the failure is observed for that capture too. |
| SOP: 4,342,464 bytes, 10,358 rows, 93 columns, `last_modified` unchanged, sidecar package `metadata_modified` `2026-10-16T19:50:11.269071` | Reproduced. |
| SOP: all 10,322 earlier targets present in the new dump with all 93 cells identical; 36 targets added; no earlier plan changed | Reproduced by join on `sop_datetime`: 0 missing, 0 differing cells, 36 added (`2026-10-08T14:15:00` to `2026-10-17T00:55:00`). |
| SOP: exactly one target after the capture instant (`2026-10-16T20:47:01`) | Reproduced: `2026-10-17T00:55:00`, cardinal point `1A`, status `Final`, version 3, created `2026-10-16T19:14:00`. The 8 October dump has none. |
| SOP: second silver file 10,358 rows, 102 columns, `available_at` `2026-10-16T20:47:01.196819Z` | Reproduced. |
| SOP: `sop_datetime` unique, no exact duplicates, time columns parse with no nulls, every target after its creation time | Reproduced. |

## Focus 1: the "Rows not shown" lines

- **DNO:** "The boundaries came from Western Power Distribution; NESO does not say it may license their reuse." Accurate against the licence-research answer ("does not state whether NESO is authorised to license the originating third-party rights"). Plain, no codes, no local data.
- **Pathfinder availability:** accurate. Nothing in the file tells repeated rows apart (duplicate excess is the same on all columns). Plain.
- **Pathfinder utilisation:** accurate on all three clauses (clock, no stated unit, repeated rows). It leaves out the blank-`Inertia` question in the registry text; the 16-word cap justifies that.
- **SOP:** accurate against the registry question. It does not repeat the forward-target clause, which is right: the page claims nothing about targets.

## Focus 2: the DNO request lines and the hold

The request lines are true: the three addresses are exactly what gridflow requested for those resources, and the `ingest` command and "each of six files whole unless its `last_modified` is unchanged" match `iter_members` (upload members skip when the newest capture carries the live `last_modified`). They render as plain text in code blocks, not links. They show no file content.

Against the hold: ruling 477 says "captured into bronze but unpublished (no vault/site page values)"; the ledger says "publish nothing, catalogue page only". A download address is not a value, so the page does not breach the ruling as worded, and I would keep the three lines. But the note itself is tighter than the ruling and now disagrees with the page (finding 1). The seat should rule once and make the note match. Recommendation: keep the requests; cut "in British National Grid coordinates" from `what_it_is` if the seat wants the page to stay literally catalogue only, otherwise reword the note (finding 1).

## Focus 3: the 16 October captures

All three claims in the brief reproduce exactly (table above). The Pathfinder 2026-27 files only gained a week of rows with earlier rows unchanged; the SOP dump changed no earlier plan, added 36 and holds one plan whose target is after the capture time. None of this reaches a page except through the note's body, where it is stated correctly and scoped.

## Verdicts

| Page | Verdict | blocker | major | nit |
|---|---|---|---|---|
| `gis-boundaries-for-gb-dno-license-areas` | APPROVE (seat to rule on finding 1) | 0 | 0 | 6 |
| `stability-pathfinder-service-information` | REVISE | 0 | 1 | 3 |
| `system-operating-plan-sop` | APPROVE | 0 | 0 | 6 |

## 1. `gis-boundaries-for-gb-dno-license-areas` (lead `gis_dno_license_areas_files`) - APPROVE

1. **nit (seat ruling needed)** note body "Why it is held" and `page.what_it_is`, `page.raw_feed.requests`. The note still says "What this page does not contain, on purpose: ... coordinate reference systems ..." and "Nothing about the file contents is published on this vault page or on the site", and the Holds section says a "yes" would add "the GIS catalogue facts". The page now prints the coordinate system and three download addresses, with a sentence in "Files by disposition" explaining that both come from NESO's text. These are true and are not file contents, but the note contradicts itself two paragraphs apart. Either keep them and change the "does not contain" sentence to "coordinate reference systems read from the files", or cut "in British National Grid coordinates". The requests can stay either way (focus 2).
2. **nit** `page.what_it_is`: "Shapefile and GeoJSON ..., with a PDF and a PNG map, in editions named `20200506` and `20240503`" reads as if each edition came in all four formats. From the registry and NESO's descriptions, 20200506 has Shapefile, GeoJSON and PDF; 20240503 has Shapefile, GeoJSON and PNG. Suggest "in two editions, `20200506` (with a PDF map) and `20240503` (with a PNG map)".
3. **nit** `page.what_it_is`: "NESO calls them probably a little outdated" is not NESO's own judgement. NESO's notes say the boundaries "come with the disclaimer" (from Western Power Distribution) that they are probably a little outdated and not 100% accurate. Suggest "they come with a warning that they are probably a little outdated".
4. **nit** `page.held`: "does not say it may license their reuse" can read as "no licence". NESO does label the package with its Open Data Licence; what it does not say is that it is authorised to license the third-party origin. Suggest "NESO does not say it is authorised to license them."
5. **nit** `page.raw_feed.note`: "the 2024 edition's files are shown" does not say why only three of six are listed. The request cap is the reason, not the hold. Suggest "six files in all; the 2024 edition's three are listed".
6. **nit** template, for the seat: "The silver tables / Rows not shown" heading on a package with no silver table, and the one-line "no silver table" in the raw-feed note, is the same shape as the approved ETYS page. Not a finding against the writer.

## 2. `stability-pathfinder-service-information` (leads `stability_pathfinder_availability_report`, `stability_pathfinder_utilisation_report`) - REVISE

1. **major** `page.what_it_is` and `page.family.members[1].differs`: the utilisation report is described as holding "start and cease instructions by settlement period" / "Start and cease instructions by unit and settlement period". It holds a row for every unit and every settlement period, and almost every row is instruction code `No` (no instruction issued in the period). Counted in the 8 October bronze: 2023-2024, 110,807 of 110,891 rows are `No`; 2024-2025, 197,543 of 198,157; 2025-2026, 257,883 of 258,388; 2026-2027, 123,929 of 123,987 (58 start or cease rows). The note says exactly this ("`No` rows carry an inertia figure", "rows without a new instruction still report service state"). A reader of the page would expect a short list of instructions and instead find a half-hourly state series. Suggest `differs`: "Each unit's instruction code by settlement period, mostly No, with issue and start or cease times and an `Inertia` figure", and in `what_it_is` "give each unit's declared availability, and its instruction code (mostly none) with start or cease times, by settlement period". The `summary` ("the instructions its control room gave them") is fine as a one-line gist but is made true by this fix.
2. **nit** `page.how_used[1]`: "Read beside NESO's inertia estimate" is not sourced, and the linked system inertia page says NESO's inertia estimates do not count Stability Pathfinder units. As written it suggests the two combine. Suggest "NESO's inertia estimate leaves these units out, NESO says" (true and more useful), or "Compare with NESO's Stability Y-1 utilisation report".
3. **nit** `page.related[2]` (system-inertia-cost): relevance to Pathfinder is not stated; it prices inertia bought by Balancing Mechanism offers, a different route from the Pathfinder contracts. Suggest the note says so ("Inertia bought by Balancing Mechanism offers, not by contract") or drop the link.
4. **nit** note body: "Six of the eight captures fail the transform ... so the availability family has 0 silver rows" is now one of ten captures (the two 16 October recaptures). The recapture paragraph covers it but this sentence is not updated. Suggest "Six of the first eight captures".

Checked and fine: facts table (eight CSV files; weekly; "about a week after delivery, NESO says" is NESO's text; grain); Grid Forming Batteries exclusion; "NESO says times are local, but each ends `+00:00`" (true of every time column in every file); the four request lines per member equal the sidecars; ingest and transform commands are valid forms and the "availability builds none" comment is true; related slugs exist in the page set and the Y-1 and system inertia notes match those pages.

## 3. `system-operating-plan-sop` (lead `system_operating_plan`) - APPROVE

1. **nit** `page.what_it_is`: "NESO's notes (6 October 2026)" is the date of the catalogue snapshot, not a date NESO gave. The note's reason ("package `metadata_modified` 2026-10-06, hence") does not hold: that field moves with every data upload (sidecars show `2026-10-08T05:50` and `2026-10-16T19:50`). The page also cannot say whether the notices still stand, and the dump holds plans to 17 October. Suggest "NESO's package notes carry a data-quality notice and a publishing-difficulties notice" with no date, or keep a date and say "as read on".
2. **nit** `page.summary`, `page.how_used[1]`: "expected output by technology" compresses each technology's three figures (expected maximum availability, expected output, expected minimum output). Suggest "expected availability and output by technology".
3. **nit** `page.raw_feed.note`: "one `package_show`, then the table's whole datastore dump ... and each PDF" joins two families. The PDFs belong to `system_operating_plan_files`, fetched by the third command with its own `package_show`. Suggest "one `package_show` per command".
4. **nit** `page.related[2]` (Quick Reserve requirement): the relation to a plan's standing reserve is not stated, and Quick Reserve is a separate product. Also the first two related entries use dataset keys (`historic_generation_mix`, `embedded_wind_solar_forecast`), which link to redirect pages, where the third uses a page slug. Suggest the page slugs (`historic-generation-mix`, `embedded-wind-and-solar-forecasts`).
5. **nit** note body, "Hold question": the first sentence still says "every target precedes the capture" (true only of the first capture) ahead of the new forward-target sentence; "Quality notes" still says rows show content "up to the capture date", now one target past. Scope both to the first capture.
6. **nit** note body, header table "Coverage in the captured body" gives 2026-10-08 ends. It is scoped by "captured body", but a second reader will not know which body. Say "first capture".

Checked and fine: grain ("One row per cardinal point's plan, at its latest version"; `sop_datetime` unique, 10,358 of 10,358); cadence ("Daily", aims to publish before each cardinal point, from NESO's notes); "one datastore table and two PDFs"; MW for every value column (vendor dictionary, with the one spelling variant noted in the body); the dump request equals the sidecar; "kept only if its body changed" matches `_dump_member` (refresh is daily, so the weekly frozen rule does not apply); the PDF requests equal the sidecars; the third command key exists in the registry; the hold line follows the registry question; the page does not claim anything about target timing. The open question on the single forward target does not touch the page: it holds the whole table and the note says so.

## Open questions from the writer, answered

1. DNO raw feed: keep the three request lines (true, point at NESO, not links); see finding 1 on the note.
2. SOP forward target: no page change needed.
3. Pathfinder transform command: keep it. It is valid for utilisation and the comment says availability builds none.

## Defects to carry (writer's, confirmed)

NESO's Pathfinder notes still say "local time in ." with the zone missing; availability 2026-2027 still repeats identical rows after the 9 October upload; the SOP resource `last_modified` is still `2023-01-24` on a dump holding plans to 17 October; a `Final` plan is in the 16 October dump before its cardinal point. No gridflow defect found.
