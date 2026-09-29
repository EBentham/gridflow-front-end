---
source: gie_agsi
dataset_key: storage
vendor: GIE AGSI+ (Gas Storage)
last_verified: 2026-07-25
layer_coverage: bronze, silver, gold
page:
  title: Underground gas storage, countries and EU
  summary: >-
    GIE AGSI+ daily underground gas storage reports: stock, injection, withdrawal and percent full,
    for nine countries and the EU aggregate.
  facts:
    vendor: GIE AGSI+, the `/api` storage report
    cadence: Daily, one report per gas day, as sent in the responses we hold
    grain: "`storage`: gas day and country; `storage_reports`: gas day, EU aggregate"
  landscape: gas
  what_it_is: >-
    Gas Infrastructure Europe's AGSI+ daily storage report. `storage` asks for nine countries by
    `country`, one call per country and gas day; `storage_reports` asks for the EU aggregate. Rows
    carry gas in storage, working gas volume, percent full, injection and withdrawal. Stock columns
    are TWh despite `_gwh` names, by our check against the flows and ENTSOG; compare countries by
    `storage_pct_full`.
  how_used:
    - Country fill levels as features for a winter gas-balance or storage-spread model.
    - Daily net injection by country from `net_withdrawal_gwh`, negative while injecting.
    - "The EU fill from `storage_reports`: never a sum of the country rows."
  chart:
    type: line
    silver: gie_agsi/storage
    time: gas_day
    value: storage_pct_full
    filter:
      - {column: entity_code, op: in, value: [DE, IT, NL, FR, AT]}
    group: entity_code
    group_map:
      IT: it
      FR: fr
      AT: at
      DE: de
      NL: nl
    series_order: [it, fr, at, de, nl]
    aggregation: last
    window: {start: "2026-09-13", end: "2026-09-22"}
    unit: "%"
  chart_view:
    title: Storage fill by country, 13 to 22 September 2026
    caption: >-
      Silver `gie_agsi/storage`, `storage_pct_full` in percent, one value per country and gas day,
      13 to 22 September 2026. The five countries with the largest working gas volume; BE, ES and
      PL are left out and GB sends placeholders, no storage values.
    alt: >-
      Line chart of storage percent full from gie_agsi/storage, one line per country, for gas days
      13 to 22 September 2026. Italy rises from 84.66 to 86.03%, France from 76.74 to 81.09%,
      Austria from 67.1 to 67.87% on the 21st, ending at 67.81%, Germany from 55.81 to 56.99% and
      the Netherlands from 52.55 to 56.26%. No two lines cross.
    x_label: gas day, AGSI's gasDayStart date
    key:
      - {series: it, label: Italy, codes: IT, paint: horizon}
      - {series: fr, label: France, codes: FR, paint: olive}
      - {series: at, label: Austria, codes: AT, paint: hatch-lines}
      - {series: de, label: Germany, codes: DE, paint: petrol}
      - {series: nl, label: Netherlands, codes: NL, paint: clay}
  raw_feed:
    note: >-
      One GET per country and gas day on AGSI+ `/api`, key in the `x-key` header. `gridflow ingest`
      files each response in bronze by gas day; `gridflow transform` types it.
    requests:
      - "GET https://agsi.gie.eu/api?country=DE&date=2026-09-22&page=1&size=300"
    commands:
      - {run: gridflow ingest gie_agsi storage --start 2026-09-13 --end 2026-09-22, comment: "bronze; the end day is fetched"}
      - {run: gridflow transform gie_agsi storage --start 2026-09-13 --end 2026-09-22, comment: bronze to silver}
  record:
    select:
      filter:
        - {column: gas_day, op: eq, value: "2026-09-22"}
        - {column: entity_code, op: in, value: [AT, DE, ES, FR, GB, IT, NL, PL]}
      order_by: [entity_code]
      columns: [entity_code, storage_pct_full, gas_in_storage_gwh, working_gas_volume_gwh, net_withdrawal_gwh, injection_gwh, withdrawal_gwh, status, gas_day, updated_at]
    key: [gas_day, entity_level, entity_code, entity_url]
    caption: "Gas day 22 September 2026: eight of the nine countries, BE left out."
    fields:
      entity_code: "Country code, the vendor's `code`; one of gridflow's nine"
      storage_pct_full: "Vendor `full`, percent; equals gas in storage over working gas volume here"
      gas_in_storage_gwh: "Vendor `gasInStorage`; TWh despite the name, by our check against the flows"
      working_gas_volume_gwh: "Vendor `workingGasVolume`; TWh by our check, like gas in storage"
      net_withdrawal_gwh: "Vendor `netWithdrawal`, GWh; within 0.1 of withdrawal minus injection here"
      injection_gwh: "Vendor `injection`, GWh in the gas day"
      withdrawal_gwh: "Vendor `withdrawal`, GWh in the gas day"
      status: "Vendor `status` letter: `C` or `E` here, and `N` on GB's empty row"
      gas_day: "AGSI's `gasDayStart` date; `event_time` gets a fixed 06:00 UTC project label, not the start"
      updated_at: "Vendor `updatedAt`, a zoneless stamp the transformer reads as UTC"
      gas_day_end: "Vendor `gasDayEnd` date, the next day, stored at 00:00 UTC"
      entity_level: "`country` on every row: the connector asks by country only"
      entity_name: "Vendor `name`; GB comes as United Kingdom (Pre-Brexit)"
      entity_url: "Vendor `url`, the country code again"
      country_code: "The requested country, equal to `entity_code` here"
      country_name: "Equal to `entity_name` on these country rows"
      consumption_gwh: "Vendor `consumption`, TWh like gas in storage by our check; period undocumented"
      consumption_full_pct: "Vendor `consumptionFull`; matches gas in storage over `consumption_gwh`, in percent; GB sends 0"
      injection_capacity_gwh_per_day: "Vendor `injectionCapacity`, named GWh per day"
      withdrawal_capacity_gwh_per_day: "Vendor `withdrawalCapacity`, named GWh per day"
      contracted_capacity_gwh_per_day: "Vendor `contractedCapacity`; named per day, but a TWh volume by our check"
      available_capacity_gwh_per_day: "Vendor `availableCapacity`; named per day, but a TWh volume by our check"
      covered_capacity_gwh_per_day: "Vendor `coveredCapacity`: 100 on every row here but GB's; meaning undocumented"
      trend: "Vendor `trend`; tracks the day's change in `storage_pct_full`"
      info: "Vendor `info` list as JSON text: `[]` in these rows"
  notebook:
    lead: >-
      Returns a pandas DataFrame from `silver_gie_agsi_storage`, filtered on `gas_day` with both
      ends included; lineage columns dropped. The pivot gives one column per country.
    source: gie_agsi
    cells:
      - df = data.gie_agsi.query("storage", "2026-09-13", "2026-09-22")
      - df[["gas_day", "entity_code", "storage_pct_full", "net_withdrawal_gwh"]].head()
      - |
        net = df.pivot(index="gas_day", columns="entity_code", values="net_withdrawal_gwh")
        colors = ["#155A6E", "#66793B", "#C77E3C"]
        ax = net[["DE", "FR", "NL"]].plot(ylabel="net withdrawal, GWh", figsize=(8, 3.5), color=colors)
        ax.legend(loc="upper left");
    needs: gas days 13 to 22 September 2026
    plot_alt: >-
      Line plot of net_withdrawal_gwh against gas_day for DE, FR and NL, gas days 13 to 22
      September 2026, every point below zero. France falls to -759.2 GWh on the 20th; Germany swings
      from -71.7 on the 15th to -711.1 on the 19th and ends at -1.0; the Netherlands ends at -429.5.
  related:
    - {dataset: gie/unavailability, note: Outage reports for the storage behind these figures}
    - {dataset: gie/about_listing, note: "The company and facility register for AGSI's lower levels"}
    - {dataset: gie/lng, note: LNG send-out feeds the same national gas balances as storage}
    - {dataset: entsog/physical_flows, note: "Pipeline flows at interconnection points, also per gas day"}
  family:
    slug: agsi-storage
    members:
      - dataset: storage
        differs: "Nine countries, one row each per gas day; GB's storage values are null"
        request: "GET https://agsi.gie.eu/api?country=DE&date=2026-09-22&page=1&size=300"
      - dataset: storage_reports
        differs: "EU aggregate only (`type=EU`): one row per gas day, not a country sum"
        request: "GET https://agsi.gie.eu/api?type=EU&date=2026-09-22&page=1&size=300"
