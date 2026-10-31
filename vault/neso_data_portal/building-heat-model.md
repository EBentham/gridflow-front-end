---
source: "neso_data_portal"
package: "building-heat-model"
dataset_keys: ["building_heat_model_example_output_half", "building_heat_model_list_input"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Building heat model
  summary: >-
    NESO's Excel tool that models a home's heat demand, with example half-hourly profiles for a
    gas boiler and a heat pump.
  facts:
    vendor: "NESO Data Portal: two CSVs, an Excel workbook and a user guide"
    cadence: "Ad hoc, NESO says; all four files last modified 30 July 2026"
    grain: "Example output: one half hour of one model run per row"
    history: "NESO created the package on 30 July 2026"
  landscape: power
  what_it_is: >-
    NESO built the tool with the Centre for Sustainable Energy. It simulates a building's heating
    minute by minute over 24 hours, then sums to half hours. NESO's example is one average January
    day, with no date: run 1 a gas combi boiler, run 2 an air-source heat pump (air to water).
    NESO calls the profiles synthetic, not measured.
  how_used:
    - "Set a heat pump's half-hourly electricity beside a gas boiler's gas"
    - "Run the workbook for other buildings and heating systems"
    - "Synthetic heating profiles for energy system models, NESO's stated use"
  chart:
    type: bar
    silver: neso_data_portal/building_heat_model_example_output_half
    value: total_electricity
    filter:
      - {column: run_id, op: eq, value: run_2}
    dedup: {"on": [resource_id, run_id, hh_period], order_by: capture_written_at}
    group: start_of_hh_period
    aggregation: max
    sort: label
    unit: kWh
  chart_view:
    title: Heat pump electricity per half hour, example day
    caption: >-
      Silver `building_heat_model_example_output_half`, NESO's run 2 (air-source heat pump, an
      average January day with no date): `total_electricity`, kWh per half hour, one row per
      half-hour start, nothing summed. NESO calls the profiles synthetic.
    alt: >-
      Horizontal bar chart of electricity used in NESO's example heat pump run, kWh per half hour,
      one bar per half-hour start from 00:00 to 23:30. The highest is 0.818 at 00:30, then 0.746 at
      05:00. It is zero at 00:00, from 01:30 to 03:30, from 09:00 to 13:30 and at 23:00 and 23:30.
      From 14:00 it starts at 0.694 and is 0.27 to 0.28 from 21:00 to 22:30.
    key:
      - {series: total_electricity, label: Heat pump electricity, codes: run_2, paint: petrol,
         note: "NESO's run 2, an air-source heat pump; the gas boiler run is not drawn"}
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show`, then two CSVs, the macro-enabled workbook and the
      user guide, each downloaded whole unless its `last_modified` is unchanged. The workbook and
      guide stay as files.
    commands:
      - {run: gridflow pipeline neso_data_portal building_heat_model_example_output_half --last 24h, comment: "output CSV to bronze, then silver"}
      - {run: gridflow ingest neso_data_portal building_heat_model_list_input --last 24h, comment: "input list, bronze only"}
      - {run: gridflow ingest neso_data_portal building_heat_model_files --last 24h, comment: "workbook and guide, bronze only"}
  record:
    select:
      filter:
        - {column: hh_period, op: in, value: [13, 18, 19, 29]}
      dedup: {"on": [resource_id, run_id, hh_period], order_by: capture_written_at}
      order_by: [run_id, hh_period]
      columns: [run_id, start_of_hh_period, hh_period, total_heater_output, total_gas, total_electricity,
                avg_cop_space_heat, avg_cop_dhw, resource_id, published_at, timestamp_utc]
    key: [resource_id, run_id, hh_period]
    caption: "Both runs at 06:00, 08:30, 09:00 and 14:00; the blank cells differ by run."
    fields:
      run_id: "NESO's model run: `run_1` gas combi boiler, `run_2` air-source heat pump"
      start_of_hh_period: "NESO's half-hour start, `HH:MM`, on an example day with no date"
      hh_period: "Half-hour index, 1 to 48 within a run; not a settlement period"
      total_heater_output: "NESO's total heat output in the half hour, kWh"
      total_gas: "NESO's total gas used in the half hour, kWh"
      total_electricity: "NESO's total electricity used in the half hour, kWh"
      avg_cop_space_heat: "NESO's average coefficient of performance for space heat; no unit or scale stated"
      avg_cop_dhw: "NESO's average coefficient of performance for hot water; no unit or scale stated"
      resource_id: "CKAN file id; with run and half hour, the entity key"
      published_at: "NESO's last-modified time for the file, read as UTC"
      timestamp_utc: "When gridflow captured the file, UTC; the rows carry no date"
      building_archetype: "NESO's building type; one semi-detached archetype in both runs"
      month_vendor: "NESO's `month` column, renamed; `jan` in both runs"
      heater_output_space_heat: "Heat output for space heating in the half hour, kWh"
      gas_space_heat: "Gas for space heating in the half hour, kWh"
      electricity_space_heat: "Electricity for space heating in the half hour, kWh"
      heater_output_dhw: "Heat output for domestic hot water in the half hour, kWh"
      gas_dhw: "Gas for domestic hot water in the half hour, kWh"
      electricity_dhw: "Electricity for domestic hot water in the half hour, kWh"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      `query()` filters on `timestamp_utc`, the capture time here, so these cells use `data.sql()`
      on the `_latest` view. Each run is a different heating system: never add the runs together.
    cells:
      - |
        data.sql("""
            SELECT run_id, count(*) AS half_hours,
                   count(*) FILTER (WHERE total_gas IS NULL) AS gas_blank,
                   count(*) FILTER (WHERE electricity_space_heat IS NULL) AS space_heat_electricity_blank,
                   count(*) FILTER (WHERE avg_cop_space_heat IS NULL) AS cop_space_heat_blank,
                   count(*) FILTER (WHERE avg_cop_dhw IS NULL) AS cop_dhw_blank
            FROM silver_neso_data_portal_building_heat_model_example_output_half_latest
            GROUP BY run_id
            ORDER BY run_id
        """)
      - |
        hm = data.sql("""
            SELECT run_id, hh_period, start_of_hh_period, total_heater_output, total_gas, total_electricity
            FROM silver_neso_data_portal_building_heat_model_example_output_half_latest
            ORDER BY run_id, hh_period
        """)
        hm[hm.start_of_hh_period.isin(["06:00", "14:00"])]
      - |
        wide = hm.pivot(index="start_of_hh_period", columns="run_id", values=["total_gas", "total_electricity"])
        two = wide[[("total_gas", "run_1"), ("total_electricity", "run_2")]].set_axis(
            ["run 1 gas, boiler", "run 2 electricity, heat pump"], axis=1)
        ax = two.plot(figsize=(9, 3.5), color=["#B5651D", "#155A6E"],
                      xlabel="NESO's half-hour start, example day", ylabel="kWh per half hour");
    needs: NESO's example output file for the building heat model
    plot_alt: >-
      Line plot over NESO's example January day, kWh per half hour: run 1's gas (boiler) and run 2's
      electricity (heat pump). Gas peaks at 9.06 at 06:00 and 6.69 at 16:30, spikes through the
      evening and stays below 0.31 from 09:00 to 15:30. Electricity is never above 0.82, its
      highest at 00:30.
  related:
    - {dataset: neso_data_portal/local-authority-level-spatial-heat-model-outputs-fes, note: "NESO's FES heat model outputs for each local authority"}
    - {dataset: neso_data_portal/fes-natural-gas-residential-and-non-domestic-i-c-heat-demand-summary-data-table-ed3, note: "FES natural gas heat demand for homes and businesses"}
    - {dataset: neso_data_portal/fes-electricity-demand-summary-data-table-ed1, note: "NESO's FES GB electricity demand table, by component"}
    - {dataset: neso_data_portal/future-energy-scenario-fes-building-block-data, note: "FES split to Grid Supply Points in common building blocks"}
  family:
    slug: building-heat-model
    members:
      - dataset: building_heat_model_example_output_half
        differs: "Per half hour: heat, gas, electricity and coefficient of performance (COP), two runs"
        request:
          - "GET https://api.neso.energy/api/3/action/package_show?id=building-heat-model"
          - "GET https://api.neso.energy/dataset/14d99094-165e-4de1-9452-137c2835b102/resource/27522340-008d-4c82-97c1-17eeb7ed1b6a/download/example_profiles-output_data.csv"
        caveat: "NESO states no unit or scale for the two COP columns, or what blanks mean."
      - dataset: building_heat_model_list_input
        differs: "The inputs behind both runs: one parameter per row, one column per run"
        request: "GET https://api.neso.energy/dataset/14d99094-165e-4de1-9452-137c2835b102/resource/b809e59a-e681-4ecb-af07-80997abbbd6f/download/example_profiles-list_of_input_parameters.csv"
        held: "One row appears twice and no column tells them apart, so there is no silver table."
---

# Building Heat Model

NESO's Building Heat Model is a spreadsheet tool that turns a chosen building archetype, heating
system and month into half-hourly heat demand and the gas or electricity needed to supply it. The
package publishes the tool itself (an Excel workbook and a user guide) and, as a worked example,
the inputs and outputs of two model runs. The two CSV resource descriptions call the example an average
January day (the package notes say the profiles are synthetic), with one run for a gas combi boiler and one for an air-to-water heat pump. The
modelling question it serves is how much electricity a heat-pump home draws against the gas a
boiler home draws, half hour by half hour, over a typical winter day. That is the load-shape
question behind electrified-heat scenarios in GB energy-system models. It sits beside the Future
Energy Scenarios heat tables
(@local-authority-level-spatial-heat-model-outputs-fes.md).

**This is an example, not a time series.** The package holds two example runs of a model. It does
not hold observed or forecast demand for any date. The half-hourly rows carry a period number
(1 to 48) and a clock label (`00:00` to `23:30`) and no date, no year and no time zone. Do not
treat them as GB settlement periods, as an observed series or as a scenario projection.

**The silver output of `building_heat_model_example_output_half` is held (unit E-SEM).** It exists
on disk, and this note gives its schema, row counts and structure. The site page shows its rows,
a chart of run 2's electricity and a notebook, with one line naming the hold question (ruling 66,
2026-10-24). The unit of the two
average coefficient-of-performance (COP) columns is not declared, and the meaning of a blank gas,
electricity or COP cell is not established (see Holds). The package-level `eligibility: eligible`
in the front matter is the package registry entry. The hold is per family.

**The input list has no silver output.** `building_heat_model_list_input` is ingest-only: its
bronze capture exists and nothing is transformed from it, because the vendor file repeats an
identical row and no key can tell the two copies apart (RULINGS 538 precedent, ruling 838).

Reading rules for anyone who does open the example-profile silver:

- **Each `run_id` is one model run.** The file holds two runs of 48 half-hour periods each. Never
  sum across `run_id`: the two runs are two different heating systems modelled for the same kind
  of day, not two parts of one demand.
- **Energy columns are per half hour.** The vendor dictionary gives the energy columns in kWh. A
  value is the energy in one half-hour period. A daily total is a sum within one run, never across
  runs.
- **Never sum gas and electricity.** They are different fuels and, in a heat-pump run, not
  interchangeable. The `total_*` columns are vendor columns and are not recomputed by gridflow.
- **A null is a blank vendor cell.** Its meaning is undocumented. A blank is not zero. A `0` is a
  value.
- **`hh_period` and `start_of_hh_period` carry the example day's clock only.** The clock is stored
  as the vendor string `HH:MM`. It is not cast to a timestamp.

- Publisher group: FES: Pathways to Net Zero
- Registry group: future-energy-scenarios · archetype: SCN
- Package page: [NESO Data Portal, Building Heat Model](https://www.neso.energy/data-portal/building-heat-model)
  (CKAN package id `14d99094-165e-4de1-9452-137c2835b102`; four resources, all `url_type: upload`)

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Example output half-hourly demand profiles | CSV | upload | `27522340-008d-4c82-97c1-17eeb7ed1b6a` |
| List of input parameters used for generating the example profiles | CSV | upload | `b809e59a-e681-4ecb-af07-80997abbbd6f` |

Both are `SILVER` in the registry. Only the first is transformed: the second is ingest-only (see
`building_heat_model_list_input` below).

### DOC

| Resource | Format | Capture | Id |
|---|---|---|---|
| Building Heat Model Excel tool | XLSM | upload | `78516fb0-9fd1-40cc-9db0-39cca2d78ac9` |
| Model User Guide | PPT | upload | `ff46632d-4e8e-4b19-80f4-2838399dfc92` |

The two DOC files are the model and its guide. They are captured to bronze as bytes (family
`building_heat_model_files`, catalogue only) and never parsed into silver.

### Resource download links

URLs are the `request_url` in each capture's bronze sidecar (capture date 2026-10-08). The stable
handle for a resource is its id, not the file name. All four are `url_type: upload`.

| Resource | Disposition | Download | Bytes | CKAN `last_modified` (offset-less, read as UTC) |
|---|---|---|---:|---|
| Example output half-hourly demand profiles (CSV) | SILVER → `building_heat_model_example_output_half` | [example_profiles-output_data.csv](https://api.neso.energy/dataset/14d99094-165e-4de1-9452-137c2835b102/resource/27522340-008d-4c82-97c1-17eeb7ed1b6a/download/example_profiles-output_data.csv) | 10,034 | `2026-07-30T15:36:52.510328` |
| List of input parameters (CSV) | SILVER, ingest-only → `building_heat_model_list_input` | [example_profiles-list_of_input_parameters.csv](https://api.neso.energy/dataset/14d99094-165e-4de1-9452-137c2835b102/resource/b809e59a-e681-4ecb-af07-80997abbbd6f/download/example_profiles-list_of_input_parameters.csv) | 9,219 | `2026-07-30T14:01:53.418825` |
| Building Heat Model Excel tool (XLSM) | DOC → `building_heat_model_files` | [building-heat-model-v1.xlsm](https://api.neso.energy/dataset/14d99094-165e-4de1-9452-137c2835b102/resource/78516fb0-9fd1-40cc-9db0-39cca2d78ac9/download/building-heat-model-v1.xlsm) | 9,850,366 | `2026-07-30T14:04:04.766197` |
| Model User Guide (PPT) | DOC → `building_heat_model_files` | [building-heat-model-user-guide-v1.pptx](https://api.neso.energy/dataset/14d99094-165e-4de1-9452-137c2835b102/resource/ff46632d-4e8e-4b19-80f4-2838399dfc92/download/building-heat-model-user-guide-v1.pptx) | 8,205,691 | `2026-07-30T13:29:07.038005` |

Both CSVs begin with a UTF-8 byte-order mark, which the gridflow reader handles. Both decode as
strict UTF-8 with no preamble, no ragged row and no wholly blank row. The `v1` in the DOC file
names is a file-name observation. gridflow infers no edition or model version from it, from the
example month or from the modification dates.

## Families

### `building_heat_model_example_output_half`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| run_id | `run_id` | string | — | no | — | — |
| building_archetype | `building_archetype` | string | — | no | — | — |
| month | `month_vendor` | string | — | no | — | — |
| hh_period | `hh_period` | int64 | — | no | — | — |
| start_of_hh_period | `start_of_hh_period` | string | — | no | — | HH:MM |
| heater_output_space_heat | `heater_output_space_heat` | float64 | — | no | — | kWh |
| gas_space_heat | `gas_space_heat` | float64 | — | yes | — | kWh |
| avg_COP_space_heat | `avg_cop_space_heat` | float64 | — | yes | — | — |
| electricity_space_heat | `electricity_space_heat` | float64 | — | yes | — | kWh |
| heater_output_dhw | `heater_output_dhw` | float64 | — | no | — | kWh |
| gas_dhw | `gas_dhw` | float64 | — | yes | — | kWh |
| avg_COP_dhw | `avg_cop_dhw` | float64 | — | yes | — | — |
| electricity_dhw | `electricity_dhw` | float64 | — | no | — | kWh |
| total_heater_output | `total_heater_output` | float64 | — | no | — | kWh |
| total_gas | `total_gas` | float64 | — | yes | — | kWh |
| total_electricity | `total_electricity` | float64 | — | no | — | kWh |

- Entity key: `resource_id`, `run_id`, `hh_period`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured resource, read as UTC per ADR-030 (gridflow
   `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). There is one resource and one
   vintage, `2026-07-30T15:36:52.510328`, shared by every row. Checked on every silver row on
   2026-10-15: `available_at` equals `published_at`. The vintage says when the file last changed
   on the portal. It does not say when the model runs were produced or first published, and no
   date inside the file says either. The point-in-time rule is `WHERE available_at <= :as_of`.
