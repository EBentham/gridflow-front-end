---
source: "neso_data_portal"
package: "stability-midterm-y-1-utilisation-report"
dataset_key: "stability_midterm_y1"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-10
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Stability midterm (Y-1) utilisation report

Delivered-utilisation report for NESO's stability midterm (Y-1) service: one row per
instructed interval in which a contracted balancing-mechanism unit (BMU) was utilised to
provide system inertia, with the unit's contracted inertia, the start and end of the interval,
and a duration text. The vendor describes the report as published after settlement payments,
covering utilisation that was actually delivered (gridflow
`@.planning/phases/v0.22-K-SYS-1/K-SYS-1-FACTS.md` section 3, g2). It is an **outturn
record**, not a forecast: there is no forecast column. Use it to see which units NESO
utilised for inertia, when, and how much contracted inertia each carried. It pairs with the
system-wide inertia series (@system-inertia.md) and the Pathfinder reports
(@stability-pathfinder-service-information.md), which describe the same stability-service
space at different grains and are not interchangeable with it. The grain here is an
**instructed interval**, not a settlement period.

`TODO: verify` what "midterm" and "Y-1" denote in the vendor's service design (the
inspected sources describe the report but do not define the service names).

- Publisher group: System
- Registry group: system · archetype: SER

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Stability midterm (Y-1) utilisation report 25/26 | CSV | upload | `e0c86d21-8ad1-4ba3-a112-b2bbcf5277ce` |

