---
source: "neso_data_portal"
package: "dynamic-regulation-requirements"
dataset_key: "dr_requirements"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-18
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Dynamic Regulation requirements
  summary: >-
    NESO's latest view of the Dynamic Regulation it needs: MW for the low and high products in
    each EFA block.
  facts:
    vendor: "NESO Data Portal, package `dynamic-regulation-requirements`: one CSV file, no archive"
    cadence: "Ad hoc (NESO's catalogue); NESO publishes updates in the same file"
    grain: One row per EFA date and service, with six EFA block columns
  landscape: market
  what_it_is: >-
    Dynamic Regulation is a NESO frequency response service, with a low (`DRL`) and a high (`DRH`)
    product. NESO's file, titled Indicative DR Requirements and called its latest view, gives MW
    before overholding per EFA date for six EFA blocks. Blocks run on the UK clock from 23:00 the
    evening before; block 1 lasts 3 or 5 hours at clock changes.
  how_used:
    - Requirement per block against cleared `DRL` and `DRH` MW in NESO's EAC results.
    - To join EAC results, convert each block's UK start time to UTC.
    - "Point-in-time studies: each capture is one vintage, stamped with the file's `published_at`."
  chart:
    type: line
    silver: neso_data_portal/dr_requirements
    time: efa_date
    value: efa1
    group: service
    series_order: [DRH, DRL]
    filter:
      - {column: published_at, op: eq, value: "2026-09-22T14:48:17.409242"}
    aggregation: mean
    window: {start: "2026-09-23", end: "2026-10-31"}
    unit: MW
  chart_view:
    title: Dynamic Regulation requirement in EFA block 1, by date
    caption: >-
      Silver `dr_requirements`, MW before overholding: EFA block 1 (from 23:00 the evening before,
      UK time) per EFA date, 23 September to 31 October 2026, NESO's 22 September file. Every block
      on every date in the file is 480 MW.
    alt: >-
      Line chart of NESO's Dynamic Regulation requirement for EFA block 1 in MW, one point per EFA
      date from 23 September to 31 October 2026. Both lines are flat at 480 MW across all 39 dates
      and lie on top of each other: the high product, DRH, solid, and the low product, DRL, drawn
      dashed over it. Every block on every date in the file is also 480 MW.
    x_label: EFA date
    y_min: 0
    key:
      - {series: DRH, label: High product, codes: DRH, paint: petrol, note: "480 MW in every block, all 39 dates in this file; the low line runs along it."}
      - {series: DRL, label: Low product, codes: DRL, paint: clay, note: "480 MW in every block on all 39 dates, drawn dashed over the high line."}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then the file downloaded whole unless its
      `last_modified` is unchanged. Dates select nothing.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=dynamic-regulation-requirements"
      - "GET https://api.neso.energy/dataset/bcc9b338-00a4-4858-a1ed-0b7728048462/resource/d6c576b9-91d5-4c48-bf6d-300c7d7aa6ad/download/dr-requirements.csv"
    commands:
      - {run: gridflow ingest neso_data_portal dr_requirements --last 24h, comment: "whole file; window must end recently"}
      - {run: gridflow transform neso_data_portal dr_requirements --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: published_at, op: eq, value: "2026-09-22T14:48:17.409242"}
        - {column: efa_date, op: in, value: ["2026-09-23", "2026-10-25", "2026-10-26", "2026-10-31"]}
      order_by: [efa_date, service]
      columns: [efa_date, service, efa1, efa2, efa3, efa4, efa5, efa6, timestamp_utc, published_at]
    key: [efa_date, service]
    caption: "First and last dates; around 25 October's clock change `timestamp_utc` goes from 23:00 to 00:00 UTC."
    fields:
      efa_date: EFA date of the requirement; block 1 starts 23:00 UK time the evening before
      service: "`DRL` (low) or `DRH` (high); NESO's dictionary writes `DR-L` and `DR-H`"
      efa1: Block 1, 23:00 to 03:00 UK time, MW before overholding (NESO)
      efa2: Block 2, 03:00 to 07:00 UK time, MW before overholding (NESO)
      efa3: Block 3, 07:00 to 11:00 UK time, MW before overholding (NESO)
      efa4: Block 4, 11:00 to 15:00 UK time, MW before overholding (NESO)
      efa5: Block 5, 15:00 to 19:00 UK time, MW before overholding (NESO)
      efa6: Block 6, 19:00 to 23:00 UK time, MW before overholding (NESO)
      timestamp_utc: UK midnight starting calendar date `efa_date`, in UTC; block 1 starts an hour earlier
      published_at: "NESO's last-modified time for the whole file, read as UTC"
      bronze_capture_id: Path of the bronze capture the row was read from
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      Reads the `_latest` view, the newest capture, with `data.sql` so the cells see every date the
      file holds and show `published_at` in UTC; `query()` reads the same view but takes a date range.
    cells:
      - |
        df = data.sql("""
            SELECT efa_date, service, efa1, efa2, efa3, efa4, efa5, efa6,
                   published_at AT TIME ZONE 'UTC' AS published_utc
            FROM silver_neso_data_portal_dr_requirements_latest
            ORDER BY efa_date, service""")
        df.groupby("service").agg(
            first=("efa_date", "min"), last=("efa_date", "max"),
            dates=("efa_date", "count"), published_utc=("published_utc", "max")).reset_index()
      - |
        blocks = [f"efa{i}" for i in range(1, 7)]
        long = df.melt(["efa_date", "service"], blocks, var_name="block", value_name="mw")
        long.groupby("service").mw.agg(["min", "max", "count"]).reset_index()
      - |
        import pandas as pd
        n = long.block.str[3:].astype(int)
        local = long.efa_date + pd.to_timedelta(4 * n - 5, unit="h")
        long["start_utc"] = local.dt.tz_localize("Europe/London").dt.tz_convert("UTC")
        low = long[long.service.eq("DRL")].sort_values("start_utc")
        low["hours"] = low.start_utc.diff().shift(-1).dt.total_seconds() / 3600
        low[low.efa_date.eq("2026-10-25")][["efa_date", "block", "start_utc", "hours", "mw"]]
      - |
        wide = long.pivot_table(index="start_utc", columns="service", values="mw")
        wide[["DRH", "DRL"]].plot(
            drawstyle="steps-post", style=["-", "--"], color=["#155A6E", "#C77E3C"], lw=2,
            ylim=(0, 600), figsize=(8, 3.5), xlabel="EFA block start, UTC", ylabel="requirement, MW");
    needs: a capture of the requirement file
    plot_alt: >-
      Step plot of NESO's Dynamic Regulation requirement in MW at each EFA block start in UTC, from
      22:00 on 22 September to 19:00 on 31 October 2026. The high product, DRH (solid petrol), and
      the low product, DRL (dashed clay), both hold 480 MW throughout.
  related:
    - {dataset: neso_data_portal/eac-auction-results, note: "Cleared `DRL` and `DRH` MW and price for each EFA block"}
    - {dataset: neso_data_portal/dynamic-moderation-requirements, note: "The same requirement layout for Dynamic Moderation, `DML` and `DMH`"}
    - {dataset: neso_data_portal/long-term-forecasts-for-dc-dm-dr-requirements, note: "NESO's twelve-month outlook for this service, as weights over bands"}
    - {dataset: elexon/freq, note: The system frequency Dynamic Regulation responds to}
