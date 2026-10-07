---
source: entsog
dataset_key: aggregated_physical_flows
vendor: ENTSOG Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Gas entry from production, storage, LNG
  summary: >-
    Daily physical gas flow into the British balancing zone from production, storage and LNG
    terminals only, as ENTSOG aggregates it, in kWh/d.
  facts:
    vendor: "ENTSOG Transparency Platform, aggregated data, indicator Physical Flow"
    cadence: Daily, one value per gas day
    grain: One row per gas day, zone, operator, direction and adjacent system
  landscape: gas
  what_it_is: >-
    ENTSOG's aggregate flow by zone, direction and adjacent system. For the British zone gridflow
    requests only production, storage and LNG entry, plus Northern Ireland entry and exit, which
    returned no records in the responses fetched. Entry from other systems and the remaining exits
    are not requested: this is not total entry. The notebook matches each to its points in
    `physical_flows`.
  how_used:
    - Daily British-zone entry from production, storage and LNG terminals, in one table.
    - Days when gas enters the zone from storage, and how much.
    - Checking a zone aggregate against the point flows it names.
  chart:
    type: line
    silver: entsog/aggregated_physical_flows
    time: timestamp_utc
    value: value
    filter:
      - {column: operator_key, op: eq, value: UK-TSO-0001}
      - {column: direction_key, op: eq, value: entry}
    group: adjacent_systems_key
    group_map:
      Production: production
      Storage: storage
      "LNG Terminals": lng
    series_order: [production, storage, lng]
    aggregation: last
    window: {start: "2026-09-13", end: "2026-09-21"}
    unit: kWh/d
  chart_view:
    title: Production, storage and LNG entry, 13 to 21 September 2026
    caption: >-
      Silver `entsog/aggregated_physical_flows`, kWh/d as sent and provisional, gas days 13 to 21
      September 2026: entry from production, storage and LNG. Northern Ireland entry and exit
      returned nothing when fetched; other entry and exits are not requested. Not total entry.
    alt: >-
      Line chart of National Gas Transmission's daily entry into the British zone from
      entsog/aggregated_physical_flows, in kWh/d, for gas days 13 to 21 September 2026.
      Production rises from 322,977,312 on the 13th to 452,816,220 on the 18th, then falls to
      383,537,205. Storage reads 134,058,118 on the 13th, 0 on the 15th and the 18th to 20th, then
      378,788,337 on the 21st. LNG terminals stay between 54,248,476 and 71,944,652 until
      113,764,382 on the 21st.
    x_label: gas day, starting 04:00 UTC here
    key:
      - {series: production, label: Production entry, codes: Production, paint: petrol, note: "Bacton (UKCS), Barrow, Burton Point and Teesside, as `pointsNames` lists them."}
      - {series: storage, label: Storage entry, codes: Storage, paint: olive, note: "Entry from storage only: 0 on the 15th and the 18th to 20th. Storage exit is not requested."}
      - {series: lng, label: LNG terminals entry, codes: LNG Terminals, paint: clay, note: "Isle of Grain and Milford Haven together: 113,764,382 on the 21st."}
  raw_feed:
    note: >-
      One request per day to ENTSOG's `aggregatedData` endpoint with five zone filters; in the
      responses fetched, the Northern Ireland pair returned no record. Silver keeps `value` and
      `unit` unconverted.
    requests:
      - "GET https://transparency.entsog.eu/api/v1/aggregatedData?limit=-1&timeZone=UCT&from=2026-09-21&to=2026-09-21&indicator=Physical+Flow&periodType=day&pointDirection=UK\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DIE-TSO-0001entryTransmissionUK-NI\x2D\x2D\x2D\x2D\x2D\x2D%2CUK\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DIE-TSO-0001exitTransmissionUK-NI\x2D\x2D\x2D\x2D\x2D\x2D%2CUK\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DUK-TSO-0001entryLNG+Terminals%2CUK\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DUK-TSO-0001entryProduction%2CUK\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DUK-TSO-0001entryStorage"
    commands:
      - {run: gridflow ingest entsog aggregated_physical_flows --start 2026-09-13 --end 2026-09-22, comment: "bronze, end exclusive"}
      - {run: gridflow transform entsog aggregated_physical_flows --start 2026-09-13 --end 2026-09-21, comment: "silver, kWh/d kept"}
  record:
    select:
      filter:
        - {column: timestamp_utc, op: in, value: ["2026-09-18T04:00:00", "2026-09-19T04:00:00", "2026-09-20T04:00:00", "2026-09-21T04:00:00"]}
        - {column: adjacent_systems_key, op: in, value: [Production, Storage]}
      order_by: [timestamp_utc, adjacent_systems_key]
      columns: [timestamp_utc, adjacent_systems_key, direction_key, value, unit, count_point_presents, last_update_date_time, flow_status, bz_key, operator_key, points_names]
    key: [timestamp_utc, bz_key, operator_key, direction_key, adjacent_systems_key]
    caption: "Production and storage entry, gas days 18 to 21 September 2026; LNG rows left out."
    fields:
      timestamp_utc: "Start of the gas day, from the vendor `periodFrom`, in UTC"
      adjacent_systems_key: "Vendor `adjacentSystemsKey`, the category the aggregate groups its points by"
      direction_key: "Flow direction relative to the zone, lowercase as sent"
      value: "Aggregated physical flow in the row's `unit`, as sent"
      unit: "Vendor unit as sent, not converted: kWh/d in these rows"
      count_point_presents: "Vendor `countPointPresents`, as sent: 6 for storage, which names seven points"
      last_update_date_time: "The vendor's `lastUpdateDateTime`, converted to UTC; one stamp per gas day here"
      flow_status: "Vendor `flowStatus`, as sent: `Provisionnal`, ENTSOG's spelling"
      bz_key: "ENTSOG balancing zone key; `UK\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D` is the British zone"
      operator_key: ENTSOG key of the operator reporting the aggregate
      points_names: "The points the aggregate covers, separated by `|`, as sent"
      period_from: "Gas-day start as sent in `periodFrom`, converted to UTC"
      period_to: "Gas-day end as sent in `periodTo`, converted to UTC"
      indicator: "The indicator the connector requests, echoed back by the vendor"
      period_type: "`day`, the period type the connector requests"
      operator_label: Name of the operator reporting the aggregate, as sent
      tso_eic_code: Energy Identification Code of the reporting operator, as sent
      country_key: Country key of the zone, as sent
      country_label: Country name of the zone, as sent
      id: "Vendor record id, the deduplication key: zone, operator, direction, system and dates joined"
      data_set: "Vendor `dataSet` code, as sent; ENTSOG's meaning for it is not documented here"
      data_set_label: "Vendor label for the `dataSet` code, as sent"
      bz_short: Short name of the zone, as sent
      bz_long: Full name of the zone, as sent
      adjacent_systems_label: Name of the adjacent system, as sent
      year: Gas-day year as sent, kept as text
      month: Gas-day month as sent, kept as text, without a leading zero
      day: Gas-day day of month as sent, kept as text
  notebook:
    lead: >-
      Reads `silver_entsog_aggregated_physical_flows` and `silver_entsog_physical_flows`, lineage
      columns dropped, where `timestamp_utc` falls on the UTC dates given, ends included, then sets
      each aggregate beside its points' sum.
    cells:
      - |
        agg = data.entsog.query("aggregated_physical_flows", "2026-09-13", "2026-09-21")
        pts = data.entsog.query("physical_flows", "2026-09-13", "2026-09-21")
        agg["timestamp_utc"] = agg.timestamp_utc.dt.tz_convert("UTC")
        pts["timestamp_utc"] = pts.timestamp_utc.dt.tz_convert("UTC")
      - |
        wide = (agg.pivot(index="timestamp_utc", columns="adjacent_systems_key", values="value")
                .rename_axis(columns=None))
        wide
      - |
        named = agg.assign(point_label=agg.points_names.str.split("|")).explode("point_label")
        ng = pts[(pts.operator_key == "UK-TSO-0001") & (pts.direction_key == "entry")]
        summed = (named.merge(ng[["timestamp_utc", "point_label", "flow_gwh_per_day"]],
                              on=["timestamp_utc", "point_label"])
                  .groupby(["adjacent_systems_key", "timestamp_utc"]).flow_gwh_per_day.sum())
        gap = agg.set_index(["adjacent_systems_key", "timestamp_utc"]).value / 1e6 - summed
        gap.abs().groupby(level=0).max().round(6).rename("largest gap, GWh/d")
      - |
        wide[["Production", "Storage", "LNG Terminals"]].plot(
            ylabel="kWh/d", color=["#155A6E", "#66793B", "#C77E3C"], figsize=(8, 3.5))
    needs: gas days 13 to 21 September 2026, aggregate and point-level flows
    plot_alt: >-
      Line plot of the three aggregates in kWh/d against timestamp_utc for gas days 13 to 21
      September 2026, axis in 1e8. Production runs from 322,977,312 to 452,816,220 and ends
      at 383,537,205. Storage falls from 134,058,118 to 0 on the 15th, stays at 23,003,243 or
      below, then reaches 378,788,337 on the 21st. LNG terminals stay between 54,248,476 and
      71,944,652, then 113,764,382.
  related:
    - {dataset: entsog/physical_flows, note: "The point-level flows behind each aggregate, converted to GWh/d"}
    - {dataset: entsog/aggregate_interconnections, note: "ENTSOG's register of zone aggregates, including those not requested here"}
    - {dataset: entsog/balancing_zones, note: "The register of balancing zone keys, including the British zone"}
    - {dataset: entsog/connection_points, note: "The register of the points each aggregate names"}
