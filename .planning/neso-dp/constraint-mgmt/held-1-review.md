# Held pages, Constraint management part 1: checker review (2026-10-23)

Verdicts: all four pages APPROVE. 0 blockers, 0 majors, 8 nits on the pages, 1 nit on a note body.

| Page | Verdict |
|---|---|
| `24-months-ahead-constraint-cost-forecast` | APPROVE |
| `24-months-ahead-constraint-limits` | APPROVE |
| `constraint-management-intertrip-service-information-cmis` | APPROVE |
| `day-ahead-constraint-flows-and-limits` | APPROVE |

## What I ran and read

Batch file, standing instructions, the writer's report, the four canonical note diffs against `origin/master` in
`C:\gridflow-wt\vault-neso-cm`, the mirrors in `C:\gridflow-wt\fe-neso-cm\vault\neso_data_portal\`, the built pages, the
registry JSON of each package (eligibility question per family), the 2026-10-06 catalogue snapshot (package notes, extras,
resource descriptions), the 2026-10-08 field dictionaries, the ledger rows (50, 51, 52, 137), the bronze sidecars and
bodies of all six families (read only, Polars), silver row counts, and `refresh-20261016/DRIFT.md`.

Gates, my own runs: `gridflow-build --only neso_data_portal/<lead>` ok on all four, no budget errors, only the known
"Known issues" caveat warnings; `cmp` canonical note against mirror clean on all four; detector `[]` on all four. Rendered
text, checked on the UTF-8 bytes of the built HTML: 0 replacement characters, em or en dashes, arrows or middle dots on all
four; the pound sign and the curly apostrophe render as proper characters (the question marks that showed in my own console
output came from the console code page, not the page); none of live, now, yet, soon, pending, coming, planned, shipped,
real-time, locally, ruling, ledger, TODO, E-SEM or any local path in the page text; viewport meta and `<main>` present. The
word "capture" appears once on the cost and limits pages (the shared transform comment "the capture's date to silver", the
same wording as ten approved pages). No page states a capture date, size or row count.

Overflow at 390 px, measured: all four pages in a true 390 px iframe in the browser pane. `scrollWidth` and `clientWidth`
are 390 on every page, 0 non-SVG elements extend past the right edge, 0 elements with inner horizontal scroll or clipped
overflow. The only things past the edge are the 12 hero scenery SVG paths, identical on all four (template, not page
content). Long request URLs wrap (looked at the CMIS raw feed at 390). Viewport emulation reset to desktop.

Server: port 9913, started from Bash with its PID recorded (shell PID 16354, Windows PID 6660), stopped by that PID, port
confirmed down. Port 9670 not touched.

## The five asks

**1. "Rows not shown" lines against the ledger.** All four are accurate, plain and free of codes.
- Cost forecast (ledger: currency unit): true. NESO's package notes rename `Constraint Cost (£m)` to `Constraint Cost` from 9
  September 2026, and both captures have the header `Month,Constraint Cost`. See finding 1 on the wording "the metadata's £m".
- Limits (ledger: week calendar, issue clock): maps one to one, "does not map its week numbers to dates" (calendar) and "nor
  say when each week was forecast" (issue clock). The dictionary says only "(1-52)" and the header has no date column.
- CMIS (ledger: +00:00 against GB local clock, fee units): true. NESO's notes say "local time in GB"; all six captures have
  every arming and disarming time ending `+00:00` (checked on every file). The 2026-27 dictionary describes the fee as
  "(in £/MWH)" and gives the unit `£/SP`. See finding 5 for "newer".
- Day-ahead (ledger: only the unit label): true and checkable. In both captures 1,436 excess rows, 1,392 whole-row
  duplicates, 44 key groups with differing limit or flow. It names one of the three open questions in the registry (row
  grain; the other two are the clock and the unit and sentinel values). See finding 8.

**2. Ingest-only commands on the intertrip and day-ahead pages.** Honest, and clean of local-data references. Day-ahead: the
transform fails on duplicate keys on both captures, and the page says "bronze only" and "there is no silver table", which is
exactly right. Intertrip: the transform raises a header error on the 16 October capture only (the five older captures are in
silver, 1,047 rows, unchanged), so a transform line that "works" would be false for the newest file and one that fails would
mislead; omitting it states nothing untrue, and the raw-feed note says "Headers differ by year, and changed again in October
2026". Neither page carries a path, a table name under `C:\gridflow-data`, a capture date, a size or a row count. The one gap
is that the intertrip reader cannot tell why there is no transform line; see finding 6. The cost and limits pages keep a
transform line, which is correct (both transforms run: silver has 48 and 210 rows from two captures each).

**3. The 16 October URLs against bronze sidecars, stale dates, note bodies.** Every request URL on every page equals the
`request_url` of the newest sidecar of that resource: cost `..._oct26.csv`; limits CSV `..._limit_oct26.csv`; intertrip
2022-2023 and 2026-2027 files; day-ahead CSV (name unchanged) and both `-oct2026` diagrams. The two limits diagrams have only
8 October captures (not fetched on 16 October because unchanged), so their URLs rest on the 8 October sidecars, which is as
fresh as bronze gets. Dataset and resource ids match the catalogue snapshot. No page states a capture date. The updated note
bodies check out on the facts: cost forecast, 24 rows in both, 23 shared months, all 23 differ (the page states none of
this); limits, 105 rows each, window 2026 week 40 to 2028 week 40 then 2026 week 44 to 2028 week 44, 101 shared weeks, 30
rows and 102 cells changed, weeks run 1 to 52; intertrip, 83 rows and the same 83 keys, third header read exactly as
quoted (`B6 or EC5 ` with a trailing space); day-ahead, 740,443 rows and 28,324,304 bytes, 6,794 new keys, none dropped, every
distinct row of the first capture present in the second, last target 2026-10-17. The remaining "2026-10-08" mentions in the
bodies are all correctly the first capture or the activation record. One wording slip in the intertrip body: finding 7.

**4. "A boundary is a cut across the transmission network."** Not NESO's wording. Nothing in the package notes, resource
descriptions or dictionaries defines a boundary beyond "the main boundaries on the transmission system" and "a constraint
boundary", and nothing in the repo or vault quotes a definition. NESO's own ETYS material does describe a boundary as
dividing the transmission system into two parts, crossing the circuits that carry power between areas where flow limits can
bite, so the sentence is consistent with NESO's meaning (web search of neso.energy ETYS pages: "Our ETYS analysis",
https://www.neso.energy/research-and-publications/electricity-ten-year-statement-etys/our-etys-analysis; a search snippet,
not a page I read in full). The page does not attribute the sentence to NESO, so there is no misattribution. Keep it, with
the optional refinement in finding 3.

**5. Overflow at 390.** Measured, none; see above.

## Findings

### Page 1, `24-months-ahead-constraint-cost-forecast`: APPROVE

1. **nit** `page.held`: "the metadata's £m is unconfirmed" is vendor-internal ("which metadata?"), and it hides that NESO's
   own dictionary says £m outright (title `Constraint Cost (£m)`, unit `£m`, description "in £m"; the bytes are a valid
   pound sign). What is true and useful: the unit left the column name, and the only statement of it is the dictionary's.
   Suggest "NESO dropped £m from the column name, and the dictionary's £m is unconfirmed." (13 words, under the 16 budget).
2. **nit** `page.what_it_is`: "In NESO's words it does not include the cost of managing inertia or the largest loss of
   infeed." NESO's text is "These costs do not include the cost of managing inertia or the largest loss of infeed"; the
   sentence is a paraphrase, so "In NESO's words" over-claims. Suggest "NESO says it does not include ..." (same length).

### Page 2, `24-months-ahead-constraint-limits`: APPROVE

3. **nit** `page.what_it_is`: first sentence is the note's own gloss (ask 4). Optional, closer to NESO's ETYS wording and
   shorter: "A boundary splits the transmission network in two." No change needed for approval.

### Page 3, `constraint-management-intertrip-service-information-cmis`: APPROVE

4. **nit** `page.what_it_is` / title: the page never says that CMIS is the package's acronym (the title drops "(CMIS)" and the
   body never uses it), so a reader searching for it will not match the page text. If words allow, "intertrip service (CMIS)".
   The `what_it_is` field is already at 60 of 60 words, so something must go (for example "on the network"). (Seat's call;
   the manifest name keeps it.)
5. **nit** `page.held` and `page.what_it_is`: "the newer fee" is unexplained on the page. The five files have two header
   epochs (the 2022-23 and 2023-24 headers say `£ / SP`, 2024-25 onward say `£ / MWH`, and the 14 October upload carries no
   unit at all). Suggest for the held line "Times carry +00:00 though NESO says local time, and the fee's unit is given two ways."
   (16 words), and in `what_it_is` "For the arming fee since 2024-25, NESO's dictionary ..." (same word count as now).
6. **nit** `page.raw_feed.note`: the page shows `ingest` only and does not say why there is no transform line, though the
   silver section implies one exists. One clause fixes it: "The newest file's October 2026 header is not read into silver."
   The note is at 29 of 30 words, so replace "Headers differ by year, and changed again in October 2026" (10 words) with
   "Headers differ by year; the newest file's October 2026 header is not read into silver." (14 words; trim "(first and
   newest shown)" to "(first and newest)" to fit). Not a defect: the omission is honest, the clause makes it self-explaining.

### Page 4, `day-ahead-constraint-flows-and-limits`: APPROVE

7. (see note body below; no page finding)
8. **nit** `page.held`: the line gives one of the registry's three open questions (row grain). Also open: the meaning of the
   timestamp (period start or end, the repeated autumn hour), and the unit of the flow and the meaning of blanks and 99999.
   This matters for the page's own sentence "gives the boundary's limit in MW": 8,166 of the 740,443 limit values on the 16
   October capture are 99999 and 3,365 flows are blank, and the dictionary gives the flow no unit. No values are needed
   on the page; a half sentence is. Suggest "Boundary and half-hour pairs repeat, and NESO does not explain 99999 limits or
   the flow's unit." (16 words) and keep "no silver table" in the raw-feed note, which already says "Everything stays in
   bronze".
9. **nit** `page.raw_feed.note`: the cost and limits notes say the file name carries the upload month; the day-ahead note
   is silent although both diagram names changed to `...-oct2026.pdf` between the captures (only the CSV name is stable). Add
   "The diagrams are re-issued under new names." in place of "Everything stays in bronze." (the ingest comment already
   says "bronze only").

### Note body (not a page finding)

7. **nit** `constraint-management-intertrip-service-information-cmis.md` ("A third header", the Cadence block) and the
   writer's pasteable defect: "NESO restated three published costs" overstates. The three rows (WHILW-1, WHILW-2, BLLA-1,
   all armed 2026-04-03) carried a cost of 0 on 8 October and carry 8,693.04, 4,124.34 and 3,376.24 on 16 October: zeros
   filled in, not published figures revised. The 8 October file held four zero-cost rows, the 16 October file holds one.
   Suggest "three zero costs were filled in". The conclusion that the current-year file is edited in place still stands.

## Defects (for the seat to paste)

- **gridflow, `da_constraint_flows_limits`:** the duplicate keys are two different things, and each is fixable on its own.
  The 44 key groups whose values differ all fall on the two autumn clock-change days (2024-10-27 and 2025-10-26, 22 each,
  at 01:00 and 01:30): the repeated local hour, a fold. The 1,392 whole-row duplicates are two full repeated days at some
  boundaries (2025-08-12 at 11 boundaries, 2026-08-19 at 18). Identical on the 8 and 16 October captures. The note body
  says "others fall on ordinary dates, so a fold rule alone does not explain them", which is true of the whole-row
  duplicates, but the value-differing collisions are all fold rows. Relevant to the remediation unit.
- **gridflow, `da_constraint_flows_limits`:** NESO says "the ten most important boundaries" are in the file; the 16 October
  capture has 31 distinct constraint groups, and the diagrams' descriptions list more than ten. Ten of them match the 24
  month limits file by code. The page says "main" and gives no count, so it is not affected.
- **gridflow, `cmis_intertrip`:** the three zero costs filled in (finding 7) plus the header with no units; the 16 October
  capture still fails the header check, as the writer reported.
- **Vault, cost forecast note, Holds block:** the registry's "undecodable symbol before 'm'" reading is not reproducible; the
  dictionary bytes are a valid pound sign (confirmed). The hold question to ask NESO is the missing unit in the file, not a
  garbled character.
- **Seat items, not findings:** the OTF related link on the limits and day-ahead pages, and `constraint-breakdown` and
  `elexon/bmunits_reference` on the cost and intertrip pages, resolve only because those pages are in the page set; the
  OTF page is the next batch's, so it is a name-only page until that batch ships. Registry status reads `eligible` on all
  four packages while every family is held (known pattern). Manifest lead and member lists are correct for all four.
