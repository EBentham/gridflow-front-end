---
source: "neso_data_portal"
package: "embedded-register"
dataset_key: "embedded_register"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Embedded generation register
  summary: >-
    NESO's list of embedded generation projects in Scotland, connected or contracted to connect:
    MW, connection site, plant type, status, dates.
  facts:
    vendor: "NESO Data Portal, package `embedded-register`: one CSV"
    cadence: "Twice weekly, Tuesdays and Fridays, as NESO's resource text states"
    grain: "One row per project or stage: 562 in the file of 16 October 2026"
  landscape: units
  what_it_is: >-
    NESO calls it "a list of connected or contracted to connect embedded generation projects in
    Scotland"; its file of 16 October 2026 also lists one project hosted by `NGET`. Each row is a
    project or one stage of one: connection site, host transmission owner, plant type, status, MW
    connected and MW contracted to change. NESO does not define "embedded".
  how_used:
    - "Size the contracted pipeline by plant type, status or connection site."
    - "Sum `mw_connected` and `mw_increase_decrease`; in these rows the cumulative is a running total."
    - "Place projects by `connection_site`, free text naming a substation or grid supply point."
  chart:
    type: bar
    silver: neso_data_portal/embedded_register
    value: mw_increase_decrease
    filter:
      - {column: published_at, op: eq, value: "2026-10-16T18:05:22.024485+00:00"}
    dedup: {"on": [project_number], order_by: capture_written_at}
    group: plant_type
    group_map:
      "Energy Storage System": storage
      "Wind Onshore": wind
      "PV Array (Photo Voltaic/solar)": solar
      "Hydro": water
      "Tidal": water
      "Wave": water
      "CCGT (Combined Cycle Gas Turbine)": thermal
      "Gas Reciprocating": thermal
      "CHP (Combined Heat and Power)": thermal
      "Thermal": thermal
      "Biomass": biomass
      "Waste": biomass
      "Energy Storage System;PV Array (Photo Voltaic/solar)": mixed
      "Energy Storage System;Wind Onshore": mixed
      "Energy Storage System;PV Array (Photo Voltaic/solar);Wind Onshore": mixed
      "Demand;Energy Storage System": mixed
      "Demand;Hydro": mixed
      "PV Array (Photo Voltaic/solar);Wind Onshore": mixed
      "Demand;PV Array (Photo Voltaic/solar);Wind Onshore": mixed
      "Hydro;PV Array (Photo Voltaic/solar)": mixed
      "Demand;Tidal": mixed
      "Demand;Energy Storage System;Wind Onshore": mixed
      "CHP (Combined Heat and Power);PV Array (Photo Voltaic/solar)": mixed
      "CHP (Combined Heat and Power);Demand": mixed
      "Demand;Wind Onshore": mixed
    aggregation: sum
    sort: value_desc
    unit: MW
  chart_view:
    title: Contracted MW by plant type, 16 October 2026 file
    caption: >-
      Silver `embedded_register`, NESO's file modified 16 October 2026: `mw_increase_decrease` (MW)
      summed per plant type, any contracted date. One negative 5.5 MW entry is read as a removal
      (70 + (-5.5) = 64.5) and netted. NESO warns of duplicate entries.
    alt: >-
      Horizontal bar chart of MW contracted to connect or be removed, summed per plant type group,
      in NESO's Embedded Register file of 16 October 2026, largest first: energy storage 4,853;
      mixed technologies 2,020; onshore wind 1,882; solar PV 1,106; biomass and waste 139; gas and
      thermal 106; hydro, tidal and wave 85. The seven bars sum to 10,191 MW.
    key:
      - {series: storage, label: Energy storage, paint: hatch-dots, note: "NESO's `Energy Storage System` on its own."}
      - {series: mixed, label: Mixed technologies, paint: hatch-cross, note: "Any plant type naming several, joined by `;`: mostly storage with solar or wind, some with `Demand`."}
      - {series: wind, label: Onshore wind, note: "`Wind Onshore`, net of one negative 5.5 MW entry (Paul's Hill), read as a removal."}
      - {series: solar, label: Solar PV, note: "NESO's `PV Array (Photo Voltaic/solar)`."}
      - {series: biomass, label: Biomass and waste, note: "`Biomass` and `Waste` summed."}
      - {series: thermal, label: Gas and thermal, paint: hatch-vertical, note: "CCGT, gas reciprocating, CHP and `Thermal` summed; NESO states no fuel for the last two."}
      - {series: water, label: "Hydro, tidal, wave", paint: hatch-lines, note: "`Hydro`, `Tidal` and `Wave` summed."}
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show`, then the CSV downloaded whole, skipped while its
      `last_modified` is unchanged. NESO renames the file at each update.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=embedded-register"
      - "GET https://api.neso.energy/dataset/4b0e109c-aa23-45ac-86c1-0bda557d1aab/resource/68b6f3a1-e1bf-403b-9062-0269fc758d77/download/embedded-register-16-october-2026.csv"
    commands:
      - {run: gridflow ingest neso_data_portal embedded_register --last 24h, comment: "whole file; window must end recently"}
      - {run: gridflow transform neso_data_portal embedded_register --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: published_at, op: eq, value: "2026-10-16T18:05:22.024485+00:00"}
        - {column: project_number, op: in, value: [PRO-000815-1, PRO-000815-2, PRO-000902, PRO-001213, PRO-001297, PRO-002244, PRO-003597, PRO-004878]}
      dedup: {"on": [project_number], order_by: capture_written_at}
      order_by: [project_number]
      columns: [project_number, project_status, mw_connected, mw_increase_decrease,
                cumulative_total_capacity_mw, mw_effective_from, stage, gate, host_to, plant_type,
                project_name, connection_site, customer_name, project_id, published_at, timestamp_utc]
    key: [project_number]
    caption: "16 October file: a staged pair, a negative entry, Gates 1 and 2, `NGET`'s project."
    fields:
      project_number: "NESO's unique project number; a staged project adds a dash and the stage"
      project_status: "Build-cycle stage, such as `Scoping` or `Built`; NESO holds no authority over it"
      mw_connected: "MW connected when the file was made; 0 until built and connected (NESO)"
      mw_increase_decrease: "MW to connect or be removed (NESO); negative read by us as a removal"
      cumulative_total_capacity_mw: "NESO: total across all stages; in these rows, the running total to this stage"
      mw_effective_from: "Contracted date (NESO); 16 October file: 129 already past, one 40 MW row blank"
      stage: "Stage number of a staged project; null when unstaged (NESO)"
      gate: "Connections Reform Gate, 1 or 2; null until a Gate contract is countersigned"
      host_to: "Transmission owner responsible for the connection; NESO's dictionary lists `SHET` or `SPT`"
      plant_type: "Fuel type contracted to connect; several types are joined by `;`"
      project_name: "Name of the generation project, as NESO spells it"
      connection_site: "Connection site name as NESO writes it, a substation or grid supply point"
      customer_name: "Name of the generator, NESO's customer"
      project_id: "Case-sensitive project id, shared by a project's stages; NESO plans to retire it"
      published_at: "NESO's last-modified time for the file, read as UTC; one per capture"
      timestamp_utc: "When gridflow captured the file, UTC; the register has no event time"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      `query()` filters on `timestamp_utc`, the capture time here, so these cells use `data.sql()`
      on the `_latest` relation, which holds the newest captured file only.
    cells:
      - |
        df = data.sql("""
            SELECT project_number, project_name, project_status, plant_type, host_to,
                   mw_connected, mw_increase_decrease, cumulative_total_capacity_mw,
                   mw_effective_from, stage, gate, published_at
            FROM silver_neso_data_portal_embedded_register_latest
            ORDER BY project_number
        """)
        cols = ["project_number", "project_status", "plant_type", "mw_connected",
                "mw_increase_decrease", "published_at"]
        df[cols].head()
      - |
        df.groupby("project_status")[["mw_connected", "mw_increase_decrease"]].sum().round(1)
      - |
        import pandas as pd
        dated = df.dropna(subset=["mw_effective_from"]).assign(
            year=lambda d: pd.to_datetime(d.mw_effective_from).dt.year)
        ax = dated.pivot_table(index="year", columns="project_status", values="mw_increase_decrease",
                               aggfunc="sum").plot.bar(stacked=True, figsize=(8, 4))
        ax.legend(title=None, fontsize=8, bbox_to_anchor=(1, 1), loc="upper left")
        ax.set(xlabel="year the MW change is contracted from (NESO)", ylabel="MW");
    needs: NESO's Embedded Register file
    plot_alt: >-
      Stacked bars of MW contracted to change per year of `mw_effective_from`, split by status, from
      NESO's file of 16 October 2026. Years run 2019 to 2036, without 2020. The tallest are 2026 at
      about 1,380 MW, 2033 at 1,290 and 2027 at 1,190. Years 2019 to 2025, already past, still carry
      MW; from 2030 most is Scoping.
  related:
    - {dataset: neso_data_portal/transmission-entry-capacity-tec-register, note: "Same columns plus `Agreement Type`, for transmission entry capacity holders"}
    - {dataset: neso_data_portal/interconnector-register, note: "The connection register for interconnectors, with import and export MW"}
    - {dataset: neso_data_portal/gis-boundaries-for-gb-grid-supply-points, note: "Boundaries and lookup for the GSPs many `connection_site` names cite"}
    - {dataset: neso_data_portal/embedded_wind_solar_forecast, note: "NESO's forecasts of embedded wind and solar output across GB"}
---

# Embedded Register

The **Embedded Register** is NESO's list of **embedded generation projects in Scotland** that are
either connected or contracted to connect (CKAN package `notes`,
@.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json). The two Scottish
transmission owners are named in the `Host TO` column (`SHET` and `SPT`). The file of 16 October 2026
also carries one row hosted by `NGET` (`PRO-001297`, Grimsby, site `Grimsby West 132kV Substation`),
outside the `SHET or SPT` the dictionary comment allows (silver, checked 2026-10-24). Each row is one project, or one **stage** of a staged project, with its connected
capacity, capacity contracted to connect or be removed later, the cumulative contracted total, the
date a change is contracted to take effect, the project's build status, its plant type and, since
November 2025, its connection **Gate**. `TODO: verify` the vendor's exact definition of "embedded";
the package notes do not define it.

The resource description says the file "contains the latest version of the Embedded Register
including all changes up to publication" and is updated "twice weekly on Tuesdays and Fridays". It
is therefore a **registry snapshot, not a time series**: the vendor describes each file as the latest
version of the register. gridflow holds two captures (the files of 6 and 16 October 2026); between
them one project joined and none left, so how a project that leaves the register appears (or whether
it simply drops out of the next file) is still not shown; `TODO: verify`. For modelling it is a pipeline
view of future Scottish embedded capacity, useful as a leading indicator of where distributed supply
and storage is contracted to arrive. It is a sibling of the transmission-connected registers
(@./transmission-entry-capacity-tec-register.md) and the interconnector register
(@./interconnector-register.md), and it should be read with the vendor's own caveat that status
classifications are produced "as far as we are aware" and carry no NESO authority (see the `Project Status` entry under the vendor dictionary and the gotchas below).

As of 2026-10-24 gridflow holds **two captures**: taken 2026-10-08 (561 rows, NESO's file of
6 October) and 2026-10-16 (562 rows, NESO's file of 16 October), so silver has **1,123 rows**, 540 of
them repeated unchanged between the two captures. The package is **eligible**: nothing is held, so
values may be used, and the site page shows rows of the 16 October file. (When first written on
2026-10-16 the note had one capture and gave only schema, counts and aggregate profiles.)

- Publisher group: Connection registers
- Registry group: connection-registers · archetype: REG
- Package page: [embedded-register](https://www.neso.energy/data-portal/embedded-register)

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Embedded Register | CSV | upload | `68b6f3a1-e1bf-403b-9062-0269fc758d77` |

The package has one resource, a CSV with disposition SILVER. It has no DOC or catalogue-only
resources and no `_files` family.

Download links and the two captures (a CKAN upload resource). Size, CKAN `last_modified` and hash come
from the capture sidecars under `C:/gridflow-data/bronze/neso_data_portal/embedded_register/2026/10/08/`
and `.../2026/10/16/`.

| File | Bytes | Data rows | CKAN `last_modified` | Captured (UTC) |
|---|---:|---:|---|---|
| [embedded-register-05-october-2026.csv](https://api.neso.energy/dataset/4b0e109c-aa23-45ac-86c1-0bda557d1aab/resource/68b6f3a1-e1bf-403b-9062-0269fc758d77/download/embedded-register-05-october-2026.csv) | 92,325 | 561 | 2026-10-06T10:47:45.071632 | 2026-10-08T10:36:47.628831 |
| [embedded-register-16-october-2026.csv](https://api.neso.energy/dataset/4b0e109c-aa23-45ac-86c1-0bda557d1aab/resource/68b6f3a1-e1bf-403b-9062-0269fc758d77/download/embedded-register-16-october-2026.csv) | 92,625 | 562 | 2026-10-16T18:05:22.024485 | 2026-10-16T20:18:02.195475 |

**Bronze body (full scan of the 2026-10-08 capture, 2026-10-16).** Valid UTF-8 with a **UTF-8 BOM**, CRLF line endings
(562 lines: one header and 561 data rows), one header row, body sha256 prefix `2feb369e` (full digest
in the sidecar, equal to the declared `Content-Length` of 92,325 bytes). The profiler (ADR-036) found
the same 561 rows. The file name carries a date, 05 October 2026, one day before the CKAN
`last_modified` of 2026-10-06; `TODO: verify` what the name date records. The 2026-10-16 capture
(sha256 prefix `43190337`) also has a BOM and CRLF endings, 563 lines (one header and 562 data rows),
the same 14-column header, and a file name dated 16 October 2026, the same day as its `last_modified`.

## Families

### `embedded_register`

- Kind: tabular · archetype: REG · refresh: daily · empty allowed: yes

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Project Name | `project_name` | string | — | yes | — | — |
| Customer Name | `customer_name` | string | — | yes | — | — |
| Connection Site | `connection_site` | string | — | yes | — | — |
| Stage | `stage` | float64 | — | yes | — | number |
| MW Connected | `mw_connected` | float64 | — | yes | — | MW |
| MW Increase / Decrease | `mw_increase_decrease` | float64 | — | yes | — | MW |
| Cumulative Total Capacity (MW) | `cumulative_total_capacity_mw` | float64 | — | yes | — | MW |
| MW Effective From | `mw_effective_from` | date | `%Y-%m-%d` | yes | — | yyyy-mm-dd |
| Project Status | `project_status` | string | — | yes | — | — |
| HOST TO | `host_to` | string | — | yes | — | — |
| Plant Type | `plant_type` | string | — | yes | — | — |
| Project ID | `project_id` | string | — | yes | — | — |
| Project Number | `project_number` | string | — | no | — | — |
| Gate | `gate` | float64 | — | yes | — | — |

- Entity key: `project_number`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks.**

- **Vintage** is `ckan_last_modified`. `published_at` and `available_at` both equal the CKAN
  `last_modified` of the captured file, here **2026-10-06T10:47:45.071632Z**. A point-in-time query
  (`WHERE available_at <= :as_of`) therefore sees a capture only from the moment NESO updated the
  file, not from the moment gridflow fetched it.
- **Event time** is `none`. The temporal recipe is `none`, so `timestamp_utc` (and the silver
  `event_time`) is the **capture time**, here 2026-10-08T10:36:47.633836Z. It is not a property of
  the project. A register has no observation instant. The only date in the body, `MW Effective From`,
  is a contractual date for a future change and stays a plain `date` column.

**One header epoch.** The record accepts one exact header, the 14 columns above (record version 1,
`dataset_version` `1+e1`). The package notes say a **Gate** column was added from 21 November 2025,
so earlier files presumably lacked it. gridflow holds no earlier capture, so a body without `Gate` is
not a known epoch and would fail the header match loudly rather than load. `TODO: verify` whether
NESO retains or serves the earlier layout.

**What the columns mean (vendor dictionary).** Descriptions and comments come from NESO's saved field
info for the resource (gridflow
`@.planning/research/neso-snapshots/field-info/20261008T114228Z/embedded_register.json`, 2026-10-08).
The dictionary's `info.label` and `info.notes` are empty, as for the whole catalogue.

- **`Project Name`**, **`Customer Name`**, **`Connection Site`**: free text. "Name of Generation
  Project", "Name of Generator", "Name of Generation Connection Site". Stored as supplied (no normalisation).
- **`Stage`**: unit "number". Staged capacity: how much capacity the customer will connect and when,
  in chunks aligned to the build or to reinforcement works. The vendor comment says the field "is only
  completed if the project is staged otherwise it will be empty". The body carries it as text like
  `1.00` and silver types it `float64`. It is an ordinal label, not a measurement.
- **`MW Connected`**: unit **MW**. "Amount of capacity currently connected to the National Grid". Vendor
  comment: the field "will state 0MW until the project is built and connected". `0` is a real value, the
  vendor's way of saying not yet connected.
- **`MW Increase / Decrease`**: unit **MW**. "Amount of capacity contracted to connect or be removed at
  a future date". Vendor comment: it "will state 0MW unless the capacity is due to increase or
  decrease". NESO does not state the sign. We read a negative value as a contracted removal: the one
  negative row, `PRO-000902`, has 70.0 connected, -5.5 here and 64.5 cumulative (70 + (-5.5) = 64.5).
- **`Cumulative Total Capacity (MW)`**: unit **MW**. "Total amount of capacity contracted across all
  Stages". See the staged-project gotcha below.
- **`MW Effective From`**: dictionary type `date`, unit string `yyyy-mm-dd`. "Date on which Connection is
  contracted to be effective from". Vendor comment: it "will only include dates for future connections
  or increase/decreases to capacity, otherwise this field will be empty". No time of day and no time
  zone are given, so silver keeps a calendar `date` and builds no instant from it. The dictionary
  example (`31/10/2032`) uses day-first order, but the bronze body uses `YYYY-MM-DD` (for example, the
  first cell is in the form `2030-10-31`), which is what the record's format `%Y-%m-%d` parses. This
  differs from the TEC register, whose body uses `dd/mm/yyyy`.
- **`Project Status`**: "Indicates what stage the Project is at in it's build cycle" (vendor spelling).
  Vendor comment: the classifications rest on information NESO has "ascertained from the customer or
  from another source" and NESO holds "no authority" over them; they are produced on an "as far as we
  are aware" basis.
- **`HOST TO`**: "Indicates which Transmission Owner (TO) is responsible for the connection", `SHET` or
  `SPT` per the vendor comment.
- **`Plant Type`**: "Indicates the fuel type contracted to connect". Multi-technology projects hold
  several values joined by a semicolon (see below).
- **`Project ID`**: "Unique Project Identifier". Vendor comment: the reference is **case sensitive**.
- **`Project Number`**: "Unique Project Number". Vendor comment: where a project has more than one
  stage, the number is followed by a dash and the stage number, for example the dictionary's
  `PRO-000630-1`. The resource description says NESO plans to phase out Project ID in favour of
  Project Number and will keep both "until the end of this year" (the text carries no year; the
  snapshot is from 2026, `TODO: verify` which year is meant).
- **`Gate`**: dictionary unit `n/a`, type number. "Indicates which Gate the Project is contracted at".
  Vendor comment: it is filled only once a signed Gate 1 or Gate 2 contract is countersigned, and
  until then "all existing contracted projects will appear blank". Blank is therefore "no countersigned
  Gate contract", not a missing observation. The package notes tie the column to CUSC paragraphs
  6.30.3.2 and 6.35.2 and the Connections Reform process.

**Identity and selection (ADR-036, ADR-039).**

- The entity key is `project_number`, with `latest: whole_capture`. The registry (ADR-036) recorded the
  documented identifier as **measured unique** in the captured body, in contrast to the TEC register,
  where `PRO-000053` occupies two non-identical rows. In silver on 2026-10-16: **561 rows, 561 distinct
  `project_number`**. The 2026-10-16 capture: 562 rows, 562 distinct. Across the two captures
  `project_number` is unique within each capture only, so any read of the base relation repeats it.
- `project_id` is **not** a row key. There are 544 distinct values across the 561 rows. The 17 extra
  rows come from 14 projects that have more than one stage row: those 14 `project_id` values cover
  31 rows, and every one of the 31 has a `Stage` value and a dashed `Project Number`. All other rows
  (530) have no stage and a plain `PRO-nnnnnn` number. The 14 staged projects hold stages 1 to 5.
- Case: the 544 distinct IDs are also 544 distinct after lowercasing, so no two projects differ only by
  case in this capture. Never fold case, since the vendor says the reference is case sensitive.
- `_latest` is `whole_capture`: the newest complete capture, so a project missing from a later file is
  gone from `_latest` too. Between the captures of 2026-10-08 and 2026-10-16, every `project_id` and
  `stage` pair kept its `project_number` (561 pairs; the one new pair is `PRO-001297`). `TODO: verify`
  that `Project Number` stays stable when a project gains a stage and its number gains a suffix; no
  such case occurs between these two files.

**Sentinels and missing values (FACTS g5).** The full-body scan found no cell equal to `NA`, `N/A`, `-1`,
`99999`, `-` or `null`, and no padded cell. The record declares no null tokens, and nothing is mapped
to null by token. Empty cells are the only missingness. Exact blanks and zero counts:

| Column | Blank cells | Cells equal to zero |
|---|---:|---:|
| `Stage` | 530 | 0 |
| `MW Connected` | 0 | 345 |
| `MW Increase / Decrease` | 0 | 215 |
| `Cumulative Total Capacity (MW)` | 0 | 0 |
| `MW Effective From` | 215 | n/a (date) |
| `Gate` | 464 | 0 |
| every other column | 0 | n/a (text) |

Silver nulls equal the blank counts above (2026-10-16), so nothing was dropped, imputed or excluded. A
zero in `MW Connected` or `MW Increase / Decrease` is the vendor's stated "0MW" convention and is kept
as a real zero, never converted to null.

**Row counts and profile (silver, queried 2026-10-16T18:37Z; the 2026-10-08 capture, NESO's file of
6 October).** The file of 16 October differs as follows (silver, checked 2026-10-24): 562 rows, 545
distinct `project_id`; one added row, `PRO-001297` (`NGET`, `Under Construction/Commissioning`, 40 MW
contracted, no `MW Effective From`); none removed; 540 rows identical; among the 561 shared projects
`MW Effective From` changed on 13, `Gate` on 10 (all from blank to 2), `Project Status` on 4 (all
`Scoping` to `Consents Approved`), and names, sites or MW on a few more. Its counts: Scoping 251, Built
217, Consents Approved 62, Awaiting Consents 26, Under Construction/Commissioning 6; `Gate` 1 / 2 /
blank 56 / 51 / 455; 217 blank effective dates (216 on `Built` rows plus `PRO-001297`); 129 rows dated
before the file's own date.

| Measure | Value |
|---|---:|
| Rows | 561 |
| Distinct `project_number` | 561 |
| Distinct `project_id` | 544 |
| Staged rows (non-blank `stage`) | 31 |
| `HOST TO` = `SHET` / `SPT` | 352 / 209 |
| `Gate` = 1 / 2 / blank | 56 / 41 / 464 |
| `Project Status`: Scoping | 255 |
| `Project Status`: Built | 217 |
| `Project Status`: Consents Approved | 58 |
| `Project Status`: Awaiting Consents | 26 |
| `Project Status`: Under Construction/Commissioning | 5 |
| Rows with `MW Connected` > 0 | 216 |
| Rows with `MW Increase / Decrease` > 0 / < 0 | 345 / 1 |
| Distinct `MW Effective From` values | 141 |
| `MW Effective From` range | 2019-10-31 to 2036-10-31 |
| `MW Effective From` before the 2026-10-08 capture | 138 |

In this capture all 215 blank effective dates sit on `Built` rows; 2 `Built` rows do carry a date. No `Built` row has a
Gate. Gate 1 appears on `Scoping` and `Awaiting Consents` rows only; Gate 2 appears on `Scoping`,
`Awaiting Consents`, `Consents Approved` and `Under Construction/Commissioning` rows. `Plant Type` has
25 distinct values, led by `Wind Onshore` (196 rows), `Energy Storage System` (131) and
`PV Array (Photo Voltaic/solar)` (71). Values with a semicolon are multi-technology (for example, storage
combined with solar or wind, and `Demand;`-prefixed combinations): gridflow stores the string whole and
does not split it. `TODO: verify` the vendor's full list of plant types; none is published.

**Activation (2026-10-08, master `29b563c`, PR #85).** The profiler pilot (unit E, ADR-036) froze the
record and the activation transformed the 2026-10-08 capture with
`gridflow transform neso_data_portal embedded_register --start 2026-10-08 --end 2026-10-08` (cutoff
2026-10-08, the newest bronze partition). There was no prior silver, so nothing was overwritten and no
snapshot was taken. Silver holds **561 rows**, equal to the capture's data rows, with 0 excluded; the
reconcile over the six pilot families (`--cutoff 2026-10-08`) exited 0 with 0 gaps, and the base view
and `_latest` both counted 561 rows (RULINGS 503/504, gridflow `@.planning/v0.22-RESULTS.md` section E).
The package is **eligible** (it is one of the three eligible pilot registers). No later ruling changes
this family: a search of RULINGS for the family key finds nothing after the activation, and rulings 591
and 596 concern the demand-forecast families, not this register. Ruling 879 closed the docs gaps that
this page fills.

Silver layout: one Parquet file per capture (two as of 2026-10-24) under
`C:/gridflow-data/silver/neso_data_portal/embedded_register/year=2026/month=10/`. The `year=`/`month=`
partition is the **capture** date, not any project date. Columns (22): the 14 vendor columns, then
`timestamp_utc`, `published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`,
`available_at`, `source_run_id` and `dataset_version`. All timestamps are tz-aware UTC. No gold view or
builder reads this family; only the generated base and `_latest` views exist.

**Gotchas.**

1. **Do not sum `Cumulative Total Capacity (MW)` across rows.** It is the total "across all Stages". For
   staged projects the value repeats and grows from one stage row to the next: 17 of the 31 staged rows
   have a cumulative total that is not `MW Connected` plus `MW Increase / Decrease`, and the stage rows of
   one project look like a running total. In both captures (files of 6 and 16 October 2026) every
   staged row's cumulative total equals `MW Connected` plus `MW Increase / Decrease` summed over that
   project's stages up to and including its own (31 rows, 0 mismatches at 0.01 MW); every unstaged row's
   equals its own two columns. So `MW Connected` and `MW Increase / Decrease` add up across rows and the
   cumulative column does not. NESO states no arithmetic beyond "across all Stages"; `TODO: verify`.
2. **The vendor warns of duplicate entries.** The package notes say capacity across stages and technology
   types is "presented in aggregate, which may result in duplicate entries", and that NESO intends to
   split capacity by stage and technology later. A future capture may change the row grain.
3. **Unstaged "second lines".** The resource description says some projects have two lines without stage
   numbers, usually meaning a built project that is adding another type of generation, and that the second
   line "will fall away" once built. This capture shows no `project_id` with two unstaged rows
   (`project_number` is unique), but a later capture might.
4. **A negative `MW Increase / Decrease` reads as a contracted removal (our reading; NESO states no
   sign).** One row (a built project, `PRO-000902`) carries one in both captures: 70 + (-5.5) = 64.5
   cumulative. Do not clip it.
5. **Blank means different things per column.** Blank `Stage` = unstaged, blank `Gate` = no countersigned
   Gate contract, blank `MW Effective From` = no future change dated (in the 2026-10-08 capture all 215
   blanks are on `Built` rows and 2 of the 217 `Built` rows carry a date; in the file of 16 October, 216
   blanks are on `Built` rows and 1 `Built` row, `PRO-000902`, carries a date, because `PRO-000886` moved
   its 49.95 MW from contracted to connected and lost its 2022-02-15 date). In the file of 16 October one non-built row, `PRO-001297` with 40 MW
   contracted, has no date, against the dictionary comment. Dated rows include past dates: 129 rows in
   that file are dated before 16 October 2026, all but one not `Built`, although the comment says the field
   holds "dates for future connections". Read it as the contracted date, not a forecast.
6. **Dictionary example mismatches.** The `Project ID` example in the dictionary has 15 characters; every
   captured value has 18. The date example is day-first; the body is ISO. Trust the body, as the record
   does.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Twice weekly

The resource description says Tuesdays and Fridays. The registry polls daily, so most polls should find
the file unchanged. An unchanged file adds no capture: `iter_members` skips an upload resource as
`unchanged` when its newest capture carries the live CKAN `last_modified`, before any download
(gridflow `src/gridflow/connectors/neso_data_portal/client.py`, `iter_members`). Two captures are on
disk: 2026-10-08, holding the file NESO modified on Tuesday 2026-10-06, and 2026-10-16, holding the
file modified on Friday 2026-10-16 (18:05 UTC). The vendor's stated cadence would also give updates on
2026-10-09 and 2026-10-13; gridflow has no capture of either. `TODO: verify` whether NESO published
them (the capture of 2026-10-16 replaced whatever was current then; nothing between is held).

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- none

The family is eligible and nothing is held. The open items are `TODO: verify` points, not holds: the
exact effective instant and zone of `MW Effective From` (unit E-SEM, the semantics research unit for the pilot families; the
column stays a calendar date and no timestamp is built from it), a vendor statement of the
staged-capacity arithmetic the two captures show (a running total over stages), and the stability of
`Project Number` when a project gains a stage. Each would need more captures or a vendor statement.
