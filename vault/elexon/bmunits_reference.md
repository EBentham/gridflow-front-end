---
source: elexon
dataset_key: bmunits_reference
vendor: Elexon BMRS
last_verified: 2026-09-09
layer_coverage: bronze, silver
page:
  title: Balancing Mechanism unit register
  summary: >-
    Elexon's register of Balancing Mechanism units: each unit's ID, name, fuel-type code,
    capacity, lead party and National Grid ID.
  facts:
    vendor: Elexon BMRS, reference endpoint `/reference/bmunits/all`
    cadence: A whole-register snapshot per call; `sources.yaml` declares it weekly
    grain: One row per BM unit registration (`bm_unit_id`)
  landscape: units
  what_it_is: >-
    Elexon's Balancing Mechanism unit register in one call: each unit's Elexon ID, National
    Grid ID, name, fuel-type code, generation capacity and lead party. Many units carry no
    fuel type. Rows sent without an Elexon ID are dropped and logged. Capacity is per
    registration and does not sum: the project found one interconnector registered many times.
  how_used:
    - Joining per-unit feeds such as `pn` and `boal` to fuel type and lead party.
    - Mapping Elexon BM unit IDs to National Grid IDs, and back.
    - A starting list of units for a merit-order model; registrations are not plants.
  chart:
    type: bar
    silver: elexon/bmunits_reference
    group: fuel_type
    group_null: no_fuel
    group_map:
      WIND: wind
      OTHER: other
      CCGT: gas
      OCGT: gas
      NPSHYD: hydro
      PS: hydro
      NUCLEAR: nuclear
      BIOMASS: biomass
      COAL: coal
      INTELEC: interconnectors
      INTEW: interconnectors
      INTFR: interconnectors
      INTGRNL: interconnectors
      INTIFA2: interconnectors
      INTIRL: interconnectors
      INTNED: interconnectors
      INTNEM: interconnectors
      INTNSL: interconnectors
      INTVKL: interconnectors
    aggregation: count
    sort: value_desc
    unit: BM units
  chart_view:
    title: BM units by fuel type, 26 September 2026
    caption: >-
      Silver `elexon/bmunits_reference`, the register as fetched on 26 September 2026: a count of
      BM units per fuel-type code, grouped as the key lists. Units with no fuel type keep their own
      bar.
    alt: >-
      Horizontal bar chart counting BM units by fuel type in one snapshot of
      elexon/bmunits_reference. The no-fuel-type bar dwarfs the rest at 2,515 units. Then wind
      234, other 92, gas (CCGT and OCGT) 83, hydro (pumped and not) 38, nuclear 16, biomass 15,
      interconnectors 11 and coal 10.
    key:
      - {series: no_fuel, label: No fuel type, codes: "null", paint: hatch-dots, note: "Elexon sends `fuelType` as null: a missing code, not a fuel."}
      - {series: wind, label: Wind, codes: WIND}
      - {series: other, label: Other, codes: OTHER, note: "Elexon's own code; what it holds is undocumented."}
      - {series: gas, label: Gas, codes: "CCGT, OCGT"}
      - {series: hydro, label: Hydro, codes: "NPSHYD, PS", paint: hatch-lines, note: "Pumped storage (PS) and non-pumped hydro (NPSHYD) counted together."}
      - {series: nuclear, label: Nuclear, codes: NUCLEAR}
      - {series: biomass, label: Biomass, codes: BIOMASS}
      - {series: interconnectors, label: Interconnectors, codes: "INT*, 10 codes", paint: olive, note: "Units with an `INT*` code: a count of registrations, not a flow."}
      - {series: coal, label: Coal, codes: COAL, paint: hatch-cross}
  raw_feed:
    note: >-
      One call with no parameters returns the register. `gridflow ingest` saves it to bronze;
      `gridflow transform` rewrites one silver file from the newest capture, dropping rows with
      no Elexon ID.
    requests:
      - "GET https://data.elexon.co.uk/bmrs/api/v1/reference/bmunits/all"
    commands:
      - {run: gridflow ingest elexon bmunits_reference, comment: "bronze; no dates needed"}
      - {run: gridflow transform elexon bmunits_reference, comment: newest capture to silver}
  record:
    select:
      filter:
        - {column: bm_unit_id, op: in, value: [2__AANGE001, E_ABERDARE, I_EAD-FRAN1, I_IEG-FRAN1, T_ABRBO-1, T_DINO-1, T_HEYM11, T_PEHE-1]}
      order_by: [bm_unit_id]
    mark: {bm_unit_id: E_ABERDARE}
    key: [bm_unit_id]
    caption: "Eight units picked by ID: three have a null `fuel_type`, as Elexon sent them."
    fields:
      bm_unit_id: Elexon BM unit ID (`elexonBmUnit`), the key; rows without one are dropped
      bm_unit_name: The unit's name as Elexon sends it (`bmUnitName`)
      fuel_type: Elexon fuel-type code (`fuelType`); null when Elexon sends none
      registered_capacity_mw: MW from `generationCapacity`, cast to a float; one registration's, not additive
      company_name: Lead party name (`leadPartyName`)
      gsp_group_id: Grid supply point group (`gspGroupId`), for example `_K`; may be null
      national_grid_bm_unit: National Grid's ID for the unit (`nationalGridBmUnit`); not the EIC
      data_provider: "Same on every row: elexon"
      ingested_at: When the silver transform ran; the same on every row
  notebook:
    lead: >-
      `query()` filters on a date column, and this table's is `ingested_at`, a transform time, so
      these cells use `data.sql()` on the DuckDB relation `silver_elexon_bmunits_reference`,
      naming the vendor columns to leave lineage out.
    cells:
      - |
        df = data.sql("""
            SELECT bm_unit_id, bm_unit_name, fuel_type, registered_capacity_mw,
                   company_name, gsp_group_id, national_grid_bm_unit
            FROM silver_elexon_bmunits_reference
            ORDER BY bm_unit_id
        """)
      - df[["bm_unit_id", "fuel_type", "registered_capacity_mw", "company_name"]].head()
      - df["fuel_type"].value_counts(dropna=False)
    needs: the BM unit register
  related:
    - {dataset: elexon/pn, note: "Physical notifications per unit, keyed on the same `bm_unit_id`"}
    - {dataset: elexon/boal, note: "Accepted bids and offers per unit, keyed on the same `bm_unit_id`"}
    - {dataset: elexon/uou2t14d, note: "Availability per unit 2 to 14 days ahead, same `bm_unit_id`"}
    - {dataset: elexon/fuelhh, note: Half-hourly outturn by the fuel-type codes charted here}
