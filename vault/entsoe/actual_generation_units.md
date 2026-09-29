---
source: entsoe
dataset_key: actual_generation_units
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Actual generation per unit
  summary: >-
    ENTSO-E's realised output of individual generating units in MW, from document type A73, for
    Belgium, France and the Netherlands.
  facts:
    vendor: ENTSO-E Transparency Platform, document type A73, process type A16
    cadence: "As sent in these responses: 15-minute FR; hourly BE and most NL plants"
    grain: One row per time step and plant EIC, not per generation unit
  landscape: power
  what_it_is: >-
    ENTSO-E's realised output per generation unit, in MW. gridflow requests six zones; GB, DE-LU
    and IE-SEM come back as no-data acknowledgements. Each series names a plant and, nested inside
    it, the unit. Silver keeps only the plant EIC as `unit_mrid`, so a plant with several units
    keeps one unit's figure, and FR's consumption series land in `generation_mw` unmarked.
  how_used:
    - Hourly dispatch of the charted Dutch plants, nuclear baseload against coal and gas.
    - Load factors for the charted plants, against `installed_capacity_units` on the same EIC.
  chart:
    type: line
    silver: entsoe/actual_generation_units
    time: timestamp_utc
    value: generation_mw
    filter:
      - {column: unit_mrid, op: in, value: ["49W000000000054X", "49W000000000102B", "49W000000000069K"]}
    group: unit_mrid
    group_map:
      "49W000000000054X": nuclear
      "49W000000000102B": coal
      "49W000000000069K": gas
    series_order: [nuclear, coal, gas]
    aggregation: mean
    window: {start: "2026-09-14", end: "2026-09-20"}
    unit: MW
  chart_view:
    title: Three Dutch plants, 14 to 20 September 2026
    caption: >-
      Silver `entsoe/actual_generation_units`, MW, hourly as sent, 14 to 20 September 2026 UTC,
      three NL plants that send one generation unit each and no consumption series, so each row
      is that unit's output; one line per plant, nothing summed.
    alt: >-
      Line chart of hourly MW from entsoe/actual_generation_units, three Dutch plants, 14 to 20
      September 2026 UTC. Borssele (nuclear) is flat near 470 MW. Maasvlakte (coal) runs near
      1,040 MW with midday dips to 300 MW (15th, 17th) and 200 MW (18th), then holds about 200 MW
      from late on the 18th until the 20th's afternoon, bar 896 MW on the 19th. Claus (gas) swings
      between 133 and 1,152 MW until the 16th, stays below 395 MW on the 17th to 19th, and reaches
      830 MW on the 20th.
    x_label: date, UTC; hourly as sent
    key:
      - {series: gas, label: Claus (gas), codes: 49W000000000069K, note: "Unit Claus C, B04. Plant names from `generation_units_master_data`; `unit_name` here is empty."}
      - {series: coal, label: Maasvlakte (coal), codes: 49W000000000102B, paint: olive, note: "Unit Maasvlakte 3, B05 hard coal."}
      - {series: nuclear, label: Borssele (nuclear), codes: 49W000000000054X, note: "Unit Borssele 30, B14."}
  raw_feed:
    note: >-
      From the ENTSO-E web API, one request per bidding zone and UTC day, for six zones.
      `gridflow ingest` writes each XML response to bronze; `gridflow transform` parses it into silver.
    requests:
      - "GET https://web-api.tp.entsoe.eu/api?documentType=A73&periodStart=202609180000&periodEnd=202609190000&in_Domain=10YNL\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DL&processType=A16&securityToken=$ENTSOE_API_KEY"
    commands:
      - {run: gridflow ingest entsoe actual_generation_units --start 2026-09-14 --end 2026-09-21, comment: "bronze; the end is exclusive"}
      - {run: gridflow transform entsoe actual_generation_units --start 2026-09-14 --end 2026-09-20, comment: bronze to silver}
  record:
    select:
      filter:
        - {column: timestamp_utc, op: eq, value: "2026-09-18T18:00:00Z"}
        - {column: unit_mrid, op: in, value: ["49W000000000054X", "49W000000000102B", "49W000000000078J", "49W000000000069K", "49W000000000074R", "49W0000000000512", "49W000000000094L", "49W000000000048S"]}
      order_by: [production_type, unit_mrid]
      columns: [unit_mrid, generation_mw, area_code, resolution, timestamp_utc, production_type, published_at, unit_name]
    key: [timestamp_utc, area_code, unit_mrid]
    caption: "Eight Dutch plants that send one generation unit each, 18:00 UTC on 18 September 2026."
    fields:
      timestamp_utc: "Step start: period start plus (position minus 1) times `resolution`, UTC"
      area_code: "Bidding zone EIC, from `inBiddingZone_Domain` or `outBiddingZone_Domain`; silver cannot tell which"
      unit_mrid: "Plant EIC (`registeredResource.mRID`); the nested generation units' EICs and names are dropped"
      production_type: "ENTSO-E production type (PSR) code: B04 gas, B05 hard coal, B14 nuclear"
      generation_mw: "MW (`MAW`): the plant's one series here; elsewhere may be another unit's or consumption"
      resolution: "Step as sent (`PT60M` here, `PT15M` in FR); each point holds until the next"
      published_at: "Response `createdDateTime`: a fetch-time stamp, within seconds of gridflow's request"
      unit_name: "Empty here: the parser skips the nested unit names ENTSO-E sends"
  notebook:
    lead: >-
      Returns a pandas DataFrame from the DuckDB relation `silver_entsoe_actual_generation_units`,
      filtered on `timestamp_utc` as whole UTC days with both ends included. Lineage columns are
      dropped. Rows within a day come unordered, so sort first.
    cells:
      - |
        df = data.entsoe.query("actual_generation_units", "2026-09-14", "2026-09-20")
        df["timestamp_utc"] = df["timestamp_utc"].dt.tz_convert("UTC")
        df = df.sort_values(["timestamp_utc", "area_code", "unit_mrid"])
      - df[["timestamp_utc", "area_code", "unit_mrid", "production_type", "generation_mw"]].head()
      - |
        plants = {"49W000000000054X": "Borssele", "49W000000000102B": "Maasvlakte", "49W000000000069K": "Claus"}
        nl = df[df["unit_mrid"].isin(list(plants))].pivot(index="timestamp_utc", columns="unit_mrid", values="generation_mw").rename(columns=plants)
        nl[["Borssele", "Maasvlakte", "Claus"]].plot(ylabel="MW", color=["#155A6E", "#66793B", "#C77E3C"], figsize=(8, 3.5))
    needs: 14 to 20 September 2026
    plot_alt: >-
      Line plot of generation_mw against timestamp_utc for three Dutch plants, 14 to 20 September
      2026 UTC: Borssele flat near 470 MW; Maasvlakte near 1,040 MW with deep dips from the 15th,
      and near 200 MW from late on the 18th until the 20th's afternoon; Claus swinging between about 130 and 1,150 MW, flat
      near 130 MW on the 19th.
  related:
    - {dataset: entsoe/installed_capacity_units, note: "Capacity keyed on the same plant EIC, for load factors"}
    - {dataset: entsoe/generation_units_master_data, note: "Names the plant EICs, which this table leaves empty"}
    - {dataset: entsoe/actual_generation, note: "The same zones' output summed per production type (A75)"}
    - {dataset: elexon/pn, note: "GB output plans per BM unit; GB returns nothing here"}