---

# GIE AGSI+ — Storage (country-level gas storage)

## Overview

`storage` is the country-scoped form of the AGSI gas-storage time-series.
Same `/api` endpoint and response shape as `storage_reports`, but the
connector exercises **only** the `country` query scope — one record per
gas-day per country in gridflow's own country list (`AGSI_COUNTRIES`:
`AT, BE, DE, ES, FR, GB, IT, NL, PL`; `connectors/gie/endpoints.py:14`). Stocks (`gasInStorage`), flow components (`injection`,
`withdrawal`, `netWithdrawal`), capacity figures (`workingGasVolume`,
`injectionCapacity`, `withdrawalCapacity`), percent-full and trend.

The dataset answers: "How full is each EU country's underground storage
today, and how is it changing?" — the workhorse country-level view used
in winter-tightness models, fuel-switching signals, and storage-spread
trades.

→ [Gas day](../../../20-domain/concepts/gas-day.md) — `gas_day` is the
  vendor's `gasDayStart` date; gridflow labels its `event_time` at a fixed
  06:00 UTC (`silver/base.py:383-400`), a project convention, not the
  vendor's start instant.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://agsi.gie.eu` |
| Path             | `/api` |
| Method           | GET |
| Auth             | header `x-key` (lowercase), key from env `GIE_API_KEY` |
| Rate limit       | 60 calls/minute (vendor-published). Connector throttles to 1 req/s. |
| Pagination       | `last_page` is the source of truth; `total` is the per-page row count. Iterate `page=1..last_page`. |
| Historical depth | 2011-01-01 (per facility records in `about?show=listing`) |
| Publication lag  | Daily, ~16:00 CET refresh. `updatedAt` field per record. |
| Response format  | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `country` | str | Yes | ISO-2 country code from the AGSI footprint. | `country=GB` |
| `date` | str (YYYY-MM-DD) | Conditional | Single gas day. Mutually exclusive with `from`/`to`. | `date=2026-05-06` |
| `from` | str (YYYY-MM-DD) | Conditional | Range start gas day. | `from=2026-05-01` |
| `to` | str (YYYY-MM-DD) | Conditional | Range end gas day (inclusive). | `to=2026-05-07` |
| `page` | int | No | Page number, 1-indexed. Default 1. | `page=2` |
| `size` | int | No | Page size. Default 30, max 300. Connector uses 300. | `size=300` |

