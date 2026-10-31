---
source: "neso_data_portal"
package: "daily-demand-update"
dataset_key: "daily_demand_update"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Demand data update
  summary: >-
    NESO's daily file of half-hourly GB demand and interconnector flows, with embedded wind and
    solar estimates and seven days of their forecasts.
  facts:
    vendor: "NESO Data Portal, package Demand Data Update (`daily-demand-update`): one CSV, one FAQ"
    cadence: "Daily, NESO says, with settlement data about ten days late; recent outturn can change"
    grain: "Each row: one settlement period, marked outturn (`A`) or forecast (`F`)"
    history: "From the first day of the previous month to seven days ahead, NESO says"
  landscape: power
  what_it_is: >-
    One rolling CSV in MW: national demand (ND), transmission system demand (TSD), England and
    Wales demand, embedded wind and solar output and capacity, non-BM STOR, pumped storage pumping,
    the Scottish transfer and each interconnector's flow. NESO's FAQ says each half hour starts at
    the UK time given. NESO says it is like its historic demand data, but updated daily.
  how_used:
    - Recent half-hourly GB demand, before NESO's yearly historic files are filled
    - Embedded wind and solar output, which NESO estimates because it cannot meter it
  chart:
    type: line
    silver: neso_data_portal/daily_demand_update
    filter:
      - {column: bronze_capture_id, op: eq, value: "bronze/neso_data_portal/daily_demand_update/2026/10/16/raw_20261016T200140Z_177f6fa4-ae49-4182-81ea-0c6b35f26ca6_784eaeba.csv"}
      - {column: forecast_actual_indicator, op: eq, value: A}
    time: timestamp_utc
    values:
      - {column: nd, series: nd}
      - {column: embedded_wind_generation, series: wind}
      - {column: embedded_solar_generation, series: solar}
    aggregation: last
    window: {start: "2026-10-01", end: "2026-10-14"}
    unit: MW
  chart_view:
    title: National demand and embedded output, 1 to 14 October 2026
    caption: >-
      Silver `daily_demand_update`, MW: the outturn (`A`) rows of NESO's file of 16 October 2026,
      one point per half hour at its start in UTC. Embedded wind and solar are NESO's estimates.
      Forecast rows are not drawn.
    alt: >-
      Line chart from neso_data_portal/daily_demand_update, MW, one point per half hour, 1 to 14
      October 2026, from the outturn rows of NESO's 16 October 2026 file. National demand runs from
      17,165 at 05:00 UTC on 4 October to 34,694 at 17:30 UTC on 12 October. Embedded solar is 0 at
      night and highest at 11,648 on 1 October. Embedded wind runs from 221 on 11 October to 4,696 on
      13 October.
    x_label: half-hour start, UTC
    key:
      - {series: nd, label: National demand, paint: petrol}
      - {series: wind, label: Embedded wind, paint: horizon}
      - {series: solar, label: Embedded solar, paint: chartreuse}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then the CSV and the FAQ, each downloaded whole
      unless its `last_modified` is unchanged. Each download replaces the whole window.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=daily-demand-update"
      - "GET https://api.neso.energy/dataset/7a12172a-939c-404c-b581-a6128b74f588/resource/177f6fa4-ae49-4182-81ea-0c6b35f26ca6/download/demanddataupdate.csv"
      - "GET https://api.neso.energy/dataset/7a12172a-939c-404c-b581-a6128b74f588/resource/974b8c00-9058-4883-bf34-268e53ed9d15/download/faq-neso.docx"
    commands:
      - {run: gridflow ingest neso_data_portal daily_demand_update --last 24h, comment: "the CSV to bronze"}
      - {run: gridflow transform neso_data_portal daily_demand_update --last 24h, comment: "the capture's date to silver"}
      - {run: gridflow ingest neso_data_portal daily_demand_update_files --last 24h, comment: "the FAQ, bronze only"}
  record:
    select:
      filter:
        - {column: bronze_capture_id, op: eq, value: "bronze/neso_data_portal/daily_demand_update/2026/10/16/raw_20261016T200140Z_177f6fa4-ae49-4182-81ea-0c6b35f26ca6_784eaeba.csv"}
        - {column: settlement_date, op: eq, value: "2026-10-16"}
        - {column: settlement_period, op: ge, value: 14}
        - {column: settlement_period, op: le, value: 21}
      order_by: [settlement_period]
      columns: [settlement_date, settlement_period, forecast_actual_indicator, nd, tsd, england_wales_demand,
                embedded_wind_generation, embedded_solar_generation, embedded_wind_capacity,
                embedded_solar_capacity, pump_storage_pumping, scottish_transfer, published_at]
    key: [settlement_date, settlement_period, published_at]
    caption: "16 October 2026 in NESO's file of that day: outturn to period 17, then forecast rows."
    fields:
      settlement_date: The settlement day; NESO's FAQ says all times are UK time
      settlement_period: Half hour of the day; period 1 runs from 00:00 UK time
      nd: National demand, MW, excluding station load, pumping and exports
      forecast_actual_indicator: "`A` for outturn, `F` for forecast, as NESO marks each row"
      tsd: "Transmission system demand: ND plus station load, pumping and exports, MW"
      england_wales_demand: National demand on an England and Wales basis, MW
      embedded_wind_generation: "NESO's estimate of embedded wind output, which it cannot meter, MW"
      embedded_wind_capacity: "NESO's best view of embedded wind capacity, MW"
      embedded_solar_generation: "NESO's estimate of embedded solar output, MW"
      embedded_solar_capacity: "NESO's best view of embedded solar capacity, MW"
      non_bm_stor: Short-term operating reserve outside the Balancing Mechanism, MW
      pump_storage_pumping: Pumped storage pumping, MW, as NESO writes it
      scottish_transfer: Flow between Scotland and England and Wales, MW
      ifa_flow: "IFA interconnector flow, MW; positive into GB, negative out"
      ifa2_flow: "IFA2 interconnector flow, MW; positive into GB, negative out"
      britned_flow: "BritNed interconnector flow, MW; positive into GB, negative out"
      moyle_flow: "Moyle interconnector flow, MW; positive into GB, negative out"
      east_west_flow: "East West interconnector flow, MW; positive into GB, negative out"
      nemo_flow: "Nemo Link interconnector flow, MW; positive into GB, negative out"
      nsl_flow: "North Sea Link interconnector flow, MW; positive into GB, negative out"
      eleclink_flow: "ElecLink interconnector flow, MW; positive into GB, negative out"
      viking_flow: "Viking Link interconnector flow, MW; positive into GB, negative out"
      greenlink_flow: "Greenlink interconnector flow; the dictionary gives no unit, NESO's FAQ MW"
      timestamp_utc: Start of the settlement period, UTC
      published_at: "NESO's last-modified time for the file, read as UTC; one per file"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote the capture to bronze, UTC
  caveat: "Forecast rows carry zero demand and flows; NESO does not say whether zero means no forecast."
  notebook:
    lead: >-
      `query()` reads NESO's newest file, filtered on each half hour's start; the first cell
      converts times to UTC. The second sets outturn demand against forecast rows; the plot draws
      outturn only.
    cells:
      - |
        df = data.neso_data_portal.query("daily_demand_update", "2026-09-01", "2026-10-23")
        for c in ["timestamp_utc", "published_at"]:
            df[c] = df[c].dt.tz_convert("UTC")
        df.groupby(["published_at", "forecast_actual_indicator"]).timestamp_utc.agg(["count", "min", "max"]).reset_index()
      - |
        cols = ["nd", "tsd", "scottish_transfer"]
        spread = df.groupby("forecast_actual_indicator")[cols].agg(["min", "max"]).T
        spread.rename_axis(["column", "statistic"]).reset_index()
      - |
        outturn = df[(df.forecast_actual_indicator == "A") & (df.settlement_date < "2026-10-16")]
        daily = outturn.groupby("settlement_date").nd.agg(["min", "max"])
        ax = daily.plot(figsize=(8, 3.5), color=["#C77E3C", "#155A6E"], xlabel="settlement date",
                        ylabel="national demand, MW")
        ax.legend(["lowest half hour", "highest half hour"]);
    needs: "NESO's demand data update file of 16 October 2026"
    plot_alt: >-
      Line plot of the lowest and highest half-hour national demand of each day, MW, 1 September to
      15 October 2026, from the outturn rows of NESO's 16 October 2026 file. The lowest half hour falls
      to 14,180 on Sunday 20 September; the highest reaches 34,762 on 15 October. Both lines dip
      lowest at weekends.
  related:
    - {dataset: neso_data_portal/historic-demand-data, note: "NESO's yearly demand files; the 2026 file has this file's columns"}
    - {dataset: elexon/indo, note: "Elexon's initial national demand outturn, which NESO calls ND's equivalent"}
    - {dataset: neso_data_portal/embedded_wind_solar_forecast, note: "NESO's separate embedded wind and solar forecast, by settlement period"}
