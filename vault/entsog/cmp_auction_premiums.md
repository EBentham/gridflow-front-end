---
source: entsog
dataset_key: cmp_auction_premiums
vendor: ENTSOG Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Congestion management procedures (CMP)
  summary: >-
    ENTSOG's congestion-management records per operator, point and direction: auction premiums,
    unavailable firm capacity and unsuccessful capacity requests, across Europe.
  facts:
    vendor: "ENTSOG Transparency Platform, endpoints `cmpAuctions`, `cmpUnavailables` and `cmpUnsuccessfulRequests`"
    cadence: One request per day; a record repeats on each gas day it covers
    grain: One row per vendor record id and gas day
  landscape: gas
  what_it_is: >-
    Three tables from transmission operators, per point and direction: auction results with premium,
    cleared and reserve price; periods of unavailable firm capacity; and firm capacity requests not
    fully allocated. ENTSOG also sends statement rows, such as "Currently there are no firm capacity
    products on this point". A point can carry both: a statement of no premium beside results with
    one.
  how_used:
    - Finding interconnection points where an auction premium was sent for firm capacity.
    - "Sizing unmet firm demand at a point: requested against allocated volume."
    - Listing the points and periods where operators report firm capacity unavailable.
  chart:
    type: none
    reason: Premiums come in six units with an unconfirmed basis, so the rows below show them as sent.
  raw_feed:
    note: >-
      One request per day to each endpoint, with no point filter. Silver keeps every record whose
      period overlaps that gas day, plus ENTSOG's statement rows, stamped on the day.
    requests:
      - "GET https://transparency.entsog.eu/api/v1/cmpAuctions?limit=-1&timeZone=UCT&from=2026-08-03&to=2026-08-03&periodType=day"
    commands:
      - {run: gridflow ingest entsog cmp_auction_premiums --start 2026-08-03 --end 2026-08-04, comment: "bronze, end exclusive; repeat per member"}
      - {run: gridflow transform entsog cmp_auction_premiums --start 2026-08-03 --end 2026-08-03, comment: "silver, one gas day per file"}
  record:
    select:
      filter:
        - {column: timestamp_utc, op: eq, value: "2026-08-03T04:00:00"}
        - column: id
          op: in
          value:
            - "32025-07-10 07:00:00 +00:002025-07-16 10:00:01 +00:002025-10-01 04:00:00 +00:002026-10-01 04:00:00 +00:00DE-TSO-0009ITP-00539exitEUR/kWh/h"
            - "32023-07-03 07:00:00 +00:002023-07-04 16:00:00 +00:002025-10-01 04:00:00 +00:002026-10-01 04:00:00 +00:00BE-TSO-0001ITP-00526entryEUR/kWh/y"
            - "32025-08-04 07:00:00 +00:002025-08-07 14:00:00 +00:002026-07-01 04:00:00 +00:002026-10-01 04:00:00 +00:00BE-TSO-0001ITP-00614exitEUR/kWh/q"
            - "32024-07-01 05:00:00 +00:002024-07-03 12:00:00 +00:002025-10-01 04:00:00 +00:002026-10-01 04:00:00 +00:00HU-TSO-0001ITP-00027exitHUF"
            - "32025-08-04 07:00:00 +00:002025-08-05 10:00:00 +00:002026-07-01 04:00:00 +00:002026-10-01 04:00:00 +00:00BG-TSO-0001ITP-00128exitBGN/kWh/d"
            - "32024-07-01 10:16:00 +00:002024-07-02 10:16:00 +00:002025-10-01 04:00:00 +00:002026-10-01 04:00:00 +00:00SK-TSO-0001ITP-00027entryEUR"
            - "32017-03-06 08:00:00 +00:002017-03-06 11:05:49 +00:002025-10-01 04:00:00 +00:002026-10-01 04:00:00 +00:00DE-TSO-0010ITP-00007entryEUR"
            - "5SK-TSO-0001ITP-00027entryHU-TSO-0001"
      order_by: [operator_key, point_key]
      columns: [timestamp_utc, operator_key, point_key, direction_key, unit, auction_premium, cleared_price, reserve_price, capacity_from, capacity_to, auction_from, auction_to, operator_label, point_label, item_remarks, general_remarks, id]
    key: [timestamp_utc, id]
    caption: "Gas day 3 August 2026: six units; eustream's statement row reports no premium beside its result."
    fields:
      timestamp_utc: "gridflow's gas-day stamp: the record's start if inside that gas day, else 06:00 Brussels"
      id: "Vendor id, the per-day dedup key: dates, keys, unit; statements end in another operator"
      operator_key: ENTSOG key of the operator reporting the record
      point_key: "ENTSOG point key, such as `ITP-00027` for Balassagyarmat"
      direction_key: "`entry` or `exit` as sent, from the reporting operator's side"
      unit: Unit as sent, not converted; empty on statement rows
      auction_premium: "Premium as sent; in these rows, cleared minus reserve where both are sent"
      cleared_price: Price the auction cleared at, as sent; null when only a premium is sent
      reserve_price: Reserve price of the auction, as sent; null when only a premium is sent
      capacity_from: "Start of the capacity product, from `capacityFrom`, in UTC"
      capacity_to: "End of the capacity product, from `capacityTo`, in UTC"
      auction_from: "Start of the auction, from `auctionFrom`, in UTC; null on statement rows"
      auction_to: "End of the auction, from `auctionTo`, in UTC"
      operator_label: Name of the reporting operator, as sent
      point_label: ENTSOG's name for the point, as sent
      item_remarks: The operator's remark on the result, such as an auction id and product
      general_remarks: ENTSOG's statement text on statement rows; null on these auction results
      period_from: "Null on results; on statement rows, the requested day at 00:00+02:00, in UTC"
      period_to: "Equal to `period_from` on statement rows; null on results"
      indicator: Field shared with operational data; null or empty in these rows
      period_type: Field shared with operational data; null or empty in these rows
      tso_eic_code: Energy Identification Code of the reporting operator, as sent
      value: Field shared with operational data; null in these rows
      tso_item_identifier: The reporting operator's own identifier for the point, as sent
      last_update_date_time: "The vendor's `lastUpdateDateTime` for the record, converted to UTC"
      booking_platform_key: "Booking platform as sent, such as `PRISMA` or `RBP`"
      booking_platform_label: The booking platform's name, as sent
      booking_platform_url: The booking platform's address, as sent
      point_type: ENTSOG's point type, as sent; null on statement rows
      id_point_type: ENTSOG's point type code, as sent; null on statement rows
      data_set: "Vendor `dataSet` code, as sent; ENTSOG's meaning for it is not documented here"
      is_unlimited: Field shared with operational data; null or empty in these rows
      flow_status: Field shared with operational data; empty in these rows
      interruption_type: Field shared with operational data; null or empty in these rows
      restoration_information: Field shared with operational data; null or empty in these rows
      capacity_type: Field shared with operational data; null or empty in these rows
      capacity_booking_status: Field shared with operational data; null or empty in these rows
      is_na: Field shared with operational data; null or empty in these rows
      original_period_from: Field shared with operational data; null in these rows
      is_cmp_relevant: Field shared with operational data; null or empty in these rows
      interruption_calculation_remark: Field shared with operational data; null in these rows
      is_archived: Vendor archive flag, as sent
      is_cam_relevant: "Vendor flag `isCAMRelevant` or `isCamRelevant`, as sent; null on these results"
  notebook:
    lead: >-
      Reads `silver_entsog_cmp_auction_premiums`, lineage columns dropped, where `timestamp_utc`,
      gridflow's gas-day stamp, falls between the dates given, ends included. Each record repeats on
      every gas day it covers; the last cell reads unsuccessful requests likewise.
    cells:
      - |
        ap = data.entsog.query("cmp_auction_premiums", "2026-08-03", "2026-08-03")
        results = ap[ap.auction_premium.notna()]
        results["unit"].value_counts()
      - |
        results[results.point_key == "ITP-00027"][["operator_label", "direction_key", "unit",
                                                   "auction_premium", "cleared_price", "reserve_price"]]
      - |
        ur = data.entsog.query("cmp_unsuccessful_requests", "2026-08-03", "2026-08-03")
        ur = ur[ur.requested_volume.notna() & (ur.unit == "kWh/d")]
        ur.plot.scatter(x="requested_volume", y="allocated_volume", color="#155A6E", figsize=(6, 4),
                        xlabel="requested_volume, kWh/d", ylabel="allocated_volume, kWh/d")
    needs: the three tables for gas day 3 August 2026
    plot_alt: >-
      Scatter plot of the 41 unsuccessful requests in kWh/d on gas day 3 August 2026, requested
      volume across against allocated volume up, both axes in units of 10 million. Most requests
      sit below 7 million; the largest, 40.5 million, had 38.1 million allocated, while requests of
      28.6 and 33.7 million had none.
  related:
    - {dataset: entsog/tariffs, note: "Operators' published capacity prices per point, direction and product"}
    - {dataset: entsog/firm_booked, note: "Booked firm capacity per point, from ENTSOG's operational data"}
    - {dataset: entsog/physical_flows, note: Daily physical gas flows per point from the same platform}
    - {dataset: entsog/operator_point_directions, note: "The register of the operator, point and direction keys"}
  family:
    slug: cmp
    members:
      - dataset: cmp_auction_premiums
        differs: "Auction results per product: premium, cleared and reserve price, in mixed units"
        request: "GET https://transparency.entsog.eu/api/v1/cmpAuctions?limit=-1&timeZone=UCT&from=2026-08-03&to=2026-08-03&periodType=day"
        caveat: "Results use six units over 1 to 5 August 2026; which price `unit` covers is unconfirmed."
      - dataset: cmp_unavailable_firm_capacity
        differs: "Unavailable periods and allocation process; on 3 August 2026, no value sent"
        request: "GET https://transparency.entsog.eu/api/v1/cmpUnavailables?limit=-1&timeZone=UCT&from=2026-08-03&to=2026-08-03&periodType=day"
      - dataset: cmp_unsuccessful_requests
        differs: "Requested, allocated and unallocated volume in its `unit`, plus `occurenceCount`, per product"
        request: "GET https://transparency.entsog.eu/api/v1/cmpUnsuccessfulRequests?limit=-1&timeZone=UCT&from=2026-08-03&to=2026-08-03&periodType=day"
