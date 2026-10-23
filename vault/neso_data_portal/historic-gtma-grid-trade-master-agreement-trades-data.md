---
source: "neso_data_portal"
package: "historic-gtma-grid-trade-master-agreement-trades-data"
dataset_keys: ["gtma_trades_data", "gtma_trades_data_pre", "gtma_trades_fy"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-12
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Historic GTMA (Grid Trade Master Agreement) Trades Data

NESO's record of the **Grid Trade Master Agreement (GTMA)** trades conducted since April 2015
(package notes). The publisher's organisation text describes its trading team and trading "in
advance of the balancing mechanism"; `TODO: verify` the precise contractual meaning of a GTMA trade
with NESO, as no gridflow source defines it beyond that. Each row is one trade: an identifier, a UTC
delivery window, a volume, a price and a cost, plus a flag. In the upload families the resource
dictionary says `SO Flag` `T` is a system trade and `F` an energy trade; in the FY dictionary `T`
means mainly system security and `F` mainly balancing. The package is **trade data, not settlement
data**. It has no settlement period and no settlement run, and `SO Flag` and `Reason` are not
`run_type`. Use it to see the trades NESO records, when, at what price and, in the FY family, with
what stated reason. It
complements the BM bid-offer record (@../../elexon/README.md) and the NESO enactment tables
(@balancing-services-contract-enactment.md). Background:
@../../../20-domain/markets/gb-balancing-mechanism.md.

The vendor publishes the history as 13 CSV resources in three generations. They have different
schemas and **different volume units**, so gridflow keeps them in three separate families and
never merges them.

| Family | Resources | Generation | Output status |
|---|---|---|---|
| `gtma_trades_data` | 6 uploads, FY 2015-16 to FY 2020-21 | Upload CSV, 7 columns, volume in MWh | **Eligible** for 5 resources. The FY 2020-21 resource is held (see Holds). |
| `gtma_trades_data_pre` | 1 upload, Apr 2021 to the start of June 2021 | Same schema and units as the first | **Eligible** |
| `gtma_trades_fy` | 6 datastore dumps, FY 2021-22 to FY 2026-27 | Datastore CSV, 10 columns, volume in MW | **Held** (COST-DIMENSION) |

Silver activation (RULINGS 715, 2026-10-12, no prior silver): `gtma_trades_data` 51,230 rows,
`gtma_trades_data_pre` 7,470 rows, `gtma_trades_fy` 237,735 rows. Every count equals the planned
count. The post-merge reconcile (RULINGS 716, cutoff 2026-10-12) ran clean: 150 families, 0 gaps,
47 adjudicated, 0 stale. No gold layer consumes this package.

Attribution: Supported by National Energy SO Open Data

- Publisher group: Trading
- Registry group: trade-data · archetype: EVT

## Files by disposition

All 13 resources are CSV. **There are no DOC resources** in this package: every file is a data
resource, and none is catalogue-only. Download links below are the vendor URLs from the 2026-10-06
catalogue snapshot (gridflow `@.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json`).
The 2026-10-06 snapshot gives these upload file names; `TODO: verify` their stability over time
(only one snapshot and one capture per resource exist). The datastore dumps are keyed by resource
id only.

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Historic GTMA Trades Data - Apr 2015 - March 2016 | CSV | upload | `bde33bcf-efc6-4e4a-bc7c-452b7424ea45` |
| Historic GTMA Trades Data - Apr 2016 - March 2017 | CSV | upload | `b24d619b-f6ea-41e6-87ab-569960594d3f` |
| Historic GTMA Trades Data - Apr 2017 - March 2018 | CSV | upload | `6f2772a4-ac7a-4eb7-a8ee-59ca6a03e205` |
| Historic GTMA Trades Data - Apr 2018 - March 2019 | CSV | upload | `58f3079a-1440-4a70-b227-f4e661defee7` |
| Historic GTMA Trades Data - Apr 2019 - March 2020 | CSV | upload | `6a03c415-475f-4005-bf55-b9108291c511` |
| Historic GTMA Trades Data - Apr 2021 - Mar 2022 (Pre June 2021) | CSV | upload | `8cf964b6-b94c-4d35-88f4-312834aa6e8c` |
| Historic GTMA Trades FY 21-22 | CSV | dump | `11a2f532-a7ce-46f8-9d82-88b3289daa82` |
| Historic GTMA Trades FY 22-23 | CSV | dump | `83b1d432-f8b4-4393-a8fd-bcaeb6bd7620` |
| Historic GTMA Trades FY 23-24 | CSV | dump | `f659641a-668f-446c-92c5-72d387121330` |
| Historic GTMA Trades FY 24-25 | CSV | dump | `2d5bf30f-68ae-4340-a583-52e6af7fb7e8` |
| Historic GTMA Trades FY 25-26 | CSV | dump | `bd8a822f-b065-489c-bbdd-d3099b179f20` |
| Historic GTMA Trades FY 26-27 | CSV | dump | `e7a8abae-4e96-48b0-b9d7-54651da0cdb5` |

The first five rows and the pre-June row are the upload families. Their capture, as
`raw_20261008T<stamp>Z_<resource_id>_<hash8>.csv` under
`bronze/neso_data_portal/<family>/2026/10/08/` (gridflow `@.planning/phases/v0.22-K-TRD/K-TRD-FACTS.md` §2):

| Resource (family) | Download | CKAN `last_modified` | Bytes | Data rows |
|---|---|---|---:|---:|
| 2015-16 (`gtma_trades_data`) | [gtma_trades_2015-16.csv](https://api.neso.energy/dataset/8e511255-6cd7-41c0-868e-8d4d29bced0b/resource/bde33bcf-efc6-4e4a-bc7c-452b7424ea45/download/gtma_trades_2015-16.csv) | 2020-12-09T17:08:51.416402 | 206,088 | 2,843 |
| 2016-17 (`gtma_trades_data`) | [gtma_trades_2016-17.csv](https://api.neso.energy/dataset/8e511255-6cd7-41c0-868e-8d4d29bced0b/resource/b24d619b-f6ea-41e6-87ab-569960594d3f/download/gtma_trades_2016-17.csv) | 2020-12-09T16:50:44.945078 | 212,366 | 2,947 |
| 2017-18 (`gtma_trades_data`) | [gtma_trades_2017-18.csv](https://api.neso.energy/dataset/8e511255-6cd7-41c0-868e-8d4d29bced0b/resource/6f2772a4-ac7a-4eb7-a8ee-59ca6a03e205/download/gtma_trades_2017-18.csv) | 2020-12-09T16:51:36.261207 | 253,306 | 3,479 |
| 2018-19 (`gtma_trades_data`) | [gtma_trades_2018-19.csv](https://api.neso.energy/dataset/8e511255-6cd7-41c0-868e-8d4d29bced0b/resource/58f3079a-1440-4a70-b227-f4e661defee7/download/gtma_trades_2018-19.csv) | 2020-12-09T16:53:07.230679 | 653,577 | 8,988 |
| 2019-20 (`gtma_trades_data`) | [gtma_trades_2019-20.csv](https://api.neso.energy/dataset/8e511255-6cd7-41c0-868e-8d4d29bced0b/resource/6a03c415-475f-4005-bf55-b9108291c511/download/gtma_trades_2019-20.csv) | 2020-12-09T16:54:00.343328 | 2,385,250 | 32,973 |
| Pre June 2021 (`gtma_trades_data_pre`) | [gtma_trades_2021-22.csv](https://api.neso.energy/dataset/8e511255-6cd7-41c0-868e-8d4d29bced0b/resource/8cf964b6-b94c-4d35-88f4-312834aa6e8c/download/gtma_trades_2021-22.csv) | 2021-06-06T15:43:05.883360 | 542,796 | 7,470 |

The six FY resources are datastore dumps (ADR-035). Download: the vendor dump URL
`https://api.neso.energy/datastore/dump/<resource id>`, for example
[FY 21-22](https://api.neso.energy/datastore/dump/11a2f532-a7ce-46f8-9d82-88b3289daa82). Captured
once each on 2026-10-08. Their rows and bytes (`gtma_trades_fy`):

| Resource | Bytes | Data rows |
|---|---:|---:|
| FY 21-22 | 4,599,413 | 45,799 |
| FY 22-23 | 6,443,328 | 65,409 |
| FY 23-24 | 4,101,012 | 40,595 |
| FY 24-25 | 3,257,781 | 33,092 |
| FY 25-26 | 3,237,768 | 32,289 |
| FY 26-27 | 2,035,167 | 20,551 |

The 2026-10-06 catalogue snapshot gave a CKAN `last_modified` for FY 21-22
(2022-04-01T08:53:40.828093) and FY 22-23 (2023-01-23T06:03:04.523943) only, and `None` for the
other four. The FY family does not use it (see the clocks below).

### HOLD

| Resource | Format | Capture | Id | Reason (unit) |
|---|---|---|---|---|
| Historic GTMA Trades Data - Apr 2020 - March 2021 | CSV | upload | `8e14ae8e-2091-4abc-a2e6-a4b82e5519ab` | TODO: GTMA-2020-DUPLICATES — identifiers ES00104406–ES00104415 each appear twice as identical full rows; publication defect or distinct trades needing another identifier? (v0.22-K-TRD) |

Download (held, not published): [gtma_trades_2020-21.csv](https://api.neso.energy/dataset/8e511255-6cd7-41c0-868e-8d4d29bced0b/resource/8e14ae8e-2091-4abc-a2e6-a4b82e5519ab/download/gtma_trades_2020-21.csv)
(CKAN `last_modified` 2021-04-06T11:20:05.467319). Captured: 4,006,832 bytes, 55,542 data rows
(`raw_20261008T110453Z_8e14ae8e-2091-4abc-a2e6-a4b82e5519ab_4bd1f961.csv`). Bronze keeps the file
byte for byte. The resource-level HOLD means it produces **no silver rows** (51,230 =
2,843 + 2,947 + 3,479 + 8,988 + 32,973, the five passing resources).

## Families

All three families are tabular, archetype EVT, `empty_allowed: no`, one header epoch each, and a
`record` (declarative) silver transformer: there is no bespoke code. Silver carries the common
provenance columns beside the vendor columns: `timestamp_utc`, `published_at`, `available_at`,
`event_time`, `bronze_capture_id`, `capture_written_at`, `source_run_id` and `dataset_version`.
`resource_id` is carried by `gtma_trades_data` and `gtma_trades_fy` only (silver, checked
2026-10-12). `gtma_trades_data_pre` is a single resource and has no `resource_id` column: its 15
silver columns are `trade_id`, `start_time`, `end_time`, `volume`, `price`, `cost`, `so_flag` and the
eight provenance columns above. Every captured file so far is the only capture of its resource (2026-10-08), so
no revision between captures has been observed.

### `gtma_trades_data`

- Kind: tabular · archetype: EVT · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Trade ID | `trade_id` | string | — | no | — | — |
| Start Time | `start_time` | datetime | `%Y-%m-%dT%H:%M:%SZ` | no | UTC | — |
| End Time | `end_time` | datetime | `%Y-%m-%dT%H:%M:%SZ` | yes | UTC | — |
| Volume | `volume` | float64 | — | yes | — | MWh |
| Price | `price` | float64 | — | yes | — | £/MWh |
| Cost | `cost` | float64 | — | yes | — | £ |
| SO Flag | `so_flag` | string | — | yes | — | — |

- Entity key: `resource_id`, `trade_id`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: utc_instant (`start_time`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the CKAN `last_modified`
   of the captured resource (read as UTC, as CKAN emits it with no offset;
   gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). It is a property of the
   whole file, not of each trade. The five silver resources carry five vintages, all on
   2020-12-09 between 16:50:44 and 17:08:51 UTC (table above). The file has **no issue column**,
   and the record's issue recipe is `none`. When a trade was first public is therefore not
   evidenced: `TODO: verify` row-level publication availability (FACTS TODO
   HISTORIC-GTMA-AVAILABILITY). The vintage is later than the delivery of every row, so any
   point-in-time query with these vintages sees the whole history as published on 2020-12-09.
2. **Event time (`utc_instant` on `start_time`).** `timestamp_utc` = `event_time` = `start_time`,
   the UTC start of the trade's delivery window (checked on all 51,230 silver rows on 2026-10-12).
   The captured starts run from `2015-04-01T22:30:00Z` to `2020-03-31T23:00:00Z`. Start and end
   carry a literal `Z`. The vendor dictionary says UTC. Endpoint inclusivity of the window is not
   stated, so do not assume end-exclusive when you compute durations.

Key and shape (checked on silver, 2026-10-12):

- **Key.** `Trade ID` (example shape `ES12345678`) is unique within each of the five silver
  resources (rows equal distinct ids). The vendor gives no guarantee of permanent uniqueness. The
  key is `(resource_id, trade_id)` with `whole_capture` per resource: the five annual resources
  are independent snapshots, not amendments of one another. No trade id is shared with
  `gtma_trades_data_pre` or `gtma_trades_fy` (measured on the captured bodies: 0 overlaps).
- **Year labels are approximate.** A resource is labelled by financial year, but is not a strict
  UTC civil-year partition. The FY 2019-20 silver data ends at the `2020-03-31T23:00:00Z` start.
  The held FY 2020-21 resource is likewise labelled by financial year; `TODO: verify` its exact UTC bounds with NESO.
- **Reversed and equal windows are kept.** In the five silver resources, 10 rows have `end_time`
  before `start_time` and 26 have equal start and end. gridflow does not repair or drop them.
- **Signed values are real.** `-1` appears in `volume` (10 rows), `price` (9) and `cost` (4). No
  vendor source defines `-1` as a missing-value marker, so it is retained as a signed number and
  is not in the null-token list. Zero `price` and zero `cost` occur in 74 rows each. No source defines
  `0` as a missing-value marker, so zero cells are kept as numbers and not treated as missing.
  There are no `N/A`, padded cells, thousands separators or currency symbols in the captured
  bodies. No nulls in any silver column.
- **`SO Flag`** has two values: `T` (36,809 rows) and `F` (14,421 rows). The dictionary: `T` is a
  **system trade** and `F` an **energy trade**.

**Units (vendor dictionary only; from the resource dictionary of the FY 2020-21 upload as cited in
FACTS §3.3).** `Volume` is the **total** volume of the trade in **MWh**. `Price` is **£/MWh**.
`Cost` is **£**, positive when National Grid ESO pays (the dictionary comment). The package
description says "the volume in MW", which disagrees with the resource dictionary's MWh. Treat the
resource dictionary as authoritative and `TODO: verify` with NESO which is intended. No unit is
converted.

### `gtma_trades_data_pre`

- Kind: tabular · archetype: EVT · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Trade ID | `trade_id` | string | — | no | — | — |
| Start Time | `start_time` | datetime | `%Y-%m-%dT%H:%M:%SZ` | no | UTC | — |
| End Time | `end_time` | datetime | `%Y-%m-%dT%H:%M:%SZ` | yes | UTC | — |
| Volume | `volume` | float64 | — | yes | — | MWh |
| Price | `price` | float64 | — | yes | — | £/MWh |
| Cost | `cost` | float64 | — | yes | — | £ |
| SO Flag | `so_flag` | string | — | yes | — | — |

- Entity key: `trade_id`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`start_time`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** One resource, one vintage: `2021-06-06T15:43:05.883360`
   for all 7,470 rows. As above, no issue column (issue `none`), so this is a resource-level
   publication time, not proof of when each trade's values existed.
2. **Event time (`utc_instant` on `start_time`).** `timestamp_utc` = `event_time` = `start_time`.
   Starts run from `2021-04-01T01:00:00Z` to `2021-06-01T06:00:00Z`. Schema, flag semantics and
   units are those of `gtma_trades_data` above (`Volume` MWh, `Price` £/MWh, `Cost` £).

Key and shape (silver, 2026-10-12): `Trade ID` is unique (7,470 distinct ids). No reversed or
equal windows. `-1` appears in `volume` (3 rows) and `price` (5), not in `cost`; zero `price` and
`cost` in 30 rows each. `SO Flag`: `T` 6,074 rows, `F` 1,396. No nulls.

The family is **not** a duplicate of the modern FY table: it has zero trade-id overlap with
`gtma_trades_data` and with `gtma_trades_fy`. It is the earlier segment of FY 2021-22 (Apr to the
start of June 2021) with the upload schema and units, and the vendor then continues the history
in the FY dumps. How the pre-June cut relates to the start of the FY 21-22 dump is not documented:
`TODO: verify` with NESO that the two split cleanly with no gap or overlap in delivery time. Trade
ids do not overlap.

### `gtma_trades_fy`

- Kind: tabular · archetype: EVT · refresh: daily · empty allowed: no

**Status: held (COST-DIMENSION).** Silver exists on disk (237,735 rows from activation). This page
publishes no data values from it, and no value statistics: only structure and row counts.

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
| Note | `note` | string | — | yes | — | — |
| Last_Updated | `last_updated` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | UTC ISO 8601 |

- Entity key: `resource_id`, `id`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: utc_instant (`starttime`)

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

**The two clocks for this family:**

1. **Vintage (`capture_fallback`, not `ckan_last_modified`).** The FY dumps are datastore dumps
   (ADR-035), not uploads, and the 2026-10-06 snapshot gave no CKAN `last_modified` for four of the
   six. So `published_at` is **null** in every silver row and `available_at` is the gridflow
   capture time, the sidecar `written_at` of each dump, between
   `2026-10-08T11:04:59.977534Z` and `2026-10-08T11:07:29.142743Z`. It says when gridflow saw the
   file, not when NESO published the trade. `Last_Updated` is kept as a typed UTC column. It is
   not a vintage: NESO does not say it is immutable issue time. `TODO: verify` historical public
   availability. Issue is `none`.
2. **Event time (`utc_instant` on `starttime`).** `timestamp_utc` = `event_time` = `starttime`,
   the UTC start of the trade window. The vendor writes these without an offset ("UTC format"), so
   gridflow parses them as UTC.

Key and overlap: `ID` is unique inside every FY resource, so the key is `(resource_id, id)` with
`whole_capture` per resource. **FY 21-22 (`11a2f532-…`) and FY 22-23 (`83b1d432-…`) both publish
nine identical rows** (`ES00165376` to `ES00165384`, equal on every raw column including
`Last_Updated`). NESO states no precedence, so both are served and the overlap is recorded as
an ADR-040 reconcile adjudication in
`@src/gridflow/connectors/neso_data_portal/registry/_reconcile_adjudications.json`
(RULINGS 707). It does not make either resource canonical and it removes no rows. No other pair of
FY resources overlaps. The reconcile of 2026-10-12 therefore reports this overlap as adjudicated,
not as a gap.

**Units and the hold (dictionary text; no values here).** `Volume` is **average** volume in
**MW**, signed: the dictionary comment gives a positive number as an action that increases
generation, decreases demand or provides upward margin. `Price` is the average price in
**£/MWh**. `Cost` is labelled **£/h**, but the dictionary also describes it as the *total* cost to
National Grid ESO and gives its formula as `Cost = Volume × Price × Duration`. A total cost
would be in pounds, not pounds per hour. gridflow does not relabel the unit by calculation and does
not pick one. Held question: **which is published, £/h or £?** (unit v0.22-K-TRD; the same
inconsistency holds for `Cost` in the modern enactment tables, see
@balancing-services-contract-enactment.md). `SO_Flag`: `T` means the action is mainly for system
security, `F` mainly for balancing. `Reason` is free text (voltage, thermal, ROCOF, margin and so
on). `Reason` is blank in 3,427 of 237,735 captured rows. `Note` is blank in every captured row (bronze,
237,735 of 237,735). Silver `reason` carries 3,427 nulls. Silver `note` carries 223,075 nulls plus
14,660 empty-string cells, all in FY 23-24 (`f659641a-…`); `TODO: verify` the null-token handling
that leaves those cells as empty strings rather than null (counts only, no values, so the hold is
respected). This is the vendor's
"System Flag" and "Trade Reason", not a settlement `run_type`.

Because the dictionary for `Volume` here is **MW** and in the upload families it is **MWh**, never
stack `gtma_trades_fy.volume` with `gtma_trades_data.volume` without a documented conversion.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Status: Live
- Captures to date: one per resource, all on 2026-10-08. No scheduled refresh has run yet, so no
  revision between two captures of the same resource has been measured.

The vendor package text: the dataset "will be updated on a monthly basis shortly after the start of
the month, with the previous months data", and the live data file is "refreshed every morning to
capture the trades occurred between D-1 06:00 and D 06:00". NESO therefore reports the live file on a
06:00-to-06:00 trading window. `TODO: verify` whether the annual resources follow the same window:
a financial-year resource is not a strict midnight-to-midnight year (see the year-label note under
`gtma_trades_data`).

- `TODO: verify` which resource is the daily-refreshed "live data file". The FY 26-27 dump
  is the likely one, but the vendor does not name it. The 7 upload resource descriptions say "This data
  file will be updated on a monthly basis"; the 6 FY dump descriptions say only that the data set
  displays the detail of Historic GTMA trades for the financial year. gridflow has only one capture of each resource, so no
  refresh has been observed; `TODO: verify` which resources NESO actually still refreshes.
- `TODO: verify` whether a refresh rewrites earlier rows of the same resource. The vendor warns
  that **delivered trades can change after the fact**, for example a counterparty defaults and
  does not deliver, and that "the data may not be updated retrospectively". A trade in this data
  is therefore a record of the agreed trade, not a guarantee of delivery. Only repeated captures
  compared row by row can show how often rows change.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `gtma_trades_fy`: held: TODO: COST-DIMENSION — the dictionary labels `Cost` £/h but describes it as total cost (price × volume × duration); which is published? (unit v0.22-K-TRD)
- `gtma_trades_data`, resource `8e14ae8e-2091-4abc-a2e6-a4b82e5519ab` (Apr 2020 - March 2021):
  resource-level HOLD: TODO: GTMA-2020-DUPLICATES — identifiers ES00104406–ES00104415 each appear
  twice as identical full rows; publication defect or distinct trades needing another identifier?
  (unit v0.22-K-TRD)

**`gtma_trades_fy` (COST-DIMENSION).** Held by the seat on the FACTS recommendation (RULINGS 707).
The unit question is whether `Cost` is a rate (£/h, as labelled) or a total (£, as described). It
decides what a consumer may multiply or sum. Until NESO corrects the dictionary or answers, the
silver output stays on disk and this page publishes no `volume`, `price` or `cost` values from
it. The structure, key, clocks and row counts above are not in dispute. The hold lifts when NESO
states the dimension of `Cost`, or when a corrected dictionary is captured.

**`gtma_trades_data`, FY 2020-21 resource (GTMA-2020-DUPLICATES).** In the captured body, ten
identifiers (`ES00104406` through `ES00104415`) each appear **twice with identical complete
rows**. That is 55,542 rows for 55,532 distinct ids. Adding the value columns to the key cannot
tell the pairs apart, so no vendor-column key is lossless for this resource, and a whole-family
record that admitted it would fail the duplicate-key guard. gridflow does **not** drop one of each
pair, generate a row counter or relabel the ids (RULINGS 538: no silent dedup). The resource is
therefore carved out with a resource-level HOLD, so it feeds no silver output, while the other five
upload resources are served. Bronze keeps the file unchanged. NESO must say whether the repeats are
a publication defect, or distinct trades that need another identifier, or supply a corrected body.
The other five upload resources have no repeated ids.

The package-level `eligibility: eligible` in the front matter is the package registry entry. The
holds are per family and per resource (gridflow `@docs/neso_data_portal/eligibility.md`):
`gtma_trades_data` and `gtma_trades_data_pre` are eligible, `gtma_trades_fy` is held.

Sibling holds from the same batch, same unit: the balancing-service, index-linked and SSEL
enactment tables share the COST-DIMENSION question (@balancing-services-contract-enactment.md).
