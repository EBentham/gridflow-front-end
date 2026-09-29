---
source: elexon
dataset_key: tsdf
vendor: Elexon BMRS
last_verified: 2026-07-31
layer_coverage: bronze, silver
---

# Elexon - Transmission System Demand Forecast (`TSDF`)

## Overview

Transmission System Demand Forecast (TSDF) — published demand forecast restricted to the transmission system (excludes embedded generation). TSDF is the transmission-only demand companion of NDF.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://data.elexon.co.uk/bmrs/api/v1` |
| Path             | `/datasets/TSDF` |
| Method           | GET |
| Auth             | None required for tested endpoints (2026-05-08). Some endpoints accept an `apikey` header (env: `ELEXON_API_KEY`); registration at https://www.elexonportal.co.uk/. |
| Rate limit       | Vendor-published: not stated. Project default 2 req/sec (asyncio.Semaphore); verified safe 2026-05-08. |
| Pagination       | Connector handles via `page=N` query param; stops when `page >= total_pages`. Reference endpoints (`/reference/bmunits/all`) are not paginated. |
| Historical depth | Several years. |
| Publication lag  | Day-ahead and intra-day. |
| Response format  | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `boundary` | string | No | As per Elexon Swagger spec for tsdf. | `N` |
| `publishDateTimeFrom` | string | No | As per Elexon Swagger spec for tsdf. | `2026-05-06T00:00Z` |
| `publishDateTimeTo` | string | No | As per Elexon Swagger spec for tsdf. | `2026-05-06T03:00Z` |
| `format` | string | No | Response data format. Use json/xml to include metadata. | `json` |

### Working curl example

```bash
# Replace <ELEXON_API_KEY> with your env var if you choose to send one (Elexon endpoints
# tested 2026-05-08 do NOT require a key; set anyway for vendor courtesy).
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://data.elexon.co.uk/bmrs/api/v1/datasets/TSDF?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-06T03:00Z&format=json" \
  -o "/tmp/elexon-tsdf.json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/elexon/tsdf/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per API call (paginated requests append additional files for the same date partition).

### Bronze sample

Captured live 2026-05-08 from the https://data.elexon.co.uk/bmrs/api/v1/datasets/TSDF?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-06T03:00Z&format=json:

```json
{
  "data": [
    {
      "dataset": "TSDF",
      "demand": 195,
      "publishTime": "2026-05-06T02:47:00Z",
      "startTime": "2026-05-06T03:00:00Z",
      "settlementDate": "2026-05-06",
      "settlementPeriod": 9,
      "boundary": "B1"
    },
    {
      "dataset": "TSDF",
      "demand": 195,
      "publishTime": "2026-05-06T02:47:00Z",
      "startTime": "2026-05-06T03:30:00Z",
      "settlementDate": "2026-05-06",
      "settlementPeriod": 10,
      "boundary": "B1"
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/elexon/tsdf/year=YYYY/month=MM/tsdf_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.elexon.tsdf.TSDFTransformer`
**Pydantic schema**: `gridflow.schemas.elexon.ElexonTSDF` — validated fail-soft on the full frame at write time (VTA-SCHEMA-01: invalid rows are logged and counted, never dropped).
**Dedup key**: `(settlement_date, settlement_period, boundary)` (`silver/elexon/tsdf.py:112-115`), applied within each daily transform (one UTC publish day per silver file)
**Point-in-time field**: `published_at`, from `publishTime` (`silver/elexon/tsdf.py:98-110`)

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `settlement_date` | `date` | No | `settlementDate` | Settlement date (BST/GMT calendar). |
| `settlement_period` | `int` | No | `settlementPeriod` | 1..50 (DST: 46 spring, 50 autumn). |
| `timestamp_utc` | `datetime[UTC]` | No | _derived_ | Derived from (settlement_date, settlement_period) via `utils/time.settlement_period_to_utc`. |
| `forecast_demand_mw` | `float` | No | `demand` | MW. |
| `boundary` | `str` | Yes | `boundary` | Transmission-boundary identifier. Observed `B1` in the live bronze sample; the `boundary` query param also accepts `N` (national). Vendor-managed value list — no fixed enumeration. |
| `published_at` | `datetime[UTC]` | Yes | `publishTime` | Vendor publish time of the surviving vintage (`tsdf.py:98-110`); not in the dedup key. |
| `data_provider` | `str` | No | _derived_ | Default `"elexon"`. |
| `ingested_at` | `datetime[UTC]` | Yes | _derived_ | When the silver transform ran: stamped `datetime.now(UTC)` by the transformer (`tsdf.py:117-123`), not the bronze ingest time. |

### Silver sample

```python
[
    {
        "settlement_date": "2026-05-06",
        "settlement_period": 9,
        "timestamp_utc": "2026-05-06T03:00:00+00:00",
        "forecast_demand_mw": 195,
        "boundary": "B1",
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

- **Transmission-only forecast** — analogous to ITSDO for outturn.
- **The feed returns 18 boundaries, not one** (live-verified 2026-07-31; supersedes the "Observed `B1`" note on the `boundary` silver field, which reflected a single sampled row, not the response shape). A 24h publish window returned 50,688 rows split evenly across `B1`–`B17` **plus `N`**, 2,816 rows each. `N` is the national figure; `B*` are individual transmission boundaries at much smaller scale (a sampled `B1` row read 210 MW against a same-period national NDF of 22,810 MW). **Any query must filter `boundary = 'N'` for a national-level series** — the silver transformer passes `boundary` through without filtering, so an unfiltered group-by silently returns ~18× the expected rows and a meaningless demand total.
- **Silver does NOT retain forecast vintages — TSDF cannot be used for forecast-evolution analysis** (live-verified 2026-07-31). The upstream feed *does* republish roughly every 30 minutes (846 vintage-rows per `(settlement_date, settlement_period)` = ~47 publish times × 18 boundaries), but the transformer's dedup key is `(settlement_date, settlement_period, boundary)` with **`published_at` absent from the key** (`silver/elexon/tsdf.py`, `dedup_cols`), so vintages collapse to one `keep="last"` survivor per daily transform. Each silver file holds one UTC publish day (the Elexon publication-window filter on `published_at`, `silver/elexon/_publication_window.py`), so a period keeps one survivor per publish day that covered it, and bronze row order, not publish time, decides which (in the 2026-09-15 file it was the day's earliest publish). `published_at` survives as a *column* but is not a distinguishing key, which makes it look usable when it is not. Contrast [ndf.md](./ndf.md), whose dedup key *does* include `published_at` and therefore preserves the full vintage history. Changing this is a schema decision, not a bug fix — flagged, not assumed.

---

## Implementation delta

- **Pydantic schema** `ElexonTSDF` exists in `schemas/elexon.py` and is applied via `BaseSilverTransformer._validate_against_schema` (fail-soft).

---

## Modelling notes

TODO

---

## Links

- [Official API docs (Swagger UI)](https://bmrs.elexon.co.uk/api-documentation)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/elexon/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/elexon/tsdf.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/elexon.py)
- Gold view/builder
- [Domain: GB Balancing Mechanism](../../../20-domain/markets/gb-balancing-mechanism.md)
