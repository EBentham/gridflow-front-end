---
source: elexon
dataset_key: remit
vendor: Elexon BMRS
last_verified: 2026-05-09
layer_coverage: bronze, silver
page:
  title: REMIT unavailability messages
  summary: >-
    Elexon's REMIT messages: each outage or unavailability of a unit, with its event window,
    capacity in MW and every revision received.
  facts:
    vendor: Elexon BMRS, dataset REMIT
    cadence: No cadence stated by Elexon; revisions arrive at irregular publish times
    grain: One row per message revision received; Elexon can re-send a revision, sometimes identically
  landscape: power
  what_it_is: >-
    A message (`mrid`) reports one event, such as a unit's outage: its event start and end,
    normal, available and unavailable MW, status and cause. The sender revises it as the event
    changes, and gridflow keeps every revision it receives, not only the latest. Elexon can
    re-send a revision number with changed content, so the number alone does not order revisions.
  how_used:
    - Units out at a delivery time, for a merit-order supply stack.
    - "Point-in-time outage features: only revisions published before the forecast is made."
    - Joining outages to the BM unit register on `asset_id` for fuel and capacity.
  chart:
    type: bar
    silver: elexon/remit
    filter:
      - {column: message_type, op: eq, value: UnavailabilitiesOfElectricityFacilities}
      - {column: timestamp_utc, op: ge, value: "2026-09-13T00:00:00"}
      - {column: timestamp_utc, op: lt, value: "2026-09-22T00:00:00"}
    dedup: {on: [mrid], order_by: revision_number}
    group: fuel_type
    group_null: no_fuel
    group_map:
      Fossil Gas: gas
      Biomass: biomass
      Wind Offshore: wind
      Wind Onshore: wind
      Hydro Pumped Storage: hydro
      Hydro Water Reservoir: hydro
      Nuclear: nuclear
      Other: other
    aggregation: count
    sort: value_desc
    unit: messages
  chart_view:
    title: Unavailability messages by fuel type, 13 to 21 September 2026
    caption: >-
      Silver `elexon/remit`, unavailability messages with a revision published 13 to 21 September
      2026 (UTC), each counted once under the fuel type of its highest revision there. A count of
      messages, not of outages in force or MW.
    alt: >-
      Horizontal bar chart counting unavailability messages by fuel type from elexon/remit, each
      message with a revision published 13 to 21 September 2026 counted once. Gas leads with 246,
      then no fuel type 99, biomass 79, wind (offshore and onshore) 70, hydro (pumped storage and
      reservoir) 31, nuclear 8 and other 8.
    key:
      - {series: gas, label: Gas, codes: Fossil Gas}
      - {series: no_fuel, label: No fuel type, codes: "null", paint: hatch-dots, note: "Elexon's record has no `fuelType` field: a missing value, not a fuel."}
      - {series: biomass, label: Biomass, codes: Biomass}
      - {series: wind, label: Wind, codes: "Wind *, 2 values", note: "`Wind Offshore` and `Wind Onshore` counted together."}
      - {series: hydro, label: Hydro, codes: "Hydro *, 2 values", paint: hatch-lines, note: "`Hydro Pumped Storage` and `Hydro Water Reservoir`. Pumped units here send generating and pumping sides separately."}
      - {series: nuclear, label: Nuclear, codes: Nuclear}
      - {series: other, label: Other, codes: Other, note: "Elexon's own category; what it holds is undocumented."}
  raw_feed:
    note: >-
      Elexon Insights API, in 23-hour publish windows: the project found windows over a day
      rejected. Bronze is filed by window start day, so one silver file can span two dates.
    requests:
      - "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/REMIT?publishDateTimeFrom=2026-09-18T18:00:00Z&publishDateTimeTo=2026-09-19T17:00:00Z&page=1"
    commands:
      - {run: gridflow ingest elexon remit --start 2026-09-13 --end 2026-09-22, comment: "bronze; the end is exclusive"}
      - {run: gridflow transform elexon remit --start 2026-09-13 --end 2026-09-21, comment: "bronze to silver, by publish window"}
  record:
    select:
      filter:
        - {column: asset_id, op: eq, value: T_PEMB-41}
        - {column: timestamp_utc, op: ge, value: "2026-09-18T00:00:00"}
      order_by: [revision_number]
      columns: [asset_id, revision_number, event_start_time, event_end_time, available_capacity_mw, unavailable_capacity_mw, timestamp_utc, event_status, normal_capacity_mw, related_information, mrid]
    key: [mrid, revision_number, timestamp_utc]
    caption: "Revisions 5 to 12 of one message about gas unit `T_PEMB-41`, published 18 and 19 September."
    fields:
      asset_id: "Asset as sent (`assetId`), here a BM unit ID; `NO_ASSET` names none"
      revision_number: "Revision of the message (`revisionNumber`); Elexon can send one number twice"
      event_start_time: "Event start, UTC, as sent (`eventStartTime`)"
      event_end_time: "Event end, UTC, as sent (`eventEndTime`); it moves between these revisions"
      available_capacity_mw: "MW available during the event, as sent (`availableCapacity`)"
      unavailable_capacity_mw: "MW unavailable, as sent (`unavailableCapacity`); need not equal normal minus available"
      timestamp_utc: "When Elexon published this revision (`publishTime`); not the outage's start or end"
      event_status: "Status as sent (`eventStatus`); here `Active`, then `Inactive`"
      normal_capacity_mw: "The unit's normal MW, as sent (`normalCapacity`)"
      related_information: "Free text from the sender (`relatedInformation`); here, what the revision changed"
      mrid: "Message ID (`mrid`), shared by every revision of the message"
      message_type: "Message type as sent (`messageType`)"
      message_heading: "Heading as sent (`messageHeading`), free text"
      event_type: "Event type as sent (`eventType`), for example `Production unavailability`"
      unavailability_type: "As sent (`unavailabilityType`); here `Unplanned`"
      participant_id: "Market participant code, as sent (`participantId`)"
      registration_code: "The participant's REMIT registration code, as sent (`registrationCode`)"
      asset_type: "Asset type as sent (`assetType`), for example `Production`; may be null"
      affected_unit: "Affected unit name, as sent (`affectedUnit`)"
      affected_unit_eic: "EIC of the affected unit, as sent (`affectedUnitEIC`)"
      bidding_zone: "Bidding zone EIC, as sent (`biddingZone`)"
      fuel_type: "Fuel as sent (`fuelType`), for example `Fossil Gas`; not the FUELHH codes"
      cause: "Cause as sent (`cause`), free text"
  notebook:
    lead: >-
      Returns a pandas DataFrame from the DuckDB view `silver_elexon_remit_latest`: one row per
      `mrid`, its newest silver write then highest revision, kept if published in the window
      (`timestamp_utc`, both dates included). Lineage columns dropped.
    cells:
      - df = data.elexon.query("remit", "2026-09-13", "2026-09-21")
      - df[["asset_id", "event_start_time", "event_end_time", "unavailable_capacity_mw", "revision_number", "event_status"]].head()
      - |
        import matplotlib.pyplot as plt
        nuc = df[(df.fuel_type == "Nuclear") & (df.event_status == "Active")]
        nuc = nuc.sort_values("event_start_time", ascending=False)
        fig, ax = plt.subplots(figsize=(8, 3.5))
        ax.hlines(nuc.asset_id, nuc.event_start_time, nuc.event_end_time,
                  lw=8, color="#155A6E")
        ax.set_xlabel("event window, UK time");
    needs: 13 to 21 September 2026
    plot_alt: >-
      Timeline of the active nuclear messages returned: one bar per message from event start to
      end, UK time, not scaled by MW. T_HRTL-1 runs from early May to 23 September 2026; T_TORN-1,
      T_HRTL-2, T_SIZB-2 and T_HEYM27 sit in September and early October; T_HEYM11 has two messages
      back to back, late August to 7 January 2027.
  related:
    - {dataset: elexon/bmunits_reference, note: "The BM unit register that `asset_id` joins to"}
    - {dataset: elexon/uou2t14d, note: "Forward availability for the units these messages name"}
    - {dataset: elexon/fou2t14d, note: "Forward availability for the fuel types charted here"}
    - {dataset: elexon/pn, note: "Physical notifications for the same units, per settlement period"}
