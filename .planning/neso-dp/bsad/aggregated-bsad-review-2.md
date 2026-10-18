# Aggregated BSAD page: review 2 (after Revision 1)

Checker: Sonnet 5.5 · high, 2026-10-18. Inspection only. The port 9923 server is stopped.

**Verdict: APPROVE** (0 blockers, 0 majors, 1 nit). The nit is a one-line wording fix I recommend before merge.

## Gates re-run

- `uv run --system-certs --extra build gridflow-build --only neso_data_portal/aggregated_bsad`: succeeds. Only message is the caveat warning (seat matter).
- `detect.mjs --json`: `[]`.
- Mirror `vault/neso_data_portal/aggregated-bsad.md` equals the canonical note (`cmp` clean). The canonical note has 434 lines, all CRLF (434 LF, 434 CR).
- Vault diff against `origin/master` is 125 added and 6 removed, the same body spans as review 1. Nothing else in the body moved.
- Page text grep: no em or en dashes, middle dots or arrows; no "back-test" or "superseded" left on the page.
- Re-screenshotted the chart section at 1440, 1024, 768 and a true 390 (390 px iframe). Nothing is clipped or overlapping; the key note fits beside the chart at 1440 and 1024 and under it at 768 and 390.

## Review 1 findings

1. **Major (the 2020-21 gap reads as zero): fixed in words.** Caption now ends "No data April 2020 to March 2021 (file fails to load); that stretch is the axis, not zero." The key note says "No data April 2020 to March 2021: that flat stretch is the axis, not zero." The alt says "No line April 2020 to March 2021, only the axis: that file fails to load." All three are true: the 2019-20 file ends 2020-03-31 and the next point is 2021-04-01 (series JSON), and the 2020-21 file fails with repeated keys. The plot itself is unchanged, so the break is still only readable through the words, as the seat ruled. In the screenshots the key note sits directly beside or under the plot, so a reader who looks at the plot first meets the warning in the legend.
2. **Nit (the "superseded, carried as zero (BSC)" paraphrase): fixed by narrowing.** `what_it_is` now says only "The six cost and volume terms are zero in every row shown". That is true of the eight rows on the page and the notebook output (`ebca`, `ebva` zero in the head; silver has no non-zero value in any of the six, which I confirmed in review 1). The six guide lines are name and unit only ("Energy buy cost adjustment, £ (NESO)"), with no source claim left to defend. The cost is that the page no longer says why the six are zero; acceptable.
3. **Nit ("back-tests"): fixed.** `how_used[0]` is now "...for imbalance price studies." with no back-test claim.
4. **Nit (notebook `needs` implied every file loads): content fixed, but the rendering is garbled; see new nit A.**
5. **Nit (what BPA is, optional): the writer's reason for not applying it holds.** My source was a model-summarised read of Elexon's glossary page, which I flagged as unconfirmed, and the writer found no readable vendor text either (the BMRA service description fetch returned a table of contents). Keeping to what NESO states is the safe choice. The key note about sign convention was removed; the `bpa` and `spa` guide lines still say NESO does not state it, which is true and scoped to NESO.

## Merged-and-rewritten field lines

The writer reports a bad `replace_all` that merged the six unquoted guide lines, then rewrote that segment byte by byte. Checked: the YAML parses (the build ran), the six lines are intact and separate in the rendered guide, the note is still 434 CRLF lines, and `git diff --numstat` shows no stray changes. Nothing new was introduced there.

## New finding

A. **Nit.** `page.notebook.needs`: the template appends "ingested" after the field, so the rendered line reads: "Needs gridflow and gridflow-models installed, with one capture of each file from 2016-17 on; 2020-21 will not load ingested." The last clause is garbled. Suggested: "one capture of each file from 2016-17 on (bar 2020-21, which does not load)", or drop the clause and let the page's own gap statement carry it ("one capture of each file from 2016-17 on, bar 2020-21"). The build does not catch this. Evidence: rendered page text, "Needs" panel.

## Not re-checked (unchanged since review 1)

Series, sample and notebook artefacts are unchanged (the build's digest checks pass). Every other fact I re-derived in review 1 still stands.
