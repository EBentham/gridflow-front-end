# Held pages, Ancillary services part 1: checker review (2026-10-18)

Checked against the batch tracker, the review rubric (held-page parts), the author brief, the writer's report, the four canonical
note diffs against `origin/master` (insertions to front matter only, CRLF kept), the mirrors, the built pages, the ledger rows,
the registry JSON, gridflow `client.py`, `endpoints.py`, `cli.py`, bronze sidecars and local silver (read only).

Gates run: `gridflow-build --only neso_data_portal/<lead>` ok for all four; `cmp` of canonical note against mirror clean for all
four; detector `[]` on all four; 0 em dashes; no `live`, `now`, `yet`, `soon`, `pending`, `coming`, planning words or local row
counts or capture dates on the pages; screenshots taken through a 390 px iframe (all four) and at 1440 (long-term and EAC mock),
nothing clipped or overlapping. The 9972 server is stopped.

Checked and fine: every request URL matches the connector (dump URL built from the resource id alone; upload URLs are the
`resources[].url` redirector, equal to the newest bronze sidecar `request_url`); resource ids map to the right table keys; the
ingest and transform lines are real CLI forms; each hold reason is true to the ledger question; "real" for not-mock is used
consistently and "live" never appears; the four daily mock files are header-only in bronze (114, 163, 238, 303 bytes, one line each).

Seat rulings applied: `dc_forecast_4d` stays held. Its reason says "NESO does not say", which is true (the dictionary documents ISO
dates; the files carry slash dates) and does not call the order unknowable. The 16 October capture does show day-first dates
(`17/10/2026` to `20/10/2026`), as the writer reported; no finding.

## 1. `dynamic-containment-4-day-forecast` (lead `dc_forecast_4d`) — APPROVE

1. **nit** `page.what_it_is`: "NESO does not define the two service codes, `DC-H` and `DC-L`." The note scopes this to the
   dictionary ("the vendor's definition of each is not stated in the dictionary"); the page drops the scope, and NESO's long-term
   package description speaks of Dynamic Containment "Low and High" requirements (the sibling page says "(High and Low)").
   Suggest "NESO's dictionary does not define ...".
2. **nit** `page.raw_feed.note` and `family.members[0].request`: the note says NESO renames the files on each upload (fine, and
   the two bronze captures differ in file name between 8 and 16 October for both files), but the two addresses shown are the
   16 October names, which are probably already replaced (the files change daily at about 13:05). Nothing says the addresses are
   read from `package_show` at fetch time. The stable address is `GET https://api.neso.energy/api/3/action/package_show?id=dynamic-containment-4-day-forecast`.
   `request` accepts a list of up to four, so each upload member could list `package_show` first and the file second, as
   `aggregated-bsad` does.
3. **nit** `page.what_it_is`: "each of a day's six four-hour EFA blocks". The note's own table shows EFA 1 is 3 hours on the spring
   change day and 5 hours on the autumn one. Suggest dropping "four-hour" or adding "usually".
4. **nit** `page.how_used[1]`: "Earlier forecasts set beside the volumes the auctions later cleared" is a use the notes do not state,
   and sits oddly beside a hold that says the archive's publication time is unknown. Low risk.
5. **nit** (seat, not writer) hub card and manifest title read "Dynamic Containment 4 Day Forecast" and "4-day"; the page title says
   "four-day". `site/hifi/data/neso_data_portal.json` page-set `title`.

## 2. `long-term-forecasts-for-dc-dm-dr-requirements` (lead `dc_dm_dr_long_term_fc`) — APPROVE

1. **nit** `page.raw_feed.requests`: one-table pages list `package_show` first in the showcase pages (`aggregated-bsad`,
   `eac-br-auction-results`); this one lists only the file address. The note's "one `package_show`" names a request the reader cannot
   see. Suggest adding `GET https://api.neso.energy/api/3/action/package_show?id=long-term-forecasts-for-dc-dm-dr-requirements` first.
2. **nit** `page.what_it_is`: "Each target month, service and EFA block gets a `Possibilities` value ... for each of nine bands" is a
   completeness claim the note measured on one capture ("the grid is complete for this capture"). The nine bands are NESO's
   dictionary list; the "every combination present" part is local. Suggest "NESO lists nine bands".
3. **nit** `page.how_used[0]`: "Sizing the frequency-response market a year ahead" reads as a MW sizing while the page's own hold says
   NESO gives no unit for the bands. The note words it conditionally ("would be a market-sizing input").
