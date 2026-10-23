---
source: "neso_data_portal"
package: "interconnector-requirement-and-auction-summary-data"
dataset_key: "ic_requirement_auction"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-23
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  held: "NESO updates a lot in place with its auction result; the file keeps no earlier state."
  title: Interconnector requirement and auction summary
  summary: >-
    NESO's interconnector trading auctions: each lot it asked to buy or sell, and what cleared on
    which link at what price.
  facts:
    vendor: "NESO Data Portal, package Interconnector Requirement and Auction Summary Data: one table, one PDF"
    cadence: "Ad hoc, as NESO lists it; auctions run ad hoc across the day"
    grain: "Each row: one lot, a requirement later updated with its auction result"
  landscape: market
  what_it_is: >-
    NESO trades on IFA1, BritNed, NEMO, IFA2, ElecLink and Viking Link to adjust flows into or
    out of Great Britain, for constraints or margin. Qualified counterparties, who need a GTMA with
    NESO, bid in ad hoc auctions. Each lot is a requirement, not firm; when the auction ends NESO
    adds the volume cleared on each interconnector and the prices.
  how_used:
    - How much NESO asked to buy or sell across interconnectors, and when
    - "Clearing, best and average prices per lot, and volume cleared per interconnector"
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then the table's dump, kept if its body changed,
      and the PDF, a market notice, unless `last_modified` is unchanged.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=interconnector-requirement-and-auction-summary-data"
      - "GET https://api.neso.energy/datastore/dump/6a928369-bed3-445f-af8a-69cdb2cc5089"
      - "GET https://api.neso.energy/dataset/fdcb1853-4279-4fc9-acb2-d603965eab12/resource/74b56acb-e1ea-4c40-9f8a-2f4226630b2a/download/neso-trade-restriction-market-notice-14may26.pdf"
    commands:
      - {run: gridflow ingest neso_data_portal ic_requirement_auction --last 24h, comment: "the table's dump to bronze"}
      - {run: gridflow transform neso_data_portal ic_requirement_auction --last 24h, comment: "the capture's date to silver"}
      - {run: gridflow ingest neso_data_portal ic_requirement_auction_files --last 24h, comment: "the market notice, bronze only"}
  related:
    - {dataset: neso_data_portal/historic-gtma-grid-trade-master-agreement-trades-data, note: "NESO's GTMA trades; every bidder here must hold a GTMA"}
    - {dataset: elexon/soso, note: "Elexon's system operator to system operator interconnector trades"}
    - {dataset: elexon/fuelhh, note: "Elexon's half-hourly output by fuel type, each interconnector listed"}
---

# Interconnector Requirement and Auction Summary Data

This package is NESO's log of its **interconnector (IC) trading auctions**. NESO trades on the
IFA1, BritNed, NEMO, IFA2, ElecLink and Viking Link interconnectors to adjust the flow of
electricity into or out of Great Britain, either to manage system issues (thermal, voltage or
stability constraints) or to meet energy needs such as upward and downward margin. It invites
qualified counterparties into auctions that "run ad hoc across the day"; counterparties who hold, or
can later secure, interconnector capacity bid against a **requirement**. Each requirement is a
**lot**: a volume NESO wants to buy or sell, over a delivery window, on a stated set of qualified
interconnectors, with a bidding deadline. The vendor warns that requirements "are not firm and are
subject to change", and that once an auction concludes the lot "will be updated" to carry the
volumes secured on each interconnector, the best price, the volume-weighted average (VWA) price and
the clearing price; a requirement "may not be completely filled" (CKAN package `notes`,
@.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json). A counterparty needs a
Grid Trade Master Agreement (GTMA) with NESO, capacity on the channel interconnectors and BSC party
registration to take part. The related contract-enactment and GTMA trade tables from the same batch
are in @./balancing-services-contract-enactment.md.

Each row is therefore one lot **in its latest state**: the same row first describes a forward
requirement and is later overwritten with the auction outcome. The grain is one lot (`Auction Lot ID`,
which combines the auction identifier and a lot number); an auction (`Auction ID`) holds one or more
lots. For modelling it is a record of how much NESO cleared on each interconnector, at what price,
and when, but only once the availability question in Holds is settled.

