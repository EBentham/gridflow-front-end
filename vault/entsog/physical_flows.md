---
source: entsog
dataset_key: physical_flows
vendor: ENTSOG Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Physical gas flows by point
  summary: >-
    Daily physical gas flow from ENTSOG's Transparency Platform, fetched with no point filter, per
    reporting operator and direction, in GWh/d.
  facts:
    vendor: ENTSOG Transparency Platform, indicator Physical Flow
    cadence: Daily, one value per gas day
    grain: One row per gas day, point, operator and direction
  landscape: gas
  what_it_is: >-
    ENTSOG's daily physical flow, requested with no point filter, from GB and European operators,
    converted to GWh/d. Each operator reports its own side of a point, so one cross-border flow
    can appear twice: one operator's exit and the neighbour's entry. The gas day's start hour
    varies between operators, so `timestamp_utc` differs between them on the same day.
  how_used:
    - Daily GB exit flows on the BBL, IUK and Moffat interconnections.
    - Supply by entry point, such as St Fergus, Easington and Milford Haven.
    - Checking one operator's report of a flow against its neighbour's.
  chart:
    type: line
    silver: entsog/physical_flows
    time: timestamp_utc
    value: flow_gwh_per_day
    filter:
      - {column: operator_key, op: eq, value: UK-TSO-0001}
      - {column: point_key, op: in, value: [ITP-00090, ITP-00207, ITP-00005, LNG-00049]}
    group: point_key
    group_map:
      ITP-00090: moffat
      ITP-00207: bacton_bbl
      ITP-00005: bacton_iuk
      LNG-00049: milford_haven
    series_order: [moffat, bacton_bbl, bacton_iuk, milford_haven]
    aggregation: last
    window: {start: "2026-09-13", end: "2026-09-21"}
    unit: GWh/d
  chart_view:
    title: GB interconnection and LNG flows, 13 to 21 September 2026
    caption: >-
      Silver `entsog/physical_flows`, GWh/d, gas days 13 to 21 September 2026, one row per point
      and day as sent: National Gas TSO's own report. Each pipeline flow is reported again by
      the operator on the far side, not drawn here.
    alt: >-
      Line chart of National Gas TSO's daily physical flow from entsog/physical_flows, in GWh/d,
      for gas days 13 to 21 September 2026. Moffat exit falls from 180.0 on the 13th to 131.4 on
      the 19th, then returns to 179.7. Bacton (BBL) exit rises from 123.5 to 176.4 on the 15th,
      then falls to 64.4 on the 21st. Bacton (IUK) exit is zero until 175.2 on the 21st. Milford
      Haven entry stays between 54.2 and 71.9.
    x_label: gas day, starting 04:00 UTC at these points
    key:
      - {series: moffat, label: Moffat exit, codes: ITP-00090, paint: petrol, note: "GNI reports this flow as entry at Moffat (IE), within 0.2 GWh/d here."}
      - {series: bacton_bbl, label: "Bacton (BBL) exit", codes: ITP-00207, paint: olive, note: "BBL company reports it again as entry at Bacton (BBL)."}
      - {series: bacton_iuk, label: "Bacton (IUK) exit", codes: ITP-00005, paint: horizon, note: "Zero until 21 September, then 175.2 GWh/d."}
      - {series: milford_haven, label: Milford Haven entry, codes: LNG-00049, paint: clay, note: "ENTSOG's point type: LNG entry point."}
  raw_feed:
    note: >-
      One request per date to ENTSOG's `operationalData` endpoint, with no point filter.
      `gridflow ingest` writes each response to bronze; `gridflow transform` converts kWh/d to
      GWh/d in silver.
    requests:
      - "GET https://transparency.entsog.eu/api/v1/operationalData?limit=-1&timeZone=UCT&from=2026-09-13&to=2026-09-13&indicator=Physical+Flow&periodType=day"
    commands:
      - {run: gridflow ingest entsog physical_flows --start 2026-09-13 --end 2026-09-22, comment: "bronze; the end is exclusive"}
      - {run: gridflow transform entsog physical_flows --start 2026-09-13 --end 2026-09-21, comment: "bronze to silver, in GWh/d"}
  record:
    select:
      filter:
        - {column: timestamp_utc, op: eq, value: "2026-09-21T04:00:00"}
        - {column: point_key, op: in, value: [ITP-00005, ITP-00090, ITP-00207, ITP-00495]}
      order_by: [point_key, operator_key, direction_key]
    mark: {operator_key: IE-TSO-0002}
    key: [timestamp_utc, point_key, operator_key, direction_key]
    caption: "Gas day 21 September 2026 at three GB interconnections, both sides' reports together."
    fields:
      timestamp_utc: "Start of the operator's gas day, from the vendor `periodFrom`, in UTC"
      point_key: "ENTSOG point key, such as `ITP-00090` for Moffat"
      point_label: ENTSOG's name for the point, as sent
      operator_key: ENTSOG key of the operator reporting this row
      operator_label: Name of the operator reporting this row, as sent
      direction_key: "`entry` or `exit`, lowercase as sent, from the reporting operator's side"
      flow_gwh_per_day: Physical flow in GWh/d, converted from the vendor unit; null when none sent
      unit: "Same on every row: GWh/d, the unit after conversion"
      data_provider: "Same on every row: entsog"
      ingested_at: When the silver transform ran
  notebook:
    lead: >-
      Reads `silver_entsog_physical_flows`, lineage columns dropped, where `timestamp_utc` falls on
      the UTC dates given, ends included. An operator whose gas day starts the evening before in
      UTC loses its first gas day.
    cells:
      - df = data.entsog.query("physical_flows", "2026-09-13", "2026-09-21")
      - |
        bbl = df[df.point_label == "Bacton (BBL)"]
        bbl[["timestamp_utc", "operator_label", "direction_key", "flow_gwh_per_day"]].head(6)
      - |
        ng = bbl[bbl.operator_key == "UK-TSO-0001"]
        ng.plot(x="timestamp_utc", y="flow_gwh_per_day", ylabel="GWh/d",
                color="#66793B", figsize=(8, 3.5))
    needs: gas days 13 to 21 September 2026
    plot_alt: >-
      Line plot of National Gas TSO's Bacton (BBL) exit flow_gwh_per_day against timestamp_utc for
      gas days 13 to 21 September 2026: 123.5 GWh/d on the 13th, rising to 176.4 on the 15th,
      falling to 105.1 on the 18th, back to 126.9 on the 19th and down to 64.4 on the 21st.
  related:
    - {dataset: entsog/nominations, note: "Nominations at the same GB points, from the same endpoint"}
    - {dataset: entsog/allocations, note: "Allocations at the same GB points, from the same endpoint"}
    - {dataset: entsog/aggregated_physical_flows, note: Physical flow summed by balancing zone rather than by point}
    - {dataset: entsog/operator_point_directions, note: "The register of the operator, point and direction keys used here"}
