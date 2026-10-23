---
source: "neso_data_portal"
package: "day-ahead-power-exchange-prices-nordpool"
dataset_key: "nordpool_da_prices"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-09
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: GB day-ahead prices by hour
  summary: >-
    Nord Pool's GB day-ahead auction price for each delivery hour, in £/MWh, as NESO republishes
    it in one Data Portal file.
  facts:
    vendor: "NESO Data Portal, package `day-ahead-power-exchange-prices-nordpool`: file N2EX GB Day-Ahead Price"
    cadence: "Daily in NESO's catalogue"
    grain: One row per delivery date and one-hour GMT period
  landscape: market
  what_it_is: >-
    Nord Pool's GB day-ahead auction price for each delivery hour, in £/MWh, as NESO republishes
    it: in NESO's words, "the Day-Ahead price data published by Nord Pool each day for GB". NESO
    labels each hour by delivery date and a one-hour GMT period. gridflow keeps both labels as
    sent and builds no delivery time from them.
  how_used:
    - An hourly GB day-ahead price history for price models and backtests.
    - The GB side of a spread against ENTSO-E's European day-ahead prices.
    - Compared with Elexon's half-hourly market index price, a different product.
  chart:
    type: line
    silver: neso_data_portal/nordpool_da_prices
    time: date
    value: price
    dedup: {"on": [date, delivery_period], order_by: capture_written_at}
    aggregation: mean
    window: {start: "2021-09-21", end: "2026-10-16"}
    max_points: 2000
    unit: £/MWh
  chart_view:
    title: Daily mean price, September 2021 to October 2026
    caption: >-
      Silver `neso_data_portal/nordpool_da_prices`, £/MWh: the plain mean of the 24 hourly prices
      labelled with each date, 21 September 2021 to 16 October 2026, from the file captured
      16 October 2026. Each date carries 24 one-hour labels, which NESO gives as GMT.
    alt: >-
      Line chart of the daily mean of NESO's hourly Nord Pool GB day-ahead prices in £/MWh from
      neso_data_portal/nordpool_da_prices, 21 September 2021 to 16 October 2026. Every day above
      300 falls between 15 October 2021 and 16 December 2022; the peak is 574.82 on 26 August 2022,
      then 570.94 on 12 December 2022. Yearly medians after that are 90 in 2023, 73 in 2024, 82 in
      2025 and 105 in 2026 to 16 October. The lowest day is 0.39, on 4 October 2025.
    x_label: date as NESO labels it, GMT
    y_min: -25
    key:
      - {series: price, label: Daily mean price, codes: price, paint: petrol, note: "Highest £574.82/MWh on 26 August 2022; lowest £0.39/MWh on 4 October 2025."}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then the whole datastore dump of the file, kept
      only if its body changed. Dates select nothing.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=day-ahead-power-exchange-prices-nordpool"
      - "GET https://api.neso.energy/datastore/dump/4f27eea5-7038-4f73-9740-e3e4ad47c26a"
    commands:
      - {run: gridflow ingest neso_data_portal nordpool_da_prices --last 24h, comment: "whole file; window must end recently"}
      - {run: gridflow transform neso_data_portal nordpool_da_prices --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: date, op: eq, value: "2025-10-26"}
        - {column: delivery_period, op: in, value: ["00:00 - 01:00", "01:00 - 02:00", "02:00 - 03:00", "03:00 - 04:00", "04:00 - 05:00", "05:00 - 06:00", "06:00 - 07:00", "07:00 - 08:00"]}
      dedup: {"on": [date, delivery_period], order_by: capture_written_at}
      order_by: [delivery_period]
      columns: [date, delivery_period, price, timestamp_utc, published_at]
    key: [date, delivery_period]
    caption: "26 October 2025, UK clocks back: one label per GMT hour; five prices below zero."
    fields:
      date: "Delivery date as NESO writes it; with `delivery_period`, the key"
      delivery_period: "The delivery hour in GMT, as NESO writes it: `HH:MM - HH:MM`"
      price: "Nord Pool's day-ahead auction price for the hour, £/MWh"
      timestamp_utc: When gridflow captured the file, UTC; not the delivery hour
      published_at: "Null: gridflow keeps no publication time for a NESO datastore file"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      `query()` filters `timestamp_utc`, here the capture time, so `data.sql` reads the `_latest`
      view, the newest capture, in UTC; then hours per date and each GMT hour's yearly mean.
    cells:
      - |
        df = data.sql("""
            SELECT date, delivery_period, price,
                   timestamp_utc AT TIME ZONE 'UTC' AS captured_utc
            FROM silver_neso_data_portal_nordpool_da_prices_latest
            ORDER BY date, delivery_period""")
        df[df.date.astype(str) == "2025-10-26"].head(8)
      - df.groupby("date").size().value_counts().rename("dates").rename_axis("hours labelled")
      - |
        yr = df[df.date.astype(str).between("2025-10-01", "2026-09-30")]
        prof = yr.groupby("delivery_period").price.mean()
        prof.index = prof.index.str[:5]
        ax = prof.plot.bar(figsize=(8, 3.5), color="#155A6E", width=0.8,
                           xlabel="hour starting, GMT", ylabel="£/MWh, mean over the year");
    needs: a capture of NESO's Nord Pool price file
    plot_alt: >-
      Bar plot of the mean GB day-ahead price in £/MWh for each hour, by NESO's GMT label, 1
      October 2025 to 30 September 2026. A morning rise peaks at 103 for 06:00, the midday low is
      78 for 12:00 and 13:00, and the evening peak is 130 for 18:00, easing to 91 for 23:00.
  related:
    - {dataset: elexon/mid, note: "Elexon's half-hourly market index price: a different product, read side by side"}
    - {dataset: elexon/system_prices, note: "GB imbalance prices, settled after delivery, against the day-ahead price"}
    - {dataset: entsoe/day_ahead_prices, note: "ENTSO-E's European day-ahead prices, the far side of a GB spread"}
