---
source: elexon
dataset_key: fuelhh
vendor: Elexon BMRS
last_verified: 2026-09-09
layer_coverage: bronze, silver
v2_fix_history:
  - date: 2026-05-20
    phase: gridflow-G5-W2.2
    pr: https://github.com/EBentham/gridflow/pull/7
    change: silver transformer now casts `published_at` to UTC datetime and includes it in output_cols (previously renamed but silently dropped before write)
  - date: 2026-09-07
    phase: gridflow-v0.21-F
    pr: https://github.com/EBentham/gridflow/pull/77
    change: settlement identity (settlement_date, settlement_period, timestamp_utc) derived from the vendor start instant instead of the settlementDate label; DATASET_VERSION 1.0.0 -> 2.0.0
page:
  title: Generation by fuel type
  summary: >-
    Great Britain's generation outturn for every half-hour settlement period: one MW figure per
    Elexon fuel-type code.
  facts:
    vendor: Elexon BMRS, dataset FUELHH
    cadence: Every 30 minutes
    grain: One row per settlement period and fuel-type code
  landscape: power
  what_it_is: >-
    Elexon's outturn by fuel type for each GB settlement period: one MW figure per code for
    transmission-metered generation, from CCGT and nuclear to wind and each interconnector. A
    recent half-hour carries 20 codes. The interconnector codes are signed, and so is pumped
    storage (PS), whose sign Elexon does not explain. There is no solar code.
  how_used:
    - Fuel-mix and residual-demand features for a GB power price model.
    - Net interconnector flow by link, from the signed interconnector codes.
    - Checking a wind generation forecast against outturn.
  chart:
    type: stacked-area
    silver: elexon/fuelhh
    time: timestamp_utc
    value: generation_mw
    filter:
      - {column: settlement_date, op: ge, value: "2026-09-20"}
      - {column: settlement_date, op: le, value: "2026-09-26"}
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
    window: {start: "2026-09-19", end: "2026-09-26"}
    unit: MW
  chart_view:
    title: Generation by fuel, 20 to 26 September 2026
    caption: >-
      Silver `elexon/fuelhh`, MW, every half-hour of settlement dates 20 to 26 September 2026,
      with a group's codes summed. Positive values stack above zero and negative values hang
      below it; nothing is clipped.
    alt: >-
      Stacked area chart of GB generation by fuel from elexon/fuelhh, in MW, for every half-hour
      of settlement dates 20 to 26 September 2026. From zero upward: nuclear (3.2 to 4.0 GW),
      biomass, non-pumped hydro, coal and oil, other, gas (2.1 to 15.9 GW) and wind (1.3 to 16.1
      GW), then net imports and pumped storage when positive. Net exports and pumped storage hang
      below zero; net interconnector flow runs from 6.3 GW of exports to 6.7 GW of imports.
    x_label: settlement date; each starts at 23:00 UTC
    key:
      - {series: ps, label: Pumped storage, codes: PS, paint: hatch-cross, note: "Signed; Elexon does not say what the sign means. Drawn above or below zero as it falls."}
      - {series: imports, label: "Interconnectors, net", codes: "INT*, 10 codes", tag: net imports, note: "Positive is import to GB, checked against demand; Elexon does not state it."}
      - {series: wind, label: Wind, codes: WIND, tag: wind}
      - {series: gas, label: Gas, codes: "CCGT, OCGT", tag: gas}
      - {series: other, label: Other, codes: OTHER, tag: other, note: "Elexon's own code; what it holds is undocumented."}
      - {series: coal_oil, label: Coal and oil, codes: "COAL, OIL", paint: hatch-dots, note: "Stacked, but 133 MW at most here: too thin to see."}
      - {series: npshyd, label: "Hydro, not pumped", codes: NPSHYD, paint: hatch-lines}
      - {series: biomass, label: Biomass, codes: BIOMASS, tag: biomass}
      - {series: nuclear, label: Nuclear, codes: NUCLEAR, tag: nuclear}
  raw_feed:
    note: >-
      From the Elexon Insights API, in 24-hour publish windows. `gridflow ingest` writes each
      response to bronze; `gridflow transform` types it into silver, reading a day either side.
    requests:
      - "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELHH?publishDateTimeFrom=2026-09-19T00:00:00Z&publishDateTimeTo=2026-09-20T00:00:00Z&page=1"
    commands:
      - {run: gridflow ingest elexon fuelhh --start 2026-09-19 --end 2026-09-28, comment: "bronze; the end is exclusive"}
      - {run: gridflow transform elexon fuelhh --start 2026-09-20 --end 2026-09-26, comment: bronze to silver}
  record:
    select:
      filter:
        - {column: settlement_date, op: eq, value: "2026-09-26"}
        - {column: settlement_period, op: eq, value: 25}
        - {column: fuel_type, op: in, value: [BIOMASS, CCGT, INTFR, NPSHYD, NUCLEAR, OTHER, PS, WIND]}
      order_by: [fuel_type]
    mark: {fuel_type: PS}
    key: [settlement_date, settlement_period, fuel_type]
    caption: "All eight rows are settlement date 2026-09-26, period 25: 8 of its 20 codes."
    fields:
      settlement_date: GB settlement date, recomputed from the vendor start time
      settlement_period: Half-hour of the day, 1 to 50 (46 or 50 on clock-change days)
      timestamp_utc: Start of the half-hour, from the vendor start time
      fuel_type: Elexon fuel-type code, uppercase as sent
      generation_mw: MW for the period; interconnectors and PS are signed
      published_at: Vendor publish time
      data_provider: "Same on every row: elexon"
      ingested_at: When the silver transform ran
  notebook:
    lead: >-
      Returns a pandas DataFrame from the DuckDB relation `silver_elexon_fuelhh`, filtered on
      `settlement_date` with both ends included. Lineage columns are dropped.
    cells:
      - df = data.elexon.query("fuelhh", "2026-09-20", "2026-09-26")
      - df[["settlement_date", "settlement_period", "fuel_type", "generation_mw"]].head()
      - |
        wind = df[df.fuel_type == "WIND"]
        wind.plot(x="timestamp_utc", y="generation_mw", ylabel="MW",
                  color="#3E8C97", figsize=(8, 3.5))
    needs: 20 to 26 September 2026
    plot_alt: >-
      Line plot of WIND generation_mw against timestamp_utc for settlement dates 20 to 26 September
      2026: about 16,000 MW at the start, falling to about 1,300 MW late on the 22nd, peaks near
      10,500 MW on the 23rd and 11,700 MW on the 25th, about 7,000 MW at the end.
  related:
    - {dataset: elexon/fuelinst, note: "The same outturn by fuel type, every five minutes"}
    - {dataset: neso_data_portal/historic_generation_mix, note: Where GB solar outturn lives}
    - {dataset: elexon/bmunits_reference, note: "The Balancing Mechanism unit register"}
    - {dataset: elexon/indo, note: Demand outturn for the same settlement periods}
