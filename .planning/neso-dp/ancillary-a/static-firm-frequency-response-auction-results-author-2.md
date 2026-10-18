# Static FFR auction results: writer round 2

Fixes for `static-firm-frequency-response-auction-results-review.md` (REVISE: 1 major, 2 nits). Delivery-time wording left
as it was, per the coordinator.

Gates: canonical note edited with the Edit tool (still CRLF); mirror `cmp` identical; `gridflow-build --only
neso_data_portal/sffr_auction_results_main` succeeds (only the global known-issues warning); detector `[]`; em dashes 0.
No artefact changed: the edits touch only words, so the series, sample and notebook digests still pass.

## 1. Major: held line for buy orders (`page.family.members[1].held`)

Now: "NESO's dictionary calls the band cells prices, with no money unit: MW on nine, one blank." (16 words)

Why not "seven of ten": the checker read only the `description` field. NESO's field info
(`field-info/20261008T114228Z/sffr_auction_results_buy_orders.json`) has the same text, "The price relevant for up to
this volume limit", on all ten bands: in `description` on 25 to 150 and 250 (seven), and in `comment` on 175, 200 and
225 (three, whose `description` is empty). So "describes a price on seven of ten bands" would misstate the dictionary.
The new line drops "each" and states the units exactly as the checker verified them: `MW` on nine bands, blank on the
`200` band, no money unit on any. If the seat still prefers the seven-of-ten wording, it should say "in the description
field".

Body (smallest span, the checker's tidy-up): the band-columns paragraph now says the price text sits in the description
field on seven bands and in the comment field on `175`, `200` and `225`.

## 2. Nit: `page.record.fields.location`

Now: "A postcode, `AGG` or `Agg` (undefined by NESO), an outward code, or null" (13 words). Covers `AGG` 123,664, `Agg`
3,423, `BN44` 251 and the 275 nulls in the 2026-10-16 capture.

## 3. Nit: `page.how_used[2]`

Now: "Place rows in time by `date` and `efa`: `timestamp_utc` is the date's UK midnight." (14 words)

## Defects

None new.