2. **Event time (temporal recipe `none`).** The record declares no event-time recipe, because the
   rows describe an example day with no date. `timestamp_utc` is therefore the **capture time**,
   not a modelled time: `2026-10-08T09:14:01.292897Z`, the same on all 96 rows. `event_time` and
   `capture_written_at` carry the same instant. Do not use `timestamp_utc` as a demand time axis
   and do not derive a date from it. The only intra-day information is the vendor's own
   `hh_period` and `start_of_hh_period`.

**Shape.** One resource, 96 data rows, 16 vendor columns, one header epoch. The rows are two runs
(`run_1` and `run_2`) of exactly 48 rows each. `hh_period` runs 1 to 48 within each run and each
period's clock string is its half-hour start, `00:00` to `23:30`. Both runs name one building
archetype (the vendor label is `semi detached – medium ` and ends in a trailing space, stored as
received) and one month, `jan`. There is no unpivot and no edition. The vendor column `month` is
a reserved name in the gridflow engine and is stored as `month_vendor`. `hh_period` is a
half-hour index of an example day. The file shows no date, so there is no 46- or 50-period
daylight-saving case here, and the 1..50 settlement-period range does not apply.

**Units (vendor dictionary, as cited in FACTS).** The dictionary gives the ten energy columns
(`heater_output_*`, `gas_*`, `electricity_*` and the three `total_*`) in **kWh**, per half-hour
period. `hh_period` is an integer index and `start_of_hh_period` a clock label, so neither takes
an energy unit. The two COP columns (`avg_COP_space_heat`, `avg_COP_dhw`) are described as
average coefficients of performance and the vendor declares **no unit or scale** for them. No unit
is inferred from the column name, and gridflow does not label them (`TODO: verify` with NESO,
part of the hold). The dictionary does not say how the `total_*` columns relate to the space-heat
and hot-water columns beside them. `TODO: verify` before recomputing or reconciling any total.

