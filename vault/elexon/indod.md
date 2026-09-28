---
source: elexon
dataset_key: indod
vendor: Elexon BMRS
last_verified: 2026-05-08
layer_coverage: bronze, silver
---

# Elexon - Initial National Demand Outturn (Daily) (`INDOD`)

## Overview

Initial National Demand Outturn — Daily (INDOD) — the daily-aggregated total of INDO. One record per settlement date; the code states no unit for the total (see `initial_demand_outturn_mw` below).

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://data.elexon.co.uk/bmrs/api/v1` |
| Path             | `/datasets/INDOD` |
| Method           | GET |
| Auth             | None required for tested endpoints (2026-05-08). Some endpoints accept an `apikey` header (env: `ELEXON_API_KEY`); registration at https://www.elexonportal.co.uk/. |
| Rate limit       | Vendor-published: not stated. Project default 2 req/sec (asyncio.Semaphore); verified safe 2026-05-08. |
| Pagination       | Connector handles via `page=N` query param; stops when `page >= total_pages`. Reference endpoints (`/reference/bmunits/all`) are not paginated. |
| Historical depth | Several years. |
| Publication lag  | Daily total, published at end-of-day. |
| Response format  | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `publishDateTimeFrom` | string | Yes | As per Elexon Swagger spec for indod. | `2026-05-06T00:00Z` |
| `publishDateTimeTo` | string | Yes | As per Elexon Swagger spec for indod. | `2026-05-06T03:00Z` |
| `format` | string | No | Response data format. Use json/xml to include metadata. | `json` |

### Working curl example

```bash
# Replace <ELEXON_API_KEY> with your env var if you choose to send one (Elexon endpoints
# tested 2026-05-08 do NOT require a key; set anyway for vendor courtesy).
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://data.elexon.co.uk/bmrs/api/v1/datasets/INDOD?publishDateTimeFrom=2026-04-01T00:00Z&publishDateTimeTo=2026-04-02T00:00Z&format=json" \
  -o "/tmp/elexon-indod.json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/elexon/indod/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per API call (paginated requests append additional files for the same date partition).

### Bronze sample

Captured live 2026-05-08 from the https://data.elexon.co.uk/bmrs/api/v1/datasets/INDOD?publishDateTimeFrom=2026-04-01T00:00Z&publishDateTimeTo=2026-04-02T00:00Z&format=json:

```json
{
  "data": [
    {
      "dataset": "INDOD",
      "publishTime": "2026-04-01T23:15:00Z",
      "settlementDate": "2026-04-01",
      "demand": 676741
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/elexon/indod/year=YYYY/month=MM/indod_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.elexon.indod.INDODTransformer`
**Pydantic schema**: `gridflow.schemas.elexon.ElexonINDOD` — validated fail-soft on the full frame at write time (VTA-SCHEMA-01: invalid rows are logged and counted, never dropped).
**Dedup key**: `(settlement_date)`
**Point-in-time field**: `published_at` (vendor `publishTime`, emitted since F-08: `indod.py:92-104`)

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `settlement_date` | `date` | No | `settlementDate` | Settlement date (BST/GMT calendar). |
| `timestamp_utc` | `datetime[UTC]` | No | _derived_ | Start of settlement period 1 of the date (00:00 UK time), `settlement_period_to_utc(d, 1)` (`indod.py:80-90`). |
| `initial_demand_outturn_mw` | `float` | No | `demand` | The day's total. Neither the code ("Daily Total", `endpoints.py:191`) nor the schema states a unit. It matches half the sum of that date's INDO half-hour MW values to within 2, which is what an MWh total would give (project check against INDO, 2026-09-27; not a vendor statement). |
| `published_at` | `datetime[UTC]` | Yes | `publishTime` | Vendor publish time (`indod.py:92-104`). |
| `data_provider` | `str` | No | _derived_ | Default `"elexon"`. |
| `ingested_at` | `datetime[UTC]` | Yes | _derived_ | When the silver transform ran: stamped `datetime.now(UTC)` by the transformer (`indod.py:108-113`), not the bronze ingest time. |

### Silver sample

```python
[
    {
        "settlement_date": "2026-04-01",
        "timestamp_utc": "2026-03-31T23:00:00+00:00",
        "initial_demand_outturn_mw": 676741,
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

- **Daily aggregate** — one row per settlement_date.

---

## Implementation delta

- **Daily aggregate** — one record per `settlementDate`. Silver dedup is on `settlement_date` only.
- **Sparse cadence** — empty within 3-hour windows; V1 validation used a 1-day window.
- **Pydantic schema** `ElexonINDOD` exists in `schemas/elexon.py` and is applied via `BaseSilverTransformer._validate_against_schema` (fail-soft).

---

## Modelling notes

TODO

---

## Links

- [Official API docs (Swagger UI)](https://bmrs.elexon.co.uk/api-documentation)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/elexon/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/elexon/indod.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/elexon.py)
- Gold view/builder
- [Domain: GB Balancing Mechanism](../../../20-domain/markets/gb-balancing-mechanism.md)
