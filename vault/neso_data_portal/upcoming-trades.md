---
source: "neso_data_portal"
package: "upcoming-trades"
dataset_key: "upcoming_trades"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-12
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Upcoming trades

This package is NESO's **Upcoming trades** table: the agreed electricity trades that have **not started
delivery**, one row per trade per settlement period (NESO trading material, as read in the batch research).
The CKAN notes say that, to meet its forecast balancing requirements at minimum cost, NESO trades
energy-related products; the table "displays all upcoming electricity trades due to be delivered" and is
refreshed every ten minutes. The resource description names the trades as GTMA (Grid Trade Master Agreement)
trades. Background: @../../../20-domain/markets/gb-balancing-mechanism.md and
@../../../20-domain/concepts/settlement-period.md. `TODO: verify` how these trades relate to the balancing
mechanism and to outturn or settlement data; this page makes no such claim.

The vendor warns that the trade details are **provisional and subject to correction**, in particular
after the usual trade confirmation with the counterparty, and "should not therefore be relied upon"
(CKAN package notes; NESO terms and conditions apply). The delivered history lives in the sibling package,
@./historic-gtma-grid-trade-master-agreement-trades-data.md; the two are different tables whose volume
labels and semantics differ (historic upload tables: total MWh; the FY datastore table: average MW; this
table: MWh labelled "Average Volume"; see Holds), not one table split in time.

These are **trading events, not settlement accounting runs**. `SO_Flag` and `Reason` are not a `run_type`;
no `run_type` is fabricated and none applies (RULINGS 707).

**The silver output is HELD.** It exists on disk (28 rows from one capture) but may not be published or
used for point-in-time work until the volume quantity and the `Last_Updated` clock are settled (see Holds).
**No data values are given on this page.** Row counts and the schema are the only facts stated about the
captured rows.

- Publisher group: Trading
- Registry group: trade-data · archetype: REG
- Package page: [Upcoming trades](https://www.neso.energy/data-portal/upcoming-trades-0) (CKAN package
  name `upcoming-trades`, id `932245c1-2322-4515-bf5e-ea2093ba1333`; the vendor page URL carries a `-0` suffix)
- Attribution: Supported by National Energy SO Open Data

## Files by disposition

The package has **one resource**, a CKAN datastore table served as a CSV dump: **1 SILVER, 0 DOC, 0 HOLD**.
SILVER here means the file is a candidate data file for its family; because the family's hold is set at
record level, the silver table exists but is not publishable. There are **no DOC files, so there are no
document downloads**. The resource is fetched from the datastore dump endpoint:

