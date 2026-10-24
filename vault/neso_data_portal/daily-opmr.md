---
source: "neso_data_portal"
package: "daily-opmr"
dataset_key: "daily_opmr"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Daily operational planning margin requirement
  summary: >-
    NESO's daily view, days ahead, of the spare generation it needs above forecast demand for
    reserve, beside demand, availability and surplus.
  facts:
    vendor: "NESO Data Portal, package `daily-opmr`: one CSV file"
    cadence: "Daily (weekdays), NESO lists; its October 2026 files include weekend publications"
    grain: "Each row: one target day, as forecast on one publication date"
    history: "NESO's 16 October 2026 file holds daily publications from 12 March 2021"
  landscape: power
  what_it_is: >-
    NESO defines the operational planning margin requirement (OPMR) as the generation needed above
    its demand forecast to cover its reserve requirement. Each daily publication gives, in MW, the
    peak and minimum demand forecasts, generator availability, interconnector limits, the OPMR and
    the national surplus left after demand and the OPMR, for each day 2 to 14 days ahead, NESO says.
  how_used:
    - Track how NESO's margin view of one day moves as the day approaches
    - Flag days NESO expects to be tight on margin, up to two weeks ahead
    - Read beside NESO's negative reserve margin forecast for low-demand days
  chart:
    type: line
    silver: neso_data_portal/daily_opmr
    time: date
    values:
      - {column: generation_availability_margin, series: margin}
      - {column: opmr_total, series: opmr}
    filter:
      - {column: publish_date, op: eq, value: "2026-10-16"}
    dedup: {"on": [publish_date, date], order_by: published_at}
    aggregation: last
    window: {start: "2026-10-18", end: "2026-10-30"}
    unit: MW
  chart_view:
    title: Margin and OPMR in the 16 October 2026 publication
    caption: >-
      Silver `daily_opmr`, MW: the publication dated 16 October 2026, as in NESO's file of that day,
      for target days 18 to 30 October, one point per day. Earlier publications are not drawn.
    alt: >-
      Line chart from neso_data_portal/daily_opmr of NESO's publication dated 16 October 2026, in MW,
      for target days 18 to 30 October. The generation availability margin runs from 12,782 on
      19 October to 25,485 on 25 October. The OPMR runs from 4,277 on 18 October to 9,488 on
      25 October, below the margin on every day.
    x_label: target day, UK date
    y_min: 0
    key:
      - {series: margin, label: Availability margin, codes: Generation Availability Margin, paint: petrol,
         note: "Generation available after meeting national demand, NESO's dictionary says"}
      - {series: opmr, label: OPMR, codes: OPMR total, paint: clay,
         note: "Generation NESO needs above its demand forecast to meet its reserve requirement"}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then the CSV, downloaded whole unless
      `last_modified` is unchanged. The 8 October 2026 publication has different figures in NESO's
      8 and 16 October files.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=daily-opmr"
      - "GET https://api.neso.energy/dataset/8e0c417f-ee54-4c8b-8ed2-0d64b042c6ed/resource/0eede912-8820-4c66-a58a-f7436d36b95f/download/csv_opmr_daily.csv"
    commands:
      - {run: gridflow ingest neso_data_portal daily_opmr --last 24h, comment: "the CSV to bronze"}
      - {run: gridflow transform neso_data_portal daily_opmr --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: publish_date, op: eq, value: "2026-10-08"}
        - {column: date, op: ge, value: "2026-10-10"}
        - {column: date, op: le, value: "2026-10-13"}
      order_by: [date, published_at]
      columns: [publish_date, date, published_at, generator_availability, generation_availability_margin,
                opmr_total, national_surplus, peak_demand_forecast]
    key: [publish_date, date, published_at]
    caption: "Four target days of the 8 October 2026 publication, in NESO's 8 and 16 October files."
    fields:
      publish_date: "NESO's `Publish Date`: the publication's date, with no time or zone"
      date: The target day the row forecasts, a UK date
      published_at: "NESO's last-modified time for the file, read as UTC; one per file"
      generator_availability: Generator availability for the target day, MW
      generation_availability_margin: "Generation available after meeting national demand, MW, NESO's dictionary says"
      opmr_total: "The OPMR: generation needed above the demand forecast for reserve, MW"
      national_surplus: "NESO's dictionary: total generation minus demand minus OPMR, MW"
      peak_demand_forecast: Peak demand forecast for the target day, MW
      maximum_ic_import: Maximum interconnector import limit into GB, MW
      maximum_ic_export: Maximum interconnector export limit out of GB, MW
      operating_reserve_provided_by_ics: Operating reserve provided by interconnectors, MW
      constrained_plant: "Constrained plant, MW, as NESO's column names it"
      minimum_demand_forecast: Minimum demand forecast for the target day, MW
      high_freq_response_requirement: High-frequency response requirement at minimum demand, MW
      negative_reserve: "Negative regulating reserve plus reserve for high-frequency response, MW"
      timestamp_utc: "UK midnight opening `date`, in UTC; not a publication time"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  caveat: "`Publish Date` has no time or zone, and NESO later changed its 8 October 2026 publication."
  notebook:
    lead: >-
      `query()` filters `date`, the target day, on the `_latest` view. The second cell counts
      September 2026 rows by days ahead. NESO says 2 to 14; 436 publications from 26 September 2024
      run to 15.
    cells:
      - |
        import pandas as pd
        df = data.neso_data_portal.query("daily_opmr", "2026-09-01", "2026-10-30")
        pub = df[df.publish_date.astype(str) == "2026-10-16"].sort_values("date", ignore_index=True)
        pub[["publish_date", "date", "peak_demand_forecast", "generator_availability",
             "generation_availability_margin", "opmr_total", "national_surplus"]].head()
      - |
        sep = df[df.publish_date.astype(str).str.startswith("2026-09")]
        ahead = pd.to_datetime(sep.date) - pd.to_datetime(sep.publish_date)
        ahead.dt.days.value_counts().sort_index().rename_axis("days ahead").rename("September rows")
      - |
        ax = pub.plot(x="date", y=["generation_availability_margin", "opmr_total"],
                      color=["#155A6E", "#C77E3C"], ylim=(0, None), figsize=(8, 3.5),
                      xlabel="target day", ylabel="MW");
    needs: NESO's daily OPMR file, any capture from 16 October 2026 on
    plot_alt: >-
      Line plot of NESO's publication dated 16 October 2026, in MW, for target days 18 to 30
      October: the generation availability margin from 12,782 to 25,485, highest on 25 October, and
      the OPMR from 4,277 to 9,488, below the margin every day.
  related:
    - {dataset: neso_data_portal/weekly-opmr, note: "The same margin terms by engineering week, 2 to 52 weeks ahead"}
    - {dataset: neso_data_portal/negative-reserve-active-power-margin-nrapm-forecast, note: "NESO's forecast margin from negative reserve risk, on low-demand days"}
    - {dataset: neso_data_portal/2-14-days-ahead-national-demand-forecast, note: "NESO's national demand forecast for the same days ahead"}
    - {dataset: elexon/uou2t14d, note: "Elexon's availability forecast by BM unit, 2 to 14 days ahead"}
