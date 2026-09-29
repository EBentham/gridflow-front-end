# entsoe/actual_load: checker re-review (Revision 1)

Checker: Opus 5.5 · high, 2026-09-29. This is a re-check of Revision 1 against `actual_load-review.md`. Inputs:
- the canonical note, diffed against `origin/master`;
- the mirror;
- the writer's "Revision 1" section;
- a fresh `gridflow-build --only entsoe/actual_load`;
- the detector;
- my own screenshots.

## Verdict: APPROVE

The major and all four nits are fixed. The revision broke nothing. No new findings above nit.

## The first review's findings, re-checked

1. **Major, GB code 999 stated as an ENTSO-E rule: fixed.**
   - `what_it_is` now reads "GB and IE-SEM got ENTSO-E's 'no matching data' answer (code 999) on the days charted." Both zones are scoped. Bronze has 999 for both zones on every day from 14 to 20 Sep, which I confirmed in the first review.
   - `related[elexon/indo].note` now reads "GB demand outturn; gridflow's GB calls to ENTSO-E returned code 999". That is 11 words, past tense, and names gridflow's calls, so it states what gridflow received.
2. **Nit 2, the alt text: fixed.** It now reads "DE-LU runs highest on almost every interval". That matches silver: FR is above DE-LU in 2 of 672 intervals.
3. **Nit 3, `what_it_is`: fixed.** The last sentence now reads "ENTSO-E defines what total load includes; that definition is not quoted here." The "network losses" hint is gone, and the page still claims nothing about what total load includes.
4. **Nit 4, the body's `timestamp_utc` row: fixed.** The A03 claim now cites the bronze check ("all 104 data responses in bronze (checked 2026-09-29) are `curveType` A03"). `parsers.py:533-596` is now cited only for the forward-fill. My scan in the first review agrees: 104 of 104 are A03.
5. **Nit 5, the NL key note: fixed.** It now reads "Lows fall between late morning and early afternoon UTC; cause undocumented." That matches the daily minima from 09:45 to 14:00 UTC, and it guesses no cause.

## Batch rules (seat notes)

- **Timestamp wording.** The guide line is unchanged and correct: "period start plus (position minus 1) times resolution" (`parsers.py:530`).
- **Cadence.** `facts.cadence` now reads "15 minutes (`PT15M`) in every response charted". It states what the responses contain, not a rule. It is true: all 28 GL documents for 14 to 20 Sep are `PT15M`, and silver for the window has `PT15M` only.

## Anything broken? No

- **Scope of the edits.** The diff against the first review touches only `facts.cadence`, `what_it_is`, `chart_view.alt`, `chart_view.key[nl].note`, `related[3].note` and one body table cell.
  - The chart spec, sample select and notebook cells are unchanged.
  - The build's artefact digest checks pass with the committed series, samples and notebook.
- **Build and detector.**
  - `gridflow-build --only entsoe/actual_load` writes the page. Its single error is on a page it did not render.
  - `detect.mjs` reports only the accepted `em-dash-overuse` advisory (43, EIC padding and CLI flags).
  - The rendered page has 0 em dashes, middle dots or arrows.
- **Mirror.** The mirror is byte-identical to the canonical note: both are CRLF, 14,221 bytes and 304 lines. Git normalises it to LF on add under `*.md eol=lf`.
- **Screenshots.** I took headless Chrome shots at 1440, 1024 and 768, a 390 px iframe shot, and a CDP clip of the related list at 390.
  - The longer cadence fact wraps cleanly in the hero at 1440 and 390, and so do `what_it_is`, the NL key note and the longer related note.
  - Nothing is clipped or overlapping.
  - `scrollWidth` equals `innerWidth` at all four widths.
  - The port 9810 server was stopped.

## Optional, not a finding

`chart_view.alt` and `notebook.plot_alt` still say "NL's lows fall near midday", while the key note now says "between late morning and early afternoon UTC". Both are fair readings of the chart; aligning them is the writer's choice.
