# Demand Flexibility Service page: checker's third review

Checker, 2026-10-18, after Revision 2. Page `neso_data_portal/demand-flexibility`.

**Verdict: APPROVE** (one nit, optional).

## Checks

- Rebuilt with `--only neso_data_portal/demand_flexibility_utilisation_summary`: succeeds (old caveat-grammar warning only); detector `[]`; mirror `cmp` clean; no em dashes, arrows or middle dots; no "(checked)" anywhere.
- Rendered sentence now reads: "Needs gridflow and gridflow-models installed, with the summary and report tables for 11 September 2026 ingested." Grammatical, plain, no planning words. The earlier garble is gone.
- Nothing else changed: the Revision 1 text is intact in the rendered page (`what_it_is` with the loss, the scoped member line, the scoped guide lines, the zero-day caption, the raw-feed note, the history line, the requirement line). `needs` is the only changed line in the note.

## Finding

1. **nit** `page.notebook.needs`. The sentence is true as a requirement but cannot be met by a fresh install today. The report side can: the current report file loads and holds 11 September 2026 (280 rows, both captures). The summary side cannot: NESO re-publishes the current summary file in place, and its newest version (which contains 11 September) fails to load (88 rows share the key, failure record `ce9d3de8...json`), so a reader who ingests now gets no summary table. `what_it_is` already says the newest summary file cannot be held and the page stops at the 6 October file, and the seat ruled to ship with that stated, so I am not raising it above a nit. If the seat wants the line to be strictly reachable, add a half-clause, for example "(the summary loads once silver's key includes `event_id`)", but that is a seat choice, not a requirement of the rubric.
