---
source: entsog
dataset_key: aggregate_interconnections
vendor: ENTSOG Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
---

# ENTSOG — Aggregate Interconnections

## Overview

Aggregate connections between TSOs and balancing zones (zone-level summary).

This is a reference / inventory dataset — no time dimension, but
inventory does change weekly when ENTSOG approves new operators or points.
The connector schedule is `weekly` in `config/sources.yaml`.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://transparency.entsog.eu/api/v1` |
| Path             | `/aggregateInterconnections` |
| Method           | GET |
| Auth             | None (public) |
| Rate limit       | Not vendor-published; project default 5 req/s |
| Pagination       | `limit` + `offset` — pagination is REQUIRED for full inventory; iterate offsets until `count < limit` or fall back to `limit=-1` for a single all-records pull |
| Historical depth | n/a (snapshot) |
| Publication lag  | Vendor inventory updates daily |
| Response format  | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `limit` | int | Yes | Page size; `-1` returns all | `1000` |
| `offset` | int | No | Page offset (0-based) | `0` |
| `countryKey` | str | No | Restrict to a country | `UK` |

### Working curl example

```bash
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://transparency.entsog.eu/api/v1/aggregateInterconnections?limit=100&offset=0&countryKey=UK"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsog/aggregate_interconnections/<year>/<month>/<day>/raw_<uuid>.json` (one snapshot per weekly schedule)
**Format**: Raw JSON, as-received. Immutable.
**Granularity**: One file per fetch call (full inventory).

### Bronze sample

```json
{
  "meta": {
    "limit": 100,
    "offset": 0,
    "count": 27,
    "total": 27
  },
  "aggregateInterconnections": [
    {
      "countryKey": "UK",
      "countryLabel": "United Kingdom",
      "bzKey": "UK---------",
      "bzLabel": "UK",
      "bzLabelLong": "British Balancing Zone",
      "operatorKey": "IE-TSO-0001",
      "operatorLabel": "GNI (UK) Ltd.",
      "directionKey": "entry",
      "adjacentSystemsKey": "TransmissionUK-NI------",
      "adjacentSystemsCount": "1",
      "adjacentSystemsAreBalancingZones": null,
      "adjacentSystemsLabel": "NI",
      "id": "6UKUK---------IE-TSO-0001entryTransmissionUK-NI------",
      "dataSet": "6"
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsog/aggregate_interconnections/aggregate_interconnections.parquet` (CORRECTED 2026-10-07: `silver/base.py:834` gives each dataset its own folder; `generic.py:284` writes the file there) (single-file overwrite — `reference_dataset=True`)
**Transformer class**: `gridflow.silver.entsog.generic.GenericEntsogJsonTransformer (subclass AggregateInterconnectionsTransformer)`
**Pydantic schema**: Generic — no Pydantic schema declared
**Dedup key** (CORRECTED 2026-10-07): vendor `id`, keep last (`silver/entsog/generic.py:193-199`); every record of this register carries one (the `dataSet` digit then the natural key). Without `id` the subset would be every column but `timestamp_utc`. Silver reads only the newest bronze capture (`generic.py:112-116,128-129,252-259`), so no capture is repeated.
**Point-in-time field**: **none — CORRECTED 2026-08-13.** The live payload
carries **no date or time field of any kind** — all 14 fields checked, no
`lastUpdateDateTime`, no near-miss. Live-probe verified 2026-08-04
(`/aggregateInterconnections?limit=3&offset=0&countryKey=UK`); evidence:
gridflow
`.planning/phases/R3-test-integrity/probes/entsog_aggregate_interconnections.json`.
> **⚠ Consequence (gridflow unit N-17, hazard confirmed LIVE):** every silver
> row is stamped `event_time = target_date` — the pipeline's run date, not a
> vendor instant. Unfixed; T2 unit.

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| country_key | str | Yes | countryKey |  |
| country_label | str | Yes | countryLabel |  |
| bz_key | str | Yes | bzKey |  |
| bz_label | str | Yes | bzLabel |  |
| bz_label_long | str | Yes | bzLabelLong |  |
| operator_key | str | Yes | operatorKey |  |
| operator_label | str | Yes | operatorLabel |  |
| direction_key | str | Yes | directionKey |  |
| adjacent_systems_key | str | Yes | adjacentSystemsKey |  |
| adjacent_systems_count | float | Yes | adjacentSystemsCount |  |
| adjacent_systems_are_balancing_zones | null (sent null) | Yes | adjacentSystemsAreBalancingZones |  |
| adjacent_systems_label | str | Yes | adjacentSystemsLabel |  |
| id | str | int | Yes | id |  |
| data_set | str | int | Yes | dataSet |  |
| data_provider | str | No | derived | Always `entsog` |
| ingested_at | datetime[UTC] | No | derived | Wall-clock at silver write |
| event_time, available_at, source_run_id, dataset_version | lineage | No | derived | Pipeline lineage columns (`silver/base.py`); row added 2026-10-07 |

### Silver sample

```python
[
    {
        "country_key": "UK",
        "country_label": "United Kingdom",
        "bz_key": "UK---------",
        "bz_label": "UK",
        "bz_label_long": "British Balancing Zone",
        "operator_key": "IE-TSO-0001",
        "operator_label": "GNI (UK) Ltd.",
        "direction_key": "entry",
        "adjacent_systems_key": "TransmissionUK-NI------",
        "adjacent_systems_count": "1",
        "adjacent_systems_are_balancing_zones": null,
        "adjacent_systems_label": "NI",
        "id": "6UKUK---------IE-TSO-0001entryTransmissionUK-NI------",
        "data_set": "6",
        "data_provider": "entsog",
        "ingested_at": "2026-05-08T18:00:00+00:00"
    }
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **No date filter — pagination required**: reference endpoints accept `limit` + `offset`. Default `limit` is small; pass `limit=1000` (or the full inventory size) and iterate offset for full extracts.
- **`hasData=1`** (CORRECTED 2026-10-07): ENTSOG's API manual (v2.1, section 2.4.7) documents it for operator point directions only: it keeps the directions of TSOs that publish their REG715 data. gridflow also sends it to `/operators`, where the manual does not document it; the 27 Sep 2026 response still lists storage, LNG, hydrogen and electricity operators. The claim that it drops dormant validity-period rows is unverified.
- **Field-case duplicates**: `isCAMRelevant` (uppercase CAM) appears here while `isCamRelevant` appears in operationalData. Generic silver coalesces both into `is_cam_relevant`.
- **Reference data refresh schedule**: weekly in `config/sources.yaml`. Static-ish, but new points and operator changes do appear when ENTSOG approves them.
- **`bzKey` separators**: balancing zone keys often contain trailing dashes (`UK---------`) — preserve as-is, do not strip.


---

## Implementation delta

- **Pagination required**: full inventory may exceed default page size. Connector defaults to `limit=-1`; live validation used `limit=100` to demonstrate paging shape. For production fetches, prefer `limit=-1` or iterate `offset` in chunks.
- **`reference_dataset=True` write path**: silver writes directly to `<silver_dir>/<dataset>.parquet`, bypassing the date-partitioned layout used by operational datasets.

---

## Modelling notes

TODO — primarily used as join keys for operational datasets.

---

## Links

- [Official API docs (PDF)](https://transparency.entsog.eu/api/archiveDirectories/8/api-manual/TP_REG715_Documentation_TP_API%20-%20v2.1.pdf)
- `src/gridflow/connectors/entsog/endpoints.py`
- `src/gridflow/silver/entsog/generic.py`
- `src/gridflow/schemas/entsog.py`
- Gold view/builder
