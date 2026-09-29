---
source: gie_agsi
dataset_key: about_listing
vendor: GIE AGSI+ (Gas Storage)
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: AGSI+ storage operators and facilities
  summary: >-
    GIE's register of the storage operators and facilities that report to AGSI+, with their EIC
    codes, countries and parent operators.
  facts:
    vendor: "GIE AGSI+, `/api/about`; `show=listing` returns the flat form"
    cadence: A whole-register snapshot per call; `sources.yaml` declares it weekly
    grain: "One row per EIC per transform day; `entity_level` says operator or facility"
  landscape: gas
  what_it_is: >-
    GIE's register of AGSI+ storage system operators and their facilities, fetched whole in one
    call. `about_listing` flattens the `show=listing` form into one row per operator or facility
    EIC. The payload lists some EICs more than once (an operator under two countries, UK entries
    before and after Brexit); silver keeps one row per EIC per transform day.
  how_used:
    - gridflow's connector fetches this listing to plan company and facility storage queries.
    - Rolling facility storage up to operators through `company_code`.
    - Finding closed facilities, from the operational dates `about_summary` keeps.
  chart:
    type: bar
    silver: gie_agsi/about_listing
    filter:
      - {column: entity_level, op: eq, value: facility}
    dedup: {on: [entity_code], order_by: ingested_at}
    group: country_code
    group_map:
      DE: germany
      FR: france
      NL: netherlands
      RO: romania
      AT: austria
      GB: uk
      CZ: czech
      PL: poland
    group_default: rest
    aggregation: count
    sort: value_desc
    unit: facility EICs
  chart_view:
    title: AGSI+ facilities by country, fetched 27 September 2026
    caption: >-
      Silver `gie_agsi/about_listing` only, as fetched 27 September 2026: facility rows counted
      once per EIC by `country_code`, the country GIE lists each under. Closed and historical
      entries count too, whether or not their names say so.
    alt: >-
      Horizontal bar chart counting facility EICs by country in gie_agsi/about_listing as fetched
      27 September 2026. Germany leads with 63. The bar for thirteen smaller countries together
      comes second at 18. Then France 8, Netherlands 7, Romania 7, Austria 5, United Kingdom 5,
      Czech Republic 4 and Poland 4.
    key:
      - {series: germany, label: Germany, codes: DE, paint: petrol}
      - {series: rest, label: 13 others, codes: 13 country codes, paint: hatch-dots, note: "IT, DK, HU, SK, BE, BG, ES, HR, IE, LV, PT, SE and UA, counted together."}
      - {series: france, label: France, codes: FR, paint: petrol}
      - {series: netherlands, label: Netherlands, codes: NL, paint: petrol}
      - {series: romania, label: Romania, codes: RO, paint: petrol}
      - {series: austria, label: Austria, codes: AT, paint: petrol}
      - {series: uk, label: United Kingdom, codes: GB, paint: petrol, note: "Each is listed under `GB` to 2020 and again under post-Brexit `GB*`; silver kept the pre-Brexit `GB` entry."}
      - {series: czech, label: Czech Republic, codes: CZ, paint: petrol}
      - {series: poland, label: Poland, codes: PL, paint: petrol}
  raw_feed:
    note: >-
      One unpaginated GET per member; no dates are sent. Bronze is filed under the `--start` date,
      not the fetch time. A transform day with no bronze copies the newest capture.
    requests:
      - "GET https://agsi.gie.eu/api/about?show=listing"
    commands:
      - {run: gridflow ingest gie_agsi about_listing --start 2026-09-27, comment: "one call; folder named by --start"}
      - {run: gridflow transform gie_agsi about_listing --start 2026-09-27 --end 2026-09-27, comment: "one day, one silver copy"}
  record:
    select:
      filter:
        - {column: entity_code, op: in, value: [21X0000000011756, 55XHUMBLYGROVE1H, 21X-SE-A-A0A0A-F, 21W0000000000435, 21W000000000095N, PRIOR_EWE_000001, 21W0000000001075, 55WHUMBLY1GROVER]}
      dedup: {on: [entity_code], order_by: ingested_at}
      order_by: [entity_level, entity_code]
      columns: [entity_level, entity_code, entity_name, country_code, entity_type, company_code, company_name]
    key: [entity_code]
    caption: "Three operators and five facilities picked by EIC, operators first, then by `entity_code`."
    fields:
      entity_code: "The listing's `eic`; one row per EIC per transform day, the last sent"
      entity_level: "`company` for an operator, `facility` for a storage entry; set by gridflow"
      entity_name: "GIE's `short_name`, else `name`; `about_summary` keeps the full `name`"
      country_code: "`country` as sent; GIE's post-Brexit UK entries carry `GB*`, dropped here by EIC dedup"
      entity_type: "GIE's `type`: `SSO` for operators, other codes for facilities; blank becomes null"
      company_code: "Facilities only: the parent operator's EIC, from `company`; null on operator rows"
      company_name: "Facilities only: `short_name` of the operator entry the facility is listed under"
      entity_url: "The `/api` storage query URL GIE sends for this operator or facility"
  notebook:
    source: gie_agsi
    lead: >-
      `query()` filters on `ingested_at`, a transform time, and each transform day holds a whole
      copy of the listing, so these cells use `data.sql()` on the newest day.
    cells:
      - |
        df = data.sql("""
            SELECT entity_level, entity_code, entity_name, country_code,
                   entity_type, company_code, company_name
            FROM silver_gie_agsi_about_listing
            WHERE event_time = (SELECT max(event_time) FROM silver_gie_agsi_about_listing)
            ORDER BY entity_level, entity_code
        """)
      - df[["entity_level", "entity_code", "entity_name", "country_code"]].head()
      - df["entity_level"].value_counts()
      - df["entity_type"].value_counts(dropna=False)
    needs: the AGSI+ operator listing
  related:
    - {dataset: gie/storage_reports, note: "Company and facility storage, by the same EIC as `entity_code`"}
    - {dataset: gie/unavailability, note: "Storage outages; its `facility` field names facilities by these EICs"}
    - {dataset: gie/storage, note: "Daily storage by country; gridflow fetches nine of the countries listed here"}
  family:
    slug: agsi-reference
    members:
      - dataset: about_listing
        differs: "Flat form: short names, EIC, country and parent operator; no operational dates"
        request: "GET https://agsi.gie.eu/api/about?show=listing"
      - dataset: about_summary
        differs: "Nested form adds full names, country names, operational dates; its UK rows keep `GB*`"
        request: "GET https://agsi.gie.eu/api/about"
