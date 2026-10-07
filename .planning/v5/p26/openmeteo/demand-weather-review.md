# openmeteo/demand-weather: checker review

Checker: Sonnet 5.5 · high, 2026-10-06. Family `demand-weather` (lead `historical_demand`, member `forecast_demand`).
Checked against the rubric, gridflow code, local silver and bronze (read only), and the Open-Meteo docs the notes quote.

## Verdict: REVISE

0 blockers, 2 majors, 6 nits. The page is mostly accurate, the chart is correct and every body correction holds. The
two majors are both in the forecast wording, which is the part the seat asked to be hardest on.

## What I confirmed (no finding)

- **Build and detector:** `gridflow-build --only openmeteo/historical_demand` succeeds; `detect.mjs --json` returns `[]`.
- **Mirrors:** `cmp` of both canonical notes (vault worktree) against `vault/openmeteo/` is byte-equal. The vault diff
  against `origin/master` contains only the three body corrections described in the writer report plus the `page:` block.
- **Chart numbers, recomputed from silver** (`open_meteo/historical_demand`, london and glasgow, 1 Sep 2025 to 31 Aug 2026):
  - 17,520 rows, 0 nulls, exactly 24 hours in each of 365 UTC days per city, so every daily mean is a full 24-hour mean.
  - London is warmer on 351 days, Glasgow on 14, none equal. "351 of the 365 days" is correct.
  - London starts 16.42, Glasgow 14.5. Lows on 5 Jan 2026: London -1.34, Glasgow -2.46. Peaks: London 30.35 on 26 Jun,
    Glasgow 20.59 on 25 Jun. All match the alt text.
  - The committed series equals my recomputation to 0.0005 (rounding). The "mean of the 24 hourly values in each UTC day"
    in the caption is exactly what the distil step does, and the page says UTC day. The hourly values are instants
    (vendor "Instant"), so a mean of 24 of them is a plain arithmetic mean; the caption claims nothing more.
- **Body corrections:**
  - Snowfall is cm of snow, not water equivalent. The docs say "Snowfall amount of the preceding hour in centimeters",
    and "for the water equivalent in millimeter, divide by 7". The sample rows agree (3.29 cm against 4.9 mm).
  - The archive default is "IFS HRES, ERA5 and ERA5-Land" (docs quote). `client.py:109-116` sends no `models`.
  - Belfast is outside GB; `endpoints.py:55` says "Major UK population centres".
  - Hour-before-stamp fields: precipitation and snowfall "Preceding hour sum", shortwave "Preceding hour mean"; temperature,
    wind, humidity, pressure and snow depth "Instant". All match the column guide wording.
- **Units** against the vendor `hourly_units` in bronze: °C, km/h (divided by 3.6 in silver), °, %, mm, W/m², hPa, cm, m.
- **Request URL, commands and window semantics:** `client.py:109-116` builds the parameters in the order shown;
  `end_date` is a plain date, so the ingest `--end` date is fetched; bronze sits under the window start date
  (`data_date=start.date()`); transform `--end` is inclusive.
- **Notebook:** the JSON was written by `scripts/run_notebooks.py`, five cells, no error outputs, read-only calls.
  `query()` filters `timestamp_utc` with inclusive ends and drops `event_time`, `available_at`, `vintage_policy`,
  `source_run_id`, `dataset_version`, `month`, `year` (`schema_manifest.py:77`). The lead is right. The `plot_alt`
  numbers match silver (low -5.8 °C Manchester 01:00 on the 6th; Cardiff 11.5 °C at 20:00 on the 11th; end 8.9 to 10.1 °C).
- **Frame and guide:** the eight rows are real; the guide covers every non-pipeline column in frame order; the key columns
  are marked; the snowfall onset sits inside the eight rows (first non-zero snowfall is 18:00).
