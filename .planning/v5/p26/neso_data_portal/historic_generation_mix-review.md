# Review: `neso_data_portal/historic_generation_mix`

Checker: Sonnet 5.5 (high), 2026-10-06. Screenshot port 9884 (static server, stopped afterwards).

## Verdict: REVISE

1 blocker, 3 majors, 11 nits (15 findings). The chart, the series, the eight rows, the requests and commands, the
notebook, the start-of-half-hour match against fuelhh and the zero-carbon counts all reproduce. The blocker is a false
vendor statement in the hero facts. The majors are things the page leaves out of the column guide and the use list while
the writer's own checks show them (imports as gross per link, storage inside two totals, structural breaks in the early
years).

Checks run:

- `gridflow-build --only neso_data_portal/historic_generation_mix`: succeeds. `detect.mjs --json`: `[]`.
- Em dashes, arrows and middle dots in the page: 0.
- Mirror `vault/neso_data_portal/historic_generation_mix.md` is byte-equal to the canonical note (`cmp`).
- No staged chart spec and no authored override. Series `spec_origin: vault`.
- Screenshots at 1440, 1024, 768 and 390 (headless Chrome, 390 px iframe; the full page at 1440, 1024 and 768 in
  slices, the full page at 390 to the last section). Hero scenery, chart with its key, folded frame and column guide,
  notebook panel and related links at every width. The unfolded frame and the opened notebook drawer were read in the
  browser pane at about 800 px, and the opened drawer again at 390 px (page scroll width 390, the notebook's frame
  scrolls inside its own box, the plot image is 300 px wide). Nothing clipped or overlapping; each stratum's corner
  label is fully visible. The multi-year axis
  now carries year labels (2009, 2011, ... at 1440; 2009, 2014, 2019, 2024 at 390), so the writer's template problem 2 is
  gone in the current template. Light theme only.

## Findings

### 1. blocker: `page.facts.cadence` says NESO states no interval; NESO states "Hourly"

`facts.cadence` reads "Half-hourly values; NESO republishes the whole file, at no stated interval". The vendor's own
package metadata, in the probe the note cites for other quotes, carries an extra named Update Frequency with value
"Hourly":

```
gridflow/.planning/phases/neso-data-portal/_probe/show_historic-generation-mix.json
  ... {"key": "Update Frequency", "value": "Hourly"} ...
```

The same field says "Twice weekly" on the embedded and interconnector registers, so it is a populated vendor field, not
boilerplate. The writer's evidence for "no stated interval" was the note's own TODO, not the vendor metadata. The canonical
note body repeats the error: row `Publication lag`, "TODO, republication cadence not stated", which the writer edited
elsewhere in the same table.

The vendor label also sits uneasily with what the capture sidecars show (bronze `ckan_last_modified` against
`fetched_at`: 20 minutes, 14.6 hours, 9 minutes; the 6 Sep capture saw a last-modified time from the previous evening). So
the right wording is the vendor's label, attributed and not endorsed, for example: "NESO's package lists an update
frequency of Hourly; the file's last-modified time is what silver records". Do not state hourly as an observed cadence.

### 2. major: `page.record.fields.imports` reads as net imports; the file is gross per link

The line says "Interconnector imports, MW; NESO curtails net-negative values at zero". The natural reading is the net of all
links floored at zero. Reproduced against fuelhh (fuelhh latest, `INT*` fuel types, 1 Jun to 26 Sep 2026, 5,650 half-hours):

- `imports` against the sum of each link's positive flow: mean absolute difference 36 MW.
- `imports` against the net of all links floored at zero: 1,369 MW.
- The net of all links is negative in 1,066 of those 5,650 half-hours.

The writer found this (it is in the note body and the defect list) but the page, where a modeller reads the column, says
only the sentence that suggests the wrong reading. Use bullet 2 sets the file "beside fuelhh's outturn", which is exactly
where a user would net flows. The page needs a plain scoped line, for example: "imports tracks the sum of fuelhh's
positive link flows, each link floored at zero; it is not net imports (checked against fuelhh; NESO does not say)".

### 3. major: `page.record.fields.low_carbon` and `renewable` omit that `storage` is inside both

The lines list only NESO's examples ("wind, solar, hydro, nuclear, biomass"; "wind, hydro, solar"). Reproduced on the
26 Sep 2026 capture (310,931 rows):

- `low_carbon` = nuclear + wind + wind_emb + hydro + biomass + solar + storage, within 2 MW on every row.
- `renewable` = wind + wind_emb + hydro + solar + storage, within 1 MW on every row.
- Without `storage` the gap is up to 2,660 MW (`storage` is above zero on 178,498 rows).

