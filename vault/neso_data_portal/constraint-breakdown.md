---
source: "neso_data_portal"
package: "constraint-breakdown"
dataset_key: "constraint_breakdown"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-10
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Constraint Breakdown Costs and Volume

This package is NESO's account of **why the system operator took balancing actions on the
transmission network**, split into four named reasons: reducing the largest loss, increasing
system inertia, voltage constraints and thermal constraints. For each calendar date it gives
one **cost in pounds** and one **volume in MWh** per reason, in a single wide row of eight
numbers. The vendor describes it as "constraint breakdown information to provide additional
transparency of why as ESO we are taking actions on the system", and says the data "is applicable
to the transmission network only". The first two reasons are about rate of change of frequency
(RoCoF): a low-inertia system must either limit the largest credible loss or add inertia, and
both cost money to do. Voltage and thermal reasons are the two ordinary network-constraint
causes (reactive-power balance, and flows exceeding circuit capacity between regions). It is a
backward-looking (outturn) series, not a forecast; it has no issue time; and it is a daily
total, not a per-settlement-period series.

**Seven things to know before using it.**

1. **One family, ten resources, one per financial year.** `constraint_breakdown` reads ten CSV
   files, 2017-18 to 2026-27, each covering 1 April to 31 March (the 2026-27 file runs to
   2026-10-01 at its vintage). Silver holds **3,470 rows**, one per date, 2017-04-01 to
   2026-10-01. All ten resources are SILVER; nothing is held.
2. **Two clocks.** The vintage is the CKAN `last_modified` of each captured file (`available_at`
   = `published_at`), which differs per file and can be years after the dates in it. The event
   clock is `date_sp1(date)`: `timestamp_utc` is the **start of settlement period 1 of the date
   in GB local time, as UTC**, a day anchor and not an instant (see Families).
3. **The values can be revised after the fact.** The vendor note says tags on actions "can
   occasionally be changed post event" and the dataset "would be refreshed to reflect the up to
   date information". A past date's numbers are therefore not guaranteed immutable. gridflow
   selects the whole latest capture per resource, so a re-upload of a year replaces that year's
   rows as a unit; it never edits bronze. How often older years are re-uploaded is not stated
   (`TODO: verify`).
4. **Wide, not long.** The category is the column, not a row discriminator: eight value columns,
   cost in `£` and volume in `MWh` per category, per the vendor dictionary. Do not sum across
   categories without checking that they are exclusive (`TODO: verify`: the vendor does not say
   whether one action can appear under two reasons, or whether the four reasons are the whole of
   constraint spend).
5. **Volumes are signed, and two categories are negative on many dates.** `Reducing largest
   loss volume` is negative on 1,603 of 3,470 dates and `Thermal constraints volume` on 2,844.
   The vendor's own dictionary example for the first is `-47450`, so negatives are intended, but
   the vendor does not define the sign convention (`TODO: verify`; the gridflow data does not
   prove that negative means a net reduction in output).
6. **Zeros and `-1` are real values.** Zero runs are long and are not nulled. Four thermal
   volume cells are exactly `-1`, which is a published number, not a recognised missing-value
   marker (see Sentinels).
7. **One calendar day is absent: 2025-04-08.** The 2025-26 body has 364 rows. It is a gap in the
   vendor file, not a gridflow exclusion. Do not zero-fill.

Sibling constraint-management and cost packages: @./thermal-constraint-costs.md (a separate
daily thermal cost by named boundary group), @./outturn-voltage-costs.md,
@./24-months-ahead-constraint-cost-forecast.md and @./gb-system-inertia-bid-and-offer-costs.md.
Settlement-day background: @../../../20-domain/concepts/settlement-period.md. The batch evidence
is gridflow `@.planning/phases/v0.22-K-BAL-1/K-BAL-1-FACTS.md` and the verification is
`@.planning/phases/v0.22-K-BAL-1/VERIFICATION.md`.

