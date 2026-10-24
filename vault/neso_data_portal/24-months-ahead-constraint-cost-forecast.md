---
source: "neso_data_portal"
package: "24-months-ahead-constraint-cost-forecast"
dataset_key: "constraint_cost_fc_24m"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: 24-month constraint cost forecast
  summary: >-
    NESO's forecast of what managing transmission constraints will cost in each of the next 24
    months, one figure per month.
  facts:
    vendor: "NESO Data Portal, package `24-months-ahead-constraint-cost-forecast`: one CSV file"
    cadence: "Monthly, as NESO lists it; each upload replaces the file"
    grain: "Each row: one month, labelled like Dec-25, with one cost figure"
  landscape: market
  what_it_is: >-
    NESO's modelled cost of managing the main transmission boundaries, month by month: thermal,
    voltage and stability constraints, plus meeting voltage requirements. NESO says it does
    not include the cost of managing inertia or the largest loss of infeed. Each month has one
    figure, with no split by boundary and no range.
  how_used:
    - A forward view of NESO's constraint spend over the next two years
    - How NESO's outlook for a month shifts from one monthly upload to the next
  chart:
    type: line
    silver: neso_data_portal/constraint_cost_fc_24m
    time: forecast_month
    value: constraint_cost
    group: bronze_capture_id
    group_map:
      "bronze/neso_data_portal/constraint_cost_fc_24m/2026/10/08/raw_20261008T091541Z_28b85d3f-a1cc-4bb9-80af-600f2cca266a_c56921b4.csv": sep
      "bronze/neso_data_portal/constraint_cost_fc_24m/2026/10/16/raw_20261016T192117Z_28b85d3f-a1cc-4bb9-80af-600f2cca266a_c46bbd3e.csv": oct
    series_order: [oct, sep]
    aggregation: last
    window: {start: "2026-10-01", end: "2028-10-01"}
    unit: "Constraint Cost, no unit in the file"
  chart_view:
    title: Constraint Cost by month, in two uploads
    caption: >-
      Silver `constraint_cost_fc_24m`: NESO's `Constraint Cost` for each forecast month, as its
      September and October 2026 uploads give it, October 2026 to October 2028. The file states no
      unit; NESO's dictionary gives £m.
    alt: >-
      Line chart from neso_data_portal/constraint_cost_fc_24m of NESO's Constraint Cost per forecast
      month, no unit in the file, in two uploads. The September 2026 upload runs from 606.2 in
      October 2026 down to 155.7 in July 2027, up to 443.7 in October 2027 and ends at 236.5 in
      September 2028. The October 2026 upload starts at 520.4 in November 2026, reaches 491.6 in
      October 2027 and ends at 474.3 in October 2028.
    x_label: forecast month, as NESO labels it
    key:
      - {series: oct, label: October 2026 upload, paint: petrol, note: "File `oct26`, last modified 9 October 2026: November 2026 to October 2028."}
      - {series: sep, label: September 2026 upload, paint: clay, note: "File `sept26`, last modified 10 September 2026: October 2026 to September 2028."}
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show`, then the file downloaded whole unless its
      `last_modified` is unchanged. The file name carries the upload month, so it changes each month.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=24-months-ahead-constraint-cost-forecast"
      - "GET https://api.neso.energy/dataset/51bb8f5a-3c95-4f7f-9a72-3b36cb7f1dc0/resource/28b85d3f-a1cc-4bb9-80af-600f2cca266a/download/24-months-ahead-constraint-cost-forecast_oct26.csv"
    commands:
      - {run: gridflow ingest neso_data_portal constraint_cost_fc_24m --last 24h, comment: whole file to bronze}
      - {run: gridflow transform neso_data_portal constraint_cost_fc_24m --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: forecast_month, op: in, value: ["2027-01-01", "2027-02-01", "2027-09-01", "2027-10-01"]}
      order_by: [forecast_month, published_at]
      columns: [forecast_month, published_at, constraint_cost, timestamp_utc, bronze_capture_id, capture_written_at]
    key: [forecast_month, published_at]
    caption: "Four forecast months, each as NESO's September and October 2026 uploads give it."
    fields:
      forecast_month: "NESO's `Month` label (`MMM-YY`), stored as the month's first day"
      published_at: "NESO's last-modified time for the file, read as UTC; one per upload"
      constraint_cost: "NESO's modelled cost for the month; the file gives no unit, its dictionary £m"
      timestamp_utc: "gridflow's capture time, UTC; not the forecast month"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote the capture to bronze, UTC
  caveat: Since 9 September 2026 NESO's file names no unit; only its dictionary gives £m.
  notebook:
    lead: >-
      `data.sql` reads every upload from the table's base view, because `query()` would filter
      `timestamp_utc`, the capture time. Each upload re-forecasts the months it shares with the one
      before. Values stay unitless, as in the file.
    cells:
      - |
        df = data.sql("""
            SELECT forecast_month, published_at, constraint_cost
            FROM silver_neso_data_portal_constraint_cost_fc_24m
            ORDER BY forecast_month, published_at""")
        df["published_at"] = df.published_at.dt.tz_convert("UTC")
        df.groupby("published_at").forecast_month.agg(["min", "max", "count"]).reset_index()
      - |
        wide = df.pivot(index="forecast_month", columns="published_at", values="constraint_cost")
        wide.columns = ["September upload", "October upload"]
        change = wide.assign(change=wide["October upload"] - wide["September upload"]).dropna()
        change.head(6).round(1).reset_index()
      - |
        ax = wide.plot(figsize=(8, 3.5), color=["#C77E3C", "#155A6E"], xlabel="forecast month",
                       ylabel="Constraint Cost (no unit in the file)")
        ax.legend(["September 2026 upload", "October 2026 upload"]);
    needs: the September and October 2026 uploads
    plot_alt: >-
      Line plot of NESO's Constraint Cost per forecast month, no unit in the file, in the September
      (clay) and October (petrol) 2026 uploads, October 2026 to October 2028. Both fall to a summer
      low and rise each October. The October upload is lower for February 2027 (370.7 against 469.8)
      and higher for October 2027 (491.6 against 443.7).
  related:
    - {dataset: neso_data_portal/constraint-breakdown, note: "NESO's daily outturn constraint costs, split by reason"}
    - {dataset: neso_data_portal/thermal-constraint-costs, note: "Outturn thermal constraint costs at six named boundaries"}
    - {dataset: neso_data_portal/outturn-voltage-costs, note: "Outturn voltage costs, one part of what this forecast covers"}
    - {dataset: neso_data_portal/24-months-ahead-constraint-limits, note: "NESO's weekly boundary limits over a similar two years"}
---

# 24 Months Ahead Constraint Cost Forecast

NESO's monthly forecast of **transmission constraint costs** for Great Britain over the next 24
months, published on the Open Data Portal as a single small CSV. The vendor's own definition
(CKAN package `notes`, 2026-10-06 catalogue snapshot) is: "the 24-month ahead constraint costs on a
monthly basis for the main boundaries on the transmission system. These costs are the costs of
managing constraint boundaries (for thermal, voltage or stability constraints) plus the cost of
meeting the voltage requirements. These costs do not include the cost of managing inertia or the
largest loss of infeed." So the scope is thermal, voltage and stability boundary management plus
voltage requirements, and it **excludes** inertia management and the largest loss of infeed. The
vendor does not say in these notes which mechanism the spend runs through (`TODO: verify`).

The file has one row per calendar month and one modelled cost figure for that month. The vendor
describes the figure as the modelled constraint cost for that month (datastore field metadata,
captured 2026-10-08). **Scope mismatch.** The notes say the costs are for "the main boundaries",
but the file has only a `Month` and a `Constraint Cost` column: nothing in it gives a breakdown by
boundary, so the figure appears to be an aggregate (`TODO: verify` with NESO whether it is a total
over those boundaries). Nothing in the file gives a confidence band, a scenario label or a
breakdown by technology, and no methodology note is attached to the package (`TODO: verify`
whether NESO documents the forecasting method elsewhere).

The package carries one resource. Each monthly publication **replaces** the file in place: the
2026-10-06 catalogue snapshot listed the file name `..._sept26.csv`, and an earlier probe of the
same resource id listed `..._aug26.csv`. The 2026-10-16 capture fetched `..._oct26.csv` from the
same resource id. The stable handle is the resource id, not the URL.

**This family is held in gridflow.** The silver output exists and is reconciled, but gridflow
holds it on one open question: the currency unit of the cost column (see Holds). Under ruling 66
(2026-10-24) the site page shows the rows, a chart and a notebook, with one line naming that
question; this note still gives schema, row counts, structure and clocks only.

- Publisher group: Constraint management
- Registry group: constraint-management · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| 24 Months Ahead Constraint Cost Forecast | CSV | upload | `28b85d3f-a1cc-4bb9-80af-600f2cca266a` |

- 24 Months Ahead Constraint Cost Forecast → `constraint_cost_fc_24m`.
  Download as captured: [24-months-ahead-constraint-cost-forecast_sept26.csv](https://api.neso.energy/dataset/51bb8f5a-3c95-4f7f-9a72-3b36cb7f1dc0/resource/28b85d3f-a1cc-4bb9-80af-600f2cca266a/download/24-months-ahead-constraint-cost-forecast_sept26.csv).
  The file name carries the publication month and changes with each upload. CKAN datastore
  active (24 records). CKAN `last_modified` 2026-09-10T09:38:53.501869.
  Captured: `raw_20261008T091541Z_28b85d3f-a1cc-4bb9-80af-600f2cca266a_c56921b4.csv`,
  362 bytes, 24 data rows, one header epoch, UTF-8 with a byte-order mark and CRLF line endings.
  Captured again on 2026-10-16 as
  [24-months-ahead-constraint-cost-forecast_oct26.csv](https://api.neso.energy/dataset/51bb8f5a-3c95-4f7f-9a72-3b36cb7f1dc0/resource/28b85d3f-a1cc-4bb9-80af-600f2cca266a/download/24-months-ahead-constraint-cost-forecast_oct26.csv):
  `raw_20261016T192117Z_28b85d3f-a1cc-4bb9-80af-600f2cca266a_c46bbd3e.csv`, 360 bytes, 24 data
  rows, the same header (`Month,Constraint Cost`, no unit), CKAN `last_modified`
  2026-10-09T09:30:58.440053 (bronze sidecar).

### DOC

None. The package has no documentation resources. The vendor dictionary is the NESO web page
[24 months ahead constraint cost forecast dictionary](https://www.neso.energy/data-portal/24-months-ahead-constraint-cost-forecast/24_months_ahead_constraint_cost_forecast).

## Families

### `constraint_cost_fc_24m`

- Kind: tabular · archetype: FC · refresh: monthly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Month | `forecast_month` | date | `%b-%y` | no | — | — |
| Constraint Cost | `constraint_cost` | float64 | — | yes | — | £m |

- Entity key: `forecast_month`
- Latest: `key_latest`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the CKAN `last_modified`
   of the captured file. CKAN emits it without an offset and gridflow reads it as UTC (gridflow
   `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). For the 2026-10-08 capture that
   is `2026-09-10T09:38:53.501869`, and for the 2026-10-16 capture `2026-10-09T09:30:58.440053`.
   The 24 silver rows of each capture share its one vintage (checked 2026-10-23). It says when the
   monthly file was last uploaded. It does not say when NESO's model was run
   (`TODO: verify` whether any modelling-date statement exists).
