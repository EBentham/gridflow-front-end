---
source: gie_alsi
dataset_key: lng
vendor: GIE ALSI
last_verified: 2026-05-11
layer_coverage: bronze, silver
page:
  title: LNG terminals by country
  summary: >-
    GIE's ALSI LNG terminal data at country level: each gas day's send-out in GWh, with vendor
    fields `dtrs` and `dtmi` as sent.
  facts:
    vendor: "GIE ALSI, `alsi.gie.eu/api`, queried by country"
    cadence: One value per gas day, as sent in the responses we hold
    grain: One row per country and gas day; eight countries requested
  landscape: gas
  what_it_is: >-
    GIE's ALSI LNG figures for the eight countries gridflow requests (BE, ES, FR, GB, IT, NL, PL,
    PT), one row per country and gas day; gridflow asks for country figures, not terminals. Silver
    keeps send-out in GWh and the raw `dtrs` and `dtmi` values. GB's `-` placeholders become nulls.
    LNG inventory is in the response but not in silver.
  how_used:
    - LNG send-out as a supply term in a country's daily gas balance.
    - Reading send-out against pipeline flows and storage moves on the same gas day.
    - A per-country regasification feature for gas or power price models.
  chart:
    type: stacked-area
    silver: gie_alsi/lng
    time: gas_day
    value: send_out_gwh
    filter:
      - {column: country_code, op: ne, value: GB}
    group: country_code
    group_map:
      NL: nl
      IT: it
      PT: pt
      PL: pl
      BE: be
      ES: es
      FR: fr
    series_order: [nl, it, pt, pl, be, es, fr]
    aggregation: sum
    window: {start: "2026-09-13", end: "2026-09-22"}
    unit: GWh
  chart_view:
    title: LNG send-out by country, 13 to 22 September 2026
    caption: >-
      Silver `gie_alsi/lng`, GWh per gas day, each country's send-out as sent, stacked, for the
      ten gas days 13 to 22 September 2026: too short a window to read a trend. GB is left out:
      GIE sends it as `-`.
    alt: >-
      Stacked area chart of LNG send-out by country from gie_alsi/lng, in GWh per gas day, for gas
      days 13 to 22 September 2026. From the bottom: Netherlands (587 to 764), Italy (506 to 700),
      Portugal (173 to 187), Poland (85 to 191), Belgium (92 to 264, climbing over the last four
      days), Spain (295 to 698) and France (354 on the 15th to 1,085 on the 21st). The stacked total
      runs from about 2,690 on the 13th to 3,724 on the 21st.
    x_label: "gas day, as GIE's gasDayStart dates it"
    key:
      - {series: fr, label: France, codes: FR, paint: horizon, note: "The 18 Sep value arrived with vendor status code `E`, which silver does not keep."}
      - {series: es, label: Spain, codes: ES, paint: clay}
      - {series: be, label: Belgium, codes: BE, paint: chartreuse}
      - {series: pl, label: Poland, codes: PL, paint: hatch-dots}
      - {series: pt, label: Portugal, codes: PT, paint: hatch-lines}
      - {series: it, label: Italy, codes: IT, paint: olive}
      - {series: nl, label: Netherlands, codes: NL, paint: petrol, note: "The 17 Sep value arrived with vendor status code `E`, which silver does not keep."}
  raw_feed:
    note: >-
      From GIE's ALSI API: one request per country for the whole window, paged at `size=300`, `till`
      included. Rows also carry `inventory`, `status`, `updatedAt` and capacity fields silver drops.
    requests:
      - "GET https://alsi.gie.eu/api?country=NL&from=2026-09-13&till=2026-09-22&page=1&size=300"
    commands:
      - {run: gridflow ingest gie_alsi lng --start 2026-09-13 --end 2026-09-22, comment: "bronze; the end day is fetched"}
      - {run: gridflow transform gie_alsi lng --start 2026-09-13 --end 2026-09-22, comment: bronze to silver}
  record:
    select:
      filter:
        - {column: gas_day, op: eq, value: "2026-09-20"}
      order_by: [country_code]
      columns: [gas_day, country_code, country_name, send_out_gwh, dtrs, dtmi_lng, dtmi_gwh]
    key: [gas_day, country_code]
    caption: "Gas day 2026-09-20, the eight countries gridflow requests; GB's values arrive as `-`, stored null."
    fields:
      gas_day: "GIE's `gasDayStart` date; gridflow labels it 06:00 UTC in `event_time`"
      country_code: "Country code GIE sends as `code`"
      country_name: "Country name as GIE sends it (`name`)"
      send_out_gwh: "Send-out over the gas day, GWh, from `sendOut`; null when GIE sends `-`"
      dtrs: "Vendor `dtrs` as sent; not a percentage; units unconfirmed in gridflow's schema"
      dtmi_lng: "The `lng` member of vendor `dtmi`, as sent; units unconfirmed"
      dtmi_gwh: "The `gwh` member of vendor `dtmi`, as sent; units unconfirmed"
  notebook:
    source: gie_alsi
    lead: >-
      Returns a pandas DataFrame from the DuckDB relation `silver_gie_alsi_lng`, filtered on
      `gas_day` with both ends included. Lineage columns are dropped; rows come ordered by
      `gas_day` only.
    cells:
      - |
        df = data.gie_alsi.query("lng", "2026-09-13", "2026-09-22")
        df = df.sort_values(["gas_day", "country_code"])
      - df[["gas_day", "country_code", "send_out_gwh"]].head()
      - |
        sent = df[df.country_code != "GB"]
        wide = sent.pivot(index="gas_day", columns="country_code", values="send_out_gwh")
        ax = wide.plot.area(ylabel="GWh per gas day", figsize=(8, 3.5))
        ax.legend(loc="upper left", bbox_to_anchor=(1, 1));
    needs: 13 to 22 September 2026
    plot_alt: >-
      Pandas stacked area plot of send_out_gwh by country_code against gas_day, 13 to 22 September
      2026, GB left out: BE at the bottom, then ES, FR, IT, NL, PL and PT, legend to the right. The
      top edge runs from about 2,690 GWh on the 13th to a peak near 3,724 on the 21st.
  related:
    - {dataset: gie/storage, note: "Underground storage levels by country for the same gas days"}
    - {dataset: entsog/physical_flows, note: "Pipeline flows on the same gas days, for a daily supply balance"}