---

# ENTSOG — Cmp Auction Premiums

## Overview

CMP auction premiums and reserve/cleared prices for capacity auctions. Each record is one auction result for a firm capacity product at one operator, point and direction. ENTSOG also sends statement rows, one per operator, point, direction and neighbouring operator, with empty prices and no unit, usually "Currently there are no firm capacity products on this point with a duration of one month or longer auctioned having cleared with an auction premium." On 3 August 2026 some points carry both results and a statement row, and some points in the `operator_point_directions` register carry neither. At Open Grid Europe's Dornum GASPOOL and VIP THE-ZTP entries and eustream's Balassagyarmat entry, among others, that statement sits beside results that send a premium; ENTSOG does not say how the two relate. No ENTSOG definition of the fields is quoted here.

→ Related concepts:
  [Gas day](../../../20-domain/concepts/gas-day.md)

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://transparency.entsog.eu/api/v1` |
| Path             | `/cmpAuctions` |
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
  "https://transparency.entsog.eu/api/v1/cmpAuctions?from=2026-05-06&to=2026-05-06&timeZone=UCT&periodType=day&forceDownload=true&limit=1000"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsog/cmp_auction_premiums/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable.
**Granularity**: One file per fetch call (per calendar day window).

### Bronze sample

```json
{
  "meta": {
    "limit": 1000,
    "offset": 0,
    "count": 1,
    "total": 214,
    "query": {
      "from": "2026-05-06",
      "to": "2026-05-06",
      "timeZone": "UCT",
      "periodType": "day"
    },
    "timezone": "CET"
  },
  "cmpAuctions": [
    {
      "auctionFrom": "2017-03-06T09:00:00+01:00",
      "auctionTo": "2017-03-06T12:05:49+01:00",
      "capacityFrom": "2025-10-01T06:00:00+02:00",
      "capacityTo": "2026-10-01T06:00:00+02:00",
      "operatorKey": "DE-TSO-0010",
      "tsoEicCode": "21X-DE-A-A0A0A-A",
      "operatorLabel": "bayernets",
      "pointKey": "ITP-00007",
      "pointLabel": "\u00dcberackern SUDAL (AT) / \u00dcberackern 2 (DE)",
      "tsoItemIdentifier": "21Z0000000001240",
      "directionKey": "entry",
      "unit": "EUR",
      "itemRemarks": null,
      "generalRemarks": null,
      "auctionPremium": 0,
      "clearedPrice": 6.05243,
      "reservePrice": 6.05243,
      "lastUpdateDateTime": "2017-03-06T12:16:01+01:00",
      "isCAMRelevant": null,
      "bookingPlatformKey": "PRISMA",
      "bookingPlatformLabel": "PRISMA",
      "bookingPlatformURL": "https://platform.prisma-capacity.eu/",
      "pointType": "Cross-Border Transmission IP within EU",
      "idPointType": 0,
      "id": "32017-03-06 08:00:00 +00:002017-03-06 11:05:49 +00:002025-10-01 04:00:00 +00:002026-10-01 04:00:00 +00:00DE-TSO-0010ITP-00007entryEUR",
      "dataSet": 3,
      "indicator": null,
      "periodType": null,
      "periodFrom": null,
      "periodTo": null,
      "value": null,
      "isUnlimited": null,
      "flowStatus": "",
      "interruptionType": null,
      "restorationInformation": null,
      "capacityType": null,
      "capacityBookingStatus": null,
      "isNA": null,
      "originalPeriodFrom": null,
      "isCmpRelevant": null,
      "interruptionCalculationRemark": null,
      "isArchived": null
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsog/cmp_auction_premiums/year=YYYY/month=MM/cmp_auction_premiums_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsog.generic.GenericEntsogJsonTransformer (subclass CmpAuctionPremiumsTransformer)`
**Pydantic schema**: Generic — no Pydantic schema declared
**Dedup key**: `id`, within each gas day's file (`keep="last"`, `silver/entsog/generic.py` `transform`). Every record sends an `id`, so `(timestamp_utc, id)` is unique across files.
**Point-in-time field**: none. `timestamp_utc` is gridflow's gas-day stamp: the record's own start if it falls inside the gas day, else the gas-day start, 06:00 Europe/Brussels (`silver/entsog/datetime.py` `gas_day_stamp`). On 1 to 5 August 2026 no record starts inside a gas day, so every row reads 04:00 UTC. `last_update_date_time` is the vendor's own stamp.
**Day filter**: silver day D keeps every record whose capacity period overlaps gas day D, plus the statement rows dated D (`partition_validity_records_to_gas_day`).

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| timestamp_utc | datetime[UTC] | No | derived | gridflow's gas-day stamp; see Point-in-time field |
| auction_from | datetime[UTC] | Yes | auctionFrom |  |
| auction_to | datetime[UTC] | Yes | auctionTo |  |
| capacity_from | datetime[UTC] | Yes | capacityFrom |  |
| capacity_to | datetime[UTC] | Yes | capacityTo |  |
| operator_key | str | Yes | operatorKey |  |
| tso_eic_code | str | Yes | tsoEicCode |  |
| operator_label | str | Yes | operatorLabel |  |
| point_key | str | Yes | pointKey |  |
| point_label | str | Yes | pointLabel |  |
| tso_item_identifier | str | Yes | tsoItemIdentifier |  |
| direction_key | str | Yes | directionKey |  |
| unit | str | Yes | unit |  |
| item_remarks | str | Yes | itemRemarks |  |
| general_remarks | str | Yes | generalRemarks |  |
| auction_premium | float | Yes | auctionPremium |  |
| cleared_price | float | Yes | clearedPrice |  |
| reserve_price | float | Yes | reservePrice |  |
| last_update_date_time | datetime[UTC] | Yes | lastUpdateDateTime |  |
| is_cam_relevant | bool | Yes | isCAMRelevant | Coalesced with the statement rows' `isCamRelevant` |
| booking_platform_key | str | Yes | bookingPlatformKey |  |
| booking_platform_label | str | Yes | bookingPlatformLabel |  |
| booking_platform_url | str | Yes | bookingPlatformURL |  |
| point_type | str | Yes | pointType |  |
| id_point_type | int | Yes | idPointType |  |
| id | str | Yes | id | Vendor record id; the dedup key within a gas day |
| data_set | int | Yes | dataSet | `3` on every row of 1 to 5 August 2026 |
| indicator | str | Yes | indicator |  |
| period_type | str | Yes | periodType |  |
| period_from | datetime[UTC] | Yes | periodFrom |  |
| period_to | datetime[UTC] | Yes | periodTo |  |
| value | float | Yes | value |  |
| is_unlimited | str | Yes | isUnlimited | Kept as text |
| flow_status | str | Yes | flowStatus |  |
| interruption_type | str | Yes | interruptionType |  |
| restoration_information | str | Yes | restorationInformation |  |
| capacity_type | str | Yes | capacityType |  |
| capacity_booking_status | str | Yes | capacityBookingStatus |  |
| is_na | str | Yes | isNA |  |
| original_period_from | datetime[UTC] | Yes | originalPeriodFrom |  |
| is_cmp_relevant | str | Yes | isCmpRelevant | Kept as text |
| interruption_calculation_remark | null | Yes | interruptionCalculationRemark | Null on every row of 1 to 5 August 2026 |
| is_archived | bool | Yes | isArchived |  |
| data_provider | str | No | derived | Always `entsog` |
| ingested_at | datetime[UTC] | No | derived | Wall-clock at silver write |
| event_time, available_at, source_run_id, dataset_version | | No | derived | Pipeline lineage columns (`silver/base.py`) |

