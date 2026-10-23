---
source: "neso_data_portal"
package: "stability-midterm-y-1-utilisation-report"
dataset_key: "stability_midterm_y1"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-10
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Stability Y-1 utilisation
  summary: >-
    NESO's control-room instructions to units on Stability Y-1 contracts: start and cease, which NESO
    gives in GMT, hours and contracted inertia.
  facts:
    vendor: "NESO Data Portal, package `stability-midterm-y-1-utilisation-report`: one CSV file"
    cadence: "Monthly in NESO's catalogue, shortly after that month's service payments are made"
    grain: "One row per instruction: unit, start, cease, hours and contracted inertia"
    history: "Contracts for delivery October 2025 to September 2026, as NESO's package text states"
  landscape: market
  what_it_is: >-
    Units holding a NESO Stability midterm (Y-1) contract, here for delivery October 2025 to
    September 2026, are utilised when NESO's control room instructs them. Each row is one
    instruction: the unit, its contracted inertia in MVA.s, start and cease times, which NESO gives
    in GMT, and the hours utilised. NESO calls the report indicative and does not define Y-1 here.
  how_used:
    - "Which contracted units NESO's control room called on, and in which months."
    - Hours instructed per unit and month, worked out from the start and cease times.
    - "Contracted inertia in MVA.s, beside NESO's GB inertia estimate in GVA.s."
  chart:
    type: stacked-area
    silver: neso_data_portal/stability_midterm_y1
    time: month_and_year
    filter:
      - {column: published_at, op: eq, value: "2026-09-28T16:54:21.377483"}
    dedup: {"on": [bmu_id, utilisation_start_datetime, utilisation_end_datetime], order_by: capture_written_at}
    group: bmu_id
    group_map: {DEEPS-1: deeps, HIRWN-1: hirwn, CRUA-2: crua2, CRUA-4: crua4}
    series_order: [deeps, hirwn, crua2, crua4]
    aggregation: count
    window: {start: "2025-10-01", end: "2026-08-31"}
    unit: instructions
  chart_view:
    title: Instructions per month by unit, October 2025 to August 2026
    caption: >-
      Silver `neso_data_portal/stability_midterm_y1`, file last modified 28 September 2026:
      instructions by NESO's month label (in this file, the month each ends), stacked by unit. No
      instructions December to March; NESO says a month without an update means the service was unused.
    alt: >-
      Stacked area chart of instructions per month from neso_data_portal/stability_midterm_y1, by
      NESO's month label, October 2025 to August 2026. CRUA-4 alone has 2 in October and 1 in
      November 2025, then nothing from December to March. From April 2026 DEEPS-1 has 6, 8, 5, 6 and
      8 a month; HIRWN-1 joins in May with 2, then 5, 10 and 6; CRUA-2 has 1 each in May and June.
      July is highest, 16 in all.
    x_label: month as NESO labels each instruction
    key:
      - {series: deeps, label: DEEPS-1, codes: DEEPS-1, paint: hatch-lines, note: "3,052 MVA.s contracted inertia; instructed April to August 2026. Absent from Elexon's BM unit register, 26 September 2026."}
      - {series: hirwn, label: HIRWN-1, codes: HIRWN-1, paint: hatch-dots, note: "Contracted inertia 496 MVA.s. Elexon's register of 26 September 2026 lists HIRWN-1 as OCGT."}
      - {series: crua2, label: CRUA-2, codes: CRUA-2, paint: hatch-cross, note: "Contracted inertia 483 MVA.s. Elexon's register of 26 September 2026 lists CRUA units as pumped storage."}
      - {series: crua4, label: CRUA-4, codes: CRUA-4, paint: hatch-vertical, note: "Contracted inertia 483 MVA.s; the only unit instructed in October and November 2025."}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then the one CSV file downloaded whole unless its
      `last_modified` is unchanged; dates select nothing.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=stability-midterm-y-1-utilisation-report"
      - "GET https://api.neso.energy/dataset/84abeae2-be21-4755-bbfc-3792f5315a36/resource/e0c86d21-8ad1-4ba3-a112-b2bbcf5277ce/download/stability.csv"
    commands:
      - {run: gridflow ingest neso_data_portal stability_midterm_y1 --last 24h, comment: "whole file; window must end recently"}
      - {run: gridflow transform neso_data_portal stability_midterm_y1 --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: published_at, op: eq, value: "2026-09-28T16:54:21.377483"}
        - column: utilisation_start_datetime
          op: in
          value: ["2025-10-04T21:12:00", "2025-11-10T16:01:00", "2026-04-03T20:45:00", "2026-04-28T22:44:00",
                  "2026-05-26T13:00:00", "2026-06-02T22:41:00", "2026-07-13T06:24:00", "2026-07-13T06:34:00"]
      dedup: {"on": [bmu_id, utilisation_start_datetime, utilisation_end_datetime], order_by: capture_written_at}
      order_by: [utilisation_start_datetime, bmu_id]
      columns: [bmu_id, month_and_year, utilisation_start_datetime, utilisation_end_datetime, hours_utilised,
                inertia_mva_s, timestamp_utc, published_at]
    key: [bmu_id, utilisation_start_datetime, utilisation_end_datetime]
    caption: "Eight instructions, all four units, from NESO's file last modified 28 September 2026."
    fields:
      bmu_id: "The instructed balancing mechanism unit, as NESO writes it"
      month_and_year: "NESO's month label, read as the 1st; in this file, the month it ends"
      utilisation_start_datetime: "Start of the instruction; NESO gives GMT, read as UTC with no clock change"
      utilisation_end_datetime: "Cease time of the instruction; GMT, read as UTC with no clock change"
      hours_utilised: "NESO's duration as text, `HH:MM:SS` or `HH:MM`; four April rows are 12 seconds off"
      inertia_mva_s: "The unit's contracted inertia in MVA.s, as NESO's dictionary gives it"
      timestamp_utc: "The start again, in UTC: the column `query()` filters on"
      published_at: "NESO's last-modified time for the whole file, read as UTC"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      `query()` reads the table's `_latest` view, filtering `timestamp_utc`, the start, by UTC day with both ends included; lineage columns dropped. Times come back in UK
      time, so the first cell converts them to UTC.
    cells:
      - |
        df = data.neso_data_portal.query("stability_midterm_y1", "2025-10-01", "2026-08-31")
        times = ["utilisation_start_datetime", "utilisation_end_datetime", "timestamp_utc"]
        df[times] = df[times].apply(lambda c: c.dt.tz_convert("UTC"))
        df = df.sort_values(["utilisation_start_datetime", "bmu_id"], ignore_index=True)
        df[["bmu_id", "month_and_year", "utilisation_start_datetime", "utilisation_end_datetime", "hours_utilised"]].head()
      - |
        hours = (df.utilisation_end_datetime - df.utilisation_start_datetime).dt.total_seconds() / 3600
        parts = df.hours_utilised.str.split(":", expand=True).astype(float).fillna(0)
        stated = parts[0] + parts[1] / 60 + parts[2] / 3600
        off = ((stated - hours) * 3600).round().astype(int)
        df.assign(seconds_off=off).loc[off != 0, ["bmu_id", "utilisation_start_datetime", "hours_utilised", "seconds_off"]]
      - |
        import pandas as pd
        months = pd.date_range("2025-10-01", "2026-08-01", freq="MS")
        monthly = (df.assign(hours=hours, month=pd.to_datetime(df.month_and_year))
                     .pivot_table(index="month", columns="bmu_id", values="hours", aggfunc="sum")
                     .reindex(months))
        monthly.index = monthly.index.strftime("%b %y")
        monthly.round(1)
      - |
        ax = monthly.plot.bar(figsize=(8, 3.5), width=0.8, rot=0,
                              color=["#8A6D3B", "#C77E3C", "#155A6E", "#6B7F3A"],
                              xlabel="NESO month label", ylabel="hours, cease minus start");
    needs: "NESO's Stability Y-1 utilisation file"
    plot_alt: >-
      Grouped bar chart of hours from start to cease per unit, by NESO's month label, October 2025
      to August 2026. CRUA-4's October and November bars, under 3 hours, are too short to see, and
      December to March are empty. DEEPS-1 peaks at 514.5 hours in April; HIRWN-1 runs 411.6 to
      467.1 hours a month from June.
  related:
    - {dataset: neso_data_portal/system-inertia, note: "GB inertia each half-hour in GVA.s; 1 GVA.s is 1,000 MVA.s"}
    - {dataset: neso_data_portal/stability-pathfinder-service-information, note: "Availability and utilisation of units on NESO's Stability Pathfinder contracts"}
    - {dataset: neso_data_portal/monthly-utilisation-data-of-voltage-contracted-units, note: "NESO's monthly utilisation report for units on voltage contracts"}
    - {dataset: elexon/bmunits_reference, note: "Elexon's 26 September 2026 register: fuel type and capacity of CRUA, HIRWN"}
