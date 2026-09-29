---
source: elexon
dataset_key: uou2t14d
vendor: Elexon BMRS
last_verified: 2026-05-21
layer_coverage: bronze, silver
v2_fix_history:
  - date: 2026-05-20
    phase: gridflow-G5-W2.3
    pr: https://github.com/EBentham/gridflow/pull/7
    change: silver transformer made self-describing — restores `fuel_type` and `national_grid_bm_unit` columns; published_at also carried through as UTC datetime
  - date: 2026-05-20
    phase: gridflow-G5-W4
    pr: https://github.com/EBentham/gridflow/pull/7
    change: ElexonUOU2T14D Pydantic schema declared
page:
  title: Availability forecast by BM unit
  summary: >-
    Elexon's forward view of each BM unit's available output, one figure per delivery date, 2 to
    14 days ahead.
  facts:
    vendor: Elexon BMRS, dataset UOU2T14D
    cadence: Not stated in Elexon's API docs
    grain: One row per delivery date, unit id and fetched day; null ids share one
  landscape: power
  what_it_is: >-
    Elexon's view of availability (Grid Code Output Usable) per National Grid BM unit, accounting
    for planned outages: one figure per unit per delivery date, 2 to 14 days ahead. Silver keeps
    one row per Elexon unit id and date per fetched day, chosen by bronze file order, not publish
    time; units without an id collapse to one row.
  how_used:
    - Planned outages and returns by unit, 2 to 14 days ahead, for forward margin.
    - "Point-in-time features: what each unit was expected to offer, as of a publish."
    - Cross-checking REMIT outage messages against a unit's forecast availability.
  chart:
    type: line
    silver: elexon/uou2t14d
    time: settlement_date
    value: output_usable_mw
    filter:
      - {column: published_at, op: eq, value: "2026-09-21T20:00:00Z"}
      - {column: bm_unit_id, op: in, value: [T_PEHE-1, T_HEYM11, T_SGRWO-6]}
    group: bm_unit_id
    group_map:
      T_PEHE-1: peterhead
      T_HEYM11: heysham
      T_SGRWO-6: seagreen
    series_order: [peterhead, heysham, seagreen]
    aggregation: last
    window: {start: "2026-09-23", end: "2026-10-05"}
    unit: MW
  chart_view:
    title: Three units' forecast availability, publish of 21 September 2026
    caption: >-
      Silver `elexon/uou2t14d`, MW: what the 20:00 UTC publish of 21 September 2026 gave three BM
      units for delivery dates 23 September to 5 October. A forecast, not outturn; one figure per
      unit and date, nothing summed. Lines join daily figures.
    alt: >-
      Line chart from elexon/uou2t14d, in MW: the availability the 20:00 UTC publish of 21
      September 2026 gave three BM units for each delivery date, 23 September to 5 October.
      Peterhead Block 1 is 0 through 29 September, then 1,180 from the 30th. Heysham 1 Generator 1
      is 0 through the 29th, then 262, 360 and 476, reaching 498 on 3 October. Seagreen 6 moves
      between 89 on the 23rd and 299 on the 24th, and ends at 172.
    x_label: delivery date; one figure per day
    key:
      - {series: peterhead, label: Peterhead Block 1, codes: T_PEHE-1, paint: clay, note: "Fuel type CCGT. 0 through 29 September, 1,180 from the 30th."}
      - {series: heysham, label: Heysham 1 Generator 1, codes: T_HEYM11, paint: petrol, note: "Fuel type NUCLEAR. 0 through the 29th, then steps up to 498."}
      - {series: seagreen, label: Seagreen 6, codes: T_SGRWO-6, paint: horizon, note: "Fuel type WIND. Changes from day to day, 89 to 299."}
  raw_feed:
    note: >-
      From the Elexon Insights API in 4-hour publish windows, the most the API accepts. `gridflow
      transform` keeps one row per Elexon unit id and delivery date from each fetched day.
    requests:
      - "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/UOU2T14D?publishDateTimeFrom=2026-09-21T20:00:00Z&publishDateTimeTo=2026-09-22T00:00:00Z&page=1"
    commands:
      - {run: gridflow ingest elexon uou2t14d --start 2026-09-21 --end 2026-09-22, comment: "bronze; six 4-hour publish windows"}
      - {run: gridflow transform elexon uou2t14d --start 2026-09-21 --end 2026-09-21, comment: bronze to silver}
  record:
    select:
      filter:
        - {column: published_at, op: eq, value: "2026-09-21T20:00:00Z"}
        - {column: settlement_date, op: eq, value: "2026-09-30"}
        - {column: national_grid_bm_unit, op: in, value: [DINO-3, DRAXX-4, HEYM11, IEG-FRAN1, PEHE-1, SGRWO-6, SIZB-1, WTGRW-1]}
      order_by: [fuel_type, national_grid_bm_unit]
      columns: [bm_unit_id, output_usable_mw, national_grid_bm_unit, published_at, settlement_date, fuel_type]
    key: [settlement_date, bm_unit_id, published_at]
    caption: "Delivery date 30 September, from the 20:00 UTC publish of 21 September: eight BM units."
    fields:
      bm_unit_id: Elexon unit id; null-id units collapse to one row per date and fetched day
      output_usable_mw: "Output Usable for the delivery date; no unit sent, MW by gridflow's column name"
      national_grid_bm_unit: "National Grid BM unit id; Elexon's id adds a prefix such as `T_`"
      published_at: "Publish time from `publishTime`, UTC; separates fetched days, not in gridflow's dedup key"
      settlement_date: "Delivery date the forecast is for, from the vendor `forecastDate`"
      fuel_type: Elexon fuel-type code, as sent with each unit
      timestamp_utc: "Midnight UTC of the delivery date, set by gridflow; the vendor sends a date"
  notebook:
    lead: >-
      Returns a pandas DataFrame from the DuckDB relation `silver_elexon_uou2t14d`, filtered on
      `settlement_date` with both ends included: every stored publish (no latest view). Lineage
      columns are dropped. The cells keep the 21 September fetch's publish.
    cells:
      - |
        df = data.elexon.query("uou2t14d", "2026-09-23", "2026-10-05")
        df["published_at"] = df.published_at.dt.tz_convert("UTC")
        pub = df[df.published_at.dt.strftime("%Y-%m-%d") == "2026-09-21"]
        pub.published_at.unique()
      - |
        units = ["T_PEHE-1", "T_HEYM11", "T_SGRWO-6"]
        wide = pub[pub.bm_unit_id.isin(units)].pivot(
            index="settlement_date", columns="bm_unit_id", values="output_usable_mw")
        wide.rename_axis(index=None, columns=None).iloc[5:10]
      - |
        wide[["T_PEHE-1", "T_SGRWO-6", "T_HEYM11"]].plot(
            drawstyle="steps-post", style=["-", "--", "-"], ylabel="MW", figsize=(8, 3.5),
            color=["#C77E3C", "#3E8C97", "#155A6E"])
    needs: the publishes of 21 September 2026
    plot_alt: >-
      Step plot of output_usable_mw by settlement_date, 23 September to 5 October 2026, from the
      20:00 UTC publish kept from the 21 September fetch. T_PEHE-1 is 0, then 1,180 from 30
      September. T_HEYM11, drawn on top, is 0, then steps 262, 360, 476 to 498. T_SGRWO-6, dashed,
      moves between 89 and 299.
  related:
    - {dataset: elexon/fou2t14d, note: "The same forward availability, per fuel type instead of per unit"}
    - {dataset: elexon/bmunits_reference, note: "The register behind each unit id: name, fuel type, capacity"}
    - {dataset: elexon/remit, note: "Outage messages, to look for the outage behind a zero"}
    - {dataset: elexon/pn, note: "Each unit's notified MW per half-hour, closer to delivery"}
