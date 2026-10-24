# Embedded register: review (checker, round 1)

Page `neso_data_portal/embedded-register`, table `embedded_register`. Checked 2026-10-24 against local silver (Polars,
read only), gridflow `client.py`, the canonical note diffed against `origin/master`, the artefacts, the built page and
screenshots (1440 px; the site has no dark theme).

**Verdict: REVISE** (0 blockers, 2 majors, 4 nits). Both majors are wording fixes; every number reproduced.

Gates: `gridflow-build --only neso_data_portal/embedded_register` passes (spec digests match); detector `[]`; 0 em
dashes in the built page; mirror `cmp` identical to the canonical note; the four related links resolve.

## What reproduced

- **Chart.** Silver filtered to `published_at` = 2026-10-16T18:05:22Z, `project_number` dedup (562 rows in, 562 out,
  0 dropped), `mw_increase_decrease` summed per grouped plant type: storage 4,853.48, mixed 2,019.86, onshore wind
  1,881.78, solar 1,106.14, biomass and waste 138.80, gas and thermal 106.16, hydro/tidal/wave 85.25; total
  10,191.47 MW. Matches the committed series and the alt text (the seven rounded bars sum to 10,191). The sum uses the
  per-stage MW column; summing the cumulative column instead would give 5,131 / 2,120 / 4,127 / 1,167 / 273 / 471 /
  538, so the page avoids a real trap. All 25 plant-type strings map explicitly (13 contain `;`, all to "mixed").
  Title, caption, axis and alt state the unit (MW), the file date and the aggregation. Per-bucket checks: biomass and
  waste is Waste 138.8 plus Biomass 0.0; gas and thermal is CCGT 65.26 + gas reciprocating 39.90 + CHP 1.0 + Thermal
  0.0; mixed is 1,812 MW storage with solar or wind (of 2,020).
- **Captures.** 561 rows / 561 distinct `project_number` (published 2026-10-06T10:47:45Z, written 8 October) and
  562 / 562 (published 2026-10-16T18:05:22Z, written 16 October); 540 rows identical across all 14 vendor columns;
  one project added (`PRO-001297`), none removed. Bronze bodies: BOM, CRLF, 562 and 563 lines (561 and 562 rows),
  92,325 and 92,625 bytes.
- **Running total.** Per project, `cum_sum(mw_connected + mw_increase_decrease)` ordered by stage equals the
  cumulative column on all 31 staged rows in both captures (0 mismatches at 0.01 MW); all 531 unstaged rows of the
  16 October file equal their own two columns. 17 staged rows differ from their own two columns in both captures.
- **NGET.** `host_to` in the 16 October file: SHET 352, SPT 209, NGET 1 (`PRO-001297`, Grimsby, CCGT, 0 connected,
  40 MW contracted, no date, Under Construction/Commissioning).
- **Dates.** 129 rows dated before 16 October (128 not `Built`, one `Built`: `PRO-000902`, 2022-10-31); 217 blank
  dates (216 on `Built` rows plus `PRO-001297`). Of the chart total, 2,631 MW sits on rows dated before the file and
  40 MW on the undated row.
- **Notebook.** Cells ran on `silver_neso_data_portal_embedded_register_latest`; status sums equal my Polars sums
  (Scoping 7,448.3, Built -5.5, Consents Approved 1,813.7, Awaiting Consents 817.0, Under Construction 118.0). The
  `plot_alt` figures hold (2026 1,383; 2033 1,286; 2027 1,186; years 2019 to 2036 without 2020; 2019 to 2025 carry
  MW; from 2030, 3,786 of 4,358 MW is Scoping).
- **Code claims.** `iter_members` skips an upload member as `unchanged` when the newest capture carries the live
  `last_modified` (`client.py` 1749-1765). The note's cadence arithmetic (6 October a Tuesday, 16 October a Friday)
  is right.

## Findings