- Publisher group: Balancing costs
- Registry group: balancing · archetype: SER

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Constraint Breakdown 2017-2018 | CSV | upload | `3651e9e3-52a8-46b6-a675-3a4c2aedc813` |
| Constraint Breakdown 2018-2019 | CSV | upload | `26af8438-1824-4436-9bbd-d397a9a517e2` |
| Constraint Breakdown 2019-2020 | CSV | upload | `c4d2be3a-4c05-4fac-be7e-56368ca46142` |
| Constraint Breakdown 2020-2021 | CSV | upload | `87088ac4-72d5-48ff-9ee1-f2a99e18277a` |
| Constraint Breakdown 2021-2022 | CSV | upload | `419337fb-f609-45e3-9097-798a41b4b3de` |
| Constraint Breakdown 2022-2023 | CSV | upload | `efb633ae-f6d7-444b-8759-449ac0539dd0` |
| Constraint Breakdown 2023-2024 | CSV | upload | `24d067d8-1328-452a-9720-21cb691e491e` |
| Constraint Breakdown 2024-2025 | CSV | upload | `748557ef-2bb3-41c0-8181-5f1a148c1ff4` |
| Constraint Breakdown 2025-2026 | CSV | upload | `6afe1c2b-6d70-4e76-8e74-0952b0a2beab` |
| Constraint Breakdown 2026-2027 | CSV | upload | `4136a8e2-07c5-4784-8096-28999447a16e` |

There are no DOC, HOLD or catalogue-only resources in this package: all ten are tabular CSV
files with an identical header, and every one is read to silver.

