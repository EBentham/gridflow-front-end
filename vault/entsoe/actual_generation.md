---
source: entsoe
dataset_key: actual_generation
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Generation per production type
  summary: >-
    ENTSO-E's realised generation for each bidding zone: one MW figure per production type
    and time step, from document type A75.
  facts:
    vendor: ENTSO-E Transparency Platform, document type A75, process type A16
    cadence: "As sent in these responses: 15-minute DE-LU, FR, NL; half-hourly IE-SEM; hourly BE"
    grain: One row per time step, bidding zone and production type code
  landscape: power
  what_it_is: >-
    ENTSO-E's realised output per bidding zone and time step, one MW figure per production type
    code, B01 biomass to B25. gridflow requests six zones; GB comes back as a
    no-data acknowledgement, so GB's mix is Elexon `fuelhh`. For some types ENTSO-E also sends a
    consumption series; silver folds both onto one key, so `generation_mw` may be the consumption
    figure, unmarked.
  how_used:
    - DE-LU fuel mix without pumped storage, as charted, for a price model.
    - Wind and solar outturn to score `wind_solar_forecast`, where no consumption series is sent.
    - Comparing DE-LU's fuel mix with GB's, which comes from Elexon `fuelhh`.
  chart:
    type: stacked-area
    silver: entsoe/actual_generation
    time: timestamp_utc
    value: generation_mw
    filter:
      - {column: area_code, op: eq, value: "10Y1001A1001A82H"}
      - {column: production_type, op: ne, value: B10}
    group: production_type
    group_map:
      B01: biomass
      B11: hydro
      B12: hydro
      B02: lignite
      B03: hard_coal
      B05: hard_coal
      B06: misc
      B09: misc
      B15: misc
      B17: misc
      B20: other
      B04: gas
      B18: wind
      B19: wind
      B16: solar
    series_order: [biomass, hydro, lignite, hard_coal, misc, other, gas, wind, solar]
    aggregation: sum
    window: {start: "2026-09-12", end: "2026-09-18"}
    unit: MW
  chart_view:
    title: DE-LU generation by type, 12 to 18 September 2026
    caption: >-
      Silver `entsoe/actual_generation`, MW, every quarter-hour of 12 to 18 September 2026 UTC,
      zone DE-LU only, codes in a group summed. Pumped storage (B10) is left out: silver cannot
      separate its generation from its consumption.
    alt: >-
      Stacked area chart of DE-LU generation by production type from entsoe/actual_generation, in
      MW, for every quarter-hour of 12 to 18 September 2026 UTC, pumped storage left out. From zero
      upward: biomass (3.6 to 4.4 GW), non-pumped hydro, lignite (4.3 to 12.4 GW), hard coal and
      coal gas, oil, waste, geothermal and other renewables, other, gas (1.3 to 9.6 GW), wind (1.7 to 27.1 GW)
      and solar, which peaks each midday, up to 48.9 GW on the 15th. The stack runs from 30.1 to
      75.6 GW.
    x_label: date, UTC; quarter-hours as sent
    key:
      - {series: solar, label: Solar, codes: B16, tag: solar}
      - {series: wind, label: Wind, codes: "B18, B19", tag: wind, note: "Offshore (B18) and onshore (B19) summed."}
      - {series: gas, label: Gas, codes: B04, tag: gas}
      - {series: other, label: Other, codes: B20, note: "ENTSO-E's own code Other; what it holds is undocumented."}
      - {series: misc, label: "Oil, waste, other renewables", codes: "B06, B09, B15, B17", paint: hatch-vertical, note: "B06 oil, B09 geothermal, B15 ENTSO-E's other renewable, B17 waste."}
      - {series: hard_coal, label: "Hard coal, coal gas", codes: "B05, B03", paint: hatch-cross}
      - {series: lignite, label: Lignite, codes: B02, paint: hatch-dots, tag: lignite}
      - {series: hydro, label: "Hydro, not pumped", codes: "B11, B12", paint: hatch-lines, note: "Run-of-river (B11) and reservoir (B12)."}
      - {series: biomass, label: Biomass, codes: B01, tag: biomass}
  raw_feed:
    note: >-
      From the ENTSO-E web API, one request per bidding zone and UTC day. `gridflow ingest` writes
      each XML response to bronze; `gridflow transform` types it into silver.
    requests:
      - "GET https://web-api.tp.entsoe.eu/api?documentType=A75&periodStart=202609180000&periodEnd=202609190000&in_Domain=10Y1001A1001A82H&processType=A16&securityToken=$ENTSOE_API_KEY"
    commands:
      - {run: gridflow ingest entsoe actual_generation --start 2026-09-12 --end 2026-09-19, comment: "bronze; the end is exclusive"}
      - {run: gridflow transform entsoe actual_generation --start 2026-09-12 --end 2026-09-18, comment: bronze to silver}
  record:
    select:
      filter:
        - {column: area_code, op: eq, value: "10Y1001A1001A82H"}
        - {column: timestamp_utc, op: eq, value: "2026-09-18T12:00:00Z"}
        - {column: production_type, op: in, value: [B02, B04, B05, B10, B16, B18, B19, B20]}
      order_by: [production_type]
      columns: [timestamp_utc, area_code, production_type, generation_mw, resolution, published_at, area_name]
    key: [timestamp_utc, area_code, production_type]
    caption: "DE-LU at 12:00 UTC on 18 September 2026: 8 of its 16 codes."
    fields:
      timestamp_utc: "Step start: period start plus (position minus 1) times `resolution`, UTC"
      area_code: "Bidding zone EIC, from `inBiddingZone_Domain` or `outBiddingZone_Domain`; silver cannot tell which"
      production_type: "ENTSO-E production type (PSR) code, as sent"
      generation_mw: "MW (`MAW`); may be the consumption series; B10 here is pumping load"
      resolution: "Step as sent: `PT15M`, `PT30M` or `PT60M`"
      published_at: "Response `createdDateTime`: a fetch-time stamp, within seconds of gridflow's request"
      area_name: "Zone name from gridflow's EIC lookup; empty for codes outside it"
  notebook:
    lead: >-
      Returns a pandas DataFrame from the DuckDB relation `silver_entsoe_actual_generation`,
      filtered on `timestamp_utc` as whole UTC days with both ends included. Lineage columns are
      dropped.
    cells:
      - |
        df = data.entsoe.query("actual_generation", "2026-09-12", "2026-09-18")
        df["timestamp_utc"] = df["timestamp_utc"].dt.tz_convert("UTC")
      - df.sort_values(["timestamp_utc", "area_code", "production_type"])[["timestamp_utc", "area_code", "production_type", "generation_mw"]].head()
      - |
        solar = df[(df.area_code == "10Y1001A1001A82H") & (df.production_type == "B16")].sort_values("timestamp_utc")
        solar.plot(x="timestamp_utc", y="generation_mw", ylabel="MW",
                   color="#155A6E", figsize=(8, 3.5))
    needs: 12 to 18 September 2026
    plot_alt: >-
      Line plot of DE-LU solar (B16) generation_mw against timestamp_utc for 12 to 18 September
      2026: near zero every night and one peak each day between 10:00 and 12:00 UTC, from about
      22,000 MW on the 13th to about 48,900 MW on the 15th.
  related:
    - {dataset: elexon/fuelhh, note: "GB generation by fuel, which this feed does not carry"}
    - {dataset: entsoe/wind_solar_forecast, note: "Day-ahead forecast of B16, B18 and B19 to score against this"}
    - {dataset: entsoe/actual_load, note: "Realised load for the same zones; less wind and solar, residual load"}
    - {dataset: entsoe/installed_capacity, note: "Capacity per production type; divide to get load factors"}
