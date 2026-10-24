---
source: "neso_data_portal"
package: "index-linked-contract-volume"
dataset_key: "index_linked_contract_volume"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Index Linked Contracted Energy Volume
  summary: >-
    NESO's log of the index-linked contracts it enacted, which it can use to meet voltage needs:
    when, average MW, price and cost.
  facts:
    vendor: "NESO Data Portal, package Index Linked Contracted Energy Volume: four datastore tables, one ZIP"
    cadence: NESO gives no update frequency; gridflow re-checks each table at most weekly
    grain: "Each row: one contract enactment, with its delivery start and end"
    history: "Yearly tables 2021-22 to 2024-25, as NESO names them; older files in a ZIP"
  landscape: market
  what_it_is: >-
    NESO can meet a voltage need with an index-linked contract, normally enacted in the morning
    before the power exchange auction. The generator is paid the agreed strike price, less any
    positive generation spread, and compensated when the spread is negative; the spread comes
    from outturn market indices. An archive ZIP holds older files of volumes by date and settlement
    period.
  how_used:
    - When NESO enacted index-linked contracts, with which assets, and why
    - "Average MW and £/MWh per enactment, beside NESO's voltage requirement and costs"
  chart:
    type: bar
    silver: neso_data_portal/index_linked_contract_volume
    group: resource_id
    group_map:
      "8f694d01-68a5-41b9-9542-dd27c42fdbbf": "2021-22"
      "ff292de9-59aa-45cc-85ce-e21fed09f5ff": "2022-23"
      "dff083d2-666b-4e23-9b46-9edd9298f0d3": "2023-24"
      "9b72a2f5-db92-40ca-aa95-b9f1c56f7373": "2024-25"
    dedup: {"on": [resource_id, id], order_by: capture_written_at}
    aggregation: count
    sort: label
    unit: enactments
  chart_view:
    title: Enactments in each yearly table, 2021-22 to 2024-25
    caption: >-
      Silver `neso_data_portal/index_linked_contract_volume`: rows per financial-year table. Every
      2021-22 row is an enactment of `ROCK-1` with counterparty Coryton Energy Company Ltd, for
      `V_MERSEY` or no stated reason.
      The archive ZIP's older files are not drawn.
    alt: >-
      Horizontal bar chart counting the rows of each yearly table in
      neso_data_portal/index_linked_contract_volume: 12 in 2021-22, 2 in 2022-23, 1 in 2023-24 and
      1 in 2024-25.
    key:
      - {series: count, label: Enactments, paint: petrol}
  caveat: "`Cost` is labelled £/h, but NESO describes it as a total: volume times price times duration."
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then each yearly datastore dump (first and newest
      shown), re-checked at most weekly, and the ZIP unless `last_modified` is unchanged.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=index-linked-contract-volume"
      - "GET https://api.neso.energy/datastore/dump/8f694d01-68a5-41b9-9542-dd27c42fdbbf"
      - "GET https://api.neso.energy/datastore/dump/9b72a2f5-db92-40ca-aa95-b9f1c56f7373"
      - "GET https://api.neso.energy/dataset/ba632bb7-0bf8-4370-bfee-df3236aff285/resource/6e27b1d9-ae9a-4c13-8fe3-272d939ce984/download/archived-index-linked-contracted-energy-volume.zip"
    commands:
      - {run: gridflow ingest neso_data_portal index_linked_contract_volume --last 24h, comment: "the yearly dumps to bronze"}
      - {run: gridflow transform neso_data_portal index_linked_contract_volume --last 24h, comment: "the capture's date to silver"}
      - {run: gridflow ingest neso_data_portal index_linked_contract_volume_files --last 24h, comment: "the archive ZIP, bronze only"}
  record:
    select:
      filter:
        - {column: id, op: in, value: [ES00151372, ES00151377, ES00152294, ES00164522, ES00177627, ES00239190, ES00241156, ES00312361]}
      dedup: {"on": [resource_id, id], order_by: capture_written_at}
      order_by: [starttime]
      columns: [id, starttime, endtime, volume, price, cost, so_flag, reason, asset_id, cp_name, area, note, last_updated, resource_id]
    key: [resource_id, id]
    caption: "Eight of the 16 enactments, October 2021 to November 2024, across four assets."
    fields:
      id: "NESO's identifier of the enactment action"
      starttime: "Start of the delivery window, UTC as NESO states"
      endtime: "End of the window, UTC; NESO does not say whether it is included"
      volume: "Average volume, MW; positive raises generation or cuts demand, NESO says"
      price: "Average price, £/MWh"
      cost: "NESO's cost of the action: labelled £/h, described as a total"
      so_flag: "`T` mainly for system security, `F` mainly for balancing, NESO says"
      reason: "NESO's reason for the action, such as `V_MERSEY` or `V_LONBAR`"
      asset_id: "The asset: a BM unit name, or a name for the contract"
      cp_name: "The contract counterparty, which may differ from the asset owner"
      area: "The asset's delivery area, as NESO writes it"
      note: "NESO's free-text note; blank in all 16 rows"
      last_updated: "When NESO last updated the row, UTC; not its first publication"
      resource_id: "The yearly table the row comes from (CKAN resource id)"
      timestamp_utc: "Equals `starttime`; gridflow's event time"
      published_at: "Null: these dumps carry no usable publication time"
      bronze_capture_id: The bronze file the row was read from
      capture_written_at: When gridflow wrote the capture to bronze, UTC
  notebook:
    lead: >-
      Returns a pandas DataFrame from the view
      `silver_neso_data_portal_index_linked_contract_volume_latest`, filtered on the delivery start
      with both ends included; times come back in Europe/London.
    cells:
      - |
        df = data.neso_data_portal.query("index_linked_contract_volume", "2021-04-01", "2025-03-31")
        df[["id", "starttime", "endtime", "volume", "price", "cost", "asset_id"]].tail()
      - |
        df.assign(hours=(df.endtime - df.starttime).dt.total_seconds() / 3600)[
            ["id", "hours", "volume", "price", "cost"]]
      - |
        df.groupby(["asset_id", "reason"], dropna=False).size()
    needs: the yearly index-linked tables
  related:
    - {dataset: neso_data_portal/voltage-requirement, note: "The voltage need NESO can meet with these contracts"}
    - {dataset: neso_data_portal/outturn-voltage-costs, note: "NESO's monthly spend on voltage, by constraint group"}
    - {dataset: neso_data_portal/day-ahead-power-exchange-prices-nordpool, note: "One GB day-ahead auction; NESO does not say which exchange it means"}
    - {dataset: neso_data_portal/balancing-services-contract-enactment, note: "NESO's general contract enactments, in the same columns"}
