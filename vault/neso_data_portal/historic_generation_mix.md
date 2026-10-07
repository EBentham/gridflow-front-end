---
source: neso_data_portal
dataset_key: historic_generation_mix
vendor: "NESO Open Data Portal"
last_verified: 2026-09-25
layer_coverage: "bronze, silver"
page:
  title: GB generation mix by fuel
  summary: >-
    Great Britain's generation mix for every half-hour since 2009: MW by source, NESO's percentage
    shares and a carbon intensity, in one file.
  facts:
    vendor: NESO Data Portal, file Historic GB Generation Mix
    cadence: Half-hourly values; NESO's catalogue lists update frequency as hourly; the chart shows one capture
    grain: One row per half-hour and capture; the latest view keeps one
    history: From 1 January 2009, as NESO states
  landscape: power
  what_it_is: >-
    NESO's half-hourly GB generation mix: MW for eleven sources including embedded wind
    (`wind_emb`), their total and group totals, NESO's own percentage shares and a carbon
    intensity. NESO applies seasonal decomposition to correct missing or irregular points, and
    cleanses and republishes the whole history; gridflow keeps every capture. NESO currently
    counts batteries and transmission solar farms in `other`.
  how_used:
    - "Fuel-mix and carbon-intensity features since 2009; mind the November 2017 `biomass` and `other` switch."
    - "`wind_emb` and `solar` to set beside fuelhh's transmission-metered outturn, which lacks both."
    - "Vintage studies: how NESO's cleansing revises a half-hour between captures."
  chart:
    type: line
    silver: neso_data_portal/historic_generation_mix
    time: timestamp_utc
    value: solar
    dedup: {"on": [timestamp_utc], order_by: published_at}
    aggregation: mean
    time_bucket: 1d
    window: {start: "2009-01-01", end: "2026-09-25"}
    max_points: 6500
    unit: MW
  chart_view:
    title: Solar, daily mean, 2009 to September 2026
    caption: >-
      Silver `neso_data_portal/historic_generation_mix`, `solar` in MW: the mean of each UTC day's
      48 half-hours, 1 January 2009 to 25 September 2026, all from the capture NESO last modified
      on 26 September 2026. The file carries zero before 2013.
    alt: >-
      Line chart of daily mean solar from neso_data_portal/historic_generation_mix, in MW, for
      every UTC day from 1 January 2009 to 25 September 2026. The line sits at zero through 2012,
      starts on 1 January 2013, then rises and falls with the seasons. Summer peaks: about 600 MW
      in 2013, 2,000 MW in 2015, 3,200 to 3,500 MW in 2017 to 2022, 3,900 to 4,900 MW in 2023 to
      2025, and 5,444 MW on 12 July 2026. Winter lows stay below 160 MW. The last day shown is
      about 2,400 MW.
    x_label: UTC day, 2009 to 2026
    key:
      - {series: solar, label: Solar, codes: SOLAR, note: "Excludes transmission-connected solar farms, which NESO currently counts in OTHER."}
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show` finds the file by exact name, then gridflow downloads
      the whole CSV. Dates select nothing; silver keeps every capture.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=historic-generation-mix"
      - "GET https://api.neso.energy/dataset/88313ae5-94e4-4ddc-a790-593554d8c6b9/resource/f93d1835-75bc-43e5-84ad-12472b180a98/download/df_fuel_ckan.csv"
    commands:
      - {run: gridflow ingest neso_data_portal historic_generation_mix --last 24h, comment: "whole file; window must end recently"}
      - {run: gridflow transform neso_data_portal historic_generation_mix --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: timestamp_utc, op: ge, value: "2026-09-05T11:00:00+00:00"}
        - {column: timestamp_utc, op: le, value: "2026-09-05T12:30:00+00:00"}
      order_by: [timestamp_utc, published_at]
      columns: [timestamp_utc, published_at, solar, imports, carbon_intensity, generation, wind, wind_emb, gas]
    key: [timestamp_utc, published_at]
    caption: "Four half-hours of 5 September 2026 in two captures: NESO revised `solar`, `imports` and `carbon_intensity`."
    fields:
      timestamp_utc: "Half-hour start, UTC: NESO states UTC; start checked against fuelhh, 2021 to 2026"
      published_at: "NESO's last-modified time for the whole file, read as UTC; one per capture"
      solar: Solar, MW; transmission-connected solar farms currently sit in `other` (NESO)
      imports: Each link's imports summed, MW; exports are not netted off (checked against fuelhh)
      carbon_intensity: CO2 per kWh consumed, as NESO describes it; the file states no unit
      generation: "Total, MW: NESO's sum of the eleven source columns"
      wind: Wind, MW, without embedded wind, which `wind_emb` carries
      wind_emb: Embedded wind, MW; NESO titles it Wind EMB and gives no description
      gas: Gas, MW
      coal: Coal, MW
      nuclear: Nuclear, MW
      hydro: Hydro, MW
      biomass: Biomass, MW; zero until 1 Nov 2017, when `other` drops by about as much
      other: Other, MW; currently includes batteries, transmission solar (NESO); drops as `biomass` starts (last cell)
      storage: Pumped storage, net, MW; NESO curtails negative values at zero
      low_carbon: "Low-carbon total, MW; includes `storage` and `wind_emb`, which NESO's examples omit (checked)"
      zero_carbon: "Zero-carbon total, MW; undocumented: well below NESO's examples (wind, solar, hydro, nuclear) here"
      renewable: "Renewable total, MW; includes `storage` and `wind_emb`, which NESO's examples omit (checked)"
      fossil: "Fossil total, MW; NESO's examples: coal, natural gas"
      gas_pct: "Gas share, percent; NESO names no denominator: gas over `generation` matches (checked)"
      coal_pct: Coal share, percent; matches coal over `generation` (checked)
      nuclear_pct: Nuclear share, percent; matches nuclear over `generation` (checked)
      wind_pct: Wind share, percent; matches wind over `generation` (checked)
      wind_emb_pct: Embedded wind share, percent; matches `wind_emb` over `generation` (checked)
      hydro_pct: Hydro share, percent; matches hydro over `generation` (checked)
      imports_pct: Imports share, percent; matches imports over `generation` (checked)
      biomass_pct: Biomass share, percent; matches biomass over `generation` (checked)
      other_pct: Other share, percent; matches other over `generation` (checked)
      solar_pct: Solar share, percent; matches solar over `generation` (checked)
      storage_pct: Pumped storage share, percent; matches storage over `generation` (checked)
      generation_pct: "NESO's percentage for `generation` itself; 100 in these rows"
      low_carbon_pct: Low-carbon share, percent; matches `low_carbon` over `generation` (checked)
      zero_carbon_pct: "NESO's zero-carbon percentage, undocumented; in these rows not `zero_carbon` over `generation`, above `low_carbon_pct`"
      renewable_pct: Renewable share, percent; matches `renewable` over `generation` (checked)
      fossil_pct: Fossil share, percent; matches `fossil` over `generation` (checked)
  notebook:
    lead: >-
      Returns a pandas DataFrame from the DuckDB view
      `silver_neso_data_portal_historic_generation_mix_latest`, the newest capture's row per
      half-hour, for whole UTC days on `timestamp_utc`, both dates included. Times print in local
      time; lineage columns dropped.
    cells:
      - |
        df = data.neso_data_portal.query("historic_generation_mix", "2026-09-19", "2026-09-25")
        df = df.sort_values("timestamp_utc")
      - df.nlargest(5, "solar")[["timestamp_utc", "solar", "wind", "wind_emb", "gas", "generation"]]
      - |
        colours = {"nuclear": "#7B5EA7", "biomass": "#8C6D31", "hydro": "#1F77B4",
                   "coal": "#333333", "gas": "#E07B39", "other": "#BDB76B",
                   "storage": "#17BECF", "imports": "#999999", "wind": "#3E8C97",
                   "wind_emb": "#9ED0D6", "solar": "#F2C14E"}
        ax = df.plot.area(x="timestamp_utc", y=list(colours), color=colours,
                          ylabel="MW", linewidth=0, figsize=(8, 3.5))
        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5), fontsize=8);
      - |
        m = data.neso_data_portal.query("historic_generation_mix", "2009-01-01", "2017-11-01")
        m["biomass_plus_other"] = m.biomass + m.other
        print("biomass max before 20:00 UTC, 1 Nov 2017:",
              m[m.timestamp_utc < "2017-11-01 20:00Z"].biomass.max())
        switch = m.timestamp_utc.between("2017-11-01 18:30Z", "2017-11-01 21:00Z")
        m[switch][["timestamp_utc", "biomass", "other", "biomass_plus_other"]]
    needs: one current capture of the file
    plot_alt: >-
      Stacked area plot of the eleven MW columns, 19 to 25 September 2026, nuclear at the bottom
      and solar on top. The total runs from about 22,700 to 38,300 MW. Wind dominates the 19th
      and 20th, gas the 21st and 22nd, and solar adds a midday band every day, peaking at
      13,127 MW on the 20th.
  related:
    - {dataset: elexon/fuelhh, note: "Transmission-metered outturn by fuel, with no solar code"}
    - {dataset: neso_data_portal/embedded_wind_solar_forecast, note: "NESO's forecast of embedded wind and solar, by settlement period"}
    - {dataset: elexon/indo, note: "Demand outturn that NESO says excludes almost all solar"}
    - {dataset: neso/carbon_intensity, note: "NESO's national carbon intensity, from its separate API"}
---

# NESO Data Portal — Historic GB Generation Mix

## Overview

Half-hourly GB generation mix from 2009: MW per fuel (gas, coal, nuclear,
wind, embedded wind, hydro, imports, biomass, solar, storage, other), total
generation, carbon intensity, and NESO's own percentage shares. The longest
half-hourly fuel-mix history in the stack — a training backbone for
carbon-intensity and fuel-switching models. It also reaches what Elexon
`fuelhh` structurally cannot: `fuelhh` is transmission-only, while `wind_emb`
here includes embedded wind. NESO cleanses and republishes the **whole
history**, so two captures can legitimately disagree about the same
half-hour — vintages matter.

→ [Settlement period](../../../20-domain/concepts/settlement-period.md)

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://api.neso.energy/api/3/action/` |
| Path             | `package_show?id=historic-generation-mix` → resource URL from `resources[]`, then file download (302 → presigned CDN URL) |
| Method           | GET |
| Auth             | None — keyless public API (verified 2026-08-16) |
| Rate limit       | Vendor guidance: max 1 request/second (CKAN actions); IP-block enforcement. Connector throttles every send |
| Pagination       | None; single file download (~60 MB class — the large-file path is tested to a 1.5 GB memory budget, observed peak 180 MiB for a 60 MiB body) |
| Historical depth | 2009 onwards. Vendor: package notes "This dataset contains data from 1 January 2009"; resource description "from the 1st of Jan 2009 through to today" (gridflow `.planning/phases/neso-data-portal/_probe/show_historic-generation-mix.json`) |
| Publication lag  | Lag not stated by NESO. The package `extras` list `Update Frequency: Hourly` (CKAN `extras`; `_probe/show_historic-generation-mix.json`, and the 20 Aug 2026 catalogue snapshot under `_generated/`). That is NESO's label, not an observed cadence: the three captures held show `ckan_last_modified` 20 minutes, 14.6 hours and 9 minutes before `fetched_at`. `ckan_last_modified` carries the vendor instant |
| Response format  | JSON (CKAN metadata envelope) → CSV (the data file) |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `id` | string | Yes | CKAN package (dataset) slug | `historic-generation-mix` |