1. **major** `page.record.fields.mw_increase_decrease`, `page.chart_view.caption`, `page.chart_view.key[wind].note`,
   `page.record.caption`: the sign is worded as NESO's, and as plain fact elsewhere. The field line reads "or be
   removed when negative, at a future date (NESO)": NESO's words are "contracted to connect or be removed at a future
   date"; "when negative" is the writer's reading, not NESO's (the note body says so; the page does not). The caption
   ("One 5.5 MW decrease is netted"), the wind key ("Paul's Hill's contracted 5.5 MW decrease") and the frame caption
   ("a contracted decrease") assert it flat. The reading is sound (field name "MW Increase / Decrease", comment
   "0MW unless the capacity is due to increase or decrease", and 70.0 + (-5.5) = 64.5 on `PRO-000902`), so the fix is
   attribution, not removal. Also "at a future date" sits beside a frame row dated 2022-10-31 and the line
   "some shown are past". Suggested field line: "MW contracted to connect or be removed (NESO); we read a negative as
   a removal". Caption: "One negative 5.5 MW entry, read as a removal, is netted." Wind key: "net of one negative
   5.5 MW entry (Paul's Hill), read as a removal". Frame caption: "a negative entry".
2. **major** `page.how_used[1]` and `page.record.fields.cumulative_total_capacity_mw`: the running-total reading is not
   worded as measured, and the two register pages word it differently. The how-used line says
   "`cumulative_total_capacity_mw` counts earlier stages again" as a flat rule; the guide says "here each stage adds
   the earlier ones". NESO says only "across all stages". The reading holds on 31 of 31 staged rows in both files, so
   scope it to that. The TEC page's guide reads "NESO: total across all stages; in these rows, the running total to
   this stage" and its body says "measured on the 2026-10-08 capture; the vendor does not state this rule". Use the
   TEC wording: guide "NESO: total across all stages; in these rows, the running total to this stage"; how-used
   "Sum `mw_connected` and `mw_increase_decrease`; in these files the cumulative column is a running total, so
   summing it counts earlier stages again." Rubric 1 bars measured-on-our-copy universals.
3. **nit** `page.record.fields.mw_effective_from`, `page.chart_view.caption`: the two date oddities are only in the
   note body. The page says "some shown are past" and "whatever the contracted date", but not that 129 of the file's
   562 rows are dated before 16 October, or that a 40 MW non-built row (`PRO-001297`, null in the frame) has no date.
   Past-dated rows carry 2,631 MW of the 10,191 MW charted, so a reader sizing a pipeline needs it. Suggested field
   line: "Date the MW change is contracted to take effect (NESO); 129 rows of the 16 October file are dated before it,
   and one non-built row is blank".
4. **nit** note body, gotcha 5 (`embedded-register.md` around line 436): "all 215 blanks are on `Built` rows; 2 of the
   217 `Built` rows do carry a date" is the 8 October capture's count and is unscoped. In the 16 October file it is
   216 blanks on Built rows and 1 dated Built row (`PRO-000886` lost its date, 2022-02-15 to blank, between files).
   The writer's added sentence follows it, so scope the old figures to the 8 October capture.
5. **nit** note body, `MW Increase / Decrease` entry (line 295) and gotcha 4 (line 435): "A negative value is a
   contracted removal" and "is a contracted removal" are stated as the vendor's rule. Mark as our reading, as in
   finding 1.
6. **nit** `page.chart_view.key[mixed].note`: "mostly storage with solar or wind" is true (1,812 of 2,020 MW) but the
   bucket also holds nine rows (197.9 MW) whose plant type includes `Demand`. Add "or demand".

## Checked, no finding

- Notebook: `data.sql()` on `_latest` with the right lead. The notebook shows `published_at` as `19:05:22+01:00`
  (local time), against UTC in the frame and guide. The same shows on approved pages (for example
  `historic_generation_mix`, `eac_results_summary`), so a template item, not this page's.
- The `NGET` row: stated, dated (16 October file), set against NESO's "Scotland" text and the dictionary's
  `SHET or SPT`, and not explained away. Frame and guide show it.
- Frame (8 rows, 22 columns) and column guide (key first, 17 other lines; the four lineage columns omitted as
  elsewhere); `project_number` named as the key; 16 October rows only.
- Related links: four, all resolve; TEC "same columns plus `Agreement Type`" is right (15 columns against 14); GSP
  link note holds (348 of 562 sites name a GSP); interconnector note matches that page's summary.
- Raw feed URLs, `--last 24h` form, "skipped while `last_modified` unchanged" match `client.py`.
- The body correction counts I re-derived: 562 rows / 545 `project_id`; 13 date changes, 10 gate changes (blank to 2),
  4 status changes; status 251/217/62/26/6; gate 56/51/455 (1/2/blank).

## Defects (for logging)

None new. The writer's NESO items stand as reproduced: the `NGET` row in a register NESO calls Scotland-only, 129
past-dated rows and one undated 40 MW non-built row against the dictionary comment, and no capture of any file between
8 and 16 October.

## Round 2

**Verdict: APPROVE.** All six findings are fixed on the rebuilt page and in the note; nothing new.

Gates: `gridflow-build --only neso_data_portal/embedded_register` passes; detector `[]`; 0 em dashes in the built page;
`cmp` of the canonical note and the front-end mirror identical.

1. Sign (major): fixed. Guide "MW to connect or be removed (NESO); negative read by us as a removal"; caption "One
   negative 5.5 MW entry is read as a removal (70 + (-5.5) = 64.5) and netted"; wind key "net of one negative 5.5 MW
   entry (Paul's Hill), read as a removal"; frame caption "a negative entry". No line calls it a plain decrease and
   "at a future date" is gone from the guide.
2. Running total (major): fixed. The guide for `cumulative_total_capacity_mw` is "NESO: total across all stages; in
   these rows, the running total to this stage", word for word the TEC page's phrase. How-used now reads "in these
   rows the cumulative is a running total" (shorter than my suggestion, still scoped and not a flat rule).
3. Dates (nit): fixed. Guide "Contracted date (NESO); 16 October file: 129 already past, one 40 MW row blank"
   (reproduced: 129 past, `PRO-001297` blank at 40 MW).
4. Stale counts (nit): fixed. Gotcha 5 scopes 215 / 2 to the 8 October capture and gives 216 / 1 for 16 October. I
   reproduced the `PRO-000886` explanation: Built both times; 8 October 0.0 connected, 49.95 contracted, dated
   2022-02-15; 16 October 49.95 connected, 0.0 contracted, date blank.
5. Body sign (nit): fixed. The `MW Increase / Decrease` entry says NESO states no sign and cites the 70 + (-5.5) case;
   gotcha 4 is headed "our reading".
6. Mixed key (nit): fixed. "mostly storage with solar or wind, some with `Demand`".
