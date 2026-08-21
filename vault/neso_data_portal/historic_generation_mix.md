---
source: neso_data_portal
dataset_key: historic_generation_mix
vendor: "NESO Open Data Portal"
last_verified: 2026-08-19
layer_coverage: "bronze, silver"
---

# NESO Data Portal — Historic GB Generation Mix

## Overview

Half-hourly GB generation mix from 2009: MW per fuel (gas, coal, nuclear,
wind, embedded wind, hydro, imports, biomass, solar, storage, other), total
generation, carbon intensity, and NESO's own percentage shares. The longest
half-hourly fuel-mix history in the stack — a training backbone for
carbon-intensity and fuel-switching models. It also reaches what Elexon
`fuelhh` structurally cannot: `fuelhh` is transmission-only, while `wind_emb`
here includes embedded wind. NESO cleanses and republishes the **whole
history**, so two captures can legitimately disagree about the same
half-hour — vintages matter.

→ [Settlement period](../../../20-domain/concepts/settlement-period.md)

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://api.neso.energy/api/3/action/` |
| Path             | `package_show?id=historic-generation-mix` → resource URL from `resources[]`, then file download (302 → presigned CDN URL) |
| Method           | GET |
| Auth             | None — keyless public API (verified 2026-08-16) |
| Rate limit       | Vendor guidance: max 1 request/second (CKAN actions); IP-block enforcement. Connector throttles every send |
| Pagination       | None; single file download (~60 MB class — the large-file path is tested to a 1.5 GB memory budget, observed peak 180 MiB for a 60 MiB body) |
| Historical depth | 2009 onwards (vendor-stated coverage of the resource) |
| Publication lag  | TODO — republication cadence not stated; `ckan_last_modified` carries the vendor instant |
| Response format  | JSON (CKAN metadata envelope) → CSV (the data file) |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `id` | string | Yes | CKAN package (dataset) slug | `historic-generation-mix` |

Resource selected by **exact `resources[].name == "Historic GB Generation
Mix"`** (D-03), format `CSV`, URL re-resolved from `package_show` at every
fetch (D-06). Download size cap for this dataset: 256 MiB.

### Working curl example

```bash
# Keyless — no auth header:
curl -X GET \
  "https://api.neso.energy/api/3/action/package_show?id=historic-generation-mix"
```

---

## Bronze layer

**Path pattern**: `data/bronze/neso_data_portal/historic_generation_mix/<year>/<month>/<day>/raw_<fetched_at>_<uuid>.csv`
**Format**: Raw CSV, as-received. Immutable. `<stem>.meta.json` sidecar carries fetch provenance.
**Granularity**: One file per capture — the whole 2009-to-now history each time; partition is the ingest window's end date (D-13)

### Bronze sample

```csv
DATETIME,GAS,COAL,NUCLEAR,WIND,WIND_EMB,HYDRO,IMPORTS,BIOMASS,OTHER,SOLAR,STORAGE,GENERATION,CARBON_INTENSITY,LOW_CARBON,ZERO_CARBON,RENEWABLE,FOSSIL,GAS_perc,COAL_perc,NUCLEAR_perc,WIND_perc,WIND_EMB_perc,HYDRO_perc,IMPORTS_perc,BIOMASS_perc,OTHER_perc,SOLAR_perc,STORAGE_perc,GENERATION_perc,LOW_CARBON_perc,ZERO_CARBON_perc,RENEWABLE_perc,FOSSIL_perc
2009-06-01T05:00:00,12345,8000,6500,500,0,300,1000,0,200,0,0,28845,480,7300,7300,800,20345,42.8,27.7,22.5,1.7,0.0,1.0,3.5,0.0,0.7,0.0,0.0,100.0,25.3,25.3,2.8,70.5
2009-06-01T05:30:00,12400,7950,6500,520,0,310,1000,0,200,0,0,28880,478,7330,7330,830,20350,42.9,27.5,22.5,1.8,0.0,1.1,3.5,0.0,0.7,0.0,0.0,100.0,25.4,25.4,2.9,70.4
```

(Header is contract-exact — **34 columns**, counted from the Stage-A capture
`_probe/sample_historic-generation-mix.csv`; the plan said 37 until the
rev-14 erratum corrected it from the file. Values above are illustrative of
shape, not real records — see the fixture for real captured rows.)

---

## Silver layer

**Path pattern**: `data/silver/neso_data_portal/historic_generation_mix/<year>/<month>/<day>/data_<run_suffix>.parquet` (APPEND_ONLY — one file per vintage)
**Transformer class**: `gridflow.silver.neso_data_portal.historic_generation_mix.HistoricGenerationMixTransformer`
**Pydantic schema**: `gridflow.schemas.neso_data_portal.NesoHistoricGenerationMix`
**Dedup key**: `(timestamp_utc, published_at)` — the publication instant is in the key unconditionally because NESO republishes cleansed history and two captures may disagree about one half-hour (D-21/D-24)
**Point-in-time field**: `published_at` (`ckan_last_modified` via D-23; `available_at == published_at`, D-22)

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `timestamp_utc` | `datetime[UTC]` | No | `DATETIME` | Vendor's offset-naive stamp read **as UTC**. That reading is documented, not inferred: the UTC statement exists only in the `datastore_search` field metadata (`_probe/datastore_historic-generation-mix.json`, `DATETIME.info.description`), which a plain CSV download never exposes. A `DATETIME` that *does* carry an offset raises rather than being silently reinterpreted (vendor-drift guard, checked on the raw Utf8 before any cast) |
| `gas` … `fossil` (17 MW/index fields) | `float` | No | `GAS` … `FOSSIL` | MW per fuel; `generation` is the total; `carbon_intensity` is gCO2/kWh; strict Float64 casts |
| `gas_pct` … `fossil_pct` (16 fields) | `float` | No | `GAS_perc` … `FOSSIL_perc` | NESO's **own** published percentages, carried not recomputed — a recomputation would disagree at NESO's rounding; the vendor's number is what reconciles against the portal |
| `published_at` | `datetime[UTC]` | No | sidecar `ckan_last_modified` | Required; a body without it is declined (D-23/FM-05) |
| `data_provider` | `str` | No | derived | Constant `neso_data_portal` |

