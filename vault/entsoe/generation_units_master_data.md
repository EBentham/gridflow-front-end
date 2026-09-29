---
source: entsoe
dataset_key: generation_units_master_data
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Production unit register
  summary: >-
    ENTSO-E's register of production units per bidding zone: each unit's EIC, name, production
    type code and implementation date.
  facts:
    vendor: ENTSO-E Transparency Platform, document type A95, business type B11
    cadence: One register per zone per request; `sources.yaml` schedules it weekly
    grain: One row per production unit and zone, per requested date
  landscape: units
  what_it_is: >-
    ENTSO-E's register of production units per bidding zone, one XML time series per unit: its
    EIC (`unit_mrid`), name, production type code and implementation date. What that date marks
    is undocumented, but not commissioning: one unit's moved from 2018 to 2025 between two
    requests. Each request is kept as its own copy; filter on `event_time`.
  how_used:
    - Naming and typing the `unit_mrid` codes in per-unit generation and outage feeds.
    - A unit list per zone and type; take MW from `installed_capacity_units`.
    - GB units also appear in Elexon's BM unit register; silver shares no key.
  chart:
    type: bar
    silver: entsoe/generation_units_master_data
    filter:
      - {column: event_time, op: eq, value: "2026-09-08T00:00:00Z"}
    group: production_type
    group_map:
      B04: gas
      B18: wind
      B19: wind
      B11: hydro
      B12: hydro
      B02: fossil
      B03: fossil
      B05: fossil
      B06: fossil
      B08: fossil
      B14: nuclear
      B10: pumped
      B01: misc
      B13: misc
      B16: misc
      B17: misc
      B25: misc
      B20: other
    aggregation: count
    sort: value_desc
    unit: production units
  chart_view:
    title: Production units by type, requested for 8 September 2026
    caption: >-
      Silver `entsoe/generation_units_master_data`, the register gridflow requested for 8 September
      2026 (fetched 15 September) in six zones: a count of production units per PSR type code,
      grouped as the key lists. A count, not capacity: silver carries no MW.
    alt: >-
      Horizontal bar chart counting production units by production type in the register gridflow
      requested for 8 September 2026, six bidding zones together. Gas (B04) leads with 175, wind
      (offshore and onshore) close behind at 172, then non-pumped hydro 106, coal, lignite, oil
      and peat 80, nuclear 70, pumped storage 27, smaller types (biomass, solar, waste, marine and storage) 21,
      and ENTSO-E's code Other 9.
    key:
      - {series: gas, label: Gas, codes: B04}
      - {series: wind, label: Wind, codes: "B18, B19", note: "Offshore (B18) and onshore (B19) counted together."}
      - {series: hydro, label: "Hydro, not pumped", codes: "B11, B12", paint: hatch-lines, note: "Run-of-river (B11) and reservoir (B12)."}
      - {series: fossil, label: "Coal, oil, peat", codes: "B02, B03, B05, B06, B08", paint: hatch-cross, note: "Lignite (B02), coal-derived gas (B03), hard coal (B05), oil (B06), peat (B08)."}
      - {series: nuclear, label: Nuclear, codes: B14}
      - {series: pumped, label: Pumped storage, codes: B10, paint: hatch-dots}
      - {series: misc, label: Smaller types, codes: "B01, B13, B16, B17, B25", paint: hatch-vertical, note: "Biomass (B01), marine (B13), solar (B16), waste (B17), energy storage (B25)."}
      - {series: other, label: Other, codes: B20, note: "ENTSO-E's own code Other; what it holds is undocumented."}
  raw_feed:
    note: >-
      One request per bidding zone with a single date, not a period. `gridflow ingest` sends
      `--start`'s date; `gridflow transform` writes each date's register to its own silver file.
    requests:
      - "GET https://web-api.tp.entsoe.eu/api?documentType=A95&Implementation_DateAndOrTime=2026-09-08&BiddingZone_Domain=10YBE\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D2&BusinessType=B11&securityToken=$ENTSOE_API_KEY"
    commands:
      - {run: gridflow ingest entsoe generation_units_master_data --start 2026-09-08 --end 2026-09-09, comment: "bronze; sends the start date only"}
      - {run: gridflow transform entsoe generation_units_master_data --start 2026-09-08 --end 2026-09-08, comment: that date's register to silver}
  record:
    select:
      filter:
        - {column: unit_mrid, op: in, value: ["22W201806271\x2D\x2D\x2DD", "22W202412112\x2D\x2D\x2DT", 17W100B100P0189S, 11W0-0000-0919-L, 17W0000022653653]}
      order_by: [area_code, unit_mrid, event_time]
      columns: [event_time, implementation_datetime_utc, unit_mrid, area_code, production_type, unit_name]
    key: [event_time, area_code, unit_mrid]
    caption: "Five units from two requests (`event_time`, the date requested); Seraing's date moved between them."
    fields:
      unit_mrid: "Production unit EIC (`registeredResource.mRID`); rows without one are dropped"
      area_code: "Bidding zone EIC, from the unit's `biddingZone_Domain.mRID`"
      implementation_datetime_utc: "`implementation_DateAndOrTime.date` as 00:00 UTC; meaning undocumented, not commissioning"
      production_type: "ENTSO-E PSR type code: the first `psrType` in the unit's XML"
      unit_name: "Unit name as sent (`registeredResource.name`); empty string when absent"
  notebook:
    lead: >-
      `query()` would filter on `implementation_datetime_utc`, the record date, across every
      request, so these cells use `data.sql()` on `silver_entsoe_generation_units_master_data`,
      one requested date, naming columns to leave lineage out.
    cells:
      - |
        df = data.sql("""
            SELECT area_code, unit_mrid, unit_name, production_type,
                   implementation_datetime_utc
            FROM silver_entsoe_generation_units_master_data
            WHERE event_time = TIMESTAMPTZ '2026-09-08 00:00:00+00'
            ORDER BY area_code, unit_mrid
        """)
      - df[["area_code", "unit_name", "production_type", "implementation_datetime_utc"]].head()
      - df["area_code"].value_counts()
    needs: the register requested for 8 September 2026
  related:
    - {dataset: entsoe/installed_capacity_units, note: "MW per unit on the same `unit_mrid`; this register drops it"}
    - {dataset: entsoe/actual_generation_units, note: "Output per unit, keyed on the same `unit_mrid`"}
    - {dataset: entsoe/outages_production, note: "Production unit outages, keyed on the same `unit_mrid`"}
    - {dataset: elexon/bmunits_reference, note: "GB units by BM unit ID; silver shares no key"}
---

# ENTSO-E — Production and generation units master data (A95)

## Overview

Reference catalogue of every registered production / generation unit in a
bidding zone — EIC mRID, asset name, production type, control area,
provider/operator. Updated as units are commissioned / retired.
Distinct from operational time-series datasets — this is the static
**registry** lookup. Used to populate the unit-name mapping table for
joining EIC-coded data (A73, A71/A33, outages) with vendor-named data
(Elexon BMUs, internal asset registers).

→ [Installed capacity per unit](installed_capacity_units.md), [Outages production](outages_production.md)

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | https://web-api.tp.entsoe.eu |
| Path             | /api |
| Method           | GET |
| Auth             | query param `securityToken=$ENTSOE_API_KEY` |
| Rate limit       | 1 req/s |
| Pagination       | None |
| Historical depth | snapshot — current registry |
| Publication lag  | continuous; updated when registry changes |
| Response format  | XML — root `Configuration_MarketDocument` |
| Document type    | A95 |
| Process type     | n/a (response carries `process.processType=A39` "production unit registry") |
| Business type    | B11 (production unit) — required parameter |
| Domain param name| `BiddingZone_Domain` |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `documentType` | str | yes | `A95` | `A95` |
| `BusinessType` | str | yes | `B11` (production unit) | `B11` |
| `BiddingZone_Domain` | EIC | yes | Bidding zone | `10YGB----------A` |
| `Implementation_DateAndOrTime` | ISO date | yes | Single date — **not a period range** | `2026-05-06` |

### Working curl example

```bash
curl --ssl-no-revoke -fsS \
  "https://web-api.tp.entsoe.eu/api?securityToken=$ENTSOE_API_KEY&documentType=A95&BusinessType=B11&BiddingZone_Domain=10YGB----------A&Implementation_DateAndOrTime=2026-05-06" \
  -H "Accept: application/xml"
```

Live verification 2026-05-08:
- GB: HTTP 200, **PASS** — `Configuration_MarketDocument`, 230 TimeSeries (one per registered unit). Each has `<registeredResource.mRID>`, `<registeredResource.name>`, `<registeredResource.location.name>`, `<ControlArea_Domain>`, `<Provider_MarketParticipant>`, `<MktPSRType>` and an `<implementation_DateAndOrTime.date>`.

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsoe/generation_units_master_data/<year>/<month>/<day>/raw_<YYYYMMDDTHHMMSSZ>_<sha256[:8]>.xml` plus a `.meta.json` sidecar, the date folder being the requested `Implementation_DateAndOrTime` and the timestamp the fetch time (`gridflow/bronze/writer.py:33-57,85`; corrected 2026-09-29)
**Format**: Raw XML, immutable.
**Granularity**: One file per (zone, requested date).

### Bronze sample (GB, truncated)

```xml
<Configuration_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:configurationdocument:3:0">
  <type>A95</type>
  <process.processType>A39</process.processType>
  <TimeSeries>
    <mRID>a805edf4304d4b7d</mRID>
    <businessType>B11</businessType>
    <implementation_DateAndOrTime.date>2019-01-01</implementation_DateAndOrTime.date>
    <biddingZone_Domain.mRID codingScheme="A01">10YGB----------A</biddingZone_Domain.mRID>
    <registeredResource.mRID codingScheme="A01">48WSTN0000ABRBON</registeredResource.mRID>
    <registeredResource.name>ABRBO</registeredResource.name>
    <registeredResource.location.name>GB</registeredResource.location.name>
    <ControlArea_Domain><mRID codingScheme="A01">10YGB----------A</mRID></ControlArea_Domain>
    <Provider_MarketParticipant><mRID codingScheme="A01">48X000000000228R</mRID></Provider_MarketParticipant>
    <MktPSRType><psrType>B18</psrType></MktPSRType>
  </TimeSeries>
</Configuration_MarketDocument>
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsoe/generation_units_master_data/year=YYYY/month=MM/generation_units_master_data_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsoe.generation_units_master_data.GenerationUnitsMasterDataTransformer`
**Pydantic schema**: `gridflow.schemas.entsoe.EntsoeGenerationUnitsMasterData`
**Dedup key**: `(area_code, unit_mrid)` — registry, not time series. The dedup runs within one transform (`generation_units_master_data.py:68-69`); each requested date is written to its own file, so the table holds one copy of the register per request, told apart only by the lineage column `event_time` (the requested date, `silver/base.py:2221-2231`). Across the table the row key is `(event_time, area_code, unit_mrid)` (corrected 2026-09-29).
**Point-in-time field**: `implementation_datetime_utc`. It is the date column gridflow_models `query()` filters on (`gridflow/silver/schema_manifest.py:166`), so `query()` selects units by record date across every request, not one register; read one request with `data.sql(... WHERE event_time = ...)` (added 2026-09-29).

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| area_code | str | No | `<biddingZone_Domain.mRID>` | EIC |
| unit_mrid | str | No | `<registeredResource.mRID>` | Unit EIC — keep verbatim |
| unit_name | str | No | `<registeredResource.name>` | Default "" in canonical. Asset short name. |
| production_type | str | No | `<psrType>` | Default "" in canonical. EIC PSR type. |
| implementation_datetime_utc | datetime[UTC] | Yes | `<implementation_DateAndOrTime.date>` | UTC tz-aware |
| data_provider | str | No | constant | "entsoe" |
| ingested_at | datetime[UTC] | Yes | derived | When the silver transform ran: `datetime.now(UTC)`, the same on every row (`generation_units_master_data.py:71-75`), not the bronze fetch time |

### Silver sample

```python
[
    {
        "area_code": "10YGB----------A",
        "unit_mrid": "48WSTN0000ABRBON",
        "unit_name": "ABRBO",
        "production_type": "B18",
        "implementation_datetime_utc": "2019-01-01T00:00:00+00:00",
        "data_provider": "entsoe",
        "ingested_at": "2026-05-08T18:00:00+00:00",
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **`Implementation_DateAndOrTime` is a single date, not `periodStart`/`periodEnd`.** The connector special-cases this via `EntsoeDocType.date_param` and replaces the period range with a single ISO date. A naive `periodStart`/`periodEnd` call **will return EMPTY or 400**.
- **`BusinessType=B11` is required** — without it the request returns an Acknowledgement.
- Response root is `Configuration_MarketDocument`, **not** `Publication_MarketDocument` or `GL_MarketDocument`. Validation logic that hard-codes a single root element will reject this dataset.
- The parser uses a separate function `parse_generation_units_master_data_xml()` because the structure differs from time-series documents.
- Multiple `psrType` per unit is theoretically possible (multi-fuel) — silver keeps only the first.
- Some legacy units have `implementation_DateAndOrTime.date` as far back as 1960 (FR `LOGIS NEUF 2`, `17W000001017799C`, 1960-01-01, in the 2026-09-08 request's bronze; corrected 2026-09-29 from "1990"); check tz handling — they round-trip as UTC midnight.
- **`implementation_DateAndOrTime.date` is not a commissioning date; its vendor meaning is undocumented** (measured 2026-09-29 over the 2026-08-01 and 2026-09-08 requests). BE `EDF Luminus Seraing TGV` (`22W201806271---D`) is dated 2018-10-14 with 470 MW and three generating units in the 2026-08-01 response, and 2025-11-01 with 300 MW and two units in the 2026-09-08 response: the date moved when the record changed. Many units share placeholder-looking dates (2000-01-01; 2018-10-01 in DE-LU), and rows can be dated after the requested date (DE-LU `Nordseecluster A` 2026-09-12 in the 2026-09-08 request; BE `KALLO BESS` 2027-01-01 in both).
- **The XML carries more than silver keeps.** Each unit's `MktPSRType` holds `nominalIP_PowerSystemResources.nominalP` (MW, unit `MAW`), `production_PowerSystemResources.highVoltageLimit` (kV) and nested `GeneratingUnit_PowerSystemResources` (each with its own EIC, name, `nominalP` and PSR type). None is mapped into silver (`parsers.py:641-719`), so this table has no capacity; per-unit MW is in `installed_capacity_units` on the same `unit_mrid`. `ControlArea_Domain` and `Provider_MarketParticipant` are also dropped (added 2026-09-29).
- No size threshold is visible in the register: 139 of the 660 units in the 2026-09-08 response have a `nominalP` under 100 MW (measured 2026-09-29).

---

## Implementation delta

- Tuple verified 2026-05-08:
  - Docs (API guide §15.1.D / Static "Production and generation units"): `(documentType=A95, processType=n/a, BusinessType=B11, BiddingZone_Domain)`.
  - Code (`endpoints.py`): `("A95", None, BusinessType="B11", domain_style="bidding_zone", date_param="Implementation_DateAndOrTime")` → `BiddingZone_Domain`.
  - **Match.**
- The `date_param` mechanism is unique to A95 in `DOC_TYPES`. Anyone adding a new dataset with a similar non-period parameter must reuse this pattern.

---

## Modelling notes

- **Cross-vendor ID mapping** — join unit_mrid ↔ Elexon BM unit IDs via name fuzzy match (e.g. `bmunits_reference`).
- ~~Asset commissioning timeline — `implementation_datetime_utc` for new-build curves.~~ Wrong: the date is not a commissioning date (see Known issues; corrected 2026-09-29). Do not build a new-build curve from it.
- Production-type registry by zone — for capacity-mix dashboards.

---

## Links

- [Official API docs](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.pdf)
- `OneDrive/Desktop/Python/gridflow/src/gridflow/connectors/entsoe/client.py`
- `OneDrive/Desktop/Python/gridflow/src/gridflow/silver/entsoe/generation_units_master_data.py`
- `OneDrive/Desktop/Python/gridflow/src/gridflow/schemas/entsoe.py`
- Gold view/builder