Resource selected by **exact `resources[].name == "Historic GB Generation
Mix"`** (D-03), format `CSV`, URL re-resolved from `package_show` at every
fetch (D-06). Download size cap for this dataset: 256 MiB.

### Working curl example

```bash
# Keyless — no auth header:
curl -X GET \
  "https://api.neso.energy/api/3/action/package_show?id=historic-generation-mix"
```

---

## Bronze layer

**Path pattern**: `data/bronze/neso_data_portal/historic_generation_mix/<year>/<month>/<day>/raw_<fetched_at>_<uuid>.csv`
**Format**: Raw CSV, as-received. Immutable. `<stem>.meta.json` sidecar carries fetch provenance.
**Granularity**: One file per capture — the whole 2009-to-now history each time; partition is the ingest window's end date (D-13)

### Bronze sample

```csv
DATETIME,GAS,COAL,NUCLEAR,WIND,WIND_EMB,HYDRO,IMPORTS,BIOMASS,OTHER,SOLAR,STORAGE,GENERATION,CARBON_INTENSITY,LOW_CARBON,ZERO_CARBON,RENEWABLE,FOSSIL,GAS_perc,COAL_perc,NUCLEAR_perc,WIND_perc,WIND_EMB_perc,HYDRO_perc,IMPORTS_perc,BIOMASS_perc,OTHER_perc,SOLAR_perc,STORAGE_perc,GENERATION_perc,LOW_CARBON_perc,ZERO_CARBON_perc,RENEWABLE_perc,FOSSIL_perc
2009-06-01T05:00:00,12345,8000,6500,500,0,300,1000,0,200,0,0,28845,480,7300,7300,800,20345,42.8,27.7,22.5,1.7,0.0,1.0,3.5,0.0,0.7,0.0,0.0,100.0,25.3,25.3,2.8,70.5
2009-06-01T05:30:00,12400,7950,6500,520,0,310,1000,0,200,0,0,28880,478,7330,7330,830,20350,42.9,27.5,22.5,1.8,0.0,1.1,3.5,0.0,0.7,0.0,0.0,100.0,25.4,25.4,2.9,70.4
```

