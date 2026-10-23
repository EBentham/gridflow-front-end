# Stability midterm (Y-1) utilisation report: writer's report, round 2

All five review findings are fixed in the canonical note
(`C:\gridflow-wt\vault-neso-sys\30-vendors\neso-data-portal\datasets\stability-midterm-y-1-utilisation-report.md`). The note is mirrored to
`C:\gridflow-wt\fe-neso-sys\vault\neso_data_portal\` and `cmp` is clean. The note is 302 lines, all CRLF.
`gridflow-build --only neso_data_portal/stability_midterm_y1` passes; the only warning is the unrelated global one about
dropped Known-issues lines. Detector `[]`; real em dashes 0. The chart spec, record select and notebook cells are
unchanged, so the series, sample and notebook artefacts are unchanged and their digests pass.

## Fixes

1. **Major, `page.chart_view.caption`:** now states the gap as NESO's statement: "No instructions December to March;
   NESO says a month without an update means the service was unused." (NESO's package notes: "Where there is no
   update to this dataset for a given month, it is due to the service not being utilised in that month.") To stay
   within 40 words, I dropped the old "a count, not hours" sentence (the 16-minute and 304-hour examples). The title,
   axis unit "instructions" and the notebook's hours table still make the measure clear. Caption is exactly 40 words.
2. **Nit, key notes and related:** the Elexon notes are now dated: "Elexon's register of 26 September 2026 lists
   HIRWN-1 as OCGT" and "lists CRUA units as pumped storage". The DEEPS-1 note now says "Absent from Elexon's BM
   unit register, 26 September 2026." The related note reads "Elexon's 26 September 2026 register: fuel type and
   capacity of CRUA, HIRWN".
3. **Nit, `page.summary`:** GMT is now NESO's statement: "NESO's control-room instructions to units on Stability Y-1
   contracts: start and cease, which NESO gives in GMT, hours and contracted inertia." (21 words.)
4. **Nit, caption scope:** "here" became "in this file" ("NESO's month label (in this file, the month each ends)").
5. **Nit, vault body, `month_and_year` bullet:** added NESO's dictionary wording, "The month and year of the utilisation
   period" (field-info `20261008T114228Z`), beside the end-month observation.

## Not done this round

- No screenshots: the coordinator said not to start a server. The changes are text only (caption, summary, three key
  notes, one related note), all within budget. The longest key note is the DEEPS-1 one at 18 words; in round 1 the
  same key column wrapped notes of 11 to 14 words onto two lines with room to spare at 1440, 1024, 768 and 390. The
  checker should look at the key and the caption at 390 when re-checking.

## Defects

Unchanged from round 1 (`stability-midterm-y-1-utilisation-report-author.md`, Defects).
