---
source: "neso_data_portal"
package: "gis-boundaries-for-gb-grid-supply-points"
dataset_key: "gis_grid_supply_points"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-15
last_verified: 2026-10-15
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# GIS Boundaries for GB Grid Supply Points

NESO's GB grid supply point (GSP) region package. Grid supply points are where the transmission
system meets the distribution networks; the vendor describes Gnodes as the nodes NESO uses for
network modelling and monitoring (potentially many-to-many with GSPs) and Direct Connects as
demand connected directly to transmission. The package holds two different kinds of thing, and
gridflow treats them differently.

1. **A lookup table** (`GSP - Gnode - Direct Connect - Region Lookup 20181031`, CSV). It relates
   Gnodes, GSPs, Direct Connects, regions and PES / GSP groups. This is the only part gridflow
   parses: family `gis_grid_supply_points`, **380 rows** in silver, a reference table (archetype
   REG), eligible. Use it as vendor-published identifier and name context, not as a model feature.
2. **GSP Regions boundary files** (ZIP shapefile, GeoJSON, GeoPackage; eight GIS resources across
   six named versions) plus a **changelog** (TXT). These are **catalogue and download only**
   (family `gis_grid_supply_points_files`, archetype FILE). gridflow records format, layers, CRS,
   feature count and bounding box for each file as catalogue facts, and gives the vendor download
   link. **gridflow claims no geometry meaning**: the catalogue facts do not certify geographic
   correctness, and no GIS file is joined to anything.

The 2018 pairing is a version label, not a date: `20181031` names the GSP Regions version the
lookup accompanies (the vendor associates the lookup with that version and its resource
description relates it to the GIS files). The files were published on 2020-05-05. The **current**
GSP Regions version is `20260209` (GeoPackage and GeoJSON, no shapefile). "Current" means the
newest version the vendor lists, not a claim about geographic accuracy.

Attribution: **Supported by National Energy SO Open Data**. Licence: NESO Open Data Licence.

