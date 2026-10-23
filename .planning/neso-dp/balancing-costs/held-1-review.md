# Held pages, Balancing costs part 1: checker review (2026-10-23)

Checked against the batch file, standing instructions, the writer's report `held-1-author.md`, the four canonical note diffs
against `origin/master` in `C:\gridflow-wt\vault-neso-bc` (front matter insertions only), the mirrors in
`C:\gridflow-wt\fe-neso-bc\vault\neso_data_portal\`, the built pages, the ledger rows, the gridflow registry JSON and
`iter_members` (client.py), the NESO catalogue snapshot (20261006T195819Z) and field dictionaries (field-info 20261008T114228Z),
and the bronze sidecars and bodies under `C:\gridflow-data\bronze\neso_data_portal\` (read only).

Gates: `gridflow-build --only neso_data_portal/<lead>` ok on all four (my own run); `cmp` canonical note against mirror clean on
all four; detector `[]` on all four; 0 em or en dashes in the rendered text; none of live, now, yet, soon, pending, coming,
planned, shipped, real-time, locally, ruling, ledger, TODO in the built HTML; no capture dates, row counts or other local figures
on the pages; the pound sign renders correctly (no mojibake); 390 view through my own 390 px iframe on port 9932: `scrollWidth`
equals viewport width on all four, nothing but the template's hero scenery paths extends past the edge (identical on all four, so
not page content); header and facts block read at 390 on the cost page. Server on 9932 started with its PID recorded and stopped by
that PID; 9670 untouched. The `--only` builds print the known "Known issues" caveat warning (35 lines, all from the shared notes'
bodies, none rendered); no errors on these pages.

Seat rulings applied: titles follow the manifest names shortened to six words; the inertia page carries one related link (the two
natural targets, `system-inertia` and `system-inertia-cost`, have no mirrored note yet; confirmed, they are absent from
`vault\neso_data_portal\`); registry status reading `eligible` on all four is the known pattern. Neither is a finding.

## What I checked, per the four asks

**1. "Rows not shown" lines against the ledger.** All four match the ledger question, with no codes and no planning words.
Fixed tariffs: "NESO dates each publication but not when each row appeared, nor whether old rows change." (15 words) is the
registry hold question (issue clock, availability at the Published Date, immutability); true to the data too (every published
date precedes its start date, so the dates are NESO's own, but nothing says when a row went live). Inertia: "NESO's units
disagree, £/GVA or £ per GVAs, and it never says what a zero means." (16 words, at the budget) is exact: every field dictionary
says `£/GVA`, the package notes say "£ per GVAs", and nothing in the catalogue text or dictionary defines a zero (779, 773 and
773 of 1,096 days are zero in the three method columns, so the question is substantive; not stated on the page, correctly).
Daily forecast and daily cost: "no settlement run to key them by" is the ledger's and the ruling's reason in plain words and is
true (neither body has a run column; the cost dictionary even words `SETT_DATE` as the payment date "in relation to an Initial
Settlement Run" without labelling any row). It is accurate on the cost page. On the forecast page it is accurate but borrowed:
see finding 3.1. The reader is pointed to the current-charges page, which is linked on both and is titled "BSUoS charges by
settlement run", so the term is explained one click away.

**2. Raw feed and files against bronze.** Fixed tariffs: one capture; inertia: one capture; forecast: five captures, one per
resource, all `url_type: upload`; cost: ten yearly resources plus the workbook (2017-18 to 2026-27, as the registry and the page
say), 11 captures of the yearly family because 2026-27 was captured twice (8 and 16 October, 733,417 then 774,080 bytes, 8,826
then 9,306 rows) and one workbook capture. Every request URL on every page equals the bronze sidecar `request_url` for that
resource; `package_show` is `/api/3/action/package_show?id=<package>`. "Downloaded whole unless its `last_modified` is unchanged"
matches `iter_members` (an upload member whose newest usable capture carries the live `last_modified` is skipped). The commands
are right: the two silver pages carry ingest and transform, the two bronze-only pages carry ingest only; the cost page adds the
`daily_balancing_costs_files` ingest for the workbook (family `daily_balancing_costs_files`, resource `bfd081bc`, registry
disposition HOLD). **No page states a capture date or a newest capture**, so none can be stale: the cost page's only "newest" is
"the newest file is the current financial year", which is true now (2026-27 is the current April-to-March year) and stays true
whenever read, and its request lines name the first and newest *resources*, which is correct whatever the capture dates.
The writer's defect is confirmed (see Defects below); it is in the vault body, not on the page.

**3. Facts tables and what-it-is against NESO's text and gridflow code.** Fixed tariffs: vendor, cadence (extras `Biannual`;
package text "six monthly basis (when tariffs are published)"), grain (registry entity key `publication`, `fixed_tariff_title`,
`published_date`), rate in £/MWh (field unit `£/MWh`), revenue team (package text) all correct; the data holds three stages
(Draft, Final, Initial Forecast), so "such as draft or final" is true. Inertia: cadence `Ad hoc`, grain one day (1,096 rows,
2019-04-01 to 2022-03-31, not stated on the page), method definitions from the dictionary; units not stated beyond the held line,
correct for an unresolved unit. Forecast: five files, 2018-19 to 2022-23, "data being present from December 18", `Not Active`,
CMP361 and the "may bear no relation" disclaimer are all NESO's; £/MWh, £ and MWh from the header text; byte `0xA3` is in the
header of every one of the five files (`od` shows octal 243 in all five). Cost: six £ columns from the dictionary, per settlement
period (not per day), `SETT_DATE` payment-date wording, `Weekly`, one file per April-to-March year from 2017-18 all correct.
The cost resources' own descriptions say "total balancing cost (per MWh)" while every column is £ in the dictionary; the page
follows the column dictionary, which is the sound choice.

**4. Related links.** All resolve (build ok) and every note is true to its target: fixed tariffs to current charges, monthly
forecast ("rolling 24-month" in its note) and daily forecast (ended April 2023); inertia to constraint breakdown (its field
`increasing_system_inertia_cost_gbp` is "Increasing system inertia, £", one of four reasons); forecast to current charges, cost,
volume (half-hourly MWh, eight categories) and monthly forecast; cost to volume, current charges, constraint breakdown and the
daily forecast. Seat note, not a finding: the links to `daily-balancing-volume-...` and `bsuos-monthly-forecast` (and the
current-charges page) resolve only because those pages are in the page set; they carry content only when the other writers' pages
ship in the same PR. If the second held batch is held back, these links open a name-only page.

## 1. `bsuos-fixed-tariffs` (lead `bsuos_fixed_tariffs`): APPROVE

1. **nit** `page.facts.cadence`: "Biannual" is ambiguous in English (twice a year, or every second year), and NESO's own package
   text says "six monthly". Suggest "Biannual, as NESO lists it (six monthly): updated when tariffs are published" (12 words, under
   the 14-word fact budget).

## 2. `gb-system-inertia-bid-and-offer-costs` (lead `inertia_bid_offer_costs`): APPROVE

1. **nit** `page.what_it_is` (and `how_used[1]`): "at the average bid price (A), the average wind bid price (B) or the highest bid
   price (C)" reads as three prices of the inertia offers. NESO's dictionary says only Method A is "based on the average bid price";
   B and C are "assuming the units replace energy taken off at the average wind bid price" and "...at the highest bid price", i.e.
   the price assumed for the energy the inertia units displace. Suggest "at the average bid price (A), or assuming the energy
   displaced is replaced at the average wind bid price (B) or the highest bid price (C)". The field is at 59 of 60 words, so
   something has to give: "NESO calls them indicative, using all bid prices, not only accepted ones" can become "NESO calls them
   indicative: they use all bid prices." The `how_used[1]` line ("the bid price assumed") is acceptable once `what_it_is` is fixed.
2. **nit** `page.what_it_is`: "NESO tags some accepted Balancing Mechanism offers as bought for system inertia" names NESO as the
   tagger; NESO's text only says offers "tagged as being for System Inertia". Suggest "Some accepted Balancing Mechanism offers are
   tagged as bought for system inertia."

## 3. `balancing-services-use-of-system-bsuos-daily-forecast` (lead `bsuos_daily_forecast`): APPROVE

1. **nit** `page.held`: "Rows carry no settlement run to key them by, and the header's £ is not UTF-8." is the ledger's reason and
   true, but two things read oddly on a forecast page. A forecast is not settled, so "settlement run" invites the question why it
   would have one; the true gap is that nothing says which run or when each forecast was issued (the page already says history and
   future are mixed). And a pound sign is not "not UTF-8"; the file stores it as the single byte `0xA3`, which is not valid UTF-8.
   Also, unlike the cost page, the line never says there is no silver table, while the section is headed "The silver tables" (the
   raw feed note does say it). Suggest "Rows name no settlement run or issue time, and the header's £ is not valid UTF-8." (15
   words); the raw-feed note already carries "no silver table".
2. **nit** `page.what_it_is`, `page.summary`, `page.title`: "BSUoS" is never expanded on this page (it is the title and the first
   word of the body). The fixed tariffs page expands it; earlier reviews flagged the same for EAC and OBP. Suggest "The Balancing
   Services Use of System (BSUoS) charge recovers ..." (watch the 60-word budget; the field is about 62 with it, so drop "NESO
   forecast it per half hour as" to "It is forecast per half hour as").

## 4. `daily-balancing-costs-balancing-services-use-of-system` (lead `daily_balancing_costs`): APPROVE

1. **nit** `page.held`: "Rows carry no settlement run to key them by, so there is no silver table." Accurate (see ask 1) but "key
   them by" is gridflow's engineering term. Suggest "Rows are not labelled with a settlement run, so there is no silver table."
   (14 words).
2. **nit** `page.raw_feed.note`: "Bronze only: NESO's workbook of missing settlement periods." sits after the sentence about the yearly
   files and reads as if only the workbook is bronze only, when every file here is (the held line and the first ingest comment say
   so). Suggest "Everything here is bronze only; the workbook lists NESO's missing settlement periods." (within the 30-word budget).
3. **nit** `page.summary`: "split into six categories from energy imbalance to constraints" describes a range, but the six are
   energy imbalance, frequency control, positive reserve, negative reserve, constraints and other, and the column order differs by
   year. Suggest "split into six categories, from energy imbalance to other costs" or name the six (the body already does).
4. **nit** `page.what_it_is`: "BSUoS" is not expanded (see finding 3.2); the cost page starts "BSUoS recovers the cost ...".
   Expand at first use; the field is at the 60-word edge, so trim "from generators and suppliers" if needed (NESO's text, but not
   needed here).
5. **nit** `page.how_used[1]`: "An implied cost per MWh, with the volume package for the same periods" is the note's own suggested
   use, and a sound one, but the volume file has eight categories against six here, so only an overall figure works. Suggest "An
   implied overall cost per MWh, with the volume package for the same periods" (14 words).

## Defects (not page findings; for the seat to paste)

- **Vault note body, `daily-balancing-costs-balancing-services-use-of-system.md` (and its mirror), is stale on captures.** Confirmed:
  bronze holds a second capture of the 2026-27 file, `raw_20261016T200131Z_1d040751-f77f-4641-9130-d49f8cbfe54f_db15c574.csv`,
  774,080 bytes and 9,306 rows, against the 8 October capture's 733,417 bytes and 8,826 rows. The body still says the newest capture
  is 2026-10-08 (line 97), that "only the 2026-2027 resource changed in October 2026" (line 204), and shows 733,417 bytes, 8,826
  rows and "ten resources total 166,538 body rows" for that file. The page itself states none of this. The sibling volume note very
  likely has the same pattern (not checked, outside this package).
- **Registry eligibility reads `eligible`** on all four packages while both silver families are held and the other two have no
  record (known pattern).
- **Manifest lead and member lists are correct** for all four; no change suggested.

## Verdicts

| Page | Verdict |
|---|---|
| `bsuos-fixed-tariffs` | APPROVE |
| `gb-system-inertia-bid-and-offer-costs` | APPROVE |
| `balancing-services-use-of-system-bsuos-daily-forecast` | APPROVE |
| `daily-balancing-costs-balancing-services-use-of-system` | APPROVE |

0 blockers, 0 majors, 10 nits (1 + 2 + 2 + 5). The hold lines are accurate against the ledger on all four; the daily forecast
and daily cost "no settlement run to key them by" wording is true and survives, with plainer suggested wording (3.1, 4.1). No page
states a capture date, so the 16 October 2026-27 capture cannot make any page stale.
