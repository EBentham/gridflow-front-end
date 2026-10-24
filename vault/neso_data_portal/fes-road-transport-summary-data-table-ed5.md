---
source: "neso_data_portal"
package: "fes-road-transport-summary-data-table-ed5"
dataset_key: "fes_ed5_road_transport"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: FES road transport summary
  summary: >-
    NESO's Future Energy Scenarios (FES) table of GB road transport: energy demand, vehicle numbers
    and capacity, one file per edition.
  facts:
    vendor: "NESO Data Portal: four CSVs, one per edition, 2023 to 2026"
    cadence: "Ad hoc (NESO); editions 2023 to 2026, as at 6 October 2026"
    grain: "One value per data item, scenario or pathway, fuel and year label, per edition"
    history: "NESO created the package on 7 July 2023"
  landscape: power
  what_it_is: >-
    Each row is a road transport data item, in `TWh`, `GW` or a vehicle count such as `# Cars`,
    for one scenario or pathway and one fuel, with a column per year. NESO's ED6 notes describe
    the items and time peak items at the winter system peak, 5pm to 6pm. NESO calls the 2026 file
    a Ten-Year Outlook output.
  how_used:
    - "Electric vehicle numbers and charging demand under each FES scenario or pathway"
    - "Road transport energy demand by fuel, edition by edition"
    - "Each item read with the same edition's ED6 notes"
  chart:
    type: bar
    silver: neso_data_portal/fes_ed5_road_transport
    value: value
    filter:
      - {column: edition, op: eq, value: 2025}
      - {column: pathway, op: eq, value: Holistic Transition}
      - {column: data_item, op: eq, value: Electric Vehicle Peak Demand}
      - {column: projection_year, op: in, value: [2025, 2030, 2035, 2040, 2045, 2050]}
    dedup: {"on": [resource_id, edition, data_item, scenario, pathway, projection_year], order_by: capture_written_at}
    group: projection_year
    aggregation: sum
    sort: label
    unit: GW
  chart_view:
    title: EV peak demand, FES 2025, Holistic Transition
    caption: >-
      Silver `fes_ed5_road_transport`, FES 2025 (NESO's file of 10 December 2025), pathway Holistic
      Transition: `Electric Vehicle Peak Demand` in `GW`, one row per bar, every fifth year label as
      NESO heads its columns. A projection, not an outturn.
    alt: >-
      Horizontal bar chart of NESO's projected electric vehicle peak demand in GW, FES 2025 edition,
      pathway Holistic Transition, one bar every fifth year label: 2025 0.9; 2030 2.2; 2035 5.1;
      2040 8.1; 2045 9.2; 2050 9.0. It rises tenfold to 2045, then dips slightly.
    key:
      - {series: value, label: EV peak demand, codes: Electric Vehicle Peak Demand, paint: petrol, note: "NESO's 2025 ED6 notes: demand at winter system peak, 5pm to 6pm, after smart charging"}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then four CSVs, each downloaded whole unless its
      `last_modified` is unchanged. Shown: 2023, 2025 and 2026; edition comes from the file name.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=fes-road-transport-summary-data-table-ed5"
      - "GET https://api.neso.energy/dataset/28303fe9-62d4-46c5-ad15-a1d0e59f98cb/resource/076c5c72-ecea-47c9-81b6-e93fe824d5d4/download/fes2023_ed5_v002.csv"
      - "GET https://api.neso.energy/dataset/28303fe9-62d4-46c5-ad15-a1d0e59f98cb/resource/ce76da34-6eb0-43a1-8e93-3cc833d6d1b4/download/fes2025_ed5_v006.csv"
      - "GET https://api.neso.energy/dataset/28303fe9-62d4-46c5-ad15-a1d0e59f98cb/resource/1b59c48f-f51a-4e32-a9e7-baca0b78a042/download/10yo2026_ed5_v001.csv"
    commands:
      - {run: gridflow ingest neso_data_portal fes_ed5_road_transport --last 24h, comment: "changed files only; whole CSVs"}
      - {run: gridflow transform neso_data_portal fes_ed5_road_transport --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: edition, op: eq, value: 2025}
        - {column: data_item, op: eq, value: Electric Vehicle Peak Demand}
        - {column: projection_year, op: in, value: [2035, 2036]}
        - {column: pathway, op: in, value: [Holistic Transition, Electric Engagement, Falling Behind, Ten Year Forecast]}
      dedup: {"on": [resource_id, edition, data_item, scenario, pathway, projection_year], order_by: capture_written_at}
      order_by: [projection_year, pathway]
      columns: [data_item, pathway, projection_year, value, unit, fuel, peak_annual_minimum, scenario,
                edition, resource_id, published_at, timestamp_utc]
    key: [resource_id, edition, data_item, scenario, pathway, projection_year]
    caption: "FES 2025 electric vehicle peak demand, labels 2035 and 2036, four of the five pathways."
    fields:
      data_item: "NESO's data item; the same edition's ED6 notes describe each one"
      pathway: "NESO's pathway name in the 2024 and 2025 files; null in the others"
      projection_year: "NESO's year column header, as an integer; NESO states no period for it"
      value: "The cell, in the row's `unit`; a blank is null, a zero a value"
      unit: "NESO's unit for the row: `GW`, `TWh` or a count such as `# Cars`"
      fuel: "NESO's fuel label, such as `Electricity` or `Petrol/Diesel`"
      peak_annual_minimum: "NESO's item type; these files carry only `Peak` and `Annual`"
      scenario: "NESO's scenario name in the 2023 and 2026 files; null in these rows"
      edition: "FES edition, from the file name; 2026 is NESO's Ten-Year Outlook"
      resource_id: "CKAN file id, one per edition; first column of the entity key"
      published_at: "NESO's last-modified time for the edition's file, read as UTC"
      timestamp_utc: "When gridflow captured the file, UTC; the table has no event time"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  caveat: "NESO states no period or date for the year labels, or what blanks mean."
  notebook:
    lead: >-
      `query()` filters on `timestamp_utc`, the capture time here, so these cells use `data.sql()`
      on the `_latest` view, which keeps every edition's file, and pick FES 2025 by name.
    cells:
      - |
        peak = data.sql("""
            SELECT pathway, projection_year, value AS gw
            FROM silver_neso_data_portal_fes_ed5_road_transport_latest
            WHERE edition = 2025 AND data_item = 'Electric Vehicle Peak Demand'
        """)
        wide = peak.pivot(index="projection_year", columns="pathway", values="gw").rename_axis(index=None, columns=None)
        wide.loc[[2025, 2030, 2035, 2036, 2040, 2045, 2050]]
      - |
        ax = wide.loc[2025:].plot(figsize=(8, 3.5), xlabel="NESO's year label",
                                 ylabel="EV peak demand, GW");
      - |
        data.sql("""
            SELECT edition, scenario, pathway, MIN(projection_year) AS first_blank_label,
                   COUNT(*) AS blank_cells
            FROM silver_neso_data_portal_fes_ed5_road_transport_latest
            WHERE value IS NULL
            GROUP BY edition, scenario, pathway
            ORDER BY edition
        """)
    needs: NESO's four FES road transport files
    plot_alt: >-
      Line plot of NESO's projected electric vehicle peak demand in GW, FES 2025 edition, year labels
      2025 to 2050, one line per pathway. All start near 0.9; Falling Behind ends highest at 15.0,
      Hydrogen Evolution 13.8, Electric Engagement 13.5, Holistic Transition 9.0. Ten Year Forecast
      stops at 5.6 at label 2035.
  related:
    - {dataset: neso_data_portal/fes-road-transport-notes-data-table-ed6, note: "NESO's notes on these items; read both from one edition"}
    - {dataset: neso_data_portal/fes-electricity-demand-summary-data-table-ed1, note: "NESO's FES GB electricity demand table, from the same editions"}
    - {dataset: neso_data_portal/fes-flexibility-data-table-data-table-flx1, note: "FES flexibility table; earlier ED6 notes say vehicle-to-grid feeds flexibility modelling"}
---

# FES: Pathways to Net Zero – Road Transport Summary Data table (ED5)

NESO's road-transport summary table from the Future Energy Scenarios (FES) data workbook. It is
one wide table per edition. Each row is a data item (a road-transport energy demand, a vehicle
count or a capacity) for one scenario or pathway and one fuel, with one column per year. Its
rows split into two kinds, named by the vendor's `Peak/Annual/Minimum` column: **Annual** items
and **Peak** items. The vendor's `Unit` column carries `GW`, `TWh` and a set of vehicle-count
units such as `# Cars`. Once the hold below lifts it is a candidate scenario input for
electric-vehicle charging demand and road-transport fuel demand in GB energy-system models. It sits beside the other FES summary tables
(@fes-electricity-demand-summary-data-table-ed1.md,
@fes-european-electricity-supply-data-table-es2.md,
@fes-flexibility-data-table-data-table-flx1.md).

The package has four resources, one per edition: 2023, 2024, 2025 and 2026. The 2026 resource has
the filename prefix `10yo2026`. The batch spec treats the 2026 tables as the **Ten Year Outlook**
rather than a full FES edition (gridflow `@.planning/phases/v0.22-K-SCN-2/K-SCN-2a-SPEC.md`), and
NESO's 2026 resource description says the same: "One of the Ten-Year Outlok outputs" (sic;
catalogue snapshot `20261006T195819Z`).
`TODO: verify` how NESO scopes the 2026 outlook against the 2023–2025 FES editions before
comparing the editions column for column.

