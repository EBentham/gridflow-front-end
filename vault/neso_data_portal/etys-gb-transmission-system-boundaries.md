---
source: "neso_data_portal"
package: "etys-gb-transmission-system-boundaries"
dataset_keys: ["etys_boundaries_files"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-15
layer_coverage: "bronze"
eligibility: "eligible"
page:
  held: One zipped shapefile, kept whole; gridflow reads no rows from it and builds no silver table.
  title: ETYS transmission system boundaries
  summary: >-
    NESO's shapefile of the study boundaries in its Electricity Ten Year Statement (ETYS): names
    and paths, which NESO lists for ETYS 2024.
  facts:
    vendor: "NESO Data Portal, package `etys-gb-transmission-system-boundaries`: one ZIP file"
    cadence: Ad hoc, as NESO lists it; the file was last modified 2 June 2025
    grain: "One shapefile layer of 34 features, holding boundary names and paths"
  landscape: power
  what_it_is: >-
    ETYS, the Electricity Ten Year Statement, is a NESO publication. This package is one zipped
    ESRI shapefile of "name and geographical path data" for the transmission system boundaries used
    in ETYS 2024, NESO says. Its title says 2024; the file is named mar25, and NESO does not say why.
    NESO publishes no column dictionary. Coordinates are Web Mercator.
  how_used:
    - Draw the ETYS study boundaries on a map, after reprojecting from Web Mercator
    - Look up a boundary by its name, such as B6 or B7
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then the ZIP downloaded whole unless its
      `last_modified` is unchanged. Ingest only: gridflow builds no silver table.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=etys-gb-transmission-system-boundaries"
      - "GET https://api.neso.energy/dataset/997f4820-1ad4-499b-b1fe-4b8d3d7fbc72/resource/e914fcec-1dc9-4f1f-97e7-59c0d9521bea/download/etys-boundary-gis-data-mar25.zip"
    commands:
      - {run: gridflow ingest neso_data_portal etys_boundaries_files --last 24h, comment: "whole ZIP, bronze only"}
  related:
    - {dataset: neso_data_portal/thermal-constraint-costs, note: "Daily costs at boundaries NESO's forum deck calls B6 and B7"}
    - {dataset: neso_data_portal/24-months-ahead-constraint-limits, note: "Weekly capability of main boundaries, under operational codes such as SCOTEX"}
    - {dataset: neso_data_portal/day-ahead-constraint-flows-and-limits, note: "Day-ahead flows and limits across boundaries, under operational codes"}
    - {dataset: neso_data_portal/gis-boundaries-for-gb-grid-supply-points, note: "Grid supply point regions, in British National Grid or WGS84 coordinates"}
---

# ETYS GB Transmission System Boundaries

## Overview

This package is a single GIS file: a zipped ESRI shapefile of the transmission system boundaries as used in the ETYS 2024 publication and shown on the NESO Interactive Webmap. The vendor describes it as holding "name and geographical path data" for the ETYS (Electricity Ten Year Statement) study boundaries.
gridflow treats this package as a **catalogue and download only** dataset. The ZIP is captured to bronze byte-for-byte and its structural facts (layer, CRS, feature count, bounding box) are recorded as catalogue facts. There is no silver or gold output, gridflow parses no attributes out of the shapefile, and **gridflow claims no geometry meaning**: the catalogue facts do not certify geographic correctness, and no statement here says what any feature represents beyond what the vendor says.

Attribution: Supported by National Energy SO Open Data

- Publisher group: System
- Registry group: system · archetype: FILE
- Vendor package page: [ETYS GB Transmission System Boundaries](https://www.neso.energy/data-portal/etys-gb-transmission-system-boundaries)
- Package id: `997f4820-1ad4-499b-b1fe-4b8d3d7fbc72` (CKAN created 2025-05-30, package metadata last modified 2025-06-02)
- Tags (vendor): Boundaries, ETYS, GIS, Shapefiles, Subscribable
- Eligibility: eligible (gridflow repo `docs/neso_data_portal/eligibility.md`, row `etys-gb-transmission-system-boundaries`: 1 GIS resource)

## Resources and dispositions

The package has exactly one resource.

| Resource | Format | Disposition | Id | Vendor download link |
|---|---|---|---|---|
| ETYS 2024 GB Transmission System Boundaries | ZIP | GIS (catalogue + download) | `e914fcec-1dc9-4f1f-97e7-59c0d9521bea` | [etys-boundary-gis-data-mar25.zip](https://api.neso.energy/dataset/997f4820-1ad4-499b-b1fe-4b8d3d7fbc72/resource/e914fcec-1dc9-4f1f-97e7-59c0d9521bea/download/etys-boundary-gis-data-mar25.zip) |

- Vendor resource description: "This shapefile contains general geographical path and name data for the transmission system boundaries used in the ETYS 2024 publication and as shown on the NESO Interactive Webmap."
- There are no DOC resources in this package: no changelog, dictionary or readme file is published alongside the ZIP.
- Nothing in the package is held. The `GIS` disposition means the file is captured and its catalogue facts recorded; it does not mean gridflow interprets the geometry.

## Files by disposition

### GIS

| Resource | Format | Capture | Id |
|---|---|---|---|
| ETYS 2024 GB Transmission System Boundaries | ZIP | upload | `e914fcec-1dc9-4f1f-97e7-59c0d9521bea` |

## Families

### `etys_boundaries_files`

- Kind: files · archetype: FILE · refresh: adhoc · empty allowed: no
- files: catalogue only
- Maximum download size guard: 536,870,912 bytes (512 MiB) per file; the captured ZIP is 87,714 bytes.
- Transformer: none. There is no silver table, no gold view and no row count for this family.

## Catalogue facts (GIS)

Measured from the bronze capture and recorded in `docs/neso_data_portal/gis-facts.json`; the activation `gis --check` found that file in agreement with bronze for all 14 eligible GIS resources (26 layers), including this one. These are structural facts only.

| Property | Value |
|---|---|
| File format | ZIP containing one ESRI shapefile |
| Layers | 1: `ETYS boundary GIS data Mar25.shp` (shapefile) |
| CRS | `WGS_1984_Web_Mercator_Auxiliary_Sphere` (read from the `.prj`) |
| Feature count | 34 (from the `.shx`) |
| Bounding box (min_x, min_y, max_x, max_y, in the layer's own CRS coordinates) | `[-815124.4696802108, 6482471.494731223, 333571.19147581735, 8247249.603765618]` (from the `.shp` header) |
| ZIP members | `ETYS boundary GIS data Mar25` with extensions `.cpg`, `.dbf`, `.prj`, `.shp`, `.shx` |
| ZIP integrity | `testzip()` returned `None` (no bad member) |
| Bytes | 87,714 (declared content length equals actual body length) |
| Body SHA-256 | `0e6dbd110a5d87cd53982dc0a5fdf80badb3c86d5ab10c8c4702fcbbc02f6433` |
| HTTP status of capture | 200, content type `application/zip` |

- Feature count 34 is the number of shapefile records. In the 2026-10-08 capture every record is a PolyLine (`.shp` shape type 3) with one part (39 to 518 vertices), and the 34 `Boundary_n` values are all distinct, so in this file one feature is one named boundary drawn as a single line (measured by the project from the bronze ZIP on 2026-10-23; gridflow's code does not read records). Whether these names match the codes in NESO's constraint tables (`SCOTEX`, `SSHARN`) is not stated by the vendor.
- The bounding box is in Web Mercator coordinates, not latitude/longitude. gridflow does not reproject it.
- The attribute table (`.dbf`, UTF-8 per the `.cpg`) has two text columns: `Boundary_n` (width 254; values such as `B6`, `B7a`, `EC5`, `NW2`, `SC1.5`) and `ID` (width 10; `BND001` to `BND034`). Measured by the project from the 2026-10-08 capture; gridflow has not read them and the vendor publishes no dictionary, so their meaning beyond "name" is not stated.

## Bronze

- Path: `C:\gridflow-data\bronze\neso_data_portal\etys_boundaries_files\2026\10\08\raw_20261008T105253Z_e914fcec-1dc9-4f1f-97e7-59c0d9521bea_0e6dbd11.zip` (plus the sibling `.meta.json` sidecar).
- Captured: 2026-10-08T10:52:53Z (HTTP 200). One capture; bronze coverage for the FILE batch is clean (22 of 22 resources across the four eligible packages and the held DNO package present).
- The sidecar records `ckan_last_modified`, `ckan_format`, `url_type: upload`, `resource_filename: etys-boundary-gis-data-mar25.zip`, the body hash and `empty_capture: false`.
- Bronze is immutable. The ZIP is stored as-received.

## Silver and gold

None. GIS `files` families have no silver output (no transformer, no schema, no dedup key), so there is no gold artefact either. Activation transformed no rows for this package; the `transform` step has nothing to do for it.

## Clocks

| Clock | Value for this family |
|---|---|
| Vintage (`ckan_last_modified`; `available_at` = the CKAN `last_modified` of the capture) | `2025-06-02T08:26:28.667495`, as printed by the vendor and stored in the sidecar. TODO: verify the timezone of this CKAN string; it carries no offset. |
| Event time (temporal recipe) | `none`. There is no silver output, so there is no `timestamp_utc`; where one would exist it would be the capture time, not a time the vendor attaches to the boundaries. |

Because GIS families have no silver output, their clocks are the capture's `ckan_last_modified` only. Point-in-time use is by that vintage: a capture is available from its `ckan_last_modified`, and a later upload with a later `last_modified` would be a new capture rather than an edit of this one.

The label "2024" in the resource name is the ETYS publication year the file supports. The download name and the shapefile members say `Mar25`. Neither is a timestamp gridflow uses; the CKAN vintage is the clock. TODO: verify what `Mar25` denotes (the member name suggests a March 2025 data revision, but the vendor does not say).

## Units, sentinels and nulls

- Units: none stated. The vendor publishes no data dictionary for this package, so no unit is asserted for any attribute, and none is inferred from a column name. The bounding box above is in the layer's declared CRS coordinates.
- Sentinels: no sentinel handling applies. No tabular value from this package reaches silver, so no null-token or sentinel rule is configured for it.
- Row counts: not applicable (no silver table).

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc
- The package metadata was last modified 2025-06-02 and the resource last modified at the same minute. TODO: verify when the next ETYS publication will replace this file; the vendor gives no schedule.

## Known issues and gotchas

- Treat the shapes as opaque. The file holds one name per feature (measured, see Catalogue facts), but no claim is made that the lines are geographically correct or that they are the boundaries in NESO's constraint tables. The page's B6 and B7 forum-deck line comes from the thermal constraint costs note (@30-vendors/neso-data-portal/datasets/thermal-constraint-costs.md): NESO's Operational Transparency Forum slides of 24 June 2026 ([document 383631](https://www.neso.energy/document/383631/download), "Transparency | Network Congestion" table) present `B6 (SCOTEX)` and `B7 (SSHARN)` as aliases. That deck is not evidence that this file's `B6` and `B7` are the same boundaries.
- The CRS is Web Mercator, unlike the British National Grid or WGS84 used by sibling GIS packages in this vendor (for example the GSP regions and the generation charging zones). Do not mix bounding boxes or coordinates across packages without reprojecting; gridflow does not.
- The resource is titled "2024" but its download and members are named `Mar25`; the vintage clock is 2025-06-02.
- The ZIP is the only copy. If NESO overwrites the upload at the same URL, a later capture gets a new `ckan_last_modified` and a new hash; earlier bronze is kept.

## Licence and attribution

- Licence: NESO Open Data Licence ([licence terms](https://www.neso.energy/data-portal/ngeso-open-licence))
- Attribution: Supported by National Energy SO Open Data

## Holds

- none (no held outputs in this package; the GIS disposition is catalogue and download only).
- Note for context: the sibling package `gis-boundaries-for-gb-dno-license-areas` is held (licence carve-out; catalogue page @30-vendors/neso-data-portal/datasets/gis-boundaries-for-gb-dno-license-areas.md, no data published); it is unrelated to this package.

## Links

- Registry record: `src/gridflow/connectors/neso_data_portal/registry/etys-gb-transmission-system-boundaries.json` (in the gridflow repo)
- GIS catalogue facts: `docs/neso_data_portal/gis-facts.json` (in the gridflow repo)
- Activation receipt: `.planning/v0.22-RESULTS.md`, section "FILE" (reconcile `--all` exit 0, 256 families, 0 gaps; `gis --check` exit 0)
- Vendor package page: [ETYS GB Transmission System Boundaries](https://www.neso.energy/data-portal/etys-gb-transmission-system-boundaries)