---

# Elexon - Half-Hourly Generation Outturn by Fuel Type (`FUELHH`)

## Overview

Half-hourly generation outturn aggregated by fuel type (FUELHH) — the realised MWh in each settlement period split by fuel category (CCGT, coal, nuclear, wind, biomass, etc.). **FUELHH does not include solar** — structural exclusion confirmed by measurement and Bobbo's ruling 2026-08-31 (gridflow_models v1.8 L3 premise check: zero solar rows; the earlier "solar" in this sentence contradicted this page's own schema table; solar outturn lives elsewhere, e.g. NESO `historic_generation_mix.solar`). FUELHH is the canonical observation series for GB *transmission-metered* generation mix and underpins capacity-factor analytics and emissions reporting.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://data.elexon.co.uk/bmrs/api/v1` |
| Path             | `/datasets/FUELHH` |
| Method           | GET |
| Auth             | None required for tested endpoints (2026-05-08). Some endpoints accept an `apikey` header (env: `ELEXON_API_KEY`); registration at https://www.elexonportal.co.uk/. |
| Rate limit       | Vendor-published: not stated. Project default 2 req/sec (asyncio.Semaphore); verified safe 2026-05-08. |
| Pagination       | Connector handles via `page=N` query param; stops when `page >= total_pages`. Reference endpoints (`/reference/bmunits/all`) are not paginated. |
| Historical depth | Several years. |
| Publication lag  | Soon after each settlement period closes. |
| Response format  | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `publishDateTimeFrom` | string | No | As per Elexon Swagger spec for fuelhh. | `2026-05-06T00:00Z` |
| `publishDateTimeTo` | string | No | As per Elexon Swagger spec for fuelhh. | `2026-05-06T03:00Z` |
| `settlementDateFrom` | string | No | As per Elexon Swagger spec for fuelhh. | `2026-05-06` |
| `settlementDateTo` | string | No | As per Elexon Swagger spec for fuelhh. | `2026-05-07` |
| `settlementPeriod` | array | No | List of Settlement Periods | `24` |
| `fuelType` | array | No | Fuel Type e.g. NUCLEAR | `CCGT` |
| `format` | string | No | Response data format. Use json/xml to include metadata. | `json` |

### Working curl example

