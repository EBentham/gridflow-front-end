---
source: "neso_data_portal"
package: "slow-reserve-requirement-forecast"
dataset_key: "slow_reserve_requirement_fc"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-18
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Slow Reserve requirement forecast
  summary: >-
    NESO's daily forecast of the Slow Reserve it needs to buy: positive and negative MW for every
    half-hour service window.
  facts:
    vendor: "NESO Data Portal, package `slow-reserve-requirement-forecast`: one CSV file, no archive"
    cadence: "Updated monthly (NESO's catalogue); each auction is daily"
    grain: One row per auction date and half-hour service window, 48 on an ordinary day
  landscape: market
  what_it_is: >-
    Slow Reserve, positive and negative, reacts to a loss of generation or demand, restoring energy
    imbalances to plus or minus 0.2 Hz within 15 minutes, NESO says. NESO buys it in a daily auction
    for a service day of half-hour windows from 23:00 UK time the evening before. This file
    forecasts each window's requirement in MW.
  how_used:
    - Requirement against cleared `PSR` and `NSR` MW per window, from NESO's EAC results.
    - To join EAC results, convert `service_window_start_time` from UK local time to UTC.
    - "Point-in-time studies: each capture is one vintage, stamped with the file's `published_at`."
  chart:
    type: line
    silver: neso_data_portal/slow_reserve_requirement_fc
    time: service_delivery_date
    value: positive_slow_reserve_requirement_mw
    group: forecast_produced_on
    group_map: {"2026-08-31": aug, "2026-09-22": sep}
    series_order: [aug, sep]
    filter:
      - {column: published_at, op: eq, value: "2026-09-22T14:48:32.823004"}
    aggregation: mean
    window: {start: "2026-09-23", end: "2026-10-31"}
    unit: MW
  chart_view:
    title: Positive Slow Reserve requirement by service day
    caption: >-
      Silver `slow_reserve_requirement_fc`, MW: the positive requirement, mean of each service day's
      windows, 23 September to 31 October 2026, file last modified 22 September 2026, split by
      production date. Negative, not drawn, is also 1,800 MW in every window.
    alt: >-
      Line chart of NESO's positive Slow Reserve requirement in MW, one point per service day from
      23 September to 31 October 2026. The line is flat at 1,800 MW throughout: petrol for 23 to 30
      September, forecasts produced on 31 August, then clay for 1 to 31 October, produced on 22
      September. The negative requirement is the same, 1,800 MW throughout.
    x_label: service day (from 23:00 UK time, day before)
    y_min: 0
    key:
      - {series: aug, label: Produced 31 August, paint: petrol, note: "Service days 23 to 30 September: positive and negative both 1,800 MW in every window."}
      - {series: sep, label: Produced 22 September, paint: clay, note: "Service days 1 to 31 October: positive and negative both 1,800 MW in every window."}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then the file downloaded whole unless its
      `last_modified` is unchanged. Dates select nothing.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=slow-reserve-requirement-forecast"
      - "GET https://api.neso.energy/dataset/87d77cd4-f3c8-4fda-973b-91149ee7a0e6/resource/ccde1a9e-1885-4271-84a3-bb064194bce9/download/slow-reserve-requirement-forecast.csv"
    commands:
      - {run: gridflow ingest neso_data_portal slow_reserve_requirement_fc --last 24h, comment: "whole file; window must end recently"}
      - {run: gridflow transform neso_data_portal slow_reserve_requirement_fc --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: published_at, op: eq, value: "2026-09-22T14:48:32.823004"}
        - {column: service_delivery_date, op: in, value: ["2026-09-30", "2026-10-01", "2026-10-25"]}
        - {column: service_window, op: in, value: ["5", "6", "5x", "6x"]}
      order_by: [service_delivery_date, service_window]
      columns: [service_delivery_date, service_window, forecast_produced_on, service_window_start_time,
                positive_slow_reserve_requirement_mw, negative_slow_reserve_requirement_mw,
                auction_date, service_window_end_time, timestamp_utc, published_at]
    key: [auction_date, service_window]
    caption: "Windows 5 and 6 either side of the production-date change, and 25 October's repeated hour."
    fields:
      service_delivery_date: Service day the windows belong to; its window 1 starts 23:00 the day before
      service_window: "`1` to `48`; 25 October adds `5x`, `6x`; NESO's dictionary omits `5`, `6`"
      forecast_produced_on: Date NESO produced the forecast; a date only, not a publication time
      service_window_start_time: Window start, UK local time as NESO writes it; kept as text
      positive_slow_reserve_requirement_mw: Positive Slow Reserve requirement, MW (NESO's unit)
      negative_slow_reserve_requirement_mw: Negative Slow Reserve requirement, MW (NESO's unit), given as a positive figure
      auction_date: Date of the daily auction these requirements apply to (NESO)
      service_window_end_time: "Window end as NESO writes it (`:29` or `:59`); kept as text"
      timestamp_utc: UK midnight starting the service day, in UTC; window 1 starts an hour earlier
      published_at: "NESO's last-modified time for the whole file, read as UTC"
      bronze_capture_id: Path of the bronze capture the row was read from
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      Reads the `_latest` view, the newest capture, with `data.sql` so the cells see every day the
      file holds; `query()` reads the same view but takes a date range.
    cells:
      - |
        df = data.sql("""
            SELECT service_delivery_date, auction_date, forecast_produced_on, service_window,
                   service_window_start_time,
                   positive_slow_reserve_requirement_mw AS positive_mw,
                   negative_slow_reserve_requirement_mw AS negative_mw
            FROM silver_neso_data_portal_slow_reserve_requirement_fc_latest
            ORDER BY service_delivery_date, service_window_start_time, service_window""")
        df.groupby("forecast_produced_on").agg(
            first=("service_delivery_date", "min"), last=("service_delivery_date", "max"),
            days=("service_delivery_date", "nunique"), windows=("service_window", "count"))
      - |
        df.value_counts(["positive_mw", "negative_mw"])
      - |
        days = df.drop_duplicates("service_delivery_date").assign(
            days_ahead=lambda d: (d.service_delivery_date - d.forecast_produced_on).dt.days,
            produced=lambda d: d.forecast_produced_on.dt.strftime("%Y-%m-%d"))
        ax = days.pivot(index="service_delivery_date", columns="produced", values="days_ahead").plot(
            color=["#155A6E", "#C77E3C"], marker="o", ylim=(0, 45), figsize=(8, 3.5), rot=0,
            xlabel="service day", ylabel="days after production date")
        ax.legend(title="forecast produced on", loc="upper left");
    needs: a capture of the requirement file
    plot_alt: >-
      Line plot of the days between each forecast's production date and its service day, one point
      per service day, 23 September to 31 October 2026. Forecasts produced on 31 August (petrol) run
      23 to 30 days ahead; those produced on 22 September (clay) run 9 to 39 days ahead.
  related:
    - {dataset: neso_data_portal/eac-auction-results, note: "Cleared `PSR` and `NSR` MW and price for each half-hour window"}
    - {dataset: neso_data_portal/quick-reserve-auction-requirement-forecast, note: "Quick Reserve's requirement forecast, with the same columns and key"}
    - {dataset: neso_data_portal/balancing-reserve-auction-requirement-forecast, note: "Balancing Reserve's requirement forecast, the same windows plus a forecast type"}
    - {dataset: elexon/system_prices, note: Imbalance prices for the half-hours the reserve covers}
---

# Slow Reserve Requirement Forecast

This package is NESO's **forecast of how much Slow Reserve it expects to buy in each daily auction**.
Slow Reserve is a reserve service, separated by the vendor into **Positive Slow Reserve** (PSR) and
**Negative Slow Reserve** (NSR); the vendor text read here does not state a direction for either
(`TODO: verify` what positive and negative denote). The vendor says it is aimed at reacting to
post-fault disturbances, to restore energy imbalances to within a stated frequency band inside 15
minutes of a loss event (generation or demand). The service is procured in a daily auction held at
14:00, for delivery from 23:00 on the day before the service date to 23:00 on the service date, in
half-hour **service windows**. This data set holds the forecast of the MW NESO intends to procure
in each window, with one row per auction and window (CKAN package `notes`,
@.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json; the vendor tags
include EAC, Day-Ahead, Forecast and Subscribable).

Each row is one **auction date x service window**: the positive Slow Reserve requirement
(`positive_slow_reserve_requirement_mw`) and the negative Slow Reserve requirement
(`negative_slow_reserve_requirement_mw`), in MW, plus the window's start and end labels and the
date the forecast was produced. It is a **forecast**, not a result: it is not an awarded volume, a
clearing price or a settlement quantity. For modelling it is the demand side of the Slow Reserve
market (how much reserve NESO says it will need), to be joined later to auction results and to the
balancing-mechanism series. It is not a settlement-period table: windows are not settlement periods
(the vendor says so), and no `run_type` applies.

The package is **eligible**. Its one family has a gridflow silver output and **no hold**. The values
may be used, subject to the clock and time-label notes below. It has the same layout as the Quick
Reserve forecast, @./quick-reserve-auction-requirement-forecast.md (the one with the fuller
write-up of the window and repeated-hour behaviour), and the same window columns as
@./balancing-reserve-auction-requirement-forecast.md, whose records add a `forecast_type` column
(gridflow registry `balancing-reserve-auction-requirement-forecast.json`). The Slow Reserve
industry notifications are a separate package: @./ancillary-services-important-industry-notifications.md.

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Slow Reserve Requirement Forecast | CSV | upload | `ccde1a9e-1885-4271-84a3-bb064194bce9` |

The package has **one resource and no DOC resources**. The resource is a CKAN **upload** (so the
capture has a file name, `slow-reserve-requirement-forecast.csv`), not a datastore dump. The vendor
describes it as the forward view of the requirement for positive and negative Slow Reserve.

| Resource | Family | Download | Bytes | Data rows | CKAN `last_modified` |
|---|---|---|---:|---:|---|
| Slow Reserve Requirement Forecast | `slow_reserve_requirement_fc` | [slow-reserve-requirement-forecast.csv](https://api.neso.energy/dataset/87d77cd4-f3c8-4fda-973b-91149ee7a0e6/resource/ccde1a9e-1885-4271-84a3-bb064194bce9/download/slow-reserve-requirement-forecast.csv) | 151,639 | 1,874 | 2026-09-22T14:48:32.823004 |

Size and `last_modified` come from the capture sidecar under
`C:/gridflow-data/bronze/neso_data_portal/slow_reserve_requirement_fc/2026/10/08/`; rows are data
rows of the body (K-AS-2 FACTS section 2, capture SR1). The single capture was taken
**2026-10-08T11:24:21Z**. The SHA-256 of the body is
`77cd4e258f91a1ce99ec4a48ef3644156d3442719d934673d5e1815e3f036585` and equals the sidecar value.
Package page:
[slow-reserve-requirement-forecast](https://www.neso.energy/data-portal/slow-reserve-requirement-forecast).
Resource dictionary:
[slow_reserve_requirement_forecast](https://www.neso.energy/data-portal/slow-reserve-requirement-forecast/slow_reserve_requirement_forecast).

**What the file covers.** The body holds **39 service days, 2026-09-23 to 2026-10-31**, auction
dates 2026-09-22 to 2026-10-30. It is a rolling forward window, not a history: the captured file
holds no past service day. `TODO: verify` whether earlier forecasts are retained anywhere on the
portal, and when the first forecast was published. Do not assume this resource accumulates history.

**Bronze body (seat full-body scan, K-AS-2 FACTS g5/g6).** Strict UTF-8, one header, eight columns,
no ragged row and no blank row. The scan found no blank cell, no `-1`, `N/A`, `NA` token, no
percent sign, no thousands separator, no padded numeric cell. The body uses day-first slash dates;
the vendor dictionary's ISO examples (`2026-03-31`) do not describe what is actually served. Strict
Python CSV parsing and the Polars original-fragment parse agree on every cell of all 1,874 rows.

## Families

### `slow_reserve_requirement_fc`

- Kind: tabular · archetype: FC · refresh: monthly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Auction Date | `auction_date` | date | `%d/%m/%Y` | no | — | — |
| Service Delivery Date | `service_delivery_date` | date | `%d/%m/%Y` | no | — | — |
| Service Window | `service_window` | string | — | no | — | — |
| Service Window Start Time | `service_window_start_time` | string | — | yes | — | — |
| Service Window End Time | `service_window_end_time` | string | — | yes | — | — |
| Positive Slow Reserve Requirement MW | `positive_slow_reserve_requirement_mw` | float64 | — | yes | — | MW |
| Negative Slow Reserve Requirement MW | `negative_slow_reserve_requirement_mw` | float64 | — | yes | — | MW |
| Forecast produced on | `forecast_produced_on` | date | `%d/%m/%Y` | yes | — | — |

- Entity key: `auction_date`, `service_window`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`service_delivery_date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**One header epoch.** The record accepts one exact header, the eight columns above, spelled exactly
as in the table. Unlike the Quick Reserve file, this header uses the same capitalisation for the
start and end columns (`Service Window Start Time`, `Service Window End Time`).

**What the columns mean (vendor dictionary).** From NESO's saved field info
(@.planning/research/neso-snapshots/field-info/20261008T114228Z/slow_reserve_requirement_fc.json).

- **`Auction Date`**: "The date of the auction event that these requirements apply to". A calendar
  date with no time of day. In the body it is the day before the service date on every row.
- **`Service Delivery Date`**: "The service day for delivery of the service". The vendor comment adds
  that service window 1 starts at 23:00 on the previous date (D-1). It is a **service-day label**, not
  the start of the first window.
- **`Service Window`**: the "Service Window Identifier". The comment says it is **not** the same as a
  settlement period. Observed values are `1` to `48` on an ordinary day, plus `5x` and `6x` on the
  autumn clock-change day (see Two clocks). Kept as a string, byte-equal to the body.
- **`Service Window Start Time`** and **`Service Window End Time`**: the start and end of the window,
  "given in local time" (the UK clock). In the body they look like `22/09/2026 23:00` and
  `22/09/2026 23:29`, minute resolution. They are **raw strings** in silver: no timezone
  conversion and no endpoint repair are applied (see Known issues). The dictionary examples
  (`2026-03-31T23:00:00`, `2026-04-01T23:29:59`) use a different format and carry seconds.
- **`Positive Slow Reserve Requirement MW`**: "Requirement for Positive Slow Reserve".
- **`Negative Slow Reserve Requirement MW`**: "Requirement for Negative Slow Reserve".
- **`Forecast produced on`**: "Date that the forecast was produce[d]" (vendor spelling). A calendar
  date only: no clock, no zone, no publication instant.

**Units (vendor dictionary only).** Both requirement columns are **MW**; the dictionary also types
them as integer, and gridflow reads them as `float64` without rescaling. The date and time columns
carry no unit. Nothing is converted. The vendor unit is MW and no energy (MWh) denomination is
stated for either column: do not multiply by the half-hour to get MWh without a vendor statement
that the product is energy-denominated.

**Two clocks.**

1. **Vintage (`ckan_last_modified`).** The resource is an upload with a usable CKAN timestamp, so
   `available_at` = `published_at` = the CKAN `last_modified` of the captured file (ADR-030). In the
   capture that is **2026-09-22T14:48:32.823004Z**, one value on all 1,874 rows. That instant is
   when the file was last uploaded to the portal, not when each forecast row was first available,
   and it is not a vendor-declared publication time. It is also **not** the `Forecast produced on`
   date: that column is a creation date and is never used as an issue instant (issue is `none`).
   The capture itself was taken on 2026-10-08 (`capture_written_at` 2026-10-08T11:24:21Z). An
   as-of query before 2026-09-22T14:48:32Z sees **no** rows. Why the vintage is safe here: **all
   1,874 window starts are later than the vintage** (the earliest is 2026-09-22 22:00 UTC, i.e.
   23:00 UK local; K-AS-2 FACTS section 4.8), so the file is wholly forward-looking at that
   instant and the CKAN time stands in for availability under the forward-target rule
   (RULINGS 529). `TODO: verify` the original production-time availability and immutability of the
   forecast values, and whether rows are amended in place at the monthly refresh: one capture
   exists, so revision behaviour cannot be measured.
2. **Event time (temporal recipe `date_sp1` on `service_delivery_date`).** `timestamp_utc` and
   `event_time` are equal on every row and are the **UK local midnight at the start of the service
   date, expressed in UTC** (the settlement-period-1 start of that date). For a summer date that is
   23:00 UTC the previous evening (service date 2026-09-23 gives `2026-09-22T23:00:00Z`; the autumn
   change date 2026-10-25 gives `2026-10-24T23:00:00Z`); for a winter date it is 00:00 UTC
   (2026-10-26 gives `2026-10-26T00:00:00Z`). It is a **calendar-date storage anchor**. It is
   **not** the start of service window 1, and the two are not the same clock: window 1 begins at
   23:00 UK local on the **previous** date (for 2026-09-23 that is `2026-09-22 23:00` local, which is
   `2026-09-22T22:00:00Z`). Every one of a day's 48 or 50 rows therefore carries the **same**
   `timestamp_utc`. To place a row inside the day, use `service_window` together with the raw start
   and end labels, not the timestamp (RULINGS 720; no composed date-plus-window recipe exists,
   RULINGS 572 and 588). `TODO: verify` a row-specific conversion mechanism if a true per-window
   UTC instant is ever needed.

**Identity and selection.**

- The record key is `(auction_date, service_window)`. All 1,874 rows are distinct on it, in the body
  and in silver. A key on the start label alone is **wrong**: it has two duplicate rows on the autumn
  change date, where windows `5`/`5x` both start at `01:00` and `6`/`6x` both start at `01:30` (see
  Known issues). The vendor guarantees no key; `TODO: verify` a vendor-guaranteed identity and
  whether a row can be revised in place.
- `_latest` is `whole_capture`: the newest complete capture of the one resource. There is no
  per-key latest, no `key_latest` and no resource partition (one resource only).

**Sentinels and missing values (FACTS g5).** No sentinel exists and the record declares no null
tokens. In silver (2026-10-13) no column has a null, and the body has no zero in either requirement
column, so no zero-versus-missing question arises in this capture.

**Row counts and shape (silver, 2026-10-13).**

| Resource | Rows | Distinct on entity key |
|---|---:|---:|
| `ccde1a9e-1885-4271-84a3-bb064194bce9` | 1,874 | 1,874 |

The planned and activated counts agree (1,874), with 0 validation failures and 0 blank rows
excluded. The body has **38 service days with 48 windows and one with 50** (the autumn change date,
2026-10-25): 38 x 48 + 50 = 1,874. The requirement values observed are: positive requirement
**1800 MW on all 1,874 rows**; negative requirement **1800 MW on all 1,874 rows**. These are
single-capture observations of a forecast, not a vendor-stated range.

Silver layout: one Parquet file per capture under
`C:/gridflow-data/silver/neso_data_portal/slow_reserve_requirement_fc/year=2026/month=10/`. The
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

The family has **no hold**: it was specified as eligible and activated as such (RULINGS 727, 730,
731). The questions below are open evidence requests, not holds.

**Known issues and open questions.**

- **Repeated autumn hour.** The captured autumn change date (2026-10-25, 50 windows) is the only
  clock-change day in the body. Its four rows around the change read: window `5`
  `25/10/2026 01:00` to `01:29`; window `6` `01:30` to `01:59`; window `5x` `01:00` to `01:29`;
  window `6x` `01:30` to `01:59`. The vendor comment says service windows `7x` and `8x` are the
  repeated hour at the GMT-to-BST change and that "for BST to GMT clock change day there is no
  service window 5 or 6". The captured body and NESO's own EAC market design explainer
  (already adjudicated for the batch 1 reserve pages, K-AS-1 FACTS) say the opposite: at the
  autumn (BST to GMT) change the day gains windows **`5x` and `6x`**, with the repeated windows'
  start labels equal to those of `5` and `6`. Use the diagrams and the body, not the dictionary
  comment. `TODO: verify` the spring (GMT to BST) layout when a spring-change service day is first
  captured; no spring body is in hand.
- **Start labels are not unique.** Start and end labels each have only **1,872 distinct values**
  across the 1,874 rows: on 2026-10-25 windows `5` and `5x` both read `25/10/2026 01:00` and `6`
  and `6x` both read `25/10/2026 01:30`. A constant "earliest" or "latest" ambiguity policy on the
  start label would put one of each pair on the wrong occurrence, which is why the start and end
  labels stay raw strings and the key uses the window identifier.
- **End label convention.** Every row has end minus start equal to 1,740 seconds in naive
  local-clock arithmetic (the end reads `:29` or `:59`, seconds omitted), while the dictionary
  example ends `:59` with seconds. `TODO: verify` whether the end is inclusive or exclusive and what
  the omitted seconds mean. Do not substitute the next half-hour boundary.
- **Local clock.** The start and end labels are UK local time and carry no offset. gridflow does not
  convert them in silver. Convert at the consumer, by window identifier, never by parsing the label
  alone.
- **Date order.** The body uses day-first slash dates (`%d/%m/%Y`), unlike the ISO examples in the
  dictionary. Read with the declared format only.
- **Creation date is not an issue time.** `Forecast produced on` has no clock and cannot be promoted
  to `published_at` or `available_at`. `TODO: verify` its relation to the actual publication time;
  until then the upload vintage stands and is not backdated to production-date midnight.
- **Dictionary type.** The dictionary types the two MW columns as integer and the date columns as
  ISO; the served body is a CSV of day-first dates and whole-number MW values, read here as
  `float64`.
- **Constant requirement.** Both requirement columns read 1800 in every row of this capture. That is
  a measured value, not a vendor default; do not treat it as a fixed requirement. The dictionary
  example for the same columns is 1700.

**Activation (2026-10-13, master `fccbdeb`, PR #113).** The ancillary-services batch 2 (twelve
families in six package registries) merged triple-green (RULINGS 730). The family was transformed
from the 2026-10-08 capture with `--start/--end 2026-10-08`. There was no prior silver, so nothing
was overwritten and no snapshot was taken (RULINGS 731). The activation total across the eleven
families with a record is 241,160 rows, each family equal to its planned count; this family is
1,874. The batch-wide reconcile `--all --cutoff 2026-10-12` exited 0 with 0 gaps over 170 families
(47 adjudicated, 0 stale). Gridflow `@.planning/v0.22-RESULTS.md` section AS-2 holds the receipt.
The batch eligible set is nine families (233,437 rows); the two held families and the one family
with no record (contract transfer obligation, stays ingest-only) are listed on their own pages.

**Related.** Quick Reserve shares the half-hour window layout and the repeated-hour issue:
@./quick-reserve-auction-requirement-forecast.md; so does Balancing Reserve:
@./balancing-reserve-auction-requirement-forecast.md. The Slow Reserve industry notifications are in
@./ancillary-services-important-industry-notifications.md.
