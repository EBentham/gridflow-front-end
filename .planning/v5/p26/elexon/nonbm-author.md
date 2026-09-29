# nonbm: author report (writer, 2026-09-29)

**Status: page block written, notebook executed, build BLOCKED on the eight-row rule.**
`gridflow-sample --dataset elexon/nonbm --dry-run` gives `FAIL elexon/nonbm: select picks 5 rows; it must pick
exactly 8`, because local silver holds only five rows for NONBM, all copies of one record. `gridflow-build --only elexon/nonbm`
then fails with one error: `elexon/nonbm: no sample rows (run gridflow-sample and commit them)`. Every other check passes:
anatomy, word budgets, the `none` chart spec, related links and the notebook digest. No HTML is written in the shared worktree.
`site/hifi/data-sources/elexon/nonbm.html` there is an older render; I did not touch it.

**Recommended ruling for the seat:** hold nonbm out of the batch PR, as netbsad is held, until two things happen:
- the sampler accepts a table whose silver has fewer than eight rows: pick all of them when `select` matches everything silver
  holds, or add an explicit `rows:` count to `record.select`;
- a gridflow research unit settles the parameter question below.

Yes to both. Without them the page can only ship blank.

## What NONBM holds, and why coverage is so thin

- **One record, repeated five times.** Silver has five rows in five files, `year=2026/month=08/nonbm_20260801.parquet` to
  `nonbm_20260805.parquet`. Every row is settlement date 2026-04-01, period 22, `generation_mw` 0.0, `published_at`
  2026-04-01 10:04 UTC. Only `ingested_at` differs, by milliseconds on 2026-08-16.
- **The bronze bodies are byte-identical.** Every file is
  `{"data":[{"dataset":"NONBM","publishTime":"2026-04-01T10:04:00Z","startTime":"2026-04-01T09:30:00Z","settlementDate":"2026-04-01","settlementPeriod":22,"generation":0}]}`,
  `body_sha256` `123a943b…`. The requests behind them:
  - `C:\gridflow-data\bronze\elexon\nonbm\2026\08\01..05`: windows 1 to 5 August 2026;
  - gridflow `.tmp/validation-7day-20260511/.../nonbm/2026/05/04..10`: windows 4 to 10 May 2026;
  - the vault's own live curl of 2026-05-08: window 2026-05-06.

  That is 13 disjoint publish windows, all returning a record published outside the window.
- **Diagnosis: a connector gap first; vendor sparsity is possible but unproven.**
  - Gap: gridflow sends `publishDateTimeFrom`/`publishDateTimeTo` (`endpoints.py:194-197`, default `from_param`/`to_param`
    at `endpoints.py:35-36`). The vault's parameter table and gridflow's validation note (`elexon-VALIDATION.md:333`,
    "Swagger declares `/datasets/NONBM` parameters as `from`/`to`") name `from`/`to`.
  - The same vendor behaviour is recorded in code for FREQ: sending `publishDateTimeFrom/To` "causes the API to silently
    ignore the window and return the latest" samples (`endpoints.py:100-103`).
  - DISBSAD, NETBSAD, MID and BOAL were all switched to `from`/`to` (`endpoints.py:65-92`). NONBM was not.
  - So every window returned what looks like Elexon's latest NONBM publication.
  - That latest publication was still the 1 April 2026 record on 10 May and on 16 August 2026. So either Elexon publishes
    NONBM very rarely, or it has not published since 1 April 2026. Local evidence cannot tell these apart. I did not guess,
    and the page says it is not established.
- **The repeats are a silver trait.** Bronze is filed under the window start date (`client.py:314`,
  `data_date = start.date()`). The transformer reads one such day (`nonbm.py:31-37`) and dedups within it only
  (`nonbm.py:112`). A record returned by several windows therefore lands once per file.

## Page choices

