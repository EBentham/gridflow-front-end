---
source: entsog
dataset_key: cmp_unavailable_firm_capacity
vendor: ENTSOG Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
---

# ENTSOG — Cmp Unavailable Firm Capacity

## Overview

CMP unavailable firm capacity: per operator, point and direction, a validity period (`periodFrom` to `periodTo`) and an allocation process, with `value` and `unit` null on every record of 1 to 5 August 2026, so the data is the period and the remarks, not a quantity. ENTSOG also sends statement rows, one per operator, point, direction and neighbouring operator, usually "Currently firm products with a duration of one month or longer are offered on this point in the regular allocation process." On 3 August 2026 some points carry both a record and a statement row, and some points in the `operator_point_directions` register carry neither. gridflow reads a record as the opposite of that sentence; no ENTSOG definition is quoted here.

→ Related concepts:
  [Gas day](../../../20-domain/concepts/gas-day.md)

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://transparency.entsog.eu/api/v1` |
| Path             | `/cmpUnavailables` |
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
  "https://transparency.entsog.eu/api/v1/cmpUnavailables?from=2026-05-06&to=2026-05-06&timeZone=UCT&periodType=day&forceDownload=true&limit=1000"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsog/cmp_unavailable_firm_capacity/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable.
**Granularity**: One file per fetch call (per calendar day window).

### Bronze sample