### Working curl example

```bash
# Replace <KEY> with $GIE_API_KEY
curl --ssl-no-revoke -X GET \
  "https://agsi.gie.eu/api?country=GB&date=2026-05-06" \
  -H "x-key: <KEY>"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/gie_agsi/storage/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per (country, gas day) call after pagination is unrolled.

### Bronze sample

```json
{
  "last_page": 1,
  "total": 1,
  "dataset": "<a href=\"/historical/GB\">United Kingdom (Pre-Brexit)</a>",
  "gas_day": "2026-05-06",
  "data": [
    {
      "name": "United Kingdom (Pre-Brexit)",
      "code": "GB",
      "url": "GB",
      "updatedAt": "2026-05-08 17:36:56",
      "gasDayStart": "2026-05-06",
      "gasDayEnd": "2026-05-07",
      "gasInStorage": "-",
      "consumption": "-",
      "consumptionFull": "0",
      "injection": "-",
      "withdrawal": "-",
      "netWithdrawal": "-",
      "workingGasVolume": "-",
      "status": "N",
      "trend": "-",
      "full": "-",
      "info": []
    }
  ]
}
```

DE returns numeric values:

```json
{
  "name": "Germany", "code": "DE", "gasInStorage": "65.9608",
  "full": "26.62", "trend": "-0.57", "status": "E"
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/gie_agsi/storage/year=YYYY/month=MM/storage_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.gie.agsi.GasStorageTransformer`
**Pydantic schema**: `gridflow.schemas.gie.GasStorage`
**Dedup key**: `(gas_day, entity_level, entity_code, entity_url)`
**Point-in-time field**: `updated_at` — vendor `updatedAt`. Use for as-of filtering.

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `gas_day` | `date` | No | `gasDayStart` | Required. `event_time` labels it at a fixed 06:00 UTC (`silver/base.py:383-400`). |
| `gas_day_end` | `datetime[UTC]` | Yes | `gasDayEnd` | Vendor date (the next day) stored at 00:00 UTC (`silver/gie/agsi.py:56-57,193`). |
| `updated_at` | `datetime[UTC]` | Yes | `updatedAt` | Vendor stamp sent without a zone; the transformer reads it as UTC (`silver/gie/agsi.py:48-62`). |
| `entity_level` | `str` | No | derived | Always `country` for this dataset. |
| `entity_code` | `str` | No | request `country` / `code` | ISO-2 country code. |
| `entity_name` | `str` | No | `name` | Human-readable country name. |
| `entity_url` | `str` | Yes | `url` | |
| `country_code` | `str` | No | request `country` | |
| `country_name` | `str` | No | `name` | |
| `gas_in_storage_gwh` | `float` | Yes | `gasInStorage` | TWh despite the name (our check, 2026-09-29): its day-on-day change x 1,000 matches `injection` - `withdrawal`, and those flows are GWh/d (see Known issues). `-` placeholder → null. |
| `consumption_gwh` | `float` | Yes | `consumption` | TWh, like `gas_in_storage_gwh` (`consumption_full_pct` = stock / consumption x 100); period undocumented. |
| `consumption_full_pct` | `float` | Yes | `consumptionFull` | %. GB rows send `0` with every other value null. |
| `injection_gwh` | `float` | Yes | `injection` | GWh. |
| `withdrawal_gwh` | `float` | Yes | `withdrawal` | GWh. |
| `net_withdrawal_gwh` | `float` | Yes | `netWithdrawal` | GWh. Signed: within 0.1 of `withdrawal` - `injection` (checked), negative while injecting. |
| `working_gas_volume_gwh` | `float` | Yes | `workingGasVolume` | TWh, like `gas_in_storage_gwh` (`full` = stock / working gas volume x 100), not GWh. |
| `injection_capacity_gwh_per_day` | `float` | Yes | `injectionCapacity` | GWh/day. |
| `withdrawal_capacity_gwh_per_day` | `float` | Yes | `withdrawalCapacity` | GWh/day. |
| `contracted_capacity_gwh_per_day` | `float` | Yes | `contractedCapacity` | Named GWh/day, but a TWh volume (contracted + available ≈ working gas volume). |
| `available_capacity_gwh_per_day` | `float` | Yes | `availableCapacity` | Named GWh/day, but a TWh volume (see above). |
| `covered_capacity_gwh_per_day` | `float` | Yes | `coveredCapacity` | `100` on every non-null row checked (2026-08-01 to 09-22); meaning undocumented, not GWh/day. |
| `storage_pct_full` | `float` | Yes | `full` | 0-100, clamped at schema. |
| `trend` | `float` | Yes | `trend` | Signed daily delta. |
| `status` | `str` | Yes | `status` | `E` estimate, `C` confirmed, `N` no value. |
| `info` | `str` | Yes | `info` | JSON-encoded freeform info object. |
| `data_provider` | `str` | No | derived | Always `gie_agsi`. |
| `ingested_at` | `datetime[UTC]` | No | derived | Silver write timestamp. |

### Silver sample

```python
[
    {
        "gas_day": date(2026, 5, 6),
        "gas_day_end": datetime(2026, 5, 7, 0, 0, tzinfo=UTC),
        "updated_at": datetime(2026, 5, 8, 10, 0, 24, tzinfo=UTC),
        "entity_level": "country",
        "entity_code": "DE",
        "entity_name": "Germany",
        "entity_url": "DE",
        "country_code": "DE",
        "country_name": "Germany",
        "gas_in_storage_gwh": 65.9608,
        "consumption_gwh": 903.9,
        "consumption_full_pct": 7.3,
        "injection_gwh": 182.43,
        "withdrawal_gwh": 60.3,
        "net_withdrawal_gwh": -122.1,
        "working_gas_volume_gwh": 247.7476,
        "injection_capacity_gwh_per_day": 4286.25,
        "withdrawal_capacity_gwh_per_day": 7081.16,
        "contracted_capacity_gwh_per_day": 188.3776,
        "available_capacity_gwh_per_day": 63.0975,
        "covered_capacity_gwh_per_day": 100.0,
        "storage_pct_full": 26.62,
        "trend": -0.57,
        "status": "E",
        "info": None,
        "data_provider": "gie_agsi",
        "ingested_at": datetime(2026, 5, 8, 17, 40, 0, tzinfo=UTC),
    },
]
```

---

## Gold layer

**Name**: `gold_eu_gas_storage`
**Type**: SQL view
**File**: `src/gridflow/gold/views/eu_gas_storage.sql`
**Reads**: `silver_gie_agsi_storage` (source-qualified name; single-token aliases are deprecated) — a straight column projection, no joins.
**Columns**: `gas_day`, `country_code`, `country_name`, `gas_in_storage_gwh`, `withdrawal_gwh`, `injection_gwh`, `working_gas_volume_gwh`, `storage_pct_full`, `trend`, `data_provider`, `ingested_at`.
**Grain**: one row per (`gas_day`, `country_code`), ordered `gas_day DESC, country_code`.

Full column contract: see the Gold layer contracts section of
[data-contracts.md](../../../10-projects/gridflow/data-contracts.md).

---

## Known issues and gotchas

- Lowercase `x-key` header. Capitalised `X-Key` returns 401.
- `last_page` field is the pagination source of truth. `total` is the
  current-page row count, NOT the global record count.
- Flows (`injection`, `withdrawal`, `netWithdrawal`) are GWh per gas day:
  IT net injection matches ENTSOG `physical_flows` (exits minus entries
  at the three Italian UGS points, `flow_gwh_per_day`, converted from the
  vendor unit in `silver/entsog/physical_flows.py:27-68`) within 4% on 14
  gas days (ratio 0.96 to 1.02; checked 2026-09-29).
  The stock columns (`gas_in_storage_gwh`, `working_gas_volume_gwh`,
  `consumption_gwh`, `contracted_`/`available_capacity_gwh_per_day`) are on
  a scale 1,000 times the flows, so TWh, despite their names: across all nine
  countries, the day-on-day change in `gas_in_storage_gwh` x 1,000 matches
  `injection` - `withdrawal` (checked on silver 2026-09-29). GIE's own unit
  statement is not in our sources, so these units are our check.
- Rate limit: 60 calls/min (1 req/s).
- GB returns "United Kingdom (Pre-Brexit)" with `-` placeholders for
  numeric values post-Brexit. Convert `-` to null at the silver-transformer
  boundary (`_safe_float` already does this).
- The `gas_day` field is a `date` (vendor `gasDayStart`), not a
  timestamp. gridflow labels `event_time` at a fixed 06:00 UTC
  (`silver/base.py:383-400`), a project convention; `gas_day_end` is the
  next date at 00:00 UTC. Neither is the vendor's start or end instant.
- `gas_day_start_validation` is enforced in the connector — a country
  query for `date=2026-05-06` will fail loudly if the response contains
  a different gas day. Helps catch silent vendor caching errors.
- Country list (`AGSI_COUNTRIES`): `AT, BE, DE, ES, FR, GB, IT,
  NL, PL` is gridflow's choice (`connectors/gie/endpoints.py:14`), not
  AGSI's footprint: the `EU` aggregate in `storage_reports` has a working
  gas volume above the sum of these countries', so it covers storage in
  other countries too. Never sum country rows to get the EU figure.

---

## Implementation delta

- **Endpoint path**: registry uses `/api`; live API agrees. No discrepancy.
- **Pagination**: registry uses `last_page` correctly. No discrepancy.
- **Legacy fallback**: `connectors/gie/client.py::_fetch_country` (used
  by `gie_alsi`) still uses `till=` instead of `to=` for the range
  parameter. AGSI's `_fetch_agsi_storage` correctly uses `from`/`to`.
  The legacy code path is unused for `gie_agsi` so this is not a live
  bug, but flagged for the eventual ALSI implementation.

No discrepancies found for the active AGSI `storage` code path.

---

## Modelling notes

- **Models**: country-level winter-tightness, EU gas balance,
  storage-spread (S/W) trades, security-of-supply stress tests.
- **Targets**: `storage_pct_full` (% full), `net_withdrawal_gwh` (daily
  flow), `gas_in_storage_gwh` (absolute level).
- **Features**: lag of `full` and `trend`, weather-driven
  consumption (HDD), capacity utilisation
  (`gas_in_storage_gwh / working_gas_volume_gwh`).
- **Filters**: drop rows where `status = N` (no value); GB Pre-Brexit
  rows are effectively unusable post-2020.
- **Joins**: ENTSOG flows (cross-border imports), Open-Meteo HDD,
  Elexon `tsdf` / NESO regional demand for power-sector gas burn.

---

## Links

- [Official API docs](https://agsi.gie.eu/api)
- `Python/gridflow/src/gridflow/connectors/gie/client.py`
- `Python/gridflow/src/gridflow/connectors/gie/endpoints.py`
- `Python/gridflow/src/gridflow/silver/gie/agsi.py`
- `Python/gridflow/src/gridflow/schemas/gie.py`
- [Domain: gas day](../../../20-domain/concepts/gas-day.md)
