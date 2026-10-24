---
source: "neso_data_portal"
package: "obp-non-bm-physical-notifications"
dataset_key: "obp_physical_notifications"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-13
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: OBP non-BM physical notifications
  summary: >-
    Physical notifications (PN) that providers declare to NESO's Open Balancing Platform (OBP) for
    non-BM units: each unit's MW level over time.
  facts:
    vendor: "NESO Data Portal: one CSV, republished under a new file name"
    cadence: "Ad hoc, NESO says, and published through the day"
    grain: "One row per unit and window: the PN level at its start and end"
  landscape: market
  what_it_is: >-
    A physical notification (PN) is the MW profile a provider declares for a non-BM unit; NESO
    publishes those OBP accepted by gate closure. Each row is one window, with levels at both ends.
    Times are UTC, NESO says; the text has no zone marker and is not UK local time on 29 March
    2026, holding 01:00, which UK clocks skipped.
  how_used:
    - Each non-BM unit's declared MW profile, in windows down to a minute
    - Declared positions above and below zero, by unit and half-hour
    - 'OBP instructions: NESO gives their target MW as "power from PN in absolute values"'
  chart:
    type: line
    silver: neso_data_portal/obp_physical_notifications
    time: time_from
    value: level_from
    filter:
      - {column: unit_id, op: in, value: ["GSET-07", "GSET-04", "GSET-02"]}
    dedup: {on: [unit_id, time_from], order_by: published_at}
    group: unit_id
    group_map: {"GSET-07": gset07, "GSET-04": gset04, "GSET-02": gset02}
    series_order: [gset07, gset04, gset02]
    aggregation: mean
    time_bucket: 30m
    window: {start: "2026-09-21", end: "2026-09-21"}
    unit: MW
  chart_view:
    title: Declared PN of three units, 21 September 2026
    caption: >-
      Silver `neso_data_portal/obp_physical_notifications`, `level_from` in MW at each half-hour
      start, three units, 21 September 2026 (UTC). Every window here is a whole half-hour with equal
      start and end levels; the sloped joins are drawing only. NESO states no sign.
    alt: >-
      Line chart from neso_data_portal/obp_physical_notifications of the declared PN in MW at each
      half-hour start, 21 September 2026 UTC, for three units. GSET-07 holds -17.03 from 03:30 to
      04:30 and from 14:00 to 15:30; GSET-04 holds -6 from 03:30 to 04:30 and from 13:30 to 15:30;
      GSET-02 is -3 at 03:30, 04:00, 13:30 and 14:00. Above zero, GSET-07 reaches 15.44 at 06:30,
      15.09 at 16:30, 15.97 at 18:00 and 12.50 at 20:00; GSET-04 reaches 6 and GSET-02 3.
    x_label: half-hour start, UTC, 21 September 2026
    key:
      - {series: gset07, label: GSET-07, paint: petrol, note: "-17.03 MW from 03:30 to 04:30 and 14:00 to 15:30; 15.97 MW at 18:00."}
      - {series: gset04, label: GSET-04, paint: horizon, note: "-6 MW from 03:30 to 04:30 and 13:30 to 15:30; 6 MW at 06:30, 16:30, 18:30."}
      - {series: gset02, label: GSET-02, paint: olive, note: "-3 MW at 03:30, 04:00, 13:30 and 14:00; 3 MW at 16:30."}
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show`, then the one CSV downloaded whole unless its
      `last_modified` is unchanged. The file name changes with each publication.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=obp-non-bm-physical-notifications"
      - "GET https://api.neso.energy/dataset/73edf630-fe9e-45a6-a2be-fa0d31a8ec1d/resource/dfe1d229-e973-43c6-b5eb-c28ad59d7136/download/pn_20261016_46_nbm.csv"
    commands:
      - {run: gridflow ingest neso_data_portal obp_physical_notifications --last 24h, comment: "whole file; window must end recently"}
      - {run: gridflow transform neso_data_portal obp_physical_notifications --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: unit_id, op: eq, value: AFFR-1}
        - {column: time_from, op: ge, value: "2026-09-21T09:00:00"}
        - {column: time_from, op: lt, value: "2026-09-21T11:30:00"}
      dedup: {on: [unit_id, time_from], order_by: published_at}
      order_by: [time_from]
      columns: [time_from, level_from, time_to, level_to, unit_id, data]
    key: [unit_id, time_from]
    caption: "`AFFR-1`, 09:00 to 11:30 UTC, 21 September 2026: one-minute windows move it between 0 and -2."
    fields:
      time_from: "Window start, UTC (NESO), written without a zone marker; with `unit_id`, the key"
      level_from: "PN at gate closure for the window start, MW (NESO); no sign stated"
      time_to: "Window end, UTC (NESO); NESO does not say whether the end belongs to it"
      level_to: "PN at gate closure for the window end, MW (NESO); path between unstated"
      unit_id: "The registered non-BM unit, as NESO writes it"
      data: "`PN`, a fixed value, NESO says"
      timestamp_utc: "Equals `time_from`, the window start in UTC"
      published_at: "The CSV's portal last-modified time, read as UTC; one per capture"
      bronze_capture_id: Path of the bronze capture the row was read from
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      Returns a pandas DataFrame from `silver_neso_data_portal_obp_physical_notifications_latest`,
      the newest capture, filtered on `timestamp_utc` (window start) with both ends included. Times
      come back in the session's zone, UK time on UK machines; cell one converts.
    cells:
      - |
        df = data.neso_data_portal.query(
            "obp_physical_notifications", "2026-09-21", "2026-09-21")
        for c in ["time_from", "time_to"]:
            df[c] = df[c].dt.tz_convert("UTC")
        df = df.sort_values(["unit_id", "time_from"])
      - |
        units = df.groupby("unit_id").agg(windows=("time_from", "count"),
            lowest_mw=("level_from", "min"), highest_mw=("level_from", "max"))
        units[(units.lowest_mw < 0) & (units.highest_mw > 0)].reset_index()
      - |
        m = data.neso_data_portal.query(
            "obp_physical_notifications", "2026-03-29", "2026-03-29")
        m["time_from"] = m.time_from.dt.tz_convert("UTC")
        m.loc[m.time_from.dt.hour == 1, ["unit_id", "time_from", "level_from"]]
      - |
        import matplotlib.dates as mdates
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(8, 3.5))
        for unit in ["GSET-07", "AFFR-1"]:
            g = df[df.unit_id == unit]
            x = [t for a, b in zip(g.time_from, g.time_to) for t in (a, b)]
            y = [v for a, b in zip(g.level_from, g.level_to) for v in (a, b)]
            ax.plot(x, y, label=unit)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        ax.set(xlabel="window start and end, UTC, 21 September 2026", ylabel="PN, MW")
        ax.legend();
    needs: a capture of NESO's OBP physical notifications file
    plot_alt: >-
      Line plot of PN in MW, UTC, 21 September 2026, each window drawn from its start level to its
      end level. GSET-07 changes only at half-hour starts, from -17.03 (03:30 to 05:00, 14:00 to
      16:00) up to 15.97 from 18:00 to 18:30. AFFR-1 moves among -4, -2, 0 and 2 MW through one-minute windows.
  related:
    - {dataset: neso_data_portal/obp-non-bm-reserve-instructions, note: 'OBP instructions; target MW is "power from PN in absolute values" (NESO)'}
    - {dataset: neso_data_portal/obp-reserve-availability-utilisation-price, note: "Availability and utilisation prices offered by OBP reserve units"}
    - {dataset: elexon/pn, note: "Physical notifications for units inside the Balancing Mechanism, from Elexon"}
---

# Open Balancing Platform (OBP) - Non-BM Physical Notifications (PN)

This package is NESO's publication of the **Physical Notifications (PN) that non-BM Service Providers declare to the Open Balancing Platform (OBP)**. The vendor's package text says NESO publishes "Non-BM Physical Notifications (PN) data declared by Service Providers to Open Balancing Platform (OBP) system", published "continuously throughout the day" (CKAN package `notes`, @.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json; NESO [OBP Non-BM Physical Notifications](https://www.neso.energy/data-portal/obp-non-bm-physical-notifications)). A PN is a provider's declared MW output (or consumption) trajectory for a **registered non-BM unit**: the unit is not in the Balancing Mechanism, so its position is not otherwise visible in BM data (compare @../../../20-domain/concepts/bm-units.md). Each row is one **PN segment**: a start instant with the declared level at that instant, and an end instant with the declared level at that instant, so a flat PN is a row with equal levels (whether the vendor intends a linear ramp between unequal levels is not stated: `TODO: verify`). The vendor says both levels are "PN at Gate Closure" in MW (field-info text, below).

For a model this is the **declared pre-dispatch position of small, flexible, non-BM assets** (the units NESO procures reserve from outside the BM): it shows how much flexible capacity sits at each level over time, so it is a feature for reserve availability and for the volume NESO can instruct from non-BM providers. It is **not metered output**: these are provider declarations accepted and validated by OBP, not observed generation or demand.

**What this package is not.**

- It is **not a forecast archive.** There is no issue time; gridflow records `issue: none` and uses no forecast exemption. The recommended admission rests on the vendor's gate-closure declaration semantics, treated as an event/declaration table with a conservative capture vintage (RULINGS 738). Of the segment starts, 494,936 are on or before the CKAN `last_modified` of the 2026-10-08 capture and 150 are after it (K-AS-3 FACTS section 6.1; 692 in the 2026-10-16 capture): the later ones are declared positions, not forecasts of a value measured afterwards.
- It is **not a settlement-period table.** Segments are not uniformly half-hours: 400,690 of 495,086 rows last 1,800 s (2026-10-08 capture; 416,661 of 523,890 in the 2026-10-16 capture), and measured durations run down to 60 s. There is no `run_type`, no settlement date and no period number; none is synthesised.
- It does **not carry the dispatch instructions or the availability and price bands.** Those are the sibling packages @./obp-non-bm-reserve-instructions.md and @./obp-reserve-availability-utilisation-price.md. The PN is the reference position that the instruction "Target MW" is described against (vendor wording; see the instructions page).
- `unit_id` is a **registered non-BM unit ID**, not necessarily a BM unit ID or an NESO ID encoding. The vendor does not establish a universal encoding (K-AS-3 FACTS section 6.1). Values are stored exactly as served (101 distinct, for example `EDFE-11`, `ENGQR-02`, `ANSC-101`, `ARNKB-2`).

**Scope of the captured body.** One resource, 29,533,717 bytes, **495,086 rows** in the first capture, of 2026-10-08 (the second, of 2026-10-16, follows below). Segment starts run `2025-10-08T16:00:00` to `2026-10-08T12:29:00` and segment ends `2025-10-08T16:30:00` to `2026-10-08T12:30:00` (UTC). The body therefore spans about the 12 months before its `last_modified`: under `whole_capture`, older history lives only in older captures (K-AS-3b spec observation, not a ruling). A second capture (2026-10-16, 523,890 rows, `last_modified` 2026-10-16T20:31:22) still starts at `2025-10-08T16:00:00`, so over those eight days the file grew and did not roll forward; whether it ever drops old rows is unmeasured (front-end page check, 2026-10-23, both silver files). Rows per unit range from 13 (`ARNKB-2`) to 15,047 (`ENGQR-01`, `ENGQR-02`).

**Units (vendor dictionary only).** `Level From` and `Level To` are **MW** ("PN at Gate Closure for window start time in MW" and "... for window end time in MW"; field-info unit `MW`, @.planning/research/neso-snapshots/field-info/20261008T114228Z/obp_physical_notifications.json, K-AS-3 FACTS g4). `Time From` and `Time To` carry the vendor unit `UTC`. `Data` has unit `N/A` (a label). Nothing is converted, and no MW-to-MWh energy conversion is stated or applied: a level is an instantaneous power at an instant, not an energy volume.

**Sentinels and zeros (K-AS-3 FACTS g5).** Preserve numeric zeros: in the 2026-10-08 capture, 407,637 rows have `level_from` 0 and 407,238 have `level_to` 0 (longest file-order zero run 325 for each); a zero is a declared PN of zero, not a missing value, and is never nulled. Negative levels are real values: both columns range from **-49.9 to 50 MW**, and 42,083 rows of the 2026-10-08 capture have a negative `level_from` (`TODO: verify` the sign convention, which the dictionary does not state). In the 2026-10-16 capture, 37 of the 101 units declare both signs and 51 declare zero on every row (front-end page check, 2026-10-23). No `NA`/`N/A` token, comma numeral, percent sign, padded number or other lexical defect was found in this body (K-AS-3 FACTS section 6.1, C07/C10), and there are no blank cells in any of the six columns (checked on all silver rows: 0 nulls in `level_from`, `level_to`, `time_to`).

**Typing.** `Data` is the fixed value `PN` on every row (vendor: "Fixed value PN"), kept as a string. `Unit ID` is a string, byte-equal as served. The two level columns are `float64`. The two time columns are `%Y-%m-%dT%H:%M:%S` cells with **no offset suffix**, typed as tz-aware UTC without a shift: the BST-season start `2026-06-01T00:00:00` stays `00:00Z`, which is 01:00 UK local time. The vendor's dictionary example (`2025-11-25T05:00:00Z`) carries a `Z`, but the served cells do not, so the UTC typing rests on the vendor's stated unit and not on the cell syntax. The rows rule out UK local time on one day: on 2026-03-29, when UK clocks skipped 01:00 to 02:00, five units (`ENGQR-01`, `-02`, `-03`, `-05`, `ANSC-101`) carry contiguous windows starting `01:00:00` and `01:30:00`. On 2025-10-26 (clocks back) the three units present (`EDFE-8`, `EDFE-11`, `EDFE-21`) have 119, 50 and 95 windows, each unit's windows covering exactly 24 hours (2025-10-26T00:00 to 2025-10-27T00:00), which fits UTC (a UK local day had 25 hours) but cannot by itself exclude local time. One observation also fits UTC without proving it: in both captures the last window ends about 1 h 29 min after the file's `last_modified` (12:30 against 11:01:24; 22:00 against 20:31:22), so the file reaches the half-hour that starts just under an hour after it, while read as UK local time it would reach only about 29 minutes ahead (front-end page check, 2026-10-23).

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: EVT

## Files by disposition

One resource: the package has a single file and it is a silver source. There are no DOC files and no held files in this package.

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Non-BM Physical Notifications | CSV | upload | `dfe1d229-e973-43c6-b5eb-c28ad59d7136` |

- **Non-BM Physical Notifications** (SILVER, family `obp_physical_notifications`): CKAN resource `dfe1d229-e973-43c6-b5eb-c28ad59d7136`, package id `73edf630-fe9e-45a6-a2be-fa0d31a8ec1d`, flagged `datastore_active` by the vendor. gridflow captures it as an **upload file** (the download URL), not the datastore: [catalogue snapshot URL of 2026-10-06](https://api.neso.energy/dataset/73edf630-fe9e-45a6-a2be-fa0d31a8ec1d/resource/dfe1d229-e973-43c6-b5eb-c28ad59d7136/download/pn_20261006_44_nbm.csv). The file name in the URL embeds a date (`pn_20261006_44_nbm.csv`) and the vendor replaces the file under the same resource id (its `last_modified` was 2026-10-06T19:31:31.665985 in the snapshot and 2026-10-08T11:01:24.343784 on the first capture). The file name does change with each publication: three names are recorded, `pn_20261006_44_nbm.csv` (snapshot), `pn_20261008_27_nbm.csv` and `pn_20261016_46_nbm.csv` (the two bronze sidecars' `resource_filename`); `TODO: verify` whether a stable path exists. The second bronze capture is `bronze/neso_data_portal/obp_physical_notifications/2026/10/16/raw_20261016T204239Z_dfe1d229-e973-43c6-b5eb-c28ad59d7136_492a03ad.csv` (SHA-256 `492a03ad134b831c3b182dc74b4370d13b248837bd91f696695f9ecefd65ca4f`, 31,244,912 bytes, header plus 523,890 rows, ending in a newline). The first bronze capture is `bronze/neso_data_portal/obp_physical_notifications/2026/10/08/raw_20261008T111457Z_dfe1d229-e973-43c6-b5eb-c28ad59d7136_8f6a94d9.csv` (immutable, SHA-256 `8f6a94d98041bc5fab6e0f5e0a5c95e918666c3e72e07d7b2c639bc3e0e8a852`, UTF-8, LF line endings, no byte-order mark, header plus 495,086 rows).

## Families

### `obp_physical_notifications`

- Kind: tabular · archetype: EVT · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Data | `data` | string | — | yes | — | — |
| Unit ID | `unit_id` | string | — | no | — | — |
| Time From | `time_from` | datetime | `%Y-%m-%dT%H:%M:%S` | no | UTC | UTC |
| Level From | `level_from` | float64 | — | yes | — | MW |
| Time To | `time_to` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | UTC |
| Level To | `level_to` | float64 | — | yes | — | MW |

- Entity key: `unit_id`, `time_from`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`time_from`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Field meanings (vendor dictionary, saved field info).** `Data`: type of data, fixed value `PN`. `Unit ID`: "Registered Unit ID associated with the corresponding instruction" (example `ABERU-1`; the dictionary text mentions an "instruction" although this package holds PNs: it is word for word the `Unit ID` description of the OBP instructions dictionary. `TODO: verify` that the identifier space matches the other two OBP packages; the rows are consistent with it: in the 2026-10-16 capture, 21 of the 24 units in the instructions silver have PN rows (the three `RDP` units `NGED-004`, `NGED-005`, `UKPN-002` do not), and all 60 units in the availability silver do). `Time From`: window start datetime, UTC. `Level From`: PN at gate closure for the window start time, MW. `Time To`: window end time, UTC. `Level To`: PN at gate closure for the window end time, MW. `TODO: verify` that a segment is linearly interpolated between its two levels and what "gate closure" fixes for a segment that starts hours after it was declared: the dictionary states the levels only.

**Two clocks.**

1. **Vintage (`ckan_last_modified`).** The resource is an upload with a usable CKAN timestamp (record vintage `ckan_last_modified`, ADR-030). `published_at` and `available_at` are both the CKAN `last_modified` of the captured file, one value per capture: **2026-10-08T11:01:24.343784Z** on all 495,086 rows of the first capture and **2026-10-16T20:31:22.674649Z** on all 523,890 rows of the second (including the 495,086 rows it shares with the first). That is when the vendor last replaced the file, **not when each PN was declared**. `_latest` returns the newer capture, so through `_latest` every row, including a segment that started a year earlier, carries the 2026-10-16 `available_at`: an as-of query before 2026-10-16T20:31:22Z sees **no** row of this family there, and a point-in-time backtest cannot use it to say what a past PN looked like when it was declared. The record uses `LM` (last-modified) vintage as the conservative choice: no row is published earlier than its true availability, but the original declaration time, and whether past rows are later amended or removed, is not evidenced beyond the two captures (see Identity). `TODO: verify` the original availability of each declaration (needs publication or revision history).
2. **Event time (temporal recipe `utc_instant` on `time_from`).** `timestamp_utc` and `event_time` equal `time_from` on every row (checked on all rows): the **start of the segment, in UTC**. `time_to` is the segment end, typed UTC and kept but not the recipe column. The vendor does not state whether the end instant belongs to the segment: `TODO: verify` (INTERVAL-CLOSURE). `capture_written_at` (the gridflow capture time, one per capture: 2026-10-08T11:14:57Z and 2026-10-16T20:42:39Z) is carried on every row as an audit column and is **not** a data clock.

**Identity and selection.** The record key is `(unit_id, time_from)`: unique across all 495,086 rows in the body and in silver (0 duplicate rows, 0 full-body duplicates; K-AS-3 FACTS T04, C07). The vendor's resource metadata declares the same key for its datastore copy (`datastore_unique_keys: ["Unit ID", "Time From"]`, with `datastore_append_or_update: true`, catalogue snapshot `20261006T195819Z`); the CSV itself states no key. Whether a segment keeps its identity across later corrected re-publications is not documented: `TODO: verify` (cross-capture identity). Between the two captures (2026-10-08 and 2026-10-16) the file only grew: all 495,086 earlier rows reappear with the same `time_to` and levels, none is missing, and the 28,804 new rows all start at or after `2026-10-08T12:30:00`, the earlier file's last window end (front-end page check, 2026-10-23). One interval does not prove immutability. Measured uniqueness does not authorise `key_latest`, so `_latest` is `whole_capture`, the newest complete capture. A consumer must therefore not assume that dropping out of the file means a PN was withdrawn: no capture yet shows rows leaving the file (see Scope above), but if the vendor trims it, older history would exist only in older captures.

**Row counts and shape (silver, 2026-10-13).** 495,086 rows, 0 validation failures, 0 rows excluded; the planned and activated counts agree (@.planning/v0.22-RESULTS.md section AS-3b, RULINGS 752). Silver layout: one Parquet file per capture under `C:/gridflow-data/silver/neso_data_portal/obp_physical_notifications/year=2026/month=10/` (two by 2026-10-16: 495,086 and 523,890 rows; `_latest` returns the newer); the partition is the **capture** date, not the event date. Columns (14): the 6 vendor columns, then `timestamp_utc`, `published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id` and `dataset_version` (`1+e1`). All timestamps are tz-aware UTC. No gold view or builder reads this family. This family is 495,086 of the 645,817 rows of the three eligible OBP families activated in AS-3b (RULINGS 752).

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc

The vendor's declared update frequency is **ad hoc**, while its package text says the data is published continuously throughout the day. gridflow has **two captures**: 2026-10-08, and 2026-10-16 (`last_modified` 2026-10-16T20:31:22, 523,890 rows, a pure append of 28,804 rows; see Identity), so the real rhythm is still unmeasured. Two observations point to frequent refresh: the file's `last_modified` moved from 2026-10-06T19:31:31 (catalogue snapshot) to 2026-10-08T11:01:24 (capture), and the vendor datastore reported 495,354 rows at 2026-10-08T13:22Z (field-info run) against the 495,086 captured at 11:14Z (the two are different representations of the resource, the datastore and the uploaded file, so the difference is an observation, not a measured refresh delta). `TODO: verify` the refresh cadence, whether old rows are ever dropped, and whether each refresh replaces or appends, by comparing later complete captures with the hash-pinned body. The registry refresh is daily; the registry sets a 512 MiB download cap (`max_download_bytes` 536,870,912), against a 29.5 MB body, so the cap is not a near-term risk.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence). gridflow outputs derived from this package carry the attribution line "Supported by National Energy SO Open Data".

## Holds

- none

**No output of this package is held.** The single family was specified eligible (RULINGS 738) and activated as such (RULINGS 752), so there is no hold question or hold unit to state. The sibling AS-3b families that are held (the mock EAC and ORPS families) are different packages with their own pages; nothing here applies to them.

**Open questions that do not hold any output** (K-AS-3 FACTS section 6; carried as non-holding TODOs):

- `TODO: verify` the **original availability** of each declaration: the vintage is the file's last-modified time, never a declaration time.
- `TODO: verify` **cross-capture identity and immutability** of a `(unit_id, time_from)` segment: two captures eight days apart show a pure append (no row changed or dropped), which does not prove that later amendment or deletion never happens.
- `TODO: verify` **interval closure** (INTERVAL-CLOSURE): no source states whether a segment's end instant belongs to it.
- `TODO: verify` the **sign convention** of `level_from` and `level_to` (negative levels down to -49.9 MW occur on 42,083 rows for `level_from`) and the **interpolation** between a segment's two levels.
- `TODO: verify` the **stable download path**: the file name in the resource URL embeds a date.

**Known issues and gotchas.**

- **Same `available_at` for all history.** Every row of a capture carries that capture's `last_modified` (2026-10-08T11:01:24Z, then 2026-10-16T20:31:22Z; `_latest` shows the newer), however old the segment. Do not use this table to answer "what was declared when".
- **Declarations, not outturn.** A PN is a provider's declared position accepted by OBP; it is not metered. Do not compare it directly with metered generation or demand without that caveat.
- **Segments are not half-hours.** 400,690 rows are 1,800 s in the 2026-10-08 capture (416,661 in the 2026-10-16 one), the rest are shorter (down to 60 s). In the 2026-10-16 capture no window crosses a `:00` or `:30` boundary, windows of one unit never overlap, and a level often jumps between one window's end and the next one's start (37,502 contiguous pairs). Join on the instant, not on a settlement period; if you need half-hourly values, derive them from the segment ends explicitly and state the interpolation.
- **Zeros are declarations.** 407,637 zero `level_from` rows (and 407,238 `level_to`) in the 2026-10-08 capture are real values. Do not null or drop them.
- **Unit IDs are as served.** No normalisation: `unit_id` is not a BM unit ID and is not joined to BM-unit tables without a mapping that the vendor does not provide (`TODO: verify` whether a non-BM-to-register mapping exists).
- **`data` is constant.** It is `PN` on every row; it is kept as served and carries no information in this body.
- **Late-starting rows.** 150 segment starts are after the file's `last_modified` in the 2026-10-08 capture, 692 in the 2026-10-16 one (declared future positions). They are kept; the `available_at` of a future segment is therefore not later than its event time, but the declaration time is still unknown.

**Activation (2026-10-13, master `638b427`, PR #115).** The AS-3 research (RULINGS 736) read 26 families; the batch was split into AS-3a and AS-3b (RULINGS 737) and the specs ratified (RULINGS 738). AS-3b merged triple-green (RULINGS 751: CI green, the Sol diff review approved on the first pass with no findings, verification passed), with no engine change. This family was transformed from the 2026-10-08 capture with `--start/--end 2026-10-08`; there was no prior silver, so nothing was overwritten (RULINGS 752). The batch-wide `reconcile --all --cutoff 2026-10-12` exited 0 over 191 families with 0 gaps. The receipt is in @.planning/v0.22-RESULTS.md section AS-3b; the evidence is @.planning/phases/v0.22-K-AS-3/K-AS-3-FACTS.md (section 6) and the spec @.planning/phases/v0.22-K-AS-3/K-AS-3b-SPEC.md; the design is @docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md.

## Links

- [NESO Open Data Portal package](https://www.neso.energy/data-portal/obp-non-bm-physical-notifications)
- [Vendor field dictionary](https://www.neso.energy/data-portal/obp-non-bm-physical-notifications/non-bm_physical_notifications)
- Related packages: @./obp-non-bm-reserve-instructions.md, @./obp-reserve-availability-utilisation-price.md
- Registry record: @src/gridflow/connectors/neso_data_portal/registry/obp-non-bm-physical-notifications.json
- Domain: @../../../20-domain/concepts/bm-units.md
