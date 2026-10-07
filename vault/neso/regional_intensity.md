---
source: neso
dataset_key: regional_intensity
vendor: National Energy System Operator (NESO)
last_verified: 2026-05-09
layer_coverage: bronze, silver
page:
  title: Regional carbon intensity
  summary: >-
    NESO's forecast carbon intensity, band and generation mix per half-hour for GB's distribution
    regions, England, Scotland, Wales and GB.
  facts:
    vendor: NESO Carbon Intensity API, regional routes (beta)
    cadence: Half-hourly periods; NESO's public forecasts run up to two days ahead
    grain: One row per half-hour, region and fuel
  landscape: power
  what_it_is: >-
    NESO's forecast carbon intensity for each region and half-hour, its band from `very low` to
    `very high`, and the region's generation mix in percent by fuel. Region ids 1 to 14 are
    distribution (DNO) areas, 15 to 17 England, Scotland and Wales, 18 GB: never average all 18.
    NESO's regional examples carry `forecast` and `index`, no `actual`.
  how_used:
    - "Carbon-aware scheduling: move flexible load to a region and half-hour in a low band."
    - Local carbon and fuel-mix features for regional demand, price or siting models.
    - Explaining a region's intensity through its generation mix, fuel by fuel.
  chart:
    type: line
    silver: neso/regional_intensity
    time: timestamp_utc
    value: forecast_gco2_kwh
    filter:
      - {column: regionid, op: in, value: [1, 7, 13, 18]}
    dedup: {on: [timestamp_utc, regionid], order_by: fuel}
    group: shortname
    group_map:
      "South Wales": south_wales
      "London": london
      "GB": gb
      "North Scotland": north_scotland
    series_order: [south_wales, london, gb, north_scotland]
    aggregation: last
    window: {start: "2026-09-14", end: "2026-09-20"}
    unit: gCO2/kWh
  chart_view:
    title: Forecast intensity in four regions, 14 to 20 September 2026
    caption: >-
      Silver `neso/regional_intensity`, gCO2/kWh, NESO's forecast per half-hour, 14 to 20 September
      2026, regions 7, 13, 18 and 1, one value per region and half-hour. NESO does not say whether
      a past half-hour's forecast is revised.
    alt: >-
      Line chart of NESO's forecast carbon intensity from neso/regional_intensity, in gCO2/kWh, per
      half-hour from 00:00 UTC on 14 September to 23:30 UTC on 20 September 2026, for four regions.
      South Wales is highest except around midday on the 15th and 20th, when it drops below London,
      to 6 at 14:30 UTC on the 20th; it peaks at 390 at 22:00 UTC that day. London runs from 39 to
      246, GB from 30 to 197; both stay under 150 from 17 to 19 September. North Scotland stays at 0.
    x_label: half-hour start, UTC
    key:
      - {series: south_wales, label: South Wales, codes: regionid 7, paint: clay}
      - {series: london, label: London, codes: regionid 13, paint: olive}
      - {series: gb, label: GB, codes: regionid 18, paint: petrol, note: "GB as a whole; a project check found it on average nearer the national `actual` than its `forecast`."}
      - {series: north_scotland, label: North Scotland, codes: regionid 1, paint: horizon, note: "At 0 gCO2/kWh for every half-hour shown."}
  raw_feed:
    note: >-
      In these responses the first half-hour ends at `from`, the last at `to`; bronze files the
      whole window under its first day.
    requests:
      - "GET https://api.carbonintensity.org.uk/regional/intensity/2026-09-13T00:00Z/2026-09-22T00:00Z"
    commands:
      - {run: gridflow ingest neso regional_intensity --start 2026-09-13 --end 2026-09-22, comment: "bronze; requests split at 14 days"}
      - {run: gridflow transform neso regional_intensity --start 2026-09-13 --end 2026-09-13, comment: "the window's first day holds it"}
  record:
    select:
      filter:
        - {column: timestamp_utc, op: eq, value: "2026-09-17T16:30:00Z"}
        - {column: fuel, op: eq, value: wind}
        - {column: regionid, op: in, value: [1, 5, 7, 11, 13, 15, 17, 18]}
      order_by: [regionid]
      columns: [regionid, shortname, forecast_gco2_kwh, intensity_index, fuel, generation_percentage, actual_gco2_kwh, timestamp_utc]
    key: [timestamp_utc, regionid, shortname, postcode, fuel]
    caption: "The half-hour from 16:30 UTC on 17 September 2026: the `wind` row of eight regions."
    fields:
      regionid: "NESO region id: 1 to 14 DNO areas, 15 to 17 nations, 18 GB"
      shortname: "NESO's short region name, the vendor's `shortname`"
      forecast_gco2_kwh: "NESO's forecast for the region and half-hour, gCO2/kWh; repeats on each fuel row"
      intensity_index: "NESO's band for the forecast, `very low` to `very high`; cut-offs not sent"
      fuel: "One of nine fuels in the region's `generationmix`"
      generation_percentage: "The fuel's share of the region's generation mix in percent, from `perc`"
      actual_gco2_kwh: "The vendor's `actual`; null here, as these regional responses carry none"
      timestamp_utc: "Start of the half-hour, from the vendor's `from`"
      postcode: "Outward postcode on the postcode routes; an empty string, not null, here"
      period_end_utc: "End of the half-hour, from the vendor's `to`"
      dnoregion: "Distribution network operator's name; nations and GB carry their own name"
  notebook:
    lead: >-
      Returns a pandas DataFrame from `silver_neso_regional_intensity`, filtered on `timestamp_utc`,
      both ends included; lineage columns dropped. Rows are region by half-hour by fuel, so keep one
      row per region and half-hour for intensity.
    cells:
      - |
        df = data.neso.query("regional_intensity", "2026-09-14", "2026-09-20")
        df["timestamp_utc"] = df.timestamp_utc.dt.tz_convert("UTC")
        df = df.sort_values(["timestamp_utc", "regionid", "fuel"], ignore_index=True)
      - |
        cols = ["timestamp_utc", "regionid", "shortname", "fuel", "generation_percentage", "forecast_gco2_kwh", "intensity_index"]
        df[df.regionid == 7][cols].head(9)
      - |
        one = df.drop_duplicates(["timestamp_utc", "regionid"])
        one[one.regionid <= 14].groupby("shortname").forecast_gco2_kwh.mean().round().sort_values()
      - |
        gas = df[(df.fuel == "gas") & df.regionid.isin([7, 13, 18, 1])]
        ax = gas.pivot(index="timestamp_utc", columns="shortname", values="generation_percentage")[
            ["South Wales", "London", "GB", "North Scotland"]
        ].plot(ylabel="gas share of generation, %", color=["#C77E3C", "#66793B", "#155A6E", "#3E8C97"], figsize=(8, 3.5))
        ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.3), frameon=False);
    needs: "`regional_intensity` for 13 to 21 September 2026"
    plot_alt: >-
      Line plot of the gas share of generation, in percent, per half-hour from 14 to 20 September
      2026: South Wales (clay), London (olive), GB (petrol), North Scotland (horizon). South Wales
      swings from 1.3 at 14:30 UTC on the 20th to 98.9 at 22:00 UTC; London runs 4.8 to 59.7, GB
      4.2 to 44.8; North Scotland stays at 0.
  related:
    - {dataset: neso/carbon_intensity, note: "The national route, with NESO's estimated actual beside its forecast"}
    - {dataset: neso/generation, note: "The national generation mix, by the same nine fuels"}
    - {dataset: neso/intensity_factors, note: "Each fuel's emission factor, to weigh the mix shares here"}
    - {dataset: neso_data_portal/historic_generation_mix, note: "NESO's national outturn mix, to set against these forecast shares"}
  family:
    slug: regional-carbon-intensity
    members:
      - dataset: regional_intensity
        differs: "Every region over a `from`/`to` window; gridflow splits requests at 14 days"
        request: "GET https://api.carbonintensity.org.uk/regional/intensity/2026-09-13T00:00Z/2026-09-22T00:00Z"
      - dataset: regional_intensity_fw24h
        differs: "Every region: 49 half-hours, the first ending at `from`"
        request: "GET https://api.carbonintensity.org.uk/regional/intensity/2026-08-01T00:00Z/fw24h"
      - dataset: regional_intensity_fw48h
        differs: "Every region: 97 half-hours, the first ending at `from`"
        request: "GET https://api.carbonintensity.org.uk/regional/intensity/2026-08-01T00:00Z/fw48h"
      - dataset: regional_intensity_pt24h
        differs: "Every region: 49 half-hours, the last ending at `from`"
        request: "GET https://api.carbonintensity.org.uk/regional/intensity/2026-08-01T00:00Z/pt24h"
      - dataset: regional_intensity_postcode
        differs: "One postcode, default `RG10` (region 12), over a window; the response lacks `dnoregion`"
        request: "GET https://api.carbonintensity.org.uk/regional/intensity/2026-08-01T00:00Z/2026-08-06T00:00Z/postcode/RG10"
      - dataset: regional_intensity_regionid
        differs: "One region over a window; gridflow's default is region 13, London"
        request: "GET https://api.carbonintensity.org.uk/regional/intensity/2026-08-01T00:00Z/2026-08-06T00:00Z/regionid/13"
      - dataset: regional_intensity_fw24h_postcode
        differs: "One postcode, default `RG10`: 49 half-hours, the first ending at `from`"
        request: "GET https://api.carbonintensity.org.uk/regional/intensity/2026-08-01T00:00Z/fw24h/postcode/RG10"
      - dataset: regional_intensity_fw24h_regionid
        differs: "One region, default 13: 49 half-hours, the first ending at `from`"
        request: "GET https://api.carbonintensity.org.uk/regional/intensity/2026-08-01T00:00Z/fw24h/regionid/13"
      - dataset: regional_intensity_fw48h_postcode
        differs: "One postcode, default `RG10`: 97 half-hours, the first ending at `from`"
        request: "GET https://api.carbonintensity.org.uk/regional/intensity/2026-08-01T00:00Z/fw48h/postcode/RG10"
      - dataset: regional_intensity_fw48h_regionid
        differs: "One region, default 13: 97 half-hours, the first ending at `from`"
        request: "GET https://api.carbonintensity.org.uk/regional/intensity/2026-08-01T00:00Z/fw48h/regionid/13"
      - dataset: regional_intensity_pt24h_postcode
        differs: "One postcode, default `RG10`: 49 half-hours, the last ending at `from`"
        request: "GET https://api.carbonintensity.org.uk/regional/intensity/2026-08-01T00:00Z/pt24h/postcode/RG10"
      - dataset: regional_intensity_pt24h_regionid
        differs: "One region, default 13: 49 half-hours, the last ending at `from`"
        request: "GET https://api.carbonintensity.org.uk/regional/intensity/2026-08-01T00:00Z/pt24h/regionid/13"
      - dataset: regional_current
        differs: "Every region, one half-hour: the one NESO serves as current when fetched"
        request: "GET https://api.carbonintensity.org.uk/regional"
      - dataset: regional_england
        differs: "Region 15, England, for the half-hour NESO serves as current"
        request: "GET https://api.carbonintensity.org.uk/regional/england"
      - dataset: regional_scotland
        differs: "Region 16, Scotland, for the half-hour NESO serves as current"
        request: "GET https://api.carbonintensity.org.uk/regional/scotland"
      - dataset: regional_wales
        differs: "Region 17, Wales, for the half-hour NESO serves as current"
        request: "GET https://api.carbonintensity.org.uk/regional/wales"
      - dataset: regional_postcode
        differs: "One postcode, default `RG10` (region 12), for the current half-hour"
        request: "GET https://api.carbonintensity.org.uk/regional/postcode/RG10"
      - dataset: regional_regionid
        differs: "One region, default 13 (London), for the current half-hour"
        request: "GET https://api.carbonintensity.org.uk/regional/regionid/13"
