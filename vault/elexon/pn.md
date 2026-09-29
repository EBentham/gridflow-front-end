---
source: elexon
dataset_key: pn
vendor: Elexon BMRS
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Physical notifications by BM unit
  summary: >-
    Each Balancing Mechanism unit's notified MW level for every GB settlement period: its expected
    export or import before any acceptances.
  facts:
    vendor: Elexon BMRS, dataset PN
    cadence: Every 30 minutes
    grain: One row per settlement period and BM unit, one segment kept
  landscape: market
  what_it_is: >-
    The BSC defines a physical notification as a unit's expected export or import in each
    settlement period, absent any acceptances. Elexon sends each unit's period as segments: a
    start and end time, with a MW level at each. Silver keeps one segment per unit and period,
    the last one received, and drops the times, losing moves inside a period.
  how_used:
    - The baseline that each accepted bid or offer moves a unit away from.
    - Start, stop and part-load patterns of flexible units, period by period.
    - Expected running by unit, joined to the register for fuel type.
  chart:
    type: line
    silver: elexon/pn
    time: timestamp_utc
    value: level_from
    filter:
      - {column: settlement_date, op: ge, value: "2026-09-16"}
      - {column: settlement_date, op: le, value: "2026-09-22"}
      - {column: bm_unit_id, op: in, value: [T_PEMB-11, T_DINO-5, T_SGRWO-6]}
    group: bm_unit_id
    group_map:
      T_PEMB-11: pembroke
      T_DINO-5: dinorwig
      T_SGRWO-6: seagreen
    series_order: [pembroke, dinorwig, seagreen]
    aggregation: last
    window: {start: "2026-09-15", end: "2026-09-22"}
    unit: MW
  chart_view:
    title: Three units' notified levels, 16 to 22 September 2026
    caption: >-
      Silver `elexon/pn`, MW, for three BM units, every half-hour of settlement dates 16 to 22
      September 2026: `level_from`, one row per unit and period, nothing summed. Here each kept
      segment starts its period; moves inside a half-hour are not shown.
    alt: >-
      Line chart of level_from in MW from elexon/pn for three BM units, every half-hour of
      settlement dates 16 to 22 September 2026. Pembroke 11 runs near 430 on the 16th, sits at 0
      until it ramps up on the evening of the 20th, then runs between 219 and 435. Dinorwig 5 steps between 0,
      300 and stretches of import below zero, lowest -293 on the 18th. Seagreen 6 moves smoothly between 1
      and 354, highest on the 19th and 20th, and falls to 2 on the 22nd.
    x_label: settlement date; each starts at 23:00 UTC
    key:
      - {series: pembroke, label: Pembroke 11, codes: T_PEMB-11, paint: clay, note: "A CCGT unit, by the BM unit register's fuel type."}
      - {series: dinorwig, label: Dinorwig 5, codes: T_DINO-5, paint: petrol, note: "Pumped storage by the register. Negative is import, per the Grid Code (BC1)."}
      - {series: seagreen, label: Seagreen 6, codes: T_SGRWO-6, paint: horizon, note: "An offshore wind unit, by the register's fuel type."}
  raw_feed:
    note: >-
      From the Elexon Insights API, one call per settlement period of each date (46, 48 or 50).
      `gridflow ingest` writes each response to bronze; `gridflow transform` types it into silver.
    requests:
      - "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/PN?settlementDate=2026-09-20&settlementPeriod=1&page=1"
      - "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/PN?settlementDate=2026-09-20&settlementPeriod=48&page=1"
    commands:
      - {run: gridflow ingest elexon pn --start 2026-09-16 --end 2026-09-22, comment: "bronze; the end date is fetched"}
      - {run: gridflow transform elexon pn --start 2026-09-16 --end 2026-09-22, comment: bronze to silver}
  record:
    select:
      filter:
        - {column: settlement_date, op: eq, value: "2026-09-20"}
        - {column: settlement_period, op: eq, value: 10}
        - {column: bm_unit_id, op: in, value: [2__ALOND000, 2__BCMRO002, E_ARNKB-1, I_I2D-INCM1, T_DINO-5, T_HEYM27, T_PEMB-11, T_SGRWO-6]}
      order_by: [bm_unit_id]
      columns: [bm_unit_id, level_from, level_to]
    key: [settlement_date, settlement_period, bm_unit_id]
    caption: "Settlement date 2026-09-20, period 10: eight of its BM units, one kept segment each."
    fields:
      bm_unit_id: Elexon BM unit id; null for units sent without one, one kept per period
      level_from: MW level at the start of the kept segment
      level_to: MW level at the end of the kept segment, not of the period
      settlement_date: GB settlement date, as Elexon labels it
      settlement_period: Half-hour of the settlement day, 1 to 48; 46 or 50 on clock-change days
      timestamp_utc: Start of the half-hour, computed from settlement date and period
  notebook:
    lead: >-
      Returns a pandas DataFrame from the DuckDB relation `silver_elexon_pn`, filtered on
      `settlement_date` with both ends included. Lineage columns are dropped and rows come ordered
      by `settlement_date` only.
    cells:
      - df = data.elexon.query("pn", "2026-09-16", "2026-09-22")
      - |
        dino = df[df.bm_unit_id == "T_DINO-5"].sort_values("timestamp_utc")
        dino[dino.level_from != 0][["settlement_date", "settlement_period", "level_from", "level_to"]].head()
      - |
        dino.plot(x="timestamp_utc", y="level_from", ylabel="MW",
                  color="#155A6E", figsize=(8, 3.5), legend=False)
    needs: 16 to 22 September 2026
    plot_alt: >-
      Line plot of T_DINO-5 level_from in MW against timestamp_utc, 16 to 22 September 2026. It
      steps between 0, blocks at 300 on most evenings, and long stretches below zero (about -260
      to -293) through the 17th, 18th, 19th and 20th, with a short dip to -263 on the 22nd.
  related:
    - {dataset: elexon/boal, note: "Accepted bids and offers that move a unit off its notification"}
    - {dataset: elexon/bmunits_reference, note: "The register behind each `bm_unit_id`: name, fuel type, capacity"}
    - {dataset: elexon/uou2t14d, note: "Each unit's declared available output, 2 to 14 days ahead"}
    - {dataset: elexon/fuelhh, note: "Outturn by fuel type for the same settlement periods"}