gridflow has a silver output for it, but the output is **held**: the body mixes mutable forward
requirements with historical outcomes and carries no immutable issue time, so what was available
when is not established (see Holds). The package-level status in the front matter is generated from
the registry and reads `eligible`; the family-level eligibility is **held**. The silver exists on
disk, yet nothing in it may be published or used for point-in-time models yet. This page therefore
gives schema, row counts, clocks and missingness only, with **no data values**.

- Publisher group: Trading
- Registry group: trade-data · archetype: EVT

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Interconnector Requirements and Auction Summary | CSV | dump | `6a928369-bed3-445f-af8a-69cdb2cc5089` |

### DOC

| Resource | Format | Capture | Id |
|---|---|---|---|
| Interconnector trading restrictions for NESO | PDF | upload | `74b56acb-e1ea-4c40-9f8a-2f4226630b2a` |

Both resources were captured on 2026-10-08. The dump was captured again on 2026-10-16 (its body
had changed; the dump leg keeps a new capture only then, `client.py` `_dump_member`); bronze holds
one capture of the PDF. Sizes, hashes and `ckan_last_modified` come from the bronze sidecars under
`C:/gridflow-data/bronze/neso_data_portal/ic_requirement_auction/2026/10/{08,16}/` and
`C:/gridflow-data/bronze/neso_data_portal/ic_requirement_auction_files/2026/10/08/`.

