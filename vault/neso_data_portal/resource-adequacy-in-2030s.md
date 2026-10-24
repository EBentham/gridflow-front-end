---
source: "neso_data_portal"
package: "resource-adequacy-in-2030s"
dataset_keys: ["resource_adequacy_2030s_peak_demand", "resource_adequacy_2030s_portfolio", "resource_adequacy_2030s_results"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-15
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Resource adequacy in the 2030s
  summary: >-
    NESO's modelled loss of load and unserved energy for 2030/31, 2035/36 and 2040/41, per
    portfolio, sensitivity and historical weather year.
  facts:
    vendor: "NESO Data Portal, package `resource-adequacy-in-2030s`: three CSV files"
    cadence: "Once in 2 years, NESO says; files last modified 11 and 12 December 2025"
    grain: "One results row per case, spotlight year and historical weather year"
    history: "NESO created the package on 11 December 2025"
  landscape: power
  what_it_is: >-
    NESO's Resource Adequacy in the 2030s study models spotlight years 2030/31, 2035/36 and
    2040/41 (1 April to 31 March), under historical weather years 1984/85 to 2017/18. Files
    give peak demands, portfolio capacities, and weather-conditional Loss of Load Expectation (LOLE)
    and Expected Energy Unserved (EEU) for six portfolios and twelve sensitivities; sensitivity
    capacities deviate from Portfolio 1 (NESO). Modelled, not history.
  how_used:
    - "Compare weather-conditional LOLE and EEU across portfolios and sensitivities within one spotlight year"
    - "Find the historical weather years that carry each case's loss of load"
    - "Reuse NESO's portfolio capacities and peak demands as inputs to an adequacy model"
  chart:
    type: bar
    silver: neso_data_portal/resource_adequacy_2030s_results
    value: weather_conditional_lole_h_year
    filter:
      - {column: simulation_name, op: eq, value: "Portfolio 1"}
      - {column: spotlight_year, op: eq, value: "2035/36"}
    dedup: {"on": [resource_id, simulation_name, spotlight_year, historical_weather_year], order_by: capture_written_at}
    group: historical_weather_year
    aggregation: max
    sort: label
    unit: hours/year
  chart_view:
    title: Portfolio 1 modelled loss of load by weather year, 2035/36
    caption: >-
      Silver `resource_adequacy_2030s_results`, case `Portfolio 1`, spotlight year 2035/36 (1 April
      2035 to 31 March 2036): NESO's modelled weather-conditional LOLE in hours/year, one row per
      historical weather year, nothing summed. NESO's file last modified 12 December 2025.
    alt: >-
      Horizontal bar chart of NESO's modelled weather-conditional LOLE for Portfolio 1 in spotlight
      year 2035/36, in hours/year, one bar per historical weather year from 1984/85 to 2017/18.
      Three of the 34 bars are above zero: 1985/86 at 6.23, 1984/85 at 1.52 and 2000/01 at 0.1.
      The other 31 weather years are zero.
    key:
      - {series: weather_conditional_lole_h_year, label: Weather-conditional LOLE, codes: Portfolio 1, paint: petrol,
         note: "NESO: \"the average number of hours demand exceeds supply across all simulations\""}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then each table's file downloaded whole, unless
      its `last_modified` is unchanged. Dates select nothing; silver keeps every capture.
    commands:
      - {run: gridflow pipeline neso_data_portal resource_adequacy_2030s_results --last 24h, comment: "results file; window must end recently"}
      - {run: gridflow pipeline neso_data_portal resource_adequacy_2030s_peak_demand --last 24h, comment: "the peak demand file, both steps"}
      - {run: gridflow pipeline neso_data_portal resource_adequacy_2030s_portfolio --last 24h, comment: "the portfolio file, both steps"}
  record:
    select:
      filter:
        - {column: simulation_name, op: in, value: ["Portfolio 1", "Portfolio 2", "Portfolio 3", "Portfolio 4"]}
        - {column: spotlight_year, op: eq, value: "2035/36"}
        - {column: historical_weather_year, op: in, value: ["1984/85", "1985/86"]}
      dedup: {"on": [resource_id, simulation_name, spotlight_year, historical_weather_year], order_by: capture_written_at}
      order_by: [historical_weather_year, simulation_name]
      columns: [simulation_name, spotlight_year, historical_weather_year, weather_conditional_lole_h_year,
                weather_conditional_eeu_mwh_year, resource_id, published_at, timestamp_utc]
    key: [simulation_name, spotlight_year, historical_weather_year, resource_id]
    caption: "Portfolios 1 to 4 in spotlight year 2035/36, under weather years 1984/85 and 1985/86."
    fields:
      simulation_name: "Case label: `Portfolio 1` to `6`, or `Sensitivity 01` to `12` with a description"
      spotlight_year: "Modelled year, 1 April to 31 March per NESO: `2035/36` starts 1 April 2035"
      historical_weather_year: "Past weather NESO used to generate supply and demand; a label only"
      weather_conditional_lole_h_year: "Hours/year demand exceeds supply, averaged across simulations covering 100 randomly selected forced-outage patterns"
      weather_conditional_eeu_mwh_year: 'MWh/year; NESO: "average volume of demand exceeds supply across all simulations"; same 100 patterns'
      resource_id: "CKAN file id; with case, spotlight and weather year, the entity key"
      published_at: "NESO's last-modified time for the file, read as UTC"
      timestamp_utc: "When gridflow captured the file, UTC; the table has no event time"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      `query()` filters on `timestamp_utc`, which here is the capture time, so these cells use
      `data.sql()` on the `_latest` views, naming the vendor columns to leave lineage out.
    cells:
      - |
        res = data.sql("""
            SELECT simulation_name, spotlight_year, historical_weather_year,
                   weather_conditional_lole_h_year AS lole_h,
                   weather_conditional_eeu_mwh_year AS eeu_mwh
            FROM silver_neso_data_portal_resource_adequacy_2030s_results_latest
            WHERE simulation_name LIKE 'Portfolio %'
        """)
        res.assign(weather_years_with_loss=res.lole_h > 0).pivot_table(
            index="simulation_name", columns="spotlight_year",
            values="weather_years_with_loss", aggfunc="sum")
      - |
        p1 = res[res.simulation_name == "Portfolio 1"].pivot(
            index="historical_weather_year", columns="spotlight_year", values="lole_h")
        ax = p1.plot.bar(figsize=(9, 3.5), width=0.8, color=["#155A6E", "#8A9A2B", "#B5651D"],
                         xlabel="historical weather year", ylabel="Portfolio 1 LOLE, hours/year");
      - |
        peak = data.sql("""
            SELECT spotlight_year, historical_weather_year, peak_demand_mw
            FROM silver_neso_data_portal_resource_adequacy_2030s_peak_demand_latest
        """)
        p1_2035 = res[(res.simulation_name == "Portfolio 1") & (res.spotlight_year == "2035/36")]
        p1_2035.merge(peak, on=["spotlight_year", "historical_weather_year"]).nlargest(
            6, "peak_demand_mw")[["historical_weather_year", "peak_demand_mw", "lole_h", "eeu_mwh"]]
      - |
        cap = data.sql("""
            SELECT name, technology, installed_capacity_mw
            FROM silver_neso_data_portal_resource_adequacy_2030s_portfolio_latest
            WHERE future_year = '2035/36' AND name LIKE 'Portfolio %'
        """)
        cap.pivot(index="technology", columns="name", values="installed_capacity_mw")
    needs: NESO's three Resource Adequacy in the 2030s files
    plot_alt: >-
      Grouped bar chart of NESO's modelled weather-conditional LOLE for Portfolio 1, hours/year, by
      historical weather year 1984/85 to 2017/18, one bar each for 2030/31, 2035/36 and 2040/41.
      Only 1984/85 (3.97, 1.52, 0.36) and 1985/86 (4.98, 6.23, 5.63) reach above 0.1; the rest
      are zero or at most 0.1.
  related:
    - {dataset: neso_data_portal/capacity-market-register, note: "Capacity awarded per delivery year; these portfolios give installed MW"}
    - {dataset: neso_data_portal/future-energy-scenario-electricity-supply-data-table-es1, note: "FES electricity supply by scenario or pathway, a separate NESO study"}
    - {dataset: neso_data_portal/interconnector-register, note: "Contracted interconnectors; Sensitivities 08 to 10 here vary interconnection and imports"}
    - {dataset: neso_data_portal/historic-demand-data, note: "Half-hourly outturn demand; NESO does not state the modelled peaks' demand basis"}
  family:
    slug: resource-adequacy-in-2030s
    members:
      - dataset: resource_adequacy_2030s_results
        differs: "Study output: weather-conditional LOLE and EEU per case, spotlight and weather year"
        request:
          - "GET https://api.neso.energy/api/3/action/package_show?id=resource-adequacy-in-2030s"
          - "GET https://api.neso.energy/dataset/531e616c-7192-443f-bee0-ed067d55b182/resource/71221dca-c792-4fb6-b6b4-893f392d893a/download/resource-adequacy-in-the-2030s-results-dataset-.csv"
      - dataset: resource_adequacy_2030s_peak_demand
        differs: "Input: MW peak demand per spotlight and weather year, for NESO's 2025 study"
        request: "GET https://api.neso.energy/dataset/531e616c-7192-443f-bee0-ed067d55b182/resource/5ca210f2-96cb-4fcd-939d-a9f34b2b8174/download/peak-demand-dataset.csv"
      - dataset: resource_adequacy_2030s_portfolio
        differs: "Input: MW and MWh per portfolio, technology and year; sensitivity capacities excluded"
        request: "GET https://api.neso.energy/dataset/531e616c-7192-443f-bee0-ed067d55b182/resource/c2bba528-b75a-42c5-bb98-3af3a5b3f720/download/portfolio-capacity-dataset.csv"
---

# Resource Adequacy in the 2030s

The input and output tables of NESO's **Resource Adequacy in the 2030s** study (the report is
dated July 2025; the package notes say it "contains all the input and output data" for the
study). Resource adequacy asks whether Great Britain's supply fleet, imports and flexible demand
can meet demand in a given future year across many simulated weather and plant-outage
outcomes. The package answers that with three CSVs: the **peak demand** that each historical
weather year implies for each spotlight year, the **installed capacity** of each technology in each
modelled generation portfolio, and the **results** (Loss of Load Expectation, LOLE, and Expected
Energy Unserved, EEU) for each portfolio and each of the study's sensitivity cases. Use it as a
scenario reference for security-of-supply questions about 2030/31, 2035/36 and 2040/41. It is a
**study output published once**, not a time series: no row is an observation at a clock time.
The pages in this batch are reference tables, not feeds.

