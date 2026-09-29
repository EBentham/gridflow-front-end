# elexon/fou2t14d: checker review

Checker: Opus 5.5, 2026-09-29. Inputs: vault note diff (`git diff origin/master`, vault worktree), mirror
(`cmp` identical), committed series, sample and notebook artefacts, the built page, gridflow code, local silver
and bronze (read only), and the Elexon OpenAPI (`scratchpad/swagger.json`).

## Verdict: APPROVE

One nit and no findings above it. The three points the brief flagged are all sound.

## Findings

1. **nit**, `page.record.select.columns` and `page.record.select.filter`, the frame at 390 px folded.
   - **What is wrong.** Only `output_usable_mw` fits before the `…` fold, so rows 4 to 7 all read `12402.0`, with
     no column to tell them apart. On a page whose point is "every publish kept", four identical visible rows
     can read as duplicates.
   - **Evidence.** Screenshot `scratchpad/fou-review/r2-silver-390-0.png`. Unfolded
     (`r2-silver-390-1.png`), and at 1440 folded (`r2-silver-1440-0.png`), `published_at` separates every row. The
     caption names the eight hourly publishes, 08:00 to 15:00, so the order can be recovered.
   - **Suggested fix.** No change is required, since any hourly run of this dataset repeats values between
     publishes. This is a taste call for the seat: keep it, or lead with `published_at` and let the value fold at
     390.

## What was checked (all pass)

### 1. The "end instant is included" ingest claim, and the notebook's 22 Sep 00:00 publish

- **Code.** `partition_window.py:104-111` declares `IntervalSemantics.CLOSED` for Elexon
  `publishDateTimeFrom`/`To`. `base.py:324` puts `elexon` in `_PUBLICATION_WINDOW_FILTER_SOURCES`.
- **The connector.** `client.py` builds `PUBLISH_DATETIME` chunks with `while current < end`, so
  `--end 2026-09-22` stops at a last chunk of 21T00:00Z to 22T00:00Z.
- **Bronze.** In `2026/09/21/raw_20260926T183344Z_c83ccbca.json`, the meta shows that exact window. The body
  holds 25 distinct `publishTime`s, from `2026-09-21T00:00:00Z` to `2026-09-22T00:00:00Z`, with 247 rows at
  the end instant. The comment "the end instant is included" is therefore a vendor-and-code fact.
- **Silver.** All 247 rows of the 22 Sep 00:00 publish sit in `fou2t14d_20260921_run...parquet`, delivery
  24 Sep to 6 Oct. There is no bronze partition for 22 Sep.
  - With no bronze for the 22nd, the upper-bound trim in `filter_frame_to_window` cannot prove neighbour
    ownership, so the row is retained.
  - A reader who runs ingest 19 to 22 and transform 19 to 21 gets the same result.
- **The notebook query.** A latest-per-key pass over 24 Sep to 6 Oct resolves to exactly one publish,
  2026-09-22 00:00 UTC. 24 Sep is D+2 and 6 Oct is D+14 from the 22nd, so every requested delivery date has that
  publish. The notebook's use of it is sound, and `needs` matches the commands.

### 2. The chart

- **Series.** `series/elexon/fou2t14d.json` has `spec_origin: vault`, `aggregation: last`, a fixed window of
  19 to 21 Sep, 216 rows used and 3 series of 72 points. No staged spec or authored override exists.
- **Values, re-derived from silver.** Filter: `settlement_date == 2026-09-24`, the three fuels, and
  `published_at` from 19 Sep 00:00 up to (not including) 22 Sep 00:00. Result: 72 publishes per fuel, one row
  each.
  - CCGT runs 19,161 to 21,099. It changes 21,011 → 21,099 at 20 Sep 00:00, → 21,039 at 08:00, → 20,324 at
    21:00, alternates 20,271/20,324, then falls 19,961, 19,561, 19,161 over 21 Sep 14:00 to 16:00.
  - WIND runs 10,524 (20 Sep 09:00) to 12,504 (15:00), with 12,442 at 10:00 and a last value of 11,606.
  - NUCLEAR is 3,570, then 4,210 from 20 Sep 21:00.
  - The alt text and the nuclear key note match all of these.
- **Nothing summed.** `last` over a key that is unique per `(settlement_date, fuel_type, published_at)`: silver
  has 0 duplicate keys, and the dedup is at `fou2t14d.py:175-179`. Fuels are separate lines.