---

# Day-Ahead Power Exchange prices (Nord Pool)

Hourly **GB day-ahead auction prices from the N2EX market**, published on the NESO Data Portal
under the Nord Pool name. The resource is titled "N2EX GB Day-Ahead Price" and its description
specifies Nord Pool's GB day-ahead prices. Each row is one delivery hour on one date and carries
one price. The price is in **GBP/MWh**. The package supplies the energy denominator and the
resource dictionary specifies GBP and the auction-period price
([package page](https://www.neso.energy/data-portal/day-ahead-power-exchange-prices-nordpool),
[resource dictionary](https://www.neso.energy/data-portal/day-ahead-power-exchange-prices-nordpool/_n2ex_gb_day-ahead_price)).
Nord Pool's own GB product specification corroborates hourly N2EX contracts priced in GBP/MWh
([product specification](https://www.nordpoolgroup.com/4ab576/globalassets/download-center/rules-and-regulations/product-specifications-gb-market.pdf)).
The file has no area column and no evidence of any bidding area other than GB (gridflow
`@.planning/phases/v0.22-K-IC-2/K-IC-2-FACTS.md` §3 IC2-2).

Use: this is a day-ahead price history for GB. A price model can use it as a target or as a
feature for forward power prices, as a reference for interconnector spreads against the continental
day-ahead markets, and as a cross-check on the Elexon market index prices. Related pages:
@../../elexon/datasets/mid.md (Elexon market index prices),
@../../entsoe/datasets/day_ahead_prices.md (ENTSO-E day-ahead prices, which has no GB rows locally,
see Cross-checks below) and the NESO interconnector pages @eleclink.md, @ifa.md, @ifa2.md,
@nemolink.md, @nsl.md, @viking.md and @brit-ned.md. Domain notes:
@../../../20-domain/markets/gb-wholesale-electricity.md and
@../../../20-domain/markets/eu-day-ahead-electricity.md.

**Read this before using `timestamp_utc`.** For this family `timestamp_utc` is **the capture
time**, not the delivery hour. The temporal recipe is `none`, because no recipe in the engine can
yet compose a UTC date and an hourly interval label into one instant (RULINGS 572, 576). The
delivery instant is **`date` plus the start hour of `delivery_period`, in UTC**. For example, a row
with `date` 2024-03-31 and `delivery_period` `13:00 - 14:00` is the hour starting 2024-03-31
13:00 UTC and ending 14:00 UTC. A consumer must build that instant itself and must never read
`timestamp_utc` as the delivery hour. Until a composition recipe exists, the raw `date` and
`delivery_period` are the only carriers of the delivery time.

The family is **eligible** (not held). There is no licence hold: the package has no third-party
carve-out in the NESO Open Data Licence (RULINGS 460, 477), and the series is historical prices,
not a forecast whose past values could change.

- Publisher group: Trading
- Registry group: trade-data · archetype: SER

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| N2EX GB Day-Ahead Price | CSV | dump | `4f27eea5-7038-4f73-9740-e3e4ad47c26a` |

The package has one resource, and it is SILVER. It has no DOC resources, so there is no
methodology document and no `_files` family. Package id `8e3cc601-1fab-4325-82ca-d8a0daeddf73`.

- **N2EX GB Day-Ahead Price** → `nordpool_da_prices`.
  Download (datastore dump): [4f27eea5-7038-4f73-9740-e3e4ad47c26a](https://api.neso.energy/datastore/dump/4f27eea5-7038-4f73-9740-e3e4ad47c26a).
  The catalogue name carries a leading space (` N2EX GB Day-Ahead Price`); the table above shows
  it trimmed.
  Captured: `raw_20261008T111421Z_4f27eea5-7038-4f73-9740-e3e4ad47c26a_9cf3a923.csv`,
  1,568,234 bytes, 44,256 rows, one capture made on 2026-10-08, one header epoch. The datastore
  response was a single page. A second capture,
  `raw_20261016T204205Z_4f27eea5-7038-4f73-9740-e3e4ad47c26a_13ef1d85.csv` (1,575,939 bytes,
  44,472 rows, sidecar `written_at` 2026-10-16T20:42:05.239349Z), holds the first capture's
  44,256 hours with identical prices plus 216 later ones, through `2026-10-17` `21:00 - 22:00`.
  Its sidecar still records CKAN `last_modified` 2026-09-21T12:38:33.467657 (checked 2026-10-23).

## Families

### `nordpool_da_prices`

- Kind: tabular · archetype: SER · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Date | `date` | date | `%Y-%m-%d` | yes | — | — |
| Delivery Period | `delivery_period` | string | — | yes | — | — |
| Price | `price` | float64 | — | yes | — | GBP |

- Entity key: `date`, `delivery_period`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

**The two clocks for this family:**

1. **Vintage (`capture_fallback`, not `ckan_last_modified`).** The resource is a datastore dump.
   Under ADR-035 a family holding a datastore resource takes `capture_fallback` and nothing else
   (gridflow `@docs/DECISION_LOG/ADR-035-neso-datastore-dump-leg.md`). So `published_at` is
   **null** on every row and `available_at` = `capture_written_at`, the sidecar `written_at`:
   `2026-10-08T11:14:21.282381Z`. Checked on all 44,256 silver rows on 2026-10-09: one distinct
   value, equal to `capture_written_at`. The 16 October capture carries
   `2026-10-16T20:42:05.239349Z` on all its 44,472 rows (checked 2026-10-23). The sidecar does
   record a CKAN `last_modified` (`2026-09-21T12:38:33.467657`, no offset), and gridflow does not
   use it as the vintage. It precedes rows dated up to 2026-10-08 (2026-10-17 in the 16 October
   capture), so it does not track the body's content. It is not a row
   availability instant, and neither is any auction schedule. The vintage says only when gridflow
   first held the values. It is not when NESO or Nord Pool published them.
2. **Event time (`none`).** The temporal recipe is `none`, so `timestamp_utc` = `event_time` =
   the **capture time**: `2026-10-08T11:14:21.282381Z` in the 8 October capture and
   `2026-10-16T20:42:05.239349Z` in the 16 October one. Both columns equal it on every row of each
   capture (checked 2026-10-23). **It
   is not the delivery hour.** The delivery time is carried only by the raw `date` and
   `delivery_period`. See the sentence at the top of this page for how to build the delivery
   instant.

**Delivery-period labels.** `delivery_period` is a string of the form `HH:MM - HH:MM`. The body
has **24 distinct labels** and every one spans exactly one hour, so the resolution is hourly. No
half-hour or quarter-hour labels occur. The left endpoint is the period start and the right
endpoint its end, so `23:00 - 00:00` ends on the following civil date. The labels are GMT, which
the vendor dictionary states, and the measurements agree with it (FACTS §3 IC2-2, C-CSV, C-FINAL):

- In the 8 October capture, under the mapping `date` + left endpoint as UTC, all 44,255 steps
  between consecutive rows are exactly 3,600 seconds. The earliest start is 2021-09-20T22:00:00Z
  and the latest is 2026-10-08T21:00:00Z. In the 16 October capture all 44,471 steps are 3,600
  seconds and the latest start is 2026-10-17T21:00:00Z (checked 2026-10-23).
- The 8 October body has 1,845 distinct dates. 1,843 of them have 24 rows. The boundary dates are
  partial: 2021-09-20 has 2 rows (22:00 and 23:00) and 2026-10-08 has 22 rows (00:00 to 21:00).
  The 16 October body has 1,854 dates, 1,852 with 24 rows; 2021-09-20 has 2 rows and 2026-10-17
  has 22 (00:00 to 21:00).
- **DST check.** Each inspected transition date has 24 distinct intervals and no fold marker, in
  both spring and autumn: 2021-10-31, 2022-03-27, 2022-10-30, 2023-03-26, 2023-10-29, 2024-03-31,
  2024-10-27, 2025-03-30, 2025-10-26 and 2026-03-29. A UK-local day would have 23 or 25 hours on
  those dates. Together with the GMT dictionary and the continuous hourly sequence, this supports
  UTC intervals rather than a UK-local or CET/CEST clock. The date label is therefore a UTC civil
  date and the spring and autumn change days are not special cases.
- Nord Pool's own contract-hour schedule uses EFA numbering. That numbering is not the NESO
  label and must not be substituted for it.

Of the 8 October capture's 44,256 rows, 44,246 have a delivery start before the capture time and **10 after** (the
10 hours from 12:00 to 21:00 UTC on 2026-10-08, against a capture at 11:14 UTC). That is expected
for a day-ahead series captured during the delivery day. Because not every target follows the
vintage, the forward-target rule (RULINGS 529) does not apply to this family and was not needed:
the family is eligible as a price history with capture-time availability.

**Identity.** `(date, delivery_period)` is unique over the full body, with zero collisions and zero
exact duplicate rows (also checked on silver: 44,256 distinct pairs in the 8 October capture and
44,472 in the 16 October one). The frozen catalogue
declares no primary or unique key for this package, so the key is a capture guard and `_latest` is
`whole_capture`: the newest capture wins as a whole. `TODO: verify` the vendor's primary-key or
revision guarantee, and whether a later publication can restate a past hour's price.

**Units (vendor dictionary only, read 2026-10-08, linked above).** `price` is **GBP/MWh**: the
dictionary gives GBP and the auction-period price, and the package gives the energy denominator.
The silver "Vendor unit" cell shows only the dictionary's currency, `GBP`. `date` and
`delivery_period` are labels with no unit.

**Sentinels and missing values (FACTS g5).** No null-token map is declared. Full-body checks found
no blank price, no literal `NA` and no literal `N/A`, and silver has no null `price`. The values
include **negative prices** (591 observations), **numeric zeros** (63 observations, the longest
run 3 consecutive hours) and **two rows with the price `-1.000000`**, at CSV lines 19,901
(2023-12-29, `01:00 - 02:00`) and 22,301 (2024-04-07, `01:00 - 02:00`). The dictionary describes a
null price for the case where no price was set or trading did not occur. It does not define zero
or -1 as a sentinel. **There is no sentinel in this series.** Negative prices, zeros and the two
`-1.000000` rows are real values, stay numeric and are never converted to null. `TODO: verify`
with NESO that `-1.000000` is a genuine auction price on those two hours.

**Value range (both captures, silver):** the price runs from -54.17 to 2,000.05 GBP/MWh. 1,845
dates in the 8 October capture (1,854 in the 16 October one) and 24 labels give the coverage above.
The 591 negatives and 63 zeros are the same in both captures.

**Cross-checks (FACTS §3, C-XCHECK).** These comparisons do not establish identical products:

- ENTSO-E day-ahead price silver has **no GB-area rows**. Its areas are Ireland, Germany, Belgium,
  France and the Netherlands, in EUR, so there is no GB counterpart.
- Elexon market index data (`mid`) supplies two provider identifiers, kept as-is. Joining at the
  nominal GMT hour start gives, for `APXMIDP`, 43,679 joined rows with 6 exact price matches, a
  mean absolute difference of about 18.0 GBP/MWh and a Pearson correlation of 0.913. Averaging
  the two half-hours first (an analysis step, not a vendor definition) gives 43,671 complete hours
  and a mean absolute difference of about 17.3. Shifting the join by one hour in either direction
  gave larger differences (about 20.7 and 19.1), which supports the nominal-start mapping.
- `N2EXMIDP` has 43,508 joined rows, 63 exact matches and a correlation of 0.015. That series is
  almost all zero in the local data (87,781 of 87,977 rows are zero-price), so it cannot validate
  the auction values merely because its identifier contains N2EX.

**Activation (2026-10-09, master `2d72b83`, PR #96).** Cutoff 2026-10-08, no prior silver, so
nothing was overwritten. Rows: `nordpool_da_prices` **44,256**, equal to the planned count. The
family holds one Parquet file under `year=2026/month=10`. It needed no adjudication. The full
`reconcile --all --cutoff 2026-10-08` run covered every family and reported no gap for this one
(its one open gap, in `brit_ned`, is unrelated; see @brit-ned.md). Sources: gridflow
`@.planning/v0.22-RESULTS.md` section IC-2; RULINGS 579, 580.

Silver columns beyond the vendor columns: `timestamp_utc`, `published_at`, `bronze_capture_id`,
`capture_written_at`, `event_time`, `available_at`, `source_run_id` and `dataset_version`. All
timestamps are tz-aware UTC. `dataset_version` `1+e1` = record version 1, epoch 1.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Daily

"Daily" is the vendor's statement. The recorded CKAN `last_modified` (2026-09-21) is earlier than
the newest delivery date in either body (2026-10-08, then 2026-10-17 in the 16 October capture,
whose sidecar still records it), so it is not a reliable indicator of when
rows were appended. `TODO: verify` how and when NESO appends each day's prices and whether past
rows are ever rewritten. gridflow's refresh captures one state of the dump per run, so any rewrite
between runs is lost. The dated silver captures are therefore a sample of the vendor's state, not
a full revision history. Two captures exist (2026-10-08 and 2026-10-16; see Files). No scheduled gridflow refresh exists
yet. Captures are on demand. `TODO: verify` immutable historical public availability timestamps
if an as-of use before the capture is ever required. The series carries capture-time availability
only (ADR-035; RULINGS 477).

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above. The package has no
third-party carve-out (RULINGS 460, 477).

## Holds

- none