- Stability midterm (Y-1) utilisation report 25/26 → `stability_midterm_y1`.
  Download: [stability.csv](https://api.neso.energy/dataset/84abeae2-be21-4755-bbfc-3792f5315a36/resource/e0c86d21-8ad1-4ba3-a112-b2bbcf5277ce/download/stability.csv)
  (CKAN `last_modified` 2026-09-28T16:54:21.377483 at capture).
  Captured: `raw_20261008T112705Z_e0c86d21-8ad1-4ba3-a112-b2bbcf5277ce_998df585.csv`,
  3,950 bytes, 61 data rows, one header epoch, CRLF line endings, UTF-8, no BOM.
- The package has a single resource and no DOC files. The label "25/26" suggests a
  financial-year resource, but the file was captured as the only resource of the package, so
  `TODO: verify` how NESO will publish later years (a new resource, a replaced file, or an
  appended file). The record is `whole_capture`, so any of these lands as a fresh capture.

## Families

### `stability_midterm_y1`

- Kind: tabular · archetype: SER · refresh: monthly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| BMU ID | `bmu_id` | string | — | no | — | BMUID-1 |
| Inertia (in MVA.s) | `inertia_mva_s` | float64 | — | yes | — | MVA.s |
| Month & Year | `month_and_year` | date | `%b-%y` | yes | — | — |
| Utilisation Start Datetime | `utilisation_start_datetime` | datetime | `%d/%m/%Y %H:%M` | no | UTC | — |
| Utilisation End Datetime | `utilisation_end_datetime` | datetime | `%d/%m/%Y %H:%M` | no | UTC | — |
| Hours Utilised | `hours_utilised` | string | — | yes | — | Hours and Minutes |

- Entity key: `bmu_id`, `utilisation_start_datetime`, `utilisation_end_datetime`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`utilisation_start_datetime`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

Silver adds the standard provenance columns after the six vendor columns: `timestamp_utc`,
`published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`,
`source_run_id`, `dataset_version`. Silver holds **61 rows** (one capture, window
2026-10-08, activated under RULINGS 647, no prior silver; `@.planning/v0.22-RESULTS.md`
section SYS-1). Zero rows were excluded. Row count equals the bronze body, as the SYS-1
verification confirmed (@.planning/phases/v0.22-K-SYS-1/VERIFICATION.md).

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured resource. For the one capture to date that is
   `2026-09-28T16:54:21.377483`, which CKAN emits without an offset; gridflow reads it as UTC
   (@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md). All 61 silver rows share
   this one vintage (checked in silver on 2026-10-10). The file has **no issue column**, so
   the record's issue recipe is `none`. Nothing establishes that a row was publicly
   available when the utilisation was instructed. The vendor describes publication after
   settlement payments, so the vintage is the only honest availability claim.
2. **Event time (`utc_instant` on `utilisation_start_datetime`).** `timestamp_utc` =
   `event_time` = the interval's **start** instant. This was checked equal to
   `utilisation_start_datetime` on all 61 silver rows on 2026-10-10. Event time is therefore
   **not** the capture time and not a settlement-period start. It is a real instant, because
   the vendor dictionary states that both boundary columns are "given in GMT". A fixed GMT
   clock is typed as UTC with no London DST conversion (FACTS T01-T03). The end boundary
   stays a separate column; the interval is `[start, end]`.

**Column notes**

- `bmu_id`: stored as supplied (project identifier rule: no normalisation). Silver holds 4
  distinct BMU IDs across the 61 rows. The vendor dictionary describes it as the unique ID
  for the Balancing Mechanism Units and lists its unit field as `BMUID-1`; that is an
  identifier-format label, not a physical unit. `TODO: verify` what `BMUID-1` denotes.
- `inertia_mva_s`: the contracted inertia of the utilised unit, vendor unit **MVA.s**.
  float64; no nulls in the captured body. Unit comes from the vendor dictionary, not from
  the column name.
- `month_and_year`: a reporting/utilisation-month **label** (`Oct-25` style, vendor example
  `Jul-25`), parsed `%b-%y` to the first of the month. It is not forced to equal the month of
  the start instant: **3** of the 61 rows carry a label for a later month than their start
  (for example, a row starting `28/04/2026 22:44` labelled `May-26`). Silver holds 7
  distinct labels: 2025-10, 2025-11 and 2026-04 to 2026-08. Do not derive the label from the
  start, and do not join on it as if it were the start month.
- `utilisation_start_datetime` / `utilisation_end_datetime`: `%d/%m/%Y %H:%M`, UTC. Captured
  starts run from 2025-10-04 21:12 to 2026-08-29 22:47 UTC and ends reach 2026-08-31 14:53
  UTC. No row ends before it starts.
- `hours_utilised`: the vendor duration, kept as a **string**. Vendor unit is "Hours and
  Minutes" and the vendor example is `08:30:00`. The captured values are `HH:MM:SS` text
  (48 rows) or a two-component form (13 rows), and hours can exceed a clock-day range.
  Never converted to a number or recomputed from the boundaries: on **4** rows the stated
  duration disagrees with the boundary difference (file lines 5, 7, 8 and 9). Treat the
  boundaries as the interval and the text as the vendor's own claim. See Holds.

**Sentinels and missing values (g5).** None found. The body has no blanks, `-1`, `N/A` or
`NA` literals and no zero inertia. Inertia values have no lexical thousands separators,
currency symbols or percent signs; every value casts to float64. No sentinel handling is
configured and none is needed. Should a later capture introduce one, it must be adjudicated
explicitly rather than nulled silently.

**Keys.** The key `(bmu_id, utilisation_start_datetime, utilisation_end_datetime)` is
unique in the capture (61 distinct of 61); `(bmu_id, start)` and `start` alone are also
unique here. The wider key describes an instructed interval faithfully without claiming a
vendor uniqueness guarantee. `TODO: verify` whether NESO guarantees a primary key.

## Cadence

- Registry refresh: monthly
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Monthly
- Only one capture exists (2026-10-08). `TODO: verify` whether a monthly upload appends to
  the file, replaces it, or adds a resource; the record is `whole_capture`, so `_latest`
  serves the newest whole upload and older uploads remain reachable by vintage.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

## Holds

- none. The resource is SILVER and the family is eligible (`@docs/neso_data_portal/eligibility.md`).
  Nothing in this package is held, failed or adjudicated. The six ADR-040 failed entries
  and the held outputs in the SYS-1 batch belong to the two Pathfinder families, not this
  one (RULINGS 642).
- Open vendor questions (not holds; they do not block the faithfully retained data):
  - `TODO: verify` MIDTERM-DURATION: the format and rounding of `Hours Utilised` and the 4
    rows where it disagrees with the boundary difference. This is why the column stays a
    string.
  - `TODO: verify` T04: the vendor's primary-key guarantee (see Keys).
  - `TODO: verify` whether the dataset's monthly refresh replaces or extends the file.