So pumped storage (net discharge) counts as renewable and low-carbon, which NESO's descriptions do not say, and the
examples also omit `wind_emb`. A reader building a mix or a share from these totals double counts or mis-adds. The eight
rows cannot show it (`storage` is 0.0 in all eight, and the frame folds before `low_carbon` at some widths). Say it in
both lines, scoped as a check ("includes `storage` and `wind_emb`; checked, NESO's examples omit both").

### 4. major: `page.how_used[0]` recommends full-history features; the early-year breaks in `biomass` and `other` are not visible anywhere on the page

`how_used[0]` is "Long-history targets and features for GB carbon-intensity and fuel-mix models". The page states only
that `solar` is zero before 2013 (the chart caption). Reproduced on the 26 Sep 2026 capture:

- `biomass`: first non-zero half-hour 2017-11-01 20:00 UTC (zero for 8.8 years). Share of zero half-hours is 1.0 each
  year to 2016, 0.84 in 2017, 0.0 from 2018.
- `other`: zero before 2012-02-01 16:30 UTC, then 238 MW (2012) rising to about 1,616 MW (2016) and 1,398 MW (2017), then
  82 MW in 2018. Monthly means: October 2017 `other` 932 MW and `biomass` 0; November 2017 `other` 134 MW and `biomass`
  1,491 MW, with `generation` about 33 to 38 GW either side. The two moves coincide; NESO gives no reason.
- `solar`: zero before 2013-01-01 (on the page).

A consumer using `biomass` or `other` over the full history would read a step change as physics. The writer put the
`biomass` and `solar` zeros in the note's modelling notes and the defect list but not on the page, and missed `other`.

Remedy note, because rubric 3 limits what the page may say: a bare "biomass is zero before November 2017" is a local
first date that nothing on the page shows (the `solar` sentence passes only because the chart draws it). So do not just
paste the dates into a guide line. Either (a) rewrite `how_used[0]` so it stops recommending full-history features for every
column, for example naming what the page can back (`carbon_intensity` and the main fuel columns, with the `solar` start in
the chart) and warning that other columns change definition in the early years; or (b) add a notebook cell whose printed
output exposes the step (monthly means of `biomass` and `other` across October to December 2017, or a plot), and point the
`biomass` and `other` guide lines at it. Option (b) makes the dates page-visible and keeps the claim honest.

### 5. nit: `page.what_it_is` omits NESO's statement that missing points are replaced by a seasonal model

