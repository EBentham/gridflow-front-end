---
source: entsog
dataset_key: interruptible_total
vendor: ENTSOG Transparency Platform
last_verified: 2026-10-24
layer_coverage: bronze, silver
---

# ENTSOG — Interruptible Total (`indicator=Interruptible Total`)

## Overview

Total interruptible capacity offered by the operator. Not booked plus available at every point: in 2026-08/09 bronze, GNI's Moffat (IE) exit sends the same value here as Interruptible Booked (0 to 160,001), and BBL company's Julianadorp entry sends 0 while Interruptible Available is 494,400,000 (a project check).

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
| Indicator | `Interruptible Total` (exact-case — vendor rejects lowercase or hyphen variants) |
| Time zone | `timeZone=UCT` (ENTSOG's spelling — note the typo; not `UTC`) |
| `pointDirection` filter | `operatorKey + pointKey + directionKey` concatenated, no separator (e.g. `UK-TSO-0001ITP-00005exit`) |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `indicator` | str | Yes | Exact-case indicator name | `Interruptible Total` |
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
  "https://transparency.entsog.eu/api/v1/operationalData?from=2026-05-06&to=2026-05-06&timeZone=UCT&indicator=Interruptible%20Total&periodType=day&pointDirection=UK-TSO-0001ITP-00005exit&forceDownload=true&limit=1000"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsog/interruptible_total/<year>/<month>/<day>/raw_<uuid>.json`
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
        "Interruptible Total"
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
      "id": "1Interruptible TotaldayUK-TSO-0001ITP-00005exitkWh/d2022-04-042026-05-10",
      "dataSet": 1,
      "indicator": "Interruptible Total",
      "periodType": "day",
      "periodFrom": "2022-04-04T06:00:00+02:00",
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
      "lastUpdateDateTime": "2026-05-08T19:17:40+02:00",
      "isUnlimited": "0",
      "flowStatus": "",
      "interruptionType": "",
      "restorationInformation": "",
      "capacityType": "Interruptible",
      "capacityBookingStatus": "Total",
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

**Path pattern**: `{data_root}/silver/entsog/interruptible_total/year=YYYY/month=MM/interruptible_total_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsog.GenericEntsogJsonTransformer (subclass InterruptibleTotalTransformer)`
**Pydantic schema**: `Generic — no Pydantic schema declared`
**Dedup key**: the vendor `id`, `keep="last"`, within each gas day's bronze read (`silver/entsog/generic.py:235-241`). A partition is one gas day and every row is stamped inside it, so `(timestamp_utc, id)` is unique. The `id` joins indicator, keys, unit and the record's period dates; `(timestamp_utc, operator_key, point_key, direction_key)` is also unique in 2026-08/09 silver.
**Bronze read filter**: a record is kept when its `periodFrom`/`periodTo` window overlaps the bronze day's gas day, when its `periodFrom` falls on that date, or when it has no date (`generic.py:174-187`, `:353-369`; `datetime.py:110-153`); see Known issues.
**Point-in-time field**: none used by the pipeline. `last_update_date_time` is the vendor's `lastUpdateDateTime`, converted to UTC (`generic.py:212-214`); `ingested_at` is the silver transform time (`generic.py:243-249`).

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| timestamp_utc | datetime[UTC] | Yes | derived | Gas-day stamp (`generic.py:179-187`, `:216-220`; `datetime.py:156-180`): the record's `periodFrom` if it falls inside the gas day (06:00 to 06:00 Europe/Brussels), else the gas-day start; 04:00 UTC on every 2026-08/09 row |
| period_from | datetime[UTC] | Yes | periodFrom | The record's own validity start, converted to UTC; can be years before `timestamp_utc` |
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
| value | float | Yes | value | In the row's `unit`, not converted; sent as `""` it is null (Float64 cast with `strict=False`, `generic.py:231-233`) |
| id | str | Yes | id | Dedup key (see above) |
| data_set | Int64 | Yes | dataSet |  |
| tso_item_identifier | str | Yes | tsoItemIdentifier |  |
| item_remarks | str | Yes | itemRemarks |  |
| general_remarks | str | Yes | generalRemarks |  |
| last_update_date_time | datetime[UTC] | Yes | lastUpdateDateTime |  |
| is_unlimited | str | Yes | isUnlimited |  |
| flow_status | str | Yes | flowStatus |  |
| interruption_type | str | Yes | interruptionType |  |
| restoration_information | str | Yes | restorationInformation |  |
| capacity_type | str | Yes | capacityType |  |
| capacity_booking_status | str | Yes | capacityBookingStatus |  |
| is_cam_relevant | bool | Yes | isCamRelevant |  |
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
| ingested_at | datetime[UTC] | No | derived | Silver transform time (`generic.py:243-249`) |

### Silver sample

```python
[
    {
        "timestamp_utc": "2026-09-21T04:00:00+00:00",
        "period_from": "2026-08-27T04:00:00+00:00",
        "period_to": "2026-10-24T04:00:00+00:00",
        "indicator": "Interruptible Total",
        "period_type": "day",
        "operator_key": "UK-TSO-0003",
        "operator_label": "Interconnector",
        "tso_eic_code": "21X-GB-B-A0A0A-Z",
        "point_key": "ITP-00005",
        "point_label": "Bacton (IUK)",
        "direction_key": "entry",
        "unit": "kWh/d",
        "value": 221570160.0,
        "id": "1Interruptible TotaldayUK-TSO-0003ITP-00005entrykWh/d2026-08-272026-10-24",
        "data_set": 1,
        "tso_item_identifier": "21Z000000000084N",
        "item_remarks": "",
        "general_remarks": "",
        "last_update_date_time": "2026-08-25T05:02:47+00:00",
        "is_unlimited": "0",
        "flow_status": "",
        "interruption_type": null,
        "restoration_information": null,
        "capacity_type": "Interruptible",
        "capacity_booking_status": "",
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
        "ingested_at": "2026-10-24T13:56:01.253290+00:00"
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
- **Validity records, one row per gas day**: capacity records are validity periods (in 2026-08/09 bronze, from one day to 2015-2048). The generic transformer keeps every record whose `periodFrom`/`periodTo` window overlaps the bronze day's gas day (06:00 to 06:00 Europe/Brussels), plus any dated that day or undated, for the capacity and CMP datasets in `_VALIDITY_WINDOW_DATASETS` (`silver/entsog/generic.py:174-187`, :353-369; `datetime.py:110-153`; gridflow PR #129, branch `fix/entsog-capacity-cmp`). It stamps each kept record with that gas day (`datetime.py:156-180`): `timestamp_utc` is the record's own start if inside the gas day, else the gas-day start. A record valid over many days therefore appears once per fetched gas day; do not sum rows across days. 2026-08/09: 126 bronze records (112 with a value), 126 silver rows.
- **Not-applicable placeholders**: GNI `ITP-00495` entry sends one record a day with `isNA` 1, `value` "" (null in silver), `periodFrom` 05:00+02:00 (03:00 UTC, an hour before the gas day starts, so silver stamps them at the gas-day start, 04:00 UTC), an `id` ending `_NA<n>` with a fixed 2026-2027 range that recurs every day, and the remark "Firm Only".
- **Requested versus returned (2026-08/09 bronze)**: all nine `pointDirection` filters return one record each; `meta.count` equals `meta.total` (9) in every response except 15 September 2026, where `meta.total` is 10 while `meta.count` is 9 and nine records are returned (unexplained). Unlike nominations, BBL company's `ITP-00063` filters return values here.
- **Partition dtype drift**: a column whose rows are all null in one day's response is written with Null dtype in that partition and String in others (`generic.py` coerces no dtypes). No column drifts in 2026-08/09 silver, but a day whose rows are all null in a column would. `pl.read_parquet` over the table glob then fails; read per file and concatenate with `how="diagonal_relaxed"`.



---

## Implementation delta

- **Validity records**: capacity datasets keep every record in force on the fetched gas day, one row per gas day (`_VALIDITY_WINDOW_DATASETS`, `silver/entsog/generic.py:353-369`; see Known issues). The indicator name matches the code's exact-case constant in `OPERATIONAL_INDICATORS` (`connectors/entsog/endpoints.py:95-115`).
- **Synthetic fixture**: `tests/fixtures/entsog/physical_flows_response.json` carries placeholder `pointKey: "IUK"` and `operatorKey: "OP-IUK"`. Live data uses real keys (`ITP-00005`, `UK-TSO-0001`). Fixture regeneration is deferred (silver tests depend on the placeholder shape).

---

## Modelling notes

- Used as raw input to gas balance / interconnector flow features in `gridflow_models/`.
- Target candidates: directional flow magnitude (entry vs exit per point).
- `flow_status` is an empty string on every 2026-08/09 row, so the `Confirmed`/`Provisional` filter used for flows does not apply. Drop `is_na == 1` placeholders. A row stands for its gas day; the record behind it runs from `period_from` to `period_to` and repeats on every gas day it covers, so never sum rows across days.
- Join with `operator_point_directions` to attach country, balancing zone, and CAM-relevant flags.

---

## Links

- [Official API docs (PDF)](https://transparency.entsog.eu/api/archiveDirectories/8/api-manual/TP_REG715_Documentation_TP_API%20-%20v2.1.pdf)
- `src/gridflow/connectors/entsog/endpoints.py`
- `src/gridflow/silver/entsog/generic.py`
- `src/gridflow/schemas/entsog.py`
- Gold view/builder
- [Domain: gas day](../../../20-domain/concepts/gas-day.md)
