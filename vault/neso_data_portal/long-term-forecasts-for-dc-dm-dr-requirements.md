---
source: "neso_data_portal"
package: "long-term-forecasts-for-dc-dm-dr-requirements"
dataset_key: "dc_dm_dr_long_term_fc"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-13
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Long-Term Forecasts for DC, DM and DR Requirements

This package is NESO's forward view of how much of each **dynamic frequency-response service** the
system operator expects to need. NESO's own description says the dataset holds forecasts of the
Dynamic Containment (DC), Dynamic Moderation (DM) and Dynamic Regulation (DR) **Low and High**
requirements for the next 12 months. The method uses forecast demand, inertia and response volumes,
plus a view of the largest losses on the system. NESO adds that the actual day-ahead requirements are
likely to change after optimisation closer to real time, with better visibility of inertia, demand
and loss sizes (CKAN package `notes`,
@.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json). The single resource
description says the requirements "are shown as possibilities in each EFA each month".

Each row is therefore **one cell of a probability-style grid**: a forecast creation date, a target
month, a service and direction (`DC-H`, `DC-L`, `DM-H`, `DM-L`, `DR-H`, `DR_L`), an Electricity
Forecasting Area (EFA) block number, a requirement **band** (`Interval`, nine bands from `0-200` to
`1600-1800`), and a `Possibilities` weight that the vendor says runs from 0 to 1. It is not a MW
requirement series and not a single-number forecast; the requirement is spread across bands. For
modelling it would be a market-sizing input for the frequency-response services, but the band unit
and the availability of the forecast are both unresolved, so the output is **held** (see Holds) and
this page gives schema, row counts, clocks and missingness only, with **no data values**: no sample
rows and no value statistics. The shorter-horizon siblings are the DC four-day forecast and the DM
and DR requirement tables: @./dynamic-containment-4-day-forecast.md,
@./dynamic-moderation-requirements.md and @./dynamic-regulation-requirements.md.

The package-level status in the front matter is generated from the registry and reads `eligible`;
the family-level eligibility is **held**.

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| DX Future Requirement | CSV | upload | `5162c4d1-6d72-497b-a2ad-3a2449bc8952` |

The one resource is a CKAN **file upload** (not a datastore dump), so the download link carries a
file name. Bytes, rows and `last_modified` come from the capture sidecar under
`C:/gridflow-data/bronze/neso_data_portal/dc_dm_dr_long_term_fc/2026/10/08/`.