---

# Elexon - Physical Notifications (`PN`)

## Overview

Physical Notifications — each BM unit's declared MW level intent for each settlement period. PN is the unit-level baseline against which BOAL acceptances are deviations and is the foundation of any BM-unit dispatch model. PN is fetched per (settlementDate, settlementPeriod) tuple.

BSC definition (Elexon glossary, https://www.elexon.co.uk/glossary/physical-notification/, read 2026-09-29): "a notification made by (or on behalf of) the Lead Party to the NETSO under the Grid Code as to the expected level of Export or Import, as at the Transmission System Boundary, in the absence of any Acceptances, at all times during that Settlement Period." The glossary entries for PN and Import do not state which sign is export and which import. The Grid Code does: BC1 Appendix 1, BC1.A.1.1 "Physical Notifications" (NESO Grid Code BC1, Issue 6 Revision 22, 02 April 2024, https://www.neso.energy/document/33851/download; the same text is in Issue 3, BETTA go-active, p. BC1-13, https://www.ofgem.gov.uk/sites/default/files/docs/2005/02/9753-5505_gcbc1_0.pdf) calls the PN "a series of MW figures and associated times", says "where it is proposed that the BM Unit will be importing, the Physical Notification is negative", and says "a linear interpolation will be assumed between the Physical Notification From and To levels".
---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://data.elexon.co.uk/bmrs/api/v1` |
| Path             | `/datasets/PN` |
| Method           | GET |
| Auth             | None required for tested endpoints (2026-05-08). Some endpoints accept an `apikey` header (env: `ELEXON_API_KEY`); registration at https://www.elexonportal.co.uk/. |
| Rate limit       | Vendor-published: not stated. Project default 2 req/sec (asyncio.Semaphore); verified safe 2026-05-08. |
| Pagination       | Connector handles via `page=N` query param; stops when `page >= total_pages`. Reference endpoints (`/reference/bmunits/all`) are not paginated. |
| Historical depth | Several years. |
| Publication lag  | ~hour before delivery (gate closure). |
| Response format  | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `settlementDate` | string | Yes | The settlement date to query. This must be in the format yyyy-MM-dd. | `2026-05-06` |
| `settlementPeriod` | integer | Yes | The settlement period to query. This should be an integer from 1-50 inclusive. | `24` |
| `bmUnit` | array | No | The BM units to query. Add each unit separately. If no BM unit is selected all BM units will be displayed. | `T_DRAXX-1` |
| `format` | string | No | Response data format. Use json/xml to include metadata. | `json` |

### Working curl example

```bash
# Replace <ELEXON_API_KEY> with your env var if you choose to send one (Elexon endpoints
# tested 2026-05-08 do NOT require a key; set anyway for vendor courtesy).
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://data.elexon.co.uk/bmrs/api/v1/datasets/PN?settlementDate=2026-05-06&settlementPeriod=24&format=json" \
  -o "/tmp/elexon-pn.json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/elexon/pn/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per API call (paginated requests append additional files for the same date partition).

### Bronze sample

Captured live 2026-05-08 from the https://data.elexon.co.uk/bmrs/api/v1/datasets/PN?settlementDate=2026-05-06&settlementPeriod=24&format=json:

```json
{
  "data": [
    {
      "dataset": "PN",
      "settlementDate": "2026-05-06",
      "settlementPeriod": 24,
      "timeFrom": "2026-05-06T10:59:00Z",
      "timeTo": "2026-05-06T11:00:00Z",
      "levelFrom": -9,
      "levelTo": 0,
      "nationalGridBmUnit": "FFSE02",
      "bmUnit": "2__FFSEN007"
    },
    {
      "dataset": "PN",
      "settlementDate": "2026-05-06",
      "settlementPeriod": 24,
      "timeFrom": "2026-05-06T10:59:00Z",
      "timeTo": "2026-05-06T11:00:00Z",
      "levelFrom": 11,
      "levelTo": 0,
      "nationalGridBmUnit": "BROFB-1",
      "bmUnit": "E_BROFB-1"
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/elexon/pn/year=YYYY/month=MM/pn_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.elexon.pn.PNTransformer`
**Pydantic schema**: `gridflow.schemas.elexon.ElexonPN`
**Dedup key**: `(settlement_date, settlement_period, bm_unit_id)`
**Point-in-time field**: `ingested_at` (no native PIT field)

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `settlement_date` | `date` | No | `settlementDate` | Settlement date (BST/GMT calendar). |
| `settlement_period` | `int` | No | `settlementPeriod` | 1..50 (DST: 46 spring, 50 autumn). |
| `timestamp_utc` | `datetime[UTC]` | No | _derived_ | Derived from (settlement_date, settlement_period) via `utils/time.settlement_period_to_utc`. |
| `bm_unit_id` | `str` | Yes (in practice) | `bmUnit` | BM Unit identifier — preserve raw casing. Elexon sends `bmUnit` null for some units (only `nationalGridBmUnit` set; 46 per period on 2026-09-20, e.g. `IVG-VKL1`, `COALD-1`). The transformer does not keep `nationalGridBmUnit` and dedups on the key, so those units collapse into one null-key row per period, keeping the last one's levels and dropping the rest (e.g. `AG-PEPG01`'s non-zero levels) (`gridflow/silver/elexon/pn.py:58-64,98-101`). |
| `level_from` | `float` | Yes | `levelFrom` | MW level at the start of the kept segment, not necessarily of the period (see Known issues). |
| `level_to` | `float` | Yes | `levelTo` | MW level at the end of the kept segment, not necessarily of the period (see Known issues). |
| `data_provider` | `str` | No | _derived_ | Default `"elexon"`. |
| `ingested_at` | `datetime[UTC]` | Yes | _derived_ | When the silver transform ran: stamped `datetime.now(UTC)` by the transformer (`pn.py:103-108`), not the bronze ingest time. |

### Silver sample

```python
[
    {
        "settlement_date": "2026-05-06",
        "settlement_period": 24,
        "timestamp_utc": "2026-05-06T10:30:00+00:00",
        "bm_unit_id": "2__FFSEN007",
        "level_from": -9,
        "level_to": 0,
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

- **Per-period fetch**: connector iterates periods 1..N for each settlement date, N = `settlement_periods_in_day` (46/48/50 by the DST calendar) (`gridflow/connectors/elexon/client.py:184-188`).
- **High row count** — ~2500 rows per period (one per active BM Unit).
- **Empty period is local** — an empty page 1 skips only that period and the loop continues to the next; an empty later page raises (`client.py:207-220`). The vendor returns HTTP 200 with empty `data` for a period outside the date's DST calendar (client docstring, probed 2026-07-27).
- **Silver keeps one segment per unit and period, and drops the segment times.** Elexon sends each unit's period as one or more segments (`timeFrom`, `timeTo`, `levelFrom`, `levelTo`). The transformer maps no `timeFrom`/`timeTo` and dedups on `(settlement_date, settlement_period, bm_unit_id)` with `keep="last"` (`pn.py:58-64,98-101,111-120`), so the within-period level path cannot be rebuilt from silver, and `level_to` is the end of the kept segment, not of the period. Which segment survives depends on the response order. Checked on bronze 2026-09-16..22: every kept segment was the one that starts the period. Example, 2026-09-20 SP10, `2__BCMRO002`: five segments (0 to -42 MW in 03:30-03:31, holding, back to 0 at 03:59-04:00); silver keeps `0 / -42`.

---

## Implementation delta

- **Required params**: docs require both `settlementDate` and `settlementPeriod`; code's `SETTLEMENT_DATE_PERIOD` style iterates periods 1..N, N from `settlement_periods_in_day` (46/48/50), one request per period with `page` (`client.py:184-199`, `endpoints.py:291-313`).

---

## Modelling notes

TODO

---

## Links

- [Official API docs (Swagger UI)](https://bmrs.elexon.co.uk/api-documentation)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/elexon/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/elexon/pn.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/elexon.py)
- Gold view/builder
- [Domain: GB Balancing Mechanism](../../../20-domain/markets/gb-balancing-mechanism.md)
