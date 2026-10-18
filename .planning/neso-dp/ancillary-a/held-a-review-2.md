# Held pages, Ancillary services part 1: checker re-review (2026-10-18)

Re-checked against `held-a-author-2.md`, the diffs of the four canonical notes against `origin/master` (front matter only), the
rebuilt pages, local silver (read only) and the seat's manifest change.

Gates: `gridflow-build --only neso_data_portal/<lead>` ok on all four; detector `[]` on all four (absolute path); `cmp` canonical
note against mirror clean on all four; 0 em dashes; no `live`, `now`, `yet`, `soon`, `pending`, `coming`, local counts or capture
dates; 390 view through my own 390 px iframe on port 9972 (stopped), plus 1440 for the 4-day heading: nothing clipped or
overlapping. The manifest title is "Dynamic Containment 4 day forecast", equal to the page title.

## The two majors

1. **Auction-number line (`eac-mock-auction-results` `what_it_is`) — fixed.** New text: "Mock auction numbers also appear in NESO's
   real auction history: never join on them." Reproduced both facts. (a) Each mock auction number covers one delivery day: 22 ids in
   the summary, buy-order and sell-order tables, each with one delivery day (two calendar dates because the day starts at 23:00).
   (b) Numbers 1 to 13 also appear in the real archive: `eac_results_summary_fy` holds auction ids 1 to 13 with delivery days from
   2023-11-02 onward, while the mock's 1 to 13 are delivery days from 2026-02-23 onward; the mock intersects no other `eac_results_*`
   table. The sentence no longer claims numbers repeat within the mock (it never says "one delivery day" either, which is fine).
   Residual wording nit below.
2. **Related note to `eac-br-auction-results` — fixed.** "Real Balancing Reserve results; this mock also rehearses that service."
   True: the mock summary holds `Balancing Reserve` with `PBR` and `NBR`.
3. **Same line on `eac-br-mock-auction-results` — true there too.** Its 13 auction numbers are 1 to 13 and all 13 are in the real
   archive (and in the other mock). Note they are NOT in the real Balancing Reserve archive (`eac_br_results_*` intersection is
   empty), so the line is true only of the real EAC history; see nit 4 below.

## The 15 nits

All applied as the writer's table says; spot-verified in the diff and render:

| Nit | State |
|---|---|
| 1.1 service codes | fixed ("NESO's dictionary does not define ...") |
| 1.2 file addresses | fixed: each member lists `package_show?id=dynamic-containment-4-day-forecast` then the file; the note says the address changes with each upload; wraps cleanly at 390 |
| 1.3 "four-hour" | fixed |
| 1.4 how_used | fixed ("Read beside the other ancillary-service requirement forecasts", the note's own use) |
| 1.5 title | fixed: page and manifest both "4 day" (see nit 6) |
| 2.1 `package_show` | fixed, first request |
| 2.2 band completeness | fixed (dictionary wording) |
| 2.3 sizing | fixed (see nit 5) |
| 2.4 related | fixed |
| 3.3 daily reasons | fixed: "NESO's daily file holds only a header row when fetched; gridflow keeps it in bronze only." plus "header only when fetched" in each `differs` |
| 3.4 clock | fixed: "NESO does not say if times are UTC or UK local." (true per both notes) |
| 3.5 parser use | fixed: the three named columns exist in the mock buy and sell tables |
| 4.1 cadence | fixed: "NESO lists daily; its notice says February 2024 only; gridflow re-checks at most weekly" (both NESO statements are quoted in the note; the weekly re-check is `client.py` `_FROZEN_CADENCE`) |
| 4.2 related scope | fixed on both mock pages ("A second mock package, named ...") |
| 4.3 | no finding |

## New nits (none blocks)

1. **nit** `eac-mock-auction-results` `what_it_is`: "Mock auction numbers also appear" covers 13 of the 22 numbers (1 to 13). True as an existence statement; "Mock numbers 1 to 13 also appear" would be exact.
2. **nit** `eac-br-mock-auction-results` `what_it_is`: "They show mechanics, not real prices or volumes" lost the word "auction" in the shortening; and "EAC" is now never spelled out on this page (the EAC mock page does spell it out).
3. **nit** `eac-br-mock-auction-results` `what_it_is`: "NESO's real auction history" can read as the real Balancing Reserve archive, where the numbers do not occur; "real EAC auction history" is exact.
4. **nit** `long-term-forecasts-for-dc-dm-dr-requirements` `how_used[0]`: "Which requirement bands NESO thinks likely" reads as a probability reading that the note still lists as unverified (`TODO: verify` the formal probability meaning). "NESO's weights over requirement bands, by month and EFA block, a year ahead" avoids it.
5. **nit** (seat) the Data sources hub card still reads "Dynamic Containment 4 Day Forecast" (from the unrebuilt hub); the page and manifest say "4 day". Rebuild the hub when the batch is assembled. At 1440 the heading breaks after "4" ("Dynamic Containment 4 / day forecast"); cosmetic.

## Verdicts

| Page | Verdict |
|---|---|
| `dynamic-containment-4-day-forecast` | APPROVE |
| `long-term-forecasts-for-dc-dm-dr-requirements` | APPROVE |
| `eac-mock-auction-results` | APPROVE |
| `eac-br-mock-auction-results` | APPROVE |

0 blockers, 0 majors, 5 nits.
