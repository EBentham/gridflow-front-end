---
source: "neso_data_portal"
package: "constraint-management-intertrip-service-information-cmis"
dataset_key: "cmis_intertrip"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-10
layer_coverage: "bronze, silver"
eligibility: "eligible"
eligibility_scope: "package-level only; family cmis_intertrip is held (E-SEM, RULINGS 632), see Holds"
---

# Constraint Management Intertrip Service Information (CMIS)

NESO's record of the **arming and disarming of units contracted under the Constraint Management
Intertrip Service** (vendor wording, captured package notes). Per the captured field-info, each
row records the unit (`BMU ID`), the date and time the unit was armed to the intertrip from and
until, the arming fee in force (`Current Arming Fee`) and the cost for that utilisation
(`Cost for this utilisation`). The vendor says services are paid at least a month in arrears and
the dataset is updated shortly after the payments for the month are made. The mechanism of
the service itself (what arming does to the unit and the network) is not described in the
captured vendor notes or field-info: `TODO: verify` against the CMIS contract (linked under
Units below).
The `B6/EC5` column on the newer files tags each unit as one of two contracted service groups:
SP Renewables units (B6) or Galloper Offshore units (EC5) (captured field-info
`cmis_intertrip.json`). The package is useful as a cost and utilisation history of one
constraint-management tool, to be read alongside the thermal constraint costs
(@thermal-constraint-costs.md). It is **not** a forecast and carries no publication or
instruction-issue column.

The silver output for this package is **held** (unit E-SEM). The front-matter `eligibility:
eligible` is the registry's package-level status, not a family-level one: the only family,
`cmis_intertrip`, is held. The arming clock and the newer fee
unit are both unresolved (see Holds). This page therefore gives schema, row counts and structure
only. It publishes no data values from the held family.

- Publisher group: Constraint management
- Registry group: constraint-management · archetype: EVT

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Constraint Management Intertrip Arming 2022-2023 | CSV | upload | `60b4055c-d87e-4ebe-8d21-e023f506e461` |
| Constraint Management Intertrip Arming 2023-2024 | CSV | upload | `38c6a5cd-388d-4275-b404-361c6eb102b3` |
| Constraint Management Intertrip Arming 2024-2025 | CSV | upload | `2f0777a3-719c-4ffe-96c2-61117a5ec468` |
| Constraint Management Intertrip Arming 2025-2026 | CSV | upload | `c6f0c279-87c9-4123-a4d1-b2d6d98b43a7` |
| Constraint Management Intertrip Arming 2026-2027 | CSV | upload | `60a1c0c6-4821-4e38-bc87-c6b4d510be6d` |

All five resources map to the single family `cmis_intertrip`. The package has **no DOC
resources**. Each resource is one annual (financial-year) file. They are separate files, not
revisions of one another. The captured download URLs (from the 2026-10-06 catalogue snapshot):

