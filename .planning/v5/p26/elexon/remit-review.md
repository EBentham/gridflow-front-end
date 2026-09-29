# remit: review

Checker, 2026-09-29. Inputs: canonical note `vault-p26-elexon/30-vendors/elexon/datasets/remit.md` (its `page:` block
and the seven body corrections, `git diff origin/master`), the mirror (`cmp` identical), the three artefacts, the built
page, the writer's report, gridflow code, gridflow_models code and local silver (14 files, 2,291 rows, read with Polars).

## Verdict: REVISE

One major (a vault body correction states a count that does not reproduce), six nits. The page itself (the `page:` block
and the rendered page) has no blocker or major finding.

## Findings

1. **major**, vault body, Known issues > Revisions bullet (correction 7): "in 32 steps the number falls as
   `publishTime` rises, mostly within one second".
   - Wrong: no ordering of silver gives 32. A stable sort by (`mrid`, `timestamp_utc`) gives 30 falling steps, and 26
     of them have `dt == 0`: the two revisions share one publish second, so their order is a tie-break artefact, not
     a fall "as `publishTime` rises". Ties sorted by number descending give 65. Sorted ascending, 4.
   - Robust measure (every row pair in one `mrid` where the earlier `timestamp_utc` has the higher `revision_number`):
     **5 pairs across 4 messages**. Three are 1 s apart (`48X000000000001I-NGET-RMT-00081896` 3→2,
     `...00081916` 2→1, `11XINNOGY------2-NGET-RMT-00218398` 4→3). One is 6 h 30 m apart
     (`48X000000000357G-ELXP-RMT-20000025` 2→1). Separately, 72 pairs across 47 messages carry different numbers in the
     same publish second.
   - The writer's report example (PEMB-41 revs 6 and 7, both 15:18:05) is a same-second tie, not a rise. The report's
     own open question says "the 2 `mrid`s where the higher number was published earlier", which contradicts 32 too.
   - The rest of the bullet reproduces exactly: 62 extra rows over 42 (`mrid`, `revision_number`) pairs, 3 of them
     mixing `Active` and `Dismissed`, 6 rows repeating on every vendor field.
   - Fix: replace the sentence with, for example, "In 4 messages a lower number was published after a higher one (3 of
     them one second later), and 47 messages carry two numbers in the same publish second." Or drop the count.
   - Evidence: `remit_chk3.py` / `remit_chk6.py` in the scratchpad. Pairwise join on `mrid`, filtered
     `timestamp_utc < timestamp_utc_b & revision_number > revision_number_b`, gives height 5 and `n_unique(mrid)` 4.

2. **nit**, vault body, Silver schema, `event_status` row: still "Active / Withdrawn etc.". Silver has only `Active`
   (1,943), `Inactive` (146) and `Dismissed` (202); `Withdrawn` never appears. The note body was corrected elsewhere
   but not here. Fix: "Status as sent, e.g. `Active`, `Inactive`, `Dismissed`; meanings not documented here".

3. **nit**, `page.chart_view.key[no_fuel].note`: "Elexon sends `fuelType` as null". Silver cannot tell an explicit null
   from a missing key: `read_bronze` builds `pl.DataFrame(rows)` from the record dicts (`remit.py:62-76`), which fills
   absent keys with null. This is the pilot's "sends no field versus sends it as null" nit. I did not open bronze (my
   brief limits me to silver). Fix: "`fuelType` is empty: a missing value, not a fuel", or confirm `"fuelType": null`
   in one bronze body.

4. **nit**, `page.record.key` (hero **Key**, frame "Identifies a row"): [`mrid`, `revision_number`, `timestamp_utc`]
   is not unique. 6 rows repeat on every column, two of them in the chart and notebook window
   (`0000000000000001-ELXP-RMT-00000012` rev 12 at 15 Sep 10:31:08; `48X000000000357G-ELXP-RMT-00000516` rev 16 at
   16 Sep 17:39:53).
   - Each duplicate pair sits inside one silver file, mid-chunk, not at a 23-hour window boundary. So the writer's
     "inclusive `publishDateTimeTo`" guess does not explain them, and the cause (vendor or pagination) is unknown.
   - No column set is unique, and the grain line does warn about re-sends, so this is a nit. Consider "Elexon can
     re-send a revision, sometimes identically" in `facts.grain`, or leave as is.

5. **nit**, `page.record.fields.timestamp_utc`: "...(`publishTime`); not an event time". The lineage column
   `event_time` equals `timestamp_utc` on all 2,291 rows (`(event_time == timestamp_utc).all()` is True). A reader who
   unfolds the frame sees `event_time` holding this very value. Fix: "not the outage's start or end".

