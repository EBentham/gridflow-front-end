---
source: "neso_data_portal"
package: "eac-mock-auction-results"
dataset_keys: ["eac_mock_results_buy_orders", "eac_mock_results_by_unit", "eac_mock_results_daily_buy_orders", "eac_mock_results_daily_by_unit", "eac_mock_results_daily_sell_orders", "eac_mock_results_daily_summary", "eac_mock_results_sell_orders", "eac_mock_results_summary"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-13
layer_coverage: "bronze, silver"
eligibility: "held"
page:
  held: true
  title: EAC mock auction results
  summary: >-
    NESO's test runs of its EAC auction platform for response and reserve services: summaries, unit
    results and orders, not real procurement.
  facts:
    vendor: "NESO Data Portal: four datastore tables and four daily CSV files"
    cadence: Weekly, as NESO lists it
    grain: "Summary: one row per mock auction, product and delivery window"
  landscape: market
  what_it_is: >-
    Rehearsals of NESO's Enduring Auction Capability, the platform that buys response (Dynamic
    Containment, Moderation, Regulation) and reserve services. Tables mirror the real package's:
    summary, results by unit and orders, plus four daily files. They show auction
    mechanics, not real prices or volumes. Mock numbers 1 to 13 also appear in NESO's real EAC
    auction history: never join on them.
  how_used:
    - Learning the EAC tables and auction mechanics before reading the real results
    - "How orders fare in the auction: acceptance ratio, rejection reason, executed MW"
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then each table's datastore dump, or each daily
      file downloaded whole. Swap in any table's key; the daily tables are ingest only.
    commands:
      - {run: gridflow ingest neso_data_portal eac_mock_results_summary --last 24h, comment: "whole dump to bronze"}
      - {run: gridflow transform neso_data_portal eac_mock_results_summary --last 24h, comment: "the capture's date to silver"}
  family:
    slug: eac-mock-auction-results
    members:
      - dataset: eac_mock_results_summary
        differs: "Cleared MW and clearing price per mock auction, product and window"
        request: "GET https://api.neso.energy/datastore/dump/454216d8-61f3-40b6-b787-4dff035ce3c3"
        held: Test-run results, not real procurement; NESO does not say if times are UTC or UK local.
      - dataset: eac_mock_results_by_unit
        differs: "Winning units' MW and price per window, with participant and technology"
        request: "GET https://api.neso.energy/datastore/dump/955cf89f-232e-4b9c-8414-6351080f49fa"
        held: Test-run results, not real procurement; NESO does not say if times are UTC or UK local.
      - dataset: eac_mock_results_buy_orders
        differs: "NESO's buy orders per window: quantity, price, status and executed MW"
        request: "GET https://api.neso.energy/datastore/dump/700a73ff-38e9-45ff-a674-085bcbfc9faf"
        held: Test-run results, not real procurement; NESO does not say if times are UTC or UK local.
      - dataset: eac_mock_results_sell_orders
        differs: "Every provider's sell order, with price limit, status and executed MW"
        request: "GET https://api.neso.energy/datastore/dump/3b18345a-1933-44d7-abd9-062a2e695ccd"
        held: Test-run results, not real procurement; NESO does not say if times are UTC or UK local.
      - dataset: eac_mock_results_daily_summary
        differs: The daily counterpart of the summary; header only when fetched
        request: "GET https://api.neso.energy/dataset/8a6f23d7-8489-49ac-9b0a-566fb53d32f8/resource/f67a53d7-d46d-4550-8947-0c60328b2347/download/neso-response-reserve-daily-results-summary.csv"
        held: "NESO's daily file holds only a header row when fetched; gridflow keeps it in bronze only."
      - dataset: eac_mock_results_daily_by_unit
        differs: The daily counterpart of the results by unit; header only when fetched
        request: "GET https://api.neso.energy/dataset/8a6f23d7-8489-49ac-9b0a-566fb53d32f8/resource/6a051ca2-715b-4966-9c16-58e52254f10b/download/neso-response-reserve-daily-results-by-unit.csv"
        held: "NESO's daily file holds only a header row when fetched; gridflow keeps it in bronze only."
      - dataset: eac_mock_results_daily_buy_orders
        differs: The daily counterpart of the buy orders; header only when fetched
        request: "GET https://api.neso.energy/dataset/8a6f23d7-8489-49ac-9b0a-566fb53d32f8/resource/f994f9bb-a2f3-48ff-a776-0b343806d978/download/neso-response-reserve-daily-buy-orders.csv"
        held: "NESO's daily file holds only a header row when fetched; gridflow keeps it in bronze only."
      - dataset: eac_mock_results_daily_sell_orders
        differs: The daily counterpart of the sell orders; header only when fetched
        request: "GET https://api.neso.energy/dataset/8a6f23d7-8489-49ac-9b0a-566fb53d32f8/resource/c4d0341d-806d-4e53-9ae8-2c54df740ba3/download/neso-response-reserve-daily-sell-orders.csv"
        held: "NESO's daily file holds only a header row when fetched; gridflow keeps it in bronze only."
  related:
    - {dataset: neso_data_portal/eac-auction-results, note: The real auctions these runs rehearse; never join on auction number}
    - {dataset: neso_data_portal/eac-br-mock-auction-results, note: "A second mock package, named 2023-2024, for Balancing Reserve alone"}
    - {dataset: neso_data_portal/eac-br-auction-results, note: "Real Balancing Reserve results; this mock also rehearses that service"}
