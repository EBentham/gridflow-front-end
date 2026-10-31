---
source: "neso_data_portal"
package: "national-carbon-intensity-forecast"
dataset_key: "national_ci_forecast"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: National carbon intensity forecast
  summary: >-
    NESO's forecast and estimated actual carbon intensity of GB electricity per half hour, in
    gCO2/kWh, with a band.
  facts:
    vendor: "NESO Data Portal, package National Carbon Intensity Forecast: a CSV and methodology PDF"
    cadence: "Hourly, NESO says"
    grain: "Each row: one UTC half hour, with forecast, estimated actual and band"
    history: "NESO's October 2026 files start on 1 January 2018"
  landscape: power
  what_it_is: >-
    NESO defines carbon intensity as CO2 emitted per kWh of electricity consumed. Per half hour: a
    forecast, an actual estimated from metered generation and a band like `very low`. NESO's May
    2024 methodology opens with its Carbon Intensity API, forecasting 48 hours ahead. NESO's 16
    October 2026 file changed actuals its 8 October file gave for past half hours.
  how_used:
    - "GB carbon intensity per half hour, as NESO estimates it from metered generation"
    - "NESO's forecast for the two days after its latest file"
    - "Timing flexible demand to the lower-intensity half hours"
  chart:
    type: line
    silver: neso_data_portal/national_ci_forecast
    time: datetime
    filter:
      - {column: published_at, op: eq, value: "2026-10-16T20:10:47.063996"}
      - {column: datetime, op: gt, value: "2026-10-16T20:10:47"}
      - {column: forecast, op: not_null}
    values:
      - {column: forecast, series: forecast}
    aggregation: last
    window: {start: "2026-10-16", end: "2026-10-18"}
    unit: gCO2/kWh
  chart_view:
    title: GB forecast after NESO's 16 October 2026 file
    caption: >-
      Silver `national_ci_forecast`, gCO2/kWh: the forecast in NESO's file of 16 October 2026 for
      each half hour after the file last changed, 20:30 that day to 22:30 on 18 October. The file
      has no actual for these half hours.
    alt: >-
      Line chart from neso_data_portal/national_ci_forecast of NESO's GB forecast in gCO2/kWh for
      the 101 half hours after its file of 16 October 2026 last changed, 20:30 that day to 22:30 on
      18 October. It falls from 101 to 63 at 11:00 on 17 October, rises to 135 that evening, dips to
      85 at 11:30 on 18 October, peaks at 136 at 21:30 that evening and ends at 121.
    x_label: "Half-hour start, UTC"
    key:
      - {series: forecast, label: Forecast, codes: forecast, paint: petrol, note: "NESO's forecast; the file gives no time it was made"}
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show`, then the CSV and methodology PDF, downloaded whole
      unless `last_modified` is unchanged. Its October 2026 CSVs end in about four weeks of empty rows.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=national-carbon-intensity-forecast"
      - "GET https://api.neso.energy/dataset/f406810a-1a36-48d2-b542-1dfb1348096e/resource/0e5fde43-2de7-4fb4-833d-c7bca3b658b0/download/gb_carbon_intensity.csv"
      - "GET https://api.neso.energy/dataset/f406810a-1a36-48d2-b542-1dfb1348096e/resource/36638178-e993-4d34-afdc-4ada83993585/download/neso-ci-national-methodology_v2.pdf"
    commands:
      - {run: gridflow ingest neso_data_portal national_ci_forecast --last 24h, comment: "the CSV to bronze"}
      - {run: gridflow transform neso_data_portal national_ci_forecast --last 24h, comment: "the capture's date to silver"}
      - {run: gridflow ingest neso_data_portal national_ci_forecast_files --last 24h, comment: "the methodology PDF, bronze only"}
  record:
    select:
      filter:
        - {column: datetime, op: in, value: ["2026-10-07T19:30:00", "2026-10-07T20:00:00", "2026-10-07T20:30:00", "2026-10-07T21:00:00"]}
      order_by: [datetime, published_at]
      columns: [datetime, forecast, actual, index, published_at]
    key: [datetime, published_at]
    caption: "7 October 2026: four half hours whose actual changed between NESO's 8 and 16 October files."
    fields:
      datetime: "Half-hour start, UTC; gridflow matched it to NESO's API, the file does not say"
      forecast: "NESO's forecast, gCO2/kWh; no column says when it was made"
      actual: "Estimated from metered generation, gCO2/kWh, NESO says; a later file can change it"
      index: "NESO's band for the intensity, such as `low`; its thresholds are unstated"
      published_at: "NESO's last-modified time for the file, read as UTC; one per file"
      timestamp_utc: "Equal to `datetime`: the half-hour start, UTC"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote the capture to bronze, UTC
  caveat: No row says when its forecast was made, and NESO rewrites actuals for past half hours.
  notebook:
    lead: >-
      `query()` reads the `_latest` view, NESO's 16 October 2026 file, filtering half-hour starts,
      both ends included. Past forecasts carry no issue time, so the plot draws estimated actuals only.
    cells:
      - |
        df = data.neso_data_portal.query("national_ci_forecast", "2026-10-09", "2026-10-15")
        df = df.sort_values("timestamp_utc").assign(datetime=lambda d: d.datetime.dt.tz_convert("UTC"))
        df[["datetime", "forecast", "actual", "index"]].head()
      - |
        ax = df.set_index("datetime")["actual"].plot(
            figsize=(8, 3.5), color="#155A6E", ylim=(0, 250),
            xlabel="Half-hour start, UTC", ylabel="actual, gCO2/kWh")
      - |
        df["index"].value_counts()
    needs: NESO's 16 October 2026 file
    plot_alt: >-
      Line plot of NESO's estimated actual GB intensity in gCO2/kWh per half hour, 9 to 15 October
      2026, from its file of 16 October. It runs from 31 at 12:00 on 10 October to 209 at 17:00 on 11
      October, then peaks at 153 and 169 early on 12 and 14 October and 174 on the evening of 15 October.
  related:
    - {dataset: neso/carbon_intensity, note: "The Carbon Intensity API's national routes, which this package's methodology describes"}
    - {dataset: neso_data_portal/regional-carbon-intensity-forecast, note: "NESO's forecast for 14 GB regions, in the same unit"}
    - {dataset: neso_data_portal/country-carbon-intensity-forecast, note: "NESO's forecast for England, Scotland and Wales, in the same unit"}
    - {dataset: neso_data_portal/historic_generation_mix, note: "NESO's half-hourly generation mix, which carries its own carbon intensity"}
---

# National Carbon Intensity Forecast

GB national carbon intensity of electricity per half-hour, published by NESO as a single CSV on
the Open Data Portal. Each row carries a UTC half-hour label, a **forecast** intensity (the
vendor dictionary says it is predicted with machine-learning models), an **actual** intensity
(the dictionary says it is estimated from metered generation), and a categorical **index** of
the relative level of intensity. Intensity measures the CO2 emitted per kWh of electricity
consumed. NESO's text does not say it is the series the Carbon Intensity API's national routes
serve (gridflow ingests those under the `neso` source, @../../neso/datasets/carbon_intensity.md);
its methodology PDF only opens with that API. gridflow's own probe of 2026-10-09
(LIVE-PROBE) found forecast and actual equal on all 675 periods the two overlapped. Like the API, which sends no issue time either, the
CSV has **no issue column**: each target half-hour holds exactly one forecast/actual pair, with
no record of which forecast run produced it. The silver output is held in gridflow because that
issue clock is missing (FACTS CI-1, g2; see Holds); the site page shows its rows with that caveat.

- Publisher group: Carbon intensity
- Registry group: carbon-intensity1 · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| National Carbon Intensity Forecast | CSV | upload | `0e5fde43-2de7-4fb4-833d-c7bca3b658b0` |

- Download: [gb_carbon_intensity.csv](https://api.neso.energy/dataset/f406810a-1a36-48d2-b542-1dfb1348096e/resource/0e5fde43-2de7-4fb4-833d-c7bca3b658b0/download/gb_carbon_intensity.csv)
  (CKAN datastore active; datastore unique key `datetime`).
- Captured: `raw_20261008T111249Z_0e5fde43-2de7-4fb4-833d-c7bca3b658b0_8beca58c.csv`,
  5,874,687 bytes, 155,159 data rows, one header epoch; and
  `raw_20261016T204040Z_0e5fde43-2de7-4fb4-833d-c7bca3b658b0_5ac01f8b.csv`, 5,889,754 bytes,
  155,561 data rows, same header (CKAN `last_modified` 2026-10-16T20:10:47.063996).

### DOC

| Resource | Format | Capture | Id |
|---|---|---|---|
| National Carbon Intensity Forecast Methodology | PDF | upload | `36638178-e993-4d34-afdc-4ada83993585` |

- Download: [neso-ci-national-methodology_v2.pdf](https://api.neso.energy/dataset/f406810a-1a36-48d2-b542-1dfb1348096e/resource/36638178-e993-4d34-afdc-4ada83993585/download/neso-ci-national-methodology_v2.pdf)
  (CKAN `last_modified` 2024-10-01T03:16:37Z).
- Captured: `raw_20261008T111254Z_36638178-e993-4d34-afdc-4ada83993585_85da2e89.pdf`,
  359,920 bytes. Catalogue only: no silver output. It is still primary evidence for the
  methodology and is cited below.

## Families

### `national_ci_forecast`

- Kind: tabular · archetype: FC · refresh: intraday · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| datetime | `datetime` | datetime | `%Y-%m-%dT%H:%M:%S` | no | UTC | — |
| forecast | `forecast` | float64 | — | yes | — | gCO2/kWh |
| actual | `actual` | float64 | — | yes | — | gCO2/kWh |
| index | `index` | string | — | yes | — | — |

- Entity key: `datetime`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`datetime`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured resource. For the 2026-10-08 capture that is
   `2026-10-08T11:11:23.285254`, and for the 2026-10-16 capture `2026-10-16T20:10:47.063996`,
   which CKAN emits without an offset. gridflow reads it as UTC
   (gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`, D-15). Every
   silver row of a capture shares this one vintage. It says when the file changed, not when
   any individual forecast was issued.