---

# Daily operational planning margin requirement (OPMR)

NESO's daily forecast of the Operational Planning Margin Requirement (OPMR) for the days ahead.
The package notes define OPMR as "the amount of generation exceeding the demand forecast needed
to meet our reserve requirement". The notes say that when the ESO assesses and publishes
generation availability against system requirements, it includes an OPMR above the demand
forecast for 2-13 days ahead. The resource description says 2-14 days ahead (see the horizon
`TODO` below). Each row is one
forecast: a **publication date** (`Publish Date`) and the **target day** it is for (`Date`, the
dictionary title is "Date the OPMR published for"). For that pair the row gives the day's peak
and minimum demand forecasts, generator availability, the maximum interconnector import and
export limits, the generation availability margin, interconnector-provided operating reserve,
the OPMR total, constrained plant, the national surplus, the high-frequency response
requirement and the negative reserve requirement, all in MW. The file is history-bearing: it
holds the daily publications back to the start of the archive, so the same target day appears
under up to 14 publication dates. Use it to study how NESO's forward margin view for a day
evolved as the day approached, or as a forward indicator of tight or long system days. The
target is a whole day, not a settlement period; for settlement periods see
@../../../20-domain/concepts/settlement-period.md. The weekly sibling, on an engineering-week
grid, is @weekly-opmr.md; the negative-reserve margin forecast is
@negative-reserve-active-power-margin-nrapm-forecast.md. The silver output is held because the
historical rows carry only a publication **date**, with no evidenced issue instant (see Holds).

