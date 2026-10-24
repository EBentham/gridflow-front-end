---
source: "neso_data_portal"
package: "viking"
dataset_keys: ["viking_link_ntc", "viking_ntc"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-09
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Viking Link - NESO's Net Transfer Capacity

NESO's **net transfer capacity (NTC) restrictions on the Viking Link interconnector**, the
GB–Denmark DC link. The package notes say these are the values NESO submits to the interconnector
capacity calculation, and that they restrict the maximum GB import and export flows. They are
given in MW per hourly time period, for the day-ahead and intraday auctions. They are **limits
NESO submitted, not measured flows and not the final capacity**. The notes say the final capacity
also uses values from the connected system operator and the interconnector's own capability, so
it may be lower than the NESO value. The final values are published by each interconnector's
trading facilitator, not in this package. NESO publishes a value only when it has applied a
restriction. A missing hour means no NESO restriction. It does not mean zero capacity, and it
does not give a nameplate figure ([package page](https://www.neso.energy/data-portal/viking)).

Use: a model of GB cross-border flows or of interconnector price coupling can use these as
NESO-side **directional ceilings**: hours when the GB system operator capped Viking imports or
exports, and the reason it gave. Each row carries two separate directional maxima. `To GB` is the
import limit (Denmark → GB) and `From GB` is the export limit (GB → Denmark). They are never one
signed net-flow series (gridflow `@.planning/phases/v0.22-K-IC-1/K-IC-1-FACTS.md` §4 IC1-1).
Related pages: the other NESO interconnector packages @eleclink.md, @ifa.md, @ifa2.md,
@nemolink.md and @nsl.md. ENTSO-E cross-border capacity is in
@../../entsoe/datasets/net_transfer_capacity.md. The local ENTSO-E silver has **no GB–Denmark
rows**, so no cross-source check of Viking was possible (FACTS IC1-1).

The package has two resources and gridflow keeps them as **two families**:

- `viking_link_ntc`: the **current** resource, a CKAN datastore dump. Each row has a GMT
  publication time and an hourly GMT target start.
- `viking_ntc`: the **archive**, a static CSV upload. Each row has an operational-date label, an
  hourly-period label and a version. It has no publication time.

**Both outputs are held (unit E-SEM).** For the current dump, NESO does not say that past rows
are unchanged since their upload time. For the archive, the operational-date calendar is
undocumented. See Holds. Both outputs exist in silver, but neither can be published or used for
point-in-time modelling until E-SEM answers its question (RULINGS 565, 567). **This page gives
schema, clocks, row counts and structural counts only. It gives no data values.**

- Publisher group: Interconnectors
- Registry group: interconnectors · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Archived Viking NTC Data | CSV | upload | `0d20456e-85cc-47a9-b476-e2d8e7c1b8eb` |
| Viking Link NTC Data | CSV | dump | `f4ee9a34-1bb5-405e-b4a0-bacb193fb188` |

Both resources are SILVER. The package has no DOC resources, so there is no methodology document
and no `_files` family. Package id `53a942cc-f9ab-4ad3-a274-5beed51635ec`. The registry,
the 2026-10-06 catalogue snapshot and both bronze sidecars all carry this id. The research note
in FACTS about a package-id mismatch was checked and rejected: the ids are equal (RULINGS 565).

- **Viking Link NTC Data** → `viking_link_ntc` (held).
  Download (datastore dump): [f4ee9a34-1bb5-405e-b4a0-bacb193fb188](https://api.neso.energy/datastore/dump/f4ee9a34-1bb5-405e-b4a0-bacb193fb188).
  Captured: `raw_20261008T114058Z_f4ee9a34-1bb5-405e-b4a0-bacb193fb188_8ee22a46.csv`,
  1,781,337 bytes, 19,775 rows. The CKAN datastore total on 2026-10-08 was also 19,775.
  Vendor dictionary: [Viking Link NTC Data](https://www.neso.energy/data-portal/viking/viking_link_ntc_data).
- **Archived Viking NTC Data** → `viking_ntc` (held).
  Download: [archived_viking_data-1.csv](https://api.neso.energy/dataset/53a942cc-f9ab-4ad3-a274-5beed51635ec/resource/0d20456e-85cc-47a9-b476-e2d8e7c1b8eb/download/archived_viking_data-1.csv).
  Captured: `raw_20261008T114101Z_0d20456e-85cc-47a9-b476-e2d8e7c1b8eb_550219c0.csv`,
  400,903 bytes (equal to the declared content length), 6,456 rows. The CKAN datastore total was
  also 6,456. Vendor dictionary: [Archived Viking NTC Data](https://www.neso.energy/data-portal/viking/archived_viking_ntc_data).

Both bodies match their sidecar SHA-256 and byte length (FACTS §1, C-VERIFY). Each resource has
one capture to date, made on 2026-10-08, and one header epoch.

**Column rename on the current resource.** The resource description says NESO renamed four column
ids on **2026-09-17**:

- `Data Upload Time (GMT)` → `Data Upload Time GMT`
- `Operational Period Start Date & Time (GMT)` → `Operational Period Start Date and Time GMT`
- `Flow (MW) To GB` → `Flow in MW To GB`
- `Flow (MW) From GB` → `Flow in MW From GB`

gridflow has captured only the post-rename header, so the record has only that one epoch. It
does not invent a pre-rename epoch it never observed. If an older body with the old header is
ever ingested, it needs a second epoch. `TODO: verify` whether NESO serves the old header
anywhere (FACTS IC1-4).

**How the two resources relate.** The archive's target labels end where the current dump's
targets begin, in late September 2024 (measured boundaries in FACTS §4 IC1-4). Joining them on
target label plus compacted auction finds **2 shared keys, and the directional values differ on
both**. This uses the literal labels. Under a hypothetical shifted rollover there are 0 shared
keys. The archive's operational-date rollover is undocumented, so gridflow does not join or
deduplicate across the two families (FACTS IC1-4, C-OVERLAP). Each family uses a single-resource
`whole_capture`.

## Families

### `viking_link_ntc`

- Kind: tabular · archetype: FC · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Data Upload Time GMT | `data_upload_time_gmt` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | ISO 8601 |
| Auction Type | `auction_type` | string | — | yes | — | — |
| Operational Period Start Date and Time GMT | `operational_period_start_gmt` | datetime | `%Y-%m-%dT%H:%M:%S` | no | UTC | ISO 8601 |
| Flow in MW To GB | `flow_to_gb_mw` | float64 | — | yes | — | MW |
| Reason For Restriction To GB | `reason_for_restriction_to_gb` | string | — | yes | — | — |
| Flow in MW From GB | `flow_from_gb_mw` | float64 | — | yes | — | MW |
| Reason For Restriction From GB | `reason_for_restriction_from_gb` | string | — | yes | — | — |

- Entity key: `issue_time`, `auction_type`, `operational_period_start_gmt`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`operational_period_start_gmt`)

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

**Held (unit E-SEM). Schema, clocks and counts only, no data values.**

**The two clocks for this family:**

1. **Vintage (`capture_fallback`, not `ckan_last_modified`).** This resource is a datastore dump.
   Under ADR-035 P-10, a family holding a datastore resource takes `capture_fallback` and nothing
   else (gridflow `@docs/DECISION_LOG/ADR-035-neso-datastore-dump-leg.md`). So `published_at` is
   **null** on every row, and `available_at` = `capture_written_at`, the sidecar `written_at`:
   `2026-10-08T11:40:58.152573Z`. Checked on all 19,775 silver rows on 2026-10-09. The sidecar
   does record a CKAN `last_modified` (`2026-09-17T09:02:57.546341`), the same day as the column
   rename. gridflow does not use it as the vintage, because a dump's CKAN `last_modified` is not
   the time its rows were published. The vintage says only when gridflow first held the values.
   It is not when NESO published them.
2. **Event time (`utc_instant` on `operational_period_start_gmt`).** `timestamp_utc` =
   `event_time` = `operational_period_start_gmt` on every row: the GMT (= UTC) **start** of a
   one-hour restriction period. The vendor comment says a period labelled `2022-10-20T22:00:00`
   covers 22:00 to 23:00 on that date (dictionary example, not a captured row). So a row applies
   to `[timestamp_utc, timestamp_utc + 1h)`. It is not the capture time.

**Issue time.** The record declares `Data Upload Time GMT` as the issue column
(`issue: data_column`). The vendor describes it as the "Date and time that data was published",
in GMT. gridflow copies it to `issue_time`, UTC, on every row, and `issue_time` is in the entity
key as the record contract requires. It is **not** an availability override (FACTS g2, T05):
gridflow does not backdate `available_at` to it, because NESO does not say that a dump row is
unchanged since its upload time.

**DST check (FACTS IC1-3, C-DST).** Group the distinct target starts by UTC date and every
checked transition date has 24 hours. Group them by Europe/London date and the spring date
(2025-03-30) has 23 and the autumn date (2025-10-26) has 25. That is what genuine UTC instants
produce, which supports the vendor's GMT labelling.

**Why it is held.** This is a current dump, yet most of its rows are for past hours. Of the
19,775 rows, 19,731 have a target before the capture time and 44 after. Against each row's own
upload time, 421 targets fall before `Data Upload Time GMT` and 19,354 after (FACTS §2, §4
IC1-6). The issue column says when a row was first published. Nothing from NESO says the
**values** returned today for a past hour are the values that were current at that upload time,
so historically issued limits are not evidenced. The forward-target rule (RULINGS 529) does not
settle a family that has an issue column.

**Identity.** `(issue_time, auction_type, operational_period_start_gmt)` is unique over the full
body (also checked on silver). `(auction_type, operational_period_start_gmt)` alone is **not**
unique: 192 rows repeat an earlier row's pair, so one target hour has several uploads per auction.
No vendor primary key is declared, so the key is a capture guard and `_latest` is
`whole_capture`. The newest capture wins as a whole. `TODO: verify` the vendor's revision key and
whether a later upload supersedes an earlier one for the same hour and auction (FACTS T04, g3).

**Auctions.** The vendor field is "Day-ahead (DA) or Intraday (ID) auction". The body has five
raw spellings: `Day Ahead`, `Intraday 1`, `Intraday 2`, `Intraday 3`, `Intraday 4`, each with a
space. They are kept byte-identical and never whitespace-compacted. The archive spells the same
categories without spaces (see `viking_ntc`).

### `viking_ntc`

- Kind: tabular · archetype: FC · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Operational Date | `operational_date` | string | — | yes | — | ISO 8601 |
| Auction Type | `auction_type` | string | — | yes | — | — |
| Version | `version` | string | — | yes | — | — |
| Hourly Time Period (GMT) | `hourly_time_period` | string | — | yes | — | — |
| Flow (MW) To GB | `flow_to_gb_mw` | float64 | — | yes | — | MW |
| Flow (MW) From GB | `flow_from_gb_mw` | float64 | — | yes | — | MW |
| Reason For Reduction | `reason_for_restriction` | string | — | yes | — | — |

- Entity key: `operational_date`, `auction_type`, `hourly_time_period`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Held (unit E-SEM). Schema, clocks and counts only, no data values.**

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the capture's CKAN
   `last_modified`, `2024-12-18T11:32:34.909486`. CKAN emits it without an offset and gridflow
   reads it as UTC (gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). There
   is one distinct value over all 6,456 rows. The file has **no issue column**, and `Version` is
   not one, so the issue recipe is `none` and the vintage is the only availability clock. Every
   target label is earlier than this vintage (FACTS IC1-6).
2. **Event time (`none`).** The temporal recipe is `none`, so `timestamp_utc` = `event_time` =
   the **capture time**, `2026-10-08T11:41:01.546781Z` (`written_at` of the bronze capture). Both
   columns equal it on every row. **It is not the hour the restriction applies to.** The target
   is carried only by the two raw labels, `operational_date` and `hourly_time_period`. Both are
   kept as strings and not converted to an instant, because NESO does not document how they map
   to a calendar (see Hold question). A consumer must not read `timestamp_utc` as the target
   hour.

**Hold question.** The vendor calls `Operational Date` the "Operational Date for which restriction
applies" and `Hourly Time Period (GMT)` the "Hourly time period for which restriction applies".
It does not say which calendar the operational date belongs to or when it rolls over, so the
hourly GMT period cannot be attached to it reliably. Structurally, the spring-transition label
`20240331` has **24** distinct hourly periods, so it cannot be read as a complete UK-local civil
day (that day had 23 hours). The labels therefore stay raw (FACTS §2 T03, §4 IC1-3, C-DST).
The archive also has no issue time and every target precedes the upload's `last_modified`, so
the forward-target rule (RULINGS 529) cannot release it.

**Raw labels.**

- `operational_date`: the vendor dictionary types it `date` with the example `2022-10-20`.
  Every body value parses as `%Y%m%d`, without hyphens. gridflow keeps it as a **string** and
  does not type it as a date, because no operational calendar is evidenced (K-IC-1-SPEC column
  conventions).
- `hourly_time_period`: an `HH:MM to HH:MM` GMT range (dictionary example `22:00 to 23:00`),
  kept byte-identical.
- `version`: the dictionary types it `integer` but gives no description, example or unit. The
  body uses zero-padded three-digit labels, with 2 distinct values. It is kept as a string so the
  padding survives. It is **never** used as an issue time or for revision ordering (FACTS T02).
  `TODO: verify` with NESO what Version means and whether a higher version supersedes a lower one.
- `auction_type`: three raw spellings, `DayAhead`, `Intraday1` and `Intraday2`, without spaces.
  They are kept byte-identical and differ from the current resource's spellings.

**Identity.** `(operational_date, auction_type, hourly_time_period)` is unique over the full body
(also checked on silver). No vendor primary key is declared, so the key is a capture guard and
`_latest` is `whole_capture` (FACTS T04, g3). `TODO: verify` the vendor key, and in particular
whether `version` should be part of it.

### Both families

**Units (vendor dictionaries only; CKAN datastore field info read 2026-10-08, linked above).**
All four flow columns are **MW**. Each is described as "Maximum flow in this direction", and the
headers carry MW explicitly. The dictionaries type them `integer` (CKAN `int4`). gridflow casts
them to float64, which leaves integer values unchanged. Each is a **directional maximum
transfer limit**, never signed: `To GB` = import, `From GB` = export (FACTS g4, IC1-1). Reason,
auction and version columns are text and have no unit. The time columns are ISO 8601 / GMT labels.

**Sentinels and missing values (FACTS g5).** No null-token map is declared. Full-body checks on
both captures found no negative directional values, no `-1`, no non-numeric flow cells, no
literal `NA` or `N/A`, and no blank flow cells. Both directions are populated on every row. The
reason columns are blank in no row. No vendor column is null in silver. The dictionaries'
`N/A` and `N/Q` entries are metadata comments, not CSV sentinels. Both bodies **contain literal
zero limits**, including multi-hour runs of zeros in the current dump. No vendor source says
zero means missing, so zeros stay numeric zero and are never converted to null. Hours with no
row are not filled: the package notes say a missing value means NESO applied no restriction. The
bodies also carry explicit "no restriction" reason rows. `TODO: verify` with NESO whether a zero
limit means a full outage of the direction or something else.

**Activation (2026-10-09, master `6cccc4e`, PR #95).** Cutoff 2026-10-08, no prior silver, so
nothing was overwritten. Rows: `viking_link_ntc` **19,775** and `viking_ntc` **6,456**, both
equal to the planned counts. Each family holds one Parquet file under `year=2026/month=10`. The
full `reconcile --all --cutoff 2026-10-08` run exited 0 over 69 families with 0 open gaps.
Neither Viking family needed an adjudication (gridflow `@.planning/v0.22-RESULTS.md` section
IC-1; RULINGS 566, 567).

Silver columns beyond the vendor columns: `viking_link_ntc` adds `issue_time`, and both add
`timestamp_utc`, `published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`,
`available_at`, `source_run_id` and `dataset_version`. All timestamps are tz-aware UTC.
`dataset_version` `1+e1` = record version 1, epoch 1.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc

"Ad hoc" is the only vendor statement of cadence. The package publishes only when NESO applies a
restriction, so gaps in time are expected. `TODO: verify` how often the current datastore resource
is appended and whether past rows are rewritten. The archive upload has not changed since its
`last_modified` of 2024-12-18, and it looks closed (its targets end where the current resource
begins). `TODO: verify` with NESO that the archive will not be re-uploaded. gridflow's refresh
captures one state of the dump per run, so any rewrite between runs is lost. The dated silver
captures are therefore a sample of the vendor's state, not a full revision history. No scheduled
gridflow refresh exists yet. Captures are on demand.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `viking_link_ntc`: held: TODO: the dump returns past targets (rows before the capture) and NESO does not state that a row is unchanged since its `Data Upload Time GMT`, so historical issued limits are not evidenced. (unit E-SEM)
- `viking_ntc`: held: TODO: the archive's operational-date rollover and GMT/BST interpretation are undocumented, and every target precedes the upload's last_modified, so the forward-target rule (RULINGS 529) cannot apply. (unit E-SEM)

Both held outputs exist in silver, but they cannot be published or used for point-in-time
modelling until unit E-SEM answers its question (RULINGS 565, 567). This page publishes their
schema, clocks, row counts and structural counts only. It publishes no data value, sample row
or value statistic for either family. Each hold applies to the captured bodies and to later
captures until NESO gives what it asks for: for `viking_link_ntc`, a retention or revision
guarantee or immutable issue-specific files; for `viking_ntc`, the operational-date calendar,
its rollover and the meaning of `Version`.
