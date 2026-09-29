---
source: elexon
dataset_key: disbsad
vendor: Elexon BMRS
last_verified: 2026-05-21
layer_coverage: bronze, silver
v2_fix_history:
  - date: 2026-05-20
    phase: gridflow-G5-W1.3
    pr: https://github.com/EBentham/gridflow/pull/7
    change: silver transformer now also renames current-API `service` field to `component` alongside the legacy `component` key
page:
  title: Balancing services adjustments, per action
  summary: >-
    Elexon's balancing services adjustment actions for each GB settlement period, one row each:
    service, flags, cost in £ and volume in MWh.
  facts:
    vendor: Elexon BMRS, dataset DISBSAD
    cadence: By half-hour settlement period
    grain: One row per settlement period, action id and service
  landscape: market
  what_it_is: >-
    Elexon's balancing services adjustment actions for each GB settlement period, one row per
    action: its service (`Energy`, `System` and `Non-BM LCM` appear here), the `so_flag` and
    `stor_flag` flags, cost in £ and volume in MWh. The net table, NETBSAD, has one row per
    period instead. Elexon also sends each action's party and asset; gridflow does not keep them.
  how_used:
    - Splitting balancing adjustment volume and cost by service for an imbalance price model.
    - "Average price of each service's actions in a period: cost over volume."
  chart:
    type: stacked-area
    silver: elexon/disbsad
    time: timestamp_utc
    value: volume
    filter:
      - {column: settlement_date, op: ge, value: "2026-09-14"}
      - {column: settlement_date, op: le, value: "2026-09-19"}
    dedup: {"on": [settlement_date, settlement_period, adjustment_action_id, component], order_by: ingested_at}
    group: component
    group_map:
      Energy: energy
      System: system
      Non-BM LCM: lcm
    group_null: none
    series_order: [system, energy, lcm, none]
    aggregation: sum
    window: {start: "2026-09-13", end: "2026-09-19"}
    unit: MWh
  chart_view:
    title: Adjustment volume by service, 14 to 19 September 2026
    caption: >-
      Silver `elexon/disbsad`, MWh, every half-hour of settlement dates 14 to 19 September 2026:
      each service's action volumes summed, each action counted once. Positive values stack above
      zero and negative values hang below it.
    alt: >-
      Stacked area chart of balancing services adjustment volume by service from elexon/disbsad,
      in MWh, for every half-hour of settlement dates 14 to 19 September 2026. Energy volumes are
      positive, 0.1 to 773 MWh, highest on the 14th and 16th. System volumes reach 750 MWh on the
      17th and dip to -100 MWh on the 16th. Non-BM LCM hangs just below zero, down to -5.76 MWh.
      Many half-hours carry no action and sit at zero.
    x_label: settlement date; each starts at 23:00 UTC
    key:
      - {series: energy, label: Energy actions, codes: Energy, paint: hatch-lines, note: "Every Energy volume here is positive, with `so_flag` false."}
      - {series: system, label: System actions, codes: System, paint: hatch-cross, note: "Signed, -100 to 750 MWh here; the sign's meaning is not stated."}
      - {series: lcm, label: Non-BM LCM actions, codes: Non-BM LCM, paint: hatch-dots, note: "Negative volumes with positive costs here; 5.76 MWh at most, too thin to see."}
      - {series: none, label: No action, codes: null service, paint: hatch-vertical, note: "A period with no action here carries one zero row with no service."}
  raw_feed:
    note: >-
      From the Elexon Insights API in 24-hour `from`/`to` windows from midnight UTC. Replies
      fetched for this page also held the half-hour at `to`, so silver keeps it twice.
    requests:
      - "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/DISBSAD?from=2026-09-17T00:00:00Z&to=2026-09-18T00:00:00Z&page=1"
    commands:
      - {run: gridflow ingest elexon disbsad --start 2026-09-13 --end 2026-09-20, comment: "bronze; the end is exclusive"}
      - {run: gridflow transform elexon disbsad --start 2026-09-13 --end 2026-09-19, comment: "starts early: dates begin 23:00 UTC"}
  record:
    select:
      filter:
        - {column: settlement_date, op: eq, value: "2026-09-17"}
        - {column: settlement_period, op: eq, value: 42}
        - {column: adjustment_action_id, op: in, value: ["1", "2", "50", "51", "52", "53", "83", "84"]}
      dedup: {"on": [settlement_date, settlement_period, adjustment_action_id, component], order_by: ingested_at}
      order_by: [adjustment_action_id]
    key: [settlement_date, settlement_period, adjustment_action_id, component]
    caption: "Settlement date 2026-09-17, period 42: eight actions across three services, both `so_flag` values."
    fields:
      settlement_date: GB settlement date, as Elexon labels it
      settlement_period: Half-hour of the settlement day, 1 to 48; 46 or 50 on clock-change days
      timestamp_utc: Start of the half-hour, computed from settlement date and period
      adjustment_action_id: "Action number as Elexon sends it in `id`, stored as text"
      so_flag: "System operator flag, Elexon's `soFlag`, as sent"
      stor_flag: "STOR provider flag, from `storFlag` (legacy `storProviderFlag`)"
      component: "Service, from `service` (legacy `component`); null on a period's zero row"
      cost: "Cost of the action in £, signed; the sign's meaning is not stated"
      volume: "Volume of the action in MWh, signed; the sign's meaning is not stated"
  notebook:
    lead: >-
      Returns a pandas DataFrame from the DuckDB relation `silver_elexon_disbsad`, filtered on
      `settlement_date` with both ends included. Lineage columns are dropped; the midnight
      half-hour can come twice, so drop repeats on the key.
    cells:
      - |
        df = data.elexon.query("disbsad", "2026-09-14", "2026-09-19")
        key = ["settlement_date", "settlement_period", "adjustment_action_id", "component"]
        df = df.drop_duplicates(key).sort_values(["timestamp_utc", "component"])
      - df[key + ["so_flag", "cost", "volume"]].head()
      - |
        vol = (df.assign(component=df.component.fillna("none"))
                 .pivot_table(index="timestamp_utc", columns="component", values="volume",
                              aggfunc="sum", fill_value=0)
               [["Energy", "Non-BM LCM", "System"]])
        vol.plot(ylabel="MWh", color=["#155A6E", "#8A6D3B", "#C0703E"], figsize=(8, 3.5))
    needs: 13 to 19 September 2026
    plot_alt: >-
      Line plot of half-hourly volume by component against timestamp_utc, 14 to 19 September
      2026: Energy and System step between zero and blocks of up to 770 MWh, System dips to
      -100 MWh on the 16th, and Non-BM LCM stays at or just below zero.
  related:
    - {dataset: elexon/netbsad, note: "Elexon's net adjustment per period, published as its own table"}
    - {dataset: elexon/system_prices, note: The imbalance prices for the same settlement periods}
    - {dataset: elexon/boal, note: Balancing Mechanism acceptances for the same settlement periods}
