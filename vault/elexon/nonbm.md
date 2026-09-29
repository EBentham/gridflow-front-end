---
source: elexon
dataset_key: nonbm
vendor: Elexon BMRS
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Non-BM STOR generation
  summary: >-
    Elexon's figure for generation by Short-Term Operating Reserve providers outside the
    Balancing Mechanism, one per GB settlement period.
  facts:
    vendor: Elexon BMRS, dataset NONBM
    cadence: "Not established; gridflow asks in 24-hour publish windows"
    grain: One row per settlement period; no provider or unit column
  landscape: power
  what_it_is: >-
    Elexon's generation from Short-Term Operating Reserve (STOR) providers that sit outside the
    Balancing Mechanism: one figure per GB settlement period, with no provider named. Every
    publish window gridflow requested in May and August 2026 returned the same single record:
    settlement date 1 April 2026, period 22, generation 0. Whether Elexon publishes rarely or has
    stopped is not established.
  how_used:
    - Adding non-BM reserve output to BM-metered generation for a fuller supply picture.
    - A reserve-dispatch feature for an imbalance price model, beside BM acceptances.
  chart:
    type: none
    reason: >-
      One vendor record (settlement date 1 April 2026, period 22, generation 0) is all the
      publish-window requests have returned; one point makes no chart.
  raw_feed:
    note: >-
      Elexon's API reference lists `from` and `to` for NONBM. gridflow sends 24-hour
      `publishDateTimeFrom`/`To` windows; the record returned was published outside every window,
      so none filtered it.
    requests:
      - "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/NONBM?publishDateTimeFrom=2026-08-01T00:00:00Z&publishDateTimeTo=2026-08-02T00:00:00Z&page=1"
    commands:
      - {run: gridflow ingest elexon nonbm --start 2026-08-01 --end 2026-08-06, comment: "bronze; the end is exclusive"}
      - {run: gridflow transform elexon nonbm --start 2026-08-01 --end 2026-08-05, comment: one silver file per window}
  record:
    select:
      filter:
        - {column: settlement_date, op: eq, value: "2026-04-01"}
        - {column: settlement_period, op: eq, value: 22}
      order_by: [ingested_at]
      columns: [settlement_date, settlement_period, generation_mw, published_at, ingested_at]
    key: [settlement_date, settlement_period]
    caption: "One Elexon record, settlement date 2026-04-01 period 22, repeated in each window's silver file."
    fields:
      settlement_date: GB settlement date, as Elexon sends it in `settlementDate`
      settlement_period: Half-hour of the settlement day, 1 to 48; 46 or 50 on clock-change days
      generation_mw: "Elexon's `generation` as a float; MW by the column name, not the response"
      published_at: Vendor publish time, from `publishTime`
      timestamp_utc: "Start of the half-hour, computed from settlement date and period; `startTime` is dropped"
  notebook:
    lead: >-
      Returns a pandas DataFrame from the DuckDB relation `silver_elexon_nonbm`, filtered on
      `settlement_date` with both ends included; lineage columns are dropped. The record is dated
      1 April, though fetched in August windows.
    cells:
      - df = data.elexon.query("nonbm", "2026-04-01", "2026-04-01")
      - df[["settlement_date", "settlement_period", "generation_mw", "published_at", "ingested_at"]]
      - df.drop_duplicates(["settlement_date", "settlement_period"])[["settlement_date", "settlement_period", "generation_mw"]]
    needs: the 1 to 5 August 2026 publish windows
  related:
    - {dataset: elexon/disbsad, note: "Balancing actions outside the BM; STOR providers flagged by `stor_flag`"}
    - {dataset: elexon/boal, note: "Balancing Mechanism acceptances; non-BM STOR runs outside them"}
    - {dataset: elexon/fuelhh, note: Transmission-metered generation by fuel for the same settlement periods}
    - {dataset: elexon/system_prices, note: The imbalance prices for the same settlement periods}
---

# Elexon - Non-BM STOR Generation (`NONBM`)

## Overview

Non-BM Short-Term Operating Reserve (NONBM STOR) generation — output from STOR providers that operate outside of the Balancing Mechanism. NONBM is what supplements BM-unit dispatch in periods of system stress.

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
| Historical depth | Several years. |
| Publication lag  | Half-hourly. |
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
  "https://data.elexon.co.uk/bmrs/api/v1/datasets/NONBM?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-06T03:00Z&format=json" \
  -o "/tmp/elexon-nonbm.json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/elexon/nonbm/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per API call (paginated requests append additional files for the same date partition).

### Bronze sample

Captured live 2026-05-08 from the https://data.elexon.co.uk/bmrs/api/v1/datasets/NONBM?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-06T03:00Z&format=json:

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
| `generation_mw` | `float` | No | `generation` | MW. |
| `published_at` | `datetime[UTC]` | Yes | `publishTime` | Publication time / document vintage; bitemporal point-in-time field. |
| `data_provider` | `str` | No | _derived_ | Default `"elexon"`. |
| `ingested_at` | `datetime[UTC]` | Yes | _derived_ | When the silver transform ran, not the bronze fetch (`silver/elexon/nonbm.py:114-118`). |

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
- **One record repeated across silver files**: bronze is filed under the publish-window start date (`connectors/elexon/client.py:314`), the transformer reads one such day (`silver/elexon/nonbm.py:31-37`) and dedups within it only (`nonbm.py:112`). Because every window returned the same record, `nonbm_20260801` to `nonbm_20260805` each hold settlement date 2026-04-01, period 22. Drop repeats on the key after `query()`.

---

## Implementation delta

- **Param style mismatch**: docs declare `from`/`to`; code uses default `publishDateTimeFrom/To`. Live test 2026-05-08 (window 2026-05-06) returned 1 row published 2026-04-01T10:04Z, outside the requested window, so the default param names did not filter it. The windows 2026-05-04 to 2026-05-10 and 2026-08-01 to 2026-08-05 each returned the same body (`body_sha256` `123a943b…` in every bronze `.meta.json`). The same vendor behaviour is recorded for FREQ with the wrong param names (`connectors/elexon/endpoints.py:100-103`). Worth verifying with explicit `from`/`to` parameters and noting whichever path is canonical.
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
