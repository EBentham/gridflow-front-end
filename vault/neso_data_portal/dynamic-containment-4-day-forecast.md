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
  title: Dynamic Containment 4 day forecast
  summary: >-
    NESO's Dynamic Containment requirement forecast for the next four days, in MW per EFA block,
    with an archive of earlier forecasts.
  facts:
    vendor: "NESO Data Portal, package `dynamic-containment-4-day-forecast`: two CSV files"
    cadence: Daily, as NESO lists it; the current file covers the next four days
    grain: One row per date and service code; one MW column per EFA block
  landscape: market
  what_it_is: >-
    NESO's forecast of how much Dynamic Containment, a frequency-response service, it needs: MW for
    each of a day's six EFA blocks, the first from 23:00 UK time the day before. NESO's dictionary
    does not define the two service codes, `DC-H` and `DC-L`. The current file covers the next four
    days; the history file keeps earlier forecasts by creation date.
  how_used:
    - A look-ahead on NESO's Dynamic Containment requirement, block by block
    - Read beside the other ancillary-service requirement forecasts
    - "How the requirement has moved since 2022, from NESO's archive of forecasts"
  chart:
    type: line
    silver: neso_data_portal/dc_forecast_4d_history
    filter:
      - {column: forecast_created, op: ne, value: "09/08/2022"}
    time: forecast_target_date
    value: efa_5
    dedup: {on: [forecast_created, forecast_target_date, service_type], order_by: capture_written_at}
    group: service_type
    group_map: {DC-H: dch, DC-L: dcl}
    series_order: [dch, dcl]
    aggregation: mean
    window: {start: "2022-04-21", end: "2026-10-20"}
    unit: MW
  chart_view:
    title: "Dynamic Containment requirement, EFA block 5, 2022 to 2026"
    caption: >-
      Silver `neso_data_portal/dc_forecast_4d_history`, MW, EFA block 5 (15:00 to 19:00 UK time):
      each target date's mean over NESO's archived forecasts, leaving out the 9 August 2022 issue,
      whose targets are partly month first. Not what was known on any day.
    alt: >-
      Line chart from neso_data_portal/dc_forecast_4d_history of the Dynamic Containment requirement
      in MW for EFA block 5, each target date's mean over NESO's archived forecasts, 21 April 2022 to
      20 October 2026. DC-H (petrol) has a 2022 median of about 460, lowest 247 on 5 December 2022,
      then about 1,060 in 2023, 1,210 in 2024. DC-L (clay) rises from about 730 in 2022 to 1,310
      in 2025. Both peak on 4 July 2026, 1,675 and 1,517, and hold 1,495 almost every day from 11
      July 2026; 22 August 2026 is a gap.
    x_label: target date
    key:
      - {series: dch, label: DC-H, paint: petrol}
      - {series: dcl, label: DC-L, paint: clay}
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show` gives each file's address, which changes with each
      upload; the file is downloaded unless its `last_modified` is unchanged. Swap in
      `dc_forecast_4d` for the current file.
    commands:
      - {run: gridflow ingest neso_data_portal dc_forecast_4d_history --last 24h, comment: "whole archive file to bronze"}
      - {run: gridflow transform neso_data_portal dc_forecast_4d_history --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      silver: neso_data_portal/dc_forecast_4d_history
      filter:
        - {column: forecast_target_date, op: eq, value: "2026-06-10"}
      dedup: {on: [forecast_created, forecast_target_date, service_type], order_by: capture_written_at}
      order_by: [service_type, forecast_created]
      columns: [forecast_target_date, forecast_created, service_type, efa_1, efa_2, efa_3, efa_4, efa_5, efa_6]
    key: [forecast_created, forecast_target_date, service_type]
    caption: "NESO's four archived forecasts for 10 June 2026, labelled created 6 to 9 June, both codes."
    fields:
      forecast_target_date: "Target date, read day first; NESO wrote a few month first"
      forecast_created: "NESO's creation date, text in two formats (day first, ISO); not a publish time"
      service_type: "`DC-H` or `DC-L`; NESO's dictionary does not define the two codes"
      efa_1: "MW for EFA block 1, 23:00 to 03:00 UK time; NESO spells it MWs"
      efa_2: MW for EFA block 2, 03:00 to 07:00 UK time
      efa_3: MW for EFA block 3, 07:00 to 11:00 UK time
      efa_4: MW for EFA block 4, 11:00 to 15:00 UK time
      efa_5: MW for EFA block 5, 15:00 to 19:00 UK time
      efa_6: MW for EFA block 6, 19:00 to 23:00 UK time
      timestamp_utc: "UK midnight opening the target date, as UTC; not an issue time"
      published_at: "When NESO last changed the archive file (CKAN, read as UTC); not per forecast"
      bronze_capture_id: Path of the bronze capture the row was read from
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      Reads each file's `_latest` view (its newest capture) with `data.sql`. The archive cells drop
      the issue created 9 August 2022, its target dates partly month first. The plot averages six
      blocks by month.
    cells:
      - |
        data.sql("""
            SELECT date, service_type, efa_1, efa_6, published_at AT TIME ZONE 'UTC' AS published_utc
            FROM silver_neso_data_portal_dc_forecast_4d_latest ORDER BY service_type, date""")
      - |
        hist = data.sql("""
            SELECT forecast_created, forecast_target_date, service_type,
                   efa_1, efa_2, efa_3, efa_4, efa_5, efa_6
            FROM silver_neso_data_portal_dc_forecast_4d_history_latest
            WHERE forecast_created <> '09/08/2022'""")
        spread = (hist.groupby(["forecast_target_date", "service_type"]).efa_5
                  .agg(issues="count", low="min", high="max").reset_index())
        spread[spread.high - spread.low >= 100].tail(6)
      - |
        blocks = [f"efa_{i}" for i in range(1, 7)]
        month = hist.forecast_target_date.dt.to_period("M")
        monthly = hist[blocks].mean(axis=1).groupby([month, hist.service_type]).mean().unstack()
        monthly.plot(figsize=(8, 3.5), color=["#155A6E", "#C77E3C"], xlabel="target month",
                     ylabel="mean of six EFA blocks, MW");
    needs: a capture of both files
    plot_alt: >-
      Line plot of the mean of the six EFA blocks in MW by target month, April 2022 to October 2026.
      DC-H (petrol) rises from 454 to 1,027 in April 2023, 1,351
      in June 2024, falls to 914 in January 2026, then climbs. DC-L (clay) peaks before 2026 at
      1,312 in June 2025. Both hold 1,495 from August 2026.
  family:
    slug: dynamic-containment-4-day-forecast
    members:
      - dataset: dc_forecast_4d
        differs: "The current file: the next four days, both service codes for each"
        request:
          - "GET https://api.neso.energy/api/3/action/package_show?id=dynamic-containment-4-day-forecast"
          - "GET https://api.neso.energy/dataset/c8cd1e99-bc7e-454c-8ac1-ebd9264f4d0f/resource/1b85a3f3-80f0-49cf-9b0e-49648fa0cae6/download/465d3c6096e24ed49d796f6a7ffdaebd_dcrequirements_1b85a3f3-80f0-49cf-9b0e-49648fa0cae6_patch.csv"
        caveat: NESO does not say whether the slash dates in `Date` are day first or month first.
      - dataset: dc_forecast_4d_history
        differs: "NESO's archive of earlier forecasts, each labelled with its creation and target date"
        request:
          - "GET https://api.neso.energy/api/3/action/package_show?id=dynamic-containment-4-day-forecast"
          - "GET https://api.neso.energy/dataset/c8cd1e99-bc7e-454c-8ac1-ebd9264f4d0f/resource/d5c3b48a-a0a9-4d57-a02a-ac0af09a6298/download/da8aac209e4d4a71b4000538d9575241_dcrequirementshistorical1_d5c3b48a-a0a9-4d57-a02a-ac0af09a6298_.csv"
        caveat: NESO does not say when forecasts were published; a few target dates are month first.
  related:
    - {dataset: neso_data_portal/dynamic-containment-data, note: Auction results for the service this file forecasts}
    - {dataset: neso_data_portal/eac-auction-results, note: "EAC auctions that buy Dynamic Containment, as products `DCH` and `DCL`"}
    - {dataset: neso_data_portal/long-term-forecasts-for-dc-dm-dr-requirements, note: "The longer-horizon sibling, as weights over requirement bands"}
    - {dataset: neso_data_portal/dynamic-moderation-requirements, note: The requirement for a sibling response service}
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
file has no established publication instant for its creation-labelled issues (see Holds).
The site page shows rows from both families, each with a caveat naming its open question
(front-end ruling 66): the chart, frame and notebook read the history file, and never as what was
known at the time.

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

**Held (unit v0.22-K-AS-1).** The silver output exists but is not eligible for point-in-time use
in gridflow. Under front-end ruling 66 the site page shows these rows, with a caveat naming the open question.

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
history file's day-first examples (one archived issue writes its target dates month first), but
no resource-specific statement settles it
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

**Held (unit v0.22-K-AS-1).** The silver output exists but is not eligible for point-in-time use
in gridflow. Under front-end ruling 66 the site page shows these rows, with a caveat naming the open question.

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
- `Forecast_Target_Date` is not day first throughout. In the 2026-10-16 archive (lines 890 to
  897) the issue created `09/08/2022` lists `08/10/2022`, `08/11/2022`, `08/12/2022` (month
  first: 10 to 12 August) then `13/08/2022`. Silver reads `%d/%m/%Y`, so six rows (three
  targets, both codes) sit on 8 October, 8 November and 8 December 2022. No other row targets
  a date outside 0 to 5 days after its creation date (checked 2026-10-24). The site page's
  chart and notebook leave this issue out.
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
Silver output for both exists on disk; neither family may be used point-in-time. The site page
shows both families' rows, each with a caveat naming its question (front-end ruling 66).

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