---

# Stability midterm (Y-1) utilisation report

Delivered-utilisation report for NESO's stability midterm (Y-1) service: one row per
instructed interval in which a contracted balancing-mechanism unit (BMU) was utilised to
provide system inertia, with the unit's contracted inertia, the start and end of the interval,
and a duration text. The vendor describes the report as "an indicative overview of the monthly
utilisation" of units with a Stability Y-1 contract, "based on instructions provided by NESO's
Control Room", updated shortly after each month's service payments (catalogue snapshot
`20261006T195819Z`, package `notes`; gridflow
`@.planning/phases/v0.22-K-SYS-1/K-SYS-1-FACTS.md` section 3, g2). It is an **outturn
record**, not a forecast: there is no forecast column. Use it to see which units NESO
utilised for inertia, when, and how much contracted inertia each carried. It pairs with the
system-wide inertia series (@system-inertia.md) and the Pathfinder reports
(@stability-pathfinder-service-information.md), which describe the same stability-service
space at different grains and are not interchangeable with it. The grain here is an
**instructed interval**, not a settlement period.

`TODO: verify` what "midterm" and "Y-1" denote in the vendor's service design (the
inspected sources describe the report but do not define the service names). The package
`notes` say only that the "Stability midterm (Y-1) 25/26 contracts" cover "the delivery period
of Oct-25 to Sep-26" (catalogue snapshot `20261006T195819Z`).

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
- The package has a single resource and no DOC files. The label "25/26" is a contract year,
  not a financial year: the package `notes` give the 25/26 contracts' delivery period as Oct-25
  to Sep-26, and say that data then held in a "Stability midterm (Y-1) utilisation report 26/27"
  file is consolidated into this 25/26 file "From 15th July onwards", the 26/27 file to be
  deleted (catalogue snapshot `20261006T195819Z`). `TODO: verify` how NESO will publish later
  contract years (a new resource, a replaced file, or an appended file). The record is `whole_capture`, so any of these lands as a fresh capture.

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
  start, and do not join on it as if it were the start month. In this capture the label equals
  the month of the **end** instant on all 61 rows (the 3 above all cross a month end; checked
  in silver 2026-10-23); NESO does not state that rule. NESO's dictionary describes the column
  only as "The month and year of the utilisation period" (field-info `20261008T114228Z`).
- `utilisation_start_datetime` / `utilisation_end_datetime`: `%d/%m/%Y %H:%M`, UTC. Captured
  starts run from 2025-10-04 21:12 to 2026-08-29 22:47 UTC and ends reach 2026-08-31 14:53
  UTC. No row ends before it starts.
- `hours_utilised`: the vendor duration, kept as a **string**. Vendor unit is "Hours and
  Minutes" and the vendor example is `08:30:00`. The captured values are `HH:MM:SS` text
  (48 rows) or a two-component form (13 rows), and hours can exceed a clock-day range.
  Never converted to a number or recomputed from the boundaries: on **4** rows the stated
  duration disagrees with the boundary difference (file lines 5, 7, 8 and 9), each by 12
  seconds: three texts are 12 s longer than end minus start and one 12 s shorter, all
  `DEEPS-1` rows in April 2026 (checked in silver 2026-10-23). Treat the
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
- Only one capture exists (2026-10-08). The 2026-10-16 refresh found the file unchanged
  (gridflow `@.planning/phases/v0.22-close/refresh-20261016/ingest.log`: 0 responses
  ingested, 1 unchanged since newest capture). `TODO: verify` whether a monthly upload appends to
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