| Resource | Download | Bytes | Data rows | CKAN `last_modified` | Body sha256 prefix |
|---|---|---:|---:|---|---|
| DX Future Requirement | [dx_future_requirement.csv](https://api.neso.energy/dataset/a1256c20-f657-4186-b288-e2c238a394c0/resource/5162c4d1-6d72-497b-a2ad-3a2449bc8952/download/dx_future_requirement.csv) | 176541 | 4212 | 2026-04-01T13:52:35.778789 | `7150db73` |

Package page: [long-term-forecasts-for-dc-dm-dr-requirements](https://www.neso.energy/data-portal/long-term-forecasts-dc-dm-dr-requirements).
Data rows equal the silver rows. The vendor's resource description is quoted above; it does not
state the column semantics, which come from the field dictionary (see Families).

**Bronze body (full-body scan, FACTS section 3 and g5).** One capture only (2026-10-08), one exact
6-column header (one header epoch), CSV, strict UTF-8. The scan found no blank cell, no `-1`, `N/A`,
`NA`, `NULL`, `null` or `NaN` token, no padded cell, no embedded comma or percentage sign, and no
decoding or row-width error. Because only one capture exists, in-place revision and dropped-target
behaviour cannot yet be observed.

### DOC

None. The package has no DOC-only resource.

### HOLD

None at resource level. The single resource is read and carried to silver; the **output** is held
(see Holds).

## Families

### `dc_dm_dr_long_term_fc`

- Kind: tabular · archetype: FC · refresh: monthly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Forecast Created | `forecast_created` | date | `%Y-%m-%d` | no | — | ISO 8601 |
| Forecast Target Month | `forecast_target_month` | date | `%Y-%m-%d` | no | — | ISO 8601 |
| Service Type | `service_type` | string | — | no | — | — |
| EFA | `efa` | int64 | — | no | — | — |
| Interval | `interval` | string | — | no | — | — |
| Possibilities | `possibilities` | float64 | — | yes | — | — |

- Entity key: `forecast_created`, `forecast_target_month`, `service_type`, `efa`, `interval`
- Latest: `whole_capture`
- Temporal recipe: month (`forecast_target_month`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**One header epoch.** The record accepts one exact header, the six vendor columns in the order above.
Silver names are the vendor names in lower case with underscores. `Interval` is stored as the raw
band label and is **never** split into numeric bounds.

**What the columns mean (vendor dictionary).** The descriptions come from NESO's saved field info
for the datastore (gridflow
`@.planning/research/neso-snapshots/field-info/20261008T114228Z/dc_dm_dr_long_term_fc.json`, one
resource, so it is the dictionary for this family).

- **`Forecast Created`**: "the date for which the forecast is created". A creation **date**, ISO
  8601, with no time of day and no zone.
- **`Forecast Target Month`**: "the date for which the forecast is for", ISO 8601, written as the
  first day of the month. The grain is a **month label**, not a day.
- **`Service Type`**: the service and direction. The dictionary comment lists `DC-L`, `DC-H`,
  `DM-L`, `DM-H`, `DR-L` and `DR-H`. The body spells the Dynamic Regulation Low code `DR_L`
  (underscore), not `DR-L`. gridflow keeps the body's spelling byte for byte and does not normalise
  codes; `TODO: verify` with NESO which spelling is correct (FACTS section 3, H-LT, section 7).
- **`EFA`**: "the EFA block for which the forecast is for", an integer block number (the body holds
  1 to 6). The EFA label is a **recurring block class within the target month**, not a particular
  day. The block clock is the UK local clock (EFA 1 starts at 23:00 local time on the previous
  date), per NESO's EAC market design explainer (FACTS section 5.1). gridflow keeps `EFA` as the
  raw integer and composes no EFA start or end instant (RULINGS 572, 588, 720).
- **`Interval`**: "the interval for which the forecasted requirement is in", nine bands. The
  dictionary comment lists `0-200`, `200-400`, `400-600`, `600-800`, `800-1000`, `1000-1200`,
  `1200-1400`, `1400-1600` and `1600-1800`. The dictionary unit is `NA`. The band unit and which
  endpoint is inclusive are **not established** (see Holds).
- **`Possibilities`**: "the possibilities for which the forecasted requirement is within the
  interval". The dictionary comment says "this field is from 0 to 1" and the example is `0.1`. This
  is the vendor's own statement; gridflow asserts no distribution here. `TODO: verify` the formal
  probability interpretation and whether the weights over the nine bands for one month, service and
  EFA are meant to sum to one.

**Units (vendor dictionary only).** The dictionary `unit` field is **ISO 8601** for the two date
columns and **`NA`** for `Service Type`, `EFA`, `Interval` and `Possibilities`. Nothing in the
dictionary attaches MW, MWh, pounds or a percentage to any column. gridflow therefore records no
physical unit for `EFA` (a categorical block identifier), none for `Possibilities` (a value on the
vendor's 0 to 1 scale, never rescaled to a percentage), and **no unit for `Interval`**. A unit is
not inferred from the band magnitudes or from sibling datasets (FACTS g4).

**Two clocks.**

1. **Vintage (`ckan_last_modified`; `available_at`).** The resource is a file upload, so the vintage
   is the CKAN `last_modified` of the captured file (ADR-030, ADR-035). `published_at` equals
   `available_at` and is 2026-04-01T13:52:35.778789 UTC, taken from a naive CKAN timestamp that the
   engine reads as UTC (`_bronze.py`). The silver check (2026-10-13) confirms `available_at` equals
   `published_at` on all 4,212 rows, with a single value, and both differ from
   `capture_written_at` (2026-10-08T10:05:13.865164 UTC). An as-of query before the `last_modified`
   instant returns no rows. `Forecast Created` is a creation **date** with no clock or
   publication instant, so it is an ordinary column, **never** used as `issue_time` and never
   backdated to midnight (FACTS section 5.2): the family record has `issue: none`. The package
   refresh is listed as monthly, but the only capture has a `last_modified` six months before it was
   taken; `TODO: verify` whether NESO still refreshes the file monthly and how a refresh is
   published (in place, or as a new resource).
2. **Event time (temporal recipe `month(forecast_target_month)`).** The event instant is the
   **month-label anchor**: in silver, `timestamp_utc` equals `event_time` on all rows (checked
   2026-10-13), and `event_time` equals UK local midnight at the start of the `forecast_target_month`
   date, converted to UTC (13 distinct values for the 13 target months, tz-aware UTC). It is an
   **anchor for the calendar month, not the start of EFA 1 or of any block or band**, and it must not
   be read as a delivery instant (RULINGS 720). The month grain has no per-row daily block start
   (FACTS section 5.5). This is a different clock from the creation date and from the vintage.

**Target grain and horizon (FACTS section 5.5).** Grain is creation date by target month by
service and direction by EFA block by requirement band. The captured body holds **one creation
date** and **13 target months**, which includes the creation month. The vendor description speaks
of the next 12 months; gridflow keeps the actual target labels. Each month has 324 rows
(6 services x 6 EFA blocks x 9 bands), and 13 x 324 = 4,212. Every service and EFA block appears
with every band in every month, so the grid is complete for this capture. There is no season, year
or full-timestamp target column.

**Identity and selection.**

- The entity key is the five descriptive dimensions above. **`Possibilities` is never part of the
  key**, so a revised weight updates the same entity rather than creating a new one. The full-body
  scan found zero duplicate-key excess rows (4,212 distinct keys, FACTS g3).
- The vendor publishes no key and gives no uniqueness guarantee: `TODO: verify` a vendor-guaranteed
  identity and whether a published row can be revised in place.
- `_latest` is `whole_capture`; there is no `key_latest` selection because no identity guarantee
  exists. One capture exists, so amendment behaviour cannot yet be measured.
- This is a forecast, not settlement accounting: no `run_type` applies and none is fabricated.

**Sentinels and missing values (FACTS g5).** No sentinel token, blank cell, padding or thousands
separator occurs in the body, so none is mapped to null. Zero is a legitimate vendor value and is
kept as numeric zero; the vendor does not define any null token. Silver null counts (4,212 rows,
2026-10-13): 0 in every vendor column, including `possibilities`.

**Row counts (silver, 2026-10-13).**

| Resource | Rows | Distinct entity keys |
|---|---:|---:|
| `5162c4d1-6d72-497b-a2ad-3a2449bc8952` (DX Future Requirement) | 4212 | 4212 |

Rows per service and direction label: 702 each for the six labels (6 x 702 = 4,212).

**Activation (2026-10-13, master `7e3c023`, PR #112).** The ancillary-services batch AS-1 merged
triple-green (RULINGS 723) and was transformed from the 2026-10-08 captures with
`--start/--end 2026-10-08`. There was no prior silver, so nothing was overwritten and no snapshot
was taken (RULINGS 725). Silver has **4,212 rows** for this family, equal to the planned count,
with 0 validation failures and no blank-row exclusions (112,730 rows across the nine AS-1
families). The batch-wide reconcile `--all --cutoff 2026-10-12` exited 0 with 0 gaps over 159
families (47 adjudicated, 0 stale). Gridflow `@.planning/v0.22-RESULTS.md` section AS-1 holds the
receipt. The design choices (raw band labels, month anchor, no issue time, held outputs) are the
seat's rulings 718 and 720.

Silver layout: one Parquet file for the capture under
`C:/gridflow-data/silver/neso_data_portal/dc_dm_dr_long_term_fc/year=2026/month=10/`. The
`year=`/`month=` partition is the **capture** date, not the target month. There are 14 columns:
the six vendor columns, then `timestamp_utc`, `published_at`, `bronze_capture_id`,
`capture_written_at`, `event_time`, `available_at`, `source_run_id` and `dataset_version`. All
timestamps are tz-aware UTC. `dataset_version` is `1+e1` (record version 1, generic engine version
1). No gold view or builder reads this family.

## Cadence

- Registry refresh: monthly
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Monthly

The vendor states a monthly update frequency. The single captured file's CKAN `last_modified`
(2026-04-01) predates the capture (2026-10-08) by about six months, so the stated frequency is not
visible in the one capture available. `TODO: verify` the actual refresh pattern. Only further
captures, compared pair by pair against the hash-pinned first body, can show whether the file is
replaced monthly, appended to, or amended in place.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `dc_dm_dr_long_term_fc`: held: TODO: DX-LT-INTERVAL — what unit and which inclusive endpoint do the `Interval` bands (`0-200` … `1600-1800`) use, and when was the creation-dated forecast available? 324 rows target the creation month. (unit v0.22-K-AS-1)

The silver output exists on disk but is **held**. It may not be published or used for models until
the question above is answered. The hold sits in the record (RULINGS 720). It has two parts, both
vendor-semantics questions that a NESO answer settles and that inspection of values cannot:

1. **Band unit and boundary.** The dictionary lists the nine bands with unit `NA` and does not say
   whether they are megawatts or something else, or whether a boundary value such as 200 belongs to
   the lower or the upper band. gridflow keeps `Interval` as a raw string and builds no numeric
   bounds.
2. **Availability of the forecast.** `Forecast Created` is a date only, and the CKAN
   `last_modified` is an upload time, not proof of when each forecast was first available. The
   forward-target test, by month label against the vintage date, puts **324 rows on or before** the
   `last_modified` date (the creation month) and **3,888 rows after** it. The creation-month rows
   therefore target a period that had already begun when the file was uploaded, so their original
   publication time is unproved. The other 3,888 rows are forward targets.

**What is not established.** The band unit, the band endpoint convention, the formal meaning of
`Possibilities` (and whether the bands sum to one), the correct spelling of the Dynamic Regulation
Low code (`DR_L` in the body, `DR-L` in the dictionary), the publication clock of `Forecast Created`,
whether a published row is revised, and the refresh pattern. gridflow will not guess any of them,
will not attach MW to the bands, will not rescale `Possibilities`, and will not rewrite `DR_L`.
`TODO: name the unit that will settle DX-LT-INTERVAL` once one is opened.

**What settles it.** A NESO dictionary correction or written clarification of the `Interval` unit
and endpoint convention, plus a statement of when each creation-dated forecast is published (or
later complete captures that show the file's lifecycle). Once ruled, releasing the hold is a record
edit with no transform change.
