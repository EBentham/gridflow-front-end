---
source: "neso_data_portal"
package: "monthly-operational-metered-wind-output"
dataset_key: "metered_wind_output_monthly"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-09
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Monthly operational metered wind output

NESO's **metered wind output in MW for Scotland, England, and Wales** (vendor wording), at
half-hour resolution. Each row is one settlement date and settlement period and gives three numbers: Scottish wind
output, England/Wales wind output and their total, all in MW. The package notes describe it as
"Metered wind output in MW for Scotland, England, and Wales", provided per date per settlement
period ([package page](https://www.neso.energy/data-portal/monthly-operational-metered-wind-output)).

The figures come from **operational metering**, not settlement metering. The package notes warn
that they are "expected to be different to the data published as part of the wind forecasting
metrics", because those metrics use settlement metering, which is reconciled later. Use this
family as a quick, regional view of metered wind output. Possible uses (the author's suggestion,
not vendor text) are wind-forecast error analysis (against @14-days-ahead-wind-forecasts.md or
@day-ahead-wind-forecast.md) and Scotland-versus-England/Wales comparisons. It is **not**
settlement-grade energy. NESO does not say which generation the operational metering covers, or
whether embedded wind is included (TODO: verify metering scope and embedded-wind coverage with
NESO).

NESO publishes it as one CSV per **financial year** (1 April to 31 March), updated monthly. There
are nine resources, 2018-2019 to 2026-2027. The family is **eligible**: it has no issue-time
question, because the rows are outturn, not forecasts. Its one standing defect is a vendor overlap
between the 2025-2026 and 2026-2027 files. That overlap is adjudicated in reconcile, and no data is
altered (see the family section and Holds).

Related series:

- Elexon `fuelhh` (@../../elexon/datasets/fuelhh.md), `agws` (@../../elexon/datasets/agws.md)
  and `agpt` (@../../elexon/datasets/agpt.md) are Elexon's wind generation series. A measured
  comparison does **not** show them to be interchangeable with this family (see Known
  differences below).
- Domain background: @../../../20-domain/concepts/settlement-period.md.
- Same GEN-2 batch: @weekly-wind-availability.md (held) and @wind-bmu-boa-volumes.md (held).

- Publisher group: Generation
- Registry group: generation · archetype: SER

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Monthly Operational Metered Wind Output 2018-2019 | CSV | upload | `bf03c648-98d8-40f3-b5d9-e174cb2c1f81` |
| Monthly Operational Metered Wind Output 2019-2020 | CSV | upload | `c36868d9-9d43-47ce-ac3e-de69f0bb6222` |
| Monthly Operational Metered Wind Output 2020-2021 | CSV | upload | `043d5423-f877-4d28-864e-210dc68711d4` |
| Monthly Operational Metered Wind Output 2021-2022 | CSV | upload | `e5df03f3-a25b-4df4-a95c-8a709815924b` |
| Monthly Operational Metered Wind Output 2022-2023 | CSV | upload | `f732e9bb-b573-46a7-8767-3affbbb29b45` |
| Monthly Operational Metered Wind Output 2023-2024 | CSV | upload | `c47155bc-71b8-4b0a-aba3-0e2d1295daea` |
| Monthly Operational Metered Wind Output 2024-2025 | CSV | upload | `3ac8c742-d601-4b6c-9779-e69cea94e134` |
| Monthly Operational Metered Wind Output 2025-2026 | CSV | upload | `7622b040-977a-45a6-924e-f158df6c29f0` |
| Monthly Operational Metered Wind Output 2026-2027 | CSV | upload | `c9bc94c4-6d8c-49ff-afff-67c0030bec05` |

All nine resources are SILVER and all feed one family, `metered_wind_output_monthly`. The package
has **no DOC resources**, so it has no PDF or DOCX methodology and no `_files` family. Package id:
`7f7fa642-6eff-4b8f-9e8b-7ede1ba50e20`. Every resource is a CKAN `upload`, even though CKAN
also reports `datastore_active: true` for each one. gridflow downloads the uploaded file, not the
datastore API.

Each resource has the same description: "This file contains the monthly operational wind output
for England and Scotland and Wales. It is updated on a monthly basis."

Captures (all 2026-10-08, under
`C:/gridflow-data/bronze/neso_data_portal/metered_wind_output_monthly/2026/10/08/`, each with a
`.meta.json` sidecar whose SHA-256 matched the body; K-GEN-2-FACTS §1):

| # | Resource (download) | Capture file | Bytes | Rows | Settlement dates | CKAN `last_modified` |
|---|---|---|---:|---:|---|---|
| M01 | [2018-2019](https://api.neso.energy/dataset/7f7fa642-6eff-4b8f-9e8b-7ede1ba50e20/resource/bf03c648-98d8-40f3-b5d9-e174cb2c1f81/download/monthly-operational-metered-wind-output-2018-2019.csv) | `raw_20261008T111224Z_bf03c648-…_c448392f.csv` | 708,015 | 17,520 | 2018-04-01 → 2019-03-31 | 2021-05-12T10:42:16.491017 |
| M02 | [2019-2020](https://api.neso.energy/dataset/7f7fa642-6eff-4b8f-9e8b-7ede1ba50e20/resource/c36868d9-9d43-47ce-ac3e-de69f0bb6222/download/monthly-operational-metered-wind-output-2019-2020.csv) | `raw_20261008T111227Z_c36868d9-…_3d226cb1.csv` | 717,198 | 17,568 | 2019-04-01 → 2020-03-31 | 2021-05-12T15:33:52.605448 |
| M03 | [2020-2021](https://api.neso.energy/dataset/7f7fa642-6eff-4b8f-9e8b-7ede1ba50e20/resource/043d5423-f877-4d28-864e-210dc68711d4/download/monthly-operational-metered-wind-output-2020-2021.csv) | `raw_20261008T111230Z_043d5423-…_9de146ca.csv` | 713,459 | 17,520 | 2020-04-01 → 2021-03-31 | 2021-05-12T15:37:52.572942 |
| M04 | [2021-2022](https://api.neso.energy/dataset/7f7fa642-6eff-4b8f-9e8b-7ede1ba50e20/resource/e5df03f3-a25b-4df4-a95c-8a709815924b/download/monthly-operational-metered-wind-output-2021-2022.csv) | `raw_20261008T111232Z_e5df03f3-…_113dcceb.csv` | 710,422 | 17,520 | 2021-04-01 → 2022-03-31 | 2022-04-13T13:09:21.187848 |
| M05 | [2022-2023](https://api.neso.energy/dataset/7f7fa642-6eff-4b8f-9e8b-7ede1ba50e20/resource/f732e9bb-b573-46a7-8767-3affbbb29b45/download/monthly-operational-metered-wind-output-2022-2023.csv) | `raw_20261008T111235Z_f732e9bb-…_1a0e0bea.csv` | 714,525 | 17,520 | 2022-04-01 → 2023-03-31 | 2023-04-21T15:26:04.799398 |
| M06 | [2023-2024](https://api.neso.energy/dataset/7f7fa642-6eff-4b8f-9e8b-7ede1ba50e20/resource/c47155bc-71b8-4b0a-aba3-0e2d1295daea/download/monthly-operational-metered-wind-output-2023-2024.csv) | `raw_20261008T111238Z_c47155bc-…_2bb01ac5.csv` | 720,416 | 17,568 | 2023-04-01 → 2024-03-31 | 2024-04-15T11:23:46.779628 |
| M07 | [2024-2025](https://api.neso.energy/dataset/7f7fa642-6eff-4b8f-9e8b-7ede1ba50e20/resource/3ac8c742-d601-4b6c-9779-e69cea94e134/download/monthly-operational-metered-wind-output-2024-2025.csv) | `raw_20261008T111241Z_3ac8c742-…_561733af.csv` | 719,991 | 17,520 | 2024-04-01 → 2025-03-31 | 2025-04-29T13:43:23.087780 |
| M08 | [2025-2026](https://api.neso.energy/dataset/7f7fa642-6eff-4b8f-9e8b-7ede1ba50e20/resource/7622b040-977a-45a6-924e-f158df6c29f0/download/monthly-operational-metered-wind-output-2025-2026.csv) | `raw_20261008T111243Z_7622b040-…_4e39e845.csv` | 733,739 | 17,713 | 2025-04-01 → 2026-04-05 (P1 only) | 2026-04-07T10:00:37.054177 |
| M09 | [2026-2027](https://api.neso.energy/dataset/7f7fa642-6eff-4b8f-9e8b-7ede1ba50e20/resource/c9bc94c4-6d8c-49ff-afff-67c0030bec05/download/monthly-operational-metered-wind-output-2026-2027.csv) | `raw_20261008T111246Z_c9bc94c4-…_c5079a69.csv` | 361,150 | 8,785 | 2026-04-01 → 2026-10-01 (P1 only) | 2026-10-03T11:17:29.313427 |

How the row counts add up:

- A full financial year is 365 × 48 = **17,520** rows. The spring short day (46 periods) and the
  autumn long day (50 periods) cancel out.
- The two years containing 29 February (2019-2020, 2023-2024) have **17,568** rows.
- M08 has 17,520 + **193** rows, because it runs past 31 March to 2026-04-05 P1. That overrun is
  the overlap described below.
- M09's 8,785 rows equal the CKAN datastore `total` read on 2026-10-08.

The filenames follow `monthly-operational-metered-wind-output-<YYYY>-<YYYY>.csv`. Resolve the
URL from the CKAN resource rather than hard-coding it.

## Families

### `metered_wind_output_monthly`

- Kind: tabular · archetype: SER · refresh: monthly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Sett_Date | `sett_date` | date | `%Y-%m-%d` | no | — | Date |
| Sett_Period | `sett_period` | int64 | — | no | — | Settlement Period |
| Scottish Wind Output | `scottish_wind_output` | float64 | — | yes | — | MW |
| England/Wales Wind Output | `england_wales_wind_output` | float64 | — | yes | — | MW |
| Total | `total` | float64 | — | yes | — | MW |

- Entity key: `resource_id`, `sett_date`, `sett_period`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: sp_pair (`sett_date`, `sett_period`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Eligible. Not held.**

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the CKAN
   `last_modified` of the capture's resource. CKAN emits it without an offset, and gridflow reads it as
   UTC (gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). Every row of a
   capture shares its resource's vintage, so silver holds **nine distinct vintages**, one per
   resource (see the capture table). `available_at` equals `published_at` on all 149,234 rows
   (checked 2026-10-09). The body has **no issue column**, the filename has no issue token, and
   the issue spec is `none`. The vintage is only an availability clock. It is not a forecast
   issue time, and it is not an "immutable from" claim (FACTS §2 g2). For the older archives
   it is years after the settlement dates, because they were uploaded in 2021 and later. Data
   captured before gridflow's first capture is subject to the ADR-030 caveat about earlier
   availability.
2. **Event time (`sp_pair` on `sett_date`, `sett_period`).** `timestamp_utc` = `event_time` =
   the **start** of the settlement period in UTC: UK-local (`Europe/London`) midnight of
   `sett_date` + 30 min × (`sett_period` − 1), converted to UTC. For example, 2018-04-01 P1 →
   2018-03-31T23:00Z (BST). Event time is **not the capture time**, and the `none` fallback
   (timestamp_utc = capture time) does not apply to this family. Checks on silver (2026-10-09):
   - `timestamp_utc` matches the formula on all 149,041 distinct `(sett_date, sett_period)`
     pairs, with 0 mismatches.
   - `event_time` equals `timestamp_utc` on all 149,234 rows.

   The body has no explicit time column, so the period-start choice follows the vendor's
   settlement-day definition (half-hours from local midnight). It cannot be cross-checked
   against a vendor timestamp (FACTS §2 g1).

**Units (vendor dictionary only: CKAN datastore field info for resource `c9bc94c4…`, read
2026-10-08; [resource dictionary](https://www.neso.energy/data-portal/monthly-operational-metered-wind-output/monthly_operational_metered_wind_output_2026-2027)).**

- `Scottish Wind Output` and `England/Wales Wind Output`: **MW**, "Operational Metered MW".
- `Total`: **MW**, "Total of Scotland and England/Wales Operational Metered MW".
- All three have dictionary type `numeric`, cast to float64.
- `Sett_Date` has unit "Date" and `Sett_Period` has unit "Settlement Period". These are temporal
  coordinates, not physical quantities.

A Decimal check over every populated row found that `Total` equals the sum of the two regional
columns with zero discrepancies (FACTS C03). gridflow's float check on silver agreed (0 rows
off by more than 1e-6). This corroborates the dictionary's definition of `Total`. It does not
supply the unit.

These are MW values per half-hour, as the dictionary states. Do not relabel them as MWh. If you
need energy, MWh = MW × 0.5 **only** under an average-power reading. The dictionary does not
say whether each value is an average over the period or a spot reading.
`TODO: verify` with NESO whether each value is a half-hour average or an instantaneous sample.

**Sentinels and missing values (FACTS §2 g5).** The record declares no null-token map, and none
is needed. Full-body checks on all nine captures found:

- no blank cells and no `N/A` or `NA` tokens in any column;
- no numeric `-1`, no zeros and no negative values in any value column.

Silver has 0 nulls in every column. The value columns are nullable in the record only so that a
future blank would be preserved, not dropped. No bounds are imposed on the values.

**Settlement periods and DST.** `sett_period` is bounded `1..50` in the record. Every complete
financial-year archive (M01–M08) contains its autumn 50-period day and its spring 46-period day,
each with the full period sequence (FACTS §5). M09 (2026-04-01 → 2026-10-01) spans no clock
change, so its maximum period is 48. Two final days are partial, and this was measured, not an
error: M08 ends with only P1 on 2026-04-05, and M09 ends with only P1 on 2026-10-01 (FACTS §2).

**Regions.** "Scottish" and "England/Wales" are the vendor's broad geographic headings. NESO does not
identify them as GSP groups or as coded regions, and gridflow does not map them to any regional
code (FACTS §5, region decision). `TODO: verify` the exact boundary the vendor uses, for example how
cross-border or offshore sites are assigned.

**Identity and `_latest`.**

- The vendor grain is one row per settlement date and period in each file. Every body is unique
  on that pair, with zero duplicate full rows (FACTS §2 g3). No vendor text declares a primary
  key.
- The entity key adds `resource_id`, which the engine stamps from the capture sidecar (ADR-039
  P-2). The within-capture duplicate guard therefore enforces the per-file grain.
- `_latest` is `whole_capture` **per `resource_id`** (`latest_partition: "resource_id"`, ADR-039
  P-1/P-3). It keeps the newest complete capture of **each** financial-year file. Without the
  partition it would keep only the newest file, 2026-2027. The as-of bound is applied before
  ranking, so each resource's winner is chosen only among captures available at the as-of
  instant.
- DuckDB relations: `silver_neso_data_portal_metered_wind_output_monthly` (all captures) and
  `silver_neso_data_portal_metered_wind_output_monthly_latest`. Each resource has exactly one
  capture today, so `_latest` serves all 149,234 rows.

**The M08/M09 overlap (adjudicated, data unchanged).** The 2025-2026 file (M08) runs past its
financial year. M08 and the 2026-2027 file (M09) both publish **2026-04-01 P1 → 2026-04-05 P1**,
which is **193 settlement keys**. Their values **conflict**:

- only 3 of the 193 value triples are numerically equal;
- per column, 7 Scottish, 12 England/Wales and 3 Total values are equal.

Example at 2026-04-01 P1 (FACTS C07):

| Resource | Scottish MW | England/Wales MW | Total MW |
|---|---:|---:|---:|
| M08 (2025-2026) | 3,670.428 | 1,517.412 | 5,187.840 |
| M09 (2026-2027) | 3,677.116 | 1,520.562 | 5,197.678 |

How gridflow handles it:

- NESO states no precedence, so **both rows are served**. `_latest` and as-of output return two
  rows for each of the 193 keys, one per `resource_id`. gridflow does no dedup, no truncation, no
  averaging and no precedence filter (ADR-039 P-5; GEN-2H invariant H4; acceptance test 5 pins
  this as byte-identical to an unadjudicated run).
- Reconcile reports the overlap as an `overlap` gap. The gap is **adjudicated** by the committed
  ledger entry in gridflow
  `@src/gridflow/connectors/neso_data_portal/registry/_reconcile_adjudications.json`, which names
  the two exact 2026-10-08 captures and cites RULINGS 547 and ADR-040. The entry's question for
  NESO is:
  > Which archive is authoritative for the 193 settlement keys 2026-04-01 P1 to 2026-04-05 P1
  > that the 2025-2026 and 2026-2027 resources both publish?
- Adjudicated does not mean clean. Reconcile lists the gap in its own `ADJUDICATED` bucket with
  the reason and question, and exits 0 only because nothing is left open (ADR-040 P-4).

**Consumer rule:** never dedup this family on `(sett_date, sett_period)` alone. For 2026-04-01 →
2026-04-05 P1, choose a resource explicitly, and record that choice as your own policy, not a
vendor rule. One example policy is "prefer the file whose financial year contains the date",
which picks M09 for those keys.

`TODO: verify` (FACTS M-OVERLAP) NESO's precedence for the shared keys, or whether the 2025-2026
file's boundary is an error.

**Known differences from Elexon (FACTS §7).** A comparison of the M09 period against September
2026 Elexon partitions gave these results:

| Elexon series | Matched keys | Exact equal | Mean abs diff (MW) | Max abs diff (MW) |
|---|---:|---:|---:|---:|
| `fuelhh` WIND | 1,247 | 3 | 248.2 | 10,988.0 |
| `agws` onshore + offshore | 1,248 | 0 | 1,770.8 | 13,469.0 |
| `agpt` onshore + offshore | 432 | 0 | 2,410.7 | 12,389.9 |

For `fuelhh`, about half the keys agree within 0.5 MW (631 of 1,247), with a median absolute
difference of 0.49 MW. Large gaps remain, though. The largest is 2026-09-12 P28: NESO 5,948.960 MW
against Elexon 16,937.000 MW.

The series are **not** interchangeable. Keep NESO values as published, and never "correct" them
from Elexon. NESO's own note about operational versus settlement metering is relevant context,
but it is not a proven explanation for any individual difference.
`TODO: verify` (FACTS M-ELEXON-DIFFERENCES) coverage, measurement basis and revision conventions
with NESO.

**Dictionary versus body (recorded deltas).**

- `Sett_Period` comment: "Integer 1 to 48 per Settlement Date". Bodies carry period 50 on autumn
  clock-change days and only 46 periods on spring days. The record allows `1..50`, and long-day
  periods are preserved.
- `Sett_Date` example: `01/04/2019`. Every captured body uses `%Y-%m-%d`, so
  `formats_by_filename` is not needed (FACTS GEN2-2).
- The package and resource text says "monthly". The files are financial-year archives that are
  refreshed monthly, not one file per month.

**Activation (2026-10-09, master `73e7eec`, PR #94).** Cutoff 2026-10-08. No silver existed
before, so nothing was overwritten.

- Transform: **149,234 rows** over 9 resources, equal to the planned count. Peak memory was
  596.1 MiB.
- Reconcile `--all --cutoff 2026-10-08`, run under `rss_run.py`: exit 0 over 58 families, 0 open
  gaps and **5 adjudicated**. Two of the five are this family's overlap, one gap per capture
  (M08 and M09) under one ledger entry. The other three are the BOA duplicate-row captures
  B01, B02 and B07. `stale_adjudication` was 0, and peak memory was 2,051.3 MiB.
- Sources: gridflow `@.planning/v0.22-RESULTS.md` §"GEN-2H —"; RULINGS 557, 558.

**Silver layout.** Nine Parquet files, one per capture, under
`C:/gridflow-data/silver/neso_data_portal/metered_wind_output_monthly/year=2026/month=10/`. The
`year=`/`month=` partition is the **capture** date, not the settlement date, so do not
partition-prune by settlement year. The columns are the five vendor columns, then `resource_id`, then
`timestamp_utc`, `published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`,
`available_at`, `source_run_id` and `dataset_version`. All timestamps are tz-aware UTC.
`dataset_version` is `1+e1`, meaning record version 1, epoch 1.

## Cadence

- Registry refresh: monthly
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Monthly

What the CKAN timestamps show (observed, with no inference drawn):

- The closed-year archives were last modified between 2021-05-12 (the three oldest, uploaded on
  the day the package was created) and 2025-04-29.
- The 2025-2026 file was last modified on 2026-04-07, after the year ended, and that upload
  carries the April overrun.
- The current 2026-2027 file was last modified on 2026-10-03, and its data runs to 2026-10-01 P1.

`TODO: verify`:

- the vendor's upload day each month;
- whether each upload replaces the whole year-to-date file;
- whether closed-year archives are ever revised after the year ends.

gridflow keeps every dated capture in silver. A revision would therefore show up as a new
vintage of the same `resource_id`, and `_latest` would then serve the newer capture.

**Operational consequence (ADR-040 R-1).** The adjudication names exact captures. When the
2026-2027 resource is next captured, its new capture overlaps M08 on the same 193 keys, and that
gap is not covered. The old entry also goes stale, so reconcile turns red until the ledger is
edited in a PR. This behaviour is intended (GEN-2H invariant H3), not a regression.

gridflow config declares `schedule: "daily"` for this family (`metered_wind_output_monthly` in
`config/sources.yaml`, with `max_query_days: 1`), as it does for most NESO Data Portal datasets.
TODO: verify whether any scheduler actually runs that daily capture.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- none

This family is eligible (gridflow `@docs/neso_data_portal/eligibility.md`). Its one standing
defect is the M08/M09 overlap. That is a vendor question for NESO, already adjudicated in
reconcile under RULINGS 547 and ADR-040. It is not an E-SEM hold, and no data is altered or
withheld because of it.

The other two packages of the same GEN-2 batch are held. Only their hold questions and row
counts are given here:

- `weekly_wind_availability` (@weekly-wind-availability.md): held (unit E-SEM). NESO's
  week-number calendar is undefined, meaning the numbering, the year interpretation, week start
  and end, and timezone. 43,555 silver rows (RULINGS 547, 551; RESULTS §"GEN-2 —").
- `wind_bmu_boa_volumes` (@wind-bmu-boa-volumes.md): held (unit E-SEM). The row grain is
  unexplained (historical files repeat whole rows), and the sign in the 2026-27 file contradicts
  the dictionary's curtailment definition. 904,240 silver rows from the six clean archives. The
  three duplicate-row archives (2018/19, 2019/20, 2024/25) are adjudicated failed captures and
  are not loaded (RULINGS 547, 558; RESULTS §"GEN-2H —").