---

# Index Linked Contracted Energy Volume

This package is NESO's record of **index-linked contract enactments**. An index-linked contract is
a bilateral arrangement the system operator can use to meet a **voltage requirement**. NESO's own
description says the contract is normally enacted in the morning, ahead of the power-exchange
auction. The generator is paid the agreed strike price, is compensated if the generation spread is
negative, and has a positive spread deducted from the strike price. Because the spread is worked
out from outturn market indices, the contract is called "index linked" (CKAN package `notes`,
@.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json). Each row is **one
contract-enactment action**: an action `ID`, a UTC delivery window (`StartTime`, `EndTime`), an
average `Volume`, a `Price`, a `Cost`, a system-security flag, a free-text reason, the asset and
counterparty, the delivery area, a note, and a `Last_Updated` instant. It is not a settlement-period
table and not a contract master (gridflow `@.planning/phases/v0.22-K-TRD/K-TRD-FACTS.md` section
3.6). The package sits in the NESO Trading group, which describes itself as trading power-exchange,
forward-energy and balancing contracts ahead of the balancing mechanism.

For modelling, it is a small ledger of out-of-market actions the operator took for voltage
reasons, useful as context for constraint and balancing cost. Sibling enactment tables use the same
column layout and the same unresolved cost question:
@./balancing-services-contract-enactment.md and @./super-stable-export-limit-contract-enactment.md;
the historic trade tables are in @./historic-gtma-grid-trade-master-agreement-trades-data.md.

