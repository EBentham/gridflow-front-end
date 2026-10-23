# BSAD forward contracts page: author report

Page: `neso_data_portal/balancing-services-adjustment-data-forward-contracts` (single table `bsad_forward_contracts`). Written 2026-10-18 by the writer agent.

- Canonical note: `C:\gridflow-wt\vault-neso-as-b\30-vendors\neso-data-portal\datasets\balancing-services-adjustment-data-forward-contracts.md`. CRLF on every line, edited with the Edit tool. Vault diff: 138 added, 7 changed.
- Mirror: `C:\gridflow-wt\fe-neso-as-b\vault\neso_data_portal\balancing-services-adjustment-data-forward-contracts.md`. `cmp` is clean after the last edit.
- Artefacts (new, untracked, under `fe-neso-as-b\site\hifi\data\`):
  - `series\neso_data_portal\bsad_forward_contracts.json` (`spec_origin: vault`, 2 series x 3,105 points)
  - `samples\neso_data_portal\bsad_forward_contracts.json` (`generated_by: gridflow-sample`)
  - `notebooks\neso_data_portal\bsad_forward_contracts.json` and `bsad_forward_contracts-6.png` (from `scripts/run_notebooks.py`)
- Gates:
  - `gridflow-build --only neso_data_portal/bsad_forward_contracts` succeeds. The only message is the caveat-grammar warning (see Template problems).
  - `detect.mjs --json` returns `[]`.
  - Page text has no em or en dashes, middle dots or arrows, and none of `locally`, `held`, `since 20`, `live`, `now`, `yet`, `soon`, `planned`. The `rows` and `our` hits are template text and "hour".
- Screenshots:
  - Taken at 1440, 1024, 768 and 390 (390 through a 390 px iframe), served on port 9982. The server is stopped.
  - Nothing is clipped or overlapping.
  - The site has no dark theme, so light is the only rendering.
  - Shots are in `<scratchpad>\bsadfc-writer\shots\`.
- No staged chart spec or authored override existed.

## What one row is

- **Grain and key:**
  - One row per (`resource_id`, `settlement_date`, `settlement_period`) and capture.
  - Registry: `entity_key` as above, `latest: whole_capture`, `latest_partition: resource_id`, `vintage: capture_fallback`.
  - Settlement pairs never repeat across files, so the latest view holds one row per settlement period (Polars: 149,856 rows, 149,856 distinct pairs).
- **Not a contract list.** No column names a contract, trade, action or party. Each row is a settlement-period aggregate.
- **Six value columns** (vendor dictionary, field info `20261008T114228Z/bsad_forward_contracts.json`):
  - `bca` and `sca` in £; `bva`, `bsa`, `sva` and `ssa` in MWh.
  - Descriptions: Net Buy/Sell Price Cost Adjustment, Net Buy/Sell Price Volume Adjustment, Gross Volume Purchased/Sold (Trades).
- **Signs:**
  - Not stated by NESO (K-AS-4-FACTS line 344, `TODO: FORWARD-BSAD-SIGN-CONVENTION`).
  - Negatives in the latest view are rare: `bca` 1, `bsa` 1 (the literal `-1`), `bva` 1, `sca` 12, `ssa` 8 (`-0.001`), `sva` 1.
  - The page says only "NESO does not state its sign", and for `ssa` "NESO does not explain negatives like these". The eight rows show `ssa` at -0.001.
- **F01 and F05:**
  - F01 is 2016-17: it repeats 2 periods with identical rows.
  - F05 is 2020-21: it repeats 16 periods with conflicting values.
  - Both fail with `DuplicateEntityKeyError` (ADR-040, rulings 748/749); silver has no row for either year.
  - The page says so in five places: `facts.history` ("gridflow loads 2017-18 on, except 2020-21"), the chart caption ("No data April 2020 to March 2021; the 2016-17 and 2020-21 files fail to load"), the x label, the alt text, and `notebook.needs` ("from 2017-18").
  - The chart starts 1 April 2017.
- **Truncation check (defect 20i):**
  - Silver holds a second capture of the 2026-27 dump (2026-10-16T19:20Z).
  - It is larger than the 2026-10-08 capture (9,600 against 9,168 rows, to 2026-10-17), so it is not truncated.
  - No other file gained a capture.
  - The chart takes the newest capture per period (dedup on date and period by `available_at`).
- **Revision found (not a truncation):**
  - The 2026-10-08 capture held 2026-10-06 to 2026-10-08 as all zero.
  - The 2026-10-16 capture fills 72 of those periods (2026-10-06 period 1: `bca` 0 to 49,207.8, `bva` 0 to 350).
  - Every other shared period is identical.
  - In the new capture, 2026-10-16 and 2026-10-17 are again all zero.
  - So the newest days of a capture read zero until filled. The chart window ends 30 September 2026 to stay clear.
  - The page states it once, in `what_it_is`. See Open questions.

## Evidence table

| Claim on the page | Evidence |
|---|---|
| BSAD submits actions outside the BM to the BSC, which governs imbalance settlement; "updated twice daily" | CKAN `notes` for the package in `gridflow/.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json` (extracted) |
| NESO lists yearly files from 2016-17 | Same snapshot: 11 resources, 2016-17 to 2026-27 |
| gridflow loads 2017-18 on, except 2020-21; both files fail to load | Silver: 9 resource ids at 2026-10-08, none for `30ba12a9...` or `5d0f2119...`; K-AS-4-FACTS section 4 table (F01 2 identical excess rows; F05 16 conflicting); note Holds table |
| Key `resource_id, settlement_date, settlement_period`; latest keeps one | Registry `entity_key`, `latest`, `latest_partition`; Polars latest view 149,856 rows = 149,856 distinct settlement pairs |
| Units £ and MWh; vendor meanings in the guide lines | Field info `info.unit` and `info.description`; epoch 1 headers `BCA (£)` and so on in the registry |
| Sign not stated by NESO | Field info gives title, description and unit only; K-AS-4-FACTS line 344 |
| "no contract or party named" | Registry headers in both epochs: date, period and six values; K-AS-4-FACTS line 277 |
| "The newest days of one capture read zero and were filled by the next" | Polars full join of the two 2026-27 silver files: 9,168 shared periods, 72 differ, all on 2026-10-06 to 2026-10-08, where every column of the older capture is 0 |
| Settlement period 1 to 48; 46 or 50 on clock-change days | Registry bounds 1..50; field info "Settlement period 1 runs from 00:00-00:30"; note body lists the 46 and 50 period days |
| `timestamp_utc` is the period start, from date and period | Registry `temporal: sp_pair`; silver `timestamp_utc == event_time`; 2025-11-20 period 31 = 15:00 UTC (sample) |
| `published_at` null; capture time from bronze | Registry `vintage: capture_fallback`; silver has 0 non-null `published_at`; `capture_written_at` equals `available_at` |
| Requests: `package_show`, upload URL, `/datastore/dump/<id>` | `client.py` `iter_members` 1705-1771: one `package_show`; live `url_type == "datastore"` goes to `_dump_member`, otherwise `_capture_member` through `resource.url`. Snapshot `url_type` is upload for 2016-17 to 2020-21 and datastore after. Host `https://api.neso.energy` (`config/sources.yaml:756`). URLs from the snapshot |
| Upload skipped if `last_modified` unchanged; dump kept only if its body changed | `client.py` 1751-1765 and `_dump_member` (same mechanism as the approved Aggregated BSAD page) |
| CLI `gridflow ingest/transform neso_data_portal bsad_forward_contracts --last 24h` | `config/sources.yaml:799` dataset key; `_assert_window_admissible` (client.py 1474) refuses a window ending more than 48 h ago; same commands as the approved Aggregated BSAD page |
| Notebook lead: view `silver_neso_data_portal_bsad_forward_contracts_latest`, filtered on `settlement_date`, both ends, lineage dropped | `_validate_dataset_for_source("neso_data_portal", "bsad_forward_contracts")` returns `settlement_date`; `_relation_name_for_dataset` returns the view (run with the gridflow_models interpreter) |
| Buy line: peak £23,988,237.84 on 2022-08-11; 13 days over £10M, 11 in 2022, two since (£14,804,786.58 on 2025-11-21, £10,197,869.26 on 2026-01-06) | Committed series JSON, read back in Python |
| Both lines under £1.6M a day to March 2020 | Committed series: buy max £1,593,607.50, sell max £907,571.82 |
| Sell line: peak £2,639,168.04 on 2023-05-29 | Committed series |
| Break from 2020-03-31 to 2021-04-01 | Committed series: no points between those dates |
| `y_min: -500000` | Lowest drawn value is -20,578.22 (buy, 2026-04-04), so the floor is below the data. It lifts the zero line off the axis, so the 2020-21 break reads as a gap. In a zoomed screenshot the coloured lines break and only the template's grey zero rule crosses |
| Sample: 2025-11-20 periods 31 to 38; `bca` and `bva` constant over each pair of periods (hourly); `ssa` -0.001 to period 37, 0 at 38 | Committed sample rows |
| Notebook output 1: tail of periods with `bca` over £1M (2025-11-21 and 2026-06-24 rows) | Committed notebook JSON |
| Notebook output 2: yearly sums, 2017 to 2026 with no 2020; buy cost peaks at 618,476,494 in the year from April 2022 | Committed notebook JSON |
| Notebook plot: mean `sva` 140.9 MWh at periods 9 and 10; mean `bva` 92.4 at 15 and 16 and 83.6 at 37 and 38; `sva` under 2 MWh at 37 to 40 | Committed PNG; per-period means cross-checked with Polars on the same window |
| Related: Elexon NETBSAD terms "with names like these" | NESO descriptions ("Net Buy Price Cost Adjustment") against Elexon NETBSAD column names (`net_buy_price_cost_adjustment_energy` ...). Names only; the mapping is not verified |

## Body corrections (canonical note)

The note said every resource had one capture (2026-10-08). Silver also holds the 2026-10-16 capture of 2026-27. Smallest-span fixes:

1. **Files table lead-in:** adds "and 2026-27 a second (2026-10-16, below)".
2. **New paragraph "Later capture (2026-10-16)"** after the totals paragraph. It gives:
   - rows, dates, and that no other resource gained a capture;
   - the 72 filled zero periods, with an example;
   - the 432 new periods, and that 2026-10-16 and 2026-10-17 are all zero;
   - 159,024 rows across captures and 149,856 in the latest view, with the Polars check cited.
3. **Vintage clock:** adds "(2026-10-16 for the second 2026-27 capture)".
4. **Event clock:** "27 have a period start after their capture time" adds "55 in the 2026-10-16 capture" (Polars, `timestamp_utc > available_at`).
5. **Row counts per family:** adds the 9,600 second-capture rows and the 149,856 latest-view rows.
6. **Cadence:** "one capture per resource (all 2026-10-08)" now adds "except 2026-27, whose 2026-10-16 capture appended 432 periods and filled 72 zero periods of 2026-10-06 to 2026-10-08".
7. **Known issues:**
   - The mixed-vintage bullet adds the 2026-10-16 time.
   - New bullet "The newest days of a capture can read zero": treat the last days of the open year as provisional.

Nothing else in the body changed.

## Not verified

- **What the six variables mean economically, and how they enter the imbalance price.** The page states only the vendor descriptions and claims no formula or price. What the data shows:
  - `bva` is non-zero in 10,245 periods where `bsa` is zero, so the net volume adjustment is not just the gross trades.
  - The median of `bca`/`bva` is about £146/MWh; of `sca`/`sva`, about £25/MWh.
- **The hourly pairing.** Values repeat over each pair of periods (1 and 2, 3 and 4 ...) on most days, which looks like hourly products. The page says "hourly `bca` and `bva` blocks" only for the eight rows shown.
- **Why 2016-17 and 2020-21 repeat periods.** Which 2020-21 value set is authoritative is still an open `TODO` in the note. The page says only that the files fail to load.
- **NESO's methodology on later inclusion of contracts.** I relied on K-AS-4-FACTS line 329, which cites the BSAD methodology. I did not read the PDF, and the page does not cite it.

## Open questions

- **The late-fill sentence in `what_it_is`.** "The newest days of one capture read zero and were filled by the next" is a project observation across two captures, not a vendor statement.
  - A user needs it, because recent zeros are not real zeros.
  - The checker or seat should rule whether it counts as a local-data reference. If it does, cut it with no other change: the chart window avoids those days.
- **Chart choice.**
  - Chosen: daily cost adjustments in £. They show the 2022 rise and the 2020-21 gap on one honest axis.
  - Rejected: daily volumes in MWh. Over 9.5 years the two lines are dense and noisy.
  - Alternative: a single financial year of volumes.
- **The `elexon/netbsad` related note** says "names like these", as on Aggregated BSAD. It claims no mapping.

## Template problems

None blocking.

- **Caveat-grammar warning.** `--only` prints `WARNING: 22 line(s) in 'Known issues and gotchas' sections could not be placed by the caveat grammar and were dropped`.
  - The dataset template does not render that section, so nothing is lost.
  - The note's multi-line bullets predate this edit; my added bullet adds a few lines.
- **Notebook preview** shows only the first two code cells, as on other pages.
- **Notebook lead at 390.** The long view name breaks mid-word (`...bsad_forward_contr|acts_latest`). This is a known template item, and nothing is clipped.
- **Sample frame number format.** Large `bca` values print in exponent form (`1.1593e6`), as Polars prints them. Not an error, but it hides digits in the folded frame.

## Defects

Paste as is.

- **neso_data_portal / bsad_forward_contracts: the newest days of a capture are zero and filled later (vendor behaviour; documented in the vault note).**
  - The 2026-10-08 capture of the 2026-27 dump held 2026-10-06 to 2026-10-08 as all zero.
  - The 2026-10-16 capture fills 72 of those periods (2026-10-06 period 1: `bca` 0 to 49,207.8 £, `bva` 0 to 350 MWh) and holds 2026-10-16 and 2026-10-17 all zero.
  - Every other shared period is identical. The latest view picks the newer capture, so silver is right.
  - Consumers must treat the last days of the open year as provisional.
  - Severity: low (documentation; no data loss).
- **neso_data_portal / bsad_forward_contracts vault note stale after the 2026-10-16 capture (fixed on branch `docs/neso-dp-ancillary-b`).**
  - The note said one capture per resource, 149,424 rows and coverage to 2026-10-08.
  - Silver holds 159,024 rows across captures, 149,856 in the latest view, to 2026-10-17.
  - Severity: low.
- **neso_data_portal / bsad_forward_contracts failed files (already recorded under ADR-040, rulings 748/749/760; no new entry needed).**
  - FY 2016-17 repeats 2 periods with identical rows.
  - FY 2020-21 repeats 16 periods with conflicting values.
  - Both fail with `DuplicateEntityKeyError`. The page states the loss plainly.
- **gridflow-front-end build: caveat-grammar warning on this note (22 lines dropped).** Harmless, but noise. Severity: nit.
