---
source: neso
dataset_key: generation
vendor: National Energy System Operator (NESO)
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: GB generation mix, percent by fuel
  summary: >-
    NESO's half-hourly GB generation mix as percentage shares of nine fuels, from its Carbon
    Intensity API.
  facts:
    vendor: NESO Carbon Intensity API, national generation mix (beta)
    cadence: Half-hourly periods
    grain: One row per half-hour and fuel
  landscape: power
  what_it_is: >-
    NESO's GB generation mix for each half-hour, as one percentage per fuel for nine fuels, rounded
    to one decimal. NESO's API documentation does not define the total. Checked against its Data Portal
    mix: `wind` includes embedded wind, `hydro` pumped storage. Gas, wind, imports and biomass
    track metered data 30 minutes later (checked); solar's timing is not placed.
  how_used:
    - Renewable, low-carbon and fossil shares as features for carbon-intensity and price models.
    - A solar share, and a wind share including embedded wind, which fuelhh lacks.
    - Reading NESO's national carbon intensity half-hour by half-hour, on the same stamps.
  chart:
    type: stacked-area
    silver: neso/generation
    time: timestamp_utc
    value: generation_percentage
    group: fuel
    series_order: [nuclear, biomass, hydro, coal, other, gas, imports, wind, solar]
    aggregation: sum
    window: {start: "2026-09-14", end: "2026-09-20"}
    unit: "%"
  chart_view:
    title: Generation mix by fuel, 14 to 20 September 2026
    caption: >-
      Silver `neso/generation`, percent of the mix, every half-hour of 14 to 20 September 2026
      (UTC), one value per fuel as sent. Times are NESO's `from`; gas, wind, imports and biomass
      track fuelhh 30 minutes later (a project check).
    alt: >-
      Stacked area chart of the GB generation mix from neso/generation, in percent by fuel, for
      every half-hour of 14 to 20 September 2026 in UTC; each stack sums to between 99.8 and
      100.2. From the bottom: nuclear (8.8 to 15.5), biomass, hydro, coal (zero throughout),
      other, gas (4.2 to 44.8), imports (0 to 22.4) and wind (15.7 to 72.8), with solar on top as
      a daytime band peaking at 32.3 on the 20th.
    x_label: UTC day, as NESO stamps it
    key:
      - {series: solar, label: Solar, codes: solar, tag: solar, note: "Timing not placed: fits the Data Portal's solar at zero lag, not 30 minutes later (checked)."}
      - {series: wind, label: Wind, codes: wind, tag: wind, note: "Includes embedded wind: tracks NESO's Data Portal wind plus embedded wind (checked)."}
      - {series: imports, label: Imports, codes: imports, tag: imports, note: "Not net of exports, but about 1.9 points below the Data Portal's per-link total on average (checked)."}
      - {series: gas, label: Gas, codes: gas, tag: gas}
      - {series: other, label: Other, codes: other, note: "NESO's own category; tracks the Data Portal's other, which NESO says holds batteries and transmission solar (checked)."}
      - {series: coal, label: Coal, codes: coal, paint: hatch-dots, note: "Sent as 0 in every half-hour here."}
      - {series: hydro, label: Hydro, codes: hydro, paint: hatch-lines, note: "Includes pumped storage: tracks the Data Portal's hydro plus storage (checked)."}
      - {series: biomass, label: Biomass, codes: biomass, tag: biomass}
      - {series: nuclear, label: Nuclear, codes: nuclear, tag: nuclear}
  raw_feed:
    note: >-
      gridflow sends up to 14 days a call. A request for 13 to 22 September returned rows stamped
      12 September 23:30 to 21 September 23:30 UTC (checked).
    requests:
      - "GET https://api.carbonintensity.org.uk/generation/2026-09-14T00:00Z/2026-09-21T00:00Z"
    commands:
      - {run: gridflow ingest neso generation --start 2026-09-14 --end 2026-09-21, comment: "bronze; one call, one partition"}
      - {run: gridflow transform neso generation --start 2026-09-14 --end 2026-09-14, comment: the whole window's partition}
  record:
    select:
      filter:
        - {column: timestamp_utc, op: ge, value: "2026-09-20T12:00:00+00:00"}
        - {column: timestamp_utc, op: le, value: "2026-09-20T12:00:00+00:00"}
        - {column: fuel, op: in, value: [biomass, coal, gas, hydro, imports, nuclear, solar, wind]}
      order_by: [fuel]
      columns: [fuel, generation_percentage, timestamp_utc, period_end_utc]
    key: [timestamp_utc, fuel]
    caption: "One half-hour, from 12:00 UTC on 20 September 2026: all fuels but `other`."
    fields:
      timestamp_utc: "NESO's `from`, UTC; gas, wind, imports, biomass track metered data 30 minutes later (checked)"
      fuel: One of the nine fuel names NESO documents, lowercase as sent
      generation_percentage: "NESO's `perc`, percent to one decimal; NESO's API docs do not define the total"
      period_end_utc: "NESO's `to`, UTC: half an hour after `from`"
  notebook:
    lead: >-
      Returns a pandas DataFrame from `silver_neso_generation`, filtered on `timestamp_utc` by UTC
      day, both ends included; lineage columns dropped. The cells sort by time, total each
      half-hour and pivot fuels to columns.
    cells:
      - |
        gen = data.neso.query("generation", "2026-09-14", "2026-09-20")
        gen["timestamp_utc"] = gen.timestamp_utc.dt.tz_convert("UTC")
        gen = gen.sort_values(["timestamp_utc", "fuel"], ignore_index=True)
      - |
        gen[["timestamp_utc", "fuel", "generation_percentage"]].head(9)
      - |
        mix = gen.pivot(index="timestamp_utc", columns="fuel", values="generation_percentage")
        mix.sum(axis=1).describe().round(1)
      - |
        colours = {"nuclear": "#155A6E", "biomass": "#A5713C", "hydro": "#7FA7B0",
                   "coal": "#333333", "other": "#A39A6A", "gas": "#C77E3C",
                   "imports": "#66793B", "wind": "#3E8C97", "solar": "#AFC64E"}
        ax = mix[list(colours)].plot.area(color=colours, ylabel="percent", linewidth=0,
                                          figsize=(8, 3.5))
        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5), fontsize=8);
    needs: generation for 14 to 20 September 2026
    plot_alt: >-
      Stacked area plot of nine fuel shares, 14 to 20 September 2026 in UTC, filling to about 100
      percent throughout. Nuclear is a band of about 9 to 15 at the bottom; wind is the largest
      share most of the week; gas peaks near 45 at the start of the 14th; solar adds a daytime
      band on top each day.
  related:
    - {dataset: neso_data_portal/historic_generation_mix, note: "NESO's MW mix by source, embedded wind and storage split out"}
    - {dataset: elexon/fuelhh, note: "Transmission-metered MW; tracks gas, wind, imports, biomass shares 30 minutes later"}
    - {dataset: neso/carbon_intensity, note: National carbon intensity from the same API and stamps}
    - {dataset: neso/intensity_factors, note: "NESO's emission factor per fuel, in gCO2/kWh"}
  family:
    slug: generation-mix
    members:
      - dataset: generation
        differs: "A chosen window, up to 14 days a call; the chart's source"
        request: "GET https://api.carbonintensity.org.uk/generation/2026-09-14T00:00Z/2026-09-21T00:00Z"
      - dataset: generation_current
        differs: One half-hour per call, the one NESO serves as current; no inputs
        request: "GET https://api.carbonintensity.org.uk/generation"
      - dataset: generation_pt24h
        differs: "The 24 hours before `from`; gridflow sends the ingest start as `from`"
        request: "GET https://api.carbonintensity.org.uk/generation/2026-09-21T00:00Z/pt24h"
