# gie/lng (ALSI LNG terminals): checker re-review 2

Checker: Opus 5.5 · high, 2026-09-29. This is a focused re-check of `lng-author-2.md` against `lng-review.md`. Port 9857
was used briefly and is now stopped. Port 9670 was not touched.

## Verdict: REVISE

1 major, 1 nit. Both are one-word fixes. Everything else asked for in round 1 is in place and correct.

## Findings

### 1. major: `page.chart_view.key[fr].note` and `page.chart_view.key[nl].note`, "which gridflow does not keep"

**What is wrong.** gridflow does keep `status`: the bronze layer stores the full ALSI response, including `status` on
every record. Only silver drops it. The note puts the loss at the wrong layer, and it contradicts the page's own
`raw_feed.note` ("fields silver drops").

**Evidence.**
- Bronze `gie_alsi/lng/2026/09/13/raw_20260926T174756Z_2d7fcb5d.json` (NL) holds `status` values `C` and `E`.
- Bronze `..._174812Z_5ce35681.json` (FR) holds `C` and `E`.
- `status` is absent from silver's `output_cols` (`silver/gie/alsi.py:167-181`), and `"status" in df.columns` is
  `False` on silver.

**Severity.** Rubric §1 classes a wrong fact as a blocker. I grade this major because the same page states the correct
scope in `raw_feed.note`, and the fix is a single word.

**Fix.** Replace "gridflow" with "silver" in both notes: "…with vendor status code `E`, which silver does not keep."

### 2. nit: note body, `## Overview`, "which silver does not keep yet" (not rendered)

**What is wrong.** "yet" promises future work. The page carries none, but the vault note should not either. This was
the wording I suggested in round 1, so the slip is mine.

**Fix.** Drop "yet": "…the response also carries inventory, which silver does not keep." The inventory defect is
already logged for the backlog.

## Checked and correct

- **Major from round 1 (reproduced).**
  - Bronze has NL 2026-09-17 `status: "E"`, `sendOut` 734.6 (`updatedAt` 2026-09-18 06:50:03), and FR 2026-09-18
    `status: "E"`, `sendOut` 1052.8 (`updatedAt` 2026-09-19 08:10:04). These are the only non-`C` records besides GB's
    `N`.
  - Silver matches: NL 17 Sep is 734.6 and FR 18 Sep is 1052.8.
  - The committed series has `nl` 734.6 at 2026-09-17 and `fr` 1052.8 at 2026-09-18, and `spec_sha256` is unchanged
    (`5d7595…03e6`).
  - Each note names its point, with no count and without the words "estimated" or "provisional". A grep of the rendered
    page for `estimat`, `provisional` and `final` found nothing.
- **Nit 2 from round 1 (Overview).** The inventory overclaim has been removed. The one remaining word is finding 2 above.
- **Nit 3 from round 1 (`what_it_is`).**
  - "gridflow asks for country figures, not terminals" is now scoped to the request (`endpoints.py:17`; `client.py`
    `_fetch_country` sends only `country`, `from`, `till`, `page` and `size`).
  - The shortened "GB's `-` placeholders become nulls" is accurate. Bronze GB records send `"-"` with `status: "N"`,
    the transformer casts with `strict=False` (`alsi.py:134-136`), and every GB numeric in silver is null.
  - "one row per country and gas day" is still true: 8 × 15 rows, unique on (`gas_day`, `country_code`).
- **No regression.**
  - `gridflow-build --only gie/lng` exited 0 and wrote `data-sources/gie/lng.html`. Its warnings are for other GIE
    datasets only.
  - `node C:/Users/Bobbo/OneDrive/Desktop/Python/gridflow-front-end/.claude/skills/impeccable/scripts/detect.mjs --json`
    returned `[]`.
  - The mirror is byte-identical to the canonical note (`cmp`).
- **No planning language in rendered text.**
  - I grepped the visible text plus the `alt`, `aria-label` and `title` attributes for: yet, will, soon, planned,
    future, upcoming, coming, until, pending, TODO, live, now, em dash, middle dot and `→`.
  - The only hit is the template's hero alt text, "Drawing of gas coming ashore". That describes scenery and is not
    planning language.
- **Rendering.**
  - Headless Chrome (`timeout 60`, `--timeout=15000 --virtual-time-budget=5000`) at 1440 and 768: both key notes wrap
    under France and Netherlands, fully visible, with no overlap with the chart or the next entry.
  - Round 1 already covered 390, and the only rendered change is two short wrapped notes and one shorter
    `what_it_is`.

Summary: REVISE, because the two new key notes say "gridflow does not keep" when bronze keeps `status` (change it to
"silver"); drop "yet" from the note body; the `E` points reproduce exactly, the other round-1 fixes hold, the build is
green and the detector returns `[]`.
