# neso/regional-carbon-intensity: review

Checker: Sonnet 5.5 (high), 2026-10-06. Family lead `regional_intensity`, 18 members. Rubric: `.planning/v5/review-rubric.md`.

## Verdict: REVISE

2 majors, 5 nits, 0 blockers. Facts, chart provenance, commands, the one-day transform, cross-member agreement and the `postcode` claim all reproduce. The two majors are one overreaching key note and one notebook plot where the legend covers data. Both are small edits.

## Findings

1. **major** `page.chart_view.key[gb].note` ("GB as a whole; checked by the project, it is not the national route's `forecast`.")
   - **What is wrong:** it is a categorical negative measured on the project's own copy. It carries no window or figures, and the reader cannot tell what GB is instead.
   - **Evidence** (silver `neso/regional_intensity` region 18 joined to `neso/carbon_intensity` on `timestamp_utc`, 674 shared half-hours, reproduced):

     | Comparison | Max difference | Mean difference | Exactly equal |
     |---|---|---|---|
     | GB against national `forecast` | 173 | 9.23 | 44 half-hours |
     | GB against national `actual` | 17 | 3.85 | 49 half-hours |

   - In 44 half-hours GB equals the national forecast exactly. The real observation is that GB sat nearer the national `actual` than the national `forecast`.
   - The big gaps are not a regional feature. 9 half-hours differ from the national forecast by more than 60, all at 19:30, 04:00 or 04:30 UTC (13 Sep 19:30: GB 209, national forecast 139, national actual 199). The author's defect list says 8, using the national actual minus the national forecast; same cluster. In every one of them GB is within 10 of the national actual. The page implies the oddity sits in GB.
   - The lead note's Known issues bullet is correctly scoped and numeric. The page note is not.
   - **Fix:** word it as an observation and keep NESO's silence: "GB as a whole. In a project check it sat nearer the national route's `actual` than its `forecast`; NESO does not say how they relate." Or drop the note. Both are inside the key-note budget.
   - If the seat keeps the current wording, downgrade to nit: it is flagged as a project check, which is the precedent for sign conventions.

2. **major** `notebook.cells[3]` output image (`site/hifi/data/notebooks/neso/regional_intensity-6.png`)
   - **What is wrong:** the plot's default legend sits upper right and covers the South Wales line over about 19 to 20 September. That includes the 80 to 98.9 stretch that `notebook.plot_alt` cites as the peak. Rubric 5: nothing overlapping.
   - **Evidence:** I zoomed the PNG. The legend box (about x 525 to 690, y 15 to 130 of 699 by 369) overlays orange line segments.
   - **Fix:** put the legend outside or on one row, for example `.legend(loc="upper center", ncol=4)` above the axes or `bbox_to_anchor=(1, 0.5)`. Then re-run `scripts/run_notebooks.py`.

3. **nit** `page.chart` / template: the North Scotland series is flat at 0 and sits exactly under the x axis line. In screenshots at 1440, 1024, 768 and 390 only three lines are visible, while the key lists four.
   - The key note ("At 0 gCO2/kWh for every half-hour shown.") discloses it, and 336 of 336 values are 0 (recomputed), so the page is not wrong.
   - A template problem (axis drawn over a zero line). Report it to the seat; do not work around it on the page.

4. **nit** `page.family.members[regional_intensity_fw24h|fw48h|pt24h].differs` ("for the 24 hours after `from`" and similar).
   - **Evidence:** bronze `fw24h` has 49 half-hours, `from` 2026-07-31T23:30Z to 2026-08-01T23:30Z, with `from=2026-08-01T00:00Z` in the request. `fw48h` has 97. `pt24h` has 49, 30 Jul 23:30 to 31 Jul 23:30.
   - So the first `fw` half-hour ends at `from` (it lies before it), consistent with the lead's `raw_feed.note`. "24 hours after" reads as 48 half-hours starting at `from`.
   - **Fix:** for example "Every region: 49 half-hours, the first ending at `from`" (9 words). Or leave it as the vendor's own "forward 24 hours" naming and accept the nit.

