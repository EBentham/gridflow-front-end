---
source: "neso_data_portal"
package: "balancing-services-contract-enactment"
dataset_keys: ["bs_contract_enactment_balancing", "bs_contract_enactment_balancing_service"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-23
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  held: true
  title: Balancing services contract enactment
  summary: >-
    NESO's log of balancing service contracts its trading team enacted, days to hours before
    delivery: when, how much and at what price.
  facts:
    vendor: "NESO Data Portal, package `balancing-services-contract-enactment`: six datastore tables, one ZIP"
    cadence: NESO says its current file refreshes every ten minutes; one table per financial year
    grain: "Each row: one contract enactment, with its delivery start and end"
    history: "Yearly tables 2021-22 to 2026-27, none for 2024-25; older files in a ZIP"
  landscape: market
  what_it_is: >-
    Days to hours ahead, NESO's trading team weighs trades against balancing service contracts and
    enacts a contract when it is the most cost-effective action, for example to manage constraints
    in Scotland or meet a reactive power need. NESO says an enactment usually involves no physical
    exchange of energy. The yearly tables add `Cost`, a system-security flag and a reason.
  how_used:
    - Which units and counterparties NESO enacted contracts with, when, and for what reason
    - "Average MW and £/MWh of each enactment, beside NESO's constraint costs"
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then each table's dump, kept if its body changed.
      The archive ZIP, listed under the older table, is its own key, `bs_contract_enactment_files`.
    commands:
      - {run: gridflow ingest neso_data_portal bs_contract_enactment_balancing --last 24h, comment: "yearly dumps; swap in either key"}
      - {run: gridflow transform neso_data_portal bs_contract_enactment_balancing --last 24h, comment: "the capture's date to silver"}
      - {run: gridflow ingest neso_data_portal bs_contract_enactment_files --last 24h, comment: "the ZIP's own key, bronze only"}
  family:
    slug: balancing-services-contract-enactment
    members:
      - dataset: bs_contract_enactment_balancing
        differs: "Five yearly tables from 2021-22, first and newest shown; times in UTC"
        request:
          - "GET https://api.neso.energy/api/3/action/package_show?id=balancing-services-contract-enactment"
          - "GET https://api.neso.energy/datastore/dump/84837a48-8f5d-40d8-bc9f-53dd5e519447"
          - "GET https://api.neso.energy/datastore/dump/183ecdfb-56e0-487d-8262-468ce1c78ed4"
        held: "`Cost` is labelled £/h, but NESO describes it as a total: volume times price times duration."
      - dataset: bs_contract_enactment_balancing_service
        differs: "Older table; its name, Pre June 2021, is not an end date"
        request:
          - "GET https://api.neso.energy/api/3/action/package_show?id=balancing-services-contract-enactment"
          - "GET https://api.neso.energy/datastore/dump/f75a1dcb-de6e-4c20-8407-e37d5e67cf79"
          - "GET https://api.neso.energy/dataset/1a03230c-94c6-4816-bb93-e4450f31aa17/resource/46ec41f3-1307-4faa-90e0-4b05a7710681/download/archived-balancing-services-contract-enactment.zip"
        held: Start times are dates only, and NESO gives no clock for the end and update times.
  related:
    - {dataset: neso_data_portal/index-linked-contract-volume, note: "Index-linked contract enactments for voltage, in the same columns"}
    - {dataset: neso_data_portal/super-stable-export-limit-contract-enactment, note: "Super SEL enactments, in the same columns from 2021-22"}
    - {dataset: neso_data_portal/historic-gtma-grid-trade-master-agreement-trades-data, note: "Trades by NESO's trading team, the other action it weighs"}
    - {dataset: neso_data_portal/constraint-breakdown, note: "NESO's daily constraint costs, one reason it enacts these contracts"}
---

# Balancing Services Contract Enactment

This package is NESO's log of **balancing-service contract enactments**. NESO procures balancing
service contracts to balance supply and demand and keep the transmission system secure. For the
contracts that fall within trading timescales (the vendor says "several days ahead to a couple of
hours ahead") the trading team compares all possible balancing actions, including trading and
balancing services, and takes the most cost-effective one. When a balancing service contract is
that best action, the contract is **enacted**, and the enactment is logged here. The vendor groups
enactments of contracts with a similar shape, or whose price is fixed at decision time, for
example constraint management in Scotland or reactive power. Its note adds that this usually
involves no physical exchange of power or energy, and that contracts not enacted by the trading
team are not included (CKAN package `notes`,
@.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json).

Each row is one **contract-enactment action**: a counterparty, an asset or unit, a delivery window
(start and end), an average volume, a price, and for the modern table a cost, a system-security
flag and a reason. It is **not** a settlement-period table, a contract master or a settlement
accounting run: no period column exists and no `run_type` applies (RULINGS 707). For modelling it
is a record of what NESO paid for, and when, in the forward trading window, alongside the
balancing-mechanism and constraint-cost series. It is not a forecast.

There are two families, from two vendor tables with different shapes:

- `bs_contract_enactment_balancing`: the **modern** table (ID-keyed, UTC delivery windows), one
  resource per financial year. 83 rows across five resources.
- `bs_contract_enactment_balancing_service`: the **legacy** "21-22 (Pre June 2021)" table
  (Record-keyed, date-only start times). 79 rows in one resource.

Both have a gridflow silver output, and **both are held**: the modern one on a cost-dimension
question, the legacy one on a clock question (see Holds). The package-level status in the front
matter is generated from the registry and reads `eligible`, but the family-level eligibility of
both is **held**. The silver exists on disk, yet nothing in it may be published or used for
point-in-time models yet. This page therefore gives schema, row counts, clocks and missingness
only, with **no data values**. A third family, `bs_contract_enactment_files`, is a catalogue-only
ZIP of archived files and is on HOLD.

- Publisher group: Trading
- Registry group: trade-data · archetype: EVT

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Balancing Contract Enactment FY 21-22 | CSV | dump | `84837a48-8f5d-40d8-bc9f-53dd5e519447` |
| Balancing Contract Enactment FY 22-23 | CSV | dump | `ed753a4b-1b8c-4b07-9997-b5c0e09da041` |
| Balancing Contract Enactment FY 23-24 | CSV | dump | `3ca7b6d5-d211-479f-8d5f-4bca92add3c9` |
| Balancing Contract Enactment FY 25-26 | CSV | dump | `b13cfa5e-53e3-41de-ace6-a5d3997b532c` |
| Balancing Contract Enactment FY 26-27 | CSV | dump | `183ecdfb-56e0-487d-8262-468ce1c78ed4` |
| Balancing Service Contract Enactment 21-22 (Pre June 2021) | CSV | dump | `f75a1dcb-de6e-4c20-8407-e37d5e67cf79` |

### HOLD

| Resource | Format | Capture | Id | Reason (unit) |
|---|---|---|---|---|
| Balancing Contract Enactment (Archived files) | ZIP | upload | `46ec41f3-1307-4faa-90e0-4b05a7710681` | data container: child inventory committed by X; records pending in TRD (TRD) |
| ↳ Archived Balancing Services Contract Enactment/balancing-1.csv | — | — | HOLD: proposed family bs_contract_enactment_archive: COVERED nomination by f75a1dcb-de6e-4c20-8407-e37d5e67cf79 — partial overlap only, 2 records differ (TRD) | — |
| ↳ Archived Balancing Services Contract Enactment/balancing-service-contract-enactment-20-21.csv | — | — | HOLD: proposed family bs_contract_enactment_archive: record pending in TRD (V-11) (TRD) | — |

The package has **no DOC resources**: seven resources, six CSV (SILVER) and one ZIP (HOLD).

**Download links and captures.** All six CSV resources are CKAN **datastore dumps**, so the capture
has no file name and `url_type` is `datastore`. The one ZIP is a CKAN upload with a file name. Each
resource has exactly one capture, taken 2026-10-08 by the NESO Data Portal connector. Size comes
from the capture sidecar under `C:/gridflow-data/bronze/neso_data_portal/<family>/2026/10/08/`;
rows are data rows of the body. "CKAN `last_modified`" is the sidecar value, blank where CKAN
publishes none.

| Resource | Family | Download | Bytes | Data rows | CKAN `last_modified` |
|---|---|---|---:|---:|---|
| FY 21-22 | `bs_contract_enactment_balancing` | [datastore dump](https://api.neso.energy/datastore/dump/84837a48-8f5d-40d8-bc9f-53dd5e519447) | 12,313 | 72 | 2022-06-02T08:03:03.868365 |
| FY 22-23 | `bs_contract_enactment_balancing` | [datastore dump](https://api.neso.energy/datastore/dump/ed753a4b-1b8c-4b07-9997-b5c0e09da041) | 598 | 3 | 2023-01-24T03:40:19.307106 |
| FY 23-24 | `bs_contract_enactment_balancing` | [datastore dump](https://api.neso.energy/datastore/dump/3ca7b6d5-d211-479f-8d5f-4bca92add3c9) | 914 | 5 | blank |
| FY 25-26 | `bs_contract_enactment_balancing` | [datastore dump](https://api.neso.energy/datastore/dump/b13cfa5e-53e3-41de-ace6-a5d3997b532c) | 218 | 1 | blank |
| FY 26-27 | `bs_contract_enactment_balancing` | [datastore dump](https://api.neso.energy/datastore/dump/183ecdfb-56e0-487d-8262-468ce1c78ed4) | 433 | 2 | blank |
| 21-22 (Pre June 2021) | `bs_contract_enactment_balancing_service` | [datastore dump](https://api.neso.energy/datastore/dump/f75a1dcb-de6e-4c20-8407-e37d5e67cf79) | 10,018 | 79 | 2023-01-07T19:43:18.676821 |
| Archived files | `bs_contract_enactment_files` | [archived-balancing-services-contract-enactment.zip](https://api.neso.energy/dataset/1a03230c-94c6-4816-bb93-e4450f31aa17/resource/46ec41f3-1307-4faa-90e0-4b05a7710681/download/archived-balancing-services-contract-enactment.zip) | 2,938 | 120 (in 2 members) | 2025-01-09T14:17:36.221173 |

Package page: [balancing-services-contract-enactment](https://www.neso.energy/data-portal/balancing-services-contract-enactment).
Legacy resource dictionary:
[balancing_service_contract_enactment_21-22_pre_june_2021](https://www.neso.energy/data-portal/balancing-services-contract-enactment/balancing_service_contract_enactment_21-22_pre_june_2021).

**Which years are covered.** There is **no FY 24-25 resource** in the 2026-10-06 catalogue snapshot
(the years run 21-22, 22-23, 23-24, 25-26, 26-27). `TODO: verify` where, if anywhere, FY 24-25
actions are published. The resource name is also not a reliable date boundary: the legacy
resource's start dates run into later years than its label suggests (FACTS sections 3.2 and
TRD-2). Use the row's own window, never the resource name, to place it in time.

**Bronze bodies (seat full-body scan, K-TRD-FACTS g3 and g5).** All six CSV bodies are strict UTF-8
with one header. The scans found no blank identifier, no malformed row width, no wholly blank row,
no padded cell, no thousands separator or currency symbol, no literal `N/A` or `NA` and no
non-finite number token in either family. SHA-256 digests are in the sidecars and in
@.planning/phases/v0.22-K-TRD/K-TRD-FACTS.md section 2.

## Families

### `bs_contract_enactment_balancing`

- Kind: tabular · archetype: EVT · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| ID | `id` | string | — | no | — | — |
| StartTime | `starttime` | datetime | `%Y-%m-%dT%H:%M:%S` | no | UTC | UTC ISO 8601 |
| EndTime | `endtime` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | UTC ISO 8601 |
| Volume | `volume` | float64 | — | yes | — | MW |
| Price | `price` | float64 | — | yes | — | £/MWh |
| Cost | `cost` | float64 | — | yes | — | £/h |
| SO_Flag | `so_flag` | string | — | yes | — | — |
| Reason | `reason` | string | — | yes | — | — |
| AssetID | `asset_id` | string | — | yes | — | — |
| CP_Name | `cp_name` | string | — | yes | — | — |
| Area | `area` | string | — | yes | — | — |
| Note | `note` | string | — | yes | — | — |
| Last_Updated | `last_updated` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | UTC ISO 8601 |

- Entity key: `resource_id`, `id`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: utc_instant (`starttime`)

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

**One header epoch.** The record accepts one exact header, the thirteen columns above, with `ID`
and `StartTime` required. The vendor column names are kept as the source; the silver names are
lower snake case.

**What the columns mean (vendor dictionary).** These descriptions come from NESO's saved field info
for the resource (gridflow
@.planning/research/neso-snapshots/field-info/20261008T114228Z/bs_contract_enactment_balancing.json).

- **`ID`**: "ID of the Contract Enactment Action". An identifier string, kept byte-equal to the
  body and never normalised.
- **`StartTime`** and **`EndTime`**: the start and end of the contract enactment action "in UTC
  format". Whether the end instant is inclusive or exclusive is **not** stated: `TODO: verify`
  before any duration-sensitive use. Do not assume end-exclusive behaviour.
- **`Volume`**: the "Average Volume of the contract enactment action". The vendor comment gives
  the sign convention: a positive number means the action increases generation, decreases demand
  or provides upwards margin; a negative number means it reduces generation, increases demand or
  provides downwards margin. The comment says it is rounded to up to one decimal place.
- **`Price`**: the "Average price of the contract enactment action", rounded to up to two decimal
  places.
- **`Cost`**: "Total cost to Nationalgrid ESO for the contract enctment action" (spelling as
  supplied), with the comment "Cost = Volume * Price * Duration". This is the subject of the hold
  (see Units).
- **`SO_Flag`**: "System flag indicating whether the action is mainly for system security
  purpose". The comment defines `T` as mainly system security and `F` as mainly balancing. It is
  stored as a string and not recoded to a boolean.
- **`Reason`**: "Detailed reason for the contract enactment action"; the comment lists examples
  such as voltage, thermal constraints, ROCOF, upwards margin and downwards reserve.
- **`AssetID`**: the asset identifier. The comment says that for a balancing-mechanism unit it is
  the NG BMU name, otherwise a name reflecting the contract with the counterparty. BM unit ids are
  stored as supplied.
- **`CP_Name`**: the contract counterparty, which the comment says may differ from the asset owner.
- **`Area`**: the delivery area of the asset (the comment names England and Wales, Scotland and
  interconnectors as example kinds). Free text, stored as supplied.
- **`Note`**: notes or comments.
- **`Last_Updated`**: "Date and Time that the information has been last updated", UTC. It is an
  **update** column. It is not proved to be the initial publication time or an immutable issue
  time, so it is never used as `published_at` or `available_at`.

**Units (vendor dictionary only).** `Volume`: **MW**. `Price`: **£/MWh**. `Cost`: **£/h**, exactly
as the dictionary labels it. The three time columns' dictionary unit is "UTC ISO 8601"; that is a
clock, not a physical unit. Identifiers, flags, reason, asset, counterparty, area and note carry no
unit. gridflow keeps every value as delivered: no MW-to-MWh conversion, no price-dimension
conversion, and no recomputation or relabelling of `Cost`. **The `Cost` unit is the hold
question:** the dictionary labels `Cost` £/h but its own comment and description describe it as a
total cost (Volume x Price x Duration), which is a sum in £ and not a rate. Which dimension is
published cannot be settled from the dictionary (see Holds). The conflict is a consumer-semantics
limit, not a casting failure: the column casts cleanly.

**Two clocks.**

1. **Vintage.** The resources are datastore dumps with no usable publication instant, so the
   registry vintage is **`capture_fallback`**: `available_at` is the capture's sidecar `written_at`
   (2026-10-08T09:01:07 to 09:03:07 UTC, one value per resource) and `published_at` is **null**.
   The CKAN `last_modified` is present on two resources (FY 21-22 and FY 22-23) and absent on the
   other three, so it cannot be a uniform vintage and gridflow does not use it. Because only one
   capture exists and it was taken on 2026-10-08, an as-of query before that sees **no** rows. That
   `available_at` is when gridflow fetched the file, not when NESO first published an action
   (ADR-035). `TODO: verify` vendor-publication availability: nothing here shows when a given
   action first appeared on the portal. The package note says the live file is "refreshed every
   ten minutes", so a row can also be revised in place.
2. **Event time.** The temporal recipe is `utc_instant` on `starttime`. `timestamp_utc` and
   `event_time` are both **`starttime`**, the UTC start of the delivery window, on every row
   (silver 2026-10-12, equal on all 83 rows). It is a delivery start instant, not a settlement
   date and not a publication time. The end instant is kept in `endtime` and is not part of the
   recipe.

**Identity and selection.**

- The vendor documents `ID` as the action identifier but does not guarantee permanent uniqueness.
  The record key is `(resource_id, id)`. All 83 rows are distinct on it, in the bodies and in
  silver, and no `ID` is shared between resources. `TODO: verify` a vendor-guaranteed key and
  whether a published action can be revised in place.
- `_latest` is `whole_capture` with `latest_partition: resource_id`: the newest complete capture of
  each resource, not a per-key latest. Each financial-year resource is selected on its own, so the
  five resources do not supersede one another. gridflow claims no vendor-certified revision key.

**Sentinels and missing values (FACTS g5).** No sentinel exists. The record declares no null
tokens, and `-1` is not treated as missing in any column. Zeros and signed values stay as
supplied, and the vendor does not mark any as missing (long runs of zeros occur, and the
package note says the contracts can be non-energy services, so a zero cannot be read as absent).
Blank numeric cells become null and never zero. In silver (2026-10-12) the only nulls are `reason`
(1 of 83), `area` (1) and `note` (10), plus `published_at` (all 83, by design: it is null for
this vintage). `endtime`, `last_updated` and the three value columns have no nulls.

**Row counts (silver, 2026-10-12).**

| Resource | Rows | Distinct on entity key |
|---|---:|---:|
| `84837a48-8f5d-40d8-bc9f-53dd5e519447` (FY 21-22) | 72 | 72 |
| `ed753a4b-1b8c-4b07-9997-b5c0e09da041` (FY 22-23) | 3 | 3 |
| `3ca7b6d5-d211-479f-8d5f-4bca92add3c9` (FY 23-24) | 5 | 5 |
| `b13cfa5e-53e3-41de-ace6-a5d3997b532c` (FY 25-26) | 1 | 1 |
| `183ecdfb-56e0-487d-8262-468ce1c78ed4` (FY 26-27) | 2 | 2 |
| Total | 83 | 83 |

Silver layout: one Parquet file per capture under
`C:/gridflow-data/silver/neso_data_portal/bs_contract_enactment_balancing/year=2026/month=10/`
(five files). The `year=`/`month=` partition is the **capture** date, not the delivery date.
Columns (22): the thirteen vendor columns, then `resource_id`, `timestamp_utc`, `published_at`,
`bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id` and
`dataset_version`. All timestamps are tz-aware UTC. `dataset_version` is `1+e1` (record version 1,
generic engine version 1). No gold view or builder reads this family.

### `bs_contract_enactment_balancing_service`

- Kind: tabular · archetype: EVT · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Record | `record` | string | — | no | — | — |
| Counterparty | `counterparty` | string | — | yes | — | — |
| Unit | `unit` | string | — | yes | — | — |
| Start Time | `start_time` | string | — | yes | — | — |
| End Time | `end_time` | string | — | yes | — | — |
| Volume | `volume` | float64 | — | yes | — | MW |
| Price | `price` | float64 | — | yes | — | £/MWh |
| Notes | `notes` | string | — | yes | — | — |
| Last Updated | `last_updated` | string | — | yes | — | — |

- Entity key: `record`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

**One header epoch.** The record accepts one exact header, the nine columns above (with spaces in
`Start Time`, `End Time` and `Last Updated`, unlike the modern table).

**What the columns mean (vendor dictionary).** From NESO's saved field info
(@.planning/research/neso-snapshots/field-info/20261008T114228Z/bs_contract_enactment_balancing_service.json).

- **`Record`**: "Identifier for the contract enactment action", in the format `YYYY_MM_DD-XX`
  where `XX` is the sequential number for the day. So it is a date plus a daily sequence number,
  a label and not an instant. Kept as a string.
- **`Counterparty`** and **`Unit`**: the counterparty the contract rights are held with, and the
  name of the unit or units (the vendor says some units have no equivalent BM unit name).
- **`Start Time`**: described as the "Start date time of a given contract enactment", yet the
  vendor's own datastore type for the column is **`date`**, and every captured cell is date-only.
  The time of day is lost. Kept as the raw string.
- **`End Time`** and **`Last Updated`**: described as the end date-time and the last-update
  date-time, both with vendor unit "N/A". The captured cells carry time of day, but **no clock or
  zone is declared**. Kept as raw strings.
- **`Volume`**: "Average volume of the contract"; the comment says a positive volume means more
  active power output to the grid and a negative volume means less.
- **`Price`**: "Price of the contract enactment action"; the comment says a negative price
  indicates NESO paying for the service.
- **`Notes`**: additional information, normally what the enactment is for.

**Units (vendor dictionary only).** `Volume`: **MW**. `Price`: **£/MWh**. The three time columns'
dictionary unit is "N/A": no unit and, importantly, **no clock**. gridflow does no conversion.

**Two clocks.**

1. **Vintage.** The resource is a datastore dump, so the vintage is **`capture_fallback`**:
   `available_at` is the sidecar `written_at` (2026-10-08T09:03:37.485867Z, one value for all 79
   rows) and `published_at` is **null**. The sidecar `ckan_last_modified` is
   2023-01-07T19:43:18.676821, but it is not used. As above, that is the fetch time, and
   `TODO: verify` vendor-publication availability.
2. **Event time (temporal recipe `none`).** There is **no event-time column**: the start time was
   truncated to a date and the end and update clocks are undocumented, so no delivery instant is
   derived. A date-only anchor was deliberately **not** built, because it would present a
   truncated date as an enactment start instant. `timestamp_utc` and `event_time` are therefore
   the **capture time** (`capture_written_at`, equal on all 79 rows), a storage convention and not
   a vendor measurement instant. Do not read either as the enactment's delivery time. Faithful
   delivery-window semantics are the hold.

**Identity and selection.**

- The measured grain is `record`: 79 non-blank, distinct values in the body and in silver. The
  vendor guarantees no key. `TODO: verify` permanent uniqueness and whether a row can be revised
  in place.
- `_latest` is `whole_capture` (the newest complete capture, no per-key latest, no partition).
- The `Start Time` dates span more than the resource's "21-22 (Pre June 2021)" label suggests
  (K-TRD-FACTS section 3.2), so the label is not a boundary.
- One row's end date precedes its start date. It is preserved as supplied and not repaired, and
  `TODO: verify` with NESO whether it is a typing error.

**Sentinels and missing values (FACTS g5).** No sentinel exists and no null tokens are declared.
Zeros and signed values stay as supplied, with no vendor marking of missing. Silver (2026-10-12)
has no nulls in any vendor column; `published_at` is null on all 79 rows by design.

**Row counts (silver, 2026-10-12).**

| Resource | Rows | Distinct on entity key |
|---|---:|---:|
| `f75a1dcb-de6e-4c20-8407-e37d5e67cf79` | 79 | 79 |

Silver layout: one Parquet file under
`C:/gridflow-data/silver/neso_data_portal/bs_contract_enactment_balancing_service/year=2026/month=10/`
(partition = **capture** date). Columns (17): the nine vendor columns (all three time columns as
strings), then `timestamp_utc`, `published_at`, `bronze_capture_id`, `capture_written_at`,
`event_time`, `available_at`, `source_run_id` and `dataset_version`. There is no `resource_id`
column, because the entity key does not include it. All metadata timestamps are tz-aware UTC;
`dataset_version` is `1+e1`. No gold view or builder reads this family.

**Path-length warning.** The final silver path under `C:\gridflow-data` is **225 characters**
(measured 2026-10-12 on the actual file,
`...\bs_contract_enactment_balancing_service\year=2026\month=10\bs_contract_enactment_balancing_service_20261008_run<timestamp>_<32 hex>.parquet`).
The binding length is the writer's temporary sibling, `{name}.tmp_<16 hex>`
(`storage/parquet.py`), which is used for the atomic `os.replace`: it is **246 characters**, or
**247 counting the NUL terminator**, which leaves **13** under the Windows `MAX_PATH` of 260. The
247 in RULINGS 716 and the activation receipt is this temp path, not the silver file name. A longer
data root fails the `.tmp` to `.parquet` replace (seen under a long scratch root, RULINGS 711;
close note, RULINGS 716).

### `bs_contract_enactment_files`

- Kind: files · archetype: EVT · refresh: daily · empty allowed: no
- files: catalogue only

This family holds the single ZIP of **archived** enactment files (2,938 bytes, CKAN upload,
`last_modified` 2025-01-09T14:17:36.221173). Its two clocks: the **vintage** is the upload's
`ckan_last_modified` (`available_at` is that CKAN `last_modified` of the capture); there is **no
event time** (catalogue only: no silver output, so no `timestamp_utc` or temporal recipe applies).
The captured bytes are kept in bronze and catalogued only.

It contains two CSV members, both with the same nine-column header as the legacy table:

| Member | Data rows | Overlap with the legacy table | Disposition |
|---|---:|---|---|
| `Archived Balancing Services Contract Enactment/balancing-1.csv` | 6 | 2 records in common, and **both differ** | HOLD |
| `Archived Balancing Services Contract Enactment/balancing-service-contract-enactment-20-21.csv` | 114 | none | HOLD |

Neither member is **COVERED** by the current CSV. A shared identifier or a partial overlap is not
enough: ADR-037 needs equal cleanly typed projections for every exempted capture plus a committed
proof test, and the equivalence harness was not run or granted for this package. The two shared
records differ in start time, end time and last-updated clocks: the archive keeps time of day
where the current table has only a date, some archive cells carry a trailing `Z` where others
do not, and the end and update values differ from the current ones. These are lost time of day,
changed end points and changed update stamps, not whole-member equivalence.
`TODO: ARCHIVE-BS-CLOCK/AMENDMENT:` obtain a vendor explanation of the naive versus `Z` timestamps
and of the changed rows. Until it is documented, naive timestamps stay raw and no offset is
subtracted. The proposed archive family `bs_contract_enactment_archive` has no record.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Status: Live

The registry polls daily. The vendor package note says the "Live data file is refreshed every ten
minutes", and the status is "Live", but the six datastore resources carry a CKAN `last_modified`
only on two of them and the three newest resources have none, so the portal gives no per-resource
update time to key a schedule on. `TODO: verify` how often new actions are appended, whether a
new financial year is a new resource each April (the FY 24-25 gap above suggests it may not be),
and whether NESO revises logged actions. Only more captures, compared pair by pair, can show this.
One capture exists per resource to date (2026-10-08).

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `bs_contract_enactment_balancing`: held: TODO: COST-DIMENSION — the dictionary labels `Cost` £/h but describes it as total cost (price × volume × duration); which is published? (unit v0.22-K-TRD)
- `bs_contract_enactment_balancing_service`: held: TODO: LEGACY-BS-CLOCK — start times truncated to dates, end/update clocks undocumented; what instants were published? (unit v0.22-K-TRD)

Both silver outputs exist on disk but are **held**. They may not be published or used for
point-in-time models until the questions are answered. The hold sits in the record. The seat
specified and approved the batch (RULINGS 707), and PR #111 merged triple-green at master
`374a7be` (RULINGS 714). Activation and the reconcile followed (RULINGS 715 and 716, below). The
records' own unit tag is v0.22-K-TRD; no resolving unit is named yet
(`TODO: name the unit that will settle COST-DIMENSION and LEGACY-BS-CLOCK`).

**COST-DIMENSION (modern family).**

- *The question.* `Cost` is labelled £/h, but the vendor describes it as total cost and gives
  Volume x Price x Duration as the formula. Volume is MW and price is £/MWh, so that product
  times a duration is £, not £/h. Which quantity is in the column (a rate in £/h, or a total
  in £) is not established.
- *The unit as published.* The vendor unit, £/h, is kept as written. gridflow does not relabel it
  as £ and does not recompute it from volume, price and duration, because any such inference
  would be a guess at vendor semantics.
- *What is established.* The column casts cleanly, has no nulls in silver, and `Volume` (MW) and
  `Price` (£/MWh) carry no such conflict. The hold is on consuming `Cost`; it covers the whole
  family output because the record is the publishing unit.
- *What settles it.* A corrected or clarified NESO data dictionary for `Cost`. The same
  question is held on three sibling families (GTMA financial-year trades, index-linked contract
  volume and the modern super stable export limit enactment table).

**LEGACY-BS-CLOCK (legacy family).**

- *The question.* `Start Time` is described as a date-time, but its datastore type is `date` and
  every captured cell is date-only, so the actual start instant was lost upstream. The end and
  update columns carry time of day, but the vendor declares no clock for them (the dictionary
  unit is "N/A"). What instants were published, and in what zone?
- *Why nothing is derived.* Without the start instant there is no event time; the table is
  therefore stored with temporal recipe `none` and all three time columns as raw strings. A
  date-only storage anchor was rejected because it would label a truncated date as an enactment
  start.
- *Corroborating evidence.* The archive ZIP (above) holds two records that overlap this table and
  differ in exactly these clocks, which suggests that a time of day existed for at least those
  actions and was later truncated or changed (`TODO: verify`). Equivalence between the archive and this table is
  not proved.
- *What settles it.* A NESO statement of the clock for the end and update columns and an
  explanation, or a corrected export, of the truncated start times.

**Why the usual shortcuts fail.** Both tables log actions that began before the capture, so the
forward-target exception that lets a vintage stand in for an issue time (RULINGS 529) does not
apply, and no update column is promoted to a publication time. These are agreed historical
actions and not forecasts of them, so a pre-vintage delivery target is not by itself a
forecast-eligibility failure; the open point is when each row was available, which a single
capture cannot show.

**Activation (2026-10-12, master `374a7be`, PR #111).** The trading batch (nine records in six
package registries) merged triple-green (RULINGS 714). Both families were transformed from the
2026-10-08 captures with `--start/--end 2026-10-08`. There was no prior silver, so nothing was
overwritten and no snapshot was taken (RULINGS 715). Silver has **83** rows (modern) and **79**
rows (legacy), each equal to the planned count, with 0 validation failures and no blank rows
excluded; the batch total across nine families is 324,996. The batch-wide reconcile
`--all --cutoff 2026-10-12` exited 0 with 0 gaps over 150 families (47 adjudicated, 0 stale;
RULINGS 716). Gridflow `@.planning/v0.22-RESULTS.md` section TRD holds the receipt. The family
hold set for the whole batch is: COST-DIMENSION, LEGACY-BS-CLOCK, IC-ISSUE-AVAILABILITY,
UPCOMING-VOLUME-FORMULA and GTMA-2020-DUPLICATES (one GTMA resource only).

**Related packages.** The sibling enactment tables share the cost question or the same table shape:
@./super-stable-export-limit-contract-enactment.md and @./index-linked-contract-volume.md.
Historic trades are in @./historic-gtma-grid-trade-master-agreement-trades-data.md.
