---
source: elexon
dataset_key: lolpdrm
vendor: Elexon BMRS
last_verified: 2026-07-30
layer_coverage: bronze, silver
page:
  title: Loss-of-load probability and de-rated margin
  summary: >-
    Forecast, per settlement period, of loss-of-load probability and de-rated margin, published on BMRS
    and republished as each period draws nearer.
  facts:
    vendor: Elexon BMRS, dataset LOLPDRM
    cadence: Republished through the day, as the feed's publish times show
    grain: One row per settlement period from each day's publishes
  landscape: power
  what_it_is: >-
    Two forecasts for each half-hour settlement period. The loss-of-load probability is unitless,
    from 0 to 1. The de-rated margin is, in the schema's words, the system margin after de-rating
    capacity for unavailability risk; the feed sends no unit, gridflow's column says MW. Each
    publish covers the coming periods, so one period is forecast more than once.
  how_used:
    - A scarcity feature for GB imbalance price models, from the publish then available.
    - Watching how the evening margin forecast moves between publishes.
    - "Scoring forecast revision: one period from publishes made at different lead times."
  chart:
    type: line
    silver: elexon/lolpdrm
    time: timestamp_utc
    value: derated_margin_mw
    filter:
      - {column: published_at, op: in, value: ["2026-09-13T12:04:53Z", "2026-09-14T12:05:03Z", "2026-09-15T12:05:10Z"]}
    group: published_at
    group_map:
      "2026-09-13 12:04:53.000000+00:00": pub_13
      "2026-09-14 12:05:03.000000+00:00": pub_14
      "2026-09-15 12:05:10.000000+00:00": pub_15
    series_order: [pub_13, pub_14, pub_15]
    aggregation: last
    window: {start: "2026-09-13", end: "2026-09-17"}
    unit: MW
  chart_view:
    title: De-rated margin, three noon publishes, 13 to 15 September 2026
    caption: >-
      Silver `elexon/lolpdrm`, `derated_margin_mw`, MW per settlement period, from the publishes at
      12:04 to 12:05 UTC on 13, 14 and 15 September. Each runs to 03:30 two days on, so periods
      from 13:00 on the 14th and 15th appear twice.
    alt: >-
      Line chart of de-rated margin in MW from three elexon/lolpdrm publishes at 12:04 to 12:05 UTC
      on 13, 14 and 15 September, each running from 13:00 that day to 03:30 two days on. Each
      line's low is early evening: 4,998 at 16:30 on the 13th, 8,389 at 17:30 on the 14th, 7,773 at
      16:30 on the 16th. The highest is 26,302 at 02:30 on the 17th. Where lines overlap, the later
      publish is 1,750 lower at 17:30 on the 14th and 1,747 higher at 17:00 on the 15th.
    x_label: period start, UTC
    key:
      - {series: pub_13, label: "13 Sep, 12:04 UTC", paint: clay}
      - {series: pub_14, label: "14 Sep, 12:05 UTC", paint: petrol, note: "At 17:30 UTC on the 14th: 8,389 MW, against 10,139 a day earlier."}
      - {series: pub_15, label: "15 Sep, 12:05 UTC", paint: horizon, note: "At 17:00 UTC on the 15th: 13,131 MW, against 11,384 a day earlier."}
  raw_feed:
    note: >-
      From the Elexon Insights API in 12-hour publish windows, the widest it accepts. A day's
      bronze holds that day's publishes; `gridflow transform` keeps one row per settlement period
      from them.
    requests:
      - "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/LOLPDRM?publishDateTimeFrom=2026-09-14T00:00:00Z&publishDateTimeTo=2026-09-14T12:00:00Z&page=1"
      - "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/LOLPDRM?publishDateTimeFrom=2026-09-14T12:00:00Z&publishDateTimeTo=2026-09-15T00:00:00Z&page=1"
    commands:
      - {run: gridflow ingest elexon lolpdrm --start 2026-09-13 --end 2026-09-16, comment: "bronze; the end is exclusive"}
      - {run: gridflow transform elexon lolpdrm --start 2026-09-13 --end 2026-09-15, comment: bronze to silver}
  record:
    select:
      filter:
        - {column: settlement_date, op: eq, value: "2026-09-14"}
        - {column: settlement_period, op: in, value: [37, 38, 39, 40]}
      order_by: [settlement_period, published_at]
    key: [settlement_date, settlement_period, published_at]
    caption: "Periods 37 to 40 on 14 September, each from the 13 and 14 September noon publishes."
    fields:
      settlement_date: "Settlement day, UK local calendar, from the vendor `settlementDate`"
      settlement_period: "Half-hour period, 1 to 48; 46 or 50 on clock-change days"
      published_at: "Publish time of the forecast, from the vendor `publishTime`, UTC"
      timestamp_utc: "Period start in UTC, derived from `settlement_date` and `settlement_period`"
      loss_of_load_probability: "From `lossOfLoadProbability`; unitless, the schema expects 0 to 1"
      derated_margin_mw: "From `deratedMargin`; MW by gridflow's column name, the feed sends no unit"
  notebook:
    lead: >-
      Returns a pandas DataFrame from the DuckDB relation `silver_elexon_lolpdrm`, filtered on
      `settlement_date` with both ends included and not de-duplicated: a period returns once per
      publish kept. Lineage columns are dropped.
    cells:
      - |
        df = data.elexon.query("lolpdrm", "2026-09-13", "2026-09-17")
        for col in ["timestamp_utc", "published_at"]:
            df[col] = df[col].dt.tz_convert("UTC")
        df = df[df.published_at.dt.day.isin([13, 14, 15])]
      - df.sort_values(["timestamp_utc", "published_at"])[["timestamp_utc", "published_at", "derated_margin_mw"]].head()
      - |
        wide = df.pivot(index="timestamp_utc", columns="published_at", values="derated_margin_mw")
        wide.columns = wide.columns.strftime("%d %H:%M")
        ax = wide.plot(ylabel="MW", figsize=(8, 3.5))
        ax.legend(title="published_at", loc="upper left", bbox_to_anchor=(1, 1));
    needs: publishes of 13 to 15 September 2026
    plot_alt: >-
      Line plot of derated_margin_mw in MW against timestamp_utc, one line per publish: 00:06 and
      12:04 on 13 September, 00:04 and 12:05 on the 14th and 15th. Lines from the midnight
      publishes stop at 12:30 UTC. Lows near 5,000 MW on the evening of the 13th and 7,800 on the
      16th; highest near 26,300 early on the 17th.
  related:
    - {dataset: elexon/melngc, note: "Indicated margin for the same settlement periods, a second margin measure"}
    - {dataset: elexon/ndf, note: "National demand forecast per settlement period, to read beside the margin"}
    - {dataset: elexon/system_prices, note: "Imbalance prices per settlement period, to test against margin and LOLP"}
    - {dataset: elexon/windfor, note: "Wind generation forecast by hour, to read beside the margin forecast"}
