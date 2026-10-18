---
source: "neso_data_portal"
package: "obp-reserve-availability-utilisation-price"
dataset_key: "obp_reserve_avail_price"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-13
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Open Balancing Platform (OBP) - Non-BM Reserve Availability MW and Utilisation Price

For each registered **non-BM** unit, this table says how many MW the provider had available for a
reserve service in a 30-minute UTC window, and the £/MWh price at which that capacity could be
used. The vendor describes it as Non-BM Quick Reserve and Slow Reserve availability and
utilisation-price data **declared by service providers, once the declarations have been accepted
and validated by the OBP system by gate closure**. It is published continuously through the day.
Non-BM here means units that are not Balancing Mechanism units: they take part through the Open
Balancing Platform instead (gridflow `@.planning/phases/v0.22-K-AS-3/K-AS-3-FACTS.md` §8). A row is
one unit, one window, one service and one price band. It is a **declaration at gate closure**, not
a metered delivery and not an instruction. Use it to see which reserve capacity and price levels
non-BM providers offered, and how the offered price stack moved over the year the file spans.
Pair it with the OBP instruction points (`@obp-non-bm-reserve-instructions.md`) and the physical
notification levels (`@obp-non-bm-physical-notifications.md`); the quick-reserve requirement
side is in `@quick-reserve-auction-requirement-forecast.md`. Point-in-time use needs the vintage
rule below (`@../../../20-domain/modelling/point-in-time-correctness.md`).

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: EVT
- Attribution: **Supported by National Energy SO Open Data**

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Non-BM Reserve Availability MW and Utilisation Price | CSV | upload | `6bfe7df0-60aa-462d-94cd-44ac0a4abb2c` |

- The package has **one resource**, and it is the only one: no DOC, HOLD or other file. It
  feeds family `obp_reserve_avail_price`. CKAN datastore active; datastore unique keys declared by
  the vendor: `Unit ID`, `Time From`, `Service ID`.