The vendor text the note quotes says the file "has seasonal decomposition applied to correct missing or irregular data
points" (package notes, probe `show_historic-generation-mix.json`, quoted in the note's known issues). That supports a
filled half-hourly grid, so "every half-hour since 2009" in `summary` is consistent with it (and "half-hourly from
1 January 2009" is vendor-stated). The omission is the issue: some values are model fill, not measurement, and the page's
first use is model targets. Add NESO's sentence to `what_it_is` as a vendor statement. Also, `generation` includes
`imports` and `storage`, so "generation ... by fuel type" in the summary is loose; "supply" or "mix" would be exact.
Severity nit because the page makes no claim the sentence contradicts.

### 6. nit: `page.record.fields.zero_carbon` turns NESO's "e.g." into a "described sum"

NESO's description is "Zero carbon generation e.g. wind, solar, hydro, nuclear" (datastore field metadata), not a sum.
"here below NESO's described sum" is true in the rows shown (16,695 against wind plus solar plus hydro plus nuclear of
27,167 in the first row) but misquotes the vendor. Reproduced: `zero_carbon_pct` exceeds `low_carbon_pct` on 204,578 of
310,931 rows of the 26 Sep capture, and differs from 100 x `zero_carbon` / `generation` by up to 69.2 points; every other
`_pct` column matches within 0.053 points. The page scopes both lines with "here" (correct: file-wide counts are local
data), but neither line says "undocumented", which the note does. Suggest: "NESO's examples are wind, solar, hydro,
nuclear; the totals here are well below them and no fixed sum fits" and "NESO's zero-carbon percentage; in these rows it is
not `zero_carbon` over `generation` and it is above `low_carbon_pct`".

### 7. nit: `page.record.caption` names only `solar` and `imports` as revised

In the eight rows `carbon_intensity` also differs between captures (63 against 53, 64 against 53, 74 against 55, 75
against 56), and so do `generation`, `low_carbon`, `zero_carbon`, `renewable` and the matching percentages. Reproduced for
the whole pair of captures: `solar` changed on 27 half-hours (all on 5 Sep 2026, up to 721 MW); 1,172 half-hours differ in
some column. The caption would mislead only by omission; name `carbon_intensity` as well.

### 8. nit: sample frame at 390 px reads as four duplicate pairs (decision: keep the pairs)

At 390 only `timestamp_utc` stays visible (the `…` fold hides `published_at`, `solar` and the rest), so the eight rows show
as four identical stamps in pairs. The caption directly above says "Four half-hours ... in two captures", and the guide lists
`published_at` as a row identifier, so the frame does not mislead; the unfolded frame (opened in the pane at 800 px, scrolls
horizontally, all 40 columns) is clear. Decision: do not swap to eight distinct half-hours. The pairs show the vintage
axis, which is the dataset's distinguishing feature and the page's third use. Eight distinct half-hours would hide it (the
latest view keeps one row per stamp). Template point for the seat: a two-column key that folds one key column at 390 is
confusing; keeping both key columns visible, or starting the frame with `published_at`, would fix it for every
append-only page.

The eight rows are the last day of the older capture (published 5 Sep 2026 at 22:15 UTC, data to 21:00), so they are the
provisional tail. The caption does not say that, and the page makes no claim about revisions elsewhere, which is correct.

### 9. nit: `page.chart_view.alt` skips 2023 to 2025

Reproduced from the series (daily-mean maxima by year): 613 (2013), 1,003 (2014), 2,045 (2015), 2,795 (2016), 3,174 to
3,475 (2017 to 2022), 3,895 (2023), 4,091 (2024), 4,912 (2025), 5,444 (2026-07-12); minima at most 153 MW; last day
2,426 MW. Every number in the alt matches. The alt jumps from "3,200 to 3,500 MW from 2017 to 2022" to "5,444 MW on
12 July 2026", so a reader of the alt alone cannot tell the rise was steady; add "3,900 to 4,900 MW in 2023 to 2025".

Chart provenance otherwise verified: recomputed from silver (latest capture per `timestamp_utc`), 6,477 daily means,
48 half-hours each, identical to the committed series to 0.0005 MW; first non-zero half-hour 2013-01-01 08:30 UTC (31 MW);
zero for every half-hour before 2013; maximum 5,443.7 MW on 2026-07-12. Silver holds three captures (published 20 Aug,
5 Sep, 26 Sep 2026; 309,161 / 309,931 / 310,931 rows), no duplicate `(timestamp_utc, published_at)`, 1,000 stamps with one
capture, 770 with two, 309,161 with three. The chart's dedup is the `_latest` rule and every point comes from the 26 Sep
capture, as the caption says. Handled honestly.

### 10. nit: `page.record.fields.timestamp_utc` leaves the check's owner and span unsaid

"NESO states UTC, start matched against fuelhh" is an observation (it does not call start a NESO rule), but the passive
"matched" does not say the project did it, nor over what span. Reproduced and wider than the writer's check: at lag 0 the
NESO `wind` equals fuelhh `WIND` on 98.5% and `nuclear` equals `NUCLEAR` on 96.7% of 5,650 half-hours (1 Jun to 26 Sep
2026); `hydro` against `NPSHYD` and `storage` against floored `PS` differ by 0 MW. By year 2021 to 2026 the lag 0 mean
absolute difference for `wind` is 0.0 (2021), 12.6, 17.1, 18.7, 9.6, 10.3 MW, against about 190 to 410 MW at a 30 or 60
minute shift. fuelhh silver starts in 2021, so 2009 to 2020 is unchecked. Suggest: "Start of the half-hour in UTC. NESO
states only UTC; stamps line up with fuelhh's start times (checked 2021 to 2026)".

### 11. nit: "currently" and the announced change are dropped from the `other` composition statements

NESO's text is "Batteries (NET discharge) are currently included in the OTHER category. Transmission-connected solar farms
are currently included in the OTHER category", with "Updates will be released later in 2026". `what_it_is`, the `other`
line and the `solar` key note state it as standing fact. Keep "NESO currently counts" (no planning words needed). The page
correctly never calls `solar` embedded or estimated, and agrees with the note's `solar` composition section (a deduction,
not a vendor statement); the use bullet "`wind_emb` and `solar` to set beside fuelhh's ... outturn, which lacks both" leans
on that deduction mildly but is true as written (fuelhh has no solar code and is transmission only).

### 12. nit: `_pct` guide lines define the denominator as a fact

"Gas as a percentage of `generation`, as NESO publishes it" (and 12 more) is a project measurement, not a NESO statement.
NESO says only "Fuel Type as a percentage for gas generation". Reproduced: each of the 14 `_pct` columns other than
`zero_carbon_pct` and `generation_pct` equals 100 x column / `generation` within 0.053 points on every row of the 26 Sep
capture. True, but unscoped. Optional: say once "NESO names no denominator; each matches `generation`" in the first line.

### 13. nit: vault body says `zero_carbon` fits "through 2018"; it fits through 2022