---

# NESO - National generation mix range (`generation`)

## Overview

This dataset represents the GB generation mix share by fuel for each half hour. It answers what technologies are supplying electricity at a point in time and is a direct explanatory feature for carbon intensity, price regimes, and renewable penetration models. See [Carbon intensity](../../../20-domain/concepts/carbon-intensity.md) and [Settlement period](../../../20-domain/concepts/settlement-period.md).

---

## API endpoint

| Property | Value |
|----------|-------|
| Base URL | `https://api.carbonintensity.org.uk` |
| Path | `/generation/{from}/{to}` |
| Method | GET |
| Auth | None; send `Accept: application/json` |
| Rate limit | Not documented by NESO; Gridflow config uses 10 req/s. |
| Pagination | None. Dynamic inputs are path segments, not query parameters. |
| Historical depth | TODO - official docs do not state earliest date |
| Publication lag | As published by generation mix endpoint |
| Response format | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| from | string | Yes | Path parameter: Start datetime in ISO8601 format YYYY-MM-DDThh:mmZ | 2024-01-15T00:00Z |
| to | string | Yes | Path parameter: End datetime in ISO8601 format YYYY-MM-DDThh:mmZ | 2024-01-16T00:00Z |

### Working curl example

```bash
curl --ssl-no-revoke -X GET \
  "https://api.carbonintensity.org.uk/generation/2024-01-15T00:00Z/2024-01-16T00:00Z" \
  -H "Accept: application/json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/neso/generation/<year>/<month>/<day>/raw_<timestamp>_<hash>.json`