- Download as listed in the 2026-10-06 catalogue snapshot:
  [av_20261006_44_qr_sr_nbm.csv](https://api.neso.energy/dataset/769ec53a-9940-4df3-a867-6fa62d483097/resource/6bfe7df0-60aa-462d-94cd-44ac0a4abb2c/download/av_20261006_44_qr_sr_nbm.csv)
  (CKAN `last_modified` 2026-10-06T19:31:32.248565 at that snapshot). The file name carries a date
  and a number (`20261006`, `44`) and changes with each publication, so the stable handle is the
  resource id, not the URL. No reviewed source documents the date or the `44` as an issue time
  (FACTS g2); `TODO: verify` what `44` denotes.
- Captured: `raw_20261008T111500Z_6bfe7df0-60aa-462d-94cd-44ac0a4abb2c_70723223.csv`,
  10,215,008 bytes, 150,309 data rows, one header epoch, strict UTF-8, no BOM, LF line endings,
  no duplicate header (docs profile `@docs/neso_data_portal/profile/families/obp_reserve_avail_price.json`).
  Bronze written 2026-10-08T11:15:00.909612Z; CKAN `last_modified` of the captured file
  2026-10-08T11:01:23.882138.

## Families

### `obp_reserve_avail_price`

- Kind: tabular · archetype: EVT · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Data | `data` | string | — | yes | — | — |
| Unit ID | `unit_id` | string | — | no | — | — |
| Time From | `time_from` | datetime | `%Y-%m-%dT%H:%M:%S` | no | UTC | UTC |
| Time To | `time_to` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | UTC |
| Pair ID | `pair_id` | int64 | — | no | — | — |
| Availability Power | `availability_power` | float64 | — | yes | — | MW |
| Utilisation Price | `utilisation_price` | float64 | — | yes | — | £/MWh |
| Service ID | `service_id` | string | — | no | — | — |

- Entity key: `unit_id`, `time_from`, `pair_id`, `service_id`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`time_from`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured resource, which CKAN emits without an offset and gridflow reads
   as UTC (gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). For the one
   capture to date that is `2026-10-08T11:01:23.882138Z`, shared by all 150,309 silver rows
   (checked 2026-10-13). The file has **no issue column**, and the record's issue recipe is
   `none`: no row carries its own declaration or publication time. The vintage is a conservative
   proxy, so no row is published earlier than it was truly available. It does **not** backdate:
   the original availability time of any row is `TODO: verify` (FACTS g2).
2. **Event time (`utc_instant` on `time_from`).** `timestamp_utc` = `event_time` = `time_from`,
   the UTC start of the 30-minute window, with no shift. Equality held on every silver row on
   2026-10-13. Event time is **not** the capture time. A BST-season `Time From` keeps its clock
   because the cells are already UTC. `time_to` is the window end and is kept as a data column.

**Mixed horizon.** The capture spans `Time From` 2025-10-09T10:00:00 to 2026-10-08T12:00:00
(`Time To` 2025-10-09T10:30:00 to 2026-10-08T12:30:00), so about the 12 months before its
`last_modified`. Of the 150,309 rows, 150,237 start on or before the vintage and **72 start
after it**: those are declared positions for windows still ahead at the vintage instant. The
mixed history/future starts do not satisfy a forward-only forecast test, so the package is
admitted as a **gate-closure declaration / event table**, not as a forecast (FACTS §8, g2). Filter
`available_at <= :as_of` for point-in-time queries. Under `whole_capture`, history older than the
newest capture's window lives only in older captures, so a single capture is not a full archive.
`TODO: verify` whether earlier declarations are revised or removed after publication, and the
vendor's retention window (no repeated same-resource capture exists yet to show either).

**Columns (vendor dictionary, cited in FACTS; nothing inferred from names).**

| Column | Vendor text | Silver treatment |
|---|---|---|
| `data` | Type of data; fixed value `AV` | string; `AV` in every row |
| `unit_id` | Registered unit ID. The vendor wording ("associated with the corresponding instruction") looks copied from the instructions dictionary | string, stored as-is, no normalisation; 60 distinct IDs in the capture |
| `time_from` / `time_to` | Window start / end datetime, unit UTC | tz-aware UTC datetimes, no shift |
| `pair_id` | Band specifying the MW and price. Comment: positive service `+1`, negative `-1` | int64, kept signed |
| `availability_power` | MW available for the service at gate closure for the window | float64, **MW** |
| `utilisation_price` | Utilisation price available for the service at gate closure for the window | float64, **£/MWh** |
| `service_id` | Name of the non-BM service; vendor examples `PQR, NQR, PSR, NSR` | string |

- **Units** come only from the vendor dictionary: MW for `availability_power`, £/MWh for
  `utilisation_price`. No MW-to-MWh or price-unit conversion is inferred from any other service
  (FACTS g4).
- **Service IDs in the capture:** `PQR` 58,384 rows, `NQR` 18,381, `PSR` 73,544. `NSR` is a vendor
  example but is absent from the capture. The vendor text does not expand the codes. Reading them
  as positive/negative Quick/Slow Reserve is consistent with the resource description, but the
  code expansion is `TODO: verify` against a vendor definition.
- **`pair_id` is a signed band, not a sentinel.** `1` in 131,928 rows and `-1` in 18,381 rows.
  The `-1` count equals the `NQR` count, and `1` equals `PQR + PSR`, a measured coincidence
  with the vendor's positive/negative comment, not a documented rule. **`-1` is valid
  negative-service data and is never mapped to null** (FACTS T03, g5).
- **Sentinels and missing values (FACTS g5).** The record declares no null token. No NA tokens,
  percent-bearing numbers, comma numerals or padding were found. Zeros are real values and are
  kept: `availability_power` is 0 in 24,941 rows (longest zero run 4,622 in file order),
  `utilisation_price` is 0 in 115 rows (longest run 1). Negative prices are kept as published.
  Nulls in the capture: none in any column. No `min` / `max` bounds are imposed.
- **Value ranges in the capture (this eligible family only):** `availability_power` 0 to 55 MW;
  `utilisation_price` -10000 to 10000 £/MWh. The extremes are **not** reclassified as sentinels
  or caps. `TODO: verify` whether the vendor documents a price cap or floor.
- **Window length** is 1,800 seconds in every row. `TODO: INTERVAL-CLOSURE`: no reviewed source
  states whether the window is closed or open at either end, so no interval convention is invented.
- **Identity.** The recommended entity key (`unit_id`, `time_from`, `pair_id`, `service_id`) is
  unique in the capture, as are `(unit_id, time_from, pair_id)` and
  `(unit_id, time_from, service_id)` separately (the vendor's own datastore key is
  `Unit ID, Time From, Service ID`). That is a duplicate guard: a repeated key fails as a
  duplicate-entity-key error. It does not prove revision identity, so `_latest` stays
  `whole_capture` and the newest capture replaces the previous one as a whole. `TODO: verify`
  cross-capture identity.

**Row count drift.** A later datastore field-info call (2026-10-08T13:22Z, about two hours after
the bronze write) reported 150,431 total records against 150,309 in the captured file, consistent
with continuous publication into an append-or-update datastore. The captured file is the
reference; `TODO: verify` whether the CSV download and the datastore are the same population.

**Activation (2026-10-13, master `638b427`, PR #115).** Transformed with `--start/--end
2026-10-08` (one capture, no prior silver, so nothing was overwritten): **150,309 silver rows**,
equal to the planned count and to the CSV row count, zero exclusions. The batch's reconcile
`--all --cutoff 2026-10-12` exited 0 with 191 families and 0 gaps (gridflow
`@.planning/v0.22-RESULTS.md` §AS-3b; RULINGS 751, 752).

Silver columns beyond the vendor columns: `timestamp_utc`, `published_at`, `bronze_capture_id`,
`capture_written_at`, `event_time`, `available_at`, `source_run_id`, `dataset_version` (all
timestamps tz-aware UTC; `dataset_version` `1+e1` = record version 1, epoch 1). One Parquet file
under `silver/neso_data_portal/obp_reserve_avail_price/year=2026/month=10/`.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc
- The resource description says the data is "continuously published throughout the day"; the
  "Ad hoc" label is the CKAN metadata value, and the two do not agree. The registry refreshes
  daily. `TODO: verify` the vendor's actual publication cadence and latency.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

## Holds

- none

This package has no held output. Its eligibility rests on the declaration / event-table reading
above, not on forecast semantics. Non-holding open questions, all `TODO: verify`: original
availability time and revision behaviour of declared rows, the `44` file-name token, the
`PQR`/`NQR`/`PSR`/`NSR` code definitions, cross-capture identity, interval closure, and any
price cap. Other packages in the same batch (the mock EAC and ORPS families) are held; their
holds do not affect this page.