6. **nit**, `page.related[elexon/uou2t14d].note` and `page.related[elexon/fou2t14d].note`: "Availability per BM unit 2 to
   14 days ahead" and "Availability by fuel type 2 to 14 days ahead" say what those datasets are, not how they relate
   (brief, related: "Say how they relate, not what they are called"). The other two notes do relate ("that `asset_id`
   joins to", "for the same units"). Fix: for example "Forward availability for the units these messages name".

## The three checks asked for

### 1. Revision handling

- **Silver keeps every revision.** Confirmed. The transformer does no dedup: `remit.py:44` `APPEND_ONLY = True`,
  `:46-50` ("NO unique(subset=...)"), and `transform()` ends in `.select(available).sort("timestamp_utc")` (`:176-177`).
  Silver's natural time is `timestamp_utc` (`publishTime`, `:118-123`); the entity key for the latest view is `mrid`
  alone (`:50`).
- **Re-sends (62 extra rows).** Confirmed: 42 pairs, 62 extra rows, 3 pairs mixing `Active`/`Dismissed`, 6 exact
  repeats. 41 of the 42 pairs differ in `timestamp_utc`, so these are separate vendor publications. 26 pairs differ
  in content beyond publish time (`event_end_time` 19, `event_start_time` 7, `message_heading` 6,
  `available_capacity_mw` 3, `event_status` 3, `fuel_type` 2 and others). "Elexon can re-send a revision number with
  changed content" (`what_it_is`, `facts.grain`, `fields.revision_number`) stands.
- **Notebook lead, "its newest silver write then highest revision".** This is what the code does:
  `latest_views.py:100-103` (`order_columns=("available_at", "revision_number")`), rendered as
  `QUALIFY ROW_NUMBER() OVER (PARTITION BY "mrid" ORDER BY "available_at" DESC NULLS LAST, "revision_number" DESC NULLS
  LAST) = 1` (`:261-270`).
  - `available_at` is the transform-run stamp: one value per silver file. It increases with the partition date here,
    because the September files were written by one run in date order (18:32:07.72 to 18:32:07.90 UTC).
  - `query()` then filters the view on `timestamp_utc`, from 13 Sep 00:00 UTC up to but not including 22 Sep 00:00
    UTC (`_get_method_registry.py:92-96`), and drops lineage. "Kept if published in the window" is right.
- **Soundness (not a page defect; for the seat, as a gridflow issue).** The lead describes the rule accurately and the
  page never claims the view follows publish order, but the rule is not a total order:
  - 11 messages have more than one row at their top (`available_at`, `revision_number`), so the pick is arbitrary. 4
    of these were published in the notebook window. One, `23X--140120-SCCN-NGET-RMT-00021242` (T_SCCL-2), has rev 1
    twice in file 20260920: `Fossil Gas` ending 24 Sep and null ending 28 Sep.
  - 12 messages get a row published earlier than the message's latest publish time (ties plus the inversions in
    finding 1).
  - Order depends on write time. If a reader re-transforms an earlier date after a later one, the older file wins.
  - Suggested gridflow fix (the writer's open question 1): add `timestamp_utc DESC` to the order, or rank it first.

### 2. The chart

- Counts reproduce: `UnavailabilitiesOfElectricityFacilities` rows with `timestamp_utc` in [13 Sep, 22 Sep) give 1,353
  rows and 541 `mrid`s. The highest revision per `mrid`, mapped by the spec's `group_map`, gives gas 246, no fuel type
  99, biomass 79, wind 70, hydro 31, nuclear 8 and other 8, total 541. This matches the series `values` and provenance
  (`rows_matched` 1353, `duplicates_dropped` 812, `rows_used` 541), and the alt text.
- Tie case: 3 `mrid`s have their top revision twice in the window; 1 has differing fuel (SCCN-00021242 above). Distil
  keeps the last row after a stable sort on `revision_number` (`distil.py:282-284`), and silver files are sorted by
  `timestamp_utc`, so it takes the later publication (null). That puts it under "No fuel type": 246/99, not 247/98.
  Deterministic, and it matches a publish-latest pick. The caption's "fuel type of its highest revision there" is
  slightly loose for this one message; not worth a finding.
- The caption says what is counted: "A count of messages, not of outages in force or MW", with dataset, filter
  (unavailability messages), window (13 to 21 Sep 2026 UTC) and dedup. The `other` series is khaki for the vendor code
  `Other` only. `null` and hydro are unpainted hatches. No non-additive column is summed.
- Key notes: "Pumped units here send generating and pumping sides separately" holds. Every pumped-storage asset in the
  window (CRUA-1/2, DINO-3/4/5, FFES-3, FOYE-2) has both `Production unavailability` and `Consumption unavailability`
  messages. The writer's report adds "with the same window", which is not true for 10 of 33 windows, but that phrase is
  not on the page.

### 3. The seven body corrections

| # | Correction | Verdict | Evidence |
|---|---|---|---|
| 1 | Dedup key: none in transformer; read-time `_latest` by `available_at`, `revision_number` | correct | `remit.py:44-50`; `latest_views.py:100-103` |
| 2 | Point-in-time field `timestamp_utc` (vendor `publishTime`) | correct | `remit.py:118-123`; same form as `temp.md`'s note |
| 3 | `timestamp_utc` row: from `publishTime`; `published_at`/`created_time` not written | correct | `remit.py:85-86`, `:149-177` (not in `output_cols`) |
| 4 | `fuel_type` values like `Fossil Gas`, not FUELHH codes | correct | silver `value_counts`: 8 vendor strings + null |
| 5 | `ingested_at` = silver transform time | correct | `remit.py:141-146` `datetime.now(UTC)` |
| 6 | Silver sample `timestamp_utc` = `2026-05-06T23:09:05+00:00` | correct | the note's own bronze sample `publishTime` |
| 7 | Revisions bullet: re-send counts, then "32 steps" | first half correct; second half wrong | finding 1 |

Each is a minimal span with a `file:line` or measurement; the curl example is untouched.

## Other checks (no finding)

- **Build and detector:**
  - `gridflow-build --only elexon/remit` passes.
  - The staged spec and authored override are absent; the series has `spec_origin: vault`.
  - The detector returns only the accepted advisory `em-dash-overuse` ("92 em-dashes"). The page has 0 `—`, 0 `–`,
    0 `→`, 0 middle dots. 88 of the `--` hits are in `<td>` cells (EIC and `mrid` padding), the rest in other ID
    spans, plus the four CLI flags.
- **Raw feed:**
  - Base URL `sources.yaml:3`; path `/datasets/REMIT`, `publishDateTimeFrom/To` in `%Y-%m-%dT%H:%M:%SZ`, `page`
    (`endpoints.py:33-36`, `:234-240`, `:300-313`).
  - 23 h chunks (`client.py` chunk loop, `while current < end`). From `--start 2026-09-13`, chunk 7 is 18 Sep 18:00 to
    19 Sep 17:00, and silver file 20260918 spans 18 Sep 18:10 to 19 Sep 16:27. "One silver file can span two dates"
    holds (file 20260913 runs 13 Sep 00:34 to 14 Sep 21:33).
  - Ingest end exclusive (last chunk 21 Sep 15:00 to 22 Sep 00:00, partition 21); transform end inclusive;
    `PARTITION_SOURCE_OFFSETS = (0,)` (`base.py:417`).
- **Frame and guide:**
  - The eight rows are real (`generated_by: gridflow-sample`): revisions 5 to 12 of `...00218399` (T_PEMB-41),
    published 18 and 19 Sep, as the caption says.
  - The guide lines hold against the rows: end time moves; unavailable 394 with normal 465 and available 0;
    `Active` then `Inactive`; `related_information` states each change; `NO_ASSET` in 11 rows (all
    `OtherMarketInformation`); `asset_type` null in 650 rows.
  - 23 guide lines cover the 23 non-pipeline columns.
- **Notebook:**
  - Written by `scripts/run_notebooks.py`; cells read-only, no errors.
  - Cell 4 shows UK-time offsets; the plot label says UK time.
  - `plot_alt` matches `remit-5.png`: T_HRTL-1 from early May to about 23 Sep, T_HEYM11 two back-to-back bars to
    Jan 2027, and the others in Sep and early Oct.
  - `needs` (13 to 21 Sep) matches the commands.
- **No local data** on the page: grep of the page text for `locally`, `held`, `our `, `since 20`, `rows`, `% of`,
  `live` finds only template text (help card, "Schema and sample rows"), "delivery", "hour" and the vendor value
  `Unplanned`.
- **Screenshots** (headless Chrome, same-origin iframe wrapper on port 9745, profile
  `scratchpad/remit-review/chrome-profile`, server stopped):
  - 1440, 1024, 768 and true 390, each folded, and unfolded with the notebook open.
  - Nothing clipped or overlapping: hero scenery tops, chart, key (the hydro codes fit), raw feed, frame, guide,
    notebook panel, corner labels and related list.
  - The unfolded frame and the notebook's `df` output are horizontal scrollers by design (`.fw`, `.df-wrap`
    `overflow-x: auto`).
  - No stylesheet has a `prefers-color-scheme` or `data-theme` rule, so dark renders the same as light (site-wide,
    not this page).