---

# Elexon - Loss of Load Probability and De-Rated Margin (`LOLPDRM`)

## Overview

Loss of Load Probability and De-Rated Margin (LOLPDRM) — reliability forecasts per settlement period, republished through the day (see Publication lag). LOLP is the probability that demand exceeds available generation; de-rated margin is available MW above expected demand after de-rating intermittent capacity. These are the canonical operational reliability signals.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://data.elexon.co.uk/bmrs/api/v1` |
| Path             | `/datasets/LOLPDRM` |
| Method           | GET |
| Auth             | None required for tested endpoints (2026-05-08). Some endpoints accept an `apikey` header (env: `ELEXON_API_KEY`); registration at https://www.elexonportal.co.uk/. |
| Rate limit       | Vendor-published: not stated. Project default 2 req/sec (asyncio.Semaphore); verified safe 2026-05-08. |
| Pagination       | Connector handles via `page=N` query param; stops when `page >= total_pages`. Reference endpoints (`/reference/bmunits/all`) are not paginated. |
| Historical depth | Several years. |
| Publication lag  | Not day-ahead only: each publish carries a half-hour `publishingPeriodCommencingTime` and forecasts the coming settlement periods. Observed in bronze for publishes of 2026-09-15: 48 publishes, one per half-hour, each from about 1 hour ahead to 03:30 UTC one or two days on (up to about 40 hours). Vendor docs not re-checked. |
| Response format  | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `publishDateTimeFrom` | string | Yes | As per Elexon Swagger spec for lolpdrm. Window to `publishDateTimeTo` must not exceed 12 hours (see gotchas). | `2026-05-06T00:00Z` |
| `publishDateTimeTo` | string | Yes | As per Elexon Swagger spec for lolpdrm. Window from `publishDateTimeFrom` must not exceed 12 hours (see gotchas). | `2026-05-06T03:00Z` |
| `format` | string | No | Response data format. Use json/xml to include metadata. | `json` |

### Working curl example

