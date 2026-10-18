---
source: "neso_data_portal"
package: "contract-transfer-of-obligation"
dataset_key: "contract_transfer_obligation"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-13
layer_coverage: "bronze"
eligibility: "eligible"
page:
  held: Identical rows repeat and no transfer id tells them apart, so there is no silver table.
  title: Contract transfer of obligation
  summary: >-
    NESO's log of balancing-service contracts that providers asked to move from one unit to another:
    product, MW, price and delivery dates.
  facts:
    vendor: "NESO Data Portal, package `contract-transfer-of-obligation`: one CSV file"
    cadence: Ad hoc, as NESO lists it; updated only when a transfer request arrives
    grain: "Each row: a contract's product, MW, price, delivery dates and receiving unit"
  landscape: market
  what_it_is: >-
    A provider can ask NESO to move a Balancing Service contract from its contracted unit to one
    without a contract. This file publishes those transfers: participant, product, executed MW,
    clearing price in £/MW/h, delivery dates, the receiving unit and a status. NESO does not say
    whether rows that repeat exactly are separate transfers, nor what clock the delivery dates use.
  how_used:
    - Which unit took over each transferred contract, with its MW and price
    - Read beside the Enduring Auction Capability (EAC) results that NESO tags this package with
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then the file downloaded whole unless its
      `last_modified` is unchanged. Ingest only: gridflow builds no silver table.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=contract-transfer-of-obligation"
      - "GET https://api.neso.energy/dataset/cb295f83-bfb8-4aa0-9b92-0a6791342c7e/resource/dbd7f746-07c9-4804-8ab2-9bec2d7ef0ec/download/contract-transfers.csv"
    commands:
      - {run: gridflow ingest neso_data_portal contract_transfer_obligation --last 24h, comment: "whole file, bronze only"}
  related:
    - {dataset: neso_data_portal/eac-br-auction-results, note: "Balancing Reserve auction results, among the tags NESO gives this log"}
    - {dataset: neso_data_portal/eac-auction-results, note: "EAC response and reserve auction results, also among its tags"}
    - {dataset: neso_data_portal/balancing-reserve-auction-requirement-forecast, note: The Balancing Reserve requirement forecast}
---

# Contract Transfer of Obligation

A log of **balancing-service contract transfers**. A market provider can ask NESO to transfer a
Balancing Service contract from a contracted unit to a non-contracted unit (the vendor's
wording). All 12 captured rows are Balancing Reserve (`serviceType` PBR, `auctionProduct`
BALANCING RESERVE); the vendor note names no specific product. NESO publishes the
contract details for those transfer requests: the participant, the auction product, the
executed quantity and clearing price, the delivery period, the unit that receives the obligation
and the status. The vendor describes it as the published contract information for units,
covering accepted and cancelled transfer requests, for both the transferrer and the transferee.
The vendor says it is updated **only when a transfer request is received**, so it is ad hoc and
event-driven, not on a schedule. The tags tie it to the BR auction results on the Enduring
Auction Capability (EAC). Per the vendor dictionary, `executedQuantity` is the volume of
response accepted at the clearing price. Reading it as BR volume that moved between units is
interpretation: the file does not name the originating unit (`auctionUnit` is blank), and the
repeated rows are unresolved (see Identity). It is a side channel to the auction results in
@./balancing-reserve-auction-requirement-forecast.md and @./balancing-services-contract-enactment.md,
not a settlement or price series.

**Read this first.** This family is **captured in bronze but not loaded to silver**. It has
**no registry record**, so no transformer runs. There are no silver rows, no silver views and
no `_latest` view. The reason is RULINGS 538 (the same ruling as `demand_profile_dates`): the
captured file repeats identical rows (12 rows, 7 distinct), the file has no transfer
identifier, and no column set from the source can tell the repeats apart. The engine's
duplicate-key guard would reject every capture, and gridflow forbids silent deduplication or an
invented row ordinal. The AS-2 batch (RULINGS 727) therefore left it ingest-only. The
activation receipt (RULINGS 731, `v0.22-RESULTS` section AS-2) confirms the same: no record,
no silver rows.

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: EVT

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Contract Transfer of Obligation 2025-2026 | CSV | upload | `dbd7f746-07c9-4804-8ab2-9bec2d7ef0ec` |

