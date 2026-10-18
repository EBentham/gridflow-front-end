# Held pages, Ancillary services part 2: writer round 2 (2026-10-18)

Answers `held-b-review.md`. Every finding is fixed: 2 majors and 15 nits. I edited only the `page:` blocks of the four
canonical notes (front matter, CRLF kept on every line, body untouched) and mirrored each byte for byte (`cmp` clean on
all four).

| Page | Build `--only` | Detector | Em or en dashes / banned words |
|---|---|---|---|
| `contract-transfer-of-obligation` | `contract_transfer_obligation` ok | `[]` | 0 / 0 |
| `disaggregated-bsad` | `disaggregated_bsad` ok | `[]` | 0 / 0 |
| `non-bm-ancillary-service-dispatch-platform-asdp-window-prices` | `asdp_window_prices` ok | `[]` | 0 / 0 |
| `obligatory-reactive-power-service-orps-utilisation` | `orps_utilisation_reactive` ok | `[]` | 0 / 0 |

Screenshots: `held-b-shots\r2-*` (ORPS and ASDP at 1440 and 390). I also read both 390 views in slices through my
390 px iframe. Nothing is clipped or overlapping. My 9979 server is stopped; 9670 was not touched.

## Majors (ORPS)

1. **Archive columns.** The lead member's `differs` now reads "Lead, lag, total by month, April 2020 to December 2024,
   plus the long file". The historic member's matches: "Lead, lag and total by month, October 2013 to March 2020". In
   the lead line, "Lead, lag, total" (not "and total") keeps it inside the 14-word budget.
2. **The long file stays in bronze.** `raw_feed.note` now ends "Bronze only: the workbook, PDFs and newer long file,
   which repeats a complete row." To fit 30 words, the first sentence is shortened, and "swap in any key" moved to
   the ingest command's comment. I checked bronze: the long file's `Month-Year` runs April 2020 to August 2026, so it
   restates the archive's months and adds the later ones. No dates from this go on the page.

## Nits

| Finding | Fix |
|---|---|
| Contract 1, EAC | `how_used[1]`: "Read beside the Enduring Auction Capability (EAC) results that NESO tags this package with" |
| Contract 2, unsourced relation | `related[2]`: "The Balancing Reserve requirement forecast" |
| Disaggregated 1, cadence goes stale | "NESO states no update frequency; the newest file is the current financial year" |
| Disaggregated 2, which dump | Raw-feed note: "... uploads to 2020-21, dumps from 2021-22 (2013-14 and 2026-27 shown). Ingest only: no silver table." |
| Disaggregated 3, unstated use | `how_used[0]`: "Cost and volume of individual balancing actions outside the Balancing Mechanism" |
| ASDP 1, OBP and Non-BM | Cadence: "... moved to its Open Balancing Platform". `what_it_is`: "Non-BM STOR and Fast Reserve (outside the Balancing Mechanism)" and "The Open Balancing Platform (OBP) uses other ids" |
| ASDP 2, reason for no join | "The Open Balancing Platform (OBP) uses other ids: never join the two." To fit 60 words, "Each change is a row:" became "Each row gives" and "window start and end" became "window" |
| ORPS 3, held reason | "Some long-file values differ, with 0 for blanks; NESO does not say which file to use." (16 words; the review's text was 22) |
| ORPS 4, lead and lag | "lead (read as absorbed) and lag (read as produced)". To fit, "Generators covered by the Grid Code" became "Grid Code generators", and the last sentence became "Another table holds default payment rate inputs." |
| ORPS 5, BM unit | Summary: "each unit" |
| ORPS 6, dash | "NESO does not say what a dash cell means; one unit appears twice, with different values." |
| ORPS 7, pound sign | "NESO gives the three power-price inputs only a pound sign, with no denominator." |
| ORPS 8, two rates | `how_used[1]`: "The two default rates NESO pays for reactive power, in £/MVArh, by month" |

## Defects

None new. The round-1 defect stands: the `disaggregated-bsad.md` body still says each file was fetched once, but
bronze also holds the 16 October fetch of the 2026-27 file. The ledger row is unaffected.

Summary: I fixed all 17 findings (2 ORPS majors, 15 nits) on the four held pages. All four rebuild clean, with detector `[]` and mirrors `cmp`-identical.

## Nits fixed (answering `held-b-review-2.md`)

| Nit | Fix |
|---|---|
| ORPS newer-table member line | `differs`: "Lead, lag, total by month, April 2020 to December 2024; long file bronze only" (14 words) |
| ORPS archive reason, differ from what | `held`: "The long file alters some archive values, zeroes blanks; NESO does not say which to use." (16 words) |

Gates: `page:` block only (CRLF kept), mirrored, `cmp` clean; `gridflow-build --only neso_data_portal/orps_utilisation_reactive`
ok; detector `[]`; 0 em or en dashes.

Summary: Both ORPS nits are fixed; the page rebuilds clean with detector `[]`, and all four held pages are approved.