5. **nit** `page.chart_view.caption` / `page.raw_feed.note`: no statement of whether a past half-hour's `forecast` is the original or a revised one.
   - **Evidence:** the 14 to 20 September window was fetched on 26 September (sidecar `fetched_at` 2026-09-26T17:43:40Z), and GB tracks the national `actual` (finding 1). The writer lists forecast vintage as unverified in the report, but the page is silent.
   - **Fix:** the accurate hedge, if wanted: "NESO does not say whether a finished half-hour's forecast is revised." No local dates needed.

6. **nit** `page.family.members[regional_intensity_postcode].differs`: silver `dnoregion` is `""` for this member only. The body note says so, but the page and the `dnoregion` guide line ("Distribution network operator's name") do not.
   - **Evidence:** silver `regional_intensity_postcode` has `dnoregion ['']` on all 2,169 rows. The Aug bronze body has no `dnoregion` on the region object.
   - Mention it only if the budget allows (the current line is 13 words); otherwise skip.

7. **nit** vault body, lead note and `regional_intensity_postcode.md`. Two small things:
   - The lead's Silver schema row `actual_gco2_kwh` still says "Not present in many official examples; nullable", while Known issues now says regional responses carry no `actual`.
   - `regional_intensity_postcode.md` says "the sample below is older", which is unclear.

## What I checked and found correct

**Chart (rubric 1 and 2)**
- Recomputed from silver `neso/regional_intensity`, deduped on `timestamp_utc, regionid`. Per (half-hour, region), `n_unique(forecast)` and `n_unique(index)` are both 1, with 9 fuel rows each.
- 4 series of 336 points. The committed series equals my recompute exactly for all four (`list ==`). Window 14 Sep 00:00 to 20 Sep 23:30 UTC. `spec_origin: vault`, the build digest check passes, and no staged chart spec or authored override exists.
- Min and max per series:

  | Series | Min | Max |
  |---|---|---|
  | South Wales | 6 (20 Sep 14:30) | 390 (20 Sep 22:00) |
  | London | 39 (17 Sep 12:00) | 246 (14 Sep 03:00) |
  | GB | 30 (15 Sep 11:00) | 197 (14 Sep 00:00) |
  | North Scotland | 0 | 0 |

- Alt text:
  - South Wales is below London in 14 half-hours (15 Sep 11:30 to 13:30, 20 Sep 10:00 to 15:00). It also ties London once, and sits below GB in 4 half-hours. It is the highest of the four in 322 of 336, so "highest except around midday on the 15th and 20th" holds.
  - Daily maxima 17 to 19 September: London 131, 116, 144 and GB 95, 83, 95, so "both stay under 150" is true.
- Unit: gCO2/kWh comes from the code column names. The vendor docs state none in the vault, and the writer says so. This is the same basis as the national page; acceptable.

**No `actual` in regional responses**
- Bronze: all 19 regional bodies (18 datasets, 2 files for `regional_intensity`) contain no `"actual"` key (grep).
- Silver: `actual_gco2_kwh` is null on all 109,188 rows, and null on every row of all 18 members.
- The page says "NESO's regional examples carry `forecast` and `index`, no `actual`" and "null here, as these regional responses carry none". Both are scoped, and nothing implies an `actual`.
- The connector reads `intensity.get("actual")` (`silver/neso/carbon_intensity.py:~440`), so the null is genuine.

**Window, commands and one-day transform**
- Connector: `data_date=window_start.date()` (`connectors/neso/carbon_intensity.py:79`). `_request_specs` chunks at 14 days. The `from_dt` and `to_dt` format is `%Y-%m-%dT%H:%MZ`. A bare date is midnight UTC (`runner._parse_window_bound`).
- `ingest neso regional_intensity --start 2026-09-13 --end 2026-09-22` gives request `.../2026-09-13T00:00Z/2026-09-22T00:00Z`, which is exactly the sidecar `request_url`.
- `silver/neso/carbon_intensity.py:87-154`: exact-partition read only. `transform --start 2026-09-13 --end 2026-09-13` reads `bronze/neso/regional_intensity/2026/09/13` and writes `regional_intensity_20260913.parquet`. That file holds 433 half-hours, 12 Sep 23:30 to 21 Sep 23:30, so the command works as written.
- `raw_feed.note` ("first half-hour ends at `from`, the last at `to`") matches both bronze bodies, scoped "in these responses".
- `gridflow_models` `query()` end is inclusive (`source.py:389`, `+ timedelta(days=1)`), so the lead and `needs` ("13 to 21 September") are consistent.

