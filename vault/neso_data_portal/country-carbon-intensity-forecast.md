---
source: "neso_data_portal"
package: "country-carbon-intensity-forecast"
dataset_key: "country_ci_forecast"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  held: "No row says when NESO first published it, and NESO changes values for past half hours."
  title: Carbon intensity forecast by country
  summary: >-
    NESO's forecast carbon intensity of electricity per half hour for Scotland, England and Wales,
    in gCO2/kWh.
  facts:
    vendor: "NESO Data Portal, package Country Carbon Intensity Forecast: one CSV"
    cadence: "Hourly, NESO says"
    grain: "Each row: one UTC half hour, with a forecast for each country"
    history: "NESO's October 2026 files start on 17 September 2018"
  landscape: power
  what_it_is: >-
    NESO defines carbon intensity as CO2 emitted per kWh of electricity consumed. The file has one
    column each for Scotland, England and Wales, and NESO calls every value a forecast, from
    machine-learning models and metered generation. NESO's 16 October 2026 file changed values its
    8 October file gave for past half hours.
  how_used:
    - "Scotland, England and Wales intensity side by side, per half hour"
    - "Timing flexible demand in one country to its lower-intensity half hours"
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then the CSV, downloaded whole unless its
      `last_modified` is unchanged.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=country-carbon-intensity-forecast"
      - "GET https://api.neso.energy/dataset/d8084aa3-8c9e-425c-bf0d-51e0441fc241/resource/e032e7aa-dea5-4695-80d6-19739142021d/download/country_carbon_intensity.csv"
    commands:
      - {run: gridflow ingest neso_data_portal country_ci_forecast --last 24h, comment: "the CSV to bronze"}
      - {run: gridflow transform neso_data_portal country_ci_forecast --last 24h, comment: "the capture's date to silver"}
  related:
    - {dataset: neso_data_portal/national-carbon-intensity-forecast, note: "NESO's GB-wide forecast, with an estimated actual beside it"}
    - {dataset: neso_data_portal/regional-carbon-intensity-forecast, note: "NESO's forecast for 14 GB regions, in the same unit"}
---

# Country Carbon Intensity Forecast

A half-hourly carbon intensity series for each of Great Britain's three countries
(Scotland, England, Wales), in grams of CO2 per kWh of electricity consumed. The
vendor dictionary calls every value a forecast, "predicted using machine learning
models and metered generation". It is one wide CSV with one column per country.
NESO's text for this package does not link it to the Carbon Intensity API. gridflow's
own probe of 2026-10-09 (LIVE-PROBE) matched 2,167 of 2,169 values to the API's regions
15 (England), 16 (Scotland) and 17 (Wales) (`neso` source,
@../../neso/datasets/regional_england.md, @../../neso/datasets/regional_scotland.md,
@../../neso/datasets/regional_wales.md); that is the project's measurement, not a NESO
statement. Its siblings are the
national series (@./national-carbon-intensity-forecast.md) and the 14-region series
(@./regional-carbon-intensity-forecast.md).

**Read this first.** The silver output is **held** (see Holds). The file has no
forecast-issue column, so a value at a past half-hour cannot be tied to the forecast
that produced it. It is not known whether values are revised after the period. The
rows are parsed, timed and stored, but they are not handed off as a point-in-time
forecast series.

- Publisher group: Carbon intensity
- Registry group: carbon-intensity1 · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Country Carbon Intensity Forecast | CSV | upload | `e032e7aa-dea5-4695-80d6-19739142021d` |

The package has one resource, and it is SILVER. It has no DOC, GIS, COVERED or
ingest-only files.