```bash
# Replace <ELEXON_API_KEY> with your env var if you choose to send one (Elexon endpoints
# tested 2026-05-08 do NOT require a key; set anyway for vendor courtesy).
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://data.elexon.co.uk/bmrs/api/v1/datasets/LOLPDRM?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-06T03:00Z&format=json" \
  -o "/tmp/elexon-lolpdrm.json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/elexon/lolpdrm/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per API call (paginated requests append additional files for the same date partition).

### Bronze sample

Captured live 2026-05-08 from the https://data.elexon.co.uk/bmrs/api/v1/datasets/LOLPDRM?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-06T03:00Z&format=json:

```json
{
  "data": [
    {
      "dataset": "LOLPDM",
      "publishTime": "2026-05-06T02:34:22Z",
      "publishingPeriodCommencingTime": "2026-05-06T02:30:00Z",
      "startTime": "2026-05-07T03:30:00Z",
      "settlementDate": "2026-05-07",
      "settlementPeriod": 10,
      "lossOfLoadProbability": 0.0,
      "deratedMargin": 17769.74
    },
    {
      "dataset": "LOLPDM",
      "publishTime": "2026-05-06T02:34:22Z",
      "publishingPeriodCommencingTime": "2026-05-06T02:30:00Z",
      "startTime": "2026-05-07T03:00:00Z",
      "settlementDate": "2026-05-07",
      "settlementPeriod": 9,
      "lossOfLoadProbability": 0.0,
      "deratedMargin": 17801.912
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/elexon/lolpdrm/year=YYYY/month=MM/lolpdrm_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.elexon.lolpdrm.LOLPDRMTransformer`
**Pydantic schema**: `gridflow.schemas.elexon.ElexonLOLPDRM` — validated fail-soft on the full frame at write time (VTA-SCHEMA-01: invalid rows are logged and counted, never dropped).
**Dedup key**: `(settlement_date, settlement_period)`, within one bronze day only (see Known issues)
**Point-in-time field**: `published_at`

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `settlement_date` | `date` | No | `settlementDate` | Settlement date (BST/GMT calendar). |
| `settlement_period` | `int` | No | `settlementPeriod` | 1..50 (DST: 46 spring, 50 autumn). |
| `timestamp_utc` | `datetime[UTC]` | No | _derived_ | Derived from (settlement_date, settlement_period) via `utils/time.settlement_period_to_utc`. |
| `loss_of_load_probability` | `float` | No | `lossOfLoadProbability` | Probability 0..1. |
| `derated_margin_mw` | `float` | No | `deratedMargin` | MW. |
| `published_at` | `datetime[UTC]` | Yes | `publishTime` | Publication time / document vintage; bitemporal point-in-time field. |
| `data_provider` | `str` | No | _derived_ | Default `"elexon"`. |
| `ingested_at` | `datetime[UTC]` | Yes | _derived_ | Stamped at silver transform time, `datetime.now(UTC)` (`silver/elexon/lolpdrm.py:122-126`). |

### Silver sample

```python
[
    {
        "settlement_date": "2026-05-07",
        "settlement_period": 10,
        "timestamp_utc": "2026-05-07T03:30:00+00:00",
        "loss_of_load_probability": 0.0,
        "derated_margin_mw": 17769.74,
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

- **Max 12-hour query window** (live-verified 2026-07-30): requests spanning more than 12 hours between `publishDateTimeFrom` and `publishDateTimeTo` return HTTP 400 with `"The date range between PublishDateTimeFrom and PublishDateTimeTo inclusive must not exceed 12 hours"`; a window of exactly 12 hours returns 200. Not present in the vault's 2026-05-08 verification (the 3-hour sample window masked it); the developer-portal page could not be re-checked (TODO: confirm whether the cap is now stated in the official docs). Note the connector's 24h default chunking violated this — see Implementation delta.
- **Silver keeps one publish per period per bronze day** (`silver/elexon/lolpdrm.py:42,120`): the transformer reads the day's two 12-hour bronze files in file-name order (fetch time, then the first 8 hex digits of the body's SHA-256, `bronze/writer.py:33-34,57`; so fixed for a given bronze but unrelated to publish time) and dedups on `(settlement_date, settlement_period)` with `keep="last"`, with no sort on `published_at`. Bronze rows arrive newest publish first, so the survivor is the earliest publish carrying that period in whichever file is read last (for 2026-09-13 to 2026-09-18, the ~00:04 and ~12:05 UTC publishes; where the file order flips, ~00:04 and ~11:04). A period is kept once per bronze day that forecast it, so reads across days return several rows per period, told apart by `published_at`. `publishingPeriodCommencingTime` is renamed then dropped; `startTime` is not carried (`timestamp_utc` is derived and equals it).
- **De-rated margin** is post-derating intermittent capacity; differs from MELNGC's indicated margin.
- **LOLP unit**: probability (dimensionless 0..1).

---

## Implementation delta

- **Pydantic schema** `ElexonLOLPDRM` exists in `schemas/elexon.py` and is applied via `BaseSilverTransformer._validate_against_schema` (fail-soft).
- **Chunking** (2026-07-30): connector sets `max_chunk_hours=12` on the `lolpdrm` endpoint to respect the vendor's 12-hour window cap. Supersedes G7 (2026-05), which had moved it to the 24h dataclass default — under which every chunk returned HTTP 400 and no bronze ever landed.

---

## Modelling notes

TODO

---

## Links

- [Official API docs (Swagger UI)](https://bmrs.elexon.co.uk/api-documentation)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/elexon/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/elexon/lolpdrm.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/elexon.py)
- Gold view/builder
- [Domain: GB Balancing Mechanism](../../../20-domain/markets/gb-balancing-mechanism.md)
