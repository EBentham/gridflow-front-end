# Review: `demand-flexibility-service-live-events` (DFS 2022/23 live events)

Checker, 2026-10-23. Lead `dfs_live_events_utilisation_report_sum`. Front-end worktree `C:\gridflow-wt\fe-neso-dfs`, vault
worktree `C:\gridflow-wt\vault-neso-dfs`.

## Verdict: APPROVE

No blocker or major. Five nits, all optional. Build `--only neso_data_portal/dfs_live_events_utilisation_report_sum`
ran clean (only the general caveat-grammar warning, not tied to this page); detector `[]`; mirror `cmp` clean; 0 em
dashes in the built page; no local-data, planning or "live"-framing words in the `page:` block (the only "live" hits are
the package name, file names and "live events only").

## What I reproduced

- **Chart.** Silver report, one capture, 170 rows, 170 distinct (`date`, `window_from`, `unit`) keys, so no double count
  (series provenance: `duplicates_dropped` 0, `files` 1, `rows_used` 33). Filter 23 January, 17:30, Accepted gives 33
  bids, 19 providers; per-provider sums match the committed series value for value (Octopus 191.029 = 63.675 + 63.677 +
  63.677). Total 336.8888 = summary `dfs_procured` 336.89 for that window, so the caption's "336.89 MW to two decimals"
  is true. Adding MW across units inside one half-hour is legitimate (and is how the summary is built).
- **One window is a fair, stated choice.** Title, caption ("One of five windows") and alt all name the window. It is the
  largest D-1 total of the five (323.81, 336.89, 288.62, 314.19, 327.18) and the same 19 providers bid in every window,
  so the provider mix is representative; Octopus is 156 to 191 MW across windows. Read from the report as the brief
  asked; the lead's five rows can't carry a per-provider bar.
- **Alt text and key.** Octopus 191.03, Gridbeyond 25.54, Drax 23.0, EON Next 18.0, British Gas 12.0; "other 14 have 11.0
  or less" (Engie 11.0); "six of them 2.3 or less" (2.3, 2.0, 1.02, 1.0 x3); "three 1.0" (Equiwatt, EvDOT, Zenobe;
  VpowerU8lectric is 1.02). All true against the series file. Key has one series, no numbers to check.
- **Provider labels.** `group_map` shortens 20 names (19 present in this window); the caption says "short names; the
  rows give NESO's"; the frame's `dfs_provider` column shows NESO's run-together spellings (Drax, EDF, Oaktree, Octopus,
  Orange Power appear there). Fits at 390 (checked in a 375 view, no clipping).
- **Times.** Registry header `From GMT`/`To GMT` for the requirement; NESO field-info snapshot `20261008T114228Z` gives
  `From`/`To` the comment "GMT" in both the report and the summary. All windows are 23 and 24 January 2023, when GMT is
  UK clock time, so "Windows are GMT labels, also UK clock time in January" is true and correctly scoped.
  `timestamp_utc` is 2023-01-23T00:00Z (`date_sp1` recipe), and the guide says "not the window start". `published_at` is
  CKAN `last_modified` read as UTC (silver 2026-07-27 13:22:45.267 UTC for the summary, same digits as the sidecar).
- **Notebook.** Written by `run_notebooks.py`, read-only cells, no errors. Cell 3 converts `published_at` to UTC; output
  shows `+00:00` and the same digits as silver (July, so unconverted it would show BST). Rows equal silver: requirement
  323/336/274/330/341, D-1 323.81/336.89/288.62/314.19/327.18, D0, settled. Cell 4 (top five providers) equals the
  chart's top five; Octopus D0 106.61 against D-1 191.03 is real (53.31 + 26.65 + 26.65). The plot is grouped bars of
  four measures side by side per window, nothing summed. `plot_alt` numbers all true: 23 January D-1 323.81/336.89, D0
  224.66/232.98, settled 271.73/294.61; 24 January D0 minus D-1 is 0.79, 1.98, 3.09 (within 3.1); settled 233.12 to 286.93,
  below D-1 in all five windows.