---

# ENTSO-E — Actual generation per generation unit (A73/A16)

## Overview

Realised MW output **per individual generation unit** rather than per
production type. Identifies units by their EIC mRID and human-readable
name. The unit-level granularity is what makes A73 special — it's the
TSO-published equivalent of Elexon's `pn` (Physical Notifications) at
the level of the EIC unit registry. Used to calibrate plant-by-plant
must-run / capacity-factor models.

→ [Actual generation](actual_generation.md), [Installed capacity per unit](installed_capacity_units.md)

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
| Historical depth | 2014-12-05 onwards |
| Publication lag  | T+~1h |
| Response format  | XML — root `GL_MarketDocument` |
| Document type    | A73 |
| Process type     | A16 (realised) |
| Business type    | n/a |
| Domain param name| `in_Domain` |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `documentType` | str | yes | `A73` | `A73` |
| `processType` | str | yes | `A16` | `A16` |
| `in_Domain` | EIC | yes | Bidding zone | `10YGB----------A` |
| `periodStart` | str | yes | UTC `yyyymmddhhmm` | `202605060000` |
| `periodEnd` | str | yes | UTC `yyyymmddhhmm` | `202605070000` |
| `psrType` | str | no | Filter to one production type | `B16` |

### Working curl example

```bash
curl --ssl-no-revoke -fsS \
  "https://web-api.tp.entsoe.eu/api?securityToken=$ENTSOE_API_KEY&documentType=A73&processType=A16&in_Domain=10YGB----------A&periodStart=202605060000&periodEnd=202605070000" \
  -H "Accept: application/xml"
```