(Header is contract-exact — **34 columns**, counted from the Stage-A capture
`_probe/sample_historic-generation-mix.csv`; the plan said 37 until the
rev-14 erratum corrected it from the file. Values above are illustrative of
shape, not real records — see the fixture for real captured rows.)

---

## Silver layer

**Path pattern**: `data/silver/neso_data_portal/historic_generation_mix/<year>/<month>/<day>/data_<run_suffix>.parquet` (APPEND_ONLY — one file per vintage)
**Transformer class**: `gridflow.silver.neso_data_portal.historic_generation_mix.HistoricGenerationMixTransformer`
**Pydantic schema**: `gridflow.schemas.neso_data_portal.NesoHistoricGenerationMix`
**Dedup key**: `(timestamp_utc, published_at)` — the publication instant is in the key unconditionally because NESO republishes cleansed history and two captures may disagree about one half-hour (D-21/D-24)
**Point-in-time field**: `published_at` (`ckan_last_modified` via D-23; `available_at == published_at`, D-22)

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `timestamp_utc` | `datetime[UTC]` | No | `DATETIME` | Vendor's offset-naive stamp read **as UTC**. That reading is documented, not inferred: the UTC statement exists only in the `datastore_search` field metadata (`_probe/datastore_historic-generation-mix.json`, `DATETIME.info.description`), which a plain CSV download never exposes. A `DATETIME` that *does* carry an offset raises rather than being silently reinterpreted (vendor-drift guard, checked on the raw Utf8 before any cast) |
| `gas` … `fossil` (17 MW/index fields) | `float` | No | `GAS` … `FOSSIL` | MW per fuel; `generation` is the total; `carbon_intensity` carries no unit in NESO's field metadata (described as CO2 "per kilowatt hour of electricity consumed"; values fit gCO2/kWh, unconfirmed; `_probe/datastore_historic-generation-mix.json`); strict Float64 casts |
| `gas_pct` … `fossil_pct` (16 fields) | `float` | No | `GAS_perc` … `FOSSIL_perc` | NESO's **own** published percentages, carried not recomputed — a recomputation would disagree at NESO's rounding; the vendor's number is what reconciles against the portal |
| `published_at` | `datetime[UTC]` | No | sidecar `ckan_last_modified` | Required; a body without it is declined (D-23/FM-05) |
| `data_provider` | `str` | No | derived | Constant `neso_data_portal` |

