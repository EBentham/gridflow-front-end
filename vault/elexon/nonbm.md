---
source: elexon
dataset_key: nonbm
vendor: Elexon BMRS
last_verified: 2026-10-24
layer_coverage: bronze, silver
page:
  title: Non-BM STOR generation
  summary: >-
    Elexon's figure for Short-Term Operating Reserve that the system operator used outside the
    Balancing Mechanism, one per GB settlement period.
  facts:
    vendor: Elexon BMRS, dataset NONBM
    cadence: Half-hourly, by settlement period
    grain: One row per settlement period; no provider or BM unit column
    history: "No record published after 1 April 2026, 10:04 UTC, as of 16 October 2026"
  landscape: power
  what_it_is: >-
    Elexon's figure for Short-Term Operating Reserve (STOR) that the system operator used outside
    the Balancing Mechanism, per GB settlement period, stamped with its publish time. The feed
    sends no unit; gridflow's column says MW.
  how_used:
    - A reserve-use feature for an imbalance price model, beside BM acceptances.
    - Flagging the settlement periods in which non-BM STOR was used.
  chart:
    type: line
    silver: elexon/nonbm
    time: timestamp_utc
    value: generation_mw
    filter:
      - {column: settlement_date, op: ge, value: "2026-01-12"}
      - {column: settlement_date, op: le, value: "2026-01-18"}
    aggregation: last
    window: {start: "2026-01-12", end: "2026-01-18"}
    unit: MW
  chart_view:
    title: Non-BM STOR generation, 12 to 18 January 2026
    caption: >-
      Silver `elexon/nonbm`, MW by gridflow's column name (Elexon states none), every half-hour
      of settlement dates 12 to 18 January 2026, one value each. Only periods 25 to 27 on the
      15th are above 0: 17, 28 and 11.
    alt: >-
      Line chart of non-BM STOR generation from elexon/nonbm, MW by gridflow's column name, for
      every half-hour of 12 to 18 January 2026. The line lies at 0 throughout except from 12:00 to
      13:30 UTC on 15 January, periods 25 to 27, where it reads 17, 28 and 11.
    x_label: settlement date; each starts at 00:00 UTC
    y_min: -2
    key:
      - {series: generation_mw, label: Non-BM STOR, codes: NONBM, paint: petrol, note: "Highest 28 in period 26 of 15 January, 12:30 UTC."}
  raw_feed:
    note: >-
      Requested in 24-hour publish windows (`from` and `to`, UTC), the names Elexon's API
      reference gives. Each period arrives in the window of its publish time.
    requests:
      - "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/NONBM?from=2026-01-15T00:00:00Z&to=2026-01-16T00:00:00Z&page=1"
    commands:
      - {run: gridflow ingest elexon nonbm --start 2026-01-12 --end 2026-01-20, comment: "bronze; the end is exclusive"}
      - {run: gridflow transform elexon nonbm --start 2026-01-12 --end 2026-01-19, comment: "19th adds the 18th's last period"}
  record:
    select:
      filter:
        - {column: settlement_date, op: eq, value: "2026-01-15"}
        - {column: settlement_period, op: ge, value: 23}
        - {column: settlement_period, op: le, value: 30}
      order_by: [settlement_period]
      columns: [settlement_period, generation_mw, settlement_date, timestamp_utc, published_at]
    key: [settlement_date, settlement_period]
    caption: "Periods 23 to 30 of 15 January 2026, around the charted week's only values above 0."
    fields:
      settlement_date: GB settlement date, from `settlementDate`
      settlement_period: Half-hour of the settlement day, 1 to 48; 46 or 50 on clock-change days
      generation_mw: "Elexon's `generation`, a whole number with no unit; MW by gridflow's column name"
      timestamp_utc: "Start of the half-hour, computed from settlement date and period; `startTime` is dropped"
      published_at: "Elexon's publish time, from `publishTime`, UTC"
  notebook:
    lead: >-
      Returns a pandas DataFrame from the DuckDB relation `silver_elexon_nonbm`, filtered on
      `settlement_date` with both ends included; lineage columns are dropped. Sort by
      `timestamp_utc` before plotting.
    cells:
      - df = data.elexon.query("nonbm", "2026-01-12", "2026-01-18").sort_values("timestamp_utc")
      - df[df.generation_mw > 0][["settlement_date", "settlement_period", "timestamp_utc", "generation_mw"]]
      - df.plot(x="timestamp_utc", y="generation_mw", ylabel="MW", legend=False, figsize=(8, 3.5))
    needs: 12 to 19 January 2026
    plot_alt: >-
      Line plot of generation_mw against timestamp_utc for 12 to 18 January 2026, flat at 0 except
      a spike on 15 January to 17, 28 and 11 MW from 12:00 to 13:30 UTC.
  related:
    - {dataset: elexon/disbsad, note: "Balancing actions outside the BM, each with a STOR provider flag"}
    - {dataset: elexon/boal, note: "Balancing Mechanism acceptances; non-BM STOR is used outside them"}
