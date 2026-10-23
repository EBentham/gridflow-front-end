---
source: "neso_data_portal"
package: "balancing-services-adjustment-data-forward-contracts"
dataset_key: "bsad_forward_contracts"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-13
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Forward contract balancing adjustments
  summary: >-
    NESO's balancing adjustments from forward contracts outside the Balancing Mechanism, per
    settlement period: buy and sell costs in £, volumes in MWh.
  facts:
    vendor: "NESO Data Portal, package `balancing-services-adjustment-data-forward-contracts`: one CSV file per financial year"
    cadence: Updated twice daily, as NESO's package text states
    grain: One row per settlement period and capture; the latest view keeps one
    history: "NESO lists yearly files from 2016-17; gridflow loads 2017-18 on, except 2020-21"
  landscape: market
  what_it_is: >-
    BSAD is how NESO submits balancing actions outside the Balancing Mechanism to the BSC, which
    governs imbalance settlement (NESO). Each row is a settlement-period total, not a contract: net
    buy and sell price adjustments, cost (£) and volume (MWh), and gross volumes traded. NESO's
    current-year file can show its newest days as zero and fill them in a later upload.
  how_used:
    - Daily buy and sell cost adjustments, beside imbalance prices, for balancing cost studies.
    - Which settlement periods carry the forward buying and selling.
    - "Setting NESO's terms beside Elexon's NETBSAD, whose terms carry similar names."
  chart:
    type: line
    silver: neso_data_portal/bsad_forward_contracts
    time: settlement_date
    values:
      - {column: bca, series: buy}
      - {column: sca, series: sell}
    dedup: {"on": [settlement_date, settlement_period], order_by: available_at}
    aggregation: sum
    window: {start: "2017-04-01", end: "2026-09-30"}
    max_points: 4000
    unit: £
  chart_view:
    title: Buy and sell cost adjustments, daily total, 2017 to 2026
    caption: >-
      Silver `neso_data_portal/bsad_forward_contracts`, `bca` and `sca` in £: each settlement day's
      sum, 1 April 2017 to 30 September 2026, newest capture per file. No data April 2020 to March
      2021; the 2016-17 and 2020-21 files fail to load.
    alt: >-
      Line chart of daily total buy and sell cost adjustments from
      neso_data_portal/bsad_forward_contracts, in £, for settlement days 1 April 2017 to 30
      September 2026. Both lines stay under £1.6M a day to March 2020. No line April 2020 to March
      2021: that file fails to load. The buy line then rises, peaking at £24.0M on 11 August 2022,
      with 11 days over £10M that year and two since, the higher £14.8M on 21 November 2025. The
      sell line peaks at £2.64M on 29 May 2023.
    x_label: settlement date; no file loads for 2020-21
    y_min: -500000
    key:
      - {series: buy, label: Buy cost adjustment, codes: BCA, paint: petrol, note: "Peak £24.0M on 11 August 2022; 13 days above £10M, 11 of them in 2022."}
      - {series: sell, label: Sell cost adjustment, codes: SCA, paint: clay, note: "Never above £2.7M a day here; peak £2.64M on 29 May 2023."}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then each yearly file whole. An upload is
      skipped if `last_modified` is unchanged; a dump is kept only if its body changed.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=balancing-services-adjustment-data-forward-contracts"
      - "GET https://api.neso.energy/dataset/ca51d03a-53e8-4397-aee1-2f40f9973b96/resource/16fe508d-27da-4282-b8af-1fa519b6f480/download/bs_forwardcontract_01-04-2017_31-03-2018.csv"
      - "GET https://api.neso.energy/datastore/dump/449c73a6-a7fd-4166-91f0-3dd1a0e0bb14"
    commands:
      - {run: gridflow ingest neso_data_portal bsad_forward_contracts --last 24h, comment: "whole files; window must end recently"}
      - {run: gridflow transform neso_data_portal bsad_forward_contracts --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: settlement_date, op: eq, value: "2025-11-20"}
        - {column: settlement_period, op: ge, value: 31}
        - {column: settlement_period, op: le, value: 38}
      order_by: [settlement_period]
      columns: [settlement_date, settlement_period, bca, bva, bsa, sca, sva, ssa, resource_id, timestamp_utc]
    key: [resource_id, settlement_date, settlement_period]
    caption: "2025-11-20, periods 31 to 38: hourly `bca` and `bva` blocks; `ssa` -0.001 until period 38."
    fields:
      settlement_date: GB settlement date, as NESO labels it, on the UK local clock (NESO)
      settlement_period: Half-hour of the settlement day, 1 to 48; 46 or 50 on clock-change days
      bca: "Net buy price cost adjustment, £ (NESO); NESO does not state its sign"
      bva: "Net buy price volume adjustment, MWh (NESO); NESO does not state its sign"
      bsa: Gross volume purchased (trades), MWh (NESO)
      sca: "Net sell price cost adjustment, £ (NESO); NESO does not state its sign"
      sva: "Net sell price volume adjustment, MWh (NESO); NESO does not state its sign"
      ssa: "Gross volume sold (trades), MWh (NESO); NESO does not explain negatives like these"
      resource_id: CKAN id of the financial-year file the row came from
      timestamp_utc: Start of the settlement period, UTC, computed from date and period
      published_at: "Null: gridflow takes no vendor publication time for this table"
      bronze_capture_id: Path of the bronze capture the row was read from
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      Returns a pandas DataFrame from the DuckDB view
      `silver_neso_data_portal_bsad_forward_contracts_latest`, every row of each file's newest
      capture, filtered on `settlement_date` with both ends included; lineage columns dropped.
    cells:
      - |
        df = data.neso_data_portal.query("bsad_forward_contracts", "2017-04-01", "2026-09-30")
        df = df.sort_values("timestamp_utc")
      - df.loc[df.bca > 1_000_000, ["settlement_date", "settlement_period", "bca", "bva", "sca", "sva"]].tail()
      - |
        s = df.settlement_date.astype("datetime64[ns]")
        fy = (s.dt.year - (s.dt.month < 4)).rename("year_from_april")
        df.groupby(fy)[["bva", "sva", "bca", "sca"]].sum().round(0).reset_index()
      - |
        day = df[df.settlement_period <= 48]
        day.groupby("settlement_period")[["bva", "sva"]].mean().plot.bar(
            ylabel="mean MWh per period", color=["#155A6E", "#C77E3C"], figsize=(8, 3.5));
    needs: "a capture of NESO's yearly files from 2017-18 except 2020-21"
    plot_alt: >-
      Bar plot of mean `bva` and `sva` per settlement period, periods 1 to 48, 1 April 2017 to 30
      September 2026. Selling leads overnight, 140.9 MWh at periods 9 and 10. Buying peaks at
      92.4 MWh at periods 15 and 16, then 83.6 MWh at periods 37 and 38, while selling stays under
      2 MWh from periods 37 to 40.
  related:
    - {dataset: neso_data_portal/aggregated-bsad, note: "NESO's per-period net adjustments, a separate BSAD file set"}
    - {dataset: neso_data_portal/disaggregated-bsad, note: "NESO's per-action BSAD files; their rows are not shown"}
    - {dataset: elexon/netbsad, note: "Elexon's per-period adjustment terms, with names like these"}
    - {dataset: elexon/system_prices, note: "Imbalance prices, settled under the BSC that BSAD is submitted to"}
