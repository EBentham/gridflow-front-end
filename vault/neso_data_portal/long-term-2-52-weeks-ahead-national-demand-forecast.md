---
source: "neso_data_portal"
package: "long-term-2-52-weeks-ahead-national-demand-forecast"
dataset_key: "demand_forecast_2_52w"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Long-term national demand forecast
  summary: >-
    NESO's forecast of GB national demand 2 to 52 weeks ahead: each week's peak and minimums, in MW.
  facts:
    vendor: "NESO Data Portal, package Long Term (2-52 weeks ahead) National Demand Forecast: one CSV"
    cadence: "Ad hoc, NESO says"
    grain: "Each row: one forecast week, by NESO's week number and year labels"
  landscape: power
  what_it_is: >-
    One row per week ahead, which NESO numbers as an ESI week under calendar and financial year
    labels: the date of the week's peak and, in MW, the peak, minimum, minimum daytime and minimum
    overnight demand. NESO counts national demand as GB's generation requirement, less station
    load, pumped storage pumping and interconnector exports. No column gives an issue time.
  how_used:
    - Weekly peak and minimum GB demand, which NESO labels 2 to 52 weeks ahead
    - "Balancing supply and demand positions, the purpose NESO states for it"
  chart:
    type: none
    reason: >-
      NESO defines no week calendar, so the weeks cannot be placed on a time axis and the page
      draws no chart; the notebook plots each peak at NESO's own peak date.
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then the CSV, downloaded whole unless its
      `last_modified` is unchanged.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=long-term-2-52-weeks-ahead-national-demand-forecast"
      - "GET https://api.neso.energy/dataset/edd6190a-66d4-480d-a125-88d32bd11c91/resource/903302b4-b577-4228-a347-b9917568b4e1/download/year_ahead_weekly.csv"
    commands:
      - {run: gridflow ingest neso_data_portal demand_forecast_2_52w --last 24h, comment: "a changed file to bronze"}
      - {run: gridflow transform neso_data_portal demand_forecast_2_52w --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: calendar_year, op: eq, value: 2027}
        - {column: esiwk, op: in, value: [26, 27, 28, 29, 30, 31, 32]}
      dedup: {"on": [calendar_year, esiwk, cdate_peak], order_by: capture_written_at}
      order_by: [cdate_peak]
      columns: [calendar_year, esiwk, cdate_peak, tsd_peak, tsd_min, day_min, night_min,
                financial_year, published_at, timestamp_utc]
    key: [calendar_year, esiwk, cdate_peak]
    caption: "2027's weeks 26 to 32, in peak-date order."
    fields:
      calendar_year: "NESO's calendar year label for the week; no week calendar given"
      esiwk: "NESO's ESI week number; in this file 2026 runs 42 to 53"
      cdate_peak: "Date of the week's peak demand, NESO says; no day boundary or zone"
      tsd_peak: "The week's peak demand, MW, per NESO's dictionary"
      tsd_min: "The week's minimum demand, MW; NESO gives no date for it"
      day_min: "The week's minimum daytime demand, MW; NESO does not define daytime"
      night_min: "The week's minimum overnight demand, MW; NESO does not define overnight"
      financial_year: "NESO's financial year label; NESO does not say when its year starts"
      published_at: "NESO's last-modified time for the file, read as UTC; not an issue time"
      timestamp_utc: "When gridflow captured the file, UTC; not the week the row forecasts"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  caveat: "NESO never defines its ESI weeks, and 2027's week 29 appears twice, with two peak dates."
  notebook:
    lead: >-
      `query()` filters on `timestamp_utc`, the capture time here, so these cells use `data.sql()`
      on the `_latest` view. Weeks stay NESO's year and week labels; the plot puts each peak at
      NESO's own peak date.
    cells:
      - |
        weeks = data.sql("""
            SELECT calendar_year, financial_year, esiwk, cdate_peak,
                   tsd_peak, tsd_min, day_min, night_min
            FROM silver_neso_data_portal_demand_forecast_2_52w_latest
            ORDER BY cdate_peak
        """)
        weeks[weeks.duplicated(["calendar_year", "esiwk"], keep=False)]
      - |
        weeks.groupby("calendar_year").esiwk.agg(["min", "max", "count"]).reset_index()
      - |
        ax = weeks.plot(x="cdate_peak", y="tsd_peak", style="o-", legend=False, color="#155A6E",
                        figsize=(8, 3.5), xlabel="NESO's peak date", ylabel="peak demand, MW");
    needs: NESO's long-term national demand forecast file
    plot_alt: >-
      NESO's weekly peak demand in MW, one dot per row at its peak date: 35,497 on 15 October
      2026, 43,519 on 5 January 2027 (after 38,162 on 30 December), 28,186 on 17 June, 43,175 on
      21 December, then 39,125 on 29 December 2027. Week 29's two dots, 21 and 22 July 2027, show
      28,673.
  related:
    - {dataset: neso_data_portal/2-14-days-ahead-national-demand-forecast, note: "NESO's national demand forecast 2 to 14 days ahead"}
    - {dataset: neso_data_portal/7-day-ahead-national-forecast, note: "A shorter-range NESO national demand forecast, for the next week"}
    - {dataset: neso_data_portal/historic-demand-data, note: "The national demand outturn NESO publishes, by half hour"}
