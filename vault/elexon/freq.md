---
source: elexon
dataset_key: freq
vendor: Elexon BMRS
last_verified: 2026-05-09
layer_coverage: bronze, silver
page:
  title: System frequency
  summary: >-
    Great Britain's system frequency in hertz, one measured value per timestamp, from Elexon's
    FREQ dataset.
  facts:
    vendor: Elexon BMRS, dataset FREQ
    cadence: Samples 15 seconds apart, as in the rows below
    grain: One row per measurement time; a midnight can sit in two day files
  landscape: power
  what_it_is: >-
    Measured GB system frequency, in Hz. gridflow asks for one 24-hour `measurementDateTime`
    window per call and keeps `measurementTime` and `frequency`. In responses gridflow has
    fetched, Elexon includes the sample at the window's end, so a day's file can end on the next
    midnight. The schema bounds values to 49.0 to 51.0 Hz; a breach is counted,
    not dropped.
  how_used:
    - Deviation from 50 Hz as a feature in balancing-cost models.
    - Finding excursions past a threshold, timed to the sample.
    - Measuring how quickly frequency recovers after a dip, sample by sample.
  chart:
    type: line
    silver: elexon/freq
    time: timestamp_utc
    value: frequency_hz
    filter:
      - {column: timestamp_utc, op: ge, value: "2026-09-17T00:00:00Z"}
      - {column: timestamp_utc, op: lt, value: "2026-09-17T06:00:00Z"}
    dedup: {"on": [timestamp_utc], order_by: ingested_at}
    aggregation: last
    window: {start: "2026-09-17", end: "2026-09-17"}
    unit: Hz
  chart_view:
    title: System frequency, 17 September 2026, 00:00 to 06:00 UTC
    caption: >-
      Silver `elexon/freq`, Hz, every 15-second sample from 00:00 to 06:00 UTC on 17 September
      2026, unaggregated.
    alt: >-
      Line chart of system frequency from elexon/freq, in Hz, for every 15-second sample from
      00:00 to 06:00 UTC on 17 September 2026, on an axis spanning a few tenths of a hertz
      either side of 50. The line wanders
      either side of 50 Hz in every hour, peaking at 50.208 Hz at 01:00:15 UTC. Its lowest point
      is a dip to 49.755 Hz at 03:13:15 UTC, back above 49.9 Hz by 03:17:30.
    x_label: 00:00 to 06:00 UTC, 17 September 2026
    key:
      - {series: frequency_hz, label: Frequency, codes: FREQ, paint: petrol, note: "Lowest 49.755 Hz at 03:13:15 UTC; highest 50.208 Hz at 01:00:15 UTC."}
  raw_feed:
    note: >-
      From the Elexon Insights API, one 24-hour `measurementDateTime` window per call. `gridflow
      ingest` writes each response to bronze; `gridflow transform` types each day's bronze into
      silver.
    requests:
      - "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/FREQ?measurementDateTimeFrom=2026-09-17T00:00:00Z&measurementDateTimeTo=2026-09-18T00:00:00Z&page=1"
    commands:
      - {run: gridflow ingest elexon freq --start 2026-09-16 --end 2026-09-18, comment: "bronze; two 24-hour windows"}
      - {run: gridflow transform elexon freq --start 2026-09-16 --end 2026-09-17, comment: bronze to silver}
  record:
    select:
      filter:
        - {column: timestamp_utc, op: ge, value: "2026-09-17T03:12:30Z"}
        - {column: timestamp_utc, op: le, value: "2026-09-17T03:14:15Z"}
      order_by: [timestamp_utc]
    key: [timestamp_utc]
    caption: "Eight consecutive samples on 17 September 2026, through the chart's lowest value."
    fields:
      timestamp_utc: Measurement time, UTC, parsed from `measurementTime` as sent
      frequency_hz: "System frequency, Hz, from `frequency`; schema bounds 49.0 to 51.0"
  notebook:
    lead: >-
      Returns a pandas DataFrame from the DuckDB view `silver_elexon_freq`: whole UTC days on
      `timestamp_utc`, ordered by it, lineage columns dropped. Times print in local time. A
      midnight in two day files comes back twice.
    cells:
      - df = data.elexon.query("freq", "2026-09-17", "2026-09-17")
      - df[["timestamp_utc", "frequency_hz"]].head()
      - |
        df.plot(x="timestamp_utc", y="frequency_hz", ylabel="Hz",
                color="#155A6E", figsize=(8, 3.5))
    needs: 16 and 17 September 2026
    plot_alt: >-
      Line plot of frequency_hz against timestamp_utc for 17 September 2026, with the time axis
      in UTC+1 clock time (01:00 to 01:00). Frequency wanders between 49.755 and 50.219 Hz,
      crossing 50 Hz many times, with its lowest point just after 04:00 on that clock.
  related:
    - {dataset: elexon/fuelinst, note: "Generation by fuel every five minutes, over the same hours"}
    - {dataset: elexon/boal, note: "Balancing Mechanism acceptances issued around the same instants"}
    - {dataset: elexon/system_prices, note: "Imbalance prices for the half-hours these samples fall in"}
    - {dataset: elexon/indo, note: "Demand outturn for the same half-hours"}
---

# Elexon - System Frequency (`FREQ`)

## Overview

