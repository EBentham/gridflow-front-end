# entsog/cmp: author report

Writer: Opus 5.5 · high, 2026-10-07. Family `cmp`, lead `cmp_auction_premiums`, members `cmp_unavailable_firm_capacity` and `cmp_unsuccessful_requests`.

## Recommendation: HOLD (stopped before writing)

I ran the two checks the brief puts first. Silver misleads overall for all three members, so I stopped as instructed. The page stays blank: no `page:` block, no body edits, no mirror copy, no artefacts, no build, no screenshots. Nothing in either worktree was changed.

All three tables lose their real records. Silver keeps only ENTSOG's "nothing to report" default sentences.

| Member | Bronze, 1 to 5 Aug (5 gas days) | Silver | Real records kept |
|---|---|---|---|
| `cmp_auction_premiums` (lead) | 1,061 a day: 54 real auction records + 1,007 default sentences | 5,035 = 1,007 × 5 | **0 of 54** on every day; no silver row has a premium |
| `cmp_unavailable_firm_capacity` | 870 a day: 291 real records + 579 default sentences | 2,920 = 579 × 5 + 25 | **25 on 1 Aug only**, 0 on 2 to 5 Aug |
| `cmp_unsuccessful_requests` | 1,082 a day: 43 real records + 1,039 default sentences | 5,197 = 1,039 × 5 + 2 | **2 on 1 Aug only**; and `timestamp_utc` is null on **5,197 of 5,197** rows (defect 8a reproduced) |

The real records are the same records every day: 54, 291 and 43 distinct `id`s, identical across all five bronze days. The bronze bodies are complete (`meta.count` = `meta.total` = 1,061, 870 and 1,082).

Every seat hold trigger applies at once:

- **Most records lost.** The lead holds nothing to chart. A family page charts the lead's table (`entsog.json` fixes the lead), so no member can carry the page.
- **Arbitrary picks.** The only real records kept are the ones whose period happens to start on a fetched day:
  - unavailable capacity: 25 monthly August products (Gasunie Deutschland 15, terranets bw 6, Open Grid Europe 2, Bulgartransgaz 1, Thyssengas 1, all 2026-08-01 to 2026-09-01);
  - unsuccessful requests: 2 FGSZ August requests (Csanadpalota entry and Dravaszerdahely entry).
- **Wrong-looking stamps.** Every default-sentence row has a zero-length period at 00:00+02:00, so `timestamp_utc` is 22:00 UTC on the previous day. That is DATA-MATRIX's "31 Jul to 4 Aug" for the first two members: the 1 Aug partition holds rows dated 31 Jul. The unsuccessful-requests stamps are all null.
- **Repeated rows.** The 4-tuple `(timestamp_utc, operator_key, point_key, direction_key)` repeats in 185, 115 and 994 groups. The default-sentence `id` names an adjacent operator (`5UK-TSO-0004ITP-00207exitUK-TSO-0001`), so a point with three neighbours gets three sentence rows a day (for example `CZ-TSO-0001` `ITP-00010` entry ×3). For unsuccessful requests every row has a null stamp, so the tuple collapses across days.

The unmerged gridflow fix for 8a (`fix/silver-entsog-cmp-timestamp`, commit `0b577dc`) is **necessary but not sufficient**. It changes only how `timestamp_utc` is picked (a row-wise `pl.coalesce` over `_TIMESTAMP_PRIORITY`). It does not touch the retention filter. After it lands, unsuccessful requests would get 22:00 UTC previous-day stamps from `capacity_from`, and the loss would remain: 2 of 43.

**What unblocks the page:** a silver fix that keeps CMP's real records (Defect 1), followed by a fresh transform. The stamp choice after that fix is an open design question (see Open questions 1).

## Why the records are dropped (code trace)

- `GenericEntsogJsonTransformer` sets `date_window_dataset = endpoint.requires_dates` (`silver/entsog/generic.py:332`). All three CMP endpoints have `requires_dates=True` (`connectors/entsog/endpoints.py:129-155`).
- `_read_bronze_records` runs `partition_records_to_target_date` on each bronze file (`generic.py:157-161`). That keeps a record only when `_record_date` equals the bronze day (`silver/entsog/datetime.py:56-87`).
- `_record_date` (`datetime.py:191-213`) takes the local date of the first parseable field in `_RAW_TIMESTAMP_PRIORITY` (`generic.py:390-398`). Order: `periodFrom`, `publicationDateTime`, `eventStart`, `auctionFrom`, `capacityFrom`, `validFrom`, `lastUpdateDateTime`.
  - **Auction premiums.** Real records send `periodFrom` null, so the date comes from `auctionFrom` (for example 2018-07-02, 2024-07-01, 2025-07-07). They are always dropped. Sentence rows send `periodFrom` = the fetched day 00:00+02:00, so they are kept.
  - **Unavailable firm capacity.** Real records are dated by `periodFrom`, a validity start from 2015 to 2026. Only the 25 whose period starts 2026-08-01 survive, on the 1 Aug partition.
  - **Unsuccessful requests.** Real records send `periodFrom` null and `auctionFrom` `"N/A"` (parsed as empty), so the date comes from `capacityFrom` (2025-10-01, 2026-07-01, 2026-08-01). Only the two 2026-08-01 records survive. Sentence rows are dated by `capacityFrom` = the fetched day.