The three tables are already long (one row per label combination). Nothing is unpivoted, and no
year is parsed into a date. Year labels are kept as the vendor's strings (`2030/31`,
`1999/2000`). **Study years are April-March intervals.** The vendor field dictionary for all three
tables says: "As the years in the study run from April to March a spotlight year 2035 refers to the
spotlight time frame 1 April 2035 to 31 March 2036." So a spotlight label such as `2035/36` is
the interval 1 April 2035 to 31 March 2036 (gridflow
`@.planning/research/neso-snapshots/field-info/20261008T114228Z/`, files
`resource_adequacy_2030s_{peak_demand,portfolio,results}.json`). The dictionary states this for
spotlight years only: `TODO: verify` whether `Historical weather year` labels (`1984/85` to
`2017/18`) follow the same April-March convention. The vendor page lives at
[resource-adequacy-2030s](https://www.neso.energy/data-portal/resource-adequacy-2030s); the
registry package name is `resource-adequacy-in-2030s`. The package notes also embed a Power BI
report, which gridflow does not capture.

- Publisher group: FES: Pathways to Net Zero
- Registry group: future-energy-scenarios · archetype: SCN

**Reading rules for this package** (they follow from the evidence below, not from convenience):

- **Never sum or average across `name` / `simulation_name`, across spotlight years, or across
  historical weather years** without a stated method. Each portfolio and each sensitivity is a
  separate simulated case. The results are **weather-conditional**: each row is one
  spotlight-year and weather-year pairing. They are not values already averaged over all weather
  years. `TODO: verify` how NESO weights weather years when it reports a headline LOLE or EEU
  for a portfolio. The tables do not say.
- **Do not total capacity across `technology` or `category`.** The portfolio table carries a
  broad `category` (13 labels) and a finer `technology` (15 labels) for the same capacity.
  `TODO: verify` that no technology row overlaps another (for example storage rows against
  `Batteries`) before any total is built.
- `edition` exists on two of the three tables and not on the third (see Holds and Known issues).

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Peak Demand | CSV | upload | `5ca210f2-96cb-4fcd-939d-a9f34b2b8174` |
| Portfolio Capacities | CSV | upload | `c2bba528-b75a-42c5-bb98-3af3a5b3f720` |
| Resource Adequacy Results | CSV | upload | `71221dca-c792-4fb6-b6b4-893f392d893a` |

The package has three resources, all CSV, all `upload` type, all CKAN datastore active. There
are no DOC resources. The resource id is the stable handle. The download URL embeds the package
id (`531e616c-7192-443f-bee0-ed067d55b182`) and the file name.

- Peak Demand → `resource_adequacy_2030s_peak_demand`.
  Download: [peak-demand-dataset.csv](https://api.neso.energy/dataset/531e616c-7192-443f-bee0-ed067d55b182/resource/5ca210f2-96cb-4fcd-939d-a9f34b2b8174/download/peak-demand-dataset.csv).
  CKAN `last_modified` `2025-12-12T12:36:08.151108`. Vendor description: peak demand for spotlight
  years for each historic weather year within the 2025 resource adequacy study.
  Captured: 2,409 bytes, 102 data rows, one header epoch
  (`raw_20261008T111705Z_5ca210f2-96cb-4fcd-939d-a9f34b2b8174_3e5a1793.csv`).
- Portfolio Capacities → `resource_adequacy_2030s_portfolio`.
  Download: [portfolio-capacity-dataset.csv](https://api.neso.energy/dataset/531e616c-7192-443f-bee0-ed067d55b182/resource/c2bba528-b75a-42c5-bb98-3af3a5b3f720/download/portfolio-capacity-dataset.csv).
  CKAN `last_modified` `2025-12-11T13:47:53.306382`. Vendor description: the installed capacities
  of each technology within the portfolios used for the resource adequacy study published in
  2025. Capacities used for uncertainty and sensitivity analysis are deviations from Portfolio 1
  and are **not** included in this file.
  Captured: 18,166 bytes, 315 data rows, one header epoch
  (`raw_20261008T111708Z_c2bba528-b75a-42c5-bb98-3af3a5b3f720_d2ffb943.csv`).
- Resource Adequacy Results → `resource_adequacy_2030s_results`.
  Download: [resource-adequacy-in-the-2030s-results-dataset-.csv](https://api.neso.energy/dataset/531e616c-7192-443f-bee0-ed067d55b182/resource/71221dca-c792-4fb6-b6b4-893f392d893a/download/resource-adequacy-in-the-2030s-results-dataset-.csv)
  (the trailing hyphen is part of the vendor's file name).
  CKAN `last_modified` `2025-12-12T12:34:52.812310`. Vendor description: the LOLE and EEU
  results from each portfolio, alternative scenarios and sensitivity study, broken down by
  spotlight years.
  Captured: 112,157 bytes, 1,462 data rows, one header epoch
  (`raw_20261008T111713Z_71221dca-c792-4fb6-b6b4-893f392d893a_ef3f6cb7.csv`).

All three captures were taken on 2026-10-08 (bronze path
`bronze/neso_data_portal/<family>/2026/10/08/`) and transformed in the same window. The silver
row counts equal the CSV data row counts: 102 + 315 + 1,462 = **1,879 rows**, no validation
failures, no rows excluded (gridflow `@.planning/v0.22-RESULTS.md`, section SCN-3).

## Families

### `resource_adequacy_2030s_peak_demand`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Spotlight year | `spotlight_year` | string | — | no | — | — |
| Historical weather year | `historical_weather_year` | string | — | no | — | — |
| Peak Demand (MW) | `peak_demand_mw` | float64 | — | no | — | MW |

- Entity key: `resource_id`, `edition`, `spotlight_year`, `historical_weather_year`
- Latest: `whole_capture` per `resource_id`
- Edition: `peak-demand-dataset.csv` → 2025
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured resource: `2025-12-12T12:36:08.151108`. CKAN emits it without
   an offset and gridflow reads it as UTC (gridflow
   `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). All 102 rows share it. Point-in-time
   queries cut on `available_at <= :as_of`.
2. **Event time (`none`).** The record has no temporal recipe, so `timestamp_utc` and `event_time`
   are the **capture time** (`2026-10-08T11:17:05.133341Z`), not a date the data describes. The
   year labels carry the period; no column is an instant. Do not read `timestamp_utc` as
   anything but "when gridflow captured the file".

Content: 102 rows = 3 spotlight years (`2030/31`, `2035/36`, `2040/41`) × 34 historical weather
years (`1984/85` to `2017/18`, including `1999/2000`). The key is the full spotlight × weather
grid and is unique across the body. The measure is **MW** (vendor dictionary), cast strictly to
float64. There are no blanks, no sentinel tokens and no zero values in this capture.

### `resource_adequacy_2030s_portfolio`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Name | `name` | string | — | no | — | — |
| Category | `category` | string | — | no | — | — |
| Technology | `technology` | string | — | no | — | — |
| Future Year | `future_year` | string | — | no | — | — |
| Installed Capacity (MW) | `installed_capacity_mw` | float64 | — | no | — | MW |
| Stored energy (MWh) | `stored_energy_mwh` | float64 | — | no | — | MWh |

- Entity key: `resource_id`, `edition`, `name`, `technology`, `future_year`
- Latest: `whole_capture` per `resource_id`
- Edition: `portfolio-capacity-dataset.csv` → 2025
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = `2025-12-11T13:47:53.306382`
   (UTC, read from CKAN's offset-less string). All 315 rows share it.
2. **Event time (`none`).** `timestamp_utc` = `event_time` = the capture time
   (`2026-10-08T11:17:08.685157Z`). The study year is in `future_year`, a label, not a timestamp.

Content: 315 rows = 7 `name` values × 15 `technology` labels × 3 `future_year` labels
(`2030/31`, `2035/36`, `2040/41`). The `name` values are `Portfolio 1` to `Portfolio 6` and
`Starting point`. Every name has all 45 technology and year rows. `TODO: verify` what
`Starting point` represents: it is a seventh portfolio name in the file, and the vendor
description does not define it. The 13 `category` labels group the 15 technologies. `LDES`
contains `Pumped hydro` and `Other LDES `, `DSR+Dynamic Demand-Shifting` contains `DSR` and
`Max. Dynamic Demand Shifting`, and every other category holds a single technology of the same
or near name. `category` is an attribute, not part of the key. Keep the technology spelling
exactly as supplied, including the **trailing space in `Other LDES `**.

Units are the vendor's: `Installed Capacity (MW)` is MW and `Stored energy (MWh)` is MWh. Both
cast strictly to float64 and are integer-valued in this capture. There are no blanks and no
sentinel tokens. **Zeros are real values**: 29 installed-capacity cells and 257 stored-energy
cells are 0 (longest consecutive run 1 and 13 respectively). `TODO: verify` what a zero stored-energy cell
means for a technology. No source defines zero as missing, so do not null them.

### `resource_adequacy_2030s_results`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Simulation Name | `simulation_name` | string | — | no | — | — |
| Spotlight year | `spotlight_year` | string | — | no | — | — |
| Historical weather year | `historical_weather_year` | string | — | no | — | — |
| Weather-conditional LOLE (h/year) | `weather_conditional_lole_h_year` | float64 | — | no | — | hours/year |
| Weather-conditional EEU (MWh/year) | `weather_conditional_eeu_mwh_year` | float64 | — | no | — | MWh/year |

- Entity key: `resource_id`, `simulation_name`, `spotlight_year`, `historical_weather_year`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = `2025-12-12T12:34:52.812310`
   (UTC, read from CKAN's offset-less string). All 1,462 rows share it.
2. **Event time (`none`).** `timestamp_utc` = `event_time` = the capture time
   (`2026-10-08T11:17:13.510244Z`). The spotlight and weather years are labels only.

**No `edition` column and no `edition` in the key.** The results resource's description does not
state which study edition it belongs to, unlike the other two (which say 2025). It is probably the
same study, but that is an inference, so gridflow stamps no edition on it
(`TODO: verify` with a resource-specific NESO statement; adding an edition later needs direct
evidence and `edition` added to the key).

Content: 1,462 rows over 18 `simulation_name` labels. Six are `Portfolio 1` to `Portfolio 6`; twelve are
sensitivity cases named `Sensitivity 01: ...` to `Sensitivity 12: ...`. Eleven of the labels are
phrased as "Portfolio 1 with ..." a change (for example a demand change, a doubled gas
forced-outage rate, removed interconnection, reduced hydrogen storage); Sensitivity 01 describes
its own build-out. Keep the whole label: it carries the description.
The grid is **ragged**: some simulations cover all three spotlight years (102 rows), some two
(68 rows) and `Sensitivity 03` one (34 rows). Every simulation has 34 weather years per covered
spotlight year. By spotlight year the file holds 272 rows for 2030/31, 578 for 2035/36 and 612
for 2040/41. `TODO: verify` whether the missing spotlight years are by design, since the vendor
text does not say.

The two measures are **weather-conditional LOLE in hours/year** and **weather-conditional EEU in
MWh/year** (vendor dictionary units). The dictionary describes them as averaged across the
plant-outage simulations for the given spotlight-year and weather-year pair. They are not
averaged across weather years. Both cast strictly to float64. There are no blanks and no sentinel
tokens. **Zeros are real values**: 1,195 LOLE cells and 1,197 EEU cells are 0 (longest consecutive run 33 for both columns).
Do not read a zero as missing. In the 2026-10-08 capture every EEU value is a whole multiple of
10 MWh and every LOLE value a whole hundredth of an hour, and two rows carry a LOLE above zero
with an EEU of 0 (`Sensitivity 08`, 2040/41, weather year 1996/97, 0.02 h; `Sensitivity 09`,
2035/36, 2012/13, 0.01 h). That fits EEU rounded to 10 MWh, but NESO does not state any
rounding (`TODO: verify`).

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Once in 2 years

The vendor's stated frequency is "once in 2 years", which matches a periodic study rather than a
feed. The package was created 2025-12-11 and its metadata last changed 2026-02-09. The three
resources were last modified between 2025-12-11 and 2025-12-12. There is no schedule in
gridflow: refresh is `adhoc`, and each family's latest data is the whole latest capture of its
resource. One capture per family exists so far (2026-10-08).

- `TODO: verify` whether a later study edition would replace these files in place under the same
  resource ids or arrive as new resources. Under `whole_capture` per `resource_id`, an in-place
  replacement would silently supersede the 2025 rows, and for the results table (no edition in
  the key) nothing in the data would show that the study had changed.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- none

All three families are **eligible** and nothing is held in this package. They are reference-style
scenario tables with `temporal: none`, so the CKAN vintage is the only point-in-time clock and
no issue-time question arises. Eligibility is recorded in gridflow
`@docs/neso_data_portal/eligibility.md`.

Open `TODO: verify` items (none of them holds an output): the edition of the results table; what
`Starting point` is; whether the portfolio technology rows overlap; whether NESO guarantees the
composite uniqueness that gridflow measured on the keys above (the vendor dictionary does not
state it); how weather years are weighted for any headline figure; and why the results grid is
ragged across spotlight years.

Related holds in the same batch (unit E-SEM, different packages): the Building Heat Model example
profile (@building-heat-model.md), the whole-system gas tables WS1 and WS2
(@fes-whole-system-gas-supply-data-table-ws1.md, @fes-whole-system-gas-supply-emissions-data-table-ws2.md)
and the two local-authority heat-model tables
(@local-authority-level-spatial-heat-model-outputs-fes.md). Nothing from those hold questions
carries over to this package.
