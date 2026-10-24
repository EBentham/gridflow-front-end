# Capacity Market Register: writer's report (round 2)

These fixes answer `capacity-market-register-review.md` (REVISE: one major, eight nits) and the seat's three rulings.

**Gates:** `gridflow-build --only neso_data_portal/capacity_market_auction_static` is clean. The detector returns
`[]` and the page has no em dashes. The mirror `cmp`s identical and the note is still CRLF. The notebook was re-run
by `scripts/run_notebooks.py`, because the plot's y label changed; it gave 5 cells, one image and no errors.

## Fixes

1. **Major, summed awarded MW (ruling 1).** The page now calls it our sum and says NESO gives no total.
   - `how_used[1]` now reads "Our sum of NESO's per-auction MW awarded per delivery year; NESO gives no total".
   - `plot_alt` now reads "our sum, per delivery year, of NESO's MW awarded by every auction, split by auction type;
     NESO gives no per-year total". "Hold" is replaced by "sums to".
   - The notebook plot's y label now reads "MW awarded, summed over auctions".
2. **Caption (ruling 2).** It names the three unpriced auctions: "No price, so not drawn: 2022-23 T-4, 2027-28 T-1,
   2030-31 T-4." The caption is 39 words.
3. **`record.fields.base_period_for_the_agreement`.** It now reads "Base period for calculating capacity payments
   (NESO); null here on T-1 and 2030-31 T-4".
   - "Here" scopes it to the eight rows shown.
   - I did not take the checker's "every TR" wording, because it would add a claim about rows the page does not show.
4. **`plot_alt` start.** It now begins at 2016/2017: "sums to 803 MW (TR only)".
5. **`related[3].note`.** It now reads "Elexon's de-rated margin per settlement period, a short-run adequacy
   measure".
6. **Body, stale after the second capture:**
   - Cadence TODO: "Two weekly captures cannot establish it."
   - Silver output lines for CMU, CMU History, Components and Component History now add the 2026-10-16 capture: its
     file, rows (18,200 / 72,282 / 29,849 / 7,488) and bytes (from the sidecars).
   - Component History change-date span: the first-capture span is kept and marked as such, and the second capture's
     is added (to 2026-10-14, 12 distinct dates). This is in both the clock paragraph and the CI-3 table.
   - CMU History: the second capture's span runs to 2026-10-14, with 49 distinct dates.
7. **Body, personal data.** The CMU History "Contact values" paragraph now also names:
   - `Name of Applicant`, `Agent Name`, `Registered Holder`, `Parent Company` and `Legal Name of any Person with a
     Security Interest`, because a name can be a sole trader's;
   - `Location and Post Code` and `OS Grid Reference`, in the component logs and in Components.
8. **Body citation.** `casting.py:619` is now `casting.py:620`, the `date_sp1` line.
9. **Bar labels rounding to two significant figures.** Not changed: it is a template item for the seat, as in round 1.

## The 1440 blank (ruling 3)

- **The built HTML has every section.** Each of these appears once:
  - "The raw feed", "Schema and sample rows", "Query it from a notebook" and "Related datasets";
  - the notebook image `capacity_market_auction_static-5.png`;
  - the new caption text.
- **It is a headless capture effect, not a page fault.** Round 1's 1440 capture stopped at 2,259 px. Re-run with the
  same flags (`--headless=new`, `--timeout=15000`, `--virtual-time-budget=5000`, window 1440×9000, port 9901), the
  page captured to 6,099 px. Every section showed, from the raw feed through Related datasets, with nothing clipped.
  So the blank is intermittent at the same settings.
- **Other pages: not established.** I tried the interconnector register and EAC results pages for comparison, but
  this worktree builds only this page with `--only`, and generated HTML is gitignored, so both returned 404. I cannot
  say from my own run whether other pages show the blank. The checker saw it too on this page. `site.js:279` uses an
  `IntersectionObserver`, which is a plausible cause of a capture that depends on timing, but I have not verified it.
- I started the server with its PID recorded and stopped only that PID.

## Unchanged

The chart, frame, sample and series artefacts did not change: the chart spec and record select were untouched.
