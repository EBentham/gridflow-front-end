---
source: "neso_data_portal"
package: "super-stable-export-limit-contract-enactment"
dataset_key: "ssel_contract_enactment"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-12
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Super Stable Export Limit Contract Enactment

A register of **Super Stable Export Limit (SSEL) contract enactments** published by NESO on the
Open Data Portal. NESO describes an enactment as the exercise of a contract that lowers a
generator's minimum-generation capability, followed by Balancing Mechanism dispatch if it is
needed. An enactment does not itself have to change energy output (gridflow
`@.planning/phases/v0.22-K-TRD/K-TRD-FACTS.md` §3.8). Each row is one enactment action with a
UTC start and end. It is **not** a per-settlement-period table: no period column exists in either
header. The package is a small, historical record of how often NESO used the service and what it
paid. Use it as context for constraint and minimum-generation analysis, joined by time to the
balancing and constraint-cost pages (@balancing-services-contract-enactment.md,
@constraint-breakdown.md). It is not a forecast and not a settlement table.

The package spans **two header epochs** under one family. The oldest year (FY 20-21) uses a
legacy layout with `Reduction (MW)` and `Price (£/MW/hr)`. Later years use the modern layout
shared with the other contract-enactment tables (`Volume`, `Price`, `Cost`, ...). The two value
vocabularies are **different quantities** and are never merged in silver. The family's silver
output is **held** (see Holds): the modern `Cost` column has an unresolved unit question. Row
counts and the schema are published here. No data values are.

- Publisher group: Trading
- Registry group: trade-data · archetype: EVT

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Super Stable Export Limit Contract Enactment 20-21 | CSV | dump | `835d50b9-2d7c-4318-bd04-c7f94b149041` |
| Super Stable Export Limit Contract Enactment FY 21-22 | CSV | dump | `bf9ca254-e9de-4aa2-841a-fb34566de38a` |
| Super Stable Export Limit Contract Enactment FY 22-23 | CSV | dump | `34f185bc-087a-41b2-b514-305e31158e5a` |
| Super Stable Export Limit Contract Enactment FY 23-24 | CSV | dump | `817036a8-10af-442e-93d4-8f21ae038b52` |
| Super Stable Export Limit Contract Enactment FY 24-25 | CSV | dump | `43078fd2-7583-4b0a-b398-e48de3817515` |
| Super Stable Export Limit Contract Enactment FY 25-26 | CSV | dump | `8e7168fa-8617-4d83-9696-d6bf1f09c9c5` |

All six resources are CKAN datastore tables captured through the datastore dump endpoint
`https://api.neso.energy/datastore/dump/<resource id>` (ADR-035). There are **no DOC or
catalogue-only resources** in this package, so there are no download links to list. The stable
handle for each resource is its id. Each has exactly one capture so far (2026-10-08), so each
bronze body is both its newest and its only capture.

| Resource | Epoch | Bytes | Data rows | Bronze file (under `2026/10/08/`) |
|---|---|---:|---:|---|
| 20-21 | 1 (legacy) | 1,200 | 20 | `raw_20261008T112422Z_835d50b9-2d7c-4318-bd04-c7f94b149041_ab93d260.csv` |
| FY 21-22 | 2 (modern) | 212 | 1 | `raw_20261008T112453Z_bf9ca254-e9de-4aa2-841a-fb34566de38a_3d0f6244.csv` |
| FY 22-23 | 2 (modern) | 340 | 2 | `raw_20261008T112523Z_34f185bc-087a-41b2-b514-305e31158e5a_3e4e6917.csv` |
| FY 23-24 | 2 (modern) | 345 | 2 | `raw_20261008T112553Z_817036a8-10af-442e-93d4-8f21ae038b52_3b0639d7.csv` |
| FY 24-25 | 2 (modern) | 233 | 1 | `raw_20261008T112623Z_43078fd2-7583-4b0a-b398-e48de3817515_8efaf3df.csv` |
| FY 25-26 | 2 (modern) | 219 | 1 | `raw_20261008T112653Z_8e7168fa-8617-4d83-9696-d6bf1f09c9c5_43b83723.csv` |

Totals: 2,549 bytes, **27 data rows** (20 legacy + 7 modern). Each sidecar `.meta.json` sits
beside its body. Bodies are UTF-8 CSV.

