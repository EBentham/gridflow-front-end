---
source: entsoe
dataset_key: installed_capacity_units
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Installed capacity per production unit
  summary: >-
    ENTSO-E's year list of production units per bidding zone: each unit's EIC, name, production
    type and installed capacity in MW.
  facts:
    vendor: ENTSO-E Transparency Platform, document type A71, process type A33 (year ahead)
    cadence: One `P1Y` point per unit; a one-day request returned the whole year
    grain: One row per year, bidding zone, production unit and fetch
  landscape: units
  what_it_is: >-
    ENTSO-E's list of production units per bidding zone for one year, with each unit's EIC,
    name, production type and installed capacity in MW. A unit can hold several generating
    units; gridflow keeps the production unit only. gridflow asks per UTC day; the replies
    received each carried the whole year, so silver holds one copy per fetch, told apart by
    `published_at`.
  how_used:
    - Looking up a unit's installed capacity and production type by its EIC.
    - Setting per-unit output from `actual_generation_units` against each unit's capacity.
    - A starting point for matching GB units to Elexon BM unit IDs by name.
  chart:
    type: bar
    silver: entsoe/installed_capacity_units
    filter:
      - {column: timestamp_utc, op: eq, value: "2025-12-31T23:00:00Z"}
    dedup: {on: [area_code, unit_mrid], order_by: published_at}
    group: production_type
    group_map:
      B04: gas
      B18: wind
      B19: wind
      B10: hydro
      B11: hydro
      B12: hydro
      B14: nuclear
      B02: coal
      B03: coal
      B05: coal
      B06: oil
      B01: biomass
      B20: other
      B08: smaller
      B13: smaller
      B16: smaller
      B17: smaller
      B25: smaller
    aggregation: count
    sort: value_desc
    unit: production units
  chart_view:
    title: Production units by type, 2026 list, fetched 15 September 2026
    caption: >-
      Silver `entsoe/installed_capacity_units`, the 2026 year document as fetched on 15 September
      2026, six bidding zones: a count of production units per `psrType`, grouped as the key
      lists. Earlier fetches of each unit are dropped. Types are as ENTSO-E sends them.
    alt: >-
      Horizontal bar chart counting production units by type in the 2026 list of
      entsoe/installed_capacity_units, six bidding zones, as fetched on 15 September 2026. Fossil
      gas and wind are level at the top with 167 and 166 units, then hydro 133, nuclear 70, coal
      and lignite 50 and oil 26. The five smaller types together make 14, biomass 7 and ENTSO-E's
      Other code 6.
    key:
      - {series: gas, label: Fossil gas, codes: B04}
      - {series: wind, label: Wind, codes: "B18, B19", note: "Offshore (B18) and onshore (B19) counted together."}
      - {series: hydro, label: Hydro, codes: "B10, B11, B12", paint: hatch-lines, note: "Pumped storage (B10), run-of-river (B11) and reservoir (B12) counted together."}
      - {series: nuclear, label: Nuclear, codes: B14}
      - {series: coal, label: Coal and lignite, codes: "B02, B03, B05", paint: hatch-cross, note: "Lignite (B02), coal-derived gas (B03) and hard coal (B05) counted together."}
      - {series: oil, label: Oil, codes: B06, paint: hatch-dots}
      - {series: smaller, label: Five smaller types, codes: "B08, B13, B16, B17, B25", paint: hatch-vertical, note: "B08 peat per entsoe-py (IE-SEM's West Offaly, Edenderry, Lanesboro), with marine, solar, waste and storage."}
      - {series: biomass, label: Biomass, codes: B01}
      - {series: other, label: Other, codes: B20, note: "ENTSO-E's own code; what it holds is undocumented."}
  raw_feed:
    note: >-
      One GET per bidding zone per UTC day, six zones; the replies received carried the whole
      2026 document. `gridflow ingest` saves each reply to bronze; `gridflow transform` parses it.
    requests:
      - "GET https://web-api.tp.entsoe.eu/api?documentType=A71&periodStart=202609140000&periodEnd=202609150000&in_Domain=10YGB\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DA&processType=A33&securityToken=$ENTSOE_API_KEY"
    commands:
      - {run: gridflow ingest entsoe installed_capacity_units --start 2026-09-14 --end 2026-09-15, comment: "bronze; end date excluded"}
      - {run: gridflow transform entsoe installed_capacity_units --start 2026-09-14 --end 2026-09-14, comment: "bronze to silver; end included"}
  record:
    select:
      filter:
        - {column: unit_mrid, op: eq, value: "22W201806271\x2D\x2D\x2DD"}
        - {column: published_at, op: ge, value: "2026-08-16T13:43:46Z"}
        - {column: published_at, op: le, value: "2026-09-15T20:09:05Z"}
      order_by: [published_at]
      columns: [published_at, capacity_mw, unit_name, unit_mrid, area_code, production_type, timestamp_utc, resolution]
    key: [timestamp_utc, area_code, unit_mrid, published_at]
    caption: "Eight fetches of one Belgian gas unit, Seraing: 470 MW in August, 300 in September."
    fields:
      published_at: "Response `createdDateTime`, UTC: a fetch-time stamp that tells repeated fetches apart"
      capacity_mw: "Installed capacity in MW (`quantity`, sent as `MAW`); one point per unit"
      unit_name: "Production unit name as sent (`registeredResource.name`)"
      unit_mrid: "Production unit EIC (`registeredResource.mRID`); rows without one are dropped"
      area_code: "Bidding zone EIC (`inBiddingZone_Domain.mRID`), the zone requested"
      production_type: "PSR type code as sent (`psrType`), for example `B04`, fossil gas"
      timestamp_utc: "Year start, UTC: 23:00 on 31 December 2025 is midnight CET"
      resolution: "Period resolution code as sent: `P1Y`, one point per year"
  notebook:
    lead: >-
      Returns a pandas DataFrame from `silver_entsoe_installed_capacity_units`, filtered on
      `timestamp_utc` with both ends included; lineage columns are dropped. In the replies
      received each fetch added a full copy, so keep each unit's latest `published_at`.
    cells:
      - |
        df = data.entsoe.query("installed_capacity_units", "2025-12-31", "2025-12-31")
        latest = df.sort_values("published_at").drop_duplicates(["area_code", "unit_mrid"], keep="last")
      - latest[["area_code", "unit_mrid", "unit_name", "production_type", "capacity_mw"]].sort_values("capacity_mw", ascending=False).head()
      - latest["area_code"].value_counts()
    needs: one day's fetch of the 2026 list, 14 September 2026
  related:
    - {dataset: entsoe/installed_capacity, note: "Zone totals per production type for the same year, not per unit"}
    - {dataset: entsoe/generation_units_master_data, note: "Unit master data keyed on the same `unit_mrid`, with implementation dates"}
    - {dataset: entsoe/actual_generation_units, note: "Output per unit, keyed on the same kind of unit EIC (`unit_mrid`)"}
    - {dataset: elexon/bmunits_reference, note: "GB's BM unit register; names such as `ABRBO` recur in its IDs"}