---

# Long Term (2-52 weeks ahead) National Demand Forecast

NESO's **long-horizon weekly forecast of GB national demand**, published on the Open Data Portal
as one CSV and updated "on an ad hoc basis" (resource description). The package notes call it
incremental updates to the 2-52 weeks ahead demand forecast, which "assist the industry to make
efficient decisions in balancing their supply and demand positions". The resource description
defines National Demand as Great Britain's generation requirement: the sum of metered generation
from the Transmission Network Operators' operational generation metering, excluding generation
required to meet station load, pump storage pumping and interconnector exports. The package
carries the portal tags `2-52`, `Cardinal`, `Point`, `Weeks Ahead`, `Long Term` and `National`,
which indicate a cardinal-point forecast (a few characteristic demand values per week) and not a
half-hourly profile.

Each row is one forecast week. The vendor dictionary gives, per "ESI week", the date of the peak
demand (`CDATE_peak`) and four MW values: the peak (`tsd_peak`), the minimum (`tsd_min`), the
minimum daytime demand (`day_min`) and the minimum overnight demand (`night_min`). Two label
columns name the calendar year and financial year in which the demand is forecast to occur, and
`ESIWK` names the ESI week. A model of forward margins, of weekly peak and trough planning, or of
the long-range demand shape would use this as the national-demand anchor alongside the shorter
horizons in @7-day-ahead-national-forecast.md and @2-14-days-ahead-national-demand-forecast.md.

**The silver output is held** (unit E-SEM). NESO's dictionary does not define the ESI week (its
start and end day, its numbering, or how it rolls over against the calendar and financial year
labels), and the table repeats one `(calendar_year, ESIWK)` label at two different peak dates. No
week can be placed on a calendar with certainty, so the table is not eligible for publication or
point-in-time use until NESO answers. See Holds. This note gives schema, clocks and structural
counts only; under ruling 66 (2026-10-24) the site page shows the rows and a notebook, with one
line naming the week-calendar question and no chart on a time axis.

- Publisher group: Demand
- Registry group: demand · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Long term demand forecast | CSV | upload | `903302b4-b577-4228-a347-b9917568b4e1` |

