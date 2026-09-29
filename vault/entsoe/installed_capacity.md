---
source: entsoe
dataset_key: installed_capacity
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Installed capacity per production type
  summary: >-
    ENTSO-E's installed generation capacity for each bidding zone: one MW figure per production
    type for the year, from document type A68.
  facts:
    vendor: ENTSO-E Transparency Platform, document type A68, process type A33
    cadence: "One `P1Y` point per year, as sent in these responses"
    grain: One row per year, bidding zone and production type code, per silver file
  landscape: power
  what_it_is: >-
    ENTSO-E's installed capacity per bidding zone and production type: a single annual snapshot,
    one MW figure per type. 2026's is stamped 23:00 UTC on 31 December 2025. Of six zones
    requested, GB and IE-SEM return no-data acknowledgements in these responses. A type may come as
    0 MW or be absent: the 2026 document has DE-LU B07 at 0, no B14.
  how_used:
    - "The denominator for load factors: `actual_generation` MW over installed MW, per type."
    - Sizing each zone's wind, solar and storage fleet for a scenario or merit order.
    - Scaling a wind or solar forecast error by the installed MW behind it.
  chart:
    type: bar
    silver: entsoe/installed_capacity
    value: capacity_mw
    filter:
      - {column: area_code, op: eq, value: "10Y1001A1001A82H"}
      - {column: timestamp_utc, op: eq, value: "2025-12-31T23:00:00Z"}
    dedup: {on: [timestamp_utc, area_code, production_type], order_by: published_at}
    group: production_type
    group_map:
      B16: solar
      B18: wind
      B19: wind
      B04: gas
      B02: coal
      B03: coal
      B05: coal
      B10: storage
      B25: storage
      B01: biomass
      B06: misc
      B07: misc
      B08: misc
      B09: misc
      B13: misc
      B15: misc
      B17: misc
      B11: hydro
      B12: hydro
      B20: other
    aggregation: sum
    sort: value_desc
    unit: MW
  chart_view:
    title: DE-LU installed capacity by type, 2026
    caption: >-
      Silver `entsoe/installed_capacity`, MW, zone DE-LU, the 2026 figure (stamped 23:00 UTC on
      31 December 2025). Each silver file repeats it; one copy is kept, then codes in a group are
      summed. DE-LU sends no nuclear (B14) row.
    alt: >-
      Bar chart of DE-LU installed generation capacity for 2026 from entsoe/installed_capacity, in
      MW, one bar per type group, largest first: solar 104,030; wind, onshore and offshore, 77,149;
      gas 35,678; coal and lignite 31,907; pumped and other storage 23,428; biomass 8,856; oil,
      waste, geothermal and other renewables 6,287; non-pumped hydro 5,576; other 2,030. The nine
      bars sum to 294,941 MW.
    key:
      - {series: solar, label: Solar, codes: B16}
      - {series: wind, label: Wind, codes: "B18, B19", note: "Offshore (B18) and onshore (B19) summed."}
      - {series: gas, label: Gas, codes: B04}
      - {series: coal, label: Coal and lignite, codes: "B02, B05, B03", paint: hatch-cross, note: "Lignite (B02), hard coal (B05) and coal-derived gas (B03) summed."}
      - {series: storage, label: Storage, codes: "B10, B25", paint: hatch-dots, note: "Hydro pumped storage (B10) and ENTSO-E's energy storage code (B25) summed."}
      - {series: biomass, label: Biomass, codes: B01}
      - {series: misc, label: "Oil, waste, others", codes: "B06, B07, B08, B09, B13, B15, B17", paint: hatch-vertical, note: "B06 oil, B09 geothermal, B15 other renewable, B17 waste; B07, B08, B13 at 0 MW."}
      - {series: hydro, label: "Hydro, not pumped", codes: "B11, B12", paint: hatch-lines, note: "Run-of-river (B11) and reservoir (B12)."}
      - {series: other, label: Other, codes: B20, note: "ENTSO-E's own code Other; what it holds is undocumented."}
  raw_feed:
    note: >-
      One GET per bidding zone and UTC day. In these responses a one-day request returns the whole
      year's document, so every day's bronze file repeats it.
    requests:
      - "GET https://web-api.tp.entsoe.eu/api?documentType=A68&periodStart=202609140000&periodEnd=202609150000&in_Domain=10Y1001A1001A82H&processType=A33&securityToken=$ENTSOE_API_KEY"
    commands:
      - {run: gridflow ingest entsoe installed_capacity --start 2026-09-14 --end 2026-09-15, comment: "bronze; one day, end excluded"}
      - {run: gridflow transform entsoe installed_capacity --start 2026-09-14 --end 2026-09-14, comment: "bronze to silver; end included"}
  record:
    select:
      filter:
        - {column: area_code, op: eq, value: "10YNL\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DL"}
        - {column: production_type, op: in, value: [B02, B04, B10, B14, B16, B18, B19, B20]}
      dedup: {on: [timestamp_utc, area_code, production_type], order_by: published_at}
      order_by: [production_type]
      columns: [timestamp_utc, area_code, production_type, capacity_mw, resolution, published_at]
    key: [timestamp_utc, area_code, production_type]
    caption: "NL's 2026 figures for eight codes, one copy each: B02 and B10 are sent as 0."
    fields:
      timestamp_utc: "Period start, UTC: 2025-12-31 23:00 is midnight CET, the start of 2026"
      area_code: "Bidding zone EIC, from `inBiddingZone_Domain.mRID`"
      production_type: "ENTSO-E production type (PSR) code, from `MktPSRType/psrType` as sent"
      capacity_mw: "Installed MW (`MAW`) from `quantity`, for the zone, type and year"
      resolution: "Point length as sent; `P1Y` in these rows"
      published_at: "Response `createdDateTime`, UTC: a fetch-time stamp, within seconds of gridflow's request"
  notebook:
    lead: >-
      `query()` reads `silver_entsoe_installed_capacity` by whole UTC days of `timestamp_utc`, ends
      included, without lineage columns. The 2026 row is stamped 31 December 2025 whatever day you
      ingest, so query that day, then drop per-file duplicates.
    cells:
      - |
        df = data.entsoe.query("installed_capacity", "2025-12-31", "2025-12-31")
        key = ["timestamp_utc", "area_code", "production_type"]
        df = df.sort_values("published_at").drop_duplicates(subset=key, keep="last")
      - "zones = {'10Y1001A1001A82H': 'DE-LU', '10YFR-RTE\x2D\x2D\x2D\x2D\x2D\x2DC': 'FR',\n         '10YNL\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DL': 'NL', '10YBE\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D2': 'BE'}\nwide = (df.pivot_table(index='production_type', columns='area_code', values='capacity_mw')\n          .rename(columns=zones).rename_axis(index=None, columns=None))\nwide"
      - |
        types = {"B04": "gas", "B14": "nuclear", "B16": "solar", "B19": "wind onshore", "B18": "wind offshore"}
        mix = wide.loc[list(types)].rename(index=types).T
        mix.plot.bar(ylabel="MW", rot=0, figsize=(8, 3.5))
    needs: one day of 2026, for example 14 September
    plot_alt: >-
      Grouped bar chart of 2026 capacity_mw by zone (DE-LU, BE, FR, NL) for gas, nuclear, solar,
      onshore and offshore wind. DE-LU solar is tallest at about 104,000 MW, then DE-LU onshore
      wind near 68,000 and FR nuclear near 63,000. DE-LU has no nuclear bar; every BE bar is under
      12,000 MW.
  related:
    - {dataset: entsoe/actual_generation, note: "Realised MW by the same type codes; divide for load factors"}
    - {dataset: entsoe/installed_capacity_units, note: "Installed capacity per production unit (A71), not per type"}
    - {dataset: entsoe/wind_solar_forecast, note: "Wind and solar forecasts to scale by B16, B18 and B19"}
    - {dataset: elexon/bmunits_reference, note: "GB capacity by unit, since this feed returns no GB rows"}
