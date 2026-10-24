---
source: gie_agsi
dataset_key: unavailability
vendor: GIE AGSI+ (Gas Storage)
last_verified: 2026-10-24
layer_coverage: bronze, silver
page:
  title: Gas storage outage notices
  summary: >-
    GIE AGSI+ storage outage notices: each facility's injection and withdrawal figures, its window
    and every publication, filed by calendar day.
  facts:
    vendor: "GIE AGSI+, the `/api/unavailability` endpoint"
    cadence: As operators publish notices
    grain: One row per publication and calendar day it overlaps
  landscape: gas
  caveat: GIE states no time zone for these stamps, so they are kept as sent.
  what_it_is: >-
    An operator's notice reports an outage at a storage facility from a start to an end;
    gridflow reads `injection` and `withdrawal` as the capacity lost. GIE sends no notice id, so
    every publication is its own row, keyed on the whole record. Each is filed under every
    calendar day its window overlaps (`outage_date`): a 06:00 to 06:00 notice appears twice.
  how_used:
    - Facility outages by day, as inputs to short-term injection and withdrawal limits.
    - "Point-in-time features: notices published before the forecast, allowing for unknown time zones."
    - Joining `facility_eic` to the AGSI facility register for operator and country.
  chart:
    type: bar
    silver: gie_agsi/unavailability
    value: withdrawal
    filter:
      - {column: outage_date, op: ge, value: "2026-08-01"}
      - {column: outage_date, op: le, value: "2026-08-05"}
      - {column: withdrawal, op: gt, value: 0}
    group: facility_eic
    group_map:
      "21W000000000084S": saline
      "63W197197128864M": serene_atlantique
      "21W0000000000702": sediane_b
      "21W0000000000087": bergermeer
      "21W000000000073X": serene_nord
      "16ZAS01\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D8": carrico
    aggregation: max
    sort: value_desc
    unit: "withdrawal, no unit stated"
  chart_view:
    title: Highest withdrawal figure per facility, 1 to 5 August 2026
    caption: >-
      Silver `gie_agsi/unavailability`: the highest `withdrawal` in any of each facility's notices
      overlapping 1 to 5 August 2026. The response labels no unit, so bars across operators may
      not compare. All-zero facilities are left out.
    alt: >-
      Horizontal bar chart from gie_agsi/unavailability of the highest withdrawal figure in each
      facility's notices overlapping 1 to 5 August 2026, no unit stated: VGS Saline 304.4, VGS
      Serene Atlantique 270.5, VGS Sediane B 167.5, UGS Bergermeer 108, VGS Serene Nord 89 and UGS
      Carriço 85.7.
    key:
      - {series: saline, label: Saline, codes: 21W000000000084S, paint: clay}
      - {series: serene_atlantique, label: Serene Atlantique, codes: 63W197197128864M, paint: clay}
      - {series: sediane_b, label: Sediane B, codes: 21W0000000000702, paint: clay}
      - {series: bergermeer, label: Bergermeer, codes: 21W0000000000087, paint: clay, note: "The only unplanned notice charted, described as `Gas treatment plant unavailability`."}
      - {series: serene_nord, label: Serene Nord, codes: 21W000000000073X, paint: clay}
      - {series: carrico, label: Carriço, codes: "16ZAS01\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D8", paint: clay}
  raw_feed:
    note: >-
      One query for the window, fetched page by page to the response's `last_page`, 30 notices a
      page, key in the `x-key` header. Country, company and facility arrive nested.
    requests:
      - "GET https://agsi.gie.eu/api/unavailability?start=2026-08-01&end=2026-08-06&page=1"
    commands:
      - {run: gridflow ingest gie_agsi unavailability --start 2026-08-01 --end 2026-08-06, comment: "bronze; both dates sent as given"}
      - {run: gridflow transform gie_agsi unavailability --start 2026-08-01 --end 2026-08-05, comment: one file per calendar day}
  record:
    select:
      filter:
        - {column: facility_eic, op: eq, value: 21W000000000015A}
        - {column: outage_date, op: le, value: "2026-08-04"}
      order_by: [outage_date, start, published]
      columns: [outage_date, facility_name, published, start, end, injection, withdrawal, end_flag, type, description, volume]
    key: [outage_date, country_code, country_name, company_eic, company_name, facility_eic, facility_name, published, start, end, type, end_flag, volume, injection, withdrawal, description]
    caption: "UGS Norg on 3 and 4 August 2026; each publication is its own row."
    fields:
      outage_date: "Calendar day the notice's window overlaps; a 06:00 to 06:00 window falls on two"
      facility_name: "Facility name, the `name` in GIE's `facility` object"
      published: "When this notice was published, as sent; no time zone; can follow the window"
      start: "Window start, as sent; gridflow reads the reporters as mixing UTC and local time"
      end: "Window end, as sent; later publications move it out to 6 August, then back"
      injection: "Injection figure in the notice, read as capacity lost; the response labels no unit"
      withdrawal: "Withdrawal figure in the notice, read as capacity lost; the response labels no unit"
      end_flag: "Whether the end is `Confirmed` or an `Estimate`, as sent"
      type: "`Planned` or `Unplanned`, as sent"
      description: "The operator's free text, as sent"
      volume: "Vendor `volume`, as sent; meaning and unit not stated; 0 in these rows"
      country_code: "Country code, the `code` in GIE's `country` object"
      country_name: "Country name, the `name` in GIE's `country` object"
      company_eic: "Operator's EIC, the `eic` in GIE's `company` object"
      company_name: "Operator name, the `name` in GIE's `company` object"
      facility_eic: "Facility EIC, the `eic` in GIE's `facility` object; joins the facility register"
  notebook:
    source: gie_agsi
    lead: >-
      These cells use `data.sql()` on `silver_gie_agsi_unavailability` to name the columns and sort
      each day's notices; `query()` orders rows by its date column only. Both window ends are
      included.
    cells:
      - |
        df = data.sql("""
            SELECT outage_date, country_code, facility_name, published, start, "end",
                   type, end_flag, injection, withdrawal, description
            FROM silver_gie_agsi_unavailability
            WHERE outage_date BETWEEN '2026-08-01' AND '2026-08-05'
            ORDER BY outage_date, facility_name, published
        """)
      - df[["outage_date", "country_code", "start", "end", "injection", "withdrawal"]].head()
      - |
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        u = df.loc[df.type == "Unplanned", df.columns[1:]].drop_duplicates()
        u = u.assign(site=u.facility_name.str.split(" (", regex=False).str[0])
        fig, ax = plt.subplots(figsize=(8, 3.5))
        ax.hlines(u.site, u.start, u["end"], lw=6, color="#155A6E", alpha=0.5)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
        ax.set_xlabel("outage window, as sent (no time zone)");
    needs: 1 to 5 August 2026
    plot_alt: >-
      Timeline of the unplanned notices, one bar per notice from start to end, not scaled by
      capacity; later publications overlap and darken. Bergermeer runs 4 to 9 August. Norg and Grijpskerk
      have short bars on 3 August and longer ones from 4 into 6 August. Wierzchowice sits on 2
      August, GIM Sanok on 1 August.
  related:
    - {dataset: gie/about_listing, note: "The facility register; its `entity_code` matches `facility_eic` here"}
    - {dataset: gie/storage, note: "Country storage stock, injection and withdrawal to read outages against"}
    - {dataset: elexon/remit, note: "GB power-unit outage messages, where gridflow also keeps every publication"}
