# pn (Physical notifications) re-check after Revision 1

Checker: Opus 5.5 · high, 2026-09-29. This re-check covers the writer's "Revision 1" in `pn-author.md`, the vault
note (the `page:` block and body), the regenerated sample and notebook artefacts, and the page rebuilt with
`gridflow-build --only elexon/pn`. The build passes and the detector returns `[]`. The mirror is byte-identical to
the vault note (`cmp`). Screenshots were taken with headless Chrome on port 9741 (server stopped) at 1440, 1024 and
768, and at 390 through the iframe. The notebook drawer was opened and the frame unfolded at 390 in the browser pane.

## Verdict: APPROVE

All five findings from `pn-review.md` are fixed, and the revision broke nothing I could find. Two nits remain for
the seat to take or leave.

## Earlier findings

1. **Sign (was major), fixed.**
   - The key note now reads "Negative is import, per the Grid Code (BC1)."
   - The chart alt says "stretches of import below zero".
   - **Is the dated citation sound?** The fact is. The NESO-hosted Grid Code has the same sentence: BC1, Issue 6
     Revision 22, 02 April 2024 (https://www.neso.energy/document/33851/download). Its BC1.A.1.1 "Physical
     Notifications" (p. 15) has:
     - "a series of MW figures and associated times";
     - the importing-is-negative convention, word for word as in the 2005 Issue 3;
     - the linear-interpolation sentence.
     The rule has held from the BETTA text to 2024, so the page's present-tense wording stands. As a source, though,
     the 2005 copy is weaker than the current issue (nit 1 below).
   - **Does the page claim too much?** No:
     - "Negative is import" is the Grid Code's rule for the PN data that Elexon publishes;
     - "per the Grid Code (BC1)" names the source, not the BSC;
     - silver agrees (`T_DINO-5` pumping stretches below zero, interconnector import `I_I2D-INCM1` -110).
2. **Null ids (was major), fixed.**
   - The field line now reads "Elexon BM unit id; null for units sent without one, one kept per period" (14 words).
     That matches `pn.py:98-101` and the bronze check in `pn-review.md`: one of the 46 null-id records per period
     survives.
   - The body's schema row names the dropped levels (`AG-PEPG01`).
   - No count or chart includes the null row.
3. **Known-issues exception (was nit), fixed.** The body now reads "every kept segment was the one that starts the
   period", which matches my replication (0 mismatches on 16 to 22 Sep, all rows from the 26 Sep capture).
4. **Frame folding (was nit), fixed.**
   - `select.columns: [bm_unit_id, level_from, level_to]`.
   - The sample columns print in the order `bm_unit_id, level_from, level_to, settlement_date, settlement_period,
     timestamp_utc`, then the pipeline columns.
   - The fold thresholds are 250 (`level_from`), 330 (`level_to`), 480, 640 and 840. So:
     - at 390 the folded frame shows the unit and both levels;
     - at 768 it adds `settlement_date` and `settlement_period`;
     - at 1024 and 1440 it shows every non-pipeline column.
   - **Guide order.** The guide lists the key columns first, then the rest, each group in frame order:
     - "Identifies a row": `bm_unit_id`, `settlement_date`, `settlement_period`;
     - "Other columns": `level_from`, `level_to`, `timestamp_utc`.
     This is what the rubric asks for ("key columns first"). The split comes from the template (`build.py:1185-1186`),
     and `record.fields` in the note is in frame order.
5. **Notebook head (was nit), fixed.**
   - Cell 4 now filters `level_from != 0`.
   - The output shows 16 Sep periods 35 to 39 at `300.0 / 300.0`, which match the committed series (the Dinorwig
     300 block on the evening of the 16th).
   - The cell is read-only, with outputs `card, df, text, image` and no errors.
   - The plot and `plot_alt` are unchanged.

## New findings

1. **nit: vault body, Overview, the Grid Code citation.**
   - **What is wrong:** The body cites only the 2005 Ofgem copy (Issue 3) and says "The current NESO Grid Code issue
     ... was not read".
   - **Fix:** Cite BC1 Issue 6 Revision 22 (02 April 2024), BC1.A.1.1, https://www.neso.energy/document/33851/download.
     It has the same three quoted sentences. Replace the "was not read" line. The 2005 citation can stay as history or
     go. The page is unaffected.
   - **Evidence:** `pdftotext -layout` of that PDF. The footer reads "Issue 6 Revision 22 BC1 02 April 2024". The sign
     sentence ends "the Physical Notification is negative".
2. **nit: `pn-author.md` (the report, not the page).** The top half still contradicts Revision 1:
   - the evidence row "Sign not stated", and "The page describes negative values as shape only";
   - the "Unverified" bullets "PN sign convention ... not in the sources quoted" and "apart from the re-capture case".
   These are worth striking so that the evidence record agrees with the note.

## Checked, no regressions

- **Budgets and build.** The key note is 13 words (budget 18), the field line 14 and the alt within budget. The build
  passes, including the sample, notebook and series digests. The series is unchanged (the chart spec was untouched).
- **Screenshots, light only (the site has no dark theme).**
  - The Dinorwig key note wraps cleanly in the key column at 1440 and 390, and under the chart at 1024 and 768.
  - The reordered frame, the guide, the notebook drawer (the new head, the plot) and the related list: none clipped
    or overlapping at 1440, 1024, 768 or 390.
  - At 390, with the drawer open and the frame unfolded, `scrollWidth - innerWidth = 0`. The notebook DataFrame
    scrolls inside its box, as before (by design).
- **Leakage and filler.** No new filler, em dashes, local-data references or planning labels in the changed fields.

Scratch left behind: `scratchpad/bc1-neso.txt` and `scratchpad/pn-rev/r2/` (screenshots).
