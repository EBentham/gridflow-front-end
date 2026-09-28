# fuelinst: review

Page `elexon/fuelinst`, "Five-minute generation by fuel type". Checked 2026-09-28 against
`review-rubric.md`.

## Verdict: APPROVE

Three nits and no blockers or majors. Every fact on the page was re-derived from gridflow code, local
silver and bronze (read only), or gridflow_models. The page is distinct from `fuelhh` where it counts:
- the chart is one GB day at five-minute grain, not a week of half-hours;
- the frame shows the doubled midnight instant;
- the lead prose is about publish-time keying and the duplicates;
- the notebook plots net interconnector flow, not wind;
- the raw-feed note is specific to FUELINST.

## The writer's three flags

1. **Publish time against the interval start.** The transformer maps `publishTime` and
   `publishDateTime` to `published_at`, which becomes `timestamp_utc` (`fuelinst.py:61-93`).
   `startTime` is only a fallback (`:94-100`). In local bronze, all 80,920 rows have
   `publishTime - startTime = 5m`. All 5,780 bronze rows in the chart's window (publish time
   > 19 Sep 23:00Z and <= 20 Sep 23:00Z) have `settlementDate = 2026-09-20`, with `startTime` from
   19 Sep 23:00Z to 20 Sep 22:55Z. So "GB day 20 September" is exactly what the chart shows. The page
   never states the five-minute offset as a rule. Sound.
2. **Midnight duplicates.**
   - Silver `fuelinst_20260919` spans 19 Sep 00:00Z to 20 Sep 00:00Z, and `_20260920` spans 20 Sep
     00:00Z to 21 Sep 00:00Z (5,780 rows each).
   - In the chart window there are 5,780 rows but 5,760 unique keys. The series provenance agrees:
     `duplicates_dropped 20`.
   - The two 00:00 `PS` rows are identical except `ingested_at` and `available_at` (.592271 and
     .653977).
   - The notebook's `query()` window (19 Sep 00:00Z to 21 Sep 00:00Z, half-open) returns 11,560 rows,
     11,520 of them unique: midnights 19 and 20 Sep are both doubled.
   - Code: the transformer dedups within one file only (`fuelinst.py:105`), fuelinst is exempt from the
     publication-window trim (`_publication_window.py:39-42`), and the boundary instant is written to
     both partitions (`partition_window.py:3-8`).
   - The grain "per daily file", the raw-feed note and "midnight duplicates stay" are all correct.
3. **The eight body corrections.** Each one cites a line that says what the edit says:
   - `ElexonFuelInst` at `schemas/elexon.py:87`, the `schema_cls` at `fuelinst.py:28`;
   - no `published_at` in `output_cols`, `:115-121`;
   - the `timestamp_utc` source, `:61-100`;
   - `ingested_at = datetime.now(UTC)`, `:107-112`;
   - the silver sample `03:00` follows from `publishTime` 03:00 under the code;
   - the known-issue bullets;
   - the implementation delta.

   The edits are the smallest spans, and the curl example and vendor table are untouched. The mirror
   is byte-identical to the vault note (`cmp` clean).

On the writer's "unverified" imports sign: FUELINST's INT and PS codes, averaged into half-hours
(`startTime` = publish time minus 5 min), agree in sign with FUELHH in 7,392 of 7,392 joined
half-hours (corr 0.99999, max diff 70 MW). The key note scopes the check to FUELHH, which is honest.
The data supports carrying it over.

## Findings

1. **nit** `page.chart_view.x_label`: "publish time, UTC; GB day starts 23:00 UTC" sits on an axis whose
   first point is 23:05. The caption says "published from 23:05", but nothing tells the reader why a
   day that starts at 23:00 begins at 23:05. Optional: name the 23:05 to 23:00 span as the publish
   times of GB day 20 September's intervals. Keep the offset out as a rule, since it is evidenced only
   by the vendor sample and data. Evidence: series `x[0] = 2026-09-19T23:05:00Z`,
   `x[-1] = 2026-09-20T23:00:00Z`.
2. **nit** `page.how_used[1]` and `[2]`: "Net interconnector flow by link, from the signed interconnector
   codes." is word for word `fuelhh`'s `how_used[1]`. "Checking a wind generation forecast against
   five-minute outturn." is `fuelhh`'s `how_used[2]` plus one word. Only `[0]` says what five-minute
   grain adds. Rewording these two around five-minute use (ramps, within-period imbalance) would sharpen
   the difference from the sibling page. Evidence: `vault/elexon/fuelhh.md`, the `page.how_used`
   block.
3. **nit** Vault body, silver section, "Point-in-time field: none in silver". Silver still carries the
   lineage `available_at`. Its rule is `coalesce(published_at, ingest_time)` (`silver/base.py:87`), and
   the transformer drops `published_at`, so here it is the ingest-side stamp, not the vendor publish
   time. The line is not wrong, since there is no vendor point-in-time column. It could add that
   `available_at` falls back to ingest time for this reason (the "F-08-class" note at
   `_publication_window.py:39-42`).

## Rubric checks that passed (evidence)

