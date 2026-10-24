---
source: entsoe
dataset_key: outages_generation
vendor: ENTSO-E Transparency Platform
last_verified: 2026-10-24
layer_coverage: bronze, silver
page:
  title: Unavailability (outages)
  summary: >-
    ENTSO-E outage notices for generation and production units, consumption, transmission and the
    offshore grid: each notice's stepped MW, window and status.
  facts:
    vendor: ENTSO-E Transparency Platform, unavailability documents, one type per member (A76 to A80)
    cadence: Notices carry revision numbers; gridflow requests each zone one UTC day at a time
    grain: One row per notice step, latest revision fetched for the day, cut at midnight
  landscape: power
  what_it_is: >-
    A notice (`document_mrid`) gives one unit, asset or zone aggregate's outage window and a
    stepped MW curve. ENTSO-E codes `A53` planned maintenance, `A54` forced unavailability and
    `A09` cancelled. gridflow requests only planned notices, except for the offshore grid. It keeps
    the highest revision fetched for each day and cuts steps at UTC midnight; `outage_start_utc` and
    `outage_end_utc` stay whole.
  how_used:
    - Units out at a delivery time, by production type, for a supply-stack model.
    - Interconnector and line outages beside cross-border capacity and flows.
    - Joining notices to the ENTSO-E unit register on `unit_mrid`.
  chart:
    type: bar
    silver: entsoe/outages_generation
    filter:
      - {column: timestamp_utc, op: le, value: "2026-09-15T12:00:00Z"}
      - {column: step_end_utc, op: gt, value: "2026-09-15T12:00:00Z"}
      - {column: document_status, op: ne, value: A09}
    group: production_type
    group_map:
      B10: hydro
      B11: hydro
      B12: hydro
      B04: gas
      B14: nuclear
      B05: hard_coal
      B03: hard_coal
      B02: lignite
      B06: misc
      B25: misc
      B01: biomass
    aggregation: count
    sort: value_desc
    unit: notices
  chart_view:
    title: Outage notices covering 12:00 UTC, 15 September 2026, as fetched
    caption: >-
      Silver `entsoe/outages_generation` (GB, FR, NL, BE, DE-LU, IE-SEM): gridflow's count of
      planned notices whose latest fetched revision covers 12:00 UTC, 15 September 2026, cancelled
      (`A09`) left out, so revisions made after noon decide. Notices, not MW.
    alt: >-
      Horizontal bar chart from entsoe/outages_generation counting planned outage notices for
      generation units in GB, FR, NL, BE, DE-LU and IE-SEM whose latest revision as fetched covers
      12:00 UTC on 15 September 2026, cancelled notices left out. Hydro leads with 70 (pumped storage, run-of-river and reservoir),
      then gas 53, nuclear 37, hard coal and coal gas 29, lignite 14, oil and storage 10 and
      biomass 5: 218 in all.
    key:
      - {series: hydro, label: Hydro, codes: "B10, B11, B12", paint: hatch-lines, note: "Pumped storage (B10), run-of-river (B11) and reservoir (B12) counted together."}
      - {series: gas, label: Gas, codes: B04}
      - {series: nuclear, label: Nuclear, codes: B14}
      - {series: hard_coal, label: "Hard coal, coal gas", codes: "B05, B03", paint: hatch-cross}
      - {series: lignite, label: Lignite, codes: B02, paint: hatch-dots}
      - {series: misc, label: "Oil, storage", codes: "B06, B25", paint: hatch-vertical, note: "B06 oil and B25 energy storage counted together."}
      - {series: biomass, label: Biomass, codes: B01}
  raw_feed:
    note: >-
      One GET per zone, or zone pair for transmission, per UTC day. A reply is a ZIP of notice XML
      files, or an acknowledgement with reason 999 when nothing matches.
    requests:
      - "GET https://web-api.tp.entsoe.eu/api?documentType=A80&periodStart=202609150000&periodEnd=202609160000&BiddingZone_Domain=10Y1001A1001A82H&BusinessType=A53&securityToken=$ENTSOE_API_KEY"
    commands:
      - {run: gridflow ingest entsoe outages_generation --start 2026-09-15 --end 2026-09-21, comment: "bronze; the end is exclusive"}
      - {run: gridflow transform entsoe outages_generation --start 2026-09-15 --end 2026-09-20, comment: "bronze to silver; end included"}
  record:
    select:
      filter:
        - {column: document_mrid, op: eq, value: x-GtbpThrnCQ-ys1m-U_EQ}
      order_by: [timestamp_utc]
      columns: [timestamp_utc, step_end_utc, unavailable_mw, nominal_mw, generation_unit_name, outage_start_utc, outage_end_utc, revision_number, document_status, published_at]
    key: [document_mrid, timeseries_mrid, generation_unit_mrid, timestamp_utc]
    caption: "KW Boxberg Block Q's whole notice, 19 to 20 September; midnight splits its 0 MW step."
    fields:
      document_mrid: "The notice's `mRID`, shared by every revision of it"
      timeseries_mrid: "Series `mRID` within the notice, as sent"
      generation_unit_mrid: "EIC of the generation unit inside the production unit, as sent"
      timestamp_utc: "Step start, UTC; the day's 00:00 when the step began the day before"
      step_end_utc: "Step end, UTC: the next point or the period end, cut at midnight"
      generation_unit_name: "Generation unit name, as sent (`powerSystemResources.name`)"
      unavailable_mw: "The step's `quantity` in MW (`MAW`); gridflow's name, its meaning unverified"
      nominal_mw: "The generation unit's `nominalP` in MW, as sent"
      outage_start_utc: "The notice's period start, UTC, not cut to the day"
      outage_end_utc: "The notice's period end, UTC, not cut to the day; may be years ahead"
      revision_number: "`revisionNumber`; a day keeps the highest revision fetched for it"
      document_status: "`docStatus`: `A09` cancelled; empty where ENTSO-E sends no status"
      published_at: "The revision's `createdDateTime`, UTC; here, after the outage began"
      area_code: "Bidding zone EIC, from `biddingZone_Domain.mRID`"
      unit_mrid: "Production unit EIC (`production_RegisteredResource.mRID`)"
      unit_name: "Production unit name, as sent"
      production_type: "ENTSO-E production type code as sent, for example `B05` hard coal"
      outage_type: "gridflow's mapping: `planned` for `A53`, `unplanned` for `A54`"
      business_type: "`businessType` as sent; gridflow requests only `A53`, planned maintenance"
      resolution: "Point spacing as sent: `PT1M`"
  notebook:
    lead: >-
      Returns a pandas DataFrame from `silver_entsoe_outages_generation`, filtered on
      `timestamp_utc` with both ends included; lineage columns dropped, rows ordered by
      `timestamp_utc` only. The cells count non-cancelled notices covering 12:00 UTC each day, as fetched.
    cells:
      - |
        df = data.entsoe.query("outages_generation", "2026-09-15", "2026-09-20")
        for col in ["timestamp_utc", "step_end_utc"]:
            df[col] = df[col].dt.tz_convert("UTC")
        active = df[df["document_status"] != "A09"].sort_values(["timestamp_utc", "generation_unit_name"])
      - active[["timestamp_utc", "step_end_utc", "generation_unit_name", "unavailable_mw", "nominal_mw", "revision_number"]].head()
      - |
        import pandas as pd
        noons = pd.date_range("2026-09-15 12:00", "2026-09-20 12:00", freq="D", tz="UTC")
        in_force = pd.Series([((active.timestamp_utc <= t) & (active.step_end_utc > t)).sum() for t in noons], index=noons.date)
        in_force.plot(ylabel="notices covering 12:00 UTC", ylim=(0, 250), color="#155A6E", figsize=(8, 3.5))
    needs: generation-unit outages for 15 to 20 September 2026
    plot_alt: >-
      Line plot, y axis from 0 to 250, of non-cancelled planned generation-unit notices covering
      12:00 UTC each day, 15 to 20 September 2026, each at its revision as fetched: 218 on the 15th,
      a high of 226 on the 16th, then 220, 211 and 203, down to 201 on the 20th.
  related:
    - {dataset: entsoe/generation_units_master_data, note: "Unit register that `unit_mrid` joins to, for type and area"}
    - {dataset: entsoe/actual_generation, note: "Generation by production type, with the same `B` codes as charted"}
    - {dataset: entsoe/net_transfer_capacity, note: "Transfer capacity on borders such as GB-FR, also named in transmission notices"}
    - {dataset: elexon/remit, note: "GB unit outages from Elexon, with available and unavailable MW"}
  family:
    slug: outages
    members:
      - dataset: outages_generation
        differs: "Generation units within production units (A80), each with its nominal MW"
        request: "GET https://web-api.tp.entsoe.eu/api?documentType=A80&periodStart=202609150000&periodEnd=202609160000&BiddingZone_Domain=10Y1001A1001A82H&BusinessType=A53&securityToken=$ENTSOE_API_KEY"
        caveat: "ENTSO-E sends this MW as `quantity` in an `Available_Period`, not labelled available or unavailable."
      - dataset: outages_production
        differs: "Production units (A77): `unit_mrid` and nominal MW, no generation unit"
        request: "GET https://web-api.tp.entsoe.eu/api?documentType=A77&periodStart=202609090000&periodEnd=202609100000&BiddingZone_Domain=10Y1001A1001A82H&BusinessType=A53&securityToken=$ENTSOE_API_KEY"
        caveat: "ENTSO-E sends this MW as `quantity` in an `Available_Period`, not labelled available or unavailable."
      - dataset: outages_consumption
        differs: "Consumption units (A76): one aggregate MW per zone, no unit named"
        request: "GET https://web-api.tp.entsoe.eu/api?documentType=A76&periodStart=202609150000&periodEnd=202609160000&BiddingZone_Domain=10Y1001A1001A82H&BusinessType=A53&securityToken=$ENTSOE_API_KEY"
        caveat: "ENTSO-E sends this MW as `quantity` in an `Available_Period`, not labelled available or unavailable."
      - dataset: outages_transmission
        differs: "Transmission assets (A78) between a zone pair, keyed on `asset_mrid`"
        request: "GET https://web-api.tp.entsoe.eu/api?documentType=A78&periodStart=202609080000&periodEnd=202609090000&In_Domain=10YFR-RTE\x2D\x2D\x2D\x2D\x2D\x2DC&Out_Domain=10YBE\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D2&BusinessType=A53&securityToken=$ENTSOE_API_KEY"
        caveat: "ENTSO-E sends this MW as `quantity` in an `Available_Period`, not labelled available or unavailable."
      - dataset: outages_offshore_grid
        differs: "Offshore grid assets (A79); no business type sent, so unplanned notices too"
        request: "GET https://web-api.tp.entsoe.eu/api?documentType=A79&periodStart=202609220000&periodEnd=202609230000&BiddingZone_Domain=10YNL\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DL&securityToken=$ENTSOE_API_KEY"
        caveat: "ENTSO-E sends this MW as `quantity` in a `WindPowerFeedin_Period`, not labelled available or unavailable."