The package has one resource. It has no DOC, GIS, COVERED or other ingest-only files.

| Resource | Disposition | Download |
|---|---|---|
| Contract Transfer of Obligation 2025-2026 (CSV, `datastore_active: true`) | SILVER → `contract_transfer_obligation` (**not realised**: no record, `transformer: null`) | [contract-transfers.csv](https://api.neso.energy/dataset/cb295f83-bfb8-4aa0-9b92-0a6791342c7e/resource/dbd7f746-07c9-4804-8ab2-9bec2d7ef0ec/download/contract-transfers.csv) |

- Package id `cb295f83-bfb8-4aa0-9b92-0a6791342c7e`; created 2024-04-18; licence ESO / NESO
  Open Data Licence. The catalogue snapshot `20261006T195819Z` lists no author or version. Its
  tags are BR Auction Results on EAC, Contract Transfers, EAC-BR Auction Results, Reserve
  Auction Results on EAC, Response Auction Results and Subscribable.
- Vendor dataset page: <https://www.neso.energy/data-portal/contract-transfer-of-obligation>.
- The resource name says "2025-2026", but the captured body holds delivery dates that start in
  April 2026 and run to August 2026. TODO: verify with NESO whether the resource is a
  financial-year file that gets replaced by a new resource each year, or one file that is
  appended to. Only one capture exists, so gridflow cannot tell.
- **Implementation delta, reconciled.** The registry JSON gives the package `eligibility:
  eligible` and the resource a `SILVER` disposition. The eligibility report
  (`docs/neso_data_portal/eligibility.md`) lists the family as "ingest-only (no silver
  output)". The code has no record (pinned by
  `tests/unit/test_neso_as2_records.py::test_contract_transfer_obligation_has_no_record`).
  The three agree once you read RULINGS 538: the licence and format make the package eligible,
  the `SILVER` disposition shows the intended target, and the duplicate rows alone keep a
  record from being written.

## Families

### `contract_transfer_obligation`

- Kind: tabular · archetype: EVT · refresh: adhoc · empty allowed: no
- ingest-only: no silver yet

Bronze schema, one header epoch (exact header H-CT; all cells are text in bronze):

| Vendor column | Vendor dictionary meaning | Vendor unit |
|---|---|---|
| `registeredAuctionParticipant` | Name of the participant who submitted the bid | N/A |
| `auctionUnit` | Unit identifier: one or more eligible assets registered as an auction unit | N/A |
| `serviceType` | Service identifier, "Balancing Reserve" | N/A |
| `auctionProduct` | Service type identifier, "NBR, PBR" | N/A |
| `executedQuantity` | Volume of response accepted at the clearing price | MW |
| `clearingPrice` | Cleared price per MW per hour | £/MW/h |
| `deliveryStart` | Time from which delivery of the auction product commences | ISO 8601 (dictionary) |
| `deliveryEnd` | Time from which delivery of the auction product ends | ISO 8601 (dictionary) |
| `Transfer To Unit` | Name of the unit that receives the contract obligation | N/A |
| `Transfer Status` | Status of the transfer, "accepted, rejected, or cancelled" | N/A |

No silver column names exist, because there is no record. Units come only from the vendor
dictionary, as cited in the FACTS research (FACTS g4): MW for `executedQuantity` and £/MW/h for
`clearingPrice`. No unit was inferred from a column name. There is no `Season`-style code
column or numeric identifier column.

#### What the captured file shows against the dictionary

These are observations from the one capture (FACTS section 4.7). They are not corrections.
Bronze keeps the file as published.

