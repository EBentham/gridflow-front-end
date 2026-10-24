---
source: "neso_data_portal"
package: "weekly-opmr"
dataset_key: "weekly_opmr"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  held: "Rows name engineering weeks NESO does not map to dates, and give only a publication date."
  title: Weekly operational planning margin requirement
  summary: >-
    NESO's view, by engineering week, of the spare generation it needs above forecast demand, 2 to
    52 weeks ahead, it says.
  facts:
    vendor: "NESO Data Portal, package `weekly-opmr`: one CSV file"
    cadence: "Weekly, NESO lists; its October 2026 files carry a publication almost every day"
    grain: "Each row: one engineering week, as forecast on one publication date"
    history: "NESO's 16 October 2026 file holds publications from 12 March 2021"
  landscape: power
  what_it_is: >-
    NESO defines the operational planning margin requirement (OPMR) as the generation needed above
    its demand forecast for its reserve requirement. Each publication gives, in MW per engineering
    week, peak and minimum demand forecasts, generator availability, interconnector limits, the
    OPMR and national surplus. NESO says 2 to 52 weeks ahead; its 16 October 2026 file's newest
    publication reaches engineering year 2029.
  how_used:
    - See NESO's expected margin over the weeks ahead, week by week
    - Track how NESO's view of one engineering week changes between publications
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then the CSV, downloaded whole unless
      `last_modified` is unchanged. The 8 October 2026 publication has different figures in NESO's
      8 and 16 October files.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=weekly-opmr"
      - "GET https://api.neso.energy/dataset/025b9417-83a0-445b-a818-414ea49cf7c3/resource/c08419f5-a28d-4e35-87a4-676d7eb05713/download/csv_opmr_weekly.csv"
    commands:
      - {run: gridflow ingest neso_data_portal weekly_opmr --last 24h, comment: "the CSV to bronze"}
      - {run: gridflow transform neso_data_portal weekly_opmr --last 24h, comment: "the capture's date to silver"}
  related:
    - {dataset: neso_data_portal/daily-opmr, note: "The same margin terms by target day, 2 to 14 days ahead"}
    - {dataset: neso_data_portal/long-term-2-52-weeks-ahead-national-demand-forecast, note: "NESO's national demand forecast, also labelled 2 to 52 weeks ahead"}
    - {dataset: neso_data_portal/negative-reserve-active-power-margin-nrapm-forecast, note: "NESO's negative reserve margin forecast, daily and by week"}
---

# Weekly operational planning margin requirement (OPMR)

NESO's **weekly Operational Planning Margin Requirement (OPMR)** view: the generation required
above the demand forecast to meet the reserve requirement, assessed **2 to 52 weeks ahead** and
published as a single CSV upload on the Open Data Portal.
The package notes define OPMR as the generation, over and above the demand forecast, needed to
meet NESO's reserve requirement. When NESO assesses generation availability against system
needs for 2–52 weeks ahead, it adds this margin on top of the demand forecast.

Each row is one engineering week (`ENG_Year`, `ENG_Week`) as seen from one publication date
(`Publish Date`). It carries the week's peak and minimum demand forecasts, generator
availability, interconnector import and export limits, the margin terms (generation
availability margin, OPMR total, national surplus), constrained plant, interconnector-provided
operating reserve, the high-frequency response requirement and the negative reserve
requirement. All value columns are MW. Per the vendor dictionary, Generation Availability Margin
is available generation minus demand, and OPMR is the generation above the demand forecast
needed to meet the reserve requirement. The dictionary gives no definition for National Surplus
beyond its name. `TODO: verify` its derivation, sign convention and interpretation.

The body is a **history-bearing upload**: one file holds many publication dates, and each
publication date carries a forward view of many engineering weeks. The family is **held**
(unit E-SEM). NESO does not document how an engineering year/week maps to calendar dates, so
gridflow cannot place a row on a target time axis. See Holds.

Related NESO pages: the daily OPMR (@daily-opmr.md), which has a target `Date` column, the
negative reserve active power margin forecast
(@negative-reserve-active-power-margin-nrapm-forecast.md), and the 2–52 week national demand
forecast on the same horizon (@long-term-2-52-weeks-ahead-national-demand-forecast.md). Elexon's
2–14 day generation-availability series (@../../elexon/datasets/uou2t14d.md,
@../../elexon/datasets/fou2t14d.md) describe generator availability on a much shorter horizon.
They are related but not interchangeable.