### Silver sample

One real silver row, gas day 3 August 2026 (the same bayernets record the bronze sample shows), in silver's column order with UTC stamps:

```python
[
    {
        "timestamp_utc": "2026-08-03T04:00:00+00:00",
        "period_from": null,
        "period_to": null,
        "indicator": null,
        "period_type": null,
        "operator_key": "DE-TSO-0010",
        "operator_label": "bayernets",
        "tso_eic_code": "21X-DE-A-A0A0A-A",
        "point_key": "ITP-00007",
        "point_label": "\u00dcberackern SUDAL (AT) / \u00dcberackern 2 (DE)",
        "direction_key": "entry",
        "unit": "EUR",
        "value": null,
        "id": "32017-03-06 08:00:00 +00:002017-03-06 11:05:49 +00:002025-10-01 04:00:00 +00:002026-10-01 04:00:00 +00:00DE-TSO-0010ITP-00007entryEUR",
        "auction_from": "2017-03-06T08:00:00+00:00",
        "auction_to": "2017-03-06T11:05:49+00:00",
        "capacity_from": "2025-10-01T04:00:00+00:00",
        "capacity_to": "2026-10-01T04:00:00+00:00",
        "tso_item_identifier": "21Z0000000001240",
        "item_remarks": null,
        "general_remarks": null,
        "auction_premium": 0.0,
        "cleared_price": 6.05243,
        "reserve_price": 6.05243,
        "last_update_date_time": "2017-03-06T11:16:01+00:00",
        "booking_platform_key": "PRISMA",
        "booking_platform_label": "PRISMA",
        "booking_platform_url": "https://platform.prisma-capacity.eu/",
        "point_type": "Cross-Border Transmission IP within EU",
        "id_point_type": 0,
        "data_set": 3,
        "is_unlimited": null,
        "flow_status": "",
        "interruption_type": null,
        "restoration_information": null,
        "capacity_type": null,
        "capacity_booking_status": null,
        "is_na": null,
        "original_period_from": null,
        "is_cmp_relevant": null,
        "interruption_calculation_remark": null,
        "is_archived": null,
        "is_cam_relevant": null,
        "data_provider": "entsog",
        "ingested_at": "2026-10-24T13:56:02+00:00",
        "event_time": "2026-08-03T04:00:00+00:00",
        "available_at": "2026-08-16T14:21:16+00:00",
        "source_run_id": "adhoc-2026-10-24T13:56:02.858530+00:00",
        "dataset_version": "1.0.0"
    }
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **Records in force, repeated daily**: CMP family endpoints accept `from` / `to`. In the responses for 1 to 5 August 2026, every result's capacity period covers the requested day and the same 54 results come back each day; starts reach back years (a 2017 auction for the 2025/26 gas year). Silver keeps each result in every gas day's file it overlaps, so an `id` repeats once per fetched day. Don't dedup on period alone.
- **Statement rows**: on 1 to 5 August 2026, 1,007 of the 1,061 records a day are ENTSOG statement rows, not auction results: `id` starts with `5` and ends with another operator's key, the three prices are empty strings (null in silver), `unit` is empty, and `periodFrom` = `periodTo` = 00:00+02:00 on the requested day, as sent. A point and direction with several neighbouring operators gets one statement row per neighbour (three for National Gas TSO at Moffat entry on 3 August 2026). Statement rows do not mark the points without results: on 3 August 2026, 15 of the 21 operator, point and direction triples with results also carry one, and 256 of the 1,225 triples in `operator_point_directions` have no row of either kind. Filter on `auction_premium` not null to keep results only.
- **Statements that contradict results**: on 1 to 5 August 2026 the statement "no firm capacity products ... auctioned having cleared with an auction premium" sits beside results with premiums at Open Grid Europe's Dornum GASPOOL entry (0.02) and VIP THE-ZTP entry (up to 1.92), eustream's Balassagyarmat entry (368.65), `FR-TSO-0003`'s Oltingue and VIRTUALYS exits (results labelled NaTran and GRTgaz) and Gasunie Deutschland's Emden (EPT1) entry. ENTSOG does not say how the two relate (the statement may describe a later auction round; unconfirmed).
- **Statement text from another table**: on 1 to 5 August 2026 some of bayernets' statement rows in this table carry the unsuccessful-requests sentence ("Currently there are no request for firm capacity products on this point ..."), others its own remarks; FGSZ's are empty.
- **Mixed units**: on 1 to 5 August 2026 the 54 results use six units: `EUR/kWh/h` 22 (Open Grid Europe), `EUR` 18, `HUF` 7 (FGSZ), `EUR/kWh/y` 4 and `EUR/kWh/q` 2 (Fluxys Belgium), `BGN/kWh/d` 1 (Bulgartransgaz). Which of `auctionPremium`, `clearedPrice` and `reservePrice` the `unit` applies to is unconfirmed, and silver converts nothing. Never sum or chart across units.
- **Premium against prices**: where both prices are sent (46 of the 54 results, 1 to 5 August 2026), `auction_premium` equals `cleared_price` minus `reserve_price` to within 1e-12. Eight results (GRTgaz, NaTran and eustream, unit `EUR`) send a premium and no prices. This is gridflow's check on those days, not an ENTSOG rule.
- **Zero premiums**: some results send a premium of 0 (bayernets) or about 1e-8, although ENTSOG's statement text speaks of products "having cleared with an auction premium".
- **`isCAMRelevant` (uppercase CAM)**: in the 1 to 5 August 2026 responses only `cmpAuctions` results send the uppercase variant; its statement rows and the other two CMP endpoints send `isCamRelevant`. Generic silver coalesces them into `is_cam_relevant`.
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
