---
source: "neso_data_portal"
package: "school-holiday-percentages"
dataset_key: "school_holiday_percentages"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: School holiday percentages
  summary: >-
    NESO's daily calendar of public school holidays in GB, by local authority, with a
    population-weighted national share.
  facts:
    vendor: "NESO Data Portal, package School Holiday Percentages: six yearly CSV files"
    cadence: "Yearly, NESO says"
    grain: "Each row: one local authority on one date, plus one `Total` row per date"
    history: "School years 2021/22 to 2026/27, NESO lists"
  landscape: power
  what_it_is: >-
    For each date, whether each local authority's public schools are on holiday (1 or 0), a
    population multiplier, and a `Total` row NESO calls the population-weighted percentage on
    holiday across GB. NESO takes the dates from local authority websites and leaves out private
    schools and the City of London. It uses the data as an input to its demand models.
  how_used:
    - Which parts of GB are on school holiday on a given date
    - A calendar input to demand models, as NESO uses it
  chart:
    type: line
    silver: neso_data_portal/school_holiday_percentages
    time: date
    value: school_holiday
    filter:
      - {column: local_authority, op: eq, value: Total}
    dedup: {"on": [resource_id, local_authority, date], order_by: capture_written_at}
    aggregation: last
    window: {start: "2025-06-25", end: "2026-06-07"}
    unit: "School_Holiday, scale not stated"
  chart_view:
    title: "NESO's Total row for each date, school year 2025/26"
    caption: >-
      Silver `neso_data_portal/school_holiday_percentages`, the `Total` row of each date in NESO's
      2025/26 file, 25 June 2025 to 7 June 2026, drawn as written. NESO calls it a percentage and
      states no scale.
    alt: >-
      Line chart of NESO's `Total` row per date, 25 June 2025 to 7 June 2026. It stays below 0.2
      until 21 July 2025, then reaches 1.0 in the summer (from 30 July), at Christmas and at Easter.
      The October, February and May half terms peak at 0.939, 0.954 and 0.938. Between holidays
      it is mostly at or near 0.
    x_label: NESO's date; no day boundary or zone stated
    y_min: -0.05
    key:
      - {series: school_holiday, label: "Total row", paint: petrol, note: "NESO's population-weighted figure for GB"}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then each of six yearly files, downloaded whole
      unless its `last_modified` is unchanged. Three are shown; 2024/25 writes dates day first.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=school-holiday-percentages"
      - "GET https://api.neso.energy/dataset/c0e9769c-0a6b-460d-a6e6-c66515317a64/resource/48f922ef-b18f-4193-868c-e95c1f271b5c/download/school_holiday_2021_22.csv"
      - "GET https://api.neso.energy/dataset/c0e9769c-0a6b-460d-a6e6-c66515317a64/resource/f2c25078-5721-4abd-b9e3-0fd6d839bb04/download/school_holiday_2024_25.csv"
      - "GET https://api.neso.energy/dataset/c0e9769c-0a6b-460d-a6e6-c66515317a64/resource/5e4bb837-a43b-4709-91e6-ddf8ca9a660a/download/school_holiday_2026_27.csv"
    commands:
      - {run: gridflow ingest neso_data_portal school_holiday_percentages --last 24h, comment: "each changed yearly file to bronze"}
      - {run: gridflow transform neso_data_portal school_holiday_percentages --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: date, op: eq, value: "2025-07-02"}
        - {column: local_authority, op: in, value: [Birmingham, Cardiff, Edinburgh, Essex, Glasgow, Kent, North Lanarkshire, Total]}
      dedup: {"on": [resource_id, local_authority, date], order_by: capture_written_at}
      order_by: [local_authority]
      columns: [local_authority, date, school_holiday, multiplier, resource_id, published_at, timestamp_utc]
    key: [resource_id, local_authority, date]
    caption: "2 July 2025: three Scottish authorities on holiday, four English and Welsh not, and `Total`."
    fields:
      resource_id: "NESO's file the row came from, one per school year"
      local_authority: "NESO's authority name, or `Total` for its GB row; names, not codes"
      date: "The date, as NESO writes it; no day boundary or zone stated"
      school_holiday: "1 or 0 per authority, NESO says; on `Total`, what NESO calls a percentage"
      multiplier: "NESO's population weight, used to turn the flags into a GB total"
      published_at: "NESO's last-modified time for the file, read as UTC; one per file"
      timestamp_utc: "When gridflow captured the file, UTC; not the date the row describes"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  caveat: "NESO calls the `Total` rows a percentage but states no scale; they run 0 to 1."
  notebook:
    lead: >-
      `query()` filters on `timestamp_utc`, the capture time here, so these cells use `data.sql()`
      on the `_latest` view: the `Total` rows, the local authorities' values, then `Total` across
      all six files.
    cells:
      - |
        total = data.sql("""
            SELECT date, school_holiday
            FROM silver_neso_data_portal_school_holiday_percentages_latest
            WHERE local_authority = 'Total'
            ORDER BY date
        """)
        total.school_holiday.agg(["count", "min", "max"]).to_frame().T
      - |
        data.sql("""
            SELECT school_holiday, count(*) AS rows, count(DISTINCT local_authority) AS authorities
            FROM silver_neso_data_portal_school_holiday_percentages_latest
            WHERE local_authority <> 'Total'
            GROUP BY school_holiday
            ORDER BY school_holiday
        """)
      - |
        import pandas as pd
        daily = total.assign(date=pd.to_datetime(total.date)).set_index("date").school_holiday.asfreq("D")
        ax = daily.plot(color="#155A6E", figsize=(9, 3.5), xlabel="NESO's date",
                        ylabel="Total row, as written");
    needs: NESO's six school holiday files
    plot_alt: >-
      Line of NESO's `Total` row per date across all six files, June 2021 to June 2027.
      Each school year repeats one pattern: 1.0 (Easter 2023 0.998) in the summer, at
      Christmas and at Easter, half-term peaks of 0.89 to 0.99, and mostly 0 or near it between holidays.
      The line breaks for 11 to 17 days each June between files.
  related:
    - {dataset: neso_data_portal/demand-profile-dates, note: "Past days NESO matches to forecast days, partly by calendar activities"}
    - {dataset: neso_data_portal/historic-demand-data, note: "GB demand by half hour, to set against holiday dates"}
    - {dataset: neso_data_portal/daily-demand-update, note: "This year's GB demand by half hour, updated daily"}