---

# ENTSOG — Physical Flows (`indicator=Physical Flow`)

## Overview

Daily physical gas flows at each operator-point-direction (volumetric throughput delivered). The connector requests `periodType=day` only (`gridflow/connectors/entsog/endpoints.py:16,77-80`).

The dataset is one of 19 indicators served by the same `/operationalData`
endpoint. The (operator, point, direction) tuple selects which physical
location to read; the `indicator` query parameter selects which series
(physical flow, nomination, allocation, etc.) is returned. Records carry
the daily `periodFrom` / `periodTo` window and a `value` in `kWh/d` (or
indicator-specific units for content/quality series).

→ Related concepts:
  [Gas day](../../../20-domain/concepts/gas-day.md)
  [Nominations vs allocations](../../../20-domain/markets/gas-nominations.md)

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://transparency.entsog.eu/api/v1` |
| Path             | `/operationalData` |
| Method           | GET |
| Auth             | None (public) |
| Rate limit       | Not vendor-published; project default 5 req/s, validation throttled to 1 req/s |
| Pagination       | `limit` + `offset`; project sets `limit=-1` (all records) |
| Historical depth | Approx. 2010 onwards (operator-dependent) |
| Publication lag  | Same-day for `Provisional` flow status; revised within ~1 week |
| Response format  | JSON |
| Indicator | `Physical Flow` (exact-case — vendor rejects lowercase or hyphen variants) |
| Time zone | `timeZone=UCT` (ENTSOG's spelling — note the typo; not `UTC`) |
| `pointDirection` filter | `operatorKey + pointKey + directionKey` concatenated, no separator (e.g. `UK-TSO-0001ITP-00005exit`) — omitted by connector for `physical_flows` |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `indicator` | str | Yes | Exact-case indicator name | `Physical Flow` |
| `from` | date (YYYY-MM-DD) | Yes | Window start (gas day) | `2026-05-06` |
| `to` | date (YYYY-MM-DD) | Yes | Window end (inclusive) | `2026-05-06` |
| `timeZone` | str | Yes | `UCT` (vendor typo for UTC) | `UCT` |
| `periodType` | str | No | `day` (default) or `hour` | `day` |
| `pointDirection` | str / list[str] | No | Connector deliberately omits this for `physical_flows` — full-system query | (none in default) |
| `forceDownload` | bool | No | Bypass server-side cache | `true` |
| `limit` | int | No | `-1` returns all records | `-1` |

### Working curl example

```bash
# physical_flows: connector deliberately omits the pointDirection filter — full-system fetch
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://transparency.entsog.eu/api/v1/operationalData?from=2026-05-06&to=2026-05-06&timeZone=UCT&indicator=Physical%20Flow&periodType=day&forceDownload=true&limit=1000"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsog/physical_flows/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per `fetch()` call (one calendar day per file by convention)

### Bronze sample

```json
{
  "meta": {
    "limit": 1000,
    "offset": 0,
    "count": 1,
    "total": 2,
    "query": {
      "indicator": [
        "Physical Flow"
      ],
      "periodType": "day",
      "pointDirection": "UK-TSO-0001ITP-00005exit",
      "from": "2026-05-06",
      "to": "2026-05-06",
      "timeZone": "UCT"
    },
    "timezone": "CET"
  },
  "operationalData": [
    {
      "id": "1Physical Flowday2026-05-062026-05-07UK-TSO-0001ITP-00005exitkWh/d",
      "dataSet": 1,
      "indicator": "Physical Flow",
      "periodType": "day",
      "periodFrom": "2026-05-06T06:00:00+02:00",
      "periodTo": "2026-05-07T06:00:00+02:00",
      "operatorKey": "UK-TSO-0001",
      "tsoEicCode": "21X-GB-A-A0A0A-7",
      "operatorLabel": "National Gas TSO",
      "pointKey": "ITP-00005",
      "pointLabel": "Bacton (IUK)",
      "tsoItemIdentifier": "21Z000000000083P",
      "directionKey": "exit",
      "unit": "kWh/d",
      "itemRemarks": null,
      "generalRemarks": null,
      "value": 203102928,
      "lastUpdateDateTime": "2026-05-08T19:57:09+02:00",
      "isUnlimited": null,
      "flowStatus": "Provisional",
      "interruptionType": null,
      "restorationInformation": null,
      "capacityType": null,
      "capacityBookingStatus": null,
      "isCamRelevant": false,
      "isNA": null,
      "originalPeriodFrom": null,
      "isCmpRelevant": false,
      "bookingPlatformKey": "PRISMA",
      "bookingPlatformLabel": null,
      "bookingPlatformURL": "https://platform.prisma-capacity.eu/",
      "interruptionCalculationRemark": null,
      "pointType": "Cross-Border Transmission IP between EU and ExtEU",
      "idPointType": 23,
      "isArchived": false
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsog/physical_flows/year=YYYY/month=MM/physical_flows_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsog.PhysicalFlowsTransformer`
**Pydantic schema**: `gridflow.schemas.entsog.EntsogPhysicalFlow`
**Dedup key**: `(timestamp_utc, point_key, operator_key, direction_key)` — fields uniquely identifying one daily record per series
**Point-in-time field**: none in silver. The vendor's `lastUpdateDateTime` stays in bronze; the transformer does not output it (`gridflow/silver/entsog/physical_flows.py:254-265`).

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `timestamp_utc` | `datetime` | No | `periodFrom` | UTC-aware, derived in silver: `periodFrom` (sent with a `+02:00` offset in September 2026 bronze) converted to UTC (`gridflow/silver/entsog/datetime.py:26-45`). The silver file for date D holds rows whose `periodFrom` date, as sent, is D (`datetime.py:199-206`). Start hours differ by operator and point: 2026-09 bronze carries `periodFrom` hours from 23:00 to 07:00 `+02:00`, so a row can fall on the UTC evening before. |
| `point_key` | `str` | No | `pointKey` | Identifies the gas transmission point. Required. |
| `point_label` | `str` | No | `pointLabel` | Default "" in canonical (EntsogPhysicalFlow.point_label: str = ""). |
| `operator_key` | `str` | No | `operatorKey` | Default "" in canonical. |
| `operator_label` | `str` | No | `operatorLabel` | Default "" in canonical. |
| `direction_key` | `str` | No | `directionKey` | Default "" in canonical. "entry" or "exit". |
| `flow_gwh_per_day` | `float` | Yes | derived from `value` x unit-conversion | Daily physical flow in GWh/d. `value` times an explicit factor per vendor unit (`kWh/d` x 1e-6, `kWh/h` x 24e-6, `MWh/d` x 1e-3, `MWh/h` x 24e-3, `GWh/d` x 1, `GWh/h` x 24); a row with any other unit is dropped with a warning (`physical_flows.py:38-51,197-224`). Null when the vendor sends no value; schema default `None` (`schemas/entsog.py:21`). |
| `unit` | `str` | No | `unit` | Always `"GWh/d"`: overwritten after conversion, so it never carries the raw vendor unit (`physical_flows.py:246-250`). |
| `data_provider` | `str` | No | derived | Always `"entsog"` (canonical default). |
| `ingested_at` | `datetime[UTC]` | No | derived | When the silver transform ran: `datetime.now(UTC)` stamped by the transformer (`physical_flows.py:241-245`). |

### Silver sample

```python
[
    {
        "timestamp_utc": "2026-05-06T04:00:00+00:00",
        "point_key": "ITP-00005",
        "point_label": "Bacton (IUK)",
        "operator_key": "UK-TSO-0001",
        "operator_label": "National Gas TSO",
        "direction_key": "exit",
        "flow_gwh_per_day": 203.102928,
        "unit": "GWh/d",
        "data_provider": "entsog"
    }
]
```

---

## Bronze response keys

The ENTSO-G physical-flows endpoint returns these raw keys in each bronze record. The silver layer consolidates them into the schema table above; raw keys are preserved here for reference only.

Raw bronze fields (not in silver): `id`, `dataSet`, `indicator`, `periodType`, `periodFrom`, `periodTo`, `tsoEicCode`, `tsoItemIdentifier`, `itemRemarks`, `generalRemarks`, `value`, `lastUpdateDateTime`, `isUnlimited`, `flowStatus`, `interruptionType`, `restorationInformation`, `capacityType`, `capacityBookingStatus`, `isCamRelevant`, `isNA`, `originalPeriodFrom`, `isCmpRelevant`, `bookingPlatformKey`, `bookingPlatformLabel`, `bookingPlatformURL`, `interruptionCalculationRemark`, `pointType`, `idPointType`, `isArchived`.

These keys are available in the bronze layer at `{data_root}/bronze/entsog/physical_flows/`. The silver transformer selects and normalises only the fields listed in the schema table above.

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **Indicator string is exact-case**: the connector sends the exact human-readable form (`Physical Flow`, `Nomination`, `Available through UIOLI long-term`). Sending lowercase or hyphen variants returns 404.
- **`timeZone=UCT` (note typo)**: ENTSOG documents the parameter as `timeZone=UCT` rather than `UTC`. The connector spells it the vendor's way. The response `meta.timezone` echoes back `CET` regardless of the request value.
- **`pointDirection` filter**: built as `operatorKey + pointKey + directionKey` concatenated with no separator (e.g. `UK-TSO-0001ITP-00005exit`). Multi-value lists are comma-joined.
- **Missing data returns HTTP 404**: ENTSOG returns `HTTP 404` with body `{"message":"No result found"}` when an indicator/window/point combination has no rows. This is the vendor's empty convention, not a true failure. The connector's retry policy must let 404 surface.
- **Field-case duplicates**: live records may carry both `isCamRelevant` and `isCAMRelevant` shape (or `isCmpRelevant`/`isCMPRelevant`) depending on indicator. The generic silver transformer `_normalise_column_names` collapses these via `pl.coalesce` into one snake_case column.
- **Datetime placeholders**: `lastUpdateDateTime` and `originalPeriodFrom` may be empty strings, `"-"`, `"N/A"`, or human-formatted strings (`"Jan 15 2024 06:00AM"`). `parse_entsog_datetime` returns `None` for unparseable values rather than raising.
- **`directionKey` casing varies**: lowercase (`entry`/`exit`) in `/operationalData`; capitalised (`Exit`) in `/cmpUnsuccessfulRequests`. Don't compare with `==` across families.
- **Period offset is +02:00 (CET)**: even with `timeZone=UCT`, `periodFrom` carries `+02:00` (CEST in summer / `+01:00` in winter). The silver transformer's `parse_entsog_datetime` converts to UTC.

- **`physical_flows` deliberately drops the `pointDirection` filter** in the connector to fetch a full-system snapshot in one call. All other operationalData datasets attach `DEFAULT_POINT_DIRECTIONS` from `endpoints.py`.

---

## Implementation delta

- **No documented discrepancies** for this indicator. Live API returns the indicator name in `meta.fields` matching the code's exact-case constant in `OPERATIONAL_INDICATORS`.
- **Synthetic fixture**: `tests/fixtures/entsog/physical_flows_response.json` carries placeholder `pointKey: "IUK"` and `operatorKey: "OP-IUK"`. Live data uses real keys (`ITP-00005`, `UK-TSO-0001`). Fixture regeneration is deferred (silver tests depend on the placeholder shape).

---

## Modelling notes

- Used as raw input to gas balance / interconnector flow features in `gridflow_models/`.
- Target candidates: directional flow magnitude (entry vs exit per point).
- Filter on `flowStatus == 'Confirmed'` for backtesting; `Provisional` for live model serving. `flowStatus` is in bronze only: silver does not carry it (`physical_flows.py:254-265`).
- Join with `operator_point_directions` to attach country, balancing zone, and CAM-relevant flags.

---

## Links

- [Official API docs (PDF)](https://transparency.entsog.eu/api/archiveDirectories/8/api-manual/TP_REG715_Documentation_TP_API%20-%20v2.1.pdf)
- `src/gridflow/connectors/entsog/endpoints.py`
- `src/gridflow/silver/entsog/physical_flows.py`
- `src/gridflow/schemas/entsog.py`
- Gold view/builder
- [Domain: gas day](../../../20-domain/concepts/gas-day.md)
