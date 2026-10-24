---
source: "neso_data_portal"
package: "transmission-network-use-of-system-tnuos-tariffs"
dataset_keys: ["tnuos_tariffs_embedded_export", "tnuos_tariffs_half_hourly_hh_demand", "tnuos_tariffs_local_offshore_generator", "tnuos_tariffs_local_substation_tariff", "tnuos_tariffs_non_half_hourly_nhh_demand", "tnuos_tariffs_onshore_generator", "tnuos_tariffs_onshore_local_circuit", "tnuos_tariffs_transmission_demand"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  held: true
  title: TNUoS tariffs
  summary: >-
    NESO's Transmission Network Use of System (TNUoS) tariffs for generation and demand, by zone,
    site or band, stage and financial year.
  facts:
    vendor: "NESO Data Portal, package `transmission-network-use-of-system-tnuos-tariffs`: eight CSV files"
    cadence: Quarterly, as NESO lists it; updated when tariffs are published
    grain: "Row key: financial year, stage, publication date, and zone, site, band or substation type"
  landscape: market
  what_it_is: >-
    TNUoS tariffs price use of the GB transmission network by generation and demand. NESO's
    revenue team forecasts and sets them. Eight files cover half-hourly and non-half-hourly demand,
    embedded export, demand residual bands, onshore and offshore generators, local substations and
    onshore local circuits. Each row is one stage, forecast, draft or final, of a financial year's
    tariffs, with its publication date.
  how_used:
    - Compare zonal generation and demand tariffs across Great Britain, year by year
    - Follow NESO's forecasts for one charging year from release to final tariff
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show` per table, then its file downloaded whole unless
      its `last_modified` is unchanged. Swap in any table's key.
    commands:
      - {run: gridflow ingest neso_data_portal tnuos_tariffs_half_hourly_hh_demand --last 24h, comment: "whole file; swap in any key"}
      - {run: gridflow transform neso_data_portal tnuos_tariffs_half_hourly_hh_demand --last 24h, comment: "the capture's date to silver"}
  family:
    slug: transmission-network-use-of-system-tnuos-tariffs
    members:
      - dataset: tnuos_tariffs_half_hourly_hh_demand
        differs: "Half-hourly demand by zone 1 to 14: peak, year-round and floored tariffs, £/kW"
        request: "GET https://api.neso.energy/dataset/eaef4708-1100-4ad9-98d5-d892f3c9a56c/resource/6abe8416-149c-4c78-b65b-059eea19957a/download/tnuos_demand_hh.csv"
        held: NESO dates each publication but not when each row appeared, nor whether old rows change.
      - dataset: tnuos_tariffs_non_half_hourly_nhh_demand
        differs: "Non-half-hourly demand by zone 1 to 14: zonal and floored tariffs, in p/kWh"
        request: "GET https://api.neso.energy/dataset/eaef4708-1100-4ad9-98d5-d892f3c9a56c/resource/4e8dd130-5283-4f22-8c05-84e4d3280eb3/download/tnuos_demand_nhh.csv"
        held: NESO dates each publication but not when each row appeared, nor whether old rows change.
      - dataset: tnuos_tariffs_embedded_export
        differs: "Embedded export by demand zone: locational, avoided GSP infrastructure and floored tariffs, £/kW"
        request: "GET https://api.neso.energy/dataset/eaef4708-1100-4ad9-98d5-d892f3c9a56c/resource/af4501a0-6b96-4088-926c-7c7b0c499b08/download/tnuos_embeddedexport.csv"
        held: NESO dates each publication but not when each row appeared, nor whether old rows change.
      - dataset: tnuos_tariffs_transmission_demand
        differs: "Transmission Demand Residual tariffs by band, £ per site per day except unmetered supplies"
        request: "GET https://api.neso.energy/dataset/eaef4708-1100-4ad9-98d5-d892f3c9a56c/resource/dcca94fd-343e-4d4e-8c5d-66009dec4ad3/download/tnuos_tdr-tariffs.csv"
        held: "NESO dates each publication but not when each row appeared; the unmetered band's units conflict."
      - dataset: tnuos_tariffs_onshore_generator
        differs: "Onshore generation by zone 1 to 27: peak, year-round, residual and small-generator discount, £/kW"
        request: "GET https://api.neso.energy/dataset/eaef4708-1100-4ad9-98d5-d892f3c9a56c/resource/ffc0adb8-5426-474e-94a3-a5f3f01a0cdb/download/tnuos_generation_onshore.csv"
        held: NESO dates each publication but not when each row appeared, nor whether old rows change.
      - dataset: tnuos_tariffs_local_offshore_generator
        differs: "Each offshore generator's local substation, circuit and embedded transmission tariffs, £/kW"
        request: "GET https://api.neso.energy/dataset/eaef4708-1100-4ad9-98d5-d892f3c9a56c/resource/98569a29-940d-4bb7-8dc4-01e46187039a/download/tnuos_generation_offshore.csv"
        held: NESO dates each publication but not when each row appeared, nor whether old rows change.
      - dataset: tnuos_tariffs_local_substation_tariff
        differs: "Generators' local substation tariff by voltage, substation capacity and redundancy, £/kW"
        request: "GET https://api.neso.energy/dataset/eaef4708-1100-4ad9-98d5-d892f3c9a56c/resource/e697e9be-c068-482d-ae35-01f60bcb6700/download/local-substation-tnuos-tariff.csv"
        held: NESO dates each publication but not when each row appeared, nor whether old rows change.
      - dataset: tnuos_tariffs_onshore_local_circuit
        differs: "Onshore local circuit tariff by named substation, £/kW"
        request: "GET https://api.neso.energy/dataset/eaef4708-1100-4ad9-98d5-d892f3c9a56c/resource/01f36b32-4ad3-47fa-a645-7f7a47f1b0ae/download/tnuos_onshore_local_circuit.csv"
        held: "NESO dates each publication but not when each row appeared; some substation names end in whitespace."
  related:
    - {dataset: neso_data_portal/gis-boundaries-for-gb-generation-charging-zones, note: "Approximate boundaries of the TNUoS generation zones, as GIS files"}
    - {dataset: neso_data_portal/gis-boundaries-for-gb-dno-license-areas, note: "Licence areas NESO points to for TNUoS demand zone maps"}
    - {dataset: neso_data_portal/aahedc-tariffs, note: "Another network charge, forecast and set by the same NESO team"}
    - {dataset: neso_data_portal/bsuos-fixed-tariffs, note: "Fixed BSUoS rates, also published by stage with a publication date"}
---

# Transmission Network Use of System (TNUoS) Tariffs

This package is NESO's published set of **Transmission Network Use of System (TNUoS) tariffs**.
TNUoS is the annual charge that recovers the cost of owning and operating the GB transmission
network. It is levied on generators (a locational and a residual element, with separate local
charges for the substation and circuit a generator connects through) and on demand (a zonal
tariff for half-hourly and non-half-hourly demand, a credit for embedded export, and the
Transmission Demand Residual, TDR, charged by band). The vendor describes the package as "a
breakdown of all the Transmission Network Use of System (TNUoS) tariff elements" that are
"forecasted and set by the revenue team", updated quarterly "when tariffs are published" (CKAN
package `notes`,
@.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json). It is a Great
Britain package. Each of the eight resources is a CSV, and each row is one published version of
one tariff for one **financial year**, tagged with a **Publication** stage of `Forecast`,
`Draft` or `Final`, and a **Published Date**. The files therefore answer "what tariff was
announced, at which stage, for which charging year and which zone, circuit, substation or
band?". For modelling they are the transmission-charge side of a site's cost of connection and
use, to be read alongside the balancing charge (BSUoS) pages
(@./bsuos-fixed-tariffs.md) and the AAHEDC levy (@./aahedc-tariffs.md).

**Status: eligible package, every output held.** The package is eligible, and gridflow has a
silver output for each of the 8 families (captured 2026-10-08, transformed 2026-10-12). **All 8 outputs are
held** (hold TARIFF-ISSUE-AVAILABILITY): each body mixes `Forecast`, `Draft` and `Final` rows,
and no row carries a publication instant, so the evidence does not establish when each row
became available. Nothing in silver may be published or used for point-in-time models until
the hold is ruled. This page therefore gives schema, row counts, clocks and missingness only,
with **no data values** (no sample rows, no minima, maxima or value statistics). The
front-matter `eligibility: "eligible"` is the package-level registry status, not a statement
about the outputs.

- Publisher group: Network charges
- Registry group: network-charges · archetype: TAR

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Embedded Export Tariffs | CSV | upload | `af4501a0-6b96-4088-926c-7c7b0c499b08` |
| Half-Hourly (HH) Demand Tariffs | CSV | upload | `6abe8416-149c-4c78-b65b-059eea19957a` |
| Local Offshore Generator Tariffs | CSV | upload | `98569a29-940d-4bb7-8dc4-01e46187039a` |
| Local Substation TNUoS Tariff | CSV | upload | `e697e9be-c068-482d-ae35-01f60bcb6700` |
| Non Half-Hourly (NHH) Demand Tariffs | CSV | upload | `4e8dd130-5283-4f22-8c05-84e4d3280eb3` |
| Onshore Generator Tariffs | CSV | upload | `ffc0adb8-5426-474e-94a3-a5f3f01a0cdb` |
| Onshore Local Circuit Tariffs | CSV | upload | `01f36b32-4ad3-47fa-a645-7f7a47f1b0ae` |
| Transmission Demand Residual (TDR) Tariffs | CSV | upload | `dcca94fd-343e-4d4e-8c5d-66009dec4ad3` |

The package has 8 resources and every one has disposition SILVER, each feeding one family. It
has no DOC, GIS or catalogue-only resources and no `_files` family, so there are no DOC links to
list. Every resource is a CKAN upload with one body per family.

Download links and the one capture per family (2026-10-08, all CKAN `upload` resources). Size
and CKAN `last_modified` come from the capture sidecars under
`C:/gridflow-data/bronze/neso_data_portal/<family>/2026/10/08/`. "Body rows" counts the data
rows in the body, including wholly blank ones.

| File | Family | Bytes | Body rows | Silver rows | CKAN `last_modified` |
|---|---|---:|---:|---:|---|
| [tnuos_embeddedexport.csv](https://api.neso.energy/dataset/eaef4708-1100-4ad9-98d5-d892f3c9a56c/resource/af4501a0-6b96-4088-926c-7c7b0c499b08/download/tnuos_embeddedexport.csv) | `tnuos_tariffs_embedded_export` | 40,021 | 602 | 602 | 2026-05-28T16:24:12.610430 |
| [tnuos_demand_hh.csv](https://api.neso.energy/dataset/eaef4708-1100-4ad9-98d5-d892f3c9a56c/resource/6abe8416-149c-4c78-b65b-059eea19957a/download/tnuos_demand_hh.csv) | `tnuos_tariffs_half_hourly_hh_demand` | 46,457 | 602 | 602 | 2026-05-12T13:12:39.529022 |
| [tnuos_generation_offshore.csv](https://api.neso.energy/dataset/eaef4708-1100-4ad9-98d5-d892f3c9a56c/resource/98569a29-940d-4bb7-8dc4-01e46187039a/download/tnuos_generation_offshore.csv) | `tnuos_tariffs_local_offshore_generator` | 81,445 | 1,346 | 1,233 | 2026-05-12T13:07:57.900619 |
| [local-substation-tnuos-tariff.csv](https://api.neso.energy/dataset/eaef4708-1100-4ad9-98d5-d892f3c9a56c/resource/e697e9be-c068-482d-ae35-01f60bcb6700/download/local-substation-tnuos-tariff.csv) | `tnuos_tariffs_local_substation_tariff` | 2,702 | 84 | 36 | 2026-05-12T13:05:48.317924 |
| [tnuos_demand_nhh.csv](https://api.neso.energy/dataset/eaef4708-1100-4ad9-98d5-d892f3c9a56c/resource/4e8dd130-5283-4f22-8c05-84e4d3280eb3/download/tnuos_demand_nhh.csv) | `tnuos_tariffs_non_half_hourly_nhh_demand` | 40,071 | 602 | 602 | 2026-05-12T13:13:48.215441 |
| [tnuos_generation_onshore.csv](https://api.neso.energy/dataset/eaef4708-1100-4ad9-98d5-d892f3c9a56c/resource/ffc0adb8-5426-474e-94a3-a5f3f01a0cdb/download/tnuos_generation_onshore.csv) | `tnuos_tariffs_onshore_generator` | 112,370 | 1,161 | 1,161 | 2026-05-12T13:09:05.384311 |
| [tnuos_onshore_local_circuit.csv](https://api.neso.energy/dataset/eaef4708-1100-4ad9-98d5-d892f3c9a56c/resource/01f36b32-4ad3-47fa-a645-7f7a47f1b0ae/download/tnuos_onshore_local_circuit.csv) | `tnuos_tariffs_onshore_local_circuit` | 216,111 | 4,647 | 4,647 | 2026-05-12T13:10:10.034982 |
| [tnuos_tdr-tariffs.csv](https://api.neso.energy/dataset/eaef4708-1100-4ad9-98d5-d892f3c9a56c/resource/dcca94fd-343e-4d4e-8c5d-66009dec4ad3/download/tnuos_tdr-tariffs.csv) | `tnuos_tariffs_transmission_demand` | 22,977 | 462 | 462 | 2026-05-12T13:06:47.185973 |

Package page: [transmission-network-use-of-system-tnuos-tariffs](https://www.neso.energy/data-portal/transmission-network-use-of-system-tnuos-tariffs).

The silver total is **9,345 rows** across the 8 families. The 161 rows between body and silver
are all wholly blank rows (113 in the offshore generator body, 48 in the local substation
body). They are excluded by the non-nullable key columns and tallied, not treated as
observations. Transformed row counts equal the spec plan in every family
(@.planning/v0.22-RESULTS.md, section BAL-2c); no validation-failure tally is recorded.

## Families

All eight families share the same shape, and the points below apply to each one.

- **Single resource, whole-body capture.** Each family has one resource. `_latest` is
  `whole_capture`: the newest complete capture, not a per-key latest. The vendor publishes no
  key, and gridflow claims no vendor-certified revision key. `TODO: verify` a
  vendor-guaranteed unique key, and whether a published row can be revised in place.
- **Reader.** `csv`, `utf-8`, one header epoch per family. All eight bodies are valid UTF-8,
  have one header row and start with a UTF-8 BOM, which is kept off the first silver column
  name (seat full-body check, RULINGS 692,
  @.planning/phases/v0.22-K-BAL-2/BAL-2c-BRONZE-CHECK.json).
- **Identifiers are kept as supplied.** Zone numbers are int64 identifiers. Zone names,
  offshore-generator names, substation names, voltage, TEC band, connection type and TDR band
  are strings with no trimming or normalisation.
- **`Publication` labels are kept as-is.** `Forecast`, `Draft` and `Final` are never relabelled.
  A `Final` row is not a forecast merely because forecast inputs fed its calculation.
- **`Year_FY` is an identifier, not an instant.** It is the **ending** year of an April to March
  financial year. The vendor dictionary reads "Year in which the tariff relates to i.e. 2021 = 1
  April 2020 to 31 March 2021 (2020/21)". It carries no unit and is stored as int64.
- **`Published_Date` is a calendar date.** The captured spelling is `DD/MM/YYYY` in seven
  families (local circuit is the exception, below). The vendor dictionary sometimes describes
  an ISO format and records "ISO-8601" or "ISO 8601" in its unit field for the date column of
  two families (and for `Year_FY` in the TDR family); those are format labels, not physical
  units, and the actual spelling of the upload governs parsing. No publication time or clock
  is stated, and gridflow does **not** turn the date into a midnight-UTC instant.
- **Units come from the vendor dictionary only.** Where the dictionary leaves the unit field
  empty, the unit is taken from the cited vendor tariff statement or left as `—`, never
  inferred from a column name or a value range. Money columns are declared as delivered, so
  **£/kW is not rewritten to £/kW per year**. NESO describes annual charging liabilities, but
  the scoped columns declare £/kW (NESO final tariff statement,
  [document 376336](https://www.neso.energy/document/376336/download)).
- **Zeros are values.** A zero in a money column stays zero. Runs of zeros (for example in
  discount or adjustment columns) are not missing-value evidence.
- **Sentinels and missing values (FACTS g5).** The full-body scans found no literal `NA` or
  `N/A`, no thousands separators, currency symbols or percent signs in any measure cell, no
  padded or non-numeric measure cell and no numeric cast failure in any family. The records
  declare no null tokens. The only blanks are the 161 wholly blank rows above. Silver has
  **0 nulls in every column** of every family (2026-10-12), although the measure columns are
  declared nullable.
- **Two clocks, the same for every family.**
  1. **Vintage (`ckan_last_modified`).** `published_at` is the CKAN `last_modified` of the
     captured file, read as UTC (ADR-030), and `available_at = published_at`. In silver
     (2026-10-12) each family has one distinct `published_at`, equal to the sidecar's
     `ckan_last_modified` in the table above, and `available_at = published_at` on every row.
     The captures were written on 2026-10-08, between about four and five months after
     those vintages. The `last_modified` therefore does not prove that the bytes gridflow
     holds are the ones NESO published at that instant (ADR-039 FM-12, accepted residual), and
     the vendor's per-row Published Date is **not** used as `available_at`. Only one capture
     exists per family, so an as-of query before the family's `published_at` sees no rows.
  2. **Event time (temporal recipe `none`).** No column is an instant, so the engine has no
     event time to derive. `timestamp_utc` is the **capture time** (`capture_written_at`,
     2026-10-08), and `event_time` equals `timestamp_utc`; neither is a tariff date. Financial
     year and publication date stay typed (or raw) columns. Do not read `timestamp_utc` as the
     start of the charging year.
- **Silver layout.** One Parquet file per family under
  `C:/gridflow-data/silver/neso_data_portal/<family>/year=2026/month=10/`. The `year=`/`month=`
  partition is the **capture** date, not the tariff date. Columns are the vendor columns
  (below) then eight engine columns: `timestamp_utc`, `published_at`, `bronze_capture_id`,
  `capture_written_at`, `event_time`, `available_at`, `source_run_id` and `dataset_version`.
  All timestamps are tz-aware UTC. `dataset_version` is `1+e1` (record version 1, generic
  engine version 1). No gold view or builder reads any of these families.
- **Forward-target screening (FACTS g2).** The financial-year target start is 1 April of
  `Year_FY - 1`. The comparison of that start against each resource's own `last_modified` is the
  evidence behind the hold: every body mixes rows whose charging year starts before the vintage
  with rows that start after it, so the usual forward-target shortcut (RULINGS 529) does not
  apply. The counts are given per family below.

**What the stage counts mean.** The row counts by `Publication` stage and the on/before and
after counts are label and identifier tallies, not tariff values.

### `tnuos_tariffs_embedded_export`

- Kind: tabular · archetype: TAR · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Publication | `publication` | string | — | no | — | — |
| Year_FY | `year_fy` | int64 | — | no | — | — |
| Published_Date | `published_date` | date | `%d/%m/%Y` | no | — | — |
| Zone_No | `zone_no` | int64 | — | no | — | — |
| Zone_Name | `zone_name` | string | — | yes | — | — |
| Locational_£/kW | `locational_gbp_per_kw` | float64 | — | yes | — | £ per kW |
| AGIC_£/kW | `agic_gbp_per_kw` | float64 | — | yes | — | £ per kW |
| PhasedResidual_£/kW | `phased_residual_gbp_per_kw` | float64 | — | yes | — | £ per kW |
| EET(Floored)_£/kW | `eet_floored_gbp_per_kw` | float64 | — | yes | — | £ per kW |

- Entity key: `publication`, `year_fy`, `published_date`, `zone_no`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

Vintage `ckan_last_modified` (2026-05-28T16:24:12.610430); event time `none`, so `timestamp_utc`
is the capture time. Silver 602 rows (body 602), 17 columns, 0 nulls.

- **Columns (vendor dictionary).** `Zone_No` is the "Number Assigned to the Demand (Embedded
  Export) Zones 1 - 14" and `Zone_Name` its name. `Locational`, `AGIC` (Avoided GSP
  Infrastructure Costs), `PhasedResidual` and `EET(Floored)` (Embedded Export Tariff, floored)
  are each declared "£ per kW". The vendor comment on `PhasedResidual` says it "No longer applies
  from 2020/21"; the column is kept as delivered.
- **Identity.** All 602 rows are distinct on (publication, year_fy, published_date, zone_no),
  in the body and in silver. The zone number is the vendor demand-zone identifier, preserved
  as-is.
- **Stages.** Forecast 420, Draft 84, Final 98. Financial years in silver run from 2021 to 2031.
- **Forward targets.** 476 rows start on or before the vintage and 126 after it.

### `tnuos_tariffs_half_hourly_hh_demand`

- Kind: tabular · archetype: TAR · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Publication | `publication` | string | — | no | — | — |
| Year_FY | `year_fy` | int64 | — | no | — | — |
| Published_Date | `published_date` | date | `%d/%m/%Y` | no | — | — |
| Zone_No | `zone_no` | int64 | — | no | — | — |
| Zone_Name | `zone_name` | string | — | yes | — | — |
| Peak_£/kW | `peak_gbp_per_kw` | float64 | — | yes | — | £ per kW |
| YearRound_£/kW | `year_round_gbp_per_kw` | float64 | — | yes | — | £ per kW |
| HH_SGD_Adjustment_£/kW | `hh_sgd_adjustment_gbp_per_kw` | float64 | — | yes | — | £ per kW |
| HHTariff(Floored)_£/kW | `hh_tariff_floored_gbp_per_kw` | float64 | — | yes | — | £ per kW |

- Entity key: `publication`, `year_fy`, `published_date`, `zone_no`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

Vintage `ckan_last_modified` (2026-05-12T13:12:39.529022); event time `none`, so `timestamp_utc`
is the capture time. Silver 602 rows (body 602), 17 columns, 0 nulls.

- **Columns (vendor dictionary).** `Zone_No` is the "Number Assigned to the Demand Zones 1 -
  14". `Peak` and `YearRound` are the locational peak-security and year-round transport zonal
  tariffs (unfloored), `HH_SGD_Adjustment` is the half-hourly demand small-generator-discount
  adjustment, and `HHTariff(Floored)` is the overall half-hourly demand tariff, "Floored at
  £0/kW" per the vendor comment. All four are declared "£ per kW". The first three are described
  as elements of the overall HH demand tariff.
- **Identity.** All 602 rows are distinct on (publication, year_fy, published_date, zone_no).
- **Stages.** Forecast 420, Draft 84, Final 98 (the same totals as embedded export). Financial
  years 2021 to 2031.
- **Forward targets.** 476 on or before the vintage, 126 after.

### `tnuos_tariffs_local_offshore_generator`

- Kind: tabular · archetype: TAR · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Publication | `publication` | string | — | no | — | — |
| Year_FY | `year_fy` | int64 | — | no | — | — |
| Published_Date | `published_date` | date | `%d/%m/%Y` | no | — | ISO-8601 |
| OffshoreGenerator | `offshore_generator` | string | — | no | — | — |
| Substation_£/kW | `substation_gbp_per_kw` | float64 | — | yes | — | £/kW |
| Circuit_£/kW | `circuit_gbp_per_kw` | float64 | — | yes | — | £/kW |
| ETUoS_£/kW | `etuos_gbp_per_kw` | float64 | — | yes | — | £/kW |

- Entity key: `publication`, `year_fy`, `published_date`, `offshore_generator`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

Vintage `ckan_last_modified` (2026-05-12T13:07:57.900619); event time `none`, so `timestamp_utc`
is the capture time. Silver 1,233 rows (body 1,346), 15 columns, 0 nulls.

- **Blank rows.** 113 of the 1,346 body rows are wholly blank (every column empty). They are
  excluded by the non-nullable key columns, with the tally recorded at transform time. The
  other 1,233 rows are the observations.
- **Columns (vendor dictionary).** The dictionary gives `OffshoreGenerator`, `Substation`,
  `Circuit` and `ETUoS` titles but no description text. The money columns carry the dictionary
  unit "£/kW". Generator names are identifiers kept as supplied. The `Year_FY` dictionary unit
  is "N/A" and the `Published_Date` unit field reads "ISO-8601" (a format label).
- **Identity.** All 1,233 non-blank rows are distinct on (publication, year_fy, published_date,
  offshore_generator).
- **Stages (non-blank rows).** Forecast 865, Draft 174, Final 194. Financial years 2021 to 2031.
- **Forward targets.** 935 on or before the vintage, 298 after (non-blank rows).

### `tnuos_tariffs_local_substation_tariff`

- Kind: tabular · archetype: TAR · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Publication | `publication` | string | — | no | — | — |
| Year_FY | `year_fy` | int64 | — | no | — | — |
| Published_Date | `published_date` | date | `%d/%m/%Y` | no | — | — |
| Voltage | `voltage` | string | — | no | — | — |
| Sum of TEC at Connecting Substation | `sum_of_tec_at_connecting_substation` | string | — | no | — | — |
| Connection Type | `connection_type` | string | — | no | — | — |
| Tariff | `tariff_gbp_per_kw` | float64 | — | yes | — | — |

- Entity key: `publication`, `year_fy`, `published_date`, `voltage`, `sum_of_tec_at_connecting_substation`, `connection_type`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

Vintage `ckan_last_modified` (2026-05-12T13:05:48.317924); event time `none`, so `timestamp_utc`
is the capture time. Silver 36 rows (body 84), 15 columns, 0 nulls.

- **Blank rows.** 48 of the 84 body rows are wholly blank and are excluded by the non-nullable
  key columns, with a tally.
- **Unit.** The skeleton's vendor-unit cell is `—` because the dictionary's `unit` field for
  `Tariff` is empty (its description is "Local Substation Tariff"). The unit **£/kW** is taken
  from the vendor's local-substation tariff table in the five-year tariff statement
  ([document 367801](https://www.neso.energy/document/367801/download)), not from the column
  name or the neighbouring families. The silver column is named `tariff_gbp_per_kw` on that
  basis.
- **Dimensions.** `Voltage`, `Sum of TEC at Connecting Substation` (the dictionary calls it the
  "Capacity of the Substations") and `Connection Type` (the "Redundancy of the Substation") are
  string categories in the vendor's own spellings. They are not parsed into numbers and not
  normalised.
- **Identity.** All 36 non-blank rows are distinct on the six-column key.
- **Stages (non-blank rows).** Forecast 12, Draft 12, Final 12. Financial years in silver run
  2027 to 2028.
- **Forward targets.** 24 on or before the vintage, 12 after. Per the batch evidence
  (FACTS section 6), the Forecast rows all target charging years starting after the vintage
  while the Draft and Final rows start on or before it, so the mixed body still needs a stage
  and issue treatment (see Holds).

### `tnuos_tariffs_non_half_hourly_nhh_demand`

- Kind: tabular · archetype: TAR · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Publication | `publication` | string | — | no | — | — |
| Year_FY | `year_fy` | int64 | — | no | — | — |
| Published_Date | `published_date` | date | `%d/%m/%Y` | no | — | — |
| Zone_No | `zone_no` | int64 | — | no | — | — |
| Zone_Name | `zone_name` | string | — | yes | — | — |
| NHH_Zonal_p/kWh | `nhh_zonal_p_per_kwh` | float64 | — | yes | — | Pence per kWh |
| NHH_SGD_Adjustment_p/kWh | `nhh_sgd_adjustment_p_per_kwh` | float64 | — | yes | — | pence per kWh |
| NHHTariff(Floored)_p/kWh | `nhh_tariff_floored_p_per_kwh` | float64 | — | yes | — | Pence per kWh |

- Entity key: `publication`, `year_fy`, `published_date`, `zone_no`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

Vintage `ckan_last_modified` (2026-05-12T13:13:48.215441); event time `none`, so `timestamp_utc`
is the capture time. Silver 602 rows (body 602), 16 columns, 0 nulls.

- **Units.** This is the one demand family quoted in **pence per kWh**, unlike the £/kW demand
  families. The dictionary declares "Pence per kWh" (and, for the adjustment column, "pence per
  kWh"). The two spellings are the same unit. No conversion to £/kW is made.
- **Columns (vendor dictionary).** `NHH_Zonal` is the zonal non-half-hourly tariff (unfloored),
  `NHH_SGD_Adjustment` the non-half-hourly small-generator-discount adjustment, and
  `NHHTariff(Floored)` the overall non-half-hourly demand tariff (floored).
- **Identity.** All 602 rows are distinct on (publication, year_fy, published_date, zone_no).
- **Stages.** Forecast 420, Draft 84, Final 98. Financial years 2021 to 2031.
- **Forward targets.** 476 on or before the vintage, 126 after.

### `tnuos_tariffs_onshore_generator`

- Kind: tabular · archetype: TAR · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Publication | `publication` | string | — | no | — | — |
| Year_FY | `year_fy` | int64 | — | no | — | — |
| Published_Date | `published_date` | date | `%d/%m/%Y` | no | — | — |
| Zone_No | `zone_no` | int64 | — | no | — | — |
| Zone_Name | `zone_name` | string | — | yes | — | — |
| SystemPeak_£/kW | `system_peak_gbp_per_kw` | float64 | — | yes | — | £ per kW |
| SharedYearRound_£/kW | `shared_year_round_gbp_per_kw` | float64 | — | yes | — | £ per kW |
| NotSharedYearRound_£/kW | `not_shared_year_round_gbp_per_kw` | float64 | — | yes | — | £ per kW |
| Residual_£/kW | `residual_gbp_per_kw` | float64 | — | yes | — | £ per kW |
| SmallGenDiscount_£/kW | `small_gen_discount_gbp_per_kw` | float64 | — | yes | — | £ per kW |

- Entity key: `publication`, `year_fy`, `published_date`, `zone_no`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

Vintage `ckan_last_modified` (2026-05-12T13:09:05.384311); event time `none`, so `timestamp_utc`
is the capture time. Silver 1,161 rows (body 1,161), 18 columns, 0 nulls.

- **Zones.** `Zone_No` is the "Number Assigned to the Generation Zone 1 - 27": generation zones,
  not the 14 demand zones. Do not join this family to a demand family on `zone_no`.
- **Columns (vendor dictionary).** System Peak, Shared Year-Round, Not Shared Year-Round,
  Generation Residual and Small Generator Discount tariffs, each declared "£ per kW". The
  dictionary text writes the unit as "£/kw" in some descriptions; the unit field is "£ per kW".
- **Zeros.** Small Generator Discount is a value column in which zeros are values, not gaps.
- **Identity.** All 1,161 rows are distinct on (publication, year_fy, published_date, zone_no).
- **Stages.** Forecast 810, Draft 162, Final 189. Financial years 2021 to 2031.
- **Forward targets.** 918 on or before the vintage, 243 after.

### `tnuos_tariffs_onshore_local_circuit`

- Kind: tabular · archetype: TAR · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Publication | `publication` | string | — | no | — | — |
| Year_FY | `year_fy` | int64 | — | no | — | — |
| Published_Date | `published_date` | string | — | no | — | — |
| Substation_Name | `substation_name` | string | — | no | — | — |
| Tariff_£/kW | `tariff_gbp_per_kw` | float64 | — | yes | — | £ per kW |

- Entity key: `publication`, `year_fy`, `published_date`, `substation_name`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

Vintage `ckan_last_modified` (2026-05-12T13:10:10.034982); event time `none`, so `timestamp_utc`
is the capture time. Silver 4,647 rows (body 4,647), 13 columns, 0 nulls.

- **`Published_Date` is a raw string, not a date.** One body holds two spellings: 3,677 rows use
  `DD/MM/YYYY` and 970 rows use `YYYY/MM/DD`. A single resource with two formats cannot be
  typed by the per-filename format mechanism, so the column is stored raw, byte-equal to the
  body. The vendor dictionary's own example uses the year-first spelling, but the body mixes
  both. `TODO: CIRCUIT-PUBLICATION-DATE-CAST` is needed only if a typed date is required; it
  must be settled with an existing faithful casting capability or a vendor-normalised body, not
  an invented parser. Raw preservation is available now.
- **Padded substation names.** 78 `Substation_Name` cells carry trailing spaces or a tab. They
  are **kept raw**; the key is unique both raw and stripped. Whether the padding is meaningful
  is a vendor question (see Holds). Any join on substation name must account for it.
- **Column (vendor dictionary).** `Tariff_£/kW` is the "Onshore Local Circuit Tariff",
  declared "£ per kW".
- **Identity.** All 4,647 rows are distinct on (publication, year_fy, published_date,
  substation_name).
- **Stages.** Forecast 3,594, Draft 492, Final 561. Financial years 2021 to 2031.
- **Forward targets.** 3,135 on or before the vintage, 1,512 after.

### `tnuos_tariffs_transmission_demand`

- Kind: tabular · archetype: TAR · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Publication | `publication` | string | — | no | — | — |
| Year_FY | `year_fy` | int64 | — | no | — | ISO 8601 |
| Published_Date | `published_date` | date | `%d/%m/%Y` | no | — | ISO 8601 |
| TDR Band | `tdr_band` | string | — | no | — | — |
| TDR Tariff in Â£/(Site Day) | `tdr_tariff` | float64 | — | yes | — | p/kWh for sites of unmetered supplies; OR £/site for all other final demand sites |
| Notes | `notes` | string | — | yes | — | — |

- Entity key: `publication`, `year_fy`, `published_date`, `tdr_band`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

Vintage `ckan_last_modified` (2026-05-12T13:06:47.185973); event time `none`, so `timestamp_utc`
is the capture time. Silver 462 rows (body 462), 14 columns, 0 nulls.

- **Mojibake header.** The tariff column header in the body is literally `TDR Tariff in Â£/(Site
  Day)`: the bytes `c3 82 c2 a3`, a double-encoded pound sign. The body is otherwise valid
  UTF-8. The record keeps that spelling as the vendor column source, and the silver name is
  clean (`tdr_tariff`). The silver column carries **no unit suffix** on purpose.
- **Unit conflict (held question).** The dictionary description reads "TDR tariffs per day, at
  6d.p. ... for all sites except UMS (UMS sites TDR tariffs are in p/kWh per day)", and its unit
  field "p/kWh for sites of unmetered supplies; OR £/site for all other final demand sites". So
  ordinary bands are £ per site per day, but the **unmetered (UMS) band's unit conflicts**: the
  dictionary says p/kWh per day, while NESO's final tariff statement
  ([document 376336](https://www.neso.energy/document/376336/download)) labels the unmetered
  charge p/kWh/annum in its summary and p/kWh in its detailed table. `TODO: TDR-UNMETERED-UNIT`
  (see Holds). The value is preserved as delivered with its band; no daily or annual conversion
  is applied, and the column must not be summed across bands without resolving it.
- **Dictionary versus body.** The dictionary says the date is "in the format of year-month-date"
  and the unit field says "ISO 8601" for `Year_FY` and `Published_Date`. The body spells the date
  `DD/MM/YYYY`, which is what the record parses. `Year_FY` is the ending year (the dictionary
  comment: "for example, 2024 for financial year 2023/24").
- **Bands.** `TDR Band` is the "Band category for final demand sites that are liable for
  Transmission Demand Residual (TDR) tariffs"; the body has 22 band identifiers, kept as
  supplied. `Notes` is the vendor's "alternative names for the TDR bands" (nullable string,
  kept as supplied).
- **Identity.** All 462 rows are distinct on (publication, year_fy, published_date, tdr_band).
- **Stages.** Forecast 308, Draft 66, Final 88. Financial years in silver run 2024 to 2031.
- **Forward targets.** 286 on or before the vintage, 176 after.

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Quarterly

The vendor says the files are updated quarterly "when tariffs are published" and that
registered users can subscribe to automatic updates. The registry refresh is `adhoc`, so
gridflow does not schedule these captures. Seven resources share a `last_modified` on or about
2026-05-12 and the embedded-export resource was last modified on 2026-05-28, which is
consistent with an update in May 2026 but does not prove a tariff publication on those dates.
`TODO: verify` the publication calendar (the Draft and Final dates relative to the charging
year), whether earlier publications are retained in the same file, and whether NESO revises a
published row in place. Only more captures, compared pair by pair, can show this. One capture
per family exists to date (2026-10-08).

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `tnuos_tariffs_embedded_export`: held: TODO: TARIFF-ISSUE-AVAILABILITY — each body mixes Forecast/Draft/Final rows with no publication instant; what was available when (publication-level evidence), and how should mixed stages be treated? A publication date alone does not establish availability at midnight. (unit v0.22-K-BAL-2c)
- `tnuos_tariffs_half_hourly_hh_demand`: held: TODO: TARIFF-ISSUE-AVAILABILITY — each body mixes Forecast/Draft/Final rows with no publication instant; what was available when (publication-level evidence), and how should mixed stages be treated? A publication date alone does not establish availability at midnight. (unit v0.22-K-BAL-2c)
- `tnuos_tariffs_local_offshore_generator`: held: TODO: TARIFF-ISSUE-AVAILABILITY — each body mixes Forecast/Draft/Final rows with no publication instant; what was available when (publication-level evidence), and how should mixed stages be treated? A publication date alone does not establish availability at midnight. (unit v0.22-K-BAL-2c)
- `tnuos_tariffs_local_substation_tariff`: held: TODO: TARIFF-ISSUE-AVAILABILITY — each body mixes Forecast/Draft/Final rows with no publication instant; what was available when (publication-level evidence), and how should mixed stages be treated? A publication date alone does not establish availability at midnight. (unit v0.22-K-BAL-2c)
- `tnuos_tariffs_non_half_hourly_nhh_demand`: held: TODO: TARIFF-ISSUE-AVAILABILITY — each body mixes Forecast/Draft/Final rows with no publication instant; what was available when (publication-level evidence), and how should mixed stages be treated? A publication date alone does not establish availability at midnight. (unit v0.22-K-BAL-2c)
- `tnuos_tariffs_onshore_generator`: held: TODO: TARIFF-ISSUE-AVAILABILITY — each body mixes Forecast/Draft/Final rows with no publication instant; what was available when (publication-level evidence), and how should mixed stages be treated? A publication date alone does not establish availability at midnight. (unit v0.22-K-BAL-2c)
- `tnuos_tariffs_onshore_local_circuit`: held: TODO: TARIFF-ISSUE-AVAILABILITY — each body mixes Forecast/Draft/Final rows with no publication instant; what was available when (publication-level evidence), and how should mixed stages be treated? A publication date alone does not establish availability at midnight. Are trailing spaces / tab in `Substation_Name` meaningful, or should NESO republish them trimmed? (unit v0.22-K-BAL-2c)
- `tnuos_tariffs_transmission_demand`: held: TODO: TARIFF-ISSUE-AVAILABILITY — each body mixes Forecast/Draft/Final rows with no publication instant; what was available when (publication-level evidence), and how should mixed stages be treated? A publication date alone does not establish availability at midnight. TODO: TDR-UNMETERED-UNIT — ordinary bands are £/(site day), but the unmetered band's unit conflicts (the dictionary says p/kWh per day, the final tariff statement p/kWh/annum in its summary and p/kWh in its detailed table); which unit does the Unmetered band carry in this column? (unit v0.22-K-BAL-2c)

All 8 silver outputs exist on disk (activated 2026-10-12, captures dated 2026-10-08, ruled in RULINGS 702, reconcile
`--all --cutoff 2026-10-12` exit 0 with 0 gaps over 141 families, RULINGS 703) but are **held**.
They may not be published or used for point-in-time models until unit v0.22-K-BAL-2c's
questions are answered. The holds sit in the records (RULINGS 692 set them when the batch was
ruled; PR #110 merged triple-green, RULINGS 701).

**Why the usual shortcut fails.** Where every row of a forecast-style file targets a period after
the file's CKAN `last_modified`, gridflow lets the vintage stand in for the issue time (RULINGS
529, forward-target exception). Here every family mixes rows whose charging year starts on or
before the vintage with rows whose charging year starts after it (the on/before and after
counts above), and each body mixes the three stages. The vintage therefore cannot be read as
the date each row became known, and a `Final` row must not be relabelled a forecast.

**What is not established.** The vendor gives a publication **date** but no time of day, and
nothing shows when a given row first appeared on the portal, or that an old row is never
rewritten in place. gridflow will not manufacture a midnight-UTC issue time from
`Published_Date` to fill the gap. NESO's tariff statements distinguish Draft forecasts from
Final tariffs and describe Final publication relative to the start of the charging year, but
neither the labels nor the statements supply a per-row timestamp or a historical availability
guarantee.

**What settles it.** An immutable, dated vendor publication history showing when each row (or
publication) was available, or an approved conservative publication-date availability recipe
together with an authorised treatment of mixed Forecast, Draft and Final rows. Either is a
record edit once ruled. The two family-specific questions, the padded substation names and the
unmetered TDR unit, need a vendor clarification tied to the specific CSV column. Until then, row
counts, schema, clocks and missingness are all this page asserts.
