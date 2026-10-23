# Demand Flexibility Service 2023/24: writer's report, round 2

Answers `demand-flexibility-service-review.md` (REVISE: 1 major, 2 nits). Writer, 2026-10-23.

## Fixes

1. **Major, `page.family.members[3].held`:** the old line ("NESO does not say when each window's requirement was
   first published") is replaced. The checker is right: the notification member has a dated "Requirement Published"
   notice for every delivery date. The new line says only what is missing: "The requirement file has no publication
   time; the notices give one only per date." That is 14 words; the checker's 17-word suggestion was over the
   16-word budget, so "of its own" was dropped. It renders as "Rows not shown: ..." under the member.
2. **Nit, `page.chart_view.alt`:** "Both fall from 2 February" now reads "Both series fall from 2 February".
3. **Nit, `dfs_required_mw`:** unchanged, per the seat's ruling (marked PROXY-SOURCED) to keep it from the summary in
   the frame and notebook. The summary is an eligible table; the hold is about publication time, not the values.

Neither edit touches the chart spec, record selection or notebook cells, so the series, sample and notebook
artefacts are unchanged and their digests still pass.

## Gates

- Mirror: `cp` then `cmp` clean; the note is CRLF on all 589 lines (round 1's "586" was a miscount).
- Build `--only neso_data_portal/dfs_utilisation_report_sum`: no errors (the 37-line "Known issues" warning is
  global).
- Detector: `[]`.
- No server or background process was started this round. The changes are one text line in the raw feed and the chart
  alt text, which a screen reader reads, so they cannot change the layout.

## Defects

None new.
