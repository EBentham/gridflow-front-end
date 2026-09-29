---
source: elexon
dataset_key: boal
vendor: Elexon BMRS
last_verified: 2026-05-21
layer_coverage: bronze, silver
v2_fix_history:
  - date: 2026-05-20
    phase: gridflow-G5-W2.1
    pr: https://github.com/EBentham/gridflow/pull/7
    change: silver transformer now casts `acceptance_time` from str to UTC datetime; `bid_offer_acceptance_number` dropped from ElexonBOAL schema (duplicated `acceptance_number`)
page:
  title: Bid-offer acceptance levels
  summary: >-
    Each bid or offer the GB system operator accepted in the Balancing Mechanism, with its BM unit
    and MW levels.
  facts:
    vendor: Elexon BMRS, dataset BOALF
    cadence: No fixed interval; records follow each acceptance issued
    grain: One row per settlement period, BM unit and acceptance
  landscape: market
  what_it_is: >-
    Elexon sends each acceptance as segments, each with the unit's MW operating level at its start
    and end time. A level is where the unit runs, not a change, so levels do not add up.
    Silver keeps one segment per acceptance and settlement period, the last one received, and
    drops the segment times, so the full profile cannot be rebuilt.
  how_used:
    - Counting accepted actions per hour, and how many the system operator flagged.
    - Which BM units were redispatched, joined to the unit register on `bm_unit_id`.
    - Dispatch features for a BM unit model, beside that unit's physical notifications.
  chart:
    type: stacked-area
    silver: elexon/boal
    time: acceptance_time
    dedup: {on: [bm_unit_id, acceptance_number, acceptance_time], order_by: timestamp_utc}
    group: so_flag
    group_map: {"true": so_flagged, "false": not_flagged}
    series_order: [not_flagged, so_flagged]
    aggregation: count
    time_bucket: 1h
    window: {start: "2026-09-14", end: "2026-09-20"}
    unit: count
  chart_view:
    title: Acceptances per hour, 14 to 20 September 2026
    caption: >-
      Silver `elexon/boal`, a count of acceptances (not MW) in each hour of acceptance time, UTC,
      14 to 20 September 2026. An acceptance counts once however many rows it has; no level is
      summed.
    alt: >-
      Stacked area chart from elexon/boal of acceptances per hour of acceptance time, UTC, 14 to 20
      September 2026: acceptances not SO-flagged at the bottom, SO-flagged on top. Hourly totals
      run from 80 at 22:00 on the 15th to 1,304 at 15:00 on the 19th. SO-flagged acceptances are 0
      to 66 an hour on the 14th, peak at 283 at 18:00 on the 19th, and reach at most 188 an hour on
      the 20th.
    x_label: acceptance time, UTC, per hour
    key:
      - {series: so_flagged, label: SO-flagged, codes: "so_flag true", paint: hatch-cross, note: "Elexon: the SO flags an acceptance it believes a transmission constraint may affect."}
      - {series: not_flagged, label: Not flagged, codes: "so_flag false", paint: hatch-lines}
  raw_feed:
    note: >-
      From the Elexon Insights API in 24-hour `from`/`to` windows. Replies fetched for this page held
      midnight-UTC segments in both adjacent windows; silver repeats them. Summer settlement days start 23:00 UTC.
    requests:
      - "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/BOALF?from=2026-09-13T00:00:00Z&to=2026-09-14T00:00:00Z&page=1"
    commands:
      - {run: gridflow ingest elexon boal --start 2026-09-13 --end 2026-09-22, comment: "bronze; the end is exclusive"}
      - {run: gridflow transform elexon boal --start 2026-09-13 --end 2026-09-21, comment: bronze to silver}
  record:
    select:
      filter:
        - {column: settlement_date, op: eq, value: "2026-09-19"}
        - {column: bm_unit_id, op: eq, value: T_COALB-2}
        - {column: settlement_period, op: ge, value: 36}
        - {column: settlement_period, op: le, value: 38}
      order_by: [settlement_period, acceptance_number]
    key: [settlement_date, settlement_period, bm_unit_id, acceptance_number]
    caption: "Unit `T_COALB-2`, 2026-09-19, periods 36 to 38: acceptances 991, 993 and 994 span two periods."
    fields:
      settlement_date: GB settlement date, as Elexon labels it
      settlement_period: "Half-hour the kept segment starts in (`settlementPeriodFrom`)"
      timestamp_utc: "Start of that settlement period, not the segment's own start time"
      bm_unit_id: BM unit id, casing as sent
      acceptance_number: "Elexon's acceptance number; one acceptance can span several periods"
      acceptance_time: When the system operator issued the acceptance, UTC
      deem_flag: "Elexon's deemed bid-offer flag (`deemedBoFlag`), as sent"
      so_flag: True when the SO believes a transmission constraint may affect the acceptance
      stor_flag: "Elexon's STOR flag (`storFlag`), as sent"
      rr_flag: "Elexon's replacement reserve flag (`rrFlag`), as sent"
      bid_offer_level_from: MW operating level at the start of the kept segment
      bid_offer_level_to: MW operating level at the end of the kept segment
  notebook:
    lead: >-
      Returns a pandas DataFrame from the DuckDB relation `silver_elexon_boal`, filtered on
      `settlement_date` with both ends included. Lineage columns are dropped.
    cells:
      - df = data.elexon.query("boal", "2026-09-19", "2026-09-19")
      - df[["settlement_period", "bm_unit_id", "acceptance_number", "bid_offer_level_from", "bid_offer_level_to"]].head()
      - |
        acc = df.drop_duplicates(["bm_unit_id", "acceptance_number"])
        acc.bm_unit_id.value_counts().head(10).sort_values().plot.barh(
            xlabel="acceptances", color="#155A6E", figsize=(8, 3.5))
    needs: 13 to 21 September 2026
    plot_alt: >-
      Horizontal bar chart of the ten BM units with the most acceptances on settlement date 19
      September 2026, each acceptance counted once: `E_THMRB-1` leads with 201, then `E_WHTBB-1`
      199 and `E_NEWPB-1` 187, down to `E_CHAPB-1` with 143.
  related:
    - {dataset: elexon/pn, note: "Each unit's notified level, which an acceptance moves it from"}
    - {dataset: elexon/bmunits_reference, note: "Fuel type, capacity and company behind each `bm_unit_id`"}
    - {dataset: elexon/disbsad, note: "Balancing actions taken outside the Balancing Mechanism, also SO-flagged"}
    - {dataset: elexon/system_prices, note: The imbalance prices these accepted bids and offers feed into}
