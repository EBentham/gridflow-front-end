# Demand Flexibility Service 2022/23 test events: writer's report, round 2

Page `demand-flexibility-service-test-events` (lead `dfs_test_events_utilisation_report_sum`). Writer, 2026-10-23.
Answers `demand-flexibility-service-test-events-review.md` (REVISE: 2 majors, 2 nits) as the coordinator directed.

## Fixes

| # | Finding | Change (canonical note `page:` block) |
|---|---|---|
| 1 | Major, `page.chart_view.alt`: "the last two days settle 0.725 and 1.01 MW" named the wrong days (the last two are 23 and 28 March; 0.725 MW is 21 March) | Now "Settled peaks at 269.0 on 21 February; it is 0.725 MW on 21 March and 1.01 on 28 March." To stay within 90 words, "of NESO Demand Flexibility Service test days" became "of DFS test days" (the page title names the service). I didn't use the suggested "falls to": it implies a direct drop from 21 February, but 15 and 23 March sit between at 231.355 and 235.695 MW. Alt is 90 words, within its budget (build passes). |
| 2 | Major, `page.family.members[3].held` was stronger than the evidence | Now the approved 2023/24 wording: "The requirement file has no publication time; the notices give one only per date." (14 words). Renders as "Rows not shown: The requirement file has no publication time; the notices give one only per date." |
| 3 | Nit, `page.chart_view.key[1].note` read as true of every window | Now "Volume of the accepted bids; on average above the requirement on 19 January and 15 March." (16 words; the chart draws daily means; 21 February's 18:00 window, 252.42 MW against 250, is under on the day's mean) |
| 4 | Nit, `page.record.fields.dfs_required` | Unchanged, per the coordinator (seat ruling, as on 2023/24). |

No chart spec, record select or notebook cell changed, so the series, sample and notebook artefacts are as in round 1
(the build's digest check passes).

## Checks

- Mirror: `cp` + `cmp` clean. The note is CRLF on every line (569 of 569; my round 1 figure of 559 was a miscount, as
  the checker noted). The diff against `origin/master` is 134 insertions, 0 deletions: the `page:` block only.
- Build `uv run --system-certs --extra build gridflow-build --only neso_data_portal/dfs_test_events_utilisation_report_sum`:
  passes, no errors. The first rebuild after the edits failed on the alt at 93 words; I tightened it to 90 and it passed.
- Detector on `site/hifi/data-sources/neso_data_portal/demand-flexibility-service-test-events.html`: `[]`. Real em dashes: 0.
- No server or background process started this round, per the coordinator; no new screenshots. The changes are
  wording only, in places that rendered cleanly at all four widths in round 1 (alt is not visible; the key note grows
  by two words and the held line keeps about the same length).

## Defects

No change from round 1: no new gridflow defect. The NESO clock-label ambiguity (28 March 2023 windows and 27 March
notices fall in British Summer Time but are labelled GMT) and the 17 January £4.50 summary cost difference stand as
reported in `demand-flexibility-service-test-events-author.md`.
