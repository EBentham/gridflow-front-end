---
source: "neso_data_portal"
package: "future-energy-scenario-electricity-supply-data-table-es1"
dataset_key: "fes_es1_electricity_supply"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: FES electricity supply
  summary: >-
    NESO's GB electricity supply table (ES1) from its Future Energy Scenarios (FES) and 2026
    Ten-Year Outlook, one file per edition.
  facts:
    vendor: "NESO Data Portal: seven CSVs, one per edition, 2020 to 2026"
    cadence: "Ad hoc (NESO); editions 2020 to 2026, as at 6 October 2026"
    grain: "One value per connection, scenario, variable, technology and year label, per edition"
    history: "NESO created the package on 3 December 2020"
  landscape: power
  what_it_is: >-
    NESO says the files cover capacity, generation and interconnector flows. Rows run by
    connection, scenario or pathway and technology. The unit sits in each row's `Variable` label, such as
    `Capacity (MW)` or `Generation (TWh)`, so one column mixes units. NESO's 2021 and 2022 files
    open with notes above the table. The package has no definitions file.
  how_used:
    - "GB capacity and generation by technology under each FES scenario or pathway"
    - "Interconnector imports, exports and net flows in each scenario or pathway"
    - "Supply beside FES demand and flexibility from the same edition"
  chart:
    type: bar
    silver: neso_data_portal/fes_es1_electricity_supply
    value: value
    filter:
      - {column: edition, op: eq, value: 2025}
      - {column: pathway, op: eq, value: Holistic Transition}
      - {column: connection, op: eq, value: Transmission}
      - {column: variable, op: eq, value: Capacity (MW)}
      - {column: sub_type, op: eq, value: Offshore Wind}
      - {column: projection_year, op: in, value: [2030, 2035, 2040, 2045, 2050]}
    dedup: {"on": [resource_id, edition, connection, pathway, variable, category, type, sub_type, projection_year], order_by: capture_written_at}
    group: projection_year
    aggregation: max
    sort: label
    unit: MW
  chart_view:
    title: Offshore wind capacity, FES 2025, Holistic Transition
    caption: >-
      Silver `fes_es1_electricity_supply`, FES 2025 edition (NESO's file last modified 10 December
      2025), pathway Holistic Transition: `Capacity (MW)` for `Transmission` `Offshore Wind`, one
      row per fifth year label, as written. NESO states no period for the labels.
    alt: >-
      Horizontal bar chart of NESO's transmission-connected offshore wind capacity in the FES 2025
      edition, pathway Holistic Transition, in MW, one bar per year label: 2030 45,723.75; 2035
      85,404.75; 2040 92,454.75; 2045 98,082.75; 2050 103,190.8. The largest step is between the
      2030 and 2035 labels.
    key:
      - {series: value, label: Offshore wind capacity, codes: Holistic Transition, paint: petrol,
         note: "NESO's year labels as written; the `Transmission` row only, not distributed or non-networked"}
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show`, then seven CSVs, downloaded whole when
      `last_modified` changes. 2023 to 2026 have rows; 2020 to 2022 carry commas, spaces or
      `N/A`. Shown: 2020, 2023, 2026.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=future-energy-scenario-electricity-supply-data-table-es1"
      - "GET https://api.neso.energy/dataset/549b0667-b533-4748-95bd-f6e13933a47d/resource/40f40b39-5eba-4479-94b1-328ea9b8eefe/download/fes_es1.csv"
      - "GET https://api.neso.energy/dataset/549b0667-b533-4748-95bd-f6e13933a47d/resource/86812136-3f52-43e5-8f7c-7e4f6d5f95fc/download/fes2023_es1_v002.csv"
      - "GET https://api.neso.energy/dataset/549b0667-b533-4748-95bd-f6e13933a47d/resource/b3bf8ac0-d27a-447c-975c-208ae92c0fa5/download/10yo2026_es1_v001.csv"
    commands:
      - {run: gridflow ingest neso_data_portal fes_es1_electricity_supply --last 24h, comment: "changed CSVs to bronze"}
      - {run: gridflow transform neso_data_portal fes_es1_electricity_supply --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: edition, op: eq, value: 2025}
        - {column: pathway, op: eq, value: Holistic Transition}
        - {column: projection_year, op: eq, value: 2035}
        - {column: connection, op: in, value: [Transmission, Both]}
        - {column: sub_type, op: in, value: [Offshore Wind, Interconnectors, Battery]}
        - {column: variable, op: in, value: [Capacity (MW), Generation (TWh), Curtailment (TWh), Netflows (TWh), Storage Capacity (GWh)]}
      dedup: {"on": [resource_id, edition, connection, pathway, variable, category, type, sub_type, projection_year], order_by: capture_written_at}
      order_by: [sub_type, variable]
      columns: [connection, variable, sub_type, projection_year, value, pathway, category, type, edition,
                resource_id, published_at, timestamp_utc]
    key: [resource_id, edition, connection, scenario, pathway, variable, category, type, sub_type, projection_year]
    caption: "FES 2025 Holistic Transition, label 2035: MW, TWh and GWh rows side by side."
    fields:
      connection: "NESO's connection label, such as `Transmission`, `Distributed` or `Both`"
      variable: "NESO's measure, with the row's unit in brackets"
      sub_type: "NESO's technology at its finest level, such as `Offshore Wind` or `Battery`"
      projection_year: "NESO's year header as an integer; its period is not stated"
      value: "NESO's value in the unit named in `variable`, sign as written; blanks stay blank"
      pathway: "NESO's pathway name in the 2024 and 2025 files; blank in 2023 and 2026"
      category: "NESO's technology group, such as `Renewable`, `Storage` or `Interconnectors`"
      type: "NESO's technology type, between category and sub-type"
      edition: "The FES edition, from the file name; 2026 is the Ten-Year Outlook"
      scenario: "NESO's scenario name in the 2023 and 2026 files; blank in 2024 and 2025"
      resource_id: "CKAN file id, one per edition; first column of the entity key"
      published_at: "NESO's last-modified time for the edition's file, read as UTC"
      timestamp_utc: "When gridflow captured the file, UTC; the table has no event time"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  caveat: "NESO states no period for the year labels, nor whether each starts or ends one."
  notebook:
    lead: >-
      `query()` filters on `timestamp_utc`, the capture time here, so these cells use `data.sql()`
      on the `_latest` view, which keeps every edition's file, and pick FES 2025 by `edition`.
    cells:
      - |
        es1 = data.sql("""
            SELECT pathway, projection_year, value
            FROM silver_neso_data_portal_fes_es1_electricity_supply_latest
            WHERE edition = 2025 AND connection = 'Transmission'
              AND variable = 'Capacity (MW)' AND sub_type = 'Offshore Wind'
        """)
        wide = es1.pivot(index="projection_year", columns="pathway", values="value").rename_axis(index=None, columns=None)
        wide.loc[[2030, 2035, 2040, 2045, 2050]]
      - |
        ax = wide.plot(figsize=(9, 3.5), color=["#155A6E", "#8A9A2B", "#B5651D", "#6E4A7E", "#5A6B70"],
                       xlabel="NESO's year label, as written", ylabel="transmission offshore wind, MW");
      - |
        data.sql("""
            SELECT variable, count(*) AS cells, count(value) AS filled
            FROM silver_neso_data_portal_fes_es1_electricity_supply_latest
            WHERE edition = 2025
            GROUP BY variable
            ORDER BY variable
        """)
    needs: NESO's four FES electricity supply files from 2023 to 2026
    plot_alt: >-
      Line plot of NESO's transmission-connected offshore wind capacity in the FES 2025 edition, MW,
      by year label 2024 to 2050, one line per pathway. All five start at 14,771.5 at label 2024.
      At 2050 Holistic Transition is highest at 103,190.8, then Electric Engagement 95,625.75,
      Hydrogen Evolution 94,942.75 and Falling Behind 79,689.75. Ten Year Forecast is blank after
      2035.
  related:
    - {dataset: neso_data_portal/fes-electricity-demand-summary-data-table-ed1, note: "NESO's FES electricity demand table, the counterpart to this supply table"}
    - {dataset: neso_data_portal/fes-european-electricity-supply-data-table-es2, note: "The European counterpart: NESO's FES supply table for European countries"}
    - {dataset: neso_data_portal/fes-flexibility-data-table-data-table-flx1, note: "NESO's FES flexibility table: storage, demand side response, interconnectors"}
    - {dataset: neso_data_portal/resource-adequacy-in-2030s, note: "NESO's separate study of GB resource adequacy in the 2030s"}
---

# FES: Pathways to Net Zero – Electricity Supply Data Table (ES1)

This package is NESO's **Future Energy Scenarios (FES)** electricity-supply data table (ES1).
The package notes say one FES output is "an agreed set of data tables containing the GB FES
values for electricity Supply". Each CSV is one **edition** of the FES (2020 to 2026; the 2026
file name starts `10yo2026`). A row is one (connection, scenario or pathway, variable, category,
type, sub-type) combination with one value per year column. The vendor `Variable` label carries
the row's unit in brackets, for example `(MW)`, `(GWh)` or `(TWh)`, so one year column mixes
units by row (see Units). The year headers are the vendor's labels. The period each label
covers (calendar, financial or winter year; start or end of it) is **not established**
(`TODO: verify`; first part of the hold question, see Holds). Some early year columns may be
historical rather than projected, and this page does not establish whether any column is outturn
or projection. Until the hold is answered, do not use the values as either outturn or a forecast.

gridflow reshapes each wide body into **long rows**: one row per (dimension tuple,
`projection_year`) with a `value`, and it stamps an `edition` from the file name (ADR-042).
Silver holds **54,359 rows from 4 resources** (2023: 17,052 · 2024: 17,192 · 2025: 16,740 ·
2026: 3,375), of which **8,117** have a blank (null) `value`. The silver output is **held**
(unit E-SEM; see Holds). **The three oldest resources (2020, 2021, 2022) are held at resource
level and have no silver at all** (see Resource detail). This note gives schema, row counts,
clocks and missingness; the site page shows the 2023 to 2026 rows, a chart of one FES 2025 row
and a notebook, with one line naming the hold question (ruling 66, 2026-10-24).

Sibling scenario packages in this vault: @./fes-electricity-demand-summary-data-table-ed1.md
(ED1, the demand counterpart, same mechanism) and @./future-energy-scenario-fes-building-block-data.md.

- Publisher group: FES: Pathways to Net Zero
- Registry group: future-energy-scenarios · archetype: SCN

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Electricity Supply Data table (ES1) 2023 | CSV | upload | `86812136-3f52-43e5-8f7c-7e4f6d5f95fc` |
| Electricity Supply Data table (ES1) 2024 | CSV | upload | `8c8a436d-408a-441b-8c7a-84249805772c` |
| Electricity Supply Data table (ES1) 2025 | CSV | upload | `6c78a777-b885-4bb6-bc35-8100f9e137a2` |
| Electricity Supply Data table (ES1) 2026 | CSV | upload | `b3bf8ac0-d27a-447c-975c-208ae92c0fa5` |

### HOLD

| Resource | Format | Capture | Id | Reason (unit) |
|---|---|---|---|---|
| Electricity Supply Data table (ES1) 2020 | CSV | upload | `40f40b39-5eba-4479-94b1-328ea9b8eefe` | the 2020 body fails the strict float64 cast on 5456 projection cells (2,645 comma-formatted thousands and 2,811 literal N/A cells of undocumented meaning) and the record has no lexical-number mechanism; re-disposition only after a declared lexical-number mechanism and a vendor meaning for N/A, or a corrected NESO upload (a new last_modified) (E-SEM) |
| Electricity Supply Data table (ES1) 2021 | CSV | upload | `bca9679e-9860-4efd-9145-220d7dc4b912` | the 2021 body opens with a title and notes preamble before its table header on physical line 10, which the CSV reader cannot skip, and every nonblank projection cell is whitespace-padded (12184 fail the strict float64 cast, 2899 of them also with thousands separators); re-disposition only after a supported header-row recipe and a lexical-number mechanism, or a corrected NESO upload (a new last_modified) (E-SEM) |
| Electricity Supply Data table (ES1) 2022 | CSV | upload | `90c4a0e8-22fd-4bda-b5bd-14a540893a98` | the 2022 body opens with a title and notes preamble before its table header on physical line 10, which the CSV reader cannot skip, and every nonblank projection cell is whitespace-padded (15545 fail the strict float64 cast, 3189 of them also with thousands separators); re-disposition only after a supported header-row recipe and a lexical-number mechanism, or a corrected NESO upload (a new last_modified) (E-SEM) |

### Resource detail

Package `future-energy-scenario-electricity-supply-data-table-es1` (CKAN id
`549b0667-b533-4748-95bd-f6e13933a47d`) has **7 resources**, all CSV, in the 2026-10-06
catalogue snapshot. There are no DOC (PDF) resources in this package: **the CSVs carry no
definitions**, and the package gives no companion definitions table (`TODO: verify` with NESO
where ES1 variable definitions are published). `last_modified` is the CKAN value in that
snapshot; download links are the snapshot's resource URLs; `size` is null in the snapshot.

| Edition | Disposition | File | CKAN `last_modified` | Download |
|---|---|---|---|---|
| 2020 | HOLD (E-SEM) | `fes_es1.csv` | 2020-12-03T11:58:42.191637 | [CSV](https://api.neso.energy/dataset/549b0667-b533-4748-95bd-f6e13933a47d/resource/40f40b39-5eba-4479-94b1-328ea9b8eefe/download/fes_es1.csv) |
| 2021 | HOLD (E-SEM) | `fes2021_es1.csv` | 2021-07-12T10:24:36.047429 | [CSV](https://api.neso.energy/dataset/549b0667-b533-4748-95bd-f6e13933a47d/resource/bca9679e-9860-4efd-9145-220d7dc4b912/download/fes2021_es1.csv) |
| 2022 | HOLD (E-SEM) | `fes2022_es1_v001.csv` | 2022-07-17T23:22:23.498433 | [CSV](https://api.neso.energy/dataset/549b0667-b533-4748-95bd-f6e13933a47d/resource/90c4a0e8-22fd-4bda-b5bd-14a540893a98/download/fes2022_es1_v001.csv) |
| 2023 | SILVER | `fes2023_es1_v002.csv` | 2023-08-24T10:35:22.143299 | [CSV](https://api.neso.energy/dataset/549b0667-b533-4748-95bd-f6e13933a47d/resource/86812136-3f52-43e5-8f7c-7e4f6d5f95fc/download/fes2023_es1_v002.csv) |
| 2024 | SILVER | `fes2024_es1_v002.csv` | 2024-08-02T11:01:29.547730 | [CSV](https://api.neso.energy/dataset/549b0667-b533-4748-95bd-f6e13933a47d/resource/8c8a436d-408a-441b-8c7a-84249805772c/download/fes2024_es1_v002.csv) |
| 2025 | SILVER | `fes2025_es1_v006.csv` | 2025-12-10T16:48:54.482473 | [CSV](https://api.neso.energy/dataset/549b0667-b533-4748-95bd-f6e13933a47d/resource/6c78a777-b885-4bb6-bc35-8100f9e137a2/download/fes2025_es1_v006.csv) |
| 2026 | SILVER | `10yo2026_es1_v001.csv` | 2026-09-16T14:27:45.949534 | [CSV](https://api.neso.energy/dataset/549b0667-b533-4748-95bd-f6e13933a47d/resource/b3bf8ac0-d27a-447c-975c-208ae92c0fa5/download/10yo2026_es1_v001.csv) |

- **The edition map is exact.** Only the four file names above (2023-2026) are in the record's
  `edition_by_filename`. An unmapped file name fails loudly rather than being guessed from the
  naming convention (the 2020 file `fes_es1.csv` and the 2026 file `10yo2026_es1_v001.csv` break
  the `fesYYYY_` pattern). The three held resources have no edition entry and are expected by no
  completion check.
- **Why 2020 is held.** Its body fails the strict float64 cast on 5,456 projection cells: 2,645
  comma-formatted numbers and 2,811 literal `N/A` cells. The vendor meaning of `N/A` is not
  documented (`TODO: verify`). The current record has no lexical-number mechanism, and gridflow
  does not strip commas or convert `N/A` on its own.
- **Why 2021 and 2022 are held.** Each body opens with a title and notes preamble; the real
  table header is on physical line 10, and the CSV reader cannot skip the preamble. The preamble
  notes say, per the FACTS read, that values may be estimated or backcast, that several variables
  share one table and that zero-valued scenario rows are omitted. The notes do not state the
  period a year label covers. Every non-blank projection cell is also whitespace-padded (12,184
  strict-cast failures in 2021, 2,899 also with thousands separators; 15,545 in 2022, 3,189
  also). Both tables also end in two entirely blank unnamed trailing columns.
- **Do not read the vintage as a sequence of one file.** File names carry version tokens
  (`v001`, `v002`, `v006`) that show NESO re-uploads within an edition under the same resource
  slot; gridflow keys the edition on the file name, not on the token.
- All seven CSVs were probed in full against the captured bronze bodies (FACTS SCN-1d); the
  held bodies are captured in bronze but never transformed.

## Families

### `fes_es1_electricity_supply`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Connection | `connection` | string | — | no | — | — |
| Scenario | `scenario` | string | — | yes | — | — |
| Variable | `variable` | string | — | no | — | — |
| Category | `category` | string | — | yes | — | — |
| Type | `type` | string | — | yes | — | — |
| SubType | `sub_type` | string | — | yes | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 1: `2022` → 2022, `2023` → 2023, `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Connection | `connection` | string | — | no | — | — |
| Pathway | `pathway` | string | — | yes | — | — |
| Variable | `variable` | string | — | no | — | — |
| Category | `category` | string | — | yes | — | — |
| Type | `type` | string | — | yes | — | — |
| SubType | `sub_type` | string | — | yes | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 2: `2023` → 2023, `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

Schema, epoch 3:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Connection | `connection` | string | — | no | — | — |
| Pathway | `pathway` | string | — | yes | — | — |
| Variable | `variable` | string | — | no | — | — |
| Category | `category` | string | — | yes | — | — |
| Type | `type` | string | — | yes | — | — |
| SubType | `sub_type` | string | — | yes | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 3: `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