2. **Event time (temporal recipe `none`).** The record declares **no event-time recipe**.
   `timestamp_utc` and `event_time` therefore equal the **capture time**, here
   `2026-10-08T09:15:41.750414Z` for all 24 rows of the first capture and
   `2026-10-16T19:21:17.395578Z` for the second. They do **not** locate the
   forecast month. The month a row refers to is carried only by `forecast_month`, a calendar
   date (always the first of the month in silver). The vendor dictionary says the cost applies to
   that month. Converting a month to UTC interval bounds would need a stated timezone, which the
   dictionary does not give (`TODO: verify`; class 3, so it stays unconverted).

Silver columns beyond the vendor columns: `timestamp_utc`, `published_at`, `bronze_capture_id`,
`capture_written_at`, `event_time`, `available_at`, `source_run_id`, `dataset_version` (all
timestamps tz-aware UTC; `dataset_version` `1+e1` = record version 1, epoch 1).

**Month label.** `Month` is the vendor's `MMM-YY` label (the first captured label is `Oct-26`; the vendor's own example is `Dec-25`, so treat the form as `MMM-YY`, not a fixed month) and parses with
`%b-%y` on all 24 rows with no failures. The silver `forecast_month` column therefore holds a
`date`, not a timestamp. The 24 rows span `2026-10-01` to `2028-09-01`, one per month with no
gap and no duplicate. Note the lead: the capture's file name is `sept26` and its CKAN
`last_modified` is in September 2026, while the first forecast month is October 2026. The
2026-10-16 capture repeats the pattern one month on: file name `oct26`, `last_modified`
2026-10-09, rows `2026-11-01` to `2028-10-01` (24 months, no gap, no duplicate). Whether the
file-name month is the issue month is `TODO: verify`.