---

# EAC mock auction results

This package is NESO's record of the **mock (test-run) auctions of the Enduring Auction Capability (EAC)**, the
platform that now buys NESO's response services (Dynamic Containment, Dynamic Moderation, Dynamic Regulation)
and reserve services (Balancing Reserve, Quick Reserve, Slow Reserve). NESO describes these resources as the
outcomes of **mock auction runs** and separates their publication from the successful live auctions
(K-AS-3 FACTS section 4.1; NESO [EAC mock auction results](https://www.neso.energy/data-portal/eac-mock-auction-results)).
They have the same four table kinds as the live package (results by unit, buy orders, results summary, sell
orders), plus four **daily** counterparts. The tables describe what bidders offered and what a rehearsal of the
auction algorithm awarded: **they are not evidence of real procurement, real clearing prices or real volumes.**
A model must therefore not use them as price or volume history for the live ancillary-services market. Their
use is to understand the shape of the EAC tables and the auction mechanics before the live package
(@./eac-auction-results.md) is read.

**The whole package is held, and every output is held twice.** Nothing in this package is published
(RULINGS 738, 751, 752; ledger in `.planning/RULINGS.md`):

1. **Package hold, EAC-MOCK-TEST-DATA.** The package is registered `held` so the rows stay unpublished even
   after the clock question below is answered, until an explicit test/mock label with separate provenance exists.
2. **Family hold, EAC-MOCK-CLOCK.** Each of the four populated families carries a hold on the unanswered
   question of which clock the mock exports use for their naive time cells.

Held means silver is written and reconciled but **no consumer-facing output is released**. This page therefore
documents the **schema, row counts, clocks and the hold questions only; it states no data values** for any
held family (no sample rows, no value ranges, no zero or outlier counts). Eight resources, eight families:
four populated (hold EAC-MOCK-CLOCK) and four **header-only** daily resources that have no record and no silver.

**What this package is not.**

- It is **not the live EAC package** (@./eac-auction-results.md). The mock environment **reuses small auction
  numbers for different dates** and the mock summary key set does not intersect the live one (K-AS-3 FACTS
  4.1, 3.5). **Never join mock to live on `auction_id`.** There is no safe shared key.
- It is **not a forecast**: no issue time exists or is invented (`issue: none` on every family).
- It is **not the sibling `eac-br-mock-auction-results` package**, a separate registered package of four
  ingest-only families (`eac_br_mock_results_*`; eligibility report `docs/neso_data_portal/eligibility.md`).
  Whether the two mock packages are related by scope or duplicate each other is not established here:
  `TODO: verify` before relying on either.
- It is **not a settlement-period table**: there is no `run_type`, no settlement period and none is fabricated.

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: EVT

## Files by disposition

All eight resources are disposition **SILVER** (a CKAN datastore dump or an uploaded CSV that gridflow parses);
there are **no DOC, HOLD or SKIP resources** in this package, hence no document download links. For the four
daily resources a SILVER disposition is nominal: the vendor serves them header-only, so they are captured
ingest-only and no silver exists (see Families).

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| NESO Mock Response-Reserve Buy Orders 2025-2026 | CSV | dump | `700a73ff-38e9-45ff-a674-085bcbfc9faf` |
| NESO Mock Response-Reserve Daily Buy Orders | CSV | upload | `f994f9bb-a2f3-48ff-a776-0b343806d978` |
| NESO Mock Response-Reserve Daily Results By Unit | CSV | upload | `6a051ca2-715b-4966-9c16-58e52254f10b` |
| NESO Mock Response-Reserve Daily Results Summary | CSV | upload | `f67a53d7-d46d-4550-8947-0c60328b2347` |
| NESO Mock Response-Reserve Daily Sell Orders | CSV | upload | `c4d0341d-806d-4e53-9ae8-2c54df740ba3` |
| NESO Mock Response-Reserve Results By Unit 2025-2026 | CSV | dump | `955cf89f-232e-4b9c-8414-6351080f49fa` |
| NESO Mock Response-Reserve Results Summary 2025-2026 | CSV | dump | `454216d8-61f3-40b6-b787-4dff035ce3c3` |
| NESO Mock Response-Reserve Sell Orders 2025-2026 | CSV | dump | `3b18345a-1933-44d7-abd9-062a2e695ccd` |

**Where each resource is fetched from** (sidecar `request_url`, bronze under
`C:/gridflow-data/bronze/neso_data_portal/<family>/`). The package id is `8a6f23d7-8489-49ac-9b0a-566fb53d32f8`.

| Family | Fetch URL | Bronze capture |
|---|---|---|
| `eac_mock_results_by_unit` | `https://api.neso.energy/datastore/dump/955cf89f-232e-4b9c-8414-6351080f49fa` | 2026-10-08, 1,654,174 bytes |
| `eac_mock_results_buy_orders` | `https://api.neso.energy/datastore/dump/700a73ff-38e9-45ff-a674-085bcbfc9faf` | 2026-10-08, 2,261,483 bytes |
| `eac_mock_results_sell_orders` | `https://api.neso.energy/datastore/dump/3b18345a-1933-44d7-abd9-062a2e695ccd` | 2026-10-08, 5,304,231 bytes |
| `eac_mock_results_summary` | `https://api.neso.energy/datastore/dump/454216d8-61f3-40b6-b787-4dff035ce3c3` | 2026-10-08, 504,375 bytes |
| `eac_mock_results_daily_by_unit` | `https://api.neso.energy/dataset/8a6f23d7-8489-49ac-9b0a-566fb53d32f8/resource/6a051ca2-715b-4966-9c16-58e52254f10b/download/neso-response-reserve-daily-results-by-unit.csv` | 2026-10-13, 163 bytes |
| `eac_mock_results_daily_buy_orders` | `https://api.neso.energy/dataset/8a6f23d7-8489-49ac-9b0a-566fb53d32f8/resource/f994f9bb-a2f3-48ff-a776-0b343806d978/download/neso-response-reserve-daily-buy-orders.csv` | 2026-10-13, 238 bytes |
| `eac_mock_results_daily_summary` | `https://api.neso.energy/dataset/8a6f23d7-8489-49ac-9b0a-566fb53d32f8/resource/f67a53d7-d46d-4550-8947-0c60328b2347/download/neso-response-reserve-daily-results-summary.csv` | 2026-10-13, 114 bytes |
| `eac_mock_results_daily_sell_orders` | `https://api.neso.energy/dataset/8a6f23d7-8489-49ac-9b0a-566fb53d32f8/resource/c4d0341d-806d-4e53-9ae8-2c54df740ba3/download/neso-response-reserve-daily-sell-orders.csv` | 2026-10-13, 303 bytes |

Vendor dictionaries (human pages): [mock buy orders](https://www.neso.energy/data-portal/eac-mock-auction-results/neso_mock_response-reserve_buy_orders_2025-2026),
[mock by unit](https://www.neso.energy/data-portal/eac-mock-auction-results/neso_mock_response-reserve_results_by_unit_2025-2026),
[mock sell orders](https://www.neso.energy/data-portal/eac-mock-auction-results/neso_mock_response-reserve_sell_orders_2025-2026),
[mock summary](https://www.neso.energy/data-portal/eac-mock-auction-results/neso_mock_response-reserve_results_summary_2025-2026).
Saved field info: `.planning/research/neso-snapshots/field-info/20261008T114228Z/eac_mock_results_*.json`.

## The two clocks, family by family

Every silver row carries two clocks. They are the same for every populated family of this package, and the
**event clock is deliberately empty**:

| Clock | Value in this package |
|---|---|
| **Vintage** (when the data was available) | `available_at` = the **gridflow capture time**, taken from the bronze sidecar `written_at`. The registry vintage is `capture_fallback`: the four datastore dumps carry **no `ckan_last_modified`** (an empty value in every sidecar), so there is no vendor modification time to use. `published_at` is null on every row. `available_at` is labelled as capture time, never as a vendor publication time. |
| **Event time** (what the row is about) | Temporal recipe **`none`**. `timestamp_utc` and `event_time` are **the capture time** (they equal `capture_written_at` on every row of every family, checked in silver on 2026-10-13); they are **not** the delivery window and **not** the order time. This is a deliberate consequence of the open clock question, not a defect. |

Because the recipe is `none`, the vendor's own time cells, `deliveryStart`, `deliveryEnd` and `orderEntryTime`,
are kept as **raw `string` columns**, byte-for-byte as served. They are naive (no offset). The vendor does not
declare their clock for this package and the live package's UTC declaration **does not extend to it**
(EAC-MOCK-CLOCK below). Do not parse them as UTC and do not parse them as UK local time. Their roles are known
from the vendor dictionaries: `deliveryStart` is the time from which delivery of the auction product commences,
`deliveryEnd` the time delivery ends, `orderEntryTime` when the bid was submitted.

| Family | Vintage clock | Event clock |
|---|---|---|
| `eac_mock_results_by_unit` | `capture_fallback` (capture time) | `none`: `timestamp_utc` is the capture time |
| `eac_mock_results_buy_orders` | `capture_fallback` | `none`: `timestamp_utc` is the capture time |
| `eac_mock_results_sell_orders` | `capture_fallback` | `none`: `timestamp_utc` is the capture time |
| `eac_mock_results_summary` | `capture_fallback` | `none`: `timestamp_utc` is the capture time |
| the four `eac_mock_results_daily_*` | no record: no silver, no clock | no record |

The four daily resources do have a CKAN `last_modified` in their sidecars (2026-06-04, from 14:36 to 14:41 UTC;
sidecar field `ckan_last_modified`), but with no record it is stored only in bronze metadata.

## Units and sentinels

**Units come only from the vendor's own dictionaries for these mock resources** (saved field info, K-AS-3 FACTS
4.2); none is inferred from a column name.

| Columns | Unit (vendor dictionary) |
|---|---|
| `quantity`, `executed_quantity`, `cleared_volume` | **MW** |
| `price`, `price_limit`, `clearing_price` | **£/MW/h** (the vendor's wording: cleared price per MW per hour). This is a per-MW-per-hour capacity price, not £/MWh. |
| `acceptance_ratio` | dimensionless **fraction** (the dictionary: a number between 0 and 1, the proportion of an offered or bid quantity matched); not a percentage |
| `minimum_consecutive_windows` | a **count** of consecutive service windows |
| `auction_id`, `order_id`, `basket_id`, `product_id`, `looped_basket_id`, `substitutability_family`, `joined_family`, `flexible_group_id`, `linked_service_window_id`, `unit_result_id` | identifiers or linking labels: no physical unit |
| `delivery_start`, `delivery_end`, `order_entry_time` | time labels: held, see the clocks above. The vendor dictionary unit for the by-unit times is "ISO 8601" (a format, not a clock). |

Nothing is converted or rescaled. The dictionary gives no MW-to-energy conversion and none is applied.

**Typing and sentinels (K-AS-3 FACTS g5).** Identifiers are `string`, byte-equal and never cast (the vendor
types them as integers in some dictionaries, but they are opaque labels and are not used arithmetically).
`minimum_consecutive_windows` is `int64`; measured values are `float64`. **Zeros are real values and stay zero,
negative prices would stay as published, and blanks stay null** (linking, basket and window ids, rejection
reasons, technology type, post code). FACTS found **no `NA`/`N/A` token, thousands separator, percent sign or
padded number** in any body of this package, and the production CSV reader agreed with a strict second parse
on every row and cell, so **no token is mapped to null and no sentinel rule is applied**. There is no price
floor or ceiling and no `min`/`max` bound in any record. A zero executed quantity does not by itself identify
a rejected order.

## Families

The "Vendor unit" column below is the unit stated in the vendor's saved field-info dictionary; it is sparse
because the dictionary states a unit for only some columns. Column meanings are those of the live package;
read @./eac-auction-results.md for the full column-by-column description, since the mock headers are
**identical** to the live modern headers (the by-unit, buy-order, summary and 22-column sell-order headers).
Not all mock facts carry over: the live package's UTC declaration and its eligibility do not.

### `eac_mock_results_buy_orders`

- Kind: tabular · archetype: EVT · refresh: weekly · empty allowed: no

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
| substitutabilityFamily | `substitutability_family` | string | — | yes | — | — |
| paradoxicallyAcceptanceAllowed | `paradoxically_acceptance_allowed` | string | — | yes | — | — |
| orderEntryTime | `order_entry_time` | string | — | yes | — | — |
| acceptanceRatio | `acceptance_ratio` | float64 | — | yes | — | — |
| status | `status` | string | — | yes | — | — |
| executedQuantity | `executed_quantity` | float64 | — | yes | — | MW |
| clearingPrice | `clearing_price` | float64 | — | yes | — | £/MW/h |
| reasonRejected | `reason_rejected` | string | — | yes | — | — |
| joinedFamily | `joined_family` | string | — | yes | — | — |

- Entity key: `auction_id`, `order_id`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

One row per submitted buy order. Resource `700a73ff-38e9-45ff-a674-085bcbfc9faf` (datastore dump), one capture
(2026-10-08). **Silver: 16,938 rows**; one Parquet file under
`C:/gridflow-data/silver/neso_data_portal/eac_mock_results_buy_orders/year=2026/month=10/` (the partition is
the capture date), with the 17 vendor columns then `timestamp_utc`, `published_at`, `bronze_capture_id`,
`capture_written_at`, `event_time`, `available_at`, `source_run_id`, `dataset_version` (25 columns). Held:
EAC-MOCK-CLOCK (and the package hold). The key is unique in the body (FACTS); the vendor guarantees no key and
order identity across later corrected exports is undocumented, so `_latest` is `whole_capture`, never
`key_latest` (`TODO: verify` order identity across re-exports, as for the live package).

### `eac_mock_results_by_unit`

- Kind: tabular · archetype: EVT · refresh: weekly · empty allowed: no

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

- Entity key: `unit_result_id`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

One row per accepted unit result. Resource `955cf89f-232e-4b9c-8414-6351080f49fa` (datastore dump), one capture
(2026-10-08). **Silver: 13,073 rows**; 19 columns (the 11 vendor columns plus the 8 gridflow
columns). The vendor documents `unitResultID` as the unique unit-result record identifier, which is why it is
the key; it is an opaque string and its composition is `TODO: verify` (do not split it). There is **no
`auctionID` column** in this table. Place a unit result in an auction only through the explicit delivery
fields, and only after the clock is settled. Held: EAC-MOCK-CLOCK.

### `eac_mock_results_daily_buy_orders`

- Kind: tabular · archetype: EVT · refresh: weekly · empty allowed: yes
- ingest-only: no silver yet

Resource `f994f9bb-a2f3-48ff-a776-0b343806d978` (upload). **Header-only at the vendor**: the body is 238 bytes,
one header line of 17 column names (the live buy-order header, H-B), **0 data rows**. Captured once,
on 2026-10-13, and marked an empty capture by the admission path. See "Header-only daily resources" below.

### `eac_mock_results_daily_by_unit`

- Kind: tabular · archetype: EVT · refresh: weekly · empty allowed: yes
- ingest-only: no silver yet

Resource `6a051ca2-715b-4966-9c16-58e52254f10b` (upload). **Header-only at the vendor**: 163 bytes, one line of
11 column names (the by-unit header, H-U), **0 data rows**. Captured once, on 2026-10-13, empty capture. See
"Header-only daily resources" below.

### `eac_mock_results_daily_sell_orders`

- Kind: tabular · archetype: EVT · refresh: weekly · empty allowed: yes
- ingest-only: no silver yet

Resource `c4d0341d-806d-4e53-9ae8-2c54df740ba3` (upload). **Header-only at the vendor**: 303 bytes, one line of
22 column names (the sell-order header, H-O22), **0 data rows**. Captured once, on 2026-10-13, empty capture.
See "Header-only daily resources" below, including a header-spelling discrepancy.

### `eac_mock_results_daily_summary`

- Kind: tabular · archetype: EVT · refresh: weekly · empty allowed: yes
- ingest-only: no silver yet

Resource `f67a53d7-d46d-4550-8947-0c60328b2347` (upload). **Header-only at the vendor**: 114 bytes, one line of
8 column names (the summary header, H-S), **0 data rows**. Captured once, on 2026-10-13, empty capture. See
"Header-only daily resources" below.

### `eac_mock_results_sell_orders`

- Kind: tabular · archetype: EVT · refresh: weekly · empty allowed: no

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
| flexibleGroupID | `flexible_group_id` | string | — | yes | — | — |
| minimumConsecutiveWindows | `minimum_consecutive_windows` | int64 | — | yes | — | — |

- Entity key: `auction_id`, `order_id`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

One row per sell order (the vendor dictionary lists order types `PARENT`, `CHILD`, `SUBSTITUTABLECHILD`).
Resource `3b18345a-1933-44d7-abd9-062a2e695ccd` (datastore dump), one capture (2026-10-08). **Silver: 30,869
rows**; 30 columns (22 vendor plus 8 gridflow). Only one sell-order header (the 22-column H-O22)
occurs in this package, so there is no header-epoch split as in the live sell-order family. Held:
EAC-MOCK-CLOCK.

### `eac_mock_results_summary`

- Kind: tabular · archetype: EVT · refresh: weekly · empty allowed: no

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
| linkedServiceWindowID | `linked_service_window_id` | string | — | yes | — | — |

- Entity key: `auction_id`, `auction_product`, `delivery_start`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

One row per auction, product and service window. Resource `454216d8-61f3-40b6-b787-4dff035ce3c3` (datastore
dump), one capture (2026-10-08). **Silver: 7,128 rows**; 16 columns (8 vendor plus 8 gridflow).
Note the entity key contains `delivery_start`, which here is a **raw string** (the clock is held), so the key
is a byte-equality key on the vendor's text, not on an instant. The key is unique in the body (FACTS); the
vendor revision behaviour is undocumented (`TODO: verify`). Held: EAC-MOCK-CLOCK.

### Header-only daily resources

The four daily mock resources have **no record, no silver and no key**. FACTS measured nothing about them but a
header, so uniqueness and every cross-family intersection are **unmeasured**, and a header-only body cannot
establish a populated record. They are registered with `empty_allowed: true` and `transformer: null`, so the
admission path captures the header-only body and marks the capture empty instead of failing the non-empty guard.
This is the S-sweep `missing` finding made clean (RULINGS 738, 752): the four captures landed on 2026-10-13
(one response each, exit 0, `phases/v0.22-K-AS-3/post-merge/ingest.log`).

- **Vendor behaviour.** The earlier vendor probe of 2026-10-13T03:20:30Z (`phases/v0.22-K-AS-3/LIVE-PROBE.md`)
  and the bronze captures of 2026-10-13T09:5x agree: HTTP 200, a header line, no rows. Whether these files will
  ever populate (the live daily files hold the latest auction only) is `TODO: verify` against later captures.
- **Header discrepancy.** FACTS 4.3 (from the probe) reports the daily sell-order header ending in the
  **singular** `minimumConsecutiveWindow`, unlike the populated sell table's plural. **The bronze capture of
  2026-10-13 shows the plural `minimumConsecutiveWindows`** (22 columns, identical to the populated mock table
  and the live H-O22). Bronze is the better evidence; the discrepancy with the probe record is unexplained
  (`TODO: verify`: probe transcription error, or a vendor change between the probe and the capture). No record
  is frozen from either, so nothing depends on it today.

## Cadence

- Registry refresh: weekly
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Weekly

The vendor states weekly. gridflow has **one capture per resource** (2026-10-08 for the four dumps,
2026-10-13 for the four daily files), so the real refresh rhythm, whether a refresh replaces or extends a
dump, and whether mock runs continue are unmeasured: `TODO: verify` by comparing later complete captures with
the hash-pinned bodies (K-AS-3 FACTS section 2.3). Because the dump sidecars carry no `ckan_last_modified`,
a changed dump can only be told apart by its capture time and body hash.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence). Any
gridflow output derived from this package, once it is released, carries the attribution line
"Supported by National Energy SO Open Data".

## Holds

- package: held: TODO: EAC-MOCK-TEST-DATA — NESO publishes these resources as outcomes of mock auction runs, not live procurement; publish only under an explicit test/mock label with separate provenance, and never join them to live EAC on auction id (mock ids 1–22 are reused for different dates). (unit v0.22-K-AS-3b)
- `eac_mock_results_buy_orders`: held: TODO: EAC-MOCK-CLOCK — the mock package and its dictionaries do not state the clock of the naive deliveryStart / deliveryEnd / orderEntryTime cells, the live package's UTC declaration does not extend to it, and every captured date falls in GMT so UTC and UK local time cannot be told apart; which clock do the mock exports use? (Mock / test data, not procurement results.) (unit v0.22-K-AS-3b)
- `eac_mock_results_by_unit`: held: TODO: EAC-MOCK-CLOCK — (question text as for `eac_mock_results_buy_orders`) (unit v0.22-K-AS-3b)
- `eac_mock_results_sell_orders`: held: TODO: EAC-MOCK-CLOCK — (question text as for `eac_mock_results_buy_orders`) (unit v0.22-K-AS-3b)
- `eac_mock_results_summary`: held: TODO: EAC-MOCK-CLOCK — (question text as for `eac_mock_results_buy_orders`) (unit v0.22-K-AS-3b)

**Skeleton correction.** The generated skeleton printed the package-level question (EAC-MOCK-TEST-DATA) against
every family. The frozen family records carry the EAC-MOCK-CLOCK question above (registry
`src/gridflow/connectors/neso_data_portal/registry/eac-mock-auction-results.json`); the eligibility report
(`docs/neso_data_portal/eligibility.md`) still shows the package question against each family because the
package hold dominates. Both holds apply.

**What would release the output.**

- *EAC-MOCK-CLOCK* needs a mock-specific statement of the export clock, or a vendor API specification expressly
  covering the mock environment. The measured dates all fall in GMT, so agreement with a UTC reading
  does not distinguish UTC from UK local time. The vendor dictionary examples are also inconsistent about a
  `Z` suffix (FACTS 4.1). Until it is answered the time cells stay raw strings and the event recipe stays `none`.
- *EAC-MOCK-TEST-DATA* needs an explicit test/mock label and separate provenance for any published mock row,
  and a guarantee that no consumer joins mock to live on `auction_id`. This hold stays even after the clock
  question is answered.

**Open questions that do not hold any output** (carried as `TODO: verify`):

- The **original publication instant** of the mock results. The vintage is the capture time, never a publication time.
- **Order and result identity across corrected re-exports**, and the **amendment and deletion behaviour** of the
  dumps (one capture each).
- **Interval closure** (INTERVAL-CLOSURE): no source states whether a window's end instant belongs to it.
- Whether the four daily files ever populate, and the spelling of the daily sell-order header (above).
- The relationship between this package and `eac-br-mock-auction-results` (above).

## Known issues and gotchas

- **Do not join to the live package on `auction_id`.** Mock auction numbers are small and are reused for
  different dates; the mock summary keys have no intersection with the live ones (K-AS-3 FACTS 3.5, 4.1).
- **`timestamp_utc` is the capture time, not an event time.** Filtering these tables by `timestamp_utc` filters
  by when gridflow fetched them (a single instant per family today), never by delivery date.
- **The summary entity key includes a raw string `delivery_start`**, so equal instants written differently
  would be different keys. Do not normalise it until the clock is settled.
- **The daily families are empty.** A query against `eac_mock_results_daily_*` finds no silver; the bronze
  captures are header-only. Do not interpret them as "no mock auctions today".
- **Held means unpublished.** Silver exists and reconciles, but no gold, chart, front-end page or model input
  may use these rows.

## Implementation delta

Where the code or a source differs from the docs or from another source:

- **Skeleton hold text** names the package question on every family; the frozen records carry EAC-MOCK-CLOCK
  (above). No code change implied.
- **Daily sell-order header spelling**: probe record (singular) versus bronze capture (plural). Bronze wins.
- **Event time is the capture time** for all four populated families by design (recipe `none`): the code does
  not interpret the vendor's time cells.
- **Download cap**: the registry sets `max_download_bytes` 536,870,912; the largest mock body is 5,304,231
  bytes, so the cap is not a concern for this package.

## Activation receipt

AS-3b merged as PR #115 (`638b427`), triple-green (RULINGS 751). Activation on 2026-10-13 with
`--start/--end 2026-10-08` and no prior silver (`phases/v0.22-K-AS-3/post-merge/transform.log`): the four
populated mock families wrote **13,073 + 16,938 + 7,128 + 30,869 = 68,008** rows, each equal to the spec plan.
Reconcile `--all --cutoff 2026-10-12` exited 0 over 191 families with 0 gaps (RULINGS 752; `.planning/v0.22-RESULTS.md`
section "AS-3b"). The package holds 0 eligible families and 4 held-with-silver, 4 ingest-only (eligibility report).

## Links

- Sibling live package: @./eac-auction-results.md
- Neighbouring auctions: @./static-firm-frequency-response-auction-results.md, @./quick-reserve-auction-requirement-forecast.md
- Vendor index: @../README.md, @../coverage.md
- GB balancing context: @../../../20-domain/markets/gb-balancing-mechanism.md
- Evidence in the gridflow repo: `.planning/phases/v0.22-K-AS-3/K-AS-3-FACTS.md` (sections 2.3, 4), `K-AS-3b-SPEC.md`,
  `LIVE-PROBE.md`, `.planning/RULINGS.md` (736, 737, 738, 751, 752), `.planning/v0.22-RESULTS.md` ("AS-3b")