```json
{
  "meta": {
    "limit": 1000,
    "offset": 0,
    "count": 1,
    "total": 269,
    "query": {
      "from": "2026-05-06",
      "to": "2026-05-06",
      "timeZone": "UCT",
      "periodType": "day"
    },
    "timezone": "CET"
  },
  "cmpUnavailables": [
    {
      "periodFrom": "2015-10-01T00:00:00+02:00",
      "periodTo": "2026-09-30T00:00:00+02:00",
      "operatorKey": "FR-TSO-0003",
      "tsoEicCode": "21X-FR-A-A0A0A-S",
      "operatorLabel": "GRTgaz",
      "pointKey": "ITP-00039",
      "pointLabel": "Oltingue (FR) / Rodersdorf (CH)",
      "tsoItemIdentifier": "21Z000000000037W",
      "directionKey": "exit",
      "allocationProcess": "Auction",
      "auctionStartDate": "N/A",
      "itemRemarks": "N/A",
      "generalRemarks": null,
      "lastUpdateDateTime": "2020-11-27T18:01:55+01:00",
      "pointType": "Cross-Border Transmission IP between EU and Non-EU",
      "idPointType": 14,
      "id": "42015-09-30 22:00:00 +00:002026-09-29 22:00:00 +00:0021X-FR-A-A0A0A-SFR-TSO-0003ITP-00039exitAuction",
      "dataSet": 4,
      "indicator": null,
      "periodType": null,
      "unit": null,
      "value": null,
      "isUnlimited": null,
      "flowStatus": "",
      "interruptionType": null,
      "restorationInformation": null,
      "capacityType": null,
      "capacityBookingStatus": null,
      "isCamRelevant": null,
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

**Path pattern**: `{data_root}/silver/entsog/cmp_unavailable_firm_capacity/year=YYYY/month=MM/cmp_unavailable_firm_capacity_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsog.generic.GenericEntsogJsonTransformer (subclass CmpUnavailableFirmCapacityTransformer)`
**Pydantic schema**: Generic — no Pydantic schema declared
**Dedup key**: `id`, within each gas day's file (`keep="last"`, `silver/entsog/generic.py` `transform`). Every record sends an `id`, so `(timestamp_utc, id)` is unique across files.
**Point-in-time field**: none. `timestamp_utc` is gridflow's gas-day stamp: the record's own start if it falls inside the gas day, else the gas-day start, 06:00 Europe/Brussels (`silver/entsog/datetime.py` `gas_day_stamp`). On 1 to 5 August 2026 no record starts inside a gas day, so every row reads 04:00 UTC. `last_update_date_time` is the vendor's own stamp.
**Day filter**: silver day D keeps every record whose validity period overlaps gas day D, plus the statement rows dated D (`partition_validity_records_to_gas_day`).

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| timestamp_utc | datetime[UTC] | No | derived | gridflow's gas-day stamp; see Point-in-time field |
| period_from | datetime[UTC] | Yes | periodFrom |  |
| period_to | datetime[UTC] | Yes | periodTo |  |
| operator_key | str | Yes | operatorKey |  |
| tso_eic_code | str | Yes | tsoEicCode |  |
| operator_label | str | Yes | operatorLabel |  |
| point_key | str | Yes | pointKey |  |
| point_label | str | Yes | pointLabel |  |
| tso_item_identifier | str | Yes | tsoItemIdentifier |  |
| direction_key | str | Yes | directionKey |  |
| allocation_process | str | Yes | allocationProcess |  |
| auction_start_date | str | Yes | auctionStartDate | Kept as text: `N/A` or a stamp with its offset, as sent |
| item_remarks | str | Yes | itemRemarks |  |
| general_remarks | str | Yes | generalRemarks |  |
| last_update_date_time | datetime[UTC] | Yes | lastUpdateDateTime |  |
| point_type | str | Yes | pointType |  |
| id_point_type | int | Yes | idPointType |  |
| id | str | Yes | id | Vendor record id; the dedup key within a gas day |
| data_set | int | Yes | dataSet | Statement rows send lowercase `dataset`, folded in here (`_COLUMN_ALIASES`); `4` on every row of 1 to 5 August 2026 |
| indicator | str | Yes | indicator |  |
| period_type | str | Yes | periodType |  |
| unit | str | Yes | unit | Null on records, empty on statement rows (1 to 5 August 2026) |
| value | float | Yes | value | Null on every row of 1 to 5 August 2026 |
| is_unlimited | str | Yes | isUnlimited | Kept as text |
| flow_status | str | Yes | flowStatus |  |
| interruption_type | str | Yes | interruptionType |  |
| restoration_information | str | Yes | restorationInformation |  |
| capacity_type | str | Yes | capacityType |  |
| capacity_booking_status | str | Yes | capacityBookingStatus |  |
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

One real silver row, gas day 3 August 2026 (the same GRTgaz record the bronze sample shows), in silver's column order with UTC stamps:

```python
[
    {
        "timestamp_utc": "2026-08-03T04:00:00+00:00",
        "period_from": "2015-09-30T22:00:00+00:00",
        "period_to": "2026-09-29T22:00:00+00:00",
        "indicator": null,
        "period_type": null,
        "operator_key": "FR-TSO-0003",
        "operator_label": "GRTgaz",
        "tso_eic_code": "21X-FR-A-A0A0A-S",
        "point_key": "ITP-00039",
        "point_label": "Oltingue (FR) / Rodersdorf (CH)",
        "direction_key": "exit",
        "unit": null,
        "value": null,
        "id": "42015-09-30 22:00:00 +00:002026-09-29 22:00:00 +00:0021X-FR-A-A0A0A-SFR-TSO-0003ITP-00039exitAuction",
        "tso_item_identifier": "21Z000000000037W",
        "allocation_process": "Auction",
        "auction_start_date": "N/A",
        "item_remarks": "N/A",
        "general_remarks": null,
        "last_update_date_time": "2020-11-27T17:01:55+00:00",
        "point_type": "Cross-Border Transmission IP between EU and Non-EU",
        "id_point_type": 14,
        "is_unlimited": null,
        "flow_status": "",
        "interruption_type": null,
        "restoration_information": null,
        "capacity_type": null,
        "capacity_booking_status": null,
        "is_cam_relevant": null,
        "is_na": null,
        "original_period_from": null,
        "is_cmp_relevant": null,
        "booking_platform_key": null,
        "booking_platform_label": null,
        "booking_platform_url": null,
        "interruption_calculation_remark": null,
        "is_archived": false,
        "data_set": 4,
        "data_provider": "entsog",
        "ingested_at": "2026-10-24T13:56:03+00:00",
        "event_time": "2026-08-03T04:00:00+00:00",
        "available_at": "2026-08-16T14:21:11+00:00",
        "source_run_id": "adhoc-2026-10-24T13:56:03.432445+00:00",
        "dataset_version": "1.0.0"
    }
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **Records in force, repeated daily**: CMP family endpoints accept `from` / `to`. In the responses for 1 to 5 August 2026, every record's validity period covers the requested day and the same 291 records come back each day; periods start between 2015 and 2026 and end between 2026 and 2039. Silver keeps each record in every gas day's file it overlaps, so an `id` repeats once per fetched day. Don't dedup on period alone.
- **No quantity**: on 1 to 5 August 2026 all 291 records send `value` and `unit` null and `allocationProcess` `Auction`; `auctionStartDate` is `N/A` on 132 and a stamp on 159.
- **Statement rows**: on 1 to 5 August 2026, 579 of the 870 records a day are ENTSOG statement rows: `id` starts with `5` and ends with another operator's key, `unit` is empty, `periodFrom` = `periodTo` = 00:00+02:00 on the requested day, as sent, and the field is spelt `dataset`, not `dataSet` (folded into `data_set`). They do not mark the points without records: on 3 August 2026, 27 of the 112 operator, point and direction triples with records also carry one, and 589 of the 1,225 triples in `operator_point_directions` have no row of either kind. Some carry other remarks, such as "No congestion on this point over the selected period".
- **`isCAMRelevant` (uppercase CAM)**: in the 1 to 5 August 2026 responses only `cmpAuctions` results send the uppercase variant; this endpoint sends `isCamRelevant`. Generic silver coalesces them into `is_cam_relevant`.
- **`directionKey` capitalised**: `Exit` not `exit` in `/cmpUnsuccessfulRequests` records; its statement rows send lowercase. Compare case-insensitively.
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