---

# Elexon - 2-14 Day Ahead Generation Availability by BM Unit (`UOU2T14D`)

## Overview

2-14 day-ahead generation availability per BM Unit (UOU2T14D). The unit-level companion of FOU2T14D — one availability figure per National Grid BM Unit per forecast date, 2-14 days ahead: daily rows with no settlement period (vendor row schema `AvailabilityByBmUnitDaily`). Vendor description (Insights API OpenAPI, `/datasets/UOU2T14D`): "a forward view of availability (also referred to as Output Usable data under the Grid Code) for generation and interconnector capacity, accounting for planned outages covering availability data from 2 days ahead to 14 days ahead; it is aggregated by National Grid Balancing Mechanism Units (NGC BMUs)", and "Elexon BMUs differs from NGC BMUs by including a prefix e.g. 'T_'". The vendor enforces a maximum 4-hour query window so the connector chunks requests accordingly.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://data.elexon.co.uk/bmrs/api/v1` |
| Path             | `/datasets/UOU2T14D` |
| Method           | GET |
| Auth             | None required for tested endpoints (2026-05-08). Some endpoints accept an `apikey` header (env: `ELEXON_API_KEY`); registration at https://www.elexonportal.co.uk/. |
| Rate limit       | Vendor-published: not stated. Project default 2 req/sec (asyncio.Semaphore); verified safe 2026-05-08. |
| Pagination       | Connector handles via `page=N` query param; stops when `page >= total_pages`. Reference endpoints (`/reference/bmunits/all`) are not paginated. |
| Historical depth | Several years. |
| Publication lag  | Vendor-published: not stated. Bronze for 2026-09-21 (fetched 2026-09-26) holds a publish every hour, 00:00 to 23:00 UTC, plus 00:00 on the 22nd (the publish windows include both ends); each covers 13 forecast dates, moving on a day at the 23:00 UTC publish. |
| Response format  | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `fuelType` | array | No | The fuel type to query. Add each fuel type separately. If no fuel types are supplied, all fuel types will be returned. | `CCGT` |
| `publishDateTimeFrom` | string | No | Start of the Publish Time range to query. If specified, PublishDateTimeTo must also be specified.
If both are omitted, latest published data is returned. | `2026-05-06T00:00Z` |
| `publishDateTimeTo` | string | No | End of the Publish Time range to query. If specified, PublishDateTimeFrom must also be specified.
If both are omitted, latest published data is returned. | `2026-05-06T03:00Z` |
| `bmUnit` | array | No | The BM units to query. Add each unit separately. Either the Elexon ID or the National Grid ID can be used.
If no BM unit is supplied all BM units will be returned. | `T_DRAXX-1` |
| `format` | string | No | Response data format. Use json/xml to include metadata. | `json` |