| File | Disposition | Capture | Bytes | Data rows | CKAN `last_modified` | sha256 prefix |
|---|---|---|---:|---:|---|---|
| [Interconnector Requirements and Auction Summary (datastore dump)](https://api.neso.energy/datastore/dump/6a928369-bed3-445f-af8a-69cdb2cc5089) | SILVER | 2026-10-08 | 5,255,998 | 28,328 | 2023-01-23T22:44:59.745674 (datastore; see Two clocks) | `e87ac116` |
| same dump | SILVER | 2026-10-16 | 5,278,600 | 28,439 | 2023-01-23T22:44:59.745674 (unchanged) | `d1fc25d1` |
| [neso-trade-restriction-market-notice-14may26.pdf](https://api.neso.energy/dataset/fdcb1853-4279-4fc9-acb2-d603965eab12/resource/74b56acb-e1ea-4c40-9f8a-2f4226630b2a/download/neso-trade-restriction-market-notice-14may26.pdf) | DOC | 2026-10-08 | 112,483 | n/a | 2026-05-14T13:08:23.653612 | `1dd05c67` |

**What changed between the two dump captures (bronze, compared row by row on 2026-10-23; same
header).** 111 lots were added (delivery starts `2026-10-08T19:00:00` to `2026-10-16T16:00:00`) and
none removed. Exactly two existing rows changed: the two lots that started after the 2026-10-08
capture, `2026_10_08-11_43-1` and `2026_10_08-11_43-2`. On 2026-10-08 their outcome columns were
blank and `System Flag` read `null`; on 2026-10-16 the same rows carried `Clearing Price`,
`Best Price`, `VWA Price`, `Cleared Volume`, `Total Bid Volume` and per-interconnector volumes,
`System Flag` `F`, and `Published DateTime` moved from `2026-10-08T10:44:55` to
`2026-10-08T11:20:10`. This is a measured case of NESO's statement that a lot "will be updated" once
its auction concludes: the requirement row is overwritten in place, and the 2026-10-16 body keeps no
copy of its earlier state. The CKAN `last_modified` did not move.

Package page: [interconnector-requirement-and-auction-summary-data](https://www.neso.energy/data-portal/interconnector-requirement-and-auction-summary-data).
Resource dictionary: [interconnector_requirements_and_auction_summary](https://www.neso.energy/data-portal/interconnector-requirement-and-auction-summary-data/interconnector_requirements_and_auction_summary).

**The PDF is a market notice, not data.** The vendor describes it as a notice that a limit is to be
implemented on NESO's within-day trading in the opposite direction to the Day-Ahead schedule, from
20 May 2026. It is kept as **DOC**: gridflow catalogues it (family `ic_requirement_auction_files`,
metadata only) and extracts no tabular record from it. It is not needed to read the CSV schema, units
or clocks. `TODO: verify` whether the restriction changes how lots after 2026-05-20 should be read;
gridflow has not read the notice for that purpose.

**Bronze body (seat full-body scan, K-TRD facts).** One CSV, one header, no BOM issue, no wholly blank
row, no malformed row width, no blank identifier. Zero cells are padded, and none carry a literal
`N/A` or `NA`, a thousands separator, a currency or percentage symbol, or a non-finite numeric token.
Silver rows equal data rows.

## Families

### `ic_requirement_auction`

- Kind: tabular · archetype: EVT · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Published DateTime | `published_datetime` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | UTC ISO 8601 |
| Notes | `notes` | string | — | yes | — | — |
| Auction ID | `auction_id` | string | — | no | — | — |
| Auction Lot ID | `auction_lot_id` | string | — | no | — | — |
| Buy Sell | `buy_sell` | string | — | yes | — | — |
| Volume Required | `volume_required` | float64 | — | yes | — | MW |
| Qualified IC | `qualified_ic` | string | — | yes | — | — |
| Start Time | `start_time` | datetime | `%Y-%m-%dT%H:%M:%S` | no | UTC | UTC ISO 8601 |
| End Time | `end_time` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | UTC ISO 8601 |
| Bid Deadline | `bid_deadline` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | UTC ISO 8601 |
| Default Price | `default_price` | float64 | — | yes | — | £/MWh |
| Clearing Price | `clearing_price` | float64 | — | yes | — | £/MWh |
| Best Price | `best_price` | float64 | — | yes | — | £/MWh |
| VWA Price | `vwa_price` | float64 | — | yes | — | £/MWh |
| Cleared Volume | `cleared_volume` | float64 | — | yes | — | MW |
| Total Bid Volume | `total_bid_volume` | float64 | — | yes | — | MW |
| IFA1 Volume | `ifa1_volume` | float64 | — | yes | — | MW |
| BN Volume | `bn_volume` | float64 | — | yes | — | MW |
| NEMO Volume | `nemo_volume` | float64 | — | yes | — | MW |
| IFA2 Volume | `ifa2_volume` | float64 | — | yes | — | MW |
| EL Volume | `el_volume` | float64 | — | yes | — | MW |
| VKL Volume | `vkl_volume` | float64 | — | yes | — | MW |
| System Flag | `system_flag` | string | — | yes | — | — |

- Entity key: `auction_lot_id`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`start_time`)

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

**One header epoch.** The record accepts one exact 23-column header. Vendor names are kept as the
source; silver names are lower snake case. The silver table has 31 columns: the 23 vendor columns,
then `timestamp_utc`, `published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`,
`available_at`, `source_run_id` and `dataset_version`. All timestamps are tz-aware UTC.
`dataset_version` is `1+e1` (record version 1, generic engine version 1).

**What the columns mean (vendor dictionary).** From NESO's saved field info for the resource
(gridflow
`@.planning/research/neso-snapshots/field-info/20261008T114228Z/ic_requirement_auction.json`).

- **`Published DateTime`**: "The date and time when the data was last updated". It is an **update**
  instant, not a proved immutable issue time. gridflow keeps it as a typed column and never uses it as
  `available_at`.
- **`Notes`**: free-text notes and comments for a requirement.
- **`Auction ID`**: identifier of an auction, "typically based on the timestamp when initial
  requirement was sent"; the dictionary gives the format `YYYY_MM_DD-HH_MM`, with extra text possible
  "if there is some revision". Stored as a string, byte-equal to the body.
- **`Auction Lot ID`**: the combination of the Auction ID and the lot number, typically
  `YYYY_MM_DD-HH_MM-XX`. String, byte-equal to the body.
- **`Buy Sell`**: whether NESO intends to buy or sell for the lot.
- **`Qualified IC`**: the qualified interconnector or interconnectors for the lot; a combination uses
  `/` as separator. Kept as a single string, not split.
- **`Start Time` / `End Time`**: the delivery start and end of the requirement lot, documented UTC.
- **`Bid Deadline`**: the bidding deadline instant, documented UTC.
- **`Default Price`**: "The default price that applied if the counterparty failed to deliver".
- **`Clearing Price`**: described as "the clearing price (worst price)"; **`Best Price`**: the best
  price for the lot; **`VWA Price`**: the volume-weighted average price for the lot.
- **`Cleared Volume`**: total volume accepted for the requirement; **`Total Bid Volume`**: total bid
  volume for the requirement; **`IFA1` / `BN` / `NEMO` / `IFA2` / `EL` / `VKL Volume`**: the volume
  cleared on IFA1, BritNed, NEMO Link, IFA2, ElecLink and Viking Link respectively.
- **`System Flag`**: "Trade is for system or energy", with dictionary comment "T or F".
  `TODO: verify` which letter means which; the dictionary does not say and gridflow does not infer it.

**Units (vendor dictionary only, never inferred from a column name).** Every volume column
(`Volume Required`, `Cleared Volume`, `Total Bid Volume` and the six per-interconnector volumes) is
**MW**. Every price column (`Default Price`, `Clearing Price`, `Best Price`, `VWA Price`) is
**£/MWh**. The datetime columns' dictionary unit is "UTC ISO 8601", which is a zone and format, not a
physical unit. gridflow does no MW to MWh or price-dimension conversion. The bare CSV does not declare
these units or the zone: they exist only in NESO's external resource dictionary.

**Two clocks.**

1. **Vintage (`available_at`, capture-time fallback).** The registry sets vintage to
   `capture_fallback`, because the resource is a datastore dump and its `ckan_last_modified`
   (2023-01-23T22:44:59.745674 in the sidecar) is a frozen refresh stamp that says nothing about when
   today's body was available (ADR-035). `available_at` is therefore the **gridflow capture time**,
   the sidecar `written_at`: 2026-10-08T11:08:50.312375Z on all 28,328 rows of the first silver run
   (silver, 2026-10-12) and 2026-10-16T20:37:18.225890Z on the 28,439 rows of the 2026-10-16 run,
   equal to `capture_written_at`. `published_at` is **null** on all rows:
   gridflow does not backdate to the vendor's `Published DateTime`. An as-of query before the capture
   sees no rows.
2. **Event time (temporal recipe `utc_instant(start_time)`).** `event_time` and `timestamp_utc` equal
   `start_time`, the lot's delivery start, on every row (silver, 2026-10-12). Endpoint inclusivity of
   the start and end is not stated by the vendor; do not assume end-exclusive behaviour.

**Windows kept as published.** In the 2026-10-08 capture, one lot has an end before its start and two
lots have equal start and end. They are preserved, never repaired. No `run_type` applies: these are trading lots, not settlement
accounting runs, and none is fabricated (RULINGS 707).

**Identity and selection (ADR-039).**

- The entity key is `auction_lot_id`. The first silver run has **28,328 rows and 28,328 distinct lot
  ids** (2026-10-12), in **4,737 distinct auctions**, so an auction has one or more lots. The
  2026-10-16 capture has 28,439 rows, 28,439 distinct lot ids and 4,767 auctions (bronze).
- The vendor publishes no uniqueness guarantee; `TODO: verify` a vendor-guaranteed unique key and how
  an auction revision shows in `Auction ID`.
- `_latest` is `whole_capture`: the newest complete capture, not a per-key latest. Because the body
  already holds each lot in its latest state, older states of a lot are not recoverable from one
  capture; only an earlier gridflow capture keeps them (the two lots above).

**Sentinels and missing values (FACTS g5).**

- Signed **`-1`** occurs in `Clearing Price`, `Best Price` and `VWA Price`. No vendor source defines
  it as a missing-value marker, so it stays a value; it is **not** in any null token list.
- **Blank numeric cells** become null, never zero. Blank counts in the 2026-10-08 bronze body (the
  counts in this list are from that capture): `Clearing Price`,
  `Best Price` and `VWA Price` 232 each; `Cleared Volume` 1,740; `Total Bid Volume` 1,742. Whether a
  blank means a pending result, non-participation or missing history is `TODO: verify`. Blank counts
  for the other numeric columns were not measured here.
- **`Notes`** is blank in 27,689 rows; **`System Flag`** is blank in 26,776 rows and holds the literal
  token `null` in 30 further rows. That token is kept raw; its meaning is `TODO: IC-SYSTEM-FLAG-NULL`.
- `Published DateTime`, `End Time` and `Bid Deadline` have 0 nulls in silver; `Start Time` is
  non-nullable.
- Signed values and zeros stay values; nothing is trimmed, mapped or repaired.

**Activation (2026-10-12, master `374a7be`, PR #111).** The trading batch merged triple-green
(RULINGS 714). The family was transformed from the 2026-10-08 capture with
`--start/--end 2026-10-08`; there was no prior silver, so nothing was overwritten and no snapshot was
taken (RULINGS 715). Silver has **28,328 rows**, equal to the planned count, with 0 validation
failures and no blank-row exclusions. The batch-wide reconcile `--all --cutoff 2026-10-12` exited 0
with 0 gaps over 150 families (47 adjudicated, 0 stale; RULINGS 716). Gridflow
`@.planning/v0.22-RESULTS.md` section TRD holds the receipt.

A second silver run, from the 2026-10-16 capture, has 28,439 rows.

Silver layout: one Parquet file per capture (2026-10-08 and 2026-10-16) under
`C:/gridflow-data/silver/neso_data_portal/ic_requirement_auction/year=2026/month=10/`. The
`year=`/`month=` partition is the **capture** date, not the lot date. No gold view or builder reads
this family.

### `ic_requirement_auction_files`

- Kind: files · archetype: EVT · refresh: adhoc · empty allowed: no
- files: catalogue only

This family catalogues the market-notice PDF (resource `74b56acb-e1ea-4c40-9f8a-2f4226630b2a`,
disposition DOC). No tabular record is proposed and no silver is produced. Its vintage, were it ever
used, is the upload's `ckan_last_modified` (2026-05-14T13:08:23.653612).

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Ad hoc

The vendor says auctions run ad hoc across the day. The datastore resource's `ckan_last_modified` is
2023-01-23, long before the capture, while the package metadata was modified on 2026-10-06
(catalogue snapshot) and the resource metadata on 2026-10-08; the 2026-10-08 body held lots up to and
just after that capture. Between the 2026-10-08 and 2026-10-16 captures the body changed (111 lots
added, two overwritten with outcomes) while `ckan_last_modified` stayed at 2023-01-23, so that stamp
does not move when the body is refreshed. `TODO: verify` how often the body is refreshed: two
captures show that it changes, not how often.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `ic_requirement_auction`: held: TODO: IC-ISSUE-AVAILABILITY — lots are mutable forward requirements later overwritten with outcomes (28,326 targets on/before the capture, 2 after); what was available when? (unit v0.22-K-TRD)

The silver output exists on disk but is **held**. It may not be published or used for point-in-time
models until the question above is answered. The hold sits in the record, set when the trading batch
was specified (RULINGS 707) and merged under RULINGS 714. No resolving unit is named yet
(`TODO: name the unit that will settle IC-ISSUE-AVAILABILITY`).

**Why the usual shortcut fails.** Where every row in a forecast-style file targets a period after
the file's vintage, gridflow lets the vintage stand in for the issue time (RULINGS 529, forward-target
exemption). In the 2026-10-08 capture, 28,326 delivery starts are on or before the capture time and
only 2 are after it; in the 2026-10-16 capture none of the 28,439 is after it. So the body is a mix
of mutable forward requirements and completed historical outcomes, and the exemption does not apply.
The two forward lots of 2026-10-08 were overwritten with their outcomes by 2026-10-16 (see Files by
disposition), which shows the overwrite the question describes. `Published DateTime` is the only candidate vendor clock, but its description
("last updated") does not prove the captured historical values were available at that timestamp.

**What is not established.** When each lot first appeared, what it said then, and whether any earlier
state is retained anywhere. Nor is it shown what the `Published DateTime` of a lot refers to after
the outcome overwrites the requirement. gridflow will not infer an immutable issue history from the
column name or from the timestamp embedded in the auction identifier, will not backdate
`available_at`, and will not split the table into "requirement" and "outcome" views without evidence.

**What settles it:** edition-specific publication or retention evidence from NESO that shows what was
available at each time, or an explicit project decision establishing a separate **retrospective event
table** contract for this body (a record of outcomes as of the capture, not a point-in-time series).
Either is a record edit once ruled. Until then, row counts, schema and clocks are all this page
asserts. Unit and sentinel decisions above are independent of the hold and stand.