---

# Demand Data Update

GB electricity demand per settlement period (half-hour), published by NESO as one rolling
CSV on the Open Data Portal. Each row is one UK settlement date and period. It carries
**National Demand (ND)**, **Transmission System Demand (TSD)** and England and Wales demand,
NESO's estimates of embedded (distribution-connected) wind and solar generation and their
installed capacities, non-BM STOR, pump-storage pumping, the Scottish transfer, and the flow on
each GB interconnector. The vendor dictionary says ND is equivalent to the Initial National
Demand Outturn (INDO) on BM Reports, and TSD to the Initial Transmission System Demand Outturn
(ITSDO). gridflow ingests both from Elexon (@../../elexon/datasets/indo.md,
@../../elexon/datasets/itsdo.md). The resource description says the file covers outturn "from
the first day of the previous month up to the current day", plus forecast embedded wind and
solar generation for 7 days ahead. A `FORECAST_ACTUAL_INDICATOR` column marks each row as
outturn (`A`) or forecast (`F`). The package notes call it a faster sibling of the Historic
Demand Data package: it is updated daily, with roughly ten days' lag in receiving settlement
data. Use it for recent half-hourly demand and embedded-generation history before the historic
package catches up. Settlement periods follow @../../../20-domain/concepts/settlement-period.md.
The package notes also state, verbatim, "NESO have moved the data source to its new forecast
system". `TODO: verify` what that change altered (values, forecast tail, or timing) and from
when. The silver output is held because the forecast rows' zero demand is unexplained (see
Holds).

