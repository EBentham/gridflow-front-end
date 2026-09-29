# disbsad: checker re-review (after Revision 1)

Checker, 2026-09-29. This re-check answers `disbsad-review.md` (REVISE: 2 majors, 4 nits) against "Revision 1" in
`disbsad-author.md`. Inputs:
- the vault note diff (`git diff origin/master`);
- the mirror (cmp identical; the note is CRLF on all 309 lines);
- a rebuild with `gridflow-build --only elexon/disbsad`;
- the rendered HTML;
- Elexon's *Imbalance Pricing Guidance* v15.0, 25 June 2020 (59 pages), which I fetched from the URL cited in the
  note and read with pypdf.

## Verdict: APPROVE

No findings above nit. Both majors are fixed, the citation supports every claim it is used for, and nothing else
changed.

## Previous findings

1. **major, `raw_feed.note`: fixed.**
   - **Page:** it now reads "Replies fetched for this page also held the half-hour at `to`, so silver keeps it
     twice." This is scoped to the fetched replies, and it is true: in all nine bronze replies for 13 to 21 Sep,
     the last period starts exactly at `to`, and silver holds 9 keys twice (both re-derived in the first review).
   - **Note body:** Known issues gains the dated "Midnight half-hour in two replies (measured 2026-09-29)"
     bullet. It gives:
     - the nine windows and their fetch date (2026-09-26);
     - the within-day dedup (`disbsad.py:118-123`);
     - that `to` inclusivity is undocumented (`_publication_window.py:53-56`).

     It matches my earlier Polars results. This is now worded like boal.

2. **major, units £ and MWh: fixed.** The new body section "Vendor documentation" quotes the guidance at p. 16,
   and I checked the quote verbatim against the PDF:
   - "BSAD is made up of two parts: Balancing Services Adjustment Actions (disaggregated BSAD); and Buy Price
     Price Adjustment (BPA) / Sell Price Price Adjustment (SPA)."
   - "Each Balancing Services Adjustment Action has a: Balancing Services Adjustment Cost – value in £ (can be a
     NULL cost); Balancing Services Adjustment Volume – value in MWh; SO-Flag - either set to True/False; and STOR
     Provider Flag – either set to True/False."

   So cost in £ and volume in MWh per action are vendor facts. The field list also matches DISBSAD's own fields:
   `cost`, `volume`, `soFlag` and `storFlag`. The schema rows and the "Cost field unit" gotcha now cite it.
   - The p. 19 quote (SO flagging for Balancing Services Adjustment Actions) is also verbatim.
   - **Sign:** the note says "states no sign convention for the action's cost or volume". A search of the whole
     PDF bears this out. The "positive" and "negative" hits describe the NIV (p. 27, p. 30), party imbalance
     (p. 44), interconnector demand flows (p. 54) and the glossary. The p. 27/28 worked examples label actions
     "BSAA - Buy 35MWh", which gives a stack direction, not the sign of the volume field.
   - The page therefore still correctly says "the sign's meaning is not stated": in `fields.cost`,
     `fields.volume` and the System key note (3 occurrences in the rendered text).

3. **nit, System key note "in the note": fixed.** It now reads "Signed, -100 to 750 MWh here; the sign's meaning
   is not stated." The rendered text has no "in the note".

4. **nit, grain against the relation: accepted without change**, as the first review allowed once finding 1 was
   scoped. The notebook lead, chart and rows all dedup.

5. **nit, `plot_alt`: fixed.** The rendered image `alt` reads "blocks of up to 770 MWh".

6. **nit, body NETBSAD claims: fixed.**
   - The Overview now calls DISBSAD the individual Balancing Services Adjustment Actions, one of BSAD's two parts
     (guidance p. 16, verified). It adds "no vendor text found says NETBSAD is derived from DISBSAD (checked
     2026-09-29)".
   - The "aggregate" gotcha is replaced by the guidance reading plus a dated measurement (netbsad 0.0 on 17 Sep
     P40 to 44, while these actions total 450 to 750 MWh; reproduced in the first review).
   - The rendered page still makes no aggregation claim (0 hits for "aggregat").

## Nothing else broke

- `gridflow-build --only elexon/disbsad` succeeds, and `detect.mjs --json` returns `[]`.
- The chart spec is unchanged (series `spec_sha256` `30788edf7a56…`, 6 duplicates dropped). The series, sample
  and notebook files still have their first-review timestamps (00:37, 00:38 and 00:39), and the build's digest
  checks pass.
- The diff touches only the `page:` words named above and the body spans named above. The other body edits (the
  dedup key, `stor_flag` source and `ingested_at`) are as approved.
- Rendered text: no em dashes, middle dots or arrows, and no "live", "now", "real-time", "locally", "since 20" or
  "% of". The one "held" is "also held the half-hour", which describes the fetched replies, not local holdings.
- Layout: the changed strings are the same length or shorter than those I screenshotted at 1440, 1024, 768 and
  390 in the first review. The raw-feed note went from about 175 to 165 characters, and the others are within a
  few characters. I did not re-shoot.

## For the seat (not a disbsad finding)

- The netbsad note quotes the same guidance. Its p. 11 wording, "BSAD is split into two components", is correct.
  Two of its page numbers are off by one in this v15.0 PDF:
  - "It does not have a volume" is on p. 12;
  - the "System Buy Price = 30 + 6.50 = £36.50/MWh" example is on p. 30, not p. 29.
