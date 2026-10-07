# Writer revision 2: `neso/generation-mix`

Answers `generation-mix-review.md` (REVISE: 0 blockers, 2 majors, 9 nits). Writer: Opus 5.5, 2026-10-06.

All findings are fixed in the lead's canonical note, `30-vendors/neso/datasets/generation.md`. The `page:` block was
edited and three body passages changed; the edit was scripted on the raw bytes, so CRLF is kept. The two member
notes are unchanged. All three were re-copied to `vault/neso/` and `cmp` reports them byte-equal.

**Checks run:**
- `gridflow-build --only neso/generation` is clean.
- `detect.mjs --json` at its absolute path returns `[]`.
- Real em dashes on the page: 0. No literal backticks render.
- Screenshots retaken at 1440, 1024, 768 and a true 390 iframe (port 9871, stopped afterwards; 9670 untouched). The
  longer key notes and the new solar note wrap cleanly and nothing is clipped.
- No artefact needed regenerating: the chart spec and `record.select` are unchanged, and only page words moved.

## Findings and fixes

| # | Field | Fix (new text) |
|---|---|---|
| 1 major | `what_it_is` | Offset scoped to the placed fuels: "Gas, wind, imports and biomass track metered data 30 minutes later (checked); solar's timing is not placed." (58/60 words) |
| 1 major | `related[1].note` (fuelhh) | "Transmission-metered MW; tracks gas, wind, imports, biomass shares 30 minutes later" |
| 1 major | `chart_view.key[solar].note` (new) | "Timing not placed: fits the Data Portal's solar at zero lag, not 30 minutes later (checked)." |
| 1 major | Vault body, offset bullet | Replaced "`solar` is smooth and the test cannot place it" with the checker's numbers: zero-lag level fit (MAE 1.01 vs 1.51 at +30), the symmetric differenced test, and the wider sunrise and sunset edges. Says plainly: do not shift `solar` with the metered fuels |
| 2 major | `chart_view.key[imports].note` | "Not net of exports, but about 1.9 points below the Data Portal's per-link total on average (checked)." The over-reading "above zero while fuelhh shows GB exporting" is gone |
| 2 major | Vault body, composition bullet | `imports`: almost no response to exports (coefficient −0.065), so not net; 1.9 points below portal `imports_pct` (MAE 1.88, p95 4.4); about 0.86 of fuelhh's per-link sum at the median; 0.0 in 42 of the 213 net-export half-hours while per-link imports are 2 to 1,250 MW. Credited to the checker |
| 3 nit | `raw_feed.note` | "gridflow sends up to 14 days a call. A request for 14 to 21 September returns rows stamped 13 September 23:30 to 20 September 23:30 UTC (checked)." This removes the two meanings of `from`/`to` |
| 4 nit | `chart_view.caption` | "…Times are NESO's `from`; gas, wind, imports and biomass track fuelhh 30 minutes later (a project check)." (38/40) |
| 4 nit | `record.fields.timestamp_utc` | "NESO's `from`, UTC; gas, wind, imports, biomass track metered data 30 minutes later (checked)" (14/14) |
| 4 nit | `key[hydro].note` | "matches" changed to "tracks". The wind note already said "tracks" |
| 5 nit | `how_used[1]` | "A solar share, and a wind share including embedded wind, which fuelhh lacks." |
| 6 nit | `notebook.needs` | Backticks dropped: "generation for 14 to 20 September 2026" |
| 7 nit | `what_it_is`, `fields.generation_percentage`, `key[other].note` | "undocumented" became "No NESO source cited here defines the total" (in both places). `other` now reads "NESO's own category; tracks the Data Portal's other, which NESO says holds batteries and transmission solar (checked)", using the checker's measured fit (MAE 0.43, differenced correlation 0.78 at +30) and the approved portal page's vendor quote |
| 8 nit | `record.caption` | "One half-hour, from 12:00 UTC on 20 September 2026: all fuels but `other`." (renders `other` as code) |
| 9 nit | `related[2].note`, `how_used[2]` | No edit, as the checker allows; this is the seat's cross-page ruling. Both pages hold: they share the key, and this page's offset is stated against metered data only. The open question to the `national-carbon-intensity` page stands (author report, question 2) |
| 10 nit | Vault body, silver schema table | `timestamp_utc` reads: "Half-hour period start as NESO labels it; see Known issues for the offset against metered data." |
| 11 nit | `chart_view.x_label` | "UTC day, as NESO stamps it" |

One deliberate change: `what_it_is` lost "There are no MW figures" to fit the budget. The summary already says
"percentage shares", and the frame shows `generation_percentage` only.

## Defects

I take the checker's two pasteable additions as written: `solar` does not follow the offset, and `imports` is neither
net nor the portal's gross. They extend my items "stamps sit 30 minutes before the metered half-hour" and "share
denominator and fuel composition undocumented" in `generation-mix-author.md`. The other items there stand.

---

All 2 majors and 9 nits are fixed in the note. The build is clean and the detector returns `[]`. Mirrors are byte-equal,
and screenshots at 1440, 1024, 768 and 390 show nothing clipped.

## Nits fixed (answers `generation-mix-review-2.md`, APPROVE with 2 nits)

- **A. "No NESO source cited here defines the total."**
  - I read NESO's official API docs (`carbon-intensity.github.io/api-definitions`, 2026-10-06; documentation only, no
    API call). The generation-mix routes are described only as "Get generation mix for current half hour", "…for the
    past 24 hours" and "…between from and to datetimes". The nine fuels are listed. `perc` and its total are never
    defined.
  - The plain wording is now backed:
    - `what_it_is`: "NESO's API documentation does not define the total." (word count unchanged)
    - `record.fields.generation_percentage`: "NESO's `perc`, percent to one decimal; NESO's API docs do not define the
      total" (14/14 words)
    - The vault body's "No denominator" bullet records the docs read and what it found.
  - This also closes the "Not verified" item on the live docs from `generation-mix-author.md`.
- **B. "(checked)" on a window that was not run.**
  - `raw_feed.note` now names the held call: "A request for 13 to 22 September returned rows stamped 12 September 23:30
    to 21 September 23:30 UTC (checked)." This matches bronze sidecar `generation/2026/09/13/raw_20260926T174333Z_d2d0fdf9`.
  - The request URL and commands still show the 14 to 21 September window the chart uses.

**Checks:**
- Canonical note edited on the raw bytes; CRLF kept.
- All three mirrors were re-copied and `cmp` reports them byte-equal.
- `gridflow-build --only neso/generation` is clean.
- `detect.mjs --json` at its absolute path returns `[]`.
- Em dashes on the page: 0.
- No artefact changed. No screenshot retake: the changed fields kept their word counts.

Both re-check nits are fixed in the note. The build is clean and the detector returns `[]`.
