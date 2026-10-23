---
source: "neso_data_portal"
package: "system-inertia"
dataset_key: "system_inertia"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-10
last_verified: 2026-10-10
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: GB system inertia by settlement period
  summary: >-
    NESO's estimate of GB transmission-system inertia in GVA.s per half-hour settlement period:
    the outturn, and a market-provided figure with NESO's actions removed.
  facts:
    vendor: "NESO Data Portal, package `system-inertia`: one CSV file per financial year"
    cadence: "Weekly in NESO's catalogue; its package text says updates are temporarily paused"
    grain: One row per settlement period, from one yearly file
    history: "Yearly files from 2017-18, as NESO's catalogue lists them"
  landscape: power
  what_it_is: >-
    NESO's estimate of inertia on the GB transmission system each settlement period, in GVA.s
    (NESO writes GVAs). Outturn inertia sums generators above 15 MW or running to provide inertia,
    plus a demand estimate. Market-provided inertia recalculates generator positions without
    NESO's trades and bid-offer acceptances. Neither counts Stability Pathfinder units, NESO says.
  how_used:
    - "Low-inertia periods, and how far NESO's actions moved them from the market outcome."
    - "Set beside NESO's daily inertia price, joined on the settlement date."
    - Post-event studies with NESO's one-second frequency record.
  chart:
    type: line
    silver: neso_data_portal/system_inertia
    time: settlement_date
    values:
      - {column: outturn_inertia, series: outturn}
      - {column: market_provided_inertia, series: market}
    dedup: {"on": [settlement_date, settlement_period], order_by: capture_written_at}
    aggregation: min
    window: {start: "2025-04-01", end: "2026-03-31"}
    max_points: 400
    unit: GVA.s
  chart_view:
    title: Daily lowest inertia, April 2025 to March 2026
    caption: >-
      Silver `neso_data_portal/system_inertia`, GVA.s: each settlement day's lowest outturn and
      lowest market-provided value, taken separately, 1 April 2025 to 31 March 2026, from NESO's
      2025-26 file last modified 20 May 2026.
    alt: >-
      Line chart of each settlement day's lowest inertia in GVA.s from neso_data_portal/system_inertia,
      1 April 2025 to 31 March 2026, two lines. The outturn line never drops below 107, on 21
      February 2026; its median daily low is 125. The market-provided line runs lower, median 101,
      down to 71 on 4 May 2025. Outturn is higher on 354 of the 365 days. Both lines peak on 5
      January 2026, at 252 and 248.
    x_label: settlement day, April 2025 to March 2026
    y_min: 60
    key:
      - {series: outturn, label: Outturn, codes: outturn_inertia, paint: petrol, note: "Lowest 107 GVA.s, on 21 February 2026; median daily low 125."}
      - {series: market, label: Market provided, codes: market_provided_inertia, paint: clay, note: "Lowest 71 GVA.s, on 4 May 2025; median daily low 101."}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then each financial-year file downloaded whole
      unless its `last_modified` is unchanged; dates select nothing.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=system-inertia"
      - "GET https://api.neso.energy/dataset/8f3cd0ce-6636-469e-b582-55eadfeaa1d9/resource/096d2e9f-fc94-439c-899a-31a67650bda7/download/inertia.csv"
      - "GET https://api.neso.energy/dataset/8f3cd0ce-6636-469e-b582-55eadfeaa1d9/resource/3ff8b466-5c16-4713-abfe-ad332298f15f/download/inertia.csv"
    commands:
      - {run: gridflow ingest neso_data_portal system_inertia --last 24h, comment: "whole files; window must end recently"}
      - {run: gridflow transform neso_data_portal system_inertia --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: settlement_date, op: eq, value: "2025-10-26"}
        - {column: settlement_period, op: in, value: [1, 2, 3, 4, 5, 6, 49, 50]}
      dedup: {"on": [settlement_date, settlement_period], order_by: capture_written_at}
      order_by: [settlement_period]
      columns: [settlement_date, settlement_period, timestamp_utc, outturn_inertia, market_provided_inertia, resource_id, published_at]
    key: [resource_id, settlement_date, settlement_period]
    caption: "26 October 2025, clocks back: 50 periods, period 1 at 23:00 UTC the evening before."
    fields:
      settlement_date: "Settlement day as NESO labels it; gridflow starts it at 00:00 UK time"
      settlement_period: "Half-hour of the settlement day, 1 to 48; 46 or 50 when clocks change"
      timestamp_utc: Start of the period in UTC, computed by gridflow from date and period
      outturn_inertia: "Estimated GB transmission-system inertia, GVA.s (NESO writes GVAs)"
      market_provided_inertia: "The same estimate without NESO's trades and bid-offer acceptances, GVA.s"
      resource_id: CKAN id of the financial-year file the row came from
      published_at: "NESO's last-modified time for the whole yearly file, read as UTC"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      `query()` reads `silver_neso_data_portal_system_inertia_latest`, filtering `settlement_date`
      with both ends included; lineage columns dropped. Times come back in UK time, so the query cell
      converts `timestamp_utc` to UTC; the next counts periods per day.
    cells:
      - |
        df = data.neso_data_portal.query("system_inertia", "2025-04-01", "2026-03-31")
        df["timestamp_utc"] = df.timestamp_utc.dt.tz_convert("UTC")
        df = df.sort_values("timestamp_utc", ignore_index=True)
        day = df[df.settlement_date.astype(str) == "2025-10-26"]
        day.loc[day.settlement_period.isin([1, 2, 49, 50]),
                ["settlement_date", "settlement_period", "timestamp_utc", "outturn_inertia"]]
      - df.groupby("settlement_date").size().value_counts().rename("days").rename_axis("periods in the day")
      - |
        daily = df.groupby("settlement_date")[["outturn_inertia", "market_provided_inertia"]].min()
        daily.agg(["min", "median", "max"])
      - |
        ax = daily.plot(figsize=(8, 3.5), color=["#155A6E", "#C77E3C"], lw=0.8,
                        xlabel="settlement day", ylabel="GVA.s, daily lowest");
    needs: NESO's yearly inertia files
    plot_alt: >-
      Line plot of each settlement day's lowest outturn and market-provided inertia in GVA.s, 1 April
      2025 to 31 March 2026. The outturn line holds between about 107 and 150 on most days, with
      peaks near 228 in October and 252 in early January. The market-provided line sits below it,
      often between 75 and 100, and meets it at the peaks.
  related:
    - {dataset: neso_data_portal/system-inertia-cost, note: "NESO's daily average price per GVA.s of inertia, by settlement date"}
    - {dataset: neso_data_portal/system-frequency-data, note: "NESO's GB frequency each second, read with inertia in event studies"}
    - {dataset: neso_data_portal/stability-pathfinder-service-information, note: "Stability Pathfinder units, whose inertia NESO leaves out here"}
    - {dataset: neso_data_portal/historic_generation_mix, note: "GB generation by fuel each half-hour, to set against inertia"}