- **Screenshots** (own server on 9881, headless Chrome, 1440, 1024, 768 and 390 wide, light only, frame unfolded,
  notebook open): hero, chart, raw feed, frame and guide, notebook outputs and related list are fully visible at all four. The frame and the degree-day table
  scroll inside their boxes at 390, by design. The site has no dark theme.
- **Local-data grep** (`locally`, `held`, `our `, `since 20`, `rows`, `% of`, digits plus `days`): the only digit-day
  hits are "5 days late" (vendor docs) and "351 of the 365 days" (derived from the committed series, in the alt).
  No em dashes.

## Findings

### 1. [major] `page.family.members[1].differs`: "no run time kept, a re-fetch overwrites"

- **What is wrong:** the word "overwrites" is true only of silver, and the sentence is rendered under "The raw feed"
  (the bronze section, headed "bronze, the response as fetched"), where it reads as a claim about stored responses.
  - **Bronze never overwrites.** Each fetch writes its own file named for its fetch time (for example
    `raw_20260816T132833Z_...json` with a sidecar). Bronze keeps every fetch; only silver collapses them.
  - **In silver the collapse is a "last file in the day's partition" rule, not "the latest fetch".** `read_bronze` reads the
    target day's own window-start partition if it has any files, and only otherwise the nearest earlier partition
    (`silver/openmeteo/historical.py:178-212`); within the partition the last file by name wins (`unique(keep="last")`,
    line 258). Two overlapping windows with different start days therefore do not overwrite each other by fetch time.
    The writer's defect list and the forecast note body already say this.
  - I rate it major rather than nit only because it sits in the bronze section and on the one member whose whole point is
    that its history is not kept; it is not a wrong fact in silver for the common case (same window fetched twice).
- **Evidence:** `ls C:\gridflow-data\bronze\open_meteo\forecast_demand__london\2026\08` shows separate partitions `01`, `20`,
  `21`, each with its own timestamped raw file. Code lines above.
- **Fix:** say it in the silver terms the code supports and within 14 words, for example
  "Forecast host, own grid cells; silver keeps one value per hour, no run time". The same change would suit the
  `raw_feed.note` if the seat wants one plain sentence there.

### 2. [major] `page.how_used[2]`: "Forward weather from `forecast_demand`, fetched ahead of the hours it covers."

- **What is wrong:** it suggests a use silver cannot vouch for, and the pipeline cannot guarantee the "fetched ahead" part
  even when run as intended.
  - The connector sends `start_date` and `end_date` unchanged (`client.py:113-114`, no clamp to the fetch time), so a window
    starting earlier than the fetch returns hours that are already past, and silver stores them beside the hours still
    ahead with nothing to tell them apart. The only time stamp silver carries for these rows, `available_at`, is the
    silver build time (`base.py:1181` uses `now()`), not a fetch or model run time.
  - Because `read_bronze` prefers the day's own window-start partition (finding 1), a rolling daily fetch makes silver for
    day D come from the fetch that starts on D, not from a day-ahead fetch. A reader following the bullet would not get
    day-ahead weather.
  - The page already says (what_it_is) that the lead time is unknown; the bullet reads as if this table is the forward-looking
    feed anyway.
- **Evidence:** `silver/openmeteo/historical.py:187-195`; `connectors/openmeteo/client.py:109-116`;
  `silver/openmeteo/forecast.py:37` (`VINTAGE_POLICY = None`). In the local silver every `forecast_demand` day has one
  `available_at`, equal to the silver build, one run id, and 168 rows per day (7 cities x 24 hours).
- **Fix:** keep what the data can do and state the limit, for example "Weather inputs for the coming days if you fetch
  before they happen; silver does not record when a row was fetched." Or drop the bullet, since the page's own first two
  bullets and the family text already cover the use of `historical_demand`.

### 3. [nit] `page.record.caption` does not say the frame is `historical_demand`

