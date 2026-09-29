# indicated-day-ahead: review 2 (Revision 1)

Checker, 2026-09-29. Re-check of the Revision 1 fixes against `indicated-day-ahead-review.md`, and a
search for anything the revision broke.

- **What changed.** A diff of the `indgen.md` `page:` block before and after the revision shows six
  changed fields: `facts.grain`, `what_it_is`, `chart_view.alt`, `notebook.lead`, and the `imbalngc`
  and `melngc` `differs`. Nothing else changed.
- **Mirror.** All four `vault/elexon/*.md` files are `cmp`-identical to the vault worktree.
- **Build.** `gridflow-build --only elexon/indgen` is green, and `detect.mjs --json` returns `[]`.

## Verdict: APPROVE

The major from review 1 is fixed. Two nits remain, and neither needs another round.

## Review 1 findings

### 1 (major, zone row for `imbalngc`/`melngc`): fixed

Every place the page describes the `imbalngc`/`melngc` zone row now matches the code:
`imbalngc.py:117` and `melngc.py:116` keep the last row the API lists, with no sort, and drop
`boundary`.

- **`facts.grain`:** "One row per half-hour, zone, publish day; IMBALNGC, MELNGC keep one unlabelled
  zone row". This is 14 of 14 words.
- **`what_it_is`:** "Silver keeps one unlabelled `IMBALNGC` and `MELNGC` zone row per half-hour, the API's last (`N`
  in this window)."
  - "In this window" scopes the `N` observation, as the rubric allows.
  - Review 1's bronze replicate gave `{'N': 103}` for both datasets on publish days 16 and 17 Sep. These
    are the only days the commands and notebook use.
  - The Elexon definitions are intact. The INDDEM sign ("so negative") survives in the `inddem` member
    line.
- **Both `differs`:** "silver keeps the zone row listed last, unlabelled". This is true to the code, at
  14 words each.
- **`notebook.lead`:** "The cells keep the 00:17 UTC publish, with `boundary` filtered to `N` where present." This is
  exact.
  - Cell 3 filters `boundary == "N"` only under `if "boundary" in df`, which covers indgen, inddem
    and tsdf.
  - The lead no longer claims the `imbalngc`/`melngc` rows are national.
- **Other "national" and "zone" lines checked, all correct:** `summary` "nationally and by zone" (the
  vendor publishes both), `raw_feed.note`, the `boundary` field line, the frame caption, and the
  `indgen` and `inddem` `differs`.

### 2 (nit, alt pairing): fixed

`chart_view.alt` now reads "at 33,220 (00:17) and 31,228 MW (10:48)". This matches the committed
series: `same_day` max is 33,220 at 18:30, and `day_ahead` max is 31,228 at 18:30. The rendered HTML
carries the new sentence.

### 3 (nit, `related[elexon/ndf]`): unchanged, accepted

It is a term match with the glossary. It stays listed as unverified for the seat.

### 4 (nit, template): unchanged, accepted

Code wraps mid-token at 390. This is template CSS, and the writer reported it to the seat.

## New findings

### 1. nit: `page.notebook.plot_alt`

It still reads "the 00:17 UTC publish's national rows", and it covers melngc and imbalngc. The code
cannot filter those two to `N`. The claim is supported for this window: `what_it_is` now says `N` in
this window, the bronze replicate shows `N`, and cell 5's check comes out at −62 to 0. So this is
wording consistency with the new lead, not a false claim.

Optional: "the 00:17 UTC publish's rows (`N` for indgen and tsdf; the kept row for melngc, imbalngc)".
Alternatively, mirror the lead: "…with `boundary` at `N` where present". The budget is 60 words and the
field currently uses about 54, so any rewording must stay within about six extra words.

### 2. nit: `page.what_it_is`

"One unlabelled … zone row per half-hour" leaves out "per publish day". Silver holds a half-hour in up
to three publish-day files. `facts.grain` directly above states the publish day, and `what_it_is` is at
59 of 60 words, so no change is needed.

## Nothing broken

- **Screenshots.**
  - Headless Chrome, each call under `timeout 60` with `--timeout=15000 --virtual-time-budget=5000`.
  - Served from the worktree's `site/hifi` on 127.0.0.1:9752 (the server was stopped afterwards).
  - Taken at 1440, 1024, 768 and 390, the last in a 390 px iframe, with the frame unfolded and the
    notebook open.
- **What I looked at.** The three-line grain fact, the reworded `what_it_is`, both new member lines,
  the chart and its key, the frame and the notebook lead. All are whole, with nothing clipped or
  overlapping.
- **Dark mode.** There is still no dark theme in the CSS or JS, so there is no separate dark shot.