---

# GIE AGSI+ — Unavailability (storage outage and maintenance reports)

## Overview

`unavailability` returns AGSI's storage-outage / planned-maintenance
records — per-event entries with `start` / `end` windows, affected
country / company / facility, a `volume` (meaning not stated), `injection` /
`withdrawal` figures (read by gridflow as the capacity lost; no GIE
definition is quoted here), a free-text `description`, and a
`type` (`Planned`, `Unplanned`, ...).

The dataset answers: "Which AGSI storage facilities are out, when, and
how much capacity is missing?", where "how much" is gridflow's reading of
the `injection` / `withdrawal` figures as capacity lost (GIE gives no
definition in the response) — a critical input for short-term
withdrawal-capacity forecasts, fundamental gas-spread trades, and
explaining sudden capacity reductions in `storage_reports` /
`storage`.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://agsi.gie.eu` |
| Path             | `/api/unavailability` |
| Method           | GET |
| Auth             | header `x-key` (lowercase), key from env `GIE_API_KEY` |
| Rate limit       | 60 calls/minute. The connector keeps one request in flight at a time (`rate_limit_per_second: 1` in `config/sources.yaml` sizes a semaphore, `connectors/base.py:195`); it adds no delay, and the August 2026 capture's pages were fetched about 0.1 s apart (corrected 2026-10-24). |
| Pagination       | `last_page` is the source of truth; `total` is the per-page row count. Iterate `page=1..last_page` (`client.py:318-357`). `last_page` can run past the last record: in the 16 August 2026 fetch for 1 to 6 August, `last_page` was 16, page 12 held 11 records and page 16 answered `{"last_page":16,"total":0,"dataset":"No data found","data":[]}`; pages 13 to 15 left no file of their own and must have returned the same body (see Bronze, File names) (added 2026-10-24). |
| Historical depth | All visible AGSI unavailability records (typically multi-year). |
| Publication lag  | Real-time when operators report. `published` field per record. |
| Response format  | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `country` | str | No | ISO-2 country code. Filters by affected country. | `country=DE` |
| `company` | str | No | Company EIC. | `company=21X0000000011756` |
| `facility` | str | No | Facility EIC. | `facility=37W000000000002O` |
| `start` | str (YYYY-MM-DD) | No | Range start. **Used by the connector and registry**. | `start=2026-04-01` |
| `end` | str (YYYY-MM-DD) | No | Range end (inclusive). | `end=2026-05-07` |
| `from` | str (YYYY-MM-DD) | No | Alternate range start. Live API also accepts this — produces a different `last_page`. | `from=2026-04-01` |
| `to` | str (YYYY-MM-DD) | No | Alternate range end. | `to=2026-05-07` |
| `page` | int | No | Page number, 1-indexed. | `page=2` |
| `size` | int | No | Page size. Default 30, max 300. | `size=300` |

