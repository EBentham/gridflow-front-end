---
source: "neso_data_portal"
package: "bsuos-fixed-tariffs"
dataset_key: "bsuos_fixed_tariffs"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-10
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: BSUoS fixed tariffs
  summary: >-
    NESO's fixed BSUoS tariffs: each tariff's stages and publication dates, the settlement dates
    covered and the rate in £/MWh.
  facts:
    vendor: "NESO Data Portal, package `bsuos-fixed-tariffs`: one CSV file"
    cadence: "Biannual, as NESO lists it (six monthly): updated when tariffs are published"
    grain: "Each row: one tariff at one publication stage, with its published date"
  landscape: market
  what_it_is: >-
    Balancing Services Use of System (BSUoS) charges recover the cost of day-to-day operation of the
    transmission system. A fixed tariff is a rate in £/MWh set in advance for a stated range of
    settlement dates. NESO's revenue team forecasts and sets them; each row is one stage of one
    tariff, initial forecast, draft or final, with its publication date.
  how_used:
    - The BSUoS rate NESO announced for a range of settlement dates, stage by stage
    - How far each tariff moved between its draft and final stages
    - Read beside the settled BSUoS charges for the same settlement dates
  chart:
    type: line
    silver: neso_data_portal/bsuos_fixed_tariffs
    time: fixed_tariff_start_date
    value: fixed_tariff_gbp_per_mwh
    group: publication
    group_map: {"Initial Forecast": initial, Draft: draft, Final: final}
    series_order: [final, draft, initial]
    dedup: {"on": [publication, fixed_tariff_title, published_date], order_by: published_at}
    aggregation: last
    window: {start: "2023-04-01", end: "2027-10-01"}
    unit: "£/MWh"
  chart_view:
    title: Fixed BSUoS tariff by stage, April 2023 to March 2028
    caption: >-
      Silver `neso_data_portal/bsuos_fixed_tariffs`, £/MWh: each tariff's rate at each stage NESO
      published, one point per six-month tariff, placed at its period. Lines join tariffs, not dates
      within one. Published dates are not drawn.
    alt: >-
      Line chart from neso_data_portal/bsuos_fixed_tariffs in £/MWh, one point per six-month tariff,
      April 2023 to the period from October 2027. Final rates, in order: 13.41, 14.03, 7.63, 12.17,
      10.74, 15.69, 13.74 and 12.49 for the period from October 2026. Draft rates run from 7.60 for
      October 2024 to 21.67 and 18.42 for the two periods from April 2027, which have no final rate
      in the file. Initial forecasts: 14.55 and 11.03 for the two periods from April 2026.
    x_label: "each tariff's six months, from its first date"
    key:
      - {series: final, label: Final, paint: petrol}
      - {series: draft, label: Draft, paint: clay}
      - {series: initial, label: Initial forecast, paint: olive}
  caveat: Published Date has no time, and NESO does not say older rows stay unchanged.
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then the file downloaded whole unless its
      `last_modified` is unchanged.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=bsuos-fixed-tariffs"
      - "GET https://api.neso.energy/dataset/6c862622-48ff-4025-b998-d4d3db9e984d/resource/4dfa533f-bec6-491b-a3f1-7ce92449bc9a/download/bsuos-fixed-tariffs-data-portal-new-header.csv"
    commands:
      - {run: gridflow ingest neso_data_portal bsuos_fixed_tariffs --last 24h, comment: whole file to bronze}
      - {run: gridflow transform neso_data_portal bsuos_fixed_tariffs --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: fixed_tariff_title, op: in, value: [Fixed Tariff 7, Fixed Tariff 8, Fixed Tariff 9, Fixed Tariff 10]}
      dedup: {"on": [publication, fixed_tariff_title, published_date], order_by: published_at}
      order_by: [published_date, fixed_tariff_start_date]
      columns: [publication, fixed_tariff_title, published_date, fixed_tariff_start_date, fixed_tariff_end_date, fixed_tariff_gbp_per_mwh, published_at, timestamp_utc]
    key: [publication, fixed_tariff_title, published_date]
    caption: "Tariffs 7 to 10 at every stage NESO published: initial forecast, draft and final."
    fields:
      publication: "The stage: Initial Forecast, Draft or Final; part of the key"
      fixed_tariff_title: "NESO's name for the tariff, one per six-month period; part of the key"
      published_date: "NESO's published date for this stage, with no time; part of the key"
      fixed_tariff_start_date: "First settlement date the tariff applies to (NESO's dictionary)"
      fixed_tariff_end_date: "Final settlement date the tariff applies to (NESO's dictionary)"
      fixed_tariff_gbp_per_mwh: "The BSUoS tariff at this stage, £/MWh (NESO's dictionary)"
      published_at: "NESO's last-modified time for the whole file, read as UTC; one per capture"
      timestamp_utc: "Start of `fixed_tariff_start_date`, GB local midnight, as UTC; gridflow's anchor"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote the capture to bronze, UTC
  notebook:
    lead: >-
      Returns a pandas DataFrame from the DuckDB view
      `silver_neso_data_portal_bsuos_fixed_tariffs_latest`, every row of the newest capture,
      filtered on `fixed_tariff_start_date` with both ends included; lineage columns dropped.
    cells:
      - |
        df = data.neso_data_portal.query("bsuos_fixed_tariffs", "2023-04-01", "2027-10-01")
        df = df.sort_values(["published_date", "fixed_tariff_start_date"], ignore_index=True)
        df[["publication", "fixed_tariff_title", "published_date", "fixed_tariff_start_date", "fixed_tariff_gbp_per_mwh"]].tail()
      - |
        rates = df.pivot(index="fixed_tariff_title", columns="publication", values="fixed_tariff_gbp_per_mwh")
        rates = rates.loc[df.fixed_tariff_title.unique(), ["Initial Forecast", "Draft", "Final"]].rename_axis(index=None, columns=None)
        rates["final_minus_draft"] = rates.Final - rates.Draft
        rates
      - |
        rates.final_minus_draft.dropna().plot.bar(color="#155A6E", rot=0, figsize=(8, 3.5),
                                                  xlabel="tariff", ylabel="final minus draft, £/MWh");
    needs: the fixed tariffs file
    plot_alt: >-
      Bar plot of each tariff's final rate minus its draft rate, in £/MWh, for Fixed Tariffs 4 to 8,
      the tariffs with both stages: 4.57, -1.74, 3.70, -0.47 and 0.56.
  related:
    - {dataset: neso_data_portal/current-balancing-services-use-of-system-bsuos-data, note: "The settled BSUoS charges, one file per settlement run"}
    - {dataset: neso_data_portal/bsuos-monthly-forecast, note: "NESO's rolling monthly forecast of BSUoS costs, 24 months ahead"}
    - {dataset: neso_data_portal/balancing-services-use-of-system-bsuos-daily-forecast, note: "NESO's half-hourly BSUoS charge forecast, stopped in April 2023"}
