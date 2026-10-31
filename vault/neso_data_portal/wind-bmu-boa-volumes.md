---
source: "neso_data_portal"
package: "wind-bmu-boa-volumes"
dataset_key: "wind_bmu_boa_volumes"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Wind bid-offer acceptance volumes
  summary: >-
    NESO's volumes of bid-offer acceptances (BOAs) on wind balancing mechanism (BM) units, in MW,
    by settlement period and financial year.
  facts:
    vendor: "NESO Data Portal, package Wind BOA Volumes: nine yearly CSV files"
    cadence: "Daily, NESO says"
    grain: "Each row: a BM unit, date, settlement period and volume"
    history: "Financial years 2018/19 to 2026/27, April to March, NESO lists"
  landscape: market
  what_it_is: >-
    Each row gives a BM unit, date, settlement period and `BOA_Volume` in MW, which NESO defines as
    generation a BOA curtailed, negative because it cuts the wind farm's output. NESO's wind
    incentive forecasts use these units. As fetched on 8 and 16 October 2026, some yearly files
    repeat rows, whole or by unit and period, and 2026/27 holds positive volumes.
  how_used:
    - "Wind curtailment per BM unit and half hour through the Balancing Mechanism"
    - "Accepted wind reductions set against wind forecasts and metered wind output"
  chart:
    type: bar
    silver: neso_data_portal/wind_bmu_boa_volumes
    group: resource_id
    group_map:
      "b8670a89-36cd-4a19-b00d-2129ab15d3b2": fy2020
      "094ad551-630a-4302-b259-800a27122cfb": fy2021
      "62da8915-4b87-4d77-a8f5-89084de1830d": fy2022
      "1edaa5fe-86fe-41b4-95b9-55e9ec45fab0": fy2023
      "7bf83942-3590-4fe5-9980-49a9546e30a9": fy2025
      "45598dcd-ea9c-4911-95f2-7946c5f3b034": fy2026
    dedup: {"on": [resource_id, date, settlement_period, generator_name], order_by: published_at}
    aggregation: count
    sort: label
    unit: unit half-hours
  chart_view:
    title: Wind unit half-hours with a BOA volume, by yearly file
    caption: >-
      Silver `wind_bmu_boa_volumes`: BM unit half-hours with at least one row, per yearly file; a unit
      and half-hour listed twice counts once. 2018/19, 2019/20 and 2024/25 repeat whole rows, so have
      no rows here.
    alt: >-
      Horizontal bar chart from neso_data_portal/wind_bmu_boa_volumes counting wind BM unit
      half-hours with a BOA volume in each yearly file: 113,023 in 2020/21, 90,561 in 2021/22,
      106,617 in 2022/23, 171,867 in 2023/24, 276,413 in 2025/26 and 160,485 in the part-year
      2026/27 file, to 16 October 2026. There are no 2018/19, 2019/20 or 2024/25 bars.
    key:
      - {series: fy2020, label: 2020/21 file, paint: petrol}
      - {series: fy2021, label: 2021/22 file, paint: petrol}
      - {series: fy2022, label: 2022/23 file, paint: petrol}
      - {series: fy2023, label: 2023/24 file, paint: petrol}
      - {series: fy2025, label: 2025/26 file, paint: petrol, note: "NESO's file runs to 29 March 2026"}
      - {series: fy2026, label: 2026/27 file, paint: hatch-lines,
         note: "Part year: NESO's file of 16 October 2026, with its positive volumes"}
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show`, then nine yearly CSVs, downloaded whole unless
      `last_modified` is unchanged. Shown: first, current and 2024/25. The transform rejects 2018/19,
      2019/20 and 2024/25 (repeated rows).
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=wind-bmu-boa-volumes"
      - "GET https://api.neso.energy/dataset/102638b9-6214-4db6-9115-86b5e879d1ce/resource/28183033-4464-4b3a-a0ff-0efdc5cd6c7a/download/boa_data_2018_19.csv"
      - "GET https://api.neso.energy/dataset/102638b9-6214-4db6-9115-86b5e879d1ce/resource/d3fbf6c1-7688-4486-8716-b5af0c895a5a/download/boa_data_2024_25.csv"
      - "GET https://api.neso.energy/dataset/102638b9-6214-4db6-9115-86b5e879d1ce/resource/45598dcd-ea9c-4911-95f2-7946c5f3b034/download/boa_data_2026_27.csv"
    commands:
      - {run: gridflow ingest neso_data_portal wind_bmu_boa_volumes --last 24h, comment: "each changed yearly file to bronze"}
      - {run: gridflow transform neso_data_portal wind_bmu_boa_volumes --last 24h, comment: "the clean yearly files to silver"}
  record:
    select:
      filter:
        - {column: generator_name, op: eq, value: NNGAO-1}
        - {column: date, op: eq, value: "2025-04-04"}
        - {column: settlement_period, op: ge, value: 4}
        - {column: settlement_period, op: le, value: 8}
      order_by: [settlement_period, boa_volume]
      columns: [date, settlement_period, generator_name, boa_volume, generator_full_name, resource_id]
    key: [resource_id, date, settlement_period, generator_name, boa_volume]
    caption: "One unit on 4 April 2025: periods 5 to 7 each listed twice, with different volumes."
    fields:
      resource_id: NESO's id for the yearly file the row came from
      date: The UK settlement date
      settlement_period: "Half-hour of the UK settlement day, from 1"
      generator_name: The wind BM unit, as NESO writes it
      boa_volume: "NESO's `BOA_Volume`, MW: generation a BOA curtailed, negative, its dictionary says"
      generator_full_name: The wind farm's name, as NESO writes it
      published_at: "NESO's last-modified time for the yearly file, read as UTC"
      timestamp_utc: "Start of the settlement period, UTC, from `date` and `settlement_period`"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  caveat: "NESO does not explain rows repeating a unit and half-hour, or 2026/27's positive volumes."
  notebook:
    lead: >-
      `query()` filters `date` on the `_latest` view, the newest capture of each yearly file, lineage
      columns dropped. The second cell counts each file's rows, positive volumes and repeated unit
      half-hours.
    cells:
      - |
        import pandas as pd
        df = data.neso_data_portal.query("wind_bmu_boa_volumes", "2025-04-01", "2026-10-16")
        df = df.sort_values(["date", "settlement_period", "generator_name"], ignore_index=True)
        df[["date", "settlement_period", "generator_name", "boa_volume", "resource_id"]].head()
      - |
        key = ["date", "settlement_period", "generator_name"]
        files = df.groupby("resource_id").agg(first=("date", "min"), last=("date", "max"),
                                              rows=("boa_volume", "size"),
                                              positive=("boa_volume", lambda v: int((v > 0).sum())))
        files["repeats"] = df[df.duplicated(key)].groupby("resource_id").size()
        files.fillna({"repeats": 0}).astype({"repeats": int})
      - |
        per_day = df.drop_duplicates(key).groupby("date").size()
        per_day.index = pd.to_datetime(per_day.index)
        ax = per_day.asfreq("D").plot(color="#155A6E", figsize=(8, 3.5), xlabel="settlement date",
                                      ylabel="unit half-hours with a volume");
    needs: NESO's 2025/26 and 2026/27 wind BOA volume files
    plot_alt: >-
      Line plot of wind BM unit half-hours with a BOA volume per settlement date, 1 April 2025 to
      16 October 2026, each unit and half-hour counted once: from 1 to 3,590 a day, median 546,
      highest on 14 October 2026; 41 dates with no rows break the line.
  related:
    - {dataset: elexon/boal, note: "Elexon's record of each accepted bid and offer, by BM unit"}
    - {dataset: neso_data_portal/monthly-operational-metered-wind-output, note: "NESO's metered wind output by half hour, beside the curtailed volumes"}
    - {dataset: elexon/bmunits_reference, note: "Elexon's unit register; most of these names match its National Grid IDs"}
---

# Wind BOA Volumes

## Overview

NESO publishes, per BMU, the volume of Balancing Mechanism bid-offer acceptances (BOAs) taken on the wind farms whose BM units feed NESO's wind incentive forecasts. The catalogue describes each resource as "the volume of all BOAs taken on the BMU wind farms used in our wind incentive forecasts" for one April-to-March financial year. Each row is a BMU, a settlement date, a settlement period and one `BOA_Volume`. In market terms it is the record of when and by how much NESO instructed wind farms to change output through the Balancing Mechanism, which makes it a source for wind curtailment, constraint-driven output loss, and the gap between a wind forecast and what the system actually accepted.

The package is **eligible** at the package level (all nine resources are routed to silver) but its single family is **held**. NESO does not explain what a repeated identical row means, so the identity of a row (one acceptance, one contribution to a period total, or a duplicate) is unknown; the 2026/27 file also carries positive volumes against the vendor dictionary's description of the field as curtailed (negative) generation. gridflow therefore loads the six archives that pass its duplicate guard, keeps the three that fail as unloaded failed captures with committed adjudications, and keeps the family out of point-in-time model use until NESO answers the hold question below (see Holds). Under ruling 66 (2026-10-24) the site page shows the loaded rows, a count chart and a notebook, with the question as a caveat.

- Publisher group: Generation
- Registry group: generation · archetype: SER
- Package id: `102638b9-6214-4db6-9115-86b5e879d1ce`
- Domain notes: @../../../20-domain/concepts/settlement-period.md, @../../../20-domain/markets/gb-balancing-mechanism.md, @../../../20-domain/concepts/bm-units.md
- Related vendor page (Elexon acceptances): @../../elexon/datasets/boal.md

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Wind BOA Volumes 2018/19 | CSV | upload | `28183033-4464-4b3a-a0ff-0efdc5cd6c7a` |
| Wind BOA Volumes 2019/20 | CSV | upload | `6ef6f5f2-2852-4f66-931c-29f8e5b46ddf` |
| Wind BOA Volumes 2020/21 | CSV | upload | `b8670a89-36cd-4a19-b00d-2129ab15d3b2` |
| Wind BOA Volumes 2021/22 | CSV | upload | `094ad551-630a-4302-b259-800a27122cfb` |
| Wind BOA Volumes 2022/23 | CSV | upload | `62da8915-4b87-4d77-a8f5-89084de1830d` |
| Wind BOA Volumes 2023/24 | CSV | upload | `1edaa5fe-86fe-41b4-95b9-55e9ec45fab0` |
| Wind BOA Volumes 2024/25 | CSV | upload | `d3fbf6c1-7688-4486-8716-b5af0c895a5a` |
| Wind BOA Volumes 2025/26 | CSV | upload | `7bf83942-3590-4fe5-9980-49a9546e30a9` |
| Wind BOA Volumes 2026/27 | CSV | upload | `45598dcd-ea9c-4911-95f2-7946c5f3b034` |

### Resource dispositions and load status

All nine resources have registry disposition `SILVER` into the one family `wind_bmu_boa_volumes`. There are no `COVERED`, `DOC`, `GIS` or `HOLD` resources and no supplemental document files in this package. Every resource is an `upload` (a stored file), not a datastore dump; the header is identical across all nine (one schema epoch) and every date matches `%Y-%m-%d`, so no per-filename format map is needed.

Download links are the CKAN snapshot URLs. The vintage is the CKAN `last_modified` of the capture that was loaded (bronze capture written 2026-10-08).

| Financial year | Download | Vintage (`ckan_last_modified`) | Bronze rows | Load status |
|---|---|---|---|---|
| 2018/19 (B01) | [boa_data_2018_19.csv](https://api.neso.energy/dataset/102638b9-6214-4db6-9115-86b5e879d1ce/resource/28183033-4464-4b3a-a0ff-0efdc5cd6c7a/download/boa_data_2018_19.csv) | 2026-08-10T14:49:13.976357 | 73,220 | **Not loaded.** Failed `DuplicateEntityKeyError`; adjudicated (ruling 547) |
| 2019/20 (B02) | [boa_data_2019_20.csv](https://api.neso.energy/dataset/102638b9-6214-4db6-9115-86b5e879d1ce/resource/6ef6f5f2-2852-4f66-931c-29f8e5b46ddf/download/boa_data_2019_20.csv) | 2026-08-10T14:50:20.869485 | 85,093 | **Not loaded.** Failed `DuplicateEntityKeyError`; adjudicated (ruling 547) |
| 2020/21 (B03) | [boa_data_2020_21.csv](https://api.neso.energy/dataset/102638b9-6214-4db6-9115-86b5e879d1ce/resource/b8670a89-36cd-4a19-b00d-2129ab15d3b2/download/boa_data_2020_21.csv) | 2026-08-10T14:51:37.793755 | 113,267 | Loaded, 113,267 silver rows |
| 2021/22 (B04) | [boa_data_2021_22.csv](https://api.neso.energy/dataset/102638b9-6214-4db6-9115-86b5e879d1ce/resource/094ad551-630a-4302-b259-800a27122cfb/download/boa_data_2021_22.csv) | 2026-08-10T14:52:41.781468 | 90,570 | Loaded, 90,570 silver rows |
| 2022/23 (B05) | [boa_data_2022_23.csv](https://api.neso.energy/dataset/102638b9-6214-4db6-9115-86b5e879d1ce/resource/62da8915-4b87-4d77-a8f5-89084de1830d/download/boa_data_2022_23.csv) | 2026-08-10T14:53:53.634728 | 106,620 | Loaded, 106,620 silver rows |
| 2023/24 (B06) | [boa_data_2023_24.csv](https://api.neso.energy/dataset/102638b9-6214-4db6-9115-86b5e879d1ce/resource/1edaa5fe-86fe-41b4-95b9-55e9ec45fab0/download/boa_data_2023_24.csv) | 2026-08-10T14:55:40.154160 | 171,952 | Loaded, 171,952 silver rows |
| 2024/25 (B07) | [boa_data_2024_25.csv](https://api.neso.energy/dataset/102638b9-6214-4db6-9115-86b5e879d1ce/resource/d3fbf6c1-7688-4486-8716-b5af0c895a5a/download/boa_data_2024_25.csv) | 2026-08-10T14:58:05.288334 | 251,296 | **Not loaded.** Failed `DuplicateEntityKeyError`; adjudicated (ruling 547) |
| 2025/26 (B08) | [boa_data_2025_26.csv](https://api.neso.energy/dataset/102638b9-6214-4db6-9115-86b5e879d1ce/resource/7bf83942-3590-4fe5-9980-49a9546e30a9/download/boa_data_2025_26.csv) | 2026-05-28T09:03:25.895718 | 277,345 | Loaded, 277,345 silver rows |
| 2026/27 (B09) | [boa_data_2026_27.csv](https://api.neso.energy/dataset/102638b9-6214-4db6-9115-86b5e879d1ce/resource/45598dcd-ea9c-4911-95f2-7946c5f3b034/download/boa_data_2026_27.csv) | 2026-10-08T09:00:15.469647 | 144,486 | Loaded, 144,486 silver rows |

Activation receipt (RESULTS `GEN-2H`, ruling 558, cutoff 2026-10-08, no prior silver): **904,240** silver rows over the **6 clean resources** (B03 to B06, B08, B09), matching the plan. The three failed resources wrote failure records and no completion marker, as designed; the dataset transform exits 1 for that reason, which is expected and adjudicated, not a fault to clear. The six loaded counts sum to 904,240.

The snapshot's `last_modified` for the 2026/27 file is earlier than the loaded vintage because the file is updated daily and the capture was taken later.

**Second capture of 2026/27 (measured 2026-10-24).** A refresh on 2026-10-16 recaptured only the 2026/27 file (`raw_20261016T204821Z_45598dcd-..._e3f8bac0.csv`, `last_modified` `2026-10-16T09:00:18.236752`, 160,485 rows, dates 2026-04-01 to 2026-10-16); the eight other files carried an unchanged `last_modified` and were skipped. Its rows dated before 2026-10-08 are identical, as a multiset, to the first capture's 144,399 such rows, so between the two captures NESO only appended. It still has no whole-row or (`Date`, `Settlement_Period`, `Generator_Name`) repeats, and 1,125 positive volumes (dates 2026-04-01 to 2026-10-16, 34 identifiers) against 1,044 in the first. Silver holds both 2026/27 captures (144,486 and 160,485 rows); `_latest` per `resource_id` takes the 2026-10-16 one, so the clean resources now give 920,239 latest rows. The closed years each still have one capture.

## Families

### `wind_bmu_boa_volumes`

- Kind: tabular · archetype: SER · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Date | `date` | date | `%Y-%m-%d` | no | — | ISO 8601 |
| Settlement_Period | `settlement_period` | int64 | — | no | — | — |
| Generator_Name | `generator_name` | string | — | yes | — | — |
| Generator_Full_Name | `generator_full_name` | string | — | yes | — | — |
| BOA_Volume | `boa_volume` | float64 | — | yes | — | MW |

- Entity key: `resource_id`, `date`, `settlement_period`, `generator_name`, `boa_volume`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: sp_pair (`date`, `settlement_period`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

### Silver columns added by the engine

Besides the five vendor columns, each silver row carries the engine's provenance columns: `resource_id` (CKAN resource id of the financial-year archive), `timestamp_utc`, `event_time`, `published_at`, `available_at`, `bronze_capture_id` (repo-relative path of the bronze file), `capture_written_at`, `source_run_id` and `dataset_version` (format `<record version>+e<epoch>`, currently `1+e1`). Silver is Parquet under `year=YYYY/month=MM/` of the transform run, not of the event date: all current files sit under `year=2026/month=10`, one file per resource per run. No column is null in the loaded silver.

### The two clocks

| Clock | Value | How it is derived |
|---|---|---|
| Vintage (when the bytes became available) | `published_at` = `available_at` = CKAN `last_modified` of the captured file | ADR-030; one value per resource capture. NESO has no per-row issue or revision stamp, so the record's issue is `none`. |
| Event time (what the row describes) | `event_time` = `timestamp_utc` = beginning of the settlement period | The `sp_pair` recipe turns (`date`, `settlement_period`) into the UTC start of that half hour on the UK settlement day. |

Event time. `timestamp_utc` is not the capture time here (that is the `none` recipe used by other NESO families); it is the period beginning. The mapping assumes NESO's GMT/BST settlement-day convention (an inference from NESO's settlement documentation, high confidence): period 1 of an ordinary BST day begins at 23:00 UTC the previous evening, and short and long clock-change days run 46 and 50 periods. The silver check `event_time == timestamp_utc` holds on every row. See @../../../20-domain/concepts/settlement-period.md.

Vintage. The data is as-of the CKAN modification time, not the time the underlying acceptance happened or was first published. The archive `last_modified` stamps (2026-05-28 and 2026-08-10 for the closed years) are months or years after the periods they describe, so they do not establish when each row was originally available. A point-in-time query with `available_at <= :as_of` will therefore see no historical BOA data before 2026-05-28. Do not use the target date or acceptance date as a publication time.

## Units, signs and sentinels

- **`BOA_Volume`**: vendor dictionary unit **MW**, described as curtailed generation, with negative values explained as reduced wind-farm output. Keep it in MW; the name contains "volume" but it is not relabelled MWh. The dictionary does not give a row-aggregation algorithm (it does not say whether a row is one acceptance or part of a period total), and the general NESO balancing-volume dictionary's bid/offer convention is not enough to settle it.
- **`Settlement_Period`**: an interval index, not a physical quantity; blank unit is expected. Allowed range is 1 to 50 (46 on the short clock-change day, 50 on the long one; a vendor dictionary comment of 48 periods for the sibling metered-wind family is incomplete for clock-change days, and periods above 48 are valid). No row in any of the nine archives exceeds its UK day's expected interval count.
- **Sentinels**: the vendor defines none. Observed bodies contain no blank populated rows, no `N/A` or `NA` tokens and no zero volumes. A numeric `-1` does occur among the volumes (some written with decimals); because no primary source says `-1` marks a missing value, it is retained as an ordinary signed numeric reading. Do not null it out.
- **Signs are preserved as published.** Do not negate, take absolute values, discard positive values or label every row curtailed output. Identifiers (`Generator_Name`) are stored as-is, no normalisation.
- **Regions**: the file has no region, zone or area column; none may be inferred.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Daily
- Resources are split by financial year; only the current-year archive (2026/27) changes regularly. Closed years were last modified 2026-05-28 and 2026-08-10. Whether NESO revises closed years is `TODO: verify (no revision history observed; only one capture of each closed year exists locally, and the 2026/27 file's two captures, 2026-10-08 and 2026-10-16, show appends only)`.
- Historic depth: the 2018/19 file begins in April 2018.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

## Holds

- `wind_bmu_boa_volumes`: held: TODO: NESO does not explain whole repeated rows (the 2018/19, 2019/20 and 2024/25 files repeat 21 rows on every column; 2,396 rows repeat date, period and generator), so a row's identity (one acceptance, one contribution or a duplicate) is unknown and the key carries boa_volume; the 2026/27 file also carries 1,044 positive volumes against the dictionary's negative-curtailment definition. (unit E-SEM)

### What the hold means

- **Hold unit: E-SEM** (an open data-semantics question for the vendor). Two questions, both for NESO:
  1. **Row grain (`B-ROW-GRAIN`).** What does a repeated identical BOA row mean: separate acceptances, separate contributions to a period total, or duplication? Can NESO publish an acceptance identifier or a corrected unique export?
  2. **Positive values (`B-POSITIVE-SEMANTICS`).** What do positive `BOA_Volume` values in the current-year file mean (offers, corrections, or another quantity) given the dictionary's negative-curtailment definition? (The registry's 1,044 is the 2026-10-08 capture; the 2026-10-16 capture has 1,125, the earlier 1,044 unchanged.)
