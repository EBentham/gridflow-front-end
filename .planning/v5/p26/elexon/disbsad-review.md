# disbsad: checker review

Checker, 2026-09-29. Page `elexon/disbsad` (Disaggregated balancing services adjustment data). Inputs: vault note
`30-vendors/elexon/datasets/disbsad.md` in the vault worktree (`git diff origin/master`), mirror
`vault/elexon/disbsad.md` (cmp identical), the three artefacts, the built page, `disbsad-author.md`, gridflow code,
local bronze and silver (Polars, read only).

## Verdict: REVISE

2 majors, 4 nits.

## Findings

1. **major**: `page.raw_feed.note`, "Each reply also holds the half-hour starting at `to`, so silver repeats it on
   neighbouring days."
   - **What:** this is stated as the vendor's rule. It is a measurement of the replies gridflow fetched. gridflow's
     code says the bare `from`/`to` semantics are undocumented: `silver/elexon/_publication_window.py:53-56`
     exempts `disbsad` because its "bare from/to params" are "undocumented ... do not invent semantics for the
     override". The vendor text quoted in the note (query parameter table: "The "to" start time or settlement date
     for the filter") does not say whether `to` is inclusive. The note body has no dated, labelled observation to
     back the sentence either.
   - **Evidence:** all nine bronze replies for 13 to 21 September (`bronze/elexon/disbsad/2026/09/<dd>/*.meta.json`,
     `from=D T00:00:00Z&to=D+1 T00:00:00Z`) run from `D 00:00` UTC to exactly `D+1 00:00` UTC (settlement D+1
     period 3), computed with `settlement_period_to_utc`. Silver then repeats those keys across files: 9 keys x 2
     rows in September (14 to 21 Sep, all period 3, same cost and volume). So the sentence is true of these
     replies, and its second half is true of gridflow (`disbsad.py:32-56` reads one bronze day and `:118-123`
     dedups within it).
   - **Fix:** scope it, for example "The replies fetched for this page each also held the half-hour starting at
     `to`, so silver repeats it on neighbouring days." Add a dated "measured" bullet to the note body's Known
     issues (13 to 21 Sep 2026 replies, fetched 2026-09-26), as the boal note does.
   - **Batch consistency:** boal's `raw_feed.note` has the same unscoped shape ("A segment starting at midnight UTC
     is in both adjacent windows") and was approved (`boal-review.md` nit 1). boal's note body does carry a
     labelled measurement. The seat may want the two pages worded the same way.

2. **major**: units `£` and `MWh` in `page.summary`, `page.what_it_is`, `page.record.fields.cost`,
   `page.record.fields.volume`, `page.chart.unit`, `page.chart_view.caption`, `page.chart_view.alt`,
   `page.chart_view.key[system].note` and `page.notebook.cells` (the `ylabel`).
   - **What:** every unit is stated flatly as fact, but none has a source. gridflow code states no unit
     (`disbsad.py:97-99` only casts to Float64; `ElexonDISBSAD` has no unit). No vendor text quoted in the note
     states one. The only sources are the vault schema table (`cost` "GBP.", `volume` "MWh.") and the gotcha
     "Cost field unit: GBP (not GBP/MWh)", neither cited. The domain note `20-domain/instruments/bsad-disbsad.md`
     (lines 9, 30-31) is uncited too. The writer's check (cost over volume is 158 to 186 on 17 Sep P42 System
     rows, near system-price levels) makes £ and MWh plausible, but it is a project check. The pilot calibration
     graded exactly this as a major (INDOD "MWh" from a project check).
   - **Fix, preferred:** quote a vendor source in the note body. The netbsad note on the same branch already cites
     Elexon, *Imbalance Pricing Guidance* v15.0, 25 June 2020
     (https://www.elexon.co.uk/bsc/documents/training-guidance/bscguidance-notes/imbalance-pricing/). Its p. 11
     splits BSAD into "Balancing Services Adjustment Actions", and p. 28 covers the individual action the SO
     submits. If it (or BSC Section Q) gives the action's cost in £ and volume in MWh, quote it with the page
     number. The units then stand as written.
   - **Fix, fallback:** attribute them on the page as a project reading, per the brief's rule for anything only
     the project measured. For example, cost: "Cost of the action, signed; £ by our reading (cost over volume
     matches system prices), Elexon's quoted docs give no unit". Keep the fields within 14 words.

