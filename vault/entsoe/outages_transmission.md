---
source: entsoe
dataset_key: outages_transmission
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
---

# ENTSO-E — Unavailability of transmission infrastructure (A78)

## Overview

Outage notifications for transmission assets — interconnectors,
cross-border lines, internal critical lines. Domain pair `(In_Domain,
Out_Domain)` identifies the affected interconnection. Used to flag NTC
reductions, predict cross-border price decoupling events, and as input
to interconnector flow-direction models.

→ [Net transfer capacity](net_transfer_capacity.md), [Cross-border flows](cross_border_flows.md)

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | https://web-api.tp.entsoe.eu |
| Path             | /api |
| Method           | GET |
| Auth             | query param `securityToken=$ENTSOE_API_KEY` |
| Rate limit       | 1 req/s |
| Pagination       | None at the API; large windows return ZIP archives |
| Historical depth | ~2014 onwards |
| Publication lag  | T+~1h |
| Response format  | XML — root `Unavailability_MarketDocument`. ZIP archive for multi-document responses. |
| Document type    | A78 |
| Process type     | n/a |
| Business type    | A53 (planned) — also A54 (unplanned) |
| Domain param name| `In_Domain` + `Out_Domain` (zone pair, capital-I) |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `documentType` | str | yes | `A78` | `A78` |
| `BusinessType` | str | yes | `A53` or `A54` | `A53` |
| `In_Domain` | EIC | yes | Receiving zone | `10YGB----------A` |
| `Out_Domain` | EIC | yes | Sending zone | `10YFR-RTE------C` |
| `periodStart` | str | yes | UTC `yyyymmddhhmm`, 30-day window | `202604010000` |
| `periodEnd` | str | yes | UTC `yyyymmddhhmm` | `202605010000` |
| `DocStatus` | str | no | A05/A09/A13 status filter | |
| `mRID` | str | no | Specific notification | |
| `PeriodStartUpdate` | str | no | Update-time filter | |
| `PeriodEndUpdate` | str | no | Update-time filter | |

### Working curl example

```bash
curl --ssl-no-revoke -fsS \
  "https://web-api.tp.entsoe.eu/api?securityToken=$ENTSOE_API_KEY&documentType=A78&BusinessType=A53&In_Domain=10YGB----------A&Out_Domain=10YFR-RTE------C&periodStart=202604010000&periodEnd=202605010000" \
  -H "Accept: application/xml" \
  --output outages_tx.zip
```

Live verification 2026-05-08:
- GB↔FR 30-day window: HTTP 200, **PASS** — ZIP archive (7.6 KB) of 7 individual `UNAVAILABILITY_IN_TRANSMISSION_GRID_*.xml` files. Each XML is one transmission outage notification.

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsoe/outages_transmission/<year>/<month>/<day>/raw_<uuid>.xml`
**Format**: Raw XML — one bronze file per inner ZIP entry.
**Granularity**: One bronze XML file per outage notification. gridflow sends one request per zone pair per UTC day (`client.py:162-163`, `:211-226`) and files it under that day (`client.py:312`), so a multi-day outage is filed again under every day it overlaps.

### Bronze sample (single outage doc, schematic)

```xml
<Unavailability_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:outagedocument:3:0">
  <type>A78</type>
  <docStatus><value>A05</value></docStatus>
  <TimeSeries>
    <businessType>A53</businessType>
    <in_Domain.mRID>10YGB----------A</in_Domain.mRID>
    <out_Domain.mRID>10YFR-RTE------C</out_Domain.mRID>
    <Asset_RegisteredResource>
      <mRID>...</mRID><name>IFA1</name>
    </Asset_RegisteredResource>
    <Available_Period>
      <timeInterval>...</timeInterval>
      <resolution>PT1M</resolution>
      <Point><position>1</position><quantity>1000</quantity></Point>
    </Available_Period>
  </TimeSeries>
