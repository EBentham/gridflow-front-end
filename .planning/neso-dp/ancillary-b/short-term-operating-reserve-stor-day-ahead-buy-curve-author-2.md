# Writer report, round 2: STOR day-ahead buy curve

Fixes for review 1 (REVISE: 2 majors, 4 nits) under the seat's rulings. `page:` block only; body untouched.

**Status:** `gridflow-build --only neso_data_portal/stor_da_buy_curve` exit 0 (template-wide caveat warning only);
detector `[]`; 0 em dashes. Mirror `cmp` identical; note CRLF throughout (420 CRLF, 420 lines). Series re-distilled
(unchanged: 365 points, 6.82 to 33.53, median 9.83), sample regenerated (same eight rows), notebook re-run (6 cells,
no errors, 1 image). Screenshots at 1440, 1024, 768 and 390 replaced in `stor-da-buy-curve-shots\`; nothing clipped,
including the longer chart title and key label. Server on 9989: PID 4751 recorded, stopped by that PID, port down.

## Fixes

1. **Units (major), seat ruling.** Dropped the clearing-price comparison from the results cell: no `clearing`
   aggregate, no `clearing_at_or_below` column, no unit comment. The cell now reads only `contracted_mw` from the
   results (days with an accepted tender, days with contracted MW above the curve MW; neither needs a price
   conversion). Output: days 365/364/366/365/365, accepted 362/362/365/363/365, contracted above MW 63/103/158/243/141.
   `how_used[0]` now names both units as NESO labels them: "Each day's maximum availability price, £/MWh, beside its
   clearing price in £/MW/Hr".
2. **"Every" (major), seat ruling.** `facts.vendor`: "one uploaded CSV of NESO's daily STOR buy curves".
   `what_it_is`: "published the buy curves used to assess them; its file has no curve for 17 August 2022."
3. **"it" ambiguous (nit).** Last sentence of `what_it_is`: "NESO decommissioned STOR day-ahead after launching Slow
   Reserve" (NESO's package notes: "STOR DA has been officially decommissioned following the launch of the new Slow
   Reserve service").
4. **Not Active (nit).** `facts.cadence`: "NESO marks the package Not Active" (package `extras`).
5. **04:00Z (nit).** `record.fields.effective_from_date`: "Service day start, UTC with a `Z`: 05:00 UK time, so
   04:00Z in summer"; `effective_to_date`: "Service day end, likewise; 23 or 25 hours after the start at clock
   changes".
6. **"cut-off" (nit), seat ruling.** Dropped as a label: `summary` now "the maximum MW and availability price for each
   day's assessment" (dictionary words); `chart_view.title` "Maximum availability price, April 2025 to March 2026";
   key label "Maximum availability price"; alt "the STOR buy curve's maximum availability price per service day".
   "cut-offs" stays only in the hash-file sentence, where it is NESO's own description.

## Report correction (round 1, not on the page)

The contracted-MW to curve-MW ratio runs 0.037 to 1.30 (median 1.00), not 0.82 to 1.30 as round 1 said; 708 days
above 1, up to 401 MW over, unchanged.

## Defects (unchanged from round 1)

- **NESO data:** no curve for 17 August 2022; `BCN-` and `BCS-` ids skip numbers (53 and 169 unused); three curves
  list their points in reverse (`BCN-00000007`, `-00000176`, `-00001499`); contracted MW above the curve's "maximum
  MW requirement" on 708 of 1,817 service days (suggest a vault TODO beside the unit-relation one). Bronze equals
  NESO's datastore total, so gridflow lost nothing.
- No gridflow defect found.

Summary: both majors and all four nits fixed per the seat's rulings; build exit 0, detector `[]`, notebook re-run clean.