---

# ENTSO-E — Installed capacity per production unit (A71/A33)

## Overview

Installed capacity in MW for each named generation unit per bidding zone,
broken out by EIC PSR production type. The unit-level twin of A68/A33.
One `P1Y` point per unit in the responses received (2026-09-29 check; no vendor update cadence verified). Used to look up nameplate capacity per unit, attribute
generation to specific assets, and to map asset names ↔ EIC mRIDs for
cross-referencing with `actual_generation_units` (A73) or master data
(A95).

→ [Installed capacity (aggregate)](installed_capacity.md), [Generation units master data](generation_units_master_data.md)

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | https://web-api.tp.entsoe.eu |
| Path             | /api |
| Method           | GET |
| Auth             | query param `securityToken=$ENTSOE_API_KEY` |
| Rate limit       | 1 req/s |
| Pagination       | None (large responses arrive in one document — 366 KB observed for GB) |
| Historical depth | yearly snapshots from ~2014 |
| Publication lag  | yearly publication |
| Response format  | XML — root `GL_MarketDocument` |
| Document type    | A71 |
| Process type     | A33 (year-ahead reference) |
| Business type    | n/a (per-TimeSeries `B11` — production unit) |
| Domain param name| `in_Domain` |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `documentType` | str | yes | `A71` | `A71` |
| `processType` | str | yes | `A33` | `A33` |
| `in_Domain` | EIC | yes | Bidding zone | `10YGB----------A` |
| `periodStart` | str | yes | UTC `yyyymmddhhmm` | `202601010000` |
| `periodEnd` | str | yes | UTC `yyyymmddhhmm` | `202612310000` |

