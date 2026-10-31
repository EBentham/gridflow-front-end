---
source: entsog
dataset_key: firm_available
vendor: ENTSOG Transparency Platform
last_verified: 2026-10-24
layer_coverage: bronze, silver
page:
  title: Transmission capacity by indicator
  summary: >-
    Firm, interruptible and congestion-management capacity at the Bacton, Julianadorp and Moffat
    interconnection points, from ENTSOG's Transparency Platform, per operator, in kWh/d.
  facts:
    vendor: "ENTSOG Transparency Platform, ten capacity indicators, such as Firm Available"
    cadence: One request per gas day; each record carries its own validity period
    grain: One row per record overlapping or dated on the gas day
  landscape: gas
  what_it_is: >-
    Ten ENTSOG capacity indicators for nine operator, point and direction filters at the BBL,
    IUK and Moffat interconnections, in kWh/d. Records run from `period_from` to `period_to`; in
    firm available, one day for GNI at Moffat entry, 2018 to 2048 for BBL company's entry.
    gridflow keeps each record overlapping or dated on the gas day, stamped with that day.
  how_used:
    - Reading the firm capacity still on offer at each interconnection point, by gas day.
    - Setting firm technical, booked and available capacity side by side at one point.
    - Reading ENTSOG's statement of whether congestion management released any capacity.
  chart:
    type: line
    silver: entsog/firm_available
    time: timestamp_utc
    value: value
    filter:
      - {column: operator_key, op: in, value: [IE-TSO-0002, UK-TSO-0003]}
      - {column: point_key, op: in, value: [ITP-00495, ITP-00005]}
      - {column: direction_key, op: eq, value: entry}
      - {column: value, op: not_null}
    group: operator_key
    group_map:
      IE-TSO-0002: moffat_ie
      UK-TSO-0003: bacton_iuk
    series_order: [moffat_ie, bacton_iuk]
    aggregation: last
    window: {start: "2026-09-13", end: "2026-09-21"}
    unit: kWh/d
  chart_view:
    title: Firm available capacity at two entry points, September 2026
    caption: >-
      Silver `entsog/firm_available`, kWh/d as sent, gas days (06:00 to 06:00 Brussels time) 13 to
      21 September 2026, one row per point and day, so nothing is combined. GNI sends one-day
      records; Interconnector's one record runs 8 September to 1 October.
    alt: >-
      Line chart of firm available capacity from entsog/firm_available, in kWh/d, gas days 13 to
      21 September 2026. GNI's Moffat (IE) entry starts at 145,654,424 on the 13th, climbs to
      162,488,829 on the 14th, holds between 170,299,881 and 170,746,545 from the 15th to the 20th
      and ends at 163,891,514. Interconnector's Bacton (IUK) entry is flat at 88,226,760 on all
      nine days.
    x_label: gas day, starting 04:00 UTC
    key:
      - {series: moffat_ie, label: "Moffat (IE), GNI", codes: ITP-00495, paint: petrol, note: "Entry; GNI sends a one-day record, so the figure can change daily."}
      - {series: bacton_iuk, label: "Bacton (IUK), Interconnector", codes: ITP-00005, paint: clay, note: "Entry; one record from 8 September to 1 October, repeated each gas day."}
  raw_feed:
    note: >-
      One request per gas day and indicator to `operationalData`, with nine `pointDirection`
      filters. Silver keeps every record overlapping or dated on that day, with `value` and `unit`
      unconverted.
    requests:
      - "GET https://transparency.entsog.eu/api/v1/operationalData?limit=-1&timeZone=UCT&from=2026-09-21&to=2026-09-21&indicator=Firm+Available&periodType=day&pointDirection=UK-TSO-0001ITP-00005exit%2CUK-TSO-0003ITP-00005entry%2CUK-TSO-0003ITP-00005exit%2CUK-TSO-0001ITP-00207exit%2CUK-TSO-0004ITP-00063entry%2CUK-TSO-0004ITP-00063exit%2CIE-TSO-0002ITP-00495entry%2CIE-TSO-0002ITP-00495exit%2CUK-TSO-0001ITP-00090entry"
    commands:
      - {run: gridflow ingest entsog firm_available --start 2026-09-13 --end 2026-09-22, comment: "bronze, end exclusive; repeat per member"}
      - {run: gridflow transform entsog firm_available --start 2026-09-13 --end 2026-09-21, comment: "silver, kWh/d kept; repeat per member"}
  record:
    select:
      filter:
        - {column: timestamp_utc, op: in, value: ["2026-09-21T04:00:00"]}
        - {column: id, op: ne, value: "1Firm AvailabledayUK-TSO-0004ITP-00063exitkWh/d2015-10-302048-12-13"}
      order_by: [point_key, operator_key, direction_key]
      columns: [timestamp_utc, operator_key, point_key, direction_key, value, unit, period_from, period_to, is_na, item_remarks, last_update_date_time, id, operator_label, point_label]
    key: [timestamp_utc, id]
    caption: "Gas day 21 September 2026: every record except BBL company's Julianadorp exit (0, like its entry)."
    fields:
      timestamp_utc: "gridflow's stamp: record start, or gas-day start (06:00 Brussels) if the record began earlier"
      operator_key: ENTSOG key of the operator reporting this row
      point_key: "ENTSOG point key, such as `ITP-00495` for Moffat (IE)"
      direction_key: "`entry` or `exit`, lowercase as sent, from the reporting operator's side"
      value: "Firm available capacity in the row's `unit`, as sent; null on not-applicable rows"
      unit: "Vendor unit as sent, not converted"
      period_to: "End of the record's validity period, from `periodTo`, converted to UTC"
      is_na: "Vendor not-applicable flag: 1 on placeholder rows, null otherwise"
      item_remarks: "The operator's remark on this item, as sent; it explains the placeholders"
      last_update_date_time: "The vendor's `lastUpdateDateTime` for this row, converted to UTC"
      operator_label: Name of the operator reporting this row, as sent
      point_label: ENTSOG's name for the point, as sent
      period_from: "Start of the record's validity period, from `periodFrom`, converted to UTC"
      indicator: "The indicator requested, as sent: `Firm Available`"
      period_type: "`day`, the period type the connector requests"
      tso_eic_code: Energy Identification Code of the reporting operator, as sent
      id: "Vendor record id, the deduplication key: indicator, keys, unit and period dates joined"
      data_set: "Vendor `dataSet` code, as sent; ENTSOG's meaning for it is not documented here"
      tso_item_identifier: The reporting operator's own identifier for the point, as sent
      general_remarks: The operator's general remark, as sent; empty in these rows
      is_unlimited: "Vendor unlimited-capacity flag, kept as text: `0`, or null on placeholders"
      flow_status: "Vendor `flowStatus`, as sent; an empty string in these rows"
      interruption_type: Interruption field shared by all indicators; empty or null here
      restoration_information: Interruption restoration field shared by all indicators; empty or null here
      capacity_type: "Vendor capacity type: `Firm`, or null on placeholders"
      capacity_booking_status: Capacity booking status field, as sent; null in these rows
      is_cam_relevant: "Vendor flag for capacity allocation mechanism (CAM) relevance, as sent"
      original_period_from: "Vendor `originalPeriodFrom`, converted to UTC; set only on the placeholders here"
      is_cmp_relevant: "Vendor congestion management procedure (CMP) flag, kept as text; empty or null here"
      booking_platform_key: Capacity booking platform for the point, as sent; empty or null here
      booking_platform_label: Booking platform name, as sent; empty or null here
      booking_platform_url: Booking platform web address, as sent; empty or null here
      interruption_calculation_remark: Interruption calculation field shared by all indicators; null in these rows
      point_type: ENTSOG's type for the point, as sent; null on placeholders
      id_point_type: ENTSOG's numeric code for the point type, as sent; null on placeholders
      is_archived: Vendor archive flag; null in these rows
  notebook:
    lead: >-
      Reads `silver_entsog_firm_technical`, `_firm_booked` and `_firm_available`, lineage columns
      dropped, where `timestamp_utc` falls on the UTC dates given, ends included, then joins the
      three at GNI's Moffat entry.
    cells:
      - |
        tech = data.entsog.query("firm_technical", "2026-09-13", "2026-09-21")
        booked = data.entsog.query("firm_booked", "2026-09-13", "2026-09-21")
        avail = data.entsog.query("firm_available", "2026-09-13", "2026-09-21")
      - |
        key = ["timestamp_utc", "operator_key", "point_key", "direction_key"]
        firm = (tech[key + ["value"]].rename(columns={"value": "technical"})
                .merge(booked[key + ["value"]].rename(columns={"value": "booked"}), on=key)
                .merge(avail[key + ["value"]].rename(columns={"value": "available"}), on=key))
        moffat = firm[(firm.point_key == "ITP-00495") & (firm.direction_key == "entry")]
        moffat = moffat.sort_values("timestamp_utc").assign(
            timestamp_utc=lambda d: d.timestamp_utc.dt.tz_convert("UTC"))
        moffat[["timestamp_utc", "technical", "booked", "available"]]
      - |
        moffat.plot(x="timestamp_utc", y=["technical", "booked", "available"],
                    style=["--", "-", "-"], color=["#66793B", "#C77E3C", "#155A6E"],
                    ylabel="kWh/d", figsize=(8, 3.5))
    needs: gas days 13 to 21 September 2026, firm technical, booked and available
    plot_alt: >-
      Line plot of GNI's Moffat entry in kWh/d for gas days 13 to 21 September 2026. Technical
      is flat at 433,368,000. Booked falls from 287,713,576 on the 13th to between 262,621,455
      and 263,068,119 from the 15th to the 20th, ending at 269,476,486; available moves the other
      way, from 145,654,424 up to 170,746,545, ending at 163,891,514.
  related:
    - {dataset: entsog/physical_flows, note: "Physical flow at the same points, against the capacity shown here"}
    - {dataset: entsog/nominations, note: "Nominated quantities at the same points, requested with the same filters"}
    - {dataset: entsog/cmp_unavailable_firm_capacity, note: Firm capacity declared unavailable under congestion management}
    - {dataset: entsog/operator_point_directions, note: "The register of the operator, point and direction keys used here"}
  family:
    slug: capacity-by-indicator
    members:
      - dataset: firm_available
        differs: "Firm capacity still available; GNI sends one-day records at Moffat (IE) entry"
        request: "GET https://transparency.entsog.eu/api/v1/operationalData?limit=-1&timeZone=UCT&from=2026-09-21&to=2026-09-21&indicator=Firm+Available&periodType=day&pointDirection=UK-TSO-0001ITP-00005exit%2CUK-TSO-0003ITP-00005entry%2CUK-TSO-0003ITP-00005exit%2CUK-TSO-0001ITP-00207exit%2CUK-TSO-0004ITP-00063entry%2CUK-TSO-0004ITP-00063exit%2CIE-TSO-0002ITP-00495entry%2CIE-TSO-0002ITP-00495exit%2CUK-TSO-0001ITP-00090entry"
      - dataset: firm_booked
        differs: "Firm capacity booked; GNI also sends one-day records at Moffat (IE) entry"
        request: "GET https://transparency.entsog.eu/api/v1/operationalData?limit=-1&timeZone=UCT&from=2026-09-21&to=2026-09-21&indicator=Firm+Booked&periodType=day&pointDirection=UK-TSO-0001ITP-00005exit%2CUK-TSO-0003ITP-00005entry%2CUK-TSO-0003ITP-00005exit%2CUK-TSO-0001ITP-00207exit%2CUK-TSO-0004ITP-00063entry%2CUK-TSO-0004ITP-00063exit%2CIE-TSO-0002ITP-00495entry%2CIE-TSO-0002ITP-00495exit%2CUK-TSO-0001ITP-00090entry"
      - dataset: firm_technical
        differs: "Firm technical capacity; long records, such as GNI's Moffat (IE) entry, 2026 to 2036"
        request: "GET https://transparency.entsog.eu/api/v1/operationalData?limit=-1&timeZone=UCT&from=2026-09-21&to=2026-09-21&indicator=Firm+Technical&periodType=day&pointDirection=UK-TSO-0001ITP-00005exit%2CUK-TSO-0003ITP-00005entry%2CUK-TSO-0003ITP-00005exit%2CUK-TSO-0001ITP-00207exit%2CUK-TSO-0004ITP-00063entry%2CUK-TSO-0004ITP-00063exit%2CIE-TSO-0002ITP-00495entry%2CIE-TSO-0002ITP-00495exit%2CUK-TSO-0001ITP-00090entry"
      - dataset: interruptible_available
        differs: "Interruptible capacity still available; GNI marks Moffat (IE) entry 'Firm Only', with no value"
        request: "GET https://transparency.entsog.eu/api/v1/operationalData?limit=-1&timeZone=UCT&from=2026-09-21&to=2026-09-21&indicator=Interruptible+Available&periodType=day&pointDirection=UK-TSO-0001ITP-00005exit%2CUK-TSO-0003ITP-00005entry%2CUK-TSO-0003ITP-00005exit%2CUK-TSO-0001ITP-00207exit%2CUK-TSO-0004ITP-00063entry%2CUK-TSO-0004ITP-00063exit%2CIE-TSO-0002ITP-00495entry%2CIE-TSO-0002ITP-00495exit%2CUK-TSO-0001ITP-00090entry"
      - dataset: interruptible_booked
        differs: "Interruptible capacity booked; GNI marks Moffat (IE) entry 'Firm Only', with no value"
        request: "GET https://transparency.entsog.eu/api/v1/operationalData?limit=-1&timeZone=UCT&from=2026-09-21&to=2026-09-21&indicator=Interruptible+Booked&periodType=day&pointDirection=UK-TSO-0001ITP-00005exit%2CUK-TSO-0003ITP-00005entry%2CUK-TSO-0003ITP-00005exit%2CUK-TSO-0001ITP-00207exit%2CUK-TSO-0004ITP-00063entry%2CUK-TSO-0004ITP-00063exit%2CIE-TSO-0002ITP-00495entry%2CIE-TSO-0002ITP-00495exit%2CUK-TSO-0001ITP-00090entry"
      - dataset: interruptible_total
        differs: "Interruptible total, as ENTSOG names it; GNI marks Moffat (IE) entry 'Firm Only'"
        request: "GET https://transparency.entsog.eu/api/v1/operationalData?limit=-1&timeZone=UCT&from=2026-09-21&to=2026-09-21&indicator=Interruptible+Total&periodType=day&pointDirection=UK-TSO-0001ITP-00005exit%2CUK-TSO-0003ITP-00005entry%2CUK-TSO-0003ITP-00005exit%2CUK-TSO-0001ITP-00207exit%2CUK-TSO-0004ITP-00063entry%2CUK-TSO-0004ITP-00063exit%2CIE-TSO-0002ITP-00495entry%2CIE-TSO-0002ITP-00495exit%2CUK-TSO-0001ITP-00090entry"
      - dataset: available_through_oversubscription
        differs: "Oversubscription; 1 to 5 August 2026: annual Bacton (IUK) records, 'no capacity' rows"
        caveat: "ENTSOG sends National Gas TSO's Bacton (IUK) exit 472 kWh/d and a same-day 'no capacity' sentence."
        request: "GET https://transparency.entsog.eu/api/v1/operationalData?limit=-1&timeZone=UCT&from=2026-08-05&to=2026-08-05&indicator=Available+through+Oversubscription&periodType=day&pointDirection=UK-TSO-0001ITP-00005exit%2CUK-TSO-0003ITP-00005entry%2CUK-TSO-0003ITP-00005exit%2CUK-TSO-0001ITP-00207exit%2CUK-TSO-0004ITP-00063entry%2CUK-TSO-0004ITP-00063exit%2CIE-TSO-0002ITP-00495entry%2CIE-TSO-0002ITP-00495exit%2CUK-TSO-0001ITP-00090entry"
      - dataset: available_through_surrender
        differs: "Surrender; 1 to 5 August 2026: annual Bacton (IUK) records, 'no capacity' rows"
        caveat: "ENTSOG sends National Gas TSO's Bacton (IUK) exit 472 kWh/d and a same-day 'no capacity' sentence."
        request: "GET https://transparency.entsog.eu/api/v1/operationalData?limit=-1&timeZone=UCT&from=2026-08-05&to=2026-08-05&indicator=Available+through+Surrender&periodType=day&pointDirection=UK-TSO-0001ITP-00005exit%2CUK-TSO-0003ITP-00005entry%2CUK-TSO-0003ITP-00005exit%2CUK-TSO-0001ITP-00207exit%2CUK-TSO-0004ITP-00063entry%2CUK-TSO-0004ITP-00063exit%2CIE-TSO-0002ITP-00495entry%2CIE-TSO-0002ITP-00495exit%2CUK-TSO-0001ITP-00090entry"
      - dataset: available_through_uioli_long_term
        differs: "Long-term use-it-or-lose-it; 1 to 5 August 2026: annual Bacton (IUK) records, 'no capacity' rows"
        caveat: "ENTSOG sends National Gas TSO's Bacton (IUK) exit 472 kWh/d and a same-day 'no capacity' sentence."
        request: "GET https://transparency.entsog.eu/api/v1/operationalData?limit=-1&timeZone=UCT&from=2026-08-05&to=2026-08-05&indicator=Available+through+UIOLI+long-term&periodType=day&pointDirection=UK-TSO-0001ITP-00005exit%2CUK-TSO-0003ITP-00005entry%2CUK-TSO-0003ITP-00005exit%2CUK-TSO-0001ITP-00207exit%2CUK-TSO-0004ITP-00063entry%2CUK-TSO-0004ITP-00063exit%2CIE-TSO-0002ITP-00495entry%2CIE-TSO-0002ITP-00495exit%2CUK-TSO-0001ITP-00090entry"
      - dataset: available_through_uioli_short_term
        differs: "Short-term use-it-or-lose-it; 1 to 5 August 2026 hold only ENTSOG's 'no capacity' rows"
        request: "GET https://transparency.entsog.eu/api/v1/operationalData?limit=-1&timeZone=UCT&from=2026-08-05&to=2026-08-05&indicator=Available+through+UIOLI+short-term&periodType=day&pointDirection=UK-TSO-0001ITP-00005exit%2CUK-TSO-0003ITP-00005entry%2CUK-TSO-0003ITP-00005exit%2CUK-TSO-0001ITP-00207exit%2CUK-TSO-0004ITP-00063entry%2CUK-TSO-0004ITP-00063exit%2CIE-TSO-0002ITP-00495entry%2CIE-TSO-0002ITP-00495exit%2CUK-TSO-0001ITP-00090entry"