---

# System Inertia

## Overview

System Inertia is NESO's published estimate of the rotational inertia of the Great Britain transmission system, one value per half-hour settlement period. Inertia is the kinetic energy stored in synchronised spinning plant; it slows the rate at which grid frequency moves after a generation or demand loss (RoCoF), so a low-inertia period costs the system operator more to secure. The dataset carries two quantities per period: `Outturn Inertia`, the vendor's estimate of actual transmission-system inertia, and `Market Provided Inertia`, the same estimate recalculated with the effect of NESO's own balancing actions removed. The gap between the two is therefore the inertia that NESO actions added or removed relative to a market-only outcome. In a model it is useful as a stability-cost driver, a feature for synchronous-plant dispatch, and a denominator or companion to the daily inertia price in the sibling package `system-inertia-cost` (see @30-vendors/neso-data-portal/datasets/system-inertia-cost.md).

Both quantities are retrospective estimates. There is no forecast column. The vendor states the dataset does not include the contribution of Stability Pathfinder units. The vendor description currently carries a note that updates to the dataset are temporarily paused while NESO reviews and validates the most appropriate data. The newest resource ends at settlement date 2026-07-26, which is consistent with that note even though the registry refresh label is weekly. TODO: verify when updates resume and whether published history is revised on resumption.