- Publisher group: Generation
- Registry group: generation · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Weekly Operational Planning Margin Requirement (OPMR) | CSV | upload | `c08419f5-a28d-4e35-87a4-676d7eb05713` |

The package has one resource, and it is SILVER. There are no DOC resources (no PDF/DOCX
methodology) and no `_files` family (K-GEN-1-FACTS §3).

- **Weekly Operational Planning Margin Requirement (OPMR)** → `weekly_opmr` (held).
  Download: [csv_opmr_weekly.csv](https://api.neso.energy/dataset/025b9417-83a0-445b-a818-414ea49cf7c3/resource/c08419f5-a28d-4e35-87a4-676d7eb05713/download/csv_opmr_weekly.csv).
  The filename is fixed: the 2026-10-06 catalogue snapshot and the 2026-10-08 and 2026-10-16
  captures used the same URL.
  Captured: `raw_20261008T114122Z_c08419f5-a28d-4e35-87a4-676d7eb05713_383a7b45.csv`,
  24,685,076 bytes, 314,712 physical data rows (314,711 populated + 1 blank).
  Second capture: `raw_20261016T204813Z_c08419f5-a28d-4e35-87a4-676d7eb05713_1c51ac0c.csv`,
  24,786,014 bytes, 315,953 physical data rows (315,952 populated + 1 blank), the same header.
  Package id `025b9417-83a0-445b-a818-414ea49cf7c3`.

The resource is `datastore_active` in CKAN. The datastore total at a field-info read on
2026-10-08 (314,711) equals the populated row count and the silver row count. Each capture
(2026-10-08 and 2026-10-16) has one header epoch, no UTF-8 BOM, and lines ending in `\n`.

**Header history.** The package notes announced a column-id change on 17 September 2026:
`ENG.Week` → `ENG_Week`, `ENG.Year` → `ENG_Year`, `Maximum I/C Import` → `Maximum IC Import`,
`Maximum I/C Export` → `Maximum IC Export`, `Operating Reserve provided by I/Cs` →
`Operating Reserve provided by ICs`. Epoch 1 is the post-change header. gridflow holds no
capture with the old header (both captures, 2026-10-08 and 2026-10-16, carry the new one). A pre-change body would fail the epoch match loudly rather than
type silently (the header contract raises on any name mismatch, gridflow
`@src/gridflow/silver/csv_bronze.py` `_assert_header_contract`). `TODO: verify` whether NESO will rename columns again.

## Families

### `weekly_opmr`

- Kind: tabular · archetype: FC · refresh: weekly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| ENG_Week | `eng_week` | int64 | — | yes | — | — |
| ENG_Year | `eng_year` | int64 | — | yes | — | — |
| Publish Date | `publish_date` | date | `%Y-%m-%d` | yes | — | — |
| Peak Demand Forecast | `peak_demand_forecast` | float64 | — | yes | — | MW |
| Generator Availability | `generator_availability` | float64 | — | yes | — | MW |
| Maximum IC Import | `maximum_ic_import` | float64 | — | yes | — | MW |
| Maximum IC Export | `maximum_ic_export` | float64 | — | yes | — | MW |
| Generation Availability Margin | `generation_availability_margin` | float64 | — | yes | — | MW |
| Operating Reserve provided by ICs | `operating_reserve_provided_by_ics` | float64 | — | yes | — | MW |
| OPMR total | `opmr_total` | float64 | — | yes | — | MW |
| Constrained Plant | `constrained_plant` | float64 | — | yes | — | MW |
| National Surplus | `national_surplus` | float64 | — | yes | — | MW |
| Minimum Demand Forecast | `minimum_demand_forecast` | float64 | — | yes | — | MW |
| High Freq Response Requirement | `high_freq_response_requirement` | float64 | — | yes | — | MW |
| Negative Reserve | `negative_reserve` | float64 | — | yes | — | MW |

- Entity key: `eng_year`, `eng_week`, `publish_date`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Held (unit E-SEM). This page gives schema, clocks and counts only, and no data values.**

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the CKAN
   `last_modified` of the captured resource: `2026-10-08T11:20:53.625059` for the first capture
   and `2026-10-16T20:20:44.102738` for the second. CKAN emits it without an offset, and gridflow reads it as UTC
   (gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). Every row of a
   capture shares this vintage, including rows published years earlier. The file has **no
   issue column**. `Publish Date` is a calendar date with no time or zone. gridflow keeps it as
   a typed `date` column and does **not** promote it to an issue instant or backdate
   availability to it (K-GEN-1-FACTS g1/g2).
2. **Event time (`none`).** The family has **no event-time recipe**. `timestamp_utc` and
   `event_time` are **the capture time** (the bronze write instant), not a target week. In the
   activated silver all 314,711 rows carry the same `timestamp_utc` = `event_time` =
   `capture_written_at` = `2026-10-08T11:41:22.987668Z` (checked 2026-10-09); the 315,952 rows of
   the 2026-10-16 capture all carry `2026-10-16T20:48:13.953486Z` (checked 2026-10-24). **Never use
   `timestamp_utc` as a time axis for this family.** The forecast's target is carried only by
   `eng_year` + `eng_week`. Those are engineering-calendar identifiers, and gridflow has no
   evidenced mapping from them to UTC.

**Hold question.** NESO's engineering year/week → target date mapping is undocumented, and the
body gives a publication date only. The vendor dictionary describes `ENG_Week` as "Engineering
Week ISO" and `ENG_Year` as the year "as defined by the engineering calendar". The word "ISO"
alone does not settle the week's start day or the week-year convention (K-GEN-1-FACTS
`weekly_opmr` T03). The open points:

- `TODO: verify` the engineering week's start day and the year that week 1 belongs to.
- `TODO: verify` the original issue time and zone behind `Publish Date`.
- `TODO: verify` whether past publications are immutable, and so whether a row was available at
  its publication date in the form now captured.

Because no target date can be derived, the RULINGS 529 forward-target test (every target after
the CKAN vintage) cannot be run. The body is history-bearing in any case, since it holds many
past publication dates. FACTS also notes that the body runs further ahead than the "2–52
weeks" in the resource description. gridflow keeps every supplied row and does not truncate to
the described horizon. Measured on silver (2026-10-24): the newest publication in each capture
has 155 rows, one per engineering week, from 2026 week 43 to 2029 week 40 (publication
2026-10-08) and from 2026 week 44 to 2029 week 41 (publication 2026-10-16). Engineering year
2026 is the only year in the file with a week 53. That is consistent with ISO 8601 weeks (2026
has 53 ISO weeks; 2021 to 2029 have no other), but it does not prove the mapping.

**Units (vendor dictionary only: the CKAN datastore field-info for the resource, read
2026-10-08; package page [weekly-opmr](https://www.neso.energy/data-portal/weekly-opmr)).**
Every value column has `unit: MW` in the vendor field-info. The dictionary types them `int4`,
and gridflow casts them to float64, so integer values are unchanged. `ENG_Week` and `ENG_Year`
have an empty unit field. They are engineering-calendar identifiers, not physical quantities.
`Publish Date` is a date (K-GEN-1-FACTS `weekly_opmr` T01/T02, GEN1-3, g4). Vendor definitions,
paraphrased:

- **Peak / Minimum Demand Forecast**: the week's peak and lowest forecast demand.
- **Generator Availability**: the summed generator availability for the given time in the week.
- **Maximum IC Import / Export**: the maximum import or export level achievable on the
  interconnectors.
- **Generation Availability Margin**: available generation minus demand.
- **Operating Reserve provided by ICs**: operating reserve provided by the interconnectors.
- **OPMR total**: the generation required for OPMR.
- **Constrained Plant**: generation that cannot be used because of network limitations.
- **National Surplus**: the dictionary repeats the name and gives no further definition.
  `TODO: verify` the arithmetic NESO uses to derive it from the other terms.
- **High Freq Response Requirement**: MW of response delivered within 10 seconds of an event.
- **Negative Reserve**: the total negative reserve requirement.

`TODO: verify` which demand definition (ND, TSD or other) the demand forecasts use. The
dictionary does not say.

**Sentinels and missing values (K-GEN-1-FACTS g5).** No null-token map is declared, and none
is needed:

- Full-body checks found no `N/A`, `NA` or literal `-1` tokens, and no value numerically
  equal to −1.
- The body has **one entirely blank row**: the vendor's trailing lone carriage-return line
  (`\r\n` after the last data row). The generic reader drops it on its logged blank-row path
  (gridflow `@src/gridflow/silver/csv_bronze.py` `_drop_blank_rows`). It is not filtered
  silently, and it is not data. No other blank cells occur, so the activated silver has
  **zero nulls in every column** (checked 2026-10-09).
- Numeric **zeros occur** in some value columns and are **kept as zeros**. No vendor source
  says a zero means missing, unavailable or not applicable. `TODO: verify` zero semantics with
  NESO. No bounds are imposed.

**Header spelling (RULINGS 544).** In the raw body, `Maximum IC Export ` and `National Surplus `
carry a trailing space. The generic reader strips header names before the epoch match
(gridflow `@src/gridflow/silver/neso_data_portal/readers.py`). The record therefore freezes the
stripped spelling shown in the schema. The round trip is pinned by
`test_opmr_trailing_space_headers_type_through_the_stripped_epoch` (gridflow
`@tests/unit/test_neso_gen1_records.py`).

**Identity and selection.** `(eng_year, eng_week, publish_date)` was measured unique across the
full body: 0 duplicates in the 314,711 silver rows, and 0 in the 315,952 rows of the 2026-10-16
capture (which also has no null in any column). No vendor text says it is a contractual
revision key (K-GEN-1-FACTS `weekly_opmr` T04, g3). `TODO: verify` the vendor's revision
identity. `_latest` is `whole_capture`: the newest capture wins as a whole.

**Activation (2026-10-09, master `f19effb`, PR #92).** Cutoff 2026-10-08, one capture at activation:
**314,711 rows**, equal to the planned count. Peak memory was 829.0 MiB. No prior silver
existed, so nothing was overwritten. Reconcile `--all --cutoff 2026-10-08` found 0 gaps over 55
families, with overlap 0 (gridflow `@.planning/v0.22-RESULTS.md` §GEN-1; RULINGS 545–546).
Silver lives at `C:/gridflow-data/silver/neso_data_portal/weekly_opmr/year=2026/month=10/`.

Silver columns beyond the vendor columns: `timestamp_utc`, `published_at`,
`bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id`,
`dataset_version`. All timestamps are tz-aware UTC. `dataset_version` `1+e1` = record version 1,
epoch 1.

## Cadence

- Registry refresh: weekly
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Weekly

The resource description says the file is published weekly with a 2–52 weeks-ahead view.
`TODO: verify` the weekday and time of publication. They are not stated.

Observed at capture (no inference drawn): the resource's CKAN `last_modified` was
`2026-10-06T19:20:38.599788` in the 2026-10-06 catalogue snapshot and
`2026-10-08T11:20:53.625059` at the 2026-10-08 capture. That is two modifications within
two days of a nominally weekly file. At the 2026-10-16 capture it was
`2026-10-16T20:20:44.102738`.

The file is published more often than its label: in the 2026-10-16 capture, `Publish Date`
covers every day from 2021-03-12 to 2026-10-16 except seven (2022-04-24, 2024-02-23 to 25,
2024-03-09, 2024-07-30, 2026-08-23), the same dates as the daily OPMR file, spread evenly over all
seven days of the week (silver, read 2026-10-24).

Re-uploads both append and revise (2026-10-08 against 2026-10-16 captures, silver read
2026-10-24): every first-capture key is still present; 1,241 rows are new (publications 9 to 16
October, 155 rows each and 156 on 11 October); 314,556 shared rows are identical. The other 155 are every row of the 2026-10-08
publication: all changed `generator_availability`, `generation_availability_margin` and
`national_surplus`, and 111 also `opmr_total` and `constrained_plant`. No earlier publication
changed. `TODO: verify` whether publications older than their own day are ever revised.

No scheduled gridflow refresh exists yet. Captures are on demand.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `weekly_opmr`: held: TODO: NESO's engineering year/week to target date mapping is undocumented; the body gives a publication date only (unit E-SEM)

The held output exists in silver, but it is not eligible for publication or point-in-time
model use until unit E-SEM answers its question (RULINGS 542). This page publishes its schema,
clocks and row counts only.

- **What would lift the hold:** a vendor definition of the engineering calendar (the week start
  day, the week-year rule, and ideally a published week → date table), so that each row can be
  given a target-week anchor. Separately, a vendor statement on the publication instant and on
  revision behaviour would be needed before `Publish Date` could serve as an issue time.

The package-level `eligibility: eligible` in the front matter refers to the package registry
entry. Holds are per family, and the package's only family, `weekly_opmr`, is held.

Related, same unit and batch (gridflow `@docs/neso_data_portal/eligibility.md`): `daily_opmr`
is held on a separate question. Its body is history-bearing (targets at or before the CKAN
vintage), and its `Publish Date` likewise has no issue instant or zone. The two weekly NRAPM
families are held because their value columns have no vendor unit or scale. The current
metered-wind, day-ahead-wind and daily NRAPM families in the same batch are eligible on the
forward-target rule (RULINGS 529, 542).