---

# ENTSO-E — Actual generation per production type (A75/A16)

## Overview

Actual realised generation in MW for each EIC bidding zone broken down by
PSR (Primary Source) production type — coal, gas, wind onshore, wind
offshore, solar, hydro, nuclear, biomass, etc. Published per settlement
period (PT15M / PT30M / PT60M depending on zone). Used to back out the
realised fuel mix, regress wind/solar against weather drivers, and
cross-check with national TSO publications. Underpins residual-load
modelling — `actual_load - wind - solar` is a standard MEF feature.

→ [Cross-border flows](cross_border_flows.md), [Wind/solar forecast](wind_solar_forecast.md)

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | https://web-api.tp.entsoe.eu |
| Path             | /api |
| Method           | GET |
| Auth             | query param `securityToken=$ENTSOE_API_KEY` |
| Rate limit       | not documented — code uses 1 req/s, polite default |
| Pagination       | None (response truncates at 200 TimeSeries with HTTP 400 reason 999) |
| Historical depth | 2014-12-05 onwards (varies by area) |
| Publication lag  | T+1 hour to T+24 hours depending on zone |
| Response format  | XML — root `GL_MarketDocument` |
| Document type    | A75 |
| Process type     | A16 (realised) |
| Business type    | `A01` on every TimeSeries in bronze (all five zones, 2026-09-15). The side is the domain tag, not the business type: `inBiddingZone_Domain.mRID` series are generation, `outBiddingZone_Domain.mRID` series the consumption side. Vendor: ENTSO-E's Postman collection "Transparency Platform Restful API" (https://documenter.getpostman.com/view/7009892/2s93JtP3F6), item "16.1.B&C Actual Generation per Production Type": `inBiddingZone_Domain` series carry generation, `outBiddingZone_Domain` series carry consumption (read by the page checker 2026-09-29; the page renders client-side). Also consistent with entsoe-py `parsers.py` and with B10 values (see Known issues). |
| Domain param name| `in_Domain` (single area) |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `documentType` | str | yes | Always `A75` | `A75` |
| `processType` | str | yes | `A16` for realised | `A16` |
| `in_Domain` | EIC | yes | Bidding zone EIC | `10YGB----------A` |
| `periodStart` | str | yes | UTC `yyyymmddhhmm` | `202605060000` |
| `periodEnd` | str | yes | UTC `yyyymmddhhmm` | `202605070000` |
| `psrType` | str | no | Filter to one production type | `B16` |