---

# Elexon - REMIT Outage and Unavailability Messages (`REMIT`)

## Overview

REMIT outage and unavailability messages — Regulation (EU) No 1227/2011 mandates publication of generation, transmission, and demand-side asset unavailability events. The dataset carries every UMM (Urgent Market Message) raised against GB assets, with start/end times, capacity affected, cause, and event status.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://data.elexon.co.uk/bmrs/api/v1` |
| Path             | `/datasets/REMIT` |
| Method           | GET |
| Auth             | None required for tested endpoints (2026-05-08). Some endpoints accept an `apikey` header (env: `ELEXON_API_KEY`); registration at https://www.elexonportal.co.uk/. |
| Rate limit       | Vendor-published: not stated. Project default 2 req/sec (asyncio.Semaphore); verified safe 2026-05-08. |
| Pagination       | Connector handles via `page=N` query param; stops when `page >= total_pages`. Reference endpoints (`/reference/bmunits/all`) are not paginated. |
| Historical depth | Active and recent expired messages; full history per UMM lifecycle. |
| Publication lag  | Real-time as messages are raised. |
| Response format  | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `publishDateTimeFrom` | string | Yes | As per Elexon Swagger spec for remit. | `2026-05-06T00:00Z` |
| `publishDateTimeTo` | string | Yes | As per Elexon Swagger spec for remit. | `2026-05-06T03:00Z` |
| `format` | string | No | Response data format. Use json/xml to include metadata. | `json` |

