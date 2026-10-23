---
source: "neso_data_portal"
package: "system-operating-plan-sop"
dataset_key: "system_operating_plan"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-09
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# System Operating Plan (SOP)

NESO's **System Operating Plan**: a planning snapshot that the control-room strategy team
produces for each key demand peak or trough of the day (a **cardinal point**, CP) and hands to
the real-time team. One row is the plan for one cardinal point. It records the expected demand
at that point, the reserve the plan requires and has available, two maximum-loss columns
(`maximum_loss_generation`, `maximum_loss_demand`; TODO: verify their meaning with NESO — not
defined in the dictionary), the resulting margins and residuals, and, for each generation
technology and each interconnector, three expected figures (see Units). The vendor says the SOP
is a snapshot of what the control room knew when the plan was created, and that the real-time
team keeps reviewing and, if needed, modifies the plan as the cardinal point approaches. So a
row is a **plan, not a measurement**: it is not an outturn, and it can later be revised.

The vendor aims to publish the plans for cardinal points `1A`, `1B`, `2F`/`2A`/`2B` (whichever
is the morning peak), `3B`, `3C` and `4B` each day, ahead of the cardinal point. The captured
body also carries other cardinal-point labels (see Row meaning), and its spacing is irregular,
so it is **not** a regular hourly or settlement-period series.

**The output is held (unit E-SEM).** The dump returns each plan's **latest version**, and NESO
does not state that a returned version's values were fixed and public at the plan's creation
time. Every target also precedes the capture, so the forward-target rule (RULINGS 529) cannot
release it. The output exists in silver, but it is not eligible for publication or
point-in-time model use until E-SEM is answered (RULINGS 569, 571, 579, 580). **This page gives
schema, clocks and row counts only, and no data values.**

Related pages: @brit-ned.md and @interconnector-register.md cover BritNed and the
interconnectors, whose expected flows appear here as triplets named after each link. Those
triplets are expected reference-program flows. They are **not** NESO's directional transfer
limits (those are in the interconnector limit packages such as @ifa.md).

- Publisher group: System
- Registry group: system · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| System Operating Plan - Data Table | CSV | dump | `e51f2721-00ab-4182-9cae-3c973e854aa8` |

### DOC

| Resource | Format | Capture | Id |
|---|---|---|---|
| An Introduction to System Operator Plans | PDF | upload | `8be74d9e-9f41-4ab7-8606-2c06d60cb63d` |
| Glossary of terms used in System Operating Plan | PDF | upload | `596fbeb4-77be-48a4-89b7-f442e73e54c0` |

Package id `99442aab-b184-44f5-8495-fc0b82869d46`. Package CKAN `metadata_modified`
`2026-10-06T19:30:14.075416`; package created `2020-06-05`. The package has three resources
and one SILVER resource.