---

# GIE AGSI+ — About listing (flat operator and facility inventory)

## Overview

`about_listing` returns the same operator / facility universe as
`about_summary` but in a flat, list-shaped form via
`/api/about?show=listing`. Each list entry is a company dict carrying
its EIC, country, and a nested `facilities` array. This is the form
gridflow uses to plan expected counts for `storage_reports` queries
across `company` and `facility` scopes (see
`build_storage_query_plan` in `connectors/gie/endpoints.py`).

The dataset answers: "What companies and facilities does AGSI know
about, in machine-readable list form, with one record per row?" — used
for query inventory planning and deduplicating against `about_summary`.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://agsi.gie.eu` |
| Path             | `/api/about` |
| Method           | GET |
| Auth             | header `x-key` (lowercase), key from env `GIE_API_KEY` |
| Rate limit       | 60 calls/minute. Connector throttles to 1 req/s. |
| Pagination       | None — single response. (No `last_page` / `total` fields in live response.) |
| Historical depth | Snapshot of current state. |
| Publication lag  | Refreshed when GIE updates the operator inventory. |
| Response format  | JSON (top-level **list** in live behaviour) |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `show` | str | Yes | Must be `listing` to switch from the nested `about` form. | `show=listing` |

### Working curl example

```bash
# Replace <KEY> with $GIE_API_KEY
curl --ssl-no-revoke -X GET \
  "https://agsi.gie.eu/api/about?show=listing" \
  -H "x-key: <KEY>"
```

Live response: HTTP 200, ~53 KB, top-level list of 71 company objects.

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/gie_agsi/about_listing/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON. Immutable.
**Granularity**: One file per fetch (weekly schedule per `config/sources.yaml`).

### Bronze sample

Live shape — top-level list (no `data` envelope):

```json
[
  {
    "name": "GSA LLC",
    "short_name": "GSA",
    "type": "SSO",
    "eic": "25X-GSALLC-----E",
    "country": "AT",
    "url": "https://agsi.gie.eu/api?country=AT&company=25X-GSALLC-----E",
    "facilities": [
      {
        "name": "UGS Haidach (GSA) // historical data prior to 6 Oct 2022",
        "type": "DSR",
        "eic": "25W-SPHAID-GAZ-M",
        "country": "AT",
        "company": "25X-GSALLC-----E",
        "url": "https://agsi.gie.eu/api?country=AT&company=25X-GSALLC-----E&facility=25W-SPHAID-GAZ-M",
        "operational_start_date": "2011-01-01",
        "operational_end_date": "2022-10-07"
      }
    ]
  }
]
```

The fixture (`tests/fixtures/gie/agsi_listing_response.json`) wraps the
list in a `{"data": [...]}` envelope. The connector parser
(`_listing_rows`) accepts either shape.

---

## Silver layer