### Working curl example

```bash
curl --ssl-no-revoke -fsS \
  "https://web-api.tp.entsoe.eu/api?securityToken=$ENTSOE_API_KEY&documentType=A75&processType=A16&in_Domain=10Y1001A1001A82H&periodStart=202605060000&periodEnd=202605070000" \
  -H "Accept: application/xml"
```

Live verification 2026-05-08:
- GB (`10YGB----------A`): HTTP 200, **EMPTY** — `Acknowledgement_MarketDocument` reason 999 "No matching data found for AGGREGATED_GENERATION_PER_TYPE_R3 [16.1.B&C]". GB stopped publishing this dataset to ENTSO-E post-Brexit.
- DE-LU (`10Y1001A1001A82H`): HTTP 200, **PASS** — `GL_MarketDocument`, 17 TimeSeries (one per production type).

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsoe/actual_generation/<year>/<month>/<day>/raw_<uuid>.xml`
**Format**: Raw XML, as-received. Immutable.
**Granularity**: One XML file per (zone, day) — connector iterates over `DEFAULT_ZONES`.

### Bronze sample (DE-LU 2026-05-06, truncated)

```xml
<GL_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0">
  <mRID>...</mRID>
  <type>A75</type>
  <process.processType>A16</process.processType>
  <createdDateTime>2026-05-06T03:00Z</createdDateTime>
  <TimeSeries>
    <mRID>1</mRID>
    <businessType>A03</businessType>
    <inBiddingZone_Domain.mRID codingScheme="A01">10Y1001A1001A82H</inBiddingZone_Domain.mRID>
    <quantity_Measure_Unit.name>MAW</quantity_Measure_Unit.name>
    <MktPSRType><psrType>B19</psrType></MktPSRType>
    <Period>
      <timeInterval><start>2026-05-05T22:00Z</start><end>2026-05-06T22:00Z</end></timeInterval>
      <resolution>PT15M</resolution>
      <Point><position>1</position><quantity>0</quantity></Point>
      ...
    </Period>
  </TimeSeries>