### Working curl example

```bash
curl --ssl-no-revoke -fsS \
  "https://web-api.tp.entsoe.eu/api?securityToken=$ENTSOE_API_KEY&documentType=A71&processType=A33&in_Domain=10YGB----------A&periodStart=202601010000&periodEnd=202612310000" \
  -H "Accept: application/xml"
```

Live verification 2026-05-08:
- GB yearly window: HTTP 200, **PASS** — `GL_MarketDocument`, 230 TimeSeries (one per registered production unit). Each TimeSeries has `<registeredResource.mRID>` (EIC unit code) and `<registeredResource.name>` (asset short name e.g. "ABRBO", a `B18` wind offshore unit; Aberthaw B is a separate unit, `ABTHB`, `B05`, in the same document; corrected 2026-09-29 from bronze `2026/09/14/raw_20260915T200920Z_58ce819c.xml`).

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsoe/installed_capacity_units/<year>/<month>/<day>/raw_<uuid>.xml`
**Format**: Raw XML, immutable.
**Granularity**: One file per zone per requested UTC day: the connector splits every window into one-day requests (`connectors/entsoe/client.py:162`, `day_subwindows`). In the replies received (2026-08-16 and 2026-09-15 fetches) each one-day request returned the whole year document (`time_Period` 2025-12-31T23:00Z to 2026-12-31T23:00Z), so every ingest day holds a full copy.

### Bronze sample (GB 2026, truncated)

```xml
<GL_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0">
  <type>A71</type>
  <process.processType>A33</process.processType>
  <TimeSeries>
    <mRID>4207978978a44c9a</mRID>
    <businessType>B11</businessType>
    <objectAggregation>A06</objectAggregation>
    <inBiddingZone_Domain.mRID codingScheme="A01">10YGB----------A</inBiddingZone_Domain.mRID>
    <registeredResource.mRID codingScheme="A01">48WSTN0000ABRBON</registeredResource.mRID>
    <registeredResource.name>ABRBO</registeredResource.name>
    <quantity_Measure_Unit.name>MAW</quantity_Measure_Unit.name>
    <MktPSRType><psrType>B18</psrType></MktPSRType>
    ...
  </TimeSeries>
