---
source: "neso_data_portal"
package: "eac-auction-results"
dataset_keys: ["eac_results_buy_orders", "eac_results_buy_orders_fy", "eac_results_by_unit", "eac_results_by_unit_fy", "eac_results_daily_buy_orders", "eac_results_daily_by_unit", "eac_results_daily_sell_orders", "eac_results_daily_summary", "eac_results_sell_orders", "eac_results_summary", "eac_results_summary_fy"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-13
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Enduring Auction Capability (EAC) auction results

This package is NESO's **auction-results record for the Enduring Auction Capability (EAC)**, the
platform through which NESO now buys its **response services (Dynamic Containment DC, Dynamic Moderation
DM, Dynamic Regulation DR)** and its **reserve services (Balancing Reserve BR, Quick Reserve QR, Slow
Reserve SR)**. The vendor's package text says the daily auction results are published here and that
datetime values (for example `deliveryStart` and `deliveryEnd`) are provided **in UTC rather than local
time** (CKAN package `notes`,
@.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json; NESO
[EAC auction results](https://www.neso.energy/data-portal/eac-auction-results)). Each auction clears a set
of **auction products** (the dictionary lists the codes `DCH, DCL, DMH, DML, DRH, DRL, NSR, PSR, NQR, PQR`)
for **delivery windows** of one delivery day: the response products clear mostly in four-hour windows, the
reserve products in half-hour windows (measured, see Known issues). The tables answer: which participants
and units bid what volume at what price, which bids the auction accepted, and what the clearing price and
cleared volume were per product and window. For a model they are the **price-and-volume outcome of the
ancillary-services market**: clearing price per product per window (the target), cleared volume, and
unit-level winners with their technology type.

**What this package is not.**

- It is a set of **event results, not forecasts**: they record what was bid and what the auction awarded
  for windows that have been auctioned. No forecast issue time is used (`issue: none` on every family),
  and no forecast exemption applies.
- It is **not a settlement-period table**: there is no `run_type` and none is fabricated. The windows are
  the product delivery windows given by `delivery_start` and `delivery_end`.
- It is **not the Balancing Reserve history before September 2025** and **not the Response history before
  November 2023**: the vendor points to separate packages for those (the EAC BR auction results package
  and the Dynamic Containment data package). It is **not the mock auction results**: those are a different
  NESO package (`eac-mock-auction-results`), a test environment that re-uses small auction numbers, and
  must never be joined to these tables on `auction_id` (K-AS-3 FACTS section 4.1). The mock package
  is documented separately.

**Eleven families, built from four table kinds in three scopes.** Every table kind appears in a
**current** scope (a CKAN datastore dump, or for sell orders a dump plus monthly archives), an **FY
archive** scope where the vendor splits history by financial year, and a **daily** scope that holds the
latest auction only (the vendor added the four daily files and says they populate from 5 May 2026).

| Table kind | Current | FY / monthly archive | Daily (latest auction only) |
|---|---|---|---|
| Results by unit (one row per accepted unit result) | `eac_results_by_unit` | `eac_results_by_unit_fy` | `eac_results_daily_by_unit` |
| Buy orders (one row per submitted buy order) | `eac_results_buy_orders` | `eac_results_buy_orders_fy` | `eac_results_daily_buy_orders` |
| Results summary (one row per auction, product and window) | `eac_results_summary` | `eac_results_summary_fy` | `eac_results_daily_summary` |
| Sell orders (one row per order, parent, child or substitutable child) | `eac_results_sell_orders` (dump plus 35 monthly archives) | (inside `eac_results_sell_orders`) | `eac_results_daily_sell_orders` |

All eleven families are **eligible** (RULINGS 738) and **none is held**; the package is eligible with
36,335,448 silver rows (RULINGS 741, 742). Current, FY and daily families are **separate records**.
Measured keys are disjoint between the current segment and the FY archives, and each daily file repeats
the latest-auction slice of its current counterpart (section Known issues). So **gridflow never merges or
sums across the three scopes**, and a consumer must never add a daily family to its current counterpart:
that double counts the latest auction.

**Delivery span of each scope (silver, delivery starts).** Current by-unit, buy-order and summary dumps:
`2026-03-31T22:00:00` to `2026-10-08T21:30:00`. FY archives (FY2023, FY2024, FY2025 as the vendor labels
them): `2023-11-02T23:00:00` to `2026-03-31T21:30:00`, with the three resources covering
`2023-11-02`-`2024-03-31`, `2024-03-31`-`2025-03-31` and `2025-03-31`-`2026-03-31` by delivery start. The
current sell-order dump covers only `2026-09-30T22:00:00` to `2026-10-08T21:30:00` (8 auctions), the 35
monthly archives `2023-11-02T23:00:00` to `2026-09-30T21:30:00`. Daily files: `2026-10-07T22:00:00` to
`2026-10-08T21:30:00`, **one delivery day** (the buy-order, summary and sell-order daily files hold a single auction ID). Over the complete summary tables there are
**1,071 auction IDs and 1,071 delivery days**, no auction maps to more than one delivery day and no day
to more than one auction (K-AS-3 FACTS section 3.5; a measured property, not a vendor guarantee).
`auctionID` is an opaque identifier and **not** a date code: auction `2661` is the auction for delivery
day 2026-04-01 and `2676` for 2026-04-02.

**Column meanings (vendor dictionary).** From NESO's saved field info
(@.planning/research/neso-snapshots/field-info/20261008T114228Z/eac_results_by_unit.json,
`eac_results_buy_orders.json`, `eac_results_summary.json`, `eac_results_sell_orders.json`; the FY and
daily families share their counterpart's header exactly).

- **Results by unit.** `registeredAuctionParticipant`: name of the participant who submitted the bid, free
  text. `auctionUnit`: the unit identifier, a collection of one or more eligible assets registered as an
  auction unit (example `AG-GEDF02`); kept as served. `serviceType` and
  `auctionProduct`: the service and product. `executedQuantity`: volume accepted at the clearing price,
  MW. `clearingPrice`: cleared price per MW per hour, £/MW/h. `deliveryStart` and `deliveryEnd`: the time
  from which delivery commences and ends (the dictionary unit is ISO 8601). `technologyType` (optional,
  for example `Batteries`) and `postCode` (optional): free text, blank when absent. `unitResultID`: the unique
  identifier of the unit result record; the values are `#||#`-joined strings such as
  `2661#||#2710#||#PSR#||#150423`. The components are not documented: store as served and do not split
  (`TODO: verify` the composition).
- **Buy orders.** `auctionID`: unique auction identifier. `orderID`: the ID of the submitted bid, generated
  by EAC. `quantity`: the total volume of the bid, MW. `price`: a price indicating the willingness to
  pay to procure the quantity, £/MW/h. `substitutabilityFamily` (optional) and `joinedFamily` (optional, a
  linked order marking which service windows are looped): linking identifiers.
  `paradoxicallyAcceptanceAllowed`: whether the order can be paradoxically accepted, served as a text
  flag. `orderEntryTime`: when the bid was submitted. `acceptanceRatio`: a number between 0 and 1
  giving the proportion matched by the auction algorithm. `status`: the dictionary lists
  `EXECUTED, REJECTED, EXCLUDED`. `executedQuantity` (MW), `clearingPrice` (£/MW/h) and `reasonRejected`
  (optional, "Reason Codes") are the outcome columns.
- **Results summary.** `auctionID`, `auctionProduct`, `serviceType`, `deliveryStart`, `deliveryEnd`;
  `clearedVolume`: volume of the product accepted at the clearing price, MW; `clearingPrice`: £/MW/h;
  `linkedServiceWindowID` (optional): which service windows of one service (for example QR or BR) have
  been linked together for consistency over particular periods.
- **Sell orders.** `auctionID`, `registeredAuctionParticipant`, `auctionUnit`, `basketID` (the basket bid
  ID generated by EAC), `serviceType`, `deliveryStart`, `deliveryEnd`, `orderID`, `orderType` (the
  dictionary lists `PARENT, CHILD, SUBSTITUTABLECHILD`), `auctionProduct`, `productID` (identifier of each
  product offered within an auction ID), `quantity` (MW), `priceLimit` (the price for providing the
  service, £/MW/h), `loopedBasketID` (optional; blank for a child or substitutable child and for a
  basket not looped to another), `orderEntryTime`, `acceptanceRatio`, `status`, `executedQuantity` (MW),
  `clearingPrice` (£/MW/h), `reasonRejected` (optional), `flexibleGroupID` (optional: a participant's
  flexible service-window group linked for one auction and service) and `minimumConsecutiveWindows`
  (optional: the minimum number of consecutive windows that can be accepted from that group).

**Units (vendor dictionary only).** Volumes and quantities (`quantity`, `executedQuantity`,
`clearedVolume`) are **MW**; prices (`price`, `priceLimit`, `clearingPrice`) are **£/MW/h**, the vendor's
own stated unit (the neighbouring Static FFR results use £/MWh, so do not carry one convention across).
`acceptanceRatio` is a **dimensionless fraction** (a proportion, not a percentage). `minimumConsecutiveWindows` is a
**count** of windows. Every `...ID`, `...Family` and `...Type` column is an identifier or label with no
unit. Nothing is converted or rescaled, and no MW-to-energy conversion is stated or applied.

**Typing and sentinels (K-AS-3 FACTS g5, g6).** Identifiers are `string`, byte-equal and never cast
(`auctionID` is opaque). Zeros are real values and stay zero; blanks stay null (basket, linking and window
IDs, `reasonRejected`, `technologyType`, `postCode`). **A price of -1 is a signed price, not a sentinel**:
it stays `-1.0` and is never nulled (counts per family below). No `NA`/`N/A` token, thousands
separator, percent sign or padded number occurs in any body of this package, and the production CSV reader
agreed with a strict second parse on every row and cell. There is no price floor or ceiling in the
record, and `acceptanceRatio` has **no upper bound**.

**Where the tables meet.** The natural join between kinds is `auction_id` (+ `auction_product` +
`delivery_start` for the summary). Results by unit has **no `auctionID` column**, only `unitResultID`.
Place a unit result inside an auction through the explicit delivery fields, not by decoding the opaque
identifier. Related requirement and result pages:
@./balancing-reserve-auction-requirement-forecast.md, @./quick-reserve-auction-requirement-forecast.md,
@./slow-reserve-requirement-forecast.md, @./dynamic-moderation-requirements.md,
@./dynamic-regulation-requirements.md and, for the neighbouring Static FFR auction,
@./static-firm-frequency-response-auction-results.md.

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: EVT

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| NESO Response-Reserve Buy Orders | CSV | dump | `1cf68f59-8eb8-4f1d-bccf-11b5a47b24e5` |
| NESO Response-Reserve Buy Orders FY2023 (Archive) | CSV | upload | `7a2d64a5-3233-4ee2-92fd-240db03717f1` |
| NESO Response-Reserve Buy Orders FY2024 (Archive) | CSV | upload | `c6f09570-58f9-4e04-81c3-2c99af2fded0` |
| NESO Response-Reserve Buy Orders FY2025 (Archive) | CSV | upload | `270a5e1d-ea44-43a0-82b1-703fdaa354ac` |
| NESO Response-Reserve Daily Buy Orders | CSV | upload | `e638cf3d-bed1-42ae-a984-8fe3c556febf` |
| NESO Response-Reserve Daily Results By Unit | CSV | upload | `07f0dd8b-4471-4e2e-9ed6-d21b0ce1f6f5` |
| NESO Response-Reserve Daily Results Summary | CSV | upload | `3c51a666-1c33-450e-a6eb-c9b4a0c91584` |
| NESO Response-Reserve Daily Sell Orders | CSV | upload | `8ba48f26-d73e-4094-a90d-ba075eb739c1` |
| NESO Response-Reserve Results By Unit | CSV | dump | `a63ab354-7e68-44c2-ad96-c6f920c30e85` |
| NESO Response-Reserve Results By Unit FY2023 (Archive) | CSV | upload | `7505ec16-e1e7-432e-8abd-a554e03e4f02` |
| NESO Response-Reserve Results By Unit FY2024 (Archive) | CSV | upload | `2fc9dd7e-5274-40e3-abf4-6d31b30f21c6` |
| NESO Response-Reserve Results By Unit FY2025 (Archive) | CSV | upload | `c312358e-87da-480e-88cc-d45c1dce1b41` |
| NESO Response-Reserve Results Summary | CSV | dump | `596f29ac-0387-4ba4-a6d3-95c243140707` |
| NESO Response-Reserve Results Summary FY2023 (Archive) | CSV | upload | `be5c6b0d-a335-4859-93f2-389585b4e9a1` |
| NESO Response-Reserve Results Summary FY2024 (Archive) | CSV | upload | `ab130833-3ce4-4361-90fb-69fa3cf30f15` |
| NESO Response-Reserve Results Summary FY2025 (Archive) | CSV | upload | `be55ee51-b79e-47da-b71e-a0f8865d9d66` |
| NESO Response-Reserve Sell Orders | CSV | dump | `13b511df-d6ec-4143-afb1-0ecc6fd19810` |
| NESO Response-Reserve Sell Orders 202311 (Archive) | CSV | upload | `3780a81e-bee4-43e2-9ebe-ef85d2ba18de` |
| NESO Response-Reserve Sell Orders 202312 (Archive) | CSV | upload | `66bde1bc-1e81-4d91-b022-ae0f072020b6` |
| NESO Response-Reserve Sell Orders 202401 (Archive) | CSV | upload | `5901ba21-44e3-4f22-922b-e759f9930f92` |
| NESO Response-Reserve Sell Orders 202402 (Archive) | CSV | upload | `301443b5-2629-482f-8904-d73cdffffc69` |
| NESO Response-Reserve Sell Orders 202403 (Archive) | CSV | upload | `f588ba39-c449-4879-93f5-e771b85c93dc` |
| NESO Response-Reserve Sell Orders 202404 (Archive) | CSV | upload | `85690ec6-741b-4853-840c-7afe70da3e79` |
| NESO Response-Reserve Sell Orders 202405 (Archive) | CSV | upload | `1b31276c-31a1-46ce-8579-52c4444ccc95` |
| NESO Response-Reserve Sell Orders 202406 (Archive) | CSV | upload | `fb1ed018-e6c3-4032-a08a-7abd4d4fb150` |
| NESO Response-Reserve Sell Orders 202407 (Archive) | CSV | upload | `91f2ad1c-c592-4bbb-8c3b-d5ace1d7a32a` |
| NESO Response-Reserve Sell Orders 202408 (Archive) | CSV | upload | `f62d283f-66e0-4e71-8e8e-b58c31bf8746` |
| NESO Response-Reserve Sell Orders 202409 (Archive) | CSV | upload | `3aa319e4-21bb-4f69-be63-05144ddca6b4` |
| NESO Response-Reserve Sell Orders 202410 (Archive) | CSV | upload | `7cee44eb-0668-489c-9a0f-fef5f5d7fa50` |
| NESO Response-Reserve Sell Orders 202411 (Archive) | CSV | upload | `39c7648c-d43b-4ef9-b689-a82619245cda` |
| NESO Response-Reserve Sell Orders 202412 (Archive) | CSV | upload | `0a6325b9-1b78-4ee2-a1a0-647aa3b6d014` |
| NESO Response-Reserve Sell Orders 202501 (Archive) | CSV | upload | `3c03d431-7f94-4009-903d-8a4df1aea9f4` |
| NESO Response-Reserve Sell Orders 202502 (Archive) | CSV | upload | `5997f602-24f1-4f44-aa36-c7b898229d60` |
| NESO Response-Reserve Sell Orders 202503 (Archive) | CSV | upload | `02c3ede4-6909-4c7b-9b77-511c774decb2` |
| NESO Response-Reserve Sell Orders 202504 (Archive) | CSV | upload | `57340708-6f3a-429b-8ede-682df3c86709` |
| NESO Response-Reserve Sell Orders 202505 (Archive) | CSV | upload | `069a047e-5b0a-4d27-83fa-f45e451661e3` |
| NESO Response-Reserve Sell Orders 202506 (Archive) | CSV | upload | `e0b50ef5-b37f-46ad-8eb2-17ab0eedb6d1` |
| NESO Response-Reserve Sell Orders 202507 (Archive) | CSV | upload | `81a9700a-6fcd-4c26-ab3b-965d771bfa2c` |
| NESO Response-Reserve Sell Orders 202508 (Archive) | CSV | upload | `d4bc27fe-45a1-43c4-b469-f5f1ba5824ed` |
| NESO Response-Reserve Sell Orders 202509 (Archive) | CSV | upload | `f8db9239-1f96-42ad-bab9-d2ef60c52e1e` |
| NESO Response-Reserve Sell Orders 202510 (Archive) | CSV | upload | `a6ce3d85-4cdd-4276-b23b-01b160f49164` |
| NESO Response-Reserve Sell Orders 202511 (Archive) | CSV | upload | `8adbb902-6029-4af7-b8dd-e1e500aaaa51` |
| NESO Response-Reserve Sell Orders 202512 (Archive) | CSV | upload | `eaa6961f-87c2-483a-94a2-7d6247c7e994` |
| NESO Response-Reserve Sell Orders 202601 (Archive) | CSV | upload | `b155f068-e10f-4c6e-8960-a2cb2806ae13` |
| NESO Response-Reserve Sell Orders 202602 (Archive) | CSV | upload | `4e5c9a3c-77c6-4709-abdd-236353451771` |
| NESO Response-Reserve Sell Orders 202603 (Archive) | CSV | upload | `5531d313-cab5-4f02-9eda-d0242a62d984` |
| NESO Response-Reserve Sell Orders 202604 (Archive) | CSV | upload | `45d867bb-eccb-4a60-8618-74316aafde5a` |
| NESO Response-Reserve Sell Orders 202605 (Archive) | CSV | upload | `654c9fcd-9d0b-42c5-bac7-9fa245b5f99d` |
| NESO Response-Reserve Sell Orders 202606 (Archive) | CSV | upload | `85272de8-2fd7-4578-ae4b-55da74629841` |
| NESO Response-Reserve Sell Orders 202607 (Archive) | CSV | upload | `fc52a1fa-6ce5-4c35-a661-be1b49c1c48f` |
| NESO Response-Reserve Sell Orders 202608 (Archive) | CSV | upload | `aeef326a-9379-4263-a7cd-63c5e4fb0911` |
| NESO Response-Reserve Sell Orders 202609 (Archive) | CSV | upload | `06f4396f-d222-477d-85ad-916ac0662630` |

The package has **52 resources and no DOC resources**; every resource is CSV and carries the disposition
SILVER (the generated table above). Four are CKAN **datastore dumps** (`url_type` datastore: the three
current by-unit, buy-order and summary tables and the current sell-order table) and 48 are CKAN
**uploads**. The datastore rows link to the dump endpoint that gridflow fetched; the upload rows link to
the file URL recorded in the capture sidecar. Each upload's file name is chosen by NESO and may be
replaced when it re-uploads, so a link records what was fetched and is not a permanent address. Package
page: [eac-auction-results](https://www.neso.energy/data-portal/eac-auction-results). Bytes, rows and
`last_modified` come from the capture sidecars under
`C:/gridflow-data/bronze/neso_data_portal/<family>/2026/10/08/` and from the hash-pinned bodies
(K-AS-3 FACTS section 2: captures L1 to L52). **Every resource has exactly one capture**, all written on
**2026-10-08** between 10:28Z and 10:36Z, so successive-capture behaviour (amendment, deletion) is
unmeasured.

**CKAN `last_modified` of a datastore dump is stale and is not used as the vintage.** For the four
dumps it reads 2026-04-15 (by unit, buy orders, summary) and 2026-10-01 (sell orders), while their rows
run to delivery 2026-10-08. A family holding a datastore resource therefore takes the gridflow capture
time as its vintage (record rule V-8); upload-only families take the upload's `last_modified`.

**Current results by unit** (`eac_results_by_unit`):

| Resource | Id | Download | Bytes | Data rows | CKAN `last_modified` |
|---|---|---|---:|---:|---|
| NESO Response-Reserve Results By Unit | `a63ab354-7e68-44c2-ad96-c6f920c30e85` | [datastore dump](https://api.neso.energy/datastore/dump/a63ab354-7e68-44c2-ad96-c6f920c30e85) | 218,717,646 | 1,444,630 | 2026-04-15T11:43:07.338503 |

**FY results by unit** (`eac_results_by_unit_fy`):

| Resource | Id | Download | Bytes | Data rows | CKAN `last_modified` | Delivery starts (first to last) |
|---|---|---|---:|---:|---|---|
| NESO Response-Reserve Results By Unit FY2023 (Archive) | `7505ec16-e1e7-432e-8abd-a554e03e4f02` | [neso-response-reserve-results-by-unit-fy2023-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/7505ec16-e1e7-432e-8abd-a554e03e4f02/download/neso-response-reserve-results-by-unit-fy2023-archive.csv) | 22,015,241 | 161,252 | 2026-04-15T11:14:07.744257 | 2023-11-02T23:00:00 to 2024-03-31T18:00:00 |
| NESO Response-Reserve Results By Unit FY2024 (Archive) | `2fc9dd7e-5274-40e3-abf4-6d31b30f21c6` | [neso-response-reserve-results-by-unit-fy2024-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/2fc9dd7e-5274-40e3-abf4-6d31b30f21c6/download/neso-response-reserve-results-by-unit-fy2024-archive.csv) | 79,395,667 | 563,041 | 2026-04-15T11:18:09.202266 | 2024-03-31T22:00:00 to 2025-03-31T21:30:00 |
| NESO Response-Reserve Results By Unit FY2025 (Archive) | `c312358e-87da-480e-88cc-d45c1dce1b41` | [neso-response-reserve-results-by-unit-fy2025-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/c312358e-87da-480e-88cc-d45c1dce1b41/download/neso-response-reserve-results-by-unit-fy2025-archive.csv) | 170,512,661 | 1,176,445 | 2026-04-15T11:22:51.072165 | 2025-03-31T22:00:00 to 2026-03-31T21:30:00 |

**Daily results by unit** (`eac_results_daily_by_unit`):

| Resource | Id | Download | Bytes | Data rows | CKAN `last_modified` |
|---|---|---|---:|---:|---|
| NESO Response-Reserve Daily Results By Unit | `07f0dd8b-4471-4e2e-9ed6-d21b0ce1f6f5` | [neso-response-reserve-daily-results-by-unit.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/07f0dd8b-4471-4e2e-9ed6-d21b0ce1f6f5/download/neso-response-reserve-daily-results-by-unit.csv) | 1,182,864 | 7,925 | 2026-10-07T13:49:22.409022 |

**Current buy orders** (`eac_results_buy_orders`):

| Resource | Id | Download | Bytes | Data rows | CKAN `last_modified` |
|---|---|---|---:|---:|---|
| NESO Response-Reserve Buy Orders | `1cf68f59-8eb8-4f1d-bccf-11b5a47b24e5` | [datastore dump](https://api.neso.energy/datastore/dump/1cf68f59-8eb8-4f1d-bccf-11b5a47b24e5) | 18,010,342 | 139,306 | 2026-04-15T11:42:37.727269 |

**FY buy orders** (`eac_results_buy_orders_fy`):

| Resource | Id | Download | Bytes | Data rows | CKAN `last_modified` | Delivery starts (first to last) |
|---|---|---|---:|---:|---|---|
| NESO Response-Reserve Buy Orders FY2023 (Archive) | `7a2d64a5-3233-4ee2-92fd-240db03717f1` | [neso-response-reserve-buy-orders-fy2023-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/7a2d64a5-3233-4ee2-92fd-240db03717f1/download/neso-response-reserve-buy-orders-fy2023-archive.csv) | 3,510,784 | 27,900 | 2026-04-15T11:12:53.676038 | 2023-11-02T23:00:00 to 2024-03-31T18:00:00 |
| NESO Response-Reserve Buy Orders FY2024 (Archive) | `c6f09570-58f9-4e04-81c3-2c99af2fded0` | [neso-response-reserve-buy-orders-fy2024-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/c6f09570-58f9-4e04-81c3-2c99af2fded0/download/neso-response-reserve-buy-orders-fy2024-archive.csv) | 12,775,172 | 97,840 | 2026-04-15T11:16:25.056958 | 2024-03-31T22:00:00 to 2025-03-31T21:30:00 |
| NESO Response-Reserve Buy Orders FY2025 (Archive) | `270a5e1d-ea44-43a0-82b1-703fdaa354ac` | [neso-response-reserve-buy-orders-fy2025-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/270a5e1d-ea44-43a0-82b1-703fdaa354ac/download/neso-response-reserve-buy-orders-fy2025-archive.csv) | 25,538,263 | 198,154 | 2026-04-15T11:20:36.062264 | 2025-03-31T22:00:00 to 2026-03-31T21:30:00 |

**Daily buy orders** (`eac_results_daily_buy_orders`):

| Resource | Id | Download | Bytes | Data rows | CKAN `last_modified` |
|---|---|---|---:|---:|---|
| NESO Response-Reserve Daily Buy Orders | `e638cf3d-bed1-42ae-a984-8fe3c556febf` | [neso-response-reserve-daily-buy-orders.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/e638cf3d-bed1-42ae-a984-8fe3c556febf/download/neso-response-reserve-daily-buy-orders.csv) | 93,083 | 720 | 2026-10-07T13:50:00.627160 |

**Current results summary** (`eac_results_summary`):

| Resource | Id | Download | Bytes | Data rows | CKAN `last_modified` |
|---|---|---|---:|---:|---|
| NESO Response-Reserve Results Summary | `596f29ac-0387-4ba4-a6d3-95c243140707` | [datastore dump](https://api.neso.energy/datastore/dump/596f29ac-0387-4ba4-a6d3-95c243140707) | 4,442,879 | 61,884 | 2026-04-15T11:41:56.782602 |

**FY results summary** (`eac_results_summary_fy`):

| Resource | Id | Download | Bytes | Data rows | CKAN `last_modified` | Delivery starts (first to last) |
|---|---|---|---:|---:|---|---|
| NESO Response-Reserve Results Summary FY2023 (Archive) | `be5c6b0d-a335-4859-93f2-389585b4e9a1` | [neso-response-reserve-results-summary-fy2023-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/be5c6b0d-a335-4859-93f2-389585b4e9a1/download/neso-response-reserve-results-summary-fy2023-archive.csv) | 376,217 | 5,400 | 2026-04-15T11:11:47.892835 | 2023-11-02T23:00:00 to 2024-03-31T18:00:00 |
| NESO Response-Reserve Results Summary FY2024 (Archive) | `ab130833-3ce4-4361-90fb-69fa3cf30f15` | [neso-response-reserve-results-summary-fy2024-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/ab130833-3ce4-4361-90fb-69fa3cf30f15/download/neso-response-reserve-results-summary-fy2024-archive.csv) | 1,771,751 | 24,464 | 2026-04-15T11:15:14.025635 | 2024-03-31T22:00:00 to 2025-03-31T21:30:00 |
| NESO Response-Reserve Results Summary FY2025 (Archive) | `be55ee51-b79e-47da-b71e-a0f8865d9d66` | [neso-response-reserve-results-summary-fy2025-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/be55ee51-b79e-47da-b71e-a0f8865d9d66/download/neso-response-reserve-results-summary-fy2025-archive.csv) | 4,579,797 | 62,864 | 2026-04-15T11:19:18.288047 | 2025-03-31T22:00:00 to 2026-03-31T21:30:00 |

**Daily results summary** (`eac_results_daily_summary`):

| Resource | Id | Download | Bytes | Data rows | CKAN `last_modified` |
|---|---|---|---:|---:|---|
| NESO Response-Reserve Daily Results Summary | `3c51a666-1c33-450e-a6eb-c9b4a0c91584` | [neso-response-reserve-daily-results-summary.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/3c51a666-1c33-450e-a6eb-c9b4a0c91584/download/neso-response-reserve-daily-results-summary.csv) | 23,318 | 324 | 2026-10-07T13:50:37.548300 |

**Daily sell orders** (`eac_results_daily_sell_orders`):

| Resource | Id | Download | Bytes | Data rows | CKAN `last_modified` |
|---|---|---|---:|---:|---|
| NESO Response-Reserve Daily Sell Orders | `8ba48f26-d73e-4094-a90d-ba075eb739c1` | [neso-response-reserve-daily-sell-orders.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/8ba48f26-d73e-4094-a90d-ba075eb739c1/download/neso-response-reserve-daily-sell-orders.csv) | 12,905,812 | 73,098 | 2026-10-07T13:51:36.544135 |

**Sell orders** (`eac_results_sell_orders`, 36 resources: the datastore dump and 35 monthly archives). The
archive month in the title is the **delivery-day month**: each archive's first delivery start is the
evening before its first delivery day (for example `202604` starts `2026-03-31T22:00:00`, which is 23:00
UK time on the evening before 1 April). `TODO: verify` that month definition with the vendor. The five
archives `202411` to `202503` are the 20-column header epoch (no `flexibleGroupID` or
`minimumConsecutiveWindows`); the `202607` archive writes its time cells with a space separator (see
Known issues).

| Resource | Id | Download | Bytes | Data rows | CKAN `last_modified` | Delivery starts (first to last) |
|---|---|---|---:|---:|---|---|
| NESO Response-Reserve Sell Orders | `13b511df-d6ec-4143-afb1-0ecc6fd19810` | [datastore dump](https://api.neso.energy/datastore/dump/13b511df-d6ec-4143-afb1-0ecc6fd19810) | 107,670,541 | 588,221 | 2026-10-01T16:01:12.539145 | 2026-09-30T22:00:00 to 2026-10-08T21:30:00 |
| NESO Response-Reserve Sell Orders 202311 (Archive) | `3780a81e-bee4-43e2-9ebe-ef85d2ba18de` | [neso-response-reserve-sell-orders-202311-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/3780a81e-bee4-43e2-9ebe-ef85d2ba18de/download/neso-response-reserve-sell-orders-202311-archive.csv) | 35,907,337 | 213,541 | 2026-03-03T15:30:30.205226 | 2023-11-02T23:00:00 to 2023-11-30T19:00:00 |
| NESO Response-Reserve Sell Orders 202312 (Archive) | `66bde1bc-1e81-4d91-b022-ae0f072020b6` | [neso-response-reserve-sell-orders-202312-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/66bde1bc-1e81-4d91-b022-ae0f072020b6/download/neso-response-reserve-sell-orders-202312-archive.csv) | 49,000,150 | 287,086 | 2026-03-03T15:32:21.053074 | 2023-11-30T23:00:00 to 2023-12-31T19:00:00 |
| NESO Response-Reserve Sell Orders 202401 (Archive) | `5901ba21-44e3-4f22-922b-e759f9930f92` | [neso-response-reserve-sell-orders-202401-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/5901ba21-44e3-4f22-922b-e759f9930f92/download/neso-response-reserve-sell-orders-202401-archive.csv) | 48,107,363 | 281,110 | 2026-03-03T15:39:22.479737 | 2023-12-31T23:00:00 to 2024-01-31T19:00:00 |
| NESO Response-Reserve Sell Orders 202402 (Archive) | `301443b5-2629-482f-8904-d73cdffffc69` | [neso-response-reserve-sell-orders-202402-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/301443b5-2629-482f-8904-d73cdffffc69/download/neso-response-reserve-sell-orders-202402-archive.csv) | 42,912,248 | 249,698 | 2026-03-03T15:41:14.250917 | 2024-01-31T23:00:00 to 2024-02-29T19:00:00 |
| NESO Response-Reserve Sell Orders 202403 (Archive) | `f588ba39-c449-4879-93f5-e771b85c93dc` | [neso-response-reserve-sell-orders-202403-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/f588ba39-c449-4879-93f5-e771b85c93dc/download/neso-response-reserve-sell-orders-202403-archive.csv) | 42,255,239 | 245,602 | 2026-03-03T15:43:11.307637 | 2024-02-29T23:00:00 to 2024-03-31T18:00:00 |
| NESO Response-Reserve Sell Orders 202404 (Archive) | `85690ec6-741b-4853-840c-7afe70da3e79` | [neso-response-reserve-sell-orders-202404-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/85690ec6-741b-4853-840c-7afe70da3e79/download/neso-response-reserve-sell-orders-202404-archive.csv) | 43,883,314 | 254,662 | 2026-03-03T15:45:02.947505 | 2024-03-31T22:00:00 to 2024-04-30T18:00:00 |
| NESO Response-Reserve Sell Orders 202405 (Archive) | `1b31276c-31a1-46ce-8579-52c4444ccc95` | [neso-response-reserve-sell-orders-202405-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/1b31276c-31a1-46ce-8579-52c4444ccc95/download/neso-response-reserve-sell-orders-202405-archive.csv) | 47,271,147 | 272,339 | 2026-03-03T15:46:53.322005 | 2024-04-30T22:00:00 to 2024-05-31T18:00:00 |
| NESO Response-Reserve Sell Orders 202406 (Archive) | `fb1ed018-e6c3-4032-a08a-7abd4d4fb150` | [neso-response-reserve-sell-orders-202406-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/fb1ed018-e6c3-4032-a08a-7abd4d4fb150/download/neso-response-reserve-sell-orders-202406-archive.csv) | 49,906,218 | 287,224 | 2026-03-03T15:48:44.632196 | 2024-05-31T22:00:00 to 2024-06-30T18:00:00 |
| NESO Response-Reserve Sell Orders 202407 (Archive) | `91f2ad1c-c592-4bbb-8c3b-d5ace1d7a32a` | [neso-response-reserve-sell-orders-202407-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/91f2ad1c-c592-4bbb-8c3b-d5ace1d7a32a/download/neso-response-reserve-sell-orders-202407-archive.csv) | 57,155,286 | 329,638 | 2026-03-03T15:50:41.747999 | 2024-06-30T22:00:00 to 2024-07-31T18:00:00 |
| NESO Response-Reserve Sell Orders 202408 (Archive) | `f62d283f-66e0-4e71-8e8e-b58c31bf8746` | [neso-response-reserve-sell-orders-202408-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/f62d283f-66e0-4e71-8e8e-b58c31bf8746/download/neso-response-reserve-sell-orders-202408-archive.csv) | 58,894,268 | 339,697 | 2026-03-03T15:52:37.799930 | 2024-07-31T22:00:00 to 2024-08-31T18:00:00 |
| NESO Response-Reserve Sell Orders 202409 (Archive) | `3aa319e4-21bb-4f69-be63-05144ddca6b4` | [neso-response-reserve-sell-orders-202409-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/3aa319e4-21bb-4f69-be63-05144ddca6b4/download/neso-response-reserve-sell-orders-202409-archive.csv) | 53,395,387 | 307,636 | 2026-03-03T15:54:30.771090 | 2024-08-31T22:00:00 to 2024-09-30T18:00:00 |
| NESO Response-Reserve Sell Orders 202410 (Archive) | `7cee44eb-0668-489c-9a0f-fef5f5d7fa50` | [neso-response-reserve-sell-orders-202410-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/7cee44eb-0668-489c-9a0f-fef5f5d7fa50/download/neso-response-reserve-sell-orders-202410-archive.csv) | 52,799,276 | 304,431 | 2026-03-03T15:56:30.755469 | 2024-09-30T22:00:00 to 2024-10-31T19:00:00 |
| NESO Response-Reserve Sell Orders 202411 (Archive) | `39c7648c-d43b-4ef9-b689-a82619245cda` | [neso-response-reserve-sell-orders-202411-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/39c7648c-d43b-4ef9-b689-a82619245cda/download/neso-response-reserve-sell-orders-202411-archive.csv) | 47,947,411 | 279,753 | 2026-03-03T16:02:06.498574 | 2024-10-31T23:00:00 to 2024-11-30T19:00:00 |
| NESO Response-Reserve Sell Orders 202412 (Archive) | `0a6325b9-1b78-4ee2-a1a0-647aa3b6d014` | [neso-response-reserve-sell-orders-202412-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/0a6325b9-1b78-4ee2-a1a0-647aa3b6d014/download/neso-response-reserve-sell-orders-202412-archive.csv) | 125,884,505 | 727,057 | 2026-03-03T16:03:38.790793 | 2024-11-30T23:00:00 to 2024-12-31T22:30:00 |
| NESO Response-Reserve Sell Orders 202501 (Archive) | `3c03d431-7f94-4009-903d-8a4df1aea9f4` | [neso-response-reserve-sell-orders-202501-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/3c03d431-7f94-4009-903d-8a4df1aea9f4/download/neso-response-reserve-sell-orders-202501-archive.csv) | 136,429,757 | 787,375 | 2026-03-03T16:05:17.927776 | 2024-12-31T23:00:00 to 2025-01-31T22:30:00 |
| NESO Response-Reserve Sell Orders 202502 (Archive) | `5997f602-24f1-4f44-aa36-c7b898229d60` | [neso-response-reserve-sell-orders-202502-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/5997f602-24f1-4f44-aa36-c7b898229d60/download/neso-response-reserve-sell-orders-202502-archive.csv) | 144,626,455 | 828,362 | 2026-03-03T16:06:53.676437 | 2025-01-31T23:00:00 to 2025-02-28T22:30:00 |
| NESO Response-Reserve Sell Orders 202503 (Archive) | `02c3ede4-6909-4c7b-9b77-511c774decb2` | [neso-response-reserve-sell-orders-202503-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/02c3ede4-6909-4c7b-9b77-511c774decb2/download/neso-response-reserve-sell-orders-202503-archive.csv) | 137,419,588 | 781,966 | 2026-03-03T16:08:32.479610 | 2025-02-28T23:00:00 to 2025-03-31T21:30:00 |
| NESO Response-Reserve Sell Orders 202504 (Archive) | `57340708-6f3a-429b-8ede-682df3c86709` | [neso-response-reserve-sell-orders-202504-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/57340708-6f3a-429b-8ede-682df3c86709/download/neso-response-reserve-sell-orders-202504-archive.csv) | 126,915,224 | 714,073 | 2026-04-15T10:05:06.979386 | 2025-03-31T22:00:00 to 2025-04-30T21:30:00 |
| NESO Response-Reserve Sell Orders 202505 (Archive) | `069a047e-5b0a-4d27-83fa-f45e451661e3` | [neso-response-reserve-sell-orders-202505-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/069a047e-5b0a-4d27-83fa-f45e451661e3/download/neso-response-reserve-sell-orders-202505-archive.csv) | 132,477,318 | 745,433 | 2026-04-15T10:07:06.738467 | 2025-04-30T22:00:00 to 2025-05-31T21:30:00 |
| NESO Response-Reserve Sell Orders 202506 (Archive) | `e0b50ef5-b37f-46ad-8eb2-17ab0eedb6d1` | [neso-response-reserve-sell-orders-202506-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/e0b50ef5-b37f-46ad-8eb2-17ab0eedb6d1/download/neso-response-reserve-sell-orders-202506-archive.csv) | 128,969,508 | 725,837 | 2026-04-15T10:09:09.476407 | 2025-05-31T22:00:00 to 2025-06-30T21:30:00 |
| NESO Response-Reserve Sell Orders 202507 (Archive) | `81a9700a-6fcd-4c26-ab3b-965d771bfa2c` | [neso-response-reserve-sell-orders-202507-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/81a9700a-6fcd-4c26-ab3b-965d771bfa2c/download/neso-response-reserve-sell-orders-202507-archive.csv) | 124,858,450 | 703,957 | 2026-04-15T10:11:04.709123 | 2025-06-30T22:00:00 to 2025-07-31T21:30:00 |
| NESO Response-Reserve Sell Orders 202508 (Archive) | `d4bc27fe-45a1-43c4-b469-f5f1ba5824ed` | [neso-response-reserve-sell-orders-202508-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/d4bc27fe-45a1-43c4-b469-f5f1ba5824ed/download/neso-response-reserve-sell-orders-202508-archive.csv) | 126,353,399 | 711,622 | 2026-04-15T10:20:38.019063 | 2025-07-31T22:00:00 to 2025-08-31T21:30:00 |
| NESO Response-Reserve Sell Orders 202509 (Archive) | `f8db9239-1f96-42ad-bab9-d2ef60c52e1e` | [neso-response-reserve-sell-orders-202509-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/f8db9239-1f96-42ad-bab9-d2ef60c52e1e/download/neso-response-reserve-sell-orders-202509-archive.csv) | 126,610,118 | 713,323 | 2026-04-15T10:22:36.856860 | 2025-08-31T22:00:00 to 2025-09-30T21:30:00 |
| NESO Response-Reserve Sell Orders 202510 (Archive) | `a6ce3d85-4cdd-4276-b23b-01b160f49164` | [neso-response-reserve-sell-orders-202510-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/a6ce3d85-4cdd-4276-b23b-01b160f49164/download/neso-response-reserve-sell-orders-202510-archive.csv) | 135,139,235 | 755,167 | 2026-04-15T10:24:40.379593 | 2025-09-30T22:00:00 to 2025-10-31T22:30:00 |
| NESO Response-Reserve Sell Orders 202511 (Archive) | `8adbb902-6029-4af7-b8dd-e1e500aaaa51` | [neso-response-reserve-sell-orders-202511-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/8adbb902-6029-4af7-b8dd-e1e500aaaa51/download/neso-response-reserve-sell-orders-202511-archive.csv) | 182,302,153 | 1,009,534 | 2026-04-15T10:28:17.277412 | 2025-10-31T23:00:00 to 2025-11-30T22:30:00 |
| NESO Response-Reserve Sell Orders 202512 (Archive) | `eaa6961f-87c2-483a-94a2-7d6247c7e994` | [neso-response-reserve-sell-orders-202512-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/eaa6961f-87c2-483a-94a2-7d6247c7e994/download/neso-response-reserve-sell-orders-202512-archive.csv) | 210,693,512 | 1,165,305 | 2026-04-15T10:40:34.426226 | 2025-11-30T23:00:00 to 2025-12-31T22:30:00 |
| NESO Response-Reserve Sell Orders 202601 (Archive) | `b155f068-e10f-4c6e-8960-a2cb2806ae13` | [neso-response-reserve-sell-orders-202601-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/b155f068-e10f-4c6e-8960-a2cb2806ae13/download/neso-response-reserve-sell-orders-202601-archive.csv) | 230,859,840 | 1,269,891 | 2026-04-15T10:42:58.574624 | 2025-12-31T23:00:00 to 2026-01-31T22:30:00 |
| NESO Response-Reserve Sell Orders 202602 (Archive) | `4e5c9a3c-77c6-4709-abdd-236353451771` | [neso-response-reserve-sell-orders-202602-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/4e5c9a3c-77c6-4709-abdd-236353451771/download/neso-response-reserve-sell-orders-202602-archive.csv) | 236,208,403 | 1,290,484 | 2026-04-15T10:47:02.588741 | 2026-01-31T23:00:00 to 2026-02-28T22:30:00 |
| NESO Response-Reserve Sell Orders 202603 (Archive) | `5531d313-cab5-4f02-9eda-d0242a62d984` | [neso-response-reserve-sell-orders-202603-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/5531d313-cab5-4f02-9eda-d0242a62d984/download/neso-response-reserve-sell-orders-202603-archive.csv) | 268,590,322 | 1,468,655 | 2026-04-15T11:01:13.682173 | 2026-02-28T23:00:00 to 2026-03-31T21:30:00 |
| NESO Response-Reserve Sell Orders 202604 (Archive) | `45d867bb-eccb-4a60-8618-74316aafde5a` | [neso-response-reserve-sell-orders-202604-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/45d867bb-eccb-4a60-8618-74316aafde5a/download/neso-response-reserve-sell-orders-202604-archive.csv) | 407,096,188 | 2,224,075 | 2026-05-12T12:16:01.802743 | 2026-03-31T22:00:00 to 2026-04-30T21:30:00 |
| NESO Response-Reserve Sell Orders 202605 (Archive) | `654c9fcd-9d0b-42c5-bac7-9fa245b5f99d` | [neso-response-reserve-sell-orders-202605-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/654c9fcd-9d0b-42c5-bac7-9fa245b5f99d/download/neso-response-reserve-sell-orders-202605-archive.csv) | 438,169,445 | 2,383,896 | 2026-06-09T14:44:42.446538 | 2026-04-30T22:00:00 to 2026-05-31T21:30:00 |
| NESO Response-Reserve Sell Orders 202606 (Archive) | `85272de8-2fd7-4578-ae4b-55da74629841` | [neso-response-reserve-sell-orders-202606-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/85272de8-2fd7-4578-ae4b-55da74629841/download/neso-response-reserve-sell-orders-202606-archive.csv) | 413,774,943 | 2,248,258 | 2026-07-14T13:10:12.271937 | 2026-05-31T22:00:00 to 2026-06-30T21:30:00 |
| NESO Response-Reserve Sell Orders 202607 (Archive) | `fc52a1fa-6ce5-4c35-a661-be1b49c1c48f` | [neso-response-reserve-sell-orders-202607-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/fc52a1fa-6ce5-4c35-a661-be1b49c1c48f/download/neso-response-reserve-sell-orders-202607-archive.csv) | 422,104,078 | 2,291,298 | 2026-08-12T16:47:23.277278 | 2026-06-30 22:00:00 to 2026-07-31 21:30:00 |
| NESO Response-Reserve Sell Orders 202608 (Archive) | `aeef326a-9379-4263-a7cd-63c5e4fb0911` | [neso-response-reserve-sell-orders-202608-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/aeef326a-9379-4263-a7cd-63c5e4fb0911/download/neso-response-reserve-sell-orders-202608-archive.csv) | 416,593,733 | 2,259,805 | 2026-10-01T14:42:19.957517 | 2026-07-31T22:00:00 to 2026-08-31T21:30:00 |
| NESO Response-Reserve Sell Orders 202609 (Archive) | `06f4396f-d222-477d-85ad-916ac0662630` | [neso-response-reserve-sell-orders-202609-archive.csv](https://api.neso.energy/dataset/291e3c28-75f2-4a8f-b5f5-008bebaac368/resource/06f4396f-d222-477d-85ad-916ac0662630/download/neso-response-reserve-sell-orders-202609-archive.csv) | 413,221,997 | 2,244,190 | 2026-10-01T15:31:04.901596 | 2026-08-31T22:00:00 to 2026-09-30T21:30:00 |

## Families

### `eac_results_buy_orders`

- Kind: tabular · archetype: EVT · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| auctionID | `auction_id` | string | — | no | — | — |
| orderID | `order_id` | string | — | no | — | — |
| serviceType | `service_type` | string | — | yes | — | — |
| auctionProduct | `auction_product` | string | — | yes | — | — |
| deliveryStart | `delivery_start` | datetime | `%Y-%m-%dT%H:%M:%S` | no | UTC | — |
| deliveryEnd | `delivery_end` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | — |
| quantity | `quantity` | float64 | — | yes | — | MW |
| price | `price` | float64 | — | yes | — | £/MW/h |
| substitutabilityFamily | `substitutability_family` | string | — | yes | — | — |
| paradoxicallyAcceptanceAllowed | `paradoxically_acceptance_allowed` | string | — | yes | — | — |
| orderEntryTime | `order_entry_time` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | — |
| acceptanceRatio | `acceptance_ratio` | float64 | — | yes | — | — |
| status | `status` | string | — | yes | — | — |
| executedQuantity | `executed_quantity` | float64 | — | yes | — | MW |
| clearingPrice | `clearing_price` | float64 | — | yes | — | £/MW/h |
| reasonRejected | `reason_rejected` | string | — | yes | — | — |
| joinedFamily | `joined_family` | string | — | yes | — | — |

- Entity key: `auction_id`, `order_id`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`delivery_start`)

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

- **Eligible**, no hold. **Current** buy orders: resource `1cf68f59-8eb8-4f1d-bccf-11b5a47b24e5` (datastore dump, 18,010,342 bytes, 139,306 rows). One row per submitted buy order. Header H-B, 17 columns, one epoch; the FY and daily buy-order families share it exactly.

**Two clocks.**

1. **Vintage (`capture_fallback`).** The current table is a datastore dump, so `published_at` is **null**
   and `available_at` is the **gridflow capture time** (sidecar `written_at`), **2026-10-08T10:28:57.818532Z**, one value on
   all rows. That is when gridflow fetched the dump, **not when NESO published each result**. The dump's
   CKAN `last_modified` (2026-04-15T11:42:37.727269) is stale against its own rows and is not used (record rule V-8). Every
   row, including results delivered months earlier, carries the same 2026-10-08 `available_at`, so an
   as-of query before 2026-10-08T10:28:57Z sees **no** rows of this family and a point-in-time backtest cannot use it to
   say when a past result became known. These are event results, so the forward-target rule for
   forecasts (RULINGS 529) does not apply. `TODO: verify` the vendor's original publication instant of
   each result and whether past rows are amended in place at the daily refresh: one capture exists.
2. **Event time (temporal recipe `utc_instant` on `delivery_start`).** `timestamp_utc` and `event_time` equal
   `delivery_start` on every row (checked on all rows): the **start of the delivery window, in UTC**. The
   vendor's package text declares the datetimes UTC; the cells carry no offset suffix, so the UTC typing
   rests on that declaration and not on syntax. There is no shift: the BST-season value
   `2026-03-31T22:00:00` is `22:00Z` (23:00 UK local time). `delivery_end` is the window end, kept as a
   typed UTC datetime but not the recipe column. The endpoint closure (whether the end instant belongs to
   the window) is not stated by the vendor: `TODO: verify` (INTERVAL-CLOSURE). Delivery starts run `2026-03-31T22:00:00` to `2026-10-08T21:30:00`; `order_entry_time` runs `2026-03-31T09:24:45` to `2026-10-07T11:00:07`.

**Identity and selection.**

- The record key is `(auction_id, order_id)`: unique across all 139,306 rows, in the body and in silver (`order_id` alone also passes). The vendor guarantees no key, and an order identity that is stable across later corrected exports is not documented: `TODO: verify` (EAC-ORDER-REVISION-IDENTITY). `_latest` is therefore `whole_capture`, the newest complete capture; there is no `key_latest` and no resource partition.
- Current and FY buy-order keys are disjoint (0 shared); every one of the 720 daily keys is in this table.

**Sentinels, zeros and the one out-of-range ratio.** Quantities are never zero (minimum 6 MW). Zero `acceptance_ratio` and zero `executed_quantity` each occur on 48,166 rows (rejected or unmatched orders; a zero executed quantity does not by itself identify a rejected order), and 29,302 rows have a zero `clearing_price`. **One row has `acceptance_ratio` 1.049999949856768**, above the documented 0 to 1 range: auction `2758`, order `2405348`, product `DMH`, delivery start `2026-06-23T06:00:00`, quantity 20 MW, executed quantity 21 MW, status `EXECUTED`. It is kept as served and not clamped; vendor correction or explanation would settle it (`TODO: verify`, EAC-BUY-ACCEPTANCE-RANGE). Observed in this capture: `price` 0 to 354.2 £/MW/h, `clearing_price` -20 to 230 £/MW/h, `quantity` 6 to 1,800 MW, 191 auction IDs. Blank: `reason_rejected`, `substitutability_family`, `joined_family` are optional and stay null when empty.

**Row counts and shape (silver, 2026-10-13).** 139,306 rows, 0 validation failures, 0 rows excluded; the planned and activated counts agree (RULINGS 741). Silver layout: one Parquet file under `C:/gridflow-data/silver/neso_data_portal/eac_results_buy_orders/year=2026/month=10/`; the partition is the **capture** date. Columns (25): the 17 vendor columns, then `timestamp_utc`, `published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id` and `dataset_version` (`1+e1`). All timestamps are tz-aware UTC. No gold view or builder reads this family.

### `eac_results_buy_orders_fy`

- Kind: tabular · archetype: EVT · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| auctionID | `auction_id` | string | — | no | — | — |
| orderID | `order_id` | string | — | no | — | — |
| serviceType | `service_type` | string | — | yes | — | — |
| auctionProduct | `auction_product` | string | — | yes | — | — |
| deliveryStart | `delivery_start` | datetime | `%Y-%m-%dT%H:%M:%S` | no | UTC | — |
| deliveryEnd | `delivery_end` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | — |
| quantity | `quantity` | float64 | — | yes | — | MW |
| price | `price` | float64 | — | yes | — | £/MW/h |
| substitutabilityFamily | `substitutability_family` | string | — | yes | — | — |
| paradoxicallyAcceptanceAllowed | `paradoxically_acceptance_allowed` | string | — | yes | — | — |
| orderEntryTime | `order_entry_time` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | — |
| acceptanceRatio | `acceptance_ratio` | float64 | — | yes | — | — |
| status | `status` | string | — | yes | — | — |
| executedQuantity | `executed_quantity` | float64 | — | yes | — | MW |
| clearingPrice | `clearing_price` | float64 | — | yes | — | £/MW/h |
| reasonRejected | `reason_rejected` | string | — | yes | — | — |
| joinedFamily | `joined_family` | string | — | yes | — | — |

- Entity key: `resource_id`, `auction_id`, `order_id`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: utc_instant (`delivery_start`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

- **Eligible**, no hold. **FY archive** buy orders: three upload resources, FY2023 `7a2d64a5-3233-4ee2-92fd-240db03717f1` (27,900 rows), FY2024 `c6f09570-58f9-4e04-81c3-2c99af2fded0` (97,840) and FY2025 `270a5e1d-ea44-43a0-82b1-703fdaa354ac` (198,154); 323,894 rows. Same 17-column header as the current table.

**Two clocks.**

1. **Vintage (`ckan_last_modified`).** Every resource is an upload with a usable CKAN timestamp, so
   `published_at` = `available_at` = the CKAN `last_modified` of the captured file (ADR-030): FY2023 **2026-04-15T11:12:53.676038Z**, FY2024 **2026-04-15T11:16:25.056958Z**, FY2025 **2026-04-15T11:20:36.062264Z** (three distinct values, one per resource).
   All three are April 2026 uploads, so every result back to November 2023 carries a 2026 `available_at`: an as-of query before 2026-04-15T11:12:53Z sees **no** rows. That is when the file was last uploaded, not when each result was first published: the
   files have no publication column. `TODO: verify` the vendor's original publication instant of each
   result and whether past rows are amended in place when NESO re-uploads: one capture exists.
2. **Event time (temporal recipe `utc_instant` on `delivery_start`).** `timestamp_utc` and `event_time` equal
   `delivery_start` on every row (checked on all rows): the **start of the delivery window, in UTC**. The
   vendor's package text declares the datetimes UTC; the cells carry no offset suffix, so the UTC typing
   rests on that declaration and not on syntax. There is no shift: the BST-season value
   `2026-03-31T22:00:00` is `22:00Z` (23:00 UK local time). `delivery_end` is the window end, kept as a
   typed UTC datetime but not the recipe column. The endpoint closure (whether the end instant belongs to
   the window) is not stated by the vendor: `TODO: verify` (INTERVAL-CLOSURE). Delivery starts run `2023-11-02T23:00:00` to `2026-03-31T21:30:00`; by resource FY2023 covers `2023-11-02T23:00:00` to `2024-03-31T18:00:00`, FY2024 `2024-03-31T22:00:00` to `2025-03-31T21:30:00` and FY2025 `2025-03-31T22:00:00` to `2026-03-31T21:30:00`.

**Identity and selection.**

- The record key is `(resource_id, auction_id, order_id)` with `_latest` = `whole_capture` **per `resource_id`** (ADR-039): all three archive bodies are kept side by side. The archives are mutually key-disjoint and disjoint from the current table, so no cross-resource dedup or precedence is invented. `(auction_id, order_id)` is unique across the 323,894 rows. No `key_latest`. `TODO: verify` order identity across corrected re-exports (EAC-ORDER-REVISION-IDENTITY).

**Sentinels and zeros.** 88,016 rows have a zero `acceptance_ratio` and a zero `executed_quantity`, 12 have a zero `quantity`, 19,722 a zero `clearing_price`. **185 rows carry a `clearing_price` of -1**; it is a signed price and stays `-1.0`, never null. Observed: `price` -0.09 to 163.2 £/MW/h, `clearing_price` -20 to 159.69 £/MW/h, `acceptance_ratio` 0 to 1, 880 auction IDs.

**Row counts and shape (silver, 2026-10-13).** 323,894 rows, 0 validation failures, 0 rows excluded; the planned and activated counts agree (RULINGS 741). Silver layout: three Parquet files (one per resource) under `C:/gridflow-data/silver/neso_data_portal/eac_results_buy_orders_fy/year=2026/month=10/`; the partition is the **capture** date. Columns (26): `resource_id` first, then the 17 vendor columns, then `timestamp_utc`, `published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id` and `dataset_version` (`1+e1`). All timestamps are tz-aware UTC. No gold view or builder reads this family.

### `eac_results_by_unit`

- Kind: tabular · archetype: EVT · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| registeredAuctionParticipant | `registered_auction_participant` | string | — | yes | — | — |
| auctionUnit | `auction_unit` | string | — | yes | — | — |
| serviceType | `service_type` | string | — | yes | — | — |
| auctionProduct | `auction_product` | string | — | yes | — | — |
| executedQuantity | `executed_quantity` | float64 | — | yes | — | MW |
| clearingPrice | `clearing_price` | float64 | — | yes | — | £/MW/h |
| deliveryStart | `delivery_start` | datetime | `%Y-%m-%dT%H:%M:%S` | no | UTC | ISO8601 |
| deliveryEnd | `delivery_end` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | ISO 8601 |
| technologyType | `technology_type` | string | — | yes | — | — |
| postCode | `post_code` | string | — | yes | — | — |
| unitResultID | `unit_result_id` | string | — | no | — | — |

- Entity key: `unit_result_id`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`delivery_start`)

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

- **Eligible**, no hold. **Current** results by unit: resource `a63ab354-7e68-44c2-ad96-c6f920c30e85` (datastore dump, 218,717,646 bytes, 1,444,630 rows). One row per accepted unit result. Header H-U, 11 columns, one epoch; the FY and daily by-unit families share it exactly.

**Two clocks.**

1. **Vintage (`capture_fallback`).** The current table is a datastore dump, so `published_at` is **null**
   and `available_at` is the **gridflow capture time** (sidecar `written_at`), **2026-10-08T10:31:38.664575Z**, one value on
   all rows. That is when gridflow fetched the dump, **not when NESO published each result**. The dump's
   CKAN `last_modified` (2026-04-15T11:43:07.338503) is stale against its own rows and is not used (record rule V-8). Every
   row, including results delivered months earlier, carries the same 2026-10-08 `available_at`, so an
   as-of query before 2026-10-08T10:31:38Z sees **no** rows of this family and a point-in-time backtest cannot use it to
   say when a past result became known. These are event results, so the forward-target rule for
   forecasts (RULINGS 529) does not apply. `TODO: verify` the vendor's original publication instant of
   each result and whether past rows are amended in place at the daily refresh: one capture exists.
2. **Event time (temporal recipe `utc_instant` on `delivery_start`).** `timestamp_utc` and `event_time` equal
   `delivery_start` on every row (checked on all rows): the **start of the delivery window, in UTC**. The
   vendor's package text declares the datetimes UTC; the cells carry no offset suffix, so the UTC typing
   rests on that declaration and not on syntax. There is no shift: the BST-season value
   `2026-03-31T22:00:00` is `22:00Z` (23:00 UK local time). `delivery_end` is the window end, kept as a
   typed UTC datetime but not the recipe column. The endpoint closure (whether the end instant belongs to
   the window) is not stated by the vendor: `TODO: verify` (INTERVAL-CLOSURE). Delivery starts run `2026-03-31T22:00:00` to `2026-10-08T21:30:00`.

**Identity and selection.**

- The record key is `unit_result_id` alone (the vendor dictionary describes it as the unique identifier of the unit result record): all 1,444,630 values are distinct. **Do not** replace it with `(auction_unit, auction_product, delivery_start)`; that triple repeats (36 duplicate-excess rows in the FY2024 body). `_latest` is `whole_capture`; no `key_latest`, no resource partition.
- Current and FY by-unit keys are disjoint (0 shared); all 7,925 daily keys are in this table, with numeric lexical forms differing (`5.0` versus `5`) but no numeric disagreement.

**Sentinels and zeros.** `executed_quantity` is never zero in this table (minimum 1 MW); 76,510 rows have a zero `clearing_price`, and no `-1` price occurs. Observed: `executed_quantity` 1 to 287 MW, `clearing_price` -20 to 230 £/MW/h, 432 distinct `auction_unit` values, 13 `technology_type` values; `technology_type` and `post_code` are optional and stay null when blank.

**Row counts and shape (silver, 2026-10-13).** 1,444,630 rows, 0 validation failures, 0 rows excluded; the planned and activated counts agree (RULINGS 741). Silver layout: one Parquet file under `C:/gridflow-data/silver/neso_data_portal/eac_results_by_unit/year=2026/month=10/`; the partition is the **capture** date. Columns (19): the 11 vendor columns, then `timestamp_utc`, `published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id` and `dataset_version` (`1+e1`). All timestamps are tz-aware UTC. No gold view or builder reads this family.

### `eac_results_by_unit_fy`

- Kind: tabular · archetype: EVT · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| registeredAuctionParticipant | `registered_auction_participant` | string | — | yes | — | — |
| auctionUnit | `auction_unit` | string | — | yes | — | — |
| serviceType | `service_type` | string | — | yes | — | — |
| auctionProduct | `auction_product` | string | — | yes | — | — |
| executedQuantity | `executed_quantity` | float64 | — | yes | — | MW |
| clearingPrice | `clearing_price` | float64 | — | yes | — | £/MW/h |
| deliveryStart | `delivery_start` | datetime | `%Y-%m-%dT%H:%M:%S` | no | UTC | ISO8601 |
| deliveryEnd | `delivery_end` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | ISO 8601 |
| technologyType | `technology_type` | string | — | yes | — | — |
| postCode | `post_code` | string | — | yes | — | — |
| unitResultID | `unit_result_id` | string | — | no | — | — |

- Entity key: `resource_id`, `unit_result_id`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: utc_instant (`delivery_start`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

- **Eligible**, no hold. **FY archive** results by unit: three upload resources, FY2023 `7505ec16-e1e7-432e-8abd-a554e03e4f02` (161,252 rows), FY2024 `2fc9dd7e-5274-40e3-abf4-6d31b30f21c6` (563,041) and FY2025 `c312358e-87da-480e-88cc-d45c1dce1b41` (1,176,445); 1,900,738 rows. Same 11-column header as the current table.

**Two clocks.**

1. **Vintage (`ckan_last_modified`).** Every resource is an upload with a usable CKAN timestamp, so
   `published_at` = `available_at` = the CKAN `last_modified` of the captured file (ADR-030): FY2023 **2026-04-15T11:14:07.744257Z**, FY2024 **2026-04-15T11:18:09.202266Z**, FY2025 **2026-04-15T11:22:51.072165Z**.
   Every result back to November 2023 carries a 2026-04 `available_at`; an as-of query before 2026-04-15T11:14:07Z sees **no** rows. That is when the file was last uploaded, not when each result was first published: the
   files have no publication column. `TODO: verify` the vendor's original publication instant of each
   result and whether past rows are amended in place when NESO re-uploads: one capture exists.
2. **Event time (temporal recipe `utc_instant` on `delivery_start`).** `timestamp_utc` and `event_time` equal
   `delivery_start` on every row (checked on all rows): the **start of the delivery window, in UTC**. The
   vendor's package text declares the datetimes UTC; the cells carry no offset suffix, so the UTC typing
   rests on that declaration and not on syntax. There is no shift: the BST-season value
   `2026-03-31T22:00:00` is `22:00Z` (23:00 UK local time). `delivery_end` is the window end, kept as a
   typed UTC datetime but not the recipe column. The endpoint closure (whether the end instant belongs to
   the window) is not stated by the vendor: `TODO: verify` (INTERVAL-CLOSURE). Delivery starts run `2023-11-02T23:00:00` to `2026-03-31T21:30:00`; by resource FY2023 `2023-11-02T23:00:00` to `2024-03-31T18:00:00`, FY2024 `2024-03-31T22:00:00` to `2025-03-31T21:30:00`, FY2025 `2025-03-31T22:00:00` to `2026-03-31T21:30:00`.

**Identity and selection.**

- The record key is `(resource_id, unit_result_id)` with `_latest` = `whole_capture` per `resource_id` (ADR-039): all three archive bodies are kept. `unit_result_id` is unique across the 1,900,738 rows and the archives are mutually key-disjoint and disjoint from the current table. Do not key on `(auction_unit, auction_product, delivery_start)`. No `key_latest`.

**Sentinels and zeros.** 12,042 rows have a zero `executed_quantity` (the current table has none), 56,225 a zero `clearing_price`, and **512 rows carry a `clearing_price` of -1**, kept as `-1.0` and never null. Observed: `executed_quantity` 0 to 99 MW, `clearing_price` -20 to 159.69 £/MW/h, 351 distinct `auction_unit` values; `technology_type` here includes the value `BM (SVA/VLP/Battery)`, which does not occur in the current table.

**Row counts and shape (silver, 2026-10-13).** 1,900,738 rows, 0 validation failures, 0 rows excluded; the planned and activated counts agree (RULINGS 741). Silver layout: three Parquet files (one per resource) under `C:/gridflow-data/silver/neso_data_portal/eac_results_by_unit_fy/year=2026/month=10/`; the partition is the **capture** date. Columns (20): `resource_id` first, then the 11 vendor columns, then `timestamp_utc`, `published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id` and `dataset_version` (`1+e1`). All timestamps are tz-aware UTC. No gold view or builder reads this family.

### `eac_results_daily_buy_orders`

- Kind: tabular · archetype: EVT · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| auctionID | `auction_id` | string | — | no | — | — |
| orderID | `order_id` | string | — | no | — | — |
| serviceType | `service_type` | string | — | yes | — | — |
| auctionProduct | `auction_product` | string | — | yes | — | — |
| deliveryStart | `delivery_start` | datetime | `%Y-%m-%dT%H:%M:%S` | no | UTC | — |
| deliveryEnd | `delivery_end` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | — |
| quantity | `quantity` | float64 | — | yes | — | MW |
| price | `price` | float64 | — | yes | — | £/MW/h |
| substitutabilityFamily | `substitutability_family` | string | — | yes | — | — |
| paradoxicallyAcceptanceAllowed | `paradoxically_acceptance_allowed` | string | — | yes | — | — |
| orderEntryTime | `order_entry_time` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | — |
| acceptanceRatio | `acceptance_ratio` | float64 | — | yes | — | — |
| status | `status` | string | — | yes | — | — |
| executedQuantity | `executed_quantity` | float64 | — | yes | — | MW |
| clearingPrice | `clearing_price` | float64 | — | yes | — | £/MW/h |
| reasonRejected | `reason_rejected` | string | — | yes | — | — |
| joinedFamily | `joined_family` | string | — | yes | — | — |

- Entity key: `auction_id`, `order_id`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`delivery_start`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

- **Eligible**, no hold. **Daily** buy orders (latest auction only): resource `e638cf3d-bed1-42ae-a984-8fe3c556febf` (upload, 93,083 bytes, 720 rows). Header H-B, 17 columns. The vendor describes the daily resources as results for the **latest auction only**, per day and not aggregated across days. Measured: delivery starts span exactly one delivery day (`2026-10-07T22:00:00` to `2026-10-08T21:30:00`). Only one capture exists, so what a later capture holds is unmeasured. Never add a daily row to its current counterpart.

**Two clocks.**

1. **Vintage (`ckan_last_modified`).** Every resource is an upload with a usable CKAN timestamp, so
   `published_at` = `available_at` = the CKAN `last_modified` of the captured file (ADR-030): **2026-10-07T13:50:00.627160Z**, one value on all 720 rows.
   The capture was written 2026-10-08T10:31:54Z; the upload itself is dated the previous day, ahead of the delivery day it holds. That is when the file was last uploaded, not when each result was first published: the
   files have no publication column. `TODO: verify` the vendor's original publication instant of each
   result and whether past rows are amended in place when NESO re-uploads: one capture exists.
2. **Event time (temporal recipe `utc_instant` on `delivery_start`).** `timestamp_utc` and `event_time` equal
   `delivery_start` on every row (checked on all rows): the **start of the delivery window, in UTC**. The
   vendor's package text declares the datetimes UTC; the cells carry no offset suffix, so the UTC typing
   rests on that declaration and not on syntax. There is no shift: the BST-season value
   `2026-03-31T22:00:00` is `22:00Z` (23:00 UK local time). `delivery_end` is the window end, kept as a
   typed UTC datetime but not the recipe column. The endpoint closure (whether the end instant belongs to
   the window) is not stated by the vendor: `TODO: verify` (INTERVAL-CLOSURE). `order_entry_time` runs `2026-10-07T09:18:27` to `2026-10-07T11:00:07`.

**Identity and selection.**

- The record key is `(auction_id, order_id)`, unique across 720 rows; `_latest` = `whole_capture`, which makes the newest capture the current view of the latest auction. All 720 keys are in the current buy-order table and the rows are lexically identical to it (0 differences). `TODO: verify` retention of earlier daily captures once a second capture exists.

**Zeros.** 261 rows have a zero `acceptance_ratio` and zero `executed_quantity`, 146 a zero `clearing_price`; no zero `quantity` and no -1 price. Observed: `price` 0 to 101.99 £/MW/h, `clearing_price` -13.4 to 30.95 £/MW/h, `acceptance_ratio` 0 to 1.

**Row counts and shape (silver, 2026-10-13).** 720 rows, 0 validation failures, 0 rows excluded; the planned and activated counts agree (RULINGS 741). Silver layout: one Parquet file under `C:/gridflow-data/silver/neso_data_portal/eac_results_daily_buy_orders/year=2026/month=10/`; the partition is the **capture** date. Columns (25): the 17 vendor columns, then `timestamp_utc`, `published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id` and `dataset_version` (`1+e1`). All timestamps are tz-aware UTC. No gold view or builder reads this family.

### `eac_results_daily_by_unit`

- Kind: tabular · archetype: EVT · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| registeredAuctionParticipant | `registered_auction_participant` | string | — | yes | — | — |
| auctionUnit | `auction_unit` | string | — | yes | — | — |
| serviceType | `service_type` | string | — | yes | — | — |
| auctionProduct | `auction_product` | string | — | yes | — | — |
| executedQuantity | `executed_quantity` | float64 | — | yes | — | MW |
| clearingPrice | `clearing_price` | float64 | — | yes | — | £/MW/h |
| deliveryStart | `delivery_start` | datetime | `%Y-%m-%dT%H:%M:%S` | no | UTC | ISO8601 |
| deliveryEnd | `delivery_end` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | ISO 8601 |
| technologyType | `technology_type` | string | — | yes | — | — |
| postCode | `post_code` | string | — | yes | — | — |
| unitResultID | `unit_result_id` | string | — | no | — | — |

- Entity key: `unit_result_id`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`delivery_start`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

- **Eligible**, no hold. **Daily** results by unit (latest auction only): resource `07f0dd8b-4471-4e2e-9ed6-d21b0ce1f6f5` (upload, 1,182,864 bytes, 7,925 rows). Header H-U, 11 columns. The vendor describes the daily resources as results for the **latest auction only**, per day and not aggregated across days. Measured: delivery starts span exactly one delivery day (`2026-10-07T22:00:00` to `2026-10-08T21:30:00`). Only one capture exists, so what a later capture holds is unmeasured. Never add a daily row to its current counterpart.

**Two clocks.**

1. **Vintage (`ckan_last_modified`).** Every resource is an upload with a usable CKAN timestamp, so
   `published_at` = `available_at` = the CKAN `last_modified` of the captured file (ADR-030): **2026-10-07T13:49:22.409022Z**, one value on all 7,925 rows.
   The capture was written 2026-10-08T10:31:58Z. That is when the file was last uploaded, not when each result was first published: the
   files have no publication column. `TODO: verify` the vendor's original publication instant of each
   result and whether past rows are amended in place when NESO re-uploads: one capture exists.
2. **Event time (temporal recipe `utc_instant` on `delivery_start`).** `timestamp_utc` and `event_time` equal
   `delivery_start` on every row (checked on all rows): the **start of the delivery window, in UTC**. The
   vendor's package text declares the datetimes UTC; the cells carry no offset suffix, so the UTC typing
   rests on that declaration and not on syntax. There is no shift: the BST-season value
   `2026-03-31T22:00:00` is `22:00Z` (23:00 UK local time). `delivery_end` is the window end, kept as a
   typed UTC datetime but not the recipe column. The endpoint closure (whether the end instant belongs to
   the window) is not stated by the vendor: `TODO: verify` (INTERVAL-CLOSURE).

**Identity and selection.**

- The record key is `unit_result_id`, unique across 7,925 rows; `_latest` = `whole_capture`. All 7,925 keys are in the current by-unit table. The two differ only in numeric lexical form (`5.0` versus `5`, 7,925 rows with a different text form, 0 numerically different).

**Zeros.** `executed_quantity` is never zero; 437 rows have a zero `clearing_price`; no -1 price. Observed: `executed_quantity` 1 to 270 MW, `clearing_price` -13.4 to 30.95 £/MW/h, 317 distinct `auction_unit` values.

**Row counts and shape (silver, 2026-10-13).** 7,925 rows, 0 validation failures, 0 rows excluded; the planned and activated counts agree (RULINGS 741). Silver layout: one Parquet file under `C:/gridflow-data/silver/neso_data_portal/eac_results_daily_by_unit/year=2026/month=10/`; the partition is the **capture** date. Columns (19): the 11 vendor columns, then `timestamp_utc`, `published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id` and `dataset_version` (`1+e1`). All timestamps are tz-aware UTC. No gold view or builder reads this family.

### `eac_results_daily_sell_orders`

- Kind: tabular · archetype: EVT · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| auctionID | `auction_id` | string | — | no | — | — |
| registeredAuctionParticipant | `registered_auction_participant` | string | — | yes | — | — |
| auctionUnit | `auction_unit` | string | — | yes | — | — |
| basketID | `basket_id` | string | — | yes | — | — |
| serviceType | `service_type` | string | — | yes | — | — |
| deliveryStart | `delivery_start` | datetime | `%Y-%m-%dT%H:%M:%S` | no | UTC | — |
| deliveryEnd | `delivery_end` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | — |
| orderID | `order_id` | string | — | no | — | — |
| orderType | `order_type` | string | — | yes | — | — |
| auctionProduct | `auction_product` | string | — | yes | — | — |
| productID | `product_id` | string | — | yes | — | — |
| quantity | `quantity` | float64 | — | yes | — | MW |
| priceLimit | `price_limit` | float64 | — | yes | — | £/MW/h |
| loopedBasketID | `looped_basket_id` | string | — | yes | — | — |
| orderEntryTime | `order_entry_time` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | — |
| acceptanceRatio | `acceptance_ratio` | float64 | — | yes | — | — |
| status | `status` | string | — | yes | — | — |
| executedQuantity | `executed_quantity` | float64 | — | yes | — | MW |
| clearingPrice | `clearing_price` | float64 | — | yes | — | £/MW/h |
| reasonRejected | `reason_rejected` | string | — | yes | — | — |
| flexibleGroupID | `flexible_group_id` | string | — | yes | — | — |
| minimumConsecutiveWindows | `minimum_consecutive_windows` | int64 | — | yes | — | — |

- Entity key: `auction_id`, `order_id`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`delivery_start`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

- **Eligible**, no hold. **Daily** sell orders (latest auction only): resource `8ba48f26-d73e-4094-a90d-ba075eb739c1` (upload, 12,905,812 bytes, 73,098 rows). Header H-O22, 22 columns. The vendor describes the daily resources as results for the **latest auction only**, per day and not aggregated across days. Measured: delivery starts span exactly one delivery day (`2026-10-07T22:00:00` to `2026-10-08T21:30:00`). Only one capture exists, so what a later capture holds is unmeasured. Never add a daily row to its current counterpart. Unlike the main sell-order family, the daily file uses the `T`-separated time form throughout, so its time columns are typed.

**Two clocks.**

1. **Vintage (`ckan_last_modified`).** Every resource is an upload with a usable CKAN timestamp, so
   `published_at` = `available_at` = the CKAN `last_modified` of the captured file (ADR-030): **2026-10-07T13:51:36.544135Z**, one value on all 73,098 rows.
   The capture was written 2026-10-08T10:32:02Z. That is when the file was last uploaded, not when each result was first published: the
   files have no publication column. `TODO: verify` the vendor's original publication instant of each
   result and whether past rows are amended in place when NESO re-uploads: one capture exists.
2. **Event time (temporal recipe `utc_instant` on `delivery_start`).** `timestamp_utc` and `event_time` equal
   `delivery_start` on every row (checked on all rows): the **start of the delivery window, in UTC**. The
   vendor's package text declares the datetimes UTC; the cells carry no offset suffix, so the UTC typing
   rests on that declaration and not on syntax. There is no shift: the BST-season value
   `2026-03-31T22:00:00` is `22:00Z` (23:00 UK local time). `delivery_end` is the window end, kept as a
   typed UTC datetime but not the recipe column. The endpoint closure (whether the end instant belongs to
   the window) is not stated by the vendor: `TODO: verify` (INTERVAL-CLOSURE). `order_entry_time` runs `2026-09-24T12:20:11` to `2026-10-07T12:55:26`: a sell order can be entered well before the auction day (up to roughly two weeks here).

**Identity and selection.**

- The record key is `(auction_id, order_id)`, unique across 73,098 rows; `_latest` = `whole_capture`. All 73,098 keys are in the main sell-order table; the rows differ from it only in numeric lexical form (0 numeric differences).

**Sentinels and zeros.** 6,709 rows have a zero `quantity`, 63,581 a zero `acceptance_ratio`, 64,104 a zero `executed_quantity`, 17,439 a zero `clearing_price`. **8 rows carry a `price_limit` of -1**, kept as `-1.0`, never null. Observed: `price_limit` -20 to 999.99 £/MW/h, `clearing_price` -13.4 to 30.95 £/MW/h, 324 distinct `auction_unit` values. Blank `flexible_group_id`, `minimum_consecutive_windows`, `looped_basket_id` and `reason_rejected` stay null.

**Row counts and shape (silver, 2026-10-13).** 73,098 rows, 0 validation failures, 0 rows excluded; the planned and activated counts agree (RULINGS 741). Silver layout: one Parquet file under `C:/gridflow-data/silver/neso_data_portal/eac_results_daily_sell_orders/year=2026/month=10/`; the partition is the **capture** date. Columns (30): the 22 vendor columns, then `timestamp_utc`, `published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id` and `dataset_version` (`1+e1`). All timestamps are tz-aware UTC. No gold view or builder reads this family.

### `eac_results_daily_summary`

- Kind: tabular · archetype: EVT · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| auctionID | `auction_id` | string | — | no | — | — |
| auctionProduct | `auction_product` | string | — | no | — | — |
| serviceType | `service_type` | string | — | yes | — | — |
| deliveryStart | `delivery_start` | datetime | `%Y-%m-%dT%H:%M:%S` | no | UTC | — |
| deliveryEnd | `delivery_end` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | — |
| clearedVolume | `cleared_volume` | float64 | — | yes | — | MW |
| clearingPrice | `clearing_price` | float64 | — | yes | — | £/MW/h |
| linkedServiceWindowID | `linked_service_window_id` | string | — | yes | — | — |

- Entity key: `auction_id`, `auction_product`, `delivery_start`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`delivery_start`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

- **Eligible**, no hold. **Daily** results summary (latest auction only): resource `3c51a666-1c33-450e-a6eb-c9b4a0c91584` (upload, 23,318 bytes, 324 rows). Header H-S, 8 columns. The vendor describes the daily resources as results for the **latest auction only**, per day and not aggregated across days. Measured: delivery starts span exactly one delivery day (`2026-10-07T22:00:00` to `2026-10-08T21:30:00`). Only one capture exists, so what a later capture holds is unmeasured. Never add a daily row to its current counterpart.

**Two clocks.**

1. **Vintage (`ckan_last_modified`).** Every resource is an upload with a usable CKAN timestamp, so
   `published_at` = `available_at` = the CKAN `last_modified` of the captured file (ADR-030): **2026-10-07T13:50:37.548300Z**, one value on all 324 rows.
   The capture was written 2026-10-08T10:32:06Z. That is when the file was last uploaded, not when each result was first published: the
   files have no publication column. `TODO: verify` the vendor's original publication instant of each
   result and whether past rows are amended in place when NESO re-uploads: one capture exists.
2. **Event time (temporal recipe `utc_instant` on `delivery_start`).** `timestamp_utc` and `event_time` equal
   `delivery_start` on every row (checked on all rows): the **start of the delivery window, in UTC**. The
   vendor's package text declares the datetimes UTC; the cells carry no offset suffix, so the UTC typing
   rests on that declaration and not on syntax. There is no shift: the BST-season value
   `2026-03-31T22:00:00` is `22:00Z` (23:00 UK local time). `delivery_end` is the window end, kept as a
   typed UTC datetime but not the recipe column. The endpoint closure (whether the end instant belongs to
   the window) is not stated by the vendor: `TODO: verify` (INTERVAL-CLOSURE).

**Identity and selection.**

- The record key is `(auction_id, auction_product, delivery_start)`, unique across 324 rows; `_latest` = `whole_capture`. All 324 keys are in the current summary and the rows are lexically identical to it.

**Zeros.** 94 rows have a zero `cleared_volume` and 120 a zero `clearing_price`; no -1 price. Observed: `cleared_volume` 0 to 1,821 MW, `clearing_price` -13.4 to 30.95 £/MW/h.

**Row counts and shape (silver, 2026-10-13).** 324 rows, 0 validation failures, 0 rows excluded; the planned and activated counts agree (RULINGS 741). Silver layout: one Parquet file under `C:/gridflow-data/silver/neso_data_portal/eac_results_daily_summary/year=2026/month=10/`; the partition is the **capture** date. Columns (16): the 8 vendor columns, then `timestamp_utc`, `published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id` and `dataset_version` (`1+e1`). All timestamps are tz-aware UTC. No gold view or builder reads this family.

### `eac_results_sell_orders`

- Kind: tabular · archetype: EVT · refresh: daily · empty allowed: no

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

Schema, epoch 2:

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

- Entity key: `resource_id`, `auction_id`, `order_id`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

- **Eligible**, no hold. **Sell orders**: 36 resources, the datastore dump `13b511df-d6ec-4143-afb1-0ecc6fd19810` (107,670,541 bytes, 588,221 rows, delivery `2026-09-30T22:00:00` to `2026-10-08T21:30:00`, 8 auctions) and 35 monthly uploaded archives `202311` to `202609` (31,701,980 rows, mutually key-disjoint and disjoint from the dump); 32,290,201 rows in all, 1,071 auction IDs, 540 distinct `auction_unit` values. One row per sell order: `PARENT` 10,574,379, `CHILD` 17,243,839, `SUBSTITUTABLECHILD` 4,471,983. **Two header epochs**, selected by exact header, never by date: epoch 1 is H-O22 (22 columns) for 31 resources; epoch 2 is H-O20 (the same without `flexibleGroupID` and `minimumConsecutiveWindows`) for the five archives `202411`, `202412`, `202501`, `202502`, `202503` (`39c7648c-d43b-4ef9-b689-a82619245cda`, `0a6325b9-1b78-4ee2-a1a0-647aa3b6d014`, `3c03d431-7f94-4009-903d-8a4df1aea9f4`, `5997f602-24f1-4f44-aa36-c7b898229d60`, `02c3ede4-6909-4c7b-9b77-511c774decb2`). The change is not monotonic: archives re-exported later include the added columns. For H-O20 rows the two absent columns are null in silver. The family is large (5.8 GB of bronze CSV, 36 captures); silver is one Parquet file per capture.

**Two clocks.**

1. **Vintage (`capture_fallback` for the whole mixed family).** The dump is a datastore resource, so the family as a whole takes the gridflow capture time (record rule V-8): `published_at` is **null** and `available_at` is each resource's own capture time (`written_at`, 36 distinct values from 2026-10-08T10:32:59Z to 2026-10-08T10:36:08Z, equal to `capture_written_at` on all rows). The 35 archives therefore also stamp capture time, not their upload `last_modified` (2026-03-03 to 2026-10-01); this is conservative and never earlier than true availability. An as-of query before 2026-10-08T10:32:59Z sees **no** rows. `TODO: verify` original publication instants and whether past archives are amended in place: one capture per resource exists.

2. **Event time (temporal recipe `none`).** `timestamp_utc` and `event_time` equal `capture_written_at` on
   **every row**: this family has **no delivery-based event time**. All three time columns (`delivery_start`, `delivery_end`,
   `order_entry_time`) are kept as **raw strings**, exactly as served. NESO's package text declares the datetimes UTC, so the
   semantics are documented, but no parse is applied. The reason is a measured format split: the `202607` archive
   (`fc52a1fa-6ce5-4c35-a661-be1b49c1c48f`) writes **every** delivery and submission cell with a **space** separator
   (`2026-06-30 22:00:00`; all 2,291,298 of its rows), while the other 35 bodies use the **`T`** form
   (`2026-10-01T10:00:00`). A single format string cannot read both, and the per-filename format map is limited to date
   columns (ADR-039), so the whole family keeps strings and the typed alternative is deferred to a later mechanism. A consumer
   parses the strings itself (`T` for 35 resources, space for `202607`), reading them as UTC; the endpoint closure is not stated
   by the vendor (`TODO: verify`, INTERVAL-CLOSURE). Do not use `timestamp_utc` as a delivery time.

**Identity and selection.**

- The record key is `(resource_id, auction_id, order_id)` with `_latest` = `whole_capture` per `resource_id` (ADR-039): the dump and all archives are kept. `(auction_id, order_id)` is unique across the whole 32,290,201-row union (archive union 31,701,980 keys, 588,221 dump keys, 0 shared). `resource_id` stays in the key because the family is resource-partitioned. No `key_latest`; `TODO: verify` order identity across re-exports (EAC-ORDER-REVISION-IDENTITY).
- Each of the 73,098 daily sell-order keys is in the dump.

**Sentinels, zeros and blanks.** Zero counts over the whole family: 4,175,836 rows with a zero `quantity`, 27,201,046 with a zero `acceptance_ratio`, 27,774,634 with a zero `executed_quantity`, 4,916,127 with a zero `clearing_price` (zero executed quantity does not by itself identify a rejected order). **-1 occurs as a price**: 6,879 `price_limit` cells and 8,273 `clearing_price` cells; they are signed prices, kept as `-1.0`, never null. Observed: `price_limit` -20 to 999.99 £/MW/h, `clearing_price` -20 to 230 £/MW/h, `quantity` 0 to 300 MW, `executed_quantity` 0 to 270 MW, `acceptance_ratio` 0 to 1. `reason_rejected` is blank on 5,224,051 rows. `flexible_group_id` and `minimum_consecutive_windows` are **blank on every row of every archive through `202603`** and only populated from the `202604` archive and the dump (partly), so they say nothing about the earlier months.

**Row counts and shape (silver, 2026-10-13).** 32,290,201 rows, 0 validation failures, 0 rows excluded; planned and activated counts agree (RULINGS 741), and every one of the 36 resources equals its bronze row count. The family was transformed **alone and last**, with a peak working set of **3,745.0 MiB** (RULINGS 742). Silver layout: 36 Parquet files (~279 MB in total) under `C:/gridflow-data/silver/neso_data_portal/eac_results_sell_orders/year=2026/month=10/`; the partition is the **capture** date. Columns (31): `resource_id` first, the 22 vendor columns (the three time columns as `string`), then `timestamp_utc`, `published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id` and `dataset_version` (`1+e1`). `dataset_version` is `1+e1` on every row, including the H-O20 archives; `TODO: verify` what the `+e1` suffix encodes. No gold view or builder reads this family.

### `eac_results_summary`

- Kind: tabular · archetype: EVT · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| auctionID | `auction_id` | string | — | no | — | — |
| auctionProduct | `auction_product` | string | — | no | — | — |
| serviceType | `service_type` | string | — | yes | — | — |
| deliveryStart | `delivery_start` | datetime | `%Y-%m-%dT%H:%M:%S` | no | UTC | — |
| deliveryEnd | `delivery_end` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | — |
| clearedVolume | `cleared_volume` | float64 | — | yes | — | MW |
| clearingPrice | `clearing_price` | float64 | — | yes | — | £/MW/h |
| linkedServiceWindowID | `linked_service_window_id` | string | — | yes | — | — |

- Entity key: `auction_id`, `auction_product`, `delivery_start`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`delivery_start`)

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

- **Eligible**, no hold. **Current** results summary: resource `596f29ac-0387-4ba4-a6d3-95c243140707` (datastore dump, 4,442,879 bytes, 61,884 rows). One row per auction, product and delivery window. Header H-S, 8 columns, one epoch.

**Two clocks.**

1. **Vintage (`capture_fallback`).** The current table is a datastore dump, so `published_at` is **null**
   and `available_at` is the **gridflow capture time** (sidecar `written_at`), **2026-10-08T10:36:10.800537Z**, one value on
   all rows. That is when gridflow fetched the dump, **not when NESO published each result**. The dump's
   CKAN `last_modified` (2026-04-15T11:41:56.782602) is stale against its own rows and is not used (record rule V-8). Every
   row, including results delivered months earlier, carries the same 2026-10-08 `available_at`, so an
   as-of query before 2026-10-08T10:36:10Z sees **no** rows of this family and a point-in-time backtest cannot use it to
   say when a past result became known. These are event results, so the forward-target rule for
   forecasts (RULINGS 529) does not apply. `TODO: verify` the vendor's original publication instant of
   each result and whether past rows are amended in place at the daily refresh: one capture exists.
2. **Event time (temporal recipe `utc_instant` on `delivery_start`).** `timestamp_utc` and `event_time` equal
   `delivery_start` on every row (checked on all rows): the **start of the delivery window, in UTC**. The
   vendor's package text declares the datetimes UTC; the cells carry no offset suffix, so the UTC typing
   rests on that declaration and not on syntax. There is no shift: the BST-season value
   `2026-03-31T22:00:00` is `22:00Z` (23:00 UK local time). `delivery_end` is the window end, kept as a
   typed UTC datetime but not the recipe column. The endpoint closure (whether the end instant belongs to
   the window) is not stated by the vendor: `TODO: verify` (INTERVAL-CLOSURE). Delivery starts run `2026-03-31T22:00:00` to `2026-10-08T21:30:00`.

**Identity and selection.**

- The record key is `(auction_id, auction_product, delivery_start)`: unique across 61,884 rows. `delivery_start` is a required key column. `(auction_id, auction_product)` alone **repeats** (59,592 duplicate-excess rows in this table), because one product clears in several windows. `_latest` is `whole_capture`; the vendor gives no revision guarantee for a summary row (`TODO: verify`), so no `key_latest`.
- Current and FY keys are disjoint (0 shared); all 324 daily keys are in this table, lexically identical.

**Zeros.** 15,919 rows have a zero `cleared_volume` and 22,799 a zero `clearing_price`; no -1 price. Observed: `cleared_volume` 0 to 1,899 MW, `clearing_price` -20 to 230 £/MW/h, 191 auction IDs. `linked_service_window_id` is optional and stays null when blank.

**Row counts and shape (silver, 2026-10-13).** 61,884 rows, 0 validation failures, 0 rows excluded; the planned and activated counts agree (RULINGS 741). Silver layout: one Parquet file under `C:/gridflow-data/silver/neso_data_portal/eac_results_summary/year=2026/month=10/`; the partition is the **capture** date. Columns (16): the 8 vendor columns, then `timestamp_utc`, `published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id` and `dataset_version` (`1+e1`). All timestamps are tz-aware UTC. No gold view or builder reads this family.

### `eac_results_summary_fy`

- Kind: tabular · archetype: EVT · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| auctionID | `auction_id` | string | — | no | — | — |
| auctionProduct | `auction_product` | string | — | no | — | — |
| serviceType | `service_type` | string | — | yes | — | — |
| deliveryStart | `delivery_start` | datetime | `%Y-%m-%dT%H:%M:%S` | no | UTC | — |
| deliveryEnd | `delivery_end` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | — |
| clearedVolume | `cleared_volume` | float64 | — | yes | — | MW |
| clearingPrice | `clearing_price` | float64 | — | yes | — | £/MW/h |
| linkedServiceWindowID | `linked_service_window_id` | string | — | yes | — | — |

- Entity key: `resource_id`, `auction_id`, `auction_product`, `delivery_start`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: utc_instant (`delivery_start`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

- **Eligible**, no hold. **FY archive** results summary: three upload resources, FY2023 `be5c6b0d-a335-4859-93f2-389585b4e9a1` (5,400 rows), FY2024 `ab130833-3ce4-4361-90fb-69fa3cf30f15` (24,464) and FY2025 `be55ee51-b79e-47da-b71e-a0f8865d9d66` (62,864); 92,728 rows. Same 8-column header as the current table.

**Two clocks.**

1. **Vintage (`ckan_last_modified`).** Every resource is an upload with a usable CKAN timestamp, so
   `published_at` = `available_at` = the CKAN `last_modified` of the captured file (ADR-030): FY2023 **2026-04-15T11:11:47.892835Z**, FY2024 **2026-04-15T11:15:14.025635Z**, FY2025 **2026-04-15T11:19:18.288047Z**.
   Every result back to November 2023 carries a 2026-04 `available_at`; an as-of query before 2026-04-15T11:11:47Z sees **no** rows. That is when the file was last uploaded, not when each result was first published: the
   files have no publication column. `TODO: verify` the vendor's original publication instant of each
   result and whether past rows are amended in place when NESO re-uploads: one capture exists.
2. **Event time (temporal recipe `utc_instant` on `delivery_start`).** `timestamp_utc` and `event_time` equal
   `delivery_start` on every row (checked on all rows): the **start of the delivery window, in UTC**. The
   vendor's package text declares the datetimes UTC; the cells carry no offset suffix, so the UTC typing
   rests on that declaration and not on syntax. There is no shift: the BST-season value
   `2026-03-31T22:00:00` is `22:00Z` (23:00 UK local time). `delivery_end` is the window end, kept as a
   typed UTC datetime but not the recipe column. The endpoint closure (whether the end instant belongs to
   the window) is not stated by the vendor: `TODO: verify` (INTERVAL-CLOSURE). Delivery starts run `2023-11-02T23:00:00` to `2026-03-31T21:30:00`; by resource FY2023 `2023-11-02T23:00:00` to `2024-03-31T18:00:00`, FY2024 `2024-03-31T22:00:00` to `2025-03-31T21:30:00`, FY2025 `2025-03-31T22:00:00` to `2026-03-31T21:30:00`.

**Identity and selection.**

- The record key is `(resource_id, auction_id, auction_product, delivery_start)` with `_latest` = `whole_capture` per `resource_id` (ADR-039). The summary key is unique across the 92,728 rows and the three archives are mutually key-disjoint. `(auction_id, auction_product)` alone repeats (86,176 duplicate-excess rows across the archives). No `key_latest`.

**Sentinels and zeros.** 6,706 rows have a zero `cleared_volume` and 12,227 a zero `clearing_price`; **37 rows carry a `clearing_price` of -1**, kept as `-1.0`, never null. Observed: `cleared_volume` 0 to 1,646 MW, `clearing_price` -20 to 159.69 £/MW/h, 880 auction IDs.

**Row counts and shape (silver, 2026-10-13).** 92,728 rows, 0 validation failures, 0 rows excluded; the planned and activated counts agree (RULINGS 741). Silver layout: three Parquet files (one per resource) under `C:/gridflow-data/silver/neso_data_portal/eac_results_summary_fy/year=2026/month=10/`; the partition is the **capture** date. Columns (17): `resource_id` first, then the 8 vendor columns, then `timestamp_utc`, `published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id` and `dataset_version` (`1+e1`). All timestamps are tz-aware UTC. No gold view or builder reads this family.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Daily

The vendor says the package is updated daily, and its note says the four daily files were added to populate from 5 May 2026
and hold the latest auction only. gridflow has **one capture per resource** (all 2026-10-08), so the real rhythm, whether the
current dumps are re-trimmed or extended each day, whether the monthly sell archives are closed when a month ends, and
whether a refresh replaces or appends to a file are unmeasured. `TODO: verify` by comparing later complete captures with the
hash-pinned bodies (K-AS-3 FACTS section 2). The catalogue snapshot of 2026-10-06 and the captures of 2026-10-08 are consistent
with a refresh at least every couple of days. The registry sets a 512 MiB download cap (`max_download_bytes` 536,870,912): the
newest monthly sell archives are 407 to 438 MB (the largest, `202605`, is 438,169,445 bytes), so a larger month would fail
capture (the sibling `eac_br_results_sell_orders` already hit this cap). That is a later unit, not a defect of this page.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence). gridflow outputs derived from this
package carry the attribution line "Supported by National Energy SO Open Data".

## Holds

- none

**No family in this package is held.** All eleven were specified as eligible (RULINGS 738) and activated as such (RULINGS 741, 742), so
there is no hold question or hold unit to state. The sibling mock auction package is a different package with its own
dispositions; nothing here applies to it.

**Open questions that do not hold any output** (K-AS-3 FACTS, carried verbatim as non-holding TODOs):

- `TODO: verify` the **original publication instant** of auction results. The vintage is the capture time (current dumps, all sell
  orders) or the upload time (FY and daily files), never a publication time; the full history of every table carries a 2026 `available_at`.
- `TODO: verify` **interval closure** (INTERVAL-CLOSURE): no source states whether a window's end instant belongs to it.
- `TODO: verify` **order identity across corrected re-exports** (EAC-ORDER-REVISION-IDENTITY): measured uniqueness of `(auction_id, order_id)`
  does not authorise `key_latest`.
- `TODO: verify` the **out-of-range acceptance ratio** (EAC-BUY-ACCEPTANCE-RANGE): one current buy-order row has `acceptance_ratio`
  1.049999949856768 against a documented 0 to 1.
- `TODO: verify` the **amendment and deletion behaviour** of resources: one capture each.

**Known issues and gotchas.**

- **Same `available_at` for all history.** The current dumps and every sell order carry the 2026-10-08 capture time; the FY files carry
  2026-04-15; the daily files carry 2026-10-07. A point-in-time backtest cannot use these tables to say when a past result became known.
- **Never sum across scopes.** Each daily file repeats the latest auction already inside the current table (shared keys: 7,925 by unit, 720 buy
  orders, 324 summary, 73,098 sell orders); the lexical differences are numeric forms only (`5.0` versus `5`) in the by-unit and sell-order
  files, and the buy-order and summary files are identical. The current segment and the FY archives share **no** keys, and the FY archives
  and monthly sell archives are mutually key-disjoint. The current dump is **not** the union of the archives: it holds a later segment.
  gridflow keeps the scopes as separate records and provides no merged view.
- **Dictionary versus body.** The dictionary lists `status` values `EXECUTED, REJECTED, EXCLUDED` but the bodies also contain
  `PARTIALLY_EXECUTED` and no `EXCLUDED`. It lists `serviceType` values Response, Quick Reserve and Slow Reserve but the bodies also carry
  `Balancing Reserve`, and it lists ten product codes while the bodies also carry `NBR` and `PBR` (the Balancing Reserve products; `TODO: verify`
  their definition and the mapping from every code to its product name, since the dictionary example for `auctionProduct` is a name,
  `Dynamic Containment LF`, not a code). The dictionary example for the buy-order times carries a `Z` suffix; the served cells do not. The
  `reasonRejected` entry says only "Reason Codes": `TODO: verify` the code meanings (the profiler sees integers, silver keeps strings).
- **Windows are not all the same length.** Over the complete summary union response windows are 14,400 s (38,526 rows), 10,800 s (18 rows)
  and 18,000 s (12 rows), and every measured reserve window is 1,800 s (K-AS-3 FACTS section 3.5); window edges match the established
  local EFA boundaries with 0 mismatches. `TODO: verify` that the 3-hour and 5-hour rows are the clock-change days. Reconstruct no
  timestamp from `auctionID` or product.
- **Sell-order times are strings with two layouts.** See the sell-order family: `T` for 35 resources, a space for `202607`.
- **`unit_result_id` is opaque** and `auction_unit` may be a collection of assets: keep both as served.
- **Submission time is not result time.** `order_entry_time` is when the bid was submitted. The outcome columns (`executed_quantity`,
  `clearing_price`, `acceptance_ratio`, `status`) exist only after the auction cleared, so submission time is not evidence that
  they were available at submission. A sell order can be entered up to about two weeks before its auction day.
- **Zeros are results.** A zero executed quantity, volume or price is a real value; do not null or drop it. Prices can be negative
  (minimum -20 £/MW/h observed) and `-1` appears as a price.
- **Size.** The sell-order family is 5.8 GB of bronze and 32.3 million rows; a full transform is a seat-level job (peak 3,745.0 MiB).

**Activation (2026-10-13, master `0f7bd1d`, PR #114).** Research AS-3 (RULINGS 736) read 26 families and 37,069,169 CSV rows parsed
faithfully; the batch was split into AS-3a (this package, 11 families) and AS-3b (RULINGS 737) and the specs ratified (RULINGS 738). AS-3a merged
triple-green (RULINGS 740: CI green, the Sol diff review approved on the first pass with no findings, verification passed), with no engine
change. The families were transformed from the 2026-10-08 captures with `--start/--end 2026-10-08`; there was no prior silver, so
nothing was overwritten and no snapshot was taken (RULINGS 741). Counts: by unit 1,444,630; by unit FY 1,900,738; daily by unit 7,925;
buy orders 139,306; buy orders FY 323,894; daily buy orders 720; summary 61,884; summary FY 92,728; daily summary 324; daily sell orders
73,098; sell orders 32,290,201; **total 36,335,448**, each equal to the spec plan. All 11 eligible, none held. The batch-wide
`reconcile --all --cutoff 2026-10-12` exited 0 over 181 families with 0 gaps (47 adjudicated, 0 stale; RULINGS 742). The receipt is in
@.planning/v0.22-RESULTS.md section AS-3a; the evidence is @.planning/phases/v0.22-K-AS-3/K-AS-3-FACTS.md and the spec
@.planning/phases/v0.22-K-AS-3/K-AS-3a-SPEC.md.