Note body (known issues, "Derived columns") and the defect text say `zero_carbon` equals nuclear + wind + hydro + biomass +
storage "through 2018" and "fits no fixed sum in recent years". On the 26 Sep capture the maximum difference is at most
1 MW in every year 2009 to 2022; the first half-hour above 1 MW is 2023-01-01 08:30 UTC, and 43,936 half-hours deviate
from then on (2.0 MW at first, up to 1,441 MW in 2024). Correct the year in both places. `generation` within 3 MW,
`fossil` within 1 MW, the 1,172 changed half-hours and the `solar` change (27 half-hours, up to 721 MW, all 5 Sep)
reproduce.

### 14. nit: notebook `.head()` shows only night rows

Cell 4 prints `solar`, `wind`, `wind_emb`, `gas`, `generation` for the first five rows (00:00 to 02:00 UTC on 19 Sep),
so `solar` is 0.0 in all five. Not wrong, but the demonstrated column is empty. The lead matches `query()` (checked:
relation `silver_neso_data_portal_historic_generation_mix_latest`, date column `timestamp_utc`, TIMESTAMPTZ, half-open UTC
days with the end day included), the output prints `01:00:00+01:00` for 00:00 UTC (the lead says times print in local
time), and the plot alt matches the PNG and the data (stack of eleven columns, nuclear at the bottom, solar on top;
generation 22,707 to 38,306 MW; solar peak 13,127 MW on 2026-09-20 12:00 UTC; daily means wind 15.2 and 11.4 GW on the
19th and 20th, gas 9.2 and 12.2 GW on the 21st and 22nd).

### 15. nit (template): dataset id breaks mid-word at 390 px

The hero id pill wraps as `neso_data_portal/historic_generation_mi` then `x` on its own line. Cosmetic, template-owned.

## Facts and structure confirmed

- `raw_feed.requests`: `package_show?id=historic-generation-mix` on `https://api.neso.energy/api/3/action/`; the resource
  URL equals the bronze sidecar `request_url` (package and resource ids, `df_fuel_ckan.csv`). Resource selected by exact
  name and CSV format, so "finds the file by exact name" is true.
- `raw_feed.commands`: `--last 24h` on both is right. `fetch()` ignores the window as a selector, screens only `end`
  (not in the future, within 48 hours, span within the lookback maximum), and partitions at `end.date()`; transform with
  `--last 24h` iterates `start.date()` to `end.date()`, so it covers the ingest partition. "Dates select nothing" is true.
- Grain and key: `ENTITY_KEY_COLUMNS = (timestamp_utc, published_at)`, `APPEND_ONLY`, `VINTAGE_PER_BRONZE_FILE`; the latest
  view keeps one row per `timestamp_utc`. `published_at` is the sidecar `ckan_last_modified` read as UTC (sidecar
  `2026-09-26T18:19:36.497453` equals the silver value). `timestamp_utc` is the raw `DATETIME` read as UTC, with the
  datastore field metadata as the stated source.
- Vendor quotes the page relies on match the probe: "contains data from 1 January 2009", "Pumped Storage units (NET) are
  represented in the STORAGE category", "All Net-Negative values are curtailed at zero", the `GENERATION` description (eleven
  columns), `WIND_EMB` titled "Wind EMB" with no description, `CARBON_INTENSITY` with an empty unit and the description "per
  kilowatt hour of electricity consumed". In the 26 Sep capture `imports` and `storage` have no values below zero.
- No local-data leakage beyond the caption's capture date (a property of what the chart plots, acceptable) and "100 in
  these rows" (visible). Related notes are 7 to 10 words and the four pages resolve.
- Vault body edits: smallest spans with evidence, the curl example untouched; the exceptions are the `Publication lag` row
  (finding 1) and the "through 2018" year (finding 13).

## Defects for the backlog (additions to the writer's list)

- **NESO historic_generation_mix: `other` and `biomass` change definition at 2017-11-01.** In the capture published
  2026-09-26 18:19:36 UTC, `biomass` is 0 before 2017-11-01 20:00 UTC and `other` falls from a monthly mean of 932 MW
  (Oct 2017) to 134 MW (Nov 2017) while `biomass` rises from 0 to 1,491 MW. NESO gives no reason. Treat as a structural
  break; do not read `biomass` or `other` as one series across it. `other` is also 0 before 2012-02-01 16:30 UTC.
- **NESO historic_generation_mix: package metadata states Update Frequency "Hourly".** The vault's "not stated" is wrong; the
  captures held show last-modified gaps of hours to days, so the label does not describe an observed cadence.
- **NESO historic_generation_mix: `zero_carbon` fits nuclear + wind + hydro + biomass + storage through 2022,** not 2018 (first
  deviation above 1 MW on 2023-01-01 08:30 UTC).
