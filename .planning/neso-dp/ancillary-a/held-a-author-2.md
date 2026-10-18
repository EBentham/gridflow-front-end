# Held pages, Ancillary services part 1: writer round 2 (2026-10-18)

Answers `held-a-review.md`. Every finding fixed except the seat's own (page 1, nit 5), which I worked around.
I edited only the `page:` blocks of the four canonical notes (front matter, CRLF kept, body untouched) and mirrored
each byte for byte (`cmp` clean on all four).

| Page | Build `--only` | Detector | Em dashes / live, now, yet, soon |
|---|---|---|---|
| `dynamic-containment-4-day-forecast` | `dc_forecast_4d` ok | `[]` | 0 / 0 |
| `long-term-forecasts-for-dc-dm-dr-requirements` | `dc_dm_dr_long_term_fc` ok | `[]` | 0 / 0 |
| `eac-mock-auction-results` | `eac_mock_results_summary` ok | `[]` | 0 / 0 |
| `eac-br-mock-auction-results` | `eac_br_mock_results_summary` ok | `[]` | 0 / 0 |

Screenshots at 1440 and 390 (390 through my own iframe on port 9952):
`held-a-shots\r2-*.png`. Nothing clipped or overlapping. The 390 wrappers in my scratchpad had been overwritten to
point at port 9972; I recreated them under `w9952\`.

## Majors (`eac-mock-auction-results`)

1. **`what_it_is`, auction numbers.** I reproduced the finding: every one of the 22 mock auction numbers covers one
   delivery day (at most 2 calendar dates, because the day starts at 23:00). Numbers 1 to 13 also appear in
   `eac_results_summary_fy` (real, 880 ids) and in the Balancing Reserve mock. They do not appear in
   `eac_results_summary` or `eac_br_results_summary`. New sentence: "Mock auction numbers also appear in NESO's real
   auction history: never join on them." The same sentence replaces "never join them to real results" on the
   Balancing Reserve mock page: its 13 ids are also 1 to 13, so it is true there too.
2. **`related[2]`.** The note is now "Real Balancing Reserve results; this mock also rehearses that service".

## Nits

| Page, finding | Fix |
|---|---|
| 1.1 service codes | "NESO's dictionary does not define the two service codes" |
| 1.2 stale file addresses | Each member's `request` is a list: `package_show?id=dynamic-containment-4-day-forecast` first, then the file. The raw-feed note says `package_show` gives each file's address, which changes with each upload |
| 1.3 "four-hour" | Dropped: "each of a day's six EFA blocks, the first from 23:00 UK time the day before" |
| 1.4 `how_used[1]` | "Read beside the other ancillary-service requirement forecasts" (the note's own use) |
| 1.5 title mismatch (seat's) | The manifest is not mine. The page title is now "Dynamic Containment 4 day forecast", NESO's own wording. "4-day" broke at its hyphen in the 1440 heading ("4-" / "day"); "four-day" did not match the manifest. Seat: the manifest's "4-day" may want the same change |
| 2.1 `package_show` request | Added first in `raw_feed.requests` |
| 2.2 band completeness | "NESO lists nine requirement bands, `0-200` to `1600-1800`, each given a `Possibilities` value from 0 to 1 per target month, service and EFA block" (dictionary wording, no claim that the grid is complete) |
| 2.3 sizing | `how_used[0]`: "Which requirement bands NESO thinks likely, by month and EFA block, a year ahead" |
| 2.4 page 1 related | "The longer-horizon sibling, as weights over requirement bands" |
| 3.3 daily reasons | Reason: "NESO's daily file holds only a header row when fetched; gridflow keeps it in bronze only." Each daily `differs` ends "header only when fetched" |
| 3.4 clock | "Test-run results, not real procurement; NESO does not say if times are UTC or UK local." (all eight populated mock tables, both pages) |
| 3.5 parser use | "How orders fare in the auction: acceptance ratio, rejection reason, executed MW" (columns `acceptance_ratio`, `reason_rejected`, `executed_quantity`; the note's "auction mechanics"). The same change is on the Balancing Reserve mock page |
| 4.1 cadence | "NESO lists daily; its notice says February 2024 only; gridflow re-checks at most weekly" |
| 4.2 related scope | Page 4: "A second mock package, named 2025-2026, for response and the reserve services". Page 3: "A second mock package, named 2023-2024, for Balancing Reserve alone" |
| 4.3 | No finding |

To fit the Balancing Reserve mock `what_it_is` in its 60-word budget, I shortened "Enduring Auction Capability
platform" to "EAC platform" (the summary already names EAC) and the table list to "summary, results by unit, buy
orders, sell orders".

## Template problems

- A heading breaks at a hyphen ("4-" / "day" at 1440), as code spans do (`1600-` / `1800`). A nit.

## Defects

None new. The round-1 defects stand: the `dc_forecast_4d` date-order hold looks liftable on the 16 October capture
(the seat has ruled it stays held); the DC note body and ledger row describe one capture where silver holds two; and
the package registry status reads "eligible" while every table is held.

Summary: all 17 findings fixed (2 majors, 15 nits; the seat's title nit worked around), all four pages rebuilt with
detector `[]`.

## Nits fixed (answering `held-a-review-2.md`)

| Nit | Fix |
|---|---|
| 1. EAC mock, which numbers | "Mock numbers 1 to 13 also appear in NESO's real EAC auction history: never join on them." To stay inside 60 words, the table list now reads "summary, results by unit and orders" (the raw feed names each table) |
| 2. Balancing Reserve mock, "mechanics" and EAC | "They show auction mechanics, not real prices or volumes"; EAC is spelled out: "its Enduring Auction Capability (EAC) platform". To stay inside 60 words, the table list became "Its four tables mirror the real package" (the raw feed names all four) |
| 3. Balancing Reserve mock, which history | "Mock auction numbers also appear in NESO's real EAC auction history: never join on them." (true: its ids 1 to 13 are in `eac_results_summary_fy`, not in `eac_br_results_*`) |
| 4. Long-term `how_used[0]` | "NESO's weights over requirement bands, by month and EFA block, a year ahead" |
| 5. Hub card and heading break (seat) | Not mine: the hub needs a rebuild when the batch is assembled. I left the "4" / "day" heading break as it is (cosmetic, at a space) |

Gates: notes edited in the `page:` block only (CRLF kept), mirrored and `cmp` clean on all four; `gridflow-build --only`
ok for `dc_forecast_4d`, `dc_dm_dr_long_term_fc`, `eac_mock_results_summary` and `eac_br_mock_results_summary`;
detector `[]` and 0 em dashes on all four; 390 check of both mock pages (`held-a-shots\r3-*-390.png`) clean.

Summary: the four nits that fall to me are fixed (the hub rebuild is the seat's); all four held pages rebuild clean with detector `[]` and are ready for the owner's review.
