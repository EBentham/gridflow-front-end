---
source: entsog
dataset_key: urgent_market_messages
vendor: ENTSOG Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Gas urgent market messages
  summary: >-
    Messages from European gas transmission operators on ENTSOG's platform: capacity unavailability and
    other notices, one row per version ENTSOG sends.
  facts:
    vendor: ENTSOG Transparency Platform, `/urgentMarketMessages`
    cadence: One call returns the whole list; `sources.yaml` declares it daily
    grain: "One row per message version: `thread_id` plus `version_number`"
  landscape: gas
  what_it_is: >-
    Operators' messages: capacity unavailability at a point or facility (`message_type` `Gas`) or
    other notices (`Other`), such as auction, tariff or outage-plan news. Each update is a version
    under one `thread_id`. Silver holds only the newest fetch: a message ENTSOG stops sending leaves
    silver at the next transform, so silver is not a history; bronze keeps each fetch.
  how_used:
    - Unavailable capacity at a point or facility over a message's event window.
    - Matching current messages to flows through connection point EICs; some do not resolve.
    - Joining senders to the operator register on `market_participant_key`.
  chart:
    type: bar
    silver: entsog/urgent_market_messages
    dedup: {on: [thread_id], order_by: version_number}
    group: market_participant_key
    group_map:
      DE-TSO-0009: oge
      DE-TSO-0004: natran_de
      DE-TSO-0001: gascade
      FR-TSO-0003: natran_fr
      HU-TSO-0001: fgsz
      DE-TSO-0014: terranets
      LV-TSO-0001: conexus
      CZ-TSO-0001: net4gas
    group_default: rest
    aggregation: count
    sort: value_desc
    unit: messages
  chart_view:
    title: Messages by sending operator, fetched 27 September 2026
    caption: >-
      Silver `entsog/urgent_market_messages`, all ENTSOG returned when fetched 27 September 2026. Each
      message (`thread_id`) counted once, at its highest version, by `market_participant_key`; none of
      the 20 operators is from the UK. A count of messages, not capacity.
    alt: >-
      Horizontal bar chart counting urgent market messages by sending operator in
      entsog/urgent_market_messages as fetched 27 September 2026, each message counted once. Open Grid
      Europe leads with 31, then NaTran Deutschland 21, the 12 other operators together 17, GASCADE 12,
      NaTran 5, Conexus Baltic Grid, FGSZ and terranets bw 4 each, and NET4GAS 3.
    key:
      - {series: oge, label: Open Grid Europe, codes: DE-TSO-0009, paint: petrol}
      - {series: natran_de, label: NaTran DE, codes: DE-TSO-0004, paint: petrol, note: "NaTran Deutschland; an older message names it GRTgaz Deutschland, under the same key."}
      - {series: rest, label: 12 others, codes: "12 keys", paint: hatch-dots, note: "Plinacro, Gasunie Deutschland, ONTRAS, Elering, Energinet, bayernets, Gastransport Nord, Plinovodi, Fluxys Deutschland, NEL, Fluxys TENP, Fluxys Belgium."}
      - {series: gascade, label: GASCADE, codes: DE-TSO-0001, paint: petrol}
      - {series: natran_fr, label: NaTran FR, codes: FR-TSO-0003, paint: petrol, note: "NaTran, the French operator; a separate key from NaTran Deutschland."}
      - {series: conexus, label: Conexus, codes: LV-TSO-0001, paint: petrol, note: "Conexus Baltic Grid, Latvia."}
      - {series: fgsz, label: FGSZ, codes: HU-TSO-0001, paint: petrol}
      - {series: terranets, label: terranets bw, codes: DE-TSO-0014, paint: petrol}
      - {series: net4gas, label: NET4GAS, codes: CZ-TSO-0001, paint: petrol}
  raw_feed:
    note: >-
      One GET with `limit=-1` and no dates or operator filter. Bronze keeps each fetch under its UTC
      day; `transform` rewrites one silver file from the newest fetch only.
    requests:
      - "GET https://transparency.entsog.eu/api/v1/urgentMarketMessages?limit=-1&timeZone=UCT"
    commands:
      - {run: gridflow ingest entsog urgent_market_messages, comment: "one call; no dates sent"}
      - {run: gridflow transform entsog urgent_market_messages --start 2026-09-27 --end 2026-09-27, comment: "newest fetch to one file"}
  record:
    select:
      filter:
        - {column: thread_id, op: in, value: [25063021X000000001379R006, 25112721X-FR-A-A0A0A-S001, 26090421X000000001304L001, "V0025119/1\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D"]}
      order_by: [thread_id, version_number]
      columns: [thread_id, version_number, is_latest_version, event_status, publication_date_time, event_start, event_stop, message_type, market_participant_name, event_type, affected_asset_name, unit_measure, unavailable_capacity, available_capacity, technical_capacity, last_update_date_time, u_mm_type]
    key: [thread_id, version_number]
    caption: "Eight versions of four messages. ENTSOG's manual defines no fields; meanings come from names and values."
    fields:
      thread_id: "ENTSOG's `threadId`, as sent: links the versions of one message"
      version_number: "Version within the thread as zero-padded text (`001`), so it sorts in order"
      is_latest_version: "`Yes` or `No` as text; some threads in this fetch, Kiemenai here, lack `Yes`"
      event_status: "`Active`, `Inactive` or `Dismissed`, as sent; OGE's version `002` here is `Dismissed`"
      publication_date_time: "ENTSOG's publication stamp for this version, converted to UTC from its offset"
      event_start: "Start of the event window, converted to UTC; Kiemenai's moves between versions here"
      event_stop: "End of the event window, converted to UTC from its offset"
      message_type: "`Gas` for capacity unavailability, `Other` for other notices, as sent"
      market_participant_name: "Sending operator's name, as sent; it can change under one key"
      event_type: "Kind of unavailability, such as transmission system; null on the `Other` row"
      affected_asset_name: "The affected point or facility in the operator's own wording"
      unit_measure: "Unit of this row's three capacities, as sent; it varies, so never sum rows"
      unavailable_capacity: "Unavailable in the event, in `unit_measure`; this fetch includes apparent placeholders 10000000000 and 1"
      available_capacity: "Still available, in `unit_measure`; sent as text; some versions send all three as 0"
      technical_capacity: "Here available plus unavailable; one version fetched reads a thousandth of its successor"
      last_update_date_time: "As sent; five rows here, about a quarter of this fetch, share one value"
      u_mm_type: "ENTSOG's `uMMType`: `Automatic`, `Feeds` or null, as sent; ENTSOG does not define it"
      timestamp_utc: "gridflow's copy of `publication_date_time`, not when gridflow fetched it; `query()` filters on it"
      id: "ENTSOG's record id, one per version; silver keeps one row per `id`"
      message_id: "One per version: `thread_id` and `version_number` joined by `_`, as sent"
      market_participant_key: "Sender's ENTSOG operator key, as in the operator register"
      market_participant_eic: "Sender's EIC code, as sent"
      unavailability_type: "`Planned` or `Unplanned` on `Gas` messages, as sent"
      unavailability_reason: "The operator's reason, free text; sometimes only a reference number"
      balancing_zone_key: "ENTSOG balancing zone key, as sent; often null"
      balancing_zone_eic: "Balancing zone EIC, as sent; can be present when the key is null"
      balancing_zone_name: "Balancing zone name, as sent, such as `DE THE BZ`"
      affected_asset_eic: "EIC of the affected point or facility, as sent"
      direction: "`Entry` or `Exit`, as sent; blank on some `Gas` messages"
      remarks: "The operator's free-text note; can run to several lines"
      share_point_point_id: "ENTSOG's internal point number, as sent; ENTSOG does not define it"
      share_point_publication_id: "ENTSOG's internal publication id, as sent, beginning with the sender's EIC"
      is_archived: "Archive flag, as sent; `false` or null on these rows"
  notebook:
    lead: >-
      Returns a pandas DataFrame from `silver_entsog_urgent_market_messages`, the newest fetch only:
      each version whose publication time (`timestamp_utc`) falls in the window, both dates included.
      Lineage columns dropped.
    cells:
      - |
        from datetime import date
        df = data.entsog.query("urgent_market_messages", "2000-01-01", date.today())
      - |
        msgs = df.sort_values("version_number").drop_duplicates("thread_id", keep="last")
        msgs[["thread_id", "version_number", "market_participant_name", "event_type", "event_start", "event_stop"]].head()
      - msgs["event_type"].fillna("none (an Other message)").value_counts()
      - |
        import matplotlib.pyplot as plt
        # status at the highest version sent; is_latest_version can be No throughout
        oge = msgs[(msgs.market_participant_key == "DE-TSO-0009") & (msgs.message_type == "Gas")
                   & (msgs.event_status == "Active")].sort_values("event_start", ascending=False)
        labels = oge.affected_asset_name + ", from " + oge.event_start.dt.strftime("%d %b %Y")
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.hlines(labels, oge.event_start, oge.event_stop, lw=8, color="#155A6E")
        ax.set_xlabel("event window, UK time");
    needs: one fetch of ENTSOG's urgent market messages
    plot_alt: >-
      Timeline of Open Grid Europe's 15 capacity messages flagged Active at the highest version
      sent: one bar per message, event start to end, UK time. All end 1 October 2026. VIP
      Oberkappel (a thread sent without its latest version) and Emden EPT start 1 October 2025, two
      VIP THE-ZTP in April 2026, three in July, eight on 1 September.
  related:
    - {dataset: entsog/operators, note: "The operator register that `market_participant_key` and its EIC join to"}
    - {dataset: entsog/physical_flows, note: "Daily flows by point key, reached through connection point EICs"}
    - {dataset: gie/unavailability, note: "Storage outages reported to GIE, the storage-side counterpart"}
    - {dataset: elexon/remit, note: "Unavailability messages for GB power units, from Elexon"}