---

# Elexon - Disaggregated Balancing Services Adjustment Data (`DISBSAD`)

## Overview

Disaggregated Balancing Services Adjustment Data (DISBSAD) — the individual Balancing Services Adjustment Actions, which Elexon's guidance names as one of the two parts of BSAD, the other being the BPA/SPA (see Vendor documentation below); no vendor text found says NETBSAD is derived from DISBSAD (checked 2026-09-29). Each row captures the cost and volume of a single non-BM balancing action (e.g. STOR call-off, ancillary services, system operator instructions outside of BOALF). Together with NETBSAD, DISBSAD is what BSC parties consume to reconcile imbalance settlement.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://data.elexon.co.uk/bmrs/api/v1` |
| Path             | `/datasets/DISBSAD` |
| Method           | GET |
| Auth             | None required for tested endpoints (2026-05-08). Some endpoints accept an `apikey` header (env: `ELEXON_API_KEY`); registration at https://www.elexonportal.co.uk/. |
| Rate limit       | Vendor-published: not stated. Project default 2 req/sec (asyncio.Semaphore); verified safe 2026-05-08. |
| Pagination       | Connector handles via `page=N` query param; stops when `page >= total_pages`. Reference endpoints (`/reference/bmunits/all`) are not paginated. |
| Historical depth | Several years. |
| Publication lag  | Same cadence as system prices (per settlement run). |
| Response format  | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `from` | string | Yes | The "from" start time or settlement date for the filter. | `2026-05-06T00:00Z` |
| `to` | string | Yes | The "to" start time or settlement date for the filter. | `2026-05-06T03:00Z` |
| `settlementPeriodFrom` | integer | No | The "from" settlement period for the filter. This should be an integer from 1-50 inclusive. | `1` |
| `settlementPeriodTo` | integer | No | The "to" settlement period for the filter. This should be an integer from 1-50 inclusive. | `48` |
| `format` | string | No | Response data format. Use json/xml to include metadata. | `json` |