---

# BSUoS Fixed Tariffs

This package is NESO's schedule of **fixed Balancing Services Use of System (BSUoS) tariffs**.
BSUoS is the charge that recovers the cost of balancing the GB system, and a fixed tariff is a
pre-announced £/MWh rate that applies to a stated range of settlement dates. NESO's revenue
team forecasts and sets the tariffs, and the vendor says the file is updated six-monthly, "when
tariffs are published" (CKAN package `notes`,
@.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json). The CKAN update
frequency is "Biannual". Each row is one published version of one tariff: a **Publication**
stage, a **Fixed Tariff Title** naming the tariff, the **Published Date**, the first and last
settlement dates the tariff applies to, and the rate in £/MWh. The package is a single CSV
resource covering Great Britain. It is a forward-looking schedule of charge rates, so it
answers "what rate was announced, at which stage, for which settlement dates?" For modelling
it is the rate side of BSUoS cost recovery. The settled charges themselves are in the
current and historic BSUoS run files (@./current-balancing-services-use-of-system-bsuos-data.md),
which are a separate package.

The capture holds 17 rows. gridflow has a silver output for it, but it is **held**: the evidence
does not establish when each publication was actually available (see Holds). The package is
still eligible and the silver exists on disk, but it may not be used for point-in-time models
yet. The site page shows the rows and a chart with a caveat naming this question (ruling 66).

- Publisher group: Balancing costs
- Registry group: balancing · archetype: TAR

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Balancing Services Use of System Charges (BSUoS) Tariffs | CSV | upload | `4dfa533f-bec6-491b-a3f1-7ce92449bc9a` |

The package has one resource, a CSV with disposition SILVER. It has no DOC or catalogue-only
resources and no `_files` family.