---

# Elexon - Bid Offer Acceptance Level Flagged (`BOALF`)

## Overview

Bid Offer Acceptance Levels Flagged (BOALF) — every accepted bid or offer instruction issued by the National Energy System Operator (NESO; the name NESO uses for itself at https://www.neso.energy/, checked 2026-09-29) to a Balancing Mechanism Unit. Each acceptance carries level-from / level-to MW values that fully describe how the unit's output was redispatched. BOALF is the row-level audit trail behind the headline BSC settlement numbers and is a primary feature for any BM-unit dispatch model.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://data.elexon.co.uk/bmrs/api/v1` |
| Path             | `/datasets/BOALF` |
| Method           | GET |
| Auth             | None required for tested endpoints (2026-05-08). Some endpoints accept an `apikey` header (env: `ELEXON_API_KEY`); registration at https://www.elexonportal.co.uk/. |
| Rate limit       | Vendor-published: not stated. Project default 2 req/sec (asyncio.Semaphore); verified safe 2026-05-08. |
| Pagination       | Connector handles via `page=N` query param; stops when `page >= total_pages`. Reference endpoints (`/reference/bmunits/all`) are not paginated. |
| Historical depth | Several years. |
| Publication lag  | Near real-time as acceptance instructions are issued. |
| Response format  | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `from` | string | Yes | The "from" start time or settlement date for the filter. | `2026-05-06T00:00Z` |
| `to` | string | Yes | The "to" start time or settlement date for the filter. | `2026-05-06T03:00Z` |
| `settlementPeriodFrom` | integer | No | The "from" settlement period for the filter. This should be an integer from 1-50 inclusive. | `1` |
| `settlementPeriodTo` | integer | No | The "to" settlement period for the filter. This should be an integer from 1-50 inclusive. | `48` |
| `bmUnit` | array | No | The BM units to query. Add each unit separately. If no BM unit is selected all BM units will be displayed. | `T_DRAXX-1` |
| `format` | string | No | Response data format. Use json/xml to include metadata. | `json` |

### Working curl example

```bash
# Replace <ELEXON_API_KEY> with your env var if you choose to send one (Elexon endpoints
# tested 2026-05-08 do NOT require a key; set anyway for vendor courtesy).
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://data.elexon.co.uk/bmrs/api/v1/datasets/BOALF?from=2026-05-06T00:00Z&to=2026-05-06T03:00Z&format=json" \
  -o "/tmp/elexon-boal.json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/elexon/boal/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per API call (paginated requests append additional files for the same date partition).

### Bronze sample

Captured live 2026-05-08 from the https://data.elexon.co.uk/bmrs/api/v1/datasets/BOALF?from=2026-05-06T00:00Z&to=2026-05-06T03:00Z&format=json:

```json
{
  "data": [
    {
      "dataset": "BOALF",
      "settlementDate": "2026-05-06",
      "settlementPeriodFrom": 9,
      "settlementPeriodTo": 10,
      "timeFrom": "2026-05-06T03:00:00Z",
      "timeTo": "2026-05-06T03:30:00Z",
      "levelFrom": 480,
      "levelTo": 480,
      "acceptanceNumber": 217257,
      "acceptanceTime": "2026-05-06T02:31:00Z",
      "deemedBoFlag": false,
      "soFlag": true,
      "amendmentFlag": "ORI",
      "storFlag": false,
      "rrFlag": false,
      "nationalGridBmUnit": "MRWD-1",
      "bmUnit": "T_MRWD-1"
    },
    {
      "dataset": "BOALF",
      "settlementDate": "2026-05-06",
      "settlementPeriodFrom": 9,
      "settlementPeriodTo": 9,
      "timeFrom": "2026-05-06T03:00:00Z",
      "timeTo": "2026-05-06T03:14:00Z",
      "levelFrom": -2,
      "levelTo": -2,
      "acceptanceNumber": 1170,
      "acceptanceTime": "2026-05-06T02:46:00Z",
      "deemedBoFlag": false,
      "soFlag": false,
      "amendmentFlag": "ORI",
      "storFlag": false,
      "rrFlag": false,
      "nationalGridBmUnit": "AG-DUKP08",
      "bmUnit": "2__DUKPR008"
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/elexon/boal/year=YYYY/month=MM/boal_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.elexon.boal.BOALTransformer`
**Pydantic schema**: `gridflow.schemas.elexon.ElexonBOAL`
**Dedup key**: `(settlement_date, settlement_period, bm_unit_id, acceptance_number)`, `keep="last"` within one bronze day (`silver/elexon/boal.py:120-123`)
**Point-in-time field**: `acceptance_time`

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `settlement_date` | `date` | No | `settlementDate` | Settlement date (BST/GMT calendar). |
| `settlement_period` | `int` | No | `settlementPeriod` or `settlementPeriodFrom` | 1..50 (DST: 46 spring, 50 autumn). |
| `timestamp_utc` | `datetime[UTC]` | No | _derived_ | Derived from (settlement_date, settlement_period) via `utils/time.settlement_period_to_utc`. |
| `bm_unit_id` | `str` | No | `bmUnit` | BM Unit identifier — preserve raw casing. |
| `acceptance_number` | `int` | Yes | `acceptanceNumber` | Acceptance instruction number. |
| `acceptance_time` | `datetime[UTC]` | Yes | `acceptanceTime` | Time the acceptance was issued. G5-W2.1: now cast str→UTC datetime in the transformer; previously emitted as raw string and the acceptance-test caught the schema drift. |
| `deem_flag` | `bool` | No | `deemedBoFlag` | Deemed-bid/offer flag. |
| `so_flag` | `bool` | No | `soFlag` | System Operator flag. Elexon, Imbalance Pricing Guidance v15.0 (25 June 2020), section 3: "For BOAs, the SO flags when it believes the BOA may be impacted by a transmission constraint." |
| `stor_flag` | `bool` | No | `storProviderFlag` or `storFlag` | STOR flag. |
| `rr_flag` | `bool` | No | `rrFlag` | Replacement Reserve flag. |
| `bid_offer_level_from` | `float` | Yes | `levelFrom` | MW. Level of operation at the segment's start (Elexon BSC glossary, "Bid-Offer Acceptance Level": MW levels at the start and end, with start and end times). |
| `bid_offer_level_to` | `float` | Yes | `levelTo` | MW. |
| `data_provider` | `str` | No | _derived_ | Default `"elexon"`. |
| `ingested_at` | `datetime[UTC]` | Yes | _derived_ | When the silver transform ran (`silver/elexon/boal.py:125-129`). |

### Silver sample

```python
[
    {
        "settlement_date": "2026-05-06",
        "settlement_period": 9,
        "timestamp_utc": "2026-05-06T03:00:00+00:00",
        "bm_unit_id": "T_MRWD-1",
        "acceptance_number": 217257,
        "acceptance_time": "2026-05-06T02:31:00Z",
        "deem_flag": false,
        "so_flag": true,
        "stor_flag": false,
        "rr_flag": false,
        "bid_offer_level_from": 480,
        "bid_offer_level_to": 480,
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

- **BM Unit IDs**: keep raw casing (e.g. `T_DRAXX-1`); do NOT normalise.
- **`settlementPeriodFrom`/`settlementPeriodTo`**: a single acceptance can span multiple periods. Silver maps `settlementPeriodFrom → settlement_period` (loses span info). Each raw record is one segment of an acceptance; silver drops `timeFrom`, `timeTo`, `settlementPeriodTo`, `amendmentFlag` and `nationalGridBmUnit` (all but `settlementPeriodTo` renamed at `silver/elexon/boal.py:74-77`; all five absent from `output_cols` at `boal.py:133-148`), and the dedup at `boal.py:120-123` keeps one segment per (date, period, unit, acceptance): the last in response order.
- **Midnight boundary (measured 2026-09-29 on the 2026-09-19 bronze response, not vendor-documented)**: the `from`/`to` window returned segments with `timeFrom` from 00:00 to 24:00 UTC inclusive, so a segment starting exactly at midnight is in two adjacent bronze days and two silver files with the same key. Checked 2026-09-29 over the silver built from the responses fetched 2026-08-16 (1 to 5 August) and 2026-09-26 (13 to 21 September 2026): 539 keys (1,078 rows) repeat across two adjacent files, all at `timestamp_utc` 00:00 UTC, with identical levels. Elexon does not document this; it is what these responses held.
- **Acceptance number** is non-unique across (date, BM unit) — required for proper deduplication.

---

## Implementation delta

- **Path rename**: vault `endpoints.md` (pre-V1) listed path as `/datasets/BOAL`; docs and code use `/datasets/BOALF` (vendor renamed BOAL → BOALF). Vault page now corrected. Old `bod` and the original `boal` are in `EXCLUDED_ENDPOINTS`.
- **Param style**: docs require `from`/`to` (NOT `publishDateTimeFrom/To`); code uses `from_param="from", to_param="to"` — matches docs.

### V2-FIX changelog

- **2026-05-20 — gridflow G5-W2.1 (PR #7)**: silver transformer now casts
  `acceptance_time` from the raw string the API returns into a UTC-aware
  datetime so the column matches the schema's `datetime[UTC] | None`
  declaration. Pre-G5 the parametrised schema-alignment acceptance test
  caught the type drift. Same commit also dropped the duplicate
  `bid_offer_acceptance_number` field from `ElexonBOAL`
  (was a stale duplicate of `acceptance_number`).

---

## Modelling notes

TODO

---

## Links

- [Official API docs (Swagger UI)](https://bmrs.elexon.co.uk/api-documentation)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/elexon/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/elexon/boal.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/elexon.py)
- Gold view/builder
- [Domain: GB Balancing Mechanism](../../../20-domain/markets/gb-balancing-mechanism.md)