### Working curl example

```bash
# Replace <ELEXON_API_KEY> with your env var if you choose to send one (Elexon endpoints
# tested 2026-05-08 do NOT require a key; set anyway for vendor courtesy).
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://data.elexon.co.uk/bmrs/api/v1/datasets/UOU2T14D?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-06T03:00Z&format=json" \
  -o "/tmp/elexon-uou2t14d.json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/elexon/uou2t14d/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per API call (paginated requests append additional files for the same date partition).

### Bronze sample

Captured live 2026-05-08 from the https://data.elexon.co.uk/bmrs/api/v1/datasets/UOU2T14D?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-06T03:00Z&format=json:

```json
{
  "data": [
    {
      "dataset": "UOU2T14D",
      "fuelType": "BIOMASS",
      "nationalGridBmUnit": "DNBAR-1",
      "bmUnit": "2__NSMAE001",
      "publishTime": "2026-05-06T03:00:00Z",
      "forecastDate": "2026-05-08",
      "outputUsable": 36
    },
    {
      "dataset": "UOU2T14D",
      "fuelType": "BIOMASS",
      "nationalGridBmUnit": "DRAXX-1",
      "bmUnit": "T_DRAXX-1",
      "publishTime": "2026-05-06T03:00:00Z",
      "forecastDate": "2026-05-08",
      "outputUsable": 660
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/elexon/uou2t14d/year=YYYY/month=MM/uou2t14d_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.elexon.uou2t14d.UOU2T14DTransformer`
**Pydantic schema**: `gridflow.schemas.elexon.ElexonUOU2T14D` (added 2026-05-20, gridflow G5-W4).
**Dedup key**: `(settlement_date, bm_unit_id)`, plus `settlement_period` when present (it never is in the live shape), `keep="last"`, applied to one bronze day at a time (`silver/elexon/uou2t14d.py:133-136`). `published_at` is not in the key and the transformer is not `APPEND_ONLY` (unlike FOU2T14D), so each fetched day keeps one row per unit and forecast date; the surviving publish is the last row read, in sorted bronze file order (`uou2t14d.py:40`), not the newest publish. After the dedup, the Elexon publication-window filter (`base.py:1638-1642`, `1761-1805`; uou2t14d is in scope, `_publication_window.py:94-117`) drops day D's rows published at or after D+1 00:00 when day D+1's bronze owns that publish, so a boundary publish that won the dedup is removed from day D. Rows from different fetched days coexist in silver, one file per day.
**Point-in-time field**: `published_at` (vendor `publishTime`); `available_at` is added by `BaseSilverTransformer`.

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `settlement_date` | `date` | No | `settlementDate` or `forecastDate` | Settlement date (BST/GMT calendar). |
| `settlement_period` | `int` | Yes | `settlementPeriod` | Absent from silver: the feed sends `forecastDate` only, so the transformer skips it (`uou2t14d.py:112-131`). |
| `timestamp_utc` | `datetime[UTC]` | No | _derived_ | Midnight UTC of `settlement_date` when there is no period (`uou2t14d.py:125-131`). |
| `bm_unit_id` | `str` | Yes | `bmUnit` | BM Unit identifier — preserve raw casing. Vendor schema marks `bmUnit` nullable; units sent without it share one null dedup key, so one survives per forecast date per fetched day (81 null-id units per forecast date in the 2026-09-21 20:00 UTC publish). |
| `fuel_type` | `str` | Yes | `fuelType` | Fuel category (G5-W2.3: restored — was dropped before write). |
| `national_grid_bm_unit` | `str` | Yes | `nationalGridBmUnit` | National Grid BM unit identifier (G5-W2.3: restored). |
| `output_usable_mw` | `float` | No | `outputUsable` | MW. |
| `published_at` | `datetime[UTC]` | Yes | `publishDateTime` (also `publishTime`) | Publication time (G5-W2.3). |
| `data_provider` | `str` | No | _derived_ | Default `"elexon"`. |
| `ingested_at` | `datetime[UTC]` | Yes | _derived_ | When the silver transform ran (`uou2t14d.py:138-142`). |

### Silver sample

```python
[
    {
        "settlement_date": "2026-09-30",
        "timestamp_utc": "2026-09-30T00:00:00+00:00",
        "bm_unit_id": "T_PEHE-1",
        "national_grid_bm_unit": "PEHE-1",
        "fuel_type": "CCGT",
        "output_usable_mw": 1180.0,
        "published_at": "2026-09-21T20:00:00+00:00",
        "data_provider": "elexon"
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **Vendor max-chunk-hours = 4** — wider queries return HTTP 400.
- **High row count** — a 4-hour window returns every hourly publish in it, each with 13 forecast dates × every unit: 36,075 rows per window for 2026-09-21 (fetched 2026-09-26), one page each.
- **Null `bmUnit` rows collapse in silver** — the dedup key includes `bm_unit_id`, which is null for units sent with only `nationalGridBmUnit`; Polars `unique` treats nulls as equal, so one such unit survives per forecast date per fetched day (`uou2t14d.py:133-136`). `national_grid_bm_unit` is the vendor's own grain.
- **Kept publish is file order, not publish time** — see Dedup key above. Open for gridflow, not fixed here.

---

## Implementation delta

- **API max-chunk 4 hours**: `ElexonEndpoint.max_chunk_hours = 4` — connector enforces, vendor returns 400 for wider ranges.
- **`forecastDate → settlement_date`** mapping (same as FOU2T14D).
- **Pydantic schema declared** as of gridflow G5-W4: `ElexonUOU2T14D`.

### V2-FIX changelog

- **2026-05-20 — gridflow G5-W2.3 (PR #7)**: silver transformer is now
  self-describing — restores the `fuel_type` and `national_grid_bm_unit`
  columns the rename map produced but `output_cols` was dropping before
  write (P2 schema-vs-output mismatch bug). `published_at` also surfaced
  as a UTC-aware datetime under the same fix. Pre-G5 silver carried only
  the bare `bm_unit_id` + `output_usable_mw` pair — downstream readers
  had to look up fuel type / NG mapping separately.
- **2026-05-20 — gridflow G5-W4 (PR #7)**: `ElexonUOU2T14D` Pydantic class
  added to `schemas/elexon.py`.

---

## Modelling notes

TODO

---

## Links

- [Official API docs (Swagger UI)](https://bmrs.elexon.co.uk/api-documentation)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/elexon/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/elexon/uou2t14d.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/elexon.py)
- Gold view/builder
- [Domain: GB Balancing Mechanism](../../../20-domain/markets/gb-balancing-mechanism.md)