---

# NESO - Regional carbon intensity range (`regional_intensity`)

## Overview

This dataset represents regional carbon intensity and regional generation mix for GB DNO or nation-level areas. It answers where electricity consumption is cleaner or dirtier within GB, useful for regional demand, siting, carbon-aware scheduling, and distribution-aware modelling. See [Carbon intensity](../../../20-domain/concepts/carbon-intensity.md) and [Settlement period](../../../20-domain/concepts/settlement-period.md).

---

## API endpoint

| Property | Value |
|----------|-------|
| Base URL | `https://api.carbonintensity.org.uk` |
| Path | `/regional/intensity/{from}/{to}` |
| Method | GET |
| Auth | None; send `Accept: application/json` |
| Rate limit | Not documented by NESO; Gridflow config uses 10 req/s. |
| Pagination | None. Dynamic inputs are path segments, not query parameters. |
| Historical depth | TODO - official docs do not state earliest date |
| Publication lag | Forecast/index published per region and half hour; actual estimate not guaranteed |
| Response format | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| from | string | Yes | Path parameter: Start datetime in ISO8601 format YYYY-MM-DDThh:mmZ | 2024-01-15T00:00Z |
| to | string | Yes | Path parameter: End datetime in ISO8601 format YYYY-MM-DDThh:mmZ | 2024-01-16T00:00Z |

