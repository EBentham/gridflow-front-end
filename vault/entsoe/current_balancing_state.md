---
source: entsoe
dataset_key: current_balancing_state
vendor: ENTSO-E Transparency Platform
last_verified: 2026-10-24
layer_coverage: bronze, silver
page:
  title: Current balancing state
  summary: >-
    Each balancing area's open loop area control error in MW, averaged over each minute, with
    ENTSO-E's Up or Down direction code.
  facts:
    vendor: ENTSO-E Transparency Platform, document type A86, business type B33
    cadence: Minute resolution; ENTSO-E's deadline is 30 minutes after each minute
    grain: One row per minute, area and direction code
  landscape: market
  what_it_is: >-
    ENTSO-E's open loop area control error, an area's total imbalance volume averaged over each
    minute in MW, sent unsigned with a direction code, `A01` Up or `A02` Down. gridflow requests
    six areas: for 1 to 5 August 2026, FR, NL and BE sent values, FR's changing only on
    quarter-hours; GB, DE-LU and IE-SEM answered with no matching data.
  how_used:
    - Minute by minute system stress in NL and BE, before settled imbalance figures.
    - A short-horizon feature for imbalance price and balancing activation models.
    - How often an area's imbalance changes direction within an hour.
  caveat: ENTSO-E does not say whether direction Up or Down means excess or deficit.
  chart:
    type: line
    silver: entsoe/current_balancing_state
    time: timestamp_utc
    value: quantity_mw
    filter:
      - {column: area_code, op: eq, value: "10YBE\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D2"}
      - {column: timestamp_utc, op: ge, value: "2026-08-01T12:00:00Z"}
      - {column: timestamp_utc, op: lt, value: "2026-08-01T18:00:00Z"}
    group: direction
    group_map: {A01: up, A02: down}
    series_order: [up, down]
    aggregation: last
    window: {start: "2026-08-01", end: "2026-08-01"}
    unit: MW
  chart_view:
    title: Belgian imbalance by the minute, 1 August 2026
    caption: >-
      Silver `entsoe/current_balancing_state`, MW as sent, Belgian area, one value per minute,
      12:00 to 18:00 UTC on 1 August 2026. Each minute carries one direction code, so each line
      breaks where the other runs.
    alt: >-
      Line chart of MW per minute for the Belgian area from entsoe/current_balancing_state, 12:00
      to 18:00 UTC on 1 August 2026, one line per direction code, each broken where the other
      runs. Down holds most of the window, all of 16:00 to 17:00, and peaks at 571 MW at 16:45. Up
      holds most of 13:00 to 14:00 and peaks at 401 MW at 14:18. At their lowest, Up is 1.3 MW and
      Down 0.9 MW.
    x_label: UTC time on 1 August 2026
    key:
      - {series: up, label: Up, codes: A01, paint: petrol}
      - {series: down, label: Down, codes: A02, paint: clay}
  raw_feed:
    note: >-
      One GET per area per UTC day, six areas. An area with no data gets an acknowledgement
      with reason 999, not a document. `gridflow transform` makes one row per minute.
    requests:
      - "GET https://web-api.tp.entsoe.eu/api?documentType=A86&periodStart=202608010000&periodEnd=202608020000&area_Domain=10YBE\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D2&businessType=B33&securityToken=$ENTSOE_API_KEY"
    commands:
      - {run: gridflow ingest entsoe current_balancing_state --start 2026-08-01 --end 2026-08-02, comment: "bronze; end date excluded"}
      - {run: gridflow transform entsoe current_balancing_state --start 2026-08-01 --end 2026-08-01, comment: "bronze to silver; end included"}
  record:
    select:
      filter:
        - {column: area_code, op: eq, value: "10YBE\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D2"}
        - {column: timestamp_utc, op: ge, value: "2026-08-01T12:56:00Z"}
        - {column: timestamp_utc, op: le, value: "2026-08-01T13:03:00Z"}
      order_by: [timestamp_utc]
      columns: [timestamp_utc, area_code, business_type, direction, quantity_mw, resolution, published_at]
    key: [timestamp_utc, area_code, business_type, direction]
    caption: "The Belgian area, eight minutes from 12:56 UTC on 1 August 2026, as the direction changes."
    fields:
      timestamp_utc: "Minute start, UTC: period start plus (position minus one) minutes"
      area_code: "The area's EIC, read from the document's `area_Domain.mRID`"
      business_type: "Always `B33`, ENTSO-E's area control error"
      direction: "`flowDirection.direction`: `A01` Up or `A02` Down, from the point's series"
      quantity_mw: "MW as sent (`MAW`), unsigned; a declared point repeats each minute until the next"
      resolution: "Point spacing as sent: `PT1M`"
      published_at: "Response `createdDateTime`, UTC: a fetch-time stamp, within seconds of gridflow's request"
  notebook:
    lead: >-
      Returns a pandas DataFrame from `silver_entsoe_current_balancing_state`, filtered on
      `timestamp_utc` with both ends included. Lineage columns are dropped and rows come ordered by
      `timestamp_utc` only, so sort before pivoting.
    cells:
      - |
        df = data.entsoe.query("current_balancing_state", "2026-08-01", "2026-08-01")
        df["timestamp_utc"] = df["timestamp_utc"].dt.tz_convert("UTC")
        df = df.sort_values(["area_code", "timestamp_utc"])
      - df[["timestamp_utc", "area_code", "direction", "quantity_mw"]].head(8)
      - |
        be = df[df["area_code"].str.startswith("10YBE")]
        by_direction = be.pivot(index="timestamp_utc", columns="direction", values="quantity_mw")
        by_direction.between_time("12:00", "17:59")[["A01", "A02"]].plot(ylabel="MW", color=["#155A6E", "#C77E3C"], figsize=(8, 3.5))
    needs: 1 August 2026
    plot_alt: >-
      Line plot of quantity_mw for the Belgian area, 12:00 to 18:00 UTC on 1 August 2026, one line
      per direction (A01, A02), each broken where the other runs. A01 runs through most of 13:00 to
      14:00 and reaches about 400 MW; A02 holds most of the afternoon and peaks near 570 MW around
      16:45.
  related:
    - {dataset: entsoe/procured_balancing_capacity, note: "Balancing capacity procured in the same areas, by direction"}
    - {dataset: entsoe/balancing-energy-bids, note: "Balancing energy bids, also split by direction code"}
    - {dataset: entsoe/cross_border_flows, note: "Physical flows on GB's borders with four of these areas"}
    - {dataset: elexon/system_prices, note: "GB's net imbalance volume per half hour, from Elexon instead"}
