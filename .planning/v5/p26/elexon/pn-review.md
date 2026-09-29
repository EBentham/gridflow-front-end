# pn (Physical notifications) review

Checker: Opus 5.5 · high, 2026-09-29. Inputs: the vault note in the batch vault worktree (its `page:` block and
`git diff origin/master`), the artefacts under `site/hifi/data/{series,samples,notebooks}/elexon/pn*`, the page
built with `gridflow-build --only elexon/pn`, the writer's report, gridflow code, local bronze and silver (read only),
and the vendor documents below. Screenshots: headless Chrome on port 9741 (server stopped) at 1440, 1024 and 768, and
390 through a 390 px iframe. The unfolded frame and the open notebook drawer were checked at 1280 and 390 in the
browser pane.

## Verdict: REVISE

Two majors, three nits. The segment reading, the chart, the frame, the notebook, the request and the commands all
check out. The majors are both about what the page says. The sign is documented by the Grid Code, but the page says
it is not named. And the null-id line says those units "share" a row, when silver in fact keeps one unit's levels and
drops the rest.

## Findings

### 1. major: `page.chart_view.key[dinorwig].note`, sign stated as unnamed when the Grid Code names it

- **What is wrong:** "The BSC names export and import, not which sign is which." This may be literally true of the BSC
  documents read:
  - the writer read the glossary entries;
  - I checked Elexon's Section Q simple guide, which also states no sign.
  But the BSC definition itself says the PN is made "under the Grid Code", and the Grid Code states the convention:
  - an importing unit's Physical Notification is negative;
  - PN levels are MW figures.
  A reader of the note will conclude that the sign is undocumented. The rubric's sign rule is to say what the code or
  vendor says, so a documented convention should not be presented as missing.
