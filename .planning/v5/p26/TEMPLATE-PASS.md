# End-of-batch template pass (2026-10-07)

Worktrees: front end `scratchpad\p26-rest` (branch `v5/p26-rest`), vault `scratchpad\vault-p26-rest`. No git writes.
Paths below are relative to the front-end worktree unless they start with `vault:` (the vault worktree's
`30-vendors/entsog/datasets/`). Screenshots: `scratchpad\tpass\shots\`.

## Items

### 1. Blank-page test (done)
- `tests/test_dataset_page.py:199-226`: the blank family example moves from `neso/national-carbon-intensity`
  to `entsoe/outages` (lead `outages_generation`, member `outages_offshore_grid`). It has no page block on
  `origin/main` or this branch. The held `entsog/capacity-by-indicator` still has a page block here, so it
  was not used.
- The test now also asserts that the family page itself is blank (`ds-blank`, no `data-chart`), alongside
  the member chip and pointer page. LF endings kept.

### 2. Zero line hidden by the x axis (done)
- `src/gridflow_front_end/chart_svg.py:513`: `_lines` draws the axes first and the series over them, so a
  series at 0 throughout runs along the axis in its own colour. Stacked areas are unchanged. Headroom below
  0 was rejected: `nice_ticks` would add a negative tick and a mid-plot zero line.
- Test: `tests/test_chart_axis.py:104` (the zero path comes after the frame, at `y == fr.bottom`).
- Evidence: `neso/regional-carbon-intensity`, North Scotland drawn after the axis at y 410 (wide) and 246
  (narrow). `regional-1440.png` shows the axis in North Scotland's horizon colour.

### 3. Overlapping lines (done) and the 390 folded table (done)
- `chart_svg.py:49, 468-511`: on dot charts (60 points a series or fewer), a later series that lands within
  2.5 px of an earlier one at the same time stamp is drawn **dashed (6 5) over that stretch**, so the line
  beneath shows through the gaps, and **its dots are drawn small (r 1.7) inside the earlier dot**. It stays
  solid elsewhere. The key is unchanged.
  - Dense line charts are left alone: a first version dashed dozens of brief near-crossings on approved
    pages (day-ahead prices, actual load, wind).
  - Affected charts: `entsog/gcv`, `elexon/ndf` and `elexon/uou2t14d` (real shared stretches), plus a
    single small dot on `indgen`, `nominations`, `physical_flows` and `aggregated_physical_flows`.
- The ring dots alone were tried first and failed visually: the horizon line was still hidden from 13 to
  18 Sep (`gasq-1440-zoom.png` before the change).
- Test: `tests/test_chart_axis.py:122` (radii, and a dashed stretch then a solid one, on both frames).
- Evidence: `gasq-1440-zoom.png`, with Bacton (IUK) entry alternating clay and horizon across 13 to 18 Sep.
- **390 folded table:** on gas quality, the frame showed only `timestamp_utc`, so the eight rows read as
  duplicates.
  - `operator_key` needs 355 px. The box is 358 px. The tier rounded up to 360, so the column folded.
  - `src/gridflow_front_end/build.py:1076`: `_FRAME_STEP` goes from 10 to 5. A column still shows only where
    the box is at least the width it needs (the estimate matched the rendered box within 2 px).
  - At 390 exactly three frames change, each gaining `operator_key`: gcv, nominations, and
    firm_available (held).
  - Evidence: `gasq-table-390.png` (two columns, rows tell apart, box inside the gutter).

### 4. Values containing `|` (done, samples regenerated)
- `src/gridflow_front_end/sample.py:67-98, 102-135`: before Polars prints, `|` and line ends (`\r\n`, `\n`,
  `\r`) in String and List(String) columns become private-use stand-ins (U+E000 to U+E003). They are
  restored in each cut cell, so the output equals what Polars prints. A value that already holds a stand-in
  raises `SampleError`. Line ends were included because a multi-line cell (operators `b_m_penalties`)
  breaks the read-back the same way.
- Tests: `tests/test_sample_columns.py:38` (pipe, line end, list, nulls) and `:54` (stand-in collision).
- Regenerated with `uv run --extra distil gridflow-sample --dataset entsog/aggregated_physical_flows
  --dataset entsog/operators` (operators is the reference-data lead). Both files are **byte-identical** to
  the hand-masked versions the authors committed (`cmp`). The site was rebuilt.

### 5. Related-dataset wording (done)
- `vault:physical_flows.md:114` and `vault:nominations.md:150`: "Physical flow summed by balancing zone
  rather than by point" becomes "ENTSOG's British-zone entry totals from production, storage and LNG
  only". That is 10 words, within the 12-word budget, and matches the note's own scope (entry from
  production, storage and LNG only, not a zone balance).
- Mirrors `vault/entsog/{physical_flows,nominations}.md`: `cp` plus `cmp` gave byte-equal copies.
  - The `physical_flows` mirror previously differed from canonical only in line endings (LF against CRLF).
- Built pages carry the new line (1 hit each). The old wording is gone (0 hits).

### 6. Narrow column guide (done)
- `site/hifi/assets/dataset.css:42-44, 46`: the name column is `fit-content(min(48%, 280px))`, not
  `max-content`, and `dt` gets `overflow-wrap: anywhere`. Only names over about 34 characters wrap.
- Measured at 1440 (browser pane, cache-busted), narrowest meaning, before and after:

  | Page | Before | After |
  |---|---|---|
  | `entsog/reference-data` | 91 px | 289 px |
  | `entsog/tariffs-and-simulations` | squeezed | 289 px |
  | `market_depth`, `gas-quality`, `nominations-allocations`, `agsi-storage`, `solar-weather`, `fuelhh` | unchanged | unchanged, no name wraps |

  - A 45% cap was tried first and wrapped `market_depth`'s 33-character name by 1 px.
- Evidence: `refdata-guide-1440.png`.

### 7. Percent axis past 100 (done)
- `chart_svg.py:47, 405-409`: a stacked `%` chart whose stack tops out at 101 or less ends its axis at 100.
  `neso/generation` sums to 100.2, which gave 0 to 125 wide and 0 to 150 narrow. It now gives 0 to 100 by
  20 (wide) and by 25 (narrow). A `%` line chart (`gie/storage`) is unchanged.
- Test: `tests/test_chart_axis.py:145` (both drawings end at 100).
- Evidence: `genmix-390.png` (axis 0, 25, 50, 75, 100) and `genmix-1440.png`.

### 8. DESIGN.md (done)
- `DESIGN.md:128-133`, anatomy step 2: after the chart, for weather sites (the Open-Meteo pages), the
  locations map.
  - The clause covers the outline, the markers, the dot at the answered grid cell, the hover or tap card
    and the no-script linked table.
  - It notes that its statistics are the only ones computed from our own rows (ruling 50), and that each
    states its source.
- The map review's separate note, recording ruling 50 against rubric section 3, is left for the seat.

### 9. Broken link (done)
- The dead link was `[Nominations vs allocations](../../../20-domain/markets/gas-nominations.md)` in 19
  ENTSOG notes (also on vault `origin/master`). No domain note covers nominations against allocations.
- Each link now points at the existing family note: `[Nominations, renominations and allocations](nominations.md)`.
  `nominations.md:181` itself points at `[Allocations](allocations.md)`. All 19 canonical notes were edited
  byte-wise (CRLF kept) and mirrored with `cp` plus `cmp` (19 of 19 equal).
- 0 hits for `gas-nominations` in either tree. Skill templates under `~/.claude/skills` do not contain it.
  The notes are: allocations, the four available_through_*, firm_available, firm_booked, firm_technical,
  gcv, hydrogen_content, the three interruptible_*, methane_content, nominations, oxygen_content,
  physical_flows, renominations and wobbe_index.

## Gates (final run, after all edits)

- `uv run --system-certs --extra build gridflow-build`: exit 0, 73 dataset pages, 149 datasets, 7 hubs and
  the landing.
- `... gridflow-build --check`: OK, idempotent across 73 pages and 7 hubs. 0 vault-relative `.md` links.
- `uv run --extra build pytest -x -q`: **139 passed**, including the blank-page test (polars stays installed
  under `--extra build`).
- `npx -y htmlhint "site/hifi/**/*.html"`: 184 files, no errors.
- `lychee --offline --no-progress site/hifi`: 144 total, 36 OK, 0 errors, 108 excluded.
- Detector (`.claude/skills/impeccable/scripts/detect.mjs --json`) on all 65 dataset pages with a chart or
  guide: **0 non-advisory findings**.
  - 22 pages carry the em-dash-overuse advisory. On `aggregated_physical_flows` it comes from CLI flags
    (54 `--flag`, 0 em or en dashes), which the ruling accepts. These pages are unchanged in copy.
- Em dashes in `site/hifi`: 0.
- `ruff check` on changed files: all pass except `build.py:1212` ISC004, which is **pre-existing on
  `origin/main`** and not in my change.
- `ruff format --check`: `chart_svg.py`, `test_chart_axis.py` and `test_sample_columns.py` would reformat.
  The same three files also fail on `origin/main`, and the remaining hunks are on lines I did not write.
  My two unformatted test lines were formatted.
- Port 9882 server stopped (curl returns 000). Port 9670 untouched. The scratch `site/hifi/_measure.html`
  was removed.

## For the seat

- The pre-existing ruff ISC004 and format drift in `chart_svg.py`, `build.py` and the two test files are
  worth a separate tidy.
- `elexon/ndf` and `elexon/uou2t14d` (live) now show dashed shared stretches. This is intended and honest,
  but it is a visible change on approved pages.
