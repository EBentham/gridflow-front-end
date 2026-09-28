---
source: elexon
dataset_key: fuelinst
vendor: Elexon BMRS
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Five-minute generation by fuel type
  summary: >-
    Great Britain's generation outturn by Elexon fuel-type code in five-minute steps: one MW
    figure per code, keyed on Elexon's publish time.
  facts:
    vendor: Elexon BMRS, dataset FUELINST
    cadence: Every five minutes
    grain: One row per five-minute instant and fuel-type code, per daily file
  landscape: power
  what_it_is: >-
    Elexon's generation outturn by fuel type in five-minute steps: one MW figure per fuel-type
    code, from CCGT and nuclear to wind and each interconnector. Silver keys each value on
    Elexon's publish time, not the interval start, and keeps no settlement date or period. The
    interconnector codes and pumped storage (`PS`) are signed. There is no solar code.
  how_used:
    - "Fuel mix within the half-hour: wind, gas and interconnector ramps at five-minute steps."
    - The most recent fuel mix for intraday trading, one value every five minutes.
    - Within-period features for imbalance price models, from the mix inside each half-hour.
  chart:
    type: stacked-area
    silver: elexon/fuelinst
    time: timestamp_utc
    value: generation_mw
    filter:
      - {column: timestamp_utc, op: gt, value: "2026-09-19T23:00:00"}
      - {column: timestamp_utc, op: le, value: "2026-09-20T23:00:00"}
    dedup: {on: [timestamp_utc, fuel_type], order_by: ingested_at}
    group: fuel_type
    group_map:
      NUCLEAR: nuclear
      BIOMASS: biomass
      NPSHYD: npshyd
      COAL: coal_oil
      OIL: coal_oil
      OTHER: other
      CCGT: gas
      OCGT: gas
      WIND: wind
      INTELEC: imports
      INTEW: imports
      INTFR: imports
      INTGRNL: imports
      INTIFA2: imports
      INTIRL: imports
      INTNED: imports
      INTNEM: imports
      INTNSL: imports
      INTVKL: imports
      PS: ps
    series_order: [nuclear, biomass, npshyd, coal_oil, other, gas, wind, imports, ps]
    aggregation: sum
    window: {start: "2026-09-19", end: "2026-09-20"}
    unit: MW
  chart_view:
    title: Generation by fuel, five-minute steps, 20 September 2026
    caption: >-
      Silver `elexon/fuelinst`, MW, the 288 five-minute values published from 23:05 UTC on 19
      September to 23:00 UTC on 20 September 2026 (GB day 20 September's intervals), a group's codes summed,
      00:00 counted once. Negative values hang below zero.
    alt: >-
      Stacked area chart of GB generation by fuel from elexon/fuelinst, in MW, for the 288
      five-minute values of GB day 20 September 2026. From zero upward: nuclear (about 3.3 GW),
      biomass, non-pumped hydro, other, gas (2.3 to 9.2 GW, peaking at 18:30 UTC) and wind (16.2
      GW early on, falling to 5.4 GW at 19:05 UTC), then net imports and pumped storage when
      positive. Net interconnector flow runs from 6.3 GW of exports at 04:20 UTC to 6.0 GW of
      imports at 16:10 UTC, crossing zero at 14:05 UTC.
    x_label: publish time, UTC; first point 23:05, 19 September
    key:
      - {series: ps, label: Pumped storage, codes: PS, paint: hatch-cross, note: "Signed; Elexon does not say what the sign means. Drawn above or below zero as it falls."}
      - {series: imports, label: "Interconnectors, net", codes: "INT*, 10 codes", note: "Signed. Positive is import to GB, checked on FUELHH against demand; Elexon does not state it."}
      - {series: wind, label: Wind, codes: WIND, tag: wind}
      - {series: gas, label: Gas, codes: "CCGT, OCGT", tag: gas}
      - {series: other, label: Other, codes: OTHER, tag: other, note: "Elexon's own code; what it holds is undocumented."}
      - {series: coal_oil, label: Coal and oil, codes: "COAL, OIL", paint: hatch-dots, note: "0 MW at every instant here."}
      - {series: npshyd, label: "Hydro, not pumped", codes: NPSHYD, paint: hatch-lines}
      - {series: biomass, label: Biomass, codes: BIOMASS, tag: biomass}
      - {series: nuclear, label: Nuclear, codes: NUCLEAR, tag: nuclear}
  raw_feed:
    note: >-
      From the Elexon Insights API in 24-hour publish windows that include both ends, so each
      midnight instant lands in two daily files; silver does not trim it.
    requests:
      - "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELINST?publishDateTimeFrom=2026-09-19T00:00:00Z&publishDateTimeTo=2026-09-20T00:00:00Z&page=1"
      - "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELINST?publishDateTimeFrom=2026-09-20T00:00:00Z&publishDateTimeTo=2026-09-21T00:00:00Z&page=1"
    commands:
      - {run: gridflow ingest elexon fuelinst --start 2026-09-19 --end 2026-09-21, comment: "bronze; the end is exclusive"}
      - {run: gridflow transform elexon fuelinst --start 2026-09-19 --end 2026-09-20, comment: bronze to silver}
  record:
    select:
      filter:
        - {column: fuel_type, op: eq, value: PS}
        - {column: timestamp_utc, op: ge, value: "2026-09-19T23:40:00"}
        - {column: timestamp_utc, op: le, value: "2026-09-20T00:10:00"}
      order_by: [timestamp_utc, ingested_at]
    key: [timestamp_utc, fuel_type]
    caption: "`PS` every five minutes around midnight UTC, 20 September; 00:00 comes from two daily files."
    fields:
      timestamp_utc: "Elexon's publish time for the value, not the interval `startTime`"
      fuel_type: Elexon fuel-type code, as sent
      generation_mw: "MW; interconnector codes and `PS` are signed"
  notebook:
    lead: >-
      Returns a pandas DataFrame from DuckDB relation `silver_elexon_fuelinst`: `timestamp_utc`
      on the start to end dates (UTC, both included), returned in local time. Lineage columns go;
      midnight duplicates stay.
    cells:
      - |
        df = data.elexon.query("fuelinst", "2026-09-19", "2026-09-20")
        df = df.drop_duplicates(["timestamp_utc", "fuel_type"])
        df["timestamp_utc"] = df.timestamp_utc.dt.tz_convert("UTC")
      - df.sort_values(["timestamp_utc", "fuel_type"])[["timestamp_utc", "fuel_type", "generation_mw"]].head()
      - |
        ints = df[df.fuel_type.str.startswith("INT")]
        net = ints.groupby("timestamp_utc").generation_mw.sum()
        net.plot(ylabel="MW", color="#155A6E", figsize=(8, 3.5))
    needs: 19 and 20 September 2026
    plot_alt: >-
      Line plot of net interconnector flow, the INT codes summed, in MW against timestamp_utc for
      19 and 20 September 2026 at five-minute steps. It moves in steps: about -5,600 MW overnight
      on the 19th, up to 1,201 MW at 19:45, down to -6,343 MW at 04:20 on the 20th, then up to
      6,023 MW by 16:10 UTC.
  related:
    - {dataset: elexon/fuelhh, note: "The same codes per settlement period, with settlement date and period"}
    - {dataset: elexon/agpt, note: "Generation by type from another Elexon feed, with solar"}
    - {dataset: elexon/windfor, note: "Elexon's wind forecast, to set against the `WIND` code"}
---

# Elexon - Instantaneous Generation Outturn by Fuel Type (`FUELINST`)

## Overview

Instantaneous (5-minute) generation outturn by fuel type (FUELINST) — the same fuel split as FUELHH but published at 5-minute resolution. FUELINST is what drives near-real-time stack-and-fuel monitoring; the half-hour aggregates feed FUELHH.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://data.elexon.co.uk/bmrs/api/v1` |
| Path             | `/datasets/FUELINST` |
| Method           | GET |
| Auth             | None required for tested endpoints (2026-05-08). Some endpoints accept an `apikey` header (env: `ELEXON_API_KEY`); registration at https://www.elexonportal.co.uk/. |
| Rate limit       | Vendor-published: not stated. Project default 2 req/sec (asyncio.Semaphore); verified safe 2026-05-08. |
| Pagination       | Connector handles via `page=N` query param; stops when `page >= total_pages`. Reference endpoints (`/reference/bmunits/all`) are not paginated. |
| Historical depth | Several years. |
| Publication lag  | 5-minute publication cadence. |
| Response format  | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `publishDateTimeFrom` | string | No | As per Elexon Swagger spec for fuelinst. | `2026-05-06T00:00Z` |
| `publishDateTimeTo` | string | No | As per Elexon Swagger spec for fuelinst. | `2026-05-06T03:00Z` |
| `settlementDateFrom` | string | No | As per Elexon Swagger spec for fuelinst. | `2026-05-06` |
| `settlementDateTo` | string | No | As per Elexon Swagger spec for fuelinst. | `2026-05-07` |
| `settlementPeriod` | array | No | List of Settlement Periods | `24` |
| `fuelType` | array | No | Fuel Type e.g. NUCLEAR | `CCGT` |
| `format` | string | No | Response data format. Use json/xml to include metadata. | `json` |

### Working curl example

```bash
# Replace <ELEXON_API_KEY> with your env var if you choose to send one (Elexon endpoints
# tested 2026-05-08 do NOT require a key; set anyway for vendor courtesy).
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELINST?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-06T03:00Z&format=json" \
  -o "/tmp/elexon-fuelinst.json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/elexon/fuelinst/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per API call (paginated requests append additional files for the same date partition).

### Bronze sample

Captured live 2026-05-08 from the https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELINST?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-06T03:00Z&format=json:

```json
{
  "data": [
    {
      "dataset": "FUELINST",
      "publishTime": "2026-05-06T03:00:00Z",
      "startTime": "2026-05-06T02:55:00Z",
      "settlementDate": "2026-05-06",
      "settlementPeriod": 8,
      "fuelType": "BIOMASS",
      "generation": 2712
    },
    {
      "dataset": "FUELINST",
      "publishTime": "2026-05-06T03:00:00Z",
      "startTime": "2026-05-06T02:55:00Z",
      "settlementDate": "2026-05-06",
      "settlementPeriod": 8,
      "fuelType": "CCGT",
      "generation": 7527
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/elexon/fuelinst/year=YYYY/month=MM/fuelinst_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.elexon.fuelinst.FuelInstTransformer`
**Pydantic schema**: `gridflow.schemas.elexon.ElexonFuelInst` (`schemas/elexon.py:87-103`; `schema_cls` at `silver/elexon/fuelinst.py:28`).
**Dedup key**: `(timestamp_utc, fuel_type)`
**Point-in-time field**: none in silver. The publish time becomes `timestamp_utc`; no `published_at` column is written (`fuelinst.py:86-121`). The lineage `available_at` is `coalesce(published_at, ingest_time)` (`silver/base.py:2095-2100`), so for fuelinst it is always the ingest-side stamp, not the vendor publish time (the F-08-class note at `silver/elexon/_publication_window.py:39-42`).

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `timestamp_utc` | `datetime[UTC]` | No | `publishTime` (also `publishDateTime`) | The vendor publish time parsed as UTC; `startTime` is used only when no publish field is present (`fuelinst.py:61-100`). In the bronze sample above it is five minutes after `startTime`. |
| `fuel_type` | `str` | No | `fuelType` | Fuel category (CCGT, COAL, NUCLEAR, WIND, etc.). |
| `generation_mw` | `float` | No | `generation` | MW. |
| `data_provider` | `str` | No | _derived_ | Default `"elexon"`. |
| `ingested_at` | `datetime[UTC]` | Yes | _derived_ | When the silver transform ran: stamped `datetime.now(UTC)` by the transformer (`fuelinst.py:107-112`), not the bronze ingest time. |

### Silver sample

```python
[
    {
        "timestamp_utc": "2026-05-06T03:00:00+00:00",
        "fuel_type": "BIOMASS",
        "generation_mw": 2712,
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

- **5-minute resolution** — silver drops `settlement_date`/`settlement_period`. The instantaneous timestamp is `timestamp_utc` derived from the publish time (`publishTime`), not `startTime` (`fuelinst.py:86-100`).
- **The midnight instant is in two daily files.** With `--start`/`--end` dates, each daily request is the publish window D 00:00Z to D+1 00:00Z (24-hour chunks, `connectors/elexon/client.py:93-99`, `endpoints.py:40`), which Elexon treats as closed at both ends (`silver/partition_window.py:3-8`), and fuelinst is exempt from the publication-window trim (`silver/elexon/_publication_window.py:39-42`). The transformer dedups within one file only (`fuelinst.py:105`), so the D+1 00:00Z rows are written into both files and a plain read of the silver view returns them twice.

---

## Implementation delta

- **Pydantic schema**: `ElexonFuelInst` (`schemas/elexon.py:87-103`), declared as the transformer's `schema_cls` (`fuelinst.py:24-28`); its fields match the transformer's output columns.
- **`fuelinst` does not produce a settlement_date or settlement_period in silver output** — transformer drops those (output is `timestamp_utc`, `fuel_type`, `generation_mw`).

---

## Modelling notes

TODO

---

## Links

- [Official API docs (Swagger UI)](https://bmrs.elexon.co.uk/api-documentation)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/elexon/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/elexon/fuelinst.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/elexon.py)
- Gold view/builder
- [Domain: GB Balancing Mechanism](../../../20-domain/markets/gb-balancing-mechanism.md)