---

# ENTSO-E — Installed generation capacity aggregated (A68/A33)

## Overview

Installed generation capacity in MW per bidding zone, aggregated by EIC
production type. Published yearly. Used as the structural denominator for
capacity-factor models, scenario builds, and to track new-build / closure
trends. Process type `A33` denotes "year-ahead" reference.

→ [Installed capacity per unit](installed_capacity_units.md), [Generation units master data](generation_units_master_data.md)

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
| Historical depth | ~2014 onwards |
| Publication lag  | yearly publication, around start of year |
| Response format  | XML — root `GL_MarketDocument` |
| Document type    | A68 |
| Process type     | A33 (year-ahead reference) |
| Business type    | n/a |
| Domain param name| `in_Domain` |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `documentType` | str | yes | `A68` | `A68` |
| `processType` | str | yes | `A33` | `A33` |
| `in_Domain` | EIC | yes | Bidding zone | `10Y1001A1001A82H` |
| `periodStart` | str | yes | UTC `yyyymmddhhmm`, year boundary | `202601010000` |
| `periodEnd` | str | yes | UTC `yyyymmddhhmm`, year boundary | `202612310000` |

### Working curl example

```bash
curl --ssl-no-revoke -fsS \
  "https://web-api.tp.entsoe.eu/api?securityToken=$ENTSOE_API_KEY&documentType=A68&processType=A33&in_Domain=10Y1001A1001A82H&periodStart=202601010000&periodEnd=202612310000" \
  -H "Accept: application/xml"
```

