---
source: entsog
dataset_key: nominations
vendor: ENTSOG Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Nominations, renominations and allocations
  summary: >-
    Daily gas nominations, renominations and allocations at the Bacton and Moffat interconnection
    points, from ENTSOG's Transparency Platform, per reporting operator, in kWh/d.
  facts:
    vendor: "ENTSOG Transparency Platform, indicators Nomination, Renomination and Allocation"
    cadence: Daily, one value per gas day
    grain: One row per gas day, operator, point and direction
  landscape: gas
  what_it_is: >-
    Three ENTSOG indicators for the nine operator, point and direction filters gridflow sends for
    the BBL, IUK and Moffat interconnections; BBL company's two return no rows. GNI's remark calls
    its figure the latest aggregate nomination or renomination available when published. Values
    stay in kWh/d. Each operator reports its own side of a point, and the two sides can differ.
  how_used:
    - Comparing the nominated quantity at Moffat or Bacton with its later renomination.
    - Checking allocations against physical flow at the same point and gas day.
    - Reading both operators' reports of one point, such as Bacton (IUK).
  chart:
    type: line
    silver: entsog/nominations
    time: timestamp_utc
    value: value
    filter:
      - {column: operator_key, op: in, value: [UK-TSO-0001, IE-TSO-0002]}
      - {column: point_key, op: in, value: [ITP-00495, ITP-00207, ITP-00005]}
      - {column: value, op: not_null}
    group: point_key
    group_map:
      ITP-00495: moffat_ie
      ITP-00207: bacton_bbl
      ITP-00005: bacton_iuk
    series_order: [moffat_ie, bacton_bbl, bacton_iuk]
    aggregation: last
    window: {start: "2026-09-13", end: "2026-09-21"}
    unit: kWh/d
  chart_view:
    title: GB interconnection nominations, 13 to 21 September 2026
    caption: >-
      Silver `entsog/nominations` only, kWh/d as sent, gas days 13 to 21 September 2026, one row
      per point and day. Moffat is GNI's entry report; both Bacton lines are National Gas TSO's
      exit reports. A gap is a null value.
    alt: >-
      Line chart of daily gas nominations from entsog/nominations, in kWh/d, for gas days 13 to 21
      September 2026. GNI's Moffat (IE) entry moves between 45,664,771 on the 19th and 95,147,913
      on the 15th, ending at 90,763,437. National Gas TSO's Bacton (BBL) exit falls from
      100,104,000 on the 14th to 12,000,000 on the 19th, rises to 91,224,000 on the 20th and reads
      77,088,000 on the 21st. Its
      Bacton (IUK) exit is zero, with no value on the 17th, then 91,153,956 on the 21st.
    x_label: gas day, starting 04:00 UTC
    key:
      - {series: moffat_ie, label: "Moffat (IE) entry", codes: ITP-00495, paint: petrol, note: "GNI's report; gridflow asks National Gas TSO only for Moffat entry, null here."}
      - {series: bacton_bbl, label: "Bacton (BBL) exit", codes: ITP-00207, paint: olive, note: "BBL company is asked for Julianadorp, not Bacton, and returns no rows here."}
      - {series: bacton_iuk, label: "Bacton (IUK) exit", codes: ITP-00005, paint: horizon, note: "Zero, null on the 17th, then 91,153,956; Interconnector's own entry report for the 21st is 112,753,956."}
  raw_feed:
    note: >-
      One request per day and indicator to `operationalData`, with nine operator, point and
      direction filters. The response's `meta.total` can exceed the records returned, unexplained.
      Silver keeps `value` and `unit` unconverted.
    requests:
      - "GET https://transparency.entsog.eu/api/v1/operationalData?limit=-1&timeZone=UCT&from=2026-09-21&to=2026-09-21&indicator=Nomination&periodType=day&pointDirection=UK-TSO-0001ITP-00005exit%2CUK-TSO-0003ITP-00005entry%2CUK-TSO-0003ITP-00005exit%2CUK-TSO-0001ITP-00207exit%2CUK-TSO-0004ITP-00063entry%2CUK-TSO-0004ITP-00063exit%2CIE-TSO-0002ITP-00495entry%2CIE-TSO-0002ITP-00495exit%2CUK-TSO-0001ITP-00090entry"
    commands:
      - {run: gridflow ingest entsog nominations --start 2026-09-13 --end 2026-09-22, comment: "bronze, end exclusive; repeat per member"}
      - {run: gridflow transform entsog nominations --start 2026-09-13 --end 2026-09-21, comment: "silver, kWh/d kept; repeat per member"}
  record:
    select:
      filter:
        - {column: timestamp_utc, op: in, value: ["2026-09-20T04:00:00", "2026-09-21T04:00:00"]}
        - {column: point_key, op: in, value: [ITP-00005, ITP-00207]}
      order_by: [timestamp_utc, point_key, operator_key, direction_key]
      columns: [timestamp_utc, operator_key, point_key, direction_key, value, unit, last_update_date_time, operator_label, point_label]
    key: [timestamp_utc, operator_key, point_key, direction_key]
    caption: "Gas days 20 and 21 September 2026 at the two Bacton points, both operators' reports."
    fields:
      timestamp_utc: "Start of the gas day, from the vendor `periodFrom`, in UTC"
      operator_key: ENTSOG key of the operator reporting this row
      point_key: "ENTSOG point key, such as `ITP-00005` for Bacton (IUK)"
      direction_key: "`entry` or `exit`, lowercase as sent, from the reporting operator's side"
      value: "Nominated quantity in the row's `unit`, as sent; null when none is sent"
      unit: "Vendor unit as sent, not converted"
      last_update_date_time: "The vendor's `lastUpdateDateTime` for this row, converted to UTC"
      operator_label: Name of the operator reporting this row, as sent
      point_label: ENTSOG's name for the point, as sent
      period_from: "Gas-day start as sent in `periodFrom`, converted to UTC"
      period_to: "Gas-day end as sent in `periodTo`, converted to UTC"
      indicator: "The indicator requested, as sent: `Nomination`"
      period_type: "`day`, the period type the connector requests"
      tso_eic_code: Energy Identification Code of the reporting operator, as sent
      id: "Vendor record id, the deduplication key: indicator, dates, keys and unit joined"
      data_set: "Vendor `dataSet` code, as sent; ENTSOG's meaning for it is not documented here"
      tso_item_identifier: The reporting operator's own identifier for the point, as sent
      item_remarks: The operator's remark on this item, as sent; null when none
      general_remarks: The operator's general remark, as sent; null in these rows
      is_unlimited: Capacity flag shared by all indicators; null in these rows
      flow_status: "Vendor `flowStatus`, as sent; an empty string in these rows"
      interruption_type: Interruption field shared by all indicators; null in these rows
      restoration_information: Interruption restoration field shared by all indicators; null in these rows
      capacity_type: Capacity field shared by all indicators; null in these rows
      capacity_booking_status: Capacity booking field shared by all indicators; null in these rows
      is_cam_relevant: "Vendor flag for capacity allocation mechanism (CAM) relevance, as sent"
      is_na: Vendor not-applicable flag; null in these rows
      original_period_from: "Vendor `originalPeriodFrom`, converted to UTC; null in these rows"
      is_cmp_relevant: "Vendor flag for congestion management procedure (CMP) relevance, as sent"
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
      `timestamp_utc` falls on the UTC dates given, ends included, then joins the three stages at
      GNI's Moffat entry.
    cells:
      - |
        nom = data.entsog.query("nominations", "2026-09-13", "2026-09-21")
        ren = data.entsog.query("renominations", "2026-09-13", "2026-09-21")
        alloc = data.entsog.query("allocations", "2026-09-13", "2026-09-21")
      - |
        key = ["timestamp_utc", "operator_key", "point_key", "direction_key"]
        stages = (nom[key + ["value"]].rename(columns={"value": "nominated"})
                  .merge(ren[key + ["value"]].rename(columns={"value": "renominated"}), on=key)
                  .merge(alloc[key + ["value"]].rename(columns={"value": "allocated"}), on=key))
        moffat = stages[(stages.point_key == "ITP-00495") & (stages.direction_key == "entry")]
        moffat = moffat.sort_values("timestamp_utc").assign(
            timestamp_utc=lambda d: d.timestamp_utc.dt.tz_convert("UTC"))
        moffat[["timestamp_utc", "nominated", "renominated", "allocated"]]
      - |
        moffat.plot(x="timestamp_utc", y=["nominated", "renominated", "allocated"],
                    style=["-", "-", "--"], color=["#C77E3C", "#155A6E", "#66793B"],
                    ylabel="kWh/d", figsize=(8, 3.5))
    needs: gas days 13 to 21 September 2026, all three members
    plot_alt: >-
      Line plot of GNI's Moffat entry in kWh/d for gas days 13 to 21 September 2026. The
      renominated and allocated lines lie on each other, from 180,146,144 on the 13th down to
      131,501,901 on the 19th and back to 180,105,551. The nominated line runs lower, between
      45,664,771 and 95,147,913.
  related:
    - {dataset: entsog/physical_flows, note: "Physical flow at the same points, from the same endpoint"}
    - {dataset: entsog/firm_booked, note: "Firm capacity booked, requested with the same nine filters"}
    - {dataset: entsog/aggregated_physical_flows, note: "ENTSOG's British-zone entry totals from production, storage and LNG only"}
    - {dataset: entsog/operator_point_directions, note: "The register of the operator, point and direction keys used here"}
  family:
    slug: nominations-allocations
    members:
      - dataset: nominations
        differs: "Nominated quantity; GNI calls it the latest aggregate nomination when published"
        request: "GET https://transparency.entsog.eu/api/v1/operationalData?limit=-1&timeZone=UCT&from=2026-09-21&to=2026-09-21&indicator=Nomination&periodType=day&pointDirection=UK-TSO-0001ITP-00005exit%2CUK-TSO-0003ITP-00005entry%2CUK-TSO-0003ITP-00005exit%2CUK-TSO-0001ITP-00207exit%2CUK-TSO-0004ITP-00063entry%2CUK-TSO-0004ITP-00063exit%2CIE-TSO-0002ITP-00495entry%2CIE-TSO-0002ITP-00495exit%2CUK-TSO-0001ITP-00090entry"
      - dataset: renominations
        differs: "Renominated quantity; GNI calls it the latest aggregate renomination when published"
        request: "GET https://transparency.entsog.eu/api/v1/operationalData?limit=-1&timeZone=UCT&from=2026-09-21&to=2026-09-21&indicator=Renomination&periodType=day&pointDirection=UK-TSO-0001ITP-00005exit%2CUK-TSO-0003ITP-00005entry%2CUK-TSO-0003ITP-00005exit%2CUK-TSO-0001ITP-00207exit%2CUK-TSO-0004ITP-00063entry%2CUK-TSO-0004ITP-00063exit%2CIE-TSO-0002ITP-00495entry%2CIE-TSO-0002ITP-00495exit%2CUK-TSO-0001ITP-00090entry"
      - dataset: allocations
        differs: "Allocated quantity, flow status; National Gas TSO sends only not-applicable placeholders at 03:00 UTC"
        request: "GET https://transparency.entsog.eu/api/v1/operationalData?limit=-1&timeZone=UCT&from=2026-09-21&to=2026-09-21&indicator=Allocation&periodType=day&pointDirection=UK-TSO-0001ITP-00005exit%2CUK-TSO-0003ITP-00005entry%2CUK-TSO-0003ITP-00005exit%2CUK-TSO-0001ITP-00207exit%2CUK-TSO-0004ITP-00063entry%2CUK-TSO-0004ITP-00063exit%2CIE-TSO-0002ITP-00495entry%2CIE-TSO-0002ITP-00495exit%2CUK-TSO-0001ITP-00090entry"