- **Chart: `type: none`.** One distinct point cannot support a chart, and `reason` records why. The template renders no
  figure for `none`, and `reason` is not rendered anywhere (`build.py:1723`, `dataset.html.j2:74`). So the coverage
  statement lives in `what_it_is`, and the parameter fact lives in `raw_feed.note`.
- **Frame:**
  - `select` picks settlement date 2026-04-01, period 22: all five rows, ordered by `ingested_at`.
  - `columns` puts the key, `generation_mw`, `published_at` and `ingested_at` first.
  - `ingested_at` is a pipeline column, so it folds; it shows when the frame is unfolded.
  - The caption says the rows are one Elexon record repeated per window file.
- **Notebook:** three cells:
  - `query("nonbm", "2026-04-01", "2026-04-01")`;
  - the key, value, `published_at` and `ingested_at` (five identical keys);
  - `drop_duplicates` on the key (one row).

  There is no plot, because one repeated point would suggest a trend that isn't there. `needs` is the 1 to 5 August windows,
  matching the commands, and the lead explains why the query dates (April) differ from them.
- **Commands:**
  - `ingest --start 2026-08-01 --end 2026-08-06`: the loop is `while current < end` (`client.py:94-99`), so the end is
    exclusive and there are five 24-hour windows;
  - `transform --start 2026-08-01 --end 2026-08-05`: the end date is inclusive (`runner.py:1125-1138`).

  The request URL is copied from the 2026-08-01 bronze `.meta.json` `request_url` (decoded).

## Evidence table

| Claim (field) | Evidence |
|---|---|
| NONBM is non-BM STOR generation (summary, what_it_is) | `schemas/elexon.py:634-639` "Half-hourly generation from non-BM Short-Term Operating Reserve (STOR) providers"; `endpoints.py:196` "Non-BM STOR Generation" |
| No provider or unit column (facts.grain, what_it_is) | `nonbm.py:122-130` output columns; bronze body has no unit or provider field |
| Key `(settlement_date, settlement_period)` (record.key) | `nonbm.py:26-29` `ENTITY_KEY_COLUMNS`; `nonbm.py:112` `unique(subset=[...])` |
| Cadence not established; 24-hour windows (facts.cadence) | No vendor cadence quote in the note or code (so the page says "not established", not "not stated by Elexon"); `endpoints.py:40` `max_chunk_hours: int = 24`; `config/sources.yaml:104-107` `schedule: "daily"` |
| Every window requested in May and August 2026 returned the same record (what_it_is, chart.reason) | 12 gridflow bronze bodies (5 local, 7 in `.tmp/validation-7day-20260511`), all `123a943b…`, request windows 2026-05-04..10 and 2026-08-01..05 in `.meta.json` |
| API reference lists `from`/`to` (raw_feed.note) | Vault note parameter table (lines "`from` ... The start of the data publish time window"); gridflow `elexon-VALIDATION.md:333` |
| Publish window did not filter (raw_feed.note) | `publishTime` 2026-04-01T10:04Z lies outside each requested window; FREQ precedent `endpoints.py:100-103` |
| Request URL (raw_feed.requests) | `bronze/elexon/nonbm/2026/08/01/*.meta.json` `request_url`; `build_params` `endpoints.py:280-311`, `_to_utc_z` `%Y-%m-%dT%H:%M:%SZ` |
| Ingest end exclusive, transform end inclusive (commands) | `client.py:94-99` `while current < end`; `runner.py:1126` "date taken, inclusive"; `runner.py:497-500` bare date = midnight UTC |
| One silver file per window date (command comment, caption) | `client.py:314` `data_date = start.date()`; `nonbm.py:31-37` reads `bronze/<y>/<m>/<d>` for the target date |
| `settlement_date` from `settlementDate` (fields) | `nonbm.py:62,79` |
| Period 1 to 48, 46 or 50 on clock-change days (fields) | `schemas/elexon.py:642` `Field(ge=1, le=50)`; GB settlement convention (same wording as approved disbsad and fuelhh) |
| `generation_mw` from `generation` as float; MW by name only (fields) | `nonbm.py:65,81`; the response carries no unit field |
| `published_at` from `publishTime` (fields) | `nonbm.py:64,98-103` |
| `timestamp_utc` computed from date and period; `startTime` dropped (fields) | `nonbm.py:85-94` `settlement_period_to_utc`; `startTime` not in `output_cols` (`nonbm.py:122-130`); silver 09:30 UTC matches vendor `startTime` |
| `query()` relation, date column, inclusive ends, lineage dropped (notebook.lead) | `gridflow_models/research/handles/source.py:401-451`; `schema_manifest.py:135` `("elexon","nonbm"): "settlement_date"`; no `VINTAGE_POLICY`, no `_latest` view; `bitemporal_exclude()` = `event_time, available_at, vintage_policy, source_run_id, dataset_version, month, year` (so `ingested_at` stays) |
| Notebook outputs | `site/hifi/data/notebooks/elexon/nonbm.json` (runner 2026-09-29T11:34Z): 5 rows then 1 row after `drop_duplicates`, no errors |
| DISBSAD flags STOR providers with `stor_flag` (related) | `vault/elexon/disbsad.md` approved page fields: `stor_flag` "STOR provider flag" |
| Non-BM STOR runs outside BM acceptances (related, boal) | Definition in the schema docstring ("non-BM") and `endpoints.py:196` |