gridflow holds **16 rows** across four year-labelled resources, all captured on 2026-10-08. The
silver output exists on disk but is **held**: the vendor dictionary labels `Cost` as pounds per hour
while describing it as a total cost (price times volume times duration), and gridflow will not
choose between the two readings (see Holds). The package-level status in the front matter is
generated from the registry and reads `eligible`; the family-level eligibility is **held**:
gridflow's models do not consume it until the cost question is answered. The site page shows its
rows (ruling 66): a chart, eight sample rows and a notebook, with the cost question as a caveat.

- Publisher group: Trading
- Registry group: trade-data · archetype: EVT

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Index Linked Contract Enactment FY 21-22 | CSV | dump | `8f694d01-68a5-41b9-9542-dd27c42fdbbf` |
| Index Linked Contract Enactment FY 22-23 | CSV | dump | `ff292de9-59aa-45cc-85ce-e21fed09f5ff` |
| Index Linked Contract Enactment FY 23-24 | CSV | dump | `dff083d2-666b-4e23-9b46-9edd9298f0d3` |
| Index Linked Contract Enactment FY 24-25 | CSV | dump | `9b72a2f5-db92-40ca-aa95-b9f1c56f7373` |

The four CSV resources are CKAN **datastore** resources, captured through the datastore dump
endpoint (ADR-035, @docs/DECISION_LOG/ADR-035-neso-datastore-dump-leg.md). They are not file
uploads, so the download links are dump endpoints and carry no file name. Bytes, rows and CKAN
`last_modified` come from the capture sidecars under
`C:/gridflow-data/bronze/neso_data_portal/index_linked_contract_volume/2026/10/08/`. Data rows equal
the silver rows.