- **Defect 8a.** `transform` picks the first `_TIMESTAMP_PRIORITY` column that *exists* (`generic.py:185-187`). `period_from` exists in unsuccessful requests but is null on every row, so `timestamp_utc` is null on all 5,197 rows.
- **Not exempt.** `generic.py:297-306` exempts `tariffs` and `tariff_simulations` from this filter (VTA-ENTSOG-TARIFF-01) and says CMP is "deliberately NOT" exempt, deferring it to `fix/entsog-cmp-schema-drift (ADR-021)`. Neither that branch nor an ADR-021 file exists in the local gridflow repo: `git branch -a` lists only `fix/silver-entsog-cmp-timestamp`, and `docs/adr` has no match.

## What the data is (research done before stopping)

- **Request.** One call per gas day, with no point filter, so the data is Europe-wide (`client.py:78-102`; `endpoints.py:129-155,263-281`). Verbatim `request_url` from the 2026-08-03 sidecars:
  - `https://transparency.entsog.eu/api/v1/cmpAuctions?limit=-1&timeZone=UCT&from=2026-08-03&to=2026-08-03&periodType=day`
  - The same shape for `/cmpUnavailables` and `/cmpUnsuccessfulRequests`.
- **Breadth in silver.**
  - Auction premiums: 47 operators, 654 points.
  - Unavailable firm capacity: 30 operators, 367 points.
  - Unsuccessful requests: 50 operators, 670 points.