- **Held means no model use.** No gold view or model feature is derived from this family. Under ruling 66 (2026-10-24) the site page shows eight loaded rows, a chart counting unit half-hours per yearly file (a unit and half-hour listed twice counts once, so no BMU-period total is taken) and a notebook, with the question as a caveat.
- **Why no lossless key exists.** No combination of vendor columns identifies every historical row uniquely. The profiler's every-column identity still has repeats, adding `Generator_Full_Name` does not separate them, and a resource id cannot resolve repeats inside one resource. The registry key therefore carries `boa_volume`, which is value-based identity chosen to load the clean archives, not a statement that the volume identifies the row. gridflow does not sum, drop duplicates, pick the last row or invent an occurrence index.
- **Repeats also exist in the loaded archives.** The excess-row counts on (`Date`, `Settlement_Period`, `Generator_Name`) are 44, 290 and 789 in the three failed archives (B01, B02, B07) and 244, 9, 3, 85 and 932 in B03, B04, B05, B06 and B08 respectively; B09 has none. The loaded archives pass the guard only because their repeats differ in `BOA_Volume`. A consumer must therefore not assume one row per BMU, date and period even in loaded silver, and must not take a BMU-period total without the vendor answer to the grain question.
- **Cross-resource overlap**: the nine archives share no (`Date`, `Settlement_Period`, `Generator_Name`) key across resources, so partitioned `whole_capture` retention by `resource_id` is safe for year coverage.