| Resource | Download | Bytes | Data rows | CKAN `last_modified` | Body sha256 prefix |
|---|---|---:|---:|---|---|
| FY 21-22 | [datastore dump](https://api.neso.energy/datastore/dump/8f694d01-68a5-41b9-9542-dd27c42fdbbf) | 1871 | 12 | 2022-04-01T08:24:17.441490 | `5d65334d` |
| FY 22-23 | [datastore dump](https://api.neso.energy/datastore/dump/ff292de9-59aa-45cc-85ce-e21fed09f5ff) | 360 | 2 | 2022-09-01T13:14:15.968060 | `07b45b68` |
| FY 23-24 | [datastore dump](https://api.neso.energy/datastore/dump/dff083d2-666b-4e23-9b46-9edd9298f0d3) | 226 | 1 | none (empty in the sidecar) | `f61cd01e` |
| FY 24-25 | [datastore dump](https://api.neso.energy/datastore/dump/9b72a2f5-db92-40ca-aa95-b9f1c56f7373) | 226 | 1 | none (empty in the sidecar) | `2df1a7d0` |

Package page: [index-linked-contract-volume](https://www.neso.energy/data-portal/index-linked-contract-volume).
The vendor's resource descriptions say only that each resource displays the detail of index-linked
contract enactments for the labelled financial year, and the first two point to a reference
workbook for the Party ID and Asset ID fields. The year labels are names, not proved boundaries:
`TODO: verify` which delivery dates each resource actually covers. gridflow does not assign a
financial year from the label (FACTS section TRD-2).

**Bronze body (full-body scan, FACTS section 3.6 and g5).** Every body has the same exact
13-column header (one header epoch), no BOM, no padded cell and no wholly blank row. All datetime
cells use `%Y-%m-%dT%H:%M:%S` with no literal offset. Each resource was captured once, so no
in-place revision can be observed.

### DOC

None. The package has no DOC-only resource.

### HOLD

| Resource | Format | Capture | Id | Reason (unit) |
|---|---|---|---|---|
| Index Linked Contract Enactment (Archived files) | ZIP | upload | `6e27b1d9-ae9a-4c13-8fe3-272d939ce984` | data container: child inventory committed by X; records pending in TRD (TRD) |
| ↳ Index Linked Contracted Energy Volume/2021-05-07.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2020-12-11.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2020-12-12.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2020-12-13.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2020-12-31.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-01-30.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-01-31.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-03-01.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-03-07.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-03-08.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-03-12.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-03-13.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-03-14.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-04-06.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-04-24.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-04-26.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-04-27.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-04-28 v1.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-04-28 v2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-04-29 v1.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-04-29 v2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-04-30.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-05-02 v1.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-05-02 v2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-05-03.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-05-04.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-05-06.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-05-08.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-05-09.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-05-10.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-05-11.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-05-12.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-05-13.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-05-14.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-05-15.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-05-16.csv::Trades | — | — | HOLD: proposed family index_linked_archive_trades: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-05-17.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-05-18.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-05-19.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-05-20.csv::Trades | — | — | HOLD: proposed family index_linked_archive_trades: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-05-21.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-05-23.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-05-24.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-05-25.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-05-26.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-05-27.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-05-28.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-05-28v2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-05-30.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-05-31.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-01.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-02.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-03.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-04.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-05.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-06.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-07 v2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-07.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-08 v2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-08.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-09 v2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-09.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-10 v2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-10.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-11 v2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-11.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-12 v1.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-12 v2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-13 v2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-13.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-14 v2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-14.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-15.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-16.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-17 v2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-17.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-18 v2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-18 v3.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-20 v2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-20 v3.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-21 v2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-21 v3.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-21.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-21-1.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-22 v2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-22.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-23 v2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-23.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-25 v2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-25 v3.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-25.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-26 v2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-26.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-27 v2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-27 v3.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-27.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-28 v2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-28.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-30 v2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-06-30.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-07-01 v2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-07-01.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-07-02 v2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-07-02.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-07-03 V2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-07-03.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-07-04 V2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-07-04.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-07-05 V2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-07-05.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-07-06 V2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-07-06.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-07-07.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-07-08 v2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-07-08.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-07-10, v2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-07-10.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-07-11 v2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-07-11.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-07-12 v2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-07-12.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-07-13 v2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-07-13.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-07-14 v2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-07-14.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-07-15.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Contract Volume 2021-07-18 .csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Histroic Index Linked Volumes for 2018.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Histroic Index Linked Volumes for 2019.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Histroic Index Linked Volumes from 2017.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Index-Linked Contract Volume update 2021.05.05.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Index-Linked Contract Volume update 2021.05.29 V1.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Index-Linked Contract Volume update 2021.05.29 V2.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |
| ↳ Index Linked Contracted Energy Volume/Index-Linked Contract Volume update 2021-05-22, ROCK-1.csv | — | — | HOLD: proposed family index_linked_contract_volume_archive: record pending in TRD (V-11) (TRD) | — |

The only HOLD resource is the **archive ZIP** `6e27b1d9-ae9a-4c13-8fe3-272d939ce984` (upload,
captured 2026-10-08 as a 391,990 byte body, CKAN `last_modified` 2025-01-09T15:22:16.816570).
Download: [archived-index-linked-contracted-energy-volume.zip](https://api.neso.energy/dataset/ba632bb7-0bf8-4370-bfee-df3236aff285/resource/6e27b1d9-ae9a-4c13-8fe3-272d939ce984/download/archived-index-linked-contracted-energy-volume.zip).
It is a data container with 134 members; the 134 child rows above are held individually.
Neither the container nor any child is **COVERED**: no equivalence proof was run (ADR-037,
@docs/DECISION_LOG/ADR-037-neso-container-readers-and-covered-harness.md), and the members are a
different, older table, not a copy of the modern CSVs. Detail is in the `_files` family below.

## Families

### `index_linked_contract_volume`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

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

**One header epoch.** The record accepts one exact header, the thirteen vendor columns in the
order above. Vendor column names are kept as the source; silver names are lower case, with
`AssetID` and `CP_Name` spelled `asset_id` and `cp_name`. `resource_id` (the CKAN resource the row
came from) is added as a key column, so a row is identified by resource and action `ID`.

**What the columns mean (vendor dictionary).** The descriptions come from NESO's saved field info
for the datastore (gridflow
`@.planning/research/neso-snapshots/field-info/20261008T114228Z/index_linked_contract_volume.json`).
That file was read for **one** resource, the FY 24-25 one (selected as the resource with the latest
metadata); the other three resources' dictionaries were not read separately, so `TODO: verify`
that they carry the same descriptions and units.

- **`ID`**: the ID of the contract enactment action. Treated as a string identifier, never
  normalised.
- **`StartTime`**, **`EndTime`**: start and end of the enactment action, "in UTC format". The
  window is a delivery window; the dictionary does not say whether the end is inclusive, so do not
  assume an end-exclusive convention for duration-sensitive work (FACTS g1).
- **`Volume`**: the **average volume** of the action. The dictionary comment gives a sign
  convention: a positive number is an action that increases generation, decreases demand or
  provides upward margin; a negative number reduces generation, increases demand or provides
  downward margin. It adds that values are rounded to up to one decimal place.
- **`Price`**: the average price of the action, rounded to up to two decimal places.
- **`Cost`**: described as the total cost to the system operator for the action, with the comment
  that cost is volume times price times duration. See the unit conflict below.
- **`SO_Flag`**: `T` means the action is mainly for system-security reasons and `F` that it is
  mainly for balancing reasons. It is kept as the supplied letter; it is not a settlement run type.
- **`Reason`**: free-text detail (voltage, thermal, rate-of-change-of-frequency, upward margin,
  downward reserve and similar).
- **`AssetID`**: the asset; for a balancing-mechanism unit it is the NG BM unit name, otherwise a
  name reflecting the contract with the counterparty. Stored as supplied, with no BM unit or EIC
  normalisation.
- **`CP_Name`**: the contract counterparty, which may differ from the asset owner.
- **`Area`**: the delivery area of the asset (for example England and Wales, Scotland, or an
  interconnector).
- **`Note`**: notes or comments.
- **`Last_Updated`**: the date and time the information was last updated, in UTC.

**Units (vendor dictionary only).** The dictionary `unit` field is **MW** for `Volume`, **pounds
per MWh** for `Price`, and **pounds per hour** for `Cost`; the three datetime columns carry "UTC
ISO 8601", and every other column has `N/A`. The dictionary file stores the pound sign as an
ordinary UTF-8 £ in the Price unit (£/MWh) and the Cost unit (£/h). gridflow keeps the values as
delivered and does no unit conversion: no MW-to-MWh, no hourly-to-total scaling, and no change to
the `Cost` label (FACTS g4). The archived ZIP tables below use different quantities and must never
be merged into these columns.

**Cost dimension (the hold).** The dictionary gives `Cost` the unit pounds per hour, but its
description (total cost) and its formula (volume times price times duration) describe a total in
pounds. Both cannot be right. Which one NESO publishes is **TODO: COST-DIMENSION**, and it needs a
corrected NESO dictionary or a clarification. It is a consumer-semantic limit, not a casting
failure: the column parses cleanly as a float. The duration unit in the formula is also not stated
(`TODO: verify`). gridflow does not relabel `Cost` as pounds by calculation.

**Two clocks.**

1. **Vintage (capture-based; `available_at`).** Each resource is a datastore dump, so the vintage
   policy is `capture_fallback` (ADR-035): `available_at` is the sidecar `written_at` of the
   capture, to the microsecond, and `published_at` is **null**. The silver check (2026-10-12)
   confirms `available_at` equals `capture_written_at` on all 16 rows, and `published_at` is null
   on all 16. The four capture times are 2026-10-08T11:10:20.129708Z, 11:10:50.188914Z,
   11:11:20.182592Z and 11:11:50.199636Z. CKAN `last_modified` exists for two of the four
   resources (2022-04-01 and 2022-09-01, above) but is **not** used as the vintage, because the
   package refresh is `frozen` and a frozen refresh does not establish when a row was first
   available (FACTS section 3.6, T06). `Last_Updated` is an **update** instant, not an issue
   time: no immutable-publication guarantee is documented, so it is never used as `available_at`.
   Because the vintage is the capture time (2026-10-08), an as-of query before that sees no rows,
   even for old enactments, and an as-of read returns the bytes gridflow holds, not necessarily
   what NESO showed on that date.
2. **Event time (temporal recipe `utc_instant(starttime)`).** The event instant is the
   enactment-window **start**. In silver, `timestamp_utc` and `event_time` both equal `starttime`
   on all 16 rows (checked 2026-10-12), tz-aware UTC. The cells are naive text that the
   dictionary documents as UTC, so they are read as UTC and converted at the silver boundary. This
   is the delivery start, not the time the action was agreed or published; `EndTime` is the window
   end and is kept as its own column. No row in silver has an end before its start.

**Identity and selection (ADR-039).**

- The entity key is `(resource_id, id)`. All 16 `id` values are distinct, and none repeats
  between resources, so no overlap exists (FACTS g3).
- The vendor publishes no key and gives no permanent-uniqueness guarantee for `ID`: `TODO: verify`
  a vendor-guaranteed unique key, and whether a published row can be revised in place.
- `_latest` is `whole_capture` per `resource_id`: the newest complete capture of each
  year-labelled resource, not a per-key latest. gridflow does not claim a revision key. Only one
  capture per resource exists, so amendment behaviour cannot yet be measured.
- These are agreed enactment actions, not forecasts and not settlement accounting: no `run_type`
  applies and none is fabricated (RULINGS 707). The measured delivery targets all precede the
  capture, so the forward-target exemption does not apply and is not needed (FACTS g2).

**Sentinels and missing values (FACTS g5).** The full-body scans found no literal `N/A` or `NA`,
no padded cell, no numeric thousands separator, no currency or percentage symbol and no
non-finite token in this family. FACTS lists no signed `-1` count for it. No null token is
declared and nothing is mapped to null. Blank cells stay null, never zero or an empty string.
Silver null counts (16 rows, 2026-10-12): `reason` 1, `area` 2, `note` 16 (the note is blank on
every row), and 0 in every other vendor column, including the three measure columns.
`published_at` is null on all 16 by design.

**Row counts (silver, 2026-10-12).**

| Resource | Rows | Distinct `id` |
|---|---:|---:|
| `8f694d01-68a5-41b9-9542-dd27c42fdbbf` (FY 21-22) | 12 | 12 |
| `ff292de9-59aa-45cc-85ce-e21fed09f5ff` (FY 22-23) | 2 | 2 |
| `dff083d2-666b-4e23-9b46-9edd9298f0d3` (FY 23-24) | 1 | 1 |
| `9b72a2f5-db92-40ca-aa95-b9f1c56f7373` (FY 24-25) | 1 | 1 |
| Total | 16 | 16 |

**Activation (2026-10-12, master `374a7be`, PR #111).** The trading batch merged triple-green
(RULINGS 714) and was transformed from the 2026-10-08 captures with `--start/--end 2026-10-08`.
There was no prior silver, so nothing was overwritten and no snapshot was taken (RULINGS 715).
Silver has **16 rows** for this family, equal to the planned count, with 0 validation failures
and no blank-row exclusions (324,996 rows across the nine trading families). The batch-wide
reconcile `--all --cutoff 2026-10-12` exited 0 with 0 gaps over 150 families (47 adjudicated,
0 stale; RULINGS 716). Gridflow `@.planning/v0.22-RESULTS.md` section TRD holds the receipt.

Silver layout: one Parquet file per resource capture under
`C:/gridflow-data/silver/neso_data_portal/index_linked_contract_volume/year=2026/month=10/`. The
`year=`/`month=` partition is the **capture** date, not the delivery date. There are 22 columns:
the thirteen vendor columns, then `resource_id`, `timestamp_utc`, `published_at`,
`bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id` and
`dataset_version`. All timestamps are tz-aware UTC. `dataset_version` is `1+e1` (record version 1,
generic engine version 1). No gold view or builder reads this family.

### `index_linked_contract_volume_files`

- Kind: files · archetype: EVT · refresh: frozen · empty allowed: no
- files: catalogue only

This family catalogues the archive ZIP and produces **no silver**. The disposition of the ZIP and
all its members is HOLD (table above); the two workbook members are named in the table with the
suffix `::Trades`.

What the ZIP contains (gridflow `@.planning/phases/v0.22-K-TRD/K-TRD-FACTS.md` section 4.2):

- **134 members**: 132 genuine CSV files and **2 Excel workbooks named `.csv`** (the two
  `Contract Volume` files for 2021-05-16 and 2021-05-20, each with a worksheet called `Trades`).
- The CSV members hold **330,024 physical data rows**: 162,000 wholly blank rows and 168,024
  nonblank rows. 127 of the CSVs need the cp1252 fallback and 5 decode as UTF-8.
- These are **Date and settlement-period volume tables**, a different grain from the modern
  enactment actions (one row per `Date`, `SP` and sometimes `Unit ID`). Five distinct header
  epochs occur:

| Header | Members |
|---|---:|
| `Date,SP,Unit ID,Strike Price (£/MWh),Volume Indexed (MW)` | 112 |
| `Date,SP,Strike Price (£/MWh),Volume Indexed (MW)` | 15 |
| `Date,SP,Volume Indexed (MW)` | 3 |
| `Date,SP,Volume Fixed Price (MW),Volume Indexed (MW)` | 1 |
| `Date,SP,Volume (MW)` | 1 |

- The archive dates end before the modern resources begin, and the modern table is keyed by
  enactment `ID`, so no current-family duplicate nomination survives (FACTS section 4.2). No
  COVERED grant exists.
- Three historical members (the 2017, 2018 and 2019 volume files, spelled "Histroic" by the
  vendor) contain **exact repeated full rows** (excess repeats: 45,249 in the 2017 file, 19,153 in
  the 2018 file and 5,504 in the 2019 file). No vendor-column key is therefore lossless, and
  gridflow adds no occurrence counter and drops nothing silently (RULINGS 538).
- Date cells appear in both `%d/%m/%Y` and `%Y-%m-%d` spellings, sometimes under the same header.

Open archive questions, none of which blocks the modern family:

- `TODO: ARCHIVE-INDEX-RECORDS` faithful per-member records, worksheet interpretation, date-format
  mapping, settlement and calendar evidence, run identity where required, and amendment
  precedence.
- `TODO: ARCHIVE-INDEX-DUPLICATES` NESO to explain or correct the identical repeated rows, or
  supply an omitted identity.
- `TODO: verify` how the archive `SP` ordinal (1 to 48 in the measured members) maps to
  settlement periods on 46- and 50-period clock-change days (gridflow's period range is 1 to 50).
- The archive header labels name MW volume columns and a strike price in pounds per MWh. That is
  the vendor's own header text; the archive tables' units are not otherwise documented here, and
  `Volume Indexed (MW)` must not be merged into the modern `volume`.

## Cadence

- Registry refresh: frozen
- Vendor metadata (snapshot extras, verbatim):
  - Status: Live

The portal lists the package as "Live", while gridflow's registry sets the refresh to **frozen**:
the four resources are named for the financial years 2021-22 to 2024-25 and are not re-polled on a
schedule. The vendor gives no update frequency (the snapshot has no `update_frequency` field), and
the package `metadata_modified` is 2025-01-09. `TODO: verify` whether NESO still appends
enactments for later financial years and whether a new year will arrive as a new resource. Only
more captures, compared pair by pair, can show whether rows are amended in place. One capture per
resource exists to date.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `index_linked_contract_volume`: held: TODO: COST-DIMENSION — the dictionary labels `Cost` £/h but describes it as total cost (price × volume × duration); which is published? (unit v0.22-K-TRD)

The silver output exists on disk but is **held**. It may not be used for models until the question
above is answered; the site page shows its rows with the question as a caveat (ruling 66). The hold
sits in the record (RULINGS 707); the sibling modern enactment families (balancing, GTMA
financial-year and super-stable export limit) carry the same question under the same unit tag. It
is a vendor-semantics question, so a NESO answer settles it, not inspection of values. The archive
ZIP is held separately and is not part of this hold.

**What the rows show (silver, checked 2026-10-24).** In all 16 rows, `Cost` equals `Volume` ×
`Price` × the window's length in hours, for example `ES00151372`: 110 × 71.82 × 9 = 71,101.8. That
is how a total in £ behaves, not a rate in £/h. It supports NESO's description over its label, but
it does not settle what NESO intends to publish, so the hold stands.

**What is not established.** Whether `Cost` is a rate (pounds per hour) or a total (pounds), the
duration unit in the NESO formula, the end-of-window convention, whether a published `ID` is
permanently unique, and whether rows are revised after publication. gridflow will not guess any of
them, will not rename `Cost`, and will not derive a total from price, volume and the window
length to fill the gap. `TODO: name the unit that will settle COST-DIMENSION` once one is opened.

**What settles it.** A NESO dictionary correction or a written clarification of the `Cost`
dimension; once ruled, releasing the hold is a record edit with no transform change.