(Full field list: `gas, coal, nuclear, wind, wind_emb, hydro, imports,
biomass, other, solar, storage, generation, carbon_intensity, low_carbon,
zero_carbon, renewable, fossil` + the 16 `_pct` counterparts — 33 numeric
columns mapping the 34-column vendor header minus `DATETIME`.)

### Silver sample

```python
[
    {
        "timestamp_utc": datetime(2009, 6, 1, 5, 0, tzinfo=timezone.utc),
        "gas": 12345.0, "coal": 8000.0, "nuclear": 6500.0, "wind": 500.0,
        "wind_emb": 0.0, "hydro": 300.0, "imports": 1000.0, "biomass": 0.0,
        "other": 200.0, "solar": 0.0, "storage": 0.0, "generation": 28845.0,
        "carbon_intensity": 480.0, "low_carbon": 7300.0, "zero_carbon": 7300.0,
        "renewable": 800.0, "fossil": 20345.0,
        "gas_pct": 42.8, "coal_pct": 27.7, "nuclear_pct": 22.5,
        "wind_pct": 1.7, "wind_emb_pct": 0.0, "hydro_pct": 1.0,
        "imports_pct": 3.5, "biomass_pct": 0.0, "other_pct": 0.7,
        "solar_pct": 0.0, "storage_pct": 0.0, "generation_pct": 100.0,
        "low_carbon_pct": 25.3, "zero_carbon_pct": 25.3,
        "renewable_pct": 2.8, "fossil_pct": 70.5,
        "published_at": datetime(2026, 8, 16, 18, 20, 11, tzinfo=timezone.utc),
        "data_provider": "neso_data_portal",
    },
]
```

