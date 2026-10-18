---
source: "neso_data_portal"
package: "phase-2-ffr-auction-results-summary"
dataset_keys: ["ffr_phase2_auction_phase_block_order", "ffr_phase2_auction_phase_blockorders", "ffr_phase2_auction_phase_linear_orders", "ffr_phase2_auction_phase_linearorders", "ffr_phase2_auction_phase_results_sum", "ffr_phase2_auction_phase_results_unit", "ffr_phase2_auction_phase_resultsbyunit", "ffr_phase2_auction_phase_resultsum", "ffr_phase2_blockorders_archive", "ffr_phase2_linearorders_archive", "ffr_phase2_result_summary_archive", "ffr_phase2_results_by_unit_archive"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-14
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Phase 2: FFR Auction Results Summary

> **Frozen trial history. Held outputs: two of the six current silver tables, plus all four archive tables.**
> This package is NESO's published record of the Phase 2 Firm Frequency Response (FFR) auction trial. It holds
> auction **orders and results**, not requirement forecasts. Two silver tables (the master block orders and
> the results summary) and the four historic archive tables (result summary, block orders, linear orders,
> results by unit) are **held**: silver is written but nothing is released to consumers, and this page states
> their schema, row counts, clocks and hold questions only, **no data values**. All four ZIP archives now have
> silver (the result summary from unit X, the other three from unit AS-5c); one archive member, the 2019-11-22 results-by-unit file, is held back from silver and
> read by no record.

This package is NESO's published history of the **Phase 2 FFR auction trial**: weekly auctions in which
providers bid to supply frequency response in four-hour Electricity Forward Agreement (EFA) blocks, for the
two trial products the vendor's dictionaries name **DLH (Dynamic Low High)** and **LFS (Low Frequency
Static)**. It is the order book and the outcome of each auction, in four tables that each exist twice, as
a **weekly export** (one auction week, files published 2021-11-26) and as **master data exports** (the accumulated
history, three trial years):

1. **Block orders**: one row per order period (a bid for a flat block of MW), with executed and offered
   volume, the bid price, the market clearing price and an execution status.
2. **Linear orders**: the market buy curve for each delivery period, as up to four price/volume points.
3. **Results by unit**: the cleared volume and clearing price awarded to each unit for each service and EFA
   block.
4. **Results summary**: the cleared volume and clearing price per service and EFA block.

