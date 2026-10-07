---
source: entsog
dataset_key: available_through_uioli_short_term
vendor: ENTSOG Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
---

# ENTSOG — Available Through Uioli Short Term (`indicator=Available through UIOLI short-term`)

## Overview

Capacity made available through short-term UIOLI. ENTSOG's `defaultSentence` on the records it sends without a value reads "Currently no capacity has been made available on this point through the application of the congestion-management procedures"; those are the only records silver keeps (see Known issues).

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
| Indicator | `Available through UIOLI short-term` (exact-case — vendor rejects lowercase or hyphen variants) |
| Time zone | `timeZone=UCT` (ENTSOG's spelling — note the typo; not `UTC`) |
| `pointDirection` filter | `operatorKey + pointKey + directionKey` concatenated, no separator (e.g. `UK-TSO-0001ITP-00005exit`) |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `indicator` | str | Yes | Exact-case indicator name | `Available through UIOLI short-term` |
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
  "https://transparency.entsog.eu/api/v1/operationalData?from=2026-05-06&to=2026-05-06&timeZone=UCT&indicator=Available%20through%20UIOLI%20short-term&periodType=day&pointDirection=UK-TSO-0001ITP-00005exit&forceDownload=true&limit=1000"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsog/available_through_uioli_short_term/<year>/<month>/<day>/raw_<uuid>.json`
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
        "Available through UIOLI short-term"
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
      "id": "5UK-TSO-0001ITP-00005exitUK-TSO-0003Available through UIOLI short-term",
      "dataset": "5",
      "indicator": "Available through UIOLI short-term",
      "periodType": "",
      "periodFrom": "2026-05-06T00:00:00+02:00",
      "periodTo": "2026-05-06T00:00:00+02:00",
      "operatorKey": "UK-TSO-0001",
      "tsoEicCode": "21X-GB-A-A0A0A-7",
      "operatorLabel": "National Gas TSO",
      "pointKey": "ITP-00005",
      "pointLabel": "Bacton (IUK)",
      "tsoItemIdentifier": "21Z000000000083P",
      "directionKey": "exit",
      "unit": "",
      "itemRemarks": "",
      "generalRemarks": "",
      "value": "",
      "lastUpdateDateTime": "2026-05-08T18:05:40+02:00",
      "isUnlimited": "",
      "flowStatus": "",
      "interruptionType": "",
      "restorationInformation": "",
      "capacityType": "",
      "capacityBookingStatus": "",
      "isCamRelevant": false,
      "isNA": "",
      "originalPeriodFrom": "",
      "isCmpRelevant": "",
      "isDefaultSentence": true,
      "defaultSentence": "Available through UIOLI short-term: Currently no capacity has been made available on this point through the application of the congestion-management procedures."
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsog/available_through_uioli_short_term/year=YYYY/month=MM/available_through_uioli_short_term_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsog.GenericEntsogJsonTransformer (subclass AvailableThroughUioliShortTermTransformer)`
**Pydantic schema**: `Generic — no Pydantic schema declared`
**Dedup key**: the vendor `id`, `keep="last"`, within each day's bronze read (`silver/entsog/generic.py:193-199`). A default-sentence `id` joins the dataset code, keys, an adjacent operator and the indicator, with no date; see Known issues for the repeated 4-tuple.
**Bronze read filter**: a record is kept only when the local date of its `periodFrom` is the bronze day (`generic.py:157-161`, `:332`; `datetime.py:56-87`); see Known issues.
**Point-in-time field**: none used by the pipeline. `last_update_date_time` is the vendor's `lastUpdateDateTime`, converted to UTC (`generic.py:181-183`); `ingested_at` is the silver transform time (`generic.py:201-206`).

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| timestamp_utc | datetime[UTC] | Yes | derived | `period_from` copied (`generic.py:185-187`); 22:00 UTC the previous day on the default-sentence rows (`periodFrom` 00:00+02:00) |
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
| unit | str | Yes | unit | As sent, not converted; `""` on every kept 2026-08/09 row |
| value | float | Yes | value | In the row's `unit`, not converted; sent as `""` it is null (Float64 cast with `strict=False`, `generic.py:189-191`) |
| id | str | Yes | id | Dedup key (see above) |
| dataset | str | Yes | dataset |  |
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
| is_default_sentence | bool | Yes | isDefaultSentence |  |
| default_sentence | str | Yes | defaultSentence |  |
| data_provider | str | No | derived | Always `entsog` |
| ingested_at | datetime[UTC] | No | derived | Silver transform time (`generic.py:201-206`) |

### Silver sample

```python
[
    {
        "timestamp_utc": "2026-08-04T22:00:00+00:00",
        "period_from": "2026-08-04T22:00:00+00:00",
        "period_to": "2026-08-04T22:00:00+00:00",
        "indicator": "Available through UIOLI short-term",
        "period_type": "",
        "operator_key": "UK-TSO-0001",
        "operator_label": "National Gas TSO",
        "tso_eic_code": "21X-GB-A-A0A0A-7",
        "point_key": "ITP-00005",
        "point_label": "Bacton (IUK)",
        "direction_key": "exit",
        "unit": "",
        "value": null,
        "id": "5UK-TSO-0001ITP-00005exitUK-TSO-0003Available through UIOLI short-term",
        "dataset": "5",
        "tso_item_identifier": "21Z000000000083P",
        "item_remarks": "",
        "general_remarks": "",
        "last_update_date_time": "2026-08-16T14:08:10+00:00",
        "is_unlimited": "",
        "flow_status": "",
        "interruption_type": "",
        "restoration_information": "",
        "capacity_type": "",
        "capacity_booking_status": "",
        "is_cam_relevant": false,
        "is_na": "",
        "original_period_from": null,
        "is_cmp_relevant": "",
        "is_default_sentence": true,
        "default_sentence": "Available through UIOLI short-term: Currently no capacity has been made available on this point through the application of the congestion-management procedures.",
        "data_provider": "entsog",
        "ingested_at": "2026-08-16T14:21:03.701585+00:00"
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
- **Silver drops records whose validity starts before the fetched gas day**: the generic transformer runs the gas-day filter `partition_records_to_target_date` on every dataset that requires dates (`silver/entsog/generic.py:157-161`; `date_window_dataset = endpoint.requires_dates`, `:332`; `datetime.py:56-87`), so a record is kept only when the local date of its `periodFrom` is the bronze day (`datetime.py:191-213`). Capacity records are validity periods (in 2026-08/09 bronze, from one day to 2015-2048), so most are dropped. `tariffs` and `tariff_simulations` are exempt for the same reason (`generic.py:297-306`); capacity indicators are not. 2026-08/09: 55 bronze records (0 with a value) became 55 silver rows (0 with a value).
- **Default-sentence records**: the records sent without a value carry `isDefaultSentence` true and the `defaultSentence` quoted in the overview, with `dataset` "5" (a lowercase key, so silver has a `dataset` column and no `data_set`), `periodType` "", `unit` "", `value` "", and `periodFrom` = `periodTo` = 00:00+02:00. `timestamp_utc` is therefore 22:00 UTC on the previous day: the 2026-08-03 partition holds rows stamped 2 August.
- **Repeated 4-tuple**: National Gas TSO `ITP-00090` entry sends three default-sentence records a day, whose `id` names the adjacent operators `IE-TSO-0001`, `IE-TSO-0002` and `UK-TSO-0002`. Dedup on `id` keeps all three, so `(timestamp_utc, operator_key, point_key, direction_key)` is not unique.
- **No valued records**: every 2026-08 response for this indicator holds only default-sentence records.
- **Requested versus returned (2026-08 bronze)**: `meta.count` equals `meta.total` (11) in every response.



---

## Implementation delta

- **Silver retention**: the generic gas-day filter drops capacity records whose validity starts before the fetched day (see Known issues). The indicator name matches the code's exact-case constant in `OPERATIONAL_INDICATORS` (`connectors/entsog/endpoints.py:95-115`).
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
