---
source: "neso_data_portal"
package: "weekly-wind-availability"
dataset_key: "weekly_wind_availability"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  held: "NESO never defines its week labels, so no row can be tied to a calendar week."
  title: Weekly wind availability by BM unit
  summary: >-
    NESO's technical availability of each wind balancing mechanism (BM) unit in MW, by week; NESO
    says it covers 2 to 52 weeks.
  facts:
    vendor: "NESO Data Portal, package Weekly Wind Availability: one CSV"
    cadence: "Weekly, NESO says; its modified stamps include 6, 8 and 16 October 2026"
    grain: "Each row: one BM unit and one NESO week label"
  landscape: power
  what_it_is: >-
    One MW figure per BM unit and week label, like NESO's example `13W20`. NESO calls it technical
    availability, not what the wind lets the farms produce, and describes the label only as the week
    the units are available. Its files of 8 and 16 October 2026 each carried 155 labels, against its
    stated 2 to 52 weeks.
  how_used:
    - "Wind availability per BM unit, further ahead than the daily file's 14 days"
    - "Capacity changes by unit, as a supply input to longer-range margin outlooks"
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then the CSV, downloaded whole unless its
      `last_modified` is unchanged.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=weekly-wind-availability"
      - "GET https://api.neso.energy/dataset/542b7b69-7fbc-412c-affc-074ef58495c8/resource/bb375594-dd0b-462b-9063-51e93c607e41/download/weeklywindavailability.csv"
    commands:
      - {run: gridflow ingest neso_data_portal weekly_wind_availability --last 24h, comment: "a changed file to bronze"}
      - {run: gridflow transform neso_data_portal weekly_wind_availability --last 24h, comment: "the capture's date to silver"}
  related:
    - {dataset: neso_data_portal/daily_wind_availability, note: "The same availability by day, 2 to 14 days ahead"}
    - {dataset: elexon/uou2t14d, note: "Elexon's available output per BM unit, 2 to 14 days ahead"}
    - {dataset: neso_data_portal/14-days-ahead-wind-forecasts, note: "NESO's forecast of wind output, not availability, up to 14 days ahead"}
---

# Weekly Wind Availability

NESO's **weekly technical availability of wind generators**, in MW, per BM unit and per forward
week. The package notes describe it as the Electricity System Operator's wind generator
availability "at a generator level at a weekly resolution for 2-52 weeks ahead". The resource
description adds that this is the technical availability of the wind farms "rather than what they
are able to actually produce based on wind speed". It is therefore a capacity-availability
figure, not a wind-speed-based generation forecast and not metered output. For output-side
series see @monthly-operational-metered-wind-output.md (operational metering) and
@14-days-ahead-wind-forecasts.md (a generation forecast on a shorter horizon).

The file is a flat grid of `BMU_ID` x `Week Number` x `MW`. One CSV upload carries all of it, and
each new upload replaces the previous one.

**The output is held (unit E-SEM).** NESO does not define the `Week Number` calendar, so no row
can be dated to a target week. The body also carries more week labels than the package's
documented horizon. See Holds. The output exists in silver, but it is not eligible for
publication or point-in-time model use until E-SEM is answered (RULINGS 547, 551). **This page
gives schema, clocks and row counts only, and no data values.**

Related reference: the BM unit identifiers match Elexon's National Grid BMU namespace for a
subset. Of 281 distinct identifiers, 233 match `national_grid_bm_unit` in the local Elexon
reference (@../../elexon/datasets/bmunits_reference.md) and 0 match `bm_unit_id`. The other 48
stay as supplied. gridflow does not prefix or normalise them (K-GEN-2-FACTS §3 g3, command C06).

- Publisher group: Generation
- Registry group: generation · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Weekly Wind Availability | CSV | upload | `bb375594-dd0b-462b-9063-51e93c607e41` |

The package has one resource and it is SILVER. It has no DOC resources, so there is no
methodology document and no `_files` family. Package id `542b7b69-7fbc-412c-affc-074ef58495c8`.

