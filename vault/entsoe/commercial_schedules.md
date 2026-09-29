---
source: entsoe
dataset_key: commercial_schedules
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-11
layer_coverage: bronze, silver
page:
  title: Scheduled exchanges across borders
  summary: >-
    ENTSO-E's scheduled commercial exchanges on bidding-zone borders in MW, one direction for each
    of the eight zone pairs gridflow requests.
  facts:
    vendor: ENTSO-E Transparency Platform, document type A09
    cadence: Hourly or quarter-hourly points, as sent in the responses we hold
    grain: One row per interval start, `in_Domain` zone, `out_Domain` zone and `businessType` (only `A06` here)
  landscape: market
  what_it_is: >-
    The MW scheduled across a border after capacity allocation: traded exchanges, not the physical
    flows in `cross_border_flows`. A reply can hold a day-ahead series (`A01`) and an `A05` series
    (total, in ENTSO-E's code list); gridflow drops the contract type and keeps `A05`, listed last
    (project check), so the day-ahead series is lost. One direction per border, so no netting.
  how_used:
    - Scheduled imports into GB on each interconnector border, hour by hour.
    - Scheduled exchange set against physical flow on the same border.
    - A feature for GB price and interconnector-spread models.
  chart:
    type: line
    silver: entsoe/commercial_schedules
    time: timestamp_utc
    value: quantity_mw
    filter:
      - {column: in_area_code, op: eq, value: "10YGB\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DA"}
    group: out_area_code
    group_map:
      "10YFR\x2DRTE\x2D\x2D\x2D\x2D\x2D\x2DC": france
      "10YBE\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D2": belgium
      "10YNL\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DL": netherlands
      "10Y1001A1001A59C": ireland
    series_order: [france, belgium, netherlands, ireland]
    aggregation: mean
    window: {start: "2026-09-14", end: "2026-09-20"}
    unit: MW
  chart_view:
    title: Scheduled into GB by border, 14 to 20 September 2026
    caption: >-
      Silver `entsoe/commercial_schedules`, MW, rows with `in_area_code` GB, one value per border
      per hour as sent, 14 to 20 September 2026 UTC. Each line is the `A05` schedule. gridflow
      never requests the reverse direction, so exports from GB are not drawn.
    alt: >-
      Line chart of scheduled MW into GB from entsoe/commercial_schedules, hourly, 14 to 20
      September 2026 UTC. France is highest, near 3,030 MW for hours on every day except the 19th
      (1,979 MW at most), dipping below 210 MW daily. Belgium moves between zero and 1,055 MW, and
      reaches 660 MW at most on the 17th. The Netherlands is zero until the 19th, then reaches
      410 MW that day and 1,172 MW on the 20th. Ireland (SEM) is zero except on the 14th, 16th and
      17th, 281 MW at most.
    x_label: UTC date; hourly values
    key:
      - {series: france, label: From France, codes: "out_Domain FR", paint: petrol, note: "Tracks the import part of Elexon's INTFR, INTIFA2 and INTELEC, summed (project check)."}
      - {series: belgium, label: From Belgium, codes: "out_Domain BE", paint: horizon, note: "Moves with Elexon's INTNEM imports (project check), not hour for hour; zero for 11 hours on the 17th."}
      - {series: netherlands, label: From the Netherlands, codes: "out_Domain NL", paint: olive, note: "Zero until the 19th, then up to 410 MW that day and 1,172 MW on the 20th."}
      - {series: ireland, label: From Ireland (SEM), codes: "out_Domain IE-SEM", paint: clay, note: "Bidding zone IE-SEM. Zero except on the 14th, 16th and 17th; 281 MW at most."}
  raw_feed:
    note: >-
      One GET per ordered zone pair per UTC day, with no contract filter, so a reply can carry two
      series. `gridflow ingest` writes bronze; `gridflow transform` writes silver.
    requests:
      - "GET https://web-api.tp.entsoe.eu/api?documentType=A09&periodStart=202609160000&periodEnd=202609170000&in_Domain=10YGB\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DA&out_Domain=10YFR\x2DRTE\x2D\x2D\x2D\x2D\x2D\x2DC&securityToken=$ENTSOE_API_KEY"
    commands:
      - {run: gridflow ingest entsoe commercial_schedules --start 2026-09-14 --end 2026-09-21, comment: "bronze; end date excluded"}
      - {run: gridflow transform entsoe commercial_schedules --start 2026-09-14 --end 2026-09-20, comment: "bronze to silver; end included"}
  record:
    select:
      filter:
        - {column: timestamp_utc, op: eq, value: "2026-09-16T21:00:00Z"}
      order_by: [in_area_code, out_area_code]
      columns: [timestamp_utc, in_area_code, out_area_code, quantity_mw, business_type, resolution, published_at]
    key: [timestamp_utc, in_area_code, out_area_code, business_type]
    caption: "The eight ordered zone pairs gridflow requests, at 21:00 UTC on 16 September 2026."
    fields:
      timestamp_utc: "Interval start, UTC: period start plus (position minus 1) times resolution"
      in_area_code: "The `in_Domain` EIC, the receiving zone; GB rows track imports (project check)"
      out_area_code: "The `out_Domain` EIC, the sending zone across the border"
      quantity_mw: "MW of the last-listed series, `A05` here; A03 points repeat until the next"
      business_type: "TimeSeries `businessType` as sent, `A06` here; the contract type is dropped"
      resolution: "Interval length as sent: `PT60M` on GB borders here, `PT15M` elsewhere"
      published_at: "Response `createdDateTime`, UTC: a fetch-time stamp, within seconds of gridflow's request"
  notebook:
    lead: >-
      Returns a pandas DataFrame from `silver_entsoe_commercial_schedules`, filtered on
      `timestamp_utc` with both ends included. Lineage columns are dropped and rows come ordered by
      `timestamp_utc` only, so sort before pivoting.
    cells:
      - |
        df = data.entsoe.query("commercial_schedules", "2026-09-14", "2026-09-20")
        df["timestamp_utc"] = df["timestamp_utc"].dt.tz_convert("UTC")
        df = df.sort_values(["timestamp_utc", "in_area_code", "out_area_code"])
      - df[["timestamp_utc", "in_area_code", "out_area_code", "quantity_mw", "resolution"]].head(8)
      - |
        gb = df[df["in_area_code"].str.startswith("10YGB")].copy()
        gb["border"] = gb["out_area_code"].str[3:5].replace({"10": "IE-SEM"})
        hourly = gb.pivot_table(index="timestamp_utc", columns="border", values="quantity_mw")
        hourly[["FR", "BE", "NL", "IE-SEM"]].plot(ylabel="MW", color=["#155A6E", "#3E8C97", "#66793B", "#C77E3C"], figsize=(8, 3.5))
    needs: 14 to 20 September 2026
    plot_alt: >-
      Line plot of hourly quantity_mw into GB, one line per border (FR, BE, NL, IE-SEM), 14 to 20
      September 2026 UTC. FR sits near 3,030 MW for hours on most days, 1,979 MW at most on the
      19th; BE peaks near 1,050 MW; NL is zero until the 19th, then near 1,170 MW; IE-SEM stays
      near zero.
  related:
    - {dataset: entsoe/cross_border_flows, note: "Physical flow on the same eight ordered pairs, not the schedule"}
    - {dataset: entsoe/net_positions, note: "A zone's net position from implicit auctions, not one border's"}
    - {dataset: entsoe/net_transfer_capacity, note: "Forecast transfer capacity on the same ordered pairs"}
    - {dataset: elexon/fuelhh, note: "Elexon's interconnector flows, used here to check the direction"}
---

# ENTSO-E - Commercial Schedules (A09)

## Overview

Aggregated final commercial schedules per zone pair after capacity allocation.
Article 12.1.E of Regulation (EC) 543/2013. Each TimeSeries records nominated
commercial flow on a directional border for the relevant trading horizon.

Current status: this is the sole active A09 connector dataset. The former
`commercial_schedules_net_positions` key was removed as an identical registry
duplicate and is retained only as a deprecated pointer page.

## API endpoint

| Property | Value |
|---|---|
| Base URL | `https://web-api.tp.entsoe.eu` |
| Path | `/api` |
| Method | GET |
| Auth | Query param `securityToken=$ENTSOE_API_KEY` |
| Rate limit | 1 req/s default |
| Pagination | None |
| Historical depth | 2014-12-05 onward, border-dependent |
| Publication lag | D-1 after gate closure |
| Response format | XML |

### ENTSO-E parameter tuple

| Field | Value |
|---|---|
| `documentType` | `A09` |
| `processType` | omitted |
| `businessType` request parameter | omitted; server returns `A06` on TimeSeries |
| `contract_MarketAgreement.Type` | optional request filter, present in TimeSeries payload |
| Domain params | `in_Domain` + `out_Domain` |

### Query parameters

| Parameter | Required | Description |
|---|---|---|
| `securityToken` | Yes | API key |
| `documentType` | Yes | `A09` |
| `in_Domain` | Yes | Receiving zone EIC (project check; see Known issues) |
| `out_Domain` | Yes | Sending zone EIC |
| `contract_MarketAgreement.Type` | No | Filter horizon, e.g. `A01` daily |
| `periodStart` / `periodEnd` | Yes | `yyyymmddHHMM` UTC |

## Bronze layer

Path:
`{data_root}/bronze/entsoe/commercial_schedules/YYYY/MM/DD/raw_<uuid>.xml`

Granularity: one file per `(in_Domain, out_Domain, day)` API call.

## Silver layer

Path:
`{data_root}/silver/entsoe/commercial_schedules/year=YYYY/month=MM/commercial_schedules_YYYYMMDD.parquet`

Transformer:
`gridflow.silver.entsoe.h6_market.CommercialSchedulesTransformer`

Pydantic schema:
`gridflow.schemas.entsoe.EntsoeTransmissionMarketQuantity`

Dedup key:
`(timestamp_utc, in_area_code, out_area_code, business_type)`

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|---|---|---|---|---|
| `timestamp_utc` | `datetime` UTC | No | period + position | Expanded from TimeSeries period |
| `in_area_code` | `str` | No | `in_Domain.mRID` | EIC |
| `out_area_code` | `str` | No | `out_Domain.mRID` | EIC |
| `quantity_mw` | `float` | No | `Point.quantity` | Commercial nomination in MW |
| `business_type` | `str` or `None` | Yes | TimeSeries `businessType` | Usually `A06` |
| `resolution` | `str` or `None` | Yes | `Period.resolution` | e.g. `PT60M` |
| `published_at` | `datetime` UTC or `None` | Yes | document `createdDateTime` | Fetch-time stamp, within seconds of the request (`h6_market.py:105,114`) |
| `data_provider` | `str` | No | derived | Constant `entsoe` |
| `ingested_at` | `datetime` UTC or `None` | Yes | derived | Transformer run time |
| `event_time` | `datetime` UTC | No | base transformer | Added at write time |
| `available_at` | `datetime` UTC | No | base transformer | Added at write time |
| `source_run_id` | `str` | No | base transformer | Added at write time |
| `dataset_version` | `str` | No | base transformer | Added at write time |

## Gold layer

None implemented.

## Known issues and gotchas

- A09 is directional. Net commercial position requires both directions.
  gridflow requests one direction per border only, the eight ordered pairs in
  `connectors/entsoe/client.py:40` `_FLOW_PAIRS`, so silver cannot be netted.
  Direction (project check, 2026-09-29, not an ENTSO-E quote): rows with
  `in_Domain` = GB track the positive (import to GB) part of Elexon FUELHH
  interconnector flows for 1 August to 21 September 2026 (correlation 0.85 to
  0.94 per border, against the positive part of the summed Elexon flows,
  hourly), so `in_Domain` is the receiving zone. The entsoe-py client
  assigns `in_Domain` the "to" zone, which agrees.
- Two contract types per reply, one kept (2026-09-29, from bronze): with no
  `contract_MarketAgreement.Type` filter, a reply can carry a day-ahead series
  (`A01`) and an `A05` series. ENTSO-E Code Lists v29r0, section 3.8
  `ContractTypeList`: `A05` "Total", "the sum of all capacity contract types
  for the period covered"; `A01` "Daily"
  (https://eepublicdownloads.azureedge.net/clean-documents/EDI/Library/Core/entso-e-code-list-v29r0.pdf).
  This is the generic EDI code list, not the A09 guide; it does not make
  `A05` equal `A01` plus more (on FR to DE-LU `A05` is sometimes lower). The GB to IE-SEM replies carried
  `A05` only. The parser has no branch for
  `contract_MarketAgreement.type` (`parsers.py:320-328`), the transformer's
  dedup key omits it and keeps the last row (`h6_market.py:91-98`), so silver
  holds whichever series the reply lists last. Every reply checked lists `A01`
  then `A05`, and every silver row equals the `A05` value. The day-ahead
  series is discarded.
- Variable-resolution `curveType A03` can compress unchanged intervals; the
  previous value persists until the next point.
- `contract_MarketAgreement.type` in the payload identifies the horizon
  (`A01` daily, `A02` weekly, etc.).
- `commercial_schedules_net_positions` is not active in current `gridflow`
  master.

## Implementation delta

- Live validation 2026-05-08: GB -> FR for 2026-05-06 returned
  `Publication_MarketDocument` with 2 TimeSeries and hourly points. PASS.
- A09 dedup resolved in V2 on 2026-05-09: `commercial_schedules` is now the
  sole active A09 entry. Live re-validation for GB -> FR with
  `contract_MarketAgreement.Type=A01` returned HTTP 200 and 3078 bytes.
- A real signed `net_position_mw` derivation remains a backlog item.

## Changelog

- **2026-05-11.** Reverified against current `gridflow` master docs and
  active counts.
- **2026-05-09.** V2-FIX-05 / ADR-019 A09 registry dedup: dropped
  `commercial_schedules_net_positions`.
- **2026-05-08.** Live-validated; A09 registry duplication surfaced.

## Links

- [Official API docs (PDF)](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.pdf)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/entsoe/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/entsoe/h6_market.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/entsoe.py)
