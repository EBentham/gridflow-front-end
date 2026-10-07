---
source: entsog
dataset_key: gcv
vendor: ENTSOG Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Gas quality at interconnection points
  summary: >-
    Daily gross calorific value and methane content at Bacton and Moffat, plus Wobbe index,
    hydrogen and oxygen at Bacton, from ENTSOG.
  facts:
    vendor: "ENTSOG Transparency Platform, indicators GCV, Wobbe Index and three gas contents"
    cadence: Daily, one value per gas day
    grain: One row per gas day, operator, point and direction
  landscape: gas
  what_it_is: >-
    Five ENTSOG gas quality indicators for the nine operator, point and direction filters gridflow
    sends for the BBL, IUK and Moffat interconnections. Values stay as sent: `kWh/Nm3` for GCV and
    Wobbe index, `% (mol/mol)` for the contents; the response states no reference conditions.
    Some filters return not-applicable placeholders, with a remark, instead of a value.
  how_used:
    - Comparing the two operators' GCV reports at Bacton (IUK) for one gas day.
    - Checking Interconnector's Wobbe index and methane content against its GCV.
    - Following GNI's daily GCV and methane content at Moffat (IE) entry.
  chart:
    type: line
    silver: entsog/gcv
    time: timestamp_utc
    value: value
    filter:
      - {column: value, op: gt, value: 0}
    group: operator_key
    group_map:
      IE-TSO-0002: moffat_ie
      UK-TSO-0001: bacton_iuk_exit
      UK-TSO-0003: bacton_iuk_entry
    series_order: [moffat_ie, bacton_iuk_exit, bacton_iuk_entry]
    aggregation: last
    window: {start: "2026-09-13", end: "2026-09-21"}
    unit: kWh/Nm3
  chart_view:
    title: GCV at Bacton and Moffat, 13 to 21 September 2026
    caption: >-
      Silver `entsog/gcv` only, `kWh/Nm3` as sent, gas days 13 to 21 September 2026, rows with a
      value above zero. Interconnector's exit report, zero on every day shown, and the
      not-applicable placeholders are left out.
    alt: >-
      Line chart of daily gross calorific value from entsog/gcv, in kWh/Nm3, for gas days 13 to 21
      September 2026. GNI's Moffat (IE) entry moves between 11.76 and 11.87, ending at 11.84.
      National Gas TSO's Bacton (IUK) exit holds 11.643 from the 13th to the 18th, then reads
      11.693, 11.614 and 11.59. Interconnector's Bacton (IUK) entry holds 11.645 to the 18th,
      reads 11.673 on the 19th, jumps to 14.253 on the 20th and returns to 11.602 on the 21st.
    x_label: gas day, starting 04:00 UTC
    key:
      - {series: moffat_ie, label: "Moffat (IE) entry", codes: IE-TSO-0002, paint: petrol, note: "GNI's report, Provisional throughout; its Moffat exit is a not-applicable placeholder."}
      - {series: bacton_iuk_exit, label: "Bacton (IUK) exit", codes: UK-TSO-0001, paint: horizon, note: "National Gas TSO's report, Provisional throughout; 11.643 on six days running."}
      - {series: bacton_iuk_entry, label: "Bacton (IUK) entry", codes: UK-TSO-0003, paint: clay, note: "Interconnector's report; within 0.02 of National Gas TSO's except 14.253 on the 20th, sent `Confirmed`."}
  raw_feed:
    note: >-
      One request per day and indicator to `operationalData`, with nine operator, point and
      direction filters. The response's `meta.total` can exceed the records returned, unexplained.
      Silver keeps `value` and `unit` unconverted.
    requests:
      - "GET https://transparency.entsog.eu/api/v1/operationalData?limit=-1&timeZone=UCT&from=2026-09-21&to=2026-09-21&indicator=GCV&periodType=day&pointDirection=UK-TSO-0001ITP-00005exit%2CUK-TSO-0003ITP-00005entry%2CUK-TSO-0003ITP-00005exit%2CUK-TSO-0001ITP-00207exit%2CUK-TSO-0004ITP-00063entry%2CUK-TSO-0004ITP-00063exit%2CIE-TSO-0002ITP-00495entry%2CIE-TSO-0002ITP-00495exit%2CUK-TSO-0001ITP-00090entry"
    commands:
      - {run: gridflow ingest entsog gcv --start 2026-09-13 --end 2026-09-22, comment: "bronze, end exclusive; repeat per member"}
      - {run: gridflow transform entsog gcv --start 2026-09-13 --end 2026-09-21, comment: "silver, units kept; repeat per member"}
  record:
    select:
      filter:
        - {column: timestamp_utc, op: in, value: ["2026-09-20T04:00:00", "2026-09-21T04:00:00"]}
        - {column: value, op: not_null}
      order_by: [timestamp_utc, point_key, operator_key, direction_key]
      columns: [timestamp_utc, operator_key, point_key, direction_key, value, unit, flow_status, last_update_date_time, operator_label, point_label]
    key: [timestamp_utc, operator_key, point_key, direction_key]
    caption: "Gas days 20 and 21 September 2026, every row with a value."
    fields:
      timestamp_utc: "Gas-day start from `periodFrom`, in UTC; placeholders send an earlier one"
      operator_key: ENTSOG key of the operator reporting this row
      point_key: "ENTSOG point key, such as `ITP-00005` for Bacton (IUK)"
      direction_key: "`entry` or `exit`, lowercase as sent, from the reporting operator's side"
      value: "GCV in the row's `unit`, as sent; Interconnector's exit sends 0, placeholders null"
      unit: "Vendor unit as sent, not converted; no reference conditions stated"
      flow_status: "Vendor `flowStatus`: `Provisional` or `Confirmed`; empty on placeholders"
      last_update_date_time: "The vendor's `lastUpdateDateTime` for this row, converted to UTC"
      operator_label: Name of the operator reporting this row, as sent
      point_label: ENTSOG's name for the point, as sent
      period_from: "Gas-day start as sent in `periodFrom`, converted to UTC"
      period_to: "Gas-day end as sent in `periodTo`, converted to UTC"
      indicator: "The indicator requested, as sent: `GCV`"
      period_type: "`day`, the period type the connector requests"
      tso_eic_code: Energy Identification Code of the reporting operator, as sent
      id: "Vendor record id, the deduplication key: indicator, dates, keys and unit joined"
      data_set: "Vendor `dataSet` code, as sent; ENTSOG's meaning for it is not documented here"
      tso_item_identifier: The reporting operator's own identifier for the point, as sent
      item_remarks: "The operator's remark, as sent; each placeholder carries one, null in these rows"
      general_remarks: The operator's general remark, as sent; null in these rows
      is_unlimited: Capacity flag shared by all indicators; null in these rows
      interruption_type: Interruption field shared by all indicators; null in these rows
      restoration_information: Interruption restoration field shared by all indicators; null in these rows
      capacity_type: Capacity field shared by all indicators; null in these rows
      capacity_booking_status: Capacity booking field shared by all indicators; null in these rows
      is_cam_relevant: "Vendor flag for capacity allocation mechanism (CAM) relevance, as sent"
      is_na: "Vendor not-applicable flag: 1 on placeholders, null in these rows"
      original_period_from: "Vendor `originalPeriodFrom`, converted to UTC; null in these rows"
      is_cmp_relevant: "Vendor congestion management procedure (CMP) relevance flag; text, as placeholders send it empty"
      booking_platform_key: Capacity booking platform for the point, as sent
      booking_platform_label: Booking platform name; null in these rows
      booking_platform_url: Booking platform web address, as sent
      interruption_calculation_remark: Interruption calculation field shared by all indicators; null in these rows
      point_type: ENTSOG's type for the point, as sent
      id_point_type: ENTSOG's numeric code for the point type, as sent
      is_archived: Vendor archive flag, as sent
  notebook:
    lead: >-
      Reads each member's `silver_entsog_<member>` relation, lineage columns dropped, where
      `timestamp_utc` falls on the UTC dates given, ends included, then joins the five indicators
      at Interconnector's Bacton (IUK) entry.
    cells:
      - |
        members = ["gcv", "wobbe_index", "methane_content", "hydrogen_content", "oxygen_content"]
        frames = {m: data.entsog.query(m, "2026-09-13", "2026-09-21") for m in members}
      - |
        key = ["timestamp_utc", "operator_key", "point_key", "direction_key"]
        iuk = None
        for m, df in frames.items():
            part = df[(df.operator_key == "UK-TSO-0003") & (df.direction_key == "entry")]
            part = part[key + ["value"]].rename(columns={"value": m})
            iuk = part if iuk is None else iuk.merge(part, on=key)
        iuk = iuk.sort_values("timestamp_utc").assign(
            timestamp_utc=lambda d: d.timestamp_utc.dt.tz_convert("UTC"))
        iuk[["timestamp_utc"] + members]
      - |
        iuk.plot(x="timestamp_utc", y=["gcv", "wobbe_index"], color=["#C77E3C", "#155A6E"],
                 ylabel="kWh/Nm3", figsize=(8, 3.5))
    needs: gas days 13 to 21 September 2026, all five members
    plot_alt: >-
      Line plot of Interconnector's Bacton (IUK) entry in kWh/Nm3 for gas days 13 to 21 September
      2026. The Wobbe index holds 14.653 to the 19th, reads 14.901 on the 20th and 14.613 on the
      21st. GCV runs below at 11.645 to the 18th and 11.673 on the 19th, rises to 14.253 on the
      20th and returns to 11.602.
  related:
    - {dataset: entsog/physical_flows, note: "Physical flow at the same points, from the same endpoint"}
    - {dataset: entsog/nominations, note: "Nominated quantities, requested with the same nine filters"}
    - {dataset: entsog/operator_point_directions, note: "The register of the operator, point and direction keys used here"}
  family:
    slug: gas-quality
    members:
      - dataset: gcv
        differs: "Gross calorific value in `kWh/Nm3`; Interconnector, National Gas TSO and GNI send values"
        request: "GET https://transparency.entsog.eu/api/v1/operationalData?limit=-1&timeZone=UCT&from=2026-09-21&to=2026-09-21&indicator=GCV&periodType=day&pointDirection=UK-TSO-0001ITP-00005exit%2CUK-TSO-0003ITP-00005entry%2CUK-TSO-0003ITP-00005exit%2CUK-TSO-0001ITP-00207exit%2CUK-TSO-0004ITP-00063entry%2CUK-TSO-0004ITP-00063exit%2CIE-TSO-0002ITP-00495entry%2CIE-TSO-0002ITP-00495exit%2CUK-TSO-0001ITP-00090entry"
      - dataset: wobbe_index
        differs: "Wobbe index in `kWh/Nm3`; only Interconnector sends values, National Gas TSO publishes GCV instead"
        request: "GET https://transparency.entsog.eu/api/v1/operationalData?limit=-1&timeZone=UCT&from=2026-09-21&to=2026-09-21&indicator=Wobbe+Index&periodType=day&pointDirection=UK-TSO-0001ITP-00005exit%2CUK-TSO-0003ITP-00005entry%2CUK-TSO-0003ITP-00005exit%2CUK-TSO-0001ITP-00207exit%2CUK-TSO-0004ITP-00063entry%2CUK-TSO-0004ITP-00063exit%2CIE-TSO-0002ITP-00495entry%2CIE-TSO-0002ITP-00495exit%2CUK-TSO-0001ITP-00090entry"
      - dataset: methane_content
        differs: "Methane in `% (mol/mol)`; Bacton (IUK) and Moffat (IE) entry; Interconnector's exit sends 0"
        request: "GET https://transparency.entsog.eu/api/v1/operationalData?limit=-1&timeZone=UCT&from=2026-09-21&to=2026-09-21&indicator=Methane+Content&periodType=day&pointDirection=UK-TSO-0001ITP-00005exit%2CUK-TSO-0003ITP-00005entry%2CUK-TSO-0003ITP-00005exit%2CUK-TSO-0001ITP-00207exit%2CUK-TSO-0004ITP-00063entry%2CUK-TSO-0004ITP-00063exit%2CIE-TSO-0002ITP-00495entry%2CIE-TSO-0002ITP-00495exit%2CUK-TSO-0001ITP-00090entry"
      - dataset: hydrogen_content
        differs: "Hydrogen in `% (mol/mol)`; Interconnector at Bacton (IUK) entry, its exit sends 0"
        request: "GET https://transparency.entsog.eu/api/v1/operationalData?limit=-1&timeZone=UCT&from=2026-09-21&to=2026-09-21&indicator=Hydrogen+Content&periodType=day&pointDirection=UK-TSO-0001ITP-00005exit%2CUK-TSO-0003ITP-00005entry%2CUK-TSO-0003ITP-00005exit%2CUK-TSO-0001ITP-00207exit%2CUK-TSO-0004ITP-00063entry%2CUK-TSO-0004ITP-00063exit%2CIE-TSO-0002ITP-00495entry%2CIE-TSO-0002ITP-00495exit%2CUK-TSO-0001ITP-00090entry"
      - dataset: oxygen_content
        differs: "Oxygen in `% (mol/mol)`; Interconnector at Bacton (IUK) entry, its exit sends 0"
        request: "GET https://transparency.entsog.eu/api/v1/operationalData?limit=-1&timeZone=UCT&from=2026-09-21&to=2026-09-21&indicator=Oxygen+Content&periodType=day&pointDirection=UK-TSO-0001ITP-00005exit%2CUK-TSO-0003ITP-00005entry%2CUK-TSO-0003ITP-00005exit%2CUK-TSO-0001ITP-00207exit%2CUK-TSO-0004ITP-00063entry%2CUK-TSO-0004ITP-00063exit%2CIE-TSO-0002ITP-00495entry%2CIE-TSO-0002ITP-00495exit%2CUK-TSO-0001ITP-00090entry"