**Downloads and captures.** Every resource was captured once, on 2026-10-08 (09:15:12 to
09:15:38 UTC), from `api.neso.energy`. Bronze is under
`C:/gridflow-data/bronze/neso_data_portal/constraint_breakdown/2026/10/08/`, one body and one
`.meta.json` sidecar per resource. Sizes are physical body sizes and row counts are body rows
over the complete body (K-BAL-1 FACTS). The package page is
[Constraint Breakdown Costs and Volume](https://www.neso.energy/data-portal/constraint-breakdown);
the CKAN package id is `fb56b46e-cef3-4eb8-9294-0ca19769b7eb`. The package was created in the
catalogue on 2021-05-25, had its metadata last modified on 2026-10-03T11:00:54.744166, has no
version string, and carries nine tags (`Contstraints` as spelled by the vendor, `Costs`,
`Daily`, `Inertia`, `Rocof`, `Subscribable`, `Thermal`, `Voltage`, `Volumes`). Author:
National Grid Electricity System Operator.

| Resource | Download | Bytes | Body rows | CKAN `last_modified` (vintage) |
|---|---|---:|---:|---|
| 2017-2018 | [constraint-breakdown-2017-2018.csv](https://api.neso.energy/dataset/fb56b46e-cef3-4eb8-9294-0ca19769b7eb/resource/3651e9e3-52a8-46b6-a675-3a4c2aedc813/download/constraint-breakdown-2017-2018.csv) | 18,301 | 365 | 2021-08-03T13:02:43.115452 |
| 2018-2019 | [constraint-breakdown-2018-2019.csv](https://api.neso.energy/dataset/fb56b46e-cef3-4eb8-9294-0ca19769b7eb/resource/26af8438-1824-4436-9bbd-d397a9a517e2/download/constraint-breakdown-2018-2019.csv) | 19,279 | 365 | 2021-08-03T12:58:42.610033 |
| 2019-2020 | [constraint-breakdown-2019-2020.csv](https://api.neso.energy/dataset/fb56b46e-cef3-4eb8-9294-0ca19769b7eb/resource/c4d2be3a-4c05-4fac-be7e-56368ca46142/download/constraint-breakdown-2019-2020.csv) | 20,074 | 366 | 2024-03-07T10:32:33.105338 |
| 2020-2021 | [constraint-breakdown-2020-2021.csv](https://api.neso.energy/dataset/fb56b46e-cef3-4eb8-9294-0ca19769b7eb/resource/87088ac4-72d5-48ff-9ee1-f2a99e18277a/download/constraint-breakdown-2020-2021.csv) | 20,715 | 365 | 2021-06-09T14:57:07.736484 |
| 2021-2022 | [constraint-breakdown-2021-2022.csv](https://api.neso.energy/dataset/fb56b46e-cef3-4eb8-9294-0ca19769b7eb/resource/419337fb-f609-45e3-9097-798a41b4b3de/download/constraint-breakdown-2021-2022.csv) | 18,558 | 365 | 2022-06-08T11:22:02.313951 |
| 2022-2023 | [constraint-breakdown-2022-2023.csv](https://api.neso.energy/dataset/fb56b46e-cef3-4eb8-9294-0ca19769b7eb/resource/efb633ae-f6d7-444b-8759-449ac0539dd0/download/constraint-breakdown-2022-2023.csv) | 16,890 | 365 | 2023-04-06T15:50:32.383318 |
| 2023-2024 | [constraint-breakdown-2023-2024.csv](https://api.neso.energy/dataset/fb56b46e-cef3-4eb8-9294-0ca19769b7eb/resource/24d067d8-1328-452a-9720-21cb691e491e/download/constraint-breakdown-2023-2024.csv) | 17,986 | 366 | 2024-04-04T10:47:03.220307 |
| 2024-2025 | [constraint-breakdown-2024-2025.csv](https://api.neso.energy/dataset/fb56b46e-cef3-4eb8-9294-0ca19769b7eb/resource/748557ef-2bb3-41c0-8181-5f1a148c1ff4/download/constraint-breakdown-2024-2025.csv) | 18,384 | 365 | 2025-06-16T14:51:46.011303 |
| 2025-2026 | [constraint-breakdown-2025-2026.csv](https://api.neso.energy/dataset/fb56b46e-cef3-4eb8-9294-0ca19769b7eb/resource/6afe1c2b-6d70-4e76-8e74-0952b0a2beab/download/constraint-breakdown-2025-2026.csv) | 18,583 | 364 | 2026-04-07T09:49:30.748060 |
| 2026-2027 | [constraint-breakdown-2026-2027.csv](https://api.neso.energy/dataset/fb56b46e-cef3-4eb8-9294-0ca19769b7eb/resource/4136a8e2-07c5-4784-8096-28999447a16e/download/constraint-breakdown-2026-2027.csv) | 9,519 | 184 | 2026-10-03T11:00:54.622473 |

- **gridflow captures the uploaded file** (`url_type: upload` on every resource), not a CKAN
  datastore dump, so the vintage is the sidecar `ckan_last_modified` and not a capture-time
  fallback (ADR-030, ADR-033). The catalogue marks every resource datastore-active; that does
  not change what is captured.
- **Vintages are uneven.** The 2017-18 and 2018-19 files carry vintages in August 2021, years
  after the dates they cover; the 2019-20 file's vintage is 2024-03-07; the 2020-21 file's is
  2021-06-09. Why NESO re-uploaded these when it did is not stated (`TODO: verify`). The
  vintage is the conservative availability bound, not the first time a number was public.
- **The catalogue `size` field is unreliable.** The 2024-25 resource lists `size` 10501 in the
  catalogue snapshot while the captured body is 18,384 bytes (the other nine list no size).
  The captured byte count is authoritative here; the cause of the mismatch is `TODO: verify`.

## Families

### `constraint_breakdown`

- Kind: tabular · archetype: SER · refresh: weekly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Date | `date` | date | `%Y-%m-%d` | no | — | ISO 8601 |
| Reducing largest loss cost | `reducing_largest_loss_cost_gbp` | float64 | — | yes | — | £ |
| Increasing system inertia cost | `increasing_system_inertia_cost_gbp` | float64 | — | yes | — | £ |
| Voltage constraints cost | `voltage_constraints_cost_gbp` | float64 | — | yes | — | £ |
| Thermal constraints cost | `thermal_constraints_cost_gbp` | float64 | — | yes | — | £ |
| Reducing largest loss volume | `reducing_largest_loss_volume_mwh` | float64 | — | yes | — | MWh |
| Increasing system inertia volume | `increasing_system_inertia_volume_mwh` | float64 | — | yes | — | MWh |
| Voltage constraints volume | `voltage_constraints_volume_mwh` | float64 | — | yes | — | MWh |
| Thermal constraints volume | `thermal_constraints_volume_mwh` | float64 | — | yes | — | MWh |

- Entity key: `resource_id`, `date`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: date_sp1 (`date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Eligible. Silver: 3,470 rows, 18 columns, from all ten resources.** All ten resources share
one header, so there is a single epoch (the header is the nine vendor columns above; the
transformer is the generic record-driven one, `transformer: null`). Measured on silver
(2026-10-10):

| Resource (financial year) | Rows | Dates | `published_at` = `available_at` |
|---|---:|---|---|
| 2017-18 | 365 | 2017-04-01 to 2018-03-31 | 2021-08-03T13:02:43.115452 |
| 2018-19 | 365 | 2018-04-01 to 2019-03-31 | 2021-08-03T12:58:42.610033 |
| 2019-20 | 366 | 2019-04-01 to 2020-03-31 | 2024-03-07T10:32:33.105338 |
| 2020-21 | 365 | 2020-04-01 to 2021-03-31 | 2021-06-09T14:57:07.736484 |
| 2021-22 | 365 | 2021-04-01 to 2022-03-31 | 2022-06-08T11:22:02.313951 |
| 2022-23 | 365 | 2022-04-01 to 2023-03-31 | 2023-04-06T15:50:32.383318 |
| 2023-24 | 366 | 2023-04-01 to 2024-03-31 | 2024-04-04T10:47:03.220307 |
| 2024-25 | 365 | 2024-04-01 to 2025-03-31 | 2025-06-16T14:51:46.011303 |
| 2025-26 | 364 | 2025-04-01 to 2026-03-31 (2025-04-08 absent) | 2026-04-07T09:49:30.748060 |
| 2026-27 | 184 | 2026-04-01 to 2026-10-01 | 2026-10-03T11:00:54.622473 |

Every `date` is unique across the whole silver set (3,470 distinct dates for 3,470 rows), so
no date appears in two resources and none twice in one. The files are disjoint annual
partitions. Nothing is null in any of the 18 columns. Every capture's `capture_written_at` is
2026-10-08 (09:15:12 to 09:15:38 UTC). `dataset_version` reads `1+e1` on every row (what `e1`
encodes is not established here: `TODO: verify`).

*The two clocks.*

1. **Vintage: `ckan_last_modified`.** `published_at` and `available_at` are the CKAN
   `last_modified` of the captured file, equal on every row (measured), and different per
   resource (listed above). They are not the capture time and not the date (ADR-030). An as-of
   query is `WHERE available_at <= :as_of`. There is no issue column (`issue.kind: none`), and
   none is invented: the data is retrospective outturn and mutable (the vendor note about
   post-event retagging).
2. **Event time: `date_sp1(date)`.** `timestamp_utc` and `event_time` are equal on every row
   (measured) and are the **start of settlement period 1 of the date, in GB local time, as UTC**.
   Measured: `2017-04-01` has `timestamp_utc` `2017-03-31T23:00Z` (BST, local midnight is 23:00
   UTC), `2026-09-30` has `2026-09-29T23:00Z`, and the spring clock-change day `2024-03-31` (the
   day still in GMT at midnight) has `2024-03-31T00:00Z`. It is a **day anchor, not an
   instant**: the cost and volume belong to the whole date. The anchor is an engine convention,
   not a vendor statement. The vendor says only that `Date` is "the date of the
   costs/volumes", so the exact daily accounting window (a GB-local settlement day, a UTC day,
   or another boundary) and its timezone are `TODO: verify`. The silver column `date` is the
   vendor date, unchanged. Capture time is in `capture_written_at`.

*Units (vendor dictionary only, as cited in the K-BAL-1 FACTS).* The four cost columns have
dictionary unit **£** and the four volume columns have dictionary unit **MWh**; `Date` has unit
`ISO 8601`. Units are never inferred from a column name. The dictionary does not say whether
the £ amounts are nominal or inflation-adjusted, whether they are net or gross of any
offsetting trades, or what the sign of a MWh volume means (`TODO: verify` each). The silver
column suffixes `_gbp` and `_mwh` are gridflow's labels for these dictionary units.

*Category meanings (vendor dictionary, paraphrased).*

| Category | What the vendor says it measures |
|---|---|
| Reducing largest loss | Trades and BM actions that reduce the generation, demand or interconnector flow that makes up the largest credible loss, which lowers the RoCoF that loss would cause. The dictionary gives the example of reducing output in one area while raising it elsewhere, or cutting an interconnector export and cutting generation to balance |
| Increasing system inertia | BM actions that raise synchronous generation, which increases inertia, the other lever for limiting RoCoF |
| Voltage constraints | Trades and BM actions that support reactive-power balance and regional voltage control |
| Thermal constraints | Trades and BM actions that manage flows exceeding the capacity of the circuits connecting two regions |

Each cost column covers the cost of those actions and each volume column their volume; the
vendor does not state which actions count as "trades" versus "BM actions" in the totals, nor
how an action is assigned to exactly one category (`TODO: verify`; the retagging note suggests
the assignment is a tag applied to each action).

*Sentinels and missing values (FACTS g5).* NESO declares no null token for this package. No
blank, `NA`, `N/A` or uncastable value occurs in any body, so no cell is null in silver (the
columns are nullable in the record, but none is null). **Zero is a stated zero** and **`-1` is a
stated `-1`**: the vendor defines neither as missing, so nothing is converted to null. Measured
on silver across all 3,470 dates:

| Column | Cells equal to 0 | Cells below 0 |
|---|---:|---:|
| `reducing_largest_loss_cost_gbp` | 1,813 | 17 |
| `increasing_system_inertia_cost_gbp` | 2,303 | 8 |
| `voltage_constraints_cost_gbp` | 386 | 20 |
| `thermal_constraints_cost_gbp` | 352 | 5 |
| `reducing_largest_loss_volume_mwh` | 1,813 | 1,603 |
| `increasing_system_inertia_volume_mwh` | 2,288 | 34 |
| `voltage_constraints_volume_mwh` | 371 | 30 |
| `thermal_constraints_volume_mwh` | 352 | 2,844 |

- **Reducing largest loss is zero for whole years.** Every cost and volume cell of that
  category is exactly zero in the 2024-25, 2025-26 and 2026-27 resources, and 365 of the 366
  rows in 2023-24 (the one non-zero date has a negative cost). The longest consecutive zero run
  in any single body is 365 rows (FACTS g5). A fully zero column is a vendor value, not missing
  data, and must not be nulled. Whether it means "the lever was not used" or "the category was
  not populated" is `TODO: verify` with NESO.
- **Four thermal volume cells are exactly `-1`**, on 2017-12-18, 2019-01-06, 2019-05-13 and
  2021-09-16. They sit among values in the tens of thousands (the thermal volume on 2026-09-30
  is -99,478 MWh) and the vendor does not define `-1` as a flag; they are preserved as
  published (`TODO: verify` whether they are real near-zero volumes, rounding artefacts or a
  placeholder).
- Negative costs (50 across the four cost columns) are kept as published. The vendor gives no
  explanation (`TODO: verify` whether they are credits, re-attributions or corrections).

*Sample silver row (2026-09-30, non-held family, values as published).*
`date` 2026-09-30; `reducing_largest_loss_cost_gbp` 0; `increasing_system_inertia_cost_gbp` 0;
`voltage_constraints_cost_gbp` 164,088; `thermal_constraints_cost_gbp` 35,516,446;
`reducing_largest_loss_volume_mwh` 0; `increasing_system_inertia_volume_mwh` 0;
`voltage_constraints_volume_mwh` 16,885; `thermal_constraints_volume_mwh` -99,478;
`resource_id` `4136a8e2-07c5-4784-8096-28999447a16e`; `timestamp_utc` / `event_time`
2026-09-29T23:00Z; `published_at` / `available_at` 2026-10-03T11:00:54.622473Z. Lineage columns
appended to the nine vendor columns: `resource_id`, `timestamp_utc`, `published_at`,
`bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id`,
`dataset_version`. All timestamps are tz-aware UTC.

*Identity and selection.* Each capture is a whole file, so the record sets `latest` to
`whole_capture` partitioned by `resource_id` (`latest_partition: resource_id`): the ten
partitions are independent, and a later NESO re-upload of any resource adds a new whole capture
that `_latest` takes for that resource only. A family-wide newest-capture rule would have kept
just one year (ADR-039). The candidate key `date` is unique within every resource and across
resources in the complete bodies (no duplicates, no overlap); the entity key is
`resource_id, date`. NESO states no uniqueness guarantee (`TODO: verify` vendor identity
guarantee); it affects nothing today because selection is by whole capture, not by key. The
silver Parquet files are under `C:/gridflow-data/silver/neso_data_portal/constraint_breakdown/year=2026/month=10/`,
one file per capture; the `year=`/`month=` partition is the **capture** date, not the data date.

*The missing day.* The 2025-26 body has no row for 2025-04-08 (364 rows). Bronze and silver
agree, and it is the only gap in the 3,470-date series. Whether NESO omitted the day or had
nothing to report is `TODO: verify`; zero is a stated value in this series, so do not zero-fill.

*The open year.* The 2026-27 file ended at 2026-10-01 at its 2026-10-03 vintage (it lags the
vintage by two days). A later refresh will re-upload the same resource with a new
`last_modified`, adding a new whole capture that supersedes this one for that resource
(`TODO: verify` that NESO updates the same resource id rather than adding a new one). The
2027-28 resource does not exist yet and would need a new registry resource entry.

*Relation to the thermal cost package.* @./thermal-constraint-costs.md publishes a daily
thermal cost per named boundary group (six groups). Over the 1,644 dates present in both silver
sets (2022-04-01 onward), the sum of that package's six groups equals this package's
`thermal_constraints_cost_gbp` on only 173 dates (176 within £1). The two are not the same
quantity or are on different bases; how they relate is `TODO: verify` with NESO. Do not use one
to fill or check the other.

## Cadence

- Registry refresh: weekly
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Weekly

The weekly statement is the vendor's. The captured vintages show the older years' files last
changed between 2021 and 2026 (2017-18 and 2018-19 on 2021-08-03; 2019-20 on 2024-03-07;
2020-21 on 2021-06-09; 2021-22 on 2022-06-08; 2022-23 on 2023-04-06; 2023-24 on 2024-04-04;
2024-25 on 2025-06-16; 2025-26 on 2026-04-07) and the open 2026-27 file last changed on
2026-10-03, which is consistent with a weekly update of the current year and occasional
re-uploads of older years. Gridflow captured every resource once, on 2026-10-08, from the
portal sweep; the activation window was 2026-10-08 to 2026-10-10. A scheduled weekly re-ingest
would add a new capture of the 2026-27 file and leave the others unchanged unless NESO
re-uploads them.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence)
(CKAN licence id `ESO`). gridflow outputs derived from this package carry the attribution line
above.

## Holds

- none

No family output and no resource is held: the record is eligible and all ten resources route to
silver. There is no E-SEM question open on this package.

**Activation (2026-10-10, master `1ccb467`, PR #106, balancing-costs batch).** The frozen
records merged triple-green (CI green twice, Sol diff review APPROVE on pass 1 with no
findings, VERIFICATION passed at head `3a7907a`; RULINGS 655) and were activated with window
2026-10-08 to 2026-10-10, no prior silver, nothing overwritten (RULINGS 656). The real-body
row count was 3,470, equal to the plan, with no transform errors and no exclusions. Reconcile
`--all --cutoff 2026-10-10` exited 0 (122 families, 0 gaps, 23 adjudicated across all families, 0 stale). No engine, reader or record-model change was needed for this
family (gridflow `@.planning/v0.22-RESULTS.md`, section BAL-1). RULINGS 653 records the
decisions for the batch.

No gold view or model consumes this package as of 2026-10-10 (RULINGS 657: no balancing-costs
batch package feeds the gold views or the models).

References: gridflow `@.planning/phases/v0.22-K-BAL-1/K-BAL-1-FACTS.md`,
`@.planning/phases/v0.22-K-BAL-1/VERIFICATION.md`, `@.planning/RULINGS.md` (653, 655, 656,
657), `@.planning/v0.22-RESULTS.md`,
`@src/gridflow/connectors/neso_data_portal/registry/constraint-breakdown.json`,
`@docs/neso_data_portal/eligibility.md`,
`@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`,
`@docs/DECISION_LOG/ADR-033-neso-registry-upload-leg.md` and
`@docs/DECISION_LOG/ADR-039-neso-multi-resource-selection.md`.