- **Weekly Wind Availability** -> `weekly_wind_availability` (held).
  Download: [weeklywindavailability.csv](https://api.neso.energy/dataset/542b7b69-7fbc-412c-affc-074ef58495c8/resource/bb375594-dd0b-462b-9063-51e93c607e41/download/weeklywindavailability.csv).
  Captured: `raw_20261008T114125Z_bb375594-dd0b-462b-9063-51e93c607e41_0e401fcf.csv`,
  753,557 bytes, 43,556 CSV records of which 43,555 are populated and 1 is all-blank.
  Recaptured: `raw_20261016T204817Z_bb375594-dd0b-462b-9063-51e93c607e41_b4901dfb.csv`
  (`last_modified` `2026-10-16T20:20:25.674628`), 752,941 bytes, the same 43,556 records,
  43,555 populated (281 BM units x 155 labels, `44W26` to `41W29`); measured 2026-10-24 from
  bronze, where the earlier "one capture" statements below were written before it.

The filename `weeklywindavailability.csv` matched in the 2026-10-06 catalogue snapshot and in the
2026-10-08 and 2026-10-16 captures. It contains no date or issue token. Three observations do not establish a
vendor policy, so resolve the URL from the CKAN resource and do not hard-code it. The resource is
`datastore_active` in CKAN, but its `url_type` is `upload` and gridflow captures it as an upload.
A datastore read on 2026-10-08 reported a total of 43,555, which matches the populated-row count.
Both captures have one header epoch (`BMU_ID,Week Number,MW`).

## Families

### `weekly_wind_availability`

- Kind: tabular · archetype: FC · refresh: weekly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| BMU_ID | `bmu_id` | string | — | yes | — | MW |
| Week Number | `week_number` | string | — | yes | — | — |
| MW | `mw` | float64 | — | yes | — | MW |

- Entity key: `bmu_id`, `week_number`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Held (unit E-SEM). This page gives schema, clocks and counts only, and no data values.**

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the capture's CKAN
   `last_modified`, `2026-10-08T11:20:20.163158` for the first capture
   (`2026-10-16T20:20:25.674628` for the second). CKAN emits it without an offset, and gridflow
   reads it as UTC (gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`).
   Every row of a capture shares this vintage (one distinct value over all 43,555 rows). The
   file has **no issue column** and the filename carries no issue token, so the issue is `none`
   and the vintage is the only availability clock. No evidence shows the bytes are immutable at
   issue.
2. **Event time (`none`).** The temporal recipe is `none`, so `timestamp_utc` = `event_time` =
   the **capture time**, here `2026-10-08T11:41:25.952757Z` (`written_at` of the bronze
   capture). Both columns equal it on every row. **It is not the target week.** `week_number` is
   kept as a raw string and is not converted to an instant, because NESO does not define the
   calendar (see Hold question). A consumer must not read `timestamp_utc` as the week the
   availability applies to.

**Hold question.** The vendor dictionary describes `Week Number` only as the "Week number for
the BMU's are available", with the example `13W20`. It does not define the week-numbering
system, how the two-digit year is read, the first day of the week, or the timezone. NESO must
state these before any row can be dated to a target week. The package also documents a
2-52-week horizon, whereas the body carries **155 distinct week labels**, running from `43W26` to
`40W29` in the label's raw ordering (2026-10-08 capture; the 2026-10-16 capture also has 155,
from `44W26` to `41W29`, one week later at both ends). The live dataset description repeats the 2-52-week
statement. NESO should reconcile that horizon with the body.

A diagnostic reading each label `wwWyy` as ISO week `ww` of year `2000 + yy` (Monday start,
`Europe/London`) places every target after both the vintage and the capture time. That passes the
forward-target rule of RULINGS 529 *conditionally*. **It is not an adopted vendor calendar.**
Certification needs NESO's definition, so the forecast interpretation stays held (FACTS §3
W-CALENDAR, W-FORWARD, GEN2-4). A raw-label record with temporal `none` remains expressible, and
that is what gridflow stores.

**Shape of a capture (counts only).** 43,555 populated rows = 281 distinct `bmu_id` x 155
distinct `week_number`. Every week label has 281 BM units, so the populated body is a complete
BMU x week grid. `(bmu_id, week_number)` was measured unique over the full populated body. No
silver cell is null. The reader drops the single all-blank CSV record, which is why 43,556
records give 43,555 rows.

**Units (vendor dictionary only: CKAN datastore field info for resource `bb375594...`, read
2026-10-08; [package page](https://www.neso.energy/data-portal/weekly-wind-availability)).**
`MW` is **MW**: "Capacity of the BMU in megawatts" (dictionary title "Mega Watt Capacity", type
`integer`, CKAN type `int4`), cast to float64, which leaves integer values unchanged.
`BMU_ID` also carries `MW` as its dictionary unit, which is inconsistent with its description
("Balancing Mechanism Units Identification"). It is an identifier, so store it as a string and do
not read it as a quantity. `Week Number` has no unit and is a temporal label. The `MW` figure is
availability in the sense of the resource description (technical availability of the wind farm).
`TODO: verify` with NESO whether it is a capacity ceiling or an expected availability in a stated
week, because the field text does not distinguish them.

**Sentinels and missing values (FACTS g5).** No null-token map is declared. Full-body checks
found no `N/A`, `NA`, literal `-1` or numeric -1 and no blank cells in any populated row. The
only blank item is the one all-blank CSV record, dropped by the reader. The `MW` column contains
zero values, including runs of zeros per BM unit. No vendor source says a zero
marks an unavailable unit, a placeholder or undeveloped capacity, so zeros are kept as numbers
and never converted to null. `TODO: verify` the vendor's zero policy (FACTS W-ZERO-POLICY). No
bounds are imposed.

**Identity.** The vendor describes the grain as generator and week. `bmu_id + week_number` was
measured unique over the full populated body, with `MW` deliberately left out of the key. No
vendor text declares it a contractual key, so the entity key is a capture guard and `_latest` is
`whole_capture`: the newest capture wins as a whole (FACTS §3 T02). `TODO: verify` the vendor
revision key. Each upload replaces the whole horizon, so history across uploads lives only in the
dated silver captures.

**Activation (2026-10-09, master `0f77c85`).** Cutoff 2026-10-08, one capture: **43,555 rows**,
equal to the planned count (peak 550.8 MiB). No prior silver existed, so nothing was overwritten.
The family holds one Parquet file under `year=2026/month=10`. Reconcile found 0 gaps for it. The
all-families `reconcile --all` run was not clean at that merge for an unrelated reason (a memory
fault on another family), and the following merge fixed that with a memory-bounded check; the
later full run exited 0 over 58 families with 0 open gaps (gridflow `@.planning/v0.22-RESULTS.md`
sections GEN-2 and GEN-2H; RULINGS 550, 551, 557, 558).

**Second capture (measured 2026-10-24).** The 2026-10-16 capture was transformed to a second
Parquet file under `year=2026/month=10`, 43,555 rows, `published_at` `2026-10-16T20:20:25.674628Z`.
Silver now holds two captures; `_latest` (`whole_capture`) takes the 2026-10-16 one whole.

Silver columns beyond the vendor columns: `timestamp_utc`, `published_at`,
`bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id`,
`dataset_version`. All timestamps are tz-aware UTC. `dataset_version` `1+e1` = record version 1,
epoch 1.

## Cadence

- Registry refresh: weekly
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Weekly

"Weekly" is the only vendor statement of cadence. `TODO: verify` the upload day and time, and
whether each upload replaces the whole horizon. The 2026-10-06 catalogue snapshot recorded
`last_modified` `2026-10-06T19:20:19`, and the 2026-10-08 capture recorded
`2026-10-08T11:20:20`, and the 2026-10-16 capture recorded `2026-10-16T20:20:25`. These are three
observations about the file's modification time, and they do not establish the upload schedule. gridflow's refresh captures one state per run, so uploads
between runs are lost. The dated silver captures are therefore a sample of the vendor's
publication history, not the full history. No scheduled gridflow refresh exists yet. Captures are
on demand.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `weekly_wind_availability`: held: TODO: NESO does not define the `Week Number` calendar (week system, year, start day, zone), so no target week can be dated; the body also carries 155 week labels against a documented 2-52-week horizon. (unit E-SEM)

The held output exists in silver but is not eligible for publication or point-in-time model use
until unit E-SEM answers its question (RULINGS 547, 551). This page publishes its schema, clocks
and row counts only. No data value, sample row or value statistic for this family is published
here. The hold applies to the captured body and to later captures unless NESO defines the
calendar.
