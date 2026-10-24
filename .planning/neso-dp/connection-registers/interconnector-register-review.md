# Interconnector register: checker review (2026-10-24)

Verdict: **REVISE** (1 major, 4 nits, 0 blockers).

Checked: build `--only neso_data_portal/interconnector_register` exits 0 (the only warning is the template's
"Known issues" caveat grammar, not this package); detector `[]` on `data-sources/neso_data_portal/interconnector-register.html`;
mirror `cmp` identical to the canonical note; note is CRLF throughout (415 CRLF, 0 bare LF); no staged chart spec; series,
sample and notebook artefacts present and written by the gridflow tools (`spec_origin: vault`, `generated_by`
gridflow-distil, gridflow-sample, scripts/run_notebooks.py). Screenshots taken at 1440, 1024, 768 and 390 (390 through a 390 px iframe); I looked at
1440, 768, 390 and the notebook plot (1024 not inspected): nothing clipped or overlapping; at 390 the bar labels, the "Construction" key note and the folded frame all
fit. Server on port 9853 started and stopped by its own PID (14740).

## Reproduced from silver, bronze and gridflow code

| Claim | Result |
|---|---|
| Chart: import MW by status, 16 October file, Moyle stage 1 dropped | Polars on silver (`published_at` 2026-10-16, drop `PRO-001292-1`): Scoping 26,830, Built 10,791, Awaiting Consents 4,000, Under Construction/Commissioning 1,400 (34 rows). With stage 1 kept, Built is 11,266 (12 rows). Matches the series file and the notebook. |
| Pinned to the 16 October capture | Two captures only: `published_at` 2026-10-06T10:47:52 (file name dated 05 October) and 2026-10-16T18:06:23 (file name dated 16 October); 35 rows and 35 distinct `project_number` each; filter takes the second. |
| Same 35 projects in both captures | Yes. Anti-join on all 15 vendor columns (nulls equal): exactly 5 rows differ. |
| Gate 2 appears | Gate counts: first file 1 on 6 rows, blank 29; 16 October file 1 on 9, 2 on 1 (NeuConnect `PRO-001288`), blank 25. Gate newly filled on SENECA, GB-EU MPI, The Superconnection (1) and NeuConnect (2). |
| Three effective dates moved | NeuConnect 2026-08-01 to 2027-07-07; Teeside MPI 2033-10-31 to 2035-10-30; The Superconnection 2027-09-01 to 2032-10-28. No MW, status or host change. |
| Re-download rule keyed on CKAN `last_modified` | gridflow `client.py` `iter_members` (lines 1752 to 1768): an upload member is `unchanged` when the newest non-datastore capture's `ckan_last_modified` equals the live `last_modified`; bodies are not compared. Sidecars carry the two `ckan_last_modified` values. The old note sentence ("only when the body changed") was wrong; the fix is right. |
| Past effective dates | In the 16 October file only the two Moyle rows (2022-04-01, 2022-08-01) are before the capture; correct. |
| Moyle numbers | Stage 1: 270 + 205 = 475 total. Stage 2: 475 + 25 = 500 total. Export 500 on both. Stage 2 current equals stage 1 total; stage 2 total equals the 500 MW TEC NESO's package note gives Moyle. |
| `current + increase_decrease = total`; no negative MW | True in all 35 rows of both captures, import and export. |
| Notebook year plot | Not-built import by `mw_effective_from` year sums to 32,230 MW, equal to Scoping + Awaiting Consents + Construction, so nothing is lost today; every value in `plot_alt` matches. |
| Status counts, host TO values, blank counts | Built 11 (12 with Moyle stage 1), Scoping 19, Awaiting Consents 3, Construction 1; host TO NGET 30, SPT 3, SHET 2 (so the guide's NGET, SHET, SPT is complete); `stage` blank 33 of 35; `mw_effective_from` blank 10. |
| Units and wording | Field dictionary (`.planning/research/neso-snapshots/field-info/20261008T114228Z/interconnector_register.json`): MW for the six capacity columns, `yyyy-mm-dd` date with no time; import and export per the CUSC text in the package notes (the 9.4 and 9.5 definitions, firm TEC, Moyle 500 MW). Guide lines for current, increase/decrease, effective date, gate, host TO, project number agree. |
| Raw feed | The data request URL equals the 16 October sidecar's `request_url`; `package_show?id=interconnector-register` is the connector's call; registry `refresh: daily`, `temporal: none`, `entity_key: [project_number]`, `latest: whole_capture`. |
| Countries (seat ruling) | The built page names no far-end country. The only country words are "Britain" (NeuConnect's customer name, NESO's text in the frame) and "Scotland" (the embedded register's own NESO description in a related note). Compliant. |
| Related links | Four, all resolve; each note is 12 words or fewer and true (TEC and embedded notes read from their `page:` blocks; IFA 1,988 MW and "Britned" are rows in the frame; both transfer-limit pages are hourly limits). The choice of `ifa` and `brit-ned` is reasonable. |
| Public copy | No em dashes, no "live", "now", "locally", "held", planning words or codes on the page. |

## Findings

1. **Major.** `page.record.fields.mw_import_total` (also the sibling guide line for the export total): "Import capacity
   contracted across all stages, MW; NESO calls it firm TEC". "Across all stages" is NESO's dictionary wording (`MW Import -
   Total`: "Total amount of import capacity contracted across all Stages"), but the frame sitting above it shows Moyle's stage 1
   row with 475 and stage 2 with 500, and the page's own caption says stage 1 overlaps stage 2. Read literally the line says
   stage 1's total should already be 500. The `mw_export_total` line is attributed "(NESO)"; the import line is not, so the
   page asserts as its own fact something its sample rows contradict. Fix: attribute the wording, for example "NESO describes
   it as contracted across all stages (Moyle's stage 1 row shows 475, stage 2 500); NESO calls total import firm TEC".

2. **Nit.** `page.what_it_is`, `page.chart_view.caption`: "Moyle's two stage rows overlap: never add them" and "its stage 1 row
   overlaps it" are stated flatly. NESO states no cumulative rule; the support is (a) stage 2's current equals stage 1's total,
   (b) stage 2's total equals the 500 MW NESO gives Moyle, and (c) NESO's note that capacity across stages may produce duplicate
   entries. The note body words it as an inference ("read as cumulative ... NESO does not state the rule"); the page does not,
   and gives no basis. The conclusion is sound and the rule is safe, so only the basis is missing: add one clause to the caption,
   for example "(stage 2's 500 MW matches the 500 MW TEC NESO gives Moyle)".

3. **Nit.** `page.chart_view` (import over export): the page never says why import is shown or defines export, and the export
   totals are not the same (4,135 / 11,097 / 26,904 / 1,470 against 4,000 / 10,791 / 26,830 / 1,400, Built differing by 306 MW).
   Title and caption do say import, and `what_it_is` ties import to firm TEC, so nothing is wrong. One short clause in the key
   note or caption ("export totals run higher") would settle the question; `what_it_is` could also say export is power NESO
   transports to the link's site (CUSC 9.5).

4. **Nit.** `page.record.fields.mw_effective_from` and the frame: the guide omits NESO's rule that the date is filled only for
   future connections or changes, while the frame shows Moyle's 2022 dates on Built rows and `how_used` says "When contracted
   links or changes are due ... contract dates, not history". A reader meets two past dates with no explanation. Add to the
   guide line or the frame caption that NESO leaves Moyle's 2022 dates in place (the writer already logged this as a vendor quirk).

5. **Nit.** Vault note body, section "Silver as of 2026-10-16" (lines 336 to 373): "One bronze capture and one silver file",
   "Gate = 1 on 6 rows" and the effective-date bullet that counts NeuConnect's 2026-08-01 are now true only of the first capture,
   and the section heading does not say so. The new "Second capture" subsection corrects the substance, but a reader of the
   first section meets the old numbers unmarked. Qualify the three bullets "(first capture)" or point to the new subsection.
   Related, notebook cell 5 hard-codes `reindex(range(2027, 2038))`; it loses nothing in this file (32,230 MW accounted for) but a
   later file with a 2038 date would drop that capacity silently.

## Checked and fine (no finding)

Short label "Construction": explained in the key note beside the chart and in the alt text, and NESO's full label survives in
notebook cell 4. Grain, key, "what one row is": correct (key `project_number` within a capture, `published_at` added for the
file). Date columns per NESO: `mw_effective_from` is a date with no time; `published_at` is CKAN `last_modified`, read as UTC;
`timestamp_utc` is bronze write time. Frame: 8 real rows (generated_by gridflow-sample), both Moyle stage rows present, guide
covers every non-pipeline column with key columns first. Notebook: read-only, `data.sql` on the `_latest` view with the reason
stated, outputs clean, times printed in UK time as the lead says, `plot_alt` matches the plot. Commands: same `--last 24h`
form as the approved FFR page; the connector treats the window as a screen, not a selector.

## Unverified

Whether other interconnector rows duplicate capacity (NESO also warns about technology types); the chart corrects Moyle only,
and the page says only that. No evidence of any other overlap in the 35 rows.
