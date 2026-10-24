---
source: "neso_data_portal"
package: "negative-reserve-active-power-margin-nrapm-forecast"
dataset_keys: ["nrapm_forecast_national_daily_days", "nrapm_forecast_scotland_daily_days", "nrapm_forecast_weekly_week_national", "nrapm_forecast_weekly_week_scotland"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-09
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Negative reserve active power margin forecast
  summary: >-
    NESO's forecast, 2 to 14 days ahead, of the MW nationally and in Scotland away from negative
    reserve active power margin risk.
  facts:
    vendor: "NESO Data Portal, package `negative-reserve-active-power-margin-nrapm-forecast`: four CSV files"
    cadence: Daily, as NESO lists the package; NESO gives no publication time
    grain: "One row per target date and cardinal point: `1B` overnight minimum, `3B` daily minimum"
  landscape: power
  what_it_is: >-
    NESO says a system negative reserve active power margin (NRAPM) warning may be issued when too
    little flexibility is available to keep generation matched to demand in low demand periods; it
    asks generators for more flexible parameters and flags a risk of emergency instructions. Each
    daily file gives forecast MW away from that risk, per target date and cardinal point.
  how_used:
    - Watch the forecast margin on low-demand days up to two weeks ahead
    - Read beside NESO's two-week national demand forecast for the same target dates
    - Track how one target date's margin moves between daily files as its lead shortens
  chart:
    type: line
    silver: neso_data_portal/nrapm_forecast_national_daily_days
    time: date
    filter:
      - {column: published_at, op: ge, value: "2026-10-16T00:00:00+00:00"}
    dedup: {"on": [date, cp], order_by: published_at}
    group: cp
    group_map: {"1B": overnight, "3B": daily}
    series_order: [daily, overnight]
    value: mw_away_from_risk_of_system_level_nrapm_forecast_conditions
    aggregation: last
    window: {start: "2026-10-18", end: "2026-10-30"}
    unit: MW
  chart_view:
    title: System margin from NRAPM risk, 18 to 30 October 2026
    x_label: target date, 2 to 14 days ahead
    y_min: 0
    caption: >-
      Silver `nrapm_forecast_national_daily_days`, MW, from the file NESO last modified at 08:00 on 16
      October 2026 (read as UTC): one value per target date and cardinal point. NESO does not say which
      sign marks risk.
    alt: >-
      Line chart from neso_data_portal/nrapm_forecast_national_daily_days: NESO's forecast MW away from
      a system-level NRAPM for target dates 18 to 30 October 2026, two lines. The daily minimum line
      sits above the overnight line on every date, from 20,104 on 19 October down to 7,914 on Saturday
      24 October, ending at 19,204. The overnight minimum peaks at 13,067 on 19 October, falls to its
      lowest, 3,363, on 24 October, and ends at 9,777.
    key:
      - {series: daily, label: Daily minimum, paint: petrol,
         note: "`3B`: the daily minimum, as NESO's file description names it"}
      - {series: overnight, label: Overnight minimum, paint: clay,
         note: "`1B`: the overnight daily minimum; this package gives no clock window"}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then each file downloaded whole unless its
      `last_modified` is unchanged. The file names carry no date.
    commands:
      - {run: gridflow pipeline neso_data_portal nrapm_forecast_national_daily_days --last 24h,
         comment: "national file to bronze, then silver"}
      - {run: gridflow pipeline neso_data_portal nrapm_forecast_scotland_daily_days --last 24h,
         comment: "Scotland file to bronze, then silver"}
  record:
    select:
      filter:
        - {column: date, op: in, value: ["2026-10-10", "2026-10-22", "2026-10-26"]}
      dedup: {"on": [date, cp, published_at], order_by: capture_written_at}
      order_by: [date, published_at, cp]
      columns: [date, cp, mw_away_from_risk_of_system_level_nrapm_forecast_conditions, published_at,
                timestamp_utc]
    key: [date, cp, published_at]
    caption: Both points on 10, 22 and 26 October 2026; 22 October is in two files.
    fields:
      date: The target date NESO forecasts for, sent as `YYYY-MM-DD`
      cp: "Cardinal point: `1B` overnight daily minimum, `3B` daily minimum, per NESO's file text"
      mw_away_from_risk_of_system_level_nrapm_forecast_conditions: Forecast MW away from a system-level NRAPM; NESO does not define the sign
      published_at: NESO's last-modified time for the file, read as UTC; rows carry no issue time
      timestamp_utc: Start of the target date's first settlement period, UTC; not a cardinal point's time
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      `tail()` reads each table's `_latest` view (the newest capture's rows, newest target date first),
      lineage columns dropped; `n=100` covers a file. Times arrive in the session zone, so the first
      cell converts them to UTC.
    cells:
      - |
        nat = data.neso_data_portal.tail("nrapm_forecast_national_daily_days", n=100)
        sco = data.neso_data_portal.tail("nrapm_forecast_scotland_daily_days", n=100)
        for df in (nat, sco):
            for c in ["timestamp_utc", "published_at", "capture_written_at"]:
                df[c] = df[c].dt.tz_convert("UTC")
        both = nat.merge(sco, on=["date", "cp"], suffixes=("_national", "_scotland")).rename(columns={
            "mw_away_from_risk_of_system_level_nrapm_forecast_conditions": "national_mw",
            "mw_away_from_risk_of_scotland_level_nrapm_forecast_conditions": "scotland_mw"})
        both = both.sort_values(["date", "cp"])
        both[["date", "cp", "national_mw", "scotland_mw", "published_at_national", "published_at_scotland"]]
      - |
        wide = both.pivot(index="date", columns="cp", values=["national_mw", "scotland_mw"])
        point = {"1B": "1B overnight", "3B": "3B daily"}
        wide.columns = [f"{level.removesuffix('_mw')} {point[cp]}" for level, cp in wide.columns]
        ax = wide.plot(figsize=(8, 3.5), marker="o", style=["-", "-", "--", "--"],
                       color=["#9A5B3C", "#155A6E", "#9A5B3C", "#155A6E"],
                       xlabel="target date", ylabel="MW away from NRAPM risk")
        ax.set_ylim(bottom=0)
        ax.legend(ncol=2, loc="lower center", bbox_to_anchor=(0.5, 1.0), frameon=False);
    needs: a recent capture of NESO's two daily NRAPM files
    plot_alt: >-
      Line plot of NESO's forecast MW away from NRAPM risk by target date, 18 to 30 October 2026: solid
      national, dashed Scotland, at 1B and 3B, axis from zero. National 3B falls from 20,104 on
      19 October to 7,914 on 24 October; national 1B dips to 3,363 that day, below Scotland's 4,369.
      Scotland stays between 4,032 and 6,827.
  related:
    - {dataset: neso_data_portal/2-14-days-ahead-national-demand-forecast, note: "Demand forecast for the same days, by cardinal point"}
    - {dataset: neso_data_portal/system-operating-plan-sop, note: "Control-room plan with negative reserve at each cardinal point, on the day"}
    - {dataset: neso_data_portal/daily-opmr, note: NESO's daily negative reserve requirement in MW}
    - {dataset: elexon/windfor, note: "Wind forecast; NESO's weekly NRAPM files tie the risk to wind output"}
  family:
    slug: negative-reserve-active-power-margin-nrapm-forecast
    members:
      - {dataset: nrapm_forecast_national_daily_days,
         differs: "National file: MW away from a system-level NRAPM, days 2 to 14",
         request: "GET https://api.neso.energy/dataset/64151a33-3075-437d-bf11-fc00f297520e/resource/4c391daa-14e2-4991-a476-5539033ebb3d/download/dailynrapmresult.csv"}
      - {dataset: nrapm_forecast_scotland_daily_days,
         differs: "Scotland-level MW away from risk, same dates and points; link to national unstated",
         request: "GET https://api.neso.energy/dataset/64151a33-3075-437d-bf11-fc00f297520e/resource/c2861f81-b400-4456-870e-d51a4b530331/download/scotdailynrapmresult.csv"}
      - {dataset: nrapm_forecast_weekly_week_national,
         differs: "Weekly rows, 2 to 52 weeks ahead: wind load factor and probability",
         request: "GET https://api.neso.energy/dataset/64151a33-3075-437d-bf11-fc00f297520e/resource/42377a3d-e202-475f-9069-dcd4d1fae952/download/weeklynrapmresult.csv",
         held: "The load factor and probability columns have no NESO unit or scale, and their labels disagree."}
      - {dataset: nrapm_forecast_weekly_week_scotland,
         differs: The same weekly layout for Scotland,
         request: "GET https://api.neso.energy/dataset/64151a33-3075-437d-bf11-fc00f297520e/resource/88f3e766-fff2-418c-aef2-4b627d2cdabd/download/scotweeklynrapmresult.csv",
         held: "The load factor and probability columns have no NESO unit or scale, and their labels disagree."}
---

# Daily & Weekly NRAPM (Negative Reserve Active Power Margin) Forecast

NESO's forecast of the risk of a **Negative Reserve Active Power Margin (NRAPM)**. That is a
condition where, in the vendor's words, there is insufficient flexibility available to ensure
that generation matches demand during low demand periods. The vendor's package notes say a system NRAPM warning asks generators for more
flexible parameters and tells participants there is a risk of **emergency instructions**. The
forecast exists to signal that risk to the market ahead of time. The package has four CSVs, a
national (system-level) and a Scotland version of each of two horizons:

- **Daily, 2–14 days ahead.** For each target date, two rows, one per demand **cardinal point**:
  `1B` (overnight daily minimum) and `3B` (daily minimum), per the vendor resource
  descriptions. Each row gives the forecast **MW away from risk** of an NRAPM under forecast
  conditions.
- **Weekly, 2–52 weeks ahead.** One row per week. The vendor resource descriptions call it the
  probability of seeing a wind load factor that would cause an NRAPM. Each row has a wind
  load-factor column and a probability column.

Use the daily files as a forward indicator of NRAPM risk in low-demand periods on the GB
system, and as context for Balancing Mechanism actions at the overnight daily minimum (1B) and
daily minimum (3B) (@../../../20-domain/markets/gb-balancing-mechanism.md). gridflow's own
inference, not vendor-stated: the files may also serve as a feature for negative-price and
curtailment risk (TODO: verify against a vendor or market source before relying on it). The
daily files are eligible for
publication. The weekly files' silver output is **held**, because their value columns have no
vendor unit or scale and their dictionary text contradicts itself (see Holds). Related margin
data: the `Negative Reserve` column of Daily OPMR (@daily-opmr.md) and Weekly OPMR
(@weekly-opmr.md), both held in the same batch.

- Publisher group: Generation
- Registry group: generation · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| National Daily 2-14 days NRAPM Forecast | CSV | upload | `4c391daa-14e2-4991-a476-5539033ebb3d` |
| Scotland Daily 2-14 days NRAPM Forecast | CSV | upload | `c2861f81-b400-4456-870e-d51a4b530331` |
| Weekly 2-52 week National NRAPM Forecast | CSV | upload | `42377a3d-e202-475f-9069-dcd4d1fae952` |
| Weekly 2-52 week Scotland NRAPM forecast | CSV | upload | `88f3e766-fff2-418c-aef2-4b627d2cdabd` |

All four are CKAN uploads with the datastore active. The file names are stable (no date token).
Captures are two per family, on 2026-10-08 and 2026-10-16, all with the epoch 1 header (bronze
headers checked 2026-10-24). The second daily captures are 664 and 649 bytes with 26 data rows
each; the second weekly captures 1,742 and 1,747 bytes with 55 each.

- National Daily 2-14 days NRAPM Forecast → `nrapm_forecast_national_daily_days` (eligible).
  Download: [dailynrapmresult.csv](https://api.neso.energy/dataset/64151a33-3075-437d-bf11-fc00f297520e/resource/4c391daa-14e2-4991-a476-5539033ebb3d/download/dailynrapmresult.csv).
  Captured: `raw_20261008T111424Z_4c391daa-14e2-4991-a476-5539033ebb3d_6a70ed41.csv`,
  660 bytes, 26 data rows.
- Scotland Daily 2-14 days NRAPM Forecast → `nrapm_forecast_scotland_daily_days` (eligible).
  Download: [scotdailynrapmresult.csv](https://api.neso.energy/dataset/64151a33-3075-437d-bf11-fc00f297520e/resource/c2861f81-b400-4456-870e-d51a4b530331/download/scotdailynrapmresult.csv).
  Captured: `raw_20261008T111428Z_c2861f81-b400-4456-870e-d51a4b530331_65a59a29.csv`,
  649 bytes, 26 data rows.
- Weekly 2-52 week National NRAPM Forecast → `nrapm_forecast_weekly_week_national` (**held**).
  Download: [weeklynrapmresult.csv](https://api.neso.energy/dataset/64151a33-3075-437d-bf11-fc00f297520e/resource/42377a3d-e202-475f-9069-dcd4d1fae952/download/weeklynrapmresult.csv).
  Captured: `raw_20261008T111431Z_42377a3d-e202-475f-9069-dcd4d1fae952_f7ceaa0f.csv`,
  1,745 bytes, 55 data rows.
- Weekly 2-52 week Scotland NRAPM forecast → `nrapm_forecast_weekly_week_scotland` (**held**).
  Download: [scotweeklynrapmresult.csv](https://api.neso.energy/dataset/64151a33-3075-437d-bf11-fc00f297520e/resource/88f3e766-fff2-418c-aef2-4b627d2cdabd/download/scotweeklynrapmresult.csv).
  Captured: `raw_20261008T111435Z_88f3e766-fff2-418c-aef2-4b627d2cdabd_f6d8d5f3.csv`,
  1,747 bytes, 55 data rows.

The package has **no DOC resources** and no `_files` family (gridflow
`@.planning/phases/v0.22-K-GEN-1/K-GEN-1-FACTS.md` GEN1-4).

**Column rename (vendor notice).** The package notes announced that on 5 August 2026 the daily
value column ids would change from `... NRAPM (Forecast Conditions)` to
`... NRAPM_Forecast Conditions`. The 2026-10-08 captures already carry the new `_Forecast
Conditions` spelling, and the records freeze only that epoch. A capture with the old spelling
would not match epoch 1. `TODO: verify` whether any older bodies with the pre-rename header
need a second epoch. None has been captured.

## Families

### `nrapm_forecast_national_daily_days`

- Kind: tabular · archetype: FC · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Date | `date` | date | `%Y-%m-%d` | no | — | — |
| CP | `cp` | string | — | yes | — | — |
| MW away from risk of System Level NRAPM_Forecast Conditions | `mw_away_from_risk_of_system_level_nrapm_forecast_conditions` | float64 | — | yes | — | MW |

- Entity key: `date`, `cp`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the CKAN
   `last_modified` of the captured resource: `2026-10-08T11:04:46.768036` for the first capture
   and `2026-10-16T08:00:44.528954` for the second, which CKAN emits without an offset. gridflow
   reads it as UTC (gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). Each
   capture's 26 silver rows share its vintage. The file has **no issue column**, and the record's
   issue recipe is `none`.
2. **Event time (`date_sp1` on `date`).** `timestamp_utc` = `event_time` = the start of
   settlement period 1 of the target date: UK local midnight of `date` in UTC (23:00 UTC the
   previous day during BST). Checked on every silver row on 2026-10-09. Event time is **not**
   the capture time. It is a **date anchor**: the `1B` and `3B` rows of a date share the same
   `timestamp_utc`. No intraday instant is built for a cardinal point, because the vendor gives
   no CP clock window in this package (FACTS §`nrapm_forecast_national_daily_days`).

**Why this family is eligible (forward-target rule, RULINGS 529, applied to GEN-1 by RULINGS
542).** Every target date in the capture falls after the capture's CKAN `last_modified`. The
earliest target anchor is 2026-10-09T23:00Z against a vintage of 2026-10-08T11:04Z in the first
capture, with 0 rows at or before the vintage (FACTS GEN1-1); in the 2026-10-16 capture it is
2026-10-17T23:00Z against 2026-10-16T08:00Z (silver checked 2026-10-24). The forecast was public at the vintage, before any of
its target days began. The CKAN vintage is therefore a conservative proxy for the missing issue
time. The GEN-1 tests pin this property for each eligible no-issue forecast. Eligibility holds
only while later captures keep it.

**What a capture contains.** The 2026-10-08 capture covers target dates 2026-10-10 to
2026-10-22: 13 dates, i.e. days 2 to 14 ahead. Each date has exactly two rows, `cp` = `1B` and
`3B`. The 2026-10-16 capture covers 2026-10-18 to 2026-10-30, again days 2 to 14 and two
rows per date. The two captures share target dates 18 to 22 October; all ten shared rows carry
different values (for example national `1B` on 22 October: 11,509 then 11,041), so `(date, cp)`
repeats across captures and only `published_at` tells them apart (silver checked 2026-10-24).
The vendor's CP dictionary entry explains cardinal points generically. The codes are
glossed only in the resource description ("overnight daily minimum 1B and daily minimum 3B").
`TODO: verify` the clock window of each CP. FACTS T01 records it as unspecified.

**Units (vendor dictionary only).** The value column is **MW**, declared in the field
dictionary (`unit: MW`) and in the resource description ("Forecast Megawatt (MW) away from
risk"). Do not rescale it (FACTS g4, GEN1-3).

**Sign.** The 2026-10-08 capture holds one negative value (national, `1B`, 2026-10-10: −2,862
MW); its other 25 rows are positive. All 26 rows of the 2026-10-16 capture are positive. The
vendor does not define the sign convention. The reading "a negative value is inside the NRAPM
risk zone" is plausible from the column name but is **not established**. `TODO: verify` the sign meaning with the NESO methodology. Values are kept as
published, with no bound imposed.

**Sentinels and missing values (FACTS g5).** No `N/A`, `NA` or literal `-1` tokens, no
value equal to −1, no blank cells, and no zeros. The record declares no null token. Silver has
no nulls in any column.

**Identity and selection.** `(date, cp)` is unique within each body (FACTS T02, C02), not across
captures (see above). No vendor text declares it a contractual key. `TODO: verify` the vendor key. `_latest` is
`whole_capture`: the newest capture replaces the previous one as a whole.

**Datastore count mismatch.** The vendor datastore reported `total: 52` records for this
resource when queried at 2026-10-08T13:20Z. The uploaded CSV captured two hours earlier has
26 rows. The Scotland datastore reported 26. `TODO: verify` whether the national datastore
holds a second set of rows (for example an appended earlier forecast) that the upload does not.
gridflow captures the upload, not the datastore.

National and Scotland are **separate forecast series**. They share target keys but the daily
values never coincide (FACTS GEN1-3). Whether the Scotland calculation is a component of the
national one is undocumented. Do not subtract one from the other or dedup across them.
`TODO: verify` geographical scope and additivity.

**Activation (2026-10-09, master `f19effb`, PR #92).** Transformed at cutoff 2026-10-08:
**26 silver rows**, equal to the planned count, with no prior silver overwritten. Reconcile
`--all --cutoff 2026-10-08` exited 0 with 0 gaps over 55 families (gridflow
`@.planning/v0.22-RESULTS.md` §GEN-1; RULINGS 545–546).

Silver columns beyond the vendor columns: `timestamp_utc`, `published_at`, `bronze_capture_id`,
`capture_written_at`, `event_time`, `available_at`, `source_run_id`, `dataset_version` (all
timestamps tz-aware UTC; `dataset_version` `1+e1`).

### `nrapm_forecast_scotland_daily_days`

- Kind: tabular · archetype: FC · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Date | `date` | date | `%Y-%m-%d` | no | — | — |
| CP | `cp` | string | — | yes | — | — |
| MW away from risk of Scotland Level NRAPM_Forecast Conditions | `mw_away_from_risk_of_scotland_level_nrapm_forecast_conditions` | float64 | — | yes | — | MW |

- Entity key: `date`, `cp`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = CKAN
   `last_modified` `2026-10-08T10:55:55.308683` for the first capture and
   `2026-10-16T08:00:47.844483` for the second (offset-less, read as UTC per ADR-030). Each
   capture's 26 rows share its vintage. No issue column; issue recipe `none`.
2. **Event time (`date_sp1` on `date`).** `timestamp_utc` = `event_time` = UK local midnight
   of the target date in UTC. Checked on every silver row on 2026-10-09. It is a date anchor,
   not the capture time, and not a CP-specific instant.

**Eligible (RULINGS 529/542).** Every target falls after the vintage: the earliest anchor is
2026-10-09T23:00Z against a vintage of 2026-10-08T10:55Z in the first capture, with 0 rows at or
before it (FACTS GEN1-1); in the 2026-10-16 capture it is 2026-10-17T23:00Z against
2026-10-16T08:00Z (silver checked 2026-10-24).

**Contents and units.** Same layout as the national file: target dates 2026-10-10 to
2026-10-22, two rows per date (`1B`, `3B`). The value column is **MW** (field dictionary
`unit: MW`; resource description "Forecast Megawatt (MW) away from risk of Scotland Level
NRAPM"). All values in both captures are positive. The sign convention is undocumented, as
for the national file. The 2026-10-16 capture covers 2026-10-18 to 2026-10-30; the ten rows for
18 to 22 October that both captures hold all differ in value (silver checked 2026-10-24).

**Sentinels (FACTS g5).** No null tokens, no −1, no blanks, no zeros. Silver has no nulls.

**Identity.** `(date, cp)` unique within each body (FACTS T02), not across captures.
`TODO: verify` the vendor key.
`_latest` is `whole_capture`. The vendor datastore total (26) matches the captured CSV.

**Activation (2026-10-09, master `f19effb`).** **26 silver rows**, equal to plan, nothing
overwritten, reconcile 0 gaps (gridflow `@.planning/v0.22-RESULTS.md` §GEN-1). Silver carries
the same eight lineage/clock columns as the national family.

### `nrapm_forecast_weekly_week_national`

- Kind: tabular · archetype: FC · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Week number | `week_number` | string | — | yes | — | — |
| Date | `date` | date | `%Y-%m-%d` | no | — | — |
| Wind Load Factor required to cause a System Level NRAPM | `wind_load_factor_required_to_cause_a_system_level_nrapm` | float64 | — | yes | — | — |
| Probability of seeing Wind load factor above | `probability_of_seeing_wind_load_factor_above` | float64 | — | yes | — | — |

- Entity key: `date`, `week_number`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Held (unit E-SEM).** This family's silver output exists but is not eligible for publication
or point-in-time use. This page gives schema, row counts and structure only. It gives **no data
values, ranges or value statistics**. See Holds.

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = CKAN `last_modified`
   `2026-10-08T10:46:06.065398` for the first capture and `2026-10-15T08:00:50.650020` for the
   second, captured 2026-10-16 (offset-less, read as UTC). Each capture's 55 rows share its
   vintage. No issue column; issue recipe `none`. The week label is a target, not an issue time (FACTS GEN1-1).
2. **Event time (`date_sp1` on `date`).** `timestamp_utc` = `event_time` = UK local midnight
   of `date` in UTC. Checked on every silver row on 2026-10-09. It is not the capture time.
   It anchors the **start date of the week** only. The record does not spread a row across the
   seven days of its week. The vendor `Date` is kept as published; it is not recomputed from
   the week label (FACTS T03).

All target anchors fall after the vintage: the earliest is 2026-10-24T23:00Z (FACTS GEN1-1).
That is **not** why the family is held. The hold is about units.

**Units: none declared.** Both value columns have an empty `unit` in the vendor dictionary.
No conversion is applied (FACTS g4, GEN1-3). In particular, gridflow does not decide whether the
load factor or the probability is a fraction or a percentage.

**Dictionary contradictions** (vendor
[national weekly dictionary](https://www.neso.energy/data-portal/negative-reserve-active-power-margin-nrapm-forecast/weekly_2-52_week_national_nrapm_forecast)):

- The column `Wind Load Factor required to cause a System Level NRAPM` has the **title** "Wind
  Load Factor required to cause a **Scotland** Level NRAPM" and a **description** about the
  *probability* of seeing such a load factor in Scotland.
- The column `Probability of seeing Wind load factor above` has a description of the *forecast
  wind load factor* required to cause a System Level NRAPM.
- The titles and descriptions thus appear to swap the two columns' roles, and one mislabels the
  geography. gridflow keeps the vendor **column ids** as the silver names and asserts neither
  reading. `TODO: verify` corrected field semantics with NESO.
- The `Date` description reads "Date at which forecast will occur. Given in (Coordinated
  Universal Time) UTC or UTC+1 during British Summer Time". A calendar date has no zone, so
  this does not change the date recipe. The Scotland dictionary calls the same field "the date
  commencing the week number".

**Structure of the capture** (no values). 55 rows, 55 distinct dates, 55 distinct week labels,
no nulls. Every `week_number` has the shape `<week>W<yy>` (vendor example `13W20`), kept as a
string. The `Date` values fall on Saturdays or Sundays, and consecutive dates are 6, 7 or 8 days
apart. `TODO: verify` NESO's week-commencing convention; it is not a fixed weekday in this
capture. 55 rows also exceeds the 51 weeks a "2–52 week" horizon would give. `TODO: verify`
what the extra rows cover. The registry keeps every published row.

The second capture (vintage 2026-10-15) has the same structure, 55 rows from 2026-11-01
(`44W26`) to 2027-11-14 (`45W27`), with one exception: week `35W27` is dated Monday
2027-08-30, where the first capture dated it Saturday 2027-09-04, so its steps include 2 and 13
days. 53 `(date, week_number)` keys appear in both captures; because the `35W27` date moved, the
key does not follow a week from one capture to the next (silver checked 2026-10-24).

**Sentinels (FACTS g5).** No `N/A`, `NA` or literal `-1` tokens, no value equal to −1, and
no blank cells. Zeros are kept as numbers; no vendor rule makes a zero a sentinel. Silver has no
nulls.

**Identity.** `(date, week_number)` is unique across the body (FACTS T04). `TODO: verify` the
vendor key. `_latest` is `whole_capture`.

**Activation (2026-10-09, master `f19effb`).** **55 silver rows**, equal to plan, nothing
overwritten (gridflow `@.planning/v0.22-RESULTS.md` §GEN-1). Held output stays on disk.

### `nrapm_forecast_weekly_week_scotland`

- Kind: tabular · archetype: FC · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Week number | `week_number` | string | — | yes | — | — |
| Date | `date` | date | `%Y-%m-%d` | no | — | — |
| Wind Load Factor required to cause a Scotland Level NRAPM | `wind_load_factor_required_to_cause_a_scotland_level_nrapm` | float64 | — | yes | — | — |
| Probability of seeing Wind load factor above | `probability_of_seeing_wind_load_factor_above` | float64 | — | yes | — | — |

- Entity key: `date`, `week_number`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Held (unit E-SEM).** Schema, row counts and structure only on this page; **no data values,
ranges or value statistics**. See Holds.

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = CKAN `last_modified`
   `2026-10-08T10:35:06.056281` for the first capture and `2026-10-15T08:00:53.901030` for the
   second, captured 2026-10-16 (offset-less, read as UTC). Each capture's 55 rows share its
   vintage. No issue column; issue recipe `none`.
2. **Event time (`date_sp1` on `date`).** `timestamp_utc` = `event_time` = UK local midnight
   of the week-commencing `date` in UTC. Checked on every silver row on 2026-10-09. Not the
   capture time; anchors the week's start date only. The earliest anchor, 2026-10-24T23:00Z,
   is after the vintage (FACTS GEN1-1). The hold is about units, not timing.

**Units: none declared**, and the dictionary contradicts itself (vendor
[Scotland weekly dictionary](https://www.neso.energy/data-portal/negative-reserve-active-power-margin-nrapm-forecast/weekly_2-52_week_scotland_nrapm_forecast)):

- The column `Wind Load Factor required to cause a Scotland Level NRAPM` is **titled** "...
  **System** Level NRAPM" and **described** as the *probability* of seeing a load factor that
  would cause an NRAPM in Scotland.
- The column `Probability of seeing Wind load factor above` is described as the *forecast wind
  load factor* required to cause a **System** Level NRAPM.
- Both `unit` fields are empty. No scale (fraction or percentage) is stated.

gridflow keeps the vendor column ids as silver names and applies no conversion.
`TODO: verify` corrected semantics and scale with NESO.

**Structure of the capture** (no values). 55 rows, 55 distinct dates and week labels, no
nulls, `<week>W<yy>` labels. Dates fall on Saturdays or Sundays with 6–8-day steps, as in the
national file. National and Scotland weekly share their target keys, but their rows are not
copies of each other (FACTS GEN1-3). Keep the families separate. The second capture moves
week `35W27` from 2027-09-04 to Monday 2027-08-30 exactly as the national file does.

**Sentinels (FACTS g5).** No null tokens, no −1, no blanks. Silver has no nulls.

**Identity.** `(date, week_number)` unique across the body (FACTS T04). `TODO: verify` the
vendor key. `_latest` is `whole_capture`.

**Activation (2026-10-09, master `f19effb`).** **55 silver rows**, equal to plan, nothing
overwritten (gridflow `@.planning/v0.22-RESULTS.md` §GEN-1).

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Daily

The four resources are updated separately. In the 2026-10-06 catalogue snapshot, the daily
files had a CKAN `last_modified` of 2026-10-06 (about 10:52–10:58) and the weekly files of
2026-10-01 (about 07:57–08:01). On 2026-10-08 all four had been modified that morning
(10:35–11:05, CKAN time read as UTC). So the weekly files are not necessarily rewritten every
day, even though the package says "Daily".

- `TODO: verify` the publication schedule of each file (daily for the 2–14-day files; daily or
  weekly for the 2–52-week files). Repeated captures will show it.
- `TODO: verify` whether a new publication replaces the whole file or revises only some
  target dates. `whole_capture` makes no assumption either way.
- Captures to date: two per family (2026-10-08 and 2026-10-16). The vintages seen so far are
  2026-10-06, 2026-10-08 and 2026-10-16 for the daily files (about 08:00 on the 16th) and
  2026-10-01, 2026-10-08 and 2026-10-15 for the weekly files, a week apart (CKAN time read as
  UTC).

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `nrapm_forecast_weekly_week_national`: held: TODO: the load-factor and probability columns have no vendor unit or scale, and the dictionary titles and descriptions contradict each other (unit E-SEM)
- `nrapm_forecast_weekly_week_scotland`: held: TODO: the load-factor and probability columns have no vendor unit or scale, and the dictionary titles and descriptions contradict each other (unit E-SEM)

Both weekly families are held by RULINGS 542 (seat ruling, PROXY-SOURCED), from FACTS
§`nrapm_forecast_weekly_week_*` and GEN1-3. The timing would pass the forward-target rule. The
problem is meaning: a user cannot tell which column is the load factor and which the
probability, nor whether either is a fraction or a percentage. Unit E-SEM must obtain a
corrected NESO dictionary, or methodology text, that states for each column:

1. What it measures (load factor required versus probability of exceeding it).
2. Its geography (system or Scotland).
3. Its numeric scale.

The ranges of the captured values are **not** evidence of scale. Until the hold lifts, the
silver output stays on disk and this page publishes no data values from it.

`nrapm_forecast_national_daily_days` and `nrapm_forecast_scotland_daily_days` are **eligible**
under the forward-target rule (RULINGS 529/542). The front matter's package-level
`eligibility: eligible` is the package registry entry. Holds are per family
(gridflow `@docs/neso_data_portal/eligibility.md`).

Related holds in the same batch: Daily OPMR (@daily-opmr.md) and Weekly OPMR (@weekly-opmr.md)
on issue-time and calendar questions; the 14-day wind current files
(@14-days-ahead-wind-forecasts.md) on past targets; the historic day-ahead wind archives
(@day-ahead-wind-forecast.md) on issue zone and availability. All are unit E-SEM.