3. **nit**: `page.chart_view.key[system].note`, "no vendor text in the note says what the sign means".
   - **What:** "the note" is the vault note, which a site reader cannot see. It is the only such internal
     reference on any Elexon page (grep of `vault/elexon/*.md`).
   - **Fix:** use the fields' wording, for example "Signed, -100 to 750 MWh here; the sign's meaning is not stated."
     No sign convention is stated anywhere on the page (checked, see below), so this is wording only.

4. **nit**: `page.facts.grain` ("One row per settlement period, action id and service") and `page.what_it_is`
   ("one row per action").
   - **What:** both hold for each transform run (`disbsad.py:118-123`). They do not hold for the relation `query()`
     reads, where the midnight half-hour key is in two files (finding 1's 9 keys x 2 rows).
   - **Why nit:** this is the same case as boal nit 1. The notebook lead says "the midnight half-hour can come
     twice, so drop repeats on the key", and the chart, the eight rows and the notebook all dedup. No fix is
     needed if finding 1 is scoped.

5. **nit**: `page.notebook.plot_alt`, "Energy and System step between zero and blocks of 100 to 770 MWh".
   - **What:** Energy also has small blocks: 25 MWh on 14 Sep 15:00 to 15:30 UTC, 36.5 to 37.1 on 17 Sep 17:00 to
     17:30, and 0.15 to 2.35 around them (committed series `energy`). The plotted Energy line shows a visible bump
     at about 35 MWh on the 17th/18th.
   - **Fix:** "blocks of up to 770 MWh".

6. **nit** (vault body; not an author edit, recorded for the seat): the Overview ("the constituent BSAD components
   used to derive Net BSAD") and Known issues ("NETBSAD is the aggregate of DISBSAD components") are unchanged.
   The netbsad note on the same branch removed its twin claims, citing the Imbalance Pricing Guidance and the
   data disagreement. After merge, the two canonical notes will contradict each other. The page makes no
   aggregation claim, which I checked (see below). **Fix:** align the disbsad body with the netbsad note's
   sourced wording when the netbsad page is settled.

## What passes (evidence)

**Chart provenance.**
- `series/elexon/disbsad.json` has `generated_by: gridflow-distil` and `spec_origin: vault`. Its spec equals
  `page.chart`, and the build's digest check passed.
- There is no staged spec (`site/hifi/data/chart-specs/elexon/disbsad.json` is absent) and no authored override.
- Window: `x[0]` is 2026-09-13T23:00Z (settlement 14 Sep period 1) and `x[-1]` is 2026-09-19T22:30Z (19 Sep period
  48), 288 half-hours. The caption's "settlement dates 14 to 19 September 2026" and "every half-hour" are right.
- `provenance.duplicates_dropped: 6` are the six midnight repeats inside 14 to 19 Sep (keys on 14 to 19 Sep period
  3). That backs "each action counted once".
- The series ranges match the text:

  | Series | Min | Max | Page text |
  |---|---|---|---|
  | `system` | -100.0 (16 Sep 08:00Z) | 750.0 (17 Sep 17:00Z) | alt and key note |
  | `energy` | 0.1 | 772.85 (16 Sep); 765.8 on the 14th | alt "0.1 to 773", "14th and 16th" |
  | `lcm` | -5.76 | -0.173 | key note, alt |
  | `none` | 0 | 0 | draws nothing |

- No System half-hour mixes signs (0 of the half-hours), so summing does not net opposite actions. Volume (MWh) is
  additive across actions.
- No khaki is used; all four paints are hatches, and no scenery role fits these services. The signed series are
  neither clipped nor folded.

**Signs.**
- No sign convention is stated. `record.fields.cost` and `record.fields.volume` both say "the sign's meaning is not
  stated".
- The key notes are observations scoped with "here", and each is true in the window:

  | Service | Silver, 14 to 19 Sep, deduplicated |
  |---|---|
  | `Energy` | 2441 rows, volume 0.05 to 107.5, all `so_flag` false |
  | `Non-BM LCM` | 1279 rows, all volume < 0 and cost > 0 |
  | `System` | 506 rows, volume -75 to 150 per action |

- The uncited domain-note convention ("positive = SO paid") was correctly left out.

**NETBSAD.**
- The page makes no aggregation claim. `what_it_is` says only "The net table, NETBSAD, has one row per period
  instead", which is true (`silver/elexon/netbsad.py:136`).
- The related note "Elexon's net adjustment per period, published as its own table" makes no sum claim.
- A grep of the rendered text for "aggregat" returns nothing.

**Other facts.**
- `raw_feed.requests` is right:
  - it matches the connector: `/datasets/DISBSAD`, `from`/`to`, `%Y-%m-%dT%H:%M:%SZ`, `page=1`
    (`endpoints.py:73-79`, `build_params`, `_to_utc_z`);
  - bronze meta `request_url` agrees, with percent-encoded colons, and the literal-colon form matches the fuelhh
    convention.
- Windows are 24 h (`max_chunk_hours=24`, `client.py` `while current < end`).
- `raw_feed.commands` are right:
  - a bare date is midnight UTC (`runner.py:462, 489`), so the ingest end is exclusive and 13 to 20 fetches
    bronze 13 to 19;
  - transform 13 to 19 is inclusive;
  - silver 13 holds 14 Sep periods 1 to 3, which is what "starts early: dates begin 23:00 UTC" means (BST).
- Fields:
  - `adjustment_action_id` comes from `id` cast to Utf8 (`disbsad.py:71, 104-105`);
  - `so_flag` comes from `soFlag`, and `stor_flag` from `storFlag` or the legacy `storProviderFlag`
    (`:72-74`);
  - `component` comes from `service` or the legacy `component` (`:75-76`);
  - `timestamp_utc` comes from `settlement_period_to_utc`;
  - the period range reads "1 to 48; 46 or 50".
- The null-service rows in the window are all id 1 with cost 0 and volume 0. There is at most one per period, and
  never alongside another row. The key note is scoped with "here".
- "Elexon also sends each action's party and asset":
  - `partyId`, `assetId` and `isTendered` are non-null on all 4242 action rows in bronze 13 to 19, and null only
    on the zero rows;
  - `output_cols` (`disbsad.py:133-147`) drops them;
  - (date, period, id) is unique without `component` (4330 of 4330 rows), so "one row per action" holds per run.
- The notebook lead is right:
  - `query()` reads `silver_elexon_disbsad`, filters on `settlement_date` (`schema_manifest.py:117`) with both
    ends inclusive, drops the bitemporal lineage columns, and orders by the date column only;
  - the cell sorts and dedups;
  - the notebook's `needs` of 13 to 19 Sep matches the transform window.

**No local data.** A grep of the `page:` block and the rendered text for `locally`, `held`, `our `, `since 20`,
`rows`, `% of` and digits followed by `rows` or `days` found only template text ("sample rows", the help card) and
"hour". There are no em dashes, middle dots or arrows, and no "live", "now" or "real-time".

**Structure.**
- `gridflow-build --only elexon/disbsad` succeeds, and `detect.mjs --json` returns `[]`.
- The sample was made by `gridflow-sample`:
  - it holds eight real rows (17 Sep P42: ids 1, 2 and 50 System; 51, 52, 53 and 83 Non-BM LCM; 84 Energy
    with `so_flag` false);
  - the guide has one line per non-pipeline column, key first.
- The notebook was made by `scripts/run_notebooks.py`:
  - it has 5 cells, all read-only and without errors;
  - the plot image matches `plot_alt`, apart from nit 5.

**Body edits (rubric 7).** All three are correct, cited and minimal:
- the dedup key (`disbsad.py:118-123`, `keep="last"`, one bronze day);
- `stor_flag` source (`:73-74`);
- `ingested_at` is stamped at transform (`:125-129`).

**Rendering.**
- I looked at 1440, 1024 and 768 directly, and at 390 through a 390 px iframe. I checked the page folded, then
  unfolded with the notebook open, using a static server on 9740 (stopped afterwards).
- Everything is fully visible: the hero scenery (turbine tops), the chart (its peak at about 790 sits under the
  800 tick), the key, the raw feed, the frame and guide, the notebook panel and plot, the related section, and
  each stratum's corner label.
- No dark theme exists: a grep of `site/hifi/assets/` for `prefers-color-scheme` and `data-theme` is empty, so
  light is the only rendering.
- The unfolded frame at 390 is an `overflow-x: auto` scroll region (frame scrollWidth 2420, clientWidth 390;
  document scrollWidth 390). That is template behaviour, not clipping.

## For the seat (not findings)

- The writer's open question 1 (the midnight half-hour repeated across silver files) is the same gridflow issue
  boal raised. It also affects `netbsad` and `mid` through the same bare `from`/`to` override.
- The `none` key entry is for a series that draws nothing, which is a template workaround (`_stacked` bridges time
  gaps). Its note reads correctly. A template option to keep x points without a key entry would remove it.
