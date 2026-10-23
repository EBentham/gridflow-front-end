# Held System pages: writer report (2026-10-23)

I wrote three held pages using the author brief's held mode and ruling 6. None has a chart, frame or notebook, and I
committed no artefacts. Each `page:` block is on the canonical note in
`C:\gridflow-wt\vault-neso-sys\30-vendors\neso-data-portal\datasets\` and is mirrored byte for byte to
`C:\gridflow-wt\fe-neso-sys\vault\neso_data_portal\` (`cmp` is clean on all three). **Line endings:** these three notes
were LF, not CRLF, before I edited them (0 CR on every line). I kept LF so the diff carries no line-ending change.
`updated:` is now 2026-10-23 on all three.

| Page | Build `--only` | Detector | Content-model check |
|---|---|---|---|
| `gis-boundaries-for-gb-dno-license-areas` | `neso_data_portal/gis_dno_license_areas_files`: wrote, no errors | `[]` | `parse_page_fields` and `anatomy_errors`: `[]` |
| `stability-pathfinder-service-information` (family, `held: true`) | `neso_data_portal/stability_pathfinder_availability_report`: wrote, no errors | `[]` | `[]` |
| `system-operating-plan-sop` | `neso_data_portal/system_operating_plan`: wrote, no errors | `[]` | `[]` |

The builds print only the known repo-wide warning (35 "Known issues" lines dropped).

Rendered text of all three, checked by script:
- 0 em or en dashes.
- None of live, now, real-time, yet, soon, pending, planned, shipped, coming, locally, ruling, ledger, TODO, RULINGS or E-SEM.
- The viewport meta and `<main>` are present.
- There is one "Rows not shown" block, which lists each table with its reason.
- No capture date, size or row count on any page.

Two first-draft words were caught and changed: "PV_Live" (it tripped "live") and "planned".

Screenshots: light mode at 1440, 1024 and 768, and 390 through a 390 px iframe. They are in
`C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\held-sys-writer\`.
- Nothing is clipped or overlapping.
- Long request URLs, package slugs and member keys wrap at 390 and 768.

Server: started from Bash on 9888 (PID 4857) and stopped by that PID; 9670 was not touched. Dark mode was not checked:
headless flags do not switch the palette, as the ETYS writer found.

## Shared evidence

| Claim | Evidence |
|---|---|
| Upload files: one `package_show`, then each file downloaded whole unless `last_modified` is unchanged | gridflow `connectors/neso_data_portal/client.py` `iter_members` (about lines 1658-1770) |
| A datastore dump is downloaded each run and kept only if its body changed | same, lines 1664-1667 and `_dump_member` |
| Hold lines | registry `eligibility.question` of each family; ledger rows 43, 58 and 142 |
| Vendor wording (notes, descriptions, update frequency) | catalogue snapshot `.planning/research/neso-catalog-20261006T195819Z/catalog-snapshot.json` (gridflow repo) |
| Request URLs | bronze sidecar `request_url` of the newest capture of each file; `package_show` form as on the approved pages |
| `--last 24h` command form | same form as the approved held pages |
| Related targets exist | all are in `site/hifi/data/neso_data_portal.json` groups |

## 1. DNO licence area boundaries (`gis_dno_license_areas_files`)

**Reason (16 words):** "The boundaries came from Western Power Distribution; NESO does not say it may license their reuse."

| Claim | Evidence |
|---|---|
| Held for licence | registry question "third-party origin cited in package notes; licence carve-out"; ledger row 142 ("publish nothing, catalogue page only") |
| 14 DNOs, each with one licence area; "sometimes referred to as GSP Groups" | package notes |
| First shared by Western Power Distribution; "probably a little outdated and not 100% accurate" | package notes (paraphrased) |
| Shapefile and GeoJSON in British National Grid (EPSG:27700); PDF and PNG "suitable for print" | resource descriptions; a vendor statement, not read from the files |
| Editions named `20200506` and `20240503` | resource names; the page says "named", not "dated", because their meaning is a TODO in the note |
| Last modified in May 2024 (8 May for five files, 24 May for the PNG) | sidecar `ckan_last_modified` |
| Ad hoc | extras "Update Frequency: Ad hoc" |
| Uses: aggregation by licence area such as Elexon settlement data; regional modelling such as the University of Sheffield's regional estimates | package notes |
| No silver; ingest only | registry `kind: files`, `transformer: null` |
| Six captures on 2026-10-08, none on 16 October | bronze listing |

**Raw feed:** `package_show` plus the three `20240503` files. The one-table limit is four requests and the package has six
files, so the note says "the 2024 edition's files are shown".

**Body corrections:**
- The sentence "gridflow does not link any of the six files individually" is now "gridflow republishes none of the six
  files". It adds that the site page prints NESO's own download requests for the three `20240503` files.
- The CRS on the page is NESO's resource wording, not a fact read from the files. This keeps the note's no-file-content
  rule.

## 2. Stability Pathfinder (`stability_pathfinder_availability_report` lead, `stability_pathfinder_utilisation_report`)

**Reasons:**
- **Availability:** "Times end `+00:00` though NESO says local time; identical rows repeat, and nothing tells them apart."
- **Utilisation:** "Times end `+00:00` though NESO says local time; `Inertia` has no stated unit; some rows repeat."

| Claim | Evidence |
|---|---|
| Hold topics: clock, `Inertia` unit, row identity | registry questions; ledger row 58 |
| "indicative", per settlement period, "all contracted units", "local time in ." (the zone name is missing in NESO's text) | package notes |
| Updated about a week after delivery; Grid Forming Batteries excluded | package notes |
| Availability "as declared" to the control room, with remarks on changes; utilisation start and cease instructions | resource descriptions |
| Every period start ends `+00:00` | measured on bronze, both 2026-2027 captures (and the note for the older files) |
| `Inertia` has no unit in the field-info | note "Units", unchanged |
| Repeats: availability in every file; utilisation in 2024-2025 and 2025-2026 | note tables; new captures re-measured |
| Eight CSVs, four per table, financial years 2023-2024 to 2026-2027 | registry resources |
| Weekly | extras "Update frequency: Weekly" |

**Commands:** the transform line uses the utilisation key, with the comment "availability builds none", because every
availability capture fails `DuplicateEntityKeyError` and no availability silver directory exists.

**Body corrections:** a new "Recapture of the 2026-2027 files (2026-10-16)" paragraph, all measured on bronze on
2026-10-23:
- **Availability file:** 9,967,333 bytes, 137,322 rows, `last_modified` `2026-10-09T11:59:40.725801`.
- **Utilisation file:** 9,062,177 bytes, 129,027 rows, `last_modified` `2026-10-09T11:59:11.232115`.
- The headers are the same as before.
- Every distinct earlier row is unchanged, and the row count is the same up to the old last period start. One more week
  follows (starts to `2026-10-04T23:30:00+00:00`).
- Every start still ends `+00:00` and falls in British Summer Time.
- Duplicate excess: 7,943 and 9,650 for availability; 0 and 3 for utilisation.
- The utilisation capture became a third silver file of 129,027 rows.

Three existing lines were updated to match:
- Cadence: "Captures to date ... No scheduled refresh has run yet" is replaced.
- The current-year vintages now give both capture dates, and the paragraph adds that the 2026-2027 files only gained a
  week of rows.
- The Holds silver count now includes the third file.

## 3. System operating plan (`system_operating_plan`)

**Reason (16 words):** "NESO returns each plan's latest version and does not say when those figures were made public."

| Claim | Evidence |
|---|---|
| Hold | registry question (latest version; not shown fixed and public at creation); ledger row 43 |
| Plan per cardinal point; handed over; the team "if required modify"; aim to publish `1A`, `1B`, `2F/A/B`, `3B`, `3C`, `4B` ahead of each point | package notes |
| Quality notice and publishing-difficulties notice | package notes in the catalogue snapshot; package `metadata_modified` `2026-10-06T19:30:14`, hence "NESO's notes (6 October 2026)" |
| MW for every value column | vendor dictionary, as in the note's schema table |
| One row per plan at its latest version | note "Row meaning"; `latest_version` column |
| Daily | extras "Update Frequency: Daily" |
| Requests: dump, plus the introduction and glossary PDFs | sidecars (dump 16 October; PDFs 8 October) |
| PDFs are a separate family | registry `system_operating_plan_files` (`kind: files`), hence the third command |

**Body corrections:** the 16 October capture, measured on bronze and silver on 2026-10-23:
- 4,342,464 bytes, 10,358 rows, the same 93 columns, the same stale `last_modified`, and package
  `metadata_modified` `2026-10-16T19:50:11.269071`.
- It became a second silver file of 10,358 rows and 102 columns, with `available_at` = `2026-10-16T20:47:01.196819Z`.
- The time columns parse with no nulls. `sop_datetime` alone is unique, there are no exact duplicates, and every target
  follows its creation time.
- **One target, the last (on 2026-10-17), falls after the capture instant.**
- All 10,322 earlier targets are present with all 93 cells identical, and 36 targets are new. This shows no change to
  a past plan over eight days. It says nothing about revisions before a target.

"Every target precedes the capture" is now scoped to the first capture, in the overview and the hold paragraph. The
cadence line now lists both captures.

## Unverified

- **DNO:** what the edition stamps mean (still a TODO in the note). The page only says "named".
- **Pathfinder:** the time zone NESO intended ("local time in ." in its text). The page says "local", as NESO does.
- **Pathfinder:** whether "Units ... provide a stability service" fully captures the contract. The note's TODO on the
  mechanism stays.
- **SOP:** whether NESO's two notices are still on the live package page. The page dates them to the 6 October 2026
  notes. I made no live call.

## Open questions for the seat

1. **DNO raw feed.** The licence hold's note said gridflow links none of the files. The page now prints NESO's download
   requests for the three `20240503` files, as every raw feed does. These point at NESO; nothing is republished. If the
   seat reads ruling 477 as forbidding even NESO's URLs, cut `requests` to the `package_show` line only. The count is 1
   to 4, so that passes.
2. **SOP forward target.** The 16 October capture holds one target after its capture instant. Whether the forward-target
   rule could release that single row is not ruled. The page holds the whole table, and the note says so.
3. **Pathfinder transform command.** I showed the utilisation key, because the availability transform fails on every
   capture. If the seat prefers ingest only, drop the second command.

## Template problems

None new. The held mode rendered all three as expected. The family page lists both members' four files and prints both
reasons under "Rows not shown".

## Defects

- **NESO, Stability Pathfinder package notes:** "Time values are all given in local time in ." The zone name is missing,
  and every time cell carries `+00:00`. Already in the note and the hold; still present in the 2026-10-16 capture.
- **NESO, Stability Pathfinder availability report 2026-2027:** identical complete rows still repeat after the 9 October
  2026 upload (duplicate excess 7,943 on all columns), and the misspelt flag `Unvailable` still appears once. Every
  availability capture still fails `DuplicateEntityKeyError`, so this table has no silver.
- **NESO, System Operating Plan:** the resource `last_modified` is still `2023-01-24T00:30:04.725185` on the 2026-10-16
  dump, which holds plans up to 2026-10-17. It cannot be used for freshness (already noted).
- **NESO, System Operating Plan:** a plan with status `Final` was in the dump before its cardinal point, in the
  2026-10-16 capture. Recorded for the hold question, not a gridflow defect.
- **gridflow:** none. Registry, sidecars, silver and connector agree.
- **Manifest:** the leads and members are right: `gis_dno_license_areas_files`; `stability_pathfinder_availability_report`
  then `stability_pathfinder_utilisation_report`; `system_operating_plan`. The SOP PDF family
  `system_operating_plan_files` is not in `package_tables`. That is correct for a catalogue-only DOC family, and its PDFs
  appear in the raw feed.