### Working curl example

```bash
curl --ssl-no-revoke -X GET \
  "https://api.carbonintensity.org.uk/regional/intensity/2024-01-15T00:00Z/2024-01-16T00:00Z" \
  -H "Accept: application/json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/neso/regional_intensity/<year>/<month>/<day>/raw_<timestamp>_<hash>.json`
**Format**: Raw JSON, as received. Immutable after write, with `.meta.json` provenance sidecar.
**Granularity**: One file per API call; range and daily routes may produce one file per chunk/day/period.

### Bronze sample

Period-keyed envelope: each `data[]` entry holds `from`/`to` plus a `regions[]`
list (≈18 GB regions). `intensity` and `generationmix` are nested **inside each
region**, not at the period level.

```json
{"data":[{"from":"2026-05-08T17:30Z","to":"2026-05-08T18:00Z","regions":[{"regionid":1,"dnoregion":"Scottish Hydro Electric Power Distribution","shortname":"North Scotland","intensity":{"forecast":0,"index":"very low"},"generationmix":[{"fuel":"biomass","perc":0},{"fuel":"coal","perc":0}]}]}]}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/neso/regional_intensity/year=<YYYY>/month=<MM>/regional_intensity_<YYYYMMDD>.parquet`
**Transformer class**: `gridflow.silver.neso.carbon_intensity.RegionalIntensityTransformer`
**Pydantic schema**: `gridflow.schemas.neso.RegionalIntensity`
**Dedup key**: `(timestamp_utc, regionid, shortname, postcode, fuel)`
**Point-in-time field**: `timestamp_utc`

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| timestamp_utc | datetime[UTC] | No | from | Half-hour period start. |
| period_end_utc | datetime[UTC] | Yes | to | Half-hour period end. |
| regionid | int | Yes | regionid | NESO region identifier. |
| dnoregion | str | No | dnoregion | DNO region name. |
| shortname | str | No | shortname | Short region label. |
| postcode | str | No | postcode | Outward postcode on the postcode routes; an empty string, not null, on every other route (`silver/neso/carbon_intensity.py:610-614`). |
| forecast_gco2_kwh | float | Yes | intensity.forecast | Regional forecast carbon intensity. |
| actual_gco2_kwh | float | Yes | intensity.actual | Regional responses carry no `actual` (see Known issues), so it is null on every regional row. |
| intensity_index | str | No | intensity.index | Docs category string. |
| fuel | str | No | generationmix.fuel | Regional generation mix fuel. |
| generation_percentage | float | Yes | generationmix.perc | Regional fuel share in percent. |
| data_provider | str | No | derived | Always neso. |
| ingested_at | datetime[UTC] | No | derived | Silver transform timestamp. |

