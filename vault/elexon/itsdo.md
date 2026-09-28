---
source: elexon
dataset_key: itsdo
vendor: Elexon BMRS
last_verified: 2026-07-30
layer_coverage: bronze, silver
---

# Elexon - Initial Transmission System Demand Outturn (`ITSDO`)

## Overview

Initial Transmission System Demand Outturn (ITSDO) — the realised transmission-network demand per settlement period. ITSDO is **higher** than INDO, not lower. By the cited definitions (see Modelling notes → Definition citations), ITSDO = INDO + a **fixed station-load estimate (500 MW BST / 600 MW GMT)** + pump-storage pumping + interconnector exports, plus storage-module charging under the Grid Code definition. Unmetered embedded wind/solar is in neither series. (Corrected 2026-09-24, gridflow_models v2.1 F-5: the earlier `+ embedded generation` term is not supported by the NESO or Grid Code definitions.) Live-verified 2026-07-30 against 24 July 2026 silver: ITSDO exceeded INDO by ~2,375 MW on average across the day (every settlement period, no exceptions), ruling out the previous "national demand minus embedded generation" description, which predicted the opposite sign. ITSDO is the transmission-only counterpart to INDO and is what drives transmission-network analytics.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://data.elexon.co.uk/bmrs/api/v1` |
| Path             | `/datasets/ITSDO` |
| Method           | GET |
| Auth             | None required for tested endpoints (2026-05-08). Some endpoints accept an `apikey` header (env: `ELEXON_API_KEY`); registration at https://www.elexonportal.co.uk/. |
| Rate limit       | Vendor-published: not stated. Project default 2 req/sec (asyncio.Semaphore); verified safe 2026-05-08. |
| Pagination       | Connector handles via `page=N` query param; stops when `page >= total_pages`. Reference endpoints (`/reference/bmunits/all`) are not paginated. |
| Historical depth | Several years. |
| Publication lag  | ~hour after each settlement period closes. |
| Response format  | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `publishDateTimeFrom` | string | No | As per Elexon Swagger spec for itsdo. | `2026-05-06T00:00Z` |
| `publishDateTimeTo` | string | No | As per Elexon Swagger spec for itsdo. | `2026-05-06T03:00Z` |
| `format` | string | No | Response data format. Use json/xml to include metadata. | `json` |

### Working curl example

