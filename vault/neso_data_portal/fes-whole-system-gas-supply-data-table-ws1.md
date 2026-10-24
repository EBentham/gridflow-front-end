---
source: "neso_data_portal"
package: "fes-whole-system-gas-supply-data-table-ws1"
dataset_key: "fes_ws1_gas_supply"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-15
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# FES: Pathways to Net Zero – Whole System & Gas Supply Data table (WS1)

NESO's whole-system and gas-supply table from the Future Energy Scenarios (FES) data workbook.
The package notes call it one of "an agreed set of data tables containing the GB FES values for
whole system and gas supply". It is one wide table per edition. Each row is one supply, demand or
capacity item, described by a fuel type, a unit, a category, a sector, a fuel, a feedstock and a
category lookup, for one scenario (2023, 2026) or one pathway (2024, 2025). The columns are the
years 2020 to 2050. It is the gas and fuel-supply side of the scenario set, so once its hold lifts
it is a candidate scenario input for gas-supply, bioenergy, hydrogen and whole-system energy
models. Its companion table is the emissions table
(@fes-whole-system-gas-supply-emissions-data-table-ws2.md). It sits beside the other FES tables
(@fes-road-transport-summary-data-table-ed5.md,
@fes-natural-gas-demand-definitions-ed4.md).

The package has four resources, one per edition: 2023, 2024, 2025 and 2026. The 2026 resource has
the filename prefix `10yo2026`. NESO's 2026 resource description calls it "One of the Ten-Year Outlook outputs", so the 2026 table is
the **Ten Year Outlook** rather than a full FES edition (catalogue snapshot resource description).
`TODO: verify` how NESO scopes the 2026 outlook against the 2023-2025 FES editions before
comparing the editions column for column.

**The silver output of this family is held (unit E-SEM).** It exists on disk for two of the four
editions, and this page gives its schema, row counts and structure. It publishes no data values from
it: no sample rows and no minimum, maximum or other value statistics. What a year label denotes and
what a blank cell means is not established (see Holds). The package-level `eligibility: eligible`
in the front matter is the package registry entry. The hold is per family. Two of the four
resources have a further problem of their own, described under Per-resource status.

Reading rules for anyone who does open the silver:

- **Edition is a dimension.** The four resources are four separately published tables. Never sum or
  average across `edition`. The 2023, 2024, 2025 and 2026 rows for the same item and the same
  year are different forecasts, not observations.
- **`scenario` and `pathway` are two separate columns.** The 2023 and 2026 files head the column
  `Scenario`. The 2024 and 2025 files head it `Pathway`. Each silver row has at most one of the two
  populated and the other null. gridflow does not merge them. `TODO: verify` whether NESO treats the
  two headings as the same concept, and never sum across scenarios (or across pathways).
- **Mixed units share one `value` column.** Energy (`TWh`), power or capacity (`GW`) and gas volume
  per year (`bcm/yr`) rows all land in `value`. The row's `units` string is the only thing that
  tells them apart. Filter by `units`. **Never sum across units**, and never sum across rows without
  first reading what each row is (an item can be a component of, or an overlap with, another item
  the table does not state).
- **`projection_year` is a label.** It is the integer column header. The period it denotes is
  undocumented (see Holds).
- **A null `value` is a blank vendor cell** with an undocumented meaning. A `0` is a value.

- Publisher group: FES: Pathways to Net Zero
- Registry group: future-energy-scenarios · archetype: SCN
- Vendor tags: Bioenergy, Capacity, Demand, FES, FES2023, Hydrogen, Natural Gas, Subscribable, Supply

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Whole System & Gas Supply (WS1) 2023 | CSV | upload | `b04e227d-f329-4ccf-8e25-821ea6ea03ca` |
| Whole System & Gas Supply (WS1) 2025 | CSV | upload | `ebf4f503-0a13-45e6-89ad-b707748613b6` |
| Whole System & Gas Supply (WS1) 2026 | CSV | upload | `0dd30611-5b9f-452d-bd34-966737d14fca` |

### HOLD