- Publisher group: Demand
- Registry group: demand · archetype: SER

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Demand Data Update | CSV | upload | `177f6fa4-ae49-4182-81ea-0c6b35f26ca6` |

- Download: [demanddataupdate.csv](https://api.neso.energy/dataset/7a12172a-939c-404c-b581-a6128b74f588/resource/177f6fa4-ae49-4182-81ea-0c6b35f26ca6/download/demanddataupdate.csv)
  (CKAN datastore active).
- Captured: `raw_20261008T100502Z_177f6fa4-ae49-4182-81ea-0c6b35f26ca6_9916942d.csv`,
  215,135 bytes, 2,160 data rows, one header epoch.

### DOC

| Resource | Format | Capture | Id |
|---|---|---|---|
| Frequently Asked Questions (FAQ) | DOC | upload | `974b8c00-9058-4883-bf34-268e53ed9d15` |

- Download: [faq-neso.docx](https://api.neso.energy/dataset/7a12172a-939c-404c-b581-a6128b74f588/resource/974b8c00-9058-4883-bf34-268e53ed9d15/download/faq-neso.docx)
  (CKAN `last_modified` 2024-10-21T13:26:14.945315).
- Captured: `raw_20261008T100506Z_974b8c00-9058-4883-bf34-268e53ed9d15_39ecfdf2.docx`,
  169,027 bytes. Catalogue only: no silver output. It is still primary evidence and is cited
  below. It states the unit (MW), that all times are UK time for the half-hour beginning, and
  that demand and flow values are half-hour averages. It also explains embedded-generation
  modelling and the settlement-derived interconnector flows (gridflow
  `@.planning/phases/v0.22-K-DEM-1/K-DEM-1-FACTS.md` C5). The Historic Demand Data package
  carries a byte-identical FAQ (same body hash).

## Families

### `daily_demand_update`

- Kind: tabular · archetype: SER · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| SETTLEMENT_DATE | `settlement_date` | date | `%Y-%m-%d` | no | — | — |
| SETTLEMENT_PERIOD | `settlement_period` | int64 | — | no | — | Number |
| ND | `nd` | float64 | — | yes | — | MW |
| FORECAST_ACTUAL_INDICATOR | `forecast_actual_indicator` | string | — | yes | — | Text |
| TSD | `tsd` | float64 | — | yes | — | MW |
| ENGLAND_WALES_DEMAND | `england_wales_demand` | float64 | — | yes | — | MW |
| EMBEDDED_WIND_GENERATION | `embedded_wind_generation` | float64 | — | yes | — | MW |
| EMBEDDED_WIND_CAPACITY | `embedded_wind_capacity` | float64 | — | yes | — | MW |
| EMBEDDED_SOLAR_GENERATION | `embedded_solar_generation` | float64 | — | yes | — | MW |
| EMBEDDED_SOLAR_CAPACITY | `embedded_solar_capacity` | float64 | — | yes | — | MW |
| NON_BM_STOR | `non_bm_stor` | float64 | — | yes | — | MW |
| PUMP_STORAGE_PUMPING | `pump_storage_pumping` | float64 | — | yes | — | MW |
| SCOTTISH_TRANSFER | `scottish_transfer` | float64 | — | yes | — | MW |
| IFA_FLOW | `ifa_flow` | float64 | — | yes | — | MW |
| IFA2_FLOW | `ifa2_flow` | float64 | — | yes | — | MW |
| BRITNED_FLOW | `britned_flow` | float64 | — | yes | — | MW |
| MOYLE_FLOW | `moyle_flow` | float64 | — | yes | — | MW |
| EAST_WEST_FLOW | `east_west_flow` | float64 | — | yes | — | MW |
| NEMO_FLOW | `nemo_flow` | float64 | — | yes | — | MW |
| NSL_FLOW | `nsl_flow` | float64 | — | yes | — | MW |
| ELECLINK_FLOW | `eleclink_flow` | float64 | — | yes | — | MW |
| VIKING_FLOW | `viking_flow` | float64 | — | yes | — | MW |
| GREENLINK_FLOW | `greenlink_flow` | float64 | — | yes | — | — |

- Entity key: `settlement_date`, `settlement_period`, `nd`, `forecast_actual_indicator`, `tsd`, `england_wales_demand`, `embedded_wind_generation`, `embedded_wind_capacity`, `embedded_solar_generation`, `embedded_solar_capacity`, `non_bm_stor`, `pump_storage_pumping`, `scottish_transfer`, `ifa_flow`, `ifa2_flow`, `britned_flow`, `moyle_flow`, `east_west_flow`, `nemo_flow`, `nsl_flow`, `eleclink_flow`, `viking_flow`, `greenlink_flow`
- Latest: `whole_capture`
- Temporal recipe: sp_pair (`settlement_date`, `settlement_period`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured resource: `2026-10-08T08:20:09.592329` for the first capture
   and `2026-10-16T08:20:10.800739` for the second, taken from each capture's sidecar. CKAN emits it without an
   offset, and gridflow reads it as UTC (gridflow
   `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`, D-15). Every silver row of a
   capture shares this one vintage. It says when the file changed, not when any individual
   outturn or forecast value was produced. The record has no issue time (issue recipe `none`).
2. **Event time (`sp_pair` on `settlement_date`, `settlement_period`).** `timestamp_utc` is the
   **start** of the settlement period: UK local midnight of the settlement date, plus 30
   minutes per period after the first, converted to UTC. `event_time` equals `timestamp_utc`.
   Event time is therefore **not** the capture time for this family. The FAQ settles the
   convention: "All times are UK time and for the half hour beginning" (FACTS C5, T02). The
   dictionary agrees: "Settlement period 1 runs from 00:00-00:30". Checked against silver on
   2026-10-09, the mapping holds on all 2,160 rows, `timestamp_utc` is unique, and every one of
   the 45 settlement dates has 48 periods. The capture window (2026-09-01 → 2026-10-15) holds no
   clock-change date, so the 46- and 50-period DST days are **unobserved** in data for this
   family. The conversion is the shared settlement helper, not family-specific code.

The local Elexon cross-check (FACTS §DEM1-1, C7) supports period start as corroboration only.
Daily ND joined to INDO matched exactly on 14 of 624 pairs mapped as period start, and on 0 of
625 mapped as period end. TSD against ITSDO matched on 1 of 433 either way, too sparse to decide
timing. Equality is not expected in general, because the vendor's values may be later
revisions of the initial Elexon outturns (`TODO: verify`, see Implementation delta). The FAQ, not these tallies, is the authority for period start.

**Units (vendor dictionary only, field info read 2026-10-08, gridflow
`@.planning/research/neso-snapshots/field-info/20261008T114228Z/daily_demand_update.json`;
package page [daily-demand-update](https://www.neso.energy/data-portal/daily-demand-update)).**
Every demand, embedded-generation, capacity, STOR, pumping, Scottish-transfer and
interconnector column is **MW** in the dictionary, except `GREENLINK_FLOW`. The dictionary has
no info block (title, description or unit) for `GREENLINK_FLOW`, which is why the generated
table above shows `—`. FACTS T01 settles it as **MW** from three sources: the FAQ's
dataset-wide answer (MW), the Historic Demand Data dictionary (which gives MW for the same
column), and the exact equality of the two packages on their overlap (C3). `SETTLEMENT_PERIOD`
has the dictionary unit `Number`, an ordinal. `FORECAST_ACTUAL_INDICATOR` has `Text`: a
category (`A` outturn, `F` forecast), not a physical value. Definitions worth keeping, from the
dictionary:

- **ND** excludes generation for station load, pump-storage pumping and interconnector exports.
  It is calculated from NESO operational generation metering.
- **TSD** = ND plus station load, pumping and exports. It "includes an estimate of station load
  of 500MW in BST and 600MW in GMT".
- **Embedded wind and solar** generation are model estimates of output NESO cannot meter. The
  capacities are NESO's "best view", not definitive.
- **Interconnector flows**: negative means export out of GB, positive means import into GB.
- **Pump storage pumping**: "the -ve signifies pumping load".

**Sentinels and missing values (FACTS g5).** The vendor declares no sentinel spelling, and the
record has no null-token map. Blank cells become null; this capture has none.

- **Zeros are preserved as values**, never converted to null. That includes the forecast rows'
  zero ND and TSD, which are the subject of the hold (see Holds).
- `-1` in signed flow columns is kept as a number. The vendor defines negative as export
  direction, so there is no global sentinel conversion.
- `TODO: verify` the sign of `PUMP_STORAGE_PUMPING`. The dictionary says negative signifies
  pumping load, but FACTS g5 records positive entries in the captured demand bodies. Values are kept
  unchanged until the vendor clarifies.
- `TODO: verify` the meaning of zero-valued `NON_BM_STOR`. The dictionary describes generation
  or demand reduction outside the ND generator definition. It does not say whether a zero means
  no service or no data (FACTS g5).

**Identity and selection.** The vendor pair `(SETTLEMENT_DATE, SETTLEMENT_PERIOD)` is unique
across the whole newest body (FACTS g3: 0 duplicates). It is still not the entity key. The
record validator requires an `sp_pair` key to strictly contain the pair, and no vendor
revision identity (run type, version, issue time) exists to add (FACTS T03,
`TODO: verify` explicit vendor revision identity). The entity key is therefore every column, a
**capture uniqueness guard**, not an identity. `_latest` is `whole_capture`: the newest capture
wins as a whole. No run type is invented to satisfy the key shape. Do not dedup across
captures on the pair alone. A pair delivered as `F` does return as `A`: of the 367 `F` rows of
the 2026-10-08 capture, 366 are `A` rows in the 2026-10-16 capture, each with a non-zero ND;
the 367th, 2026-10-15 SP48, is missing from the later body (see below).

**Row composition.** The first capture (2026-10-08) has 1,793 `A` rows (settlement dates
2026-09-01 → 2026-10-08 SP17) and 367 `F` rows (2026-10-08 SP18 → 2026-10-15). The forecast
tail starts part-way through the capture date. Two of its `A` rows, 2026-10-08 SP16 and SP17,
carry ND 0, TSD 500 (the stated station-load estimate alone), England and Wales demand 0 and
every flow 0; the second capture gives both periods full values. The second capture
(2026-10-16, `raw_20261016T200140Z_177f6fa4-ae49-4182-81ea-0c6b35f26ca6_784eaeba.csv`, 255,824
bytes, same header) has 2,542 rows: 2,175 `A` (2026-09-01 → 2026-10-16 SP17) and 367 `F`
(2026-10-16 SP18 → 2026-10-23). Its `A` rows include no zero ND. It lacks two periods,
2026-10-15 SP48 and 2026-10-16 SP1, so those dates have 47 rows; NESO gives no reason. Between
the captures, 24 `A` rows of 2026-10-07 and 2026-10-08 changed `EMBEDDED_SOLAR_GENERATION`
(two of them were the zero rows above); the other 1,769 shared `A` rows are unchanged. Both
captures are in silver (2,160 and 2,542 rows). `TODO: verify` whether the `F` rows' embedded wind and solar columns
are the forecasts the package notes describe. The vendor names those columns but does not
define the other columns on forecast rows.

**Relationship to Historic Demand Data (`historic_demand`).** The two packages share an
identical header. On their overlap (2026-09-01 → 2026-09-17, 816 settlement pairs), every
column is equal on every row (FACTS C3, §DEM1-4). Neither capture is a measured revision of the
other. The vendor says the historic package is populated 21 days in arrears and can receive
retrospective demand and solar corrections. It says this package has about ten days' lag.
`TODO: verify` cross-package revision precedence: the vendor states no rule that either package
overrides the other. A consumer may choose "historic first, daily as faster fallback" as an
explicit policy, but must not present it as a vendor hierarchy. It should also filter or
flag `F` rows. `historic_demand` was split out to unit DEM-1H (multi-resource selection and
mixed date formats; RULINGS 528) and is now in silver, held (ADR-039; RULINGS 535–537); see
@historic-demand-data.md.

**Activation (2026-10-09, master `73fde80`, PR #89).** The family was transformed with cutoff
2026-10-08 (one capture). Silver has **2,160 rows**, equal to the planned count. Reconcile
`--all` at cutoff 2026-10-08 found 0 gaps over 36 recorded families. No prior silver existed,
so nothing was overwritten (gridflow `@.planning/v0.22-RESULTS.md` §DEM-1; RULINGS 531–533).

Silver columns beyond the 23 vendor columns: `timestamp_utc`, `published_at`,
`bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id`,
`dataset_version` (all timestamps tz-aware UTC; `dataset_version` `1+e1` = record version 1
plus generic-engine version 1).

### `daily_demand_update_files`

- Kind: files · archetype: SER · refresh: daily · empty allowed: no
- files: catalogue only

This family captures the FAQ document (see DOC above). It produces no silver output. Its text is
the primary source for this page's unit and period-start statements.

Clocks: with no silver rows, there is no event time. The only clock is the document's vintage,
its CKAN `last_modified` (2024-10-21T13:26:14.945315, read as UTC).

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Status: Live

The resource description says: "This dataset is usually updated daily by 08:30 UTC." The
captures' CKAN `last_modified` values (2026-10-08T08:20:09.592329, 2026-10-16T08:20:10.800739)
fit that. gridflow captures one
snapshot per refresh run. The vendor's description implies a rolling window: outturn from the
first day of the previous month, plus a 7-day forward tail. A daily update can revise earlier
outturn rows: between the two captures, embedded solar changed on 24 outturn rows of 2026-10-07
and 2026-10-08 (see Row composition). `TODO: verify` how far back revisions
reach. No scheduled gridflow refresh exists yet, so captures are on demand. Two captures
(2026-10-08, 2026-10-16) exist to date.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `daily_demand_update`: held: TODO: zero ND/TSD on FORECAST_ACTUAL_INDICATOR = F rows: a forecast of zero or no forecast? (unit E-SEM)

The silver output exists on disk, but it is **held**: it is not eligible for publication or for
point-in-time model use until unit E-SEM answers the question above (RULINGS 529). On every
forecast-labelled (`F`) row in both captures (367 each), ND and TSD are zero, as are England and
Wales demand, STOR, pumping, the Scottish transfer and every flow; only the embedded wind and
solar columns carry values. The first capture also shows the zero pattern on its last two `A`
rows (see Row composition), so a zero ND is not confined to `F` rows. The vendor describes the
forward section as embedded-generation forecasts. It does not say whether a zero ND/TSD there
is a genuine forecast of zero demand or a placeholder for "no demand forecast". Converting the
zeros to null, publishing them as demand forecasts, and excluding them would each invent a
missing-value rule, so the values and the `A`/`F` flag are kept exactly as delivered (FACTS
§daily, g5). This note gives schema, units and row counts; the site page shows the rows, a chart
of outturn rows only and a notebook, with one line naming the zero question. A field-specific
vendor missing-value definition would settle the question.

The forward-target rule (RULINGS 529) does not apply here. It made the four current
cardinal-point demand forecasts eligible, because every target in those files falls after the
capture's CKAN `last_modified`, so the capture vintage is a valid issue proxy. This family is
held on a different question, the meaning of zero, not on its issue clock.

The package-level `eligibility: eligible` in the front matter refers to the package registry
entry. The hold is per family and sits on `daily_demand_update`.

Related holds in the same batch (gridflow `@docs/neso_data_portal/eligibility.md`): the four
historic forecast archives (issue-clock zone and meaning) and the 2–14-day half-hourly forecast
(whether `GDATETIME` labels the period end) are held, all unit E-SEM.

**Implementation delta (vendor dictionary vs record).**

- The dictionary types every value column as `integer` (`int4`). The record casts them to
  nullable `float64`, the batch rule for demand and flow columns.
- The dictionary's `SETTLEMENT_DATE` example is `01/01/2021`. The captured body uses
  `%Y-%m-%d`, which the record parses. The body is ground truth.
- The dictionary has no unit for `GREENLINK_FLOW`. MW comes from the FAQ and the historic
  dictionary (FACTS T01), not the daily dictionary.
- The dictionary calls ND "equivalent to" INDO and TSD to ITSDO. Measured equality against the
  local Elexon holdings is sparse (see the event-time section). `TODO: verify` whether the
  vendor values are later revisions of the initial outturns.