**Path pattern**: `{data_root}/silver/gie_agsi/about_listing/year=YYYY/month=MM/about_listing_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.gie.agsi.AboutListingTransformer`
**Pydantic schema**: (no dedicated schema — reference data; rows are flattened companies + facilities)
**Dedup key**: `entity_code` alone, `keep="last"` (`AgsiJsonTransformer.transform` dedups on whichever of `id`, `url`, `turl`, `entity_code`, `eic` exist; only `entity_code` does here; `silver/gie/agsi.py:387-391`). The live listing repeats some EICs (an operator under two countries, such as SEFE, Uniper and EWE; UK operators and facilities under both `GB` and post-Brexit `GB*`; one Italian facility EIC under two names), so the earlier entries for those EICs are dropped.
**Point-in-time field**: none — snapshot reference table. `event_time` is the transform target date at 00:00 UTC (`silver/base.py:2228-2232`). `fallback_to_latest_partition = True` (`agsi.py:309`, `405-406`): a transform day with no bronze reads the most recently written bronze folder, so a multi-day transform writes one identical copy of the capture per day.

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `entity_level` | `str` | No | derived | `company` or `facility`. |
| `entity_code` | `str` | No | `eic` | EIC identifier. |
| `entity_name` | `str` | No | `short_name` (else `name`) | `parse_listing_inventory` prefers `short_name` (`connectors/gie/endpoints.py:265`, `281`); facilities carry no `short_name`, so they get `name`. |
| `country_code` | `str` | Yes | `country` | As sent: ISO-2, plus `GB*` for post-Brexit UK entries. |
| `entity_type` | `str` | Yes | `type` | `SSO` for companies; facilities carry `ASF`, `DSR`, `ASR`, `GRP` or `SRC` (meanings not documented in gridflow). A blank `type` becomes null (`_optional_text`, `endpoints.py:489-494`). |
| `entity_url` | `str` | Yes | `url` | |
| `company_code` | `str` | Yes | `company` | Facility-only. Parent company EIC. |
| `company_name` | `str` | Yes | derived | Facility-only. The `short_name` (else `name`) of the company entry the facility is listed under (`endpoints.py:265`, `291`). |
| `data_provider` | `str` | No | derived | Always `gie_agsi`. |
| `ingested_at` | `datetime[UTC]` | No | derived | Silver transform time, `datetime.now(UTC)` (`agsi.py:381`). |

`AboutListingTransformer._records_from_payload` builds each row from
the fields above only (`silver/gie/agsi.py:462-489`), so
`operational_start_date` and `operational_end_date`, present in the
live JSON, are not carried to silver. `about_summary` keeps them.

### Silver sample

```python
[
    {
        "entity_level": "company",
        "entity_code": "25X-GSALLC-----E",
        "entity_name": "GSA",
        "country_code": "AT",
        "entity_type": "SSO",
        "entity_url": "https://agsi.gie.eu/api?country=AT&company=25X-GSALLC-----E",
        "data_provider": "gie_agsi",
        "ingested_at": datetime(2026, 5, 8, 17, 40, tzinfo=UTC),
    },
    {
        "entity_level": "facility",
        "entity_code": "25W-SPHAID-GAZ-M",
        "entity_name": "UGS Haidach (GSA) // historical data prior to 6 Oct 2022",
        "country_code": "AT",
        "entity_type": "DSR",
        "entity_url": "https://agsi.gie.eu/api?country=AT&company=25X-GSALLC-----E&facility=25W-SPHAID-GAZ-M",
        "company_code": "25X-GSALLC-----E",
        "company_name": "GSA",
        "data_provider": "gie_agsi",
        "ingested_at": datetime(2026, 5, 8, 17, 40, tzinfo=UTC),
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- Lowercase `x-key` header. Capitalised `X-Key` returns 401.
- No `last_page` / `total` / pagination fields in live response — single
  list of 71 companies (as of 2026-05-08).
- All values in **GWh** at the `storage` endpoints; this dataset is
  reference-only and carries no numeric storage values.
- Rate limit: 60 calls/min (1 req/s).
- Live response is a top-level **list**, fixture is a `{"data": [...]}`
  envelope. Connector parser `_listing_rows` accepts either.
- Two query-string forms work: `?show=listing` (documented and used by
  registry) and concatenating into the path; both return the same body.
- `operational_end_date` indicates a facility no longer reports —
  useful filter for current-snapshot inventory.
- Some companies have `country` as ISO-2 string (`"AT"`); the connector
  inventory parser treats it as a string. No nested country object in
  this endpoint.

---

## Implementation delta

- **Live shape**: top-level list. Fixture: `{"data": [...]}` envelope.
  Connector handles both via `_listing_rows`. Fixture is technically
  stale relative to live but still functionally compatible (logged here,
  not regenerated in V1).
- **Endpoint path**: registry `path = "/api/about"` with
  `default_params = {"show": "listing"}`. Equivalent to
  `/api/about?show=listing`. No discrepancy.
- **Pagination params**: catalog YAML declares
  `pagination.params: []` and live response has no pagination fields —
  consistent.

No discrepancies found.

---

## Modelling notes

- **Use**: entity inventory for query planning and joining facility-level
  storage data to companies. Not a modelling input on its own.
- **Joins**: `storage_reports` on `entity_code` for facility-level
  attribution; on `company_code` to roll facility data up to companies.
- **Filters**: this table has no operational dates; use
  `about_summary`'s `operational_end_date` (not null → facility no
  longer reports) to exclude closed facilities.

---

## Links

- [Official API docs](https://agsi.gie.eu/api)
- `Python/gridflow/src/gridflow/connectors/gie/client.py`
- `Python/gridflow/src/gridflow/connectors/gie/endpoints.py`
- `Python/gridflow/src/gridflow/silver/gie/agsi.py`
- [Domain: gas day](../../../20-domain/concepts/gas-day.md)