---

# GIE ALSI - LNG Terminals

## Overview

Country-level LNG terminal send-out data from GIE ALSI (the response also
carries inventory, which silver does not keep). ALSI shares
the same `x-key` authentication model as AGSI+, but uses the base URL
`https://alsi.gie.eu`. In `gridflow`, the active source is `gie_alsi` and the
active dataset key is `lng`.

## API endpoint

| Property | Value |
|---|---|
| Base URL | `https://alsi.gie.eu` |
| Path | `/api` |
| Method | GET |
| Auth | Header `x-key: <GIE_API_KEY>` |
| Country set | `BE, ES, FR, GB, IT, NL, PL, PT` |
| Response format | JSON |
| Pagination | `page` + `size`; connector stops from `last_page` (the authoritative page count). `total` is the per-page row count; `pageSize` is absent from the live envelope. |

### Query parameters

`country`, `from`, `till`, `page`, `size`.

## Bronze layer

Path:
`{data_root}/bronze/gie_alsi/lng/YYYY/MM/DD/raw_<uuid>.json`

The connector stamps `data_date=start.date()`.

## Silver layer

Path:
`{data_root}/silver/gie_alsi/lng/year=YYYY/month=MM/lng_YYYYMMDD.parquet`

Transformer:
`gridflow.silver.gie.alsi.LNGTerminalTransformer`

Pydantic schema:
`gridflow.schemas.gie.LNGTerminal`

Dedup key:
`(gas_day, country_code)` when `country_code` is present, otherwise
`gas_day`.

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|---|---|---|---|---|
| `gas_day` | `date` | No | `gasDayStart` | Gas-day grain; the only date field the transformer reads (`silver/gie/alsi.py:56-67`) |
| `country_code` | `str` or `None` | Yes | `countryCode` / `code` | ISO-like country code |
| `country_name` | `str` or `None` | Yes | `countryName` / `name` | Country display name |
| `lng_in_storage_gwh` | `float` or `None` | Yes | `lngInventory` / `gasInStorage` | Stored LNG volume. **Not written:** the live response sends inventory as `inventory: {lng, gwh}`, which this field map does not match (`silver/gie/alsi.py:96-97`), so silver has no such column |
| `send_out_gwh` | `float` or `None` | Yes | `sendOut` / `withdrawal` | LNG send-out over the gas day, GWh |
| `injection_gwh` | `float` or `None` | Yes | `injection` | LNG injection. **Not written:** the live response has no `injection` field |
| `lng_pct_full` | `float` or `None` | Yes | derived (`lng_in_storage_gwh` / `dtmi_gwh` × 100) | Honest LNG %-full, clamped to [0, 100] in the transformer. **Not written:** it needs `lng_in_storage_gwh`, which is absent (`silver/gie/alsi.py:142`) |
| `dtrs` | `float` or `None` | Yes | `dtrs` | Raw vendor `dtrs`; **unconfirmed non-percentage** metric (live ~724–2132, so not a percent), units not in official ALSI docs |
| `dtmi_lng` | `float` or `None` | Yes | `dtmi.lng` | Raw vendor `dtmi.lng` member; unconfirmed units |
| `dtmi_gwh` | `float` or `None` | Yes | `dtmi.gwh` | Raw vendor `dtmi.gwh` member; unconfirmed units; feeds derived `lng_pct_full` |
| `trend` | `float` or `None` | Yes | `trend` | Daily trend where published. **Not written:** the live response has no `trend` field |
| `data_provider` | `str` | No | derived | Constant `gie_alsi` |
| `ingested_at` | `datetime` UTC or `None` | Yes | derived | Transformer run time |
| `event_time` | `datetime` UTC | No | derived | `gas_day` at 06:00 UTC, gridflow's fixed labelling convention (`silver/gie/alsi.py:27-28`, `silver/base.py:383-400`) |
| `available_at` | `datetime` UTC | No | base transformer | Added at write time |
| `source_run_id` | `str` | No | base transformer | Added at write time |
| `dataset_version` | `str` | No | base transformer | Added at write time |

## Modelling notes

- Use `gas_day` as the date grain; do not infer an hourly timestamp without an
  explicit gas-day convention.
- Pair this dataset with `gie_agsi/storage` and ENTSO-G physical flows for
  cross-gas-supply views.
- GB numeric values arrive as `-` placeholders (status `N`) and are stored as
  null; treat null as publication absence, not zero.

## Links

- [Connector](../../../../../../Python/gridflow/src/gridflow/connectors/gie/client.py)
- [Endpoint constants](../../../../../../Python/gridflow/src/gridflow/connectors/gie/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/gie/alsi.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/gie.py)
