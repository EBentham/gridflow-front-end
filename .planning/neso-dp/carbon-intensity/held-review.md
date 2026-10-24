# Held Carbon intensity pages: checker review (2026-10-24)

Pages: `carbon-intensity-of-balancing-actions`, `country-carbon-intensity-forecast`, `national-carbon-intensity-forecast`, `regional-carbon-intensity-forecast`. Front-end worktree `C:\gridflow-wt\fe-neso-ci`, vault worktree `C:\gridflow-wt\vault-neso-ci`. Inspection only: nothing edited, no ingest, no live API.

## Verdicts

| Page | Verdict |
|---|---|
| carbon-intensity-of-balancing-actions | APPROVE with nits |
| country-carbon-intensity-forecast | APPROVE with nits |
| national-carbon-intensity-forecast | APPROVE with nits |
| regional-carbon-intensity-forecast | APPROVE with nits |

No blockers, no majors. Nine nits (below), none needs a re-check.

## Gates run

- `gridflow-build --only neso_data_portal/<key>` for all four: dataset template, no errors (the only warning is the repo-wide "Known issues" one). A full `gridflow-build --check` also passes ("idempotent across 183 pages + 7 hubs").
- Detector (`detect.mjs --json`) returns `[]` on all four built pages.
- Mirrors: `cmp` identical for all four. Each note is CRLF throughout (298, 243, 266 and 316 lines, 0 bare LF). Diff against `origin/master` is limited to the `updated:` date, the `page:` block and the body spans listed under "Body edits".
- Rendered `<main>` scan: no em or en dashes, arrows, middle dots, "live/now/real-time/soon/pending/planned/shipped/coming/locally/ruling/ledger/TODO/held/yet/E-SEM/since 20/rows/days/%". Viewport meta present. Page `<h2>` and nav anatomy as on other held pages.
- Screenshots (headless Chrome, own port 9931, server PID recorded and stopped by PID): 1440, 1024, 768, and 390 through a 390 px iframe, for all four. Looked at national at 1440, balancing at 390 and 1440 (full page), regional at 390 (full page): nothing clipped or overlapping, long URLs and commands wrap, bronze and silver strata corner labels intact. Light mode only; dark not checked.
- Related links: every target exists in a full build of the worktree (`elexon/boal`, `neso/carbon_intensity`, `neso/regional_intensity`, `wind-bmu-boa-volumes`, `historic_generation_mix`, and the three sibling pages).

## 1. "NESO changes values for past half hours" (national, country): reproduced

Method: both bronze CSVs per table read with Polars as strings, joined on `datetime`, columns cast to Float64, compared as numbers (both non-null and unequal), plus null to value transitions counted separately. "Past" means the target label is at or before the first file's CKAN `last_modified`.

| Table | Shared targets | Dropped / appended | Numeric changes (both non-null) | Of those, past at first file's stamp | Text-only differences (`51` vs `51.0`) |
|---|---|---|---|---|---|
| country | 141,009 | 0 / 404 | Scotland 6, England 105, Wales 110 | Scotland 0, England 4, Wales 9 (9 distinct targets, 2026-10-08T04:30 to 09:00; stamp 09:10:31) | 337, 238, 233 (this is what inflates a text comparison to hundreds) |
| national `actual` | 155,159 | 0 / 402 | 30 | 30, 2026-10-07T10:30 to 2026-10-08T10:00 (stamp 11:11:23); example 124 to 123 | 402 |
| national `forecast` | | | 100 (2026-10-08T11:30 to 10-10T13:30) | 0 | 402 |
| national `index` | | | 8 (`moderate` to `low`) | | |
| balancing `BOA`, `Difference` | 96,163 | 0 / 432 | 4 each (2026-10-06T00:00 and 00:30, 2026-10-07T00:00 and 00:30; `BOA` 224.85 to 229.33 first row) | 4 (stamp 2026-10-07T11:38:19) | 0 |
| balancing `FPN` | | | 0 | | 0 |

Every number in the writer's report and the note bodies matches, with one exception (nit 5: nine versus eight). National's 402 appended rows are all blank, and 402 blank rows in the first file were filled. The sidecar stamps used (`ckan_last_modified`: 2026-10-07T11:38:19.659640, 2026-10-16T11:44:41.199607 for balancing; 2026-10-08T09:10:31.323607 and 2026-10-16T19:10:24.514761 for country; 2026-10-08T11:11:23.285254 and 2026-10-16T20:10:47.063996 for national) match the notes.

