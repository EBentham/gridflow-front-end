# Held Carbon intensity pages: writer report (2026-10-24)

Packages: `carbon-intensity-of-balancing-actions` (`ci_balancing_actions`), `country-carbon-intensity-forecast` (`country_ci_forecast`), `national-carbon-intensity-forecast` (`national_ci_forecast`), `regional-carbon-intensity-forecast` (`regional_ci_forecast`). Each is a one-table held page (`page.held: <reason>`) with no chart, frame, notebook or artefacts. Vault worktree `C:\gridflow-wt\vault-neso-ci`, front-end worktree `C:\gridflow-wt\fe-neso-ci`. Nothing is staged or committed.

## Gates

| Gate | Result |
|---|---|
| CRLF | Notes edited with the Edit tool. 0 bare LF: 298, 243, 266 and 316 lines, all CRLF |
| Mirror | `cp` to `vault\neso_data_portal\<slug>.md`, then `cmp`: clean on all four |
| Build | `gridflow-build --only neso_data_portal/<key>` (`ci_balancing_actions`, `national_ci_forecast`, `country_ci_forecast`, `regional_ci_forecast`) wrote each page with the dataset template and no errors. The only warning is the repo-wide "Known issues" one |
| Detector | `[]` on all four built pages |
| Artefacts | None. No series, sample, notebook, staged spec or authored override exists for any key |
| Rendered `<main>` | No em or en dashes, arrows or middle dots. None of: live, now, real-time, soon, pending, planned, shipped, coming, locally, ruling, ledger, TODO, held, yet, E-SEM, "our ", "since 20". Viewport meta is present |
| Related links | Every related key passed the build's resolve check. The targets (`elexon/boal`, `wind-bmu-boa-volumes`, `neso/carbon_intensity`, `neso/regional_intensity`, `historic_generation_mix`) are not built in this worktree, because I only ran `--only` builds |
| Screenshots | 1440, 1024 and 768, plus 390 through a 390 px iframe, for all four pages on port 9921. Files are in `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\ci-held-writer\shots\`. I looked at regional at 1440 and balancing actions at 390: nothing is clipped or overlapping, and long URLs and commands wrap. Light mode only. The server was started in Bash with its PID recorded (52718) and stopped by that PID. 9670 was not touched |

## The hold lines (16 words each, budget 16)

The four lines share one opening clause, word for word: "No row says when NESO first published it". The second half differs because gridflow's hold questions differ:

- **national, country:** "No row says when NESO first published it, and NESO changes values for past half hours."
- **balancing actions, regional:** "No row says when NESO first published it, or whether times mark half-hour starts or ends."

How I checked the batch's gloss ("the files don't say when each row was first published") against the sources:

- **national and country:** the gloss matches the registry and the eligibility report ("no issue column; which forecast issue a past target's value reflects, and whether values are revised after the period"). Both bronze pairs show NESO changing values for half hours that were already past (below). That is the second half of the line.
- **regional:** the registry asks three questions: issue and revision, period start or end, and negative intensities. Issue and period position apply to every row, so they go in the line. Negatives affect only two columns, so they sit in `what_it_is` as a dated fact.
- **balancing actions:** the registry question is **only** "whether DATETIME marks period start or end". Ruling 521 says this hold "has no issue-clock part". But the two captures show NESO revised 4 past half hours, so the first-publication clause is true and relevant too. The line covers both. This mismatch is a seat item (see Defects): either the registry gains the revision question, or the seat drops the shared clause from this page.

## What each page says

All four pages:
- define carbon intensity in NESO's catalogue words ("CO2 emitted per kWh of electricity consumed");
- give cadence as "Hourly, NESO says" or "Daily, NESO says", from the snapshot extras;
- carry a dated history fact from NESO's October 2026 files;
- show a raw feed of `package_show`, the CSV, and the methodology PDF where the package has one;
- give commands as `ingest` and `transform` with `--last 24h`, plus `ingest <key>_files` for the PDF.

**Balancing actions** (`market` landscape):
- `FPN`, `BOA` and `Difference` are described in the dictionary's words. NESO's term is "Final Physical Notice".
- From the PDF, issued April 2021: the measure "is not a measure of emissions but instead tracks the difference of carbon intensity", and it excludes "interconnectors or small BMUs".
- "Fetched 16 October 2026, the file had changed values for half hours past on 8 October."
- Related: `elexon/boal`, `wind-bmu-boa-volumes` (the PDF's own example is wind bid down for a constraint, which raises BOA), and `national-carbon-intensity-forecast`. There is no Carbon Intensity API link: the PDF names the API only as reference [1], and the API serves no balancing series.

**National:**
- The forecast, the actual "estimated from metered generation", and the band (`very low`).
- "NESO's May 2024 methodology opens with its Carbon Intensity API, forecasting 48 hours ahead." The PDF text is: "NESO's Carbon Intensity API provides an indicative trend ... up to 48 hours ahead" and "Forecast carbon intensity is provided 48 hours ahead of real-time".
- The dated statement that actuals were changed.
- Raw-feed note: "Its October 2026 CSVs end in about four weeks of empty rows."
- Related: `neso/carbon_intensity` ("which this package's methodology describes"; the tie is NESO's PDF text, and no numbers are equated), regional, country, `historic_generation_mix`.

**Country:**
- Three columns, each of which NESO calls a forecast "predicted using machine learning models and metered generation".
- The dated statement that values were changed.
- No API link: no NESO text in the country package ties it to the API. The vault note's region 15 to 17 mapping is the project's, not NESO's.
- Related: national, regional.

**Regional:**
- The summary describes 14 regions on DNO boundaries, from the dictionary and the PDF.
- What it is: the PDF, issued May 2024, describes regional forecasts in the Carbon Intensity API, and two regions carry negative values NESO does not explain.
- History: "NESO's October 2026 files run from 17 September 2018 to 24 July 2026".
- Raw-feed note: "Fetched 16 October 2026, the CSV matched 8 October's byte for byte."
- Related: `neso/regional_intensity` (tied by the PDF), country, national.

## Evidence

| Claim | Evidence |
|---|---|
| Hold questions | Registry JSON `record.eligibility` for each package; `docs/neso_data_portal/eligibility.md` lines 68, 73, 211, 262; ledger rows 10-13 (all "E-SEM") |
| No issue column on any table | Registry epochs: `issue: {kind: none}` on all four |
| Catalogue text, cadence, resource names and URLs | Snapshot `20261006T195819Z` `catalog-snapshot.json`: notes, extras, resources |
| Column meanings and units | Field info `20261008T114228Z/<key>.json` |
| PDF statements | `pdftotext` of the three bronze PDFs. Balancing: "Issue: April 2021". National and regional: "Issue: May 2024"; the API sentences are quoted above |
| Request URLs | Equal to each sidecar's `request_url`; `package_show` is the connector form |
| Upload rule ("downloaded whole unless `last_modified` is unchanged") | `client.py` `iter_members` docstring (about lines 1661-1672) |
| Keys exist | `config/sources.yaml` lines 822-823, 830, 992-993, 1027-1028 |
| Second captures | Bronze 2026-10-16: balancing `c7f20642` (`last_modified` 2026-10-16T11:44:41), country `311c2cf4` (19:10:24), national `5ac01f8b` (20:10:47), regional `0b435a16` (20:10:38, same sha256 as 8 October). No PDF recaptured. Silver: a second Parquet file per key (96,595; 141,413; 155,561; 136,190 rows) |
| Balancing revisions | Of 96,163 shared timestamps, none dropped and 432 appended. `FPN` is unchanged everywhere. `BOA` and `Difference` changed at 2026-10-06T00:00 and 00:30 and 2026-10-07T00:00 and 00:30 (`BOA` 224.85 to 229.33 ...), all past at the first upload |
| National changes | 155,159 shared targets, none dropped, 402 appended (blank). `actual` changed on 30 targets from 2026-10-07T10:30 to 2026-10-08T10:00, all before the first file's stamp (11:11:23). `forecast` changed on 100 targets, all ahead of the first file. `index` changed on 8 targets. 402 blanks were filled |
| Country changes | 141,009 shared targets, none dropped, 404 appended. 110 targets changed. 9 of them (2026-10-08T04:30 to 09:00; England 4, Wales 9) were before the first file's stamp (09:10:31) |
| Regional | Both bodies are byte-identical. Every column ends at 2026-07-24T12:00. Negatives: West Midlands 6 (min -13), London 329 (min -8) |
| History fact | First labels in both bodies: balancing 2021-03-31T00:00, national 2018-01-01T00:00, country and regional 2018-09-17T23:00 |
| National empty tail | 1,339 all-blank rows after the last forecast in each body (2026-11-07T11:00 and 2026-11-15T20:00 ends) |

The scripts are `compare.py`, `past.py`, `first.py`, `gaps.py`, `days.py` and `silver.py`, all in `...\scratchpad\ci-held-writer\`, all read only.

## Body corrections (canonical notes; each gets `updated: 2026-10-24`)

- **Balancing actions:**
  - Clocks give both captures' `last_modified` and write instants.
  - Identity: both captures are unique, and a new "Second capture" bullet records the appends and the 4 revisions. The rewrite TODO is replaced by a revision-policy TODO that notes the registry question gap.
  - Multiplicity is given for both captures.
  - A second silver file is recorded.
  - Cadence: each file ended at 00:30 on its upload day (two observations). The label gaps are listed: nine days with only 00:00 and 00:30, four days absent, and 2022-10-27T23:30 missing.
  - PDF paragraph: quoted statements, the API cited only as [1], no 16 October capture.
- **National:**
  - The second capture is added under Captured and in clock 1.
  - The blank census is extended, with the empty tail.
  - Identity is given for both bodies.
  - A second silver file is recorded.
  - PDF paragraph: issue date, the API sentence, and the "regional" wording oddity.
  - A new "Second capture" block under Cadence.
- **Country:**
  - Clock values for the second capture.
  - Blanks are the same in both captures.
  - Identity is given for both. The "only one capture" TODO is replaced by the measured comparison, which shows past values rewritten, plus a narrower TODO.
  - A "Second capture" row in the silver table.
  - The Cadence paragraph is updated.
- **Regional:**
  - Intro: "the one capture held" becomes both captures.
  - The second, byte-identical capture is recorded.
  - Both clock values.
  - Keys: the file was re-stamped unchanged, and a second silver file is recorded.
  - Target coverage covers both captures.
  - PDF paragraph: quoted.
  - Cadence and silver path are updated.

## Not verified / open

- Whether 16 October runs tried the three `_files` keys at all. There is no bronze for them, and I read no run log.
- The national note body still says the CSV "is the bulk file of the same series that the Carbon Intensity API's national routes serve". This rests on the project's 675-period probe, not on NESO text. It is not public copy and the data does not prove it wrong, so I left it. The seat may want it softened under ruling 57.
- The country note maps the CSV to API regions 15 to 17 from the project probe; this is not on the page.
- Dark mode was not checked.
- `historic_generation_mix` related note says it "carries its own carbon intensity": this rests on that page's own summary.

## Template problems

None. The one-table held mode rendered as the brief describes. The page set's members are right: one table per package, and the `_files` families are catalogue only.

## Defects

- **gridflow registry (`carbon-intensity-of-balancing-actions.json`, hold question):** it names only "whether DATETIME marks period start or end", and ruling 521 says the hold has no issue-clock part. But the 2026-10-16 file revised `BOA` and `Difference` on 4 half hours already in the 2026-10-08 file (2026-10-06T00:00 and 00:30, 2026-10-07T00:00 and 00:30). Suggest adding the revision and first-publication question at the next registry edit.
- **NESO, Carbon Intensity of Balancing Actions:**
  - Past half hours are revised with no record (above).
  - Each daily file ended at 00:30 on its upload day (7 and 16 October 2026).
  - The body has nine past UTC days carrying only 00:00 and 00:30 (2022-03-26, 2022-04-25, 2022-08-24, 2022-12-26, 2023-01-26, 2023-02-24, 2023-09-17, 2023-10-05, 2026-03-06), four days absent (2023-01-27, 2023-10-06 to 2023-10-08), and 2022-10-27T23:30 missing.
  - The file is not in time order.
- **NESO, National Carbon Intensity Forecast:**
  - Estimated `actual` values for 30 past half hours (2026-10-07T10:30 to 2026-10-08T10:00) changed between the 8 and 16 October 2026 files, and forecasts are overwritten in place with no issue time.
  - Each file ends with 1,339 all-blank future half hours (about four weeks).
  - The unexplained `forecast` maximum of 13,579 is still present (it was already in the note).
  - The methodology PDF (May 2024) says it "details the methodology behind the regional carbon intensity estimates", although it is the national package's file.
- **NESO, Country Carbon Intensity Forecast:**
  - Values for 9 half hours already past on 8 October (2026-10-08T04:30 to 09:00) changed by 16 October 2026.
  - The file is not in time order.
  - Targets 2025-07-27T11:00 to 2025-08-03T07:00 are absent.
- **NESO, Regional Carbon Intensity Forecast:**
  - The 16 October 2026 file is byte-identical to the 8 October one under a new `last_modified`.
  - Targets still stop at 2026-07-24T12:00 against an "Hourly" cadence.
  - There are negative intensities (West Midlands 6, min -13; London 329, min -8).
  - Targets 2024-01-25T10:30 to 2024-02-16T20:00 and 2025-07-27T11:00 to 2025-08-03T07:00 are absent.
  - The dictionary example format `17/09/2018  02:30:00` does not match the ISO body (already in the note).
- **Planning (seat item):** the batch file's gloss says all four pages share one question; the registry disagrees for balancing actions and regional (see the hold lines above).

## What the checker should look at hardest

1. **The hold lines.** Should the second halves really differ by page, given that the launch prompt asked for identical wording? And is the shared clause fair on balancing actions, whose registry question is period position only?
2. **"NESO changes values for past half hours" (national, country) and "changed values for half hours past on 8 October" (all but regional).** Reproduce the comparisons with values compared as numbers, not strings. The strings change format (`40` becomes `40.0`), and comparing them as text inflates the counts to hundreds.
3. **The Carbon Intensity API links (ruling 57).** National and regional are linked on the strength of each package's methodology PDF text. Country and balancing actions are deliberately not linked. Check that no page equates the two sources' numbers.
4. **The national raw-feed note's "about four weeks of empty rows" and the regional "byte for byte" claim**, both dated NESO file facts.
