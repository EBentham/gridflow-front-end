# agsi-reference (GIE AGSI+ operator and facility register): checker review

Family `agsi-reference`, lead `about_listing`, member `about_summary`. Checker port 9856.

## Verdict: APPROVE

No blocker and no major. Three nits, below. Every fact on the page reproduces against gridflow code, local silver and the bronze payloads.

## What I checked, and how

- **Notes.** Both notes diffed against vault `origin/master`. The mirrors are byte-identical to the canonical notes (`cmp`). `about_summary.md` has no `page:` block. The body edits cite `file:line`, fix narrow spans and match the code (`agsi.py:309,381,387-391,462-489,579-634`; `endpoints.py:265,281,291,489-494`). The curl examples are unchanged.
- **Build and detector.**
  - `gridflow-build --only gie/about_listing` is green. The only warnings are the existing "no Pydantic class" content warnings.
  - `detect.mjs --json` returns `[]`.
  - There is no staged chart spec (`site/hifi/data/chart-specs/gie/` does not exist).
  - The series has `spec_origin: vault`, and the build's digest check passes.
- **Row identity.** Reproduced with Polars (`scratchpad\agref-check\silver1.py`).
  - Each member has 9 partitions of 185 rows (1,665). With the lineage columns dropped, all 9 are equal.
  - `event_time` runs from 2026-09-19 to 2026-09-27 at 00:00 UTC, one value per partition.
  - `ingested_at` is 2026-09-27 00:31:42 for the listing and 00:31:54 for the summary.
  - Bronze is one capture per member, both filed under `2026/09/20`. The listing's `.meta.json` has `fetched_at` 2026-09-27T00:31:37Z and `data_date` 2026-09-20.
  - Per partition, `entity_code` has 185 unique values: 64 `company` and 121 `facility` in both members.
  - The set difference of `entity_code` between the members is empty both ways, and `entity_level` agrees on every EIC.
- **Duplicate listings** (`bronze1.py`, parsing the raw JSON).
  - Listing: 71 operator entries (64 EICs) and 127 facility entries (121 EICs). The summary walk gives the same counts.
  - That makes 13 repeated EICs: 7 operators and 6 facilities.
    - SEFE and Uniper appear under AT and DE, and EWE under DE and NL.
    - 4 UK operators and 5 UK facilities appear under both `GB` and `GB*`.
    - `21W000000000095N` is listed as the Edison Stoccaggio group (ending 2025-03-01) and as VGS HUB2.
  - The two payloads put the UK entries in opposite orders:
    - the listing sends `GB*` (index 63 to 66) before `GB` (67 to 70);
    - the summary sends `Europe/United Kingdom` (`GB`) before `Non-EU/United Kingdom` (`GB*`).
  - With `unique(subset=["entity_code"], keep="last")` (`agsi.py:387-391`), the listing therefore keeps `GB` and the summary keeps `GB*`. The join shows exactly those 9 EICs differing in `country_code`.
  - **Wording.** The UK key note, the `country_code` guide line and the summary's `differs` line are all accurate. On plainness, see nit 2.
- **Chart.**
  - Facility rows by `country_code` in the 27 Sep partition: DE 63, FR 8, NL 7, RO 7, AT 5, GB 5, CZ 4, PL 4.
  - The 13 other codes are IT 3, HU 2, SK 2, DK 2, and 1 each for HR, SE, PT, UA, LV, IE, ES, BG and BE, which sums to 18. That matches the committed series and the key note's 13 codes.
  - The series provenance is `rows_used 121`, and `unmapped_groups` lists the same 13 codes.
  - Khaki is not used. The countries are painted `petrol` (as in the approved ENTSO-E pages), and "others" is `hatch-dots`.
  - The alt text's numbers match the series.
  - The title and caption date the capture ("fetched 27 September 2026", which is `fetched_at`) and make no time-series claim.
- **Other facts.**
  - The request URL matches `endpoints.py:139-153` and the meta `request_url`, and the client sends no page parameter when `paginated=False` (`client.py:328-333`).
  - Ingest `--end` defaults to now, and transform `--end` is inclusive (`cli.py:186-300`, `runner.py:479-500`).
  - `query()` date column is `ingested_at` (`schema_manifest.py:226`).
  - The connector's planning fetches `about_listing` live (`client.py:183-185,311-316`).
  - `AGSI_COUNTRIES` has 9 codes (`endpoints.py:14`), and all 9 appear in the listing.
  - `entity_type` counts: SSO 64, ASF 50, DSR 48, ASR 13, null 5, GRP 4, SRC 1. They match the notebook output.
