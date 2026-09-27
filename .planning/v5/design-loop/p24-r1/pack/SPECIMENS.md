# Dataset-page fact pack: four specimens

Measured 2026-09-27 (about 00:15-01:20 UTC). Every number here was read from local silver (`C:/gridflow-data/silver`), gridflow code, or the canonical vault. Nothing was recalled from memory. Bulk points, full sample rows and per-code tables are in `specimens.json`. Paths are shortened: `gridflow/` = `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow\src\gridflow\`, `gm/` = `...\gridflow_models\src\gridflow_models\`, `vault/` = `quant-vault\30-vendors\`.

**Silver is live.** A scheduled transform rewrote FUELHH silver at 2026-09-27T00:09Z, during this session (it added settlement dates 2026-09-22..26 and rewrote 09-21). FUELHH figures below were re-measured after that write (1,849 files). The other three specimens did not change during the session.

## Palette mapping for FUELHH codes

From DESIGN.md:43-45 and `site/hifi/assets/tokens.css:33-40`. Note that tokens.css is untracked (`??`) in the front-end working tree.

| Palette slot | Token (hex) | FUELHH codes in silver |
|---|---|---|
| wind = horizon | `--fuel-wind` #3E8C97 | WIND |
| solar = chartreuse | `--fuel-solar` #AFC64E | **none.** FUELHH has no solar code (0 rows; vault/elexon/datasets/fuelhh.md:22) |
| gas = clay | `--fuel-gas` #C77E3C | CCGT, OCGT (tokens.css:36 "CCGT / OCGT: clay") |
| nuclear = petrol | `--fuel-nuclear` #155A6E | NUCLEAR |
| imports = olive | `--fuel-imports` #66793B | INTELEC, INTEW, INTFR, INTGRNL, INTIFA2, INTIRL, INTNED, INTNEM, INTNSL, INTVKL (signed MW, positive = import to GB) |
| biomass = bronze | `--fuel-biomass` #A5713C | BIOMASS |
| other = khaki | `--fuel-other` #A39A6A | OTHER (composition undocumented, vault fuelhh.md:166-168) |

**Codes the palette does not cover (flagged):**
- **NPSHYD**: non-pumped hydro, 243-923 MW in the chart window.
- **PS**: pumped storage. It is signed (-1456..+1508 MW in the window, negative in 186 of 336 half-hours). Neither code nor vault defines what the sign means.
- **COAL**: nearly always 0 MW (4 non-zero half-hours in 2026, the last at 2026-09-23T09:00Z, peaking at 133 MW in the window).
- **OIL**: 0 MW except for 17 half-hours since 2021-09.
- **INTELE**: a stray code with 9 rows on 2021-09-10, all 0 MW. It is not a live series.

Whether these codes fold into khaki "other" is a design decision that has not been made. The palette slot "other" and the vendor code `OTHER` share a name.

## Workbench, shared facts (all four specimens)

- Bootstrap: `from gridflow_models import setup_notebook` then `data, models, common = setup_notebook()` (gm/research/notebook_setup.py:278).
- Verb: `SourceClient.query(self, dataset: str, start: date | str, end: date | str) -> pd.DataFrame` (gm/research/handles/source.py:401-451). It returns **pandas**. Source handles are named after gridflow's config sources (`data.elexon`, `data.entsog`; data.py:112-114).
- The dataset name resolves to a relation and a date column through gridflow's schema manifest (gridflow/silver/schema_manifest.py:454, read via gm/research/handles/_schema_manifest.py:31-80). A DATE column uses an inclusive `BETWEEN`. A TIMESTAMPTZ column uses `>= start 00:00Z AND < end+1 00:00Z` (_get_method_registry.py:62-96).
- `query()` and `tail()` drop `event_time, available_at, vintage_policy, source_run_id, dataset_version` (source.py:116-144, 441-446).
- **Stale doc:** gridflow_models `notebooks/README.md:285` shows `data.elexon.system_prices(start, end)`, and :313-317 describes a `DatasetProxy`. Neither exists in src; source.py:5-12 says per-dataset attributes were removed in F24. The notebooks themselves use `query("<dataset>", start, end)`.
- All four relations were confirmed read-only in `C:/gridflow-data/gridflow.duckdb`.

---

## 1. elexon/fuelhh

**Identity.** Elexon BMRS (Insights API). Code `FUELHH` (gridflow key `fuelhh`). Vendor name: "Half-hourly Generation Outturn by Fuel Type" (gridflow/connectors/elexon/endpoints.py:111-115). *Half-hourly GB generation outturn in MW, one value per settlement period per Elexon fuel-type code.*

**Silver schema.** `ElexonFuelHH`, gridflow/schemas/elexon.py:113-130. Transformer `silver/elexon/fuelhh.py`, DATASET_VERSION 2.0.0.

| Column | Dtype | Meaning |
|---|---|---|
| settlement_date | Date | GB settlement date; since v2.0.0 derived from the vendor startTime (fuelhh.py:135-165) |
| settlement_period | Int32 | Half-hour index 1..50 (46/50 on clock-change days) |
| timestamp_utc | Datetime(us,UTC) | Start of the half-hour, UTC (vendor startTime) |
| fuel_type | String | Elexon fuel-type code, uppercase as sent |
| generation_mw | Float64 | MW for the period. INT* are signed, positive = import to GB (vault fuelhh.md:150-156). PS is signed, meaning unknown |
| published_at | Datetime(us,UTC) | Vendor publishTime/publishDateTime (fuelhh.py:81-85) |
| data_provider | String | "elexon" |
| ingested_at | Datetime(us,UTC) | Wall clock of the silver transform run (fuelhh.py:191-196) |
| event_time, available_at, source_run_id, dataset_version | lineage | Added by BaseSilverTransformer, not in the Pydantic class. available_at = coalesce(published_at, ingest time) (silver/base.py:2095) |

**Silver facts.**
- Rows: 1,682,517.
- Time span: 2021-08-31T23:30Z to 2026-09-26T22:30Z (settlement dates 2021-09-01..2026-09-26), 88,672 distinct half-hours.
- Grain: one row per (settlement_date, settlement_period, fuel_type), with 0 duplicate keys. Cadence is 30 min.
- Codes per half-hour: 17 (634 half-hours), 18 (38,324), 19 (12,373), 20 (37,341). The recent standard is 20.
- Codes present (21): BIOMASS, CCGT, COAL, INTELE (stray), INTELEC, INTEW, INTFR, INTGRNL, INTIFA2, INTIRL, INTNED, INTNEM, INTNSL, INTVKL, NPSHYD, NUCLEAR, OCGT, OIL, OTHER, PS, WIND.
- **SOLAR does not appear**: no solar code at all.
- Code start dates: INTELEC from 2021-09-14, INTVKL from 2023-07-12, INTGRNL from 2024-03-19.
- Missing dates: 2026-09-07, 08 and 09. 2026-09-06 has SP1-2 only. There are short days on 2021-11-23 (44 SPs) and 2022-01-18 (45). In total there are 29 gaps over 30 minutes: 26 of 1 h, 2 of 2 h, and one of 96 h ending 2026-09-09T23:30Z.
- Units: MW. Volume: 29,760 rows in 2026-08.

**Sample rows** (silver, settlement_date 2026-09-26, SP25; 8 of 20 codes). Every row has `published_at` = `available_at` = 2026-09-26T11:30:00Z, `event_time` = timestamp_utc, `data_provider` elexon, `ingested_at` 2026-09-27T00:09Z run, and `dataset_version` 2.0.0. Full rows are in the JSON.

| settlement_date | SP | timestamp_utc | fuel_type | generation_mw |
|---|---|---|---|---|
| 2026-09-26 | 25 | 2026-09-26T11:00:00Z | BIOMASS | 1272.0 |
| 2026-09-26 | 25 | 2026-09-26T11:00:00Z | CCGT | 2139.0 |
| 2026-09-26 | 25 | 2026-09-26T11:00:00Z | INTFR | 1000.0 |
| 2026-09-26 | 25 | 2026-09-26T11:00:00Z | NPSHYD | 264.0 |
| 2026-09-26 | 25 | 2026-09-26T11:00:00Z | NUCLEAR | 4020.0 |
| 2026-09-26 | 25 | 2026-09-26T11:00:00Z | OTHER | 575.0 |
| 2026-09-26 | 25 | 2026-09-26T11:00:00Z | PS | -1454.0 |
| 2026-09-26 | 25 | 2026-09-26T11:00:00Z | WIND | 6094.0 |

**Chart series.**
- Content: per-fuel generation, stacked by fuel. Dataset `elexon/fuelhh` silver, unit **MW**.
- Window: settlement dates 2026-09-20..2026-09-26, which is 336 half-hours from 2026-09-19T23:00Z to 2026-09-26T22:30Z. The window is clear of the September hole.
- **Aggregation:** for each fuel code, the mean of the 2 half-hour `generation_mw` values in each UTC hour (168 points). For palette groups, `generation_mw` is summed across the group's codes per half-hour first, then the same hourly mean is taken. It is never a mean across fuels.
- Data: `specimens.json` → `chart.per_fuel_mw` (20 series) and `chart.palette_groups_mw` (wind, gas, nuclear, imports, biomass, other, plus `uncovered:COAL|NPSHYD|OIL|PS`).
- Query: `read_parquet(fuelhh/**) → filter settlement_date in [2026-09-20, 2026-09-26] → truncate timestamp_utc to 1h → group (hour, fuel_type) → mean(generation_mw)`.
- Hourly ranges: wind 1,325-16,011; gas 2,124-15,860; nuclear 3,330-4,027; biomass 584-3,048; other 94-3,620; **imports -6,312..+6,614**; **PS -1,455..+1,508**.
- **Shape warning:** a stacked area with signed series needs an explicit rule, either positives above zero and negatives below, or net imports drawn as a separate line. Never clip or abs().

**How to get it.**
- Workbench: `data.elexon.query("fuelhh", "2026-09-20", "2026-09-26")` (relation `silver_elexon_fuelhh`, date column `settlement_date`; 6,720 rows for that range). `query("fuel_generation", ...)` is a serving alias of the same relation.
- Vendor: `GET https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELHH?publishDateTimeFrom=<UTC Z>&publishDateTimeTo=<UTC Z>&page=<n>` (endpoints.py:34-35, 111-115, 300-313; config/sources.yaml:3, 27-30).
- CLI: `gridflow ingest elexon fuelhh --start 2026-09-20 --end 2026-09-26` (bronze), or `gridflow pipeline elexon fuelhh --start ... --end ...` (bronze to silver) (cli.py:186, :485).

**Caveats.**
1. There is no solar code, so solar outturn is not in this dataset. Evidence: 21 distinct codes, none solar; vault fuelhh.md:22.
2. Eleven codes are signed: the ten INT* codes (positive = import) and PS. Negatives are routine; for example INTIRL is negative in 70.3% of all half-hours and PS in 54.7% (silver). Vault fuelhh.md:150-162.
3. The code set changes over time (INTELEC 2021-09-14, INTVKL 2023-07-12, INTGRNL 2024-03-19), so a half-hour holds 17 to 20 rows.

**Compact facts.**
- Publication lag: evidenced. `published_at` equals the period end (start + 30 min) on 99.82% of rows, with a maximum of 271 min.
- History depth: in local silver, 2021-09-01..2026-09-26 with the gaps above. Vendor depth is not established.

**Related.** elexon/fuelinst (same connector, instantaneous outturn, endpoints.py:116-120); elexon/bmunits_reference (shared fuel vocabulary, vault bmunits_reference.md:207-212); elexon/indo (sign check against demand, vault fuelhh.md:150-156); neso_data_portal/historic_generation_mix (where solar lives, vault fuelhh.md:22).

**Discrepancies.**
- Site (`authored-pages/elexon/fuelhh.html`) claims solar in its overview, lists a SOLAR code, and shows a SOLAR sample row. Silver has none.
- Site says "All 16 codes" and lists `INTEM`, which does not exist. It omits INTELEC, INTGRNL, INTIFA2, INTNEM, INTNSL and INTVKL.
- Site says interconnectors are "negative (import)". The vault, backed by the demand identity, says positive = import.
- Site claims "~5 min publication lag" and "1.4M / mo". Silver shows publication at the period end (30 min after start) and 29,760 rows in 2026-08.
- The site sample for 2026-05-06 SP8 is wrong. It shows 03:30Z with CCGT 7840, NUCLEAR 4310, WIND 9220, NPSHYD 410, INTFR 1640 and INTNED 720. Silver has 02:30Z with CCGT 7729, NUCLEAR 4137, WIND 5691, NPSHYD 198, INTFR 978 and INTNED 334. Only BIOMASS (2821) matches.
- Vault fuelhh.md:116 says timestamp_utc is derived from (date, period). Code v2.0.0 uses vendor startTime, as does the vault's own :189-205. The vault silver sample (:130) shows 03:30Z against its own bronze startTime of 02:30Z (:81).
- Vault :121 says ingested_at is the "time ingested into bronze". Code stamps it at silver transform time.
- `site/hifi/data/chart-series.json` elexon/fuelhh is "mean of generation_mw per timestamp_utc", a mean across fuels. DESIGN.md:88-90 carries this as a standing caveat.
- Site SQL uses the deprecated alias `silver_fuelhh`.

---

## 2. elexon/system_prices

**Identity.** Elexon BMRS. The response dataset is `DISEBSP` (vault system_prices.md:63-66); the gridflow key is `system_prices`. Vendor description: "System Sell Price and System Buy Price per settlement period" (endpoints.py:58-62). *GB imbalance (cash-out) prices, SSP and SBP in GBP/MWh, with net imbalance volume, per settlement period.*

**Silver schema.** `ElexonSystemPrice`, gridflow/schemas/elexon.py:25-66. Transformer `silver/elexon/system_prices.py`, DATASET_VERSION 2.0.0, **APPEND_ONLY** (:65-66).

| Column | Dtype | Meaning |
|---|---|---|
| settlement_date / settlement_period | Date / Int32 | GB settlement date; half-hour 1..50 |
| timestamp_utc | Datetime(us,UTC) | Period start, from settlement_period_to_utc (:210-220) |
| system_sell_price | Float64 | SSP, GBP/MWh; schema bound -500..10000 (elexon.py:45) |
| system_buy_price | Float64 | SBP, GBP/MWh |
| net_imbalance_volume | Float64 | NIV, MWh. Sign convention unknown in code/vault (data evidence below) |
| run_type | String | BSC run code; **null on every row** (this endpoint has no such field, elexon.py:28-33) |
| price_derivation_code | String | Vendor priceDerivationCode: N 49,764, P 47,019, K 10. The vault reads N = normal and P = provisional; K is unknown |
| published_at | Datetime(us,UTC) | Vendor createdDateTime (:129, :168-182) |
| data_provider / ingested_at | String / Datetime | "elexon" / silver transform wall clock |
| event_time, available_at, source_run_id, dataset_version, vintage_policy | lineage | vintage_policy = "vendor" on all rows |

**Silver facts.**
- Rows: 96,793, covering **88,694 distinct settlement periods**. The extra rows are vintages: 6,357 periods have more than one row, and only 6 of those differ in price.
- Time span: 2021-08-31T23:00Z to 2026-09-22T22:30Z (settlement dates 2021-09-01..2026-09-22). No dates are missing; 2023-01-22 has 45 periods.
- Grain: one row per period per vendor createdDateTime. Cadence is 30 min.
- **SSP equals SBP on 96,793 of 96,793 rows.**
- Units: GBP/MWh and MWh.
- Negative SSP (latest vintage): 4,052 periods. Minimum is -185.33 (2023), maximum 4,037.80 (2021). Per year: 2022 had 314, 2023 had 850, 2024 had 1,073, 2025 had 1,121, and 2026 to 09-22 has 618.
- NIV evidence (latest vintage): median SSP is 128.80 when NIV > 0 (43,010 periods) and 65.00 when NIV < 0 (45,674); corr(NIV, SSP) = 0.41.

**Sample rows** (silver, settlement_date 2026-09-20, SP22-29; one vintage each). `run_type` is null, `vintage_policy` is vendor, and available_at = published_at.

| SP | timestamp_utc | SSP | SBP | NIV (MWh) | code | published_at |
|---|---|---|---|---|---|---|
| 22 | 2026-09-20T09:30Z | -0.87 | -0.87 | -722.2791975565136 | N | 2026-09-21T10:14:32Z |
| 23 | 2026-09-20T10:00Z | -2.86 | -2.86 | -730.1364863554893 | N | 2026-09-21T10:44:31Z |
| 24 | 2026-09-20T10:30Z | -2.81 | -2.81 | -666.4044157035205 | N | 2026-09-21T11:14:33Z |
| 25 | 2026-09-20T11:00Z | -16.21 | -16.21 | -1046.9714302777777 | N | 2026-09-21T11:44:29Z |
| 26 | 2026-09-20T11:30Z | -4.52 | -4.52 | -1005.3920633333333 | N | 2026-09-21T12:14:29Z |
| 27 | 2026-09-20T12:00Z | -19.623944805628415 | -19.623944805628415 | -782.3633315277777 | N | 2026-09-21T12:46:44Z |
| 28 | 2026-09-20T12:30Z | -25.509591094964623 | -25.509591094964623 | -1104.0918609722223 | N | 2026-09-21T13:14:38Z |
| 29 | 2026-09-20T13:00Z | -49.9 | -49.9 | -1386.7454283333334 | N | 2026-09-21T13:44:56Z |

**Chart series.**
- Content: system sell price. Dataset `elexon/system_prices` silver (latest vintage per period), unit **GBP/MWh**.
- Window: settlement dates 2026-09-19..2026-09-22, which is 192 half-hours from 2026-09-18T23:00Z to 2026-09-22T22:30Z.
- **Aggregation: none.** These are native half-hourly values. For each period the latest vintage by available_at is kept, as the workbench `_latest` view does.
- **34 of 192 points are negative.** The minimum is -50.00 at 2026-09-20T13:30Z and the maximum 594.00 at 2026-09-22T20:00Z.
- SBP is identical in the window, so draw one line.
- Data: `specimens.json` → `chart.t_utc` and `chart.ssp_gbp_per_mwh`, with the negative periods listed in `chart.negatives.periods`.
- Query: `read_parquet(system_prices/**) → sort available_at → group (settlement_date, settlement_period).last() → filter dates → sort timestamp_utc`.

**How to get it.**
- Workbench: `data.elexon.query("system_prices", "2026-09-19", "2026-09-22")`. It reads `silver_elexon_system_prices_latest` (the manifest relation), so vintages are already collapsed; raw parquet does not do this. `data.imbalance_context(start, end)` adds NESO carbon intensity (data.py:67-78).
- Vendor: `GET https://data.elexon.co.uk/bmrs/api/v1/balancing/settlement/system-prices/{YYYY-MM-DD}?page=<n>` (endpoints.py:58-62; client.py:255; sources.yaml:10-13).
- CLI: `gridflow ingest elexon system_prices --start 2026-09-19 --end 2026-09-22` or `gridflow pipeline elexon system_prices ...`.

**Caveats.**
1. Silver is append-only (96,793 rows for 88,694 periods). Plot from `_latest` or dedupe on available_at (system_prices.py:65-71).
2. SSP equals SBP on every row since 2021-09, so one line carries both.
3. Negative prices are routine: 4,052 periods since 2021-09, and 34 of 192 in the chart window.

**Compact facts.**
- Publication lag: evidenced. `published_at` minus period start has a median of **52 min in 2021-2023** and **1,484 min (about 24.7 h) in 2024-2026**. The cause is not established.
- History depth: in local silver, 2021-09-01..2026-09-22. Vendor depth is not established.

**Related.** neso/carbon_intensity (gold_uk_imbalance_context join, vault system_prices.md:222-227); elexon/mid (workbench gb_day_ahead_benchmark, data.py:79-90); gold system_marginal_price (vault :229-234); elexon/netbsad and elexon/disbsad (same connector, relation taken from the site page and not checked in code).

**Discrepancies.**
- Vault system_prices.md:128 gives a dedup key and :243 says "keeps the highest-rank run only". Code is APPEND_ONLY with no dedup, and the vault's own :207-216 contradicts it. The site repeats the claim.
- Vault :129 and the site name run_type as the point-in-time field. It is null on every row.
- Vault silver sample (:153) puts SP1 at 2026-05-06T00:00Z. On a BST date SP1 starts at 23:00Z on the previous day (vault bronze :72).
- Site says "negative NIV means the system was short". The data evidence above points the other way.
- Site says "single-price since Nov 2018". That date is not evidenced here.
- Site lists price_derivation_code values "N, P" only; K also occurs (10 rows).
- Site claims a publication lag of "hours → weeks" and an II…RF timetable. Neither is evidenced in code; the measured lag is 52 min or 24.7 h as above.
- Site chart is "illustrative, seeded", and its SQL uses the deprecated alias `silver_system_prices`, which is the raw append-only view.

---

## 3. entsog/physical_flows

**Identity.** ENTSOG Transparency Platform, `/operationalData` with indicator `Physical Flow` (gridflow key `physical_flows`; endpoints.py:20, :95-96). *Daily physical gas flow per operator, point and direction across European transmission systems, in GWh/d.*

**Silver schema.** `EntsogPhysicalFlow`, gridflow/schemas/entsog.py:12-30 (the only class in that module). Transformer `silver/entsog/physical_flows.py`.

| Column | Dtype | Meaning |
|---|---|---|
| timestamp_utc | Datetime(us,UTC) | Gas-day start (vendor periodFrom) in UTC (:158) |
| point_key / point_label | String | ENTSOG point id / name (e.g. ITP-00005, "Bacton (IUK)") |
| operator_key / operator_label | String | Reporting operator id / name (e.g. UK-TSO-0001, "National Gas TSO") |
| direction_key | String | "entry" or "exit" (entsog.py:20). Treated as relative to the reporting operator's system; this is inferred from paired values, not documented |
| flow_gwh_per_day | Float64 | Flow normalised to GWh/d from vendor value and unit (:38-69, :197-224). **Nullable** |
| unit | String | Always "GWh/d" after normalisation (:246-250) |
| data_provider | String | "entsog" |
| ingested_at | Datetime(us,UTC) | Silver transform wall clock (:241-245). **Not declared in EntsogPhysicalFlow** |
| event_time, available_at, source_run_id, dataset_version | lineage | available_at is the ingest time here |

**Silver facts.**
- Rows: 13,764, from 14 files.
- Gas days: **2026-08-01..05 and 2026-09-13..21 only.** Timestamps run from 2026-07-31T22:00Z to 2026-09-21T21:00Z.
- Grain: one row per (timestamp_utc, point_key, operator_key, direction_key), with 0 duplicate keys and about 983 rows per gas day. There are 986 series across 620 points and 48 operators.
- Cadence is daily. The timestamp is each operator's gas-day start, so it varies. GB operators are mostly at 04:00Z (2,268 rows); others fall at 02:00-05:00Z or 21:00-23:00Z.
- direction_key: entry 5,652, exit 8,112. unit: GWh/d on all 13,764 rows. dataset_version is 1.0.0.
- Nulls: 2,499 rows have a null flow, and **176 series are null on every day**.
- There are no negative values (range 0.0 to 1,096.595 GWh/d).

**Sample rows** (silver, gas day 2026-09-21, timestamp_utc 2026-09-21T04:00Z). unit is GWh/d, ingested_at 2026-09-26T17:46:49.526383Z, dataset_version 1.0.0.

| point_key | point_label | operator_key | operator_label | direction | flow_gwh_per_day |
|---|---|---|---|---|---|
| ITP-00005 | Bacton (IUK) | UK-TSO-0001 | National Gas TSO | exit | 175.165952 |
| ITP-00005 | Bacton (IUK) | UK-TSO-0003 | Interconnector | entry | 175.165952 |
| ITP-00061 | Zeebrugge IZT | UK-TSO-0003 | Interconnector | exit | 176.236744 |
| ITP-00207 | Bacton (BBL) | UK-TSO-0001 | National Gas TSO | exit | 64.358734 |
| ITP-00207 | Bacton (BBL) | UK-TSO-0004 | BBL company | entry | 64.358734 |
| ITP-00022 | St. Fergus | UK-TSO-0001 | National Gas TSO | entry | 559.186147 |
| LNG-00007 | Teesside | UK-TSO-0001 | National Gas TSO | entry | 245.890309 |
| LNG-00053 | Avonmouth LNG | UK-TSO-0001 | National Gas TSO | entry | null |

**Chart series.**
- Content: daily flow at two GB points. Dataset `entsog/physical_flows` silver, unit **GWh/d**.
- Window: all local silver. There is a **gap from 2026-08-06 to 2026-09-12 with no rows**; draw a break and do not interpolate.
- **Aggregation: none.** Each series has one native value per gas day. Nothing is averaged across points.
- All timestamps are 04:00Z.

| Gas day | National Gas TSO, Bacton (IUK), exit | National Gas TSO, St. Fergus, entry |
|---|---|---|
| 2026-08-01 | 406.880 | 433.651 |
| 2026-08-02 | 381.867 | 409.020 |
| 2026-08-03 | 382.044 | 411.354 |
| 2026-08-04 | 381.880 | 405.794 |
| 2026-08-05 | 381.876 | 350.288 |
| 2026-09-13 | 0.0 | 473.217 |
| 2026-09-14 | 0.0 | 472.952 |
| 2026-09-15 | 0.0 | 501.833 |
| 2026-09-16 | 0.0 | 515.166 |
| 2026-09-17 | 0.0 | 491.312 |
| 2026-09-18 | 0.0 | 551.905 |
| 2026-09-19 | 0.0 | 594.565 |
| 2026-09-20 | 0.0 | 584.382 |
| 2026-09-21 | 175.166 | 559.186 |

Query: `read_parquet(physical_flows/**) → filter operator_key='UK-TSO-0001', point_key in (ITP-00005 exit, ITP-00022 entry) → sort timestamp_utc`. The zeros are as observed; no cause is established.

**How to get it.**
- Workbench: `data.entsog.query("physical_flows", "2026-09-13", "2026-09-21")` (relation `silver_entsog_physical_flows`, TIMESTAMPTZ predicate `>= 2026-09-13T00:00Z AND < 2026-09-22T00:00Z`). Operators whose gas day starts at 21:00-23:00Z on the previous UTC date fall outside the first day of the range.
- Vendor: `GET https://transparency.entsog.eu/api/v1/operationalData?limit=-1&timeZone=UCT&from=YYYY-MM-DD&to=YYYY-MM-DD&indicator=Physical%20Flow&periodType=day`, with no `pointDirection` (a full-system fetch). Sources: endpoints.py:12-20, :71-90, :118-124, :263-281; sources.yaml:461-472 (max_query_days 30).
- CLI: `gridflow ingest entsog physical_flows --start 2026-09-13 --end 2026-09-21` or `gridflow pipeline entsog physical_flows ...`.

**Caveats.**
1. Local history is only 14 gas days in two blocks.
2. Both sides of a point are reported, so summing every row double counts. For example, Bacton (IUK) National Gas TSO exit and Interconnector entry are both 175.165952 on 2026-09-21.
3. Flows can be null (2,499 rows, and every day for 176 series such as Avonmouth LNG). Do not zero-fill.

**Compact facts.**
- Publication lag: **not established.** available_at is the ingest time, and vendor lastUpdateDateTime is not carried into silver.
- History depth: in local silver, 14 gas days. Vendor depth is not established (the vault says "approx. 2010 onwards").

**Related.** entsog/aggregated_physical_flows (same indicator at zone level via `/aggregatedData`, endpoints.py:168-180); entsog/nominations (endpoints.py:97); entsog/allocations (:98); operator_point_directions (vault physical_flows.md:225, which suggests a join; no local silver).

**Discrepancies.**
- Vault :159 and the site say `unit` holds the raw vendor unit ("kWh/d"), and the site's sample rows show kWh/d. Silver is "GWh/d" on every row.
- Vault :146 names a point-in-time field `last_update_date_time`; that column is not in silver.
- Vault :158 and the site describe flow as not nullable, "default 0.0". The schema is `float | None = None`, and 2,499 rows are null.
- Site says "~9 points/day"; there are about 983 rows per gas day.
- Site tells readers to filter on flowStatus, which exists only in bronze.
- Site sample rows are "synthesised" apart from the first row.
- Site lists `ingested_at` under the Pydantic class, which does not declare it.
- `chart-series.json` entsog/physical_flows is "mean of flow_gwh_per_day per event_time", averaging about 980 unrelated series.
- Site SQL uses the deprecated alias `silver_physical_flows`.

---

## 4. elexon/bmunits_reference

**Identity.** Elexon BMRS `GET /reference/bmunits/all` (gridflow key `bmunits_reference`). Vendor description: "All BM Unit reference data" (endpoints.py:257-262). *Registry snapshot of Balancing Mechanism Unit registrations: id, name, fuel type, capacity, lead party, GSP group.*

**Silver schema.** `ElexonBMUnit`, gridflow/schemas/elexon.py:309-320. Transformer `silver/elexon/bmunits.py`, DATASET_VERSION 1.1.0.

| Column | Dtype | Meaning |
|---|---|---|
| bm_unit_id | String | Elexon BM Unit id (vendor elexonBmUnit); entity key |
| bm_unit_name | String | Vendor bmUnitName; often repeats the id |
| fuel_type | String | Vendor fuelType; **null on 2,515 of 3,014 rows** |
| registered_capacity_mw | Float64 | Vendor generationCapacity, MW; per registration, not additive (vault :175-193) |
| company_name | String | Vendor leadPartyName |
| gsp_group_id | String | Vendor gspGroupId (e.g. _A); null on 1,822 rows |
| national_grid_bm_unit | String | Vendor nationalGridBmUnit (e.g. ABERU-1); not the ENTSO-E EIC (vault :135) |
| data_provider / ingested_at | String / Datetime | "elexon" / silver transform wall clock |
| event_time, available_at, source_run_id, dataset_version | lineage | event_time = 2026-09-26T00:00Z (target-date fallback) |

**Silver facts.**
- Rows: 3,014, from a single file overwritten each run (bmunits.py:212-220). The snapshot was ingested 2026-09-26T19:08:06Z.
- **No time axis.** Grain is one row per bm_unit_id, with 0 duplicates. The configured schedule is weekly (sources.yaml:141-144).
- Units with a fuel type: 499. Counts by fuel_type: (null) 2,515; WIND 234; OTHER 92; CCGT 61; OCGT 22; NPSHYD 22; NUCLEAR 16; PS 16; BIOMASS 15; COAL 10; INTELEC 2; and 1 each for INTEW, INTFR, INTGRNL, INTIFA2, INTIRL, INTNED, INTNEM, INTNSL, INTVKL. There is no SOLAR code.
- Counts by id prefix (a string pattern whose meaning is not vendor-documented): I_ 1,315 (11 typed); 2__ 872 (19); T_ 496 (372); E_ 174 (81); V__ 140 (6); M_ 8 (8); C__ 4 (2); T__ 3; E__ 2.
- There are 379 distinct companies.

**Sample rows** (silver snapshot 2026-09-26). data_provider is elexon, dataset_version 1.1.0.

| bm_unit_id | bm_unit_name | fuel_type | registered_capacity_mw | company_name | gsp_group_id | national_grid_bm_unit |
|---|---|---|---|---|---|---|
| E_ABERDARE | Aberdare Power Station | null | 15.4 | UK Power Reserve Limited | _K | ABERU-1 |
| T_ABRBO-1 | ABRBO-1 | WIND | 99.0 | Aberdeen Offshore Wind Farm | null | ABRBO-1 |
| T_DRAXX-1 | T_DRAXX-1 | BIOMASS | 665.248 | Drax Power Ltd | null | DRAXX-1 |
| T_HEYM27 | Heysham 2 Generator 7 | NUCLEAR | 660.0 | EDF Energy Nuclear Generation | null | HEYM27 |
| T_PEHE-1 | Peterhead Block 1 | CCGT | 1200.0 | SSE Thermal Generation | null | PEHE-1 |
| I_IEG-FRAN1 | IEG-FRAN1 | INTFR | 2013.945 | Nat Grid Interconnectors Ltd | null | IEG-FRAN1 |
| 2__AANGE001 | 2__AANGE001 | null | 80.0 | Limejump Energy Limited | _A | AG-ALIM02 |
| V__AENEL001 | V__AENEL001 | null | 0.0 | Enel X UK Limited | _A | AG-ENX00A |

**Chart: the honest alternative.**
- There is no time axis, so there is no line chart.
- Proposal: **horizontal bars of unit counts by fuel_type**, 19 codes, using the counts listed above. Show the 2,515 null-fuel units as a separate labelled bar or a stated total, so the typed bars are not read as the whole registry.
- Unit: **count of BM units**. Aggregation is `group_by(fuel_type).len()`, with null kept.
- Palette-grouped counts: wind 234; gas (CCGT+OCGT) 83; nuclear 16; imports (10 INT codes) 11; biomass 15; other 92; uncovered NPSHYD 22, PS 16 and COAL 10.
- **Do not sum `registered_capacity_mw`.** Null-fuel rows alone sum to 727,551 MW. The sums are in the JSON for reference only.

**How to get it.**
- Workbench: `data.elexon.tail("bmunits_reference", n=3014)` (source.py:453-489) or `data.sql("SELECT * FROM silver_elexon_bmunits_reference")` (read-only, data.py:255-270).
- **Do not use `query()`.** The manifest date column for this dataset is `ingested_at`, so `query("bmunits_reference", "2026-01-01", "2026-01-31")` returns **0 rows** (checked read-only).
- Vendor: `GET https://data.elexon.co.uk/bmrs/api/v1/reference/bmunits/all`, with no params and no pagination (endpoints.py:257-262; client.py:63-68).
- CLI: `gridflow pipeline elexon bmunits_reference`. The NO_PARAMS fetch ignores dates (client.py:63-68).

**Caveats.**
1. 83% of units (2,515 of 3,014) have no fuel type, so a fuel breakdown covers only 499 units.
2. Capacity is per registration and is not additive. 1,315 ids start `I_`, which the vault describes as per-party interconnector registrations (vault :183-193, :214-220).
3. There is one snapshot, overwritten each run, and keyless vendor rows are dropped (ADR-032, bmunits.py:116-171). Counts therefore drift between runs: the vault recorded 2,969 on 2026-09-09, and there are 3,014 now.

**Compact facts.** Publication lag is not established. History depth: current snapshot only (2026-09-26); no history is kept.

**Related.** elexon/boal and elexon/pn (joined on bm_unit_id, bmunits.py:49-52); elexon/uou2t14d (vault :13); elexon/fuelhh (shared vocabulary and interconnector flow, vault :207-212).

**Discrepancies.**
- The site sample rows are wrong against silver:
  - `T_DRAXX-1` is named "T_DRAXX-1" with a null GSP group (the site gives "Drax Power Station 1" and `_D`).
  - `T_HEYM27` is "Heysham 2 Generator 7" with a null GSP group (the site gives `_N`).
  - `T_HOWAO-2` is "HORNSEA_1B", owned by Hornsea 1 Limited (the site says Hornsea 2 / Ørsted).
  - `T_PEHE-1` is "Peterhead Block 1", owned by SSE (the site says "Pembroke 1" / RWE).
  - `T_GRMO-1` is Grangemouth CHP, CCGT, 0 MW (the site says Greater Gabbard, WIND).
  - `I_IFA1` does not exist.
- The site's Python example uses `query(...)` and returns 0 rows.
- The site lists INT codes including `INTEM` (which does not exist) and omits OTHER, V__, M_ and C__.
- The site calls national_grid_bm_unit an "ENTSO-E EIC"; the vault says it is not.
- The site cites the schema at elexon.py lines 269-280; the class is at :309-320.
- The site's SQL sums capacity across null-fuel rows and uses the deprecated alias `silver_bmunits_reference`.
- Vault :119 gives a partitioned silver path, but the code writes one file. Vault :199 says the response is a bare array, but its own sample (:61) has a `{data: [...]}` envelope.
