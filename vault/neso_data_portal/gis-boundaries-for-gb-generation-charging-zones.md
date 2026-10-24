---
source: "neso_data_portal"
package: "gis-boundaries-for-gb-generation-charging-zones"
dataset_keys: ["gis_gen_charging_zones_files"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze"
eligibility: "eligible"
page:
  held: Two map files, kept whole; gridflow reads no rows from them and builds no silver table.
  title: TNUoS generation charging zones
  summary: >-
    NESO's approximate boundaries of the generation zones in Transmission Network Use of System
    (TNUoS) charging, as Shapefile and GeoJSON.
  facts:
    vendor: "NESO Data Portal, package `gis-boundaries-for-gb-generation-charging-zones`: two files"
    cadence: Ad hoc, as NESO lists it; both files were last modified 16 May 2022
    grain: "One layer of 28 features in each file, with `id`, `layer` and `path` attributes"
  landscape: power
  what_it_is: >-
    NESO's notes, as read in October 2026, count 27 TNUoS generation zones, each with its own
    tariffs; the count may change, and boundaries shift as substations are added. NESO
    calls the boundaries indicative; its charging documents prevail where the two disagree. Both
    files, last modified May 2022, contain 28 features and state WGS 84 coordinates in degrees.
  how_used:
    - Find a site's approximate TNUoS generation zone from its coordinates
    - Map zonal generation tariffs across Great Britain
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then each of the two files whole unless its
      `last_modified` is unchanged. Ingest only: gridflow builds no silver table.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=gis-boundaries-for-gb-generation-charging-zones"
      - "GET https://api.neso.energy/dataset/f72029e7-3056-4021-9493-01c58a667d7a/resource/102b90d8-db66-42d1-a305-1108b3384e62/download/tnuosgenzones.zip"
      - "GET https://api.neso.energy/dataset/f72029e7-3056-4021-9493-01c58a667d7a/resource/539a04ea-8bf3-4366-a277-49812c651cfb/download/tnuosgenzones_geojs.geojson"
    commands:
      - {run: gridflow ingest neso_data_portal gis_gen_charging_zones_files --last 24h, comment: "both files whole, bronze only"}
  related:
    - {dataset: neso_data_portal/transmission-network-use-of-system-tnuos-tariffs, note: "Onshore generator tariffs for each generation zone, by stage and year"}
    - {dataset: neso_data_portal/gis-boundaries-for-gb-dno-license-areas, note: "Licence areas NESO points to for TNUoS demand zone maps"}
    - {dataset: neso_data_portal/gis-boundaries-for-gb-grid-supply-points, note: "Grid supply point regions, another set of NESO GIS boundaries"}
    - {dataset: neso_data_portal/etys-gb-transmission-system-boundaries, note: "NESO's study boundaries across the transmission system, as a shapefile"}
---

# GIS Boundaries for GB Generation Charging Zones

This package is two downloadable map files from NESO: an ESRI Shapefile (zipped) and a GeoJSON file, both showing boundaries for the generation zones used in transmission network use of system (TNUoS) charging in Great Britain. The vendor describes the boundaries as approximate and indicative rather than exact. It also says that if the files disagree with the CUSC, the TNUoS tariff reports or the Use of System Charging Statements, those documents take precedence. gridflow treats the package as a catalogue entry plus a download: it captures the raw files into bronze, records plain facts about each file, and links to the vendor download. It builds no silver table from them and claims no meaning for the geometry. (Supported by National Energy SO Open Data.)

- Publisher group: Network charges
- Registry group: network-charges · archetype: FILE
- Package id: `f72029e7-3056-4021-9493-01c58a667d7a`
- Layer coverage: bronze only. A GIS "files" family has no silver output and no gold output; the files are held in bronze and catalogued, and nothing more.

### What gridflow claims, and what it does not

- The catalogue facts below (file format, layers, CRS, feature count, bounding box) were measured from the captured bytes by the existing GIS helper and agree with `docs/neso_data_portal/gis-facts.json`. They describe the files. They do not certify that the geography is correct.
- **27 zones vs 28 features.** The vendor package text says there are 27 TNUoS generation zones, and that the number may change over time. Both captured files contain 28 features. gridflow records the measured feature count as published and establishes no equivalence between a feature and a charging zone. Measured on the 2026-10-08 captures (2026-10-24): in both files the **first feature has no geometry** (a GeoJSON `MultiPolygon` with no coordinates; a null shape, type 0, in the shapefile) and carries `id` 1 and `layer` `GZ1`. The other 27 features each have one polygon, with `id` 1 to 27 and `layer` `GZ1` to `GZ27`, so `id` 1 appears twice. `TODO: verify` from a vendor statement why the empty feature is there; none was found in the captured material. The site page states NESO's 27 and the files' 28 features in separate sentences, without linking them, and does not mention the empty feature.
- The vendor text points to a separate package of GB DNO licence areas for the TNUoS demand zones. That package is held and unpublished (see Holds); its catalogue page (@30-vendors/neso-data-portal/datasets/gis-boundaries-for-gb-dno-license-areas.md) states the licence question and publishes no data.
- Attribute columns inside the files are listed by name only. gridflow records no meaning, unit or key for them.

## Files by disposition

### GIS

Both resources are catalogue-and-download only. Both were captured once, on 2026-10-08, with HTTP status 200 and a body size and SHA-256 that match the recorded sidecar.

| Resource | Format | Capture | Id |
|---|---|---|---|
| GB Generation Charging Zones with ESRI Shape File | ZIP | upload | `102b90d8-db66-42d1-a305-1108b3384e62` |
| GB Generation Charging Zones with GeoJSON | GEOJSON | upload | `539a04ea-8bf3-4366-a277-49812c651cfb` |

No resource in this package is a DOC, a CSV, a held resource or a silver nomination.

### Catalogue facts per file

| Fact | ESRI Shapefile (ZIP) | GeoJSON |
|---|---|---|
| Vendor download | [tnuosgenzones.zip](https://api.neso.energy/dataset/f72029e7-3056-4021-9493-01c58a667d7a/resource/102b90d8-db66-42d1-a305-1108b3384e62/download/tnuosgenzones.zip) | [tnuosgenzones_geojs.geojson](https://api.neso.energy/dataset/f72029e7-3056-4021-9493-01c58a667d7a/resource/539a04ea-8bf3-4366-a277-49812c651cfb/download/tnuosgenzones_geojs.geojson) |
| Body size | 15,399 bytes | 46,980 bytes |
| Body SHA-256 | `18fa9cffdb7c4db1e1eedd09676edd1d82087ac7ae9a3b32ccc383686101c8b2` | `1a07757853b13eddb67f98f8e1b143cfc2413a34c45fcfa12f9c1209ad107ef7` |
| Layers | 1: `TNUoSGenZones.shp` (shapefile) | 1: the file body itself (geojson) |
| Feature count | 28 | 28 |
| CRS as published | `GCS_WGS_1984` (from the `.prj` member) | `urn:ogc:def:crs:OGC:1.3:CRS84` (from the GeoJSON `crs` member) |
| Bounding box `(min_x, min_y, max_x, max_y)` | `[-6.963220489449052, 0.0, 1.7641537971959256, 58.65245217705044]` | `[-6.963220489449052, 49.946448656095164, 1.764153797195926, 58.65245217705044]` |
| Attribute names (observed order) | `id, layer, path` | `id, layer, path` |
| ZIP members | `TNUoSGenZones` + `.cpg`, `.dbf`, `.prj`, `.shp`, `.shx` | not applicable |

Notes on the facts:

- Shapefile feature counts come from the `.shx` index, the shapefile bounding box from the `.shp` header, and the CRS from the `.prj`. GeoJSON counts and bounding box come from the JSON itself. The ZIP passed its integrity test and its `.cpg` member decodes to `UTF-8`.
- The shapefile bounding box has a minimum y of `0.0`, which the GeoJSON bounding box does not (it has `49.946448656095164`). Both reproduce the committed facts exactly. The shapefile's first record is a null shape (see above), and a header box that counted it at `(0, 0)` would give this minimum y; its x range already spans 0. That is consistent, not proven: gridflow records the header as published.
- gridflow records no units for coordinates or attributes; none are stated in the vendor material it has captured. `TODO: verify` any attribute meaning from a vendor data dictionary, if one exists; none is catalogued.
- Sentinel and null-token handling does not apply: no file in this package is parsed into rows.

## Families

### `gis_gen_charging_zones_files`

- Kind: files · archetype: FILE · refresh: frozen · empty allowed: no
- files: catalogue only
- Maximum download size accepted by the connector: 536,870,912 bytes
- Transformer: none. There is no silver Parquet and no gold view for this family.

**Clocks.** A files family has no event-time column and no silver output, so its only clock is the vintage of the capture.

| Clock | Value for this family |
|---|---|
| Vintage (`ckan_last_modified`; `available_at` = the CKAN `last_modified` of the capture, per ADR-030) | Shapefile ZIP: `2022-05-16T15:06:19.632967`. GeoJSON: `2022-05-16T15:07:09.000668`. Both match the catalogue snapshot of 2026-10-06. |
| Event time (temporal recipe) | `none`. No `timestamp_utc` is produced because there is no silver output. If one ever were, it would be the capture time, not an observation time. |
| Capture time | `fetched_at` 2026-10-08, shapefile `11:04:01Z`, GeoJSON `11:04:04Z`. This is bookkeeping and is not a vendor clock. |

Neither file's name or the vendor text carries an edition date. The package is not versioned in its resource names, unlike the GSP Regions package.

## Cadence

- Registry refresh: frozen
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc
- Observed: both resources were last modified on 2022-05-16, and gridflow has captured one version of each (2026-10-08). `TODO: verify` future revisions against the portal; the vendor says the zone boundaries and zone count may change over time but gives no schedule.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

## Holds

- None for this package. It is eligible, and nothing in it is held.
- The vendor text refers readers to the GB DNO licence areas package for TNUoS demand zones. That package, `gis-boundaries-for-gb-dno-license-areas`, is held for a licence carve-out (a third-party origin cited in its package notes) and remains unpublished. Its catalogue page is @30-vendors/neso-data-portal/datasets/gis-boundaries-for-gb-dno-license-areas.md; its data is not used here.
- Provenance: activation of this batch on 2026-10-15 (receipt in the v0.22 results, section FILE) transformed no silver for this package and reconciled with zero gaps; `gis --check` reports the committed facts agree with bronze.

## References

- Registry record: `src/gridflow/connectors/neso_data_portal/registry/gis-boundaries-for-gb-generation-charging-zones.json`
- Catalogue facts: `docs/neso_data_portal/gis-facts.json` (entries for the two resource ids above)
- Eligibility report: `docs/neso_data_portal/eligibility.md` ("catalogue only" row for this package)
- Vendor package page: [GIS Boundaries for GB Generation Charging Zones](https://www.neso.energy/data-portal/gis-boundaries-gb-generation-charging-zones)
- Sibling GIS packages: @30-vendors/neso-data-portal/datasets/gis-boundaries-for-gb-grid-supply-points.md, @30-vendors/neso-data-portal/datasets/ssep-onshore-publication-zone-shapefile.md, @30-vendors/neso-data-portal/datasets/etys-gb-transmission-system-boundaries.md
