# gie/lng (ALSI LNG terminals): checker review

Checker: Opus 5.5 · high, 2026-09-29. Screenshot port 9857.

## Verdict: REVISE

1 major, 2 nits. No blockers. Every fact, number, URL, command and unit on the page holds against code, silver and
bronze. The one major is a missing caveat: two charted values carry a non-`C` vendor status that silver drops, and the page
does not say what dropping `status` means for the chart.

## Findings

### 1. major: `page.chart_view.caption` (or a key note on `nl` and `fr`)

**What is wrong.** Two of the 70 charted values arrived with a vendor `status` other than `C`. Silver drops `status`,
so on the page they look the same as every other point. The page never calls them final. Its only mention of `status` is
the list of dropped fields in `raw_feed.note`, which gives no consequence, and the caption's "as sent" hedges where the
values came from, not their status. The author brief requires a caption to state "any caveat needed to read it", and the
seat asked for this check by name.

**Evidence.**
- The bronze file for the charted window (`gie_alsi/lng/2026/09/13/raw_20260926T174756Z_*.json` and `..._174812Z_*.json`)
  has two non-`C` records:
  - NL, `gasDayStart` 2026-09-17, `status: "E"`, `sendOut` 734.6, `updatedAt` 2026-09-18 06:50:03
  - FR, `gasDayStart` 2026-09-18, `status: "E"`, `sendOut` 1052.8, `updatedAt` 2026-09-19 08:10:04

  Every other non-GB record in the window is `C`, and GB is `N`.
- Both values sit in the committed series: `nl[4]` = 734.6 and `fr[5]` = 1052.8. The FR value is the day France's rise
  to about 1,075 begins.
- `status` is not in `output_cols` (`silver/gie/alsi.py:167-181`) and not in the silver schema (Polars `read_parquet` →
  13 columns, no `status`).

**Fix: evidence only.** No gridflow code, schema or vault page defines `C`, `E` or `N`, so the page must **not** say
"estimated" or "provisional" until a source for the codes is cited. Something like this stays within the evidence:
"GIE tags each row with a `status` code (`C`, `E` or `N` in these responses) that silver drops, so the chart cannot
tell them apart." The codes are visible in bronze and the drop is a code fact, so this passes rubric §3. Do not count
the `E` rows on the page. A count would be a statistic about our own copy, and the rows are not visible in the chart.

### 2. nit: note body, `## Overview`, first sentence (not rendered)

**What is wrong.** The sentence still reads "Country-level LNG terminal inventory and flow data from GIE ALSI." The writer
proved that inventory never reaches silver, and corrected the `lng_in_storage_gwh` and `lng_pct_full` rows, but left the
note's opening line as it was. Read as a description of the silver dataset, it overclaims inventory, which is the same
overclaim the seat is fixing in `gie.json`.

**Evidence.**
- Canonical note, line 120 (the body opens after the front matter).
- `silver/gie/alsi.py:95-97`: the field map expects `lngInventory` or `gasInStorage`.
- Bronze sends `inventory: {"lng": ..., "gwh": ...}`.
- The silver schema has no `lng_in_storage_gwh` column.

**Fix.** Make the smallest edit: say that the response carries inventory, which silver does not keep yet.

### 3. nit: `page.what_it_is`, "never per terminal"