```bash
# Replace <ELEXON_API_KEY> with your env var if you choose to send one (Elexon endpoints
# tested 2026-05-08 do NOT require a key; set anyway for vendor courtesy).
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://data.elexon.co.uk/bmrs/api/v1/datasets/ITSDO?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-06T03:00Z&format=json" \
  -o "/tmp/elexon-itsdo.json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/elexon/itsdo/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per API call (paginated requests append additional files for the same date partition).

### Bronze sample

Captured live 2026-05-08 from the https://data.elexon.co.uk/bmrs/api/v1/datasets/ITSDO?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-06T03:00Z&format=json:

```json
{
  "data": [
    {
      "dataset": "ITSDO",
      "publishTime": "2026-05-06T03:00:00Z",
      "startTime": "2026-05-06T02:30:00Z",
      "settlementDate": "2026-05-06",
      "settlementPeriod": 8,
      "demand": 23628
    },
    {
      "dataset": "ITSDO",
      "publishTime": "2026-05-06T02:30:00Z",
      "startTime": "2026-05-06T02:00:00Z",
      "settlementDate": "2026-05-06",
      "settlementPeriod": 7,
      "demand": 24569
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/elexon/itsdo/year=YYYY/month=MM/itsdo_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.elexon.itsdo.ITSDOTransformer`
**Pydantic schema**: `gridflow.schemas.elexon.ElexonITSDO` — validated fail-soft on the full frame at write time (VTA-SCHEMA-01: invalid rows are logged and counted, never dropped).
**Dedup key**: `(settlement_date, settlement_period)`
**Point-in-time field**: `published_at`

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `settlement_date` | `date` | No | `settlementDate` | Settlement date (BST/GMT calendar). |
| `settlement_period` | `int` | No | `settlementPeriod` | 1..50 (DST: 46 spring, 50 autumn). |
| `timestamp_utc` | `datetime[UTC]` | No | _derived_ | Derived from (settlement_date, settlement_period) via `utils/time.settlement_period_to_utc`. |
| `initial_transmission_system_demand_outturn_mw` | `float` | No | `demand` | MW. |
| `published_at` | `datetime[UTC]` | Yes | `publishTime` | Publication time / document vintage; bitemporal point-in-time field. |
| `data_provider` | `str` | No | _derived_ | Default `"elexon"`. |
| `ingested_at` | `datetime[UTC]` | Yes | _derived_ | When the silver transform ran: stamped `datetime.now(UTC)` by the transformer (`itsdo.py:118-123`), not the bronze ingest time. |

### Silver sample

```python
[
    {
        "settlement_date": "2026-05-06",
        "settlement_period": 8,
        "timestamp_utc": "2026-05-06T02:30:00+00:00",
        "initial_transmission_system_demand_outturn_mw": 23628,
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

- **ITSDO is above INDO, not below.** A 2026-07-30 correction previously described this as `ITSDO = INDO + embedded generation + interconnector exports + pump-storage pumping` — that attribution was itself wrong on closer testing (see below) and is superseded again here. What's confirmed by live data (24 July 2026, 48 settlement periods): `itsdo_minus_indo` is consistently positive and stays in a narrow ~1,530–3,050 MW band all day (mean ~2,375 MW), with **no meaningful midday peak** — its correlation with AGWS solar output is only 0.35 despite solar swinging 0 → 12,700 MW over the same periods, which rules out embedded solar as a material driver. Correlation with FUELHH pumped-storage flow (`PS`, negative = pumping) is −0.43 — a real but partial signal, consistent with pump-storage pumping load being one contributor, not confirmed as the whole story. **Do not derive an "embedded generation" estimate as `INDO − ITSDO`** — the sign and magnitude don't support that reading. Exact decomposition of the ITSDO−INDO gap is TODO.
- **Neither INDO nor ITSDO is a full generation-side reconciliation against FUELHH — but the gap is not embedded-generation-driven.** `FUELHH-stack + net-interconnector-flow` undershoots ITSDO by ~1,000–2,200 MW at every settlement period on 24 July 2026 (live-verified), essentially flat across the day (correlation with AGWS solar: 0.02 — no midday widening despite solar's 0→12,700 MW swing over the same window). A prior note here claimed this gap was embedded-solar-driven and widened at midday; that claim did not survive testing the full-day shape and is retracted. The flat, few-GW magnitude is more consistent with transmission losses and/or generation categories FUELHH doesn't bucket cleanly, but neither is confirmed — TODO before citing a cause.

---

## Implementation delta

- **Pydantic schema** `ElexonITSDO` exists in `schemas/elexon.py` and is applied via `BaseSilverTransformer._validate_against_schema` (fail-soft).

---

## Modelling notes

### Definition citations (gridflow_models v2.1 F-5, OWNER #865)

Source record: `gridflow_models/.planning/phases/v2.1-F-5-vendor-definitions/CITATIONS.md` (Opus research review CONVERGED, REVIEW-RESEARCH-2); archived bytes under `C:/gridflow-data/receipts/v2.1-F-5/sources/` (`#NN:line`). Written under OWNER #865 on 2026-09-24. Citations only: the owner's class-3 ruling on them is pending at the gridflow_models v2.1 close.

- **Mapping.** NESO: National Demand "is equivalent to the Initial National Demand Outturn (INDO)"; Transmission System
  Demand "is equivalent to the Initial Transmission System Outturn (ITSDO)" (NESO data portal, Daily demand update
  definitions, #01:244, #01:268; live page, undated). The Grid Code's terms are **National Demand** and **National
  Electricity Transmission System Demand** (Grid Code Glossary, Issue 6 Revision 45, 13 Aug 2026, #02:3009–3033); no
  archived Grid Code text names INDO/ITSDO.
- **Station-transformer load:** INDO excludes it (Grid Code National Demand "minus … the Demand taken by Station
  Transformers"). ITSDO includes it **as a fixed estimate**: "Transmission System Demand includes an estimate of station
  load of 500MW in BST and 600MW in GMT" (#01:268). ITSDO−INDO does not contain metered station load.
- **Pumped-storage pumping and interconnector exports:** INDO excludes both; ITSDO includes both. TSD is "ND plus the
  additional generation required to meet station load, pump storage pumping and interconnector exports" (#01:268); the
  Grid Code National Demand "does not include … any exports".
- **Electricity Storage Modules (battery charging):** the Grid Code lists "Pumped Storage Units' and Electricity Storage
  Modules'" in both clauses (excluded from National Demand, included in NETS Demand; #02:3013–3015, 3031–3033). NESO
  names only pump-storage pumping, so the sources disagree. `TODO:` battery treatment in INDO/ITSDO *as published*.
- **Embedded wind and solar:** NESO's unmetered estimates are components of neither series. They are "embedded in the
  distribution network and invisible to National Grid ESO. Their effect is to suppress the electricity demand" (#01:292,
  #01:316, with #01:244 "sum of metered generation"). Supply from **Embedded Large Power Stations** is included in both
  (Grid Code). `TODO:` no blanket classification of all distribution-connected wind/solar.

---

## Links

- [Official API docs (Swagger UI)](https://bmrs.elexon.co.uk/api-documentation)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/elexon/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/elexon/itsdo.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/elexon.py)
- Gold view/builder
- [Domain: GB Balancing Mechanism](../../../20-domain/markets/gb-balancing-mechanism.md)