### Working curl example

```bash
# Replace <ELEXON_API_KEY> with your env var if you choose to send one (Elexon endpoints
# tested 2026-05-08 do NOT require a key; set anyway for vendor courtesy).
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://data.elexon.co.uk/bmrs/api/v1/datasets/REMIT?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-07T00:00Z&format=json" \
  -o "/tmp/elexon-remit.json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/elexon/remit/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per API call (paginated requests append additional files for the same date partition).

### Bronze sample

Captured live 2026-05-08 from the https://data.elexon.co.uk/bmrs/api/v1/datasets/REMIT?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-07T00:00Z&format=json:

```json
{
  "data": [
    {
      "dataset": "REMIT",
      "mrid": "48X000000000392E-NGET-RMT-00209309",
      "revisionNumber": 147,
      "publishTime": "2026-05-06T23:09:05Z",
      "createdTime": "2026-05-06T23:00:13Z",
      "messageType": "UnavailabilitiesOfElectricityFacilities",
      "messageHeading": "Actual Availability of Generation Unit",
      "eventType": "Production unavailability",
      "unavailabilityType": "Unplanned",
      "participantId": "SOFIA",
      "registrationCode": "48X000000000392E",
      "assetId": "T_SOFOW-12",
      "assetType": "Production",
      "affectedUnit": "SOFWO-12",
      "affectedUnitEIC": "48W0000SOFOW-12T",
      "biddingZone": "10YGB----------A",
      "fuelType": "Wind Offshore",
      "normalCapacity": 350.0,
      "availableCapacity": 0.0,
      "unavailableCapacity": 0.0,
      "eventStatus": "Active",
      "eventStartTime": "2025-12-09T05:00:00Z",
      "eventEndTime": "2026-05-22T04:00:00Z",
      "cause": "Ambient Conditions",
      "relatedInformation": "Estimated End Date / Time changed to 22 May 2026 04:00 (GMT); Detailed MEL profile has changed",
      "outageProfile": [
        {
          "startTime": "2025-12-09T05:00:00Z",
          "endTime": "2025-12-09T05:00:00Z",
          "capacity": 0.0
        },
        {
          "startTime": "2025-12-09T05:00:00Z",
          "endTime": "2026-05-22T04:00:00Z",
          "capacity": 0.0
        }
      ]
    },
    "... (truncated)"
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/elexon/remit/year=YYYY/month=MM/remit_YYYYMMDD_run<available_at>.parquet`
**Write mode**: append-only revision-preserving Silver files (`APPEND_ONLY = True`).
**Transformer class**: `gridflow.silver.elexon.remit.REMITTransformer`
**Pydantic schema**: `gridflow.schemas.elexon.ElexonREMIT` — validated fail-soft on the full frame at write time (VTA-SCHEMA-01: invalid rows are logged and counted, never dropped).
**Dedup key**: none in the transformer: every revision received is written (`silver/elexon/remit.py:22-27`, `:46-50`). Read-time latest: `silver_elexon_remit_latest` keeps one row per `mrid`, ordered `available_at` then `revision_number`, both descending (`silver/latest_views.py:100-103`).
**Point-in-time field**: `timestamp_utc` (the vendor `publishTime`); `revision_number` numbers a message's revisions

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `mrid` | `str` | No | `mrid` | REMIT message MRID. |
| `revision_number` | `int` | Yes | `revisionNumber` | Revision number. |
| `timestamp_utc` | `datetime[UTC]` | No | `publishTime` | The vendor publish time, parsed to UTC (`remit.py:118-123`). `publishTime` and `createdTime` are renamed to `published_at` and `created_time` but not written (`remit.py:149-177`). |
| `message_type` | `str` | Yes | `messageType` | REMIT message type. |
| `message_heading` | `str` | Yes | `messageHeading` | Message heading. |
| `event_type` | `str` | Yes | `eventType` | Event type code. |
| `unavailability_type` | `str` | Yes | `unavailabilityType` | Planned/Unplanned. |
| `participant_id` | `str` | Yes | `participantId` | Market participant identifier. |
| `registration_code` | `str` | Yes | `registrationCode` | REMIT registration code. |
| `asset_id` | `str` | Yes | `assetId` | Asset identifier. |
| `asset_type` | `str` | Yes | `assetType` | Asset type. |
| `affected_unit` | `str` | Yes | `affectedUnit` | Affected unit name. |
| `affected_unit_eic` | `str` | Yes | `affectedUnitEIC` | EIC of affected unit. |
| `bidding_zone` | `str` | Yes | `biddingZone` | Bidding zone code. |
| `fuel_type` | `str` | Yes | `fuelType` | Fuel as sent, e.g. `Fossil Gas`, `Wind Offshore`, `Nuclear` (not the FUELHH codes); often null (silver, 2026-09-29). |
| `normal_capacity_mw` | `float` | Yes | `normalCapacity` | MW. |
| `available_capacity_mw` | `float` | Yes | `availableCapacity` | MW. |
| `unavailable_capacity_mw` | `float` | Yes | `unavailableCapacity` | MW. |
| `event_status` | `str` | Yes | `eventStatus` | Status as sent, e.g. `Active`, `Inactive`, `Dismissed` (silver, 2026-09-29; no `Withdrawn`); meanings not documented here. |
| `event_start_time` | `datetime[UTC]` | Yes | `eventStartTime` | Outage start. |
| `event_end_time` | `datetime[UTC]` | Yes | `eventEndTime` | Outage end. |
| `cause` | `str` | Yes | `cause` | Free-text cause. |
| `related_information` | `str` | Yes | `relatedInformation` | Related information field. |
| `data_provider` | `str` | No | _derived_ | Default `"elexon"`. |
| `ingested_at` | `datetime[UTC]` | Yes | _derived_ | When the silver transform ran: `datetime.now(UTC)` (`remit.py:141-146`), not the bronze ingest time. |

### Silver sample

```python
[
    {
        "mrid": "48X000000000392E-NGET-RMT-00209309",
        "revision_number": 147,
        "timestamp_utc": "2026-05-06T23:09:05+00:00",
        "message_type": "UnavailabilitiesOfElectricityFacilities",
        "message_heading": "Actual Availability of Generation Unit",
        "event_type": "Production unavailability",
        "unavailability_type": "Unplanned",
        "participant_id": "SOFIA",
        "registration_code": "48X000000000392E",
        "asset_id": "T_SOFOW-12",
        "asset_type": "Production",
        "affected_unit": "SOFWO-12",
        "affected_unit_eic": "48W0000SOFOW-12T",
        "bidding_zone": "10YGB----------A",
        "fuel_type": "Wind Offshore",
        "normal_capacity_mw": 350.0,
        "available_capacity_mw": 0.0,
        "unavailable_capacity_mw": 0.0,
        "event_status": "Active",
        "event_start_time": "2025-12-09T05:00:00Z",
        "event_end_time": "2026-05-22T04:00:00Z",
        "cause": "Ambient Conditions",
        "related_information": "Estimated End Date / Time changed to 22 May 2026 04:00 (GMT); Detailed MEL profile has changed",
        "data_provider": "elexon",
        "ingested_at": "2026-05-08T12:00:00Z"
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **Max-1-day query window enforced** — see Implementation delta.
- **Revisions**: `revisionNumber` increments — keep the highest per `mrid` for the canonical state.
  But `(mrid, revisionNumber)` is not unique: Elexon re-sends a revision number with changed
  content (event window, status). Measured on silver 2026-09-29: 62 extra rows over 42 such
  pairs, 3 mixing `Active` and `Dismissed`; 6 rows repeat on every vendor field. Nor does
  publish time order every case: in 4 messages a lower number was published after a higher one
  (3 of them one second later), and 47 messages carry two or more numbers in the same publish second.

---

## Implementation delta

- **Vendor-enforced max 1-day query window — RESOLVED in V2 (2026-05-09).** Connector now declares `max_chunk_hours=23` on `ENDPOINTS["remit"]` so chunks stay safely under the undocumented 1-day cap. Boundary re-verified live 2026-05-09: 23h request → HTTP 200, 25h request → HTTP 400 (same vendor error body). See gridflow commit `fix(V2-C):`.
- **Pydantic schema** `ElexonREMIT` exists in `schemas/elexon.py` and is applied via `BaseSilverTransformer._validate_against_schema` (fail-soft).

---

## Changelog

- **2026-05-09 — V2-FIX-03.** `max_chunk_hours=23` for safe DST margin. Regression test in `tests/unit/test_elexon_endpoints.py::TestRemitSosoMaxChunkHours`. Live-revalidated 23h pass / 25h fail boundary.
- **2026-05-08 — V1.** Live-validated; vendor 1-day cap surfaced.

---

## Modelling notes

TODO

---

## Links

- [Official API docs (Swagger UI)](https://bmrs.elexon.co.uk/api-documentation)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/elexon/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/elexon/remit.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/elexon.py)
- Gold view/builder
- [Domain: GB Balancing Mechanism](../../../20-domain/markets/gb-balancing-mechanism.md)