---

# ENTSOG — Firm Available (`indicator=Firm Available`)

## Overview

Firm capacity remaining available for booking (offered to market, not yet booked). In 2026-08/09 bronze, `value` equals Firm Technical minus Firm Booked on every valued point and gas day (a project check; ENTSOG's definition is not quoted here).

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
| Indicator | `Firm Available` (exact-case — vendor rejects lowercase or hyphen variants) |
| Time zone | `timeZone=UCT` (ENTSOG's spelling — note the typo; not `UTC`) |
| `pointDirection` filter | `operatorKey + pointKey + directionKey` concatenated, no separator (e.g. `UK-TSO-0001ITP-00005exit`) |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `indicator` | str | Yes | Exact-case indicator name | `Firm Available` |
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
  "https://transparency.entsog.eu/api/v1/operationalData?from=2026-05-06&to=2026-05-06&timeZone=UCT&indicator=Firm%20Available&periodType=day&pointDirection=UK-TSO-0001ITP-00005exit&forceDownload=true&limit=1000"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsog/firm_available/<year>/<month>/<day>/raw_<uuid>.json`
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
        "Firm Available"
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
      "id": "1Firm AvailabledayUK-TSO-0001ITP-00005exitkWh/d2022-01-012028-05-01",
      "dataSet": 1,
      "indicator": "Firm Available",
      "periodType": "day",
      "periodFrom": "2022-01-01T06:00:00+01:00",
      "periodTo": "2028-05-01T06:00:00+02:00",
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
      "value": 518112451,
      "lastUpdateDateTime": "2026-05-01T02:11:58+02:00",
      "isUnlimited": "0",
      "flowStatus": "",
      "interruptionType": "",
      "restorationInformation": "",
      "capacityType": "Firm",
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

**Path pattern**: `{data_root}/silver/entsog/firm_available/year=YYYY/month=MM/firm_available_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsog.GenericEntsogJsonTransformer (subclass FirmAvailableTransformer)`
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
| capacity_booking_status | str | Yes | capacityBookingStatus | Null dtype in partitions where the day's rows are all null (dtype drift) |
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
        "period_from": "2022-01-01T05:00:00+00:00",
        "period_to": "2028-09-01T04:00:00+00:00",
        "indicator": "Firm Available",
        "period_type": "day",
        "operator_key": "UK-TSO-0001",
        "operator_label": "National Gas TSO",
        "tso_eic_code": "21X-GB-A-A0A0A-7",
        "point_key": "ITP-00005",
        "point_label": "Bacton (IUK)",
        "direction_key": "exit",
        "unit": "kWh/d",
        "value": 518112451.0,
        "id": "1Firm AvailabledayUK-TSO-0001ITP-00005exitkWh/d2022-01-012028-09-01",
        "data_set": 1,
        "tso_item_identifier": "21Z000000000083P",
        "item_remarks": "",
        "general_remarks": "",
        "last_update_date_time": "2026-08-31T23:53:55+00:00",
        "is_unlimited": "0",
        "flow_status": "",
        "interruption_type": "",
        "restoration_information": "",
        "capacity_type": "Firm",
        "capacity_booking_status": null,
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
        "is_archived": null,
        "data_provider": "entsog",
        "ingested_at": "2026-10-24T13:55:58.231613+00:00"
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
- **Validity records, one row per gas day**: capacity records are validity periods (in 2026-08/09 bronze, from one day to 2015-2048). The generic transformer keeps every record whose `periodFrom`/`periodTo` window overlaps the bronze day's gas day (06:00 to 06:00 Europe/Brussels), plus any dated that day or undated, for the capacity and CMP datasets in `_VALIDITY_WINDOW_DATASETS` (`silver/entsog/generic.py:174-187`, :353-369; `datetime.py:110-153`; gridflow PR #129, branch `fix/entsog-capacity-cmp`). It stamps each kept record with that gas day (`datetime.py:156-180`): `timestamp_utc` is the record's own start if inside the gas day, else the gas-day start. A record valid over many days therefore appears once per fetched gas day; do not sum rows across days. 2026-08/09: 126 bronze records (84 with a value), 126 silver rows.
- **Not-applicable placeholders**: National Gas TSO `ITP-00090` entry and `ITP-00207` exit, and GNI `ITP-00495` exit send one record a day with `isNA` 1, `value` "" (null in silver), `periodFrom` 05:00+02:00 (03:00 UTC, an hour before the gas day starts, so silver stamps them at the gas-day start, 04:00 UTC), an `id` ending `_NA<n>` with a fixed 2026-2027 range that recurs every day, and the remarks "Virtual Point, currently Moffat is only Unidirectional exit", "Virtual Point, currently BBL is only Unidirectional entry", "Not currently systemised in TSO System".
- **Requested versus returned (2026-08/09 bronze)**: all nine `pointDirection` filters return one record each; `meta.count` equals `meta.total` (9) in every response. Unlike nominations, BBL company's `ITP-00063` filters return values here.
- **Partition dtype drift**: a column whose rows are all null in one day's response is written with Null dtype in that partition and String in others (`generic.py` coerces no dtypes). In 2026-08/09 silver: `capacity_booking_status` (see the schema table). `pl.read_parquet` over the table glob then fails; read per file and concatenate with `how="diagonal_relaxed"`.



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
