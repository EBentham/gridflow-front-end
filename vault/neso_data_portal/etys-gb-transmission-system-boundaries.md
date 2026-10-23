---
source: "neso_data_portal"
package: "etys-gb-transmission-system-boundaries"
dataset_keys: ["etys_boundaries_files"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-15
layer_coverage: "bronze"
eligibility: "eligible"
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

- Feature count 34 is the number of shapefile records. TODO: verify what a feature represents (a boundary, a boundary segment, or a named boundary with multiple parts); the vendor says only that the file holds study boundaries, and gridflow has not established a feature-to-boundary equivalence.
- The bounding box is in Web Mercator coordinates, not latitude/longitude. gridflow does not reproject it.
- TODO: verify the attribute (`.dbf`) column names and their meaning; gridflow has not read them and the vendor publishes no dictionary for this file.

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

- Treat the geometry as opaque. No claim is made that the 34 features correspond one-to-one to named ETYS boundaries or that the shapes are geographically correct.
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