4. **nit** (page 1 `related`) "The same requirement a year ahead, as weights over bands" asserts the long-term requirement is the same
   quantity as the four-day one, with a unit that is unestablished. "The same service" or "the longer-horizon sibling" is safe.

## 3. `eac-mock-auction-results` (lead `eac_mock_results_summary`) — REVISE

1. **major** `page.what_it_is`: "Mock auction numbers repeat across dates: never join them to real results." Read plainly this says
   one mock auction number covers several dates. Within this package it does not: in silver the summary, buy-order and sell-order
   tables hold 22 auction numbers (1 to 22) and each maps to exactly one delivery day (two calendar dates only because the day starts
   at 23:00). Evidence: `group_by('auction_id').agg(n_unique(delivery_start[:10]))` returned 2 for all 22 ids in all three tables
   (max span 1 day). What the registry and K-AS-3 FACTS 4.1 mean is that the mock's small numbers also exist in NESO's real
   auction history for other dates (real archive numbers start at 1; `eac_results_summary_fy` carries ids 1 to 13) and in the Balancing
   Reserve mock. Suggest: "Mock auction numbers also appear in NESO's real auctions, for other dates: never join on them."
2. **major** `page.related[2].note`: "Real Balancing Reserve auction results, one product rehearsed here." Balancing Reserve is a
   service with two products (`PBR`, `NBR`); the mock summary holds both (and the sibling BR mock page says "two products").
   Evidence: `eac_mock_results_summary` distinct `(service_type, auction_product)` includes `Balancing Reserve / NBR` and `/ PBR`.
   Suggest "Real Balancing Reserve results; this mock also rehearses that service".
3. **nit** `page.family.members[4..7].held`: "As fetched, NESO's file has a header and no rows, so there is no silver table." True of the
   fetched files (each one line in bronze) and does not imply rows, but it is undated and the "so" gives the wrong cause: there is no
   silver table because gridflow defines no record for these files, not because of any rule about empty files. Also the raw-feed
   `differs` lines ("The daily counterpart of the summary") do not say the files are header-only, so the reader meets that only in the
   silver section. Suggest "NESO's daily file holds only a header row when fetched; gridflow keeps it in bronze only" and
   "header only" in each `differs`.
4. **nit** `page.family.members[0..3].held`: "NESO does not say which clock their times use" is true but vague for a reader; "UTC or UK
   local time" is the plain version of the ledger question.
5. **nit** `page.how_used[1]`: "Testing a parser or pipeline on EAC-shaped data" is not stated in the note, which gives only
   "understand the shape of the tables and the auction mechanics".

## 4. `eac-br-mock-auction-results` (lead `eac_br_mock_results_summary`) — APPROVE

1. **nit** `page.facts.cadence`: "Treated by gridflow as frozen: re-checked at most once a week." Accurate (registry `refresh: frozen`;
   `client.py:107` `_FROZEN_CADENCE` 7 days, `_frozen_not_due` 2409; hash suppression in `_dump_member`), and the writer rightly avoided
   a number or date the evidence does not settle. But "frozen" is undefined jargon, and the line says nothing of NESO's own words:
   its metadata says "Update frequency: Daily" and its package notice says the results are "scheduled to be published on this page from
   14th-23rd February 2024 only" (vendor quote in the note, so a date with evidence). A reader cannot tell NESO's label from
   gridflow's policy. Suggest: "NESO lists daily, but its notice says February 2024 only; gridflow re-checks at most weekly."
2. **nit** `page.related[1].note`: "Separate mock runs for response and every reserve service, named 2025-2026" states as settled what the
   note leaves open ("Whether the two mock packages overlap in scope is not established"). The data support separate runs (this
   package's windows are 2024, the other's 2026, and no summary key overlaps), but only the resource names are vendor evidence. Same
   point on page 3 `related[1]` ("Separate mock runs for Balancing Reserve alone"). Suggest "A second mock package, named 2025-2026,
   for response and the reserve services".
3. **nit** `page.what_it_is`: "(read as positive and negative reserve)" and "half-hour windows" match the showcase page and are
   labelled as a reading; fine. No finding beyond noting NESO's dictionary lists only the codes.

## Summary

| Page | Verdict | blocker | major | nit |
|---|---|---|---|---|
| `dynamic-containment-4-day-forecast` | APPROVE | 0 | 0 | 5 |
| `long-term-forecasts-for-dc-dm-dr-requirements` | APPROVE | 0 | 0 | 4 |
| `eac-mock-auction-results` | REVISE | 0 | 2 | 3 |
| `eac-br-mock-auction-results` | APPROVE | 0 | 0 | 3 |
