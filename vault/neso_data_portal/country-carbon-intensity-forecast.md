---
source: "neso_data_portal"
package: "country-carbon-intensity-forecast"
dataset_key: "country_ci_forecast"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-09
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Country Carbon Intensity Forecast

A half-hourly carbon intensity series for each of Great Britain's three countries
(Scotland, England, Wales), in grams of CO2 per kWh of electricity consumed. The
vendor dictionary calls every value a forecast, "predicted using machine learning
models and metered generation". It is the country tier of the Carbon Intensity
service: regions 15 (England), 16 (Scotland) and 17 (Wales) of the Carbon Intensity
API (`neso` source, @../../neso/datasets/regional_england.md,
@../../neso/datasets/regional_scotland.md, @../../neso/datasets/regional_wales.md),
published here as one wide CSV with one column per country. Its siblings are the
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
  value is 2026-10-08T09:10:31.323607Z. It is the CKAN `last_modified` of the
  resource, not the time any single row was forecast. The file is an `upload` resource, and
  the epoch declares `issue: none`, so there is no evidenced issue time.
- **Event clock (`utc_instant(datetime)`).** `event_time` = `timestamp_utc` = the
  vendor `datetime`, parsed as UTC. It is the **start** of the half-hour it labels. The
  vendor dictionary documents the timestamp as UTC (field-info `country_ci_forecast`,
  `datetime`: "Timestamp of record, given in UTC"). The start-of-period position was
  measured by the seat (`.planning/phases/v0.22-K-CI/LIVE-PROBE.md` in gridflow). The
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
  capture. Silver keeps them as nulls (1,311 nulls per column, matching the bronze
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
  capture has 141,009 distinct `datetime` values, with 0 duplicates and 0 missing
  keys. The vendor does not guarantee that a `datetime` names the same logical record
  across revisions.
- The `_latest` mode is `whole_capture`: `silver_neso_data_portal_country_ci_forecast_latest`
  returns every row of the newest complete capture (ADR-034 P-10). It does not pick
  the latest row per key across captures. This avoids assuming that rows dropped from
  a newer file still hold. The base view `silver_neso_data_portal_country_ci_forecast`
  is the full vintage archive; filter it with `available_at <= :as_of` for
  point-in-time reads.
- TODO: verify whether the vendor rolls, appends to or rewrites the file. Settling
  this needs repeated captures of the same resource, and only one exists so far
  (FACTS CI-1).

#### Silver at activation

| Property | Value |
|---|---|
| Activation cutoff | 2026-10-08 (one capture) |
| Rows | 141,009 (= planned count; `timestamp_utc` unique) |
| Path | `C:/gridflow-data/silver/neso_data_portal/country_ci_forecast/year=2026/month=10/` |
| Lineage columns | `timestamp_utc`, `event_time`, `published_at`, `available_at`, `capture_written_at`, `bronze_capture_id`, `source_run_id`, `dataset_version` (`1+e1`) |
| Reconcile | `--all --cutoff 2026-10-08`: 0 gaps for this family |

The CKAN `datastore_search` total read at 2026-10-08T12:04Z was 141,013 rows, against
141,009 in the 09:15Z CSV capture. The two reads were three hours apart on an hourly
resource, so they are not expected to reconcile. TODO: verify whether the CSV
download and the datastore table are always the same body.

## Cadence

- Registry refresh: intraday
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Hourly
- Intraday: captured once per refresh run — sampled, not complete

The vendor lists the update frequency as Hourly. TODO: verify how the file changes
between updates: whether it rolls, appends or rewrites. Only one capture exists so
far (FACTS CI-1). No scheduled gridflow refresh exists yet (OWNER 457–460), so new
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
- @../../neso/README.md — Carbon Intensity API (`neso` source), the live counterpart for region ids 15–17
- gridflow `docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md` (vintage clock, `_latest`)
- gridflow `.planning/phases/v0.22-K-CI/K-CI-FACTS.md` §2.3, §3.1–3.2 and `LIVE-PROBE.md`
- gridflow `.planning/v0.22-RESULTS.md` §CI; RULINGS 521, 523–526
- gridflow registry `src/gridflow/connectors/neso_data_portal/registry/country-carbon-intensity-forecast.json`
