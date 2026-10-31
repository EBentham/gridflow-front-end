---
source: entsog
dataset_key: available_through_uioli_long_term
vendor: ENTSOG Transparency Platform
last_verified: 2026-10-24
layer_coverage: bronze, silver
---

# ENTSOG — Available Through Uioli Long Term (`indicator=Available through UIOLI long-term`)

## Overview

Capacity made available through long-term UIOLI (Use-It-Or-Lose-It). ENTSOG's `defaultSentence` on the records it sends without a value reads "Currently no capacity has been made available on this point through the application of the congestion-management procedures". On 1 to 5 August 2026 each response also carried three annual valued records at Bacton (IUK) (see Known issues).

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
| Indicator | `Available through UIOLI long-term` (exact-case — vendor rejects lowercase or hyphen variants) |
| Time zone | `timeZone=UCT` (ENTSOG's spelling — note the typo; not `UTC`) |
| `pointDirection` filter | `operatorKey + pointKey + directionKey` concatenated, no separator (e.g. `UK-TSO-0001ITP-00005exit`) |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `indicator` | str | Yes | Exact-case indicator name | `Available through UIOLI long-term` |
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
  "https://transparency.entsog.eu/api/v1/operationalData?from=2026-05-06&to=2026-05-06&timeZone=UCT&indicator=Available%20through%20UIOLI%20long-term&periodType=day&pointDirection=UK-TSO-0001ITP-00005exit&forceDownload=true&limit=1000"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsog/available_through_uioli_long_term/<year>/<month>/<day>/raw_<uuid>.json`
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
        "Available through UIOLI long-term"
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
      "id": "1Available through UIOLI long-termkWh/ddayUK-TSO-0001ITP-00005exitkWh/d2025-10-012026-10-01",
      "dataSet": 1,
      "indicator": "Available through UIOLI long-term",
      "periodType": "day",
      "periodFrom": "2025-10-01T06:00:00+02:00",
      "periodTo": "2026-10-01T06:00:00+02:00",
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
      "value": 472,
      "lastUpdateDateTime": "2026-05-08T20:04:37+02:00",
      "isUnlimited": "",
      "flowStatus": "",
      "interruptionType": "",
      "restorationInformation": "",
      "capacityType": "",
      "capacityBookingStatus": "",
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
      "isArchived": false
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsog/available_through_uioli_long_term/year=YYYY/month=MM/available_through_uioli_long_term_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsog.GenericEntsogJsonTransformer (subclass AvailableThroughUioliLongTermTransformer)`
**Pydantic schema**: `Generic — no Pydantic schema declared`
**Dedup key**: the vendor `id`, `keep="last"`, within each gas day's bronze read (`silver/entsog/generic.py:235-241`). A partition is one gas day and every row is stamped inside it, so `(timestamp_utc, id)` is unique. A default-sentence `id` joins the dataset code, keys, an adjacent operator and the indicator, with no date; `(timestamp_utc, operator_key, point_key, direction_key)` repeats (see Known issues).
**Bronze read filter**: a record is kept when its `periodFrom`/`periodTo` window overlaps the bronze day's gas day, when its `periodFrom` falls on that date, or when it has no date (`generic.py:174-187`, `:353-369`; `datetime.py:110-153`); see Known issues.
**Point-in-time field**: none used by the pipeline. `last_update_date_time` is the vendor's `lastUpdateDateTime`, converted to UTC (`generic.py:212-214`); `ingested_at` is the silver transform time (`generic.py:243-249`).

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| timestamp_utc | datetime[UTC] | Yes | derived | Gas-day stamp (`generic.py:179-187`, `:216-220`; `datetime.py:156-180`): the record's `periodFrom` if it falls inside the gas day (06:00 to 06:00 Europe/Brussels), else the gas-day start; 04:00 UTC on every 2026-08 row |
| period_from | datetime[UTC] | Yes | periodFrom | The record's own validity start; 22:00 UTC the previous day on default-sentence rows (00:00+02:00) |
| period_to | datetime[UTC] | Yes | periodTo |  |
| indicator | str | Yes | indicator |  |
| period_type | str | Yes | periodType |  |
| operator_key | str | Yes | operatorKey |  |
| operator_label | str | Yes | operatorLabel |  |
| tso_eic_code | str | Yes | tsoEicCode |  |
| point_key | str | Yes | pointKey |  |
| point_label | str | Yes | pointLabel |  |
| direction_key | str | Yes | directionKey |  |
| unit | str | Yes | unit | As sent, not converted; `kWh/d` on valued rows, `""` on default-sentence rows |
| value | float | Yes | value | In the row's `unit`, not converted; sent as `""` it is null (Float64 cast with `strict=False`, `generic.py:231-233`) |
| id | str | Yes | id | Dedup key (see above) |
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
| is_na | str | Yes | isNA |  |
| original_period_from | datetime[UTC] | Yes | originalPeriodFrom |  |
| is_cmp_relevant | str | Yes | isCmpRelevant |  |
| booking_platform_key | null | Yes | bookingPlatformKey | Null dtype: null on every 2026-08 row |
| booking_platform_label | null | Yes | bookingPlatformLabel | Null dtype: null on every 2026-08 row |
| booking_platform_url | null | Yes | bookingPlatformURL | Null dtype: null on every 2026-08 row |
| interruption_calculation_remark | null | Yes | interruptionCalculationRemark | Null dtype: null on every 2026-08 row |
| point_type | str | Yes | pointType |  |
| id_point_type | Int64 | Yes | idPointType |  |
| is_archived | bool | Yes | isArchived |  |
| is_default_sentence | bool | Yes | isDefaultSentence |  |
| default_sentence | str | Yes | defaultSentence |  |
| data_set | str | Yes | dataSet / dataset | `1` on valued rows (`dataSet`), `5` on default-sentence rows (`dataset`), folded into one column (`generic.py:70`, `:429`) |
| data_provider | str | No | derived | Always `entsog` |
| ingested_at | datetime[UTC] | No | derived | Silver transform time (`generic.py:243-249`) |

### Silver sample

```python
[
    {
        "timestamp_utc": "2026-08-05T04:00:00+00:00",
        "period_from": "2025-10-01T04:00:00+00:00",
        "period_to": "2026-10-01T04:00:00+00:00",
        "indicator": "Available through UIOLI long-term",
        "period_type": "day",
        "operator_key": "UK-TSO-0001",
        "operator_label": "National Gas TSO",
        "tso_eic_code": "21X-GB-A-A0A0A-7",
        "point_key": "ITP-00005",
        "point_label": "Bacton (IUK)",
        "direction_key": "exit",
        "unit": "kWh/d",
        "value": 472.0,
        "id": "1Available through UIOLI long-termkWh/ddayUK-TSO-0001ITP-00005exitkWh/d2025-10-012026-10-01",
        "tso_item_identifier": "21Z000000000083P",
        "item_remarks": "",
        "general_remarks": "",
        "last_update_date_time": "2026-08-16T13:56:56+00:00",
        "is_unlimited": "",
        "flow_status": "",
        "interruption_type": "",
        "restoration_information": "",
        "capacity_type": "",
        "capacity_booking_status": "",
        "is_cam_relevant": false,
        "is_na": null,
        "original_period_from": null,
        "is_cmp_relevant": null,
        "booking_platform_key": null,
        "booking_platform_label": null,
        "booking_platform_url": null,
        "interruption_calculation_remark": null,
        "point_type": "Cross-Border Transmission IP between EU and ExtEU",
        "id_point_type": 23,
        "is_archived": false,
        "is_default_sentence": null,
        "default_sentence": null,
        "data_set": "1",
        "data_provider": "entsog",
        "ingested_at": "2026-10-24T13:56:02.458096+00:00"
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
- **Validity records, one row per gas day**: capacity records are validity periods (in this indicator's 2026-08 bronze, annual records from 2025-10-01 to 2026-10-01, and zero-length default-sentence records). The generic transformer keeps every record whose `periodFrom`/`periodTo` window overlaps the bronze day's gas day (06:00 to 06:00 Europe/Brussels), plus any dated that day or undated, for the capacity and CMP datasets in `_VALIDITY_WINDOW_DATASETS` (`silver/entsog/generic.py:174-187`, :353-369; `datetime.py:110-153`; gridflow PR #129, branch `fix/entsog-capacity-cmp`). It stamps each kept record with that gas day (`datetime.py:156-180`): `timestamp_utc` is the record's own start if inside the gas day, else the gas-day start. A record valid over many days therefore appears once per fetched gas day; do not sum rows across days. 2026-08: 70 bronze records (15 with a value), 70 silver rows.
- **Default-sentence records**: the records sent without a value carry `isDefaultSentence` true and the `defaultSentence` quoted in the overview (ENTSOG sends two spellings, "the congestion-management procedures" and "congestion management procedures"), with `dataset` "5" (a lowercase key, folded into `data_set`, `generic.py:70`, `:429`), `periodType` "", `unit` "", `value` "", and `periodFrom` = `periodTo` = 00:00+02:00. `period_from` is therefore 22:00 UTC on the previous day; the record is kept because that is the bronze day's local date, and stamped at the gas-day start, 04:00 UTC (`datetime.py:149-150`, `:156-180`).
- **Repeated 4-tuple**: National Gas TSO `ITP-00090` entry sends three default-sentence records a day, whose `id` names the adjacent operators `IE-TSO-0001`, `IE-TSO-0002` and `UK-TSO-0002`, and at Bacton (IUK) a valued record and a default-sentence record arrive for the same operator, point and direction. Dedup on `id` keeps all of them, so `(timestamp_utc, operator_key, point_key, direction_key)` is not unique.
- **Valued records, and a contradiction as sent**: each 2026-08 response also carries three annual records (`periodFrom` 2025-10-01 to 2026-10-01): National Gas TSO Bacton (IUK) exit 472 kWh/d, Interconnector Bacton (IUK) entry and exit 0. Silver keeps them, stamped at the gas-day start. The same point and day also carry a "no capacity made available" sentence, and the same 472 record (same `lastUpdateDateTime`) appears under oversubscription, surrender and UIOLI long-term. Unexplained.
- **Requested versus returned (2026-08 bronze)**: `meta.count` equals `meta.total` (14) in every response.



---

## Implementation delta

- **Validity records**: capacity datasets keep every record in force on the fetched gas day, one row per gas day (`_VALIDITY_WINDOW_DATASETS`, `silver/entsog/generic.py:353-369`; see Known issues). The indicator name matches the code's exact-case constant in `OPERATIONAL_INDICATORS` (`connectors/entsog/endpoints.py:95-115`).
- **Synthetic fixture**: `tests/fixtures/entsog/physical_flows_response.json` carries placeholder `pointKey: "IUK"` and `operatorKey: "OP-IUK"`. Live data uses real keys (`ITP-00005`, `UK-TSO-0001`). Fixture regeneration is deferred (silver tests depend on the placeholder shape).

---

## Modelling notes

- Used as raw input to gas balance / interconnector flow features in `gridflow_models/`.
- Target candidates: directional flow magnitude (entry vs exit per point).
- `flow_status` is an empty string on every 2026-08/09 row, so the `Confirmed`/`Provisional` filter used for flows does not apply. Drop the default-sentence rows (`is_default_sentence` true): they carry no value.
- Join with `operator_point_directions` to attach country, balancing zone, and CAM-relevant flags.

---

## Links

- [Official API docs (PDF)](https://transparency.entsog.eu/api/archiveDirectories/8/api-manual/TP_REG715_Documentation_TP_API%20-%20v2.1.pdf)
- `src/gridflow/connectors/entsog/endpoints.py`
- `src/gridflow/silver/entsog/generic.py`
- `src/gridflow/schemas/entsog.py`
- Gold view/builder
- [Domain: gas day](../../../20-domain/concepts/gas-day.md)