---

# ENTSOG — Urgent Market Messages

## Overview

Operator unavailability notifications and other UMM bulletins.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://transparency.entsog.eu/api/v1` |
| Path             | `/urgentMarketMessages` |
| Method           | GET |
| Auth             | None (public) |
| Rate limit       | Not vendor-published; project default 5 req/s |
| Pagination       | `limit` + `offset` |
| Historical depth | TODO |
| Publication lag  | TODO |
| Response format  | JSON |
| Pagination control | `limit` + `offset` only — no `from`/`to` accepted |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `limit` | int | Yes | Page size; `-1` returns all | `100` |
| `offset` | int | No | Page offset (0-based) | `0` |

### Working curl example

```bash
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://transparency.entsog.eu/api/v1/urgentMarketMessages?limit=100"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsog/urgent_market_messages/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable.
**Granularity**: One file per fetch call.

### Bronze sample

```json
{
  "meta": {
    "limit": 100,
    "offset": 0,
    "count": 1,
    "total": 100
  },
  "urgentMarketMessages": [
    {
      "id": "5FF6EC12250430000000000000000000038576001",
      "messageId": "0000000000000000000038576_001",
      "marketParticipantKey": "DE-TSO-0009",
      "marketParticipantEic": "21X-DE-C-A0A0A-T",
      "marketParticipantName": "Open Grid Europe",
      "messageType": "Other",
      "publicationDateTime": "2021-01-07T12:08:29+01:00",
      "threadId": "0000000000000000000038576",
      "versionNumber": "001",
      "eventStatus": "Active",
      "eventType": null,
      "eventStart": "2021-10-01T06:00:00+02:00",
      "eventStop": "2030-01-01T06:00:00+01:00",
      "unavailabilityType": null,
      "unavailabilityReason": null,
      "unitMeasure": null,
      "balancingZoneKey": null,
      "balancingZoneEic": null,
      "balancingZoneName": null,
      "affectedAssetName": null,
      "affectedAssetEic": null,
      "direction": null,
      "unavailableCapacity": null,
      "availableCapacity": null,
      "technicalCapacity": null,
      "remarks": "Reduction of firm capacities for yearly auction (01.07.2019): OGE will not offer any firm freely allocable capacities at entry points (Entry-FZK) within the H-Gas market area in the yearly auction from 01.10.2021 onwards. Only interruptible capacities at entry points will be offered for a period of five years.",
      "lastUpdateDateTime": null,
      "sharePointPointId": null,
      "isLatestVersion": "Yes",
      "sharePointPublicationId": null,
      "uMMType": "Feeds",
      "isArchived": null
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsog/urgent_market_messages/urgent_market_messages.parquet` (CORRECTED 2026-10-07: one file, rewritten on every transform from the newest bronze capture only, because the endpoint is `reference=True`; `connectors/entsog/endpoints.py:199-206`, `silver/entsog/generic.py:106-116,128-129,252-259,284`. A message ENTSOG stops serving leaves silver at the next transform; older bronze bodies keep it.)
**Transformer class**: `gridflow.silver.entsog.generic.GenericEntsogJsonTransformer (subclass UrgentMarketMessagesTransformer)`
**Pydantic schema**: Generic — no Pydantic schema declared
**Dedup key**: vendor `id`, keep last (`generic.py:193-199`); `id` is unique per message version, so every version served is kept. One row = one message version; `(thread_id, version_number)` is equally unique and `message_id` = `thread_id` + `_` + `version_number` (all 133 records of the 27 Sep 2026 capture). (CORRECTED 2026-10-07)
**Point-in-time field**: `timestamp_utc` is a copy of `publication_date_time`, the first column of `_TIMESTAMP_PRIORITY` present (`generic.py:51-59,185-187`); `period_from` is absent here. `last_update_date_time` is never used. (CORRECTED 2026-10-07)

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| timestamp_utc | datetime[UTC] | No | derived | Copy of `publication_date_time` (`generic.py:185-187`) |
| id | str | Yes | id | Vendor record id, one per version; silver dedup key |
| message_id | str | Yes | messageId |  |
| market_participant_key | str | Yes | marketParticipantKey |  |
| market_participant_eic | str | Yes | marketParticipantEic |  |
| market_participant_name | str | Yes | marketParticipantName |  |
| message_type | str | Yes | messageType |  |
| publication_date_time | datetime[UTC] | Yes | publicationDateTime |  |
| thread_id | str | Yes | threadId |  |
| version_number | str | Yes | versionNumber |  |
| event_status | str | Yes | eventStatus |  |
| event_type | str | Yes | eventType |  |
| event_start | datetime[UTC] | Yes | eventStart |  |
| event_stop | datetime[UTC] | Yes | eventStop |  |
| unavailability_type | str | Yes | unavailabilityType |  |
| unavailability_reason | str | Yes | unavailabilityReason |  |
| unit_measure | str | Yes | unitMeasure |  |
| balancing_zone_key | str | Yes | balancingZoneKey |  |
| balancing_zone_eic | str | Yes | balancingZoneEic |  |
| balancing_zone_name | str | Yes | balancingZoneName |  |
| affected_asset_name | str | Yes | affectedAssetName |  |
| affected_asset_eic | str | Yes | affectedAssetEic |  |
| direction | str | Yes | direction |  |
| unavailable_capacity | float | Yes | unavailableCapacity |  |
| available_capacity | float | Yes | availableCapacity |  |
| technical_capacity | float | Yes | technicalCapacity |  |
| remarks | str | Yes | remarks |  |
| last_update_date_time | datetime[UTC] | Yes | lastUpdateDateTime |  |
| share_point_point_id | int | Yes | sharePointPointId |  |
| is_latest_version | str | Yes | isLatestVersion | `Yes` / `No` as text |
| share_point_publication_id | str | Yes | sharePointPublicationId |  |
| u_mm_type | str | Yes | uMMType |  |
| is_archived | bool | Yes | isArchived |  |
| data_provider | str | No | derived | Always `entsog` |
| ingested_at | datetime[UTC] | No | derived | Wall-clock at silver write |
| event_time, available_at, source_run_id, dataset_version | lineage | No | derived | Pipeline lineage columns (`silver/base.py`) |

### Silver sample

```python
[
    {
        "id": "5FF6EC12250430000000000000000000038576001",
        "message_id": "0000000000000000000038576_001",
        "market_participant_key": "DE-TSO-0009",
        "market_participant_eic": "21X-DE-C-A0A0A-T",
        "market_participant_name": "Open Grid Europe",
        "message_type": "Other",
        "publication_date_time": "2021-01-07T12:08:29+01:00",
        "thread_id": "0000000000000000000038576",
        "version_number": "001",
        "event_status": "Active",
        "event_type": null,
        "event_start": "2021-10-01T06:00:00+02:00",
        "event_stop": "2030-01-01T06:00:00+01:00",
        "unavailability_type": null,
        "unavailability_reason": null,
        "unit_measure": null,
        "balancing_zone_key": null,
        "balancing_zone_eic": null,
        "balancing_zone_name": null,
        "affected_asset_name": null,
        "affected_asset_eic": null,
        "direction": null,
        "unavailable_capacity": null,
        "available_capacity": null,
        "technical_capacity": null,
        "remarks": "Reduction of firm capacities for yearly auction (01.07.2019): OGE will not offer any firm freely allocable capacities at entry points (Entry-FZK) within the H-Gas market area in the yearly auction from 01.10.2021 onwards. Only interruptible capacities at entry points will be offered for a period of five years.",
        "last_update_date_time": null,
        "share_point_point_id": null,
        "is_latest_version": "Yes",
        "share_point_publication_id": null,
        "u_mm_type": "Feeds",
        "is_archived": null,
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

- **Different schema from operationalData**: UMM has `messageId`, `eventStart`, `eventStop`, `unavailabilityType`, `affectedAssetEic` — designed for human-readable bulletins not numeric series.
- **No date filter accepted on the URL**: `from`/`to` are ignored; pagination via `limit`/`offset` is the only window control. `requires_dates=False` in the connector.
- **`messageType`** (CORRECTED 2026-10-07): the values sent are `Gas` (capacity unavailability: `eventType`, `unavailabilityType`, capacities and `unitMeasure` filled) and `Other` (auction, tariff, outage-plan and similar notices; no capacities). 27 Sep 2026 capture: 69 `Gas`, 64 `Other` records. Don't filter on it without first inspecting.
- **`isLatestVersion`** (CORRECTED 2026-10-07): messages are versioned via `threadId`/`versionNumber`; the flag is text `Yes`/`No`. The response does not carry every version: in the 27 Sep 2026 capture 6 of 101 threads have no `Yes` version (for example Conexus `25063021X000000001379R006`, versions 001 to 003 all `No`), and two NaTran threads start at version 004. Filtering on `isLatestVersion = Yes` silently drops those threads; take the highest `versionNumber` per `threadId` instead.
- **`lastUpdateDateTime` is often one shared stamp** (ADDED 2026-10-07, reworded after review): 35 of 133 records (all with `uMMType` null) share `2026-09-27T02:28:56+02:00`, 2 min 27 s before the 00:31:23 UTC fetch; `Automatic` records usually carry a stamp minutes after publication (median about 7 minutes; one is earlier than publication, two about 65 days later). ENTSOG does not define it, so whether the shared value reflects an edit is unknown.
- **No field definitions** (ADDED 2026-10-07): ENTSOG's API manual v2.1 (Links) lists `/urgentMarketMessages` only as "UMM Data, Urgent Market Messages" in its endpoint table and defines none of the response fields; every meaning above is read from field names and values.
- **Capacities** (ADDED 2026-10-07): `unavailableCapacity`, `availableCapacity`, `technicalCapacity` arrive as strings (`"42000000.00"`) and are cast to float (`generic.py:189-191`). `unitMeasure` mixes `kWh/d` (61) and `kWh/h` (8) in one capture: never sum across rows. Values include apparent placeholders (`10000000000` kWh/d unavailable with 0 available at VIP France - Germany; `1` kWh/d at `SPNS2U`) and one version-001 entry a thousandfold low (terranets RC Basel `25090321X000000001163D001`: unavailable / available / technical 26.57 / 239.2 / 265.77 kWh/h in version 001 against 26,578 / 239,200 / 265,778 in version 002). Ten `Gas` versions (NaTran Deutschland, `26082121X...`) send all three capacities as 0.
- **Time offsets** (ADDED 2026-10-07): every `publicationDateTime`, `eventStart`, `eventStop` and `lastUpdateDateTime` in the 27 Sep 2026 capture carries an offset (`+01:00`/`+02:00`), so the UTC conversion is exact. `eventStop` is null on one record and runs to 2030 to 2099 on 15 (open-ended notices).
- **Senders** (ADDED 2026-10-07): no operator or point filter is sent, so the response covers every operator posting on the platform; in the 27 Sep 2026 capture that is 20 continental TSOs (no UK operator), each `marketParticipantKey` resolving in `operators` with a matching EIC.

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

- **Vendor empty convention**: HTTP 404 + `{"message":"No result found"}`.
- **Generic transformer**: dynamic schema; columns derived from live response.
- **`requires_dates=False` for UMM**: connector does not pass `from`/`to`. Date filtering is downstream.
- **Request sent** (ADDED 2026-10-07): one call, `GET /urgentMarketMessages?limit=-1&timeZone=UCT` (`endpoints.py:263-281`, `client.py:75-76`); bronze sidecar `request_url` matches. No `limit`/`offset` paging is used.

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