System frequency measurements — instantaneous samples of the GB transmission system frequency, nominally 50 Hz with a statutory operating range of 49.5–50.5 Hz. The dataset is a high-frequency (sub-minute) telemetry stream used in operational frequency-response models, as a regressor for ancillary services costs, and to validate frequency-keeping performance under the Frequency Response services.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://data.elexon.co.uk/bmrs/api/v1` |
| Path             | `/datasets/FREQ` |
| Method           | GET |
| Auth             | None required for tested endpoints (2026-05-08). Some endpoints accept an `apikey` header (env: `ELEXON_API_KEY`); registration at https://www.elexonportal.co.uk/. |
| Rate limit       | Vendor-published: not stated. Project default 2 req/sec (asyncio.Semaphore); verified safe 2026-05-08. |
| Pagination       | Connector handles via `page=N` query param; stops when `page >= total_pages`. Reference endpoints (`/reference/bmunits/all`) are not paginated. |
| Historical depth | Several years. |
| Publication lag  | Continuous stream; samples are 15 seconds apart as returned (bronze response for 2026-09-20: 5,761 samples from 00:00:00 to the next 00:00:00). Elexon's own statement of the interval not verified. |
| Response format  | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `measurementDateTimeFrom` | string | No | As per Elexon Swagger spec for freq. | `2026-05-06T00:00Z` |
| `measurementDateTimeTo` | string | No | As per Elexon Swagger spec for freq. | `2026-05-06T03:00Z` |
| `format` | string | No | Response data format. Use json/xml to include metadata. | `json` |

### Working curl example

```bash
# Replace <ELEXON_API_KEY> with your env var if you choose to send one (Elexon endpoints
# tested 2026-05-08 do NOT require a key; set anyway for vendor courtesy).
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://data.elexon.co.uk/bmrs/api/v1/datasets/FREQ?measurementDateTimeFrom=2026-05-06T00:00Z&measurementDateTimeTo=2026-05-06T03:00Z&format=json" \
  -o "/tmp/elexon-freq.json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/elexon/freq/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per API call (paginated requests append additional files for the same date partition).

### Bronze sample

Captured live 2026-05-08 from the https://data.elexon.co.uk/bmrs/api/v1/datasets/FREQ?measurementDateTimeFrom=2026-05-06T00:00Z&measurementDateTimeTo=2026-05-06T03:00Z&format=json (re-verified with corrected param names 2026-05-09):

```json
{
  "data": [
    {
      "dataset": "FREQ",
      "measurementTime": "2026-05-08T00:00:00Z",
      "frequency": 49.97
    },
    {
      "dataset": "FREQ",
      "measurementTime": "2026-05-07T23:59:45Z",
      "frequency": 50.017
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/elexon/freq/year=YYYY/month=MM/freq_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.elexon.freq.FreqTransformer`
**Pydantic schema**: `gridflow.schemas.elexon.ElexonFrequency`
**Dedup key**: `(timestamp_utc)`
**Point-in-time field**: `ingested_at` (no native PIT field)

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `timestamp_utc` | `datetime[UTC]` | No | `reportDateTime` or `measurementTime` | Parsed from the vendor's `measurementTime` (or `reportDateTime`) as sent, UTC (`silver/elexon/freq.py:57-78`). |
| `frequency_hz` | `float` | No | `frequency` | Hz; ge=49.0 le=51.0 (validation is fail-soft: a breaching row is counted and still written, `silver/base.py:2022-2029`). |
| `data_provider` | `str` | No | _derived_ | Default `"elexon"`. |
| `ingested_at` | `datetime[UTC]` | Yes | _derived_ | Stamped when the silver transform runs (`silver/elexon/freq.py:85-89`), not the bronze ingest time. |

### Silver sample

```python
[
    {
        "timestamp_utc": "2026-05-08T00:00:00Z",
        "frequency_hz": 49.97,
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

- **Midnight in two day files**: the response includes the sample at `measurementDateTimeTo` (bronze 2026-09-20 starts at 2026-09-21T00:00:00Z), and dedup on `timestamp_utc` runs per transform date (`silver/elexon/freq.py:83`), so each midnight sample sits in two adjacent `freq_YYYYMMDD.parquet` files. The DuckDB view is a plain `read_parquet` glob (`storage/duckdb.py:444-447`), so a query spanning both returns it twice.
- **High-frequency stream**: ~5760 samples per 24-hour window (15-second spacing; bronze response for 2026-09-20 holds 5,761 samples for a 24-hour From/To). Bronze files can grow large — partition by hour or use a streaming silver pipeline if querying long ranges.
- **Historical bronze re-ingest required**: existing bronze files for `freq` were captured before V2-FIX-01 with the wrong param names — they hold "latest 5761 samples" rather than the requested window. Re-ingest historical FREQ to get correctly-windowed bronze on disk.

---

## Implementation delta

- **Param-name mismatch — RESOLVED in V2 (2026-05-09).** Connector now sends the Swagger-correct `measurementDateTimeFrom`/`measurementDateTimeTo`. See gridflow commit `fix(V2-A):` on `claude/lucid-mccarthy-9ed3e0`. Live re-verification 2026-05-09: `?measurementDateTimeFrom=2026-05-09T00:00Z&measurementDateTimeTo=2026-05-09T01:00Z` returns 241 rows, all within the 1-hour window.

---

## Changelog

- **2026-05-09 — V2-FIX-01.** Connector `from_param`/`to_param` override on `ENDPOINTS["freq"]` now sends `measurementDateTimeFrom`/`measurementDateTimeTo` (per Swagger). API previously silently ignored the wrong-named params and returned latest 5761 samples regardless of window. Regression tests added under `tests/unit/test_elexon_endpoints.py` and `tests/endpoints/test_endpoint_urls.py`.
- **2026-05-08 — V1.** Live-validated; bug surfaced + documented.

---

## Modelling notes

TODO

---

## Links

- [Official API docs (Swagger UI)](https://bmrs.elexon.co.uk/api-documentation)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/elexon/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/elexon/freq.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/elexon.py)
- Gold view/builder
- [Domain: GB Balancing Mechanism](../../../20-domain/markets/gb-balancing-mechanism.md)
