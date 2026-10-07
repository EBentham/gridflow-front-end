---
source: entsog
dataset_key: wobbe_index
vendor: ENTSOG Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
---

# ENTSOG — Wobbe Index (`indicator=Wobbe Index`)

## Overview

Wobbe index of the gas at the point (interchangeability indicator), in `kWh/Nm3` as sent; the response states no reference conditions. In 2026-08/09 bronze only Interconnector sends values (Bacton (IUK) entry; its exit is 0). National Gas TSO's placeholder remark says it publishes GCV and not the Wobbe index.

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
| Publication lag  | Not vendor-documented here. 2026-08/09 bronze: `lastUpdateDateTime` 29 h to 52 h after the gas-day start (Interconnector, the only operator sending values); `flowStatus` `Provisional` or `Confirmed`, empty on placeholders |
| Response format  | JSON |
| Indicator | `Wobbe Index` (exact-case — vendor rejects lowercase or hyphen variants) |
| Time zone | `timeZone=UCT` (ENTSOG's spelling — note the typo; not `UTC`) |
| `pointDirection` filter | `operatorKey + pointKey + directionKey` concatenated, no separator (e.g. `UK-TSO-0001ITP-00005exit`) |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `indicator` | str | Yes | Exact-case indicator name | `Wobbe Index` |
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
  "https://transparency.entsog.eu/api/v1/operationalData?from=2026-05-06&to=2026-05-06&timeZone=UCT&indicator=Wobbe%20Index&periodType=day&pointDirection=UK-TSO-0001ITP-00005exit&forceDownload=true&limit=1000"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsog/wobbe_index/<year>/<month>/<day>/raw_<uuid>.json`
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
        "Wobbe Index"
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
      "id": "1Wobbe IndexdayUK-TSO-0001ITP-00005exitkWh/Nm32026-01-012027-01-01_NA0",
      "dataSet": 1,
      "indicator": "Wobbe Index",
      "periodType": "day",
      "periodFrom": "2026-05-06T05:00:00+02:00",
      "periodTo": "2026-05-07T05:00:00+02:00",
      "operatorKey": "UK-TSO-0001",
      "tsoEicCode": "21X-GB-A-A0A0A-7",
      "operatorLabel": "National Gas TSO",
      "pointKey": "ITP-00005",
      "pointLabel": "Bacton (IUK)",
      "tsoItemIdentifier": "21Z000000000083P",
      "directionKey": "exit",
      "unit": "kWh/Nm3",
      "itemRemarks": "According to article 3.3.4 of Annex 1 of Reg. 715/2009 TSO publishes either the GCV or the WI, we publish GCV and not WI. You may find additional information about Wobbe Index on our website, at least if the point falls under art. 16 of Reg. 2015/703",
      "generalRemarks": "",
      "value": "",
      "lastUpdateDateTime": "2025-02-20T14:02:39+01:00",
      "isUnlimited": null,
      "flowStatus": "",
      "interruptionType": null,
      "restorationInformation": null,
      "capacityType": null,
      "capacityBookingStatus": null,
      "isCamRelevant": null,
      "isNA": 1,
      "originalPeriodFrom": "2013-10-01T05:00:00+02:00",
      "isCmpRelevant": "",
      "bookingPlatformKey": "",
      "bookingPlatformLabel": "",
      "bookingPlatformURL": "",
      "interruptionCalculationRemark": null
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsog/wobbe_index/year=YYYY/month=MM/wobbe_index_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsog.GenericEntsogJsonTransformer (subclass WobbeIndexTransformer)`
**Pydantic schema**: `Generic — no Pydantic schema declared`
**Dedup key**: the vendor `id`, `keep="last"`, within each day's bronze read (`silver/entsog/generic.py:193-199`). The `id` concatenates indicator, period, operator, point, direction and unit, so `(timestamp_utc, operator_key, point_key, direction_key)` is unique in 2026-08/09 silver.
**Point-in-time field**: none used by the pipeline. `last_update_date_time` is the vendor's `lastUpdateDateTime` as sent, converted to UTC (`generic.py:181-183`); `ingested_at` is the silver transform time (`generic.py:201-206`).

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| timestamp_utc | datetime[UTC] | Yes | derived | `period_from` copied (`generic.py:185-187`): the gas-day start, `periodFrom` 06:00+02:00 as sent, 04:00 UTC, on every valued 2026-08/09 row; placeholders sit at 03:00 UTC, GNI's at 02:00 UTC |
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
| unit | str | Yes | unit | As sent, not converted; `kWh/Nm3` on every 2026-08/09 row; no reference conditions in the response |
| value | float | Yes | value | In the row's `unit`, not converted (Float64 cast with `strict=False`, `generic.py:189-191`); sent as `""` on placeholders, it is null |
| id | str | Yes | id | Dedup key (see above); placeholder ids carry no gas-day date and their `_NA<n>` suffix changes between days |
| data_set | Int64 | Yes | dataSet |  |
| tso_item_identifier | str | Yes | tsoItemIdentifier |  |
| item_remarks | str | Yes | itemRemarks |  |
| general_remarks | str | Yes | generalRemarks |  |
| last_update_date_time | datetime[UTC] | Yes | lastUpdateDateTime | Vendor stamp, converted to UTC; not used by the pipeline |
| is_unlimited | null | Yes | isUnlimited | Null dtype: null on every 2026-08/09 row |
| flow_status | str | Yes | flowStatus | `Provisional` or `Confirmed`; empty string on placeholders |
| interruption_type | null | Yes | interruptionType | Null dtype: null on every 2026-08/09 row |
| restoration_information | null | Yes | restorationInformation | Null dtype: null on every 2026-08/09 row |
| capacity_type | null | Yes | capacityType | Null dtype: null on every 2026-08/09 row |
| capacity_booking_status | null | Yes | capacityBookingStatus | Null dtype: null on every 2026-08/09 row |
| is_cam_relevant | bool | Yes | isCamRelevant |  |
| is_na | Int64 | Yes | isNA | 1 on not-applicable placeholders, else null |
| original_period_from | datetime[UTC] | Yes | originalPeriodFrom |  |
| is_cmp_relevant | str | Yes | isCmpRelevant | Kept as text: placeholders send `""`, valued rows `true`/`false` |
| booking_platform_key | str | Yes | bookingPlatformKey |  |
| booking_platform_label | str | Yes | bookingPlatformLabel |  |
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
        "indicator": "Wobbe Index",
        "period_type": "day",
        "operator_key": "UK-TSO-0003",
        "operator_label": "Interconnector",
        "tso_eic_code": "21X-GB-B-A0A0A-Z",
        "point_key": "ITP-00005",
        "point_label": "Bacton (IUK)",
        "direction_key": "entry",
        "unit": "kWh/Nm3",
        "value": 14.613,
        "id": "1Wobbe Indexday2026-09-212026-09-22UK-TSO-0003ITP-00005entrykWh/Nm3",
        "data_set": 1,
        "tso_item_identifier": "21Z000000000084N",
        "item_remarks": null,
        "general_remarks": null,
        "last_update_date_time": "2026-09-22T08:39:49+00:00",
        "is_unlimited": null,
        "flow_status": "Confirmed",
        "interruption_type": null,
        "restoration_information": null,
        "capacity_type": null,
        "capacity_booking_status": null,
        "is_cam_relevant": true,
        "is_na": null,
        "original_period_from": null,
        "is_cmp_relevant": "true",
        "booking_platform_key": "PRISMA",
        "booking_platform_label": null,
        "booking_platform_url": "https://platform.prisma-capacity.eu/",
        "interruption_calculation_remark": null,
        "point_type": "Cross-Border Transmission IP between EU and ExtEU",
        "id_point_type": 23,
        "is_archived": false,
        "data_provider": "entsog",
        "ingested_at": "2026-09-26T17:46:38+00:00"
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
- **Requested versus returned (2026-08/09 bronze, 14 gas days)**: the connector sends nine `pointDirection` filters (`connectors/entsog/endpoints.py:24-34`); every response returns nine records (`meta.count` 9, `meta.total` 9). Only Interconnector's Bacton (IUK) entry and exit carry values. The other seven are not-applicable placeholders (`isNA` 1, `value` `""`): National Gas TSO's Bacton (IUK) exit, Bacton (BBL) exit and Moffat entry and BBL company's Julianadorp entry and exit, all with the remark "According to article 3.3.4 of Annex 1 of Reg. 715/2009 TSO publishes either the GCV or the WI, we publish GCV and not WI" (truncated); GNI's Moffat (IE) entry ("n/a") and exit ("GCV published").
- **Interconnector's exit is zero**: Interconnector's Bacton (IUK) exit `value` is 0 on all 14 gas days of 2026-08/09, `Confirmed` or `Provisional`. Zero is not a gas-quality measurement; treat it as no value.
- **Three `timestamp_utc` values per gas day**: GNI's placeholders send `periodFrom` 04:00+02:00 (02:00 UTC), the other placeholders 05:00+02:00 (03:00 UTC), valued rows 06:00+02:00 (04:00 UTC).
- **Placeholder ids are not stable across days**: the `_NA<n>` suffix alternates between two values for the same operator, point and direction (for example `_NA0`/`_NA4` for National Gas TSO Bacton (BBL) exit). Do not key on `id` across days.
- **Repeated values**: Interconnector sends 14.653 on seven consecutive gas days, 13 to 19 September 2026, each with its own `lastUpdateDateTime`. Unexplained.



---

## Implementation delta

- **No documented discrepancies** for this indicator. The exact-case constant is in `OPERATIONAL_INDICATORS` (`connectors/entsog/endpoints.py:95-115`); the response echoes it in `meta.query.indicator` (`meta.fields` lists field names, not the indicator).
- **Synthetic fixture**: `tests/fixtures/entsog/physical_flows_response.json` carries placeholder `pointKey: "IUK"` and `operatorKey: "OP-IUK"`. Live data uses real keys (`ITP-00005`, `UK-TSO-0001`). Fixture regeneration is deferred (silver tests depend on the placeholder shape).

---

## Modelling notes

- Used as raw input to gas balance / interconnector flow features in `gridflow_models/`.
- Target candidates: directional flow magnitude (entry vs exit per point).
- Drop not-applicable placeholders (`is_na == 1`) and Interconnector's zero exit rows first; what remains is Interconnector's Bacton (IUK) entry, mostly `Confirmed` in 2026-08/09.
- Join with `operator_point_directions` to attach country, balancing zone, and CAM-relevant flags.

---

## Links

- [Official API docs (PDF)](https://transparency.entsog.eu/api/archiveDirectories/8/api-manual/TP_REG715_Documentation_TP_API%20-%20v2.1.pdf)
- `src/gridflow/connectors/entsog/endpoints.py`
- `src/gridflow/silver/entsog/generic.py`
- `src/gridflow/schemas/entsog.py`
- Gold view/builder
- [Domain: gas day](../../../20-domain/concepts/gas-day.md)