---

# School Holiday Percentages

This package is NESO's calendar of school holidays across Great Britain, used as a demand
input. Each row pairs a **local authority** with a **calendar date**. It says whether that
authority's public schools are on holiday that day, and gives the authority's **population
weight** (`Multiplier`), which NESO uses to turn the local flags into a national total. Each
date also has an aggregate row labelled `Total`, which the vendor describes as the percentage
of public schools on holiday nationally. NESO publishes one CSV per school-holiday year, six
resources in all (2021/22 through 2026/27). Each year runs from the first summer holiday to the
last holiday before the next summer period, so the files do not overlap. NESO says it collects
the dates from local-authority websites. Private schools are excluded, and so, for now, is the
City of London. The vendor states only that "This data is used as an input into our demand
models" (CKAN package `notes`,
@.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json). TODO: verify how
school holidays affect GB electricity demand; no vendor source in this capture says. Coverage is
GB (per local authority, population-weighted). The newest file (2026/27) has CKAN
`last_modified` 2026-02-12 and its latest `Date` is 2027-06-07. TODO: verify NESO's publication
lead time; no vendor source states one.

gridflow has a silver output for all six years, but it is **held**: NESO has not stated the
numeric scale of the `Total` rows (see Holds). The site page shows the rows with one line
naming that question (ruling 66, 2026-10-24).

- Publisher group: Demand
- Registry group: demand · archetype: SER

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| School Holiday Percentages 2021/22 | CSV | upload | `48f922ef-b18f-4193-868c-e95c1f271b5c` |
| School Holiday Percentages 2022/23 | CSV | upload | `8a9a21e2-91d9-40e0-ac99-68f5e3f1a732` |
| School Holiday Percentages 2023/24 | CSV | upload | `4b640366-af9a-4785-b12f-ff2274e369c0` |
| School Holiday Percentages 2024/25 | CSV | upload | `f2c25078-5721-4abd-b9e3-0fd6d839bb04` |
| School Holiday Percentages 2025/26 | CSV | upload | `73c68bc9-d08b-4173-bfef-6ba1ac0684a9` |
| School Holiday Percentages 2026/27 | CSV | upload | `5e4bb837-a43b-4709-91e6-ddf8ca9a660a` |

Every resource is a CSV with disposition SILVER. The package has no DOC or catalogue-only
resources and no `_files` family (FACTS §1 "`_files` / DOC scope").

Download links and the one capture of each resource (2026-10-08, all CKAN upload resources).
Sizes and CKAN `last_modified` come from each capture's sidecar under
`C:/gridflow-data/bronze/neso_data_portal/school_holiday_percentages/2026/10/08/`. Data rows
equal the silver rows for each resource.