</Unavailability_MarketDocument>
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsoe/outages_transmission/year=YYYY/month=MM/outages_transmission_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsoe.outages_h7.OutagesTransmissionTransformer`
**Pydantic schema**: `gridflow.schemas.entsoe.EntsoeOutagesTransmission`
**Dedup key**: `(timestamp_utc, in_area_code, out_area_code, asset_mrid, timeseries_mrid)`
**Point-in-time (as-of) field**: `available_at` (the bitemporal as-of column written by `BaseSilverTransformer`, reconstructable from bronze sidecars on reingest). `ingested_at` is the transform wall-clock (`datetime.now(UTC)`), **not** a publication vintage, so do not use it as a leak-proof as-of anchor. `published_at` is the document `createdDateTime` (`outages_h7.py:107`), the notice's creation time (dates from November 2025 onwards in bronze fetched in 2026), and it feeds `available_at`.

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| timestamp_utc | datetime[UTC] | No | `Available_Period` start + (position - 1) × resolution (`parsers.py:530`) | tz-aware UTC. One row per declared `<Point>`; the period end is not kept. `PT1M` steps by 1 hour (see Known issues). |
| in_area_code | str | No | `<in_Domain.mRID>` (the response's casing; the request parameter is `In_Domain`) | EIC |
| out_area_code | str | No | `<out_Domain.mRID>` | EIC |
| asset_mrid | str | No | `<Asset_RegisteredResource><mRID>` | Default "" in canonical. Transmission asset EIC. |
| asset_name | str | No | `<Asset_RegisteredResource><name>` | Default "" in canonical. Asset name (e.g. IFA1). |
| outage_type | str | No | derived from `<businessType>` | "planned" / "unplanned" |
| unavailable_mw | float | No | `<Point><quantity>` of `Available_Period` | MW. Available or unavailable is unverified (see [outages generation](outages_generation.md)). |
| business_type | str | No | `<businessType>` | Default "" in canonical. Raw. |
| document_mrid | str | No | root `<mRID>` | Default "" in canonical. |
| document_status | str | No | `<docStatus><value>` | Default "" in canonical. A05/A09/A13. |
| timeseries_mrid | str | No | TimeSeries `<mRID>` | Default "" in canonical. |
| resolution | str | No | parsed | Default "" in canonical. ISO code as sent (`parsers.py:438`); `PT1M` in every document received 2026. |
| published_at | datetime[UTC] | Yes | root `<createdDateTime>` | Notice creation time; typed null when absent. |
| data_provider | str | No | constant | "entsoe" |
| ingested_at | datetime[UTC] | Yes | derived | optional |

### Silver sample

```python
[
    {
        "timestamp_utc": "2026-04-08T05:30:00+00:00",
        "in_area_code": "10YGB----------A",
        "out_area_code": "10YFR-RTE------C",
        "asset_mrid": "ABC123",
        "asset_name": "IFA1",
        "outage_type": "planned",
        "unavailable_mw": 1000.0,
        "business_type": "A53",
        "document_mrid": "DOC-001",
        "document_status": "A05",
        "timeseries_mrid": "1",
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

- **`In_Domain` / `Out_Domain` use capital-I prefix** for A78 (and A80 transmission), distinct from the lowercase `in_Domain` / `out_Domain` for prices and flows. Wrong casing → 400 / Acknowledgement.
- **Zone-pair iteration** — in code, `domain_style="zone_pair"` plus `domain_params=("In_Domain", "Out_Domain")` overrides the casing. Each interconnector pair is a separate API call; `_FLOW_PAIRS` in `client.py` iterates over GB-FR, GB-NL, GB-BE, GB-IE, plus internal European pairs.
- **30-day window** as for other outages.
- **ZIP archives** for multi-document responses.
- **Outage status codes** (DocStatus): `A05` Active, `A09` Cancelled, `A13` Withdrawn. gridflow sends no `DocStatus` (`endpoints.py:70-77`); responses include cancelled documents (9 of 78 document versions in bronze fetched in August and September 2026), kept as `document_status` `A09`.
- **Shared with A80** (details in [outages generation](outages_generation.md)): outages repeat in every daily file they overlap (exempt from the event-window trim, `_event_window.py:187-189`; 78 document versions fetched 281 times over 12 days); `PT1M` points after position 1 are stamped in hours (`parsers.py:35-51`; 6 of 78 versions carry a point past their own period end, up to 2052); no revision column in silver; `BusinessType=A53` only.
- Asset names (e.g. "IFA1") differ across TSOs and may not match BMRS interconnector IDs verbatim.

---

## Implementation delta

- Tuple verified 2026-05-08:
  - Docs (API guide §10.1.A): `(documentType=A78, processType=n/a, BusinessType=A53|A54, In_Domain+Out_Domain)` — capital-I.
  - Code: `("A78", None, BusinessType="A53", domain_style="zone_pair", domain_params=("In_Domain", "Out_Domain"))`.
  - **Match.**
- The shared `domain_style="zone_pair"` for both lowercase- and capital-domain endpoints is disambiguated only by `domain_params`. Ensure new transmission datasets reuse the explicit `domain_params=("In_Domain", "Out_Domain")` tuple.

---

## Modelling notes

- Interconnector availability — `installed_capacity - sum(unavailable_mw)` gives effective NTC.
- Cross-border price decoupling — outage events ↔ price spread changes.
- Combine with `cross_border_flows` for utilisation analysis under reduced capacity.

---

## Links

- [Official API docs](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.pdf)
- `OneDrive/Desktop/Python/gridflow/src/gridflow/connectors/entsoe/client.py`
- `OneDrive/Desktop/Python/gridflow/src/gridflow/silver/entsoe/outages_h7.py`
- `OneDrive/Desktop/Python/gridflow/src/gridflow/schemas/entsoe.py`
- Gold view/builder