Schema, epoch 4:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Connection | `connection` | string | — | no | — | — |
| Scenario | `scenario` | string | — | yes | — | — |
| Variable | `variable` | string | — | no | — | — |
| Category | `category` | string | — | yes | — | — |
| Type | `type` | string | — | yes | — | — |
| SubType | `sub_type` | string | — | yes | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 4: `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

- Entity key: `resource_id`, `edition`, `connection`, `scenario`, `pathway`, `variable`, `category`, `type`, `sub_type`, `projection_year`
- Latest: `whole_capture` per `resource_id`
- Edition: `fes2023_es1_v002.csv` → 2023; `fes2024_es1_v002.csv` → 2024; `fes2025_es1_v006.csv` → 2025; `10yo2026_es1_v001.csv` → 2026
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

#### Shape and epoch map

Each SILVER resource is exactly one header epoch and one edition. Every body has six dimension
columns, then contiguous year columns. Epoch numbers follow the tables above. **`Scenario` and
`Pathway` are separate nullable silver columns and are never merged**: `scenario` is populated
only in the 2023 and 2026 editions, `pathway` only in 2024 and 2025, and the other column is
entirely null in each edition (verified in silver). Whether a vendor `Scenario` and a vendor
`Pathway` mean the same thing across editions is not established by the CSVs (`TODO: verify`
with NESO before any cross-edition join on them); the entity key keeps both so no row collapses.

| Epoch | Edition | Resource | Year columns (header labels) | Long rows | Null `value` |
|---|---|---|---|---:|---:|
| 1 | 2023 | `86812136-…` | 2022–2050 (29) | 17,052 | 1,958 |
| 2 | 2024 | `8c8a436d-…` | 2023–2050 (28) | 17,192 | 2,499 |
| 3 | 2025 | `6c78a777-…` | 2024–2050 (27) | 16,740 | 1,785 |
| 4 | 2026 | `b3bf8ac0-…` | 2024–2050 (27) | 3,375 | 1,875 |
| | **Total** | 4 resources | | **54,359** | **8,117** |

Epochs 3 and 4 share the same year range but differ in the scenario/pathway column, so they
are separate epochs. The long-row counts equal the independent pre-merge count over the real
bronze bodies (non-blank rows × year columns, VERIFICATION SCN-1d) and the activation receipt
(RULINGS 628; RESULTS §SCN-1d). Raw table row counts are 588, 614, 620 and 125 wide rows for
2023 to 2026 (the 2026 file is much smaller).

The full dimension tuple is unique within every retained body, and the silver long key
(including `edition` and `resource_id`) has no duplicates (verified in silver). Raw
all-blank rows occur only in the fully blank tails of the held 2021 and 2022 bodies (49 and 4
rows) and are not in silver.

Dimension cardinalities per edition (count of distinct non-null labels in silver, no label
values):

| Edition | `connection` | `variable` | `category` | `type` | `sub_type` | scenario or pathway |
|---|---:|---:|---:|---:|---:|---:|
| 2023 | 5 | 16 | 8 | 28 | 31 | 6 (scenario) |
| 2024 | 4 | 14 | 9 | 24 | 30 | 5 (pathway) |
| 2025 | 5 | 13 | 7 | 19 | 32 | 5 (pathway) |
| 2026 | 5 | 11 | 6 | 18 | 30 | 1 (scenario) |

The label domains change between editions, and a changed label is **not** a proven alias of an
earlier one. FACTS records, for example, that the carbon-intensity label spells its unit
differently in different editions and that some variables appear or disappear by edition
(for example the 2026 file has no CO2 labels). Keep the exact value; do not treat a changed
label as a semantic alias (`TODO: verify` with NESO).

#### Clocks

Two clocks, separate and not to be mixed (ADR-030, ADR-042):

1. **Vintage (`published_at` = `available_at`):** the CKAN `last_modified` of the captured
   resource (registry `vintage: ckan_last_modified`). It is when NESO last changed that file,
   not when the vendor generated the values. Verified in silver: `published_at` equals
   `available_at` on every row.
   - 2023: 2023-08-24T10:35:22.143299Z
   - 2024: 2024-08-02T11:01:29.547730Z
   - 2025: 2025-12-10T16:48:54.482473Z
   - 2026: 2026-09-16T14:27:45.949534Z
2. **Event time:** the temporal recipe is **`none`** (issue recipe also `none`). A projection
   year is a vendor header label, not a dated instant, so there is no row-level event time.
   `timestamp_utc` (and `event_time`, which equals it on every row, verified in silver) is the
   **capture time** of the bronze file, here 2026-10-08 about 10:55 UTC (the four captures
   within about eight seconds). It carries no information about the year a value covers. The
   period a label covers is held (see Holds); `projection_year` is only the vendor's header
   label as an integer.

`edition` is stamped from the file name, independent of both clocks; it is not an issue time.
Point-in-time queries bound `available_at <= as_of` per capture (RULINGS 597, the available-at
cutoff); that bound is on the vintage clock, not on the capture time. Every file was captured on
2026-10-08, after its `last_modified`, so `available_at <= as_of` is not proof that the bytes
held now were the bytes captured by then (ADR-039 FM-12). `TODO: verify` whether NESO edits a
file in place without bumping `last_modified`; nothing here shows it either way.

#### Units

The unit is **inside the `Variable` label**, in brackets, and gridflow keeps `variable`
verbatim with no unit column. The same year column therefore mixes units by row; no single unit
annotation is valid for a column, and a unit must never be inferred from a column name. The
vendor's 2021 field dictionary states explicitly that the unit is contained in `Variable`
(NESO ES1 2021 dictionary, cited in FACTS SCN-1d C10). Unit-bearing label classes observed in
the bodies (FACTS g-units; units as embedded in the vendor label):

| Variable label or label class | Unit in the label |
|---|---|
| `Capacity (MW)`, `Demand (MW)`, `Available DSR (MW)` | MW |
| `Storage Capacity (GWh)` | GWh |
| Consumption, Curtailment, Curtailment including DACCS, Demand, Demand Reduction, Export, Generation, Import, Netflows, each with `(TWh)` | TWh |
| `CO2 emissions (mt CO2)` and its excluding-BECCS variant | mt CO2 |
| `CO2 intensity of generation (gCO2/KWh)` | exact embedded spelling gCO2/KWh |
| `CO2 Intensity of Generation (gCO2/kWh)` and its excluding-BECCS variant | gCO2/kWh |

Not every class occurs in every edition: for example Available DSR appears from 2022 and is
not in the 2025 file, and the 2026 file has no CO2 labels. The two CO2-intensity spellings
differ only in capitalisation; `TODO: verify` they denote the same unit and quantity. What a
label such as `Demand` or `Generation` measures (and the definitions of category, type and
sub-type) is not defined in the CSVs (`TODO: verify` with NESO).

#### Missing values and sentinels

- **Blank year cells are kept as null `value`**, never replaced by zero (8,117 rows; table
  above). What a blank means (not modelled, not applicable, or zero) is not stated in the
  CSVs; the registry's hold question does not ask it. Zero is a real value and is kept as zero.
- The blanks are structured: in the 2023 file every year from 2029 to 2050 is blank in 89
  rows; in the 2024 file every year from 2030 is blank in 119 rows; in the 2025 file every
  year from 2036 is blank in 119 rows. The 2026 file has **all** its cells blank in header
  year 2024 and in 2037-2050, and non-blank cells only under 2025-2036, so a header year
  must not be read as proof that a projection exists for it.
- `Type` and `SubType` are blank in a few rows of each retained edition (2023: 20 Type and
  41 SubType; 2024: 5 and 25; 2025: 5 and 5; 2026: 1 and 1; wide-row counts in silver).
  `Category` is never blank in the 2023 to 2026 silver editions (0 nulls). Valid rows are
  kept; a blank lower-level dimension never excludes a row. `Connection` and `Variable` are
  non-null.
- Every non-blank year cell in the four SILVER bodies casts strictly to `Float64` (0
  failures); no null-token or whitespace rule is applied. No `-`, `NA` or `n/a` token occurs
  in any ES1 column. The only literal sentinel in the package is the **`N/A` text of the held
  2020 body**, kept as text in bronze and not converted; its meaning is unknown
  (`TODO: verify`).
- Held 2020 to 2022 bodies are not in silver and their figures are not on this page.
- Silver has no NaN in `value`.

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Ad hoc

One CSV per annual FES edition, so a new resource appears about once a year (editions in the
snapshot: 2020 to 2026). Each resource was captured once, on 2026-10-08. Package
`metadata_modified` in the 2026-10-06 snapshot is 2026-09-16T14:27:46.024221. The version
tokens in the file names show NESO re-uploads files within an edition; the vendor does not
publish a revision policy. `TODO: verify` whether a published edition file is revised in
place. Only a changed `last_modified` across successive captures can show it, and the registry
captured each resource once so far.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `fes_es1_electricity_supply`: held: TODO: for each ES1 edition, what period does a year label denote (calendar, financial or winter year; start or end label)? What does N/A mean in the 2020 edition, and will NESO republish the 2020–2022 tables without preambles, padding and thousands separators? (unit E-SEM)

The silver output exists on disk (54,359 rows, 2023 to 2026) but is **held**: gridflow's
models may not use it for point-in-time work until unit E-SEM answers the question above (held at activation, RULINGS 628). The registry carries `eligible` at package level and
`held` at family level (gridflow `@docs/neso_data_portal/eligibility.md`); the family status
governs the silver output. The hold has three parts:

1. **What a year header denotes (all editions).** `projection_year` is the vendor's header
   label as an integer. The period it denotes (calendar, financial or winter year), and whether
   the label is the start or the end of that period, is not stated in the CSVs or in the
   dictionaries captured, for any edition. The matching-edition FES Data Workbook notes might
   say; the FACTS research could not read them, so this stays `TODO: verify` with NESO.
2. **What `N/A` means in the 2020 edition.** 2,811 literal `N/A` cells sit in projection
   cells, and the 2020 body also has literal `N/A` in the dimension columns (68 in Category, 10
   in Type, 24 in SubType). The meaning (not modelled, not applicable or other) is
   undocumented.
3. **Whether NESO will republish 2020 to 2022 cleanly.** Those three resources are held at
   resource level: lexical numbers (thousands separators, padding, `N/A`) and, for 2021 and
   2022, a preamble before the header that the CSV reader cannot skip. They re-enter only
   after a supported header-row recipe and a lexical-number mechanism in gridflow (an engine
   change, a candidate for a later unit) or a corrected NESO upload (a new `last_modified`).

Settles it: a NESO statement of the period each year label covers per edition, a meaning for
the 2020 `N/A`, and either a corrected 2020 to 2022 upload or an adopted engine mechanism for
preambles and lexical numbers. The site page shows the 2023 to 2026 rows, read through the
`_latest` silver view, with one line naming the year-label question (ruling 66,
2026-10-24). Until the hold lifts, gridflow gold does not read this family (no gold view or gridflow_models consumer
for this package; RULINGS 611 applies the same decision to the sibling SCN docs-wave packages).

## Links

- Registry record: gridflow `@src/gridflow/connectors/neso_data_portal/registry/future-energy-scenario-electricity-supply-data-table-es1.json`
- Eligibility report: gridflow `@docs/neso_data_portal/eligibility.md`
- ADRs: gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md` (clocks),
  `@docs/DECISION_LOG/ADR-036-neso-profiler-and-pilot-records.md` (records and holds),
  `@docs/DECISION_LOG/ADR-039-neso-multi-resource-selection.md` (per-resource `_latest`),
  `@docs/DECISION_LOG/ADR-042-neso-scenario-unpivot-and-edition.md` (unpivot and edition)
- Package page: [NESO Data Portal – ES1](https://www.neso.energy/data-portal/future-energy-scenario-electricity-supply-data-table-es1)
- Vendor README: @../README.md
