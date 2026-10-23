---
source: "neso_data_portal"
package: "system-inertia-cost"
dataset_key: "system_inertia_cost"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-10
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Daily average price of inertia
  summary: >-
    NESO's indicative average daily price, in £ per GVA.s, of Balancing Mechanism offers tagged
    for system inertia, one file per financial year.
  facts:
    vendor: "NESO Data Portal, package `system-inertia-cost`: one CSV file per financial year"
    cadence: "Ad hoc in NESO's catalogue; its file notes say appended daily"
    grain: One row per settlement day, from one financial-year file
    history: "Financial-year files from 2017-18, as NESO's catalogue lists them"
  landscape: market
  what_it_is: >-
    NESO divides the day's cost of Balancing Mechanism offers tagged for inertia by the day's
    inertia shortfall summed over settlement periods: a rate, not a total. NESO's unit text
    varies: £ per GVAs in its notes and field unit, £ per GVA in its description, £/GVA.s in its
    worked method, used here. NESO does not say what a zero means.
  how_used:
    - A daily indicative price of inertia bought through Balancing Mechanism offers.
    - "Set beside NESO's settlement-period inertia, joined on the day; never multiplied into a cost."
    - Counting the days each financial year that carry a price above zero.
  chart:
    type: line
    silver: neso_data_portal/system_inertia_cost
    time: settlement_date
    value: cost_gbp_per_gvas
    dedup: {"on": [settlement_date], order_by: published_at}
    aggregation: last
    window: {start: "2025-04-01", end: "2025-06-30"}
    max_points: 400
    unit: £/GVA.s
  chart_view:
    title: Daily inertia price, April to June 2025
    caption: >-
      Silver `neso_data_portal/system_inertia_cost`, `cost_gbp_per_gvas` in £ per GVA.s, one value
      per settlement day, 1 April to 30 June 2025, from NESO's 2025-26 file last modified 10 April
      2026. The zeros are NESO's own values. Most other quarters have more zero days.
    alt: >-
      Line chart of NESO's daily inertia price in pounds per GVA.s from
      neso_data_portal/system_inertia_cost, one value per settlement day, 1 April to 30 June 2025.
      The line is above zero on 61 of the 91 days and drops to zero on the other 30, in runs of one
      to six days. Priced days run from 1,427 on 12 April to 9,366 on 17 June, median 2,969. From
      21 May to 17 June every day is priced; 15 May reaches 7,714.
    x_label: settlement day, April to June 2025
    y_min: -400
    key:
      - {series: cost_gbp_per_gvas, label: Daily price, codes: cost_gbp_per_gvas, paint: petrol, note: "Highest £9,366 per GVA.s on 17 June; zero on 30 of 91 days."}
  raw_feed:
    note: >-
      A `package_show`, then each file downloaded whole unless its `last_modified` is unchanged;
      dates select nothing. The 2026-27 file stays in bronze: its one date, `01/04/2026`, breaks its
      filename's date format.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=system-inertia-cost"
      - "GET https://api.neso.energy/dataset/59f20804-9c9e-4f70-a809-c4c48a4f4c6e/resource/28dc603e-3472-45cd-8e7b-998efc674084/download/inertia_costs17.csv"
      - "GET https://api.neso.energy/dataset/59f20804-9c9e-4f70-a809-c4c48a4f4c6e/resource/a6a52241-1774-48d8-935f-2bef0d843e18/download/inertia_costs.csv"
      - "GET https://api.neso.energy/dataset/59f20804-9c9e-4f70-a809-c4c48a4f4c6e/resource/6295f4ed-b43d-4a80-8ca9-c27c9fa16517/download/inertia_costs.csv"
    commands:
      - {run: gridflow ingest neso_data_portal system_inertia_cost --last 24h, comment: "whole files; window must end recently"}
      - {run: gridflow transform neso_data_portal system_inertia_cost --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: settlement_date, op: ge, value: "2025-03-27"}
        - {column: settlement_date, op: le, value: "2025-04-03"}
      dedup: {"on": [settlement_date], order_by: published_at}
      order_by: [settlement_date]
      columns: [settlement_date, cost_gbp_per_gvas, timestamp_utc, resource_id, published_at]
    key: [resource_id, settlement_date]
    caption: "27 March to 3 April 2025: clocks forward on 30 March, 2025-26 file from 1 April."
    fields:
      settlement_date: "The UK calendar day NESO prices; with `resource_id`, the key"
      cost_gbp_per_gvas: "Average daily price, £ per GVA.s; NESO's `Cost` to 2020-21, then `Cost_per_GVAs`"
      timestamp_utc: "Set by gridflow: 00:00 UK time on the settlement day, in UTC"
      resource_id: CKAN id of the financial-year file the row came from
      published_at: "NESO's last-modified time for the whole yearly file, read as UTC"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      `query()` reads `silver_neso_data_portal_system_inertia_cost_latest`, filtering
      `settlement_date` with both ends included; lineage columns dropped. Times come back in UK
      time, so the query cell converts `timestamp_utc` to UTC; the next summarises each year.
    cells:
      - |
        df = data.neso_data_portal.query("system_inertia_cost", "2017-04-01", "2026-03-31")
        df["timestamp_utc"] = df.timestamp_utc.dt.tz_convert("UTC")
        df = df.sort_values("settlement_date", ignore_index=True)
        df.loc[df.settlement_date.between("2025-03-29", "2025-04-01"),
               ["settlement_date", "timestamp_utc", "cost_gbp_per_gvas", "resource_id"]]
      - |
        import pandas as pd
        p = df.set_index("settlement_date").cost_gbp_per_gvas
        fy = pd.Series([f"{y}-{(y + 1) % 100:02d}" for y in p.index.year - (p.index.month < 4)],
                       index=p.index)
        pd.DataFrame({"days": p.groupby(fy).size(), "above zero": (p > 0).groupby(fy).sum(),
                      "median above zero": p.where(p > 0).groupby(fy).median(),
                      "max": p.groupby(fy).max()})
      - |
        ax = p[p > 0].plot(style=".", ms=3, color="#155A6E", logy=True, figsize=(8, 3.5),
                           xlabel="settlement day", ylabel="£ per GVA.s, days above zero");
    needs: NESO's yearly inertia price files
    plot_alt: >-
      Dot plot on a log scale of NESO's daily inertia price in £ per GVA.s, days above zero only,
      April 2017 to March 2026. Dots sit mostly between about 1,000 and 3,000 until 2021, between
      about 5,000 and 10,000 from late 2021 into early 2023, then mostly about 2,000 to
      5,000. One day in
      July 2025 stands alone at 58,570.
  related:
    - {dataset: neso_data_portal/system-inertia, note: "NESO's inertia per settlement period; join on the day, never multiply"}
    - {dataset: neso_data_portal/gb-system-inertia-bid-and-offer-costs, note: "NESO's daily inertia price with the needed bids added, three ways"}
    - {dataset: neso_data_portal/constraint-breakdown, note: "NESO's daily spend in £ on increasing system inertia"}