- Long term demand forecast → `demand_forecast_2_52w`.
  Download as captured: [year_ahead_weekly.csv](https://api.neso.energy/dataset/edd6190a-66d4-480d-a125-88d32bd11c91/resource/903302b4-b577-4228-a347-b9917568b4e1/download/year_ahead_weekly.csv).
  The CKAN resource is an upload with the datastore active. The file name is the vendor's; the
  stable handle is the resource id. Captured:
  `raw_20261008T100602Z_903302b4-b577-4228-a347-b9917568b4e1_79991bf0.csv`, 3,404 bytes
  (equal to the declared content length), body sha256 prefix `79991bf0`, UTF-8 with no BOM and
  CRLF line endings, one header line plus 65 data rows, one header epoch, CKAN `last_modified`
  `2026-09-29T12:28:44.374647`, `url_type: upload`. Package `metadata_modified` is
  `2026-09-29T12:28:44.448654`.

The package has this one resource only (`num_resources` 1 in snapshot `20261006T195819Z`), so it
has no DOC or other disposition entries. Package tags and the single resource are from the
catalogue snapshot (gridflow `@.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json`).

## Families

### `demand_forecast_2_52w`

- Kind: tabular · archetype: FC · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| calendar_year | `calendar_year` | int64 | — | yes | — | — |
| financial_year | `financial_year` | int64 | — | yes | — | — |
| ESIWK | `esiwk` | int64 | — | yes | — | — |
| CDATE_peak | `cdate_peak` | date | `%Y-%m-%d` | yes | — | — |
| tsd_peak | `tsd_peak` | int64 | — | yes | — | MW |
| tsd_min | `tsd_min` | int64 | — | yes | — | MW |
| day_min | `day_min` | int64 | — | yes | — | MW |
| night_min | `night_min` | int64 | — | yes | — | MW |

- Entity key: `calendar_year`, `financial_year`, `esiwk`, `cdate_peak`, `tsd_peak`, `tsd_min`, `day_min`, `night_min`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Held (unit E-SEM).** This family's silver output exists but is not eligible for publication or
point-in-time use. This note gives schema, row counts and structural counts only; under ruling
66 (2026-10-24) the site page shows the rows, with one line naming the week-calendar question.
See Holds.

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured file. For the one capture to date that is
   `2026-09-29T12:28:44.374647`, which CKAN emits without an offset. gridflow reads it as UTC
   (gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). All 65 silver rows
   share this one vintage (checked on the silver file, 2026-10-16). The file has **no issue
   column** and the record's issue recipe is `none`: no row carries its own issue time. The
   vintage says when the file last changed. It does **not** say that every week in the file was
   forecast on that date, and the vendor states no forecast issue time.
2. **Event time (`none`).** The record has no temporal recipe, so `timestamp_utc` = `event_time`
   = the **capture time** (`capture_written_at`, `2026-10-08T10:06:02.958906Z`), not any week's
   start or peak. Checked on every silver row on 2026-10-16: `timestamp_utc` equals
   `capture_written_at` and `event_time`, and `available_at` equals `published_at`. The target
   period is carried only by the raw `calendar_year`, `financial_year`, `esiwk` and `cdate_peak`
   columns. No timestamp is derived from them, because the ESI week calendar is not established
   (see below). Do not read `timestamp_utc` on this family as a target time.

**Key and coverage.** No label key exists. The label pair `(calendar_year, esiwk)` is not
unique: of 65 silver rows there are 64 distinct pairs, with one pair appearing twice. That pair
is 2027 week 29, with `CDATE_peak` 2027-07-21 on one row and 2027-07-22 on the other (this is the
hold question's own wording; gridflow `@docs/DECISION_LOG/ADR-036-neso-profiler-and-pilot-records.md`).
The two rows are identical in all four MW columns and differ only by one day in `CDATE_peak`
(silver, 2026-10-24). That points at a repeated row, but it does not prove one.
`cdate_peak` alone has 65 distinct values and the full eight-column row has 65 distinct values,
which is why the record takes every column as the entity key and `latest: whole_capture`. That
key is a gridflow choice made so every row is preserved, not a vendor identity guarantee.
`TODO: verify` the vendor's row identity and whether the repeated week label is a revision, a
split week at a boundary, or an error.

**ESI week and year labels (unresolved).** The vendor dictionary describes `calendar_year` as
"the calendar year the demand is forecast to occur", `financial_year` as "the financial year the
demand is forecast to occur" and `ESIWK` as "the ESI week the forecast is for". It defines
neither the ESI week nor the financial year boundary. `TODO: verify` what "ESI" stands for in
this column, the week start and end day, the numbering and how it rolls over at the year
boundary against both year labels, which month the financial year starts in (the data suggest
April: see the measurement below), and which label
the row's `calendar_year` follows when a week straddles two years. Do not apply an ISO-week or
a fixed-date conversion to `esiwk`. Measured in the one capture (silver, 2026-10-24):
`financial_year` equals `calendar_year` on every row except the 13 whose `CDATE_peak` falls from
January to March 2027, which carry `financial_year` 2026. The label changes between peak dates
2027-03-31 and 2027-04-05. That fits a financial year starting in April and labelled by its
first calendar year, but NESO does not say so, and it is a measurement, not a definition.
The numbering, measured the same way: `calendar_year` 2026 runs from ESI week 42 to week 53
(week 53's peak date is 2026-12-30), and 2027 runs from week 1 (peak 2027-01-05) to week 52.
So week numbers 42 to 52 occur under both years; only the pair 2027 and week 29 repeats.

**`CDATE_peak`.** The dictionary defines it as "the date of the peak demand during that ESI week".
It is a calendar date with no time of day and no zone, stored as a `date` with format
`%Y-%m-%d` (all 65 bronze values are ISO dates: profiler shape `iso_date` 65 of 65). It is the
date of the peak, not a week start. `TODO: verify` the day boundary and zone that "date" uses.

**Units (vendor dictionary only).** `tsd_peak`, `tsd_min`, `day_min` and `night_min` are **MW**,
each declared in the vendor dictionary (field-info `demand_forecast_2_52w.json`). The
descriptions are: the peak demand during that ESI week; the minimum demand during that ESI week;
the minimum daytime demand during that ESI week; the minimum overnight demand during that ESI
week. `calendar_year`, `financial_year` and `esiwk` carry no physical unit (the vendor unit field
is empty): they are labels. No unit was inferred from a column name. `TODO: verify` the expansion
of the "TSD" prefix (the dictionary titles read "TSD Peak" and "TSD minimum") and the hours that
define "daytime" and "overnight" for `day_min` and `night_min`.

**Sentinels and missing values (FACTS g5).** The record declares no null token. In the one
capture no column holds a blank (zero blank and zero null cells in all eight columns), and no
numeric column holds a value that is zero, negative, `-1` or `99999`. A text scan of the bronze
file found no `NA`, `N/A` or `null` token. That establishes absence in this capture, not a
vendor sentinel policy. All eight columns are nullable in silver; any future blank stays a null
and no value is converted. `TODO: verify` the vendor's missing-value convention.

**Activation (2026-10-08, master `29b563c`, PR #85).** Transformed at cutoff 2026-10-08 (one
capture, first capture = cutoff): **65 silver rows**, equal to the CKAN datastore total
(`total` 65 in field-info) and to the bronze data-row count. No prior silver existed, so nothing
was overwritten. The silver file is `year=2026/month=10/…parquet` under
`C:/gridflow-data/silver/neso_data_portal/demand_forecast_2_52w/`. Reconcile `--cutoff
2026-10-08` over the six pilot families exited 0 with 0 gaps (gridflow `@.planning/v0.22-RESULTS.md`
§E; RULINGS 504). The record was typed by the engine and matches the pilot column table
(gridflow `@.planning/phases/v0.22-E-profiler-pilot/VERIFICATION.md`, criterion 3). Row count
queried 2026-10-16: still 65 across a single silver file; no later capture has been written.
This is a count as of that query, and a later ad hoc upload will change it.

Silver columns beyond the vendor columns: `timestamp_utc`, `published_at`, `bronze_capture_id`,
`capture_written_at`, `event_time`, `available_at`, `source_run_id`, `dataset_version` (all
timestamps tz-aware UTC; `dataset_version` `1+e1` = record version 1, epoch 1).

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Ad hoc
- Ad hoc: the vendor uploads when it chooses. gridflow keeps the newest capture whole
  (`latest: whole_capture`). Captures to date: one (2026-10-08), whose CKAN `last_modified`
  (2026-09-29) is nine days before capture. No scheduled refresh has produced a second capture.
- `TODO: verify` whether an upload revises weeks already covered by the previous upload, only
  extends the horizon, or drops elapsed weeks. Only repeated captures compared row by row can
  show this.
- `TODO: verify` the vendor's update schedule. The resource description says only "ad hoc".
- `TODO: verify` the forecast horizon the file actually covers against the documented 2-52 weeks
  ahead. The row count (65) is more than 52, and the vendor does not explain it. Measured
  (silver, 2026-10-24): peak dates run from 2026-10-15 to 2027-12-29, about 1 to 64 weeks after
  the 2026-10-08 capture and about 2 to 65 weeks after the file's `last_modified` (2026-09-29).

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `demand_forecast_2_52w`: held: TODO: ESI week definition (start and end day, numbering, rollover against calendar_year and financial_year) and why 2027 week 29 appears twice with CDATE_peak 2027-07-21 and 2027-07-22; the NESO dictionary is silent (unit E-SEM)

The hold is a class-3 finding of the E pilot research, recorded as question Q-1 in the registry
record and in gridflow `@docs/neso_data_portal/eligibility.md` (RULINGS 504). Two things are
missing, and either one alone would block point-in-time use:

1. **The week calendar.** The table gives an ESI week number and two year labels, plus one
   peak date per row. The vendor's dictionary does not define the ESI week's start and end,
   numbering or rollover, so the target interval of each row is unknown. gridflow therefore
   keeps temporal `none`, derives no timestamp, and keeps `esiwk` and the year labels raw. The
   one repeated week label (2027 week 29, two different peak dates) shows the label does not
   identify a single week.
2. **The issue clock.** There is no issue or publication column. The CKAN vintage is only the
   date the file last changed. Without the calendar, gridflow cannot show that every target week
   lay after the vintage, so the CKAN vintage cannot be accepted as a conservative proxy for the
   missing issue time. This is the same forward-target test applied to the other forecast
   families (RULINGS 529).

Unit E-SEM must answer both questions with NESO. Until then the silver output stays out of any
point-in-time query. There is no gold view for this family. Under ruling 66 (2026-10-24) the site
page shows the rows, with one line naming the week-calendar question and no chart on a time
axis; its notebook plots each peak at NESO's own peak date only. This note itself states no
MW values. Rulings 591 and 596
(ADR-041, `@docs/DECISION_LOG/ADR-041-gold-forecast-vs-outturn-contracts.md`, status proposed
since RULINGS 874) concern the day-ahead demand forecast and its performance pairing and do not
lift this hold; the pairing of the day-ahead forecast with its performance family stays held with
no gold view. Rulings 494, 499 and 879 are the bootstrap, sweep and close records for the
activation and this docs wave and set no further constraint on this family.

## Links

- [NESO Open Data Portal package](https://www.neso.energy/data-portal/long-term-2-52-weeks-ahead-national-demand-forecast)
- [Vendor dictionary](https://www.neso.energy/data-portal/long-term-2-52-weeks-ahead-national-demand-forecast/long_term_demand_forecast)
- Registry record: gridflow `@src/gridflow/connectors/neso_data_portal/registry/long-term-2-52-weeks-ahead-national-demand-forecast.json`
- Eligibility report: gridflow `@docs/neso_data_portal/eligibility.md`
- Pilot record decision: gridflow `@docs/DECISION_LOG/ADR-036-neso-profiler-and-pilot-records.md`
- Related pages: @7-day-ahead-national-forecast.md, @2-14-days-ahead-national-demand-forecast.md, @day-ahead-half-hourly-demand-forecast-performance.md