Live verification 2026-05-08:
- GB 1-day window: HTTP 200, **EMPTY** (Ack 999 "ACTUAL_GENERATION_OUTPUT_PER_UNIT_R3 [16.1.A]"). Brexit-GB.
- DE-LU 1-day window: HTTP 200, **EMPTY** (Ack 999 same code) — DE-LU does not publish A73/A16 to ENTSO-E either; many continental TSOs publish only A75 aggregated.
- Bronze 2026-08-01..05 and 2026-09-08..21 (fetched 2026-08-16, 2026-09-15 and 2026-09-26, six zones per request day): FR, BE and NL return `GL_MarketDocument` with data; GB, DE-LU and IE-SEM return Ack 999 (checked 2026-09-29).

A73/A16 is generally only available in zones where the TSO chooses to
publish per-unit realised flows; expect EMPTY across most European zones.

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsoe/actual_generation_units/<year>/<month>/<day>/raw_<uuid>.xml`
**Format**: Raw XML, immutable.
**Granularity**: One file per (zone, day).

### Bronze sample (DE-LU, EMPTY response)

```xml
<Acknowledgement_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-1:acknowledgementdocument:7:0">
  <Reason><code>999</code><text>No matching data found ...</text></Reason>
</Acknowledgement_MarketDocument>
```

When data is published, response root is `GL_MarketDocument` with one
`<TimeSeries>` per generation unit and side. `registeredResource.mRID` is the plant
(production unit) EIC, the code A95 `generation_units_master_data` lists with the plant
name; the generation unit's own EIC and name sit in `MktPSRType/PowerSystemResources`
(bronze 2026-09-15: plant `17W100P100P02756` carries GRAND MAISON 1 to 12, each its own
series). Every series has `businessType` A01 and `curveType` A03. FR also sends
`outBiddingZone_Domain.mRID` series; BE and NL send none. For A75 ENTSO-E documents
that tag as the consumption side (see [Actual generation](actual_generation.md)); no A73
vendor text was found, but the values fit it (B10 up to 237 MW, pumping scale; B14 up to
94 MW). No generation unit has both sides at the same instant in bronze 2026-08/09.

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsoe/actual_generation_units/year=YYYY/month=MM/actual_generation_units_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsoe.actual_generation_units.ActualGenerationUnitsTransformer`
**Pydantic schema**: `gridflow.schemas.entsoe.EntsoeActualGenerationUnits`
**Dedup key**: `(timestamp_utc, area_code, unit_mrid)`, keep last (`actual_generation_units.py:69-72`). `unit_mrid` is the plant EIC, so the key has neither the generation unit nor the side (see Known issues)
**Point-in-time field**: none in effect. `published_at` is the response `createdDateTime` (`actual_generation_units.py:82-83`), a fetch-time stamp within seconds of gridflow's request (across the 60 data files in bronze 2026-08/09, 11.7 s before to 0.2 s after bronze `fetched_at`; 2026-09-18 FR: 18:24:24Z against 18:24:24.48Z), not a publication time

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| timestamp_utc | datetime[UTC] | No | Period start + (position - 1) * resolution (`connectors/entsoe/parsers.py:530`) | tz-aware UTC. `curveType` A03: a point repeats until the next declared one (`parsers.py:533-601`) |
| area_code | str | No | `<inBiddingZone_Domain.mRID>` or `<outBiddingZone_Domain.mRID>` | EIC. The parser reads both tags into one field (`parsers.py:289-297`); silver cannot tell which |
| production_type | str | No | `<MktPSRType><psrType>` | EIC PSR type |
| unit_mrid | str | No | `<registeredResource.mRID>` | The plant (production unit) EIC, not the generation unit: the nested `MktPSRType/PowerSystemResources/mRID` is not read (`parsers.py:345-348`; the plant EIC is read at `351-352`). Keep verbatim, no normalisation |
| unit_name | str | No | `<registeredResource.name>` | Default "" in canonical (str = ""). Not present in the A73 responses in bronze 2026-08/09, so always ""; the unit names sit in `PowerSystemResources/name`, which the parser does not read (`parsers.py:345-348`, `353-354`) |
| generation_mw | float | No | `<Point><quantity>` | MW (`MAW`). The last series read for the plant key, which may be another generation unit's or a consumption figure (see Known issues) |
| resolution | str | No | `<Period><resolution>` | Default "" in canonical (str = ""). As sent in bronze 2026-08/09: PT15M for FR and one NL plant, PT60M for BE and the other NL plants |
| published_at | datetime[UTC] | Yes | document `<createdDateTime>` | `silver/entsoe/_published_at.py`; a fetch-time stamp, not a publication time |
| data_provider | str | No | constant | "entsoe" |
| ingested_at | datetime[UTC] | Yes | derived | When the silver transform ran (`actual_generation_units.py:74-79`) |