Download link and the one capture (2026-10-08, a CKAN upload resource). Size and CKAN
`last_modified` come from the capture sidecar under
`C:/gridflow-data/bronze/neso_data_portal/bsuos_fixed_tariffs/2026/10/08/`. Data rows equal the
silver rows.

| File | Bytes | Data rows | CKAN `last_modified` |
|---|---:|---:|---|
| [bsuos-fixed-tariffs-data-portal-new-header.csv](https://api.neso.energy/dataset/6c862622-48ff-4025-b998-d4d3db9e984d/resource/4dfa533f-bec6-491b-a3f1-7ce92449bc9a/download/bsuos-fixed-tariffs-data-portal-new-header.csv) | 1,179 | 17 | 2026-10-05T15:43:25.730825 |

Package page: [bsuos-fixed-tariffs](https://www.neso.energy/data-portal/bsuos-fixed-tariffs).

## Families

### `bsuos_fixed_tariffs`

- Kind: tabular · archetype: TAR · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Publication | `publication` | string | — | no | — | — |
| Fixed Tariff Title | `fixed_tariff_title` | string | — | no | — | — |
| Published Date | `published_date` | date | `%Y-%m-%d` | no | — | — |
| Fixed Tariff Start Date | `fixed_tariff_start_date` | date | `%Y-%m-%d` | no | — | — |
| Fixed Tariff End Date | `fixed_tariff_end_date` | date | `%Y-%m-%d` | no | — | — |
| Fixed Tariff_GBP per MWh | `fixed_tariff_gbp_per_mwh` | float64 | — | yes | — | £/MWh |

- Entity key: `publication`, `fixed_tariff_title`, `published_date`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`fixed_tariff_start_date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**One header epoch.** The record accepts one exact header, the six columns above. The vendor
renamed the rate column on 5 October 2026 ("Fixed Tariff £/MWh" became "Fixed Tariff_GBP per
MWh"; CKAN package `notes`), and the resource's `last_modified` (2026-10-05) is the day of that
change. The capture holds only the new header. `TODO: verify` whether earlier copies under the
old column name exist; none was captured.

**What the columns mean (vendor dictionary).** These descriptions come from NESO's saved field
info for the resource (gridflow
`@.planning/research/neso-snapshots/field-info/20261008T114228Z/bsuos_fixed_tariffs.json`).

- **`Publication`**: "States what publication type the tariff relates to". The vendor comment is
  "Final or Draft Tariff". The body also carries an `Initial Forecast` stage (3 distinct stage
  labels in the capture), which the comment does not list. `TODO: verify` the full list of
  stages and what each means.
- **`Fixed Tariff Title`**: "Name ascribed to a particular Fixed Tariff". The title names the
  tariff, and the capture holds 10 distinct titles. A title is repeated across stages, so a
  published version is identified by title together with stage and Published Date.
- **`Published Date`**: "Date tariffs were published". It is a calendar date, with no time of
  day and no zone.
- **`Fixed Tariff Start Date`**: "First settlement date the tariff relates to".
- **`Fixed Tariff End Date`**: "Final settlement date the tariff relates to". The end date is
  inclusive (it is the final settlement date, not the day after).
- **`Fixed Tariff_GBP per MWh`**: "BSUoS Tariff in £/MWh".

**Units (vendor dictionary only).** The tariff column's dictionary `unit` field is **£/MWh**.
The date and text columns have an empty unit field, so the skeleton's Vendor unit column is `—`
for them. No unit is inferred from a column name. Values are stored as delivered.

**Two clocks.**

1. **Vintage (`ckan_last_modified`).** `published_at` is the CKAN `last_modified` of the
   captured file, read as UTC (ADR-030). `available_at` equals `published_at`. In silver
   (2026-10-10) all 17 rows share one `published_at`, 2026-10-05T15:43:25.730825Z, equal to the
   sidecar's `ckan_last_modified`, and `available_at = published_at` on every row. The capture
   was written on 2026-10-08, three days later. Only one capture exists, so an as-of query
   before 2026-10-05T15:43 sees **no** rows. The `last_modified` predates the capture, so
   `available_at <= as_of` does not prove that the bytes gridflow holds are the ones NESO
   published at that instant (ADR-039 FM-12, accepted residual). The vendor's per-row
   Published Date is **not** used as `available_at`.
2. **Event time (temporal recipe `date_sp1` on `fixed_tariff_start_date`).** `timestamp_utc`
   and `event_time` are the engine's settlement-day storage anchor for the tariff's **start
   date**, which gridflow computes from the date. They are a storage convention, not a vendor
   measurement instant. The end date does not enter the recipe; it stays a typed date column.
   NESO documents no time zone or day boundary for these dates beyond "settlement date", so
   gridflow makes no further instant from them (ADR-036). `Published Date` is a publication
   date only, and gridflow does **not** turn it into a midnight-UTC issue instant. The record's
   issue recipe is `none`.

**Identity and selection (ADR-039).**

- The **measured grain** is `(publication, fixed_tariff_title, published_date)`. All 17 rows
  are distinct on it, in the captured body and in silver (2026-10-10). The rate is a measure,
  not part of identity.
- The vendor publishes no key. `TODO: verify` a vendor-guaranteed unique key, and whether a
  published row can be revised in place.
- `_latest` is `whole_capture`: the newest complete capture, not a per-key latest. gridflow
  does not claim a vendor-certified revision key.

**Sentinels and missing values (FACTS g5).** The full-body scans found no blanks, `NA`/`N/A`,
numeric `-1`, thousands separators or currency symbols in the value column, and no numeric cast
failures. The record declares no null tokens. Silver has 0 nulls in every column (2026-10-10),
although the rate column is declared nullable. Nothing is mapped to null.

**Row counts (silver, 2026-10-10).**

| Resource | Rows | Distinct on entity key |
|---|---:|---:|
| `4dfa533f-bec6-491b-a3f1-7ce92449bc9a` | 17 | 17 |

**Activation (2026-10-10, master `1ccb467`, PR #106).** The balancing-costs batch merged
triple-green (RULINGS 655). The family was transformed from the 2026-10-08 capture; there was
no prior silver, so nothing was overwritten (RULINGS 656). Silver has **17 rows**, equal to the
planned count, and the family is recorded as held. Reconcile `--all --cutoff 2026-10-10` exited
0 with 0 gaps over 122 families (gridflow `@.planning/v0.22-RESULTS.md` §BAL-1).

Silver layout: one Parquet file under
`C:/gridflow-data/silver/neso_data_portal/bsuos_fixed_tariffs/year=2026/month=10/`. The
`year=`/`month=` partition is the **capture** date, not the tariff date. Columns (14): the six
vendor columns, then `timestamp_utc`, `published_at`, `bronze_capture_id`,
`capture_written_at`, `event_time`, `available_at`, `source_run_id` and `dataset_version`. All
timestamps are tz-aware UTC. `dataset_version` is `1+e1` (record version 1, generic engine
version 1). No gold view or builder reads this family.

**Related package.** The settled BSUoS charge files from the same batch are described in
@./current-balancing-services-use-of-system-bsuos-data.md.

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Biannual

The vendor says updates come when tariffs are published, about every six months. The CKAN
`last_modified` of the single resource (2026-10-05) is consistent with a recent publication,
but it coincides with the column rename, so it does not prove a new tariff publication on that
date. `TODO: verify` the publication calendar, whether earlier publications are retained in the
file, and whether NESO revises a published row. Only more captures, compared pair by pair, can
show this. One capture exists to date (2026-10-08).

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `bsuos_fixed_tariffs`: held: TODO: precise issue clock and availability of each publication at its Published Date, and whether historical publication rows are immutable — 15 of 17 targets start on or before the capture vintage, so RULINGS 529's forward-target exception does not apply. (unit E-SEM)

The silver output exists on disk but is **held**. It may not be used for point-in-time models
until unit E-SEM answers the question above; the site shows its rows with a caveat (ruling 66). The hold sits in the record,
and RULINGS 653 set it when the batch was ruled.

**Why the usual shortcut fails.** Where every row in a forecast-style file targets a period
after the file's CKAN `last_modified`, gridflow lets the vintage stand in for the issue time
(RULINGS 529, forward-target exception). Here 15 of the 17 rows have a start date on or before
the vintage (2026-10-05), and only 2 start later. The file mixes `Final`, `Draft` and
`Initial Forecast` stages. The vintage of 2026-10-05 therefore cannot be read as the date each
row became known.

**What is not established.** The vendor gives a publication **date** but not the time of day,
and nothing shows when a given row first appeared on the portal. Nor is it shown that an old
row is never rewritten in place. gridflow will not manufacture a midnight-UTC issue time from
`Published Date` to fill the gap.

What settles it: an immutable, dated vendor publication history that shows when each row was
available, or an approved conservative publication-date availability recipe. Either is a
record edit once ruled.
