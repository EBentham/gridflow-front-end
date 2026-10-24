---
source: "neso_data_portal"
package: "aahedc-tariffs"
dataset_key: "aahedc_tariffs"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  held: NESO dates each publication but not when each row appeared, nor whether old rows change.
  title: AAHEDC tariffs
  summary: >-
    NESO's tariffs for Assistance for Areas of High Electricity Distribution Costs (AAHEDC): draft
    and final rates by financial year, in p/kWh.
  facts:
    vendor: "NESO Data Portal, package `aahedc-tariffs`: one CSV file"
    cadence: Every 6 months, as NESO lists it; updated when tariffs are published
    grain: "Each row: one financial year's tariffs at one stage, with its published date"
  landscape: market
  what_it_is: >-
    Each row gives one financial year's AAHEDC tariffs at a draft or final stage, with the date NESO
    published them: the total scheme tariff, the Shetland tariff and the tariff excluding the
    Shetland assistance amount, in pence per kWh. A financial year runs April to March and is named
    by its ending year. NESO's revenue team forecasts and sets them.
  how_used:
    - The AAHEDC rate NESO set for each financial year, in pence per kWh
    - How far the final rate moved from its draft, financial years 2025 to 2027
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then the file downloaded whole unless its
      `last_modified` is unchanged.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=aahedc-tariffs"
      - "GET https://api.neso.energy/dataset/43d94335-c97f-4939-a8b9-607d2cfb3734/resource/ffd29cc8-3c55-4e83-aa0e-73212d4fedba/download/aahedc-tariffs-for-dataportal-2026-07.csv"
    commands:
      - {run: gridflow ingest neso_data_portal aahedc_tariffs --last 24h, comment: whole file to bronze}
      - {run: gridflow transform neso_data_portal aahedc_tariffs --last 24h, comment: "the capture's date to silver"}
  related:
    - {dataset: neso_data_portal/transmission-network-use-of-system-tnuos-tariffs, note: "Transmission network charges, forecast and set by the same NESO team"}
    - {dataset: neso_data_portal/bsuos-fixed-tariffs, note: "Fixed BSUoS rates, also published by stage with a publication date"}
---

# Assistance for Areas of High Electricity Distribution Costs (AAHEDC) Tariffs

