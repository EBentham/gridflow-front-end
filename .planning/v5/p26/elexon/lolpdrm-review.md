# lolpdrm: checker review (2026-09-29)

**Verdict: REVISE** (1 major, 2 nits). The page itself is sound: every page field, number and command checks
out against code, silver and bronze. The major is a wrong code fact in a vault body edit, a one-phrase fix.

Inputs: canonical note (`vault-p26-elexon/30-vendors/elexon/datasets/lolpdrm.md`, diff against `origin/master`),
mirror `p26-elexon/vault/elexon/lolpdrm.md` (`cmp` identical), artefacts under
`p26-elexon/site/hifi/data/{series,samples,notebooks}/elexon/lolpdrm*`, built page, author report.

## Findings

### 1. major: vault body, Known issues, new bullet "Silver keeps one publish per period per bronze day"

**What is wrong.** The bullet says the transformer reads the day's two bronze files "in file-name order (random
suffix)". The suffix is not random. It is the first 8 hex digits of the SHA-256 of the response body, after the
fetch timestamp: `bronze/writer.py:33` `body_hash = hashlib.sha256(response.body).hexdigest()[:8]`, `:34`
`ts = response.fetched_at.strftime(...)`, `:57` `filename = f"raw_{ts}_{body_hash}.{ext}"`. So the read order is
set by fetch second and then body hash. It does not follow publish time, but it is deterministic for the same
bronze files. The cited evidence (`lolpdrm.py:42`, `sorted(glob("raw_*.json"))`) shows only that the files are
sorted by name, not that the names are random. The author report goes further ("a re-transform can keep different
publishes on different machines"). That is false for identical bronze and should not go into the proposed
gridflow issue. The order can differ only between separate ingests (a new fetch time and body).

**Fix.** Change "(random suffix)" to something like "(fetch time, then a hash of the body, so unrelated to publish
time)". Cite `bronze/writer.py:33,57`. Re-copy the mirror. The rest of the bullet is correct (see "Verified" below).

### 2. nit: `page.summary`, "Elexon's forecast"

Nothing in the repo or vault says who computes LOLP and de-rated margin. The vault body calls the dataset "Elexon"
and the endpoint is BMRS, but nothing evidences that Elexon makes the forecast (grep of `30-vendors/` for
NESO, National Grid or system operator near LOLP or de-rated: no match). "Elexon's" claims authorship where the
evidence supports only publication. It is rated a nit, below the pilot's overclaim majors (a unit or a universal
stated without evidence). Here the publisher is named as the author, which changes no number, unit or structural
claim, and the vendor fact "Elexon BMRS, dataset LOLPDRM" is correct. Suggested wording: "Forecast, per settlement period, of loss-of-load
probability and de-rated margin, published on BMRS and republished as each period draws nearer."

### 3. nit: `page.facts.cadence`, "Repeated through the day; each publish names its half-hour publishing period"

