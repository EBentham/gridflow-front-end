# Writer report 2: `demand-flexibility-service-live-events`

Writer, 2026-10-23. Fixes for the checker's five nits (`demand-flexibility-service-live-events-review.md`, APPROVE).

## Fixes

1. `page.record.caption`: now names the table: "Report table: eight bids, 17:30 to 18:00 GMT on 23 January 2023, one
   Rejected."
2. `page.record.fields.total`: "Total volume submitted for grid supply points (GSPs) at D-1, MW (NESO)", so GSP is
   expanded on first use in the guide (`other` and `d0_other` follow it).
3. `page.record.fields.d0_north_wales_merseyside_and_cheshire`: "Event-day forecast, North Wales, Merseyside and
   Cheshire, MW; named with `and`, unlike D-1".
4. Notebook plot cell: x labels are date and window on two lines (`"\n"` join), so the five labels stand apart. The
   legend reads `requirement`, `D-1 procured`, `D0 procured`, `settled` (`set_axis` on the four columns). Values and
   colours are unchanged, so `plot_alt` still matches the image.
5. `page.notebook.lead`: "the first query cell converts `published_at` to UTC".

## Gates

- Canonical note edited with the Edit tool (CRLF kept), mirrored, `cmp` clean.
- Notebook re-run with `scripts/run_notebooks.py` (the plot cell changed): 5 cells, no errors, 1 image.
- `gridflow-build --only neso_data_portal/dfs_live_events_utilisation_report_sum`: no errors. Detector `[]`. Em dashes
  in page: 0. The four new strings are in the built page.
- Series and sample unchanged (no chart or select edits). No server or background process started.

## Defects

None new.