---

# Dynamic Regulation Requirements

Supported by National Energy SO Open Data

## Overview

NESO's indicative requirement, in megawatts, for the Dynamic Regulation (DR) frequency-response
service. The vendor describes the file as its latest view of the requirement, with any update
published into the same file. Each row is one EFA date and one product code (`DRL` low-frequency
side, `DRH` high-frequency side) and carries six wide columns, one per EFA block. The vendor
dictionary defines each value as the requirement for the service before overholding for that block.
Use it as a forward-looking procurement-volume signal for the DR market: how much DR capacity NESO
intends to buy per EFA block per day.

The package is a single CSV with a latest-view lifecycle. The vendor package notes read "This dataset
will contain our forecasted requirements for Dynamic Regulation." Update frequency is "Ad hoc". Only
one capture of the resource exists, so amendment-in-place and dropped-target behaviour are unmeasured
(see Known issues).

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: FC
- Sibling package with the identical layout: `dynamic-moderation-requirements` (family `dm_requirements`, product codes `DML`/`DMH`). Do not mix the two: the DM vendor dictionary wrongly describes DR services, and the DR dictionary is not affected.
- Related reading: @../README.md · @../coverage.md · @../endpoints.md

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Indicative DR Requirements | CSV | upload | `d6c576b9-91d5-4c48-bf6d-300c7d7aa6ad` |

