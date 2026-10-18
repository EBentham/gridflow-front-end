# Static FFR auction results (`static-firm-frequency-response-auction-results`): checker review

Checker, port 9967 (stopped), 2026-10-18. Lead `sffr_auction_results_main`; `sffr_auction_results_buy_orders` held.

**Verdict: REVISE** (0 blockers, 1 major, 2 nits). One sentence to fix; everything else checked true.

Build `--only neso_data_portal/sffr_auction_results_main`: succeeds (only the global known-issues warning). Detector `[]`. Mirror `cmp` with the canonical note: identical. No sideways page scroll at 390 (scrollWidth 390); hero, chart, key, folded frame, guide and notebook not clipped at 1440, 1024, 768, 390.

## Findings

1. **major** `page.family.members[1].held` (rendered "Rows not shown: NESO's dictionary calls each buy-curve cell a price but gives it no money unit.")
   "Each" is wrong. NESO's field info for `sffr_auction_results_buy_orders`
   (`gridflow/.planning/research/neso-snapshots/field-info/20261008T114228Z/sffr_auction_results_buy_orders.json`) has ten band
   fields (fields 3 to 12). Seven carry the description "The price relevant for up to this volume limit"; three (fields 9, 10, 11,
   the 175, 200 and 225 bands) have an empty description. The other half is true: unit is `MW` on nine and empty on the
   200 band, so no field has a money unit. Suggested fix: "NESO's dictionary describes the buy-curve cells as prices on seven of ten bands and gives none a money unit."
   or, shorter, "NESO's dictionary gives the buy-curve cells no money unit." The canonical note body (Families, "What the columns mean")
   says the dictionary "describes the cell as" a price in the singular; a smallest-span "on seven of ten bands" there too would be tidy (body, nit level).

2. **nit** `page.record.fields.location` ("A postcode as NESO writes it, or `AGG`, which NESO's dictionary does not define")
   True but incomplete for a reader who will filter on it. In the 231,369-row capture: `AGG` 123,664 rows, `Agg` 3,423 rows,
   outward code `BN44` 251 rows, null 275 (Polars `value_counts` on the 2026-10-16 silver). Someone matching `location == 'AGG'` misses
   `Agg`. The body correction records all of this; the page line could say "`AGG` (also written `Agg`)". Not wrong, so nit.

3. **nit** `page.how_used[2]` ("`timestamp_utc` is the date's midnight")
   The guide line is exact ("UK midnight starting the EFA date's calendar day, as UTC"), but the bullet alone reads as 00:00 UTC.
   For 8 October 2026 it is 2026-10-07 23:00 UTC (the frame shows it); for 31 March 2024 it is 00:00 UTC. Suggest "the date's UK midnight".

## Coordinator's extra item: delivery start/end and `timestamp_utc`

- Page never says UTC for `delivery_start`/`delivery_end`. Guide: "Block start as NESO writes it, kept as text; NESO states no clock."
  That is accurate to the vendor: field info `Delivery Start`/`Delivery End` give unit `ISO-8601`, example `30/01/2023 07:00`, no zone.
  The sibling writer's "UK local wall clock" is an inference, not a vendor statement. The evidence for it is consistent
  (labels read 23:00 to 03:00 for block 1 and 15:00 to 19:00 for block 5 on all six clock-change dates in the file, which is what a local wall clock does)
  but NESO does not say it. Recommend leaving this page as is; if the seat wants "UK local" here, word it as "appear to follow the UK wall clock; NESO does not say".
- Code: registry `static-firm-frequency-response-auction-results.json`, family `sffr_auction_results_main`: `temporal {kind: date_sp1, date_column: date}`;
  `delivery_start`/`delivery_end` are `dtype: string, nullable: true` (never parsed). `silver/neso_data_portal/casting.py` (about lines 616 to 625)
  builds `timestamp_utc` from the `date` column only: `settlement_period_to_utc(date, 1)` (`utils/time.py:28`), a left join on `date`.
  So `timestamp_utc` does not come from the delivery strings. Silver confirms: 2026-10-08 gives 2026-10-07 23:00 UTC, 2024-03-31 gives 2024-03-31 00:00 UTC.

## What was checked and found true