| Year | File | `Date` format | Bytes | Data rows | CKAN `last_modified` |
|---|---|---|---:|---:|---|
| 2021/22 | [school_holiday_2021_22.csv](https://api.neso.energy/dataset/c0e9769c-0a6b-460d-a6e6-c66515317a64/resource/48f922ef-b18f-4193-868c-e95c1f271b5c/download/school_holiday_2021_22.csv) | `%Y-%m-%d` | 3,139,073 | 73,595 | 2024-10-17T16:13:23.814979 |
| 2022/23 | [school_holiday_2022_23.csv](https://api.neso.energy/dataset/c0e9769c-0a6b-460d-a6e6-c66515317a64/resource/8a9a21e2-91d9-40e0-ac99-68f5e3f1a732/download/school_holiday_2022_23.csv) | `%Y-%m-%d` | 3,542,576 | 72,718 | 2024-10-17T16:09:06.364747 |
| 2023/24 | [school_holiday_2023_24.csv](https://api.neso.energy/dataset/c0e9769c-0a6b-460d-a6e6-c66515317a64/resource/4b640366-af9a-4785-b12f-ff2274e369c0/download/school_holiday_2023_24.csv) | `%Y-%m-%d` | 3,278,978 | 72,512 | 2024-10-17T16:07:36.806001 |
| 2024/25 | [school_holiday_2024_25.csv](https://api.neso.energy/dataset/c0e9769c-0a6b-460d-a6e6-c66515317a64/resource/f2c25078-5721-4abd-b9e3-0fd6d839bb04/download/school_holiday_2024_25.csv) | `%d/%m/%Y` | 2,724,434 | 71,829 | 2024-10-17T16:05:05.134322 |
| 2025/26 | [school_holiday_2025_26.csv](https://api.neso.energy/dataset/c0e9769c-0a6b-460d-a6e6-c66515317a64/resource/73c68bc9-d08b-4173-bfef-6ba1ac0684a9/download/school_holiday_2025_26.csv) | `%Y-%m-%d` | 3,593,306 | 72,036 | 2025-07-15T11:27:03.752628 |
| 2026/27 | [school_holiday_2026_27.csv](https://api.neso.energy/dataset/c0e9769c-0a6b-460d-a6e6-c66515317a64/resource/5e4bb837-a43b-4709-91e6-ddf8ca9a660a/download/school_holiday_2026_27.csv) | `%Y-%m-%d` | 3,168,237 | 72,243 | 2026-02-12T16:12:22.167008 |

Package page: [school-holiday-percentages](https://www.neso.energy/data-portal/school-holiday-percentages).

## Families

### `school_holiday_percentages`

- Kind: tabular · archetype: SER · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Local_Authority | `local_authority` | string | — | yes | — | — |
| Multiplier | `multiplier` | float64 | — | yes | — | — |
| Date | `date` | date | `school_holiday_2021_22.csv` → `%Y-%m-%d`; `school_holiday_2022_23.csv` → `%Y-%m-%d`; `school_holiday_2023_24.csv` → `%Y-%m-%d`; `school_holiday_2024_25.csv` → `%d/%m/%Y`; `school_holiday_2025_26.csv` → `%Y-%m-%d`; `school_holiday_2026_27.csv` → `%Y-%m-%d` | yes | — | — |
| School_Holiday | `school_holiday` | float64 | — | yes | — | — |

- Entity key: `resource_id`, `local_authority`, `multiplier`, `date`, `school_holiday`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**One header epoch.** All six files share one exact header: `Local_Authority`, `Multiplier`,
`Date`, `School_Holiday`. The 2024/25 file writes its dates differently (`%d/%m/%Y`), but that
does not make a second epoch. The record maps each exact filename to its format instead (see
below) (FACTS §1 "Exact header epochs", §5).

**What the columns mean (vendor dictionary).** These descriptions come from NESO's saved field
info for the 2026/27 resource (gridflow
`@.planning/research/neso-snapshots/field-info/20261008T114228Z/school_holiday_percentages.json`).
NESO's rendered resource page currently shows these descriptions blank. The saved
`datastore_search` response holds them, so this page relies on the saved response (FACTS §2).

- **`Local_Authority`**: "The Local Authority responsible for setting the holiday times". The
  values are text names. Each date also has one aggregate row labelled `Total`.
- **`Multiplier`**: "The population weighting used to convert the data to a national total".
- **`Date`**: "The date which could be a holiday": a calendar date.
- **`School_Holiday`**: the vendor describes this as "The percentage of public schools on
  holiday in the local authority or in total". The dictionary comment adds that, at local
  authority level, the value is "currently either 1 or 0" depending on whether the authority
  is on holiday.

**Units (vendor dictionary only).** Every column's dictionary `unit` field is **empty**, so the
skeleton's Vendor unit column is `—` throughout. No unit is inferred from a column name.

- `Multiplier`: the vendor documents a role (population weighting) but no unit. FACTS T01
  reads that role as a dimensionless weight. That reading is not a vendor unit field.
- `School_Holiday`: on local-authority rows, the vendor documents a 1/0 holiday flag. On
  `Total` rows, the vendor calls the value a percentage but does not state its numeric scale.
  That gap is the hold. Values are stored as delivered: nothing is multiplied or divided.
- `TODO: verify` the numeric scale of `School_Holiday` on `Total` rows (hold unit E-SEM).

**Geography.** `Local_Authority` holds vendor-provided names, not codes. NESO's descriptions do
not say it is an ONS code, a GSP group or a DNO area, and no name-to-code mapping is
published. Names are kept as delivered, and the `Total` label stays a row value. Do not join
these names through an ONS, DNO or GSP mapping you have built yourself.
`TODO: verify` the formal geography standard behind the names, and get a vendor crosswalk
(FACTS §5 DEM2-1). The number of distinct labels, `Total` included, is 205 in 2021/22, 206 in
2022/23 and 2023/24, and 207 from 2024/25 (silver, 2026-10-09). The set of authorities
therefore changes between years.

**Two clocks.**

1. **Vintage (`ckan_last_modified`).** `published_at` is the CKAN `last_modified` of the
   captured file, read as UTC (ADR-030). `available_at` equals `published_at`. In silver
   (2026-10-09), each resource has a single `published_at`, equal to its sidecar's
   `ckan_last_modified`, and `available_at = published_at` on every row:
   - 2021/22, 2022/23, 2023/24 and 2024/25: 2024-10-17, between 16:05 and 16:13 UTC (one
     upload cohort).
   - 2025/26: 2025-07-15T11:27:03.752628Z.
   - 2026/27: 2026-02-12T16:12:22.167008Z.

   An as-of query before a resource's `last_modified` sees **no** rows from that resource,
   because only one capture of each exists. For example, all four files from 2021/22 to
   2024/25 are invisible to any as-of before 2024-10-17. When a `last_modified` predates the
   capture (true of every file here), `available_at <= as_of` does not prove that the bytes
   gridflow holds are the ones NESO published at that instant. An earlier version may have
   been overwritten before capture (ADR-039 FM-12, accepted residual).
2. **Event time (temporal recipe `none`).** Event time here is **not** the holiday date.
   `timestamp_utc` is the **capture time**: it equals `capture_written_at` on every row,
   giving one value per resource (2026-10-08, 11:17 UTC). `event_time` equals
   `timestamp_utc`. The represented day is the separate typed `date` column, kept as
   delivered. NESO documents no time zone or day boundary for `Date`, so gridflow makes no UTC
   instant from it (FACTS T04, g1; ADR-036). `TODO: verify` the zone and day-boundary
   convention for `Date` before any instant recipe is adopted. Dates in the future (the
   2026/27 file runs into 2027) do not mean the rows were available before capture (FACTS g2).

There is no issue-time column (issue recipe `none`), and the vendor does not promise that
values are fixed once published.

**Per-filename date formats (ADR-039 P-4).** `Date` uses `%Y-%m-%d` in five files and
`%d/%m/%Y` in `school_holiday_2024_25.csv`. The record maps each exact filename (as spelt in the
capture sidecars) to its format. A body whose filename is not listed fails the capture. There
is no fallback format. Each format was tested over each whole body, with zero date-cast
failures (FACTS §5, C-S). A new year's file needs a new map entry before it can be loaded.

**Identity and selection (ADR-039).**

- `resource_id` is **not a vendor column**. The engine stamps each row with its capture's
  sidecar resource UUID.
- The **measured grain** is `(resource_id, local_authority, date)`. It has 0 duplicates in
  every resource's body (FACTS §5) and in silver (2026-10-09).
- The record's entity key also includes `multiplier` and `school_holiday`. It is the
  conservative ADR-036 duplicate guard used when the vendor guarantees no key. Do not read it
  as saying that values define identity. `TODO: verify` a vendor-guaranteed unique key (FACTS
  T05).
- The multiplier is **not** constant per authority within a year. Buckinghamshire (2021/22),
  Swindon (2022/23), Hull (2023/24) and Dorset (2026/27) each carry two distinct multiplier
  values (FACTS §5). Do not reduce this family to one weight per authority.
- `_latest` is `whole_capture` **per `resource_id`** (`latest_partition: resource_id`). It keeps
  the newest complete capture of each yearly file, rather than only the single newest file of
  the family.
- **No `(local_authority, date)` key is shared between any two of the six resources** (all 15
  pairs checked, FACTS §5). That separation is measured, not promised by the vendor. If a
  future file overlaps another, reconcile reports an `overlap` gap; no precedence rule is
  invented (ADR-039).

**Sentinels and missing values (FACTS g5).** The full-body scans found no blanks, `-1`, `NA`
or `N/A` in any of the six files, and the record declares no null tokens. Silver has 0 nulls in
every column (2026-10-09). A `School_Holiday` of `0` means "not on holiday" (dictionary
comment). It is a real value, not a missing-data marker, and is never converted to null,
however long a run of zeros. Each date has exactly one `Total` row, 2,108 in all (one per
distinct date in each resource).

**Row counts per resource (silver, 2026-10-09).**

| Year | Rows | Distinct dates (= `Total` rows) | Distinct authority labels incl. `Total` |
|---|---:|---:|---:|
| 2021/22 | 73,595 | 359 | 205 |
| 2022/23 | 72,718 | 353 | 206 |
| 2023/24 | 72,512 | 352 | 206 |
| 2024/25 | 71,829 | 347 | 207 |
| 2025/26 | 72,036 | 348 | 207 |
| 2026/27 | 72,243 | 349 | 207 |
| **All** | **434,933** | 2,108 | — |

**Activation (2026-10-09, master `776e87a`, PR #91).** The DEM-2 batch merged triple-green
(RULINGS 540). The family was transformed from the 2026-10-08 captures with cutoff
2026-10-08; there was no prior silver, so nothing was overwritten (RULINGS 541). Silver has
**434,933 rows over 6 resources**, equal to the planned count. Reconcile
`--all --cutoff 2026-10-08` exited 0 with 0 gaps over 41 families, `overlap` 0. Coverage was
unchanged at 1,379 captured and 6 missing (gridflow `@.planning/v0.22-RESULTS.md` §DEM-2).

Silver layout: 6 Parquet files, one per capture, under
`C:/gridflow-data/silver/neso_data_portal/school_holiday_percentages/year=2026/month=10/`. The
`year=`/`month=` partition is the **capture** date, not the holiday date. Columns (13): the four
vendor columns, then `resource_id`, `timestamp_utc`, `published_at`, `bronze_capture_id`,
`capture_written_at`, `event_time`, `available_at`, `source_run_id` and `dataset_version`. All
timestamps are tz-aware UTC. `dataset_version` is `1+e1` (record version 1, generic engine
version 1). No gold view or builder reads this family.

**Related package.** The DEM-2 batch also covered Demand Profile Dates
(@./demand-profile-dates.md), which is a separate package.

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Yearly

The vendor says yearly. The CKAN `last_modified` dates match that: the four older years were
last re-uploaded together on 2024-10-17, 2025/26 on 2025-07-15, and 2026/27 on 2026-02-12. A
new year's file appears as a new resource (a new UUID), which needs a new
`formats_by_filename` entry. `TODO: verify` whether NESO revises a year's file after its first
upload (for example after a local authority changes its term dates), and when in the year the
next file appears. Only more captures, compared pair by pair, can show this. One capture of
each resource exists to date (2026-10-08).

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `school_holiday_percentages`: held: TODO: the numeric scale of the Total rows: the vendor calls the aggregate a percentage, but the values measure as a fraction equal to the sum of (multiplier x local indicator) within 0.0005; NESO has not stated the encoding (unit E-SEM)

The silver output exists on disk but is **held**. gridflow's models may not use it for
point-in-time work until unit E-SEM answers the question above. The record carries the hold,
and RULINGS 538 set it when the batch was ruled. The local-authority rows are clear: the
dictionary documents them as 1/0 holiday flags. The `Total` rows are not. NESO calls them a
percentage, but their scale (0–1 or 0–100) is not stated. The measured values match a
population-weighted fraction, but a measurement does not settle the encoding. So the values
are kept exactly as delivered, and none is rescaled. This note gives schema, row counts, clocks
and missingness only; under ruling 66 (2026-10-24) the site page shows the rows, a chart of the
`Total` row as written and a notebook, with one line naming the scale question.

What settles it: NESO states the numeric encoding of the `Total` aggregate, and ideally its
rounding. If the vendor confirms the values as delivered, clearing the hold is a record edit
only. If it says otherwise, the change must be an explicit, documented transform, never a
silent rescale.