**Units (vendor dictionary only).** The unit comes from the vendor's datastore field metadata
for `Constraint Cost` (captured 2026-10-08): title `Constraint Cost (£m)`, unit `£m`, description
"the modelled constraint cost in £m for that month". Read literally, the vendor labels the figure
in millions of pounds. The package notes record that on 9 September 2026 the CSV column id was
renamed from `Constraint Cost (£m)` to `Constraint Cost`. That is why the captured header carries no
unit and the `£m` exists only in the datastore metadata (title and unit), never in the CSV itself. The registry hold records that the profiler's metadata read showed an
undecodable symbol before `m`, so the currency was not accepted without confirmation against the
NESO data dictionary. That reading does not reproduce: the captured field-info bytes
(`field-info/20261008T114228Z/constraint_cost_fc_24m.json`) hold a valid UTF-8 pound sign
(`C2 A3`) in the title, description and unit (checked 2026-10-23). The open question is
therefore the missing unit in the file itself, not a garbled character. That confirmation (unit E-SEM) is still open, so the unit stays a held
question. It is not inferred from the column name. `Month` carries no unit.

**Sentinels and missing values (FACTS g5).** The record declares no null token. The profiler
found 0 blank cells and 0 nulls in the capture, and `constraint_cost` is typed nullable only as a
guard. Silver holds 0 nulls in either column. No bounds are imposed and no value is converted.
Whether a missing month would be omitted or left blank is unknown (`TODO: verify`).

