# Static FFR auction results (`static-firm-frequency-response-auction-results`): writer report

Writer, port 9947, 2026-10-18. Lead `sffr_auction_results_main`; `sffr_auction_results_buy_orders` held. Manifest family
(slug, title, members, lead) is right; no change needed.

Status: `gridflow-build --only neso_data_portal/sffr_auction_results_main` succeeds (only the global "3 line(s) in Known
issues" warning other pages also show); detector `[]`; em dashes, middle dots and arrows in the page: 0; mirror `cmp`
identical; the vault note stays CRLF.

Chart: line, silver `sffr_auction_results_main`, clearing price of EFA blocks 1 and 5 per EFA date, 1 April 2023 to
17 October 2026 (1,296 dates, two series), £/MWh.

## Truncated-capture check

Two captures per family: 2026-10-08 and 2026-10-16. The newer ones are complete and larger, not truncated:

| Family | 2026-10-08 | 2026-10-16 |
|---|---|---|
| results (bronze and silver rows) | 229,631, dates 2023-04-01 to 2026-10-09 | 231,369, dates 2023-04-01 to 2026-10-17 |
| buy orders | 7,722, to 2026-10-09 | 7,770, to 2026-10-17 |

Every 2026-10-08 row recurs in the 2026-10-16 capture with all vendor columns equal (results: left join on the key, 0
missing, 0 changed in 12 columns; buy orders: anti-join on all 12 columns, 0). So `_latest` (the newest whole capture)
is safe, the chart's dedup is exact either way, and the notebook window (1 to 7 October 2026) returns 1,510 rows from
either capture.

## Evidence

| Claim on the page | Evidence |
|---|---|
| Grain: one row per unit, EFA date and EFA block; key `date, unit, efa` | registry `static-firm-frequency-response-auction-results.json` `entity_key` [date, unit, efa]; 231,369 rows, 231,369 distinct keys (2026-10-16 silver) |
| Daily auction; "NESO's catalogue" cadence | note: CKAN package notes "results of the daily Static FFR auction"; vendor metadata Update frequency: Daily |
| Six EFA blocks, block 1 from 23:00 the evening before | NESO field info for `EFA`: "6 EFA blocks in 24h window with first EFA block starting at 23:00"; delivery strings for block 1 read `D-1 23:00:00` to `D 03:00:00` |
| Block 5 labelled 15:00 to 19:00; block 1 labelled 23:00 to 03:00 | `delivery_start`/`delivery_end` per `efa`: one label pair per block in every block (0 blocks with two labels) |
| No "four-hour" claim | on clock-change dates the labels still read 23:00 to 03:00 (2023-10-29, 2024-03-31, 2024-10-27, 2025-03-30, 2025-10-26, 2026-03-29), so elapsed time differs; the page never says four hours |
| Units: `volume`, `accepted_volume` MW; `price`, `clearing_price` £/MWh | NESO field info (`field-info/20261008T114228Z/sffr_auction_results_main.json`): unit `MW`, `MW`, `£/MWh`, `£/MWh` |
| "NESO says all accepted units are paid it" | field info `Clearing Price`: "Price paid for all accepted unit for all awarded contracts.", title "Clearing Price for given EFA" |
| Rank: random, for clustered offers | field info `Rank`: "Before auction is run every bid will get randomly selected bid in case of cluster bids" |
| `status` as the auction algorithm cleared it | field info `Status`: "...accepted or rejected depending on how auction algorithm cleared" |
| "One price per block in NESO's results" (caption) | 7,776 date-EFA blocks, 0 with more than one `clearing_price`, 0 null; plus the vendor title "for given EFA" |
| "a rejected offer here shows `0.0`, not null" | visible in the eight rows; overall 37,362 Rejected rows all 0, 194,007 Accepted all equal to `volume` (scoped to "here" on the page) |
| `location`: a postcode or `AGG`, undefined by NESO | `AGG` 123,664 rows, `Agg` 3,423, `BN44` 251; field info says only "Post code of where unit is located" |
| `technology_type` null where NESO leaves it blank | 275 null rows; registry `nullable: true` |
| `timestamp_utc` UK midnight starting the date, as UTC | registry temporal `date_sp1` on `date`; sample row date 2026-10-08 has `2026-10-07 23:00:00 UTC`; 2024-03-31 gives 00:00 UTC |
| `published_at` NESO's last-modified for the whole file, read as UTC | sidecar `ckan_last_modified` "2026-10-16T10:46:09.594804" (naive) equals silver `published_at` 10:46:09.594804 UTC on every row |
| Requests | sidecar `request_url` of both 2026-10-16 captures, byte for byte |
| Raw-feed note: whole file unless `last_modified` unchanged | `client.py` `iter_members`: upload member is `unchanged` when the newest capture's `ckan_last_modified` equals the live one, else `_capture_member` downloads it |
| Commands `--last 24h`, "window must end recently" | `_assert_window_admissible`, 48 h tolerance (`_HISTORICAL_WINDOW_TOLERANCE`); same lines as the approved DM and DR pages |
| Notebook lead: `query()` reads `_latest`, filters `date`, both ends included | gridflow_models manifest: date column `date` (SQL DATE), relation `silver_neso_data_portal_sffr_auction_results_main_latest`; `_date_range_predicate` DATE is `BETWEEN ? AND ?` |
| History: delivery dates from 1 April 2023 in NESO's results file | first `date` in both captures 2023-04-01; stated as what the file holds, not a service start |
| Held line for buy orders | ledger row 88 question SFFR-BUY-CURVE-CELL-UNITS; field info: titles "Volume band in MWs procured on buy curve", text "The price relevant for up to this volume limit", unit `MW` on nine, empty on `200` |
| Buy orders `differs`: ten bands 25 to 250 MW | registry header `25` to `250`; field-info titles call them MW volume bands |

### Chart alt and key notes, from the committed series

All figures computed from `site/hifi/data/series/neso_data_portal/sffr_auction_results_main.json` (`statistics.median`,
true median of 1,296 values):

- Block 5: median 6.50; 224 dates at 10 or more; max 16.57 on 2023-12-30 (unique); min 0.60 on 2026-04-28 (unique).
- Block 1: median 1.55; 445 dates under 1; max 5.86 on 2023-10-24 (unique); min 0.40 on eleven dates (2024-11-05, -06,
  -13, -14, -15, -16, -26, -27, -29, 2024-12-13, -15).
- Block 5 above block 1 on 1,291 dates, equal on 1 (2026-04-28, both 0.60), below on 4 (2023-06-16, 2023-06-17,
  2025-07-12, 2025-08-09). The alt says "above on 1,291 dates", not a universal.
- Block 1 key note: 1.50 on all 59 dates 2025-04-19 to 2025-06-16 (the long flat run, real data, not a joined gap).

Dedup: `on [date, efa]`, newest capture kept; values are identical in both captures and one price per block, so nothing
is lost. Provenance: 461,000 rows read, 2,592 used.

### Sample rows

Delivery date 2026-10-08, block 2 (03:00 to 07:00 as labelled), filtered to the 2026-10-16 capture, ordered by price then
rank: PGFFR-5 1.67, PGFFR-9 1.89, PGHAT-1 1.95, ENDSR-2 1.98, LEV-FRU05 2.00 (Accepted); CITY01 2.00, PGFFR-8 2.11,
PGCOV-1 2.17 (Rejected); clearing price 2.00. These are the five highest-priced accepted offers and the three lowest
rejected in a 36-offer block (caption). `price` and `clearing_price` print before the volumes so they stay in view when the
frame folds at 768.

### Notebook

Query 1 to 7 October 2026; per-block table for 7 October (offers 35 to 36, offered 272.8 to 291.0 MW, accepted 152.8 to
248.3 MW, one price per block: 2.37, 2.17, 6.29, 2.37, 7.34, 9.27); step plot of the 42 block prices. Plot alt
reproduced: blocks 1, 2 and 4 from 1.52 to 2.37; block 3 at 6.29 (6.28 on 5 October); block 5 6.60 to 7.34; block 6 at
9.27, 9.41 on 3 October. Outputs: card, two frames, one image; no errors; `generated_by: scripts/run_notebooks.py`.

## Body corrections (canonical note, smallest spans)

1. Buy orders "Two clocks": "one capture exists" is stale; now says a second capture (2026-10-16, 7,770 rows to EFA date
   2026-10-17) repeats all 7,722 earlier rows unchanged; one comparison only.
2. Results "Two clocks": same correction (2026-10-16, `last_modified` 2026-10-16T10:46:09.594804, 231,369 rows to
   2026-10-17, all 229,631 earlier rows unchanged).
3. Both "Silver layout" lines: one Parquet file per capture (2026-10-08 and 2026-10-16), not one file.
4. Cadence: two captures per resource; each 2026-10-16 file is again the whole history from 2023-04-01 with earlier rows
   unchanged. The `TODO: verify` stays.
5. `Location`: not always a postcode (`AGG` 123,664, `Agg` 3,423, `BN44` 251 rows); the dictionary does not define `AGG`.
6. Known issues, new bullet: one clearing price per block, not always an accepted offer's price (122 blocks above every
   accepted offer; 963 Rejected offers equal to it; `Rank` does not order the ties consistently: accepted ranks all lower in
   231 of 456 tie blocks, all higher in 58); `TODO: verify` how the price is set.