- [Upcoming Trades (datastore dump)](https://api.neso.energy/datastore/dump/0b7e84ec-eded-4458-b111-d29ba4508e85)
  · CSV · resource id `0b7e84ec-eded-4458-b111-d29ba4508e85` · `url_type` datastore · CKAN
  `last_modified` 2026-10-06T12:30:13 in the 2026-10-06 catalogue snapshot
  (`catalog_snapshot_20261006T195819Z`) and 2026-10-08T11:30:04 in the capture sidecar
  (`request_params.ckan_last_modified`); what that stamp measures is unverified (see Clocks).

The CKAN resource declares no byte size or hash. The captured body is described under Bronze capture.

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Upcoming Trades | CSV | dump | `0b7e84ec-eded-4458-b111-d29ba4508e85` |

## Families

### `upcoming_trades`

- Kind: tabular · archetype: REG · refresh: daily · empty allowed: yes

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| ID | `id` | string | — | no | — | — |
| Date | `date` | date | `%Y-%m-%d` | no | — | — |
| SP | `sp` | int64 | — | no | — | — |
| Volume | `volume` | float64 | — | yes | — | MWh |
| Price | `price` | float64 | — | yes | — | £/MWh |
| Cost | `cost` | float64 | — | yes | — | £ |
| SO_Flag | `so_flag` | string | — | yes | — | — |
| Reason | `reason` | string | — | yes | — | — |
| Note | `note` | string | — | yes | — | — |
| Last_Updated | `last_updated` | string | — | yes | — | — |

- Entity key: `id`, `date`, `sp`
- Latest: `whole_capture`
- Temporal recipe: sp_pair (`date`, `sp`)

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

**What it is.** One row per trade per settlement period of delivery. One trade that spans several
half-hours appears as several rows: in the capture, 14 trade ids each appear in more than one period,
giving 28 rows, so `id` alone is not a key. Both `(id, sp)` and `(id, date, sp)` are unique in the
capture; the registry key is `(id, date, sp)` so that the complete temporal pair is in the key. The key is
never reduced to `(date, sp)`: several trades share a period. No vendor guarantee of permanent
uniqueness of the identifier was found.

**Vendor dictionary** (CKAN resource field info, snapshot `20261006T195819Z`, as read in the batch
research, @.planning/phases/v0.22-K-TRD/K-TRD-FACTS.md in the gridflow checkout):

| Column | Vendor title and description | Vendor unit |
|---|---|---|
| `ID` | "Trade ID": ID of the GTMA trade (the dictionary spells it "GMTA") | none |
| `Date` | "Settlement date": settlement date of the trade | none |
| `SP` | "Settlement period": settlement period number that the trade is delivered | none |
| `Volume` | "Average Volume": average volume of trade | MWh |
| `Price` | "Price": price of the trade | £/MWh |
| `Cost` | "Cost": cost of the trade to National Grid ESO; comment "Cost = Price * Volume * Duration" | £ |
| `SO_Flag` | "System Flag": whether the action was potentially taken for reasons other than balancing the short-term energy imbalance (`T` system security, `F` balancing, per the dictionary comment) | none |
| `Reason` | "Trade Reason": detailed reason, e.g. voltage, thermal constraints, ROCOF, upwards margin, downwards reserve | none |
| `Note` | "Note": notes or comments | none |
| `Last_Updated` | "Last Updated": date and time the information was last updated | none |

The vendor comments give the sign convention of `Volume` (positive: increase generation, decrease demand
or provide upwards margin; negative: the opposite) and rounding (volume to one decimal place, price and
cost to two).

**Units.** Only from the vendor dictionary above: `Volume` **MWh**, `Price` **£/MWh**, `Cost` **£**.
Nothing is converted and no unit is inferred from a column name. The dictionary calls `Volume` an
"average" and puts the duration in the cost formula, which reads like a power (MW) and does not match its
MWh unit label. gridflow keeps the stated MWh and holds the output (see Holds). `SP` is a settlement-period
ordinal, not a physical quantity; the vendor says a normal day has 48 half-hour periods, long days 50 and
short days 46. Silver accepts `sp` from 1 to 50.

**Sentinels and lexical rules.** The body is read with strict UTF-8, no trimming and no null-token map.
Across the captured body there are no literal `N/A` or `NA` tokens, no padded cells, no thousands
separators, no currency or percentage symbols and no non-finite number tokens. A blank numeric cell
becomes null, never zero. Signed values are values: `-1` is not a missing-value marker (the vendor defines
none), and zeros are kept as zeros. `Last_Updated` and the other string columns are kept byte-equal to the body.

**Clocks.** Two clocks, stated separately:

- **Vintage.** The record's vintage is `capture_fallback`: `available_at` is the gridflow capture time
  (the bronze sidecar's `written_at`, read as UTC), labelled so. The family is a datastore dump
  (`url_type` datastore), not an upload, so there is no per-file CKAN `last_modified` to use as vintage
  (`ckan_last_modified` applies to upload resources; ADR-035). The resource's CKAN `last_modified` is
  2026-10-06T12:30:13 in the 2026-10-06 catalogue snapshot (`catalog_snapshot_20261006T195819Z`) and
  2026-10-08T11:30:04 in the bronze capture sidecar (`request_params.ckan_last_modified`, ten minutes before
  the 11:40:27 fetch; the profile record `docs/neso_data_portal/profile/families/upcoming_trades.json` carries the
  same value). `TODO: verify` what that stamp measures. `published_at` is null: the `Last_Updated` column is an update
  column, never an issue time (`issue: none`).
- **Event time.** `sp_pair(date, sp)`: `timestamp_utc` and `event_time` are the start of the settlement
  period, computed from the settlement `Date` as Europe/London midnight plus `(sp - 1)` half-hours, then
  converted to UTC. This is the established UK settlement conversion, so it handles the 46 and 50 period
  clock-change days; it is not a composed UTC-date plus hour-label recipe. The date format is
  `%Y-%m-%d`.

The `Last_Updated` clock is undocumented: the dictionary gives a type (datetime) but no zone, so the
column is kept as a raw string and no instant is derived from it (`TODO: UPCOMING-UPDATE-CLOCK`, see Holds).

**Whole-capture semantics.** `latest` is `whole_capture`: each capture is a replacement snapshot of the
table, not an increment. The vendor text supports this: the table is for trades that have not started
delivery and its details are provisional and correctable. A trade should therefore disappear from the
table after delivery, which is supported by NESO trading material but **not measured** between captures
here. `empty_allowed` is `yes`: a genuine, marked empty capture is valid and replaces the previous
populated snapshot under whole-capture selection. See Holds for the two open items.

**Forward-target property.** In the one capture, all 28 rows have a settlement-period start **after** the
capture time, so the table behaves as a forward-looking snapshot there and passes the forward-target
check (RULINGS 529) without treating the update column as issuance. That is a measurement of one capture
and must not be generalised.

**Held.** The silver output exists on disk and is held. The questions are in Holds. Because the held
question concerns what `Volume` measures, do not read `volume` as MWh or MW, and do not recompute or
reinterpret `cost` from `volume`, `price` or a period length.

## Bronze capture

One capture exists (2026-10-08), so there is no capture-pair history. The measured bronze body:

| Item | Value |
|---|---|
| Bronze file | `C:/gridflow-data/bronze/neso_data_portal/upcoming_trades/2026/10/08/raw_20261008T114027Z_0b7e84ec-eded-4458-b111-d29ba4508e85_7441677b.csv` |
| Format | CSV, strict UTF-8, header as the vendor column list above |
| Size and rows | 2,276 bytes · 28 data rows |
| SHA-256 | `7441677b3c34242b7df2aa6d49a21cd8c73a29a401c3f9434f2903924ce778a0` (matches the sidecar) |
| Sidecar `fetched_at` | `2026-10-08T11:40:27.998064+00:00` |
| Sidecar `written_at` | `2026-10-08T11:40:28.001597+00:00` |
| Empty-capture marker | false (the capture is populated; no empty capture was ever observed) |

Mind the second boundary: the filename stamp reads `114027Z` but `written_at`, which is the vintage, is
`11:40:28.001597`, one second later. Use the sidecar value, never the filename.

Silver lives at `C:/gridflow-data/silver/neso_data_portal/upcoming_trades/year=2026/month=10/`
(partitioned by capture month), one Parquet file for this capture with **28 rows**. System columns:
`timestamp_utc`, `published_at`, `available_at`, `event_time`, `bronze_capture_id`, `capture_written_at`,
`source_run_id`, `dataset_version`.

Activation (RULINGS 715, 2026-10-12): the transform for `--start/--end 2026-10-08`, with no prior silver, gave
28 rows for this family, equal to the plan (9 TRD families, 324,996 rows in total). The reconcile run over all families (RULINGS 716, cutoff 2026-10-12) exited 0 with 150 families,
0 gaps and 0 stale; no adjudication concerns this package.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Status: Live

The vendor says the table is **refreshed every ten minutes** (CKAN package notes and resource
description), whereas the registry refreshes it **daily**. A daily ingest therefore sees one snapshot a
day: trades that are agreed and delivered between two captures are never observed. Only one bronze
capture exists today, so neither the refresh behaviour nor the rate of change can be measured. `TODO:
verify` whether a higher ingest frequency is wanted once the hold is settled. No rate limit or
pagination for the datastore dump was found in the documentation read: `TODO: verify`.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence). gridflow
outputs derived from this package carry the attribution line above. The vendor's disclaimers apply to the
data: the details are provisional and subject to correction. The CKAN notes link NESO's terms and
conditions at `https://trades.nationalgrid.co.uk/terms-and-conditions`.

## Holds

- `upcoming_trades`: held: TODO: UPCOMING-VOLUME-FORMULA — `Volume` is labelled MWh but described as average with duration in the cost formula; MW or MWh? Also `Last_Updated` clock undocumented. (unit v0.22-K-TRD)

The silver output exists on disk and is **held**. It may not be published, nor used for point-in-time
models, until the unit that settles the semantics questions (E-SEM) answers the questions below. The
registry records the hold against the unit that created it (`v0.22-K-TRD`); the eligibility report agrees
with the registry (the package is `eligible` as a package; the hold is on the family output).

**The hold questions, in plain terms.**

1. **What does `Volume` measure (`TODO: UPCOMING-VOLUME-FORMULA`)?** The dictionary labels it MWh and calls
   it "Average Volume", while the cost comment is `Cost = Price * Volume * Duration`. If `Volume` were energy
   in MWh, multiplying by a duration would be wrong; if it is an average power in MW, the MWh label is wrong.
   Which is the published quantity, and what is the duration? The unit as published (MWh), the price unit
   (£/MWh) and the cost unit (£) are preserved; no conversion, no derived `volume` in another unit and no
   recomputed `cost` is published. Note that the historic GTMA upload tables label volume as total MWh and the
   FY datastore table labels it as an average in MW, so the unit is not safe to carry across the GTMA
   packages. Unit: E-SEM.
2. **What clock is `Last_Updated` on (`TODO: UPCOMING-UPDATE-CLOCK`)?** The dictionary says "date and time
   that the information has been last updated" with no time zone. The column is kept as a raw string and
   `issue` is `none`; no `available_at` is taken from it. Unit: E-SEM.

Open items that do not hold the output but limit what can be claimed:

- `TODO: EMPTY-PUBLICATION`: no explicit NESO statement that the table is published as a header-only file
  when no trade is upcoming was found. `empty_allowed` stays `yes`; a genuine marked empty capture or
  vendor confirmation would settle it.
- `TODO: MEASURED-IN-PLACE-AMENDMENTS`: NESO says details may be corrected, but with one capture it is not
  possible to measure which rows change between captures, or whether an amended trade keeps its `ID`.
- `TODO: verify` that a trade disappears from the table after its delivery period starts (supported by NESO
  trading material, not measured).

## Gotchas

- **Snapshot, not history.** The table is a rolling list of upcoming trades. Whole-capture selection means
  the newest capture replaces the previous one; to study how trades appear, change and vanish you need many
  captures, and the daily refresh cannot give them (see Cadence).
- **`id` is not a key on its own.** One trade spans several periods. Join and dedup on `(id, date, sp)`,
  never on `(date, sp)` alone, and never on `id` alone.
- **No `run_type`.** The `SO_Flag` and `Reason` columns are trade attributes, not settlement runs.
  Point-in-time queries use `available_at <= :as_of`, where `available_at` is capture time.
- **Do not confuse with the historic GTMA tables.** Different tables: the historic upload tables label
  volume as total MWh and carry start/end timestamps; the historic FY datastore table labels volume as
  average MW and cost as £/h. No trade-id overlap between this table and the historic ones was measured
  (the batch research measured id overlaps only among the GTMA families). Units must not be carried across
  packages.
- **Do not repair or recompute.** Preserve `Last_Updated` raw; do not derive `cost`; do not relabel
  `volume`.

## Modelling notes

Not designed: the output is held, so no model may consume it yet. `TODO` once UPCOMING-VOLUME-FORMULA is
answered. Likely uses, subject to the hold and to a multi-capture history: a forward look at committed
balancing trades by settlement period (with @../../../20-domain/concepts/settlement-period.md for the
event-time conversion), and a comparison against the delivered history in
@./historic-gtma-grid-trade-master-agreement-trades-data.md once units are reconciled.

## Links

- Package page: [Upcoming trades](https://www.neso.energy/data-portal/upcoming-trades-0)
- Datastore dump: [Upcoming Trades](https://api.neso.energy/datastore/dump/0b7e84ec-eded-4458-b111-d29ba4508e85)
- NESO trading publication cited by the batch research: [document 266956](https://www.neso.energy/document/266956/download)
- Licence: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence)
- Registry record: `src/gridflow/connectors/neso_data_portal/registry/upcoming-trades.json` (gridflow checkout)
- Eligibility report: `docs/neso_data_portal/eligibility.md` (gridflow checkout)
- Batch evidence: @.planning/phases/v0.22-K-TRD/K-TRD-FACTS.md and @.planning/v0.22-RESULTS.md (gridflow checkout)
- Sibling package: @./historic-gtma-grid-trade-master-agreement-trades-data.md
- Domain: @../../../20-domain/concepts/settlement-period.md · @../../../20-domain/markets/gb-balancing-mechanism.md
