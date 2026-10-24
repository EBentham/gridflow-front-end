# Capacity Market Register: checker's review (round 1)

Page `capacity-market-register`, lead `capacity_market_auction_static`, 8 members. Front-end worktree `C:\gridflow-wt\fe-neso-emr`, vault worktree `C:\gridflow-wt\vault-neso-emr`.

**Verdict: REVISE.** 0 blockers, 1 major, 8 nits. The privacy check passes and the chart reproduces. The one major is wording on the summed awarded MW.

## What was checked and passes

- **Build and gates.** `gridflow-build --only neso_data_portal/capacity_market_auction_static` is clean. Detector `[]`. Em dashes, arrows and middle dots: 0. Mirror `cmp` identical. The vault diff against `origin/master` touches only this note.
- **Privacy (blocker class): clean.**
  - Built page, series, sample and notebook JSON: no `@` outside the Google Fonts URL, no phone-like digit run outside SVG coordinates, and no `email`, `telephone`, `applicant`, `post_code` or `secondary_trading` anywhere. The only `contact` hits are the two sentences saying the contact columns exist and are never shown (`what_it_is`, the unit_cmu `differs` line).
  - Frame, guide and chart read the lead only. The lead has no contact, name or postcode column.
  - The notebook cannot print them as written. Cell 2 is the generic method card. Cell 3 selects five named lead columns. Cell 4 selects `primary_fuel_type`, `COUNT(*)` and `SUM(auction_acquired_capacity_obligation)` from the CMU `_latest` view. Cell 5 selects auction name, delivery year and MW from the cost view. No `SELECT *`, no `describe`, `tail` or `query` on CMU or CMU history. The PNG is a plot of MW only.
- **Chart reproduced from silver.** Lead silver is 27 rows, 27 distinct names, one capture. The 24 non-null prices, sorted by `auction_name`, equal the committed series value for value (27.5, 6.95, 45, 6, 19.4, 0.77, 18, 1, 22.5, 45, 8.4, 75, 6.44, 60, 15.97, 35.79, 18, 20, 30.59, 5, 63, 65, 60, 27.1).
  - The three nulls are 2022-23 T-4, 2027-28 T-1 and 2030-31 T-4.
  - Every number in `chart_view.alt` is right: 75, 65 and 63 highest; 0.77 and 1 lowest; T-4 from 8.4 to 65; 2029-30 T-4 at 27.1.
  - Unit "£ per kW per year" matches the CSV heading. NESO's dictionary says `£` with the comment `£kW/year`. File date 9 September 2026 equals `published_at` 2026-09-09 11:51 UTC.
- **Captures.** All eight match the writer's table and the note's new **Captures** paragraph.
  - Three auction-level tables: 1 capture, `published_at` 2026-09-09.
  - Pre-aggregation history: 1 capture, 1,918,503 rows, change dates 2025-12-10 to 2026-07-15.
  - Weekly tables: 2 captures (written 2026-10-08 and 2026-10-16; `last_modified` 10-07 and 10-14):
    - CMU 18,200 and 18,200 rows, 18,185 identical;
    - CMU History 72,166 and 72,282, all of the first recur;
    - Components 29,849 and 29,849, 29,803 identical;
    - Component History 7,460 and 7,488, all of the first recur.
  - The chart and frame read only the lead, so `dedup` is a guard there. The notebook reads `_latest` views, so the repeats do not reach it. The 2029-30 T-4 notebook output (691 units, 40,108.608 MW) equals one capture and the lead's awarded volume.
- **Rows.**
  - Lead: one row per auction.
  - Cost: unique on (auction, delivery year), 192 rows. `forecast_cost_gbp` = MW x price x 1000, max difference 0.26 (rounding). NESO's dictionary says "Capacity Awarded * Clearing Price".
  - CMU: unique on (auction, application_id), 18,200.
  - Components: unique on (auction, application, component), 29,849.
  - De-rating: unique on (auction, technology class), 890.
  - Component History starts 2026-07-29, as the page says.
- **Claims scoped "here".**
  - Fee 6 non-null only for 2027-28 T-1 and 2030-31 T-4: true in the rows and in all 27 silver rows.
  - Annual cap `100%` (and monthly `200%`): the only values in silver.
  - Base period `Winter 2012/2013` to `Winter 2024/2025`: true.
  - Dictionary text for "rounded to 3 decimal places" and "Electricity Capacity Report": quoted correctly.