Live verification 2026-05-08:
- GB yearly window: HTTP 200, **EMPTY** (Ack 999 "INSTALLED_GENERATION_CAPACITY_AGGREGATED_R3 [14.1.A]"). Brexit-GB.
- DE-LU yearly window: HTTP 200, **PASS** — `GL_MarketDocument`, 20 TimeSeries (one per production type).

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsoe/installed_capacity/<year>/<month>/<day>/raw_<uuid>.xml`
**Format**: Raw XML, immutable.
**Granularity**: One file per zone per requested UTC day (`connectors/entsoe/client.py` `fetch`, `day_subwindows`); each day's reply carries the whole-year document.

### Bronze sample (DE-LU, truncated)

```xml
<GL_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0">
  <type>A68</type>
  <process.processType>A33</process.processType>
  <TimeSeries>
    <businessType>A37</businessType>
    <inBiddingZone_Domain.mRID>10Y1001A1001A82H</inBiddingZone_Domain.mRID>
    <quantity_Measure_Unit.name>MAW</quantity_Measure_Unit.name>
    <MktPSRType><psrType>B16</psrType></MktPSRType>
    <Period>
      <resolution>P1Y</resolution>
      <Point><position>1</position><quantity>104029.51</quantity></Point>
    </Period>
  </TimeSeries>
</GL_MarketDocument>
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsoe/installed_capacity/year=YYYY/month=MM/installed_capacity_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsoe.installed_capacity.InstalledCapacityTransformer`
**Pydantic schema**: `gridflow.schemas.entsoe.EntsoeInstalledCapacity`
**Dedup key**: `(timestamp_utc, area_code, production_type)`
**Point-in-time field**: `published_at`, the response `createdDateTime`: a fetch-time stamp (`silver/entsoe/installed_capacity.py:85`)

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| timestamp_utc | datetime[UTC] | No | Period start | Year boundary, P1Y resolution |
| area_code | str | No | `<inBiddingZone_Domain.mRID>` | EIC |
| production_type | str | No | `<MktPSRType><psrType>` | EIC PSR type |
| capacity_mw | float | No | `<Point><quantity>` | MW |
| resolution | str | No | parsed | Default "" in canonical. `P1Y`. |
| published_at | datetime[UTC] | Yes | `<createdDateTime>` | Fetch-time stamp (`_published_at.py`) |
| data_provider | str | No | constant | "entsoe" |

### Silver sample

```python
[
    {
        "timestamp_utc": "2025-12-31T23:00:00+00:00",
        "area_code": "10Y1001A1001A82H",
        "production_type": "B16",
        "capacity_mw": 104029.51,
        "resolution": "P1Y",
        "data_provider": "entsoe",
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **A one-day window is enough.** gridflow requests one UTC day per zone, and each reply for a day in 2026 carried the whole 2026 document (period 2025-12-31T23:00Z to 2026-12-31T23:00Z), so every daily silver file repeats the same rows; the dedup key holds within one file only.
- **GB EMPTY post-Brexit.** GB capacity registry is via Elexon and DUKES.
- A68 is yearly snapshot — values change at year boundaries; intra-year ingestion just rewrites the same data.
- Distinct from `installed_capacity_units` (A71/A33) which gives unit-level breakdown. Same `processType` A33 but different documentType.

---

## Implementation delta

- Tuple verified 2026-05-08:
  - Docs (API guide §14.1.A): `(documentType=A68, processType=A33, businessType=n/a, in_Domain)`.
  - Code: `("A68", "A33", -, domain_style="in_domain")` → `in_Domain`.
  - **Match.**
- `max_query_days: 365` in `config/sources.yaml` is appropriate for yearly publication.

---

## Modelling notes

- Capacity-factor denominators per production type per zone per year.
- Capacity-mix scenario builds (closure / new-build trajectories).
- Combine with `actual_generation` (A75) for utilisation rates.

---

## Links

- [Official API docs](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.pdf)
- `OneDrive/Desktop/Python/gridflow/src/gridflow/connectors/entsoe/client.py`
- `OneDrive/Desktop/Python/gridflow/src/gridflow/silver/entsoe/installed_capacity.py`
- `OneDrive/Desktop/Python/gridflow/src/gridflow/schemas/entsoe.py`
- Gold view/builder
