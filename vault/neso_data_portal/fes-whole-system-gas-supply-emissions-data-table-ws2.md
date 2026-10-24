---
source: "neso_data_portal"
package: "fes-whole-system-gas-supply-emissions-data-table-ws2"
dataset_key: "fes_ws2_gas_emissions"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: FES whole system emissions
  summary: >-
    NESO's Future Energy Scenarios (FES) table of GB emissions from whole system and gas supply, by
    sector, one file per edition.
  facts:
    vendor: "NESO Data Portal: four CSVs, one per edition, 2023 to 2026"
    cadence: "Ad hoc (NESO); editions 2023 to 2026, as at 6 October 2026"
    grain: "One value per sector, scenario or pathway and year label; 2026 adds a category"
    history: "NESO created the package on 7 July 2023"
  landscape: gas
  what_it_is: >-
    Each row is an emissions sector under one scenario or pathway, with a column per year from 2021
    to 2050. There is no unit column. NESO's dictionaries, as read in October 2026, give `MTCO2e`
    for 2025 and `N/A` for 2023 and 2024. The 2026 file, a Ten-Year Outlook output last modified
    September 2026, adds two category labels that read `MtCO2e`.
  how_used:
    - "GB emissions by sector under each FES scenario or pathway"
    - "Read beside WS1, the gas supply table these emissions accompany"
  chart:
    type: bar
    silver: neso_data_portal/fes_ws2_gas_emissions
    value: value
    filter:
      - {column: edition, op: eq, value: 2025}
      - {column: pathway, op: eq, value: Holistic Transition}
      - {column: sector, op: eq, value: Electricity without BECCS}
      - {column: projection_year, op: in, value: [2025, 2030, 2035, 2040, 2045, 2050]}
    dedup: {"on": [resource_id, edition, scenario, pathway, category, sector, projection_year], order_by: capture_written_at}
    group: projection_year
    aggregation: sum
    sort: label
    unit: MTCO2e
  chart_view:
    title: Power emissions, FES 2025, Holistic Transition
    caption: >-
      Silver `fes_ws2_gas_emissions`, FES 2025 (NESO's file of 10 December 2025), pathway Holistic
      Transition: sector `Electricity without BECCS`, one row per bar, every fifth year label. Unit
      `MTCO2e` from NESO's 2025 dictionary, the one edition that states it. A projection.
    alt: >-
      Horizontal bar chart of NESO's projected emissions from the sector Electricity without BECCS,
      in MTCO2e, FES 2025 edition, pathway Holistic Transition, one bar every fifth year label:
      2025 12.8; 2030 6.81; 2035 2.75; 2040 1.18; 2045 1.08; 2050 0.91. Most of the fall comes
      by 2035.
    key:
      - {series: value, label: Power emissions, codes: Electricity without BECCS, paint: petrol, note: "NESO's sector name; its BECCS power sector is a separate row"}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then four CSVs, each downloaded whole unless its
      `last_modified` is unchanged. Shown: 2023, 2025 and 2026; edition comes from the file name.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=fes-whole-system-gas-supply-emissions-data-table-ws2"
      - "GET https://api.neso.energy/dataset/cd6e42b0-13de-4f2a-bd0d-08e31bdde67f/resource/5f8f7293-4894-40c5-8f5c-e096b19e8198/download/fes2023_ws2_v001.csv"
      - "GET https://api.neso.energy/dataset/cd6e42b0-13de-4f2a-bd0d-08e31bdde67f/resource/a80a94cc-b349-412c-83a0-0f5f9eaf4e7e/download/fes2025_ws2_v006.csv"
      - "GET https://api.neso.energy/dataset/cd6e42b0-13de-4f2a-bd0d-08e31bdde67f/resource/3aba22fd-1934-4654-a33a-f3273c973560/download/10yo2026_ws2_v001.csv"
    commands:
      - {run: gridflow ingest neso_data_portal fes_ws2_gas_emissions --last 24h, comment: "changed files only; whole CSVs"}
      - {run: gridflow transform neso_data_portal fes_ws2_gas_emissions --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: edition, op: eq, value: 2025}
        - {column: pathway, op: eq, value: Holistic Transition}
        - {column: projection_year, op: eq, value: 2030}
        - {column: sector, op: in, value: [Electricity without BECCS, Power Sector BECCS, Road Transport and Rail, Residential Heat, Industrial Heat, LULUCF N, LULUCF P, DACCS]}
      dedup: {"on": [resource_id, edition, scenario, pathway, category, sector, projection_year], order_by: capture_written_at}
      order_by: [sector]
      columns: [sector, pathway, projection_year, value, category, scenario, edition, resource_id,
                published_at, timestamp_utc]
    key: [resource_id, edition, scenario, pathway, category, sector, projection_year]
    caption: "Eight FES 2025 Holistic Transition sectors at year label 2030, two of them negative."
    fields:
      sector: "NESO's emissions sector; sets differ by edition, and NESO gives no totals rule"
      pathway: "NESO's pathway name in the 2024 and 2025 files; null in the others"
      projection_year: "NESO's year column header, as an integer; NESO states no period for it"
      value: "The cell; `MTCO2e` per NESO's 2025 dictionary; sign convention not stated"
      category: "2026 file only: `Emissions (MtCO2e)` or `Carbon Captured (MtCO2e)`"
      scenario: "NESO's scenario name in the 2023 and 2026 files; null in these rows"
      edition: "FES edition, from the file name; 2026 is NESO's Ten-Year Outlook"
      resource_id: "CKAN file id, one per edition; first column of the entity key"
      published_at: "NESO's last-modified time for the edition's file, read as UTC"
      timestamp_utc: "When gridflow captured the file, UTC; the table has no event time"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  caveat: "NESO gives no year-label period or blank meaning; only 2025's dictionary states a unit."
  notebook:
    lead: >-
      `query()` filters on `timestamp_utc`, the capture time here, so these cells use `data.sql()`
      on the `_latest` view, which keeps every edition's file, and pick FES 2025, whose dictionary
      gives the unit.
    cells:
      - |
        power = data.sql("""
            SELECT pathway, projection_year, value AS mtco2e
            FROM silver_neso_data_portal_fes_ws2_gas_emissions_latest
            WHERE edition = 2025 AND sector = 'Electricity without BECCS'
        """)
        wide = power.pivot(index="projection_year", columns="pathway", values="mtco2e").rename_axis(index=None, columns=None)
        wide.loc[[2025, 2030, 2035, 2036, 2040, 2045, 2050]].round(2)
      - |
        ax = wide.loc[2025:].plot(figsize=(8, 3.5), xlabel="NESO's year label",
                                 ylabel="MTCO2e, NESO's 2025 dictionary");
      - |
        data.sql("""
            SELECT edition, category, COUNT(*) AS cells, COUNT(DISTINCT sector) AS sectors
            FROM silver_neso_data_portal_fes_ws2_gas_emissions_latest
            GROUP BY edition, category
            ORDER BY edition, category
        """)
    needs: NESO's four FES whole system emissions files
    plot_alt: >-
      Line plot of NESO's projected emissions from Electricity without BECCS in MTCO2e, FES 2025
      edition, year labels 2025 to 2050, one line per pathway. Holistic Transition falls from 12.8 to
      0.91; Falling Behind peaks at 24.13 at label 2030 and ends at 16.3. Ten Year Forecast stops at
      label 2035.
  related:
    - {dataset: neso_data_portal/fes-whole-system-gas-supply-data-table-ws1, note: "NESO's FES whole system and gas supply table, its companion"}
    - {dataset: neso_data_portal/fes-natural-gas-residential-and-non-domestic-i-c-heat-demand-summary-data-table-ed3, note: "NESO's FES gas and heat demand tables, from the same editions"}
    - {dataset: neso_data_portal/fes-road-transport-summary-data-table-ed5, note: "NESO's FES road transport table, from the same editions"}
---

# FES: Pathways to Net Zero – Whole System & Gas Supply - Emissions Data table (WS2)

NESO's whole-system emissions table from the Future Energy Scenarios (FES) data workbook, which
the package description calls "the GB FES values for emissions from whole system and gas supply".
It is one wide table per edition. Each row is an emissions **sector** (for example `Road
Transport and Rail`, `Residential Heat` or `DACCS`) under one scenario or pathway, with one
column per projection year from 2021 to 2050. The 2026 edition adds a `Category` column. Once the
hold below lifts it is a candidate scenario input for GB emissions trajectories and for carbon
constraints in energy-system models. It is the emissions companion to the gas-supply table
(@fes-whole-system-gas-supply-data-table-ws1.md) and sits beside the other FES tables
(@fes-road-transport-summary-data-table-ed5.md,
@fes-electricity-demand-summary-data-table-ed1.md).

The package has four resources, one per edition: 2023, 2024, 2025 and 2026. The 2026 resource has
the filename prefix `10yo2026`, and its CKAN description calls it an output of the **Ten-Year
Outlook**, not of the FES (the 2023–2025 descriptions say FES). The batch spec treats the 2026
tables as the Ten Year Outlook (gridflow `@.planning/phases/v0.22-K-SCN-3/K-SCN-3-SPEC.md`).
`TODO: verify` how NESO scopes the 2026 outlook against the 2023–2025 FES editions before
comparing the editions column for column.

**The silver output of this family is held in gridflow (unit E-SEM).** This note gives its schema,
row counts and structure. Under ruling 66 the site page shows its rows (a chart and eight sample
rows from the 2025 edition, whose dictionary states the unit, and a notebook) with one caveat line
naming the open question. The unit of the year columns in three of the four editions, the period a
year label denotes and the meaning of a blank cell are not established (see Holds). The package-level `eligibility: eligible` in the
front matter is the package registry entry. The hold is per family.

Reading rules for anyone who does open the silver:

- **Edition is a dimension.** The four resources are four separately published tables. Never sum
  or average across `edition`. The 2023, 2024, 2025 and 2026 rows for the same sector and the
  same year are four different forecasts, not four observations.
- **`scenario` and `pathway` are two separate columns.** The 2023 and 2026 files head the column
  `Scenario`. The 2024 and 2025 files head it `Pathway`. Each silver row has at most one of the
  two populated and the other null. gridflow does not merge them. `TODO: verify` whether NESO
  treats the two headings as the same concept. Never sum or average across scenarios or
  pathways.
- **Some scenario or pathway labels are not scenarios.** The 2023 and 2024 files carry a
  `Five Year Forecast` label, the 2025 file a `Ten Year Forecast` label and the 2026 file a single
  `Ten Year Outlook` label, alongside the named scenarios and pathways. `TODO: verify` what each
  of these labels means and how it relates to the named scenarios before comparing them.
- **Do not sum across `sector` or `category`.** The vendor does not say which sectors are
  components of another or how the 2026 `category` values relate (see Known issues). A sum over
  sectors is not established as a whole-system total.
- **`projection_year` is a label.** It is the integer column header. The period it denotes is
  undocumented (see Holds).
- **A null `value` is a blank vendor cell**, with an undocumented meaning. A `0` is a value.
- **The `value` column has no established unit** except in the 2025 edition (see Units).

- Publisher group: FES: Pathways to Net Zero
- Registry group: future-energy-scenarios · archetype: SCN
- Vendor tags: Emissions, FES, FES2023, Forecast, Subscribable

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Whole System & Gas Supply - Emissions (WS2) 2023 | CSV | upload | `5f8f7293-4894-40c5-8f5c-e096b19e8198` |
| Whole System & Gas Supply - Emissions (WS2) 2024 | CSV | upload | `31188b9d-620d-497b-80c0-83fa4fa70320` |
| Whole System & Gas Supply - Emissions (WS2) 2025 | CSV | upload | `a80a94cc-b349-412c-83a0-0f5f9eaf4e7e` |
| Whole System & Gas Supply - Emissions (WS2) 2026 | CSV | upload | `3aba22fd-1934-4654-a33a-f3273c973560` |

All four are `SILVER` and feed the one family `fes_ws2_gas_emissions`. There is no `DOC`
resource and no resource-level hold in the package: every resource was captured and transformed
(the family-level hold below applies to all four). The files, as captured on 2026-10-08:

| Edition | Download | Bytes | Wide data rows | CKAN `last_modified` (offset-less, read as UTC) |
|---|---|---:|---:|---|
| 2023 | [fes2023_ws2_v001.csv](https://api.neso.energy/dataset/cd6e42b0-13de-4f2a-bd0d-08e31bdde67f/resource/5f8f7293-4894-40c5-8f5c-e096b19e8198/download/fes2023_ws2_v001.csv) | 17,121 | 91 | `2023-07-10T03:31:44.136572` |
| 2024 | [fes2024_ws2_v002.csv](https://api.neso.energy/dataset/cd6e42b0-13de-4f2a-bd0d-08e31bdde67f/resource/31188b9d-620d-497b-80c0-83fa4fa70320/download/fes2024_ws2_v002.csv) | 28,559 | 91 | `2024-07-16T11:16:11.122722` |
| 2025 | [fes2025_ws2_v006.csv](https://api.neso.energy/dataset/cd6e42b0-13de-4f2a-bd0d-08e31bdde67f/resource/a80a94cc-b349-412c-83a0-0f5f9eaf4e7e/download/fes2025_ws2_v006.csv) | 26,962 | 106 | `2025-12-10T16:59:01.412328` |
| 2026 | [10yo2026_ws2_v001.csv](https://api.neso.energy/dataset/cd6e42b0-13de-4f2a-bd0d-08e31bdde67f/resource/3aba22fd-1934-4654-a33a-f3273c973560/download/10yo2026_ws2_v001.csv) | 3,255 | 18 | `2026-09-16T14:51:40.910171` |

The stable handle for a resource is its id, not the file name. Every body decodes as strict
UTF-8 with CRLF line endings, with no preamble, no unnamed trailing column, no ragged row and no
blank row. The 2024 file starts with a byte-order mark, which the reader handles (profile and
gridflow `@.planning/phases/v0.22-K-SCN-3/K-SCN-3-FACTS.md` g6). The file name, the resource name
and the captured edition agree for every resource. gridflow reads the edition from the exact file
name and never infers it from the projection years, the CKAN timestamps or the capture date. The
`vNNN` part of the file names (`v001`, `v002`, `v006`, `v001`) differs by edition and is a
file-name observation, not a vendor statement.

The 2026 resource is a fraction of the size of the others because it has 18 data rows against 91
to 106. The CKAN datastore view of the 2026 resource (field-info probe, 2026-10-08) types the
year columns `2021`–`2036` as numeric and `2037`–`2050` as text, and its dictionary fields carry
no unit. gridflow reads the CSV body, not the datastore, so the typing does not touch silver. It
is consistent with the entirely blank `2037`–`2050` columns of that body (see Sentinels).

## Families

### `fes_ws2_gas_emissions`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Scenario | `scenario` | string | — | yes | — | — |
| Sector | `sector` | string | — | no | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 1: `2021` → 2021, `2022` → 2022, `2023` → 2023, `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Pathway | `pathway` | string | — | yes | — | — |
| Sector | `sector` | string | — | no | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 2: `2021` → 2021, `2022` → 2022, `2023` → 2023, `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

Schema, epoch 3:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Scenario | `scenario` | string | — | yes | — | — |
| Category | `category` | string | — | yes | — | — |
| Sector | `sector` | string | — | no | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 3: `2021` → 2021, `2022` → 2022, `2023` → 2023, `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

- Entity key: `resource_id`, `edition`, `scenario`, `pathway`, `category`, `sector`, `projection_year`
- Latest: `whole_capture` per `resource_id`
- Edition: `fes2023_ws2_v001.csv` → 2023; `fes2024_ws2_v002.csv` → 2024; `fes2025_ws2_v006.csv` → 2025; `10yo2026_ws2_v001.csv` → 2026
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

The three schema epochs are numbered 1 to 3 in order of first appearance on this page only. They
map to editions as follows, and no silver column carries an epoch number:

| Epoch | Editions | Header |
|---|---|---|
| 1 | 2023 | `Scenario`, `Sector`, then `2021`–`2050` |
| 2 | 2024 and 2025 | `Pathway`, `Sector`, then `2021`–`2050` |
| 3 | 2026 | `Scenario`, `Category`, `Sector`, then `2021`–`2050` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured resource, read as UTC per ADR-030 (gridflow
   `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). There is one vintage per
   resource, and every row of an edition shares it (dates in the file table above). Checked on
   every silver row on 2026-10-15: `available_at` equals `published_at`. The vintage says when
   the file last changed on the portal. It does not say when NESO first published the edition.
   The 2023 and 2024 vintages are a year apart (July 2023 and July 2024), the 2025 vintage is
   December 2025 and the 2026 vintage is September 2026. `TODO: verify` with the vendor whether
   any of them is the original publication date of the matching workbook. The only point-in-time
   key the table supports is this vintage, a conservative proxy and nothing finer.
2. **Event time (temporal recipe `none`).** The record declares no event-time recipe, because the
   year labels have no established period (see Holds). `timestamp_utc` is therefore the **capture
   time**, not a modelled time. `event_time` and `capture_written_at` carry the same instant
   (checked on every silver row). All rows of an edition share one `timestamp_utc`, and the four
   editions' captures ran within about seven seconds of each other on 2026-10-08. Do not use
   `timestamp_utc` as a forecast horizon or a model time axis. The only year information is
   `projection_year`, a label.

Rows per edition and resource (silver, from the 2026-10-08 transform):

| Edition | Resource id | Wide rows × year columns | Silver rows | Projection-year labels |
|---|---|---|---:|---|
| 2023 | `5f8f7293-4894-40c5-8f5c-e096b19e8198` | 91 × 30 | 2,730 | 2021–2050 |
| 2024 | `31188b9d-620d-497b-80c0-83fa4fa70320` | 91 × 30 | 2,730 | 2021–2050 |
| 2025 | `a80a94cc-b349-412c-83a0-0f5f9eaf4e7e` | 106 × 30 | 3,180 | 2021–2050 |
| 2026 | `3aba22fd-1934-4654-a33a-f3273c973560` | 18 × 30 | 540 | 2021–2050 |
| | | | **9,180** | |

Distinct dimension values per edition (counts only):

| Edition | `sector` | `scenario` | `pathway` | `category` |
|---|---:|---:|---:|---:|
| 2023 | 20 | 5 | none | none |
| 2024 | 20 | none | 5 | none |
| 2025 | 23 | none | 5 | none |
| 2026 | 14 | 1 | none | 2 |

The sector sets differ between editions (20, 20, 23 and 14 labels), so a row present in one
edition has no guaranteed counterpart in another. The tables are not rectangular grids of sector
by scenario: the row counts do not equal sectors times scenarios. gridflow keeps the rows the
vendor published. `TODO: verify` the vendor's definition of each scenario, pathway, sector and
category label, and whether a label in one edition is the same concept as a label in another.

**Units (vendor dictionary; no unit column).** The table has no `Unit` column, and silver adds
none. The unit of the year columns comes only from the resource's data dictionary:

| Edition | Dictionary unit for the year fields | Status |
|---|---|---|
| 2023 | `N/A` | Not an emissions unit. `TODO: verify` the actual unit. |
| 2024 | `N/A` | Not an emissions unit. `TODO: verify` the actual unit. |
| 2025 | `MTCO2e` | Stated by the vendor for this edition. The label is kept as the vendor spells it. |
| 2026 | none (captured field info has no units; live dictionary unit fields are blank) | `TODO: verify` the actual unit. |

- Only the 2025 edition has a stated unit, so only 2025 can be read with one. That statement is
  vendor text in the dictionary and is docs-only: it is not a silver column, and gridflow does
  not convert, scale or relabel any `value` (RULINGS 707; K-SCN-3 spec ruling 11).
- The 2025 FES report also labels its whole-system emissions charts `MtCO2e`, which corroborates
  that edition. It does not establish the unit of any other resource (FACTS W4).
- The 2026 `category` labels (two of them) carry the text `MtCO2e` inside the label string
  itself. That is label text inside a data column, not a dictionary unit declaration, and
  gridflow does not adopt it as the 2026 unit. `TODO: verify` with the vendor whether it is
  their unit statement for the 2026 values, and what each of the two categories measures (for
  example emissions against captured carbon) and in which sign convention.
- No unit is inferred from the column names, the magnitudes or another edition. Do not read the
  2023, 2024 or 2026 values as `MTCO2e` until the vendor says so.
- The vendor dictionaries' year-field description does not say whether a year label is a calendar
  year, a financial year or something else, nor whether it labels the start or the end of the
  period. That is part of the hold.

**Sentinels and missing values (FACTS g5).** The record declares no null token.

- **Blank cells** are kept as **null** `value`. They are not dropped and not filled.
- The vendor does not say what a blank means. Unmodelled, unavailable, inapplicable and not yet
  published are all possible, and their position or frequency does not settle it.
  `TODO: verify` (part of the hold).
- The blanks sit at the far end of the horizon, and in two editions also at the near end. The
  CSV bodies have these blank year columns:

  | Edition | Year columns with blank cells | Blank cells per column | Silver rows with null `value` |
  |---|---|---|---:|
  | 2023 | `2029`–`2050` | 17 each | 374 |
  | 2024 | `2030`–`2050` | 17 each | 357 |
  | 2025 | `2021`–`2023` | 5 each | |
  | 2025 | `2036`–`2050` | 20 each | 315 |
  | 2026 | `2021`–`2024` | 1 each | |
  | 2026 | `2037`–`2050` | 18 each (entirely blank) | 256 |

  Every other year column has no blanks. The 2026 columns `2037`–`2050` are blank in all 18 rows.
  In the 2023 and 2024 files 17 of the 91 rows are blank in each of those columns; the vendor
  does not say why. No identifier cell is blank in any edition:
  `sector` has no nulls, and `scenario`, `pathway` and `category` are null only where the
  edition's header does not carry that column.
- The whole-cell tokens `-`, `N/A`, `NA`, `n/a` and `#N/A` occur **zero times** in the value
  cells of all four bodies. There are no text sentinels in the projection columns. (The dictionary
  uses the string `N/A` as the unit of the 2023 and 2024 year fields. That is a unit statement,
  not a cell value.)
- **Zeros are values.** Numeric zeros occur in every edition and no primary source identifies
  them as sentinels. They stay as `0.0`. Do not treat zero as missing, and do not treat a blank
  as zero.
- Every non-blank cell casts strictly to float64, with zero failures in all four resources, so no
  resource-level treatment is needed. This differs from WS1, whose 2024 resource carries a literal
  `N/A` and is held at resource level (@fes-whole-system-gas-supply-data-table-ws1.md).

**Identity and selection.** The entity key is `resource_id`, `edition`, `scenario`, `pathway`,
`category`, `sector` and `projection_year`. This is a **measured guard key**: every complete body
passed it with zero duplicated long rows, and no measure belongs in it (FACTS K4). It differs from
the `(category, sector)` key that the profiler suggests, which comes from the 2026 shape only and
is not a cross-edition identity. No vendor text declares the key as the identity of a row.
`TODO: verify` the vendor's own uniqueness rule. Because `scenario`, `pathway` and `category` are
all in the key, at least one is always null per row. `_latest` is `whole_capture` per
`resource_id`: a newer capture of a resource replaces that resource's previous capture as a
whole. It never replaces another edition. No revision rule between captures of one resource is
claimed.

**Activation (2026-10-15, master `06378b9`, PR #125).** Transformed with window 2026-10-08, one
capture per resource and no prior silver: **9,180 rows** (2,730, 2,730, 3,180 and 540), equal to
the planned count and with 0 failures. The whole SCN-3 batch transformed 59,388 rows. Reconcile
`--all --cutoff 2026-10-13` exited 0 over 255 families with 0 gaps, and coverage was clean
(gridflow `@.planning/v0.22-RESULTS.md` §SCN-3; RULINGS 842 and 844).

Silver columns beyond the vendor columns: `edition`, `resource_id`, `timestamp_utc`,
`published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`,
`source_run_id`, `dataset_version` (all timestamps tz-aware UTC; `dataset_version` is `1+e1` on
every row of every edition: the registry record version (1) plus the silver engine version
(`e1`). It does not identify the schema epoch). The silver schema carries all three of
`scenario`, `pathway` and `category`, null where the edition's header has no such column.

The silver files sit under `C:\gridflow-data\silver\neso_data_portal\fes_ws2_gas_emissions\`, in
`year=2026\month=10\`, one Parquet file per capture (four files). The bronze captures sit under
`C:\gridflow-data\bronze\neso_data_portal\fes_ws2_gas_emissions\2026\10\08\`, as the raw CSV and
a `.meta.json` per resource with the download URL, the CKAN `last_modified` and the body SHA-256.

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc
- Edition-driven: the package holds one resource per edition. The 2026 resource has a CKAN
  `last_modified` of `2026-09-16T14:51:40.910171`. The 2023, 2024 and 2025 resources were last
  modified on 2023-07-10, 2024-07-16 and 2025-12-10. `TODO: verify` when NESO adds the next
  edition's resource.
- `TODO: verify` whether NESO revises a published edition in place. The version part of the
  captured file names is the only hint, and it is a file-name observation, not a vendor
  statement.
- Captures to date: one per resource (2026-10-08). No scheduled refresh has run yet, so no
  revision behaviour has been observed.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `fes_ws2_gas_emissions`: held: TODO: What emissions unit do the 2023, 2024 and 2026 WS2 year columns carry (their dictionaries give `N/A` or no unit; only 2025 states `MTCO2e`)? For each edition, is a year label a calendar or financial year, and a starting or ending label? What does a blank projection cell mean? (unit E-SEM)

The family is held by the SCN-3 batch record (spec ruling 7, ratified in RULINGS 839; activation in
RULINGS 844). No gold view or model feed is planned for it while the hold stands. Under ruling 66
the site page shows its rows with the caveat "NESO gives no year-label period or blank meaning;
only 2025's dictionary states a unit."; its chart and frame use only the 2025 edition, the one whose
dictionary gives a unit, and its chart draws one sector at NESO's year labels, nothing summed.
Unit E-SEM must answer three things before the hold can lift:

1. **The unit of the 2023, 2024 and 2026 values.** The dictionaries give `N/A` (2023, 2024) or no
   unit (2026). Only the 2025 dictionary states `MTCO2e`.
2. **The period behind each year label.** Whether it is a calendar or a financial year, and
   whether the integer labels the start or the end of the period, separately for each edition.
3. **What a blank cell means.** The vendor does not say whether it is unmodelled, unavailable,
   inapplicable or something else, including the blanks at the near end of the 2025 and 2026
   horizons.

What the vendor text does establish, and what it does not (FACTS §3.2, g1 and g4):

- The edition dictionaries ([2023](https://www.neso.energy/data-portal/fes-whole-system-gas-supply-emissions-data-table-ws2/whole_system__gas_supply_-_emissions_ws2_2023),
  [2024](https://www.neso.energy/data-portal/fes-whole-system-gas-supply-emissions-data-table-ws2/whole_system__gas_supply_-_emissions_ws2_2024),
  [2025](https://www.neso.energy/data-portal/fes-whole-system-gas-supply-emissions-data-table-ws2/whole_system__gas_supply_-_emissions_ws2_2025),
  [2026](https://www.neso.energy/data-portal/fes-whole-system-gas-supply-emissions-data-table-ws2/whole_system__gas_supply_-_emissions_ws2_2026))
  describe the year fields generically. They do not settle the period boundary.
- The 2025 dictionary and the FES 2025 report agree on `MTCO2e` and `MtCO2e` for that edition
  only.
- The FES workbook notes that might settle the year convention could not be read in the research
  pass (the browser download returned an unsupported-format error). `TODO: verify` against the
  matching-edition workbook notes or an explicit NESO clarification. Do not substitute numerical
  inference.
- No other family's year convention transfers to this one. WS1 is held on a similar question and
  is a separate table with its own units per row.

Until the hold lifts:

- Do not join WS2 to an observed emissions series by `projection_year`, or read a label as a dated
  period.
- Do not use WS2 point-in-time. Its only clock is the CKAN `last_modified` vintage.
- Do not sum across editions, across `scenario` and `pathway`, across `sector` or `category`, or
  across WS1 units (WS1 is a separate table with a unit on every row; the two tables are not
  reconciled).
- Do not assign `MTCO2e` to any edition other than 2025.

Related holds in the same batch (gridflow `@docs/neso_data_portal/eligibility.md`): WS1
(@fes-whole-system-gas-supply-data-table-ws1.md) is held on the year-period and blank-cell
question, with a resource hold on its 2024 resource and a failed capture for its 2025 resource.
The other SCN-3 families (the heat-model output profile, the two local-authority tables) are
held on their own E-SEM questions, and the three Resource Adequacy tables are eligible. LCOH
stays held (RULINGS 477) and is not part of this package.

## Known issues and gotchas

- **Three header epochs, one family.** `Scenario` (2023), `Pathway` (2024, 2025) and `Scenario`
  plus `Category` (2026). Silver carries all three columns, null where absent. Filter on
  `edition` before reading any of them.
- **Sector labels are not stable across editions.** Spellings differ (for example the biofuel
  BECCS sector is named differently in 2025 than in 2023 and 2024), the sector sets differ in
  size (20, 20, 23, 14), and some labels have a trailing space which gridflow keeps as-is (the
  `Carbon offset from Biomethane ` label in 2025 and 2026). Do not match sectors across
  editions by string without checking.
- **Overlapping sector labels.** Some labels read as possible aggregates or overlaps of others
  (for example `Agriculture` beside `Agriculture and LULUCF`, `LULUCF N` and `LULUCF P`; in 2026
  `Energy from Waste` beside `Energy from Waste CCS`). The vendor does not say whether any sector
  is a subtotal of others, whether sectors are additive, or whether a sector value can be
  negative. `TODO: verify`. Do not build a total by summing sectors.
- **2026 has a `Category` dimension with two values.** Their label text names the quantity
  (see Units). Whether a value under one category is meant to be netted against the other is not
  stated. `TODO: verify`.
- **The 2026 resource is the Ten Year Outlook,** with one scenario label and 14 sectors, not an
  FES edition. It must not be treated as a drop-in fourth FES edition (see the overview).
- **Blank tails differ by edition and are not comparable** (22, 21, 18 and 18 blank year columns
  in 2023, 2024, 2025 and 2026). The 2025 file also has blanks at the near end (2021–2023) and the
  2026 file too (2021–2024), which is part of the blank-cell question. Do not forward-fill,
  back-fill or interpolate across them.
- **The 2024 file has a byte-order mark.** The gridflow reader handles it (FACTS g6). A consumer
  that reads the raw bronze CSV directly must strip it itself.
- **Datastore typing is not the CSV typing.** The CKAN datastore view of the 2026 resource types
  `2037`–`2050` as text because they are blank. gridflow's float64 `value` comes from the CSV
  body.
- **CKAN `last_modified` is offset-less.** gridflow reads it as UTC (ADR-030). No timezone is
  stated by the vendor. `TODO: verify`.
- **A hold is not a gap.** Reconcile counts this family as complete (0 gaps). The hold is a
  consumption restriction, not a missing-data state.

## Implementation delta

- **Unit**: the vendor dictionaries give `N/A`, `MTCO2e` (2025 only) or nothing, and the silver
  record has no unit column and no unit conversion — consistent with the docs. The 2025 unit is
  recorded here only, as docs, by design.
- **Year label**: the dictionaries call the year fields the year of the data, with no calendar or
  financial-year definition, and silver stores `projection_year` as an int64 label with no
  period semantics — consistent, and the reason for the hold.
- **Event time**: the record has `temporal: none`, so `timestamp_utc` equals capture time. A
  future event-time recipe is blocked on the year-period question.
- **Entity key**: includes the nullable `scenario`, `pathway` and `category`, which the profiler
  did not (it suggested `(category, sector)` from the 2026 shape). The profiler's key is not a
  cross-edition identity.
- **Vendor uniqueness**: not declared by the vendor. The key is a measured guard, not a vendor
  guarantee.
- No other discrepancies found between the vendor text and the registry record.

## Modelling notes

Not designed. While the hold stands the family is not a feed for gridflow_models and no gold view
or model input is planned. The gaps that block any use are the unit (2023, 2024, 2026), the
period behind a year label and the blank-cell meaning. If the hold lifts:

- Treat `edition` and the scenario or pathway label as keys, never as features to average.
- Use `sector` and `category` as the grouping dimensions. Do not total across them without a
  vendor statement of how they relate.
- The only point-in-time filter available is the CKAN vintage (`available_at`).
- Related tables for a richer view: the gas-supply table (@fes-whole-system-gas-supply-data-table-ws1.md)
  and the other FES tables. Join only on the same `edition`, and only after each table's own
  year convention is settled. `TODO: verify` whether WS2 emissions are defined on the same basis
  as WS1 supply quantities.

## Links

- [Official package page](https://www.neso.energy/data-portal/fes-whole-system-gas-supply-emissions-data-table-ws2)
- [2025 dictionary](https://www.neso.energy/data-portal/fes-whole-system-gas-supply-emissions-data-table-ws2/whole_system__gas_supply_-_emissions_ws2_2025)
- [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence)
- Registry record: gridflow `@src/gridflow/connectors/neso_data_portal/registry/fes-whole-system-gas-supply-emissions-data-table-ws2.json`
- Eligibility report: gridflow `@docs/neso_data_portal/eligibility.md`
- Batch evidence: gridflow `@.planning/phases/v0.22-K-SCN-3/K-SCN-3-FACTS.md` (§3.2, §6.2, g1, g4, g5), `@.planning/phases/v0.22-K-SCN-3/K-SCN-3-SPEC.md` (§3), `@.planning/v0.22-RESULTS.md` §SCN-3
- Companion table: @fes-whole-system-gas-supply-data-table-ws1.md
- Sibling FES tables: @fes-road-transport-summary-data-table-ed5.md, @fes-electricity-demand-summary-data-table-ed1.md