- **What a real record is** (bronze):
  - **Auction premium:** one auction result for one operator, point and direction. Fields: `auctionFrom`/`auctionTo` (when the auction ran), `capacityFrom`/`capacityTo` (the product's capacity period, here 2025-10-01 to 2026-10-01, 2026-07-01 to 2026-10-01, or 2026-08-01 to 2026-09-01), and `auctionPremium`, `clearedPrice` and `reservePrice`. Of the 54 records, 49 have a premium above 0; the largest is 1,275.81 (FGSZ, Balassagyarmat exit, HUF).
  - **Unavailable firm capacity:** one record per operator, point and direction, with a validity period (`periodFrom`/`periodTo`, starting 2015 to 2026), `allocationProcess` `Auction` on all 291, and `auctionStartDate` `N/A`. **`value` and `unit` are null on every real record**, so the data is the period and the remarks, not a number.
  - **Unsuccessful request:** one record per operator, point, direction and capacity period. Fields: `requestedVolume`, `allocatedVolume`, `unallocatedVolume` and `occurenceCount` (vendor spelling). For example, FGSZ Csanadpalota entry, August: 51,000 requested, 17,000 allocated, 34,000 unallocated, kWh/d, count 2.
- **Units, from the rows.**
  - Auction premiums mix **six units across 54 records**: `EUR/kWh/h` 22, `EUR` 18, `HUF` 7, `EUR/kWh/y` 4, `EUR/kWh/q` 2, `BGN/kWh/d` 1. Any premium chart after a fix needs a filter on one unit.
  - Unsuccessful requests: `kWh/d` 41, `kWh/h` 2.
  - Sentence rows carry `unit` `""`.
  - The generic transformer converts nothing: it only casts `_NUMERIC_NAMES` to Float64 (`generic.py:80-93,189-191`).
- **ENTSOG definitions.** The notes quote none; each Overview is a one-line authored paraphrase. The only vendor wording is the default sentences:
  - Auction premiums: "Currently there are no firm capacity products on this point with a duration of one month or longer auctioned having cleared with an auction premium."
  - Unavailable firm capacity: "Currently firm products with a duration of one month or longer are offered on this point in the regular allocation process."
  - Unsuccessful requests: "Currently there are no request for firm capacity products on this point with a duration of one month or longer that weren't successfully fulfilled."
  - Other remarks include "No congestion on this point over the selected period", "Not applicable" and "Non-Cam Point". Blank remarks: 405, 320 and 405 rows.
- **Partition schema drift.** The 1 Aug partitions of `cmp_unavailable_firm_capacity` and `cmp_unsuccessful_requests` differ from 2 to 5 Aug: `point_type`, `id_point_type`, `data_set`, `is_archived` and the `booking_platform_*` columns come only from the real records kept that day. Sentence rows send lowercase `dataset`, so silver carries both `data_set` and `dataset`. The lead's five partitions share one schema. `gridflow-sample`'s single-schema `_scan` would likely fail on the two drifted members (the capacity report's template problem 1). I did not run it.

## Evidence table

| Claim | Evidence |
|---|---|
| Bronze against silver counts, per member and day | `scratchpad\cmp\count.py`: runs gridflow's own `partition_records_to_target_date` with `_RAW_TIMESTAMP_PRIORITY` on each bronze file, then compares with the silver partition heights (all equal to the kept counts) |
| 0 premiums in silver; sentence rows only | Kept real records = 0 on all 5 days; silver `general_remarks` top value is the auction default sentence (4,275 rows); `unit` `""` |
| 25 and 2 real records survive, 1 Aug only | `count.py` and `dropped.py`: unavailable capacity kept 604 on 1 Aug (579 + 25), the 25 starting 2026-08-01T06:00+02:00; unsuccessful requests kept 2 FGSZ records with `capacityFrom` 2026-08-01 |
| `timestamp_utc` null on 5,197 of 5,197 rows | `silver.py`: `df["timestamp_utc"].null_count()` = 5197 |
| 22:00 UTC previous-day stamps | `silver.py`: lead `timestamp_utc` values 2026-07-31 to 08-04 22:00 UTC, 1,007 each; unavailable capacity the same, plus 25 at 2026-08-01 04:00 UTC |
| Same real records every day | `ids.py`: 54, 291 and 43 distinct non-sentence `id`s, the same set on all 5 days |
| Dating field per record type | `ids.py`: real auction dated by `auctionFrom`, real unavailable by `periodFrom`, real unsuccessful by `capacityFrom`; sentence rows by `periodFrom` or `capacityFrom` = the fetched day |
| Repeated 4-tuples 185 / 115 / 994 | `silver.py` group-by on `(timestamp_utc, operator_key, point_key, direction_key)` |
| Fix branch only changes the stamp | `git diff master...fix/silver-entsog-cmp-timestamp -- src/gridflow/silver/entsog/generic.py`: one hunk at `:185-187` |
| Premium units | `dropped.py`: `Counter(unit)` over the 54 real records on 3 Aug |

## Body corrections: recommended, not applied

Deferred on purpose. The silver schema and sample sections change again once the retention fix lands, so editing them now is churn. The seat can rule otherwise. In each of the three canonical notes:

1. **Dedup key** ("`(id)` if present, else all non-`timestamp_utc` columns"): `id` is always present, so it is the vendor `id`, `keep="last"` (`generic.py:193-199`). State the repeated 4-tuple.
2. **Point-in-time field** `last_update_date_time`: the pipeline uses none. Say what `last_update_date_time` and `ingested_at` are (`generic.py:181-183,201-206`).
3. **Silver schema:**
   - fix the broken `id | str | int` and `data_set | str | int` cells;
   - add `timestamp_utc`;
   - add lowercase `dataset` for the two members whose sentence rows send it;
   - note the 1 Aug partition drift.
4. **Silver sample:** each note shows a bronze-shaped record with `+01:00`/`+02:00` stamps. Each is a record silver drops: a 2017 auction, a 2015-2026 unavailable period, and a 2025-2026 unsuccessful request. Replace each with a real silver row after the fix.
5. **Known issues:**
   - add the retention loss with the counts above;
   - add the null stamp (8a, unsuccessful requests);
   - add the sentence rows and their 22:00 UTC stamps;
   - add the repeated sentence rows per adjacent operator;
   - add the mixed premium units.

   The "Date-bound but light" bullet is right that real rows describe future capacity, but it omits that silver discards them.
6. **Overview:** quote the vendor default sentence as the only ENTSOG wording. For unavailable firm capacity, say that `value` is null on every real record.
7. **Historical depth, Publication lag, Modelling notes:** all `TODO`. Fill them only with vendor evidence or "Not vendor-documented here".

## Not verified

- ENTSOG's formal definitions of the three CMP measures (CMP Guidelines, Annex I of Regulation 715/2009). Neither the notes nor the vendor README quotes them, and I read no PDF.
- Whether `auctionPremium` is in the record's `unit`, or `unit` describes the cleared and reserve prices only. `EUR` against `EUR/kWh/h` is ambiguous.
- What `dataSet` 3/4/2 against sentence-row values means, and why the sentence `id` carries an adjacent operator.
- Whether a later fetch changes a stored CMP record. The five bodies are identical in their real records.

## Open questions

1. **What silver should hold after a fix.** Exempting CMP from the date window (the tariffs route) would keep every record but stamp `timestamp_utc` from `auction_from` (2017 onwards) or `capacity_from`. That puts a 2018 auction into a 2026 fetch's partition by stamp but not by file. Alternatives:
   - stamp each record with the fetched gas day, keeping the auction and capacity periods as columns;
   - treat CMP as a register (newest body only, like the reference family), since the same 54/291/43 records come back every day.

   This decides the key, the chart and whether the page has a time axis at all.
2. Should the default-sentence rows be filtered out, or flagged (for example `is_default_sentence`)?
3. Should the page wait for the fix (my recommendation), or ship as a register of default sentences? The second would mislead: the lead would show 0 auction premiums at points where ENTSOG reports 49.

## Template problems

None hit, since I built nothing. Expected after the fix: `gridflow-sample` `_scan` fails on partition dtype drift for the two non-lead members (as in the capacity report). The lead is unaffected in the current silver.

## Defects

- **[gridflow silver, HIGH] Generic ENTSOG silver drops every real CMP record and keeps only default sentences.**
  - `GenericEntsogJsonTransformer` filters each bronze file with `partition_records_to_target_date` (`silver/entsog/generic.py:157-161,332`; `silver/entsog/datetime.py:56-87,191-213`). It keeps a record only if the local date of its first parseable `_RAW_TIMESTAMP_PRIORITY` field equals the fetched day.
  - CMP records are dated by `auctionFrom`, `periodFrom` or `capacityFrom`, which fall years or months before the fetch.
  - 2026-08-01 to 05:
    - `cmp_auction_premiums` keeps 0 of 54 real records a day (5,035 silver rows, all sentences);
    - `cmp_unavailable_firm_capacity` keeps 25 of 291 on 1 Aug only (August monthly products), 0 on 2 to 5 Aug;
    - `cmp_unsuccessful_requests` keeps 2 of 43 on 1 Aug only.
  - `generic.py:302-305` defers CMP to `fix/entsog-cmp-schema-drift (ADR-021)`, which does not exist in the local gridflow repo.
  - Same class as VTA-ENTSOG-TARIFF-01 and the capacity-indicator loss. Blocks `entsog/cmp`.
- **[gridflow silver] 8a reproduced: `cmp_unsuccessful_requests.timestamp_utc` is null on 5,197 of 5,197 rows.**
  - `generic.py:185-187` takes the first existing `_TIMESTAMP_PRIORITY` column (`period_from`), which is null on every row.
  - `fix/silver-entsog-cmp-timestamp` (`0b577dc`, unmerged) coalesces row-wise. That is necessary but not sufficient: it does not change the retention loss above.
- **[gridflow silver] CMP default-sentence rows are stamped 22:00 UTC on the previous day.**
  - Sentence rows send a zero-length period at 00:00+02:00, so each partition's rows are dated the day before (DATA-MATRIX "31 Jul to 4 Aug").
  - The sentence `id` names an adjacent operator, so a point with three neighbours gets three identical rows a day. The 4-tuple repeats in 185 / 115 / 994 groups.
- **[gridflow silver] CMP partition schema drift.**
  - On 1 Aug, the kept real records add `point_type`, `id_point_type`, `data_set`, `is_archived` and `booking_platform_*` to `cmp_unavailable_firm_capacity` and `cmp_unsuccessful_requests`, with different dtypes from 2 to 5 Aug.
  - Sentence rows send lowercase `dataset`, so silver carries both `data_set` and `dataset`. `pl.read_parquet` over the glob needs `diagonal_relaxed`.
- **[vendor data, observation] Auction premiums mix six units in one table:** `EUR/kWh/h` 22, `EUR` 18, `HUF` 7, `EUR/kWh/y` 4, `EUR/kWh/q` 2, `BGN/kWh/d` 1 (54 records). It is unconfirmed which of `auctionPremium`, `clearedPrice` and `reservePrice` the `unit` applies to.
- **[vault, not yet corrected] All three CMP notes:**
  - dedup key and point-in-time field stale;
  - broken `id`/`data_set` schema cells, no `timestamp_utc`;
  - silver samples are bronze-shaped records that silver drops;
  - no mention of the retention loss or the null stamp;
  - `TODO` history, lag and modelling notes.

  Corrections are listed above for after the silver fix.