---

# ENTSO-E — Unavailability of generation units (A80)

## Overview

Outage notifications for generation units — one document per outage, each
declaring the affected unit (`registeredResource`), the period of
unavailability (`Available_Period`), a stepped MW curve (`<quantity>`, in `MAW`;
whether it is available or unavailable MW is unverified, see Known issues),
and the planning status (`businessType`; ENTSO-E's API documentation: "A53 = Planned
maintenance; A54 = Forced unavailability (unplanned outage)").
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
| Pagination       | Multi-document replies are a **ZIP archive**. ENTSO-E's API documentation (Postman collection "Transparency Platform Restful API", https://documenter.getpostman.com/view/7009892/2s93JtP3F6, request "15.1.A&B Unavailability of Generation Units", read 2026-10-24): each request may cover up to 1 year; "A maximum of 200 XML documents contained in the ZIP response", with an `offset` parameter for further batches of 200. gridflow sends no `offset` (see Known issues). |
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
| `BusinessType` | str | no (ENTSO-E's API documentation marks it `[O]`, optional) | `A53` (planned maintenance) or `A54` (forced unavailability) | `A53` |
| `BiddingZone_Domain` | EIC | yes | Bidding zone | `10YGB----------A` |
| `periodStart` | str | yes | UTC `yyyymmddhhmm`, **30-day window recommended** | `202604010000` |
| `periodEnd` | str | yes | UTC `yyyymmddhhmm` | `202605010000` |
| `DocStatus` | str | no | Outage status filter; ENTSO-E's API documentation (https://documenter.getpostman.com/view/7009892/2s93JtP3F6, request "15.1.A&B Unavailability of Generation Units", read 2026-10-24): "DocStatus (when not defined only Active and Cancelled outages are returned): A05 = Active; A09 = Cancelled; A13 = Withdrawn" | `A05` |
| `offset` | int | no | Skip the first N documents of the ZIP (batches of 200, per the API documentation) | `200` |
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
  <!-- docStatus is sent only on cancelled notices: <docStatus><value>A09</value></docStatus> -->
  <TimeSeries>
    <mRID>1</mRID>
    <businessType>A53</businessType>
    <biddingZone_Domain.mRID>10YGB----------A</biddingZone_Domain.mRID>
    <production_RegisteredResource.mRID>48W000000DRAXX-1Y</production_RegisteredResource.mRID>
    <production_RegisteredResource.name>DRAXX-1</production_RegisteredResource.name>
    <production_RegisteredResource.pSRType.psrType>B02</production_RegisteredResource.pSRType.psrType>
    <production_RegisteredResource.pSRType.powerSystemResources.mRID>...</production_RegisteredResource.pSRType.powerSystemResources.mRID>
    <production_RegisteredResource.pSRType.powerSystemResources.name>...</production_RegisteredResource.pSRType.powerSystemResources.name>
    <production_RegisteredResource.pSRType.powerSystemResources.nominalP unit="MAW">...</production_RegisteredResource.pSRType.powerSystemResources.nominalP>
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
**Dedup key**: `(document_mrid, timeseries_mrid, generation_unit_mrid, timestamp_utc)` (`identity` plus the step start, `outages_generation.py:46-50`, `_outages.py:199-219`; gridflow `fix/entsoe-pt1m-steps`, `DATASET_VERSION` 2.0.0)
**Row shape** (`_outages.py:1-18, 87-156`): the parser emits each declared `<Point>` of the `A03` curve as one step with an explicit end (`parsers.py` `_as_steps`, `a03_as_steps=True`): the next declared point, or the period end. Within one bronze day the transformer keeps only each document's highest `revisionNumber` (whole document, not point by point), then clips every step to that UTC day, so `query()` over several days returns each outage-minute once. A step that runs past midnight becomes one row per day it touches. The document's own period survives unclipped as `outage_start_utc` / `outage_end_utc`.
**Point-in-time (as-of) field**: `available_at` (the bitemporal as-of column written by `BaseSilverTransformer`, reconstructable from bronze sidecars on reingest). `ingested_at` is the transform wall-clock (`datetime.now(UTC)`), **not** a publication vintage, so do not use it as a leak-proof as-of anchor. `published_at` is the revision's `createdDateTime` (`outages_generation.py:86-87`, `_published_at.py`), and it feeds `available_at`. It is the notice revision's creation time, not the fetch time (silver built from bronze fetched in September 2026 holds creation times from 30 September 2025), and it can fall after the outage window itself (HKW Tiefstack Block 2: period 7 to 9 September 2026 07:00, created 9 September 10:06). Older revisions are dropped, so silver cannot show what an earlier revision said.

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| timestamp_utc | datetime[UTC] | No | `Available_Period` start + (position - 1) × resolution | Step start, tz-aware UTC; `PT1M` is mapped to one minute. Clipped to the partition day: 00:00 when the step began the day before. |
| step_end_utc | datetime[UTC] | No | next declared point's start, else the period end | Step end, clipped to the next midnight. |
| area_code | str | No | `<biddingZone_Domain.mRID>` | EIC |
| unit_mrid | str | No | `<production_RegisteredResource.mRID>` | Production-unit EIC; joins `generation_units_master_data.unit_mrid`. |
| unit_name | str | No | `<production_RegisteredResource.name>` | Default "" in canonical. |
| generation_unit_mrid | str | No | `<production_RegisteredResource.pSRType.powerSystemResources.mRID>` | Generation-unit EIC inside the production unit. |
| generation_unit_name | str | No | `<...powerSystemResources.name>` | |
| production_type | str | No | `<production_RegisteredResource.pSRType.psrType>` | ENTSO-E PSR code (B01..B25). |
| nominal_mw | float | Yes | `<...powerSystemResources.nominalP unit="MAW">` | The generation unit's nominal power, MW. |
| outage_type | str | No | derived from `<businessType>` | "planned" (A53) / "unplanned" (A54) |
| unavailable_mw | float | No | `<Point><quantity>` of `Available_Period` (`quantity_Measure_Unit.name` `MAW`) | Named "unavailable" by gridflow; whether the quantity is available or unavailable MW is unverified (see Known issues). |
| business_type | str | No | `<businessType>` | Raw code, `A53` only (see Known issues). |
| document_mrid | str | No | root `<mRID>` | Shared by every revision of a notice. |
| revision_number | int | Yes | root `<revisionNumber>` | Highest revision in that day's bronze. |
| document_status | str | No | root `<docStatus><value>` | `A09` on cancelled notices; "" when no `docStatus` is sent (every non-cancelled document received). |
| timeseries_mrid | str | No | TimeSeries `<mRID>` | "1" in every document received. |
| outage_start_utc | datetime[UTC] | Yes | min Period `timeInterval/start` of the series | Not clipped. |
| outage_end_utc | datetime[UTC] | Yes | max Period `timeInterval/end` of the series | Not clipped. |
| resolution | str | No | parsed | ISO code as sent. `PT1M` in every document received September 2026. |
| published_at | datetime[UTC] | Yes | root `<createdDateTime>` | Revision creation time; typed null when absent. |
| data_provider | str | No | constant | "entsoe" |
| ingested_at | datetime[UTC] | Yes | derived | optional |

Not kept: the TimeSeries `<Reason><code>` (for example `B19`) and `<text>`, and the root `unavailability_Time_Period`.

### Silver sample

```python
[
    {
        "timestamp_utc": "2026-09-08T22:00:00+00:00",
        "step_end_utc": "2026-09-09T00:00:00+00:00",
        "area_code": "10Y1001A1001A82H",
        "unit_mrid": "11WD8TIEF5X----V",
        "unit_name": "HKW Tiefstack",
        "generation_unit_mrid": "11WD8TIEF5C----9",
        "generation_unit_name": "HKW Tiefstack Block 2",
        "production_type": "B05",
        "nominal_mw": 189.0,
        "outage_type": "planned",
        "unavailable_mw": 41.0,
        "business_type": "A53",
        "document_mrid": "9YcVzweZsiJAoxxxPZbNVg",
        "revision_number": 1,
        "document_status": "",
        "timeseries_mrid": "1",
        "outage_start_utc": "2026-09-07T18:30:00+00:00",
        "outage_end_utc": "2026-09-09T07:00:00+00:00",
        "resolution": "PT1M",
        "published_at": "2026-09-09T10:06:59+00:00",
        "data_provider": "entsoe",
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **30-day window minimum.** A 1-day query window often returns Acknowledgement reason 999 even when outages exist. Use 30-day windows for backfill; daily incremental queries can use a rolling 30-day window with dedup. (Unsourced; ENTSO-E's API documentation allows up to 1 year per request. gridflow sends 1-day windows per zone, `client.py:162-163`, for GB, FR, NL, BE, DE-LU and IE-SEM, `endpoints.py:395`, and they returned up to 180 documents per DE-LU day in September 2026.)
- **More than 200 documents: rejected or cut short is unknown, and gridflow sends no `offset`.** ENTSO-E's API documentation (request "15.1.A&B Unavailability of Generation Units") says `offset` "paginates the response in batches of 200 XML documents" and gives "A maximum of 200 XML documents contained in the ZIP response"; it does not say what a request matching more than 200 returns without `offset`. The one observation on file is a rejection: a DE-LU 30-day A77 request on 2026-05-08 got HTTP 400 reason 999 "The number of instances (3209) exceeds the allowed maximum (200)" ([outages production](outages_production.md), Live verification). No A80 request has been seen past 200. gridflow's outage requests carry no `offset` (the paging on `fix/entsoe-balancing-paging` covers balancing bids and procured capacity only). A 400 makes `_raise_for_status` raise and fails the whole ingest run (`client.py:170-179, 428-441`); a 200-document ZIP would lose the rest silently. No reply for 8 to 20 September 2026 reached 200 (largest 180, DE-LU, 17 September).
- **ZIP archives** — the API returns a ZIP for any window with ≥1 outage. Bytes start with `PK\x03\x04`. Connector detects this in `client._is_zip_response()` and `_iter_zip_xml()` extracts inner XMLs into separate `RawResponse`s.
- **Outage status codes** (DocStatus): `A05` Active, `A09` Cancelled, `A13` Withdrawn (ENTSO-E's API documentation). gridflow sends no `DocStatus` (`endpoints.py:54-60`), so replies include cancelled notices; silver keeps them with `document_status` `A09` (299 of 909 documents in silver for 8 to 20 September 2026, fetched on 15 and 21 September). Non-cancelled documents send no `docStatus` element at all, so their `document_status` is empty; `A05` and `A13` were never seen. Filter `document_status != "A09"` for outages still planned.
- **Revision number: highest per day, not overall.** A notice (`mRID`) is republished with a higher `revisionNumber`; ENTSO-E's API documentation lists the `mRID` parameter as "Used to retrieve older versions of an outage", and gridflow sends none. The transformer keeps each document's highest revision within one bronze day (`_outages.py:112-128`), before clipping. Different days can therefore hold different revisions of one notice: 40 of 909 documents carry more than one revision across the 13 days, and 5 are active on earlier days and cancelled on later ones (for example Niederaußem, revision 9 on 8 to 13 September, revision 12 `A09` from 14 September). The split follows the fetch: days 8 to 13 were fetched on 15 September, days 15 to 20 on 21 September, and 14 September on both dates (its highest revision comes from the later fetch). A window query returns each day's own revision, as fetched for that day.
- **`unavailable_mw` meaning is unverified** (gridflow backlog 13am). gridflow renames the `<quantity>` of `Available_Period` to `unavailable_mw` (`_outages.py:172`); the transformer docstring says the reading is unverified, and no vendor text for it is on file (the project spec asserted it; ENTSO-E's API documentation does not describe the quantity). In silver for 8 to 20 September 2026 the quantity never exceeds `nominal_mw` and is 0 in 3,805 of 5,501 step rows, and multi-point profiles step like availability (KW Boxberg Block R, `nominalP` 630: 477, 415, 370, 305, 220 then back up). That reads as **available** MW. Confirm against the ENTSO-E data description before using it either way.
- **Daily files and clipping.** Outages are exempt from the event-window trim (`silver/entsoe/_event_window.py`), and the transformer clips each step to its partition day instead (`_outages.py:131-156`), so a long outage contributes one slice per day fetched and nothing repeats across days. Silver holds only the days requested: an outage running past the last requested day is cut there, though `outage_end_utc` keeps its real end.
- **Far-future ends, as sent.** Some notices give a period end years ahead: in silver for 8 to 20 September 2026, 777 of 5,501 rows (61 documents, 42 not cancelled) end after 2027, the latest 2099-12-31 23:00 UTC, and 104 rows end 2050-12-31 23:00. Treat such ends as open-ended before computing durations.
- **Planned only.** `BusinessType=A53` is fixed in `extra_params` (`endpoints.py:59`) and `gridflow ingest` has no option to pass another (`cli.py:185-216`), so `outage_type` is always `planned` and forced unavailability (`A54`) is never requested.
- **Reason not kept.** Each TimeSeries carries a `<Reason>` code (and, for some senders, free text); silver keeps neither.

---

## Implementation delta

- Tuple verified 2026-05-08:
  - Docs (API guide §15.1.A): `(documentType=A80, processType=n/a, BusinessType=A53|A54, BiddingZone_Domain)`.
  - Code: `("A80", None, BusinessType="A53", domain_style="bidding_zone")` → `BiddingZone_Domain`.
  - **Match.** (Code fixes A53. A54 is not reachable: `BusinessType` is not a forwarded optional param, `client.py:567-576`, and the CLI passes none.)
- DocStatus values (A05/A09/A13) are **not** validated server-side beyond the codelist; passing other strings returns reason 999.

---

## Modelling notes

- Capacity-tightness models — `installed_capacity - sum(unavailable_mw)` per zone, only once the meaning of `unavailable_mw` is settled (if it is available MW, use `nominal_mw - unavailable_mw`). Drop `A09` rows first.
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
