---
source: "neso_data_portal"
package: "eac-br-auction-results"
dataset_keys: ["eac_br_results_buy_orders", "eac_br_results_by_unit", "eac_br_results_sell_orders", "eac_br_results_summary"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-13
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Balancing Reserve auction results
  summary: >-
    NESO's daily Balancing Reserve auctions on its EAC platform: cleared MW and price per
    half-hour window, winning units, and every order.
  facts:
    vendor: "NESO Data Portal, package `eac-br-auction-results`: four datastore tables"
    cadence: One auction per delivery day; later auctions are in NESO's newer EAC package
    grain: "Summary: one row per auction, product (`PBR` or `NBR`) and half-hour window"
    history: "Delivery windows `2024-03-12T23:00:00` to `2025-10-29T22:30:00` in NESO's archive dump"
  landscape: market
  what_it_is: >-
    NESO buys Balancing Reserve, `PBR` and `NBR` (read as positive and negative reserve on BM units),
    in one auction per delivery day of half-hour windows. The summary gives cleared MW and clearing
    price. Across NESO's archive, buy, sell and by-unit executed MW each sum to the summary's: never
    add two tables. Window times are text with no stated clock.
  how_used:
    - Clearing price per window and product, as the target of a reserve-price model.
    - "Sell-order bid stacks per window: MW offered against price limit, with the outcome."
    - "Who holds the reserve: MW per BM unit, participant and technology, per window."
  chart:
    type: line
    silver: neso_data_portal/eac_br_results_summary
    time: delivery_start
    time_text: {format: "%Y-%m-%dT%H:%M:%S", day: {zone: Europe/London, starts: -1}}
    value: clearing_price
    filter:
      - {column: cleared_volume, op: gt, value: 0}
    group: auction_product
    group_map: {PBR: pbr, NBR: nbr}
    series_order: [pbr, nbr]
    aggregation: mean
    window: {start: "2024-03-13", end: "2025-10-29"}
    unit: "£/MW/h"
  chart_view:
    title: Mean Balancing Reserve clearing price, March 2024 to October 2025
    caption: >-
      Silver `neso_data_portal/eac_br_results_summary`, £/MW/h: each day's unweighted mean over
      cleared half-hours; NESO records £0 where nothing cleared, so a day with no clears is a gap. Days
      run 23:00 to 23:00 UK time (inferred), reading NESO's clockless text as UTC.
    alt: >-
      Line chart from neso_data_portal/eac_br_results_summary of the daily mean Balancing Reserve
      clearing price over cleared half-hours, in £/MW/h, for delivery days 13 March 2024 to 29
      October 2025. Positive (PBR) clears every day, mostly 2 to 10, lowest at 1.47
      on 4 July 2024, and spikes in winter: 40.47 on 13 December 2024 and 51.54 on 21 January 2025,
      the highest. Negative (NBR) stays at or below 1.55, reached in April 2024, with 11 gap days
      before December; from 4 December 2024 it cleared on two days only, both at 0.
    x_label: delivery day, 23:00 to 23:00 UK (inferred)
    key:
      - {series: pbr, label: Positive (PBR), codes: PBR, paint: petrol}
      - {series: nbr, label: Negative (NBR), codes: NBR, paint: clay, note: "Gaps are days when no negative reserve cleared; from December 2024 almost every day."}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then the table's whole datastore dump; run one line
      per table. Frozen: re-fetched at most weekly, unchanged bodies not stored again.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=eac-br-auction-results"
    commands:
      - {run: gridflow pipeline neso_data_portal eac_br_results_summary --last 24h, comment: "summary to bronze, then silver"}
      - {run: gridflow pipeline neso_data_portal eac_br_results_by_unit --last 24h, comment: "by-unit table, read by the notebook"}
  record:
    select:
      filter:
        - {column: auction_id, op: eq, value: "947"}
        - {column: delivery_start, op: in, value: ["2025-01-21T16:00:00", "2025-01-21T16:30:00", "2025-01-21T17:00:00", "2025-01-21T17:30:00"]}
      order_by: [delivery_start, auction_product]
      columns: [delivery_start, auction_product, cleared_volume, clearing_price, auction_id, delivery_end, service_type]
    key: [auction_id, auction_product, delivery_start]
    caption: "Four evening windows of auction 947 (21 January 2025), both products, as NESO wrote them."
    fields:
      delivery_start: "Window start as NESO wrote it, kept as text; NESO states no clock"
      auction_product: "`PBR` or `NBR`, read as positive or negative reserve; NESO's dictionary lists only codes"
      cleared_volume: MW bought in the window (NESO's unit); 0 when nothing cleared
      clearing_price: "Clearing price, £/MW/h (NESO's unit); NESO records 0 where nothing cleared"
      auction_id: "NESO's auction number, kept as text; one auction per delivery day"
      delivery_end: Window end as NESO wrote it, kept as text
      service_type: "NESO's service name, `Balancing Reserve`"
      timestamp_utc: gridflow's capture time, UTC; not the delivery window
      published_at: "Null: when NESO first published each result is unknown"
      bronze_capture_id: Path of the bronze capture the row was read from
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      Reads with `data.sql` from the `_latest` views (newest capture): `query()` would filter on
      `timestamp_utc`, the capture time. The first query averages price over cleared windows, as the
      chart does; the second checks by-unit MW.
    cells:
      - |
        data.sql("""
            SELECT auction_id, auction_product,
                   COUNT(*) FILTER (WHERE cleared_volume > 0) AS windows_cleared,
                   ROUND(AVG(cleared_volume), 2) AS mean_mw_per_window,
                   ROUND(AVG(clearing_price) FILTER (WHERE cleared_volume > 0), 2) AS mean_price_cleared
            FROM silver_neso_data_portal_eac_br_results_summary_latest
            WHERE auction_id IN ('943', '945', '947', '949', '951', '953', '955')
            GROUP BY ALL ORDER BY auction_product DESC, auction_id""")
      - |
        pbr = data.sql("""
            SELECT s.delivery_start, s.cleared_volume, SUM(u.executed_quantity) AS units_mw, s.clearing_price
            FROM silver_neso_data_portal_eac_br_results_summary_latest s
            LEFT JOIN silver_neso_data_portal_eac_br_results_by_unit_latest u
              ON u.auction_product = s.auction_product AND u.delivery_start = s.delivery_start
            WHERE s.auction_id = '947' AND s.auction_product = 'PBR'
            GROUP BY ALL ORDER BY s.delivery_start""")
        pbr.iloc[34:38]
      - |
        pbr.index = pbr.delivery_start.str[11:16]
        pbr.clearing_price.plot(drawstyle="steps-post", color="#155A6E", figsize=(8, 3.5),
                                xlabel="window start as written; the day opens 23:00, 20 January",
                                ylabel="PBR clearing price, £/MW/h");
    needs: a capture of the summary and by-unit tables
    plot_alt: >-
      Step plot of the PBR clearing price, in £/MW/h, for each half-hour window of auction 947, from
      23:00 on 20 January to 22:30 on 21 January 2025 as written. It holds 6.85 to 02:30, is 0 at
      06:00 and 06:30, peaks at 179.99 at 17:00 and 17:30, and ends at 84.99.
  related:
    - {dataset: elexon/bmunits_reference, note: "All `auction_unit` values are National Grid BM unit IDs in the register"}
    - {dataset: elexon/boal, note: "BM acceptances for the units holding reserve, joined via the register"}
    - {dataset: elexon/system_prices, note: Imbalance prices for the half-hours the reserve covers}
  family:
    slug: eac-br-auction-results
    members:
      - dataset: eac_br_results_summary
        differs: "Cleared MW and clearing price per auction, product and half-hour window"
        request: "GET https://api.neso.energy/datastore/dump/1b3f2ee1-74a0-4939-a5a3-f01f19e663e4"
      - dataset: eac_br_results_by_unit
        differs: "Winning units' MW per window, summing to the summary's; no rows at 0 MW"
        request: "GET https://api.neso.energy/datastore/dump/5d8e47be-e262-4398-89b0-6f93f636faf6"
      - dataset: eac_br_results_buy_orders
        differs: "NESO's price targets for quantities per window; executed MW sums to the summary"
        request: "GET https://api.neso.energy/datastore/dump/8a549d29-52cd-4016-a04e-c01a3e31bd3a"
      - dataset: eac_br_results_sell_orders
        differs: "Every provider order with price limit and outcome; zero-MW orders can read executed"
        request: "GET https://api.neso.energy/datastore/dump/3f53c38b-d287-41af-b4c8-769abb6e707a"
---

# EAC-BR Auction Results

This package is NESO's **archive of Balancing Reserve (BR) auction results from the Enduring Auction
Capability (EAC) platform**: the day-ahead auctions in which NESO buys Balancing Reserve, a reserve
service delivered in half-hour windows. It holds four tables that describe each auction from different
angles: what each participant offered (**sell orders**), what NESO asked to buy (**buy orders**), which
units won and at what price (**results by unit**), and the cleared volume and price per product and window
(**results summary**). For a model they are the price-and-volume outcome of the reserve market: the
clearing price per product and window is the natural target, cleared volume and unit-level winners are
features. The vendor tags the package "BR Auction Results on EAC" and publishes it as a frozen archive
(CKAN package `notes` and tags,
@.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json; NESO
[EAC-BR auction results](https://www.neso.energy/data-portal/eac-br-auction-results)).

Supported by National Energy SO Open Data

**What this package is not.**

- It is **event results, not forecasts**: no forecast issue time is used (`issue: none` on every family).
- It is **not a settlement-period table**: there is no `run_type` and none is invented. The windows are the
  product delivery windows in `delivery_start` and `delivery_end`.
- It is **not the newer EAC auction results package** (@./eac-auction-results.md). Measured on the captured
  bodies, the two share no auction id and no entity key (596 Balancing Reserve archive auction ids against
  1,071 in the newer package's by-unit/buy/sell tables, 0 in common; the newer package's BR rows start at
  2025-10-29T23:00:00Z, after this archive's last raw half-hour start). Publishing both therefore does not
  double count the measured tables. This is a measured result, not a vendor guarantee that the two id
  namespaces are separate, so the families stay separate and carry package provenance
  (@.planning/phases/v0.22-K-AS-4/K-AS-4-FACTS.md section 7 and
  @.planning/phases/v0.22-K-AS-4/post-merge/SELL-CAPTURE-CHECKS.md check 7).
- It is **not the EAC-BR mock auction results** (`eac-br-mock-auction-results`), a separate NESO package of
  mock/test data. That package is held and documented on its own page; never join it to these tables on
  auction id.

**How the four tables reconcile (measured with Polars on silver, 2026-10-18).** For every summary row
(auction, product, window), the buy orders' `executed_quantity` summed equals `cleared_volume` (57,216 of
57,216), and so does the sell orders' `executed_quantity` summed over all order types (parent, child and
substitutable child together). The by-unit table is one row per `auction_unit`, product and window, equal
to that unit's sell-order executed MW summed (621,111 of 621,111); summed per window it equals
`cleared_volume` in the 39,673 windows that have unit rows, and the other 17,543 summary windows cleared
0 MW. Every buy, sell and by-unit row carries its window's summary `clearing_price`. The tables restate
the same cleared MW from different sides, so never add two of them. All 157 `auction_unit` values match
`national_grid_bm_unit` in `elexon/bmunits_reference` silver.

**The clock is undocumented.** The resource dictionaries give the role of `deliveryStart`, `deliveryEnd` and
`orderEntryTime` (delivery window start and end; bid submission time) but do not state the clock of these
archive exports. The cells are timezone-naive text (single shape `YYYY-MM-DDThh:mm:ss`). The newer EAC
package's statement that its datetimes are UTC is **not** transferred to this archive. So gridflow keeps
every time cell as a **raw string**, declares temporal recipe `none`, and does not slice a date out of a
timestamp. Silver asserts neither UTC nor UK local time; any reading is a stated convention (the site's
chart reads them as UTC, on the evidence below). TODO: verify the clock of the
BR archive exports (BR-ARCHIVE-EXPORT-CLOCK); an archive-specific vendor statement or export specification
would settle it. Until then the question is non-holding because the raw string publishes no clock.
Evidence toward settling the clock, measured on silver (2026-10-18), not a vendor statement: each of the 596
auctions covers one day of 30-minute windows whose first start is written `23:00` when that day is in
GMT and `22:00` when it is in BST, with 46 windows on the spring clock-change days (auctions 189, 1109)
and 50 on the autumn ones (746, 2081). That is what UTC strings for a 23:00-to-23:00 UK day would show,
and not what UK local strings would. Corroboration from the sell orders: in 595 of 596 auctions the last
`order_entry_time` falls 14h44m to 15h29m before the auction's first window string, so it is written one
hour earlier on BST days (06:31 to 07:16) than on GMT days (07:31 to 08:16), as a fixed UK-time gate
written in UTC would be (auction 187 is the exception, 29h15m). NESO's companion package gives the auction
time as 08:15, zone unstated. The cells stay raw strings.

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: EVT
- Package id: `94c65383-a108-468f-aad4-1d96380be93f` · CKAN licence id `ESO` (NESO Open Data Licence)
- Silver rows (RULINGS 770, 775; @.planning/v0.22-RESULTS.md section AS-4b): by unit 621,111 · buy orders
  98,592 · summary 57,216 · sell orders 3,124,058 = **3,900,977** rows, 0 validation failures, 0 rows
  excluded. No family is held.

## Files by disposition

All four resources are CKAN datastore tables: there is no DOC file and no uploaded file in this package, so
there are no download links to documents. Each resource is captured as one whole-table CSV dump from the
datastore dump endpoint (the "Id" is the dump path suffix: `https://api.neso.energy/datastore/dump/<Id>`).
The resource names say "2023-2024" but the captured contents are not limited to those years: the sell-order
delivery windows run from 2024-03-12T23:00:00 to 2025-10-29T22:30:00 (raw strings, see the clock note), and
the CKAN `last_modified` of each resource (2024-02-16 to 2024-02-19) predates that content, so it does not
date the rows.

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| NESO Balancing-Reserve Buy Orders 2023-2024 | CSV | dump | `8a549d29-52cd-4016-a04e-c01a3e31bd3a` |
| NESO Balancing-Reserve Results By Unit 2023-2024 | CSV | dump | `5d8e47be-e262-4398-89b0-6f93f636faf6` |
| NESO Balancing-Reserve Results Summary 2023-2024 | CSV | dump | `1b3f2ee1-74a0-4939-a5a3-f01f19e663e4` |
| NESO Balancing-Reserve Sell Orders 2023-2024 | CSV | dump | `3f53c38b-d287-41af-b4c8-769abb6e707a` |

Captures (one per resource; amendment and deletion behaviour between captures is unmeasured):

| Family | Stamp (UTC) | Bytes | Logical rows | CKAN `last_modified` of the resource |
|---|---|---:|---:|---|
| `eac_br_results_by_unit` | 20261008T101551Z | 97,082,626 | 621,111 | 2024-02-19T11:31:32 |
| `eac_br_results_buy_orders` | 20261008T101453Z | 13,614,854 | 98,592 | 2024-02-19T11:28:38 |
| `eac_br_results_summary` | 20261008T102623Z | 4,293,803 | 57,216 | 2024-02-16T16:40:40 |
| `eac_br_results_sell_orders` | 20261013T170016Z | 569,094,121 | 3,124,058 | 2024-02-19T11:25:47 |

All four bodies are valid UTF-8 and parse faithfully (production reader against a strict `csv.reader`, cell
by cell). The sell-orders dump has no `Content-Length`, was estimated at about 561 MB before capture and
tripped the registry's 512 MiB default, so that one family carries a per-family
`max_download_bytes` of 805,306,368 (RULINGS 747, 767); the other three keep 536,870,912.

## Families

Every family shares the same record shape: reader `csv`, strict `utf-8`, one header epoch, temporal `none`,
issue `none`, `latest: whole_capture` (the newest capture replaces the table; no partition), vintage
`capture_fallback`. No trim, no null-token map and no bounds apply: the bodies contain no padding,
separators, percent signs, `NA`, `N/A` or `-1` tokens, and zeros are real values. Opaque identifiers are
strings, byte-equal (never cast to integers); quantity, price and ratio columns are `float64`; every time
cell is a raw string.

**The two clocks, per family.**

- **Vintage.** The record is `capture_fallback`: all four resources are datastore tables, for which the
  record model forbids the CKAN `last_modified` vintage (`registry/record.py` V-8, per
  @.planning/phases/v0.22-K-AS-4/K-AS-4b-SPEC.md). `available_at` is therefore the **gridflow capture
  time** (sidecar `written_at`), labelled so, and `published_at` is null. The CKAN `last_modified` of each
  resource is recorded in the bronze sidecar (`request_params.ckan_last_modified`, table above) but is not
  used as `available_at`. The vendor's original publication instant is unknown. TODO: verify when each
  auction result was first published.
- **Event time.** Temporal recipe `none` on every family: `timestamp_utc` is **the capture time, not the
  delivery window**, and `event_time` carries no auction information. The delivery window is in the raw
  `delivery_start` / `delivery_end` strings.

`orderEntryTime` is bid submission time. An order row also carries the auction outcome (acceptance,
executed quantity, clearing price, rejection reason), which was not known at submission, so
`order_entry_time` is not evidence of when those outcome columns became available. For point-in-time work
use `available_at`, and treat the archive as revised-at-capture.

Units (vendor resource dictionaries, never inferred from column names; @.planning/phases/v0.22-K-AS-4/K-AS-4-FACTS.md
section 7): `quantity`, `executed_quantity`, `cleared_volume` are **MW**; `price`, `price_limit`,
`clearing_price` are **£/MW/h**; `acceptance_ratio` is a **dimensionless proportion**; auction, order,
basket, product and unit-result ids are identifiers with no physical unit; `reason_rejected` is a text
code. The skeleton's vendor-unit column below shows what the field info publishes (it lists `ISO8601` on the
by-unit time cells, which describes a format, not a unit).

Sentinel handling: no sentinel values were found in any of the four bodies, so none is mapped. Zero stays
zero. Blank cells are null in every column except two: `technology_type` and `post_code` in
`eac_br_results_by_unit`, where blanks appear as null or as empty string (split under that family below) and
both mean missing. Measured on silver, `joined_family` and `substitutability_family` (buy orders) are null
in all 98,592 rows, `looped_basket_id` is null in 150,918 sell-order rows and `reason_rejected` in 671,741,
with 0 empty strings in each; `acceptance_ratio` has no upper bound applied (measured range in the sell
orders is 0 to 1, with no value above 1).

### `eac_br_results_buy_orders`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no
- Grain: one row per buy order and its outcome within an auction. Silver rows: 98,592.

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| auctionID | `auction_id` | string | — | no | — | — |
| orderID | `order_id` | string | — | no | — | — |
| serviceType | `service_type` | string | — | yes | — | — |
| auctionProduct | `auction_product` | string | — | yes | — | — |
| deliveryStart | `delivery_start` | string | — | yes | — | — |
| deliveryEnd | `delivery_end` | string | — | yes | — | — |
| quantity | `quantity` | float64 | — | yes | — | MW |
| price | `price` | float64 | — | yes | — | £/MW/h |
| joinedFamily | `joined_family` | string | — | yes | — | — |
| substitutabilityFamily | `substitutability_family` | string | — | yes | — | — |
| paradoxicallyAcceptanceAllowed | `paradoxically_acceptance_allowed` | string | — | yes | — | — |
| orderEntryTime | `order_entry_time` | string | — | yes | — | — |
| acceptanceRatio | `acceptance_ratio` | float64 | — | yes | — | — |
| status | `status` | string | — | yes | — | — |
| executedQuantity | `executed_quantity` | float64 | — | yes | — | MW |
| clearingPrice | `clearing_price` | float64 | — | yes | — | £/MW/h |
| reasonRejected | `reason_rejected` | string | — | yes | — | — |

- Entity key: `auction_id`, `order_id`. `order_id` alone is also unique in the captured body, but the vendor
  defines order identity within an auction, so the composite key is used.
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time
- Column order differs from the newer EAC buy-orders table: here `joinedFamily` comes before
  `substitutabilityFamily`. The header is frozen in this body's own order.
- `joined_family` and `substitutability_family` are blank throughout the captured body (null); do not
  assume the same of the mock package or the newer EAC table.

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

### `eac_br_results_by_unit`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no
- Grain: one accepted unit result for an auction product and delivery window. Silver rows: 621,111.

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| registeredAuctionParticipant | `registered_auction_participant` | string | — | yes | — | — |
| auctionUnit | `auction_unit` | string | — | yes | — | — |
| serviceType | `service_type` | string | — | yes | — | — |
| auctionProduct | `auction_product` | string | — | yes | — | — |
| executedQuantity | `executed_quantity` | float64 | — | yes | — | MW |
| clearingPrice | `clearing_price` | float64 | — | yes | — | £/MW/h |
| deliveryStart | `delivery_start` | string | — | yes | — | ISO8601 |
| deliveryEnd | `delivery_end` | string | — | yes | — | ISO 8601 |
| technologyType | `technology_type` | string | — | yes | — | — |
| postCode | `post_code` | string | — | yes | — | — |
| unitResultID | `unit_result_id` | string | — | no | — | — |

- Entity key: `unit_result_id` (vendor-described as a unique result identifier; nonblank and unique across
  all 621,111 rows). It carries no separate auction id column; the auction id is a prefix inside the
  identifier, which gridflow keeps intact and does not split.
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time
- `technology_type` (1,877 blank cells) and `post_code` (149,665 blank cells) are optional; blanks are not
  a key defect. In silver the blanks are a **mix of null and empty string**, not uniformly null (measured
  with Polars on the silver Parquet): `technology_type` is 922 null + 955 empty string = 1,877;
  `post_code` is 144,128 null + 5,537 empty string = 149,665. Consumers must treat both null and `""` as
  missing for these two columns. This differs from the K-AS-4b-SPEC expectation of "blank becomes null".
  TODO: verify why the transformer leaves empty strings in these two columns (finding for the transformer
  owner; no value is dropped or invented either way).
- The vendor's `ISO8601` note on the time cells describes the intended format. The cells are naive text with
  no offset, so it does not establish the clock.

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

### `eac_br_results_sell_orders`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no
- Grain: one row per sell order (parent, child or substitutable child) and its outcome within an auction.
  Silver rows: 3,124,058. The largest family in the package; `max_download_bytes` is 805,306,368.

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| auctionID | `auction_id` | string | — | no | — | — |
| registeredAuctionParticipant | `registered_auction_participant` | string | — | yes | — | — |
| auctionUnit | `auction_unit` | string | — | yes | — | — |
| basketID | `basket_id` | string | — | yes | — | — |
| serviceType | `service_type` | string | — | yes | — | — |
| deliveryStart | `delivery_start` | string | — | yes | — | — |
| deliveryEnd | `delivery_end` | string | — | yes | — | — |
| orderID | `order_id` | string | — | no | — | — |
| orderType | `order_type` | string | — | yes | — | — |
| auctionProduct | `auction_product` | string | — | yes | — | — |
| productID | `product_id` | string | — | yes | — | — |
| quantity | `quantity` | float64 | — | yes | — | MW |
| priceLimit | `price_limit` | float64 | — | yes | — | £/MW/h |
| loopedBasketID | `looped_basket_id` | string | — | yes | — | — |
| orderEntryTime | `order_entry_time` | string | — | yes | — | — |
| acceptanceRatio | `acceptance_ratio` | float64 | — | yes | — | — |
| status | `status` | string | — | yes | — | — |
| executedQuantity | `executed_quantity` | float64 | — | yes | — | MW |
| clearingPrice | `clearing_price` | float64 | — | yes | — | £/MW/h |
| reasonRejected | `reason_rejected` | string | — | yes | — | — |

- Entity key: `auction_id`, `order_id`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time
- This record was frozen **before** any bronze existed, from the pre-capture row count and header probe, and
  was activated only after the capture passed its checks (RULINGS 747, 772). Capture checks
  (@.planning/phases/v0.22-K-AS-4/post-merge/SELL-CAPTURE-CHECKS.md): row count equals the probe's 3,124,058;
  strict UTF-8 over the whole body; header byte-equal to the frozen header (and to the newer EAC sell-orders
  first epoch); parser faithful on every row; `(auctionID, orderID)` nonblank and unique, 0 identical rows;
  all five `float64` columns cast strictly; the three time columns have one lexical form
  (`YYYY-MM-DDThh:mm:ss`, no offset, no `Z`).
- Structure notes from that receipt: `status` is `REJECTED`, `EXECUTED` or `PARTIALLY_EXECUTED`; `orderType`
  is `PARENT`, `CHILD` or `SUBSTITUTABLECHILD`; `serviceType` is only "Balancing Reserve"; `auctionProduct`
  is `PBR` or `NBR`. `reason_rejected` is a text code (for example `11`, `21`, `14`; digits are kept as
  text) and is blank exactly for the executed and partially executed rows. `looped_basket_id` is blank on
  about 5% of rows (150,918), otherwise digits. `basketID`, `productID` and `orderID` are digit strings.
- Overlap closed: the 596 auction ids of this table equal the archive's ids in the other three families, with
  **0** auction ids and **0** `(auction_id, order_id)` pairs in common with the newer EAC
  `eac_results_sell_orders` silver (BR-SELL-ARCHIVE-OVERLAP, measured disjoint).
- Peak working set to transform this family alone was 3,183.4 MiB (RULINGS 775); transform it on its own,
  not alongside other large families.

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

### `eac_br_results_summary`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no
- Grain: one row per auction, product and delivery window. Silver rows: 57,216.

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| auctionID | `auction_id` | string | — | no | — | — |
| auctionProduct | `auction_product` | string | — | no | — | — |
| serviceType | `service_type` | string | — | yes | — | — |
| deliveryStart | `delivery_start` | string | — | no | — | — |
| deliveryEnd | `delivery_end` | string | — | yes | — | — |
| clearedVolume | `cleared_volume` | float64 | — | yes | — | MW |
| clearingPrice | `clearing_price` | float64 | — | yes | — | £/MW/h |

- Entity key: `auction_id`, `auction_product`, `delivery_start` (the start is a raw string and is part of
  the key as text). Auction identity stays in the key, as in the newer EAC summary tables.
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time
- Unlike the newer EAC summary, this archive has no `linkedServiceWindowID` column; none is generated.

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

## Cadence

- Registry refresh: frozen
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Daily
- The vendor's "Daily" label does not match the data: the resources' CKAN `last_modified` dates are February
  2024 and the delivery windows end on 2025-10-29, when the newer EAC package takes over Balancing Reserve.
  gridflow treats the package as a frozen archive: one whole-table capture per resource. TODO: verify with
  NESO whether the archive is ever amended, and whether the "Daily" label is a stale default. A re-capture
  replaces the table (`whole_capture`) and is not blended with earlier captures.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

## Holds

- none

Non-holding open questions (all keep their records eligible; each is surfaced rather than guessed):

- TODO: verify the clock of the archive's naive `deliveryStart`, `deliveryEnd` and `orderEntryTime` cells
  (BR-ARCHIVE-EXPORT-CLOCK). Until settled the cells stay raw strings.
- TODO: verify the exact closure of the delivery interval endpoints (whether `deliveryEnd` is inclusive);
  the period roles are established, interval-closure semantics are not.
- TODO: verify when each auction result was first published, and whether the archive is amended after
  publication; one capture per resource cannot measure revision behaviour.

Related pages: @./eac-auction-results.md (the newer EAC package, which carries Balancing Reserve from
2025-10-29), @./balancing-reserve-auction-requirement-forecast.md (the volume NESO forecast it would
procure), and the held mock package page for `eac-br-mock-auction-results`.
Delivered in v0.22 batch AS-4b: @.planning/v0.22-RESULTS.md section AS-4b, evidence
@.planning/phases/v0.22-K-AS-4/K-AS-4-FACTS.md and spec
@.planning/phases/v0.22-K-AS-4/K-AS-4b-SPEC.md, rulings 747, 748, 749, 767, 770, 772 and 775 in
@.planning/RULINGS.md.