### Working curl example

```bash
# Replace <ELEXON_API_KEY> with your env var if you choose to send one (Elexon endpoints
# tested 2026-05-08 do NOT require a key; set anyway for vendor courtesy).
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://data.elexon.co.uk/bmrs/api/v1/datasets/DISBSAD?from=2026-05-06T00:00Z&to=2026-05-06T03:00Z&format=json" \
  -o "/tmp/elexon-disbsad.json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/elexon/disbsad/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per API call (paginated requests append additional files for the same date partition).

### Bronze sample

Captured live 2026-05-08 from the https://data.elexon.co.uk/bmrs/api/v1/datasets/DISBSAD?from=2026-05-06T00:00Z&to=2026-05-06T03:00Z&format=json:

```json
{
  "data": [
    {
      "dataset": "DISBSAD",
      "settlementDate": "2026-05-06",
      "settlementPeriod": 9,
      "id": 1,
      "cost": 0.0,
      "volume": 0.0,
      "soFlag": true,
      "storFlag": false,
      "partyId": null,
      "assetId": null,
      "isTendered": null,
      "service": null
    },
    {
      "dataset": "DISBSAD",
      "settlementDate": "2026-05-06",
      "settlementPeriod": 8,
      "id": 1,
      "cost": 0.0,
      "volume": 0.0,
      "soFlag": true,
      "storFlag": false,
      "partyId": null,
      "assetId": null,
      "isTendered": null,
      "service": null
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/elexon/disbsad/year=YYYY/month=MM/disbsad_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.elexon.disbsad.DISBSADTransformer`
**Pydantic schema**: `gridflow.schemas.elexon.ElexonDISBSAD`
**Dedup key**: `(settlement_date, settlement_period, adjustment_action_id, component)`, `keep="last"`, applied to one bronze day's rows at a time (`silver/elexon/disbsad.py:118-123`)
**Point-in-time field**: `ingested_at` (no native PIT field)

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `settlement_date` | `date` | No | `settlementDate` | Settlement date (BST/GMT calendar). |
| `settlement_period` | `int` | No | `settlementPeriod` | 1..50 (DST: 46 spring, 50 autumn). |
| `timestamp_utc` | `datetime[UTC]` | No | _derived_ | Derived from (settlement_date, settlement_period) via `utils/time.settlement_period_to_utc`. |
| `adjustment_action_id` | `str` | Yes | `id` | DISBSAD action identifier. |
| `so_flag` | `bool` | No | `soFlag` | System Operator flag. |
| `stor_flag` | `bool` | No | `storFlag` (current) / `storProviderFlag` (legacy) | STOR flag. The transformer maps both (`disbsad.py:73-74`). |
| `component` | `str` | Yes | `component` (legacy) / `service` (current) | DISBSAD component code. G5-W1.3: live API renamed to `service` 2026-05; transformer renames both. |
| `cost` | `float` | Yes | `cost` | GBP (*Imbalance Pricing Guidance* p. 16; see Vendor documentation). |
| `volume` | `float` | Yes | `volume` | MWh (*Imbalance Pricing Guidance* p. 16). |
| `data_provider` | `str` | No | _derived_ | Default `"elexon"`. |
| `ingested_at` | `datetime[UTC]` | Yes | _derived_ | When the silver transform ran: stamped `datetime.now(UTC)` by the transformer (`disbsad.py:125-129`), not the bronze ingest time. |

### Silver sample

```python
[
    {
        "settlement_date": "2026-05-06",
        "settlement_period": 9,
        "timestamp_utc": "2026-05-06T04:00:00+00:00",
        "adjustment_action_id": 1,
        "so_flag": true,
        "stor_flag": "...",
        "component": "...",
        "cost": 0.0,
        "volume": 0.0,
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

- **DISBSAD and NETBSAD are not "sum and total"**: Elexon's guidance treats the individual actions (DISBSAD) and the BPA/SPA as the two parts of BSAD (Vendor documentation below); no vendor text found says NETBSAD sums DISBSAD. Measured 2026-09-29 on local silver: `netbsad` reads 0.0 in every column for 2026-09-17 periods 40 to 44, where these actions total 450 to 750 MWh of positive volume per period. Do not read NETBSAD as a DISBSAD sum.
- **Cost field unit**: GBP (not GBP/MWh). Vendor source: *Imbalance Pricing Guidance* p. 16, quoted below.
- **Midnight half-hour in two replies (measured 2026-09-29)**: the nine replies for `from=D T00:00:00Z&to=D+1 T00:00:00Z`, D = 13 to 21 September 2026 (fetched 2026-09-26), each ran from the period starting at D 00:00 UTC to the one starting at D+1 00:00 UTC, both included. The transformer dedups within one bronze day only (`disbsad.py:118-123`), so silver holds those keys twice (9 keys in September, all settlement period 3, same cost and volume). The vendor text quoted here does not say whether `to` is inclusive, and gridflow treats the bare `from`/`to` override as undocumented (`silver/elexon/_publication_window.py:53-56`). Dedup on the four key columns when reading across days.

### Vendor documentation

- Elexon, *Imbalance Pricing Guidance*, v15.0, 25 June 2020 (https://www.elexon.co.uk/bsc/documents/training-guidance/bscguidance-notes/imbalance-pricing/), p. 16: "BSAD is made up of two parts: Balancing Services Adjustment Actions (disaggregated BSAD); and Buy Price Price Adjustment (BPA) / Sell Price Price Adjustment (SPA)." "Each Balancing Services Adjustment Action has a: Balancing Services Adjustment Cost – value in £ (can be a NULL cost); Balancing Services Adjustment Volume – value in MWh; SO-Flag - either set to True/False; and STOR Provider Flag – either set to True/False."
- Same, p. 19: "For Balancing Services Adjustment Actions, the SO also flags when it believes the balancing action was impacted by a transmission constraint", with two further interconnector reasons.
- The guidance states no sign convention for the action's cost or volume (text search of the whole document, 2026-09-29).

---

## Implementation delta

- **Param style**: docs require `from`/`to`; code matches.
- **No Pydantic class** beyond `ElexonDISBSAD` for many fields — schema enforces the core (settlement_date, settlement_period, optional flags); silver transformer enforces full output column set.

### V2-FIX changelog

- **2026-05-20 — gridflow G5-W1.3 (PR #7)**: live Elexon API now returns
  `service` rather than `component`. Silver transformer renames both;
  pre-G5 silver carried `null` on `component` because the live bronze
  didn't match the original rename map (P1 silent-null bug).

---

## Modelling notes

TODO

---

## Links

- [Official API docs (Swagger UI)](https://bmrs.elexon.co.uk/api-documentation)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/elexon/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/elexon/disbsad.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/elexon.py)
- Gold view/builder
- [Domain: GB Balancing Mechanism](../../../20-domain/markets/gb-balancing-mechanism.md)