- **Raw feed.** All eight resource ids, the package id and the file names match the registry and the bronze sidecars. `last_modified` skip is `client.py` ~1752-1766. "Weekly" is the vendor's stated update frequency. Commands use the same form as the approved EAC/BR page.
- **Related.**
  - All four slugs resolve, and each note is 12 words or fewer.
  - The TEC deferral column, the `transmission_or_distribution` column and interconnector units by link exist in the CMU table.
  - The embedded register is described as Scottish.
- **Body corrections.** The `casting.py:605` citation is right. The Base period, Captures and Cadence edits are right. Contact values counts agree with silver (3,108 + 721 + 2,683 + 184 in the newest capture; 13,386 across both).
- **Layout.** At 390 px in the browser pane `scrollWidth` is 390 and no element sits outside the viewport except inside scroll containers. I looked at the hero, bar chart and legend, frame (about 800 px wide) and the notebook header and cells. I did not review 768 or dark. Headless Chrome renders nothing below the raw-feed heading (scroll reveal), so the notebook plot was reviewed from its PNG: the legend and axes are intact, and the 2016/2017 TR bar is a sliver.

## Findings

1. **major. `page.how_used[1]` and `page.notebook.plot_alt`: awarded MW added across auctions per delivery year.**
   - Wording: "Capacity contracted per delivery year, summed across auctions from the cost table", and "Years 2017/2018 to 2029/2030 hold 54,746 to 62,325 MW".
   - Both read as a contracted total per year. NESO's dictionary describes `Capacity Awarded` only as "(MW) by Auction and Delivery Year", and no source says the sum is a valid per-year total. The figures are the Polars sum I reproduced, for example 2017/2018 = 54,745.805 and 2026/2027 = 62,324.708.
   - Fix: word it as our sum, for example "our sum of NESO's per-auction MW awarded for each delivery year; NESO publishes no per-year total". Change "hold" in the alt to "sum to", or cut the bullet and keep only the stacked plot.
2. **nit. `page.chart_view.caption`.** "Three auctions with no price are not drawn" does not say which. Name them (2022-23 T-4, 2027-28 T-1, 2030-31 T-4). Two show as `null` in the frame; the third appears only as `NaN` in the notebook output.
3. **nit. `page.record.fields.base_period_for_the_agreement`.** "null on the T-1 rows here" is true but incomplete. In the eight rows the 2030-31 T-4 base period is also null, and in silver every TR row is too. Suggest "null on T-1 and TR auctions and on 2030-31 T-4".
4. **nit. `page.notebook.plot_alt`.** The plot starts at 2016/2017 (803 MW, TR only) but the alt begins at 2017/2018. Say so, or start the range at 2016/2017.
5. **nit. `page.related[3].note`.** "the adequacy measured short run" is not plain English. For example: "Elexon's de-rated margin per settlement period, a short-run adequacy measure".
6. **nit. Note body, stale after the second capture.**
   - Line ~1022: "One capture cannot establish it" is now wrong for the four weekly files.
   - The per-family "Silver output" lines for CMU, CMU History, Components and Component History (18,200 / 72,166 / 29,849 / 7,460) describe only the first capture.
   - The Component History change-date span "2026-07-29 .. 2026-10-07" (lines ~512 and 574) is the first capture's.
7. **nit. Note body, CMU History "Contact values".** The paragraph names only the email and telephone attributes. The same logs also carry `Name of Applicant`, `Agent Name`, `Registered Holder`, `Parent Company` and `Legal Name of any Person with a Security Interest`, and Components holds `location_and_post_code` and `os_grid_reference`. Name these, since a sole trader's name or site address is personal. The page never shows them.
8. **nit. Note body, `casting.py:619`.** Line 619 is the `else:`; the `date_sp1` logic is at 620-624. Cite 620.
9. **nit. Page, bar labels (seat item, template).** Labels round to 2 significant figures: 27.50 reads 28, 22.50 reads 22, 6.95 reads 7.0, 0.77 reads 0.8. The alt has the exact values.

## Not checked

- Dark mode and 768 px.
- The 1440 px sections below the chart (headless blank; checked in the pane at about 800 px and 390 px).
- Why 2022-23 T-4, 2027-28 T-1 and 2030-31 T-4 carry no price. The page states no cause, which is right.
