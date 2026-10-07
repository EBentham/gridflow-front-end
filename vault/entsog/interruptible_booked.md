---
source: entsog
dataset_key: interruptible_booked
vendor: ENTSOG Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
---

# ENTSOG — Interruptible Booked (`indicator=Interruptible Booked`)

## Overview

Interruptible capacity booked by shippers. Mostly sent as long-period records, which silver drops unless they start on the fetched gas day (see Known issues).

The dataset is one of 19 indicators served by the same `/operationalData`
endpoint. The (operator, point, direction) tuple selects which physical
location to read; the `indicator` query parameter selects which series
(physical flow, nomination, allocation, etc.) is returned. Records carry
a `periodFrom` / `periodTo` window (for capacity, the record's validity period, from one day to decades) and a `value` in `kWh/d` (or
indicator-specific units for content/quality series).

→ Related concepts:
  [Gas day](../../../20-domain/concepts/gas-day.md)
  [Nominations, renominations and allocations](nominations.md)

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
| Publication lag  | Not vendor-documented here. Records carry their own validity period (`periodFrom`/`periodTo`); `flowStatus` is an empty string on every 2026-08/09 record |
| Response format  | JSON |
| Indicator | `Interruptible Booked` (exact-case — vendor rejects lowercase or hyphen variants) |
| Time zone | `timeZone=UCT` (ENTSOG's spelling — note the typo; not `UTC`) |
| `pointDirection` filter | `operatorKey + pointKey + directionKey` concatenated, no separator (e.g. `UK-TSO-0001ITP-00005exit`) |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `indicator` | str | Yes | Exact-case indicator name | `Interruptible Booked` |
| `from` | date (YYYY-MM-DD) | Yes | Window start (gas day) | `2026-05-06` |
| `to` | date (YYYY-MM-DD) | Yes | Window end (inclusive) | `2026-05-06` |
| `timeZone` | str | Yes | `UCT` (vendor typo for UTC) | `UCT` |
| `periodType` | str | No | `day` (default) or `hour` | `day` |
| `pointDirection` | str / list[str] | No (recommended) | Concatenated `operatorKey + pointKey + directionKey`; comma-joined for multiple | `UK-TSO-0001ITP-00005exit` |
| `forceDownload` | bool | No | Bypass server-side cache | `true` |
| `limit` | int | No | `-1` returns all records | `-1` |

### Working curl example

```bash
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://transparency.entsog.eu/api/v1/operationalData?from=2026-05-06&to=2026-05-06&timeZone=UCT&indicator=Interruptible%20Booked&periodType=day&pointDirection=UK-TSO-0001ITP-00005exit&forceDownload=true&limit=1000"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsog/interruptible_booked/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per `fetch()` call (one calendar day per file by convention)

### Bronze sample

```json
{
  "meta": {
    "limit": 1000,
    "offset": 0,
    "count": 1,
    "total": 1,
    "query": {
      "indicator": [
        "Interruptible Booked"
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
      "id": "1Interruptible BookeddayUK-TSO-0001ITP-00005exitkWh/d2022-03-012026-05-10",
      "dataSet": 1,
      "indicator": "Interruptible Booked",
      "periodType": "day",
      "periodFrom": "2022-03-01T06:00:00+01:00",
      "periodTo": "2026-05-10T06:00:00+02:00",
      "operatorKey": "UK-TSO-0001",
      "tsoEicCode": "21X-GB-A-A0A0A-7",
      "operatorLabel": "National Gas TSO",
      "pointKey": "ITP-00005",
      "pointLabel": "Bacton (IUK)",
      "tsoItemIdentifier": "21Z000000000083P",
      "directionKey": "exit",
      "unit": "kWh/d",
      "itemRemarks": "",
      "generalRemarks": "",
      "value": 0,
      "lastUpdateDateTime": "2026-05-08T19:17:39+02:00",
      "isUnlimited": "0",
      "flowStatus": "",
      "interruptionType": "",
      "restorationInformation": "",
      "capacityType": "Interruptible",
      "capacityBookingStatus": null,
      "isCamRelevant": false,
      "isNA": null,
      "originalPeriodFrom": null,
      "isCmpRelevant": null,
      "bookingPlatformKey": null,
      "bookingPlatformLabel": null,
      "bookingPlatformURL": null,
      "interruptionCalculationRemark": null,
      "pointType": "Cross-Border Transmission IP between EU and ExtEU",
      "idPointType": 23,
      "isArchived": null
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsog/interruptible_booked/year=YYYY/month=MM/interruptible_booked_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsog.GenericEntsogJsonTransformer (subclass InterruptibleBookedTransformer)`
**Pydantic schema**: `Generic — no Pydantic schema declared`
**Dedup key**: the vendor `id`, `keep="last"`, within each day's bronze read (`silver/entsog/generic.py:193-199`). The `id` joins indicator, keys, unit and the record's period dates, so `(timestamp_utc, operator_key, point_key, direction_key)` is unique in 2026-08/09 silver.
**Bronze read filter**: a record is kept only when the local date of its `periodFrom` is the bronze day (`generic.py:157-161`, `:332`; `datetime.py:56-87`); see Known issues.
**Point-in-time field**: none used by the pipeline. `last_update_date_time` is the vendor's `lastUpdateDateTime`, converted to UTC (`generic.py:181-183`); `ingested_at` is the silver transform time (`generic.py:201-206`).

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| timestamp_utc | datetime[UTC] | Yes | derived | `period_from` copied (`generic.py:185-187`): the start of the record's validity period in UTC; 04:00 UTC on valued 2026-08/09 rows, 03:00 UTC on not-applicable placeholders |
| period_from | datetime[UTC] | Yes | periodFrom |  |
| period_to | datetime[UTC] | Yes | periodTo |  |
| indicator | str | Yes | indicator |  |
| period_type | str | Yes | periodType |  |
| operator_key | str | Yes | operatorKey |  |
| operator_label | str | Yes | operatorLabel |  |
| tso_eic_code | str | Yes | tsoEicCode |  |
| point_key | str | Yes | pointKey |  |
| point_label | str | Yes | pointLabel |  |
| direction_key | str | Yes | directionKey |  |
| unit | str | Yes | unit | As sent, not converted; `kWh/d` on every 2026-08/09 row |
| value | float | Yes | value | In the row's `unit`, not converted; sent as `""` it is null (Float64 cast with `strict=False`, `generic.py:189-191`) |
| id | str | Yes | id | Dedup key (see above) |
| data_set | Int64 | Yes | dataSet |  |
| tso_item_identifier | str | Yes | tsoItemIdentifier |  |
| item_remarks | str | Yes | itemRemarks |  |
| general_remarks | str | Yes | generalRemarks |  |
| last_update_date_time | datetime[UTC] | Yes | lastUpdateDateTime |  |
| is_unlimited | str | Yes | isUnlimited | Null dtype in partitions where the day's rows are all null (dtype drift) |
| flow_status | str | Yes | flowStatus |  |
| interruption_type | str | Yes | interruptionType | Null dtype in partitions where the day's rows are all null (dtype drift) |
| restoration_information | str | Yes | restorationInformation | Null dtype in partitions where the day's rows are all null (dtype drift) |
| capacity_type | str | Yes | capacityType | Null dtype in partitions where the day's rows are all null (dtype drift) |
| capacity_booking_status | str | Yes | capacityBookingStatus | Null dtype in partitions where the day's rows are all null (dtype drift) |
| is_cam_relevant | bool | Yes | isCamRelevant | Null dtype in partitions where the day's rows are all null (dtype drift) |
| is_na | Int64 | Yes | isNA |  |
| original_period_from | datetime[UTC] | Yes | originalPeriodFrom |  |
| is_cmp_relevant | str | Yes | isCmpRelevant |  |
| booking_platform_key | str | Yes | bookingPlatformKey |  |
| booking_platform_label | str | Yes | bookingPlatformLabel |  |
| booking_platform_url | str | Yes | bookingPlatformURL |  |
| interruption_calculation_remark | null | Yes | interruptionCalculationRemark | Null dtype: null on every 2026-08/09 row |
| point_type | str | Yes | pointType |  |
| id_point_type | Int64 | Yes | idPointType |  |
| is_archived | null | Yes | isArchived | Null dtype: null on every 2026-08/09 row |
| data_provider | str | No | derived | Always `entsog` |
| ingested_at | datetime[UTC] | No | derived | Silver transform time (`generic.py:201-206`) |

### Silver sample

```python
[
    {
        "timestamp_utc": "2026-09-16T04:00:00+00:00",
        "period_from": "2026-09-16T04:00:00+00:00",
        "period_to": "2026-09-27T04:00:00+00:00",
        "indicator": "Interruptible Booked",
        "period_type": "day",
        "operator_key": "IE-TSO-0002",
        "operator_label": "GNI",
        "tso_eic_code": "47X0000000000576",
        "point_key": "ITP-00495",
        "point_label": "Moffat (IE)",
        "direction_key": "exit",
        "unit": "kWh/d",
        "value": 160000.0,
        "id": "1Interruptible BookeddayIE-TSO-0002ITP-00495exitkWh/d2026-09-162026-09-27",
        "data_set": 1,
        "tso_item_identifier": "21Z000000000081T",
        "item_remarks": "",
        "general_remarks": "",
        "last_update_date_time": "2026-09-26T05:07:34+00:00",
        "is_unlimited": "0",
        "flow_status": "",
        "interruption_type": "",
        "restoration_information": "",
        "capacity_type": "Interruptible",
        "capacity_booking_status": null,
        "is_cam_relevant": true,
        "is_na": null,
        "original_period_from": null,
        "is_cmp_relevant": null,
        "booking_platform_key": null,
        "booking_platform_label": null,
        "booking_platform_url": null,
        "interruption_calculation_remark": null,
        "point_type": "Cross-Border Transmission IP between EU and ExtEU",
        "id_point_type": 23,
        "is_archived": null,
        "data_provider": "entsog",
        "ingested_at": "2026-09-26T17:44:55.438651+00:00"
    }
]
```

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
- **Silver drops records whose validity starts before the fetched gas day**: the generic transformer runs the gas-day filter `partition_records_to_target_date` on every dataset that requires dates (`silver/entsog/generic.py:157-161`; `date_window_dataset = endpoint.requires_dates`, `:332`; `datetime.py:56-87`), so a record is kept only when the local date of its `periodFrom` is the bronze day (`datetime.py:191-213`). Capacity records are validity periods (in 2026-08/09 bronze, from one day to 2015-2048), so most are dropped. `tariffs` and `tariff_simulations` are exempt for the same reason (`generic.py:297-306`); capacity indicators are not. 2026-08/09: 126 bronze records (112 with a value) became 20 silver rows (6 with a value).
- **Not-applicable placeholders**: GNI `ITP-00495` entry sends one record a day with `isNA` 1, `value` "" (null in silver), `periodFrom` 05:00+02:00 (03:00 UTC, an hour before valued rows), an `id` ending `_NA<n>` with a fixed 2026-2027 range that recurs every day, and the remark "Firm Only".
- **Requested versus returned (2026-08/09 bronze)**: all nine `pointDirection` filters return one record each; `meta.count` equals `meta.total` (9) in every response. Unlike nominations, BBL company's `ITP-00063` filters return values here.
- **Partition dtype drift**: a column whose rows are all null in one day's response is written with Null dtype in that partition and String in others (see the schema table). `pl.read_parquet` over the table glob fails; read per file and concatenate with `how="diagonal_relaxed"`.



---

## Implementation delta

- **Silver retention**: the generic gas-day filter drops capacity records whose validity starts before the fetched day (see Known issues). The indicator name matches the code's exact-case constant in `OPERATIONAL_INDICATORS` (`connectors/entsog/endpoints.py:95-115`).
- **Synthetic fixture**: `tests/fixtures/entsog/physical_flows_response.json` carries placeholder `pointKey: "IUK"` and `operatorKey: "OP-IUK"`. Live data uses real keys (`ITP-00005`, `UK-TSO-0001`). Fixture regeneration is deferred (silver tests depend on the placeholder shape).

---

## Modelling notes

- Used as raw input to gas balance / interconnector flow features in `gridflow_models/`.
- Target candidates: directional flow magnitude (entry vs exit per point).
- `flow_status` is an empty string on every 2026-08/09 row, so the `Confirmed`/`Provisional` filter used for flows does not apply. Drop `is_na == 1` placeholders, and treat a row's `value` as applying from `period_from` to `period_to`, not only on the gas day it is stamped with.
- Join with `operator_point_directions` to attach country, balancing zone, and CAM-relevant flags.

---

## Links

- [Official API docs (PDF)](https://transparency.entsog.eu/api/archiveDirectories/8/api-manual/TP_REG715_Documentation_TP_API%20-%20v2.1.pdf)
- `src/gridflow/connectors/entsog/endpoints.py`
- `src/gridflow/silver/entsog/generic.py`
- `src/gridflow/schemas/entsog.py`
- Gold view/builder
- [Domain: gas day](../../../20-domain/concepts/gas-day.md)