- **Note fix.** Both `TODO: verify` edits are right. Dictionary text: report D0 columns "Forecasted volume to be
  delivered for GSP on day of event 10:00GMT", `D0 Total` "Total forecasted volume to be delivered on day of event
  10:00GMT"; summary `D0 DFS Procured`/`D0 Bids Accepted Total Cost` "based on provider submissions on the day of the
  event at 10:00 GMT". "The report is updated around 10:00 GMT on that day" is supported by the package notes. Smallest
  span changed; no unrelated rewrite.
- **Captures.** One bronze capture and one silver file per member, all 2026-10-08, none recaptured. Bronze data rows:
  requirement 5, notifications 7, report 170, summary 5 (headers as the registry; BOM and CRLF only). Requirement
  `last_modified` 2023-01-23T14:59:08Z is before the first window (17:00 GMT), so "last changed before any window" holds.
- **Raw feed and commands.** The four request URLs match the bronze sidecars (package, resource id, file name). Command
  shape and `--last 24h` match the approved showcase and `client.py` (end more than 48 h before now is refused).
- **Related.** Showcase starts with a 29 November 2024 archive (winter 2024/25); 2023/24 note says Live and Test share
  each file; Test events: no shared delivery date with Live (note, K-DFS-FACTS). All notes 12 words or fewer.
- **Dedup key.** Seat's extra item: the page block writes `dedup: {on: ...}` unquoted. Raw PyYAML does read the key as
  boolean `True`, but `page_fields._jsonable` (lines 419 to 420) maps it back to `"on"` for both `chart` (line 649) and
  `record.select` (line 560). I ran `parse_page_fields` on the note: no errors, both come out `{'on': ['date',
  'window_from', 'unit'], 'order_by': 'published_at'}`. The committed series spec carries `"on"`, the distil and sample
  code read `["on"]` without error, and the digests pass. The build neither ignores nor misapplies it. Not a finding
  (the seat confirmed: the build maps the `True` key back to "on", and many pages write it unquoted).

## Findings

1. **nit** `page.record.caption` (rendered frame header). The frame is drawn from the report table, but the visible
   caption ("Eight bids for 17:30 to 18:00 GMT on 23 January 2023, one of them Rejected.") does not say so; the table
   name appears only in the frame's `aria-label`. The page's lead is the five-row summary, so a reader can wonder why
   the frame has 48 columns and a `unit`. The word "bids", `shape: (8, 48)` and the grain fact ("the report adds DFS
   unit") make it guessable. Suggest: "From the report table: eight bids for 17:30 ... one of them Rejected."
2. **nit** `page.record.fields.total`, `other`, `d0_other` (guide). "GSP" is used and never expanded (grid supply point,
   NESO's term). Suggest "grid supply points (GSPs)" once, in `total`.
3. **nit** `page.record.fields.d0_north_wales_merseyside_and_cheshire`. "a second spelling" is unclear; the point is that
   this column's name has "and" where the D-1 column's does not. Suggest: "...Cheshire, MW; the name spells it with
   'and', unlike the D-1 column".
4. **nit** notebook plot (`dfs_live_events_utilisation_report_sum-5.png`). The five x labels ("2023-01-23 17:00 ...")
   sit about one space apart, so they read as one run-on line, and the legend uses raw column names. Legible, so only a
   nit; the image also shrinks to about 285 px wide at 375, which is a template matter.
5. **nit** `page.notebook.lead`. "the first cell converts `published_at`": the conversion is the first authored cell, but
   the panel numbers it [3]. Sibling pages use the same wording; "the first query cell" would be exact.

## Not findings

Template limits (column-guide key wrapping at 1024, the one-category-column `bar`, 8000 px wide frame) are seat items.
The writer's blank 1440 x 9000 capture was a capture artefact; my pane screenshots at 1024 and 375 of the hero, chart,
folded and unfolded frame, guide and notebook panel showed nothing clipped or overlapping (the SVG scenery paths
overflow only inside their clipped containers; no horizontal page scroll at 375).

Process: server started on 9875 with PID 9483 recorded and stopped by that PID. Scratch scripts in
`...\scratchpad\dfs-live-checker\`. No files written other than this review; the build re-rendered the gitignored page.