---

## Gold layer

None implemented. Consumer surface:
`silver_neso_data_portal_historic_generation_mix` (all vintages) and
`silver_neso_data_portal_historic_generation_mix_latest` (one winning row per
`timestamp_utc`) — `_latest` is the consumer default (D-30).

---

## Known issues and gotchas

- **Whole-history republication**: every capture re-delivers 2009-to-now, so
  the base view multiplies with each capture. Consume `_latest`. The
  vintage axis is real signal (NESO cleanses history), not noise.
- **Naive `DATETIME` is UTC by metadata only** — the CSV itself never says
  so. The transformer refuses offset-carrying values so a future vendor
  format change surfaces loudly instead of shifting the series by an hour.
- **Cross-checked against Elexon**: the settlement-convention test asserts
  the embedded-forecast dataset derives the same UTC instants as `elexon/fuelhh` through the
  shared `settlement_period_to_utc`; a non-binding corroboration pins
  NESO's `TIME_GMT` (on the embedded-forecast dataset) as period-END.
  Neither test covers this dataset (`tests/integration/test_neso_data_portal_mocked_e2e.py:633-735`
  run on `embedded_wind_solar_forecast`): here `timestamp_utc` is the vendor `DATETIME`, never
  derived from a settlement pair. A magnitude cross-check against local fuelhh silver skips under pytest by
  conftest design (the data-dir env var is cleared in tests).
  *Measured 2026-10-06 (v5 page author), 26 Sep 2026 capture vs fuelhh latest, 1 Jun to 26 Sep 2026:*
  at zero lag `wind` equals fuelhh `WIND` on 98.5% of half-hours and `nuclear` equals `NUCLEAR` on
  96.7%; `hydro` equals `NPSHYD` and `storage` equals `PS` floored at zero on every one. A 30-minute
  shift either way raises every mean absolute difference (wind 15 MW to about 239 MW). So
  `DATETIME` is the **start** of the half-hour, as fuelhh stamps it; NESO states only UTC.
  `imports` tracks the sum of fuelhh's **positive** interconnector flows, each link floored at zero
  (mean absolute difference 36 MW), not the net of all links floored at zero (1,369 MW): exports
  on one link do not offset imports on another.
- **No backfill** (D-35) and **D-13 partition-on-window-end** — same
  operator guidance and residuals as the other two datasets: prefer
  `gridflow pipeline`; transform over a window covering the ingest window's
  end date.
- **FM-15 completeness limit**: vintages are only as dense as the capture
  cadence.
- **Large file**: ~60 MB class today and growing; the 256 MiB download cap
  and the tested memory budget (1.5 GB, observed 180 MiB peak) cover it.
  D-19's `schema_overrides` escape hatch exists if the budget is ever hit —
  not needed to date.
- Skipped/unusable bodies → `completed_with_warnings` / all-declined →
  `failed` (D-41, ADR-030).
- **Vendor package notes** (`_probe/show_historic-generation-mix.json`): "seasonal decomposition
  applied to correct missing or irregular data points"; "Pumped Storage units (NET) are
  represented in the STORAGE category"; "All Net-Negative values are curtailed at zero". In the
  26 Sep 2026 capture `imports` and `storage` are never below zero.