### Silver sample

A real row (NL, Borssele, silver 2026-09-18), replacing a GB example: GB returns no data.

```python
[
    {
        "timestamp_utc": "2026-09-18T18:00:00+00:00",
        "area_code": "10YNL----------L",
        "production_type": "B14",
        "unit_mrid": "49W000000000054X",
        "unit_name": "",
        "generation_mw": 470.65525,
        "resolution": "PT60M",
        "published_at": "2026-09-26T18:24:24+00:00",
        "data_provider": "entsoe",
        "ingested_at": "2026-09-26T18:25:34.852545+00:00",
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **GB EMPTY** — GB stopped publishing per-unit data to ENTSO-E post-Brexit.
- **DE-LU EMPTY** — German TSOs publish unit-level data only via SMARD / national portals, not ENTSO-E.
- **`businessType` requirement (per plan):** plan flags A73/A16 as needing a `psrType` filter for "production-unit-level data". In practice the API accepts the call with no `psrType`; the EMPTY result is data availability, not a filter requirement. `psrType` is documented as **optional** in the API guide. Code does not include `psrType` in `optional_params` — flag as `unverified` for the connector caller.
- Unit mRIDs vary by TSO encoding (IGCC, EIC, internal). Treat as opaque strings.
- Re-publication: silver `keep="last"` overwrites earlier revisions.
- **One row per plant, not per generation unit, and no side (gridflow defect, measured 2026-09-29).** `unit_mrid` is `registeredResource.mRID`, the plant EIC; the generation unit's EIC and name (`MktPSRType/PowerSystemResources`) are never read (`connectors/entsoe/parsers.py:345-348`), and `outBiddingZone_Domain.mRID` lands in the same `in_domain` field as generation (`parsers.py:289-297`). The dedup key `(timestamp_utc, area_code, unit_mrid)` (`silver/entsoe/actual_generation_units.py:69-72`) therefore keeps one series per plant and instant, the last read, and nothing records which. 30 plants send several generation units (BE 8, FR 17, NL 5; FR Grand Maison 12); 79 of FR's 110 plants also send consumption series. Re-parsing all 19 bronze days with the gridflow parser and the transformer's dedup reproduces silver exactly (229,612 rows, 0 value mismatches). Of those rows: 137,358 hold the plant's only series (clean); 56,214 (FR) hold a consumption figure with no generation series at that instant; 15,102 hold one of several generation units' differing figures; 6,340 (FR) hold one unit's consumption figure while the plant's other series differ; 3,194 (FR) hold a generation figure while other units' series, some of them consumption, differ; 11,404 had several series all equal (11,387 all zero). 80,112 distinct series points are dropped. Example, 2026-09-18 18:00Z: Grand Maison `17W100P100P02756` silver 129.77 MW (GRAND MAISON 9), while six of its twelve units generated 772.0 MW in total; Cheylas `17W100P100P0273A` silver 0.11 MW (CHEYLAS 1 consumption) while CHEYLAS 2 generated 228.64 MW. Plants with one generation unit and no consumption series (all NL single-unit plants, for example) are clean. Fix needs the generation unit EIC and the side in the key, as for `actual_generation` (BACKLOG 13a).
- `unit_name` is "" on every row: A73 responses carry no `registeredResource.name`; the names ENTSO-E sends are in `PowerSystemResources/name` (see above). A95 `generation_units_master_data` names the plant EICs.

---

## Implementation delta

- Tuple verified 2026-05-08:
  - Docs (API guide §16.1.A): `(documentType=A73, processType=A16, businessType=n/a, in_Domain)`.
  - Code: `("A73", "A16", -, domain_style="in_domain")` → `in_Domain`.
  - **Match.**
- Plan-flagged: `psrType` not in `optional_params`. Documented as optional, not required — code is correct in not enforcing it. Flag as `unverified` for consumer ergonomics.

---

## Modelling notes

- Plant-level capacity-factor models — when data is available.
- Deviation from declared `pn` (Elexon) for outage-detection style features.
- For GB use Elexon `pn` / `boal` instead.

---

## Links

- [Official API docs](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.pdf)
- `OneDrive/Desktop/Python/gridflow/src/gridflow/connectors/entsoe/client.py`
- `OneDrive/Desktop/Python/gridflow/src/gridflow/silver/entsoe/actual_generation_units.py`
- `OneDrive/Desktop/Python/gridflow/src/gridflow/schemas/entsoe.py`
- Gold view/builder