```bash
# Replace <ELEXON_API_KEY> with your env var if you choose to send one (Elexon endpoints
# tested 2026-05-08 do NOT require a key; set anyway for vendor courtesy).
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELHH?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-06T03:00Z&format=json" \
  -o "/tmp/elexon-fuelhh.json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/elexon/fuelhh/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per API call (paginated requests append additional files for the same date partition).

### Bronze sample

Captured live 2026-05-08 from the https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELHH?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-06T03:00Z&format=json:

```json
{
  "data": [
    {
      "dataset": "FUELHH",
      "publishTime": "2026-05-06T03:00:00Z",
      "startTime": "2026-05-06T02:30:00Z",
      "settlementDate": "2026-05-06",
      "settlementPeriod": 8,
      "fuelType": "BIOMASS",
      "generation": 2821
    },
    {
      "dataset": "FUELHH",
      "publishTime": "2026-05-06T03:00:00Z",
      "startTime": "2026-05-06T02:30:00Z",
      "settlementDate": "2026-05-06",
      "settlementPeriod": 8,
      "fuelType": "CCGT",
      "generation": 7729
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/elexon/fuelhh/year=YYYY/month=MM/fuelhh_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.elexon.fuelhh.FuelHHTransformer`
**Pydantic schema**: `gridflow.schemas.elexon.ElexonFuelHH`
**Dedup key**: `(settlement_date, settlement_period, fuel_type)`
**Point-in-time field**: `published_at`

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `settlement_date` | `date` | No | _derived_ | Settlement date (BST/GMT calendar), recomputed from `timestamp_utc` with `utc_to_settlement_period` since 2.0.0; the vendor `settlementDate` label is only a counted fallback (`gridflow/silver/elexon/fuelhh.py:102-165`). |
| `settlement_period` | `int` | No | _derived_ | 1..50 (DST: 46 spring, 50 autumn), recomputed from `timestamp_utc` like `settlement_date`. |
| `timestamp_utc` | `datetime[UTC]` | No | `startTime` (coalesced with `startTimeOfHalfHrPeriod`) | The vendor start instant of the half-hour (`fuelhh.py:102-165`). |
| `fuel_type` | `str` | No | `fuelType` | Fuel category (CCGT, COAL, NUCLEAR, WIND, etc.). |
| `generation_mw` | `float` | No | `generation` | MW. |
| `published_at` | `datetime[UTC]` | Yes | `publishDateTime` (also `publishTime`) | Publication time. G5-W2.2: now cast to UTC-aware datetime and included in `output_cols`; previously the rename produced the column but it was dropped before write. |
| `data_provider` | `str` | No | _derived_ | Default `"elexon"`. |
| `ingested_at` | `datetime[UTC]` | Yes | _derived_ | When the silver transform ran: stamped `datetime.now(UTC)` by the transformer (`fuelhh.py:191-195`), not the bronze ingest time. |

### Silver sample

```python
[
    {
        "settlement_date": "2026-05-06",
        "settlement_period": 8,
        "timestamp_utc": "2026-05-06T02:30:00+00:00",
        "fuel_type": "BIOMASS",
        "generation_mw": 2821,
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

- **Settlement period range 1..50** — DST handling required.
- **Interconnector codes are SIGNED, and positive = IMPORT to GB** (established
  2026-09-09, gridflow_models RULINGS #542). Verified against the demand identity rather
  than assumed: summing every FUELHH fuel type against INDO over 816 half-hours gives
  MAE **945.8 MW** as stored, versus **6,546.3 MW** with the ten INT signs flipped — a 7x
  degradation. Net INT flow over that window averages **+2,754.4 MW** (GB importing).
  A consumer that nets these must subtract the **signed** value; taking `abs()`, clipping
  at zero or zero-filling silently corrupts the result.
- **Negative values are the majority regime for several codes, not an edge case**
  (measured over 816 headline and 17,520 diagnostic half-hours, 2026-09-09). All ten INT
  codes go negative, from `INTNSL` at 2.7% of periods to `INTGRNL` at 97.9%. `PS` is
  negative in ~60% of periods in both windows. `NPSHYD` is **never** negative in either.
  Coverage is complete for all twelve codes — a full row per period, zero nulls, zero
  missing rows — so a gap-filling strategy is unnecessary as well as harmful.
- **`OIL` is legitimately zero, and that is not a data gap.** Identically 0.0 MW in 816 of
  816 headline periods, and exactly one 8.0 MW half-hour in a full 17,520-period year.
  Confirmed by Bobbo 2026-09-09 (RULINGS #537): oil plant is too expensive to start. Do not
  raise it as missing coverage. TODO: verify what `OTHER` contains — it averages 755.4 MW
  every period (16.2% of mean NUCLEAR), is never negative, and no vendor document, repo or
  vault page defines its composition.
- **Partition grain is capture date; silver grain is settlement date (v0.21 unit P,
  PR #78).** A bronze capture partition D does not hold exactly settlement date D.
  Measured over 600 fuelhh bronze files (`settlement_date - partition_date`):
  `{-1: 4,074, 0: 542,903, +1: 14,672}` — fuelhh spills in **both** directions, so
  the silver file for date D is built by reading bronze partitions **D-1, D and
  D+1**, applying each partition's own publication window, then trimming to the
  rows date D owns. Before this, the per-date overwrite wrote the same entity key
  into two files: **4,502 duplicate keys** on disk. After the rebuild: **0**, with
  row conservation proven exactly against all 2,091 bronze bodies (bronze distinct
  keys == silver rows == 1,666,217, none missing either way).
  **Live-running precondition:** because D's own last GMT-season period also
  appears in partition D+1, date D is final only once bronze D+1 exists. The
  shipped defaults re-touch it (24 h lookback, inclusive date range); a transform
  window narrower than ~24 h would leave yesterday's last period out of silver
  until the next wider run.
- **27 short days / 33 missing periods remain, and every one is a vendor gap** —
  each was confirmed absent from bronze, not dropped in transform. Includes
  2021-09-01 SP1, whose instant is 2021-08-31T23:00Z (BST): the history starts at
  2021-09-01, so the partition holding it does not exist.
- **`fuelType` casing**: API returns uppercase (CCGT, COAL); transformer preserves casing.
- **Last-period date label (RESOLVED 2026-09-07, gridflow v0.21 unit F, PR #77).**
  Publish-window responses return the day's **last** settlement period (SP48;
  SP46/SP50 on DST days) with `startTime` = D-1 22:30Z but `settlementDate` = D.
  Silver derived `timestamp_utc` from the label, so 5,202 rows over 289 days
  were stamped 24 h late and 54 entity keys collided with differing
  `generation_mw`. From `DATASET_VERSION` 2.0.0 the transformer derives
  `(settlement_date, settlement_period, timestamp_utc)` from the vendor start
  instant (`startTime` / `startTimeOfHalfHrPeriod`, coalesced) via
  `utc_to_settlement_period`; the label path is a counted fallback only
  (`start_time_fallback_count`, 0 on every probe; raw nulls 0 / 1,955,044).
  Independent read-only probe on live bronze (2021-09-20..23, 2022-07-14..16,
  2022-03-26..28 spring/46, 2021-10-30..11-01 autumn/50): 0 conflicting keys,
  0 calendar holes, versus 12-15 conflicting keys and 0-36 holes per window
  under the label convention on the same bytes. **On-disk silver was rebuilt
  full-tree on 2026-09-07 under unit P** (1,833 dates, ~16 min): every row is
  `dataset_version` 2.0.0, 0 start-time-fallback rows, and the mixed-version
  transient is over.
  `TODO: verify` — vendor precedence is undocumented: Elexon's FUELHH docs
  define `settlementDate`/`settlementPeriod` as the temporal fields and show
  `startTime` without stating which wins when they conflict. The data-level
  finding above is evidence about the bytes, not a claim about Elexon's intent.

---

## Implementation delta

- **No documented `from_param`/`to_param` override** needed — connector uses default `publishDateTimeFrom/To` which docs accept (alongside `settlementDateFrom/To`).
- **Schema**: `ElexonFuelHH` declared and matches silver output.

### V2-FIX changelog

- **2026-09-07 — gridflow v0.21 unit F (PR #77)**: settlement identity derived
  from the vendor start instant; `DATASET_VERSION` 2.0.0; counted label
  fallback; see Known issues. Full-tree acceptance recorded in gridflow
  `v0.21-RESULTS.md` §F+P after unit P's rebuild.
- **2026-05-20 — gridflow G5-W2.2 (PR #7)**: silver transformer now casts
  `published_at` (renamed from `publishDateTime`) to a UTC-aware datetime
  and includes it in `output_cols`. Previously the column was renamed but
  the `select(output_cols)` step dropped it before write — schema declared
  `published_at: datetime | None` but Parquet never carried it (W2.2
  schema-vs-output silent-drop pattern). Acceptance test
  `test_published_at_emitted_when_bronze_carries_it` pins the fix.

---

## Modelling notes

TODO

---

## Links

- [Official API docs (Swagger UI)](https://bmrs.elexon.co.uk/api-documentation)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/elexon/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/elexon/fuelhh.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/elexon.py)
- Gold view/builder
- [Domain: GB Balancing Mechanism](../../../20-domain/markets/gb-balancing-mechanism.md)