## Note-body corrections (vault note, mirrored byte for byte)

1. **Silver schema, `ingested_at`.** Was "Time ingested into bronze." Now "When the silver transform ran, not the bronze
   fetch (`silver/elexon/nonbm.py:114-118`)". This is the stale fact from the fuelhh calibration.
2. **Silver sample, `timestamp_utc`.** Was `2026-04-01T10:30:00+00:00`. Now `09:30:00+00:00`: period 22 in BST starts at
   09:30 UTC, as silver and the vendor's `startTime` both show.
3. **Implementation delta, "Param style mismatch".** The claim "the API may accept both" was not supported. It now records
   what was observed:
   - the returned `publishTime` lies outside the requested window;
   - 12 more windows returned the same `body_sha256`;
   - the FREQ precedent (`endpoints.py:100-103`).

   "Worth verifying" is kept. The curl example is unchanged, because no A/B test exists.
4. **Known issues.** Added one bullet: the record repeats across silver day files, with `client.py:314`, `nonbm.py:31-37`
   and `nonbm.py:112`. It advises dropping repeats on the key after `query()`.

## Could not verify

- **Whether `/datasets/NONBM` honours `from`/`to`.** It is not tested, and no Swagger is vendored in gridflow. My only
  source for "API reference lists `from` and `to`" is the vault table plus `elexon-VALIDATION.md:333`.
- **Whether Elexon publishes NONBM only on dispatch, half-hourly, or has stopped since 2026-04-01.** No vendor quote exists.
  The page says "not established".
- **The MW unit.** It rests on gridflow's column name, not on a vendor quote, and the field says so.
- **The sign of `generation`.** Only 0 has been seen, so the page says nothing about sign.
- **Other body claims left as they are, without evidence:**
  - "Historical depth: Several years";
  - "Publication lag: Half-hourly";
  - the Overview line "NONBM is what supplements BM-unit dispatch in periods of system stress".

  I did not rewrite them, for lack of a source.

## Open questions (for a gridflow research unit, with no live call made here)

1. Run an A/B on `/datasets/NONBM`: `from`/`to` against `publishDateTimeFrom`/`To` over a window that includes
   2026-04-01T10:04Z, and over a recent week. Does `from`/`to` filter? Is anything published after 1 April 2026?
2. If `from`/`to` filters, switch `endpoints.py` `nonbm` to `from_param="from", to_param="to"`, as DISBSAD, NETBSAD, MID and
   BOAL were. Then re-ingest and rewrite this page's commands, request and notebook window.
