claude-opus-5-5

Boards (in p24\D\): D-fuelhh.dc.html 3483 · D-system-prices.dc.html 3156 · D-physical-flows.dc.html 3269 · D-bmunits-reference.dc.html 3170 (root height = $preview = measured content bottom). Generator: gen_d.py (run with the gridflow_models venv, pandas 3.0.2).

Idea: the page is an annotated notebook. Each rail note sits level with the cell it explains, so a reader who never runs code gets the whole documentation from the rail.

CONTENT MODEL (order, budget):
1. Hero: breadcrumb; h1 name (≤5 words); code + gridflow key (1 line); one-liner (≤20 words, 2 lines)
2. [1] setup + exact workbench call + one check the pack proves | What it is (≤60 words)
3. [2] pandas selection returning exactly the pack sample | Facts: grain, cadence, stored, published, units (≤15 words each)
4. (fuelhh only) [3] code-to-band mapping | bands note (≤60)
5. chart cell + plot | caption naming dataset, unit, window, aggregation (≤50) + Caveats ×3 (≤35 each)
6. How it's used ×3 (h3 ≤4 words + ≤20 words)
7. The silver table: help-card schema (≤12 words per column)
8. Other ways to get it: vendor endpoint + CLI wells, 1 note (≤25)
9. Related, ≤4 (code + ≤12 words)
10. Deep footer (name, role, links from R3-final)

Decisions:
- Uncovered codes: bands named by the codes they sum. OTHER+NPSHYD+COAL+OIL share khaki (the label removes the OTHER clash); PS gets khaki with an ink hatch (signed, storage is khaki in the scenery); INT* is net olive; INTELE folds into INT*.
- Signed stack: one pandas area call over the positive parts plus the INT*/PS negative parts. INT* and PS mirror around the zero line, a zero rule is drawn, and the negatives are labelled on the plot. Verified: no clipping loss, no warning, correct y-limits.
- BMUNITS: [1] prints True 2515 / False 499; the bars show the 499 typed units with exact labels; the title is computed in code ("499 of 3,014").
- ENTSOG: a second, wider query plus asfreq("D") makes a real NaN break for 6 Aug to 12 Sep; the zeros are drawn as reported.
- Deviations from the brief: the sample is Out[2], not Out[1], and the chart is [3]/[4], because the call's true output is not the sample. The schema card sits outside the notebook, because no real call prints those dtypes. 192 rows is derived (4 × 48). Every cell was run on synthetic frames under pandas 3 / mpl 3.10; timestamp_utc is never printed because it displays in Europe/London.