### Working curl example

```bash
# Replace <KEY> with $GIE_API_KEY
curl --ssl-no-revoke -X GET \
  "https://agsi.gie.eu/api/unavailability?country=DE&start=2026-04-01&end=2026-05-07" \
  -H "x-key: <KEY>"
```

Live response (DE, 2026-05-08): HTTP 200, ~14 KB,
`{"last_page": 7, "total": 30, "data": [30 records]}`.

GB returned `{"last_page": 1, "total": 0, "data": []}` — empty by
design (no UK storage outages reported on AGSI).

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/gie_agsi/unavailability/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON. Immutable.
**Granularity**: One file per page of one request window; the connector sends no `country`, only `start`, `end` and `page` (`client.py:247-256`), and files every page under the window's start day (`data_date=start.date()`, `client.py:262`). Corrected 2026-10-24.
**File names**: `raw_<fetch second>_<first 8 hex of the body's SHA-256>.json` (`bronze/writer.py:51-75`), so byte-identical pages fetched in the same second share one file and one sidecar, the last page written winning. The August 2026 capture (fetched 16 August 2026, request `start=2026-08-01&end=2026-08-06`) is 13 files for GIE's 16 pages for that reason: pages 13 to 16 were fetched within 14:18:13 UTC and left one file between them, with page 16's sidecar and its empty body. Pages 13 to 15 must have returned that same body: only five files exist from that second, the other four still carry the sidecars of pages 9 to 12, and a later page with a colliding body would have overwritten one of them. So no page holding records was overwritten; pages 1 to 12 hold all the records (added 2026-10-24).

### Bronze sample

Live (DE, page 1):

