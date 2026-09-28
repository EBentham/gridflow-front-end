# agpt: checker review

Page `elexon/agpt`, "Actual generation per type". Checker: Opus 5.5 · high, 2026-09-28.

## Verdict: APPROVE

No blocker or major findings. 4 nits, all optional. One process note for the seat (build rerun).

## Findings

1. **nit**: `page.chart_view.caption` ("FUELHH wind does not dip") and the new wind-dip Known issues bullet in the note body.
   - **The FUELHH clause:** it compares against the project's FUELHH silver for a window that no page shows (the fuelhh chart covers 20 to 26 Sep). It is a project observation, not a vendor fact.
   - **Why it is only a nit:**
     - it is scoped to that day;
     - it carries no number;
     - it is true: FUELHH `WIND` is 11,704 to 16,879 MW over the same 49 half-hours.
   - **Brief's pattern:** a project measurement should be labelled as one ("checked against demand; Elexon does not state it").
   - **Suggestion for the caption:** label the clause, for example "FUELHH wind for the same half-hours, checked by the project, does not dip", within the 30-word budget.
   - **Do not add** a second unlabelled local comparison to the caption.
   - **The AGWS evidence:** AGWS, the other B-series wind feed, shows the identical dip. That places the dip in the vendor's B-series data as fetched, not in the gridflow transform or a mis-fetch.
   - **Where the AGWS evidence goes:** in the note body's Known issues bullet, dated and labelled as measured, not on the page.
   - **Evidence:**
     - AGWS silver, `timestamp_utc` from 2026-09-17 15:30 to 2026-09-18 15:30 UTC (49 half-hours):
       - `Wind Offshore` is 117 to 288 MW and `Wind Onshore` is 2,104 to 4,337 MW;
       - summed per half-hour, 2,245 to 4,625 MW;
       - all rows are revision 1.
     - These are exactly AGPT's figures.
     - Bronze holds one raw file per publish day for 17 and 18 Sep (`raw_20260926T183105Z_*`), so keep-last dedup cannot have picked a stale fetch.
2. **nit**: `page.chart_view.key[other].note` ("Elexon's own type; what it holds is undocumented.").
   - **What's wrong:** the wording is copied from fuelhh, where `OTHER` really is a BMRS fuel code. AGPT's labels are the ENTSO-E production-type names of the B1620 report (note body: "AGPT is the GB equivalent of the ENTSO-E B1620 series"), and `Other` is ENTSO-E's own B20 category. So "Elexon's own type" can be read as Elexon having defined it.
   - **Suggestion:** "The vendor's `Other` type; what it holds is undocumented."
   - **Confidence:** low. The note's column table also calls these "Elexon's human-readable PSR label".
3. **nit**: chart tag for series `wind` (`page.chart_view.key[wind].tag`).
   - **What's wrong:** at 1440, 1024 and 768 the renderer places the `wind` tag at the step where wind recovers (2026-09-18 about 16:00 UTC). The first letter or two sit on the empty background above the dip, the rest on the band edge.
   - **Impact:** it is legible and not clipped, and it overlaps no other label.
   - **Cause:** this is the template's tag placement meeting the dip, not something the writer wrote. If it bothers Bobbo, the seat can fix the placement, or the writer can drop `tag: wind`.
   - **Evidence:** screenshots `crops/1440-open-unfold-1.png` (zoom `crops/z-1440-wind.png`), `1024-open-unfold-1.png` and `shots/v768-1300.png` under `scratchpad/agpt-review/`.
4. **nit**: note body additions that are not corrections:
   - the Publication lag row: "Measured ... 149 min after `timestamp_utc` on every row";
   - the new "Wind dip, 17-18 Sep 2026" Known issues bullet.

   **What's wrong:** these add local measurements to the canonical note rather than fix a wrong fact (rubric 7: smallest span).

   **Why it is only a nit:** both are dated, labelled as measured on local silver and not presented as vendor rules, and neither reaches the page. The lag measurement is what justifies the command windows.

   **Suggestion:** if the dip bullet stays, add the AGWS agreement from finding 1.