- **The caption does not overclaim.** It states the dataset, MW, the publish window and the delivery date, and
  says "Forecasts, not outturn".
- **Unit and meaning are sourced.** The OpenAPI row schema `AvailabilityByFuelTypeDaily` gives `outputUsable` as
  int64 with no unit. The page says the feed sends no unit and that MW is gridflow's column name
  (`fou2t14d.py:99`). "Output Usable" is the OpenAPI's own wording ("also referred to as Output Usable data under
  the Grid Code"), which I checked against the swagger text.

### 3. The frame and the notebook lead

- **Frame rows.** The 8 rows are real (`generated_by: gridflow-sample`): WIND, delivery 24 Sep, publishes 20 Sep
  08:00 to 15:00, and the values match silver.
- **Frame layout.** Column order follows `select.columns`. The guide lists the key columns first and has no
  pipeline lines. For how the rows read apart at 390, see finding 1.
- **The `query()` "latest stored publish" claim holds.** In gridflow_models, `_relation_name_for_dataset` returns
  `silver_elexon_fou2t14d_latest`, and `_validate_dataset_for_source` returns `settlement_date`. The predicate is
  inclusive at both ends (`source.py` `query`).
  - The view is `QUALIFY ROW_NUMBER() OVER (PARTITION BY settlement_date, fuel_type ORDER BY available_at DESC
    NULLS LAST) = 1` (`latest_views.py:104-107` and `:261-269`).
  - `available_at == published_at` on every silver row, with no nulls.
- **Notebook outputs.** Cell 3 prints the single 22 Sep 00:00 publish, and cell 4's rows match silver.
- **Plot and `plot_alt`.** The plot PNG matches `plot_alt`: CCGT 19,214 to 24,826 on 1 Oct, 23,872 on 2 Oct,
  24,910 on 6 Oct; WIND 5,824 on 25 Sep and 15,891 on 29 Sep; NUCLEAR 4,210 to 5,158, never falling. All cells
  are read-only, with no errors.

### Other rubric items

- **Facts.**
  - The grain and key come from `ENTITY_KEY_COLUMNS` (`fou2t14d.py:59`).
  - `timestamp_utc` is midnight UTC of `settlement_date` on every row, as the code says
    (`fou2t14d.py:132-139`).
  - Bronze carries `forecastDateTimezone: "Europe/London"`, which supports "a London date".
  - `INT*` rows carry `biddingZone` and `interconnectorName`, and `output_cols` drops both.
  - "2 to 14 days ahead" is the vendor's wording for both FOU2T14D and NDFD, per the OpenAPI.
  - The request URL matches the bronze meta (`page=1` included).
  - Transform `--end` is inclusive.
- **No local data.** The rendered page and the note's `page:` block are clean of `locally`, `held`, `our `,
  `since 20`, and "rows" or "days" counts. The cadence line is scoped to the chart ("the charted publishes are an
  hour apart").
- **Build and detector.** `gridflow-build --only elexon/fou2t14d` succeeded, and `detect.mjs --json` returned `[]`.
- **Leakage and filler.** No em dashes, middle dots, arrows or "live"/"now". Every related note is 12 words or
  fewer and says how the datasets relate.
- **Vault body edits.** Each one is cited and minimal:
  - the Overview quote;
  - the publication-lag row;
  - the dedup key;
  - the `settlement_period`, `timestamp_utc` and `ingested_at` rows (`fou2t14d.py:181-186` stamps `ingested_at`
    at transform);
  - the sample line;
  - the dated Known-issues update. I checked it: a fetch at 26 Sep 18:33 of the 13 Sep window holds 25
    publishes.
- **Screenshots.** Taken with headless Chrome through a 390 px iframe on port 9743, plus 1440. I looked at the
  hero and scenery, the chart and key, the raw feed, the frame folded and unfolded with its guide, the notebook
  drawer, and the stratum labels. Nothing is clipped or overlapping.
  - The unfolded frame scrolls inside its box at 390, as on other pages.
  - The shot set is reduced, on the coordinator's instruction after a hung Chrome call. 1024 and 768 were not
    re-shot.

## Out of scope, for the seat

- **Vault glossary error.** `20-domain/glossary.md:123-124` in the vault describes FOU2T14D as a day-ahead
  forecast by BM Unit, which is wrong. The writer reported it and left it alone. It needs a separate vault fix.
