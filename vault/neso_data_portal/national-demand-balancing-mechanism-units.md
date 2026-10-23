---
source: "neso_data_portal"
package: "national-demand-balancing-mechanism-units"
dataset_key: "national_demand_bmus"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-23
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: National demand BM units
  summary: >-
    NESO's preliminary list of the Balancing Mechanism units that make up National Demand: one CSV
    of unit names, nothing else.
  facts:
    vendor: "NESO Data Portal, package `national-demand-balancing-mechanism-units`: one CSV"
    cadence: "Ad hoc, as NESO's catalogue states; the file was last modified 29 September 2026"
    grain: "One row per BM unit name: 1,001 in NESO's file of 29 September 2026"
  landscape: units
  what_it_is: >-
    NESO calls this "a preliminary list of Balancing Mechanism units that make up National Demand".
    NESO's Historic Demand Data dictionary defines National Demand: it "is the sum of metered
    generation, but excludes generation required to meet station load, pump storage pumping and
    interconnector exports". The file holds unit names only. NESO does not say what "preliminary"
    means.
  how_used:
    - "Join to Elexon's BM unit register on `national_grid_bm_unit`, not `bm_unit_id`."
    - "Filter BM unit data to the units NESO says make up National Demand."
    - "See the units' Elexon fuel types by joining through the register."
  chart:
    type: none
    reason: >-
      A list of unit names with no other column: nothing NESO publishes here to count or
      plot by.
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show`, then the CSV downloaded whole, skipped while its
      `last_modified` is unchanged. One column, `BM_Name`.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=national-demand-balancing-mechanism-units"
      - "GET https://api.neso.energy/dataset/1999ccfb-5f8c-4921-b408-d92ab5c61c2b/resource/7e1e84cf-89f4-4c69-a72a-d778087c22a4/download/bmunits_29_09_26.csv"
    commands:
      - {run: gridflow ingest neso_data_portal national_demand_bmus --last 24h, comment: "whole file; window must end recently"}
      - {run: gridflow transform neso_data_portal national_demand_bmus --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: bm_name, op: in, value: [ABERU-1, ABRTW-1, AG-ADL03E, AG-PEPG01, DIDCB6, DNGB21, HAB02G, ZEN02A]}
      dedup: {"on": [bm_name], order_by: capture_written_at}
      order_by: [bm_name]
      columns: [bm_name, published_at, timestamp_utc, capture_written_at, bronze_capture_id]
    key: [bm_name]
    caption: "Eight names picked from the list, alphabetical, among them NESO's dictionary example `AG-ADL03E`."
    fields:
      bm_name: "BM unit name as NESO spells it; matches Elexon's `national_grid_bm_unit` where registered"
      published_at: "NESO's last-modified time for the file, read as UTC; one value per capture"
      timestamp_utc: "When gridflow captured the file, UTC; the list has no event time"
      capture_written_at: When gridflow wrote that capture to bronze, UTC
      bronze_capture_id: The bronze file the row was read from; one per capture
  notebook:
    lead: >-
      `query()` filters on `timestamp_utc`, the capture time here, so these cells use `data.sql()`
      on the `_latest` relation and join Elexon's BM unit register, fetched 26 September 2026, on
      `national_grid_bm_unit`.
    cells:
      - |
        df = data.sql("""
            SELECT n.bm_name, e.bm_unit_id, e.bm_unit_name, e.fuel_type
            FROM silver_neso_data_portal_national_demand_bmus_latest AS n
            LEFT JOIN silver_elexon_bmunits_reference AS e
              ON e.national_grid_bm_unit = n.bm_name
            ORDER BY n.bm_name
        """)
        df.head()
      - df.bm_unit_id.notna().rename("in_elexon_register").value_counts()
      - |
        reg = data.sql("""
            SELECT fuel_type, national_grid_bm_unit IN (
                       SELECT bm_name FROM silver_neso_data_portal_national_demand_bmus_latest
                   ) AS on_list
            FROM silver_elexon_bmunits_reference
            WHERE fuel_type IS NOT NULL
        """)
        reg.groupby(["fuel_type", "on_list"]).size().unstack(fill_value=0)
      - |
        kind = df.fuel_type.where(df.bm_unit_id.notna(), "not in register").fillna("no fuel type")
        ax = kind.value_counts(ascending=True).plot.barh(figsize=(6, 4))
        ax.set(xlabel="BM units on NESO's list", ylabel="");
    needs: NESO's national demand BM unit list and Elexon's BM unit register
    plot_alt: >-
      Horizontal bars counting the 1,001 names on NESO's list by Elexon fuel type, in the register
      fetched 26 September 2026. 445 match a unit with no fuel type, 222 are WIND and 142 are not in
      the register. Then OTHER 89, CCGT 47, NPSHYD 16, NUCLEAR 14, BIOMASS and OCGT 12 each, COAL 2.
  related:
    - {dataset: elexon/bmunits_reference, note: "Elexon's BM unit register; join on its `national_grid_bm_unit`"}
    - {dataset: neso_data_portal/historic-demand-data, note: "Half-hourly National Demand, which NESO says these units make up"}
    - {dataset: elexon/indo, note: "Elexon's demand outturn, which NESO calls equivalent to `ND`"}
    - {dataset: neso_data_portal/daily-demand-update, note: "Recent `ND` outturn, updated daily by NESO"}
---

# National Demand Balancing Mechanism Units

A reference list of Balancing Mechanism (BM) unit names, published by NESO as one CSV on the
Open Data Portal. The package notes describe it as "a preliminary list of Balancing Mechanism
units that make up National Demand", and relate it to the Historic Demand Data package
(@historic-demand-data.md). The file has a single column, `BM_Name`. It has no attributes, no
effective dates and no issue time. It is a **membership snapshot**, not a time series: each
capture is the whole list as NESO last uploaded it, and membership may change between uploads.
Use it to see which BM units NESO counts towards National Demand (ND, as published in
@daily-demand-update.md and @historic-demand-data.md), and to join those units to the Elexon BM
unit reference (@../../elexon/datasets/bmunits_reference.md). BM units are explained in
@../../../20-domain/concepts/bm-units.md. `TODO: verify` what "preliminary" means here: whether
NESO ever publishes a final list, and what would change in it. `TODO: verify` the composition
rule: whether these are the metered units whose output is summed into ND, or units on the
demand side of it. The vendor does not say, and it is not inferred here from the ID shapes.

- Publisher group: Demand
- Registry group: demand · archetype: REG

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| National Demand Balancing Mechanism Units | CSV | upload | `7e1e84cf-89f4-4c69-a72a-d778087c22a4` |

- Download: [bmunits_29_09_26.csv](https://api.neso.energy/dataset/1999ccfb-5f8c-4921-b408-d92ab5c61c2b/resource/7e1e84cf-89f4-4c69-a72a-d778087c22a4/download/bmunits_29_09_26.csv)
  (CKAN datastore active; CKAN `last_modified` 2026-09-29T13:45:22.344455).
- Captured: `raw_20261008T111257Z_7e1e84cf-89f4-4c69-a72a-d778087c22a4_46cdc2ce.csv`,
  9,462 bytes, 1,001 data rows, one header epoch (`BM_Name`). Body SHA-256 matches its sidecar.

The package has no DOC resources and no `_files` family (gridflow
`@.planning/phases/v0.22-K-DEM-2/K-DEM-2-FACTS.md` §1). There is no vendor documentation file
to download; the package notes, the resource description and the CKAN field dictionary are the
only vendor sources.

## Families

### `national_demand_bmus`

- Kind: tabular · archetype: REG · refresh: adhoc · empty allowed: yes

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| BM_Name | `bm_name` | string | — | yes | — | — |

- Entity key: `bm_name`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured resource. For the one capture to date that is
   `2026-09-29T13:45:22.344455`, taken from the capture's sidecar. CKAN emits it without an
   offset, and gridflow reads it as UTC (gridflow
   `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`, D-15). Every row of a capture
   shares this one vintage. It says when NESO last changed the file, not from when the list of
   units was true. The record has no issue time (issue recipe `none`). The date in the filename
   (`29_09_26`) is not a documented issue time either (FACTS §4 g2).
2. **Event time (`none`).** The list has no represented-time column, so there is no event time
   from the data. `timestamp_utc` is simply the **capture time**: when gridflow fetched the
   file, `2026-10-08T11:12:57.464036+00:00` for the one capture. `event_time` equals
   `timestamp_utc`. This is not a date the vendor attaches to the list, and it must not be read
   as "the date these units made up National Demand" (FACTS §2; gridflow
   `@src/gridflow/silver/neso_data_portal/casting.py` lines 605 to 607).

**Units (vendor dictionary only, field info read 2026-10-08, gridflow
`@.planning/research/neso-snapshots/field-info/20261008T114228Z/national_demand_bmus.json`).**
The dictionary has one field, `BM_Name`: type `text`, description "Name of BM Unit", example
`AG-ADL03E`, unit blank. It is an identifier, not a measurement, so no unit applies (FACTS g4).

**Sentinels and missing values (FACTS g5).** The vendor declares no sentinel spelling, and the
record has no null-token map. The capture has **zero** blank, `-1`, `N/A`, `NA` or literal-zero
cells. One name carries a trailing space: `"EEND01 "` (CSV line 990). It is an identifier
spelling, kept exactly as delivered. Checked in silver on 2026-10-09, the value is 7 characters
long, so the space survives. BM unit IDs are stored as-is, with no trimming, case change or
other normalisation.

**Identity and selection.** `bm_name` is the entity key and the only vendor column. In this
capture it is unique: 1,001 rows, 1,001 distinct names, no duplicates (FACTS §4). That makes it
a **within-capture uniqueness guard**, not a vendor-guaranteed identity: NESO states no
uniqueness promise (`TODO: verify` vendor uniqueness guarantee, FACTS T02). `_latest` is
`whole_capture`: the newest capture replaces the list as a whole. A unit missing from a newer
capture has left the list; it is not carried forward from an older one. `key_latest` is not
used, because measured uniqueness alone does not justify it (ADR-036).

**Elexon cross-check (FACTS §4, evidence C-E).** The unchanged NESO names were compared with the
local Elexon BM unit reference (`bmunits_reference`, 3,014 rows, ingested
2026-09-26 19:08:06 UTC):

| NESO `bm_name` matched exactly against | Matching NESO names (of 1,001) |
|---|---:|
| Elexon `bm_unit_id` | 0 |
| Elexon `national_grid_bm_unit` | 859 |
| Either identifier column | 859 |
| Elexon `bm_unit_name` (diagnostic only) | 17 |
| Absent from both identifier columns | 142 |

So the NESO names are in the **National Grid BM unit** namespace. Join NESO `bm_name` to Elexon
`national_grid_bm_unit`, not to `bm_unit_id`. The two Elexon namespaces are kept apart in the
repository mapping (gridflow `@src/gridflow/silver/elexon/bmunits.py` lines 95 and 104). Not
every NESO name is found. Examples absent from both identifier columns: `ACHYW-1`, `AG-PEPG01`,
`AG-REC07E`, `AIGA-1` and `"EEND01 "`. `TODO: verify` why the 142 are unmatched. The local
Elexon snapshot predates the NESO file's `last_modified`, but that does not explain any one ID.
A newer Elexon reference or a vendor answer would settle it. Do not normalise IDs or invent
aliases to force matches. By Elexon `fuel_type` (same snapshot, checked 2026-10-23), the 859
matched names are 222 `WIND`, 89 `OTHER`, 47 `CCGT`, 16 `NPSHYD`, 14 `NUCLEAR`, 12 `BIOMASS`,
12 `OCGT`, 2 `COAL` and 445 with no fuel type; none of the register's 16 `PS` units or its 11
interconnector units (ten `INT*` fuel types) is on the list. NESO states no rule that explains this.

**Activation (2026-10-09, master `776e87a`, PR #91).** The family was transformed with cutoff
2026-10-08 (one capture). Silver has **1,001 rows**, equal to the planned count. Reconcile
`--all` at cutoff 2026-10-08 found 0 gaps over 41 recorded families, with overlap 0. No prior
silver existed, so nothing was overwritten (gridflow `@.planning/v0.22-RESULTS.md` §DEM-2;
RULINGS 538 ruled the family eligible, 540 the merge, 541 the activation).

Silver columns beyond the one vendor column: `timestamp_utc`, `published_at`,
`bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id`,
`dataset_version` (all timestamps tz-aware UTC; `dataset_version` `1+e1` = record version 1
plus generic-engine version 1). Silver lives at
`C:/gridflow-data/silver/neso_data_portal/national_demand_bmus/`.

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc

The vendor gives no schedule beyond "Ad hoc". The package was created 2024-04-15; the current
file was last modified 2026-09-29. gridflow has no scheduled refresh for this family, so
captures are on demand. One capture (2026-10-08) exists, still the only one on 2026-10-23: an
ingest skips an upload resource while its CKAN `last_modified` equals the newest capture's
(gridflow `@src/gridflow/connectors/neso_data_portal/client.py` `iter_members`). The 2026-10-16
refresh found it so: "1 unchanged since newest capture" (gridflow
`@.planning/phases/v0.22-close/refresh-20261016/ingest.log` line 226). `TODO: verify` whether a new
NESO upload replaces this resource in place or adds a new resource beside it. Only a second
capture can show that.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- none

`national_demand_bmus` is eligible (RULINGS 538). No unit E-SEM question is open on it, and its
silver output may be used and published.

Other packages in the same batch are not all eligible. Demand Profile Dates is captured in
bronze but has no silver output (@demand-profile-dates.md), and the school holiday percentages
are in silver but held (@school-holiday-percentages.md). Those pages give the reasons.

**Implementation delta (vendor metadata vs capture and record).**

- The catalogue snapshot (2026-10-06) gives the resource a CKAN `size` of 6,175 bytes. The
  captured body is 9,462 bytes, which equals the download's declared content length. Both carry
  the same `last_modified` (2026-09-29T13:45:22.344455). `TODO: verify` why the CKAN size
  differs from the delivered body.
- The dictionary types `BM_Name` as `text`; the record reads it as `string`. These agree.
- The record marks `bm_name` nullable, although it is the entity key. The capture has no
  blanks, so this has had no effect.
