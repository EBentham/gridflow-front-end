---
source: "neso_data_portal"
package: "dynamic-containment-data"
dataset_keys: ["dynamic_containment_dc_dr_dm_block", "dynamic_containment_dc_dr_dm_linear", "dynamic_containment_dc_dr_dm_results", "dynamic_containment_dc_dr_dm_results_sum", "dynamic_containment_masterdata"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-13
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Dynamic Containment, Regulation and Moderation auction results

> **Retired package. Auction results, not requirement forecasts.** NESO states this package will no longer
> be updated and directs users to the Enduring Auction Capability (EAC) for newer results. It records what
> the legacy auctions **procured and cleared**, never how much NESO said it needed. The two must not be
> joined or summed. Two of the five families are held (below).

This package is NESO's published history of the **legacy frequency-response auctions for Dynamic
Containment (DC), Dynamic Regulation (DR) and Dynamic Moderation (DM)**, the frequency services NESO bought
before the EAC platform took over. It splits into two regimes with different structures, kept as **five
separate families** because the headers and the grain differ (NESO
[package page](https://www.neso.energy/data-portal/dynamic-containment-data)):

1. A **first-regime tender** (the upload, `dynamic_containment_masterdata`): one row per DC low-frequency
   tender bid with its volumes, fee and rejection reason, for delivery from 2020-10-02 to 2021-09-15.
2. A **later auction regime** (four datastore tables): the **results by unit**, the **results summary** per
   service and block, and the underlying **block orders** and **linear (bid-curve) orders**, for EFA dates
   from 2021-09-16 to 2023-11-02.

Use the results-by-unit and masterdata tables to see who was procured, how much, and at what price in the
legacy regime. They are history only: for current procurement read the EAC package
(@./eac-auction-results.md).

**Relation to the forecast pages.** The requirement forecasts live in other packages
(@./dynamic-containment-4-day-forecast.md, @./dynamic-regulation-requirements.md,
@./dynamic-moderation-requirements.md, @./long-term-forecasts-for-dc-dm-dr-requirements.md). The AS-1
current DC forecast shares **no target dates** with these results, but the forecast **history** shares 561
date labels with them (2022-04-21 to 2023-11-02; K-AS-4 FACTS section 6). A shared date label is not a shared
meaning: a requirement forecast and an accepted auction result are different measures. Never join them on
date and never add them.

**Held outputs.** `dynamic_containment_dc_dr_dm_results_sum` (hold DC-SUMMARY-PRICE-UNIT) and
`dynamic_containment_dc_dr_dm_linear` (hold DC-LINEAR-PRICE-UNITS) are **held**: silver is written and
reconciled but nothing is released to consumers. For those two, this page states the schema, row counts,
clocks and hold questions only, and **no data values** (no sample rows, no value ranges or statistics).
The other three families (block orders, results by unit, masterdata) are eligible.

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: EVT
- Package id: `aca07dcb-f807-409c-a4ec-da5dc052b8ba`
- Background: @../../../20-domain/concepts/settlement-period.md (EFA blocks are not settlement periods; the
  link is context for the local-clock handling only), @../../../20-domain/markets/gb-balancing-mechanism.md

## Files by disposition

All five resources are disposition **SILVER** (a CKAN datastore dump or an uploaded CSV that gridflow
parses). There are **no DOC, HOLD or SKIP resources** in this package, so there are no document download
links. Every resource has exactly one capture (2026-10-08), so amendments and deletions between captures are
unmeasured.

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| DC, DR & DM Block Orders Master Data 2021-2023 | CSV | dump | `6fd8e042-be27-4c67-ad59-5acdd2a7b0fd` |
| DC, DR & DM Linear Orders Master Data 2021-2023 | CSV | dump | `26aefbcc-fce0-403f-80e1-4a26af3fe84b` |
| DC, DR & DM Results By Unit Master Data 2021-2023 | CSV | dump | `ddc4afde-d2bd-424d-891c-56ad49c13d1a` |
| DC, DR & DM Results Summary Master Data 2021-2023 | CSV | dump | `888e5029-f786-41d2-bc15-cbfd1d285e96` |
| Dynamic Containment Masterdata | CSV | upload | `0b8dbc3c-e05e-44a4-b855-7dd1aa079c68` |

**Where each resource is fetched from** (sidecar `request_url`; bronze under
`C:/gridflow-data/bronze/neso_data_portal/<family>/2026/10/08/`, file name
`raw_<stamp>_<resource-id>_<first-8-of-sha256>.csv`, immutable).

| Family | Fetch URL | Bronze capture |
|---|---|---|
| `dynamic_containment_masterdata` | `https://api.neso.energy/dataset/aca07dcb-f807-409c-a4ec-da5dc052b8ba/resource/0b8dbc3c-e05e-44a4-b855-7dd1aa079c68/download/dynamic_containment_masterdata.csv` | 2026-10-08T10:12:23Z, 1,687,187 bytes |
| `dynamic_containment_dc_dr_dm_results_sum` | `https://api.neso.energy/datastore/dump/888e5029-f786-41d2-bc15-cbfd1d285e96` | 2026-10-08T10:12:20Z, 1,504,029 bytes |
| `dynamic_containment_dc_dr_dm_results` | `https://api.neso.energy/datastore/dump/ddc4afde-d2bd-424d-891c-56ad49c13d1a` | 2026-10-08T10:12:05Z (sidecar `written_at`), 45,481,922 bytes |
| `dynamic_containment_dc_dr_dm_linear` | `https://api.neso.energy/datastore/dump/26aefbcc-fce0-403f-80e1-4a26af3fe84b` | 2026-10-08T10:11:20Z, 9,437,913 bytes |
| `dynamic_containment_dc_dr_dm_block` | `https://api.neso.energy/datastore/dump/6fd8e042-be27-4c67-ad59-5acdd2a7b0fd` | 2026-10-08T10:11:19Z, 155,259,593 bytes |

Vendor dictionaries (human pages): [masterdata](https://www.neso.energy/data-portal/dynamic-containment-data/dynamic_containment_masterdata),
[results summary](https://www.neso.energy/data-portal/dynamic-containment-data/dc_dr__dm_results_summary_master_data_2021-2023),
[results by unit](https://www.neso.energy/data-portal/dynamic-containment-data/dc_dr__dm_results_by_unit_master_data_2021-2023),
[linear orders](https://www.neso.energy/data-portal/dynamic-containment-data/dc_dr__dm_linear_orders_master_data_2021-2023).
The block-orders dictionary page address is not recorded in the research files (`TODO: verify`; start from the
[package page](https://www.neso.energy/data-portal/dynamic-containment-data)). The CTS++ auction guide that
FACTS cites for the curve, MAR and signed-quantity conventions is
[NESO document 155846](https://www.neso.energy/document/155846/download).
Saved field info: `.planning/research/neso-snapshots/field-info/20261008T114228Z/dynamic_containment_*.json`.

All five bodies are valid UTF-8 (the records declare strict UTF-8) and the production CSV reader agreed
with a strict second parse on every row and cell. No body has embedded quotes, commas or newlines in a cell.

## The two clocks, family by family

Every silver row carries a **vintage** clock (`available_at`: when the data was available) and an **event**
clock (`event_time`: what the row is about). All five families use `issue: none`: no result or order has an
evidenced publication instant. `OrderEntryTime` is the bid **submission** time, not the publication of the
later result, so it is never used as an issue time.

| Family | Vintage clock (`available_at`) | Event clock (`event_time`) |
|---|---|---|
| `dynamic_containment_masterdata` | CKAN `last_modified` of the captured upload (ADR-030): `published_at` = `available_at` = 2026-05-29T12:35:35Z on every row | `utc_instant(delivery_start)`: the vendor-declared UTC service start |
| `dynamic_containment_dc_dr_dm_results` | `capture_fallback`: gridflow capture time (sidecar `written_at`); `published_at` null | `date_sp1(efa_date)`: start of the UK-local EFA date, as UTC (a date anchor, not a block start) |
| `dynamic_containment_dc_dr_dm_results_sum` (held) | `capture_fallback`; `published_at` null | `date_sp1(efa_date)`: as above |
| `dynamic_containment_dc_dr_dm_linear` (held) | `capture_fallback`; `published_at` null | **`none`**: `timestamp_utc` and `event_time` are the **capture time** |
| `dynamic_containment_dc_dr_dm_block` | `capture_fallback`; `published_at` null | **`none`**: `timestamp_utc` and `event_time` are the **capture time** |

**What `none` means here.** For the linear and block families `timestamp_utc` is the time gridflow fetched
the file (equal to `capture_written_at` on every row, checked in silver on 2026-10-13). It is **not** a
delivery time or a bid time. Filtering these two tables by `timestamp_utc` filters by fetch time (a single
instant today) and never by delivery date. Their delivery start, delivery end and order-entry times are kept
as raw `string` columns, byte-for-byte as served.

**Why the datastore resources use the capture-time fallback.** A family holding a datastore resource cannot
take the CKAN `last_modified` vintage (registry rule V-8), so the four datastore families use the capture
time: the vintage is never earlier than the moment gridflow could have seen the file. The bronze sidecars do
carry a `ckan_last_modified` for these resources (dated 2023); it is stored only in bronze metadata and is
not a silver clock. The upload-only masterdata keeps the CKAN stamp.

**The naive endpoint strings (DC-RESULT-EXPORT-CLOCK / DC-ORDER-EXPORT-CLOCK).** `delivery_start`,
`delivery_end` and `order_entry_time` in the results, summary, linear and block tables carry no offset. NESO
auction guidance describes GMT/BST delivery windows, which hints at UK local time, but the portal export's
exact clock is not stated. `TODO: verify`. Until NESO answers, do not parse them as UTC and do not parse them
as UK local time. Their roles are known: delivery start / end are the service-window endpoints; order entry is
when the bid was submitted. **EFA labels and dates are never composed into a timestamp** (RULINGS 572, 588);
the `efa` column is an ordinal 1..6 of the four-hour EFA block, with no time zone.

**Settlement periods.** None of the five families has a settlement period or a `run_type`; neither is
fabricated.

## Units and sentinels

**Units come only from the vendor's own dictionaries** (saved field info; K-AS-4 FACTS sections 6.1-6.5); none
is inferred from a column name or from arithmetic.

| Columns | Unit (vendor dictionary) |
|---|---|
| masterdata `volume_offered`, `volume_accepted`; results `cleared_volume`; block `volume`, `executed_volume`; linear `executed_volume`, `v1`..`v32`; summary `cleared_volume` | **MW** |
| results `clearing_price` | **£/MW/h** (this resource's own dictionary: "cleared price per MW per hour") |
| block `price`, `clearing_price` | **£/MW as published**; hour basis not stated (`TODO: verify` DC-BLOCK-PRICE-HOUR-BASIS) |
| masterdata `availability_fee`, `total_cost` | **£ as published**; no rate is derived from them |
| masterdata `service_duration` | hours |
| block `mar` | dimensionless minimum acceptance ratio (NESO auction guide) |
| summary `clearing_price` (held) | **unresolved**: description says per MW per hour, unit cell says £/MW (DC-SUMMARY-PRICE-UNIT) |
| linear `p1`..`p32` (held) | **unresolved**: the dictionary's unit cells conflict (DC-LINEAR-PRICE-UNITS) |
| `efa` | block ordinal 1..6; no unit |
| identifiers (`order_id`, `order_period_id`, `trade_id`, `unique_bid_number`, `rejection_code`) | opaque labels; no unit |
| `delivery_start`, `delivery_end`, `order_entry_time` | time labels; UTC ISO 8601 for the masterdata only (dictionary); for the rest the clock is unresolved |

Nothing is converted or rescaled. The masterdata dictionary also puts a unit of "MW" on `Technology Type`;
that is a dictionary error (the column is a categorical string, `technology_type`).

**Typing and sentinels (K-AS-4 FACTS g5; RULINGS 749 ratifies the `NA` and `-1` handling, 748 is the batch
split).** Identifiers are `string` and byte-equal, never cast. `efa` and `service_duration` are `int64`;
measured values are `float64`. **Zeros are real values and stay zero; `-1` stays `-1`** (the block volumes'
sell convention; no sign flip, absolute value or null). **Blank cells in numeric columns are null. Blank cells in string columns are stored two ways**, and the
transformer does not normalise them: the empty string `''` or null, depending on the column (measured in
silver on 2026-10-13). Three columns hold empty strings: block `bid_validity` (728,794 `''`, 0 null), results
`cancelled` (397,662 `''`, 0 null) and results `location` (49,373 `''` plus 9,030 null). Elsewhere a blank
string cell is null: block `block_code_prm` (244,571 null, 0 `''`), masterdata `related_entity` (1,507 null)
and `rejection_code` (9,195 null). When filtering these columns test for both null and `''`
(`TODO: verify` whether the transformer should null the empty strings; it does not today). The literal strings `NA` and `N/A` in string columns are kept byte-equal and are **not**
mapped to null (no token map exists for this package). No thousands separator, percent sign or padded number
was found in any body. No `min` or `max` bound is set on any column.

## Families

The "Vendor unit" column below is the unit stated in the vendor's saved field-info dictionary; it is sparse
because the dictionary states a unit for only some columns, and for the held linear table it reproduces the
conflicting declarations unreconciled. Five families, 1,183,422 silver rows in all:

| Family | Status | Silver rows |
|---|---|---:|
| `dynamic_containment_dc_dr_dm_block` | eligible | 728,794 |
| `dynamic_containment_dc_dr_dm_linear` | **held** (DC-LINEAR-PRICE-UNITS) | 23,154 |
| `dynamic_containment_dc_dr_dm_results` | eligible | 397,662 |
| `dynamic_containment_dc_dr_dm_results_sum` | **held** (DC-SUMMARY-PRICE-UNIT) | 23,424 |
| `dynamic_containment_masterdata` | eligible | 10,388 |

### `dynamic_containment_dc_dr_dm_block`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| MarketName | `market_name` | string | — | yes | — | — |
| BiddingLevelName | `bidding_level_name` | string | — | yes | — | — |
| MemberName | `member_name` | string | — | yes | — | — |
| OrderID | `order_id` | string | — | yes | — | — |
| Portfolio | `portfolio` | string | — | yes | — | — |
| OrderEntryTime | `order_entry_time` | string | — | yes | — | — |
| OrderEntryUser | `order_entry_user` | string | — | yes | — | — |
| SettlementCurrency | `settlement_currency` | string | — | yes | — | — |
| ClearingPrice | `clearing_price` | float64 | — | yes | — | £/MW |
| Price | `price` | float64 | — | yes | — | £/MW |
| MAR | `mar` | float64 | — | yes | — | — |
| Status | `status` | string | — | yes | — | — |
| BlockCode | `block_code` | string | — | yes | — | — |
| BlockCodePRM | `block_code_prm` | string | — | yes | — | — |
| Paradoxically | `paradoxically` | string | — | yes | — | — |
| OrderPeriodID | `order_period_id` | string | — | no | — | — |
| TradeID | `trade_id` | string | — | yes | — | — |
| EFA | `efa` | int64 | — | yes | — | — |
| DeliveryStart | `delivery_start` | string | — | yes | — | — |
| DeliveryEnd | `delivery_end` | string | — | yes | — | — |
| ExecutedVolume | `executed_volume` | float64 | — | yes | — | MW |
| Volume | `volume` | float64 | — | yes | — | MW |
| Invalid | `invalid` | string | — | yes | — | — |
| Bid Validity | `bid_validity` | string | — | yes | — | — |

- Entity key: `order_period_id`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

One row per **block-offer order period** (a bid, with its status, for one EFA block). Resource
`6fd8e042-be27-4c67-ad59-5acdd2a7b0fd` (datastore dump), one capture (2026-10-08, 155,259,593 bytes).
**Silver: 728,794 rows**; one Parquet file under
`C:/gridflow-data/silver/neso_data_portal/dynamic_containment_dc_dr_dm_block/year=2026/month=10/`
(the partition is the capture date), with the 24 vendor columns then `timestamp_utc`, `published_at`,
`bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id`, `dataset_version`
(32 columns). **Status: eligible** (no hold).

- **Key.** `order_period_id` is unique across all 728,794 rows (FACTS, full-body measurement, not a sample).
  `trade_id` is unique too and equals `order_period_id` on every row, so it adds nothing as a key.
- **Clocks.** Vintage `capture_fallback` (capture time); event recipe `none`, so `timestamp_utc`,
  `event_time` and `available_at` all equal `capture_written_at` on every row (checked in silver on
  2026-10-13) and `published_at` is null. The vendor times `order_entry_time`, `delivery_start` and
  `delivery_end` are **raw naive strings** (see the clocks section above).
- **Units (vendor dictionary).** `volume` and `executed_volume` **MW**; `price` and `clearing_price`
  **£/MW as published** (the dictionary gives no hour basis, see the TODO below). `mar` is a dimensionless
  minimum acceptance ratio per the NESO auction guide (it is not a physical quantity) and is `float64`
  because fractional values occur (526 cells).
- **Sell convention and sentinels.** Negative volume is the platform's sell-order convention, not a missing
  value: the whole `volume` column is negative (222,434 cells are literal `-1`) and `executed_volume` is
  negative or zero (103,369 cells are literal `-1`). Stored as published, never absolute-valued, nulled or
  sign-flipped (FACTS g5). `block_code_prm` holds a literal `NA` string on 84,074 rows and is blank on
  244,571; the literal `NA` is kept and the blanks are null. `bid_validity` is blank on every row and is
  stored as the **empty string `''` on all 728,794 rows (0 nulls)**, so a null test on it matches nothing.
- **Flags and free text.** `status`, `invalid`, `paradoxically` and the block codes are categorical strings
  kept byte-equal, including capitalisation.
- `TODO: verify` **DC-BLOCK-PRICE-HOUR-BASIS** (does not hold the output): the block dictionary labels the
  prices £/MW with no hour basis, while the by-unit result table states £/MW/h. Do not equate the block
  prices with the by-unit result price until NESO confirms the rate basis.
- `TODO: verify` the dictionary text still refers to FFR (Firm Frequency Response), "the trial" and the market
  names `DLH` and `LFS`, and describes `MAR` as "automatically infilled, please leave blank". The body
  nevertheless carries fractional `MAR` values and the NESO guide defines MAR; which description is
  authoritative is not established.

### `dynamic_containment_dc_dr_dm_linear`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| MarketName | `market_name` | string | — | yes | — | — |
| BiddingLevelName | `bidding_level_name` | string | — | yes | — | — |
| MemberName | `member_name` | string | — | yes | — | — |
| OrderID | `order_id` | string | — | yes | — | — |
| Portfolio | `portfolio` | string | — | yes | — | — |
| OrderEntryTime | `order_entry_time` | string | — | yes | — | — |
| OrderEntryUser | `order_entry_user` | string | — | yes | — | — |
| SettlementCurrency | `settlement_currency` | string | — | yes | — | — |
| OrderPeriodID | `order_period_id` | string | — | no | — | — |
| TradeID | `trade_id` | string | — | yes | — | — |
| EFA | `efa` | int64 | — | yes | — | — |
| DeliveryStart | `delivery_start` | string | — | yes | — | — |
| DeliveryEnd | `delivery_end` | string | — | yes | — | — |
| ExecutedVolume | `executed_volume` | float64 | — | yes | — | MW |
| 1P | `p1` | float64 | — | yes | — | £/MW |
| 1V | `v1` | float64 | — | yes | — | MW |
| 2P | `p2` | float64 | — | yes | — | £/MW |
| 2V | `v2` | float64 | — | yes | — | MW |
| 3P | `p3` | float64 | — | yes | — | £/MW |
| 3V | `v3` | float64 | — | yes | — | MW |
| 4P | `p4` | float64 | — | yes | — | £/MW |
| 4V | `v4` | float64 | — | yes | — | MW |
| 5P | `p5` | float64 | — | yes | — | MW |
| 5V | `v5` | float64 | — | yes | — | MW |
| 6P | `p6` | float64 | — | yes | — | £/MW |
| 6V | `v6` | float64 | — | yes | — | MW |
| 7P | `p7` | float64 | — | yes | — | £/MW |
| 7V | `v7` | float64 | — | yes | — | MW |
| 8P | `p8` | float64 | — | yes | — | £/MW |
| 8V | `v8` | float64 | — | yes | — | MW |
| 9P | `p9` | float64 | — | yes | — | £/MW |
| 9V | `v9` | float64 | — | yes | — | MW |
| 10P | `p10` | float64 | — | yes | — | £/MW |
| 10V | `v10` | float64 | — | yes | — | MW |
| 11P | `p11` | float64 | — | yes | — | MW |
| 11V | `v11` | float64 | — | yes | — | MW |
| 12P | `p12` | float64 | — | yes | — | MW |
| 12V | `v12` | float64 | — | yes | — | MW |
| 13P | `p13` | float64 | — | yes | — | MW |
| 13V | `v13` | float64 | — | yes | — | MW |
| 14P | `p14` | float64 | — | yes | — | MW |
| 14V | `v14` | float64 | — | yes | — | MW |
| 15P | `p15` | float64 | — | yes | — | £/MW |
| 15V | `v15` | float64 | — | yes | — | MW |
| 16P | `p16` | float64 | — | yes | — | £/MW |
| 16V | `v16` | float64 | — | yes | — | MW |
| 17P | `p17` | float64 | — | yes | — | £/MW |
| 17V | `v17` | float64 | — | yes | — | MW |
| 18P | `p18` | float64 | — | yes | — | £/MW |
| 18V | `v18` | float64 | — | yes | — | MW |
| 19P | `p19` | float64 | — | yes | — | £/MW |
| 19V | `v19` | float64 | — | yes | — | MW |
| 20P | `p20` | float64 | — | yes | — | £/MW |
| 20V | `v20` | float64 | — | yes | — | MW |
| 21P | `p21` | float64 | — | yes | — | MW |
| 21V | `v21` | float64 | — | yes | — | MW |
| 22P | `p22` | float64 | — | yes | — | MW |
| 22V | `v22` | float64 | — | yes | — | MW |
| 23P | `p23` | float64 | — | yes | — | MW |
| 23V | `v23` | float64 | — | yes | — | MW |
| 24P | `p24` | float64 | — | yes | — | MW |
| 24V | `v24` | float64 | — | yes | — | MW |
| 25P | `p25` | float64 | — | yes | — | £/MW |
| 25V | `v25` | float64 | — | yes | — | MW |
| 26P | `p26` | float64 | — | yes | — | £/MW |
| 26V | `v26` | float64 | — | yes | — | MW |
| 27P | `p27` | float64 | — | yes | — | £/MW |
| 27V | `v27` | float64 | — | yes | — | MW |
| 28P | `p28` | float64 | — | yes | — | £/MW |
| 28V | `v28` | float64 | — | yes | — | MW |
| 29P | `p29` | float64 | — | yes | — | £/MW |
| 29V | `v29` | float64 | — | yes | — | MW |
| 30P | `p30` | float64 | — | yes | — | £/MW |
| 30V | `v30` | float64 | — | yes | — | MW |
| 31P | `p31` | float64 | — | yes | — | MW |
| 31V | `v31` | float64 | — | yes | — | MW |
| 32P | `p32` | float64 | — | yes | — | MW |
| 32V | `v32` | float64 | — | yes | — | MW |

- Entity key: `order_period_id`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

One row per **linear (bid-curve) order period**: the same order header fields as the block table, plus a
curve of up to 32 price/volume points (`p1`..`p32`, `v1`..`v32`). Resource
`26aefbcc-fce0-403f-80e1-4a26af3fe84b` (datastore dump), one capture (2026-10-08, 9,437,913 bytes).
**Silver: 23,154 rows**; one Parquet file under
`C:/gridflow-data/silver/neso_data_portal/dynamic_containment_dc_dr_dm_linear/year=2026/month=10/`,
with the 78 vendor-derived columns (14 header columns and 64 curve columns) then the 8 gridflow
columns (86 columns). **Status: HELD (E-SEM, a vendor unit/semantics question).**

**Held; no data values are published for this family.** This page documents the schema, the row count, the
clocks and the hold question only. It gives no sample row and no minimum, maximum, zero or outlier statistic
for any column.

- **Hold, DC-LINEAR-PRICE-UNITS (unit v0.22-K-AS-4a).** The linear-orders dictionary declares the `nP` price
  points in conflicting units (1P-4P, 6P-10P, 15P-20P, 25P-30P as £/MW; 5P as MW with test-placeholder
  text; 11P-14P, 21P-24P, 31P-32P as MW) while the NESO auction guide calls every `nP` a price. What is the
  unit and the hour basis of each `nP` column? The "Vendor unit" column of the schema above reproduces the
  dictionary's own declarations, **unreconciled**; it is not a claim about the true unit. `nV` and
  `ExecutedVolume` are declared MW.
- **Key.** `order_period_id` is unique across the full body; `trade_id` equals it on every row.
- **Clocks.** Vintage `capture_fallback`; event recipe `none`, so `timestamp_utc`, `event_time` and
  `available_at` equal `capture_written_at` on every row (checked in silver on 2026-10-13); `published_at`
  null. `order_entry_time` (bid **submission**, not result publication), `delivery_start` and `delivery_end`
  are raw naive strings (`TODO: verify` DC-ORDER-EXPORT-CLOCK).
- **Curve columns.** A vendor header `1P`..`32V` cannot be a silver name (a silver name starts with a
  letter), so they are `p1`, `v1`, ..., `p32`, `v32`, in header order. The names carry no price or volume
  semantics beyond the vendor letter. All are `float64`; the published width is 32 pairs.
- `TODO: verify` which side of the auction the curve rows describe; the dictionary does not say.

### `dynamic_containment_dc_dr_dm_results`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Company | `company` | string | — | yes | — | — |
| Unit Name | `unit_name` | string | — | no | — | — |
| EFA Date | `efa_date` | date | `%Y-%m-%d` | no | — | — |
| Delivery Start | `delivery_start` | string | — | yes | — | — |
| Delivery End | `delivery_end` | string | — | yes | — | — |
| EFA | `efa` | int64 | — | no | — | — |
| Service | `service` | string | — | no | — | — |
| Cleared Volume | `cleared_volume` | float64 | — | yes | — | MW |
| Clearing Price | `clearing_price` | float64 | — | yes | — | £/MW/h |
| Technology Type | `technology_type` | string | — | yes | — | — |
| Location | `location` | string | — | yes | — | — |
| Cancelled | `cancelled` | string | — | yes | — | — |

- Entity key: `unit_name`, `efa_date`, `efa`, `service`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`efa_date`)

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

One row per **accepted unit result**: a unit, a service and one EFA block on one EFA date. Resource
`ddc4afde-d2bd-424d-891c-56ad49c13d1a` (datastore dump), one capture (2026-10-08, 45,481,922 bytes).
**Silver: 397,662 rows**; one Parquet file under
`C:/gridflow-data/silver/neso_data_portal/dynamic_containment_dc_dr_dm_results/year=2026/month=10/`,
with the 12 vendor columns then the 8 gridflow columns (20 columns). **Status: eligible.**

- **Key.** (`unit_name`, `efa_date`, `efa`, `service`) is unique across the full body. There is no auction id
  column. The vendor-column key was chosen over a delivery-time key so that identity does not depend on the
  unresolved export clock.
- **Clocks.** Vintage `capture_fallback`; `published_at` null. **Event time** is the recipe
  `date_sp1(efa_date)`: `event_time` is the **start of the `efa_date` calendar day in UK local time**,
  expressed in UTC (so 23:00Z the previous day when the date falls in BST, 00:00Z in GMT; silver
  `event_time` runs from 2021-09-15T23:00Z to 2023-11-02T00:00Z). It is a **calendar-date anchor, not the
  start of the EFA block**: the block start is never composed from `efa_date` plus `efa` (RULINGS 572, 588).
  `delivery_start` and `delivery_end` are raw naive strings.
- **Coverage.** EFA dates 2021-09-16 to 2023-11-02, six service codes (`DCL`, `DCH`, `DRL`, `DRH`, `DML`,
  `DMH`), `efa` 1..6.
- **Units (this resource's own dictionary).** `cleared_volume` **MW**; `clearing_price` **£/MW/h**
  (the dictionary: "cleared price per MW per hour"), stated explicitly by this resource's own dictionary.
- **Sentinels and strings.** `technology_type` holds a literal `NA` on 19,601 rows; kept as the string `NA`
  (no token map). `location` has 58,403 blank cells, stored as 9,030 null plus 49,373 empty string
  (`''`), so blank is not uniformly null for this column. `cancelled` is blank on every row and is stored as
  the empty string `''` on all 397,662 rows (0 nulls); no cancellation state is invented.
- `TODO: verify` **DC-RESULT-EXPORT-CLOCK**: the clock of the naive `delivery_start` / `delivery_end` strings.
  The literal interval between them is 240 minutes on every row, which is literal-clock arithmetic and not
  proof of a four-hour UTC duration across a DST change. The by-unit dictionary also describes `EFA Date` as
  the "equivalent date to the delivery end date in this instance"; `TODO: verify` that against the data
  before relying on it.

### `dynamic_containment_dc_dr_dm_results_sum`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Service | `service` | string | — | no | — | — |
| EFA Date | `efa_date` | date | `%Y-%m-%d` | no | — | — |
| Delivery Start | `delivery_start` | string | — | yes | — | — |
| Delivery End | `delivery_end` | string | — | yes | — | — |
| EFA | `efa` | int64 | — | no | — | — |
| Cleared Volume | `cleared_volume` | float64 | — | yes | — | MW |
| Clearing Price | `clearing_price` | float64 | — | yes | — | £/MW |

- Entity key: `service`, `efa_date`, `efa`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`efa_date`)

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

One row per **service, EFA date and EFA block** (the cleared total for that block). Resource
`888e5029-f786-41d2-bc15-cbfd1d285e96` (datastore dump), one capture (2026-10-08, 1,504,029 bytes).
**Silver: 23,424 rows**; one Parquet file under
`C:/gridflow-data/silver/neso_data_portal/dynamic_containment_dc_dr_dm_results_sum/year=2026/month=10/`,
with the 7 vendor columns then the 8 gridflow columns (15 columns). **Status: HELD (E-SEM, a vendor
unit/semantics question).**

**Held; no data values are published for this family.** This page documents the schema, the row count, the
clocks and the hold question only. It gives no sample row and no minimum, maximum or other statistic for
`cleared_volume` or `clearing_price`.

- **Hold, DC-SUMMARY-PRICE-UNIT (unit v0.22-K-AS-4a).** The DC/DR/DM results-summary dictionary describes
  Clearing Price as a price per MW per hour but gives its unit as £/MW (the by-unit results table states
  £/MW/h); which rate dimension does this export publish? The delivery start/end cells are naive and their
  export clock is also undocumented. `cleared_volume` is MW per the dictionary.
- **Key.** (`service`, `efa_date`, `efa`) is unique across the full body.
- **Clocks.** Vintage `capture_fallback`; `published_at` null. Event recipe `date_sp1(efa_date)`: a
  calendar-date anchor at the start of the UK-local `efa_date`, not an EFA block start. `delivery_start` and
  `delivery_end` are raw naive strings (`TODO: verify` DC-RESULT-EXPORT-CLOCK).

### `dynamic_containment_masterdata`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Market Name | `market_name` | string | — | yes | — | — |
| Delivery Date | `delivery_date` | date | `%d/%m/%Y` | yes | — | — |
| Unique bid number | `unique_bid_number` | string | — | no | — | — |
| Response Unit | `response_unit` | string | — | yes | — | — |
| Unit type | `unit_type` | string | — | yes | — | — |
| Agent/Applicant | `agent_applicant` | string | — | yes | — | — |
| Related Entity | `related_entity` | string | — | yes | — | — |
| Volume offered | `volume_offered` | float64 | — | yes | — | MW |
| Volume Accepted | `volume_accepted` | float64 | — | yes | — | MW |
| Delivery Start UTC | `delivery_start` | datetime | `%Y-%m-%dT%H:%M:%SZ` | no | UTC | UTC ISO 8601 |
| Delivery End UTC | `delivery_end` | datetime | `%Y-%m-%dT%H:%M:%SZ` | yes | UTC | UTC ISO 8601 |
| Service Duration | `service_duration` | int64 | — | yes | — | — |
| Availability Fee | `availability_fee` | float64 | — | yes | — | £ |
| Total Cost | `total_cost` | float64 | — | yes | — | £ |
| RTM/no RTM | `rtm_no_rtm` | string | — | yes | — | — |
| Accepted/Rejected | `accepted_rejected` | string | — | yes | — | — |
| Rejection code | `rejection_code` | string | — | yes | — | — |
| Technology Type | `technology_type` | string | — | yes | — | MW |

- Entity key: `unique_bid_number`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`delivery_start`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

One row per **tender bid and result**, identified by `unique_bid_number` (the vendor describes it as
delivery date plus unit name). This is the **historic first-regime DC tender**: it is bid-level, with the
volume offered, the volume accepted, the availability fee and the rejection reason. It is not a unit lookup.
Resource `0b8dbc3c-e05e-44a4-b855-7dd1aa079c68` (uploaded CSV), one capture (2026-10-08, 1,687,187 bytes).
**Silver: 10,388 rows**; one Parquet file under
`C:/gridflow-data/silver/neso_data_portal/dynamic_containment_masterdata/year=2026/month=10/`, with the 18
vendor columns then the 8 gridflow columns (26 columns). **Status: eligible.**

- **Key.** `unique_bid_number` is unique and non-blank across all 10,388 rows.
- **Clocks.** Vintage is the CKAN `last_modified` of the captured file (ADR-030): `published_at` =
  `available_at` = **2026-05-29T12:35:35.769649Z** on every row (this is a file-upload stamp, **not** a
  tender or result publication time; `TODO: verify` what changed in the upload on that date, since the package
  states it is no longer updated). Event time is the recipe `utc_instant(delivery_start)`:
  `event_time` is the tz-aware UTC `delivery_start`, unshifted. Silver `event_time` runs from
  2020-10-01T22:00Z to 2021-09-14T22:00Z, and every `delivery_start` falls at 22:00Z or 23:00Z.
- **Delivery-date label.** `delivery_date` (`%d/%m/%Y`) is the service day label. In silver it equals the
  UK-local date of `delivery_start` **plus one day on all 10,388 rows** (the 24-hour service day starts at
  23:00 UK local time on the evening before the labelled date). That is an observed relationship, not a
  vendor statement; `TODO: verify` the vendor's definition of the labelled day.
- **Units (vendor dictionary).** `volume_offered` and `volume_accepted` **MW**; `delivery_start` /
  `delivery_end` UTC ISO 8601; `service_duration` hours (23, 24 and 25 hour days occur and all equal the
  elapsed UTC time between the endpoints: 10,347 rows at 24 h, 10 at 25 h, 31 at 23 h); `availability_fee`
  **£ as published** (not converted to a rate: it is not established whether it is per MW, per hour or a
  total); `total_cost` **£**.
- **Sentinels and strings.** `volume_accepted` is `0` on 1,199 rows (the dictionary: zero means rejected),
  kept as 0.0. `total_cost` is blank on 1,198 rows (null; the dictionary: blank means rejected). 1,104 rows
  have market name `Withdraw` (withdrawn entries), kept, not filtered; the other 9,284 are `DC LF`.
  `related_entity` holds the literal strings `N/A` (5,424 rows) and `NA` (7 rows) and blanks (1,507 rows):
  the literals are kept byte-equal and are not mapped to null. `agent_applicant` has 210 padded cells, kept
  as published. `rejection_code` is a `string` identifier (codes reach 5; `TODO: verify` DC-REJECTION-CODE-5,
  the dictionary enumerates fewer codes). `technology_type` is categorical despite its erroneous MW unit cell.
- `TODO: verify` **DC-MASTER-ENDPOINT-CLOSURE**: whether the `delivery_end` instant belongs to the service
  window. The start-instant recipe does not depend on it.

## Cadence

- Registry refresh: frozen
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Not Active

The vendor states the package is "Not Active" and no longer updated. gridflow has **one capture per
resource** (2026-10-08), so whether the 2023 tables will ever change, and the amendment and deletion behaviour
of the dumps, are unmeasured (`TODO: verify` by comparing later complete captures against the hash-pinned
bodies). The registry refresh is `frozen`, so nothing re-fetches on a schedule. The masterdata upload's CKAN
`last_modified` (2026-05-29) is later than the end of the data it holds (see the clocks section).

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence). Any gridflow
output derived from this package carries the attribution line "Supported by National Energy SO Open Data".

## Holds

- `dynamic_containment_dc_dr_dm_linear`: held: TODO: DC-LINEAR-PRICE-UNITS — the linear-orders dictionary declares the nP price points in conflicting units (1P–4P, 6P–10P, 15P–20P, 25P–30P £/MW; 5P MW with test-placeholder text; 11P–14P, 21P–24P, 31P–32P MW) while the auction guide calls every nP a price; what is the unit and hour basis of each nP column? (nV and ExecutedVolume are MW.) (unit v0.22-K-AS-4a)
- `dynamic_containment_dc_dr_dm_results_sum`: held: TODO: DC-SUMMARY-PRICE-UNIT — the DC/DR/DM results-summary dictionary describes Clearing Price as a price per MW per hour but gives its unit as £/MW (the by-unit results table states £/MW/h); which rate dimension does this export publish? (The delivery start/end cells are naive and their export clock is also undocumented.) (unit v0.22-K-AS-4a)

**Held means unpublished.** Hold class E-SEM: the vendor's unit or semantics for the output are unresolved.
Silver exists and reconciles, but no gold, chart, front-end page or model input may use these two families,
and this page deliberately states no values for them. Unit for both holds: v0.22-K-AS-4a.

**What would release the outputs.**

- *DC-SUMMARY-PRICE-UNIT* needs NESO to confirm the canonical rate dimension of the summary `Clearing Price`
  (per MW per hour, or per MW) and to correct the conflicting field documentation.
- *DC-LINEAR-PRICE-UNITS* needs a corrected linear-orders dictionary, or an explicit vendor export
  specification, that states the unit and hour basis of every `nP` column.

**Open questions that do not hold any output** (carried as `TODO: verify`):

- **DC-BLOCK-PRICE-HOUR-BASIS**: the hour basis of block `price` and `clearing_price` (published as £/MW).
- **DC-RESULT-EXPORT-CLOCK / DC-ORDER-EXPORT-CLOCK**: the clock of the naive delivery and order-entry strings.
- **DC-MASTER-ENDPOINT-CLOSURE**: whether the masterdata `delivery_end` instant belongs to the window.
- **DC-REJECTION-CODE-5**: rejection codes reach 5 while the dictionary enumerates only the lower codes.
- The original publication instant of every result (vintage is capture time, or the upload stamp for the
  masterdata, never a publication time), the amendment and deletion behaviour between captures, and order or
  result identity across any corrected re-export (`_latest` is `whole_capture`, never `key_latest`).

## Known issues and gotchas

- **Do not treat these as requirement forecasts, and do not join them to the forecast packages by date.** The
  forecast history shares 561 date labels with the legacy results (2022-04-21 to 2023-11-02); a shared label
  is not a shared meaning.
- **`timestamp_utc` is the capture time for the linear and block families**, not a delivery or bid time. A
  filter on it selects by fetch time.
- **The results and summary `event_time` is a date anchor, not the EFA block start.** The six EFA blocks of a
  day share one `event_time`; distinguish them by `efa`. Do not rebuild a block start from `efa_date` plus
  `efa`.
- **The masterdata `delivery_date` is one day after the UK-local date of `delivery_start`** on every row (the
  service day starts at 23:00 UK local time the evening before). Do not join it to the UTC date of
  `event_time`.
- **Block volumes are negative by design** (sell-order convention). `-1` values are signed quantities, not a
  missing-value marker. Do not take absolute values, null them or flip the sign.
- **Literal `NA` / `N/A` strings are values.** `technology_type` (results), `block_code_prm` (block) and
  `related_entity` (masterdata) hold them; they are not nulls. Blank string cells are null in those three columns but `''` in some others (see
  Typing and sentinels).
- **Blank-only columns.** `cancelled` (results) and `bid_validity` (block) are blank on every row; their
  silver columns hold the empty string `''` on every row (397,662 and 728,794 respectively), with no nulls.
  Results `location` mixes 9,030 nulls with 49,373 empty strings.
- **Withdrawn masterdata rows are kept** (`market_name` = `Withdraw`); they are not malformed service names.
- **`trade_id` equals `order_period_id`** on every row of the block and linear tables.
- **Dictionary quirks.** The saved field-info files carry the pound sign correctly (UTF-8) in the £/MW and
  £/MW/h unit cells; the only wrong unit cell is the masterdata `Technology Type`, which says MW for a
  categorical string. The block and results dictionaries still carry FFR-era text ("member of the trial",
  `DLH` / `LFS`) that does not match the six service codes seen in the data. `TODO: verify` against the live
  dictionary pages.
- **Memory.** The block body is 155 MB and 728,794 rows; transform it on its own (peak working set 1,399.0
  MiB at activation).

## Implementation delta

Where the code or a source differs from the docs or from another source:

- **Event time is the capture time** for the linear and block families by design (recipe `none`): the code
  does not interpret the vendor's naive time cells. The results and summary families use the date anchor
  (`date_sp1`) rather than a composed block start.
- **Linear curve column names.** Vendor `1P`..`32V` become `p1`..`v32` in silver (a silver name must begin
  with a letter); the vendor name is preserved in the "Vendor column" of the schema above.
- **Masterdata unit cell.** The dictionary says MW for `Technology Type`; silver types it as a string and the
  schema above repeats the dictionary's cell as published.
- **MAR.** The block dictionary calls `MAR` "automatically infilled, please leave blank"; the body carries
  fractional values (526 cells) and the NESO auction guide defines MAR as a minimum acceptance ratio. Silver
  keeps `float64` and the published values; no meaning is imposed beyond the guide.
- **`published_at`.** For the four datastore families it is null by design (the capture fallback), although
  the bronze sidecars hold a 2023 `ckan_last_modified` that is not used.
- **Package eligibility** is `eligible` in the registry while two families are held; the family records
  carry the holds (eligibility report `docs/neso_data_portal/eligibility.md`).
- **No ADR-040 ledger entry** exists for this package: every body loads. (The BSAD packages in the same batch
  do carry ledger entries.)

## Activation receipt

AS-4a merged as PR #116 (`c690258`), triple-green (RULINGS 759). Activation on 2026-10-13 with
`--start/--end 2026-10-08` and no prior silver (`phases/v0.22-K-AS-4a/post-merge/transform.log`): the five
families wrote **728,794 + 23,154 + 397,662 + 23,424 + 10,388 = 1,183,422** rows, each equal to the spec plan.
The block family was transformed alone. Reconcile `--all --cutoff 2026-10-12` exited 0 over 198 families with
0 gaps and 0 stale (RULINGS 760; `.planning/v0.22-RESULTS.md` section "AS-4a"). The package has 3 eligible
families and 2 held-with-silver.

## Links

- Current auction results (successor): @./eac-auction-results.md
- Requirement forecasts (a different measure): @./dynamic-containment-4-day-forecast.md, @./dynamic-regulation-requirements.md, @./dynamic-moderation-requirements.md, @./long-term-forecasts-for-dc-dm-dr-requirements.md
- Neighbouring auction results: @./static-firm-frequency-response-auction-results.md
- Vendor index: @../README.md, @../coverage.md
- GB balancing context: @../../../20-domain/markets/gb-balancing-mechanism.md
- Evidence in the gridflow repo: `.planning/phases/v0.22-K-AS-4/K-AS-4-FACTS.md` (section 6, g1-g6),
  `K-AS-4a-SPEC.md`, `.planning/RULINGS.md` (747, 748, 749, 759, 760), `.planning/v0.22-RESULTS.md` ("AS-4a")