3. Is there a `/datasets/NONBM/stream` variant for backfill?
4. If NONBM turns out to be dormant, should the page stay, with the coverage sentence, or be dropped from `elexon.json`?

## Edge items for the checker

- **`what_it_is`, "Every publish window gridflow requested in May and August 2026 returned the same single record".** This
  is near the no-local-data line. It describes dated vendor responses (12 identical `body_sha256`), in the same shape as
  bmunits' "the register as fetched on 26 September 2026". The task asked for coverage in domain terms. It does not
  describe holdings: there is no row count and no local first or last date.
- **`raw_feed.note`, "Elexon's API reference lists `from` and `to`".** It rests on the vault table and
  `elexon-VALIDATION.md:333`, not on a Swagger file I read.
- **`how_used[0]`, "Adding non-BM reserve output to BM-metered generation".** This assumes NONBM is not already inside
  FUELHH's metered totals, which is unverified either way.

## Template and tooling problems (the seat's)

1. **`sample.py:109` hard-requires exactly eight rows.** A table whose silver has fewer can never pass, and the build
   requires the sample (`build.py:1024`). This is the blocker.
2. **A `none` chart's `reason` is not rendered anywhere.** The words have to live in `what_it_is`. That is fine, but the
   `chart_spec.py` docstring suggests `reason` is visible.

## Visual check (scratch preview only; nothing in the shared worktree)

I rendered the page in an isolated copy at `<scratch>/nonbm-preview`, with its own `src` on `PYTHONPATH` and the sampler's
`ROWS` patched to 5 there only. The shared worktree has no nonbm sample file (checked).

To reproduce it (Git Bash; `S` is the scratchpad root, `W=$S/p26-elexon`, `P=$S/nonbm-preview`):

```
mkdir -p "$P/site" && cp -r "$W/src" "$W/templates" "$W/vault" "$P/" && cp -r "$W/site/hifi" "$P/site/"
cd "$P" && PYTHONPATH="$P/src" PYTHONIOENCODING=utf-8 "$W/.venv/Scripts/python.exe" -c "import gridflow_front_end.sample as s; s.ROWS = 5; s.main(['--dataset','elexon/nonbm'])"
cd "$P" && PYTHONPATH="$P/src" PYTHONIOENCODING=utf-8 "$W/.venv/Scripts/python.exe" -m gridflow_front_end.build --only elexon/nonbm
```

`gridflow_front_end.paths.REPO_ROOT` resolves from the package file, so the copy writes only under `$P`. First re-copy the
vault mirror into `$P/vault` if the note has changed. `$P/site/hifi/shot.html?w=<width>&y=<scroll>&open=1` frames the page
at a set width and scroll position for headless Chrome.

- The detector returns `[]` on the preview page.
- I took headless Chrome screenshots at 1440, 1024, 768 and 390 (390 inside a 390 px iframe), in `<scratch>/nonbm-shots/`.
  Hero scenery, turbine tops, strata corner labels, raw feed, frame (folded and unfolded), guide, notebook and related
  links are all fully visible. Nothing is clipped or overlapping.
- At 390 the unfolded frame scrolls inside its box, exactly as approved fuelhh does. There is no page-level horizontal
  overflow: `scrollWidth` 375 for both.
- The site defines no dark theme (no `prefers-color-scheme` or `data-theme` rules in `tokens.css`, `theme.css` or
  `site.js`), so light and dark render the same.

## Files touched

- Vault note: `<scratch>/vault-p26-elexon/30-vendors/elexon/datasets/nonbm.md`: `page:` block plus four body edits; CRLF
  kept.
- Mirror: `<scratch>/p26-elexon/vault/elexon/nonbm.md`: plain `cp`, byte-identical (`cmp` passed).
- `<scratch>/p26-elexon/site/hifi/data/notebooks/elexon/nonbm.json`, from `scripts/run_notebooks.py`.
- There is no series file (a `none` chart) and no sample file (blocked). No staged spec or authored override existed.