---

# Elexon - BM Units Reference Data (`BMUNITS`)

## Overview

Reference data describing every registered Balancing Mechanism Unit — BM Unit ID, friendly name, fuel type, registered capacity, lead party, GSP group, and ENTSO-E EIC. This is slowly-changing master data used to enrich every per-unit dataset (BOALF, PN, UOU2T14D, etc.).

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://data.elexon.co.uk/bmrs/api/v1` |
| Path             | `/reference/bmunits/all` |
| Method           | GET |
| Auth             | None required for tested endpoints (2026-05-08). Some endpoints accept an `apikey` header (env: `ELEXON_API_KEY`); registration at https://www.elexonportal.co.uk/. |
| Rate limit       | Vendor-published: not stated. Project default 2 req/sec (asyncio.Semaphore); verified safe 2026-05-08. |
| Pagination       | None — full snapshot returned in one call. |
| Historical depth | Current state only (point-in-time snapshot). |
| Publication lag  | Slowly-changing reference data; refreshed when BM Unit registrations change. |
| Response format  | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| _none_ | _none_ | _none_ | No query parameters required. | _n/a_ |

### Working curl example

```bash
# Replace <ELEXON_API_KEY> with your env var if you choose to send one (Elexon endpoints
# tested 2026-05-08 do NOT require a key; set anyway for vendor courtesy).
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://data.elexon.co.uk/bmrs/api/v1/reference/bmunits/all?format=json" \
  -o "/tmp/elexon-bmunits_reference.json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/elexon/bmunits_reference/<year>/<month>/<day>/raw_<YYYYMMDDTHHMMSSZ>_<sha256[:8]>.json`, partitioned by fetch date because the request carries no date (`gridflow/bronze/writer.py:33-57`)
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per API call (paginated requests append additional files for the same date partition).

### Bronze sample

Captured live 2026-05-08 from the https://data.elexon.co.uk/bmrs/api/v1/reference/bmunits/all?format=json (envelope corrected 2026-09-27: the body is a bare JSON array with no `data` key, as a bronze capture's first bytes show; see Implementation delta):