**Sentinels and missing values (FACTS g5).** The record declares no null token.

- **Blank cells** are kept as **null**. They are not dropped and not filled. The vendor does not
  say what a blank means (not applicable to that heating system, not modelled, or unavailable).
  `TODO: verify` (part of the hold). The position of a blank does not settle it.
- Null counts by silver column over the 96 rows: `gas_space_heat` 48, `electricity_space_heat`
  48, `gas_dhw` 48, `total_gas` 48, `avg_cop_space_heat` 70, `avg_cop_dhw` 92. The other ten
  vendor columns have none.
- The whole-cell tokens `-`, `N/A`, `NA` and `n/a` occur **zero times** in every column. There
  are no text sentinels.
- **Zeros are values.** Numeric zeros occur in many columns, among them the energy columns. No
  primary source identifies a zero as a sentinel. Do not treat zero as missing, and do not treat
  a blank as zero.
- Every non-blank cell casts strictly to float64 (and `hh_period` to int64), with zero failures.

**Identity and selection.** The entity key is `resource_id`, `run_id` and `hh_period`. This is a
**measured guard key**: the body passed it with zero duplicated rows. No vendor text declares it
as the identity of a row. `TODO: verify` the vendor's own uniqueness rule. The guide says the run
ID links the output rows to the parameter list, and the dictionary defines the half-hour period.
`_latest` is `whole_capture` per `resource_id`: a newer capture of the resource replaces its
previous capture as a whole. No revision rule between captures is claimed, and no second capture
has happened.

