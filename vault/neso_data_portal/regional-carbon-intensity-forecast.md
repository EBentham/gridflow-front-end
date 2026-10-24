---
source: "neso_data_portal"
package: "regional-carbon-intensity-forecast"
dataset_key: "regional_ci_forecast"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  held: "No row says when NESO first published it; half-hour labels and negative values are unexplained."
  title: Carbon intensity forecast by region
  summary: >-
    NESO's forecast carbon intensity of electricity per half hour for 14 GB regions drawn on
    distribution network operator (DNO) boundaries, in gCO2/kWh.
  facts:
    vendor: "NESO Data Portal, package Regional Carbon Intensity Forecast: a CSV and methodology PDF"
    cadence: "Hourly, NESO says"
    grain: "Each row: one UTC half hour, with a forecast for each region"
    history: "NESO's October 2026 files run from 17 September 2018 to 24 July 2026"
  landscape: power
  what_it_is: >-
    NESO defines carbon intensity as CO2 emitted per kWh of electricity consumed. One column per
    region gives NESO's forecast; NESO does not say whether each time starts or ends its half hour.
    Its May 2024 methodology describes regional forecasts in its Carbon Intensity API. Two regions
    carry negative values in NESO's October 2026 files, which it does not explain.
  how_used:
    - "Regional differences in GB grid carbon intensity, per half hour"
    - "Weighting regional demand by forecast intensity for emissions estimates"
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show`, then the CSV and PDF, downloaded whole unless
      `last_modified` is unchanged. Fetched 16 October 2026, the CSV matched 8 October's byte for byte.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=regional-carbon-intensity-forecast"
      - "GET https://api.neso.energy/dataset/bf3d723b-b4ae-4ec7-9fc9-e584c651a9da/resource/c16b0e19-c02a-44a8-ba05-4db2c0545a2a/download/regional_carbon_intensity.csv"
      - "GET https://api.neso.energy/dataset/bf3d723b-b4ae-4ec7-9fc9-e584c651a9da/resource/1d817f4c-a126-45c8-baf0-218bf57d37be/download/neso-ci-regional-methodology_v2.pdf"
    commands:
      - {run: gridflow ingest neso_data_portal regional_ci_forecast --last 24h, comment: "the CSV to bronze"}
      - {run: gridflow transform neso_data_portal regional_ci_forecast --last 24h, comment: "the capture's date to silver"}
      - {run: gridflow ingest neso_data_portal regional_ci_forecast_files --last 24h, comment: "the methodology PDF, bronze only"}
  related:
    - {dataset: neso/regional_intensity, note: "The Carbon Intensity API's regional routes, which this package's methodology describes"}
    - {dataset: neso_data_portal/country-carbon-intensity-forecast, note: "NESO's forecast for England, Scotland and Wales, in the same unit"}
    - {dataset: neso_data_portal/national-carbon-intensity-forecast, note: "NESO's GB forecast, with an estimated actual beside it"}
---

# Regional Carbon Intensity Forecast

NESO publishes this package on its CKAN Open Data Portal. It contains the half-hourly
**forecast carbon intensity of electricity (gCO2/kWh)** for each of the 14 GB DNO
regions. The vendor dictionary says the forecasts are "predicted using machine learning
models and metered generation". Its methodology PDF (May 2024) describes the regional
forecasts of NESO's Carbon Intensity API, whose `/regional` endpoints gridflow ingests
separately as the `neso` source (@../../neso/README.md,
@../../neso/datasets/regional_regionid.md). No values have been compared: the API silver
starts after this file's populated targets end, so nothing says the two carry the same figures. The file is
**wide**: one `datetime` column plus one value column per region, with region names as
column headers rather than as values of a region-id column. You might use it for a long
regional history of the forecast without paging the API, for example to study geographic
dispersion of grid carbon or to weight regional load by marginal emissions. Concept
background: @../../../20-domain/concepts/carbon-intensity.md. The file has no issue column,
and in both captures (2026-10-08 and 2026-10-16) the populated targets stop well before the capture date (see
"Target coverage" below). So it is **not** a point-in-time forecast archive and not a
current forward forecast. gridflow's silver output is **held** (unit E-SEM).

- Publisher group: Carbon intensity
- Registry group: carbon-intensity1 · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Regional Carbon Intensity Forecast | CSV | upload | `c16b0e19-c02a-44a8-ba05-4db2c0545a2a` |

- Download: [regional_carbon_intensity.csv](https://api.neso.energy/dataset/bf3d723b-b4ae-4ec7-9fc9-e584c651a9da/resource/c16b0e19-c02a-44a8-ba05-4db2c0545a2a/download/regional_carbon_intensity.csv)
  (the URL is the same in the 2026-10-06 catalogue snapshot and in the 2026-10-08 capture sidecar)
- Captured 2026-10-08T11:16:58Z: 13,180,555 bytes, 136,190 data rows, one header epoch;
  CKAN `last_modified` 2026-10-08T11:11:10.800726
- Captured again 2026-10-16T20:43:07Z: the same body byte for byte (13,180,555 bytes,
  `body_sha256` `0b435a16…` in both sidecars), under CKAN `last_modified`
  2026-10-16T20:10:38.828649

### DOC

| Resource | Format | Capture | Id |
|---|---|---|---|
| Regional Carbon Intensity Forecast Methodology | PDF | upload | `1d817f4c-a126-45c8-baf0-218bf57d37be` |

- Download: [neso-ci-regional-methodology_v2.pdf](https://api.neso.energy/dataset/bf3d723b-b4ae-4ec7-9fc9-e584c651a9da/resource/1d817f4c-a126-45c8-baf0-218bf57d37be/download/neso-ci-regional-methodology_v2.pdf)
  (419,571 bytes; CKAN `last_modified` 2024-10-01T03:14:20.020531)
- Catalogue only: bronze keeps the file, and there is no silver output. Its extracted text
  covers forecast resolution, regular forecast updates and a geographical figure of the
  regions. It does **not** say whether the CSV `datetime` marks the start or the end of the
  period (K-CI-FACTS §2.14, C5). The figure is not readable as a text crosswalk.

## Families

### `regional_ci_forecast`

- Kind: tabular · archetype: FC · refresh: intraday · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| datetime | `datetime` | string | — | yes | — | — |
| North Scotland | `north_scotland` | float64 | — | yes | — | gCO2/kWh |
| South Scotland | `south_scotland` | float64 | — | yes | — | gCO2/kWh |
| North West England | `north_west_england` | float64 | — | yes | — | gCO2/kWh |
| North East England | `north_east_england` | float64 | — | yes | — | gCO2/kWh |
| Yorkshire | `yorkshire` | float64 | — | yes | — | gCO2/kWh |
| North Wales and Merseyside | `north_wales_and_merseyside` | float64 | — | yes | — | gCO2/kWh |
| South Wales | `south_wales` | float64 | — | yes | — | gCO2/kWh |
| West Midlands | `west_midlands` | float64 | — | yes | — | gCO2/kWh |
| East Midlands | `east_midlands` | float64 | — | yes | — | gCO2/kWh |
| East England | `east_england` | float64 | — | yes | — | gCO2/kWh |
| South West England | `south_west_england` | float64 | — | yes | — | gCO2/kWh |
| South England | `south_england` | float64 | — | yes | — | gCO2/kWh |
| London | `london` | float64 | — | yes | — | gCO2/kWh |
| South East England | `south_east_england` | float64 | — | yes | — | gCO2/kWh |

- Entity key: `datetime`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

#### The two clocks

- **Vintage: `ckan_last_modified`.** `published_at` and `available_at` both equal the
  CKAN `last_modified` of the captured resource. For the 2026-10-08 capture that is
  2026-10-08T11:11:10.800726Z, and for the 2026-10-16 capture 2026-10-16T20:10:38.828649Z,
  taken from the bronze sidecars. Every silver row of a capture
  carries this single value. It records when NESO last replaced the file, not when any
  forecast was issued. The record declares issue `none`, and no column carries an issue
  time.
- **Event time: recipe `none`.** `timestamp_utc` and `event_time` are the **capture
  time**, not the target half-hour. They hold the bronze write instant (2026-10-08T11:16:58Z
  and 2026-10-16T20:43:07Z for the two captures), so every row in a capture has the same value. The target half-hour
  exists only in the raw `datetime` string. The vendor dictionary describes it as
  "Timestamp of record, given in UTC". In the captured body every value matches
  `%Y-%m-%dT%H:%M:%S`: 136,190 values, all distinct, none null.
  `TODO: verify` whether `datetime` marks the **start or the end** of the half-hour. For
  the national and country files, the seat's API join (LIVE-PROBE) proved period start. It
  could not be measured for this file: the API regional silver starts after the CSV's
  populated targets end, so there is no overlap. Do not carry the national finding over.
  Until this is settled, `datetime` stays a raw string, and that is why no `utc_instant`
  recipe is applied.

#### Units

Each of the 14 value columns is `gCO2/kWh`. The vendor field dictionary states this for
every column, at `FI(regional_ci_forecast)` lines :34, :46, :58, :70, :82, :94, :106, :118,
:130, :142, :154, :166, :178 and :190 in header order (K-CI-FACTS §2.2 g4). The unit is not
inferred from column names. The dictionary gives `datetime` unit `N/A` and zone UTC.

#### Sentinels and nulls (K-CI-FACTS g5)

- Blank cells in value columns become null. Every value column is nullable.
- **No null token is declared.** `-1`, other negative values and `0` are kept as signed
  float values. gridflow does not map `-1` to null and does not apply a non-negative bound,
  because no vendor statement says these values are missing-data markers.
- Negative intensities do occur in the captured body, and not only as an isolated `-1`.
  `TODO: verify` whether they are genuine model outputs, error sentinels or some other
  vendor convention. A vendor dictionary statement or correction notice would settle it.
- Long runs of zeros occur in at least one region column. `TODO: verify` whether a zero
  means a true zero forecast or missing data. The values are kept as they are.
- Value statistics are deliberately not published here while the family is held.

#### Keys and `_latest`

`datetime` is a **capture uniqueness guard**, not a proven vendor identity. In the
2026-10-08 body it is unique, with no duplicates and no missing keys (K-CI-FACTS §2.2 T03).
`_latest` uses `whole_capture`, the newest capture taken whole, because one capture cannot
show whether NESO rolls, appends to or rewrites the file. `key_latest` could keep targets
that a newer snapshot has dropped. The 2026-10-16 capture is byte-identical to the
2026-10-08 one, although CKAN `last_modified` moved by eight days: NESO re-stamped the file
without changing it, so two captures show neither appends nor rewrites. Silver holds a
second Parquet file of the same 136,190 rows, and `_latest` takes it whole.
`TODO: verify` rolling, append or rewrite behaviour by comparing captures across a change
of body (K-CI-FACTS §3.1).

#### Target coverage

In both captures, every populated region column ends at target
`2026-07-24T12:00:00`, while the resource's CKAN `last_modified` is 2026-10-08, then
2026-10-16. A recent
file modification is therefore **not** evidence that the targets are current. Do not
treat this file as a live forward forecast. `TODO: verify` the vendor's explanation of
this target cutoff. Use the Carbon Intensity API (`neso` source) for current regional
forecasts.

#### Region crosswalk (CSV label → Carbon Intensity API `regionid`)

The CSV keeps its 14 wide columns, and silver does not unpivot them. To join this file to
the `neso` source, use this mapping. It matches names only (K-CI-FACTS §3.2 and gridflow's
probe of 2026-10-09); no values have been compared, and the methodology PDF's API covers 17
regions against this file's 14 columns.

| CSV column | API `regionid` | API quick-start name | Live API `shortname` |
|---|---:|---|---|
| North Scotland | 1 | North Scotland | — |
| South Scotland | 2 | South Scotland | — |
| North West England | 3 | North West England | — |
| North East England | 4 | North East England | — |
| Yorkshire | 5 | South Yorkshire | Yorkshire (dnoregion `NPG Yorkshire`) |
| North Wales and Merseyside | 6 | North Wales, Merseyside and Cheshire | North Wales & Merseyside |
| South Wales | 7 | South Wales | — |
| West Midlands | 8 | West Midlands | — |
| East Midlands | 9 | East Midlands | — |
| East England | 10 | East England | — |
| South West England | 11 | South West England | — |
| South England | 12 | South England | — |
| London | 13 | London | — |
| South East England | 14 | South East England | — |

Twelve labels match the API quick-start region list exactly (K-CI-FACTS §3.2). The other
two names differ from the quick-start list. They do match the `shortname` that the live
API returns for regionid 5 and 6 (`&` ↔ `and`), as measured from the `neso` regional
silver in LIVE-PROBE. That closes the alias question. A "—" means the shortname was not
recorded separately because the label already matches exactly. Countries 15–17 (England,
Scotland, Wales) belong to the sibling package
@country-carbon-intensity-forecast.md, not to this file.

### `regional_ci_forecast_files`

- Kind: files · archetype: FC · refresh: intraday · empty allowed: no
- files: catalogue only

This family captures the methodology PDF (DOC disposition) to bronze only. It has no
silver output and no clocks. The download link is listed above. Read 2026-10-24
(`pdftotext`): it gives "Issue: May 2024" and opens "NESO's Carbon Intensity API has been
extended to include forecasts for 17 geographical regions of the GB electricity system up to
48 hours ahead of real-time", the tie the page's related link to the `neso` regional routes
rests on. It says GB regions follow Distribution Network Operator (DNO) boundaries. No body
was captured on 2026-10-16.

## Cadence

- Registry refresh: intraday
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Hourly
- Intraday: captured once per refresh run — sampled, not complete

The vendor says the file updates hourly. gridflow keeps only the bodies it captures, so
any intermediate hourly versions between captures are lost. Activation took exactly one
capture (2026-10-08); a second (2026-10-16) found the same body under a new `last_modified`.
There is currently no scheduled refresh task, so new captures come
only from sweep runs.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

## Holds

- `regional_ci_forecast`: held: TODO: no issue column; which forecast issue a past target's value reflects, and whether values are revised after the period, is undocumented; whether datetime marks period start or end; meaning of negative intensities (min -13.0) (unit E-SEM)

In plain terms, the silver output is written but held from publication until the
semantics work (unit E-SEM) answers three questions:

1. **Issue and revision:** which forecast issue a past target's value reflects, and
   whether values are rewritten after the period. With no issue column, a row cannot be
   placed at the time it was known.
2. **Period position:** whether `datetime` marks the start or the end of the period. This
   could not be measured against the API (see "The two clocks").
3. **Negatives:** what negative intensities mean (see "Sentinels and nulls").

The seat ruled the hold in RULINGS 521 (detail in K-CI-SPEC). The package-level
`eligibility: eligible` refers to the package. The hold applies only to this family.

## Activation receipt

- Frozen record merged in PR #88, squash `1ceeaab`, triple-green (RULINGS 523).
- Activation (RULINGS 524/525): cutoff 2026-10-08, one capture, no earlier silver and
  nothing overwritten. `gridflow transform neso_data_portal regional_ci_forecast --start
  2026-10-08 --end 2026-10-08` wrote **136,190 rows**, which equals the planned count.
  Reconcile with `--cutoff 2026-10-08` found 0 gaps for this family.
- Silver path:
  `C:/gridflow-data/silver/neso_data_portal/regional_ci_forecast/year=2026/month=10/`
  (one Parquet file at activation; a second, from the 2026-10-16 capture, since). Besides the 15 record columns, silver carries the engine columns
  `timestamp_utc`, `published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`,
  `available_at`, `source_run_id` and `dataset_version`. All timestamps are tz-aware UTC.

## Implementation delta and open items

- **Dictionary vs body format:** the dictionary example for `datetime` is
  `17/09/2018  02:30:00` (day-first, double space), but the captured body is ISO
  `%Y-%m-%dT%H:%M:%S`. `TODO: verify` whether older bodies used the dictionary format. One
  epoch has been observed, so history cannot be checked yet.
- **Region names:** the API quick-start list and the CSV disagree for regions 5 and 6. The
  live API `shortname` agrees with the CSV (see the crosswalk above).
- **Methodology PDF:** catalogued but not used to settle period position. Its text does
  not address it.
- `TODO: verify` period start or end, issue and revision behaviour, the meaning of
  negatives and zeros, cross-capture behaviour, and the reason for the target cutoff.

## References

- Vendor: @../README.md (NESO Open Data Portal, CKAN mechanics, ADR-030 clocks)
- Carbon Intensity API (the `neso` source): @../../neso/README.md,
  @../../neso/datasets/regional_regionid.md
- Sibling packages: @national-carbon-intensity-forecast.md,
  @country-carbon-intensity-forecast.md
- Concept: @../../../20-domain/concepts/carbon-intensity.md
- gridflow evidence (gridflow checkout, `.planning/` is local):
  `.planning/phases/v0.22-K-CI/K-CI-FACTS.md` §1, §2.2, §2.14, §3.1, §3.2, §3.5;
  `.planning/phases/v0.22-K-CI/LIVE-PROBE.md`; `.planning/v0.22-RESULTS.md` §CI;
  `.planning/RULINGS.md` 521, 523–525
- Registry record:
  `src/gridflow/connectors/neso_data_portal/registry/regional-carbon-intensity-forecast.json`;
  eligibility report `docs/neso_data_portal/eligibility.md`
- Vendor dictionary: [NESO data dictionary](https://www.neso.energy/data-portal/regional-carbon-intensity-forecast/regional_carbon_intensity_forecast)