- **System Operating Plan - Data Table** -> `system_operating_plan` (held).
  Download: [datastore dump](https://api.neso.energy/datastore/dump/e51f2721-00ab-4182-9cae-3c973e854aa8).
  Captured: `raw_20261008T113818Z_e51f2721-00ab-4182-9cae-3c973e854aa8_92dcd12f.csv`,
  4,326,360 bytes, 10,322 rows, 93 columns, `datastore` (dump, one page). CKAN `last_modified`
  `2023-01-24T00:30:04.725185`; resource created `2020-09-30`; resource `metadata_modified`
  `2026-10-06T19:30:14.075416`. The capture sidecar records the package-side
  `ckan_metadata_modified` as `2026-10-08T05:50:10.663089`.
- **An Introduction to System Operator Plans** -> `system_operating_plan_files` (DOC).
  Download: [an-introduction-to-system-operator-plans.pdf](https://api.neso.energy/dataset/99442aab-b184-44f5-8495-fc0b82869d46/resource/8be74d9e-9f41-4ab7-8606-2c06d60cb63d/download/an-introduction-to-system-operator-plans.pdf).
  Captured: `raw_20261008T113823Z_8be74d9e-9f41-4ab7-8606-2c06d60cb63d_a0e64a68.pdf`,
  140,612 bytes. CKAN `last_modified` `2025-11-06T13:57:34.532638`; resource created
  `2020-06-25`. Vendor description: introduces SOPs and gives guidance to support
  understanding a SOP.
- **Glossary of terms used in System Operating Plan** -> `system_operating_plan_files` (DOC).
  Download: [glossary-of-terms-used-in-a-system-operating-plan.pdf](https://api.neso.energy/dataset/99442aab-b184-44f5-8495-fc0b82869d46/resource/596fbeb4-77be-48a4-89b7-f442e73e54c0/download/glossary-of-terms-used-in-a-system-operating-plan.pdf).
  Captured: `raw_20261008T113822Z_596fbeb4-77be-48a4-89b7-f442e73e54c0_c57603fd.pdf`,
  174,338 bytes. CKAN `last_modified` `2025-11-06T13:57:58.053642`; resource created
  `2020-06-05`. Vendor description: supports understanding of the System Operating Plan.

The two PDFs are retained as immutable bronze documents with their provenance. They are
**DOC**: catalogue only, with no schema, temporal recipe, issue key or silver output. The PDF
contents were not read as evidence for this page, so term definitions below come from the
vendor's field dictionary only. `TODO: verify` any term against the Glossary PDF before relying
on it.

## Families

### `system_operating_plan`

- Kind: tabular · archetype: FC · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| sop_datetime | `sop_datetime` | datetime | `%Y-%m-%dT%H:%M:%S` | no | UTC | UTC ISO 8601 |
| report_date | `report_date` | date | `%Y-%m-%dT%H:%M:%S` | yes | — | — |
| latest_version | `latest_version` | int64 | — | yes | — | — |
| latest_status | `latest_status` | string | — | yes | — | — |
| cardinal_point | `cardinal_point` | string | — | yes | — | — |
| customer_demand_forcast | `customer_demand_forcast` | float64 | — | yes | — | MW |
| station_transformer | `station_transformer` | float64 | — | yes | — | MW |
| dsbr | `dsbr` | float64 | — | yes | — | MW |
| total_sop_demand | `total_sop_demand` | float64 | — | yes | — | MW |
| standing_reserve_requirement | `standing_reserve_requirement` | float64 | — | yes | — | MW |
| standing_reserve_availability | `standing_reserve_availability` | float64 | — | yes | — | MW |
| standing_reserve_shortfall | `standing_reserve_shortfall` | float64 | — | yes | — | MW |
| standing_reserve_excess | `standing_reserve_excess` | float64 | — | yes | — | MW |
| standing_res_wind_adj | `standing_res_wind_adj` | float64 | — | yes | — | MW |
| net_positive_regulating_reserve | `net_positive_regulating_reserve` | float64 | — | yes | — | MW |
| positive_reg_res_wind_adj | `positive_reg_res_wind_adj` | float64 | — | yes | — | MW |
| reserve_for_response | `reserve_for_response` | float64 | — | yes | — | MW |
| total_positive_reserve | `total_positive_reserve` | float64 | — | yes | — | MW |
| percentage_of_standing_reserve_excess | `percentage_of_standing_reserve_excess` | float64 | — | yes | — | MW |
| net_negative_regulating_reserve | `net_negative_regulating_reserve` | float64 | — | yes | — | MW |
| negative_reg_res_wind_adj | `negative_reg_res_wind_adj` | float64 | — | yes | — | MW |
| negative_response_reserve | `negative_response_reserve` | float64 | — | yes | — | MW |
| total_negative_reserve | `total_negative_reserve` | float64 | — | yes | — | MW |
| maximum_loss_generation | `maximum_loss_generation` | float64 | — | yes | — | MW |
| maximum_loss_demand | `maximum_loss_demand` | float64 | — | yes | — | MW |
| positive_residual | `positive_residual` | float64 | — | yes | — | MW |
| imbalance | `imbalance` | float64 | — | yes | — | MW |
| negative_residual | `negative_residual` | float64 | — | yes | — | MW |
| sop_report_creation_time_gmt | `sop_report_creation_time_gmt` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | UTC ISO 8601 |
| sop_d_and_c_time_gmt | `sop_d_and_c_time_gmt` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | UTC ISO 8601 |
| contingency_requirement | `contingency_requirement` | float64 | — | yes | — | MW |
| operating_margin_surplus | `operating_margin_surplus` | float64 | — | yes | — | MW |
| trigger_level | `trigger_level` | float64 | — | yes | — | MW |
| no1_temx | `no1_temx` | float64 | — | yes | — | MW |
| no1_teol | `no1_teol` | float64 | — | yes | — | MW |
| no1_temi | `no1_temi` | float64 | — | yes | — | MW |
| nw1_temx | `nw1_temx` | float64 | — | yes | — | MW |
| nw1_teol | `nw1_teol` | float64 | — | yes | — | MW |
| nw1_temi | `nw1_temi` | float64 | — | yes | — | MW |
| so1_temx | `so1_temx` | float64 | — | yes | — | MW |
| so1_teol | `so1_teol` | float64 | — | yes | — | MW |
| so1_temi | `so1_temi` | float64 | — | yes | — | MW |
| sw1_temx | `sw1_temx` | float64 | — | yes | — | MW |
| sw1_teol | `sw1_teol` | float64 | — | yes | — | MW |
| sw1_temi | `sw1_temi` | float64 | — | yes | — | MW |
| britned_temx | `britned_temx` | float64 | — | yes | — | MW |
| britned_teol | `britned_teol` | float64 | — | yes | — | MW |
| britned_temi | `britned_temi` | float64 | — | yes | — | MW |
| ewic_temx | `ewic_temx` | float64 | — | yes | — | MW |
| ewic_teol | `ewic_teol` | float64 | — | yes | — | MW |
| ewic_temi | `ewic_temi` | float64 | — | yes | — | MW |
| france_temx | `france_temx` | float64 | — | yes | — | MW |
| france_teol | `france_teol` | float64 | — | yes | — | MW |
| france_temi | `france_temi` | float64 | — | yes | — | MW |
| intifa2_temx | `intifa2_temx` | float64 | — | yes | — | MW |
| intifa2_teol | `intifa2_teol` | float64 | — | yes | — | MW |
| intifa2_temi | `intifa2_temi` | float64 | — | yes | — | MW |
| moyle_temx | `moyle_temx` | float64 | — | yes | — | MW |
| moyle_teol | `moyle_teol` | float64 | — | yes | — | MW |
| moyle_temi | `moyle_temi` | float64 | — | yes | — | MW |
| nemo_temx | `nemo_temx` | float64 | — | yes | — | MW |
| nemo_teol | `nemo_teol` | float64 | — | yes | — | MW |
| nemo_temi | `nemo_temi` | float64 | — | yes | — | MW |
| ps_temx | `ps_temx` | float64 | — | yes | — | MW |
| ps_teol | `ps_teol` | float64 | — | yes | — | MW |
| ps_temi | `ps_temi` | float64 | — | yes | — | MW |
| sto_temx | `sto_temx` | float64 | — | yes | — | MW |
| sto_teol | `sto_teol` | float64 | — | yes | — | MW |
| sto_temi | `sto_temi` | float64 | — | yes | — | MW |
| sb_temx | `sb_temx` | float64 | — | yes | — | MW |
| sb_teol | `sb_teol` | float64 | — | yes | — | MW |
| sb_temi | `sb_temi` | float64 | — | yes | — | MW |
| total_temx | `total_temx` | float64 | — | yes | — | MW |
| total_teol | `total_teol` | float64 | — | yes | — | MW |
| total_temi | `total_temi` | float64 | — | yes | — | MW |
| INTNSL_temx | `intnsl_temx` | float64 | — | yes | — | MW |
| INTNSL_teol | `intnsl_teol` | float64 | — | yes | — | MW |
| INTNSL_temi | `intnsl_temi` | float64 | — | yes | — | MW |
| INTELEC_temx | `intelec_temx` | float64 | — | yes | — | MW |
| INTELEC_teol | `intelec_teol` | float64 | — | yes | — | MW |
| INTELEC_temi | `intelec_temi` | float64 | — | yes | — | MW |
| BAT_temx | `bat_temx` | float64 | — | yes | — | MW |
| BAT_teol | `bat_teol` | float64 | — | yes | — | MW |
| BAT_temi | `bat_temi` | float64 | — | yes | — | MW |
| SLR_temx | `slr_temx` | float64 | — | yes | — | MW |
| SLR_teol | `slr_teol` | float64 | — | yes | — | MW |
| SLR_temi | `slr_temi` | float64 | — | yes | — | MW |
| INTGRNL_temx | `intgrnl_temx` | float64 | — | yes | — | Mw |
| INTGRNL_teol | `intgrnl_teol` | float64 | — | yes | — | MW |
| INTGRNL_temi | `intgrnl_temi` | float64 | — | yes | — | MW |
| INTVKL_temx | `intvkl_temx` | float64 | — | yes | — | MW |
| INTVKL_teol | `intvkl_teol` | float64 | — | yes | — | MW |
| INTVKL_temi | `intvkl_temi` | float64 | — | yes | — | MW |

- Entity key: `issue_time`, `sop_datetime`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`sop_datetime`)

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

**Held (unit E-SEM). This page gives schema, clocks and counts only, and no data values.**

**Shape of the silver output (counts only).** One bronze capture (`2026-10-08`, 93 vendor
columns) became one silver Parquet of **10,322 rows and 102 columns** (activation cutoff
`2026-10-08`, RULINGS 580; no earlier silver). Silver path pattern:
`silver/neso_data_portal/system_operating_plan/year=YYYY/month=MM/…parquet`. The 102 columns are
the 93 vendor columns above plus nine gridflow columns: `issue_time`, `timestamp_utc`,
`published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`,
`source_run_id` and `dataset_version`. In the captured body, `issue_time` equals
`sop_report_creation_time_gmt`, and `timestamp_utc` and `event_time` both equal `sop_datetime`,
on every row.

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`, not used as availability).** The registry vintage is
   `capture_fallback`: `published_at` is null and `available_at` is the **capture time**
   (sidecar `written_at`), here `2026-10-08T11:38:18.294948Z`, on every row. The capture's CKAN
   `last_modified` is `2023-01-24T00:30:04.725185`. gridflow records it in the sidecar but
   **does not use it as `available_at`**: the body holds plans created long after that
   instant, so that field is stale for this resource and says nothing about when a given plan
   became public (K-IC-2-FACTS IC2-3 T08; gridflow `@docs/DECISION_LOG/ADR-035` datastore
   vintage). The plan's own creation time (`sop_report_creation_time_gmt`, carried as
   `issue_time`) is kept as an **issue label** and is part of the entity key, but it is not
   evidenced as the instant the values were public. Do not substitute either field for
   `available_at`.
2. **Event time (`utc_instant` on `sop_datetime`).** `timestamp_utc` = `event_time` =
   `sop_datetime`, the UTC instant the plan is **for** (the cardinal point). It is a point
   target, not an evidenced interval start or end. It is not the creation time. The format is
   `%Y-%m-%dT%H:%M:%S`, read as UTC.

Time columns (all four parse strictly with no nulls and no invalid cells in the captured body):

| Column | Role | Coverage in the captured body |
|---|---|---|
| `sop_datetime` | UTC target instant (event time) | 2020-09-30 to 2026-10-08 |
| `report_date` | Date label; vendor-typed date, serialised at midnight | 2020-02-10 to 2026-10-08 |
| `sop_report_creation_time_gmt` | UTC creation instant (issue label) | 2020-09-30 to 2026-10-08 |
| `sop_d_and_c_time_gmt` | UTC time of the demand-and-constraint process run; not a publication instant | 2020-09-30 to 2026-10-08 |

Every target in the captured body follows its recorded creation time, but every target precedes
the capture. So all rows are past targets at capture, and the ordering of target after creation
does **not** show that the returned version's values were public at creation.

**Row meaning and vocabulary.** One row is the latest version of the SOP for one cardinal point.
`latest_version` is a unitless version counter (integer, starting at one). `latest_status` and
`cardinal_point` are categorical text. Observed `latest_status` values are `Final`, `Revised`
and `Day Ahead`. The vendor dictionary says the status should be final, so the other values are
kept as published. Observed `cardinal_point` labels are `1A`, `1B`, `1S`, `2A`, `2B`, `2F`, `3B`,
`3C`, `4B`, `DP` and `Fix`. Spellings are kept as published. `TODO: verify` the meaning of
`1S`, `DP` and `Fix` with NESO, because the vendor notes name only `1A`, `1B`, `2F`/`2A`/`2B`,
`3B`, `3C` and `4B`.

**Key.** In the captured body `sop_datetime` alone is unique (one row per target), and
`(issue_time, sop_datetime)` is unique, with no exact duplicate rows. The registry key includes
`issue_time` because the family declares an issue (gridflow contract: `issue_time` belongs in the
key exactly when an issue is declared). The key is a gridflow guard. `TODO: verify` NESO's
identity and revision guarantee for a plan (CKAN declares no datastore primary key that was
inspected).

**Units (vendor dictionary only).** The frozen vendor field dictionary assigns **MW** to every
physical-value column in the table above. Nothing here is inferred from a column name.

- One dictionary spelling differs: `INTGRNL_temx` is listed as `Mw`. The unit is read as MW
  because every sibling column is MW.
- `percentage_of_standing_reserve_excess` is documented as **MW**, not percent, despite its
  name. The name suggests a ratio, so `TODO: verify` this unit with NESO before using the
  column as a percentage.
- `latest_version` has no unit. `latest_status` and `cardinal_point` are text. The date and
  time columns carry no power unit.
- The `*_temx`, `*_teol` and `*_temi` triplets are, in general, the plan's expected maximum
  availability, expected output and expected minimum output for that technology. The
  dictionary gives technology-specific exceptions (for example battery minimum import, and the
  solar minimum definition). Read the dictionary entry for a column before interpreting it.
  `TODO: verify` each exception against the Glossary PDF.
- For the interconnector triplets (`britned_`, `ewic_`, `france_`, `intifa2_`, `moyle_`,
  `nemo_`, `intnsl_`, `intelec_`, `intgrnl_`, `intvkl_`) the figures are expected
  reference-program flows. Sign convention: `TODO: verify` with NESO.
- `dsbr` is marked obsolete in the vendor dictionary, but it is present in the body.

**Missing values and sentinels (FACTS g5).** The body has many blank cells, many literal numeric
zero cells and some literal numeric `-1` cells in physical-value columns. It has no literal
`NA` or `N/A` cells. The vendor supplies **no** missing-value or not-applicable convention for
the value columns, and no global `-1` sentinel rule. gridflow therefore keeps blanks as null,
and keeps zero and `-1` as the published numbers: **no value is replaced, dropped or reinterpreted**.
A blank, a zero and a `-1` are three different facts, and the page does not say what any of them
means for a given column. `TODO: verify` column-specific missing and not-applicable conventions
with NESO. Long runs of consecutive zero rows exist in some columns. They are row runs in an irregularly spaced series, not
durations. Counts per column are not published here because the family is held.

**Quality notes.**

- `report_date` is a vendor date label, not an issue or target time. In the captured body it
  often differs from the creation date, and in a small number of rows (four) it also differs
  from the target date. No date swap or correction is applied. `TODO: verify` the meaning of
  `report_date` with NESO (the dictionary describes a creation date).
- The package page shows two vendor notices: one about the **quality** of the published SOP
  data, and one about **technical difficulties in publishing** it, with updates to resume when
  the issue is fixed. Recent rows and package metadata show content up to the capture date, but
  they do not prove uninterrupted daily publication or that the notices are resolved.
- The resource's CKAN `last_modified` (`2023-01-24`) is far older than the newest rows in the
  body. Do not use it to judge freshness.

**Hold question (unit E-SEM).** The dump returns each plan's latest version. NESO does not state
that a returned version's values were fixed and public at the plan's creation time, and every
target precedes the capture, so the forward-target rule (RULINGS 529) cannot apply. The hold is
released only when NESO supplies evidence that each returned version's values were fixed and
publicly available at its recorded issue instant, or successive immutable captures document the
actual revision behaviour. `TODO: verify` the operational publication status and the revision
retention guarantee with NESO.

### `system_operating_plan_files`

- Kind: files · archetype: FC · refresh: daily · empty allowed: no
- files: catalogue only

This family holds the two DOC PDFs listed above. It has no schema, temporal recipe, issue key
or silver output. Each captured PDF keeps its provenance sidecar (capture time, CKAN
`last_modified`, SHA-256). Both are `upload` resources.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Daily

The vendor says it aims to publish the day's plans for the cardinal points listed in the
overview ahead of each cardinal point, which matches the "Daily" frequency. The vendor also
shows the two notices above. `TODO: verify` the actual publication schedule and whether
updates are paused. gridflow's daily refresh captures one state per run, and each capture
replaces the family as a whole. The dated silver captures are therefore a sample of the vendor's
state, not a revision history of any one plan. Captures are on demand. The one local capture is
dated `2026-10-08`.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above. Package page:
[System Operating Plan (SOP)](https://www.neso.energy/data-portal/system-operating-plan-sop).

## Holds

- `system_operating_plan`: held: TODO: the dump returns each plan's latest version and NESO does not state that its values are fixed and public at their creation time, and every target precedes the capture, so the forward-target rule (RULINGS 529) cannot apply. (unit E-SEM)

The held output exists in silver but is not eligible for publication or point-in-time model use
until unit E-SEM answers its question (RULINGS 569, 571, 579, 580). This page publishes its
schema, clocks and row counts only. No data value, sample row or value statistic is published
here. The hold applies to the captured body and to later captures unless NESO supplies the
missing evidence. The DOC family `system_operating_plan_files` is not held: it is catalogue
only.