---

# ENTSOG — Gcv (`indicator=GCV`)

## Overview

Gross calorific value (GCV) of the gas at the point, in `kWh/Nm3` as sent; the response states no reference conditions. In 2026-08/09 bronze, values come from Interconnector (Bacton (IUK) entry; its exit is 0), National Gas TSO (Bacton (IUK) exit) and GNI (Moffat (IE) entry); see Known issues.

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
| Publication lag  | Not vendor-documented here. 2026-08/09 bronze: `lastUpdateDateTime` 25 h to 29 h after the gas-day start for GNI, 29 h to 52 h for Interconnector, 84 h to 133 h for National Gas TSO; `flowStatus` `Provisional` or `Confirmed`, empty on placeholders |
| Response format  | JSON |
| Indicator | `GCV` (exact-case — vendor rejects lowercase or hyphen variants) |
| Time zone | `timeZone=UCT` (ENTSOG's spelling — note the typo; not `UTC`) |
| `pointDirection` filter | `operatorKey + pointKey + directionKey` concatenated, no separator (e.g. `UK-TSO-0001ITP-00005exit`) |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `indicator` | str | Yes | Exact-case indicator name | `GCV` |
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
  "https://transparency.entsog.eu/api/v1/operationalData?from=2026-05-06&to=2026-05-06&timeZone=UCT&indicator=GCV&periodType=day&pointDirection=UK-TSO-0001ITP-00005exit&forceDownload=true&limit=1000"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsog/gcv/<year>/<month>/<day>/raw_<uuid>.json`
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
        "GCV"
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
      "id": "1GCVday2026-05-062026-05-07UK-TSO-0001ITP-00005exitkWh/Nm3",
      "dataSet": 1,
      "indicator": "GCV",
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
      "unit": "kWh/Nm3",
      "itemRemarks": null,
      "generalRemarks": null,
      "value": 11.5638,
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

**Path pattern**: `{data_root}/silver/entsog/gcv/year=YYYY/month=MM/gcv_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsog.GenericEntsogJsonTransformer (subclass GcvTransformer)`
**Pydantic schema**: `Generic — no Pydantic schema declared`
**Dedup key**: the vendor `id`, `keep="last"`, within each day's bronze read (`silver/entsog/generic.py:193-199`). The `id` concatenates indicator, period, operator, point, direction and unit, so `(timestamp_utc, operator_key, point_key, direction_key)` is unique in 2026-08/09 silver.
**Point-in-time field**: none used by the pipeline. `last_update_date_time` is the vendor's `lastUpdateDateTime` as sent, converted to UTC (`generic.py:181-183`); `ingested_at` is the silver transform time (`generic.py:201-206`).

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| timestamp_utc | datetime[UTC] | Yes | derived | `period_from` copied (`generic.py:185-187`): the gas-day start, `periodFrom` 06:00+02:00 as sent, 04:00 UTC, on every valued 2026-08/09 row; placeholders sit at 03:00 UTC |
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
| id | str | Yes | id | Dedup key (see above); placeholder ids carry a fixed 2026-2027 range, no gas-day date |
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
        "indicator": "GCV",
        "period_type": "day",
        "operator_key": "UK-TSO-0001",
        "operator_label": "National Gas TSO",
        "tso_eic_code": "21X-GB-A-A0A0A-7",
        "point_key": "ITP-00005",
        "point_label": "Bacton (IUK)",
        "direction_key": "exit",
        "unit": "kWh/Nm3",
        "value": 11.5902,
        "id": "1GCVday2026-09-212026-09-22UK-TSO-0001ITP-00005exitkWh/Nm3",
        "data_set": 1,
        "tso_item_identifier": "21Z000000000083P",
        "item_remarks": null,
        "general_remarks": null,
        "last_update_date_time": "2026-09-24T16:59:49+00:00",
        "is_unlimited": null,
        "flow_status": "Provisional",
        "interruption_type": null,
        "restoration_information": null,
        "capacity_type": null,
        "capacity_booking_status": null,
        "is_cam_relevant": false,
        "is_na": null,
        "original_period_from": null,
        "is_cmp_relevant": "false",
        "booking_platform_key": "PRISMA",
        "booking_platform_label": null,
        "booking_platform_url": "https://platform.prisma-capacity.eu/",
        "interruption_calculation_remark": null,
        "point_type": "Cross-Border Transmission IP between EU and ExtEU",
        "id_point_type": 23,
        "is_archived": false,
        "data_provider": "entsog",
        "ingested_at": "2026-09-26T17:46:32+00:00"
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
- **Requested versus returned (2026-08/09 bronze, 14 gas days)**: the connector sends nine `pointDirection` filters (`connectors/entsog/endpoints.py:24-34`); every response returns seven records. Four carry values: Interconnector's Bacton (IUK) entry and exit, National Gas TSO's Bacton (IUK) exit and GNI's Moffat (IE) entry. Three are not-applicable placeholders (`isNA` 1, `value` `""`, `periodFrom` 05:00+02:00, so 03:00 UTC): GNI Moffat (IE) exit ("Virtual Reverse Flow - No gas flows therefore no metering or gas quality analysis"), National Gas TSO Bacton (BBL) exit ("Virtual Point, currently BBL is only Unidirectional entry") and BBL company Julianadorp exit ("backhaul no measurements"). BBL company's entry and National Gas TSO's Moffat (`ITP-00090`) entry return nothing. With `limit=-1`, `meta.count` is 7 against `meta.total` 8; what `total` counts is unverified.
- **Interconnector's exit is zero**: Interconnector's Bacton (IUK) exit `value` is 0 on all 14 gas days of 2026-08/09, `Confirmed` or `Provisional`. Zero is not a gas-quality measurement; treat it as no value.
- **Two reports of Bacton (IUK)** (project check): National Gas TSO's exit and Interconnector's entry agree within 0.02 kWh/Nm3 on 13 of the 14 gas days. On 20 September 2026 Interconnector sends 14.253 (`Confirmed`, `lastUpdateDateTime` 2026-09-21 08:48 UTC) against National Gas TSO's 11.6136. Interconnector's own Wobbe index that day is 14.901, which with this GCV implies a relative density of about 0.91, against 0.62 to 0.64 on its other 13 days. The 14.253 looks wrong; ENTSOG has not confirmed it.
- **Repeated values**: 13 to 18 September 2026, National Gas TSO sends 11.6429 and Interconnector 11.645 on six consecutive gas days. Interconnector's six rows each carry their own `lastUpdateDateTime`. National Gas TSO's do not: gas days 14 and 15 September share 2026-09-18 15:54:29 UTC, and gas days 18, 19 and 20 September share 2026-09-23 17:02:50 UTC, though the value changes from the 18th (11.6429) to the 19th (11.6927) and 20th (11.6136). So National Gas TSO's `lastUpdateDateTime` reads as a batch time, not a per-value revision time. The repeats are unexplained.
- **Declared GCV units in the register differ from the row unit**: `entsog/operator_point_directions` (`tp_tso_gcv_unit`) declares `MJ/Sm3` for National Gas TSO at Bacton (IUK) exit, Bacton (BBL) exit and Moffat, `kWh/Nm3` for Interconnector and GNI, and `kWh/m3(n)` for BBL company; GNI's remark cites ISO 13443:1996. The `operationalData` rows label every GCV `kWh/Nm3`, and the two Bacton (IUK) reports agree within 0.02 on 13 of 14 days, but check the register before comparing operators' GCV in a model.
- **Two `timestamp_utc` values per gas day**: placeholders start at 03:00 UTC, valued rows at 04:00 UTC.



---

## Implementation delta

- **No documented discrepancies** for this indicator. The exact-case constant is in `OPERATIONAL_INDICATORS` (`connectors/entsog/endpoints.py:95-115`); the response echoes it in `meta.query.indicator` (`meta.fields` lists field names, not the indicator).
- **Synthetic fixture**: `tests/fixtures/entsog/physical_flows_response.json` carries placeholder `pointKey: "IUK"` and `operatorKey: "OP-IUK"`. Live data uses real keys (`ITP-00005`, `UK-TSO-0001`). Fixture regeneration is deferred (silver tests depend on the placeholder shape).

---

## Modelling notes

- Used as raw input to gas balance / interconnector flow features in `gridflow_models/`.
- Target candidates: directional flow magnitude (entry vs exit per point).
- Drop not-applicable placeholders (`is_na == 1`) and Interconnector's zero exit rows first. `flow_status` is `Provisional` on every National Gas TSO and GNI row in 2026-08/09 and mostly `Confirmed` for Interconnector, so a `Confirmed` filter keeps Interconnector only.
- Join with `operator_point_directions` to attach country, balancing zone, and CAM-relevant flags.

---

## Links

- [Official API docs (PDF)](https://transparency.entsog.eu/api/archiveDirectories/8/api-manual/TP_REG715_Documentation_TP_API%20-%20v2.1.pdf)
- `src/gridflow/connectors/entsog/endpoints.py`
- `src/gridflow/silver/entsog/generic.py`
- `src/gridflow/schemas/entsog.py`
- Gold view/builder
- [Domain: gas day](../../../20-domain/concepts/gas-day.md)