| Resource | Disposition | Download |
|---|---|---|
| Country Carbon Intensity Forecast (CSV, `datastore_active: true`) | SILVER → `country_ci_forecast` | [country_carbon_intensity.csv](https://api.neso.energy/dataset/d8084aa3-8c9e-425c-bf0d-51e0441fc241/resource/e032e7aa-dea5-4695-80d6-19739142021d/download/country_carbon_intensity.csv) |

- Package id `d8084aa3-8c9e-425c-bf0d-51e0441fc241`; author "National Grid Electricity
  System Operator"; created 2020-05-06 (catalogue snapshot `20261006T195819Z`).
- Vendor dictionary page:
  [country_carbon_intensity_forecast](https://www.neso.energy/data-portal/country-carbon-intensity-forecast/country_carbon_intensity_forecast).
- The CKAN Datastore metadata for this resource declares `datastore_unique_keys:
  ["datetime"]` and `datastore_append_or_update: true`. This is the vendor's datastore
  configuration. It does not guarantee row identity across revisions (see Identity).

## Families

### `country_ci_forecast`

- Kind: tabular · archetype: FC · refresh: intraday · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| datetime | `datetime` | datetime | `%Y-%m-%dT%H:%M:%S` | no | UTC | — |
| Scotland | `scotland` | float64 | — | yes | — | gCO2/kWh |
| England | `england` | float64 | — | yes | — | gCO2/kWh |
| Wales | `wales` | float64 | — | yes | — | gCO2/kWh |

- Entity key: `datetime`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`datetime`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

#### The two clocks

- **Vintage clock (`ckan_last_modified`).** `available_at` = `published_at` = the CKAN
  `last_modified` of the resource at the moment gridflow captured it. Every row from one
  capture carries the same value. For the activation capture
  (`raw_20261008T091558Z_e032e7aa-…_5d621791.csv`, written 2026-10-08T09:15:58Z) that
  value is 2026-10-08T09:10:31.323607Z; for the 2026-10-16 capture
  (`raw_20261016T192126Z_e032e7aa-…_311c2cf4.csv`, written 2026-10-16T19:21:26Z) it is
  2026-10-16T19:10:24.514761Z. It is the CKAN `last_modified` of the
  resource, not the time any single row was forecast. The file is an `upload` resource, and
  the epoch declares `issue: none`, so there is no evidenced issue time.
- **Event clock (`utc_instant(datetime)`).** `event_time` = `timestamp_utc` = the
  vendor `datetime`, parsed as UTC. It is the **start** of the half-hour it labels. The
  vendor dictionary documents the timestamp as UTC (field-info `country_ci_forecast`,
  `datetime`: "Timestamp of record, given in UTC"). The start-of-period position was
  measured by the seat on 2026-10-09 (`.planning/phases/v0.22-K-CI/LIVE-PROBE.md` in gridflow). The
  CSV was unpivoted to Carbon Intensity API region ids 15/16/17 and joined to the API's
  own `from`/`to` periods. On period start, 2,167 of 2,169 values matched exactly. On
  period end, 755 of 2,169 matched. The two mismatches are left unexplained; revisions
  between the API read and the CSV capture are plausible. The research facts
  originally proposed `temporal: none`. The probe settled the period position, and
  RULINGS 521 moved the record to `utc_instant`. The values are therefore **not**
  capture-time stamped.
- DST check: silver has 46 rows on London-local 2024-03-31 and 2025-03-30, and 50 on
  2024-10-27 and 2025-10-26. This matches a UTC half-hour grid, not a naive London
  clock.

#### Units

The vendor dictionary gives the unit of all three value columns as **gCO2/kWh**
explicitly (field-info `unit` and description for Scotland, England and Wales). The
dictionary describes each one as a "Forecast … carbon intensity". `datetime` has no
unit.

#### Sentinels and missing values

- **Blank cells → null.** Each country column has 1,311 blank cells in the activation
  capture, and again in the 2026-10-16 capture. Silver keeps them as nulls (1,311 nulls per column, matching the bronze
  census). They are not filled, interpolated or zeroed. TODO: verify with NESO why
  particular half-hours are blank.
- **Zeros are preserved as values.** Numeric zeros occur in the Scotland and Wales
  columns. They are stored as `0.0` and are not converted to null. TODO: verify with
  NESO whether a zero is a real modelled intensity or a missing-data marker.
- The file is **not time-sorted**: it does not open on its earliest target. Sort by
  `timestamp_utc`, and never read file-order runs as chronological durations.
- The research census (FACTS §2.3 g5) records only blanks and zeros for this family.
  It names no textual sentinel such as `N/A`, and no negative values.

#### Identity and `_latest`

- `entity_key = ["datetime"]` is a **per-capture uniqueness guard**. The activation
  capture has 141,009 distinct `datetime` values and the 2026-10-16 capture 141,413, each
  with 0 duplicates and 0 missing keys. The vendor does not guarantee that a `datetime` names the same logical record
  across revisions.
- The `_latest` mode is `whole_capture`: `silver_neso_data_portal_country_ci_forecast_latest`
  returns every row of the newest complete capture (ADR-034 P-10). It does not pick
  the latest row per key across captures. This avoids assuming that rows dropped from
  a newer file still hold. The base view `silver_neso_data_portal_country_ci_forecast`
  is the full vintage archive; filter it with `available_at <= :as_of` for
  point-in-time reads.
- **Second capture (2026-10-16), compared with the first** (Polars on both bronze bodies,
  values compared as numbers, read 2026-10-24). The later file keeps all 141,009 earlier
  targets, drops none and appends 404 (2026-10-10T12:00:00 to 2026-10-18T21:30:00). Values
  changed on 110 shared targets from 2026-10-08T04:30:00 to 2026-10-10T11:30:00 (Scotland 6,
  England 105, Wales 110). Nine of them, 2026-10-08T04:30:00 to 2026-10-08T09:00:00 (England 4,
  Wales 9), carry labels before the first file's stamp (2026-10-08T09:10:31). Read as period
  starts, as this note does, the 09:00 half-hour was still running at that stamp, so eight
  (04:30 to 08:30; England 3, Wales 8) had already ended; for
  example Wales 67 to 68 at 2026-10-08T04:30:00. So NESO rewrites values after their half-hour,
  and the file keeps no record of earlier values or of when each was written. Both files end
  about 50 hours after their modified stamp.
- TODO: verify how far back and how often NESO rewrites values (two captures only, FACTS
  CI-1).

#### Silver at activation

| Property | Value |
|---|---|
| Activation cutoff | 2026-10-08 (one capture) |
| Rows | 141,009 (= planned count; `timestamp_utc` unique) |
| Path | `C:/gridflow-data/silver/neso_data_portal/country_ci_forecast/year=2026/month=10/` |
| Lineage columns | `timestamp_utc`, `event_time`, `published_at`, `available_at`, `capture_written_at`, `bronze_capture_id`, `source_run_id`, `dataset_version` (`1+e1`) |
| Reconcile | `--all --cutoff 2026-10-08`: 0 gaps for this family |
| Second capture | a second Parquet file of 141,413 rows from the 2026-10-16 capture; `_latest` takes it whole |

The CKAN `datastore_search` total read at 2026-10-08T12:04Z was 141,013 rows, against
141,009 in the 09:15Z CSV capture. The two reads were three hours apart on an hourly
resource, so they are not expected to reconcile. TODO: verify whether the CSV
download and the datastore table are always the same body.

## Cadence

- Registry refresh: intraday
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Hourly
- Intraday: captured once per refresh run — sampled, not complete

The vendor lists the update frequency as Hourly. Between the 2026-10-08 and 2026-10-16
captures the file appended new targets and rewrote some earlier ones, past ones included
(see Identity). TODO: verify whether it ever rolls old targets off (none were dropped in
those eight days). No scheduled gridflow refresh exists yet (OWNER 457–460), so new
captures come from manual or seat-run sweeps.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: <https://www.neso.energy/data-portal/ngeso-open-licence>. Any derived
output must carry the attribution line above verbatim.

## Holds

- `country_ci_forecast`: held: TODO: no issue column; which forecast issue a past target's value reflects, and whether values are revised after the period, is undocumented (unit E-SEM)

The hold was ruled in RULINGS 521, following the embedded-forecast precedent. Silver is
written and registered, but this output is **not** handed off to the front end or
models as a forecast series. Its values, ranges and samples are deliberately left
off this page. The question goes to unit **E-SEM**. It is settled by vendor
documentation of a real issue clock and of revision behaviour, or by enough repeated
captures to measure how the file changes. The hold covers the forecast semantics
only. The period position (UTC start) is settled.

## References

- @../README.md — NESO Data Portal vendor page (CKAN, file-download model)
- @./national-carbon-intensity-forecast.md · @./regional-carbon-intensity-forecast.md · @./carbon-intensity-of-balancing-actions.md
- @../../neso/README.md — Carbon Intensity API (`neso` source); gridflow's 2026-10-09 probe matched this file to its region ids 15–17
- gridflow `docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md` (vintage clock, `_latest`)
- gridflow `.planning/phases/v0.22-K-CI/K-CI-FACTS.md` §2.3, §3.1–3.2 and `LIVE-PROBE.md`
- gridflow `.planning/v0.22-RESULTS.md` §CI; RULINGS 521, 523–526
- gridflow registry `src/gridflow/connectors/neso_data_portal/registry/country-carbon-intensity-forecast.json`
