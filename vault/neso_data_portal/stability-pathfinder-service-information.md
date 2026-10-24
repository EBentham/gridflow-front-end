---
source: "neso_data_portal"
package: "stability-pathfinder-service-information"
dataset_keys: ["stability_pathfinder_availability_report", "stability_pathfinder_utilisation_report"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
eligibility_scope: "package-level only; both families are held (E-SEM, RULINGS 642), see Holds"
page:
  title: Stability Pathfinder availability and utilisation
  summary: >-
    NESO's indicative record, by settlement period, of Stability Pathfinder units' availability and
    any instructions its control room gave them.
  facts:
    vendor: "NESO Data Portal, package `stability-pathfinder-service-information`: eight CSV files"
    cadence: Weekly, as NESO lists it; about a week after delivery, NESO says
    grain: "Rows by unit and settlement period; one file per report and financial year"
  landscape: market
  what_it_is: >-
    Units on NESO's Stability Pathfinder contracts provide a stability service. Two reports, yearly
    files from 2023-2024, give, for every unit and settlement period, its declared availability and
    its instruction code, mostly none, with any start or cease times and an `Inertia` figure of no
    stated unit. NESO says times are local, but each ends `+00:00`. Grid Forming Batteries are excluded.
  how_used:
    - Which contracted units were available, or instructed, for stability in each settlement period
    - "Compare with NESO's Stability Y-1 utilisation report"
  chart:
    type: bar
    silver: neso_data_portal/stability_pathfinder_utilisation_report
    filter:
      - {column: resource_id, op: eq, value: 75996c0a-70fb-4ddb-a345-bb1e8d39de35}
      - {column: instruction_code, op: ne, value: "No"}
    dedup: {"on": [resource_id, unit, settlement_period_start_date_time, settlement_period_end_date_time, instruction_code, instruction_issue_time, actual_service_start_or_cease_time, inertia], order_by: capture_written_at}
    group: unit
    aggregation: count
    sort: value_desc
    unit: instructions
  chart_view:
    title: Start and cease instructions by unit, April to October 2026
    caption: >-
      Silver `neso_data_portal/stability_pathfinder_utilisation_report`, NESO's 2026-2027 file last
      modified 9 October 2026, periods to 4 October: rows with a start or cease instruction, per
      unit. Four units had none. Files for 2024-2025 (one identical repeat) and 2025-2026 (3,964) have no table.
    alt: >-
      Horizontal bar chart from neso_data_portal/stability_pathfinder_utilisation_report of rows with
      a start or cease instruction per unit in NESO's 2026-2027 file, 58 in all. KILLSC-2 and
      PMBSC-61 have 15 each; KTHRS-1 has 6; LRDSC-1, LRDSC-2 and NLSSC-1 have 4 each; BEASC-1 has 3;
      GRTSC-1, KTHRS-2 and THRSC-1 have 2 each; RTHSC-1 has 1.
    key:
      - {series: count, label: Instructions, paint: petrol}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then each financial-year file whole unless its
      `last_modified` is unchanged. Swap in either table's key.
    commands:
      - {run: gridflow ingest neso_data_portal stability_pathfinder_utilisation_report --last 24h, comment: "whole files; swap in either key"}
      - {run: gridflow transform neso_data_portal stability_pathfinder_utilisation_report --last 24h, comment: "to silver; availability builds none"}
  record:
    select:
      filter:
        - {column: resource_id, op: eq, value: 75996c0a-70fb-4ddb-a345-bb1e8d39de35}
        - {column: unit, op: eq, value: KILLSC-2}
        - column: settlement_period_start_date_time
          op: in
          value: ["2026-06-25T05:30:00+00:00", "2026-06-25T06:00:00+00:00", "2026-06-25T06:30:00+00:00",
                  "2026-06-25T07:00:00+00:00", "2026-06-25T07:30:00+00:00", "2026-06-25T08:00:00+00:00",
                  "2026-06-25T08:30:00+00:00"]
      dedup: {"on": [resource_id, unit, settlement_period_start_date_time, settlement_period_end_date_time, instruction_code, instruction_issue_time, actual_service_start_or_cease_time, inertia], order_by: capture_written_at}
      order_by: [settlement_period_start_date_time, instruction_issue_time]
      columns: [unit, settlement_period_start_date_time, instruction_code, instruction_issue_time,
                actual_service_start_or_cease_time, inertia, settlement_period_end_date_time]
    key: [resource_id, unit, settlement_period_start_date_time, instruction_code, instruction_issue_time]
    caption: "KILLSC-2 on 25 June 2026: two instructions share one period, and `Inertia` changes."
    fields:
      unit: "The contracted unit, as NESO writes it; a BM unit id where one exists"
      settlement_period_start_date_time: "Period start as NESO writes it, text ending `+00:00`; NESO says local time"
      instruction_code: "`No` (no instruction issued this period), `Service Start` or `Service Cease`"
      instruction_issue_time: "When NESO issued the instruction, in the same text form; blank on `No` rows"
      actual_service_start_or_cease_time: "When the service actually started or ceased, same text form; blank on `No` rows"
      inertia: "NESO's `Inertia` figure, with no unit stated; blank in most 2023-2024 rows"
      settlement_period_end_date_time: "Period end, 30 minutes after the start, in the same text form"
      resource_id: "NESO's id for the financial-year file the row came from"
      timestamp_utc: "gridflow's capture time, UTC; not the settlement period"
      published_at: "When NESO last changed the file (CKAN `last_modified`), read as UTC"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      `data.sql` reads the `_latest` view, each file's newest capture. The time columns are NESO's
      text and `timestamp_utc` is the capture time, so `query()` cannot pick periods.
    cells:
      - |
        files = data.sql("""
            SELECT min(settlement_period_start_date_time) AS first_start,
                   max(settlement_period_start_date_time) AS last_start,
                   count(*) AS rows, count(inertia) AS inertia_given,
                   count(*) FILTER (WHERE instruction_code <> 'No') AS instructions
            FROM silver_neso_data_portal_stability_pathfinder_utilisation_report_latest
            GROUP BY resource_id ORDER BY first_start""")
        files
      - |
        data.sql("""
            SELECT right(settlement_period_start_date_time, 6) AS offset, count(*) AS rows
            FROM silver_neso_data_portal_stability_pathfinder_utilisation_report_latest
            GROUP BY 1""")
      - |
        ins = data.sql("""
            SELECT unit, count(*) AS instructions,
                   CASE WHEN resource_id = '52af0f68-e1c3-45dd-ae7f-54f68e32e0c6'
                        THEN '2023-2024' ELSE '2026-2027' END AS file
            FROM silver_neso_data_portal_stability_pathfinder_utilisation_report_latest
            WHERE instruction_code <> 'No' GROUP BY ALL""")
        ins.pivot_table(index="unit", columns="file", values="instructions", fill_value=0).plot.barh(
            color=["#C77E3C", "#155A6E"], figsize=(8, 4),
            xlabel="rows with a start or cease instruction", ylabel="unit");
    needs: the 2023-2024 and 2026-2027 utilisation files
    plot_alt: >-
      Horizontal bar chart of rows with a start or cease instruction per unit, in the 2023-2024 and
      2026-2027 files. CRUA-3 leads 2023-2024 with 38, then LRDSC-2 19 and LRDSC-1 15. In 2026-2027,
      KILLSC-2 and PMBSC-61 lead with 15 each.
  family:
    slug: stability-pathfinder-service-information
    members:
      - dataset: stability_pathfinder_utilisation_report
        differs: "Every unit and settlement period: instruction code, mostly `No`, start or cease times, `Inertia`"
        request:
          - "GET https://api.neso.energy/dataset/ae59b12b-4cfe-40a0-844f-1d139c63d893/resource/52af0f68-e1c3-45dd-ae7f-54f68e32e0c6/download/stability-pathfinder-utilisation-report-2023.csv"
          - "GET https://api.neso.energy/dataset/ae59b12b-4cfe-40a0-844f-1d139c63d893/resource/f43f5d61-b51f-45f9-a7e7-66f2959d38b5/download/stability-pathfinder-utilisation-report-2024.csv"
          - "GET https://api.neso.energy/dataset/ae59b12b-4cfe-40a0-844f-1d139c63d893/resource/fc08cdba-1a86-460b-85c4-3d8c0d3d4e42/download/stability-pathfinder-utilisation-report-2025.csv"
          - "GET https://api.neso.energy/dataset/ae59b12b-4cfe-40a0-844f-1d139c63d893/resource/75996c0a-70fb-4ddb-a345-bb1e8d39de35/download/stability-pathfinder-utilisation-report-2026.csv"
        caveat: "Times end `+00:00` though NESO says local; `Inertia`'s unit, its blanks and row identity are unexplained."
      - dataset: stability_pathfinder_availability_report
        differs: "Each unit's declared availability by settlement period, with remarks on changes"
        request:
          - "GET https://api.neso.energy/dataset/ae59b12b-4cfe-40a0-844f-1d139c63d893/resource/a4fd8208-3e36-4f9c-bdc7-435c3734a2da/download/stability-pathfinder-availability-report-2023.csv"
          - "GET https://api.neso.energy/dataset/ae59b12b-4cfe-40a0-844f-1d139c63d893/resource/bacc45e5-11ac-4bac-88ef-6872f499db97/download/stability-pathfinder-availability-report-2024.csv"
          - "GET https://api.neso.energy/dataset/ae59b12b-4cfe-40a0-844f-1d139c63d893/resource/1264f36f-27ce-4ed9-aab1-393c7612d6bc/download/stability-pathfinder-availability-report-2025.csv"
          - "GET https://api.neso.energy/dataset/ae59b12b-4cfe-40a0-844f-1d139c63d893/resource/690a9e42-20e2-4b0e-b74f-f3e37cac4bac/download/stability-pathfinder-availability-report-2026.csv"
        held: "Every file repeats identical rows with nothing to tell them apart, so no table is built."
  related:
    - {dataset: neso_data_portal/system-inertia, note: "NESO's GB inertia estimate, in GVA.s; it leaves Pathfinder units out"}
    - {dataset: neso_data_portal/stability-midterm-y-1-utilisation-report, note: "Instructions under NESO's Stability Y-1 contracts, with contracted inertia"}
    - {dataset: neso_data_portal/system-inertia-cost, note: "Price of inertia bought through Balancing Mechanism offers, not by contract"}
---

# Stability Pathfinder service information

NESO's **indicative availability and utilisation record for the Stability Pathfinder contracts**
(vendor wording, captured package notes). The vendor says the information is given at
settlement-period resolution for all contracted units. The package ships two report types, each
as one CSV per financial year (2023-2024 to 2026-2027):

- **Availability report**: per unit and settlement period, an availability flag and a free-text
  remark that records changes (captured field-info).
- **Utilisation report**: per unit and settlement period, an instruction code, the instruction
  issue time, the actual service start or cease time and an `Inertia` figure.

The Stability Pathfinder contracts procure system-stability services (the package carries an
inertia column). The mechanism and what the `Inertia` figure represents in contract terms are not
described in the captured notes or field-info: `TODO: verify` against the Stability Pathfinder
contract documents. The vendor says that for long-term stability services no utilisation payment
is made, so the dataset is updated roughly a week after delivery, and that Grid Forming Batteries
are **not** included, because the NESO control room is not required to instruct that technology
for stability purposes. The package is a delivered-state record, not a forecast. It carries no
publication or instruction-availability column. Read it alongside the system inertia package
(@system-inertia.md) and the mid-term utilisation report (@stability-midterm-y-1-utilisation-report.md).

**Both silver families are held (unit E-SEM): neither is eligible for point-in-time use, and
gridflow's models do not consume them until the questions below are answered.** The front-matter
`eligibility: eligible` is the registry's package-level status only. This note gives schema, row
counts and structural counts. The site page shows the utilisation rows, a chart and a notebook,
with a caveat naming the open questions (ruling 66); the availability family has no rows to
show. Six of the first eight captures (2026-10-08) fail the transform
(ADR-040, `DuplicateEntityKeyError`), so the availability family has **0 silver rows**.

- Publisher group: System
- Registry group: system · archetype: SER

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Stability Pathfinder Availability Report 2023-2024 | CSV | upload | `a4fd8208-3e36-4f9c-bdc7-435c3734a2da` |
| Stability Pathfinder Availability Report 2024-2025 | CSV | upload | `bacc45e5-11ac-4bac-88ef-6872f499db97` |
| Stability Pathfinder Availability Report 2025-2026 | CSV | upload | `1264f36f-27ce-4ed9-aab1-393c7612d6bc` |
| Stability Pathfinder Availability Report 2026-2027 | CSV | upload | `690a9e42-20e2-4b0e-b74f-f3e37cac4bac` |
| Stability Pathfinder Utilisation Report 2023-2024 | CSV | upload | `52af0f68-e1c3-45dd-ae7f-54f68e32e0c6` |
| Stability Pathfinder Utilisation Report 2024-2025 | CSV | upload | `f43f5d61-b51f-45f9-a7e7-66f2959d38b5` |
| Stability Pathfinder Utilisation Report 2025-2026 | CSV | upload | `fc08cdba-1a86-460b-85c4-3d8c0d3d4e42` |
| Stability Pathfinder Utilisation Report 2026-2027 | CSV | upload | `75996c0a-70fb-4ddb-a345-bb1e8d39de35` |

All eight resources carry the disposition SILVER, and they map to two families (four resources
each). The package has **no DOC resources, no HOLD resources and no skipped resources**. The
family-level holds below are not resource-level dispositions. Each resource is one annual
(financial-year) file. They are separate files, not revisions of one another. No
`(UNIT, period start)` pair repeats across resources of a family (measured, FACTS section 4 g3 and
section 5 g3). The captured download URLs (from the 2026-10-06 catalogue snapshot) and
captures (2026-10-08, `C:/gridflow-data/bronze/neso_data_portal/<family>/2026/10/08/`):

**Utilisation report** (`stability_pathfinder_utilisation_report`)

| Resource | Download | Bytes | Data rows | CKAN `last_modified` | Silver rows |
|---|---|---:|---:|---|---:|
| 2023-2024 | [stability-pathfinder-utilisation-report-2023.csv](https://api.neso.energy/dataset/ae59b12b-4cfe-40a0-844f-1d139c63d893/resource/52af0f68-e1c3-45dd-ae7f-54f68e32e0c6/download/stability-pathfinder-utilisation-report-2023.csv) | 7,487,598 | 110,891 | `2024-04-05T15:45:09.278460` | 110,891 |
| 2024-2025 | [stability-pathfinder-utilisation-report-2024.csv](https://api.neso.energy/dataset/ae59b12b-4cfe-40a0-844f-1d139c63d893/resource/f43f5d61-b51f-45f9-a7e7-66f2959d38b5/download/stability-pathfinder-utilisation-report-2024.csv) | 13,996,566 | 198,157 | `2025-04-11T14:21:51.833357` | 0 (failed) |
| 2025-2026 | [stability-pathfinder-utilisation-report-2025.csv](https://api.neso.energy/dataset/ae59b12b-4cfe-40a0-844f-1d139c63d893/resource/fc08cdba-1a86-460b-85c4-3d8c0d3d4e42/download/stability-pathfinder-utilisation-report-2025.csv) | 18,086,315 | 258,388 | `2026-04-10T15:11:46.723351` | 0 (failed) |
| 2026-2027 | [stability-pathfinder-utilisation-report-2026.csv](https://api.neso.energy/dataset/ae59b12b-4cfe-40a0-844f-1d139c63d893/resource/75996c0a-70fb-4ddb-a345-bb1e8d39de35/download/stability-pathfinder-utilisation-report-2026.csv) | 8,708,369 | 123,987 | `2026-10-02T14:49:24.733259` | 123,987 |

Total 691,423 bronze rows, 234,878 silver rows.

**Availability report** (`stability_pathfinder_availability_report`)

| Resource | Download | Bytes | Data rows | CKAN `last_modified` | Silver rows |
|---|---|---:|---:|---|---:|
| 2023-2024 | [stability-pathfinder-availability-report-2023.csv](https://api.neso.energy/dataset/ae59b12b-4cfe-40a0-844f-1d139c63d893/resource/a4fd8208-3e36-4f9c-bdc7-435c3734a2da/download/stability-pathfinder-availability-report-2023.csv) | 8,026,553 | 110,887 | `2024-04-05T15:44:41.388092` | 0 (failed) |
| 2024-2025 | [stability-pathfinder-availability-report-2024.csv](https://api.neso.energy/dataset/ae59b12b-4cfe-40a0-844f-1d139c63d893/resource/bacc45e5-11ac-4bac-88ef-6872f499db97/download/stability-pathfinder-availability-report-2024.csv) | 14,429,386 | 199,201 | `2025-04-11T14:19:34.799957` | 0 (failed) |
| 2025-2026 | [stability-pathfinder-availability-report-2025.csv](https://api.neso.energy/dataset/ae59b12b-4cfe-40a0-844f-1d139c63d893/resource/1264f36f-27ce-4ed9-aab1-393c7612d6bc/download/stability-pathfinder-availability-report-2025.csv) | 21,533,621 | 297,478 | `2026-04-10T15:12:15.650724` | 0 (failed) |
| 2026-2027 | [stability-pathfinder-availability-report-2026.csv](https://api.neso.energy/dataset/ae59b12b-4cfe-40a0-844f-1d139c63d893/resource/690a9e42-20e2-4b0e-b74f-f3e37cac4bac/download/stability-pathfinder-availability-report-2026.csv) | 9,582,437 | 132,011 | `2026-10-02T14:49:34.759439` | 0 (failed) |

Total 739,577 bronze rows, 0 silver rows.

**Recapture of the 2026-2027 files (2026-10-16).** Both 2026-2027 files were captured again on
2026-10-16, each with a new CKAN `last_modified` on 2026-10-09 and the same header:
`raw_20261016T204636Z_690a9e42-…_dca03343.csv` (availability, 9,967,333 bytes, 137,322 data rows,
`last_modified` `2026-10-09T11:59:40.725801`) and `raw_20261016T204639Z_75996c0a-…_17e4ffc7.csv`
(utilisation, 9,062,177 bytes, 129,027 data rows, `last_modified` `2026-10-09T11:59:11.232115`).
The six past-year files kept their `last_modified` and were not downloaded again. Measured by the
project from bronze on 2026-10-23: each new file holds exactly as many rows as the 2026-10-08
capture up to its last period start (`2026-09-27T23:30:00+00:00`), every distinct row of the older
capture appears unchanged, and one more week of periods follows (starts to
`2026-10-04T23:30:00+00:00`). Every period start still ends `+00:00` and falls in British Summer
Time. Duplicate excess in the new availability file is 7,943 on all vendor columns and 9,650 on
`(UNIT, period start)`; in the new utilisation file, 0 and 3. The utilisation capture transformed
to a third silver file of 129,027 rows; the availability family still has no silver directory.

The stable handle for each file is its resource id, not the URL. CKAN `last_modified` values are
emitted without an offset and read as UTC (gridflow
`@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). Within a family, all resources share
one header (a single epoch). The resource filenames end in the calendar year in which the
financial year starts (2023 for 2023-2024).

## Families

### `stability_pathfinder_availability_report`

- Kind: tabular · archetype: SER · refresh: weekly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| UNIT | `unit` | string | — | no | — | — |
| Settlement Period Start Date Time | `settlement_period_start_date_time` | string | — | no | — | — |
| Settlement Period End Date Time | `settlement_period_end_date_time` | string | — | no | — | — |
| Availability Flag | `availability_flag` | string | — | no | — | — |
| REMARK | `remark` | string | — | yes | — | — |

- Entity key: `resource_id`, `unit`, `settlement_period_start_date_time`, `settlement_period_end_date_time`, `availability_flag`, `remark`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the CKAN `last_modified`
   of the captured resource. Each of the four files has its own vintage (table above). The files
   carry **no issue or publication column**: nothing says when an individual row first became
   public. The older files' vintages (2024 and 2025) are therefore a late upper bound on
   availability for their rows. No source establishes that report contents are immutable once
   issued. Silver for this family is empty, so no per-row check against silver was possible.
2. **Event time (`none`).** The record's temporal recipe is `none`. A `timestamp_utc` would
   therefore be the **capture time** (`capture_written_at`, 2026-10-08), not a settlement-period
   instant. It carries no information about the period a row describes. The settlement-period
   boundaries stay in the two raw string columns. Do not filter or order by `timestamp_utc`
   expecting event order. Because the family has no silver rows, this is a statement of the record,
   not of a checked silver column.

**Raw-string time columns, and the clock conflict.** The vendor package notes say time values are
"all given in local time" (the zone name is missing from the captured description text, so
the exact zone wording is `TODO: verify`). Every nonblank boundary timestamp in the bodies
nevertheless ends in a literal `+00:00` offset, and displayed end minus start is 1,800 seconds
throughout. Two readings are possible: GB local wall times with a mechanically attached zero
offset, or true UTC instants. If the displayed wall times were Europe/London, a large number of
start literals on British Summer Time dates would carry the wrong offset, and the 2023-2024 to
2025-2026 files contain wall times that do not exist in London (the spring-forward gap). The
2026-2027 file shows no such gap values in its range, but every one of its start literals sits
in British Summer Time and so conflicts with a London reading. gridflow does **not** pick a reading. It
stores both boundary columns as **raw strings**, does not strip or relabel the offset, and builds
no UTC event time. Stripping the offset and declaring London instants is ruled out by the
nonexistent wall times. `TODO: verify` with NESO which reading is correct, including the treatment of clock-change
periods and repeated or nonexistent local times.

**Units.** None. The family has no measured-value column. `unit` is a unit identifier (BMU ID
where applicable, per the field-info). `availability_flag` and `remark` are categorical and
free text. No MW, MVA, MVA.s or currency unit applies. `remark` can embed timestamps inside its
free text, but it is vendor free text and not a typed time column. Identifiers are stored as-is.

**Sentinels and missing values (FACTS g5).** The record declares no null token.

- `remark` is blank on 110,792 / 198,942 / 297,094 / 131,760 rows in resource order (2023-2024 to
  2026-2027). Blank remark is a nullable, preserved value. It is not a sentinel.
- Observed flag literals in bronze: `Available`, `Unavailable`, and one occurrence of a misspelt
  `Unvailable`. Stored as supplied; no normalisation to a documented flag without an explicit rule.
- No `-1`, `N/A` or `NA` literal was found.

**Identity, duplicates and why the family fails.** The vendor documents no row identity or grain,
and no contract identifier column exists. Identical complete rows repeat inside every capture
(duplicate excess, meaning occurrences after the first, counted on all vendor columns):

| Resource | Duplicate excess, all vendor columns | Duplicate excess, `(UNIT, period start)` |
|---|---:|---:|
| 2023-2024 | 306 | 312 |
| 2024-2025 | 1,003 | 1,061 |
| 2025-2026 | 46,921 | 49,786 |
| 2026-2027 | 7,679 | 9,379 |

No subset of the supplied columns distinguishes identical complete rows, so no supplied-column key
can keep them as distinct entities. gridflow therefore does not deduplicate and adds no occurrence
index. The transform raises `DuplicateEntityKeyError` on every capture, so all four captures are
adjudicated **failed** under ADR-040
(`@docs/DECISION_LOG/ADR-040-neso-reconcile-adjudication.md`; RULINGS 642) and the family has
**0 silver rows**. Verified independently with `polars.unique()` on 2026-10-10 (RESULTS and
VERIFICATION). `TODO: verify` what vendor row identity or grain makes the report unique, or
whether NESO will publish corrected uploads without the unintended identical records.

### `stability_pathfinder_utilisation_report`

- Kind: tabular · archetype: SER · refresh: weekly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| UNIT | `unit` | string | — | no | — | — |
| Settlement Period Start Date Time | `settlement_period_start_date_time` | string | — | no | — | — |
| Settlement Period End Date Time | `settlement_period_end_date_time` | string | — | no | — | — |
| Instruction Code | `instruction_code` | string | — | no | — | — |
| Instruction Issue Time | `instruction_issue_time` | string | — | yes | — | — |
| Actual Service Start or Cease Time | `actual_service_start_or_cease_time` | string | — | yes | — | — |
| Inertia | `inertia` | int64 | — | yes | — | — |

- Entity key: `resource_id`, `unit`, `settlement_period_start_date_time`, `settlement_period_end_date_time`, `instruction_code`, `instruction_issue_time`, `actual_service_start_or_cease_time`, `inertia`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the CKAN `last_modified`
   of the captured resource. Checked on every silver row on 2026-10-10: the two clocks are equal,
   each resource's rows share one value, and it equals the vintage in the table above
   (`2024-04-05T15:45:09` for 2023-2024, `2026-10-02T14:49:24` for 2026-2027). The files carry
   **no report-publication column**. `Instruction Issue Time` is not one: it is the time a
   start or cease instruction was issued, it is blank on 690,163 of the 691,423 bronze rows, and
   rows without a new instruction still report service state. The vendor describes publication
   after delivery. Nothing establishes that report contents are immutable or were public at
   instruction time, so the upload vintage is the only availability evidence.
2. **Event time (`none`).** The record's temporal recipe is `none`. So `timestamp_utc` =
   `event_time` = the **capture time** (`capture_written_at`, 2026-10-08), not a
   settlement-period instant. Checked equal on every silver row on 2026-10-10 (234,878 rows).
   There is no independent date and settlement-period pair, and the time columns cannot be
   faithfully read as instants while the clock conflict stands, so no instant is built. The
   period and instruction times stay in the raw string columns. Do not filter or order by
   `timestamp_utc` expecting event order.

**Raw-string time columns, and the clock conflict.** The same conflict as the availability family
applies to all four time columns (`settlement_period_start_date_time`,
`settlement_period_end_date_time`, `instruction_issue_time`,
`actual_service_start_or_cease_time`). The vendor says time values are in local time. Every
nonblank time cell parses as an offset datetime carrying a literal `+00:00`, and displayed end
minus start is 1,800 seconds throughout. If the displayed wall times were Europe/London, a large
number of start literals on British Summer Time dates would carry the wrong offset, and the
2023-2024 to 2025-2026 files contain wall times that do not exist in London (the spring-forward
gap). The 2026-2027 file shows none in its range, but every one of its start literals
sits in British Summer Time and so conflicts with a London reading. gridflow stores the columns as **raw strings**,
does not strip or relabel the offset, and builds no UTC event time (the same ruling as the CMIS
package). `TODO: verify` with NESO whether the values are actual UTC instants or GB local wall
times with a mechanically attached `+00:00`, including clock-change periods and repeated or
nonexistent local times.

**Units (vendor dictionary only, as cited in FACTS).**

- `Inertia` → `inertia`: **unit and scale not stated.** The upload's field-info gives the column
  no unit. NESO's stability procurement documents use MVA.s for inertia, but nothing inspected
  connects that scale to this column. The unit is **not** assigned from the column name or from
  magnitudes. `TODO: verify` (unit E-SEM). Do not combine this column with `system_inertia`
  (GVAs) or the mid-term report (MVA.s) until the unit is settled.
- `unit` is a unit identifier (BMU ID where applicable). There is no separate contract
  identifier column. Identifiers are stored as-is, including look-alike codes that differ by one
  character, with no normalisation.
- `instruction_code`, the time columns and the identifiers carry no physical unit. No MW, MVA or
  currency column exists in this family.

**`instruction_code` meaning.** The vendor dictionary describes the code's `No` value as no
instruction issued in the period. It does not mean no service was being delivered: `No` rows
carry an inertia figure. The full code vocabulary is not described in the captured notes
(`TODO: verify`). Codes are stored as supplied.

**Sentinels and missing values (FACTS g5).** The record declares no null token.

| Resource | Blank `Inertia` | Blank issue time = blank actual start or cease time |
|---|---:|---:|
| 2023-2024 | 92,408 | 110,807 |
| 2024-2025 | 69 | 197,543 |
| 2025-2026 | 574 | 257,884 |
| 2026-2027 | 0 | 123,929 |

- Blank cells are preserved as null. A blank `Inertia` is not turned into zero and its row is not
  excluded. What a blank means (especially in the 2023-2024 file, where it is widespread) is
  undefined by the vendor. `TODO: verify` with NESO. Measured on silver on 2026-10-24: in the
  2023-2024 file every row with a period start from September 2023 to January 2024 is blank,
  13,202 of 15,314 in February 2024 are, and none in March 2024.
- Zero `Inertia` values occur in the bodies. They are vendor-supplied values and are preserved
  as-is. The vendor does not define what a zero means. This note gives no value statistics; the
  site page shows the rows with a caveat that a blank is unexplained.
- No literal `-1`, `N/A` or `NA` was found. No thousands separators, currency symbols or percent
  signs occur in numeric cells, and every nonblank `Inertia` passes the int64 cast.

**Identity, duplicates and selection.** The vendor documents no row identity. Multiple
instructions can fall inside one settlement period, so `(UNIT, period start)` is not unique:
duplicate excess on that pair is 11, 13, 5,352 and 3 across the four files in resource order.
The conservative entity key is `resource_id` plus every vendor column. Duplicate excess on that
full key is 0, 1, 3,964 and 0:

| Resource | Duplicate excess, all vendor columns | Transform result |
|---|---:|---|
| 2023-2024 | 0 | 110,891 silver rows |
| 2024-2025 | 1 | `DuplicateEntityKeyError`, adjudicated **failed** |
| 2025-2026 | 3,964 | `DuplicateEntityKeyError`, adjudicated **failed** |
| 2026-2027 | 0 | 123,987 silver rows |

No subset of the supplied columns distinguishes the identical rows, so gridflow does not
deduplicate and adds no occurrence index (ADR-040; RULINGS 642). `_latest` is `whole_capture`
partitioned by `resource_id`: the newest capture of each resource replaces its previous capture as
a whole, and the other three resources are untouched. `TODO: verify` the vendor row identity.

**Activation (2026-10-10, master `4d06b9f`, PR #105).** Transformed at window 2026-10-08 to
2026-10-10 (four captures, no prior silver): **234,878 silver rows** = 110,891 + 123,987, equal
to the planned count. The 2024-2025 and 2025-2026 captures failed as designed. Reconcile
`--all --cutoff 2026-10-10` exited 0 with 113 families, 0 gaps, 21 adjudicated and 0 stale
(gridflow `@.planning/v0.22-RESULTS.md` section SYS-1; RULINGS 646, 647). Silver is stored as one
Parquet file per successfully transformed capture under
`silver/neso_data_portal/stability_pathfinder_utilisation_report/year=2026/month=10/`. Silver
columns beyond the vendor columns: `resource_id`, `timestamp_utc`, `published_at`,
`bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id`,
`dataset_version` (timestamps tz-aware UTC; `dataset_version` reads `1+e1`, where `e1` is the
engine version, not the header epoch). The silver is not eligible for point-in-time use; the
site page shows its rows with a caveat (ruling 66). The availability family has no silver
directory at all.

## Cadence

- Registry refresh: weekly
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Weekly
- Captures to date: one per resource on 2026-10-08, and the two 2026-2027 files again on
  2026-10-16 (see Files by disposition).

The vendor says the dataset is updated approximately a week after delivery. The 2026-2027 files are
the current year: both carry the most recent vintages (`2026-10-02` at the first capture,
`2026-10-09` at the second), and the earlier years have not changed since April 2024 to April 2026.
Between the two captures the 2026-2027 files only gained a week of rows, with no earlier row
changed. `TODO: verify` whether past-year files are ever restated. Only repeated captures compared
row by row can show this. `TODO: verify` whether a new
financial-year file appears as a new resource and what gridflow must change to capture it.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `stability_pathfinder_availability_report`: held: TODO: the timestamp clock (as §3), and what vendor row identity / grain makes the report unique given identical repeated rows? (unit E-SEM)
- `stability_pathfinder_utilisation_report`: held: TODO: are the Pathfinder timestamps actual UTC instants or GB local wall times with a mechanically attached +00:00 offset (incl. clock-change periods), what unit/scale is `Inertia`, what does a blank `Inertia` mean, and what vendor row identity distinguishes identical rows? (unit E-SEM)

Both families are held by RULINGS 642 (seat ruling, PROXY-SOURCED). The section reference "§3"
in the availability question points into the SYS-1 spec (`K-SYS-1-SPEC.md`):
in the spec, §3 is the utilisation-report section, whose timestamp-clock question the availability
report shares. It is reproduced verbatim from the registry. The utilisation silver output (234,878 rows
at activation, plus a third file of 129,027 rows from the 2026-10-16 capture) is not eligible for point-in-time use, and downstream models must not consume it; the site page shows its rows with a caveat naming these questions (ruling 66). Unit E-SEM must answer these
before the holds can lift:

1. Whether the boundary and instruction timestamps are GB local wall time with a mechanically
   attached `+00:00`, or true UTC instants. Until then no event instant is built and the temporal
   recipe stays `none`. Resolving this would change the event-time recipe and so needs a new
   record version. It is not a re-label of existing silver.
2. What unit and scale the utilisation `Inertia` column carries, and what a blank `Inertia` means.
   Until then the column is not combined with any other inertia quantity.
3. What vendor row identity or grain makes each report unique given the identical repeated rows.
   The repeats are why six captures are adjudicated **failed** (utilisation 2024-2025 and
   2025-2026; availability all four, the whole of that family). Resolving this needs a vendor row
   or contract identifier with a grain definition, or corrected uploads that remove the unintended
   identical records.

Related holds in the same batch (gridflow `@docs/neso_data_portal/eligibility.md`): the
`system_inertia_cost` resource `6295f4ed-b43d-4a80-8ca9-c27c9fa16517` is held at resource level
(an ambiguous slash date under a filename shared with ISO-dated resources, unit SYS-1). The
other SYS-1 families, `voltage_units_utilisation`, `stability_midterm_y1`, `system_inertia` and
both `outturn_voltage_costs` families, are eligible.
