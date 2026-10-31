---
source: "neso_data_portal"
package: "balancing-reserve-auction-requirement-forecast"
dataset_keys: ["br_auction_requirement_fc_da", "br_auction_requirement_fc_da_archive", "br_auction_requirement_fc_medium_term"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-18
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Balancing Reserve requirement forecast
  summary: >-
    NESO's forecast Balancing Reserve requirement for each daily auction: positive and negative MW
    for every half-hour service window of the delivery day.
  facts:
    vendor: "NESO Data Portal, package `balancing-reserve-auction-requirement-forecast`: three tables from four CSV files"
    cadence: "Daily (NESO's catalogue); current files are overwritten, earlier days moved to archives"
    grain: One row per auction date and half-hour service window, 48 on an ordinary day
  landscape: market
  what_it_is: >-
    NESO buys Balancing Reserve, positive and negative reserve held on BM units, in a daily auction
    for a delivery day of half-hour windows from 23:00 UK time. These files forecast each window's
    requirement in MW: a medium-term view first, then the day-ahead refinement, in a file NESO
    replaces daily.
  how_used:
    - Requirement against cleared `PBR` and `NBR` MW per window, from NESO's EAC results.
    - To join EAC results, convert `service_window_start_time` from UK local time to UTC.
    - Day-ahead positive and negative requirement per window as a reserve-price model feature.
  chart:
    type: line
    silver: neso_data_portal/br_auction_requirement_fc_da
    time: service_window_start_time
    time_text: {format: "%Y-%m-%d %H:%M:%S"}
    filter:
      - {column: service_delivery_date, op: eq, value: "2026-10-18"}
    values:
      - {column: positive_balancing_reserve_requirement_mw, series: positive}
      - {column: negative_balancing_reserve_requirement_mw, series: negative}
    aggregation: mean
    window: {start: "2026-10-17", end: "2026-10-18"}
    unit: MW
  chart_view:
    title: Balancing Reserve requirement by window, 18 October 2026
    caption: >-
      Silver `br_auction_requirement_fc_da`, MW: NESO's day-ahead forecast for service day 18
      October 2026 (auction 17 October), from 23:00 the evening before: one value per half-hour
      window, drawn at each window's start on the UK clock as NESO writes it.
    alt: >-
      Line chart of NESO's day-ahead Balancing Reserve requirement in MW for the 48 half-hour
      windows of service day 18 October 2026, from 23:00 on 17 October, UK local time. Negative
      reserve is flat at 1,450 MW. Positive reserve is 200 MW from 23:00, 400 MW from 03:00, 600 MW
      from 07:00, 500 MW from 11:00, 600 MW from 15:00 and 400 MW from 19:00 to the last window,
      22:30.
    x_label: window start, UK local time as written
    y_min: 0
    key:
      - {series: positive, label: Positive reserve, paint: petrol, note: "Steps only at the four-hour EFA block edges from 23:00 this day: 200 to 600 MW."}
      - {series: negative, label: Negative reserve, paint: clay, note: "NESO gives it as a positive figure: 1,450 MW in every window here."}
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show`, then each file whole unless `last_modified` is
      unchanged; its name's hash prefix can change. Dates select nothing. Swap in any table's key.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=balancing-reserve-auction-requirement-forecast"
    commands:
      - {run: gridflow ingest neso_data_portal br_auction_requirement_fc_da --last 24h, comment: "whole files; window must end recently"}
      - {run: gridflow transform neso_data_portal br_auction_requirement_fc_da --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: service_delivery_date, op: eq, value: "2026-10-18"}
        - {column: service_window, op: in, value: ["1", "8", "9", "16", "17", "24", "25", "48"]}
      order_by: [service_window_start_time]
      columns: [service_window, service_window_start_time, positive_balancing_reserve_requirement_mw,
                negative_balancing_reserve_requirement_mw, auction_date, service_delivery_date,
                service_window_end_time, forecast_produced_on, forecast_type]
    key: [auction_date, service_window]
    caption: "Service day 18 October 2026: its first and last windows and either side of three steps."
    fields:
      service_window: "Window number, `1` to `48`; spring drops `5`, `6`, autumn adds `5x`, `6x`"
      service_window_start_time: Window start, UK local time as NESO writes it; kept as text
      positive_balancing_reserve_requirement_mw: Positive reserve requirement, MW (NESO's unit)
      negative_balancing_reserve_requirement_mw: Negative reserve requirement, MW (NESO's unit), given as a positive figure
      auction_date: Date of the daily auction the forecast is for, as NESO labels it
      service_delivery_date: Service day the windows belong to; its window 1 starts 23:00 the day before
      service_window_end_time: "Window end as NESO writes it (`:29` or `:59`); kept as text"
      forecast_produced_on: Date NESO produced the forecast; a date only, not a publication time
      forecast_type: "`Dayahead` in this table; the medium-term files say `Medium term`"
      timestamp_utc: UK midnight opening the delivery date, in UTC; window 1 starts an hour earlier
      published_at: "NESO's last-modified time for the whole file, read as UTC"
      bronze_capture_id: Path of the bronze capture the row was read from
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      Reads with `data.sql` from the `_latest` view, the newest capture, because NESO replaces the
      file daily and a dated `query()` finds rows only for the day it holds.
    cells:
      - |
        df = data.sql("""
            SELECT auction_date, service_delivery_date, forecast_produced_on, service_window,
                   service_window_start_time,
                   positive_balancing_reserve_requirement_mw AS positive_mw,
                   negative_balancing_reserve_requirement_mw AS negative_mw
            FROM silver_neso_data_portal_br_auction_requirement_fc_da_latest
            ORDER BY service_window_start_time, service_window""")
        df.groupby(["auction_date", "service_delivery_date", "forecast_produced_on"]).size()
      - |
        steps = df[df.positive_mw.ne(df.positive_mw.shift())]
        steps[["service_window", "service_window_start_time", "positive_mw", "negative_mw"]]
      - |
        df.set_index(df.service_window_start_time.str[11:16])[["positive_mw", "negative_mw"]].plot(
            drawstyle="steps-post", color=["#155A6E", "#C77E3C"], ylim=(0, 1600), figsize=(8, 3.5),
            rot=0, xlabel="window start, UK local time as written", ylabel="requirement, MW");
    needs: a capture of the day-ahead table
    plot_alt: >-
      Step plot of the day-ahead Balancing Reserve requirement in MW for each half-hour window of
      service day 18 October 2026, from 23:00 on 17 October to 22:30, UK local time as written.
      Negative reserve (clay) holds 1,450 MW. Positive reserve (petrol) steps 200, 400, 600, 500, 600
      and 400 MW, changing at 03:00, 07:00, 11:00, 15:00 and 19:00.
  related:
    - {dataset: neso_data_portal/eac-auction-results, note: "Cleared `PBR` and `NBR` MW and price for the same windows"}
    - {dataset: neso_data_portal/eac-br-auction-results, note: Results of the earlier Balancing Reserve auctions}
    - {dataset: neso_data_portal/quick-reserve-auction-requirement-forecast, note: "The same forecast for Quick Reserve, per service window"}
    - {dataset: elexon/system_prices, note: Imbalance prices for the half-hours the reserve covers}
  family:
    slug: balancing-reserve-auction-requirement-forecast
    members:
      - dataset: br_auction_requirement_fc_da
        differs: Day-ahead forecast; NESO replaces the file daily
        request: "GET https://api.neso.energy/dataset/6b31e0f0-f711-461c-84bb-4ed4775a9992/resource/019f6fba-4f17-4056-9ef8-31df44ff2e30/download/132671df40b4484aa1638b6c8e9a57a4_balancing-reserve-day-ahead-auction-requirements-forecast.csv"
      - dataset: br_auction_requirement_fc_da_archive
        differs: Earlier day-ahead forecasts, moved here as NESO replaces the current file
        request: "GET https://api.neso.energy/dataset/6b31e0f0-f711-461c-84bb-4ed4775a9992/resource/b9ce03d0-c189-44ef-92e4-c02e91feb65d/download/a0664df3495746588204c88cbfbce45d_balancing-reserve-day-ahead-auction-requirement-forecast-archiv.csv"
        held: NESO does not say when each archived forecast was published, or whether it is ever amended.
      - dataset: br_auction_requirement_fc_medium_term
        differs: "Medium-term forecast without detailed wind and solar forecasts; a current and an archive file"
        request:
          - "GET https://api.neso.energy/dataset/6b31e0f0-f711-461c-84bb-4ed4775a9992/resource/a9470515-c1de-4c4b-9597-2d78bf24c29f/download/dd18490b18ff4f449412e3d3b3415a20_balancing-reserve-requirements-medium-term-forecast.csv"
          - "GET https://api.neso.energy/dataset/6b31e0f0-f711-461c-84bb-4ed4775a9992/resource/fb2e0eea-b1c0-4ba3-a817-0561182a6e26/download/3ec3e0603862483798b0f555ad4bb440_balancing-reserve-requirements-medium-term-forecast-archive.csv"
        held: Its table includes the archive file, and NESO does not say when archived forecasts were published.
---

# Balancing Reserve Auction Requirement Forecast

NESO's forecast of how much **Balancing Reserve** it will buy. Balancing Reserve secures firm
positive and negative reserve on BM units at the day-ahead stage. NESO procures it in a daily
auction at 08:15 for delivery from 23:00 to 23:00 on D+1 (the vendor's package description;
exact times are the vendor's wording and the clock zone is not restated there, so
`TODO: verify` the zone). This package publishes the **requirement** for that auction: for each
half-hour *service window* of a service day, the megawatts of positive reserve and of negative
reserve NESO expects to procure. It does not publish auction results, prices or awarded units.
Use it to see how much reserve the system operator needs to hold ahead of delivery, and how the
requirement changes between the coarse medium-term view and the refined day-ahead view.

The vendor describes two forecast products. The **medium-term** forecast gives an approximate
requirement without detailed wind and solar forecasts. The **day-ahead** forecast refines the
medium-term figure with the latest short-term features. Each is a separate current file that
the vendor overwrites daily, with the previous entries moved to an archive file. The vendor
adds that forecasts published after 27 February are Live Demand Forecasts; the year is not
given (`TODO: verify` which year).

Four CSV resources are captured, mapped to three gridflow families. Only the current day-ahead
file is eligible for publication. Both archive-bearing families are held (see Holds). The
reserve auction and balancing-mechanism context is in
@../../../20-domain/markets/gb-balancing-mechanism.md.

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Balancing Reserve Day ahead auction requirement forecast (Archive) | CSV | upload | `b9ce03d0-c189-44ef-92e4-c02e91feb65d` |
| Balancing Reserve Day ahead auction requirements forecast | CSV | upload | `019f6fba-4f17-4056-9ef8-31df44ff2e30` |
| Balancing Reserve Requirements Medium term forecast | CSV | upload | `a9470515-c1de-4c4b-9597-2d78bf24c29f` |
| Balancing Reserve Requirements Medium term forecast (Archive) | CSV | upload | `fb2e0eea-b1c0-4ba3-a817-0561182a6e26` |

There are no DOC or other-disposition resources in this package: all four resources are CSV,
CKAN datastore active, and all four go to silver. Download links are the URLs in the 2026-10-06
catalogue snapshot. The file name carries a vendor hash prefix and can change, so the stable
handle is the resource id.

- Day-ahead current, `br_auction_requirement_fc_da`:
  [balancing-reserve-day-ahead-auction-requirements-forecast.csv](https://api.neso.energy/dataset/6b31e0f0-f711-461c-84bb-4ed4775a9992/resource/019f6fba-4f17-4056-9ef8-31df44ff2e30/download/69ca2874825b4c709e685a9f65e16761_balancing-reserve-day-ahead-auction-requirements-forecast.csv).
  Captured as `raw_20261008T085201Z_019f6fba-4f17-4056-9ef8-31df44ff2e30_55978d13.csv`,
  4,722 bytes, 48 data rows, one header epoch.
- Day-ahead archive, `br_auction_requirement_fc_da_archive`:
  [balancing-reserve-day-ahead-auction-requirement-forecast-archiv.csv](https://api.neso.energy/dataset/6b31e0f0-f711-461c-84bb-4ed4775a9992/resource/b9ce03d0-c189-44ef-92e4-c02e91feb65d/download/01687c8c0834407fae6020cff46657c7_balancing-reserve-day-ahead-auction-requirement-forecast-archiv.csv).
  Captured as `raw_20261008T085205Z_b9ce03d0-c189-44ef-92e4-c02e91feb65d_8ff327b8.csv`,
  4,337,894 bytes, 46,414 data rows, one header epoch.
- Medium-term current, `br_auction_requirement_fc_medium_term`:
  [balancing-reserve-requirements-medium-term-forecast.csv](https://api.neso.energy/dataset/6b31e0f0-f711-461c-84bb-4ed4775a9992/resource/a9470515-c1de-4c4b-9597-2d78bf24c29f/download/f794c8df01f24e2999b018b6c095461b_balancing-reserve-requirements-medium-term-forecast.csv).
  Captured as `raw_20261008T085211Z_a9470515-c1de-4c4b-9597-2d78bf24c29f_69d332df.csv`,
  65,277 bytes, 672 data rows, one header epoch.
- Medium-term archive, `br_auction_requirement_fc_medium_term`:
  [balancing-reserve-requirements-medium-term-forecast-archive.csv](https://api.neso.energy/dataset/6b31e0f0-f711-461c-84bb-4ed4775a9992/resource/fb2e0eea-b1c0-4ba3-a817-0561182a6e26/download/331c281fca13498f8957aa8cf3bbc6d6_balancing-reserve-requirements-medium-term-forecast-archive.csv).
  Captured as `raw_20261008T085208Z_fb2e0eea-b1c0-4ba3-a817-0561182a6e26_a29eb9b5.csv`,
  4,476,944 bytes, 46,414 data rows, one header epoch.

Each resource has **two** captured bodies (2026-10-08 and 2026-10-16; bronze sidecars under
`C:/gridflow-data/bronze/neso_data_portal/br_auction_requirement_fc_*/2026/10/`). Measured on
silver 2026-10-18: in both archives every 2026-10-08 row is present in the 2026-10-16 body with
equal values, window labels and production dates; each archive gained 432 rows (service days
2026-10-09 to 2026-10-17). The rows comparable with the 2026-10-08 current files are equal: all 48
day-ahead rows for 2026-10-09, and all 672 medium-term rows (432 now in the archive, 240 still in
the current file). Two captures do not make a vendor rule: whether a later capture amends a row
in place, or drops a target, stays `TODO: verify` (gridflow `@.planning/phases/v0.22-K-AS-1/K-AS-1-FACTS.md` g3).

## Families

### `br_auction_requirement_fc_da`

- Kind: tabular · archetype: FC · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Auction Date | `auction_date` | date | `%Y-%m-%d` | no | — | — |
| Service Delivery Date | `service_delivery_date` | date | `%Y-%m-%d` | no | — | — |
| Service Window | `service_window` | string | — | no | — | — |
| Service window start time | `service_window_start_time` | string | — | yes | — | — |
| Service Window End Time | `service_window_end_time` | string | — | yes | — | — |
| Positive Balancing Reserve Requirement MW | `positive_balancing_reserve_requirement_mw` | float64 | — | yes | — | MW |
| Negative Balancing Reserve Requirement MW | `negative_balancing_reserve_requirement_mw` | float64 | — | yes | — | MW |
| Forecast produced on | `forecast_produced_on` | date | `%Y-%m-%d` | yes | — | — |
| Forecast type | `forecast_type` | string | — | yes | — | — |

- Entity key: `auction_date`, `service_window`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`service_delivery_date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**This family is eligible.** It is the one output of the package cleared for publication.

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the CKAN `last_modified`
   of the captured file: `2026-10-07T13:05:02.227904`. CKAN emits it without an offset;
   gridflow reads it as UTC (gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`).
   All 48 silver rows share this one vintage. The record's issue recipe is `none`: the file has
   no issue-time column. `Forecast produced on` is a **date** (here `2026-10-07`), not an issue
   instant, and gridflow does not promote it to one, since that would invent a clock and an
   availability instant. `TODO: verify` the clock, zone and availability rule for it.
2. **Event time (`date_sp1` on `service_delivery_date`).** `timestamp_utc` = `event_time` = the
   start of settlement period 1 of the service delivery date, i.e. UK local midnight of that date
   expressed in UTC. Checked on every silver row on 2026-10-13. This is a **date anchor**. It is
   **not** the start of service window 1: window 1 starts at 23:00 UK local on the previous
   calendar date, one hour before the anchor. The window clocks stay in the raw
   `service_window_start_time` / `service_window_end_time` strings. `timestamp_utc` is not the
   capture time.

**Why it is eligible (forward-target rule, RULINGS 529).** Every target in the capture is later
than the capture's CKAN vintage: all 48 service-delivery dates and all 48 window starts fall
after `2026-10-07T13:05:02Z`. The forecast was therefore public before the service day began, so
the CKAN vintage is a valid conservative proxy for the missing issue time. Eligibility holds
only while that property continues to hold for each capture.

**Window layout.** Each service day has half-hour windows `1`..`48` on an ordinary day. The
capture covers auction date 2026-10-08 and service day 2026-10-09 (`forecast_type` is
`Dayahead`). Per the vendor's EAC explainer (Appendix B), the clock is UK local time and the
first window of a service day starts at 23:00 on the previous local date. On the autumn
clock-change day, windows `5x` and `6x` are added and repeat the local start labels of `5` and
`6`. The spring clock-change day omits `5` and `6` (see Known quirks for the dictionary conflict).
The window label is therefore needed to tell the repeated autumn labels apart.

**Time-column treatment (FACTS g1).**

- `Auction Date`, `Service Delivery Date`: vendor calendar dates, no time of day, ISO
  `%Y-%m-%d`.
- `Service window start time`, `Service Window End Time`: UK local clock labels kept as **raw
  strings**, observed form `%Y-%m-%d %H:%M:%S`. gridflow does not build an instant from them: the
  engine cannot choose between the two occurrences of a repeated autumn hour from the window
  label (RULINGS 572 and 588, FACTS §5.1). `TODO: verify` the endpoint convention: in the
  capture every end label is 1,740 seconds after its start label (a `:29` or `:59` minute with
  seconds `00`), while the vendor dictionary's examples end in seconds `59`. End labels are kept
  literally and not repaired.
- `Forecast produced on`: date label, see clock 1.

**Units (vendor dictionary).** Both requirement columns are **MW**, declared by the vendor
dictionary for the day-ahead file (field-info units; FACTS g4). The unit was not inferred from
the column name or from magnitudes. Positive and negative requirements are separate wide
columns. In the capture the positive requirement ranges from 200 to 600 MW and the negative
requirement is 1,450 MW in every window.

**Sentinels and missing values (FACTS g5).** The record declares no null token. The capture has
no blank cells, no `-1`, `N/A`, `NA`, `NULL`, `null` or `NaN` tokens, no padded cells, and no
embedded commas or percent signs. There are no zeros in this capture and no nulls in silver.

**Identity and selection.** The measured guard key is (`auction_date`, `service_window`),
which is unique in the capture (48 keys, no duplicates). No vendor text declares it a revision
identity (`TODO: verify`). `_latest` is `whole_capture`: the newest capture replaces the
previous one as a whole.

**Silver sample** (2 of 48 rows; lineage columns omitted):

```python
[
    {"auction_date": "2026-10-08", "service_delivery_date": "2026-10-09", "service_window": "1",
     "service_window_start_time": "2026-10-08 23:00:00", "service_window_end_time": "2026-10-08 23:29:00",
     "positive_balancing_reserve_requirement_mw": 200.0, "negative_balancing_reserve_requirement_mw": 1450.0,
     "forecast_produced_on": "2026-10-07", "forecast_type": "Dayahead"},
    {"auction_date": "2026-10-08", "service_delivery_date": "2026-10-09", "service_window": "2",
     "service_window_start_time": "2026-10-08 23:30:00", "service_window_end_time": "2026-10-08 23:59:00",
     "positive_balancing_reserve_requirement_mw": 200.0, "negative_balancing_reserve_requirement_mw": 1450.0,
     "forecast_produced_on": "2026-10-07", "forecast_type": "Dayahead"},
]
```

Both rows carry the same `timestamp_utc` / `event_time` (2026-10-08T23:00:00Z, the date anchor)
and `published_at` = `available_at` = 2026-10-07T13:05:02.227904Z.

### `br_auction_requirement_fc_da_archive`

- Kind: tabular · archetype: FC · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Auction Date | `auction_date` | date | `%Y-%m-%d` | no | — | — |
| Service Delivery Date | `service_delivery_date` | date | `%Y-%m-%d` | no | — | — |
| Service Window | `service_window` | string | — | no | — | — |
| Service window start time | `service_window_start_time` | string | — | yes | — | — |
| Service Window End Time | `service_window_end_time` | string | — | yes | — | — |
| Positive Balancing Reserve Requirement MW | `positive_balancing_reserve_requirement_mw` | float64 | — | yes | — | MW |
| Negative Balancing Reserve Requirement MW | `negative_balancing_reserve_requirement_mw` | float64 | — | yes | — | MW |
| Forecast produced on | `forecast_produced_on` | date | `%Y-%m-%d` | yes | — | — |
| Forecast type | `forecast_type` | string | — | yes | — | — |

- Entity key: `auction_date`, `service_window`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`service_delivery_date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Held (unit E-SEM).** The silver output exists on disk (**46,414 rows**, one capture, no nulls,
`forecast_type` `Dayahead`) but is not eligible for publication or point-in-time use. This page
gives schema, row counts and structural counts only. It gives no data values or ranges for this
family. See Holds.

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the CKAN `last_modified`
   of the archive file, `2026-10-07T13:05:08.053897` (offset-less, read as UTC per ADR-030). All
   46,414 rows share this one vintage. It says when the archive file last changed. It does
   **not** say when any archived forecast became available: most rows describe targets that were
   already past by the time of the capture (46,349 of 46,414 window starts are on or before the
   vintage; 65 are after). The record's issue recipe is `none`. `Forecast produced on` is kept as
   a date label, with 944 distinct production labels and production-to-delivery leads of 2 and
   15 days, so it cannot be read as one uniform day-ahead issue series.
2. **Event time (`date_sp1` on `service_delivery_date`).** `timestamp_utc` = `event_time` = UK
   local midnight of the service delivery date in UTC. Checked on every silver row on
   2026-10-13. It is a date anchor, not the capture time and not the start of window 1. The
   window clocks stay raw strings.

The archive carries 50 distinct window labels because the autumn clock-change days include `5x`
and `6x`. A key on the raw start-time string alone would collide on those days (4 duplicate
excess rows measured); (`auction_date`, `service_window`) is unique across all 46,414 rows.

**Units.** Both requirement columns are **MW** (vendor dictionary, as for the current file).
**Sentinels.** No null token is declared and none occurs. Zeros occur in both requirement
columns and are kept as numeric zero. The vendor does not say whether a zero means "no
requirement" or "no forecast"; `TODO: verify`.

**Identity and selection.** Guard key (`auction_date`, `service_window`); `_latest` is
`whole_capture`. The vendor's description says previous entries are archived to this file
daily. That states the intended operation, not that archived rows are immutable or were public
at their original issue time.

### `br_auction_requirement_fc_medium_term`

- Kind: tabular · archetype: FC · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Auction Date | `auction_date` | date | `%Y-%m-%d` | no | — | — |
| Service Delivery Date | `service_delivery_date` | date | `%Y-%m-%d` | no | — | — |
| Service Window | `service_window` | string | — | no | — | — |
| Service window start time | `service_window_start_time` | string | — | yes | — | — |
| Service Window End Time | `service_window_end_time` | string | — | yes | — | — |
| Positive Balancing Reserve Requirement MW | `positive_balancing_reserve_requirement_mw` | float64 | — | yes | — | — |
| Negative Balancing Reserve Requirement MW | `negative_balancing_reserve_requirement_mw` | float64 | — | yes | — | — |
| Forecast produced on | `forecast_produced_on` | date | `%Y-%m-%d` | yes | — | — |
| Forecast type | `forecast_type` | string | — | yes | — | — |

- Entity key: `resource_id`, `auction_date`, `service_window`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: date_sp1 (`service_delivery_date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Held (unit E-SEM).** One family holds two resources, the current file and its archive. Silver
holds **47,086 rows**: 46,414 from the archive resource and 672 from the current resource
(`forecast_type` `Medium term`, no nulls). The family is held as a whole because the archive
half fails the forward-target test. This page gives schema, row counts and structural counts
only, and no data values or ranges. See Holds. The current resource on its own is all-forward
(all 672 window starts are after its vintage). Serving it separately would change the family's
resource scope, and that is a later decision, not made here.

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`), per resource.** `published_at` = `available_at` = each
   resource's own CKAN `last_modified`, both offset-less and read as UTC: current resource
   `2026-10-07T13:05:12.119883`, archive resource `2026-10-07T13:05:18.722316`. The silver table
   therefore has **two** distinct vintages, one per resource, and a `resource_id` column
   that the other two families do not have. The record's issue recipe is `none`. `Forecast
   produced on` is a date label only. In both resources every production-to-delivery lead is
   15 days, but no publication instant is given.
2. **Event time (`date_sp1` on `service_delivery_date`).** `timestamp_utc` = `event_time` = UK
   local midnight of the service delivery date in UTC. Checked on every silver row on
   2026-10-13. It is a date anchor, not the capture time and not the start of window 1.

**Why `resource_id` is in the key.** The two resources have identical headers and disjoint
targets. Selecting a single newest capture for the whole family would silently drop one complete
body. The record therefore partitions `_latest` by `resource_id` (gridflow
`@docs/DECISION_LOG/ADR-039-neso-multi-resource-selection.md`), and `resource_id` is part of the
guard key. Neither resource has a conflicting overlap with the other in the captures, but the
vendor gives no precedence rule if they ever disagree (`TODO: verify`, FACTS §5.3).

**Units.** The schema table shows no vendor unit because the medium-term dictionary leaves it
blank. The unit is **MW**, by a documented evidence transfer, not by inference from the column
name: the vendor's shared Balancing Reserve requirements definition and its capacity procurement
guidance describe the requirement in megawatts, and the day-ahead dictionaries of this same
package declare MW for identically named columns (FACTS §4.3, g4).

**Sentinels.** No null token is declared and none occurs. Zeros occur in the archive resource's
requirement columns and are kept as numeric zero; the current resource has none. Meaning of a
zero is not established (`TODO: verify`).

**Medium-term retention wording.** The vendor says medium-term figures are retained without
closer-to-real-time revision, and that a day is removed from the rolling file and appended to
the archive. This is evidence of intended value retention. It does not give a publication
instant and does not prove availability at the start of the production date.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Daily

The vendor says the datasets are overwritten daily and the previous entries archived to the
history file. Captures to date: two per resource (2026-10-08 and 2026-10-16), eight days apart,
so the daily roll into the archives is seen only across that gap (see Files by disposition). The day-ahead and medium-term
files are separate series on separate rolling windows: the day-ahead current file covered one
service day in the capture, the medium-term current file covered 14.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `br_auction_requirement_fc_da_archive`: held: TODO: BR-ARCHIVE-AVAILABILITY — archive rows carry only a production date (944 labels, leads of 2 and 15 days); when was each forecast published, and are archived values ever amended? (unit v0.22-K-AS-1)
- `br_auction_requirement_fc_medium_term`: held: TODO: BR-MT-ARCHIVE-AVAILABILITY — the archive resource's targets are past (46,349 window starts on/before the vintage) and its production dates carry no publication instant; when was each medium-term forecast available? (unit v0.22-K-AS-1)

The two quoted lines are the registry records' hold text, generated and kept verbatim. The
records name the unit that opened the question (v0.22-K-AS-1). The unit that must answer it is
**E-SEM**. These holds follow the seat rulings of 2026-10-12 and 2026-10-13 (RULINGS 718, 720,
723, 725, all PROXY-SOURCED) and the forward-target rule (RULINGS 529): a capture whose targets
are already past at its CKAN vintage cannot use that vintage as a point-in-time proxy, and the
only per-row label, `Forecast produced on`, is a date with no instant.

What would lift each hold:

1. A vendor statement of when each archived forecast was published, and whether archived values
   are ever amended (day-ahead archive).
2. The same for the medium-term archive resource (publication instant for each production
   date).
3. For both, later complete captures of the same resource compared against the hash-pinned
   2026-10-08 bodies, to measure in-place amendment and dropped targets.

The silver outputs of both held families stay on disk. This page publishes no data values from
them; row counts and schema are the only content given.

`br_auction_requirement_fc_da` is **eligible** and is not held. The package-level
`eligibility: eligible` in the front matter is the package registry entry (4 resources, all
SILVER); the hold is per family.

## Activation

Merged as PR #112 (master `7e3c023`, triple-green: CI, diff review APPROVE, verification passed;
RULINGS 723). Transformed (RULINGS 725) for `--start/--end 2026-10-08` with no prior silver, so
nothing was overwritten: `br_auction_requirement_fc_da` **48**, `br_auction_requirement_fc_da_archive`
**46,414**, `br_auction_requirement_fc_medium_term` **47,086** (two resources). Every count
equals the planned count. Reconcile `--all --cutoff 2026-10-12` exited 0 over 159 families with
0 gaps, 47 adjudicated and 0 stale (gridflow `@.planning/v0.22-RESULTS.md` §AS-1).

Silver columns beyond the vendor columns: `timestamp_utc`, `published_at`,
`bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id`,
`dataset_version`, plus `resource_id` on the medium-term family. All timestamps are tz-aware UTC.
`dataset_version` reads `1+e1` (record version 1, epoch 1).

## Known quirks

- **Window clocks are raw strings.** Do not parse `service_window_start_time` as a UTC
  timestamp. The values are UK local time. On the autumn change day the labels `5`/`5x` share one
  start label and `6`/`6x` share another, so the `service_window` label is required to identify the
  occurrence. A constant "earliest" or "latest" ambiguity policy would misplace one of each pair.
  `TODO: verify` a row-specific conversion mechanism (an engine feature, not a vendor fact).
- **`timestamp_utc` is a date anchor.** It is the same for all 48 windows of a service day. Do not
  read it as window or EFA start.
- **Vendor dictionary clock-change wording conflicts with the data.** The dictionary's comment on
  windows at clock changes is contradicted by the vendor's EAC explainer diagrams and by the
  archive bodies (spring omits `5`/`6`, autumn adds `5x`/`6x`). gridflow follows the diagrams and
  the data. `TODO: verify` a corrected dictionary.
- **End labels are literal.** Captured end labels are 1,740 seconds after the start label, and the
  dictionary examples show seconds `59`. gridflow does not substitute the next half-hour
  boundary. `TODO: verify` the endpoint convention.
- **Archive production labels are not a day-ahead series.** The day-ahead archive's
  `Forecast produced on` mixes leads of 2 and 15 days. The vendor's explanation is not
  documented (`TODO: verify`).
- **Medium-term needs per-resource selection.** Any consumer reading the silver family directly
  must group by `resource_id` before taking a "latest" view.
- **Dictionary units.** Only the day-ahead dictionaries declare MW. The medium-term dictionary
  is blank (see Units above).

## Modelling notes

`TODO`: modelling use is not yet designed. Held families must not be used point-in-time. The
eligible current day-ahead file is a candidate feature for reserve-cost and balancing-cost
models, to be joined to Elexon and NESO balancing data on service delivery date. Join on the
anchor date plus the window label, not on `timestamp_utc`, until a row-specific window recipe
exists.

## Links

- [Package page](https://www.neso.energy/data-portal/balancing-reserve-auction-requirement-forecast)
- [Day-ahead requirement dictionary](https://www.neso.energy/data-portal/balancing-reserve-auction-requirement-forecast/balancing_reserve_day_ahead_auction_requirements_forecast)
- [Medium-term requirement dictionary](https://www.neso.energy/data-portal/balancing-reserve-auction-requirement-forecast/balancing_reserve_requirements_medium_term_forecast)
- [NESO EAC Market Design Explainer](https://www.neso.energy/document/277671/download) (Appendix B, EFA blocks and service windows)
- Registry record: @../../../../Python/gridflow/src/gridflow/connectors/neso_data_portal/registry/balancing-reserve-auction-requirement-forecast.json
- Eligibility report: @../../../../Python/gridflow/docs/neso_data_portal/eligibility.md
- Batch evidence: @../../../../Python/gridflow/.planning/phases/v0.22-K-AS-1/K-AS-1-FACTS.md
- Domain: @../../../20-domain/markets/gb-balancing-mechanism.md