**The silver output of this family is held in gridflow (unit E-SEM).** This note gives its schema,
row counts and structure. Under ruling 66 the site page shows its rows (a chart, eight sample rows
and a notebook) with one caveat line naming the open question: the meaning of the year label and
of a blank cell is not established (see Holds). The package-level
`eligibility: eligible` in the front matter is the package registry entry. The hold is per family.

Reading rules for anyone who does open the silver:

- **Edition is a dimension.** The four resources are four separately published tables.
  Never sum or average across `edition`. The 2023, 2024, 2025 and 2026 rows for
  the same data item and the same year are four different forecasts, not four observations.
- **`scenario` and `pathway` are two separate columns.** The 2023 and 2026 files head the column
  `Scenario`. The 2024 and 2025 files head it `Pathway`. Each silver row has exactly one of the
  two populated and the other null. gridflow does not merge them. `TODO: verify` whether NESO
  treats the two headings as the same concept.
- **Counts and energy share one `value` column.** Vehicle counts (`# Cars` and so on), `GW` and
  `TWh` all land in `value`. The row's `unit` is the only thing that tells them apart. Filter by
  `unit`. Never sum across units.
- **`projection_year` is a label.** It is the integer column header. The period it denotes is
  undocumented (see Holds).
- **A null `value` is a blank vendor cell**, with an undocumented meaning. A `0` is a value.

