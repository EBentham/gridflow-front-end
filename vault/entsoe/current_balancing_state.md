---
source: entsoe
dataset_key: current_balancing_state
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
---

# ENTSO-E — Current balancing state (A86 / B33)

## Overview

ENTSO-E's definition (Transparency Platform knowledge base, "Current
Balancing State [GL EB 12.3.A]", updated 2025-08-26): the total
imbalance volume of an imbalance area, i.e. the open loop area control
error, averaged over each minute, in MW, with a state of Excess, Deficit
or Balanced. "Deficit is equivalent to negative imbalance while excess is
equivalent to positive imbalance" (GL EB article 54.6). Published with
minute resolution, 30 minutes after the end of the minute described;
updates are "not foreseen".

The response does not send a signed number. Each TimeSeries carries an
unsigned `quantity` (unit `MAW`) and a `flowDirection.direction`: ENTSO-E's
XML example labels `A01` Up, `A02` Down, `A03` Symmetric
(gitlab.entsoe.eu/transparency/xml-examples, "Current balancing state
[GL EB 12.3.A] - XSD4:1.xml"). Neither source says which direction is
excess and which is deficit. (Corrected 2026-09-29: this paragraph
previously said "positive = system short"; silver holds no signed value,
see Known issues.)

Document type **A86** is shared with `imbalance_volume`. The two
datasets distinguish themselves only by the `businessType` query
parameter — `B33` (this dataset; ENTSO-E's code list names it "Area control error")
versus `A19` (settled imbalance volumes, see
[imbalance_volume.md](./imbalance_volume.md)). Always specify
`businessType` when calling A86 or you will get an `Acknowledgement`
back with reason 999.

This is the dataset to use for: short-horizon imbalance forecasts,
real-time alerting on system stress, and as a feature in BM activation
likelihood models. Use [imbalance_volume.md](./imbalance_volume.md)
when you need the settled (after-the-fact) volume per settlement period.

→ Domain concepts:
  [Imbalance pricing](../../../20-domain/markets/imbalance-price.md)
  [Settlement period](../../../20-domain/concepts/settlement-period.md)

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://web-api.tp.entsoe.eu` |
| Path             | `/api` |
| Method           | GET |
| Auth             | Query param `securityToken=<ENTSOE_API_KEY>` (header auth NOT supported) |
| Rate limit       | Vendor-published: not documented. Project default: 1 req/s. ENTSOE rejects bursts even when calls are sequential — see `_throttle_request`. |
| Pagination       | None for A86. The endpoint returns one Balancing_MarketDocument per call. |
| Historical depth | TODO — H8 balancing extension catalogue went live progressively from 2022. GB control area has no published data (see EMPTY note below). |
| Publication lag  | Vendor deadline: 30 minutes after the end of the minute described; minute resolution (TP knowledge base, GL EB 12.3.A). |
| Response format  | XML (`Balancing_MarketDocument` urn:iec62325.351:tc57wg16:451-6) |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `documentType` | string (A-code) | Yes | Fixed `A86` | `A86` |
| `businessType` | string (B-code) | Yes | Fixed `B33` (current balancing state). Without this you get reason-999 even on data-rich areas — A86 is shared with imbalance_volume which uses `A19`. | `B33` |
| `area_Domain` | string (EIC) | Yes | Control area EIC. H8 spec uses `area_Domain` here, not `controlArea_Domain`. | `10YGB----------A` |
| `periodStart` | string (yyyyMMddHHmm UTC) | Yes | Window start, intra-day resolution. | `202605070000` |
| `periodEnd` | string (yyyyMMddHHmm UTC) | Yes | Window end, exclusive. gridflow sends one whole UTC day per call (`day_subwindows`, `connectors/entsoe/client.py:161-167`), e.g. `202608010000` to `202608020000`. | `202605071400` |
| `securityToken` | string (UUID) | Yes | API key from `ENTSOE_API_KEY`. | `<UUID>` |

ENTSOE tuple: `(documentType=A86, processType=n/a, businessType=B33, area-param-name=area_Domain)`.

### Working curl example

```bash
curl --ssl-no-revoke -fsS -H "Accept: application/xml" \
  "https://web-api.tp.entsoe.eu/api?documentType=A86&businessType=B33&area_Domain=10YGB----------A&periodStart=202605070000&periodEnd=202605071400&securityToken=${ENTSOE_API_KEY}" \
  -o /tmp/entsoe-current_balancing_state.xml \
  -w "HTTP %{http_code} | %{size_download} bytes\n"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsoe/current_balancing_state/<year>/<month>/<day>/raw_<uuid>.xml`
**Format**: Raw XML (`Balancing_MarketDocument`), as-received. Immutable — never modified after write.
**Granularity**: One file per (zone, UTC day). The connector loops `DEFAULT_ZONES` (GB, FR, NL, BE, DE-LU, IE-SEM; `endpoints.py:395`, `client.py:249`), so six files per day, including code-999 acknowledgements.

### Bronze sample

From `tests/fixtures/entsoe/current_balancing_state_gb.xml` (a hand-made fixture, not a vendor response). Real responses differ: `area_Domain.mRID` sits at document level, not in the TimeSeries; each TimeSeries carries `flowDirection.direction`, `quantity_Measure_Unit.name` `MAW` and `curveType` `A03`; the resolution is `PT1M`; quantities are unsigned (bronze FR/NL/BE responses for 1 to 5 Aug 2026, and ENTSO-E's XML example):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Balancing_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:balancingdocument:4:0">
  <mRID>fixture-current-balancing-state-gb-20240115</mRID>
  <revisionNumber>1</revisionNumber>
  <type>A86</type>
  <createdDateTime>2024-01-14T12:00:00Z</createdDateTime>
  <TimeSeries>
    <mRID>state-1</mRID>
    <businessType>B33</businessType>
    <area_Domain.mRID codingScheme="A01">10YGB----------A</area_Domain.mRID>
    <Period>
      <timeInterval>
        <start>2024-01-15T00:00Z</start>
        <end>2024-01-15T02:00Z</end>
      </timeInterval>
      <resolution>PT60M</resolution>
      <Point><position>1</position><quantity>125</quantity></Point>
      <Point><position>2</position><quantity>-75</quantity></Point>
    </Period>
  </TimeSeries>
</Balancing_MarketDocument>
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsoe/current_balancing_state/year=YYYY/month=MM/current_balancing_state_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsoe.h8_balancing.CurrentBalancingStateTransformer`
**Pydantic schema**: `gridflow.schemas.entsoe.EntsoeBalancingState`
**Dedup key**: `(timestamp_utc, area_code, business_type)`
**Point-in-time field**: `published_at`, the response's `createdDateTime`: a fetch-time stamp, within seconds of the request, not a vendor publication time (`silver/entsoe/_published_at.py`; ENTSO-E sets `createdDateTime` when it builds the response)

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `timestamp_utc` | `datetime[UTC]` | No | derived (Period.timeInterval.start + (position - 1) * resolution, `parsers.py:530`) | Validator rejects naive datetimes. `PT1M` is missing from `_RESOLUTION_MAP` (`parsers.py:35-43`), so `_resolve_resolution` falls back to one hour (`parsers.py:50-51`) and A03 forward-fill is skipped (`parsers.py:547-555`): every point after position 1 lands (position - 1) hours after its period start. |
| `area_code` | `str` | No | `area_Domain.mRID` | Renamed from `area_domain` by the transformer. The parser reads it only inside a TimeSeries (`parsers.py:302`); real A86 responses send it at document level, so it is empty on every silver row. |
| `quantity_mw` | `float` | No | `<quantity>` per Point | Unsigned magnitude in MW (`MAW`), as sent. The direction (`flowDirection.direction`) is parsed but not in `output_cols` (`silver/entsoe/h8_balancing.py:36-45`), so silver keeps no sign. |
| `business_type` | `str` | No | `<businessType>` | Default "B33" in canonical. Always `B33` for this dataset. |
| `resolution` | `str` | No | `<resolution>` (raw ISO duration) | Default "" in canonical. Emitted verbatim as the ISO-8601 duration code; `PT1M` in every response held (FR, NL, BE, 1 to 5 Aug 2026). |
| `published_at` | `datetime[UTC]` | Yes | root `createdDateTime` | Fetch-time stamp, within seconds of the request. |
| `data_provider` | `str` | No | derived | Default "entsoe" in canonical. |
| `ingested_at` | `datetime` | Yes | derived (now(UTC) at transform) | Nullable (datetime or None). |

### Silver sample

Derived from the hand-made fixture above, not from real silver. Real silver has an empty `area_code`, `PT1M`, unsigned values and a `published_at` column (see Known issues).

```python
[
    {
        "timestamp_utc": datetime(2024, 1, 15, 0, 0, tzinfo=UTC),
        "area_code": "10YGB----------A",
        "quantity_mw": 125.0,
        "business_type": "B33",
        "resolution": "PT60M",
        "data_provider": "entsoe",
        "ingested_at": datetime(2026, 5, 8, 18, 3, tzinfo=UTC),
    },
    {
        "timestamp_utc": datetime(2024, 1, 15, 1, 0, tzinfo=UTC),
        "area_code": "10YGB----------A",
        "quantity_mw": -75.0,
        "business_type": "B33",
        "resolution": "PT60M",
        "data_provider": "entsoe",
        "ingested_at": datetime(2026, 5, 8, 18, 3, tzinfo=UTC),
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **GB returns EMPTY.** Live curl on 2026-05-08 with `area_Domain=10YGB----------A` and a 14h window returns HTTP 200 with `Acknowledgement_MarketDocument` reason 999: `No matching data found for Data item CURRENT_BALANCING_STATE_R3 [12.3.A] (10YGB----------A)...`. ENTSOE has reduced GB-area coverage post-Brexit; National Grid ESO publishes equivalent data via Elexon BMRS instead. The whole-UTC-day calls for 1 to 5 Aug 2026 (fetched 2026-08-16) got the same code-999 answer for GB, DE-LU (`10Y1001A1001A82H`) and IE-SEM (`10Y1001A1001A59C`); FR, NL and BE returned data.
- **A86 + businessType is mandatory.** Submitting A86 without `businessType` returns reason 999. This is the same documentType used by `imbalance_volume` (with `businessType=A19`). Cross-link: see [imbalance_volume.md](./imbalance_volume.md).
- **Window length.** gridflow sends one whole UTC day per call, not an intra-day window, and whole-day calls fetched on 2026-08-16 for 1 to 5 Aug 2026 returned a full day of minutes for FR, NL and BE. Multi-day windows are untested here. (Corrected 2026-09-29: this bullet previously said an intra-day window is required.)
- **No DocStatus on TimeSeries.** Unlike outage feeds, A86 carries no per-TimeSeries status. Each TimeSeries has an `mRID` that is only a sequence number (`1`, `2`, ...); the document `mRID` and `revisionNumber` at the root are the only versioning artefacts.
- **Sign is a direction code, not a signed number.** ENTSO-E defines deficit as negative imbalance and excess as positive (GL EB 54.6), but the response sends unsigned quantities with `flowDirection.direction` `A01` (Up) or `A02` (Down), and no vendor source held here maps Up/Down to excess/deficit. Do not borrow `imbalance_volume`'s `A01` long / `A02` short mapping without evidence.
- **Silver is not usable as built (gridflow defect, found 2026-09-29).** Three parser/transformer gaps compound: (1) `area_Domain.mRID` is read only inside a TimeSeries (`parsers.py:302`), so `area_code` is empty on every row; (2) `flow_direction` is dropped (`h8_balancing.py:36-45`), so the sign is lost; (3) `PT1M` is unmapped (`parsers.py:35-43`, fallback one hour at `:50-51`), so point times are spread hours apart and A03 forward-fill is skipped. The dedup on `(timestamp_utc, area_code, business_type)` with `keep="last"` then collapses FR, NL, BE and both directions into one row per timestamp: 14,880 parsed points for 1 to 5 Aug 2026 become 9,414 silver rows, with timestamps running to 25 Aug. Needs a gridflow fix and a re-transform before any page or model uses this table.

---

## Implementation delta

- **Area parameter:** docs/code use `area_Domain`, **not** `controlArea_Domain` as suggested in the V1-PLAN-B4 orchestrator instructions. The H8 balancing extension spec (Article 12.3 of GL EB) uses `area_Domain` for A86/A24/A15. The fixture file at `tests/fixtures/entsoe/current_balancing_state_gb.xml` confirms this — the response carries `<area_Domain.mRID>`. The orchestrator instruction was incorrect; code is right.
- **A86 dual mapping:** This dataset shares documentType A86 with `imbalance_volume` — they differ only by `businessType` (B33 here, A19 there). See [imbalance_volume.md](./imbalance_volume.md) for the settled-volume counterpart.
- **`processType` not specified:** A86/B33 has no `processType` in `endpoints.py` (`process_type=None`). The ENTSOE API guide does not list a process type for B33. Confirmed by successful live (HTTP 200) call without `processType`.
- **`controlArea_Domain` mention in entsoe README:** The current vendor README does not yet document the H8 area_Domain pattern. Will be addressed by the V1-PLAN-B5 aggregate plan.

---

## Modelling notes

- Useful as a **leading indicator** for imbalance price direction. Models that predict period-end imbalance volume / price benefit from A86 features sampled at minute resolution within the period.
- Use as a feature for: BM activation likelihood, imbalance price short-horizon regression, NIV (Net Imbalance Volume) nowcast.
- Caveat for GB: since GB returns EMPTY here, equivalent data must be sourced from Elexon (`freq`, `disbsad`, `imbalngc` family). Cross-area comparisons require pulling from EU-country control areas where A86/B33 is published (e.g. FR, NL, BE; DE-LU returned code 999 for 1 to 5 Aug 2026).

---

## Links

- [Official API docs](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.pdf) — Section 17 (Balancing) and 12.3.A
- [TP knowledge base: Current Balancing State [GL EB 12.3.A]](https://transparencyplatform.zendesk.com/hc/en-us/articles/12824861339924-Current-Balancing-State-GL-EB-12-3-A): definition, unit, excess/deficit wording, deadline
- [ENTSO-E XML example](https://gitlab.entsoe.eu/transparency/xml-examples/-/blob/main/Balancing/Current%20balancing%20state%20[GL%20EB%2012.3.A]%20-%20XSD4:1.xml): `B33` Area control error; `A01` Up, `A02` Down, `A03` Symmetric
- `src/gridflow/connectors/entsoe/client.py`
- `src/gridflow/connectors/entsoe/endpoints.py` — see `current_balancing_state` entry
- `src/gridflow/silver/entsoe/h8_balancing.py`
- `src/gridflow/schemas/entsoe.py` — `EntsoeBalancingState`
- `tests/fixtures/entsoe/current_balancing_state_gb.xml`
- [Imbalance volume (A86 / A19)](./imbalance_volume.md)
