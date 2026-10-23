---
source: "neso_data_portal"
package: "gis-boundaries-for-gb-dno-license-areas"
dataset_keys: ["gis_dno_license_areas_files"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-16
layer_coverage: "bronze"
eligibility: "held"
---

# GIS Boundaries for GB DNO Licence Areas

**This package is held. gridflow publishes no data values, previews, geometry facts or sample rows for it.** The page exists so the NESO Data Portal catalogue is complete (owner ruling 879); it records what the package is, what gridflow holds in bronze, and the single licence question that stands between the package and publication.

The package is a set of six downloadable files from NESO: map boundaries of the Distribution Network Operator (DNO) licence areas of Great Britain, offered as zipped ESRI Shapefiles, GeoJSON files and two picture or PDF renderings, in two editions named `20200506` and `20240503`. The vendor describes the boundaries as originally shared by Western Power Distribution and warns that they are not fully accurate. gridflow treats the package as a catalogue entry: the raw files are captured into bronze and nothing further is done with them. No silver table, no gold view and no activation exists for it, so this page has no results section.

Vendor page: [GIS Boundaries for GB DNO Licence Areas](https://www.neso.energy/data-portal/gis-boundaries-gb-dno-license-areas) (the vendor's own portal page; gridflow hosts none of the files).

- Publisher group: System
- Registry group: system · archetype: FILE
- Package id: `0e377f16-95e9-4c15-a1fc-49e06a39cfa0`
- Layer coverage: bronze only. The files are held in bronze, catalogued and not published.

## Why it is held

The package description names a third party (Western Power Distribution) as the original source of the boundaries, and the package carries the NESO Open Data Licence label. That licence excludes third-party rights the information provider is not authorised to license. Nothing gridflow has found shows whether NESO is authorised to license the originating rights for public republication. The ratified catalogue snapshot (`20261006T195819Z`) shows `license_id: "ESO"`, title `NESO Open Data Licence`, and no permission or restriction text in the package notes or in any resource description beyond the origin and accuracy wording. Ruling 477 therefore kept this package as HOLD(N): it is captured but unpublished for v0.22, and lifts only on a NESO statement.

The exact question, as written for NESO (packet section 4.1, group J, shared with the other licence-held package):

> "The Levelised Cost of Green Hydrogen package cites Bloomberg NEF, Aurora Energy Research and IEA among its sources, and the GIS boundaries for GB DNO licence areas package names Western Power Distribution as its source; both are labelled NESO Open Data Licence. Is NESO authorised to license those inputs, so that a third party may republish the files under the Open Data Licence with the attribution 'Supported by National Energy SO Open Data'?"

Disposition of the answer: ask NESO (owner decision: yes). Until NESO answers, nothing about the file contents is published on this vault page or on the site.

What this page does not contain, on purpose: feature counts, bounding boxes, coordinate reference systems, attribute names or values, DNO names read from the files, preview images, ZIP member listings or any other fact derived from the file contents. Only registry metadata and bronze capture sidecar fields (names, formats, sizes, hashes, timestamps) are given below.

## Files by disposition

Six resources, all uploads, all in one family. None is individually held at resource level; the whole package is held.

### DOC

| Resource | Format | Capture | Id |
|---|---|---|---|
| GB DNO Licence Areas 20200506 | PDF | upload | `af79a476-33b0-42a3-8c6d-1c578d844cc3` |
| GB DNO Licence Areas 20240503 | PNG | upload | `26d1b3b3-2ea7-4681-bbd0-8fc7f574c6db` |

### GIS

| Resource | Format | Capture | Id |
|---|---|---|---|
| GB DNO Licence Areas 20200506 with ESRI Shape File | ZIP | upload | `46a7b674-49f9-4ad6-b778-df48f6736222` |
| GB DNO Licence Areas 20200506 with GeoJson | GEOJSON | upload | `e96db306-aaa8-45be-aecd-65b34d38923a` |
| GB DNO Licence Areas 20240503 with ESRI Shape File | ZIP | upload | `668df251-b8a5-4ac3-8427-20b93b2f5f67` |
| GB DNO Licence Areas 20240503 with GeoJson | GEOJSON | upload | `1c6a7dc0-1b6c-443a-bc67-5f7125649434` |

The DOC and GIS dispositions are the registry's. gridflow does not link any of the six files individually; to obtain them, use the vendor page above. `TODO: verify` what the edition stamps `20200506` and `20240503` in the resource names denote (effective date, publication date or file date); no vendor statement was found.

### What bronze holds

Each resource was captured once, on 2026-10-08 between 11:03:43Z and 11:03:57Z, with HTTP status 200 and a body size that equals the vendor's declared content length. Sizes and hashes come from the bronze sidecars. No capture was empty.

| Resource id (short) | Format | Body size (bytes) | Body SHA-256 | `ckan_last_modified` |
|---|---|---|---|---|
| `46a7b674` (2020 Shapefile) | ZIP | 716,425 | `1d7a9c70d3c9890310a463cad58f336d4b1d02361bf0838f9750cfa6914180b5` | 2024-05-08T11:52:07.166219 |
| `af79a476` (2020 rendering) | PDF | 650,346 | `7990d5878894700419c7a2d81777ab2b8be641db05df889c7d124f898c644f24` | 2024-05-08T11:51:46.035675 |
| `e96db306` (2020 GeoJSON) | GeoJSON | 3,006,882 | `fca19fbc551376a84f402e4ceef02fff1452fcbf9d9d91c0e5884d611456710b` | 2024-05-08T11:51:23.868845 |
| `668df251` (2024 Shapefile) | ZIP | 718,128 | `83f5cb9241f9d493bde404a9712d82bbd2fc9e780b1a5e0f5c96c4c3ac3dd358` | 2024-05-08T11:54:50.115016 |
| `1c6a7dc0` (2024 GeoJSON) | GeoJSON | 3,079,547 | `871d0b42c05fef95e2f3d4db2393be969489fbca45079bf83d96d160643ca5c2` | 2024-05-08T11:57:08.460183 |
| `26d1b3b3` (2024 rendering) | PNG | 866,495 | `52a826bb65b18c402ee91d319cc8de53db7290c915c0ef3c11e94aaebc888e21` | 2024-05-24T10:38:52.719744 |

The sidecars sit beside each bronze file under `bronze/neso_data_portal/gis_dno_license_areas_files/2026/10/08/`. Total captured: 9,037,823 bytes. The bytes are immutable and are not published anywhere.

## Families

### `gis_dno_license_areas_files`

- Kind: files · archetype: FILE · refresh: adhoc · empty allowed: no
- files: catalogue only
- Maximum download size accepted by the connector: 536,870,912 bytes
- Transformer: none. There is no silver Parquet and no gold view for this family, and no activation was run: the v0.22 results ledger has no row for this package.

**Clocks.** A files family has no event-time column and no silver output, so only the vintage clock applies.

| Clock | Value for this family |
|---|---|
| Vintage (`ckan_last_modified`; `available_at` = the CKAN `last_modified` of the capture, per ADR-030) | Per resource, as in the table above. Five resources were last modified on 2024-05-08; the 2024 PNG on 2024-05-24. |
| Event time (temporal recipe) | `none`. No `timestamp_utc` is produced because there is no silver output; if one ever were, it would be the capture time, not an observation time. |
| Capture time | `fetched_at` 2026-10-08, 11:03Z. Bookkeeping, not a vendor clock. |

Units: none are stated in any vendor dictionary gridflow has, and none are claimed. Sentinel and null-token handling does not apply: no file in this package is parsed into rows.

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Ad hoc

## Licence and attribution

- Licence: NESO Open Data Licence (snapshot `license_id` `ESO`)
- Attribution: Supported by National Energy SO Open Data
- Third-party status: the package names Western Power Distribution as the original source. Whether NESO may license that origin for republication is unresolved (see Why it is held). The package's own text states an accuracy limitation but no republication restriction.
- Completeness of the "no restriction" finding: the package page and snapshot notes and descriptions were checked; the original research could not read the live CKAN response and inspected only one of the six resource pages directly, so the resource-level finding rests on the snapshot. `TODO: verify` against the live `package_show` response.

## Holds

- package: held: third-party origin cited in package notes; licence carve-out (unit N)
- Question: the group J question quoted above, unanswered at 2026-10-16.
- Outputs held: all of them. No silver or gold output exists; the bronze captures are retained and unpublished; this page carries no file-content facts.
- To lift: a NESO statement that the origin inputs are licensed for republication under the NESO Open Data Licence. On a yes, a follow-up unit would add the GIS catalogue facts (as done for the eligible GIS packages) and refresh this page and the site mirror.
- Related: the generation charging zones page says the vendor text points to a separate DNO licence-areas package for the TNUoS demand zones; this package is presumably that one (`TODO: verify`), and it remains unpublished.

## Links

- Vendor page: [GIS Boundaries for GB DNO Licence Areas](https://www.neso.energy/data-portal/gis-boundaries-gb-dno-license-areas)
- Licence: [NESO Open Licence](https://www.neso.energy/data-portal/neso-open-licence)
- Registry record: `src/gridflow/connectors/neso_data_portal/registry/gis-boundaries-for-gb-dno-license-areas.json` (in the gridflow repo)
- Eligibility report: `docs/neso_data_portal/eligibility.md` (in the gridflow repo)
- Sibling package: @gis-boundaries-for-gb-generation-charging-zones.md
- Vendor README: @../README.md
