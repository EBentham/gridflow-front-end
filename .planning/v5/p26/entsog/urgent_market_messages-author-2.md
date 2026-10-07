# entsog/urgent_market_messages: writer report, round 2

Writer: Opus 5.5 · high, 2026-10-07. This round answers `urgent_market_messages-review.md` (3 majors, 7 nits). All
ten findings are fixed.

## Status

- **Build:** `gridflow-build --only entsog/urgent_market_messages` passes; `anatomy_errors` is `[]`.
- **Detector** (absolute path): only the accepted `em-dash-overuse` advisory ("49 em-dashes", from codes and CLI
  flags). The page has 0 real em dashes.
- **Removed wording:** "still serves" and "not an edit" no longer appear on the page.
- **Mirror:** `cp` then `cmp` shows byte-equal; the note is CRLF (393/393).
- **Artefacts:**
  - The notebook re-ran with the new first cell (6 cells, no errors). Its outputs are unchanged: event types
    48 / 47 / 5 / 1, and the plot is the same 15 bars.
  - The series and sample are unchanged (the chart spec and `record.select` were not edited), and the build digest
    check passes.
- **Screenshots** (`...\scratchpad\umm\shots\`):
  - `r2_w390.png` (true 390 iframe) with sheets `r2_s390_0..1.png`, and `r2_w1440.png`.
  - The new guide lines wrap cleanly; nothing is clipped.
  - Server 9879 is stopped.

## Majors

1. **Silver is not a history; "still" dropped.**
   - `summary`: "...other notices, one row per version ENTSOG sends."
   - `what_it_is`: "Silver holds only the newest fetch: a message ENTSOG stops sending leaves silver at the next
     transform, so silver is not a history; bronze keeps each fetch." (57 words)
   - The unobserved "still serves / some threads without their latest" sentence is gone from `what_it_is`. The
     observation moved, scoped, to `record.fields.is_latest_version`: "some threads in this fetch, Kiemenai here, lack
     `Yes`".
   - `raw_feed.note`: "Bronze keeps each fetch under its UTC day; `transform` rewrites one silver file from the
     newest fetch only."
   - `how_used[1]`: "Matching current messages to flows through connection point EICs; some do not resolve." This is
     tied to current messages and is no longer a history use.
   - `record.fields.timestamp_utc`: adds "not when gridflow fetched it".
   - `notebook.lead`: "...from `silver_entsog_urgent_market_messages`, the newest fetch only: each version whose
     publication time (`timestamp_utc`) falls in the window, both dates included."
   - Evidence: `endpoints.py:199-206`, `generic.py:106-116,128-129,252-259,284`.
2. **Capacity values stated.**
   - `unavailable_capacity`: "this fetch includes placeholders 10000000000 and 1".
   - `available_capacity`: "sent as text; some versions send all three as 0" (ten NaTran Deutschland `26082121X...`
     versions).
   - `technical_capacity`: "Here available plus unavailable; one version fetched reads a thousandth of its successor"
     (RC Basel v001 against v002).
   - The mixed-unit warning on `unit_measure` stays.
3. **`last_update_date_time`.**
   - Now: "Update stamp as sent; five rows here, about a quarter overall, share one value".
   - Evidence: 35 of 133 rows; 5 of the 8 shown.
   - No cause is asserted. "Not an edit" and "several" are gone. The caption still says ENTSOG's manual defines no
     fields.

## Nits

4. **`plot_alt` and the plot cell:**
   - `plot_alt` now says "15 capacity messages flagged Active at the highest version sent". It names the top bar:
     "VIP Oberkappel (a thread sent without its latest version)".
   - The cell gains a comment: "status at the highest version sent; is_latest_version can be No throughout".
   - It still does not filter on `Yes`.
5. **`how_used[0]`:** "at a point or facility".
6. **Flows join:**
   - `how_used[1]` names the join through connection point EICs and says some do not resolve.
   - `related[entsog/physical_flows]`: "Daily flows by point key, reached through connection point EICs".
7. **Notebook window:** the first cell is now `from datetime import date` then
   `data.entsog.query("urgent_market_messages", "2000-01-01", date.today())`, so nothing published later is cut off.
8. **Manual citation:** new body gotcha, "No field definitions": the manual v2.1 lists `/urgentMarketMessages` only
   as "UMM Data, Urgent Market Messages" and defines no response fields.
9. **Body numbers:**
   - "three minutes" becomes "2 min 27 s".
   - "one 65 days later" becomes "two about 65 days later".
   - RC Basel now names the columns: unavailable / available / technical 26.57 / 239.2 / 265.77 against
     26,578 / 239,200 / 265,778 kWh/h.
   - Added the ten all-zero `Gas` versions.
   - The gotcha heading changed from "is not an edit time" to "is often one shared stamp", with "whether the shared
     value reflects an edit is unknown".
10. **`message_id`:** "One per version: `thread_id` and `version_number` joined by `_`, as sent".

## Defects

Unchanged from `urgent_market_messages-author.md`, with one correction to the capacity defect. RC Basel version 001
sends unavailable / available / technical 26.57 / 239.2 / 265.77 kWh/h against 26,578 / 239,200 / 265,778 in
version 002. Ten NaTran Deutschland `Gas` versions (`26082121X...`) send all three capacities as 0.

Summary: all 3 majors and 7 nits are fixed; the build is clean, the detector shows only the accepted advisory, the
mirror is byte-equal and the notebook re-ran with unchanged outputs; ready for re-check.

Nits fixed (review 2): `unavailable_capacity` now reads "this fetch includes apparent placeholders 10000000000 and 1"; `last_update_date_time` now reads "As sent; five rows here, about a quarter of this fetch, share one value" (14 words). Mirror `cmp` byte-equal (CRLF 393/393), `anatomy_errors` `[]`, build passes, detector only the accepted em-dash advisory.