(Full field list: `gas, coal, nuclear, wind, wind_emb, hydro, imports,
biomass, other, solar, storage, generation, carbon_intensity, low_carbon,
zero_carbon, renewable, fossil` + the 16 `_pct` counterparts — 33 numeric
columns mapping the 34-column vendor header minus `DATETIME`.)

### Silver sample

```python
[
    {
        "timestamp_utc": datetime(2009, 6, 1, 5, 0, tzinfo=timezone.utc),
        "gas": 12345.0, "coal": 8000.0, "nuclear": 6500.0, "wind": 500.0,
        "wind_emb": 0.0, "hydro": 300.0, "imports": 1000.0, "biomass": 0.0,
        "other": 200.0, "solar": 0.0, "storage": 0.0, "generation": 28845.0,
        "carbon_intensity": 480.0, "low_carbon": 7300.0, "zero_carbon": 7300.0,
        "renewable": 800.0, "fossil": 20345.0,
        "gas_pct": 42.8, "coal_pct": 27.7, "nuclear_pct": 22.5,
        "wind_pct": 1.7, "wind_emb_pct": 0.0, "hydro_pct": 1.0,
        "imports_pct": 3.5, "biomass_pct": 0.0, "other_pct": 0.7,
        "solar_pct": 0.0, "storage_pct": 0.0, "generation_pct": 100.0,
        "low_carbon_pct": 25.3, "zero_carbon_pct": 25.3,
        "renewable_pct": 2.8, "fossil_pct": 70.5,
        "published_at": datetime(2026, 8, 16, 18, 20, 11, tzinfo=timezone.utc),
        "data_provider": "neso_data_portal",
    },
]
```

---

## Gold layer

None implemented. Consumer surface:
`silver_neso_data_portal_historic_generation_mix` (all vintages) and
`silver_neso_data_portal_historic_generation_mix_latest` (one winning row per
`timestamp_utc`) — `_latest` is the consumer default (D-30).

---

## Known issues and gotchas

- **Whole-history republication**: every capture re-delivers 2009-to-now, so
  the base view multiplies with each capture. Consume `_latest`. The
  vintage axis is real signal (NESO cleanses history), not noise.
- **Naive `DATETIME` is UTC by metadata only** — the CSV itself never says
  so. The transformer refuses offset-carrying values so a future vendor
  format change surfaces loudly instead of shifting the series by an hour.
- **Cross-checked against Elexon**: the settlement-convention test asserts
  this stack derives the same UTC instants as `elexon/fuelhh` through the
  shared `settlement_period_to_utc`; a non-binding corroboration pins
  NESO's `TIME_GMT` (on the embedded-forecast dataset) as period-END.
  A magnitude cross-check against local fuelhh silver skips under pytest by
  conftest design (the data-dir env var is cleared in tests).
- **No backfill** (D-35) and **D-13 partition-on-window-end** — same
  operator guidance and residuals as the other two datasets: prefer
  `gridflow pipeline`; transform over a window covering the ingest window's
  end date.
- **FM-15 completeness limit**: vintages are only as dense as the capture
  cadence.
- **Large file**: ~60 MB class today and growing; the 256 MiB download cap
  and the tested memory budget (1.5 GB, observed 180 MiB peak) cover it.
  D-19's `schema_overrides` escape hatch exists if the budget is ever hit —
  not needed to date.
- Skipped/unusable bodies → `completed_with_warnings` / all-declined →
  `failed` (D-41, ADR-030).

---

## Implementation delta

- **Column count**: plan prose said **37** columns through rev 13; the
  Stage-A capture has **34**. Corrected by rev-14 erratum, counted from the
  file — the file is the authority (D-24). No live disagreement observed.

---

## Modelling notes

TODO. Intended use: carbon-intensity forecasting targets and features
(`carbon_intensity` as target, fuel MW/shares as features); fuel-switching
studies (gas-vs-coal margins); `wind_emb` as the embedded-generation
complement to Elexon's transmission-only view; long-history seasonal
baselines from 2009. Filter guidance: use `_latest`; treat pre-solar-era
zeros (`solar` before ~2011) as structural, not missing.

---

## Links

- [Official API docs](https://api.neso.energy/api/3/action/package_show?id=historic-generation-mix)
- [Connector source](../../../../../Python/gridflow/src/gridflow/connectors/neso_data_portal/client.py)
- [Silver transformer](../../../../../Python/gridflow/src/gridflow/silver/neso_data_portal/historic_generation_mix.py)
- [Pydantic schema](../../../../../Python/gridflow/src/gridflow/schemas/neso_data_portal.py)
- Gold view/builder: none
- [Domain: settlement period](../../../20-domain/concepts/settlement-period.md)