- **Facts.**
  - Key `(timestamp_utc, fuel_type)`: `fuelinst.py:29,105`.
  - The `timestamp_utc` and `ingested_at` meanings are as above.
  - Unit MW: `generation` becomes `generation_mw`.
  - There is no settlement date or period in silver: the silver schema is `timestamp_utc`, `fuel_type`,
    `generation_mw`, `data_provider`, `ingested_at` plus the four lineage columns.
  - "Coal and oil 0 MW at every instant here": series `coal_oil` min = max = 0.0.
  - The related note on `fuelhh`, "the same codes": the code sets match, except one `INTELE` in local
    fuelhh on 10 Sep 2021, which lies outside local fuelinst coverage. That is a coverage difference,
    not a code difference.
- **Requests.**
  - Path `/datasets/FUELINST`, `PUBLISH_DATETIME` with the default `publishDateTimeFrom/To` params:
    `endpoints.py:116-120`.
  - `%Y-%m-%dT%H:%M:%SZ` format: `_to_utc_z`. `page`: `build_params`. 24-h chunks:
    `endpoints.py:40`, `client.py:93-99`.
  - The bronze sidecar `2026/09/20/*.meta.json` records exactly the second request (URL-encoded).
- **Commands.**
  - Ingest `--end` is exclusive: `client.py` `while current < end`, and a bare date is midnight UTC
    (`runner.py` `resolve_dates`). The ingest 19 to 21 Sep fetches bronze 19 and 20, which is what
    silver 19 and 20 need. There are no offsets.
  - Transform `--end` is inclusive: `runner.py:1136` `date_range(start_dt.date(), end_dt.date())`.
- **Notebook lead.**
  - Relation `silver_elexon_fuelinst`, filtered on `timestamp_utc >= start 00:00Z AND < end+1 00:00Z`:
    `_date_range_predicate`.
  - "Lineage columns go": `BITEMPORAL_EXCLUDE` covers `event_time`, `available_at`, `source_run_id`
    and `dataset_version` (gridflow `schema_manifest.py:76-84`).
  - "Duplicates stay" was measured above.
- **Chart provenance.**
  - `spec_origin: vault`. No staged spec or authored override exists.
  - The build digest check passed: `gridflow-build --only elexon/fuelinst` wrote the page at 22:06
    with no content errors. The first attempt at 22:00 failed on another writer's `agws` note; the
    retry was clean.
  - The alt text matches the committed series:
    - nuclear 3,321 to 3,346;
    - gas 2,324 to 9,165 (18:30);
    - wind max 16,176 (19 Sep 23:55), min 5,413 (19:05);
    - imports -6,343 (04:20) to 6,023 (16:10), one sign change at 14:05.
  - The plot_alt matches silver:
    - 19 Sep 00:00 to 06:00 net INT has a median of -5,507 and a min of -5,623 (01:55);
    - 1,201 at 19:45;
    - -6,343 and 6,023 as above.
  - Palette: khaki only on `OTHER`. `PS`, `COAL`/`OIL` and `NPSHYD` are unpainted hatches. Signed
    series are stacked, not clipped. Nothing non-additive is summed.
- **No local data.**
  - Grepped the `page:` block and the rendered text for `locally`, `held`, `our `, `since 20`, `rows`,
    `% of`, `live`, `now`, em dash, middle dot and `→`.
  - The only hits are "24-hour" and template or help-card text.
- **Structure.**
  - The detector returns `[]` on the rebuilt page.
  - The sample has `generated_by: gridflow-sample`, 8 real rows that match silver.
  - The notebook has `generated_by: scripts/run_notebooks.py`, read-only cells and no error outputs.
    The PNG shows the described line.
- **Related.** The three notes are 12 words or fewer and say how the datasets relate.

## Screenshots

Headless Chrome over CDP, with a static server on 9718 (stopped). The page was rebuilt after the
template fixes (`3e51d6b`, `a0e18d9`). Captures are full-page at 1440, 1024, 768 and 390, in two
states: default, then frame unfolded plus notebook opened. 390 used true device emulation
(`setDeviceMetricsOverride`, `mobile: true`), not a wide window.

Every crop was viewed:
- `scrollWidth` equals the viewport at all widths;
- no element runs off-page outside a scroll box;
- no clipped text;
- turbine tops, scene edges and stratum corner labels are fully visible.

At 390 the narrow chart's `−10,000` and `MW` labels sit 2 to 3 px outside the SVG viewBox. `.chart` is
`overflow: visible` (`theme.css:571`) and a zoomed crop shows them rendered whole, so no finding.

There is no dark theme: no `prefers-color-scheme` or `data-theme` in `site/hifi/assets/`. Light is the
only mode.

Template observations, not findings against this page:
- At 390 the unfolded frame and the notebook's `.head()` table scroll inside their own boxes, so
  `generation_mw` is off-screen until scrolled.
- Code cells wrap mid-identifier (`timestamp_ut` / `c`).

One capture-harness hiccup: two reruns at 390 stalled on the external font stylesheet before `site.js`
loaded. The final run waited for `readyState === complete` and matched the first run's page heights.

## Process notes

- Wrote a CDP capture script and PNGs under the scratchpad only (`scratchpad/fi-review/`). No file in
  either worktree was edited.
- Beyond the mandated vault `git diff`, I ran read-only `git log` and `git status` in the front-end
  worktree to confirm the template-fix commits were present.
- No ingest, no live API, no commits.