### Reconcile adjudication (ADR-040, ruling 547)

The three failed captures are recorded in the committed ledger `_reconcile_adjudications.json` as `failed` gaps with cause `DuplicateEntityKeyError`, one entry covering exactly these bronze captures (2026-10-08): B01 (2018/19), B02 (2019/20) and B07 (2024/25). The ledger asks NESO the row-meaning question and states the reason; it never alters data. Adjudicated is not clean: reconcile reports these in their own bucket, beside (not inside) open gaps, and an adjudication that stops matching a live gap (for example NESO publishes a fixed file and a new capture succeeds) is itself reported as a stale-adjudication gap. A new failure of the same kind on another capture is not covered. Reconcile `--all --cutoff 2026-10-08` (ruling 558): exit 0, 58 families, 0 open gaps, 5 adjudicated gaps in total (the metered-wind overlap, covered on its own page, plus these three failed BOA captures), 0 stale adjudications.

When NESO answers, expected path: obtain a vendor identity or corrected file, re-profile, replace the key, lift the hold, then re-capture and re-transform B01, B02 and B07 (their adjudication goes stale and must be removed in the same change).

## Cross-checks and gotchas

- **Identifier namespace.** `Generator_Name` values are in Elexon's National Grid BMU namespace: 208 of the 209 distinct identifiers across all nine archives match `national_grid_bm_unit` in the local Elexon BM unit reference, and none match Elexon's `bm_unit_id`. The one unmatched identifier is `CAIRW-1`. This is measured namespace evidence only; the reference may not cover every historical or future unit. Identifiers are stored unmodified.
- **Acceptance-key overlap with Elexon.** Against local `elexon/boal` (settlement dates 2026-08-01 to 2026-09-22, 16 distinct dates), 15,071 of 16,270 NESO unit/period keys in the 2026/27 file in that window match an Elexon BOAL unit/period, covering 128 identifiers. This shows the two sources describe the same acceptances at key level only.
- **`TODO: verify B-ELEXON-VOLUME-AGREEMENT`**: Elexon BOAL silver carries acceptance identifiers, times, flags and bid/offer levels but no accepted MW or MWh volume, so numerical agreement with `BOA_Volume` cannot be tested and no vendor transformation from Elexon fields to the NESO quantity is documented. Do not treat bid/offer levels as volumes.
- **Sparse by design.** A row exists only when a BOA applied; missing periods are not evidence of a wrong calendar or missing data. On long clock-change days periods up to 50 occur (for example 2020-10-25) and on short days up to 46; because the data is sparse, not every period appears.
- **Package eligibility vs family hold.** Front matter and the eligibility report mark the package `eligible` because every resource routes to silver; the family-level hold is what controls publication.
- **Large file.** Bronze bodies total about 53 MB (largest about 11 MB); the registry download cap is 512 MiB.

