---
source: "neso_data_portal"
package: "eac-br-mock-auction-results"
dataset_keys: ["eac_br_mock_results_buy_orders", "eac_br_mock_results_by_unit", "eac_br_mock_results_sell_orders", "eac_br_mock_results_summary"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-13
layer_coverage: "bronze, silver"
eligibility: "held"
page:
  held: true
  title: Balancing Reserve mock auction results
  summary: >-
    NESO's test runs of Balancing Reserve auctions on its EAC platform: summaries, unit results and
    orders, not real procurement.
  facts:
    vendor: "NESO Data Portal: four datastore tables, named Mock Balancing-Reserve 2023-2024"
    cadence: "NESO lists daily; its notice says February 2024 only; gridflow re-checks at most weekly"
    grain: "Summary: one row per mock auction, product (`PBR`, `NBR`) and half-hour window"
  landscape: market
  what_it_is: >-
    Rehearsals of NESO's Balancing Reserve auctions on its Enduring Auction Capability (EAC)
    platform: two products, `PBR` and `NBR` (read as positive and negative reserve), in half-hour
    windows. Its four tables mirror the real package. They show auction mechanics, not real prices
    or volumes. Mock auction numbers also appear in NESO's real EAC auction history: never join on
    them.
  how_used:
    - Learning the Balancing Reserve tables and auction mechanics before the real results
    - "How orders fare in the auction: acceptance ratio, rejection reason, executed MW"
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then each table's datastore dump, re-checked at
      most weekly; an unchanged dump is not stored again. Swap in any table's key.
    commands:
      - {run: gridflow ingest neso_data_portal eac_br_mock_results_summary --last 24h, comment: "whole dump to bronze"}
      - {run: gridflow transform neso_data_portal eac_br_mock_results_summary --last 24h, comment: "the capture's date to silver"}
  family:
    slug: eac-br-mock-auction-results
    members:
      - dataset: eac_br_mock_results_summary
        differs: "Cleared MW and clearing price per mock auction, product and window"
        request: "GET https://api.neso.energy/datastore/dump/a285483f-d830-4ae2-8b6d-98c05f6d21f3"
        held: Test-run results, not real procurement; NESO does not say if times are UTC or UK local.
      - dataset: eac_br_mock_results_by_unit
        differs: "Winning units' MW and price per window, with participant and technology"
        request: "GET https://api.neso.energy/datastore/dump/7f5a3d87-a3fb-4c5b-88f0-ecba2401834d"
        held: Test-run results, not real procurement; NESO does not say if times are UTC or UK local.
      - dataset: eac_br_mock_results_buy_orders
        differs: "NESO's buy orders per window: quantity, price, status and executed MW"
        request: "GET https://api.neso.energy/datastore/dump/e3ad918b-f10b-49c7-93ba-b7e81fe6feea"
        held: Test-run results, not real procurement; NESO does not say if times are UTC or UK local.
      - dataset: eac_br_mock_results_sell_orders
        differs: "Every provider's sell order, with price limit, status and executed MW"
        request: "GET https://api.neso.energy/datastore/dump/b73e34ca-28fc-4fb2-9275-d5f546d6f33a"
        held: Test-run results, not real procurement; NESO does not say if times are UTC or UK local.
  related:
    - {dataset: neso_data_portal/eac-br-auction-results, note: The real auctions these runs rehearse; never join on auction number}
    - {dataset: neso_data_portal/eac-mock-auction-results, note: "A second mock package, named 2025-2026, for response and the reserve services"}
    - {dataset: neso_data_portal/eac-auction-results, note: "NESO's EAC auctions, which also buy Balancing Reserve"}
---

# EAC-BR Mock Auction Results

This package is NESO's record of the **mock (test-run) auctions for Balancing Reserve (BR)** on the Enduring
Auction Capability (EAC) platform. Balancing Reserve here means service type "Balancing Reserve" (products NBR and PBR) bought through
EAC auctions, with 30-minute delivery intervals (K-AS-4 FACTS section 8). The purpose of the product beyond that is
not documented in the sources used for this page (`TODO: verify`). NESO describes the
resources as the outcome of daily **EAC-BR mock auction runs** (the vendor's own package notes, K-AS-4 FACTS
section 8; NESO [EAC-BR mock auction results](https://www.neso.energy/data-portal/eac-br-mock-auction-results)).
There are four tables, each the mock counterpart of a table in the live archive package (@./eac-br-auction-results.md):
results by unit, buy orders, sell orders and a results summary. They describe what bidders offered and what a
rehearsal of the auction algorithm awarded. **They are not evidence of real procurement, real clearing prices
or real volumes**, and a model must not use them as price or volume history for the live Balancing Reserve
market. Their use is to understand the shape of the BR tables and the auction mechanics.

**The whole package is held, and every output is held twice** (RULINGS 747, 748, 749, 767, 770, 772, 775;
ledger in `.planning/RULINGS.md`, activation in `.planning/v0.22-RESULTS.md` section "AS-4b"):

1. **Package hold, EAC-BR-MOCK-TEST-DATA.** The package is registered `held` so its rows stay unpublished
   until an explicit mock/test label with separate provenance exists, and no consumer joins them to live EAC or
   EAC-BR results on auction id.
2. **Family hold, BR-MOCK-EXPORT-CLOCK.** Each of the four families carries a hold on the unanswered question of
   which clock the mock exports use for their naive time cells.

Held means silver is written and reconciled but **no consumer-facing output is released**. This page therefore
documents the **schema, row counts, clocks and the hold questions only; it states no data values** for any
held family (no sample rows, no value ranges, no counts of blanks or outliers).

**What this package is not.**

- It is **not the live BR archive** (@./eac-br-auction-results.md). The measured mock auction-id sets are
  disjoint from the live archive's ids, but the hold text is explicit that this is a measurement of the captured
  bodies and **not a namespace guarantee**. Never join mock to live on `auction_id`.
- It is **not the live EAC package** (@./eac-auction-results.md), and **not the sibling mock package**
  (@./eac-mock-auction-results.md), whose resources are the Response-Reserve mocks for 2025-2026. This package's
  resources are named "Mock Balancing-Reserve ... 2023-2024". Whether the two mock packages overlap in scope is
  not established: `TODO: verify` before relying on either.
- It is **not a forecast**: no issue time exists or is invented (`issue: none` on every family).
- It is **not a settlement-period table**: there is no `run_type` and no settlement period.

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: EVT

## Files by disposition

All four resources are disposition **SILVER** (a CKAN datastore dump that gridflow parses). There are **no DOC,
HOLD or SKIP resources** in this package, hence no document download links; the only download URLs are the
dump endpoints in the fetch table below. The package id is `c9843f08-bb12-461d-9741-69729fe887a0`.

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| NESO Mock Balancing-Reserve Buy Orders 2023-2024 | CSV | dump | `e3ad918b-f10b-49c7-93ba-b7e81fe6feea` |
| NESO Mock Balancing-Reserve Results By Unit 2023-2024 | CSV | dump | `7f5a3d87-a3fb-4c5b-88f0-ecba2401834d` |
| NESO Mock Balancing-Reserve Results Summary 2023-2024 | CSV | dump | `a285483f-d830-4ae2-8b6d-98c05f6d21f3` |
| NESO Mock Balancing-Reserve Sell Orders 2023-2024 | CSV | dump | `b73e34ca-28fc-4fb2-9275-d5f546d6f33a` |

**Where each resource is fetched from** (sidecar `request_url`, bronze under
`C:/gridflow-data/bronze/neso_data_portal/<family>/2026/10/08/`). Each family has exactly one capture.

| Family | Fetch URL | Bronze capture |
|---|---|---|
| `eac_br_mock_results_buy_orders` | `https://api.neso.energy/datastore/dump/e3ad918b-f10b-49c7-93ba-b7e81fe6feea` | 2026-10-08, 503,081 bytes |
| `eac_br_mock_results_by_unit` | `https://api.neso.energy/datastore/dump/7f5a3d87-a3fb-4c5b-88f0-ecba2401834d` | 2026-10-08, 915,202 bytes |
| `eac_br_mock_results_summary` | `https://api.neso.energy/datastore/dump/a285483f-d830-4ae2-8b6d-98c05f6d21f3` | 2026-10-08, 120,262 bytes |
| `eac_br_mock_results_sell_orders` | `https://api.neso.energy/datastore/dump/b73e34ca-28fc-4fb2-9275-d5f546d6f33a` | 2026-10-08, 4,059,468 bytes |

Vendor dictionaries (human pages):
[mock by unit](https://www.neso.energy/data-portal/eac-br-mock-auction-results/neso_mock_balancing-reserve_results_by_unit_2023-2024),
[mock buy orders](https://www.neso.energy/data-portal/eac-br-mock-auction-results/neso_mock_balancing-reserve_buy_orders_2023-2024),
[mock sell orders](https://www.neso.energy/data-portal/eac-br-mock-auction-results/neso_mock_balancing-reserve_sell_orders_2023-2024),
[mock summary](https://www.neso.energy/data-portal/eac-br-mock-auction-results/neso_mock_balancing-reserve_results_summary_2023-2024).
Saved field info: `.planning/research/neso-snapshots/field-info/20261008T114228Z/eac_br_mock_results_*.json`.

## The two clocks, family by family

Every silver row carries two clocks. They are the same for all four families of this package, and the
**event clock is deliberately empty**:

| Clock | Value in this package |
|---|---|
| **Vintage** (when the data was available) | `available_at` = the **gridflow capture time**, taken from the bronze sidecar `written_at`. The registry vintage is `capture_fallback`: the registry model forbids a `ckan_last_modified` vintage for a datastore-only family (record model rule V-8). The sidecar does record a CKAN `last_modified` for each resource (all four are dated 2024-01-24; the package `metadata_modified` is 2024-11-25), but it is **not used as `available_at`**; it sits only in bronze metadata. Checked in silver on 2026-10-13: `available_at` equals `capture_written_at` on every row of every family. `published_at` is null on every row. |
| **Event time** (what the row is about) | Temporal recipe **`none`**. `timestamp_utc` and `event_time` are **the capture time** (they equal `capture_written_at` on every row of every family, checked in silver on 2026-10-13); they are **not** the delivery window and **not** the order time. This is a deliberate consequence of the open clock question, not a defect. |

Because the recipe is `none`, the vendor's own time cells, `deliveryStart`, `deliveryEnd` and `orderEntryTime`,
are kept as **raw `string` columns**, byte-for-byte as served. They are naive (no offset). **The clock is
undocumented**: neither the package nor its dictionaries state it, and the live EAC package's UTC declaration
does not extend to this mock package (BR-MOCK-EXPORT-CLOCK below). Do not parse them as UTC and do not parse
them as UK local time. Their roles are known from the vendor dictionaries: `deliveryStart` is the time from
which delivery of the auction product commences, `deliveryEnd` the time delivery ends, `orderEntryTime` when the
bid was submitted (a submission time, not the publication time of the outcome columns).

| Family | Vintage clock | Event clock |
|---|---|---|
| `eac_br_mock_results_buy_orders` | `capture_fallback` (capture time) | `none`: `timestamp_utc` is the capture time |
| `eac_br_mock_results_by_unit` | `capture_fallback` | `none`: `timestamp_utc` is the capture time |
| `eac_br_mock_results_sell_orders` | `capture_fallback` | `none`: `timestamp_utc` is the capture time |
| `eac_br_mock_results_summary` | `capture_fallback` | `none`: `timestamp_utc` is the capture time |

## Units and sentinels

**Units come only from the vendor's own dictionaries for these mock resources** (saved field info, K-AS-4
FACTS section 8 and g4); none is inferred from a column name.

| Columns | Unit (vendor dictionary) |
|---|---|
| `quantity`, `executed_quantity`, `cleared_volume` | **MW** |
| `price`, `price_limit`, `clearing_price` | **£/MW/h** (cleared price per MW per hour). This is a per-MW-per-hour capacity price, not £/MWh. |
| `acceptance_ratio` | dimensionless **proportion** (the matched share of an offered or bid quantity); not a percentage |
| `auction_id`, `order_id`, `basket_id`, `product_id`, `looped_basket_id`, `substitutability_family`, `joined_family`, `unit_result_id`, `reason_rejected` | identifiers, linking labels or codes: no physical unit |
| `delivery_start`, `delivery_end`, `order_entry_time` | time labels: held, see the clocks above. The vendor dictionary unit for the by-unit times is "ISO8601" / "ISO 8601" (a format, not a clock). |

Nothing is converted or rescaled.

**Typing and sentinels (K-AS-4 FACTS g5).** Identifiers are `string`, byte-equal and never cast; `reason_rejected`
is a code and stays `string`. Quantities, prices and the acceptance ratio are `float64`. **Zeros are real values
and stay zero, and blanks stay null.** FACTS found **no `NA`/`N/A` token, no `-1` sentinel, no thousands
separator, percent sign or padded number** in any body of this package, and the production CSV reader agreed
with a strict second parse on every row and cell, so **no token is mapped to null, nothing is trimmed and no
bound is applied** in any record (no price floor or ceiling, no range on the acceptance ratio). All four bodies
are strictly valid UTF-8, and each is read under `encoding: utf-8`.

## Families

Column meanings are those of the live BR archive package; read @./eac-br-auction-results.md for the full
column-by-column description, since the mock headers are **identical** to the live BR archive headers (by unit,
buy orders, summary and the 20-column sell-orders header), in the BR body's own column order (the buy-order
header places `joinedFamily` before `substitutabilityFamily`, and the summary has no `linkedServiceWindowID`).
Not all mock facts carry over: the live package's eligibility does not.

All four families are `refresh: frozen` in the registry: the vendor notice says the mock results were scheduled
to be published only for a short window in February 2024 (see Cadence), and each family has one capture.

### `eac_br_mock_results_buy_orders`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

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

- Entity key: `auction_id`, `order_id`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

One row per submitted mock buy order. Resource `e3ad918b-f10b-49c7-93ba-b7e81fe6feea`, one capture
(2026-10-08). **Silver: 3,696 rows**; one Parquet file under
`C:/gridflow-data/silver/neso_data_portal/eac_br_mock_results_buy_orders/year=2026/month=10/` (the partition is
the capture date), with the 17 vendor columns then `timestamp_utc`, `published_at`, `bronze_capture_id`,
`capture_written_at`, `event_time`, `available_at`, `source_run_id`, `dataset_version` (25 columns). Held:
BR-MOCK-EXPORT-CLOCK (and the package hold). The composite key is unique in the body (FACTS) and was preferred
to `order_id` alone; the vendor guarantees no key, and order identity across later corrected exports is
undocumented, so `_latest` is `whole_capture`, never `key_latest` (`TODO: verify` order identity across
re-exports). `joined_family` is a nullable `string`.

### `eac_br_mock_results_by_unit`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

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

One row per mock accepted unit result. Resource `7f5a3d87-a3fb-4c5b-88f0-ecba2401834d`, one capture
(2026-10-08). **Silver: 7,074 rows**; one Parquet file under
`C:/gridflow-data/silver/neso_data_portal/eac_br_mock_results_by_unit/year=2026/month=10/`, the 11 vendor
columns then the 8 metadata columns (19). Held: BR-MOCK-EXPORT-CLOCK (and the package hold). The identifier
`unit_result_id` is nonblank and unique across the body; this is a vendor-described unique identifier, but the
vendor does not guarantee it across later exports (`TODO: verify`). The unit-level party and technology fields
are free text kept as published. This table does not have an order column, so it does not join to the buy or
sell tables on a documented key: `TODO: verify` before linking by unit or auction.

### `eac_br_mock_results_sell_orders`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

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

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

One row per mock sell-order element, retaining the parent, child and substitutable-child structure of the
auction; the basket and looped-basket ids link those elements and are optional text. Resource
`b73e34ca-28fc-4fb2-9275-d5f546d6f33a`, one capture (2026-10-08). **Silver: 23,263 rows**; one Parquet file
under `C:/gridflow-data/silver/neso_data_portal/eac_br_mock_results_sell_orders/year=2026/month=10/`, the 20
vendor columns then the 8 metadata columns (28). Held: BR-MOCK-EXPORT-CLOCK (and the package hold). The
composite key is unique in the body (FACTS). This body is the only real vendor bytes with the 20-column
sell-orders header that existed when the live BR sell-orders record was written, so its rows were used (and
labelled mock) only to exercise that shared header in the unit tests; they are not live BR evidence
(K-AS-4b SPEC ruling 8). `reason_rejected` is a code and stays a `string`.

### `eac_br_mock_results_summary`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

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

- Entity key: `auction_id`, `auction_product`, `delivery_start`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

One row per mock auction, product and delivery window. Resource `a285483f-d830-4ae2-8b6d-98c05f6d21f3`, one
capture (2026-10-08). **Silver: 1,632 rows**; one Parquet file under
`C:/gridflow-data/silver/neso_data_portal/eac_br_mock_results_summary/year=2026/month=10/`, the 7 vendor
columns then the 8 metadata columns (15). Held: BR-MOCK-EXPORT-CLOCK (and the package hold). The key keeps
`auction_id` and includes the raw string `delivery_start`, so two equal instants written differently would be
different keys: do not normalise the string until the clock is settled. The key is unique in the body (FACTS).

## Cadence

- Registry refresh: frozen
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Daily
- Vendor notice (package description): the mock results are "scheduled to be published on this page from 14th-23rd
  February 2024 only". The "Daily" metadata and this notice disagree, and the registry hold question records
  that the captured dates run beyond the notice's February window. All captured rows are kept and none is clipped
  to the notice window. `TODO: BR-MOCK-NOTICE-SCOPE` (non-holding): ask NESO whether later runs were added and
  whether the notice describes only an initial campaign.
- gridflow captured each resource once on 2026-10-08; the resources' CKAN `last_modified` is 2024-01-24, so
  nothing newer than the January 2024 resource update is known. Amendment and deletion behaviour between
  captures is unmeasured (one capture each): `TODO: verify`.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

## Holds

- package: held: TODO: EAC-BR-MOCK-TEST-DATA — NESO publishes these resources as outcomes of EAC-BR mock auction runs, not live Balancing Reserve procurement; publish only under an explicit mock/test label with separate provenance, and never join them to live EAC or EAC-BR results on auction id (the measured mock id sets are disjoint from the 596 BR archive ids, which is not a namespace guarantee). (unit v0.22-K-AS-4b)
- `eac_br_mock_results_buy_orders`: held: TODO: EAC-BR-MOCK-TEST-DATA — NESO publishes these resources as outcomes of EAC-BR mock auction runs, not live Balancing Reserve procurement; publish only under an explicit mock/test label with separate provenance, and never join them to live EAC or EAC-BR results on auction id (the measured mock id sets are disjoint from the 596 BR archive ids, which is not a namespace guarantee). (unit v0.22-K-AS-4b)
- `eac_br_mock_results_by_unit`: held: TODO: EAC-BR-MOCK-TEST-DATA — NESO publishes these resources as outcomes of EAC-BR mock auction runs, not live Balancing Reserve procurement; publish only under an explicit mock/test label with separate provenance, and never join them to live EAC or EAC-BR results on auction id (the measured mock id sets are disjoint from the 596 BR archive ids, which is not a namespace guarantee). (unit v0.22-K-AS-4b)
- `eac_br_mock_results_sell_orders`: held: TODO: EAC-BR-MOCK-TEST-DATA — NESO publishes these resources as outcomes of EAC-BR mock auction runs, not live Balancing Reserve procurement; publish only under an explicit mock/test label with separate provenance, and never join them to live EAC or EAC-BR results on auction id (the measured mock id sets are disjoint from the 596 BR archive ids, which is not a namespace guarantee). (unit v0.22-K-AS-4b)
- `eac_br_mock_results_summary`: held: TODO: EAC-BR-MOCK-TEST-DATA — NESO publishes these resources as outcomes of EAC-BR mock auction runs, not live Balancing Reserve procurement; publish only under an explicit mock/test label with separate provenance, and never join them to live EAC or EAC-BR results on auction id (the measured mock id sets are disjoint from the 596 BR archive ids, which is not a namespace guarantee). (unit v0.22-K-AS-4b)

The skeleton above repeats the package hold on every family because the package hold dominates in the
eligibility report (`docs/neso_data_portal/eligibility.md`). The registry records, in addition, a **family-level
hold on each of the four families** (unit `v0.22-K-AS-4b`):

- `eac_br_mock_results_buy_orders`, `eac_br_mock_results_by_unit`, `eac_br_mock_results_sell_orders`,
  `eac_br_mock_results_summary`: held: TODO: BR-MOCK-EXPORT-CLOCK — the EAC-BR mock package and its dictionaries do
  not state the clock of the naive deliveryStart / deliveryEnd / orderEntryTime cells, the live EAC package's UTC
  declaration does not extend to it, and the captured dates span February–September 2024 (both GMT and BST), so
  the clock cannot be inferred; which clock do the mock exports use? (Mock / test data, not procurement results.)

**What would release the output.**

- *BR-MOCK-EXPORT-CLOCK* needs a mock-specific statement of the export clock, or a vendor API specification
  expressly covering the mock environment. The captured dates cross both GMT and BST, so a reading cannot be
  inferred from the data. Until it is answered the time cells stay raw strings and the event recipe stays `none`.
  The live Balancing Reserve archive has its own, separate clock question (below): it is not answered by, and does
  not answer, this one.
- *EAC-BR-MOCK-TEST-DATA* needs an explicit mock/test label and separate provenance for any published mock row, and
  a guarantee that no consumer joins mock to live on `auction_id`. This hold stays even after the clock question is
  answered.

**Open questions that do not hold any output** (carried as `TODO: verify`):

- The **original publication instant** of the mock results. The vintage is the capture time, never a publication time.
- **Order and result identity across corrected re-exports**, and the **amendment and deletion behaviour** of the
  dumps (one capture each).
- **Interval closure**: no source states whether a window's end instant belongs to it.
- `TODO: BR-MOCK-NOTICE-SCOPE` (see Cadence).
- Whether this package duplicates or complements the sibling mock package (see the top of the page).

## Known issues and gotchas

- **Mock, not procurement.** These rows are rehearsal outcomes. Any published use needs the explicit mock/test
  label and separate provenance (EAC-BR-MOCK-TEST-DATA).
- **Do not join to the live package on `auction_id`.** The measured id sets of the four mock families are
  disjoint from the live BR archive's 596 auction ids. Separately, the live BR archive's entity keys and auction-id
  sets are measured disjoint from the live EAC main and FY archives (K-AS-4 FACTS AS-4-d), and the BR sell-orders
  capture had 0 overlap with AS-3 `eac_results_sell_orders` (RULINGS 772). That is a measurement of the captured bodies, not a
  guarantee that the mock environment will never reuse a live id.
- **The time clock is undocumented, and the time cells are raw strings.** The live BR archive pages state the same
  of their own time cells ("clock undocumented, raw strings"); the newer live EAC package's UTC declaration is not
  transferred to either.
- **`timestamp_utc` is the capture time, not an event time.** Filtering these tables by `timestamp_utc` filters by
  when gridflow fetched them (a single instant per family today), never by delivery date.
- **The summary entity key includes a raw string `delivery_start`.** Do not normalise it until the clock is
  settled.
- **Held means unpublished.** Silver exists and reconciles, but no gold, chart, front-end page or model input may
  use these rows.

## Implementation delta

Where the code or a source differs from the docs or from another source:

- **Skeleton hold text** names the package question on every family; the frozen records carry BR-MOCK-EXPORT-CLOCK
  at family level (above). No code change implied.
- **Vintage clock.** The docs-wave brief for this page described the vintage as the CKAN `last_modified`; the
  registry and silver use `capture_fallback` (capture time) because the record model forbids a
  `ckan_last_modified` vintage for a datastore-only family. The silver check confirms capture time. The CKAN
  value stays in the bronze sidecar only. The page follows the code and silver.
- **Event time is the capture time** for all four families by design (recipe `none`): the code does not interpret
  the vendor's time cells.
- **Vendor update frequency** ("Daily") versus the vendor notice (a short February 2024 window) versus the
  registry (`frozen`): documented under Cadence; the registry follows the evidence of one capture and a 2024
  resource update.
- **Download cap**: the registry sets `max_download_bytes` 536,870,912 on all four mock families; the largest
  mock body is 4,059,468 bytes, so the cap is not a concern for this package. (The live BR archive's sell-orders
  family has a raised cap of 805,306,368, which does not apply here.)

## Activation receipt

AS-4b merged as PR #117 (`e3d6908`), triple-green (RULINGS 767). Activation on 2026-10-13 with
`--start/--end 2026-10-08` and no prior silver (`phases/v0.22-K-AS-4/post-merge/transform.log`, RULINGS 770):
the four mock families wrote **7,074 + 3,696 + 23,263 + 1,632 = 35,665** rows, each equal to the spec plan, with
zero validation failures and zero rows excluded. Together with the live BR archive's three captured tables, the
seven activated families wrote 812,584 rows. Reconcile `--all --cutoff 2026-10-13` exited 0 over 206 families
with 0 gaps (RULINGS 775; `.planning/v0.22-RESULTS.md` section "AS-4b"); the coverage run reports 0 missing
resources, and its six unfrozen keys are none of this package's families. The package holds 0 eligible families
and 4 held-with-silver (eligibility report).

## Links

- Sibling live archive: @./eac-br-auction-results.md
- Live EAC package: @./eac-auction-results.md
- Sibling mock package (Response-Reserve): @./eac-mock-auction-results.md
- Vendor index: @../README.md, @../coverage.md
- GB balancing context: @../../../20-domain/markets/gb-balancing-mechanism.md
- Evidence in the gridflow repo: `.planning/phases/v0.22-K-AS-4/K-AS-4-FACTS.md` (sections 1, 2.6, 8, 9),
  `K-AS-4b-SPEC.md`, `.planning/RULINGS.md` (738, 747, 748, 749, 767, 770, 772, 775), `.planning/v0.22-RESULTS.md`
  ("AS-4b")
