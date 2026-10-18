# Static FFR auction results: checker re-review (round 2)

**Verdict: APPROVE.** The round-1 major is withdrawn (my error); both nits are fixed; no regressions.

## Round-1 major: the held buy-orders line (withdrawn)

The writer is right and my count was wrong. I read only the `description` field of NESO's field info
(`gridflow/.planning/research/neso-snapshots/field-info/20261008T114228Z/sffr_auction_results_buy_orders.json`). Reading both fields:
all ten band fields (ids 25 to 250) carry "The price relevant for up to this volume limit": in `description` on 25, 50, 75, 100,
125, 150 and 250 (seven), and in `comment` on 175, 200 and 225 (three, with an empty `description`). Units: `MW` on nine, empty on
200 (the 200 field's `comment` carries the price text and its `unit` is empty).

New line: "NESO's dictionary calls the band cells prices, with no money unit: MW on nine, one blank." True on every clause: all ten
cells are called prices (across both fields), no band has a money unit, nine say `MW`, one is blank. Plain English, 16 words, no codes.
Body paragraph now says the price text is in the description field on seven bands and the comment field on 175, 200, 225; true.

## Nits

- `record.fields.location`: now "A postcode, `AGG` or `Agg` (undefined by NESO), an outward code, or null". Matches silver (2026-10-16
  capture): `AGG` 123,664, `Agg` 3,423, `BN44` 251, null 275. Fixed.
- `how_used[2]`: now "`timestamp_utc` is the date's UK midnight." Consistent with the guide line and with silver (2026-10-08 gives
  2026-10-07 23:00 UTC; 2024-03-31 gives 00:00 UTC). Fixed.

## No regressions

- `gridflow-build --only neso_data_portal/sffr_auction_results_main`: succeeds (global known-issues warning only).
- Detector on the built page: `[]`.
- Mirror `cmp` against the canonical note: identical; note still CRLF.
- Rendered page: 0 em dashes, en dashes, middle dots or arrows; the new held line, location line and how-used line render as written.
- Artefacts untouched (the edits are words only); the delivery-time wording is unchanged and still accurate (NESO states no clock).
- Port 9670 not touched; no server of mine is running.