**What is wrong.** "never per terminal" is a universal. It is true of what gridflow requests: `ALSI_COUNTRIES`, and one
`country=` call each. The writer could not verify whether ALSI itself offers terminal-level queries (author report, "Could
not verify"). As written, a reader could take it as a vendor limit.

**Evidence.**
- `connectors/gie/endpoints.py:17`
- `connectors/gie/client.py` `_fetch_country` (`query_params` carries only `country`, `from`, `till`, `page`, `size`)

**Fix.** Scope it to the request, for example "gridflow requests country totals, not terminals".

## What I checked and found correct

- **Units (look-hard 1).**
  - Only send-out is given a unit (GWh per gas day). This rests on the transformer's column name `send_out_gwh`
    (`alsi.py:98`) and the GIE README ("stocks and flows are GWh").
  - `dtrs`, `dtmi_lng` and `dtmi_gwh` are called "units unconfirmed", "as sent", with no acronym expansion. This
    matches `schemas/gie.py:62-68`.
  - `dtrs` "not a percentage" matches the schema comment, and the page shows values of 724.1 to 2132.3.
  - No inventory or volume unit appears anywhere on the page.
- **Missing inventory (look-hard 2).**
  - `what_it_is` says plainly: "LNG inventory is in the response but not in silver".
  - `raw_feed.note` lists `inventory` among the fields silver drops.
  - No field, chart or notebook line implies inventory, and `dtmi` is not expanded.
  - The hub blurb in `gie.json` is the seat's (ruling), so it is not a finding here.
  - Code: the field map at `alsi.py:95-97` misses the nested `inventory` object. `lng_pct_full` is gated on
    `lng_in_storage_gwh` (`alsi.py:142`). Silver has neither column.
- **Chart (look-hard 3).**
  - The spec is a `stacked-area` of `send_out_gwh` by `country_code`, with `aggregation: sum`, filter
    `country_code ne GB`, and a fixed window from 2026-09-13 to 2026-09-22 on `gas_day` (a `Date` column).
  - The committed series has `spec_origin: vault` and `rows_used` 70 (7 × 10), and matches silver exactly. I pivoted it
    in Polars: NL 587.2 to 763.6, IT 505.8 to 699.8, PT 173.2 to 187.4, PL 84.8 to 190.5, BE 91.8 to 263.8,
    ES 295.0 to 697.9, FR 354.4 (15th) to 1,085.1 (21st).
  - The daily totals run from 2,689.8 on the 13th to a peak of 3,723.5 on the 21st, so the alt text and `plot_alt`
    numbers are right.
  - **Stacking is additive.** Every row is country level, with one row per (gas_day, country_code): 8 × 15, with no
    duplicates (the dedup is at `alsi.py:154-157`). No EU aggregate row exists.
  - **GB.** Every numeric is null for all 10 days, and bronze sends `"-"` with `status: "N"`, name "United Kingdom
    (Pre-Brexit)". "GIE sends it as `-`" is correct.
  - **Key order and paints.** The key order FR, ES, BE, PL, PT, IT, NL is the reverse of `series_order`, so the top of
    the stack comes first. There is no khaki. Named paints for countries follow the approved ENTSO-E precedent
    (`actual_load`, `day_ahead_prices`).
- **`till` claim.**
  - `client.py` `_fetch_country` formats `end.strftime("%Y-%m-%d")` into `till`, and `runner.resolve_dates` turns a bare
    date into midnight UTC.
  - The sidecar `request_url` is `...&from=2026-09-13&till=2026-09-22&page=1&size=300`, and each country's file holds
    10 records running from 2026-09-13 to 2026-09-22. So `till` is inclusive, and "the end day is fetched" is right.
  - The transform window equals the ingest window. The transformer falls back to the covering partition 2026/09/13 (at
    most 35 days back, `base.py:2366-2390`; `gie_alsi` is not exact-partition-only), and
    `_filter_records_to_gas_day` keeps the target day.
  - The paging (`size=300`, stop on `last_page`) matches `endpoints.py:22` and the `client.py` pagination.
- **Gas day (look-hard 5).**
  - `gas_day` is `gasDayStart` parsed to a date (`alsi.py:56-67`).
  - `event_time` is `gas_day` + 06:00 UTC (`gas_day_event_time_expr`, `base.py`), and silver's `event_time` hour is
    always 6.
  - The field line "gridflow labels it 06:00 UTC in `event_time`" calls it a gridflow label and makes no claim about
    ALSI's clock, which is correct.
  - The x label "gas day, as GIE's gasDayStart dates it" is fine.
  - The cadence wording ("as sent in the responses we hold") follows the batch ruling.
- **Rows and notebook.**
  - The sample is `gridflow-sample`, with 8 rows for gas day 2026-09-20. It matches silver, and GB is null.
  - The guide has one line per non-pipeline column, with the key columns first.
  - The notebook was written by `run_notebooks.py`: 5 cells, read-only, no errors.
  - The lead matches `source.py` `query()`: `_date_range_predicate` on `gas_day` (`schema_manifest.py:233`),
    `ORDER BY gas_day`, and the bitemporal columns excluded.
  - I viewed the `lng-5.png` plot. BE is at the bottom, with the others alphabetical upward, and the top edge runs from
    about 2,690 to 3,724. This matches `plot_alt`.
- **Build, detector and leakage.**
  - `gridflow-build --only gie/lng` wrote the page. Its three warnings are for other GIE datasets.
  - `detect.mjs --json` returned `[]`.
  - There is no staged spec or authored override for `gie`.
  - I grepped the `page:` block for em or en dashes, middle dots, `→`, locally, held, our, "since 20", live, now,
    final, and "N rows/days". The only hits were "units unconfirmed", which is intended, and the ruled cadence wording.
- **Vault body edits (§7).**
  - The 8 edits in the writer's report are each small and cited, and each matches the code (`gasDayStart` only;
    the not-written rows; the `event_time` derivation; GB placeholders).
  - The mirror is byte-identical (`cmp`).
  - `.gitattributes` sets `*.md text eol=lf`, so the writer's worry about a whole-file CRLF diff doesn't apply: the git
    diff shows 118 lines inserted and 9 deleted.