- **Wording.** No text calls a copied partition a dated observation. The raw-feed note ("A transform day with no bronze copies the newest capture") and the notebook lead ("each transform day holds a whole copy") describe the copies correctly.
- **Local-data and leakage grep** on the rendered text (`locally|held|our|since 20|rows|% of|live|now|—|·|→|planned`): no hits except the generic "rows" in the template and help card.
- **Screenshots.**
  - **Method.** Static server on 9856 (stopped) and CDP headless Chrome with true device-width viewports, each run under `timeout 60`.
    - `--virtual-time-budget` froze the CDP session and the run timed out, so the CDP runs omit that flag and `--timeout`. Both are screenshot-mode flags.
  - **Widths and themes.** 1440, 1024, 768 and 390, light and emulated dark. No page overflow at any width.
    - The site has no dark theme: the body background stays `rgb(246, 244, 236)` with `prefers-color-scheme: dark` matching.
    - My first dark capture was cut short by load timing. A re-run with a settle wait gave the same heights as light.
  - **What I looked at.**
    - The hero at 1440, 1024, 768 and 390: turbines, gas-station, terminal, landfall and platform labels are whole.
    - The chart and key notes at 1440, 1024, 768 and 390. The key reflows to 3, 2 and 1 columns with nothing clipped.
    - The raw feed at 1440 and 768. The URLs and commands wrap inside their boxes.
    - The frame folded, then **unfolded** (`#fx` checked). At 1440 all 14 columns show and scroll inside the box; `company_name` and `entity_url` are readable.
    - The column guide.
    - The **opened notebook** at 1440 and 390, whose outputs match silver: 185 rows, facility 121 and company 64, and the `entity_type` counts above.
  - **Scroll regions.** At 390 the frame (`.fw`, 0 to 390 px) and the `.head()` output (`.df-wrap`) are `overflow-x: auto` scroll regions, as the template designs them. Nothing is clipped.
  - Files: `scratchpad\agref-check\shots\`.

## Findings

1. **nit — `page.chart_view.caption`.** "Entries GIE names historical or decommissioned count too" understates which closed entries the bars include.
   - **Evidence** (`bronze2.py`, applying keep-last to the listing payload): 35 of the 121 charted facility EICs carry an `operational_end_date` in the payload, and 20 have names saying historical or decommissioned. The rest include entries GIE has dated as closed without saying so in the name:
     - UGS Allmenhausen (DE), 2023-05-31;
     - UGS Nüttermoor L GUD (DE), 2022-04-22;
     - UGS Cetatea de Baltă (RO), 2018-12-31;
     - the five pre-Brexit UK entries (nit 2).
   - Others carry placeholder dates such as 3000-12-31 and 4022-03-07.
   - **Suggestion:** "Closed and historical entries count too, whether or not their names say so." Alternatively, keep the sentence as it is; it is true, just narrower than the bars.
2. **nit — `page.chart_view.key[uk].note`.** "GIE lists each of these under `GB` and again under post-Brexit `GB*`; silver kept `GB`" is accurate, but it doesn't say which listing survives.
   - **Evidence.** The five `GB` facility entries silver keeps are the pre-Brexit ones: in the listing payload each has `operational_end_date` 2020-12-31, and their names lack "(Post-Brexit)". The current `GB*` entries are the dropped ones.
   - The `country_code` guide line does say the post-Brexit entries are dropped, so a careful reader can work it out.
   - **Suggestion:** "Each is listed under `GB` to 2020 and again under post-Brexit `GB*`; silver kept the `GB` entry." The EIC count per country is unaffected either way: it is 5 UK EICs.
3. **nit — `page.facts.grain`, `page.what_it_is`, `page.record.fields.entity_code`.** "One row per EIC" and "silver keeps one row per EIC" hold within one transform day, not across the table.
   - **Evidence.** The dedup runs inside each day's transform (`agsi.py:387-391`), and `event_time` is that day (`base.py:2228-2232`). The table therefore holds one row per EIC per transform day (Polars: 9 partitions, each with 185 unique `entity_code`).
   - The page already warns in the raw-feed note and the notebook lead, so this is consistency, not a false fact.
   - **Suggestion:** scope the grain line to "per transform day". Keep `record.key: [entity_code]`, since the frame shows one day.

## Observations for the seat (not findings)

- **The chart spec cannot pin a capture.**
  - The spec dedups on `entity_code` across every partition, with no `event_time` filter. `chart_spec.py:283` rejects `window` on a bar chart.
  - Today there is only one capture, so the committed series is exactly the 27 Sep register.
  - If a later capture is ingested and the series re-distilled, the bars would count every EIC ever seen: an EIC that GIE dropped would survive. Meanwhile the title would still say "fetched 27 September 2026".
  - This is a limit of the template or distiller, not a writing error.
- **Writer's report.** "65 EICs differ" in `entity_name` is 60 operators (short versus full name) plus the 5 UK facilities, which differ because each member keeps a different duplicate. The page does not repeat the figure.
- **Defects.** The writer's Defects section reproduces as stated. One refinement: blank facility `type` becomes null in the listing and stays `""` in the summary for 4 EICs. The fifth listing null (`55WHUMBLY1GROVER`) is `DSR` in the summary because the members keep different UK entries. For the backlog, the defects are:
  - the dedup on `entity_code`;
  - the per-day copies;
  - bronze filed under `--start`;
  - dropped operational dates;
  - the blank-type inconsistency;
  - the missing views, since resolved.