The vendor describes the EFA numbering as "the week is split into 42 blocks, with 6 four-hour blocks each
day" (the field dictionary, quoted in the schema notes below). **EFA in this package is that weekly ordinal
(1 to 42), not a settlement period and not a clock time.** The Phase 2 trial itself is described in NESO's
[trial evaluation](https://www.neso.energy/document/176721/download); this page cites it only for the points
named in the open questions below.

Use the by-unit results to see who was awarded what, in which service and block (calendar dates 2019-12-07
to 2021-11-30 in the `efa_date` column), and the order tables to see how bids were structured. All of it is
history: the package is "Not Active" and frozen, and newer procurement is published through other packages
(see Links).

**Weekly and master exports overlap. Never add them.** The weekly export and the master data export of a
table are the **same table** in two vintages (same header, same business columns), so the weekly rows are a
subset of the masters for the result tables, and the two order exports overlap with differences in spelling
and identifier fidelity. gridflow keeps the **order** tables as separate tables per export (never union or
sum them) and deduplicates the **result** tables to one row per business key, keeping the master row.
Details in "Weekly and master exports" below.

**Held outputs.** Held (hold class E-SEM, a vendor identity or unit question, unit `v0.22-K-AS-5a`):

- `ffr_phase2_auction_phase_blockorders` (master block orders): PHASE2-MASTER-ORDER-ID.
- `ffr_phase2_auction_phase_resultsum` (results summary): PHASE2-SUMMARY-PRICE-UNIT.
- `ffr_phase2_result_summary_archive` (historic summary archive, unit AS-5): date and EFA semantics
  undocumented.
- `ffr_phase2_blockorders_archive` (1,042 rows), `ffr_phase2_linearorders_archive` (588 rows) and
  `ffr_phase2_results_by_unit_archive` (436 rows), unit `v0.22-K-AS-5c`: PHASE2-ARCHIVE-SEMANTICS (the
  archive members have no data dictionary; see Holds).
- The 2019-11-22 results-by-unit archive member (521 rows in bronze, none in silver), unit `v0.22-K-AS-5c`:
  PHASE2-ARCHIVE-BYUNIT-COLLISION.

For these held outputs this page gives no sample row, no minimum, maximum or other value statistic. The other
four current silver tables (weekly block orders, weekly linear orders, master linear orders and the by-unit
results) are eligible. Attribution for any output derived from this package: **Supported by National
Energy SO Open Data**.

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: EVT
- Package id: `2d649d03-fb37-46a2-ae82-9e651438b559`
- Package page: [NESO Data Portal, Phase 2: FFR Auction Results Summary](https://www.neso.energy/data-portal/phase-2-ffr-auction-results-summary)
- Background (context only, for the local-clock handling and the balancing services these auctions sit in):
  @../../../20-domain/concepts/settlement-period.md, @../../../20-domain/markets/gb-balancing-mechanism.md


## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Phase 2 FFR Auction BlockOrders Masterdata 2019-2020 | CSV | upload | `979329c3-5587-4b08-a900-5520b58b2d8f` |
| Phase 2 FFR Auction BlockOrders Masterdata 2020-2021 | CSV | upload | `c074d827-ad03-4b11-b22e-8bbc96be3bab` |
| Phase 2 FFR Auction BlockOrders Masterdata 2021-2022 | CSV | upload | `89467af0-a577-4bba-9955-f8c380a78923` |
| Phase 2 FFR Auction LinearOrders Masterdata 2020-2021 | CSV | upload | `404a1de1-5fe9-4569-815a-394e83af96eb` |
| Phase 2 FFR Auction LinearOrders Masterdata 2021-2022 | CSV | upload | `eb394ce7-20c6-4434-a263-470b2896fd7b` |
| Phase 2 FFR Auction LinearOrders Masterdata-2019-2020 | CSV | upload | `47ceb316-e284-4e14-bb67-76067a8f9562` |
| Phase 2 FFR Auction ResultSummary Masterdata 2020-2021 | CSV | upload | `279572a9-21c9-4e1e-a7c8-7aed233f8936` |
| Phase 2 FFR Auction ResultSummary Masterdata 2021-2022 | CSV | upload | `920105e5-a5e3-4bed-83ce-ab6901cc1b84` |
| Phase 2 FFR Auction ResultSummary Masterdata-2019-2020 | CSV | upload | `8b5fa222-f39f-4eea-9475-728ea8365ff3` |
| Phase 2 FFR Auction ResultsByUnit Masterdata 2020-2021 | CSV | upload | `52faffc9-e804-44d8-b222-dd0821d79e7d` |
| Phase 2 FFR Auction ResultsByUnit Masterdata 2021-2022 | CSV | upload | `feafb7ab-7db6-406e-a46f-bbcf6ed92ba1` |
| Phase 2 FFR Auction ResultsByUnit Masterdata-2019-2020 | CSV | upload | `15d7fa42-1c8d-4a79-86f8-890cf9228794` |
| Phase 2: FFR Auction Block Order 26.11.2021 | CSV | upload | `edfb5b8f-4415-45e6-b378-57020c41e96b` |
| Phase 2: FFR Auction Linear Orders 26.11.2021 | CSV | upload | `5cce4cb6-c270-488f-96c7-9f5cd7476898` |
| Phase 2: FFR Auction Results Summary 26.11.2021 | CSV | upload | `a9659701-f0d4-40d2-91f1-31f4bac0619d` |
| Phase 2: FFR Auction Results by Unit 26.11.2021 | CSV | upload | `87ee8fc4-11ae-4575-b734-99548aab2d98` |
| ResultSummary 2019-11-22 to 2019-11-29 | ZIP | upload | `3928f192-97a5-4b4f-9234-0dcc9ad071a0` | SILVER `ffr_phase2_result_summary_archive` |
| ↳ ResultSummary 2019-11-22 to 2019-11-29/NGESO_FRA_2019-11-22_ResultSummary.csv | — | — | SILVER `ffr_phase2_result_summary_archive` |
| ↳ ResultSummary 2019-11-22 to 2019-11-29/NGESO_FRA_2019-11-29_ResultSummary.csv | — | — | SILVER `ffr_phase2_result_summary_archive` |
| BlockOrders 2019-11-22 to 2019-11-29 | ZIP | upload | `e988552e-8bc1-43db-af15-cff01e40d83c` | SILVER `ffr_phase2_blockorders_archive` |
| ↳ BlockOrders 2019-11-22 to 2019-11-29/NGESO_FRA_2019-11-22_BlockOrders.csv | — | — | SILVER `ffr_phase2_blockorders_archive` |
| ↳ BlockOrders 2019-11-22 to 2019-11-29/NGESO_FRA_2019-11-29_BlockOrders.csv | — | — | SILVER `ffr_phase2_blockorders_archive` |
| LinearOrders 2019-11-22 to 2020-01-03 | ZIP | upload | `7ab29f1c-4da1-4f36-b611-cb74f62737fc` | SILVER `ffr_phase2_linearorders_archive` |
| ↳ LinearOrders 2019-11-22 to 2020-01-03/NGESO_FRA_2019-11-22_LinearOrders.csv | — | — | SILVER `ffr_phase2_linearorders_archive` |
| ↳ LinearOrders 2019-11-22 to 2020-01-03/NGESO_FRA_2019-11-29_LinearOrders.csv | — | — | SILVER `ffr_phase2_linearorders_archive` |
| ↳ LinearOrders 2019-11-22 to 2020-01-03/NGESO_FRA_2019-12-06_LinearOrders.csv | — | — | SILVER `ffr_phase2_linearorders_archive` |
| ↳ LinearOrders 2019-11-22 to 2020-01-03/NGESO_FRA_2019-12-13_LinearOrders.csv | — | — | SILVER `ffr_phase2_linearorders_archive` |
| ↳ LinearOrders 2019-11-22 to 2020-01-03/NGESO_FRA_2019-12-20_LinearOrders.csv | — | — | SILVER `ffr_phase2_linearorders_archive` |
| ↳ LinearOrders 2019-11-22 to 2020-01-03/NGESO_FRA_2019-12-27_LinearOrders.csv | — | — | SILVER `ffr_phase2_linearorders_archive` |
| ↳ LinearOrders 2019-11-22 to 2020-01-03/NGESO_FRA_2020-01-03_LinearOrders.csv | — | — | SILVER `ffr_phase2_linearorders_archive` |
| ResultByUnit 2019-11-22 to 2019-11-29 | ZIP | upload | `a99410bb-5501-4292-a308-eb7c16b1b3f4` | SILVER `ffr_phase2_results_by_unit_archive` |
| ↳ ResultByUnit 2019-11-22 to 2019-11-29/NGESO_FRA_2019-11-29_ResultsByUnit.csv | — | — | SILVER `ffr_phase2_results_by_unit_archive` |

(All four ZIP archives and their SILVER members are **held outputs**: silver is written, nothing is released;
see Holds. The `ResultByUnit` container is SILVER, but one of its two members is HOLD, below.)

### HOLD

| Resource | Format | Capture | Id | Reason (unit) |
|---|---|---|---|---|
| ↳ ResultByUnit 2019-11-22 to 2019-11-29/NGESO_FRA_2019-11-22_ResultsByUnit.csv | — | — | child of `a99410bb-5501-4292-a308-eb7c16b1b3f4` | HOLD: PHASE2-ARCHIVE-BYUNIT-COLLISION (v0.22-K-AS-5c) |

The 2019-11-22 by-unit member is **held and read by no record**; its 521 rows stay in immutable bronze and
produce no silver. The hold question (the registry reason, with the member's data values left out here
because the family is a held output): the member has two rows for one unit, one date, one EFA block and one
service, sharing a clearing price but with different cleared volumes; which row is the result, or are both
legitimate? The collision is **never resolved by selecting a row** and the rows are not deduplicated. The
2019-11-29 member (436 rows) loads. If a later reader read both members, the capture would fail whole on a
duplicate entity key rather than choose.

**There are no DOC resources in this package**, so there are no document download links. All 16 CSV resources
and all four ZIP archives are disposition SILVER (the `ResultByUnit` ZIP carries one HOLD child, above); of the
13 ZIP members, 12 are SILVER and 1 is HOLD. Every resource has exactly one capture (2026-10-08), so
amendments and deletions between captures are unmeasured. No resource or child keeps the earlier "data
container, records pending" reason.

**Dispositions, in plain terms.**

| Disposition | Resources | What happens |
|---|---|---|
| SILVER, own family | 3 master block-order CSVs, 3 master linear-order CSVs, 1 weekly block-order CSV, 1 weekly linear-order CSV | Parsed to the family of the same name |
| SILVER, to a master family | The weekly CSV and the three master CSVs of each of the two result tables (by unit, summary): 8 resources | The weekly resource is a **sibling** (it has its own bronze capture family, `results_unit` or `results_sum`, with no silver of its own) and its rows land in the master family's silver (`resultsbyunit`, `resultsum`) |
| SILVER, ZIP members (held output) | `ResultSummary 2019-11-22 to 2019-11-29` (2 CSV members) | Parsed to `ffr_phase2_result_summary_archive` (held, 168 rows) |
| SILVER, ZIP members (held output) | `BlockOrders 2019-11-22 to 2019-11-29` (2 members) | Parsed to `ffr_phase2_blockorders_archive` (held, 1,042 rows) |
| SILVER, ZIP members (held output) | `LinearOrders 2019-11-22 to 2020-01-03` (7 members) | Parsed to `ffr_phase2_linearorders_archive` (held, 588 rows) |
| SILVER, ZIP member (held output) | `ResultByUnit 2019-11-22 to 2019-11-29`, member 2019-11-29 | Parsed to `ffr_phase2_results_by_unit_archive` (held, 436 rows) |
| HOLD (single member) | `ResultByUnit 2019-11-22 to 2019-11-29`, member 2019-11-22 | Read by no record; 521 rows stay in bronze (PHASE2-ARCHIVE-BYUNIT-COLLISION) |

The archives add the earlier auctions (2019-11-22 to 2020-01-03) that are not in the masters. Their data
values are not published on this page: all four archive tables are held outputs. Each archive member is read
by exactly one record; no archive record reads a masterdata CSV, and the summary archive record, container
and children were left unchanged by AS-5c (its 168 rows are identical to before).

**Where each resource is fetched from.** Sidecar `request_url` (the pattern is
`https://api.neso.energy/dataset/2d649d03-fb37-46a2-ae82-9e651438b559/resource/<resource id>/download/<file name>`),
bronze under `C:/gridflow-data/bronze/neso_data_portal/<family>/2026/10/08/`, file name
`raw_<stamp>_<resource-id>_<first-8-of-sha256>.csv` (or `.zip`), immutable. The CKAN `last_modified` is the
**vintage** (see the clocks section).

| Family (bronze) | File name | CKAN `last_modified` (UTC) | Bytes |
|---|---|---|---:|
| `ffr_phase2_auction_phase_block_order` | `ngeso_fra-weekly_2021-11-26_blockorders.csv` | 2021-11-26T11:15:54.702162 | 80,174 |
| `ffr_phase2_auction_phase_blockorders` | `phase-2-ffr-auction-blockorders-masterdata-2019-2020.csv` | 2021-03-31T09:28:52.708950 | 2,082,226 |
| `ffr_phase2_auction_phase_blockorders` | `phase-2-ffr-auction-blockorders-masterdata-2020-2021.csv` | 2022-03-18T12:08:37.494234 | 8,874,187 |
| `ffr_phase2_auction_phase_blockorders` | `phase-2-ffr-auction-blockorders-masterdata-2021-2022.csv` | 2021-11-26T11:18:31.140573 | 4,089,601 |
| `ffr_phase2_auction_phase_linear_orders` | `ngeso_fra-weekly_2021-11-26_linearorders.csv` | 2021-11-26T11:16:28.900983 | 16,283 |
| `ffr_phase2_auction_phase_linearorders` | `phase-2-ffr-auction-linearorders-masterdata-2019-2020.csv` | 2021-03-31T09:29:46.319416 | 197,017 |
| `ffr_phase2_auction_phase_linearorders` | `phase-2-ffr-auction-linearorders-masterdata-2020-2021.csv` | 2022-03-18T12:09:08.574821 | 707,061 |
| `ffr_phase2_auction_phase_linearorders` | `phase-2-ffr-auction-linearorders-masterdata-2021-2022.csv` | 2021-11-26T11:19:09.079965 | 483,242 |
| `ffr_phase2_auction_phase_results_unit` | `ngeso_fra-weekly_2021-11-26_resultsbyunit.csv` | 2021-11-26T11:17:15.657545 | 19,729 |
| `ffr_phase2_auction_phase_resultsbyunit` | `phase-2-ffr-auction-resultsbyunit-masterdata-2019-2020.csv` | 2021-03-31T09:30:53.612085 | 899,469 |
| `ffr_phase2_auction_phase_resultsbyunit` | `phase-2-ffr-auction-resultsbyunit-masterdata-2020-2021.csv` | 2021-04-01T10:32:40.269524 | 3,578,657 |
| `ffr_phase2_auction_phase_resultsbyunit` | `phase-2-ffr-auction-resultsbyunit-masterdata-2021-2022.csv` | 2021-11-26T11:20:28.830268 | 1,733,445 |
| `ffr_phase2_auction_phase_results_sum` | `ngeso_fra-weekly_2021-11-26_resultsummary.csv` | 2021-11-26T11:17:51.159026 | 5,522 |
| `ffr_phase2_auction_phase_resultsum` | `phase-2-ffr-auction-resultsummary-masterdata-2019-2020.csv` | 2021-03-31T09:44:47.928290 | 86,769 |
| `ffr_phase2_auction_phase_resultsum` | `phase-2-ffr-auction-resultsummary-masterdata-2020-2021.csv` | 2021-04-01T10:32:10.734130 | 259,655 |
| `ffr_phase2_auction_phase_resultsum` | `phase-2-ffr-auction-resultsummary-masterdata-2021-2022.csv` | 2021-11-26T11:20:55.997220 | 176,739 |
| `ffr_phase2_auction_files` (ZIP, SILVER) | `resultsummary-2019-11-22-to-2019-11-29.zip` | 2021-03-31T09:22:26.071477 | 1,641 |
| `ffr_phase2_auction_files` (ZIP, SILVER) | `blockorders-2019-11-22-to-2019-11-29.zip` | 2021-03-31T09:18:59.033322 | 14,204 |
| `ffr_phase2_auction_files` (ZIP, SILVER) | `linearorders-2019-11-22-to-2020-01-03.zip` | 2021-03-31T09:19:40.922008 | 20,796 |
| `ffr_phase2_auction_files` (ZIP, SILVER) | `resultbyunit-2019-11-22-to-2019-11-29.zip` | 2021-03-31T09:20:11.157228 | 5,140 |

All are uploads (not datastore dumps), so the vintage is the CKAN `last_modified` of the captured file
(registry rule V-8 allows it for uploads). The "2021-2022" masters carry the same stamp family as the weekly
files (2021-11-26), while the "2020-2021" ones were stamped in March/April 2021 or March 2022; the stamps are
the vendor's upload times and are used as given.

Vendor dictionaries (human pages): the package page above lists one dictionary per resource. The
[2019-2020 BlockOrders master dictionary](https://www.neso.energy/data-portal/phase-2-ffr-auction-results-summary/phase_2_ffr_auction_blockorders_masterdata_2019-2020)
is the one that describes hourly capacity prices (see Units). The other resource dictionary addresses are
not recorded in the research files (`TODO: verify`; start from the package page). Saved field info (the
newest resource's dictionary per family): `.planning/research/neso-snapshots/field-info/20261008T114228Z/ffr_phase2_auction_phase_*.json`.

All 16 CSV bodies are valid UTF-8 (the records declare strict UTF-8) and the production CSV reader agreed
with a strict second parse on every retained cell. There are no wholly blank rows in any phase-2 CSV.

## The two clocks, family by family

Every silver row carries a **vintage** clock (`available_at`: when the data was available to gridflow's
consumers) and an **event** clock (`event_time`, equal to `timestamp_utc`: what the row is about). All
families use `issue: none`: no order or result has an evidenced publication instant, and `OrderEntryTime` is
the bid **submission** time, never an issue time.

| Family | Vintage clock (`available_at` = `published_at`) | Event clock (`event_time` = `timestamp_utc`) |
|---|---|---|
| `ffr_phase2_auction_phase_block_order` | `ckan_last_modified` of the weekly capture: 2021-11-26T11:15:54Z on every row | **`none`**: the **capture time** (`capture_written_at`, 2026-10-08T10:58:37Z) |
| `ffr_phase2_auction_phase_blockorders` (held) | `ckan_last_modified` of each resource's capture: three stamps (2021-03-31, 2022-03-18, 2021-11-26) | **`none`**: the capture time of the row's resource |
| `ffr_phase2_auction_phase_linear_orders` | `ckan_last_modified` of the weekly capture: 2021-11-26T11:16:28Z | **`none`**: the capture time |
| `ffr_phase2_auction_phase_linearorders` | `ckan_last_modified` of each resource's capture: three stamps (2021-03-31, 2021-11-26, 2022-03-18) | **`none`**: the capture time of the row's resource |
| `ffr_phase2_auction_phase_resultsbyunit` | `ckan_last_modified` of the capture that supplied the row: four stamps (three masters and the weekly) | `date_sp1(efa_date)`: the **start of the UK-local `efa_date`, as UTC**. A date anchor, **not an EFA block start** |
| `ffr_phase2_auction_phase_resultsum` (held) | as by-unit: four stamps | `date_sp1(efa_date)`: date anchor |
| `ffr_phase2_result_summary_archive` (held) | `ckan_last_modified` of the ZIP: 2021-03-31T09:22:26Z | `date_sp1(date)`: date anchor, not an EFA start |
| `ffr_phase2_blockorders_archive` (held) | `ckan_last_modified` of the ZIP: 2021-03-31T09:18:59Z on every row | **`none`**: the **capture time** |
| `ffr_phase2_linearorders_archive` (held) | `ckan_last_modified` of the ZIP: 2021-03-31T09:19:40Z on every row | **`none`**: the **capture time** |
| `ffr_phase2_results_by_unit_archive` (held) | `ckan_last_modified` of the ZIP: 2021-03-31T09:20:11Z on every row | `date_sp1(date)`: date anchor, not an EFA start |

**What `none` means here.** For the four current order tables and the block-order and linear-order archives `timestamp_utc` is the time
gridflow fetched the file (equal to `capture_written_at` on every row, checked in silver on 2026-10-13 for the
current tables and on 2026-10-14 for the two archives). It is **not** a delivery time
or a bid time. Filtering the order tables by `timestamp_utc` filters by fetch time (a single instant per
resource today) and never by delivery date. Their delivery start, delivery end and order-entry times are kept
as raw `string` columns, byte for byte as served.

**What the date anchor means.** For the result tables `event_time` is midnight of the UK-local `efa_date`
expressed as UTC (for a summer date that is 23:00 UTC the evening before; for a winter date it is 00:00 UTC).
All EFA blocks of a date share one anchor;
distinguish them by `efa`. **Never rebuild a block start from `efa_date` plus `efa`** (RULINGS 572 and 588).


**Why `efa_date` is a date anchor and not a delivery time.** The dictionary describes `EFA Date` as the
"equivalent date to the delivery end date in this instance" (weekly and by-unit dictionaries) but the master
summary dictionary calls it "Delivery Date". The two descriptions differ. `TODO: verify` which date the export
publishes (PHASE2-EFA-DATE-ROLE); the typed `efa_date` is the vendor's calendar date as served and is used
only as a date anchor.

**The naive delivery and entry strings (PHASE2-EXPORT-CLOCK).** `order_entry_time`, `delivery_start` and
`delivery_end` carry no offset and are spelled `YYYY-MM-DD HH:MM:SS` in the weekly files and in the
2019-2020 linear master, and `DD/MM/YYYY HH:MM` in the other masters (shapes measured in silver 2026-10-13).
The vendor states the auction runs on EFA blocks and the examples show 23:00 starts, but **the clock of the
export is not stated**. `TODO: verify` PHASE2-EXPORT-CLOCK: obtain a vendor statement covering Delivery
Start/End and OrderEntryTime in each export epoch. Until then do not parse them as UTC and do not parse them
as UK local time, and do not borrow the export clock of the later Dynamic Containment auctions merely because
those services followed this trial.

**Settlement periods.** None of the families has a settlement period or a `run_type`; neither is fabricated.

## Units and sentinels

**Units come only from the vendor's dictionaries** (saved field info; FACTS section "Clocks, issue and units");
none is inferred from a column name or from arithmetic.

| Columns | Unit (vendor dictionary) |
|---|---|
| `executed_volume`, `volume`, `v1`..`v4`, `cleared_volume` | **MW** per the newest dictionary of each table, except the master summary `cleared_volume`, whose dictionary says `number` (volumes of response; the weekly block-order volumes are negative, the sell-order convention) |
| by-unit `clearing_price` | **£/MW/h** (this resource's dictionary: "cleared price per MW per hour", weekly and master) |
| block `clearing_price`, `price` (weekly and masters) | **£/MW as published**; hour basis not stated in the newest dictionary (`TODO: verify` PHASE2-PRICE-DICTIONARY-CORRECTION, below) |
| linear `p1`..`p4` | **£/MW as published** (the newest linear dictionary); same open question |
| summary `clearing_price` (held) | **unresolved**: the weekly dictionary gives unit £/MW and describes it as the cleared price per MW per hour; the master dictionary gives the unit cell "number" (PHASE2-SUMMARY-PRICE-UNIT) |
| `efa` | weekly ordinal 1 to 42; no unit |
| identifiers (`order_id`, `order_period_id`, `trade_id`), `mar`, status and flag columns | opaque labels; no unit |
| `delivery_start`, `delivery_end`, `order_entry_time` | time labels; export clock unresolved |
| `efa_date` | calendar date |
| every archive value column (`clearing_price`, `price`, `p1`..`p16`, `cleared_volume`, `executed_volume`, `volume`, `v1`..`v16`) | **no unit stated**: the archive members have no data dictionary and the current tables' dictionaries are not transferred to them (PHASE2-ARCHIVE-SEMANTICS); price unit and hour basis `TODO: verify` |

Nothing is converted or rescaled. In the master summary dictionary the unit cells "string", "day", "datetime"
and "number" are **type words the vendor typed into the unit field**, not physical units; they appear in the
generated "Vendor unit" column below and must not be read as units.

**PHASE2-PRICE-DICTIONARY-CORRECTION (does not hold any output).** The older 2019-2020 BlockOrders master
dictionary and NESO's trial evaluation explicitly describe the capacity prices as hourly, whereas the newest
dictionaries label the order prices £/MW. The trial's own explanation points to an economic price of **£/MW/h**
(an inference from the trial evaluation, not a dictionary statement). Vendor confirmation that the newer £/MW
labels omit the hourly denominator would settle it. Until then the numeric prices are preserved as published
and **no rescaling is applied**.

**Typing and sentinels (K-AS-5 FACTS g5, g6; the AS-5a spec).** Identifiers (`order_id`, `order_period_id`,
`trade_id`) are `string` and byte-equal, never cast: a spreadsheet-style number would lose digits (the master
block exports already did, see the hold). `efa` is `int64`; measured values are `float64`; `efa_date` is
`date`; `mar` is a `string` raw indicator (the dictionary says only "Automatically infilled, please leave
blank"; its meaning and scale are `TODO: verify`, so no ratio or percentage is invented). **Zeros are real
values and stay zero. Negative volumes stay negative** (sell-order sign convention; no absolute value, no sign
flip, no null). **Blank cells in numeric columns are null; blank cells in string columns are null in silver**
(no empty-string cells were measured in any eligible family). The literal strings `NA` are **values, not
nulls**, in string columns; see the family notes (`block_code_prm`, linear `p3`..`v4`). No token map, no trim
and no min/max bound is configured. The `cancelled` column carries prose
(`Executed volume is over tested volume - cancelled`) kept as a string.

**LINEAR-NA-SEMANTICS (`TODO: verify`, does not hold).** The literal `NA` in the linear curve columns
`3P`, `3V`, `4P`, `4V` (36 rows in the weekly file and 36 rows in the 2021-2022 master) is not defined by
the vendor. A bid-curve export specification that defines unused point cells would decide whether it may
become a nullable number. Today those four columns are `string`, so `NA` is preserved and is never mapped to
zero or null.

## Weekly and master exports

The weekly files (one auction week, files published 2021-11-26) and the master exports (three trial years)
publish the same four tables under the same headers. The relationship was measured, not assumed (FACTS
"headers, pairs and grain", 2026-10-13):

| Pair | Weekly rows | Master rows | Relationship |
|---|---:|---:|---|
| Block order / BlockOrders | 379 | 85,662 | Same table. Weekly `OrderID`s are full-digit; master ones are in scientific notation. **No trustworthy identifier-based equivalence** |
| Linear orders / LinearOrders | 84 | 8,232 | All 84 weekly (MarketName, DeliveryStart) keys occur in the masters when the date spellings are parsed; the **full rows differ** |
| Results by unit / ResultsByUnit | 201 | 69,006 | All 201 weekly business keys, **and their normalised full rows**, occur in the masters |
| Results summary / ResultSummary | 84 | 8,652 | Same: all 84 weekly keys and rows occur in the masters |

(The by-unit and summary master counts are the **distinct business keys across the three masters**; the
silver base table also holds the weekly rows, see below.)

How gridflow treats them:

- **Order tables are separate tables per export.** The weekly block-order table, the master block-order
  table, the weekly linear table and the master linear table are four different families. They overlap in
  coverage, so **never union them and never add their volumes**. A consumer that wants the master history
  uses the master family and a consumer that wants the weekly files uses the weekly family; there is no
  merged order book.
- **Result tables are deduplicated to the master rows.** By-unit and summary rows from the weekly file and
  the three masters land in one silver table per result (the weekly resource is a sibling of the master
  family). The `_latest` view is `key_latest` over the business key: where a key occurs twice the row from
  the capture with the later CKAN `last_modified` is kept, which is the **master** (the 2021-2022 master was
  stamped 2021-11-26T11:20:28Z for by-unit and 11:20:55Z for summary, later than the weekly stamps of
  11:17:15Z and 11:17:51Z). Measured in silver: by-unit has 69,207 base rows and 69,006 distinct keys (201
  keys occur twice, once weekly and once in the master); the summary has 8,736 base rows and 8,652 distinct
  keys (84 repeated).
- **Weekly delivery coverage is not complete.** The weekly by-unit file does not contain all the delivery
  periods present in the weekly summary; do not manufacture missing unit results from the summary.

This overlap is design, not a defect. The reconcile overlap check is separate: see the activation receipt.

## Families

Thirteen families: six current record families with silver, four held archive families, two weekly siblings with no silver, and a file catalogue. The "Vendor unit" column below
is the unit stated in the vendor's saved field-info dictionary for the newest resource; it is sparse because
the dictionary states a unit for only some columns, and for the summary it reproduces type words (see Units).
Silver rows at activation: 172,300 in the six current record families (2026-10-13, AS-5a), 168 in the summary archive (AS-5a) and 2,066 in the three archives added by AS-5c (2026-10-14: 1,042 + 588 + 436):

| Family | Status | Silver rows |
|---|---|---:|
| `ffr_phase2_auction_phase_block_order` | eligible | 379 |
| `ffr_phase2_auction_phase_blockorders` | **held** (PHASE2-MASTER-ORDER-ID) | 85,662 |
| `ffr_phase2_auction_phase_linear_orders` | eligible | 84 |
| `ffr_phase2_auction_phase_linearorders` | eligible | 8,232 |
| `ffr_phase2_auction_phase_resultsbyunit` | eligible | 69,207 base · 69,006 `_latest` |
| `ffr_phase2_auction_phase_resultsum` | **held** (PHASE2-SUMMARY-PRICE-UNIT) | 8,736 base · 8,652 `_latest` |
| `ffr_phase2_result_summary_archive` | **held** (archive date and EFA semantics) | 168 |
| `ffr_phase2_blockorders_archive` | **held** (PHASE2-ARCHIVE-SEMANTICS) | 1,042 |
| `ffr_phase2_linearorders_archive` | **held** (PHASE2-ARCHIVE-SEMANTICS) | 588 |
| `ffr_phase2_results_by_unit_archive` | **held** (PHASE2-ARCHIVE-SEMANTICS) | 436 (957 rows in bronze; the 521-row 2019-11-22 member is held back) |
| `ffr_phase2_auction_phase_results_unit`, `..._results_sum` | siblings, ingest-only | no silver of their own |
| `ffr_phase2_auction_files` | catalogue only | none |

Silver path for every family: `C:/gridflow-data/silver/neso_data_portal/<family>/year=2026/month=10/`, one
Parquet file per captured resource, with the vendor columns (renamed to snake_case), `resource_id` where the
key needs it, then the 8 gridflow columns (`timestamp_utc`, `published_at`, `bronze_capture_id`,
`capture_written_at`, `event_time`, `available_at`, `source_run_id`, `dataset_version`). Column counts at
activation: block order 32, master block 33, linear 30, master linear 31, by-unit 18, summary 15, summary archive 15, block-order archive 32, linear-order archive 56, by-unit archive 17.

### `ffr_phase2_auction_files`

- Kind: files · archetype: EVT · refresh: frozen · empty allowed: no
- files: catalogue only

The file catalogue for the package's four ZIP archives (the generated line says "catalogue only": no
tabular silver of its own). Resource-level dispositions are in the table at the top: each of the four ZIPs
feeds one held archive family (`ResultSummary`, `BlockOrders`, `LinearOrders`, `ResultByUnit`). 12 of the 13
members are SILVER; the 2019-11-22 `ResultByUnit` member is HOLD. No data from the held archives is published.

### `ffr_phase2_auction_phase_block_order`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| MarketName | `market_name` | string | — | yes | — | — |
| BiddingLevelName | `bidding_level_name` | string | — | yes | — | — |
| MemberName | `member_name` | string | — | yes | — | — |
| OrderID | `order_id` | string | — | no | — | — |
| Portfolio | `portfolio` | string | — | yes | — | — |
| OrderEntryTime | `order_entry_time` | string | — | yes | — | — |
| OrderEntryUser | `order_entry_user` | string | — | yes | — | — |
| SettlementCurrency | `settlement_currency` | string | — | yes | — | — |
| ClearingPrice | `clearing_price` | float64 | — | yes | — | £/MW |
| Price | `price` | float64 | — | yes | — | £/MW |
| MAR | `mar` | string | — | yes | — | — |
| Status | `status` | string | — | yes | — | — |
| BlockCode | `block_code` | string | — | yes | — | — |
| BlockCodePRM | `block_code_prm` | string | — | yes | — | — |
| Paradoxically | `paradoxically` | string | — | yes | — | — |
| OrderPeriodID | `order_period_id` | string | — | yes | — | — |
| TradeID | `trade_id` | string | — | yes | — | — |
| EFA | `efa` | int64 | — | yes | — | — |
| DeliveryStart | `delivery_start` | string | — | yes | — | — |
| DeliveryEnd | `delivery_end` | string | — | yes | — | — |
| ExecutedVolume | `executed_volume` | float64 | — | yes | — | MW |
| Volume | `volume` | float64 | — | yes | — | MW |
| Invalid | `invalid` | string | — | yes | — | — |
| Bid Validity | `bid_validity` | string | — | yes | — | — |

- Entity key: `order_id`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

The **weekly block-order export**. Resource `edfb5b8f-4415-45e6-b378-57020c41e96b`, one capture (2026-10-08,
80,174 bytes). **Silver: 379 rows**, one Parquet file, 24 vendor columns then the 8 gridflow columns (32).
**Status: eligible.**

- **Grain.** One row per order period (a bid or executed block). `order_id` is unique in this body (379
  distinct); in the masters orders repeat over periods, so do not generalise this key to the masters.
- **Prices.** `price` and `clearing_price` are **£/MW as published** (hour basis open, see Units).
  `executed_volume` and `volume` are MW; **all 379 `volume` cells are negative** (sell orders).
- **Sentinels measured.** `block_code_prm` is `NA` on all 299 `C01` rows and on none of the 80 `C02` rows
  (the dictionary says it is blank for a C01 block and holds the parent Order ID for a C02 block; the
  literal `NA` is kept, never mapped to zero). `invalid` is `FALSE` on all 379 rows. `bid_validity` is blank
  on all 379 rows, so it is null in silver on every row. `status` takes the two values `Executed` and
  `Rejected`.
- **Clocks.** Vintage CKAN `last_modified` 2021-11-26T11:15:54Z; event recipe `none` (capture time).
  `order_entry_time`, `delivery_start` and `delivery_end` are raw naive strings (PHASE2-EXPORT-CLOCK).
- **Dictionary.** The vendor describes `OrderID` as an integer, but the silver column is `string` and
  byte-equal to the file.

### `ffr_phase2_auction_phase_blockorders`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| MarketName | `market_name` | string | — | no | — | — |
| BiddingLevelName | `bidding_level_name` | string | — | no | — | — |
| MemberName | `member_name` | string | — | no | — | — |
| OrderID | `order_id` | string | — | no | — | — |
| Portfolio | `portfolio` | string | — | no | — | — |
| OrderEntryTime | `order_entry_time` | string | — | no | — | — |
| OrderEntryUser | `order_entry_user` | string | — | no | — | — |
| SettlementCurrency | `settlement_currency` | string | — | no | — | — |
| ClearingPrice | `clearing_price` | float64 | — | no | — | £/MW |
| Price | `price` | float64 | — | no | — | £/MW |
| MAR | `mar` | string | — | no | — | — |
| Status | `status` | string | — | no | — | — |
| BlockCode | `block_code` | string | — | no | — | — |
| BlockCodePRM | `block_code_prm` | string | — | no | — | — |
| Paradoxically | `paradoxically` | string | — | no | — | — |
| OrderPeriodID | `order_period_id` | string | — | no | — | — |
| TradeID | `trade_id` | string | — | no | — | — |
| EFA | `efa` | int64 | — | no | — | — |
| DeliveryStart | `delivery_start` | string | — | no | — | — |
| DeliveryEnd | `delivery_end` | string | — | no | — | — |
| ExecutedVolume | `executed_volume` | float64 | — | no | — | MW |
| Volume | `volume` | float64 | — | no | — | MW |
| Invalid | `invalid` | string | — | no | — | — |
| Bid Validity | `bid_validity` | string | — | yes | — | — |

- Entity key: `resource_id`, `market_name`, `bidding_level_name`, `member_name`, `order_id`, `portfolio`, `order_entry_time`, `order_entry_user`, `settlement_currency`, `clearing_price`, `price`, `mar`, `status`, `block_code`, `block_code_prm`, `paradoxically`, `order_period_id`, `trade_id`, `efa`, `delivery_start`, `delivery_end`, `executed_volume`, `volume`, `invalid`, `bid_validity`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

The **master block-order exports**, three resources (2019-2020, 2020-2021, 2021-2022), one capture each.
**Silver: 85,662 rows** (12,446 for `979329c3-5587-4b08-a900-5520b58b2d8f`, 50,145 for
`c074d827-ad03-4b11-b22e-8bbc96be3bab`, 23,071 for `89467af0-a577-4bba-9955-f8c380a78923`), three Parquet
files, 24 vendor columns, `resource_id` and the 8 gridflow columns (33). **Status: HELD (E-SEM, a vendor
identifier question).**

**Held; no data values are published for this family.** This page documents the schema, the row counts,
the clocks and the hold question only. It gives no sample row and no minimum, maximum or other statistic.

- **Hold, PHASE2-MASTER-ORDER-ID (unit v0.22-K-AS-5a).** The three master exports write OrderID, OrderPeriodID
  and TradeID in spreadsheet scientific notation (1E+14, 1.00E+14), so no row keeps a recoverable order
  identity and the record's key is the complete row (`resource_id` plus all 24 vendor columns, `bid_validity`
  being the only nullable key column); can NESO republish the masters with full identifiers? (The 2019-2020
  master dictionary and the trial evaluation describe hourly capacity prices while the newest dictionary
  labels prices £/MW; delivery and entry times are naive with an undocumented export clock.)
- **Key.** The complete row is the entity key. The weekly `order_id` is not a join key to this table (the
  masters' identifiers are collapsed).
- **Clocks.** Vintage `ckan_last_modified` per resource; event recipe `none` (capture time). Naive time
  strings (PHASE2-EXPORT-CLOCK). **Prices are published as served; no rescaling.**

### `ffr_phase2_auction_phase_linear_orders`

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
| 3P | `p3` | string | — | yes | — | £/MW |
| 3V | `v3` | string | — | yes | — | MW |
| 4P | `p4` | string | — | yes | — | £/MW |
| 4V | `v4` | string | — | yes | — | MW |

- Entity key: `order_period_id`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

The **weekly linear-order export** (the market buy curve per delivery period). Resource
`5cce4cb6-c270-488f-96c7-9f5cd7476898`, one capture (2026-10-08, 16,283 bytes). **Silver: 84 rows**, one
Parquet file, 22 vendor columns then the 8 gridflow columns (30). **Status: eligible.**

- **Grain.** One row per delivery period of a market, with up to four price/volume points (`p1`..`v4`;
  vendor `1P`..`4V`, renamed because a silver name must begin with a letter). `order_period_id` is unique
  in this body (84 distinct).
- **Typing.** `p1`, `v1`, `p2`, `v2` are `float64`; `p3`, `v3`, `p4`, `v4` are `string` because the literal
  `NA` occurs in 36 rows of each (LINEAR-NA-SEMANTICS). Prices are **£/MW as published**; volumes MW.
- **Clocks.** Vintage CKAN `last_modified` 2021-11-26T11:16:28Z; event recipe `none` (capture time). Time
  cells are raw naive strings.

### `ffr_phase2_auction_phase_linearorders`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| MarketName | `market_name` | string | — | no | — | — |
| BiddingLevelName | `bidding_level_name` | string | — | yes | — | — |
| MemberName | `member_name` | string | — | yes | — | — |
| OrderID | `order_id` | string | — | yes | — | — |
| Portfolio | `portfolio` | string | — | yes | — | — |
| OrderEntryTime | `order_entry_time` | string | — | yes | — | — |
| OrderEntryUser | `order_entry_user` | string | — | yes | — | — |
| SettlementCurrency | `settlement_currency` | string | — | yes | — | — |
| OrderPeriodID | `order_period_id` | string | — | yes | — | — |
| TradeID | `trade_id` | string | — | yes | — | — |
| EFA | `efa` | int64 | — | yes | — | — |
| DeliveryStart | `delivery_start` | string | — | no | — | — |
| DeliveryEnd | `delivery_end` | string | — | yes | — | — |
| ExecutedVolume | `executed_volume` | float64 | — | yes | — | MW |
| 1P | `p1` | float64 | — | yes | — | £/MW |
| 1V | `v1` | float64 | — | yes | — | MW |
| 2P | `p2` | float64 | — | yes | — | £/MW |
| 2V | `v2` | float64 | — | yes | — | MW |
| 3P | `p3` | string | — | yes | — | £/MW |
| 3V | `v3` | string | — | yes | — | MW |
| 4P | `p4` | string | — | yes | — | £/MW |
| 4V | `v4` | string | — | yes | — | MW |

- Entity key: `resource_id`, `market_name`, `delivery_start`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

The **master linear-order exports**, three resources (2019-2020 `47ceb316-e284-4e14-bb67-76067a8f9562`,
1,008 rows; 2020-2021 `404a1de1-5fe9-4569-815a-394e83af96eb`, 4,284 rows; 2021-2022
`eb394ce7-20c6-4434-a263-470b2896fd7b`, 2,940 rows). **Silver: 8,232 rows**, three Parquet files, 22 vendor
columns, `resource_id` and the 8 gridflow columns (31). **Status: eligible.**

- **Key.** (`resource_id`, `market_name`, `delivery_start`), measured unique within and across the masters
  (8,232 distinct). This is **measured identity, not a vendor guarantee** of global stability
  (`TODO: verify`), and `delivery_start` is the raw string.
- **Typing.** As the weekly table: `p1`..`v2` `float64`, `p3`..`v4` `string` with `NA` in 36 rows of the
  2021-2022 master.
- **Relation to the weekly file.** The weekly file's 84 (MarketName, DeliveryStart) keys also occur here with
  different full rows; the two stay separate families, never unioned.
- **Clocks.** Vintage CKAN `last_modified` per resource; event recipe `none` (capture time). Time cells are
  raw naive strings, spelled ISO-like in the 2019-2020 master and `DD/MM/YYYY HH:MM` in the other two.

### `ffr_phase2_auction_phase_results_sum`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no
- ingest-only: no silver yet

The **weekly results-summary** bronze family (resource `a9659701-f0d4-40d2-91f1-31f4bac0619d`, one capture,
5,522 bytes). It is a **sibling** of `ffr_phase2_auction_phase_resultsum`: it has its own bronze capture
family but no silver of its own; its 84 rows land in the `resultsum` silver table (held, below).

### `ffr_phase2_auction_phase_results_unit`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no
- ingest-only: no silver yet

The **weekly results-by-unit** bronze family (resource `87ee8fc4-11ae-4575-b734-99548aab2d98`, one capture,
19,729 bytes). It is a **sibling** of `ffr_phase2_auction_phase_resultsbyunit`: it has its own bronze capture
family but no silver of its own; its 201 rows land in the `resultsbyunit` silver table.

### `ffr_phase2_auction_phase_resultsbyunit`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Company | `company` | string | — | yes | — | — |
| Unit Name | `unit_name` | string | — | no | — | — |
| EFA Date | `efa_date` | date | `ngeso_fra-weekly_2021-11-26_resultsbyunit.csv` → `%Y-%m-%d`; `phase-2-ffr-auction-resultsbyunit-masterdata-2019-2020.csv` → `%d/%m/%Y`; `phase-2-ffr-auction-resultsbyunit-masterdata-2020-2021.csv` → `%d/%m/%Y`; `phase-2-ffr-auction-resultsbyunit-masterdata-2021-2022.csv` → `%d/%m/%Y` | no | — | — |
| Delivery Start | `delivery_start` | string | — | yes | — | — |
| Delivery End | `delivery_end` | string | — | yes | — | — |
| EFA | `efa` | int64 | — | no | — | — |
| Service | `service` | string | — | no | — | — |
| Cleared Volume | `cleared_volume` | float64 | — | yes | — | MW |
| Clearing Price | `clearing_price` | float64 | — | yes | — | £/MW/h |
| Cancelled | `cancelled` | string | — | yes | — | — |

- Entity key: `unit_name`, `efa_date`, `efa`, `service`
- Latest: `key_latest`
- Temporal recipe: date_sp1 (`efa_date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

The **results by unit**, the weekly file plus the three masters, in one silver table. Resources
`87ee8fc4-...` (weekly, 201 rows), `15d7fa42-1c8d-4a79-86f8-890cf9228794` (2019-2020, 9,985),
`52faffc9-e804-44d8-b222-dd0821d79e7d` (2020-2021, 39,765) and `feafb7ab-7db6-406e-a46f-bbcf6ed92ba1`
(2021-2022, 19,256). **Silver: 69,207 base rows, 69,006 `_latest` rows**, four Parquet files, 10 vendor
columns then the 8 gridflow columns (18). **Status: eligible** (both dictionaries state £/MW/h for the price).

- **Grain.** One row per unit, service, EFA date and EFA block: the volume cleared to that unit and the
  clearing price. Services are `DLH` and `LFS`; `efa` runs 1 to 42; `efa_date` runs 2019-12-07 to 2021-11-30.
- **Key.** (`unit_name`, `efa_date`, `efa`, `service`): the measured business key passes across the complete
  master bodies; service is kept as an explicit dimension. `_latest` is `key_latest` (see Weekly and master
  exports): 69,006 distinct keys.
- **Date typing.** `efa_date` is parsed per file name: `%Y-%m-%d` for the weekly file and `%d/%m/%Y` for the
  three masters (the formats table above). A row whose date does not match its file's format would be a recorded failure, never a silent drop; none occurred at activation.
- **Units and cells.** `cleared_volume` MW, `clearing_price` **£/MW/h** (vendor). `cancelled` carries the
  prose `Executed volume is over tested volume - cancelled` in 84 rows and is null in the other 69,123.
- **Clocks.** Vintage: four CKAN stamps (see the fetch table). Event: `date_sp1(efa_date)`, a date anchor.
  `delivery_start` / `delivery_end` are raw naive strings (ISO-like in the weekly file, `DD/MM/YYYY HH:MM` in
  the masters); `TODO: verify` PHASE2-EXPORT-CLOCK.

### `ffr_phase2_auction_phase_resultsum`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Service | `service` | string | — | no | — | string |
| EFA Date | `efa_date` | date | `ngeso_fra-weekly_2021-11-26_resultsummary.csv` → `%Y-%m-%d`; `phase-2-ffr-auction-resultsummary-masterdata-2019-2020.csv` → `%d/%m/%Y`; `phase-2-ffr-auction-resultsummary-masterdata-2020-2021.csv` → `%d/%m/%Y`; `phase-2-ffr-auction-resultsummary-masterdata-2021-2022.csv` → `%d/%m/%Y` | no | — | day |
| Delivery Start | `delivery_start` | string | — | yes | — | datetime |
| Delivery End | `delivery_end` | string | — | yes | — | — |
| EFA | `efa` | int64 | — | no | — | number |
| Cleared Volume | `cleared_volume` | float64 | — | yes | — | number |
| Clearing Price | `clearing_price` | float64 | — | yes | — | number |

- Entity key: `service`, `efa_date`, `efa`
- Latest: `key_latest`
- Temporal recipe: date_sp1 (`efa_date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

The **results summary**, the weekly file plus the three masters, in one silver table. Resources
`a9659701-f0d4-40d2-91f1-31f4bac0619d` (weekly, 84 rows), `8b5fa222-f39f-4eea-9475-728ea8365ff3`
(2019-2020, 1,428), `279572a9-21c9-4e1e-a7c8-7aed233f8936` (2020-2021, 4,284) and
`920105e5-a5e3-4bed-83ce-ab6901cc1b84` (2021-2022, 2,940). **Silver: 8,736 base rows, 8,652 `_latest` rows**,
four Parquet files, 7 vendor columns then the 8 gridflow columns (15). **Status: HELD (E-SEM, a vendor
unit question).**

**Held; no data values are published for this family.** This page documents the schema, the row counts,
the clocks and the hold question only. It gives no sample row and no minimum, maximum or other statistic
for `cleared_volume` or `clearing_price`.

- **Hold, PHASE2-SUMMARY-PRICE-UNIT (unit v0.22-K-AS-5a).** The weekly results-summary dictionary gives
  Clearing Price the unit £/MW while describing it as the cleared price per MW per hour, and the masterdata
  dictionary gives it no unit ("number"); the by-unit results tables state £/MW/h. Which rate dimension does
  the summary export publish? (Delivery start / end cells are naive with an undocumented export clock.)
  `cleared_volume` is MW per the weekly dictionary (the master dictionary gives "number").
- **Key.** (`service`, `efa_date`, `efa`): unique across the complete master bodies; 8,652 distinct keys.
  `_latest` is `key_latest`.
- **Clocks.** Vintage: four CKAN stamps. Event: `date_sp1(efa_date)`, a date anchor. `efa_date` is parsed as
  `%Y-%m-%d` (weekly) or `%d/%m/%Y` (masters).

### `ffr_phase2_result_summary_archive`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Service | `service` | string | — | no | — | — |
| Date | `date` | date | `%Y-%m-%d` | no | — | — |
| EFA | `efa` | int64 | — | no | — | — |
| Cleared Volume | `cleared_volume` | float64 | — | yes | — | — |
| Clearing Price | `clearing_price` | float64 | — | yes | — | — |

- Entity key: `service`, `date`, `efa`
- Latest: `key_latest`
- Temporal recipe: date_sp1 (`date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

The **historic result-summary archive**: the two CSV members of the ZIP
`ResultSummary 2019-11-22 to 2019-11-29` (resource `3928f192-97a5-4b4f-9234-0dcc9ad071a0`, one capture,
1,641 bytes), 84 rows each. **Silver: 168 rows**, one Parquet file, 5 vendor columns, `child_id`,
`child_crc32` and the 8 gridflow columns (15). **Status: HELD** (unit AS-5).

**Held; no data values are published for this family.** The archive record is an existing one that AS-5a
created and AS-5c did not change (record, container, children and its 168 rows are as before). The archive
Date convention is the open question; the three sibling archives (block orders, linear orders, results by
unit) are now modelled as their own held families, below.

- **Hold (unit AS-5).** Phase-2 FFR archive: Date and EFA (1-42) semantics are undocumented;
  `timestamp_utc` is `date_sp1` of Date, not an EFA block start.
- **Clocks.** Vintage CKAN `last_modified` of the ZIP, 2021-03-31T09:22:26Z. Event `date_sp1(date)`.
- **TODO: ARCHIVE-DATE-CONVENTION.** The archive `Date` labels are not interchangeable with the current
  `EFA Date` merely by renaming; a vendor archive definition would settle it. No synthetic EFA timestamp is
  produced.
- **Member ownership.** The two members are read only by this record; AS-5c added no archive pattern that
  matches a ResultSummary member.

### `ffr_phase2_blockorders_archive`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

Schema, epoch 1 (one epoch, 22 vendor columns):

| Vendor column | Silver column | Dtype | Nullable | Vendor unit |
|---|---|---|---|---|
| MarketName | `market_name` | string | yes | — |
| BiddingLevelName | `bidding_level_name` | string | yes | — |
| MemberName | `member_name` | string | yes | — |
| OrderID | `order_id` | string | no | — |
| Portfolio | `portfolio` | string | yes | — |
| OrderEntryTime | `order_entry_time` | string | yes | — |
| OrderEntryUser | `order_entry_user` | string | yes | — |
| SettlementCurrency | `settlement_currency` | string | yes | — |
| ClearingPrice | `clearing_price` | float64 | yes | — (`TODO: verify`) |
| Price | `price` | float64 | yes | — (`TODO: verify`) |
| MAR | `mar` | string | yes | — |
| Status | `status` | string | yes | — |
| BlockCode | `block_code` | string | yes | — |
| BlockCodePRM | `block_code_prm` | string | yes | — |
| Paradoxically | `paradoxically` | string | yes | — |
| OrderPeriodID | `order_period_id` | string | yes | — |
| TradeID | `trade_id` | string | yes | — |
| EFA | `efa` | int64 | yes | — |
| DeliveryStart | `delivery_start` | string | yes | — |
| DeliveryEnd | `delivery_end` | string | yes | — |
| ExecutedVolume | `executed_volume` | float64 | yes | — (`TODO: verify`) |
| Volume | `volume` | float64 | yes | — (`TODO: verify`) |

- Entity key: `order_id`, `order_period_id`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured ZIP (ADR-030): 2021-03-31T09:18:59Z |
| `available_at` | = `published_at` |

The **block-order archive**: the two CSV members of the ZIP `BlockOrders 2019-11-22 to 2019-11-29` (resource
`e988552e-8bc1-43db-af15-cff01e40d83c`, one capture 2026-10-08, 14,204 bytes): the 2019-11-22 member (606
rows) and the 2019-11-29 member (436 rows). **Silver: 1,042 rows**, one Parquet file, the 22 vendor columns,
`child_id`, `child_crc32` and the 8 gridflow columns (32). **Status: HELD** (E-SEM, unit `v0.22-K-AS-5c`).

**Held; no data values are published for this family.** This page gives the schema, row counts and clocks only.

- **Hold, PHASE2-ARCHIVE-SEMANTICS (unit v0.22-K-AS-5c).** The 2019-11 to 2020-01 Phase-2 FFR archive members
  have no data dictionary: their price unit and hour basis, the export clock of the naive delivery and
  order-entry times, and (for results) whether the archive `Date` is the EFA date of the later masterdata
  exports are undocumented, and the current tables' dictionaries are not transferred to the archive.
- **Not the master or weekly order tables.** The archive covers earlier auctions than the masters and is a
  separate family; never add it to the weekly or master order tables. Unlike them it has no `Invalid` or
  `Bid Validity` column (22 vendor columns against 24). Its identifiers are `string`, kept as served.
- **Clocks.** Vintage `ckan_last_modified` of the ZIP; event recipe `none`: `timestamp_utc` is the capture time
  (equal to `capture_written_at` on every row). Delivery and entry times are raw `string` cells
  (PHASE2-EXPORT-CLOCK, `TODO: verify` per archive epoch).

### `ffr_phase2_linearorders_archive`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

Schema, three epochs. Each epoch declares only the points its header has: **12, 14 or 16 price/volume points**
(38, 42 and 46 vendor columns). The silver table is the typed-null union of the three epochs, so a point that
an epoch's header lacks is null in that epoch's rows (no padding is declared inside an epoch). Columns:

| Vendor column | Silver column | Dtype | Vendor unit |
|---|---|---|---|
| MarketName, BiddingLevelName, MemberName, OrderID, Portfolio, OrderEntryTime, OrderEntryUser, SettlementCurrency, OrderPeriodID, TradeID, DeliveryStart, DeliveryEnd | `market_name`, `bidding_level_name`, `member_name`, `order_id`, `portfolio`, `order_entry_time`, `order_entry_user`, `settlement_currency`, `order_period_id`, `trade_id`, `delivery_start`, `delivery_end` | string (`market_name` not nullable) | — |
| EFA | `efa` | int64 | — |
| ExecutedVolume | `executed_volume` | float64 | — (`TODO: verify`) |
| 1P, 1V, 2P, 2V | `p1`, `v1`, `p2`, `v2` | float64 | — (`TODO: verify`) |
| 3P, 3V, 4P, 4V | `p3`, `v3`, `p4`, `v4` | string (the dtype of the current linear tables) | — (`TODO: verify`) |
| 5P..16P, 5V..16V (where the epoch has them) | `p5`..`p16`, `v5`..`v16` | float64 (planner's choice: every archive curve cell is numeric) | — (`TODO: verify`) |

- Entity key: `market_name`, `delivery_start`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured ZIP (ADR-030): 2021-03-31T09:19:40Z |
| `available_at` | = `published_at` |

The **linear-order archive**: the seven weekly CSV members (2019-11-22, 2019-11-29, 2019-12-06, 2019-12-13,
2019-12-20, 2019-12-27 and 2020-01-03) of the ZIP `LinearOrders 2019-11-22 to 2020-01-03` (resource
`7ab29f1c-4da1-4f36-b611-cb74f62737fc`, one capture 2026-10-08, 20,796 bytes), 84 rows each.
**Silver: 588 rows**, one Parquet file, up to 46 vendor columns (the 14 non-curve columns, then `p1`..`p16` and
`v1`..`v16` where present), `child_id`, `child_crc32` and the 8 gridflow columns (56 in the union).
**Status: HELD** (E-SEM, unit `v0.22-K-AS-5c`).

**Held; no data values are published for this family.** Schema, row counts and clocks only. The meaning of the
literal `NA` in the current linear tables (LINEAR-NA-SEMANTICS) is not asserted for the archive; `p3`..`v4`
are `string` for dtype compatibility with the current tables only.

- **Hold, PHASE2-ARCHIVE-SEMANTICS (unit v0.22-K-AS-5c):** as for the block-order archive (no dictionary; price
  unit and hour basis, export clock of the naive times).
- **Key.** (`market_name`, `delivery_start`), unique across the seven members as measured at activation;
  `delivery_start` is the raw string. This is measured identity, not a vendor guarantee (`TODO: verify`).
- **Clocks.** Vintage `ckan_last_modified` of the ZIP; event recipe `none` (capture time, equal to
  `capture_written_at` on every row). Time cells are raw `string`.

### `ffr_phase2_results_by_unit_archive`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

Schema, epoch 1 (one epoch, 7 vendor columns):

| Vendor column | Silver column | Dtype | Format | Nullable | Vendor unit |
|---|---|---|---|---|---|
| Company | `company` | string | — | yes | — |
| Unit Name | `unit_name` | string | — | no | — |
| Date | `date` | date | `%Y-%m-%d` | no | — |
| EFA | `efa` | int64 | — | no | — |
| Service | `service` | string | — | no | — |
| Cleared Volume | `cleared_volume` | float64 | — | yes | — (`TODO: verify`) |
| Clearing Price | `clearing_price` | float64 | — | yes | — (`TODO: verify`) |

- Entity key: `unit_name`, `date`, `efa`, `service`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured ZIP (ADR-030): 2021-03-31T09:20:11Z |
| `available_at` | = `published_at` |

The **results-by-unit archive**: the ZIP `ResultByUnit 2019-11-22 to 2019-11-29` (resource
`a99410bb-5501-4292-a308-eb7c16b1b3f4`, one capture 2026-10-08, 5,140 bytes) has two CSV members, of which only
the **2019-11-29** member is read. **Silver: 436 rows**, one Parquet file, 7 vendor columns, `child_id`,
`child_crc32` and the 8 gridflow columns (17). The bronze total is 957 rows; the other 521 rows are the held
2019-11-22 member (below). **Status: HELD** (E-SEM, unit `v0.22-K-AS-5c`).

**Held; no data values are published for this family.** Schema, row counts and clocks only.

- **Hold, PHASE2-ARCHIVE-SEMANTICS (unit v0.22-K-AS-5c):** as for the block-order archive. For this table the
  open point is whether the archive `Date` is the EFA date of the later masterdata exports. `date` is typed as
  a plain `date` (format `%Y-%m-%d`); a cell that does not match fails the capture whole rather than being
  dropped. The price unit is not stated (the current by-unit tables state £/MW/h, but that is not transferred
  to the archive).
- **Event time.** `date_sp1(date)`: the start of the UK-local date as UTC, a **date anchor, not an EFA block
  start** (RULINGS 572 and 588). Never rebuild a block start from `date` plus `efa`. Vintage is the ZIP's
  `ckan_last_modified`.
- **The 2019-11-22 member is held (PHASE2-ARCHIVE-BYUNIT-COLLISION, unit v0.22-K-AS-5c).** It is read by no
  record: its 521 rows stay in immutable bronze and produce no silver. Reason: it carries two rows for one
  unit, date, EFA block and service with the same clearing price but different cleared volumes, which would
  make the entity key non-unique; which row is the result, or are both legitimate? The rows are neither
  deduplicated nor chosen between. If a record read both members, the capture would fail whole
  (`DuplicateEntityKeyError`) and write no silver, so the 436 rows would wait with it.

## Cadence

- Registry refresh: frozen
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Not Active

The vendor states the package is "Not Active". gridflow has **one capture per resource** (2026-10-08), so
whether the files will ever change, and their amendment and deletion behaviour, are unmeasured
(`TODO: verify` by comparing later complete captures against the hash-pinned bodies). The registry refresh is
`frozen`, so nothing re-fetches on a schedule. All captures are uploads; their CKAN `last_modified` stamps
are the vendor's upload times (2021-03 to 2022-03) and are far older than the capture.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence). Any gridflow
output derived from this package carries the attribution line "Supported by National Energy SO Open Data".

## Holds

- `ffr_phase2_auction_phase_blockorders`: held: TODO: PHASE2-MASTER-ORDER-ID — the three Phase-2 FFR BlockOrders masterdata exports write OrderID, OrderPeriodID and TradeID in spreadsheet scientific notation (1E+14, 1.00E+14), so no row keeps a recoverable order identity and the record's key is the complete row; can NESO republish the masters with full identifiers? (The 2019-2020 master dictionary and the trial evaluation describe hourly capacity prices while the newest dictionary labels prices £/MW; delivery and entry times are naive with an undocumented export clock.) (unit v0.22-K-AS-5a)
- `ffr_phase2_auction_phase_resultsum`: held: TODO: PHASE2-SUMMARY-PRICE-UNIT — the weekly results-summary dictionary gives Clearing Price the unit £/MW while describing it as the cleared price per MW per hour, and the masterdata dictionary gives it no unit ("number"); the by-unit results tables state £/MW/h. Which rate dimension does the summary export publish? (Delivery start / end cells are naive with an undocumented export clock.) (unit v0.22-K-AS-5a)
- `ffr_phase2_result_summary_archive`: held: Phase-2 FFR archive: Date and EFA (1-42) semantics are undocumented; timestamp_utc is date_sp1 of Date, not an EFA block start (unit AS-5)
- `ffr_phase2_blockorders_archive`: held: TODO: PHASE2-ARCHIVE-SEMANTICS — the 2019-11 to 2020-01 Phase-2 FFR archive members have no data dictionary: their price unit and hour basis, the export clock of the naive delivery and order-entry times, and (for results) whether the archive `Date` is the EFA date of the later masterdata exports are undocumented, and the current tables' dictionaries are not transferred to the archive. (unit v0.22-K-AS-5c)
- `ffr_phase2_linearorders_archive`: held: TODO: PHASE2-ARCHIVE-SEMANTICS — the 2019-11 to 2020-01 Phase-2 FFR archive members have no data dictionary: their price unit and hour basis, the export clock of the naive delivery and order-entry times, and (for results) whether the archive `Date` is the EFA date of the later masterdata exports are undocumented, and the current tables' dictionaries are not transferred to the archive. (unit v0.22-K-AS-5c)
- `ffr_phase2_results_by_unit_archive`: held: TODO: PHASE2-ARCHIVE-SEMANTICS — the 2019-11 to 2020-01 Phase-2 FFR archive members have no data dictionary: their price unit and hour basis, the export clock of the naive delivery and order-entry times, and (for results) whether the archive `Date` is the EFA date of the later masterdata exports are undocumented, and the current tables' dictionaries are not transferred to the archive. (unit v0.22-K-AS-5c)
- Member `ResultByUnit 2019-11-22 to 2019-11-29/NGESO_FRA_2019-11-22_ResultsByUnit.csv` (of the by-unit archive ZIP): HOLD, no silver: TODO: PHASE2-ARCHIVE-BYUNIT-COLLISION — the member has two rows for one unit, date, EFA block and service with the same clearing price but different cleared volumes; which row is the result, or are both legitimate? (unit v0.22-K-AS-5c; the registry reason names the unit and the two volumes, which this page leaves out because the family is a held output)

**Held means unpublished.** Hold class E-SEM: a vendor identifier, unit or semantics question for the output
is unresolved. Silver exists and reconciles, but no gold, chart, front-end page or model input may use the
held families, and this page deliberately states no values for them. Units: v0.22-K-AS-5a for the
master block orders and the summary, AS-5 for the summary archive, v0.22-K-AS-5c for the three new archives
and the held by-unit member.

**What would release the outputs.**

- *PHASE2-MASTER-ORDER-ID* needs NESO to republish the three BlockOrders masters with full order, order-period
  and trade identifiers (or document an alternative stable identity).
- *PHASE2-SUMMARY-PRICE-UNIT* needs NESO to confirm the rate dimension of the summary Clearing Price (per MW
  per hour, or per MW) and to correct the conflicting dictionaries.
- The archive hold needs a vendor definition of the archive `Date` and EFA labels
  (ARCHIVE-DATE-CONVENTION).
- *PHASE2-ARCHIVE-SEMANTICS* (the three AS-5c archives) needs a NESO data dictionary for the 2019-11 to
  2020-01 archive members: the price unit and hour basis, the export clock of the naive times, and whether the
  archive `Date` is the EFA date of the later masters. The current tables' dictionaries are not transferred.
- *PHASE2-ARCHIVE-BYUNIT-COLLISION* needs NESO to say which of the two conflicting rows is the result, or that
  both are legitimate (and, if both, what distinguishes them in the key).

**Open questions that do not hold any output** (carried as `TODO: verify`):

- **PHASE2-EXPORT-CLOCK**: the clock of every naive delivery start/end and order-entry string, in each export
  epoch.
- **PHASE2-PRICE-DICTIONARY-CORRECTION**: whether the order prices and the linear curve prices are per MW per
  hour (the trial documents say hourly; the newest dictionaries say £/MW).
- **PHASE2-EFA-DATE-ROLE**: whether `EFA Date` is the delivery date or the delivery end date.
- **LINEAR-NA-SEMANTICS**: the meaning of the literal `NA` in the linear curve points.
- **MAR meaning and scale**: undocumented beyond "automatically infilled".
- The original publication instant of every row, the amendment and deletion behaviour between captures, and
  the identity of orders and results across any corrected re-export (`_latest` is `whole_capture` for the
  orders and `key_latest` for the results).

**The ZIP archives (AS-5c, 2026-10-14).** The BlockOrders, LinearOrders and ResultByUnit ZIPs, which AS-5a left
as HOLD containers with no record, now have records and silver (1,042, 588 and 436 rows) and are held outputs
(E-SEM). They add earlier auctions (2019-11-22 to 2020-01-03) that are not in the masters. The 2019-11-22
by-unit member is held back from silver. Nothing about their values is published here.

## Known issues and gotchas

- **Do not add the weekly and master order exports, and do not union them.** They overlap in coverage with
  differences in identifier fidelity and spelling. Use one family at a time.
- **Result tables: read `_latest`, not the base table, for a business view.** The base tables hold the weekly
  rows and the master rows; for 201 by-unit keys and 84 summary keys the same business key occurs twice.
- **EFA is a weekly block ordinal 1 to 42**, not a settlement period (1..50) and not a clock time. The six
  daily blocks are 4 hours each. Never compose it with a date.
- **The result `event_time` is a date anchor, not an EFA block start**; all blocks of a date share it.
- **`timestamp_utc` is the capture time for the four order tables**, not a delivery or bid time.
- **All delivery, delivery-end and order-entry strings are naive with an undocumented export clock**
  (PHASE2-EXPORT-CLOCK). The weekly and master files spell them differently, and the 2019-2020 linear
  master uses the ISO-like spelling the weekly files use.
- **Master order identifiers are collapsed** to scientific notation in all three block-order masters. Do not
  attempt to rebuild an order identity from them (held).
- **Order prices are published as £/MW but the trial documents describe hourly prices**; the by-unit prices
  are explicitly £/MW/h. Do not compare an order price with a clearing price without resolving the unit.
- **Literal `NA` strings are values**: `block_code_prm` (block), `p3`..`v4` (linear). They are not nulls and
  not zeros. Blank string cells are null.
- **Block volumes are negative by design** (sell-order convention). Do not take absolute values.
- **Dictionary quirks.** The vendor describes OrderID as an integer; `EFA Date` is a delivery date in one dictionary and the delivery end date in another; "Member of the
  trial" text and the DLH / LFS service names appear in every dictionary. The unit cells in the master summary
  dictionary are type words.
- **The four archives are held and separate.** Never add an archive to the weekly or master tables of the same
  kind; they cover earlier auctions and have no dictionary. The archive `date` is a date anchor, not an EFA
  block start.
- **A ZIP can be SILVER and still carry a HOLD member.** The by-unit archive ZIP is SILVER but its 2019-11-22
  member is read by no record (521 rows remain in bronze only).
- **Memory.** All bodies are small (the largest is 8.9 MB); the AS-5a batch activation peaked at 684.6 MiB and
  the AS-5c one at 586.5 MiB.

## Implementation delta

Where the code or a source differs from the docs or from another source:

- **Event time is the capture time** for the order tables by design (recipe `none`): the code does not
  interpret the vendor's naive time cells. The result tables use the date anchor (`date_sp1`) rather than a
  composed block start.
- **Linear curve column names.** Vendor `1P`..`4V` become `p1`..`v4` in silver (a silver name must begin with
  a letter); the vendor name is preserved in the "Vendor column" of the schema above.
- **`mar` is a string.** The dictionary says only "Automatically infilled, please leave blank"; silver keeps
  the raw cell (it is not the numeric ratio used for the later Dynamic Containment block table, whose meaning
  is documented).
- **Weekly resources are siblings.** The weekly by-unit and summary resources are dispositioned to the master
  family's silver key, not to a family of their own, so their registry family (`results_unit`,
  `results_sum`) shows "ingest-only: no silver yet" while their rows are in the master tables.
- **`published_at`.** For all families it is the CKAN `last_modified` of the captured upload (ADR-030), never
  the vendor's auction or publication time.
- **Package eligibility** is `eligible` in the registry while six families are held (the master block orders,
  the summary and the four archives) and one archive member is held; the family records carry the holds (eligibility report `docs/neso_data_portal/eligibility.md`).
- **Dictionary versus body.** The dictionary calls `OrderID` an integer, `Date` a delivery date and the
  summary `Clearing Price` £/MW or "number"; the bodies are strings and numbers served as in the CSVs, with
  the conflicts carried as holds or TODOs above, not repaired.

- **Archive records read the ZIP members, not a table-per-file.** The four archive families are `zip_member`
  records over their ZIP containers; each carries `child_id` and `child_crc32` columns naming the member a row
  came from. A container can be SILVER while one child is HOLD (the 2019-11-22 by-unit member).
- **Linear archive epochs.** Three header shapes (12, 14 and 16 price/volume points) in one family; the silver
  table is the typed-null union (56 columns including bookkeeping), the engine's existing multi-epoch
  behaviour.

## Activation receipt

AS-5a merged as PR #118 (`ee5c903`), triple-green (RULINGS 778). Activation on 2026-10-13 with
`--start/--end 2026-10-08` and no prior silver (`phases/v0.22-K-AS-5a/post-merge/transform.log`): the six
phase-2 records wrote **379 + 85,662 + 84 + 8,232 + 69,207 + 8,736 = 172,300** rows, each equal to the spec
plan, in a seven-record batch of 177,757 rows (the seventh, the FFR post-tender CSV record, is documented on
its own page), with 0 recorded failures and a peak working set of 684.6 MiB (RULINGS 780;
`.planning/v0.22-RESULTS.md` section "AS-5a"). Of the phase-2 rows, 77,902 are in eligible families and
94,398 in the two held families.

Reconcile `--all --cutoff 2026-10-13` exited 1 over 213 families with 3 gaps. **None of the 3 gaps is in a
phase-2 family**: all are `overlap` gaps on the FFR post-tender family `ffr_post_tender_reports_csv_ext`
(one tender, 162.198, republished identically in three monthly resources). Their ADR-040 adjudication is
**pending AS-5b**, not resolved (RULINGS 780). The phase-2 families have no gap at this cutoff.

**AS-5c (2026-10-14).** AS-5c merged as PR #120 (`59d41c9`), triple-green (RULINGS 796). Activation on
2026-10-14 with `--start/--end 2026-10-08` and no prior silver for the new families
(`phases/v0.22-K-AS-5c/post-merge/transform.log`) wrote four families, **12,160 rows = plan**: the three
phase-2 archive families **1,042 + 588 + 436 = 2,066** rows (here) and the FFR post-tender workbook family
10,094 rows (documented on its own page), with 0 recorded failures and a peak working set of 586.5 MiB
(RULINGS 798; `.planning/v0.22-RESULTS.md` section "AS-5c"). The summary archive stays at 168 rows. No resource
or child of the phase-2 package keeps the earlier "records pending in AS-5" container reason.

Reconcile `--all --cutoff 2026-10-13` exited 1 over 222 families with 4 gaps, all `overlap` gaps on the FFR
workbook family (TR127 and TR136, two editions each; see the FFR post-tender page). **None of the 4 gaps is in
a phase-2 family.** The coverage check was clean (captured 1,385, missing 0, unregistered 0, unfrozen 0,
orphans 0).

## Links

- Neighbouring FFR pages: @./firm-frequency-response-post-tender-reports.md, @./static-firm-frequency-response-auction-results.md, @./static-firm-frequency-response-requirement.md
- Successor-era auction results (a different measure and platform): @./dynamic-containment-data.md, @./eac-auction-results.md
- Vendor index: @../README.md, @../coverage.md
- Package page: [NESO Data Portal, Phase 2: FFR Auction Results Summary](https://www.neso.energy/data-portal/phase-2-ffr-auction-results-summary)
- Trial evaluation: [NESO document 176721](https://www.neso.energy/document/176721/download)
- GB balancing context: @../../../20-domain/markets/gb-balancing-mechanism.md
- Evidence in the gridflow repo: `.planning/phases/v0.22-K-AS-5/K-AS-5-FACTS.md` (phase-2 package, g1-g6),
  `K-AS-5a-SPEC.md`, `K-AS-5c-SPEC.md`, `.planning/phases/v0.22-K-AS-5c/PLAN.md`,
  `.planning/RULINGS.md` (765, 766, 773, 778, 780, 796, 798), `.planning/v0.22-RESULTS.md` ("AS-5a", "AS-5c")