---

# ENTSOG — Aggregated Physical Flows

## Overview

Zone-level aggregated physical flows by adjacent system (Production / Storage / LNG / interconnection). Each record is ENTSOG's daily physical flow for one balancing zone, operator, direction and adjacent system, in `kWh/d`, with the points it covers in `pointsNames` and a `countPointPresents` count. No ENTSOG definition of the aggregate is quoted here; `dataSetLabel` reads `Aggregates`. Project check, 2026-08/09 silver: every `value` equals the sum of the named points' National Gas TSO entry flows in `entsog/physical_flows` for the same gas day, to the kWh (42 of 42 rows; that table is in GWh/d). Gridflow requests only five British-zone aggregates, so this is not a zone balance (see Known issues).

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://transparency.entsog.eu/api/v1` |
| Path             | `/aggregatedData` |
| Method           | GET |
| Auth             | None (public) |
| Rate limit       | Not vendor-published; project default 5 req/s |
| Pagination       | `limit` + `offset`; project sets `limit=-1` |
| Historical depth | Not vendor-documented here |
| Publication lag  | Not vendor-documented here. 2026-08/09 bronze: `lastUpdateDateTime` 108 h to 158 h after the gas-day start, one stamp per gas day; `flowStatus` `Provisionnal` on every record |
| Response format  | JSON |
| Indicator | `Physical Flow` (only indicator served by `/aggregatedData`) |
| Time zone | `timeZone=UCT` (ENTSOG's spelling) |
| `pointDirection` filter | aggregate-zone form (`bzKey + operatorKey + directionKey + adjacentSystemsKey`) |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `from` | date | Yes | Window start | `2026-05-06` |
| `to` | date | Yes | Window end | `2026-05-06` |
| `timeZone` | str | Yes | `UCT` | `UCT` |
| `indicator` | str | No | `Physical Flow`, sent by the connector (`connectors/entsog/endpoints.py:168-180`) | `Physical Flow` |
| `periodType` | str | No | `day`, sent by the connector | `day` |
| `pointDirection` | str / list[str] | No | aggregate-zone form (`bzKey + operatorKey + directionKey + adjacentSystemsKey`); the connector sends five, comma-joined (`endpoints.py:46-54`) | `UK---------UK-TSO-0001entryProduction` |
| `forceDownload` | bool | No | Bypass cache | `true` |
| `limit` | int | No | `-1` returns all | `-1` |

### Working curl example

```bash
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://transparency.entsog.eu/api/v1/aggregatedData?from=2026-05-06&to=2026-05-06&timeZone=UCT&periodType=day&forceDownload=true&limit=1000"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsog/aggregated_physical_flows/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable.
**Granularity**: One file per fetch call.

### Bronze sample

```json
{
  "meta": {
    "limit": 1000,
    "offset": 0,
    "count": 1,
    "total": 2,
    "query": {
      "from": "2026-05-06",
      "to": "2026-05-06",
      "timeZone": "UCT"
    },
    "timezone": "CET"
  },
  "aggregatedData": [
    {
      "id": "1AggregatesUKUK---------UK-TSO-0001entryLNG Terminals2026-05-06T00:00:00+00:002026-05-07T00:00:00+00:00Physical Flow",
      "dataSet": "1",
      "dataSetLabel": "Aggregates",
      "indicator": "Physical Flow",
      "periodType": "day",
      "periodFrom": "2026-05-06T06:00:00+02:00",
      "periodTo": "2026-05-07T06:00:00+02:00",
      "countryKey": "UK",
      "countryLabel": "United Kingdom",
      "bzKey": "UK---------",
      "bzShort": "UK",
      "bzLong": "British Balancing Zone",
      "operatorKey": "UK-TSO-0001",
      "operatorLabel": "National Gas Transmission",
      "tsoEicCode": "21X-GB-A-A0A0A-7",
      "directionKey": "entry",
      "adjacentSystemsKey": "LNG Terminals",
      "adjacentSystemsLabel": "LNG Terminals",
      "year": "2026",
      "month": "5",
      "day": "6",
      "unit": "kWh/d",
      "value": 100259283,
      "countPointPresents": "2",
      "flowStatus": "Provisionnal",
      "pointsNames": "Isle of Grain|Milford Haven",
      "lastUpdateDateTime": "2026-05-08T18:33:42+02:00"
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsog/aggregated_physical_flows/year=YYYY/month=MM/aggregated_physical_flows_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsog.generic.GenericEntsogJsonTransformer (subclass AggregatedPhysicalFlowsTransformer)`
**Pydantic schema**: Generic — no Pydantic schema declared
**Dedup key**: the vendor `id`, `keep="last"`, within each day's bronze read (`silver/entsog/generic.py:193-199`). The `id` joins data set, country, zone, operator, direction, adjacent system, the gas-day dates and the indicator, so `(timestamp_utc, bz_key, operator_key, direction_key, adjacent_systems_key)` is unique in 2026-08/09 silver.
**Bronze read filter**: a record is kept only when the local date of its `periodFrom` equals the bronze day (`generic.py:157-161,332`; `silver/entsog/datetime.py:56-87,191-213`). Aggregates are one gas day long, so none is dropped: 42 bronze records, 42 silver rows in 2026-08/09.
**Point-in-time field**: none used by the pipeline. `last_update_date_time` is the vendor's `lastUpdateDateTime` as sent, converted to UTC (`generic.py:181-183`); `ingested_at` is the silver transform time (`generic.py:201-206`).

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| timestamp_utc | datetime[UTC] | Yes | derived | `period_from` copied (`generic.py:185-187`): the gas-day start, `periodFrom` 06:00+02:00 as sent, 04:00 UTC, on every 2026-08/09 row |
| period_from | datetime[UTC] | Yes | periodFrom | Converted to UTC |
| period_to | datetime[UTC] | Yes | periodTo | Converted to UTC |
| indicator | str | Yes | indicator | `Physical Flow` |
| period_type | str | Yes | periodType | `day` |
| operator_key | str | Yes | operatorKey |  |
| operator_label | str | Yes | operatorLabel | `National Gas Transmission` for `UK-TSO-0001` |
| tso_eic_code | str | Yes | tsoEicCode |  |
| direction_key | str | Yes | directionKey | `entry` on every 2026-08/09 row |
| country_key | str | Yes | countryKey |  |
| country_label | str | Yes | countryLabel |  |
| bz_key | str | Yes | bzKey |  |
| unit | str | Yes | unit | `kWh/d`, not converted (`generic.py:189-191` casts only numeric columns) |
| value | float | Yes | value | Cast to Float64 (`_NUMERIC_NAMES`, `generic.py:80-93`) |
| id | str | Yes | id | Dedup key (see above) |
| data_set | str | Yes | dataSet | `"1"` as sent |
| data_set_label | str | Yes | dataSetLabel | `Aggregates` |
| bz_short | str | Yes | bzShort |  |
| bz_long | str | Yes | bzLong |  |
| adjacent_systems_key | str | Yes | adjacentSystemsKey |  |
| adjacent_systems_label | str | Yes | adjacentSystemsLabel |  |
| year | str | Yes | year | Text as sent |
| month | str | Yes | month | Text as sent, no leading zero |
| day | str | Yes | day | Text as sent |
| count_point_presents | float | Yes | countPointPresents | Sent as text, cast to Float64 (`_NUMERIC_NAMES`) |
| flow_status | str | Yes | flowStatus | `Provisionnal` (vendor spelling) |
| points_names | str | Yes | pointsNames | Point names joined by a vertical bar |
| last_update_date_time | datetime[UTC] | Yes | lastUpdateDateTime | Converted to UTC |
| data_provider | str | No | derived | Always `entsog` |
| ingested_at | datetime[UTC] | No | derived | Silver transform time (`generic.py:201-206`) |

### Silver sample

```python
[
    {
        "timestamp_utc": "2026-09-21T04:00:00+00:00",
        "period_from": "2026-09-21T04:00:00+00:00",
        "period_to": "2026-09-22T04:00:00+00:00",
        "indicator": "Physical Flow",
        "period_type": "day",
        "operator_key": "UK-TSO-0001",
        "operator_label": "National Gas Transmission",
        "tso_eic_code": "21X-GB-A-A0A0A-7",
        "direction_key": "entry",
        "country_key": "UK",
        "country_label": "United Kingdom",
        "bz_key": "UK---------",
        "unit": "kWh/d",
        "value": 113764382.0,
        "id": "1AggregatesUKUK---------UK-TSO-0001entryLNG Terminals2026-09-21T00:00:00+00:002026-09-22T00:00:00+00:00Physical Flow",
        "data_set": "1",
        "data_set_label": "Aggregates",
        "bz_short": "UK",
        "bz_long": "British Balancing Zone",
        "adjacent_systems_key": "LNG Terminals",
        "adjacent_systems_label": "LNG Terminals",
        "year": "2026",
        "month": "9",
        "day": "21",
        "count_point_presents": 2.0,
        "flow_status": "Provisionnal",
        "points_names": "Isle of Grain|Milford Haven",
        "last_update_date_time": "2026-09-25T17:42:15+00:00",
        "data_provider": "entsog",
        "ingested_at": "2026-09-26T17:45:39+00:00"
    }
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **`pointDirection` is the aggregate-zone form**: `bzKey + operatorKey + directionKey + adjacentSystemsKey` (e.g. `UK---------UK-TSO-0001entryLNG Terminals`). NOT the per-point form used in `/operationalData`.
- **`adjacentSystemsKey` enumerates source category**: `LNG Terminals`, `Production`, `Storage`, `Distribution`, `Final Consumers`, `Transmission`, plus `Transmission<bzKey>` keys for cross-border aggregates (several zones joined by `|`), as the `aggregate_interconnections` register lists them.
- **`flowStatus: "Provisionnal"`** (vendor typo): preserve the string as-is in bronze, normalise downstream if needed.
- **HTTP 404 = empty**: as elsewhere.

- **Indicator string is exact-case**: the connector sends the exact human-readable form (`Physical Flow`, `Nomination`, `Available through UIOLI long-term`). Sending lowercase or hyphen variants returns 404.
- **`timeZone=UCT` (note typo)**: ENTSOG documents the parameter as `timeZone=UCT` rather than `UTC`. The connector spells it the vendor's way. The response `meta.timezone` echoes back `CET` regardless of the request value.
- **`pointDirection` filter**: for `/aggregatedData` the connector sends the aggregate-zone form above (`connectors/entsog/endpoints.py:46-54`), not the `operatorKey + pointKey + directionKey` form of `/operationalData`. Multi-value lists are comma-joined.
- **Missing data returns HTTP 404**: ENTSOG returns `HTTP 404` with body `{"message":"No result found"}` when an indicator/window/point combination has no rows. This is the vendor's empty convention, not a true failure. The connector's retry policy must let 404 surface.
- **Field-case duplicates**: live records may carry both `isCamRelevant` and `isCAMRelevant` shape (or `isCmpRelevant`/`isCMPRelevant`) depending on indicator. The generic silver transformer `_normalise_column_names` collapses these via `pl.coalesce` into one snake_case column.
- **Datetime placeholders**: `lastUpdateDateTime` and `originalPeriodFrom` may be empty strings, `"-"`, `"N/A"`, or human-formatted strings (`"Jan 15 2024 06:00AM"`). `parse_entsog_datetime` returns `None` for unparseable values rather than raising.
- **`directionKey` casing varies**: lowercase (`entry`/`exit`) in `/operationalData`; capitalised (`Exit`) in `/cmpUnsuccessfulRequests`. Don't compare with `==` across families.
- **Period offset is +02:00 (CET)**: even with `timeZone=UCT`, `periodFrom` carries `+02:00` (CEST in summer / `+01:00` in winter). The silver transformer's `parse_entsog_datetime` converts to UTC.
- **Requested versus returned (2026-08/09 bronze, 14 gas days)**: the connector sends five `pointDirection` filters (`endpoints.py:48-54`). Every response returns three records: National Gas TSO (`UK-TSO-0001`) entry from `LNG Terminals`, `Production` and `Storage`. The two GNI (UK) (`IE-TSO-0001`) filters for the Northern Ireland transmission aggregate are valid `aggregate_interconnections` combinations but return no record. `meta.count` is 3 against `meta.total` 6; what `total` counts is unverified.
- **Not requested**: the `aggregate_interconnections` register (2026-09-27 snapshot) lists 17 British-zone aggregates; the connector asks for five. The 12 not requested, all National Gas TSO (`UK-TSO-0001`): entry from `Transmission`, Ireland, Ireland and Northern Ireland combined, the Netherlands and IUK (5); exit to `Distribution`, `Final Consumers`, `Storage`, Ireland, Ireland and Northern Ireland combined, the Netherlands and IUK (7). The table is not total entry or a zone balance: in 2026-08/09 `physical_flows`, St. Fergus and Easington (vendor `pointType` cross-border transmission import points) carry National Gas TSO entry outside the three requested aggregates.
- **Aggregate equals the sum of its points (project check, not an ENTSOG statement)**: on every 2026-08/09 row, `value` equals the sum of `flow_gwh_per_day` × 10^6 over the `pointsNames` points' National Gas TSO entry rows in `entsog/physical_flows`, same gas day, to the kWh.
- **`countPointPresents` against `pointsNames`**: Storage names seven points and `countPointPresents` is 6. Avonmouth LNG (`LNG-00053`, vendor `pointType` "Storage point ExtEU", consistent with its place under `Storage`): its point-level physical flow is null as sent on every 2026-08/09 gas day, so the count appears to cover points that sent a value; ENTSOG does not say so here. LNG (2 names, 2) and Production (4 names, 4) agree.
- **Teesside under `Production`**: `pointsNames` lists Teesside under `Production`; in `entsog/physical_flows` it is point `LNG-00007`, whose vendor `pointType` is "Aggregated production point - TP ExtEU". The `LNG-` prefix is only the key's prefix.
- **Shared update stamps**: the three records of a gas day share one `lastUpdateDateTime`. Gas day 2026-09-16 carries the same stamp as 2026-09-14 (2026-09-20 16:30:29 UTC), and 2026-09-21 the same as 2026-09-19 (2026-09-25 17:42:15 UTC). Unexplained.
- **Zero storage entry**: Storage `value` is 0 as sent on 6 of 14 gas days in 2026-08/09 (1 and 3 August, 15 and 18 to 20 September); each named storage point sends 0 (Avonmouth LNG null) on those days. It is entry only: injection into storage would be the unrequested Storage exit aggregate.


---

## Implementation delta

- **Vendor empty convention**: HTTP 404 + `{"message":"No result found"}` for empty windows.
- **Generic transformer**: dynamic schema. Columns are derived from whatever the live response contains.

---

## Modelling notes

- Daily British-zone entry from production, storage and LNG terminals, in `kWh/d`; divide by 10^6 for the GWh/d of `entsog/physical_flows`.
- Storage here is entry only; storage exit (injection) is not requested, so this is not net storage flow.
- `flow_status` is `Provisionnal` on every 2026-08/09 row and `lastUpdateDateTime` falls 4.5 to 6.6 days after the gas-day start; whether a later fetch revises a value is unverified.
- For the point breakdown, split `points_names` on `|` and join `entsog/physical_flows` on `timestamp_utc` and `point_label` (National Gas TSO entry rows).

---

## Links

- [Official API docs (PDF)](https://transparency.entsog.eu/api/archiveDirectories/8/api-manual/TP_REG715_Documentation_TP_API%20-%20v2.1.pdf)
- `src/gridflow/connectors/entsog/endpoints.py`
- `src/gridflow/silver/entsog/generic.py`
- `src/gridflow/schemas/entsog.py`
- Gold view/builder
