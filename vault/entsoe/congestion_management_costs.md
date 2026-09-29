---
source: entsoe
dataset_key: congestion_management_costs
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
---

# ENTSO-E — Costs of Congestion Management (A92)

## Overview

Monthly (`P1M`, see the silver callout; "daily" was wrong) congestion-management costs paid by TSOs (in EUR) — the financial
total of redispatching plus countertrading actions per zone. Article 13.1.C
of Regulation (EC) 543/2013. Used to monetise congestion at the bidding-zone
level and as a target for congestion-cost forecast models.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://web-api.tp.entsoe.eu` |
| Path             | `/api` |
| Method           | GET |
| Auth             | Query param `securityToken=$ENTSOE_API_KEY` |
| Rate limit       | 1 req/s default |
| Pagination       | None |
| Historical depth | 2015 onward |
| Publication lag  | D-1 to weekly |
| Response format  | XML |

### ENTSO-E parameter tuple

| Field | Value |
|-------|-------|
| documentType | `A92` |
| processType | (none) |
| businessType (request) | (none) |
| domain-param-name | `in_Domain` only (single zone, `domain_style="zone"`) |

### Single-domain parameters (NOT cross-zonal)

A92 is **single-zone** despite the connector's `zone_pair`-style invocation
in some test paths. The official API treats `in_Domain` as the bidding zone
whose congestion costs are reported. The connector currently calls the API
with `in_Domain == out_Domain` (e.g. `10YGB----------A` for both) which
the server interprets as a single-zone request.

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `securityToken` | str | Yes | API key | UUID |
| `documentType` | str | Yes | `A92` | `A92` |
| `in_Domain` | str | Yes | Bidding zone EIC | `10YGB----------A` |
| `out_Domain` | str | (mirrored) | Same EIC as `in_Domain` | `10YGB----------A` |
| `periodStart` / `periodEnd` | str | Yes | UTC | |

### Working curl example

```bash
curl --ssl-no-revoke -fsS \
  -o "/tmp/entsoe-congestion_management_costs.xml" \
  "https://web-api.tp.entsoe.eu/api?securityToken=$ENTSOE_API_KEY&documentType=A92&in_Domain=10YGB----------A&out_Domain=10YGB----------A&periodStart=202605060000&periodEnd=202605070000"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsoe/congestion_management_costs/<year>/<month>/<day>/raw_<uuid>.xml`
**Format**: Raw XML, immutable.
**Granularity**: One file per (zone, day) — published in EUR.

### Bronze sample

