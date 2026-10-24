---
source: "neso_data_portal"
package: "ssep-onshore-publication-zone-shapefile"
dataset_keys: ["ssep_publication_zones_files"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-15
layer_coverage: "bronze"
eligibility: "eligible"
---

# Strategic Spatial Energy Plan (SSEP) Onshore Publication Zone Shapefile

Three GIS shapefile ZIPs from NESO's Strategic Energy Planning group. They carry the zone
boundaries used to publish the draft and final **Strategic Spatial Energy Plan (SSEP)**. The
vendor's package note reads "Onshore and Offshore economic and publication zones related to the
draft and final Strategic Spatial Energy Plan (SSEP)". The three resources are the 19 land
publication zones, the 19 marine publication zones and the 17 land economic zones used for SSEP
economic modelling (resource descriptions, vendor text). The package title names only the onshore
file; the package holds all three.

gridflow treats this package as **catalogue plus download only**. It captures each ZIP to bronze
unchanged and records catalogue facts about the contents: file format, layers, coordinate
reference system, feature count and bounding box. It does not read geometry meaning into the
files and has no silver or gold output for them. It claims nothing about what a feature or a zone
represents in network terms. Use the pages as a pointer to the vendor's boundary files and as a
record of what was published when. For any spatial work, download the ZIP from the vendor link
below. For the SSEP economic zones as an attribute of GSP regions, see the current GSP Regions
version on @gis-boundaries-for-gb-grid-supply-points.md, which the vendor changelog says
associates GSPs with SSEP economic zones from `20260209`
(@../../../.planning/phases/v0.22-K-FILE/K-FILE-FACTS.md §4). That association is vendor text and
gridflow has not validated it.

- Publisher group: Strategic Energy Planning
- Registry group: strategic-energy-planning · archetype: FILE

## Files by disposition

### GIS

Every resource is a ZIP of ESRI shapefile members, uploaded to the portal (`url_type: upload`).
The download link for each is the vendor URL recorded in the catalogue snapshot
(@../../../.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json).

| Resource | Format | Capture | Id |
|---|---|---|---|
| Strategic Spatial Energy Plan (SSEP) Economic Zones Shapefile | ZIP | upload | `d5b5e32e-e605-4823-b29c-312ab12f37cd` |
| Strategic Spatial Energy Plan (SSEP) Offshore Publication Zone Shapefile | ZIP | upload | `6a9ce615-b791-46fd-8a8f-dd7b1c847c10` |
| Strategic Spatial Energy Plan (SSEP) Onshore Publication Zone Shapefile | ZIP | upload | `aa824951-880f-44cc-ac5c-7b5569dd1423` |

Vendor download links:

- Economic zones: [ssep_economic_zones.zip](https://api.neso.energy/dataset/dc958942-c5bf-428d-974d-24d7d1d1f370/resource/d5b5e32e-e605-4823-b29c-312ab12f37cd/download/ssep_economic_zones.zip)
- Offshore (marine) publication zones: [offshore_publication_zones_v5_clipped_to_coastline.zip](https://api.neso.energy/dataset/dc958942-c5bf-428d-974d-24d7d1d1f370/resource/6a9ce615-b791-46fd-8a8f-dd7b1c847c10/download/offshore_publication_zones_v5_clipped_to_coastline.zip)
- Onshore publication zones: [onshore_publication_zones_v4_master_simplified.zip](https://api.neso.energy/dataset/dc958942-c5bf-428d-974d-24d7d1d1f370/resource/aa824951-880f-44cc-ac5c-7b5569dd1423/download/onshore_publication_zones_v4_master_simplified.zip)

The package has no DOC, SILVER or held resources. There is no companion CSV, changelog or
data dictionary in the package.

## Families

### `ssep_publication_zones_files`

- Kind: files · archetype: FILE · refresh: adhoc · empty allowed: no
- files: catalogue only

All three resources sit in this one family. It has no transformer and no silver output
(registry `transformer: null`). Bronze holds one capture per resource, taken 2026-10-08.

#### Two clocks

A files family that is catalogue only has **one** clock: the vintage. There is no event time.

| Clock | Value for this family |
|---|---|
| Vintage: `ckan_last_modified` | The CKAN `last_modified` of the resource at capture. A consumer could not have seen the file before this instant, so it is the file's `available_at`. |
| Event time | None. No silver is produced and there is no temporal recipe, so no `timestamp_utc` exists. The ZIPs carry no observation timestamp that gridflow reads. |

Vintage per resource, from the capture sidecars (they equal the catalogue snapshot values for all
22 FILE-batch resources, K-FILE-FACTS §6):

| Resource | Vintage: CKAN `last_modified` | Bronze capture written |
|---|---|---|
| Onshore Publication Zone | `2026-03-03T16:32:10.339680` | 2026-10-08 11:26:56 UTC |
| Offshore Publication Zone | `2026-03-03T16:30:55.147392` | 2026-10-08 11:26:58 UTC |
| Economic Zones | `2026-02-11T11:04:12.840301` | 2026-10-08 11:27:01 UTC |

The CKAN package itself was created 2026-02-11 and last modified 2026-03-03 (snapshot
`metadata_created`, `metadata_modified`). The "last modified" timestamps record uploads and edits
on the portal. The v4, v5 and `MASTER` tokens that appear in the member names are labels inside
the files, not dates. The portal states no version number for the package
(snapshot `version` is empty). `TODO: verify` what edition of the SSEP each file corresponds to;
the vendor text says only that they relate to the draft and final plan.

#### Catalogue facts per resource

Source: `docs/neso_data_portal/gis-facts.json`
(@../../../docs/neso_data_portal/gis-facts.json), re-derived from the bronze bodies on
2026-10-15 by `gridflow gis --check` and found to agree for all three resources (K-FILE-FACTS
§3.1). Each ZIP holds exactly one shapefile layer. The method is fixed by ADR-037: the feature
count is read from the `.shx`, the bounding box from the `.shp` header and the CRS from the
`.prj`. These are file-structure facts. They do not certify that the geography is correct.

| Property | Onshore publication zones | Offshore publication zones | Economic zones |
|---|---|---|---|
| Resource id | `aa824951-880f-44cc-ac5c-7b5569dd1423` | `6a9ce615-b791-46fd-8a8f-dd7b1c847c10` | `d5b5e32e-e605-4823-b29c-312ab12f37cd` |
| Format | ZIP, 1 shapefile | ZIP, 1 shapefile | ZIP, 1 shapefile |
| Bytes | 253,690 | 433,761 | 830,975 |
| Layer path inside ZIP | `onshore_publication_zones_v4_MASTER_SIMPLIFIED/onshore_publication_zones_v4_MASTER_SIMPLIFIED.shp` | `offshore_publication_zones_v5_clipped_to_coastline/marine_publication_zones_v5_clipped_to_coastline.shp` | `ssep_economic_zones_MASTER/ssep_economic_zones_MASTER.shp` |
| Feature count | 19 | 19 | 17 |
| CRS (from `.prj`) | `British_National_Grid` | `British_National_Grid` | `British_National_Grid` |
| Bbox min x, min y, max x, max y (CRS coordinates) | `54247.034099999815, 7054.101999999955, 655653.8635, 1218618.0724999998` | `-366362.5137, -243836.70659999922, 750946.9402000001, 1557813.3973000012` | `5257.746899999678, 6614.869000000879, 655964.9758000001, 1220373.0` |
| Attribute names (DBF, in order) | `ssep_pubzn, Shape_Leng, Shape_Area` | `PUB_ZN_ID, Region, Symb_Grp, Label_Str, Label_Two, Shape_Leng, Shape_Area` | `SSEP_Zone, CENTROID_X, CENTROID_Y, Zn_Area_Ha, Shape_Leng, Shape_Area` |
| Body SHA-256 | `7d5fd8e6…b02b` (full value in `gis-facts.json`) | `51abd72e…eecd` (full value in `gis-facts.json`) | `2e978527…9270` (full value in `gis-facts.json`) |

The feature counts equal the zone counts the vendor states in each resource description (19, 19
and 17). That is a numeric agreement only. gridflow has not established that one feature is one
zone, so it makes no feature-to-zone claim. The generation-charging-zone package shows why
caution is needed: its vendor text says 27 zones while both of its files hold 28 features
(@gis-boundaries-for-gb-generation-charging-zones.md).

**Units.** The vendor publishes no data dictionary for this package. No unit is stated for the
coordinates, for `Shape_Leng`, `Shape_Area`, `CENTROID_X`, `CENTROID_Y` or for the area field
`Zn_Area_Ha`. gridflow does not infer one from a column name or from the CRS name.
`TODO: verify` the units from vendor documentation before any use.

**Sentinels.** There is no tabular parse of these files, so no null-token or sentinel handling
applies. Attribute values are not read.

**ZIP members** (complete inventories; the archives pass the zip integrity test):

| Resource | Members |
|---|---|
| Onshore | `onshore_publication_zones_v4_MASTER_SIMPLIFIED/onshore_publication_zones_v4_MASTER_SIMPLIFIED` + `{.cpg, .dbf, .prj, .sbn, .sbx, .shp, .shp.xml, .shx}` |
| Offshore | `offshore_publication_zones_v5_clipped_to_coastline/marine_publication_zones_v5_clipped_to_coastline` + `{.cpg, .dbf, .prj, .sbn, .sbx, .shp, .shp.xml, .shx}` |
| Economic | `ssep_economic_zones_MASTER/ssep_economic_zones_MASTER` + `{.cpg, .dbf, .prj, .sbn, .sbx, .shp, .shp.xml, .shx}` |

The `.shp.xml` member is the shapefile's own metadata file. gridflow has not read it for this
page. `TODO: verify` whether it documents field meanings or units.

#### Bronze

- Path pattern: `C:/gridflow-data/bronze/neso_data_portal/ssep_publication_zones_files/2026/10/08/raw_<capture-time>_<resource-id>_<sha8>.zip`, with a `.meta.json` sidecar beside each.
- Format: the vendor ZIP, byte for byte. Bronze is immutable.
- Granularity: one capture per resource. Each sidecar records HTTP status 200, the body size and
  the SHA-256, and these matched the bodies on the coverage scan (K-FILE-FACTS §6).
- Coverage: all three resources are present in bronze (reconcile coverage CLEAN, 0 missing).

#### Known issues and gotchas

- **Package title names only the onshore file.** The package also holds the offshore and
  economic zone files. Use the resource ids, not the package title, to pick a file.
- **Bounding boxes differ widely.** All three declare `British_National_Grid`, but the offshore
  bbox has negative x and y values and a much larger extent than the other two. gridflow records
  the header values as published and has not checked them against the geometry.
- **No silver, no point-in-time series.** Files families are not tabular. A consumer wanting
  "what did NESO publish as of date X" can use only the capture's `ckan_last_modified` and the
  catalogue facts. Nothing in gridflow decides which edition of the SSEP a file belongs to.
- **Third-party origin note.** The portal's package `url` field reads "Office for National
  Statistics licensed under the Open Government Licence v.3.0". The registry marks this package
  `eligible`, so it is not held. `TODO: verify` which, if any, of the three files include
  third-party geometry and what that means for reuse beyond the NESO Open Data Licence. (The
  neighbouring DNO licence-area package is held for a third-party-origin carve-out, and has no
  page: RULINGS 477.)
- **Ad hoc refresh.** The vendor update frequency is Ad-hoc. A refresh run captures whatever the
  portal serves at that time. A changed `ckan_last_modified` or SHA-256 means a new vintage.

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad-hoc
- Captures to date: one per resource (2026-10-08). No scheduled refresh has run yet.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above. See the
third-party origin note under Known issues for the unresolved package `url` field.

## Holds

- none

No output of this package is held. The only FILE-batch hold is the separate DNO licence-area
package (HOLD unit N, RULINGS 477; catalogue page @30-vendors/neso-data-portal/datasets/gis-boundaries-for-gb-dno-license-areas.md, no data published), which does not touch these files. This
package's activation produced no silver rows by design: the FILE batch wrote 380 rows for the GSP
lookup family only, and the reconcile ran clean with 0 gaps (gridflow
`@.planning/v0.22-RESULTS.md` §FILE; RULINGS 849, 850, 854, 857).
