---
source: entsoe
dataset_key: outages_generation
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
---

# ENTSO-E — Unavailability of generation units (A80)

## Overview

Outage notifications for generation units — one document per outage, each
declaring the affected unit (`registeredResource`), the period of
unavailability (`Available_Period`), the unavailable MW (`<quantity>`),
and the planning status (`businessType` A53=planned / A54=unplanned).
Critical input for short-term tightness models, supply-stack adjustments,
and outage-driven price spike features.

→ [Outages production](outages_production.md), [Generation units master data](generation_units_master_data.md)

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | https://web-api.tp.entsoe.eu |
| Path             | /api |
| Method           | GET |
| Auth             | query param `securityToken=$ENTSOE_API_KEY` |
| Rate limit       | 1 req/s |
| Pagination       | None at the API; large windows return a **ZIP archive** of multiple XML files |
| Historical depth | ~2014 onwards |
| Publication lag  | T+~1h after TSO publication |
| Response format  | XML — root `Unavailability_MarketDocument`. Multi-document responses come as a ZIP of XML files. Code unzips transparently. |
| Document type    | A80 |
| Process type     | n/a |
| Business type    | A53 (planned) — also accepts A54 (unplanned) |
| Domain param name| `BiddingZone_Domain` |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `documentType` | str | yes | `A80` | `A80` |
| `BusinessType` | str | yes | `A53` (planned) or `A54` (unplanned) | `A53` |
| `BiddingZone_Domain` | EIC | yes | Bidding zone | `10YGB----------A` |
| `periodStart` | str | yes | UTC `yyyymmddhhmm`, **30-day window recommended** | `202604010000` |
| `periodEnd` | str | yes | UTC `yyyymmddhhmm` | `202605010000` |
| `DocStatus` | str | no | Outage status filter (A05 active, A09 cancelled, A13 withdrawn) | `A05` |
| `mRID` | str | no | Lookup specific outage notification | |
| `RegisteredResource` | EIC | no | Filter to one unit | |

### Working curl example

```bash
curl --ssl-no-revoke -fsS \
  "https://web-api.tp.entsoe.eu/api?securityToken=$ENTSOE_API_KEY&documentType=A80&BusinessType=A53&BiddingZone_Domain=10YGB----------A&periodStart=202604010000&periodEnd=202605010000" \
  -H "Accept: application/xml" \
  --output outages.zip
```

Live verification 2026-05-08:
- GB 30-day window: HTTP 200, **PASS** — ZIP archive (40 KB) of 17 individual `UNAVAILABILITY_OF_PRODUCTION_AND_GENERATION_UNITS_*.xml` documents covering generation outages active in the period. Connector unzips transparently and writes one bronze file per archive entry.

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsoe/outages_generation/<year>/<month>/<day>/raw_<uuid>.xml`
**Format**: Raw XML — one bronze file per inner ZIP entry.
**Granularity**: One bronze XML file per outage notification (multiple inner XMLs per API call). gridflow sends one request per zone per UTC day (`client.py:162-163`) and files it under that day (`client.py:312`); ENTSO-E returns every outage overlapping the day, so a multi-day outage is filed again under every day it overlaps.

### Bronze sample (single outage doc, schematic)

```xml
<Unavailability_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:outagedocument:3:0">
  <mRID>...</mRID>
  <type>A80</type>
  <revisionNumber>2</revisionNumber>
  <docStatus><value>A05</value></docStatus>
  <TimeSeries>
    <mRID>1</mRID>
    <businessType>A53</businessType>
    <biddingZone_Domain.mRID>10YGB----------A</biddingZone_Domain.mRID>
    <production_RegisteredResource.mRID>48W000000DRAXX-1Y</production_RegisteredResource.mRID>
    <production_RegisteredResource.name>DRAXX-1</production_RegisteredResource.name>
    <production_RegisteredResource.pSRType.psrType>B02</production_RegisteredResource.pSRType.psrType>
    <Available_Period>
      <timeInterval><start>...</start><end>...</end></timeInterval>
      <resolution>PT1M</resolution>
      <Point><position>1</position><quantity>0</quantity></Point>
    </Available_Period>
  </TimeSeries>
