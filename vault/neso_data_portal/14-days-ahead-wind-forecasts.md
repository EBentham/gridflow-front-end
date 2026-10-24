---
source: "neso_data_portal"
package: "14-days-ahead-wind-forecasts"
dataset_keys: ["wind_forecast_14d_day_ahead_bmu", "wind_forecast_14d_days_ahead"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  held: true
  title: 14-day wind forecast
  summary: >-
    NESO's forecast of GB wind output for each half-hour out to 14 days ahead, in MW, nationally
    and per wind BM unit.
  facts:
    vendor: "NESO Data Portal, package `14-days-ahead-wind-forecasts`: 2 CSV files"
    cadence: "8 times a day, NESO says, at no stated times"
    grain: "One row per half-hour; in the BMU file, per half-hour and BM unit"
  landscape: power
  what_it_is: >-
    NESO's forecast of wind output, in MW, for each half-hour over 14 days, beside operational
    wind capacity on the transmission network. NESO says these forecasts feed its day-ahead
    incentive wind forecast and leave out licence-exempt wind farms. The national file states when
    its forecast was produced. The BMU file splits it by wind BM unit, with region and capacity.
  how_used:
    - Benchmark a medium-range wind model against NESO's forecast, half-hour by half-hour
    - Trace NESO's day-ahead incentive wind forecast back to its two-week inputs
    - Attach a two-week wind forecast to individual wind BM units, by unit name
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then each CSV downloaded whole unless its
      `last_modified` is unchanged. Each file holds one 14-day window and replaces the last.
    commands:
      - {run: gridflow pipeline neso_data_portal wind_forecast_14d_days_ahead --last 24h,
         comment: "national file to bronze, then silver"}
      - {run: gridflow pipeline neso_data_portal wind_forecast_14d_day_ahead_bmu --last 24h,
         comment: "BMU file to bronze, then silver"}
  family:
    slug: 14-days-ahead-wind-forecasts
    members:
      - dataset: wind_forecast_14d_days_ahead
        differs: "National forecast and operational wind capacity, with the time NESO says it was produced"
        request:
          - "GET https://api.neso.energy/api/3/action/package_show?id=14-days-ahead-wind-forecasts"
          - "GET https://api.neso.energy/dataset/2f134a4e-92e5-43b8-96c3-0dd7d92fcc52/resource/93c3048e-1dab-4057-a2a9-417540583929/download/14da_wind_forecast.csv"
        held: "All rows stay out: NESO's October 2026 files open with half-hours before their forecast time, unexplained."
      - dataset: wind_forecast_14d_day_ahead_bmu
        differs: "The same forecast per wind BM unit, with region and capacity; no forecast time"
        request:
          - "GET https://api.neso.energy/api/3/action/package_show?id=14-days-ahead-wind-forecasts"
          - "GET https://api.neso.energy/dataset/2f134a4e-92e5-43b8-96c3-0dd7d92fcc52/resource/342aae25-d3a6-436c-b168-db8b247ccb83/download/14da_windunit_forecast.csv"
        held: "All rows stay out: NESO's files open with half-hours before publication, and carry no forecast time."
  related:
    - {dataset: neso_data_portal/day-ahead-wind-forecast, note: "NESO's day-ahead incentive wind forecast, which NESO says these forecasts feed"}
    - {dataset: neso_data_portal/14-days-ahead-operational-metered-wind-forecasts, note: "NESO's daily 14-day forecast for farms that send it SCADA metering"}
    - {dataset: elexon/windfor, note: "Elexon's wind generation forecast, issued several times a day"}
    - {dataset: elexon/bmunits_reference, note: "Elexon's BM unit register, to look up the BMU file's units"}
---

# 14 Days Ahead Wind Forecasts

NESO's medium-term GB **wind generation forecast**, 0–14 days ahead at half-hour resolution. It is
published as two CSV uploads on the Open Data Portal:

- **National forecast.** One half-hourly curve of forecast transmission-connected wind output.
  Each row also carries the total operational wind capacity and the time the forecast was
  produced (`ForecastDateTime`).
- **BMU forecast.** The same half-hourly horizon broken down by wind **BM unit**. Each row
  carries the unit's name, full name, region and capacity.

The package notes say these forecasts are the ones "used to produce NESO's national day ahead
incentive wind forecasts" (see @day-ahead-wind-forecast.md). The notes also say they are based
on evaluated **Operational Capacity**. This is a deterministic value derived from recent actual
output of each BMU, captured from SCADA telemetry (operational metering). Both resource
descriptions say the set is "not a complete list of BMU's within NESO systems and excludes
licence-exempt windfarms". It therefore covers transmission-visible wind, not total GB wind
including embedded generation. A model that needs embedded wind must add it from elsewhere
(see @embedded-wind-and-solar-forecasts.md).

**Both families are held (unit E-SEM).** Neither file passes the forward-target rule of
RULINGS 529: some targets in each capture start at or before the capture's CKAN
`last_modified`, so the vintage cannot serve as an issue-time proxy for every row. The BMU file
also has no issue column. See Holds. This page therefore gives schema, clocks and counts only,
and no data values.

Related series:

- Elexon WINDFOR (@../../elexon/datasets/windfor.md) is the closest Elexon wind forecast. The
  local WINDFOR store has **zero** target overlap with the current NESO bodies, so no
  value cross-check exists (K-GEN-1-FACTS §5).
- @14-days-ahead-operational-metered-wind-forecasts.md is the sibling package on the same
  0–14 day horizon. Its current files are eligible: every target lies after the vintage.
- BMU identifiers can be joined to Elexon reference data
  (@../../elexon/datasets/bmunits_reference.md). See the BMU family below.

- Publisher group: Generation
- Registry group: generation · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| 14 Day Ahead Wind BMU Forecast | CSV | upload | `342aae25-d3a6-436c-b168-db8b247ccb83` |
| 14 Days Ahead Wind Forecast | CSV | upload | `93c3048e-1dab-4057-a2a9-417540583929` |

Both resources are SILVER. The package has no DOC resources, so it has no PDF/DOCX
methodology and no `_files` family. Package id `2f134a4e-92e5-43b8-96c3-0dd7d92fcc52`.

- **14 Days Ahead Wind Forecast** → `wind_forecast_14d_days_ahead` (held).
  Download: [14da_wind_forecast.csv](https://api.neso.energy/dataset/2f134a4e-92e5-43b8-96c3-0dd7d92fcc52/resource/93c3048e-1dab-4057-a2a9-417540583929/download/14da_wind_forecast.csv).
  Captured: `raw_20261008T114200Z_93c3048e-1dab-4057-a2a9-417540583929_276f1185.csv`,
  46,257 bytes, 672 data rows. Second capture:
  `raw_20261016T204827Z_93c3048e-1dab-4057-a2a9-417540583929_3783cd3f.csv`, 46,176 bytes, 672 data
  rows, same header.
- **14 Day Ahead Wind BMU Forecast** → `wind_forecast_14d_day_ahead_bmu` (held).
  Download: [14da_windunit_forecast.csv](https://api.neso.energy/dataset/2f134a4e-92e5-43b8-96c3-0dd7d92fcc52/resource/342aae25-d3a6-436c-b168-db8b247ccb83/download/14da_windunit_forecast.csv).
  Captured: `raw_20261008T114156Z_342aae25-d3a6-436c-b168-db8b247ccb83_cd363d08.csv`,
  12,223,991 bytes, 155,232 data rows. Second capture:
  `raw_20261016T204824Z_342aae25-d3a6-436c-b168-db8b247ccb83_2967d1e7.csv`, 12,212,455 bytes,
  155,232 data rows, same header.

Both filenames **appear fixed**: they matched in the 2026-10-06 catalogue snapshot and in the
2026-10-08 and 2026-10-16 captures. That is unlike the date-stamped demand-forecast files, but two observations
do not establish a vendor policy. Even so, resolve the URL from the CKAN resource and do not hard-code it.

Both resources are `datastore_active` in CKAN. The datastore totals at a field-info read on
2026-10-08 (672 / 155,232) matched the captured row counts. Each capture has one header epoch.
**Both bodies start with a UTF-8 BOM** (in both captures), and the other GEN-1 bodies do not (FACTS C10). The
reader strips it, so the first silver column is `datetime`, not `﻿Datetime`. A test pins
this (gridflow `@tests/unit/test_neso_gen1_records.py`, `test_bom_bodies_type_their_first_column`).

## Families

### `wind_forecast_14d_day_ahead_bmu`

- Kind: tabular · archetype: FC · refresh: intraday · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Datetime | `datetime` | datetime | `%Y-%m-%dT%H:%M:%SZ` | no | UTC | UTC ISO 8601 |
| Date | `date` | date | `%Y-%m-%d` | yes | — | — |
| Settlement_Period | `settlement_period` | int64 | — | yes | — | — |
| Generator_Name | `generator_name` | string | — | yes | — | — |
| Generator_Full_Name | `generator_full_name` | string | — | yes | — | — |
| Region | `region` | string | — | yes | — | — |
| Capacity | `capacity` | float64 | — | yes | — | MW |
| Wind_Forecast | `wind_forecast` | float64 | — | yes | — | MW |

- Entity key: `datetime`, `generator_name`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`datetime`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Held (unit E-SEM). This page gives schema, clocks and counts only, and no data values.**

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the capture's CKAN
   `last_modified`, `2026-10-08T11:30:44.268960`. CKAN emits it without an offset, and gridflow
   reads it as UTC (gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`).
   Every row of a capture shares this vintage. The file has **no issue column**, so the
   vintage is the only availability clock. Do not borrow the national file's
   `ForecastDateTime` for this family (FACTS §2). No filename token is evidenced as an issue
   instant either.
2. **Event time (`utc_instant` on `datetime`).** `timestamp_utc` = `event_time` = `Datetime`,
   the target settlement period's **start** in UTC. It is **not the capture time**, and the
   `none` fallback (timestamp_utc = capture time) does not apply to this family. Checks on all
   155,232 silver rows (2026-10-09): `timestamp_utc` equals `datetime` on every row, and
   `datetime` equals UK-local midnight of `date` + 30 min × (`settlement_period` − 1) on every
   row.

**Hold question.** 693 rows have a target at or before the vintage. These are the three
half-hours starting 2026-10-08 10:30, 11:00 and 11:30 UTC, each × 231 generators. With no issue
column, nothing shows when each value became available. The past-target rows may be forecasts
or retrospective values (FACTS GEN1-1, C06). The same three targets cause the national
family's hold. The 2026-10-16 capture repeats the pattern: its CKAN `last_modified` is
`2026-10-16T20:30:47.916675`, and 693 rows (the half-hours starting 19:30, 20:00 and 20:30 UTC on
2026-10-16, × 231 generators) sit at or before it (silver, read 2026-10-24).

**Shape of a capture (counts only).** 155,232 rows = 672 half-hourly targets (14 days × 48)
× 231 generators. Every target has exactly 231 rows. In the 2026-10-08 capture the targets run
from 2026-10-08 10:30 UTC to 2026-10-22 10:00 UTC, and settlement periods are 1–48 (that capture
spans no clock change). In the 2026-10-16 capture they run from 2026-10-16 19:30 UTC to
2026-10-30 19:00 UTC; 25 October 2026 (the autumn clock change) has periods 1–50, and the
start-of-period mapping on `date` and `settlement_period` holds on every row. Both captures name
the same 231 generators. In both captures the generators' `wind_forecast` and `capacity` sum
exactly to the national file's values at every target (silver, read 2026-10-24).
There are 10 distinct `region` values. The vendor defines the regions as ITL 1 regions for England
and DNO licence areas for Wales and Scotland, extended to their national borders. Offshore
regions use IHO Sea Areas, split by the land area the connection reaches. No vendor column has
a null cell.

**Generator identifiers: the dictionary and the body disagree.** The vendor dictionary describes
`Generator_Name` as an "Anonymised generator name" (example `WINDFARM_1`). In the captured body,
all **231** distinct names exactly match an Elexon `national_grid_bm_unit` value and **0** match
`bm_unit_id` (FACTS §5). gridflow stores the names as-is, with no prefixing or normalisation.
`TODO: verify` with NESO whether the dictionary text is stale.

**Units (vendor dictionary only: CKAN datastore field info for resource `342aae25…`, read 2026-10-08; [package page](https://www.neso.energy/data-portal/14-days-ahead-wind-forecasts)).**
`Capacity` and `Wind_Forecast` are **MW** (`unit: MW`; dictionary type `numeric`, cast to
float64). The BMU dictionary reuses the national description for `Capacity` ("the total
operational wind capacity that is connected to the National Grid Transmission Network").
`TODO: verify` that the BMU column is the unit's own evaluated operational capacity. The package
notes imply it, but the field text does not say so. `Settlement_Period` is a settlement index,
not a physical quantity. `Datetime`'s "unit" is the clock encoding `UTC ISO 8601`.

**Sentinels and missing values (FACTS g5).** No null-token map is declared. Full-body checks
found no `N/A`, `NA`, literal `-1` or numeric −1 in any value column, and no blank cells. Zero
values occur in both value columns, including zero forecasts against positive capacity and
generator-long zero runs. No vendor source says a zero means missing or unavailable, so zeros are
kept as numbers. No bounds are imposed, and negative values would be preserved.
`TODO: verify` the vendor's zero/missing-value policy.

**Identity.** `datetime + generator_name` was measured unique over the full body. No vendor text
declares it a contractual key, so the entity key is a capture guard and `_latest` is
`whole_capture`: the newest capture wins as a whole (FACTS g3, §2 T04).
`TODO: verify` the vendor revision key. Because each upload replaces the whole 14-day window,
history across uploads lives only in the dated silver captures.

**Activation (2026-10-09, master `f19effb`).** Cutoff 2026-10-08, one capture at activation: **155,232 rows**,
equal to the planned count. No prior silver existed, so nothing was overwritten. Reconcile
`--all --cutoff 2026-10-08` found 0 gaps across 55 recorded families (gridflow
`@.planning/v0.22-RESULTS.md` §GEN-1; RULINGS 542, 545, 546).

Silver columns beyond the vendor columns: `timestamp_utc`, `published_at`,
`bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id`,
`dataset_version`. All timestamps are tz-aware UTC. `dataset_version` `1+e1` = record version 1,
epoch 1. This is the same for both families.

**Settlement-period wording (applies to both families).** Both dictionaries describe
`Settlement_Period` as periods "of 30 minutes ending at the half hour or hour". That describes
the interval, not the label. The `Datetime` label matches the period **start** on every row of
both families, and on every Elexon PN date/SP pair in the local store (FACTS g1, C09).
Do not shift `Datetime` by 30 minutes.

### `wind_forecast_14d_days_ahead`

- Kind: tabular · archetype: FC · refresh: intraday · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Datetime | `datetime` | datetime | `%Y-%m-%dT%H:%M:%SZ` | no | UTC | UTC ISO 8601 |
| Date | `date` | date | `%Y-%m-%d` | yes | — | — |
| Settlement_Period | `settlement_period` | int64 | — | yes | — | — |
| Capacity | `capacity` | float64 | — | yes | — | MW |
| Wind_Forecast | `wind_forecast` | float64 | — | yes | — | MW |
| ForecastDateTime | `forecast_datetime` | datetime | `%Y-%m-%dT%H:%M:%SZ` | no | UTC | UTC ISO 8601 |

- Entity key: `datetime`, `issue_time`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`datetime`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Held (unit E-SEM). This page gives schema, clocks and counts only, and no data values.**

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the capture's CKAN
   `last_modified`, `2026-10-08T11:30:47.254827`, read as UTC (ADR-030). This is the only
   availability clock gridflow uses. It is deliberately **not** replaced by `ForecastDateTime`:
   no source guarantees that the stated production instant dates the availability of these
   exact values, so `issue_time_evidenced` is not used (FACTS g2).
2. **Event time (`utc_instant` on `datetime`).** `timestamp_utc` = `event_time` = `Datetime`,
   the target settlement period's **start** in UTC. It is **not the capture time**, and the
   `none` fallback does not apply. Both start-convention checks held on all 672 silver rows
   (2026-10-09).

**Issue time (a third column, not an availability clock).** The record declares
`ForecastDateTime` as the issue column. The vendor dictionary defines it as the "Date and time
of when the forecast is produced", unit `UTC ISO 8601`. Silver keeps it twice: as
`forecast_datetime` and as the derived `issue_time`, which is equal on every row and is part of
the entity key. The 2026-10-08 capture has **one** distinct issue, `2026-10-08T11:30:00Z`, for
all 672 targets (FACTS GEN1-1). It sits 47 seconds before the CKAN vintage. The 2026-10-16
capture likewise has one issue, `2026-10-16T20:30:00Z`, 51 seconds before its CKAN vintage
`2026-10-16T20:30:51.163278`.

**Hold question.** Three targets sit at or before the CKAN vintage: the half-hours starting
10:30, 11:00 and 11:30 UTC on 2026-10-08. Two of them start strictly before the stated production
instant, and the third (11:30) starts exactly at it. The frozen hold line below says "before
both", but the measured split is 2 strictly before and 1 equal. The 2026-10-16 capture has the
same split: 19:30 and 20:00 UTC strictly before its stated instant, 20:30 equal to it. Open points:

- whether the body mixes retrospective values with forecasts for those first half-hours;
- whether `ForecastDateTime` dates the availability of every row;
- whether past values are immutable across uploads.

Neither the issue column nor its UTC unit settles this (FACTS §2).

**Shape of a capture (counts only).** 672 rows, one per half-hourly target (14 days × 48). In
the 2026-10-08 capture they run from 2026-10-08 10:30 UTC to 2026-10-22 10:00 UTC, with
settlement periods 1–48 and no clock change. In the 2026-10-16 capture they run from 2026-10-16
19:30 UTC to 2026-10-30 19:00 UTC; 25 October 2026 has periods 1–50, and the start-of-period
mapping holds on every row. `datetime` and `datetime + issue_time` were both measured unique. No vendor
column has a null cell.

**Units (vendor dictionary only: CKAN datastore field info for resource `93c3048e…`, read 2026-10-08; [package page](https://www.neso.energy/data-portal/14-days-ahead-wind-forecasts)).**
`Capacity` is **MW**: "the total operational wind capacity that is connected to the National
Grid Transmission Network". `Wind_Forecast` is **MW**: the "Wind forecast for each half hourly
settlement period". Both have dictionary type `int4` and are cast to float64, which leaves
integer values unchanged. `Settlement_Period` is a settlement index. `Datetime` and
`ForecastDateTime` carry the clock encoding `UTC ISO 8601`.

**Sentinels (FACTS g5).** No null token is declared. Full-body checks found no `N/A`, `NA`,
literal `-1` or numeric −1, no blank cells and no zero value cells. Zeros and negatives would
be preserved, and no bounds are imposed.

**Identity.** `_latest` is `whole_capture`, and the entity key `datetime + issue_time` is a
capture guard, not a vendor-declared key (FACTS §2 T05). `TODO: verify` the vendor revision key.

**Activation.** **672 rows**, equal to the planned count (cutoff 2026-10-08, RULINGS 546).

## Cadence

- Registry refresh: intraday
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: 8 times/day
- Intraday: captured once per refresh run — sampled, not complete

"8 times/day" is the only vendor statement of cadence. `TODO: verify` the upload times and
whether each upload replaces the whole window. gridflow's intraday refresh captures one state
per run, so uploads between runs are lost. The dated silver captures are therefore a sample of
the vendor's issue history, not the full history.

Observed at capture (no inference drawn): the 2026-10-08 national `ForecastDateTime` is
11:30:00 UTC, and both files' CKAN `last_modified` values fall at 11:30:44–11:30:47 UTC. The
2026-10-16 national `ForecastDateTime` is 20:30:00 UTC, and both files' values fall at
20:30:47–20:30:51 UTC. The 2026-10-06 catalogue snapshot recorded both files at about 19:30 UTC.
Each new file replaces the whole window: the 2026-10-16 files keep none of the 2026-10-08
targets before 2026-10-16 19:30 UTC.

No scheduled gridflow refresh exists yet. Captures are on demand.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `wind_forecast_14d_day_ahead_bmu`: held: TODO: 693 target rows sit at or before the CKAN vintage and the body has no issue column; there is no evidence of when each value was available (unit E-SEM)
- `wind_forecast_14d_days_ahead`: held: TODO: 3 target rows sit before both the stated production instant and the CKAN vintage; whether the body mixes retrospective values with forecasts, and whether ForecastDateTime dates the availability of every row (unit E-SEM)

Both held outputs exist in silver, but neither is eligible for publication or point-in-time
model use until unit E-SEM answers its question (RULINGS 529, 542). This page publishes their
schema, clocks and row counts only.

Both holds come from the same 3 targets: the half-hours starting 10:30, 11:00 and 11:30 UTC on
2026-10-08. In the BMU file that is 3 × 231 generators = 693 rows. The 2026-10-16 capture
repeats it with the half-hours starting 19:30, 20:00 and 20:30 UTC on 2026-10-16 (3 national
rows, 693 BMU rows), so the past targets are not a one-off (FACTS GEN1-1 asked whether later
captures include them).

- **What would lift the BMU hold:** an issue-bearing publication history, or vendor evidence of
  when each forecast vintage became available. A narrower fix would be a vendor statement that
  the window always starts at a future half-hour; a filter on target > vintage could then make
  the remainder eligible under RULINGS 529. That is a design decision for unit E-SEM, not a
  current behaviour.
- **What would lift the national hold:** a vendor explanation of the first half-hours (forecast
  versus retrospective values), plus evidence that `ForecastDateTime` is the immutable
  instant at which every row was available.

The package-level `eligibility: eligible` in the front matter refers to the package registry
entry. Holds are per family, and **neither** family in this package is eligible.

Related, same unit and batch (gridflow `@docs/neso_data_portal/eligibility.md`; RULINGS 542):

- The current metered 14-day wind files (@14-days-ahead-operational-metered-wind-forecasts.md)
  are eligible: every target lies after the vintage.
- The current day-ahead wind and BMU files are eligible on the same rule. The historic
  day-ahead national and BMU archives are held (@day-ahead-wind-forecast.md).
- Daily NRAPM is eligible. Weekly NRAPM is held on undocumented value scales.
- Daily and weekly OPMR are held.