**Activation (2026-10-15, master `06378b9`, PR #125).** Transformed with window 2026-10-08, one
capture and no prior silver: **96 rows**, equal to the planned count and with 0 failures. The
whole SCN-3 batch transformed 59,388 rows. Reconcile `--all --cutoff 2026-10-13` exited 0 over 255
families with 0 gaps, and coverage was clean (gridflow `@.planning/v0.22-RESULTS.md` §SCN-3;
RULINGS 838, 839, 842 and 844).

Silver columns beyond the vendor columns: `resource_id`, `timestamp_utc`, `published_at`,
`bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id` and
`dataset_version` (all timestamps tz-aware UTC; `dataset_version` is `1+e1`: the registry record
version (1) plus the silver engine version (`e1`)). There is no `edition` column, because the
package has no evidenced edition.

The silver file sits under
`C:\gridflow-data\silver\neso_data_portal\building_heat_model_example_output_half\`, in
`year=2026\month=10\`, one Parquet file per capture.

### `building_heat_model_files`

- Kind: files · archetype: SCN · refresh: adhoc · empty allowed: no
- files: catalogue only

The two DOC resources, the Excel workbook and the user guide, captured as raw bytes (2026-10-08)
with no silver output. Clocks: the vintage is each file's CKAN `last_modified` (dates in the file
table above), and there is no event time because nothing is parsed. They are the model that
produced the two CSVs.

- **Workbook** (`building-heat-model-v1.xlsm`): a macro-enabled Excel model. gridflow has not
  opened it for this page, so it makes no claim about its sheets, macros or saved state beyond
  earlier gridflow research that matched the sheet `parameter list for portfolio` to the input
  list and `hh agg (outputs)` to the half-hourly output (gridflow
  `@.planning/phases/v0.22-K-SCN-3/K-SCN-3-FACTS.md` §2.3). Macro-enabled files are bronze bytes
  only; do not open them from a pipeline.
- **User guide** (`building-heat-model-user-guide-v1.pptx`): a slide deck. Slides 19 to 22 explain
  that the export copies the output table and the parameters into portfolio sheets and adds a run
  ID, which is the vendor's link between the two CSVs.
- The guide establishes that the CSVs expose the tool's parameter and output content. It does not
  establish that they equal the saved workbook state cell for cell. `TODO: verify` by comparing
  the CSVs with the workbook. That comparison has not been done.

### `building_heat_model_list_input`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no
- ingest-only: no silver yet

The inputs behind the two example runs: 269 data rows under the header `parameter,run_1,run_2`.
Each row is a model parameter with its value in the first run and its value in the second. The
two value columns carry the same strings as `run_id` in the output file (`run_1`, `run_2`). The
guide says a run ID links output rows to the parameter list. `TODO: verify` that the output's
`run_1` is the input's `run_1` column.

- **Clocks.** Vintage: `ckan_last_modified` `2026-07-30T14:01:53.418825` (the capture's
  `available_at` would be this value, and no silver row exists to carry it). Event time: none. The
  file is reference material with no date or projection-year axis.
- **Content is mixed text.** Section headings, numbers, booleans, system names and spreadsheet
  error strings share one column. The vendor dictionary describes both run columns as text.
  No unit is declared for the columns. `TODO: verify` any unit of an individual parameter with
  NESO. Do not read the columns as numbers.
- **Blanks and sentinels.** Blank cells: 79 in each of `run_1` and `run_2`. The literal `#N/A`
  appears in 6 `run_1` cells and 4 `run_2` cells. Its parameter-specific meaning is not
  established. It is not mapped to null and the column stays text. The tokens `-`, `N/A`, `NA` and
  `n/a` occur zero times.
- **Why there is no silver.** The key `parameter` repeats (two labels each occur twice), and one
  repeat is an entire identical row: a section heading with blank values in both runs. No
  combination of vendor columns, resource id or capture date distinguishes the two copies. The
  duplicate guard rejects the body with two participating rows. Silently dropping one copy, or
  numbering rows, would be a new mechanism and not vendor evidence. gridflow follows the
  precedent for repeated identical vendor rows (RULINGS 538, applied in ruling 838): no record,
  no silent dedup, the resource stays `SILVER` ingest-only and bronze keeps the faithful bytes.
  Making it `DOC` instead would hide a tabular body, so it was not chosen (RULINGS 839).
  The lift condition is a corrected NESO upload or a vendor-issued row identity (`TODO: verify`
  with NESO).
- The bronze file is at
  `C:\gridflow-data\bronze\neso_data_portal\building_heat_model_list_input\2026\10\08\`.
  Bronze is immutable. Read it as raw text.

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc
- All four resources were last modified on 2026-07-30 (times above). `TODO: verify` whether NESO
  plans a new model version or a refreshed example. The `v1` in the DOC file names is the only
  hint, and it is a file-name observation, not a vendor statement.
- Captures to date: one per resource (2026-10-08). No scheduled refresh has run yet, so no
  revision behaviour has been observed.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `building_heat_model_example_output_half`: held: TODO: What unit or scale does NESO declare for `avg_COP_space_heat` and `avg_COP_dhw`? What does a blank gas, electricity or COP cell mean in the example profiles (blank is not zero)? (unit E-SEM)

The family is held by the SCN-3 batch record (ruling 839, seat ruling 7; activation in rulings 842
and 844). Its silver output stays on disk. No gold view or model feed is planned for it while the
hold stands. The site page shows its rows with one line naming the question below (ruling 66,
2026-10-24). Row counts and schema are given above. Unit E-SEM must answer
two things before the hold can lift:

1. **The unit or scale of the COP columns.** The dictionary calls them average coefficients of
   performance and declares nothing else. A COP is a ratio of heat delivered to energy consumed,
   but whether these columns are that ratio, a percentage or something else is the vendor's to say.
2. **What a blank cell means.** Gas, electricity and COP cells are blank in parts of the file. The
   vendor does not say whether a blank is not applicable (for example gas in a heat-pump run),
   not modelled or unavailable. A blank is not zero.

What the vendor text does establish (FACTS §2.2):

- The ten energy columns are in kWh per half-hour period (vendor dictionary).
- `hh_period` is the half-hour period index and `start_of_hh_period` its start time, both for an
  example day. The resource description names the two systems and the average-January-day profile.
- The run ID links the output rows to the input parameter list (guide).

Until the hold lifts:

- Show its values only as NESO wrote them, with the question named; never derive a COP unit.
- Do not use it point-in-time beyond its vintage, `available_at` (the CKAN `last_modified`), a
  conservative proxy and nothing finer.
- Do not sum across `run_id`, across gas and electricity or across any of the periods and treat
  the result as GB demand.

`building_heat_model_list_input` is not held. It has no record (ruling 838) and no silver. The
other families in the package are not held. Related holds in the same batch (gridflow
`@docs/neso_data_portal/eligibility.md`): the whole-system gas tables
(@fes-whole-system-gas-supply-data-table-ws1.md,
@fes-whole-system-gas-supply-emissions-data-table-ws2.md) and the local-authority heat outputs
(@local-authority-level-spatial-heat-model-outputs-fes.md) are held on year-period, unit or blank
questions. The Resource Adequacy tables (@resource-adequacy-in-2030s.md) are eligible.

## Evidence

- Registry record: `@src/gridflow/connectors/neso_data_portal/registry/building-heat-model.json`
  (gridflow repo). Eligibility report: `@docs/neso_data_portal/eligibility.md`.
- Batch research and spec: `@.planning/phases/v0.22-K-SCN-3/K-SCN-3-FACTS.md` (§2 and the g5
  register; evidence tags C1 to C11) and `@.planning/phases/v0.22-K-SCN-3/K-SCN-3-SPEC.md`
  (docs-wave bullet).
- Activation receipt: `@.planning/v0.22-RESULTS.md` §SCN-3. Rulings 538 (repeated identical rows,
  no record), 838 (research done, input list no record), 839 (spec ratified, B2 held E-SEM), 842
  (merge) and 844 (activation): `@.planning/RULINGS.md`.
- Checked on 2026-10-15 against the silver Parquet and the bronze sidecars: row count (96), the
  25 silver columns (16 vendor plus 9 gridflow), two runs of 48, one distinct `timestamp_utc`,
  `available_at` equal to `published_at`, null counts per column, key uniqueness, and the
  `ckan_last_modified`, byte size and download URL of each of the four resources.
- Not checked: the workbook (unopened), any comparison of the CSVs with the workbook, and any
  vendor statement on the COP unit or on blank cells (none found in the captured dictionary or
  the inspected guide slides).
- Vendor reference: [Building Heat Model package](https://www.neso.energy/data-portal/building-heat-model),
  [input resource](https://www.neso.energy/data-portal/building-heat-model/list_of_input_parameters_used_for_generating_the_example_profiles),
  [output resource](https://www.neso.energy/data-portal/building-heat-model/example_output_half-hourly_demand_profiles).
- Portal overview: @../README.md.