---

# Elexon - Non-BM STOR Generation (`NONBM`)

## Overview

Non-BM Short-Term Operating Reserve (NONBM STOR) generation — output from STOR providers that operate outside of the Balancing Mechanism. Elexon's API reference (`/datasets/NONBM`, `swagger.json` read 2026-10-24) describes it as STOR "made use of by NGESO", activity outside the Balancing Mechanism; `generation` is an int64 with no unit stated. NESO's STOR page (https://www.neso.energy/industry-information/balancing-services/reserve-services/short-term-operating-reserve-stor, read 2026-10-24) says NESO "has now ceased all procurement of the STOR service", the last auction (30 March 2026) covering 05:00 on 31 March to 05:00 on 1 April 2026, and that Slow Reserve has replaced it. NESO gives no time zone for 05:00; UK clocks were on BST (UTC+1) on 1 April 2026. Neither NESO nor Elexon states any link between the end of STOR procurement and the NONBM feed, whose last record (period 22 of 1 April, published 10:04Z) comes after that delivery window.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://data.elexon.co.uk/bmrs/api/v1` |
| Path             | `/datasets/NONBM` |
| Method           | GET |
| Auth             | None required for tested endpoints (2026-05-08). Some endpoints accept an `apikey` header (env: `ELEXON_API_KEY`); registration at https://www.elexonportal.co.uk/. |
| Rate limit       | Vendor-published: not stated. Project default 2 req/sec (asyncio.Semaphore); verified safe 2026-05-08. |
| Pagination       | Connector handles via `page=N` query param; stops when `page >= total_pages`. Reference endpoints (`/reference/bmunits/all`) are not paginated. |
| Historical depth | Not stated by Elexon. Nothing published after 2026-04-01T10:04Z as of 2026-10-16 (see Known issues). |
| Publication lag  | Not stated. In every row gridflow fetched, `publishTime` is 34 minutes after `startTime`, as in the API reference's own example (13:00, 13:34). |
| Response format  | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `from` | string | No | The start of the data publish time window. | `2026-05-06T00:00Z` |
| `to` | string | No | The end of the data publish time window. | `2026-05-06T03:00Z` |
| `format` | string | No | Response data format. Use json/xml to include metadata. | `json` |

### Working curl example

```bash
# Replace <ELEXON_API_KEY> with your env var if you choose to send one (Elexon endpoints
# tested 2026-05-08 do NOT require a key; set anyway for vendor courtesy).
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://data.elexon.co.uk/bmrs/api/v1/datasets/NONBM?from=2026-01-15T00:00:00Z&to=2026-01-16T00:00:00Z&format=json" \
  -o "/tmp/elexon-nonbm.json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/elexon/nonbm/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per API call (paginated requests append additional files for the same date partition).

### Bronze sample

Captured live 2026-05-08 from the https://data.elexon.co.uk/bmrs/api/v1/datasets/NONBM?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-06T03:00Z&format=json (the endpoint ignores these names and answers as if no window were given, with its latest record; `connectors/elexon/endpoints.py:194-197`):

```json
{
  "data": [
    {
      "dataset": "NONBM",
      "publishTime": "2026-04-01T10:04:00Z",
      "startTime": "2026-04-01T09:30:00Z",
      "settlementDate": "2026-04-01",
      "settlementPeriod": 22,
      "generation": 0
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/elexon/nonbm/year=YYYY/month=MM/nonbm_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.elexon.nonbm.NONBMTransformer`
**Pydantic schema**: `gridflow.schemas.elexon.ElexonNonBM` — validated fail-soft on the full frame at write time (VTA-SCHEMA-01: invalid rows are logged and counted, never dropped).
**Dedup key**: `(settlement_date, settlement_period)`
**Point-in-time field**: `published_at`

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `settlement_date` | `date` | No | `settlementDate` | Settlement date (BST/GMT calendar). |
| `settlement_period` | `int` | No | `settlementPeriod` | 1..50 (DST: 46 spring, 50 autumn). |
| `timestamp_utc` | `datetime[UTC]` | No | _derived_ | Derived from (settlement_date, settlement_period) via `utils/time.settlement_period_to_utc`. |
| `generation_mw` | `float` | No | `generation` | Elexon sends an integer with no unit (API reference schema `NonBmStorData`); MW is gridflow's column name. |
| `published_at` | `datetime[UTC]` | Yes | `publishTime` | Publication time / document vintage; bitemporal point-in-time field. |
| `data_provider` | `str` | No | _derived_ | Default `"elexon"`. |
| `ingested_at` | `datetime[UTC]` | Yes | _derived_ | When the silver transform ran, not the bronze fetch (`silver/elexon/nonbm.py:154-159`). |

### Silver sample

```python
[
    {
        "settlement_date": "2026-04-01",
        "settlement_period": 22,
        "timestamp_utc": "2026-04-01T09:30:00+00:00",
        "generation_mw": 0,
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

- **STOR-only** — captures only Short-Term Operating Reserve providers operating outside the BM. Total non-BM dispatch needs further sources.
- **Nothing published after 2026-04-01T10:04Z (dated probes, no Elexon notice found)**: the API reference says that with no time window "the default output will be the latest published data", and the endpoint ignores `publishDateTimeFrom/To`. Requests sent that way on 2026-05-08 (this note's sample), 2026-08-16 (bronze `2026/08/01..05`, `body_sha256` `123a943b…`) and 2026-10-16 (gridflow's A/B, `connectors/elexon/endpoints.py:194-197`) each returned settlement date 2026-04-01, period 22, published 10:04Z. `from`/`to` windows for 2026-04-02 (fetched 2026-10-24) and 2026-08-01 to 2026-08-05 (fetched 2026-10-18) returned `{"data":[]}`. NESO ended STOR procurement with delivery to 05:00 on 2026-04-01 (Overview); no source links that to NONBM, and Elexon has not said whether NONBM has ended.
- **A UTC day's window starts late the evening before**: windows filter on `publishTime`, so the half-hour from 23:30 UTC (published 00:04Z) falls in the next day's bronze. Ingest one day past the last settlement date wanted.

---

## Implementation delta

- **Window params**: the connector sends `from`/`to`, the names the API reference declares (`connectors/elexon/endpoints.py:194-204`). The transformer reads only bronze whose `.meta.json` records a `from`/`to` request and excludes the rest, which stay in bronze (`silver/elexon/nonbm.py:22-52`, `83-87`).
- **Pydantic schema** `ElexonNonBM` exists in `schemas/elexon.py` and is applied via `BaseSilverTransformer._validate_against_schema` (fail-soft).

---

## Modelling notes

TODO

---

## Links

- [Official API docs (Swagger UI)](https://bmrs.elexon.co.uk/api-documentation)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/elexon/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/elexon/nonbm.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/elexon.py)
- Gold view/builder
- [Domain: GB Balancing Mechanism](../../../20-domain/markets/gb-balancing-mechanism.md)