| Resource | Format | Capture | Id | Reason (unit) |
|---|---|---|---|---|
| Whole System & Gas Supply (WS1) 2024 | CSV | upload | `fa5697c5-9810-480f-b4c5-ab41dc53777a` | the 2024 body fails the strict float64 cast on 7128 projection cells, every one the literal `N/A` (264 per column 2023-2049), whose meaning NESO does not document; declaring it a null token would assert an undocumented semantic; re-disposition only after NESO defines `N/A` (then an exact `null_tokens` declaration) or uploads a corrected file (a new last_modified) (E-SEM) |

There is no `DOC` resource in the package: all four resources are CSV data tables, and the page
has no separate documentation download. The files, as captured on 2026-10-08 (bytes and wide data
rows from the bronze capture and the batch facts; `last_modified` is the CKAN value in the
2026-10-06 catalogue snapshot, offset-less and read as UTC):

| Edition | Disposition | Download | Bytes | Wide data rows | CKAN `last_modified` |
|---|---|---|---:|---:|---|
| 2023 | SILVER | [fes2023_ws1_v001.csv](https://api.neso.energy/dataset/8cbe76c7-6971-40ed-8e0c-2d8c8520cd0c/resource/b04e227d-f329-4ccf-8e25-821ea6ea03ca/download/fes2023_ws1_v001.csv) | 84,644 | 547 | `2023-07-10T03:30:11.101381` |
| 2024 | HOLD | [fes2024_ws1_v001.csv](https://api.neso.energy/dataset/8cbe76c7-6971-40ed-8e0c-2d8c8520cd0c/resource/fa5697c5-9810-480f-b4c5-ab41dc53777a/download/fes2024_ws1_v001.csv) | 115,812 | 537 | `2024-07-15T06:19:57.831578` |
| 2025 | SILVER (capture fails, see below) | [fes2025_ws1_v006.csv](https://api.neso.energy/dataset/8cbe76c7-6971-40ed-8e0c-2d8c8520cd0c/resource/ebf4f503-0a13-45e6-89ad-b707748613b6/download/fes2025_ws1_v006.csv) | 112,615 | 657 | `2025-12-10T16:57:40.652852` |
| 2026 | SILVER | [10yo2026_ws1_v001.csv](https://api.neso.energy/dataset/8cbe76c7-6971-40ed-8e0c-2d8c8520cd0c/resource/0dd30611-5b9f-452d-bd34-966737d14fca/download/10yo2026_ws1_v001.csv) | 9,840 | 52 | `2026-09-16T14:49:53.687177` |

The stable handle for a resource is its id, not the file name. The file name, the resource name and
the captured edition agree for every resource, and gridflow reads the edition from the exact file
name. The version token differs by file (`v001`, `v001`, `v006`, `v001`), which shows NESO
re-uploads files under the same slot (the 2025 file is at `v006`). The vendor publishes no revision
policy; `TODO: verify` whether a published edition is revised in place. Every body decodes strictly
as UTF-8. The 2023 and 2024 bodies start with a byte-order mark, which the reader handles. No body
has a preamble, an unnamed trailing column, a ragged row or an all-blank row.

The vendor's resource description for 2023 to 2025 reads "an agreed set of data tables containing
the GB FES values for whole system and gas supply"; the 2026 description reads "a set of data
tables containing the values for whole system and gas supply" and names the Ten-Year Outlook.

### Per-resource status

| Edition | Silver rows | Status |
|---|---:|---|
| 2023 | 16,957 | Transformed (547 wide rows × 31 year columns). Family held E-SEM. |
| 2024 | 0 | Resource HOLD (E-SEM): never transformed. The would-be output is 537 × 31 = 16,647 rows if the cast ever passes. |
| 2025 | 0 | Capture fails the duplicate-entity-key guard (`DuplicateEntityKeyError`) and is recorded as an ADR-040 `failed` ledger entry (ruling 839). The would-be output is 657 × 31 = 20,367 rows. Never deduplicated. |
| 2026 | 1,612 | Transformed (52 wide rows × 31 year columns). Family held E-SEM. |
| | **18,569** | Silver total = the planned count (RULINGS 844). |

## Families

### `fes_ws1_gas_supply`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Fuel Type | `fuel_type` | string | — | no | — | — |
| Scenario | `scenario` | string | — | yes | — | — |
| Units | `units` | string | — | no | — | — |
| Category | `category` | string | — | no | — | — |
| Sector | `sector` | string | — | yes | — | — |
| Fuel | `fuel` | string | — | yes | — | — |
| Feedstock | `feedstock` | string | — | yes | — | — |
| Category Lookup | `category_lookup` | string | — | yes | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 1: `2020` → 2020, `2021` → 2021, `2022` → 2022, `2023` → 2023, `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Fuel Type | `fuel_type` | string | — | no | — | — |
| Pathway | `pathway` | string | — | yes | — | — |
| Units | `units` | string | — | no | — | — |
| Category | `category` | string | — | no | — | — |
| Sector | `sector` | string | — | yes | — | — |
| Fuel | `fuel` | string | — | yes | — | — |
| Feedstock | `feedstock` | string | — | yes | — | — |
| Category Lookup | `category_lookup` | string | — | yes | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 2: `2020` → 2020, `2021` → 2021, `2022` → 2022, `2023` → 2023, `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

- Entity key: `resource_id`, `edition`, `fuel_type`, `scenario`, `pathway`, `units`, `category`, `sector`, `fuel`, `feedstock`, `category_lookup`, `projection_year`
- Latest: `whole_capture` per `resource_id`
- Edition: `fes2023_ws1_v001.csv` → 2023; `fes2025_ws1_v006.csv` → 2025; `10yo2026_ws1_v001.csv` → 2026
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

The edition map has three entries. The 2024 file name is deliberately **not** in the map: its
resource is on hold and never transformed, so it has no edition stamp. The two header epochs are
the two physical headers: epoch 1 heads the second column `Scenario` (2023 and 2026 files), epoch 2
heads it `Pathway` (the 2024 and 2025 files). The 2024 file's header is the same as the 2025 header,
but because the 2024 resource is held, epoch 2 is exercised by no successfully transformed
capture. Silver also carries the standard provenance columns written to every silver row:
`edition` (int64), `resource_id`, `timestamp_utc`, `published_at`, `available_at`, `event_time`,
`bronze_capture_id`, `capture_written_at`, `source_run_id`, `dataset_version` (the value is `1+e1`
on every row: registry record version 1 plus silver engine version `e1`. It does not identify the
schema epoch). Silver has both a `scenario` and a `pathway` column in every file, because a union of
the two epochs is written; the column that the file does not head is null. The silver files sit
under `C:\gridflow-data\silver\neso_data_portal\fes_ws1_gas_supply\`, in `year=2026\month=10\`,
one Parquet file per successful capture (two files: the 2023 and 2026 captures).

#### The two clocks

Two clocks, separate and not to be mixed (ADR-030, ADR-042):

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured resource, read as UTC. There is one vintage per resource and every
   row of an edition shares it. Checked on every silver row on 2026-10-15: `available_at` equals
   `published_at`, and `published_at` equals the resource's `last_modified` (2023:
   `2023-07-10T03:30:11.101381Z`; 2026: `2026-09-16T14:49:53.687177Z`). It says when the file last
   changed on the portal, not when NESO first published the edition, so do not read the dates as the
   original publication dates of the FES workbooks (`TODO: verify` with the vendor). For the held
   2024 and failed 2025 resources the vintage is in the file table above; no silver row carries it.
2. **Event time (temporal recipe `none`).** The record declares no event-time recipe, because the
   year labels have no established period (see Holds). `timestamp_utc` is therefore the **capture
   time** of the bronze file, not a modelled time. `event_time` and `capture_written_at` carry the
   same instant. All rows of a capture share one `timestamp_utc`: `2026-10-08 10:58:02 UTC` (the 2023
   capture) and `2026-10-08 10:58:11 UTC` (the 2026 capture). Do not use `timestamp_utc` as a forecast
   horizon or a model time axis. The only year information is `projection_year`, a label.

`edition` is stamped from the file name, independent of both clocks; it is not an issue time.
Point-in-time queries bound `available_at <= as_of` per capture. That bound is on the vintage clock,
not on the capture time. Every file was captured on 2026-10-08, after its `last_modified`, so
`available_at <= as_of` does not prove that the bytes held now were the bytes NESO published by then
(ADR-039). `TODO: verify` whether NESO edits a file in place without bumping `last_modified`.

#### Shape and counts

Each wide row is unpivoted over the same 31 year columns (`2020` to `2050`) in every edition, so the
silver row count is the wide-row count × 31.

| Edition | Wide rows | Silver rows (potential) | Silver rows (actual) | `projection_year` labels |
|---|---:|---:|---:|---|
| 2023 | 547 | 16,957 | 16,957 | 2020-2050 |
| 2024 | 537 | 16,647 | 0 (held) | 2020-2050 |
| 2025 | 657 | 20,367 | 0 (capture failed) | 2020-2050 |
| 2026 | 52 | 1,612 | 1,612 | 2020-2050 |

The 2023 file has 6 distinct `scenario` values and the 2026 file has 1. The 2024 and 2025 files each
head the column `Pathway`. This page publishes no label lists for the held family.
`TODO: verify` the vendor's definition of each scenario and pathway label, and whether a label in one
edition is the same scenario as a label in another. Activation (2026-10-15, master `06378b9`,
PR #125): transform window 2026-10-08, one capture per resource and no prior silver, **18,569 rows**
(2023: 16,957 · 2026: 1,612) = the planned count, with the one planned failure (2025 capture,
`DuplicateEntityKeyError`). The whole SCN-3 batch transformed 59,388 rows. Reconcile `--all --cutoff
2026-10-13` exited 0 over 255 families with 0 gaps, 61 adjudicated (+1, this family's 2025 capture),
and coverage was clean (gridflow `@.planning/v0.22-RESULTS.md` §SCN-3; RULINGS 842, 844).

#### Units (vendor dictionary: the row's `Units` field)

The unit carrier is each wide row's exact `Units` value, read from that field and never inferred
from a column name or from magnitudes (FACTS g4). No `Units` cell is blank. The year columns mix
units by row, so the table has no single scalar unit. Wide rows by unit, as published:

| `units` | 2023 | 2024 | 2025 | 2026 |
|---|---:|---:|---:|---:|
| `TWh` | 470 | 467 | 587 | 38 |
| `GW` | 35 | 35 | 35 | 7 |
| `bcm/yr` | 42 | 35 | 35 | 7 |

- The silver `units` column holds these three strings verbatim. There is no conversion and no
  separate unit column beyond `units` itself. Silver rows by unit (the wide rows × 31): 2023 `TWh`
  14,570 · `GW` 1,085 · `bcm/yr` 1,302; 2026 `TWh` 1,178 · `GW` 217 · `bcm/yr` 217.
- `TWh` rows are energy over a period, `GW` rows are power or capacity, and `bcm/yr` rows are gas
  volume per year. The dictionary's year description does not say which period a `TWh` or `bcm/yr`
  row integrates over, nor at what moment a `GW` capacity is assessed. Both are part of the held
  question.
- `TODO: verify` whether any row is a total, a component or an overlap of another row. The table
  carries no stated aggregation rule, so never sum rows within or across `units`, `category`,
  `sector` or `fuel`.

#### Sentinels and missing values (FACTS g5)

The record declares no null token.

- **Blank projection cells** are kept as **null** `value`. They are not dropped and not filled.
  The vendor does not say what a blank means. Unmodelled, unavailable, inapplicable and not yet
  published are all possible; their position or frequency does not settle it. `TODO: verify`
  (part of the hold). A blank in one edition says nothing about another edition. The blank cells
  per body (CSV bodies, all 31 year columns):

  | Edition | Blank projection cells | Where |
  |---|---:|---|
  | 2023 | 8,525 | `2020`: 351; each of `2021`-`2028`: 253; each of `2029`-`2049`: 291; `2050`: 39 |
  | 2024 | 2,166 | `2020`: 361; `2021`: 353; `2022`: 339; each of `2030`-`2050`: 53; others none |
  | 2025 | 11,901 | `2020`: 412; `2021`: 402; `2022`: 384; `2023`: 369; each of `2024`-`2035`: 364; each of `2036`-`2049`: 422; `2050`: 58 |
  | 2026 | 734 | `2020`: 3; each of `2021`-`2023`: 1; each of `2037`-`2050`: 52; others none |

  In silver these are the null `value` rows: 8,525 (2023) and 734 (2026), equal to the blank counts.
- **Blank identifier cells.** `sector`, `fuel`, `feedstock` and `category_lookup` may be blank (the
  four columns are nullable). Counts of blank cells in the wide rows: 2023 sector 26 · fuel 177 ·
  feedstock 291 · category lookup 321; 2024 26 · 170 · 269 · 318; 2025 1 · 117 · 289 · 436; 2026 1 ·
  25 · 52 · 11. A blank identifier stays null and takes part in the entity key as null. A few identifier cells in the
  2023–2025 files hold only a non-breaking space (U+00A0; sector 4, fuel 3, feedstock 4, category lookup 4
  rows per file); silver keeps these as non-null strings, so they key as a distinct value, not as null. `fuel_type`,
  `units` and `category` have no blanks.
- **The literal `N/A`.** It occurs **only** in the 2024 file's projection cells: 7,128 cells, exactly
  264 in each of the year columns `2023` to `2049`. It is not a blank and is not declared a null
  token. NESO does not define it in the inspected primary sources. Reading it as missing would
  assert an undocumented semantic, so the 2024 resource is on hold (see Holds). No other file has
  it, and literal `-`, `NA` and `n/a` are absent from every file.
- **Zeros are values.** Numeric zeros occur in the bodies. No primary source identifies them as
  sentinels, and no zero-as-missing rule is applied. Do not treat zero as missing.
- Every non-blank cell of the 2023, 2025 and 2026 bodies casts strictly to float64 with zero
  failures. The 2024 body fails on the `N/A` cells only (7,128 of 16,647 potential values).

#### Identity and selection

The entity key is `resource_id`, `edition`, `fuel_type`, `scenario`, `pathway`, `units`, `category`,
`sector`, `fuel`, `feedstock`, `category_lookup` and `projection_year`. This is a **measured guard
key**: the 2023, 2024 and 2026 bodies pass it with zero duplicated long rows, and no measure belongs
in it (FACTS K3). No vendor text declares it as the identity of a row. `TODO: verify` the vendor's
own uniqueness rule. `_latest` is `whole_capture` per `resource_id`: a newer capture of a resource
replaces that resource's previous capture as a whole, never another edition. No revision rule between
captures of one resource is claimed.

**The 2025 capture fails the key.** The 2025 body repeats one set of seven dimension values (fuel
type bioenergy, unit `TWh`, category supply, sector waste, fuel waste, feedstock `MSW, C&I
(biogenic)` and a blank category lookup) twice for each of four pathways: 8 wide rows sharing 4 dimension tuples, with
conflicting values between the two rows of a pair. The missing discriminator is an omitted vendor
dimension. Unpivoted, the 8 wide rows are 248 participating long rows sharing 124 keys, and the
duplicate guard fails the capture. gridflow never deduplicates it, never keeps one of the two
rows and never adds a measure to the key to make it pass. The failure is recorded as an ADR-040
`failed` entry in the reconcile adjudication ledger (`DuplicateEntityKeyError`, ruling 839) and the
capture stays unloaded until NESO publishes a corrected file (a new `last_modified`) or names the
omitted dimension. See Holds.

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc

One CSV per annual FES edition, so a new resource appears about once a year (editions in the
snapshot: 2023, 2024, 2025, 2026). Each resource was captured once, on 2026-10-08. Package
`metadata_modified` in the 2026-10-06 snapshot is `2026-09-16T14:49:53.749804`. The registry captured
each resource once, so a change to a published file's `last_modified` between captures has not been
observed.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `fes_ws1_gas_supply`: held: TODO: For each WS1 edition and quantity class (`TWh`, `GW`, `bcm/yr` rows), what interval or assessment date does a year header denote, and is the integer a starting or ending label? What does a blank projection cell mean? What does the literal `N/A` in `fes2024_ws1_v001.csv` mean? Which omitted dimension distinguishes the four repeated Bioenergy / Waste / `MSW, C&I (biogenic)` rows per pathway in `fes2025_ws1_v006.csv`, and can NESO publish a corrected file? (unit E-SEM)

The family is held by the SCN-3 batch records (RULINGS 838 and 839, with the activation in 842
and 844). Its silver output stays on disk for 2023 and 2026. No gold view or model feed is planned for it
while the hold stands, and this page publishes no data values from it. Unit E-SEM must answer
four things before the hold can lift:

1. **The period behind each year label**, separately for the `TWh`, `GW` and `bcm/yr` rows, and for
   each edition. For example, is a `TWh` item a calendar year, a financial year, a gas year or a
   winter, and is a `GW` capacity assessed at the start, the end or the middle of the year? Is the
   integer a starting or an ending label?
2. **What a blank projection cell means.** The vendor does not say whether it is unmodelled,
   unavailable, inapplicable or something else.
3. **What the literal `N/A` means** in the 2024 file. When NESO defines it, the 2024 resource
   can be re-dispositioned with an exact `null_tokens` declaration. A corrected upload (a new
   `last_modified`) also re-opens it.
4. **Which omitted dimension distinguishes the repeated rows** in the 2025 file, and whether NESO
   can publish a corrected file. The 2025 capture's ADR-040 ledger entry lifts on a corrected upload.

What the vendor text does establish, and what it does not (FACTS g1):

- The [WS1 dictionary](https://www.neso.energy/data-portal/fes-whole-system-gas-supply-data-table-ws1/whole_system__gas_supply_ws1_2026)
  describes a year as the year of data for the item and names the `Units` field as the row's unit.
  It does not establish a calendar, financial or gas-year interval, an assessment date for stock
  or capacity items, or a start-versus-end label.
- No other SCN family's year convention transfers to this one. The same-edition notes for other
  FES tables (for example the ED6 notes for ED5) describe their own items only.
- Publication vintage is not a substitute for the period: the CKAN `last_modified` is a
  conservative proxy for availability and nothing finer.

Until the hold lifts:

- Do not publish WS1 values, or join WS1 to an observed series by `projection_year`.
- Do not use WS1 point-in-time. Its only clock is the CKAN `last_modified` vintage, a conservative
  proxy and nothing finer.
- Do not sum across editions, across units, across `scenario` and `pathway`, or across WS1 rows.
- Do not read the 2024 or 2025 resource through any workaround: no coercion of `N/A` to null, no
  deduplication of the 2025 repeats and no measure added to the key.

Related: the WS2 emissions table (@fes-whole-system-gas-supply-emissions-data-table-ws2.md) is
held on its own questions (gridflow `@docs/neso_data_portal/eligibility.md`). Its units are
undocumented except for the 2025 edition's `MTCO2e`; no WS2 unit transfers to WS1.

No gold view or gridflow_models consumer reads this family (RULINGS 555: no gold feed for the docs
wave of this package).

## Links

- Registry record: gridflow `@src/gridflow/connectors/neso_data_portal/registry/fes-whole-system-gas-supply-data-table-ws1.json`
- Eligibility report: gridflow `@docs/neso_data_portal/eligibility.md`
- Batch evidence: gridflow `@.planning/phases/v0.22-K-SCN-3/K-SCN-3-FACTS.md` (§3.1, §6.1), `@.planning/phases/v0.22-K-SCN-3/K-SCN-3-SPEC.md` (§2 and the ledger)
- Activation receipt: gridflow `@.planning/v0.22-RESULTS.md` (§SCN-3)
- ADRs: gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md` (clocks),
  `@docs/DECISION_LOG/ADR-040-neso-reconcile-adjudication.md` (the 2025 `failed` ledger entry),
  `@docs/DECISION_LOG/ADR-042-neso-scenario-unpivot-and-edition.md` (unpivot and edition)
- Sibling (the emissions table): @30-vendors/neso-data-portal/datasets/fes-whole-system-gas-supply-emissions-data-table-ws2.md
- Package page: [NESO Data Portal – WS1](https://www.neso.energy/data-portal/fes-whole-system-gas-supply-data-table-ws1)
- Vendor README: @../README.md
