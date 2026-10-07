---
source: entsog
dataset_key: methane_content
vendor: ENTSOG Transparency Platform
last_verified: 2026-06-04
layer_coverage: bronze, silver
---

# ENTSOG — Methane Content (`indicator=Methane Content`)

## Overview

Methane (CH4) content of the gas at the point, in `% (mol/mol)` as sent (a molar fraction). In 2026-08/09 bronze, rows come from Interconnector (Bacton (IUK) entry; its exit is 0) and GNI (Moffat (IE) entry) only.

The dataset is one of 19 indicators served by the same `/operationalData`
endpoint. The (operator, point, direction) tuple selects which physical
location to read; the `indicator` query parameter selects which series
(physical flow, nomination, allocation, etc.) is returned. Records carry
the daily `periodFrom` / `periodTo` window and a `value` in `kWh/d` (or
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
| Publication lag  | Not vendor-documented here. 2026-08/09 bronze: `lastUpdateDateTime` 25 h to 29 h after the gas-day start for GNI, 29 h to 52 h for Interconnector; `flowStatus` `Provisional` or `Confirmed` |
| Response format  | JSON |
| Indicator | `Methane Content` (exact-case — vendor rejects lowercase or hyphen variants) |
| Time zone | `timeZone=UCT` (ENTSOG's spelling — note the typo; not `UTC`) |
| `pointDirection` filter | `operatorKey + pointKey + directionKey` concatenated, no separator (e.g. `UK-TSO-0001ITP-00005exit`) |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `indicator` | str | Yes | Exact-case indicator name | `Methane Content` |
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
  "https://transparency.entsog.eu/api/v1/operationalData?from=2026-05-06&to=2026-05-06&timeZone=UCT&indicator=Methane%20Content&periodType=day&pointDirection=UK-TSO-0001ITP-00005exit&forceDownload=true&limit=1000"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsog/methane_content/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per `fetch()` call (one calendar day per file by convention)

### Bronze sample

```json
{
  "meta": {
    "limit": 1000,
    "offset": 0,
    "count": 1,
    "total": 0,
    "query": {
      "indicator": [
        "Methane Content"
      ],
      "periodType": "day",
      "pointDirection": "UK-TSO-0001ITP-00005exit",
      "from": "2026-05-06",
      "to": "2026-05-06",
      "timeZone": "UCT"
    },
    "timezone": "CET"
  },
  "operationalData": []
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsog/methane_content/year=YYYY/month=MM/methane_content_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsog.GenericEntsogJsonTransformer (subclass MethaneContentTransformer)`
**Pydantic schema**: `Generic — no Pydantic schema declared`
**Dedup key**: the vendor `id`, `keep="last"`, within each day's bronze read (`silver/entsog/generic.py:193-199`). The `id` concatenates indicator, period, operator, point, direction and unit, so `(timestamp_utc, operator_key, point_key, direction_key)` is unique in 2026-08/09 silver.
**Point-in-time field**: none used by the pipeline. `last_update_date_time` is the vendor's `lastUpdateDateTime` as sent, converted to UTC (`generic.py:181-183`); `ingested_at` is the silver transform time (`generic.py:201-206`).

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| timestamp_utc | datetime[UTC] | Yes | derived | `period_from` copied (`generic.py:185-187`): the gas-day start, `periodFrom` 06:00+02:00 as sent, 04:00 UTC, on every valued 2026-08/09 row |
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
| unit | str | Yes | unit | As sent, not converted; `% (mol/mol)` on every 2026-08/09 row; no reference conditions in the response |
| value | float | Yes | value | In the row's `unit`, not converted (Float64 cast with `strict=False`, `generic.py:189-191`) |
| id | str | Yes | id | Dedup key (see above) |
| data_set | Int64 | Yes | dataSet |  |
| tso_item_identifier | str | Yes | tsoItemIdentifier |  |
| item_remarks | null | Yes | itemRemarks | Null dtype: null on every 2026-08/09 row |
| general_remarks | null | Yes | generalRemarks | Null dtype: null on every 2026-08/09 row |
| last_update_date_time | datetime[UTC] | Yes | lastUpdateDateTime | Vendor stamp, converted to UTC; not used by the pipeline |
| is_unlimited | null | Yes | isUnlimited | Null dtype: null on every 2026-08/09 row |
| flow_status | str | Yes | flowStatus | `Provisional` or `Confirmed` |
| interruption_type | null | Yes | interruptionType | Null dtype: null on every 2026-08/09 row |
| restoration_information | null | Yes | restorationInformation | Null dtype: null on every 2026-08/09 row |
| capacity_type | null | Yes | capacityType | Null dtype: null on every 2026-08/09 row |
| capacity_booking_status | null | Yes | capacityBookingStatus | Null dtype: null on every 2026-08/09 row |
| is_cam_relevant | bool | Yes | isCamRelevant |  |
| is_na | null | Yes | isNA | Null dtype: null on every 2026-08/09 row |
| original_period_from | datetime[UTC] | Yes | originalPeriodFrom |  |
| is_cmp_relevant | bool | Yes | isCmpRelevant |  |
| booking_platform_key | str | Yes | bookingPlatformKey |  |
| booking_platform_label | null | Yes | bookingPlatformLabel | Null dtype: null on every 2026-08/09 row |
| booking_platform_url | str | Yes | bookingPlatformURL |  |
| interruption_calculation_remark | null | Yes | interruptionCalculationRemark | Null dtype: null on every 2026-08/09 row |
| point_type | str | Yes | pointType |  |
| id_point_type | Int64 | Yes | idPointType |  |
| is_archived | bool | Yes | isArchived |  |
| data_provider | str | No | derived | Always `entsog` |
| ingested_at | datetime[UTC] | No | derived | Silver transform time (`generic.py:201-206`) |

### Silver sample

```python
[
    {
        "timestamp_utc": "2026-09-21T04:00:00+00:00",
        "period_from": "2026-09-21T04:00:00+00:00",
        "period_to": "2026-09-22T04:00:00+00:00",
        "indicator": "Methane Content",
        "period_type": "day",
        "operator_key": "IE-TSO-0002",
        "operator_label": "GNI",
        "tso_eic_code": "47X0000000000576",
        "point_key": "ITP-00495",
        "point_label": "Moffat (IE)",
        "direction_key": "entry",
        "unit": "% (mol/mol)",
        "value": 87.73,
        "id": "1Methane Contentday2026-09-212026-09-22IE-TSO-0002ITP-00495entry% (mol/mol)",
        "data_set": 1,
        "tso_item_identifier": "21Z000000000081T",
        "item_remarks": null,
        "general_remarks": null,
        "last_update_date_time": "2026-09-22T05:03:49+00:00",
        "is_unlimited": null,
        "flow_status": "Provisional",
        "interruption_type": null,
        "restoration_information": null,
        "capacity_type": null,
        "capacity_booking_status": null,
        "is_cam_relevant": true,
        "is_na": null,
        "original_period_from": null,
        "is_cmp_relevant": true,
        "booking_platform_key": "PRISMA",
        "booking_platform_label": null,
        "booking_platform_url": "https://platform.prisma-capacity.eu/",
        "interruption_calculation_remark": null,
        "point_type": "Cross-Border Transmission IP between EU and ExtEU",
        "id_point_type": 23,
        "is_archived": false,
        "data_provider": "entsog",
        "ingested_at": "2026-09-26T17:45:45+00:00"
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
- **Requested versus returned (2026-08/09 bronze, 14 gas days)**: the connector sends nine `pointDirection` filters (`connectors/entsog/endpoints.py:24-34`); every response returns three records: Interconnector's Bacton (IUK) entry and exit and GNI's Moffat (IE) entry. No placeholders. With `limit=-1`, `meta.count` is 3 against `meta.total` 6; what `total` counts is unverified.
- **Interconnector's exit is zero**: Interconnector's Bacton (IUK) exit `value` is 0 on all 14 gas days of 2026-08/09, `Confirmed` or `Provisional`. Zero is not a gas-quality measurement; treat it as no value.
- **Repeated values**: Interconnector sends 85.39 on six consecutive gas days, 13 to 18 September 2026, each with its own `lastUpdateDateTime`. Unexplained.



---

## Implementation delta

- **Vendor empty convention**: ENTSOG returns HTTP 404 with body `{"message":"No result found"}` instead of HTTP 200 with `[]` when an indicator/window combination has no rows. The connector's retry policy (`@RETRY_POLICY`) treats 4xx as final by default — confirm 404 is not retried indefinitely.
- **Synthetic fixture**: `tests/fixtures/entsog/physical_flows_response.json` carries placeholder `pointKey: "IUK"` and `operatorKey: "OP-IUK"`. Live data uses real keys (`ITP-00005`, `UK-TSO-0001`). Fixture regeneration is deferred (silver tests depend on the placeholder shape).

---

## Modelling notes

- Used as raw input to gas balance / interconnector flow features in `gridflow_models/`.
- Target candidates: directional flow magnitude (entry vs exit per point).
- Drop Interconnector's zero exit rows first. `flow_status` is `Provisional` on every GNI row in 2026-08/09 and mostly `Confirmed` for Interconnector, so a `Confirmed` filter keeps Interconnector only.
- Join with `operator_point_directions` to attach country, balancing zone, and CAM-relevant flags.

---

## Links

- [Official API docs (PDF)](https://transparency.entsog.eu/api/archiveDirectories/8/api-manual/TP_REG715_Documentation_TP_API%20-%20v2.1.pdf)
- `src/gridflow/connectors/entsog/endpoints.py`
- `src/gridflow/silver/entsog/generic.py`
- `src/gridflow/schemas/entsog.py`
- Gold view/builder
- [Domain: gas day](../../../20-domain/concepts/gas-day.md)