---

# ENTSOG — Nominations (`indicator=Nomination`)

## Overview

Nominated gas quantities in kWh/d per operator, point, direction and gas day (quantities, not capacity). GNI's `itemRemarks` reads "Latest Aggregate Transporter Nomination available at the time of publishing"; the other operators send none. Not strictly day-ahead in what the platform keeps: in 2026-08/09 bronze, `lastUpdateDateTime` runs from 14 h before the gas-day start (GNI) to 34 h after it (Interconnector), and National Gas TSO's falls inside the gas day.

The dataset is one of 19 indicators served by the same `/operationalData`
endpoint. The (operator, point, direction) tuple selects which physical
location to read; the `indicator` query parameter selects which series
(physical flow, nomination, allocation, etc.) is returned. Records carry
the daily `periodFrom` / `periodTo` window and a `value` in `kWh/d` (or
indicator-specific units for content/quality series).

→ Related concepts:
  [Gas day](../../../20-domain/concepts/gas-day.md)
  [Allocations](allocations.md)

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
| Publication lag  | Not vendor-documented here. 2026-08/09 bronze: `lastUpdateDateTime` from 14 h before to 34 h after the gas-day start; `flowStatus` is an empty string |
| Response format  | JSON |
| Indicator | `Nomination` (exact-case — vendor rejects lowercase or hyphen variants) |
| Time zone | `timeZone=UCT` (ENTSOG's spelling — note the typo; not `UTC`) |
| `pointDirection` filter | `operatorKey + pointKey + directionKey` concatenated, no separator (e.g. `UK-TSO-0001ITP-00005exit`) |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `indicator` | str | Yes | Exact-case indicator name | `Nomination` |
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
  "https://transparency.entsog.eu/api/v1/operationalData?from=2026-05-06&to=2026-05-06&timeZone=UCT&indicator=Nomination&periodType=day&pointDirection=UK-TSO-0001ITP-00005exit&forceDownload=true&limit=1000"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsog/nominations/<year>/<month>/<day>/raw_<uuid>.json`
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
        "Nomination"
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
      "id": "1Nominationday2026-05-062026-05-07UK-TSO-0001ITP-00005exitkWh/d",
      "dataSet": 1,
      "indicator": "Nomination",
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
      "value": 15282000,
      "lastUpdateDateTime": "2026-05-06T18:02:09+02:00",
      "isUnlimited": null,
      "flowStatus": "",
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

**Path pattern**: `{data_root}/silver/entsog/nominations/year=YYYY/month=MM/nominations_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsog.GenericEntsogJsonTransformer (subclass NominationsTransformer)`
**Pydantic schema**: `Generic — no Pydantic schema declared`
**Dedup key**: the vendor `id`, `keep="last"`, within each day's bronze read (`silver/entsog/generic.py:193-199`). The `id` concatenates indicator, period, operator, point, direction and unit, so `(timestamp_utc, operator_key, point_key, direction_key)` is unique in 2026-08/09 silver (14 gas days x 7 rows).
**Point-in-time field**: none used by the pipeline. `last_update_date_time` is the vendor's `lastUpdateDateTime` as sent, converted to UTC (`generic.py:181-183`); `ingested_at` is the silver transform time (`generic.py:201-206`).

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| timestamp_utc | datetime[UTC] | Yes | derived | `period_from` copied (`generic.py:185-187`): the gas-day start, `periodFrom` 06:00+02:00 as sent, 04:00 UTC, on every valued 2026-08/09 row |
| id | str | Yes | id | Dedup key (see above) |
| data_set | Int64 | Yes | dataSet |  |
| indicator | str | Yes | indicator |  |
| period_type | str | Yes | periodType |  |
| period_from | datetime[UTC] | Yes | periodFrom |  |
| period_to | datetime[UTC] | Yes | periodTo |  |
| operator_key | str | Yes | operatorKey |  |
| tso_eic_code | str | Yes | tsoEicCode |  |
| operator_label | str | Yes | operatorLabel |  |
| point_key | str | Yes | pointKey |  |
| point_label | str | Yes | pointLabel |  |
| tso_item_identifier | str | Yes | tsoItemIdentifier |  |
| direction_key | str | Yes | directionKey |  |
| unit | str | Yes | unit | As sent, not converted; `kWh/d` on every 2026-08/09 row |
| item_remarks | str | Yes | itemRemarks |  |
| general_remarks | str | Yes | generalRemarks |  |
| value | float | Yes | value | In the row's `unit`, not converted; sent as null or `""`, it is null (Float64 cast with `strict=False`, `generic.py:189-191`) |
| last_update_date_time | datetime[UTC] | Yes | lastUpdateDateTime |  |
| is_unlimited | bool | Yes | isUnlimited |  |
| flow_status | str | Yes | flowStatus |  |
| interruption_type | str | Yes | interruptionType |  |
| restoration_information | str | Yes | restorationInformation |  |
| capacity_type | str | Yes | capacityType |  |
| capacity_booking_status | str | Yes | capacityBookingStatus |  |
| is_cam_relevant | bool | Yes | isCamRelevant |  |
| is_na | null | Yes | isNA | Null dtype: sent as null on every row |
| original_period_from | datetime[UTC] | Yes | originalPeriodFrom |  |
| is_cmp_relevant | bool | Yes | isCmpRelevant |  |
| booking_platform_key | str | Yes | bookingPlatformKey |  |
| booking_platform_label | str | Yes | bookingPlatformLabel |  |
| booking_platform_url | str | Yes | bookingPlatformURL |  |
| interruption_calculation_remark | str | Yes | interruptionCalculationRemark |  |
| point_type | str | Yes | pointType |  |
| id_point_type | Int64 | Yes | idPointType |  |
| is_archived | bool | Yes | isArchived |  |
| data_provider | str | No | derived | Always `entsog` |
| ingested_at | datetime[UTC] | No | derived | Wall-clock at silver write |

### Silver sample

```python
[
    {
        "id": "1Nominationday2026-05-062026-05-07UK-TSO-0001ITP-00005exitkWh/d",
        "data_set": 1,
        "indicator": "Nomination",
        "period_type": "day",
        "period_from": "2026-05-06T04:00:00+00:00",
        "period_to": "2026-05-07T04:00:00+00:00",
        "operator_key": "UK-TSO-0001",
        "tso_eic_code": "21X-GB-A-A0A0A-7",
        "operator_label": "National Gas TSO",
        "point_key": "ITP-00005",
        "point_label": "Bacton (IUK)",
        "tso_item_identifier": "21Z000000000083P",
        "direction_key": "exit",
        "unit": "kWh/d",
        "item_remarks": null,
        "general_remarks": null,
        "value": 15282000,
        "last_update_date_time": "2026-05-06T16:02:09+00:00",
        "is_unlimited": null,
        "flow_status": "",
        "interruption_type": null,
        "restoration_information": null,
        "capacity_type": null,
        "capacity_booking_status": null,
        "is_cam_relevant": false,
        "is_na": null,
        "original_period_from": null,
        "is_cmp_relevant": false,
        "booking_platform_key": "PRISMA",
        "booking_platform_label": null,
        "booking_platform_url": "https://platform.prisma-capacity.eu/",
        "interruption_calculation_remark": null,
        "point_type": "Cross-Border Transmission IP between EU and ExtEU",
        "id_point_type": 23,
        "is_archived": false,
        "data_provider": "entsog",
        "ingested_at": "2026-05-08T18:00:00+00:00"
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
- **Requested versus returned (2026-08/09 bronze, 14 gas days)**: the connector sends nine `pointDirection` filters (`connectors/entsog/endpoints.py:24-34`); every response returns seven rows. The two BBL company filters (`UK-TSO-0004ITP-00063entry`/`exit`, Julianadorp/Balgzand) return nothing. With `limit=-1`, `meta.count` is 7 against `meta.total` 14; what `total` counts is unverified.
- **Moffat**: National Gas TSO is asked only for `UK-TSO-0001ITP-00090entry` (its allocation remark: "Virtual Point, currently Moffat is only Unidirectional exit"); its nomination value is null on every 2026-08/09 row, as is GNI's `ITP-00495` exit. The Moffat flow appears here only as GNI's `ITP-00495` entry.



---

## Implementation delta

- **No documented discrepancies** for this indicator. Live API returns the indicator name in `meta.fields` matching the code's exact-case constant in `OPERATIONAL_INDICATORS`.
- **Synthetic fixture**: `tests/fixtures/entsog/physical_flows_response.json` carries placeholder `pointKey: "IUK"` and `operatorKey: "OP-IUK"`. Live data uses real keys (`ITP-00005`, `UK-TSO-0001`). Fixture regeneration is deferred (silver tests depend on the placeholder shape).

---

## Modelling notes

- Used as raw input to gas balance / interconnector flow features in `gridflow_models/`.
- Target candidates: directional flow magnitude (entry vs exit per point).
- `flow_status` is an empty string on every 2026-08/09 row of this indicator, so the `Confirmed`/`Provisional` filter used for flows and allocations does not apply.
- Join with `operator_point_directions` to attach country, balancing zone, and CAM-relevant flags.

---

## Links

- [Official API docs (PDF)](https://transparency.entsog.eu/api/archiveDirectories/8/api-manual/TP_REG715_Documentation_TP_API%20-%20v2.1.pdf)
- `src/gridflow/connectors/entsog/endpoints.py`
- `src/gridflow/silver/entsog/generic.py`
- `src/gridflow/schemas/entsog.py`
- Gold view/builder
- [Domain: gas day](../../../20-domain/concepts/gas-day.md)