## Bronze and silver layout

- Bronze: `bronze/neso_data_portal/wind_bmu_boa_volumes/YYYY/MM/DD/raw_<stamp>_<resource_id>_<hash>.csv`, raw CSV as received, immutable; one file per resource per capture, with a JSON sidecar recording the capture URL and `last_modified`.
- Silver: Parquet at `silver/neso_data_portal/wind_bmu_boa_volumes/year=YYYY/month=MM/` (data root `C:\gridflow-data`), one file per resource per transform run, written with the engine's `whole_capture` selection per `resource_id`.
- Gold: none implemented; the family is held.

## Modelling notes

`TODO`. Not designed and not permitted while the hold stands. Intended use once released: a wind curtailment signal at BMU and half-hour grain, joined to NESO wind forecasts and metered wind output (see @monthly-operational-metered-wind-output.md) and to Elexon acceptances (@../../elexon/datasets/boal.md) and the BM unit reference. Any use first needs the row-grain and positive-value answers from NESO.

## Links

- NESO package: https://www.neso.energy/data-portal/wind-bmu-boa-volumes (landing page timed out during research; resource dictionaries were reachable at /wind_boa_volumes_202324 and /wind_boa_volumes_202627 under it)
- Registry record: @src/gridflow/connectors/neso_data_portal/registry/wind-bmu-boa-volumes.json
- Reconcile adjudication ledger: @src/gridflow/connectors/neso_data_portal/registry/_reconcile_adjudications.json
- Eligibility report: @docs/neso_data_portal/eligibility.md
- Decisions: @docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md (vintage), @docs/DECISION_LOG/ADR-039-neso-multi-resource-selection.md (multi-resource selection), @docs/DECISION_LOG/ADR-040-neso-reconcile-adjudication.md (adjudication)
- Evidence: @.planning/phases/v0.22-K-GEN-2/K-GEN-2-FACTS.md (section 4, BOA), @.planning/phases/v0.22-GEN-2H-adjudicated-gaps/GEN-2H-SPEC.md, @.planning/v0.22-RESULTS.md (section `GEN-2H`)
- Rulings: 547 (split and holds), 550, 551, 557, 558 in @.planning/RULINGS.md
- Domain: @../../../20-domain/concepts/settlement-period.md, @../../../20-domain/markets/gb-balancing-mechanism.md
