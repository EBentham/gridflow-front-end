# Dataset page review rubric (v5 Phases 25b and 26)

Calibrated on the 25b pilot. The reviewer checks one dataset page objectively; taste is Bobbo's. A
same-family review is weak on taste, so do not grade look or wording style beyond the rules below.
Inputs: the dataset's canonical vault note (its `page:` block and any body edits), the committed
artefacts, the rendered page, the author's evidence table, and the sources of truth in
`author-brief.md`. Bash is for inspection only: read code, read silver with Polars, run the build
`--only`, run the detector. Never write any file other than your review, never run ingest or any live
API, never commit.

Verdict: **APPROVE** (no findings above nit) or **REVISE** with numbered findings, each with a
severity (blocker, major, nit), the field path (`page.chart_view.caption`), what is wrong, and the
evidence (file:line, or the Polars expression you ran and its output).

## 1. Facts (blocker if wrong)

- [ ] Every factual sentence in `summary`, `facts`, `what_it_is`, `how_used`, `chart_view` (caption,
      key notes, alt), `raw_feed.note`, `record.fields`, `record.caption`, `notebook.lead`, `related`
      notes and `family.members[].differs` is true against gridflow code, silver or the vendor docs
      quoted in the note. Re-derive at least: the grain and key (transformer dedup), each meaning of a
      derived column (`timestamp_utc`, `settlement_date`, `ingested_at`), sign conventions, units.
- [ ] `raw_feed.requests` is the URL the connector builds: host, path, parameter names and formats.
- [ ] `raw_feed.commands` are real CLI calls with the right `--start`/`--end` semantics: transform end
      inclusive; ingest end exclusive for time-window requests but fetched for one-call-per-date
      requests (read `client.py`); the ingest window covers `PARTITION_SOURCE_OFFSETS` and any period
      published before its settlement day starts.
- [ ] `notebook.lead` matches what `query()` does (relation, date column, inclusive ends, lineage
      columns dropped) or why `sql()` is used instead.
- [ ] Any "equal", "always", "never", "every row" claim is either a vendor or code rule with evidence,
      or is scoped to what the page shows ("in this window"). Measured-on-our-copy universals are not
      allowed (see 3).

## 2. Chart provenance (blocker if wrong)

- [ ] The committed series was distilled from the note's spec (`spec_origin: vault`, the build's
      digest check passes) and the staged spec for the dataset is gone.
- [ ] Title and caption state the dataset, unit, window and aggregation that the spec actually applies
      (read `chart`: filter, window, group_map, aggregation, time_bucket).
- [ ] The alt text and every number in a key note match the committed series (min, max, count).
- [ ] Palette: khaki only for the vendor code OTHER; codes the palette does not cover are unpainted
      hatches; a signed series is not clipped or folded into another group; no non-additive column is
      summed.

## 3. No local data (blocker)

- [ ] No "held locally", local row counts, local first/last dates, local gaps, local coverage, "our
      copy" statistics. History only as a vendor fact with evidence.
- [ ] Numbers are vendor facts, code facts, or visible in the chart, the eight rows or the notebook
      outputs.
- Grep the note's `page:` block and the rendered page for: `locally`, `held`, `our `, `since 20`,
  `rows`, `% of`, digits followed by `rows` or `days`.

## 4. Budgets and structure (the build enforces; confirm it ran)

- [ ] `gridflow-build --only <key>` succeeds (budgets, required fields, key entries per series, artefact
      digests, related pages resolve, no authored override).
- [ ] `detect.mjs --json` on the page returns `[]`.
- [ ] The eight rows are real (`generated_by: gridflow-sample`), the marked row shows the column that
      matters, and every schema column has a meaning.
- [ ] The notebook JSON was written by `scripts/run_notebooks.py`, every cell is read-only (no
      `refresh`, `backfill`, ingest), outputs have no errors, and `plot_alt` describes the real plot.

## 5. Nothing clipped or overlapping (major; look at rendered screenshots, not only the HTML)

- [ ] Nothing clipped or overlapping. Every drawing, label and caption is fully visible at 1440, 1024,
      768 and 390 in light and dark, in particular scenery tops (turbines), scene edges and
      section-corner labels.
- [ ] Take the screenshots yourself (a headless browser or your own preview tab on a free port) and
      look at each one: the hero scenery, the chart, the eight rows, the notebook panel and each
      stratum's corner label. A passing detector or HTML check does not replace looking.

## 6. Leakage and filler (major)

- [ ] No planning labels, phase codes, "coming soon", counts of future work.
- [ ] No filler captions (restating the heading, explaining an obvious method), no marketing words, no
      "live"/"now"/"real-time".
- [ ] No em dashes; no middle-dot strings; no "→".
- [ ] `related` notes say how the datasets relate, in 12 words or fewer.

## 7. Vault body edits (major)

- [ ] Each body correction the author made cites evidence and fixes the smallest span. No unrelated
      rewrites; the curl example is only changed if it is wrong for the vendor.

## Calibration notes from the pilot

- fuelhh: the vault claimed `ingested_at` is the bronze ingest time; the transformer stamps it at
  silver transform time. `timestamp_utc` comes from the vendor start instant, not the settlement
  label. These are the kind of stale body facts to expect.
- Interconnector sign: positive is import, measured by the project against demand, not stated by
  Elexon; the page must say that, not present it as a vendor rule.
- The gridflow_models help card says a dataset count that disagrees with `list_datasets()`; the page
  never states a count.
- The pilot reviews' majors were all overclaims: a unit stated from a project check (INDOD "MWh"),
  "every point" where the code only sends no filter (ENTSOG `meta.count` 984 against `meta.total`
  1650), and "the same flow" where two operators' reports differ by up to 0.2 GWh/d. Check every
  universal and every equality against the rows.
- Nits worth catching: undated snapshots of a register (date the capture the chart shows); "sends no
  field" versus "sends it as null"; "1 to 50" periods without the normal 48; notebook `needs` that
  disagree with the commands' window.
- Cost per page at list prices: author about $7 (range $6.36 to $7.67), Opus review about $3.30
  including one re-review.
