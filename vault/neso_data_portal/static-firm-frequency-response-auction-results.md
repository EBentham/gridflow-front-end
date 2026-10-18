---
source: "neso_data_portal"
package: "static-firm-frequency-response-auction-results"
dataset_keys: ["sffr_auction_results_buy_orders", "sffr_auction_results_main"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-13
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Static FFR day-ahead auction results
  summary: >-
    NESO's daily Static Firm Frequency Response auction: every unit's offer for each EFA block,
    accepted or rejected, with the block's clearing price.
  facts:
    vendor: "NESO Data Portal, package `static-firm-frequency-response-auction-results`: two uploaded CSV files"
    cadence: Daily (NESO's catalogue); gridflow downloads each file whole
    grain: "Results: one row per unit, EFA date and EFA block"
    history: Delivery dates from 1 April 2023 in NESO's results file
  landscape: market
  what_it_is: >-
    NESO buys Static Firm Frequency Response in a daily auction for the six EFA blocks of each
    delivery day; block 1 starts at 23:00 the evening before. Each row is one unit's offer for one
    block: MW and price offered, accepted or rejected, MW accepted, and the block's clearing price,
    which NESO says all accepted units are paid.
  how_used:
    - Clearing price per EFA block, as revenue history for Static FFR providers.
    - "Offer stacks per block: who offered how many MW, at what price, who won."
    - "Place rows in time by `date` and `efa`: `timestamp_utc` is the date's UK midnight."
  chart:
    type: line
    silver: neso_data_portal/sffr_auction_results_main
    time: date
    value: clearing_price
    filter:
      - {column: efa, op: in, value: [1, 5]}
    dedup: {on: [date, efa], order_by: capture_written_at}
    group: efa
    group_map: {"5": efa5, "1": efa1}
    series_order: [efa5, efa1]
    aggregation: mean
    window: {start: "2023-04-01", end: "2026-10-17"}
    unit: "£/MWh"
  chart_view:
    title: Static FFR clearing price in EFA blocks 1 and 5
    caption: >-
      Silver `sffr_auction_results_main`, £/MWh as NESO labels it: the clearing price of blocks 1 and
      5 on each EFA date, one price per block in NESO's results, 1 April 2023 to 17 October 2026.
    alt: >-
      Line chart from neso_data_portal/sffr_auction_results_main: Static FFR clearing price, £/MWh,
      for EFA blocks 1 and 5 on 1,296 EFA dates, 1 April 2023 to 17 October 2026. Block 5: median
      6.50, 10 or more on 224 dates, highest 16.57 on 30 December 2023. Block 1: median 1.55, under 1
      on 445 dates, highest 5.86 on 24 October 2023, lowest 0.40 on eleven dates in November and
      December 2024. Block 5 is above block 1 on 1,291 dates; both are 0.60 on 28 April 2026, block
      5's lowest.
    x_label: EFA date of delivery, as NESO labels it
    key:
      - {series: efa5, label: Block 5, paint: clay, note: "NESO labels it 15:00 to 19:00 on the EFA date."}
      - {series: efa1, label: Block 1, paint: petrol, note: "NESO labels it 23:00 the evening before to 03:00; 1.50 from 19 April to 16 June 2025."}
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show`, then each file downloaded whole unless its
      `last_modified` is unchanged. Dates select nothing. Swap in either table's key.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=static-firm-frequency-response-auction-results"
    commands:
      - {run: gridflow ingest neso_data_portal sffr_auction_results_main --last 24h, comment: "whole file; window must end recently"}
      - {run: gridflow transform neso_data_portal sffr_auction_results_main --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: date, op: eq, value: "2026-10-08"}
        - {column: efa, op: eq, value: 2}
        - {column: unit, op: in, value: [PGFFR-5, PGFFR-9, PGHAT-1, ENDSR-2, LEV-FRU05, CITY01, PGFFR-8, PGCOV-1]}
        - {column: capture_written_at, op: ge, value: "2026-10-16T00:00:00Z"}
      order_by: [price, rank]
      columns: [date, efa, unit, status, price, clearing_price, volume, accepted_volume, rank, provider,
                technology_type, delivery_start, delivery_end, service, location]
    key: [date, unit, efa]
    caption: "Block 2, 8 October 2026: its five dearest accepted offers and three cheapest rejected."
    fields:
      date: "EFA date of delivery (NESO); block 1 starts 23:00 the evening before"
      efa: "EFA block of the date, `1` to `6` (NESO: six in 24 hours)"
      unit: "The unit offered, as NESO names it: the unit that delivers if awarded"
      status: "`Accepted` or `Rejected`, as NESO's auction algorithm cleared the offer"
      price: "Price offered, £/MWh (NESO's unit)"
      clearing_price: "The block's clearing price, £/MWh: NESO says all accepted units are paid it"
      volume: MW offered by the unit for the block (NESO's unit)
      accepted_volume: "MW accepted (NESO's unit); a rejected offer here shows `0.0`, not null"
      rank: "Random rank NESO gives each offer before the auction, for clustered offers"
      provider: The provider offering the unit, as NESO writes it
      technology_type: "Technology as NESO writes it; null where NESO leaves it blank"
      delivery_start: "Block start as NESO writes it, kept as text; NESO states no clock"
      delivery_end: Block end as NESO writes it, kept as text
      service: "Service name; `SFFR` in these rows"
      location: "A postcode, `AGG` or `Agg` (undefined by NESO), an outward code, or null"
      timestamp_utc: "UK midnight starting the EFA date's calendar day, as UTC; not the block start"
      published_at: "NESO's last-modified time for the whole file, read as UTC"
      bronze_capture_id: Path of the bronze capture the row was read from
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      `query()` reads the `_latest` view, the newest capture, filtering `date` with both ends
      included. The next cell totals each block's offers and accepted MW and keeps its one clearing
      price.
    cells:
      - |
        df = data.neso_data_portal.query("sffr_auction_results_main", "2026-10-01", "2026-10-07")
        df = df.sort_values(["date", "efa", "price", "rank"])
        df[["date", "efa", "unit", "status", "volume", "price", "clearing_price"]].head()
      - |
        blocks = (df.groupby(["date", "efa"], as_index=False)
                    .agg(offers=("unit", "size"), offered_mw=("volume", "sum"),
                         accepted_mw=("accepted_volume", "sum"), prices=("clearing_price", "nunique"),
                         clearing_price=("clearing_price", "first")))
        blocks[blocks.date == "2026-10-07"]
      - |
        blocks.clearing_price.plot(drawstyle="steps-post", color="#155A6E", figsize=(8, 3.5),
                xlabel="EFA blocks, 1 to 7 October 2026, six per EFA date",
                ylabel="clearing price, £/MWh");
    needs: a capture of the results file
    plot_alt: >-
      Step plot of the Static FFR clearing price per EFA block, £/MWh, for the 42 blocks of EFA dates
      1 to 7 October 2026. Each day repeats one shape: blocks 1, 2 and 4 from 1.52 to 2.37, block 3
      at 6.28 or 6.29, block 5 from 6.60 to 7.34 and block 6 at 9.27, or 9.41 on 3 October.
  related:
    - {dataset: neso_data_portal/static-firm-frequency-response-requirement, note: "NESO's forecast MW requirement for the same EFA blocks"}
    - {dataset: neso_data_portal/eac-auction-results, note: "NESO's daily auctions for dynamic response and reserve, by unit"}
    - {dataset: neso_data_portal/firm-frequency-response-post-tender-reports, note: "Offers and decisions in NESO's monthly Firm Frequency Response tenders"}
    - {dataset: neso_data_portal/phase-2-ffr-auction-results-summary, note: "Orders and results of NESO's Phase 2 FFR auction trial"}
  family:
    slug: static-firm-frequency-response-auction-results
    members:
      - dataset: sffr_auction_results_main
        differs: "Every offer per unit and EFA block: MW and price, accepted or rejected"
        request: "GET https://api.neso.energy/dataset/75457796-f9de-49c2-8e64-81f97131c56a/resource/76bc5d39-c39f-490b-984e-58eb8ff296ef/download/static-firm-frequency-response-auction-results_76bc5d39-c39f-490b-984e-58eb8ff296ef_patch.csv"
      - dataset: sffr_auction_results_buy_orders
        differs: "NESO's buy curve per EFA date and block: ten bands, 25 to 250 MW"
        request: "GET https://api.neso.energy/dataset/75457796-f9de-49c2-8e64-81f97131c56a/resource/f9f4b295-6de6-4379-9211-b0b2117a0c48/download/static-firm-frequency-response-buy-order_f9f4b295-6de6-4379-9211-b0b2117a0c48_patch.csv"
        held: "NESO's dictionary calls the band cells prices, with no money unit: MW on nine, one blank."
---

# Static Firm Frequency Response auction results

This package is NESO's **daily auction record for Static Firm Frequency Response (Static FFR, "SFFR")**.
The vendor describes it as the results of the daily Static FFR auction together with the buy orders
used in it (CKAN package `notes`,
@.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json). Static FFR is a
frequency-response service that NESO buys in a day-ahead auction, delivered in the six **EFA blocks**
(Electricity Forward Agreement blocks) of a delivery day. The vendor's EFA text says a day has six
EFA blocks in a 24-hour window with the first block starting at 23:00 (UK local, the evening before
the delivery date). The package carries two separate tables, one per resource:

- **Auction results** (`sffr_auction_results_main`): one row per **unit, delivery date and EFA
  block**. It gives the provider, the unit, the offered volume (MW) and price (£/MWh), whether the bid
  was accepted or rejected, the accepted volume (MW), the clearing price (£/MWh) and the unit's
  technology type and location, plus a random rank assigned before the auction runs. This is a
  **result**, not a forecast: it records what was offered and what the auction awarded for blocks that
  have been auctioned. For modelling it is the price-and-volume outcome of the Static FFR market
  (clearing price per block, who won what), to be joined later to the Static FFR requirement
  (@./static-firm-frequency-response-requirement.md) and to the balancing series.
- **Auction buy orders** (`sffr_auction_results_buy_orders`): one row per **delivery date and EFA
  block**, holding the auction's buy curve as ten columns headed `25` to `250`. **This family is
  held** (see Holds): the vendor's own dictionary does not establish the unit of the cell values, so
  gridflow does not publish them.

The package is **partly eligible**: `sffr_auction_results_main` is eligible and has no hold;
`sffr_auction_results_buy_orders` has a gridflow silver output but is **held**. It is not a
settlement-period table (no `run_type` applies and none is fabricated), and neither file has a
publication-time column. The Static FFR requirement is a separate package, documented at
@./static-firm-frequency-response-requirement.md. The same EFA structure appears in the Dynamic
requirement tables, for example @./dynamic-moderation-requirements.md.

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: EVT

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Static Firm Frequency Response Auction Buy Orders | CSV | upload | `f9f4b295-6de6-4379-9211-b0b2117a0c48` |
| Static Firm Frequency Response Auction Results | CSV | upload | `76bc5d39-c39f-490b-984e-58eb8ff296ef` |

The package has **two resources and no DOC resources**. Both are CKAN **uploads** (a file with a name,
not a datastore dump). The download links below are the URLs recorded in the capture sidecars; each
file name is replaced by NESO when it patches the upload, so the link is a record of what was fetched,
not a permanent address.

| Resource | Family | Download | Bytes | Data rows | CKAN `last_modified` of the capture |
|---|---|---|---:|---:|---|
| Static Firm Frequency Response Auction Results | `sffr_auction_results_main` | [static-firm-frequency-response-auction-results_76bc5d39-c39f-490b-984e-58eb8ff296ef_patch.csv](https://api.neso.energy/dataset/75457796-f9de-49c2-8e64-81f97131c56a/resource/76bc5d39-c39f-490b-984e-58eb8ff296ef/download/static-firm-frequency-response-auction-results_76bc5d39-c39f-490b-984e-58eb8ff296ef_patch.csv) | 31,093,666 | 229,631 | 2026-10-08T10:16:13.970875 |
| Static Firm Frequency Response Auction Buy Orders | `sffr_auction_results_buy_orders` | [static-firm-frequency-response-buy-order_f9f4b295-6de6-4379-9211-b0b2117a0c48_patch.csv](https://api.neso.energy/dataset/75457796-f9de-49c2-8e64-81f97131c56a/resource/f9f4b295-6de6-4379-9211-b0b2117a0c48/download/static-firm-frequency-response-buy-order_f9f4b295-6de6-4379-9211-b0b2117a0c48_patch.csv) | 496,593 | 7,722 | 2026-10-08T10:16:20.134250 |

Size and `last_modified` come from the capture sidecars under
`C:/gridflow-data/bronze/neso_data_portal/<family>/2026/10/08/`; rows are data rows of the body
(K-AS-2 FACTS section 2, captures A1 and A2). The two captures were written on **2026-10-08** at
11:17:37Z (results) and 11:17:33Z (buy orders). Package page:
[static-firm-frequency-response-auction-results](https://www.neso.energy/data-portal/static-firm-frequency-response-auction-results).
Resource dictionaries:
[static_firm_frequency_response_auction_results](https://www.neso.energy/data-portal/static-firm-frequency-response-auction-results/static_firm_frequency_response_auction_results)
and
[static_firm_frequency_response_auction_buy_orders](https://www.neso.energy/data-portal/static-firm-frequency-response-auction-results/static_firm_frequency_response_auction_buy_orders).

**The captures are newer than the catalogue snapshot.** The catalogue snapshot of 2026-10-06 lists
`last_modified` 2026-10-06T10:34:52 (results) and 2026-10-06T10:34:57 (buy orders). The captures
taken two days later carry 2026-10-08T10:16, so NESO re-uploaded both files in between, consistent
with the vendor's daily update frequency. gridflow uses the **capture sidecar** value as the vintage,
never the catalogue metadata.

**What the files cover.** Both files run from delivery date **2023-04-01** to **2026-10-09**, one day
after the capture date. The latest delivery date is later than the capture date, which fits the
`Day-Ahead` tag on the package (the auction for tomorrow's blocks is published today); the exact
auction and publication times are not in the vendor text read here, so `TODO: verify` the auction
timing. Results cover **1,288 delivery dates** and **7,728 delivery-date/EFA pairs** (1,288 x 6);
buy orders cover **1,287 delivery dates** and **7,722 pairs**. All 7,722 buy-order pairs also appear
in the results; the results have six more pairs (the six EFA blocks of 2023-12-02) with no buy-order
row. The two files are **separate tables, not revisions of each other**: results add unit, status and
award fields; buy orders carry the buy curve only (K-AS-2 FACTS AS-2-c).

**Bronze bodies (seat full-body scan, K-AS-2 FACTS section 2 and g5/g6).** Strict UTF-8, one header
each, no ragged row, no all-blank row. The SHA-256 of each body equals its sidecar value:
results `d50586226abb14f288c06dad695eee73cd308f006f1356a82f35b748fc32a5fd`, buy orders
`8a6f9f958d6d848c105e0fb728fe6d5a04802fd1a07a7ff5dee3daee7a4e3da5`. No `-1`, `NA` or `N/A` token,
no thousands separator, no percent suffix and no padded numeric cell occurs in either body. Strict
date and numeric casts and a second independent parse of every row (Python `csv` against Polars on
original text fragments) agreed on every cell.

## Families

### `sffr_auction_results_buy_orders`

- Kind: tabular · archetype: EVT · refresh: daily · empty allowed: no
- **Held** (unit v0.22-K-AS-2): see Holds. Rows exist in silver; the band values are not to be used or
  published until the unit is settled.

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| EFA Date | `efa_date` | date | `%Y-%m-%d` | no | — | DATE |
| EFA | `efa` | int64 | — | no | — | — |
| 25 | `c_25` | float64 | — | yes | — | MW |
| 50 | `c_50` | float64 | — | yes | — | MW |
| 75 | `c_75` | float64 | — | yes | — | MW |
| 100 | `c_100` | float64 | — | yes | — | MW |
| 125 | `c_125` | float64 | — | yes | — | MW |
| 150 | `c_150` | float64 | — | yes | — | MW |
| 175 | `c_175` | float64 | — | yes | — | MW |
| 200 | `c_200` | float64 | — | yes | — | — |
| 225 | `c_225` | float64 | — | yes | — | MW |
| 250 | `c_250` | float64 | — | yes | — | MW |

- Entity key: `efa_date`, `efa`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`efa_date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**One header epoch.** The record accepts one exact header of twelve columns: `EFA Date`, `EFA` and
the ten band headers `25`, `50`, `75`, `100`, `125`, `150`, `175`, `200`, `225`, `250`. The band
headers are bare numbers, so the engine's snake-case rule for numeric headers prefixes them: `25`
becomes `c_25`, and so on.

**What the columns mean (vendor dictionary).** From NESO's saved field info
(@.planning/research/neso-snapshots/field-info/20261008T114228Z/sffr_auction_results_buy_orders.json).

- **`EFA Date`**: "Date of delivery" (the delivery date of the block). A calendar date with no time of
  day. The dictionary example is day-first (`30/01/2023`) and its unit is `DATE`, but the served body
  is ISO (`%Y-%m-%d`), and gridflow reads it with that format.
- **`EFA`**: the Electricity Forward Agreement block number. A dimensionless block identifier, not a
  physical quantity. Observed values: `1` to `6`.
- **Band columns `25` ... `250`**: the dictionary titles each "Volume band in MWs procured on buy
  curve" and describes the cell as "the price relevant for up to this volume limit" (in the
  description field on seven bands, in the comment field on `175`, `200` and `225`). So the **header**
  is a volume threshold and the **cell** is described as a price. The dictionary lists the unit of nine
  of these columns as `MW`, which is the unit of the *threshold*, not of a price; the entry for `200`
  has an empty unit. **No monetary unit is stated for any band cell** (see Holds). Nothing is
  inferred: the cells are not relabelled MW, and the result-file price unit is not copied across.

**Units (vendor dictionary only).** `EFA` is dimensionless. The band **cell values have no
established unit** (`TODO: verify`, held). The band thresholds in the headers are MW volume limits.

**Two clocks.**

1. **Vintage (`ckan_last_modified`).** The resource is an upload with a usable CKAN timestamp, so
   `available_at` = `published_at` = the CKAN `last_modified` of the captured file (ADR-030),
   **2026-10-08T10:16:20.134250Z**, one value on all 7,722 rows. That is when the file was last
   uploaded, not when each buy curve was first available: the vendor describes the curves as
   accompanying the published auction results, which gives no per-row publication instant (NESO
   [Static FFR auction Q&A](https://www.neso.energy/document/277286/download)). Every historical
   row from 2023 onward therefore carries the same 2026 `available_at`; an as-of query before
   2026-10-08T10:16:20Z sees **no** rows. `TODO: verify` the vendor's original publication instants
   and whether past curves are amended in place at the daily refresh: a second capture (2026-10-16,
   7,770 rows to EFA date 2026-10-17) repeats all 7,722 earlier rows unchanged; one comparison only.
2. **Event time (temporal recipe `date_sp1` on `efa_date`).** `timestamp_utc` and `event_time` are
   equal on every row and are the **UK local midnight at the start of the delivery date, expressed in
   UTC** (a calendar-date storage anchor). For a summer date that is 23:00 UTC the previous evening;
   for a winter date it is 00:00 UTC. It is **not** the start of the EFA block (EFA 1 starts at 23:00
   UK local on the previous evening; EFA 2 at 03:00): the six rows of one delivery date carry the
   **same** `timestamp_utc`, so use `efa` to place a row inside the day. There are 1,287 distinct
   `timestamp_utc` values for 1,287 delivery dates. There is no issue column; `issue: none`. No
   composed date-plus-block recipe exists (RULINGS 572, 588).

**Identity and selection.**

- The record key is `(efa_date, efa)`. All 7,722 rows are distinct on it, in the body and in silver.
  The vendor guarantees no key and there is no order id or provider column: `TODO: verify` a
  vendor-guaranteed identity.
- `_latest` is `whole_capture`: the newest complete capture of the one resource. There is no
  `key_latest` and no resource partition.

**Sentinels and missing values (FACTS g5).** No sentinel exists. Every band cell in the body is
populated; the record nevertheless allows nulls on the band columns. This page publishes no band
values and no band statistics, because the family is held.

**Row counts and shape (silver, 2026-10-13).** 7,722 rows, 7,722 distinct on the entity key, 0
validation failures, 0 blank rows excluded; the planned and activated counts agree (RULINGS 731).
Silver layout: one Parquet file per capture (2026-10-08 and 2026-10-16) under
`C:/gridflow-data/silver/neso_data_portal/sffr_auction_results_buy_orders/year=2026/month=10/`; the
partition is the **capture** date. Columns (20): the twelve vendor columns, then `timestamp_utc`,
`published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`,
`source_run_id` and `dataset_version` (`1+e1`). All timestamps are tz-aware UTC. No gold view or
builder reads this family.

### `sffr_auction_results_main`

- Kind: tabular · archetype: EVT · refresh: daily · empty allowed: no
- **Eligible**, no hold.

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Date | `date` | date | `%Y-%m-%d` | no | — | ISO 8601 |
| Provider | `provider` | string | — | yes | — | — |
| Unit | `unit` | string | — | no | — | — |
| Delivery Start | `delivery_start` | string | — | yes | — | ISO-8601 |
| Delivery End | `delivery_end` | string | — | yes | — | ISO-8601 |
| EFA | `efa` | int64 | — | no | — | — |
| Service | `service` | string | — | yes | — | — |
| Status | `status` | string | — | yes | — | — |
| Volume | `volume` | float64 | — | yes | — | MW |
| Accepted Volume | `accepted_volume` | float64 | — | yes | — | MW |
| Price | `price` | float64 | — | yes | — | £/MWh |
| Clearing Price | `clearing_price` | float64 | — | yes | — | £/MWh |
| Technology Type | `technology_type` | string | — | yes | — | — |
| Location | `location` | string | — | yes | — | — |
| Rank | `rank` | int64 | — | yes | — | — |

- Entity key: `date`, `unit`, `efa`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**One header epoch.** The record accepts one exact header of fifteen columns, in the order above.

**What the columns mean (vendor dictionary).** From NESO's saved field info
(@.planning/research/neso-snapshots/field-info/20261008T114228Z/sffr_auction_results_main.json).

- **`Date`**: the EFA date of delivery (dictionary title "EFA date"). A calendar date, ISO in the
  served body.
- **`Provider`**: the provider participating in the auction. Free text, kept byte-equal.
- **`Unit`**: the unit that would deliver the service if awarded (dictionary example `AG-BBB22`).
  An identifier, stored as served with no normalisation.
- **`Delivery Start`** and **`Delivery End`**: start and end of delivery for the EFA block. In the
  body they are `YYYY-MM-DD HH:MM:SS` strings with no offset (all rows of both columns match that
  shape), for example a delivery date 2023-04-01 block 1 reads `2023-03-31 23:00:00` to
  `2023-04-01 03:00:00`. The dictionary example is day-first (`30/01/2023 07:00`) and its unit is
  `ISO-8601`; neither describes the served shape. They are **raw strings** in silver (see Two clocks).
- **`EFA`**: the block number, 1 to 6. A dimensionless identifier.
- **`Service`**: the service name. The only value observed is `SFFR`.
- **`Status`**: whether the bid was accepted or rejected as the auction algorithm cleared. Observed
  values: `Accepted` and `Rejected`.
- **`Volume`**: the volume offered per unit (dictionary title "Offered Volume"), MW.
- **`Accepted Volume`**: the dictionary text repeats the offered-volume wording, but the title and the
  data are the awarded volume, MW; see Sentinels for the zeros.
- **`Price`**: the price offered per unit (dictionary title "Offered Price"), £/MWh.
- **`Clearing Price`**: the price paid for accepted units for the EFA (dictionary title "Clearing
  Price for given EFA"), £/MWh.
- **`Technology Type`**: free text (dictionary example `Battery`). Blank on 275 rows.
- **`Location`**: the dictionary says the postcode of where the unit is located; kept as served.
  Blank on 275 rows. Not always a postcode: the 2026-10-16 capture has `AGG` on 123,664 rows, `Agg`
  on 3,423 and the outward code `BN44` on 251; the dictionary does not define `AGG`.
- **`Rank`**: the dictionary says every bid gets a random rank before the auction runs, to order
  clustered bids. A dimensionless ordinal, not a volume or a price. Observed values: 1 to 42.

**Units (vendor dictionary only).** `Volume` and `Accepted Volume` are **MW**; `Price` and
`Clearing Price` are **£/MWh** (the vendor's spelling is kept, and no convention is borrowed from the
other reserve services); `EFA` and `Rank` are dimensionless. Nothing is converted or rescaled. Volumes
are MW (power) and no energy (MWh) denomination is stated for them: do not multiply by the block
length to get MWh without a vendor statement.

**Two clocks.**

1. **Vintage (`ckan_last_modified`).** The resource is an upload with a usable CKAN timestamp, so
   `available_at` = `published_at` = the CKAN `last_modified` of the captured file (ADR-030),
   **2026-10-08T10:16:13.970875Z**, one value on all 229,631 rows. That is when the file was last
   uploaded, not when each result was first published: the file has no issue or publication column and
   the auction timing must not be turned into a per-row publication time. Because the file is a
   multi-year history uploaded as a whole, **every row back to April 2023 carries the same 2026
   `available_at`**: an as-of query before 2026-10-08T10:16:13Z sees **no** rows, and a point-in-time
   backtest cannot rely on this table to say when a historical result became known. These are event
   records, so the forward-target rule for forecasts (RULINGS 529) does not apply to them. `TODO:
   verify` the vendor's original publication moment per result and whether past rows are amended in
   place at the daily refresh: a second capture (2026-10-16, `last_modified`
   2026-10-16T10:46:09.594804, 231,369 rows to date 2026-10-17) repeats all 229,631 earlier rows with
   every vendor column unchanged; one comparison only.
2. **Event time (temporal recipe `date_sp1` on `date`).** `timestamp_utc` and `event_time` are equal
   on every row and are the **UK local midnight at the start of the delivery date, expressed in
   UTC**: for a summer date it is 23:00 UTC the previous evening (delivery date 2026-07-01 gives
   `2026-06-30T23:00:00Z`) and for a winter date 00:00 UTC (2026-01-15 gives `2026-01-15T00:00:00Z`).
   It is a **calendar-date storage anchor**, not the start of the block: there are 1,288 distinct
   `timestamp_utc` values for 1,288 delivery dates, so every unit and block row of one delivery date
   carries the **same** value. Place a row inside the day with `efa`, and with the raw
   `delivery_start` and `delivery_end` strings.

   The delivery strings are **local EFA wall-clock labels**: every `delivery_start` and `delivery_end`
   matches the local clock times of the six EFA blocks (EFA 1 from 23:00 on the previous date to 03:00,
   then 03:00-07:00, 07:00-11:00, 11:00-15:00, 15:00-19:00, 19:00-23:00; K-AS-1 FACTS, reused in
   K-AS-2 FACTS AS-2-c), with zero mismatches, and the naive end minus start is 14,400 seconds on
   every row. That is a measured correspondence, **not** a vendor declaration that the cells are UK
   local time or what the endpoint closure is, and it does not prove a 4-hour elapsed UTC duration on
   a clock-change day. gridflow therefore keeps them raw and applies no timezone conversion (RULINGS
   720, 727). `TODO: verify` the clock and endpoint closure of the two timestamp columns.

**Identity and selection.**

- The record key is `(date, unit, efa)`. All 229,631 rows are distinct on it, in the body and in
  silver. `(Unit, Delivery Start)` and `(Unit, Delivery End)` also pass the duplicate guard; the
  date/unit/block key is used because it states the documented result grain without relying on the
  unresolved timestamp typing. There is no order id, so a unit with several bids in one block would
  collide; none occurs in this capture. The vendor guarantees no key: `TODO: verify` a vendor
  identity statement.
- `_latest` is `whole_capture`: the newest complete capture. There is no `key_latest` and no resource
  partition.

**Sentinels and missing values (FACTS g5).** No sentinel exists and no null token is declared. The
**36,999 zero `Accepted Volume` cells are real results, not missing values**: every `Rejected` row has
zero accepted volume and every `Accepted` row has a non-zero value, so zeros match the status exactly
and must not be nulled or dropped. The longest consecutive zero run in file order is 25 rows. No other
numeric column has a zero. The only blanks are `Technology Type` and `Location` (275 rows each); they
stay null and must not be read as a technology or a location. Provider, rank, delivery start and
delivery end are never null in this capture.

**Row counts and shape (silver, 2026-10-13).**

| Resource | Rows | Distinct on entity key |
|---|---:|---:|
| `76bc5d39-c39f-490b-984e-58eb8ff296ef` | 229,631 | 229,631 |

The planned and activated counts agree (229,631), with 0 validation failures and 0 blank rows
excluded (RULINGS 731). Observed in this capture (single-capture measurements, not vendor-stated
ranges):

| Measure | Value |
|---|---|
| Delivery dates / date-EFA pairs | 1,288 / 7,728 |
| Distinct `unit` values | 57 |
| `Status` | `Accepted` 192,632 rows; `Rejected` 36,999 rows |
| `Volume` | 0.2 to 39 MW |
| `Accepted Volume` | 0 to 39 MW |
| `Price` | 0.01 to 100 £/MWh |
| `Clearing Price` | 0.4 to 16.57 £/MWh |

Silver layout: one Parquet file per capture (2026-10-08 and 2026-10-16) under
`C:/gridflow-data/silver/neso_data_portal/sffr_auction_results_main/year=2026/month=10/`; the
partition is the **capture** date. Columns (23): the fifteen vendor columns, then `timestamp_utc`,
`published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`,
`source_run_id` and `dataset_version` (`1+e1`). All timestamps are tz-aware UTC. There is no
`resource_id` column, because the entity key does not include it. No gold view or builder reads this
family.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Daily

The vendor says the package is updated daily. The two captures taken on 2026-10-08 are newer than
the 2026-10-06 catalogue snapshot, which agrees with a refresh at least every couple of days, but
two captures per resource exist (2026-10-08 and 2026-10-16), so the real rhythm is unmeasured. Each
2026-10-16 file is again the whole history from delivery date 2023-04-01 (the file names end
`_patch.csv`), with every earlier row unchanged. `TODO: verify` by comparing
later complete captures with the hash-pinned bodies above.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `sffr_auction_results_buy_orders`: held: TODO: SFFR-BUY-CURVE-CELL-UNITS — the dictionary labels the band columns MW but describes their cells as prices (the `200` entry has no unit); what monetary unit are the cells? (unit v0.22-K-AS-2)

`sffr_auction_results_main` has **no hold**: it was specified as eligible and activated as such
(RULINGS 724, 727, 730, 731).

**Why the buy orders are held.** The band headers are volume limits, and the dictionary describes
each cell as the price relevant up to that volume limit. But the `MW` unit the dictionary attaches to
nine of the ten band columns is the unit of the threshold, and the `200` entry has no unit at all, so
the dictionary never states the monetary unit of the price cells (RULINGS 707 hold treatment; K-AS-2
FACTS section 4.10). The question covers **all ten band columns**, not only `200`. It is settled only
by corrected resource dictionary entries or vendor guidance that maps these CSV cells to a monetary
unit. It is not settled by copying the £/MWh unit of the results file, by calling the cells MW, or by
reading a number range. Consequence: the silver rows, schema and row count are kept and the family is
reconciled, but **no band value, sample row or value statistic is published on this page or in any
gridflow output**, and the family must not feed a model or a gold view until the hold clears.

**Known issues and open questions.**

- **Same `available_at` for all history.** Both files are whole-history uploads, so the vintage is
  the 2026-10-08 upload time for every row from 2023-04-01. Point-in-time use of these tables for a
  past date is unsafe. `TODO: verify` original publication instants.
- **Anchor is not the block start.** `timestamp_utc` is the UK-midnight date anchor, identical for
  all rows of a delivery date. EFA 1 begins the evening before (23:00 UK local). Never read
  `timestamp_utc` as the start of a block.
- **Delivery labels are strings.** `delivery_start` and `delivery_end` are naive local-looking
  strings (`YYYY-MM-DD HH:MM:SS`), raw by design. Convert at the consumer, by `date` and `efa`, and
  not by parsing the label alone. Clock and endpoint closure are `TODO: verify`
  (SFFR-RESULT-TIMESTAMP-CLOCK / ENDPOINT). On clock-change dates (23- and 25-hour days) the labels
  and the explicit `efa` are the only placement; `TODO: verify` how the labels and the 14,400-second
  naive durations behave on the autumn and spring change dates.
- **Zero accepted volume is a result.** See Sentinels. Do not treat it as missing.
- **One clearing price per block, not always an accepted offer's price.** In the 2026-10-16 capture
  each of the 7,776 date-EFA blocks carries one `Clearing Price` and at least one `Accepted` row; in
  122 blocks the price is above every accepted offer, and 963 `Rejected` offers equal it. `Rank` does
  not order those ties consistently. NESO states only "Price paid for all accepted unit for all
  awarded contracts"; `TODO: verify` how the price is set.
- **No order id.** The grain is unit x date x block. A second bid from the same unit in the same
  block would break the key; none occurs in this capture.
- **Dictionary versus body.** The dictionary examples show day-first slash dates and ISO-8601 unit
  labels; the body uses ISO dates and `YYYY-MM-DD HH:MM:SS` delivery strings. The dictionary text for
  `Accepted Volume` repeats the offered-volume wording. The body and the titles are followed.
- **Overlap with buy orders.** The two files share the date/EFA grain (7,722 common pairs) but are
  not interchangeable; no cross-family adjudication follows from the overlap.
- **Empty publication.** Both families allow no empty capture. `TODO: verify` (EMPTY-PUBLICATION)
  what a genuine empty publication looks like if one is ever served.

**Activation (2026-10-13, master `fccbdeb`, PR #113).** The ancillary-services batch 2 (twelve
families in six package registries) merged triple-green (RULINGS 730): CI green, the Sol diff review
approved on the first pass with no findings, and verification passed. The families were transformed
from the 2026-10-08 captures with `--start/--end 2026-10-08`. There was no prior silver, so nothing
was overwritten and no snapshot was taken (RULINGS 731). The activation total across the eleven
families with a record is 241,160 rows, each family equal to its planned count: **229,631** for
`sffr_auction_results_main` and **7,722** for `sffr_auction_results_buy_orders`. The batch-wide
reconcile `--all --cutoff 2026-10-12` exited 0 with 0 gaps over 170 families (47 adjudicated, 0 stale).
The batch has 9 eligible families (233,437 rows) and 2 held ones (this package's buy orders and the
SFFR important-notifications family); `contract_transfer_obligation` has no record. Gridflow
`@.planning/v0.22-RESULTS.md` section AS-2 holds the receipt.

**Related.** The Static FFR requirement is @./static-firm-frequency-response-requirement.md; the SFFR
important notifications are in @./ancillary-services-important-industry-notifications.md; the Dynamic
requirement tables use the same EFA blocks: @./dynamic-moderation-requirements.md and
@./dynamic-regulation-requirements.md.