**Format**: Raw JSON, as received. Immutable after write, with `.meta.json` provenance sidecar.
**Granularity**: One file per API call; range and daily routes may produce one file per chunk/day/period.

### Bronze sample

```json
{"data":[{"from":"2026-04-21T23:30Z","to":"2026-04-22T00:00Z","generationmix":[{"fuel":"biomass","perc":8.7},{"fuel":"gas","perc":11.2},{"fuel":"wind","perc":46.1}]}]}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/neso/generation/year=<YYYY>/month=<MM>/generation_<YYYYMMDD>.parquet`. The date is the request window's first day: the connector files each call's bronze under `window_start.date()` (`connectors/neso/carbon_intensity.py:79`) and the transformer reads only that exact partition (`silver/neso/carbon_intensity.py:87-154`), so one silver file holds the whole window (up to 14 days). Transform the start date; other dates log "covered-but-not-owned" and write nothing.
**Transformer class**: `gridflow.silver.neso.carbon_intensity.GenerationTransformer`
**Pydantic schema**: `gridflow.schemas.neso.GenerationMix`
**Dedup key**: `(timestamp_utc, fuel)`
**Point-in-time field**: `timestamp_utc`

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| timestamp_utc | datetime[UTC] | No | from | Half-hour period start as NESO labels it; see Known issues for the offset against metered data. |
| period_end_utc | datetime[UTC] | Yes | to | Half-hour period end. |
| fuel | str | No | generationmix.fuel | Fuel type, e.g. gas, wind, solar. |
| generation_percentage | float | Yes | generationmix.perc | Share of generation mix in percent. |
| data_provider | str | No | derived | Always neso. |
| ingested_at | datetime[UTC] | No | derived | Silver transform timestamp. |

### Silver sample