- Publisher group: Generation
- Registry group: generation · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Daily Operational Planning Margin Requirement | CSV | upload | `0eede912-8820-4c66-a58a-f7436d36b95f` |

- Download: [csv_opmr_daily.csv](https://api.neso.energy/dataset/8e0c417f-ee54-4c8b-8ed2-0d64b042c6ed/resource/0eede912-8820-4c66-a58a-f7436d36b95f/download/csv_opmr_daily.csv)
  (CKAN datastore active; resource created 2019-12-20).
- Resource description (verbatim): "The daily Operational Planning Margin Requirement (OPMR)
  is published on a daily basis and contains a view of 2-14 days ahead forecast for the OPMR."
- Captured: `raw_20261008T100510Z_0eede912-8820-4c66-a58a-f7436d36b95f_6c474505.csv`,
  2,161,291 bytes, 26,828 raw data rows (one all-empty), one header epoch.
- Second capture: `raw_20261016T200145Z_0eede912-8820-4c66-a58a-f7436d36b95f_0fb60a83.csv`,
  2,170,323 bytes, 26,938 raw data rows (one all-empty), the same header.

The package has no DOC resource and no `_files` family (gridflow
`@.planning/phases/v0.22-K-GEN-1/K-GEN-1-FACTS.md` GEN1-4).

## Families

### `daily_opmr`

- Kind: tabular · archetype: FC · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Publish Date | `publish_date` | date | `%Y-%m-%d` | yes | — | — |
| Date | `date` | date | `%Y-%m-%d` | no | — | — |
| Peak Demand Forecast | `peak_demand_forecast` | float64 | — | yes | — | MW |
| Generator Availability | `generator_availability` | float64 | — | yes | — | MW |
| Maximum IC Import | `maximum_ic_import` | float64 | — | yes | — | MW |
| Maximum IC Export | `maximum_ic_export` | float64 | — | yes | — | MW |
| Generation Availability Margin | `generation_availability_margin` | float64 | — | yes | — | MW |
| Operating Reserve provided by ICs | `operating_reserve_provided_by_ics` | float64 | — | yes | — | MW |
| OPMR total | `opmr_total` | float64 | — | yes | — | MW |
| Constrained Plant | `constrained_plant` | float64 | — | yes | — | MW |
| National Surplus | `national_surplus` | float64 | — | yes | — | MW |
| Minimum Demand Forecast | `minimum_demand_forecast` | float64 | — | yes | — | MW |
| High Freq Response Requirement | `high_freq_response_requirement` | float64 | — | yes | — | MW |
| Negative Reserve | `negative_reserve` | float64 | — | yes | — | MW |

- Entity key: `publish_date`, `date`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured resource: `2026-10-08T09:20:23.077566` for the first capture
   and `2026-10-16T19:20:20.671046` for the second, taken from the captures' sidecars. CKAN emits it without an
   offset, and gridflow reads it as UTC (gridflow
   `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). Every silver row of the
   capture shares this one vintage (checked on silver 2026-10-09: one distinct `published_at`,
   `available_at` equal on every row). It says when the file last changed, not when any
   individual row was first published. The record has **no issue time** (issue recipe `none`).
   `Publish Date` is kept as a typed `date` column, `publish_date`; it is not promoted to
   `issue_time`, because it has no time of day and no vendor zone (FACTS g1, g2).
2. **Event time (`date_sp1` on `date`).** `timestamp_utc` is the start of the target day: UK
   local midnight of `Date`, converted to UTC (the settlement-day anchor of the shared helper;
   no intraday period is invented). `event_time` equals `timestamp_utc`. Event time is
   therefore the **target day**, not the capture time and not the publication date. Checked
   against silver on 2026-10-09: the mapping holds on all 26,827 rows, and `event_time` equals
   `timestamp_utc` on every row.

**Units (vendor dictionary only, field info read 2026-10-08, gridflow
`@.planning/research/neso-snapshots/field-info/20261008T114228Z/daily_opmr.json`; package page
[daily-opmr](https://www.neso.energy/data-portal/daily-opmr)).** Every power column is **MW** in
the dictionary: all twelve from `Peak Demand Forecast` to `Negative Reserve` (FACTS
§`daily_opmr`, g4). `Publish Date` and `Date` are dates with an empty unit, shown as `—`.
Definitions worth keeping, from the dictionary:

- **OPMR total**: "the amount of generation, in excess of demand forecast, that is required to
  meet" the day-ahead reserve requirement.
- **National Surplus**: "The total generation – demand - OPMR".
- **Generation Availability Margin**: generation available after meeting national demand.
- **Negative Reserve**: the sum of the Negative Regulating Reserve Requirement and the reserve
  for the High Frequency Response Requirement.
- **High Freq Response Requirement**: the high-frequency response requirement at minimum demand.
- **Maximum IC Import / Export**: the maximum interconnector transfer limits into and out of the
  GB system.

**Sentinels and missing values (FACTS g5).** The vendor declares no sentinel spelling, and the
record has no null-token map. The full body has no `N/A`, `NA` or literal `-1` tokens, and no
value numerically equal to −1.

- The body has **one all-empty row**. The non-nullable target `Date` drops it through the
  reader's logged blank-row path (`silver/csv_bronze.py:_drop_blank_rows`), not a silent filter:
  26,828 raw rows → 26,827 silver rows.
- Blank cells become null and stay null; they are never converted to zero. In silver,
  `operating_reserve_provided_by_ics`, `constrained_plant`, `high_freq_response_requirement` and
  `negative_reserve` each have 14 nulls (FACTS counts 15 per column in the body, including the
  empty row). Every other column has none.
- **Zeros are preserved as values**, never converted to null. FACTS g5 records long zero runs in
  some columns; `TODO: verify` whether a zero means a genuine zero requirement or "not
  applicable / not provided". No vendor missing-value policy says.

**Identity and structure.** `(publish_date, date)` is unique across the whole silver output (0
duplicates; FACTS T02 measured the same on the raw body). It is the entity key, but it is a
measured grain, not a vendor-documented key: `TODO: verify` the contractual key and whether
NESO ever revises a past publication in place (FACTS T02, g2, g3). `_latest` is
`whole_capture`: the newest capture wins as a whole. Measured structure on 2026-10-09:

- 2,030 distinct publication dates and 2,049 distinct target dates.
- 1,595 publication dates carry 13 target rows, 434 carry 14, and one carries 16.
- Measured as target minus publication date, the main grid is 2–14 days: days 2–13 on all
  2,030 publication dates, day 14 on 2,029 (one publication lacks it), plus a 15-day row on
  430 publication dates.
- 8 rows sit off that main grid: one target one day **before** its own publication date, one
  on the same day, and six one day ahead (on six different publication dates). `TODO: verify` whether these are vendor data-entry
  errors. They are kept as delivered.
- `TODO: verify` the horizon. The package notes say "2-13 days ahead", the resource
  description says "2-14 days ahead", and the body measures 2–15.

**Second capture (2026-10-16, silver read 2026-10-24).** 26,937 rows; 2,038 publication dates
(2021-03-12 to 2026-10-16) and 2,057 target dates (to 2026-10-30); `(publish_date, date)` unique;
the same four columns with 14 nulls each; the same 8 off-grid rows. Publication dates cover every
day from 2021-03-12 to 2026-10-16 except seven (2022-04-24, 2024-02-23 to 25, 2024-03-09,
2024-07-30, 2026-08-23). Against the first capture:

- Every first-capture key is still present; 110 rows are new (one more target, 2026-10-23, for
  the 2026-10-08 publication, and the publications of 9 to 16 October).
- 26,814 shared rows are identical. The other 13 are every row of the 2026-10-08 publication:
  each changed `generator_availability`, `generation_availability_margin`, `opmr_total`,
  `national_surplus`, `minimum_demand_forecast`, `high_freq_response_requirement` and
  `negative_reserve` (12 also `constrained_plant`, 6 `peak_demand_forecast`, 5 the interconnector
  limits). The first capture's 2026-10-08 rows match neither the 7 nor the 9 October
  publication, so NESO replaced that day's publication after its 09:20 UTC file under the same
  `Publish Date`. No earlier publication changed. This answers part of the revision `TODO`
  above: a publication can change on its own day; whether older ones ever do is still open.

**Activation (2026-10-09, master `f19effb`, PR #92).** The family was transformed with cutoff
2026-10-08 (one capture at the time). Silver has **26,827 rows**, equal to the planned count. Reconcile
`--all --cutoff 2026-10-08` found 0 gaps over 55 recorded families, overlap 0. No prior silver
existed, so nothing was overwritten (gridflow `@.planning/v0.22-RESULTS.md` §GEN-1; RULINGS
545–546).

Silver columns beyond the 14 vendor columns: `timestamp_utc`, `published_at`,
`bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id`,
`dataset_version` (all timestamps tz-aware UTC; `dataset_version` `1+e1` = record version 1
plus generic-engine version 1). The silver file sits in the `year=2026/month=10` partition of
the capture, not of the target dates.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Daily (Weekdays)

The resource description says the OPMR "is published on a daily basis". The CKAN
`last_modified` was `2026-10-06T19:20:23.655476` in the catalogue snapshot,
`2026-10-08T09:20:23.077566` at the first capture and `2026-10-16T19:20:20.671046` at the second.
`TODO: verify` the publication time of day; no vendor source states it. The extras say weekdays,
but the measured publication dates spread evenly over all seven days of the week (288–291 each in
the first capture, 289–292 in the second); `TODO: verify` which is right (see Implementation
delta). No scheduled gridflow refresh exists yet, so captures are on demand. Two captures
(2026-10-08 and 2026-10-16) exist.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `daily_opmr`: held: TODO: history-bearing body (26,709 targets at or before the CKAN vintage); Publish Date is a date with no issue instant or zone (unit E-SEM)

The silver output exists on disk, but it is **held**: it is not eligible for point-in-time model
use until unit E-SEM answers the question above (RULINGS 542). Under ruling 66 (2026-10-24) the
site page shows its rows, a chart of the 16 October 2026 publication and a notebook, with the
question as a caveat.

Why the forward-target rule (RULINGS 529) does not rescue it: that rule makes a forecast
eligible when every target in the captured file falls after the capture's CKAN
`last_modified`, so the vintage can stand in for an issue time. The daily NRAPM families in
the same batch pass it. This body fails it: it is the full archive of past publications, and
26,709 of its 26,827 target rows fall at or before the vintage (FACTS GEN1-1, reproduced on
silver 2026-10-09); in the 2026-10-16 capture it is 26,821 of 26,937. For those rows the vintage is far later than the moment the forecast was
made, and the only per-row clue, `Publish Date`, is a date with no time of day or zone. Turning
it into an issue instant (for example midnight UK time) would invent an availability time. A
vendor statement of when each daily OPMR is published, in which zone, and whether past
publications are ever revised, would settle it (FACTS §`daily_opmr`, g2).

The package-level `eligibility: eligible` in the front matter refers to the package registry
entry. The hold is per family and sits on `daily_opmr`.

Related holds in the same batch (gridflow `@docs/neso_data_portal/eligibility.md`): weekly OPMR
(the engineering year/week → target date mapping is undocumented), the two weekly NRAPM
families (value scales undocumented), the two historic day-ahead wind archives and the two
ordinary 14-day wind bodies, all unit E-SEM.

**Implementation delta (vendor body and dictionary vs record).**

- The CSV body's headers carry trailing spaces on `Maximum IC Export ` and `National Surplus `
  (FACTS H-I). FACTS told the executor to freeze them with the spaces. The CSV reader strips header
  names (gridflow `@src/gridflow/silver/neso_data_portal/readers.py`, line 136), so the record freezes the stripped spellings and the FACTS
  correction was ruled moot (RULINGS 544). The datastore dictionary also uses the stripped
  names.
- The package notes announce that the column ids changed on 17 September 2026:
  `Maximum I/C Import` → `Maximum IC Import`, `Maximum I/C Export` → `Maximum IC Export`,
  `Operating Reserve provided by I/Cs` → `Operating Reserve provided by ICs`. Both captures and
  the 2026-10-08 field info use the new names, hence one header epoch. A body captured
  before the rename would need a second epoch. Both bronze bodies (2026-10-08 and 2026-10-16)
  carry the new names, so no pre-rename body exists in bronze.
- The dictionary types every power column as `integer` (`int4`). The record casts them to
  nullable `float64`.
- The extras say "Daily (Weekdays)"; the publication dates cover all seven weekdays evenly.
  `TODO: verify` the publication calendar.
- The dictionary describes `Publish Date` only as the date the OPMR was published. No source
  gives its time of day or zone (FACTS g1). `TODO: verify`.
