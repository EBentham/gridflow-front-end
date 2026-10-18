# Review: dynamic-containment-data (lead dynamic_containment_dc_dr_dm_results)

Checker, port 9962. Build `--only neso_data_portal/dynamic_containment_dc_dr_dm_results` ran clean; detector `[]`;
mirror `cmp` identical; note diff touches only the intended hunks (CRLF intact, no em dashes or middle dots in the
`page:` block).

## Verdict: APPROVE (0 blockers, 0 majors, 5 nits)

## What I reproduced

- **Chart, from the complete 2026-10-08 file only** (not the series' own inputs): daily unweighted mean of one price
  per (service, efa_date, efa), DCL and DCH. All 778 DCL and 729 DCH daily points match the committed series (max
  difference under 0.0006, 0 mismatches). Spot days: 2021-09-16 DCL 17.000; 2021-11-04 DCH 6.492, DCL 9.477;
  2022-06-25 DCL 77.608, DCH 5.795; 2023-04-01 DCL 0.235; 2023-06-15 DCH 17.438; 2023-11-02 DCL 1.882, DCH 3.898.
  Blocks: 9,023 charted (4,658 DCL, 4,365 DCH); 19,211 blocks over all six services; none has more than one
  `clearing_price`, none null, so the dedup to one row per block loses nothing. 13 service-days have fewer than six
  cleared blocks (the caption's "over its cleared blocks" is right).
- **Alt text, every number:** DCL exactly 17.00 through 31 October 2021 (first change 1 November, 16.633); DCL max
  77.608 on 2022-06-25; 2023 has 306 dates, DCL under 2 on 145, min 0.235 (1 April); DCH max 17.438 on 2023-06-15,
  above DCL on 200 of the 306; DCH deciles 1.08 to 7.34; DCH first 2021-11-04 (49 null days before it).
- **Unit:** NESO's saved field info for the results table: "The cleared price per MW per hour", unit £/MW/h;
  `Cleared Volume` unit MW. DR from 2022-04-09 and DM from 2022-05-07 in the by-unit results (the summary table
  carries them from 2022-03-26 with zero cleared MW, consistent).
- **Truncated capture:** the 2026-10-16 file is a byte prefix of the 2026-10-08 file (`cmp -n 25461781` clean; end of
  the short file at line 224,001; 224,000 rows, last EFA date 2023-04-02). Every short-capture row (unit, date,
  block, service, MW, price) is present in the full capture. Page text, artefacts and rendered HTML contain no
  mention of the short capture, April 2023, or any 2026-10-16 path (grep of the built page: 0 hits).
- **Chart avoidance:** the series reads both files (`provenance.files` 2, 621,662 rows read) and dedups, so it does
  not literally avoid the short copy, but the result equals the full-capture-only result (above), and stays right if
  the short capture is removed. Frame: filtered to `capture_written_at` before 2026-10-09, so it shows only the
  complete capture; all eight rows match silver. Notebook: uses `query()` (date column `efa_date`, both ends
  inclusive, relation `_latest`: confirmed in gridflow_models `_get_method_registry` and `handles/source.py`). Window
  20 to 26 June 2022 returns 3,318 rows from either capture (full 3,318, short 3,318), so it runs and gives the same
  answer whichever capture `_latest` serves. Every cell output matches silver: 42 DCL and 42 DCH blocks; DCL 4.07 to
  69.95 to 24 June, 59.00 to 105.00 on 25 and 26 June (105.00 in block 5 of 25 June, the only 105.00); DCH 0.80 to
  8.90; block table values (units, MW, price) for 25 June identical. No error outputs; `generated_by`
  `scripts/run_notebooks.py`; cells are read-only; plot looks right (legend clear of the lines).
- **Held lines:** results summary dictionary: description "The cleared price per MW per hour", unit "£/MW": line is
  accurate. Linear dictionary: 21 `nP` columns £/MW, 11 MW (5P, 11P to 14P, 21P to 24P, 31P, 32P), descriptions give
  no hour basis: line is accurate and plain, no codes or planning words. The summary's `differs` (per service, EFA
  date and block) holds: no duplicate keys over 23,424 rows.
- **Body corrections:** (1) bronze holds one 2026-10-08 file per resource and a second results file from
  2026-10-16; the other four resources have no 2026-10-16 capture. (2) `client.py` `_FROZEN_CADENCE = timedelta(days=7)`
  and `_frozen_not_due` (due once the last capture or check stamp is 7 or more `end` days old); identical bodies are
  not stored (`_dump_member`, hash compare). (3) Two Parquet files in `year=2026/month=10/` for results (397,662 plus
  224,000 rows). (4) results `Service` text still says DLH and LFS; the linear dictionary `MarketName` defines
  DCL to DMH as written; "one price per block, 19,211 blocks" reproduced.
- **Retired-package history:** every history statement traces to the note's quoted NESO package page ("will no
  longer be updated", EAC successor), the vendor metadata "Update Frequency: Not Active", or the date range of
  NESO's own files (masterdata `delivery_date` 2020-10-02 to 2021-09-15; results `efa_date` 2021-09-16 to
  2023-11-02), the same form as the approved pages. Nothing is inferred beyond that.