2. **Event time (`utc_instant` on `datetime`).** `event_time` = `timestamp_utc` = `datetime`.
   All three are equal on every silver row (checked 2026-10-09). `datetime` is the **UTC start**
   of the half-hour it labels. The vendor dictionary documents the column as UTC. The seat's
   probe of 2026-10-09 (local silver, no network) joined the captured CSV to the Carbon Intensity API silver, whose `from` is the
   period start: forecast and actual matched on all 675 overlapping periods when joined on
   period start, and on fewer than 1 in 10 when joined on period end
   (gridflow `@.planning/phases/v0.22-K-CI/LIVE-PROBE.md`). Event time is therefore **not** the
   capture time here. The "`none` = capture time" fallback applies to sibling families
   (regional, balancing actions), not this one.

DST check: London-local days 2024-03-31 / 2024-10-27 / 2025-03-30 / 2025-10-26 hold
46 / 50 / 46 / 50 periods after activation, as UTC labels should.

**Units (vendor dictionary only, [NESO data dictionary](https://www.neso.energy/data-portal/national-carbon-intensity-forecast/national_carbon_intensity_forecast)).**
`forecast` and `actual` are **gCO2/kWh**, as the dictionary
states for each field (`unit: gCO2/kWh`). `index` is a text category the dictionary describes as
"Index describing the relative level of the carbon intensity" (its example is `very low`). It
has no physical unit. `TODO: verify` the complete vendor list of index labels and their band
thresholds. The dictionary does not enumerate them.

**Sentinels and missing values (FACTS g5).** The vendor declares no sentinel spelling, and the
record's null-token map is empty.

- Empty `forecast`, `actual` and `index` cells are kept as **null**. The full-body census of the
  2026-10-08 capture counted 2,901 blank `forecast`, 3,732 blank `actual` and 2,901 blank `index`
  cells; the 2026-10-16 capture has the same three counts. In each capture 1,339 of the
  all-blank rows are the file's tail: the 2026-10-08 file runs to 2026-11-07T11:00:00 with its
  last forecast at 2026-10-10T13:30:00, the 2026-10-16 file to 2026-11-15T20:00:00 with its last
  forecast at 2026-10-18T22:30:00 (about four weeks of empty future half-hours).
  `TODO: verify` why particular observations are absent. Only the vendor can settle it.
- Numeric **zeros** in `actual` are preserved as values, not converted to null.
  `TODO: verify` whether a zero actual is a real estimate or an error marker.
- A small number of `forecast` values the vendor has not explained are preserved **unclipped**,
  and no upper bound is imposed. `TODO: verify` with a vendor correction or explanation.

**Identity and selection.** `datetime` was unique across each whole body (155,159 distinct on
2026-10-08, 155,561 on 2026-10-16, no duplicates or missing keys). It is kept as the entity key only as a **capture
uniqueness guard**. No vendor text guarantees that a `datetime` identifies one stable record
across revisions, so `_latest` is `whole_capture` (the newest capture wins as a whole) rather
than per-key selection.

**Activation (2026-10-09, master `1ceeaab`).** The family was transformed with cutoff
2026-10-08 (one capture). Silver has **155,159 rows**, equal to the planned count, with
`timestamp_utc` unique. Reconcile at cutoff 2026-10-08 found 0 gaps for this family. No prior
silver existed, so nothing was overwritten (gridflow `@.planning/v0.22-RESULTS.md` §CI;
RULINGS 523–525). A second Parquet file (155,561 rows) now holds the 2026-10-16 capture, and
`_latest` takes it whole.

Silver columns beyond the four vendor columns: `timestamp_utc`, `published_at`,
`bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id`,
`dataset_version` (all timestamps tz-aware UTC; `dataset_version` `1+e1` = record version 1,
epoch 1).

**Supersedes the research proposal.** The batch research (gridflow
`@.planning/phases/v0.22-K-CI/K-CI-FACTS.md` §2.1, T01/T02) proposed `temporal: none` with
`datetime` kept as a raw string, because it could not tell period start from period end. The
seat's live probe then established period start, and RULINGS 521 shipped the record as
`utc_instant` on a parsed UTC `datetime`. Where FACTS and this page disagree on the temporal
recipe, the registry record and this page are current.

### `national_ci_forecast_files`

- Kind: files · archetype: FC · refresh: intraday · empty allowed: no
- files: catalogue only

This family captures the methodology PDF (see DOC above). Its extracted text says estimated
data becomes available at the end of a settlement period and that forecasts are provided ahead
of real time. That is publication-timing evidence only. Read 2026-10-24 (`pdftotext`): it gives
"Issue: May 2024" and opens "NESO's Carbon Intensity API provides an indicative trend of carbon
intensity for the electrical grid of Great Britain up to 48 hours ahead of real-time", the tie
the page's related link to the `neso` national routes rests on. Its next sentence says the
report "details the methodology behind the regional carbon intensity estimates", although this
is the national package's file; the regional package's PDF opens the same way. No body was
captured on 2026-10-16. It does not on its own fix whether
the CSV's `datetime` labels the start or the end of the period. The live probe settled that
(see above).

## Cadence

- Registry refresh: intraday
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Hourly
- Intraday: captured once per refresh run — sampled, not complete

The vendor updates the file hourly. gridflow captures one snapshot per refresh run, so hourly
states between runs are not retained. `TODO: verify` whether each hourly update rewrites past
targets, appends new ones, or rolls the window. Only more captures of the same resource,
compared target by target, can show this.

**Second capture (2026-10-16), compared with the first** (Polars on both bronze bodies, values
compared as numbers, read 2026-10-24). The later file keeps all 155,159 earlier targets, drops
none and appends 402 (2026-11-07T11:30:00 to 2026-11-15T20:00:00, all blank). On shared
targets, 402 blank rows were filled, and values changed as follows:
- `actual` changed on 30 targets from 2026-10-07T10:30:00 to 2026-10-08T10:00:00, all past
  when the first file was modified (2026-10-08T11:11:23); for example 124 to 123 at
  2026-10-07T10:30:00. NESO revises its estimated actuals after the period.
- `forecast` changed on 100 targets from 2026-10-08T11:30:00 to 2026-10-10T13:30:00, all
  ahead of the first file; no forecast changed for a target already past at the first
  capture. The file keeps one forecast per target and overwrites it, so a past target's value
  is the last one written, with no record of when.
- `index` changed on 8 targets on 2026-10-08 (`moderate` to `low`).
No scheduled gridflow refresh exists yet, so
captures are on demand (gridflow `@.planning/v0.22-RESULTS.md` §CI).

Observed (no inference drawn): the CKAN datastore reported a `total` of 155,163 records in a
field-info read at 2026-10-08T13:14Z, about two hours after the capture (written
2026-10-08T11:12:49Z), against 155,159 rows in the captured CSV.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `national_ci_forecast`: held: TODO: no issue column; which forecast issue a past target's value reflects, and whether values are revised after the period, is undocumented (unit E-SEM)

The silver output exists on disk, but it is **held** in gridflow: it is not eligible for
point-in-time model use until unit E-SEM answers the question above (RULINGS 521). The
resource carries no forecast-issue clock. A past half-hour's `forecast` may come from any
earlier forecast run, and the vendor does not say whether the stored value is replaced after the
period closes. Without that, the CKAN vintage is the only availability clock. It bounds when
the file existed, not when each value was known. This note gives schema, units and counts.
Under ruling 66 (2026-10-24) the site page shows the rows, with one line naming the question:
its chart draws only forecasts for half hours after the 16 October 2026 file last changed, and
its notebook plots estimated actuals alone, so no past forecast is drawn as known beforehand.

Partial evidence for E-SEM, recorded here without lifting the hold: the CKAN resource metadata
shows `datastore_unique_keys: ["datetime"]` and `datastore_append_or_update: true`.
`TODO: verify` whether the vendor's datastore append-or-update on `datetime` means past targets
are overwritten in place, and whether the downloadable CSV follows the datastore.

The package-level `eligibility: eligible` in the front matter refers to the package registry
entry. The hold is per family and sits on `national_ci_forecast`.

Related holds (gridflow `@docs/neso_data_portal/eligibility.md`): `country_ci_forecast` is
held on the same issue-clock question. `regional_ci_forecast` is held on it too, and also on
period position and on the meaning of negative intensities. `ci_balancing_actions` is held on
period position only. All are unit E-SEM.