---

# System Inertia Cost

Daily average price that NESO paid per unit of system inertia, published as one CSV per financial year from 2017-18 onwards. The vendor describes the figure as the average daily inertia price, derived from accepted offers tagged for inertia and the associated inertia estimates (gridflow @.planning/phases/v0.22-K-SYS-1/K-SYS-1-FACTS.md §7). The unit is pounds per GVAs (GVA.s) - a rate, never a total daily spend. It is a retrospective, indicative price: there is no forecast column and no issue column.

Use it as a daily indicative price alongside the settlement-period inertia estimates in @system-inertia.md, but do not multiply an inertia estimate by this rate and call the result a cost. The two datasets have different grains (settlement period versus day) and the published cost denominator covers inertia supplied for tagged actions across settlement periods, not the outturn estimate.

Supported by National Energy SO Open Data

- Publisher group: System
- Registry group: system · archetype: SER

## Files by disposition

Nine resources are captured to silver; one (the 2026 resource) is a resource-level HOLD. There are no DOC resources in this package. All ten are `upload` CSVs, captured 2026-10-08 (silver run 2026-10-08).

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| GB System Inertia Costs 2017 | CSV | upload | `28dc603e-3472-45cd-8e7b-998efc674084` |
| GB System Inertia Costs 2018 | CSV | upload | `1146f7af-9f3b-4a8a-a37d-3003c727bfbf` |
| GB System Inertia Costs 2019 | CSV | upload | `620491fa-ae1b-45b3-baa0-6e87c2d574cf` |
| GB System Inertia Costs 2020 | CSV | upload | `130c9f71-cbce-4027-b5b8-13cba14df0dd` |
| GB System Inertia Costs 2021 | CSV | upload | `3518e47e-ffb3-4561-aff1-4a102fcb242d` |
| GB System Inertia Costs 2022 | CSV | upload | `8a3a4233-e9aa-45c2-b0c4-28b8d614165b` |
| GB System Inertia Costs 2023 | CSV | upload | `3cc32e61-bf87-471c-bf00-abb356d3f8c8` |
| GB System Inertia Costs 2024 | CSV | upload | `91947c0c-bbbf-4d55-a29d-dc610d91d075` |
| GB System Inertia Costs 2025 | CSV | upload | `a6a52241-1774-48d8-935f-2bef0d843e18` |