There are no DOC, ingest-only, held or skipped resources in this package: it has exactly one resource
and it feeds silver.

- Indicative DR Requirements, `dr-requirements.csv` (SILVER, family `dr_requirements`): [download](https://api.neso.energy/dataset/bcc9b338-00a4-4858-a1ed-0b7728048462/resource/d6c576b9-91d5-4c48-bf6d-300c7d7aa6ad/download/dr-requirements.csv). Vendor description: "This dataset provides our latest view of our requirements for the Dynamic Regulation Service, any updates to our requirements will be published here."
- Package id `bcc9b338-00a4-4858-a1ed-0b7728048462`. CKAN `url_type` is `upload`, so the CKAN `last_modified` is the file vintage (ADR-035).

## Families

### `dr_requirements`

- Kind: tabular · archetype: FC · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| EFA_DATE | `efa_date` | date | `%d/%m/%Y` | no | — | — |
| Service | `service` | string | — | no | — | — |
| EFA1 | `efa1` | float64 | — | yes | — | MW |
| EFA2 | `efa2` | float64 | — | yes | — | MW |
| EFA3 | `efa3` | float64 | — | yes | — | MW |
| EFA4 | `efa4` | float64 | — | yes | — | MW |
| EFA5 | `efa5` | float64 | — | yes | — | MW |
| EFA6 | `efa6` | float64 | — | yes | — | MW |

- Entity key: `efa_date`, `service`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`efa_date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

#### Two clocks

- **Vintage (`published_at` / `available_at`)**: the CKAN `last_modified` of the captured file. The captured body has `last_modified` 2026-09-22T14:48:17.409242, read as UTC, so every row of that capture has `available_at` = 2026-09-22 14:48:17.409242 UTC. The file carries no issue or production column, so the issue recipe is `none` and no creation date is promoted to a publication instant.
- **Event time (`event_time` and `timestamp_utc`)**: `date_sp1(efa_date)`. This is a **calendar-date storage anchor**: the UK settlement-period-one start of `efa_date`, converted to UTC. For example `efa_date` 2026-09-23 (BST) gives 2026-09-22 23:00 UTC. It is **not** the start of EFA block 1 (which starts 23:00 UK local on the previous date) and not the start of any other block. Do not read `timestamp_utc` as a service-delivery instant.

The engine cannot compose a date plus an EFA block label into a row-specific instant (RULINGS 572/588), so the six EFA columns stay wide and uncomposed. A consumer that needs block instants builds them from the vendor's local-clock boundaries below.

#### Column semantics

- `efa_date`: the EFA date the requirement is for (vendor dictionary: "EFA Date the requirement is for"; dictionary example `16/02/2022`). Parsed day-first with `%d/%m/%Y`. All 78 captured values are consistent with that format and span 2026-09-23 to 2026-10-31.
- `service`: the product code, stored byte-equal to the body: `DRL` (Dynamic Regulation Low) and `DRH` (Dynamic Regulation High). The vendor dictionary field description uses hyphenated forms (`DR-L`, `DR-H`, example `DR-L`); the body uses the compact forms and NESO's EAC product list supports the compact spellings. The compact codes are stored as-is and never normalised.
- `efa1`..`efa6`: the requirement for the service before overholding, in **MW** (vendor dictionary unit, every column). The columns are blocks, wide.
- EFA block boundaries, UK local clock (vendor boundaries as cited in the research; the DC history dictionary and NESO EAC guidance Appendix B): EFA 1 = 23:00 on the previous date to 03:00; EFA 2 = 03:00-07:00; EFA 3 = 07:00-11:00; EFA 4 = 11:00-15:00; EFA 5 = 15:00-19:00; EFA 6 = 19:00-23:00. On clock-change days the day has 23 or 25 elapsed hours and EFA 1 has 3 or 5.
- Sentinels: none. The body has no blank cells, no `-1`, `N/A`, `NA`, `NULL`, `NaN` tokens, no padded cells, no thousands separators and no percent signs; no trim or token map is applied. A leading UTF-8 BOM is present and is handled by the CSV reader.

#### Captured data and silver output

| Fact | Value |
|---|---|
| Captured body | `dr_requirements/2026/10/08/raw_20261008T101008Z_d6c576b9-91d5-4c48-bf6d-300c7d7aa6ad_c58dfc4d.csv`, 3,171 bytes, 78 rows, sha256 prefix `c58dfc4d` |
| `ckan_last_modified` | 2026-09-22T14:48:17.409242 |
| Capture time (`written_at`) | 2026-10-08T10:10:08.916643 UTC |
| Silver rows | 78 (activation 2026-10-13, RULINGS 725; no prior silver, no snapshot needed); equals the spec plan |
| `efa_date` range | 2026-09-23 to 2026-10-31 (39 dates x 2 product codes) |
| Silver dataset version | `1+e1` |
| Validation failures / blank rows excluded | 0 / 0 |

Eligibility: this family is **eligible**. The forward-only test passes: all 78 target-date rows and all 468 EFA block starts are after the capture's `ckan_last_modified`, so vintage `ckan_last_modified` is a sound availability clock for this body.

Values: every one of the 468 requirement cells in the captured body is 480.0 MW (all six columns, both product codes, all dates). A constant requirement across the window is what the vendor published; it is not an artefact of the pipeline.

Silver sample (first rows, abridged to the data columns; the clock and lineage columns are as above):

| `efa_date` | `service` | `efa1` | `efa2` | `efa3` | `efa4` | `efa5` | `efa6` | `event_time` (UTC) | `available_at` (UTC) |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-23 | DRL | 480.0 | 480.0 | 480.0 | 480.0 | 480.0 | 480.0 | 2026-09-22 23:00 | 2026-09-22 14:48:17.409242 |
| 2026-09-23 | DRH | 480.0 | 480.0 | 480.0 | 480.0 | 480.0 | 480.0 | 2026-09-22 23:00 | 2026-09-22 14:48:17.409242 |

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc
- Lifecycle: latest-view resource. Updates replace the published view rather than appending history. gridflow keeps each complete capture (`whole_capture`); how a later capture amends or drops earlier targets is not yet measured.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

## Known issues and open questions

- TODO: verify amendment-in-place and dropped-target behaviour. Only one capture of this resource exists (3,171 bytes, hash-pinned); settle by comparing a later complete capture against it.
- TODO: verify the vendor's uniqueness and revision identity for `(efa_date, service)`. The key is a measured duplicate guard (78 distinct keys, zero duplicate excess rows), not a vendor-declared primary key.
- TODO: verify a vendor statement of when each requirement revision is published. The only clock is the CKAN `last_modified` of the upload; a later capture will carry a later vintage for the same targets, and the page makes no claim about the vendor's own revision times.
- Product-code spelling: the dictionary uses `DR-L`/`DR-H`, the body uses `DRL`/`DRH`. Both denote the same low/high products; the body spelling is kept literally. The sibling long-term family spells one code `DR_L`, a separate unresolved vendor question that does not apply to this family.
- DM versus DR: the copied DM dictionary text describes DR services. Never use it to relabel `dm_requirements` rows as DR, and never use this family's `DRL`/`DRH` rows as DM.

## Holds

- none. This family is eligible and no output is held. Row counts, schema and values are published.