This package is NESO's schedule of **AAHEDC tariffs**. AAHEDC is the charge that funds assistance for
areas with high electricity distribution costs, and the vendor singles out a Shetland
assistance amount. It is published as a flat pence-per-kWh rate and is **not** a geographical
zone series: there is one tariff per financial year and stage, not one per zone. `TODO: verify`
who pays the charge and how it is recovered; the vendor dictionary does not say.
NESO's revenue team forecasts and sets the tariffs, and the vendor says the file is updated
"bi annual (when tariffs are published)" (CKAN package `notes`,
@.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json). The CKAN update
frequency is "Every 6 months". Each row is one published version of the tariff for one
**financial year (FY)**: a **Publication Type** stage (`Draft` or `Final`), the **Year FY**
(the ending year of an April-March financial year), the **Published Date**, and three tariff
columns in pence per kWh: the total scheme tariff, the Shetland tariff, and the AAHEDC tariff
excluding the Shetland assistance amount. A `Draft` row is a forecast of a coming year's rate
and a `Final` row is the rate set for that year (NESO's AAHEDC guidance, FACTS section 6 W08).
A `Final` row must not be relabelled a forecast just because forecast demand entered its
calculation.

For modelling, it is one of several network-charge components, published alongside the TNUoS tariffs
(@./transmission-network-use-of-system-tnuos-tariffs.md) and the fixed BSUoS tariffs
(@./bsuos-fixed-tariffs.md).

The capture holds 9 rows (6 `Final`, 3 `Draft`). gridflow has a silver output for it, but it is
**held**: the body mixes `Draft` and `Final` rows with no publication instant, so what was
available when is not established (see Holds). The package-level status in the front matter is
generated from the registry and reads `eligible`, but the family-level eligibility is **held**.
The silver exists on disk, yet nothing in it may be published or used for point-in-time models
yet. This page therefore gives schema, row counts, clocks and missingness only, with **no data
values**.

- Publisher group: Network charges
- Registry group: network-charges · archetype: TAR

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Assistance for Areas of High Electricity Distribution Costs (AAHEDC) Tariffs | CSV | upload | `ffd29cc8-3c55-4e83-aa0e-73212d4fedba` |

The package has one resource, a CSV with disposition SILVER. It has no DOC or catalogue-only
resources and no `_files` family.

Download link and the one capture (2026-10-08, a CKAN upload resource). Size and CKAN
`last_modified` come from the capture sidecar under
`C:/gridflow-data/bronze/neso_data_portal/aahedc_tariffs/2026/10/08/`. Data rows equal the
silver rows.

| File | Bytes | Data rows | CKAN `last_modified` |
|---|---:|---:|---|
| [aahedc-tariffs-for-dataportal-2026-07.csv](https://api.neso.energy/dataset/43d94335-c97f-4939-a8b9-607d2cfb3734/resource/ffd29cc8-3c55-4e83-aa0e-73212d4fedba/download/aahedc-tariffs-for-dataportal-2026-07.csv) | 608 | 9 | 2026-07-15T09:16:36.703704 |

Package page: [aahedc-tariffs](https://www.neso.energy/data-portal/aahedc-tariffs).

**Bronze body (seat full-body check, RULINGS 692,
@.planning/phases/v0.22-K-BAL-2/BAL-2c-BRONZE-CHECK.json).** Valid UTF-8, **no BOM** (unlike the
eight TNUoS bodies), one header, CRLF line endings, 9 data rows, no wholly blank row, no padded
cell and no null in any column. The three tariff columns hold plain decimals and the body has no
literal `NA`, `-1` or other sentinel. Body sha256 prefix `2ebbf27d` (full digest in the sidecar).

## Families

### `aahedc_tariffs`

- Kind: tabular · archetype: TAR · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Publication Type | `publication_type` | string | — | no | — | — |
| Year FY | `year_fy` | int64 | — | no | — | ISO 8601 |
| Published Date | `published_date` | date | `%d/%m/%Y` | no | — | ISO 8601 |
| Total Scheme Tariff in p/kwh | `total_scheme_tariff_p_per_kwh` | float64 | — | yes | — | Pence per kilowatt hour |
| Shetland Tariff in p/kwh | `shetland_tariff_p_per_kwh` | float64 | — | yes | — | Pence per kilowatt hour |
| AAHEDC tariff excluding the Shetland Assistance Amount in p/kwh | `tariff_excluding_shetland_assistance_amount_p_per_kwh` | float64 | — | yes | — | Pence per kilowatt hour |

- Entity key: `publication_type`, `year_fy`, `published_date`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**One header epoch.** The record accepts one exact header, the six columns above. The vendor
column names are kept as the source; the silver names are lower snake case with `p_per_kwh`
spelling out the unit.

**What the columns mean (vendor dictionary).** These descriptions come from NESO's saved field
info for the resource (gridflow
`@.planning/research/neso-snapshots/field-info/20261008T114228Z/aahedc_tariffs.json`).

- **`Publication Type`**: "Draft or Final Tariffs". The capture holds exactly these two labels,
  kept as supplied and never relabelled.
- **`Year FY`**: "Financial year". The dictionary example is "2024 for financial year 2023/24",
  so the value is the **ending year** of an April-March financial year. It is an identifier, not
  an instant and not a measurement.
- **`Published Date`**: "Date when this tariff was published". It is a calendar date, with no
  time of day and no zone.
- **`Total Scheme Tariff in p/kwh`**, **`Shetland Tariff in p/kwh`** and **`AAHEDC tariff
  excluding the Shetland Assistance Amount in p/kwh`**: each described as the named tariff "at 6
  decimal places". `TODO: verify` the arithmetic relationship between the three columns (for
  example whether the total is the sum of the other two); the dictionary does not state it and
  gridflow does not infer it from values.

**Units (vendor dictionary only).** The three tariff columns' dictionary `unit` field is **Pence
per kilowatt hour**, and each header also carries `p/kwh`. gridflow keeps the value as delivered
and does no unit conversion (no pounds, no per-year scaling). The dictionary `unit` field for
`Year FY` and `Published Date` reads "ISO 8601", which is not a physical unit; `Year FY` is a
four-digit identifier and neither column is treated as a quantity. `Publication Type` has an
empty unit field.

**Date spelling conflict (settled by the body).** The dictionary comment says "year-month-date"
and the unit says ISO 8601, but its own example, and every one of the 9 body values, is
`DD/MM/YYYY` (the first component exceeds 12 in all nine, so day-first is unambiguous).
The record therefore parses `%d/%m/%Y`; the actual upload spelling governs faithful parsing
(FACTS section 6). Zero cast failures.

**Two clocks.**

1. **Vintage (`ckan_last_modified`).** `published_at` is the CKAN `last_modified` of the
   captured file, read as UTC (ADR-030): 2026-07-15T09:16:36.703704Z, equal to the sidecar's
   `ckan_last_modified`. `available_at` equals `published_at` on all 9 rows (silver,
   2026-10-12), and all 9 rows share one value. The capture was written on 2026-10-08, almost
   three months later. Only one capture exists, so an as-of query before 2026-07-15T09:16 sees
   **no** rows. The `last_modified` predates the capture, so `available_at <= as_of` does not
   prove that the bytes gridflow holds are the ones NESO published at that instant (ADR-039
   FM-12, accepted residual). The vendor's per-row Published Date is **not** used as
   `available_at`, because a date alone does not establish availability at midnight.
2. **Event time (temporal recipe `none`).** The record carries **no** event-time column:
   financial year and publication date are labels, not instants, so no settlement-date or
   timestamp anchor is derived. `timestamp_utc` and `event_time` are therefore the **capture
   time** (`capture_written_at`, 2026-10-08T08:13:00.098981Z on every row), a storage
   convention and not a vendor measurement instant. Do not read either as the tariff's
   effective period or its publication time. To find the tariff period, use `year_fy`
   (April to March ending in that year); gridflow makes no further instant from it.

**Identity and selection (ADR-039).**

- The **measured grain** is `(publication_type, year_fy, published_date)`. All 9 rows are
  distinct on it, in the captured body and in silver (2026-10-12). The tariffs are measures, not
  part of identity.
- The vendor publishes no key. `TODO: verify` a vendor-guaranteed unique key, and whether a
  published row can be revised in place.
- `_latest` is `whole_capture`: the newest complete capture, not a per-key latest. gridflow does
  not claim a vendor-certified revision key. The stage and the date are both part of
  the key, so a reader must choose a stage deliberately.

**Sentinels and missing values (FACTS g5).** The full-body scans found no blanks, no `NA`/`N/A`,
no numeric `-1`, no thousands separators or currency symbols, and no measured zero or sentinel
cell. The record declares no null tokens. Silver has 0 nulls in every column (2026-10-12),
although the three tariff columns are declared nullable. Nothing is mapped to null.

**Row counts (silver, 2026-10-12).**

| Resource | Rows | Distinct on entity key | `Final` | `Draft` |
|---|---:|---:|---:|---:|
| `ffd29cc8-3c55-4e83-aa0e-73212d4fedba` | 9 | 9 | 6 | 3 |

**Activation (2026-10-12, master `784fa86`, PR #110).** The AAHEDC and TNUoS batch merged
triple-green (RULINGS 701). The family was transformed from the 2026-10-08 capture with
`--start/--end 2026-10-08`; there was no prior silver, so nothing was overwritten and no
snapshot was taken (RULINGS 702). Silver has **9 rows**, equal to the planned count, with 0
validation failures and no blank-row exclusions, and the family is recorded as held. The
batch-wide reconcile `--all --cutoff 2026-10-12` exited 0 with 0 gaps over 141 families
(45 adjudicated, 0 stale; RULINGS 703). Gridflow `@.planning/v0.22-RESULTS.md` section BAL-2c
holds the receipt.

Silver layout: one Parquet file under
`C:/gridflow-data/silver/neso_data_portal/aahedc_tariffs/year=2026/month=10/`. The
`year=`/`month=` partition is the **capture** date, not the tariff date. Columns (14): the six
vendor columns, then `timestamp_utc`, `published_at`, `bronze_capture_id`,
`capture_written_at`, `event_time`, `available_at`, `source_run_id` and `dataset_version`. All
timestamps are tz-aware UTC. `dataset_version` is `1+e1` (record version 1, generic engine
version 1). No gold view or builder reads this family.

**Related packages.** The TNUoS tariff families share this batch, the same hold and the
Draft/Final/Forecast stage pattern; see @./transmission-network-use-of-system-tnuos-tariffs.md.
The fixed BSUoS tariffs are in @./bsuos-fixed-tariffs.md.

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Every 6 months

The vendor says updates come twice a year, when tariffs are published. The resource file name
carries a year and month (`2026-07`), and its CKAN `last_modified` is 2026-07-15, consistent
with a July publication. `TODO: verify` the publication calendar, whether a new publication
replaces the file in place (same resource id, new file name) or adds a resource, whether earlier
publications are retained in the body, and whether NESO revises a published row. Only more
captures, compared pair by pair, can show this. One capture exists to date (2026-10-08).

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `aahedc_tariffs`: held: TODO: TARIFF-ISSUE-AVAILABILITY — each body mixes Forecast/Draft/Final rows with no publication instant; what was available when (publication-level evidence), and how should mixed stages be treated? A publication date alone does not establish availability at midnight. (unit v0.22-K-BAL-2c)

The silver output exists on disk but is **held**. It may not be published or used for
point-in-time models until the question above is answered. The record's own unit tag is
v0.22-K-BAL-2c; no resolving unit is named yet (`TODO: name the unit that will settle TARIFF-ISSUE-AVAILABILITY`). The hold sits in the record,
and RULINGS 692 set it when the batch was specified (class 3, merged under RULINGS 701).

**Why the usual shortcut fails.** Where every row in a forecast-style file targets a period
after the file's CKAN `last_modified`, gridflow lets the vintage stand in for the issue time
(RULINGS 529, forward-target exception). Here every financial year starts on or before the
vintage (2026-07-15), so the exception does not apply. The question text mentions Forecast
because it is shared across the nine families of the batch; this body carries `Draft` and
`Final` only. The vintage therefore cannot be read as the date each row became known.

**What is not established.** The vendor gives a publication **date** but not the time of day,
and nothing shows when a given row first appeared on the portal. Nor is it shown that an old
row is never rewritten in place. gridflow will not manufacture a midnight-UTC issue time from
`Published Date` to fill the gap, and will not relabel `Final` rows as forecasts or drop
`Draft` rows to dodge the question.

What settles it: an immutable, dated vendor publication history that shows when each row was
available, or an approved conservative publication-date availability recipe that also rules how
mixed stages are treated. Either is a record edit once ruled. Until then, row counts, schema and
clocks are all this page asserts.