This rests on the feed, not on a vendor document (none is quoted in the note; the report says so). The wording
has no count or horizon, and every observed day agrees. Bronze for all 14 local days has 37 to 48 distinct
`publishTime` per day, and every record carries `publishingPeriodCommencingTime` on :00 or :30 (0 nulls, a
Polars scan of each day's `raw_*.json`). 2026-09-15 has one publish per half-hour, each tagged with that
half-hour. The page also shows two publishes on the 13th (notebook `[4]` 00:06:57, chart 12:04). So it passes as
feed structure, not a local statistic. Two small points:
- the field the fact relies on is not visible anywhere on the page: the transformer renames and then drops it
  (`lolpdrm.py:65,130-139`);
- "half-hour" is observed, not documented.

Optional: "Republished through the day; each publish carries its `publishingPeriodCommencingTime`". Or keep
it as is and add a vendor source to the note body when one is re-checked.

## Verified (no finding)

**Key and grain (focus 1).**
- `transform()` dedups on `(settlement_date, settlement_period)` with `keep="last"` (`lolpdrm.py:120`). It runs
  over one bronze day: `read_bronze(target_date)` (`:31-55`), the plain branch of `base.py` `run()` (lolpdrm sets
  neither `VINTAGE_PER_BRONZE_FILE` nor `LOCKSTEP_BRONZE_READ`), `PARTITION_SOURCE_OFFSETS = (0,)`
  (`base.py:417`).
- `_process_frame` does no further dedup (`base.py:1614-1642`). It applies the Elexon publication-window filter
  on `published_at`, because lolpdrm is in scope (`_publication_window.py:94-114`, not in
  `PUBLICATION_WINDOW_EXEMPT`).
- Each day writes one file, `lolpdrm_YYYYMMDD.parquet`, overwritten per run (`base.py:2610-2639`).
- Silver, all 14 files: within each file, 0 duplicate `(date, period)`. Across the union of 1,428 rows, 0
  duplicate `(date, period, published_at)`. Every file holds exactly two publishes: 24 + 78 rows normally, 54 +
  48 where the file order flips (08-02, 08-05, 09-19).
- The code guarantees the key. Dedup makes `(date, period)` unique within a partition, and the
  publication-window filter keeps only publishes from that bronze day's own request window. So one
  `published_at` cannot occur in two partitions, and `(date, period, published_at)` is unique across the table.
  The silver counts above only confirm this rule; they are not the basis for it.
- The page's three-column key and "One row per settlement period from each day's publishes" are therefore true.
  The class's `ENTITY_KEY_COLUMNS` is only `(date, period)` (`:26-29`), which identifies a row within one
  partition only. The page's key is the right one for the table.

**Cadence (focus 2).** See finding 3. The Publication lag edit in the note body is dated and scoped ("Observed in
bronze for publishes of 2026-09-15 ... Vendor docs not re-checked"). On 09-15 there are 48 publishes, the
00:04 publish starts at 01:00, and the 11:34 publish reaches 03:30 on the 17th (about 40 h).

**Chart (focus 3).**
- The committed series has `spec_origin: vault`. `rows_matched = rows_used = 234`. There are three series of 78
  points each. `pub_13` runs 13:00 on the 13th to 03:30 on the 15th, `pub_14` 13:00 on the 14th to 03:30 on the
  16th, and `pub_15` 13:00 on the 15th to 03:30 on the 17th.
- The caption's "runs to 03:30 two days on" and "periods from 13:00 on the 14th and 15th appear twice" are true.
  Each overlap covers 30 points.
- Alt lows: 4,998.457 at 16:30 on the 13th, 8,388.98 at 17:30 on the 14th, 7,772.727 at 16:30 on the 16th. Max
  26,302.14 at 02:30 on the 17th. 10,138.974 - 8,388.98 = 1,749.99; 13,130.808 - 11,384.242 = 1,746.57. All
  match, and so do both key notes ("a day earlier" = the previous noon publish).
- Palette: clay, petrol and horizon are line paints, so the palette rule holds. There is no staged spec or
  authored override for lolpdrm.

**Other page fields.**
- `raw_feed.requests` match the bronze sidecar `request_params` for 2026-09-15: publishDateTimeFrom, publishDateTimeTo
  and `page=1`, in that order. The request is 12 h (`max_chunk_hours=12`, `endpoints.py:220-229`). The sidecar
  URL encodes `:` as `%3A`, which is equivalent.
- `raw_feed.commands`: `resolve_dates` treats a bare date as midnight UTC. The connector uses `while current < end`
  (`client.py:94-99`), so ingest 13 to 16 exclusive gives bronze days 13 to 15. The transform end is inclusive.
  `data_date = start.date()` (`client.py:314`), which supports "a day's bronze holds that day's publishes" for the
  midnight-aligned window shown.
- `record.fields` match the code (`lolpdrm.py:61-67,93-111`, schema `elexon.py:711-726`), including "the schema
  expects 0 to 1" (fail-soft validation). The eight rows are `generated_by: gridflow-sample`: periods 37 to 40
  on 14 Sep, two publishes each. LOLP is at most 0.0000044.
- `notebook.lead`: `query()` does `SELECT *{exclude} FROM silver_elexon_lolpdrm WHERE <date predicate> ORDER BY
  settlement_date` (gridflow_models `research/handles/source.py:401-450`). lolpdrm has no `_latest` view
  (`latest_views.py:94+` lists only system_prices, remit and fou2t14d), so nothing de-duplicates.
- The notebook JSON is `generated_by: scripts/run_notebooks.py`, with read-only cells and no errors.
- `plot_alt` matches `lolpdrm-5.png` and silver. There are six publishes; the 00:0x lines stop at 12:30. Lows
  are 4,998 (evening of the 13th) and 7,773 (16th); the max is 26,302 early on the 17th.
- `related`: windfor is hourly in silver (every `timestamp_utc` step is 1 h) and melngc is per settlement
  period. Every note is 12 words or fewer.

**Other vault body edits.**
- The `ingested_at` edit matches `lolpdrm.py:122-126`.
- The silver sample fix (SP10 on 2026-05-07 is 03:30 UTC) is correct.
- The dedup-key scope edit is correct.
- The rest of the Known-issues bullet is correct:
  - bronze rows arrive newest first;
  - the survivor is the earliest publish carrying the period in the last-read file;
  - the flip pattern (00:04 plus 11:04) matches;
  - `startTime` equals the derived `timestamp_utc`: 0 mismatches in 7,643 bronze records for 09-13, 09-15
    and 09-19.
- The curl example is untouched.

**No local data, leakage or filler.**
- A grep of the rendered page text for locally, held, "our ", "since 20", rows, "% of", "N rows/days", em dash,
  middle dot, arrow, live, now, real-time, latest, day-ahead, always, never and every found no hits except the
  template's `data.elexon` help card and the `shape:` line.
- The local statistics ("48 publishes", "2026-09-13 to 2026-09-18") appear only in the vault body. They are
  dated and scoped, and they do not render.

**Build and detector.** `gridflow-build --only elexon/lolpdrm` wrote the page ("dataset template", one
distilled series). `detect.mjs --json` returned `[]`.

**Rendered checks (my screenshots, port 9737, stopped).**
- Setup:
  - headless Chrome, full page at 1440, 1024 and 768, notebook closed;
  - notebook open with the frame unfolded at 1024 and 768;
  - a true 390 (a 390 px same-origin iframe served from memory, stepped through the page), closed and open plus
    unfolded.
- Nothing is clipped or overlapping: hero scenery (turbine tops, offshore edge), chart ticks through "17 Sep",
  key notes, stratum corner labels, code blocks, guide and notebook.
- The page does not scroll sideways at 390 (`scrollWidth` 390 in both states).
- The unfolded frame and the notebook `head()` scroll inside their own boxes (template behaviour).
- The site has no dark theme (no `prefers-color-scheme` or `data-theme` in `site/hifi/assets/`), so there was
  no dark mode to check.

## Seat notes (template, not this page)

- At 768 and 390 the fold rule hides `published_at` behind `…`. It is a key column (marked with a square), so
  the square-marked key is only two-thirds visible while folded. Consider keeping key columns out of the fold.
- Petrol and horizon are close where `pub_14` and `pub_15` overlap. This is a taste call, already raised by the
  author.
