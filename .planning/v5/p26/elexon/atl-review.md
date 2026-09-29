# elexon/atl: review

Checker, 2026-09-29. Inputs: vault worktree note `30-vendors/elexon/datasets/atl.md` (diff against
`origin/master`), mirror `vault/elexon/atl.md` (`cmp` clean), the three artefacts, the page rebuilt with
`gridflow-build --only elexon/atl` on the p26-elexon worktree (includes #51 and #52), the writer's report
with Revision 1.

## Verdict: APPROVE

No blocker or major. Three nits, none of which blocks the page.

## Findings

1. **nit** `page.how_used[2]`: "A load feature for a GB power price model, once missing half-hours are
   handled." This turns the gaps seen in the charted week into a property of ATL in general. Whether the
   missing periods come from Elexon, or from the publish-window query style, is unknown: see the writer's
   open question 1. `what_it_is` and the caption scope the gaps correctly ("In the week charted..."), so
   this line is the only one that generalises them. Suggested fix: "..., handling half-hours with no row"
   or drop the clause.
   Evidence: silver has 206 of 336 half-hours for settlement dates 14 to 20 Sep (Polars over
   `silver/elexon/atl/**`). No vendor statement about the missing periods is quoted in the note or the
   repo.

2. **nit** `page.facts.cadence`: "One vendor document per settlement period, each published on its own."
   It is measured on our copy, with no vendor text behind it: all 403 local rows have distinct
   `document_id`s and `document_revision` 1 (`n_unique` 403 of 403). It is visible in the eight rows
   (eight ids, eight publish times) and fits the vault's bronze sample, so it is acceptable as written.
   Scoping it to what the frame shows would be stricter ("each settlement period sent as its own
   document, as the frame shows").

3. **nit** `page.summary`: "actual total load for each half-hour settlement period" reads as full coverage,
   while the chart below shows many half-hours with no row. It is fair as a definition of the data item.
   "one MW figure per settlement period" alone would avoid the tension.

## What was checked and held

**Missing half-hours (focus 1).** The page gives no cause anywhere.
- Present: 206 of 336 half-hours in the chart week. Absent: 130, of which 92 are before 12:00 UTC (90
  before UK midday), so "mostly before midday" holds in either reading.
- The caption ("line breaks at each one... a dot"), the alt and `what_it_is` state only what the chart
  shows.
- The rebuilt SVG has 33 lone dots (`r="3.2"`) in both the wide and narrow charts.

**The 2,670 MW half-hour (focus 2).**
- Silver: 18 Sep period 15 (06:00 UTC) 25,600; period 16 (06:30) 2,670; period 17 has no row; period 18
  30,651.
- Bronze `bronze/elexon/atl/2026/09/18/raw_20260926T182917Z_96b3d494.json` holds
  `"settlementPeriod":16,"quantity":2670.000`, so "as sent" is true. The transformer only casts the value
  to float (`silver/elexon/atl.py:84`).
- The key note and the alt ("drops from 25,600 to 2,670 MW and stops there") match, and give no cause.

**The INDO comparison (focus 3).**
- A Polars left join of INDO (336 rows) with ATL on `(settlement_date, settlement_period, timestamp_utc)`
  matches 206 rows.
- Grouped into 6-hour UTC blocks, it reproduces the notebook's cell 6 exactly:

  | From UTC hour | Min | Median | Max |
  |---|---|---|---|
  | 0 | -874 | 2,510 | 5,003 |
  | 6 | -23,291 | 6,357 | 12,876 |
  | 12 | 2,154 | 7,916 | 15,704 |
  | 18 | 902 | 3,686 | 6,079 |

- `what_it_is` quotes 7,916 as a notebook output ("in the notebook it runs a median..."). It gives no
  cause and does not define total load.
- `plot_alt` checks out:
  - 202 of 206 differences are positive;
  - the largest are at 12:00 to 14:00 UTC;
  - the ATL maximum is 34,330;
  - the INDO maximum is 30,813 (16 Sep 18:30);
  - the image `atl-5.png` shows the same.
- `tz_convert("UTC")` is in cell 4, so the blocks are UTC.

**Note-body fixes (focus 4).** Each is the smallest span and cites evidence.
- `business_type`: the transformer renames it only if present (`atl.py:70`) and selects available
  columns (`:137`). Silver has no such column. The sample placeholder is removed.
- `ingested_at`: stamped `datetime.now(UTC)` in `transform` (`atl.py:117-121`), so "silver transform
  time" is right.
- Sample `timestamp_utc`: 2026-05-06 period 5 in BST is 23:00 UTC + 2 h = 01:00Z, matching the bronze
  sample's `startTime`.
- AGPT is B1620 (`connectors/elexon/endpoints.py:165`) and ATL is B0610 (`:175`).

**Distinct from demand-outturn.**
- `elexon.json` family `demand-outturn` has members `indo`, `itsdo`, `indod`. `atl` is its own page in
  group 2.
- The page says ATL "is not INDO national demand" and relates it to `elexon/indo`, which resolves to
  `demand-outturn.html#indo`.

**Facts and provenance.**
- Grain and key: `ENTITY_KEY_COLUMNS` and `unique(keep="last")` (`atl.py:26-29`, `:115`); 0 duplicate
  keys in silver.
- `timestamp_utc` comes from `settlement_period_to_utc` (`:88-97`); `startTime` is not read.
- `total_load_mw` is `quantity`, in MW (`schemas/elexon.py:590`).
- `raw_feed.requests`: the format matches `build_params`/`_to_utc_z` and the bronze sidecar
  `request_params`.
- `raw_feed.commands`:
  - ingest `--end` is a bare date, so it is midnight UTC, exclusive (`pipeline/runner.py:resolve_dates`,
    `client.py` `while current < end`);
  - there is no `PARTITION_SOURCE_OFFSETS` (base default `(0,)`);
  - silver files `atl_20260914` to `atl_20260921` hold all settlement dates 14 to 20, and period 48 of
    the 20th sits in `atl_20260921`. So ingest 14 to 22 and transform 14 to 21 is exactly the needed
    window.
- The notebook `needs` INDO window (13 to 20) matches the demand-outturn page's own commands.
- Series: `spec_origin: vault`, 206 points, `rows_used` 206.
- Alt highs and lows:
  - highs 30,836 to 34,330 at 11:00 to 12:30 or 17:00 UTC;
  - lows 19,958 to 22,392 at 03:30 to 05:00 UTC, the 2,670 aside;
  - all match silver.
- No staged spec and no authored override remain.
- Samples: `generated_by: gridflow-sample`. The eight rows are periods 39, 41, 43 to 48, and period 48 was
  published 2026-09-21 00:29:01, as the caption says.
- The guide covers every non-pipeline column, key first.
- Notebook: written by `scripts/run_notebooks.py`, read-only cells, no errors. The lead matches `query()`:
  relation `silver_elexon_atl`/`_indo`, date column `settlement_date` (`schema_manifest.py:114`, `:125`).
- Related: the targets exist (`indo` and `ndf` are family pointers); NDF is day-ahead
  (`endpoints.py:128`); notes are 12 words or fewer.

**Build, detector, leakage.**
- `gridflow-build --only elexon/atl` wrote the page with no errors, and `detect.mjs --json` returns `[]`.
- A grep of the rendered text finds no "locally", "held", "our", "since 20", "% of", "N rows/days", em
  dash, middle dot, arrow, "live/now/real-time" or planning codes. Every "row" hit is scoped or is the
  help card.
- The axis ends at "20" on both the wide and narrow charts: the #52 fix removed the stray "21".

**Screens.**
- Headless Chrome through iframe wrappers:
  - 1440, 1024, 768 and a true 390 (390 px iframe);
  - folded, and open (frame unfolded, notebook drawer open, images eager);
  - shots in `scratchpad/atl-review/shots/`.
- Nothing is clipped or overlapping: hero scenery tops, corner labels, chart labels, legend, frame, guide,
  notebook plot and tables. Wide tables scroll inside their containers by design.
- The site has no dark theme: no `prefers-color-scheme` rule in any asset.
- Port 9728 was held by another process, so 9788/9789 were used. Both servers are stopped.

## Not a finding (for the seat)

The vault body still has unevidenced lines the writer flagged and rightly left alone, since they are not
on the page:
- "Historical depth: several years";
- "Publication lag: soon after each settlement period closes"; on our rows `published_at` is
  `timestamp_utc` + 119 min;
- "ATL is what the EU transparency platform consumes for GB load".

The last one is worth a research check: whether GB data still flows to the ENTSO-E platform is not
evidenced anywhere in the repo. The writer's two open questions (why periods are missing; where B0610 is
defined) stand as research units.
