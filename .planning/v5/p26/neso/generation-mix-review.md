# Review: `neso/generation-mix` (members `generation`, `generation_current`, `generation_pt24h`)

Checker: Sonnet 5.5 (high), 2026-10-06. Screenshot port 9891 (static server, stopped afterwards; 9670 untouched).
Answers `generation-mix-author.md`.

## Verdict: REVISE

0 blockers, 2 majors, 9 nits. The facts, the chart, the artefacts and the build are sound and almost everything in the
writer's evidence table reproduces. The two majors are about what the page over-says on two of the three
things the seat asked me to press on: the scope of the stamp offset (solar is not placed) and `imports`. Both are one-line fixes in the note.

## What I reproduced (no finding)

- **Build and detector.** `gridflow-build --only neso/generation` succeeds; `detect.mjs --json` on
  `site/hifi/data-sources/neso/generation-mix.html` returns `[]`. Em dashes, arrows, middle dots, en dashes on the page: 0.
  No staged chart spec and no authored override exist for these datasets. Series `spec_origin: vault`, sample
  `generated_by: gridflow-sample`, notebook `generated_by: scripts/run_notebooks.py`, 6 cells, no error output.
- **Mirrors.** `cmp` of the three canonical notes against `vault/neso/{generation,generation_current,generation_pt24h}.md`:
  all byte-equal. The vault diff against `origin/master` is the `page:` block on `generation.md` plus Known-issues and one
  Silver-path edit; the other two notes carry body edits only, no `page:` block. No wholesale rewrite; no curl example touched.
