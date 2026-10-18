---
source: "neso_data_portal"
package: "dynamic-containment-4-day-forecast"
dataset_keys: ["dc_forecast_4d", "dc_forecast_4d_history"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-13
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  held: true
  title: Dynamic Containment 4 day forecast
  summary: >-
    NESO's forecast of the Dynamic Containment requirement for the next four days, and its archive
    of earlier issues.
  facts:
    vendor: NESO Data Portal, two CSV files
    cadence: A rolling four-day forecast; the archive is updated daily
    grain: One row per date and service code, one column per EFA block
  what_it_is: >-
    NESO's forecast of the Dynamic Containment requirement, one of the GB frequency-response
    services the system operator procures. Each file is a wide table: one row per service code
    (`DC-H`, `DC-L`) and date, and one MW column per EFA block, `EFA_1` to `EFA_6`.
  how_used:
    - A look-ahead feature for Dynamic Containment procurement volumes
    - Read beside the other ancillary-service requirement forecasts
  raw_feed:
    note: Each table's file downloaded whole, by its CKAN resource.
    commands:
      - {run: gridflow ingest neso_data_portal dc_forecast_4d --last 24h, comment: bronze only}
      - {run: gridflow ingest neso_data_portal dc_forecast_4d_history --last 24h, comment: bronze only}
  family:
    slug: dynamic-containment-4-day-forecast
    members:
      - dataset: dc_forecast_4d
        differs: The next four days, eight rows a file
        request: "GET https://api.neso.energy/dataset/c8cd1e99-bc7e-454c-8ac1-ebd9264f4d0f/resource/1b85a3f3-80f0-49cf-9b0e-49648fa0cae6/download/f9bf31f0d49f45baa72649f0a8d2e254_dcrequirements_1b85a3f3-80f0-49cf-9b0e-49648fa0cae6_patch.csv"
        held: NESO does not say whether the slash dates in `Date` are day first or month first.
      - dataset: dc_forecast_4d_history
        differs: Earlier issues, one per creation date
        request: "GET https://api.neso.energy/dataset/c8cd1e99-bc7e-454c-8ac1-ebd9264f4d0f/resource/d5c3b48a-a0a9-4d57-a02a-ac0af09a6298/download/b4634e50af5e4d3bb7f610422776a819_dcrequirementshistorical1_d5c3b48a-a0a9-4d57-a02a-ac0af09a6298_.csv"
        held: No stated publication time for each issue; some creation dates are after the upload.
  related:
    - {dataset: neso_data_portal/eac-br-auction-results, note: Another reserve NESO buys at the day-ahead stage}
---

# Dynamic Containment 4 Day Forecast

NESO's forecast of the **Dynamic Containment (DC) requirement**, published on the Open Data
Portal as two CSVs. DC is one of the GB frequency-response services procured by the system
operator. The file is a wide table: one row per service/direction code (`DC-H`, `DC-L`) and
one column per **EFA block** (`EFA_1` to `EFA_6`), in MW per the vendor dictionary (see Units).
The **current** file is a rolling forecast for the next four days (8 rows in the capture: 4
dates by 2 service codes). The **history** file is the vendor's daily-updated archive of earlier
issues, one issue per creation date, 12,932 rows in the capture. Use the package as a
look-ahead feature for DC procurement volumes, alongside the other ancillary-service
requirement packages (@dynamic-moderation-requirements.md, @dynamic-regulation-requirements.md,
@long-term-forecasts-for-dc-dm-dr-requirements.md, @balancing-reserve-auction-requirement-forecast.md).
What the figure means precisely (for example volume to be procured) is not defined beyond the
file name and dictionary: `TODO: verify` the vendor's definition of the requirement.

**Both silver outputs are held** (unit v0.22-K-AS-1). The current file's `Date` column is
published in a slash format whose day/month order the dictionary does not settle. The history
file has no established publication instant for its creation-labelled issues. This page gives
schema, row counts and structure only, and publishes **no data values** from either family
(see Holds).

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: FC
- Settlement-period and clock background: @../../../20-domain/concepts/settlement-period.md
  (EFA blocks are not settlement periods; the link is context for the local-clock handling only)

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Dynamic Containment - 4 Day forecast | CSV | upload | `1b85a3f3-80f0-49cf-9b0e-49648fa0cae6` |
| Dynamic Containment 4 Day Forecast - History | CSV | upload | `d5c3b48a-a0a9-4d57-a02a-ac0af09a6298` |

- Dynamic Containment - 4 Day forecast → `dc_forecast_4d`.
  Download as captured: [f9bf31f0d49f45baa72649f0a8d2e254_dcrequirements_1b85a3f3-80f0-49cf-9b0e-49648fa0cae6_patch.csv](https://api.neso.energy/dataset/c8cd1e99-bc7e-454c-8ac1-ebd9264f4d0f/resource/1b85a3f3-80f0-49cf-9b0e-49648fa0cae6/download/f9bf31f0d49f45baa72649f0a8d2e254_dcrequirements_1b85a3f3-80f0-49cf-9b0e-49648fa0cae6_patch.csv).
  The file name carries a content-hash prefix and a `_patch` suffix, so it can change with each
  publication. The stable handle is the resource id, not the URL.
  Captured: `raw_20261008T100517Z_1b85a3f3-80f0-49cf-9b0e-49648fa0cae6_8c90bf7e.csv`,
  575 bytes, 8 data rows, one header epoch. CKAN `last_modified` `2026-10-07T13:05:22.967331`.
- Dynamic Containment 4 Day Forecast - History → `dc_forecast_4d_history`.
  Download as captured: [b4634e50af5e4d3bb7f610422776a819_dcrequirementshistorical1_d5c3b48a-a0a9-4d57-a02a-ac0af09a6298_.csv](https://api.neso.energy/dataset/c8cd1e99-bc7e-454c-8ac1-ebd9264f4d0f/resource/d5c3b48a-a0a9-4d57-a02a-ac0af09a6298/download/b4634e50af5e4d3bb7f610422776a819_dcrequirementshistorical1_d5c3b48a-a0a9-4d57-a02a-ac0af09a6298_.csv).
  The same caveat applies to the file name.
  Captured: `raw_20261008T100521Z_d5c3b48a-a0a9-4d57-a02a-ac0af09a6298_42e2b455.csv`,
  722,981 bytes, 12,932 data rows, one header epoch. CKAN `last_modified`
  `2026-10-07T13:05:28.053180`.

### DOC

None. The package has no documentation-file resources in the registry. The only dictionaries
are the vendor's field-info pages, linked under Units.

## Families

### `dc_forecast_4d`

- Kind: tabular · archetype: FC · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Date | `date` | string | — | no | — | ISO 8601 |
| Service_Type | `service_type` | string | — | no | — | — |
| EFA_1 | `efa_1` | float64 | — | yes | — | MW |
| EFA_2 | `efa_2` | float64 | — | yes | — | MW |
| EFA_3 | `efa_3` | float64 | — | yes | — | MW |
| EFA_4 | `efa_4` | float64 | — | yes | — | MW |
| EFA_5 | `efa_5` | float64 | — | yes | — | MW |
| EFA_6 | `efa_6` | float64 | — | yes | — | MW |

- Entity key: `date`, `service_type`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Held (unit v0.22-K-AS-1).** The silver output exists but is not eligible for publication or
point-in-time use. This page gives schema, row counts and structure only.

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the CKAN
   `last_modified` of the captured file: `2026-10-07T13:05:22.967331`, which CKAN emits without
   an offset and gridflow reads as UTC (gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`).
   All 8 silver rows share this one vintage. The file has **no issue or production column**,
   and the record's issue recipe is `none`.
2. **Event time: none.** The temporal recipe is `none`, so `timestamp_utc` = `event_time` = the
   **capture time** (the bronze sidecar `written_at`, `2026-10-08T10:05:17.614229Z`), the same on
   all 8 rows. It does **not** locate any row in forecast time, and it is later than
   `available_at` (the file was changed on 2026-10-07 and fetched on 2026-10-08). Checked on
   every silver row on 2026-10-13. The forecast date is carried only by the raw `date` string.
   A date anchor (`date_sp1`) is conditionally planned for `date` once its order is settled
   (FACTS T02), and is not applied now.

**Date format (the hold).** `date` is stored as the **raw string**. The capture holds four
consecutive dates from the capture day onward, written as slash dates (`08/10/2026` to
`11/10/2026`, as captured). Every one of them is ambiguous between day-first and month-first,
and the current dictionary documents the column as ISO 8601, which the values are not. A
day-first reading is strongly favoured by the vendor's "next four days" description and by the
history file's unambiguous day-first examples, but no resource-specific statement settles it
(FACTS §4.4 T01). Under day-first, all 8 target dates fall after the vintage. Under
month-first, 4 of the 8 would fall on or before it. No unconditional forward-target claim is
made while the order is open.

**EFA blocks and the local clock.** `EFA_1` to `EFA_6` are wide columns. There is no per-row
block timestamp, and gridflow composes none (EFA labels stay raw wide columns; RULINGS 572/588).
The vendor's history dictionary defines the blocks on the **UK local clock**:

| EFA | Local start | Local end |
|---:|---|---|
| 1 | delivery date − 1, 23:00 | delivery date, 03:00 |
| 2 | 03:00 | 07:00 |
| 3 | 07:00 | 11:00 |
| 4 | 11:00 | 15:00 |
| 5 | 15:00 | 19:00 |
| 6 | 19:00 | 23:00 |

NESO's EAC market design explainer (Appendix B,
[document 277671](https://www.neso.energy/document/277671/download)) gives the same local-clock
blocks with spring and autumn diagrams. The boundaries are the vendor's. The consequence on
clock-change days is gridflow's calculation from those boundaries and `Europe/London`: a
service day has 23 hours in spring (EFA 1 is 3 hours long) and 25 in autumn (EFA 1 is 5 hours
long), with EFA 2 to 6 four hours each. Using them is a modelling step, not a stored column.

**Units (vendor dictionary only).** `EFA_1` to `EFA_6` are **MW**, as declared in the current
dictionary
([current dictionary](https://www.neso.energy/data-portal/dynamic-containment-4-day-forecast/dynamic_containment_-_4_day_forecast)).
`Date` carries the dictionary's "ISO 8601" in its unit field, which describes a format, not a
unit (and does not match the values; see above). `Service_Type` carries no unit. No unit was
inferred from a column name.

**Service codes.** `Service_Type` holds two codes, `DC-H` and `DC-L`, in the capture. They are
kept byte-equal as captured and the vendor's definition of each is not stated in the
dictionary. They are presumably the high- and low-frequency directions of DC;
`TODO: verify` with the vendor.

**Sentinels and missing values (FACTS g5).** A full scan of the body found no blank cells,
`-1`, `N/A`, `NA`, `NULL`, `null` or `NaN` tokens, no padded cells, and no embedded commas or
percent signs. The record declares no null token, and no column has a null in silver. Zero, if
it appears, is a numeric zero and is kept. `TODO: verify` whether the vendor gives any
meaning to zero. No bounds are imposed and no value is converted.

**Identity and selection.** The entity key is `(date, service_type)`, a capture-level
duplicate guard, unique in the capture (FACTS T03). The vendor documents no revision identity:
`TODO: verify`. `_latest` is `whole_capture`: the newest capture replaces the previous one as
a whole.

**Activation (2026-10-13, master `7e3c023`, PR #112).** Transformed at cutoff 2026-10-08 (one
capture): **8 silver rows**, equal to the planned count. No prior silver existed, so nothing
was overwritten (gridflow `@.planning/v0.22-RESULTS.md` §AS-1; RULINGS 723, 725).

### `dc_forecast_4d_history`

- Kind: tabular · archetype: FC · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Forecast_Created | `forecast_created` | string | — | no | — | date |
| Forecast_Target_Date | `forecast_target_date` | date | `%d/%m/%Y` | no | — | date |
| Service_Type | `service_type` | string | — | no | — | text |
| EFA_1 | `efa_1` | float64 | — | yes | — | MWs |
| EFA_2 | `efa_2` | float64 | — | yes | — | MWs |
| EFA_3 | `efa_3` | float64 | — | yes | — | MWs |
| EFA_4 | `efa_4` | float64 | — | yes | — | MWs |
| EFA_5 | `efa_5` | float64 | — | yes | — | MWs |
| EFA_6 | `efa_6` | float64 | — | yes | — | MWs |

- Entity key: `forecast_created`, `forecast_target_date`, `service_type`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`forecast_target_date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Held (unit v0.22-K-AS-1).** The silver output exists but is not eligible for publication or
point-in-time use. This page gives schema, row counts and structural counts only. It gives no
EFA values, value ranges or sample rows.

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the CKAN
   `last_modified` of the captured archive, `2026-10-07T13:05:28.053180` (offset-less, read as
   UTC per ADR-030). All 12,932 rows share this one vintage. It says when the archive file last
   changed. It does **not** say when any archived issue became available.
2. **Event time (`date_sp1` on `forecast_target_date`).** `timestamp_utc` = `event_time` = the
   start of settlement period 1 of the target date, i.e. UK local midnight of the target date
   expressed in UTC. A spring example: the target date 2026-03-29 maps to `2026-03-29T00:00Z`
   (GMT). A BST example: 2026-07-01 maps to `2026-06-30T23:00Z`. Checked on 2026-10-13: the 12,932
   silver rows carry 1,634 distinct `timestamp_utc` values, equal to the 1,634 distinct target
   dates. It is not the capture time. It is a **calendar-date anchor**, not the start of any
   EFA block: EFA 1 starts at 23:00 local the day before (table above), and all six blocks of
   a target date share one `timestamp_utc`. The `EFA_n` columns stay wide.

The record's issue recipe is `none`. `Forecast_Created` is kept as a **raw string**, not an
issue clock, for these reasons:

- It changes format inside the one file: **12,476 values are day-first** (`%d/%m/%Y`) and
  **456 are ISO** (`%Y-%m-%d`), in the same header epoch. A single date format cannot read
  both, and the column is raw to avoid silently dropping rows. Raw storage reads the body
  faithfully with no validation failures, so this is not an unreadable-resource failure.
- It is a date, with no time and no zone. It does not say when during the day the issue was
  published.
- Eight rows carry the creation date `2026-10-08`, which is **later than the archive's own
  CKAN `last_modified` date** (`2026-10-07`); they are the last 8 physical lines of the CSV
  (lines 12,926 to 12,933). The production label and the upload vintage therefore cannot be
  treated as one clock.
- Between the earliest and latest creation dates, **15 creation dates are missing** from the
  archive. NESO calls the file a daily-updated archive and gives no completeness or
  immutability guarantee for past issues. `TODO: verify` the vendor's retention and
  amendment behaviour.

**Forward-target test (why the vintage cannot stand in for the issue time).** Against the
vintage, 12,912 rows have a target date on or before the CKAN `last_modified` and 20 after (at
EFA-block grain, 77,456 block starts on or before and 136 after, using the vendor's local
block boundaries). Most of the archive's targets are therefore in the past relative to the
vintage, so the vintage cannot show when any of them was available.

**Coverage (structure only).** 1,618 distinct creation labels and 1,634 distinct target dates;
creation dates span 2022-04-20 to 2026-10-08 and target dates 2022-04-21 to 2026-10-11. Two
service codes (`DC-H`, `DC-L`), as in the current file.

**Units (vendor dictionary).** `EFA_1` to `EFA_6` are declared with the unit spelling `MWs`
in the
[history dictionary](https://www.neso.energy/data-portal/dynamic-containment-4-day-forecast/dynamic_containment_4_day_forecast_-_history).
The dictionary's prose for the same fields explicitly describes the values as **megawatts**, so
the spelling is read as MW and **not** as megawatt-seconds (FACTS §4.5). The two dictionaries
therefore agree on MW. `Forecast_Created` and `Forecast_Target_Date` are dates; `Service_Type`
is text. None of these carries a physical unit.

**Sentinels and missing values (FACTS g5).** The same full-body scan as the current file found
no blank cells, `-1`, `N/A`, `NA`, `NULL`, `null` or `NaN` tokens, no padded cells, and no
embedded commas or percent signs. No null token is declared and no column has a null in
silver. Zero is a numeric zero and is kept; the vendor's reason for any zero is not stated
(`TODO: verify`). No bounds are imposed and no value is converted.

**Identity and selection.** The key is `(forecast_created, forecast_target_date,
service_type)`, unique in the capture. The pair `(forecast_target_date, service_type)` is
**not** a key: it repeats up to 5 times per pair because the archive holds several issues per
target, and a key without the creation label would drop 9,664 rows. `TODO: verify` the
vendor's issue identity and retention. `_latest` is `whole_capture`. A per-key latest would
need a true `issue_time`, which waits on the hold below.

**Activation (2026-10-13, master `7e3c023`).** Transformed at cutoff 2026-10-08:
**12,932 silver rows**, equal to the planned count, with no prior silver overwritten.
Reconcile `--all --cutoff 2026-10-12` exited 0 with 159 families, 0 gaps, 47 adjudicated and
0 stale (gridflow `@.planning/v0.22-RESULTS.md` §AS-1; RULINGS 725).

Silver columns beyond the vendor columns in both families: `timestamp_utc`, `published_at`,
`bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id`,
`dataset_version` (all timestamps tz-aware UTC; `dataset_version` `1+e1` = record version 1,
epoch 1). Silver lives under `silver/neso_data_portal/<family>/year=2026/month=10/`.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Status: Live
  - Update Frequency: Daily
- Captured once per refresh run: sampled, not complete.

The current file is a rolling window: each publication replaces the previous four-day forecast,
so a refresh run keeps only the forecast present at capture time. The history file is described
by the vendor as a daily-updated archive of earlier issues. Captures to date: one per family
(2026-10-08), so successive-capture behaviour (rows amended, dropped or appended between
captures) is **unmeasured**.

- `TODO: verify` what time of day the files are republished (both captures' CKAN
  `last_modified` is about 13:05 UTC on 2026-10-07).
- `TODO: verify` whether each day's current forecast is appended to the history file and
  whether archived rows are ever amended. Only repeated captures compared row by row can show
  this.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `dc_forecast_4d`: held: TODO: DC-DATE-ORDER — `Date` is published as dd/mm/yyyy or mm/dd/yyyy? The dictionary documents ISO dates; every captured value is ambiguous. (unit v0.22-K-AS-1)
- `dc_forecast_4d_history`: held: TODO: DC-HISTORY-ISSUE — when was each creation-labelled issue published? 8 rows are created after the upload's last-modified date and 15 creation dates are missing from the archive. (unit v0.22-K-AS-1)

Both holds were set by the AS-1 unit and activated unchanged (RULINGS 718, 720, 723, 725).
Silver output for both exists on disk, but neither family may be published or used
point-in-time. This page publishes no data values from either.

`dc_forecast_4d` lifts when NESO states the slash-date order for this resource (or an
unambiguous current-format date is captured) and the rolling-horizon contract corroborates it
(FACTS §7). `dc_forecast_4d_history` lifts when NESO supplies a publication instant or
availability definition for each creation-labelled issue, and explains the creation dates that
postdate the upload, with retention evidence for the missing dates. Until then the creation
label is never promoted to `issue_time`, and the CKAN vintage is never used as a stand-in for
the original availability.

Related holds from the same unit (gridflow `@docs/neso_data_portal/eligibility.md`): the
balancing-reserve archive and medium-term families (@balancing-reserve-auction-requirement-forecast.md)
and the long-term DC/DM/DR forecast (@long-term-forecasts-for-dc-dm-dr-requirements.md). The
dynamic moderation, dynamic regulation and quick-reserve requirement families are eligible
(@dynamic-moderation-requirements.md, @dynamic-regulation-requirements.md,
@quick-reserve-auction-requirement-forecast.md).