The claim is true: past targets were rewritten in both files, and in national it is the `actual` column. National's forecasts changed only for targets still ahead of the first file, which the note says correctly. It is not dated in the hold line itself (nit 3), but the dated version sits in `what_it_is` directly above.

## 2. "or whether times mark half-hour starts or ends" (balancing, regional): matches

- Balancing: registry `record.eligibility.question` is exactly "TODO: whether DATETIME marks period start or end"; eligibility report line 68 says the same. True: the dictionary calls `DATETIME` "Time stamp of record" (UTC ISO 8601, example `2021-03-28T14:30`) and the April 2021 PDF does not say where in the half hour it sits (`pdftotext` read).
- Regional: the registry question has three parts (no issue column and revisions undocumented; whether `datetime` marks start or end; meaning of negative intensities, min -13.0). The line covers the first two; negatives are covered on the page in `what_it_is` (nit 2). The dictionary says only "Timestamp of record, given in UTC", and the PDF is silent. The vault note also says the probe that settled "start" for national and country could not be run for regional (no overlap with the API). The second half is therefore true and is the registry's question.
- National and country carry no start-or-end clause, which is right: the registry gives them `utc_instant` and their questions are the issue clock and revision.

## 3. Carbon Intensity API links: fair, no equating

Both PDFs read with `pdftotext` (bronze `*_files` captures, 8 October 2026).