---

# ENTSO-E — Current balancing state (A86 / B33)

## Overview

ENTSO-E's definition (Transparency Platform knowledge base, "Current
Balancing State [GL EB 12.3.A]", updated 2025-08-26): the total
imbalance volume of an imbalance area, i.e. the open loop area control
error, averaged over each minute, in MW, with a state of Excess, Deficit
or Balanced. "Deficit is equivalent to negative imbalance while excess is
equivalent to positive imbalance" (GL EB article 54.6). Published with
minute resolution, 30 minutes after the end of the minute described;
updates are "not foreseen".

The response does not send a signed number. Each TimeSeries carries an
unsigned `quantity` (unit `MAW`) and a `flowDirection.direction`: ENTSO-E's
XML example labels `A01` Up, `A02` Down, `A03` Symmetric
(gitlab.entsoe.eu/transparency/xml-examples, "Current balancing state
[GL EB 12.3.A] - XSD4:1.xml"). Neither source says which direction is
excess and which is deficit. (Corrected 2026-09-29: this paragraph
previously said "positive = system short". Silver keeps the unsigned
value and the direction code in `direction`, and signs nothing.)

Document type **A86** is shared with `imbalance_volume`. The two
datasets distinguish themselves only by the `businessType` query
parameter — `B33` (this dataset; ENTSO-E's code list names it "Area control error")
versus `A19` (settled imbalance volumes, see
[imbalance_volume.md](./imbalance_volume.md)). Always specify
`businessType` when calling A86 or you will get an `Acknowledgement`
back with reason 999.

This is the dataset to use for: short-horizon imbalance forecasts,
real-time alerting on system stress, and as a feature in BM activation
likelihood models. Use [imbalance_volume.md](./imbalance_volume.md)
when you need the settled (after-the-fact) volume per settlement period.

→ Domain concepts:
  [Imbalance pricing](../../../20-domain/markets/imbalance-price.md)
  [Settlement period](../../../20-domain/concepts/settlement-period.md)

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://web-api.tp.entsoe.eu` |
| Path             | `/api` |
| Method           | GET |
| Auth             | Query param `securityToken=<ENTSOE_API_KEY>` (header auth NOT supported) |
| Rate limit       | Vendor-published: not documented. Project default: 1 req/s. ENTSOE rejects bursts even when calls are sequential — see `_throttle_request`. |
| Pagination       | None for A86. The endpoint returns one Balancing_MarketDocument per call. |
| Historical depth | Not stated by ENTSO-E: the TP knowledge base article for GL EB 12.3.A (read 2026-10-24) gives none. GB control area has no published data (see EMPTY note below). |
| Publication lag  | Vendor deadline: 30 minutes after the end of the minute described; minute resolution (TP knowledge base, GL EB 12.3.A). |
| Response format  | XML (`Balancing_MarketDocument` urn:iec62325.351:tc57wg16:451-6) |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `documentType` | string (A-code) | Yes | Fixed `A86` | `A86` |
| `businessType` | string (B-code) | Yes | Fixed `B33` (current balancing state). Without this you get reason-999 even on data-rich areas — A86 is shared with imbalance_volume which uses `A19`. | `B33` |
| `area_Domain` | string (EIC) | Yes | Control area EIC. H8 spec uses `area_Domain` here, not `controlArea_Domain`. | `10YGB----------A` |
| `periodStart` | string (yyyyMMddHHmm UTC) | Yes | Window start, intra-day resolution. | `202605070000` |
| `periodEnd` | string (yyyyMMddHHmm UTC) | Yes | Window end, exclusive. gridflow sends one whole UTC day per call (`day_subwindows`, `connectors/entsoe/client.py:161-167`), e.g. `202608010000` to `202608020000`. | `202605071400` |
| `securityToken` | string (UUID) | Yes | API key from `ENTSOE_API_KEY`. | `<UUID>` |

ENTSOE tuple: `(documentType=A86, processType=n/a, businessType=B33, area-param-name=area_Domain)`.

### Working curl example

```bash
curl --ssl-no-revoke -fsS -H "Accept: application/xml" \
  "https://web-api.tp.entsoe.eu/api?documentType=A86&businessType=B33&area_Domain=10YGB----------A&periodStart=202605070000&periodEnd=202605071400&securityToken=${ENTSOE_API_KEY}" \
  -o /tmp/entsoe-current_balancing_state.xml \
  -w "HTTP %{http_code} | %{size_download} bytes\n"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsoe/current_balancing_state/<year>/<month>/<day>/raw_<uuid>.xml`
**Format**: Raw XML (`Balancing_MarketDocument`), as-received. Immutable — never modified after write.
**Granularity**: One file per (zone, UTC day). The connector loops `DEFAULT_ZONES` (GB, FR, NL, BE, DE-LU, IE-SEM; `endpoints.py:395`, `client.py:249`), so six files per day, including code-999 acknowledgements.

### Bronze sample

From `tests/fixtures/entsoe/current_balancing_state_gb.xml` (a hand-made fixture, not a vendor response). Real responses differ: `area_Domain.mRID` sits at document level, not in the TimeSeries; each TimeSeries carries `flowDirection.direction`, `quantity_Measure_Unit.name` `MAW` and `curveType` `A03`; the resolution is `PT1M`; quantities are unsigned (bronze FR/NL/BE responses for 1 to 5 Aug 2026, and ENTSO-E's XML example):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Balancing_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:balancingdocument:4:0">
  <mRID>fixture-current-balancing-state-gb-20240115</mRID>
  <revisionNumber>1</revisionNumber>
  <type>A86</type>
  <createdDateTime>2024-01-14T12:00:00Z</createdDateTime>
  <TimeSeries>
    <mRID>state-1</mRID>
    <businessType>B33</businessType>
    <area_Domain.mRID codingScheme="A01">10YGB----------A</area_Domain.mRID>
    <Period>
      <timeInterval>
        <start>2024-01-15T00:00Z</start>
        <end>2024-01-15T02:00Z</end>
      </timeInterval>
      <resolution>PT60M</resolution>
      <Point><position>1</position><quantity>125</quantity></Point>
      <Point><position>2</position><quantity>-75</quantity></Point>
    </Period>
  </TimeSeries>
</Balancing_MarketDocument>
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsoe/current_balancing_state/year=YYYY/month=MM/current_balancing_state_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsoe.h8_balancing.CurrentBalancingStateTransformer`
**Pydantic schema**: `gridflow.schemas.entsoe.EntsoeBalancingState`
**Dedup key**: `(timestamp_utc, area_code, business_type, direction)`, keep last (`silver/entsoe/h8_balancing.py`, `CurrentBalancingStateTransformer.unique_subset`, `DATASET_VERSION` 2.0.0). Only the latest fetch run of each request (zone and day) is read (`LATEST_FETCH_PER_REQUEST`, `_latest_fetch_files`).
**Point-in-time field**: `published_at`, the response's `createdDateTime`: a fetch-time stamp, within seconds of the request, not a vendor publication time (`silver/entsoe/_published_at.py`; ENTSO-E sets `createdDateTime` when it builds the response)

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `timestamp_utc` | `datetime[UTC]` | No | derived (Period.timeInterval.start + (position - 1) * resolution, `parsers.py` `_point_timestamp`) | Validator rejects naive datetimes. `PT1M` maps to one minute in `_RESOLUTION_MAP`. The documents are A03 curves, so the parser forward-fills each declared point to every minute until the next one or the Period end: one row per minute. |
| `area_code` | `str` | No | `area_Domain.mRID` | Renamed from `area_domain` by the transformer. Real A86 responses send it once at document level; the parser falls back to that when a TimeSeries has none (`parsers.py`, `document_area_domain`). |
| `quantity_mw` | `float` | No | `<quantity>` per Point | Unsigned magnitude in MW (`MAW`), as sent; a forward-filled minute repeats the last declared point. |
| `direction` | `str` | No | `flowDirection.direction` of the point's TimeSeries | `A01` Up or `A02` Down (ENTSO-E's XML example); part of the key. Each series is one block with one direction, so FR, NL and BE rows hold one direction per area and minute (1 to 5 Aug 2026). |
| `business_type` | `str` | No | `<businessType>` | Default "B33" in canonical. Always `B33` for this dataset. |
| `resolution` | `str` | No | `<resolution>` (raw ISO duration) | Default "" in canonical. Emitted verbatim as the ISO-8601 duration code; `PT1M` in every response held (FR, NL, BE, 1 to 5 Aug 2026). |
| `published_at` | `datetime[UTC]` | Yes | root `createdDateTime` | Fetch-time stamp, within seconds of the request. |
| `data_provider` | `str` | No | derived | Default "entsoe" in canonical. |
| `ingested_at` | `datetime` | Yes | derived (now(UTC) at transform) | Nullable (datetime or None). |

### Silver sample

Two real silver rows (Belgian area, 1 Aug 2026, `DATASET_VERSION` 2.0.0; lineage columns omitted). The direction changes between consecutive minutes; neither value is signed.

```python
[
    {
        "timestamp_utc": datetime(2026, 8, 1, 12, 57, tzinfo=UTC),
        "area_code": "10YBE----------2",
        "quantity_mw": 11.958,
        "direction": "A02",
        "business_type": "B33",
        "resolution": "PT1M",
        "published_at": datetime(2026, 8, 16, 14, 11, 4, tzinfo=UTC),
        "data_provider": "entsoe",
    },
    {
        "timestamp_utc": datetime(2026, 8, 1, 12, 58, tzinfo=UTC),
        "area_code": "10YBE----------2",
        "quantity_mw": 6.185,
        "direction": "A01",
        "business_type": "B33",
        "resolution": "PT1M",
        "published_at": datetime(2026, 8, 16, 14, 11, 4, tzinfo=UTC),
        "data_provider": "entsoe",
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **GB returns EMPTY.** Live curl on 2026-05-08 with `area_Domain=10YGB----------A` and a 14h window returns HTTP 200 with `Acknowledgement_MarketDocument` reason 999: `No matching data found for Data item CURRENT_BALANCING_STATE_R3 [12.3.A] (10YGB----------A)...`. ENTSOE has reduced GB-area coverage post-Brexit; National Grid ESO publishes equivalent data via Elexon BMRS instead. The whole-UTC-day calls for 1 to 5 Aug 2026 got the same code-999 answer for GB, DE-LU (`10Y1001A1001A82H`) and IE-SEM (`10Y1001A1001A59C`); FR, NL and BE returned data.
- **A86 + businessType is mandatory.** Submitting A86 without `businessType` returns reason 999. This is the same documentType used by `imbalance_volume` (with `businessType=A19`). Cross-link: see [imbalance_volume.md](./imbalance_volume.md).
- **Window length.** gridflow sends one whole UTC day per call, not an intra-day window (`connectors/entsoe/client.py`, `day_subwindows`). (Corrected 2026-09-29: this bullet previously said an intra-day window is required.)
- **No DocStatus on TimeSeries.** Unlike outage feeds, A86 carries no per-TimeSeries status. Each TimeSeries has an `mRID` that is only a sequence number (`1`, `2`, ...); the document `mRID` and `revisionNumber` at the root are the only versioning artefacts.
- **Sign is a direction code, not a signed number.** ENTSO-E defines deficit as negative imbalance and excess as positive (GL EB 54.6), but the response sends unsigned quantities with `flowDirection.direction` `A01` (Up) or `A02` (Down), and no vendor source held here maps Up/Down to excess/deficit. Do not borrow `imbalance_volume`'s `A01` long / `A02` short mapping without evidence.
- **Declared points differ by area; silver repeats them per minute.** The A03 forward-fill gives every area one row per minute, but in the documents for 1 to 5 Aug 2026 FR declares a point every 15 minutes (96 a day), so its silver minutes repeat each quarter-hour's value, while NL and BE declare all 1,440 minutes. Silver does not mark which minutes were declared. All documents carry `process.processType` `A16` at the root; silver does not keep it.

---

## Implementation delta

- **Area parameter:** docs/code use `area_Domain`, **not** `controlArea_Domain` as suggested in the V1-PLAN-B4 orchestrator instructions. The H8 balancing extension spec (Article 12.3 of GL EB) uses `area_Domain` for A86/A24/A15. The fixture file at `tests/fixtures/entsoe/current_balancing_state_gb.xml` confirms this — the response carries `<area_Domain.mRID>`. The orchestrator instruction was incorrect; code is right.
- **A86 dual mapping:** This dataset shares documentType A86 with `imbalance_volume` — they differ only by `businessType` (B33 here, A19 there). See [imbalance_volume.md](./imbalance_volume.md) for the settled-volume counterpart.
- **`processType` not specified:** A86/B33 has no `processType` in `endpoints.py` (`process_type=None`). The ENTSOE API guide does not list a process type for B33. Confirmed by successful live (HTTP 200) call without `processType`.
- **`controlArea_Domain` mention in entsoe README:** The current vendor README does not yet document the H8 area_Domain pattern. Will be addressed by the V1-PLAN-B5 aggregate plan.

---

## Modelling notes

- Useful as a **leading indicator** for imbalance price direction. Models that predict period-end imbalance volume / price benefit from A86 features sampled at minute resolution within the period.
- Use as a feature for: BM activation likelihood, imbalance price short-horizon regression, NIV (Net Imbalance Volume) nowcast.
- Caveat for GB: since GB returns EMPTY here, equivalent data must be sourced from Elexon (`freq`, `disbsad`, `imbalngc` family). Cross-area comparisons require pulling from EU-country control areas where A86/B33 is published (e.g. FR, NL, BE; DE-LU returned code 999 for 1 to 5 Aug 2026).

---

## Links

- [Official API docs](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.pdf) — Section 17 (Balancing) and 12.3.A
- [TP knowledge base: Current Balancing State [GL EB 12.3.A]](https://transparencyplatform.zendesk.com/hc/en-us/articles/12824861339924-Current-Balancing-State-GL-EB-12-3-A): definition, unit, excess/deficit wording, deadline
- [ENTSO-E XML example](https://gitlab.entsoe.eu/transparency/xml-examples/-/blob/main/Balancing/Current%20balancing%20state%20[GL%20EB%2012.3.A]%20-%20XSD4:1.xml): `B33` Area control error; `A01` Up, `A02` Down, `A03` Symmetric
- `src/gridflow/connectors/entsoe/client.py`
- `src/gridflow/connectors/entsoe/endpoints.py` — see `current_balancing_state` entry
- `src/gridflow/silver/entsoe/h8_balancing.py`
- `src/gridflow/schemas/entsoe.py` — `EntsoeBalancingState`
- `tests/fixtures/entsoe/current_balancing_state_gb.xml`
- [Imbalance volume (A86 / A19)](./imbalance_volume.md)