```json
[
  {
    "nationalGridBmUnit": "ABERU-1",
    "elexonBmUnit": "E_ABERDARE",
    "eic": null,
    "fuelType": null,
    "leadPartyName": "UK Power Reserve Limited",
    "bmUnitType": "E",
    "fpnFlag": true,
    "bmUnitName": "Aberdare Power Station",
    "leadPartyId": "UKPR",
    "demandCapacity": "0.000",
    "generationCapacity": "15.400",
    "productionOrConsumptionFlag": "C",
    "transmissionLossFactor": "0.0162928",
    "workingDayCreditAssessmentImportCapability": "0.000",
    "nonWorkingDayCreditAssessmentImportCapability": "0.000",
    "workingDayCreditAssessmentExportCapability": "6.160",
    "nonWorkingDayCreditAssessmentExportCapability": "6.160",
    "creditQualifyingStatus": true,
    "demandInProductionFlag": false,
    "gspGroupId": "_K",
    "gspGroupName": "South Wales",
    "interconnectorId": null
  },
  {
    "nationalGridBmUnit": "ABRBO-1",
    "elexonBmUnit": "T_ABRBO-1",
    "eic": "48W00000ABRBO-19",
    "fuelType": "WIND",
    "leadPartyName": "Aberdeen Offshore Wind Farm",
    "bmUnitType": "T",
    "fpnFlag": true,
    "bmUnitName": "ABRBO-1",
    "leadPartyId": "ABERDEEN",
    "demandCapacity": "-2.000",
    "generationCapacity": "99.000",
    "productionOrConsumptionFlag": "P",
    "transmissionLossFactor": "-0.0323359",
    "workingDayCreditAssessmentImportCapability": "-0.800",
    "nonWorkingDayCreditAssessmentImportCapability": "-0.800",
    "workingDayCreditAssessmentExportCapability": "39.600",
    "nonWorkingDayCreditAssessmentExportCapability": "39.600",
    "creditQualifyingStatus": true,
    "demandInProductionFlag": false,
    "gspGroupId": null,
    "gspGroupName": null,
    "interconnectorId": null
  }
]
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/elexon/bmunits_reference/bmunits_reference.parquet`, one file rewritten on every transform from the newest bronze capture (`gridflow/silver/elexon/bmunits.py:66-80` and the `_write_silver` override at `:212-220`)
**Transformer class**: `gridflow.silver.elexon.bmunits.BMUnitsTransformer`
**Pydantic schema**: `gridflow.schemas.elexon.ElexonBMUnit`
**Dedup key**: `(bm_unit_id)`
**Point-in-time field**: `ingested_at` (no native PIT field)

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `bm_unit_id` | `str` | No | `bmUnit` or `elexonBmUnit` | BM Unit identifier — preserve raw casing. |
| `bm_unit_name` | `str` | Yes | `name` or `bmUnitName` | Friendly name of the BM Unit. |
| `fuel_type` | `str` | Yes | `fuelType` | Fuel category (CCGT, COAL, NUCLEAR, WIND, etc.). Nullable per ElexonBMUnit. |
| `registered_capacity_mw` | `float` | Yes | `registeredCapacity` or `generationCapacity` | MW. |
| `company_name` | `str` | Yes | `companyName` or `leadPartyName` | Lead party (operator) name. |
| `gsp_group_id` | `str` | Yes | `gspGroupId` | GSP group identifier. |
| `national_grid_bm_unit` | `str` | Yes | `nationalGridBmUnit` | National Grid BM Unit id (e.g. `ABERU-1`) — **not** the ENTSO-E EIC. The bronze carries the EIC in a separate `eic` field (e.g. `48W00000ABRBO-19`), which the transformer does not currently map into silver. |
| `data_provider` | `str` | No | _derived_ | Default `"elexon"`. |
| `ingested_at` | `datetime[UTC]` | Yes | _derived_ | When the silver transform ran: stamped `datetime.now(UTC)` by the transformer, the same on every row (`bmunits.py:190-196`), not the bronze ingest time. |

### Silver sample