## The writer's four flagged points

1. **The wind dip: keep the window and the caveat.**
   - **The window:** local silver holds settlement data only for 13 to 21 Sep and 1 to 5 Aug 2026. 14 to 20 Sep is the only complete 7-day run, and writers may not ingest.
   - **The numbers are right:**
     - AGPT wind (offshore plus onshore) is 2,245 to 4,625 MW from 17 Sep 15:30 to 18 Sep 15:30 UTC inclusive, 49 half-hours, so "for a day from 15:30 UTC on the 17th" is accurate.
     - The 15:00 half-hour is a partial drop (8,380 MW), which "from 15:30" correctly leaves out of the 2.2 to 4.6 GW range.
     - FUELHH `WIND` over the same 49 half-hours is 11,704 to 16,879 MW.
   - **The wording follows the rules:** no cause is asserted ("Cause unverified"), which follows the brief's "never a cause nobody has verified". "FUELHH wind does not dip" is scoped to that day and carries no number.
   - See finding 1 for the stronger wording.
2. **The command windows are correct.**
   - **Ingest:** the connector has the `PUBLISH_DATETIME` style with 24 h chunks (`endpoints.py:163-166`, `max_chunk_hours=24` at `:40`).
     - The loop runs `while current < end` (`client.py` PUBLISH_DATETIME branch), and a bare `--end` date is midnight UTC (`pipeline/runner.py:479-501`).
     - So `--start 2026-09-14 --end 2026-09-22` fetches publish days 14 to 21, with the end exclusive.
   - **Filing:** bronze is filed by `data_date = start.date()` (`client.py` `_fetch_datetime_range`).
   - **Transform:** there are no `PARTITION_SOURCE_OFFSETS` (base default `(0,)`, `silver/base.py:417`), and `AGPTTransformer.read_bronze` reads only the exact day directory. `run_transform` iterates `date_range(start.date(), end.date())`, with the end inclusive (`runner.py:1125-1138`).
   - **Coverage:** the lag is 149 minutes on every row in the window.
     - Settlement 14 Sep period 1 (13 Sep 23:00 UTC) is published at 01:29 on the 14th.
     - Periods 47 and 48 of the 20th are published on the 21st.
     - So publish days 14 to 21 cover settlement dates 14 to 20 completely, and transform 14 to 21 is right.
   - **The rest agrees:** `notebook.needs` "14 to 21 September 2026" matches, and the comments are 6 words or fewer.
3. **Summing offshore and onshore wind is allowed; the choice is Bobbo's.**
   - `KEY_MAX = 9` (`page_fields.py:163`) and there are 11 types. MW is additive, the key note and caption say the band is summed, and the frame and notebook plot show the split.
   - The other option is to split wind into two bands and drop coal and oil, which are 0 MW in every half-hour. That would show the offshore collapse on the chart itself. It is a taste call, not a finding.
4. **The body fix on revisions is correct.**
   - `AGPTTransformer.read_bronze` concatenates `sorted(glob("raw_*.json"))` in name order (`raw_{ts}_{hash}`, so fetch order). `transform()` then runs `unique(subset=[settlement_date, settlement_period, psr_type], keep="last")` (`agpt.py:114-117`) and never reads `document_revision`.
   - The default (non partition-owned) `run()` path adds no second dedup, and `_write_silver` overwrites one file per date.
   - A re-issue published on a later day lands in that day's silver file, as the bullet says. The other three body fixes are also right:
     - `ingested_at` is stamped at transform time (`agpt.py:119-124`);
     - the sample's `timestamp_utc` is 00:30 for BST period 4;
     - the path pattern is the publish day.

## Checklist