- Publisher group: FES: Pathways to Net Zero
- Registry group: future-energy-scenarios · archetype: SCN
- Vendor tags: Demand, FES, FES2023, Forecast, Subscribable, Transport

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Road Transport Summary (ED5) 2023 | CSV | upload | `076c5c72-ecea-47c9-81b6-e93fe824d5d4` |
| Road Transport Summary (ED5) 2024 | CSV | upload | `7189f5d3-aed3-41b7-962f-fdb9fe11cbb7` |
| Road Transport Summary (ED5) 2025 | CSV | upload | `ce76da34-6eb0-43a1-8e93-3cc833d6d1b4` |
| Road Transport Summary (ED5) 2026 | CSV | upload | `1b59c48f-f51a-4e32-a9e7-baca0b78a042` |

All four are `SILVER` and feed the one family `fes_ed5_road_transport`. There is no `DOC`
resource in the package. The files, as captured on 2026-10-08:

| Edition | Download | Bytes | Wide data rows | CKAN `last_modified` (offset-less, read as UTC) |
|---|---|---:|---:|---|
| 2023 | [fes2023_ed5_v002.csv](https://api.neso.energy/dataset/28303fe9-62d4-46c5-ad15-a1d0e59f98cb/resource/076c5c72-ecea-47c9-81b6-e93fe824d5d4/download/fes2023_ed5_v002.csv) | 95,142 | 315 | `2025-07-01T17:03:39.781640` |
| 2024 | [fes2024_ed5_v003.csv](https://api.neso.energy/dataset/28303fe9-62d4-46c5-ad15-a1d0e59f98cb/resource/7189f5d3-aed3-41b7-962f-fdb9fe11cbb7/download/fes2024_ed5_v003.csv) | 89,997 | 315 | `2025-07-01T17:04:57.258965` |
| 2025 | [fes2025_ed5_v006.csv](https://api.neso.energy/dataset/28303fe9-62d4-46c5-ad15-a1d0e59f98cb/resource/ce76da34-6eb0-43a1-8e93-3cc833d6d1b4/download/fes2025_ed5_v006.csv) | 90,217 | 315 | `2025-12-10T17:01:17.874457` |
| 2026 | [10yo2026_ed5_v001.csv](https://api.neso.energy/dataset/28303fe9-62d4-46c5-ad15-a1d0e59f98cb/resource/1b59c48f-f51a-4e32-a9e7-baca0b78a042/download/10yo2026_ed5_v001.csv) | 13,578 | 63 | `2026-09-16T14:30:16.337617` |

The stable handle for a resource is its id, not the file name. Every body decodes as strict
UTF-8 with CRLF line endings, no BOM, no ragged rows and no embedded newlines (gridflow
`@.planning/phases/v0.22-K-SCN-2/K-SCN-2-FACTS.md` §9). The file name, the resource name and the
captured edition all agree for every resource. gridflow reads the edition from the exact
file name and never infers it from the projection years, the CKAN timestamps or the capture date.

The 2026 resource is about a seventh of the size of the others because it has 63 data rows
against 315: one scenario against five (see Families).

The CKAN datastore view of the 2026 resource (field-info probe, 2026-10-08) types the year
columns `2023`–`2036` as numeric and `2037`–`2050` as text. gridflow reads the CSV body, not the
datastore, so the typing does not touch silver. It is consistent with the profile, which finds
those 14 columns entirely blank in the 2026 body.

## Families

### `fes_ed5_road_transport`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Data item | `data_item` | string | — | no | — | — |
| Unit | `unit` | string | — | no | — | — |
| Scenario | `scenario` | string | — | yes | — | — |
| Fuel | `fuel` | string | — | no | — | — |
| Peak/Annual/Minimum | `peak_annual_minimum` | string | — | no | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 1: `2017` → 2017, `2018` → 2018, `2019` → 2019, `2020` → 2020, `2021` → 2021, `2022` → 2022, `2023` → 2023, `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Data item | `data_item` | string | — | no | — | — |
| Unit | `unit` | string | — | no | — | — |
| Pathway | `pathway` | string | — | yes | — | — |
| Fuel | `fuel` | string | — | no | — | — |
| Peak/Annual/Minimum | `peak_annual_minimum` | string | — | no | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 2: `2020` → 2020, `2021` → 2021, `2022` → 2022, `2023` → 2023, `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

Schema, epoch 3:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Data item | `data_item` | string | — | no | — | — |
| Unit | `unit` | string | — | no | — | — |
| Pathway | `pathway` | string | — | yes | — | — |
| Fuel | `fuel` | string | — | no | — | — |
| Peak/Annual/Minimum | `peak_annual_minimum` | string | — | no | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 3: `2023` → 2023, `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

Schema, epoch 4:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Data item | `data_item` | string | — | no | — | — |
| Unit | `unit` | string | — | no | — | — |
| Scenario | `scenario` | string | — | yes | — | — |
| Fuel | `fuel` | string | — | no | — | — |
| Peak/Annual/Minimum | `peak_annual_minimum` | string | — | no | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 4: `2023` → 2023, `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

- Entity key: `resource_id`, `edition`, `data_item`, `unit`, `scenario`, `fuel`, `peak_annual_minimum`, `pathway`, `projection_year`
- Latest: `whole_capture` per `resource_id`
- Edition: `fes2023_ed5_v002.csv` → 2023; `fes2024_ed5_v003.csv` → 2024; `fes2025_ed5_v006.csv` → 2025; `10yo2026_ed5_v001.csv` → 2026
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured resource, read as UTC per ADR-030 (gridflow
   `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). There is one vintage per
   resource, and every row of an edition shares it (dates in the file table above). Checked on
   every silver row on 2026-10-14: `available_at` equals `published_at`, and `published_at`
   equals the resource's `last_modified`. The vintage says when the file last changed on the
   portal. It does not say when NESO first published the edition. For the 2023 and 2024
   resources the two `last_modified` values are about 80 seconds apart on the same day, so they
   look like one bulk upload (`TODO: verify` with the vendor). Do not read them as the original
   publication dates of the FES 2023 and FES 2024 workbooks.
2. **Event time (temporal recipe `none`).** The record declares no event-time recipe, because the
   year labels have no established period (see Holds). `timestamp_utc` is therefore the **capture
   time**, not a modelled time. `event_time` and `capture_written_at` carry the same instant. All
   rows of an edition share one `timestamp_utc`, and the four editions' captures ran within about
   nine seconds of each other on 2026-10-08. Do not use `timestamp_utc` as a forecast horizon or
   a model time axis. The only year information is `projection_year`, a label.

Rows per edition and resource (silver, from the 2026-10-08 transform):

| Edition | Resource id | Wide rows × year columns | Silver rows | Projection-year labels |
|---|---|---|---:|---|
| 2023 | `076c5c72-ecea-47c9-81b6-e93fe824d5d4` | 315 × 34 | 10,710 | 2017–2050 |
| 2024 | `7189f5d3-aed3-41b7-962f-fdb9fe11cbb7` | 315 × 31 | 9,765 | 2020–2050 |
| 2025 | `ce76da34-6eb0-43a1-8e93-3cc833d6d1b4` | 315 × 28 | 8,820 | 2023–2050 |
| 2026 | `1b59c48f-f51a-4e32-a9e7-baca0b78a042` | 63 × 28 | 1,764 | 2023–2050 |
| | | | **31,059** | |

Every edition has 63 distinct `data_item` values and 7 distinct `fuel` values. The
`peak_annual_minimum` column carries the two values `Annual` and `Peak` in every edition, despite
the header's third word, `Minimum`. The 2023 file has 5 distinct `scenario` values, the 2024 and
2025 files have 5 distinct `pathway` values, and the 2026 file has 1 `scenario` value. Each of
the 63 data items therefore appears once per scenario or pathway: 5 × 63 = 315 wide rows in the
2023–2025 files and 1 × 63 = 63 in the 2026 file. `TODO: verify` the vendor's definition of each scenario and pathway label, and
whether a label in one edition is the same scenario as a label in another.

**Units (vendor dictionary: the row's `Unit` field).** Each wide row carries its own unit. The
unit is read from that field and never inferred from the column name. The units, as published
(FACTS g4), and the wide rows in each file:

| `unit` | 2023 / 2024 / 2025 | 2026 |
|---|---:|---:|
| `GW` | 20 | 4 |
| `TWh` | 145 | 29 |
| `# Cars` | 30 | 6 |
| `# Vans` | 30 | 6 |
| `# Motorbikes` | 20 | 4 |
| `# Buses` | 25 | 5 |
| `# HGVs` | 25 | 5 |
| `# Vehicles` | 20 | 4 |

- The silver `unit` column holds these eight strings verbatim, `#` included. There is no
  conversion and no separate unit column beyond `unit` itself.
- `TWh` rows are energy over a period and `GW` rows are power. The dictionary's year description
  does not say which period the `TWh` rows integrate over, nor at what moment a `# Vehicles`
  count is taken. Both are part of the held question.
- `# Vehicles` is not documented as the sum of the other vehicle-count units, and this page does
  not treat it as one. `TODO: verify` whether it is a total, a separate category or an
  overlapping one before using it beside `# Cars`, `# Vans` and the rest.
- Whether a count item is a stock at a date or a flow is not established. `TODO: verify`.

**Sentinels and missing values (FACTS g5).** The record declares no null token.

- **Blank cells** are kept as **null** `value`. They are not dropped and not filled.
- The vendor does not say what a blank means. Unmodelled, unavailable, inapplicable and not yet
  published are all possible. Their position or frequency does not settle it. `TODO: verify`
  (part of the hold).
- The blanks sit at the far end of the horizon. The CSV bodies have these blank year columns:

  | Edition | Year columns with 63 blank cells each | Year columns with 58 blank cells each |
  |---|---|---|
  | 2023 | `2029`–`2050` | none |
  | 2024 | `2030`–`2032` | `2033`–`2050` |
  | 2025 | `2036`–`2050` | none |
  | 2026 | `2037`–`2050` | none |

  Every other year column has no blanks. These blanks are the silver rows with a null `value`:
  1,386 in 2023, 1,233 in 2024, 945 in 2025 and 882 in 2026. In the 2023 and 2025 files all the
  nulls fall in one of the five scenario or pathway groups. In the 2026 file the single scenario
  is populated through 2036 and blank from 2037; the vendor does not say why. A blank in one
  edition says nothing about another edition.
- The whole-cell tokens `-`, `N/A`, `NA`, `n/a`, `#N/A`, `NULL`, `null` and `NaN` occur **zero
  times** in every column of every captured body. There are no text sentinels in the value cells.
- **Zeros are values.** Numeric zeros occur in every edition. No primary source identifies them
  as sentinels. They stay as `0.0`. Do not treat zero as missing.
- Every non-blank cell casts strictly to float64, with zero failures in all four resources. The
  values are plain decimals. This differs from FLX1 2023, which is held for padded numbers
  (@fes-flexibility-data-table-data-table-flx1.md).

**Identity and selection.** The entity key is `resource_id`, `edition`, `data_item`, `unit`,
`scenario`, `fuel`, `peak_annual_minimum`, `pathway` and `projection_year`. This is a
**measured guard key**: every complete body passed it with zero duplicated long rows, and no
measure belongs in it (FACTS K7). No vendor text declares it as the identity of a row.
`TODO: verify` the vendor's own uniqueness rule. Because `scenario` and `pathway` are both in the
key, one is always null per row. `_latest` is `whole_capture` per `resource_id`: a newer capture
of a resource replaces that resource's previous capture as a whole. It never replaces another
edition. No revision rule between captures of one resource is claimed.

**Activation (2026-10-14, master `209adb9`, PR #123).** Transformed with window 2026-10-08, one
capture per resource and no prior silver: **31,059 rows**, equal to the planned count and with
0 failures. The whole SCN-2a batch transformed 110,515 rows (ES2 67,968, FLX1 11,382,
ED5 31,059, ED6 106). Reconcile `--all --cutoff 2026-10-13` exited 0 over 243 families with 0
gaps, and coverage was clean (gridflow `@.planning/v0.22-RESULTS.md` §SCN-2a; RULINGS 825 and
827).

Silver columns beyond the vendor columns: `edition`, `resource_id`, `timestamp_utc`,
`published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`,
`source_run_id`, `dataset_version` (all timestamps tz-aware UTC; `dataset_version` is `1+e1`
on every row of every edition: the registry record version (1) plus the silver engine version
(`e1`). It does not identify the schema epoch). The four schema epochs listed above are
numbered 1 to 4 in edition order on this page only; no silver column carries an epoch number.

The silver files sit under `C:\gridflow-data\silver\neso_data_portal\fes_ed5_road_transport\`, in
`year=2026\month=10\`, one Parquet file per capture.

### ED6, the codebook for this table

ED6 (@fes-road-transport-notes-data-table-ed6.md) is the vendor's codebook for this table. Its
`column_name` and `category` columns name an ED5 column and one of its values, and its
`description` explains it. Join ED6 to ED5 on the **same `edition`**: ED6 carries its own `edition`, and its notes differ by
edition (its row counts differ). Use it to resolve what a `data_item`, `fuel` or `peak_annual_minimum` value means. ED6
is an eligible reference family with 106 rows (27, 27, 26 and 26 by edition). Its descriptions
carry the vendor text about how ED5's peak items are timed (see Holds).

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc
- Edition-driven: the package holds one resource per edition. The 2026 resource has a CKAN
  `last_modified` of `2026-09-16T14:30:16.337617`. The 2023 and 2024 resources were last
  modified on 2025-07-01 and the 2025 resource on 2025-12-10. `TODO: verify` when NESO adds the next
  edition's resource.
- `TODO: verify` whether NESO revises a published edition in place. The version part of the
  captured file names (`v002`, `v003`, `v006`, `v001`) is the only hint, and it is a file-name
  observation, not a vendor statement.
- Captures to date: one per resource (2026-10-08). No scheduled refresh has run yet, so no
  revision behaviour has been observed.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `fes_ed5_road_transport`: held: TODO: For each ED5 annual-energy, vehicle-count and capacity item, what interval or observation date does the year label denote? For winter-peak items, does the integer label identify the starting or ending winter year? What does a blank projection cell mean? (unit E-SEM)

The family is held by the SCN-2 batch records (RULINGS 821 and 822, with the activation in 825 and
827). No gold view or model feed is planned for it while the hold stands. Under ruling 66 the site
page shows its rows with the caveat "NESO states no period or date for the year labels, or what
blanks mean."; its chart draws one FES 2025 peak item at NESO's year labels, without reading them as
dates. Unit E-SEM must answer three things before the hold can lift:

1. **The period behind each year label.** What interval or observation date the integer
   denotes, separately for the annual-energy items, the vehicle-count items and the capacity
   items. For example, is a `TWh` item a calendar year, a financial year or a winter, and is a
   `# Cars` count taken at the start, the end or the middle of the year?
2. **The winter-peak convention.** Whether the integer on a peak item names the winter's
   starting year or its ending year.
3. **What a blank cell means.** The vendor does not say whether it is unmodelled, unavailable,
   inapplicable or something else.

What the vendor text does establish, and what it does not (FACTS §6 and g1):

- The [ED5 dictionary](https://www.neso.energy/data-portal/fes-road-transport-summary-data-table-ed5/road_transport_summary_ed5_2025)
  describes the item, unit, pathway, fuel and peak/annual category columns. Its year description
  calls the year columns the year of the data item. That does not settle the period boundary.
- The same-edition ED6 notes say peak demand and capacity apply at the **transmission-system
  peak**. The earlier notes describe the **winter peak** explicitly. The later notes describe the
  peak timing and the annual categories for vehicle demand, counts and capacity. Neither says which
  winter an integer year names, and neither gives the date of a vehicle-stock count.
- No other SCN-2 family's year convention transfers to this one. ED4 settles the gas-year start
  label for its own peak gas item only, and ES2 has its own notes (FACTS g1).

Until the hold lifts:

- Do not join ED5 to an observed series by `projection_year`, or read a label as a dated period.
- Do not use ED5 point-in-time. Its only clock is the CKAN `last_modified` vintage (the
  per-resource `last_modified` in the file table), which is a conservative proxy and nothing finer.
- Do not sum across editions, across units or across `scenario` and `pathway`.

Related holds in the same batch (gridflow `@docs/neso_data_portal/eligibility.md`): ES2
(@fes-european-electricity-supply-data-table-es2.md) and FLX1
(@fes-flexibility-data-table-data-table-flx1.md) are held on the same kind of year-period and
blank-cell question, along with the 2026 ES2 notes resource and the 2023 FLX1 resource, which
are resource holds. ED6 (@fes-road-transport-notes-data-table-ed6.md) is eligible. All are unit
E-SEM, except ED6, which has no hold.