- **Evidence:**
  - Grid Code BC1 Appendix 1, BC1.A.1.1 "Physical Notifications", Issue 3 (BETTA go-active text,
    https://www.ofgem.gov.uk/sites/default/files/docs/2005/02/9753-5505_gcbc1_0.pdf), p. BC1-13:
    - it calls the PN "a series of MW figures and associated times";
    - it gives the sign rule: when the BM Unit will be importing, "the Physical Notification is negative";
    - it adds that a linear interpolation is assumed between the From and To levels.
  - Silver agrees with this sign:
    - `T_DINO-5` (pumped storage) runs from -293 to 300;
    - interconnector import `I_I2D-INCM1` is -110 in the eight rows.
- **Fix:**
  - Key note, for example: "Pumped storage by the register. Negative is import, per the Grid Code (BC1)."
    (14 words, within the 18 budget.)
  - Add the Grid Code citation and the sign sentence to the note body's Overview, next to the glossary quote. Cite the
    current NESO Grid Code BC1 Appendix 1 if the writer can read it. The copy above is the 2005 issue.
  - The writer's Overview line "The glossary entries for PN and Import do not state which sign ..." can stay, since it
    is true of the glossary.
  - The chart and notebook alts may then call Dinorwig's negative stretches imports (optional).

### 2. major: `page.record.fields.bm_unit_id`, the null-id row is not "shared"

- **What is wrong:** "units sent without one share a null row per period" suggests the row stands for all of those
  units together. It does not:
  - the dedup keeps the last null-id record received and drops the other 45;
  - their levels are gone from silver, and so is `nationalGridBmUnit`, which silver never keeps.
  The task asked for this to be stated plainly and accurately. `what_it_is` is at 59 of 60 words, so the field line is
  the only place on the page that says it.
- **Evidence:**
  - Code:
    - `gridflow/silver/elexon/pn.py:98-101` runs `unique(subset=[settlement_date, settlement_period, bm_unit_id],
      keep="last")`, and Polars treats null keys as equal;
    - `pn.py:58-64` maps no `nationalGridBmUnit`.
  - Bronze, latest capture (`raw_20260926*`):
    - 46 null-`bmUnit` records in every period, settlement dates 16 to 22 Sep;
    - for 2026-09-20 SP10, the last one is `IVD-VKL1` (0/0);
    - the silver null row for that period is `(0.0, 0.0)`.
  - One null-id unit, `AG-PEPG01`, has non-zero levels on every day of the window (1 to 18 records a day). Silver
    cannot show them.
  - Silver has 48 null `bm_unit_id` rows per settlement date, one per period.
    Expression: `group_by("settlement_date").agg(pl.col("bm_unit_id").is_null().sum())` gives 48 for each of 16 to
    22 Sep.
- **Fix:** Reword it, for example: "Elexon BM unit id; null for units sent without one, one kept per period" (14
  words). The note body's `bm_unit_id` row already describes the collapse. Its "collapse into one null-key row" could
  add "keeping the last one's levels".
- **Not affected:** No count or chart on the page includes the null row:
  - the chart filters to three named units (`provenance.rows_matched` 1008 = 3 x 336);
  - the eight rows filter to named units;
  - the notebook filters to `T_DINO-5`;
  - the page states no unit count.

### 3. nit: vault body, Known issues, "Silver keeps one segment ...", the exception does not reproduce

- **What is wrong:** The body says "every kept segment was the one that starts the period, except 48 rows on
  2026-09-21 (two supplier units kept from an earlier capture)". I cannot reproduce the exception, on either count:
  - those rows start their period;
  - they come from the latest capture.
- **Evidence:** I replicated `read_bronze` and `transform` in memory, keeping `timeFrom` and the source file.
  - On each settlement date 16 to 22 Sep, 0 non-null kept rows have a `timeFrom` that differs from `timestamp_utc`.
  - Every kept non-null row comes from the `raw_20260926*` capture. On 2026-09-21 that is 119,592 of 119,592.
  - `2__DSTAT008` and `2__NSTAT005` are present in the 26 Sep capture for all 48 periods. The `raw_20260921*` capture
    covers only 24 periods and is overridden by it.
- **Fix:** Drop the "except ..." clause: "Checked on bronze 2026-09-16..22: every kept segment was the one that starts
  the period." The writer's report makes the same claim, so its evidence row needs the same correction. The page
  itself is unaffected.

### 4. nit: `page.record.select`, the frame shows no distinguishing column below 670 px

- **What is wrong:** At 1280 the folded frame shows `bm_unit_id`, `level_from` and `level_to` (fold thresholds 670,
  760 and 840), so nothing at the 1280 budget is hidden. Narrower screens lose the levels:
  - at 1024 both levels are still shown;
  - at 768 the folded frame ends at `bm_unit_id`;
  - at 390 only `settlement_date` and `settlement_period` stay in view, and they are identical in all eight rows.
- **Fix:** `select.columns: [bm_unit_id, level_from, level_to]`, so that the unit and its levels print first.

### 5. nit: `page.notebook.cells[1]`, `.head()` shows only zeros

- **What is wrong:** `dino[...].head()` prints settlement periods 1 to 5 of 16 Sep, all `0.0 / 0.0`. The output is
  real and error-free, but it shows no notified level. A slice that starts in a non-zero stretch would show the column
  that matters. One example is `dino[dino.level_from != 0][...].head()`, whose first rows are the 300 MW block on the
  16th. Optional.

## Checked and correct

- **Segments.**
  - The transformer drops `timeFrom`/`timeTo` (`pn.py:58-64,111-120`) and keeps the last record per key.
  - "Here each kept segment starts its period" holds for every non-null row in the window. It holds for all 144
    charted unit-periods on every date (my bronze replication, 0 mismatches).
  - The charted units have multi-segment periods on 55 to 74 of 144 unit-periods a day. So the caption's "moves inside
    a half-hour are not shown" is a necessary caveat, and it is accurate.
  - The chart claims no within-period profile. Its alt uses "steps" and period-level values.
  - The Grid Code's linear-interpolation rule means the true PN path is piecewise linear inside a period. Silver cannot
    give that path, and the page says so.
- **Chart.**
  - Distilled from the vault spec: `spec_origin: vault`, no staged spec, no authored override, build digest check
    passes.
  - 3 series x 336 points, no nulls, `aggregation: last` over exactly one row per unit and period.
  - The alt numbers match the series:
    - Pembroke 0 to 435, and 219 to 431 after the 20 Sep ramp;
    - Dinorwig min -293 at 2026-09-18 09:30 UTC, max 300;
    - Seagreen min 1, max 354 on the 19th, 353 on the 20th, 2 on the 22nd.
  - The x label "each starts at 23:00 UTC" is right for BST dates.
- **Units.** MW, per the Grid Code BC1.A.1.1 "series of MW figures".
- **Raw request.** It matches `endpoints.py:94-98,291-313` and the bronze meta `request_url` for 2026-09-20 SP1.
- **Period loop.** 46/48/50 periods per date (`client.py:184-188`).
- **Commands.**
  - The ingest end date is fetched (`client.py:360-372`, `_date_range` inclusive, dispatched at `client.py:85-86`).
  - There are no `PARTITION_SOURCE_OFFSETS` (base default `(0,)`), so ingest and transform share 16 to 22 Sep.
- **Eight rows.**
  - Real (`generated_by: gridflow-sample`).
  - `2__BCMRO002` `0.0 / -42.0` shows the kept-segment effect.
  - The guide has a line for every non-pipeline column, key columns first.
- **Notebook.**
  - Written by `scripts/run_notebooks.py`, read-only cells, no errors.
  - `pn-5.png` matches `plot_alt` (300 blocks on six of seven evenings, negative stretches on the 17th to 20th, the
    -263 dip on the 22nd).
  - The lead matches `source.py:449` (`ORDER BY {date_col}`) and `_date_range_predicate` (inclusive `BETWEEN`).
    `_BITEMPORAL_EXCLUDE` covers the lineage columns, and `schema_manifest.py:136` has `settlement_date` for pn.
- **Build and detector.** `gridflow-build --only elexon/pn` passes and `detect.mjs --json` returns `[]`. The mirror
  `vault/elexon/pn.md` is byte-identical to the vault note (`cmp`).
- **No local data, leakage or filler.** A grep of the rendered `<main>` found:
  - no `locally`, `held`, "our", `since 20`, local row counts or "% of";
  - no em dashes, middle dots, arrows, "live" or "now".
  "14 days" is the `uou2t14d` vendor horizon. The related notes are 12 words or fewer.
- **Screenshots, light only (the site CSS has no `prefers-color-scheme`).**
  - Hero scenery (turbines, "transmission lines", "substation", "battery storage"), the chart and its key, the raw
    feed, the frame (folded and unfolded), the guide, the notebook drawer, the related list and the stratum corner
    labels: none clipped or overlapping at 1440, 1024, 768 or 390.
  - At 390 with the drawer open and the frame unfolded, the page has no horizontal overflow (`scrollWidth - innerWidth
    = 0`). The frame and the DataFrame output scroll inside their boxes.

## Template observation for the seat (not the writer's)

The line renderer plots each value at the middle of its half-hour (`chart_svg.py` `_lines`, `t + half`), while
`level_from` is the level at the half-hour's start. At this scale the shift is about 1.5 px, so it does not change
any finding.

## Scratch left behind

`scratchpad/pn_seg_check.py` (the bronze replication), `scratchpad/bc1.txt` (Grid Code text) and
`scratchpad/pn-rev/` (screenshots, the iframe wrapper, the Chrome profile). No repo or data files were written.