Not changed: the "Row counts and shape (silver, 2026-10-13)" tables are dated to the activation and still true for that
capture.

## Not verified

- How NESO sets the clearing price (above every accepted offer in 122 blocks); the page only quotes NESO's "price paid for
  all accepted unit" and claims no rule.
- What `AGG` means (likely aggregated units, but NESO does not say); the page says it is undefined.
- Whether `delivery_start`/`delivery_end` are UK local time; the page says "NESO states no clock".
- When each result was first published; nothing on the page claims a publication time.

## Open questions

- None blocking. A reader may want accepted MW against the Static FFR requirement; the related link points there without
  claiming a join, because the requirement note itself leaves that relation unverified.

## Template problems

Nothing new. Seen and already on the seat list: the unfolded frame scrolls sideways; the notebook preview breaks long
names at 390; the grouped-table stray index column (the 7 October block table shows an unnamed first column). A family page
does not print the `package_show` request line (as the Dynamic Containment review noted). The site has no dark theme
(`tokens.css`, `theme.css`, `site.js` carry no `prefers-color-scheme`), so screenshots are light only.

## Screenshots

`<scratchpad>\sffr-writer\shots\final-{1440,1024,768,390}.png` (390 through a 390 px iframe), plus browser-pane checks of
the unfolded frame at 1440 and the folded frame at 768. Nothing clipped or overlapping; no sideways page scroll at 390.

## Defects

- None in gridflow code or silver for this package.
- Vendor (NESO dictionary), `sffr_auction_results_main`: `Accepted Volume` description repeats the offered-volume text
  ("Volume offered per each unit"); `Location` is described as a postcode but carries `AGG`/`Agg` on 127,087 of 231,369
  rows and an outward code (`BN44`) on 251; the `Delivery Start`/`Delivery End` examples are day-first (`30/01/2023 07:00`)
  while the file serves `YYYY-MM-DD HH:MM:SS`. Already noted in the vault page; nothing published depends on them.
- Vendor semantics, `sffr_auction_results_main`: the clearing price is above every accepted offer in 122 of 7,776 blocks
  and NESO's text does not say how it is set. Candidate research question for the note's `TODO: verify`.