---

# Balancing Services Adjustment Data (BSAD) Forward Contracts

This package is NESO's half-hourly record of **forward-contract balancing adjustments**, one row per
GB settlement period. Balancing Services Adjustment Data (BSAD) is how NESO reports to the Balancing and
Settlement Code (BSC) the balancing actions it takes **outside the Balancing Mechanism**; the vendor's
package text says it covers those off-mechanism actions and links the BSAD methodology statement
(CKAN package `notes`, @.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json;
[BSAD methodology](https://www.neso.energy/document/110891/download)). The catalogue also describes the
package as updated twice daily; the registry refresh is daily (see Cadence).

**Despite the name, this is not a contract list.** No column of any captured header identifies a
contract, action, trade or party. Every row is a **settlement-period aggregate** of six adjustment
variables as the vendor defines them (K-AS-4 FACTS section 4: "aggregated forward-contract adjustment
variables"): BCA, BSA and BVA on the buy side and SCA, SSA and SVA on the sell side (vendor meanings in the
Units table below). It is not an individual-trade record. `TODO: verify` whether and how these variables
feed the imbalance price or the priced balancing cost and volume; the reviewed vendor text does not say, and
the direction of each adjustment is unresolved (see FORWARD-BSAD-SIGN-CONVENTION under Known issues).

**What this package is not.**

- It is **event data, not a forecast**: `issue: none`, no forecast exemption applies, and there is **no
  `run_type`** and no settlement-run or revision column (the registry therefore never deduplicates on
  `(date, period)`; identity is `resource_id` + date + period).
- It is **not the aggregated BSAD** (a different table with different columns, see
  @./aggregated-bsad.md) and **not the disaggregated BSAD** (action-level rows, see
  @./disaggregated-bsad.md, ingest-only). Do not add or join these tables on date and period without
  reading each page.
- It is **not delivered in one table**: the vendor publishes one resource per financial year (April to
  March), 11 resources from 2016-17 to 2026-27, and gridflow keeps them as one family partitioned by
  resource.

See @../../../20-domain/concepts/settlement-period.md and
@../../../20-domain/markets/imbalance-price.md for the market context.

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: EVT

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| BSAD Forward Contracts 2016-17 | CSV | upload | `30ba12a9-9a9e-4dbb-a69e-ad256d274b04` |
| BSAD Forward Contracts 2017-18 | CSV | upload | `16fe508d-27da-4282-b8af-1fa519b6f480` |
| BSAD Forward Contracts 2018-19 | CSV | upload | `0e7f8536-b449-4f04-a5f5-d08e8121c8c4` |
| BSAD Forward Contracts 2019-20 | CSV | upload | `7ce8164f-0f0c-4940-b821-ca232e2eefaf` |
| BSAD Forward Contracts 2020-21 | CSV | upload | `5d0f2119-1ba6-4d7d-8db5-ea4e23720aa9` |
| BSAD Forward Contracts 2021-22 | CSV | dump | `c435e464-f4d5-4ec2-b8f5-693416e22baa` |
| BSAD Forward Contracts 2022-23 | CSV | dump | `38f74f2c-f735-46fb-8e26-32545011a310` |
| BSAD Forward Contracts 2023-24 | CSV | dump | `56e8e727-3ef9-4b0a-bd06-756cbf5df2fc` |
| BSAD Forward Contracts 2024-25 | CSV | dump | `93f9bdde-1fd9-4619-99e2-d1c5e38239e1` |
| BSAD Forward Contracts 2025-26 | CSV | dump | `9382cd2a-656d-4a0a-a82e-eb26cd8bf7f7` |
| BSAD Forward Contracts 2026-27 | CSV | dump | `449c73a6-a7fd-4166-91f0-3dd1a0e0bb14` |

All 11 resources are disposition **SILVER** (family `bsad_forward_contracts`). There are **no DOC files**
in this package. The package's own page link is `https://extranet.nationalgrid.com/BSAD/` (CKAN `url`).
Each resource has one bronze capture (2026-10-08), and 2026-27 a second (2026-10-16, below); the table below gives the vendor download location, the
CKAN `last_modified` the catalogue showed on 2026-10-06, the header epoch, and what happened at the
activation transform (@.planning/v0.22-RESULTS.md section AS-4a; RULINGS 759, 760).

| Resource (FY) | Download | CKAN `last_modified` | Header epoch | Silver rows | Outcome |
|---|---|---|---|---:|---|
| 2016-17 | [CSV upload](https://api.neso.energy/dataset/ca51d03a-53e8-4397-aee1-2f40f9973b96/resource/30ba12a9-9a9e-4dbb-a69e-ad256d274b04/download/bs_forwardcontract_01-04-2016_31-03-2017.csv) | 2019-12-13T13:00:26 | 1 | 0 | **failed**: `DuplicateEntityKeyError` (ADR-040 adjudicated) |
| 2017-18 | [CSV upload](https://api.neso.energy/dataset/ca51d03a-53e8-4397-aee1-2f40f9973b96/resource/16fe508d-27da-4282-b8af-1fa519b6f480/download/bs_forwardcontract_01-04-2017_31-03-2018.csv) | 2019-12-13T13:00:03 | 1 | 17,520 | loaded |
| 2018-19 | [CSV upload](https://api.neso.energy/dataset/ca51d03a-53e8-4397-aee1-2f40f9973b96/resource/0e7f8536-b449-4f04-a5f5-d08e8121c8c4/download/bs_forwardcontract_01-04-2018_31-03-2019.csv) | 2019-12-13T12:59:35 | 1 | 17,520 | loaded |
| 2019-20 | [CSV upload](https://api.neso.energy/dataset/ca51d03a-53e8-4397-aee1-2f40f9973b96/resource/7ce8164f-0f0c-4940-b821-ca232e2eefaf/download/bs_forwardcontract_01-04-2019_31-03-2020.csv) | 2020-04-02T19:09:59 | 1 | 17,568 | loaded |
| 2020-21 | [CSV upload](https://api.neso.energy/dataset/ca51d03a-53e8-4397-aee1-2f40f9973b96/resource/5d0f2119-1ba6-4d7d-8db5-ea4e23720aa9/download/data.csv) | 2021-11-25T18:16:36 | 1 | 0 | **failed**: `DuplicateEntityKeyError` (ADR-040 adjudicated) |
| 2021-22 | [datastore dump](https://api.neso.energy/datastore/dump/c435e464-f4d5-4ec2-b8f5-693416e22baa) | 2022-03-31T12:40:18 | 2 | 17,520 | loaded |
| 2022-23 | [datastore dump](https://api.neso.energy/datastore/dump/38f74f2c-f735-46fb-8e26-32545011a310) | 2023-01-23T16:28:36 | 2 | 17,520 | loaded |
| 2023-24 | [datastore dump](https://api.neso.energy/datastore/dump/56e8e727-3ef9-4b0a-bd06-756cbf5df2fc) | none (null) | 2 | 17,568 | loaded |
| 2024-25 | [datastore dump](https://api.neso.energy/datastore/dump/93f9bdde-1fd9-4619-99e2-d1c5e38239e1) | none (null) | 2 | 17,520 | loaded |
| 2025-26 | [datastore dump](https://api.neso.energy/datastore/dump/9382cd2a-656d-4a0a-a82e-eb26cd8bf7f7) | none (null) | 2 | 17,520 | loaded |
| 2026-27 | [datastore dump](https://api.neso.energy/datastore/dump/449c73a6-a7fd-4166-91f0-3dd1a0e0bb14) | none (null) | 2 | 9,168 | loaded (in progress year) |

Total **149,424 silver rows** from 9 resources, 0 validation failures, 0 rows excluded (the reader
counted and removed wholly blank trailing rows in the 2017-18 to 2019-20 uploads, 15 in total; that is a
faithful read of empty rows, not an exclusion). Silver covers settlement days `2017-04-01` to
`2026-10-08` at activation (`2026-10-17` with the later capture below); **the 2016-17 and 2020-21 financial years are absent** because their captures failed
(see Holds).

**Later capture (2026-10-16).** Silver also holds a second capture of the 2026-27 dump
(`available_at` 2026-10-16T19:20:28Z, 9,600 rows, settlement dates 2026-04-01 to 2026-10-17); no other
resource gained a capture. Against the 2026-10-08 capture, its 9,168 shared periods are identical except
**72 periods of 2026-10-06 to 2026-10-08**, which the earlier capture held as all zero and the later one
fills (for example 2026-10-06 period 1: `bca` 0 to 49,207.8, `bva` 0 to 350); 432 periods are new
(2026-10-09 to 2026-10-17), and 2026-10-16 and 2026-10-17 are all zero in it. So the newest days of a
capture can read zero before NESO fills them (observed; `TODO: verify` the cause with NESO).
Silver now holds 159,024 rows across both captures; the latest view (newest capture per resource) holds
149,856 (Polars full join on settlement date and period of the 2026-27 silver files written
2026-10-08 and 2026-10-16, run 2026-10-18).

## Families

### `bsad_forward_contracts`

- Kind: tabular · archetype: EVT · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Date | `settlement_date` | date | `%d/%m/%Y` | no | — | — |
| Settlement Period | `settlement_period` | int64 | — | no | — | — |
| BCA (£) | `bca` | float64 | — | yes | — | — |
| BSA (MWh) | `bsa` | float64 | — | yes | — | — |
| BVA (MWh) | `bva` | float64 | — | yes | — | — |
| SCA (£) | `sca` | float64 | — | yes | — | — |
| SSA (MWh) | `ssa` | float64 | — | yes | — | — |
| SVA (MWh) | `sva` | float64 | — | yes | — | — |

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Date | `settlement_date` | date | `%Y-%m-%d` | no | — | — |
| SettlementPeriod | `settlement_period` | int64 | — | no | — | — |
| BCA | `bca` | float64 | — | yes | — | £ |
| BSA | `bsa` | float64 | — | yes | — | MWh |
| BVA | `bva` | float64 | — | yes | — | MWh |
| SCA | `sca` | float64 | — | yes | — | £ |
| SSA | `ssa` | float64 | — | yes | — | MWh |
| SVA | `sva` | float64 | — | yes | — | MWh |

- Entity key: `resource_id`, `settlement_date`, `settlement_period`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: sp_pair (`settlement_date`, `settlement_period`)

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

**Epochs.** Epoch 1 (the profiler's F-H0) is the uploaded financial years 2016-17 to 2020-21: header
`Date, Settlement Period, BCA (£), BSA (MWh), BVA (MWh), SCA (£), SSA (MWh), SVA (MWh)` with dates as
`dd/mm/yyyy`. Epoch 2 (F-H1) is the datastore years 2021-22 onward: `Date, SettlementPeriod, BCA, BSA,
BVA, SCA, SSA, SVA` with dates as `yyyy-mm-dd`. The epochs differ in column names, not only in transport.
A header outside the two epochs fails loudly. The silver names are harmonised across the epochs and every
value column is `float64` (not the profiler's integer drafts). `settlement_period` is bounded `1..50`.

**The two clocks.**

- **Vintage clock (when gridflow could have known the row).** `ckan_last_modified` is **not** used for
  this family: it mixes upload and datastore resources and the rule (V-8) forbids it for a family holding a
  datastore resource. The record uses `capture_fallback`, so `available_at` is the gridflow capture time
  (sidecar `written_at`): every silver row carries a 2026-10-08 `available_at` (2026-10-16 for the second
  2026-27 capture) and `published_at` is null.
  The CKAN `last_modified` values in the table above are recorded for reference only (four of the
  datastore resources have none). A backtest therefore cannot use this table to say when a past adjustment
  became known; **original submission time is not published** (`TODO: verify` whether NESO or the BSC
  retain it).
- **Event clock (the temporal recipe).** `sp_pair(settlement_date, settlement_period)`: `event_time`
  (equal to `timestamp_utc` in silver) is the **UTC start instant of the GB settlement period**. The
  settlement day is the UK local day, period 1 starts at 00:00 local (the vendor dictionary: "Settlement
  period 1 runs from 00:00-00:30"), and the pair is converted to UTC at the silver boundary. In silver this
  gives, for example, 2023-10-29 period 1 at `2023-10-28T23:00Z` and period 50 at `2023-10-29T23:30Z`.
  Of the non-blank rows, 27 have a period start after their capture time (the open 2026-27 year; 55 in
  the 2026-10-16 capture; all of them zero in every value column), so no forward-only exemption is claimed.

**Settlement periods and daylight saving.** Periods are `1..50`, not `1..48`. Silver holds 8 autumn
days of 50 periods (2017-10-29, 2018-10-28, 2019-10-27, 2021-10-31, 2022-10-30, 2023-10-29, 2024-10-27,
2025-10-26), 8 spring days of 46 (2018-03-25, 2019-03-31, 2020-03-29, 2022-03-27, 2023-03-26, 2024-03-31,
2025-03-30, 2026-03-29), and 48 otherwise; the 2019-20 and 2023-24 years have 17,568 rows (leap years).
The 2020-21 autumn and spring days are absent with the failed 2020-21 capture.

**Units (vendor dictionary only, never inferred from a column name).** From NESO's saved field info
(@.planning/research/neso-snapshots/field-info/20261008T114228Z/bsad_forward_contracts.json, K-AS-4 FACTS
section 4):

| Silver column | Vendor meaning | Unit |
|---|---|---|
| `bca` | Net buy price cost adjustment | £ |
| `bsa` | Gross volume purchased (trades) | MWh |
| `bva` | Net buy price volume adjustment | MWh |
| `sca` | Net sell price cost adjustment | £ |
| `ssa` | Gross volume sold (trades) | MWh |
| `sva` | Net sell price volume adjustment | MWh |

`settlement_period` is an ordinal with no unit. The epoch-1 header suffixes `(£)` / `(MWh)` agree with
the dictionary; the generated epoch-1 schema table shows no unit because the unit is read from the
dictionary, not the header. The dictionary text says the date is "Given in UTC or UTC+1 during British
Summer Time", which is the UK settlement-day convention used above.

**Typing and sentinels (K-AS-4 FACTS g5, g6).** Zeros are real values and stay zero; blank cells would
stay null (none occur in the loaded silver). There is **no sentinel token**: no `NA` / `N/A`, no padded or
separator-bearing number, no percent sign, no embedded quote, comma or newline. Values are kept exactly as
published, **signed**; no bounds, sign flip, abs or netting is applied. One cell is a literal `-1` (see
Known issues). All captured bodies are valid UTF-8.

**Row counts per family in silver:** 149,424 (9 resources; the two failed captures would have added
17,522 and 17,536 populated rows), plus 9,600 from the 2026-10-16 capture of 2026-27; 149,856 in the
latest view.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Status: Live

The vendor text says the package updates twice daily (CKAN `notes`). gridflow holds **one capture per
resource** (all 2026-10-08) except 2026-27, whose 2026-10-16 capture appended 432 periods and filled 72
zero periods of 2026-10-06 to 2026-10-08 (see Later capture); otherwise the real rhythm, whether a financial-year resource is extended in place
each day for the current year (2026-27 had 9,168 rows to 2026-10-08, with 27 period starts after the
capture), and whether earlier years are ever amended or deleted are unmeasured: `TODO: verify` by
comparing later complete captures with the hash-pinned bodies (K-AS-4 FACTS section 2.2). The BSAD
methodology permits corrections and later inclusion of contracts, so earlier rows may be revised.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence). gridflow
outputs derived from this package carry the attribution line "Supported by National Energy SO Open Data".

## Holds

- none

**No output of this package is held**: the family is eligible and its loaded values are published. Two
captures are **adjudicated failures** (ADR-040 `failed`, ruling 748, ratified 749), unloaded and kept with
their failure records; this is not a hold on the family. Reconcile `--all` at cutoff 2026-10-12 was clean
with the 5 captures of AS-4a adjudicated across both BSAD families (RULINGS 760, 198 families, 0 gaps).

| Capture | Cause | Why |
|---|---|---|
| 2016-17 (`30ba12a9-...`, hash prefix `f0aeb0c5`) | `DuplicateEntityKeyError` | repeats 2 settlement periods with identical rows (17,522 populated rows, 17,520 distinct pairs) |
| 2020-21 (`5d0f2119-...`, hash prefix `070a68c3`) | `DuplicateEntityKeyError` | repeats 16 settlement periods with **conflicting values**, no revision label or precedence rule (17,536 rows, 17,520 distinct pairs) |

For 2020-21 the repeated 2020-08-25 period 1 appears once with non-zero buy and sell volumes and once with
every column zero; the same conflict occurs for the next repeated period (K-AS-4 FACTS section 4). gridflow
**never deduplicates, picks the last row, adds value columns to the key or invents an occurrence index**.

Ledger questions (carried verbatim as non-holding `TODO:`s):

- `TODO: verify` which value set is authoritative for the repeated 2020-21 settlement periods (for
  example 25/08/2020 period 1), and what the repeated identical 2016-17 row means.

**Known issues and gotchas.**

- **Two financial years are missing from silver** (2016-17 and 2020-21), above. A consumer of a long
  history must treat 2016-04-01 to 2017-03-31 and 2020-04-01 to 2021-03-31 as not loaded rather than zero.
- **Sign convention unresolved.** `TODO: verify` FORWARD-BSAD-SIGN-CONVENTION: the reviewed sources do not
  settle the sign of every historical aggregate variable or every negative gross-volume correction. The
  split buy and sell columns are not a signed individual-action volume. No nonnegative bound, sign flip or
  netting recipe is applied, and none should be assumed.
- **A literal `-1` in `bsa`.** One cell: 2024-25 resource, 2025-01-08 period 39, `bsa = -1.0`. No vendor
  source defines it as missing. It stays numeric `-1.0`, not null. `TODO: verify` FORWARD-BSA-MINUS-ONE:
  signed correction or sentinel.
- **Blank trailing rows in the 2017-18 to 2019-20 uploads** (five per body, 15 removed);
  they are empty rows, not data.
- **Mixed vintage is capture time, not publication time**: see the two clocks. The 2026-10-08 `available_at`
  applies to all history (2026-10-16 for the second 2026-27 capture).
- **The newest days of a capture can read zero.** The 2026-10-08 capture held 2026-10-06 to 2026-10-08
  as all zero; the 2026-10-16 capture filled 72 of those periods (see Later capture). Treat the last
  days of the open year as provisional.
- **No `run_type`, no revision column.** Never deduplicate on `(date, period)`; the resource partition is
  the only disambiguator, and measured settlement pairs are disjoint across the resources (zero shared
  pairs in the 55 pair comparisons across all 11 resources in FACTS section 4; silver's 149,424 rows held
  149,424 distinct settlement date and period pairs at activation, and the latest view's 149,856 rows
  hold 149,856), so no overlap adjudication is needed. The site chart deduplicates on `(date, period)`
  by `available_at` only because of that disjointness: it keeps the newest capture of each resource.
- **The package name is misleading** (see Overview): no contract, trade or party identifier exists in the
  data.
- **Related but different tables.** The aggregated BSAD (@./aggregated-bsad.md) carries different columns
  and has its own encoding and duplicate-key failures and an unresolved sign question; the disaggregated
  BSAD (@./disaggregated-bsad.md) is ingest-only. The three BSAD tables were activated together in AS-4a
  (the third has no silver record); do not sum or join them without reading their pages.