```python
[
    {
        "bm_unit_id": "E_ABERDARE",
        "bm_unit_name": "Aberdare Power Station",
        "fuel_type": null,
        "registered_capacity_mw": 15.4,
        "company_name": "UK Power Reserve Limited",
        "gsp_group_id": "_K",
        "national_grid_bm_unit": "ABERU-1",
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

- **Slowly-changing data** — re-fetch when the BM unit registry changes (typically a few times per year).
- **No pagination** — full snapshot returned in one call (~3000 rows).
- **Keyless rows are real and blank at source** (measured 2026-09-09). Every one of the 19
  bronze captures of 2026-09-01 holds **3060 rows, exactly 90 with `elexonBmUnit: null`**, the
  same 90 `nationalGridBmUnit` values each time. Confirmed against the live endpoint the same
  day: a fresh `GET /reference/bmunits/all` returned 3063 rows with **89** still null. Not an
  ingest or parsing defect. At least partly transient — `DYCEB-1` was null in all 19 captures
  and is `E_DYCEB-1` eight days later. Handled by gridflow ADR-032 (drop + log, not fatal).
- **`registeredCapacity` is absent from the payload entirely.** The field that populates
  `registered_capacity_mw` is **`generationCapacity`**, 100% of the time — determinate, not a
  split between the two mapped names (measured 2026-09-09 over the 2026-09-01 capture).
- **Capacity fields arrive as JSON strings, not numbers** — cast before arithmetic.
- **`bmUnitType`, `fpnFlag` and `demandCapacity` are present in bronze but are NOT mapped into
  silver** by `BMUnitsTransformer.column_mapping`. Consumers needing to tell a generating
  registration from a non-generating one cannot do it from silver today (gridflow_models
  RULINGS #524, 2026-09-09).
- **Registration rows are not one-per-physical-asset.** Of the 1,200 positive-capacity rows
  with a null `fuelType`, **627 carry `bmUnitType = "I"` and a non-null `interconnectorId`,
  totalling 681,375.860 MW** across just ten `interconnectorId` values — e.g. `FRANCE` has
  **126 registrations under 125 distinct `leadPartyName` values summing 183,199.82 MW while
  its largest single registration is 4,000.00 MW**. Summing `generationCapacity` across these
  rows does not yield physical capacity. **`bmUnitType = "I"` is an INTERCONNECTOR, not a
  plant** — confirmed by Bobbo 2026-09-09 (gridflow_models RULINGS #536). Each row is one
  party's registration against a shared physical link, so the rows are per-party trading
  registrations and are **not additive**. Still undocumented by the vendor: what the other
  codes (`G`, `S`, `E`, `T`, `V`) denote — no vendor documentation defining any of them was
  found (three OpenAPI paths 404'd, 2026-09-09); `"I"` is owner-confirmed, not vendor-cited.

---

## Implementation delta

- **Response is a JSON array** (no `{data: [...]}` envelope) — silver `BMUnitsTransformer` and connector handle this.
- **`ElexonBMUnit`** Pydantic schema declared.
- **No pagination** — `supports_pagination = False`.

---

## Modelling notes

**Interconnector capacity does not come from this dataset.** A consumer that needs
interconnector flow reads the ten `INT*` codes in **FUELHH** — a realised half-hourly signed
series — not a `generationCapacity` sum here. The two are different objects and only one is
a flow. **FUELHH sign convention: positive = IMPORT to GB**, established 2026-09-09 by
summing all FUELHH fuel types against INDO over 816 half-hours (MAE 945.8 MW as stored vs
6,546.3 MW with the INT signs flipped; net flow +2,754.4 MW).

**Do not treat this dataset as a plant list.** It is a registry of *registrations*, and a
single physical asset can carry many — the interconnector rows above are the clearest case
(53.1x more registered MW on the ten `interconnectorId` values than the 11 fuel-typed `INT*`
units in silver carry for the same links). A Plant Universe built by summing
`registered_capacity_mw` without a type filter will overstate GB capacity by roughly an order
of magnitude: 708,308.823 MW of null-fuel registrations against ~47,952 MW of typed
CCGT/COAL/OCGT/NUCLEAR/BIOMASS (measured 2026-09-09).

**`fuel_type` coverage is thin** — only 496 of 2969 silver rows carry one (2026-09-09, after
ADR-032's drop). A FUELHH↔BMUNITS technology mapping cannot rely on it alone.

---

## Links

- [Official API docs (Swagger UI)](https://bmrs.elexon.co.uk/api-documentation)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/elexon/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/elexon/bmunits.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/elexon.py)
- Gold view/builder
- [Domain: GB Balancing Mechanism](../../../20-domain/markets/gb-balancing-mechanism.md)
