# Balancing Reserve requirement forecast: author round 2

Response to `balancing-reserve-auction-requirement-forecast-review.md` (REVISE: 2 majors, 8 nits). Writer, 2026-10-18.

## Gates

- Canonical note edited with the Edit tool; CRLF kept (554 lines, 554 CR). Mirror copied, `cmp` equal.
- `gridflow-build --only neso_data_portal/br_auction_requirement_fc_da`: success (budgets pass). Detector: `[]`.
- No artefact changed (chart spec, sample selection and notebook cells untouched; only page words changed). The
  build's digest check passed.
- Rendered page: "holds one", "next service day" and "one per day" no longer appear.
- Screenshots at 1440, 768 and a 390 px iframe after the edits: the reworded text (what it is, how it's used,
  caption, key note, raw-feed note, member lines, field guide) is fully visible, nothing clipped. Server on 9941
  stopped.

## Findings and what changed

| # | Severity | Field | Change |
|---|---|---|---|
| 1 | major | `what_it_is` | "...then the day-ahead refinement, whose file holds one delivery day and is replaced daily." became "...then the day-ahead refinement, in a file NESO replaces daily." |
| 1 | major | `notebook.lead` | Now: "Reads with `data.sql` from the `_latest` view, the newest capture, because NESO replaces the file daily and a dated `query()` finds rows only for the day it holds." |
| 1 | major | `family.members[0].differs` | "Day-ahead forecast; NESO replaces the file daily" ("for the next service day" dropped) |
| 2 | major | `how_used` | The window-label join bullet is replaced by "To join EAC results, convert `service_window_start_time` from UK local time to UTC." (12 words). The EAC comparison bullet comes first, the join second, the model-feature bullet third. The `timestamp_utc` point remains in its field line. |
| 3 | nit | `family.members[2].held` | "Its table includes the archive file, and NESO does not say when archived forecasts were published." (16 words) |
| 4 | nit | `record.select.columns` | Nothing to change on the page: silver names cannot be shortened, and the order already puts window, start and positive MW first. For the seat: at 768 no MW column shows before unfolding. |
| 5 | nit | template | Report only: the unfolded frame scrolls inside its own pane. |
| 6 | nit | template | Report only: the notebook preview breaks identifiers mid-word and truncates the tab label at 390 and 768. |
| 7 | nit | `chart_view.caption`, key note | Caption adds "from 23:00 the evening before" (38 words). Positive key note is now "Steps only at the four-hour EFA block edges from 23:00 this day: 200 to 600 MW." (16 words), which gives EFA its 4-hour, 23:00 meaning. |
| 8 | nit | `raw_feed.note` | Now: "From NESO's CKAN portal: `package_show`, then each file whole unless `last_modified` is unchanged; its name's hash prefix can change. Dates select nothing. Swap in any table's key." ("can change" is the note body's vendor wording.) |
| 9 | nit | `record.fields.service_window` | "Window number, `1` to `48`; spring drops `5`, `6`, autumn adds `5x`, `6x`" (from the note body: EAC explainer diagrams and archive rows) |
| 10 | nit | series JSON `Z` stamps | Report only: this is the template's `time_text` contract. Distil writes the parsed label with `Z`. Suggest the seat document that `time_text` x values are labels, not UTC. |
| body | cosmetic | "Files by disposition" | The ragged line break ("Two captures / do not make a vendor rule") is reflowed. No wording change. |

## For the seat

- Template (findings 4 to 6 and 10): first-view MW columns at 768; the unfolded frame scrolls; the notebook
  preview breaks words; `time_text` series carry `Z` on local labels.
- No gridflow or data defect. The archive-retention evidence in the first report (both archives unchanged across
  the 8 and 16 October captures) still stands as input to the two hold questions.

Summary: both majors and all page-level nits fixed in the note and mirror (`cmp` equal). Build passes, detector
`[]`, screenshots clean. The four template nits are reported to the seat, not worked around.