```python
[{"timestamp_utc":"2026-04-21T23:30:00+00:00","period_end_utc":"2026-04-22T00:00:00+00:00","fuel":"biomass","generation_percentage":8.7,"data_provider":"neso","ingested_at":"2026-05-04T14:52:28+00:00"},{"timestamp_utc":"2026-04-21T23:30:00+00:00","period_end_utc":"2026-04-22T00:00:00+00:00","fuel":"wind","generation_percentage":46.1,"data_provider":"neso","ingested_at":"2026-05-04T14:52:28+00:00"}]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- Official docs use UTC timestamps ending in `Z`; keep joins in UTC.
- The connector sends no query parameters; all documented inputs are path parameters.
- (Corrected 2026-10-06, v5 page author.) The two bullets that stood here described the intensity routes (null `actual`, `intensity_period` clock-change counts) and do not apply: this route has no intensity fields, and `_transform_generation` (`silver/neso/carbon_intensity.py:559-586`) keeps `from`, `to`, `fuel` and `perc` only, deduplicated on `(timestamp_utc, fuel)`, keep last.
- **No denominator.** NESO's docs as quoted in this vault list the nine fuel names (gas, coal, nuclear, biomass, hydro, imports, solar, wind, other; `../endpoints.md`) but do not say what `perc` divides by. Read 2026-10-06 (v5 page author): the official API docs (`carbon-intensity.github.io/api-definitions`) describe the routes only as "Get generation mix for current half hour", "for the past 24 hours" and "between from and to datetimes", list the nine fuels, and do not define `perc` or its total. NESO's Carbon Intensity methodology (May 2024, receipt `C:/gridflow-data/receipts/v2.2-G-1/sources/14-neso-ci-national-methodology-v2.txt`) covers the intensity estimate only: "Estimated data is used for embedded wind and solar generation."
- **Measured 2026-10-06 (v5 page author), silver 31 Jul to 5 Aug and 12 to 21 Sep 2026 (674 half-hours):** every half-hour carries all nine fuels, `perc` has one decimal, and the nine sum to 99.8 to 100.2. `coal` is 0 throughout. Each response runs from the half-hour *ending* at `from` to the one ending at `to` (the `2026-09-13T00:00Z/2026-09-22T00:00Z` call returned `from` 2026-09-12T23:30Z to 2026-09-21T23:30Z).
- **Stamp offset against metered data (measured 2026-10-06, same rows).** Differenced shares against `elexon/fuelhh` MW and the NESO Data Portal `historic_generation_mix` (latest capture; its `DATETIME` is the half-hour start, checked against fuelhh) correlate best when this route's row stamped `from` = T is set against the metered half-hour starting at T+30 min: gas 0.98 vs 0.69 at zero lag (portal), 0.93 vs 0.67 (fuelhh); wind 0.92 vs 0.62; imports 0.94 vs 0.10; biomass vs fuelhh 0.88 vs 0.50. The control, portal gas against fuelhh gas, peaks at zero lag (0.996). `solar` does not follow: the differenced test is symmetric about zero (0.94 at zero, 0.91 at +/-30 min) and its level fits the portal's `solar_pct` best at zero lag (mean absolute difference 1.01 points, against 1.51 at +30; gas on the same scale 1.26 at zero, 0.69 at +30). Its sunrise and sunset edges are also wider than the portal's (19 and 20 Sep: first non-zero half-hour 05:30 against 06:00, last 18:30 against 17:30; checker, 2026-10-06). The portal's `solar` is itself unanchored to metered data, so `solar`'s timing is not placed; do not shift it with the metered fuels. Within this API, the gas share and `carbon_intensity` `actual` line up at zero lag (0.88). NESO does not explain the labelling; join to settlement-period data with care.
- **Fuel composition (measured, same rows, at the +30 min alignment).** `wind` matches the Data Portal's (`wind` + `wind_emb`) / `generation` (mean absolute difference 1.2 points; `wind` alone is 7.5 points lower), so it includes embedded wind. `hydro` matches (`hydro` + `storage`) / `generation` within 0.07 points on average, so it includes pumped storage; there is no storage fuel. `imports` shows almost no response to exports (regression coefficient on fuelhh exports -0.065), so it is not net of exports; but it is neither the portal's gross figure: it runs about 1.9 points below the portal's `imports_pct` on average (mean absolute difference 1.88, p95 4.4), about 0.86 of fuelhh's summed per-link imports at the median, and is 0.0 in 42 of the 213 half-hours where fuelhh nets to export although per-link imports there are 2 to 1,250 MW (checker, 2026-10-06). The denominator stays undocumented.

---

## Implementation delta

- **`from` / `to` placeholders**: official docs and `config/sources.yaml` use `{from}` and `{to}`; `src/gridflow/connectors/neso/endpoints.py` uses `{from_dt}` and `{to_dt}` internally before formatting the same path.

---

## Modelling notes

Use fuel percentages as features for carbon intensity, price, imbalance, and renewable regime models. Consider wide pivots by fuel and derived `clean_share`, `fossil_share`, `import_share`, and `renewable_share`.

---

## Links

- [Official API docs](https://carbon-intensity.github.io/api-definitions/)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/neso/carbon_intensity.py)
- [Endpoint metadata](../../../../../../Python/gridflow/src/gridflow/connectors/neso/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/neso/carbon_intensity.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/neso.py)
- [Gold view/builder](../../../../../../Python/gridflow/src/gridflow/gold/views/uk_imbalance_context.sql)
- [Domain: Carbon intensity](../../../20-domain/concepts/carbon-intensity.md)

