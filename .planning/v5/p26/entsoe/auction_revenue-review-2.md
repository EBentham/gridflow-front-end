# entsoe/auction_revenue: re-review after Revision 1

This re-checks the note after Revision 1 against `auction_revenue-review.md`. Inspection only. The canonical note is still CRLF, and the mirror `vault/entsoe/auction_revenue.md` is byte-identical (`cmp`).

## Verdict: APPROVE

0 blocker, 0 major, 1 nit.

## The five findings

1. **Blocker: ENTSO-E attribution (`summary`, `what_it_is`). Fixed.**
   - `summary` now reads: "TSO revenue from daily explicit capacity auctions on GB's borders with the Netherlands and Belgium, in EUR per hour, published by ENTSO-E."
   - `what_it_is` now reads: "Revenue from explicit capacity auctions on a border (Article 12.1.A), as ENTSO-E publishes it…"
   - Both agree with the note's overview ("Revenue earned by TSOs…").
   - A grep of the rendered page finds no "ENTSO-E's revenue" and no "ENTSO-E's daily".
2. **Nit: local-fetch wording. Fixed.**
   - `raw_feed.note` now reads: "GB-NL and GB-BE carry a series; the other six answer 'no matching data'", which matches the Reason 999 acknowledgement text.
   - `record.fields.in_area_code` now reads: "GB on the GB-NL and GB-BE series".
   - "returned" no longer appears on the page.
3. **Nit: grain. Fixed.**
   - `facts.grain` now reads: "One row per hour and zone pair per file; most hours in two files".
   - This is true: each file is unique on the key (`h6_market.py:91-99`), and 552 of 744 keys sit in two files.
4. **Nit: body count label. Fixed.** The label now reads "silver, Aug and Sep 2026: 1,296 rows, 744 keys".
5. **Nit: A03 vendor citation. Added.** The new "A03 curve" known-issues bullet quotes the ENTSO-E curvetypes guide v1.4 and cites `parsers.py:533-600`. See the new nit below for one section reference.

## New nit

1. **nit**: note body, `## Known issues`, "A03 curve" bullet: "(… v1.4, §4.3)".
   - **What is wrong.** The section reference is partly wrong. "only the position where a block change occurs is provided" is in §4.3 (A03 – Variable sized block). "The value of the Qty remains constant within each Block" is in §4 (Curvetype, the definition list, item 3).
   - **Evidence.** In the extracted PDF text, the heading `4 CURVETYPE` is at text line 264, the quoted sentence is at line 296, and `4.3 A03` starts at line 497.
   - **Fix.** Write "§4 and §4.3", or leave it: the quotes themselves are accurate.

## Did the revision break anything?

- **Build and detector.** `gridflow-build --only entsoe/auction_revenue` passes, including the artefact digest checks. The detector reports only the accepted `em-dash-overuse` advisory. The page has 0 `—`, 0 `→` and 0 `·`.
- **Leakage grep.** Clean: no `locally`, `held`, `our `, `since 20`, `% of`, digit+rows/days, `live`, `real-time` or `returned`.
- **Artefacts are unchanged in substance.**
  - Series: `spec_origin: vault`, 336 rows used, 336 duplicates dropped, maxima 115,433.72 (NL) and 81,197.76 (BE).
  - Sample: `gridflow-sample`, the same 8 rows (21 Sep 08:00 to 11:00Z; NL 42,566.24 to 115,433.72, BE 0.0).
  - Notebook: `scripts/run_notebooks.py`, 5 cells; outputs are a card, a df, text and an image, with no errors.
- **Unchanged fields.** The chart spec, `chart_view`, `record.select` and `key`, the notebook, the commands, the request and `related` still read exactly as checked in `auction_revenue-review.md`. Those checks stand.
- **Screenshots** (`scratchpad/arrev-shots/r2-*.png`, through a 9824 iframe wrapper, each Chrome call under `timeout 60`):
  - The longer summary and grain lines wrap cleanly in the hero at 390 and 1440.
  - The new raw-feed note is fully visible.
  - `scrollWidth` equals the width at both sizes, and nothing sits outside the viewport.