- **Placement is swapped.** The dictionary describes `serviceType` as the service
  ("Balancing Reserve") and `auctionProduct` as the product ("NBR, PBR"). In the body,
  `serviceType` holds `PBR` and `auctionProduct` holds `BALANCING RESERVE`. gridflow keeps the
  actual headers and values and does not swap them. TODO: verify with NESO which labelling is
  correct.
- **`auctionUnit` is blank in all 12 rows**, although the dictionary marks it MANDATORY. The
  only unit identifier that is populated is `Transfer To Unit`, the receiving unit. So the file
  does not say which unit the obligation came from.
- **`Transfer Status`** is `Complete` in the capture. The dictionary example is "Accepted", and
  its description lists accepted, rejected and cancelled. TODO: verify the full status
  vocabulary with NESO. The capture cannot show whether cancelled or rejected transfers ever
  appear.
- **Delivery labels are date-only.** `deliveryStart` and `deliveryEnd` hold `dd/mm/yyyy`
  strings with no time of day. The dictionary types them as datetimes and gives ISO 8601
  examples. Values such as `26/08/2026` and `29/04/2026` show the order is day-first. Start and
  end are often the same date. See the period TODO below.
- **A receiving-unit value carries a trailing U+00A0** (no-break space). Unit IDs are stored
  as-is, so the value is preserved. Normalising it would merge two distinct source spellings.
- **Numbers are clean.** `executedQuantity` and `clearingPrice` parse as numbers with no trim
  and no token repairs.

#### The two clocks (proposed, not applied)

No record exists, so neither clock is stamped on any row.

- **Vintage clock (`ckan_last_modified`).** `available_at` = `published_at` = the CKAN
  `last_modified` of the resource at the moment gridflow captured it (ADR-030). The resource is
  an `upload`. The activation capture's sidecar records
  `ckan_last_modified = 2026-10-05T09:45:24.439961`, read as UTC. That is when NESO last
  replaced the file. It is not the time any single transfer was requested or accepted, and the
  body has no request-time column. The vendor gives no revision guarantee, so no immutable
  issue time can be read from the file.
- **Event clock (`temporal: none`).** In plain terms, there is no event-time recipe:
  `timestamp_utc` would be the **capture time**, not any date in the row. The proposal keeps the
  delivery labels as raw strings, because their date-only meaning is unsettled (FACTS T03). No
  UTC instant is built. TODO: verify the timezone, the omitted time of day and the end-date
  inclusivity of `deliveryStart` and `deliveryEnd`. This is the CONTRACT-TRANSFER-PERIOD
  question.

#### Sentinels and missing values

The research census (FACTS g5) found no `-1`, `NA` or `N/A` tokens, no thousands separators
and no percent signs in this body. The only blank column is `auctionUnit` (12 of 12 rows). It
is ordinary missing data. Do not read it as zero or as a sentinel, and do not fill it from
another column.

#### Identity and the blocker

Measured in the one capture (FACTS C04, C05):

| Property | Value |
|---|---:|
| Rows | 12 |
| Distinct complete rows | 7 |
| Duplicate excess rows | 5 |
| Rows inside duplicate groups | 7 |

- **Two groups repeat.** In the capture, one Statkraft contract (BALANCING RESERVE, quantity
  and price both 13, delivery label `24/08/2026`, receiving unit `AG-DSTK01`) appears three
  times. The same contract to receiving unit `AG-ESTK01` appears four times. The group agrees
  in every source field. A fifth `AG-ESTK01` spelling with a trailing U+00A0 is distinct and
  is not in the group.
- **Every source column together still fails.** The key made of all ten columns has 5
  duplicate excess rows. There is no transfer id, order id, source-row sequence or request
  timestamp, so no broader composite can be lossless.
- **The `whole_capture` `_latest` mode does not bypass the duplicate-key guard**
  (`DuplicateEntityKeyError`, raised at `src/gridflow/silver/neso_data_portal/casting.py:531-534`,
  as recorded for `demand_profile_dates`).
- The CKAN `datastore_search` total on 2026-10-08 was 12, equal to the CSV row count. The
  datastore `_id` is not in the uploaded body, so it cannot supply an entity key. TODO: verify
  whether the datastore holds the same repeated rows as the CSV, and whether `_id` is stable
  across updates.
