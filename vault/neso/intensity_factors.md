---
source: neso
dataset_key: intensity_factors
vendor: National Energy System Operator (NESO)
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Emission factors by fuel type
  summary: >-
    The emission factor NESO's Carbon Intensity API assigns each fuel type, labelled gCO2/kWh by
    gridflow: one table of 14 fuels.
  facts:
    vendor: NESO Carbon Intensity API, route `/intensity/factors`
    cadence: One call returns the whole table; gridflow's schedule fetches it weekly
    grain: One row per fuel (`fuel`), its factor labelled gCO2/kWh by gridflow
  landscape: power
  what_it_is: >-
    NESO's Carbon Intensity factor for each fuel type, one table per call. Gas is split
    into open and combined cycle, imports by country (Dutch, French, Irish). gridflow reads the
    factors as gCO2/kWh; the response states no unit, and NESO's API definitions do not say whether
    a factor is combustion only or life cycle.
  how_used:
    - Approximate carbon intensity of a mix; `generation` lumps gas and imports, so assume factors.
    - A per-fuel factor lookup for approximate carbon-intensity features.
  chart:
    type: bar
    silver: neso/intensity_factors
    value: factor_gco2_kwh
    group: fuel
    group_map:
      coal: Coal
      oil: Oil
      gas_open_cycle: Gas (OCGT)
      gas_combined_cycle: Gas (CCGT)
      dutch_imports: Dutch imports
      irish_imports: Irish imports
      french_imports: French imports
      other: Other
      biomass: Biomass
      hydro: Hydro
      nuclear: Nuclear
      pumped_storage: Pumped storage
      solar: Solar
      wind: Wind
    aggregation: last
    sort: value_desc
    unit: gCO2/kWh
  chart_view:
    title: Emission factor by fuel, fetched 26 September 2026
    caption: >-
      Silver `neso/intensity_factors`, gCO2/kWh, the table as fetched on 26 September 2026: one
      factor per fuel, nothing summed. CCGT and OCGT are NESO's combined- and open-cycle gas. Hydro,
      nuclear, pumped storage, solar and wind are 0.
    alt: >-
      Horizontal bar chart of NESO's emission factor per fuel, in gCO2/kWh, from
      neso/intensity_factors as fetched on 26 September 2026. Coal 937 and oil 935 lead, then
      open-cycle gas 651, Dutch imports 474, Irish imports 458, combined-cycle gas 394, other 300,
      biomass 120 and French imports 53. Hydro, nuclear, pumped storage, solar and wind are all 0.
    key:
      - {series: factor_gco2_kwh, label: Factor per fuel, codes: gCO2/kWh, paint: petrol, note: "One value per fuel as NESO sends it; imports carry one factor per country."}
  raw_feed:
    note: >-
      One call with no parameters returns the whole table. `gridflow transform` rewrites one silver
      file from the newest bronze capture, so a revised factor replaces the old row.
    requests:
      - "GET https://api.carbonintensity.org.uk/intensity/factors"
    commands:
      - {run: gridflow ingest neso intensity_factors, comment: "bronze; the window is ignored"}
      - {run: gridflow transform neso intensity_factors, comment: newest capture to silver}
  record:
    select:
      filter:
        - {column: fuel, op: in, value: [coal, dutch_imports, french_imports, gas_combined_cycle, gas_open_cycle, irish_imports, other, wind]}
      order_by: [fuel]
      columns: [fuel, factor_gco2_kwh]
    key: [fuel]
    caption: "Eight of 14 fuels: gas split by cycle, imports by country, and wind at 0."
    fields:
      fuel: "NESO's fuel name, lowercased and snake-cased: `Gas (Combined Cycle)` becomes `gas_combined_cycle`"
      factor_gco2_kwh: "Factor as a float; gCO2/kWh is gridflow's label, the response states no unit"
  notebook:
    lead: >-
      `query()` filters on a date column, and this table's is `ingested_at`, a transform time, so
      these cells use `data.sql()` on the DuckDB relation `silver_neso_intensity_factors`.
    cells:
      - |
        df = data.sql("""
            SELECT fuel, factor_gco2_kwh
            FROM silver_neso_intensity_factors
            ORDER BY factor_gco2_kwh DESC, fuel
        """)
      - df.head()
      - df[df["fuel"].str.contains("gas|imports")]
    needs: the fuel factor table
  related:
    - {dataset: neso/generation, note: "Half-hourly mix by fuel; gas and imports are single categories there"}
    - {dataset: neso/carbon_intensity, note: "NESO's half-hourly national carbon intensity, also in gCO2/kWh"}
    - {dataset: elexon/fuelhh, note: "Splits gas by cycle and imports by interconnector, closer to these factors"}
    - {dataset: neso_data_portal/historic_generation_mix, note: "NESO's mix history, with a carbon intensity column of its own"}