The page is a family and the frame, chart and notebook come from the lead (author brief, "Family pages"). The chart caption
says so; the frame caption ("Birmingham, 16:00 to 23:00 UTC on 8 January 2026, the hours snowfall began.") does not, and the
Schema section carries no table name. A reader may take the rows as covering both members. Suggest "From `historical_demand`:
Birmingham, 16:00 to 23:00 UTC on 8 January 2026, the hours snowfall began."

### 4. [nit] `page.notebook.plot_alt`: "Most lines stay between -5 and 7 °C until the 10th; the low is -5.8 °C"

The sentence puts the range at -5 to 7 and then gives a low of -5.8. From silver, 5 to 10 January 2026: maximum 6.9, minimum
-5.8. Say "between -6 and 7 °C" (or "-5.8 and 6.9").

### 5. [nit] Notebook plot (`site/hifi/data/notebooks/openmeteo/historical_demand-5.png`): the legend sits on the data

At the default placement the seven-entry legend covers the lines for 5 to 7 January in the upper left (screenshot of the
open notebook). The cell is `...plot(ylabel=..., figsize=(8, 3.5))`; moving the legend below the axes, for example
`ax.legend(ncol=7, loc="upper center", bbox_to_anchor=(0.5, -0.25))`, would clear the lines. Rerun `run_notebooks.py`
after the cell change.

### 6. [nit] `page.chart_view.alt`: "Both start near 16.4 and 14.5 °C"

Reads as if both cities start near both numbers. Say "London starts near 16.4 °C and Glasgow near 14.5 °C". (The numbers are
right; checked above.)

### 7. [nit, advisory, seat's call] Canonical `historical_demand.md` still carries ERA5-only statements the new overview contradicts

Not rendered on the page and not a revision requirement (the writer kept to the smallest spans, as rubric 7 asks). But the corrected overview now says the archive blends three datasets while these remain:
the H1 "(ERA5 archive, population centres)" (line 132 of the note), the `models` parameter row "ERA5 model variant override"
(line 185), "ERA5 archive values are stable once published" (line 264), and "ERA5 grid-cell snapping" (around line 378).
The writer listed the first as not verified. The one at line 264 is the risky one: if recent days come from IFS and are
replaced later, it is false for the newest days. A one-clause scoping ("for the ERA5 part") would keep the note consistent
without a rewrite.

### 8. [nit] `page.raw_feed.requests` and family `request` for `forecast_demand`: the example window is all in the past

`start_date=2026-09-13&end_date=2026-09-22` is a window the forecast host answered on a fetch made after it had ended, so the
example shows a forecast request that returns no forecast. It is a valid request and the page does say past windows are
sent, so this is only a clarity point: a window starting today (or a note that this one is past) would show the member doing
its job.

## Template and hub issues (seat's, not findings)

As briefed: family-heading codes `HISTORICAL_DEMAND` / `FORECAST_DEMAND`, the mid-word wrap of the `hourly=` value
(`precipitati/on` at 1440), and the hub's "GB" and "ERA5" wording in `site/hifi/data/openmeteo.json`. I saw the wrap and the
codes in my own screenshots and agree with the writer's description.

## Defects for the backlog (confirming the writer's, one addition)

- The writer's four items hold (no run time and leakage risk; the value kept depends on partition layout; the `snowfall_cm`
  vault text; "GB" and "ERA5" wording). I reproduced the partition-layout one from `historical.py:178-212` and the bronze
  folder listing; the data I hold cannot show a case where the older fetch wins, so it rests on the code.
- **Addition:** silver `available_at` for `forecast_*` looks like the silver build time, not the fetch time (inferred from
  the default branch at `silver/base.py:1181`, which uses `now()` when not a re-ingest, and the one-second gap between the
  13:28:33 fetch and the 13:28:34 `available_at`; the transformer sets neither `VINTAGE_PER_BRONZE_FILE` nor
  `LOCKSTEP_BRONZE_READ`). In practice a pipeline run builds silver seconds after the fetch.
  A separate transform run days later would stamp a much later `available_at` and no row would carry the fetch time. Any
  future "lead time from `available_at`" work on these tables would be wrong.