**Chart** (series `site/hifi/data/series/neso_data_portal/sffr_auction_results_main.json`, `spec_origin: vault`, digest passes, no staged spec left):
- Recomputed every point from the 2026-10-16 silver (mean of `clearing_price` per date and block 1 or 5): 2,592 points, 0 mismatches; 1,296 distinct dates, none missing from silver; at most 1 distinct price per block.
- Alt and key numbers from the committed series, true medians: block 5 median 6.50, 224 dates at 10 or more, max 16.57 on 2023-12-30 (unique); block 1 median 1.55, 445 dates under 1, max 5.86 on 2023-10-24 (unique), min 0.40 on eleven dates, all in November and December 2024; block 5 above block 1 on 1,291 dates, equal only on 2026-04-28 (0.60 both, block 5's minimum), below on four. Key note 1.50 from 19 April to 16 June 2025: the longest run, 59 consecutive dates.
- Unit £/MWh from NESO's dictionary (`Clearing Price for given EFA`, unit `£/MWh`); title and caption match the spec's filter, window and aggregation.

**Clearing-price wording:**
- 7,776 blocks, 0 with more than one clearing price, 0 null, each with at least one accepted row. Clearing price above every accepted offer in 122 blocks (equal to the dearest accepted in 7,654, below in none); 963 Rejected offers priced exactly at the clearing price (555 blocks); no accepted offer above it, no rejected offer below it.
- The page quotes NESO ("NESO says all accepted units are paid it"; dictionary: "Price paid for all accepted unit for all awarded contracts.") and states no pricing rule; the 122 and 963 appear only in the canonical note's Known issues, with `TODO: verify`. The `Rank` claim there holds: in the 456 blocks with both an accepted and a rejected offer at the clearing price, accepted ranks are all lower in 231, all higher in 58, mixed in 167.

**Row, rejected, labels:**
- Grain unit, date, block: registry `entity_key [date, unit, efa]`; 231,369 rows, 231,369 distinct keys. Rejected 37,362 rows, all `accepted_volume` 0.0 (not null); Accepted 194,007 rows, all equal to `volume`. `service` is SFFR throughout.
- No "four-hour" claim on the page. `delivery_start`/`delivery_end`: one label pair per block; labels unchanged on the six clock-change dates.
- Eight rows: block 2 on 2026-10-08 in the 2026-10-16 capture has 36 offers; the five dearest accepted (LEV-FRU05 2.00, ENDSR-2 1.98, PGHAT-1 1.95, PGFFR-9 1.89, PGFFR-5 1.67) and the three cheapest rejected (CITY01 2.00, PGFFR-8 2.11, PGCOV-1 2.17) match the caption exactly; `generated_by: gridflow-sample`.

**Held line otherwise and family:** buy orders have 7,770 keys (efa_date, efa), ten bands 25 to 250, unit `MW` on nine bands and empty on the 200 band (only the "each" wording in finding 1 is wrong). "Two uploaded CSV files": the note records two resources and no documentation resources. Request URLs match the capture sidecars byte for byte. `_HISTORICAL_WINDOW_TOLERANCE` is 48 h (`client.py:130`, used at 1543).

**Notebook:** `scripts/run_notebooks.py`, no error outputs, cells read-only. `query()` reads `silver_neso_data_portal_sffr_auction_results_main_latest` (registry `latest: whole_capture`) on the `date` column (inclusive `BETWEEN`). The output head and the 7 October block table reproduce exactly from silver (offers 36/36/35/36/35/36, prices 2.37, 2.17, 6.29, 2.37, 7.34, 9.27). `plot_alt` checked against all 42 blocks: blocks 1, 2, 4 span 1.52 to 2.37; block 3 is 6.29 except 6.28 on 5 October; block 5 6.60 to 7.34; block 6 9.27 except 9.41 on 3 October; the shape repeats every day.

**Related notes:** each is 12 words or fewer. The requirement link is supported by NESO's own package text ("For service requirement see this page"); the requirement note says it makes no claim about how the requirement relates to auction clearing, and this page claims none beyond "the same EFA blocks". Post-tender reports are monthly; Phase 2 is a trial.

**The six body corrections (canonical note vs `origin/master`), each true and smallest-span:**
1. Buy orders "Two clocks": second capture 2026-10-16, 7,770 rows to 2026-10-17, all 7,722 earlier rows unchanged (anti-join on all 12 columns: 0).
2. Results "Two clocks": `last_modified` 2026-10-16T10:46:09.594804 (sidecar `ckan_last_modified`), 231,369 rows to 2026-10-17, all 229,631 earlier rows unchanged (left join on the key: 0 missing, 0 changed cells across the 12 non-key vendor columns).
3. Both Silver layout lines: one Parquet file per capture, two files each in `year=2026/month=10/`.
4. Cadence: two captures per resource; whole history again from 2023-04-01; earlier rows unchanged.
5. `Location`: `AGG` 123,664, `Agg` 3,423, `BN44` 251; dictionary does not define `AGG`.
6. Known issues: 122 blocks, 963 rejected offers, Rank ties, one price per block, the NESO quote; all reproduced above.
The "Row counts and shape (silver, 2026-10-13)" and the 1,288-date coverage paragraph are dated to the 8 October capture and stay true for it; Rank 1 to 42, Price 0.01 to 100 and Clearing Price 0.4 to 16.57 hold in both captures.

**Rubric sweep:** no em dashes, middle dots, arrows, planning words or codes on the page; no "live" or "now". "Delivery dates from 1 April 2023 in NESO's results file" is stated as what the file holds, with evidence (first `date` in both captures), the same pattern as approved pages. Template limits (folded frame at 390 shows only date, efa and unit; unfolded frame scrolls sideways; family page prints no `package_show` line) are seat items.