### Silver sample

```python
[{"timestamp_utc":"2024-01-15T00:00:00+00:00","period_end_utc":"2024-01-15T00:30:00+00:00","regionid":13,"dnoregion":"UKPN London","shortname":"London","postcode":"","forecast_gco2_kwh":120.0,"actual_gco2_kwh":None,"intensity_index":"low","fuel":"gas","generation_percentage":30.0,"data_provider":"neso","ingested_at":"2026-05-04T00:00:00+00:00"},{"timestamp_utc":"2024-01-15T00:00:00+00:00","period_end_utc":"2024-01-15T00:30:00+00:00","regionid":13,"dnoregion":"UKPN London","shortname":"London","postcode":"","forecast_gco2_kwh":120.0,"actual_gco2_kwh":None,"intensity_index":"low","fuel":"wind","generation_percentage":40.0,"data_provider":"neso","ingested_at":"2026-05-04T00:00:00+00:00"}]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- Official docs use UTC timestamps ending in `Z`; keep joins in UTC.
- The connector sends no query parameters; all documented inputs are path parameters.
- Regional responses carry no `actual`: NESO's regional examples show `forecast` and `index` only, and no regional bronze body checked on 2026-10-06 had an `actual` key, so `actual_gco2_kwh` is null on every regional row.
- Window edges (observed 2026-10-06): `/regional/intensity/2026-09-13T00:00Z/2026-09-22T00:00Z` returned 433 half-hours, the first starting 12 Sep 23:30 UTC (its `to` equals `from`) and the last ending 22 Sep 00:00 (its `to` equals `to`). The connector files the whole window under its first day (`data_date=window_start.date()`, `connectors/neso/carbon_intensity.py:79`) and silver reads that date only, so `gridflow transform ... --start 2026-09-13 --end 2026-09-13` writes all nine days.
- Region 18 (GB) is not the national route's forecast (project check, 2026-10-06; NESO does not say how they relate): over the 674 half-hours shared with `neso/carbon_intensity`, regional GB `forecast_gco2_kwh` was within 17 gCO2/kWh of the national `actual_gco2_kwh` but up to 173 from the national `forecast_gco2_kwh`.
- For `intensity_period`, GB clock-change days can have 46 or 50 settlement periods in implementation even though official docs describe period 1-48.

---

## Implementation delta

- **`from` / `to` placeholders**: official docs and `config/sources.yaml` use `{from}` and `{to}`; `src/gridflow/connectors/neso/endpoints.py` uses `{from_dt}` and `{to_dt}` internally before formatting the same path.
- **`actual`**: official regional examples include `forecast` and `index`; code supports nullable `actual_gco2_kwh` if the API returns it.
- **Period-keyed shape vs silver row builder — RESOLVED in V2 (2026-05-09).** See [regional_current](./regional_current.md) for full notes. Silver `_rows_from_region_period` now reads from whichever level (region or period) holds the data. Live re-validated 2026-05-09 via `fix(V2-B):` on `claude/lucid-mccarthy-9ed3e0`.

---

## Changelog

- **2026-05-09 — V2-FIX-02.** Period-keyed silver now populates carbon and mix fields. See [regional_current](./regional_current.md#changelog) for evidence.
- **2026-05-08 — V1.** Live-validated; bug surfaced + documented.

---

## Modelling notes

Use regional `forecast_gco2_kwh` and fuel mix as local carbon features. Join to regional weather, demand, and postcode/region mapping before training; filter missing `regionid`/`postcode` intentionally.

---

## Links

- [Official API docs](https://carbon-intensity.github.io/api-definitions/)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/neso/carbon_intensity.py)
- [Endpoint metadata](../../../../../../Python/gridflow/src/gridflow/connectors/neso/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/neso/carbon_intensity.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/neso.py)
- [Gold view/builder](../../../../../../Python/gridflow/src/gridflow/gold/views/uk_imbalance_context.sql)
- [Domain: Carbon intensity](../../../20-domain/concepts/carbon-intensity.md)

