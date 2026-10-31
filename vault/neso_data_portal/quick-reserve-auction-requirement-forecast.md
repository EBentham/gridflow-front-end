---
source: "neso_data_portal"
package: "quick-reserve-auction-requirement-forecast"
dataset_key: "qr_auction_requirement_fc"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-18
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Quick Reserve requirement forecast
  summary: >-
    NESO's forecast Quick Reserve requirement for each daily auction: positive and negative MW for
    every half-hour service window.
  facts:
    vendor: "NESO Data Portal, package `quick-reserve-auction-requirement-forecast`: one CSV file, no archive"
    cadence: "Updated monthly (NESO's catalogue); each auction is daily"
    grain: One row per auction date and half-hour service window, 48 on an ordinary day
  landscape: market
  what_it_is: >-
    Quick Reserve, positive and negative, is NESO's reserve for reacting to pre-fault disturbances
    and bringing frequency back near 50.0 Hz. NESO buys it in a daily auction for a delivery day of
    half-hour windows from 23:00 UK time the evening before. This file forecasts each window's
    requirement in MW; NESO updates it monthly.
  how_used:
    - Requirement against cleared `PQR` and `NQR` MW per window, from NESO's EAC results.
    - To join EAC results, convert `service_window_start_time` from UK local time to UTC.
    - "Point-in-time studies: each capture is one vintage, stamped with the file's `published_at`."
  chart:
    type: line
    silver: neso_data_portal/qr_auction_requirement_fc
    time: service_window_start_time
    time_text: {format: "%d/%m/%Y %H:%M"}
    filter:
      - {column: service_delivery_date, op: eq, value: "2026-10-01"}
    values:
      - {column: positive_quick_reserve_requirement_mw, series: positive}
      - {column: negative_quick_reserve_requirement_mw, series: negative}
    aggregation: mean
    window: {start: "2026-09-30", end: "2026-10-01"}
    unit: MW
  chart_view:
    title: Quick Reserve requirement by window, 1 October 2026
    caption: >-
      Silver `qr_auction_requirement_fc`, MW: NESO's forecast for service day 1 October 2026
      (auction 30 September, produced 22 September), each half-hour window from 23:00 the evening
      before, drawn at its start on the UK clock as NESO writes it.
    alt: >-
      Line chart of NESO's forecast Quick Reserve requirement in MW for the 48 half-hour windows of
      service day 1 October 2026, from 23:00 on 30 September, UK local time. Negative reserve is flat
      at 300 MW. Positive reserve is 500 MW in the first window, 300 MW from 23:30 to the window
      starting 05:00, where the two lines meet, and 500 MW from 05:30 to the last window, 22:30.
    x_label: window start, UK local time as written
    y_min: 0
    key:
      - {series: positive, label: Positive reserve, paint: petrol, note: "300 MW for windows starting 23:30 to 05:00, else 500 MW; the same every day in this file."}
      - {series: negative, label: Negative reserve, paint: clay, note: "300 MW in every window of every day in this file."}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then the file downloaded whole unless its
      `last_modified` is unchanged. Dates select nothing.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=quick-reserve-auction-requirement-forecast"
      - "GET https://api.neso.energy/dataset/7247a5da-563e-4159-b8c1-e388e39ff5a2/resource/f012de08-b258-408b-bc41-f885e183f97f/download/qr.csv"
    commands:
      - {run: gridflow ingest neso_data_portal qr_auction_requirement_fc --last 24h, comment: "whole file; window must end recently"}
      - {run: gridflow transform neso_data_portal qr_auction_requirement_fc --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: service_delivery_date, op: in, value: ["2026-09-30", "2026-10-01"]}
        - {column: service_window, op: in, value: ["1", "2", "13", "14"]}
      order_by: [service_delivery_date]
      columns: [auction_date, service_window, positive_quick_reserve_requirement_mw,
                negative_quick_reserve_requirement_mw, forecast_produced_on, service_window_start_time,
                service_delivery_date, service_window_end_time]
    key: [auction_date, service_window]
    caption: "Service days 30 September and 1 October around both steps, from forecasts produced on different dates."
    fields:
      auction_date: Date of the daily auction these requirements apply to (NESO)
      service_window: "`1` to `48`; autumn change day adds `5x`, `6x`; NESO's dictionary omits `5`, `6`"
      service_window_start_time: Window start, UK local time as NESO writes it, day first; kept as text
      positive_quick_reserve_requirement_mw: Positive Quick Reserve requirement, MW (NESO's unit)
      negative_quick_reserve_requirement_mw: Negative Quick Reserve requirement, MW (NESO's unit), given as a positive figure
      forecast_produced_on: Date NESO produced the forecast; a date only, not a publication time
      service_delivery_date: Service day the windows belong to; its window 1 starts 23:00 the day before
      service_window_end_time: "Window end as NESO writes it (`:29` or `:59`); kept as text"
      timestamp_utc: UK midnight starting calendar date `service_delivery_date`, in UTC; window 1 starts an hour earlier
      published_at: "NESO's last-modified time for the whole file, read as UTC"
      bronze_capture_id: Path of the bronze capture the row was read from
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      Reads with `data.sql` from the `_latest` view, the newest capture, because NESO updates the
      file monthly and a dated `query()` on `service_delivery_date` finds only the days a capture
      holds.
    cells:
      - |
        df = data.sql("""
            SELECT auction_date, service_delivery_date, forecast_produced_on, service_window,
                   service_window_start_time,
                   positive_quick_reserve_requirement_mw AS positive_mw,
                   negative_quick_reserve_requirement_mw AS negative_mw,
                   published_at AT TIME ZONE 'UTC' AS published_utc
            FROM silver_neso_data_portal_qr_auction_requirement_fc_latest
            ORDER BY service_delivery_date,
                     strptime(service_window_start_time, '%d/%m/%Y %H:%M'), service_window""")
        df.groupby("forecast_produced_on").agg(
            first=("service_delivery_date", "min"), last=("service_delivery_date", "max"),
            days=("service_delivery_date", "nunique"), published_utc=("published_utc", "max"))
      - |
        df[["positive_mw", "negative_mw"]].value_counts()
      - |
        low = df[df.positive_mw.lt(500)].groupby("service_delivery_date").service_window
        low.agg(["first", "last", "size"]).value_counts()
      - |
        day = df[df.service_delivery_date.astype(str) == "2026-10-01"]
        day.set_index(day.service_window_start_time.str[11:16])[["positive_mw", "negative_mw"]].plot(
            drawstyle="steps-post", color=["#155A6E", "#C77E3C"], ylim=(0, 600), figsize=(8, 3.5),
            rot=0, xlabel="window start, UK local time as written", ylabel="requirement, MW");
    needs: a capture of the requirement file
    plot_alt: >-
      Step plot of NESO's forecast Quick Reserve requirement in MW for each half-hour window of
      service day 1 October 2026, from 23:00 on 30 September to 22:30, UK local time as written.
      Negative reserve (clay) holds 300 MW. Positive reserve (petrol) is 500 MW at 23:00, 300 MW from
      23:30, where the lines meet, and 500 MW from 05:30.
  related:
    - {dataset: neso_data_portal/eac-auction-results, note: "Cleared `PQR` and `NQR` MW and price for the same windows"}
    - {dataset: neso_data_portal/slow-reserve-requirement-forecast, note: The same file layout and key for Slow Reserve}
    - {dataset: neso_data_portal/balancing-reserve-auction-requirement-forecast, note: "Balancing Reserve's forecast, on the same half-hour service windows"}
    - {dataset: elexon/freq, note: The system frequency Quick Reserve helps bring back near 50 Hz}
---

# Quick Reserve Auction Requirement Forecast

This package is NESO's **forecast of how much Quick Reserve it expects to buy in each daily auction**.
Quick Reserve is a reserve service, separated by the vendor into **Positive Quick Reserve**
(PQR) and **Negative Quick Reserve** (NQR); the vendor text read here does not state a direction for
either (`TODO: verify` what positive and negative denote). The vendor says it is aimed at reacting
to pre-fault disturbances to restore the energy imbalance quickly and return frequency close to
50.0 Hz. The service is procured in a daily auction held at 14:00, for delivery from 23:00 on the
day before the service date to 23:00 on the service date, in half-hour **service windows**. This
data set holds the forecast of the MW NESO intends to procure in each window, with one row per
auction and window (CKAN package `notes`,
@.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json).

Each row is one **auction date x service window**: the positive Quick Reserve requirement
(`positive_quick_reserve_requirement_mw`) and the negative Quick Reserve requirement
(`negative_quick_reserve_requirement_mw`), in MW, plus the window's start and end labels and the
date the forecast was produced. It is a **forecast**, not a result: it is not an awarded volume, a
clearing price or a settlement quantity. For modelling it is the demand side of the Quick Reserve
market (how much reserve NESO says it will need), to be joined later to auction results and to the
balancing-mechanism series. It is not a settlement-period table: windows are not settlement periods
(the vendor says so), and no `run_type` applies.

The package is **eligible**. Its one family has a gridflow silver output and **no hold**. The values
may be used, subject to the clock and time-label notes below. The sibling reserve products are in
@./balancing-reserve-auction-requirement-forecast.md (Balancing Reserve, which shares the window
layout) and, for the Dynamic family, @./dynamic-containment-4-day-forecast.md,
@./dynamic-moderation-requirements.md and @./dynamic-regulation-requirements.md.

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Quick Reserve Auction Requirement Forecast | CSV | upload | `f012de08-b258-408b-bc41-f885e183f97f` |

The package has **one resource and no DOC resources**. The resource is a CKAN **upload** (so the
capture has a file name, `qr.csv`), not a datastore dump.

| Resource | Family | Download | Bytes | Data rows | CKAN `last_modified` |
|---|---|---|---:|---:|---|
| Quick Reserve Auction Requirement Forecast | `qr_auction_requirement_fc` | [qr.csv](https://api.neso.energy/dataset/7247a5da-563e-4159-b8c1-e388e39ff5a2/resource/f012de08-b258-408b-bc41-f885e183f97f/download/qr.csv) | 147,893 | 1,874 | 2026-09-22T14:48:27.491459 |

Size and `last_modified` come from the capture sidecar under
`C:/gridflow-data/bronze/neso_data_portal/qr_auction_requirement_fc/2026/10/08/`; rows are data
rows of the body (K-AS-1 FACTS section 2, capture Q1). The single capture was taken
**2026-10-08T11:16:53Z**. Package page:
[quick-reserve-auction-requirement-forecast](https://www.neso.energy/data-portal/quick-reserve-auction-requirement-forecast).
Resource dictionary:
[quick_reserve_auction_requirement_forecast](https://www.neso.energy/data-portal/quick-reserve-auction-requirement-forecast/quick_reserve_auction_requirement_forecast).

**What the file covers.** The body holds **39 service days, 2026-09-23 to 2026-10-31**, auction
dates 2026-09-22 to 2026-10-30. It is a rolling forward window, not a history: the vendor
description says the first auction was held on 3 December 2024, but the captured file does not go
back that far. `TODO: verify` whether earlier forecasts are retained anywhere on the portal. Do not
assume this resource accumulates history.

**Bronze body (seat full-body scan, K-AS-1 FACTS g5).** Strict UTF-8, one header, eight columns, no
malformed row width. The scan found no blank cell, no `-1`, `N/A`, `NA`, `NULL`, `null` or `NaN`
token, no padded cell, no embedded comma or percent sign. The SHA-256 of the single body is
`d3ce986f91517b29e84541ed57a78b1e34d780e398fe00aa67466bb562d0a0d2` and equals the sidecar value.
The body uses day-first slash dates; the vendor dictionary's ISO examples (`2024-11-01`) do not
describe what is actually served.

## Families

### `qr_auction_requirement_fc`

- Kind: tabular · archetype: FC · refresh: monthly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Auction Date | `auction_date` | date | `%d/%m/%Y` | no | — | — |
| Service Delivery Date | `service_delivery_date` | date | `%d/%m/%Y` | no | — | — |
| Service Window | `service_window` | string | — | no | — | — |
| Service window Start Time | `service_window_start_time` | string | — | yes | — | — |
| Service Window End Time | `service_window_end_time` | string | — | yes | — | — |
| Positive Quick Reserve Requirement MW | `positive_quick_reserve_requirement_mw` | float64 | — | yes | — | MW |
| Negative Quick Reserve Requirement MW | `negative_quick_reserve_requirement_mw` | float64 | — | yes | — | MW |
| Forecast produced on | `forecast_produced_on` | date | `%d/%m/%Y` | yes | — | — |

- Entity key: `auction_date`, `service_window`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`service_delivery_date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030, ADR-034) |
| `available_at` | = `published_at` |

**One header epoch.** The record accepts one exact header, the eight columns above. Note the exact
capitalisation: the vendor spells `Service window Start Time` (lower-case "window") and `Service
Window End Time` (capital "W") differently, and the header contract keeps both as served. The Balancing
Reserve page spells the start column differently again.

**What the columns mean (vendor dictionary).** From NESO's saved field info
(@.planning/research/neso-snapshots/field-info/20261008T114228Z/qr_auction_requirement_fc.json).

- **`Auction Date`**: "The date of the auction event that these requirements apply to". A calendar
  date with no time of day. In the body it is the day before the service date.
- **`Service Delivery Date`**: "The service day for delivery of the service". The vendor comment adds
  that service window 1 starts at 23:00 on the previous date (D-1). It is a **service-day label**, not
  the start of the first window.
- **`Service Window`**: the "Service window identifier". The comment says it is **not** a
  settlement period. Observed values are `1` to `48` on an ordinary day, plus `5x` and `6x` on the
  autumn clock-change day (see Two clocks). Kept as a string, byte-equal to the body.
- **`Service window Start Time`** and **`Service Window End Time`**: the start and end of the window,
  "given in local time" (the UK clock). In the body they look like `22/09/2026 23:00` and
  `22/09/2026 23:29`, minute resolution. They are **raw strings** in silver: no timezone
  conversion and no endpoint repair are applied (see Known issues). The dictionary examples
  (`2024-10-31T23:00:00`, `2024-11-01T23:29:59`) use a different format and carry seconds.
- **`Positive Quick Reserve Requirement MW`**: "Requirement for Positive Quick Reserve".
- **`Negative Quick Reserve Requirement MW`**: "Requirement for Negative Quick Reserve".
- **`Forecast produced on`**: "Date that the forecast was produce[d]" (vendor spelling). A calendar
  date only: no clock, no zone, no publication instant.

**Units (vendor dictionary only).** Both requirement columns are **MW**; the dictionary also types
them as integer, and gridflow reads them as `float64` without rescaling. The date and time columns
carry no unit. Nothing is converted. The vendor unit is MW and no energy (MWh) denomination is
stated for either column: do not multiply by the half-hour to get MWh without a vendor statement
that the product is energy-denominated.

**Two clocks.**

1. **Vintage (`ckan_last_modified`).** The resource is an upload with a usable CKAN timestamp, so
   `available_at` = `published_at` = the CKAN `last_modified` of the captured file (ADR-030,
   ADR-034). In the capture that is **2026-09-22T14:48:27.491459Z**, one value on all 1,874 rows.
   That instant is when the file was last uploaded to the portal, not when each forecast row was
   first available, and it is not a vendor-declared publication time. It is also **not** the
   `Forecast produced on` date: that column is a creation date and is never used as an issue
   instant. The capture itself was taken on 2026-10-08 (`capture_written_at`
   2026-10-08T11:16:53Z). An as-of query before 2026-09-22T14:48:27Z sees **no** rows.
   Why the vintage is safe here: **all 1,874 window starts are later than the vintage** (the earliest
   is 2026-09-22 22:00 UTC, i.e. 23:00 UK local; K-AS-1 FACTS g2), so the file is wholly forward-looking at that
   instant and the CKAN time stands in for availability under the forward-target rule
   (RULINGS 529). `TODO: verify` the vendor's actual publication moment and whether rows are
   amended in place at the monthly refresh: one capture exists, so revision behaviour cannot be
   measured.
2. **Event time (temporal recipe `date_sp1` on `service_delivery_date`).** `timestamp_utc` and
   `event_time` are equal on every row and are the **UK local midnight at the start of the service
   date, expressed in UTC** (the settlement-period-1 start of that date). For a summer date that is
   23:00 UTC the previous evening (service date 2026-09-23 gives `2026-09-22T23:00:00Z`; the autumn
   change date 2026-10-25 gives `2026-10-24T23:00:00Z`); for a winter date it is 00:00 UTC
   (2026-10-26 gives `2026-10-26T00:00:00Z`). It is a **calendar-date storage anchor**. It is
   **not** the start of service window 1, and the two are not the same clock: window 1 begins at
   23:00 UK local on the **previous** date (for 2026-09-23 that is `2026-09-22 23:00` local, which is
   `2026-09-22T22:00:00Z`). Every one of a day's 48 or 50 rows therefore carries the **same**
   `timestamp_utc`. To place a row inside the day, use `service_window` together with the
   raw start and end labels, not the timestamp (RULINGS 720; no composed date-plus-window recipe
   exists, RULINGS 572 and 588). `TODO: verify` a row-specific conversion mechanism if a true
   per-window UTC instant is ever needed.

**Identity and selection.**

- The record key is `(auction_date, service_window)`. All 1,874 rows are distinct on it, in the body
  and in silver. A key on the start label alone is **wrong**: it has two duplicate rows on the autumn
  change date, where windows `5`/`5x` both start at `01:00` and `6`/`6x` both start at `01:30` (see
  Known issues). No full-row duplicate exists. The vendor guarantees no key; `TODO: verify` a
  vendor-guaranteed identity and whether a row can be revised in place.
- `_latest` is `whole_capture`: the newest complete capture of the one resource. There is no
  per-key latest, no `key_latest` and no resource partition (one resource only).

**Sentinels and missing values (FACTS g5).** No sentinel exists and the record declares no null
tokens. In silver (2026-10-13) no column has a null, and the body has no zero in either requirement
column, so no zero-versus-missing question arises in this capture.

**Row counts and shape (silver, 2026-10-13).**

| Resource | Rows | Distinct on entity key |
|---|---:|---:|
| `f012de08-b258-408b-bc41-f885e183f97f` | 1,874 | 1,874 |

The planned and activated counts agree (1,874), with 0 validation failures and 0 blank rows
excluded. The body has **38 service days with 48 windows and one with 50** (the autumn change date,
2026-10-25): 38 x 48 + 50 = 1,874. The requirement values observed are: positive requirement
**300 MW on 470 rows and 500 MW on 1,404 rows**; negative requirement **300 MW on all 1,874 rows**.
These are single-capture observations of a forecast, not a vendor-stated range.
Every service day in the capture carries the same profile (silver, 2026-10-18): positive 500 MW in
window `1`, 300 MW in windows `2` to `13` (and `5x`, `6x` on 2026-10-25), 500 MW in windows `14` to
`48`, under both production dates.

Silver layout: one Parquet file per capture under
`C:/gridflow-data/silver/neso_data_portal/qr_auction_requirement_fc/year=2026/month=10/`. The
`year=`/`month=` partition is the **capture** date, not the service date. Columns (16): the eight
vendor columns, then `timestamp_utc`, `published_at`, `bronze_capture_id`, `capture_written_at`,
`event_time`, `available_at`, `source_run_id` and `dataset_version`. All timestamps are tz-aware UTC.
`dataset_version` is `1+e1` (record version 1, generic engine version 1). There is no
`resource_id` column, because the entity key does not include it. No gold view or builder reads
this family.

Two forecast vintages sit inside the one file: `Forecast produced on` is `2026-09-22` on 1,490 rows
and `2026-08-31` on 384 rows (384 = 8 x 48). Production-to-service leads run from 9 to 39 days. They
are production **dates**, not publication instants.

## Cadence

- Registry refresh: monthly
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Monthly

The vendor says the data set is updated monthly and describes it as a daily forecast of requirements.
One capture exists to date (2026-10-08), so the real refresh rhythm, and whether a refresh
replaces the whole file or appends to it, are unmeasured. `TODO: verify` by comparing later
complete captures with the hash-pinned body above. This capture spans 39 service days.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- none

The family has **no hold**: it was specified as eligible and activated as such (RULINGS 720, 723,
725). The questions below are open evidence requests, not holds.

**Known issues and open questions.**

- **Repeated autumn hour.** The captured autumn change date (2026-10-25, 50 windows) is the only
  clock-change day in the body. The vendor comment says service windows `7x` and `8x` are the
  repeated hour at the GMT-to-BST change and that "for BST to GMT clock change day there is no
  service window 5 or 6". NESO's own EAC market design explainer (Appendix B, printed pages
  109 to 111) and the captured body say the opposite: at the autumn (BST to GMT) change the day
  gains windows **`5x` and `6x`**, with the repeated windows' start labels equal to those of `5`
  and `6`. Use the diagrams and the body, not the dictionary comment. `TODO: verify` the spring
  (GMT to BST) layout when a spring-change service day is first captured; the explainer omits
  windows `5` and `6` that day, but no spring body is in hand.
- **Start labels are not unique.** On 2026-10-25 windows `5` and `5x` both read `25/10/2026 01:00`
  and `6` and `6x` both read `25/10/2026 01:30`. A constant "earliest" or "latest" ambiguity policy
  on the start label would put one of each pair on the wrong occurrence, which is why the start and
  end labels stay raw strings and the key uses the window identifier.
- **End label convention.** Every row has end minus start equal to 1,740 seconds in naive
  local-clock arithmetic (the end reads `:29` or `:59`, seconds omitted), while the dictionary
  example ends `:59` with seconds. `TODO: verify` whether the end is inclusive or exclusive and what
  the omitted seconds mean. Do not substitute the next half-hour boundary.
- **Local clock.** The start and end labels are UK local time and carry no offset. gridflow does not
  convert them in silver. Convert at the consumer, by window identifier, never by parsing the label
  alone.
- **Date order.** The body uses day-first slash dates (`%d/%m/%Y`), unlike the ISO examples in the
  dictionary. The labels are unambiguous in this capture only because the days run past the 12th and
  the window start labels (`24/10/2026`, `25/10/2026`) confirm the order. Read with the declared
  format only.
- **Creation date is not an issue time.** `Forecast produced on` has no clock and cannot be promoted
  to `published_at` or `available_at`. `TODO: verify` its relation to the actual publication time.
- **Dictionary type.** The dictionary types the two MW columns as integer and the date columns as
  ISO; the served body is a CSV of day-first dates and whole-number MW values, read here as
  `float64`.

**Activation (2026-10-13, master `7e3c023`, PR #112).** The ancillary-services batch 1 (nine
families in six package registries) merged triple-green (RULINGS 723). The family was transformed
from the 2026-10-08 capture with `--start/--end 2026-10-08`. There was no prior silver, so nothing
was overwritten and no snapshot was taken (RULINGS 725). The activation total across the nine
families is 112,730 rows, each family equal to its planned count; this family is 1,874. The
batch-wide reconcile `--all --cutoff 2026-10-12` exited 0 with 0 gaps over 159 families (47
adjudicated, 0 stale). Gridflow `@.planning/v0.22-RESULTS.md` section AS-1 holds the receipt. The batch
eligible set is Balancing Reserve day-ahead, Dynamic Moderation, Dynamic Regulation and Quick
Reserve; the five held families are listed on their own pages.

**Related.** Balancing Reserve shares the half-hour window layout and the repeated-hour issue:
@./balancing-reserve-auction-requirement-forecast.md. The Dynamic requirement and long-term
tables are in @./dynamic-moderation-requirements.md,
@./dynamic-regulation-requirements.md and @./long-term-forecasts-for-dc-dm-dr-requirements.md.
Slow Reserve has the same eight-column layout, key, clocks and temporal recipe (gridflow registry
`slow-reserve-requirement-forecast.json`): @./slow-reserve-requirement-forecast.md.