Live 2026-05-08: Acknowledgement, Reason 999 — `COSTS_OF_CONGESTION_MANAGEMENT_R3
[13.1.C] (10YGB----------A)`. A populated payload reports
`<currency_Unit.name>EUR</currency_Unit.name>` with
`<Point><congestionCost_Price.amount>...</congestionCost_Price.amount></Point>`
carrying the monthly cost (corrected 2026-09-29 from 2026-07/08 bronze: the
earlier text named `quantity_Measure_Unit.name` and `<quantity>`, and "daily").
Replies for FR, NL and BE carry three TimeSeries per month, `businessType`
`A46`, `B03` and `B04`, each `curveType` `A03`, `resolution` `P1M`, one Point.
In every populated reply seen, the `B04` value equals `A46` plus `B03`
(project observation; the code list in the vault gives no meaning for `B03`
or `B04`).

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsoe/congestion_management_costs/year=YYYY/month=MM/congestion_management_costs_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsoe.h6_market.CongestionManagementCostsTransformer`
**Pydantic schema**: `gridflow.schemas.entsoe.EntsoeTransmissionMarketAmount`
**Dedup key**: `(timestamp_utc, in_area_code, out_area_code, business_type)`
**Point-in-time field**: `none`

> **Vendor cadence is MONTHLY (`P1M`) — live-probe verified 2026-08-04.**
> A single-UTC-day request returns a real populated document whose
> `Period.timeInterval` spans the **whole calendar month**
> (`[2026-05-31T22:00Z, 2026-06-30T22:00Z)` for a 2026-06-01 request) with
> `<resolution>P1M</resolution>` and one point. Evidence: gridflow
> `.planning/phases/R3-test-integrity/probes/entsoe_A92_congestion_costs_FR_20260601.xml`.
> A92 is a TSO financial-reporting article (13.1.C) that settles over
> accounting periods, not delivery days — structurally unlike the MW/quantity
> families. **Consequence:** this dataset is EXEMPT from gridflow's row-level
> event-window filter (a day-exact trim would delete the row on every day
> except the one containing the period start) — see unit N-9. The prior "P1D"
> value in the silver sample below was a synthetic assumption and was wrong.

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `timestamp_utc` | `datetime[UTC]` | No | period + position | |
| `in_area_code` | `str` | No | `in_Domain.mRID` | Zone EIC |
| `out_area_code` | `str` | No | `out_Domain.mRID` | Mirrors `in_area_code` |
| `amount_eur` | `float` | No | `Point.congestionCost_Price.amount` (suffix match, `parsers.py:148-153`) | EUR (note: amount, not MW); `currency_Unit.name` is not kept |
| `business_type` | `str` | No | TS `businessType` | `A46`, `B03`, `B04` in replies (schema default ""). |
| `resolution` | `str` | No | `Period.resolution` | `P1M` in replies (schema default ""). |
| `published_at` | `datetime[UTC]` | Yes | root `createdDateTime` | Fetch-time stamp (added 2026-09-29) |
| `data_provider` | `str` | No | derived | `"entsoe"` |
| `ingested_at` | `datetime[UTC]` | Yes | derived | |

### Silver sample

Real row from silver (NL, July 2026), replacing the synthetic `P1D` example on 2026-09-29.

```python
[
    {
        "timestamp_utc": "2026-06-30T22:00:00Z",
        "in_area_code": "10YNL----------L",
        "out_area_code": "10YNL----------L",
        "amount_eur": 16882788.28,
        "business_type": "A46",
        "resolution": "P1M",
        "published_at": "2026-09-27T00:38:23Z",
        "data_provider": "entsoe",
        "ingested_at": "2026-09-27T00:44:55Z",
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **Currency, not power.** Use the `EntsoeTransmissionMarketAmount` schema
  (`amount_eur`) — the transformer correctly switches from `quantity_mw` to
  `amount_eur` via `_H6AmountTransformer`.
- Often published with weekly or longer cadence (not daily) — empty daily
  responses do not necessarily indicate the absence of cost.
- Single-zone (`domain_style=zone` per the `congestion_management_costs` entry in `endpoints.py`) — passing different
  `in_Domain`/`out_Domain` may be ignored or cause confusing empties.
- **Silver repeats each month in every daily partition (2026-09-29).** Every
  daily request returns the whole-month document, the transformer is exempt
  from the event-window filter (`_event_window.py:201-204`) and dedups only
  within one partition (`h6_market.py:91-99`). July and August 2026 silver
  holds 744 rows but 24 distinct keys, each stored 31 times, so any read over
  the partitions returns each month-row once per day. De-duplicate on the key
  first.
- **False second point in some months (2026-09-29).** With `curveType` `A03`
  the parser forward-fills to the Period end (`parsers.py:578-600`) and steps
  `P1M` by calendar month from the UTC start (`parsers.py:54-63`, `76-93`).
  July's Period is `[2026-06-30T22:00Z, 2026-07-31T22:00Z)`; one month on from
  the start is 2026-07-30T22:00Z, still inside it, so silver gains a copy of
  July's value at 30 July 22:00 UTC (9 of the 24 keys). August
  (`[07-31T22:00Z, 08-31T22:00Z)`) steps exactly to its end and gains none.
  Any month following a shorter month is affected.
- A month's row is stamped at its Period start in UTC (July: 2026-06-30T22:00Z),
  so a `timestamp_utc` filter from 1 July misses July's real row but keeps the
  false 30 July row. Start the range a day earlier. Checked 2026-09-29 with
  `data.entsoe.query("congestion_management_costs", "2026-07-01", "2026-07-31")`:
  465 rows, only the 30 July 22:00 and 31 July 22:00 UTC (August) stamps;
  from `"2026-06-30"` it returns all 744 rows, 24 distinct keys.

---

## Implementation delta

- **Tuple recorded:** `(documentType=A92, processType=none, businessType=none-in-request, domain=in_Domain only)`. Matches code — the `congestion_management_costs` entry in `endpoints.py` `DOC_TYPES`.
- **Live validation 2026-05-08 GB for 2026-05-06:** Acknowledgement, Reason 999. **EMPTY** — cause: "border has zero allocation in window" (publication cadence weekly/monthly; no GB cost record for that single day).
- A92 is the only `domain_style="zone"` dataset in this batch; matches advisor's note that A92 should NOT be treated as cross-zonal.

---

## Modelling notes

- Stitch with A63 + A91 to get the full congestion-management story —
  redispatch volumes, countertrading volumes, and the EUR-cost.
- Use as target for cost forecasting models conditioned on weather, NTC, and
  load-forecast features.

---

## Links

- [Official API docs (PDF)](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.pdf)
- `src/gridflow/connectors/entsoe/endpoints.py`
- `src/gridflow/silver/entsoe/h6_market.py`
- `src/gridflow/schemas/entsoe.py`
