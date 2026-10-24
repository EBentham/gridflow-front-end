---
source: entsog
dataset_key: cmp_unsuccessful_requests
vendor: ENTSOG Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
---

# ENTSOG — Cmp Unsuccessful Requests

## Overview

CMP (congestion management procedures) unsuccessful requests: per operator, point, direction and capacity product, the requested, allocated and unallocated volume in the record's `unit`, and an occurrence count (`occurenceCount`, the vendor's spelling). ENTSOG also sends statement rows, one per operator, point, direction and neighbouring operator, usually "Currently there are no request for firm capacity products on this point with a duration of one month or longer that weren't successfully fulfilled." On 3 August 2026 some points carry both a record and a statement row, and some points in the `operator_point_directions` register carry neither. `occurenceCount` is not defined in any ENTSOG text quoted here. No ENTSOG definition of the fields is quoted here.

→ Related concepts:
  [Gas day](../../../20-domain/concepts/gas-day.md)

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://transparency.entsog.eu/api/v1` |
| Path             | `/cmpUnsuccessfulRequests` |
| Method           | GET |
| Auth             | None (public) |
| Rate limit       | Not vendor-published; project default 5 req/s |
| Pagination       | `limit` + `offset`; project sets `limit=-1` |
| Historical depth | TODO |
| Publication lag  | TODO |
| Response format  | JSON |
| Time zone | `timeZone=UCT` (ENTSOG's spelling — vendor typo) |
| `pointDirection` filter | Optional. Same `operatorKey + pointKey + directionKey` form as `/operationalData` |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `from` | date (YYYY-MM-DD) | Yes | Window start | `2026-05-06` |
| `to` | date (YYYY-MM-DD) | Yes | Window end | `2026-05-06` |
| `timeZone` | str | Yes | `UCT` | `UCT` |
| `periodType` | str | No | `day` | `day` |
| `pointDirection` | str / list[str] | No | Optional point filter | `UK-TSO-0001ITP-00005exit` |
| `forceDownload` | bool | No | Bypass cache | `true` |
| `limit` | int | No | `-1` returns all | `-1` |

### Working curl example

```bash
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://transparency.entsog.eu/api/v1/cmpUnsuccessfulRequests?from=2026-05-06&to=2026-05-06&timeZone=UCT&periodType=day&forceDownload=true&limit=1000"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsog/cmp_unsuccessful_requests/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable.
**Granularity**: One file per fetch call (per calendar day window).

### Bronze sample

```json
{
  "meta": {
    "limit": 1000,
    "offset": 0,
    "count": 1,
    "total": 248,
    "query": {
      "from": "2026-05-06",
      "to": "2026-05-06",
      "timeZone": "UCT",
      "periodType": "day"
    },
    "timezone": "CET"
  },
  "cmpUnsuccessfulRequests": [
    {
      "auctionFrom": "N/A",
      "auctionTo": "N/A",
      "capacityFrom": "2025-10-01T06:00:00+02:00",
      "capacityTo": "2026-10-01T06:00:00+02:00",
      "operatorKey": "FR-TSO-0003",
      "tsoEicCode": "21X-FR-A-A0A0A-S",
      "operatorLabel": "NaTran",
      "pointKey": "ITP-00526",
      "pointLabel": "VIRTUALYS",
      "tsoItemIdentifier": "21Z0000000004847",
      "directionKey": "Exit",
      "unit": "kWh/d",
      "itemRemarks": null,
      "generalRemarks": null,
      "requestedVolume": 3458880,
      "allocatedVolume": 216000,
      "unallocatedVolume": 3242880,
      "lastUpdateDateTime": "2026-02-09T00:28:29+01:00",
      "occurenceCount": 14,
      "indicator": null,
      "periodType": null,
      "isUnlimited": null,
      "flowStatus": null,
      "interruptionType": null,
      "restorationInformation": null,
      "capacityType": null,
      "capacityBookingStatus": null,
      "value": null,
      "pointType": "Cross-Border Transmission IP within EU",
      "idPointType": 0,
      "id": "22099-12-31 00:00:00 +00:002099-12-31 00:00:00 +00:002025-10-01 04:00:00 +00:002026-10-01 04:00:00 +00:00FR-TSO-0003ITP-00526ExitkWh/d",
      "dataSet": 2,
      "periodFrom": null,
      "periodTo": null,
      "isCamRelevant": true,
      "isNA": null,
      "originalPeriodFrom": null,
      "isCmpRelevant": null,
      "bookingPlatformKey": null,
      "bookingPlatformLabel": null,
      "bookingPlatformURL": null,
      "interruptionCalculationRemark": null,
      "isArchived": false
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsog/cmp_unsuccessful_requests/year=YYYY/month=MM/cmp_unsuccessful_requests_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsog.generic.GenericEntsogJsonTransformer (subclass CmpUnsuccessfulRequestsTransformer)`
**Pydantic schema**: Generic — no Pydantic schema declared
**Dedup key**: `id`, within each gas day's file (`keep="last"`, `silver/entsog/generic.py` `transform`). Every record sends an `id`, so `(timestamp_utc, id)` is unique across files.
**Point-in-time field**: none. `timestamp_utc` is gridflow's gas-day stamp: the record's own start if it falls inside the gas day, else the gas-day start, 06:00 Europe/Brussels (`silver/entsog/datetime.py` `gas_day_stamp`). On 1 to 5 August 2026 no record starts inside a gas day, so every row reads 04:00 UTC. `last_update_date_time` is the vendor's own stamp.
**Day filter**: silver day D keeps every record whose capacity period overlaps gas day D, plus the statement rows dated D (`partition_validity_records_to_gas_day`).

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| timestamp_utc | datetime[UTC] | No | derived | gridflow's gas-day stamp; see Point-in-time field |
| auction_from | datetime[UTC] | Yes | auctionFrom | Null where the vendor sends `N/A` |
| auction_to | datetime[UTC] | Yes | auctionTo |  |
| capacity_from | datetime[UTC] | Yes | capacityFrom |  |
| capacity_to | datetime[UTC] | Yes | capacityTo |  |
| operator_key | str | Yes | operatorKey |  |
| tso_eic_code | str | Yes | tsoEicCode |  |
| operator_label | str | Yes | operatorLabel |  |
| point_key | str | Yes | pointKey |  |
| point_label | str | Yes | pointLabel |  |
| tso_item_identifier | str | Yes | tsoItemIdentifier |  |
| direction_key | str | Yes | directionKey |  |
| unit | str | Yes | unit |  |
| item_remarks | str | Yes | itemRemarks |  |
| general_remarks | str | Yes | generalRemarks |  |
| requested_volume | float | Yes | requestedVolume |  |
| allocated_volume | float | Yes | allocatedVolume |  |
| unallocated_volume | float | Yes | unallocatedVolume |  |
| last_update_date_time | datetime[UTC] | Yes | lastUpdateDateTime |  |
| occurence_count | float | Yes | occurenceCount |  |
| indicator | str | Yes | indicator |  |
| period_type | str | Yes | periodType |  |
| is_unlimited | str | Yes | isUnlimited | Kept as text |
| flow_status | str | Yes | flowStatus |  |
| interruption_type | str | Yes | interruptionType |  |
| restoration_information | str | Yes | restorationInformation |  |
| capacity_type | str | Yes | capacityType |  |
| capacity_booking_status | str | Yes | capacityBookingStatus |  |
| value | float | Yes | value |  |
| point_type | str | Yes | pointType |  |
| id_point_type | int | Yes | idPointType |  |
| id | str | Yes | id | Vendor record id; the dedup key within a gas day |
| data_set | int | Yes | dataSet | Statement rows send lowercase `dataset`, folded in here (`_COLUMN_ALIASES`); `2` on every row of 1 to 5 August 2026 |
| period_from | datetime[UTC] | Yes | periodFrom |  |
| period_to | datetime[UTC] | Yes | periodTo |  |
| is_cam_relevant | bool | Yes | isCamRelevant |  |
| is_na | str | Yes | isNA |  |
| original_period_from | datetime[UTC] | Yes | originalPeriodFrom |  |
| is_cmp_relevant | str | Yes | isCmpRelevant | Kept as text |
| booking_platform_key | null | Yes | bookingPlatformKey | Null on every row of 1 to 5 August 2026 |
| booking_platform_label | null | Yes | bookingPlatformLabel | Null on every row of 1 to 5 August 2026 |
| booking_platform_url | null | Yes | bookingPlatformURL | Null on every row of 1 to 5 August 2026 |
| interruption_calculation_remark | null | Yes | interruptionCalculationRemark | Null on every row of 1 to 5 August 2026 |
| is_archived | bool | Yes | isArchived |  |
| data_provider | str | No | derived | Always `entsog` |
| ingested_at | datetime[UTC] | No | derived | Wall-clock at silver write |
| event_time, available_at, source_run_id, dataset_version | | No | derived | Pipeline lineage columns (`silver/base.py`) |

### Silver sample

One real silver row, gas day 3 August 2026 (the same NaTran record the bronze sample shows), in silver's column order with UTC stamps:

```python
[
    {
        "timestamp_utc": "2026-08-03T04:00:00+00:00",
        "period_from": null,
        "period_to": null,
        "indicator": null,
        "period_type": null,
        "operator_key": "FR-TSO-0003",
        "operator_label": "NaTran",
        "tso_eic_code": "21X-FR-A-A0A0A-S",
        "point_key": "ITP-00526",
        "point_label": "VIRTUALYS",
        "direction_key": "Exit",
        "unit": "kWh/d",
        "value": null,
        "id": "22099-12-31 00:00:00 +00:002099-12-31 00:00:00 +00:002025-10-01 04:00:00 +00:002026-10-01 04:00:00 +00:00FR-TSO-0003ITP-00526ExitkWh/d",
        "auction_from": null,
        "auction_to": null,
        "capacity_from": "2025-10-01T04:00:00+00:00",
        "capacity_to": "2026-10-01T04:00:00+00:00",
        "tso_item_identifier": "21Z0000000004847",
        "item_remarks": null,
        "general_remarks": null,
        "requested_volume": 3458880.0,
        "allocated_volume": 216000.0,
        "unallocated_volume": 3242880.0,
        "last_update_date_time": "2026-02-08T23:28:29+00:00",
        "occurence_count": 14.0,
        "is_unlimited": null,
        "flow_status": null,
        "interruption_type": null,
        "restoration_information": null,
        "capacity_type": null,
        "capacity_booking_status": null,
        "point_type": "Cross-Border Transmission IP within EU",
        "id_point_type": 0,
        "is_cam_relevant": true,
        "is_na": null,
        "original_period_from": null,
        "is_cmp_relevant": null,
        "booking_platform_key": null,
        "booking_platform_label": null,
        "booking_platform_url": null,
        "interruption_calculation_remark": null,
        "is_archived": false,
        "data_set": 2,
        "data_provider": "entsog",
        "ingested_at": "2026-10-24T13:56:04+00:00",
        "event_time": "2026-08-03T04:00:00+00:00",
        "available_at": "2026-08-16T14:21:06+00:00",
        "source_run_id": "adhoc-2026-10-24T13:56:04.297408+00:00",
        "dataset_version": "1.0.0"
    }
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **Records in force, repeated daily**: CMP family endpoints accept `from` / `to`. In the responses for 1 to 5 August 2026, every record's capacity period covers the requested day (yearly, quarterly and monthly products) and the same 43 records come back each day. Silver keeps each record in every gas day's file it overlaps, so an `id` repeats once per fetched day. Don't dedup on period alone.
- **Volumes and units**: on 1 to 5 August 2026 the 43 records use `kWh/d` (41) and `kWh/h` (2, Fluxys Belgium at VIRTUALYS), and `requestedVolume` equals `allocatedVolume` plus `unallocatedVolume` on every one (gridflow's check, not an ENTSOG rule). Silver converts nothing; never sum across units.
- **`N/A` auction dates**: 14 of the 43 records send `auctionFrom` / `auctionTo` as `N/A` (null in silver); their `id` carries `2099-12-31 00:00:00` in those places.
- **Statement rows**: on 1 to 5 August 2026, 1,039 of the 1,082 records a day are ENTSOG statement rows: `id` starts with `5` and ends with another operator's key, volumes and `unit` are empty, `capacityFrom` = `capacityTo` = 00:00+02:00 on the requested day, as sent, and the field is spelt `dataset`, not `dataSet` (folded into `data_set`). They do not mark the points without records: on 3 August 2026, 11 of the 16 operator, point and direction triples with records also carry one (direction compared case-insensitively), and 226 of the 1,225 triples in `operator_point_directions` have no row of either kind.
- **`isCAMRelevant` (uppercase CAM)**: in the 1 to 5 August 2026 responses only `cmpAuctions` results send the uppercase variant; this endpoint sends `isCamRelevant`. Generic silver coalesces them into `is_cam_relevant`.
- **`directionKey` capitalised**: `Entry` / `Exit`, not `entry` / `exit`, in `/cmpUnsuccessfulRequests` records; its statement rows send lowercase. Compare case-insensitively.
- **HTTP 404 = empty**: same vendor empty convention applies.

- **Indicator string is exact-case**: the connector sends the exact human-readable form (`Physical Flow`, `Nomination`, `Available through UIOLI long-term`). Sending lowercase or hyphen variants returns 404.
- **`timeZone=UCT` (note typo)**: ENTSOG documents the parameter as `timeZone=UCT` rather than `UTC`. The connector spells it the vendor's way. The response `meta.timezone` echoes back `CET` regardless of the request value.
- **`pointDirection` filter**: built as `operatorKey + pointKey + directionKey` concatenated with no separator (e.g. `UK-TSO-0001ITP-00005exit`). Multi-value lists are comma-joined.
- **Missing data returns HTTP 404**: ENTSOG returns `HTTP 404` with body `{"message":"No result found"}` when an indicator/window/point combination has no rows. This is the vendor's empty convention, not a true failure. The connector's retry policy must let 404 surface.
- **Field-case duplicates**: live records may carry both `isCamRelevant` and `isCAMRelevant` shape (or `isCmpRelevant`/`isCMPRelevant`) depending on indicator. The generic silver transformer `_normalise_column_names` collapses these via `pl.coalesce` into one snake_case column.
- **Datetime placeholders**: `lastUpdateDateTime` and `originalPeriodFrom` may be empty strings, `"-"`, `"N/A"`, or human-formatted strings (`"Jan 15 2024 06:00AM"`). `parse_entsog_datetime` returns `None` for unparseable values rather than raising.
- **`directionKey` casing varies**: lowercase (`entry`/`exit`) in `/operationalData`; capitalised (`Exit`) in `/cmpUnsuccessfulRequests`. Don't compare with `==` across families.
- **Period offset is +02:00 (CET)**: even with `timeZone=UCT`, `periodFrom` carries `+02:00` (CEST in summer / `+01:00` in winter). The silver transformer's `parse_entsog_datetime` converts to UTC.


---

## Implementation delta

- **Vendor empty convention**: HTTP 404 + `{"message":"No result found"}` for empty windows.
- **Generic silver transformer**: produces dynamic snake_case columns from the camelCase API fields. The CMP family carries `auctionFrom`/`auctionTo`/`capacityFrom`/`capacityTo` placeholders such as `"N/A"` — silver `parse_entsog_datetime` returns `None` for these.

---

## Modelling notes

TODO

---

## Links

- [Official API docs (PDF)](https://transparency.entsog.eu/api/archiveDirectories/8/api-manual/TP_REG715_Documentation_TP_API%20-%20v2.1.pdf)
- `src/gridflow/connectors/entsog/endpoints.py`
- `src/gridflow/silver/entsog/generic.py`
- `src/gridflow/schemas/entsog.py`
- Gold view/builder
