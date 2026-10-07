# entsog/tariffs-and-simulations: re-check (round 2)

Checker: Sonnet 5.5 · high, 2026-10-07. Answers `tariffs-and-simulations-author-2.md` against `tariffs-and-simulations-review.md` (0 blockers, 4 majors, 6 nits).

## Verdict: APPROVE

All four majors are fixed and verified, all six nits are fixed or correctly declined, and nothing regressed. Two new nits only (below). Findings: 0 blocker, 0 major, 2 nit.

## Regression gate

| Check | Result |
|---|---|
| `gridflow-build --only entsog/tariffs` | exit 0, `wrote: data-sources/entsog/tariffs-and-simulations.html`; only the generic "no Pydantic class" warnings |
| `detect.mjs --json` (absolute path) | `[]` |
| `cmp` canonical vs mirror | `tariffs.md` and `tariff_simulations.md` byte-equal |
| Rubric greps on rendered text (locally, held, our, since 20, % of, digits plus rows or days, live, now, real-time, yet, soon, planned, coming, em dash, arrow, middle dot) | 0 hits |
| Budgets | build passes; caption is exactly 40 of 40 words (counted) |
| Screenshots (mine, 1440, 1024, 768, 390 in a true 390 px iframe, light) | hero, chart, key, frame, raw feed: nothing clipped or overlapping |

## The four majors

**1. Simulation described in ENTSOG's wording, with what silver keeps: fixed.**
- Page: `what_it_is` says ENTSOG describes the simulation as "costs for flowing 1 GWh/d/y at IP"; each operator sets its basis. `differs` (14 of 14 words) says "Simulated cost, kept as text; `N/A` when not sent; currency only, no capacity unit". `how_used[2]` now ends "with its cost remark".
- Source check: the note cites the ENTSOG TAR NC transparency workshop slides, December 2016, slide "TRA PF Standardised Table: contents" (`TAR0762_161208_TAR_NC_Transparency_for TRA_WS_Rev2.pdf`). I had retrieved that PDF in round 1 and re-read its text layer: the slide reads "Simulation of costs for flowing 1 GWh/d/y at IP (in local currency and euro)". The vault note quotes it verbatim, and the page's 7-word quote is an exact substring. The file name in the note matches the PDF I opened.
- The count "799 of 2,782" is not on the page and not in the note's `page:` block (grep of the rendered text and of both front matters for 799, 816, 827, 2,782, 12,244, 61,220, 13,910, 902: no hits; the only "913" on the page is the RON count in the notebook's currency output, which the rubric allows). It stays in the note body (Known issues), which is correct under the numbers rule.

**2. Euro price in the folded frame at 1440: fixed.** Column 7 is `applicable_tariff_per_eurk_wh_h_value`, showing 3.63709, 1.222898, 0.588397, 0.02847, 8.76, 2.6496, 1.116, 0.0504 beside `product_type` (my screenshot `r2_frame.png`, unfolded view not needed). The unit column folds behind `…`; the guide gives it (`Euro/(kWh/h)/y`), so the folded view shows the value with its product but not its unit. I do not rate that, since the product beside it names the unit's period. The price is in view as asked.

**3. National Gas TSO omission stated, with a notebook cell: fixed.**
- Caption: "National Gas TSO excluded: its Moffat exit price, 0.008326, is labelled both yearly and monthly." Verified against silver (Moffat exit firm, yearly and monthly, 0.008326 euro per kWh/h under `Euro/(kWh/h)/y` and `/m`).
- `how_used[0]` no longer invites an all-operator comparison ("the pipeline operators at Bacton and Zeebrugge").
- New read-only notebook cell 5 filters `uk-tso-0001itp-00090exit` (Moffat exit, National Gas TSO), firm, yearly and monthly, and its recorded output is `Monthly 0.008326 Euro/(kWh/h)/m` and `Yearly 0.008326 Euro/(kWh/h)/y`. Notebook JSON is from `run_notebooks.py`, 6 cells, no error outputs; the plot is `tariffs-6.png` (exists) and `plot_alt` matches it.

**4. Transgaz claim corrected: fixed.**
- Vault `tariffs.md` Known issues now reads that Transgaz's common figure is 24 times its euro kWh/h price on its yearly records, ratio 23.99996 to 23.99998, none of its 902 prices zero. I re-derived this in round 1 (913 records, 902 priced, 0 zero, ratio 23.999965 to 23.999979).
- Round-1 report lines (analysis and Defects) corrected in `tariffs-and-simulations-author.md`; the round-2 Defects list gives "× 24 for Transgaz".
- Other items on that bullet unchanged and still right (406 at ÷365, Fluxys Belgium 26 plus 1 bayernets at ÷8,760).

## The six nits

| Nit | Result |
|---|---|
| 5. `N/A` becomes null | Fixed. `raw_feed.note` says "Silver turns `N/A` prices into nulls ..."; euro price guide line ends "null when `N/A`"; vault says 827 = 816 sent as `N/A` and cast to null (`generic.py:189-191`, `cast(pl.Float64, strict=False)`: checked, those are the lines) plus 11 evergreen Transgaz records sent as null. Re-counted from bronze 2026-08-01: 816 records have all five prices `"N/A"`, 11 have all five null, no record has `N/A` in fewer than all five. |
| 6. `plot_alt` | Fixed: "between 1.008 and 1.116 from October to March, then between 1.44 and 1.488 from April". Matches silver (Oct 1.116, Nov 1.08, Dec 1.116, Jan 1.116, Feb 1.008, Mar 1.116; Apr to Sep 1.44 to 1.488). |
| 7. `IZT`, `IUK` | Fixed as far as verifiable: "ENTSOG's point Zeebrugge IZT"; "Operator Interconnector, whose zone ENTSOG labels `IUK`" (both strings are the point name and balancing-zone value in silver). The writer rightly did not add an unverified expansion. |
| 8. Who converts the GBP | Fixed: no "ENTSOG converts" anywhere; the notes say "euro column 3.63709". |
| 9. Bar value labels rounded | Declined as template behaviour, already listed to the seat; the series JSON is right (19.32, 8.76 x 2, 8.112, 3.637 x 4). Accepted. |
| 10. Notebook window | Fixed: lead ends "widen them for later periods"; 35 of 35 words per the build. |

## New nits

**1. [nit] `page.chart_view.caption`: "fetched 1 to 5 August 2026".** Round 1 said "requested for 1 to 5 August 2026", and `chart_view.alt` still does. "Fetched" reads closer to a statement about our own holdings (rubric 3) than "requested", and the two fields now disagree. Revert to "requested for" (same word count) or drop the dates.

**2. [nit] Vault `tariff_simulations.md` Overview, "(cited by the 2026-10-07 page review; not retrieved by the writer)".** This is process wording inside a canonical note, and it is now out of date: the quote has been checked against the slide text. Replace with the plain source and "checked against the slide text, 2026-10-07". The Regulation (EU) 2017/460 text itself is still not retrieved by anyone; the note should not claim more than the slide.

## Defects

No new defects. The round-2 Defects list is accurate and pasteable. One addition for the seat: the new Defects line for the ENTSOG definition should name the source file, `TAR0762_161208_TAR_NC_Transparency_for TRA_WS_Rev2.pdf`, as retrieved and checked.
