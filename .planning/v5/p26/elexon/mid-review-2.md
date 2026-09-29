# elexon/mid: checker's re-check (review 2)

Checker: Opus 5.5 · high, 2026-09-29.

**Inputs:**
- the writer's "Revision 1" in `mid-author.md`;
- the revised vault note (the mirror is `cmp`-identical);
- the rebuilt page: `gridflow-build --only elexon/mid` green, `detect.mjs --json` `[]`;
- `chart_svg.py` after PR #50;
- my own screenshots at 1440, 1024, 768 and 390, served on port 9716.

## Verdict: REVISE

Both earlier findings are fixed. One new major: a regression from the renderer fix, the seat's code, which shows
on this page at phone width.

## Earlier findings

### 1. (major, `page.chart_view.x_label`) Fixed

- **Wide chart.** The axis runs from `x0 = 74` (14 Sep 23:00Z) to 884. Tick marks are at 74, 189.7, 305.4, 421.1,
  536.9, 652.6, 768.3 and 884: one settlement day, 115.7 px, apart, starting at 23:00 UTC.
- **Day names.** Each is centred at band start + 12 h ("15 Sep" at 131.9, "21 Sep" at 826.1). The label "settlement
  date; each starts at 23:00 UTC" is now true.
- **Code.** `_settlement_days` in `chart_svg.py` detects the axis from the label, and `_midnights(..., uk=True)`
  shifts midnight back an hour inside summer time.
- **Caption and alt.** They match the bands, so the text needs no change:
  - -3.26 (settlement date 19, period 1, 18 Sep 23:00Z) now sits inside the "19 Sep" band;
  - the 18th's only negative value, -0.5 (period 48, 22:30Z), sits inside "18 Sep";
  - -19.03 at 15:00Z and 197.83 at 20:00Z sit inside "20 Sep";
  - the 21st band holds 134.98 to 207.07.
- **`plot_alt`.** It describes the notebook's matplotlib plot, which has a UTC axis, so the renderer change does not
  affect it.

### 2. (nit, `page.what_it_is`) Fixed

- **New text.** "half-hour, one-, two- and four-hour products traded within eight hours of the submission deadline".
  This matches source 05, line 573 word for word ("Half Hour, One Hour, Two Hour and Four Hour products traded within
  eight hours of the Submission Deadline").
- **The other two claims still hold.** "Day-ahead auction trades carry no weight" (source 05, line 916) and "below
  25 MWh, both default to zero" (lines 570 and 842).
- **Budget and style.** It is 59 words against a budget of 60, and has no em dash, middle dot or arrow.

## New finding

### 3. major: the narrow chart names a day it does not show ("22" at the axis end)

- **What is wrong.** In the narrow chart (`chart--narrow`, shown at 390) the last day names read "… 20 21 22".
- **Where the "22" comes from.** It is drawn at `x = 350`, the axis end, at the 21 Sep 23:00Z boundary. That is the
  opening of settlement date 22, which has no data. The caption and title say 15 to 21 September.
- **Visual effect.** At 390 the "22" sits almost against the "21" (screenshot `mid-review2-shots/r-390-1.png`).
- **Evidence.**
  - SVG: `<text x="350" y="268" text-anchor="middle">22</text>`, with narrow ticks at 50, 92.9, … 350.
  - The cause, in `chart_svg.py` `_time_axis` (the `span_days <= 16` branch):
    1. `_midnights(lo, hi_edge, …)` includes the midnight equal to `hi_edge`, because the axis now starts and ends
       exactly on a settlement-day boundary.
    2. That midnight gets a label, and its centre is `(t + min(t + day, hi_edge)) / 2 = t`, the axis end.
    3. In the wide chart the fit check (`x + half <= fr.x1 + 8`) drops "22 Sep" (half-width 21.6).
    4. In the narrow chart the bare "22" (half-width 7.2) passes and is drawn.
- **Scope.** The rebuilt `agpt.html` in the worktree shows the same end label (`<text x="350" …>21</text>`). Any
  settlement-date chart whose series starts on a day boundary will have it at narrow width. That covers the pilot
  pages (fuelhh, system_prices, indo) once they are rebuilt.
- **Fix (the seat's; no change to the note).** In `_time_axis`, give a midnight at or after `hi_edge - 1` a tick but
  no label, as the one-value-per-day branch already does with `ticks.append((hi_edge, "", hi_edge))`.

## Nothing else broke

- **Line.** The line is one continuous path of 336 points in both the wide and the narrow chart (one `M`, 335 `L`).
  MID has no absent periods in this window, so the new gap rule (`_step` = the smallest spacing) adds no false
  break.
- **Artefacts.** The chart spec, series, sample rows and notebook are unchanged. The build's digest check passes.
- **Screenshots.**
  - 1440, 1024 and 768: hero scenery, chart, axis and x label, key, raw wells, frame and guide, notebook and related
    list are all fully visible and nothing overlaps.
  - 390: the same apart from finding 3; no page-level horizontal scroll.
- **Carried over from review 1.** The facts, the no-local-data and leakage greps, and the body edits hold. The
  revised `what_it_is` adds no banned strings.

## Re-check 3 (2026-09-29, after PR #52)

**Verdict: APPROVE.** No findings remain.

**What was checked.** I rebuilt with `gridflow-build --only elexon/mid` (green) and ran `detect.mjs --json` (`[]`).

**Finding 3 is fixed.** The narrow chart now names 15 Sep and then 16 to 21, and nothing more. The label
`<text x="350" y="268" …>22</text>` is gone. The axis-end tick at `M350 246 v6` is still drawn, with no label.

**Nothing else changed.** A line-by-line diff of the rebuilt `mid.html` against the build checked in review 2
differs in that one removed line only. It shows:
- identical wide ticks (74 … 884) and day names (15 Sep … 21 Sep);
- identical narrow ticks (50 … 350);
- an identical line path, caption, alt and frame.
