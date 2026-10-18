---
source: "neso_data_portal"
package: "obp-non-bm-physical-notifications"
dataset_key: "obp_physical_notifications"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-13
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Open Balancing Platform (OBP) - Non-BM Physical Notifications (PN)

This package is NESO's publication of the **Physical Notifications (PN) that non-BM Service Providers declare to the Open Balancing Platform (OBP)**. The vendor's package text says NESO publishes "Non-BM Physical Notifications (PN) data declared by Service Providers to Open Balancing Platform (OBP) system", published "continuously throughout the day" (CKAN package `notes`, @.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json; NESO [OBP Non-BM Physical Notifications](https://www.neso.energy/data-portal/obp-non-bm-physical-notifications)). A PN is a provider's declared MW output (or consumption) trajectory for a **registered non-BM unit**: the unit is not in the Balancing Mechanism, so its position is not otherwise visible in BM data (compare @../../../20-domain/concepts/bm-units.md). Each row is one **PN segment**: a start instant with the declared level at that instant, and an end instant with the declared level at that instant, so a flat PN is a row with equal levels (whether the vendor intends a linear ramp between unequal levels is not stated: `TODO: verify`). The vendor says both levels are "PN at Gate Closure" in MW (field-info text, below).

For a model this is the **declared pre-dispatch position of small, flexible, non-BM assets** (the units NESO procures reserve from outside the BM): it shows how much flexible capacity sits at each level over time, so it is a feature for reserve availability and for the volume NESO can instruct from non-BM providers. It is **not metered output**: these are provider declarations accepted and validated by OBP, not observed generation or demand.

**What this package is not.**

- It is **not a forecast archive.** There is no issue time; gridflow records `issue: none` and uses no forecast exemption. The recommended admission rests on the vendor's gate-closure declaration semantics, treated as an event/declaration table with a conservative capture vintage (RULINGS 738). Of the segment starts, 494,936 are on or before the CKAN `last_modified` of the capture and 150 are after it (K-AS-3 FACTS section 6.1): the later ones are declared positions, not forecasts of a value measured afterwards.
- It is **not a settlement-period table.** Segments are not uniformly half-hours: 400,690 of 495,086 rows last 1,800 s, and measured durations run down to 60 s. There is no `run_type`, no settlement date and no period number; none is synthesised.
- It does **not carry the dispatch instructions or the availability and price bands.** Those are the sibling packages @./obp-non-bm-reserve-instructions.md and @./obp-reserve-availability-utilisation-price.md. The PN is the reference position that the instruction "Target MW" is described against (vendor wording; see the instructions page).
- `unit_id` is a **registered non-BM unit ID**, not necessarily a BM unit ID or an NESO ID encoding. The vendor does not establish a universal encoding (K-AS-3 FACTS section 6.1). Values are stored exactly as served (101 distinct, for example `EDFE-11`, `ENGQR-02`, `ANSC-101`, `ARNKB-2`).

**Scope of the captured body.** One resource, 29,533,717 bytes, **495,086 rows** in the single capture of 2026-10-08. Segment starts run `2025-10-08T16:00:00` to `2026-10-08T12:29:00` and segment ends `2025-10-08T16:30:00` to `2026-10-08T12:30:00` (UTC). The body therefore spans about the 12 months before its `last_modified`: under `whole_capture`, older history lives only in older captures (K-AS-3b spec observation, not a ruling). Rows per unit range from 13 (`ARNKB-2`) to 15,047 (`ENGQR-01`, `ENGQR-02`).

**Units (vendor dictionary only).** `Level From` and `Level To` are **MW** ("PN at Gate Closure for window start time in MW" and "... for window end time in MW"; field-info unit `MW`, @.planning/research/neso-snapshots/field-info/20261008T114228Z/obp_physical_notifications.json, K-AS-3 FACTS g4). `Time From` and `Time To` carry the vendor unit `UTC`. `Data` has unit `N/A` (a label). Nothing is converted, and no MW-to-MWh energy conversion is stated or applied: a level is an instantaneous power at an instant, not an energy volume.

**Sentinels and zeros (K-AS-3 FACTS g5).** Preserve numeric zeros: 407,637 rows have `level_from` 0 and 407,238 have `level_to` 0 (longest file-order zero run 325 for each); a zero is a declared PN of zero, not a missing value, and is never nulled. Negative levels are real values: both columns range from **-49.9 to 50 MW**, and 42,083 rows have a negative `level_from` (`TODO: verify` the sign convention, which the dictionary does not state). No `NA`/`N/A` token, comma numeral, percent sign, padded number or other lexical defect was found in this body (K-AS-3 FACTS section 6.1, C07/C10), and there are no blank cells in any of the six columns (checked on all silver rows: 0 nulls in `level_from`, `level_to`, `time_to`).

**Typing.** `Data` is the fixed value `PN` on every row (vendor: "Fixed value PN"), kept as a string. `Unit ID` is a string, byte-equal as served. The two level columns are `float64`. The two time columns are `%Y-%m-%dT%H:%M:%S` cells with **no offset suffix**, typed as tz-aware UTC without a shift: the BST-season start `2026-06-01T00:00:00` stays `00:00Z`, which is 01:00 UK local time. The vendor's dictionary example (`2025-11-25T05:00:00Z`) carries a `Z`, but the served cells do not, so the UTC typing rests on the vendor's stated unit and not on the cell syntax.

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: EVT

## Files by disposition

One resource: the package has a single file and it is a silver source. There are no DOC files and no held files in this package.

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Non-BM Physical Notifications | CSV | upload | `dfe1d229-e973-43c6-b5eb-c28ad59d7136` |

- **Non-BM Physical Notifications** (SILVER, family `obp_physical_notifications`): CKAN resource `dfe1d229-e973-43c6-b5eb-c28ad59d7136`, package id `73edf630-fe9e-45a6-a2be-fa0d31a8ec1d`, flagged `datastore_active` by the vendor. gridflow captures it as an **upload file** (the download URL), not the datastore: [catalogue snapshot URL of 2026-10-06](https://api.neso.energy/dataset/73edf630-fe9e-45a6-a2be-fa0d31a8ec1d/resource/dfe1d229-e973-43c6-b5eb-c28ad59d7136/download/pn_20261006_44_nbm.csv). The file name in the URL embeds a date (`pn_20261006_44_nbm.csv`) and the vendor replaces the file under the same resource id (its `last_modified` was 2026-10-06T19:31:31.665985 in the snapshot and 2026-10-08T11:01:24.343784 on the capture), so `TODO: verify` whether the download file name changes with each refresh and whether a stable path exists. The bronze capture is `bronze/neso_data_portal/obp_physical_notifications/2026/10/08/raw_20261008T111457Z_dfe1d229-e973-43c6-b5eb-c28ad59d7136_8f6a94d9.csv` (immutable, SHA-256 `8f6a94d98041bc5fab6e0f5e0a5c95e918666c3e72e07d7b2c639bc3e0e8a852`, UTF-8, LF line endings, no byte-order mark, header plus 495,086 rows).

## Families

### `obp_physical_notifications`

- Kind: tabular · archetype: EVT · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Data | `data` | string | — | yes | — | — |
| Unit ID | `unit_id` | string | — | no | — | — |
| Time From | `time_from` | datetime | `%Y-%m-%dT%H:%M:%S` | no | UTC | UTC |
| Level From | `level_from` | float64 | — | yes | — | MW |
| Time To | `time_to` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | UTC |
| Level To | `level_to` | float64 | — | yes | — | MW |

- Entity key: `unit_id`, `time_from`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`time_from`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Field meanings (vendor dictionary, saved field info).** `Data`: type of data, fixed value `PN`. `Unit ID`: "Registered Unit ID associated with the corresponding instruction" (example `ABERU-1`; the dictionary text mentions an "instruction" although this package holds PNs, and `TODO: verify` that the identifier space matches the other two OBP packages). `Time From`: window start datetime, UTC. `Level From`: PN at gate closure for the window start time, MW. `Time To`: window end time, UTC. `Level To`: PN at gate closure for the window end time, MW. `TODO: verify` that a segment is linearly interpolated between its two levels and what "gate closure" fixes for a segment that starts hours after it was declared: the dictionary states the levels only.

**Two clocks.**

1. **Vintage (`ckan_last_modified`).** The resource is an upload with a usable CKAN timestamp (record vintage `ckan_last_modified`, ADR-030). `published_at` and `available_at` are both **2026-10-08T11:01:24.343784Z**, one value on all 495,086 rows: the CKAN `last_modified` of the captured file. That is when the vendor last replaced the file, **not when each PN was declared**. Every row, including a segment that started a year earlier, carries that one 2026-10-08 `available_at`, so an as-of query before 2026-10-08T11:01:24Z sees **no** row of this family and a point-in-time backtest cannot use it to say what a past PN looked like when it was declared. The record uses `LM` (last-modified) vintage as the conservative choice: no row is published earlier than its true availability, but the original declaration time, and whether past rows are later amended or removed, is not evidenced (one capture exists). `TODO: verify` the original availability of each declaration (needs publication or revision history).
2. **Event time (temporal recipe `utc_instant` on `time_from`).** `timestamp_utc` and `event_time` equal `time_from` on every row (checked on all rows): the **start of the segment, in UTC**. `time_to` is the segment end, typed UTC and kept but not the recipe column. The vendor does not state whether the end instant belongs to the segment: `TODO: verify` (INTERVAL-CLOSURE). `capture_written_at` (the gridflow capture time, 2026-10-08T11:14:57Z) is carried on every row as an audit column and is **not** a data clock.

**Identity and selection.** The record key is `(unit_id, time_from)`: unique across all 495,086 rows in the body and in silver (0 duplicate rows, 0 full-body duplicates; K-AS-3 FACTS T04, C07). The vendor guarantees no key, and whether a segment keeps its identity across later corrected re-publications is not documented: `TODO: verify` (cross-capture identity). Measured uniqueness does not authorise `key_latest`, so `_latest` is `whole_capture`, the newest complete capture. A consumer must therefore not assume that dropping out of the file means a PN was withdrawn: the file is a rolling window of about the last 12 months and the older history exists only in older captures.

**Row counts and shape (silver, 2026-10-13).** 495,086 rows, 0 validation failures, 0 rows excluded; the planned and activated counts agree (@.planning/v0.22-RESULTS.md section AS-3b, RULINGS 752). Silver layout: one Parquet file under `C:/gridflow-data/silver/neso_data_portal/obp_physical_notifications/year=2026/month=10/`; the partition is the **capture** date, not the event date. Columns (14): the 6 vendor columns, then `timestamp_utc`, `published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id` and `dataset_version` (`1+e1`). All timestamps are tz-aware UTC. No gold view or builder reads this family. This family is 495,086 of the 645,817 rows of the three eligible OBP families activated in AS-3b (RULINGS 752).

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc

The vendor's declared update frequency is **ad hoc**, while its package text says the data is published continuously throughout the day. gridflow has **one capture** (2026-10-08), so the real rhythm is unmeasured. Two observations point to frequent refresh: the file's `last_modified` moved from 2026-10-06T19:31:31 (catalogue snapshot) to 2026-10-08T11:01:24 (capture), and the vendor datastore reported 495,354 rows at 2026-10-08T13:22Z (field-info run) against the 495,086 captured at 11:14Z (the two are different representations of the resource, the datastore and the uploaded file, so the difference is an observation, not a measured refresh delta). `TODO: verify` the refresh cadence, the rolling window length, and whether each refresh replaces or appends, by comparing later complete captures with the hash-pinned body. The registry refresh is daily; the registry sets a 512 MiB download cap (`max_download_bytes` 536,870,912), against a 29.5 MB body, so the cap is not a near-term risk.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence). gridflow outputs derived from this package carry the attribution line "Supported by National Energy SO Open Data".

## Holds

- none

**No output of this package is held.** The single family was specified eligible (RULINGS 738) and activated as such (RULINGS 752), so there is no hold question or hold unit to state. The sibling AS-3b families that are held (the mock EAC and ORPS families) are different packages with their own pages; nothing here applies to them.

**Open questions that do not hold any output** (K-AS-3 FACTS section 6; carried as non-holding TODOs):

- `TODO: verify` the **original availability** of each declaration: the vintage is the file's last-modified time, never a declaration time.
- `TODO: verify` **cross-capture identity and immutability** of a `(unit_id, time_from)` segment: one capture, so amendment and deletion are unmeasured.
- `TODO: verify` **interval closure** (INTERVAL-CLOSURE): no source states whether a segment's end instant belongs to it.
- `TODO: verify` the **sign convention** of `level_from` and `level_to` (negative levels down to -49.9 MW occur on 42,083 rows for `level_from`) and the **interpolation** between a segment's two levels.
- `TODO: verify` the **stable download path**: the file name in the resource URL embeds a date.

**Known issues and gotchas.**

- **Same `available_at` for all history.** Every row carries 2026-10-08T11:01:24Z, however old the segment. Do not use this table to answer "what was declared when".
- **Declarations, not outturn.** A PN is a provider's declared position accepted by OBP; it is not metered. Do not compare it directly with metered generation or demand without that caveat.
- **Segments are not half-hours.** 400,690 rows are 1,800 s, the rest are shorter (down to 60 s). Join on the instant, not on a settlement period; if you need half-hourly values, derive them from the segment ends explicitly and state the interpolation.
- **Zeros are declarations.** 407,637 zero `level_from` rows (and 407,238 `level_to`) are real values. Do not null or drop them.
- **Unit IDs are as served.** No normalisation: `unit_id` is not a BM unit ID and is not joined to BM-unit tables without a mapping that the vendor does not provide (`TODO: verify` whether a non-BM-to-register mapping exists).
- **`data` is constant.** It is `PN` on every row; it is kept as served and carries no information in this body.
- **Late-starting rows.** 150 segment starts are after the file's `last_modified` (declared future positions). They are kept; the `available_at` of a future segment is therefore not later than its event time, but the declaration time is still unknown.

**Activation (2026-10-13, master `638b427`, PR #115).** The AS-3 research (RULINGS 736) read 26 families; the batch was split into AS-3a and AS-3b (RULINGS 737) and the specs ratified (RULINGS 738). AS-3b merged triple-green (RULINGS 751: CI green, the Sol diff review approved on the first pass with no findings, verification passed), with no engine change. This family was transformed from the 2026-10-08 capture with `--start/--end 2026-10-08`; there was no prior silver, so nothing was overwritten (RULINGS 752). The batch-wide `reconcile --all --cutoff 2026-10-12` exited 0 over 191 families with 0 gaps. The receipt is in @.planning/v0.22-RESULTS.md section AS-3b; the evidence is @.planning/phases/v0.22-K-AS-3/K-AS-3-FACTS.md (section 6) and the spec @.planning/phases/v0.22-K-AS-3/K-AS-3b-SPEC.md; the design is @docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md.

## Links

- [NESO Open Data Portal package](https://www.neso.energy/data-portal/obp-non-bm-physical-notifications)
- [Vendor field dictionary](https://www.neso.energy/data-portal/obp-non-bm-physical-notifications/non-bm_physical_notifications)
- Related packages: @./obp-non-bm-reserve-instructions.md, @./obp-reserve-availability-utilisation-price.md
- Registry record: @src/gridflow/connectors/neso_data_portal/registry/obp-non-bm-physical-notifications.json
- Domain: @../../../20-domain/concepts/bm-units.md