- **Requests** match every sidecar `request_url` (four dump URLs, the masterdata resource download URL).
  Commands `--last 24h` match the approved showcase pages; "window must end recently" matches the 48 hour check in
  `_assert_window_admissible`.
- **Screenshots** at 1440, 1024, 768 and a 390 px iframe plus a live 390 view: nothing clipped or overlapping; no
  text element outside the 390 viewport (only hero scenery paths); chart, held lines, frame, guide and notebook all
  legible. The notebook tab label clips at 390 (already on the seat's template list).

## Findings (all nits)

1. **nit** `page.raw_feed.note`: "Retired: re-checked at most weekly; unchanged bodies are not stored again." True
   for the four datastore dumps. The masterdata upload is not under the weekly cadence: it is compared with its CKAN
   `last_modified` on every run and only downloaded when that changes (`client.py` `iter_members`, the upload branch
   after the dump branch). Suggest "each dump is re-checked at most weekly".
2. **nit** Canonical note body, `Cadence` ("gridflow has **one capture per resource** (2026-10-08)") and the results
   section ("one capture (2026-10-08, 45,481,922 bytes)", a line above the corrected "Silver:" sentence) still say one
   capture for results; they now contradict the corrected "Files by disposition" and "Silver" text. Not on the page.
3. **nit** `page.notebook.lead`: "The second cell sums units' MW per block". In the notebook as shown, the setup
   cell is [1], the query is [2] on the page (and [3] in the notebook) and the summing cell is [4]; "second" reads as
   the query cell. Precedent exists (EAC BR: "the first query ... the second"), so low weight; "The next cell" would
   be unambiguous.
4. **nit** `page.record.fields.timestamp_utc`: "Start of the EFA date in UK time, as UTC" can be read as the start of
   the EFA day, which begins at 23:00 the evening before. The code (`casting.py`, `date_sp1`) stamps UK midnight at
   the start of the calendar date (2022-06-24 23:00Z for 25 June in summer; 00:00Z in winter). Suggest "UK midnight
   at the start of the EFA date's calendar day, as UTC; not the block start".
5. **nit** `page.family.members[0].differs`: "accepted units only" is an inference (no row has zero MW; NESO's
   `Cleared Volume` text says the volume "accepted"); NESO does not say rejected units are excluded. Safe to keep
   (the caption says "cleared"), but "NESO's cleared MW per unit" avoids a universal.

## Not findings (seat items)

- The chart reads both results captures; it equals the complete-capture result today. If the seat wants literal
  avoidance it can add a `capture_written_at` filter to `chart.filter`, but nothing is wrong now.
- A family page does not print the `package_show` request line (known template limit).

## Process note

The shared scratchpad already held other agents' `chk*.py` files; mine reused the names `chk1.py` to `chk8.py` in
the scratchpad root and may have overwritten earlier scratch scripts of that name (temp files only, nothing in the
repos). My screenshots are in the `dcchk9962` subfolder. The server on 9962 is stopped.