```json
{
  "last_page": 7,
  "total": 30,
  "dataset": "<a href=\"/unavailability/gantt/DE\">Germany</a>",
  "data": [
    {
      "published": "2026-05-08 10:40:07",
      "country": {"name": "Germany", "code": "DE"},
      "company": {"name": "EWE Gasspeicher", "eic": "21X0000000011756"},
      "facility": {"name": "EWE H-Gas Zone", "eic": "37W000000000002O"},
      "start": "2026-05-04 06:00:00",
      "end": "2026-05-08 12:00:00",
      "volume": "3.004",
      "injection": "41.4",
      "withdrawal": "82.8",
      "description": "safety test / maintenance work (only Huntorf is influenced)",
      "end_flag": "Confirmed",
      "type": "Planned"
    }
  ]
}
```

GB (empty):

```json
{
  "last_page": 1,
  "total": 0,
  "dataset": "<a href=\"/unavailability/gantt/GB\">United Kingdom (Pre-Brexit)</a>",
  "data": []
}
```

Note that the docs (v007 PDF) are ambiguous about whether
`unavailability` is part of the AGSI API surface — the catalog YAML
notes "documentation wording is ambiguous about unavailability API
coverage." The endpoint is live-served and well-formed.

---

## Silver layer

**Path pattern**: `{data_root}/silver/gie_agsi/unavailability/year=YYYY/month=MM/unavailability_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.gie.agsi.UnavailabilityTransformer`
**Pydantic schema**: `gridflow.schemas.gie.GasStorageUnavailability` (`schemas/gie.py:50`). `DATASET_VERSION` 2.0.0 (`agsi.py:543`).
**Grain**: one row per vendor notice per calendar day its window overlaps. `read_bronze` keeps a record for target day D when `[start, end)` overlaps `[D 00:00, D+1 00:00)` on the stamps' own clock; a date-only end covers its whole day; a record with no parseable bound is kept with a warning, never dropped (`_classify_unavailability_record`, `agsi.py:813-855`; `_unavailability_bound`, `agsi.py:857-884`). D is written to `outage_date`. A notice running 06:00 to 06:00 (as Storengy's French notices do) therefore appears on two calendar days.
**Bronze read for day D**: the files in D's bronze folder, else every bronze file whose request window (`start` to `end`, both included) contains D (`agsi.py:654-663`, `987-996`). One request's pages therefore feed every day of its window.
**Dedup key**: the whole vendor record plus the day, `ENTITY_KEY_COLUMNS` (`agsi.py:550-567`): `outage_date`, `country_code`, `country_name`, `company_eic`, `company_name`, `facility_eic`, `facility_name`, `published`, `start`, `end`, `type`, `end_flag`, `volume`, `injection`, `withdrawal`, `description`. Exact repeats are dropped on the vendor strings before typing (`agsi.py:619`). GIE sends no notice id, so the key is the whole record. The notice window and publication alone are not unique: the injection and withdrawal notices of one event can share facility, window and publication (UGS Carriço, 5 August 2026). Every publication is kept, so a later publication for the same facility and window (read by gridflow as a revision) sits beside the earlier one. Corrected 2026-10-24 (gridflow PR #133).
**Point-in-time field**: `published`, a naive datetime: GIE states no time zone (see Known issues).

### Silver schema

Typed explicitly (`_UNAVAILABILITY_SILVER_SCHEMA`, `agsi.py:906-917`); the nested `country`, `company` and `facility` objects are flattened to code and name columns (`_flatten_unavailability_record`, `agsi.py:919-967`). Corrected 2026-10-24.

| Field | Polars type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `outage_date` | `Date` | No | derived | The calendar day the notice's window overlaps (the partition day). The date column `query()` filters on (`schema_manifest.py:237`). |
| `country_code` | `String` | Yes | `country.code` | ISO-2 code. |
| `country_name` | `String` | Yes | `country.name` | |
| `company_eic` | `String` | Yes | `company.eic` | Operator EIC. |
| `company_name` | `String` | Yes | `company.name` | |
| `facility_eic` | `String` | Yes | `facility.eic` | Matches `entity_code` in `about_listing` (all 12 facilities of the August 2026 capture). |
| `facility_name` | `String` | Yes | `facility.name` | As sent, including GIE's spelling and punctuation. |
| `published` | `Datetime(us)`, naive | Yes | `published` | Vendor publish time, `"YYYY-MM-DD HH:MM:SS"`, parsed with no zone (`_naive_wall_clock`, `agsi.py:970-984`). |
| `start` | `Datetime(us)`, naive | Yes | `start` | Outage window start, same parsing. |
| `end` | `Datetime(us)`, naive | Yes | `end` | Outage window end; `end_flag` says whether it is confirmed or estimated. |
| `type` | `String` | Yes | `type` | `Planned`, `Unplanned`. |
| `end_flag` | `String` | Yes | `end_flag` | `Confirmed`, `Estimate`. |
| `volume` | `Float64` | Yes | `volume` | The response labels no unit, and its meaning is not stated. |
| `injection` | `Float64` | Yes | `injection` | Injection figure; gridflow reads it as the capacity lost (field name only, no GIE definition quoted). The response labels no unit. |
| `withdrawal` | `Float64` | Yes | `withdrawal` | Withdrawal figure; gridflow reads it as the capacity lost (field name only, no GIE definition quoted). The response labels no unit. |
| `description` | `String` | Yes | `description` | Free text from the operator. |
| `data_provider` | `String` | No | derived | Always `gie_agsi`. |
| `ingested_at` | `Datetime(us, UTC)` | No | derived | Silver transform time (`datetime.now(UTC)`, `agsi.py:632`), not the bronze fetch. |

Silver also carries the pipeline columns `event_time` (the partition day at 00:00 UTC),
`available_at`, `source_run_id` and `dataset_version` (`silver/base.py`).

### Silver sample

One notice of the August 2026 capture as silver holds it on `outage_date` 2026-08-03 (lineage
columns left out):

```python
[
    {
        "outage_date": date(2026, 8, 3),
        "country_code": "NL",
        "country_name": "Netherlands",
        "company_eic": "21X000000001075A",
        "company_name": "NAM",
        "facility_eic": "21W000000000015A",
        "facility_name": "UGS Norg (Langelo) L-gas",
        "published": datetime(2026, 8, 4, 0, 19, 32),
        "start": datetime(2026, 8, 3, 12, 0),
        "end": datetime(2026, 8, 3, 23, 0),
        "type": "Unplanned",
        "end_flag": "Confirmed",
        "volume": 0.0,
        "injection": 257.0,
        "withdrawal": 0.0,
        "description": "Partial unavailability due to weather conditions.",
        "data_provider": "gie_agsi",
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- Lowercase `x-key` header. Capitalised `X-Key` returns 401.
- `last_page` is the pagination source of truth (not `total`).
  `total` is the per-page row count.
- **Units are not stated.** The response labels no unit for `volume`,
  `injection` or `withdrawal`, and gridflow assigns none
  (`schemas/gie.py:50-58`). The earlier "GWh / GWh/day per docs" line
  quoted no GIE text and is withdrawn (corrected 2026-10-24).
- Rate limit: 60 calls/min; the connector keeps one request in flight
  and adds no delay (see API endpoint).
- GB returns zero rows by design (no UK storage outages reported on
  AGSI). Only post-Brexit GB rows are sparse anyway.
- `country`, `company`, `facility` arrive as nested objects
  (`{"name": ..., "code": ...}` or `{"name": ..., "eic": ...}`); silver
  flattens them to `<object>_code` / `<object>_eic` and `<object>_name`
  columns (`agsi.py:919-967`).
- **No notice id.** GIE sends no identifier linking a revised notice to
  the one it supersedes; silver keeps every publication as its own row.
- **No time zone.** `start` / `end` / `published` arrive as
  `YYYY-MM-DD HH:MM:SS` with no time zone stated. Silver parses them to
  naive datetimes and never converts them, because the reporters appear
  to mix clocks: per the transformer's docstring, Austrian and Dutch
  stamps move between 04:00 and 05:00 with summer time, so they read as
  UTC, while French ones sit at 06:00 all year, so they read as local
  time (`agsi.py:598-616`). This is gridflow's reading of the stamps,
  not a GIE statement. The overlap test compares the naive stamps with
  the calendar day as they are, so a notice near midnight may fall on a
  different `outage_date` than its true UTC day.
- **Two calendar days per gas-day notice.** A notice running 06:00 to
  06:00 overlaps two calendar days and appears on both `outage_date`s.
  Summing a column over a day's rows therefore counts such notices, and
  every superseded publication, more than once.
- `gridflow_models` `query("unavailability", ...)` filters on
  `outage_date` (`silver/schema_manifest.py:237`; corrected 2026-10-24).
- The catalog YAML notes documentation ambiguity (v007 PDF wording
  about whether `unavailability` is part of the AGSI API).

---

## Implementation delta

- **v007 documentation ambiguity**: the GIE
  `GIE_API_documentation_v007.pdf` reviewer-cross-check (per
  `docs/gie_agsi_endpoint_catalog.yaml`) leaves it unclear whether
  `/api/unavailability` is fully part of the AGSI API or a separate
  legacy/portal-only feature. The endpoint is live-served and returns
  well-formed JSON; the catalog YAML says: "Marked active because the
  endpoint is documented and live-served, though documentation wording
  is ambiguous about unavailability API coverage." This dataset page
  treats it as active per the live-validation pass on 2026-05-08.
- **Date param naming**: registry uses `start` / `end` for the date
  range (matches catalog `date_params.range: [start, end]`). The
  live API **also** accepts `from` / `to` and produces a slightly
  different filter result (different `last_page`). The connector's
  registry choice (`start` / `end`) returns matching data — no fix
  needed, but the alternative form exists.
- **Field shapes vs fixture**: the fixture
  (`tests/fixtures/gie/agsi_unavailability_response.json`) now holds
  live-shaped records: nested `country`/`company`/`facility` objects,
  `start`/`end`, `volume`/`injection`/`withdrawal` (gridflow PR #133).
  The older flat shape (`country: "DE"`, `eventStart`/`eventEnd`) is
  still accepted (its `unavailableCapacity` is not read): the flattener reads a bare
  string as the code or EIC (`agsi.py:944-948`), and the overlap
  classifier and flattener accept both bound spellings
  (`_UNAVAILABILITY_START_KEYS` / `_END_KEYS`, `agsi.py:809-810`).
  `volume`, `injection` and `withdrawal` are cast to `Float64` by name
  (`agsi.py:628-630`). Corrected 2026-10-24.

No connector-behaviour discrepancies found.

---

## Modelling notes

- **Models**: short-term withdrawal-capacity forecasts, fundamental
  gas-spread trades, explanatory features for sudden country-level
  capacity drops.
- **Targets**: `withdrawal` and `injection` (read by gridflow as the
  capacity lost during the outage; no GIE definition quoted; unit not
  stated). Before summing across facilities, keep
  one publication per event and one row per notice, not per
  `outage_date`.
- **Features**: type (planned vs unplanned), end_flag (confirmed vs
  estimate), event duration.
- **Joins**: `about_listing.entity_code` ↔ `unavailability.facility_eic`
  for the operator and facility register (all 12 facilities of the
  August 2026 capture match); `unavailability.country_code` ↔
  `storage.country_code` for country rollup. `storage_reports` is the EU
  aggregate in gridflow, not facility level (corrected 2026-10-24).

---

## Links

- [Official API docs](https://agsi.gie.eu/api)
- `Python/gridflow/src/gridflow/connectors/gie/client.py`
- `Python/gridflow/src/gridflow/connectors/gie/endpoints.py`
- `Python/gridflow/src/gridflow/silver/gie/agsi.py`
- [Domain: gas day](../../../20-domain/concepts/gas-day.md)