</Unavailability_MarketDocument>
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsoe/outages_generation/year=YYYY/month=MM/outages_generation_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsoe.outages_generation.OutagesGenerationTransformer`
**Pydantic schema**: `gridflow.schemas.entsoe.EntsoeOutagesGeneration`
**Dedup key**: `(timestamp_utc, unit_mrid)`
**Point-in-time (as-of) field**: `available_at` (the bitemporal as-of column written by `BaseSilverTransformer`, reconstructable from bronze sidecars on reingest). `ingested_at` is the transform wall-clock (`datetime.now(UTC)`), **not** a publication vintage, so do not use it as a leak-proof as-of anchor. `published_at` is the document `createdDateTime` (`outages_generation.py:100`, `_published_at.py`), and it feeds `available_at`. For these documents it is the notice's creation time, not the fetch time: bronze fetched in September 2026 carries creation dates from October 2025 onwards.

> **A80 silver is intentionally unit-level.** Unlike the H7 outage family
> (consumption/transmission/offshore-grid/production), this transformer
> deliberately omits `production_type`/`psrType`, `business_type`,
> `document_mrid`, `document_status`, and `timeseries_mrid` from silver — even
> though the bronze document carries them (e.g. `pSRType.psrType=B02` above). The
> leaner per-unit schema is by design (the unit-level shape is asserted by
> `test_existing_generation_outage_transformer_stays_unit_level`). Join
> `unit_mrid` against [generation units master data](generation_units_master_data.md)
> to recover `production_type` for capacity normalisation.

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| timestamp_utc | datetime[UTC] | No | `Available_Period` start + (position - 1) × resolution (`parsers.py:530`) | tz-aware UTC. One row per declared `<Point>`, not per outage; the period end is not kept. `PT1M` is missing from `_RESOLUTION_MAP`, so it steps by 1 hour (`parsers.py:35-51`): see Known issues. |
| area_code | str | No | `<biddingZone_Domain.mRID>` | EIC |
| unit_mrid | str | No | `<production_RegisteredResource.mRID>` (or `RegisteredResource/mRID`) | Production-unit EIC. The generation unit (`pSRType.powerSystemResources.mRID`) is not kept. |
| unit_name | str | No | `<production_RegisteredResource.name>` | Default "" in canonical. |
| outage_type | str | No | derived from `<businessType>` | "planned" (A53) / "unplanned" (A54) |
| unavailable_mw | float | No | `<Point><quantity>` of `Available_Period` | Named "unavailable" by gridflow; whether the quantity is available or unavailable MW is unverified (see Known issues). |
| resolution | str | No | parsed | ISO code as sent (`parsers.py:438`). `PT1M` in every document received September 2026. |
| published_at | datetime[UTC] | Yes | root `<createdDateTime>` | Notice creation time; typed null when absent. |
| data_provider | str | No | constant | "entsoe" |
| ingested_at | datetime[UTC] | Yes | derived | optional |

### Silver sample

```python
[
    {
        "timestamp_utc": "2026-04-15T14:00:00+00:00",
        "area_code": "10YGB----------A",
        "unit_mrid": "48W000000DRAXX-1Y",
        "unit_name": "DRAXX-1",
        "outage_type": "planned",
        "unavailable_mw": 645.0,
        "resolution": "PT1M",
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

- **30-day window minimum.** A 1-day query window often returns Acknowledgement reason 999 even when outages exist. Use 30-day windows for backfill; daily incremental queries can use a rolling 30-day window with dedup. (gridflow does not do this: it sends 1-day windows per zone, `client.py:162-163`, for GB, FR, NL, BE, DE-LU and IE-SEM, `endpoints.py:395`.)
- **ZIP archives** — the API returns a ZIP for any window with ≥1 outage. Bytes start with `PK\x03\x04`. Connector detects this in `client._is_zip_response()` and `_iter_zip_xml()` extracts inner XMLs into separate `RawResponse`s.
- **Outage status codes** (DocStatus): `A05` Active, `A09` Cancelled, `A13` Withdrawn. gridflow sends no `DocStatus` (`endpoints.py:54-60`) and the responses include cancelled (`A09`) documents: 299 of 951 document versions in bronze fetched 8 to 20 September 2026. This transformer drops `document_status`, so silver cannot tell a cancelled outage from an active one. NOTE: gridflow silver dedup is `df.unique(keep="last")` over the dedup key and is NOT revision-aware — `revisionNumber` is parsed but not used to order survivors, so the surviving row follows bronze parse order, not the highest revision.
- **Revision number** — same outage `mRID` may be republished with `revisionNumber > 1`. gridflow does NOT currently sort by `revisionNumber`; dedup keeps the last row in parse order (known limitation).
- **Pagination by record count** — windows with >200 outages return HTTP 400 reason 999 "exceeds the allowed maximum (200)". Splits into smaller windows are required for high-outage zones.
- **`unavailable_mw` meaning is unverified.** gridflow renames the `<quantity>` of `Available_Period` to `unavailable_mw`; no vendor text for that reading is on file (the project spec asserted it). In bronze fetched 8 to 20 September 2026 the quantity never exceeds the unit's `nominalP` and is 0 in 551 of 951 document versions, and multi-point profiles step like availability (Schwarze Pumpe B, `nominalP` 755: 613, 463, 389 ...). That reads as **available** MW. Confirm against the ENTSO-E data description before using it either way.
- **Repeated across daily files.** Outages are exempt from the event-window trim (`silver/entsoe/_event_window.py:181-183`) and dedup runs within one day's file only, so each daily file repeats every outage fetched that day: 236 of 951 document versions appear in all 13 files 8 to 20 September 2026. `query()` reads on `timestamp_utc` (`silver/schema_manifest.py:181`) with no latest view, so it returns the repeats.
- **`PT1M` timestamps.** `PT1M` is not in `_RESOLUTION_MAP` (`parsers.py:35-43`), so `_resolve_resolution` falls back to 1 hour (`parsers.py:50-51`) and the `A03` forward-fill is skipped (`parsers.py:547-555`). Position 1 is right; every later point is stamped hours instead of minutes after the start. One Emsland B position (381181) lands in June 2069 for a period ending December 2026; 173 of 951 versions carry a point stamped after their own period end.
- **Dedup collapses documents and generation units.** The key `(timestamp_utc, unit_mrid)` uses the production unit, so sibling generation units with the same start (for example `ABTH7`, `ABTH8`, `ABTH9` under `ABTHB`) and different documents collide; `keep="last"` keeps one in parse order. On 2026-09-15 it dropped 337 of 1,142 parsed rows (285 groups, all spanning more than one document; 41 mixing cancelled and active).
- **Planned only.** `BusinessType=A53` is fixed in `extra_params` (`endpoints.py:59`) and `gridflow ingest` has no option to pass another (`cli.py:185-216`), so `outage_type` is always `planned`.

---

## Implementation delta

- Tuple verified 2026-05-08:
  - Docs (API guide §15.1.A): `(documentType=A80, processType=n/a, BusinessType=A53|A54, BiddingZone_Domain)`.
  - Code: `("A80", None, BusinessType="A53", domain_style="bidding_zone")` → `BiddingZone_Domain`.
  - **Match.** (Code fixes A53. A54 is not reachable: `BusinessType` is not a forwarded optional param, `client.py:567-576`, and the CLI passes none.)
- DocStatus values (A05/A09/A13) are **not** validated server-side beyond the codelist; passing other strings returns reason 999.

---

## Modelling notes

- Capacity-tightness models — `installed_capacity - sum(unavailable_mw)` per zone.
- Outage-driven price spike features — high `unavailable_mw` ↔ price tail risk.
- Distinguish planned (A53) vs unplanned (A54) — unplanned has higher price elasticity.
- Use unit_mrid to join with master data for production_type and capacity normalisation.

---

## Links

- [Official API docs](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.pdf)
- `OneDrive/Desktop/Python/gridflow/src/gridflow/connectors/entsoe/client.py`
- `OneDrive/Desktop/Python/gridflow/src/gridflow/silver/entsoe/outages_generation.py`
- `OneDrive/Desktop/Python/gridflow/src/gridflow/schemas/entsoe.py`
- Gold view/builder