Supported by National Energy SO Open Data

- Publisher group: System
- Registry group: system · archetype: SER
- CKAN package: `system-inertia` (id `8f3cd0ce-6636-469e-b582-55eadfeaa1d9`), author National Grid Electricity System Operator
- Source of truth for this page: the vendor field dictionary (CKAN datastore field info, snapshot 2026-10-08), the registry record, and the SYS-1 verification of real bodies (gridflow repo, `.planning/phases/v0.22-K-SYS-1/VERIFICATION.md`)

## Files by disposition

All ten resources are dispositioned SILVER. There are no DOC resources and no HOLD resources in this package. Every resource is a CKAN `upload` CSV with the filename `inertia.csv` and one financial year (1 April to 31 March) of data.

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| GB System Inertia - 2017-2018 | CSV | upload | `096d2e9f-fc94-439c-899a-31a67650bda7` |
| GB System Inertia - 2018-2019 | CSV | upload | `1e48b665-684d-4372-925a-2beedb520cdf` |
| GB System Inertia - 2019-2020 | CSV | upload | `2f2dbaa1-3047-4e48-85f2-ec24e669678f` |
| GB System Inertia - 2020-2021 | CSV | upload | `f198d0bd-2b7d-493c-af9d-b2b9cbb4353b` |
| GB System Inertia - 2021-2022 | CSV | upload | `55161fb4-1396-46e2-9250-2e2b9df904bf` |
| GB System Inertia - 2022-2023 | CSV | upload | `b42a4fe0-32e4-47ed-9697-5fe101b75970` |
| GB System Inertia - 2023-2024 | CSV | upload | `5bd6ec4d-a2df-4c94-9b27-fdf8cf04d7dd` |
| GB System Inertia - 2024-2025 | CSV | upload | `7a12d0bd-448d-42a9-b333-4a32761dbad4` |
| GB System Inertia - 2025-2026 | CSV | upload | `936daa4f-fca4-4c6a-968a-884f3d77bafe` |
| GB System Inertia - 2026-2027 | CSV | upload | `3ff8b466-5c16-4713-abfe-ad332298f15f` |

### Captured coverage per resource

Measured in silver at activation (2026-10-10). Vintage is the CKAN `last_modified` of the captured file.