Dataset page: [NESO SSEL dataset](https://www.neso.energy/data-portal/super-stable-export-limit-contract-enactment).
Legacy-epoch dictionary:
[20-21 resource dictionary](https://www.neso.energy/data-portal/super-stable-export-limit-contract-enactment/super_stable_export_limit_contract_enactment_20-21).

## Families

### `ssel_contract_enactment`

- Kind: tabular · archetype: EVT · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Record | `id` | string | — | no | — | — |
| Unit | `unit` | string | — | yes | — | — |
| Start | `starttime` | datetime | `%Y-%m-%dT%H:%M:%S` | no | UTC | — |
| End | `endtime` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | — |
| Reduction (MW) | `reduction_mw` | float64 | — | yes | — | — |
| Price (£/MW/hr) | `price_mw_hr` | float64 | — | yes | — | — |

Schema, epoch 2:

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

**The two clocks for this family:**

1. **Vintage (capture time, not `ckan_last_modified`).** The registry's vintage is
   `capture_fallback` (ADR-035, ADR-031): the datastore dump has no evidence that any field dates
   a row's availability, so `available_at` is the sidecar's exact `written_at`, and `published_at`
   is **null** on every row. This differs from the upload families, whose vintage is the CKAN
   `last_modified` of the captured file. The sidecar does record a CKAN `last_modified` for each
   resource, and it is informational only here. For the three oldest resources it is a
   2021–2022 timestamp, and for the three newest it is **empty** (they carry only a CKAN
   `metadata_modified`). Silver `available_at` therefore equals the capture's `written_at`
   (2026-10-08T11:24–11:27Z, one value per resource), and `capture_written_at` repeats it.
   Historical publication time per enactment is `TODO: verify`. The modern `Last_Updated` column
   is a documented UTC update instant, but the vendor gives no immutable-issue guarantee, so it
   is kept as data and is not used as `published_at` (issue recipe `none` in both epochs).
2. **Event time (`utc_instant` on `starttime`).** `timestamp_utc` = `event_time` = the
   enactment's start instant, parsed as UTC from `Start` (legacy) or `StartTime` (modern).
   Checked on every silver row on 2026-10-12. Both epochs are evidenced UTC by their own
   dictionaries: the legacy dictionary declares the `Start` and `End` clocks as UTC
   `%Y-%m-%dT%H:%M:%S`, and the modern columns are naive text the dictionary labels UTC ISO 8601.
   Event time is therefore a **real delivery instant**, not the capture time. Endpoint
   inclusivity of the start/end pair is not documented: do not assume end-exclusive behaviour in
   duration-sensitive code (FACTS g1).

**Temporal-coverage caution.** Resource year labels are not perfect boundaries. The FY 22-23
resource contains a delivery start that also appears in the FY 21-22 resource. Their `id` values
do not overlap, so this is not evidence that one row amends the other (FACTS §3.8). Do not
partition by the label.

**Mapping across the two epochs.** The legacy and modern columns are folded into one silver
table so a single temporal recipe finds its typed input in every epoch:

- `Record` (legacy) and `ID` (modern) → string `id`. Legacy `Record` is a sequential SSEL
  identifier with no physical unit (FACTS T01). The literal numeric text is kept.
- `Start` / `StartTime` → `starttime`. `End` / `EndTime` → `endtime`. All four are UTC.
- Legacy-only columns (`unit`, `reduction_mw`, `price_mw_hr`) are **null** for modern rows. The
  modern-only columns (`volume`, `price`, `cost`, `so_flag`, `reason`, `asset_id`, `cp_name`,
  `area`, `note`, `last_updated`) are null for legacy rows. This is structural, not missing data.
- The legacy `Unit` column has no unit declared in the generated schema and its meaning is
  `TODO: verify` (it is not a physical unit; do not read it as a BM unit id until the vendor
  says so).

**Units (vendor dictionary only, never inferred from a column name).**

| Epoch | Column | Unit | Source |
|---|---|---|---|
| Legacy | `Reduction (MW)` | **MW** — reduction in minimum generating capability | Legacy resource dictionary |
| Legacy | `Price (£/MW/hr)` | **£/MW/hr** — the enactment payment rate | Legacy resource dictionary |
| Modern | `Volume` | **MW** | Modern dictionary (FACTS g4) |
| Modern | `Price` | **£/MWh** | Modern dictionary (FACTS g4) |
| Modern | `Cost` | **£/h as published**, unresolved (see Holds) | Modern dictionary |

- **Do not merge** legacy `reduction_mw` into `volume`, or legacy `price_mw_hr` into `price`.
  Their documented quantities and price dimensions differ (a capacity-based £/MW/hr rate versus
  a £/MWh price). Silver keeps four separate columns and no conversion is performed.
- `Cost` is labelled £/h, but the dictionary's description and formula describe a total cost
  (price × volume × duration). The label and the description conflict. gridflow does not
  relabel it by calculation (FACTS g4, §3.8).
- `Record`/`ID`, the two flags and the text columns carry no physical unit. The "Vendor unit"
  entry `UTC ISO 8601` in the generated table is a clock format, not a unit.

**Sentinels and missing values (FACTS g5).** The record declares no null token. Across the
captured bodies the measured counts are zero for the literal tokens `N/A` and `NA`, padded
cells, thousands separators, currency or percentage symbols and non-finite numeric tokens.
No `-1` sentinel and no zero-valued cell was measured in this package, so nothing is converted
and no value is treated as missing. Modern `Area` and `Note` are blank in all seven modern
rows. Blanks stay null and never become zero. The meaning of the blank `Area` and `Note` fields
is `TODO: verify`.

**Identity and selection.** The entity key is (`resource_id`, `id`). It is unique within every
resource, and no resource pair shares an identifier. `_latest` is `whole_capture` partitioned by
`resource_id`: a newer capture of a resource replaces that resource's previous capture as a
whole. Permanent vendor uniqueness and amendment precedence are not documented, and the
record claims neither (`TODO: verify`). No resource has a second capture yet, so in-place
revisions cannot be measured.

**Forecast-eligibility note.** Every enactment start is on or before the capture time (27 of
27). These are historical agreed actions, not forecasts of them, so a pre-vintage delivery
target is not itself a failure (FACTS g2). Historical pre-capture availability stays unproved,
and that is why `available_at` is the capture time and not the delivery time.

**Activation (2026-10-12, master `374a7be`, PR #111).** Transformed at `--start/--end
2026-10-08` with no prior silver, so nothing was overwritten and no snapshot was needed:
**27 silver rows**, equal to the planned count (20 + 1 + 2 + 2 + 1 + 1). Reconcile `--all
--cutoff 2026-10-12` exited 0 with 150 families, 0 gaps, 47 adjudicated and 0 stale (gridflow
`@.planning/v0.22-RESULTS.md` §TRD; RULINGS 714, 715, 716).

Silver columns beyond the vendor columns: `resource_id`, `timestamp_utc`, `published_at`,
`bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id`,
`dataset_version` (all timestamps tz-aware UTC; `dataset_version` `1+e1` is record version 1,
epoch 1, and the modern resources carry the same value in the silver files read on 2026-10-12).
`TODO: verify` whether epoch-2 rows should read `1+e2`. The measured silver value for every
resource was `1+e1`.

Silver files: `C:/gridflow-data/silver/neso_data_portal/ssel_contract_enactment/year=2026/month=10/`
(one Parquet file per capture).

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Status: Live

The registry refresh is daily, but the content is a slow register: the resources are
year-labelled and most are small. Captures to date: one per resource (2026-10-08). No scheduled
refresh has run yet. How often NESO appends to the current-year resource, and when it creates
the next year's resource, is `TODO: verify`. `TODO: verify` whether past-year resources are ever
rewritten after the year closes.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `ssel_contract_enactment`: held: TODO: COST-DIMENSION — the dictionary labels `Cost` £/h but describes it as total cost (price × volume × duration); which is published? (unit v0.22-K-TRD)

The hold is on the **whole family record**, not on one column or epoch. The registry carries a
single eligibility per record, so the legacy rows are held together with the modern rows. The
silver output exists on disk (27 rows) and is not published. This page shows no data values from
it: no sample rows and no minimum, maximum or other value statistics.

The question for NESO is which of two quantities the modern `Cost` column holds: a rate in £/h,
as its unit label says, or a total in £ over the enactment, as its description and formula say.
The hold lifts when NESO corrects the dictionary or answers the question. gridflow will not
relabel the unit by calculation. This is a consumer-semantic limit, not a casting failure, and
the same question holds the modern balancing, index-linked and GTMA FY-table outputs (gridflow
`@.planning/v0.22-RESULTS.md` §TRD; RULINGS 707, 715).

Related pages in the same batch: @balancing-services-contract-enactment.md,
@index-linked-contract-volume.md and @historic-gtma-grid-trade-master-agreement-trades-data.md.
