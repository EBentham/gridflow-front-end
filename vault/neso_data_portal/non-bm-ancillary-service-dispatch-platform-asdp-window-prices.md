---
source: "neso_data_portal"
package: "non-bm-ancillary-service-dispatch-platform-asdp-window-prices"
dataset_key: "asdp_window_prices"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-13
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: ASDP window prices
  summary: >-
    Price changes that Non-BM reserve providers sent to NESO's dispatch platform, ASDP, for
    settlement windows in 2025 and 2026.
  facts:
    vendor: "NESO Data Portal: two datastore tables, one per calendar year"
    cadence: "NESO lists it as not active: the services moved to its Open Balancing Platform"
    grain: One row per window-price change a provider sent
  landscape: market
  what_it_is: >-
    Providers of Non-BM STOR and Fast Reserve (outside the Balancing Mechanism) told NESO a price for
    each settlement window through its dispatch platform, ASDP. Each row gives provider, asset,
    service, window, price and creation time. `EntryID` points to the instruction table but repeats,
    so it identifies no row. The Open Balancing Platform (OBP) uses other ids: never join the two.
  how_used:
    - Which assets and providers offered Non-BM Fast Reserve and STOR through ASDP
    - How often each asset changed its window price
    - How each provider's window prices moved, day to day and month to month
  chart:
    type: line
    silver: neso_data_portal/asdp_window_prices
    time: sp_start_date_time
    time_text: {format: "%Y-%m-%dT%H:%M:%S"}
    filter:
      - {column: service_type, op: eq, value: Non-BM Fast Reserve}
    value: window_price
    group: party_id
    group_map: {"HABITAT ENERGY LIMITED": habitat, UKPR: ukpr, ENWL: enwl}
    series_order: [ukpr, habitat, enwl]
    aggregation: mean
    time_bucket: 1d
    window: {start: "2026-02-01", end: "2026-02-28"}
    unit: "WindowPrice, no unit stated"
  chart_view:
    title: Mean window price per provider, February 2026
    caption: >-
      Silver `asdp_window_prices`, Non-BM Fast Reserve, windows starting in February 2026 (no clock
      change, no price over 1,000), dated as written: each provider's daily mean `WindowPrice`. NESO
      states no unit or clock; UKPR sent none on four days.
    alt: >-
      Line chart from neso_data_portal/asdp_window_prices of the mean WindowPrice each provider sent
      per day, windows starting 1 to 28 February 2026, no unit stated. UKPR is highest on most days,
      up to 138.0 on the 3rd, and breaks on the 1st, 4th, 15th and 23rd. Habitat Energy starts at
      128.0 and ENWL at 114.9; all three are lowest on the 26th, at 91.0, 91.8 and 85.7.
    x_label: window start date as written, February 2026
    key:
      - {series: ukpr, label: UKPR, codes: UKPR, paint: clay}
      - {series: habitat, label: Habitat Energy, codes: HABITAT ENERGY LIMITED, paint: petrol}
      - {series: enwl, label: ENWL, codes: ENWL, paint: olive}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then each year's datastore dump, kept only if its
      body changed. gridflow re-checks it at most weekly.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=non-bm-ancillary-service-dispatch-platform-asdp-window-prices"
      - "GET https://api.neso.energy/datastore/dump/91749b29-d98a-4565-b126-bd021253b3af"
      - "GET https://api.neso.energy/datastore/dump/832e6702-3007-4424-9146-8d35db8b2fe4"
    commands:
      - {run: gridflow ingest neso_data_portal asdp_window_prices --last 24h, comment: "both dumps to bronze"}
      - {run: gridflow transform neso_data_portal asdp_window_prices --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: asset_id, op: eq, value: OFR-ENWL-1}
        - {column: sp_start_date_time, op: ge, value: "2026-03-29T00:30:00"}
        - {column: sp_start_date_time, op: le, value: "2026-03-29T05:30:00"}
      order_by: [created_time]
      columns: [sp_start_date_time, sp_end_date_time, window_price, created_time, asset_id, party_id,
                entry_id, service_type, resource_id]
    key: [resource_id, created_time, asset_id]
    caption: "One asset's eight prices on 29 March 2026, the clock-change night; one window runs backwards."
    fields:
      sp_start_date_time: "Settlement window start, as NESO writes it; no zone stated"
      sp_end_date_time: "Settlement window end, as written; NESO states no clock"
      window_price: "NESO's `WindowPrice`, an indicative price; NESO gives no unit or currency"
      created_time: "When the provider's price change was created, as written; no zone stated"
      asset_id: "The Non-BM unit, as NESO names it; with `created_time`, the key"
      party_id: The provider, as NESO writes it
      entry_id: "The ASDP instruction the price refers to; it repeats, so identifies no row"
      service_type: "`Non-BM Fast Reserve` or `Non-BM STOR`"
      resource_id: "The yearly file the row came from; part of the key"
      timestamp_utc: "gridflow's capture time, UTC; not the window time"
      published_at: "Null: when NESO first published each price is not recorded"
      bronze_capture_id: Path of the bronze capture the row was read from
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  caveat: NESO gives `WindowPrice` no unit and does not say whether times are UTC or UK local.
  notebook:
    lead: >-
      `data.sql` reads the `_latest` view; `query()` would filter on `timestamp_utc`, the capture
      time. Months are cut from the window start as written. Prices are NESO's `WindowPrice`, with
      no unit stated.
    cells:
      - |
        monthly = data.sql("""
            SELECT substr(sp_start_date_time, 1, 7) AS month, party_id,
                count(*) AS prices,
                count(DISTINCT asset_id) AS assets,
                round(median(window_price), 1) AS median_price
            FROM silver_neso_data_portal_asdp_window_prices_latest
            WHERE service_type = 'Non-BM Fast Reserve'
            GROUP BY ALL ORDER BY month, party_id""")
        monthly.head()
      - |
        data.sql("""
            SELECT sp_start_date_time, sp_end_date_time, count(*) AS prices
            FROM silver_neso_data_portal_asdp_window_prices_latest
            WHERE sp_end_date_time < sp_start_date_time
            GROUP BY ALL""")
      - |
        monthly.pivot(index="month", columns="party_id", values="median_price").plot(
            color=["#66793B", "#155A6E", "#C77E3C"], figsize=(8, 3.5),
            xlabel="window start month as written",
            ylabel="median WindowPrice, no unit stated");
    needs: a capture of the two yearly files
    plot_alt: >-
      Monthly median Fast Reserve WindowPrice per provider, 28 January 2025 to 17 April 2026 (part
      months at each end), no unit stated. UKPR is highest every month, 113.0 to 164.5. All three
      are lowest in December 2025; ENWL peaks at 135.0 in March 2026, Habitat Energy at 144.0 in
      February 2025.
  related:
    - {dataset: neso_data_portal/non-bm-ancillary-service-dispatch-platform-asdp-instructions, note: "The ASDP dispatch instructions that `EntryID` points to"}
    - {dataset: neso_data_portal/obp-reserve-availability-utilisation-price, note: "Reserve prices on OBP, where these services moved; never join on ids"}
    - {dataset: neso_data_portal/obp-non-bm-reserve-instructions, note: Non-BM reserve instructions on OBP}