**Identity and selection.** The entity key is `forecast_month`: within one capture each month
appears once. `_latest` is `key_latest`, so the newest capture's row for a month supersedes older
ones. Because each monthly upload re-forecasts overlapping months, successive captures will carry
different figures for the same `forecast_month`. Point-in-time use must therefore select on
`published_at` / `available_at`, not on `forecast_month`. The two captures confirm it: they share
23 months (November 2026 to September 2028), and the figure differs on all 23 (checked on bronze,
2026-10-23). Whether NESO ever back-fills or
restates an issued file, rather than issuing a new one, is `TODO: verify`.

**Activation (2026-10-08, pilot batch E).** Transformed at cutoff 2026-10-08 (one capture,
first capture = cutoff): **24 silver rows**, equal to the planned count. No prior silver existed,
so nothing was overwritten. The reconcile reported 0 gaps (gridflow `@.planning/v0.22-RESULTS.md`
§E; RULINGS 504). The first daily refresh (2026-10-16) captured the October upload and wrote a
second parquet file under `year=2026/month=10` (24 rows), so silver holds 48 rows from two
captures (checked 2026-10-23); `_latest` takes each month from the newest. Activation receipt:
RESULTS §E; RULINGS 503/504.

## Cadence

- Registry refresh: monthly
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Monthly
- Monthly: one capture per refresh run. The vendor replaces the file in place each month, so a
  missed run loses that month's vintage unless a capture happened in between.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

## Holds

- `constraint_cost_fc_24m`: held: TODO: currency unit of Constraint Cost; vendor metadata shows an undecodable symbol before 'm'; confirm GBP million from the NESO data dictionary (unit E-SEM)

Status as of 2026-10-16: the hold stands. A grep of RULINGS.md found no ruling naming this family
or lifting its hold. The later rulings the batch brief lists (591 and 596 for the demand-forecast
pairing, 879 for the close gaps) do not touch it, and the activation receipt records the family as
"silver exists, publication held". Consequences while held:

- The site page shows the rows with a line naming the unit question (ruling 66, 2026-10-24);
  this note itself states no cost figure.
- Silver rows remain readable for engineering checks (row counts, schema, month coverage), but
  must not be used as a published or point-in-time input until E-SEM answers the unit question.
  Modelling use is not endorsed while the hold stands.
- What would lift it: confirmation from the NESO data dictionary that the unit is GBP million.
  The datastore field metadata already says `£m`, so the remaining gap looks like a decoding
  question rather than a semantic one, but that reading is not a ruling.
