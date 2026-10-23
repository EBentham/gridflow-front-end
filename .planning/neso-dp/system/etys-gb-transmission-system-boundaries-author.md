# ETYS GB transmission system boundaries: writer report

Page `etys-gb-transmission-system-boundaries`, table `etys_boundaries_files`. Written 2026-10-23.

## Recommendation: hold the page (written as a held one-table page)

There are no rows to show. `etys_boundaries_files` is a `files` family with `transformer: null`. NESO publishes one
zipped ESRI shapefile. gridflow captures the ZIP to bronze and records its catalogue facts, but it builds no silver
table. That leaves no eight-row frame, no notebook `query()` and no chart. A full page would mean inventing rows.

The numbers:
- 0 silver rows. No silver directory exists under `C:\gridflow-data\silver\neso_data_portal\`.
- 1 bronze capture: `etys_boundaries_files/2026/10/08/raw_20261008T105253Z_e914fcec-..._0e6dbd11.zip`, 87,714 bytes.
- 0 recaptures on 16 October (or any other day).
- The shapefile itself has 34 features.

So I wrote the page as a held one-table page (`page.held: <reason>`), following the approved
`contract-transfer-of-obligation` page ("so there is no silver table"). The page has a hero, facts, what it is, how it
is used, the raw feed with both requests, the silver section with the reason, and related pages. There is no chart, frame
or notebook, and I committed no artefacts. If the seat wants a full page instead, the only honest visual is a map of
the boundary lines. The template cannot draw one (see Template problems).

## Answers to the four questions

1. **What one row is.** There is no row in gridflow. What NESO publishes is one shapefile layer, and gridflow's
   `gis-facts.json` records 34 features. I measured the bronze ZIP myself (gridflow's code does not read records):
   - Each record is a PolyLine (shape type 3) with one part, of 39 to 518 vertices.
   - The attribute table has two text columns: `Boundary_n`, with names such as `B6`, `B7a`, `EC5`, `SC1.5`, all 34
     distinct; and `ID`, from `BND001` to `BND034`.
   - So in this file, one feature is one named boundary drawn as a single line.

   **ETYS in NESO's words** (package notes in the catalogue snapshot): "Shapefile containing name and geographical
   path data relating to ETYS (Electricity Ten Year Statement) study boundaries as used and published in the ETYS
   publication." The resource description adds that these are the boundaries "used in the ETYS 2024 publication and as
   shown on the NESO Interactive Webmap".
2. **Time fields.** None in the data: the `.dbf` has no date column. The only clock is the vendor's CKAN
   `last_modified`, `2025-06-02T08:26:28.667495`, which carries no offset. The page uses only its date, as cadence
   context ("last modified 2 June 2025"). There is no `timestamp_utc`, and I invented no clock.
3. **Captures.** One capture, on 2026-10-08 (above). Nothing was recaptured on 16 October. `dedup:` does not apply
   because there are no rows.
4. **Honest visual.** None. Held pages reject `chart`, `chart_view` and `locations`. The template's map
   (`map_svg.py` / `locations.py`) only draws Open-Meteo site points, not polylines in Web Mercator.

## Evidence

| Claim | Evidence |
|---|---|
| Files family, no transformer, one GIS resource | gridflow `connectors/neso_data_portal/registry/etys-gb-transmission-system-boundaries.json` (`kind: files`, `transformer: null`, `disposition: GIS`) |
| No silver | `ls C:\gridflow-data\silver\neso_data_portal\` has no `etys*` entry; the ledger row reads "GIS only (1 ZIP, 34 features), catalogue + download" |
| One capture, 87,714 bytes, `ckan_last_modified` 2025-06-02T08:26:28.667495 | bronze `.meta.json` sidecar |
| One `package_show`, then the file downloaded whole unless `last_modified` is unchanged | `client.py` `iter_members` (around lines 1658-1760): an upload member whose newest capture has the live `last_modified` is `unchanged` |
| Download URL | sidecar `request_url`; catalogue snapshot resource `url` |
| 34 features, CRS `WGS_1984_Web_Mercator_Auxiliary_Sphere` | gridflow `docs/neso_data_portal/gis-facts.json`, entry `e914fcec` |
| "name and geographical path data", "ETYS 2024", "Interactive Webmap", Ad hoc | catalogue snapshot `20260820T214455Z` (package `notes`, resource `description`, extras "Update frequency: Ad hoc") |
| No column dictionary | the package has one resource and no DOC resource (registry; snapshot `num_resources: 1`) |
| GSP region files are British National Grid or WGS84 | `gis-facts.json`, GSP entries (`British_National_Grid`, `EPSG:27700`, `EPSG:4326`, `CRS84`, `GCS_WGS_1984`) |
| B6 and B7 in NESO's constraint reporting | the approved `thermal-constraint-costs` note key: "B6 in NESO's Operational Transparency Forum deck of 24 June 2026", same for B7 |
| `B6` and `B7` are names in this file | `.dbf` records `BND019` (`B6`) and `BND017` (`B7`), measured from bronze |
| `--last 24h` ingest form | the same form as the approved `system-frequency-data` and `contract-transfer-of-obligation` pages |

## Body corrections (canonical note)

Two TODO bullets under "Catalogue facts (GIS)" are now resolved with facts I measured from the 2026-10-08 bronze ZIP.
Both are labelled as project measurements, not gridflow code facts:
- **What a feature represents:** a PolyLine with one part, 34 distinct `Boundary_n` values, so one named boundary per
  feature in this file. The bullet adds that NESO does not state whether these names match the constraint-table codes
  (`SCOTEX`, `SSHARN`).
- **The `.dbf` columns:** `Boundary_n` (C 254) and `ID` (C 10), with example values; UTF-8 per the `.cpg`.

I changed nothing else in the body. The other TODOs (the CKAN timezone, what `Mar25` means, when the file is next
replaced) are still open.

## Build and gates

- The mirror is copied byte for byte and `cmp` passes. The note stays CRLF (168 CRLF out of 168 lines).
- `gridflow-build --only neso_data_portal/etys_boundaries_files` wrote the page with no errors. It also printed the
  repo-wide warning that 35 caveat lines were dropped; that warning predates this page.
- The detector returns `[]`.
- Screenshots: 1440, 1024 and 768 light and dark, and 390 through a 390 px iframe. I served on port 9884 (PID 1490,
  started from Bash and stopped by that PID).
  - Nothing is clipped or overlapping.
  - The long package slug in the Vendor fact wraps cleanly at 390.
  - Chrome's dark-mode flags did not change the palette, so dark mode is effectively unchecked. The checker should
    look at it.
  - Files are in `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\etys-writer\`.
- Artefacts: none, by design for a held page.

## Unverified

- Whether the ETYS names (`B6`) and the operational codes (`SCOTEX`) refer to the same boundaries. The page only says
  that NESO's forum deck uses B6 and B7, which is evidenced on the thermal page. It claims no mapping.
- The timezone of CKAN `last_modified`. The page states only the date.

## Open questions for the seat

- Should a no-silver GIS package be a held page, or should these packages get their own form? The held label reads as
  "a question is pending", but nothing is pending here: there are no rows by design. The reason line says so plainly.
- If you want a full page: build a template feature for a boundary-line map, drawn from a committed artefact that is
  reprojected from Web Mercator. That is seat work, and it conflicts with the note's stance that gridflow claims no
  geometry meaning.

## Template problems

- No map type for polylines or polygons. `map_svg.py` draws only Open-Meteo site points from `locations.py`, so
  boundary and GIS packages cannot show their shape.
- Held pages show "Rows not shown" even when no rows exist by design. That is acceptable, but the wording assumes a hold.

## Defects

- **gridflow:** none in code. The registry, sidecar and `gis-facts.json` agree.
- **Data (vendor):** the package publishes no column dictionary for the `.dbf` (`Boundary_n`, `ID`), and the resource
  title says "2024" while the file and members say `Mar25`. These are already recorded in the note; they are not
  gridflow defects.
- **Manifest:** the lead and member are right (one table, `etys_boundaries_files`).