---

# NESO - Generation fuel emission factors (`intensity_factors`)

## Overview

This reference endpoint gives carbon intensity factors by fuel type. It explains how generation technologies are weighted inside the Carbon Intensity methodology and is useful for validating model-derived emissions estimates or deriving generation-mix carbon proxies. See [Carbon intensity](../../../20-domain/concepts/carbon-intensity.md) and [Settlement period](../../../20-domain/concepts/settlement-period.md).

---

## API endpoint

| Property | Value |
|----------|-------|
| Base URL | `https://api.carbonintensity.org.uk` |
| Path | `/intensity/factors` |
| Method | GET |
| Auth | None; send `Accept: application/json` |
| Rate limit | Not documented by NESO; Gridflow config uses 10 req/s. |
| Pagination | None. Dynamic inputs are path segments, not query parameters. |
| Historical depth | Static reference endpoint |
| Publication lag | Static reference data |
| Response format | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| None | - | - | No query string or path parameters. | - |

### Working curl example

```bash
curl --ssl-no-revoke -X GET \
  "https://api.carbonintensity.org.uk/intensity/factors" \
  -H "Accept: application/json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/neso/intensity_factors/<year>/<month>/<day>/raw_<timestamp>_<hash>.json`
**Format**: Raw JSON, as received. Immutable after write, with `.meta.json` provenance sidecar.
**Granularity**: One file per API call; range and daily routes may produce one file per chunk/day/period.

### Bronze sample

```json
{"data":[{"Gas (Combined Cycle)":394,"Wind":0,"Solar":0}]}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/neso/intensity_factors/intensity_factors.parquet`
**Transformer class**: `gridflow.silver.neso.carbon_intensity.IntensityFactorsTransformer`
**Pydantic schema**: `gridflow.schemas.neso.CarbonIntensityFactor`
**Dedup key**: `(fuel)`
**Point-in-time field**: `none`
**Write mode**: one file, rewritten on every transform from the newest bronze body only; a revised factor replaces the old row in silver, and only bronze keeps earlier fetches (`silver/neso/carbon_intensity.py:132-139`, `:251`).

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| fuel | str | No | raw object key | Normalised to lowercase snake_case. |
| factor_gco2_kwh | float | Yes | raw object value | Fuel carbon factor in gCO2/kWh. |
| data_provider | str | No | derived | Always neso. |
| ingested_at | datetime[UTC] | No | derived | Silver transform timestamp. |

### Silver sample

```python
[{"fuel":"gas_combined_cycle","factor_gco2_kwh":394.0,"data_provider":"neso","ingested_at":"2026-05-04T00:00:00+00:00"},{"fuel":"wind","factor_gco2_kwh":0.0,"data_provider":"neso","ingested_at":"2026-05-04T00:00:00+00:00"}]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- Official docs use UTC timestamps ending in `Z`; keep joins in UTC.
- The connector sends no query parameters; all documented inputs are path parameters.
- Actual carbon intensity values can be null or absent, especially before post-period estimates are available.
- For `intensity_period`, GB clock-change days can have 46 or 50 settlement periods in implementation even though official docs describe period 1-48.
- The 14 factor fuels do not match the 9 `generation` fuels: gas is split into `gas_combined_cycle` and `gas_open_cycle`, imports into `dutch_imports`, `french_imports` and `irish_imports`, and `oil` and `pumped_storage` have no `generation` category. A join on `fuel` needs a mapping (gridflow `.planning/phases/V1-vault-vendor-validation-and-docs/neso-VALIDATION.md` section 5; silver `neso/generation` fuels checked 2026-10-06).
- The response sends bare numbers with no unit; `gCO2/kWh` is gridflow's column label. The API definitions page describes the route only as "Get Carbon Intensity factors for each fuel type" and states no unit, no emissions basis (combustion or life cycle) and nothing on how import factors are set; no sentence anywhere on that page mentions life cycle or combustion, and its only scope line is that "The Carbon Intensity forecast includes CO2 emissions related to electricity generation only" (whole page checked 2026-10-06). The linked national methodology PDF was not read.

---

## Implementation delta

No discrepancies found.

---

## Modelling notes

Use as a static lookup to convert generation mix into approximate carbon intensity features. Version/staleness matters because factor changes can silently shift labels.

---

## Links

- [Official API docs](https://carbon-intensity.github.io/api-definitions/)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/neso/carbon_intensity.py)
- [Endpoint metadata](../../../../../../Python/gridflow/src/gridflow/connectors/neso/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/neso/carbon_intensity.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/neso.py)
- [Gold view (does not read this table)](../../../../../../Python/gridflow/src/gridflow/gold/views/uk_imbalance_context.sql)
- [Domain: Carbon intensity](../../../20-domain/concepts/carbon-intensity.md)