</GL_MarketDocument>
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsoe/installed_capacity_units/year=YYYY/month=MM/installed_capacity_units_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsoe.installed_capacity_units.InstalledCapacityUnitsTransformer`
**Pydantic schema**: `gridflow.schemas.entsoe.EntsoeInstalledCapacityUnits`
**Dedup key**: `(timestamp_utc, area_code, unit_mrid)`, applied within one transform day only (`silver/entsoe/installed_capacity_units.py:74-77`). Each ingest day writes its own silver file with a full copy of the year document, so across days a unit repeats; `published_at` tells the copies apart.
**Point-in-time field**: `published_at`, the response `createdDateTime` (`installed_capacity_units.py:88`, `_published_at.py`): a fetch-time stamp. `available_at` equals it; `ingested_at` is the silver transform time (`installed_capacity_units.py:79-83`).

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| timestamp_utc | datetime[UTC] | No | Period start | Yearly P1Y resolution; 2025-12-31T23:00Z (midnight CET) for the 2026 document |
| area_code | str | No | `<inBiddingZone_Domain.mRID>` | EIC |
| production_type | str | No | `<MktPSRType><psrType>` | EIC PSR type; codes as listed in [actual_generation](actual_generation.md) "PSR codes" (ENTSO-E code list v36r0 and Postman `psrType` list; B08 Fossil Peat from entsoe-py only; in the 2026 document its three units are IE-SEM `West Offaly Production`, `Edenderry Prod` and `Lanesboro Production`, consistent with peat). The 2026 document uses B01 to B06, B08, B10 to B14, B16 to B20, B25. |
| unit_mrid | str | No | `<registeredResource.mRID>` | Unit EIC — keep verbatim |
| unit_name | str | No | `<registeredResource.name>` | Default "" in canonical. Asset short name. |
| capacity_mw | float | No | `<Point><quantity>` | MW |
| resolution | str | No | parsed | Default "" in canonical. `P1Y`. |
| published_at | datetime[UTC] | Yes | `<createdDateTime>` | Fetch-time stamp; distinguishes repeated fetches (`installed_capacity_units.py:88`) |
| data_provider | str | No | constant | "entsoe" |
| ingested_at | datetime[UTC] | Yes | derived | optional |

### Silver sample

```python
[
    {
        "timestamp_utc": "2025-12-31T23:00:00+00:00",
        "area_code": "10YGB----------A",
        "production_type": "B18",
        "unit_mrid": "48WSTN0000ABRBON",
        "unit_name": "ABRBO",
        "capacity_mw": 99.0,
        "resolution": "P1Y",
        "published_at": "2026-09-15T20:09:21+00:00",
        "data_provider": "entsoe",
        "ingested_at": "2026-09-15T20:09:28.630326+00:00",
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **GB still publishes A71/A33** — capacity per unit is part of network code obligations and survives Brexit, unlike most operational A75/A73 datasets. Use this instead of A68/A33 (aggregate) which **does** EMPTY for GB.
- **One day is enough.** `max_query_days: 365` in `sources.yaml` does not produce a yearly request: the connector splits any window into UTC-day requests (`connectors/entsoe/client.py:162`), and in the replies received each one returned the whole year document. A one-year window makes about 365 requests per zone (differing only in `periodStart`/`periodEnd`); if each returns the same document, as all replies seen so far did, that is 365 silver copies. Keep each unit's latest `published_at` when reading more than one day.
- **The year document can change between fetches.** BE unit `22W201806271---D` (EDF Luminus Seraing TGV, `B04`) was 470 MW in the 2026-08-16 fetches and 300 MW in the 2026-09-15 fetches of the same 2026 document; every other unit was unchanged (bronze `2026/08/*` against `2026/09/*`, checked 2026-09-29).
- **The parser keeps the production unit only.** Each TimeSeries also carries `production_PowerSystemResources.highVoltageLimit` (kV), `nominalIP_PowerSystemResources.nominalP` (equal to the point quantity in the 2026 document) and one or more `PowerSystemResources` children (the generating units, each with `mRID`, `name`, `nominalP`). `parse_timeseries_xml` reads only `psrType` from `MktPSRType` (`connectors/entsoe/parsers.py:345-348`), so none of these reach silver.
- A71 documentType is shared with `generation_forecast` (A71/A01); disambiguate by `processType`.
- Unit names are short codes (ABRBO, DRAXX, etc.; the `-1` suffixed names such as `ABRBO-1` belong to the generating units the parser drops) — see Elexon `bmunits_reference` to map to BM unit IDs.
- `MAW` in the `quantity_Measure_Unit.name` field is ENTSO-E shorthand for MW.

---

## Implementation delta

- Tuple verified 2026-05-08:
  - Docs (API guide §14.1.A unit-level annex): `(documentType=A71, processType=A33, businessType=n/a, in_Domain)`.
  - Code: `("A71", "A33", -, domain_style="in_domain")` → `in_Domain`.
  - **Match.**
- A71 collision with `generation_forecast` (A71/A01) — code disambiguates by `processType` and dataset key. No bug, just a footgun for direct API users.

---

## Modelling notes

- Asset registry — map BM unit IDs (Elexon) ↔ EIC mRIDs (ENTSO-E) via name match.
- Capacity-weighted aggregation for portfolio models.
- Closure / new-build tracking via year-on-year diffs.

---

## Links

- [Official API docs](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.pdf)
- `OneDrive/Desktop/Python/gridflow/src/gridflow/connectors/entsoe/client.py`
- `OneDrive/Desktop/Python/gridflow/src/gridflow/silver/entsoe/installed_capacity_units.py`
- `OneDrive/Desktop/Python/gridflow/src/gridflow/schemas/entsoe.py`
- Gold view/builder