- **The chart (item 1).** Recomputed from silver `C:\gridflow-data\silver\neso\generation\` (6,066 rows, two files) for
  14 to 20 Sep UTC: 336 half-hours x 9 fuels = 3,024 rows, no duplicate `(timestamp_utc, fuel)`, no null, every value has
  one decimal. Stack sums min 99.8, max 100.2, every half-hour has all nine fuels. Per-fuel min/max match the committed
  series and the alt text exactly: nuclear 8.8 to 15.5, gas 4.2 to 44.8, imports 0 to 22.4, wind 15.7 to 72.8, coal 0
  throughout, solar peak 32.3 at 2026-09-20 13:00 UTC. Series order bottom to top matches `series_order` and the key
  (top first). Notebook cell output (count 336, min 99.8, max 100.2) and `generation-6.png` agree with `plot_alt`
  (wind largest in 287 of 336 half-hours; gas 44.8 at 00:00 on the 14th).
- **Request and commands.** URL shapes match `endpoints.py:135-154` and `build_path`; bronze sidecars confirm
  `generation/2026-09-13T00:00Z/2026-09-22T00:00Z` returned `from` 2026-09-12T23:30Z to 2026-09-21T23:30Z (433 periods),
  `generation_pt24h` for `from` 2026-08-01T00:00Z returned 49 periods from 2026-07-30T23:30Z. Ingest `--end` is an
  exclusive instant, one 7-day call, bronze filed under the window start (`carbon_intensity.py:79`), transform reads that
  one partition; the 14 to 21 Sep ingest yields `from` 13 Sep 23:30 to 20 Sep 23:30, which covers the chart window.
  `_transform_generation` keeps `from`, `to`, `fuel`, `perc`; `period_end_utc` minus `timestamp_utc` is 30 minutes on all rows.
- **Stamp offset (item 2), reproduced.** Differenced-correlation at lags -60/-30/0/+30/+60 minutes (CI row at T against the
  other series at T+lag), `generation` silver, both blocks together (n = 672):
  - vs Data Portal `gas_pct` 0.35/0.52/0.69/**0.98**/0.68; `wind_pct` 0.38/0.47/0.62/**0.92**/0.63;
    `imports_pct` 0.02/0.40/0.10/**0.94**/0.10; `biomass_pct` 0.18/0.32/0.60/**0.96**/0.59; `nuclear_pct` 0.87 at +30 against 0.57 at 0.
  - vs `elexon/fuelhh` (latest `published_at` per key; gas = CCGT+OCGT) gas 0.30/0.46/0.67/**0.93**/0.66; WIND 0.75 at +30
    against 0.46 at 0; BIOMASS 0.88 against 0.50.
  - Control, portal gas MW against fuelhh gas MW: 0.56/0.75/**1.00**/0.75/0.56.
  - Holds in each block separately (31 Jul to 5 Aug: gas 0.99 vs 0.74; 12 to 21 Sep: 0.98 vs 0.66) and for `generation_pt24h`
    (49 periods, n = 48): gas vs fuelhh 0.94 at +30 against 0.76; wind 0.80 against 0.33; biomass 0.89 against 0.16; imports vs
    portal 0.93 against 0.05. fuelhh `timestamp_utc` is the period start (settlement 20 Sep period 1 = 2026-09-19 23:00Z).
  - Wording: the caption says "(a project check)", `what_it_is` and the guide say "(checked)"; the claim is attributed to
    the project, not to NESO. The body says "NESO does not explain the labelling". That meets the brief. See nit 4.
  - `generation_current` is one row set, so it cannot be lag-tested; the page says nothing about it beyond the shared table claim.
- **Composition (item 3), reproduced** at the +30 alignment against portal `historic_generation_mix` (latest capture, 674 joined
  half-hours), CI share minus the portal figure, in points:
  - `wind` against (`wind` + `wind_emb`) / `generation`: MAE 1.16, mean +0.87 (against `wind` alone: MAE 7.51, mean +7.51).
  - `hydro` against (`hydro` + `storage`) / `generation`: MAE 0.07, p95 0.22, max 0.39 (against `hydro` alone: MAE 0.51).
  - `imports` against portal `imports_pct`: MAE 1.88, mean -1.86, p95 4.40 (portal `imports` equals fuelhh's per-link imports summed:
    MAE 9.9 MW, against 2,067 MW for the net). So the page agrees with the approved portal page on `wind`, `hydro`/`storage`
    and on "not net". Net-export half-hours in fuelhh: 213 of 674 (31.6%), as the writer says. See finding 2.
- **Fuel list and denominator.** Nine lowercase fuel names as in `endpoints.md:79` and the bronze bodies. Nothing quoted in the
  vault, `endpoints.md` or the methodology receipt defines the denominator (the receipt divides the intensity estimate by
  national demand and says nothing of `perc`). The page's "undocumented" matches what the notes quote; see nit 7.
- **Same stamps as `carbon_intensity`.** Silver `neso/carbon_intensity` has exactly the same 674 `timestamp_utc` values with
  30-minute periods; the gas share lines up with `actual_gco2_kwh` at zero lag (0.88 against 0.61/0.67 at -30/+30), as claimed.
- **Members.** `generation_current` is `/generation`, no inputs (one capture, `from` 2026-09-27T00:00Z, nine fuels summing
  to 99.9). `generation_pt24h` is the 24 hours before the ingest start sent as `from` (code `endpoints.py:141-147`, chunk
  branch `carbon_intensity.py:149-161`); on its one shared half-hour (`from` 2026-07-31T23:30Z) all nine values are
  identical to `generation`. Body corrections are evidence-cited and small (two copied intensity bullets replaced, silver
  file-date explained, measurements appended).
- **Look.** Screenshots at 1440, 1024, 768 and a true 390 px iframe: hero scenery, chart (stack, tags, key), raw feed, frame,
  guide, notebook panel, related list; nothing clipped or overlapping. Opened the unfolded frame (it scrolls inside its own
  box) and the notebook drawer in the browser pane. Series tags are hidden at 390 and the key carries the reading, as the
  writer says. There is no dark theme (not a finding), and the percent axis running past 100 is the seat's (not a finding).

## Findings

### 1. major: `page.what_it_is`, `page.related[1].note`: the offset is stated for "the stamps" as a whole, but it was placed for four of nine fuels and `solar` does not follow it

`what_it_is` says "the stamps sit 30 minutes before the metered half-hour they match (checked)" and the fuelhh related note
says it "tracks these shares 30 minutes later", with no fuel scope. (The caption and the `timestamp_utc` guide line do say
"metered fuels".) The lag test placed gas, wind, imports and biomass (and `other` and nuclear against the portal); it did not
place `solar`, which the page draws on top and lists in `how_used[1]` as a use, nor `hydro` (portal 0.47 at +30 against 0.10
at 0) nor `coal` (zero throughout). Stated as a property of the stamps, that is an unscoped universal (rubric 1).
`solar` in fact does not shift with the metered fuels. Level fit against the portal's `solar_pct` (same data as the +30
test), MAE in points by lag in minutes: -30: 1.50, -15: 1.12, **0: 1.01**, +15: 1.13, +30: 1.51 (gas on the same scale:
0: 1.26, +15: 0.85, **+30: 0.69**). Differenced correlation is also best at zero (0.94 against 0.91 at +/-30). The sunrise
and sunset edges are wider than the portal's on both sides (19 and 20 Sep the first non-zero half-hour is 05:30 in the mix
against 06:00 in the portal, the last 18:30 against 17:30), which a plain +30 shift would not produce. What this does not
show is that the mix's solar is right or wrong: the portal's `solar` was never anchored to a metered source either. The
writer's report says the test "cannot place" solar and notes the zero-lag fit under "Not verified", but the page carries
neither. A reader who shifts the whole table by 30 minutes, as the page invites, would move `solar` the wrong way relative to
the portal.
Fix (smallest, safe): scope `what_it_is` and the related note to the fuels the check placed ("gas, wind, imports and
biomass line up 30 minutes later (checked)") and say in the `solar` key note that the lag test cannot place `solar`, whose
level fits the Data Portal's `solar` at zero lag, not +30 minutes. Same sentence for the vault note's Known-issues offset bullet.

### 2. major: `page.chart_view.key[imports].note` (and the matching vault body bullet): "above zero while fuelhh shows GB exporting" is not true of every such half-hour, and the page leaves the gap to the portal's gross `imports` unsaid

The key note reads "Not a net figure: above zero while fuelhh shows GB exporting (checked)". "Not net" reproduces, but the
evidence sentence over-reads. At the +30 alignment, fuelhh's interconnectors net to export in 213 of 674 half-hours; the
mix's `imports` is **0.0 in 42 of those 213** (a fifth), and in all 42 fuelhh's per-link imports are positive (2 to
1,250 MW, median 364 MW, mean 474 MW, about 1.6 points of the mix on average, so rounding does not explain a zero). Across all half-hours
the mix's `imports` MW (share x portal `generation`) is 0.86 of the per-link gross on median and sits 1.9 points below the
portal's `imports_pct` (MAE 1.88, mean -1.86, p95 4.4, max 5.7), with almost no response to exports (regression
coefficient on exports -0.065 on 674 half-hours). So the figure is neither net nor the portal's gross; the page lets the
reader assume it is gross like the portal's `imports`, which the approved portal page defines as "each link's imports
summed". The brief asks the page to say plainly how this feed differs from that page; for `imports` it does not. The vault
body has the same shape ("above zero in half-hours when fuelhh's interconnectors net to export (31% of these
half-hours)"; it does give the 1.9-point gap, but the page does not).
Fix: "Not net of exports, but about 1.9 points below the Data Portal's per-link total, and 0.0 in some half-hours where
fuelhh shows imports (checked)", or drop the "above zero" clause and keep the gap. Same edit in the body bullet.

### 3. nit: `page.raw_feed.note`: "from" and "to" mean two things in one sentence

"Responses run from the half-hour ending at `from` to the one ending at `to`" uses the request's path segments, but the next
page section and the column guide use `from`/`to` for the row fields. Checked on bronze: a request `T0/T1` returns rows
with `from` T0-30 min through T1-30 min. Say "the request's `from`" and "the request's `to`" (or "a request for 14 to 21
September returns rows stamped 13 Sep 23:30 to 20 Sep 23:30").

### 4. nit: `page.chart_view.caption`, `page.related[1].note`, `page.chart_view.key[wind|hydro].note`: "match" is looser than the evidence, and "the metered fuels" is not named

The evidence is a correlation of half-hour changes (gas 0.93 to 0.98, wind 0.75 to 0.92, biomass 0.88 to 0.96, imports 0.94).
Nuclear, hydro and `other` are weaker or flat: nuclear against fuelhh NUCLEAR is 0.10 at +30 (the series is nearly constant;
against the portal it is 0.87), hydro against the portal 0.47 at +30 against 0.10 at 0. "Tracks" (used in the wind note) is
the honest verb; "match" in the caption and `timestamp_utc` guide line reads as equal values. Name the fuels the check
placed (gas, wind, imports, biomass) instead of "the metered fuels".

### 5. nit: `page.how_used[1]`: "A solar and embedded-wind share"

Embedded wind is not a share here; it is folded into `wind` and cannot be separated (the page says so elsewhere). Say "A
solar share, and a wind share that includes embedded wind, which transmission-metered fuelhh lacks".

### 6. nit: `page.notebook.needs`: backticks print literally

The page shows "with `generation` for 14 to 20 September 2026 ingested." with the backticks visible (the template does not
render markdown in `needs`; the fuelhh page has none). Drop the backticks, as `national-carbon-intensity` does.

### 7. nit: `page.what_it_is`, `generation_percentage` guide line, `other` key note, `fuel` guide line: "undocumented" rests on docs the writer did not read

The writer's own "Not verified" says `carbon-intensity.github.io/api-definitions` was not read; "undocumented" (denominator,
`other`) is true of what the vault quotes. I could not check the live docs (no live calls). The seat may accept it as is,
or word it "not defined in the NESO material we cite". Separately, the portal page (approved) documents that NESO counts
batteries and transmission-connected solar farms in its `other`; at +30 the mix's `other` tracks the portal's `other`
(MAE 0.43 points, mean +0.33; differenced correlation 0.78 at +30 against 0.08 at 0), so "what it holds is undocumented"
could point to that comparison.

### 8. nit: `page.record.caption`: "8 of its 9 fuels" does not say which is left out

The frame omits `other` (1.6 at that half-hour; the nine sum to 100.0, the eight shown to 98.4). Say "without `other`".

### 9. nit: cross-page, `page.related[2].note` and `page.how_used[2]` ("same API and stamps", "on the same stamps")

True as a key match (674 of 674 stamps equal). But the approved `neso/carbon_intensity` page calls its `timestamp_utc` the
"start of the half-hour" and its chart axis "each point is a half-hour's start", while this page says the same stamps sit
30 minutes before the metered half-hour. The two pages do not contradict each other (this one is about metered data), but
a reader of both gets two readings of one stamp. The portal's own `carbon_intensity` against the mix API's `actual` peaks at
+30 (0.42, weak), which fits an offset in the intensity routes too; the writer flagged this as open question 2. Seat's
ruling; no page edit needed unless the seat wants one sentence on the `carbon_intensity` page.

### 10. nit: vault body, `generation.md` Overview / schema table

The silver-schema table still says `timestamp_utc` is the "Half-hour period start" with no pointer to the Known-issues
offset; fine as a statement of NESO's label, but a one-clause pointer would save a reader the trip. Optional.

### 11. nit: `page.x_label` ("UTC day; times are NESO's from stamps")

"from stamps" is the row field name in prose; "times are NESO's period starts, not metered-half-hour starts" is clearer, or
drop the second clause (the caption already says it). Optional.

## Defects (pasteable; additions to the writer's list)

- **NESO generation mix: `solar` does not follow the +30 minute stamp offset (research unit, same unit as the writer's
  stamp-offset item).** Measured 2026-10-06 on silver 31 Jul to 5 Aug and 12 to 21 Sep 2026 against the NESO Data Portal
  `historic_generation_mix` latest capture: gas, wind, imports, biomass and `other` fit best at +30 minutes (gas MAE 0.69
  points against 1.26 at zero); `solar` fits best at zero lag (MAE 1.01 against 1.51 at +30) and is wider than the portal's
  solar on both the sunrise and sunset sides. The lag test cannot place `solar` itself, because the portal's `solar` was never
  anchored to a metered source. Named unknowns: whether NESO shifts only the metered inputs; whether the mix's solar is
  smoothed across two periods; where the portal's solar sits against the sun.
- **NESO generation mix: `imports` is neither net nor the portal's gross (research unit).** Measured on the same rows: 0.0 in
  42 of the 213 half-hours where fuelhh's interconnectors net to export (per-link imports 2 to 1,250 MW in those
  half-hours); on average 1.9 points below the portal's `imports_pct`; about 0.86 of fuelhh's summed per-link imports, with no
  response to exports. Named unknown: how NESO builds `imports` for this route.

## Not checked

- NESO's live API documentation (no live calls); the claims "undocumented" and "NESO does not explain the labelling" stand on
  the vault's quoted sources only.
- `generation_current` against any metered series (one capture).