- Dropping the repeats in silence, or adding a row ordinal, is forbidden (RULINGS 538). No
  failed-key entry is proposed as a substitute for a valid family key.
- **TODO: CONTRACT-TRANSFER-IDENTITY.** Does NESO have a transfer identifier, or any revision of
  the file that carries distinguishing columns? Are the repeated rows genuinely separate
  transfers of the same size, or a publishing defect? What settles it: a vendor transfer
  identifier, a source revision that carries distinguishing columns, or an explicitly approved
  engine mechanism for exact-duplicate rows. A broader composite of the existing columns cannot
  settle it.
- **TODO: CONTRACT-TRANSFER-PERIOD.** What clock, boundary and inclusivity do the date-only
  `deliveryStart` and `deliveryEnd` labels use? What settles it: resource-specific guidance on
  date-only delivery boundaries.

#### Bronze at activation

| Property | Value |
|---|---|
| Captures | 1 (the only local capture of this resource) |
| File | `C:/gridflow-data/bronze/neso_data_portal/contract_transfer_obligation/2026/10/08/raw_20261008T091555Z_dbd7f746-07c9-4804-8ab2-9bec2d7ef0ec_39631781.csv` |
| Bytes · rows | 1,289 · 12 |
| Written | 2026-10-08T09:15:55Z; sidecar SHA-256 `39631781ea5e60ca64e9636d2b882870d47a195d75b035a6c5f412287bacb62c` verified (FACTS section 2) |
| Encoding | UTF-8 with BOM, CRLF line ends; strict UTF-8 decode passed |
| Silver | **none.** No silver directory and no row count for this family. The AS-2 transform covered the other 11 families |
| Reconcile | `--all --cutoff 2026-10-12`: exit 0, 170 families, 0 gaps, 47 adjudicated, 0 stale. This family stays ingest-only (`v0.22-RESULTS` section AS-2) |

The reader is faithful. A strict Python CSV parse and a Polars parse of the original text agree
on every ordered cell, so encoding and parsing are not the blocker. Identity is.

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc

The vendor updates the file only when a transfer request is received. No cadence is
documented, and only one capture exists. TODO: verify whether an update rewrites the whole file
or only appends rows, and whether an existing row can be amended or removed. Settling this needs
repeated captures of the same resource.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: <https://www.neso.energy/data-portal/ngeso-open-licence>. Any derived output must
carry the attribution line above verbatim.

## Holds

- none

There is no held silver output because there is **no silver output at all**. The family is
blocked structurally (class 3, RULINGS 538) by the identical-row repeats described under
Identity. It is not an E-SEM semantics hold. The two TODOs above are the open questions, and
neither is a hold question on a published output. Until the identity question is settled, the
data exists only as immutable bronze captures.

## References

- @../README.md: NESO Data Portal vendor page (CKAN, file-download model)
- @./balancing-reserve-auction-requirement-forecast.md · @./balancing-services-contract-enactment.md: the BR requirement forecast and the contract-enactment records this log sits beside
- @./demand-profile-dates.md: the other ingest-only family (same RULINGS 538 blocker)
- gridflow `docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md` (vintage clock), `ADR-034-neso-generic-silver-engine.md` (generic engine, `_latest`), `ADR-036-neso-profiler-and-pilot-records.md` (`temporal: none`)
- gridflow `.planning/phases/v0.22-K-AS-2/K-AS-2-FACTS.md` section 4.7 and section AS-2-d; `K-AS-2-SPEC.md` item 7
- gridflow `.planning/v0.22-RESULTS.md` section AS-2; RULINGS 538, 724, 727, 730, 731
- gridflow registry `src/gridflow/connectors/neso_data_portal/registry/contract-transfer-of-obligation.json`; eligibility report `docs/neso_data_portal/eligibility.md`
- gridflow `tests/unit/test_neso_as2_records.py` (no-record pin)
