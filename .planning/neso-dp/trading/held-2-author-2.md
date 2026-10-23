# Held Trading pages, part 2: writer report, round 2 (2026-10-23)

These are the fixes for `held-2-review.md`. GTMA was APPROVE with 4 nits, the interconnector page APPROVE with 3 nits,
and upcoming trades REVISE with 1 major and 2 nits. I started no server or background process.

## Upcoming trades

1. **Major, `page.held`.** It now reads: "NESO's cost note multiplies `Volume`, labelled MWh, by duration, and
   `Last_Updated` has no clock." (14 words.) The duration formula is now attributed to NESO's cost note and is no longer
   stated as NESO's practice.
   - **Measured fact in the note body:** the Holds section, question 1, and a pointer in Units now say the rows do not
     follow the cost comment.
   - In every row of both captures, `Cost` equals `Volume` × `Price` exactly, with no duration factor: 28 of 28 rows
     on 2026-10-08 and 48 of 48 on 2026-10-16.
   - No row fits `Volume` × `Price` × 0.5.
   - I reproduced it myself in bronze, with two worked rows: `ES00382991`, period 47 of 2026-10-16, 110 × 218 =
     23,980; and `ES00380892`, period 29 of 2026-10-08, -3.5 × 76.96 = -269.36.
   - The note says the rows behave as energy per period in MWh, which matches the unit label but not the "Average
     Volume" title or the cost comment, and that the hold stands.
2. **Nit, `related[0]`.** It now reads "Past GTMA trades; this table lists those still to come" (10 words).
3. **Nit, `raw_feed.note`.** It now reads "Each fetch replaces the whole list."

## Historic GTMA trades

1. **Nit, the MWh attribution.**
   - `what_it_is` now says "Files to June 2021 give a trade's total, which NESO's dictionary calls MWh".
   - The lead member's `differs` now reads "...; total per trade, MWh".
2. **Nit, the default warning.** It now reads "NESO warns trades can change after delivery, as when a counterparty
   defaults; the data may not be updated." This follows NESO's "post-delivery things can change". `what_it_is` is at
   60 words, within budget.
3. **Nit, `members[0].held`.** It now reads "...; the 2020-21 file repeats ten trades." (16 words.) This is a fact of
   NESO's file, which has `last_modified` 2021-04-06.
4. **Nit, the yearly-table `Cost` wording.** Left as the approved enactment wording, so all four pages match. Changing
   it to the "rate against total" phrasing is a seat call across the approved pages.

**Note body (the checker's gap):** the upload Units paragraph now records the following, from bronze, checked
2026-10-23:
- In all seven upload bodies, `Cost` equals `Volume` × `Price` on every row with a parsable, positive window, whatever
  its length.
- This supports the dictionary's MWh over the package text's MW.

The `TODO: verify` with NESO stays.

## Interconnector requirement and auction summary

1. **Nit, `page.held`.** It now reads "NESO updates a lot in place with its auction result; the file keeps no earlier
   state." (16 words.) It says "a lot" because 230 lots still have no clearing price on 16 October.
2. **Nit, `related[1]` (`elexon/soso`).** It now reads "Elexon's system operator to system operator interconnector
   trades".
3. **Nit, `facts.vendor`.** It now reads "NESO Data Portal, package Interconnector Requirement and Auction Summary Data:
   one table, one PDF" (14 words).
   - `page.title` is unchanged: it is the manifest's name, a seat item.

## Gates

- All three notes are still CRLF. The CR count equals the line count: GTMA 466, IC 335, upcoming 343.
- All three are mirrored, and `cmp` is clean.
- `parse_page_fields` and `anatomy_errors` return `[]` on all three.
- `--only` builds of `gtma_trades_data`, `ic_requirement_auction` and `upcoming_trades` all wrote, with no errors.
- The detector returns `[]` on all three.
- Rendered `<main>`: no dashes and no banned words, and every new string is present.
- No new screenshots: the changes are short prose swaps of equal or shorter length. The one longer string is the IC
  vendor fact, which wraps in the facts column like the GTMA one did in round 1.

## Defects (new or updated)

- **NESO, upcoming trades (new; log for remediation):** `Cost` equals `Volume` × `Price` in every row of both
  captures, although the dictionary's cost comment includes a duration and titles `Volume` "Average Volume". The
  checker found it, and I reproduced it.
- **NESO, Historic GTMA upload files:** the rows agree with the dictionary's MWh, not the package text's MW. This
  strengthens the defect already recorded.
- **NESO, interconnector auctions:** 230 lots still have no clearing price in the 16 October body.

The earlier NESO defects stand, and the checker confirmed them. No gridflow defect.