---

# Non-BM Ancillary Service Dispatch Platform (ASDP) Window Prices

**Status in one line: the ingested rows are in silver and gridflow's registry holds the family on the unit question,
so no model consumes them. The site page shows the rows, a chart and a notebook, with the open questions as a caveat:
the price column has no documented unit and the times have no documented clock.**

This package carries the **window-price changes** that service providers sent to NESO's Ancillary Services Dispatch
Platform (ASDP) for the Non-BM (non-Balancing-Mechanism) reserve services, Non-BM STOR and Non-BM Fast Reserve. The
vendor's package text calls it "Non-BM Window Price change on ASDP sent by Service Provider and published on
National Energy Data portal website"; the resource text says the data is published near real time, "every 30
minutes and on event basis", with a new file each year (CKAN package `notes` and resource `description`,
@.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json; NESO
[ASDP window prices](https://www.neso.energy/data-portal/non-bm-ancillary-service-dispatch-platform-asdp-window-prices)).
In market terms, a provider that is able to be dispatched for a settlement window tells NESO a price for that window,
and each change is a row here. Each row names the provider (`party_id`), the asset (`asset_id`), the service, the
settlement-period boundaries the price applies to, the price, and a creation label. `entry_id` references an
instruction dispatch in the sibling ASDP instruction table
(@./non-bm-ancillary-service-dispatch-platform-asdp-instructions.md), but it is **not** this row's identity: it is
blank in 6 rows and repeats widely.

- **Migrated to OBP.** The vendor states that the Non-BM services that used to be published on this page have
  **migrated to the OBP system**, and links the successor datasets: @./obp-non-bm-reserve-instructions.md,
  @./obp-non-bm-physical-notifications.md and @./obp-reserve-availability-utilisation-price.md. The vendor update
  frequency is recorded as "Not Active". This establishes a successor relationship only. gridflow's OBP reserve
  availability and utilisation price data and these ASDP rows cover **overlapping reporting periods but have
  different grains and different identifier systems**, so **never match, union or join the ASDP identifiers to any
  OBP identifier**, and do not treat an OBP price as a restatement of a window price.
- **Times are raw; the clock is undocumented.** `sp_start_date_time`, `sp_end_date_time` and `created_time` are
  naive strings in the bodies, and no portal dictionary states which clock they use. gridflow keeps them as
  strings, exactly as published, and does not type them as UTC or as local time.
- **The window price has no unit.** NESO's dictionary calls `WindowPrice` only an "Indicative Price", with unit `N/A`,
  no currency, no energy or capacity denominator and no time denominator. The instruction table's indicative price
  has a documented unit, but that unit cannot be copied across because the two fields are both merely "indicative
  prices". See Holds.

Related pages: @./non-bm-ancillary-service-dispatch-platform-asdp-instructions.md (the dispatch table whose
`EntryID` these rows reference), the three OBP pages above, @../../../20-domain/concepts/settlement-period.md.

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: EVT

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Non BM Window Price Change_2025 | CSV | dump | `91749b29-d98a-4565-b126-bd021253b3af` |
| Non BM Window Price Change_2026 | CSV | dump | `832e6702-3007-4424-9146-8d35db8b2fe4` |

Both resources are dispositioned `SILVER` and are **CSV data files**. The package has **no documentation (DOC)
files**: the catalogue snapshot of 2026-10-06 lists exactly two resources and both are data files, so there is no DOC
download to link. Both are datastore dumps, one per calendar year, downloadable from these vendor URLs (CKAN,
@.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json):

| Resource | Download | Bronze capture (UTC) | Body size | Silver rows | Loaded? |
|---|---|---|---:|---:|---|
| 2025 | [datastore dump](https://api.neso.energy/datastore/dump/91749b29-d98a-4565-b126-bd021253b3af) | 2026-10-08T08:51:28Z | 3,079,847 bytes | 25,933 | Yes |
| 2026 | [datastore dump](https://api.neso.energy/datastore/dump/832e6702-3007-4424-9146-8d35db8b2fe4) | 2026-10-08T08:51:58Z | 1,577,565 bytes | 13,309 | Yes |

**Both resources load, giving 39,242 silver rows** (activation 2026-10-08, window `2026-10-08..2026-10-08`, no prior
silver, 0 recorded transform failures, 0 rows excluded; @.planning/v0.22-RESULTS.md section AS-5b; RULINGS 789 and
792). The row count of the silver table equals the data rows of the two bronze bodies (4,657,412 bytes in total). The
bronze body hashes are `a94dcf61…` (2025) and `1249d37d…` (2026) (first eight characters of the sidecar SHA-256).
**There is exactly one capture of each resource**, so how the vendor amends, appends to or replaces a yearly file is
unmeasured (see Known issues).

## Families

### `asdp_window_prices`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

Schema, epoch 1 (one header in both bodies, `EntryID,ServiceType,SPStartDateTime,SPEndDateTime,WindowPrice,CreatedTime,PartyID,AssetID`):

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| EntryID | `entry_id` | string | — | yes | — | N/A (identifier) |
| ServiceType | `service_type` | string | — | yes | — | N/A |
| SPStartDateTime | `sp_start_date_time` | string | — | yes | — | N/A |
| SPEndDateTime | `sp_end_date_time` | string | — | yes | — | N/A |
| WindowPrice | `window_price` | float64 | — | yes | — | **none documented (open question ASDP-WINDOW-PRICE-UNIT)** |
| CreatedTime | `created_time` | string | — | no | — | N/A |
| PartyID | `party_id` | string | — | yes | — | N/A |
| AssetID | `asset_id` | string | — | no | — | N/A |

The "Vendor unit" column is the `unit` field of NESO's saved field info
(@.planning/research/neso-snapshots/field-info/20261008T114228Z/asdp_window_prices.json), which reads `N/A` for
every field including `WindowPrice`. Nothing in this table is a unit inferred from a column name. `entry_id` is typed
`string`, not an integer, although the vendor dictionary types it as an integer: identifiers are kept as-is and never
cast.

- Entity key: `resource_id`, `created_time`, `asset_id`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: none: `timestamp_utc` is the capture time

**Silver also carries** the engine-stamped columns `resource_id` (the key partition), `timestamp_utc`, `published_at`
(null on every row), `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id` and
`dataset_version` (observed `1+e1` on every row).

**Two clocks.** This family has no usable event-time clock, and its vintage clock is the capture time.

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |
| `timestamp_utc` / `event_time` | the same capture time: temporal recipe `none` |

- **Vintage (when it was known): `available_at` = gridflow capture time**, the `written_at` of the bronze sidecar
  (2026-10-08T08:51:28Z for the 2025 resource and 08:51:58Z for the 2026 resource; every loaded row equals one of the
  two), **not** the CKAN `last_modified`. Both resources are datastore dumps, and the record model forbids the CKAN
  `last_modified` vintage on a datastore dump (check V-8), so the family uses `capture_fallback`. The CKAN
  `last_modified` is therefore not used: it is 2025-01-27T10:19:34 for the 2025 resource and **null** for the 2026
  resource, and even the 2025 value says nothing about when a given row became available. A point-in-time query
  (`WHERE available_at <= :as_of`) therefore sees **no** history before 2026-10-08. `published_at` is null.
- **Event time: none.** The temporal recipe is `none`, so **`timestamp_utc` is the capture time**, equal to
  `available_at` and `event_time` on all 39,242 rows (verified). It is **not** the time the price applied to, and not
  the creation time. The only event-like information is in the raw string columns `sp_start_date_time`,
  `sp_end_date_time` (settlement-period boundary roles) and `created_time` (a creation label). The dictionary
  describes `sp_start_date_time` as the "Date time Settlment Period starts" and `sp_end_date_time` as the "Settlement
  Period End Date Time". They are naive strings of a single length in every row (no offset, no literal `Z`), and the
  portal states no clock. gridflow does **not** compose them with the settlement-period convention and does not type
  them as UTC. A UK settlement-day label would be a Europe/London clock on a 46 to 50 period day, and ASDP message
  timestamps are documented elsewhere as UTC (NESO
  [ASDP guidance](https://www.neso.energy/document/186511/download)), but no portal dictionary maps either statement
  onto these exported columns. `TODO: verify` the export clock of `SPStartDateTime`, `SPEndDateTime` and `CreatedTime`
  (ASDP-EXPORT-CLOCK; a portal statement covering this table would settle it). Until then, do not compute a UTC event
  time from them, and do not assume a 30-minute boundary on a clock-change day.
- **Creation time is not availability.** `created_time` is the vendor's creation label for the change. It is not
  proved immutable, and no issue or publication time is published, so `issue` is `none` and nothing is backdated to the
  creation label or the settlement-period start (`TODO: verify` ASDP-ISSUE-IMMUTABILITY: repeat captures or a vendor
  availability guarantee would settle it).

**Units (vendor dictionary only; nothing converted).**

| Silver | Vendor title (dictionary) | Unit |
|---|---|---|
| `entry_id` | Entry ID ("EntryID from Instruction Dispatches") | identifier, no physical unit |
| `service_type` | Service Type | none (categorical) |
| `sp_start_date_time` | SP Start DateTime | time label, clock `TODO: verify` |
| `sp_end_date_time` | SP End DateTime | time label, clock `TODO: verify` |
| `window_price` | Window Price ("Indicative Price") | **`TODO: verify` ASDP-WINDOW-PRICE-UNIT; no unit documented** |
| `created_time` | Created Time | time label, clock `TODO: verify` |
| `party_id` | Party ID (service provider name for the corresponding instruction) | identifier |
| `asset_id` | Asset ID (Non-BMU id for the corresponding instruction) | identifier |

`window_price` is stored as `float64` exactly as published. gridflow attaches **no** currency, no energy or capacity
quantity and no time denominator to it: do not read it as £/MWh, £/MW/h, £/MW or p/kWh.

**Sentinels and typing (K-AS-5-FACTS g5, g6).**

- **Strict typing, no repair.** The body is valid UTF-8, with no embedded data-cell commas, quotes or newlines (the
  production CSV reader agreed with a strict second parse on every row and cell). No whitespace trim, no token map
  and no bounds are applied: **no new token is mapped to null**, and no `NA`, `N/A` or thousands-separator marker
  occurs in the price column.
- **Blanks stay null, zeros stay zero.** The `window_price` column has no blank cell in either body. `entry_id` is
  blank (null) in 6 rows; the other columns have no blank. Any zero price is a published value, not a missing one,
  and is kept.
- **Identifiers as-is.** `entry_id`, `party_id` and `asset_id` are stored byte-for-byte as published. `party_id` is a
  provider name and can carry padding; it is not normalised.

**Identity and selection.**

- **`entry_id` is not the identity.** It repeats widely (30,618 of the 39,242 rows share a non-blank `entry_id` with
  another row; the 6 blank-`entry_id` rows, all in the 2025 resource, have no id to share and are not counted), because one instruction can carry several price changes. In the 2025 resource, both
  (`EntryID`, `SPStartDateTime`) and (`EntryID`, `CreatedTime`) repeat, and adding the settlement boundaries does not
  remove the collision.
- **The measured key is (`resource_id`, `created_time`, `asset_id`).** (`CreatedTime`, `AssetID`) is nonblank and
  unique within each resource and across all 39,242 rows, and all 39,242 silver rows are unique on the key. This is a
  **measured** identity, not a vendor guarantee, so the vendor-side stability is `TODO: verify`; `resource_id` stays in
  the key under the whole-capture-per-resource selection, so a re-capture of a resource replaces that resource's rows and
  no other. Two rows that share an `entry_id` are therefore both kept, under distinct `created_time` and `asset_id`
  pairs. Nothing is deduplicated, and there is no `run_type` (this is a price-change table, not a settlement run).
- **Service vocabulary.** `service_type` carries the vendor values `Non-BM Fast Reserve` (39,239 rows) and
  `Non-BM STOR` (3 rows), byte-equal. The dictionary adds that RDP dispatch instructions carry `RDP_NEGATIVE` in the
  instruction table; no such row occurs in this table.

## Cadence

- Registry refresh: frozen
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Not Active

The vendor says a new file is created each year and that the data was published every 30 minutes and on event basis;
its update-frequency extra now reads "Not Active", consistent with the migration to OBP. The CKAN metadata of the 2026
resource was last modified 2026-04-17T21:01:00 (resource `metadata_modified`), and the package metadata 2026-05-11.
The registry marks the family `frozen`: it does not expect new rows. gridflow has **one capture** of each resource
(2026-10-08), so whether the 2026 file continued to grow after April 2026, whether past rows were ever amended, and
what an amendment looks like are unmeasured (`TODO: verify`, repeat captures against the hash-pinned bodies).

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence). Any gridflow output
derived from this package carries the attribution line "Supported by National Energy SO Open Data". The site page
shows the rows, a chart and a notebook under it, with the unit and clock questions stated as a caveat.

## Holds

- `asdp_window_prices`: held: TODO: ASDP-WINDOW-PRICE-UNIT — the ASDP window-price dictionary calls WindowPrice only an indicative price and gives no currency, energy or time denominator, and the instruction table's £/MWh cannot be transferred because both are "indicative prices"; which unit does WindowPrice carry (for example £/MWh or £/MW/h)? (Settlement-period and creation times are naive with an undocumented export clock.) (unit v0.22-K-AS-5b)

**What the hold means.**

- **The package stays `eligible`; the family is `held` in gridflow.** The 39,242 silver rows exist, with a validated
  schema and the key above. A model must not consume `window_price` while the hold stands, and there is no gold
  artefact (see below). The site page shows the rows anyway (ruling 66: show rows, name the open question): eight
  sample rows, a chart of the daily mean `WindowPrice` per provider labelled "no unit stated", and a notebook, with a
  caveat that NESO gives `WindowPrice` no unit and states no clock for the times.
- **Hold unit:** `v0.22-K-AS-5b` (seat ruling 4: window prices held on the unit question; the key is the measured one
  and is never `EntryID`). The hold question is the one printed above, verbatim from the registry and the eligibility
  report (@.planning/RULINGS.md rulings 765, 766 and 789; eligibility report
  `docs/neso_data_portal/eligibility.md` in the gridflow repo).
- **What would release it.** A vendor definition that explicitly maps the exported `WindowPrice` field to a unit
  (£/MWh, £/MW/h or another dimension). The ASDP instruction table's documented indicative-price unit is **not**
  transferred by analogy. A hold is a question for NESO, not a data-quality verdict on the rows.

**Open questions that do not hold any further output** (K-AS-5-FACTS, carried as non-holding TODOs):

- `TODO: verify` the **export clock** of `SPStartDateTime`, `SPEndDateTime` and `CreatedTime` (ASDP-EXPORT-CLOCK), above.
- `TODO: verify` the **availability and immutability** of a row relative to its `created_time`
  (ASDP-ISSUE-IMMUTABILITY), above.
- `TODO: verify` the **stable vendor identity** of a price change; only the measured (`created_time`, `asset_id`)
  uniqueness is established.
- `TODO: verify` how the **blank `entry_id`** in 6 rows arises (a price change with no instruction reference, or a
  publication gap).

**Known issues and gotchas.**

- **Do not give `window_price` a unit.** The unit is unknown, so the numbers must not be compared with any £/MWh,
  £/MW/h or £/MW series, including the sibling instruction price and the OBP prices.
- **Backwards windows on 29 March 2026.** Ten rows (one per asset priced that night) have `SPStartDateTime`
  `2026-03-29T01:30:00` and `SPEndDateTime` `2026-03-29T01:00:00`, and windows starting 01:00 and 01:30 exist on a
  night UK local time skipped 01:00 to 01:59; the next window starts 03:00. No backwards window occurs on the 2025
  clock changes. Evidence for the export-clock question, not an answer to it.
- **Never match to OBP.** The services migrated to OBP; the reporting periods overlap, the grain and identifiers
  differ. There is no silver relation to OBP and none should be built from `entry_id`.
- **Join to ASDP instructions with care.** `entry_id` is described as the id from the instruction dispatches, but it is
  stored as a string here and it is blank in 6 rows. gridflow defines no silver join between the two tables, and
  `entry_id` is not this table's identity. `TODO: verify` the vendor's referential guarantee before joining.
- **Capture time stands in for everything.** `timestamp_utc` is the 2026-10-08 capture time on every row, so this
  table cannot be placed on a time axis through `timestamp_utc`. Until the clock is established, use the raw string
  columns labelled "as written" (as the site's chart does), never as UTC or UK local instants.
- **Coverage is two calendar-year files.** The 2025 resource and the 2026 resource are the whole package; the 2026
  file is a year in progress whose CKAN `metadata_modified` is 2026-04-17.
  Whether it is complete for its stated year, or still being appended to, is not stated by the vendor.
- **Settlement-period conventions.** Settlement periods run 1 to 50 (46 on the spring clock-change day and 50 on the
  autumn day). This table has no settlement-period number, only boundary timestamps; a window boundary near a clock
  change cannot be interpreted until the export clock is known.

**Gold layer.** None implemented. No gold view or Parquet builder reads this family, and none may while the hold stands.

**Modelling notes.** Not used in gridflow_models. `TODO` until the unit is established: the table is a candidate
feature source for Non-BM reserve availability pricing, and would be joined to the instruction table and to
@./obp-reserve-availability-utilisation-price.md **by time and asset only after the clocks and the unit are settled**,
never by identifier.