### HOLD

| Resource | Format | Capture | Id | Reason (unit) |
|---|---|---|---|---|
| GB System Inertia Costs 2026 | CSV | upload | `6295f4ed-b43d-4a80-8ca9-c27c9fa16517` | The captured resource uses `Settlement Date,Cost_per_GVAs` and filename `inertia_costs.csv`, shared with resources whose dates are ISO. Its sole date is `01/04/2026`, which cannot pass their declared ISO cast, and does not independently establish day/month order. ADR-039 maps formats by exact filename, so it cannot distinguish these resources. Re-disposition requires a corrected vendor upload, an explicit distinguishing vendor filename/date contract, or a declared engine mechanism that resolves formats by a sufficient resource discriminator. (SYS-1) |

The hold is a reader/typing limitation (one filename, two incompatible date literals), not an ADR-040 adjudicated failure. The held resource contributes 0 silver rows and its data values are not published here. Nothing else in this family is held or failed.

## Resource downloads and coverage

Download URLs are the CKAN snapshot URLs (snapshot 20261006T195819Z). Resource names say a calendar year, but the files are financial years: every resource starts on 1 April of its label year (vendor resource description: one file per financial year). The "CKAN last_modified" column is the vintage clock described below.

| Resource | Filename | Download | CKAN last_modified | Silver rows | Settlement dates covered |
|---|---|---|---|---:|---|
| 2017 | `inertia_costs17.csv` | [download](https://api.neso.energy/dataset/59f20804-9c9e-4f70-a809-c4c48a4f4c6e/resource/28dc603e-3472-45cd-8e7b-998efc674084/download/inertia_costs17.csv) | 2021-12-07T12:12:09.974451 | 365 | 2017-04-01 to 2018-03-31 |
| 2018 | `inertia_costs18.csv` | [download](https://api.neso.energy/dataset/59f20804-9c9e-4f70-a809-c4c48a4f4c6e/resource/1146f7af-9f3b-4a8a-a37d-3003c727bfbf/download/inertia_costs18.csv) | 2021-12-07T12:14:12.860862 | 365 | 2018-04-01 to 2019-03-31 |
| 2019 | `inertia_costs19.csv` | [download](https://api.neso.energy/dataset/59f20804-9c9e-4f70-a809-c4c48a4f4c6e/resource/620491fa-ae1b-45b3-baa0-6e87c2d574cf/download/inertia_costs19.csv) | 2021-12-07T12:14:59.890158 | 366 | 2019-04-01 to 2020-03-31 |
| 2020 | `inertia_costs20.csv` | [download](https://api.neso.energy/dataset/59f20804-9c9e-4f70-a809-c4c48a4f4c6e/resource/130c9f71-cbce-4027-b5b8-13cba14df0dd/download/inertia_costs20.csv) | 2021-12-07T12:15:37.611975 | 365 | 2020-04-01 to 2021-03-31 |
| 2021 | `inertia_costs.csv` | [download](https://api.neso.energy/dataset/59f20804-9c9e-4f70-a809-c4c48a4f4c6e/resource/3518e47e-ffb3-4561-aff1-4a102fcb242d/download/inertia_costs.csv) | 2022-04-07T08:30:42.821949 | 361 | 2021-04-01 to 2022-03-31 |
| 2022 | `inertia_costs22.csv` | [download](https://api.neso.energy/dataset/59f20804-9c9e-4f70-a809-c4c48a4f4c6e/resource/8a3a4233-e9aa-45c2-b0c4-28b8d614165b/download/inertia_costs22.csv) | 2024-04-02T16:17:02.960104 | 362 | 2022-04-01 to 2023-03-31 |
| 2023 | `inertia_costs.csv` | [download](https://api.neso.energy/dataset/59f20804-9c9e-4f70-a809-c4c48a4f4c6e/resource/3cc32e61-bf87-471c-bf00-abb356d3f8c8/download/inertia_costs.csv) | 2025-01-21T15:54:38.545770 | 366 | 2023-04-01 to 2024-03-31 |
| 2024 | `inertia_costs.csv` | [download](https://api.neso.energy/dataset/59f20804-9c9e-4f70-a809-c4c48a4f4c6e/resource/91947c0c-bbbf-4d55-a29d-dc610d91d075/download/inertia_costs.csv) | 2025-09-04T13:30:48.701007 | 365 | 2024-04-01 to 2025-03-31 |
| 2025 | `inertia_costs.csv` | [download](https://api.neso.energy/dataset/59f20804-9c9e-4f70-a809-c4c48a4f4c6e/resource/a6a52241-1774-48d8-935f-2bef0d843e18/download/inertia_costs.csv) | 2026-04-10T09:06:09.725049 | 366 | 2025-04-01 to 2026-04-01 |
| 2026 (HOLD) | `inertia_costs.csv` | [download](https://api.neso.energy/dataset/59f20804-9c9e-4f70-a809-c4c48a4f4c6e/resource/6295f4ed-b43d-4a80-8ca9-c27c9fa16517/download/inertia_costs.csv) | 2026-04-14T14:54:26.059319 | 0 (held) | one data row in bronze (3,282 bronze CSV rows in total) |

Silver total: 3,281 rows (activation receipt, RESULTS "SYS-1", RULINGS 647). The 2025 resource reaches one day into 2026-27, so the financial-year boundary and the resource label do not line up exactly.

## Families

### `system_inertia_cost`

- Kind: tabular · archetype: SER · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Settlement Date | `settlement_date` | date | `inertia_costs17.csv` → `%d/%m/%Y`; `inertia_costs18.csv` → `%d/%m/%Y`; `inertia_costs19.csv` → `%d/%m/%Y`; `inertia_costs20.csv` → `%d/%m/%Y`; `inertia_costs22.csv` → `%Y-%m-%d`; `inertia_costs.csv` → `%Y-%m-%d` | no | — | — |
| Cost | `cost_gbp_per_gvas` | int64 | — | yes | — | not carried in the generated schema; the legacy dictionary and methodology give £ per GVAs (see Units) |

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Settlement Date | `settlement_date` | date | `inertia_costs17.csv` → `%d/%m/%Y`; `inertia_costs18.csv` → `%d/%m/%Y`; `inertia_costs19.csv` → `%d/%m/%Y`; `inertia_costs20.csv` → `%d/%m/%Y`; `inertia_costs22.csv` → `%Y-%m-%d`; `inertia_costs.csv` → `%Y-%m-%d` | no | — | — |
| Cost_per_GVAs | `cost_gbp_per_gvas` | int64 | — | yes | — | £ per GVAs |

- Entity key: `resource_id`, `settlement_date`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: date_sp1 (`settlement_date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

## Two clocks

- **Vintage clock - `ckan_last_modified`.** `published_at` and `available_at` are both the CKAN `last_modified` of the captured resource file (the table above). There is no issue column in the vendor data and no evidence that a daily price was publicly available at its operational day, so availability is the upload date, not the settlement date. The 2017-2020 resources therefore carry an `available_at` of 2021-12-07, years after their event time. Point-in-time queries must filter on `available_at`.
- **Event clock - `date_sp1(settlement_date)`.** Each row is one calendar day. The silver `timestamp_utc` / `event_time` is the UK settlement-period-1 start of that date, i.e. the engine's daily anchor, not a vendor timestamp (for example a summer date lands at 23:00 UTC the previous evening). Treat it as a day label: the price is a daily average and has no sub-day resolution.

## Units, sentinels and identifiers

- **Unit.** Both header epochs are the same vendor quantity and land in one silver column, `cost_gbp_per_gvas` (int64, nullable). Epoch 1 (`Cost`, resources 2017-2020) and epoch 2 (`Cost_per_GVAs`, resources 2021-2026) are documented by NESO as the daily average cost of a unit of inertia in pounds per GVAs; the epoch-2 field dictionary carries the explicit unit "£ per GVAs", but its own description reads "(£ per GVA)" (field-info snapshot 20261008T114228Z, captured from the 2026 resource), while the package notes give "£ per GVAs" and then "£/GVA.s" in the method and worked examples (K-SYS-1-FACTS §7 T01, ruling 642). No conversion is applied. The vendor example value shows whole numbers, consistent with int64.
- **Zeros.** Zero is a supplied numeric value and stays numeric; it is never nulled or dropped. Zero counts per resource (settlement days with a zero price, longest consecutive file-order run): 2017: 358 (116); 2018: 288 (29); 2019: 279 (30); 2020: 219 (18); 2021: 237 (28); 2022: 231 (30); 2023: 202 (17); 2024: 170 (28); 2025: 192 (19). TODO: verify what a zero means - no inspected source says whether it is no tagged inertia action, a computed zero rate, or another reporting condition (INERTIA-COST-ZERO).
- **Other sentinels.** No blank cells, `-1`, `N/A`, `NA`, thousands separators, currency symbols or percent signs occur in the value cells of any captured resource; every value passes the int64 cast (FACTS g5). Because the dtype is nullable, a future blank would land as null rather than zero.
- **Identifiers.** The only identifier is the CKAN `resource_id`, stored as-is, which separates financial-year files in the entity key. There are no group labels or BMU/EIC codes in this family.

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc

The vendor publishes one resource per financial year, and the CKAN catalog snapshot (20261006T195819Z) describes every resource as updated daily, appending to one file per financial year. The observed `last_modified` values are listed in the coverage table above (2021-12-07 for 2017-2020, then 2022-04-07, 2024-04-02, 2025-01-21, 2025-09-04, 2026-04-10 and, for the held 2026 resource, 2026-04-14). A `last_modified` later than a financial-year end is consistent with that append description and is not by itself evidence of revision. TODO: verify whether any resource was revised after first publication; no conclusion is drawn here. `latest` is `whole_capture` per `resource_id`: for each resource, the newest whole captured file supersedes older captures of that same resource, while different resources never replace each other.

## Known issues and gotchas

- **Date formats are filename-specific.** Resources 2017-2020 use `%d/%m/%Y`; 2021-2025 use ISO `%Y-%m-%d`. The format map is keyed on exact filename (ADR-039), and five resources (four admitted, plus the held 2026 resource) share `inertia_costs.csv`.
- **The 2026 resource is held** because its single date literal is a slash date (`01/04/2026`) under the same filename as the ISO resources, and its day/month order is not independently established. Re-disposition conditions are in the HOLD table. TODO: verify with NESO whether the 2026 upload is DMY and whether the file will be corrected.
- **Conditional overlap if the held resource were later admitted.** If the 2026 literal is read as day/month, it repeats the final settlement date already present in the 2025 resource. This is a conditional observation, not a settled fact; precedence between the two would then need an ADR-039/040 ruling, and none is invented here.
- **Missing days are preserved, not filled.** The 2021 resource lacks 2021-11-24, 2021-11-25, 2021-11-26 and 2021-12-08 (361 rows); the 2022 resource lacks 2022-05-16, 2022-05-17 and 2022-08-18 (362 rows). The reason is not documented. TODO: verify with NESO.
- **One isolated extreme value.** 2025-07-25 carries 58,570 £/GVA.s in the 2025 resource, four times the next highest value in any resource (14,650 on 2022-03-09), between zero-priced days (silver, 2026-10-08 capture). NESO's method divides by the day's inertia shortfall, so a small denominator could produce it, but nothing inspected says so. Silver keeps it as supplied. TODO: verify with NESO (INERTIA-COST-OUTLIER).
- **Entity-key uniqueness is measured, not vendor-guaranteed.** The settlement date is unique within every captured resource (duplicate excess 0), but the dictionary states no primary-key guarantee. TODO: verify (vendor key guarantee).
- **Resource label is not a calendar year.** See the coverage table; join on `settlement_date`, never on the label.
- **Settlement-day grain.** The daily row is an anchor at settlement period 1 for the GB (UK) day; no per-period or DST (46/50-period) structure exists in this dataset.

## Holds

- none

The family itself has no hold; the only hold is the resource-level one on the 2026 file listed above (unit SYS-1). Nothing in this family is an ADR-040 adjudicated failure.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data