Vendor documentation: [GSP dataset page](https://www.neso.energy/data-portal/gis-boundaries-gb-grid-supply-points),
[lookup resource page](https://www.neso.energy/data-portal/gis-boundaries-gb-grid-supply-points/gsp_-_gnode_-_direct_connect_-_region_lookup_20181031),
[current GSP Regions resource page](https://www.neso.energy/data-portal/gis-boundaries-gb-grid-supply-points/gsp_regions_20260209).
Package id `2810092e-d4b2-472f-b955-d8bea01f9ec0`.

- Publisher group: System
- Registry group: system · archetype: FILE

Related pages: @gis-boundaries-for-gb-generation-charging-zones.md,
@ssep-onshore-publication-zone-shapefile.md, @etys-gb-transmission-system-boundaries.md.

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| GSP - Gnode - Direct Connect - Region Lookup 20181031 | CSV | upload | `bbe2cc72-a6c6-46e6-8f4e-48b879467368` |

### DOC

| Resource | Format | Capture | Id |
|---|---|---|---|
| GSP Regions changelog | TXT | upload | `857f8af8-e41b-4f1b-9962-2b441cd31eea` |

### GIS

| Resource | Format | Capture | Id |
|---|---|---|---|
| GSP Regions 20181031 with ESRI Shape file | ZIP | upload | `506d99a3-d4f5-4dd8-9586-652047682ccc` |
| ↳ GSP_regions_20181031.cpg | — | — | GIS |
| ↳ GSP_regions_20181031.dbf | — | — | GIS |
| ↳ GSP_regions_20181031.prj | — | — | GIS |
| ↳ GSP_regions_20181031.sbn | — | — | GIS |
| ↳ GSP_regions_20181031.sbx | — | — | GIS |
| ↳ GSP_regions_20181031.shp | — | — | GIS |
| ↳ GSP_regions_20181031.shp.xml | — | — | GIS |
| ↳ GSP_regions_20181031.shx | — | — | GIS |
| ↳ view_gsp_gnode_all_20181031.csv | — | — | HOLD: proposed family gis_gsp_lookup_archive: COVERED nomination by bbe2cc72-a6c6-46e6-8f4e-48b879467368 — byte-identical but covering published 129.559 s later (FILE) |
| GSP Regions 20181031 with GeoJson | GEOJSON | upload | `a3ed5711-407a-42a9-a63a-011615eea7e0` |
| GSP Regions 20220314 (ESRI Shapefile) | ZIP | upload | `8100d4f2-9a55-41cb-bc3c-c190de7aa0dc` |
| GSP Regions 20220314 (GeoJSON) | GEOJSON | upload | `08534dae-5408-4e31-8639-b579c8f1c50b` |
| GSP Regions 20250102 | ZIP | upload | `c798be82-d2eb-470c-a921-05f1ed91c727` |
| GSP Regions 20250109 | ZIP | upload | `d95e8c1b-9cd9-41dd-aacb-4b53b8c07c20` |
| GSP Regions 20251204 | ZIP | upload | `c5647312-afab-4a58-8158-2f1efed1d7fc` |
| GSP Regions 20260209 | ZIP | upload | `5dfab3dd-f192-40ab-b97f-b365a594293c` |

All ten resources were captured to bronze on 2026-10-08 (one capture each, HTTP 200, size and
SHA-256 verified; 10 of 10 present). The resource-name date is a vendor version label and is a
separate thing from the CKAN `last_modified` vintage in the table below.

### Resource download links

Vendor download links (the URL recorded in each bronze capture's request). Names are the vendor's.

| Resource | Disposition | Bytes | CKAN `last_modified` (vintage) | Download |
|---|---|---:|---|---|
| GSP Regions 20181031 with ESRI Shape file | GIS | 836,252 | `2020-05-05T07:51:58.241615` | [gsp_regions_20181031.zip](https://api.neso.energy/dataset/2810092e-d4b2-472f-b955-d8bea01f9ec0/resource/506d99a3-d4f5-4dd8-9586-652047682ccc/download/gsp_regions_20181031.zip) |
| GSP Regions 20181031 with GeoJson | GIS | 3,363,095 | `2020-05-05T07:53:11.324353` | [gsp_regions_20181031.geojson](https://api.neso.energy/dataset/2810092e-d4b2-472f-b955-d8bea01f9ec0/resource/a3ed5711-407a-42a9-a63a-011615eea7e0/download/gsp_regions_20181031.geojson) |
| GSP - Gnode - Direct Connect - Region Lookup 20181031 | SILVER | 34,324 | `2020-05-05T07:54:07.800829` | [gsp_gnode_directconnect_region_lookup.csv](https://api.neso.energy/dataset/2810092e-d4b2-472f-b955-d8bea01f9ec0/resource/bbe2cc72-a6c6-46e6-8f4e-48b879467368/download/gsp_gnode_directconnect_region_lookup.csv) |
| GSP Regions 20220314 (GeoJSON) | GIS | 13,409,418 | `2022-05-05T16:01:29.461187` | [gsp_regions_20220314.geojson](https://api.neso.energy/dataset/2810092e-d4b2-472f-b955-d8bea01f9ec0/resource/08534dae-5408-4e31-8639-b579c8f1c50b/download/gsp_regions_20220314.geojson) |
| GSP Regions 20220314 (ESRI Shapefile) | GIS | 2,652,817 | `2022-05-05T16:04:16.983335` | [gsp_regions_20220314.zip](https://api.neso.energy/dataset/2810092e-d4b2-472f-b955-d8bea01f9ec0/resource/8100d4f2-9a55-41cb-bc3c-c190de7aa0dc/download/gsp_regions_20220314.zip) |
| GSP Regions 20250102 | GIS | 15,257,500 | `2025-01-30T13:49:18.360535` | [gsp_regions_20250102.zip](https://api.neso.energy/dataset/2810092e-d4b2-472f-b955-d8bea01f9ec0/resource/c798be82-d2eb-470c-a921-05f1ed91c727/download/gsp_regions_20250102.zip) |
| GSP Regions 20250109 | GIS | 15,994,203 | `2025-01-30T13:50:51.687886` | [gsp_regions_20250109.zip](https://api.neso.energy/dataset/2810092e-d4b2-472f-b955-d8bea01f9ec0/resource/d95e8c1b-9cd9-41dd-aacb-4b53b8c07c20/download/gsp_regions_20250109.zip) |
| GSP Regions changelog | DOC | 7,615 | `2026-04-29T14:26:49.862724` | [gsp-regions-changelog.txt](https://api.neso.energy/dataset/2810092e-d4b2-472f-b955-d8bea01f9ec0/resource/857f8af8-e41b-4f1b-9962-2b441cd31eea/download/gsp-regions-changelog.txt) |
| GSP Regions 20251204 | GIS | 15,864,718 | `2025-12-05T15:16:09.302935` | [gsp_regions_20251204.zip](https://api.neso.energy/dataset/2810092e-d4b2-472f-b955-d8bea01f9ec0/resource/c5647312-afab-4a58-8158-2f1efed1d7fc/download/gsp_regions_20251204.zip) |
| GSP Regions 20260209 | GIS | 16,240,499 | `2026-04-29T14:30:10.464770` | [gsp_regions_20260209.zip](https://api.neso.energy/dataset/2810092e-d4b2-472f-b955-d8bea01f9ec0/resource/5dfab3dd-f192-40ab-b97f-b365a594293c/download/gsp_regions_20260209.zip) |

## Families

### `gis_grid_supply_points`

- Kind: tabular · archetype: REG · refresh: adhoc · empty allowed: yes

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| ng_id | `ng_id` | int64 | — | no | — | — |
| ggd_id | `ggd_id` | int64 | — | no | — | — |
| gnode_id | `gnode_id` | int64 | — | yes | — | — |
| gnode_name | `gnode_name` | string | — | yes | — | — |
| gnode_lat | `gnode_lat` | float64 | — | yes | — | Decimal degrees in WGS 1984 Coordinate Reference System |
| gnode_lon | `gnode_lon` | float64 | — | yes | — | Decimal degrees in WGS 1984 Coordinate Reference System |
| gsp_id | `gsp_id` | int64 | — | yes | — | — |
| gsp_name | `gsp_name` | string | — | yes | — | — |
| gsp_lat | `gsp_lat` | float64 | — | yes | — | Decimal degrees in WGS 1984 Coordinate Reference System |
| gsp_lon | `gsp_lon` | float64 | — | yes | — | Decimal degrees in WGS 1984 Coordinate Reference System |
| dc_id | `dc_id` | int64 | — | yes | — | — |
| dc_name | `dc_name` | string | — | yes | — | — |
| dc_lat | `dc_lat` | float64 | — | yes | — | Decimal degrees in WGS 1984 Coordinate Reference System |
| dc_lon | `dc_lon` | float64 | — | yes | — | Decimal degrees in WGS 1984 Coordinate Reference System |
| region_id | `region_id` | int64 | — | yes | — | — |
| region_name | `region_name` | string | — | yes | — | — |
| has_pv | `has_pv` | int64 | — | no | — | — |
| pes_id | `pes_id` | int64 | — | yes | — | — |
| pes_name | `pes_name` | string | — | yes | — | — |

- Entity key: `ggd_id`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

#### Two clocks

- **Vintage** (`ckan_last_modified`): `available_at` = `published_at` = the CKAN `last_modified` of
  the captured CSV, `2020-05-05T07:54:07.800829Z`. This is when the vendor last modified the upload,
  not when gridflow captured it, and it is not the `20181031` version label.
- **Event time**: temporal recipe is `none`. The lookup carries no event timestamp, so
  `timestamp_utc` (and `event_time`) is the **capture time**, `2026-10-08T11:04:07.596378Z`. It says
  when gridflow fetched the file and means nothing about when any row became true.

Silver also carries the standard provenance columns (`bronze_capture_id`, `capture_written_at`,
`source_run_id`, `dataset_version`, observed `1+e1`).

#### Silver state

One capture (`bronze/neso_data_portal/gis_grid_supply_points/2026/10/08/`), one silver file under
`silver/neso_data_portal/gis_grid_supply_points/year=2026/month=10/`. Activation (transform window
2026-10-08, no prior silver): **380 rows**, which equals the plan, **0 recorded failures**. Not held.

#### Physical layout of the CSV (measured on the full bronze body)

| Property | Value |
|---|---|
| Encoding | UTF-8, with a UTF-8 BOM |
| Header | first line, 19 fields, no preamble |
| Data rows | 380 (all 19 wide; no blank rows, no trailing empty columns) |
| Line terminators | CRLF throughout; final newline present |

Header, verbatim: `ng_id,ggd_id,gnode_id,gnode_name,gnode_lat,gnode_lon,gsp_id,gsp_name,gsp_lat,gsp_lon,dc_id,dc_name,dc_lat,dc_lon,region_id,region_name,has_pv,pes_id,pes_name`.

#### Column meanings, units and nulls

Meanings are paraphrased from the vendor field dictionary captured in the catalogue. Units are only
what the dictionary states: `N/A` means the vendor gives no unit (the column is an identifier, a
name or a flag), and "decimal degrees" is the vendor's WGS 1984 unit for the four coordinate pairs.
Nothing is inferred from a column name. "Null rows" counts empty CSV cells, all of which become
nulls; no strict cast failed in any column.

| Column | Vendor meaning | Vendor unit | Null rows (of 380) |
|---|---|---|---:|
| `ng_id` | Dataset-local identifier used when deriving regions | N/A | 0 |
| `ggd_id` | Identity of a lookup entity linking GSP, Gnode and licence-area information | N/A | 0 |
| `gnode_id` | Dataset-local Gnode identifier | N/A | 4 |
| `gnode_name` | NESO's preferred Gnode name | N/A | 4 |
| `gnode_lat`, `gnode_lon` | Gnode latitude and longitude | decimal degrees (WGS 1984) | 4 each |
| `gsp_id` | Dataset-local GSP identifier | N/A | 20 |
| `gsp_name` | GSP name, following Elexon settlement naming | N/A | 20 |
| `gsp_lat`, `gsp_lon` | GSP latitude and longitude | decimal degrees (WGS 1984) | 20 each |
| `dc_id` | Dataset-local Direct Connect identifier | empty unit field | 361 |
| `dc_name` | Preferred Direct Connect name | empty unit field | 361 |
| `dc_lat`, `dc_lon` | Direct Connect latitude and longitude | decimal degrees (WGS 1984) | 361 each |
| `region_id` | Identifier of a boundary record (the dictionary equates it with GIS `RegionID`) | N/A | 20 |
| `region_name` | Boundary name, usually based on a GSP name | N/A | 20 |
| `has_pv` | Vendor assessment of possible embedded solar-PV hosting; vendor type boolean | N/A | 0 |
| `pes_id` | PES / licence-area / GSP-group identifier | N/A | 20 |
| `pes_name` | Industry character code for that PES / GSP group | N/A | 20 |

Notes that bind use of the table:

- **Integer ids are dataset-local.** The vendor describes the internal numeric ids as arbitrary
  and inconsistent between versions of the data. They are **not stable across GSP Regions
  versions**, so an id from this 2018-paired lookup must not be assumed to identify the same thing
  in any later boundary file or version. gridflow stores every id and name as published.
- Gnode and GSP coordinates need not coincide.
- `has_pv` is a vendor boolean stored as `int64` (the record dtype vocabulary has no boolean), with
  values `1` in 356 rows and `0` in 24. Stored as published.
- `ng_id` and `ggd_id` are different columns and are not interchangeable (verified on a sample row
  where `ng_id` is 387 and `ggd_id` is 372).
- Sentinels: only the exact empty cell occurs as a missing marker. The probe also looked for
  whitespace-only cells and the case-folded tokens `NULL`, `NA`, `N/A`, `NaN`, `None`, `-`, `--`,
  `..`, `...`; none occur, so the record declares no extra null tokens. Missing cells stay null: no
  zero substitution, no filling from another row, no coordinate correction, no id normalisation.

#### Keys

`ggd_id` is the entity key: 380 distinct values, no nulls, no duplicates (so no deduplication is
applied and the duplicate guard passes). `ng_id` is also unique, but the vendor ties `ggd_id` to the
lookup entity itself, so it is the key. The other id columns repeat by design and are not keys:
`gnode_id` 360 distinct non-null values (4 null), `gsp_id` 338 (20 null), `region_id` 325 (20 null),
`dc_id` 17 (361 null); counts exclude the null group. The triple `(gnode_id, gsp_id, dc_id)` is unique in the file but is null-bearing in
every row and is not used.

#### Pairing with the 2018 GIS files

- The **2018 GeoJSON carries only `RegionID` and `RegionName`**. It has no GSP id property and no
  GSP name property, so there is **no GSP-id join** between the lookup and the 2018 boundaries.
  A comparison of `gsp_id` with `RegionID` is a comparison of different identifier domains and its
  numerical overlap is not evidence of identity.
- Lookup `region_id` against GeoJSON `RegionID` agree as sets: 325 distinct values on each side,
  325 in common, none on either side alone. The GeoJSON has **329 features** but only 325 distinct
  `RegionID` values: `18`, `41`, `60`, `64` each occur twice. A join on `RegionID` alone is
  therefore not one-to-one on the GeoJSON side.
- **Region-name spelling difference, kept as published on both sides:** lookup `region_name` has
  `Clyde’s Mill` while the GeoJSON `RegionName` has `Clydeâ€™s Mill` (a mis-decoded apostrophe in the
  vendor GeoJSON). Exact-string comparison agrees on 324 of 325 distinct names; this is the one
  difference. gridflow does not repair either spelling.
- TODO: verify whether the vendor issues a GSP id or GSP-to-feature mapping for the 2018 boundaries.
  Until then the lookup stands alone as a reference table and no geometry claim is made.

### `gis_grid_supply_points_files`

- Kind: files · archetype: FILE · refresh: adhoc · empty allowed: no
- files: catalogue only

There is **no silver output** for the GIS and DOC resources. Their only clock is the
`ckan_last_modified` of the capture (listed in the download-links table above). There is no event
time and no `timestamp_utc`; nothing is parsed from these files beyond the catalogue facts below.

#### Catalogue facts per GIS file

Format, layers, CRS, feature count and bounding box as derived by the gridflow GIS helper from each
bronze body and checked against `docs/neso_data_portal/gis-facts.json` (`gis --check` exit 0 at
activation: all 14 eligible GIS resources across the FILE packages, 26 layers, agree with bronze;
the 10 GSP resources here contribute 8 GIS resources). Counts come from the `.shx` (shapefile),
the JSON (GeoJSON) or SQLite metadata (GeoPackage); bounding boxes from the `.shp` header, the
coordinates or the table, ordered `(min_x, min_y, max_x, max_y)` and **rounded** here (full
precision is in `gis-facts.json`). These are catalogue facts under the helper's methods; they do
not certify geographic correctness or what any feature represents. `::` separates an inner archive
or GeoPackage file from its layer or table; an empty path is the body itself.

| Resource | Layer path | Kind | Features | CRS (as read) | CRS from | Bbox |
|---|---|---|---:|---|---|---|
| 20181031 shapefile ZIP | `GSP_regions_20181031.shp` | shapefile | 329 | `British_National_Grid` | `.prj` | `[5257.7469, 5180.0, 655964.9758, 1220373.0]` |
| 20181031 GeoJSON | body | geojson | 329 | `urn:ogc:def:crs:EPSG::27700` | `crs` member | `[5257.7469, 5180.0, 655964.9758, 1220373.0]` |
| 20220314 GeoJSON | body | geojson | 333 | `urn:ogc:def:crs:EPSG::27700` | `crs` member | `[5257.7469, 5180.0, 655964.9758, 1220373.0]` |
| 20220314 shapefile ZIP | `GSP_regions_20220314.shp` | shapefile | 333 | `British_National_Grid` | `.prj` | `[5257.7469, 5180.0, 655964.9758, 1220373.0]` |
| 20250102 ZIP | `Proj_4326/GSP_regions_20250102.zip::GSP_regions_20250102.shp` | shapefile | 340 | `GCS_WGS_1984` | `.prj` | `[-8.65472688, 49.87417088, 1.7683533, 60.8614356]` |
| 20250102 ZIP | `Proj_4326/GSP_regions_4326_20250102.geojson` | geojson | 340 | `urn:ogc:def:crs:OGC:1.3:CRS84` | `crs` member | `[-8.65472688, 49.87417088, 1.7683533, 60.8614356]` |
| 20250102 ZIP | `Proj_27700/GSP_regions_20250102.zip::GSP_regions_20250102.shp` | shapefile | 340 | `British_National_Grid` | `.prj` | `[5257.7469, 6614.869, 655964.9758, 1220373.0]` |
| 20250102 ZIP | `Proj_27700/GSP_regions_27700_20250102.geojson` | geojson | 340 | `urn:ogc:def:crs:EPSG::27700` | `crs` member | `[5257.7469, 6614.869, 655964.9758, 1220373.0]` |
| 20250109 ZIP | `Proj_4326/GSP_regions_20250109.zip::GSP_regions_20250109.shp` | shapefile | 349 | `GCS_WGS_1984` | `.prj` | `[-8.65472688, 49.87417088, 1.7683533, 60.8614356]` |
| 20250109 ZIP | `Proj_4326/GSP_regions_4326_20250109.geojson` | geojson | 349 | `urn:ogc:def:crs:OGC:1.3:CRS84` | `crs` member | `[-8.65472688, 49.87417088, 1.7683533, 60.8614356]` |
| 20250109 ZIP | `Proj_27700/GSP_regions_20250109.zip::GSP_regions_20250109.shp` | shapefile | 349 | `British_National_Grid` | `.prj` | `[5257.7469, 6614.869, 655964.9758, 1220373.0]` |
| 20250109 ZIP | `Proj_27700/GSP_regions_27700_20250109.geojson` | geojson | 349 | `urn:ogc:def:crs:EPSG::27700` | `crs` member | `[5257.7469, 6614.869, 655964.9758, 1220373.0]` |
| 20251204 ZIP | `Proj_4326/GSP_regions_4326_20251204.zip::GSP_regions_4326_20251204.shp` | shapefile | 353 | `GCS_WGS_1984` | `.prj` | `[-8.65472688, 49.87417088, 1.7683533, 60.8614356]` |
| 20251204 ZIP | `Proj_4326/GSP_regions_4326_20251204.geojson` | geojson | 353 | `urn:ogc:def:crs:OGC:1.3:CRS84` | `crs` member | `[-8.65472688, 49.87417088, 1.7683533, 60.8614356]` |
| 20251204 ZIP | `Proj_27700/GSP_regions_27700_20251204.zip::GSP_regions_27700_20251204.shp` | shapefile | 353 | `British_National_Grid` | `.prj` | `[5257.7469, 6614.869, 655964.9758, 1220373.0]` |
| 20251204 ZIP | `Proj_27700/GSP_regions_27700_20251204.geojson` | geojson | 353 | `urn:ogc:def:crs:EPSG::27700` | `crs` member | `[5257.7469, 6614.869, 655964.9758, 1220373.0]` |
| 20260209 ZIP | `Proj_4326/GSP_regions_4326_20260209.gpkg::gsp_regions` | gpkg | 362 | `EPSG:4326` | `gpkg_spatial_ref_sys` | `[-8.65472688, 49.87417088, 1.7683533, 60.8614356]` |
| 20260209 ZIP | `Proj_4326/GSP_regions_4326_20260209.geojson` | geojson | 362 | `urn:ogc:def:crs:OGC:1.3:CRS84` | `crs` member | `[-8.65472688, 49.87417088, 1.7683533, 60.8614356]` |
| 20260209 ZIP | `Proj_27700/GSP_regions_27700_20260209.gpkg::gsp_regions` | gpkg | 362 | `EPSG:27700` | `gpkg_spatial_ref_sys` | `[5257.7469, 6614.869, 655964.9758, 1220373.0]` |
| 20260209 ZIP | `Proj_27700/GSP_regions_27700_20260209.geojson` | geojson | 362 | `urn:ogc:def:crs:EPSG::27700` | `crs` member | `[5257.7469, 6614.869, 655964.9758, 1220373.0]` |

The feature count grows with each named version (329, 333, 340, 349, 353, 362); that is a count of
features in the file, and gridflow draws no conclusion about what the extra features are.

#### Archive contents

All inspected top-level and nested ZIPs pass `testzip()`. Stem plus `{.a,.b}` means every listed
extension is present.

| Resource | Members |
|---|---|
| 20181031 shapefile ZIP | `GSP_regions_20181031` + `{.cpg,.dbf,.prj,.sbn,.sbx,.shp,.shp.xml,.shx}`; `view_gsp_gnode_all_20181031.csv` |
| 20220314 shapefile ZIP | `GSP_regions_20220314` + `{.cpg,.dbf,.prj,.shp,.shx}` |
| 20250102, 20250109, 20251204 ZIPs | directories `Proj_4326/` and `Proj_27700/`; per projection one GeoJSON and one nested shapefile ZIP. Nested `Proj_4326` ZIPs hold `{.dbf,.prj,.shp,.shx}` (no `.cpg`); nested `Proj_27700` ZIPs hold `{.cpg,.dbf,.prj,.qmd,.shp,.shx}` |
| 20260209 ZIP | directories `Proj_4326/` and `Proj_27700/`; per projection one GeoPackage and one GeoJSON. **No shapefile members** (matches the vendor description and changelog) |

Every `.cpg` present decodes to `UTF-8`.

#### Attribute names per layer (names only; no interpretation)

| Layer | Attribute names |
|---|---|
| 20181031 shapefile and GeoJSON | `RegionID, RegionName` |
| 20220314 shapefile and GeoJSON; every 20250102, 20250109, 20251204 layer | `GSPs, GSPGroup` |
| 20260209 GeoJSON layers | `fid, GSPs, GSPGroup, SSEP17Zone, DSCPs, InGroup_, CDCA_I030` |
| 20260209 GeoPackage `gsp_regions` tables | `fid, geom, GSPs, GSPGroup, SSEP17Zone, DSCPs, InGroup_, CDCA_I030` |

The attribute scheme changes between 20181031 (`RegionID`/`RegionName`) and 20220314 (`GSPs`/
`GSPGroup`); the 2018 files carry no `GSPs`. gridflow does not map one scheme onto the other.
In the GeoPackage tables `geom` is the geometry column and `fid` the integer primary key.

#### Changelog (DOC) and version history

The changelog (`GSP Regions changelog`, TXT, 7,615 bytes, UTF-8, CRLF, 68 lines) is catalogued and
linked only; it is not transformed. It documents the following revisions, summarised from the
vendor's text. These are the vendor's descriptions; gridflow has not validated their network or
geometry meaning.

| Version | Vendor-described change (summary) |
|---|---|
| `20250102` | Boundaries updated from DNO publications; merged regions split; cross-border and off-NETS regions added; suspect regions removed; assignments and overlaps corrected |
| `20250109` | GSP labels reconciled against active settlement data; GSPs added or renamed; several regions split; UKPN areas improved; off-NETS labels clarified |
| `20251204` | A cross-border area added; SSEN Southern regions updated; several combined regions split |
| `20260209` | DSCP-related areas and attributes `InGroup_` and `CDCA_I030` added; GSP assignments and boundaries revised; GSPs associated with SSEP economic zones; shapefiles replaced by GeoPackage |

**The changelog covers `20250102` onward only.** It has no heading for `20181031` or `20220314` and
does not document the change between them. TODO: verify the detail of the `20181031` to `20220314`
revisions from a vendor source; until then those two versions are catalogued by name and upload
vintage only, with no revision narrative.

Version labels in the resource names: `20181031` (lookup and 2018 GIS files), `20220314`,
`20250102`, `20250109`, `20251204`, `20260209`. The vintage of each upload is its own CKAN
`last_modified`; for example `20250102` and `20250109` were both last modified on 2025-01-30, and
`20260209` shows `2026-04-29`.

#### Attribution and use

Supported by National Energy SO Open Data.

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Ad hoc

New GSP Regions versions are published by the vendor at irregular intervals (the changelog's
dated versions run `20250102`, `20250109`, `20251204`, `20260209`). The lookup is paired with the
`20181031` version; its captured CKAN `last_modified` is 2020-05-05.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

## Holds

- **No package-level hold.** The package is eligible. The lookup (`gis_grid_supply_points`) is
  published to silver with no hold. Nothing in this package is held on a data question except the
  archive child below.
- **Held child, unit FILE.** `view_gsp_gnode_all_20181031.csv` inside the 2018 shapefile ZIP is held.
  Hold question (registry, verbatim): "proposed family gis_gsp_lookup_archive: COVERED nomination by
  bbe2cc72-a6c6-46e6-8f4e-48b879467368 — byte-identical but covering published 129.559 s later".
  The embedded CSV is byte-identical to the standalone lookup (SHA-256
  `e6048a53a37a68e09b781b1151e560c73b09576bc089dcf230deb2ea5a1f44de`), but byte identity does not
  grant coverage and the standalone upload was published 129.559 s later. It stays held; its
  content is available only through the standalone lookup resource.
- **Adjacent, not part of this package:** the GB DNO licence-area files remain unpublished under a
  licence carve-out (third-party origin cited in package notes; unit N); their catalogue page is
  @30-vendors/neso-data-portal/datasets/gis-boundaries-for-gb-dno-license-areas.md (no data published). This
  page does not depend on them: the lookup's `pes_id` and `pes_name` are vendor-published columns
  of the lookup itself.

## Evidence

- Activation (2026-10-15, master `4c4b8ec`, PR #126): `gis_grid_supply_points` 380 rows, 0 failures;
  `reconcile --all` exit 0 with 0 gaps over 256 families; coverage clean (captured 1,385, missing
  0); `gis --check` exit 0. See @.planning/v0.22-RESULTS.md section "FILE".
- Registry record: @src/gridflow/connectors/neso_data_portal/registry/gis-boundaries-for-gb-grid-supply-points.json
- Catalogue facts: @docs/neso_data_portal/gis-facts.json
- Eligibility report: @docs/neso_data_portal/eligibility.md
- Batch evidence: @.planning/phases/v0.22-K-FILE/K-FILE-FACTS.md and @.planning/phases/v0.22-K-FILE/K-FILE-SPEC.md
- Rulings: 849, 850, 854, 857 in @.planning/RULINGS.md
- Paths above are relative to the gridflow repository root.