- National PDF ("Carbon Intensity Forecast Methodology", Issue: May 2024): "NESO's Carbon Intensity API provides an indicative trend of carbon intensity for the electrical grid of Great Britain up to 48 hours ahead of real-time [1]", plus the GB-wide formula and index bands. The catalogue calls it "a detailed description of national carbon intensity forecast methodology". The related note "The Carbon Intensity API's national routes, which this package's methodology describes" stands on that. (The PDF's next sentence says it details "the regional carbon intensity estimates", a NESO slip the writer put in the note body, not on the page.)
- Regional PDF ("Carbon Intensity Regional Forecast Methodology", Issue: May 2024): "NESO's Carbon Intensity API has been extended to include forecasts for 17 geographical regions ... up to 48 hours ahead", regions follow DNO boundaries. This ties the API's regional routes to this package.
- Balancing PDF (Issue: April 2021) only points to the API as reference [1] ("for more information about the Carbon Intensity visit here"). No link is the conservative choice and it is fine. Country has no PDF and no NESO text tie. Fine.
- No rendered page equates the two sources' numbers. The related notes say "which this package's methodology describes", not "the same series". (Unrendered body sentences do: nit 6.)

## 4. Facts, dates, raw feeds

- **Hold lines:** the four share the first clause word for word and are 16 words each (budget 16). First clause is true for all four (no issue column, `issue: {kind: none}` in every registry epoch; the CSV columns are `datetime` plus values).
- **Facts tables:** cadence from the catalogue snapshot `20261006T195819Z` extras ("Update Frequency" Daily for balancing, Hourly for the other three). History: first labels in both bodies are balancing 2021-03-31T00:00, national 2018-01-01T00:00, country and regional 2018-09-17T23:00; regional last label 2026-07-24T12:00 in both bodies. All as on the page. Vendor line names the package and files (balancing: CSV plus PDF; country: one CSV; national and regional: CSV plus PDF), matching the registry resources.
- **Definitions and quotes:** "CO2 emitted per kWh of electricity consumed" is the catalogue notes (national, regional, country). `FPN`, `BOA`, `Difference` and the "positive when BOA is higher" rule are the dictionary's words; "Final Physical Notice" is the PDF glossary's term. Country, regional "machine learning models and metered generation" and national "estimated from metered generation" are dictionary text. 14 regions on DNO boundaries: 14 value columns, dictionary says "DNO region", PDF says DNO boundaries.
- **Page-only measured facts, all re-derived:** regional negatives West Midlands 6 (min -13), London 329 (min -8), identical in both bodies; national tail 1,339 all-blank rows after the last forecast in each body (27.9 days, "about four weeks"; ends 2026-11-07T11:00 and 2026-11-15T20:00); regional 16 October body sha256 `0b435a16...` identical to 8 October's (13,180,555 bytes), so "matched byte for byte" is true and the CKAN stamp moved (2026-10-08T11:11:10 to 2026-10-16T20:10:38).
- **Raw feed requests:** every URL on the pages equals the matching bronze sidecar `request_url` (CSVs and the three PDFs: `eso-ci-balancing-actions-methodology_neso.pdf`, `neso-ci-national-methodology_v2.pdf`, `neso-ci-regional-methodology_v2.pdf`) and the resource ids match the registry. `package_show?id=<slug>` is the connector's form. The "downloaded whole unless `last_modified` is unchanged" rule is the `iter_members` upload rule and is worded as on approved pages.
- **Commands:** `ingest` and `transform` keys are real; the `_files` keys are real for the three packages that have a PDF; balancing has no second CSV and country has no PDF, and neither shows one.
- **Related notes:** all at most 12 words; `historic_generation_mix` does carry a `carbon_intensity` column (its own page); `wind-bmu-boa-volumes` defines `BOA_Volume` as curtailed generation, matching "Wind curtailed by accepted bids"; the PDF's own example (wind bid down, gas offered up, BOA profile higher) supports "a case NESO says can raise BOA".
- **No local data, codes or planning words** on any page. "Fetched 16 October 2026" is a dated NESO file fact in the same form as the approved wind BOA page.

## Body edits (canonical notes)

All four add `updated: 2026-10-24` and stay in the smallest spans: second-capture clocks and write instants (match sidecars), identity counts for both bodies (96,163 and 96,595; 141,009 and 141,413; 155,159 and 155,561; 136,190 twice, all with 0 duplicates), the second silver file (silver has two Parquet files per key with exactly those row counts), PDF text quotes (match `pdftotext`), balancing cadence and gaps (re-derived: nine past days with only 00:00 and 00:30, days 2023-01-27 and 2023-10-06 to 08 absent, 2022-10-27T23:30 missing), country and regional target gaps (2025-07-27T11:00 to 2025-08-03T07:00; regional also 2024-01-25T10:30 to 2024-02-16T20:00), and the national, country and balancing revision paragraphs (table above). Stale "one capture" TODOs are replaced by measurements. No unrelated rewrites.

## Findings

1. **Nit, `ci_balancing_actions` `page.held` (first clause).** The registry's hold question and the eligibility report name only period position, and the vault's own ruling text says this hold "has no issue-clock part". The line adds "No row says when NESO first published it". It is true (4 past half hours revised between the 8 and 16 October files, above), but it is a reason gridflow's registry does not give. The writer already logged the registry gap as a defect; the seat should either update the registry's question or accept the page as ahead of it.
2. **Nit, `regional_ci_forecast` `page.held`.** The registry holds on three questions; the line gives two. Negative intensities are on the page in `what_it_is`, so nothing is hidden, but the line alone does not cover the whole table. Word budget makes this unfixable inside the line.
3. **Nit, `country_ci_forecast` and `national_ci_forecast` `page.held`.** "NESO changes values for past half hours" is undated and present tense, measured across two captures eight days apart. The dated form ("Fetched 16 October 2026, the file had changed...") is in `what_it_is` right above it, and approved held pages use undated present tense for vendor behaviour, so this is acceptable as it stands.
4. **Nit, `page.what_it_is` on balancing, country and national.** "the file had changed values for half hours past on 8 October" does not say changed relative to what, and "on 8 October" can be read as the date of the half hours (true only for country; balancing's were 6 and 7 October, national's 7 and 8). Suggest "changed values for half hours already past in its 8 October copy" if the field budget allows.
5. **Nit, country note body, "Silver at activation / Identity" paragraph and writer report.** "Nine of them ... already past" (England 4, Wales 9) counts the 09:00 target against the 09:10:31 stamp. The note itself says labels mark period start, so the 09:00 half hour was still running; by that rule eight targets (04:30 to 08:30; Wales 8, England 3) were past. The page text is unaffected.
6. **Nit, national note body (line 57) and regional body (line 53), country body (line 50).** Sentences such as "the bulk file of the same series that the Carbon Intensity API's national routes serve" and "country tier of the Carbon Intensity service: regions 15, 16 and 17" rest on the project's API probe, not NESO text (the writer flagged this). Not rendered on a held page, so no rendered page equates the sources, but soften them before a body is ever published.
7. **Nit, regional page.** The linked PDF says the API carries 17 regions; the file has 14 columns. The related note does not equate them, so it is fine; a reader following the link may wonder, so a caution in the note body would be kind.
8. **Nit, all four `page.raw_feed.note`.** Several approved pages add "Dates select nothing" beside commands that carry `--last 24h`; these four omit it. Optional.
9. **Nit, balancing `page.landscape: market`.** The scene is the transmission and battery drawing; defensible for balancing actions, taste only.

## Not checked

Dark mode. Whether the 16 October runs attempted the three `_files` keys (no bronze, no run log read). The 1024 and 768 shots were taken for all four pages but I looked at the 1440 and 390 views in detail only.