- **Clipping and overlap (§5).**
  - Headless Chrome full-page shots at 1440, 1024 and 768: the hero scenery, chart, key, stratum corner labels,
    folded frame, guide, notebook panel and related list are all fully visible.
  - True 390 viewport (pane tab emulation):
    - `scrollWidth` is 390, and no text element lies outside the viewport except inside scrollers.
    - No label boxes overlap (chart ticks or scenery labels).
    - The only "clipped" hits are screen-reader-only spans.
  - Unfolded frame (`#fx` checked) at 1440, 1024, 768 and 390: all 13 columns show, `.fw` scrolls sideways, and
    nothing escapes.
  - Open notebook drawer at 1440 and 390: the panel sits within the gutter (16 to 374 at 390). The `head()` table
    scrolls in `.df-wrap` (300/343), and the plot image fits (right edge 363).
  - Light and dark are the same design: `prefers-color-scheme` gets 0 hits in `theme.css` and `tokens.css`.

## Procedure deviations (for the seat)

- **Headless Chrome and CDP.** With `--virtual-time-budget`, headless Chrome ends the run and drops the renderer, so it
  can't be driven over CDP. Without it, cross-site navigation and `data:`-wrapped iframes lost the renderer ("Render
  process gone").
- **The 390 and interactive checks** therefore ran as numeric DOM measurements in a Browser pane tab of my own, with a
  390×844 emulated viewport. The folded-view shots at 1440, 1024 and 768 were taken with the prescribed flags.
- **Temporary files.**
  - The shots are in `scratchpad/lng-review-shots/`.
  - The Chrome profiles are `scratchpad/lng-review-chrome*`, left in place.
  - I wrote one temporary Polars script to the scratchpad by mistake, then deleted it (a literal-path `rm -f`).
    After that I ran every script over stdin.
- **Server and tab.** The static server on 9857 has been stopped, and my pane tab is closed.

## Defects (paste as is)

- **gie_alsi/lng: vendor `status` codes are undefined and dropped.**
  - ALSI sends a per-row `status` (`C`, `E`, `N` seen in bronze `gie_alsi/lng/2026/09/13/*`). Silver drops it
    (`silver/gie/alsi.py:167-181`), and no code, schema or vault page defines the codes.
  - In the 13 to 22 Sep 2026 window, NL 2026-09-17 and FR 2026-09-18 carry `E`. It was still `E` at ingest on
    2026-09-26.
  - Named unknown for a research unit: what `C`, `E` and `N` mean in ALSI, and whether and when GIE revises `E` rows.
  - Then decide whether silver should carry `status` (and `updatedAt`) so that readers and vintaging can tell them apart.
- **vault `30-vendors/gie/datasets/lng.md` Overview overclaims inventory.** See finding 2. It is the same overclaim as
  the `gie.json` hub blurb the seat is fixing.