- **Facts**
  - The grain and key match `ENTITY_KEY_COLUMNS` and the dedup (`agpt.py:26,114-117`).
  - `timestamp_utc` comes from `settlement_period_to_utc(settlement_date, settlement_period)` (`:87-96`), and `settlement_date` is the vendor label cast to a date (`:80`).
  - `generation_mw` comes from `quantity` (MW, note body column table), and `psr_type` is a label.
  - Silver has 11 labels and no interconnector. `settlement_period` is limited to 1 to 50 (`schemas/elexon.py`).
  - The request URL matches `build_params` and `_to_utc_z` (`%Y-%m-%dT%H:%M:%SZ`, `page` appended), with base URL `https://data.elexon.co.uk/bmrs/api/v1` (`config/sources.yaml:3`).
  - `notebook.lead` is right:
    - `query()` reads relation `silver_elexon_agpt` on date column `settlement_date` (DATE), with both ends inclusive, ordered by `settlement_date`;
    - it drops `event_time, available_at, vintage_policy, source_run_id, dataset_version, month, year`, checked through the `_get_method_registry` values;
    - it returns a pandas frame (`source.py:436-451`).
  - The related notes match `endpoints.py:162-176` (B1630, B0610). For GB, `vault/entsoe/actual_generation.md:63` and `:152` record an empty response: HTTP 200, reason 999 "No matching data found".
  - Universals are scoped: "in this window", "here", "in these rows".
- **Chart provenance**
  - The series file has `spec_origin: vault` and `generated_by: gridflow-distil`, with 0 duplicates dropped. No staged spec or authored override exists.
  - The build reported no agpt error, so the digest check passes.
  - Series min and max match the alt text exactly:

    | Series | Min (MW) | Max (MW) |
    |---|---|---|
    | nuclear | 3,279 | 3,737 |
    | gas | 1,460 | 12,101 |
    | wind | 2,245 | 20,223 |
    | solar | 0 | 10,099 |
    | ps | 0 | 1,211 |
    | total | 12,401 | 33,774 |
    | coal and oil | 0 | 0 |

  - Palette:
    - khaki (`other`) is used only for `Other`;
    - PS, coal and oil, and hydro are unpainted hatches;
    - no signed series is clipped (PS never falls below 0 here).
- **No local data:** the grep of the `page:` block and the rendered text is clean. The "our" hits are "half-hour".
- **Budgets and structure**
  - The detector returns `[]`.
  - The sample has `generated_by: gridflow-sample`: 8 real rows, and the guide covers every non-pipeline column, key columns first.
  - The notebook has `generated_by: scripts/run_notebooks.py`, read-only cells and no errors. `plot_alt` matches `agpt-5.png` (viewed).
  - The mirror is byte-identical to the vault note (`cmp`).
- **Clipping**
  - The page scroll width equals the viewport at 1440, 1024, 768 and 390, with the notebook closed and also open with the frame unfolded. The only overflow in any clipping container is the intended `sr-only` spans.
  - I viewed the hero scenery, chart, key, raw feed, frame, guide, notebook and related section. The longest key code, "Fossil Hard coal, Fossil Oil", fits at 390.
  - The site has no dark theme (no `prefers-color-scheme` in any stylesheet), so light only.
- **Leakage and filler:** no em dashes, arrows, middle dots, "live", "now" or planning labels. All related notes are 12 words or fewer.

## Process note for the seat

`gridflow-build --only elexon/agpt` could not be rerun green. The vendor-wide content check fails on another writer's in-progress note:

- first `windfor: page.raw_feed.note: 31 words`;
- then `windfor: page.related[1].note: 13 words`;
- earlier also `agws: key[1].paint`.

The page on disk was built at 21:57:01, 13 s after the last template commit (`a0e18d9`, 21:56:48). None of its inputs have changed since, except `site/hifi/data/elexon.json`, whose one uncommitted change (21:57:53) rewords the `mid` hub blurb. That does not touch the agpt page, but writers were told not to edit `elexon.json`, so check who changed it.

Rerun `--only elexon/agpt` once windfor passes.