</GL_MarketDocument>
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsoe/actual_generation/year=YYYY/month=MM/actual_generation_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsoe.actual_generation.ActualGenerationTransformer`
**Pydantic schema**: `gridflow.schemas.entsoe.EntsoeActualGeneration`
**Dedup key**: `(timestamp_utc, area_code, production_type)`
**Point-in-time field**: none in effect. `published_at` is the document `createdDateTime` (`silver/entsoe/actual_generation.py:90-91`), a fetch-time stamp within seconds of gridflow's request, not when ENTSO-E published the values; revisions overwrite, as dedup keeps the last row read (`actual_generation.py:80`)

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| timestamp_utc | datetime[UTC] | No | `<Period>` start + (position - 1) * resolution (`connectors/entsoe/parsers.py:530`) | tz-aware UTC; PT15M / PT30M / PT60M resolution |
| area_code | str | No | `<inBiddingZone_Domain.mRID>` or `<outBiddingZone_Domain.mRID>` | EIC bidding zone code. The parser reads both tags into the same field (`connectors/entsoe/parsers.py:289-297`), so a consumption series lands on the same key as generation. |
| area_name | str | No | derived | Filled from the EIC via `connectors/entsoe/area_codes.py` (`actual_generation.py:66-72`); "" for codes outside that map. |
| production_type | str | No | `<MktPSRType><psrType>` | ENTSO-E PSR type code (B01..B25); see PSR codes below |
| generation_mw | float | No | `<Point><quantity>` | Renamed from `value`; MW (XML unit `MAW`). For a type that also has a consumption series, holds one of the two figures (see Known issues). |
| resolution | str | No | `<Period><resolution>` | As sent: `PT15M` (DE-LU, FR, NL), `PT30M` (IE-SEM), `PT60M` (BE) in bronze 2026-09-15 |
| published_at | datetime[UTC] | Yes | document `<createdDateTime>` | `silver/entsoe/_published_at.py`; a fetch-time stamp, within seconds of gridflow's request (DE-LU 2026-09-15: `createdDateTime` 2026-09-21T10:06:50Z, bronze `fetched_at` 10:06:51.8Z), not a publication time |
| data_provider | str | No | constant | "entsoe" |
| ingested_at | datetime[UTC] | No | derived | When the silver transform ran (`actual_generation.py:82-87`) |

### PSR codes (production types)

Official ENTSO-E code list v36r0, as cached in gridflow `.planning/audit/2026-05-31-vendor-truth-audit/vendor-docs/entsoe-codes.md` §6: B01 Biomass, B04 Fossil Gas, B05 Fossil Hard coal, B09 Geothermal, B10 Hydro Pumped Storage, B11 Hydro Run-of-river, B12 Hydro Water Reservoir, B13 Marine, B14 Nuclear, B15 Other renewable, B16 Solar, B17 Waste, B18 Wind Offshore, B19 Wind Onshore, B20 Other. The cache omits B02, B03, B06, B07, B08 and B25. Vendor: ENTSO-E's Postman collection "Transparency Platform Restful API" (https://documenter.getpostman.com/view/7009892/2s93JtP3F6), `psrType` parameter list: B02 Fossil Brown coal/Lignite, B03 Fossil Coal-derived gas, B06 Fossil Oil, B20 Other, B25 Energy storage (read by the page checker 2026-09-29). B07 Fossil Oil shale and B08 Fossil Peat are from entsoe-py `mappings.py` `PSRTYPE_MAPPINGS` only (de facto).

### Silver sample

```python
[
    {
        "timestamp_utc": "2026-05-05T22:00:00+00:00",
        "area_code": "10Y1001A1001A82H",
        "area_name": "",
        "production_type": "B19",
        "generation_mw": 0.0,
        "data_provider": "entsoe",
    },
    {
        "timestamp_utc": "2026-05-05T22:15:00+00:00",
        "area_code": "10Y1001A1001A82H",
        "area_name": "",
        "production_type": "B16",
        "generation_mw": 1843.5,
        "data_provider": "entsoe",
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **GB EMPTY post-Brexit.** GB ceased publishing aggregated generation to ENTSO-E after the GB exit from the IEM. Use Elexon `fuelhh` / `fuelinst` for GB fuel mix instead.
- Resolution varies by zone — in bronze (2026-09-15) DE-LU, FR and NL send PT15M, IE-SEM PT30M, BE PT60M. Don't assume hourly when joining.
- Multiple revisions of the same period — silver dedup keeps the **last** seen row; silver carries `published_at`, but it is the response `createdDateTime`, a fetch-time stamp, so it does not date revisions; older revisions are overwritten on re-ingest.
- `area_name` is populated from the EIC lookup (`actual_generation.py:66-72`); "" only for codes outside `area_codes.py`.
- **Generation and consumption collapse into one row (gridflow defect, measured 2026-09-29).** A75 sends a separate consumption series (`outBiddingZone_Domain.mRID`, `businessType` A01 like generation) for some types: in bronze 2026-09-15, DE-LU B10; FR B05, B10, B18, B25; BE B10; NL all ten types; IE-SEM eight. The parser reads both domain tags into `in_domain` (`connectors/entsoe/parsers.py:289-297`) and the dedup key `(timestamp_utc, area_code, production_type)` has no side (`actual_generation.py:80`), so only the last row read survives and nothing records which. Re-parsing all 24 bronze days with the gridflow parser: of 100,831 silver rows, 19,623 hold the consumption figure where a different generation figure exists, 11,193 hold generation, 2,752 have only a consumption series, 3,279 have both equal. Which side wins is effectively arbitrary and changes from day to day (DE-LU B10 holds generation on 2026-08-01..05, 09-07, 09-09, 09-11 and 09-13, consumption on every other day through 09-20). Example: DE-LU B10 at 2026-09-18 12:00Z, silver 4,055.19 MW = consumption; generation was 67.36 MW. DE-LU types other than B10 are clean (34,017 of 34,017 rows match the generation series). Fix needs the side in the key.

---

## Implementation delta

- Tuple verified 2026-05-08:
  - Docs (API guide §16.1.B): `(documentType=A75, processType=A16, businessType=n/a, in_Domain)`.
  - Code (`endpoints.py:DOC_TYPES["actual_generation"]`): `("A75", "A16", -, domain_style="in_domain")` → query param `in_Domain`.
  - **Match.**
- `psrType` is a documented optional filter (per-production-type query) and is in `optional_params` (`connectors/entsoe/endpoints.py:37-43`); the default ingest does not send it.
- `area_name` field in `EntsoeActualGeneration` is filled by the transformer from the EIC lookup (`actual_generation.py:66-72`).

---

## Modelling notes

- Residual-demand and price models — `actual_load - actual_generation_renewables` is the standard residual-load feature.
- Wind/solar nowcast benchmarks — actual vs `wind_solar_forecast` for forecast skill.
- Production-type-conditional regressions (e.g. nuclear capacity factor).
- Filter on resolution before joining settlement-period datasets — DE-LU 15-min vs UK 30-min mismatch.

---

## Links

- [Official API docs](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.pdf)
- `OneDrive/Desktop/Python/gridflow/src/gridflow/connectors/entsoe/client.py`
- `OneDrive/Desktop/Python/gridflow/src/gridflow/silver/entsoe/actual_generation.py`
- `OneDrive/Desktop/Python/gridflow/src/gridflow/schemas/entsoe.py`
- Gold view/builder