- **Grid and keys (measured 2026-10-06, three captures: published 2026-08-20, 2026-09-05,
  2026-09-26):** each capture is a complete UTC half-hour grid from 2009-01-01 00:00 to its last
  stamp, no gaps or duplicates, and the bronze CSVs carry no duplicate `DATETIME`, so the
  transformer's `unique(keep="last")` drops nothing. Between the 5 Sep and 26 Sep captures,
  1,172 half-hours changed, all in 2026 (12 Jun to 5 Sep); `solar` changed only on 5 Sep (the
  older capture's last day), by up to 721 MW.
- **Derived columns (measured, 26 Sep 2026 capture; NESO's descriptions say "e.g.")**:
  `generation` equals the sum of the 11 source columns within 3 MW. `low_carbon` = nuclear + wind +
  wind_emb + hydro + biomass + solar + storage, and `renewable` = wind + wind_emb + hydro + solar +
  storage, both within 2 MW: **storage counts as renewable and low-carbon**, which the descriptions do
  not say. `fossil` = gas + coal. `zero_carbon` matches nuclear + wind + hydro + biomass + storage
  within 1 MW in every year 2009 to 2022 (so it **includes biomass and omits `wind_emb` and `solar`**, against its
  description "wind, solar, hydro, nuclear"); from 2023-01-01 08:30 UTC it fits no fixed sum (up to 1,441 MW off). Every
  `_pct` column equals its MW column over `generation` within 0.06 points **except
  `zero_carbon_pct`**, which exceeds `low_carbon_pct` on 204,578 of 310,931 rows (88 to 92% at
  midday on 5 Sep 2026, when `zero_carbon / generation` is 40 to 46%). Treat both zero-carbon
  columns as undocumented.

- **`solar` composition against INDO (primary-source citations, gridflow_models v2.2 G-1, 2026-09-25, #865).** Full
  chain, quote index and archive: `gridflow_models/.planning/phases/v2.2-G-1-g5-closure/G5-CLOSURE.md`. Raw bytes are
  under `C:/gridflow-data/receipts/v2.2-G-1/sources/`, with shas in `SOURCES-INDEX.json`.
  - *Vendor:* "Transmission-connected solar farms are currently included in the OTHER category" and "Batteries (NET
    discharge) are currently included in the OTHER category" (this page, retrieved 2026-09-25). NESO: "Updates will be
    released later in 2026, to highlight BESS … and Transmission Solar values", so **pin the vintage** before relying on
    the split.
  - *Vendor (NESO Carbon Intensity methodology, May 2024):* "Estimated data is used for embedded wind and solar
    generation". NESO OTF (Feb 2026): "Sheffield Solar currently provide the estimated actuals for embedded Solar PV in
    GB". PV_Live excludes "Solar BMUs … PV sites that NESO meters directly".
  - *Deduction, not a vendor statement:* `solar` is NESO's estimated embedded solar and holds no BMU-metered solar. It
    links to this dataset **only by its title and portal section**. No statement names this column's input or
    post-dates Feb 2026. **TODO:** the source identity per vintage, and whether any NETSO-metered non-BMU embedded solar
    sits inside `solar`.
  - *Consequence for INDO users:* NESO says INDO "excludes … almost all solar installations" (NESO OTF, 22 Jan 2025). So
    `INDO − solar` likely subtracts embedded solar twice. The formula ruling is OWNER's (O-1, `G5-NEEDS-BOBBO.md`).

---

## Implementation delta

- **Column count**: plan prose said **37** columns through rev 13; the
  Stage-A capture has **34**. Corrected by rev-14 erratum, counted from the
  file — the file is the authority (D-24). No live disagreement observed.

---

## Modelling notes

TODO. Intended use: carbon-intensity forecasting targets and features
(`carbon_intensity` as target, fuel MW/shares as features); fuel-switching
studies (gas-vs-coal margins); `wind_emb` as the embedded-generation
complement to Elexon's transmission-only view; long-history seasonal
baselines from 2009. Filter guidance: use `_latest`; treat structural
zeros as not missing: in the 26 Sep 2026 capture `solar` is zero in every half-hour before
2013-01-01 and `biomass` before 2017-11-01 (measured 2026-10-06; NESO gives no reason).
`other` is zero before 2012-02-01 16:30 UTC, and its monthly mean falls from 932 MW (Oct 2017) to
134 MW (Nov 2017) as `biomass` rises from 0 to 1,491 MW. `biomass` is 0 on all 154,848
half-hours before 2017-11-01 20:00 UTC. At the switch, `biomass + other` runs on: 1,462 MW at
19:30 UTC, 1,464 MW at 20:30 UTC (the 20:00 half-hour counts both, 2,595 MW). That suggests
biomass sat inside `other` before then; NESO does not say so. Neither column is one series across
that half-hour.

---

## Links

- [Official API docs](https://api.neso.energy/api/3/action/package_show?id=historic-generation-mix)
- [Connector source](../../../../../Python/gridflow/src/gridflow/connectors/neso_data_portal/client.py)
- [Silver transformer](../../../../../Python/gridflow/src/gridflow/silver/neso_data_portal/historic_generation_mix.py)
- [Pydantic schema](../../../../../Python/gridflow/src/gridflow/schemas/neso_data_portal.py)
- Gold view/builder: none
- [Domain: settlement period](../../../20-domain/concepts/settlement-period.md)