**Members agree exactly (a stronger test than the three pairs asked for)**
- Joined on (half-hour, region, fuel), comparing `forecast_gco2_kwh`, `intensity_index` and `generation_percentage`. Zero mismatches in:
  - `fw24h` against lead (7,938 cells), `fw48h` against lead (15,714), `fw24h` against `fw48h` (7,938);
  - `postcode` against lead (2,169), `regionid` against lead (2,169);
  - the other `fw*` and `pt24h*` postcode and regionid members against the lead (441, 873, 9);
  - `regional_england`, `regional_scotland`, `regional_wales`, `regional_postcode` and `regional_regionid` against `regional_current` (9 each).
- The window members were all fetched on 16 Aug within about 2 minutes, so this is agreement between routes, not stability over time. The page makes no such claim.

**Thin members and `postcode`**
- The snapshot members (`regional_current`, `regional_england`, `regional_scotland`, `regional_wales`, `regional_postcode`, `regional_regionid`) are one half-hour each (27 Sep 00:00 UTC), fetched 00:33 to 00:34 UTC. The `differs` lines say "one half-hour" or "the half-hour NESO serves as current". That is accurate, and no trend is claimed.
- `postcode` is `""` (not null) on every non-postcode member: 0 null and 109,188 empty on the lead (`silver/neso/carbon_intensity.py:610-614`). The postcode members hold `RG10`, `regionid` 12.
- Region labels: ids 1 to 14 are DNO areas, 15 England, 16 Scotland, 17 Wales, 18 GB (silver distinct), and the percent sums run 99.7 to 100.2.

**Plot alt and eight rows**
- `plot_alt` numbers recomputed: gas share South Wales 1.3 (20 Sep 14:30) to 98.9 (20 Sep 22:00), London 4.8 to 59.7, GB 4.2 to 44.8, North Scotland 0.
- Eight rows: real `gridflow-sample`, all five bands, nations and GB. The unfolded frame (`#fx` checked) shows `ingested_at` 2026-09-26, `event_time` equal to `timestamp_utc`, `postcode ""`, and `dnoregion` "England", "Wales" and "GB" for the nation and GB rows. The guide covers every non-pipeline column, key columns first.
- Notebook JSON is from `run_notebooks.py`. Every cell is read-only with no errors. The by-region means in cell 4 match my recompute (North Scotland 0.0, South Wales 246.8 rounded to 247).

**Structure, leakage and layout**
- `gridflow-build --only neso/regional_intensity` succeeded here. `detect.mjs --json` returns `[]`.
- Grep of the rendered page text: no `locally`, `held`, `our`, `since 20`, `% of`, live, now, yet, soon, planned or coming. 0 em dashes, 0 arrows, 0 middle dots. Related notes are 10 words or fewer.
- Screenshots at 1440, 1024, 768 and a true 390 px iframe, plus an unfolded copy at 1440 and 390. The site has no dark theme (seat note). Nothing is clipped or overlapping on the page: the 18 member chips wrap cleanly, long URLs wrap in their boxes, the scenery tops are intact, and every stratum corner label is visible. The only overlap is the notebook plot legend (finding 2).

**Vault body edits**
- All 18 mirrors under `vault/neso/` are `cmp`-equal to the canonical notes, and all notes are CRLF. Diffs against `origin/master` on ten members (current, postcode, `fw24h_postcode`, `fw48h_regionid`, england, scotland, wales, `pt24h` and others) are exactly the schema `postcode` row, the silver sample and the `actual` known-issue line. Each fixes the smallest span and cites `file:line`. The lead's two extra bullets are scoped and numeric.

## Defects (confirming the writer's list; paste as is)

- The three writer defects reproduce: vault README stale V1 latent-bug note; `schemas/neso.py:68-74` comment says `postcode` is null but the transformer writes `""`; `regional_intensity_postcode` omits `dnoregion` (a vendor shape, so silver holds `""`).
- Correction to the writer's national-forecast anomaly: it is 9 half-hours, not 8, where national `forecast` is more than 60 from regional GB. All fall at 19:30, 04:00 or 04:30 UTC. Regional GB is within 10 of the national `actual` at every one of them. 13 Sep 19:30: GB 209, national forecast 139, national actual 199. Whether the oddity is in the vendor's national forecast or in gridflow's national silver is unverified.