| Resource year | Silver rows | First settlement date | Last settlement date | Vintage (`ckan_last_modified`) | Download |
|---|---:|---|---|---|---|
| 2017-2018 | 17,520 | 2017-04-01 | 2018-03-31 | 2021-07-01T10:44:28 | [inertia.csv](https://api.neso.energy/dataset/8f3cd0ce-6636-469e-b582-55eadfeaa1d9/resource/096d2e9f-fc94-439c-899a-31a67650bda7/download/inertia.csv) |
| 2018-2019 | 17,520 | 2018-04-01 | 2019-03-31 | 2021-07-01T10:56:25 | [inertia.csv](https://api.neso.energy/dataset/8f3cd0ce-6636-469e-b582-55eadfeaa1d9/resource/1e48b665-684d-4372-925a-2beedb520cdf/download/inertia.csv) |
| 2019-2020 | 17,568 | 2019-04-01 | 2020-03-31 | 2021-07-01T10:58:44 | [inertia.csv](https://api.neso.energy/dataset/8f3cd0ce-6636-469e-b582-55eadfeaa1d9/resource/2f2dbaa1-3047-4e48-85f2-ec24e669678f/download/inertia.csv) |
| 2020-2021 | 17,520 | 2020-04-01 | 2021-03-31 | 2021-07-01T11:00:55 | [inertia.csv](https://api.neso.energy/dataset/8f3cd0ce-6636-469e-b582-55eadfeaa1d9/resource/f198d0bd-2b7d-493c-af9d-b2b9cbb4353b/download/inertia.csv) |
| 2021-2022 | 17,520 | 2021-04-01 | 2022-03-31 | 2022-04-04T10:31:22 | [inertia.csv](https://api.neso.energy/dataset/8f3cd0ce-6636-469e-b582-55eadfeaa1d9/resource/55161fb4-1396-46e2-9250-2e2b9df904bf/download/inertia.csv) |
| 2022-2023 | 17,472 | 2022-04-01 | 2023-03-31 | 2023-04-04T15:40:55 | [inertia.csv](https://api.neso.energy/dataset/8f3cd0ce-6636-469e-b582-55eadfeaa1d9/resource/b42a4fe0-32e4-47ed-9697-5fe101b75970/download/inertia.csv) |
| 2023-2024 | 17,476 | 2023-04-01 | 2024-03-31 | 2024-04-11T07:51:13 | [inertia.csv](https://api.neso.energy/dataset/8f3cd0ce-6636-469e-b582-55eadfeaa1d9/resource/5bd6ec4d-a2df-4c94-9b27-fdf8cf04d7dd/download/inertia.csv) |
| 2024-2025 | 17,520 | 2024-04-01 | 2025-03-31 | 2025-05-14T09:56:49 | [inertia.csv](https://api.neso.energy/dataset/8f3cd0ce-6636-469e-b582-55eadfeaa1d9/resource/7a12d0bd-448d-42a9-b333-4a32761dbad4/download/inertia.csv) |
| 2025-2026 | 17,520 | 2025-04-01 | 2026-03-31 | 2026-05-20T10:37:49 | [inertia.csv](https://api.neso.energy/dataset/8f3cd0ce-6636-469e-b582-55eadfeaa1d9/resource/936daa4f-fca4-4c6a-968a-884f3d77bafe/download/inertia.csv) |
| 2026-2027 | 4,788 | 2026-04-01 | 2026-07-26 | 2026-07-27T14:01:47 | [inertia.csv](https://api.neso.energy/dataset/8f3cd0ce-6636-469e-b582-55eadfeaa1d9/resource/3ff8b466-5c16-4713-abfe-ad332298f15f/download/inertia.csv) |

Total: 162,424 silver rows over 10 resources. Row counts equal the CSV body row counts in bronze; nothing was rejected. The older resources are uploaded once and have not changed since their listed vintage; the current-year resource is the only one that grows. TODO: verify whether NESO re-uploads or revises a closed financial-year resource (the vintage clock would show it, but no second capture exists yet).

## Families

### `system_inertia`

- Kind: tabular · archetype: SER · refresh: weekly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Settlement Date | `settlement_date` | date | `%Y-%m-%d` | no | — | — |
| Settlement Period | `settlement_period` | int64 | — | no | — | — |
| Outturn Inertia | `outturn_inertia` | int64 | — | yes | — | GVAs |
| Market Provided Inertia | `market_provided_inertia` | int64 | — | yes | — | GVAs |

- Entity key: `resource_id`, `settlement_date`, `settlement_period`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: sp_pair (`settlement_date`, `settlement_period`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

### The two clocks

- **Vintage clock (`ckan_last_modified`).** `published_at` and `available_at` are both the CKAN `last_modified` of the captured resource file (ADR-030). They are equal on every silver row. There is no issue column in the vendor file and no evidence these estimates were publicly available earlier than the upload, so a point-in-time query (`available_at <= as_of`) sees a financial-year resource only once its file was uploaded. For the 2017-2021 resources that is 2021-07-01, so the early history is not point-in-time honest for any `as_of` before that date.
- **Event clock (temporal recipe `sp_pair`).** `timestamp_utc` and `event_time` are derived from `settlement_date` plus `settlement_period` as the start of that UK settlement period, in tz-aware UTC. They are equal on every row. Example: settlement date 2026-04-01, period 1 maps to 2026-03-31 23:00 UTC (BST), period 2 to 23:30 UTC. On the spring clock-change day 2026-03-29 the 2025-2026 resource has 46 periods and period 1 begins at 00:00 UTC.

### Silver layer

- Path pattern: `C:/gridflow-data/silver/neso_data_portal/system_inertia/year=<YYYY>/month=<MM>/system_inertia_<capture-date>_run<timestamp>_<hash>.parquet`, one file per captured resource (10 files after activation). `dataset_version` is `1+e1` (record version 1, header epoch 1).
- Dedup / entity key: (`resource_id`, `settlement_date`, `settlement_period`). Measured duplicate excess is 0 in every resource and 0 across resources (the financial years do not overlap).
- Silver columns: `settlement_date`, `settlement_period`, `outturn_inertia`, `market_provided_inertia`, `resource_id`, `timestamp_utc`, `published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id`, `dataset_version`.

Silver sample (first two rows of the 2026-2027 resource; envelope columns shortened):

```python
[
    {"settlement_date": "2026-04-01", "settlement_period": 1, "outturn_inertia": 193,
     "market_provided_inertia": 174, "resource_id": "3ff8b466-5c16-4713-abfe-ad332298f15f",
     "timestamp_utc": "2026-03-31T23:00:00Z", "published_at": "2026-07-27T14:01:47.463582Z",
     "available_at": "2026-07-27T14:01:47.463582Z", "dataset_version": "1+e1"},
    {"settlement_date": "2026-04-01", "settlement_period": 2, "outturn_inertia": 192,
     "market_provided_inertia": 174, "resource_id": "3ff8b466-5c16-4713-abfe-ad332298f15f",
     "timestamp_utc": "2026-03-31T23:30:00Z", "published_at": "2026-07-27T14:01:47.463582Z",
     "available_at": "2026-07-27T14:01:47.463582Z", "dataset_version": "1+e1"},
]
```

### Units and value semantics

- `Outturn Inertia` and `Market Provided Inertia` carry the vendor unit **GVAs** (the field dictionary writes `GVAs`; the same quantity is also written GVA.s). The unit comes from the vendor dictionary, not from the column name. Silver stores the integers as supplied, with no scaling.
- `Outturn Inertia`: vendor description, an estimate of GB transmission-system inertia, the sum of the estimated inertia of each generator with output above 15 MW or operating to provide inertia, plus an estimate of the demand-side contribution.
- `Market Provided Inertia`: calculated the same way, but with generator positions recalculated to remove the effect of actions taken by NESO (BMU-specific trades to manage constraints, RoCoF risk and voltage, and Bid Offer Acceptances). It is a retrospective counterfactual, not a forecast.
- `Settlement Period` is an ordinal index, not a physical quantity, and takes the range 1 to 50. Clock-change days carry 46 or 50 periods, except 2022-10-30, which carries only periods 1 and 2; ordinary days 48.
- Sentinels: none. No blank cells, `-1`, `N/A`, `NA`, zero values, thousands separators, currency or percent signs were found in any inertia body, and every value passes its int64 cast. Both inertia columns are therefore non-null in silver (0 nulls over 162,424 rows) although the schema allows null. If a sentinel appears in a later capture, store it as supplied and raise a TODO rather than coercing it.

## Cadence

- Registry refresh: weekly
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Weekly
- Effective cadence: the vendor currently states updates are paused (see Overview). The only growing resource is the 2026-2027 file, last modified 2026-07-27 and ending at settlement date 2026-07-26.
- Resources are uploaded files, one per financial year. A new financial year appears as a new resource id; the registry will need to record it before it is dispositioned.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

## Holds

- none

No hold applies to this package. The related inertia-cost resource hold (2026 resource of `system-inertia-cost`) and the two held Stability Pathfinder reports are separate packages; see @30-vendors/neso-data-portal/datasets/system-inertia-cost.md.

## Known issues and gotchas

- **Sparse days.** The bodies are not uniform complete grids. The 2022-2023 resource has 1 day carrying only 2 periods; 2023-2024 has 2 such days; 2026-2027 has 18 days carrying only 2 periods and 99 days carrying 48. Each sparse day carries periods 1 and 2 only; the 2022-2023 one is the autumn clock-change day 2022-10-30 (silver, 2026-10-23). Omitted periods are not filled and must not be read as zero inertia. TODO: verify with NESO why these days are sparse (INERTIA-SPARSITY).
- **Settlement period range.** Valid periods are 1 to 50; the silver record enforces the bound and an exhaustive check found 0 invalid (date, period) pairs. Spring and autumn clock-change days have 46 and 50 periods respectively, except 2022-10-30, which carries only periods 1 and 2.
- **Whole low days.** On 2022-03-19, 2022-06-08, 2023-01-05, 2023-09-30 and 2026-06-01, `outturn_inertia` is below 100 in 46 to 48 periods (lows 43 to 54) while the neighbouring days' lows are 109 to 207 (silver, 2026-10-23). NESO gives no reason. TODO: verify with NESO whether these days are valid estimates.
- **Leap-year and total counts.** 2019-2020 has 17,568 rows (366 days at 48 periods); the 2022-2023 and 2023-2024 counts fall short of a full grid because of the sparse days above.
- **Key guarantee.** Uniqueness of (date, period) within a resource is measured, not a documented vendor guarantee. TODO: verify with NESO that (settlement date, settlement period) is a primary key. Silver keys on `resource_id` as well, per ADR-039.
- **Whole-capture latest.** `_latest` serves the newest whole capture of each resource id, never row-level merges across captures.
- **Stability Pathfinder exclusion.** Per the vendor, the inertia figures exclude the contribution of Stability Pathfinder units. Do not add Pathfinder inertia to these columns.
- **Retrospective only.** Both columns are estimates produced after the fact; do not use them as a forecast or as an operational signal known at the time of the period.

## Implementation delta

- No discrepancy between the vendor dictionary, the registry record and silver was found. The vendor lists `Settlement Date` with example `2021-06-30`; the captured bodies use ISO `%Y-%m-%d` in every resource, so a single date format applies and no per-filename format map is needed.
- Registry refresh is `weekly` (from the vendor `Update frequency` extra) while the vendor note says updates are paused. This is a vendor-side tension, not a code defect.

## Modelling notes

TODO: modelling use is not yet designed in gridflow_models. Candidate uses, unverified: outturn minus market-provided inertia as a measure of NESO intervention; the daily join to `system_inertia_cost` at date level (the cost is a daily rate in £ per GVAs, not timestamp-equivalent to the half-hour inertia, and multiplying the two is not the vendor's stated cost calculation).

## Links

- [Vendor dataset page](https://www.neso.energy/data-portal/system-inertia)
- Registry record: `src/gridflow/connectors/neso_data_portal/registry/system-inertia.json` (gridflow repo)
- Eligibility report: `docs/neso_data_portal/eligibility.md` (gridflow repo)
- Decision records: ADR-030 (vintage clock), ADR-039 (multi-resource selection) in `docs/DECISION_LOG/` (gridflow repo)
- Silver root: `C:/gridflow-data/silver/neso_data_portal/system_inertia/`
- Sibling package: @30-vendors/neso-data-portal/datasets/system-inertia-cost.md