| Resource | Download | Captured file | Bytes | Data rows | CKAN `last_modified` | Header epoch |
|---|---|---|---:|---:|---|---|
| 2022-2023 | [cmp-management-intertrip-arming-2022-2023.csv](https://api.neso.energy/dataset/7c20761d-3aab-4e9f-926e-6117fa8c4524/resource/60b4055c-d87e-4ebe-8d21-e023f506e461/download/cmp-management-intertrip-arming-2022-2023.csv) | `raw_20261008T091457Z_60b4055c-d87e-4ebe-8d21-e023f506e461_bf43e369.csv` | 33,675 | 441 | `2024-03-12T14:16:03.129176` | 1 (older) |
| 2023-2024 | [cmp-intertrip-arming-2023-2024.csv](https://api.neso.energy/dataset/7c20761d-3aab-4e9f-926e-6117fa8c4524/resource/38c6a5cd-388d-4275-b404-361c6eb102b3/download/cmp-intertrip-arming-2023-2024.csv) | `raw_20261008T091500Z_38c6a5cd-388d-4275-b404-361c6eb102b3_5baf9a29.csv` | 8,403 | 110 | `2024-04-08T11:56:08.968572` | 1 (older) |
| 2024-2025 | [cmp-intertrip-arming-2024-2025.csv](https://api.neso.energy/dataset/7c20761d-3aab-4e9f-926e-6117fa8c4524/resource/2f0777a3-719c-4ffe-96c2-61117a5ec468/download/cmp-intertrip-arming-2024-2025.csv) | `raw_20261008T091502Z_2f0777a3-719c-4ffe-96c2-61117a5ec468_c1016587.csv` | 18,916 | 247 (246 nonblank) | `2025-05-06T10:00:06.772385` | 2 (newer) |
| 2025-2026 | [cmp-intertrip-arming-2025-2026.csv](https://api.neso.energy/dataset/7c20761d-3aab-4e9f-926e-6117fa8c4524/resource/c6f0c279-87c9-4123-a4d1-b2d6d98b43a7/download/cmp-intertrip-arming-2025-2026.csv) | `raw_20261008T091505Z_c6f0c279-87c9-4123-a4d1-b2d6d98b43a7_c156410d.csv` | 12,900 | 167 | `2026-04-28T16:25:43.722522` | 2 (newer) |
| 2026-2027 | [cmp-intertrip-arming-2026-2027.csv](https://api.neso.energy/dataset/7c20761d-3aab-4e9f-926e-6117fa8c4524/resource/60a1c0c6-4821-4e38-bc87-c6b4d510be6d/download/cmp-intertrip-arming-2026-2027.csv) | `raw_20261008T091508Z_60a1c0c6-4821-4e38-bc87-c6b4d510be6d_bb03d88d.csv` | 6,478 | 83 | `2026-10-01T10:37:07.382134` | 2 (newer) |

The stable handle for each file is its resource id, not the URL. CKAN `last_modified` values are
emitted without an offset and read as UTC (gridflow
`@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). The 2024-2025 file holds one
wholly blank record (all columns empty), which is not a row of the family. Silver therefore holds
246 rows for that file.

## Families

### `cmis_intertrip`

- Kind: tabular · archetype: EVT · refresh: monthly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| BMU ID | `bmu_id` | string | — | no | — | — |
| Arming Date Time | `arming_date_time` | string | — | no | — | — |
| Disarming Date Time | `disarming_date_time` | string | — | yes | — | — |
| Current Arming Fee (£ / SP) | `current_arming_fee_gbp_per_sp` | float64 | — | yes | — | — |
| Cost for this utilisation (£) | `utilisation_cost_gbp` | float64 | — | yes | — | £ |

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| BMU ID | `bmu_id` | string | — | no | — | — |
| Arming Date Time | `arming_date_time` | string | — | no | — | — |
| Disarming Date Time | `disarming_date_time` | string | — | yes | — | — |
| Current Arming Fee (£ / MWH) | `current_arming_fee_gbp_per_mwh` | float64 | — | yes | — | £/SP |
| Cost for this utilisation (£) | `utilisation_cost_gbp` | float64 | — | yes | — | £ |
| B6/EC5 | `b6_ec5` | string | — | yes | — | — |

- Entity key: `resource_id`, `bmu_id`, `arming_date_time`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the CKAN `last_modified`
   of the captured resource. Each of the five files has its own vintage (table above), and all rows
   of a file share it. Checked on every silver row on 2026-10-10. The vintage says when the file
   was last changed on the portal. The files carry **no issue or publication column**: nothing says
   when an individual arming row first became public. Older files' vintages (2024) are
   therefore a late upper bound on availability for their rows.
2. **Event time (`none`).** The record's temporal recipe is `none`. So `timestamp_utc` =
   `event_time` = the **capture time** (`capture_written_at`, 2026-10-08), not an arming
   instant. Checked equal on every silver row on 2026-10-10. It carries no information about when
   a unit was armed. The intended event anchor is the arming start (FACTS T06), but no instant is
   built from it until the clock question below is answered. The arming and disarming times stay
   in the raw string columns `arming_date_time` and `disarming_date_time`. Do not filter or order
   by `timestamp_utc` expecting event order.

**Two header epochs, stored in one schema.** The two older files (2022-2023, 2023-2024) carry the
five-column header with `Current Arming Fee (£ / SP)`. The three newer files carry a six-column
header with `Current Arming Fee (£ / MWH)` and a trailing `B6/EC5` column. Silver holds the union
of columns: every row has all seven vendor-derived columns, and the columns that its file's header
lacks are null (checked on 2026-10-10: `current_arming_fee_gbp_per_mwh` and `b6_ec5` are null on
all 551 older rows; `current_arming_fee_gbp_per_sp` is null on all 496 newer rows).
**The two fee columns stay distinct.** They are not converted, merged or coalesced, because the
unit of the newer column is in dispute (below). The vendor's current documentation announces a
later header renaming. That is evidence of a possible third epoch, not a captured one
(FACTS g5). `dataset_version` reads `1+e1` on every row: the `e1` is the engine version, not the
header epoch.

**Clock conflict (arming and disarming timestamps).** The vendor's package page says the
timestamps are in **GB local time**. Every captured `Arming Date Time` and `Disarming Date Time`
nevertheless ends in a literal `+00:00` offset, including dates inside British Summer Time.
Two readings are possible: GB local wall time with a mechanically added zero offset, or true
UTC instants. gridflow does **not** pick one. It stores both columns as **raw strings**, does not
strip or relabel the offset, and does not build a UTC event time (FACTS CON-6 clock blocker).
`TODO: verify` with NESO which reading is correct. Until then these columns are not usable as
instants, and the family is held.

**Units (vendor dictionary only, as cited in FACTS).**

- `Cost for this utilisation (£)` → `utilisation_cost_gbp`: **GBP**, declared in the dictionary
  unit field. The vendor comment says it combines the arming fee and the arming duration. The
  comment's formula is the arming fee per settlement period divided by 30 minutes and multiplied
  by the duration in minutes.
- Older `Current Arming Fee (£ / SP)` → `current_arming_fee_gbp_per_sp`: **GBP per settlement
  period**. The older resource's dictionary states `£/SP` explicitly
  ([2022-2023 dictionary](https://www.neso.energy/data-portal/constraint-management-intertrip-service-information-cmis/constraint_management_intertrip_arming_2022-2023)).
- Newer `Current Arming Fee (£ / MWH)` → `current_arming_fee_gbp_per_mwh`: **unit disputed**. The
  column header and the field description both say £/MWh. The dictionary's `unit` field says
  `£/SP`, and the cost comment repeats the older duration-only formula (captured field-info
  `cmis_intertrip.json`). The contracted B6 service terms define the arming payment rate in
  GBP/MWh ([CMIS contract, Schedule 4](https://www.neso.energy/document/247621/download)),
  which supports the header. That contract does not remove the conflicting dictionary and does not
  prove it applies to every EC5 row. `TODO: verify` with NESO, or a corrected resource dictionary,
  before the newer fee is treated as a settled unit. The table above shows the generated
  "Vendor unit" `£/SP` for the newer column. That is the dictionary's value and is the thing in
  dispute. Do not read it as the established unit.
- `bmu_id`, `arming_date_time`, `disarming_date_time` and `b6_ec5` carry no physical unit.
  Do not convert between the two fee columns.

**`B6/EC5` definitions.** The captured field-info describes the column as a unit tag: a
SP Renewables unit (B6) or a Galloper Offshore unit (EC5). A live annual-resource dictionary
instead describes the groups with SCOTEX / East Anglia wording
([2025-2026 dictionary](https://www.neso.energy/data-portal/constraint-management-intertrip-service-information-cmis/constraint_management_intertrip_arming_2025-2026)).
These are contextual definitions. The raw codes stay as stored (FACTS section 8: boundary and
group codes are stored as-is, with no case, punctuation or alias normalisation). `bmu_id` is
likewise stored as-is, with no normalisation. `TODO: verify` which dictionary wording is current.

**Sentinels and missing values (FACTS g5).** The record declares no null token.

- The 2024-2025 file contains one wholly blank record. It is dropped as an empty row, not
  treated as a sentinel (247 file rows, 246 silver rows).
- No nonblank `NA`, `N/A` or `-1` token was observed.
- **Zero is a real value.** `Cost for this utilisation` is zero on 0, 1, 8, 10 and 4 rows across the
  five files in resource order, with longest consecutive zero runs of 0, 1, 3, 2 and 3 rows
  (physical body order, not a reconstructed time series). All zeros are preserved. gridflow
  makes no claim about what a zero means. Sentinel observation does not establish vendor
  sentinel meaning.
- No column is null in silver other than the structural nulls of the absent-header columns above.

**Identity and selection.** The entity key is `(resource_id, bmu_id, arming_date_time)`, using the
raw arming string. The pair `(BMU ID, Arming Date Time)` is measured unique inside each file:
441, 110, 246, 167 and 83 distinct nonblank keys with zero duplicate excess. No pair of files
shares a key, so the annual files are disjoint. `TODO: verify` that NESO guarantees the key. No
vendor text says so. Because the files are separate annual resources, `_latest` is `whole_capture`
partitioned by `resource_id`: the newest capture of each resource replaces its previous capture as
a whole, and the other four resources are untouched. A family-wide newest-capture rule would have
kept only one year.

**Activation (2026-10-10, master `49f7c1a`, PR #104).** Transformed at cutoff 2026-10-08
(five captures, no prior silver): **1,047 silver rows**, equal to the planned count
(441 + 110 + 246 + 167 + 83). Nothing was overwritten. Reconcile `--all --cutoff 2026-10-08`
exited 0 with 105 families, 0 gaps and 0 stale (gridflow `@.planning/v0.22-RESULTS.md` section CON;
RULINGS 632, 634, 635). Silver is stored as one Parquet file per capture under
`silver/neso_data_portal/cmis_intertrip/year=2026/month=10/`. Silver columns beyond the vendor
columns: `resource_id`, `timestamp_utc`, `published_at`, `bronze_capture_id`,
`capture_written_at`, `event_time`, `available_at`, `source_run_id`, `dataset_version`
(timestamps tz-aware UTC).

## Cadence

- Registry refresh: monthly
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Monthly
- Captures to date: one per resource (2026-10-08). No scheduled refresh has run yet.

The vendor's package description says services are paid at least a month in arrears and the
dataset is updated shortly after the payments for the month are made, so the feed lags the
events it records. The 2026-2027 file is the live year: its vintage (`2026-10-01`) is the
most recent of the five, and the earlier four have not changed since 2024 to April 2026.
`TODO: verify` whether past-year files are ever restated after their first publication. Only
repeated captures compared row by row can show this. `TODO: verify` whether a new financial-year file appears as a new resource
and what gridflow must change to capture it.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `cmis_intertrip`: held: TODO: do the arming/disarming timestamps carry GB local wall time with a mechanically added +00:00 offset, or actual UTC instants? And is the newer arming fee GBP/MWh (header) or GBP/SP (dictionary)? (unit E-SEM)

The family is held by RULINGS 632 (seat ruling, PROXY-SOURCED). The silver output exists on disk
(1,047 rows) but is not eligible for publication or point-in-time use. This page gives schema,
row counts and structural counts only. It gives no data values, ranges or samples. Unit E-SEM
must answer two things before the hold can lift:

1. Whether the arming and disarming timestamps are GB local wall time with a mechanically
   added `+00:00`, or true UTC instants. Until then no event instant is built and the temporal
   recipe stays `none`.
2. Whether the newer `Current Arming Fee (£ / MWH)` column is GBP per MWh (header, description and
   contract) or GBP per settlement period (dictionary unit field). Until then the two fee
   columns are never combined.

A resolution of (1) would change the event-time recipe for the family and so needs a new
record version. It is not a re-label of existing silver.

Related holds in the same batch (gridflow `@docs/neso_data_portal/eligibility.md`):
`constraint_limits_24m`, `otf_network_congestion` and `voltage_requirement` are held under their
own E-SEM questions. `da_constraint_flows_limits` is held and its one capture is adjudicated
**failed**: the transform raises `DuplicateEntityKeyError` (ADR-040), so it has **0 silver
rows**. `thermal_constraint_costs` is eligible apart from its oldest CSV resource, which is held at
resource level (comma-formatted costs), and its workbook child family
`thermal_constraint_costs_xlsx` is eligible.
